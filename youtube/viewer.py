"""
YouTube Transcript Viewer — Flask web app
Visualizes per-chunk video summaries stored in video_summaries.db.
Clicking a timestamp opens YouTube at that exact moment.

Usage:
    python viewer.py           # http://localhost:8081
    python viewer.py --port 8082
"""

import sys
import sqlite3
import argparse
from pathlib import Path
from jinja2 import DictLoader, Environment
from flask import Flask, request, jsonify

SCRIPT_DIR = Path(__file__).parent
DB_PATH    = SCRIPT_DIR / "video_summaries.db"

app = Flask(__name__)

# ── Database helpers ──────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_videos() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT video_id,
                   COUNT(*)          AS chunk_count,
                   SUM(CASE WHEN summary IS NOT NULL AND summary != '' THEN 1 ELSE 0 END)
                                     AS summarized_count,
                   MAX(analyzed_at)  AS last_analyzed
            FROM video_chunks
            GROUP BY video_id
            ORDER BY last_analyzed DESC
        """).fetchall()
    return [dict(r) for r in rows]


def get_chunks(video_id: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT id, video_id, chunk_index, start_seconds, end_seconds,
                   start_label, end_label, transcript, summary, analyzed_at
            FROM video_chunks
            WHERE video_id = ?
            ORDER BY chunk_index ASC
        """, (video_id,)).fetchall()
    return [dict(r) for r in rows]


# ── Routes ────────────────────────────────────────────────────────────────────

