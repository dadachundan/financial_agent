"""
zsxq_common.py — Shared constants and helpers for zsxq_downloader and zsxq_index.

Covers:
  - API constants and HTTP headers
  - Chrome / Selenium session setup
  - Filename sanitisation
  - Paginated file listing (with retry)
  - Download URL resolution and file download
  - SQLite database init and upsert (zsxq.db)
"""

import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import browser_cookie3
import requests

# ── Constants ─────────────────────────────────────────────────────────────────

API_BASE = "https://api.zsxq.com/v2"

SCRIPT_DIR              = Path(__file__).parent
DEFAULT_CHROME_PROFILE  = SCRIPT_DIR / "chrome_profile"
DEFAULT_DB              = SCRIPT_DIR / "db" / "zsxq.db"
DEFAULT_DOWNLOADS       = Path("~/Downloads/zsxq_reports").expanduser()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Referer":       "https://wx.zsxq.com/",
    "Origin":        "https://wx.zsxq.com",
    "zsxq-platform": "Web",
}


# ── Cookie / session ──────────────────────────────────────────────────────────

def get_session_via_selenium(chrome_profile: Path) -> requests.Session:
    """Build a requests.Session with zsxq cookies read from a Chrome profile."""
    cookie_file = chrome_profile / "Default" / "Cookies"
    if not cookie_file.exists():
        raise FileNotFoundError(f"Cookie file not found: {cookie_file}")

    print("Loading session cookies from Chrome profile...")
    cookies = list(browser_cookie3.chrome(
        cookie_file=str(cookie_file),
        domain_name=".zsxq.com",
    ))
    session = requests.Session()
    for c in cookies:
        session.cookies.set(c.name, c.value)
        session.cookies.set(c.name, c.value, domain="api.zsxq.com")

    print(f"Loaded {len(cookies)} cookies from Chrome profile.\n")
    return session


# ── Utilities ─────────────────────────────────────────────────────────────────

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def clean_zsxq_text(text: str) -> str:
    """Strip zsxq custom markup (e.g. <e type="hashtag" .../>) from text.

    Hashtag/mention tags are replaced with their decoded title so
    '#农产品#' becomes '#农产品' in the output.
    """
    if not text:
        return text

    def _replace(m: re.Match) -> str:
        title_m = re.search(r'title="([^"]*)"', m.group(0))
        if title_m:
            decoded = unquote(title_m.group(1)).strip('#').strip()
            return f'#{decoded}' if decoded else ''
        return ''

    text = re.sub(r'<e\b[^>]*/>', _replace, text)
    # Collapse runs of whitespace left by removed tags
    text = re.sub(r'[ \t]{2,}', ' ', text).strip()
    return text


# ── API: paginated file listing ────────────────────────────────────────────────

def fetch_files_page(
    session: requests.Session,
    group_id: str,
    count: int = 20,
    end_time: str | None = None,
    retries: int = 4,
) -> list[dict]:
    """Fetch one page of files. Returns list of raw file entries."""
    params: dict = {"count": count}
    if end_time:
        params["end_time"] = end_time

    url = f"{API_BASE}/groups/{group_id}/files"

    for attempt in range(retries):
        resp = session.get(url, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("succeeded"):
            return data["resp_data"].get("files", [])
        err = data.get("info") or data.get("error") or ""
        # Transient server errors — back off and retry
        if data.get("code") in (1059,) or "内部" in err:
            wait = 3 * (attempt + 1)
            print(f"    Transient error (attempt {attempt+1}/{retries}), "
                  f"retrying in {wait}s…")
            time.sleep(wait)
            continue
        raise RuntimeError(f"API error: {err}")

    raise RuntimeError(f"API error after {retries} retries")


def fetch_all_files(
    session: requests.Session,
    group_id: str,
    max_files: int = 0,
    delay: float = 0.5,
    from_date: str | None = None,
) -> list[dict]:
    """Paginate through files; return a flat list of entries.

    Args:
        max_files: Stop after this many files (0 = fetch everything).
        from_date: YYYY-MM-DD lower bound.  Pagination stops as soon as the
                   oldest entry on a page pre-dates this value; entries older
                   than from_date are excluded from the result.
    """
    all_entries: list[dict] = []
    end_time: str | None = None
    page = 0

    while True:
        page += 1
        page_size = min(max_files, 20) if (max_files and not end_time) else 20
        entries = fetch_files_page(session, group_id, count=page_size, end_time=end_time)
        if not entries:
            break

        if from_date:
            in_range = [e for e in entries
                        if e["file"]["create_time"][:10] >= from_date]
            all_entries.extend(in_range)
            print(f"  Page {page}: fetched {len(entries)} files "
                  f"(in range: {len(in_range)}, total so far: {len(all_entries)})")
            # Any entry fell outside the window — we've gone far enough back
            if len(in_range) < len(entries):
                break
        else:
            all_entries.extend(entries)
            print(f"  Page {page}: fetched {len(entries)} files "
                  f"(total so far: {len(all_entries)})")

        if max_files and len(all_entries) >= max_files:
            all_entries = all_entries[:max_files]
            break

        if len(entries) < 20:
            break  # last page

        oldest = min(entries, key=lambda e: e["file"]["create_time"])
        end_time = oldest["file"]["create_time"]
        time.sleep(delay)

    return all_entries


# ── API: download URL + file download ─────────────────────────────────────────

def get_download_url(session: requests.Session, file_id: int,
                     retries: int = 4) -> str | None:
    """Resolve a CDN download URL for a file. Retries on transient 1059 errors."""
    url = f"{API_BASE}/files/{file_id}/download_url"
    for attempt in range(retries):
        try:
            resp = session.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if data.get("succeeded"):
                return data["resp_data"]["download_url"]
            # 1059 = transient internal error — back off and retry
            if data.get("code") == 1059:
                wait = 3 * (attempt + 1)
                print(f"    ⚠ Download URL transient error for {file_id} "
                      f"(attempt {attempt+1}/{retries}), retrying in {wait}s…")
                time.sleep(wait)
                continue
            print(f"    ⚠ Download URL API error for file {file_id}: "
                  f"{data.get('info') or data}")
            return None
        except Exception as exc:
            print(f"    ⚠ Failed to get download URL for file {file_id}: {exc}")
            return None
    print(f"    ⚠ Download URL still failing after {retries} retries for file {file_id}")
    return None


def download_file(
    session: requests.Session, download_url: str, dest_path: Path
) -> int:
    """Stream-download a file to dest_path. Returns bytes written.

    Cleans up the partial file on any error (including KeyboardInterrupt).
    """
    resp = session.get(download_url, stream=True, headers=HEADERS)
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    try:
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=65536):
                fh.write(chunk)
                written += len(chunk)
    except BaseException:
        dest_path.unlink(missing_ok=True)
        raise
    return written


