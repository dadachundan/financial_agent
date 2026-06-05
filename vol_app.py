"""Flask blueprint for the Options Volatility dashboard (mounted at /vol).

Type a ticker -> the page renders, from *free* yfinance option-chain data:

  * a market-regime bar (VIX / VIX9D / VIX3M / VIX6M term structure + VVIX)
    with a Calm / Normal / Elevated / Stress badge,
  * single-name vol metrics: spot, realized vol (10/20/30/60d), 30d ATM
    implied vol, the implied-minus-realized variance-risk-premium spread,
    25-delta risk-reversal skew, put/call ratio, and the straddle-implied
    expected move,
  * three Plotly charts: the IV term structure (ATM IV vs days-to-expiry),
    the vol smile/skew (IV vs strike for one expiry), and a 1-year
    realized-vol history with the current ATM IV drawn on top.

Honesty notes (this project is allergic to fabricated numbers):
  * yfinance option IVs are end-of-day-ish and can be stale on illiquid
    strikes -> good for a regime/skew dashboard, NOT a live trading signal.
  * A *true* IV-rank needs a stored history of implied vol, which yfinance
    does not provide. The "IV percentile" shown here is ATM IV ranked
    against the trailing-1-year *realized*-vol distribution, and is
    labelled as such in the UI -- it is a proxy, not a real IV rank.
  * Greeks (delta) are computed locally with Black-Scholes; no external
    Greeks feed is used.

No LLM/Claude API is called anywhere here (project-wide hard rule).
"""
from __future__ import annotations

import math
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

import numpy as np
import yfinance as yf
from flask import Blueprint, jsonify, render_template, request

vol_bp = Blueprint("vol", __name__, template_folder="templates")

# Annualisation: 252 trading days.
_ANN = math.sqrt(252.0)
# Risk-free proxy for the Black-Scholes delta used only to locate the
# 25-delta strikes. The skew is insensitive to small r changes.
_RFR = 0.04

# ---------------------------------------------------------------------------
# Tiny in-memory TTL cache so a page reload / expiry-dropdown change does not
# re-hammer Yahoo. Keyed by an arbitrary string; values expire after _TTL s.
# ---------------------------------------------------------------------------
_TTL = 90.0
_CACHE: dict[str, tuple[float, object]] = {}


def _cached(key: str, producer):
    hit = _CACHE.get(key)
    now = time.time()
    if hit and (now - hit[0]) < _TTL:
        return hit[1]
    val = producer()
    _CACHE[key] = (now, val)
    return val


# ---------------------------------------------------------------------------
# Black-Scholes helpers (stdlib only -- erf-based normal CDF, no scipy).
# ---------------------------------------------------------------------------
def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _bs_delta(spot: float, strike: float, t_years: float, iv: float,
              kind: str) -> float | None:
    """Black-Scholes delta. `kind` is 'call' or 'put'."""
    if not (spot > 0 and strike > 0 and t_years > 0 and iv > 0):
        return None
    d1 = (math.log(spot / strike) + (_RFR + 0.5 * iv * iv) * t_years) / (
        iv * math.sqrt(t_years))
    nd1 = _norm_cdf(d1)
    return nd1 if kind == "call" else nd1 - 1.0


def _dte(expiry: str, today: date) -> int:
    return (datetime.strptime(expiry, "%Y-%m-%d").date() - today).days


