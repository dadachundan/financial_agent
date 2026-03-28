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
    ),
    dict(
        id="yield_spread", symbol="_SPREAD_^TNX_^IRX", name="10Y – 3M Spread",
        category="Liquidity", unit="pp",
        description="Yield curve slope. Negative (inverted) = funding stress signal.",
        thresholds=dict(direction="down", caution=0.5, stress=0.0),
    ),
    # ── Credit ───────────────────────────────────────────────────────────────
    dict(
        id="hy_oas", symbol="_FRED_BAMLH0A0HYM2", name="HY Spread (OAS)",
        category="Credit", unit="%",
        description="ICE BofA HY Option-Adjusted Spread. Widening = credit stress.",
        thresholds=dict(direction="up", caution=4.5, stress=6.5),
    ),
    dict(
        id="ig_oas", symbol="_FRED_BAMLC0A0CM", name="IG Spread (OAS)",
        category="Credit", unit="%",
        description="ICE BofA IG Option-Adjusted Spread. Widening = credit stress.",
        thresholds=dict(direction="up", caution=1.3, stress=2.0),
    ),
    dict(
        id="hyg", symbol="HYG", name="HY Bond ETF (HYG)",
        category="Credit", unit="$",
        description="High-yield bond ETF price. Falling = credit market stress.",
        thresholds=None,
    ),
    dict(
        id="lqd", symbol="LQD", name="IG Bond ETF (LQD)",
        category="Credit", unit="$",
        description="Investment-grade bond ETF price.",
        thresholds=None,
    ),
    # ── Volatility ───────────────────────────────────────────────────────────
    dict(
        id="vix", symbol="^VIX", name="VIX",
        category="Volatility", unit="",
        description="S&P 500 30-day implied vol. >20 = elevated stress, >30 = high stress.",
        thresholds=dict(direction="up", caution=20, stress=30),
    ),
    dict(
        id="vvix", symbol="^VVIX", name="VVIX",
        category="Volatility", unit="",
        description="Vol-of-vol index. High = uncertainty about vol itself.",
        thresholds=dict(direction="up", caution=100, stress=120),
    ),
    dict(
        id="vix_slope", symbol="_RATIO_^VIX9D_^VIX3M", name="VIX Term Slope",
        category="Volatility", unit="×",
        description="VIX9D ÷ VIX3M. <1 = contango (calm), >1 = backwardation (stress).",
        thresholds=dict(direction="up", caution=1.0, stress=1.15),
    ),
    # ── Cross-Asset ──────────────────────────────────────────────────────────
    dict(
        id="spy", symbol="SPY", name="S&P 500 (SPY)",
        category="Cross-Asset", unit="$",
        description="US large-cap equities — primary risk asset benchmark.",
        thresholds=None,
    ),
    dict(
        id="tnx", symbol="^TNX", name="10Y Treasury Yield",
        category="Cross-Asset", unit="%",
        description="Long-term rates. Rising = tightening or growth optimism.",
        thresholds=None,
    ),
    dict(
        id="dxy", symbol="DX-Y.NYB", name="US Dollar (DXY)",
        category="Cross-Asset", unit="",
        description="USD index. Rising = risk-off or dollar funding stress.",
        thresholds=None,
    ),
    dict(
        id="gold", symbol="GLD", name="Gold (GLD)",
        category="Cross-Asset", unit="$",
        description="Safe-haven demand. Rising = risk-off or inflation concerns.",
        thresholds=None,
    ),
    dict(
        id="oil", symbol="CL=F", name="WTI Crude Oil",
        category="Cross-Asset", unit="$",
        description="Growth/demand proxy. Falling = demand contraction.",
        thresholds=None,
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

def _load_fred_key() -> str | None:
    """Walk up from this file to find config.py containing FRED_API_KEY."""
    for p in [Path(__file__).parent.parent, Path(__file__).parent.parent.parent]:
        cfg = p / "config.py"
        if cfg.exists():
            ns: dict = {}
            exec(cfg.read_text(), ns)  # noqa: S102
            key = ns.get("FRED_API_KEY")
            if key:
                return key
    return None


def _fetch_fred(series_id: str, api_key: str, days: int = 60) -> list[dict]:
    """Return [{date, value}, ...] from FRED for the last *days* calendar days."""
    import datetime
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={series_id}&api_key={api_key}&file_type=json"
        f"&observation_start={start}&sort_order=asc"
    )
    try:
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        rows = []
        for obs in r.json().get("observations", []):
            try:
                rows.append({"date": obs["date"], "value": float(obs["value"])})
            except (ValueError, KeyError):
                pass
        return rows
    except Exception as exc:
        log.warning("FRED fetch failed for %s: %s", series_id, exc)
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

    fred_key = _load_fred_key()
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
                if fred_key:
                    rows = _fetch_fred(series_id, fred_key)
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
                # If no FRED key: leave indicator absent (UI shows N/A)

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
