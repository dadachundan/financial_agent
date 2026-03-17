#!/usr/bin/env python3
"""
graphiti_ingest.py — Index PDFs and HTML financial reports into a local graphiti-core graph.

Sources:
  - zsxq         : PDFs from zsxq.db  (pdf_files table)
  - financial_reports : HTML SEC filings from financial_reports.db (reports table)
  - all          : both sources

Uses:
  - KuzuDB    (embedded, file-based graph DB — no server required)
  - bge-m3    (local embeddings via SentenceTransformer)
  - MiniMax   (entity / relationship extraction via LLM)

No cloud graph service needed. The knowledge graph is stored in ./graphiti_db/.

Usage:
    python graphiti_ingest.py                                          # index new zsxq PDFs
    python graphiti_ingest.py --source all                             # index new PDFs + 10-K/10-Q
    python graphiti_ingest.py --source financial_reports               # index new 10-K/10-Q only
    python graphiti_ingest.py --source financial_reports --ticker NVDA TSMC
    python graphiti_ingest.py --form-type 10-K                         # annual reports only
    python graphiti_ingest.py --reindex                                # clear graph and re-ingest
    python graphiti_ingest.py --limit 5                                # process at most 5 docs
    python graphiti_ingest.py --limit 2 --debug-llm                   # print all LLM calls
    python graphiti_ingest.py --db zsxq.db
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import argparse
import asyncio
import logging
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber

try:
    import fitz as _fitz_available  # pymupdf — optional but preferred
except ImportError:
    _fitz_available = None  # type: ignore[assignment]

# Suppress noisy but harmless graphiti-core warnings:
#   "LLM did not return resolutions for IDs: [0, 1, ...]"
#     → MiniMax returned empty NodeResolutions; all entities treated as new. Fine.
#   "Source entity not found in nodes for edge relation: ..."
#     → Handled by case-insensitive matching patch in edge_operations.py.
#       Any remaining ones are genuinely unmatchable names (LLM hallucinations).
logging.getLogger("graphiti_core.utils.maintenance.node_operations").setLevel(logging.ERROR)
logging.getLogger("graphiti_core.utils.maintenance.edge_operations").setLevel(logging.ERROR)

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR.parent / "db" / "zsxq.db"
MAX_CHARS   = 80_000   # ~20 k tokens — full document, no page limit

GROUP_ID    = "financial-pdfs"

_PROJECT_ROOT = None

def _find_project_root() -> Path:
    p = SCRIPT_DIR.resolve()
    while p != p.parent:
        if (p / ".git").is_dir():
            return p
        p = p.parent
    return SCRIPT_DIR

def _get_project_root() -> Path:
    global _PROJECT_ROOT
    if _PROJECT_ROOT is None:
        _PROJECT_ROOT = _find_project_root()
    return _PROJECT_ROOT


# ── Text extraction ────────────────────────────────────────────────────────────

def _extract_text_pdfplumber(pdf_path: Path, max_chars: int) -> str:
    """Fallback PDF extraction using pdfplumber (no heading detection)."""
    try:
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text.strip())
        full = "\n\n".join(pages)
        return full[:max_chars] if len(full) >= 200 else ""
    except Exception:
        return ""


def extract_text(pdf_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract text from a PDF with heading detection via pymupdf (fitz).

    Inspired by DeepRead's structured extraction approach:
    - Detects headings from font size relative to body text
    - Marks headings with # / ## markers for LLM context
    - Skips table-of-contents pages (many lines ending with ". . . N")
    - Falls back to pdfplumber when fitz is unavailable or extracts too little.
    """
    if _fitz_available is None:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    import fitz
    from collections import Counter

    try:
        doc = fitz.open(str(pdf_path))
    except Exception:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    if not doc.page_count:
        doc.close()
        return _extract_text_pdfplumber(pdf_path, max_chars)

    BOLD_FLAG = 1 << 4  # pymupdf bold flag bit

    # Pass 1: find body font size — mode of sizes for text spans longer than 10 chars
    all_sizes: list[float] = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    if len(span["text"].strip()) > 10:
                        all_sizes.append(round(span["size"], 1))

    if not all_sizes:
        doc.close()
        return _extract_text_pdfplumber(pdf_path, max_chars)

    body_size: float = Counter(all_sizes).most_common(1)[0][0]
    h1_min = body_size * 1.4   # e.g. 12.6 when body=9.0
    h2_min = body_size * 1.2   # e.g. 10.8 when body=9.0 (tightened from 1.15)

    # ToC line: "Section title . . . 42" or "Title       42"
    toc_line_re = re.compile(r"[.\u2026]{2,}\s*\d+\s*$|\s{4,}\d{1,3}\s*$")

    lines_out: list[str] = []
    for page in doc:
        page_lines: list[tuple[str, float, bool]] = []
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                if not line["spans"]:
                    continue
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text:
                    continue
                max_size = max(s["size"] for s in line["spans"])
                is_bold = any(s["flags"] & BOLD_FLAG for s in line["spans"])
                page_lines.append((text, max_size, is_bold))

        if not page_lines:
            continue

        # Skip ToC pages: >35 % of lines look like "entry . . . N"
        toc_count = sum(1 for t, _, _ in page_lines if toc_line_re.search(t))
        if len(page_lines) > 5 and toc_count / len(page_lines) > 0.35:
            continue

        for text, size, bold in page_lines:
            # Skip standalone page numbers
            if len(text) <= 4 and text.strip().isdigit():
                continue
            if size >= h1_min:
                lines_out.append(f"\n# {text}")
            elif size >= h2_min:
                lines_out.append(f"\n## {text}")
            else:
                lines_out.append(text)

    doc.close()

    full = "\n".join(lines_out)
    full = re.sub(r"\n{3,}", "\n\n", full).strip()

    if len(full) < 200:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    return full[:max_chars]


