"""Persist sell-side PT calls into ``stock_price_target.db``.

Shared helper used by **both** `/zsxq-recommend` (light extraction from
summary text) and `/zsxq-analyze` (high-fidelity extraction from full
PDF text). The agent emits a JSON array of records on stdin; this
script:

  1. Bulk-loads PDF metadata (filename, report_date) from db/zsxq.db
     for every file_id referenced.
  2. Looks up close price + market cap on report_date via yfinance once
     per (yf_ticker, date) tuple (cached in-process).
  3. Calls ``stock_price_target_db.upsert_target()`` per row.
  4. Emits a JSON summary on stdout.

The full record schema, currency / rating vocabulary, and which kinds
of PT mentions to skip are documented at
``reference/pt_extraction.md`` — read that first if you're not sure
what to emit.

Minimal record shape::

    {
      "ticker":       "1109.HK",        # yfinance form, REQUIRED
      "company_name": "CR Land",        # REQUIRED
      "broker":       "Goldman Sachs",  # REQUIRED
      "rating":       "Buy",            # optional
      "pt":           36.6,             # optional (number)
      "ccy":          "HKD",            # required if `pt` is set
      "catalyst":     "Tier-1 housing", # optional
      "file_id":      184152128158222   # REQUIRED — zsxq.db pdf_files.file_id
    }

Idempotency (no flags) → ``INSERT OR IGNORE``:
- ``(ticker, broker, file_id)`` AND ``(ticker, broker, date)``. A row
  already in either bucket is a no-op.

With ``--replace`` → ``INSERT OR REPLACE``:
- Same-conflict rows are overwritten. Use this from `/zsxq-analyze`
  because the deep-read extraction is more reliable than the
  summary-only path used by `/zsxq-recommend`; the analyze pass should
  win.

Usage (from either skill, or by hand)::

    python3 scripts/persist_pts.py <<'JSON'
    [...]
    JSON

    python3 scripts/persist_pts.py --replace <<'JSON'
    [...]
    JSON
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# project root = parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db_paths import db_path                           # noqa: E402
from stock_price_target_db import upsert_target, count # noqa: E402


# ---------------------------------------------------------------------------
# zsxq.db metadata lookup
# ---------------------------------------------------------------------------

def _derive_exchange(ticker: str) -> str:
    """Map yfinance-form ticker → legacy exchange code.

    The live ``price_targets`` schema (pre-migration) still has
    ``exchange TEXT NOT NULL``. ``INSERT OR IGNORE`` silently swallows NOT
    NULL violations, so omitting this field looks like a duplicate. Until
    `scripts/migrate_pt_drop_exch_zh.py --apply` lands, we derive a
    best-effort value here. For bare US tickers, default to NASDAQ — the
    column is for display only; the ticker itself is the source of truth.
    """
    t = (ticker or "").upper()
    if t.endswith(".HK"):  return "HKEX"
    if t.endswith(".SS"):  return "SSE"
    if t.endswith(".SH"):  return "SSE"
    if t.endswith(".SZ"):  return "SZSE"
    if t.endswith(".TWO"): return "TWO"
    if t.endswith(".TW"):  return "TWSE"
    if t.endswith(".T") or t.endswith(".JP"): return "TSE"
    if t.endswith(".KS") or t.endswith(".KQ"): return "KRX"
    if t.startswith("^") or t in {"SPX", "NDX", "DJI"}: return "INDEX"
    return "NASDAQ"  # bare US default — caller can override if known otherwise


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
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--replace", action="store_true",
        help="Use INSERT OR REPLACE instead of INSERT OR IGNORE — overwrite "
             "any row that conflicts on (ticker, broker, file_id) or (ticker, "
             "broker, date). Use this from /zsxq-analyze where the deep-read "
             "extraction is more reliable than the summary-only path used "
             "by /zsxq-recommend.",
    )
    p.add_argument(
        "--no-prices", action="store_true",
        help="Skip yfinance close/market-cap/currency lookups — leave "
             "report_date_price, report_date_market_cap, price_currency, "
             "upside_pct as NULL. Useful for bulk loads (yfinance is the "
             "dominant cost at scale). A separate backfill script can fill "
             "these later by re-walking rows with NULL report_date_price.",
    )
    args = p.parse_args()

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
    skipped = errored = replaced = 0
    # Track unique-key tuples that already existed BEFORE this batch, so we
    # can report how many of the considered records hit a conflict and were
    # either ignored (default) or overwritten (with --replace).
    from db_paths import db_path as _dbp
    existing_keys: set[tuple[str, str, int]] = set()
    existing_date_keys: set[tuple[str, str, str]] = set()
    with sqlite3.connect(_dbp("stock_price_target.db")) as ro:
        for row in ro.execute("SELECT company_ticker, research_institute, report_file_id, report_date FROM price_targets"):
            existing_keys.add((row[0], row[1], int(row[2])))
            existing_date_keys.add((row[0], row[1], row[3]))

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
        if args.no_prices:
            close, cap, ccy = None, None, None
        else:
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
            # Legacy NOT NULL column (until migrate_pt_drop_exch_zh runs).
            "exchange":               _derive_exchange(ticker),
        }
        broker_norm = payload["research_institute"]
        conflict_fid = (ticker, broker_norm, fid) in existing_keys
        conflict_date = (ticker, broker_norm, report_date) in existing_date_keys
        try:
            upsert_target(payload, replace=args.replace)
            if args.replace and (conflict_fid or conflict_date):
                replaced += 1
        except Exception as e:
            errored += 1
            print(f"  ! upsert failed for {ticker}/{rec.get('broker')}: {e}", file=sys.stderr)

    after = count()
    inserted = after - before              # net new rows
    # In default mode (INSERT OR IGNORE), anything that didn't insert and
    # wasn't skipped/errored is a duplicate. In --replace mode the count
    # tells us how many overwrote a prior row; the rest are still treated
    # as "duplicates" only if the new row had nothing actually changing.
    duplicate = max(0, len(records) - inserted - skipped - errored - replaced)
    summary = {
        "considered":  len(records),
        "inserted":    inserted,
        "replaced":    replaced,
        "duplicate":   duplicate,
        "skipped":     skipped,
        "errored":     errored,
        "total_in_db": after,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
