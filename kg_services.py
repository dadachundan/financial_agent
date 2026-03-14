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
import re
import sqlite3
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

def fetch_url_text(url: str, max_bytes: int = 200_000) -> str:
    """Fetch a URL and return stripped plain text (script/style blocks and HTML tags removed)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read(max_bytes).decode("utf-8", errors="replace")
    # Remove script/style blocks (content + tags) before stripping remaining tags
    text = re.sub(r"<(script|style)[^>]*>.*?</(script|style)>", " ", raw,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()[:8000]


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
