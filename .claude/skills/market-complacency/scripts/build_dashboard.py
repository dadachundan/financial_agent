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
    # CBOE Equity Put/Call Ratio REMOVED in v8 — the public CSV stopped
    # updating Oct 2019, so it cannot inform current readings. Keeping it in
    # the catalog only polluted the flag-count denominator with a row that
    # was permanently "off" (stale value < 60th percentile by construction).
    # Restore only when a non-paywalled live feed is identified.
    # NEW v6 (added 2026-06-07, after user asked "can't you use WebSearch?"):
    # IPO activity — annual US IPO proceeds from Renaissance Capital,
    # 2017-present. Cached as oneoff/ipo_proceeds_annual.csv (manually
    # updated when Renaissance refreshes). Normalized by S&P 500 cap-weighted
    # mkt cap proxy. Citi BMC thresholds: amber ~0.4%, red ~0.7%.
    # 2021 peak ($142B) was the bubble-era extreme; 2022 ($7.7B) the trough.
    # Direction "high" — strong IPO issuance = late-cycle exuberance.
    {"id": "ipo_pct", "name": "IPO Proceeds / Mkt Cap", "source": "ipo_pct", "code": None, "direction": "high", "weight": 0.04, "required": False, "unit": "%", "category": "Corporate Behaviour"},
    # M&A activity — annual global M&A volume from Bain/PitchBook reports
    # 2000-present. US ~50% of global. Normalized by S&P 500 cap-weighted
    # mkt cap proxy. Citi BMC thresholds: amber ~8%, red ~11%.
    # 2021 peak ($5.9T global, ~$3T US) was the extreme; 2022-23 was suppressed.
    # Direction "high" — high M&A = late-cycle deal exuberance.
    {"id": "ma_pct", "name": "M&A Volume / Mkt Cap", "source": "ma_pct", "code": None, "direction": "high", "weight": 0.04, "required": False, "unit": "%", "category": "Corporate Behaviour"},
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


def fetch_ipo_pct(date_slug: str) -> pd.Series:
    """Annual US IPO proceeds as % of S&P 500 market cap proxy.

    Reads oneoff/ipo_proceeds_annual.csv (manually-maintained, refreshed
    from Renaissance Capital periodically via WebSearch). Normalises by
    the S&P 500 year-end level — since shares outstanding is roughly stable
    over the medium term, level is a workable mkt-cap proxy for percentile
    ranking.
    """
    cache = Path(__file__).resolve().parent.parent / "data" / "ipo_proceeds_annual.csv"
    if not cache.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(cache)
    # Use Dec 31 of each year as the date
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-12-31")
    spx = fetch_yf("^GSPC", start="2000-01-01", end="2026-06-08")
    if spx.empty:
        return pd.Series(dtype=float)
    spx_yearend = spx.resample("YE").last()
    spx_yearend.index = spx_yearend.index.normalize()
    merged = pd.merge_asof(df.sort_values("date"),
                            spx_yearend.rename("spx").reset_index().rename(columns={"Date":"date"}),
                            on="date", direction="nearest")
    # ipo_pct = proceeds ($B) / SPX level — scale-free percentile rank
    merged["ipo_pct"] = merged["proceeds_usd_billion"] / merged["spx"]
    annual = merged.dropna(subset=["ipo_pct"]).set_index("date")["ipo_pct"]
    # Upsample to monthly via forward-fill — the percentile rank logic needs
    # ≥30 obs in the trailing 10y window; annual data alone has only ~10.
    monthly = annual.resample("MS").ffill()
    return monthly


