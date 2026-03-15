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
    python graphiti_ingest.py                                  # index new zsxq PDFs
    python graphiti_ingest.py --source all                     # index new PDFs + 10-K/10-Q
    python graphiti_ingest.py --source financial_reports       # index new 10-K/10-Q only
    python graphiti_ingest.py --source financial_reports --ticker NVDA TSMC
    python graphiti_ingest.py --form-type 10-K                 # annual reports only
    python graphiti_ingest.py --reindex                        # clear graph and re-ingest
    python graphiti_ingest.py --limit 5                        # process at most 5 docs
    python graphiti_ingest.py --db zsxq.db
"""

import argparse
import asyncio
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR / "zsxq.db"
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

def extract_text(pdf_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract all text from a PDF with pdfplumber.

    Returns empty string for image-only or DRM-obfuscated PDFs so the caller
    can skip them gracefully.
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    full = "\n\n".join(pages)
    if len(full) < 200:
        return ""
    return full[:max_chars]


def extract_html_text(html_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract readable text from an SEC HTML filing using BeautifulSoup."""
    from bs4 import BeautifulSoup
    html = html_path.read_text(errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) < 200:
        return ""
    return text[:max_chars]


# ── DB helpers — zsxq.db ───────────────────────────────────────────────────────

def ensure_zsxq_column(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN graphiti_indexed_at TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_pending_pdfs(conn: sqlite3.Connection, reindex: bool) -> list:
    if reindex:
        return conn.execute(
            "SELECT file_id, name, local_path, create_time "
            "FROM pdf_files WHERE local_path IS NOT NULL"
        ).fetchall()
    return conn.execute(
        "SELECT file_id, name, local_path, create_time "
        "FROM pdf_files WHERE local_path IS NOT NULL AND graphiti_indexed_at IS NULL"
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

    return conn.execute(
        f"SELECT id, ticker, company_name, period, form_type, local_path, filed_date "
        f"FROM reports WHERE {where} ORDER BY filed_date DESC",
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


async def _ingest_items(items: list[dict]) -> tuple[int, int]:
    """
    Each item dict has:
      name, episode_body, source_description, reference_time,
      db_conn, mark_fn, row_id
    """
    graphiti = await _build_graphiti()
    ok = skipped = 0

    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {item['label'][:70]}")
        text = item["episode_body"]
        if not text:
            print("  ⚠  No text extracted.")
            skipped += 1
            continue

        print(f"  {len(text):,} chars extracted.")
        try:
            result = await graphiti.add_episode(
                name=item["name"],
                episode_body=text,
                source_description=item["source_description"],
                reference_time=item["reference_time"],
                group_id=GROUP_ID,
            )
            n_nodes = len(result.nodes)
            n_edges = len(result.edges)
            item["mark_fn"](item["db_conn"], item["row_id"])
            print(f"  ✓ {n_nodes} entities, {n_edges} relationships extracted.")
            ok += 1
        except Exception as e:
            print(f"  ✗ Graphiti error: {e}")
            skipped += 1

    await graphiti.close()
    return ok, skipped


def _build_pdf_items(rows, db_path: Path) -> tuple[list[dict], sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_zsxq_column(conn)

    items = []
    for row in rows:
        file_id    = row["file_id"]
        name       = row["name"]
        local_path = Path(row["local_path"])
        create_time = row["create_time"] or ""

        if not local_path.exists():
            print(f"  ⚠  File not found: {local_path}")
            continue

        try:
            text = extract_text(local_path)
        except Exception as e:
            print(f"  ⚠  Could not extract text from {name}: {e}")
            continue

        try:
            ref_time = datetime.fromisoformat(create_time.replace("Z", "+00:00"))
        except Exception:
            ref_time = datetime.now(timezone.utc)

        items.append({
            "label":              name,
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
    conn = sqlite3.connect(reports_db_path)
    conn.row_factory = sqlite3.Row
    ensure_reports_column(conn)

    items = []
    for row in rows:
        report_id   = row["id"]
        ticker      = row["ticker"]
        company     = row["company_name"] or ticker
        period      = row["period"]
        form_type   = row["form_type"]
        local_path  = Path(row["local_path"])
        filed_date  = row["filed_date"] or ""

        if not local_path.exists():
            print(f"  ⚠  File not found: {local_path}")
            continue

        try:
            text = extract_html_text(local_path)
        except Exception as e:
            print(f"  ⚠  Could not extract text from {ticker} {period}: {e}")
            continue

        try:
            ref_time = datetime.fromisoformat(filed_date.replace("Z", "+00:00"))
        except Exception:
            ref_time = datetime.now(timezone.utc)

        label = f"{ticker} {form_type} {period}"
        items.append({
            "label":              label,
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

    if args.debug_llm:
        import minimax_llm_client
        minimax_llm_client.PRINT_ALL_LLM_CALLS = True

    root = _get_project_root()
    zsxq_db_path    = Path(args.db).expanduser()
    reports_db_path = root / "financial_reports.db"

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
        rows = get_pending_pdfs(conn, args.reindex)
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
        rows = get_pending_reports(conn, args.reindex, args.ticker, args.form_type)
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
