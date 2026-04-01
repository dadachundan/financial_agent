#!/usr/bin/env python3
"""
pe/app.py — P/E Ratio Viewer for watchlist stocks.

Routes
------
  GET  /pe/          Main table, sortable by column
  GET  /pe/api/data  JSON: all stocks with PE data (cached 30 min)
  POST /pe/api/refresh  Force-refresh from yfinance

Standalone usage
----------------
    python pe/app.py [--port 8004]
"""

import argparse
import logging
import sys
import threading
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
_PROJECT_ROOT = SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import yfinance as yf
from flask import Blueprint, Flask, jsonify, redirect, render_template_string
from markupsafe import Markup

import nav_widget2 as nw2  # noqa: F401

log = logging.getLogger(__name__)

# ── Watchlist (from 🤪PER SECTOR.txt) ────────────────────────────────────────
# Each entry is (sector_name, [yfinance_ticker, ...])
# Exchange prefixes stripped; TSX → .TO, ASX → .AX, BRK.B → BRK-B

WATCHLIST: list[tuple[str, list[str]]] = [
    ("BIG TECH",         ["ORCL", "NFLX", "MSFT", "BRK-B", "AAPL", "NVDA", "AVGO", "AMZN",
                          "TSM",  "META", "TSLA", "GOOG",  "ASML", "AMD",  "MU"]),
    ("SEMICONDUCTORS",   ["NVTS", "ALAB", "QCOM", "TXN",   "ARM",  "GSIT", "DELL", "CRDO",
                          "APLD", "CAT",  "AMAT", "VRT",   "LRCX", "COHR", "TER",  "MRVL", "LITE"]),
    ("芯片设计公司",       ["SNPS", "CDNS"]),
    ("STORAGE",          ["STX", "SNDK", "WDC"]),
    ("ENERGY",           ["SMR",  "XOM",  "OXY",  "OKLO", "BE",   "SHEL", "UUUU",
                          "FSLR", "TLN",  "PWR",  "GEV"]),
    ("MINING",           ["USAR", "CIFR", "GMIN.TO", "B", "NEM"]),
    ("AI云服务",           ["NBIS", "DDOG", "GTLB", "MDB", "DOCN"]),
    ("网络安全",           ["PANW"]),
    ("机器人",             ["SERV", "SYM"]),
    ("教育",              ["DUOL", "LRN"]),
    ("AI",               ["SOUN", "ZETA", "BBAI", "PLTR", "SNOW", "INOD", "TEM"]),
    ("AEROSPACE/SATELLITE", ["AMPX", "HEI", "ACHR", "RTX", "VSAT", "ASTS", "HWM",
                             "ATRO", "RDW", "PL",   "BKSY"]),
    ("OTHER",            ["WYFI", "RDDT", "VST", "RMBS", "RMS.AX"]),
]

ALL_TICKERS: list[str] = [t for _, tickers in WATCHLIST for t in tickers]
SECTOR_MAP:  dict[str, str] = {t: s for s, tickers in WATCHLIST for t in tickers}

CACHE_TTL = 30 * 60  # 30 minutes

_cache_lock = threading.Lock()
_cache_data: list[dict] | None = None
_cache_ts:   float = 0.0
_refresh_in_progress = False


# ── Data fetching ─────────────────────────────────────────────────────────────