HTML_BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<style>
  body        { background: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
  .navbar     { background: #161b22 !important; border-bottom: 1px solid #30363d; }
  .navbar-brand { color: #58a6ff !important; font-weight: 700; font-size: 1.3rem; }
  .card       { background: #161b22; border: 1px solid #30363d; border-radius: 10px; }
  .card:hover { border-color: #58a6ff; transition: border-color .2s; }
  .badge-chunk { background: #1f6feb; font-size: .75rem; }
  .ts-link    { color: #58a6ff; text-decoration: none; font-weight: 600; font-size: .85rem; }
  .ts-link:hover { color: #79c0ff; text-decoration: underline; }
  .summary    { color: #e6edf3; line-height: 1.65; }
  .transcript-box {
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 12px; font-size: .78rem; color: #8b949e;
    max-height: 220px; overflow-y: auto; white-space: pre-wrap;
    font-family: 'Courier New', monospace;
  }
  .video-card { background: #161b22; border: 1px solid #30363d;
                border-radius: 10px; padding: 20px; margin-bottom: 16px;
                transition: border-color .2s; }
  .video-card:hover { border-color: #58a6ff; }
  .video-title { font-size: 1.1rem; font-weight: 600; color: #58a6ff; }
  .stats-badge { font-size: .8rem; color: #8b949e; }
  .no-summary { color: #6e7681; font-style: italic; font-size: .9rem; }
  .search-box { background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; }
  .search-box:focus { border-color: #58a6ff; box-shadow: 0 0 0 3px rgba(88,166,255,.2); background: #0d1117; color: #c9d1d9; }
  .progress   { background: #21262d; }
  .chunk-num  { color: #8b949e; font-size: .82rem; }
  a.yt-btn    { background: #c4302b; border-color: #c4302b; }
  a.yt-btn:hover { background: #a82420; border-color: #a82420; }
  .collapse-toggle { cursor: pointer; color: #8b949e; font-size: .8rem; }
  .collapse-toggle:hover { color: #c9d1d9; }
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg">
  <div class="container-fluid px-4">
    <a class="navbar-brand" href="/">▶ Video Summaries</a>
  </div>
</nav>
<div class="container-fluid px-4 py-4">
  {% block content %}{% endblock %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
{% block scripts %}{% endblock %}
</body>
</html>
"""

INDEX_CONTENT = """
{% extends "base.html" %}
{% block content %}
<div class="row mb-4 align-items-center">
  <div class="col">
    <h4 class="mb-0" style="color:#e6edf3;">Analyzed Videos</h4>
    <small class="text-muted">{{ videos|length }} video(s) in database</small>
  </div>
</div>

{% if not videos %}
<div class="alert" style="background:#21262d; border:1px solid #30363d; color:#8b949e;">
  No videos analyzed yet. Run:
  <code style="color:#58a6ff;">python analysis_video.py &lt;video_id&gt;</code>
</div>
{% else %}
<div class="row g-3">
  {% for v in videos %}
  <div class="col-12 col-md-6 col-xl-4">
    <a href="/video/{{ v.video_id }}" class="text-decoration-none">
      <div class="video-card h-100">
        <div class="d-flex align-items-start gap-3">
          <div style="flex-shrink:0; width:48px; height:48px; background:#1f6feb;
                      border-radius:8px; display:flex; align-items:center; justify-content:center;
                      font-size:1.4rem;">▶</div>
          <div class="flex-grow-1 min-w-0">
            <div class="video-title text-truncate">{{ v.video_id }}</div>
            <div class="stats-badge mt-1">
              {{ v.chunk_count }} chunks &nbsp;·&nbsp;
              {{ v.summarized_count }}/{{ v.chunk_count }} summarized
            </div>
            {% if v.summarized_count > 0 %}
            <div class="mt-2">
              <div class="progress" style="height:4px; border-radius:2px;">
                <div class="progress-bar"
                     style="width:{{ (v.summarized_count / v.chunk_count * 100)|int }}%;
                            background:#1f6feb; border-radius:2px;"></div>
              </div>
            </div>
            {% endif %}
            {% if v.last_analyzed %}
            <div class="stats-badge mt-1" style="font-size:.75rem;">
              Last analyzed: {{ v.last_analyzed[:19] }}
            </div>
            {% endif %}
          </div>
        </div>
      </div>
    </a>
  </div>
  {% endfor %}
</div>
{% endif %}
{% endblock %}
"""

VIDEO_CONTENT = """
{% extends "base.html" %}
{% block content %}
<div class="d-flex align-items-center gap-3 mb-4 flex-wrap">
  <a href="/" class="btn btn-sm btn-outline-secondary">← Back</a>
  <div>
    <h5 class="mb-0" style="color:#e6edf3;">{{ video_id }}</h5>
    <small class="text-muted">{{ chunks|length }} chunks &nbsp;·&nbsp;
      {{ summarized }} summarized</small>
  </div>
  <a href="https://www.youtube.com/watch?v={{ video_id }}"
     target="_blank" class="btn btn-sm yt-btn text-white ms-auto">
    ▶ Open on YouTube
  </a>
</div>

<!-- Search -->
<div class="mb-4">
  <input id="searchInput" type="text" class="form-control search-box"
         placeholder="Search summaries or transcript…" autocomplete="off">
</div>

<!-- Chunks -->
<div id="chunkList">
{% for c in chunks %}
<div class="card mb-3 chunk-card"
     data-summary="{{ (c.summary or '')|lower }}"
     data-transcript="{{ c.transcript|lower }}">
  <div class="card-body p-3">
    <div class="d-flex align-items-center justify-content-between mb-2 flex-wrap gap-2">
      <div class="d-flex align-items-center gap-2">
        <span class="badge badge-chunk">Chunk {{ c.chunk_index + 1 }}</span>
        <a class="ts-link"
           href="https://www.youtube.com/watch?v={{ video_id }}&t={{ c.start_seconds }}s"
           target="_blank"
           title="Open at {{ c.start_label }} on YouTube">
          ⏱ {{ c.start_label }} – {{ c.end_label }}
        </a>
      </div>
      <div class="d-flex gap-2">
        <a href="https://www.youtube.com/watch?v={{ video_id }}&t={{ c.start_seconds }}s"
           target="_blank" class="btn btn-sm yt-btn text-white py-0 px-2"
           style="font-size:.75rem;">▶ Play</a>
        <span class="collapse-toggle"
              data-bs-toggle="collapse"
              data-bs-target="#transcript-{{ c.id }}">
          📄 transcript
        </span>
      </div>
    </div>

    {% if c.summary %}
    <p class="summary mb-2">{{ c.summary }}</p>
    {% else %}
    <p class="no-summary mb-2">No summary yet.</p>
    {% endif %}

    <div class="collapse" id="transcript-{{ c.id }}">
      <div class="transcript-box mt-2">{{ c.transcript }}</div>
    </div>
  </div>
</div>
{% endfor %}
</div>

<div id="noResults" class="alert" style="display:none; background:#21262d; border:1px solid #30363d; color:#8b949e;">
  No chunks match your search.
</div>

{% endblock %}
{% block scripts %}
<script>
const searchInput = document.getElementById('searchInput');
const cards       = document.querySelectorAll('.chunk-card');
const noResults   = document.getElementById('noResults');

searchInput.addEventListener('input', function() {
  const q = this.value.toLowerCase().trim();
  let visible = 0;
  cards.forEach(card => {
    const match = !q
      || card.dataset.summary.includes(q)
      || card.dataset.transcript.includes(q);
    card.style.display = match ? '' : 'none';
    if (match) visible++;
  });
  noResults.style.display = visible === 0 && q ? '' : 'none';
});
</script>
{% endblock %}
"""


def _render(template_name: str, **ctx) -> str:
    env = Environment(loader=DictLoader({
        "base.html":  HTML_BASE,
        "index.html": INDEX_CONTENT,
        "video.html": VIDEO_CONTENT,
    }), autoescape=True)
    return env.get_template(template_name).render(**ctx)


@app.route("/")
def index():
    videos = list_videos()
    return _render("index.html", videos=videos, title="Video Summaries")


@app.route("/video/<video_id>")
def video_detail(video_id: str):
    chunks = get_chunks(video_id)
    summarized = sum(1 for c in chunks if c.get("summary"))
    return _render("video.html", video_id=video_id, chunks=chunks,
                   summarized=summarized, title=f"Video {video_id}")


@app.route("/api/videos")
def api_videos():
    return jsonify(list_videos())


@app.route("/api/video/<video_id>")
def api_video(video_id: str):
    return jsonify(get_chunks(video_id))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube transcript web viewer")
    parser.add_argument("--port", type=int, default=8081)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        print("Run analysis_video.py first to generate summaries.")
        sys.exit(1)

    print(f"Starting viewer at http://{args.host}:{args.port}")
    print(f"Database: {DB_PATH}")
    app.run(host=args.host, port=args.port, debug=False)
