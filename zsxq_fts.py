"""
zsxq_fts.py — Ranked full-text retrieval over the zsxq broker-PDF library.

This is the retrieval layer of the "PDF expert system": instead of the naive
unranked ``LIKE`` scan the viewer uses, it queries a trigram-tokenised FTS5
index (``pdf_files_fts``, created by ``zsxq_common.init_db``) and ranks hits by
BM25. The trigram tokenizer matches CJK and Latin substrings alike, so the
bilingual corpus (English + 中文 summaries) is searchable with one index.

Read-only by default. The FTS index itself is created/maintained through the
sanctioned helper ``zsxq_common.init_db`` (Tier-2 write path); this module never
issues raw DDL/DML against pdf_files — it only SELECTs, plus an opt-in
``ensure_index()`` that delegates to ``init_db``.

CLI:
    python3 zsxq_fts.py --query "Intuitive Surgical 手术机器人" --limit 20
    python3 zsxq_fts.py --query "surgical robotics" --bank "Morgan Stanley" --json
    python3 zsxq_fts.py --rebuild        # force-create / backfill the FTS index
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from urllib.parse import quote

from db_paths import db_path

# Module-level DB constant — resolved through db_paths so FINAGENT_DB_DIR
# redirection reaches this module (see tests/test_db_paths.py).
DB_PATH = db_path("zsxq.db")

# User-facing base for citation URLs (see feedback_urls_xs_macbook_air memory).
PDF_URL_BASE = "http://xs-macbook-air.local:5001/zsxq/pdf"

# Columns indexed by pdf_files_fts (must match zsxq_common._FTS_DDL).
_FTS_COLUMNS = ("name", "topic_title", "summary", "tickers", "bank", "tags", "comment")


# ── connections ────────────────────────────────────────────────────────────────

def _connect_ro() -> sqlite3.Connection:
    """Open a read-only connection to the library DB."""
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_index() -> None:
    """Create / backfill the FTS index via the sanctioned init_db helper.

    Idempotent. This is the only write path in this module, and it delegates to
    zsxq_common.init_db (the Tier-2 schema authority for zsxq.db) — never raw SQL.
    """
    import zsxq_common
    conn = zsxq_common.init_db(DB_PATH)
    conn.close()


def _has_fts(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='pdf_files_fts'"
    ).fetchone()
    return row is not None


# ── query building ──────────────────────────────────────────────────────────────

def _esc_phrase(s: str) -> str:
    """Escape a string for use inside an FTS5 double-quoted phrase."""
    return s.replace('"', '""')


def _build_fts_query(terms: list[str]) -> str | None:
    """Build an FTS5 MATCH expression from trigram-eligible (>=3 char) terms.

    Strategy mirrors graph_mirror.search but without prefix '*' (the trigram
    tokenizer does substring matching, so a quoted term already matches any
    superstring):
      1. exact full phrase   "intuitive surgical"      (highest relevance)
      2. all-terms AND        "intuitive" AND "surgical"
      3. any-term OR          "intuitive" OR "surgical"
    """
    eligible = [t for t in terms if len(t) >= 3]
    if not eligible:
        return None
    if len(eligible) == 1:
        return f'"{_esc_phrase(eligible[0])}"'
    phrase   = '"' + _esc_phrase(" ".join(eligible)) + '"'
    and_part = " AND ".join(f'"{_esc_phrase(t)}"' for t in eligible)
    or_part  = " OR ".join(f'"{_esc_phrase(t)}"' for t in eligible)
    return f"{phrase} OR ({and_part}) OR ({or_part})"


def _pdf_url(file_id: int, name: str, page: int | None = None) -> str:
    url = f"{PDF_URL_BASE}/{file_id}/{quote(name or '')}"
    if page:
        url += f"#page={page}"
    return url


def _row_to_dict(r: sqlite3.Row, score: float | None, summary_chars: int) -> dict:
    summary = r["summary"] or ""
    if summary_chars and len(summary) > summary_chars:
        summary = summary[:summary_chars].rstrip() + "…"
    return {
        "file_id":     r["file_id"],
        "name":        r["name"],
        "topic_title": r["topic_title"],
        "bank":        r["bank"],
        "create_time": r["create_time"],
        "page_count":  r["page_count"],
        "tickers":     r["tickers"],
        "summary":     summary,
        "score":       score,
        "has_card":    bool(r["card_file_id"]) if "card_file_id" in r.keys() else False,
        "card_primary_ticker": r["primary_ticker"] if "primary_ticker" in r.keys() else None,
        "card_theme":  r["theme"] if "theme" in r.keys() else None,
        "local_path":  r["local_path"],
        "pdf_url":     _pdf_url(r["file_id"], r["name"]),
    }


_SELECT_COLS = """
    p.file_id, p.name, p.topic_title, p.summary, p.bank, p.create_time,
    p.page_count, p.tickers, p.local_path,
    c.file_id AS card_file_id, c.primary_ticker, c.theme
