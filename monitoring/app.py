"""
monitoring/app.py — Stock price shape viewer.

Exposes `price_shape_bp` for registration in main.py under /price-shape.

Standalone usage:
    python3 monitoring/app.py --port 8005
"""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
import traceback
from datetime import date as _date
from pathlib import Path
from flask import Blueprint, Flask, redirect, render_template, request, jsonify
import numpy as np

from monitoring.price_shape_monitor import fetch_ohlcv, zigzag, classify_shape
from pe.app import WATCHLIST, SECTOR_MAP

SCRIPT_DIR = Path(__file__).parent

price_shape_bp = Blueprint(
    "price_shape", __name__,
    template_folder="templates",
)

# ── In-memory OHLCV cache (keyed by (ticker, days, date)) ────────────────────
# Valid for the entire trading day; stale entries from previous days are ignored.
_CACHE: dict = {}   # key → {"df": df, "label": str}


def _today() -> str:
    return _date.today().isoformat()


def _cached_ohlcv(ticker: str, days: int):
    key = (ticker.upper(), days, _today())
    entry = _CACHE.get(key)
    if entry:
        return entry["df"], entry["label"], True   # (df, label, from_cache)
    df, label = fetch_ohlcv(ticker, days=days)
    # Evict any stale entries for this ticker (different date)
    for k in [k for k in _CACHE if k[0] == ticker.upper() and k[2] != _today()]:
        del _CACHE[k]
    _CACHE[key] = {"df": df, "label": label}
    return df, label, False


# ── V-shape detection ─────────────────────────────────────────────────────────

def detect_vshapes(pivot_idx, directions, prices, min_depth_pct=5.0):
    shapes = []
    n = len(pivot_idx)
    for i in range(1, n - 1):
        d_left, d_mid, d_right = directions[i-1], directions[i], directions[i+1]
        p_left  = prices[pivot_idx[i-1]]
        p_mid   = prices[pivot_idx[i]]
        p_right = prices[pivot_idx[i+1]]

        if d_mid == -1 and d_left == +1 and d_right == +1:   # V-bottom
            depth = min(
                (p_left  - p_mid) / p_left  * 100,
                (p_right - p_mid) / p_right * 100,
            )
            if depth >= min_depth_pct:
                shapes.append({
                    "type": "V-bottom",
                    "idx_left":  int(pivot_idx[i-1]),
                    "idx_mid":   int(pivot_idx[i]),
                    "idx_right": int(pivot_idx[i+1]),
                    "depth_pct": round(depth, 1),
                })

        elif d_mid == +1 and d_left == -1 and d_right == -1:  # Inverted-V
            depth = min(
                (p_mid - p_left)  / p_left  * 100,
                (p_mid - p_right) / p_right * 100,
            )
            if depth >= min_depth_pct:
                shapes.append({
                    "type": "inv-V",
                    "idx_left":  int(pivot_idx[i-1]),
                    "idx_mid":   int(pivot_idx[i]),
                    "idx_right": int(pivot_idx[i+1]),
                    "depth_pct": round(depth, 1),
                })

    # Greedy non-overlapping filter: keep a shape only when it starts
    # strictly after the previous kept shape ends (no shared pivots).
    non_overlapping = []
    last_right = -1
    for s in shapes:
        if s["idx_left"] > last_right:
            non_overlapping.append(s)
            last_right = s["idx_right"]

    return list(reversed(non_overlapping))


# ── Routes ────────────────────────────────────────────────────────────────────

@price_shape_bp.route("/")
def index():
    import nav_widget2 as nw2
    return render_template("price_shape.html", nav=nw2.NAV_HTML, _base="/price-shape")


@price_shape_bp.route("/api/ohlcv")
def api_ohlcv():
    """Fetch + cache raw OHLCV. Called once per ticker/period change."""
    ticker = request.args.get("ticker", "").strip()
    days   = int(request.args.get("days", 365))

    if not ticker:
        return jsonify({"error": "ticker required"}), 400

    t0 = time.time()
    try:
        df, label, from_cache = _cached_ohlcv(ticker, days)
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}",
                        "traceback": traceback.format_exc()}), 500

    closes = df["close"].values.astype(float)
    dates  = df["date"].values.astype("datetime64[D]").astype(str).tolist()

    return jsonify({
        "ticker":     label,
        "dates":      dates,
        "open":       df["open"].values.astype(float).round(2).tolist(),
        "high":       df["high"].values.astype(float).round(2).tolist(),
        "low":        df["low"].values.astype(float).round(2).tolist(),
        "close":      closes.round(2).tolist(),
        "volume":     df["volume"].values.astype(float).tolist(),
        "from_cache": from_cache,
        "elapsed_ms": round((time.time() - t0) * 1000),
    })


