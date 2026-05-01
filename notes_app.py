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
import shutil
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

SCRIPT_DIR   = Path(__file__).parent
DB_PATH      = SCRIPT_DIR / "db" / "notes.db"
PDFS_DIR     = SCRIPT_DIR / "notes_pdfs"
MANUAL_REPORT_DIR = Path.home() / "Downloads" / "zsxq_report" / "manual_report"

notes_bp = Blueprint("notes", __name__)


# ── Database ──────────────────────────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    PDFS_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            name               TEXT NOT NULL,
            local_path         TEXT,
            comment            TEXT,
            comment_updated_at TEXT,
            created_at         TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
            pinned             INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


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

    /* Two-column notes table */
    .notes-table { width:100%; border-collapse:separate; border-spacing:0; }
    .notes-table thead th {
      background:#212529; color:#fff; font-size:.78rem; font-weight:600;
      letter-spacing:.06em; text-transform:uppercase; padding:10px 14px;
      position:sticky; top:0; z-index:2;
    }
    .notes-table thead th:first-child { border-radius:8px 0 0 0; }
    .notes-table thead th:last-child  { border-radius:0 8px 0 0; }
    .notes-table tbody tr { vertical-align:top; }
    .notes-table tbody tr:hover > td { background:#f0f4fb; }

    .pdf-cell {
      width:55%; border:none; border-bottom:1px solid #e8eaed;
      border-right:1px solid #e8eaed; background:#fff; padding:0;
    }
    .comment-cell {
      width:45%; border:none; border-bottom:1px solid #e8eaed;
      background:#fff; padding:12px 14px; vertical-align:top;
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

    /* Upload area */
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
    <a href="{{ _base | default('') }}/feed" class="btn btn-sm btn-outline-secondary ms-auto">📓 Feed View</a>
  </div>

  <!-- Upload zone -->
  <div class="upload-zone" id="uploadZone">
    <p>📄 <b>Click or drag &amp; drop</b> a PDF to upload</p>
    <p class="mt-1" style="font-size:.78rem">Accepts .pdf files up to 50 MB</p>
    <input type="file" id="fileInput" accept=".pdf" style="display:none">
    <div id="uploadProgress" class="mt-2">
      <div class="progress" style="height:6px;max-width:300px;margin:0 auto">
        <div class="progress-bar progress-bar-striped progress-bar-animated"
             id="uploadBar" style="width:100%"></div>
      </div>
      <p class="text-muted mt-1" style="font-size:.78rem" id="uploadMsg">Uploading…</p>
    </div>
  </div>

  <!-- Notes table -->
  {% if rows %}
  <table class="notes-table">
    <thead>
      <tr>
        <th>PDF</th>
        <th>Comment</th>
      </tr>
    </thead>
    <tbody id="notesBody">
      {% for row in rows %}
      <tr id="row-{{ row.id }}" class="{% if row.pinned %}pinned-row{% endif %}">
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
              {% if row.pinned %} · 📌 pinned{% endif %}
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

__MCW_MODALS__

<script src="/static/vendor/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
const _base = "{{ _base | default('') }}";
window._commentSavePrefix = '';

__MCW_JS__

// ── Upload ────────────────────────────────────────────────────────────────────
const uploadZone = document.getElementById('uploadZone');
const fileInput  = document.getElementById('fileInput');

uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', ()  => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', e => {
  e.preventDefault(); uploadZone.classList.remove('dragover');
  const f = e.dataTransfer.files[0];
  if (f) uploadFile(f);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) uploadFile(fileInput.files[0]); });

function uploadFile(file) {
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    alert('Only PDF files are supported.'); return;
  }
  document.getElementById('uploadProgress').style.display = 'block';
  document.getElementById('uploadMsg').textContent = 'Uploading ' + file.name + '…';
  const fd = new FormData();
  fd.append('pdf', file);
  fetch('/upload', { method: 'POST', body: fd })
    .then(r => r.json())
    .then(data => {
      document.getElementById('uploadProgress').style.display = 'none';
      fileInput.value = '';
      if (data.ok) {
        window.location.reload();
      } else {
        alert(data.error || 'Upload failed');
      }
    })
    .catch(() => {
      document.getElementById('uploadProgress').style.display = 'none';
      alert('Upload failed');
    });
}

// ── Row actions ───────────────────────────────────────────────────────────────
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
          const base = meta.textContent.replace(/·\s*📌\s*pinned/g, '').trim();
          meta.textContent = d.pinned ? base + ' · 📌 pinned' : base;
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
        SELECT id, name, comment, created_at, comment_updated_at, pinned
        FROM   notes
        ORDER  BY pinned DESC, COALESCE(comment_updated_at, created_at) DESC
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

    PDFS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(f.filename).name
    dest = PDFS_DIR / safe_name
    # Avoid collisions
    stem = dest.stem; i = 1
    while dest.exists():
        dest = PDFS_DIR / f"{stem}_{i}.pdf"; i += 1

    f.save(dest)

    # Mirror copy to ~/Downloads/zsxq_report/manual_report/YYYY-MM-DD/
    today = datetime.date.today().isoformat()
    mirror_dir = MANUAL_REPORT_DIR / today
    mirror_dir.mkdir(parents=True, exist_ok=True)
    mirror_dest = mirror_dir / dest.name
    _i = 1
    while mirror_dest.exists():
        mirror_dest = mirror_dir / f"{dest.stem}_{_i}.pdf"; _i += 1
    shutil.copy2(dest, mirror_dest)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = get_conn()
    conn.execute(
        "INSERT INTO notes (name, local_path, created_at) VALUES (?,?,?)",
        (dest.name, str(dest), now),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True, mirror=str(mirror_dest))


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
        p = Path(local_path)
        try:
            p.unlink(missing_ok=True)
        except Exception as exc:
            print(f"[notes/delete] could not remove {p}: {exc}")
        # Also remove the dated mirror copy under ~/Downloads/zsxq_report/manual_report/
        for dated_dir in MANUAL_REPORT_DIR.glob("*/"):
            mirror = dated_dir / p.name
            if mirror.exists():
                try:
                    mirror.unlink()
                except Exception as exc:
                    print(f"[notes/delete] could not remove mirror {mirror}: {exc}")
    return jsonify(ok=True)


@notes_bp.route("/feed")
def feed():
    from pathlib import Path as _Path
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, name, comment, created_at, comment_updated_at, pinned
        FROM   notes
        WHERE  comment IS NOT NULL AND comment != ''
        ORDER  BY pinned DESC, COALESCE(comment_updated_at, created_at) DESC
    """).fetchall()
    conn.close()
    tmpl = (_Path(__file__).parent / "templates" / "notes_feed.html").read_text(encoding="utf-8")
    tmpl = tmpl.replace("__NAV__",      nw2.NAV_HTML)
    tmpl = tmpl.replace("__URLPATCH__", nw2.URL_PATCH_JS)
    return render_template_string(tmpl, rows=rows, total=len(rows))
