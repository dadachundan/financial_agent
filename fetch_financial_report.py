#!/usr/bin/env python3
"""
fetch_financial_report.py — Download and browse US company SEC 10-K / 10-Q / 8-K filings.

Features
--------
  • Enter any US ticker → streams download of all 10-K / 10-Q / 8-K filings from SEC EDGAR
  • 8-K: scans each filing index for EX-99.x PDF exhibits (investor presentations, etc.)
  • Files stored under  financial_reports/<TICKER>/
  • SQLite DB (financial_reports.db) tracks metadata
  • Web UI: download with live progress, filter, open filings in new tab, delete

Usage
-----
    python fetch_financial_report.py [--port 8081]
    Then open  http://localhost:8081
"""

import argparse
import datetime
import json
import sqlite3
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, abort, jsonify, render_template_string, request, send_file
import md_comment_widget as mcw

# ── Paths & config ────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "financial_reports"
UPLOADS_DIR = SCRIPT_DIR / "uploads"
DB_FILE     = SCRIPT_DIR / "financial_reports.db"

REPORTS_DIR.mkdir(exist_ok=True)

# SEC EDGAR rate-limit: ≤ 10 req/sec; be polite
_SEC_DELAY   = 0.12
_SEC_HEADERS = {
    "User-Agent": "FinancialReportDownloader contact@localhost.local",
    "Accept-Encoding": "gzip, deflate",
}

app      = Flask(__name__)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))
_DB_PATH = DB_FILE


# ── Database ──────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker           TEXT    NOT NULL,
                company_name     TEXT,
                period           TEXT    NOT NULL,
                form_type        TEXT,
                filed_date       TEXT,
                period_of_report TEXT,
                local_path       TEXT,
                accession_no     TEXT    UNIQUE,
                file_size        INTEGER,
                comment          TEXT,
                created_at       TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reports_ticker ON reports(ticker)"
        )
        # Migration: add comment column to existing DBs
        try:
            conn.execute("ALTER TABLE reports ADD COLUMN comment TEXT")
        except Exception:
            pass  # column already exists


# ── SEC EDGAR helpers ─────────────────────────────────────────────────────────

_ticker_map_cache: dict | None = None


def _sec_get(url: str, **kw) -> requests.Response:
    """Rate-limited GET with SEC EDGAR headers."""
    time.sleep(_SEC_DELAY)
    r = requests.get(url, headers=_SEC_HEADERS, timeout=30, **kw)
    r.raise_for_status()
    return r


def resolve_cik(ticker: str) -> tuple[str, str]:
    """Return (cik_padded_10, company_name) for a ticker symbol."""
    global _ticker_map_cache
    if _ticker_map_cache is None:
        _ticker_map_cache = _sec_get(
            "https://www.sec.gov/files/company_tickers.json"
        ).json()
    tic = ticker.strip().upper()
    for item in _ticker_map_cache.values():
        if item["ticker"].upper() == tic:
            return str(item["cik_str"]).zfill(10), item["title"]
    raise ValueError(f"Ticker '{ticker}' not found in SEC EDGAR")


def fetch_all_filings(cik: str) -> dict:
    """Return the combined recent-filings dict (parallel lists) for a CIK.

    The primary submissions JSON covers the most recent ~1 000 filings.
    Older filings are in additional pages referenced in filings.files[].
    """
    data   = _sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
    recent = data["filings"]["recent"]

    for fpage in data["filings"].get("files", []):
        page = _sec_get(f"https://data.sec.gov/submissions/{fpage['name']}").json()
        for key in recent:
            recent[key].extend(page.get(key, []))

    return recent


