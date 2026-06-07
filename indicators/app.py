#!/usr/bin/env python3
"""
indicators/app.py — Market Indicators Dashboard.

Routes
------
  GET  /indicators/          Dashboard page
  GET  /indicators/api/config    Indicator catalogue (metadata)
  GET  /indicators/api/snapshot  Latest snapshot (auto-refresh if stale)
  POST /indicators/api/refresh   Force-refresh all data (synchronous)
  GET  /indicators/api/history/<id>  Full DB history for one indicator

Standalone usage
----------------
    python indicators/app.py [--port 8003]
"""

import argparse
import logging
import sys
import threading
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
# Ensure the project root (parent of indicators/) is on sys.path so that
# nav_widget2, claude_llm, etc. are importable when running standalone.
_PROJECT_ROOT = SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from flask import Blueprint, Flask, abort, jsonify, render_template, redirect, request

import nav_widget2 as nw2  # noqa: F401  (NAV_HTML used in template)
import indicators.db as _db
from indicators.data_fetcher import (
    CATEGORIES, INDICATORS, fetch_all, fetch_history_range, fetch_range_snapshot,
)

log = logging.getLogger(__name__)

# ── Blueprint ─────────────────────────────────────────────────────────────────

indicators_bp = Blueprint(
    "indicators", __name__,
    template_folder="templates",
)

# ── Background refresh ────────────────────────────────────────────────────────

CACHE_TTL = 15 * 60   # refresh if snapshot older than 15 minutes

_refresh_lock = threading.Lock()
_refresh_in_progress = False


def _do_refresh() -> dict:
    global _refresh_in_progress
    log.info("Fetching indicator data…")
    data = fetch_all()
    if data:
        _db.save_snapshot(data)
        log.info("Snapshot saved (%d indicators)", len(data))
    _refresh_in_progress = False
    return data


def _background_refresh() -> None:
    with _refresh_lock:
        _do_refresh()


def ensure_fresh(force: bool = False) -> None:
    """Trigger a background refresh if the snapshot is stale or forced."""
    global _refresh_in_progress
    if _refresh_in_progress:
        return
    if force or _db.snapshot_age_seconds() > CACHE_TTL:
        _refresh_in_progress = True
        t = threading.Thread(target=_background_refresh, daemon=True)
        t.start()


# ── Indicator metadata helper ─────────────────────────────────────────────────

def _indicator_meta() -> list[dict]:
    return [
        dict(
            id=ind["id"],
            name=ind["name"],
            category=ind["category"],
            unit=ind["unit"],
            description=ind["description"],
            thresholds=ind["thresholds"],
            sources=ind.get("sources", []),
        )
        for ind in INDICATORS
    ]


# ── Routes ────────────────────────────────────────────────────────────────────

@indicators_bp.route("/")
def dashboard():
    """Default view: Bear Market Checklist (BMC) calibration table.
    Mirrors Figure 2 of the market-complacency report — historical reference
    columns hardcoded, Now column fetched live from /api/bmc-today (5-min cache).
    """
    return render_template(
        "bmc.html",
        nav=nw2.NAV_HTML,
    )


@indicators_bp.route("/grid")
def dashboard_grid():
    """Legacy view: the card-grid of every indicator with sparklines."""
    ensure_fresh()
    return render_template(
        "indicators.html",
        nav=nw2.NAV_HTML,
        _base="/indicators",
    )


# ── BMC live-today endpoint ───────────────────────────────────────────────
import time as _time
_BMC_TODAY_CACHE = {"t": 0.0, "data": None}
_BMC_TODAY_TTL = 300.0   # 5 minutes — fresh enough during market hours, light on upstream APIs