# 10-K: annual report section patterns
_10K_PATTERNS = {
    "item1":  r"(?i)item\s+1[\s\.\n\u2014\-]+\s*business\b",
    "item1a": r"(?i)item\s+1a[\s\.\n\u2014\-]+\s*risk factors\b",
    "item2":  r"(?i)item\s+2[\s\.\n\u2014\-]+\s*properties\b",
    "item3":  r"(?i)item\s+3[\s\.\n\u2014\-]+\s*legal proceedings\b",
    "item7":  r"(?i)item\s+7[\s\.\n\u2014\-]+\s*management",
    "item7a": r"(?i)item\s+7a[\s\.\n\u2014\-]+\s*quantitative",
    "item8":  r"(?i)item\s+8[\s\.\n\u2014\-]+\s*financial statements",
}

# 10-Q: quarterly report — Part I has Financial Statements + MD&A
_10Q_PATTERNS = {
    "item1_fs":  r"(?i)item\s+1[\s\.\n\u2014\-]+\s*financial statements\b",
    "item2_mda": r"(?i)item\s+2[\s\.\n\u2014\-]+\s*management.{0,30}discussion\b",
    "item3_mkt": r"(?i)item\s+3[\s\.\n\u2014\-]+\s*quantitative",
    "item4":     r"(?i)item\s+4[\s\.\n\u2014\-]+\s*controls",
    "item1a":    r"(?i)item\s+1a[\s\.\n\u2014\-]+\s*risk factors\b",
}

# 8-K: current report — items use decimal notation e.g. 1.01, 2.02
# Excluded: 5.02 (officer/director changes — HR noise),
#           7.01 (Reg FD — thin text, actual content is in the attached exhibit)
_8K_PATTERNS = {
    "item1_01": r"(?i)item\s+1\.01\b",   # Entry into material agreement
    "item2_01": r"(?i)item\s+2\.01\b",   # Completion of acquisition
    "item2_02": r"(?i)item\s+2\.02\b",   # Results of operations (earnings)
    "item5_02": r"(?i)item\s+5\.02\b",   # Officer/director changes — boundary only, not extracted
    "item7_01": r"(?i)item\s+7\.01\b",   # Reg FD — boundary only, not extracted
    "item8_01": r"(?i)item\s+8\.01\b",   # Other material events
    "item9_01": r"(?i)item\s+9\.01\b",   # Financial statements / exhibits (end boundary)
}

