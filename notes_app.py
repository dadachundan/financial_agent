#!/usr/bin/env python3
"""
notes_app.py — Personal PDF notes: upload PDFs, write markdown comments.

Routes
------
  GET  /notes/                      — Index table (PDF | Comment two-column view)
  GET  /notes/feed                  — Blog/timeline feed of notes with comments
  POST /notes/upload                — Upload a PDF file
  GET  /notes/pdf/<id>              — Serve PDF inline
  POST /notes/comment/<id>          — Save markdown comment
  GET  /notes/open-local/<id>       — Open PDF in local OS viewer
  POST /notes/sync-annotations/<id> — Extract PDF annotations → save to comment
  POST /notes/pin/<id>              — Toggle pinned flag
  POST /notes/delete/<id>           — Delete note
"""

import datetime
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

from flask import (
    Blueprint, abort, jsonify, redirect,
    render_template_string, request, send_file,
)
import md_comment_widget as mcw
import nav_widget2 as nw2
from zsxq_viewer import (
    _extract_annotations_from_pdf,
    _format_annotations,
)

SCRIPT_DIR             = Path(__file__).parent
DB_PATH                = SCRIPT_DIR / "db" / "notes.db"
MANUAL_REPORT_DIR      = Path.home() / "Downloads" / "zsxq_report" / "manual_report"
TICKER_MAP_PATH        = SCRIPT_DIR / "db" / "name_to_ticker.json"
TICKER_NAME_CACHE_PATH = SCRIPT_DIR / "ticker_name_cache.json"

# Suffixes whose buckets get enriched with the Chinese company name.
# Korean (.KS / .KP) and Taiwan (.TW) tickers stay as plain symbols.
_CN_TICKER_SUFFIX_RE = re.compile(r"\.(HK|SZ|SS|SH)$", re.IGNORECASE)

notes_bp = Blueprint("notes", __name__)