def _bmc_compute_today() -> dict:
    """Fetch today's value + flag color for each BMC indicator.

    Returns a dict {indicator_id: {value: float|str, flag: "red"|"amber"|"green"|"stress"|None, suffix: str|None}}
    """
    import yfinance as yf
    import urllib.request, re as _re, html as _html, json as _json
    import pandas as pd
    out = {}

    def _safe(fn, default=None):
        try:
            return fn()
        except Exception:
            return default

    # ── FRED API helper (reads config.FRED_API_KEY) ───────────────────────
    try:
        import sys as _sys, pathlib as _pl
        _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
        import config as _cfg
        _FRED_KEY = getattr(_cfg, "FRED_API_KEY", None)
    except Exception:
        _FRED_KEY = None

    def _fred_latest(series_id: str) -> float | None:
        if not _FRED_KEY:
            return None
        url = (f"https://api.stlouisfed.org/fred/series/observations"
               f"?series_id={series_id}&file_type=json&api_key={_FRED_KEY}"
               f"&sort_order=desc&limit=5")
        data = _json.loads(urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "curl/8.4.0"}),
            timeout=20).read())
        for o in data.get("observations", []):
            if o.get("value") not in ("", "."):
                return float(o["value"])
        return None

    # ── Yahoo Finance latest close ────────────────────────────────────────
    def _yf_latest(ticker: str) -> float | None:
        h = yf.download(ticker, period="5d", progress=False,
                        auto_adjust=True, threads=False)
        if h is None or h.empty:
            return None
        c = h["Close"].iloc[:, 0] if isinstance(h.columns, pd.MultiIndex) else h["Close"]
        return float(c.iloc[-1])

    # ── Multpl scraper (one row per indicator) ────────────────────────────
    def _multpl_latest(slug: str) -> tuple[float | None, str | None]:
        """Returns (value, latest_date) from a multpl by-month page."""
        url = f"https://www.multpl.com/{slug}/table/by-month"
        text = urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=20).read().decode("utf-8", errors="replace")
        rows = _re.findall(r"<tr[^>]*>(.*?)</tr>", text, _re.S)
        for r in rows:
            cells = [_html.unescape(_re.sub(r"<[^>]+>", "", c)).strip()
                     for c in _re.findall(r"<td[^>]*>(.*?)</td>", r, _re.S)]
            if len(cells) < 2:
                continue
            try:
                dt = pd.to_datetime(cells[0])
                v = float(_re.sub(r"[†$  %\s]", "", cells[1]))
                return v, dt.strftime("%Y-%m-%d")
            except Exception:
                continue
        return None, None

    # ── Each indicator: pull value + decide flag ──────────────────────────

    # Trailing PE: red if ≥ 28, amber 18-28
    pe, pe_date = _safe(lambda: _multpl_latest("s-p-500-pe-ratio"), (None, None))
    if pe is not None:
        flag = "red" if pe >= 28 else ("amber" if pe >= 18 else None)
        out["trailing_pe"] = {"value": round(pe, 1), "flag": flag, "suffix": f"as of {pe_date}" if pe_date else None}

    # Dividend Yield: red if ≤ 1.3, amber if ≤ 2.1
    dy, dy_date = _safe(lambda: _multpl_latest("s-p-500-dividend-yield"), (None, None))
    if dy is not None:
        flag = "red" if dy <= 1.3 else ("amber" if dy <= 2.1 else None)
        out["dy"] = {"value": round(dy, 2), "flag": flag, "suffix": f"as of {dy_date}" if dy_date else None}

    # Shiller CAPE: red if ≥ 30, amber if ≥ 25
    cape, cape_date = _safe(lambda: _multpl_latest("shiller-pe"), (None, None))
    if cape is not None:
        flag = "red" if cape >= 30 else ("amber" if cape >= 25 else None)
        out["cape"] = {"value": round(cape, 1), "flag": flag, "suffix": f"as of {cape_date}" if cape_date else None}

    # ERP: derived from current PE - 10Y. Red if negative or near zero, amber if low
    tnx_val = _safe(lambda: _yf_latest("^TNX"))
    if pe is not None and tnx_val is not None:
        tnx_pct = tnx_val if tnx_val < 10 else tnx_val / 10  # ^TNX usually in % already
        ep = 100.0 / pe
        erp_val = ep - tnx_pct
        flag = "red" if erp_val <= 0.5 else ("amber" if erp_val <= 2.0 else None)
        out["erp"] = {"value": round(erp_val, 2), "flag": flag,
                      "suffix": f"E/P {ep:.2f}% − 10Y {tnx_pct:.2f}%"}

    # 10Y - 2Y curve (FRED T10Y2Y, bp)
    t10y2y = _safe(lambda: _fred_latest("T10Y2Y"))
    if t10y2y is not None:
        bp = round(t10y2y * 100)
        flag = "red" if bp <= -25 else ("amber" if bp <= 0 else None)
        out["t10y2y"] = {"value": ("+%d" % bp) if bp >= 0 else str(bp), "flag": flag, "suffix": None}

    # Moody's BAA - 10Y (long-history credit, FRED BAA10Y)
    baa = _safe(lambda: _fred_latest("BAA10Y"))
    if baa is not None:
        flag = "red" if baa <= 1.6 else ("amber" if baa <= 2.0 else None)
        out["baa10y"] = {"value": round(baa, 2), "flag": flag, "suffix": None}

    # HY OAS (FRED BAMLH0A0HYM2). Bilateral: low = complacent, high = stress
    hy = _safe(lambda: _fred_latest("BAMLH0A0HYM2"))
    if hy is not None:
        if hy <= 2.8: flag = "red"
        elif hy <= 3.0: flag = "amber"
        elif hy >= 6.5: flag = "stress"
        elif hy >= 4.5: flag = "amber"
        else: flag = None
        out["hy_oas"] = {"value": round(hy, 2), "flag": flag, "suffix": None}

    # IG OAS (FRED BAMLC0A0CM). Bilateral
    ig = _safe(lambda: _fred_latest("BAMLC0A0CM"))
    if ig is not None:
        if ig <= 0.85: flag = "red"
        elif ig <= 0.95: flag = "amber"
        elif ig >= 2.0: flag = "stress"
        elif ig >= 1.3: flag = "amber"
        else: flag = None
        out["ig_oas"] = {"value": round(ig, 2), "flag": flag, "suffix": None}

    # CCC - HY spread (derived from FRED BAMLH0A3HYC - BAMLH0A0HYM2)
    ccc = _safe(lambda: _fred_latest("BAMLH0A3HYC"))
    if ccc is not None and hy is not None:
        spread = ccc - hy
        # High spread = credit-tier divergence (green / contra-signal)
        flag = "green" if spread >= 6.0 else None
        suffix = "(10y max — contra)" if flag == "green" else None
        out["ccc_hy_spread"] = {"value": round(spread, 2), "flag": flag, "suffix": suffix}

    # HYG / LQD ratio
    hyg = _safe(lambda: _yf_latest("HYG"))
    lqd = _safe(lambda: _yf_latest("LQD"))
    if hyg is not None and lqd is not None:
        r = hyg / lqd
        flag = "red" if r >= 0.72 else ("amber" if r >= 0.69 else None)
        out["hyg_lqd"] = {"value": round(r, 3), "flag": flag, "suffix": "(19y high)" if r >= 0.72 else None}

    # VIX (Yahoo ^VIX)
    vix = _safe(lambda: _yf_latest("^VIX"))
    if vix is not None:
        flag = "stress" if vix >= 30 else ("amber" if vix >= 20 else None)
        out["vix"] = {"value": round(vix, 1), "flag": flag, "suffix": None}

    # SKEW (Yahoo ^SKEW). High = contra (hedges bid)
    skew = _safe(lambda: _yf_latest("^SKEW"))
    if skew is not None:
        flag = "green" if skew >= 145 else None
        out["skew"] = {"value": round(skew, 0), "flag": flag, "suffix": "(contra)" if flag == "green" else None}

    # MOVE (Yahoo ^MOVE)
    move = _safe(lambda: _yf_latest("^MOVE"))
    if move is not None:
        flag = "stress" if move >= 120 else ("amber" if move >= 100 else None)
        out["move"] = {"value": round(move, 0), "flag": flag, "suffix": None}

    # VIX9D / VIX3M slope
    vix9d = _safe(lambda: _yf_latest("^VIX9D"))
    vix3m = _safe(lambda: _yf_latest("^VIX3M"))
    if vix9d is not None and vix3m is not None:
        sl = vix9d / vix3m
        flag = "stress" if sl >= 1.5 else ("green" if sl >= 1.05 else None)
        suffix = "backwardated (contra)" if flag == "green" else ("backwardated" if sl >= 1.0 else "contango")
        out["vix_slope"] = {"value": round(sl, 2), "flag": flag, "suffix": suffix}

    return out