def _clean_iv(v) -> float | None:
    """yfinance IV is a fraction (0.28 == 28%). Drop NaN / junk values."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(f) or f <= 0.01 or f > 5.0:
        return None
    return f


def _mid(row) -> float | None:
    """Mid price from bid/ask, falling back to last traded price."""
    bid, ask, last = row.get("bid"), row.get("ask"), row.get("lastPrice")
    try:
        bid, ask = float(bid), float(ask)
        if bid > 0 and ask > 0:
            return (bid + ask) / 2.0
    except (TypeError, ValueError):
        pass
    try:
        last = float(last)
        return last if last > 0 else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Realized volatility
# ---------------------------------------------------------------------------
def _realized_vol(closes, window: int) -> float | None:
    """Annualised close-to-close realized vol over the last `window` days."""
    logret = np.log(closes / closes.shift(1)).dropna()
    if len(logret) < window:
        return None
    return float(logret.tail(window).std(ddof=1) * _ANN)


def _rv_series(closes, window: int):
    """Rolling annualised realized-vol series (for the history chart)."""
    logret = np.log(closes / closes.shift(1))
    rv = logret.rolling(window).std(ddof=1) * _ANN
    return rv.dropna()


# ---------------------------------------------------------------------------
# Option-chain analytics
# ---------------------------------------------------------------------------
def _chain(ticker: str, expiry: str):
    """Cached (calls, puts) DataFrames for one expiry."""
    def produce():
        oc = yf.Ticker(ticker).option_chain(expiry)
        return oc.calls, oc.puts
    return _cached(f"chain:{ticker}:{expiry}", produce)


def _atm_iv(calls, puts, spot: float) -> float | None:
    """ATM IV = average of the call & put IV at the strike nearest spot."""
    ivs = []
    for df in (calls, puts):
        if df is None or df.empty:
            continue
        idx = (df["strike"] - spot).abs().idxmin()
        iv = _clean_iv(df.loc[idx, "impliedVolatility"])
        if iv is not None:
            ivs.append(iv)
    return float(np.mean(ivs)) if ivs else None


def _risk_reversal(calls, puts, spot: float, t_years: float) -> float | None:
    """25-delta risk reversal = IV(25d put) - IV(25d call).

    Positive = downside puts bid over upside calls = the usual equity skew.
    Strikes are located by Black-Scholes delta computed from each option's
    own IV.
    """
    def iv_at_target_delta(df, kind, target):
        best, best_gap = None, 1e9
        for _, row in df.iterrows():
            iv = _clean_iv(row["impliedVolatility"])
            if iv is None:
                continue
            d = _bs_delta(spot, float(row["strike"]), t_years, iv, kind)
            if d is None:
                continue
            gap = abs(abs(d) - target)
            if gap < best_gap:
                best_gap, best = gap, iv
        # Only trust it if we found a strike whose delta is within 0.12 of
        # the 0.25 target -- otherwise the chain is too sparse to be honest.
        return best if best_gap <= 0.12 else None

    put_iv = iv_at_target_delta(puts, "put", 0.25)
    call_iv = iv_at_target_delta(calls, "call", 0.25)
    if put_iv is None or call_iv is None:
        return None
    return put_iv - call_iv


def _expected_move(calls, puts, spot: float):
    """Straddle-implied expected move at the ATM strike."""
    if calls is None or calls.empty or puts is None or puts.empty:
        return None
    kc = (calls["strike"] - spot).abs().idxmin()
    kp = (puts["strike"] - spot).abs().idxmin()
    cm, pm = _mid(calls.loc[kc]), _mid(puts.loc[kp])
    if cm is None or pm is None:
        return None
    straddle = cm + pm
    return {
        "straddle": round(straddle, 2),
        "abs": round(straddle, 2),
        "pct": round(100.0 * straddle / spot, 2),
        "lo": round(spot - straddle, 2),
        "hi": round(spot + straddle, 2),
    }


def _pcr(calls, puts):
    """Put/call ratios on volume and open interest."""
    def s(df, col):
        if df is None or df.empty or col not in df:
            return 0.0
        return float(df[col].fillna(0).sum())
    cv, pv = s(calls, "volume"), s(puts, "volume")
    co, po = s(calls, "openInterest"), s(puts, "openInterest")
    return {
        "vol": round(pv / cv, 2) if cv > 0 else None,
        "oi": round(po / co, 2) if co > 0 else None,
    }


def _smile(calls, puts, spot: float):
    """IV-vs-strike series for one expiry (the skew/smile chart)."""
    def series(df):
        out = []
        for _, row in df.iterrows():
            iv = _clean_iv(row["impliedVolatility"])
            if iv is None:
                continue
            out.append((float(row["strike"]), round(100.0 * iv, 2)))
        out.sort()
        return out
    # Keep strikes within +/-35% of spot so far-OTM junk does not flatten
    # the curve.
    lo, hi = spot * 0.65, spot * 1.35
    c = [(k, v) for k, v in series(calls) if lo <= k <= hi]
    p = [(k, v) for k, v in series(puts) if lo <= k <= hi]
    return {
        "spot": round(spot, 2),
        "call": {"strikes": [k for k, _ in c], "iv": [v for _, v in c]},
        "put": {"strikes": [k for k, _ in p], "iv": [v for _, v in p]},
    }


# ---------------------------------------------------------------------------
# Market regime (VIX complex)
# ---------------------------------------------------------------------------
_REGIME_TICKERS = {
    "vix9d": "^VIX9D",
    "vix": "^VIX",
    "vix3m": "^VIX3M",
    "vix6m": "^VIX6M",
    "vvix": "^VVIX",
}


def _regime():
    def produce():
        out = {"asof": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        hist = {}
        for key, sym in _REGIME_TICKERS.items():
            try:
                h = yf.Ticker(sym).history(period="6mo")["Close"].dropna()
                out[key] = round(float(h.iloc[-1]), 2) if len(h) else None
                if key in ("vix", "vix3m"):
                    hist[key] = h
            except Exception:
                out[key] = None
        # Term-structure slope: VIX - VIX3M. > 0 == backwardation == stress.
        vix, vix3m = out.get("vix"), out.get("vix3m")
        slope = round(vix - vix3m, 2) if (vix and vix3m) else None
        out["slope"] = slope
        out["backwardation"] = bool(slope is not None and slope > 0)

        if vix is None:
            regime = ("unknown", "secondary")
        elif (slope is not None and slope > 0) or vix >= 30:
            regime = ("Stress", "danger")
        elif vix >= 20:
            regime = ("Elevated", "warning")
        elif vix >= 15:
            regime = ("Normal", "info")
        else:
            regime = ("Calm", "success")
        out["regime"], out["regime_class"] = regime

        # Shared 6mo history (VIX vs VIX3M) for a future sparkline. The two
        # CBOE series can carry different intraday timestamps, so align them
        # by calendar date (a naive reindex yields all-NaN) and sanitise any
        # residual NaN to None -- bare NaN is invalid JSON and would make the
        # whole /api/regime response unparseable in the browser.
        if "vix" in hist:
            v = hist["vix"].copy()
            v.index = v.index.normalize()
            out["history"] = {
                "dates": [d.strftime("%Y-%m-%d") for d in v.index],
                "vix": [round(float(x), 2) for x in v.values],
            }
            if "vix3m" in hist:
                m = hist["vix3m"].copy()
                m.index = m.index.normalize()
                out["history"]["vix3m"] = [
                    None if (x != x) else round(float(x), 2)
                    for x in m.reindex(v.index).values
                ]
        return out
    return _cached("regime", produce)


# ---------------------------------------------------------------------------
# Single-name bundle
# ---------------------------------------------------------------------------
def _term_and_skew(ticker: str, today: date, spot: float):
    """ATM IV across expiries (term structure) + the per-expiry chains.

    Chains are fetched in parallel (one yfinance call per expiry) so a name
    with 10+ expiries stays responsive.
    """
    try:
        expiries = list(yf.Ticker(ticker).options or [])
    except Exception:
        expiries = []
    cand = [(e, _dte(e, today)) for e in expiries]
    cand = [(e, d) for e, d in cand if 3 <= d <= 420][:12]
    if not cand:
        return [], expiries, None

    def fetch(item):
        e, d = item
        try:
            calls, puts = _chain(ticker, e)
            return e, d, calls, puts
        except Exception:
            return e, d, None, None

    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for e, d, calls, puts in pool.map(fetch, cand):
            iv = _atm_iv(calls, puts, spot) if calls is not None else None
            results.append({"expiry": e, "dte": d, "atmIV": iv,
                            "_calls": calls, "_puts": puts})
    results.sort(key=lambda r: r["dte"])
    return results, expiries, cand


def _bundle(ticker: str) -> dict:
    ticker = ticker.strip().upper()
    today = date.today()
    tk = yf.Ticker(ticker)

    hist = tk.history(period="1y")
    if hist is None or hist.empty:
        return {"ok": False, "error": f"No price data for '{ticker}'."}
    closes = hist["Close"].dropna()
    spot = float(closes.iloc[-1])
    prev = float(closes.iloc[-2]) if len(closes) > 1 else spot
    chg_pct = round(100.0 * (spot - prev) / prev, 2) if prev else None

    rv = {f"rv{w}": (round(100.0 * (_realized_vol(closes, w) or 0), 2)
                     if _realized_vol(closes, w) else None)
          for w in (10, 20, 30, 60)}

    term, expiries, _ = _term_and_skew(ticker, today, spot)

    # Pick the expiry closest to 30 DTE as the "headline" 30d ATM IV + skew.
    atm_iv = atm_dte = expected = skew25 = pcr = smile = None
    headline_expiry = None
    if term:
        headline = min(term, key=lambda r: abs(r["dte"] - 30))
        headline_expiry = headline["expiry"]
        atm_dte = headline["dte"]
        atm_iv = (round(100.0 * headline["atmIV"], 2)
                  if headline["atmIV"] else None)
        calls, puts = headline["_calls"], headline["_puts"]
        if calls is not None:
            expected = _expected_move(calls, puts, spot)
            skew25 = _risk_reversal(calls, puts, spot, headline["dte"] / 365.0)
            skew25 = round(100.0 * skew25, 2) if skew25 is not None else None
            pcr = _pcr(calls, puts)
            smile = _smile(calls, puts, spot)
            smile["expiry"] = headline_expiry
            smile["dte"] = headline["dte"]

    # Variance-risk-premium proxy: 30d ATM IV minus 30d realized vol.
    vrp = (round(atm_iv - rv["rv30"], 2)
           if (atm_iv is not None and rv.get("rv30") is not None) else None)

    # IV percentile vs the trailing-1Y *realized*-vol range (a proxy -- see
    # the module docstring; this is NOT a true IV rank).
    iv_pct = None
    rv20s = _rv_series(closes, 20)
    if atm_iv is not None and len(rv20s) > 20:
        arr = (rv20s.values * 100.0)
        iv_pct = round(100.0 * float((arr < atm_iv).mean()), 1)
    rv_hist = {
        "dates": [d.strftime("%Y-%m-%d") for d in rv20s.index],
        "rv20": [round(float(v) * 100.0, 2) for v in rv20s.values],
    } if len(rv20s) else {"dates": [], "rv20": []}

    return {
        "ok": True,
        "ticker": ticker,
        "asof": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "spot": round(spot, 2),
        "changePct": chg_pct,
        "high52": round(float(closes.max()), 2),
        "low52": round(float(closes.min()), 2),
        "rv": rv,
        "atmIV": atm_iv,
        "atmDTE": atm_dte,
        "headlineExpiry": headline_expiry,
        "vrp": vrp,
        "ivPercentile": iv_pct,
        "skew25": skew25,
        "pcr": pcr,
        "expectedMove": expected,
        "termStructure": [{"expiry": r["expiry"], "dte": r["dte"],
                           "atmIV": (round(100.0 * r["atmIV"], 2)
                                     if r["atmIV"] else None)}
                          for r in term],
        "smile": smile,
        "expiries": [e for e, _ in [(x["expiry"], x["dte"]) for x in term]],
        "rvHistory": rv_hist,
        "hasOptions": bool(term),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@vol_bp.route("/")
def index():
    return render_template("vol.html")


@vol_bp.route("/api/regime")
def api_regime():
    try:
        return jsonify({"ok": True, **_regime()})
    except Exception as exc:  # pragma: no cover - network failure path
        return jsonify({"ok": False, "error": str(exc)}), 502


@vol_bp.route("/api/vol/<ticker>")
def api_vol(ticker):
    try:
        data = _bundle(ticker)
        return jsonify(data), (200 if data.get("ok") else 404)
    except Exception as exc:  # pragma: no cover - network failure path
        return jsonify({"ok": False, "error": str(exc)}), 502


@vol_bp.route("/api/smile/<ticker>")
def api_smile(ticker):
    """Recompute just the smile for a chosen expiry (dropdown re-draw)."""
    expiry = request.args.get("expiry", "")
    try:
        tk = yf.Ticker(ticker.upper())
        spot = float(tk.history(period="5d")["Close"].dropna().iloc[-1])
        calls, puts = _chain(ticker.upper(), expiry)
        out = _smile(calls, puts, spot)
        out["expiry"] = expiry
        out["dte"] = _dte(expiry, date.today())
        return jsonify({"ok": True, **out})
    except Exception as exc:  # pragma: no cover
        return jsonify({"ok": False, "error": str(exc)}), 502


# ---------------------------------------------------------------------------
# Standalone runner:  python vol_app.py --port 5055
# (Also mounted into the main app at /vol via main.py.)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    from flask import Flask, redirect

    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5055)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()

    app = Flask(__name__)
    app.register_blueprint(vol_bp, url_prefix="/vol")
    # The page lives at /vol/ (relative api/... fetches resolve under it);
    # send the bare root there so a standalone launch lands on the dashboard.
    app.add_url_rule("/", "root", lambda: redirect("/vol/"))
    print(f"Vol dashboard -> http://{args.host}:{args.port}/vol/")
    app.run(host=args.host, port=args.port, debug=False)
