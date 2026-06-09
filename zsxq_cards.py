"""
zsxq_cards.py — Agent-curated "cards" over the zsxq PDF library.

Each time Claude deep-reads a broker PDF (via /zsxq-analyze or /zsxq-expert), it
writes back a compact structured card: which tickers the report covers, its
theme, a one-paragraph thesis, and which comparison tables / figures live on
which pages. This turns the sparse native metadata (only ~5% of rows carry
tickers) into an index that compounds over the PDFs actually used, so the next
query is faster and the comparison tables are findable without re-reading.

This module IS the sanctioned Tier-2 write helper for the pdf_cards table — the
schema is owned by zsxq_common.init_db; all writes flow through upsert_card().
No raw DDL/DML against the table from anywhere else.

CLI (batch upsert from a JSON array on stdin, like scripts/persist_pts.py):
    python3 zsxq_cards.py <<'JSON'
    [{"file_id": 184124282514242, "primary_ticker": "ISRG",
      "covered_tickers": ["ISRG","SYK","MDT"], "theme": "surgical-robotics",
      "thesis": "Bull case on da Vinci installed-base razor-and-blade ...",
      "has_comparison_table": true,
      "key_tables": "p.7 ISRG vs SYK vs MDT procedure-volume & margin table",
      "key_figures": "p.4 installed-base CAGR chart", "rating": "Buy"}]
    JSON

    python3 zsxq_cards.py --get 184124282514242
    python3 zsxq_cards.py --ticker ISRG
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone

from db_paths import db_path

# Module-level DB constant — resolved through db_paths so FINAGENT_DB_DIR
# redirection reaches this module (see tests/test_db_paths.py).
DB_PATH = db_path("zsxq.db")

_FIELDS = (
    "covered_tickers", "primary_ticker", "theme", "thesis",
    "has_comparison_table", "key_tables", "key_figures", "rating", "card_json",
)


def _connect() -> sqlite3.Connection:
    """Open a writable connection with the card/FTS schema ensured via init_db."""
    import zsxq_common
    return zsxq_common.init_db(DB_PATH)


def _norm_tickers(v) -> str | None:
    if v is None:
        return None
    if isinstance(v, (list, tuple, set)):
        return ",".join(str(t).strip() for t in v if str(t).strip())
    return str(v).strip()


def upsert_card(file_id: int, *, covered_tickers=None, primary_ticker=None,
                theme=None, thesis=None, has_comparison_table=None,
                key_tables=None, key_figures=None, rating=None,
                card_json=None, conn: sqlite3.Connection | None = None) -> dict:
    """Insert or update the card for *file_id*.

    Only non-None fields overwrite; passing None leaves the existing value
    intact (COALESCE semantics), so a partial update — e.g. just adding a
    figure note — never wipes the thesis.
    """
    own = conn is None
    if own:
        conn = _connect()
    try:
        # file_id must exist in pdf_files (FK in spirit; we don't enforce, but
        # warn the caller via the return payload).
        known = conn.execute(
            "SELECT 1 FROM pdf_files WHERE file_id = ?", (file_id,)
        ).fetchone() is not None

        ct = _norm_tickers(covered_tickers)
        hct = None if has_comparison_table is None else int(bool(has_comparison_table))
        cj = json.dumps(card_json, ensure_ascii=False) if isinstance(card_json, (dict, list)) else card_json
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")

        existed = conn.execute(
            "SELECT 1 FROM pdf_cards WHERE file_id = ?", (file_id,)
        ).fetchone() is not None

        conn.execute(
            """
            INSERT INTO pdf_cards
                (file_id, covered_tickers, primary_ticker, theme, thesis,
                 has_comparison_table, key_tables, key_figures, rating,
                 card_json, updated_at)
            VALUES
                (:file_id, :covered_tickers, :primary_ticker, :theme, :thesis,
                 :has_comparison_table, :key_tables, :key_figures, :rating,
                 :card_json, :updated_at)
            ON CONFLICT(file_id) DO UPDATE SET
                covered_tickers      = COALESCE(excluded.covered_tickers,      pdf_cards.covered_tickers),
                primary_ticker       = COALESCE(excluded.primary_ticker,       pdf_cards.primary_ticker),
                theme                = COALESCE(excluded.theme,                 pdf_cards.theme),
                thesis               = COALESCE(excluded.thesis,               pdf_cards.thesis),
                has_comparison_table = COALESCE(excluded.has_comparison_table, pdf_cards.has_comparison_table),
                key_tables           = COALESCE(excluded.key_tables,           pdf_cards.key_tables),
                key_figures          = COALESCE(excluded.key_figures,          pdf_cards.key_figures),
                rating               = COALESCE(excluded.rating,               pdf_cards.rating),
                card_json            = COALESCE(excluded.card_json,            pdf_cards.card_json),
                updated_at           = excluded.updated_at
            """,
            {
                "file_id": file_id, "covered_tickers": ct,
                "primary_ticker": primary_ticker, "theme": theme, "thesis": thesis,
                "has_comparison_table": hct, "key_tables": key_tables,
                "key_figures": key_figures, "rating": rating, "card_json": cj,
                "updated_at": now,
            },
        )
        conn.commit()
        return {"file_id": file_id, "action": "updated" if existed else "inserted",
                "in_library": known}
    finally:
        if own:
            conn.close()


def upsert_cards(rows: list[dict], *, conn: sqlite3.Connection | None = None) -> list[dict]:
    own = conn is None
    if own:
        conn = _connect()
    try:
        out = []
        for row in rows:
            fid = row.get("file_id")
            if fid is None:
                out.append({"error": "missing file_id", "row": row})
                continue
            kwargs = {k: row.get(k) for k in _FIELDS}
            out.append(upsert_card(int(fid), conn=conn, **kwargs))
        return out
    finally:
        if own:
            conn.close()


def get_card(file_id: int, *, conn: sqlite3.Connection | None = None) -> dict | None:
    own = conn is None
    if own:
        conn = _connect()
    try:
        conn.row_factory = sqlite3.Row
        r = conn.execute("SELECT * FROM pdf_cards WHERE file_id = ?", (file_id,)).fetchone()
        return dict(r) if r else None
    finally:
        if own:
            conn.close()


def cards_for_ticker(ticker: str, *, limit: int = 50,
                     conn: sqlite3.Connection | None = None) -> list[dict]:
    """Return cards whose primary or covered tickers include *ticker*, newest first."""
    own = conn is None
    if own:
        conn = _connect()
    try:
        conn.row_factory = sqlite3.Row
        pat = f"%{ticker}%"
        rows = conn.execute(
            """SELECT c.*, p.name, p.create_time
               FROM pdf_cards c JOIN pdf_files p ON p.file_id = c.file_id
               WHERE c.primary_ticker = ? OR c.covered_tickers LIKE ?
               ORDER BY p.create_time DESC LIMIT ?""",
            (ticker, pat, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        if own:
            conn.close()


def stats(*, conn: sqlite3.Connection | None = None) -> dict:
    own = conn is None
    if own:
        conn = _connect()
    try:
        n = conn.execute("SELECT count(*) FROM pdf_cards").fetchone()[0]
        nct = conn.execute(
            "SELECT count(*) FROM pdf_cards WHERE has_comparison_table = 1"
        ).fetchone()[0]
        return {"cards": n, "with_comparison_table": nct}
    finally:
        if own:
            conn.close()


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Read/write agent cards over the zsxq library.")
    ap.add_argument("--get", type=int, metavar="FILE_ID", help="print one card as JSON")
    ap.add_argument("--ticker", help="list cards covering a ticker")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    if args.get is not None:
        card = get_card(args.get)
        print(json.dumps(card, ensure_ascii=False, indent=2) if card else "null")
        return 0
    if args.ticker:
        print(json.dumps(cards_for_ticker(args.ticker), ensure_ascii=False, indent=2))
        return 0
    if args.stats:
        print(json.dumps(stats(), ensure_ascii=False, indent=2))
        return 0

    # Default: batch-upsert a JSON array of cards from stdin.
    raw = sys.stdin.read().strip()
    if not raw:
        ap.error("provide a JSON array of cards on stdin, or use --get/--ticker/--stats")
    payload = json.loads(raw)
    if isinstance(payload, dict):
        payload = [payload]
    results = upsert_cards(payload)
    inserted = sum(1 for r in results if r.get("action") == "inserted")
    updated  = sum(1 for r in results if r.get("action") == "updated")
    print(json.dumps({"considered": len(payload), "inserted": inserted,
                      "updated": updated, "results": results,
                      "total_in_db": stats()["cards"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
