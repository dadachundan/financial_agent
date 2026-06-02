"""One-shot migration: drop `exchange` and `chinese_name` columns from
`price_targets`, and rewrite `report_url` from `/zsxq/pdf/...` to
`/zsxq/pdf-viewer/...`.

WHY THIS IS A SCRIPT, NOT AN AUTO-RUN
=====================================
Per the project-wide "Database Safety" rule in CLAUDE.md, Claude is not
allowed to run schema migrations (CREATE/DROP/ALTER) or row mutations
(UPDATE/INSERT/DELETE) against a real `*.db` directly. This migration
must be invoked by the user.

USAGE
=====
Dry-run / sandbox preview (recommended first):

    cp db/stock_price_target.db /tmp/pt-sandbox.db
    FINAGENT_DB_DIR=/tmp PT_DB_OVERRIDE=/tmp/pt-sandbox.db python3 \\
        scripts/migrate_pt_drop_exch_zh.py
    sqlite3 /tmp/pt-sandbox.db ".schema price_targets"
    sqlite3 /tmp/pt-sandbox.db "SELECT report_url FROM price_targets LIMIT 3;"

Real run (against db/stock_price_target.db):

    python3 scripts/migrate_pt_drop_exch_zh.py --apply

The script is idempotent — if the columns are already gone it exits clean.
The whole thing happens inside a single transaction, so a failure leaves
the original table untouched.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

# Path-resolution: honor PT_DB_OVERRIDE if set (for sandbox runs), else
# fall back to db_paths.db_path() which already honors FINAGENT_DB_DIR.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from db_paths import db_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="actually run the migration. Without this flag the script "
                             "prints what it WOULD do and exits.")
    args = parser.parse_args()

    override = os.environ.get("PT_DB_OVERRIDE")
    target = Path(override).resolve() if override else db_path("stock_price_target.db")

    if not target.exists():
        print(f"ERROR: target DB does not exist: {target}", file=sys.stderr)
        return 1

    # Read-only inspection first
    with sqlite3.connect(target) as ro:
        ro.row_factory = sqlite3.Row
        cols = [r[1] for r in ro.execute("PRAGMA table_info(price_targets)").fetchall()]
        n_rows = ro.execute("SELECT COUNT(*) FROM price_targets").fetchone()[0]
        n_old_url = ro.execute(
            "SELECT COUNT(*) FROM price_targets WHERE report_url LIKE '%/zsxq/pdf/%' "
            "AND report_url NOT LIKE '%/zsxq/pdf-viewer/%'"
        ).fetchone()[0]

    has_exchange  = "exchange" in cols
    has_chinese   = "chinese_name" in cols
    needs_url_fix = n_old_url > 0
    needs_schema_fix = has_exchange or has_chinese

    print(f"Target DB             : {target}")
    print(f"Rows in price_targets : {n_rows}")
    print(f"Has `exchange` column : {has_exchange}")
    print(f"Has `chinese_name`    : {has_chinese}")
    print(f"Rows with /pdf/ URL   : {n_old_url}  (will be rewritten to /pdf-viewer/)")
    print()

    if not (needs_schema_fix or needs_url_fix):
        print("Nothing to do — DB is already on the new schema.")
        return 0

    if not args.apply:
        print("(dry-run — pass --apply to execute)")
        return 0

    # Sanity: refuse to mutate anything outside /tmp or *.test.db / *.sandbox.db
    # UNLESS the path resolves through db_paths to the canonical project DB.
    canonical = db_path("stock_price_target.db").resolve()
    safe = (str(target) == str(canonical)
            or str(target).startswith("/tmp/")
            or target.name.endswith((".test.db", ".sandbox.db")))
    if not safe:
        print(f"REFUSING to mutate non-canonical, non-sandbox path: {target}",
              file=sys.stderr)
        return 2

    new_table_ddl = """
        CREATE TABLE price_targets_new (
            id                       INTEGER PRIMARY KEY AUTOINCREMENT,
            company_ticker           TEXT NOT NULL,
            company_name             TEXT NOT NULL,
            research_institute       TEXT NOT NULL,
            rating                   TEXT,
            price_target             REAL,
            target_currency          TEXT,
            catalyst                 TEXT,
            report_file_id           INTEGER NOT NULL,
            report_pdf_filename      TEXT,
            report_url               TEXT NOT NULL,
            report_date              TEXT NOT NULL,
            report_date_price        REAL,
            report_date_market_cap   REAL,
            price_currency           TEXT,
            upside_pct               REAL,
            created_at               TEXT NOT NULL,
            UNIQUE(company_ticker, research_institute, report_file_id)
        );
    """

    copy_sql = """
        INSERT INTO price_targets_new
            (id, company_ticker, company_name, research_institute, rating,
             price_target, target_currency, catalyst, report_file_id,
             report_pdf_filename, report_url, report_date, report_date_price,
             report_date_market_cap, price_currency, upside_pct, created_at)
        SELECT
            id, company_ticker, company_name, research_institute, rating,
            price_target, target_currency, catalyst, report_file_id,
            report_pdf_filename,
            REPLACE(report_url, '/zsxq/pdf/', '/zsxq/pdf-viewer/'),
            report_date, report_date_price,
            report_date_market_cap, price_currency, upside_pct, created_at
        FROM price_targets;
    """

    print("Running migration in a single transaction…")
    with sqlite3.connect(target) as c:
        c.execute("BEGIN")
        try:
            # Drop any leftover from a failed prior run
            c.execute("DROP TABLE IF EXISTS price_targets_new")
            c.executescript(new_table_ddl)
            c.execute(copy_sql)
            moved = c.execute("SELECT COUNT(*) FROM price_targets_new").fetchone()[0]
            if moved != n_rows:
                raise RuntimeError(f"row count mismatch: {moved} new vs {n_rows} old")
            c.execute("DROP TABLE price_targets")
            c.execute("ALTER TABLE price_targets_new RENAME TO price_targets")
            # Re-create indexes (schema-bound, not data-bound, so drop+create OK)
            for stmt in [
                "CREATE INDEX IF NOT EXISTS idx_ticker      ON price_targets(company_ticker)",
                "CREATE INDEX IF NOT EXISTS idx_institute   ON price_targets(research_institute)",
                "CREATE INDEX IF NOT EXISTS idx_report_date ON price_targets(report_date)",
                "CREATE INDEX IF NOT EXISTS idx_file_id     ON price_targets(report_file_id)",
                "CREATE INDEX IF NOT EXISTS idx_rating      ON price_targets(rating)",
            ]:
                c.execute(stmt)
            c.execute("COMMIT")
        except Exception:
            c.execute("ROLLBACK")
            raise

    # Verify post-state
    with sqlite3.connect(target) as ro:
        cols2 = [r[1] for r in ro.execute("PRAGMA table_info(price_targets)").fetchall()]
        n2 = ro.execute("SELECT COUNT(*) FROM price_targets").fetchone()[0]
        n_old_url2 = ro.execute(
            "SELECT COUNT(*) FROM price_targets WHERE report_url LIKE '%/zsxq/pdf/%' "
            "AND report_url NOT LIKE '%/zsxq/pdf-viewer/%'"
        ).fetchone()[0]

    print(f"OK. New columns       : {cols2}")
    print(f"   Rows after         : {n2}")
    print(f"   Stale /pdf/ URLs   : {n_old_url2} (should be 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
