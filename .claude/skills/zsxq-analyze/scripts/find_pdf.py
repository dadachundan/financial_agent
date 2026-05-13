#!/usr/bin/env python3
"""Look up a PDF row in db/zsxq.db.

Usage:
    python3 find_pdf.py --file-id 184124282514242
    python3 find_pdf.py --query "Deloitte 2026"          # name / topic_title LIKE
    python3 find_pdf.py --query "Deloitte" --limit 5

Output: JSON {count, rows:[{file_id, name, topic_title, summary,
local_path, file_size, page_count, create_time, tickers, tags, comment,
ai_robotics_analysis, categories_analysis, bank, group_id, claude_rating,
user_rating}, ...]}.

The query mode does a case-insensitive substring match on `name` and
`topic_title` (and falls back to `summary` / `tags` / `comment`). Rows are
sorted by `create_time DESC` (most recent first).
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "zsxq.db"

# Columns we surface to Claude. Order matters: most discriminating first.
COLUMNS = [
    "file_id", "name", "topic_title", "summary",
    "local_path", "file_size", "page_count",
    "create_time", "downloaded_at",
    "tickers", "tags", "comment",
    "ai_robotics_analysis", "categories_analysis",
    "bank", "group_id",
    "claude_rating", "user_rating",
]


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = {}
    for c in COLUMNS:
        try:
            d[c] = row[c]
        except (IndexError, KeyError):
            d[c] = None
    return d


def by_id(conn: sqlite3.Connection, file_id: int) -> list[dict]:
    cols = ", ".join(COLUMNS)
    cur = conn.execute(f"SELECT {cols} FROM pdf_files WHERE file_id = ?",
                       (file_id,))
    return [_row_to_dict(r) for r in cur.fetchall()]


def by_query(conn: sqlite3.Connection, query: str, limit: int) -> list[dict]:
    q = f"%{query}%"
    cols = ", ".join(COLUMNS)
    sql = (
        f"SELECT {cols} FROM pdf_files "
        "WHERE name LIKE ? OR topic_title LIKE ? "
        "OR summary LIKE ? OR tags LIKE ? OR comment LIKE ? "
        "ORDER BY create_time DESC LIMIT ?"
    )
    cur = conn.execute(sql, (q, q, q, q, q, limit))
    return [_row_to_dict(r) for r in cur.fetchall()]


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file-id", type=int)
    g.add_argument("--query", type=str,
                   help="substring to match against name / topic_title / "
                        "summary / tags / comment (case-insensitive LIKE)")
    ap.add_argument("--limit", type=int, default=10,
                    help="max rows for --query mode (default 10)")
    args = ap.parse_args()

    conn = _connect()
    try:
        if args.file_id is not None:
            rows = by_id(conn, args.file_id)
        else:
            rows = by_query(conn, args.query, args.limit)
    finally:
        conn.close()

    # Verify local_path existence so Claude knows whether extraction will
    # work without trying first.
    for r in rows:
        p = r.get("local_path")
        r["local_exists"] = bool(p) and Path(p).exists() if p else False

    out = {"count": len(rows), "rows": rows}
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