def fetch_ma_pct(date_slug: str) -> pd.Series:
    """Annual US M&A volume as % of S&P 500 market cap proxy.

    Reads oneoff/ma_volume_annual.csv (manually-maintained). US share
    is ~45-50% of global volume historically. Normalises by S&P 500 level.
    """
    cache = Path(__file__).resolve().parent.parent / "data" / "ma_volume_annual.csv"
    if not cache.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(cache)
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-12-31")
    # US M&A in $T = global volume × US share %
    df["us_ma_trn"] = df["global_volume_usd_trillion"] * df["us_share_pct"] / 100
    spx = fetch_yf("^GSPC", start="2000-01-01", end="2026-06-08")
    if spx.empty:
        return pd.Series(dtype=float)
    spx_yearend = spx.resample("YE").last()
    spx_yearend.index = spx_yearend.index.normalize()
    merged = pd.merge_asof(df.sort_values("date"),
                            spx_yearend.rename("spx").reset_index().rename(columns={"Date":"date"}),
                            on="date", direction="nearest")
    # ma_pct = US M&A ($T × 1000 → $B) / SPX level — scale-free percentile rank
    merged["ma_pct"] = (merged["us_ma_trn"] * 1000) / merged["spx"]
    annual = merged.dropna(subset=["ma_pct"]).set_index("date")["ma_pct"]
    monthly = annual.resample("MS").ffill()
    return monthly


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
    if src == "ipo_pct":
        return fetch_ipo_pct(date_slug)
    if src == "ma_pct":
        return fetch_ma_pct(date_slug)
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

    # ── Historical flag count (Citi-BMC style) ────────────────────────────
    # For each date, count indicators in red (>=80) and amber (60-80) buckets,
    # flag_count = n_red × 1.0 + n_amber × 0.5
    def _flag_count_row(row):
        avail = row.dropna()
        if avail.empty:
            return np.nan
        n_red = int((avail >= FLAG_RED_THR).sum())
        n_amber = int(((avail >= FLAG_AMBER_THR) & (avail < FLAG_RED_THR)).sum())
        return n_red * 1.0 + n_amber * 0.5

    flag_count_hist = pct_history.apply(_flag_count_row, axis=1).dropna()
    flag_count_hist.name = "flag_count"
    flag_count_hist.to_frame().to_csv(ONEOFF / f"market_complacency_{as_of}_flag_count_history.csv")
    print(f"  Flag-count history: {len(flag_count_hist)} obs, current {flag_count_hist.iloc[-1]:.1f}, all-time max {flag_count_hist.max():.1f} on {flag_count_hist.idxmax().date()}")

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
    # Flag-count + SPY overlay (Figure 1) REMOVED in v9 — user rejected as
    # "inaccurate" (annotation positions drifted from data; "Now" arrow off
    # the actual data point; reference-line labels collided at the bottom).
    # Function definition kept further down for archival; the call is gone.
    # _make_flag_count_html(as_of, flag_count_hist)

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


