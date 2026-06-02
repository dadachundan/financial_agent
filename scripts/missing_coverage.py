"""Surface tickers that have a price-target call in ``stock_price_target.db``
but are NOT yet covered by a ``reports/company/<…ticker…>/`` folder — sorted
by market cap descending so the user can decide where to spend the next
``/company-research`` slot.

The /zsxq-recommend skill runs this right after persisting PT calls, so the
"what's still missing" table is the last thing the user sees.

USAGE
=====

Default (one row per (ticker, broker), latest PT per pair):

    python3 .claude/skills/zsxq-recommend/scripts/missing_coverage.py

Flags:

  --limit N       cap to top N rows by market cap (default: no cap)
  --markdown      emit a github-markdown table (default text-table is
                  for inline shell viewing); the skill calls it with
                  ``--markdown`` so the output drops straight into chat
  --regions       comma list of regions to include: US,HK,CN,TW,JP,KR,IN.
                  Default: US,HK,CN (the ones the user typically wants
                  to research next; can be widened on demand).
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db_paths import db_path  # noqa: E402


# yfinance-suffix -> region label
_REGION_BY_SUFFIX = {
    ".HK":  "HK",
    ".SS":  "CN", ".SZ": "CN",
    ".TW":  "TW", ".TWO": "TW",
    ".T":   "JP", ".JP":  "JP",
    ".KS":  "KR",
    ".NS":  "IN", ".BO":  "IN",
    ".DE":  "EU", ".PA":  "EU", ".AS": "EU", ".SW": "EU",
    ".TO":  "CA", ".V":   "CA",
    ".AX":  "AU",
}


def _region(ticker: str) -> str:
    if not ticker:
        return "?"
    if ticker.startswith("^"):
        return "INDEX"
    if "." in ticker:
        suffix = "." + ticker.rsplit(".", 1)[1]
        return _REGION_BY_SUFFIX.get(suffix, "?")
    return "US"  # bare ticker = US (NYSE/NASDAQ/AMEX)


def _ticker_core(ticker: str) -> str:
    """The chunk we expect to find inside the folder name.

    Folder convention: ``EnglishName_(中文名_)?<EXCHANGE><CODE>``. The
    EXCHANGE part is letters (HKEX/SSE/SZSE/...) and the CODE is digits
    (or alphanumerics for US). We strip everything that isn't the code.
    """
    if not ticker:
        return ""
    if "." in ticker:
        return ticker.split(".", 1)[0]  # "1109.HK" -> "1109"
    return ticker  # "LLY"


_EXCH_PREFIX = (
    "HKEX|SSE|SZSE|TWSE|TWO|TSE|KRX|NASDAQ|NYSE|AMEX|TSX|XETR|BSE|ASX|HOSE"
)


def _folder_for_record(folders: list[str], ticker: str, company_name: str) -> str | None:
    """Match a (ticker, company_name) PT record to an existing
    ``reports/company/<folder>``. Returns the folder name or None.

    Two strategies:
      1. **Ticker code at end of folder** — matches the project's naming
         convention ``<English>_(中文_)?<EXCH><CODE>`` (e.g.
         ``Meituan_美团_HKEX3690``, ``Anpeilong_安培龙_SZSE301413``) and
         the underscore-separated variant ``<English>_<EXCH>_<CODE>``
         (e.g. ``AbbVie_NYSE_ABBV``, ``Hesai_NASDAQ_HSAI``).
      2. **Company-name prefix** — for cross-listings like BYD (PT call
         on H-share ``1211.HK`` but the existing folder is for the A-share
         ``BYD_SZSE002594``). If the company_name's first significant
         word appears as the start of a folder (followed by ``_``/``-``),
         count it as covered. Avoids 3-letter false positives by
         requiring the first word be ≥3 chars.
    """
    code = _ticker_core(ticker).upper()
    if code:
        # The boundary character RIGHT BEFORE the code is allowed to be
        # an underscore OR a letter (the exchange prefix attached form);
        # the character RIGHT AFTER must be end-of-string or '_'/'-'.
        pat = re.compile(
            rf"(?:_|{_EXCH_PREFIX}){re.escape(code)}(?:[_-]|$)",
            re.IGNORECASE,
        )
        for f in folders:
            if pat.search(f.upper()):
                return f

    if company_name:
        first = company_name.split()[0] if " " in company_name else company_name
        # strip trailing punctuation like "BYD," or "Inc."
        first = re.sub(r"[^A-Za-z一-鿿]+$", "", first)
        if len(first) >= 3:
            first_up = first.upper()
            for f in folders:
                f_up = f.upper()
                if f_up.startswith(first_up) and (
                    len(f_up) == len(first_up) or f_up[len(first_up)] in "_-"
                ):
                    return f
    return None


def _format_cap(cap: float | None, ccy: str | None) -> str:
    if not cap:
        return ""
    if cap >= 1e12:
        return f"{cap / 1e12:.1f}T {ccy or ''}".strip()
    if cap >= 1e9:
        return f"{cap / 1e9:.1f}B {ccy or ''}".strip()
    if cap >= 1e6:
        return f"{cap / 1e6:.0f}M {ccy or ''}".strip()
    return f"{cap:.0f} {ccy or ''}".strip()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0,
                   help="cap to top N rows by mkt cap (0 = no cap)")
    p.add_argument("--markdown", action="store_true",
                   help="emit a github-flavoured markdown table")
    p.add_argument("--regions", default="US,HK,CN",
                   help="comma list of regions to include")
    args = p.parse_args()

    target_regions = {r.strip().upper() for r in args.regions.split(",") if r.strip()}

    # 1. latest PT per (ticker, broker) — newest report_date wins
    pt_db = db_path("stock_price_target.db")
    if not pt_db.exists():
        print(f"ERROR: {pt_db} not found", file=sys.stderr)
        return 1

    with sqlite3.connect(pt_db) as c:
        rows = c.execute("""
            WITH ranked AS (
                SELECT *,
                       ROW_NUMBER() OVER (
                           PARTITION BY company_ticker
                           ORDER BY report_date DESC, id DESC
                       ) AS rn
                FROM price_targets
            )
            SELECT company_ticker, company_name, research_institute, rating,
                   price_target, target_currency,
                   report_date_price, report_date_market_cap, price_currency,
                   upside_pct, report_date, report_file_id, report_url
            FROM ranked
            WHERE rn = 1
            ORDER BY report_date_market_cap DESC NULLS LAST
        """).fetchall()

    # 2. existing report folders
    reports_dir = PROJECT_ROOT / "reports" / "company"
    folders = [p.name for p in reports_dir.iterdir() if p.is_dir()] if reports_dir.exists() else []

    # 3. filter to MISSING tickers in target regions
    missing = []
    for r in rows:
        ticker = r[0]
        reg = _region(ticker)
        if reg not in target_regions:
            continue
        if _folder_for_record(folders, ticker, r[1]):
            continue
        missing.append(r)

    if args.limit > 0:
        missing = missing[:args.limit]

    if not missing:
        print("✓ Every PT-mentioned ticker (in the requested regions) "
              "already has a report under reports/company/.")
        return 0

    # 4. render
    if args.markdown:
        print(f"\n### 🟡 PT-mentioned tickers without a `reports/company/` entry "
              f"({len(missing)} in {','.join(sorted(target_regions))}, sorted by mkt cap desc)\n")
        print("| # | Mkt Cap | Region | Ticker | Company | Broker | Rating | PT | Px @ Report | Upside | Report Date |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(missing, start=1):
            (tk, name, broker, rating, pt, pt_ccy, px, cap, px_ccy, ups, rd, fid, url) = r
            pt_str = f"{pt:.2f} {pt_ccy or ''}".strip() if pt is not None else ""
            px_str = f"{px:.2f} {px_ccy or ''}".strip() if px is not None else ""
            ups_str = f"{ups:+.1f}%" if ups is not None else ""
            print(f"| {i} | {_format_cap(cap, px_ccy)} | {_region(tk)} | "
                  f"`{tk}` | {name or ''} | {broker or ''} | {rating or ''} | "
                  f"{pt_str} | {px_str} | {ups_str} | {rd or ''} |")
    else:
        print(f"\n=== {len(missing)} PT-mentioned tickers without reports/company/ entry "
              f"(regions: {','.join(sorted(target_regions))}) ===")
        header = f"{'#':>3} {'Mkt Cap':>14} {'Reg':>4} {'Ticker':<14} {'Broker':<18} {'Rating':<14} {'PT':>12} {'Px':>12} {'Up%':>7}"
        print(header)
        print("-" * len(header))
        for i, r in enumerate(missing, start=1):
            (tk, name, broker, rating, pt, pt_ccy, px, cap, px_ccy, ups, rd, fid, url) = r
            cap_s = _format_cap(cap, px_ccy)
            pt_s = f"{pt:.1f} {pt_ccy or ''}".strip() if pt is not None else ""
            px_s = f"{px:.1f} {px_ccy or ''}".strip() if px is not None else ""
            ups_s = f"{ups:+.1f}%" if ups is not None else ""
            print(f"{i:>3} {cap_s:>14} {_region(tk):>4} {tk:<14} "
                  f"{(broker or '')[:18]:<18} {(rating or '')[:14]:<14} "
                  f"{pt_s:>12} {px_s:>12} {ups_s:>7}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