# ── Database ──────────────────────────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            name               TEXT NOT NULL,
            local_path         TEXT,
            comment            TEXT,
            comment_updated_at TEXT,
            created_at         TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
            pinned             INTEGER DEFAULT 0,
            quarter            TEXT,
            report_date        TEXT,
            sector             TEXT,
            competitors        TEXT
        )
    """)
    for col in ("quarter", "report_date", "sector", "competitors", "ticker", "type"):
        try:
            conn.execute(f"ALTER TABLE notes ADD COLUMN {col} TEXT")
        except Exception:
            pass
    conn.commit()
    conn.close()


# ── Filename metadata extraction ─────────────────────────────────────────────

_MONTH_MAP = {
    'jan': '01', 'january': '01',
    'feb': '02', 'february': '02',
    'mar': '03', 'march': '03',
    'apr': '04', 'april': '04',
    'may': '05',
    'jun': '06', 'june': '06',
    'jul': '07', 'july': '07',
    'aug': '08', 'august': '08',
    'sep': '09', 'september': '09',
    'oct': '10', 'october': '10',
    'nov': '11', 'november': '11',
    'dec': '12', 'december': '12',
}

_TYPE_PATTERNS = [
    (r'\b10[- ]?q[_ ]?slide',  '10Q_slide'),
    (r'\bslides?\b',            '10Q_slide'),
    (r'\b10[- ]?k\b',           'annual'),
    (r'\bannual\b',             'annual'),
    (r'\b10[- ]?q\b',           '10Q'),
    (r'\b8[- ]?k\b',            '8K'),
    (r'\binvestor\b',           'investor'),
]


_TICKER_MAP_CACHE: dict | None = None


def _load_ticker_map() -> dict:
    """Load db/name_to_ticker.json (case-folded keys). Cached, reloads on mtime change."""
    global _TICKER_MAP_CACHE
    if not TICKER_MAP_PATH.exists():
        return {}
    try:
        raw = json.loads(TICKER_MAP_PATH.read_text(encoding="utf-8"))
    except Exception:
        return _TICKER_MAP_CACHE or {}
    folded = {k.casefold(): v for k, v in raw.items() if not k.startswith("_")}
    _TICKER_MAP_CACHE = folded
    return folded


def _resolve_ticker(name_prefix: str) -> str:
    """Map a filename prefix to a real symbol; falls back to the input."""
    if not name_prefix:
        return name_prefix
    return _load_ticker_map().get(name_prefix.casefold(), name_prefix)


_CN_NAME_CACHE: dict | None = None


def _load_cn_name_map() -> dict:
    """Load ticker_name_cache.json (code → Chinese name) directly, bypassing
    the background-refresh dance in ticker_names.py. Cached in-process."""
    global _CN_NAME_CACHE
    if _CN_NAME_CACHE is not None:
        return _CN_NAME_CACHE
    if not TICKER_NAME_CACHE_PATH.exists():
        _CN_NAME_CACHE = {}
        return _CN_NAME_CACHE
    try:
        _CN_NAME_CACHE = json.loads(TICKER_NAME_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        _CN_NAME_CACHE = {}
    return _CN_NAME_CACHE


def ticker_to_bucket(ticker: str) -> str:
    """Disk-folder name for a ticker. HK/A-share symbols get the Chinese
    company name appended ('0981.HK 中芯国际'); everything else returns as-is."""
    if not ticker:
        return "unknown"
    if not _CN_TICKER_SUFFIX_RE.search(ticker):
        return ticker
    code = _CN_TICKER_SUFFIX_RE.sub("", ticker)
    cn_map = _load_cn_name_map()
    name = cn_map.get(code) or cn_map.get(code.lstrip("0") or code)
    return f"{ticker} {name}" if name else ticker


def _parse_filename_meta(stem: str) -> dict:
    """Extract type, quarter, report_date, ticker from a PDF filename stem.

    Example: "Micron Technology, Inc., Earnings, Q2 FY2026 Mar 18 2026 8k"
      → type="8K", quarter="2026Q2", report_date="2026-03-18", ticker="MU"
    """
    meta = {}

    # Type — check in priority order (10Q_slide before 10Q)
    for pattern, label in _TYPE_PATTERNS:
        if re.search(pattern, stem, re.IGNORECASE):
            meta['type'] = label
            break

    # Quarter: "Q2 FY2026" or "Q2 2026"
    m = re.search(r'\bQ([1-4])\s+(?:FY)?(\d{4})\b', stem, re.IGNORECASE)
    if m:
        meta['quarter'] = f"{m.group(2)}Q{m.group(1)}"

    # Report date: "Mar 18 2026", "Apr 17, 2026", "March 17, 2026"
    m = re.search(r'\b([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})\b', stem)
    if m:
        month = _MONTH_MAP.get(m.group(1).lower())
        if month:
            meta['report_date'] = f"{m.group(3)}-{month}-{int(m.group(2)):02d}"

    # Ticker: first word of the filename, resolved through name→symbol map.
    # Accepts ASCII (Alibaba) and CJK prefixes (黑芝麻智能) so Chinese filenames work too.
    m = re.match(r'([A-Za-z][A-Za-z0-9]*|[一-鿿]+)', stem)
    if m:
        meta['ticker'] = _resolve_ticker(m.group(1))

    return meta


# ── Main index template ───────────────────────────────────────────────────────

_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Notes</title>
  <link href="/static/vendor/bootstrap.min.css" rel="stylesheet">
__MCW_HEAD__
  <style>
    body { background:#f4f6f8; padding:0; margin:0; }
    .page-wrap { padding:20px 24px 40px; }
    h4 { font-weight:700; }

    /* Notes table */
    .notes-table { width:100%; border-collapse:separate; border-spacing:0; }
    .notes-table thead th {
      background:#212529; color:#fff; font-size:.75rem; font-weight:600;
      letter-spacing:.06em; text-transform:uppercase; padding:9px 12px;
      position:sticky; top:0; z-index:2; white-space:nowrap;
    }
    .notes-table thead th:first-child { border-radius:8px 0 0 0; }
    .notes-table thead th:last-child  { border-radius:0 8px 0 0; }
    .notes-table tbody tr { vertical-align:top; }
    .notes-table tbody tr:hover > td { background:#f0f4fb; }
    .notes-table td {
      border:none; border-bottom:1px solid #e8eaed; border-right:1px solid #e8eaed;
      background:#fff;
    }
    .notes-table td:last-child { border-right:none; }

    .pdf-cell { width:32%; padding:0; }
    .meta-cell {
      width:9%; padding:10px 10px; vertical-align:middle;
      font-size:.82rem; color:#1f2937;
    }
    .comment-cell {
      width:32%; padding:12px 14px; vertical-align:top;
    }

    /* PDF cell inner layout */
    .pdf-cell-inner { display:flex; flex-direction:column; height:100%; min-height:140px; }
    .pdf-name {
      padding:12px 14px 8px; font-size:.875rem; font-weight:600; color:#1a1a1a;
      line-height:1.4; word-break:break-word;
    }
    .pdf-name a { color:#1a56db; text-decoration:none; }
    .pdf-name a:hover { text-decoration:underline; }
    .pdf-meta { padding:0 14px 4px; font-size:.72rem; color:#aaa; }
    .pdf-spacer { flex:1; }
    .pdf-actions {
      padding:8px 14px 12px; display:flex; gap:6px; align-items:center;
      border-top:1px solid #f0f0f0;
    }
    .btn-open   { font-size:.75rem; padding:3px 10px; border-color:#dc3545; color:#dc3545; }
    .btn-open:hover { background:#dc3545; color:#fff; }
    .btn-local  { font-size:.75rem; padding:3px 10px; }
    .btn-pin    { font-size:.75rem; padding:3px 8px; }
    .btn-pin.pinned { background:#198754; border-color:#198754; color:#fff; }
    .btn-delete { font-size:.75rem; padding:3px 8px; margin-left:auto;
                  color:#bbb; border-color:#ddd; }
    .btn-delete:hover { background:#dc3545; border-color:#dc3545; color:#fff; }

    /* Comment cell */
    .comment-cell .comment-preview { font-size:.85rem; }
    .comment-placeholder { font-size:.82rem; color:#ccc; font-style:italic; cursor:pointer; }
    .comment-placeholder:hover { color:#999; }

    /* Inline meta cell editing */
    .meta-val {
      display:block; cursor:pointer; border-radius:4px; padding:2px 4px;
      border:1px solid transparent; transition:border-color .15s, background .15s;
      white-space:pre-wrap; word-break:break-word;
    }
    .meta-val:hover { border-color:#93c5fd; background:#f0f7ff; }
    .meta-val.empty { color:#d1d5db; font-style:italic; font-size:.78rem; }
    .meta-input {
      font-size:.82rem; border:1.5px solid #3b82f6; border-radius:4px;
      padding:2px 6px; outline:none; width:100%; box-sizing:border-box;
    }

    /* Tag chips (competitors / ticker) */
    .tag-chip {
      display:inline-block; font-size:.7rem; font-weight:600;
      padding:1px 6px; border-radius:4px; margin:1px 2px;
      white-space:nowrap; text-decoration:none;
    }
    .tag-chip.comp { background:#fce8d4; color:#8a3d00; border:1px solid #f0c090; }
    .tag-chip.tick { background:#dbeafe; color:#1e40af; border:1px solid #93c5fd; }
    .chip-edit { cursor:pointer; color:#bbb; font-size:.72rem; margin-left:2px; }
    .chip-edit:hover { color:#555; }
    .chip-input {
      font-size:.78rem; border:1.5px solid #3b82f6; border-radius:4px;
      padding:2px 6px; outline:none; width:100%; box-sizing:border-box;
    }

    /* Upload area */
    .filter-bar { display:flex; align-items:center; flex-wrap:wrap; gap:6px;
                  background:#fff; border:1px solid #e0e0e0; border-radius:8px;
                  padding:8px 14px; margin-bottom:14px; }
    .filter-label { font-size:.72rem; color:#888; font-weight:700;
                    text-transform:uppercase; letter-spacing:.05em; white-space:nowrap; margin-right:2px; }
    .upload-zone {
      border:2px dashed #c8d0da; border-radius:10px; padding:28px 20px;
      text-align:center; background:#fff; cursor:pointer; transition:border-color .2s;
      margin-bottom:20px;
    }
    .upload-zone.dragover { border-color:#1a56db; background:#f0f4fb; }
    .upload-zone p { margin:0; color:#888; font-size:.88rem; }
    .upload-zone b { color:#1a56db; }
    #uploadProgress { display:none; }

    /* Pinned row highlight */
    tr.pinned-row > td { background:#fffbf0 !important; }

    __MCW_CSS__
  </style>
</head>
<body>
__NAV__
__URLPATCH__

<div class="page-wrap">
  <div class="d-flex align-items-center mb-3 gap-3 flex-wrap">
    <h4 class="mb-0">📎 Notes</h4>
    <span class="text-muted small">{{ rows|length }} PDFs</span>
    <button id="openSelectedBtn" class="btn btn-sm btn-danger" onclick="openSelected()" disabled>
      📄 Open (<span id="selCount">0</span>)
    </button>
    <button id="revealBtn" class="btn btn-sm btn-outline-secondary" onclick="revealInFinder(this)" disabled>
      🔍 Show in Finder
    </button>
    <button id="batchSectorBtn" class="btn btn-sm btn-outline-info" onclick="batchSet('sector')" disabled>
      Set Sector
    </button>
    <button id="batchTickerBtn" class="btn btn-sm btn-outline-info" onclick="batchSet('ticker')" disabled>
      Set Ticker
    </button>
    <button class="btn btn-sm btn-outline-warning" onclick="moveBySector(this)">
      Move PDFs per sector
    </button>
    <button id="scanBtn" class="btn btn-sm btn-outline-primary" onclick="scanManualReport(this)">
      🔍 Scan manual_report
    </button>
    <a href="{{ _base | default('') }}/feed" class="btn btn-sm btn-outline-secondary ms-auto">📓 Feed View</a>
  </div>

  <!-- Scan log -->
  <div id="scanLog" style="display:none;background:#1e1e2e;color:#cdd6f4;border-radius:8px;
       padding:12px 16px;margin-bottom:14px;font-size:.78rem;font-family:monospace;
       max-height:220px;overflow-y:auto;white-space:pre-wrap"></div>

  <!-- Upload zone -->
  <div class="upload-zone" id="uploadZone">
    <p>📄 <b>Click or drag &amp; drop</b> PDFs to upload</p>
    <p class="mt-1" style="font-size:.78rem">Accepts multiple .pdf files up to 50 MB each</p>
    <input type="file" id="fileInput" accept=".pdf" multiple style="display:none">
    <div id="uploadProgress" class="mt-2">
      <div class="progress" style="height:6px;max-width:300px;margin:0 auto">
        <div class="progress-bar progress-bar-striped progress-bar-animated"
             id="uploadBar" style="width:100%"></div>
      </div>
      <p class="text-muted mt-1" style="font-size:.78rem" id="uploadMsg">Uploading…</p>
    </div>
  </div>

  <!-- Filter bar -->
  <div class="filter-bar" id="filterBar">
    <span class="filter-label">TICKER:</span>
    <select id="fTicker" class="form-select form-select-sm" style="max-width:180px"
            onchange="applyNotesFilter()">
      <option value="">All tickers</option>
      {% for t in rows | map(attribute='ticker') | select | unique | sort %}
        {% for chip in t.split(',') if chip.strip() %}
      <option value="{{ chip.strip()|lower }}">{{ chip.strip() }}</option>
        {% endfor %}
      {% endfor %}
    </select>
    <span class="filter-label ms-2">TYPE:</span>
    <select id="fType" class="form-select form-select-sm" style="max-width:150px"
            onchange="applyNotesFilter()">
      <option value="">All types</option>
      <option>10Q_slide</option><option>annual</option><option>10Q</option>
      <option>8K</option><option>investor</option>
    </select>
    <span class="filter-label ms-2">COMMENT:</span>
    <select id="fComment" class="form-select form-select-sm" style="max-width:140px"
            onchange="applyNotesFilter()">
      <option value="">All</option>
      <option value="1">Has comment</option>
      <option value="0">No comment</option>
    </select>
    <input id="fSearch" type="text" class="form-control form-control-sm ms-2"
           style="max-width:280px" placeholder="Search name / ticker / sector…"
           oninput="applyNotesFilter()">
    <a href="#" onclick="clearNotesFilter();return false"
       class="btn btn-sm btn-link text-muted p-0 ms-1">✕ Clear</a>
    <span id="filterCount" class="text-muted small ms-2"></span>
  </div>

  <!-- Notes table -->
  {% if rows %}
  <table class="notes-table">
    <thead>
      <tr>
        <th style="width:36px">
          <input type="checkbox" id="chkAll" title="Select all"
                 onchange="toggleAllChecks(this.checked)">
        </th>
        <th>PDF</th>
        <th>Ticker</th>
        <th>Type</th>
        <th>Quarter</th>
        <th>Report Date</th>
        <th>Sector</th>
        <th>Competitors</th>
        <th>Comment</th>
      </tr>
    </thead>
    <tbody id="notesBody">
      {% for row in rows %}
      <tr id="row-{{ row.id }}" class="{% if row.pinned %}pinned-row{% endif %}" data-has-comment="{{ '1' if row.comment else '0' }}">
        <td style="text-align:center;vertical-align:middle;padding:0 8px">
          <input type="checkbox" class="row-chk" data-id="{{ row.id }}"
                 onchange="updateSelCount()">
        </td>
        <td class="pdf-cell">
          <div class="pdf-cell-inner">
            <div class="pdf-name">
              <a href="{{ _base | default('') }}/pdf/{{ row.id }}" target="_blank"
                 title="{{ row.name }}">
                {{ row.name | replace('.pdf','') }}
              </a>
            </div>
            <div class="pdf-meta">
              {{ (row.created_at or '')[:10] }}
              {% if row.pinned %} [pinned]{% endif %}
            </div>
            <div class="pdf-spacer"></div>
            <div class="pdf-actions">
              <a href="{{ _base | default('') }}/pdf/{{ row.id }}" target="_blank"
                 class="btn btn-sm btn-outline-danger btn-open">
                📄 Open
              </a>
              <button class="btn btn-sm btn-outline-secondary btn-local"
                      onclick="openLocal({{ row.id }}, this)">
                📁 Local
              </button>
              <button class="btn btn-sm btn-outline-secondary"
                      onclick="syncAnnotations({{ row.id }}, this)"
                      title="Extract PDF annotations and save to comment">
                📌
              </button>
              <button class="btn btn-sm btn-outline-success btn-pin {% if row.pinned %}pinned{% endif %}"
                      onclick="togglePin({{ row.id }}, this)"
                      title="{{ 'Unpin' if row.pinned else 'Pin' }}">
                📍
              </button>
              <button class="btn btn-sm btn-outline-secondary btn-delete"
                      onclick="deleteNote({{ row.id }}, this)"
                      title="Delete">
                —
              </button>
            </div>
          </div>
        </td>
        <td class="meta-cell" id="ticker-cell-{{ row.id }}" style="min-width:80px">
          <span data-chips="{{ (row.ticker or '')|e }}">
            {%- for t in (row.ticker or '').split(',') if t.strip() %}
            <span class="tag-chip tick">{{ t.strip() }}</span>
            {%- endfor %}
            <span class="chip-edit" onclick="editChips({{ row.id }}, 'ticker', this)" title="Edit">✏</span>
          </span>
        </td>
        <td class="meta-cell">
          <span class="meta-val type-val {% if not row.type %}empty{% endif %}"
                data-field="type" data-id="{{ row.id }}"
                onclick="editType(this)">{{ row.type or '—' }}</span>
        </td>
        <td class="meta-cell">
          <span class="meta-val {% if not row.quarter %}empty{% endif %}"
                data-field="quarter" data-id="{{ row.id }}"
                onclick="editMeta(this)">{{ row.quarter or '—' }}</span>
        </td>
        <td class="meta-cell">
          <span class="meta-val {% if not row.report_date %}empty{% endif %}"
                data-field="report_date" data-id="{{ row.id }}"
                onclick="editMeta(this)">{{ row.report_date or '—' }}</span>
        </td>
        <td class="meta-cell">
          <span class="meta-val {% if not row.sector %}empty{% endif %}"
                data-field="sector" data-id="{{ row.id }}"
                onclick="editMeta(this)">{{ row.sector or '—' }}</span>
        </td>
        <td class="meta-cell" id="competitors-cell-{{ row.id }}" style="min-width:120px">
          <span data-chips="{{ (row.competitors or '')|e }}">
            {%- for t in (row.competitors or '').split(',') if t.strip() %}
            <span class="tag-chip comp">{{ t.strip() }}</span>
            {%- endfor %}
            <span class="chip-edit" onclick="editChips({{ row.id }}, 'competitors', this)" title="Edit">✏</span>
          </span>
        </td>
        <td class="comment-cell" id="comment-cell-{{ row.id }}"
            onclick="viewComment({{ row.id }}, this.querySelector('.comment-preview'))">
          <span class="comment-preview"
                data-comment="{{ row.comment | e if row.comment else '' }}"
                title="Click to preview / edit">
            {% if not row.comment %}
            <span class="comment-placeholder">Click to add note…</span>
            {% endif %}
          </span>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  {% else %}
  <div class="text-center text-muted py-5">
    <p style="font-size:2rem">📄</p>
    <p>No PDFs yet — upload one above.</p>
  </div>
  {% endif %}
</div>

<!-- Batch set modal -->
<div class="modal fade" id="batchSetModal" tabindex="-1">
  <div class="modal-dialog modal-sm">
    <div class="modal-content">
      <div class="modal-header py-2">
        <h6 class="modal-title mb-0" id="batchSetTitle"></h6>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body py-2">
        <input type="text" id="batchSetInput" class="form-control form-control-sm"
               placeholder="Enter value (blank to clear)…"
               onkeydown="if(event.key==='Enter') batchSetConfirm()">
      </div>
      <div class="modal-footer py-2">
        <button class="btn btn-sm btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-sm btn-primary" onclick="batchSetConfirm()">Apply</button>
      </div>
    </div>
  </div>
</div>

__MCW_MODALS__

<script src="/static/vendor/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
const _base = "{{ _base | default('') }}";
window._commentSavePrefix = '';
window._onCommentRendered = function(cell) {
  const tr = cell.closest('tr');
  if (tr) {
    const span = cell.querySelector('.comment-preview');
    tr.dataset.hasComment = (span && span.dataset.comment) ? '1' : '0';
  }
};

__MCW_JS__

// ----------------------------------------
const uploadZone = document.getElementById('uploadZone');
const fileInput  = document.getElementById('fileInput');

uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', ()  => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault(); uploadZone.classList.remove('dragover');
  const files = Array.from(e.dataTransfer.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
  if (files.length) uploadFiles(files);
  else alert('Only PDF files are supported.');
});
fileInput.addEventListener('change', () => {
  const files = Array.from(fileInput.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
  if (files.length) uploadFiles(files);
  fileInput.value = '';
});

async function uploadFiles(files) {
  const progressEl = document.getElementById('uploadProgress');
  const msgEl      = document.getElementById('uploadMsg');
  progressEl.style.display = 'block';
  let failed = 0;
  const skipped = [];
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    msgEl.textContent = `Uploading ${i + 1} / ${files.length}: ${file.name}…`;
    const fd = new FormData();
    fd.append('pdf', file);
    try {
      const r    = await fetch('/upload', { method: 'POST', body: fd });
      const data = await r.json();
      if (!data.ok) {
        if (r.status === 409) { skipped.push(file.name); }
        else { failed++; console.error('Upload failed:', file.name, data.error); }
      }
    } catch (e) {
      failed++;
      console.error('Upload error:', file.name, e);
    }
  }
  progressEl.style.display = 'none';
  if (skipped.length > 0) alert(`${skipped.length} file(s) already in database, skipped:\\n${skipped.join('\\n')}`);
  if (failed > 0) alert(`${failed} file(s) failed to upload.`);
  window.location.reload();
}

// ----------------------------------------
function openLocal(id, btn) {
  btn.disabled = true;
  fetch('/open-local/' + id)
    .then(r => r.json())
    .then(d => { btn.disabled = false; if (!d.ok) alert(d.error || 'Cannot open file'); })
    .catch(() => { btn.disabled = false; });
}

function togglePin(id, btn) {
  fetch('/pin/' + id, { method: 'POST' })
    .then(r => r.json())
    .then(d => {
      if (d.ok) {
        btn.classList.toggle('pinned', d.pinned);
        btn.title = d.pinned ? 'Unpin' : 'Pin';
        const row = document.getElementById('row-' + id);
        if (row) row.classList.toggle('pinned-row', d.pinned);
        const meta = row && row.querySelector('.pdf-meta');
        if (meta) {
          const base = meta.textContent.replace(/\s*\[pinned\]/g, '').trim();
          meta.textContent = d.pinned ? base + ' [pinned]' : base;
        }
      }
    });
}

function deleteNote(id, btn) {
  if (!confirm('Delete this PDF and its notes? This cannot be undone.')) return;
  fetch('/delete/' + id, { method: 'POST' })
    .then(r => r.json())
    .then(d => {
      if (d.ok) {
        const row = document.getElementById('row-' + id);
        if (row) row.remove();
      } else {
        alert(d.error || 'Delete failed');
      }
    });
}

function syncAnnotations(id, btn) {
  const orig = btn.textContent;
  btn.disabled = true;
  btn.textContent = '⏳';
  fetch('/sync-annotations/' + id, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
      btn.disabled = false;
      btn.textContent = orig;
      if (data.ok) {
        const cell = document.getElementById('comment-cell-' + id);
        if (cell) renderCommentCell(cell, id, data.comment);
        btn.textContent = '✅';
        btn.title = data.count + ' annotation(s) saved';
        setTimeout(() => { btn.textContent = orig; btn.title = 'Extract PDF annotations and save to comment'; }, 2500);
      } else {
        btn.textContent = '❌';
        btn.title = data.error || 'No annotations found';
        setTimeout(() => { btn.textContent = orig; btn.title = 'Extract PDF annotations and save to comment'; }, 2500);
      }
    })
    .catch(() => {
      btn.disabled = false;
      btn.textContent = '❌';
      setTimeout(() => { btn.textContent = orig; }, 2000);
    });
}

document.addEventListener('DOMContentLoaded', renderAllCommentCells);

// ----------------------------------------
const TYPE_OPTIONS = ['10Q_slide', 'annual', '10Q', '8K', 'investor'];

function editType(span) {
  if (span.querySelector('select')) return;
  const id  = span.dataset.id;
  const cur = span.classList.contains('empty') ? '' : span.textContent.trim();

  const sel = document.createElement('select');
  sel.style.cssText = 'font-size:.82rem;border:1.5px solid #3b82f6;border-radius:4px;padding:2px 4px;outline:none';
  const blank = document.createElement('option');
  blank.value = ''; blank.textContent = '—';
  sel.appendChild(blank);
  TYPE_OPTIONS.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt; o.textContent = opt;
    if (opt === cur) o.selected = true;
    sel.appendChild(o);
  });

  span.textContent = '';
  span.appendChild(sel);
  sel.focus();

  function commit() {
    const val = sel.value;
    span.textContent = val || '—';
    span.classList.toggle('empty', !val);
    _saveMeta(id, 'type', val, span, cur);
  }
  sel.addEventListener('change', () => { sel.blur(); });
  sel.addEventListener('blur', commit);
  sel.addEventListener('keydown', e => {
    if (e.key === 'Escape') { sel.removeEventListener('blur', commit); span.textContent = cur || '—'; span.classList.toggle('empty', !cur); }
  });
}

// ----------------------------------------
function editMeta(span) {
  if (span.querySelector('input')) return;
  const field = span.dataset.field;
  const id    = span.dataset.id;
  const cur   = span.classList.contains('empty') ? '' : span.textContent.trim();

  if (field === 'report_date') { _editDate(span, id, cur); return; }

  const input = document.createElement('input');
  input.type  = 'text';
  input.value = cur;
  input.className = 'meta-input';
  if (field === 'quarter') input.placeholder = '2026Q2 or 2026';
  span.textContent = '';
  span.appendChild(input);
  input.focus();
  input.select();

  function restore() { span.textContent = cur || '—'; span.classList.toggle('empty', !cur); }

  function save() {
    const val = input.value.trim();
    if (field === 'quarter' && val && !/^\d{4}Q[1-4]$/i.test(val) && !/^\d{4}$/.test(val)) {
      input.style.borderColor = '#ef4444'; return;
    }
    const norm = (field === 'quarter' && val) ? val.toUpperCase() : val;
    restore();
    if (norm) span.textContent = norm;
    _saveMeta(id, field, norm, span, cur);
  }
  input.addEventListener('blur', save);
  input.addEventListener('input', () => { input.style.borderColor = ''; });
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter')  { input.blur(); }
    if (e.key === 'Escape') { input.removeEventListener('blur', save); restore(); }
  });
}

function _editDate(span, id, cur) {
  const inp = document.createElement('input');
  inp.type = 'text';
  inp.value = (cur && cur !== '—') ? cur : '';
  inp.placeholder = 'YYYY-MM-DD';
  inp.style.cssText = 'width:108px;font-size:.82rem;border:1.5px solid #3b82f6;' +
    'border-radius:4px;padding:2px 6px;outline:none';

  span.textContent = '';
  span.appendChild(inp);
  inp.focus(); inp.select();

  function restore() {
    span.textContent = cur || '—';
    span.classList.toggle('empty', !cur || cur === '—');
  }

  function commit() {
    const v = inp.value.trim();
    if (!v) { restore(); _saveMeta(id, 'report_date', '', span, cur); return; }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) { inp.style.borderColor = '#ef4444'; return; }
    const [y, m, d] = v.split('-').map(Number);
    if (m < 1 || m > 12 || d < 1 || d > 31) { inp.style.borderColor = '#ef4444'; return; }
    restore();
    span.textContent = v;
    _saveMeta(id, 'report_date', v, span, cur);
  }

  inp.addEventListener('blur', commit);
  inp.addEventListener('input', () => { inp.style.borderColor = '#3b82f6'; });
  inp.addEventListener('keydown', e => {
      if (e.key === 'Enter')  { inp.blur(); }
      if (e.key === 'Escape') { inp.removeEventListener('blur', commit); restore(); }
    });
}

// ----------------------------------------
function editChips(id, field, btn) {
  const wrapper = btn.closest('[data-chips]');
  const cell    = btn.closest('td');
  const cur     = wrapper ? wrapper.dataset.chips : '';
  const cls     = field === 'ticker' ? 'tick' : 'comp';
  const input   = document.createElement('input');
  input.className   = 'chip-input';
  input.value       = cur;
  input.placeholder = 'tag1, tag2, …';
  cell.innerHTML = '';
  cell.appendChild(input);
  input.focus();
  const save = () => {
    const val = input.value.trim();
    fetch('/meta/' + id, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({[field]: val}),
    }).then(r => r.json()).then(d => {
      if (d.ok) renderChips(cell, id, field, val, cls);
      else renderChips(cell, id, field, cur, cls);
    }).catch(() => renderChips(cell, id, field, cur, cls));
  };
  input.addEventListener('blur', save);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter')  { e.preventDefault(); input.blur(); }
    if (e.key === 'Escape') { renderChips(cell, id, field, cur, cls); }
  });
}

function renderChips(cell, id, field, val, cls) {
  const tags = val ? val.split(',').map(t => t.trim()).filter(Boolean) : [];
  const span = document.createElement('span');
  span.dataset.chips = val || '';
  tags.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'tag-chip ' + cls;
    chip.textContent = t;
    span.appendChild(chip);
  });
  const ei = document.createElement('span');
  ei.className = 'chip-edit'; ei.textContent = ' ✏'; ei.title = 'Edit';
  ei.onclick = () => editChips(id, field, ei);
  span.appendChild(ei);
  cell.innerHTML = ''; cell.appendChild(span);
}

function _saveMeta(id, field, val, span, cur) {
  fetch('/meta/' + id, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({[field]: val}),
  }).then(r => r.json()).then(d => {
    if (d.ok) {
      span.textContent = val || '—';
      span.classList.toggle('empty', !val);
    }
  }).catch(() => {
    span.textContent = cur || '—';
    span.classList.toggle('empty', !cur);
  });
}

// ----------------------------------------
function moveBySector(btn) {
  if (!confirm('Move all PDFs into per-sector folders under manual_report/<sector>/?\\n\\nDatabase paths will be updated.')) return;
  btn.disabled = true;
  btn.textContent = 'Moving...';
  fetch('/move-by-sector', {method: 'POST'})
    .then(r => r.json())
    .then(d => {
      btn.disabled = false;
      btn.textContent = 'Move PDFs per sector';
      const errs = d.errors && d.errors.length ? '\\nErrors: ' + d.errors.length : '';
      alert('Moved: ' + d.moved + '  Skipped: ' + d.skipped + errs);
      if (d.moved > 0) location.reload();
    })
    .catch(() => { btn.disabled = false; btn.textContent = 'Move PDFs per sector'; alert('Request failed'); });
}

// ----------------------------------------
function scanManualReport(btn) {
  const log  = document.getElementById('scanLog');
  log.style.display = 'block';
  log.textContent = '';
  btn.disabled = true;
  btn.textContent = '⏳ Scanning…';

  const es = new EventSource('/scan-manual-report');
  es.onmessage = e => {
    const msg = e.data;
    if (msg === '__done__') {
      es.close();
      btn.disabled = false;
      btn.textContent = '🔍 Scan manual_report';
      log.textContent += '\\n✅ Done.';
      log.scrollTop = log.scrollHeight;
      window.location.reload();
      return;
    }
    log.textContent += msg + '\\n';
    log.scrollTop = log.scrollHeight;
  };
  es.onerror = () => {
    es.close();
    btn.disabled = false;
    btn.textContent = '🔍 Scan manual_report';
    log.textContent += '\\n❌ Connection error.';
  };
}

// ----------------------------------------
function updateSelCount() {
  const checked = document.querySelectorAll('.row-chk:checked').length;
  document.getElementById('selCount').textContent = checked;
  const none = checked === 0;
  document.getElementById('openSelectedBtn').disabled = none;
  document.getElementById('revealBtn').disabled = none;
  document.getElementById('batchSectorBtn').disabled = none;
  document.getElementById('batchTickerBtn').disabled = none;
  const all = Array.from(document.querySelectorAll('.row-chk'))
                   .filter(c => c.closest('tr').style.display !== 'none');
  document.getElementById('chkAll').checked = all.length > 0 && all.every(c => c.checked);
}

// ----------------------------------------
let _batchField = '';
let _batchModal = null;

function batchSet(field) {
  _batchField = field;
  const count = document.querySelectorAll('.row-chk:checked').length;
  const label = field === 'sector' ? 'Sector' : 'Ticker';
  document.getElementById('batchSetTitle').textContent = `Set ${label} for ${count} row${count > 1 ? 's' : ''}`;
  document.getElementById('batchSetInput').value = '';
  if (!_batchModal) _batchModal = new bootstrap.Modal(document.getElementById('batchSetModal'));
  _batchModal.show();
  setTimeout(() => document.getElementById('batchSetInput').focus(), 250);
}

async function batchSetConfirm() {
  const val = document.getElementById('batchSetInput').value.trim();
  _batchModal.hide();
  const ids = Array.from(document.querySelectorAll('.row-chk:checked')).map(c => parseInt(c.dataset.id));
  await Promise.all(ids.map(id =>
    fetch('/meta/' + id, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({[_batchField]: val}),
    })
  ));
  // Update cells in place
  ids.forEach(id => {
    if (_batchField === 'ticker') {
      const cell = document.getElementById('ticker-cell-' + id);
      if (cell) renderChips(cell, id, 'ticker', val, 'tick');
    } else {
      const span = document.querySelector(`#row-${id} .meta-val[data-field="${_batchField}"]`);
      if (span) {
        span.textContent = val || '—';
        span.classList.toggle('empty', !val);
      }
    }
  });
}

function revealInFinder(btn) {
  const ids = Array.from(document.querySelectorAll('.row-chk:checked')).map(c => parseInt(c.dataset.id));
  btn.disabled = true;
  fetch('/reveal-in-finder', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ids}),
  }).then(r => r.json())
    .then(d => { btn.disabled = false; if (!d.ok) alert(d.error || 'Failed'); })
    .catch(() => { btn.disabled = false; });
}

function toggleAllChecks(checked) {
  document.querySelectorAll('.row-chk').forEach(c => {
    if (c.closest('tr').style.display !== 'none') c.checked = checked;
  });
  updateSelCount();
}

function openSelected() {
  const ids = Array.from(document.querySelectorAll('.row-chk:checked')).map(c => c.dataset.id);
  ids.forEach(id => fetch('/open-local/' + id));
}

// ----------------------------------------
function applyNotesFilter() {
  const ticker  = document.getElementById('fTicker').value.toLowerCase();
  const type    = document.getElementById('fType').value.toLowerCase();
  const comment = document.getElementById('fComment').value;
  const search  = document.getElementById('fSearch').value.toLowerCase().trim();
  const rows    = document.querySelectorAll('#notesBody tr');
  let vis = 0;
  rows.forEach(tr => {
    const tickerCell = tr.querySelector('[data-chips]') ? tr.querySelector('[data-chips]').dataset.chips.toLowerCase() : '';
    const typeCell   = (tr.querySelector('.meta-val[data-field="type"]') || {}).textContent || '';
    const text       = tr.textContent.toLowerCase();
    const ok = (!ticker  || tickerCell.includes(ticker))
            && (!type    || typeCell.toLowerCase() === type)
            && (!comment || tr.dataset.hasComment === comment)
            && (!search  || text.includes(search));
    tr.style.display = ok ? '' : 'none';
    if (ok) vis++;
  });
  const total = rows.length;
  document.getElementById('filterCount').textContent =
    (vis < total) ? `${vis} / ${total}` : '';
}

function clearNotesFilter() {
  document.getElementById('fTicker').value  = '';
  document.getElementById('fType').value    = '';
  document.getElementById('fComment').value = '';
  document.getElementById('fSearch').value  = '';
  applyNotesFilter();
}
</script>
</body>
</html>
"""

