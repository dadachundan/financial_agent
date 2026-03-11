#!/usr/bin/env python3
"""
zsxq_index.py — Index zsxq PDFs with their summaries into a local SQLite database.

Fetches all files from a 知识星球 group, extracts the Chinese summary from each
file's associated topic (topic.talk.text), then stores file metadata + summary +
local download path in a SQLite database.

Usage:
    python zsxq_index.py                        # index + auto-classify all files
    python zsxq_index.py --last-x-files 10     # index only the 10 most recent files
    python zsxq_index.py --group-id 51111812185184 --db zsxq.db
    python zsxq_index.py --downloads ~/Downloads/zsxq_reports --count 50
    python zsxq_index.py --reclassify          # re-classify every row (even if done before)
    python zsxq_index.py --cleanup-non-ai      # delete local PDFs classified as NOT AI/Robotics

    # Offline multi-category re-classification (no website scraping):
    python zsxq_index.py --classify-db                  # classify unclassified rows only
    python zsxq_index.py --classify-db --reclassify-categories  # reclassify all rows

Classification via MiniMax runs automatically after indexing — unclassified rows only.
MiniMax API key is read from config.py (MINIMAX_API_KEY) in the project root.
The script also reads the tracker JSON written by zsxq_downloader.py to populate
the local_path column for files that have already been downloaded.
"""

import argparse
import json
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from minimax import call_minimax, MINIMAX_API_KEY as _CONFIG_MINIMAX_KEY, project_root as _project_root  # type: ignore

API_BASE = "https://api.zsxq.com/v2"

SCRIPT_DIR = Path(__file__).parent
DEFAULT_CHROME_PROFILE = SCRIPT_DIR / "chrome_profile"
DEFAULT_DB = SCRIPT_DIR / "zsxq.db"
DEFAULT_DOWNLOADS = Path("~/Downloads/zsxq_reports").expanduser()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://wx.zsxq.com/",
    "Origin": "https://wx.zsxq.com",
}


# ── Selenium / session ────────────────────────────────────────────────────────

def get_session_via_selenium(chrome_profile: Path) -> requests.Session:
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={chrome_profile}")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("Starting Chrome to load session cookies...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    try:
        driver.get("https://wx.zsxq.com")
        time.sleep(2)
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"],
                                domain=cookie.get("domain", ""))
    finally:
        driver.quit()

    print(f"Loaded {len(session.cookies)} cookies from Chrome profile.\n")
    return session


# ── API helpers ───────────────────────────────────────────────────────────────

def fetch_files_page(session: requests.Session, group_id: str,
                     count: int = 20, end_time: str | None = None,
                     retries: int = 4) -> list[dict]:
    """Fetch one page of files. Returns list of raw file entries."""
    params: dict = {"count": count}
    if end_time:
        params["end_time"] = end_time

    url = f"{API_BASE}/groups/{group_id}/files"

    for attempt in range(retries):
        resp = session.get(url, params=params, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if data.get("succeeded"):
            return data["resp_data"].get("files", [])
        err = data.get("info") or data.get("error") or ""
        # Transient server errors — back off and retry
        if data.get("code") in (1059,) or "内部" in err:
            wait = 3 * (attempt + 1)
            print(f"    Transient error (attempt {attempt+1}/{retries}), "
                  f"retrying in {wait}s...")
            time.sleep(wait)
            continue
        raise RuntimeError(f"API error: {err}")

    raise RuntimeError(f"API error after {retries} retries")


def fetch_all_files(session: requests.Session, group_id: str,
                    max_files: int = 0, delay: float = 0.5) -> list[dict]:
    """Paginate through all files, returning a flat list of entries.

    Args:
        max_files: Stop after this many files (0 = fetch everything).
                   When set, the first API page uses min(max_files, 20)
                   as its count so small limits need only one round-trip.
    """
    all_entries: list[dict] = []
    end_time: str | None = None
    page = 0

    while True:
        page += 1
        # Optimise: if we only need a few files, ask for exactly that many
        # on the first (and only) page rather than always asking for 20.
        page_size = min(max_files, 20) if (max_files and not end_time) else 20
        entries = fetch_files_page(session, group_id, count=page_size, end_time=end_time)
        if not entries:
            break

        all_entries.extend(entries)
        print(f"  Page {page}: fetched {len(entries)} files "
              f"(total so far: {len(all_entries)})")

        if max_files and len(all_entries) >= max_files:
            all_entries = all_entries[:max_files]
            break

        if len(entries) < 20:
            break  # last page

        # Use the oldest create_time as the cursor for next page
        oldest = min(entries, key=lambda e: e["file"]["create_time"])
        end_time = oldest["file"]["create_time"]
        time.sleep(delay)

    return all_entries


# ── SQLite ────────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS pdf_files (
    file_id               INTEGER PRIMARY KEY,
    name                  TEXT    NOT NULL,
    topic_id              INTEGER,
    topic_title           TEXT,
    summary               TEXT,
    topic_json            TEXT,
    local_path            TEXT,
    file_size             INTEGER,
    create_time           TEXT,
    downloaded_at         TEXT,
    indexed_at            TEXT    NOT NULL,
    ai_robotics_analysis  TEXT,
    ai_robotics_related   INTEGER,
    ai_prompt             TEXT,
    ai_raw_response       TEXT,
    tickers               TEXT
);