def _make_flag_count_html(as_of: str, flag_count_hist: pd.Series) -> None:
    """Citi BMC Figure 1 equivalent: flag count over time overlaid on SPY price.

    Dual-axis: SPY price (left, blue), flag count (right, red). Annotated at
    Mar 2000, Oct 2007, Feb 2020, Dec 2021, and Now. Rangeselector buttons
    for 1Y / YTD / 5Y / 10Y / ALL.
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        print("  plotly not available — skipping flag count chart", file=sys.stderr)
        return

    # Pull SPY back to the start of the flag-count history
    spy_start = (flag_count_hist.index[0] - pd.Timedelta(days=30)).strftime("%Y-%m-%d")
    spy = fetch_yf("SPY", start=spy_start, end=(pd.Timestamp(as_of) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    if spy.empty:
        print("  SPY fetch empty — skipping flag count chart", file=sys.stderr)
        return
    # Align to flag-count dates via reindex + ffill
    spy = spy.reindex(flag_count_hist.index, method="nearest")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Flag count (red) — right axis
    fig.add_trace(go.Scatter(
        x=flag_count_hist.index, y=flag_count_hist.values,
        mode="lines", name="Dashboard flag count (right)",
        line=dict(color="#c1272d", width=1.2),
        hovertemplate="%{x|%Y-%m-%d}<br>Flags: %{y:.1f}<extra></extra>",
    ), secondary_y=True)

    # SPY (blue) — left axis
    fig.add_trace(go.Scatter(
        x=spy.index, y=spy.values,
        mode="lines", name="SPY price (left)",
        line=dict(color="#1f4e79", width=1.4),
        hovertemplate="%{x|%Y-%m-%d}<br>SPY: $%{y:.2f}<extra></extra>",
    ), secondary_y=False)

    # Annotations at the key historical reference dates
    today = flag_count_hist.index[-1]
    today_flag = float(flag_count_hist.iloc[-1])
    annotations = []
    for label, dt_str in [("March 2000", "2000-03-31"), ("October 2007", "2007-10-31"),
                           ("Feb 2020", "2020-02-19"), ("Dec 2021", "2021-12-31")]:
        dt = pd.Timestamp(dt_str)
        avail = flag_count_hist[flag_count_hist.index <= dt]
        if avail.empty:
            continue
        v = float(avail.iloc[-1])
        annotations.append(dict(
            x=avail.index[-1], y=v, yref="y2",
            text=label, showarrow=True, arrowhead=2, ax=0, ay=-30,
            font=dict(size=10, color="#c1272d"),
        ))
    # "Now" marker
    annotations.append(dict(
        x=today, y=today_flag, yref="y2",
        text=f"<b>Now: {today_flag:.1f}</b>", showarrow=True, arrowhead=2,
        ax=-30, ay=-25,
        font=dict(size=11, color="#c1272d"),
    ))

    last = flag_count_hist.index[-1]; first = flag_count_hist.index[0]
    year_start = pd.Timestamp(f"{last.year}-01-01")
    range_buttons = [
        dict(label="1Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=1)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="YTD", method="relayout",
             args=[{"xaxis.range": [year_start.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="5Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=5)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="10Y", method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=10)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="ALL", method="relayout",
             args=[{"xaxis.range": [first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
    ]

    # Reference lines for Citi's published references
    fig.add_hline(y=10, line=dict(color="#c1272d", width=1, dash="dash"),
                  annotation_text="Double-digits (Citi: acceleration zone)",
                  annotation_position="top right",
                  annotation_font=dict(size=10, color="#c1272d"),
                  secondary_y=True)
    fig.add_hline(y=17.5, line=dict(color="#c1272d", width=1, dash="dot"),
                  annotation_text="Mar-00 Citi peak (17.5/18)",
                  annotation_position="top right",
                  annotation_font=dict(size=9, color="#c1272d"),
                  secondary_y=True)

    fig.update_layout(
        title="Figure 1. Dashboard Flag Count and SPY — Citi BMC style",
        yaxis=dict(title="SPY price ($)", side="left"),
        yaxis2=dict(title="Flag count (0–21)", side="right",
                    range=[0, max(21, flag_count_hist.max() * 1.05)], showgrid=False),
        xaxis=dict(
            title="",
            range=[first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")],
            rangeslider=dict(visible=True, thickness=0.05),
            type="date",
        ),
        annotations=annotations,
        updatemenus=[dict(
            type="buttons", direction="right",
            buttons=range_buttons,
            x=0.0, y=1.12, xanchor="left", yanchor="top",
            pad=dict(r=4, t=4),
            font=dict(size=11),
            bgcolor="#f4f4f4",
        )],
        margin=dict(l=50, r=50, t=80, b=40),
        plot_bgcolor="white",
        hovermode="x unified",
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )

    out = CHARTS / f"market_complacency_{as_of}_flag_count.html"
    fig.write_html(str(out), include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "displaylogo": False})
    print(f"  ✓ flag count chart saved: {out.name}", flush=True)


def _make_interactive_chart(
    as_of: str, slug: str, title: str, yaxis: str,
    lines: list,           # list of dict(name=..., series=..., color=..., dash=None)
    thresholds: list = None,  # list of dict(y=..., label=..., color=..., dash="dash")
    secondary_lines: list = None,  # right-axis series, same shape as lines
    secondary_yaxis: str = "",
    bear_periods: list = None,
    height: int = 460,
) -> None:
    """Generic interactive Plotly chart factory.

    - Plots one or more lines on a date x-axis
    - Optional secondary y-axis for differently-scaled overlays
    - Bear-market grey vertical shading
    - Threshold horizontal lines
    - Rangeselector buttons: 1Y / YTD / 5Y / 10Y / ALL (relayout — bypasses
      Plotly's buggy stepmode='todate')
    - Bottom range-slider for fine zoom
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        return

    if secondary_lines:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    else:
        fig = go.Figure()

    # Determine date span across all lines
    all_dates = []
    for ln in lines + (secondary_lines or []):
        if not ln["series"].empty:
            all_dates.append(ln["series"].index)
    if not all_dates:
        return
    first = min(d.min() for d in all_dates)
    last = max(d.max() for d in all_dates)

    # Bear-market shading via shapes
    shapes = []
    bp = bear_periods or [
        ("1990-07-16", "1990-10-11"),
        ("2000-03-24", "2002-10-09"),
        ("2007-10-09", "2009-03-09"),
        ("2020-02-19", "2020-03-23"),
        ("2022-01-03", "2022-10-12"),
    ]
    for start, end in bp:
        s = pd.Timestamp(start); e = pd.Timestamp(end)
        if e < first or s > last:
            continue
        shapes.append(dict(type="rect", xref="x", yref="paper",
                           x0=s, x1=e, y0=0, y1=1,
                           fillcolor="#888888", opacity=0.18,
                           line=dict(width=0), layer="below"))

    # Plot primary axis lines
    for ln in lines:
        if ln["series"].empty:
            continue
        s = ln["series"]
        kwargs = dict(
            x=s.index, y=s.values, mode="lines",
            name=ln["name"],
            line=dict(color=ln.get("color", "#1f4e79"),
                      width=ln.get("width", 1.2),
                      dash=ln.get("dash") or "solid"),
            hovertemplate=f"{ln['name']}: %{{y:.2f}}<br>%{{x|%Y-%m-%d}}<extra></extra>",
        )
        if secondary_lines:
            fig.add_trace(go.Scatter(**kwargs), secondary_y=False)
        else:
            fig.add_trace(go.Scatter(**kwargs))

    # Secondary axis lines
    for ln in (secondary_lines or []):
        if ln["series"].empty:
            continue
        s = ln["series"]
        fig.add_trace(go.Scatter(
            x=s.index, y=s.values, mode="lines",
            name=ln["name"],
            line=dict(color=ln.get("color", "#888"),
                      width=ln.get("width", 1.0),
                      dash=ln.get("dash") or "solid"),
            hovertemplate=f"{ln['name']}: %{{y:.2f}}<br>%{{x|%Y-%m-%d}}<extra></extra>",
        ), secondary_y=True)

    # Threshold lines via hlines + annotations
    for thr in (thresholds or []):
        fig.add_hline(y=thr["y"], line=dict(color=thr.get("color", "#888"),
                                            width=1, dash=thr.get("dash", "dash")),
                      annotation_text=thr.get("label", ""),
                      annotation_position="top right",
                      annotation_font=dict(size=10, color=thr.get("color", "#888")))

    year_start = pd.Timestamp(f"{last.year}-01-01")
    range_buttons = [
        dict(label="1Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=1)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="YTD", method="relayout",
             args=[{"xaxis.range": [year_start.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="5Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=5)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="10Y", method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=10)).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
        dict(label="ALL", method="relayout",
             args=[{"xaxis.range": [first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")]}]),
    ]

    layout_kwargs = dict(
        title=title,
        xaxis=dict(
            range=[first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")],
            rangeslider=dict(visible=True, thickness=0.04),
            type="date",
        ),
        shapes=shapes,
        updatemenus=[dict(
            type="buttons", direction="right", buttons=range_buttons,
            x=0.0, y=1.12, xanchor="left", yanchor="top",
            pad=dict(r=4, t=4), font=dict(size=11), bgcolor="#f4f4f4",
        )],
        margin=dict(l=50, r=50, t=80, b=40),
        plot_bgcolor="white",
        hovermode="x unified",
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(size=10)),
    )
    if secondary_lines:
        fig.update_layout(**layout_kwargs)
        fig.update_yaxes(title_text=yaxis, secondary_y=False)
        fig.update_yaxes(title_text=secondary_yaxis, secondary_y=True)
    else:
        layout_kwargs["yaxis"] = dict(title=yaxis)
        fig.update_layout(**layout_kwargs)

    out = CHARTS / f"market_complacency_{as_of}_{slug}.html"
    fig.write_html(str(out), include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "displaylogo": False})


def _make_composite_html(as_of: str, composite: float, tier: str, composite_hist: pd.Series) -> None:
    """Save an interactive Plotly composite chart with rangeselector buttons.

    Embeddable in markdown via <iframe>. The Plotly toolbar's rangeselector
    gives 1Y / YTD / 5Y / 10Y / ALL with one click — replacing the static
    matplotlib PNG for users who want to zoom into specific windows.
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        print("  plotly not available — skipping interactive composite", file=sys.stderr)
        return

    cutoff = pd.Timestamp(as_of)
    fig = go.Figure()
    # Tier bands as background shapes
    bands = [
        (0, 20, "rgba(126, 181, 65, 0.15)", "Panicked"),
        (20, 40, "rgba(185, 221, 131, 0.10)", "Cautious"),
        (40, 60, "rgba(255, 255, 255, 0.0)", "Neutral"),
        (60, 80, "rgba(244, 162, 97, 0.15)", "Elevated"),
        (80, 100, "rgba(230, 57, 70, 0.20)", "Stretched"),
    ]
    shapes = []
    for lo, hi, color, _ in bands:
        shapes.append(dict(type="rect", xref="paper", yref="y",
                           x0=0, x1=1, y0=lo, y1=hi, fillcolor=color, line_width=0, layer="below"))
    fig.update_layout(shapes=shapes)

    # Composite line
    fig.add_trace(go.Scatter(
        x=composite_hist.index, y=composite_hist.values,
        mode="lines", name="Composite",
        line=dict(color="#1f4e79", width=1.2),
        hovertemplate="%{x|%Y-%m-%d}<br>Composite: %{y:.1f}<extra></extra>",
    ))
    # Today marker
    fig.add_trace(go.Scatter(
        x=[composite_hist.index[-1]], y=[composite],
        mode="markers+text", marker=dict(color="black", size=10),
        text=[f" Today: {composite:.1f} ({tier})"], textposition="middle right",
        textfont=dict(size=11, color="black"),
        showlegend=False,
        hovertemplate=f"Today {as_of}<br>Composite: {composite:.1f}<br>Tier: {tier}<extra></extra>",
    ))

    # Explicit-range buttons (relayout). Plotly's rangeselector stepmode='todate'
    # is buggy in v6.x — sometimes computes YTD as a tiny future window. Using
    # method='relayout' with hardcoded date ranges bypasses the bug entirely.
    last = composite_hist.index[-1]
    first = composite_hist.index[0]
    year_start = pd.Timestamp(f"{last.year}-01-01")
    range_buttons = [
        dict(label="1Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=1)).strftime("%Y-%m-%d"),
                                    last.strftime("%Y-%m-%d")]}]),
        dict(label="YTD", method="relayout",
             args=[{"xaxis.range": [year_start.strftime("%Y-%m-%d"),
                                    last.strftime("%Y-%m-%d")]}]),
        dict(label="5Y",  method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=5)).strftime("%Y-%m-%d"),
                                    last.strftime("%Y-%m-%d")]}]),
        dict(label="10Y", method="relayout",
             args=[{"xaxis.range": [(last - pd.DateOffset(years=10)).strftime("%Y-%m-%d"),
                                    last.strftime("%Y-%m-%d")]}]),
        dict(label="ALL", method="relayout",
             args=[{"xaxis.range": [first.strftime("%Y-%m-%d"),
                                    last.strftime("%Y-%m-%d")]}]),
    ]

    fig.update_layout(
        title=f"Market Complacency Composite, 2001–{as_of[:4]}",
        yaxis=dict(title="Composite (0–100)", range=[0, 100]),
        xaxis=dict(
            title="",
            range=[first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")],
            rangeslider=dict(visible=True, thickness=0.05),
            type="date",
        ),
        updatemenus=[dict(
            type="buttons", direction="right",
            buttons=range_buttons,
            x=0.0, y=1.12, xanchor="left", yanchor="top",
            pad=dict(r=4, t=4),
            font=dict(size=11),
            bgcolor="#f4f4f4",
        )],
        margin=dict(l=50, r=20, t=80, b=40),
        plot_bgcolor="white",
        hovermode="x unified",
        height=520,
    )

    out = CHARTS / f"market_complacency_{as_of}_composite.html"
    fig.write_html(str(out), include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "displaylogo": False})
    print(f"  ✓ interactive composite saved: {out.name}", flush=True)


def _make_charts(as_of, composite, tier, composite_hist, series, table, prec_df, window_years):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    win_start = pd.Timestamp(as_of) - pd.DateOffset(years=window_years)

    # Citi-style bear-market shading helper. Re-applied to every chart so the
    # reader gets visual context for "what was happening in 2000-02 / 2007-09 /
    # 2020 / 2022" without reading a legend. Dates from NBER + S&P 500 bear-
    # market chronology.
    BEAR_PERIODS = [
        ("1990-07-16", "1990-10-11", "Iraq/Recession"),
        ("2000-03-24", "2002-10-09", "Dot-com"),
        ("2007-10-09", "2009-03-09", "GFC"),
        ("2020-02-19", "2020-03-23", "COVID"),
        ("2022-01-03", "2022-10-12", "Fed pivot"),
    ]
    def _shade_bears(ax):
        for start, end, _ in BEAR_PERIODS:
            ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                       alpha=0.20, color="#888888", zorder=0)

    # Interactive Plotly composite chart (with rangeselector: 1Y, YTD, 5Y, 10Y, ALL)
    _make_composite_html(as_of, composite, tier, composite_hist)

    # Chart 1: Composite
    fig, ax = plt.subplots(figsize=(11, 5))
    _shade_bears(ax)
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

    # Chart 2: Long-history credit spread — Moody's BAA-10Y (1986+) with key
    # historical reference values annotated. Used in place of HY OAS because
    # the FRED ICE BofA HY series was relicensed in mid-2023 and is no longer
    # downloadable for free pre-2023. BAA10Y is the standard long-history credit
    # proxy with 40 years of FRED data and covers every US bear market.
    # Known HY OAS reference values (from Citi BMC + published research) are
    # annotated as text alongside the BAA10Y line so the reader sees both.
    if not series["baa10y"].empty:
        baa = series["baa10y"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        ax.plot(baa.index, baa.values, lw=1.0, color="#c1272d", label="Moody's BAA − 10Y (1986+)")
        baa_win = baa[baa.index >= win_start]
        for pct, lbl in [(5, "5th"), (50, "median"), (95, "95th")]:
            v = np.percentile(baa_win.dropna(), pct)
            ax.axhline(v, ls="--", alpha=0.4, color="gray")
            ax.text(baa.index[-1], v, f" {lbl} {v:.2f}", fontsize=8, va="center")
        cur = float(baa_win.iloc[-1])
        ax.scatter([baa.index[-1]], [cur], color="black", s=60, zorder=5,
                   label=f"Today {cur:.2f}pp")
        # Annotate known HY OAS reference values from Citi BMC
        hy_refs = [
            ("2000-03-31", 6.00, "HY Mar-00 ≈ 600bp"),
            ("2007-10-31", 6.00, "HY Oct-07 ≈ 600bp"),
            ("2008-12-15", 21.82, "HY 2008 peak 2182bp"),
            ("2020-02-28", 4.80, "HY Feb-20 ≈ 480bp"),
            ("2021-12-31", 3.37, "HY Dec-21 ≈ 337bp"),
        ]
        for date_str, val, label in hy_refs:
            dt = pd.Timestamp(date_str)
            if dt >= baa.index.min() and dt <= baa.index.max():
                ax.annotate(label, xy=(dt, val), xytext=(10, 0),
                            textcoords="offset points", fontsize=7, color="#888")
        ax.legend(loc="upper right")
        ax.set_ylabel("Spread (pp / %)")
        ax.set_title(f"Long-history credit: Moody's BAA−10Y, 1986–{as_of[:4]} + HY OAS reference points (ICE BofA pre-2023 unavailable on FRED)")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_hy_oas.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 3: Long-history IG credit-tier overlay — Moody's AAA-10Y vs BAA-10Y.
    # Replaces the IG vs CCC OAS chart because ICE BofA IG and CCC are both
    # FRED-restricted to mid-2023 forward (relicensing). Moody's AAA-10Y has
    # FRED daily data back to 1983; BAA-10Y back to 1986. Together they show
    # the IG credit-quality cycle: the SPREAD between the two (BAA − AAA)
    # is the long-history analog of "CCC − HY spread" — credit-quality
    # dispersion within IG widens before turns.
    aaa_rows = fetch_fred("AAA10Y", "1983-01-01")
    if not aaa_rows.empty and not series["baa10y"].empty:
        aaa = aaa_rows
        baa = series["baa10y"]
        # Align on common dates
        df = pd.concat([aaa.rename("aaa"), baa.rename("baa")], axis=1).dropna()
        df["dispersion"] = df["baa"] - df["aaa"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        ax.plot(df.index, df["aaa"], lw=0.8, color="#2a9d8f", label="Moody's AAA − 10Y (top-tier IG, 1983+)")
        ax.plot(df.index, df["baa"], lw=0.8, color="#e76f51", label="Moody's BAA − 10Y (BBB-tier, 1986+)")
        ax2 = ax.twinx()
        ax2.plot(df.index, df["dispersion"], lw=0.6, color="#444444", alpha=0.6,
                 label="BAA − AAA dispersion (right)")
        ax.set_ylabel("Spread (pp)")
        ax2.set_ylabel("BAA − AAA dispersion (pp)", color="#444444")
        cur_aaa = float(df["aaa"].iloc[-1])
        cur_baa = float(df["baa"].iloc[-1])
        cur_disp = float(df["dispersion"].iloc[-1])
        ax.set_title(
            f"Long-history IG credit: AAA−10Y vs BAA−10Y (1983+) — Today AAA {cur_aaa:.2f}pp, "
            f"BAA {cur_baa:.2f}pp, dispersion {cur_disp:.2f}pp"
        )
        ax.grid(alpha=0.3)
        ax.legend(loc="upper left", fontsize=8)
        ax2.legend(loc="upper right", fontsize=8)
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_ig_ccc.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 4: VIX + VVIX overlay — FULL history.
    # VIX goes back to 1990 (Yahoo), VVIX back to 2007. Use full series, not
    # last-10y window, so reader sees dot-com / GFC / COVID spikes.
    if not series["vix"].empty and not series["vvix"].empty:
        vix_full = series["vix"]
        vvix_full = series["vvix"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        ax.plot(vix_full.index, vix_full.values, lw=0.7, color="#1d3557", label="VIX (1990+)")
        ax2 = ax.twinx()
        ax2.plot(vvix_full.index, vvix_full.values, lw=0.7, color="#e63946", label="VVIX (2007+)", alpha=0.6)
        ax.set_ylabel("VIX", color="#1d3557")
        ax2.set_ylabel("VVIX", color="#e63946")
        ax.set_title(f"VIX (1990+) & VVIX (2007+) — Today: VIX {vix_full.iloc[-1]:.1f}, VVIX {vvix_full.iloc[-1]:.0f}")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper left"); ax2.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_vix_vvix.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 5: VIX term slope — extended back via VIX/VIX3M (2006+) overlaid
    # with VIX9D/VIX3M (2011+). The VIX9D-based ratio is the canonical short-
    # term-fear gauge but VIX9D didn't exist before 2011. VIX/VIX3M (30-day ÷
    # 90-day) is the same kind of signal — front-month vs longer-month implied
    # vol — and extends back to 2006-07-17 when CBOE started publishing VIX3M
    # (originally VXV). Plotting both gives long history + the canonical
    # short-term metric on the same axes.
    if not series["vix_slope"].empty:
        slope_short = series["vix_slope"]   # VIX9D / VIX3M (2011+)
        vix_full = series["vix"]
        vix3m_full = fetch_yf("^VIX3M", "2005-01-01", pd.Timestamp(as_of).strftime("%Y-%m-%d"))
        # Compute VIX / VIX3M ratio (2006+) for long history
        slope_long = None
        if not vix_full.empty and not vix3m_full.empty:
            df = pd.concat([vix_full.rename("v"), vix3m_full.rename("v3")], axis=1).dropna()
            slope_long = (df["v"] / df["v3"]).rename("vix_over_vix3m")

        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        # Bands first so the lines plot on top
        max_y = max(2.5, slope_short.max() * 1.05 if not slope_short.empty else 2.5)
        ax.axhspan(0, 0.85, alpha=0.10, color="#7eb541", label="Deep contango (calm)")
        ax.axhspan(1.0, max_y, alpha=0.10, color="#e63946", label="Backwardation (stress)")
        ax.axhline(1.0, ls="--", color="black", alpha=0.5, label="Contango/Backwardation")
        if slope_long is not None and not slope_long.empty:
            ax.plot(slope_long.index, slope_long.values, lw=0.5, color="#a8a8a8",
                    alpha=0.7, label="VIX / VIX3M (30d÷90d, 2006+)")
        ax.plot(slope_short.index, slope_short.values, lw=0.6, color="#264653",
                label="VIX9D / VIX3M (9d÷90d, 2011+)")
        ax.set_ylabel("Front-month ÷ longer-month VIX")
        cur = float(slope_short.iloc[-1]) if not slope_short.empty else None
        ax.set_title(
            f"VIX Term Slope — Today VIX9D/VIX3M {cur:.2f}; long-history proxy VIX/VIX3M (2006+) overlaid"
        )
        ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=8)
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_vix_slope.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 6: MOVE — full history from 2002 (Yahoo's earliest).
    # Note: pre-2002 doesn't exist on Yahoo; the MOVE index was created in
    # 1988 but Yahoo's data starts in 2002.
    if not series["move"].empty:
        move_full = series["move"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        ax.plot(move_full.index, move_full.values, lw=0.7, color="#6a4c93", label="MOVE Index")
        ax.axhline(80, ls="--", color="green", alpha=0.5, label="80 (calm)")
        ax.axhline(120, ls="--", color="red", alpha=0.5, label="120 (stress)")
        ax.set_ylabel("MOVE Index")
        ax.set_title(f"MOVE Index (rate vol), 2002+ — Today: {move_full.iloc[-1]:.0f} (Yahoo's earliest; index created 1988)")
        ax.grid(alpha=0.3); ax.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_move.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 7: ERP (25y)
    if not series["erp"].empty:
        erp_25y = series["erp"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
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

    # Precedents scatter chart REMOVED in v9 — keyed to the composite metric
    # (since dropped as statistically uninformative), 7 scattered points showed
    # no pattern, added no signal beyond the precedents table (which was also
    # removed in v9 along with Action Implications / Backtest / Caveats).

    # Chart 9: CAPE
    if not series["cape"].empty:
        cape_25y = series["cape"]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        _shade_bears(ax)
        ax.plot(cape_25y.index, cape_25y.values, lw=1.0, color="#6d597a")
        ax.axhline(30, ls="--", color="red", alpha=0.5, label="CAPE 30 (historically rich)")
        ax.set_ylabel("Shiller CAPE")
        ax.set_title(f"Shiller CAPE, 2001–{as_of[:4]}")
        ax.grid(alpha=0.3); ax.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig(CHARTS / f"market_complacency_{as_of}_cape.png", dpi=150, bbox_inches="tight")
        plt.close()

    # ──────────────────────────────────────────────────────────────────────
    # Interactive Plotly versions of every Under-the-Hood chart.
    # Reader can use the 1Y / YTD / 5Y / 10Y / ALL buttons to zoom.
    # ──────────────────────────────────────────────────────────────────────
    # Re-fetch AAA10Y (already used above for the IG chart)
    try:
        aaa_series = fetch_fred("AAA10Y", "1983-01-01")
    except Exception:
        aaa_series = pd.Series(dtype=float)

    if not series["baa10y"].empty:
        _make_interactive_chart(
            as_of, "credit_baa",
            title="Long-history credit: Moody's BAA−10Y (1986+)",
            yaxis="Spread (pp)",
            lines=[dict(name="Moody's BAA − 10Y", series=series["baa10y"], color="#c1272d", width=1.2)],
            thresholds=[
                dict(y=float(np.percentile(series["baa10y"][series["baa10y"].index >= win_start].dropna(), 50)),
                     label=f"10y median", color="#888", dash="dash"),
            ],
        )

    if not aaa_series.empty and not series["baa10y"].empty:
        df = pd.concat([aaa_series.rename("aaa"), series["baa10y"].rename("baa")], axis=1).dropna()
        dispersion = (df["baa"] - df["aaa"]).rename("dispersion")
        _make_interactive_chart(
            as_of, "ig_credit",
            title="IG credit tiers: Moody's AAA−10Y vs BAA−10Y (1983+) + dispersion",
            yaxis="Spread (pp)",
            lines=[
                dict(name="AAA − 10Y (top-tier IG)", series=df["aaa"], color="#2a9d8f", width=1.1),
                dict(name="BAA − 10Y (BBB-tier)",     series=df["baa"], color="#e76f51", width=1.1),
            ],
            secondary_lines=[
                dict(name="BAA − AAA dispersion",     series=dispersion, color="#444444", width=0.8),
            ],
            secondary_yaxis="Dispersion (pp)",
        )

    if not series["cape"].empty:
        _make_interactive_chart(
            as_of, "cape",
            title="Shiller CAPE (cyclically-adjusted P/E), 1871+",
            yaxis="Shiller CAPE",
            lines=[dict(name="Shiller CAPE", series=series["cape"], color="#6d597a", width=1.2)],
            thresholds=[
                dict(y=30, label="CAPE 30 (historically rich)", color="#c1272d", dash="dash"),
                dict(y=44, label="Dec-1999 dot-com peak", color="#888", dash="dot"),
            ],
        )

    if not series["erp"].empty:
        _make_interactive_chart(
            as_of, "erp",
            title="Equity Risk Premium = S&P 500 E/P − 10Y Treasury",
            yaxis="ERP (pp)",
            lines=[dict(name="ERP", series=series["erp"], color="#003049", width=1.2)],
            thresholds=[
                dict(y=0, label="zero — stocks priced equal to bonds", color="#c1272d", dash="dash"),
            ],
        )

    if not series["vix"].empty:
        _make_interactive_chart(
            as_of, "vix_vvix",
            title="VIX (1990+) & VVIX (2007+)",
            yaxis="VIX",
            lines=[dict(name="VIX", series=series["vix"], color="#1d3557", width=0.8)],
            secondary_lines=[dict(name="VVIX", series=series["vvix"], color="#e63946", width=0.7)] if not series["vvix"].empty else None,
            secondary_yaxis="VVIX",
            thresholds=[
                dict(y=20, label="VIX 20 (caution)", color="#f4a261", dash="dash"),
                dict(y=30, label="VIX 30 (stress)",  color="#e63946", dash="dash"),
            ],
        )

    if not series["vix_slope"].empty:
        # Also compute long-history VIX/VIX3M overlay
        try:
            vix3m_for_slope = fetch_yf("^VIX3M", "2005-01-01", (pd.Timestamp(as_of) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
        except Exception:
            vix3m_for_slope = pd.Series(dtype=float)
        secondary = None
        if not series["vix"].empty and not vix3m_for_slope.empty:
            sl_df = pd.concat([series["vix"].rename("v"), vix3m_for_slope.rename("v3")], axis=1).dropna()
            long_slope = (sl_df["v"] / sl_df["v3"]).rename("VIX/VIX3M")
            # Plot long-history proxy on same axis as VIX9D/VIX3M
        _make_interactive_chart(
            as_of, "vix_slope",
            title="VIX Term Slope — VIX9D÷VIX3M (2011+) + VIX÷VIX3M long-history proxy (2006+)",
            yaxis="Front-month ÷ longer-month VIX",
            lines=[
                dict(name="VIX/VIX3M (30d÷90d, 2006+)", series=long_slope if not series["vix"].empty and not vix3m_for_slope.empty else pd.Series(dtype=float), color="#a8a8a8", width=0.6),
                dict(name="VIX9D/VIX3M (9d÷90d, 2011+)", series=series["vix_slope"], color="#264653", width=0.8),
            ],
            thresholds=[
                dict(y=1.0, label="Contango ↔ Backwardation", color="#000", dash="dash"),
            ],
        )

    if not series["move"].empty:
        _make_interactive_chart(
            as_of, "move",
            title="MOVE Index (rate vol, 2002+) — Yahoo's earliest; index created 1988",
            yaxis="MOVE Index",
            lines=[dict(name="MOVE", series=series["move"], color="#6a4c93", width=0.8)],
            thresholds=[
                dict(y=80,  label="80 (calm)",   color="#2a9d8f", dash="dash"),
                dict(y=120, label="120 (stress)", color="#e63946", dash="dash"),
            ],
        )


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
