"""
Market Complacency Dashboard — reusable build script.

Usage:
  python .claude/skills/market-complacency/scripts/build_dashboard.py
  python .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07
  python .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07 --window-years 10

Pulls 10y history for up to 13 indicators (10 required + 3 optional),
computes per-indicator 10y percentile ranks (inverted for "low = complacent"
indicators), assembles a weighted composite 0-100 score, maps to a 5-tier
verdict, and surfaces historical precedents within ±5 of today's score.

Outputs:
  oneoff/market_complacency_<DATE>_indicators.csv
  oneoff/market_complacency_<DATE>_precedents.csv
  oneoff/market_complacency_<DATE>_composite_history.csv
  reports/charts/market_complacency_<DATE>_*.png

The agent (Claude in conversation) then reads the CSVs and writes
reports/market-complacency/market_complacency_<DATE>.md. The report-writing
step is NOT in this script — it stays the agent's responsibility.

Read-only against db/indicators.db. No LLM API calls anywhere.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import io
import json
import sys
import urllib.request
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

# ── FRED API key (optional) ──────────────────────────────────────────────────
# When available, the API gives more reliable pulls than the public CSV
# endpoint and lets us query specific series the CSV doesn't expose. The
# project's config.py holds the key under FRED_API_KEY.
_FRED_API_KEY: str | None = None
try:
    import sys as _sys
    _sys.path.insert(0, "/Users/x/projects/financial_agent")
    import config as _cfg  # type: ignore
    _FRED_API_KEY = getattr(_cfg, "FRED_API_KEY", None) or None
except Exception:
    _FRED_API_KEY = None

# ── Path resolution ──────────────────────────────────────────────────────────
# .claude/skills/market-complacency/scripts/build_dashboard.py
#   parents[0] = scripts
#   parents[1] = market-complacency
#   parents[2] = skills
#   parents[3] = .claude
#   parents[4] = PROJECT ROOT
PROJECT_ROOT = Path(__file__).resolve().parents[4]
ONEOFF = PROJECT_ROOT / "oneoff"
CHARTS = PROJECT_ROOT / "reports" / "charts"
REPORT_DIR = PROJECT_ROOT / "reports" / "market-complacency"
ONEOFF.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Use indicators module's FRED helper if available; otherwise inline a copy.
sys.path.insert(0, str(PROJECT_ROOT))
try:
    from indicators.data_fetcher import _fetch_fred_range  # type: ignore
except Exception:
    def _fetch_fred_range(series_id: str, start: str, end: str | None = None) -> list[dict]:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
        if end:
            url += f"&coed={end}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            rows = []
            for line in text.strip().splitlines()[1:]:
                parts = line.split(",")
                if len(parts) < 2:
                    continue
                date, raw = parts[0].strip(), parts[1].strip()
                if raw in ("", "."):
                    continue
                try:
                    rows.append({"date": date, "value": float(raw)})
                except ValueError:
                    continue
            return rows
        except Exception as exc:
            print(f"  FRED CSV fetch failed for {series_id}: {exc}", file=sys.stderr)
            return []


# ── Indicator catalogue ──────────────────────────────────────────────────────
# direction: "low" = low value means complacent (invert pct);
#            "high" = high value means complacent (use pct as-is).
INDICATORS = [
    # Credit
    {"id": "hy_oas",   "name": "HY OAS",                "source": "fred",  "code": "BAMLH0A0HYM2",     "direction": "low",  "weight": 0.13, "required": True,  "unit": "%",  "category": "Credit"},
    {"id": "ig_oas",   "name": "IG OAS",                "source": "fred",  "code": "BAMLC0A0CM",       "direction": "low",  "weight": 0.06, "required": True,  "unit": "%",  "category": "Credit"},
    {"id": "ccc_oas",  "name": "CCC OAS",               "source": "fred",  "code": "BAMLH0A3HYC",      "direction": "low",  "weight": 0.08, "required": True,  "unit": "%",  "category": "Credit"},
    # NEW v2: CCC - HY spread (credit-tier divergence). Higher = CCC widening
    # relative to HY = late-cycle stress already showing in the weakest tier.
    # When this spread is LOW (tight relative to HY), credit is uniformly tight
    # → that's the "uniform complacency" regime. When HIGH, CCC is already
    # cracking → the dashboard should already be warning even if broad HY is OK.
    # Backtest motivation: this spread widened ~12 months before GFC, ~6 months
    # before Q4 2018. The original dashboard missed both.
    {"id": "ccc_hy_spread", "name": "CCC − HY OAS spread", "source": "derived_ccc_hy", "code": None, "direction": "low", "weight": 0.05, "required": True, "unit": "pp", "category": "Credit"},
    # NEW v3: Moody's BAA - 10Y Treasury (BAA10Y) is the long-history IG-credit
    # proxy. Goes back to January 1986 (40 years, ~10,000 daily obs) so percentile
    # ranks can be computed against a true 25-year window — unlike the ICE BofA
    # OAS series which FRED only carries back to 2023-06 (post-relicensing).
    # The two indicators are correlated 0.56 in their overlap window (mid-2023
    # to today), with BAA10Y running ~70-80bp wider on average because BAA
    # captures only the BBB tier (vs IG OAS's AAA/AA/A/BBB blend) and includes
    # longer-duration bonds. Tracking it separately means our composite gets
    # cycle-context for credit that the ICE BofA series alone can't provide.
    {"id": "baa10y",  "name": "Moody's BAA − 10Y",   "source": "fred",  "code": "BAA10Y", "direction": "low", "weight": 0.05, "required": True, "unit": "pp", "category": "Credit"},
    # NEW v4 (added 2026-06-07 after reading Citi BMC report): Yield curve
    # slope (10Y - 2Y Treasury). The most-cited bear-market lead indicator
    # in finance — the curve has inverted before every US recession since
    # 1969. FRED T10Y2Y goes back to 1976. Citi's BMC thresholds at start of
    # Mar 2000 (-50bp inverted) and Oct 2007 (0bp flat); today +41bp.
    # Direction = "low" because a flatter / inverted curve has historically
    # preceded the regime turn that complacency unwinds into. NOTE: this
    # captures "late-cycle flattening" complacency well; it does NOT capture
    # the "early-cycle steepness" regime which is also late in a different
    # cycle. Acceptable trade-off for a single percentile rank.
    {"id": "yc_10y2y", "name": "Yield Curve (10Y−2Y)", "source": "fred",  "code": "T10Y2Y", "direction": "low", "weight": 0.05, "required": True, "unit": "pp", "category": "Yield Curve"},
    # NEW v4: S&P 500 dividend yield from multpl. Long history, simple
    # valuation indicator. Low DY = stocks expensive relative to cash returns.
    # Citi BMC thresholds: amber ~2.1%, red ~1.3% (low = warning). Today ~1.6%.
    {"id": "spx_dy",   "name": "S&P 500 Dividend Yield", "source": "spx_dy", "code": None,    "direction": "low", "weight": 0.05, "required": False, "unit": "%",  "category": "Valuation"},
    # NEW v5 (added after Citi BMC review of missing factors):
    # EPS distance from rolling 10y peak — proxies Citi's "EPS from previous
    # peak" indicator. Computed from multpl monthly trailing S&P 500 EPS
    # (1871-present). When current EPS is at the rolling-10y high, value = 0;
    # otherwise negative. Citi treats high-from-peak as complacent (cycle high).
    # Direction "high" because closer to 0 = at the peak = complacent.
    {"id": "eps_peak", "name": "EPS dist from 10y peak", "source": "eps_peak", "code": None, "direction": "high", "weight": 0.05, "required": False, "unit": "%",  "category": "Profitability"},
    # FINRA Investor Margin Debt — proxies Levkovich-style leverage exuberance.
    # Monthly back to 1997 from FINRA's published xlsx. The level grows with the
    # market; what matters is **margin debt as % of S&P 500 market cap**, which
    # the script derives from SPY market cap proxy. Persistently high % = late-
    # cycle leverage-driven exuberance.
    {"id": "margin_debt_pct", "name": "Margin Debt / Mkt Cap", "source": "margin_debt", "code": None, "direction": "high", "weight": 0.04, "required": False, "unit": "%", "category": "Sentiment"},
    # Capex Growth (YoY) — Citi's BMC has this as a direct factor with red flag
    # at ~11% YoY. Source: FRED PNFI (Private Nonresidential Fixed Investment),
    # quarterly back to 1947 — broader than S&P 500-only but captures the
    # aggregate US capex cycle. Direction "high" — strong capex growth at this
    # point in the cycle is typically late-stage exuberance.
    {"id": "capex_yoy", "name": "US Capex YoY (PNFI)", "source": "capex_yoy", "code": None, "direction": "high", "weight": 0.04, "required": False, "unit": "%", "category": "Corporate Behaviour"},
    # CBOE Equity Put/Call Ratio — proxies Levkovich sentiment. Daily back to
    # Nov 2006, but the public CSV stops at Oct 2019 (CBOE moved newer data
    # behind a portal). Included anyway because it's useful for the backtest's
    # pre-2019 history; reports for 2026 will show "n/a — source stale" and
    # the indicator drops from the composite via the standard re-norm. Low
    # put/call = complacent (calls dominate).
    {"id": "put_call", "name": "CBOE Equity Put/Call Ratio", "source": "put_call", "code": None, "direction": "low", "weight": 0.03, "required": False, "unit": "×", "category": "Sentiment"},
    # Equity vol
    {"id": "vix",      "name": "VIX",                   "source": "yf",    "code": "^VIX",              "direction": "low",  "weight": 0.10, "required": True,  "unit": "",   "category": "Equity Vol"},
    {"id": "vvix",     "name": "VVIX",                  "source": "yf",    "code": "^VVIX",             "direction": "low",  "weight": 0.05, "required": True,  "unit": "",   "category": "Equity Vol"},
    {"id": "vix_slope","name": "VIX Term Slope (9D/3M)","source": "ratio", "code": ("^VIX9D","^VIX3M"), "direction": "low",  "weight": 0.05, "required": True,  "unit": "×",  "category": "Equity Vol"},
    {"id": "skew",     "name": "SKEW",                  "source": "yf",    "code": "^SKEW",             "direction": "low",  "weight": 0.05, "required": True,  "unit": "",   "category": "Equity Vol"},
    # Rate vol
    {"id": "move",     "name": "MOVE",                  "source": "yf",    "code": "^MOVE",             "direction": "low",  "weight": 0.08, "required": True,  "unit": "",   "category": "Rate Vol"},
    # Risk premium
    {"id": "erp",      "name": "Equity Risk Premium",   "source": "derived_erp", "code": None,         "direction": "low",  "weight": 0.10, "required": True,  "unit": "pp", "category": "Risk Premium"},
    {"id": "hyg_lqd",  "name": "HYG/LQD Ratio",         "source": "ratio_etf", "code": ("HYG","LQD"),   "direction": "high", "weight": 0.05, "required": True,  "unit": "×",  "category": "Risk Premium"},
    # Sentiment (optional)
    {"id": "aaii",     "name": "AAII Bull-Bear Spread", "source": "aaii",  "code": None,                "direction": "high", "weight": 0.05, "required": False, "unit": "pp", "category": "Sentiment"},
    {"id": "naaim",    "name": "NAAIM Exposure",        "source": "naaim", "code": None,                "direction": "high", "weight": 0.05, "required": False, "unit": "",   "category": "Sentiment"},
    # Valuation (optional)
    {"id": "cape",     "name": "Shiller CAPE",          "source": "cape",  "code": None,                "direction": "high", "weight": 0.10, "required": False, "unit": "×",  "category": "Valuation"},
]


# ── Fetchers ────────────────────────────────────────────────────────────────

def _fetch_fred_via_api(series_id: str, start: str) -> list[dict]:
    """Use the FRED JSON API when an API key is present. Returns the full
    available history of the series — works for both the new ICE BofA series
    (data only starts 2023-06) and the long-history Moody's series (back to
    1986+) that the public CSV endpoint can't reach.
    """
    if not _FRED_API_KEY:
        return []
    import json
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&observation_start={start}"
        f"&file_type=json&api_key={_FRED_API_KEY}&limit=100000"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        rows = []
        for o in data.get("observations", []):
            if o.get("value") in ("", "."):
                continue
            try:
                rows.append({"date": o["date"], "value": float(o["value"])})
            except (TypeError, ValueError):
                continue
        return rows
    except Exception as exc:
        print(f"  FRED API fetch failed for {series_id}: {exc}", file=sys.stderr)
        return []


def fetch_fred(series_id: str, start: str) -> pd.Series:
    # Prefer the API when a key is available — it returns the full series
    # history without the public CSV's silent 3-year truncation.
    rows = _fetch_fred_via_api(series_id, start) or _fetch_fred_range(series_id, start)
    if not rows:
        return pd.Series(dtype=float)
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["value"].sort_index()


def fetch_yf(ticker: str, start: str, end: str) -> pd.Series:
    try:
        df = yf.download(ticker, start=start, end=end, progress=False,
                         auto_adjust=True, threads=False)
    except Exception as exc:
        print(f"  yfinance error {ticker}: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)
    if df.empty:
        return pd.Series(dtype=float)
    if isinstance(df.columns, pd.MultiIndex):
        s = df["Close"].iloc[:, 0]
    else:
        s = df["Close"]
    s.name = ticker
    # Strip timezone for clean joins downstream
    if s.index.tz is not None:
        s.index = s.index.tz_localize(None)
    return s.dropna()


def fetch_multpl_eps_peak(date_slug: str) -> pd.Series:
    """S&P 500 trailing EPS distance from rolling 10-year peak.

    Multpl trailing EPS series (1871-present, monthly), then for each date
    compute (EPS_t / max(EPS over trailing 120 months) - 1) × 100. Result
    is ≤ 0 always; closer to 0 = nearer the cycle peak = more complacent.
    """
    cache = ONEOFF / f"sp500_eps_peak_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["eps_peak_pct"].sort_index()
    import re
    import html
    url = "https://www.multpl.com/s-p-500-earnings/table/by-month"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S)
        out = []
        for r in rows:
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if len(cells) < 2:
                continue
            try:
                dt = pd.to_datetime(cells[0])
                eps = float(re.sub(r"[†$  \s]", "", cells[1]))
                out.append({"date": dt, "eps": eps})
            except Exception:
                continue
        df = pd.DataFrame(out).sort_values("date").set_index("date")
        # Rolling 10-year max (120 months); peak distance
        df["peak"] = df["eps"].rolling(120, min_periods=12).max()
        df["eps_peak_pct"] = (df["eps"] / df["peak"] - 1) * 100
        df[["eps_peak_pct"]].dropna().to_csv(cache)
        return df["eps_peak_pct"].dropna()
    except Exception as exc:
        print(f"  EPS-peak fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_finra_margin(date_slug: str) -> pd.Series:
    """FINRA margin debt as % of S&P 500 market cap.

    Margin debt grows with the market mechanically; the relevant signal is
    leverage *intensity* = margin debt ÷ S&P 500 market cap. SPY market cap
    proxy: use yfinance S&P 500 level × an assumed shares outstanding (constant)
    for the percentile — equivalently, use SPY price as the denominator and the
    rank captures relative leverage.
    """
    cache = ONEOFF / f"finra_margin_pct_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["margin_pct"].sort_index()
    url = "https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        xlb = urllib.request.urlopen(req, timeout=60).read()
        xl = pd.read_excel(io.BytesIO(xlb), sheet_name="Customer Margin Balances")
        # Columns: Year-Month, Debit Balances in Customers' Securities Margin Accounts,
        #          Free Credit Balances ... (various)
        debit_col = next((c for c in xl.columns if "Debit" in str(c)), None)
        if debit_col is None:
            debit_col = xl.columns[1]
        df = xl[[xl.columns[0], debit_col]].copy()
        df.columns = ["date", "margin_debt"]
        df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y-%m", errors="coerce")
        df["margin_debt"] = pd.to_numeric(df["margin_debt"], errors="coerce")
        df = df.dropna().sort_values("date")
        # Normalize by S&P 500 level (proxy for market cap)
        spx = fetch_yf("^GSPC", start="1996-01-01", end="2026-06-08")
        if spx.empty:
            print("  ! S&P 500 fetch failed; using raw margin debt", file=sys.stderr)
            df["margin_pct"] = df["margin_debt"]
        else:
            spx_monthly = spx.resample("MS").last()
            merged = pd.merge_asof(df.sort_values("date"),
                                   spx_monthly.rename("spx").reset_index().rename(columns={"Date":"date"}),
                                   on="date", direction="nearest")
            # margin_pct = margin_debt ($M) / SPX level (a scale-free proxy ratio)
            merged["margin_pct"] = merged["margin_debt"] / merged["spx"]
            df = merged.dropna(subset=["margin_pct"])[["date","margin_pct"]]
        df.to_csv(cache, index=False)
        return df.set_index("date")["margin_pct"]
    except Exception as exc:
        print(f"  FINRA margin fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_capex_yoy(date_slug: str, start: str) -> pd.Series:
    """US capex YoY growth from FRED PNFI (Private Nonresidential Fixed
    Investment), quarterly back to 1947. Resampled to monthly via forward-fill;
    YoY = (PNFI_t / PNFI_{t-12} - 1) × 100. Direction "high" → fast capex
    growth at this point in the cycle is late-stage exuberance.
    """
    cache = ONEOFF / f"capex_yoy_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["capex_yoy"].sort_index()
    rows = _fetch_fred_via_api("PNFI", start) or _fetch_fred_range("PNFI", start)
    if not rows:
        return pd.Series(dtype=float)
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()["value"]
    df = df.resample("MS").ffill()
    yoy = (df / df.shift(12) - 1) * 100
    yoy = yoy.rename("capex_yoy").dropna()
    yoy.to_frame().to_csv(cache)
    return yoy


def fetch_cboe_putcall(date_slug: str) -> pd.Series:
    """CBOE equity put/call ratio from cdn.cboe.com. Daily Nov 2006 → Oct 2019
    (public CSV is stale post-2019). Returned as 21-day rolling mean to smooth
    daily noise.
    """
    cache = ONEOFF / f"cboe_putcall_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["pc_ratio"].sort_index()
    url = "https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        # First 2 lines are header notice + product line; line 3 is the column header
        lines = text.strip().splitlines()
        # Find the header row (starts with "DATE,")
        hdr_idx = next((i for i, line in enumerate(lines) if line.upper().startswith("DATE,")), None)
        if hdr_idx is None:
            raise ValueError("CBOE CSV header not found")
        rows = []
        for line in lines[hdr_idx + 1:]:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 5:
                continue
            try:
                dt = pd.to_datetime(parts[0])
                pc = float(parts[4])
                rows.append({"date": dt, "pc_ratio": pc})
            except Exception:
                continue
        df = pd.DataFrame(rows).sort_values("date").set_index("date")
        df["pc_ratio"] = df["pc_ratio"].rolling(21, min_periods=5).mean()
        df = df.dropna()
        df.to_csv(cache)
        return df["pc_ratio"]
    except Exception as exc:
        print(f"  CBOE put/call fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_multpl_dy(date_slug: str) -> pd.Series:
    """S&P 500 monthly dividend yield from multpl.com.

    Citi BMC uses MSCI AC World DY with thresholds amber ~2.1% / red ~1.3%.
    We use S&P 500 DY as the US proxy (similar long-history dynamics).
    """
    cache = ONEOFF / f"sp500_dividend_yield_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["dy"].sort_index()
    import re
    import html
    url = "https://www.multpl.com/s-p-500-dividend-yield/table/by-month"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S)
        out = []
        for r in rows:
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if len(cells) < 2:
                continue
            try:
                dt = pd.to_datetime(cells[0])
                # Multpl reports DY with a "%" suffix
                dy_raw = re.sub(r"[†%\s  ]", "", cells[1])
                dy = float(dy_raw)
                out.append({"date": dt, "dy": dy})
            except Exception:
                continue
        df = pd.DataFrame(out).sort_values("date")
        df.to_csv(cache, index=False)
        return df.set_index("date")["dy"]
    except Exception as exc:
        print(f"  multpl DY fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_multpl_pe(date_slug: str) -> pd.Series:
    """S&P 500 monthly trailing P/E — multpl.com (fresh through current month)."""
    cache = ONEOFF / f"sp500_trailing_pe_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["pe"].sort_index()
    import re
    import html
    url = "https://www.multpl.com/s-p-500-pe-ratio/table/by-month"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S)
        out = []
        for r in rows:
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if len(cells) < 2:
                continue
            try:
                dt = pd.to_datetime(cells[0])
                pe = float(re.sub(r"[†\s  ]", "", cells[1]))
                out.append({"date": dt, "pe": pe})
            except Exception:
                continue
        df = pd.DataFrame(out).sort_values("date")
        df.to_csv(cache, index=False)
        return df.set_index("date")["pe"]
    except Exception as exc:
        print(f"  multpl P/E fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_shiller_cape(date_slug: str) -> pd.Series:
    """CAPE — multpl.com primary (fresh monthly); Shiller's Yale spreadsheet fallback."""
    cache = ONEOFF / f"shiller_cape_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["cape"].sort_index()
    import re
    import html
    try:
        url = "https://www.multpl.com/shiller-pe/table/by-month"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S)
        out = []
        for r in rows:
            cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if len(cells) < 2:
                continue
            try:
                dt = pd.to_datetime(cells[0])
                cape = float(re.sub(r"[†\s  ]", "", cells[1]))
                out.append({"date": dt, "cape": cape})
            except Exception:
                continue
        if out:
            df = pd.DataFrame(out).sort_values("date")
            df.to_csv(cache, index=False)
            return df.set_index("date")["cape"]
    except Exception as exc:
        print(f"  multpl CAPE failed, falling back to Shiller: {exc}", file=sys.stderr)
    # Fallback: Shiller Yale spreadsheet (stale after 2023-09)
    try:
        url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
        xlb = urllib.request.urlopen(req, timeout=60).read()
        xl = pd.read_excel(io.BytesIO(xlb), sheet_name="Data", header=7, engine="xlrd")
        date_col = xl.columns[0]
        cape_col = next((c for c in xl.columns if "CAPE" in str(c).upper()), None)
        if cape_col is None:
            cape_col = next((c for c in xl.columns if "P/E10" in str(c) or "P_E10" in str(c)), None)
        if cape_col is None:
            raise ValueError("CAPE column not found")
        df = xl[[date_col, cape_col]].dropna()
        df["year"] = df[date_col].astype(float).apply(lambda v: int(v))
        df["month"] = df[date_col].astype(float).apply(
            lambda v: int(round((v - int(v)) * 100))
        )
        df["month"] = df["month"].clip(1, 12)
        df["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
        )
        df["cape"] = pd.to_numeric(df[cape_col], errors="coerce")
        df = df[["date", "cape"]].dropna().sort_values("date")
        df.to_csv(cache, index=False)
        return df.set_index("date")["cape"]
    except Exception as exc:
        print(f"  Shiller fallback also failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_aaii(date_slug: str) -> pd.Series:
    cache = ONEOFF / f"aaii_sentiment_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["spread"].sort_index()
    url = "https://www.aaii.com/files/surveys/sentiment.xls"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
        xlb = urllib.request.urlopen(req, timeout=60).read()
        xl = pd.read_excel(io.BytesIO(xlb), sheet_name=0, header=3, engine="xlrd")
        xl.rename(columns={c: str(c).strip() for c in xl.columns}, inplace=True)
        spread_col = next((c for c in xl.columns if "bull" in str(c).lower() and "bear" in str(c).lower()
                          and ("spread" in str(c).lower() or "-" in str(c))), None)
        if spread_col is None:
            bull_col = next((c for c in xl.columns if "bullish" in str(c).lower()), None)
            bear_col = next((c for c in xl.columns if "bearish" in str(c).lower()), None)
            if not (bull_col and bear_col):
                raise ValueError("Bull/Bear cols not found")
            xl["spread_calc"] = pd.to_numeric(xl[bull_col], errors="coerce") - pd.to_numeric(xl[bear_col], errors="coerce")
            spread_col = "spread_calc"
        date_col = xl.columns[0]
        df = xl[[date_col, spread_col]].copy()
        df.columns = ["date", "spread"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["spread"] = pd.to_numeric(df["spread"], errors="coerce")
        if df["spread"].abs().median() < 1.0:
            df["spread"] *= 100
        df = df.dropna().sort_values("date")
        df.to_csv(cache, index=False)
        return df.set_index("date")["spread"]
    except Exception as exc:
        print(f"  AAII fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def fetch_naaim(date_slug: str) -> pd.Series:
    cache = ONEOFF / f"naaim_exposure_{date_slug}.csv"
    if cache.exists():
        df = pd.read_csv(cache)
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date")["exposure"].sort_index()
    url = "https://www.naaim.org/wp-content/uploads/2014/04/NAAIM-Exposure-Index-Data.xlsx"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
        xlb = urllib.request.urlopen(req, timeout=60).read()
        xl = pd.read_excel(io.BytesIO(xlb), sheet_name=0, engine="openpyxl")
        xl.rename(columns={c: str(c).strip() for c in xl.columns}, inplace=True)
        date_col = xl.columns[0]
        exp_col = next((c for c in xl.columns if "naaim" in str(c).lower() and "mean" in str(c).lower()), None)
        if exp_col is None:
            exp_col = next((c for c in xl.columns if "mean" in str(c).lower() or "exposure" in str(c).lower()), None)
        if exp_col is None:
            raise ValueError("NAAIM exposure column not found")
        df = xl[[date_col, exp_col]].copy()
        df.columns = ["date", "exposure"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["exposure"] = pd.to_numeric(df["exposure"], errors="coerce")
        df = df.dropna().sort_values("date")
        df.to_csv(cache, index=False)
        return df.set_index("date")["exposure"]
    except Exception as exc:
        print(f"  NAAIM fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float)


def compute_erp(date_slug: str, start: str, end: str) -> pd.Series:
    """ERP = S&P 500 trailing earnings yield − 10Y Treasury yield."""
    pe = fetch_multpl_pe(date_slug)
    if pe.empty:
        print("  ! multpl PE empty; ERP cannot be computed", file=sys.stderr)
        return pd.Series(dtype=float)
    ey = (100.0 / pe).rename("ey").resample("MS").last().ffill()

    tnx = fetch_yf("^TNX", start=start, end=end)
    if tnx.empty:
        tnx_fred = fetch_fred("DGS10", start=start)
        if tnx_fred.empty:
            return pd.Series(dtype=float)
        tnx_monthly = tnx_fred.resample("MS").mean()
    else:
        if tnx.median() > 10:
            tnx = tnx / 10.0
        tnx_monthly = tnx.resample("MS").mean()

    merged = pd.concat([ey, tnx_monthly.rename("tnx")], axis=1).dropna()
    merged["erp"] = merged["ey"] - merged["tnx"]
    return merged["erp"].dropna()


def fetch_indicator(ind: dict, date_slug: str, start_25y: str, end: str) -> pd.Series:
    src = ind["source"]
    print(f"  fetching {ind['name']} ({src})...", flush=True)
    if src == "fred":
        return fetch_fred(ind["code"], start_25y)
    if src == "yf":
        return fetch_yf(ind["code"], start_25y, end)
    if src in ("ratio", "ratio_etf"):
        a, b = ind["code"]
        sa = fetch_yf(a, start_25y, end)
        sb = fetch_yf(b, start_25y, end)
        if sa.empty or sb.empty:
            return pd.Series(dtype=float)
        df = pd.concat([sa.rename("a"), sb.rename("b")], axis=1).dropna()
        return (df["a"] / df["b"]).rename(ind["id"])
    if src == "derived_erp":
        return compute_erp(date_slug, start_25y, end)
    if src == "derived_ccc_hy":
        # CCC OAS - HY OAS spread; computed from the two FRED series.
        ccc = fetch_fred("BAMLH0A3HYC", start_25y)
        hy = fetch_fred("BAMLH0A0HYM2", start_25y)
        if ccc.empty or hy.empty:
            return pd.Series(dtype=float)
        df = pd.concat([ccc.rename("ccc"), hy.rename("hy")], axis=1).dropna()
        return (df["ccc"] - df["hy"]).rename("ccc_hy_spread")
    if src == "cape":
        return fetch_shiller_cape(date_slug)
    if src == "spx_dy":
        return fetch_multpl_dy(date_slug)
    if src == "eps_peak":
        return fetch_multpl_eps_peak(date_slug)
    if src == "margin_debt":
        return fetch_finra_margin(date_slug)
    if src == "capex_yoy":
        return fetch_capex_yoy(date_slug, start_25y)
    if src == "put_call":
        return fetch_cboe_putcall(date_slug)
    if src == "aaii":
        return fetch_aaii(date_slug)
    if src == "naaim":
        return fetch_naaim(date_slug)
    return pd.Series(dtype=float)


# Citi-BMC-style flag thresholds. amber when an indicator clears 60% complacent,
# red when it clears 80% (i.e. in the top quintile of its rolling 10y window).
# Total "flag count" = (# red × 1.0) + (# amber × 0.5). Easier to interpret
# than the continuous composite; cite alongside it.
FLAG_AMBER_THR = 60.0
FLAG_RED_THR = 80.0


def flag_status(complacency_pct: float) -> str:
    if pd.isna(complacency_pct):
        return "n/a"
    if complacency_pct >= FLAG_RED_THR:
        return "red"
    if complacency_pct >= FLAG_AMBER_THR:
        return "amber"
    return "off"


def flag_count(table: pd.DataFrame) -> dict:
    """Total flags (Citi-BMC style) + per-tier breakdown."""
    active = table[table["active"]].copy()
    active["flag"] = active["complacency_pct"].apply(flag_status)
    n_red = int((active["flag"] == "red").sum())
    n_amber = int((active["flag"] == "amber").sum())
    n_off = int((active["flag"] == "off").sum())
    n_total = int(len(active))
    return {
        "flag_count": round(n_red * 1.0 + n_amber * 0.5, 1),
        "max_possible": n_total,
        "n_red": n_red,
        "n_amber": n_amber,
        "n_off": n_off,
    }


# ── Helpers ─────────────────────────────────────────────────────────────────

def decile_label(pct: float) -> str:
    if pd.isna(pct):
        return "n/a"
    d = int(min(pct / 10, 9.999))
    if d == 0:
        return "10th (least complacent)"
    if d == 9:
        return "1st (most complacent)"
    return f"{10 - d}th decile"


def tier_for_score(score: float) -> str:
    if score < 20: return "Panicked"
    if score < 40: return "Cautious"
    if score < 60: return "Neutral"
    if score < 80: return "Elevated"
    return "Stretched"


# ── Main ────────────────────────────────────────────────────────────────────

def build(as_of: str, window_years: int = 10) -> dict:
    """Compute today's dashboard and write all artifacts. Returns a summary dict."""
    cutoff = pd.Timestamp(as_of)
    end_str = (cutoff + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    ten_y_ago = cutoff - pd.DateOffset(years=window_years)
    start_25y = (cutoff - pd.DateOffset(years=25)).strftime("%Y-%m-%d")

    print(f"=== Market Complacency Dashboard {as_of} (window={window_years}y) ===")

    # 1. Fetch
    series: dict[str, pd.Series] = {}
    for ind in INDICATORS:
        s = fetch_indicator(ind, as_of, start_25y, end_str)
        # Strip tz on indices to enable clean joins
        if not s.empty and hasattr(s.index, "tz") and s.index.tz is not None:
            s.index = s.index.tz_localize(None)
        series[ind["id"]] = s
        if s.empty:
            print(f"  ! {ind['name']} returned empty")
        else:
            print(f"  ✓ {ind['name']}: {len(s)} obs, last={s.iloc[-1]:.3f} on {s.index[-1].date()}")

    # 2. Per-indicator table
    rows = []
    for ind in INDICATORS:
        s = series[ind["id"]]
        if s.empty:
            if ind["required"]:
                raise RuntimeError(f"Required indicator {ind['name']} missing — abort")
            rows.append({
                "id": ind["id"], "name": ind["name"], "category": ind["category"],
                "weight": ind["weight"], "current": None, "as_of": None,
                "min_10y": None, "median_10y": None, "max_10y": None,
                "raw_pct_10y": None, "complacency_pct": None,
                "decile": "n/a", "stretched": False, "direction": ind["direction"],
                "active": False, "unit": ind["unit"],
            })
            continue
        s = s[s.index <= cutoff]
        s_win = s[s.index >= ten_y_ago]
        if len(s_win) < 30:
            if ind["required"]:
                raise RuntimeError(f"Required indicator {ind['name']} has <30 obs in {window_years}y window")
            rows.append({
                "id": ind["id"], "name": ind["name"], "category": ind["category"],
                "weight": ind["weight"], "current": None, "as_of": None,
                "min_10y": None, "median_10y": None, "max_10y": None,
                "raw_pct_10y": None, "complacency_pct": None,
                "decile": "n/a", "stretched": False, "direction": ind["direction"],
                "active": False, "unit": ind["unit"],
            })
            continue
        current = float(s_win.iloc[-1])
        as_of_obs = s_win.index[-1].strftime("%Y-%m-%d")
        raw_pct = (s_win < current).sum() / len(s_win) * 100.0
        comp_pct = 100.0 - raw_pct if ind["direction"] == "low" else raw_pct
        rows.append({
            "id": ind["id"], "name": ind["name"], "category": ind["category"],
            "weight": ind["weight"], "current": current, "as_of": as_of_obs,
            "min_10y": float(s_win.min()), "median_10y": float(s_win.median()),
            "max_10y": float(s_win.max()),
            "raw_pct_10y": raw_pct, "complacency_pct": comp_pct,
            "decile": decile_label(comp_pct),
            "stretched": comp_pct >= 90,
            "direction": ind["direction"], "active": True, "unit": ind["unit"],
        })

    table = pd.DataFrame(rows)
    active = table[table["active"]].copy()
    active["weight_norm"] = active["weight"] / active["weight"].sum()
    composite = float((active["complacency_pct"] * active["weight_norm"]).sum())
    tier = tier_for_score(composite)
    print(f"\n→ Composite: {composite:.1f} / 100 ({tier})")
    print(f"  Active indicators: {len(active)} of {len(INDICATORS)}")

    # 3. Historical composite series (for charting + precedents)
    print("\n  Building historical composite series...")
    start_hist = pd.Timestamp("2000-01-01")
    bday_index = pd.bdate_range(start_hist, cutoff)
    aligned = {}
    for ind in INDICATORS:
        s = series[ind["id"]]
        if s.empty:
            continue
        s = s[~s.index.duplicated(keep="last")].sort_index()
        s = s.reindex(bday_index, method="ffill")
        aligned[ind["id"]] = s
    aligned_df = pd.DataFrame(aligned)

    window_bdays = 252 * window_years
    pct_history = pd.DataFrame(index=bday_index)
    for ind in INDICATORS:
        if ind["id"] not in aligned_df.columns:
            continue
        s = aligned_df[ind["id"]]
        rolling_rank = s.rolling(window_bdays, min_periods=252).rank(pct=True) * 100.0
        if ind["direction"] == "low":
            pct_history[ind["id"]] = 100.0 - rolling_rank
        else:
            pct_history[ind["id"]] = rolling_rank

    weights_map = {ind["id"]: ind["weight"] for ind in INDICATORS}
    def _weighted_avg(row):
        avail = row.dropna()
        if avail.empty:
            return np.nan
        ws = pd.Series({k: weights_map[k] for k in avail.index})
        ws = ws / ws.sum()
        return float((avail * ws).sum())
    composite_hist = pct_history.apply(_weighted_avg, axis=1).dropna()
    composite_hist.name = "composite"
    composite_hist.to_frame().to_csv(ONEOFF / f"market_complacency_{as_of}_composite_history.csv")
    print(f"  Composite history: {len(composite_hist)} obs from {composite_hist.index[0].date()} to {composite_hist.index[-1].date()}")

    # 4. Precedents within ±5
    print(f"\n  Finding precedents within ±5 of {composite:.1f}...")
    band_lo, band_hi = composite - 5, composite + 5
    in_band = composite_hist[(composite_hist >= band_lo) & (composite_hist <= band_hi)]
    in_band = in_band[in_band.index < cutoff]
    precedents_dates: list[pd.Timestamp] = []
    last = None
    for dt in in_band.index:
        if last is None or (dt - last).days >= 180:
            precedents_dates.append(dt)
            last = dt
    if len(precedents_dates) > 8:
        idx = np.linspace(0, len(precedents_dates) - 1, 8).astype(int)
        precedents_dates = [precedents_dates[i] for i in idx]

    spy = fetch_yf("SPY", start="2000-01-01", end=end_str)
    spy = spy[~spy.index.duplicated(keep="last")].sort_index()

    precedent_rows = []
    for dt in precedents_dates:
        score_at = float(composite_hist.loc[dt])
        try:
            entry_px = float(spy.loc[spy.index >= dt].iloc[0])
        except (KeyError, IndexError):
            continue
        forward = {}
        for months in (6, 12, 24):
            target = dt + pd.Timedelta(days=int(months * 30.4))
            future = spy[spy.index >= target]
            if len(future) > 0:
                fwd_px = float(future.iloc[0])
                forward[f"ret_{months}m"] = (fwd_px / entry_px - 1) * 100
                window_px = spy[(spy.index >= dt) & (spy.index <= target)]
                if len(window_px) > 0:
                    forward[f"maxdd_{months}m"] = float((window_px / window_px.cummax() - 1).min() * 100)
                else:
                    forward[f"maxdd_{months}m"] = None
            else:
                forward[f"ret_{months}m"] = None
                forward[f"maxdd_{months}m"] = None
        precedent_rows.append({"date": dt.strftime("%Y-%m-%d"), "composite": round(score_at, 1), **forward})
    prec_df = pd.DataFrame(precedent_rows)
    prec_df.to_csv(ONEOFF / f"market_complacency_{as_of}_precedents.csv", index=False)
    print(f"  {len(prec_df)} precedents:")
    if not prec_df.empty:
        print(prec_df.to_string(index=False))

    # 5. Indicator table CSV (+ Citi-BMC-style flag column)
    flags = flag_count(table)
    out_table = table.copy()
    for col in ("current", "min_10y", "median_10y", "max_10y", "raw_pct_10y", "complacency_pct"):
        out_table[col] = pd.to_numeric(out_table[col], errors="coerce").round(3)
    out_table["flag"] = out_table["complacency_pct"].apply(flag_status)
    out_table["composite_score"] = round(composite, 2)
    out_table["composite_tier"] = tier
    out_table["flag_count"] = flags["flag_count"]
    out_table["flag_max"] = flags["max_possible"]
    out_table.to_csv(ONEOFF / f"market_complacency_{as_of}_indicators.csv", index=False)
    print(f"\n  Flag count (Citi-BMC style): {flags['flag_count']} / {flags['max_possible']}")
    print(f"    Red flags (>= {FLAG_RED_THR}% complacent): {flags['n_red']}")
    print(f"    Amber flags ({FLAG_AMBER_THR}-{FLAG_RED_THR}%):    {flags['n_amber']}")
    print(f"    Off:                              {flags['n_off']}")

    # 6. Charts
    print("\n  Generating charts...")
    _make_charts(as_of, composite, tier, composite_hist, series, table, prec_df, window_years)

    return {
        "as_of": as_of,
        "window_years": window_years,
        "composite": round(composite, 2),
        "tier": tier,
        "flag_count": flags["flag_count"],
        "flag_max": flags["max_possible"],
        "flag_red": flags["n_red"],
        "flag_amber": flags["n_amber"],
        "active_indicators": int(active.shape[0]),
        "total_indicators": len(INDICATORS),
        "weights_renormalized": float(active["weight"].sum()) < 0.99,
        "indicator_table_csv": str(ONEOFF / f"market_complacency_{as_of}_indicators.csv"),
        "precedents_csv": str(ONEOFF / f"market_complacency_{as_of}_precedents.csv"),
        "composite_history_csv": str(ONEOFF / f"market_complacency_{as_of}_composite_history.csv"),
        "charts_dir": str(CHARTS),
        "report_path_hint": str(REPORT_DIR / f"market_complacency_{as_of}.md"),
    }


def _make_charts(as_of, composite, tier, composite_hist, series, table, prec_df, window_years):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    win_start = pd.Timestamp(as_of) - pd.DateOffset(years=window_years)

    # Chart 1: Composite
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(composite_hist.index, composite_hist.values, lw=1.0, color="#1f4e79")
    ax.axhspan(0, 20, alpha=0.15, color="#7eb541", label="Panicked")
    ax.axhspan(20, 40, alpha=0.10, color="#b9dd83")
    ax.axhspan(40, 60, alpha=0.06, color="#e6e6e6")
    ax.axhspan(60, 80, alpha=0.15, color="#f4a261")
    ax.axhspan(80, 100, alpha=0.20, color="#e63946", label="Stretched")
    ax.scatter([composite_hist.index[-1]], [composite], color="black", zorder=5, s=60)
    ax.annotate(f"Today: {composite:.1f}\n({tier})",
                xy=(composite_hist.index[-1], composite),
                xytext=(-100, -40), textcoords="offset points",
                fontsize=10, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_xlim(pd.Timestamp("2001-01-01"), pd.Timestamp(as_of) + pd.Timedelta(days=30))
    ax.set_ylim(0, 100)
    ax.set_ylabel("Composite (0–100)")
    ax.set_title(f"Market Complacency Composite, 2001–{as_of[:4]}")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.tight_layout()
    plt.savefig(CHARTS / f"market_complacency_{as_of}_composite.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Chart 2: HY OAS
    if not series["hy_oas"].empty:
        hy = series["hy_oas"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(hy.index, hy.values, lw=1.0, color="#c1272d")
        hy_win = hy[hy.index >= win_start]
        for pct, lbl in [(5, "5th"), (50, "median"), (95, "95th")]:
            v = np.percentile(hy_win.dropna(), pct)
            ax.axhline(v, ls="--", alpha=0.4, color="gray")
            ax.text(hy.index[-1], v, f" {lbl} {v:.2f}", fontsize=8, va="center")
        cur = float(hy_win.iloc[-1])
        ax.scatter([hy.index[-1]], [cur], color="black", s=60, zorder=5,
                   label=f"Today {cur:.2f}%")
        ax.legend(loc="upper right")
        ax.set_ylabel("HY OAS (%)")
        ax.set_title(f"ICE BofA US HY OAS, 2001–{as_of[:4]} (5/50/95 = last-{window_years}y percentiles)")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_hy_oas.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 3: IG + CCC
    if not series["ig_oas"].empty and not series["ccc_oas"].empty:
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(series["ig_oas"].index, series["ig_oas"].values, lw=1.0, color="#2a9d8f", label="IG OAS")
        ax2 = ax.twinx()
        ax2.plot(series["ccc_oas"].index, series["ccc_oas"].values, lw=1.0, color="#e76f51", label="CCC OAS")
        ax.set_ylabel("IG OAS (%)", color="#2a9d8f")
        ax2.set_ylabel("CCC OAS (%)", color="#e76f51")
        ax.set_title(f"IG vs CCC OAS, 2001–{as_of[:4]} (credit-tier divergence)")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper left"); ax2.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_ig_ccc.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 4: VIX + VVIX overlay (window)
    if not series["vix"].empty and not series["vvix"].empty:
        vix_win = series["vix"][series["vix"].index >= win_start]
        vvix_win = series["vvix"][series["vvix"].index >= win_start]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(vix_win.index, vix_win.values, lw=0.9, color="#1d3557", label="VIX")
        ax2 = ax.twinx()
        ax2.plot(vvix_win.index, vvix_win.values, lw=0.9, color="#e63946", label="VVIX", alpha=0.7)
        ax.set_ylabel("VIX", color="#1d3557")
        ax2.set_ylabel("VVIX", color="#e63946")
        ax.set_title(f"VIX & VVIX, last {window_years} years")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper left"); ax2.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_vix_vvix.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 5: VIX term slope (window)
    if not series["vix_slope"].empty:
        slope_win = series["vix_slope"][series["vix_slope"].index >= win_start]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(slope_win.index, slope_win.values, lw=0.7, color="#264653")
        ax.axhline(1.0, ls="--", color="black", alpha=0.5, label="Contango/Backwardation")
        ax.axhspan(0, 0.85, alpha=0.10, color="#7eb541", label="Deep contango (calm)")
        ax.axhspan(1.0, max(2.0, slope_win.max() * 1.05), alpha=0.10, color="#e63946", label="Backwardation (stress)")
        ax.set_ylabel("VIX9D / VIX3M")
        ax.set_title(f"VIX Term Slope (VIX9D ÷ VIX3M), last {window_years} years")
        ax.grid(alpha=0.3); ax.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_vix_slope.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 6: MOVE (window)
    if not series["move"].empty:
        move_win = series["move"][series["move"].index >= win_start]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(move_win.index, move_win.values, lw=0.9, color="#6a4c93")
        ax.axhline(80, ls="--", color="green", alpha=0.5, label="80 (calm)")
        ax.axhline(120, ls="--", color="red", alpha=0.5, label="120 (stress)")
        ax.set_ylabel("MOVE Index")
        ax.set_title(f"MOVE Index, last {window_years} years")
        ax.grid(alpha=0.3); ax.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_move.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 7: ERP (25y)
    if not series["erp"].empty:
        erp_25y = series["erp"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(erp_25y.index, erp_25y.values, lw=1.0, color="#003049")
        ax.axhline(0, color="black", alpha=0.3)
        ax.fill_between(erp_25y.index, 0, erp_25y.values,
                        where=(erp_25y.values < 0), alpha=0.3, color="#d62828", label="Negative ERP")
        ax.set_ylabel("Equity Risk Premium (pp)")
        ax.set_title(f"Equity Risk Premium (S&P 500 E/P − 10Y), 2001–{as_of[:4]}")
        ax.grid(alpha=0.3); ax.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_erp.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 8: Per-indicator bar
    fig, ax = plt.subplots(figsize=(11, 6))
    actv = table[table["active"]].sort_values("complacency_pct", ascending=True)
    colors = []
    for p in actv["complacency_pct"]:
        if p >= 80: colors.append("#e63946")
        elif p >= 60: colors.append("#f4a261")
        elif p >= 40: colors.append("#e9c46a")
        elif p >= 20: colors.append("#a8dadc")
        else: colors.append("#457b9d")
    ax.barh(actv["name"], actv["complacency_pct"], color=colors)
    for i, (_, r) in enumerate(actv.iterrows()):
        ax.text(r["complacency_pct"] + 1, i, f" {r['complacency_pct']:.0f}",
                va="center", fontsize=9)
    ax.axvline(50, color="black", alpha=0.3, ls="--")
    ax.axvline(composite, color="#1f4e79", lw=2, label=f"Composite {composite:.1f}")
    ax.set_xlim(0, 105)
    ax.set_xlabel(f"Complacency percentile ({window_years}y rolling) — higher = more complacent")
    ax.set_title(f"Per-Indicator Complacency, today vs last {window_years} years")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(CHARTS / f"market_complacency_{as_of}_indicators_bar.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Chart 9: Precedents scatter
    if not prec_df.empty and "ret_12m" in prec_df.columns and prec_df["ret_12m"].notna().any():
        fig, ax = plt.subplots(figsize=(11, 5))
        sub = prec_df.dropna(subset=["ret_12m"])
        ax.scatter(sub["composite"], sub["ret_12m"], s=80, alpha=0.7, color="#1d3557")
        for _, r in sub.iterrows():
            ax.annotate(r["date"][:7],
                        xy=(r["composite"], r["ret_12m"]),
                        xytext=(5, 5), textcoords="offset points", fontsize=8)
        ax.axhline(0, color="black", alpha=0.3)
        ax.set_xlabel("Composite at precedent date")
        ax.set_ylabel("SPY 12-month forward return (%)")
        ax.set_title(f"Precedents within ±5 of today's composite ({composite:.1f}) — 12m forward SPY")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_precedents.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 10: CAPE
    if not series["cape"].empty:
        cape_25y = series["cape"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(cape_25y.index, cape_25y.values, lw=1.0, color="#6d597a")
        ax.axhline(30, ls="--", color="red", alpha=0.5, label="CAPE 30 (historically rich)")
        ax.set_ylabel("Shiller CAPE")
        ax.set_title(f"Shiller CAPE, 2001–{as_of[:4]}")
        ax.grid(alpha=0.3); ax.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_cape.png", dpi=150, bbox_inches="tight")
        plt.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=_dt.date.today().isoformat(),
                        help="As-of date YYYY-MM-DD (default: today)")
    parser.add_argument("--window-years", type=int, default=10,
                        help="Trailing percentile window in years (default: 10)")
    args = parser.parse_args()

    summary = build(args.date, window_years=args.window_years)
    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