CREATE INDEX IF NOT EXISTS idx_create_time ON pdf_files(create_time);
CREATE INDEX IF NOT EXISTS idx_name        ON pdf_files(name);
"""

# Columns/indexes added after the initial schema — applied as safe migrations.
# Each entry is (sql, ignore_error_fragment) — the error fragment is matched
# against the exception message to suppress expected "already exists" errors.
MIGRATIONS: list[tuple[str, str]] = [
    ("ALTER TABLE pdf_files ADD COLUMN topic_json TEXT",             "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_analysis TEXT",   "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_related INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_prompt TEXT",              "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_raw_response TEXT",        "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN tickers TEXT",                "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_ai_related ON pdf_files(ai_robotics_related)", "already exists"),
    # v2 multi-category columns
    ("ALTER TABLE pdf_files ADD COLUMN ai_related          INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN robotics_related    INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN semiconductor_related INTEGER","duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN energy_related      INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_analysis TEXT",    "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_prompt   TEXT",    "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_raw      TEXT",    "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_semiconductor ON pdf_files(semiconductor_related)", "already exists"),
    ("CREATE INDEX IF NOT EXISTS idx_energy        ON pdf_files(energy_related)",        "already exists"),
]


def init_db(db_path: Path) -> sqlite3.Connection:
    # timeout=30: wait up to 30 s for the lock instead of raising immediately.
    # WAL mode: readers don't block writers (and vice-versa), which prevents
    # "database is locked" when another process still has the file open.
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    # Apply any migrations that haven't been run yet
    for sql, ignore_fragment in MIGRATIONS:
        try:
            conn.execute(sql)
        except sqlite3.OperationalError as e:
            if ignore_fragment.lower() not in str(e).lower():
                raise
    conn.commit()
    return conn


def _topic_to_json(topic: dict) -> str | None:
    """Serialize topic to JSON, stripping fields that contain personal/auth data."""
    if not topic:
        return None
    exclude = {"user_specific", "latest_likes", "likes_detail", "group"}
    clean = {k: v for k, v in topic.items() if k not in exclude}
    return json.dumps(clean, ensure_ascii=False)


def _full_title(topic: dict) -> str | None:
    """Return the un-truncated topic title.

    The API's ``title`` field is capped at ~15 chars and ends with '…'.
    The real full title is always the first non-empty line of talk.text.
    """
    text = (topic.get("talk") or {}).get("text") or ""
    first_line = text.split("\n")[0].strip()
    if first_line:
        return first_line
    # Fallback to the API title (may be truncated)
    return topic.get("title")


# ── MiniMax classification ────────────────────────────────────────────────────

CLASSIFY_SYSTEM = (
    "You are a financial research analyst. Given a research report summary, classify it "
    "across four product-focused categories and extract tickers.\n\n"
    "Respond in exactly this format (one item per line, nothing else):\n"
    "  AI: Yes or No\n"
    "  Robotics: Yes or No\n"
    "  Semiconductor: Yes or No\n"
    "  Energy: Yes or No\n"
    "  Tickers: TICK1, TICK2, ...  (or Tickers: None)\n"
    "  Analysis: <2-3 sentence summary of the report's specific product focus>\n\n"
    "Mark Yes only when the report focuses on specific, commercially available or "
    "near-market products — not just broad sector exposure or macro themes.\n\n"
    "Category definitions:\n"
    "- AI: specific AI products with market presence — LLMs and applications "
    "(DeepSeek, Kimi, Doubao, Qwen, ChatGPT, Gemini, Claude, Grok), "
    "AI inference/training chips (H100/B200/Blackwell, Ascend 910, Kunlun, Cambrian MLU), "
    "AI agents or copilot software products with named deployments.\n"
    "- Robotics: specific robot hardware products — humanoid robots "
    "(Tesla Optimus, Figure 02, Unitree H1/G1/B2, Fourier GR1, 宇树/傅利叶/智元/开普勒), "
    "commercial collaborative robots (cobots), commercially deployed autonomous-driving "
    "systems (Waymo, 萝卜快跑), autonomous delivery drones.\n"
    "- Semiconductor: specific chip or process products — advanced packaging "
    "(CoWoS, SoIC, FOPLP, Chiplet interconnects), high-bandwidth memory "
    "(HBM2e / HBM3 / HBM3E), leading-edge logic nodes (3 nm / 2 nm / 1.4 nm), "
    "power semiconductors (SiC / GaN MOSFETs), NAND / DRAM product generations, "
    "named EDA tools (Synopsys / Cadence / 华大九天).\n"
    "- Energy: specific energy products — named battery chemistries (LFP, NCM, "
    "solid-state, sodium-ion), large-scale BESS (battery energy storage systems), "
    "grid inverters, solar module technologies (TOPCon / HJT / perovskite), "
    "small modular reactors (SMR / 小型堆).\n"
    "Tickers: A-share 6-digit codes, HK codes, US symbols explicitly referenced only."
)

CLASSIFY_USER_TMPL = """\
Report filename: {name}

