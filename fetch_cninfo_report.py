#!/usr/bin/env python3
"""
fetch_cninfo_report.py — Download A-share (SSE/SZSE) and HK financial reports via CNINFO.

Features
--------
  • Enter any A-share or HK ticker (e.g. SZSE:300308, SSE:688802, HKEX:2513)
    → streams download of 年报 / 半年报 / 季报 PDFs
  • Files stored under  cninfo_reports/<EXCHANGE>/<CODE>/
  • SQLite DB (cninfo_reports.db) tracks metadata
  • Web UI: download with live progress, filter, open PDFs, delete, editable comments

Usage
-----
    python fetch_cninfo_report.py [--port 8082]
    Then open  http://localhost:8082
"""

import argparse
import json
import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, Blueprint, Response, abort, jsonify, render_template_string, request, send_file
import md_comment_widget as mcw
import nav_widget2 as nw2

# ── Paths & config ─────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "cninfo_reports"
UPLOADS_DIR = SCRIPT_DIR / "uploads"
DB_FILE     = SCRIPT_DIR / "cninfo_reports.db"

REPORTS_DIR.mkdir(exist_ok=True)

# ── CNINFO endpoints ───────────────────────────────────────────────────────────

CNINFO_QUERY_URL  = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_PDF_BASE   = "http://static.cninfo.com.cn/"
CNINFO_STOCK_URLS = {
    "szse": "http://www.cninfo.com.cn/new/data/szse_stock.json",
    "sse":  "http://www.cninfo.com.cn/new/data/sse_stock.json",
    "hke":  "http://www.cninfo.com.cn/new/data/hke_stock.json",
}

