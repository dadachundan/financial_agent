"""reports_viewer.py — render Markdown reports from ./reports/ with Mermaid.

Mounted at /reports/ in main.py. Recursively scans the reports/ directory,
parses filename metadata (company, ticker, type, date, language), collapses
EN/ZH pairs into a single row, and renders the selected file as HTML with
marked.js + mermaid.js. Filesystem layout:

    reports/
      company/<Slug>/<file>.md      — listed (public) company research
      unlisted/<Slug>/<file>.md     — private / unlisted company research
      sector/<file>.md              — sector / thematic
      compare/<file>.md             — head-to-head
      earnings/<file>.md            — earnings notes
      other/<file>.md               — anything that didn't classify
"""
from __future__ import annotations

import base64
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

from flask import Blueprint, abort, jsonify, render_template_string, request, send_from_directory

import md_comment_widget as _mcw
import nav_widget2 as _nw
import report_annotations as _ra
import report_inline_comments as _ric
from sector_map import ALL_SECTORS, sector_for
from market_cap_cache import (
    format_market_cap, get_fx_rates, get_market_caps, pending_count, to_usd,
)

try:
    import mammoth
except ImportError:
    mammoth = None

REPORTS_DIR = Path(__file__).parent / "reports"

reports_bp = Blueprint("reports", __name__)


# --- filename parsing --------------------------------------------------------

ASIA_TICKER_RE = re.compile(r"(?<![A-Z0-9])(SSE|SZSE|HKEX|TWSE|BSE|TSE|HOSE|KRX)(\d+)")
US_TICKER_RE   = re.compile(r"(?<![A-Z0-9])(NYSE|NASDAQ|AMEX)_([A-Z]+)(?![A-Z])")
RESEARCH_MARKERS = ("_Research_Document", "_研究报告", "_公司研究")
VALUATION_MARKERS = ("_Valuation_Analysis", "_Initiation_Report")
ALL_KIND_MARKERS = RESEARCH_MARKERS + VALUATION_MARKERS
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

    # Pair key: same bucket + same slug + same kind, regardless of marker/lang.
    # Normalize the research marker so EN ("_Research_Document") and ZH
    # ("_公司研究" / "_研究报告") variants of the same report collapse together.
    norm = stem
    for m in RESEARCH_MARKERS:
        if m in norm:
            norm = norm.replace(m, "_RESEARCH")
            break
    pair_key = f"{bucket}/{norm}"

    # Company display: strip the kind suffix (Research_Document /
    # Valuation_Analysis / etc.) so the UI shows just the company slug.
    display = stem
    for m in ALL_KIND_MARKERS:
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
    """Walk reports/, group EN/ZH/DOCX siblings, return rows newest-first."""
    REPORTS_DIR.mkdir(exist_ok=True)

    rows: dict[str, dict] = {}
    # Markdown files first
    for p in REPORTS_DIR.rglob("*.md"):
        rel = p.relative_to(REPORTS_DIR)
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
            if ts > existing["ts"]:
                existing["ts"] = ts
                existing["created"] = meta["created"]

    # DOCX files — attach to matching slug if present, else create own row
    for p in REPORTS_DIR.rglob("*.docx"):
        rel = p.relative_to(REPORTS_DIR)
        if rel.parts and rel.parts[0] == "charts":
            continue
        meta = _parse_docx(rel)
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
            if ts > existing["ts"]:
                existing["ts"] = ts
                existing["created"] = meta["created"]

    return sorted(rows.values(), key=lambda r: r["ts"], reverse=True)


def _parse_docx(rel_path: Path) -> dict:
    """Parse a .docx filename like Cadence_NASDAQ_CDNS_Initiation_Report_2026-05-20.docx."""
    name = rel_path.name
    stem = name[:-5] if name.endswith(".docx") else name

    parts = rel_path.parts
    bucket = parts[0] if len(parts) > 1 else "other"

    # Strip ZH suffix first so the EN/ZH DOCX siblings collapse into one row
    # (mirrors what _parse() does for .md files).
    lang = "docx"
    for suf in LANG_SUFFIXES:
        if stem.endswith(suf):
            lang = "docx_zh"
            stem = stem[: -len(suf)]
            break

    # Reuse the same pair_key normalization so DOCX collapses next to its sibling MD.
    norm = stem
    for m in ("_Initiation_Report_", "_Research_Document_", "_Valuation_Analysis_",
              "_研究报告_", "_公司研究_"):
        if m in norm:
            norm = norm.replace(m, "_RESEARCH_")
            break
    pair_key = f"{bucket}/{norm}"

    display = stem
    for m in ("_Initiation_Report_", "_Research_Document_", "_Valuation_Analysis_"):
        if m in stem:
            display = stem.split(m)[0]
            break

    tickers = _all_tickers(name)
    ticker = tickers[0] if tickers else ""

    date = ""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", stem)
    if m:
        date = m.group(1)

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


# --- templates ---------------------------------------------------------------

_INDEX_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Claude Reports</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
__MCW_HEAD__
  <style>
