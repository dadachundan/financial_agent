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
import datetime
import sqlite3
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template_string, request, send_file

SCRIPT_DIR  = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR / "zsxq.db"
UPLOADS_DIR = SCRIPT_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

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
  <link href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body            { background:#f4f6f8; padding:24px 16px; }
    h2              { font-weight:700; }
    .stat-badges    { gap:8px; flex-wrap:wrap; margin-bottom:12px; }
    .filter-section { margin-bottom:8px; }
    .filter-label   { font-size:.72rem; color:#888; font-weight:600; text-transform:uppercase;
                      letter-spacing:.04em; white-space:nowrap; align-self:center; }
    .filter-row     { gap:6px; flex-wrap:wrap; align-items:center; margin-bottom:6px; }
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
    .open-btn       { font-size:.75rem; padding:2px 8px; }
    #searchBox      { max-width:240px; }
    .page-footer    { margin-top:24px; font-size:.8rem; color:#888; }
    .count-badge    { font-size:.75rem; }
    .cat-badge      { font-size:.65rem; font-weight:700; padding:1px 4px; border-radius:3px;
                      display:inline-block; margin:1px 0; white-space:nowrap; }
    .cat-yes        { background:#d1f0d8; color:#155724; border:1px solid #b7dfbf; }
    .cat-no         { background:#f0f0f0; color:#999;    border:1px solid #ddd; }
    .cat-unk        { background:#fff8e1; color:#856404; border:1px solid #ffe083; }
    .tag-badge      { font-size:.72rem; font-weight:600; margin:1px 2px; display:inline-block;
                      background:#fce8d4; color:#8a3d00; border:1px solid #f0c090;
                      border-radius:4px; padding:1px 5px; white-space:nowrap; text-decoration:none; }
    .tag-badge:hover { background:#f5d0b0; }
    .edit-icon      { cursor:pointer; color:#bbb; font-size:.75rem; margin-left:2px; }
    .edit-icon:hover { color:#555; }
    .inline-edit    { cursor:pointer; display:block; min-height:1.2em; }
    .inline-edit:hover { background:rgba(0,0,0,.04); border-radius:3px; }
    .tag-edit-input, .comment-edit-input { font-size:.78rem; padding:1px 4px;
                      border:1px solid #999; border-radius:3px; width:100%; }
    /* Comment markdown preview in table cell */
    .comment-preview { cursor:pointer; display:block; min-height:1.2em; max-height:4.5em;
                       overflow:hidden; position:relative; }
    .comment-preview::after { content:''; position:absolute; bottom:0; left:0; right:0;
                               height:1.2em; background:linear-gradient(transparent,#fff); }
    .comment-preview:hover { background:rgba(0,0,0,.03); border-radius:3px; }
    .comment-preview p  { margin:0 0 .2em; }
    .comment-preview ul,.comment-preview ol { padding-left:1.2em; margin:0 0 .2em; }
    .comment-preview img { max-height:3em; border-radius:3px; }
    .comment-preview code { font-size:.8em; background:#f0f0f0; padding:1px 3px; border-radius:2px; }
    /* Comment preview modal body */
    #commentPreviewBody img  { max-width:100%; border-radius:6px; margin:.4em 0; display:block; }
    #commentPreviewBody p    { margin-bottom:.6em; }
    #commentPreviewBody ul,
    #commentPreviewBody ol   { padding-left:1.4em; margin-bottom:.6em; }
    #commentPreviewBody code { background:#f0f0f0; padding:1px 4px; border-radius:3px; font-size:.88em; }
    #commentPreviewBody pre  { background:#f6f8fa; padding:.75em; border-radius:6px; overflow:auto; }
    /* EasyMDE inside modal */
    #commentModal .EasyMDEContainer { height:100%; }
    #commentModal .CodeMirror        { min-height:220px; font-size:.9rem; }
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
    {% if stats.no_pdf > 0 %}
    <button class="btn btn-sm btn-outline-danger ms-2"
            onclick="deleteNoPdf({{ stats.no_pdf }})">🗑 Delete {{ stats.no_pdf }} rows without PDF</button>
    {% endif %}
    <a href="/print-view?{{ query_string }}" target="_blank"
       class="btn btn-sm btn-outline-secondary ms-2">📄 Export PDF</a>
  </div>

  <!-- Status filters -->
  <div class="filter-section">
    <div class="d-flex filter-row">
      <span class="filter-label">Status:</span>
      {%- set sp   = '&sort=' ~ current_sort if current_sort != 'desc' else '' %}
      {%- set tp   = ('&ticker=' ~ current_ticker) if current_ticker else '' %}
      {%- set tagp = ('&tag='    ~ current_tag)    if current_tag    else '' %}
      {%- set dp   = ('&date_from=' ~ current_date_from if current_date_from else '') ~ ('&date_to=' ~ current_date_to if current_date_to else '') %}
    <a href="?filter=all{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-dark' if current_filter=='all' else 'btn-outline-dark' }}">All ({{ stats.total }})</a>
      <a href="?filter=downloaded{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-primary' if current_filter=='downloaded' else 'btn-outline-primary' }}">Downloaded ({{ stats.downloaded }})</a>
      <a href="?filter=unclassified{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-warning text-dark' if current_filter=='unclassified' else 'btn-outline-warning' }}">Unclassified ({{ stats.unclassified }})</a>
    </div>

    <!-- Category filters -->
    <div class="d-flex filter-row">
      <span class="filter-label">Category:</span>
      <a href="?filter=cat_ai{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-success' if current_filter=='cat_ai' else 'btn-outline-success' }}">🤖 AI ({{ stats.cat_ai }})</a>
      <a href="?filter=cat_robotics{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-info' if current_filter=='cat_robotics' else 'btn-outline-info' }}">🦾 Robotics ({{ stats.cat_robotics }})</a>
      <a href="?filter=cat_semi{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-secondary' if current_filter=='cat_semi' else 'btn-outline-secondary' }}">💡 Semiconductor ({{ stats.cat_semi }})</a>
      <a href="?filter=cat_energy{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-warning text-dark' if current_filter=='cat_energy' else 'btn-outline-warning' }}">⚡ Energy ({{ stats.cat_energy }})</a>
      <a href="?filter=cat_any{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-dark' if current_filter=='cat_any' else 'btn-outline-dark' }}">Any category ({{ stats.cat_any }})</a>
      <a href="?filter=cat_none{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-light border' if current_filter=='cat_none' else 'btn-outline-secondary' }}">None ({{ stats.cat_none }})</a>
    </div>

    <!-- Ticker + Search row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Ticker:</span>
      <select id="tickerSelect" class="form-select form-select-sm" style="max-width:200px"
              onchange="applyTicker(this.value)">
        <option value="">All tickers</option>
        {% for t in all_tickers %}
        <option value="{{ t }}" {{ 'selected' if t == current_ticker else '' }}>{{ t }}</option>
        {% endfor %}
      </select>
      <input id="searchBox" type="text" class="form-control form-control-sm ms-2"
             placeholder="Search name / title / ticker / tag…"
             style="max-width:240px" oninput="liveSearch(this.value)">
      <span id="matchCount" class="text-muted small align-self-center ms-1"></span>
    </div>

    <!-- Tag filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Tag:</span>
      <select id="tagSelect" class="form-select form-select-sm" style="max-width:200px"
              onchange="applyTag(this.value)">
        <option value="">All tags</option>
        {% for t in all_tags %}
        <option value="{{ t }}" {{ 'selected' if t == current_tag else '' }}>{{ t }}</option>
        {% endfor %}
      </select>
      {% if current_tag %}
      <a href="#" onclick="applyTag('');return false"
         class="btn btn-sm btn-link text-muted p-0">✕ clear</a>
      {% endif %}
    </div>

    <!-- Date filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Date:</span>
      <input type="date" id="dateFrom" class="form-control form-control-sm" style="max-width:150px"
             value="{{ current_date_from }}">
      <span class="text-muted align-self-center px-1">→</span>
      <input type="date" id="dateTo" class="form-control form-control-sm" style="max-width:150px"
             value="{{ current_date_to }}">
      <button class="btn btn-sm btn-outline-secondary" onclick="applyDateFilter()">Apply</button>
      {% if current_date_from or current_date_to %}
      <a href="#" onclick="clearDateFilter();return false"
         class="btn btn-sm btn-link text-muted p-0">✕ clear</a>
      {% endif %}
    </div>
  </div>

  <!-- Table -->
  <div class="table-responsive shadow-sm rounded">
    <table class="table table-bordered table-hover mb-0" id="mainTable">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>
            <a href="?filter={{ current_filter }}{% if current_ticker %}&ticker={{ current_ticker }}{% endif %}&sort={{ 'asc' if current_sort == 'desc' else 'desc' }}{{ dp }}"
               style="color:inherit;text-decoration:none;white-space:nowrap">
              Date {{ '↑' if current_sort == 'asc' else '↓' }}
            </a>
          </th>
          <th>File name</th>
          <th>Title</th>
          <th>Categories</th>
          <th>Tickers</th>
          <th>Tags</th>
          <th>Size</th>
          <th>Rating</th>
          <th>Summary</th>
          <th>PDF</th>
          <th>Comment</th>
          <th>Analysis</th>
        </tr>
      </thead>
      <tbody>
        {% for idx, row in rows %}
        {%- set any_cat = (row.ai_related == 1 or row.robotics_related == 1
                           or row.semiconductor_related == 1 or row.energy_related == 1) %}
        {%- set unclassed = (row.ai_related is none) %}
        <tr class="{{ 'row-match' if any_cat else ('row-unclassed' if unclassed else 'row-no-match') }}"
            data-search="{{ (row.name ~ ' ' ~ (row.topic_title or '') ~ ' ' ~ (row.tickers or '') ~ ' ' ~ (row.tags or '') ~ ' ' ~ (row.comment or ''))|lower }}">
          <td class="text-muted">{{ idx }}</td>
          <td class="text-nowrap">{{ (row.create_time or '')[:16].replace('T', ' ') }}</td>
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
                <a href="#" onclick="applyTicker('{{ t }}');return false"
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

          <!-- Tags cell -->
          <td style="max-width:110px" id="tags-cell-{{ row.file_id }}">
            <span data-tags="{{ (row.tags or '')|e }}">
              {%- if row.tags %}
                {%- for t in row.tags.split(',') %}
                  {%- set t = t.strip() %}
                  <a href="#" onclick="applyTag('{{ t|e }}');return false"
                     class="tag-badge">{{ t }}</a>
                {%- endfor %}
              {%- endif %}
              <span class="edit-icon" onclick="editTags({{ row.file_id }}, this)" title="Edit tags">✏</span>
            </span>
          </td>

          <td class="text-end text-nowrap">
            {{ '%.1f MB' % (row.file_size / 1048576) if row.file_size else '—' }}
          </td>

          <td class="text-nowrap" style="min-width:90px">
            <span class="star-rating" data-id="{{ row.file_id }}" data-rating="{{ row.user_rating or 0 }}">
              {% for s in range(1, 6) %}
              <span class="star" data-val="{{ s }}"
                    style="cursor:pointer;font-size:1.1rem;color:{{ '#f5a623' if (row.user_rating or 0) >= s else '#ccc' }}"
                    onclick="setRating({{ row.file_id }}, {{ s }}, this.closest('.star-rating'))">★</span>
              {% endfor %}
            </span>
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
              <button class="btn btn-outline-secondary open-btn"
                      onclick="deleteRow({{ row.file_id }}, this)">🗑</button>
            {% endif %}
          </td>

          <!-- Comment cell -->
          <td style="max-width:160px" id="comment-cell-{{ row.file_id }}">
            <span class="comment-preview" data-comment="{{ (row.comment or '')|e }}"
                  onclick="viewComment({{ row.file_id }}, this)"
                  title="Click to preview / edit"></span>
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
</div>

<script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
  const _summaryModal = new bootstrap.Modal(document.getElementById('summaryModal'));
  function showSummary(fileId, el) {
    document.getElementById('summaryModalTitle').textContent = el.dataset.title || '';
    document.getElementById('summaryModalBody').textContent  = el.dataset.full  || '';
    _summaryModal.show();
  }

  function deleteNoPdf(count) {
    if (!confirm('Delete all ' + count + ' rows that have no local PDF?\\nThis cannot be undone.')) return;
    fetch('/delete-no-pdf', { method: 'POST' }).then(r => r.json()).then(data => {
      alert('Deleted ' + data.deleted + ' rows.');
      window.location.reload();
    });
  }

  function deleteRow(fileId, btn) {
    if (!confirm('Delete this entry from the database?')) return;
    fetch('/delete/' + fileId, { method: 'POST' }).then(r => {
      if (r.ok) {
        const tr = btn.closest('tr');
        tr.style.transition = 'opacity .3s';
        tr.style.opacity = '0';
        setTimeout(() => tr.remove(), 300);
      }
    });
  }

  function applyTicker(ticker) {
    const params = new URLSearchParams(window.location.search);
    if (ticker) {
      params.set('ticker', ticker);
    } else {
      params.delete('ticker');
    }
    window.location.href = '?' + params.toString();
  }

  function setRating(fileId, rating, container) {
    const current = parseInt(container.dataset.rating) || 0;
    const newRating = (current === rating) ? 0 : rating;  // click same star = clear
    fetch('/rate/' + fileId, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'rating=' + newRating,
    }).then(r => {
      if (r.ok) {
        container.dataset.rating = newRating;
        container.querySelectorAll('.star').forEach(s => {
          s.style.color = (newRating >= parseInt(s.dataset.val)) ? '#f5a623' : '#ccc';
        });
      }
    });
  }

  function applyDateFilter() {
    const params = new URLSearchParams(window.location.search);
    const from = document.getElementById('dateFrom').value;
    const to   = document.getElementById('dateTo').value;
    if (from) { params.set('date_from', from); } else { params.delete('date_from'); }
    if (to)   { params.set('date_to',   to);   } else { params.delete('date_to');   }
    window.location.href = '?' + params.toString();
  }

  function clearDateFilter() {
    const params = new URLSearchParams(window.location.search);
    params.delete('date_from');
    params.delete('date_to');
    window.location.href = '?' + params.toString();
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

  function applyTag(tag) {
    const params = new URLSearchParams(window.location.search);
    if (tag) { params.set('tag', tag); } else { params.delete('tag'); }
    window.location.href = '?' + params.toString();
  }

  function editTags(fileId, btn) {
    const wrapper = btn.closest('[data-tags]');
    const cell    = btn.closest('td');
    const current = wrapper ? wrapper.dataset.tags : '';
    const input   = document.createElement('input');
    input.className   = 'tag-edit-input';
    input.value       = current;
    input.placeholder = 'tag1, tag2, …';
    cell.innerHTML = '';
    cell.appendChild(input);
    input.focus();
    const save = () => {
      fetch('/tags/' + fileId, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'tags=' + encodeURIComponent(input.value),
      }).then(r => r.json()).then(data => renderTagsCell(cell, fileId, data.tags));
    };
    input.addEventListener('blur', save);
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter')  { e.preventDefault(); input.blur(); }
      if (e.key === 'Escape') { renderTagsCell(cell, fileId, current); }
    });
  }

  function renderTagsCell(cell, fileId, tagsStr) {
    const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(Boolean) : [];
    const span = document.createElement('span');
    span.dataset.tags = tagsStr || '';
    tags.forEach(t => {
      const a = document.createElement('a');
      a.href = '#'; a.className = 'tag-badge'; a.textContent = t;
      a.onclick = e => { e.preventDefault(); applyTag(t); };
      span.appendChild(a);
    });
    const ei = document.createElement('span');
    ei.className = 'edit-icon'; ei.textContent = ' ✏'; ei.title = 'Edit tags';
    ei.onclick = () => editTags(fileId, ei);
    span.appendChild(ei);
    cell.innerHTML = ''; cell.appendChild(span);
    // update row data-search
    const tr = cell.closest('tr');
    if (tr) tr.dataset.search = (tr.dataset.search || '').replace(/\btag:[^\s]*/g, '') + ' ' + tags.join(' ');
  }

  // ── Comment editor (EasyMDE modal) ───────────────────────────────────────
  const _commentModal        = new bootstrap.Modal(document.getElementById('commentModal'));
  const _commentPreviewModal = new bootstrap.Modal(document.getElementById('commentPreviewModal'));
  let _easyMDE       = null;
  let _editingFileId = null;
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
    // Clipboard paste: detect image data and upload it
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
              if (d.data && d.data.filePath) {
                cm.replaceSelection(`![image](${d.data.filePath})`);
              }
            });
          break;
        }
      }
    });
    return _easyMDE;
  }

  // Click on cell → preview modal
  function viewComment(fileId, span) {
    _editingFileId = fileId;
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
    setTimeout(() => editComment(_editingFileId, _previewSpan), 300);
  });

  function editComment(fileId, span) {
    _editingFileId = fileId;
    const mde = _getEasyMDE();
    mde.value(span.dataset.comment || '');
    _commentModal.show();
    setTimeout(() => mde.codemirror.focus(), 320);
  }

  document.getElementById('commentSaveBtn').addEventListener('click', () => {
    const val = _easyMDE ? _easyMDE.value().trim() : '';
    fetch('/comment/' + _editingFileId, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'comment=' + encodeURIComponent(val),
    }).then(r => {
      if (r.ok) {
        const cell = document.getElementById('comment-cell-' + _editingFileId);
        if (cell) renderCommentCell(cell, _editingFileId, val);
        _commentModal.hide();
      }
    });
  });

  function renderCommentCell(cell, fileId, comment) {
    const span = document.createElement('span');
    span.className       = 'comment-preview';
    span.dataset.comment = comment || '';
    span.title           = 'Click to preview / edit';
    if (comment) {
      span.innerHTML = marked.parse(comment);
    } else {
      span.textContent = '—';
    }
    span.onclick = () => viewComment(fileId, span);
    cell.innerHTML = ''; cell.appendChild(span);
  }

  // Render markdown in all comment cells on page load
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.comment-preview').forEach(span => {
      const comment = span.dataset.comment || '';
      const fileId  = span.closest('td').id.replace('comment-cell-', '');
      if (comment) {
        span.innerHTML = marked.parse(comment);
      } else {
        span.textContent = '—';
      }
      span.onclick = () => viewComment(fileId, span);
    });
  });
