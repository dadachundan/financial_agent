#!/usr/bin/env python3
"""
rag_query.py — Query the Chroma vector DB and answer via MiniMax.

Embeds the query with bge-m3, retrieves the top-k most relevant chunks,
then calls MiniMax to synthesize a grounded answer.

Usage:
    python rag_query.py "What are my views on humanoid robotics?"
    python rag_query.py "Which AI companies appear most often?" --top-k 10
    python rag_query.py "Build my investment preference profile" --top-k 20
"""

import argparse
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from minimax import call_minimax, MINIMAX_API_KEY

SCRIPT_DIR     = Path(__file__).parent
DEFAULT_CHROMA = SCRIPT_DIR / "chroma_db"
COLLECTION     = "financial_pdfs"
EMBED_MODEL    = "BAAI/bge-m3"

ANSWER_SYSTEM = (
    "You are a personal financial research assistant. You have been given excerpts "
    "from research reports that the user has chosen to save — these reflect their "
    "interests and investment preferences.\n\n"
    "Answer the user's question using only the provided excerpts. "
    "Be specific and cite the report name when referencing a finding. "
    "If the excerpts don't contain enough information, say so clearly."
)


def query(question: str, top_k: int = 8, chroma_path: Path = DEFAULT_CHROMA) -> str:
    # Load model + collection
    client = chromadb.PersistentClient(path=str(chroma_path))
    try:
        collection = client.get_collection(COLLECTION)
    except Exception:
        print("ERROR: Chroma collection not found. Run rag_index.py first.")
        sys.exit(1)

    print(f"Embedding query with {EMBED_MODEL}...")
    model = SentenceTransformer(EMBED_MODEL)
    query_vec = model.encode([question], normalize_embeddings=True).tolist()

    # Retrieve top-k chunks
    results = collection.query(query_embeddings=query_vec, n_results=top_k,
                               include=["documents", "metadatas", "distances"])
    docs      = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not docs:
        print("No relevant chunks found.")
        sys.exit(0)

    # Build context block
    context_parts = []
    for doc, meta, dist in zip(docs, metadatas, distances):
        similarity = 1 - dist   # cosine: distance=0 → similarity=1
        context_parts.append(
            f"[Report: {meta['name']} | chunk {meta['chunk']} | score {similarity:.2f}]\n{doc}"
        )
    context = "\n\n---\n\n".join(context_parts)

    print(f"Retrieved {len(docs)} chunks. Calling MiniMax...\n")

    user_msg = f"Question: {question}\n\nRelevant excerpts:\n\n{context}"
    text, elapsed, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": ANSWER_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.3,
        max_completion_tokens=1200,
    )
    print(f"[MiniMax {elapsed:.1f}s]\n")
    return text


def main():
    parser = argparse.ArgumentParser(description="Query your PDF knowledge base.")
    parser.add_argument("question", help="Natural language question to ask.")
    parser.add_argument("--top-k",  type=int, default=8,
                        help="Number of chunks to retrieve (default: 8).")
    parser.add_argument("--chroma", default=str(DEFAULT_CHROMA))
    args = parser.parse_args()

    if not MINIMAX_API_KEY:
        print("ERROR: MINIMAX_API_KEY not found in config.py")
        sys.exit(1)

    answer = query(args.question, top_k=args.top_k,
                   chroma_path=Path(args.chroma).expanduser())
    print(answer)


if __name__ == "__main__":
    main()