@price_shape_bp.route("/api/zigzag", methods=["POST"])
def api_zigzag():
    """Apply ZigZag + V-shape detection to already-supplied price data. Pure CPU, no network."""
    try:
        closes    = np.array(request.json["close"], dtype=float)
        dates     = request.json["dates"]
        threshold = float(request.json.get("threshold", 5.0))
    except Exception as e:
        return jsonify({"error": f"bad payload: {e}"}), 400

    pivot_idx, directions = zigzag(closes, threshold=threshold)
    vshapes = detect_vshapes(pivot_idx, directions, closes, min_depth_pct=threshold)

    pivots = [
        {"date": dates[i], "price": round(float(closes[i]), 2), "direction": int(d)}
        for i, d in zip(pivot_idx, directions)
    ]

    return jsonify({
        "pivots":      pivots,
        "vshapes":     vshapes,
        "shape_label": classify_shape(pivot_idx, directions, closes),
    })


# ── Watchlist bulk OHLCV cache (date-keyed) ───────────────────────────────────
_SCAN_CACHE: dict = {}   # date_str → DataFrame


def _bulk_ohlcv():
    """Fetch 90d OHLCV for every watchlist ticker in one yfinance call. Cached per day."""
    import yfinance as yf
    today = _today()
    if today in _SCAN_CACHE:
        return _SCAN_CACHE[today]
    # Evict yesterday's entry
    for k in [k for k in _SCAN_CACHE if k != today]:
        del _SCAN_CACHE[k]
    all_tickers = [t for _, ts in WATCHLIST for t in ts]
    df = yf.download(all_tickers, period="90d", progress=False,
                     auto_adjust=True, group_by="ticker")
    _SCAN_CACHE[today] = df
    return df


@price_shape_bp.route("/api/watchlist-scan")
def api_watchlist_scan():
    """
    Scan all watchlist tickers and return those whose latest ZigZag pivot
    falls within the last `n_days` trading days.
    """
    n_days    = int(request.args.get("days", 1))
    threshold = float(request.args.get("threshold", 5.0))

    try:
        bulk = _bulk_ohlcv()
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}",
                        "traceback": traceback.format_exc()}), 500

    all_tickers = [t for _, ts in WATCHLIST for t in ts]
    results = []

    for ticker in all_tickers:
        try:
            # MultiIndex: bulk[ticker]["Close"]  |  single-ticker: bulk["Close"]
            if len(all_tickers) == 1:
                closes = bulk["Close"].dropna().values.astype(float)
                dates  = bulk["Close"].dropna().index.strftime("%Y-%m-%d").tolist()
            else:
                col = bulk[ticker]["Close"].dropna()
                if len(col) < 10:
                    continue
                closes = col.values.astype(float)
                dates  = col.index.strftime("%Y-%m-%d").tolist()

            pivot_idx, directions = zigzag(closes, threshold=threshold)
            if not pivot_idx:
                continue

            last_pi = pivot_idx[-1]
            # Check if last pivot falls in the final n_days bars
            if last_pi < len(closes) - n_days:
                continue

            # Determine pivot type
            last_dir = directions[-1]
            ptype = "V-bottom ▲" if last_dir == -1 else "inv-V ▼"
            pct_move = round((closes[-1] - closes[last_pi]) / closes[last_pi] * 100, 1) \
                       if last_pi < len(closes) - 1 else 0.0

            results.append({
                "ticker":      ticker,
                "sector":      SECTOR_MAP.get(ticker, ""),
                "type":        ptype,
                "direction":   int(last_dir),
                "price":       round(float(closes[-1]), 2),
                "pivot_price": round(float(closes[last_pi]), 2),
                "pivot_date":  dates[last_pi],
                "pct_since":   pct_move,
            })
        except Exception:
            continue

    # Sort: troughs first (potential buy signals), then by abs(pct_since) desc
    results.sort(key=lambda r: (r["direction"], -abs(r["pct_since"])))

    return jsonify({
        "results":   results,
        "n_days":    n_days,
        "threshold": threshold,
        "total":     len(all_tickers),
    })


# ── Standalone entry point ────────────────────────────────────────────────────

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    app = Flask(__name__, template_folder=str(SCRIPT_DIR / "templates"))
    app.register_blueprint(price_shape_bp, url_prefix="/price-shape")

    @app.route("/")
    def _root():
        return redirect("/price-shape/")

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8005)
    args = parser.parse_args()

    print(f"Price Shape Monitor → http://localhost:{args.port}/price-shape/")
    app.run(host="0.0.0.0", port=args.port, debug=True)