</script>
</body>
</html>
"""

# ── Routes ────────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # allow concurrent reads while downloader writes
    return conn


def _get_all_tags(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT tags FROM pdf_files WHERE tags IS NOT NULL AND tags != ''"
    ).fetchall()
    seen: set[str] = set()
    for r in rows:
        for t in r["tags"].split(","):
            t = t.strip()
            if t:
                seen.add(t)
    return sorted(seen)


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


def _build_where(f: str, ticker: str, tag: str,
                 date_from: str, date_to: str) -> tuple[str, list]:
    """Build WHERE clause + params from filter args (shared by index and print-view)."""
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
    if tag:
        conditions.append("(',' || COALESCE(tags,'') || ',') LIKE ?")
        params.append(f"%,{tag},%")
    if date_from:
        conditions.append("substr(create_time, 1, 10) >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("substr(create_time, 1, 10) <= ?")
        params.append(date_to)
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Comment Export</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           font-size: 12pt; line-height: 1.7; color: #1a1a1a;
           max-width: 800px; margin: 0 auto; padding: 24px 20px; }
    .toolbar { display:flex; gap:8px; margin-bottom:24px; padding-bottom:16px;
               border-bottom:2px solid #e0e0e0; }
    .toolbar button { padding:6px 16px; border:1px solid #ccc; border-radius:4px;
                      cursor:pointer; font-size:.9rem; background:#fff; }
    .toolbar button:hover { background:#f5f5f5; }
    .toolbar button.primary { background:#1a56db; color:#fff; border-color:#1a56db; }
    .report-title { font-size:1.5rem; font-weight:700; margin-bottom:4px; }
    .report-meta  { color:#888; font-size:.85rem; margin-bottom:32px; }
    .entry { margin-bottom:2.5em; padding-bottom:2em; border-bottom:1px solid #e8e8e8; }
    .entry:last-child { border-bottom:none; }
    .entry-title { font-size:1.1rem; font-weight:700; margin-bottom:4px; }
    .entry-meta   { color:#888; font-size:.8rem; margin-bottom:.8em; }
    .entry-comment img  { max-width:100%; border-radius:4px; margin:.5em 0; display:block; }
    .entry-comment p    { margin:.3em 0 .6em; }
    .entry-comment h1,.entry-comment h2,.entry-comment h3
                        { margin:.6em 0 .3em; font-size:1rem; }
    .entry-comment ul,.entry-comment ol { padding-left:1.4em; margin:.3em 0; }
    .entry-comment code { background:#f0f0f0; padding:1px 4px; border-radius:3px;
                          font-size:.88em; font-family:monospace; }
    .entry-comment pre  { background:#f6f8fa; padding:.75em; border-radius:6px;
                          overflow:auto; font-size:.85em; }
    .entry-comment blockquote { border-left:3px solid #ddd; margin:0;
                                 padding-left:1em; color:#555; }
    .no-comment { color:#bbb; font-style:italic; }
    @media print {
      .toolbar { display:none !important; }
      body { padding:0; max-width:100%; }
      .entry { page-break-inside: avoid; }
      a { color: inherit; text-decoration: none; }
    }
  </style>
</head>
<body>
  <div class="toolbar">
    <button class="primary" onclick="window.print()">🖨️ Print / Save as PDF</button>
    <button onclick="window.close()">✕ Close</button>
    <span style="align-self:center;color:#888;font-size:.85rem;margin-left:8px">
      {{ rows|length }} entr{{ 'y' if rows|length == 1 else 'ies' }} with comments
    </span>
  </div>

  <div class="report-title">📋 Comment Export</div>
  <div class="report-meta">
    Generated {{ now }} &nbsp;·&nbsp;
    Filter: {{ filter_label }}{% if current_ticker %} &nbsp;·&nbsp; Ticker: {{ current_ticker }}{% endif %}{% if current_tag %} &nbsp;·&nbsp; Tag: {{ current_tag }}{% endif %}
  </div>

  {% if rows %}
    {% for row in rows %}
    <div class="entry">
      <div class="entry-title">{{ row.topic_title or row.name or '(untitled)' }}</div>
      <div class="entry-meta">
        {{ (row.create_time or '')[:10] }}
        {% if row.tickers %}&nbsp;·&nbsp; {{ row.tickers }}{% endif %}
        {% if row.tags %}&nbsp;·&nbsp; 🏷 {{ row.tags }}{% endif %}
      </div>
      <div class="entry-comment" data-md="{{ (row.comment or '')|e }}"></div>
    </div>
    {% endfor %}
  {% else %}
    <p style="color:#888;font-style:italic">No rows with comments match the current filter.</p>
  {% endif %}

  <script>
    document.querySelectorAll('.entry-comment[data-md]').forEach(el => {
      el.innerHTML = marked.parse(el.dataset.md || '');
    });
  </script>
</body>
</html>
"""