# Apply MCW substitutions
for _k, _v in mcw.TEMPLATE_PARTS.items():
    _INDEX_TEMPLATE = _INDEX_TEMPLATE.replace(_k, _v)
_INDEX_TEMPLATE = (
    _INDEX_TEMPLATE
    .replace("__NAV__",      nw2.NAV_HTML)
    .replace("__URLPATCH__", nw2.URL_PATCH_JS)
)


# ── Routes ────────────────────────────────────────────────────────────────────

@notes_bp.route("/")
def index():
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, name, comment, created_at, comment_updated_at, pinned,
               quarter, report_date, sector, competitors, ticker, type
        FROM   notes
        ORDER  BY pinned DESC, id DESC
    """).fetchall()
    conn.close()
    return render_template_string(_INDEX_TEMPLATE, rows=rows)


@notes_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("pdf")
    if not f:
        return jsonify(ok=False, error="No file provided"), 400
    if not f.filename.lower().endswith(".pdf"):
        return jsonify(ok=False, error="Only PDF files are supported"), 400

    safe_name = Path(f.filename).name
    conn = get_conn()
    existing = conn.execute("SELECT id FROM notes WHERE name=?", (safe_name,)).fetchone()
    conn.close()
    if existing:
        return jsonify(ok=False, error=f"Already in database: {safe_name}"), 409

    meta = _parse_filename_meta(Path(safe_name).stem)
    bucket = ticker_to_bucket((meta.get('ticker') or '').strip() or 'unknown')
    dest_dir = MANUAL_REPORT_DIR / bucket
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / safe_name
    i = 1
    while dest.exists():
        dest = dest_dir / f"{Path(safe_name).stem}_{i}.pdf"; i += 1

    f.save(dest)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = get_conn()
    conn.execute(
        """INSERT INTO notes (name, local_path, created_at, type, quarter, report_date, ticker)
           VALUES (?,?,?,?,?,?,?)""",
        (dest.name, str(dest), now,
         meta.get('type'), meta.get('quarter'), meta.get('report_date'), meta.get('ticker')),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@notes_bp.route("/pdf/<int:note_id>")
def serve_pdf(note_id: int):
    conn = get_conn()
    row = conn.execute("SELECT local_path FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        abort(404)
    path = Path(row["local_path"])
    if not path.exists():
        abort(404)
    return send_file(path, mimetype="application/pdf")


@notes_bp.route("/comment/<int:note_id>", methods=["POST"])
def set_comment(note_id: int):
    comment = request.form.get("comment", "").strip()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = get_conn()
    conn.execute(
        "UPDATE notes SET comment=?, comment_updated_at=? WHERE id=?",
        (comment or None, now if comment else None, note_id),
    )
    conn.commit()
    conn.close()
    return "", 204


@notes_bp.route("/meta/<int:note_id>", methods=["POST"])
def set_meta(note_id: int):
    data = request.get_json(silent=True) or {}
    allowed = {"quarter", "report_date", "sector", "competitors", "ticker", "type"}
    updates = {k: (v.strip() or None) for k, v in data.items() if k in allowed}
    if not updates:
        return jsonify(ok=False, error="No valid fields"), 400
    if "report_date" in updates and updates["report_date"]:
        try:
            updates["report_date"] = datetime.date.fromisoformat(updates["report_date"]).isoformat()
        except ValueError:
            return jsonify(ok=False, error="Invalid date format, expected YYYY-MM-DD"), 400
    cols = ", ".join(f"{k}=?" for k in updates)
    conn = get_conn()
    conn.execute(f"UPDATE notes SET {cols} WHERE id=?", (*updates.values(), note_id))
    conn.commit()
    conn.close()
    return jsonify(ok=True)


@notes_bp.route("/open-local/<int:note_id>")
def open_local(note_id: int):
    conn = get_conn()
    row = conn.execute("SELECT local_path FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        return jsonify(ok=False, error="File not found")
    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error=f"File missing: {path}")
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", str(path)])
        else:
            subprocess.Popen(["start", str(path)], shell=True)
        return jsonify(ok=True)
    except Exception as exc:
        return jsonify(ok=False, error=str(exc))


@notes_bp.route("/sync-annotations/<int:note_id>", methods=["POST"])
def sync_annotations(note_id: int):
    import time as _time
    import concurrent.futures as _cf
    conn = get_conn()
    row = conn.execute("SELECT local_path, name FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        return jsonify(ok=False, error="No local file"), 404
    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error="File not found on disk"), 404

    print(f"[notes/sync-annotations] 📌 {row['name']}")
    t0 = _time.time()
    with _cf.ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(_extract_annotations_from_pdf, path)
        try:
            anns = fut.result(timeout=120.0)
        except _cf.TimeoutError:
            return jsonify(ok=False, error=f"Timed out after 120s"), 200
        except Exception as exc:
            return jsonify(ok=False, error=str(exc)), 200

    elapsed = _time.time() - t0
    if not anns:
        print(f"                   ⚠ no annotations ({elapsed:.1f}s)")
        return jsonify(ok=False, error="No annotations found in PDF"), 200

    print(f"                   ✓ {len(anns)} annotation(s) in {elapsed:.1f}s")
    comment = _format_annotations(anns)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = get_conn()
    conn.execute("UPDATE notes SET comment=?, comment_updated_at=? WHERE id=?",
                 (comment, now, note_id))
    conn.commit()
    conn.close()
    return jsonify(ok=True, count=len(anns), comment=comment)


@notes_bp.route("/pin/<int:note_id>", methods=["POST"])
def toggle_pin(note_id: int):
    conn = get_conn()
    row = conn.execute("SELECT pinned FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify(ok=False, error="Not found"), 404
    new_pin = 0 if row["pinned"] else 1
    conn.execute("UPDATE notes SET pinned=? WHERE id=?", (new_pin, note_id))
    conn.commit()
    conn.close()
    return jsonify(ok=True, pinned=bool(new_pin))


@notes_bp.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id: int):
    conn = get_conn()
    row = conn.execute("SELECT local_path FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify(ok=False, error="Not found"), 404
    local_path = row["local_path"]
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    if local_path:
        try:
            Path(local_path).unlink(missing_ok=True)
        except Exception as exc:
            print(f"[notes/delete] could not remove {local_path}: {exc}")
    return jsonify(ok=True)


@notes_bp.route("/reveal-in-finder", methods=["POST"])
def reveal_in_finder():
    ids = (request.get_json(silent=True) or {}).get("ids", [])
    if not ids:
        return jsonify(ok=False, error="No IDs provided"), 400
    conn = get_conn()
    rows = conn.execute(
        f"SELECT local_path FROM notes WHERE id IN ({','.join('?'*len(ids))})", ids
    ).fetchall()
    conn.close()
    paths = [r["local_path"] for r in rows if r["local_path"] and Path(r["local_path"]).exists()]
    if not paths:
        return jsonify(ok=False, error="No valid files found")
    if sys.platform == "darwin":
        posix_list = ", ".join(f'POSIX file "{p}"' for p in paths)
        script = f'tell application "Finder"\n  reveal {{{posix_list}}}\n  activate\nend tell'
        subprocess.Popen(["osascript", "-e", script])
    else:
        for p in paths:
            subprocess.Popen(["xdg-open", str(Path(p).parent)])
    return jsonify(ok=True, count=len(paths))


@notes_bp.route("/move-by-sector", methods=["POST"])
def move_by_sector():
    import re, shutil
    conn = get_conn()
    rows = conn.execute("SELECT id, name, local_path, sector FROM notes").fetchall()
    moved, skipped, errors = [], [], []
    for row in rows:
        src = row["local_path"]
        if not src:
            skipped.append({"id": row["id"], "name": row["name"], "reason": "no path"})
            continue
        src_path = Path(src)
        if not src_path.exists():
            skipped.append({"id": row["id"], "name": row["name"], "reason": "file missing"})
            continue
        sector = (row["sector"] or "").strip()
        if not sector:
            skipped.append({"id": row["id"], "name": row["name"], "reason": "no sector"})
            continue
        safe_sector = re.sub(r'[^\w\s\-]', '_', sector).strip()
        dest_dir = src_path.parent.parent / safe_sector
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / src_path.name
        # avoid overwriting
        if dest_path.exists() and dest_path != src_path:
            stem, suffix = src_path.stem, src_path.suffix
            for i in range(1, 100):
                candidate = dest_dir / f"{stem}_{i}{suffix}"
                if not candidate.exists():
                    dest_path = candidate
                    break
        try:
            shutil.move(str(src_path), str(dest_path))
            conn.execute("UPDATE notes SET local_path=? WHERE id=?", (str(dest_path), row["id"]))
            moved.append({"id": row["id"], "name": row["name"], "dest": str(dest_path)})
        except Exception as exc:
            errors.append({"id": row["id"], "name": row["name"], "error": str(exc)})
    conn.commit()
    conn.close()
    return jsonify(ok=True, moved=len(moved), skipped=len(skipped), errors=errors)


@notes_bp.route("/scan-manual-report")
def scan_manual_report():
    import json as _json

    def _gen():
        conn = get_conn()
        existing = {r[0] for r in conn.execute("SELECT name FROM notes").fetchall()}
        conn.close()

        pdfs = sorted(MANUAL_REPORT_DIR.rglob("*.pdf"))
        yield f"data: Found {len(pdfs)} PDFs in manual_report\n\n"

        added = skipped = 0
        for path in pdfs:
            name = path.name
            if name in existing:
                skipped += 1
                yield f"data: [skip] {name}\n\n"
                continue

            # Insert into DB
            meta = _parse_filename_meta(path.stem)
            now  = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            conn = get_conn()
            cur  = conn.execute(
                """INSERT INTO notes (name, local_path, created_at, type, quarter, report_date, ticker)
                   VALUES (?,?,?,?,?,?,?)""",
                (name, str(path), now,
                 meta.get('type'), meta.get('quarter'), meta.get('report_date'), meta.get('ticker')),
            )
            note_id = cur.lastrowid
            conn.commit()
            conn.close()

            yield f"data: [add] {name} (id={note_id})\n\n"
            added += 1

            # Extract annotations
            try:
                anns = _extract_annotations_from_pdf(path)
                if anns:
                    comment = _format_annotations(anns)
                    conn = get_conn()
                    conn.execute(
                        "UPDATE notes SET comment=?, comment_updated_at=? WHERE id=?",
                        (comment, now, note_id),
                    )
                    conn.commit()
                    conn.close()
                    yield f"data:   → {len(anns)} annotation(s) extracted\n\n"
                else:
                    yield f"data:   → no annotations\n\n"
            except Exception as exc:
                yield f"data:   → annotation error: {exc}\n\n"

        yield f"data: Added {added}, skipped {skipped}\n\n"
        yield "data: __done__\n\n"

    from flask import Response as _Response
    return _Response(_gen(), mimetype="text/event-stream",
                     headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@notes_bp.route("/feed")
def feed():
    from pathlib import Path as _Path
    conn = get_conn()
    raw = conn.execute("""
        SELECT id, name, comment, pinned,
               COALESCE(comment_updated_at, created_at, '') AS date
        FROM   notes
        WHERE  comment IS NOT NULL AND comment != ''
        ORDER  BY pinned DESC, date DESC
    """).fetchall()
    conn.close()
    rows = [dict(r) | {"badge": "📌 pinned" if r["pinned"] else ""} for r in raw]
    tmpl = (_Path(__file__).parent / "templates" / "shared_feed.html").read_text(encoding="utf-8")
    tmpl = tmpl.replace("__NAV__",      nw2.NAV_HTML)
    tmpl = tmpl.replace("__URLPATCH__", nw2.URL_PATCH_JS)
    return render_template_string(tmpl, rows=rows, total=len(rows),
                                  feed_title="Notes Feed",
                                  feed_heading="📎 Notes Feed",
                                  toc_icon="📎")