_MAX_SECTION = 12_000  # chars per extracted section


def _sec_offsets(text: str, patterns: dict) -> dict[str, list[int]]:
    return {k: [m.start() for m in re.finditer(p, text)]
            for k, p in patterns.items()}

def _last_offset(offsets: dict, key: str, full_text: str = "") -> int | None:
    lst = offsets.get(key, [])
    if not lst:
        return None
    if full_text:
        line_starts = [o for o in lst
                       if re.search(r"\n\s*$", full_text[max(0, o - 60):o])]
        if line_starts:
            return line_starts[-1]
    return lst[-1]

def _first_after_offset(offsets: dict, key: str, min_pos: int,
                        full_text: str = "") -> int | None:
    for o in sorted(offsets.get(key, [])):
        if o <= min_pos + 500:
            continue
        if full_text:
            preceding = full_text[max(0, o - 60):o]
            if not re.search(r"\n\s*$", preceding):
                continue
        return o
    return None


def _clean_html_to_text(html_path: Path) -> str:
    """Parse HTML, strip boilerplate tags, flatten tables, return clean plain text."""
    from bs4 import BeautifulSoup
    html = html_path.read_text(errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "head", "footer", "nav",
                     "ix:header", "ix:hidden", "ix:references", "ix:resources"]):
        tag.decompose()
    for tag in soup.find_all(["ix:nonfraction", "ix:nonnumeric"]):
        tag.unwrap()

    for table in soup.find_all("table"):
        rows_text = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                rows_text.append(" | ".join(cells))
        if rows_text:
            table.replace_with("\n" + "\n".join(rows_text) + "\n")

    full = soup.get_text(separator="\n")
    full = re.sub(r"[ \t]{2,}", " ", full)
    full = re.sub(r"\n{3,}", "\n\n", full).strip()
    return full


def _extract_10k_sections(full: str) -> list[str]:
    """Extract Item 1 (Business) + Item 1A (Risk Factors) from a 10-K."""
    offs = _sec_offsets(full, _10K_PATTERNS)
    sections: list[str] = []

    s1 = _last_offset(offs, "item1", full)
    if s1 is not None:
        e1 = (_first_after_offset(offs, "item1a", s1, full)
              or _first_after_offset(offs, "item2", s1, full)
              or s1 + _MAX_SECTION * 2)
        chunk = full[s1:e1].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1: BUSINESS ===\n{chunk[:_MAX_SECTION]}")

    s1a = _first_after_offset(offs, "item1a", s1 or 0, full)
    if s1a is not None:
        e1a = (_first_after_offset(offs, "item2",  s1a, full)
               or _first_after_offset(offs, "item3",  s1a, full)
               or _first_after_offset(offs, "item7",  s1a, full)
               or _first_after_offset(offs, "item7a", s1a, full)
               or _first_after_offset(offs, "item8",  s1a, full)
               or s1a + _MAX_SECTION * 2)
        chunk = full[s1a:e1a].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1A: RISK FACTORS ===\n{chunk[:_MAX_SECTION]}")

    return sections


