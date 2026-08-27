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
import socket
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import requests

# ── Constants ─────────────────────────────────────────────────────────────────

API_BASE = "https://api.zsxq.com/v2"

from db_paths import db_path

SCRIPT_DIR              = Path(__file__).parent
local_profile           = SCRIPT_DIR / "chrome_profile"
DEFAULT_CHROME_PROFILE  = local_profile if local_profile.exists() else Path("~/Library/Application Support/Google/Chrome").expanduser()
DEFAULT_DB              = db_path("zsxq.db")
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

class ZsxqAuthError(RuntimeError):
    """Raised when zsxq rejects the current session cookies."""


def _raise_for_auth_or_status(resp: requests.Response, context: str) -> None:
    if resp.status_code in (401, 403):
        raise ZsxqAuthError(
            f"{context} rejected the current zsxq cookies "
            f"(HTTP {resp.status_code})."
        )
    resp.raise_for_status()


def get_session_via_selenium(
    chrome_profile: Path,
    *,
    use_json_cache: bool = True,
) -> requests.Session:
    """Build a requests.Session with zsxq cookies read from a Chrome profile."""
    import sys

    # 1) Try local JSON cache first to bypass keychain decryption issues
    cookie_json_path = chrome_profile / "zsxq_cookies.json"
    if use_json_cache and cookie_json_path.exists():
        import json
        print(f"Loading session cookies from JSON cache: {cookie_json_path}...")
        try:
            with open(cookie_json_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            session = requests.Session()
            for name, value in cookies.items():
                session.cookies.set(name, value)
                session.cookies.set(name, value, domain="api.zsxq.com")
                session.cookies.set(name, value, domain=".zsxq.com")
            print(f"Loaded {len(cookies)} cookies from JSON cache.\n")
            return session
        except Exception as e:
            print(f"Warning: Failed to load cookies from JSON cache: {e}. Falling back...")

    # 2) Fallback to browser_cookie3
    import browser_cookie3  # lazy: only the Selenium downloader needs this

    cookie_file = chrome_profile / "Default" / "Cookies"
    if not cookie_file.exists():
        raise FileNotFoundError(f"Cookie file not found: {cookie_file}")

    print("Loading session cookies from Chrome profile...")
    try:
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
    except Exception as exc:
        print(f"\nERROR: Failed to decrypt cookies from Chrome profile using browser_cookie3: {exc}")
        print("\nTo fix this on macOS:")
        print("1. Run the interactive login helper to generate a local cookie file:")
        print("   python3 login_zsxq.py")
        print("2. Once completed, re-run your downloader command.")
        sys.exit(1)



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
        try:
            resp = session.get(url, params=params, headers=HEADERS, timeout=30)
        except requests.exceptions.Timeout as exc:
            wait = 3 * (attempt + 1)
            print(f"    API timeout (attempt {attempt+1}/{retries}), retrying in {wait}s…")
            if attempt + 1 >= retries:
                raise RuntimeError(f"API timed out after {retries} retries") from exc
            time.sleep(wait)
            continue
        _raise_for_auth_or_status(resp, "File listing API")
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


# ── API: search files across all groups ───────────────────────────────────────

def fetch_search_files_page(
    session: requests.Session,
    query: str,
    count: int = 20,
    index: int = 0,
    retries: int = 4,
) -> tuple[list[dict], int]:
    """Search for files matching *query* across all joined groups (全部星球).

    Returns (entries, next_index). The search API paginates via an integer
    index offset, not end_time like the group file listing.
    """
    params: dict = {"keyword": query, "count": count}
    if index:
        params["index"] = index

    url = f"{API_BASE}/search/files"

    for attempt in range(retries):
        try:
            resp = session.get(url, params=params, headers=HEADERS, timeout=30)
        except requests.exceptions.Timeout as exc:
            wait = 3 * (attempt + 1)
            print(f"    Search API timeout (attempt {attempt+1}/{retries}), retrying in {wait}s…")
            if attempt + 1 >= retries:
                raise RuntimeError(f"Search API timed out after {retries} retries") from exc
            time.sleep(wait)
            continue
        _raise_for_auth_or_status(resp, "File search API")
        data = resp.json()
        if data.get("succeeded"):
            rd = data["resp_data"]
            return rd.get("files", []), rd.get("index", index + count)
        err = data.get("info") or data.get("error") or ""
        if data.get("code") in (1059,) or "内部" in err:
            wait = 3 * (attempt + 1)
            print(f"    Transient search error (attempt {attempt+1}/{retries}), "
                  f"retrying in {wait}s…")
            time.sleep(wait)
            continue
        raise RuntimeError(f"Search API error: {err}")

    raise RuntimeError(f"Search API error after {retries} retries")


def fetch_all_search_results(
    session: requests.Session,
    query: str,
    max_files: int = 0,
    delay: float = 0.5,
) -> list[dict]:
    """Paginate through all search results for *query*; return flat list of entries."""
    all_entries: list[dict] = []
    index = 0
    page = 0

    while True:
        page += 1
        entries, next_index = fetch_search_files_page(session, query, count=20, index=index)
        if not entries:
            break

        all_entries.extend(entries)
        print(f"  Search page {page}: fetched {len(entries)} files "
              f"(total so far: {len(all_entries)})")

        if max_files and len(all_entries) >= max_files:
            all_entries = all_entries[:max_files]
            break

        if len(entries) < 20:
            break  # last page

        index = next_index
        time.sleep(delay)

    return all_entries


# ── API: search topics across all groups ──────────────────────────────────────

def fetch_search_topics_page(
    session: requests.Session,
    query: str,
    count: int = 20,
    index: int = 0,
    retries: int = 4,
) -> tuple[list[dict], int]:
    """Search for topics matching *query* across all joined groups.

    Returns (topics, next_index).
    """
    params: dict = {"keyword": query, "count": count}
    if index:
        params["index"] = index

    url = f"{API_BASE}/search/topics"

    for attempt in range(retries):
        try:
            resp = session.get(url, params=params, headers=HEADERS, timeout=30)
        except requests.exceptions.Timeout as exc:
            wait = 3 * (attempt + 1)
            print(f"    Topics search timeout (attempt {attempt+1}/{retries}), retrying in {wait}s…")
            if attempt + 1 >= retries:
                raise RuntimeError(f"Topics search timed out after {retries} retries") from exc
            time.sleep(wait)
            continue
        _raise_for_auth_or_status(resp, "Topic search API")
        data = resp.json()
        if data.get("succeeded"):
            rd = data["resp_data"]
            return rd.get("topics", []), rd.get("index", index + count)
        err = data.get("info") or data.get("error") or ""
        if data.get("code") in (1059,) or "内部" in err:
            wait = 3 * (attempt + 1)
            print(f"    Transient topics search error (attempt {attempt+1}/{retries}), "
                  f"retrying in {wait}s…")
            time.sleep(wait)
            continue
        raise RuntimeError(f"Topics search API error: {err}")

    raise RuntimeError(f"Topics search API error after {retries} retries")


def fetch_all_search_topic_files(
    session: requests.Session,
    query: str,
    max_topics: int = 0,
    delay: float = 0.5,
) -> list[dict]:
    """Search topics for *query* and expand each topic's attachments to file entries.

    Returns a flat list in the same format as fetch_all_search_results so the
    two sources can be merged and deduplicated by file_id.

    max_topics: stop after this many topic pages-worth of topics (0 = all).
    """
    all_entries: list[dict] = []
    index = 0
    page = 0
    topics_seen = 0

    while True:
        page += 1
        topics, next_index = fetch_search_topics_page(session, query, count=20, index=index)
        if not topics:
            break

        topics_seen += len(topics)
        page_entries: list[dict] = []
        for item in topics:
            # /search/topics wraps each result as {"topic": {...}, "group": {...}}
            topic = item.get("topic") or item  # handle both wrapped and bare
            talk = topic.get("talk") or {}
            files = talk.get("files") or []
            group = item.get("group") or {}
            for f in files:
                page_entries.append({"file": f, "topic": topic, "group": group})

        all_entries.extend(page_entries)
        print(f"  Topics page {page}: {len(topics)} topics → {len(page_entries)} file(s) "
              f"(total so far: {len(all_entries)})")

        if max_topics and topics_seen >= max_topics:
            break

        if len(topics) < 20:
            break

        index = next_index
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
            _raise_for_auth_or_status(resp, "Download URL API")
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
        except ZsxqAuthError:
            raise
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
    resp = session.get(download_url, stream=True, headers=HEADERS, timeout=(15, 120))
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    # socket timeout covers stalled chunk reads that requests timeout= misses
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(120)
    try:
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=65536):
                fh.write(chunk)
                written += len(chunk)
    except BaseException:
        dest_path.unlink(missing_ok=True)
        raise
    finally:
        socket.setdefaulttimeout(old_timeout)
    return written


