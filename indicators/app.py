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
# nav_widget2, minimax, etc. are importable when running standalone.
_PROJECT_ROOT = SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from flask import Blueprint, Flask, abort, jsonify, render_template, redirect

import nav_widget2 as nw2  # noqa: F401  (NAV_HTML used in template)
import indicators.db as _db
from indicators.data_fetcher import CATEGORIES, INDICATORS, fetch_all

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
        )
        for ind in INDICATORS
    ]


# ── Routes ────────────────────────────────────────────────────────────────────

@indicators_bp.route("/")
def dashboard():
    ensure_fresh()
    return render_template(
        "indicators.html",
        nav=nw2.NAV_HTML,
        _base="/indicators",
    )


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
