#!/usr/bin/env python3
"""List SEC filings for a ticker from the local /sec/ service (or DB fallback).

Usage:
    python3 list_reports.py --ticker AAPL [--form 10-K] [--last 10] [--all]

Output: JSON array of {id, ticker, form_type, filed_date, period_of_report,
period, local_path}. Sorted newest → oldest unless --asc is given.

Prefers the live API at http://localhost:5001/sec/reports; falls back to a
direct read of db/financial_reports.db if the server isn't reachable.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import urllib.request
import urllib.parse
import urllib.error

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "financial_reports.db"
API_BASE     = "http://localhost:5001/sec"


def _from_api(ticker: str, form: str | None, per_page: int = 200) -> list[dict] | None:
    qs = {"ticker": ticker.upper(), "per_page": per_page, "sort": "filed"}
    if form:
        qs["form"] = form
    url = f"{API_BASE}/reports?{urllib.parse.urlencode(qs)}"
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        rows = data.get("rows", [])
        # /reports returns at most per_page; paginate if needed
        pages = data.get("pages", 1)
        page  = 2
        while page <= pages:
            qs["page"] = page
            url = f"{API_BASE}/reports?{urllib.parse.urlencode(qs)}"
            with urllib.request.urlopen(url, timeout=2) as resp:
                d = json.loads(resp.read().decode("utf-8"))
            rows.extend(d.get("rows", []))
            page += 1
        return rows
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
        return None


def _from_db(ticker: str, form: str | None) -> list[dict]:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    sql = ("SELECT id, ticker, company_name, form_type, filed_date, "
           "period_of_report, period, local_path, accession_no "
           "FROM reports WHERE ticker = ?")
    params: list = [ticker.upper()]
    if form:
        sql += " AND form_type LIKE ?"
        params.append(f"%{form}%")
    sql += " ORDER BY filed_date DESC, id DESC"
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--form", default="10-K",
                    help="form type filter (e.g. 10-K, 10-Q, 8-K). "
                         "Use --all to get every form.")
    ap.add_argument("--all", action="store_true",
                    help="ignore --form and return all filings")
    ap.add_argument("--last", type=int, default=0,
                    help="keep only the most recent N filings (0 = all)")
    ap.add_argument("--quarters", type=int, default=0,
                    help="return the N most recent QUARTERLY filings (10-K "
                         "and 10-Q mixed, sorted by period_of_report DESC). "
                         "Overrides --form / --all when set.")
    ap.add_argument("--asc", action="store_true",
                    help="sort oldest → newest in output")
    args = ap.parse_args()

    if args.quarters and args.quarters > 0:
        # Pull 10-K + 10-Q (and their /A amendments), merge, sort by period
        rows_k = _from_api(args.ticker, "10-K")
        rows_q = _from_api(args.ticker, "10-Q")
        source = "api"
        if rows_k is None or rows_q is None:
            rows_k = _from_db(args.ticker, "10-K")
            rows_q = _from_db(args.ticker, "10-Q")
            source = "db"
        rows = (rows_k or []) + (rows_q or [])
        # Sort by period_of_report DESC (the actual quarter end) — fall back
        # to filed_date for safety
        rows.sort(
            key=lambda r: (r.get("period_of_report") or r.get("filed_date") or "",
                           r.get("filed_date") or ""),
            reverse=True,
        )
        rows = rows[: args.quarters]
    else:
        form = None if args.all else args.form
        rows = _from_api(args.ticker, form)
        source = "api"
        if rows is None:
            rows = _from_db(args.ticker, form)
            source = "db"
        if args.last and args.last > 0:
            rows = rows[: args.last]

    if args.asc:
        rows = list(reversed(rows))

    out = {
        "ticker": args.ticker.upper(),
        "source": source,
        "count":  len(rows),
        "rows":   rows,
    }
    json.dump(out, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
