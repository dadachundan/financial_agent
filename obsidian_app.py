"""obsidian_app.py — Obsidian vault viewer blueprint.

Reads markdown files from ~/Downloads/Thoughts, renders them with image support.
Images referenced as ![[filename]] or ![[imgs/filename]] (Obsidian wikilink format)
are resolved relative to the .md file's directory (then imgs/ subfolder, then vault-wide).
"""

import os
import re
import urllib.parse
from pathlib import Path
from flask import Blueprint, send_file, jsonify, request, render_template_string
import nav_widget2 as nw2

VAULT_DIR = Path.home() / "Downloads" / "Thoughts"

obsidian_bp = Blueprint("obsidian", __name__)


def _all_notes():
    """Return list of dicts for all .md files, sorted by mtime descending."""
    notes = []
    for p in VAULT_DIR.rglob("*.md"):
        try:
            stat = p.stat()
            rel = p.relative_to(VAULT_DIR)
            folder = str(rel.parent) if str(rel.parent) != "." else ""
            notes.append({
                "path": str(rel),
                "name": p.stem,
                "folder": folder,
                "mtime": stat.st_mtime,
            })
        except Exception:
            continue
    notes.sort(key=lambda x: x["mtime"], reverse=True)
    return notes


def _resolve_image(img_ref: str, md_path: Path) -> Path | None:
    """Find an image file given its Obsidian reference and the note's path."""
    md_dir = md_path.parent

    # Try the reference as-is relative to md dir
    candidates = [
        md_dir / img_ref,
        md_dir / "imgs" / img_ref,
        md_dir / Path(img_ref).name,           # strip any leading path component
        md_dir / "imgs" / Path(img_ref).name,
    ]
    for c in candidates:
        if c.exists():
            return c

    # Vault-wide search by filename
    target_name = Path(img_ref).name
    for p in VAULT_DIR.rglob(target_name):
        if p.is_file():
            return p

    return None


def _preprocess_markdown(text: str, note_rel_path: str) -> str:
    """Convert Obsidian wikilink images ![[...]] to standard markdown images."""
    md_abs = VAULT_DIR / note_rel_path

    def replace_wikilink(m):
        inner = m.group(1).strip()
        # Handle optional display name: ![[file|alias]]
        ref = inner.split("|")[0].strip()
        resolved = _resolve_image(ref, md_abs)
        if resolved:
            encoded = urllib.parse.quote(str(resolved.relative_to(VAULT_DIR)), safe="/")
            return f'<img src="/obsidian/img/{encoded}" alt="{Path(ref).name}" style="max-width:100%">'
        return f'<span class="text-muted">[image not found: {ref}]</span>'

    # Obsidian embed: ![[...]]
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_wikilink, text)
    return text


# ── Routes ────────────────────────────────────────────────────────────────────

@obsidian_bp.route("/")
def index():
    notes = _all_notes()
    # Build folder list preserving first-seen order, sorted by their newest note mtime
    folder_mtime: dict[str, float] = {}
    for n in notes:
        f = n["folder"] or "(root)"
        if f not in folder_mtime:
            folder_mtime[f] = n["mtime"]
    folders = sorted(folder_mtime.keys(), key=lambda f: folder_mtime[f], reverse=True)

    return render_template_string(
        _TEMPLATE,
        nav=nw2.NAV_HTML,
        notes=notes,
        folders=folders,
    )


@obsidian_bp.route("/note")
def note():
    """Return rendered HTML for a single note (AJAX)."""
    path = request.args.get("path", "")
    if not path:
        return jsonify({"error": "missing path"}), 400
    abs_path = VAULT_DIR / path
    # Security: ensure path stays inside vault
    try:
        abs_path.resolve().relative_to(VAULT_DIR.resolve())
    except ValueError:
        return jsonify({"error": "invalid path"}), 403
    if not abs_path.exists():
        return jsonify({"error": "not found"}), 404
    try:
        text = abs_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    processed = _preprocess_markdown(text, path)
    return jsonify({"markdown": processed})


@obsidian_bp.route("/img/<path:img_path>")
def serve_image(img_path):
    """Serve an image file from inside the vault."""
    abs_path = VAULT_DIR / img_path
    try:
        abs_path.resolve().relative_to(VAULT_DIR.resolve())
    except ValueError:
        return "forbidden", 403
    if not abs_path.exists():
        return "not found", 404
    return send_file(abs_path)


# ── Template ──────────────────────────────────────────────────────────────────

