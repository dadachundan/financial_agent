"""reports_viewer.py — render Markdown reports from ./reports/ with Mermaid.

Mounted at /reports/ in main.py. Recursively scans the reports/ directory,
parses filename metadata (company, ticker, type, date, language), collapses
EN/ZH pairs into a single row, and renders the selected file as HTML with
marked.js + mermaid.js. Filesystem layout:

    reports/
      company/<Slug>/<file>.md      — company research
      sector/<file>.md              — sector / thematic
      compare/<file>.md             — head-to-head
      earnings/<file>.md            — earnings notes
      other/<file>.md               — anything that didn't classify
      charts/<file>.png             — shared chart assets
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from flask import Blueprint, abort, render_template_string, send_from_directory

import nav_widget2 as _nw

REPORTS_DIR = Path(__file__).parent / "reports"

reports_bp = Blueprint("reports", __name__)


# --- filename parsing --------------------------------------------------------

ASIA_TICKER_RE = re.compile(r"(?<![A-Z0-9])(SSE|SZSE|HKEX|TWSE|BSE|TSE|HOSE|KRX)(\d+)")
US_TICKER_RE   = re.compile(r"(?<![A-Z0-9])(NYSE|NASDAQ|AMEX)_([A-Z]+)(?![A-Z])")
RESEARCH_MARKERS = ("_Research_Document_", "_研究报告_", "_公司研究_")
LANG_SUFFIXES = ("_zh", "_CN")  # before .md


def _all_tickers(name: str) -> list[str]:
    """Return all tickers in 'EXCHANGE:CODE' form, in order of appearance."""
    found: list[tuple[int, str]] = []
    for m in ASIA_TICKER_RE.finditer(name):
        found.append((m.start(), f"{m.group(1)}:{m.group(2)}"))
    for m in US_TICKER_RE.finditer(name):
        found.append((m.start(), f"{m.group(1)}:{m.group(2)}"))
    found.sort()
    return [t for _i, t in found]


def _parse(rel_path: Path) -> dict:
    """Parse a markdown file's path/name into display metadata."""
    name = rel_path.name
    stem = name[:-3] if name.endswith(".md") else name

    # Top-level bucket = first path part (company / sector / compare / earnings / other)
    parts = rel_path.parts
    bucket = parts[0] if len(parts) > 1 else "other"

    # Language detection:
    #   - explicit `_zh` / `_CN` suffix → zh
    #   - Chinese research marker `_研究报告_` or `_公司研究_` → zh
    #   - otherwise (e.g. `_Research_Document_`) → en
    lang = "en"
    for suf in LANG_SUFFIXES:
        if stem.endswith(suf):
            lang = "zh"
            stem = stem[: -len(suf)]
            break
    else:
        if "_研究报告_" in stem or "_公司研究_" in stem:
            lang = "zh"

    # Pair key: same bucket + same slug + same date, regardless of marker/lang.
    # Normalize the research marker so EN ("_Research_Document_") and ZH
    # ("_公司研究_" / "_研究报告_") variants of the same report collapse together.
    norm = stem
    for m in ("_Research_Document_", "_研究报告_", "_公司研究_"):
        if m in norm:
            norm = norm.replace(m, "_RESEARCH_")
            break
    pair_key = f"{bucket}/{norm}"

    # Company display: slug (everything before _Research_Document_ etc.) or stem.
    display = stem
    for m in RESEARCH_MARKERS:
        if m in stem:
            display = stem.split(m)[0]
            break

    tickers = _all_tickers(name)
    ticker = tickers[0] if tickers else ""

    # Date from filename: prefer YYYY-MM-DD, fall back to YYYYMMDD.
    date = ""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", stem)
    if m:
        date = m.group(1)
    else:
        m = re.search(r"(\d{4})(\d{2})(\d{2})", stem)
        if m:
            date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    return {
        "rel": str(rel_path).replace("\\", "/"),
        "bucket": bucket,
        "display": display,
        "ticker": ticker,
        "all_tickers": tickers,
        "date": date,
        "lang": lang,
        "pair_key": pair_key,
    }


def _scan() -> list[dict]:
    """Walk reports/, group EN/ZH pairs, return rows newest-first."""
    REPORTS_DIR.mkdir(exist_ok=True)

    rows: dict[str, dict] = {}
    for p in REPORTS_DIR.rglob("*.md"):
        rel = p.relative_to(REPORTS_DIR)
        # Skip the shared charts dir; .md files in there would be docs about charts, unlikely.
        if rel.parts and rel.parts[0] == "charts":
            continue
        meta = _parse(rel)
        st = p.stat()
        ts = getattr(st, "st_birthtime", st.st_mtime)
        meta["ts"] = ts
        meta["created"] = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

        key = meta["pair_key"]
        existing = rows.get(key)
        if existing is None:
            rows[key] = {
                **meta,
                "langs": {meta["lang"]: meta["rel"]},
                "ts": ts,
            }
        else:
            existing["langs"][meta["lang"]] = meta["rel"]
            # Use newest ctime as the row's sort timestamp.
            if ts > existing["ts"]:
                existing["ts"] = ts
                existing["created"] = meta["created"]

    return sorted(rows.values(), key=lambda r: r["ts"], reverse=True)