def get_pdf_page_count(path: str | Path) -> int | None:
    """Return the number of pages in a PDF file, or None on failure."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(path), strict=False)
        return len(reader.pages)
    except Exception:
        return None


# Ordered list of (canonical_name, [patterns_to_match_in_filename])
# Patterns are matched case-insensitively against the start of the filename.
_BANK_PATTERNS: list[tuple[str, list[str]]] = [
    ("Goldman Sachs",  ["Goldman Sachs", "GS-", "GS_", "高盛"]),
    ("Morgan Stanley", ["Morgan Stanley", "MS-", "MS_", "摩根士丹利"]),
    ("J.P. Morgan",    ["J.P. Morgan", "J.P.Morgan", "JPM-", "JPM_", "摩根大通"]),
    ("Deutsche Bank",  ["Deutsche Bank", "DB-", "DB_", "德意志银行", "德银"]),
    ("UBS",            ["UBS-", "UBS_", "瑞银"]),
    ("Bernstein",      ["Bernstein", "伯恩斯坦"]),
    ("Nomura",         ["Nomura", "野村"]),
    ("HSBC",           ["HSBC", "汇丰"]),
    ("BofA",           ["BofA Securities", "BofA-", "BofA_", "Bofa", "美银"]),
    ("Citi",           ["CITI", "Citi-", "Citi_", "花旗"]),
    ("Barclays",       ["Barclays"]),
    ("Jefferies",      ["Jefferies"]),
    ("Macquarie",      ["Macquarie"]),
    ("Credit Suisse",  ["Credit Suisse"]),
    ("Mizuho",         ["Mizuho"]),
    ("CLSA",           ["CLSA"]),
    ("Daiwa",          ["Daiwa"]),
    ("Haitong",        ["Haitong", "海通"]),
    ("CICC",           ["CICC", "中金"]),
]


def extract_bank(name: str) -> str | None:
    """Return the canonical investment bank name from a PDF filename, or None."""
    n = name.strip()
    # Strip CHS_ prefix used for some translations
    if n.startswith("CHS_"):
        n = n[4:]
    n_lower = n.lower()
    for canonical, patterns in _BANK_PATTERNS:
        for pat in patterns:
            if n_lower.startswith(pat.lower()):
                return canonical
    return None


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
    use_date_subfolder: bool = True,
) -> tuple[str | None, bool, int | None]:
    """Fetch download URL and save the file.

    When use_date_subfolder=True (default) files are saved into a YYYY_MM_DD
    subfolder; set False to save directly into downloads_dir.

    Returns (local_path, success, page_count). local_path is None on failure.
    """
    dl_url = get_download_url(session, file_id)
    if not dl_url:
        print("           → could not get download URL")
        return None, False, None
    try:
        safe_name = sanitize_filename(name)
        if use_date_subfolder:
            sub = date_subfolder(create_time)
            dest = downloads_dir / sub / safe_name
        else:
            dest = downloads_dir / safe_name
        written = download_file(session, dl_url, dest)
        local_path = str(dest)
        pages = get_pdf_page_count(dest)
        pages_str = f"  {pages}pp" if pages else ""
        rel = f"{sub}/{dest.name}" if use_date_subfolder else dest.name
        print(f"           → saved {written/1024/1024:.1f}MB{pages_str} → {rel}")
        return local_path, True, pages
    except Exception as exc:
        print(f"           → download failed: {exc}")
        return None, False, None


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
    # v5 claude recommendation rating
    ("ALTER TABLE pdf_files ADD COLUMN claude_rating INTEGER", "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_claude_rating ON pdf_files(claude_rating)", "already exists"),
    # v6 pdf page count
    ("ALTER TABLE pdf_files ADD COLUMN page_count INTEGER", "duplicate column"),
    # v7 investment bank
    ("ALTER TABLE pdf_files ADD COLUMN bank TEXT", "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_bank ON pdf_files(bank)", "already exists"),
    # v8 skipped flag
    ("ALTER TABLE pdf_files ADD COLUMN skipped INTEGER DEFAULT 0", "duplicate column"),
    # v9 search query term
    ("ALTER TABLE pdf_files ADD COLUMN query_term TEXT", "duplicate column"),
    ("CREATE INDEX IF NOT EXISTS idx_query_term ON pdf_files(query_term)", "already exists"),
    # v10 OCR cache columns (also created ad-hoc by the zsxq-analyze ocr_pdf.py;
    # declared here so a fresh DB carries the full schema).
    ("ALTER TABLE pdf_files ADD COLUMN ocr_text TEXT", "duplicate column"),
    ("ALTER TABLE pdf_files ADD COLUMN ocr_at   TEXT", "duplicate column"),
]


# ── Full-text search (FTS5) + agent-curated card layer ──────────────────────
#
# pdf_files_fts: a trigram-tokenised FTS5 index over the short, high-signal text
# columns, so retrieval works across the bilingual (English + 中文) corpus. The
# default unicode61 tokenizer treats a space-free CJK run as one token, so a
# substring query like '手术机器人' fails to match '直觉外科手术机器人'; the
# 'trigram' tokenizer indexes every 3-char window and matches CJK and Latin
# substrings alike (minimum query length 3 chars). ocr_text (full PDF text) is
# deliberately NOT indexed — it is large and only needed once a PDF is already
# picked for a deep read; leaving it out bounds the trigram index size.
_FTS_DDL = """
CREATE VIRTUAL TABLE IF NOT EXISTS pdf_files_fts USING fts5(
    name, topic_title, summary, tickers, bank, tags, comment,
    content='pdf_files', content_rowid='file_id', tokenize='trigram'
);

