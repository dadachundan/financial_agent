"""reports_viewer.py — render Markdown reports from ./reports/ with Mermaid.

Mounted at /reports/ in main.py. Lists every .md file in the reports/
directory and renders the selected one as HTML with marked.js +
mermaid.js loaded from CDN. The reports/ directory is gitignored so
each file is local-only.
"""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, abort, render_template_string

REPORTS_DIR = Path(__file__).parent / "reports"

reports_bp = Blueprint("reports", __name__)


_INDEX_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Reports</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
         max-width:760px;margin:2rem auto;padding:0 1rem;color:#222}
    h1{font-size:1.4rem;margin-bottom:.5rem}
    ul{padding-left:1.2rem}
    li{margin:.3rem 0}
    a{color:#0366d6;text-decoration:none}
    a:hover{text-decoration:underline}
    .empty{color:#888;font-style:italic}
  </style>
</head>
<body>
  <h1>Reports</h1>
  {% if files %}
    <ul>
      {% for f in files %}
        <li><a href="{{ _base }}/view/{{ f }}">{{ f }}</a></li>
      {% endfor %}
    </ul>
  {% else %}
    <p class="empty">No reports yet — run the sec-report-summary skill.</p>
  {% endif %}
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
        href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-light.min.css">
  <style>
    body{box-sizing:border-box;min-width:200px;max-width:980px;
         margin:0 auto;padding:32px;background:#fff}
    .markdown-body pre{background:#f6f8fa}
    .mermaid{background:#fff;border:1px solid #eee;border-radius:6px;
             padding:12px;margin:16px 0}
    .nav{margin-bottom:14px;font-family:-apple-system,sans-serif;font-size:.9rem}
    .nav a{color:#0366d6;text-decoration:none}
  </style>
</head>
<body class="markdown-body">
  <div class="nav"><a href="{{ _base }}/">&larr; back to reports</a></div>
  <div id="content"></div>

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
    files = sorted((p.name for p in REPORTS_DIR.glob("*.md")), reverse=True)
    return render_template_string(_INDEX_TMPL, files=files)


@reports_bp.route("/view/<path:name>")
def view(name: str):
    # Reject path traversal
    if "/" in name or ".." in name or not name.endswith(".md"):
        abort(404)
    target = REPORTS_DIR / name
    if not target.exists() or not target.is_file():
        abort(404)
    md = target.read_text(encoding="utf-8")
    return render_template_string(_VIEW_TMPL, name=name, md=md)
