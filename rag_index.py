#!/usr/bin/env python3
"""
rag_index.py — Chunk, embed, and store PDFs into a local Chroma vector DB.

Reads downloaded PDF paths from zsxq.db, extracts text with pdfplumber,
chunks into overlapping windows, embeds with bge-m3, and persists to Chroma.

Usage:
    python rag_index.py                        # index all PDFs with a local_path
    python rag_index.py --reindex              # re-embed everything from scratch
    python rag_index.py --db zsxq.db --chroma ./chroma_db
"""

import argparse
import sqlite3
import sys
from pathlib import Path

import chromadb
import pdfplumber
from sentence_transformers import SentenceTransformer

SCRIPT_DIR   = Path(__file__).parent
DEFAULT_DB   = SCRIPT_DIR / "zsxq.db"
DEFAULT_CHROMA = SCRIPT_DIR / "chroma_db"
COLLECTION   = "financial_pdfs"
EMBED_MODEL  = "BAAI/bge-m3"

CHUNK_SIZE   = 500   # characters (not tokens — fast, good enough for bge-m3)
CHUNK_OVERLAP = 80


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text(pdf_path: Path) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    return "\n\n".join(pages)


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return [c.strip() for c in chunks if c.strip()]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Index PDFs into Chroma vector DB.")
    parser.add_argument("--db",     default=str(DEFAULT_DB))
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA))
    parser.add_argument("--reindex", action="store_true",
                        help="Delete existing collection and re-embed from scratch.")
    args = parser.parse_args()

    db_path     = Path(args.db).expanduser()
    chroma_path = Path(args.chroma).expanduser()

    # Load PDFs from SQLite
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT file_id, name, local_path FROM pdf_files WHERE local_path IS NOT NULL"
    ).fetchall()
    conn.close()

    if not rows:
        print("No downloaded PDFs found in DB. Run zsxq_index.py first.")
        sys.exit(0)

    print(f"Found {len(rows)} PDFs in DB.\n")

    # Chroma setup
    client = chromadb.PersistentClient(path=str(chroma_path))
    if args.reindex:
        try:
            client.delete_collection(COLLECTION)
            print("Deleted existing collection for reindex.\n")
        except Exception:
            pass
    collection = client.get_or_create_collection(
        COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    # Already-indexed IDs (chunk IDs are "{file_id}_{chunk_idx}")
    existing_ids: set[str] = set()
    if not args.reindex:
        existing = collection.get(include=[])
        existing_ids = set(existing["ids"])

    # Load embedding model
    print(f"Loading embedding model: {EMBED_MODEL} ...")
    model = SentenceTransformer(EMBED_MODEL)
    print("Model ready.\n")

    total_chunks = 0
    for i, row in enumerate(rows, 1):
        file_id    = row["file_id"]
        name       = row["name"]
        local_path = Path(row["local_path"])

        print(f"[{i}/{len(rows)}] {name[:70]}")

        if not local_path.exists():
            print(f"  ⚠ File not found: {local_path}")
            continue

        # Skip if already indexed (unless reindex)
        first_chunk_id = f"{file_id}_0"
        if first_chunk_id in existing_ids:
            print(f"  ✓ Already indexed, skipping.")
            continue

        # Extract + chunk
        try:
            text = extract_text(local_path)
        except Exception as e:
            print(f"  ⚠ Could not extract text: {e}")
            continue

        if not text.strip():
            print(f"  ⚠ No text extracted.")
            continue

        chunks = chunk_text(text)
        print(f"  {len(text)} chars → {len(chunks)} chunks")

        # Embed
        vectors = model.encode(chunks, show_progress_bar=False, normalize_embeddings=True).tolist()

        # Store
        ids       = [f"{file_id}_{j}" for j in range(len(chunks))]
        metadatas = [{"file_id": file_id, "name": name, "chunk": j}
                     for j in range(len(chunks))]
        collection.add(documents=chunks, embeddings=vectors, ids=ids, metadatas=metadatas)

        total_chunks += len(chunks)
        print(f"  ✓ Stored {len(chunks)} chunks.")

    print(f"\nDone. Total chunks in collection: {collection.count()}  (+{total_chunks} this run)")
    print(f"Chroma DB: {chroma_path}")


if __name__ == "__main__":
    main()
