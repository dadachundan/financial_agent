#!/usr/bin/env python3
"""Download the latest SEC filings for a ticker into db/financial_reports.db.

Incremental: filings already in the DB are skipped automatically (the
existing pipeline pre-filters by max(filed_date) per form). On a brand-new
ticker, `--last` limits how many of each form are pulled so we don't grab
hundreds of 8-Ks on first contact.

Usage:
    python3 download_reports.py --ticker QCOM
    python3 download_reports.py --ticker QCOM --forms 10-K,10-Q,8-K --last 8
    python3 download_reports.py --ticker QCOM --all       # no per-form cap

Output: one progress line per filing on stdout. Exits 0 on success.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
sys.path.insert(0, str(PROJECT_ROOT))

import fetch_financial_report as fr  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--forms", default="10-K,10-Q,8-K",
                    help="comma-separated SEC form types (default 10-K,10-Q,8-K)")
    ap.add_argument("--last", type=int, default=8,
                    help="cap to N most-recent filings per form (default 8); "
                         "ignored if --all is set")
    ap.add_argument("--all", action="store_true",
                    help="no per-form cap (download every new filing)")
    args = ap.parse_args()

    fr.init_db()
    forms = [f.strip() for f in args.forms.split(",") if f.strip()]
    last  = 0 if args.all else args.last

    for sse in fr._run_download(args.ticker.upper(), forms, last=last):
        # `_sse()` wraps as 'data: {"msg":..., "done":...}\n\n' — unwrap to msg
        payload = sse
        if payload.startswith("data: "):
            payload = payload[len("data: "):]
        payload = payload.strip()
        if not payload:
            continue
        try:
            obj = json.loads(payload)
            print(obj.get("msg", payload), flush=True)
        except json.JSONDecodeError:
            print(payload, flush=True)


if __name__ == "__main__":
    main()
