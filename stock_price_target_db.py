"""Storage for sell-side price targets extracted from zsxq broker PDFs.

Each row in ``price_targets`` represents one (company, broker, report) tuple:
a price-target call, the date of the report it came from, the zsxq ``file_id``
that lets you click through to the PDF viewer at
``http://xs-macbook-air.local:5001/zsxq/pdf-viewer/<file_id>``, and the
**point-in-time** stock price + market cap on the report date (so you can
later compute realized PT-vs-actual returns without re-fetching history).

Resolves its path through :func:`db_paths.db_path` so ``FINAGENT_DB_DIR``
correctly redirects to a sandbox copy during tests.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from db_paths import db_path

DB_PATH: Path = db_path("stock_price_target.db")

# Columns the table actually persists. Keys outside this set in a payload
# dict passed to upsert_target() are silently dropped — that way callers
# can carry extra context (exchange, chinese_name, …) for documentation
# without breaking the INSERT.
ALLOWED_COLS = {
    "company_ticker",
    "company_name",
    "research_institute",
    "rating",
    "price_target",
    "target_currency",
    "catalyst",
    "report_file_id",
    "report_pdf_filename",
    "report_url",
    "report_date",
    "report_date_price",
    "report_date_market_cap",
    "price_currency",
    "upside_pct",
    "created_at",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS price_targets (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Identity (exchange is implicit in the ticker suffix, e.g. ".HK", ".SS")
    company_ticker           TEXT NOT NULL,    -- e.g. "LLY", "1109.HK", "002847.SZ"
    company_name             TEXT NOT NULL,    -- English / Pinyin

    -- Report metadata
    research_institute       TEXT NOT NULL,    -- "Bernstein" / "Morgan Stanley" / "Goldman Sachs" / ...
    rating                   TEXT,             -- "Buy" / "Outperform" / "Overweight" / "Neutral" / "Underweight" / "Sell" / NULL
    price_target             REAL,             -- numeric PT in target_currency, NULL if no specific PT given
    target_currency          TEXT,             -- ISO ccy: USD / HKD / CNY / TWD / JPY / KRW
    catalyst                 TEXT,             -- 1-2 sentence catalyst / one-liner from the zsxq summary

    -- Source provenance (the zsxq PDF this PT came from)
    report_file_id           INTEGER NOT NULL, -- zsxq.db pdf_files.file_id
    report_pdf_filename      TEXT,             -- original PDF filename
    report_url               TEXT NOT NULL,    -- "http://xs-macbook-air.local:5001/zsxq/pdf-viewer/<file_id>"
    report_date              TEXT NOT NULL,    -- ISO date (YYYY-MM-DD) — from PDF name if present, else download date

    -- Point-in-time market data on report_date
    report_date_price        REAL,             -- close price on report_date in price_currency
    report_date_market_cap   REAL,             -- market cap on report_date in price_currency (NULL for indexes/private)
    price_currency           TEXT,             -- listing currency of the stock (often equals target_currency)
    upside_pct               REAL,             -- (price_target - report_date_price) / report_date_price * 100, NULL if either missing

    -- Bookkeeping
    created_at               TEXT NOT NULL,    -- ISO timestamp when this row was inserted

    -- One row per (ticker × broker × report). A broker can re-rate the same
    -- name in two different reports; that's two rows.
    UNIQUE(company_ticker, research_institute, report_file_id)
);

CREATE INDEX IF NOT EXISTS idx_ticker          ON price_targets(company_ticker);
CREATE INDEX IF NOT EXISTS idx_institute       ON price_targets(research_institute);
CREATE INDEX IF NOT EXISTS idx_report_date     ON price_targets(report_date);
CREATE INDEX IF NOT EXISTS idx_file_id         ON price_targets(report_file_id);
CREATE INDEX IF NOT EXISTS idx_rating          ON price_targets(rating);

-- A broker re-rating the same ticker on the same date in two different
-- PDFs (e.g. an ASCO mega-note + a single-company note from the same
-- analyst) is one call, not two. INSERT OR IGNORE skips the dup.
CREATE UNIQUE INDEX IF NOT EXISTS uq_ticker_broker_date
    ON price_targets(company_ticker, research_institute, report_date);
"""


@contextmanager
def _conn():
    """Open the DB, ensure schema, return a connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def upsert_target(row: dict, replace: bool = False) -> None:
    """Insert one price-target row.

    Required keys: ``company_ticker``, ``company_name``, ``research_institute``,
    ``report_file_id``, ``report_date``. Any extra keys (e.g. ``exchange``,
    ``chinese_name``) are silently dropped — keep them in the source-of-truth
    record literal if useful for documentation, but they won't be persisted.

    Args:
        row: payload dict — fields outside ALLOWED_COLS are filtered.
        replace: if True, use ``INSERT OR REPLACE`` so a conflict on either
            uniqueness key (``ticker × broker × file_id`` or ``ticker × broker
            × date``) overwrites the prior row instead of being ignored. The
            zsxq-analyze skill uses this because its full-PDF extraction
            should win over the summary-text extraction zsxq-recommend does.
            Default (False) = ``INSERT OR IGNORE`` — earlier row wins.
    """
    row = dict(row)  # don't mutate caller's dict
    row.setdefault("created_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    if "report_url" not in row and "report_file_id" in row:
        row["report_url"] = f"http://xs-macbook-air.local:5001/zsxq/pdf-viewer/{row['report_file_id']}"

    # Compute upside if both sides present
    if row.get("price_target") and row.get("report_date_price"):
        try:
            row["upside_pct"] = (row["price_target"] - row["report_date_price"]) / row["report_date_price"] * 100
        except Exception:
            pass

    # Drop any keys not in the live schema
    row = {k: v for k, v in row.items() if k in ALLOWED_COLS}

    cols = ", ".join(row.keys())
    qs = ", ".join("?" for _ in row)
    verb = "INSERT OR REPLACE" if replace else "INSERT OR IGNORE"
    sql = f"{verb} INTO price_targets ({cols}) VALUES ({qs})"
    with _conn() as c:
        c.execute(sql, list(row.values()))


def count() -> int:
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM price_targets").fetchone()[0]


if __name__ == "__main__":
    # Smoke test
    print(f"DB_PATH = {DB_PATH}")
    print(f"Existing rows: {count()}")
