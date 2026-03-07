#!/usr/bin/env python3
"""
zsxq_index.py — Index zsxq PDFs with their summaries into a local SQLite database.

Fetches all files from a 知识星球 group, extracts the Chinese summary from each
file's associated topic (topic.talk.text), then stores file metadata + summary +
local download path in a SQLite database.

Usage:
    python zsxq_index.py                            # index all files
    python zsxq_index.py --last-x-files 10         # index only the 10 most recent files
    python zsxq_index.py --group-id 51111812185184 --db zsxq.db
    python zsxq_index.py --downloads ~/Downloads/zsxq_reports --count 50

    # Classify already-indexed PDFs as AI/Robotics-related via MiniMax:
    python zsxq_index.py --classify --minimax-key YOUR_KEY
    python zsxq_index.py --classify --minimax-key YOUR_KEY --reclassify   # redo all

    # Index + classify in one shot:
    python zsxq_index.py --last-x-files 10 --classify --minimax-key YOUR_KEY

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

API_BASE = "https://api.zsxq.com/v2"
MINIMAX_API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"
MINIMAX_MODEL = "MiniMax-Text-01"

SCRIPT_DIR = Path(__file__).parent
DEFAULT_CHROME_PROFILE = SCRIPT_DIR / "chrome_profile"
DEFAULT_DB = SCRIPT_DIR / "zsxq.db"
DEFAULT_DOWNLOADS = Path("~/Downloads/zsxq_reports").expanduser()

# ── Load config.py (search upward so worktree runs work too) ──────────────────
def _find_project_root() -> Path | None:
    """Walk up from SCRIPT_DIR until we find a directory containing config.py."""
    for parent in [SCRIPT_DIR, *SCRIPT_DIR.parents]:
        if (parent / "config.py").exists():
            return parent
    return None

_CONFIG_MINIMAX_KEY: str = ""
_project_root = _find_project_root()
if _project_root and str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
try:
    from config import MINIMAX_API_KEY as _CONFIG_MINIMAX_KEY  # type: ignore
except ImportError:
    pass

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
    ai_robotics_related   INTEGER
);

CREATE INDEX IF NOT EXISTS idx_create_time ON pdf_files(create_time);
CREATE INDEX IF NOT EXISTS idx_name        ON pdf_files(name);
"""

# Columns/indexes added after the initial schema — applied as safe migrations.
# Each entry is (sql, ignore_error_fragment) — the error fragment is matched
# against the exception message to suppress expected "already exists" errors.
MIGRATIONS: list[tuple[str, str]] = [
    ("ALTER TABLE pdf_files ADD COLUMN topic_json TEXT",            "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_analysis TEXT",  "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_related INTEGER","duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_ai_related ON pdf_files(ai_robotics_related)", "already exists"),
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
    "You are a financial research analyst. "
    "Your task is to determine whether a given research report is primarily about "
    "Artificial Intelligence (AI), Machine Learning, or Robotics. "
    "Respond with a brief analysis of 2-3 sentences, then on a new line write "
    "exactly one of: 'Answer: Yes' or 'Answer: No'."
)

CLASSIFY_USER_TMPL = """\
Report filename: {name}

Summary (Chinese):
{summary}

Is this report primarily about Artificial Intelligence (AI), Machine Learning, or Robotics?
"""