def _period_label(form_type: str, report_date: str) -> str:
    """Build a sortable label: '2024Q1', '2024_10K', '2024-02-21_8K', etc."""
    try:
        d     = datetime.date.fromisoformat(report_date[:10])
        year  = d.year
        month = d.month
    except Exception:
        return report_date[:10] if report_date else "unknown"

    amendment = form_type.endswith("/A")
    base      = form_type.rstrip("A").rstrip("/")
    suffix    = "_A" if amendment else ""

    if base == "10-K":
        return f"{year}_10K{suffix}"
    if base == "10-Q":
        q = (month - 1) // 3 + 1
        return f"{year}Q{q}{suffix}"
    if base == "8-K":
        return f"{report_date[:10]}_8K{suffix}"
    return f"{year}_{form_type.replace('/', '-')}"


def _download_primary(cik: str, accession_no: str, primary_doc: str, dest: Path) -> int:
    """Download the primary filing document; return bytes written."""
    clean = accession_no.replace("-", "")
    url   = (
        f"https://www.sec.gov/Archives/edgar/data"
        f"/{int(cik)}/{clean}/{primary_doc}"
    )
    r    = _sec_get(url, stream=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with open(dest, "wb") as fh:
        for chunk in r.iter_content(65536):
            fh.write(chunk)
            size += len(chunk)
    return size


_EXHIBIT_EXTS   = {".pdf", ".htm", ".html"}
_EXHIBIT_HTML   = {".htm", ".html"}

# 8-K item codes → short human-readable labels
_8K_ITEMS = {
    "1.01": "Agreement", "1.02": "Termination", "1.03": "Bankruptcy",
    "1.04": "Mine Safety", "1.05": "Material Cybersecurity",
    "2.01": "Asset Acquisition/Disposal", "2.02": "Earnings Results",
    "2.03": "Debt Obligation", "2.04": "Debt Trigger", "2.05": "Costs",
    "2.06": "Asset Impairment",
    "3.01": "Exchange Delisting", "3.02": "Unregistered Sales",
    "3.03": "Shareholder Rights",
    "4.01": "Auditor Change", "4.02": "Restatement",
    "5.01": "Shell Company Change", "5.02": "Director/Officer Change",
    "5.03": "Charter Amendment", "5.04": "Bylaw Amendment",
    "5.05": "Option Plan Amendment", "5.06": "Smaller Reporting",
    "5.07": "Shareholder Vote", "5.08": "Director Vacancy",
    "6.01": "Trust Funds", "6.02": "Asset Coverage",
    "6.03": "Material Obligation", "6.04": "Exit Provision",
    "6.05": "Loss of NAV", "6.10": "Alternative Fund",
    "7.01": "Regulation FD",
    "8.01": "Other Events",
    "9.01": "Financial Statements",
}


def _8k_label(filing_date: str, items_str: str, ex_description: str) -> str:
    """Return a meaningful period label for an 8-K exhibit row.

    Priority: exhibit description → item codes → date fallback.
    """
    date = filing_date[:10] if filing_date else "?"

    # Use the exhibit description if it's informative
    desc = (ex_description or "").strip()
    if desc and desc.upper() not in ("EX-99.1", "EX-99.2", "EX-99.3",
                                      "EXHIBIT 99.1", "EXHIBIT 99.2"):
        # Truncate to keep the badge readable
        desc = desc[:40].rstrip()
        return f"{date} {desc}"

    # Derive from item codes (e.g. "2.02,9.01" → "Earnings Results")
    items = [i.strip() for i in (items_str or "").split(",") if i.strip()]
    # Skip 9.01 (just means "has exhibits") unless it's the only one
    meaningful = [_8K_ITEMS.get(i, i) for i in items if i != "9.01"]
    if not meaningful:
        meaningful = [_8K_ITEMS.get(i, i) for i in items]
    if meaningful:
        label = " / ".join(dict.fromkeys(meaningful))[:40]  # dedup, truncate
        return f"{date} {label}"

    return f"{date} 8-K"


def _inject_base_tag(path: Path, base_url: str) -> None:
    """Rewrite an HTML file on disk with a <base> tag so relative URLs resolve correctly."""
    try:
        html  = path.read_bytes().decode("utf-8", errors="replace")
        lower = html.lower()
        tag   = f'<base href="{base_url}">'
        if tag in html:
            return  # already injected
        if "<head>" in lower:
            pos = lower.index("<head>") + len("<head>")
        elif "<head" in lower:
            pos = lower.index("<head")
            pos = lower.index(">", pos) + 1
        else:
            pos = 0
        html = html[:pos] + tag + html[pos:]
        path.write_bytes(html.encode("utf-8"))
    except Exception:
        pass


def _get_8k_exhibits(cik: str, accession_no: str) -> list[dict]:
    """Return EX-99.x exhibits from an 8-K filing index page.

    Supports PDF, HTM, and HTML exhibits (companies differ).
    Each returned dict has keys: type, description, href, filename.
    """
    clean = accession_no.replace("-", "")
    # EDGAR index uses original accession number (with dashes) + .html extension
    url = (
        f"https://www.sec.gov/Archives/edgar/data"
        f"/{int(cik)}/{clean}/{accession_no}-index.html"
    )
    try:
        r = _sec_get(url)
    except Exception:
        return []

    soup    = BeautifulSoup(r.content, "html.parser")
    results = []

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        doc_type    = cells[3].get_text(strip=True)
        description = cells[1].get_text(strip=True)
        link        = cells[2].find("a")
        if not link or not doc_type.upper().startswith("EX-99"):
            continue
        href = link.get("href", "")
        ext  = Path(href).suffix.lower()
        if ext in _EXHIBIT_EXTS:
            fname = href.rsplit("/", 1)[-1]
            results.append({
                "type":        doc_type,
                "description": description,
                "href":        href,
                "filename":    fname,
            })

    return results


# ── SSE download stream ───────────────────────────────────────────────────────

def _sse(msg: str, *, done: bool = False, error: bool = False,
         count: int = 0, total: int = 0) -> str:
    payload = json.dumps(
        {"msg": msg, "done": done, "error": error, "count": count, "total": total}
    )
    return f"data: {payload}\n\n"


def _run_download(ticker: str, forms: list[str]):
    """Generator: stream SSE events while downloading filings."""
    conn = get_conn()
    try:
        tic = ticker.strip().upper()

        yield _sse(f"🔍  Resolving CIK for {tic}…")
        cik, company_name = resolve_cik(tic)
        yield _sse(f"✅  {company_name}  (CIK {cik})")

        yield _sse("📋  Fetching filing history from SEC EDGAR…")
        recent = fetch_all_filings(cik)

        # Build list of dicts from the parallel arrays
        cols        = ["accessionNumber", "form", "reportDate", "filingDate",
                       "primaryDocument", "items", "primaryDocDescription"]
        all_filings = [dict(zip(cols, v)) for v in zip(*[recent[k] for k in cols])]

        # Separate 8-K from regular forms
        base_forms   = [f for f in forms if f != "8-K"]
        include_8k   = "8-K" in forms

        # ── Regular forms (10-K / 10-Q) ──────────────────────────────────────
        expanded = set(base_forms) | {f + "/A" for f in base_forms}
        target   = [
            f for f in all_filings
            if f["form"] in expanded and f["primaryDocument"]
        ]
        target.sort(key=lambda f: f["filingDate"], reverse=True)

        # 8-K filings (include 8-K/A amendments)
        target_8k = []
        if include_8k:
            target_8k = [
                f for f in all_filings
                if f["form"] in ("8-K", "8-K/A")
            ]
            target_8k.sort(key=lambda f: f["filingDate"], reverse=True)

        total_regular = len(target)
        total_8k      = len(target_8k)
        grand_total   = total_regular + total_8k   # approximate (8-K may have 0-N exhibits)

        summary_parts = []
        if target:
            summary_parts.append(f"{total_regular} {', '.join(base_forms)} filing(s)")
        if include_8k:
            summary_parts.append(f"{total_8k} 8-K filing(s) to scan for EX-99 exhibits")
        yield _sse(
            "📂  " + ("  •  ".join(summary_parts) if summary_parts else "No filings found"),
            total=grand_total,
        )

        ticker_dir = REPORTS_DIR / tic
        ticker_dir.mkdir(exist_ok=True)

        new_dl  = 0
        counter = 0   # overall progress counter

        # ── Download regular filings ──────────────────────────────────────────
        for filing in target:
            counter += 1
            acc     = filing["accessionNumber"]
            form    = filing["form"]
            period  = _period_label(form, filing["reportDate"])
            primary = filing["primaryDocument"]
            ext     = Path(primary).suffix or ".htm"

            # Already downloaded?
            if conn.execute(
                "SELECT 1 FROM reports WHERE accession_no=?", (acc,)
            ).fetchone():
                yield _sse(
                    f"  ⏭  {period} ({form}) — already in library",
                    count=counter, total=grand_total,
                )
                continue

            safe_acc = acc.replace("-", "_")
            filename = f"{period}_{form.replace('/', '-')}_{safe_acc}{ext}"
            dest     = ticker_dir / filename

            yield _sse(
                f"  ⬇  {period} ({form})  filed {filing['filingDate']}…",
                count=counter, total=grand_total,
            )

            try:
                size = _download_primary(cik, acc, primary, dest)
                conn.execute(
                    """INSERT OR IGNORE INTO reports
                       (ticker, company_name, period, form_type, filed_date,
                        period_of_report, local_path, accession_no, file_size)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (tic, company_name, period, form, filing["filingDate"],
                     filing["reportDate"], str(dest), acc, size),
                )
                conn.commit()
                new_dl += 1
                yield _sse(
                    f"       ✅  {filename}  ({size // 1024:,} KB)",
                    count=counter, total=grand_total,
                )
            except Exception as exc:
                yield _sse(
                    f"       ❌  {period} — {exc}",
                    count=counter, total=grand_total,
                )

        # ── Download 8-K PDF exhibits ─────────────────────────────────────────
        if include_8k and target_8k:
            yield _sse(f"📑  Scanning {total_8k} 8-K filings for EX-99 exhibits…")

            for filing in target_8k:
                counter += 1
                acc    = filing["accessionNumber"]
                form   = filing["form"]

                # Scan the filing index for EX-99.x exhibits
                exhibits = _get_8k_exhibits(cik, acc)
                if not exhibits:
                    yield _sse(
                        f"  ·  {filing['filingDate']} ({form}) — no EX-99 exhibits",
                        count=counter, total=grand_total,
                    )
                    continue

                yield _sse(
                    f"  📎  {filing['filingDate']} ({form})"
                    f" — {len(exhibits)} exhibit(s)",
                    count=counter, total=grand_total,
                )

                for ex in exhibits:
                    # Per-exhibit meaningful label using item codes + description
                    period = _8k_label(
                        filing["filingDate"],
                        filing.get("items", ""),
                        ex["description"],
                    )

                    # Unique key: accession/exhibit_filename
                    unique_key = f"{acc}/{ex['filename']}"

                    if conn.execute(
                        "SELECT 1 FROM reports WHERE accession_no=?", (unique_key,)
                    ).fetchone():
                        yield _sse(f"       ⏭  {ex['filename']} — already downloaded")
                        continue

                    # Build full URL for the exhibit file
                    href  = ex["href"]
                    clean = acc.replace("-", "")   # always needed for base_url below
                    if href.startswith("/"):
                        pdf_url = f"https://www.sec.gov{href}"
                    else:
                        pdf_url = (
                            f"https://www.sec.gov/Archives/edgar/data"
                            f"/{int(cik)}/{clean}/{ex['filename']}"
                        )

                    safe_acc  = acc.replace("-", "_")
                    orig_ext  = Path(ex["filename"]).suffix.lower() or ".htm"
                    stem      = Path(ex["filename"]).stem
                    filename  = f"{period.replace(' ', '_').replace('/', '-')}_{form.replace('/', '-')}_{safe_acc}_{stem}{orig_ext}"
                    dest      = ticker_dir / filename

                    try:
                        time.sleep(_SEC_DELAY)
                        r    = requests.get(pdf_url, headers=_SEC_HEADERS,
                                            stream=True, timeout=60)
                        r.raise_for_status()
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        size = 0
                        with open(dest, "wb") as fh:
                            for chunk in r.iter_content(65536):
                                fh.write(chunk)
                                size += len(chunk)

                        # Bake <base> tag into HTML so file:// also renders images
                        if orig_ext in _EXHIBIT_HTML:
                            base_url = (
                                f"https://www.sec.gov/Archives/edgar/data"
                                f"/{int(cik)}/{clean}/"
                            )
                            _inject_base_tag(dest, base_url)

                        conn.execute(
                            """INSERT OR IGNORE INTO reports
                               (ticker, company_name, period, form_type, filed_date,
                                period_of_report, local_path, accession_no, file_size)
                               VALUES (?,?,?,?,?,?,?,?,?)""",
                            (tic, company_name, period, form, filing["filingDate"],
                             filing["filingDate"], str(dest), unique_key, size),
                        )
                        conn.commit()
                        new_dl += 1
                        label = ex["description"] or ex["type"]
                        yield _sse(
                            f"       ✅  {label} — {filename}  ({size // 1024:,} KB)"
                        )
                    except Exception as exc:
                        yield _sse(f"       ❌  {ex['filename']} — {exc}")

        yield _sse(
            f"🎉  Done!  {new_dl} new file(s) downloaded for {tic}.",
            done=True, count=grand_total, total=max(grand_total, 1),
        )

    except Exception as exc:
        yield _sse(f"❌  {exc}", done=True, error=True)
    finally:
        conn.close()


# ── HTML template ─────────────────────────────────────────────────────────────

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>US Financial Reports</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  __MCW_HEAD__
  <style>
    body            { background:#f8f9fa; font-size:.9rem; }
    h1              { font-size:1.5rem; }
    #logBox         { font-family:monospace; font-size:.78rem; height:200px;
                      overflow-y:auto; background:#1e1e1e; color:#d4d4d4;
                      border-radius:6px; padding:8px 12px; }
    .progress       { height:6px; }
    .bp             { font-size:.72rem; font-weight:600; }
    .b10k           { background:#cce5ff !important; color:#004085 !important; }
    .b10q           { background:#d4edda !important; color:#155724 !important; }
    .b8k            { background:#e2d9f3 !important; color:#6610f2 !important; }
    .bamend         { background:#fff3cd !important; color:#856404 !important; }
    .table th       { font-size:.78rem; color:#555; white-space:nowrap; }
    .del-btn   { font-size:.72rem; padding:.15rem .45rem; }
    .bp-link   { cursor:pointer; text-decoration:none; }
    .bp-link:hover { opacity:.75; }
    #search         { max-width:280px; }
    code            { font-size:.78rem; }
    __MCW_CSS__
  </style>
</head>
<body>
<div class="container-fluid py-3 px-4">
  <h1 class="mb-0">📊 US Financial Reports</h1>
  <p class="text-muted mb-3" style="font-size:.8rem">
    SEC EDGAR 10-K / 10-Q / 8-K downloader &mdash; 8-K scans EX-99 exhibits (press releases, presentations) &mdash;
    files stored in <code>financial_reports/&lt;TICKER&gt;/</code>
  </p>

  <!-- ── Download card ── -->
  <div class="card mb-4" style="max-width:580px">
    <div class="card-body pb-2">
      <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
        <input id="tickerInput" class="form-control form-control-sm"
               style="max-width:100px;font-size:1rem;font-weight:700;text-transform:uppercase"
               placeholder="AAPL" maxlength="12"
               onkeydown="if(event.key==='Enter') startDownload()"
               oninput="this.value=this.value.toUpperCase()">
        <div class="d-flex gap-3 ms-1">
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk10K" checked>
            <label class="form-check-label fw-bold" for="chk10K"
                   style="color:#004085">10-K (annual)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk10Q" checked>
            <label class="form-check-label fw-bold" for="chk10Q"
                   style="color:#155724">10-Q (quarterly)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk8K">
            <label class="form-check-label fw-bold" for="chk8K"
                   style="color:#6610f2">8-K (EX-99 exhibits)</label>
          </div>
        </div>
        <button class="btn btn-primary btn-sm ms-1" id="dlBtn"
                onclick="startDownload()">⬇ Download All</button>
      </div>

      <div id="progressSection" style="display:none">
        <div class="progress mb-2">
          <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
               id="progressBar" style="width:0%"></div>
        </div>
        <div id="logBox"></div>
      </div>
    </div>
  </div>

  <!-- ── Filter bar ── -->
  <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
    <input id="search" class="form-control form-control-sm"
           placeholder="Search ticker / company / period…"
           oninput="applyFilters()">
    <div id="tickerChips" class="d-flex gap-1 flex-wrap"></div>
    <span id="rowCount" class="text-muted ms-auto" style="font-size:.78rem"></span>
  </div>

  <!-- ── Reports table ── -->
  <div class="table-responsive">
    <table class="table table-sm table-hover align-middle" id="reportsTable">
      <thead class="table-light">
        <tr>
          <th style="width:2.5rem">#</th>
          <th>Ticker</th>
          <th>Company</th>
          <th>Period ↓</th>
          <th>Form</th>
          <th>Filed</th>
          <th>Size</th>
          <th>Comment</th>
          <th></th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
    <p id="emptyMsg" class="text-center text-muted py-4" style="display:none">
      No reports yet. Enter a ticker and click <strong>Download All</strong>.
    </p>
  </div>
</div>

__MCW_MODALS__

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
let _rows    = [];
let _actTick = null;

// ── helpers ──────────────────────────────────────────────────────────────────
function htmlEsc(s) {
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function fmtSize(b) {
  if (!b) return '—';
  return b < 1048576 ? Math.round(b/1024)+'&nbsp;KB' : (b/1048576).toFixed(1)+'&nbsp;MB';
}
function badgeCls(f) {
  if (!f) return 'bg-secondary';
  if (f.endsWith('/A')) return 'bamend';
  if (f.includes('10-K')) return 'b10k';
  if (f.includes('10-Q')) return 'b10q';
  if (f.includes('8-K')) return 'b8k';
  return 'bg-secondary';
}

// ── load & render ─────────────────────────────────────────────────────────────
function loadReports() {
  fetch('/reports').then(r=>r.json()).then(data => {
    _rows = data;
    rebuildChips();
    applyFilters();
  });
}

function rebuildChips() {
  const counts = {};
  _rows.forEach(r => { counts[r.ticker] = (counts[r.ticker]||0)+1; });
  const tickers = Object.keys(counts).sort();
  const div = document.getElementById('tickerChips');
  div.innerHTML = '';
  tickers.forEach(t => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm ' + (t===_actTick ? 'btn-dark' : 'btn-outline-secondary');
    btn.style.cssText = 'font-size:.72rem;padding:.1rem .5rem';
    btn.innerHTML = `${t} <span class="badge bg-light text-dark">${counts[t]}</span>`;
    btn.onclick = () => { _actTick = _actTick===t ? null : t; rebuildChips(); applyFilters(); };
    div.appendChild(btn);
  });
}

function applyFilters() {
  const q = document.getElementById('search').value.trim().toLowerCase();
  const filtered = _rows.filter(r => {
    const txt = [r.ticker, r.company_name, r.period, r.form_type, r.filed_date]
                  .join(' ').toLowerCase();
    return (!q || txt.includes(q)) && (!_actTick || r.ticker===_actTick);
  });
  renderRows(filtered);
}

function renderRows(rows) {
  const tbody = document.getElementById('tbody');
  const empty = document.getElementById('emptyMsg');
  document.getElementById('rowCount').textContent =
    rows.length + ' report' + (rows.length!==1?'s':'');
  if (!rows.length) { tbody.innerHTML=''; empty.style.display=''; return; }
  empty.style.display = 'none';
  tbody.innerHTML = rows.map((r,i) => `
    <tr>
      <td class="text-muted">${i+1}</td>
      <td><strong>${r.ticker}</strong></td>
      <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${(r.company_name||'').replace(/"/g,'&quot;')}">${r.company_name||'—'}</td>
      <td>
        ${r.local_path
          ? `<a href="/file/${r.id}" target="_blank" class="badge bp bg-secondary bp-link"
               title="Click to open">${r.period}</a>`
          : `<span class="badge bp bg-secondary">${r.period}</span>`}
      </td>
      <td><span class="badge bp ${badgeCls(r.form_type)}">${r.form_type||'—'}</span></td>
      <td class="text-muted">${r.filed_date||'—'}</td>
      <td class="text-muted">${fmtSize(r.file_size)}</td>
      <td id="comment-cell-${r.id}" style="max-width:160px">
        <span class="comment-preview" data-comment="${htmlEsc(r.comment)}"
              title="Click to preview / edit"></span>
      </td>
      <td class="text-end pe-2 text-nowrap">
        <button class="btn btn-outline-danger del-btn"
                onclick="deleteReport(${r.id},this)">🗑</button>
      </td>
    </tr>`).join('');
  if (typeof renderAllCommentCells === 'function') renderAllCommentCells();
}

// ── download ─────────────────────────────────────────────────────────────────
function startDownload() {
  const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!ticker) { alert('Enter a ticker symbol (e.g. AAPL, NVDA, TSLA)'); return; }
  const forms = [];
  if (document.getElementById('chk10K').checked) forms.push('10-K');
  if (document.getElementById('chk10Q').checked) forms.push('10-Q');
  if (document.getElementById('chk8K').checked)  forms.push('8-K');
  if (!forms.length) { alert('Select at least one form type.'); return; }

  document.getElementById('progressSection').style.display = '';
  document.getElementById('dlBtn').disabled = true;
  const bar = document.getElementById('progressBar');
  bar.style.width = '0%';
  bar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  const log = document.getElementById('logBox');
  log.innerHTML = '';

  const params = new URLSearchParams({ ticker, forms: forms.join(',') });
  const es = new EventSource('/stream-download?' + params);

  es.onmessage = e => {
    const d = JSON.parse(e.data);
    const line = document.createElement('div');
    line.textContent = d.msg;
    if (d.error) line.style.color = '#f48771';
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;

    if (d.total > 0)
      bar.style.width = Math.round(d.count / d.total * 100) + '%';

    if (d.done) {
      es.close();
      document.getElementById('dlBtn').disabled = false;
      bar.style.width = '100%';
      bar.classList.remove('progress-bar-animated');
      if (!d.error) {
        bar.classList.remove('bg-primary');
        bar.classList.add('bg-success');
      }
      loadReports();
    }
  };
  es.onerror = () => {
    const line = document.createElement('div');
    line.textContent = '⚠ Connection lost';
    line.style.color = '#f48771';
    log.appendChild(line);
    es.close();
    document.getElementById('dlBtn').disabled = false;
  };
}

// ── delete ────────────────────────────────────────────────────────────────────
function deleteReport(id) {
  if (!confirm('Remove this report from the library? (The local file will also be deleted.)')) return;
  fetch('/report/' + id, { method: 'DELETE' }).then(r => {
    if (r.ok) { _rows = _rows.filter(r => r.id !== id); rebuildChips(); applyFilters(); }
  });
}

// init
loadReports();

__MCW_JS__
</script>
</body>
</html>
"""

# Apply shared markdown comment widget substitutions
for _k, _v in mcw.TEMPLATE_PARTS.items():
    TEMPLATE = TEMPLATE.replace(_k, _v)


# ── Flask routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(TEMPLATE)


@app.route("/reports")
def list_reports():
    ticker = request.args.get("ticker", "").upper().strip()
    conn   = get_conn()
    if ticker:
        rows = conn.execute(
            "SELECT * FROM reports WHERE ticker=? ORDER BY period_of_report DESC, id DESC",
            (ticker,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM reports ORDER BY ticker, period_of_report DESC, id DESC"
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/stream-download")
def stream_download_route():
    ticker = request.args.get("ticker", "").strip()
    forms  = [
        f.strip()
        for f in request.args.get("forms", "10-K,10-Q").split(",")
        if f.strip()
    ]
    if not ticker:
        return "ticker required", 400
    return Response(
        _run_download(ticker, forms),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/file/<int:report_id>")
def serve_file(report_id: int):
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path, form_type, ticker, period, accession_no FROM reports WHERE id=?",
        (report_id,),
    ).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        abort(404)
    path = Path(row["local_path"])
    if not path.exists():
        abort(404)

    # For HTML 8-K exhibits: inject <base> + responsive CSS so images load and fit
    acc_no = row["accession_no"] or ""
    if path.suffix.lower() in (".htm", ".html") and "/" in acc_no:
        try:
            acc      = acc_no.split("/")[0]
            cik, _   = resolve_cik(row["ticker"])
            clean    = acc.replace("-", "")
            base_url = (
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{clean}/"
            )
            html  = path.read_bytes().decode("utf-8", errors="replace")
            lower = html.lower()
            inject = (
                f'<base href="{base_url}">'
                f'<style>'
                f'img{{max-width:100%!important;height:auto!important}}'
                f'div,table{{max-width:100%!important;overflow-x:hidden!important}}'
                f'body{{overflow-x:hidden;margin:0 auto;padding:8px;box-sizing:border-box}}'
                f'</style>'
            )
            if "<head>" in lower:
                pos  = lower.index("<head>") + len("<head>")
            elif "<head" in lower:
                pos  = lower.index("<head")
                pos  = lower.index(">", pos) + 1
            else:
                pos  = 0
            html = html[:pos] + inject + html[pos:]
            from flask import make_response
            resp = make_response(html)
            resp.headers["Content-Type"] = "text/html; charset=utf-8"
            return resp
        except Exception:
            pass  # fall through to plain send_file

    return send_file(path)


@app.route("/comment/<int:report_id>", methods=["POST"])
def set_comment(report_id: int):
    comment = request.form.get("comment", "").strip()
    conn = get_conn()
    conn.execute(
        "UPDATE reports SET comment = ? WHERE id = ?",
        (comment or None, report_id),
    )
    conn.commit()
    conn.close()
    return "", 204


@app.route("/report/<int:report_id>", methods=["DELETE"])
def delete_report(report_id: int):
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path FROM reports WHERE id=?", (report_id,)
    ).fetchone()
    if row and row["local_path"]:
        p = Path(row["local_path"])
        if p.exists():
            p.unlink()
    conn.execute("DELETE FROM reports WHERE id=?", (report_id,))
    conn.commit()
    conn.close()
    return "", 204


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="US Financial Report downloader (SEC EDGAR 10-K / 10-Q)"
    )
    parser.add_argument("--port", type=int, default=8081,
                        help="Port to listen on (default: 8081)")
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    global _DB_PATH
    _DB_PATH = DB_FILE

    init_db()

    import socket
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        local_ip = None
    print(f"  financial-reports →  http://127.0.0.1:{args.port}")
    if local_ip:
        print(f"  financial-reports →  http://{local_ip}:{args.port}")
    print(f"  Reports folder    →  {REPORTS_DIR}")
    print(f"  DB                →  {DB_FILE}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
