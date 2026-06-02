"""Persist PT calls extracted by the zsxq-recommend agent into
``stock_price_target.db``.

Designed to be called from inside the /zsxq-recommend skill loop after the
agent has scanned the same summaries it's about to recommend on. The agent
emits a JSON array of records on stdin; this script:

  1. Bulk-loads PDF metadata (filename, report_date) from db/zsxq.db
     for every file_id referenced.
  2. Looks up close price + market cap on report_date via yfinance once
     per (yf_ticker, date) tuple (cached).
  3. Calls ``stock_price_target_db.upsert_target()`` per row.
  4. Reports counts to stderr; emits a JSON summary on stdout.

Input record schema (one JSON object per PT call the agent surfaced):

    {
      "ticker":          "1109.HK" | "LLY" | "300750.SZ"  (REQUIRED — used
                          both for yfinance lookup and as company_ticker
                          in the DB),
      "company_name":    "China Resources Land",          (REQUIRED)
      "broker":          "Goldman Sachs",                 (REQUIRED)
      "rating":          "Buy" | "Outperform" | ...       (OPTIONAL)
      "pt":              36.6,                            (OPTIONAL — number)
      "ccy":             "HKD" | "USD" | ...              (OPTIONAL —
                          required if pt is given),
      "catalyst":        "Tier-1 housing recovery; …",    (OPTIONAL)
      "file_id":         184152128158222                  (REQUIRED — links
                          back to the source zsxq PDF)
    }

A record is idempotent on (ticker, broker, file_id); re-running on the
same window does nothing if those rows already exist.

Usage from the skill::

    python3 .claude/skills/zsxq-recommend/scripts/persist_pts.py <<'JSON'
    [
      {"ticker":"LLY","company_name":"Eli Lilly","broker":"Bernstein",
       "rating":"Outperform","pt":1300,"ccy":"USD",
       "catalyst":"LIBRETTO-432 Selpercatinib RET+ adjuvant HR=0.17",
       "file_id":184152151455852}
    ]
    JSON
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Make project-root modules importable when this runs from the skill dir.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db_paths import db_path                           # noqa: E402
from stock_price_target_db import upsert_target, count # noqa: E402


# ---------------------------------------------------------------------------
# zsxq.db metadata lookup
# ---------------------------------------------------------------------------

def _report_date_from_pdf_name(name: str) -> str | None:
    """Parse YYMMDD from a PDF filename suffix like '-260602.pdf'."""
    m = re.search(r"-(\d{6})\.pdf$", name or "")
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%y%m%d").date().isoformat()
    except ValueError:
        return None


def _bulk_zsxq_meta(file_ids: list[int]) -> dict[int, dict]:
    """Return {file_id: {pdf_filename, report_date}} for the given ids."""
    if not file_ids:
        return {}
    out: dict[int, dict] = {}
    with sqlite3.connect(db_path("zsxq.db")) as c:
        qs = ",".join("?" * len(file_ids))
        rows = c.execute(
            f"SELECT file_id, name, create_time FROM pdf_files WHERE file_id IN ({qs})",
            file_ids,
        ).fetchall()
        for fid, name, ctime in rows:
            rd = _report_date_from_pdf_name(name) or (ctime[:10] if ctime else None)
            out[fid] = {"pdf_filename": name, "report_date": rd}
    return out


# ---------------------------------------------------------------------------
# yfinance close + market-cap lookup, cached per (ticker, date)
# ---------------------------------------------------------------------------

_PRICE_CACHE: dict[tuple[str, str], tuple[float | None, float | None, str | None]] = {}


def _close_and_cap(yf_ticker: str, report_date: str):
    """Return (close, market_cap, currency) on report_date. None if unknown."""
    if not yf_ticker or not report_date:
        return None, None, None
    key = (yf_ticker, report_date)
    if key in _PRICE_CACHE:
        return _PRICE_CACHE[key]

    close = cap = ccy = None
    try:
        import yfinance as yf
        t = yf.Ticker(yf_ticker)
        d = datetime.fromisoformat(report_date).date()
        hist = t.history(
            start=(d - timedelta(days=5)).isoformat(),
            end=(d + timedelta(days=2)).isoformat(),
        )
        if not hist.empty:
            sub = hist.loc[hist.index.date <= d]
            if not sub.empty:
                close = float(sub["Close"].iloc[-1])

        shares = None
        try:
            fi = t.fast_info
            shares = fi.get("shares") or fi.get("shareCount")
            ccy = fi.get("currency")
        except Exception:
            pass
        if not shares:
            try:
                info = t.info
                shares = info.get("sharesOutstanding")
                ccy = ccy or info.get("currency")
            except Exception:
                pass
        if close and shares:
            cap = close * shares
    except Exception as e:
        print(f"  ! yfinance lookup failed for {yf_ticker}: {e}", file=sys.stderr)

    _PRICE_CACHE[key] = (close, cap, ccy)
    return close, cap, ccy


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    try:
        records = json.loads(sys.stdin.read())
    except Exception as e:
        print(f"ERROR: stdin is not valid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(records, list):
        print("ERROR: stdin must be a JSON array of records", file=sys.stderr)
        return 2
    if not records:
        print(json.dumps({"inserted": 0, "considered": 0, "skipped": 0}))
        return 0

    file_ids = sorted({int(r["file_id"]) for r in records if "file_id" in r})
    meta = _bulk_zsxq_meta(file_ids)

    before = count()
    skipped = errored = 0
    for rec in records:
        try:
            ticker = rec["ticker"]
            fid = int(rec["file_id"])
        except Exception:
            skipped += 1
            print(f"  ! skipping (missing ticker/file_id): {rec}", file=sys.stderr)
            continue

        m = meta.get(fid) or {}
        report_date = m.get("report_date") or rec.get("report_date") or datetime.now(timezone.utc).date().isoformat()
        close, cap, ccy = _close_and_cap(ticker, report_date)

        payload = {
            "company_ticker":         ticker,
            "company_name":           rec.get("company_name") or ticker,
            "research_institute":     rec.get("broker") or "Unknown",
            "rating":                 rec.get("rating"),
            "price_target":           rec.get("pt"),
            "target_currency":        rec.get("ccy"),
            "catalyst":               rec.get("catalyst"),
            "report_file_id":         fid,
            "report_pdf_filename":    m.get("pdf_filename"),
            "report_date":            report_date,
            "report_date_price":      close,
            "report_date_market_cap": cap,
            "price_currency":         ccy,
        }
        try:
            upsert_target(payload)
        except Exception as e:
            errored += 1
            print(f"  ! upsert failed for {ticker}/{rec.get('broker')}: {e}", file=sys.stderr)

    after = count()
    summary = {
        "considered": len(records),
        "inserted":   after - before,    # net new rows (UNIQUE drops dups)
        "duplicate":  len(records) - (after - before) - skipped - errored,
        "skipped":    skipped,
        "errored":    errored,
        "total_in_db": after,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