_TEMPLATE = """\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Obsidian – FinAgent</title>
<link rel="stylesheet" href="/static/bootstrap.min.css">
<link rel="stylesheet" href="/static/vendor/easymde.min.css">
<style>
  body { background:#1a1a2e; color:#e0e0e0; font-family:'Segoe UI',sans-serif; }
  /* sidebar */
  #sidebar {
    width:280px; min-width:220px; max-width:340px;
    background:#0f0f1a; border-right:1px solid #2a2a4a;
    display:flex; flex-direction:column; height:calc(100vh - 44px);
    overflow:hidden;
  }
  #sidebar-search {
    padding:8px; border-bottom:1px solid #2a2a4a;
  }
  #sidebar-search input {
    width:100%; background:#1a1a2e; border:1px solid #3a3a5a;
    color:#e0e0e0; border-radius:4px; padding:4px 8px; font-size:.8rem;
  }
  #folder-list { overflow-y:auto; flex:1; }
  .folder-header {
    padding:6px 10px 4px; font-size:.7rem; font-weight:700;
    color:#888; letter-spacing:.08em; text-transform:uppercase;
    cursor:pointer; user-select:none;
  }
  .folder-header:hover { color:#aaa; }
  .note-item {
    padding:5px 14px; font-size:.8rem; cursor:pointer;
    border-left:3px solid transparent; line-height:1.3;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }
  .note-item:hover { background:#1e1e38; border-color:#6060c0; }
  .note-item.active { background:#1e1e38; border-color:#9090ff; color:#c0c0ff; }
  .note-mtime { font-size:.67rem; color:#666; }
  /* viewer */
  #viewer {
    flex:1; overflow-y:auto; padding:20px 30px;
    background:#12121e;
  }
  #note-title {
    font-size:1.4rem; font-weight:700; color:#c0c0ff;
    margin-bottom:4px;
  }
  #note-meta { font-size:.75rem; color:#666; margin-bottom:16px; }
  #note-body {
    max-width:860px; line-height:1.8; font-size:.92rem; color:#d0d0e8;
  }
  #note-body h1,#note-body h2,#note-body h3 { color:#a0a0ff; margin-top:1.4em; }
  #note-body h1 { font-size:1.5rem; }
  #note-body h2 { font-size:1.25rem; }
  #note-body h3 { font-size:1.05rem; }
  #note-body a { color:#7090ff; }
  #note-body blockquote {
    border-left:3px solid #4040a0; padding-left:12px;
    color:#aaa; margin:8px 0;
  }
  #note-body pre {
    background:#0a0a18; border:1px solid #2a2a4a;
    border-radius:4px; padding:12px; overflow-x:auto;
    font-size:.82rem;
  }
  #note-body code {
    background:#0a0a18; border-radius:3px; padding:1px 5px; font-size:.85em;
  }
  #note-body pre code { background:none; padding:0; }
  #note-body table {
    border-collapse:collapse; width:100%; margin:12px 0;
  }
  #note-body th,#note-body td {
    border:1px solid #2a2a4a; padding:6px 10px; font-size:.83rem;
  }
  #note-body th { background:#1a1a3a; }
  #note-body img { max-width:100%; border-radius:4px; margin:8px 0; }
  #note-body hr { border-color:#2a2a4a; }
  #note-body mark { background:#b8860b; color:#fff; padding:0 3px; border-radius:3px; }
  #placeholder {
    color:#444; font-size:1.1rem; margin-top:80px; text-align:center;
  }
  .spinner-border { width:1.5rem;height:1.5rem; }
  /* folder toggle */
  .folder-notes { display:block; }
  .folder-notes.collapsed { display:none; }
  .folder-arrow { display:inline-block; transition:transform .15s; margin-right:4px; }
  .folder-arrow.open { transform:rotate(90deg); }
  /* outline panel */
  #outline {
    width:200px; min-width:160px;
    background:#0f0f1a; border-left:1px solid #2a2a4a;
    overflow-y:auto; padding:10px 0;
    height:calc(100vh - 44px);
    flex-shrink:0;
  }
  #outline-title {
    font-size:.68rem; font-weight:700; color:#666;
    letter-spacing:.08em; text-transform:uppercase;
    padding:0 12px 6px;
  }
  .outline-item {
    display:block; font-size:.75rem; color:#888;
    padding:3px 12px; cursor:pointer; line-height:1.35;
    text-decoration:none; white-space:nowrap;
    overflow:hidden; text-overflow:ellipsis;
    border-left:2px solid transparent;
  }
  .outline-item:hover { color:#c0c0ff; background:#1a1a3a; }
  .outline-item.h1 { color:#a0a0cc; font-weight:600; padding-left:12px; }
  .outline-item.h2 { padding-left:20px; }
  .outline-item.h3 { padding-left:28px; font-size:.72rem; }
  .outline-item.active { border-color:#6060c0; color:#c0c0ff; }
</style>
</head>
<body>
{{ nav|safe }}

<div style="display:flex; height:calc(100vh - 44px);">

  <!-- Sidebar -->
  <div id="sidebar">
    <div id="sidebar-search">
      <input id="searchInput" placeholder="Search notes…" oninput="filterNotes(this.value)">
    </div>
    <div id="folder-list">
      {% for folder in folders %}
      <div class="folder-section" data-folder="{{ folder }}">
        <div class="folder-header" onclick="toggleFolder(this)">
          <span class="folder-arrow open">▶</span>{{ folder }}
        </div>
        <div class="folder-notes">
          {% for note in notes if note.folder == (folder if folder != '(root)' else '') %}
          <div class="note-item"
               data-path="{{ note.path }}"
               data-name="{{ note.name }}"
               title="{{ note.name }}"
               onclick="openNote('{{ note.path }}', this)">
            <div>{{ note.name }}</div>
            <div class="note-mtime">{{ note.mtime|int|format_mtime }}</div>
          </div>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- Viewer -->
  <div id="viewer">
    <div id="placeholder">Select a note from the sidebar</div>
    <div id="note-content" style="display:none">
      <div id="note-title"></div>
      <div id="note-meta"></div>
      <div id="note-body"></div>
    </div>
  </div>

  <!-- Outline -->
  <div id="outline">
    <div id="outline-title">Outline</div>
    <div id="outline-list"></div>
  </div>

</div>

<script src="/static/vendor/marked.min.js"></script>
<script>
// Configure marked
marked.setOptions({
  breaks: true,
  gfm: true,
  headerIds: false,
  mangle: false,
});

// Pre-process Obsidian-specific syntax before passing to marked
function obsidianPreprocess(text) {
  // ==highlight== → <mark>highlight</mark>  (skip inside backtick code spans)
  return text.replace(/`[^`\\n]*`|==([^=\\n]+)==/g, (m, inner) => {
    if (m.startsWith('`')) return m;          // leave code spans untouched
    return '<mark>' + inner + '</mark>';
  });
}

function buildOutline() {
  const headings = document.querySelectorAll('#note-body h1, #note-body h2, #note-body h3');
  const list = document.getElementById('outline-list');
  list.innerHTML = '';
  if (!headings.length) return;

  let idx = 0;
  headings.forEach(h => {
    h.dataset.outlineIdx = idx;
    const a = document.createElement('a');
    a.className = 'outline-item ' + h.tagName.toLowerCase();
    a.textContent = h.textContent;
    a.href = '#';
    a.dataset.idx = idx;
    a.onclick = e => {
      e.preventDefault();
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    list.appendChild(a);
    idx++;
  });

  // Highlight active heading on scroll
  const viewer = document.getElementById('viewer');
  viewer.onscroll = () => {
    const scrollTop = viewer.scrollTop + 60;
    let active = 0;
    headings.forEach((h, i) => { if (h.offsetTop <= scrollTop) active = i; });
    document.querySelectorAll('.outline-item').forEach((a, i) => {
      a.classList.toggle('active', i === active);
    });
  };
}

function openNote(path, el) {
  document.querySelectorAll('.note-item').forEach(x => x.classList.remove('active'));
  if (el) el.classList.add('active');

  document.getElementById('placeholder').style.display = 'none';
  const content = document.getElementById('note-content');
  content.style.display = 'block';
  const name = path.split('/').pop().replace(/\\.md$/, '');
  document.getElementById('note-title').textContent = name;
  document.getElementById('note-meta').textContent = 'Loading…';
  document.getElementById('note-body').innerHTML = '<div class="d-flex justify-content-center mt-4"><div class="spinner-border text-secondary"></div></div>';
  document.getElementById('outline-list').innerHTML = '';

  fetch('/obsidian/note?path=' + encodeURIComponent(path))
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        document.getElementById('note-body').innerHTML = '<p class="text-danger">' + data.error + '</p>';
        return;
      }
      // Split on server-rendered <img> / <span> tags so they bypass marked
      const parts = data.markdown.split(/(<img [^>]+>|<span class="text-muted">[^<]*<\/span>)/);
      let html = '';
      for (let i = 0; i < parts.length; i++) {
        if (parts[i].startsWith('<img ') || parts[i].startsWith('<span class="text-muted">')) {
          html += parts[i];
        } else {
          html += marked.parse(obsidianPreprocess(parts[i]));
        }
      }
      document.getElementById('note-body').innerHTML = html;
      const folder = path.includes('/') ? path.split('/').slice(0, -1).join(' / ') : '';
      document.getElementById('note-meta').textContent = folder || 'Root';
      buildOutline();
    })
    .catch(err => {
      document.getElementById('note-body').innerHTML = '<p class="text-danger">Failed to load: ' + err + '</p>';
    });
}

function toggleFolder(header) {
  const arrow = header.querySelector('.folder-arrow');
  const notes = header.nextElementSibling;
  notes.classList.toggle('collapsed');
  arrow.classList.toggle('open');
}

function filterNotes(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('.note-item').forEach(el => {
    const name = el.dataset.name.toLowerCase();
    const path = el.dataset.path.toLowerCase();
    el.style.display = (!q || name.includes(q) || path.includes(q)) ? '' : 'none';
  });
  // Show/hide folder headers based on visible children
  document.querySelectorAll('.folder-section').forEach(sec => {
    const visible = [...sec.querySelectorAll('.note-item')].some(el => el.style.display !== 'none');
    sec.style.display = visible ? '' : 'none';
    if (q) {
      sec.querySelector('.folder-notes').classList.remove('collapsed');
      sec.querySelector('.folder-arrow').classList.add('open');
    }
  });
}

// Open first note on load
const first = document.querySelector('.note-item');
if (first) openNote(first.dataset.path, first);
</script>
</body>
</html>
"""


# Jinja2 filter for mtime → human-readable date
from datetime import datetime

def _format_mtime(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def register_filters(app):
    app.jinja_env.filters["format_mtime"] = _format_mtime
