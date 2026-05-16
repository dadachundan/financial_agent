"""reports_viewer.py — render Markdown reports from ./reports/ with Mermaid.

Mounted at /reports/ in main.py. Lists every .md file in the reports/
directory and renders the selected one as HTML with marked.js +
mermaid.js loaded from CDN. The reports/ directory is gitignored so
each file is local-only.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import Blueprint, abort, render_template_string

import nav_widget2 as _nw

REPORTS_DIR = Path(__file__).parent / "reports"

reports_bp = Blueprint("reports", __name__)


_INDEX_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Reports</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <style>
    .page{max-width:760px;margin:1rem auto;padding:0 1rem;color:#222;
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    .page h1{font-size:1.4rem;margin-bottom:.5rem}
    .page ul{padding-left:1.2rem}
    .page li{margin:.3rem 0}
    .page a{color:#0366d6;text-decoration:none}
    .page a:hover{text-decoration:underline}
    .empty{color:#888;font-style:italic}
    .page table{width:100%;border-collapse:collapse;margin-top:.5rem}
    .page th,.page td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid #eee}
    .page th{font-size:.85rem;color:#666;font-weight:600}
    .page td.created{color:#666;white-space:nowrap;font-variant-numeric:tabular-nums}
  </style>
</head>
<body>
  {{ _nav | safe }}
  <div class="page">
  <h1>Reports</h1>
  {% if files %}
    <table>
      <thead>
        <tr><th>Report</th><th>Created</th></tr>
      </thead>
      <tbody>
        {% for f in files %}
          <tr>
            <td><a href="{{ _base }}/view/{{ f.name }}">{{ f.name }}</a></td>
            <td class="created">{{ f.created }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p class="empty">No reports yet — run the sec-report-summary skill.</p>
  {% endif %}
  </div>
</body>
</html>
"""


_VIEW_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ name }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-light.min.css">
  <style>
    body{background:#fff}
    .doc{box-sizing:border-box;min-width:200px;max-width:980px;
         margin:0 auto;padding:24px 32px}
    .markdown-body pre{background:#f6f8fa}
    .markdown-body table{display:block;overflow-x:auto}
    .mermaid{background:#fff;border:1px solid #eee;border-radius:6px;
             padding:12px;margin:16px 0}
    .backlink{margin:8px 0 14px;font-family:-apple-system,sans-serif;font-size:.9rem}
    .backlink a{color:#0366d6;text-decoration:none}
  </style>
</head>
<body>
  {{ _nav | safe }}
  <div class="doc markdown-body">
    <div class="backlink"><a href="{{ _base }}/">&larr; back to reports</a></div>
    <div id="content"></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    mermaid.initialize({ startOnLoad:false, theme:"default" });

    const raw = {{ md | tojson }};
    document.getElementById("content").innerHTML = marked.parse(raw);

    // marked emits ```mermaid``` as <pre><code class="language-mermaid">.
    // Convert each into <pre class="mermaid">code</pre> so mermaid.run picks it up.
    document.querySelectorAll("#content pre code.language-mermaid").forEach(code => {
      const pre = code.parentElement;
      const text = code.textContent;
      const wrap = document.createElement("pre");
      wrap.className = "mermaid";
      wrap.textContent = text;
      pre.replaceWith(wrap);
    });
    await mermaid.run({ querySelector: ".mermaid" });
  </script>
</body>
</html>
"""


@reports_bp.route("/")
def index():
    REPORTS_DIR.mkdir(exist_ok=True)
    entries = []
    for p in REPORTS_DIR.glob("*.md"):
        st = p.stat()
        # st_birthtime is creation time on macOS; fall back to mtime elsewhere.
        ts = getattr(st, "st_birthtime", st.st_mtime)
        entries.append({
            "name": p.name,
            "ts": ts,
            "created": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M"),
        })
    entries.sort(key=lambda e: e["ts"], reverse=True)
    return render_template_string(_INDEX_TMPL, files=entries, _nav=_nw.NAV_HTML)


@reports_bp.route("/view/<path:name>")
def view(name: str):
    # Reject path traversal
    if "/" in name or ".." in name or not name.endswith(".md"):
        abort(404)
    target = REPORTS_DIR / name
    if not target.exists() or not target.is_file():
        abort(404)
    md = target.read_text(encoding="utf-8")
    return render_template_string(_VIEW_TMPL, name=name, md=md, _nav=_nw.NAV_HTML)
