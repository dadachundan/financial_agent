"""
kg_services.py — Business-logic services for the knowledge graph.

Covers:
  - File upload helper
  - URL-fetching + LLM summarisation (for the "mine from URL" feature)
  - PDF text extraction
  - LLM entity extraction
  - DB upsert for extracted entities
"""

import io
import json
import platform
import re
import sqlite3
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

import pdfplumber  # type: ignore

from minimax import call_minimax, MINIMAX_API_KEY  # type: ignore

# ── Constants ─────────────────────────────────────────────────────────────────

ALLOWED_IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
ALLOWED_PDF_EXT = {".pdf"}

# Prompts live here so they can be changed without touching route handlers.
_SUMMARIZE_SYSTEM = (
    "You are analysing a web article about the semiconductor / tech industry. "
    "Given article text and two entities, return a JSON object with exactly two keys: "
    "\"comment\" (one sentence ≤ 20 words summarising the relationship) and "
    "\"explanation\" (two to four sentences with detail, citing specific facts). "
    "Return only valid JSON, no markdown fences."
)

_COMPARE_SYSTEM = (
    "You are a tech-industry analyst. Given several company–business relationship descriptions, "
    "compare the companies' competitive positions in those business domains. "
    "Return a concise structured Markdown report with sections: "
    "## Overview, ## Competitive Strengths & Weaknesses (per company), ## Market Positioning Summary. "
    "Be factual and cite specific details from the provided text. "
    "Return only Markdown, no JSON or code fences."
)

_PDF_SYSTEM = (
    "You are a financial-document analyser specialising in the tech/semiconductor industry. "
    "Given document text, extract:\n"
    "  1. Companies mentioned — prefer ticker symbols (e.g. NVDA, AMD, TSMC); "
    "     if a ticker is not obvious, use the company name.\n"
    "  2. Business domains / verticals each company operates in "
    "(e.g. GPU, CPU, Memory, Manufacturing, Cloud, AI, Networking, Storage, Mobile SoC, EUV Lithography, etc.).\n\n"
    "Return ONLY valid JSON with this exact structure (no markdown fences):\n"
    "{\n"
    '  "companies": [{"ticker": "NVDA", "name": "NVIDIA", "description": "..."}],\n'
    '  "businesses": [{"name": "GPU", "description": "..."}],\n'
    '  "relationships": [{"company_ticker": "NVDA", "business": "GPU", "comment": "one-liner"}]\n'
    "}"
)


# ── Input validation helpers (mechanical enforcement) ─────────────────────────

def _require_str(value: Any, field: str) -> str:
    """Return stripped string; raise ValueError if empty."""
    s = (value or "").strip()
    if not s:
        raise ValueError(f"'{field}' is required and must not be empty")
    return s


def _parse_rating(value: Any) -> int:
    """Coerce to int in [0, 5]; defaults to 0 on bad input."""
    try:
        r = int(value or 0)
    except (TypeError, ValueError):
        return 0
    return max(0, min(5, r))


# ── File upload ───────────────────────────────────────────────────────────────

def save_upload(request_files, file_field: str, upload_dir: Path) -> str:
    """Save an uploaded image; return the filename (relative) or ''."""
    f = request_files.get(file_field)
    if not f or not f.filename:
        return ""
    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_IMG_EXT:
        return ""
    fname = uuid.uuid4().hex + ext
    f.save(upload_dir / fname)
    return fname


# ── URL summarisation ─────────────────────────────────────────────────────────