def _fetch_one(ticker: str) -> dict:
    try:
        info = yf.Ticker(ticker).info
        return {
            "ticker":      ticker,
            "name":        info.get("shortName") or info.get("longName") or ticker,
            "sector":      SECTOR_MAP.get(ticker, ""),
            "price":       info.get("currentPrice") or info.get("regularMarketPrice"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe":  info.get("forwardPE"),
            "mkt_cap":     info.get("marketCap"),
        }
    except Exception as e:
        log.warning("Failed %s: %s", ticker, e)
        return {"ticker": ticker, "name": ticker, "sector": SECTOR_MAP.get(ticker, ""),
                "price": None, "trailing_pe": None, "forward_pe": None, "mkt_cap": None}


def _fetch_all() -> list[dict]:
    log.info("Fetching PE data for %d tickers…", len(ALL_TICKERS))
    results = []
    for i, t in enumerate(ALL_TICKERS):
        results.append(_fetch_one(t))
        if i % 10 == 9:
            time.sleep(0.3)
    log.info("Done fetching PE data (%d tickers).", len(results))
    return results


def get_cached_data(force: bool = False) -> list[dict] | None:
    global _cache_data, _cache_ts, _refresh_in_progress
    with _cache_lock:
        age = time.time() - _cache_ts
        if not force and _cache_data is not None and age < CACHE_TTL:
            return _cache_data
        if _refresh_in_progress:
            return _cache_data
        _refresh_in_progress = True

    def _do():
        global _cache_data, _cache_ts, _refresh_in_progress
        data = _fetch_all()
        with _cache_lock:
            _cache_data = data
            _cache_ts = time.time()
            _refresh_in_progress = False
        log.info("Cache updated.")

    threading.Thread(target=_do, daemon=True).start()
    # Don't block — JS polls until data arrives
    return _cache_data


# ── Blueprint ─────────────────────────────────────────────────────────────────

pe_bp = Blueprint("pe", __name__, url_prefix="/pe")

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>P/E Viewer — FinAgent</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<style>
body { font-size: 13px; }
#peTable th { cursor: pointer; user-select: none; white-space: nowrap; }
#peTable th.asc::after  { content: " ▲"; font-size: 10px; opacity:.7; }
#peTable th.desc::after { content: " ▼"; font-size: 10px; opacity:.7; }
.pe-low  { color: #198754; font-weight: 600; }
.pe-mid  { color: #fd7e14; }
.pe-high { color: #dc3545; }
.pe-na   { color: #aaa; font-style: italic; }
.mkt-cap { font-size: 11px; color: #888; }
#status  { font-size: 11px; color: #888; }
.spinner-border { width: 1rem; height: 1rem; border-width: 2px; }
</style>
</head>
<body>
{{ NAV_HTML }}

<div class="container-fluid py-3">
  <div class="d-flex align-items-center gap-3 mb-3 flex-wrap">
    <h5 class="mb-0">📊 P/E Viewer</h5>
    <button class="btn btn-sm btn-outline-secondary" id="refreshBtn" onclick="doRefresh()">⟳ Refresh</button>
    <div class="form-check form-switch mb-0 ms-1">
      <input class="form-check-input" type="checkbox" id="groupChk" onchange="render()">
      <label class="form-check-label" for="groupChk">Group by sector</label>
    </div>
    <div class="form-check form-switch mb-0">
      <input class="form-check-input" type="checkbox" id="hideNaChk" onchange="render()">
      <label class="form-check-label" for="hideNaChk">Hide N/A P/E</label>
    </div>
    <span id="status"></span>
    <span id="spinner" class="spinner-border text-secondary" role="status" style="display:none"></span>
  </div>

  <table class="table table-sm table-hover table-bordered" id="peTable">
    <thead class="table-dark sticky-top">
      <tr>
        <th data-col="sector">Sector</th>
        <th data-col="ticker">Ticker</th>
        <th data-col="name">Name</th>
        <th data-col="price" class="text-end">Price</th>
        <th data-col="trailing_pe" class="text-end">Trailing P/E</th>
        <th data-col="forward_pe" class="text-end">Forward P/E</th>
        <th data-col="mkt_cap" class="text-end">Mkt Cap</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<script>
let _rows = [];
let _sortCol = 'trailing_pe';
let _sortDir = 1;
let _pollTimer = null;

function fmtPE(v) {
  if (v == null || isNaN(v)) return '<span class="pe-na">N/A</span>';
  if (v <= 0) return '<span class="pe-na">' + v.toFixed(1) + '</span>';
  const cls = v < 20 ? 'pe-low' : v < 40 ? 'pe-mid' : 'pe-high';
  return '<span class="' + cls + '">' + v.toFixed(1) + '</span>';
}
function fmtPrice(v) {
  if (v == null) return '—';
  return '$' + Number(v).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
}
function fmtCap(v) {
  if (v == null) return '—';
  if (v >= 1e12) return (v/1e12).toFixed(2) + 'T';
  if (v >= 1e9)  return (v/1e9).toFixed(1)  + 'B';
  if (v >= 1e6)  return (v/1e6).toFixed(0)  + 'M';
  return v;
}

function sortKey(r) {
  const v = r[_sortCol];
  if (v == null) return _sortDir === 1 ? Infinity : -Infinity;
  return v;
}
function cmp(a, b) {
  const av = sortKey(a), bv = sortKey(b);
  if (typeof av === 'string') return av.localeCompare(bv) * _sortDir;
  return (av - bv) * _sortDir;
}

function rowHtml(r, showSector) {
  return `<tr>
    <td>${showSector ? r.sector : ''}</td>
    <td><strong>${r.ticker}</strong></td>
    <td>${r.name}</td>
    <td class="text-end">${fmtPrice(r.price)}</td>
    <td class="text-end">${fmtPE(r.trailing_pe)}</td>
    <td class="text-end">${fmtPE(r.forward_pe)}</td>
    <td class="text-end mkt-cap">${fmtCap(r.mkt_cap)}</td>
  </tr>`;
}

function render() {
  const grouped = document.getElementById('groupChk').checked;
  const hideNa  = document.getElementById('hideNaChk').checked;
  let rows = hideNa ? _rows.filter(r => r.trailing_pe > 0) : [..._rows];

  document.querySelectorAll('#peTable thead th').forEach(th => {
    th.classList.remove('asc', 'desc');
    if (th.dataset.col === _sortCol) th.classList.add(_sortDir === 1 ? 'asc' : 'desc');
  });

  let html = '';
  if (grouped) {
    const seen = new Set(), sectorOrder = [];
    _rows.forEach(r => { if (!seen.has(r.sector)) { seen.add(r.sector); sectorOrder.push(r.sector); } });
    for (const sec of sectorOrder) {
      const grp = rows.filter(r => r.sector === sec).sort(cmp);
      if (!grp.length) continue;
      html += `<tr class="table-secondary"><td colspan="7"><strong>${sec}</strong></td></tr>`;
      html += grp.map(r => rowHtml(r, false)).join('');
    }
  } else {
    html = rows.sort(cmp).map(r => rowHtml(r, true)).join('');
  }
  document.getElementById('tbody').innerHTML = html;
}

document.querySelectorAll('#peTable thead th').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.col;
    if (_sortCol === col) _sortDir *= -1;
    else { _sortCol = col; _sortDir = 1; }
    render();
  });
});

function setStatus(json) {
  const age = json.age_minutes != null ? json.age_minutes.toFixed(0) + ' min ago' : 'just now';
  document.getElementById('status').textContent =
    json.data.length + ' stocks · updated ' + age;
  document.getElementById('spinner').style.display = json.refreshing ? '' : 'none';
  document.getElementById('refreshBtn').disabled = false;
}

async function loadData(force) {
  const url    = force ? '/pe/api/refresh' : '/pe/api/data';
  const method = force ? 'POST' : 'GET';
  try {
    const res  = await fetch(url, {method});
    const json = await res.json();
    _rows = json.data || [];
    setStatus(json);
    if (_rows.length > 0) render();

    // Poll every 4s while a background refresh is running
    clearTimeout(_pollTimer);
    if (json.refreshing) {
      _pollTimer = setTimeout(() => loadData(false), 4000);
    }
  } catch(e) {
    document.getElementById('status').textContent = 'Error: ' + e;
  }
}

function doRefresh() {
  document.getElementById('refreshBtn').disabled = true;
  document.getElementById('spinner').style.display = '';
  document.getElementById('status').textContent = 'Refreshing…';
  loadData(true);
}

// Kick off initial load; if refreshing, polling will continue automatically
loadData(false);
</script>
</body>
</html>
"""


@pe_bp.route("/")
@pe_bp.route("")
def index():
    return render_template_string(TEMPLATE, NAV_HTML=Markup(nw2.NAV_HTML))


@pe_bp.route("/api/data")
def api_data():
    data = get_cached_data()
    age = (time.time() - _cache_ts) / 60 if _cache_ts else None
    return jsonify({"data": data or [], "age_minutes": age, "refreshing": _refresh_in_progress})


@pe_bp.route("/api/refresh", methods=["POST"])
def api_refresh():
    data = get_cached_data(force=True)
    age = (time.time() - _cache_ts) / 60 if _cache_ts else None
    return jsonify({"data": data or [], "age_minutes": age, "refreshing": _refresh_in_progress})


# ── Standalone ────────────────────────────────────────────────────────────────

def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(pe_bp)

    @app.route("/")
    def root():
        return redirect("/pe/")

    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8004)
    args = parser.parse_args()
    create_app().run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