"""


def _filters_sql(bank: str | None, ticker: str | None,
                 since: str | None) -> tuple[str, list]:
    clauses, params = [], []
    if bank:
        clauses.append("p.bank = ?")
        params.append(bank)
    if ticker:
        clauses.append("(p.tickers LIKE ? OR c.covered_tickers LIKE ?)")
        params += [f"%{ticker}%", f"%{ticker}%"]
    if since:
        clauses.append("p.create_time >= ?")
        params.append(since)
    return (" AND " + " AND ".join(clauses)) if clauses else "", params


def search(query: str, limit: int = 30, *, bank: str | None = None,
           ticker: str | None = None, since: str | None = None,
           summary_chars: int = 600,
           conn: sqlite3.Connection | None = None) -> list[dict]:
    """Return up to *limit* library PDFs matching *query*, BM25-ranked.

    FTS5 (trigram) is the primary path; a LIKE scan supplements when the query
    has no trigram-eligible term (e.g. a 2-char ticker / 2-char CJK term) or
    when FTS finds nothing. Structured filters (bank / ticker / since) AND with
    the text match. Each row is annotated with whether an agent card already
    exists, so callers can skip re-reading already-digested PDFs.
    """
    own_conn = conn is None
    if own_conn:
        conn = _connect_ro()
    try:
        terms = [t.strip() for t in query.split() if t.strip()]
        fts_query = _build_fts_query(terms) if _has_fts(conn) else None
        filt_sql, filt_params = _filters_sql(bank, ticker, since)

        results: dict[int, dict] = {}

        if fts_query:
            sql = f"""
                SELECT {_SELECT_COLS}, bm25(pdf_files_fts) AS score
                FROM pdf_files_fts
                JOIN pdf_files p ON pdf_files_fts.rowid = p.file_id
                LEFT JOIN pdf_cards c ON c.file_id = p.file_id
                WHERE pdf_files_fts MATCH ?{filt_sql}
                ORDER BY score LIMIT ?
            """
            try:
                rows = conn.execute(sql, [fts_query, *filt_params, limit]).fetchall()
            except sqlite3.OperationalError:
                rows = []
            for r in rows:
                results[r["file_id"]] = _row_to_dict(r, r["score"], summary_chars)

        # LIKE supplement: when FTS is absent/empty or short terms were dropped.
        if len(results) < limit:
            like_terms = terms or [query]
            like_clauses, like_params = [], []
            for t in like_terms:
                pat = f"%{t}%"
                like_clauses.append(
                    "(p.name LIKE ? OR p.topic_title LIKE ? OR p.summary LIKE ? "
                    "OR p.tickers LIKE ? OR c.covered_tickers LIKE ?)"
                )
                like_params += [pat, pat, pat, pat, pat]
            where = "(" + " AND ".join(like_clauses) + ")" if like_clauses else "1=1"
            sql = f"""
                SELECT {_SELECT_COLS}
                FROM pdf_files p
                LEFT JOIN pdf_cards c ON c.file_id = p.file_id
                WHERE {where}{filt_sql}
                ORDER BY p.create_time DESC LIMIT ?
            """
            rows = conn.execute(sql, [*like_params, *filt_params, limit]).fetchall()
            for r in rows:
                if r["file_id"] not in results:
                    results[r["file_id"]] = _row_to_dict(r, None, summary_chars)

        # FTS hits (have a score) rank first, ascending bm25; LIKE hits after.
        ordered = sorted(
            results.values(),
            key=lambda d: (d["score"] is None, d["score"] if d["score"] is not None else 0.0),
        )
        return ordered[:limit]
    finally:
        if own_conn:
            conn.close()


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Ranked FTS search over the zsxq PDF library.")
    ap.add_argument("--query", "-q", help="search text (English and/or 中文)")
    ap.add_argument("--limit", "-n", type=int, default=20)
    ap.add_argument("--bank", help="filter by canonical bank name (e.g. 'Morgan Stanley')")
    ap.add_argument("--ticker", help="filter by ticker substring (matches tickers/cards)")
    ap.add_argument("--since", help="only reports with create_time >= YYYY-MM-DD")
    ap.add_argument("--summary-chars", type=int, default=600)
    ap.add_argument("--ensure", action="store_true",
                    help="create/backfill the FTS index before searching")
    ap.add_argument("--rebuild", action="store_true",
                    help="force create/backfill the FTS index and exit")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    if args.rebuild:
        ensure_index()
        print("FTS index ensured / backfilled.")
        return 0
    if args.ensure:
        ensure_index()
    if not args.query:
        ap.error("--query is required (or use --rebuild)")

    rows = search(args.query, args.limit, bank=args.bank, ticker=args.ticker,
                  since=args.since, summary_chars=args.summary_chars)

    if args.json:
        print(json.dumps({"query": args.query, "count": len(rows), "rows": rows},
                         ensure_ascii=False, indent=2))
        return 0

    if not rows:
        print(f"No matches for: {args.query!r}")
        return 0
    print(f"{len(rows)} match(es) for {args.query!r}:\n")
    for i, r in enumerate(rows, 1):
        score = f"{r['score']:.2f}" if r["score"] is not None else "LIKE"
        card = " ★card" if r["has_card"] else ""
        bank = f" · {r['bank']}" if r["bank"] else ""
        tick = f" · {r['tickers']}" if r["tickers"] else ""
        print(f"{i:2d}. [{score}]{card} #{r['file_id']} ({r['create_time'][:10]}{bank}{tick})")
        print(f"    {r['name']}")
        if r["summary"]:
            print(f"    {r['summary'][:200]}")
        print(f"    {r['pdf_url']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
