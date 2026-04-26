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
import md_comment_widget as mcw
import nav_widget2 as nw2
from pathlib import Path

import os
import subprocess
import sys
import json as _json

from flask import Flask, Blueprint, Response, abort, jsonify, render_template_string, request, send_file
import ticker_names as _tn

SCRIPT_DIR  = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR / "db" / "zsxq.db"
UPLOADS_DIR = SCRIPT_DIR / "uploads"

zsxq_bp = Blueprint("zsxq", __name__)

app = Flask(__name__)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))
DB_PATH: Path = DEFAULT_DB

# Kick off AKShare ticker-name cache load (instant if cache exists; bg thread if not)
_tn.init()

# ── HTML template ─────────────────────────────────────────────────────────────

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>zsxq PDF Index</title>
  <link href="/static/vendor/bootstrap.min.css" rel="stylesheet">
__MCW_HEAD__
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
    __MCW_CSS__
    /* Column toggle */
    .col-extra { display: none; }
    body.show-extra-cols .col-extra { display: table-cell; }
  </style>
</head>
<body>
__NAV__
__URLPATCH__
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
    <a href="{{ _base | default('') }}/print-view?{{ query_string }}" target="_blank"
       class="btn btn-sm btn-outline-secondary ms-2">📄 Export PDF</a>
    <button class="btn btn-sm btn-outline-info ms-2"
            onclick="enrichTickers(this)"
            title="Look up Chinese company names for bare ticker codes (e.g. 688981 → 中芯国际 688981)">🏷 Enrich Tickers</button>
    <!-- Download new posts -->
    <div class="d-flex align-items-center gap-1 ms-2">
      <input id="dlCount" type="number" value="20" min="1" max="500"
             class="form-control form-control-sm" style="width:70px"
             title="Number of posts to download">
      <button class="btn btn-sm btn-outline-success" onclick="startZsxqDownload()"
              id="dlBtn">⬇ Fetch new</button>
    </div>
  </div>
  <!-- Download log (hidden until active) -->
  <div id="dlPanel" style="display:none" class="mb-2">
    <div id="dlLog" style="font-family:monospace;font-size:.75rem;height:140px;
         overflow-y:auto;background:#1e1e1e;color:#d4d4d4;border-radius:6px;
         padding:6px 10px"></div>
  </div>

  <!-- Status filters -->
  <div class="filter-section">
    <div class="d-flex filter-row">
      <span class="filter-label">Status:</span>
      {%- set sp   = ('&sort=' ~ current_sort if current_sort != 'desc' else '') ~ ('&sort_by=' ~ current_sort_by if current_sort_by != 'date' else '') %}
      {%- set tp   = ('&ticker=' ~ current_ticker) if current_ticker else '' %}
      {%- set tagp = ('&tag='    ~ current_tag)    if current_tag    else '' %}
      {%- set dp   = ('&date_from=' ~ current_date_from if current_date_from else '') ~ ('&date_to=' ~ current_date_to if current_date_to else '') %}
      {%- set rp   = ('&min_rating=' ~ current_min_rating) if current_min_rating else '' %}
      {%- set crp  = ('&min_claude_rating=' ~ current_min_claude_rating) if current_min_claude_rating else '' %}
      {%- set qp   = ('&q=' ~ current_q) if current_q else '' %}
      {%- set bp   = ('&bank=' ~ current_bank) if current_bank else '' %}
      {%- set cwp  = '&with_comment=1' if with_comment else '' %}
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
             style="max-width:280px" value="{{ current_q }}"
             onkeydown="if(event.key==='Enter'){applySearch(this.value)}">
      <button class="btn btn-sm btn-outline-secondary" onclick="applySearch(document.getElementById('searchBox').value)">Apply</button>
      {% if current_q %}
      <a href="#" onclick="applySearch('');return false" class="btn btn-sm btn-link text-muted p-0 ms-1">✕</a>
      {% endif %}
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

    <!-- Group filter row -->
    {% if all_group_ids|length >= 1 %}
    <div class="d-flex filter-row">
      <span class="filter-label">Group:</span>
      <select id="groupSelect" class="form-select form-select-sm" style="max-width:220px"
              onchange="applyGroupId(this.value)">
        <option value="">All groups</option>
        {% for g in all_group_ids %}
        <option value="{{ g }}" {{ 'selected' if g == current_group_id else '' }}>{{ g }}</option>
        {% endfor %}
      </select>
      {% if current_group_id %}
      <a href="#" onclick="applyGroupId('');return false"
         class="btn btn-sm btn-link text-muted p-0">✕ clear</a>
      {% endif %}
    </div>
    {% endif %}

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

    <!-- Rating filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Rating:</span>
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}"
         class="btn btn-sm {{ 'btn-dark' if not current_min_rating and not unrated_only else 'btn-outline-dark' }}">Any</a>
      {% for stars in [1,2,3,4,5] %}
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}&min_rating={{ stars }}"
         class="btn btn-sm {{ 'btn-warning text-dark' if current_min_rating == stars|string else 'btn-outline-warning' }}">
        {{ '★' * stars }}+</a>
      {% endfor %}
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}&unrated=1"
         class="btn btn-sm {{ 'btn-secondary' if unrated_only else 'btn-outline-secondary' }}">Unrated</a>
    </div>

    <!-- Bank filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Bank:</span>
      <select id="bankSelect" class="form-select form-select-sm" style="max-width:200px"
              onchange="applyBank(this.value)">
        <option value="">All banks</option>
        <option value="__none__" {{ 'selected' if current_bank == '__none__' else '' }}>No bank</option>
        {% for b in all_banks %}
        <option value="{{ b }}" {{ 'selected' if b == current_bank else '' }}>{{ b }}</option>
        {% endfor %}
      </select>
      {% if current_bank %}
      <a href="#" onclick="applyBank('');return false"
         class="btn btn-sm btn-outline-secondary">✕ Clear</a>
      {% endif %}
    </div>

    <!-- Claude rating filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">🤖 Claude:</span>
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}{{ rp }}{{ qp }}"
         class="btn btn-sm {{ 'btn-dark' if not current_min_claude_rating else 'btn-outline-dark' }}">Any</a>
      {% for stars in [3,4,5] %}
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}{{ rp }}{{ qp }}&min_claude_rating={{ stars }}"
         class="btn btn-sm {{ 'btn-info' if current_min_claude_rating == stars|string else 'btn-outline-info' }}">
        {{ '★' * stars }}+</a>
      {% endfor %}
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}{{ rp }}{{ qp }}&min_claude_rating=1"
         class="btn btn-sm {{ 'btn-info' if current_min_claude_rating == '1' else 'btn-outline-info' }}">Any rated</a>
    </div>

    <!-- Comment filter row -->
    <div class="d-flex filter-row">
      <span class="filter-label">Comment:</span>
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}{{ rp }}{{ qp }}{{ crp }}{{ bp }}"
         class="btn btn-sm {{ 'btn-dark' if not with_comment else 'btn-outline-dark' }}">Any</a>
      <a href="?filter={{ current_filter }}{{ tp }}{{ tagp }}{{ sp }}{{ dp }}{{ rp }}{{ qp }}{{ crp }}{{ bp }}&with_comment=1"
         class="btn btn-sm {{ 'btn-success' if with_comment else 'btn-outline-success' }}">💬 With comment ({{ stats.with_comment }})</a>
    </div>

    <!-- Column toggle -->
    <div class="d-flex filter-row align-items-center">
      <span class="filter-label">Columns:</span>
      <div class="form-check form-switch mb-0">
        <input class="form-check-input" type="checkbox" id="showMoreCols" role="switch">
        <label class="form-check-label small text-muted" for="showMoreCols">Show more columns</label>
      </div>
    </div>
  </div>

  <!-- Table -->
  <div class="table-responsive shadow-sm rounded">
    <table class="table table-bordered table-hover mb-0" id="mainTable">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>
            <a href="#" onclick="applySort('date');return false"
               style="color:inherit;text-decoration:none;white-space:nowrap">
              Date {{ '↑' if (current_sort_by == 'date' and current_sort == 'asc') else '↓' if current_sort_by == 'date' else '' }}
            </a>
          </th>
          <th>File name</th>
          <th class="col-extra">🤖</th>
          <th>Title</th>
          <th class="col-extra">Categories</th>
          <th class="col-extra">Tickers</th>
          <th class="col-extra">Tags</th>
          <th class="col-extra">Size</th>
          <th class="col-extra">
            <a href="#" onclick="applySort('pages');return false"
               style="color:inherit;text-decoration:none;white-space:nowrap">
              Pages {{ '↑' if (current_sort_by == 'pages' and current_sort == 'asc') else '↓' if current_sort_by == 'pages' else '' }}
            </a>
          </th>
          <th class="col-extra">Rating</th>
          <th>Summary</th>
          <th>PDF</th>
          <th class="col-extra">Comment</th>
          <th class="col-extra">Analysis</th>
          <th class="col-extra">Query</th>
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
          <td class="col-extra text-nowrap" style="font-size:.8rem;color:#0dcaf0;white-space:nowrap">
            {%- if row.claude_rating == 5 %}★★★★★
            {%- elif row.claude_rating == 4 %}★★★★
            {%- elif row.claude_rating == 3 %}★★★
            {%- elif row.claude_rating == 2 %}★★
            {%- elif row.claude_rating == 1 %}★
            {%- else %}{%- endif %}
          </td>
          <td class="title-col">{{ row.topic_title or '—' }}</td>

          <!-- 4-category badges -->
          <td class="cat-col col-extra">
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

          <!-- Tickers cell -->
          <td class="col-extra" style="max-width:110px" id="tickers-cell-{{ row.file_id }}">
            <span data-tickers="{{ (row.tickers or '')|e }}">
              {%- if row.tickers %}
                {%- set ticker_list = row.tickers.split(',') %}
                {%- for t in ticker_list[:5] %}
                  {%- set t = t.strip() %}
                  <a href="#" onclick="applyTicker('{{ t|e }}');return false"
                     class="ticker-badge" style="text-decoration:none"
                     title="Filter by {{ t }}">{{ t }}</a>
                {%- endfor %}
                {%- if ticker_list|length > 5 %}
                  <span class="text-muted" style="font-size:.65rem">+{{ ticker_list|length - 5 }}</span>
                {%- endif %}
              {%- endif %}
              <span class="edit-icon" onclick="editTickers({{ row.file_id }}, this)" title="Edit tickers">✏</span>
            </span>
          </td>

          <!-- Tags cell -->
          <td class="col-extra" style="max-width:110px" id="tags-cell-{{ row.file_id }}">
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

          <td class="col-extra text-end text-nowrap">
            {{ '%.1f MB' % (row.file_size / 1048576) if row.file_size else '—' }}
          </td>

          <td class="col-extra text-end text-nowrap text-muted">
            {{ row.page_count ~ 'pp' if row.page_count else '—' }}
          </td>

          <td class="col-extra text-nowrap" style="min-width:90px">
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

          <td class="text-center" style="white-space:nowrap">
            {% if row.local_path %}
              <a href="{{ _base | default('') }}/pdf/{{ row.file_id }}/{{ row.name }}" target="_blank"
                 class="btn btn-outline-danger open-btn">📄 Open</a>
              <button class="btn btn-outline-secondary btn-sm ms-1 open-btn"
                      onclick="openLocal({{ row.file_id }}, this)"
                      title="{{ row.local_path }}">🗂 Local</button>
              <button class="btn btn-outline-secondary btn-sm ms-1"
                      onclick="syncAnnotations({{ row.file_id }}, this)"
                      title="Read annotations from local PDF and save to comment">📌</button>
            {% else %}
              <button class="btn btn-outline-secondary open-btn"
                      onclick="deleteRow({{ row.file_id }}, this)">🗑</button>
            {% endif %}
          </td>

          <!-- Comment cell -->
          <td class="col-extra" style="max-width:160px" id="comment-cell-{{ row.file_id }}">
            <span class="comment-preview" data-comment="{{ (row.comment or '')|e }}"
                  onclick="viewComment({{ row.file_id }}, this)"
                  title="Click to preview / edit"></span>
          </td>

          <td class="col-extra analysis-col text-muted">
            {{ (row.categories_analysis or row.ai_robotics_analysis or '')[:180] or '—' }}
          </td>
          <td class="col-extra text-nowrap text-muted" style="font-size:.8rem">
            {{ row.query_term or '—' }}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <!-- Pagination -->
  {% if total_pages > 1 %}
  <nav class="mt-2 d-flex align-items-center gap-2">
    <small class="text-muted">
      {{ row_from }}–{{ row_to }} of {{ total_rows }} rows
    </small>
    <ul class="pagination pagination-sm mb-0">
      {% if current_page > 1 %}
        <li class="page-item">
          <a class="page-link" href="?{{ base_qs }}&page={{ current_page - 1 }}">‹</a>
        </li>
      {% endif %}
      {% for p in page_range %}
        {% if p == '…' %}
          <li class="page-item disabled"><span class="page-link">…</span></li>
        {% else %}
          <li class="page-item {{ 'active' if p == current_page else '' }}">
            <a class="page-link" href="?{{ base_qs }}&page={{ p }}">{{ p }}</a>
          </li>
        {% endif %}
      {% endfor %}
      {% if current_page < total_pages %}
        <li class="page-item">
          <a class="page-link" href="?{{ base_qs }}&page={{ current_page + 1 }}">›</a>
        </li>
      {% endif %}
    </ul>
  </nav>
  {% endif %}
  <p class="page-footer">Showing <span id="visibleCount">{{ rows|length }}</span> of {{ total_rows }} rows (page {{ current_page }}/{{ total_pages }}).</p>
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

