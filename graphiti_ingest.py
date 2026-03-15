#!/usr/bin/env python3
"""
graphiti_ingest.py — Index PDFs from zsxq.db into a local graphiti-core graph.

Replaces zep_ingest.py. Uses:
  - KuzuDB    (embedded, file-based graph DB — no server required)
  - bge-m3    (local embeddings via SentenceTransformer)
  - MiniMax   (entity / relationship extraction via LLM)

No cloud graph service needed. The knowledge graph is stored in ./graphiti_db/.

Usage:
    python graphiti_ingest.py              # index all un-indexed PDFs
    python graphiti_ingest.py --reindex    # clear graph and re-ingest everything
    python graphiti_ingest.py --limit 5    # process at most 5 PDFs (test run)
    python graphiti_ingest.py --db zsxq.db
"""

import argparse
import asyncio
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB = SCRIPT_DIR / "zsxq.db"
MAX_CHARS  = 80_000   # ~20 k tokens — full document, no page limit

GROUP_ID   = "financial-pdfs"


# ── Text extraction ────────────────────────────────────────────────────────────

def extract_text(pdf_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract all text from a PDF with pdfplumber (no page limit)."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    return "\n\n".join(pages)[:max_chars]


# ── DB helpers ─────────────────────────────────────────────────────────────────

def ensure_graphiti_column(conn: sqlite3.Connection) -> None:
    """Add graphiti_indexed_at column if it doesn't exist yet."""
    try:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN graphiti_indexed_at TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # already exists


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


def mark_indexed(conn: sqlite3.Connection, file_id: int) -> None:
    conn.execute(
        "UPDATE pdf_files SET graphiti_indexed_at = ? WHERE file_id = ?",
        (datetime.now(timezone.utc).isoformat(), file_id),
    )
    conn.commit()


# ── Core async ingestion ───────────────────────────────────────────────────────

async def _ingest_all(rows: list, db_path: Path) -> tuple[int, int]:
    import kuzu
    from graphiti_core import Graphiti
    from graphiti_core.driver.kuzu_driver import KuzuDriver
    from minimax_llm_client import MiniMaxLLMClient, BGEEmbedder, GRAPH_DIR

    # Warm up embedder once up front
    print("Loading bge-m3 embedder …")
    embedder = BGEEmbedder()
    embedder._get_model()
    print("Embedder ready.\n")

    GRAPH_DIR.mkdir(exist_ok=True)
    kdb    = kuzu.Database(str(GRAPH_DIR))
    driver = KuzuDriver(kdb)

    graphiti = Graphiti(
        llm_client=MiniMaxLLMClient(),
        embedder=embedder,
        graph_driver=driver,
    )
    await graphiti.build_indices_and_constraints()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_graphiti_column(conn)

    ok = skipped = 0
    for i, row in enumerate(rows, 1):
        file_id    = row["file_id"]
        name       = row["name"]
        local_path = Path(row["local_path"])
        create_time = row["create_time"] or ""

        print(f"[{i}/{len(rows)}] {name[:70]}")

        if not local_path.exists():
            print(f"  ⚠  File not found: {local_path}")
            skipped += 1
            continue

        try:
            text = extract_text(local_path)
        except Exception as e:
            print(f"  ⚠  Could not extract text: {e}")
            skipped += 1
            continue

        if not text.strip():
            print(f"  ⚠  No text extracted.")
            skipped += 1
            continue

        print(f"  {len(text):,} chars extracted.")

        # Parse reference time (used for temporal graph edges)
        try:
            ref_time = datetime.fromisoformat(create_time.replace("Z", "+00:00"))
        except Exception:
            ref_time = datetime.now(timezone.utc)

        try:
            result = await graphiti.add_episode(
                name=f"pdf_{file_id}",
                episode_body=text,
                source_description=f"PDF: {name}",
                reference_time=ref_time,
                group_id=GROUP_ID,
            )
            n_nodes = len(result.nodes)
            n_edges = len(result.edges)
            mark_indexed(conn, file_id)
            print(f"  ✓ {n_nodes} entities, {n_edges} relationships extracted.")
            ok += 1
        except Exception as e:
            print(f"  ✗ Graphiti error: {e}")
            skipped += 1

    conn.close()
    await graphiti.close()
    return ok, skipped


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index financial PDFs into a local graphiti-core knowledge graph."
    )
    parser.add_argument("--db",      default=str(DEFAULT_DB),
                        help="Path to zsxq.db")
    parser.add_argument("--reindex", action="store_true",
                        help="Reset graphiti_indexed_at for all PDFs and re-ingest.")
    parser.add_argument("--limit",   type=int, default=0,
                        help="Process at most N PDFs (0 = all).")
    args = parser.parse_args()

    db_path = Path(args.db).expanduser()
    if not db_path.exists():
        print(f"ERROR: database not found: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_graphiti_column(conn)
    rows = get_pending_pdfs(conn, args.reindex)
    conn.close()

    if not rows:
        print("No new PDFs to index. All done!")
        return

    if args.limit:
        rows = rows[: args.limit]

    print(f"Found {len(rows)} PDFs to index.")
    print(f"Graph DB: {SCRIPT_DIR / 'graphiti_db'}\n")

    ok, skipped = asyncio.run(_ingest_all(rows, db_path))
    print(f"\nDone.  Indexed: {ok}  Skipped: {skipped}")
    print(
        "\nTip: search the graph with  python graphiti_ingest.py  "
        "or open the /zep route in the web app."
    )


if __name__ == "__main__":
    main()
