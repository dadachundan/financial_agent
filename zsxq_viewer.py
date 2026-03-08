#!/usr/bin/env python3
"""
zsxq_viewer.py — Local web UI for the zsxq PDF index database.

Usage:
    python zsxq_viewer.py
    python zsxq_viewer.py --db zsxq.db --port 8080

Then open http://localhost:8080 in your browser.
PDFs open in a new browser tab when you click "Open PDF".
"""

import argparse
import sqlite3
from pathlib import Path

from flask import Flask, abort, render_template_string, request, send_file

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR / "zsxq.db"

app = Flask(__name__)
DB_PATH: Path = DEFAULT_DB

# ── HTML template ─────────────────────────────────────────────────────────────

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>zsxq PDF Index</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body            { background:#f4f6f8; padding:24px 16px; }
    h2              { font-weight:700; }
    .stat-badges    { gap:8px; flex-wrap:wrap; margin-bottom:12px; }
    .filter-section { margin-bottom:8px; }
    .filter-label   { font-size:.72rem; color:#888; font-weight:600; text-transform:uppercase;
                      letter-spacing:.04em; white-space:nowrap; align-self:center; }
    .filter-row     { gap:6px; flex-wrap:wrap; align-items:center; margin-bottom:6px; }
    .ticker-cloud   { margin-bottom:14px; display:flex; flex-wrap:wrap; gap:5px; align-items:center; }
    .table          { background:#fff; font-size:.83rem; }
    th              { white-space:nowrap; vertical-align:middle; }
    td              { vertical-align:middle; }
    .row-match      { background:#d1f0d8 !important; }
    .row-no-match   { background:#fff !important; }
    .row-unclassed  { background:#fff8e1 !important; }
    .summary-col    { max-width:400px; }
    .summary-short  { display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;
                      overflow:hidden; word-break:break-word; cursor:pointer; }
    .summary-more   { font-size:.72rem; color:#1a56db; cursor:pointer; white-space:nowrap; }
    .summary-more:hover { text-decoration:underline; }
    .name-col       { max-width:180px; word-break:break-all; }
    .title-col      { max-width:200px; word-break:break-word; }
    .analysis-col   { max-width:200px; word-break:break-word; }
    .cat-col        { min-width:80px; }
    .ticker-badge   { font-size:.72rem; font-weight:600; margin:1px 2px; display:inline-block;
                      background:#e8f0fe; color:#1a56db; border:1px solid #c3d3f7;
                      border-radius:4px; padding:1px 5px; white-space:nowrap; }
    .ticker-btn     { font-size:.72rem; font-weight:600; padding:2px 7px; border-radius:4px;
                      white-space:nowrap; cursor:pointer; text-decoration:none; }
    .ticker-btn-on  { background:#1a56db; color:#fff; border:1px solid #1a56db; }
    .ticker-btn-off { background:#e8f0fe; color:#1a56db; border:1px solid #c3d3f7; }
    .ticker-btn-off:hover { background:#c3d3f7; color:#1a56db; }
    .open-btn       { font-size:.75rem; padding:2px 8px; }
    #searchBox      { max-width:240px; }
    .page-footer    { margin-top:24px; font-size:.8rem; color:#888; }
    .count-badge    { font-size:.75rem; }
    .cloud-label    { font-size:.75rem; color:#888; font-weight:600; white-space:nowrap; }
    .active-ticker-pill { font-size:.8rem; }
    .cat-badge      { font-size:.65rem; font-weight:700; padding:1px 4px; border-radius:3px;
                      display:inline-block; margin:1px 0; white-space:nowrap; }
    .cat-yes        { background:#d1f0d8; color:#155724; border:1px solid #b7dfbf; }
    .cat-no         { background:#f0f0f0; color:#999;    border:1px solid #ddd; }
    .cat-unk        { background:#fff8e1; color:#856404; border:1px solid #ffe083; }
  </style>
</head>
<body>
<div class="container-fluid">

  <h2 class="mb-1">📄 zsxq PDF Index</h2>
  <p class="text-muted mb-2" style="font-size:.85rem">DB: {{ db_path }}</p>

  <!-- Stats row -->
  <div class="d-flex stat-badges mb-2">
    <span class="badge bg-dark    fs-6">Total {{ stats.total }}</span>
    <span class="badge bg-primary fs-6">Downloaded {{ stats.downloaded }}</span>
    <span class="badge bg-warning text-dark fs-6">Unclassified {{ stats.unclassified }}</span>
    <span class="badge text-dark fs-6" style="background:#d1f0d8;border:1px solid #b7dfbf">🤖 AI {{ stats.cat_ai }}</span>
    <span class="badge text-dark fs-6" style="background:#d1ecf1;border:1px solid #bee5eb">🦾 Robotics {{ stats.cat_robotics }}</span>
    <span class="badge text-dark fs-6" style="background:#e2d9f3;border:1px solid #c5b3e6">💡 Semi {{ stats.cat_semi }}</span>
    <span class="badge text-dark fs-6" style="background:#fff3cd;border:1px solid #ffe083">⚡ Energy {{ stats.cat_energy }}</span>
  </div>

  <!-- Status filters -->
  <div class="filter-section">
    <div class="d-flex filter-row">
      <span class="filter-label">Status:</span>
      <a href="?filter=all{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-dark' if current_filter=='all' else 'btn-outline-dark' }}">All ({{ stats.total }})</a>
      <a href="?filter=downloaded{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-primary' if current_filter=='downloaded' else 'btn-outline-primary' }}">Downloaded ({{ stats.downloaded }})</a>
      <a href="?filter=unclassified{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-warning text-dark' if current_filter=='unclassified' else 'btn-outline-warning' }}">Unclassified ({{ stats.unclassified }})</a>
    </div>

    <!-- Category filters -->
    <div class="d-flex filter-row">
      <span class="filter-label">Category:</span>
      <a href="?filter=cat_ai{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-success' if current_filter=='cat_ai' else 'btn-outline-success' }}">🤖 AI ({{ stats.cat_ai }})</a>
      <a href="?filter=cat_robotics{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-info' if current_filter=='cat_robotics' else 'btn-outline-info' }}">🦾 Robotics ({{ stats.cat_robotics }})</a>
      <a href="?filter=cat_semi{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-secondary' if current_filter=='cat_semi' else 'btn-outline-secondary' }}">💡 Semiconductor ({{ stats.cat_semi }})</a>
      <a href="?filter=cat_energy{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-warning text-dark' if current_filter=='cat_energy' else 'btn-outline-warning' }}">⚡ Energy ({{ stats.cat_energy }})</a>
      <a href="?filter=cat_any{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-dark' if current_filter=='cat_any' else 'btn-outline-dark' }}">Any category ({{ stats.cat_any }})</a>
      <a href="?filter=cat_none{{ '&ticker=' ~ current_ticker if current_ticker else '' }}"
         class="btn btn-sm {{ 'btn-light border' if current_filter=='cat_none' else 'btn-outline-secondary' }}">None ({{ stats.cat_none }})</a>

      <!-- Search box -->
      <input id="searchBox" type="text" class="form-control form-control-sm ms-2"
             placeholder="Search name / title / ticker…" oninput="liveSearch(this.value)">
      <span id="matchCount" class="text-muted small align-self-center ms-1"></span>
    </div>
  </div>

  <!-- Ticker filter cloud -->
  {% if all_tickers %}
  <div class="ticker-cloud">
    <span class="cloud-label">Ticker:</span>
    {% if current_ticker %}
      <a href="?filter={{ current_filter }}"
         class="btn btn-sm btn-outline-secondary active-ticker-pill">
        ✕ {{ current_ticker }}
      </a>
    {% endif %}
    {% for t in all_tickers %}
      {% if t != current_ticker %}
        <a href="?filter={{ current_filter }}&ticker={{ t }}"
           class="ticker-btn ticker-btn-off">{{ t }}</a>
      {% endif %}
    {% endfor %}
  </div>
  {% endif %}

  <!-- Table -->
  <div class="table-responsive shadow-sm rounded">
    <table class="table table-bordered table-hover mb-0" id="mainTable">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Date</th>
          <th>File name</th>
          <th>Title</th>
          <th>Categories</th>
          <th>Tickers</th>
          <th>Size</th>
          <th>Summary</th>
          <th>PDF</th>
          <th>Analysis</th>
        </tr>
      </thead>
      <tbody>
        {% for idx, row in rows %}
        {%- set any_cat = (row.ai_related == 1 or row.robotics_related == 1
                           or row.semiconductor_related == 1 or row.energy_related == 1) %}
        {%- set unclassed = (row.ai_related is none) %}
        <tr class="{{ 'row-match' if any_cat else ('row-unclassed' if unclassed else 'row-no-match') }}"
            data-search="{{ (row.name ~ ' ' ~ (row.topic_title or '') ~ ' ' ~ (row.tickers or ''))|lower }}">
          <td class="text-muted">{{ idx }}</td>
          <td class="text-nowrap">{{ (row.create_time or '')[:10] }}</td>
          <td class="name-col">{{ row.name }}</td>
          <td class="title-col">{{ row.topic_title or '—' }}</td>

          <!-- 4-category badges -->
          <td class="cat-col">
            {%- macro cat_badge(val, label) %}
              {%- if val == 1 %}
                <span class="cat-badge cat-yes">{{ label }}</span>
              {%- elif val == 0 %}
                <span class="cat-badge cat-no">{{ label }}</span>
              {%- else %}
                <span class="cat-badge cat-unk">{{ label }}?</span>
              {%- endif %}
            {%- endmacro %}
            {{ cat_badge(row.ai_related,           '🤖 AI') }}
            {{ cat_badge(row.robotics_related,     '🦾 Rob') }}
            {{ cat_badge(row.semiconductor_related,'💡 Semi') }}
            {{ cat_badge(row.energy_related,       '⚡ Nrg') }}
          </td>

          <td style="max-width:80px">
            {% if row.tickers %}
              {% set ticker_list = row.tickers.split(',') %}
              {% for t in ticker_list[:5] %}
                {% set t = t.strip() %}
                <a href="?filter={{ current_filter }}&ticker={{ t }}"
                   class="ticker-badge" style="text-decoration:none"
                   title="Filter by {{ t }}">{{ t }}</a>
              {% endfor %}
              {% if ticker_list|length > 5 %}
                <span class="text-muted" style="font-size:.65rem">+{{ ticker_list|length - 5 }}</span>
              {% endif %}
            {% else %}
              <span class="text-muted">—</span>
            {% endif %}
          </td>

          <td class="text-end text-nowrap">
            {{ '%.1f MB' % (row.file_size / 1048576) if row.file_size else '—' }}
          </td>

          <td class="summary-col">
            {% if row.summary %}
              <div class="summary-short"
                   onclick="showSummary({{ row.file_id }}, this)"
                   data-full="{{ row.summary|e }}"
                   data-title="{{ (row.topic_title or row.name)|e }}"
                   title="Click to expand">{{ row.summary }}</div>
              {% if row.summary|length > 120 %}
                <span class="summary-more" onclick="showSummary({{ row.file_id }}, this.previousElementSibling)">more ↗</span>
              {% endif %}
            {% else %}—{% endif %}
          </td>

          <td class="text-center">
            {% if row.local_path %}
              <a href="/pdf/{{ row.file_id }}/{{ row.name }}" target="_blank"
                 class="btn btn-outline-danger open-btn">📄 Open</a>
            {% else %}
              <span class="text-muted">—</span>
            {% endif %}
          </td>

          <td class="analysis-col text-muted">
            {{ (row.categories_analysis or row.ai_robotics_analysis or '')[:180] or '—' }}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <p class="page-footer">Showing <span id="visibleCount">{{ rows|length }}</span> of {{ rows|length }} rows.</p>
</div>

<!-- Summary modal -->
<div class="modal fade" id="summaryModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="summaryModalTitle" style="font-size:.95rem;word-break:break-word"></h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" id="summaryModalBody"
           style="white-space:pre-wrap;word-break:break-word;font-size:.9rem;line-height:1.7"></div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
  const _summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
  function showSummary(fileId, el) {
    document.getElementById('summaryModalTitle').textContent = el.dataset.title || '';
    document.getElementById('summaryModalBody').textContent  = el.dataset.full  || '';
    _summaryModal.show();
  }

  function liveSearch(q) {
    q = q.toLowerCase().trim();
    let visible = 0;
    document.querySelectorAll('#mainTable tbody tr').forEach(tr => {
      const match = !q || tr.dataset.search.includes(q);
      tr.style.display = match ? '' : 'none';
      if (match) visible++;
    });
    document.getElementById('visibleCount').textContent = visible;
    const mc = document.getElementById('matchCount');
    mc.textContent = q ? visible + ' match' + (visible !== 1 ? 'es' : '') : '';
  }
</script>
</body>
</html>
"""

# ── Routes ────────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _get_all_tickers(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT tickers FROM pdf_files WHERE tickers IS NOT NULL AND tickers != ''"
    ).fetchall()
    seen: set[str] = set()
    for r in rows:
        for t in r["tickers"].split(","):
            t = t.strip()
            if t:
                seen.add(t)
    return sorted(seen)


@app.route("/")
def index():
    f      = request.args.get("filter", "all")
    ticker = request.args.get("ticker", "").strip().upper()

    conn = get_conn()

    stats = conn.execute(
        "SELECT "
        "  COUNT(*)                                                          AS total, "
        "  SUM(CASE WHEN local_path IS NOT NULL          THEN 1 ELSE 0 END) AS downloaded, "
        "  SUM(CASE WHEN ai_related IS NULL              THEN 1 ELSE 0 END) AS unclassified, "
        "  SUM(CASE WHEN ai_related          = 1         THEN 1 ELSE 0 END) AS cat_ai, "
        "  SUM(CASE WHEN robotics_related    = 1         THEN 1 ELSE 0 END) AS cat_robotics, "
        "  SUM(CASE WHEN semiconductor_related = 1       THEN 1 ELSE 0 END) AS cat_semi, "
        "  SUM(CASE WHEN energy_related      = 1         THEN 1 ELSE 0 END) AS cat_energy, "
        "  SUM(CASE WHEN (ai_related=1 OR robotics_related=1 "
        "               OR semiconductor_related=1 OR energy_related=1) "
        "               THEN 1 ELSE 0 END)                                  AS cat_any, "
        "  SUM(CASE WHEN (ai_related=0 AND robotics_related=0 "
        "               AND semiconductor_related=0 AND energy_related=0) "
        "               THEN 1 ELSE 0 END)                                  AS cat_none "
        "FROM pdf_files"
    ).fetchone()

    # Build WHERE clause
    conditions: list[str] = []
    params: list = []

    filter_cond = {
        "downloaded":   "local_path IS NOT NULL",
        "unclassified": "ai_related IS NULL",
        "cat_ai":       "ai_related = 1",
        "cat_robotics": "robotics_related = 1",
        "cat_semi":     "semiconductor_related = 1",
        "cat_energy":   "energy_related = 1",
        "cat_any":      "(ai_related=1 OR robotics_related=1 OR semiconductor_related=1 OR energy_related=1)",
        "cat_none":     "(ai_related=0 AND robotics_related=0 AND semiconductor_related=0 AND energy_related=0)",
    }.get(f)
    if filter_cond:
        conditions.append(filter_cond)

    if ticker:
        conditions.append("tickers LIKE ?")
        params.append(f"%{ticker}%")

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    rows = conn.execute(
        f"SELECT * FROM pdf_files {where_clause} ORDER BY create_time DESC",
        params,
    ).fetchall()

    all_tickers = _get_all_tickers(conn)
    conn.close()

    return render_template_string(
        TEMPLATE,
        rows=list(enumerate(rows, 1)),
        stats=stats,
        current_filter=f,
        current_ticker=ticker,
        all_tickers=all_tickers,
        db_path=DB_PATH,
    )


@app.route("/pdf/<int:file_id>")
@app.route("/pdf/<int:file_id>/<filename>")
def serve_pdf(file_id: int, filename: str = ""):
    conn = get_conn()
    row = conn.execute(
        "SELECT local_path FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    conn.close()

    if not row or not row["local_path"]:
        abort(404, "No local file recorded for this PDF.")

    path = Path(row["local_path"])
    if not path.exists():
        abort(404, f"File not found on disk: {path}")

    return send_file(path, mimetype="application/pdf",
                     download_name=path.name, as_attachment=False)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Local web viewer for the zsxq PDF index database."
    )
    parser.add_argument("--db", default=str(DEFAULT_DB),
                        help=f"SQLite DB path (default: {DEFAULT_DB})")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to listen on (default: 8080)")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host to bind (default: 0.0.0.0 = all interfaces)")
    args = parser.parse_args()

    global DB_PATH
    DB_PATH = Path(args.db).expanduser()

    if not DB_PATH.exists():
        print(f"ERROR: database not found at {DB_PATH}")
        raise SystemExit(1)

    import socket
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"  zsxq viewer →  http://127.0.0.1:{args.port}  (localhost)")
    print(f"  zsxq viewer →  http://{local_ip}:{args.port}  (LAN)")
    print(f"  DB           →  {DB_PATH}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
