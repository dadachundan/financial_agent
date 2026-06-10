"""
Market Status Dashboard — reusable build script.

Goldman-Sachs-Weekly-Kickstart-style exuberance dashboard. Fetches the
9 headline GS exuberance indicators (where public data exists), the
broader Kickstart dashboard panel (FCI / GDP / VIX / sector & factor
returns / top movers), computes percentile ranks, renders charts, and
emits a JSON summary plus a WebSearch fallback queue.

Usage:
  python .claude/skills/market-status/scripts/build_status.py
  python .claude/skills/market-status/scripts/build_status.py --date 2026-06-07
  python .claude/skills/market-status/scripts/build_status.py --date 2026-06-07 --quick

--quick skips the per-constituent breadth + concentration calc.

Outputs (idempotent — same date → same outputs):

  oneoff/market_status_<DATE>_indicators.csv     # per-indicator current value + percentile
  oneoff/market_status_<DATE>_calibration.csv    # 9-row Dot-Com / 2021 / Current table
  oneoff/market_status_<DATE>_panel.csv          # broader dashboard (FCI / NFCI / GDP / VIX / etc.)
  oneoff/market_status_<DATE>_top_movers.csv     # weekly top/bottom 5 SPX movers
  oneoff/market_status_<DATE>_sectors.csv        # sector ETF returns
  oneoff/market_status_<DATE>_summary.json       # composite score + tier + output paths
  oneoff/market_status_<DATE>_websearch_queue.json  # indicators needing WebSearch fallback
  reports/charts/market_status_<DATE>_*.png      # 12-15 charts

The agent (Claude in conversation) then:
  1. Reads _websearch_queue.json and runs WebSearch for each entry
  2. Patches _summary.json with the live values
  3. Writes reports/market-status/market_status_<DATE>.md

Read-only against db/indicators.db. No LLM API calls anywhere.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import io
import json
import sys
import urllib.request
import urllib.error
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# ── Project paths ────────────────────────────────────────────────────────────
# .claude/skills/market-status/scripts/build_status.py
#   parents[0] = scripts
#   parents[1] = market-status
#   parents[2] = skills
#   parents[3] = .claude
#   parents[4] = financial_agent (project root)
PROJECT_ROOT = Path(__file__).resolve().parents[4]
ONEOFF_DIR   = PROJECT_ROOT / "oneoff"
CHARTS_DIR   = PROJECT_ROOT / "reports" / "charts"
ONEOFF_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Reuse the project's FRED helpers (handles TLS-fingerprint quirks of fred.stlouisfed.org)
sys.path.insert(0, str(PROJECT_ROOT))
try:
    from indicators.data_fetcher import _fetch_fred_range
except Exception as exc:  # pragma: no cover — paths only diverge when the project is moved
    print(f"WARN: could not import indicators.data_fetcher: {exc}", file=sys.stderr)
    _fetch_fred_range = None

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


# ── Indicator catalog ────────────────────────────────────────────────────────
# Headline 9 from GS Exhibit 3. `gs_2000` and `gs_2021` are the percentiles
# GS publishes in the Kickstart (last verified visually against the 2026-06-05
# issue, zsxq file_id 412458845521488, Exhibit 3 rendered at 300 dpi — kept as
# anchors for the calibration table even when the script can't fully back-fill
# 30y history for that indicator).
# NOT authoritative: per SKILL.md Step 1.5, transcribe the actual Exhibit 3
# from the zsxq copy of the latest Kickstart each run — if these values
# disagree with the PDF, the PDF wins and this dict must be corrected in the
# same commit. (Past failure: momentum/breadth 2021 anchors sat transposed
# 76<->95 here and shipped into the 2026-06-07 report.)
HEADLINE_INDICATORS = [
    {
        "id": "momentum_3m",
        "category": "Share prices",
        "label": "Momentum factor 3M return",
        "direction": "high",
        "gs_2000": 100, "gs_2021": 95,
        "source_url": "https://www.ishares.com/us/products/251614/ishares-msci-usa-momentum-factor-etf",
        "requires_websearch": False,
    },
    {
        "id": "breadth_52w",
        "category": "Share prices",
        "label": "S&P 500 52-week market breadth",
        "direction": "low",
        "gs_2000": 100, "gs_2021": 76,
        "source_url": "https://www.bespokepremium.com/think-big-blog/",
        "requires_websearch": True,
    },
    {
        "id": "spec_trade",
        "category": "Trading activity",
        "label": "GS Speculative Trading Indicator",
        "direction": "high",
        "gs_2000": 100, "gs_2021": 99,
        # zsxq direct-download URL for the source Kickstart issue (SKILL.md Step 1.5).
        # Update the file_id/name to the latest issue each run; never cite a guessed
        # gspublishing.com deep URL — the pattern returns 403 even with a browser UA.
        "source_url": "http://xs-macbook-air.local:5001/zsxq/pdf/412458845521488/Goldman%20Sachs-US%20Weekly%20Kickstart%EF%BC%9AEvaluating%20exuberance-260605.pdf",
        "requires_websearch": True,
    },
    {
        "id": "put_call",
        "category": "Trading activity",
        "label": "CBOE Equity Put/Call ratio (21-day MA)",
        "direction": "low",
        "gs_2000": 100, "gs_2021": 97,
        "source_url": "https://www.cboe.com/us/options/market_statistics/",
        "requires_websearch": False,
    },
    {
        "id": "short_interest",
        "category": "Trading activity",
        "label": "Short interest, median S&P 500 stock (% of market cap)",
        "direction": "low",
        "gs_2000": 96, "gs_2021": 89,
        "source_url": "https://www.finra.org/finra-data/short-sale-volume-data",
        "requires_websearch": True,
    },
    {
        "id": "yale_confidence",
        "category": "Investor sentiment",
        "label": "Yale US Stock Market Confidence (Buy-on-Dips − Valuation)",
        "direction": "high",
        "gs_2000": 100, "gs_2021": 96,
        "source_url": "https://som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices",
        "requires_websearch": True,
    },
    {
        "id": "aaii_bullbear",
        "category": "Investor sentiment",
        "label": "AAII Bull-Bear spread (3-month MA)",
        "direction": "high",
        "gs_2000": 99, "gs_2021": 92,
        "source_url": "https://www.aaii.com/sentimentsurvey",
        "requires_websearch": True,
    },
    {
        "id": "ipo_count",
        "category": "Corporate sentiment",
        "label": "Number of US IPOs (YTD annualised, > $25M)",
        "direction": "high",
        "gs_2000": 100, "gs_2021": 87,
        "source_url": "https://www.renaissancecapital.com/IPO-Center/Stats",
        "requires_websearch": True,
    },
    {
        "id": "net_issuance",
        "category": "Corporate sentiment",
        "label": "Net US equity issuance (12m rolling, % of market cap)",
        "direction": "high",
        "gs_2000": 100, "gs_2021": 96,
        "source_url": "https://www.sifma.org/resources/research/us-equity-issuance-and-trading-volumes/",
        "requires_websearch": True,
    },
]

# Sector ETF mapping for the broader panel
SECTOR_ETFS = {
    "Energy": "XLE",
    "Information Technology": "XLK",
    "Financials": "XLF",
    "Industrials": "XLI",
    "Health Care": "XLV",
    "Materials": "XLB",
    "Real Estate": "XLRE",
    "Utilities": "XLU",
    "Consumer Staples": "XLP",
    "Communication Services": "XLC",
    "Consumer Discretionary": "XLY",
}

# Factor ETF mapping
FACTOR_ETFS = {
    "Momentum (MTUM)": "MTUM",
    "Value (IWD)": "IWD",
    "Growth (IWF)": "IWF",
    "Low Vol (USMV)": "USMV",
    "Quality (QUAL)": "QUAL",
    "Small-Cap (IWM)": "IWM",
}

# S&P 500 top names (subset — sufficient for the top-10 concentration calc + top-movers scan)
SPX_TOP = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "AMZN", "META", "BRK-B",
    "AVGO", "LLY", "JPM", "TSLA", "V", "WMT", "XOM", "UNH", "MA", "PG",
    "JNJ", "HD", "ORCL", "COST", "ABBV", "MRK", "KO", "BAC", "NFLX",
    "PEP", "ADBE", "TMO", "CSCO", "CRM", "CVX", "AMD", "ABT", "ACN",
    "MCD", "LIN", "WFC", "PM", "DIS", "TXN", "QCOM", "INTU", "T", "DHR",
    "VZ", "CAT", "AXP", "GE", "PFE", "IBM", "AMGN", "ISRG", "BX",
]


# ── Helpers ──────────────────────────────────────────────────────────────────
def _http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _percentile_rank(series: pd.Series, value: float) -> float:
    """Empirical CDF: % of valid history strictly ≤ `value`."""
    s = series.dropna()
    if s.empty:
        return float("nan")
    return float((s <= value).mean() * 100.0)


def _exuberance_pct(raw_pct: float, direction: str) -> float:
    """For 'low = exuberant' indicators, invert."""
    if pd.isna(raw_pct):
        return float("nan")
    return 100.0 - raw_pct if direction == "low" else raw_pct


def _decile_label(pct: float) -> str:
    if pd.isna(pct):
        return "n/a"
    if pct >= 90: return "10th (most exuberant)"
    if pct >= 80: return "9th"
    if pct >= 70: return "8th"
    if pct >= 60: return "7th"
    if pct >= 50: return "6th"
    if pct >= 40: return "5th"
    if pct >= 30: return "4th"
    if pct >= 20: return "3rd"
    if pct >= 10: return "2nd"
    return "1st (least exuberant)"


def _tier_for_score(score: float) -> str:
    if pd.isna(score):
        return "n/a"
    if score >= 80: return "Frothy"
    if score >= 60: return "Stretched"
    if score >= 40: return "Elevated"
    if score >= 20: return "Neutral"
    return "Subdued"


# ── Fetchers — hard data ─────────────────────────────────────────────────────
def _yf_history(ticker: str, start: str, end: str) -> pd.Series:
    # yfinance wants pure ISO dates — strip any time suffix
    end_clean = end.split(" ")[0]
    start_clean = start.split(" ")[0]
    df = yf.download(ticker, start=start_clean, end=end_clean, auto_adjust=True, progress=False, threads=False)
    if df is None or df.empty:
        return pd.Series(dtype=float, name=ticker)
    # yfinance sometimes returns a MultiIndex (Close, ticker) — flatten
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    s = df["Close"].dropna()
    s.name = ticker
    return s


def fetch_momentum_3m(start: str, end: str) -> tuple[float, float, pd.Series]:
    """
    Momentum factor proxy: rolling 3M total return of MTUM (iShares MSCI USA
    Momentum Factor ETF) minus SPY same-window return. The GS proprietary
    GSMEFMOM is long-short; MTUM-minus-SPY is the closest free public analog.

    Returns (current_value_pct, percentile_rank, history_series)
    """
    mtum = _yf_history("MTUM", start, end)
    spy  = _yf_history("SPY", start, end)
    if mtum.empty or spy.empty:
        return float("nan"), float("nan"), pd.Series(dtype=float)
    df = pd.concat([mtum.rename("MTUM"), spy.rename("SPY")], axis=1).dropna()
    # rolling 63-trading-day (~ 3 months) return
    mtum_ret = df["MTUM"].pct_change(63)
    spy_ret  = df["SPY"].pct_change(63)
    excess = (mtum_ret - spy_ret) * 100.0  # %
    excess = excess.dropna()
    if excess.empty:
        return float("nan"), float("nan"), excess
    current = float(excess.iloc[-1])
    pct = _percentile_rank(excess, current)
    return current, pct, excess


def fetch_put_call(start: str, end: str) -> tuple[float, float, pd.Series]:
    """
    CBOE Total Put/Call ratio via yfinance `^CPC`. 21-day rolling mean.
    Direction inverts later: high P/C = bearish = low exuberance.
    """
    s = _yf_history("^CPC", start, end)
    if s.empty:
        return float("nan"), float("nan"), s
    # ^CPC has occasional outliers — clip to [0.3, 2.0]
    s = s.clip(0.3, 2.0)
    rolling = s.rolling(21, min_periods=10).mean().dropna()
    current = float(rolling.iloc[-1])
    pct = _percentile_rank(rolling, current)
    return current, pct, rolling


def fetch_vix(start: str, end: str) -> tuple[float, float, pd.Series]:
    s = _yf_history("^VIX", start, end)
    if s.empty:
        return float("nan"), float("nan"), s
    current = float(s.iloc[-1])
    pct = _percentile_rank(s, current)
    return current, pct, s


def fetch_vix3m(start: str, end: str) -> tuple[float, float, pd.Series]:
    s = _yf_history("^VIX3M", start, end)
    if s.empty:
        return float("nan"), float("nan"), s
    current = float(s.iloc[-1])
    pct = _percentile_rank(s, current)
    return current, pct, s


def fetch_fred(series_id: str, start: str) -> pd.Series:
    """Return a FRED series indexed by date as float."""
    if _fetch_fred_range is None:
        return pd.Series(dtype=float, name=series_id)
    try:
        rows = _fetch_fred_range(series_id, start)
    except Exception as exc:
        print(f"WARN: FRED fetch failed for {series_id}: {exc}", file=sys.stderr)
        return pd.Series(dtype=float, name=series_id)
    if not rows:
        return pd.Series(dtype=float, name=series_id)
    s = pd.Series(
        [float(r["value"]) for r in rows if r.get("value") not in (None, ".")],
        index=pd.to_datetime([r["date"] for r in rows if r.get("value") not in (None, ".")]),
        name=series_id,
    ).sort_index()
    return s


def _parse_multpl_table(html: str, name: str, start_year: int) -> pd.Series:
    """multpl.com tables — handles both the older `class="left"/"right"` format
    and the current plain `<td>...&#x2002; VALUE</td>` format."""
    import re
    rows = re.findall(
        r'<td[^>]*>\s*([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})\s*</td>'
        r'\s*<td[^>]*>\s*(?:&#x2002;|&nbsp;|\s)*\s*([\-\d.,]+)\s*%?\s*</td>',
        html, flags=re.DOTALL,
    )
    data = []
    for date_str, val_str in rows:
        try:
            dt = pd.to_datetime(date_str)
            val = float(val_str.replace(",", ""))
        except Exception:
            continue
        if dt.year >= start_year:
            data.append((dt, val))
    if not data:
        return pd.Series(dtype=float, name=name)
    s = pd.Series([v for _, v in data], index=[d for d, _ in data], name=name).sort_index()
    return s


def fetch_multpl_pe(start_year: int = 1995) -> pd.Series:
    url = "https://www.multpl.com/s-p-500-pe-ratio/table/by-month"
    try:
        html = _http_get(url).decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"WARN: multpl fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float, name="trailing_pe")
    return _parse_multpl_table(html, "trailing_pe", start_year)


def fetch_multpl_dy(start_year: int = 1995) -> pd.Series:
    url = "https://www.multpl.com/s-p-500-dividend-yield/table/by-month"
    try:
        html = _http_get(url).decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"WARN: multpl dy fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float, name="div_yield")
    return _parse_multpl_table(html, "div_yield", start_year)


def fetch_shiller_cape(start_year: int = 1995) -> pd.Series:
    url = "https://www.multpl.com/shiller-pe/table/by-month"
    try:
        html = _http_get(url).decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"WARN: multpl CAPE fetch failed: {exc}", file=sys.stderr)
        return pd.Series(dtype=float, name="cape")
    return _parse_multpl_table(html, "cape", start_year)


def fetch_sector_returns(end_date: pd.Timestamp) -> pd.DataFrame:
    """1W / 1M / 3M / 12M / YTD total return per sector ETF."""
    start = (end_date - pd.Timedelta(days=400)).strftime("%Y-%m-%d")
    rows = []
    for label, ticker in SECTOR_ETFS.items():
        s = _yf_history(ticker, start, (end_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
        if s.empty:
            continue
        latest = float(s.iloc[-1])
        def _ret(days: int) -> float:
            past = s.iloc[: -days] if days > 0 else s
            return float(latest / past.iloc[-1] - 1.0) * 100.0 if not past.empty else float("nan")
        # YTD: from Dec 31 of prior year
        ytd_start = pd.Timestamp(year=end_date.year - 1, month=12, day=31)
        s_ytd = s[s.index >= ytd_start]
        ytd = float(latest / s_ytd.iloc[0] - 1.0) * 100.0 if not s_ytd.empty else float("nan")
        rows.append({
            "Sector": label, "Ticker": ticker,
            "1W (%)":  _ret(5),
            "1M (%)":  _ret(21),
            "3M (%)":  _ret(63),
            "12M (%)": _ret(252),
            "YTD (%)": ytd,
            "Latest":  latest,
        })
    return pd.DataFrame(rows)


def fetch_top_movers(end_date: pd.Timestamp) -> pd.DataFrame:
    """1-week and YTD total return for SPX top names; return top-5 and bottom-5 weekly."""
    start = (end_date - pd.Timedelta(days=400)).strftime("%Y-%m-%d")
    rows = []
    for t in SPX_TOP:
        s = _yf_history(t, start, (end_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
        if s.empty or len(s) < 8:
            continue
        latest = float(s.iloc[-1])
        wk_ago = float(s.iloc[-6]) if len(s) >= 6 else float("nan")
        wk_ret = (latest / wk_ago - 1.0) * 100.0 if not pd.isna(wk_ago) else float("nan")
        ytd_start = pd.Timestamp(year=end_date.year - 1, month=12, day=31)
        s_ytd = s[s.index >= ytd_start]
        ytd_ret = (latest / s_ytd.iloc[0] - 1.0) * 100.0 if not s_ytd.empty else float("nan")
        rows.append({"Ticker": t, "1W (%)": wk_ret, "YTD (%)": ytd_ret, "Latest": latest})
    df = pd.DataFrame(rows).sort_values("1W (%)", ascending=False)
    return df


def compute_top10_concentration(end_date: pd.Timestamp) -> dict:
    """Top-10 SPX names as share of total market cap (informational; uses Yahoo market caps)."""
    caps = {}
    for t in SPX_TOP[:30]:  # cap fetch
        try:
            info = yf.Ticker(t).fast_info
            mc = float(getattr(info, "market_cap", float("nan")))
            if mc and not pd.isna(mc):
                caps[t] = mc
        except Exception:
            continue
    if not caps:
        return {"top10_share": None, "top_names": []}
    sorted_caps = sorted(caps.items(), key=lambda kv: kv[1], reverse=True)
    top10 = sorted_caps[:10]
    top10_mc = sum(v for _, v in top10)
    all_mc   = sum(caps.values())
    share = top10_mc / all_mc if all_mc else None
    return {
        "top10_share_of_top30": round(share, 4) if share else None,
        "top10_names": [t for t, _ in top10],
        "top10_caps_trn": [round(v / 1e12, 2) for _, v in top10],
    }


def compute_realized_correlation(end_date: pd.Timestamp, window: int = 63) -> tuple[float, pd.Series]:
    """3-month realized average pairwise correlation across SPX top names."""
    start = (end_date - pd.Timedelta(days=400)).strftime("%Y-%m-%d")
    tickers = SPX_TOP[:30]
    rets_frames = []
    for t in tickers:
        s = _yf_history(t, start, (end_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
        if s.empty:
            continue
        rets_frames.append(s.pct_change().rename(t))
    if len(rets_frames) < 5:
        return float("nan"), pd.Series(dtype=float)
    rets = pd.concat(rets_frames, axis=1).dropna(how="all")
    # rolling 63-day avg correlation
    corrs = []
    dates = []
    for i in range(window, len(rets)):
        w = rets.iloc[i - window: i].dropna(axis=1, how="any")
        if w.shape[1] < 5:
            continue
        c = w.corr().values
        n = c.shape[0]
        if n < 2:
            continue
        mask = ~np.eye(n, dtype=bool)
        avg = c[mask].mean()
        corrs.append(float(avg))
        dates.append(rets.index[i])
    if not corrs:
        return float("nan"), pd.Series(dtype=float)
    s = pd.Series(corrs, index=dates, name="avg_correlation_3m")
    return float(s.iloc[-1]), s


# ── Chart helpers ────────────────────────────────────────────────────────────
def _annotate_source(ax, text: str) -> None:
    ax.text(
        0.99, 0.02, text, transform=ax.transAxes, fontsize=7, color="#666",
        ha="right", va="bottom", style="italic",
    )


def _line_chart(
    series: pd.Series, title: str, ylabel: str, source: str,
    outpath: Path, *,
    hline: float | None = None,
    second: pd.Series | None = None, second_label: str | None = None,
) -> None:
    """Save a single-series time-series chart with a source footer."""
    if series.empty:
        print(f"  ! skip {outpath.name}: empty series", file=sys.stderr)
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(series.index, series.values, color="#1f4e79", lw=1.4, label=ylabel)
    if second is not None and not second.empty:
        ax2 = ax.twinx()
        ax2.plot(second.index, second.values, color="#c44", lw=1.0, alpha=0.7, label=second_label or "")
        ax2.set_ylabel(second_label or "", color="#c44", fontsize=8)
        ax2.tick_params(axis="y", labelsize=7, colors="#c44")
    if hline is not None:
        ax.axhline(hline, color="#888", lw=0.7, ls="--", alpha=0.6)
    ax.set_title(title, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(True, alpha=0.25, lw=0.5)
    ax.tick_params(labelsize=8)
    _annotate_source(ax, source)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _bar_chart(
    df: pd.DataFrame, x_col: str, y_col: str, title: str, source: str, outpath: Path,
    horizontal: bool = True, color_col: str | None = None,
) -> None:
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(9, max(4, 0.35 * len(df))))
    colors = ["#1f4e79"] * len(df)
    if color_col and color_col in df.columns:
        vals = df[color_col].fillna(0).values
        colors = ["#c44" if v > 0 else "#1f4e79" for v in vals]
    if horizontal:
        ax.barh(df[x_col], df[y_col], color=colors)
        ax.invert_yaxis()
    else:
        ax.bar(df[x_col], df[y_col], color=colors)
    ax.set_title(title, fontsize=11)
    ax.grid(True, alpha=0.25, lw=0.5, axis="x" if horizontal else "y")
    ax.tick_params(labelsize=8)
    _annotate_source(ax, source)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── Build orchestrator ──────────────────────────────────────────────────────
def build(as_of: str, *, quick: bool = False) -> dict:
    as_of_ts  = pd.Timestamp(as_of)
    date_slug = as_of_ts.strftime("%Y-%m-%d")
    # yfinance treats `end` as exclusive — bump by one day so today's close is included
    end       = (as_of_ts + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    start_30y = (as_of_ts - pd.DateOffset(years=30)).strftime("%Y-%m-%d")
    start_10y = (as_of_ts - pd.DateOffset(years=10)).strftime("%Y-%m-%d")

    print(f"==> Building market-status as-of {date_slug}", file=sys.stderr)
    print(f"    project root: {PROJECT_ROOT}", file=sys.stderr)

    # ── 1. Hard-data headline indicators ────────────────────────────────────
    headline_rows: list[dict] = []
    websearch_queue: list[dict] = []

    # 1a. Momentum 3M (MTUM − SPY rolling 63-day excess)
    print("  · fetching MTUM / SPY ...", file=sys.stderr)
    mom_cur, mom_pct, mom_hist = fetch_momentum_3m(start_10y, end)
    headline_rows.append({
        "id": "momentum_3m",
        "label": "Momentum factor 3M return (MTUM − SPY proxy)",
        "category": "Share prices",
        "direction": "high",
        "current_value": round(mom_cur, 2) if not pd.isna(mom_cur) else None,
        "unit": "% excess",
        "raw_pct": round(mom_pct, 1) if not pd.isna(mom_pct) else None,
        "exuberance_pct": round(_exuberance_pct(mom_pct, "high"), 1) if not pd.isna(mom_pct) else None,
        "decile": _decile_label(_exuberance_pct(mom_pct, "high")),
        "history_window": "10y",
        "source_url": "https://www.ishares.com/us/products/251614/ishares-msci-usa-momentum-factor-etf",
        "source_date": date_slug,
        "fetched": True,
    })
    if not mom_hist.empty:
        _line_chart(
            mom_hist.iloc[-2500:], title="Momentum factor 3M excess return (MTUM − SPY proxy)",
            ylabel="% rolling 3M excess", source=f"Source: yfinance MTUM / SPY · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_momentum.png", hline=0.0,
        )

    # 1b. 52-week breadth — defer to WebSearch (per-constituent calc only when --quick=False AND fast)
    headline_rows.append({
        "id": "breadth_52w",
        "label": "S&P 500 52-week market breadth",
        "category": "Share prices",
        "direction": "low",
        "current_value": None, "unit": "diff (pp)",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y", "source_url": "https://www.bespokepremium.com/think-big-blog/",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "breadth_52w",
        "query": "S&P 500 52-week market breadth aggregate index vs median constituent latest 2026",
        "needed_fields": ["current_value", "raw_pct", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 5 — diff between SPX dist-from-52wk-high and median constituent dist-from-52wk-high. A widely-cited proxy is % of SPX members within 5% of 52-week high (FINVIZ, Bespoke, Bloomberg).",
    })

    # 1c. Speculative trading — proxy plus WebSearch override
    print("  · fetching ARKK / IPO / BUZZ speculative proxy ...", file=sys.stderr)
    spec_tickers = ["ARKK", "IPO", "BUZZ"]
    spec_excess_hist = pd.Series(dtype=float)
    excess_series = []
    spy_for_spec = _yf_history("SPY", start_10y, end)
    for t in spec_tickers:
        s = _yf_history(t, start_10y, end)
        if s.empty or spy_for_spec.empty:
            continue
        df = pd.concat([s.rename(t), spy_for_spec.rename("SPY")], axis=1).dropna()
        ret_t   = df[t].pct_change(63)
        ret_spy = df["SPY"].pct_change(63)
        excess_series.append((ret_t - ret_spy) * 100.0)
    if excess_series:
        spec_excess_hist = pd.concat(excess_series, axis=1).mean(axis=1).dropna()
    spec_cur = float(spec_excess_hist.iloc[-1]) if not spec_excess_hist.empty else float("nan")
    spec_pct = _percentile_rank(spec_excess_hist, spec_cur) if not pd.isna(spec_cur) else float("nan")
    headline_rows.append({
        "id": "spec_trade_proxy",
        "label": "Speculative trading proxy (ARKK + IPO + BUZZ avg − SPY)",
        "category": "Trading activity",
        "direction": "high",
        "current_value": round(spec_cur, 2) if not pd.isna(spec_cur) else None,
        "unit": "% rolling 3M excess",
        "raw_pct": round(spec_pct, 1) if not pd.isna(spec_pct) else None,
        "exuberance_pct": round(_exuberance_pct(spec_pct, "high"), 1) if not pd.isna(spec_pct) else None,
        "decile": _decile_label(_exuberance_pct(spec_pct, "high")),
        "history_window": "10y",
        "source_url": "https://www.ark-invest.com/funds/arkk",
        "source_date": date_slug,
        "fetched": True,
        "is_proxy": True,
        "gs_indicator": "spec_trade",
    })
    if not spec_excess_hist.empty:
        _line_chart(
            spec_excess_hist, title="Speculative-trading proxy (ARKK + IPO + BUZZ avg − SPY, 3M)",
            ylabel="% rolling 3M excess",
            source=f"Source: yfinance ARKK / IPO / BUZZ / SPY · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_spec_trade_proxy.png", hline=0.0,
        )
    # Always queue WebSearch for the actual GS indicator level
    websearch_queue.append({
        "id": "spec_trade",
        "query": "Goldman Sachs Speculative Trading Indicator current level 2026 Kickstart",
        "needed_fields": ["current_value", "exuberance_pct", "source_url", "source_date"],
        "hint": "GS Exhibit 6 — proprietary index. Do NOT trust a hardcoded level: read the current level and prior peaks off the Speculative Trading Indicator exhibit in the zsxq copy of the latest Kickstart (SKILL.md Step 1.5). Use the GS read to override the open-source proxy.",
    })

    # 1d. Put/Call (Cboe Total via ^CPC, 21-day MA) — Yahoo delisted ^CPC; queue WebSearch.
    print("  · fetching ^CPC (CBOE total put/call) ...", file=sys.stderr)
    pc_cur, pc_pct, pc_hist = fetch_put_call(start_10y, end)
    pc_fetched = not pd.isna(pc_cur)
    headline_rows.append({
        "id": "put_call",
        "label": "CBOE Equity Put/Call ratio (21-day MA)",
        "category": "Trading activity",
        "direction": "low",
        "current_value": round(pc_cur, 3) if not pd.isna(pc_cur) else None,
        "unit": "ratio",
        "raw_pct": round(pc_pct, 1) if not pd.isna(pc_pct) else None,
        "exuberance_pct": round(_exuberance_pct(pc_pct, "low"), 1) if not pd.isna(pc_pct) else None,
        "decile": _decile_label(_exuberance_pct(pc_pct, "low")) if not pd.isna(pc_pct) else "n/a",
        "history_window": "10y", "source_url": "https://www.cboe.com/us/options/market_statistics/",
        "source_date": date_slug if pc_fetched else None, "fetched": pc_fetched,
        "note": "Yahoo ^CPC delisted; Cboe equitypc.csv stalled Oct 2019. WebSearch for live value.",
    })
    if not pc_hist.empty:
        _line_chart(
            pc_hist, title="CBOE Put/Call ratio (21-day MA)",
            ylabel="ratio",
            source=f"Source: yfinance ^CPC · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_put_call.png", hline=1.0,
        )
    if not pc_fetched:
        websearch_queue.append({
            "id": "put_call",
            "query": "CBOE equity put/call ratio latest weekly 21-day moving average 2026",
            "needed_fields": ["current_value", "exuberance_pct", "decile", "source_url", "source_date"],
            "hint": "GS Exhibit 9 — current ratio HIGH (≥1.0) relative to 2000/2021 historic lows around 0.55-0.65. Low ratio = call activity dominant = exuberant.",
        })

    # 1e. Short interest — WebSearch
    headline_rows.append({
        "id": "short_interest",
        "label": "Short interest, median S&P 500 stock (% of market cap)",
        "category": "Trading activity",
        "direction": "low",
        "current_value": None, "unit": "% of market cap",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y", "source_url": "https://www.finra.org/finra-data/short-sale-volume-data",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "short_interest",
        "query": "S&P 500 median stock short interest percent of market cap 2026 Goldman Sachs FactSet FINRA",
        "needed_fields": ["current_value", "raw_pct", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 11 — current ~3.2% vs 1.5% in 2000/2021. Inverted: high short interest = LOW exuberance.",
    })

    # 1f. Yale Confidence — WebSearch
    headline_rows.append({
        "id": "yale_confidence",
        "label": "Yale US Stock Market Confidence (Buy-on-Dips − Valuation)",
        "category": "Investor sentiment",
        "direction": "high",
        "current_value": None, "unit": "pp",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y",
        "source_url": "https://som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "yale_confidence",
        "query": "Yale Stock Market Confidence Index latest 2026 buy on dips valuation individual investor",
        "needed_fields": ["current_value", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 13 — current similar to 2000/2021 peaks. Buy-on-Dips minus Valuation Confidence (individual or institutional series).",
    })

    # 1g. AAII — WebSearch (CSV blocked)
    headline_rows.append({
        "id": "aaii_bullbear",
        "label": "AAII Bull-Bear spread (latest week)",
        "category": "Investor sentiment",
        "direction": "high",
        "current_value": None, "unit": "pp",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y", "source_url": "https://www.aaii.com/sentimentsurvey",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "aaii_bullbear",
        "query": "AAII sentiment survey latest week bullish bearish percentage 2026",
        "needed_fields": ["current_value", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 12 — bulls outnumbered by bears (36% / 37%) as of late May 2026 = bull-bear spread close to −1pp. 16% exuberance percentile.",
    })

    # 1h. IPO count — WebSearch
    headline_rows.append({
        "id": "ipo_count",
        "label": "Number of US IPOs (YTD annualised, > $25M)",
        "category": "Corporate sentiment",
        "direction": "high",
        "current_value": None, "unit": "deals",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y", "source_url": "https://www.renaissancecapital.com/IPO-Center/Stats",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "ipo_count",
        "query": "Renaissance Capital US IPO count 2026 YTD year to date deals filed",
        "needed_fields": ["current_value", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 15 — current annualised 61 vs 1995-2000 median 289 and post-2000 median 100. Track Renaissance Capital weekly IPO count.",
    })

    # 1i. Net equity issuance — WebSearch
    headline_rows.append({
        "id": "net_issuance",
        "label": "Net US equity issuance (12m rolling, % of market cap)",
        "category": "Corporate sentiment",
        "direction": "high",
        "current_value": None, "unit": "% of market cap",
        "raw_pct": None, "exuberance_pct": None, "decile": "n/a",
        "history_window": "30y", "source_url": "https://www.sifma.org/resources/research/us-equity-issuance-and-trading-volumes/",
        "source_date": None, "fetched": False,
    })
    websearch_queue.append({
        "id": "net_issuance",
        "query": "SIFMA US equity issuance 2026 quarterly volume billion total",
        "needed_fields": ["current_value", "exuberance_pct", "decile", "source_url", "source_date"],
        "hint": "GS Exhibit 16 — current 68% percentile, close to 2015-2019 average. WebSearch SIFMA quarterly equity issuance report.",
    })

    indicators_df = pd.DataFrame(headline_rows)
    indicators_df.to_csv(ONEOFF_DIR / f"market_status_{date_slug}_indicators.csv", index=False)

    # ── 2. Composite (only over fetched headline indicators) ────────────────
    fetched_pcts = [r["exuberance_pct"] for r in headline_rows
                    if r.get("fetched") and not r.get("is_proxy") and r.get("exuberance_pct") is not None]
    # Include the spec_trade proxy until WebSearch override patches it
    proxy_pcts = [r["exuberance_pct"] for r in headline_rows
                  if r.get("is_proxy") and r.get("exuberance_pct") is not None]
    active = fetched_pcts + proxy_pcts
    composite = float(np.mean(active)) if active else float("nan")
    tier = _tier_for_score(composite)
    active_n = len(active)

    # ── 3. Calibration table (Dot-Com / 2021 / Current) ─────────────────────
    calib_rows = []
    by_id = {r["id"]: r for r in headline_rows}
    for spec in HEADLINE_INDICATORS:
        cur_row = by_id.get(spec["id"]) or by_id.get("spec_trade_proxy" if spec["id"] == "spec_trade" else "")
        current_pct = cur_row.get("exuberance_pct") if cur_row else None
        calib_rows.append({
            "Category": spec["category"],
            "Indicator": spec["label"],
            "Direction": "Low = exuberant (inverted)" if spec["direction"] == "low" else "High = exuberant",
            "Dot-Com (2000)": spec["gs_2000"],
            "2021": spec["gs_2021"],
            "Current": current_pct,
            "Source": spec["source_url"],
        })
    calib_df = pd.DataFrame(calib_rows)
    calib_df.to_csv(ONEOFF_DIR / f"market_status_{date_slug}_calibration.csv", index=False)

    # ── 4. Broader panel ──────────────────────────────────────────────────
    print("  · pulling broader macro panel ...", file=sys.stderr)
    panel: dict = {}

    # VIX / VIX3M
    vix_cur, vix_pct, vix_hist = fetch_vix(start_10y, end)
    vix3m_cur, vix3m_pct, vix3m_hist = fetch_vix3m(start_10y, end)
    panel["vix"]       = {"value": vix_cur, "pct_10y": vix_pct, "source": "yfinance ^VIX"}
    panel["vix3m"]     = {"value": vix3m_cur, "pct_10y": vix3m_pct, "source": "yfinance ^VIX3M"}
    if not vix_hist.empty:
        _line_chart(
            vix_hist, title="VIX and 3-month implied vol (VIX3M)",
            ylabel="VIX level",
            source=f"Source: yfinance ^VIX, ^VIX3M · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_vix.png",
            second=vix3m_hist if not vix3m_hist.empty else None,
            second_label="VIX3M",
        )

    # FRED panel
    if _fetch_fred_range is not None:
        for series_id, key, label in [
            ("DGS10",  "ust10y",       "10Y UST yield"),
            ("DGS2",   "ust2y",        "2Y UST yield"),
            ("DFII10", "tips10y",      "10Y TIPS real yield"),
            ("DFEDTARU","fedfunds_up", "Fed funds upper"),
            ("NFCI",   "nfci",         "Chicago Fed NFCI"),
            ("T10Y2Y", "curve_10y2y",  "10Y − 2Y yield curve"),
        ]:
            s = fetch_fred(series_id, start_10y)
            if s.empty:
                panel[key] = {"value": None, "source": f"FRED {series_id}", "error": "empty"}
                continue
            panel[key] = {
                "value": float(s.iloc[-1]),
                "as_of": str(s.index[-1].date()),
                "source": f"FRED {series_id}",
            }

    # Chart: NFCI + curve
    nfci_s = fetch_fred("NFCI", start_10y) if _fetch_fred_range else pd.Series(dtype=float)
    curve_s = fetch_fred("T10Y2Y", start_10y) if _fetch_fred_range else pd.Series(dtype=float)
    if not nfci_s.empty:
        _line_chart(
            nfci_s, title="Chicago Fed National Financial Conditions Index (NFCI)",
            ylabel="index (>0 = tight)",
            source=f"Source: FRED NFCI · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_nfci.png", hline=0.0,
        )
    if not curve_s.empty:
        _line_chart(
            curve_s, title="10Y − 2Y US Treasury yield curve",
            ylabel="percentage points",
            source=f"Source: FRED T10Y2Y · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_curve.png", hline=0.0,
        )

    # multpl: trailing PE / DY / CAPE
    print("  · pulling multpl (PE / DY / CAPE) ...", file=sys.stderr)
    pe_s = fetch_multpl_pe(start_year=1995)
    dy_s = fetch_multpl_dy(start_year=1995)
    cape_s = fetch_shiller_cape(start_year=1995)
    panel["trailing_pe"] = {
        "value": float(pe_s.iloc[-1]) if not pe_s.empty else None,
        "pct_30y": _percentile_rank(pe_s.loc[start_30y:], float(pe_s.iloc[-1])) if not pe_s.empty else None,
        "as_of": str(pe_s.index[-1].date()) if not pe_s.empty else None,
        "source": "multpl.com/s-p-500-pe-ratio",
    }
    panel["div_yield"] = {
        "value": float(dy_s.iloc[-1]) if not dy_s.empty else None,
        "pct_30y": _percentile_rank(dy_s.loc[start_30y:], float(dy_s.iloc[-1])) if not dy_s.empty else None,
        "as_of": str(dy_s.index[-1].date()) if not dy_s.empty else None,
        "source": "multpl.com/s-p-500-dividend-yield",
    }
    panel["cape"] = {
        "value": float(cape_s.iloc[-1]) if not cape_s.empty else None,
        "pct_30y": _percentile_rank(cape_s.loc[start_30y:], float(cape_s.iloc[-1])) if not cape_s.empty else None,
        "as_of": str(cape_s.index[-1].date()) if not cape_s.empty else None,
        "source": "multpl.com/shiller-pe",
    }
    if not cape_s.empty:
        _line_chart(
            cape_s, title="Shiller CAPE (cyclically-adjusted P/E)",
            ylabel="ratio",
            source=f"Source: multpl.com / Shiller · as of {panel['cape']['as_of']}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_cape.png", hline=30.0,
        )

    # ERP = (1 / trailing PE) − 10Y TIPS
    if not pe_s.empty and panel.get("tips10y", {}).get("value") is not None:
        ep = (100.0 / pe_s).rename("E/P")  # percent
        tips_s = fetch_fred("DFII10", start_30y) if _fetch_fred_range else pd.Series(dtype=float)
        if not tips_s.empty:
            tips_monthly = tips_s.resample("ME").last()
            ep_aligned = ep.reindex(tips_monthly.index, method="nearest")
            erp = (ep_aligned - tips_monthly).dropna()
            if not erp.empty:
                panel["erp"] = {
                    "value": float(erp.iloc[-1]),
                    "pct_30y": _percentile_rank(erp, float(erp.iloc[-1])),
                    "as_of": str(erp.index[-1].date()),
                    "source": "Derived: 100/multpl PE − FRED DFII10",
                }
                # ERP chart with E/P and TIPS overlay
                fig, ax = plt.subplots(figsize=(9, 5))
                first = max(ep_aligned.dropna().index.min(), tips_monthly.dropna().index.min())
                last  = min(ep_aligned.dropna().index.max(), tips_monthly.dropna().index.max())
                ax.plot(erp.loc[first:last].index, erp.loc[first:last].values, color="#1f4e79", lw=1.5, label="ERP")
                ax.plot(ep_aligned.loc[first:last].index, ep_aligned.loc[first:last].values, color="#888", lw=0.9, ls="--", label="E/P")
                ax.plot(tips_monthly.loc[first:last].index, tips_monthly.loc[first:last].values, color="#c44", lw=0.9, ls=":", label="10Y TIPS")
                ax.axhline(0, color="#888", lw=0.6)
                ax.set_title("S&P 500 Equity Risk Premium (E/P − 10Y TIPS)", fontsize=11)
                ax.set_ylabel("percentage points", fontsize=9)
                ax.legend(fontsize=8, loc="upper right")
                ax.grid(True, alpha=0.25, lw=0.5)
                ax.tick_params(labelsize=8)
                _annotate_source(ax, f"Source: multpl.com trailing PE · FRED DFII10 · as of {date_slug}")
                plt.tight_layout()
                plt.savefig(CHARTS_DIR / f"market_status_{date_slug}_erp.png", dpi=150, bbox_inches="tight")
                plt.close(fig)

    # Realized correlation (skip if --quick)
    if not quick:
        print("  · computing realized correlation ...", file=sys.stderr)
        corr_cur, corr_hist = compute_realized_correlation(as_of_ts)
        panel["realized_correlation_3m"] = {
            "value": corr_cur,
            "pct_10y": _percentile_rank(corr_hist, corr_cur) if not pd.isna(corr_cur) else None,
            "source": "yfinance SPX top-30 rolling 63-day avg pairwise correlation",
        }
        if not corr_hist.empty:
            _line_chart(
                corr_hist, title="S&P 500 3-month realized average pairwise correlation (top-30 names)",
                ylabel="correlation",
                source=f"Source: yfinance · as of {date_slug}",
                outpath=CHARTS_DIR / f"market_status_{date_slug}_correlation.png", hline=0.3,
            )

        print("  · computing top-10 concentration ...", file=sys.stderr)
        conc = compute_top10_concentration(as_of_ts)
        panel["concentration"] = conc

    # ── 5. Sector + factor + top movers ─────────────────────────────────────
    print("  · fetching sector ETFs ...", file=sys.stderr)
    sectors_df = fetch_sector_returns(as_of_ts)
    sectors_df.to_csv(ONEOFF_DIR / f"market_status_{date_slug}_sectors.csv", index=False)
    if not sectors_df.empty:
        df_sorted = sectors_df.sort_values("YTD (%)", ascending=False).reset_index(drop=True)
        _bar_chart(
            df_sorted, "Sector", "YTD (%)",
            title="S&P 500 sector ETF YTD total return",
            source=f"Source: yfinance · as of {date_slug}",
            outpath=CHARTS_DIR / f"market_status_{date_slug}_sectors_ytd.png",
            color_col="YTD (%)",
        )

    print("  · fetching factor ETFs ...", file=sys.stderr)
    factor_rows = []
    for label, ticker in FACTOR_ETFS.items():
        s = _yf_history(ticker, (as_of_ts - pd.Timedelta(days=400)).strftime("%Y-%m-%d"), end)
        if s.empty or len(s) < 30:
            continue
        latest = float(s.iloc[-1])
        ytd_start = pd.Timestamp(year=as_of_ts.year - 1, month=12, day=31)
        s_ytd = s[s.index >= ytd_start]
        ytd = (latest / s_ytd.iloc[0] - 1.0) * 100.0 if not s_ytd.empty else float("nan")
        m1  = (latest / s.iloc[-22] - 1.0) * 100.0 if len(s) >= 22 else float("nan")
        m3  = (latest / s.iloc[-66] - 1.0) * 100.0 if len(s) >= 66 else float("nan")
        m12 = (latest / s.iloc[-252] - 1.0) * 100.0 if len(s) >= 252 else float("nan")
        factor_rows.append({
            "Factor": label, "Ticker": ticker,
            "1M (%)": m1, "3M (%)": m3, "12M (%)": m12, "YTD (%)": ytd, "Latest": latest,
        })
    factors_df = pd.DataFrame(factor_rows)
    factors_df.to_csv(ONEOFF_DIR / f"market_status_{date_slug}_factors.csv", index=False)

    print("  · scanning top SPX movers ...", file=sys.stderr)
    movers_df = fetch_top_movers(as_of_ts)
    movers_df.to_csv(ONEOFF_DIR / f"market_status_{date_slug}_top_movers.csv", index=False)

    # ── 6. Persist panel + summary ──────────────────────────────────────────
    # JSON-safe convert
    def _safe(v):
        if isinstance(v, (np.floating, np.integer)):
            return float(v)
        if isinstance(v, float) and (pd.isna(v) or np.isinf(v)):
            return None
        return v

    def _json_clean(obj):
        if isinstance(obj, dict):
            return {k: _json_clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_json_clean(x) for x in obj]
        return _safe(obj)

    pd.DataFrame(
        [{"key": k, **(v if isinstance(v, dict) else {"value": v})} for k, v in panel.items()]
    ).to_csv(ONEOFF_DIR / f"market_status_{date_slug}_panel.csv", index=False)

    summary = {
        "as_of": date_slug,
        "composite_score": round(composite, 1) if not pd.isna(composite) else None,
        "tier": tier,
        "active_indicator_count": active_n,
        "headline_indicator_count": 9,
        "websearch_queue_size": len(websearch_queue),
        "outputs": {
            "indicators_csv":  str((ONEOFF_DIR / f"market_status_{date_slug}_indicators.csv").relative_to(PROJECT_ROOT)),
            "calibration_csv": str((ONEOFF_DIR / f"market_status_{date_slug}_calibration.csv").relative_to(PROJECT_ROOT)),
            "panel_csv":       str((ONEOFF_DIR / f"market_status_{date_slug}_panel.csv").relative_to(PROJECT_ROOT)),
            "sectors_csv":     str((ONEOFF_DIR / f"market_status_{date_slug}_sectors.csv").relative_to(PROJECT_ROOT)),
            "factors_csv":     str((ONEOFF_DIR / f"market_status_{date_slug}_factors.csv").relative_to(PROJECT_ROOT)),
            "top_movers_csv":  str((ONEOFF_DIR / f"market_status_{date_slug}_top_movers.csv").relative_to(PROJECT_ROOT)),
            "charts_dir":      str(CHARTS_DIR.relative_to(PROJECT_ROOT)),
        },
        "headline_indicators": headline_rows,
        "panel": panel,
        "websearch_queue": websearch_queue,
    }

    (ONEOFF_DIR / f"market_status_{date_slug}_summary.json").write_text(
        json.dumps(_json_clean(summary), indent=2, default=str)
    )
    (ONEOFF_DIR / f"market_status_{date_slug}_websearch_queue.json").write_text(
        json.dumps(_json_clean(websearch_queue), indent=2)
    )

    print(json.dumps({
        "as_of": date_slug,
        "composite_score": _safe(round(composite, 1) if not pd.isna(composite) else None),
        "tier": tier,
        "active_indicator_count": active_n,
        "headline_indicator_count": 9,
        "websearch_queue_size": len(websearch_queue),
        "summary_path": str((ONEOFF_DIR / f"market_status_{date_slug}_summary.json").relative_to(PROJECT_ROOT)),
    }, indent=2))

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        default=_dt.date.today().isoformat(),
        help="As-of date YYYY-MM-DD (default: today)",
    )
    parser.add_argument("--quick", action="store_true", help="Skip per-constituent calcs (faster)")
    args = parser.parse_args()
    build(args.date, quick=args.quick)


if __name__ == "__main__":
    main()