# --- templates ---------------------------------------------------------------

_INDEX_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Reports</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <style>
    .page{max-width:1100px;margin:1rem auto;padding:0 1rem;color:#222;
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    .page h1{font-size:1.4rem;margin-bottom:.5rem}
    .toolbar{display:flex;gap:.6rem;align-items:center;margin:.6rem 0 .8rem;flex-wrap:wrap}
    .toolbar input[type=search]{flex:1;min-width:220px;max-width:420px;
         padding:.35rem .6rem;border:1px solid #ccc;border-radius:6px;font-size:.95rem}
    .bucket-tag{font-size:.8rem;padding:.1rem .45rem;border-radius:10px;
         background:#eef2f7;color:#3a4a5e;border:1px solid #d6dde6}
    .bucket-tag.company{background:#eef7ee;border-color:#cfe5cf;color:#2a5d2f}
    .bucket-tag.sector{background:#fef5e6;border-color:#f0d8a6;color:#7a5118}
    .bucket-tag.compare{background:#f3eaf7;border-color:#dac3ea;color:#5a2a85}
    .bucket-tag.earnings{background:#eaf2fb;border-color:#c4d8ef;color:#1d4a85}
    .ticker{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85rem;color:#444}
    .lang-link{display:inline-block;font-size:.78rem;padding:.05rem .4rem;border-radius:4px;
         border:1px solid #cfd6df;color:#0366d6;text-decoration:none;margin-right:.3rem}
    .lang-link:hover{background:#eef4fb;text-decoration:none}
    .lang-link.missing{color:#aaa;border-color:#e0e0e0;cursor:default}
    .page table{width:100%;border-collapse:collapse;margin-top:.5rem}
    .page th,.page td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid #eee;vertical-align:middle}
    .page th{font-size:.85rem;color:#666;font-weight:600;cursor:pointer;user-select:none}
    .page th .sort-ind{color:#aaa;font-size:.7rem;margin-left:.2rem}
    .page td.created,.page td.date{color:#666;white-space:nowrap;font-variant-numeric:tabular-nums;font-size:.9rem}
    .page td a.title{color:#0366d6;text-decoration:none;font-weight:500}
    .page td a.title:hover{text-decoration:underline}
    .empty{color:#888;font-style:italic}
    .count{color:#666;font-size:.85rem;margin-left:.4rem}
  </style>
</head>
<body>
  {{ _nav | safe }}
  <div class="page">
    <h1>Reports <span class="count" id="count">{{ rows|length }} entries</span></h1>
    {% if rows %}
    <div class="toolbar">
      <input id="filter" type="search" placeholder="Filter by company, ticker, or filename…" autofocus>
      <label style="font-size:.85rem;color:#555">
        <input type="checkbox" id="onlyCompany"> Company research only
      </label>
    </div>
    <table id="grid">
      <thead>
        <tr>
          <th data-sort="display">Report</th>
          <th data-sort="ticker">Ticker</th>
          <th data-sort="bucket">Type</th>
          <th data-sort="date">Date</th>
          <th data-sort="ts" class="active">Created <span class="sort-ind">▼</span></th>
          <th>Lang</th>
        </tr>
      </thead>
      <tbody>
        {% for r in rows %}
          <tr data-bucket="{{ r.bucket }}"
              data-display="{{ r.display|lower }}"
              data-ticker="{{ r.ticker|lower }}"
              data-filename="{{ r.rel|lower }}"
              data-date="{{ r.date }}"
              data-ts="{{ r.ts }}">
            <td><a class="title" href="{{ _base }}/view/{{ r.langs.get('en') or r.langs.get('zh') }}">{{ r.display }}</a></td>
            <td class="ticker">{{ r.ticker }}</td>
            <td><span class="bucket-tag {{ r.bucket }}">{{ r.bucket }}</span></td>
            <td class="date">{{ r.date }}</td>
            <td class="created">{{ r.created }}</td>
            <td>
              {% if r.langs.get('en') %}
                <a class="lang-link" href="{{ _base }}/view/{{ r.langs['en'] }}">EN</a>
              {% else %}<span class="lang-link missing">EN</span>{% endif %}
              {% if r.langs.get('zh') %}
                <a class="lang-link" href="{{ _base }}/view/{{ r.langs['zh'] }}">ZH</a>
              {% else %}<span class="lang-link missing">ZH</span>{% endif %}
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
      <p class="empty">No reports yet — run the company-research or sec-report-summary skill.</p>
    {% endif %}
  </div>

  <script>
    (function() {
      const grid = document.getElementById("grid");
      if (!grid) return;
      const tbody = grid.querySelector("tbody");
      const rows  = Array.from(tbody.querySelectorAll("tr"));
      const filter = document.getElementById("filter");
      const onlyCompany = document.getElementById("onlyCompany");
      const count = document.getElementById("count");

      function applyFilter() {
        const q = (filter.value || "").trim().toLowerCase();
        const co = onlyCompany.checked;
        let visible = 0;
        for (const r of rows) {
          const hay = r.dataset.display + " " + r.dataset.ticker + " " + r.dataset.filename;
          const matchQ  = !q || hay.includes(q);
          const matchCo = !co || r.dataset.bucket === "company";
          const show = matchQ && matchCo;
          r.style.display = show ? "" : "none";
          if (show) visible++;
        }
        count.textContent = visible + " entries";
      }
      filter.addEventListener("input", applyFilter);
      onlyCompany.addEventListener("change", applyFilter);

      // Click-to-sort on headers (toggle asc/desc).
      let sortKey = "ts", sortDir = -1;  // newest first by default
      grid.querySelectorAll("th[data-sort]").forEach(th => {
        th.addEventListener("click", () => {
          const k = th.dataset.sort;
          if (k === sortKey) sortDir = -sortDir;
          else { sortKey = k; sortDir = (k === "ts" || k === "date") ? -1 : 1; }
          rows.sort((a, b) => {
            const av = a.dataset[sortKey] || "";
            const bv = b.dataset[sortKey] || "";
            // Numeric sort for ts.
            if (sortKey === "ts") return (Number(av) - Number(bv)) * sortDir;
            return av.localeCompare(bv) * sortDir;
          });
          for (const r of rows) tbody.appendChild(r);
          // Update indicator.
          grid.querySelectorAll("th[data-sort]").forEach(h => {
            h.classList.remove("active");
            const ind = h.querySelector(".sort-ind");
            if (ind) ind.remove();
          });
          th.classList.add("active");
          const ind = document.createElement("span");
          ind.className = "sort-ind";
          ind.textContent = sortDir > 0 ? "▲" : "▼";
          th.appendChild(ind);
        });
      });
    })();
  </script>
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
    .markdown-body mark{background:#fff3a3;color:inherit;padding:.05em .15em;border-radius:2px}
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

    // Obsidian-style ==highlight== → <mark>highlight</mark>
    marked.use({
      extensions: [{
        name: "obsidianHighlight",
        level: "inline",
        start(src) { const i = src.indexOf("=="); return i < 0 ? undefined : i; },
        tokenizer(src) {
          const m = /^==(?=\S)([\s\S]*?\S)==/.exec(src);
          if (m) return { type: "obsidianHighlight", raw: m[0], tokens: this.lexer.inlineTokens(m[1]) };
        },
        renderer(token) { return `<mark>${this.parser.parseInline(token.tokens)}</mark>`; },
      }],
    });

    const raw = {{ md | tojson }};
    const root = document.getElementById("content");
    root.innerHTML = marked.parse(raw);

    // marked emits ```mermaid``` as <pre><code class="language-mermaid">.
    // Convert each into <pre class="mermaid">code</pre> so mermaid.run picks it up.
    root.querySelectorAll("pre code.language-mermaid").forEach(code => {
      const text = code.textContent;
      const wrap = document.createElement("pre");
      wrap.className = "mermaid";
      wrap.textContent = text;
      code.parentElement.replaceWith(wrap);
    });

    // Rewrite relative chart image refs so docs in any subdir resolve correctly.
    // <img src="charts/foo.png"> → <img src="/reports/view/charts/foo.png">.
    const baseChart = "{{ _base }}/view/charts/";
    root.querySelectorAll("img").forEach(img => {
      const src = img.getAttribute("src") || "";
      // Match anything that contains "charts/" but isn't already absolute.
      if (!src.startsWith("/") && !src.startsWith("http")) {
        const idx = src.indexOf("charts/");
        if (idx >= 0) {
          img.setAttribute("src", baseChart + src.slice(idx + "charts/".length));
        }
      }
    });

    await mermaid.run({ querySelector: ".mermaid" });
  </script>
</body>
</html>
"""


# --- routes ------------------------------------------------------------------

@reports_bp.route("/")
def index():
    rows = _scan()
    return render_template_string(_INDEX_TMPL, rows=rows, _nav=_nw.NAV_HTML)


@reports_bp.route("/view/<path:rel>")
def view(rel: str):
    # Resolve safely under REPORTS_DIR.
    if ".." in rel.split("/") or not rel.endswith(".md"):
        abort(404)
    target = (REPORTS_DIR / rel).resolve()
    try:
        target.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        abort(404)
    if not target.is_file():
        abort(404)
    md = target.read_text(encoding="utf-8")
    return render_template_string(_VIEW_TMPL, name=target.name, md=md, _nav=_nw.NAV_HTML)


@reports_bp.route("/view/charts/<path:filename>", endpoint="view_chart_asset")
def view_chart_asset(filename: str):
    """Serve chart PNGs from reports/charts/, regardless of doc depth.

    Existing reports reference charts as relative `charts/foo.png`; the
    template rewrites those to `/reports/view/charts/foo.png` before
    handing them to the browser, so this single route catches them all.
    """
    charts_dir = REPORTS_DIR / "charts"
    return send_from_directory(charts_dir, filename)