def _clean_html(raw: str, limit: int = 8000) -> str:
    """Strip scripts, boilerplate blocks, and all HTML tags; return plain text."""
    text = re.sub(r"<(script|style)[^>]*>.*?</(script|style)>", " ", raw,
                  flags=re.IGNORECASE | re.DOTALL)
    for tag in ("nav", "footer", "header", "aside", "form"):
        text = re.sub(rf"<{tag}[\s>].*?</{tag}>", " ", text,
                      flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()[:limit]


def _fetch_direct(url: str, max_bytes: int = 200_000) -> str:
    """Plain urllib fetch — fast but blocked by some sites."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read(max_bytes).decode("utf-8", errors="replace")
    return _clean_html(raw)


def _fetch_chrome(url: str, page_load_timeout: int = 20) -> str:
    """
    Open Chrome with the user's profile for cookies/auth; fall back to a
    fresh profile if the profile directory is locked by a running Chrome.
    """
    from selenium import webdriver                          # type: ignore
    from selenium.webdriver.chrome.options import Options  # type: ignore
    from selenium.webdriver.chrome.service import Service  # type: ignore
    from webdriver_manager.chrome import ChromeDriverManager  # type: ignore

    service = Service(ChromeDriverManager().install())

    # Build candidate (user-data-dir, profile-dir) pairs.
    # Try the real Chrome profile first for cookies; fall back to a fresh one.
    candidates: list[tuple[str | None, str | None]] = []
    if platform.system() == "Darwin":
        profile_root = Path.home() / "Library/Application Support/Google/Chrome"
        if profile_root.exists():
            candidates.append((str(profile_root), "Default"))
    candidates.append((None, None))   # fresh temp profile as last resort

    last_err: Exception = RuntimeError("Chrome fetch: no candidates tried")
    for user_data_dir, profile_dir in candidates:
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        if user_data_dir:
            opts.add_argument(f"--user-data-dir={user_data_dir}")
            opts.add_argument(f"--profile-directory={profile_dir}")

        try:
            driver = webdriver.Chrome(service=service, options=opts)
        except Exception as exc:
            last_err = exc
            print(f"[fetch_chrome] driver launch failed ({user_data_dir}): {exc}")
            continue

        try:
            driver.set_page_load_timeout(page_load_timeout)
            driver.get(url)
            time.sleep(2)            # let JS render
            return _clean_html(driver.page_source)
        except Exception as exc:
            last_err = exc
            print(f"[fetch_chrome] navigation failed ({user_data_dir}): {exc}")
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    raise RuntimeError(f"Chrome fetch failed for {url}: {last_err}") from last_err


def fetch_url_text(url: str, max_bytes: int = 200_000) -> str:
    """
    Fetch URL and return stripped plain text.
    Tries a direct HTTP request first; if that is blocked or fails, falls
    back to opening headless Chrome with the user's Chrome profile so that
    cookies / site logins are available.
    """
    try:
        return _fetch_direct(url, max_bytes)
    except Exception as direct_err:
        print(f"[fetch_url_text] direct fetch failed ({direct_err}), trying Chrome…")
        try:
            return _fetch_chrome(url)
        except Exception as chrome_err:
            raise RuntimeError(
                f"Both direct and Chrome fetch failed.\n"
                f"  direct : {direct_err}\n"
                f"  chrome : {chrome_err}"
            ) from chrome_err


def llm_summarize_url(url: str, entity_a: str, entity_b: str) -> dict:
    """
    Fetch URL, call MiniMax, return {"comment": ..., "explanation": ...}.
    Raises ValueError if inputs are empty; RuntimeError on API/parse failure.
    """
    url      = _require_str(url,      "url")
    entity_a = _require_str(entity_a, "entity_a")
    entity_b = _require_str(entity_b, "entity_b")

    text = fetch_url_text(url)

    if not MINIMAX_API_KEY:
        return {
            "comment":     f"[API key missing] Relationship between {entity_a} and {entity_b}",
            "explanation": text[:400],
            "source_text": text,
        }

    user_msg = (
        f"Article text (truncated):\n\"\"\"\n{text}\n\"\"\"\n\n"
        f"Describe the relationship between \"{entity_a}\" and \"{entity_b}\" "
        "based ONLY on the article above."
    )

    print("\n" + "=" * 60)
    print("SUMMARIZE URL — MiniMax prompt")
    print("=" * 60)
    print("[SYSTEM]", _SUMMARIZE_SYSTEM)
    print("[USER]",   user_msg[:1000])
    print("=" * 60 + "\n")

    reply, _, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": _SUMMARIZE_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.2,
        max_completion_tokens=512,
    )
    result = json.loads(reply.strip())
    result["_system_prompt"] = _SUMMARIZE_SYSTEM
    result["_user_prompt"]   = user_msg
    result["source_text"]    = text
    return result


# ── BC comparison ────────────────────────────────────────────────────────────

def llm_compare_bc(rows: list) -> dict:
    """
    Compare multiple BC relationships using MiniMax.
    rows: list of dicts with keys business_name, company_name, comment, explanation, source_text.
    Returns {"markdown": "...", "_user_prompt": "..."}.
    """
    if not MINIMAX_API_KEY:
        raise RuntimeError("MINIMAX_API_KEY not configured")

    sections = []
    for i, r in enumerate(rows, 1):
        text = (r.get("source_text") or r.get("explanation") or "").strip()
        comment = (r.get("comment") or "").strip()
        sections.append(
            f"[{i}] {r['company_name']} in {r['business_name']}\n"
            f"Comment: {comment}\n"
            f"Article text: {text[:1500] if text else '(none)'}"
        )

    user_msg = "Relationships to compare:\n\n" + "\n\n---\n\n".join(sections)

    print("\n" + "=" * 60)
    print("COMPARE BC — MiniMax prompt")
    print("=" * 60)
    print("[SYSTEM]", _COMPARE_SYSTEM)
    print("[USER]",   user_msg[:600])
    print("=" * 60 + "\n")

    reply, _, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": _COMPARE_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.3,
        max_completion_tokens=1024,
    )
    return {"markdown": reply.strip(), "_user_prompt": user_msg}


# ── PDF entity extraction ─────────────────────────────────────────────────────

def extract_pdf_text(pdf_bytes: bytes, max_pages: int = 3) -> str:
    """Extract plain text from the first *max_pages* pages of a PDF."""
    pages_text = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages[:max_pages]:
            t = page.extract_text() or ""
            pages_text.append(t.strip())
    return "\n\n".join(pages_text).strip()


def llm_extract_entities(raw_text: str) -> dict:
    """
    Send PDF text to MiniMax; return parsed JSON dict with keys
    companies / businesses / relationships.
    Raises RuntimeError if MINIMAX_API_KEY is missing or parse fails.
    """
    if not MINIMAX_API_KEY:
        raise RuntimeError("MINIMAX_API_KEY not configured")

    user_msg = (
        f"Document text (first 3 pages):\n\"\"\"\n{raw_text[:6000]}\n\"\"\"\n\n"
        "Extract companies, businesses, and their relationships as JSON."
    )

    print("\n" + "=" * 60)
    print("PDF IMPORT — MiniMax prompt")
    print("=" * 60)
    print("[SYSTEM]", _PDF_SYSTEM)
    print("[USER]",   user_msg)
    print("=" * 60 + "\n")

    reply, _, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": _PDF_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.1,
        max_completion_tokens=1024,
    )
    print("PDF IMPORT — MiniMax reply:", reply[:500])

    # Strip optional markdown fences
    clean = reply.strip()
    if clean.startswith("```"):
        clean = "\n".join(clean.splitlines()[1:])
    if clean.endswith("```"):
        clean = clean[: clean.rfind("```")]
    return json.loads(clean.strip())


_ZSXQ_DB_PATH: "Path | None" = None


def set_zsxq_db_path(path: "Path") -> None:
    global _ZSXQ_DB_PATH
    _ZSXQ_DB_PATH = path


def get_zsxq_db_path() -> "Path":
    if _ZSXQ_DB_PATH is None:
        raise RuntimeError("zsxq DB path not set; pass --zsxq-db")
    return _ZSXQ_DB_PATH


def zsxq_import_stream(kg_conn: sqlite3.Connection):
    """
    Generator: yields SSE-formatted strings with live progress, then a final
    'done' event carrying the summary JSON.

    Each yielded line is either:
      data: {"type": "log",  "msg": "..."}\\n\\n
      data: {"type": "done", "processed": N, "skipped": N, "added": {...}, "errors": [...]}\\n\\n
    """
    import sqlite3 as _sq3

    def _sse(obj: dict) -> str:
        return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"

    zsxq_conn = _sq3.connect(get_zsxq_db_path())
    zsxq_conn.row_factory = _sq3.Row

    imported_ids = {
        r["file_id"]
        for r in kg_conn.execute("SELECT file_id FROM zsxq_imported").fetchall()
    }

    all_rows = zsxq_conn.execute("""
        SELECT file_id, name, summary, local_path
        FROM pdf_files
        WHERE summary IS NOT NULL AND summary != ''
          AND local_path IS NOT NULL AND local_path != ''
    """).fetchall()
    zsxq_conn.close()

    rows = [r for r in all_rows if r["file_id"] not in imported_ids]
    total = len(rows)
    skipped = len(all_rows) - total

    yield _sse({"type": "log", "msg": f"Found {total} new rows to process, {skipped} already imported."})

    total_companies: list[str]  = []
    total_businesses: list[str] = []
    total_bc: list[str]         = []
    errors: list[str]           = []
    processed = 0

    for i, row in enumerate(rows, 1):
        file_id    = row["file_id"]
        name       = row["name"] or f"file_id={file_id}"
        source_url = f"/zsxq-pdf/{file_id}"

        short_name = name[:60] + ("…" if len(name) > 60 else "")
        yield _sse({"type": "log", "msg": f"[{i}/{total}] Calling MiniMax for: {short_name}"})

        user_msg = (
            f"Document summary:\n\"\"\"\n{row['summary'][:6000]}\n\"\"\"\n\n"
            "Extract companies, businesses, and their relationships as JSON."
        )
        print(f"\n[zsxq {i}/{total}] MiniMax prompt — SYSTEM: {_PDF_SYSTEM[:120]}… USER: {user_msg[:200]}…\n")
        try:
            reply, elapsed, _ = call_minimax(
                messages=[
                    {"role": "system", "name": "MiniMax AI", "content": _PDF_SYSTEM},
                    {"role": "user",   "name": "User",       "content": user_msg},
                ],
                temperature=0.1,
                max_completion_tokens=1024,
            )
            clean = reply.strip()
            if clean.startswith("```"):
                clean = "\n".join(clean.splitlines()[1:])
            if clean.endswith("```"):
                clean = clean[: clean.rfind("```")]
            extracted = json.loads(clean.strip())
        except Exception as exc:
            msg = f"  ✗ LLM/parse error: {exc}"
            errors.append(f"file_id {file_id}: {exc}")
            yield _sse({"type": "log", "msg": msg})
            kg_conn.execute("INSERT OR IGNORE INTO zsxq_imported (file_id) VALUES (?)", (file_id,))
            kg_conn.commit()
            continue

        added, row_errors = upsert_pdf_entities(kg_conn, extracted, source_url)
        kg_conn.commit()

        total_companies.extend(added["companies"])
        total_businesses.extend(added["businesses"])
        total_bc.extend(added["bc_links"])
        errors.extend([f"file_id {file_id}: {e}" for e in row_errors])

        cos  = ", ".join(added["companies"])  or "—"
        bizs = ", ".join(added["businesses"]) or "—"
        bcs  = ", ".join(added["bc_links"])   or "—"
        yield _sse({"type": "log", "msg": f"  ✓ companies: {cos} | businesses: {bizs} | links: {bcs} ({elapsed:.1f}s)"})

        kg_conn.execute("INSERT OR IGNORE INTO zsxq_imported (file_id) VALUES (?)", (file_id,))
        kg_conn.commit()
        processed += 1

    yield _sse({
        "type":      "done",
        "processed": processed,
        "skipped":   skipped,
        "added": {
            "companies":  list(dict.fromkeys(total_companies)),
            "businesses": list(dict.fromkeys(total_businesses)),
            "bc_links":   total_bc,
        },
        "errors": errors,
    })


def upsert_pdf_entities(
    conn: sqlite3.Connection,
    extracted: dict,
    pdf_source: str,
) -> tuple[dict, list[str]]:
    """
    Upsert companies, businesses, and bc relationships extracted from a PDF.

    Args:
        conn:       Open SQLite connection (will be written but not committed).
        extracted:  Dict with keys companies / businesses / relationships.
        pdf_source: Value stored in source_url for each new relationship.

    Returns:
        (added, errors) where added = {"companies": [...], "businesses": [...], "bc_links": [...]}
    """
    added_companies  = []
    added_businesses = []
    added_bc         = []
    errors: list[str] = []

    for co in extracted.get("companies", []):
        ticker = (co.get("ticker") or co.get("name") or "").strip()
        desc   = (co.get("description") or "").strip()
        if not ticker:
            continue
        try:
            conn.execute(
                "INSERT OR IGNORE INTO companies (name, description) VALUES (?,?)",
                (ticker, desc),
            )
            added_companies.append(ticker)
        except Exception as exc:
            errors.append(f"company {ticker}: {exc}")

    for biz in extracted.get("businesses", []):
        bname = (biz.get("name") or "").strip()
        bdesc = (biz.get("description") or "").strip()
        if not bname:
            continue
        try:
            conn.execute(
                "INSERT OR IGNORE INTO businesses (name, description) VALUES (?,?)",
                (bname, bdesc),
            )
            added_businesses.append(bname)
        except Exception as exc:
            errors.append(f"business {bname}: {exc}")

    for rel in extracted.get("relationships", []):
        ticker  = (rel.get("company_ticker") or "").strip()
        bname   = (rel.get("business") or "").strip()
        comment = (rel.get("comment") or "").strip()
        if not ticker or not bname:
            continue
        try:
            co_row  = conn.execute("SELECT id FROM companies  WHERE name=?", (ticker,)).fetchone()
            biz_row = conn.execute("SELECT id FROM businesses WHERE name=?", (bname,)).fetchone()
            if co_row and biz_row:
                conn.execute(
                    "INSERT OR IGNORE INTO business_company "
                    "(business_id, company_id, comment, explanation, source_url) "
                    "VALUES (?,?,?,?,?)",
                    (biz_row["id"], co_row["id"], comment, "", pdf_source),
                )
                added_bc.append(f"{ticker} ↔ {bname}")
            else:
                errors.append(f"rel {ticker}↔{bname}: entity not found in DB")
        except Exception as exc:
            errors.append(f"rel {ticker}↔{bname}: {exc}")

    return (
        {"companies": added_companies, "businesses": added_businesses, "bc_links": added_bc},
        errors,
    )