@indicators_bp.route("/api/bmc-today")
def api_bmc_today():
    """Returns today's value + flag for each BMC indicator. Cached for 5 min."""
    now = _time.time()
    if _BMC_TODAY_CACHE["data"] is not None and (now - _BMC_TODAY_CACHE["t"]) < _BMC_TODAY_TTL:
        return jsonify({"ok": True, "data": _BMC_TODAY_CACHE["data"], "cached": True,
                        "age_seconds": int(now - _BMC_TODAY_CACHE["t"])})
    try:
        data = _bmc_compute_today()
        _BMC_TODAY_CACHE["t"] = now
        _BMC_TODAY_CACHE["data"] = data
        return jsonify({"ok": True, "data": data, "cached": False})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@indicators_bp.route("/api/config")
def api_config():
    return jsonify({
        "categories": CATEGORIES,
        "indicators": _indicator_meta(),
    })


@indicators_bp.route("/api/snapshot")
def api_snapshot():
    ensure_fresh()
    data, fetched_at = _db.get_latest_snapshot()
    if data is None:
        return jsonify({"ok": False, "error": "No data yet — refresh in progress."}), 202
    return jsonify({
        "ok": True,
        "fetched_at": fetched_at,
        "refreshing": _refresh_in_progress,
        "data": data,
    })