CREATE TRIGGER IF NOT EXISTS pdf_files_fts_ai AFTER INSERT ON pdf_files BEGIN
    INSERT INTO pdf_files_fts(rowid, name, topic_title, summary, tickers, bank, tags, comment)
    VALUES (new.file_id, new.name, new.topic_title, new.summary, new.tickers, new.bank, new.tags, new.comment);
END;

CREATE TRIGGER IF NOT EXISTS pdf_files_fts_ad AFTER DELETE ON pdf_files BEGIN
    INSERT INTO pdf_files_fts(pdf_files_fts, rowid, name, topic_title, summary, tickers, bank, tags, comment)
    VALUES ('delete', old.file_id, old.name, old.topic_title, old.summary, old.tickers, old.bank, old.tags, old.comment);
END;

CREATE TRIGGER IF NOT EXISTS pdf_files_fts_au AFTER UPDATE ON pdf_files BEGIN
    INSERT INTO pdf_files_fts(pdf_files_fts, rowid, name, topic_title, summary, tickers, bank, tags, comment)
    VALUES ('delete', old.file_id, old.name, old.topic_title, old.summary, old.tickers, old.bank, old.tags, old.comment);
    INSERT INTO pdf_files_fts(rowid, name, topic_title, summary, tickers, bank, tags, comment)
    VALUES (new.file_id, new.name, new.topic_title, new.summary, new.tickers, new.bank, new.tags, new.comment);
