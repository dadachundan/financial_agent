#!/usr/bin/env python3
"""List the most recent rows from db/zsxq.db's pdf_files table.

Usage:
    python3 list_recent.py                       # latest 50
    python3 list_recent.py --limit 100
    python3 list_recent.py --limit 50 --subject "robotics"
    python3 list_recent.py --since 2026-05-01    # only since that date

Output: JSON {count, generated_at, rows:[{file_id, name, topic_title,
summary, create_time, page_count, tickers, tags, comment, bank,
ai_robotics_related, ai_related, robotics_related, semiconductor_related,
energy_related, claude_rating, user_rating}, ...]} sorted by
`create_time DESC`.

`--subject` does a case-insensitive LIKE substring filter against
`name`, `topic_title`, `summary`, `tags`, and `comment` before applying
`--limit`. This is a *coarse* filter — Claude does the real semantic
ranking from the titles/summaries downstream.

`--summary-chars N` truncates each row's summary to N chars (default
1500). Set 0 to disable. Useful when pulling 100+ rows.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "zsxq.db"

COLUMNS = [
    "file_id", "name", "topic_title", "summary",
    "create_time", "page_count", "file_size",
    "tickers", "tags", "comment", "bank",
    "ai_robotics_related", "ai_related", "robotics_related",
    "semiconductor_related", "energy_related",
    "claude_rating", "user_rating",
]


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _truncate(s: str | None, n: int) -> str | None:
    if s is None or n <= 0 or len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


def fetch(conn: sqlite3.Connection, limit: int, subject: str | None,
          since: str | None) -> list[dict]:
    cols = ", ".join(COLUMNS)
    where: list[str] = ["create_time IS NOT NULL"]
    params: list = []
    if subject:
        q = f"%{subject}%"
        where.append(
            "(name LIKE ? OR topic_title LIKE ? OR summary LIKE ? "
            "OR tags LIKE ? OR comment LIKE ?)"
        )
        params.extend([q, q, q, q, q])
    if since:
        where.append("create_time >= ?")
        params.append(since)
    sql = (
        f"SELECT {cols} FROM pdf_files "
        f"WHERE {' AND '.join(where)} "
        "ORDER BY create_time DESC LIMIT ?"
    )
    params.append(limit)
    cur = conn.execute(sql, params)
    rows = []
    for r in cur.fetchall():
        d = {c: r[c] for c in COLUMNS}
        rows.append(d)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50,
                    help="how many most-recent rows to return (default 50)")
    ap.add_argument("--subject", type=str, default="",
                    help="coarse LIKE filter against name/title/summary/"
                         "tags/comment. Leave empty for unfiltered latest.")
    ap.add_argument("--since", type=str, default="",
                    help="ISO date/timestamp; only include rows whose "
                         "create_time >= this string")
    ap.add_argument("--summary-chars", type=int, default=1500,
                    help="truncate each summary to this many chars "
                         "(0 = no cap, default 1500)")
    args = ap.parse_args()

    conn = _connect()
    try:
        rows = fetch(conn, args.limit, args.subject or None,
                     args.since or None)
    finally:
        conn.close()

    for r in rows:
        r["summary"] = _truncate(r["summary"], args.summary_chars)

    out = {
        "count": len(rows),
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "filters": {
            "limit": args.limit,
            "subject": args.subject or None,
            "since": args.since or None,
        },
        "rows": rows,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