@app.route("/print-view")
def print_view():
    import datetime as dt
    f         = request.args.get("filter", "all")
    ticker    = request.args.get("ticker", "").strip().upper()
    tag       = request.args.get("tag",    "").strip()
    sort      = request.args.get("sort", "desc").lower()
    date_from = request.args.get("date_from", "").strip()
    date_to   = request.args.get("date_to",   "").strip()
    if sort not in ("asc", "desc"):
        sort = "desc"

    where, params = _build_where(f, ticker, tag, date_from, date_to)
    # Only rows that have a comment
    comment_cond = "comment IS NOT NULL AND comment != ''"
    if where:
        where += f" AND {comment_cond}"
    else:
        where = f"WHERE {comment_cond}"

    order = "ASC" if sort == "asc" else "DESC"
    conn = get_conn()
    rows = conn.execute(
        f"SELECT * FROM pdf_files {where} ORDER BY create_time {order}", params
    ).fetchall()
    conn.close()

    filter_labels = {
        "all": "All", "downloaded": "Downloaded", "unclassified": "Unclassified",
        "cat_ai": "AI", "cat_robotics": "Robotics", "cat_semi": "Semiconductor",
        "cat_energy": "Energy", "cat_any": "Any Category", "cat_none": "No Category",
    }

    return render_template_string(
        PRINT_TEMPLATE,
        rows=rows,
        filter_label=filter_labels.get(f, f),
        current_ticker=ticker,
        current_tag=tag,
        now=dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


@app.route("/")
def index():
    f         = request.args.get("filter", "all")
    ticker    = request.args.get("ticker", "").strip().upper()
    tag       = request.args.get("tag",    "").strip()
    sort      = request.args.get("sort", "desc").lower()
    date_from = request.args.get("date_from", "").strip()
    date_to   = request.args.get("date_to",   "").strip()
    if sort not in ("asc", "desc"):
        sort = "desc"

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
        "               THEN 1 ELSE 0 END)                                  AS cat_none, "
        "  SUM(CASE WHEN local_path IS NULL              THEN 1 ELSE 0 END) AS no_pdf "
        "FROM pdf_files"
    ).fetchone()

    where_clause, params = _build_where(f, ticker, tag, date_from, date_to)
    order = "ASC" if sort == "asc" else "DESC"
    rows = conn.execute(
        f"SELECT * FROM pdf_files {where_clause} ORDER BY create_time {order}",
        params,
    ).fetchall()

    all_tickers = _get_all_tickers(conn)
    all_tags    = _get_all_tags(conn)
    conn.close()

    return render_template_string(
        TEMPLATE,
        rows=list(enumerate(rows, 1)),
        stats=stats,
        current_filter=f,
        current_ticker=ticker,
        current_tag=tag,
        current_sort=sort,
        current_date_from=date_from,
        current_date_to=date_to,
        all_tickers=all_tickers,
        all_tags=all_tags,
        db_path=DB_PATH,
        query_string=request.query_string.decode(),
    )