def classify_with_minimax(name: str, summary: str, api_key: str,
                           retries: int = 3) -> tuple[str, bool | None, float]:
    """Call MiniMax to classify a PDF as AI/Robotics-related.

    Returns (full_response_text, is_related, elapsed_seconds).
    is_related is True/False, or None if the answer could not be parsed.
    """
    user_msg = CLASSIFY_USER_TMPL.format(
        name=name,
        summary=summary.strip() if summary else "(no summary available)",
    )
    payload = {
        "model": MINIMAX_MODEL,
        "messages": [
            {"role": "system", "name": "MiniMax AI", "content": CLASSIFY_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        "stream": False,
        "temperature": 0.2,
        "max_completion_tokens": 300,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    for attempt in range(retries):
        try:
            t0 = time.monotonic()
            resp = requests.post(MINIMAX_API_URL, json=payload, headers=headers, timeout=30)
            elapsed = time.monotonic() - t0
            resp.raise_for_status()
            data = resp.json()
            text = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
            )
            # Parse the mandatory "Answer: Yes/No" line
            is_related: bool | None = None
            for line in reversed(text.splitlines()):
                line_stripped = line.strip().lower()
                if line_stripped.startswith("answer:"):
                    answer = line_stripped.replace("answer:", "").strip()
                    if answer.startswith("yes"):
                        is_related = True
                    elif answer.startswith("no"):
                        is_related = False
                    break
            if is_related is None:
                print(f"    ⚠ Could not parse Answer from MiniMax response. "
                      f"Raw reply:\n{text}")
            return text, is_related, elapsed
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f"    MiniMax error (attempt {attempt+1}/{retries}): {e}, "
                  f"retrying in {wait}s...")
            time.sleep(wait)

    return "", None, 0.0


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
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("succeeded"):
        return None
    return data["resp_data"]["download_url"]


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
    parser.add_argument("--classify", action="store_true",
                        help="After indexing, classify each PDF as AI/Robotics-related "
                             "via MiniMax. Skips rows that already have a classification.")
    parser.add_argument("--reclassify", action="store_true",
                        help="Re-run classification on ALL rows, overwriting existing results.")
    parser.add_argument("--minimax-key", default=None, metavar="KEY",
                        help="MiniMax API key. Falls back to config.py MINIMAX_API_KEY "
                             "or MINIMAX_API_KEY env var.")
    parser.add_argument("--classify-delay", type=float, default=1.0,
                        help="Seconds between MiniMax API calls (default: 1.0)")
    args = parser.parse_args()

    # --last-x-files takes precedence over --count
    if args.last_x_files:
        args.count = args.last_x_files

    chrome_profile = Path(args.chrome_profile).expanduser()
    if not chrome_profile.exists():
        print(f"ERROR: Chrome profile not found at {chrome_profile}")
        sys.exit(1)

    db_path = Path(args.db).expanduser()
    downloads_dir = Path(args.downloads).expanduser()

    # ── Startup banner ────────────────────────────────────────────────────────
    print("=" * 65)
    print("  zsxq_index.py")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Group   : {args.group_id}")
    print(f"  DB      : {db_path}")
    print(f"  Downloads: {downloads_dir}")
    limit_desc_banner = f"last {args.count}" if args.count else "all"
    print(f"  Fetch   : {limit_desc_banner} files")
    if args.classify:
        print(f"  Classify: YES (MiniMax, {'reclassify all' if args.reclassify else 'unclassified only'})")
    print("=" * 65)
    print()

    # Load session
    session = get_session_via_selenium(chrome_profile)

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

    # ── Optional MiniMax classification ──────────────────────────────────────
    if args.classify:
        import os
        minimax_key = (args.minimax_key
                       or _CONFIG_MINIMAX_KEY
                       or os.environ.get("MINIMAX_API_KEY", ""))
        if not minimax_key:
            print("\nERROR: --classify requires a MiniMax API key via "
                  "--minimax-key, config.py MINIMAX_API_KEY, or MINIMAX_API_KEY env var.")
        else:
            if args.reclassify:
                to_classify = conn.execute(
                    "SELECT file_id, name, summary, local_path "
                    "FROM pdf_files ORDER BY create_time DESC"
                ).fetchall()
            else:
                to_classify = conn.execute(
                    "SELECT file_id, name, summary, local_path "
                    "FROM pdf_files WHERE ai_robotics_related IS NULL "
                    "ORDER BY create_time DESC"
                ).fetchall()

            total_to_classify = len(to_classify)
            print(f"\nClassifying {total_to_classify} PDF(s) via MiniMax "
                  f"({'reclassify all' if args.reclassify else 'unclassified only'})...\n")

            yes_count = no_count = err_count = dl_ok = dl_fail = 0
            elapsed_times: list[float] = []
            t_classify_start = time.monotonic()

            for i, row in enumerate(to_classify, 1):
                file_id    = row["file_id"]
                name       = row["name"]
                summary    = row["summary"] or ""
                local_path = row["local_path"]

                # ETA
                if elapsed_times:
                    avg_s = sum(elapsed_times) / len(elapsed_times)
                    remaining = (total_to_classify - i + 1) * avg_s
                    eta_str = f"  ETA ~{remaining:.0f}s"
                else:
                    eta_str = ""

                pct = i / total_to_classify * 100
                print(f"  [{i}/{total_to_classify}] ({pct:.0f}%){eta_str}")
                print(f"    File: {name}")

                analysis, is_related, api_elapsed = classify_with_minimax(
                    name, summary, minimax_key
                )
                elapsed_times.append(api_elapsed + args.classify_delay)

                if is_related is True:
                    label = "YES ✓  (AI/Robotics-related)"
                    yes_count += 1
                elif is_related is False:
                    label = "NO  ✗  (not AI/Robotics)"
                    no_count += 1
                else:
                    label = "ERR ?  (could not parse answer)"
                    err_count += 1

                print(f"    Result : {label}  [{api_elapsed:.1f}s]")
                # Print full MiniMax analysis, indented
                if analysis:
                    for line in analysis.splitlines():
                        print(f"    MiniMax: {line}")

                # Auto-download if AI/Robotics-related and not yet on disk
                if is_related is True and not local_path:
                    print(f"           → AI-related: downloading...")
                    dl_url = get_download_url(session, file_id)
                    if dl_url:
                        safe_name = sanitize_filename(name)
                        dest = downloads_dir / safe_name
                        try:
                            written = download_file(session, dl_url, dest)
                            local_path = str(dest)
                            dl_ts = datetime.now().isoformat()
                            # Update in-memory tracker and persist to JSON
                            tracker[str(file_id)] = {
                                "name": name,
                                "path": local_path,
                                "size": written,
                                "downloaded_at": dl_ts,
                            }
                            save_tracker(downloads_dir, tracker)
                            print(f"           → saved {written/1024/1024:.1f}MB → {dest.name}")
                            dl_ok += 1
                        except Exception as e:
                            print(f"           → download failed: {e}")
                            dl_fail += 1
                    else:
                        print(f"           → could not get download URL")
                        dl_fail += 1

                conn.execute(
                    """UPDATE pdf_files
                       SET ai_robotics_analysis = ?,
                           ai_robotics_related  = ?,
                           local_path           = COALESCE(?, local_path),
                           downloaded_at        = COALESCE(
                               (SELECT downloaded_at FROM pdf_files WHERE file_id = ?),
                               ?),
                           indexed_at           = ?
                     WHERE file_id = ?""",
                    (analysis,
                     1 if is_related is True else (0 if is_related is False else None),
                     local_path,          # new local_path (None = keep existing)
                     file_id,             # for the sub-select
                     tracker.get(str(file_id), {}).get("downloaded_at"),
                     datetime.now().isoformat(),
                     file_id),
                )
                conn.commit()

                if i < len(to_classify):
                    time.sleep(args.classify_delay)

            t_classify_total = time.monotonic() - t_classify_start
            dl_msg = (f"\n  Auto-downloaded : {dl_ok} OK, {dl_fail} failed"
                      if (dl_ok or dl_fail) else "")
            print(f"\n{'='*65}")
            print(f"  Classification done in {t_classify_total:.1f}s")
            print(f"    YES (AI/Robotics) : {yes_count}")
            print(f"    NO                : {no_count}")
            print(f"    Parse errors      : {err_count}{dl_msg}")
            print(f"{'='*65}")

    conn.close()

    # Final stats from DB
    import sqlite3 as _sq3
    conn2 = _sq3.connect(db_path, timeout=10)
    final = conn2.execute(
        "SELECT COUNT(*) as total, "
        "SUM(CASE WHEN ai_robotics_related IS NULL THEN 1 ELSE 0 END) as unclassified, "
        "SUM(CASE WHEN ai_robotics_related = 1    THEN 1 ELSE 0 END) as yes_count, "
        "SUM(CASE WHEN ai_robotics_related = 0    THEN 1 ELSE 0 END) as no_count, "
        "SUM(CASE WHEN local_path IS NOT NULL     THEN 1 ELSE 0 END) as downloaded "
        "FROM pdf_files"
    ).fetchone()
    conn2.close()

    print(f"\n{'='*65}")
    print(f"  Done  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Indexing : inserted={inserted}  updated={updated}  skipped(non-PDF)={skipped}")
    print(f"  DB totals: {final['total']} rows  "
          f"| classified={( final['yes_count'] or 0)+(final['no_count'] or 0)}"
          f"  (yes={final['yes_count'] or 0}, no={final['no_count'] or 0})"
          f"  | unclassified={final['unclassified'] or 0}"
          f"  | downloaded={final['downloaded'] or 0}")
    print(f"  DB path  : {db_path}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
