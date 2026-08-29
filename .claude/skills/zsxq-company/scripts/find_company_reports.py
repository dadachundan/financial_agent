#!/usr/bin/env python3
"""Find zsxq reports related to one company/ticker.

The script is intentionally read-only. It combines exact ticker/card matches
with the ranked FTS search helper so the agent gets a reliable reading queue.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db_paths import db_path
import zsxq_fts


DB_PATH = db_path("zsxq.db")


SELECT_COLS = """
    p.file_id, p.name, p.topic_title, p.summary, p.bank, p.create_time,
    p.page_count, p.tickers, p.local_path,
    c.primary_ticker, c.covered_tickers, c.theme, c.thesis, c.rating
"""


def connect_ro() -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def pdf_url(file_id: int, name: str) -> str:
    return zsxq_fts._pdf_url(file_id, name)


def add_row(out: dict[int, dict], row: sqlite3.Row | dict, reason: str, score: float) -> None:
    data = dict(row)
    file_id = int(data["file_id"])
    existing = out.get(file_id)
    if existing is None:
        local_path = data.get("local_path")
        out[file_id] = {
            "file_id": file_id,
            "name": data.get("name"),
            "topic_title": data.get("topic_title"),
            "summary": data.get("summary"),
            "bank": data.get("bank"),
            "create_time": data.get("create_time"),
            "page_count": data.get("page_count"),
            "tickers": data.get("tickers"),
            "local_path": local_path,
            "local_exists": bool(local_path and Path(local_path).exists()),
            "pdf_url": data.get("pdf_url") or pdf_url(file_id, data.get("name") or ""),
            "primary_ticker": data.get("primary_ticker") or data.get("card_primary_ticker"),
            "covered_tickers": data.get("covered_tickers"),
            "card_theme": data.get("theme") or data.get("card_theme"),
            "card_thesis": data.get("thesis"),
            "card_rating": data.get("rating"),
            "reasons": [reason],
            "rank_score": score,
        }
    else:
        if reason not in existing["reasons"]:
            existing["reasons"].append(reason)
        existing["rank_score"] += score


def structured_matches(conn: sqlite3.Connection, term: str, limit: int, out: dict[int, dict]) -> None:
    ticker = term.upper()
    pat = f"%{ticker}%"
    rows = conn.execute(
        f"""
        SELECT {SELECT_COLS}
        FROM pdf_files p
        LEFT JOIN pdf_cards c ON c.file_id = p.file_id
        WHERE upper(p.tickers) = ?
           OR upper(p.tickers) LIKE ?
           OR upper(c.primary_ticker) = ?
           OR upper(c.covered_tickers) LIKE ?
        ORDER BY p.create_time DESC
        LIMIT ?
        """,
        (ticker, pat, ticker, pat, limit),
    ).fetchall()
    for row in rows:
        add_row(out, row, "structured ticker/card match", 100.0)


def text_matches(term: str, limit: int, out: dict[int, dict]) -> None:
    queries = [term]
    ticker = term.upper()
    if ticker == "MRVL":
        queries += ["Marvell", "Marvell Technology", "custom silicon optical DSP switching"]
    elif len(term) <= 6 and term.isascii():
        queries.append(f"{term} company earnings stock")

    for query in queries:
        try:
            rows = zsxq_fts.search(query, limit=limit, summary_chars=1800)
        except sqlite3.OperationalError:
            zsxq_fts.ensure_index()
            rows = zsxq_fts.search(query, limit=limit, summary_chars=1800)
        for idx, row in enumerate(rows):
            score = max(1.0, 40.0 - idx)
            add_row(out, row, f"FTS query: {query}", score)


def main() -> int:
    ap = argparse.ArgumentParser(description="Find zsxq PDFs related to one company or ticker.")
    ap.add_argument("company", help="company name or ticker, e.g. MRVL")
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()

    term = args.company.strip()
    if not term:
        ap.error("company is required")

    out: dict[int, dict] = {}
    with connect_ro() as conn:
        structured_matches(conn, term, args.limit, out)
    text_matches(term, args.limit, out)

    rows = sorted(
        out.values(),
        key=lambda r: (
            not r["local_exists"],
            -r["rank_score"],
            -(r["page_count"] or 0),
            r["create_time"] or "",
        ),
    )[: args.limit]
    payload = {
        "company": term,
        "count": len(rows),
        "rows": rows,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
