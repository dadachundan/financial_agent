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
from pathlib import Path
from flask import Blueprint, Flask, redirect, render_template, request, jsonify
import numpy as np

from monitoring.price_shape_monitor import fetch_ohlcv, zigzag, classify_shape

SCRIPT_DIR = Path(__file__).parent

price_shape_bp = Blueprint(
    "price_shape", __name__,
    template_folder="templates",
)

# ── In-memory OHLCV cache (keyed by (ticker, days), TTL 30 min) ───────────────
_CACHE: dict = {}          # key → {"df": df, "label": str, "ts": float}
_CACHE_TTL = 30 * 60       # seconds


def _cached_ohlcv(ticker: str, days: int):
    key = (ticker.upper(), days)
    entry = _CACHE.get(key)
    if entry and (time.time() - entry["ts"]) < _CACHE_TTL:
        return entry["df"], entry["label"], True   # (df, label, from_cache)
    df, label = fetch_ohlcv(ticker, days=days)
    _CACHE[key] = {"df": df, "label": label, "ts": time.time()}
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

    return shapes


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


@price_shape_bp.route("/api/zigzag")
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
