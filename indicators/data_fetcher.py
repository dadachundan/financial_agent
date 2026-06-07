"""
Fetch market indicator data from yfinance (and optionally FRED).

Indicator categories:
  Liquidity   — 3M T-bill yield, 10Y-3M yield spread
  Credit      — HY OAS, IG OAS (FRED), HYG/LQD ETF prices
  Volatility  — VIX, VVIX, VIX term slope (VIX9D/VIX3M)
  Cross-Asset — SPY, 10Y yield, DXY, Gold, WTI Crude
"""

import logging
from pathlib import Path

import requests

log = logging.getLogger(__name__)

# ── Indicator catalogue ───────────────────────────────────────────────────────
#
# symbol prefixes:
#   _SPREAD_A_B   computed: last(A) - last(B), aligned by date
#   _RATIO_A_B    computed: last(A) / last(B)
#   _FRED_SERIES  fetched from FRED API
#   otherwise     yfinance ticker
#
# thresholds:
#   None                         → neutral (grey dot)
#   {direction, caution, stress} → direction="up"   higher=worse
#                                  direction="down"  lower=worse

CATEGORIES = ["Liquidity", "Credit", "Volatility", "Cross-Asset"]

INDICATORS: list[dict] = [
    # ── Liquidity ────────────────────────────────────────────────────────────
    dict(
        id="tbill_3m", symbol="^IRX", name="3M T-Bill Yield",
        category="Liquidity", unit="%",
        description="Short-term funding cost. Rising = tighter liquidity.",
        thresholds=None,
        sources=[
            {"label": "FRED DTB3", "url": "https://fred.stlouisfed.org/series/DTB3"},
            {"label": "U.S. Treasury", "url": "https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics"},
        ],
    ),
    dict(
        id="yield_spread", symbol="_SPREAD_^TNX_^IRX", name="10Y – 3M Spread",
        category="Liquidity", unit="pp",
        description="Yield curve slope. Negative (inverted) = funding stress signal.",
        thresholds=dict(direction="down", caution=0.5, stress=0.0),
        sources=[
            {"label": "FRED T10Y3M", "url": "https://fred.stlouisfed.org/series/T10Y3M"},
        ],
    ),
    # ── Credit ───────────────────────────────────────────────────────────────
    dict(
        id="hy_oas", symbol="_FRED_BAMLH0A0HYM2", name="HY Spread (OAS)",
        category="Credit", unit="%",
        description="ICE BofA HY Option-Adjusted Spread. Widening = credit stress.",
        thresholds=dict(direction="up", caution=4.5, stress=6.5),
        sources=[
            {"label": "FRED BAMLH0A0HYM2", "url": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2"},
        ],
    ),
    dict(
        id="ig_oas", symbol="_FRED_BAMLC0A0CM", name="IG Spread (OAS)",
        category="Credit", unit="%",
        description="ICE BofA IG Option-Adjusted Spread. Widening = credit stress.",
        thresholds=dict(direction="up", caution=1.3, stress=2.0),
        sources=[
            {"label": "FRED BAMLC0A0CM", "url": "https://fred.stlouisfed.org/series/BAMLC0A0CM"},
        ],
    ),
    dict(
        id="hyg", symbol="HYG", name="HY Bond ETF (HYG)",
        category="Credit", unit="$",
        description="High-yield bond ETF price. Falling = credit market stress.",
        thresholds=None,
        sources=[
            {"label": "Yahoo HYG", "url": "https://finance.yahoo.com/quote/HYG/history"},
            {"label": "iShares HYG", "url": "https://www.ishares.com/us/products/239565/ishares-iboxx-high-yield-corporate-bond-etf"},
        ],
    ),
    dict(
        id="lqd", symbol="LQD", name="IG Bond ETF (LQD)",
        category="Credit", unit="$",
        description="Investment-grade bond ETF price.",
        thresholds=None,
        sources=[
            {"label": "Yahoo LQD", "url": "https://finance.yahoo.com/quote/LQD/history"},
            {"label": "iShares LQD", "url": "https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf"},
        ],
    ),
    # ── Volatility ───────────────────────────────────────────────────────────
    dict(
        id="vix", symbol="^VIX", name="VIX",
        category="Volatility", unit="",
        description="S&P 500 30-day implied vol. >20 = elevated stress, >30 = high stress.",
        thresholds=dict(direction="up", caution=20, stress=30),
        sources=[
            {"label": "CBOE VIX", "url": "https://www.cboe.com/tradable_products/vix/vix_historical_data/"},
            {"label": "FRED VIXCLS", "url": "https://fred.stlouisfed.org/series/VIXCLS"},
        ],
    ),
    dict(
        id="vvix", symbol="^VVIX", name="VVIX",
        category="Volatility", unit="",
        description="Vol-of-vol index. High = uncertainty about vol itself.",
        thresholds=dict(direction="up", caution=100, stress=120),
        sources=[
            {"label": "CBOE VVIX", "url": "https://www.cboe.com/us/indices/dashboard/VVIX/"},
            {"label": "Yahoo VVIX", "url": "https://finance.yahoo.com/quote/%5EVVIX/history"},
        ],
    ),
    dict(
        id="vix_slope", symbol="_RATIO_^VIX9D_^VIX3M", name="VIX Term Slope",
        category="Volatility", unit="×",
        description="VIX9D ÷ VIX3M. <1 = contango (calm), >1 = backwardation (stress).",
        thresholds=dict(direction="up", caution=1.0, stress=1.15),
        sources=[
            {"label": "CBOE VIX9D", "url": "https://www.cboe.com/us/indices/dashboard/VIX9D/"},
            {"label": "CBOE VIX3M", "url": "https://www.cboe.com/us/indices/dashboard/VIX3M/"},
        ],
    ),
    # ── Cross-Asset ──────────────────────────────────────────────────────────
    dict(
        id="spy", symbol="SPY", name="S&P 500 (SPY)",
        category="Cross-Asset", unit="$",
        description="US large-cap equities — primary risk asset benchmark.",
        thresholds=None,
        sources=[
            {"label": "Yahoo SPY", "url": "https://finance.yahoo.com/quote/SPY/history"},
            {"label": "SSGA SPY", "url": "https://www.ssga.com/us/en/individual/etfs/spy-spdr-sp-500-etf-trust"},
        ],
    ),
    dict(
        id="tnx", symbol="^TNX", name="10Y Treasury Yield",
        category="Cross-Asset", unit="%",
        description="Long-term rates. Rising = tightening or growth optimism.",
        thresholds=None,
        sources=[
            {"label": "FRED DGS10", "url": "https://fred.stlouisfed.org/series/DGS10"},
            {"label": "U.S. Treasury", "url": "https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics"},
        ],
    ),
    dict(
        id="dxy", symbol="DX-Y.NYB", name="US Dollar (DXY)",
        category="Cross-Asset", unit="",
        description="USD index. Rising = risk-off or dollar funding stress.",
        thresholds=None,
        sources=[
            {"label": "Yahoo DXY", "url": "https://finance.yahoo.com/quote/DX-Y.NYB/history"},
            {"label": "ICE DXY", "url": "https://www.theice.com/products/194/US-Dollar-Index-Futures"},
        ],
    ),
    dict(
        id="gold", symbol="GLD", name="Gold (GLD)",
        category="Cross-Asset", unit="$",
        description="Safe-haven demand. Rising = risk-off or inflation concerns.",
        thresholds=None,
        sources=[
            {"label": "Yahoo GLD", "url": "https://finance.yahoo.com/quote/GLD/history"},
            {"label": "SPDR Gold", "url": "https://www.spdrgoldshares.com/"},
        ],
    ),
    dict(
        id="oil", symbol="CL=F", name="WTI Crude Oil",
        category="Cross-Asset", unit="$",
        description="Growth/demand proxy. Falling = demand contraction.",
        thresholds=None,
        sources=[
            {"label": "EIA WTI", "url": "https://www.eia.gov/dnav/pet/hist/RWTCD.htm"},
            {"label": "FRED DCOILWTICO", "url": "https://fred.stlouisfed.org/series/DCOILWTICO"},
        ],
    ),
]

# Direct yfinance tickers (excludes computed / FRED)
_YF_DIRECT = sorted({
    ind["symbol"] for ind in INDICATORS
    if not ind["symbol"].startswith("_")
})
# Extra symbols needed for computed indicators
_YF_EXTRA = ["^VIX9D", "^VIX3M"]


# ── FRED helper ───────────────────────────────────────────────────────────────
#
# We use FRED's public `fredgraph.csv` endpoint, which serves the same data the
# /series/<id> web page renders — no API key required. Format:
#   observation_date,SERIES_ID
#   2020-01-02,3.43
#   ...
# Missing observations are rendered as ".".


def _fetch_fred(series_id: str, days: int = 60) -> list[dict]:
    """Return [{date, value}, ...] from FRED for the last *days* calendar days."""
    import datetime
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    return _fetch_fred_range(series_id, start.isoformat(), end.isoformat())


def _fetch_fred_range(series_id: str, start: str, end: str | None = None) -> list[dict]:
    """Return [{date, value}, ...] from FRED between *start* and *end* (ISO dates).

    Uses urllib.request rather than `requests` — Akamai's bot manager in front
    of fred.stlouisfed.org blocks `requests`'s TLS fingerprint but lets urllib
    through cleanly.
    """
    import urllib.request
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
    if end:
        url += f"&coed={end}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        rows = []
        # First line is the header: observation_date,SERIES_ID
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
        log.warning("FRED CSV fetch failed for %s: %s", series_id, exc)
        return []


# ── Signal computation ────────────────────────────────────────────────────────

def compute_signal(value: float | None, thresholds: dict | None) -> str:
    """Return 'green', 'yellow', 'red', or 'neutral'."""
    if thresholds is None or value is None:
        return "neutral"
    direction = thresholds.get("direction", "up")
    caution = thresholds["caution"]
    stress = thresholds["stress"]
    if direction == "up":        # higher = worse
        if value >= stress:
            return "red"
        if value >= caution:
            return "yellow"
        return "green"
    else:                        # direction == "down": lower = worse
        if value <= stress:
            return "red"
        if value <= caution:
            return "yellow"
        return "green"


# ── Main fetch ────────────────────────────────────────────────────────────────

def fetch_all() -> dict:
    """
    Fetch all indicators.

    Returns a dict keyed by indicator id:
    {
      "value":        float | None,
      "change_1d":    float | None,   # % or absolute depending on change_type
      "change_1w":    float | None,
      "change_type":  "pct" | "abs",
      "signal":       "green" | "yellow" | "red" | "neutral",
      "history":      [{"date": "YYYY-MM-DD", "value": float}, ...]
    }
    """
    try:
        import yfinance as yf
        import pandas as pd
    except ImportError:
        log.error("yfinance / pandas not installed")
        return {}

    results: dict = {}

    # ── Download all yfinance symbols in one call ─────────────────────────
    all_syms = _YF_DIRECT + [s for s in _YF_EXTRA if s not in _YF_DIRECT]
    try:
        raw = yf.download(
            all_syms, period="65d", interval="1d",
            progress=False, auto_adjust=True,
        )
    except Exception as exc:
        log.error("yfinance download failed: %s", exc)
        return {}

    # Build a clean {symbol: Series} map of daily closes
    closes: dict[str, "pd.Series"] = {}
    try:
        if isinstance(raw.columns, pd.MultiIndex):
            price_df = raw["Close"]
            for sym in all_syms:
                if sym in price_df.columns:
                    s = price_df[sym].dropna()
                    if len(s) > 0:
                        closes[sym] = s
        else:
            # Single-symbol fallback (shouldn't happen with a list)
            s = raw["Close"].dropna()
            if len(s) > 0:
                closes[all_syms[0]] = s
    except Exception as exc:
        log.error("Error parsing yfinance data: %s", exc)
        return {}

    def _series_to_record(s: "pd.Series", change_type: str = "pct") -> dict:
        value = float(s.iloc[-1])
        prev_1d = float(s.iloc[-2]) if len(s) >= 2 else value
        prev_1w = float(s.iloc[-6]) if len(s) >= 6 else prev_1d

        if change_type == "pct":
            chg_1d = (value - prev_1d) / abs(prev_1d) * 100 if prev_1d else 0.0
            chg_1w = (value - prev_1w) / abs(prev_1w) * 100 if prev_1w else 0.0
        else:
            chg_1d = value - prev_1d
            chg_1w = value - prev_1w

        history = [
            {"date": str(idx.date()), "value": round(float(v), 4)}
            for idx, v in s.tail(45).items()
            if not pd.isna(v)
        ]
        return dict(value=value, change_1d=chg_1d, change_1w=chg_1w,
                    change_type=change_type, history=history)

    # ── Process each indicator ────────────────────────────────────────────
    for ind in INDICATORS:
        iid = ind["id"]
        sym = ind["symbol"]

        try:
            if sym.startswith("_FRED_"):
                series_id = sym[len("_FRED_"):]
                rows = _fetch_fred(series_id)
                if rows:
                    vals = [r["value"] for r in rows]
                    dates = [r["date"] for r in rows]
                    value = vals[-1]
                    prev_1d = vals[-2] if len(vals) >= 2 else value
                    prev_1w = vals[-6] if len(vals) >= 6 else prev_1d
                    results[iid] = dict(
                        value=value,
                        change_1d=round(value - prev_1d, 4),
                        change_1w=round(value - prev_1w, 4),
                        change_type="abs",
                        signal=compute_signal(value, ind["thresholds"]),
                        history=[{"date": d, "value": v}
                                 for d, v in zip(dates, vals)],
                    )

            elif sym.startswith("_SPREAD_"):
                # _SPREAD_^TNX_^IRX  →  TNX - IRX
                _, a, b = sym.split("_", 2)[1], sym.split("_", 2)[1], sym.split("_", 2)[2]
                parts = sym[len("_SPREAD_"):].split("_", 1)
                sa_key, sb_key = parts[0], parts[1]
                sa = closes.get(sa_key)
                sb = closes.get(sb_key)
                if sa is not None and sb is not None:
                    spread = (sa - sb).dropna()
                    if len(spread) >= 2:
                        rec = _series_to_record(spread, change_type="abs")
                        rec["signal"] = compute_signal(rec["value"], ind["thresholds"])
                        results[iid] = rec

            elif sym.startswith("_RATIO_"):
                # _RATIO_^VIX9D_^VIX3M  →  VIX9D / VIX3M
                parts = sym[len("_RATIO_"):].split("_", 1)
                sa_key, sb_key = parts[0], parts[1]
                sa = closes.get(sa_key)
                sb = closes.get(sb_key)
                if sa is not None and sb is not None:
                    ratio = (sa / sb).dropna()
                    if len(ratio) >= 2:
                        rec = _series_to_record(ratio, change_type="pct")
                        rec["signal"] = compute_signal(rec["value"], ind["thresholds"])
                        results[iid] = rec

            else:
                # Direct yfinance ticker
                s = closes.get(sym)
                if s is not None and len(s) >= 2:
                    rec = _series_to_record(s, change_type="pct")
                    rec["signal"] = compute_signal(rec["value"], ind["thresholds"])
                    results[iid] = rec

        except Exception as exc:
            log.warning("Error processing indicator %s: %s", iid, exc)

    return results


# ── On-demand history range fetch (modal range selector) ──────────────────────

_RANGE_TO_YF_PERIOD = {
    "1m":  "1mo",
    "3m":  "3mo",
    "6m":  "6mo",
    "ytd": "ytd",
    "1y":  "1y",
    "5y":  "5y",
    "max": "max",
}


def _range_to_fred_start(range_key: str) -> str:
    """Translate a UI range key into an ISO start date for FRED's CSV API."""
    import datetime
    today = datetime.date.today()
    if range_key == "1m":
        return (today - datetime.timedelta(days=31)).isoformat()
    if range_key == "3m":
        return (today - datetime.timedelta(days=93)).isoformat()
    if range_key == "6m":
        return (today - datetime.timedelta(days=186)).isoformat()
    if range_key == "ytd":
        return datetime.date(today.year, 1, 1).isoformat()
    if range_key == "1y":
        return (today - datetime.timedelta(days=366)).isoformat()
    if range_key == "5y":
        return (today - datetime.timedelta(days=5 * 366)).isoformat()
    # "max": FRED honours an arbitrarily-early start; series cap themselves.
    return "1900-01-01"


def _yf_history(symbols: list[str], period: str) -> dict[str, list]:
    """Return {symbol: [(date_iso, close), ...]} for the requested period."""
    import yfinance as yf
    import pandas as pd

    try:
        raw = yf.download(
            symbols, period=period, interval="1d",
            progress=False, auto_adjust=True,
        )
    except Exception as exc:
        log.warning("yfinance period=%s download failed: %s", period, exc)
        return {}

    out: dict[str, list] = {}
    try:
        if isinstance(raw.columns, pd.MultiIndex):
            price_df = raw["Close"]
            for sym in symbols:
                if sym in price_df.columns:
                    s = price_df[sym].dropna()
                    out[sym] = [(str(idx.date()), float(v)) for idx, v in s.items()]
        else:
            s = raw["Close"].dropna()
            if symbols:
                out[symbols[0]] = [(str(idx.date()), float(v)) for idx, v in s.items()]
    except Exception as exc:
        log.warning("yfinance parse failed: %s", exc)
    return out


def fetch_history_range(ind_id: str, range_key: str) -> list[dict]:
    """Fetch a single indicator's history over *range_key* (1m..max).

    Returns [{date, value}, ...]. yfinance for tickers, FRED CSV for FRED series,
    component-wise download + combine for _SPREAD_ / _RATIO_.
    Returns [] on unknown id / fetch failure.
    """
    ind = next((i for i in INDICATORS if i["id"] == ind_id), None)
    if ind is None:
        return []

    sym = ind["symbol"]
    range_key = range_key.lower() if range_key else "1y"
    if range_key not in _RANGE_TO_YF_PERIOD:
        range_key = "1y"
    period = _RANGE_TO_YF_PERIOD[range_key]

    if sym.startswith("_FRED_"):
        series_id = sym[len("_FRED_"):]
        rows = _fetch_fred_range(series_id, _range_to_fred_start(range_key))
        return [{"date": r["date"], "value": round(r["value"], 4)} for r in rows]

    if sym.startswith("_SPREAD_"):
        parts = sym[len("_SPREAD_"):].split("_", 1)
        if len(parts) != 2:
            return []
        a_key, b_key = parts
        data = _yf_history([a_key, b_key], period)
        a, b = dict(data.get(a_key, [])), dict(data.get(b_key, []))
        common = sorted(set(a) & set(b))
        return [{"date": d, "value": round(a[d] - b[d], 4)} for d in common]

    if sym.startswith("_RATIO_"):
        parts = sym[len("_RATIO_"):].split("_", 1)
        if len(parts) != 2:
            return []
        a_key, b_key = parts
        data = _yf_history([a_key, b_key], period)
        a, b = dict(data.get(a_key, [])), dict(data.get(b_key, []))
        common = sorted(set(a) & set(b))
        return [{"date": d, "value": round(a[d] / b[d], 4)}
                for d in common if b[d] != 0]

    # Direct yfinance ticker
    data = _yf_history([sym], period)
    series = data.get(sym, [])
    return [{"date": d, "value": round(v, 4)} for d, v in series]
