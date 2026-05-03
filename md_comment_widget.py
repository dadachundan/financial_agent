#!/usr/bin/env python3
"""
md_comment_widget.py — Shared EasyMDE markdown comment editor widget for Flask apps.

Provides HTML/CSS/JS fragments to embed in Flask templates, plus a Blueprint that
registers /upload-image and /uploads/<path> routes shared across apps.

Usage
-----
In your Flask app::

    import md_comment_widget as mcw

    UPLOADS_DIR = SCRIPT_DIR / "uploads"
    app = Flask(__name__)
    app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))

    # Place these placeholders anywhere in your TEMPLATE string:
    #   __MCW_HEAD__    inside <head>    — EasyMDE CSS + marked.js CDN
    #   __MCW_CSS__     inside <style>   — comment-preview & modal styles
    #   __MCW_MODALS__  before </body>   — Bootstrap modals for preview + editor
    #   __MCW_FOOTER__  before </body>   — EasyMDE JS CDN
    #   __MCW_JS__      inside <script>  — comment editor JS functions

    # Apply substitutions right after the TEMPLATE string is defined:
    for _k, _v in mcw.TEMPLATE_PARTS.items():
        TEMPLATE = TEMPLATE.replace(_k, _v)

App requirements
----------------
* Bootstrap 5 JS must already be loaded (``bootstrap.Modal`` is used).
* Each row's comment ``<td>`` must have ``id="comment-cell-<id>"`` and contain
  a child ``<span class="comment-preview" data-comment="...html-escaped markdown...">``.
* Provide a ``POST /comment/<int:id>`` route that persists the comment.
* For AJAX-rendered rows (client-side), call ``renderAllCommentCells()`` after
  updating ``tbody.innerHTML``.
"""

import datetime
import uuid
from pathlib import Path

from flask import Blueprint, abort, jsonify, request, send_file


# ── CDN links ─────────────────────────────────────────────────────────────────

HEAD_LINKS = (
    '  <link href="/static/vendor/easymde.min.css" rel="stylesheet">\n'
    '  <script src="/static/vendor/marked.min.js"></script>'
)

FOOTER_SCRIPTS = (
    '<script src="/static/vendor/easymde.min.js"></script>'
)


# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """\
    /* ── Comment widget ───────────────────────────────────────────────────── */
    .comment-preview { cursor:pointer; display:block; min-height:1.2em; max-height:4.5em;
                       overflow:hidden; position:relative; }
    .comment-preview::after { content:''; position:absolute; bottom:0; left:0; right:0;
                               height:1.2em; background:linear-gradient(transparent,#fff); }
    .comment-preview:hover { background:rgba(0,0,0,.03); border-radius:3px; }
    .comment-preview p  { margin:0 0 .2em; }
    .comment-preview ul,.comment-preview ol { padding-left:1.2em; margin:0 0 .2em; }
    .comment-preview img { max-height:3em; border-radius:3px; }
    .comment-preview code { font-size:.8em; background:#f0f0f0; padding:1px 3px; border-radius:2px; }
    .comment-preview blockquote { border-left:3px solid #d0d7de; margin:.1em 0; padding:.1em .5em; color:#555; }
    /* Comment preview modal body */
    #commentPreviewBody img  { max-width:100%; border-radius:6px; margin:.4em 0; display:block; }
    #commentPreviewBody p    { margin-bottom:.6em; }
    #commentPreviewBody ul,
    #commentPreviewBody ol   { padding-left:1.4em; margin-bottom:.6em; }
    #commentPreviewBody code { background:#f0f0f0; padding:1px 4px; border-radius:3px; font-size:.88em; }
    #commentPreviewBody pre  { background:#f6f8fa; padding:.75em; border-radius:6px; overflow:auto; }
    #commentPreviewBody blockquote { border-left:4px solid #d0d7de; margin:.5em 0; padding:.4em .8em;
                                     color:#555; background:#f6f8fa; border-radius:0 4px 4px 0; }
    #commentPreviewBody h1  { font-size:.8rem; font-weight:600; color:#888; margin:0 0 1em;
                               letter-spacing:.04em; border-bottom:1px solid #eee; padding-bottom:.4em; }
    #commentPreviewBody h2  { font-size:1rem; font-weight:700; color:#1a56db; margin:1.2em 0 .4em;
                               text-transform:uppercase; letter-spacing:.05em; }
    /* EasyMDE inside modal */
    #commentModal .EasyMDEContainer { height:100%; }
    #commentModal .CodeMirror       { min-height:220px; font-size:.9rem; }\
"""


# ── Modals ────────────────────────────────────────────────────────────────────

MODALS_HTML = """\
<!-- Comment preview modal -->
<div class="modal fade" id="commentPreviewModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-xl modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">💬 Comment</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" id="commentPreviewBody"
           style="font-size:.95rem;line-height:1.75;word-break:break-word"></div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="commentPreviewEditBtn">✏️ Edit</button>
      </div>
    </div>
  </div>
</div>

<!-- Comment editor modal -->
<div class="modal fade" id="commentModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-scrollable">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">✏️ Edit Comment</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body" style="min-height:340px">
        <textarea id="commentEditorTextarea"></textarea>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary" id="commentSaveBtn">Save</button>
      </div>
    </div>
  </div>
</div>\
"""


# ── JavaScript ────────────────────────────────────────────────────────────────
# Requires: Bootstrap 5 JS (bootstrap.Modal), EasyMDE, marked.js.
# Each comment <td> must have  id="comment-cell-<id>"  and contain a child
#   <span class="comment-preview" data-comment="...html-escaped markdown...">.
# App must expose  POST /comment/<id>  accepting form field  comment=<markdown>.
# For AJAX-rendered rows, call  renderAllCommentCells()  after DOM update.

JS = """\
  // ----------------------------------------
  const _commentModal        = new bootstrap.Modal(document.getElementById('commentModal'));
  const _commentPreviewModal = new bootstrap.Modal(document.getElementById('commentPreviewModal'));
  let _easyMDE       = null;
  let _editingItemId = null;
  let _previewSpan   = null;

  function _getEasyMDE() {
    if (_easyMDE) return _easyMDE;
    _easyMDE = new EasyMDE({
      element: document.getElementById('commentEditorTextarea'),
      spellChecker: false,
      minHeight: '240px',
      toolbar: [
        'bold','italic','heading','|',
        'quote','unordered-list','ordered-list','|',
        'link','upload-image','|',
        'preview','side-by-side','fullscreen'
      ],
      imageUploadFunction(file, onSuccess, onError) {
        const fd = new FormData();
        fd.append('image', file);
        fetch('/upload-image', { method: 'POST', body: fd })
          .then(r => r.json())
          .then(d => d.data ? onSuccess(d.data.filePath) : onError(d.error || 'Upload failed'))
          .catch(() => onError('Upload failed'));
      },
    });
    // Clipboard paste → detect image and upload automatically
    _easyMDE.codemirror.on('paste', (cm, e) => {
      const items = e.clipboardData && e.clipboardData.items;
      if (!items) return;
      for (const item of items) {
        if (item.type.startsWith('image/')) {
          e.preventDefault();
          const file = item.getAsFile();
          const fd = new FormData();
          fd.append('image', file, 'pasted-image.png');
          fetch('/upload-image', { method: 'POST', body: fd })
            .then(r => r.json())
            .then(d => {
              if (d.data && d.data.filePath)
                cm.replaceSelection('![image](' + d.data.filePath + ')');
            });
          break;
        }
      }
    });
    return _easyMDE;
  }

  // Click on comment cell → open preview modal
  function viewComment(itemId, span) {
    _editingItemId = itemId;
    _previewSpan   = span;
    const comment = span.dataset.comment || '';
    const body    = document.getElementById('commentPreviewBody');
    body.innerHTML = comment ? marked.parse(comment)
                             : '<em class="text-muted">No comment yet. Click Edit to add one.</em>';
    _commentPreviewModal.show();
  }

  // "Edit" button inside preview modal → switch to EasyMDE editor
  document.getElementById('commentPreviewEditBtn').addEventListener('click', () => {
    _commentPreviewModal.hide();
    setTimeout(() => editComment(_editingItemId, _previewSpan), 300);
  });

  function editComment(itemId, span) {
    _editingItemId = itemId;
    const mde = _getEasyMDE();
    mde.value(span.dataset.comment || '');
    _commentModal.show();
    setTimeout(() => mde.codemirror.focus(), 320);
  }

  document.getElementById('commentSaveBtn').addEventListener('click', () => {
    const val = _easyMDE ? _easyMDE.value().trim() : '';
    fetch((window._commentSavePrefix||'') + '/comment/' + _editingItemId, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'comment=' + encodeURIComponent(val),
    }).then(r => {
      if (r.ok) {
        const cell = document.getElementById('comment-cell-' + _editingItemId);
        if (cell) renderCommentCell(cell, _editingItemId, val);
        _commentModal.hide();
      }
    });
  });

  function renderCommentCell(cell, itemId, comment) {
    const span = document.createElement('span');
    span.className       = 'comment-preview';
    span.dataset.comment = comment || '';
    span.title           = 'Click to preview / edit';
    if (comment) {
      span.innerHTML = marked.parse(comment);
    } else {
      span.textContent = '—';
    }
    span.onclick = () => viewComment(itemId, span);
    cell.innerHTML = ''; cell.appendChild(span);
    if (typeof window._onCommentRendered === 'function') window._onCommentRendered(cell);
  }

  // Render all .comment-preview spans — call on page load and after AJAX DOM updates
  function renderAllCommentCells() {
    document.querySelectorAll('.comment-preview').forEach(span => {
      const comment = span.dataset.comment || '';
      const itemId  = span.closest('td').id.replace('comment-cell-', '');
      if (comment) { span.innerHTML = marked.parse(comment); }
      else         { span.textContent = '—'; }
      span.onclick = () => viewComment(itemId, span);
      if (typeof window._onCommentRendered === 'function') window._onCommentRendered(span.parentElement);
    });
  }

  document.addEventListener('DOMContentLoaded', renderAllCommentCells);\
"""


# ── Convenience dict for template substitution ────────────────────────────────

TEMPLATE_PARTS = {
    "__MCW_HEAD__":   HEAD_LINKS,
    "__MCW_CSS__":    CSS,
    "__MCW_MODALS__": MODALS_HTML,
    "__MCW_FOOTER__": FOOTER_SCRIPTS,
    "__MCW_JS__":     JS,
}


# ── Flask Blueprint ───────────────────────────────────────────────────────────

def create_blueprint(uploads_dir: Path) -> Blueprint:
    """Return a Flask Blueprint with /upload-image and /uploads/<path> routes.

    Register with::

        app.register_blueprint(md_comment_widget.create_blueprint(UPLOADS_DIR))
    """
    uploads_dir = Path(uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    bp = Blueprint("md_comment_widget", __name__)

    @bp.route("/uploads/<path:filename>")
    def serve_upload(filename: str):
        path = uploads_dir / filename
        if not path.exists():
            abort(404)
        return send_file(path)

    @bp.route("/upload-image", methods=["POST"])
    def upload_image():
        f = request.files.get("image")
        if not f:
            return jsonify({"error": "no file"}), 400
        ext = Path(f.filename).suffix.lower() if f.filename else ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}:
            ext = ".jpg"
        today  = datetime.date.today()
        subdir = uploads_dir / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
        subdir.mkdir(parents=True, exist_ok=True)
        name = uuid.uuid4().hex + ext
        f.save(subdir / name)
        rel = f"{today.year}/{today.month:02d}/{today.day:02d}/{name}"
        return jsonify({"data": {"filePath": f"/uploads/{rel}"}})

    return bp
