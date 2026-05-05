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
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
_PROJECT_ROOT = SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import yfinance as yf
from flask import Blueprint, Flask, jsonify, redirect, render_template_string
from markupsafe import Markup

import json
import re as _re

import nav_widget2 as nw2  # noqa: F401

log = logging.getLogger(__name__)

# Load Chinese name cache directly (ignore freshness — names don't change often)
_CN_NAME_MAP: dict = {}
_CACHE_FILE = _PROJECT_ROOT / "ticker_name_cache.json"
if _CACHE_FILE.exists():
    try:
        _CN_NAME_MAP = json.loads(_CACHE_FILE.read_text(encoding="utf-8"))
        log.info("Loaded %d Chinese ticker names from cache", len(_CN_NAME_MAP))
    except Exception as _e:
        log.warning("Could not load ticker name cache: %s", _e)

_SUFFIX_RE = _re.compile(r"\.(SZ|SS|SH|HK|KS|KP|TW|US)$", _re.IGNORECASE)


def _cn_name(ticker: str) -> str | None:
    code = _SUFFIX_RE.sub("", ticker.strip())
    return _CN_NAME_MAP.get(code) or _CN_NAME_MAP.get(code.lstrip("0") or code) or None

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
    ("HK EXCHANGE",  ["2533.HK", "6600.HK", "9880.HK", "2590.HK", "9660.HK",
                      "981.HK", "100.HK", "6082.HK", "2513.HK"]),
    ("CN-GPU",       ["002837.SZ", "688256.SS", "688802.SS", "688041.SS", "688795.SS", "300308.SZ"]),
    ("CN-AI",        ["002472.SZ", "688169.SS", "301018.SZ", "603486.SS", "603019.SS", "300383.SZ"]),
    ("机器人相关",    ["688017.SS", "601689.SS", "601100.SS", "300124.SZ", "002050.SZ"]),
    ("TRADITIONAL",  ["600519.SS", "ZIJMF"]),
    ("美股上市",      ["HSAI", "BYDDF", "PONY", "WRD", "BIDU", "BABA"]),
    ("CN-OTHERS",    ["000338.SZ", "300751.SZ", "688008.SS", "688347.SS"]),
]

ALL_TICKERS: list[str] = [t for _, tickers in WATCHLIST for t in tickers]
SECTOR_MAP:  dict[str, str] = {t: s for s, tickers in WATCHLIST for t in tickers}

CACHE_TTL = 30 * 60  # 30 minutes

_cache_lock = threading.Lock()
_cache_data: list[dict] | None = None
_cache_ts:   float = 0.0
_refresh_in_progress = False


# ── Data fetching ─────────────────────────────────────────────────────────────

def _exchange_of(ticker: str) -> str:
    t = ticker.upper()
    if t.endswith(".HK"):
        return "HK"
    if t.endswith(".SZ") or t.endswith(".SS"):
        return "CN"
    if t.endswith(".TO") or t.endswith(".AX"):
        return "Other"
    return "US"


def _batch_history(tickers: list[str]) -> dict:
    """Batch-download 1-year daily close prices. Returns {ticker: pd.Series | None}."""
    result: dict = {}
    BATCH = 50
    for i in range(0, len(tickers), BATCH):
        batch = tickers[i : i + BATCH]
        try:
            raw = yf.download(
                batch, period="1y", interval="1d",
                auto_adjust=True, threads=True, progress=False,
            )
            if raw.empty:
                continue
            close = raw["Close"]  # always a DataFrame in yfinance 0.2+
            for ticker in batch:
                try:
                    s = close[ticker].dropna()
                    result[ticker] = s if len(s) > 0 else None
                except (KeyError, TypeError):
                    result[ticker] = None
        except Exception as e:
            log.warning("History batch failed (i=%d): %s", i, e)
    return result


