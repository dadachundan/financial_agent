#!/usr/bin/env python3
"""
zep_ingest.py — Index PDFs from zsxq.db into a Zep Cloud graph.

Replaces rag_index.py (ChromaDB) + the LLM entity extraction in kg_services.py.
Zep automatically extracts entities and relationships from the text and builds
a cross-document knowledge graph you can query with natural language.

Usage:
    python zep_ingest.py                   # index all new PDFs
    python zep_ingest.py --reindex         # re-ingest everything from scratch
    python zep_ingest.py --db zsxq.db
    python zep_ingest.py --limit 10        # process at most 10 PDFs (for testing)

Requirements:
    pip install zep-cloud pdfplumber
    ZEP_API_KEY in config.py  (get free key at https://app.getzep.com)
"""

import argparse
import sqlite3
import sys
import time
from pathlib import Path

import pdfplumber
from zep_cloud.client import Zep

SCRIPT_DIR   = Path(__file__).parent
DEFAULT_DB   = SCRIPT_DIR / "zsxq.db"

GRAPH_ID     = "financial-pdfs"
GRAPH_NAME   = "Financial Research PDFs"
GRAPH_DESC   = "Cross-document knowledge graph of financial research reports"

MAX_CHARS    = 80_000   # ~20k tokens — Zep episode limit is generous but not unlimited


# ── Config ────────────────────────────────────────────────────────────────────

def _load_zep_key() -> str:
    """Walk up from script dir to find config.py and load ZEP_API_KEY."""
    for parent in [SCRIPT_DIR] + list(SCRIPT_DIR.parents):
        cfg = parent / "config.py"
        if cfg.exists():
            ns: dict = {}
            exec(cfg.read_text(), ns)
            key = ns.get("ZEP_API_KEY", "")
            if key:
                return key
    raise RuntimeError(
        "ZEP_API_KEY not found in config.py.\n"
        "  1. Go to https://app.getzep.com and sign up (free).\n"
        "  2. Copy your API key.\n"
        "  3. Add  ZEP_API_KEY = \"ze-...\"  to config.py"
    )


# ── Text extraction ────────────────────────────────────────────────────────────

def extract_text(pdf_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract full text from a PDF with pdfplumber (no page limit)."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    full = "\n\n".join(pages)
    return full[:max_chars]


# ── DB helpers ─────────────────────────────────────────────────────────────────

def ensure_zep_column(conn: sqlite3.Connection) -> None:
    """Add zep_episode_uuid column to pdf_files if it doesn't exist."""
    try:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN zep_episode_uuid TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # column already exists


def get_pending_pdfs(conn: sqlite3.Connection, reindex: bool) -> list[sqlite3.Row]:
    if reindex:
        return conn.execute(
            "SELECT file_id, name, local_path FROM pdf_files WHERE local_path IS NOT NULL"
        ).fetchall()
    return conn.execute(
        "SELECT file_id, name, local_path FROM pdf_files "
        "WHERE local_path IS NOT NULL AND zep_episode_uuid IS NULL"
    ).fetchall()


def mark_indexed(conn: sqlite3.Connection, file_id: int, episode_uuid: str) -> None:
    conn.execute(
        "UPDATE pdf_files SET zep_episode_uuid = ? WHERE file_id = ?",
        (episode_uuid, file_id),
    )
    conn.commit()


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Index PDFs into Zep Cloud graph.")
    parser.add_argument("--db",      default=str(DEFAULT_DB))
    parser.add_argument("--reindex", action="store_true",
                        help="Re-ingest all PDFs (clears existing graph first).")
    parser.add_argument("--limit",   type=int, default=0,
                        help="Process at most N PDFs (0 = all).")
    args = parser.parse_args()

    db_path = Path(args.db).expanduser()
    if not db_path.exists():
        print(f"ERROR: database not found: {db_path}")
        sys.exit(1)

    # Load API key
    try:
        api_key = _load_zep_key()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    zep = Zep(api_key=api_key)

    # Ensure graph exists
    try:
        zep.graph.get(graph_id=GRAPH_ID)
        print(f"Graph '{GRAPH_ID}' already exists.")
    except Exception:
        print(f"Creating graph '{GRAPH_ID}' ...")
        zep.graph.create(graph_id=GRAPH_ID, name=GRAPH_NAME, description=GRAPH_DESC)

    if args.reindex:
        print("--reindex: clearing existing graph episodes (nodes/edges will be rebuilt) ...")
        # Delete all episodes by clearing the graph
        try:
            zep.graph.delete(graph_id=GRAPH_ID)
            zep.graph.create(graph_id=GRAPH_ID, name=GRAPH_NAME, description=GRAPH_DESC)
            print("Graph cleared.\n")
        except Exception as e:
            print(f"  Warning: could not clear graph: {e}")

    # Open DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    ensure_zep_column(conn)

    rows = get_pending_pdfs(conn, args.reindex)
    if not rows:
        print("No PDFs to index.  All done!")
        conn.close()
        return

    if args.limit:
        rows = rows[:args.limit]

    print(f"Found {len(rows)} PDFs to index.\n")

    ok = 0
    skipped = 0
    for i, row in enumerate(rows, 1):
        file_id    = row["file_id"]
        name       = row["name"]
        local_path = Path(row["local_path"])

        label = name[:70]
        print(f"[{i}/{len(rows)}] {label}")

        if not local_path.exists():
            print(f"  ⚠  File not found: {local_path}")
            skipped += 1
            continue

        # Extract text
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

        # Send to Zep graph as an episode
        try:
            episode = zep.graph.add(
                data=text,
                type="text",
                graph_id=GRAPH_ID,
                source_description=f"PDF: {name}",
            )
            mark_indexed(conn, file_id, episode.uuid_)
            print(f"  ✓ Ingested → episode {episode.uuid_[:8]}...")
            ok += 1
        except Exception as e:
            print(f"  ✗ Zep error: {e}")
            skipped += 1
            continue

        # Brief pause to avoid hammering the API
        if i < len(rows):
            time.sleep(0.3)

    conn.close()
    print(f"\nDone.  Indexed: {ok}  Skipped: {skipped}")
    print(
        f"\nNote: Zep processes episodes asynchronously.\n"
        f"Nodes and edges will appear in the graph within a few minutes.\n"
        f"Run  python zep_app.py  or open the /zep route to search."
    )


if __name__ == "__main__":
    main()