@app.route("/delete-no-pdf", methods=["POST"])
def delete_no_pdf():
    conn = get_conn()
    cur = conn.execute("DELETE FROM pdf_files WHERE local_path IS NULL")
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return jsonify(deleted=deleted)


@app.route("/delete/<int:file_id>", methods=["POST"])
def delete_entry(file_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT local_path FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    if not row:
        conn.close()
        return jsonify(error="not found"), 404
    if row["local_path"]:
        conn.close()
        return jsonify(error="has local file — delete the PDF file first"), 409
    conn.execute("DELETE FROM pdf_files WHERE file_id = ?", (file_id,))
    conn.commit()
    conn.close()
    return "", 204


@app.route("/rate/<int:file_id>", methods=["POST"])
def rate_pdf(file_id: int):
    try:
        rating = int(request.form.get("rating", 0))
        rating = max(0, min(5, rating))
    except (TypeError, ValueError):
        return jsonify(error="invalid rating"), 400

    conn = get_conn()
    conn.execute(
        "UPDATE pdf_files SET user_rating = ? WHERE file_id = ?",
        (rating if rating > 0 else None, file_id),
    )
    conn.commit()
    conn.close()
    return "", 204


@app.route("/tags/<int:file_id>", methods=["POST"])
def set_tags(file_id: int):
    raw = request.form.get("tags", "").strip()
    normalized = ",".join(t.strip() for t in raw.split(",") if t.strip())
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET tags = ? WHERE file_id = ?",
                 (normalized or None, file_id))
    conn.commit()
    conn.close()
    return jsonify(tags=normalized)