def _extract_10q_sections(full: str) -> list[str]:
    """Extract MD&A (Item 2) + Risk Factors (Item 1A Part II) from a 10-Q.

    10-Q structure:
      Part I  Item 1  Financial Statements  (tables, skip as primary)
      Part I  Item 2  MD&A                  ← most useful narrative
      Part I  Item 3  Market Risk
      Part I  Item 4  Controls
      Part II Item 1A Risk Factors (updates)
    """
    offs = _sec_offsets(full, _10Q_PATTERNS)
    sections: list[str] = []

    # MD&A — most information-dense section for 10-Q
    s_mda = _last_offset(offs, "item2_mda", full)
    if s_mda is not None:
        e_mda = (_first_after_offset(offs, "item3_mkt", s_mda, full)
                 or _first_after_offset(offs, "item4", s_mda, full)
                 or s_mda + _MAX_SECTION * 2)
        chunk = full[s_mda:e_mda].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 2: MD&A ===\n{chunk[:_MAX_SECTION]}")

    # Risk Factors update (Part II) — optional, often short
    s_rf = _first_after_offset(offs, "item1a", s_mda or 0, full)
    if s_rf is not None:
        chunk = full[s_rf:s_rf + _MAX_SECTION].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1A: RISK FACTORS (UPDATE) ===\n{chunk[:_MAX_SECTION]}")

    return sections


def _extract_8k_sections(full: str) -> list[str]:
    """Extract substantive items from an 8-K current report.

    8-K items use decimal notation: 1.01, 2.01, 2.02, 8.01.
    We grab all found items except 9.01 (Exhibits) as separate sections.
    Excluded: 5.02 (officer changes), 7.01 (Reg FD — content is in exhibit, not item text).
    """
    offs = _sec_offsets(full, _8K_PATTERNS)

    # Items to extract (label = None means boundary-only, never extracted)
    item_labels = {
        "item1_01": "ITEM 1.01: MATERIAL AGREEMENT",
        "item2_01": "ITEM 2.01: COMPLETION OF ACQUISITION",
        "item2_02": "ITEM 2.02: RESULTS OF OPERATIONS",
        "item5_02": None,  # officer changes — boundary only
        "item7_01": None,  # Reg FD — boundary only
        "item8_01": "ITEM 8.01: OTHER EVENTS",
    }

    # Collect ALL item positions (extracted + boundary-only) for accurate end boundaries
    found: list[tuple[int, str, str | None]] = []  # (offset, key, label_or_None)
    for key, label in item_labels.items():
        pos = _last_offset(offs, key, full)
        if pos is not None:
            found.append((pos, key, label))
    found.sort(key=lambda x: x[0])

    # End boundary: Exhibits section
    exhibits_end = _last_offset(offs, "item9_01", full) or len(full)

    sections: list[str] = []
    for i, (start, key, label) in enumerate(found):
        if label is None:          # boundary-only item — skip extraction
            continue
        end = found[i + 1][0] if i + 1 < len(found) else exhibits_end
        chunk = full[start:end].strip()
        if len(chunk) > 100:
            sections.append(f"=== {label} ===\n{chunk[:_MAX_SECTION]}")

    return sections


def extract_html_text(html_path: Path, form_type: str = "10-K",
                      max_chars: int = MAX_CHARS) -> str:
    """Extract the most informative narrative sections from an SEC HTML filing.

    Dispatches to form-type-specific extractors:
      10-K  → Item 1 (Business) + Item 1A (Risk Factors)
      10-Q  → Item 2 (MD&A) + Item 1A Part II (Risk Factors update)
      8-K   → all substantive items (1.01, 2.02, 5.02, etc.)
    Falls back to a raw text dump if no sections are detected.
    """
    full = _clean_html_to_text(html_path)
    if len(full) < 200:
        return ""

    ft = (form_type or "").upper()
    if ft in ("10-K", "10-K/A"):
        sections = _extract_10k_sections(full)
    elif ft in ("10-Q", "10-Q/A"):
        sections = _extract_10q_sections(full)
    elif ft in ("8-K", "8-K/A"):
        sections = _extract_8k_sections(full)
    else:
        sections = _extract_10k_sections(full) or _extract_10q_sections(full)

    if sections:
        return "\n\n".join(sections)

    # Fallback for unrecognised/non-standard filings
    return full[:max_chars]


# ── DB helpers — zsxq.db ───────────────────────────────────────────────────────