@indicators_bp.route("/api/refresh", methods=["POST"])
def api_refresh():
    """Synchronous refresh — waits for fetch to complete, returns new data."""
    global _refresh_in_progress
    with _refresh_lock:
        _refresh_in_progress = True
        data = _do_refresh()
    saved, fetched_at = _db.get_latest_snapshot()
    return jsonify({
        "ok": bool(data),
        "fetched_at": fetched_at,
        "data": saved or {},
    })


@indicators_bp.route("/api/history/<ind_id>")
def api_history(ind_id: str):
    known_ids = {ind["id"] for ind in INDICATORS}
    if ind_id not in known_ids:
        abort(404)
    return jsonify(_db.get_history(ind_id))


@indicators_bp.route("/api/range-snapshot")
def api_range_snapshot():
    """Batch range-history fetch for ALL indicators at the same time range.

    Used by the dashboard-level range bar so switching 1Y → 5Y → MAX rerenders
    every sparkline from one round-trip rather than N parallel requests.
    """
    range_key = (request.args.get("range") or "1y").lower()
    data = fetch_range_snapshot(range_key)
    return jsonify({"range": range_key, "data": data})


@indicators_bp.route("/api/history-range/<ind_id>")
def api_history_range(ind_id: str):
    """On-demand fetch for the modal's range selector (1m..max).

    yfinance for ticker symbols, FRED CSV for FRED series (capped at ~3 years
    by FRED's CSV endpoint — the modal renders FRED's native PNG for the
    full-history view), components downloaded + combined for _SPREAD_ / _RATIO_.
    """
    known_ids = {ind["id"] for ind in INDICATORS}
    if ind_id not in known_ids:
        abort(404)
    range_key = (request.args.get("range") or "1y").lower()
    rows = fetch_history_range(ind_id, range_key)
    return jsonify({"range": range_key, "history": rows})


# ── DB initialisation (called by main.py) ─────────────────────────────────────

def init_db() -> None:
    _db.init_db()


# ── Standalone entry point ────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    _db.init_db()

    app = Flask(__name__, template_folder=str(SCRIPT_DIR / "templates"))
    app.register_blueprint(indicators_bp, url_prefix="/indicators")

    @app.route("/")
    def _root():
        return redirect("/indicators/")

    ensure_fresh(force=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8003)
    args = parser.parse_args()

    print(f"Indicators dashboard → http://localhost:{args.port}/indicators/")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