def _fetch_one(ticker: str, hist=None) -> dict:
    try:
        info = yf.Ticker(ticker).info
        en_name = info.get("shortName") or info.get("longName") or ticker

        day_change = week_change = month_change = year_change = None
        if hist is not None and len(hist) >= 2:
            cur = float(hist.iloc[-1])
            prev = float(hist.iloc[-2])
            if prev:
                day_change = cur / prev - 1
            if len(hist) >= 6:
                week_change = cur / float(hist.iloc[-6]) - 1
            if len(hist) >= 22:
                month_change = cur / float(hist.iloc[-22]) - 1
            year_change = cur / float(hist.iloc[0]) - 1

        earnings_ts = info.get("earningsTimestamp") or info.get("earningsTimestampStart")

        return {
            "ticker":           ticker,
            "name":             en_name,
            "name_cn":          _cn_name(ticker),
            "sector":           SECTOR_MAP.get(ticker, ""),
            "exchange":         _exchange_of(ticker),
            "price":            info.get("currentPrice") or info.get("regularMarketPrice"),
            "trailing_pe":      info.get("trailingPE"),
            "forward_pe":       info.get("forwardPE"),
            "mkt_cap":          info.get("marketCap"),
            "rev_growth":       info.get("revenueGrowth"),
            "earn_growth":      info.get("earningsGrowth"),
            "gross_margin":     info.get("grossMargins"),
            "op_margin":        info.get("operatingMargins"),
            "net_margin":       info.get("profitMargins"),
            "day_change":       day_change,
            "week_change":      week_change,
            "month_change":     month_change,
            "year_change":      year_change,
            "earnings_ts":      earnings_ts,
        }
    except Exception as e:
        log.warning("Failed %s: %s", ticker, e)
        return {"ticker": ticker, "name": ticker, "name_cn": _cn_name(ticker),
                "sector": SECTOR_MAP.get(ticker, ""), "exchange": _exchange_of(ticker),
                "price": None, "trailing_pe": None, "forward_pe": None, "mkt_cap": None,
                "rev_growth": None, "earn_growth": None,
                "gross_margin": None, "op_margin": None, "net_margin": None,
                "day_change": None, "week_change": None, "month_change": None,
                "year_change": None, "earnings_ts": None}


def _fetch_all() -> list[dict]:
    log.info("Fetching PE data for %d tickers…", len(ALL_TICKERS))
    log.info("Downloading 1-year price history…")
    hist_map = _batch_history(ALL_TICKERS)
    log.info("History downloaded for %d/%d tickers.", len(hist_map), len(ALL_TICKERS))
    results = []
    for i, t in enumerate(ALL_TICKERS):
        results.append(_fetch_one(t, hist_map.get(t)))
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