__MCW_MODALS__


__MCW_FOOTER__
<script src="/static/vendor/bootstrap.bundle.min.js"></script>
<script>
  const _base = "{{ _base | default('') }}";
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

  function startZsxqDownload() {
    const count = parseInt(document.getElementById('dlCount').value) || 20;
    const btn   = document.getElementById('dlBtn');
    const panel = document.getElementById('dlPanel');
    const log   = document.getElementById('dlLog');
    btn.disabled = true;
    btn.textContent = '⏳ Downloading…';
    panel.style.display = '';
    log.innerHTML = '';

    const src = new EventSource('/download-new?count=' + count);
    src.onmessage = e => {
      const d = JSON.parse(e.data);
      const line = document.createElement('div');
      line.textContent = d.msg;
      if (d.error) line.style.color = '#ff6b6b';
      log.appendChild(line);
      log.scrollTop = log.scrollHeight;
      if (d.done) {
        src.close();
        btn.disabled = false;
        btn.textContent = '⬇ Fetch new';
        setTimeout(() => window.location.reload(), 800);
      }
    };
    src.onerror = () => {
      src.close();
      btn.disabled = false;
      btn.textContent = '⬇ Fetch new';
    };
  }

  function enrichTickers(btn) {
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳ Looking up names…';
    fetch('/enrich-tickers', { method: 'POST' })
      .then(r => r.json())
      .then(d => {
        btn.disabled = false;
        btn.textContent = orig;
        if (d.status === 'building') {
          alert(d.message);
        } else if (d.status === 'ok') {
          if (d.updated > 0) {
            alert('Enriched ' + d.updated + ' of ' + d.total + ' rows with Chinese ticker names.');
            location.reload();
          } else {
            alert('All ticker codes already have Chinese names (or no matches found).');
          }
        } else {
          alert(d.message || 'Unknown error');
        }
      })
      .catch(() => { btn.disabled = false; btn.textContent = orig; alert('Request failed'); });
  }

  function openLocal(fileId, btn) {
    const orig = btn.textContent;
    fetch('/open-local/' + fileId)
      .then(r => r.json())
      .then(data => {
        if (!data.ok) {
          btn.textContent = '❌';
          btn.title = data.error || 'Could not open file';
          setTimeout(() => { btn.textContent = orig; btn.title = btn.dataset.path || ''; }, 2500);
        }
      })
      .catch(() => {
        btn.textContent = '❌';
        setTimeout(() => { btn.textContent = orig; }, 2500);
      });
  }

  function syncAnnotations(fileId, btn) {
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳';
    fetch('/sync-annotations/' + fileId, { method: 'POST' })
      .then(r => r.json())
      .then(data => {
        btn.disabled = false;
        btn.textContent = orig;
        if (data.ok) {
          // Update the comment cell in-place using the widget's own function
          const cell = document.getElementById('comment-cell-' + fileId);
          if (cell) renderCommentCell(cell, fileId, data.comment);
          btn.title = data.count + ' annotation(s) saved to comment';
          btn.textContent = '✅';
          setTimeout(() => { btn.textContent = orig; btn.title = 'Read annotations from local PDF and save to comment'; }, 2500);
        } else {
          btn.textContent = '❌';
          btn.title = data.error || 'No annotations found';
          setTimeout(() => { btn.textContent = orig; btn.title = 'Read annotations from local PDF and save to comment'; }, 2500);
        }
      })
      .catch(() => {
        btn.disabled = false;
        btn.textContent = '❌';
        setTimeout(() => { btn.textContent = orig; }, 2000);
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

  function applySearch(q) {
    const params = new URLSearchParams(window.location.search);
    params.delete('page');
    if (q.trim()) { params.set('q', q.trim()); } else { params.delete('q'); }
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

  function applyGroupId(gid) {
    const params = new URLSearchParams(window.location.search);
    params.delete('page');
    if (gid) { params.set('group_id', gid); } else { params.delete('group_id'); }
    window.location.href = '?' + params.toString();
  }

  function applySort(sortBy) {
    const params = new URLSearchParams(window.location.search);
    params.delete('page');
    const currentSortBy = params.get('sort_by') || 'date';
    const currentSort   = params.get('sort')    || 'desc';
    // Toggle direction if same column, else default to desc
    const newSort = (currentSortBy === sortBy && currentSort === 'desc') ? 'asc' : 'desc';
    params.set('sort_by', sortBy);
    params.set('sort', newSort);
    window.location.href = '?' + params.toString();
  }

  function applyBank(bank) {
    const params = new URLSearchParams(window.location.search);
    params.delete('page');
    if (bank) { params.set('bank', bank); } else { params.delete('bank'); }
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

  // ── Tickers inline editing (mirrors editTags) ────────────────────────────
  function editTickers(fileId, btn) {
    const wrapper = btn.closest('[data-tickers]');
    const cell    = btn.closest('td');
    const current = wrapper ? wrapper.dataset.tickers : '';
    const input   = document.createElement('input');
    input.className   = 'tag-edit-input';
    input.value       = current;
    input.placeholder = 'TICKER1, TICKER2, …';
    cell.innerHTML = ''; cell.appendChild(input); input.focus();
    const save = () => {
      fetch('/tickers/' + fileId, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'tickers=' + encodeURIComponent(input.value),
      }).then(r => r.json()).then(data => renderTickersCell(cell, fileId, data.tickers));
    };
    input.addEventListener('blur', save);
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter')  { e.preventDefault(); input.blur(); }
      if (e.key === 'Escape') { renderTickersCell(cell, fileId, current); }
    });
  }

  function renderTickersCell(cell, fileId, tickersStr) {
    const tickers = tickersStr ? tickersStr.split(',').map(t => t.trim()).filter(Boolean) : [];
    const span = document.createElement('span');
    span.dataset.tickers = tickersStr || '';
    tickers.slice(0, 5).forEach(t => {
      const a = document.createElement('a');
      a.href = '#'; a.className = 'ticker-badge'; a.style.textDecoration = 'none';
      a.textContent = t; a.title = 'Filter by ' + t;
      a.onclick = e => { e.preventDefault(); applyTicker(t); };
      span.appendChild(a);
    });
    if (tickers.length > 5) {
      const more = document.createElement('span');
      more.className = 'text-muted'; more.style.fontSize = '.65rem';
      more.textContent = '+' + (tickers.length - 5);
      span.appendChild(more);
    }
    const ei = document.createElement('span');
    ei.className = 'edit-icon'; ei.textContent = ' ✏'; ei.title = 'Edit tickers';
    ei.onclick = () => editTickers(fileId, ei);
    span.appendChild(ei);
    cell.innerHTML = ''; cell.appendChild(span);
    // update row data-search
    const tr = cell.closest('tr');
    if (tr) tr.dataset.search = (tr.dataset.search || '').replace(/\bticker:[^\s]*/g, '') + ' ' + tickers.join(' ');
  }


  __MCW_JS__

  // ── Column toggle ────────────────────────────────────────────────────────
  (function() {
    const KEY = 'zsxq_show_extra_cols_v2';  // v2: default OFF
    const cb  = document.getElementById('showMoreCols');
    function apply(show) {
      document.body.classList.toggle('show-extra-cols', show);
      cb.checked = show;
    }
    // Default OFF unless user explicitly saved ON
    apply(localStorage.getItem(KEY) === '1');
    cb.addEventListener('change', function() {
      localStorage.setItem(KEY, this.checked ? '1' : '0');
      apply(this.checked);
    });
  })();
</script>
</body>
</html>
"""

# Apply shared markdown comment widget substitutions
for _k, _v in mcw.TEMPLATE_PARTS.items():
    TEMPLATE = TEMPLATE.replace(_k, _v)
TEMPLATE = TEMPLATE.replace("__NAV__",      nw2.NAV_HTML)
TEMPLATE = TEMPLATE.replace("__URLPATCH__", nw2.URL_PATCH_JS)


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


def _get_all_group_ids(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT DISTINCT group_id FROM pdf_files WHERE group_id IS NOT NULL AND group_id != '' ORDER BY group_id"
    ).fetchall()
    return [r["group_id"] for r in rows]


def _get_all_banks(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT DISTINCT bank FROM pdf_files WHERE bank IS NOT NULL AND bank != '' ORDER BY bank"
    ).fetchall()
    return [r["bank"] for r in rows]


def _build_where(f: str, ticker: str, tag: str,
                 date_from: str, date_to: str,
                 min_rating: int = 0, q: str = "",
                 group_id: str = "",
                 min_claude_rating: int = 0,
                 unrated: bool = False,
                 bank: str = "",
                 with_comment: bool = False) -> tuple[str, list]:
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
    if unrated:
        conditions.append("(user_rating IS NULL OR user_rating = 0)")
    elif min_rating:
        conditions.append("user_rating >= ?")
        params.append(min_rating)
    if q:
        like = f"%{q}%"
        conditions.append(
            "(name LIKE ? OR topic_title LIKE ? OR tickers LIKE ? OR tags LIKE ? OR comment LIKE ?)"
        )
        params.extend([like, like, like, like, like])
    if group_id:
        conditions.append("group_id = ?")
        params.append(group_id)
    if min_claude_rating:
        conditions.append("claude_rating >= ?")
        params.append(min_claude_rating)
    if bank == "__none__":
        conditions.append("(bank IS NULL OR bank = '')")
    elif bank:
        conditions.append("bank = ?")
        params.append(bank)
    if with_comment:
        conditions.append("comment IS NOT NULL AND comment != ''")
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Comment Export</title>
  <script src="/static/vendor/marked.min.js"></script>
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
__NAV__
__URLPATCH__
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

# Apply nav/urlpatch to PRINT_TEMPLATE (defined above)
PRINT_TEMPLATE = PRINT_TEMPLATE.replace("__NAV__",      nw2.NAV_HTML)
PRINT_TEMPLATE = PRINT_TEMPLATE.replace("__URLPATCH__", nw2.URL_PATCH_JS)


@zsxq_bp.route("/print-view")
def print_view():
    import datetime as dt
    f         = request.args.get("filter", "all")
    ticker    = request.args.get("ticker", "").strip().upper()
    tag       = request.args.get("tag",    "").strip()
    sort      = request.args.get("sort", "desc").lower()
    date_from = request.args.get("date_from", "").strip()
    date_to   = request.args.get("date_to",   "").strip()
    group_id  = request.args.get("group_id", "").strip()
    try:
        min_rating = max(0, min(5, int(request.args.get("min_rating", 0))))
    except ValueError:
        min_rating = 0
    q = request.args.get("q", "").strip()
    if sort not in ("asc", "desc"):
        sort = "desc"

    where, params = _build_where(f, ticker, tag, date_from, date_to, min_rating, q, group_id)
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


_PAGE_SIZE = 30


def _page_range(cur: int, tot: int) -> list:
    if tot <= 7:
        return list(range(1, tot + 1))
    pages: list = [1]
    if cur > 3:
        pages.append("…")
    for p in range(max(2, cur - 1), min(tot, cur + 2)):
        pages.append(p)
    if cur < tot - 2:
        pages.append("…")
    if tot not in pages:
        pages.append(tot)
    return pages


@zsxq_bp.route("/")
def index():
    f          = request.args.get("filter", "all")
    ticker     = request.args.get("ticker", "").strip().upper()
    tag        = request.args.get("tag",    "").strip()
    sort       = request.args.get("sort", "desc").lower()
    sort_by    = request.args.get("sort_by", "date").lower()
    date_from  = request.args.get("date_from", "").strip()
    date_to    = request.args.get("date_to",   "").strip()
    group_id   = request.args.get("group_id", "").strip()
    try:
        min_rating = max(0, min(5, int(request.args.get("min_rating", 0))))
    except ValueError:
        min_rating = 0
    try:
        min_claude_rating = max(0, min(5, int(request.args.get("min_claude_rating", 0))))
    except ValueError:
        min_claude_rating = 0
    unrated = request.args.get("unrated") == "1"
    if unrated:
        min_rating = 0
    bank = request.args.get("bank", "").strip()
    q = request.args.get("q", "").strip()
    with_comment = request.args.get("with_comment") == "1"
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    if sort not in ("asc", "desc"):
        sort = "desc"
    if sort_by not in ("date", "pages"):
        sort_by = "date"

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
        "  SUM(CASE WHEN local_path IS NULL              THEN 1 ELSE 0 END) AS no_pdf, "
        "  SUM(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 ELSE 0 END) AS with_comment "
        "FROM pdf_files"
    ).fetchone()

    where_clause, params = _build_where(f, ticker, tag, date_from, date_to, min_rating, q, group_id, min_claude_rating, unrated, bank, with_comment)
    order      = "ASC" if sort == "asc" else "DESC"
    order_col  = "page_count" if sort_by == "pages" else "create_time"
    # NULLs last for page_count sort
    null_last  = " NULLS LAST" if sort_by == "pages" else ""

    total_rows  = conn.execute(
        f"SELECT COUNT(*) FROM pdf_files {where_clause}", params
    ).fetchone()[0]
    total_pages = max(1, (total_rows + _PAGE_SIZE - 1) // _PAGE_SIZE)
    page        = min(page, total_pages)
    offset      = (page - 1) * _PAGE_SIZE

    rows = conn.execute(
        f"SELECT * FROM pdf_files {where_clause} ORDER BY {order_col} {order}{null_last}"
        f" LIMIT ? OFFSET ?",
        params + [_PAGE_SIZE, offset],
    ).fetchall()

    all_tickers  = _get_all_tickers(conn)
    all_tags     = _get_all_tags(conn)
    all_group_ids = _get_all_group_ids(conn)
    all_banks    = _get_all_banks(conn)
    conn.close()

    # Build base query string without "page" for pagination links
    qs_params = {k: v for k, v in request.args.items() if k != "page"}
    base_qs   = "&".join(f"{k}={v}" for k, v in qs_params.items())

    row_from = offset + 1 if total_rows else 0
    row_to   = min(offset + _PAGE_SIZE, total_rows)

    return render_template_string(
        TEMPLATE,
        rows=list(enumerate(rows, offset + 1)),
        stats=stats,
        current_filter=f,
        current_ticker=ticker,
        current_tag=tag,
        current_sort=sort,
        current_sort_by=sort_by,
        current_date_from=date_from,
        current_date_to=date_to,
        current_min_rating=str(min_rating) if min_rating else "",
        unrated_only=unrated,
        current_q=q,
        current_group_id=group_id,
        current_min_claude_rating=str(min_claude_rating) if min_claude_rating else "",
        all_tickers=all_tickers,
        all_tags=all_tags,
        all_group_ids=all_group_ids,
        all_banks=all_banks,
        current_bank=bank,
        with_comment=with_comment,
        db_path=DB_PATH,
        query_string=request.query_string.decode(),
        # pagination
        current_page=page,
        total_pages=total_pages,
        total_rows=total_rows,
        row_from=row_from,
        row_to=row_to,
        page_range=_page_range(page, total_pages),
        base_qs=base_qs,
    )


@zsxq_bp.route("/download-new")
def download_new():
    try:
        count = max(1, min(500, int(request.args.get("count", 20))))
    except ValueError:
        count = 20

    downloader = SCRIPT_DIR / "download" / "zsxq_downloader.py"

    def generate():
        def _sse(msg: str, *, done: bool = False, error: bool = False) -> str:
            return "data: " + _json.dumps({"msg": msg, "done": done, "error": error}) + "\n\n"

        yield _sse(f"🚀  Starting zsxq_downloader --count {count} …")
        try:
            proc = subprocess.Popen(
                [sys.executable, "-u", str(downloader), "--count", str(count),
                 "--db", str(DB_PATH), "--no-classify"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            for line in proc.stdout:
                line = line.rstrip()
                if line:
                    yield _sse(line)
            proc.wait()
            if proc.returncode == 0:
                yield _sse("✅  Download complete.", done=True)
            else:
                yield _sse(f"❌  Exited with code {proc.returncode}", done=True, error=True)
        except Exception as exc:
            yield _sse(f"❌  {exc}", done=True, error=True)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@zsxq_bp.route("/delete-no-pdf", methods=["POST"])
def delete_no_pdf():
    conn = get_conn()
    cur = conn.execute("DELETE FROM pdf_files WHERE local_path IS NULL")
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return jsonify(deleted=deleted)


@zsxq_bp.route("/delete/<int:file_id>", methods=["POST"])
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


@zsxq_bp.route("/rate/<int:file_id>", methods=["POST"])
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


@zsxq_bp.route("/tags/<int:file_id>", methods=["POST"])
def set_tags(file_id: int):
    raw = request.form.get("tags", "").strip()
    normalized = ",".join(t.strip() for t in raw.split(",") if t.strip())
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET tags = ? WHERE file_id = ?",
                 (normalized or None, file_id))
    conn.commit()
    conn.close()
    return jsonify(tags=normalized)


@zsxq_bp.route("/tickers/<int:file_id>", methods=["POST"])
def set_tickers(file_id: int):
    raw = request.form.get("tickers", "").strip()
    normalized = ",".join(t.strip() for t in raw.split(",") if t.strip())
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET tickers = ? WHERE file_id = ?",
                 (normalized or None, file_id))
    conn.commit()
    conn.close()
    return jsonify(tickers=normalized)


@zsxq_bp.route("/enrich-tickers", methods=["POST"])
def enrich_tickers_route():
    """Bulk-enrich bare ticker codes with Chinese company names via AKShare cache."""
    if _tn.is_building():
        return jsonify(
            status="building",
            message="Building ticker name cache from AKShare (~2 min). Please try again shortly.",
        )
    ticker_map = _tn.get_map()
    if not ticker_map:
        return jsonify(status="error", message="Ticker name cache not available.")

    conn = get_conn()
    rows = conn.execute(
        "SELECT file_id, tickers FROM pdf_files WHERE tickers IS NOT NULL AND tickers != ''"
    ).fetchall()

    updated = 0
    for file_id, tickers_str in rows:
        enriched, n = _tn.enrich_ticker_string(tickers_str, ticker_map)
        if n > 0:
            conn.execute(
                "UPDATE pdf_files SET tickers = ? WHERE file_id = ?",
                (enriched, file_id),
            )
            updated += 1
    conn.commit()
    conn.close()
    return jsonify(status="ok", updated=updated, total=len(rows))


@zsxq_bp.route("/comment/<int:file_id>", methods=["POST"])
def set_comment(file_id: int):
    comment = request.form.get("comment", "").strip()
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET comment = ? WHERE file_id = ?",
                 (comment or None, file_id))
    conn.commit()
    conn.close()
    return "", 204



def _ocr_region(page, rect, scale: float = 2.0) -> str:
    """Render a page region and run macOS Vision OCR on it. Returns '' on failure."""
    try:
        import fitz
        from PIL import Image
        import io
        import AppKit

        # Render the full page at given scale
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Map PDF rect → pixel crop (fitz uses top-left origin, y down)
        pad = 4  # extra pixels to avoid edge clipping
        x0 = max(0, int(rect.x0 * scale) - pad)
        y0 = max(0, int(rect.y0 * scale) - pad)
        x1 = min(pix.width,  int(rect.x1 * scale) + pad)
        y1 = min(pix.height, int(rect.y1 * scale) + pad)
        crop = img.crop((x0, y0, x1, y1))

        buf = io.BytesIO()
        crop.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        import Vision
        ns_data = AppKit.NSData.dataWithBytes_length_(png_bytes, len(png_bytes))
        import Quartz
        ci_image = Quartz.CIImage.imageWithData_(ns_data)
        handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(ci_image, {})
        request = Vision.VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
        request.setUsesLanguageCorrection_(True)
        handler.performRequests_error_([request], None)
        results = request.results() or []
        texts = [r.topCandidates_(1)[0].string() for r in results if r.topCandidates_(1)]
        return " ".join(texts).strip()
    except Exception as e:
        print(f"                   OCR region failed: {e}")
        return ""


def _extract_annotations_from_pdf(path: Path) -> list[dict]:
    """Extract highlight, sticky-note, and free-text annotations from a PDF.

    Uses PyMuPDF (fitz) for speed — falls back to PyPDF2 if not available.
    For highlights with no /Contents (raster PDFs like UBS/GS), runs macOS
    Vision OCR on the highlighted region to recover the text.
    Returns list of {page, type, text, note} dicts sorted by page.
    """
    import time as _t
    _HIGHLIGHT_TYPES = {"Highlight", "Underline", "StrikeOut", "Squiggly"}
    _NOTE_TYPES      = {"Text", "FreeText"}

    try:
        import fitz  # PyMuPDF — much faster than PyPDF2
        _t0 = _t.time()
        try:
            doc = fitz.open(str(path))
        except Exception as e:
            print(f"                   fitz open failed: {e}")
            return []
        print(f"                   fitz opened in {_t.time()-_t0:.2f}s  ({doc.page_count} pages)")

        results = []
        for page_num in range(doc.page_count):
            page = doc[page_num]
            for annot in page.annots():
                ann_type = annot.type[1]  # e.g. "Highlight", "Text"
                if ann_type not in _HIGHLIGHT_TYPES and ann_type not in _NOTE_TYPES:
                    continue
                content = (annot.info.get("content") or "").strip().lstrip("﻿\x00")
                if ann_type in _HIGHLIGHT_TYPES:
                    text = content
                    if not text:
                        # /Contents empty — raster PDF (UBS/GS style).
                        # Use Vision OCR on the highlight region.
                        _t1 = _t.time()
                        text = _ocr_region(page, annot.rect)
                        print(f"                   OCR p{page_num+1} in {_t.time()-_t1:.1f}s: {text[:60]!r}")
                    if not text:
                        continue
                    results.append({"page": page_num + 1, "type": "Highlight",
                                    "text": text, "note": None})
                else:  # Text / FreeText (sticky note)
                    if not content:
                        continue
                    results.append({"page": page_num + 1, "type": ann_type,
                                    "text": content, "note": None})
        doc.close()
        results.sort(key=lambda r: r["page"])
        return results

    except ImportError:
        pass  # fall through to PyPDF2

    # ── PyPDF2 fallback ───────────────────────────────────────────────────────
    import re as _re
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("                   no PDF library available (install pymupdf)")
        return []

    results = []
    try:
        _t0 = _t.time()
        reader = PdfReader(str(path), strict=False)
        print(f"                   PdfReader loaded in {_t.time()-_t0:.1f}s  ({len(reader.pages)} pages)")
    except Exception as e:
        print(f"                   PdfReader failed: {e}")
        return []

    for page_num, page in enumerate(reader.pages, 1):
        if "/Annots" not in page:
            continue
        try:
            annots = page["/Annots"]
        except Exception:
            continue
        for ref in annots or []:
            try:
                a = ref.get_object()
                subtype = str(a.get("/Subtype", "")).strip("/")
                if subtype not in _HIGHLIGHT_TYPES and subtype not in _NOTE_TYPES:
                    continue
                contents = str(a.get("/Contents") or "").strip().lstrip("﻿\x00")
                if subtype in _HIGHLIGHT_TYPES:
                    text = contents or _re.sub(r"<[^>]+>", "", str(a.get("/RC") or "")).strip()
                    if not text:
                        continue
                    results.append({"page": page_num, "type": "Highlight",
                                    "text": text, "note": None})
                else:
                    if not contents:
                        continue
                    results.append({"page": page_num, "type": subtype,
                                    "text": contents, "note": None})
            except Exception:
                continue

    results.sort(key=lambda r: r["page"])
    return results


def _format_annotations(anns: list[dict]) -> str:
    """Format annotations as markdown.

    # P4, P21          ← top-level summary of all cited pages
    ## P4              ← one subheading per unique page
    > highlighted text
    plain note text
    ## P21
    > ...
    """
    # Collect unique pages in order
    seen_pages: list[int] = []
    for a in anns:
        if a["page"] not in seen_pages:
            seen_pages.append(a["page"])

    page_summary = ", ".join(f"P{p}" for p in seen_pages)
    lines = [f"# {page_summary}", ""]

    last_page = None
    for a in anns:
        text = (a["text"] or "").replace("\n", " ").strip()
        if a["page"] != last_page:
            if last_page is not None:
                lines.append("")
            lines.append(f"## P{a['page']}")
            last_page = a["page"]
        if a["type"] == "Highlight":
            lines.append(f"> {text}")
        else:
            lines.append(text)
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


@zsxq_bp.route("/sync-annotations/<int:file_id>", methods=["POST"])
def sync_annotations(file_id: int):
    """Read PDF annotations from disk and save them to the comment field."""
    import time as _time
    import concurrent.futures as _cf
    conn = get_conn()
    row = conn.execute(
        "SELECT local_path, name FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    conn.close()

    if not row or not row["local_path"]:
        print(f"[sync-annotations] ❌ file_id={file_id} — no local file in DB")
        return jsonify(ok=False, error="No local file"), 404

    path = Path(row["local_path"])
    if not path.exists():
        print(f"[sync-annotations] ❌ file not on disk: {path}")
        return jsonify(ok=False, error="File not found on disk"), 404

    print(f"[sync-annotations] 📌 {row['name']}")
    print(f"                   path: {path}")
    t0 = _time.time()

    # Run extraction in a thread with a hard timeout so a malformed PDF
    # can't hang the server indefinitely.
    _TIMEOUT = 15.0
    with _cf.ThreadPoolExecutor(max_workers=1) as _pool:
        _fut = _pool.submit(_extract_annotations_from_pdf, path)
        try:
            anns = _fut.result(timeout=_TIMEOUT)
        except _cf.TimeoutError:
            elapsed = _time.time() - t0
            print(f"                   ⏱ timed out after {elapsed:.1f}s")
            return jsonify(ok=False, error="Timed out reading PDF — file may be malformed"), 200

    elapsed = _time.time() - t0
    if not anns:
        print(f"                   ⚠ no annotations found  ({elapsed:.1f}s)")
        return jsonify(ok=False, error="No annotations found in PDF"), 200

    print(f"                   ✓ {len(anns)} annotation(s) found  ({elapsed:.1f}s)")
    for a in anns:
        preview = (a['text'] or '')[:60].replace('\n', ' ')
        print(f"                   p.{a['page']} [{a['type']}] {preview!r}")

    comment = _format_annotations(anns)
    conn = get_conn()
    conn.execute("UPDATE pdf_files SET comment = ? WHERE file_id = ?",
                 (comment, file_id))
    conn.commit()
    conn.close()
    return jsonify(ok=True, count=len(anns), comment=comment)


@zsxq_bp.route("/open-local/<int:file_id>")
def open_local(file_id: int):
    """Open the PDF in the system default viewer (macOS: Preview) via 'open'."""
    conn = get_conn()
    row = conn.execute(
        "SELECT local_path, name FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        return jsonify(ok=False, error="No local file"), 404
    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error="File not found on disk"), 404
    import subprocess
    result = subprocess.run(["open", str(path)], capture_output=True, text=True)
    print(f"[open-local] open rc={result.returncode} stderr={result.stderr!r} path={path}")
    if result.returncode != 0:
        return jsonify(ok=False, error=result.stderr or "open command failed"), 200
    return jsonify(ok=True)



@zsxq_bp.route("/pdf/<int:file_id>")
@zsxq_bp.route("/pdf/<int:file_id>/<filename>")
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


# Register blueprint on the standalone app (after all routes are defined)
app.register_blueprint(zsxq_bp)


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