Summary (Chinese):
{summary}

Classify this report. Mark Yes only when the report discusses specific products \
that are commercially available or near-market — not just broad sector themes or \
macro policy discussion. Extract tickers that are explicitly named.
"""


def _parse_yes_no(text: str, label: str) -> bool | None:
    """Find 'Label: Yes/No' in text, return True/False/None."""
    for line in text.splitlines():
        ls = line.strip().lower()
        if ls.startswith(f"{label.lower()}:"):
            val = ls.split(":", 1)[1].strip()
            if val.startswith("yes"):
                return True
            if val.startswith("no"):
                return False
    return None


def classify_with_minimax(
    name: str, summary: str, api_key: str, retries: int = 3
) -> tuple[str, bool | None, bool | None, bool | None, bool | None, str, float, str, str]:
    """Call MiniMax to classify a PDF across 4 categories and extract tickers.

    Returns:
        (analysis, ai_rel, robotics_rel, semiconductor_rel, energy_rel,
         tickers, elapsed_seconds, prompt_sent, raw_json)
    All bool fields are True/False, or None if the answer could not be parsed.
    """
    user_msg = CLASSIFY_USER_TMPL.format(
        name=name,
        summary=summary.strip() if summary else "(no summary available)",
    )
    text, elapsed, raw_json = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": CLASSIFY_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.1,
        max_completion_tokens=300,
        retries=retries,
        api_key=api_key,
    )

    ai_rel   = _parse_yes_no(text, "AI")
    rob_rel  = _parse_yes_no(text, "Robotics")
    semi_rel = _parse_yes_no(text, "Semiconductor")
    nrg_rel  = _parse_yes_no(text, "Energy")

    if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]) and text:
        print(f"    ⚠ Could not parse all categories. Raw reply:\n{text}")

    # Extract tickers
    tickers = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("tickers:"):
            raw_t = ls[len("tickers:"):].strip()
            if raw_t.lower() not in ("none", "n/a", ""):
                tickers = raw_t
            break

    # Extract analysis line
    analysis = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("analysis:"):
            analysis = ls[len("analysis:"):].strip()
            break
    if not analysis:
        analysis = text  # fallback: store full response

    return analysis, ai_rel, rob_rel, semi_rel, nrg_rel, tickers, elapsed, user_msg, raw_json


def upsert_entry(conn: sqlite3.Connection, row: dict):
    conn.execute(
        """
        INSERT INTO pdf_files
            (file_id, name, topic_id, topic_title, summary, topic_json,
             local_path, file_size, create_time, downloaded_at, indexed_at)
        VALUES
            (:file_id, :name, :topic_id, :topic_title, :summary, :topic_json,
             :local_path, :file_size, :create_time, :downloaded_at, :indexed_at)
        ON CONFLICT(file_id) DO UPDATE SET
            name          = excluded.name,
            topic_id      = excluded.topic_id,
            topic_title   = excluded.topic_title,
            summary       = excluded.summary,
            topic_json    = excluded.topic_json,
            local_path    = COALESCE(excluded.local_path, pdf_files.local_path),
            file_size     = excluded.file_size,
            create_time   = excluded.create_time,
            downloaded_at = COALESCE(excluded.downloaded_at, pdf_files.downloaded_at),
            indexed_at    = excluded.indexed_at
        """,
        row,
    )


# ── Download helpers (mirrors zsxq_downloader.py) ────────────────────────────

def sanitize_filename(name: str) -> str:
    import re
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def get_download_url(session: requests.Session, file_id: int) -> str | None:
    url = f"{API_BASE}/files/{file_id}/download_url"
    try:
        resp = session.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("succeeded"):
            print(f"    ⚠ Download URL API error for file {file_id}: {data.get('info') or data}")
            return None
        return data["resp_data"]["download_url"]
    except Exception as e:
        print(f"    ⚠ Failed to get download URL for file {file_id}: {e}")
        return None


def download_file(session: requests.Session, download_url: str, dest_path: Path) -> int:
    resp = session.get(download_url, stream=True, headers=HEADERS)
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
            written += len(chunk)
    return written


# ── Tracker (from zsxq_downloader.py) ────────────────────────────────────────

def load_tracker(downloads_dir: Path) -> dict:
    path = downloads_dir / "downloaded.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_tracker(downloads_dir: Path, tracker: dict) -> None:
    path = downloads_dir / "downloaded.json"
    path.write_text(json.dumps(tracker, indent=2, ensure_ascii=False))


def _do_download(session: requests.Session, file_id: int, name: str,
                 downloads_dir: Path, tracker: dict) -> tuple[str | None, bool]:
    """Fetch download URL and save the file to disk. Updates tracker in-place.

    Returns (local_path, success). local_path is None on failure.
    """
    dl_url = get_download_url(session, file_id)
    if not dl_url:
        print(f"           → could not get download URL")
        return None, False
    try:
        safe_name = sanitize_filename(name)
        dest = downloads_dir / safe_name
        written = download_file(session, dl_url, dest)
        local_path = str(dest)
        dl_ts = datetime.now().isoformat()
        tracker[str(file_id)] = {
            "name": name, "path": local_path,
            "size": written, "downloaded_at": dl_ts,
        }
        save_tracker(downloads_dir, tracker)
        print(f"           → saved {written/1024/1024:.1f}MB → {dest.name}")
        return local_path, True
    except Exception as e:
        print(f"           → download failed: {e}")
        return None, False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Index zsxq PDFs with summaries into a local SQLite database."
    )
    parser.add_argument("--group-id", default="51111812185184")
    parser.add_argument("--db", default=str(DEFAULT_DB),
                        help=f"SQLite database path (default: {DEFAULT_DB})")
    parser.add_argument("--downloads", default=str(DEFAULT_DOWNLOADS),
                        help="Directory used by zsxq_downloader.py "
                             f"(default: {DEFAULT_DOWNLOADS})")
    parser.add_argument("--count", type=int, default=0,
                        help="Max files to index (0 = all). Alias: use --last-x-files.")
    parser.add_argument("--last-x-files", type=int, default=0, metavar="N",
                        help="Index only the N most recent files. "
                             "Overrides --count when specified. "
                             "For N≤20 a single API call is made.")
    parser.add_argument("--chrome-profile", default=str(DEFAULT_CHROME_PROFILE))
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Seconds between paginated API calls")
    # ── MiniMax classification ──
    parser.add_argument("--reclassify", action="store_true",
                        help="Re-classify ALL rows with legacy AI/Robotics prompt, "
                             "overwriting existing results.")
    parser.add_argument("--classify-delay", type=float, default=1.0,
                        help="Seconds between MiniMax API calls (default: 1.0)")
    # ── Offline multi-category classification (no scraping) ──
    parser.add_argument("--classify-db", action="store_true",
                        help="Skip website scraping entirely. Read rows from the local DB "
                             "and run multi-category classification (AI / Robotics / "
                             "Semiconductor / Energy / Tickers). Auto-downloads any file "
                             "that matches at least one category.")
    parser.add_argument("--reclassify-categories", action="store_true",
                        help="Used with --classify-db: reclassify ALL rows, not just "
                             "unclassified ones.")
    # ── Cleanup ──
    parser.add_argument("--cleanup-non-ai", action="store_true",
                        help="Delete local PDF files that are classified as NOT AI/Robotics "
                             "(ai_robotics_related=0). Clears local_path in DB and tracker. "
                             "Unclassified files are never touched.")
    args = parser.parse_args()

    # --last-x-files takes precedence over --count
    if args.last_x_files:
        args.count = args.last_x_files

    db_path       = Path(args.db).expanduser()
    downloads_dir = Path(args.downloads).expanduser()

    # ── Shared: Chrome session (used by both modes for authenticated downloads) ─
    chrome_profile = Path(args.chrome_profile).expanduser()
    if not chrome_profile.exists():
        print(f"ERROR: Chrome profile not found at {chrome_profile}")
        sys.exit(1)
    session = get_session_via_selenium(chrome_profile)

    # ── Offline mode: --classify-db skips all scraping ───────────────────────
    if args.classify_db:
        if not _CONFIG_MINIMAX_KEY:
            print("ERROR: MINIMAX_API_KEY not found in config.py")
            sys.exit(1)
        if not db_path.exists():
            print(f"ERROR: DB not found at {db_path}. Run without --classify-db first.")
            sys.exit(1)

        conn = init_db(db_path)
        tracker = load_tracker(downloads_dir)

        print("=" * 65)
        print("  zsxq_index.py  [--classify-db  offline mode]")
        print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  DB       : {db_path}")
        print(f"  Downloads: {downloads_dir}")
        mode_str = "reclassify ALL" if args.reclassify_categories else "unclassified only"
        print(f"  Mode     : {mode_str}")
        print("=" * 65)
        print()

        if args.reclassify_categories:
            to_classify = conn.execute(
                "SELECT file_id, name, summary, local_path FROM pdf_files "
                "ORDER BY create_time DESC"
            ).fetchall()
        else:
            to_classify = conn.execute(
                "SELECT file_id, name, summary, local_path FROM pdf_files "
                "WHERE ai_related IS NULL ORDER BY create_time DESC"
            ).fetchall()

        total = len(to_classify)
        if total == 0:
            print("All rows already classified. Use --reclassify-categories to redo.")
            conn.close()
            sys.exit(0)

        print(f"Classifying {total} row(s) via MiniMax multi-category prompt...\n")
        counts = {"ai": 0, "robotics": 0, "semiconductor": 0, "energy": 0,
                  "dl_ok": 0, "dl_fail": 0, "err": 0}
        elapsed_times: list[float] = []
        t_start = time.monotonic()

        for i, row in enumerate(to_classify, 1):
            file_id    = row["file_id"]
            name       = row["name"]
            summary    = row["summary"] or ""
            local_path = row["local_path"]

            eta_str = ""
            if elapsed_times:
                avg_s = sum(elapsed_times) / len(elapsed_times)
                eta_str = f"  ETA ~{(total - i + 1) * avg_s:.0f}s"

            print(f"  [{i}/{total}] ({i/total*100:.0f}%){eta_str}")
            print(f"    File: {name}")

            analysis, ai_rel, rob_rel, semi_rel, nrg_rel, tickers, api_elapsed, prompt, raw_json = \
                classify_with_minimax(name, summary, _CONFIG_MINIMAX_KEY)

            elapsed_times.append(api_elapsed + args.classify_delay)

            if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]):
                counts["err"] += 1

            flags = []
            if ai_rel:    flags.append("AI");            counts["ai"] += 1
            if rob_rel:   flags.append("Robotics");      counts["robotics"] += 1
            if semi_rel:  flags.append("Semiconductor"); counts["semiconductor"] += 1
            if nrg_rel:   flags.append("Energy");        counts["energy"] += 1

            label = ("✓ " + ", ".join(flags)) if flags else "✗ None"
            print(f"    Categories : {label}  [{api_elapsed:.1f}s]")
            if tickers:
                print(f"    Tickers    : {tickers}")
            if analysis:
                print(f"    Analysis   : {analysis}")

            # Auto-download if any category matched and not yet on disk
            if any([ai_rel, rob_rel, semi_rel, nrg_rel]) and not local_path:
                dest = downloads_dir / sanitize_filename(name)
                if dest.exists():
                    local_path = str(dest)
                    print(f"           → already on disk: {dest.name}")
                else:
                    print(f"           → category match: downloading...")
                    local_path, ok = _do_download(session, file_id, name, downloads_dir, tracker)
                    if ok:
                        counts["dl_ok"] += 1
                    else:
                        counts["dl_fail"] += 1

            conn.execute(
                """UPDATE pdf_files
                   SET ai_related           = ?,
                       robotics_related     = ?,
                       semiconductor_related= ?,
                       energy_related       = ?,
                       tickers              = COALESCE(?, tickers),
                       categories_analysis  = ?,
                       categories_prompt    = ?,
                       categories_raw       = ?,
                       local_path           = COALESCE(?, local_path),
                       indexed_at           = ?
                 WHERE file_id = ?""",
                (1 if ai_rel   is True else (0 if ai_rel   is False else None),
                 1 if rob_rel  is True else (0 if rob_rel  is False else None),
                 1 if semi_rel is True else (0 if semi_rel is False else None),
                 1 if nrg_rel  is True else (0 if nrg_rel  is False else None),
                 tickers or None,
                 analysis, prompt, raw_json,
                 local_path,
                 datetime.now().isoformat(),
                 file_id),
            )
            conn.commit()

            if i < total:
                time.sleep(args.classify_delay)

        t_total = time.monotonic() - t_start
        dl_msg = (f"\n  Auto-downloaded : {counts['dl_ok']} OK, {counts['dl_fail']} failed"
                  if counts["dl_ok"] or counts["dl_fail"] else "")
        print(f"\n{'='*65}")
        print(f"  Classification done in {t_total:.1f}s  ({total} rows)")
        print(f"    AI           : {counts['ai']}")
        print(f"    Robotics     : {counts['robotics']}")
        print(f"    Semiconductor: {counts['semiconductor']}")
        print(f"    Energy       : {counts['energy']}")
        print(f"    Parse errors : {counts['err']}{dl_msg}")
        print(f"{'='*65}")
        conn.close()
        sys.exit(0)

    # ── Normal mode: scrape website ───────────────────────────────────────────
    # ── Startup banner ────────────────────────────────────────────────────────
    print("=" * 65)
    print("  zsxq_index.py")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Group   : {args.group_id}")
    print(f"  DB      : {db_path}")
    print(f"  Downloads: {downloads_dir}")
    limit_desc_banner = f"last {args.count}" if args.count else "all"
    print(f"  Fetch   : {limit_desc_banner} files")
    classify_mode = "reclassify all" if args.reclassify else "unclassified only"
    print(f"  Classify: {'MiniMax (' + classify_mode + ')' if _CONFIG_MINIMAX_KEY else 'skipped (no API key)'}")
    print("=" * 65)
    print()

    # Load local download tracker
    tracker = load_tracker(downloads_dir)
    print(f"Tracker has {len(tracker)} previously downloaded files.\n")

    # Open / create DB
    conn = init_db(db_path)
    # Show DB stats on open
    stats = conn.execute(
        "SELECT COUNT(*) as total, "
        "SUM(CASE WHEN ai_robotics_related IS NULL THEN 1 ELSE 0 END) as unclassified, "
        "SUM(CASE WHEN ai_robotics_related = 1    THEN 1 ELSE 0 END) as yes_count, "
        "SUM(CASE WHEN ai_robotics_related = 0    THEN 1 ELSE 0 END) as no_count, "
        "SUM(CASE WHEN local_path IS NOT NULL     THEN 1 ELSE 0 END) as downloaded "
        "FROM pdf_files"
    ).fetchone()
    print(f"Database : {db_path}")
    print(f"  Rows   : {stats['total']}  "
          f"(classified: {(stats['yes_count'] or 0) + (stats['no_count'] or 0)}, "
          f"unclassified: {stats['unclassified'] or 0}, "
          f"downloaded: {stats['downloaded'] or 0})")
    print()

    # Fetch files
    limit_desc = f"last {args.count}" if args.count else "all"
    print(f"Fetching {limit_desc} files from group {args.group_id}...")
    t_fetch_start = time.monotonic()
    entries = fetch_all_files(session, args.group_id,
                              max_files=args.count, delay=args.delay)
    t_fetch = time.monotonic() - t_fetch_start
    print(f"\nTotal files fetched: {len(entries)}  ({t_fetch:.1f}s)\n")

    now = datetime.now().isoformat()
    inserted = updated = skipped = 0
    pdf_entries = [e for e in entries if e["file"]["name"].lower().endswith(".pdf")]
    non_pdf    = len(entries) - len(pdf_entries)
    print(f"Indexing {len(pdf_entries)} PDFs "
          f"({'skipping ' + str(non_pdf) + ' non-PDF, ' if non_pdf else ''}"
          f"writing to {db_path.name})...\n")

    for idx, entry in enumerate(entries, 1):
        f = entry["file"]
        topic = entry.get("topic") or {}
        talk = topic.get("talk") or {}

        file_id = f["file_id"]
        name = f["name"]

        # Only index PDFs
        if not name.lower().endswith(".pdf"):
            skipped += 1
            print(f"  [{idx}/{len(entries)}] SKIP (non-PDF) {name[:60]}")
            continue

        # Local path from tracker
        tracker_info = tracker.get(str(file_id)) or {}
        local_path = tracker_info.get("path")
        downloaded_at = tracker_info.get("downloaded_at")

        size_mb = (f.get("size") or 0) / 1024 / 1024
        summary_text = talk.get("text") or ""

        row = {
            "file_id": file_id,
            "name": name,
            "topic_id": topic.get("topic_id"),
            # Full title derived from first line of talk.text (API title is truncated)
            "topic_title": _full_title(topic),
            "summary": summary_text,
            # Complete raw topic payload for future use
            "topic_json": _topic_to_json(topic),
            "local_path": local_path,
            "file_size": f.get("size"),
            "create_time": f.get("create_time"),
            "downloaded_at": downloaded_at,
            "indexed_at": now,
        }

        # Check if already in DB
        existing = conn.execute(
            "SELECT file_id FROM pdf_files WHERE file_id = ?", (file_id,)
        ).fetchone()

        upsert_entry(conn, row)

        status = "updated" if existing else "inserted"
        local_indicator = "✓ local" if local_path else "  remote"
        create_date = (f.get("create_time") or "")[:10]
        print(f"  [{idx}/{len(entries)}] [{status}] {name[:58]}")
        print(f"           date={create_date}  size={size_mb:.1f}MB  "
              f"summary={len(summary_text)}chars  {local_indicator}")

        if existing:
            updated += 1
        else:
            inserted += 1

    conn.commit()

    # ── MiniMax classification (always runs; skips already-classified rows) ──
    minimax_key = _CONFIG_MINIMAX_KEY
    if not minimax_key:
        print("\nSkipping classification: MINIMAX_API_KEY not found in config.py "
              f"(looked in: {_project_root or 'not found'})")
    else:
        limit_sql = f" LIMIT {args.count}" if args.count > 0 else ""
        if args.reclassify:
            to_classify = conn.execute(
                "SELECT file_id, name, summary, local_path "
                f"FROM pdf_files ORDER BY create_time DESC{limit_sql}"
            ).fetchall()
        else:
            to_classify = conn.execute(
                "SELECT file_id, name, summary, local_path "
                f"FROM pdf_files WHERE ai_related IS NULL "
                f"ORDER BY create_time DESC{limit_sql}"
            ).fetchall()

        total_to_classify = len(to_classify)
        if total_to_classify == 0:
            print("\nClassification: all rows already classified, nothing to do.")
        else:
            print(f"\nClassifying {total_to_classify} PDF(s) via MiniMax "
                  f"({'reclassify all' if args.reclassify else 'unclassified only'})...\n")

            counts = {"ai": 0, "robotics": 0, "semiconductor": 0, "energy": 0,
                      "dl_ok": 0, "dl_fail": 0, "err": 0}
            elapsed_times: list[float] = []
            t_classify_start = time.monotonic()

            for i, row in enumerate(to_classify, 1):
                file_id    = row["file_id"]
                name       = row["name"]
                summary    = row["summary"] or ""
                local_path = row["local_path"]

                if elapsed_times:
                    avg_s = sum(elapsed_times) / len(elapsed_times)
                    eta_str = f"  ETA ~{(total_to_classify - i + 1) * avg_s:.0f}s"
                else:
                    eta_str = ""

                pct = i / total_to_classify * 100
                print(f"  [{i}/{total_to_classify}] ({pct:.0f}%){eta_str}")
                print(f"    File: {name}")

                analysis, ai_rel, rob_rel, semi_rel, nrg_rel, tickers, api_elapsed, prompt_sent, raw_json = \
                    classify_with_minimax(name, summary, minimax_key)
                elapsed_times.append(api_elapsed + args.classify_delay)

                if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]):
                    counts["err"] += 1

                flags = []
                if ai_rel:    flags.append("AI");            counts["ai"] += 1
                if rob_rel:   flags.append("Robotics");      counts["robotics"] += 1
                if semi_rel:  flags.append("Semiconductor"); counts["semiconductor"] += 1
                if nrg_rel:   flags.append("Energy");        counts["energy"] += 1

                label = ("✓ " + ", ".join(flags)) if flags else "✗ None"
                print(f"    Categories : {label}  [{api_elapsed:.1f}s]")
                if tickers:
                    print(f"    Tickers    : {tickers}")
                if analysis:
                    print(f"    Analysis   : {analysis}")

                # Auto-download if any category matched and not yet on disk
                if any([ai_rel, rob_rel, semi_rel, nrg_rel]) and not local_path:
                    dest = downloads_dir / sanitize_filename(name)
                    if dest.exists():
                        local_path = str(dest)
                        print(f"           → already on disk: {dest.name}")
                    else:
                        print(f"           → category match: downloading...")
                        local_path, ok = _do_download(session, file_id, name, downloads_dir, tracker)
                        if ok:
                            counts["dl_ok"] += 1
                        else:
                            counts["dl_fail"] += 1

                conn.execute(
                    """UPDATE pdf_files
                       SET ai_related            = ?,
                           robotics_related      = ?,
                           semiconductor_related = ?,
                           energy_related        = ?,
                           tickers               = COALESCE(?, tickers),
                           categories_analysis   = ?,
                           categories_prompt     = ?,
                           categories_raw        = ?,
                           local_path            = COALESCE(?, local_path),
                           indexed_at            = ?
                     WHERE file_id = ?""",
                    (1 if ai_rel   is True else (0 if ai_rel   is False else None),
                     1 if rob_rel  is True else (0 if rob_rel  is False else None),
                     1 if semi_rel is True else (0 if semi_rel is False else None),
                     1 if nrg_rel  is True else (0 if nrg_rel  is False else None),
                     tickers or None,
                     analysis, prompt_sent, raw_json,
                     local_path,
                     datetime.now().isoformat(),
                     file_id),
                )
                conn.commit()

                if i < len(to_classify):
                    time.sleep(args.classify_delay)

            t_classify_total = time.monotonic() - t_classify_start
            dl_msg = (f"\n  Auto-downloaded : {counts['dl_ok']} OK, {counts['dl_fail']} failed"
                      if (counts["dl_ok"] or counts["dl_fail"]) else "")
            print(f"\n{'='*65}")
            print(f"  Classification done in {t_classify_total:.1f}s")
            print(f"    AI           : {counts['ai']}")
            print(f"    Robotics     : {counts['robotics']}")
            print(f"    Semiconductor: {counts['semiconductor']}")
            print(f"    Energy       : {counts['energy']}")
            print(f"    Parse errors : {counts['err']}{dl_msg}")
            print(f"{'='*65}")

    # ── Cleanup: delete local PDFs that are NOT AI/Robotics-related ─────────
    if args.cleanup_non_ai:
        import os
        non_ai = conn.execute(
            "SELECT file_id, name, local_path FROM pdf_files "
            "WHERE ai_robotics_related = 0 AND local_path IS NOT NULL"
        ).fetchall()

        if not non_ai:
            print("\nCleanup: no non-AI PDFs with a local file found.")
        else:
            print(f"\nCleanup: {len(non_ai)} non-AI PDF(s) to delete:\n")
            for r in non_ai:
                print(f"  {r['name'][:70]}")
                print(f"    {r['local_path']}")

            print(f"\nDeleting {len(non_ai)} file(s)...")
            deleted = skipped_missing = 0
            for r in non_ai:
                path = Path(r["local_path"])
                if path.exists():
                    path.unlink()
                    deleted += 1
                    print(f"  ✓ deleted  {path.name}")
                else:
                    skipped_missing += 1
                    print(f"  ⚠ missing  {path.name}")

                # Clear local_path in DB
                conn.execute(
                    "UPDATE pdf_files SET local_path = NULL, downloaded_at = NULL "
                    "WHERE file_id = ?", (r["file_id"],)
                )
                # Remove from tracker JSON
                tracker.pop(str(r["file_id"]), None)

            conn.commit()
            save_tracker(downloads_dir, tracker)
            print(f"\n  Deleted: {deleted}  |  Already missing: {skipped_missing}")
            print(f"  DB local_path cleared, tracker updated.")

    conn.close()

    # Final stats from DB
    import sqlite3 as _sq3
    conn2 = _sq3.connect(db_path, timeout=10)
    conn2.row_factory = _sq3.Row
    final = conn2.execute(
        "SELECT COUNT(*) as total, "
        "SUM(CASE WHEN ai_robotics_related IS NULL THEN 1 ELSE 0 END) as unclassified, "
        "SUM(CASE WHEN ai_robotics_related = 1    THEN 1 ELSE 0 END) as yes_count, "
        "SUM(CASE WHEN ai_robotics_related = 0    THEN 1 ELSE 0 END) as no_count, "
        "SUM(CASE WHEN local_path IS NOT NULL     THEN 1 ELSE 0 END) as downloaded, "
        "SUM(CASE WHEN ai_related          = 1    THEN 1 ELSE 0 END) as cat_ai, "
        "SUM(CASE WHEN robotics_related    = 1    THEN 1 ELSE 0 END) as cat_robotics, "
        "SUM(CASE WHEN semiconductor_related=1    THEN 1 ELSE 0 END) as cat_semi, "
        "SUM(CASE WHEN energy_related      = 1    THEN 1 ELSE 0 END) as cat_energy "
        "FROM pdf_files"
    ).fetchone()
    conn2.close()

    print(f"\n{'='*65}")
    print(f"  Done  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Indexing   : inserted={inserted}  updated={updated}  skipped(non-PDF)={skipped}")
    print(f"  Legacy cls : yes={final['yes_count'] or 0}  no={final['no_count'] or 0}"
          f"  unclassified={final['unclassified'] or 0}")
    print(f"  Categories : AI={final['cat_ai'] or 0}  Robotics={final['cat_robotics'] or 0}"
          f"  Semiconductor={final['cat_semi'] or 0}  Energy={final['cat_energy'] or 0}")
    print(f"  Downloaded : {final['downloaded'] or 0} / {final['total']} total")
    print(f"  DB path    : {db_path}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