# Pre-warm cache on import so data is ready before first page visit
threading.Thread(target=lambda: get_cached_data(), daemon=True).start()

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>P/E Viewer — FinAgent</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<script src="/static/vendor/bootstrap.bundle.min.js"></script>
<script src="/static/vendor/chart.umd.min.js"></script>
<script src="/static/vendor/chartjs-plugin-datalabels.min.js"></script>
<script src="/static/vendor/hammerjs.min.js"></script>
<script src="/static/vendor/chartjs-plugin-zoom.min.js"></script>
<style>
body { font-size: 13px; }
.table-wrap { overflow-x: auto; }
#peTable th { cursor: pointer; user-select: none; white-space: nowrap; }
#peTable th.asc::after  { content: " ▲"; font-size: 10px; opacity:.7; }
#peTable th.desc::after { content: " ▼"; font-size: 10px; opacity:.7; }
.pe-low  { color: #198754; font-weight: 600; }
.pe-mid  { color: #fd7e14; }
.pe-high { color: #dc3545; }
.pe-na   { color: #aaa; font-style: italic; }
.g-pos   { color: #198754; font-weight: 600; }
.g-neg   { color: #dc3545; }
.g-na    { color: #aaa; font-style: italic; }
.m-high  { color: #198754; font-weight: 600; }
.m-mid   { color: #fd7e14; }
.m-low   { color: #dc3545; }
.m-na    { color: #aaa; font-style: italic; }
#peTable th.grp-start, #peTable td.grp-start { border-left: 2px solid #555 !important; }
.small-col { font-size: 11px; color: #888; }
#status { font-size: 11px; color: #888; }
.spinner-border { width: 1rem; height: 1rem; border-width: 2px; }
thead.table-dark th { position: sticky; top: 0; z-index: 2; }
thead tr.subhdr th { background: #2c2c3e; font-size: 10px; font-weight: 400;
                     text-transform: uppercase; letter-spacing: .05em;
                     color: #aaa; padding: 2px 4px; position: sticky; top: 24px; z-index: 2; }
/* Chart */
#chartWrap { background: #fff; border-radius: 6px; padding: 12px; margin-bottom: 20px; }
#chartWrap canvas { display: block; }
/* Earnings filter */
.earnings-btn.active { background-color: #0d6efd; color: #fff; border-color: #0d6efd; }
</style>
</head>
<body>
{{ NAV_HTML }}

<div class="container-fluid py-3">
  <!-- toolbar -->
  <div class="d-flex align-items-center gap-3 mb-3 flex-wrap">
    <h5 class="mb-0">📊 P/E Viewer</h5>
    <button class="btn btn-sm btn-outline-secondary" id="refreshBtn" onclick="doRefresh()">⟳ Refresh</button>
    <div class="form-check form-switch mb-0 ms-1">
      <input class="form-check-input" type="checkbox" id="groupChk" onchange="renderTable()">
      <label class="form-check-label" for="groupChk">Group by sector</label>
    </div>
    <div class="form-check form-switch mb-0">
      <input class="form-check-input" type="checkbox" id="hideNaChk" onchange="renderTable()">
      <label class="form-check-label" for="hideNaChk">Hide N/A P/E</label>
    </div>
    <span id="status"></span>
    <span id="spinner" class="spinner-border text-secondary" role="status" style="display:none"></span>
  </div>

  <!-- earnings filter -->
  <div class="mb-2 d-flex flex-wrap align-items-center gap-2">
    <span class="text-muted small fw-bold">EARNINGS:</span>
    <div class="btn-group btn-group-sm">
      <button class="btn btn-outline-secondary earnings-btn active" data-filter="all"       onclick="setEarningsFilter('all')">All</button>
      <button class="btn btn-outline-secondary earnings-btn"        data-filter="today"     onclick="setEarningsFilter('today')">Today</button>
      <button class="btn btn-outline-secondary earnings-btn"        data-filter="tomorrow"  onclick="setEarningsFilter('tomorrow')">Tomorrow</button>
      <button class="btn btn-outline-secondary earnings-btn"        data-filter="yesterday" onclick="setEarningsFilter('yesterday')">Yesterday</button>
      <button class="btn btn-outline-secondary earnings-btn"        data-filter="last_week" onclick="setEarningsFilter('last_week')">Last Week</button>
      <button class="btn btn-outline-secondary earnings-btn"        data-filter="last_month" onclick="setEarningsFilter('last_month')">Last Month</button>
    </div>
  </div>

  <!-- filters -->
  <div class="mb-2 d-flex flex-wrap align-items-center gap-3" id="filterBar">
    <span class="text-muted small fw-bold">EXCHANGE:</span>
    <div class="dropdown" id="exchangeDropdownWrap">
      <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button"
              id="exchangeDropBtn" data-bs-toggle="dropdown" data-bs-auto-close="outside"
              aria-expanded="false">All exchanges</button>
      <div class="dropdown-menu p-2" style="min-width:180px" id="exchangeMenu">
        <div class="d-flex gap-2 mb-2">
          <button class="btn btn-xs btn-link p-0 text-decoration-none small" onclick="selectAllExchanges()">All</button>
          <button class="btn btn-xs btn-link p-0 text-decoration-none small" onclick="clearAllExchanges()">None</button>
        </div>
        <div id="exchangeCheckboxes"></div>
      </div>
    </div>
    <span class="text-muted small fw-bold ms-2">SECTOR:</span>
    <div class="dropdown" id="sectorDropdownWrap">
      <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button"
              id="sectorDropBtn" data-bs-toggle="dropdown" data-bs-auto-close="outside"
              aria-expanded="false">All sectors</button>
      <div class="dropdown-menu p-2" style="min-width:200px;max-height:320px;overflow-y:auto" id="sectorMenu">
        <div class="d-flex gap-2 mb-2">
          <button class="btn btn-xs btn-link p-0 text-decoration-none small" onclick="selectAllSectors()">All</button>
          <button class="btn btn-xs btn-link p-0 text-decoration-none small" onclick="clearAllSectors()">None</button>
        </div>
        <div id="sectorCheckboxes"></div>
      </div>
    </div>
    <span class="text-muted small fw-bold ms-2">MKT CAP:</span>
    <div class="d-flex align-items-center gap-1">
      <span class="text-muted small">Min</span>
      <input type="number" id="capMin" class="form-control form-control-sm" style="width:80px" placeholder="0" min="0" oninput="applyFilters()">
      <span class="text-muted small">B</span>
      <span class="text-muted small ms-1">Max</span>
      <input type="number" id="capMax" class="form-control form-control-sm" style="width:80px" placeholder="∞" min="0" oninput="applyFilters()">
      <span class="text-muted small">B</span>
    </div>
  </div>

  <!-- bubble chart -->
  <div id="chartWrap">
    <div class="d-flex justify-content-end mb-1 gap-2">
      <span class="text-muted small align-self-center">Scroll to zoom · Drag to pan</span>
      <button class="btn btn-xs btn-outline-secondary btn-sm" onclick="resetZoom()" style="font-size:11px;padding:2px 8px">Reset zoom</button>
    </div>
    <canvas id="peChart"></canvas>
  </div>
  <div id="chartExcluded" class="text-muted small mb-2" style="display:none"></div>

  <!-- table -->
  <div class="table-wrap">
  <table class="table table-sm table-hover table-bordered" id="peTable">
    <thead class="table-dark">
      <tr>
        <th rowspan="2" data-col="sector">Sector</th>
        <th rowspan="2" data-col="ticker">Ticker</th>
        <th rowspan="2" data-col="name">Name</th>
        <th rowspan="2" data-col="price" class="text-end">Price</th>
        <th rowspan="2" data-col="mkt_cap" class="text-end">Mkt Cap</th>
        <th colspan="2" class="text-center grp-start">Valuation</th>
        <th colspan="2" class="text-center grp-start">Growth (TTM YoY)</th>
        <th colspan="3" class="text-center grp-start">Margins (TTM)</th>
        <th colspan="4" class="text-center grp-start">Price Change</th>
        <th rowspan="2" data-col="earnings_ts" class="text-center grp-start">Earnings Date</th>
      </tr>
      <tr class="subhdr">
        <th data-col="trailing_pe" class="text-end grp-start">Trailing P/E</th>
        <th data-col="forward_pe"  class="text-end">Forward P/E</th>
        <th data-col="rev_growth"   class="text-end grp-start">Revenue</th>
        <th data-col="earn_growth"  class="text-end">Earnings</th>
        <th data-col="gross_margin" class="text-end grp-start">Gross</th>
        <th data-col="op_margin"    class="text-end">Operating</th>
        <th data-col="net_margin"   class="text-end">Net</th>
        <th data-col="day_change"   class="text-end grp-start">Day</th>
        <th data-col="week_change"  class="text-end">Week</th>
        <th data-col="month_change" class="text-end">Month</th>
        <th data-col="year_change"  class="text-end">Year</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>
  </div>
</div>

<script>
let _rows = [];
let _sortCol = 'trailing_pe';
let _sortDir = 1;
let _pollTimer = null;
let _chart = null;
let _hiddenSectors = new Set();
let _hiddenExchanges = new Set();
let _earningsFilter = 'all';

const EXCHANGE_LABELS = { US: '🇺🇸 U.S.', HK: '🇭🇰 Hong Kong', CN: '🇨🇳 Mainland China', Other: '🌐 Other' };
const EXCHANGE_ORDER  = ['US', 'HK', 'CN', 'Other'];

/* ── earnings filter ── */
function setEarningsFilter(f) {
  _earningsFilter = f;
  document.querySelectorAll('.earnings-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === f);
  });
  renderTable();
}

/* ── filtering ── */
function filteredRows() {
  const capMin = parseFloat(document.getElementById('capMin').value) || 0;
  const capMax = parseFloat(document.getElementById('capMax').value) || Infinity;
  const now = Math.floor(Date.now() / 1000);
  const todayStart = Math.floor(new Date().setHours(0,0,0,0) / 1000);
  const yesterdayStart = todayStart - 86400;
  const tomorrowStart = todayStart + 86400;
  const dayAfterTomorrow = todayStart + 86400 * 2;
  const weekAgoStart = todayStart - 86400 * 7;
  const monthAgoStart = todayStart - 86400 * 30;

  return _rows.filter(r => {
    if (_hiddenSectors.has(r.sector)) return false;
    if (_hiddenExchanges.has(r.exchange || 'US')) return false;
    const cap = r.mkt_cap ? r.mkt_cap / 1e9 : 0;
    if (cap < capMin || cap > capMax) return false;
    if (_earningsFilter !== 'all') {
      const ets = r.earnings_ts;
      if (ets == null) return false;
      if (_earningsFilter === 'today'      && !(ets >= todayStart     && ets < tomorrowStart))    return false;
      if (_earningsFilter === 'tomorrow'   && !(ets >= tomorrowStart  && ets < dayAfterTomorrow)) return false;
      if (_earningsFilter === 'yesterday'  && !(ets >= yesterdayStart && ets < todayStart))       return false;
      if (_earningsFilter === 'last_week'  && !(ets >= weekAgoStart   && ets < todayStart))       return false;
      if (_earningsFilter === 'last_month' && !(ets >= monthAgoStart  && ets < weekAgoStart))     return false;
    }
    return true;
  });
}

/* ── exchange dropdown ── */
function buildExchangeDropdown() {
  const presentExchanges = [...new Set(_rows.map(r => r.exchange || 'US'))];
  const ordered = EXCHANGE_ORDER.filter(e => presentExchanges.includes(e));
  const wrap = document.getElementById('exchangeCheckboxes');
  wrap.innerHTML = '';
  ordered.forEach(ex => {
    const id = 'ex_' + ex;
    const div = document.createElement('div');
    div.className = 'form-check';
    div.innerHTML = `
      <input class="form-check-input" type="checkbox" id="${id}" checked
             onchange="toggleExchange('${ex}', this.checked)">
      <label class="form-check-label" for="${id}" style="font-size:12px">${EXCHANGE_LABELS[ex] || ex}</label>`;
    wrap.appendChild(div);
  });
  updateExchangeDropdownLabel();
}

function toggleExchange(ex, checked) {
  if (checked) _hiddenExchanges.delete(ex);
  else         _hiddenExchanges.add(ex);
  updateExchangeDropdownLabel();
  applyFilters();
}

function updateExchangeDropdownLabel() {
  const presentExchanges = [...new Set(_rows.map(r => r.exchange || 'US'))];
  const total  = presentExchanges.length;
  const hidden = presentExchanges.filter(e => _hiddenExchanges.has(e)).length;
  const shown  = total - hidden;
  const btn = document.getElementById('exchangeDropBtn');
  btn.textContent = hidden === 0 ? 'All exchanges'
    : shown === 0 ? 'No exchanges'
    : shown + ' / ' + total + ' exchanges';
}

function selectAllExchanges() {
  _hiddenExchanges.clear();
  document.querySelectorAll('#exchangeCheckboxes .form-check-input').forEach(cb => cb.checked = true);
  updateExchangeDropdownLabel();
  applyFilters();
}

function clearAllExchanges() {
  [...new Set(_rows.map(r => r.exchange || 'US'))].forEach(e => _hiddenExchanges.add(e));
  document.querySelectorAll('#exchangeCheckboxes .form-check-input').forEach(cb => cb.checked = false);
  updateExchangeDropdownLabel();
  applyFilters();
}

function applyFilters() {
  renderChart();
  renderTable();
}

function updateDropdownLabel() {
  const total   = [...new Set(_rows.map(r => r.sector))].length;
  const hidden  = _hiddenSectors.size;
  const shown   = total - hidden;
  const btn = document.getElementById('sectorDropBtn');
  btn.textContent = hidden === 0 ? 'All sectors'
    : shown === 0 ? 'No sectors'
    : shown + ' / ' + total + ' sectors';
}

function buildSectorDropdown() {
  const sectors = [...new Set(_rows.map(r => r.sector))].sort();
  const wrap = document.getElementById('sectorCheckboxes');
  wrap.innerHTML = '';
  sectors.forEach(sec => {
    const color = sectorColor(sec);
    const id = 'sec_' + sec.replace(/[^a-z0-9]/gi, '_');
    const div = document.createElement('div');
    div.className = 'form-check';
    div.innerHTML = `
      <input class="form-check-input" type="checkbox" id="${id}" checked
             onchange="toggleSector('${sec.replace(/'/g,"\\'")}', this.checked)">
      <label class="form-check-label d-flex align-items-center gap-1" for="${id}" style="font-size:12px">
        <span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:${color};flex-shrink:0"></span>
        ${sec}
      </label>`;
    wrap.appendChild(div);
  });
  updateDropdownLabel();
}

function toggleSector(sec, checked) {
  if (checked) _hiddenSectors.delete(sec);
  else         _hiddenSectors.add(sec);
  updateDropdownLabel();
  applyFilters();
}

function selectAllSectors() {
  _hiddenSectors.clear();
  document.querySelectorAll('#sectorCheckboxes .form-check-input').forEach(cb => cb.checked = true);
  updateDropdownLabel();
  applyFilters();
}

function clearAllSectors() {
  [...new Set(_rows.map(r => r.sector))].forEach(s => _hiddenSectors.add(s));
  document.querySelectorAll('#sectorCheckboxes .form-check-input').forEach(cb => cb.checked = false);
  updateDropdownLabel();
  applyFilters();
}

/* ── sector colours ── */
const SECTOR_COLORS = [
  '#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f',
  '#edc948','#b07aa1','#ff9da7','#9c755f','#bab0ac',
  '#00b7c3','#ff6e54','#ffa600','#665191','#a05195',
];
const _sectorColorMap = {};
function sectorColor(s) {
  if (!_sectorColorMap[s]) {
    const idx = Object.keys(_sectorColorMap).length % SECTOR_COLORS.length;
    _sectorColorMap[s] = SECTOR_COLORS[idx];
  }
  return _sectorColorMap[s];
}

/* ── formatters ── */
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
function fmtPct(v) {
  if (v == null || isNaN(v)) return 'N/A';
  return (v >= 0 ? '+' : '') + (v * 100).toFixed(1) + '%';
}
function fmtGrowth(v) {
  if (v == null || isNaN(v)) return '<span class="g-na">N/A</span>';
  const cls = v >= 0 ? 'g-pos' : 'g-neg';
  return '<span class="' + cls + '">' + fmtPct(v) + '</span>';
}
function fmtMargin(v) {
  if (v == null || isNaN(v)) return '<span class="m-na">N/A</span>';
  const cls = v >= 0.3 ? 'm-high' : v >= 0.1 ? 'm-mid' : 'm-low';
  return '<span class="' + cls + '">' + (v*100).toFixed(1) + '%</span>';
}
function fmtChg(v) {
  if (v == null || isNaN(v)) return '<span class="g-na">—</span>';
  const cls = v >= 0 ? 'g-pos' : 'g-neg';
  return '<span class="' + cls + '">' + (v >= 0 ? '+' : '') + (v * 100).toFixed(1) + '%</span>';
}
function fmtEarningsDate(ts) {
  if (ts == null) return '<span class="g-na">—</span>';
  const d = new Date(ts * 1000);
  const today = new Date(); today.setHours(0,0,0,0);
  const diff = Math.round((d - today) / 86400000);
  const label = d.toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'});
  let badge = '';
  if (diff === 0)  badge = ' <span class="badge bg-warning text-dark" style="font-size:10px">Today</span>';
  else if (diff === 1)  badge = ' <span class="badge bg-info text-dark" style="font-size:10px">Tomorrow</span>';
  else if (diff === -1) badge = ' <span class="badge bg-secondary" style="font-size:10px">Yesterday</span>';
  else if (diff > 0 && diff <= 7)  badge = ' <span class="badge bg-light text-dark border" style="font-size:10px">In ' + diff + 'd</span>';
  return '<span style="white-space:nowrap;font-size:11px">' + label + badge + '</span>';
}

/* ── bubble chart ── */
function bubbleRadius(mkt_cap) {
  if (!mkt_cap) return 4;
  // sqrt scaling capped at 20px to reduce overlap
  return Math.max(4, Math.min(20, Math.sqrt(mkt_cap / 1e9) * 0.9));
}

function renderChart() {
  const all = filteredRows().filter(r => r.trailing_pe > 0 && r.forward_pe > 0);
  // Compute IQR-based cap for both axes: exclude points > Q3 + 3*IQR
  function iqrCap(vals) {
    const s = [...vals].sort((a,b) => a-b);
    const q1 = s[Math.floor(s.length * 0.25)];
    const q3 = s[Math.floor(s.length * 0.75)];
    return q3 + 3 * (q3 - q1);
  }
  const capX = iqrCap(all.map(r => r.trailing_pe));
  const capY = iqrCap(all.map(r => r.forward_pe));
  const pts = all.filter(r => r.trailing_pe <= capX && r.forward_pe <= capY);
  const excluded = all.filter(r => r.trailing_pe > capX || r.forward_pe > capY).map(r => r.ticker);
  const excNote = document.getElementById('chartExcluded');
  if (excluded.length) {
    excNote.textContent = 'Outliers excluded from chart: ' + excluded.join(', ');
    excNote.style.display = '';
  } else { excNote.style.display = 'none'; }

  // Group by sector for separate datasets (enables legend by sector)
  const sectors = [...new Set(pts.map(r => r.sector))].sort();
  const datasets = sectors.map(sec => {
    const color = sectorColor(sec);
    return {
      label: sec,
      data: pts.filter(r => r.sector === sec).map(r => ({
        x: r.trailing_pe,
        y: r.forward_pe,
        r: bubbleRadius(r.mkt_cap),
        _row: r,
      })),
      backgroundColor: color + 'aa',
      borderColor:     color,
      borderWidth: 1,
    };
  });

  const cfg = {
    type: 'bubble',
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 2.2,
      plugins: {
        legend: {
          position: 'right',
          labels: { boxWidth: 12, font: { size: 11 } },
        },
        tooltip: {
          callbacks: {
            title: (items) => {
              const r = items[0].raw._row;
              const isCN = (r.exchange === 'HK' || r.exchange === 'CN') && r.name_cn;
              return r.ticker + ' — ' + (isCN ? r.name_cn + ' (' + r.name + ')' : r.name);
            },
            label: (item) => {
              const r = item.raw._row;
              return [
                'Sector: ' + r.sector,
                'Price: ' + fmtPrice(r.price) + '   Mkt Cap: ' + fmtCap(r.mkt_cap),
                'Trailing P/E: ' + (r.trailing_pe ? r.trailing_pe.toFixed(1) : 'N/A') +
                  '   Forward P/E: ' + (r.forward_pe ? r.forward_pe.toFixed(1) : 'N/A'),
                'Rev Growth: ' + fmtPct(r.rev_growth) + '   Earn Growth: ' + fmtPct(r.earn_growth),
                'Gross: ' + (r.gross_margin != null ? (r.gross_margin*100).toFixed(1)+'%' : 'N/A') +
                  '   Op: ' + (r.op_margin != null ? (r.op_margin*100).toFixed(1)+'%' : 'N/A') +
                  '   Net: ' + (r.net_margin != null ? (r.net_margin*100).toFixed(1)+'%' : 'N/A'),
              ];
            },
          },
          backgroundColor: 'rgba(0,0,0,0.85)',
          padding: 10,
          titleFont: { size: 13, weight: 'bold' },
          bodyFont: { size: 11 },
        },
        zoom: {
          zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' },
          pan:  { enabled: true, mode: 'xy' },
        },
        datalabels: {
          formatter: (val) => {
            const r = val._row;
            const isCN = (r.exchange === 'HK' || r.exchange === 'CN') && r.name_cn;
            if (pts.length <= 15) {
              const sub = isCN ? r.name_cn
                : (r.name.length > 20 ? r.name.slice(0, 18) + '\u2026' : r.name);
              return r.ticker + '\\n' + sub;
            }
            return isCN ? r.name_cn : r.ticker;
          },
          font: (ctx) => ({ size: pts.length <= 15 ? 10 : 9, weight: 'bold' }),
          color: (ctx) => ctx.dataset.data[ctx.dataIndex].r >= 12 ? '#222' : ctx.dataset.borderColor,
          anchor: (ctx) => ctx.dataset.data[ctx.dataIndex].r >= 12 ? 'center' : 'end',
          align:  (ctx) => ctx.dataset.data[ctx.dataIndex].r >= 12 ? 'center' : 'end',
          offset: (ctx) => ctx.dataset.data[ctx.dataIndex].r >= 12 ? 0 : 4,
          clip: false,
          display: (ctx) => pts.length <= 15 || ctx.dataset.data[ctx.dataIndex].r >= 7,
        },
      },
      scales: {
        x: {
          title: { display: true, text: 'Trailing P/E', font: { size: 12, weight: 'bold' } },
          grid: { color: '#e5e5e5' },
          ticks: { maxTicksLimit: 12 },
        },
        y: {
          title: { display: true, text: 'Forward P/E', font: { size: 12, weight: 'bold' } },
          grid: { color: '#e5e5e5' },
          ticks: { maxTicksLimit: 10 },
        },
      },
    },
    plugins: [ChartDataLabels, ChartZoom],
  };

  if (_chart) {
    // Update data in-place so zoom/pan state is preserved
    _chart.data.datasets = datasets;
    _chart.update('none');
  } else {
    const canvas = document.getElementById('peChart');
    _chart = new Chart(canvas, cfg);
  }
}

function resetZoom() { if (_chart) _chart.resetZoom(); }

/* ── table sort ── */
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
function nameHtml(r) {
  const isBilingual = (r.exchange === 'HK' || r.exchange === 'CN') && r.name_cn;
  if (isBilingual) {
    return `<span style="font-weight:500">${r.name_cn}</span><br><span style="font-size:11px;color:#888">${r.name}</span>`;
  }
  return r.name;
}
function rowHtml(r, showSector) {
  return `<tr>
    <td>${showSector ? r.sector : ''}</td>
    <td><strong>${r.ticker}</strong></td>
    <td>${nameHtml(r)}</td>
    <td class="text-end">${fmtPrice(r.price)}</td>
    <td class="text-end small-col">${fmtCap(r.mkt_cap)}</td>
    <td class="text-end grp-start">${fmtPE(r.trailing_pe)}</td>
    <td class="text-end">${fmtPE(r.forward_pe)}</td>
    <td class="text-end grp-start">${fmtGrowth(r.rev_growth)}</td>
    <td class="text-end">${fmtGrowth(r.earn_growth)}</td>
    <td class="text-end grp-start">${fmtMargin(r.gross_margin)}</td>
    <td class="text-end">${fmtMargin(r.op_margin)}</td>
    <td class="text-end">${fmtMargin(r.net_margin)}</td>
    <td class="text-end grp-start">${fmtChg(r.day_change)}</td>
    <td class="text-end">${fmtChg(r.week_change)}</td>
    <td class="text-end">${fmtChg(r.month_change)}</td>
    <td class="text-end">${fmtChg(r.year_change)}</td>
    <td class="text-center grp-start">${fmtEarningsDate(r.earnings_ts)}</td>
  </tr>`;
}
function renderTable() {
  const grouped = document.getElementById('groupChk').checked;
  const hideNa  = document.getElementById('hideNaChk').checked;
  let rows = filteredRows();
  if (hideNa) rows = rows.filter(r => r.trailing_pe > 0);

  document.querySelectorAll('#peTable th[data-col]').forEach(th => {
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
      html += `<tr class="table-secondary"><td colspan="17"><strong>${sec}</strong></td></tr>`;
      html += grp.map(r => rowHtml(r, false)).join('');
    }
  } else {
    html = rows.sort(cmp).map(r => rowHtml(r, true)).join('');
  }
  document.getElementById('tbody').innerHTML = html;
}

document.querySelectorAll('#peTable th[data-col]').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.col;
    if (_sortCol === col) _sortDir *= -1;
    else { _sortCol = col; _sortDir = 1; }
    renderTable();
  });
});

/* ── data loading ── */
function setStatus(json) {
  const age = json.age_minutes != null ? json.age_minutes.toFixed(0) + ' min ago' : 'just now';
  document.getElementById('status').textContent = json.data.length + ' stocks · updated ' + age;
  document.getElementById('spinner').style.display = json.refreshing ? '' : 'none';
  document.getElementById('refreshBtn').disabled = false;
}

async function loadData(force) {
  const url = force ? '/pe/api/refresh' : '/pe/api/data';
  try {
    const res  = await fetch(url, {method: force ? 'POST' : 'GET'});
    const json = await res.json();
    _rows = json.data || [];
    setStatus(json);
    if (_rows.length > 0) { buildExchangeDropdown(); buildSectorDropdown(); renderTable(); renderChart(); }
    clearTimeout(_pollTimer);
    if (json.refreshing) _pollTimer = setTimeout(() => loadData(false), 4000);
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
    app = Flask(__name__)
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