END;
"""

# pdf_cards: the agent-curated "card" written back each time Claude deep-reads a
# PDF (see zsxq_cards.py). It turns the sparse native metadata (only ~5% of rows
# carry tickers) into a structured index that grows over the PDFs actually used.
# The embedding / embed_model columns are reserved for an optional future local
# (no-API) semantic layer; they stay NULL until/unless that layer is built.
_CARDS_DDL = """
CREATE TABLE IF NOT EXISTS pdf_cards (
    file_id              INTEGER PRIMARY KEY,
    covered_tickers      TEXT,
    primary_ticker       TEXT,
    theme                TEXT,
    thesis               TEXT,
    has_comparison_table INTEGER DEFAULT 0,
    key_tables           TEXT,
    key_figures          TEXT,
    rating               TEXT,
    card_json            TEXT,
    embedding            BLOB,
    embed_model          TEXT,
    updated_at           TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_cards_primary ON pdf_cards(primary_ticker);
CREATE INDEX IF NOT EXISTS idx_cards_theme   ON pdf_cards(theme);
"""


def ensure_search_schema(conn: sqlite3.Connection) -> None:
    """Create the FTS5 index + card table and backfill the FTS from existing
    rows. Idempotent; safe to call on every init_db(). Wrapped in try/except so
    a search-layer problem can never block the core downloader/upsert path.
    """
    try:
        # An external-content FTS5 table reports count(*) from the *content*
        # table even when its index is empty, so emptiness can't gate the
        # backfill. Instead detect whether the table existed before this call:
        # if we're creating it now, rebuild once to index all historical rows.
        # On later calls the triggers keep it in sync, so we skip the rebuild.
        fts_existed = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='pdf_files_fts'"
        ).fetchone() is not None
        conn.executescript(_FTS_DDL)
        conn.executescript(_CARDS_DDL)
        if not fts_existed:
            base_rows = conn.execute("SELECT count(*) FROM pdf_files").fetchone()[0]
            if base_rows:
                conn.execute("INSERT INTO pdf_files_fts(pdf_files_fts) VALUES('rebuild')")
    except sqlite3.OperationalError as exc:
        print(f"⚠ zsxq search schema init skipped: {exc}")


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
    ensure_search_schema(conn)
    conn.commit()
    return conn


def upsert_entry(conn: sqlite3.Connection, row: dict) -> None:
    """Insert or update a pdf_files row. Classification columns are preserved."""
    conn.execute(
        """
        INSERT INTO pdf_files
            (file_id, name, topic_id, topic_title, summary, topic_json,
             local_path, file_size, create_time, downloaded_at, indexed_at, group_id,
             query_term)
        VALUES
            (:file_id, :name, :topic_id, :topic_title, :summary, :topic_json,
             :local_path, :file_size, :create_time, :downloaded_at, :indexed_at, :group_id,
             :query_term)
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
            group_id      = COALESCE(excluded.group_id, pdf_files.group_id),
            query_term    = COALESCE(pdf_files.query_term,   excluded.query_term)
        """,
        {**row, "query_term": row.get("query_term")},
    )


def set_claude_rating(conn: sqlite3.Connection, file_id: int, rating: int | None) -> int:
    """Set the agent-curated ``claude_rating`` (0-5 stars, or None to clear) on a
    pdf_files row. This is the sanctioned write path for the ``claude_rating``
    column — callers must go through here rather than raw SQL. Returns the number
    of rows updated (0 if the file_id does not exist)."""
    if rating is not None and not (0 <= int(rating) <= 5):
        raise ValueError(f"claude_rating must be 0-5 or None, got {rating!r}")
    cur = conn.execute(
        "UPDATE pdf_files SET claude_rating = ? WHERE file_id = ?",
        (int(rating) if rating is not None else None, int(file_id)),
    )
    conn.commit()
    return cur.rowcount