@app.route("/comment/<int:file_id>", methods=["POST"])
def set_comment(file_id: int):
    comment = request.form.get("comment", "").strip()
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET comment = ? WHERE file_id = ?",
                 (comment or None, file_id))
    conn.commit()
    conn.close()
    return "", 204


@app.route("/uploads/<path:filename>")
def serve_upload(filename: str):
    path = UPLOADS_DIR / filename
    if not path.exists():
        abort(404)
    return send_file(path)


@app.route("/upload-image", methods=["POST"])
def upload_image():
    f = request.files.get("image")
    if not f:
        return jsonify({"error": "no file"}), 400
    ext = Path(f.filename).suffix.lower() if f.filename else ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}:
        ext = ".jpg"
    today = datetime.date.today()
    subdir = UPLOADS_DIR / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
    subdir.mkdir(parents=True, exist_ok=True)
    name = uuid.uuid4().hex + ext
    f.save(subdir / name)
    rel = f"{today.year}/{today.month:02d}/{today.day:02d}/{name}"
    return jsonify({"data": {"filePath": f"/uploads/{rel}"}})


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
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        local_ip = None
    print(f"  zsxq viewer →  http://127.0.0.1:{args.port}  (localhost)")
    if local_ip:
        print(f"  zsxq viewer →  http://{local_ip}:{args.port}  (LAN)")
    print(f"  DB           →  {DB_PATH}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