__MCW_CSS__
    .star-rating .star{cursor:pointer;font-size:1.05rem;line-height:1;user-select:none}
    .star-rating .star:hover{filter:brightness(.9)}
    .page td.rating-cell{white-space:nowrap;min-width:84px}
    .page td.comment-cell{max-width:220px;font-size:.86rem;color:#444}
    .page td.comment-cell .comment-preview{color:#444}
    .page td.comment-cell .comment-preview p{margin:0}
    body{background:#f6f7fa}
    .page{max-width:1280px;margin:1rem auto;padding:0 1.2rem 2rem;color:#222;
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    .page h1{font-size:1.45rem;margin:.4rem 0 .15rem;font-weight:600}
    .subtitle{color:#777;font-size:.85rem;margin-bottom:.7rem}
    .toolbar{display:flex;gap:.55rem;align-items:center;margin:.6rem 0 .9rem;flex-wrap:wrap;
         background:#fff;border:1px solid #e3e6eb;border-radius:8px;padding:.55rem .7rem;
         box-shadow:0 1px 2px rgba(0,0,0,.03)}
    .toolbar input[type=search],.toolbar select{
         padding:.4rem .6rem;border:1px solid #d0d4da;border-radius:6px;font-size:.92rem;background:#fff}
    .toolbar input[type=search]{flex:1;min-width:240px;max-width:420px}
    .toolbar select{min-width:170px;cursor:pointer}
    .toolbar label{font-size:.85rem;color:#555;display:inline-flex;align-items:center;gap:.3rem}
    .toolbar .spacer{flex:1}
    .toolbar button.reset{font-size:.8rem;padding:.3rem .65rem;border:1px solid #d0d4da;
         border-radius:6px;background:#fff;color:#555;cursor:pointer}
    .toolbar button.reset:hover{background:#f1f3f7}
    .bucket-tag{display:inline-block;font-size:.72rem;padding:.06rem .45rem;border-radius:10px;
         background:#eef2f7;color:#3a4a5e;border:1px solid #d6dde6;white-space:nowrap}
    .bucket-tag.company{background:#eef7ee;border-color:#cfe5cf;color:#2a5d2f}
    .bucket-tag.unlisted{background:#fbeef3;border-color:#e6c3d4;color:#8a2f5f}
    .bucket-tag.sector{background:#fef5e6;border-color:#f0d8a6;color:#7a5118}
    .bucket-tag.compare{background:#f3eaf7;border-color:#dac3ea;color:#5a2a85}
    .bucket-tag.earnings{background:#eaf2fb;border-color:#c4d8ef;color:#1d4a85}
    .sector-pill{display:inline-block;font-size:.74rem;padding:.08rem .5rem;border-radius:10px;
         background:#f1f3f7;color:#3a4a5e;border:1px solid #dadfe6;white-space:nowrap}
    .ticker{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.83rem;color:#444;
         white-space:nowrap}
    .lang-link{display:inline-block;font-size:.74rem;padding:.06rem .42rem;border-radius:4px;
         border:1px solid #cfd6df;color:#0366d6;text-decoration:none;margin-right:.25rem}
    .lang-link:hover{background:#eef4fb;text-decoration:none}
    .lang-link.docx{background:#fff0d8;border-color:#e0b170;color:#8a5400}
    /* Horizontal scroll on narrow viewports (tablet) — the table has 9
       columns and won't fit under ~1100 px. overflow-x:auto lets users
       drag the table right; the first column is sticky so they always
       see which row they're on. */
    .grid-wrap{background:#fff;border:1px solid #e3e6eb;border-radius:8px;
         overflow-x:auto;overflow-y:visible;-webkit-overflow-scrolling:touch;
         box-shadow:0 1px 2px rgba(0,0,0,.03)}
    .page table{width:100%;border-collapse:collapse;margin:0;min-width:1100px}
    .page th,.page td{text-align:left;padding:.5rem .7rem;border-bottom:1px solid #eef0f3;
         vertical-align:middle}
    .page tbody tr:hover{background:#fafbfc}
    .page tbody tr:last-child td{border-bottom:none}
    /* Sticky first column ("Report" title) so it stays in view while you
       scroll horizontally. Opaque background is required for sticky to
       hide the cells underneath it during scroll. */
    .page th:first-child,.page td:first-child{position:sticky;left:0;z-index:1;
         background:#fff;box-shadow:1px 0 0 #eef0f3}
    .page thead th:first-child{background:#fafbfc;z-index:2}
    .page tbody tr:hover td:first-child{background:#fafbfc}
    .page th{font-size:.74rem;color:#5a5f66;font-weight:600;cursor:pointer;user-select:none;
         background:#fafbfc;border-bottom:1px solid #e3e6eb;text-transform:uppercase;letter-spacing:.04em}
    .page th .sort-ind{color:#bbb;font-size:.7rem;margin-left:.2rem}
    .page th.active{color:#1f4e78}
    .page td.created,.page td.date{color:#666;white-space:nowrap;font-variant-numeric:tabular-nums;font-size:.86rem}
    .page td.mkt-cap{text-align:right;font-variant-numeric:tabular-nums;font-size:.88rem;color:#222;
         white-space:nowrap}
    .page td.mkt-cap.dim{color:#bbb}
    .page td a.title{color:#0366d6;text-decoration:none;font-weight:500}
    .page td a.title:hover{text-decoration:underline}
    .empty{color:#888;font-style:italic}
    .count{color:#666;font-size:.85rem;margin-left:.4rem}
    .pending-note{color:#7a5118;font-size:.78rem;margin-left:.5rem}
    /* Column toggle — default OFF; only essential columns
       (Report / Market Cap / Created / Lang) stay visible. */
    .col-extra{display:none}
    body.show-extra-cols .col-extra{display:table-cell}
    /* With extras hidden, the table no longer needs the 1100px floor. */
    body:not(.show-extra-cols) .page table{min-width:auto}
  </style>
</head>
<body>
__URLPATCH__
  {{ _nav | safe }}
  <div class="page">
    <h1>Claude Reports
      <span class="count" id="count">{{ rows|length }} entries</span>
      {% if pending %}
        <span class="pending-note">· market cap loading {{ pending }} ticker(s) — refresh in ~1 min</span>
      {% endif %}
    </h1>
    <div class="subtitle">Filter by sector, search by company/ticker, or click any column to sort.</div>
    {% if rows %}
    <div class="toolbar">
      <input id="filter" type="search" placeholder="Filter by company, ticker, or filename…" autofocus>
      <select id="sectorFilter" title="Filter by sector">
        <option value="">All sectors</option>
        {% for s in sectors %}
          <option value="{{ s }}">{{ s }}</option>
        {% endfor %}
        <option value="__none__">— No sector —</option>
      </select>
      <select id="bucketFilter" title="Filter by report type">
        <option value="">All report types</option>
        <optgroup label="By location">
          {% for b in buckets %}
            <option value="bucket:{{ b }}">{{ b }}</option>
          {% endfor %}
        </optgroup>
        <optgroup label="By kind">
          <option value="kind:research">research</option>
          <option value="kind:valuation">valuation</option>
          <option value="kind:initiation">initiation</option>
        </optgroup>
      </select>
      <label><input type="checkbox" id="showMoreCols"> Show more columns</label>
      <div class="spacer"></div>
      <button id="resetBtn" class="reset">Reset</button>
    </div>
    <div class="grid-wrap">
    <table id="grid">
      <thead>
        <tr>
          <th data-sort="display">Report</th>
          <th data-sort="ticker" class="col-extra">Ticker</th>
          <th data-sort="sector" class="col-extra">Sector</th>
          <th data-sort="mktcap" style="text-align:right">Market Cap</th>
          <th data-sort="bucket" class="col-extra">Type</th>
          <th data-sort="rating" class="col-extra">Rating</th>
          <th class="col-extra">Comment</th>
          <th data-sort="ts" class="active">Created <span class="sort-ind">▼</span></th>
          <th>Lang</th>
        </tr>
      </thead>
      <tbody>
        {% for r in rows %}
          <tr data-bucket="{{ r.bucket }}"
              data-kind="{{ r.kind }}"
              data-display="{{ r.display|lower }}"
              data-ticker="{{ r.ticker|lower }}"
              data-sector="{{ r.sector }}"
              data-mktcap="{{ r.mktcap_usd if r.mktcap_usd is not none else -1 }}"
              data-mktcap-native="{{ r.mktcap_raw if r.mktcap_raw is not none else '' }}"
              data-mktcap-currency="{{ r.mktcap_currency or '' }}"
              data-filename="{{ r.rel|lower }}"
              data-date="{{ r.date }}"
              data-ts="{{ r.ts }}"
              data-rating="{{ r.rating or 0 }}">
            <td>
              {% if r.langs.get('docx') %}
                <a class="title" href="{{ _base }}/view-docx/{{ r.langs['docx'] }}">{{ r.display }}</a>
              {% elif r.langs.get('docx_zh') %}
                <a class="title" href="{{ _base }}/view-docx/{{ r.langs['docx_zh'] }}">{{ r.display }}</a>
              {% elif r.langs.get('zh') %}
                <a class="title" href="{{ _base }}/view/{{ r.langs['zh'] }}">{{ r.display }}</a>
              {% elif r.langs.get('en') %}
                <a class="title" href="{{ _base }}/view/{{ r.langs['en'] }}">{{ r.display }}</a>
              {% else %}
                <span class="title">{{ r.display }}</span>
              {% endif %}
            </td>
            <td class="ticker col-extra">{{ r.ticker }}</td>
            <td class="col-extra">{% if r.sector %}<span class="sector-pill">{{ r.sector }}</span>{% endif %}</td>
            <td class="mkt-cap {% if r.mktcap_raw is none %}dim{% endif %}"
                {% if r.mktcap_usd is not none and r.mktcap_currency and r.mktcap_currency != 'USD' %}
                title="≈ ${{ '{:,.0f}'.format(r.mktcap_usd) }} USD (sort key)"
                {% endif %}>{{ r.mktcap_fmt }}</td>
            <td class="col-extra"><span class="bucket-tag {{ r.bucket }}">{{ r.bucket }}</span></td>
            <td class="rating-cell col-extra">
              <span class="star-rating" data-pk="{{ r.pk_enc }}" data-rating="{{ r.rating or 0 }}">
                {% for s in range(1, 6) %}
                <span class="star" data-val="{{ s }}"
                      style="color:{{ '#f5a623' if (r.rating or 0) >= s else '#ccc' }}"
                      onclick="setReportRating('{{ r.pk_enc }}', {{ s }}, this.closest('.star-rating'))">★</span>
                {% endfor %}
              </span>
            </td>
            <td class="comment-cell col-extra" id="comment-cell-{{ r.pk_enc }}">
              <span class="comment-preview" data-comment="{{ (r.comment or '')|e }}"
                    title="Click to preview / edit">{{ r.comment or '—' }}</span>
            </td>
            <td class="created">{{ r.created }}</td>
            <td>
              {% if r.langs.get('en') %}
                <a class="lang-link" href="{{ _base }}/view/{{ r.langs['en'] }}">EN</a>
              {% endif %}
              {% if r.langs.get('zh') %}
                <a class="lang-link" href="{{ _base }}/view/{{ r.langs['zh'] }}">ZH</a>
              {% endif %}
              {% if r.langs.get('docx') %}
                <a class="lang-link docx" href="{{ _base }}/view-docx/{{ r.langs['docx'] }}">DOCX</a>
              {% endif %}
              {% if r.langs.get('docx_zh') %}
                <a class="lang-link docx" href="{{ _base }}/view-docx/{{ r.langs['docx_zh'] }}">DOCX ZH</a>
              {% endif %}
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
    </div>
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
      const sectorFilter = document.getElementById("sectorFilter");
      const bucketFilter = document.getElementById("bucketFilter");
      const resetBtn = document.getElementById("resetBtn");
      const count = document.getElementById("count");

      function applyFilter() {
        const q  = (filter.value || "").trim().toLowerCase();
        const s  = sectorFilter.value || "";
        const tk = bucketFilter.value || "";

        // Type filter encodes the axis in the value: "bucket:<name>" or "kind:<name>".
        const tkAxis = tk.startsWith("kind:") ? "kind" : tk.startsWith("bucket:") ? "bucket" : "";
        const tkVal  = tk.split(":", 2)[1] || "";

        let visible = 0;
        for (const r of rows) {
          const hay = r.dataset.display + " " + r.dataset.ticker + " " + r.dataset.filename;
          const rowSector = r.dataset.sector || "";
          const matchQ  = !q || hay.includes(q);
          const matchS  = !s || (s === "__none__" ? rowSector === "" : rowSector === s);
          const matchT  = !tkAxis
            || (tkAxis === "bucket" && r.dataset.bucket === tkVal)
            || (tkAxis === "kind"   && r.dataset.kind   === tkVal);
          const show = matchQ && matchS && matchT;
          r.style.display = show ? "" : "none";
          if (show) visible++;
        }
        count.textContent = visible + " entries";
      }
      filter.addEventListener("input", applyFilter);
      sectorFilter.addEventListener("change", applyFilter);
      bucketFilter.addEventListener("change", applyFilter);
      resetBtn.addEventListener("click", () => {
        filter.value = "";
        sectorFilter.value = "";
        bucketFilter.value = "";
        applyFilter();
      });
      applyFilter();

      // Click-to-sort on headers (toggle asc/desc).
      let sortKey = "ts", sortDir = -1;  // newest first by default
      const numericKeys = new Set(["ts", "mktcap", "rating"]);
      grid.querySelectorAll("th[data-sort]").forEach(th => {
        th.addEventListener("click", () => {
          const k = th.dataset.sort;
          if (k === sortKey) sortDir = -sortDir;
          else { sortKey = k; sortDir = (numericKeys.has(k) || k === "date") ? -1 : 1; }
          rows.sort((a, b) => {
            const av = a.dataset[sortKey] || "";
            const bv = b.dataset[sortKey] || "";
            if (numericKeys.has(sortKey)) return (Number(av) - Number(bv)) * sortDir;
            return av.localeCompare(bv) * sortDir;
          });
          for (const r of rows) tbody.appendChild(r);
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

      // ── "Show more columns" toggle — default OFF, persisted ─────────────
      const COLS_KEY = "reports_show_extra_cols_v1";
      const showMoreCols = document.getElementById("showMoreCols");
      function applyCols(show) {
        document.body.classList.toggle("show-extra-cols", show);
        showMoreCols.checked = show;
      }
      applyCols(localStorage.getItem(COLS_KEY) === "1");
      showMoreCols.addEventListener("change", function() {
        localStorage.setItem(COLS_KEY, this.checked ? "1" : "0");
        applyCols(this.checked);
      });
    })();
  </script>

__MCW_MODALS__
__MCW_FOOTER__
  <script src="/static/vendor/bootstrap.bundle.min.js"></script>
  <script>
    function setReportRating(pkEnc, rating, container) {
      const current = parseInt(container.dataset.rating) || 0;
      const newRating = (current === rating) ? 0 : rating;
      fetch('/rate/' + pkEnc, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'rating=' + newRating,
      }).then(r => {
        if (r.ok) {
          container.dataset.rating = newRating;
          container.querySelectorAll('.star').forEach(s => {
            s.style.color = (newRating >= parseInt(s.dataset.val)) ? '#f5a623' : '#ccc';
          });
          const tr = container.closest('tr');
          if (tr) tr.dataset.rating = newRating;
        }
      });
    }

__MCW_JS__
  </script>
</body>
</html>
"""

# Apply shared markdown comment widget substitutions + URL_PATCH for the
# blueprint-prefix-aware fetch() shim used by MCW.
for _k, _v in _mcw.TEMPLATE_PARTS.items():
    _INDEX_TMPL = _INDEX_TMPL.replace(_k, _v)
_INDEX_TMPL = _INDEX_TMPL.replace("__URLPATCH__", _nw.URL_PATCH_JS)


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

    /* ── Inline comments ─────────────────────────────────────────────── */
    mark.ric-hl{background:#ffe9a3;cursor:pointer;border-bottom:2px solid #f0c14b;
                padding:.02em .1em;border-radius:2px}
    mark.ric-hl:hover{background:#ffd966}
    mark.ric-hl.active{background:#ffbe33}
    .ric-fab{position:absolute;z-index:1500;background:#1F4E78;color:#fff;
             border:none;border-radius:16px;padding:5px 12px;font-size:.85rem;
             cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.25);display:none;
             font-family:-apple-system,sans-serif}
    .ric-fab:hover{background:#16395a}
    .ric-toggle{position:fixed;top:64px;right:0;z-index:99;background:#1F4E78;
                color:#fff;border:none;border-top-left-radius:6px;border-bottom-left-radius:6px;
                padding:7px 11px;font-size:.85rem;cursor:pointer;
                box-shadow:-2px 2px 6px rgba(0,0,0,.12);font-family:-apple-system,sans-serif}
    .ric-toggle:hover{background:#16395a}
    .ric-sidebar{position:fixed;top:60px;right:0;width:340px;max-height:85vh;
                 overflow-y:auto;background:#fafbfd;border-left:1px solid #d8dde6;
                 padding:12px 16px;font-family:-apple-system,sans-serif;font-size:.9rem;
                 z-index:100;box-shadow:-2px 0 8px rgba(0,0,0,.06);display:none}
    .ric-sidebar.open{display:block}
    .ric-sidebar h3{font-size:.95rem;color:#333;margin:0 0 10px;display:flex;
                    align-items:center;justify-content:space-between}
    .ric-sidebar h3 .close{background:none;border:none;font-size:1.2rem;cursor:pointer;color:#888}
    .ric-item{padding:9px 10px;margin-bottom:9px;background:#fff;
              border:1px solid #e0e4ea;border-radius:6px;cursor:pointer}
    .ric-item:hover{border-color:#1F4E78}
    .ric-item.orphan{background:#fff8e7;border-color:#f0d8a6}
    .ric-quote{font-size:.78rem;color:#555;font-style:italic;
               border-left:3px solid #ffd966;padding:2px 0 2px 8px;
               margin-bottom:6px;max-height:3.6em;overflow:hidden;line-height:1.4}
    .ric-body{font-size:.88rem;color:#222;line-height:1.45}
    .ric-body p{margin:0 0 .3em}
    .ric-body ul,.ric-body ol{padding-left:1.2em;margin:.2em 0}
    .ric-meta{font-size:.7rem;color:#888;margin-top:5px;font-family:ui-monospace,Menlo,monospace}
    .ric-actions{font-size:.78rem;margin-top:5px;display:flex;gap:10px}
    .ric-actions button{background:none;border:none;color:#0366d6;cursor:pointer;
                        padding:0;font-size:.78rem}
    .ric-actions button.danger{color:#c00}
    .ric-actions button:hover{text-decoration:underline}
    .ric-modal-quote{font-size:.85rem;color:#555;font-style:italic;
                     border-left:3px solid #ffd966;padding:8px 12px;
                     margin-bottom:14px;background:#fffce6;border-radius:0 4px 4px 0;
                     max-height:8em;overflow:auto}
    #ricEmpty{color:#888;font-style:italic;font-size:.85rem;margin:8px 4px}
  </style>
</head>
<body>
  {{ _nav | safe }}
  <div class="doc markdown-body">
    <div class="backlink"><a href="{{ _base }}/">&larr; back to reports</a></div>
    <div id="content"></div>
  </div>

  <button class="ric-fab" id="ricFab" type="button">💬 Comment</button>
  <button class="ric-toggle" id="ricToggle" type="button">💬 <span id="ricCount">0</span></button>
  <aside class="ric-sidebar" id="ricSidebar">
    <h3>Comments <button type="button" class="close" id="ricClose" aria-label="Close">×</button></h3>
    <div id="ricList"></div>
    <p id="ricEmpty">No comments yet. Select text in the document and click "💬 Comment".</p>
  </aside>

  <div class="modal fade" id="ricModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="ricModalTitle">Add comment</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="ric-modal-quote" id="ricModalQuote"></div>
          <textarea id="ricModalBody" class="form-control" rows="6"
                    placeholder="Write a comment… markdown supported"></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" id="ricModalSave">Save</button>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="/static/vendor/bootstrap.bundle.min.js"></script>
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

    root.querySelectorAll("pre code.language-mermaid").forEach(code => {
      const text = code.textContent;
      const wrap = document.createElement("pre");
      wrap.className = "mermaid";
      wrap.textContent = text;
      code.parentElement.replaceWith(wrap);
    });

    await mermaid.run({ querySelector: ".mermaid" });
    // Signal the inline-comments loader that the DOM is ready.
    window._ricDocReady = true;
    document.dispatchEvent(new Event("ric:doc-ready"));
  </script>

  <script>
  (function(){
    const REPORT_PATH = {{ rel | tojson }};
    const API_BASE = {{ _base | tojson }};
    const docRoot = document.getElementById('content');
    const fab = document.getElementById('ricFab');
    const sidebar = document.getElementById('ricSidebar');
    const sidebarList = document.getElementById('ricList');
    const sidebarEmpty = document.getElementById('ricEmpty');
    const toggleBtn = document.getElementById('ricToggle');
    const countEl = document.getElementById('ricCount');
    const closeBtn = document.getElementById('ricClose');
    const modalEl = document.getElementById('ricModal');
    const modalTitleEl = document.getElementById('ricModalTitle');
    const modalQuoteEl = document.getElementById('ricModalQuote');
    const modalBodyEl = document.getElementById('ricModalBody');
    const modalSaveBtn = document.getElementById('ricModalSave');
    const bsModal = new bootstrap.Modal(modalEl);

    let pendingSelection = null;
    let editingId = null;

    function api(path, opts) {
      return fetch(API_BASE + path, opts || {}).then(r => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        if (r.status === 204) return null;
        return r.json();
      });
    }

    // Build a flat text index of all text nodes under docRoot so we can map
    // string offsets back to (node, offset) for Range construction.
    function buildIndex() {
      const nodes = [];
      let full = '';
      const walker = document.createTreeWalker(docRoot, NodeFilter.SHOW_TEXT, {
        acceptNode(n) {
          const p = n.parentNode && n.parentNode.tagName;
          if (p === 'SCRIPT' || p === 'STYLE') return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      let n;
      while ((n = walker.nextNode())) {
        if (!n.nodeValue) continue;
        const start = full.length;
        full += n.nodeValue;
        nodes.push({ node: n, start, end: full.length });
      }
      return { full, nodes };
    }

    function nearestHeading(node) {
      let el = node.nodeType === 1 ? node : node.parentNode;
      while (el && el !== docRoot && el !== document.body) {
        let sib = el;
        while ((sib = sib.previousElementSibling)) {
          if (/^H[1-6]$/.test(sib.tagName)) return sib.textContent.trim();
        }
        el = el.parentNode;
      }
      return null;
    }

    function getSelectionInfo() {
      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
      const range = sel.getRangeAt(0);
      if (!docRoot.contains(range.commonAncestorContainer)) return null;
      const quote = sel.toString();
      if (!quote || !quote.trim()) return null;
      const index = buildIndex();
      let startOff = -1, endOff = -1;
      for (const e of index.nodes) {
        if (e.node === range.startContainer) startOff = e.start + range.startOffset;
        if (e.node === range.endContainer)   endOff   = e.start + range.endOffset;
      }
      if (startOff < 0 || endOff < 0 || endOff <= startOff) return null;
      const prefix = index.full.slice(Math.max(0, startOff - 32), startOff);
      const suffix = index.full.slice(endOff, endOff + 32);
      const heading = nearestHeading(range.startContainer);
      return { quote, prefix, suffix, heading_anchor: heading, rect: range.getBoundingClientRect() };
    }

    function showFab(rect) {
      fab.style.display = 'block';
      fab.style.top  = (window.scrollY + rect.bottom + 6) + 'px';
      fab.style.left = (window.scrollX + rect.left) + 'px';
    }
    function hideFab() { fab.style.display = 'none'; }

    document.addEventListener('mouseup', function(e) {
      if (e.target === fab) return;
      setTimeout(() => {
        const info = getSelectionInfo();
        if (!info) { hideFab(); return; }
        pendingSelection = info;
        showFab(info.rect);
      }, 0);
    });
    document.addEventListener('mousedown', function(e) {
      if (e.target !== fab) hideFab();
    });

    fab.addEventListener('click', function() {
      if (!pendingSelection) return;
      hideFab();
      editingId = null;
      modalTitleEl.textContent = 'Add comment';
      modalQuoteEl.textContent = pendingSelection.quote;
      modalBodyEl.value = '';
      bsModal.show();
      setTimeout(() => modalBodyEl.focus(), 250);
    });

    modalSaveBtn.addEventListener('click', async function() {
      const body = (modalBodyEl.value || '').trim();
      if (!body) { modalBodyEl.focus(); return; }
      try {
        if (editingId) {
          await api('/inline-comments/' + editingId, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ body })
          });
        } else if (pendingSelection) {
          await api('/inline-comments', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              report_path:    REPORT_PATH,
              quote:          pendingSelection.quote,
              prefix:         pendingSelection.prefix,
              suffix:         pendingSelection.suffix,
              heading_anchor: pendingSelection.heading_anchor,
              body,
            })
          });
        }
        bsModal.hide();
        window.getSelection().removeAllRanges();
        await loadAndRender();
        sidebar.classList.add('open');
      } catch (e) {
        alert('Save failed: ' + e.message);
      }
    });

    toggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
    closeBtn.addEventListener('click',  () => sidebar.classList.remove('open'));

    function findInIndex(idx, c) {
      const targets = [];
      if (c.prefix || c.suffix) targets.push({ needle: c.prefix + c.quote + c.suffix, off: (c.prefix || '').length });
      targets.push({ needle: c.quote, off: 0 });
      for (const t of targets) {
        if (!t.needle) continue;
        const i = idx.full.indexOf(t.needle);
        if (i >= 0) return { start: i + t.off, end: i + t.off + c.quote.length };
      }
      return null;
    }

    // Wrap [oStart, oEnd) in the document text with <mark.ric-hl>. Splits
    // across multiple text nodes when the range crosses element boundaries.
    function wrapRange(idx, oStart, oEnd, cid) {
      const segs = [];
      for (const e of idx.nodes) {
        if (e.end <= oStart) continue;
        if (e.start >= oEnd) break;
        const ls = Math.max(0, oStart - e.start);
        const le = Math.min(e.node.nodeValue.length, oEnd - e.start);
        if (ls >= le) continue;
        segs.push({ node: e.node, start: ls, end: le });
      }
      const marks = [];
      for (const seg of segs) {
        const n = seg.node;
        if (!n.parentNode) continue;
        const before = n.nodeValue.slice(0, seg.start);
        const middle = n.nodeValue.slice(seg.start, seg.end);
        const after  = n.nodeValue.slice(seg.end);
        const mk = document.createElement('mark');
        mk.className = 'ric-hl';
        mk.dataset.cid = String(cid);
        mk.textContent = middle;
        const frag = document.createDocumentFragment();
        if (before) frag.appendChild(document.createTextNode(before));
        frag.appendChild(mk);
        if (after)  frag.appendChild(document.createTextNode(after));
        n.parentNode.replaceChild(frag, n);
        marks.push(mk);
      }
      return marks;
    }

    function clearHighlights() {
      docRoot.querySelectorAll('mark.ric-hl').forEach(m => {
        const t = document.createTextNode(m.textContent);
        m.parentNode.replaceChild(t, m);
      });
      docRoot.normalize();
    }

    function fmtTime(s) {
      if (!s) return '';
      return s.replace('T', ' ').replace('Z', '');
    }

    function renderSidebar(items) {
      sidebarList.innerHTML = '';
      countEl.textContent = items.length;
      sidebarEmpty.style.display = items.length ? 'none' : 'block';
      for (const it of items) {
        const div = document.createElement('div');
        div.className = 'ric-item' + (it.orphan ? ' orphan' : '');
        div.dataset.id = it.id;

        const q = document.createElement('div');
        q.className = 'ric-quote';
        q.textContent = it.quote.length > 120 ? it.quote.slice(0, 120) + '…' : it.quote;

        const b = document.createElement('div');
        b.className = 'ric-body';
        b.innerHTML = window.marked ? marked.parse(it.body || '') : (it.body || '');

        const meta = document.createElement('div');
        meta.className = 'ric-meta';
        meta.textContent = (it.orphan ? '⚠ orphan · ' : '') +
                           (it.heading_anchor ? '§ ' + it.heading_anchor + ' · ' : '') +
                           fmtTime(it.updated_at || it.created_at);

        const actions = document.createElement('div');
        actions.className = 'ric-actions';
        const eBtn = document.createElement('button');
        eBtn.type = 'button'; eBtn.textContent = '✏️ Edit';
        eBtn.addEventListener('click', (e) => { e.stopPropagation(); openEdit(it); });
        const dBtn = document.createElement('button');
        dBtn.type = 'button'; dBtn.textContent = '🗑 Delete'; dBtn.className = 'danger';
        dBtn.addEventListener('click', (e) => { e.stopPropagation(); deleteOne(it.id); });
        actions.append(eBtn, dBtn);

        div.append(q, b, meta, actions);
        div.addEventListener('click', () => {
          const mk = docRoot.querySelector('mark.ric-hl[data-cid="' + it.id + '"]');
          if (mk) {
            mk.scrollIntoView({ block: 'center', behavior: 'smooth' });
            mk.classList.add('active');
            setTimeout(() => mk.classList.remove('active'), 1500);
          }
        });
        sidebarList.appendChild(div);
      }
    }

    function openEdit(item) {
      editingId = item.id;
      pendingSelection = null;
      modalTitleEl.textContent = 'Edit comment';
      modalQuoteEl.textContent = item.quote;
      modalBodyEl.value = item.body || '';
      bsModal.show();
      setTimeout(() => modalBodyEl.focus(), 250);
    }

    async function deleteOne(id) {
      if (!confirm('Delete this comment?')) return;
      try {
        await api('/inline-comments/' + id, { method: 'DELETE' });
        await loadAndRender();
      } catch (e) { alert('Delete failed: ' + e.message); }
    }

    async function loadAndRender() {
      clearHighlights();
      let resp;
      try {
        resp = await api('/inline-comments?report=' + encodeURIComponent(REPORT_PATH));
      } catch (e) {
        console.error('Failed to load inline comments', e);
        return;
      }
      const items = resp.comments || [];
      // Re-anchor each comment. Rebuild the index after every successful
      // wrap so subsequent searches see the still-unwrapped text.
      for (const c of items) {
        const idx = buildIndex();
        const found = findInIndex(idx, c);
        if (found) {
          const marks = wrapRange(idx, found.start, found.end, c.id);
          marks.forEach(m => m.addEventListener('click', (e) => {
            e.stopPropagation();
            openEdit(c);
          }));
          c.orphan = false;
        } else {
          c.orphan = true;
        }
      }
      renderSidebar(items);
    }

    function whenDocReady(cb) {
      if (window._ricDocReady) return cb();
      document.addEventListener('ric:doc-ready', cb, { once: true });
    }
    whenDocReady(loadAndRender);
  })();
  </script>
</body>
</html>
"""


# --- routes ------------------------------------------------------------------

@reports_bp.route("/")
def index():
    rows = _scan()

    # Attach sector + market cap. Market caps come from a per-day sqlite
    # cache; the first call of the day kicks off a background fetch for
    # uncached tickers so the page renders fast and fills in on reload.
    unique_tickers = sorted({r["ticker"] for r in rows if r.get("ticker")})
    mcap = get_market_caps(unique_tickers, block=False) if unique_tickers else {}

    # Daily-cached USD FX rates so sort-by-market-cap normalises across
    # currencies (KRW/JPY/HKD/etc. → USD) while the display still shows
    # the native-currency value.
    needed_ccys = sorted({c for _v, c in mcap.values() if c})
    fx = get_fx_rates(needed_ccys) if needed_ccys else {}

    # User annotations (rating + comment) — one row per pair_key, stored in a
    # separate sqlite at db/report_annotations.db so the markdown source stays
    # untouched. EN/ZH/DOCX siblings share a single annotation via pair_key.
    annotations = _ra.get_all()

    for r in rows:
        t = r.get("ticker") or ""
        r["sector"] = sector_for(t)
        raw, cur = mcap.get(t, (None, None))
        r["mktcap_raw"] = raw            # native-currency value
        r["mktcap_currency"] = cur
        r["mktcap_usd"] = to_usd(raw, cur, fx)  # used as sort key
        r["mktcap_fmt"] = format_market_cap(raw, cur)
        ann = annotations.get(r["pair_key"], {})
        r["rating"] = ann.get("rating") or 0
        r["comment"] = ann.get("comment") or ""
        r["pk_enc"] = urllib.parse.quote(r["pair_key"], safe="")
        # Kind = the report-type token in the filename, used as a second
        # axis in the Type filter so users can narrow to research vs
        # valuation vs initiation across all folder buckets.
        stem = r["rel"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        kind = "other"
        for tok, label in (
            ("_Research_Document", "research"),
            ("_公司研究", "research"),
            ("_研究报告", "research"),
            ("_Valuation_Analysis", "valuation"),
            ("_Initiation_Report", "initiation"),
        ):
            if tok in stem:
                kind = label
                break
        r["kind"] = kind

    # Dropdown options — present every known sector and bucket plus any
    # extras we actually see in the data.
    seen_sectors = {r["sector"] for r in rows if r["sector"]}
    sectors = list(ALL_SECTORS) + sorted(s for s in seen_sectors if s not in ALL_SECTORS)
    buckets = sorted({r.get("bucket", "") for r in rows if r.get("bucket")})

    return render_template_string(
        _INDEX_TMPL,
        rows=rows,
        sectors=sectors,
        buckets=buckets,
        pending=pending_count(),
        _nav=_nw.NAV_HTML,
    )


_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


@reports_bp.route("/view/<path:rel>")
def view(rel: str):
    """Serve .md as rendered HTML; serve images directly. Path-traversal-safe."""
    if ".." in rel.split("/"):
        abort(404)
    target = (REPORTS_DIR / rel).resolve()
    try:
        target.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        abort(404)

    if rel.endswith(".md"):
        if not target.is_file():
            abort(404)
        md = target.read_text(encoding="utf-8")
        return render_template_string(
            _VIEW_TMPL, name=target.name, md=md, rel=rel, _nav=_nw.NAV_HTML
        )

    if target.suffix.lower() not in _IMAGE_EXTS or not target.is_file():
        abort(404)
    return send_from_directory(target.parent, target.name)


@reports_bp.route("/rate/<path:pair_key>", methods=["POST"])
def rate(pair_key: str):
    try:
        rating = int(request.form.get("rating", 0))
    except (TypeError, ValueError):
        return jsonify(error="invalid rating"), 400
    _ra.set_rating(pair_key, rating)
    return "", 204


@reports_bp.route("/comment/<path:pair_key>", methods=["POST"])
def comment(pair_key: str):
    _ra.set_comment(pair_key, request.form.get("comment", ""))
    return "", 204


# --- inline (selection-anchored) comments -----------------------------------
# Distinct from the per-report comment above: these anchor to a slice of text
# inside the rendered MD via a Hypothes.is-style TextQuoteSelector.

@reports_bp.route("/inline-comments", methods=["GET"])
def inline_comments_list():
    rel = request.args.get("report", "").strip()
    if not rel:
        return jsonify(error="missing report"), 400
    return jsonify(comments=_ric.list_for_report(rel))


@reports_bp.route("/inline-comments", methods=["POST"])
def inline_comments_create():
    data = request.get_json(silent=True) or {}
    rel = (data.get("report_path") or "").strip()
    quote = (data.get("quote") or "").strip()
    body = (data.get("body") or "").strip()
    if not rel or not quote or not body:
        return jsonify(error="report_path, quote, body required"), 400
    row = _ric.create(
        report_path=rel,
        quote=quote,
        prefix=data.get("prefix") or "",
        suffix=data.get("suffix") or "",
        heading_anchor=data.get("heading_anchor") or None,
        body=body,
    )
    return jsonify(comment=row), 201


@reports_bp.route("/inline-comments/<int:cid>", methods=["PATCH"])
def inline_comments_update(cid: int):
    data = request.get_json(silent=True) or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify(error="body required"), 400
    row = _ric.update(cid, body)
    if not row:
        return jsonify(error="not found"), 404
    return jsonify(comment=row)


@reports_bp.route("/inline-comments/<int:cid>", methods=["DELETE"])
def inline_comments_delete(cid: int):
    ok = _ric.delete(cid)
    if not ok:
        return jsonify(error="not found"), 404
    return "", 204


_DOCX_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ name }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{background:#f4f4f6;margin:0;font-family:"Times New Roman",Georgia,serif;color:#222}
    .toolbar{position:sticky;top:0;background:#fff;border-bottom:1px solid #e3e3e3;
             padding:10px 24px;display:flex;gap:14px;align-items:center;z-index:10;
             font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:.9rem}
    .toolbar a{color:#0366d6;text-decoration:none}
    .toolbar a.btn{padding:.35rem .7rem;border-radius:4px;border:1px solid #cfd8e3;background:#f8fafd}
    .toolbar a.btn:hover{background:#eef4fb}
    .toolbar .filename{color:#666;margin-left:auto;font-family:ui-monospace,Menlo,monospace;font-size:.8rem}
    .doc{max-width:920px;margin:24px auto;background:#fff;padding:48px 64px;
         box-shadow:0 1px 3px rgba(0,0,0,.08);border:1px solid #e3e3e3}
    .doc h1{font-size:1.9rem;color:#1F4E78;border-bottom:2px solid #1F4E78;
            padding-bottom:.3rem;margin-top:1.5rem}
    .doc h2{font-size:1.4rem;color:#1F4E78;margin-top:1.4rem}
    .doc h3{font-size:1.1rem;color:#C00000;margin-top:1.1rem}
    .doc h4{font-size:1.0rem;color:#1F4E78}
    .doc p{line-height:1.55;margin:.6rem 0;font-size:11pt}
    .doc table{border-collapse:collapse;margin:.8rem 0;width:100%;font-size:10pt;
               font-family:-apple-system,BlinkMacSystemFont,sans-serif}
    .doc table th,.doc table td{border:1px solid #bbb;padding:.4rem .55rem;vertical-align:top}
    .doc table th{background:#1F4E78;color:#fff;font-weight:600}
    .doc table tr:nth-child(even) td{background:#f6f6f9}
    .doc img{max-width:100%;height:auto;display:block;margin:1rem auto;
             box-shadow:0 1px 4px rgba(0,0,0,.1)}
    .doc ul,.doc ol{padding-left:1.6rem}
    .doc li{margin:.3rem 0;line-height:1.5}
    .doc blockquote{border-left:3px solid #999;margin:.8rem 0;padding:.2rem 0 .2rem 1rem;color:#555}
    .doc-warning{background:#fff3cd;border:1px solid #ffeaa7;padding:.6rem 1rem;border-radius:4px;color:#7a5b00;margin:.8rem 0}
  </style>
</head>
<body>
  <div class="toolbar">
    <a href="{{ _base }}/">&larr; back to reports</a>
    <a class="btn" href="{{ _base }}/download-docx/{{ rel }}">⬇ Download .docx</a>
    {% if md_companion %}
      <a class="btn" href="{{ _base }}/view/{{ md_companion }}">📄 View markdown research</a>
    {% endif %}
    <span class="filename">{{ name }}</span>
  </div>
  <div class="doc">
    {% if messages %}
      <div class="doc-warning">
        <strong>Conversion notes:</strong>
        <ul>{% for m in messages %}<li>{{ m }}</li>{% endfor %}</ul>
      </div>
    {% endif %}
    {{ html | safe }}
  </div>
</body>
</html>
"""


def _find_companion_md(rel: str) -> str | None:
    """Given a docx rel path, find a sibling .md research doc in the same folder."""
    p = (REPORTS_DIR / rel).parent
    for cand in p.glob("*_Research_Document_*.md"):
        return str(cand.relative_to(REPORTS_DIR)).replace("\\", "/")
    return None


@reports_bp.route("/view-docx/<path:rel>")
def view_docx(rel: str):
    """Render a .docx file as inline HTML using mammoth (images as data URIs)."""
    if mammoth is None:
        abort(500, "mammoth is not installed. Run: pip install mammoth")
    if ".." in rel.split("/") or not rel.endswith(".docx"):
        abort(404)
    target = (REPORTS_DIR / rel).resolve()
    try:
        target.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        abort(404)
    if not target.is_file():
        abort(404)

    def _image_handler(image):
        with image.open() as src:
            data = src.read()
        b64 = base64.b64encode(data).decode("ascii")
        return {"src": f"data:{image.content_type};base64,{b64}"}

    with open(target, "rb") as f:
        result = mammoth.convert_to_html(
            f, convert_image=mammoth.images.img_element(_image_handler)
        )
    html = result.value
    messages = [str(m) for m in result.messages if str(m).strip()][:5]

    return render_template_string(
        _DOCX_TMPL,
        name=target.name,
        rel=rel,
        html=html,
        messages=messages,
        md_companion=_find_companion_md(rel),
        _nav=_nw.NAV_HTML,
    )


@reports_bp.route("/download-docx/<path:rel>")
def download_docx(rel: str):
    """Serve a .docx file as a download."""
    if ".." in rel.split("/") or not rel.endswith(".docx"):
        abort(404)
    target = (REPORTS_DIR / rel).resolve()
    try:
        target.relative_to(REPORTS_DIR.resolve())
    except ValueError:
        abort(404)
    if not target.is_file():
        abort(404)
    return send_from_directory(target.parent, target.name, as_attachment=True)