CNINFO_HEADERS = {
    "Referer":      "https://www.cninfo.com.cn/new/index",
    "User-Agent":   (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept":       "application/json, text/plain, */*",
    "Origin":       "https://www.cninfo.com.cn",
    "Content-Type": "application/x-www-form-urlencoded",
}

# ── Market / category config ───────────────────────────────────────────────────

# exchange prefix → (market_key, column, plate)
EXCHANGE_MAP: dict[str, tuple[str, str, str]] = {
    "SZSE": ("szse", "szse", "sz"),
    "SSE":  ("sse",  "sse",  "sh"),
    "HKEX": ("hke",  "hke",  "hke"),
}

# Category codes for A-share (sse/szse) — same codes work for HK column too
ALL_CATEGORIES: dict[str, str] = {
    "年报":  "category_ndbg_szsh",
    "半年报": "category_bndbg_szsh",
    "季报":  "category_jdbg_szsh",
}

# HK listed companies don't file quarterly reports
HK_CATEGORIES: dict[str, str] = {
    "年报":  "category_ndbg_szsh",
    "半年报": "category_bndbg_szsh",
}

_DELAY = 0.6  # polite delay between CNINFO requests (seconds)

MIN_FILED_YEAR = 2020  # skip filings filed before this year

# Title whitelist per category.
# CNINFO's category filter is loose — it can return cash-management notices,
# share-reduction announcements, etc.  We only want actual financial reports.
_REPORT_KEYWORDS: dict[str, list[str]] = {
    "年报":  ["年度报告", "年报"],
    "半年报": ["半年度报告", "半年报", "中期报告", "半年业绩", "中期业绩"],
    "季报":  ["季度报告", "一季报", "二季报", "三季报",
              "第一季度", "第二季度", "第三季度"],
}


def _is_report(title: str, cat_label: str) -> bool:
    """Return True only if the title matches the expected pattern for cat_label."""
    keywords = _REPORT_KEYWORDS.get(cat_label)
    if not keywords:
        return True  # no whitelist for unknown categories — allow through
    return any(kw in title for kw in keywords)

cn_bp = Blueprint("cn", __name__)

app      = Flask(__name__)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))
_DB_PATH = DB_FILE


# ── Stock list cache ───────────────────────────────────────────────────────────

_stock_cache: dict[str, dict] = {}  # market → {code: {"orgId": ..., "name": ...}}


def _load_stock_list(market: str) -> dict[str, dict]:
    """Fetch and cache the stock list for a given market.

    Returns {code: {"orgId": ..., "name": ...}}.
    """
    if market in _stock_cache:
        return _stock_cache[market]

    url = CNINFO_STOCK_URLS[market]
    r   = requests.get(
        url,
        headers={"User-Agent": CNINFO_HEADERS["User-Agent"],
                 "Referer":    CNINFO_HEADERS["Referer"]},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()

    result: dict[str, dict] = {}
    # SZSE/HKEX: {"stockList": [...]}  |  SSE: {"stockList": [...]}
    stock_list = (
        data.get("stockList")
        or data.get("result")
        or (data if isinstance(data, list) else [])
    )
    for item in stock_list:
        code   = str(item.get("code") or item.get("CODE") or "").strip()
        org_id = str(
            item.get("orgId") or item.get("ORG_ID") or item.get("org_id") or ""
        ).strip()
        name = str(
            item.get("zwjc")           # SZSE short name
            or item.get("fullname")    # HKEX
            or item.get("SECURITY_ABBR_A")
            or item.get("FULLNAME")
            or ""
        ).strip()
        if code:
            result[code] = {"orgId": org_id, "name": name}

    _stock_cache[market] = result
    return result


def _resolve_stock(code: str, market: str) -> tuple[str, str, str]:
    """Return (code_padded, orgId, company_name).

    HK codes are zero-padded to 5 digits on CNINFO (e.g. 2513 → 02513).
    Raises ValueError if not found.
    """
    code_padded = code.zfill(5) if market == "hke" else code
    stocks      = _load_stock_list(market)
    info        = stocks.get(code_padded) or stocks.get(code)
    if not info:
        raise ValueError(
            f"Stock '{code}' not found in CNINFO {market.upper()} list "
            f"(tried '{code_padded}' and '{code}')"
        )
    return code_padded, info["orgId"], info["name"]


# ── Database ───────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cninfo_reports (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker          TEXT    NOT NULL,
                market          TEXT    NOT NULL,
                stock_code      TEXT    NOT NULL,
                company_name    TEXT,
                period          TEXT,
                form_type       TEXT,
                filed_date      TEXT,
                local_path      TEXT,
                announcement_id TEXT    UNIQUE,
                file_size       INTEGER,
                comment         TEXT,
                created_at      TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cnr_ticker ON cninfo_reports(ticker)"
        )
        # Migrations for older DBs
        for col_def in ["comment TEXT"]:
            try:
                conn.execute(f"ALTER TABLE cninfo_reports ADD COLUMN {col_def}")
            except Exception:
                pass


# ── SSE helper ─────────────────────────────────────────────────────────────────

def _sse(msg: str, *, done: bool = False, error: bool = False,
         count: int = 0, total: int = 0) -> str:
    return (
        "data: "
        + json.dumps({"msg": msg, "done": done, "error": error,
                      "count": count, "total": total})
        + "\n\n"
    )


# ── CNINFO query helpers ───────────────────────────────────────────────────────

def _query_page(column: str, plate: str, stock_param: str,
                category: str, page: int, page_size: int = 30) -> dict:
    """POST one page of announcements to CNINFO hisAnnouncement API."""
    time.sleep(_DELAY)
    payload = {
        "column":    column,
        "tabName":   "fulltext",
        "pageSize":  page_size,
        "pageNum":   page,
        "stock":     stock_param,   # e.g. "300308,9900003850"
        "category":  category,
        "seDate":    "",
        "searchkey": "",
        "secid":     "",
        "plate":     plate,
        "isHLtitle": "true",
    }
    r = requests.post(
        CNINFO_QUERY_URL, data=payload,
        headers=CNINFO_HEADERS, timeout=30,
    )
    r.raise_for_status()
    return r.json()


def _fetch_all_announcements(column: str, plate: str,
                              stock_param: str, category: str) -> list[dict]:
    """Paginate through all announcement results for a given stock/category."""
    items, page = [], 1
    while True:
        data  = _query_page(column, plate, stock_param, category, page)
        batch = data.get("announcements") or []
        items.extend(batch)
        if not data.get("hasMore") or not batch:
            break
        page += 1
    return items


# ── Download stream ────────────────────────────────────────────────────────────

def _run_download(ticker: str, categories: dict[str, str]):
    """Generator: yield SSE strings while downloading filings.

    ticker format: "SZSE:300308", "SSE:688802", "HKEX:2513"
    categories: dict {label: category_code}, e.g. {"年报": "category_ndbg_szsh"}
    """
    conn = get_conn()
    try:
        raw = ticker.strip().upper()
        if ":" not in raw:
            yield _sse(
                f"❌  Invalid ticker '{raw}' — use SZSE:300308, SSE:688802, HKEX:2513",
                done=True, error=True,
            )
            return

        exchange, code = raw.split(":", 1)
        cfg = EXCHANGE_MAP.get(exchange)
        if not cfg:
            yield _sse(
                f"❌  Unknown exchange '{exchange}' — supported: SZSE, SSE, HKEX",
                done=True, error=True,
            )
            return
        market, column, plate = cfg

        yield _sse(f"🔍  Looking up {raw} on CNINFO…")
        code_padded, org_id, company_name = _resolve_stock(code, market)
        yield _sse(f"✅  {company_name}  ({exchange}:{code_padded}  orgId={org_id})")

        stock_param = f"{code_padded},{org_id}"
        safe_name   = re.sub(r"[^\w\u4e00-\u9fff]", "_", company_name).strip("_")
        ticker_dir  = REPORTS_DIR / exchange / f"{code_padded}_{safe_name}"
        ticker_dir.mkdir(parents=True, exist_ok=True)

        # Per-form-type latest date in DB → skip already-downloaded filings quickly
        _max_rows = conn.execute(
            "SELECT form_type, MAX(filed_date) FROM cninfo_reports "
            "WHERE ticker=? GROUP BY form_type",
            (raw,),
        ).fetchall()
        _max_by_form: dict[str, str] = {r[0]: r[1] for r in _max_rows}

        # Collect all announcements across requested categories
        all_anns: list[dict] = []
        for cat_label, cat_code in categories.items():
            yield _sse(f"📋  Fetching {cat_label} list from CNINFO…")
            items = _fetch_all_announcements(column, plate, stock_param, cat_code)
            for item in items:
                item["_cat"] = cat_label
            all_anns.extend(items)
            yield _sse(f"   📄  {len(items)} {cat_label} record(s) found")

        total = len(all_anns)
        yield _sse(f"📂  {total} announcement(s) to process", total=total)

        new_dl = skipped_date = skipped_year = skipped_title = counter = 0

        for ann in all_anns:
            counter  += 1
            adj_url   = ann.get("adjunctUrl", "")
            ann_title = ann.get("announcementTitle", "untitled").strip()
            cat_label = ann.get("_cat", "")
            ts_ms     = ann.get("announcementTime", 0)
            filed_date = (
                datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d")
                if ts_ms else "unknown"
            )
            unique_key = adj_url or ann.get("announcementId", "")

            if not unique_key:
                continue

            # ── Year cutoff ───────────────────────────────────────────────────
            if filed_date != "unknown" and int(filed_date[:4]) < MIN_FILED_YEAR:
                skipped_year += 1
                continue

            # ── Title whitelist — skip non-report announcements ───────────────
            if not _is_report(ann_title, cat_label):
                skipped_title += 1
                yield _sse(
                    f"  ⏭  [not a report] {ann_title[:60]}",
                    count=counter, total=total,
                )
                continue

            # ── Date-based skip (already in DB cutoff) ────────────────────────
            cutoff = _max_by_form.get(cat_label)
            if cutoff and filed_date != "unknown" and filed_date <= cutoff:
                skipped_date += 1
                continue

            # DB duplicate check
            if conn.execute(
                "SELECT 1 FROM cninfo_reports WHERE announcement_id=?", (unique_key,)
            ).fetchone():
                yield _sse(
                    f"  ⏭  {ann_title[:60]} — already in library",
                    count=counter, total=total,
                )
                continue

            # Build safe filename
            safe_title = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", ann_title)[:60].rstrip("_")
            filename   = f"{filed_date}_{cat_label}_{safe_title}.pdf"
            dest       = ticker_dir / filename
            pdf_url    = CNINFO_PDF_BASE + adj_url

            yield _sse(
                f"  ⬇  {ann_title[:60]}  ({filed_date})…",
                count=counter, total=total,
            )
            try:
                time.sleep(_DELAY)
                r = requests.get(
                    pdf_url,
                    headers={**CNINFO_HEADERS, "Accept": "application/pdf,*/*"},
                    stream=True,
                    timeout=120,
                )
                r.raise_for_status()
                dest.parent.mkdir(parents=True, exist_ok=True)
                size = 0
                with open(dest, "wb") as fh:
                    for chunk in r.iter_content(65536):
                        fh.write(chunk)
                        size += len(chunk)

                conn.execute(
                    """INSERT OR IGNORE INTO cninfo_reports
                       (ticker, market, stock_code, company_name, period, form_type,
                        filed_date, local_path, announcement_id, file_size)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (raw, market, code_padded, company_name,
                     ann_title[:120], cat_label, filed_date,
                     str(dest), unique_key, size),
                )
                conn.commit()
                new_dl += 1
                yield _sse(
                    f"       ✅  {filename}  ({size // 1024:,} KB)",
                    count=counter, total=total,
                )
            except Exception as exc:
                yield _sse(
                    f"       ❌  {ann_title[:50]} — {exc}",
                    count=counter, total=total,
                )

        if skipped_year:
            yield _sse(f"📅  Skipped {skipped_year} filing(s) filed before {MIN_FILED_YEAR}")
        if skipped_title:
            yield _sse(f"🚫  Skipped {skipped_title} non-report announcement(s) (title mismatch)")
        if skipped_date:
            yield _sse(
                f"📅  Skipped {skipped_date} filing(s) already in library "
                f"(filed_date ≤ latest in DB)"
            )

        yield _sse(
            f"🎉  Done!  {new_dl} new file(s) downloaded for {raw}.",
            done=True, count=total, total=max(total, 1),
        )

    except Exception as exc:
        import traceback
        yield _sse(
            f"❌  {exc}\n{traceback.format_exc()}",
            done=True, error=True,
        )
    finally:
        conn.close()


# ── HTML template ──────────────────────────────────────────────────────────────

TEMPLATE = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A股 / 港股 财报下载</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  __MCW_HEAD__
  <style>
    body          { background:#f8f9fa; font-size:.9rem; }
    h1            { font-size:1.5rem; }
    #logBox       { font-family:monospace; font-size:.78rem; height:200px;
                    overflow-y:auto; background:#1e1e1e; color:#d4d4d4;
                    border-radius:6px; padding:8px 12px; }
    .progress     { height:6px; }
    .bp           { font-size:.72rem; font-weight:600; }
    .b-ndbg       { background:#cce5ff !important; color:#004085 !important; }
    .b-bndbg      { background:#d4edda !important; color:#155724 !important; }
    .b-jdbg       { background:#e2d9f3 !important; color:#6610f2 !important; }
    .table th     { font-size:.78rem; color:#555; white-space:nowrap; }
    .del-btn      { font-size:.72rem; padding:.15rem .45rem; }
    #search       { max-width:280px; }
    code          { font-size:.78rem; }
    __MCW_CSS__
  </style>
</head>
<body>
__NAV__
__URLPATCH__
<div class="container-fluid py-3 px-4">
  <h1 class="mb-0">📊 A股 / 港股 财报下载</h1>
  <p class="text-muted mb-3" style="font-size:.8rem">
    巨潮资讯 (CNINFO) &mdash; 支持 SSE (上证)、SZSE (深证)、HKEX (港交所) &mdash;
    年报 / 半年报 / 季报 PDF &mdash; 文件保存在
    <code>cninfo_reports/&lt;EXCHANGE&gt;/&lt;CODE&gt;/</code>
  </p>

  <!-- ── Download card ── -->
  <div class="card mb-4" style="max-width:640px">
    <div class="card-body pb-2">
      <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
        <input id="tickerInput" class="form-control form-control-sm"
               style="max-width:160px;font-size:1rem;font-weight:700;text-transform:uppercase"
               placeholder="SZSE:300308" maxlength="16"
               onkeydown="if(event.key==='Enter') startDownload()"
               oninput="this.value=this.value.toUpperCase()">
        <div class="d-flex gap-3 ms-1">
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="cbNdbg" checked>
            <label class="form-check-label fw-bold" for="cbNdbg"
                   style="color:#004085">年报</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="cbBndbg" checked>
            <label class="form-check-label fw-bold" for="cbBndbg"
                   style="color:#155724">半年报</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="cbJdbg" checked>
            <label class="form-check-label fw-bold" for="cbJdbg"
                   style="color:#6610f2">季报</label>
          </div>
        </div>
        <button class="btn btn-primary btn-sm ms-1" id="dlBtn"
                onclick="startDownload()">⬇ Download</button>
      </div>
      <p class="text-muted mb-2" style="font-size:.75rem">
        Examples:&nbsp;
        <code>SZSE:300308</code> (深证) &nbsp;·&nbsp;
        <code>SSE:688802</code> (上证) &nbsp;·&nbsp;
        <code>HKEX:2513</code> (港交所) &nbsp;·&nbsp;
        Note: HKEX 季报 not available, will be skipped
      </p>

      <div id="progressSection" style="display:none">
        <div class="progress mb-2">
          <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
               id="progressBar" style="width:0%"></div>
        </div>
        <div id="logBox"></div>
      </div>
    </div>
  </div>

  <!-- ── Filter row ── -->
  <div class="d-flex gap-2 mb-2 align-items-center flex-wrap">
    <input type="search" id="search" class="form-control form-control-sm"
           placeholder="🔍  Filter by ticker / company / period…"
           oninput="applyFilters()">
    <select id="filterExchange" class="form-select form-select-sm" style="max-width:110px"
            onchange="applyFilters()">
      <option value="">All exchanges</option>
      <option value="SSE">SSE</option>
      <option value="SZSE">SZSE</option>
      <option value="HKEX">HKEX</option>
    </select>
    <div id="formBtns" class="d-flex gap-1"></div>
    <span id="rowCount" class="text-muted ms-auto" style="font-size:.78rem"></span>
  </div>
  <!-- ── Company chips ── -->
  <div id="companyChips" class="d-flex gap-1 flex-wrap mb-2"></div>

  <!-- ── Reports table ── -->
  <div class="table-responsive">
    <table class="table table-sm table-hover table-bordered align-middle" id="repTable">
      <thead class="table-light">
        <tr>
          <th>#</th>
          <th>Ticker</th>
          <th>Company</th>
          <th>Period / Title</th>
          <th>Type</th>
          <th>Date</th>
          <th>Size</th>
          <th>Comment</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="repBody"></tbody>
    </table>
  </div>
  <div id="rep-pager" class="d-none d-flex align-items-center gap-2 mt-2"></div>
</div>

__MCW_MODALS__
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
// ── State ─────────────────────────────────────────────────────────────────────
let _rows = [];
let _filteredRows = [];
let _page = 1;
const PAGE_SIZE = 50;
let _actForm = null;      // active form-type filter
let _actTicker = null;    // active company/ticker filter

// ── Colour badges ──────────────────────────────────────────────────────────────
function badgeClass(ft) {
  if (ft === '年报')  return 'badge bp b-ndbg';
  if (ft === '半年报') return 'badge bp b-bndbg';
  if (ft === '季报')  return 'badge bp b-jdbg';
  return 'badge bp bg-secondary';
}

// ── Load reports ───────────────────────────────────────────────────────────────
function loadReports() {
  fetch('/reports').then(r => r.json()).then(data => {
    _rows = data;
    rebuildFormBtns();
    rebuildCompanyChips();
    applyFilters();
  });
}

function rebuildFormBtns() {
  const specs = [
    { key: '年报',  cls: 'b-ndbg',  outline: 'outline-primary' },
    { key: '半年报', cls: 'b-bndbg', outline: 'outline-success' },
    { key: '季报',  cls: 'b-jdbg',  outline: 'outline-secondary' },
  ];
  const div = document.getElementById('formBtns');
  div.innerHTML = '';
  specs.forEach(({key, cls, outline}) => {
    const count = _rows.filter(r => r.form_type === key).length;
    if (!count) return;
    const active = _actForm === key;
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm ' + (active ? `badge bp ${cls}` : `btn-${outline}`);
    btn.style.cssText = 'font-size:.72rem;padding:.15rem .55rem;font-weight:600';
    btn.innerHTML = `${key} <span class="badge bg-light text-dark">${count}</span>`;
    btn.onclick = () => { _actForm = _actForm === key ? null : key; rebuildFormBtns(); applyFilters(); };
    div.appendChild(btn);
  });
}

function rebuildCompanyChips() {
  const counts = {};
  const names  = {};
  _rows.forEach(r => {
    counts[r.ticker] = (counts[r.ticker] || 0) + 1;
    if (r.company_name) names[r.ticker] = r.company_name;
  });
  const tickers = Object.keys(counts).sort();
  const div = document.getElementById('companyChips');
  div.innerHTML = '';
  tickers.forEach(t => {
    const btn = document.createElement('button');
    const active = t === _actTicker;
    btn.className = 'btn btn-sm ' + (active ? 'btn-dark' : 'btn-outline-secondary');
    btn.style.cssText = 'font-size:.72rem;padding:.1rem .5rem';
    const label = names[t] ? `${names[t]} <span style="opacity:.6;font-size:.68rem">${t}</span>` : t;
    btn.innerHTML = `${label} <span class="badge bg-light text-dark">${counts[t]}</span>`;
    btn.onclick = () => { _actTicker = _actTicker === t ? null : t; rebuildCompanyChips(); applyFilters(); };
    div.appendChild(btn);
  });
}

function applyFilters() {
  const q    = document.getElementById('search').value.toLowerCase();
  const exch = document.getElementById('filterExchange').value;

  _filteredRows = _rows.filter(r => {
    if (exch      && !(r.ticker || '').startsWith(exch + ':')) return false;
    if (_actForm  && r.form_type !== _actForm)                  return false;
    if (_actTicker && r.ticker !== _actTicker)                  return false;
    if (q) {
      const hay = [r.ticker, r.company_name, r.period, r.form_type, r.filed_date]
                   .join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  _page = 1;
  _renderPage();
  _renderPager();
  document.getElementById('rowCount').textContent =
    `${_filteredRows.length} / ${_rows.length} records`;
}

function _renderPage() {
  const start = (_page - 1) * PAGE_SIZE;
  const slice = _filteredRows.slice(start, start + PAGE_SIZE);
  const tbody = document.getElementById('repBody');
  tbody.innerHTML = slice.map((r, i) => {
    const sz  = r.file_size ? (r.file_size / 1024).toFixed(0) + ' KB' : '—';
    const num = start + i + 1;
    const esc = s => (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
    const commentHtml = `<td id="comment-cell-${r.id}"><span class="comment-preview"
      data-comment="${esc(r.comment || '')}" title="Click to preview / edit"></span></td>`;
    return `<tr>
      <td class="text-muted">${num}</td>
      <td><code style="font-size:.78rem">${esc(r.ticker)}</code></td>
      <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${esc(r.company_name)}">${esc(r.company_name)}</td>
      <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${esc(r.period)}">${esc(r.period)}</td>
      <td><span class="${badgeClass(r.form_type)}">${esc(r.form_type)}</span></td>
      <td>${r.filed_date || ''}</td>
      <td class="text-muted">${sz}</td>
      ${commentHtml}
      <td>
        <a href="${window._BASE||''}/open/${r.id}" target="_blank"
           class="btn btn-outline-secondary btn-sm del-btn" title="Open PDF">📄</a>
        <button onclick="deleteRow(${r.id},this)"
                class="btn btn-outline-danger btn-sm del-btn ms-1" title="Delete">🗑</button>
      </td>
    </tr>`;
  }).join('');
  renderAllCommentCells();
}

function _pageRange(cur, tot) {
  if (tot <= 7) return Array.from({length: tot}, (_, i) => i + 1);
  const pages = [1];
  if (cur > 3) pages.push('…');
  for (let p = Math.max(2, cur - 1); p <= Math.min(tot - 1, cur + 1); p++) pages.push(p);
  if (cur < tot - 2) pages.push('…');
  pages.push(tot);
  return pages;
}

function _renderPager() {
  const tot    = Math.ceil(_filteredRows.length / PAGE_SIZE);
  const pager  = document.getElementById('rep-pager');
  if (tot <= 1) { pager.classList.add('d-none'); return; }
  pager.classList.remove('d-none');
  const from   = (_page - 1) * PAGE_SIZE + 1;
  const to     = Math.min(_page * PAGE_SIZE, _filteredRows.length);
  pager.innerHTML = `
    <small class="text-muted me-1">${from}–${to} of ${_filteredRows.length}</small>
    <nav><ul class="pagination pagination-sm mb-0">
      ${_pageRange(_page, tot).map(p =>
        p === '…'
          ? `<li class="page-item disabled"><span class="page-link">…</span></li>`
          : `<li class="page-item ${p === _page ? 'active' : ''}">
               <button class="page-link" onclick="_goPage(${p})">${p}</button>
             </li>`
      ).join('')}
    </ul></nav>`;
}

function _goPage(p) {
  _page = p;
  _renderPage();
  _renderPager();
}

// ── Download ───────────────────────────────────────────────────────────────────
function startDownload() {
  const ticker = document.getElementById('tickerInput').value.trim();
  if (!ticker) return;

  const cats = [];
  if (document.getElementById('cbNdbg').checked)  cats.push('年报');
  if (document.getElementById('cbBndbg').checked) cats.push('半年报');
  if (document.getElementById('cbJdbg').checked)  cats.push('季报');

  const logBox  = document.getElementById('logBox');
  const progSec = document.getElementById('progressSection');
  const progBar = document.getElementById('progressBar');
  logBox.innerHTML = '';
  progSec.style.display = '';
  progBar.style.width   = '0%';

  const url = `/download?ticker=${encodeURIComponent(ticker)}&categories=${encodeURIComponent(cats.join(','))}`;
  const src = new EventSource(url);
  src.onmessage = e => {
    const d    = JSON.parse(e.data);
    const line = document.createElement('div');
    line.textContent = d.msg;
    if (d.error) line.style.color = '#ff6b6b';
    logBox.appendChild(line);
    logBox.scrollTop = logBox.scrollHeight;
    if (d.total > 0)
      progBar.style.width = Math.round(d.count / d.total * 100) + '%';
    if (d.done) {
      src.close();
      progBar.style.width = '100%';
      setTimeout(loadReports, 600);
    }
  };
  src.onerror = () => src.close();
}

// ── Delete ─────────────────────────────────────────────────────────────────────
async function deleteRow(id) {
  if (!confirm('Delete this report record and file?')) return;
  const r = await fetch(`/delete/${id}`, {method: 'DELETE'});
  if (r.ok) {
    _rows = _rows.filter(x => x.id !== id);
    applyFilters();
  }
}

// ── Init ───────────────────────────────────────────────────────────────────────
__MCW_JS__
loadReports();
</script>
</body>
</html>
"""

# Apply MCW placeholder substitutions
for _k, _v in mcw.TEMPLATE_PARTS.items():
    TEMPLATE = TEMPLATE.replace(_k, _v)
TEMPLATE = TEMPLATE.replace("__NAV__",      nw2.NAV_HTML)
TEMPLATE = TEMPLATE.replace("__URLPATCH__", nw2.URL_PATCH_JS)


# ── Flask routes ───────────────────────────────────────────────────────────────

@cn_bp.route("/")
def index():
    init_db()
    return render_template_string(TEMPLATE)


@cn_bp.route("/download")
def download():
    ticker     = request.args.get("ticker", "").strip()
    cats_param = request.args.get("categories", "年报,半年报").strip()

    if not ticker:
        return "ticker required", 400

    # Determine which categories to use
    exchange = ticker.upper().split(":")[0] if ":" in ticker else ""
    base_cats = HK_CATEGORIES if exchange == "HKEX" else ALL_CATEGORIES

    # Filter to only requested labels; if none specified use all base cats
    requested = {c.strip() for c in cats_param.split(",") if c.strip()}
    cats = {k: v for k, v in base_cats.items() if k in requested} if requested else base_cats
    if not cats:
        cats = base_cats

    def generate():
        yield from _run_download(ticker, cats)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@cn_bp.route("/reports")
def list_reports():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM cninfo_reports ORDER BY filed_date DESC, id DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@cn_bp.route("/open/<int:rid>")
def open_report(rid: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT local_path FROM cninfo_reports WHERE id=?", (rid,)
        ).fetchone()
    if not row:
        abort(404)
    path = Path(row["local_path"])
    if not path.exists():
        abort(404)
    return send_file(path, as_attachment=False)


@cn_bp.route("/delete/<int:rid>", methods=["DELETE"])
def delete_report(rid: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT local_path FROM cninfo_reports WHERE id=?", (rid,)
        ).fetchone()
        if not row:
            abort(404)
        try:
            Path(row["local_path"]).unlink(missing_ok=True)
        except Exception:
            pass
        conn.execute("DELETE FROM cninfo_reports WHERE id=?", (rid,))
    return jsonify({"ok": True})


@cn_bp.route("/comment/<int:rid>", methods=["POST"])
def save_comment(rid: int):
    comment = request.form.get("comment", "")
    with get_conn() as conn:
        conn.execute(
            "UPDATE cninfo_reports SET comment=? WHERE id=?", (comment, rid)
        )
    return jsonify({"ok": True})


# Register blueprint on the standalone app (after all routes are defined)
app.register_blueprint(cn_bp)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    parser = argparse.ArgumentParser(
        description="A-share / HK financial report downloader via CNINFO"
    )
    parser.add_argument("--port", type=int, default=8082)
    args = parser.parse_args()
    print(f"Starting CNINFO report server on http://localhost:{args.port}")
    app.run(debug=False, port=args.port, threaded=True)
