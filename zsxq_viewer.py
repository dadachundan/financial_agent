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
    .stat-badges    { gap:8px; flex-wrap:wrap; margin-bottom:18px; }
    .filter-bar     { gap:8px; flex-wrap:wrap; margin-bottom:14px; align-items:center; }
    .table          { background:#fff; font-size:.83rem; }
    th              { white-space:nowrap; vertical-align:middle; }
    td              { vertical-align:middle; }
    .row-ai         { background:#d1f0d8 !important; }
    .row-not-ai     { background:#fff !important; }
    .row-unclassed  { background:#fff8e1 !important; }
    .summary-col    { max-width:340px; white-space:pre-wrap; word-break:break-word; }
    .name-col       { max-width:200px; word-break:break-all; }
    .title-col      { max-width:220px; word-break:break-word; }
    .analysis-col   { max-width:240px; word-break:break-word; }
    .open-btn       { font-size:.75rem; padding:2px 8px; }
    #searchBox      { max-width:260px; }
    .page-footer    { margin-top:24px; font-size:.8rem; color:#888; }
    .count-badge    { font-size:.75rem; }
  </style>
</head>
<body>
<div class="container-fluid">

  <h2 class="mb-1">📄 zsxq PDF Index</h2>
  <p class="text-muted mb-3" style="font-size:.85rem">DB: {{ db_path }}</p>

  <!-- Stats -->
  <div class="d-flex stat-badges mb-3">
    <span class="badge bg-dark   fs-6">Total {{ stats.total }}</span>
    <span class="badge bg-success fs-6">AI/Robotics {{ stats.yes }}</span>
    <span class="badge bg-secondary fs-6">Not AI {{ stats.no }}</span>
    <span class="badge bg-warning text-dark fs-6">Unclassified {{ stats.unclassified }}</span>
    <span class="badge bg-primary fs-6">Downloaded {{ stats.downloaded }}</span>
  </div>

  <!-- Filters + search -->
  <div class="d-flex filter-bar">
    <a href="?filter=all"          class="btn btn-sm {{ 'btn-dark'              if current_filter=='all'          else 'btn-outline-dark' }}">All ({{ stats.total }})</a>
    <a href="?filter=ai"           class="btn btn-sm {{ 'btn-success'           if current_filter=='ai'           else 'btn-outline-success' }}">AI only ({{ stats.yes }})</a>
    <a href="?filter=not_ai"       class="btn btn-sm {{ 'btn-secondary'         if current_filter=='not_ai'       else 'btn-outline-secondary' }}">Not AI ({{ stats.no }})</a>
    <a href="?filter=unclassified" class="btn btn-sm {{ 'btn-warning text-dark' if current_filter=='unclassified' else 'btn-outline-warning' }}">Unclassified ({{ stats.unclassified }})</a>
    <a href="?filter=downloaded"   class="btn btn-sm {{ 'btn-primary'           if current_filter=='downloaded'   else 'btn-outline-primary' }}">Downloaded ({{ stats.downloaded }})</a>
    <input id="searchBox" type="text" class="form-control form-control-sm"
           placeholder="Search name / title…" oninput="liveSearch(this.value)">
    <span id="matchCount" class="text-muted small align-self-center"></span>
  </div>

  <!-- Table -->
  <div class="table-responsive shadow-sm rounded">
    <table class="table table-bordered table-hover mb-0" id="mainTable">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Date</th>
          <th>File name</th>
          <th>Title</th>
          <th>AI?</th>
          <th>Size</th>
          <th>Summary</th>
          <th>PDF</th>
          <th>Analysis</th>
        </tr>
      </thead>
      <tbody>
        {% for idx, row in rows %}
        <tr class="{{ 'row-ai' if row.ai_robotics_related == 1 else ('row-unclassed' if row.ai_robotics_related is none else 'row-not-ai') }}"
            data-search="{{ (row.name ~ ' ' ~ (row.topic_title or ''))|lower }}">
          <td class="text-muted">{{ idx }}</td>
          <td class="text-nowrap">{{ (row.create_time or '')[:10] }}</td>
          <td class="name-col">{{ row.name }}</td>
          <td class="title-col">{{ row.topic_title or '—' }}</td>
          <td class="text-center">
            {% if row.ai_robotics_related == 1 %}
              <span class="badge bg-success">Yes</span>
            {% elif row.ai_robotics_related == 0 %}
              <span class="badge bg-secondary">No</span>
            {% else %}
              <span class="badge bg-warning text-dark">?</span>
            {% endif %}
          </td>
          <td class="text-end text-nowrap">
            {{ '%.1f MB' % (row.file_size / 1048576) if row.file_size else '—' }}
          </td>
          <td class="summary-col">
            {% if row.summary %}
              <span data-bs-toggle="tooltip" data-bs-placement="left"
                    title="{{ row.summary|e }}">
                {{ row.summary[:220] }}{% if row.summary|length > 220 %}…{% endif %}
              </span>
            {% else %}—{% endif %}
          </td>
          <td class="text-center">
            {% if row.local_path %}
              <a href="/pdf/{{ row.file_id }}" target="_blank"
                 class="btn btn-outline-danger open-btn">📄 Open</a>
            {% else %}
              <span class="text-muted">—</span>
            {% endif %}
          </td>
          <td class="analysis-col text-muted">
            {{ row.ai_robotics_analysis[:180] if row.ai_robotics_analysis else '—' }}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <p class="page-footer">Showing <span id="visibleCount">{{ rows|length }}</span> of {{ rows|length }} rows.</p>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
  // Bootstrap tooltips
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el, { html: false });
  });

  // Live search
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


@app.route("/")
def index():
    f = request.args.get("filter", "all")
    conn = get_conn()

    stats = conn.execute(
        "SELECT "
        "  COUNT(*)                                                   AS total, "
        "  SUM(CASE WHEN ai_robotics_related = 1   THEN 1 ELSE 0 END) AS yes, "
        "  SUM(CASE WHEN ai_robotics_related = 0   THEN 1 ELSE 0 END) AS no, "
        "  SUM(CASE WHEN ai_robotics_related IS NULL THEN 1 ELSE 0 END) AS unclassified, "
        "  SUM(CASE WHEN local_path IS NOT NULL     THEN 1 ELSE 0 END) AS downloaded "
        "FROM pdf_files"
    ).fetchone()

    where = {
        "all":          "",
        "ai":           "WHERE ai_robotics_related = 1",
        "not_ai":       "WHERE ai_robotics_related = 0",
        "unclassified": "WHERE ai_robotics_related IS NULL",
        "downloaded":   "WHERE local_path IS NOT NULL",
    }.get(f, "")

    rows = conn.execute(
        f"SELECT * FROM pdf_files {where} ORDER BY create_time DESC"
    ).fetchall()
    conn.close()

    return render_template_string(
        TEMPLATE,
        rows=list(enumerate(rows, 1)),
        stats=stats,
        current_filter=f,
        db_path=DB_PATH,
    )


@app.route("/pdf/<int:file_id>")
def serve_pdf(file_id: int):
    """Serve a local PDF file so the browser can open it in a new tab."""
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

    return send_file(path, mimetype="application/pdf")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Local web viewer for the zsxq PDF index database."
    )
    parser.add_argument("--db", default=str(DEFAULT_DB),
                        help=f"SQLite DB path (default: {DEFAULT_DB})")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to listen on (default: 8080)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind (default: 127.0.0.1)")
    args = parser.parse_args()

    global DB_PATH
    DB_PATH = Path(args.db).expanduser()

    if not DB_PATH.exists():
        print(f"ERROR: database not found at {DB_PATH}")
        raise SystemExit(1)

    print(f"  zsxq viewer →  http://{args.host}:{args.port}")
    print(f"  DB           →  {DB_PATH}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
