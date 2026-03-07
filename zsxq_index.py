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
    file_id     INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    topic_id    INTEGER,
    topic_title TEXT,
    summary     TEXT,
    local_path  TEXT,
    file_size   INTEGER,
    create_time TEXT,
    downloaded_at TEXT,
    indexed_at  TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_create_time ON pdf_files(create_time);
CREATE INDEX IF NOT EXISTS idx_name ON pdf_files(name);
"""


def init_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def upsert_entry(conn: sqlite3.Connection, row: dict):
    conn.execute(
        """
        INSERT INTO pdf_files
            (file_id, name, topic_id, topic_title, summary, local_path,
             file_size, create_time, downloaded_at, indexed_at)
        VALUES
            (:file_id, :name, :topic_id, :topic_title, :summary, :local_path,
             :file_size, :create_time, :downloaded_at, :indexed_at)
        ON CONFLICT(file_id) DO UPDATE SET
            name         = excluded.name,
            topic_id     = excluded.topic_id,
            topic_title  = excluded.topic_title,
            summary      = excluded.summary,
            local_path   = COALESCE(excluded.local_path, pdf_files.local_path),
            file_size    = excluded.file_size,
            create_time  = excluded.create_time,
            downloaded_at = COALESCE(excluded.downloaded_at, pdf_files.downloaded_at),
            indexed_at   = excluded.indexed_at
        """,
        row,
    )


# ── Tracker (from zsxq_downloader.py) ────────────────────────────────────────

def load_tracker(downloads_dir: Path) -> dict:
    path = downloads_dir / "downloaded.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}


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

    # Load session
    session = get_session_via_selenium(chrome_profile)

    # Load local download tracker
    tracker = load_tracker(downloads_dir)
    print(f"Tracker has {len(tracker)} previously downloaded files.\n")

    # Open / create DB
    conn = init_db(db_path)
    print(f"Database: {db_path}\n")

    # Fetch files
    limit_desc = f"last {args.count}" if args.count else "all"
    print(f"Fetching {limit_desc} files from group {args.group_id}...")
    entries = fetch_all_files(session, args.group_id,
                              max_files=args.count, delay=args.delay)
    print(f"\nTotal files fetched: {len(entries)}\n")

    now = datetime.now().isoformat()
    inserted = updated = skipped = 0

    for entry in entries:
        f = entry["file"]
        topic = entry.get("topic") or {}
        talk = topic.get("talk") or {}

        file_id = f["file_id"]
        name = f["name"]

        # Only index PDFs
        if not name.lower().endswith(".pdf"):
            skipped += 1
            continue

        # Local path from tracker
        tracker_info = tracker.get(str(file_id)) or {}
        local_path = tracker_info.get("path")
        downloaded_at = tracker_info.get("downloaded_at")

        row = {
            "file_id": file_id,
            "name": name,
            "topic_id": topic.get("topic_id"),
            "topic_title": topic.get("title"),
            "summary": talk.get("text"),
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
        summary_len = len(row["summary"] or "")
        local_indicator = "✓ local" if local_path else "  remote"
        print(f"  [{status}] {name[:60]}")
        print(f"           summary={summary_len}chars  {local_indicator}")

        if existing:
            updated += 1
        else:
            inserted += 1

    conn.commit()
    conn.close()

    print(f"\nDone.")
    print(f"  Inserted: {inserted}")
    print(f"  Updated:  {updated}")
    print(f"  Skipped (non-PDF): {skipped}")
    print(f"  DB: {db_path}")


if __name__ == "__main__":
    main()