def date_subfolder(create_time: str | None) -> str:
    """Return a YYYY_MM_DD folder name from an ISO create_time string."""
    if create_time and len(create_time) >= 10:
        return create_time[:10].replace("-", "_")
    return datetime.now().strftime("%Y_%m_%d")


def do_download(
    session: requests.Session,
    file_id: int,
    name: str,
    downloads_dir: Path,
    create_time: str | None = None,
) -> tuple[str | None, bool]:
    """Fetch download URL and save the file.

    Files are saved into a date-named subfolder (YYYY_MM_DD) derived from
    create_time so downloads are grouped by publication date.

    Returns (local_path, success). local_path is None on failure.
    """
    dl_url = get_download_url(session, file_id)
    if not dl_url:
        print("           → could not get download URL")
        return None, False
    try:
        safe_name = sanitize_filename(name)
        sub = date_subfolder(create_time)
        dest = downloads_dir / sub / safe_name
        written = download_file(session, dl_url, dest)
        local_path = str(dest)
        print(f"           → saved {written/1024/1024:.1f}MB → {sub}/{dest.name}")
        return local_path, True
    except Exception as exc:
        print(f"           → download failed: {exc}")
        return None, False


# ── SQLite database ────────────────────────────────────────────────────────────

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
    tickers               TEXT,
    user_rating           INTEGER,
    tags                  TEXT,
    comment               TEXT
);

CREATE INDEX IF NOT EXISTS idx_create_time ON pdf_files(create_time);
CREATE INDEX IF NOT EXISTS idx_name        ON pdf_files(name);
"""

# Safe migrations: (sql, substring of error message to ignore)
MIGRATIONS: list[tuple[str, str]] = [
    ("ALTER TABLE pdf_files ADD COLUMN topic_json TEXT",              "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_analysis TEXT",    "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_robotics_related INTEGER",  "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_prompt TEXT",               "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ai_raw_response TEXT",         "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN tickers TEXT",                 "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_ai_related ON pdf_files(ai_robotics_related)",
     "already exists"),
    # v2 multi-category columns
    ("ALTER TABLE pdf_files ADD COLUMN ai_related           INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN robotics_related     INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN semiconductor_related INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN energy_related       INTEGER", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_analysis  TEXT",    "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_prompt    TEXT",    "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN categories_raw       TEXT",    "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_semiconductor ON pdf_files(semiconductor_related)",
     "already exists"),
    ("CREATE INDEX IF NOT EXISTS idx_energy ON pdf_files(energy_related)",
     "already exists"),
    ("ALTER TABLE pdf_files ADD COLUMN user_rating INTEGER", "duplicate column"),
    # v3 user annotations
    ("ALTER TABLE pdf_files ADD COLUMN tags    TEXT", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN comment TEXT", "duplicate column"),
    # v4 group tracking
    ("ALTER TABLE pdf_files ADD COLUMN group_id TEXT", "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_group_id ON pdf_files(group_id)", "already exists"),
]


def init_db(db_path: Path) -> sqlite3.Connection:
    """Open (or create) the zsxq SQLite database; return an open connection."""
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    for sql, ignore_fragment in MIGRATIONS:
        try:
            conn.execute(sql)
        except sqlite3.OperationalError as exc:
            if ignore_fragment.lower() not in str(exc).lower():
                raise
    conn.commit()
    return conn


def upsert_entry(conn: sqlite3.Connection, row: dict) -> None:
    """Insert or update a pdf_files row. Classification columns are preserved."""
    conn.execute(
        """
        INSERT INTO pdf_files
            (file_id, name, topic_id, topic_title, summary, topic_json,
             local_path, file_size, create_time, downloaded_at, indexed_at, group_id)
        VALUES
            (:file_id, :name, :topic_id, :topic_title, :summary, :topic_json,
             :local_path, :file_size, :create_time, :downloaded_at, :indexed_at, :group_id)
        ON CONFLICT(file_id) DO UPDATE SET
            name          = excluded.name,
            topic_id      = excluded.topic_id,
            topic_title   = excluded.topic_title,
            summary       = excluded.summary,
            topic_json    = excluded.topic_json,
            local_path    = COALESCE(excluded.local_path,    pdf_files.local_path),
            file_size     = excluded.file_size,
            create_time   = excluded.create_time,
            downloaded_at = COALESCE(excluded.downloaded_at, pdf_files.downloaded_at),
            indexed_at    = excluded.indexed_at,
            group_id      = COALESCE(excluded.group_id, pdf_files.group_id)
        """,
        row,
    )