def ensure_zsxq_column(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN graphiti_indexed_at TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_pending_pdfs(conn: sqlite3.Connection, reindex: bool, limit: int = 0) -> list:
    limit_sql = f" LIMIT {limit}" if limit > 0 else ""
    if reindex:
        return conn.execute(
            "SELECT file_id, name, local_path, create_time "
            f"FROM pdf_files WHERE local_path IS NOT NULL "
            f"ORDER BY create_time DESC{limit_sql}"
        ).fetchall()
    return conn.execute(
        "SELECT file_id, name, local_path, create_time "
        f"FROM pdf_files WHERE local_path IS NOT NULL AND graphiti_indexed_at IS NULL "
        f"ORDER BY create_time DESC{limit_sql}"
    ).fetchall()


def mark_pdf_indexed(conn: sqlite3.Connection, file_id: int) -> None:
    conn.execute(
        "UPDATE pdf_files SET graphiti_indexed_at = ? WHERE file_id = ?",
        (datetime.now(timezone.utc).isoformat(), file_id),
    )
    conn.commit()


# ── DB helpers — financial_reports.db ─────────────────────────────────────────

def ensure_reports_column(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("ALTER TABLE reports ADD COLUMN graphiti_indexed_at TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_pending_reports(
    conn: sqlite3.Connection,
    reindex: bool,
    tickers: list[str],
    form_types: list[str],
    limit: int = 0,
) -> list:
    placeholders_ft = ",".join("?" * len(form_types))
    params: list = list(form_types)

    if reindex:
        where = f"local_path IS NOT NULL AND form_type IN ({placeholders_ft})"
    else:
        where = f"local_path IS NOT NULL AND form_type IN ({placeholders_ft}) AND graphiti_indexed_at IS NULL"

    if tickers:
        placeholders_t = ",".join("?" * len(tickers))
        where += f" AND ticker IN ({placeholders_t})"
        params.extend(tickers)

    limit_sql = f" LIMIT {limit}" if limit > 0 else ""
    return conn.execute(
        f"SELECT id, ticker, company_name, period, form_type, local_path, filed_date "
        f"FROM reports WHERE {where} ORDER BY filed_date DESC{limit_sql}",
        params,
    ).fetchall()


def mark_report_indexed(conn: sqlite3.Connection, report_id: int) -> None:
    conn.execute(
        "UPDATE reports SET graphiti_indexed_at = ? WHERE id = ?",
        (datetime.now(timezone.utc).isoformat(), report_id),
    )
    conn.commit()


# ── Core async ingestion ───────────────────────────────────────────────────────

async def _build_graphiti():
    from graphiti_core import Graphiti
    from graphiti_core.driver.kuzu_driver import KuzuDriver
    from minimax_llm_client import MiniMaxLLMClient, BGEEmbedder, PassthroughReranker, GRAPH_DIR

    print("Loading bge-m3 embedder …")
    embedder = BGEEmbedder()
    embedder._get_model()
    print("Embedder ready.\n")

    # KuzuDB creates two files: graphiti_db (main) and graphiti_db.wal.
    # If either is left in a bad state by a crash/interrupt, both must be deleted.
    def _delete_db():
        GRAPH_DIR.unlink(missing_ok=True)
        Path(str(GRAPH_DIR) + ".wal").unlink(missing_ok=True)

    # Stub guard: a valid DB is always > 4 KB; 4096-byte file = uninitialised.
    if GRAPH_DIR.exists() and GRAPH_DIR.stat().st_size <= 4096:
        print(f"⚠  Detected incomplete graphiti_db ({GRAPH_DIR.stat().st_size} bytes). "
              "Deleting and recreating …")
        _delete_db()

    try:
        driver = KuzuDriver(str(GRAPH_DIR))
    except Exception as e:
        print(f"⚠  Could not open graphiti_db ({e}). Deleting and retrying …")
        _delete_db()
        driver = KuzuDriver(str(GRAPH_DIR))
    driver._database = GROUP_ID

    import kuzu as _kuzu
    from graphiti_core.graph_queries import get_fulltext_indices
    from graphiti_core.driver.driver import GraphProvider
    _conn = _kuzu.Connection(driver.db)
    for q in get_fulltext_indices(GraphProvider.KUZU):
        try:
            _conn.execute(q)
        except Exception as e:
            if "already exists" not in str(e):
                raise
    _conn.close()

    return Graphiti(
        llm_client=MiniMaxLLMClient(),
        embedder=embedder,
        cross_encoder=PassthroughReranker(),
        graph_driver=driver,
    )


async def _heartbeat(label: str, interval: int = 30) -> None:
    """Print a 'still running' dot every `interval` seconds until cancelled."""
    try:
        elapsed = 0
        while True:
            await asyncio.sleep(interval)
            elapsed += interval
            print(f"  … still running ({elapsed}s) [{label}]", flush=True)
    except asyncio.CancelledError:
        pass


def _fmt_eta(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h{m:02d}m"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


async def _ingest_items(items: list[dict]) -> tuple[int, int]:
    """
    Each item dict has:
      name, episode_body, source_description, reference_time,
      db_conn, mark_fn, row_id
    """
    import traceback
    import langfuse_monitor
    import graph_mirror

    graphiti = await _build_graphiti()

    # Open SQLite mirror — non-blocking for web server reads
    mirror_conn = graph_mirror.get_conn()
    graph_mirror.ensure_schema(mirror_conn)
    ok = skipped = 0
    elapsed_times: list[float] = []
    session_start = asyncio.get_event_loop().time()

    try:
        for i, item in enumerate(items, 1):
            # ── ETA line ─────────────────────────────────────────────────────
            avg = sum(elapsed_times) / len(elapsed_times) if elapsed_times else None
            eta_str = (f"  ETA ~{_fmt_eta(avg * (len(items) - i + 1))}" if avg else "")
            print(f"\n[{i}/{len(items)}]{eta_str}  {item['label'][:65]}", flush=True)
            print(f"  file: {item.get('file_path', '(unknown)')}", flush=True)

            text = item["episode_body"]
            if not text:
                print("  ⚠  No text extracted — skipping.", flush=True)
                skipped += 1
                continue

            print(f"  {len(text):,} chars → LLM pipeline …", flush=True)

            # Set document label for Langfuse trace grouping
            lf_token = langfuse_monitor.set_document(item["label"])

            heartbeat = asyncio.ensure_future(
                _heartbeat(item["name"], interval=30)
            )
            t0 = asyncio.get_event_loop().time()
            try:
                result = await graphiti.add_episode(
                    name=item["name"],
                    episode_body=text,
                    source_description=item["source_description"],
                    reference_time=item["reference_time"],
                    group_id=GROUP_ID,
                )
                elapsed = asyncio.get_event_loop().time() - t0
                elapsed_times.append(elapsed)
                n_nodes = len(result.nodes)
                n_edges = len(result.edges)
                item["mark_fn"](item["db_conn"], item["row_id"])
                total_elapsed = asyncio.get_event_loop().time() - session_start
                print(
                    f"  ✓  {n_nodes} entities, {n_edges} edges  ({elapsed:.0f}s this doc | "
                    f"session {_fmt_eta(total_elapsed)} | ok={ok+1} skip={skipped})",
                    flush=True,
                )
                ok += 1

                # Mirror to SQLite so web server stays live during ingest
                try:
                    graph_mirror.upsert_entities(mirror_conn, result.nodes)
                    name_map = {str(n.uuid): n.name for n in result.nodes}
                    graph_mirror.upsert_edges(mirror_conn, result.edges, name_map)
                    graph_mirror.backfill_edge_names(mirror_conn)
                    if getattr(result, "episode", None):
                        graph_mirror.upsert_episode(mirror_conn, result.episode)
                except Exception as _me:
                    print(f"  ⚠  mirror write failed: {_me}", flush=True)
            except Exception as e:
                elapsed = asyncio.get_event_loop().time() - t0
                print(f"  ✗  Error after {elapsed:.0f}s: {e}", flush=True)
                print(traceback.format_exc(), flush=True)
                skipped += 1
            finally:
                heartbeat.cancel()
                await asyncio.sleep(0)  # let cancel propagate
                langfuse_monitor.clear_document(lf_token)
                langfuse_monitor.flush()  # push completed doc traces immediately

    except KeyboardInterrupt:
        print(f"\n⚠  Interrupted. Closing database … (ok={ok} skip={skipped})", flush=True)
    finally:
        await graphiti.close()

    return ok, skipped


def _build_pdf_items(rows, db_path: Path) -> tuple[list[dict], sqlite3.Connection]:
    import time
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_zsxq_column(conn)

    items = []
    for idx, row in enumerate(rows, 1):
        file_id    = row["file_id"]
        name       = row["name"]
        local_path = Path(row["local_path"])
        create_time = row["create_time"] or ""

        if not local_path.exists():
            print(f"  [{idx}] ⚠  File not found: {local_path}", flush=True)
            continue

        t0 = time.time()
        try:
            text = extract_text(local_path)
        except Exception as e:
            print(f"  [{idx}] ⚠  Extract failed for {name}: {e}", flush=True)
            continue
        extract_ms = int((time.time() - t0) * 1000)

        if not text:
            print(f"  [{idx}] ⚠  No text (image-only PDF?): {name}", flush=True)
            continue

        print(f"  [{idx}] {len(text):>7,}c  {extract_ms}ms  {name[:55]}", flush=True)

        try:
            ref_time = datetime.fromisoformat(create_time.replace("Z", "+00:00"))
        except Exception:
            ref_time = datetime.now(timezone.utc)

        items.append({
            "label":              name,
            "file_path":          str(local_path),
            "name":               f"pdf_{file_id}",
            "episode_body":       text,
            "source_description": f"PDF: {name}",
            "reference_time":     ref_time,
            "db_conn":            conn,
            "mark_fn":            mark_pdf_indexed,
            "row_id":             file_id,
        })
    return items, conn


def _build_report_items(rows, reports_db_path: Path) -> tuple[list[dict], sqlite3.Connection]:
    import time
    conn = sqlite3.connect(reports_db_path)
    conn.row_factory = sqlite3.Row
    ensure_reports_column(conn)

    items = []
    for idx, row in enumerate(rows, 1):
        report_id   = row["id"]
        ticker      = row["ticker"]
        company     = row["company_name"] or ticker
        period      = row["period"]
        form_type   = row["form_type"]
        local_path  = Path(row["local_path"])
        filed_date  = row["filed_date"] or ""

        if not local_path.exists():
            print(f"  [{idx}] ⚠  File not found: {local_path}", flush=True)
            continue

        t0 = time.time()
        try:
            text = extract_html_text(local_path, form_type=form_type)
        except Exception as e:
            print(f"  [{idx}] ⚠  Extract failed for {ticker} {period}: {e}", flush=True)
            continue
        extract_ms = int((time.time() - t0) * 1000)

        if not text:
            print(f"  [{idx}] ⚠  No text extracted: {ticker} {form_type} {period}", flush=True)
            continue

        print(f"  [{idx}] {len(text):>7,}c  {extract_ms}ms  {ticker} {form_type} {period}", flush=True)

        try:
            ref_time = datetime.fromisoformat(filed_date.replace("Z", "+00:00"))
        except Exception:
            ref_time = datetime.now(timezone.utc)

        label = f"{ticker} {form_type} {period}"
        items.append({
            "label":              label,
            "file_path":          str(local_path),
            "name":               f"report_{report_id}",
            "episode_body":       text,
            "source_description": f"{form_type}: {company} {period}",
            "reference_time":     ref_time,
            "db_conn":            conn,
            "mark_fn":            mark_report_indexed,
            "row_id":             report_id,
        })
    return items, conn


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index financial documents into a local graphiti-core knowledge graph."
    )
    parser.add_argument("--db",      default=str(DEFAULT_DB),
                        help="Path to zsxq.db")
    parser.add_argument("--source",  default="zsxq",
                        choices=["zsxq", "financial_reports", "all"],
                        help="Document source to index (default: zsxq)")
    parser.add_argument("--ticker",  nargs="+", default=[],
                        metavar="TICKER",
                        help="Filter financial_reports to these ticker(s) e.g. --ticker NVDA TSMC")
    parser.add_argument("--form-type", nargs="+", default=["10-K", "10-Q"],
                        metavar="FORM",
                        help="Form types to index from financial_reports (default: 10-K 10-Q)")
    parser.add_argument("--reindex", action="store_true",
                        help="Reset graphiti_indexed_at for all docs and re-ingest.")
    parser.add_argument("--limit",   type=int, default=0,
                        help="Process at most N documents (0 = all).")
    parser.add_argument("--debug-llm", action="store_true",
                        help="Print every LLM request and response to stdout.")
    args = parser.parse_args()

    import minimax_llm_client
    if args.debug_llm:
        minimax_llm_client.PRINT_ALL_LLM_CALLS = True
    # Write LLM call log to log/ directory (debug only; monitoring via Langfuse)
    minimax_llm_client.LLM_LOG_FILE = _get_project_root() / "log" / "llm_calls.jsonl"

    # Langfuse monitoring (no-op if keys not configured in config.py)
    import langfuse_monitor
    from datetime import datetime as _dt
    _session = _dt.now().strftime("%Y-%m-%d %H:%M")
    langfuse_monitor.init(session_label=f"ingest {_session}")

    root = _get_project_root()
    zsxq_db_path    = Path(args.db).expanduser()
    reports_db_path = root / "db" / "financial_reports.db"

    all_items: list[dict] = []
    open_conns: list[sqlite3.Connection] = []

    # ── zsxq PDFs ──────────────────────────────────────────────────────────────
    if args.source in ("zsxq", "all"):
        if not zsxq_db_path.exists():
            print(f"ERROR: zsxq database not found: {zsxq_db_path}")
            sys.exit(1)
        conn = sqlite3.connect(zsxq_db_path)
        conn.row_factory = sqlite3.Row
        ensure_zsxq_column(conn)
        rows = get_pending_pdfs(conn, args.reindex, args.limit)
        conn.close()
        if rows:
            print(f"Found {len(rows)} pending PDFs in zsxq.db …")
            items, conn2 = _build_pdf_items(rows, zsxq_db_path)
            all_items.extend(items)
            open_conns.append(conn2)
        else:
            print("No new PDFs in zsxq.db.")

    # ── financial_reports HTML ─────────────────────────────────────────────────
    if args.source in ("financial_reports", "all"):
        if not reports_db_path.exists():
            print(f"ERROR: financial_reports database not found: {reports_db_path}")
            sys.exit(1)
        conn = sqlite3.connect(reports_db_path)
        conn.row_factory = sqlite3.Row
        ensure_reports_column(conn)
        rows = get_pending_reports(conn, args.reindex, args.ticker, args.form_type, args.limit)
        conn.close()
        ticker_note = f" for {', '.join(args.ticker)}" if args.ticker else ""
        ft_note = "/".join(args.form_type)
        if rows:
            print(f"Found {len(rows)} pending {ft_note} reports{ticker_note} in financial_reports.db …")
            items, conn2 = _build_report_items(rows, reports_db_path)
            all_items.extend(items)
            open_conns.append(conn2)
        else:
            print(f"No new {ft_note} reports{ticker_note} in financial_reports.db.")

    if not all_items:
        print("Nothing to index. All done!")
        for c in open_conns:
            c.close()
        return

    if args.limit:
        all_items = all_items[: args.limit]

    print(f"\nIndexing {len(all_items)} document(s) …\n")

    ok, skipped = asyncio.run(_ingest_all_items(all_items))

    for c in open_conns:
        c.close()

    print(f"\nDone.  Indexed: {ok}  Skipped: {skipped}")


async def _ingest_all_items(items: list[dict]) -> tuple[int, int]:
    return await _ingest_items(items)


if __name__ == "__main__":
    main()
