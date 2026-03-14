// ── vis-network graph ──────────────────────────────────────────────────────
const graphData = window.graphData;
const nodes = new vis.DataSet(graphData.nodes);
const edges = new vis.DataSet(graphData.edges);
const network = new vis.Network(
  document.getElementById("graph"),
  { nodes, edges },
  {
    nodes: { shape:"dot", size:18, font:{size:13,face:"system-ui,sans-serif"}, borderWidth:2 },
    edges: {
      arrows: { to: {enabled:false} },
      font:   { size:10, align:"middle", color:"#666" },
      smooth: { type:"dynamic" },
    },
    physics: {
      solver:"forceAtlas2Based",
      forceAtlas2Based:{ gravitationalConstant:-50, springLength:120 },
      stabilization:{ iterations:150 },
    },
    interaction:{ hover:true, tooltipDelay:150 },
  }
);

// ── Table filtering + pagination ─────────────────────────────────────────────
const PAGE_SIZE = 20;
const _pages    = { bc: 1, bb: 1, cc: 1 };

let activeSource     = '';
let activeMinRating  = 0;
let activeGraphType  = null, activeGraphA = null, activeGraphB = null;

function switchTab(href) {
  const el = document.querySelector('a[href="' + href + '"]');
  if (el) bootstrap.Tab.getOrCreateInstance(el).show();
}

function applyFilters() {
  _filterTable('bc', row => {
    const src    = row.dataset.source || '';
    const rating = parseInt(row.dataset.rating || '0', 10);
    let show = true;
    if (activeSource)    show = show && (src === activeSource);
    if (activeMinRating) show = show && (rating >= activeMinRating);
    if (activeGraphType) {
      const biz = row.querySelector('.badge-business')?.textContent.trim();
      const co  = row.querySelector('.badge-company')?.textContent.trim();
      let g = false;
      if (activeGraphType === 'company')  g = co  === activeGraphA;
      if (activeGraphType === 'business') g = biz === activeGraphA;
      if (activeGraphType === 'bc-edge')  g = biz === activeGraphA && co === activeGraphB;
      show = show && g;
    }
    return show;
  });
  _filterTable('bb', row => {
    const src    = row.dataset.source || '';
    const rating = parseInt(row.dataset.rating || '0', 10);
    let show = true;
    if (activeSource)    show = show && (src === activeSource);
    if (activeMinRating) show = show && (rating >= activeMinRating);
    if (activeGraphType) {
      const cells = row.querySelectorAll('.badge-business');
      const from  = cells[0]?.textContent.trim();
      const to    = cells[1]?.textContent.trim();
      let g = false;
      if (activeGraphType === 'business') g = from === activeGraphA || to === activeGraphA;
      if (activeGraphType === 'bb-edge')  g = from === activeGraphA && to === activeGraphB;
      show = show && g;
    }
    return show;
  });
  _filterTable('cc', row => {
    const src    = row.dataset.source || '';
    const rating = parseInt(row.dataset.rating || '0', 10);
    let show = true;
    if (activeSource)    show = show && (src === activeSource);
    if (activeMinRating) show = show && (rating >= activeMinRating);
    if (activeGraphType) {
      const cells = row.querySelectorAll('.badge-company');
      const from  = cells[0]?.textContent.trim();
      const to    = cells[1]?.textContent.trim();
      let g = false;
      if (activeGraphType === 'company')  g = from === activeGraphA || to === activeGraphA;
      if (activeGraphType === 'cc-edge')  g = from === activeGraphA && to === activeGraphB;
      show = show && g;
    }
    return show;
  });
}

// ── Pagination helpers ────────────────────────────────────────────────────────
function _filterTable(prefix, matchFn) {
  const tbody = document.querySelector(`#tab-${prefix} tbody`);
  if (!tbody) return;
  tbody.querySelectorAll('tr').forEach(row => {
    row.dataset.match = matchFn(row) ? '1' : '0';
  });
  _pages[prefix] = 1;
  _renderPage(prefix);
  _renderPager(prefix);
}

function _renderPage(prefix) {
  const tbody = document.querySelector(`#tab-${prefix} tbody`);
  if (!tbody) return;
  const page    = _pages[prefix];
  const matched = [...tbody.querySelectorAll('tr')].filter(r => r.dataset.match === '1');
  const start   = (page - 1) * PAGE_SIZE;
  const end     = start + PAGE_SIZE;
  tbody.querySelectorAll('tr').forEach(row => {
    if (row.dataset.match !== '1') {
      row.style.display = 'none';
    } else {
      const idx = matched.indexOf(row);
      row.style.display = (idx >= start && idx < end) ? '' : 'none';
    }
  });
}

function _renderPager(prefix) {
  const pager = document.getElementById(`${prefix}-pager`);
  if (!pager) return;
  const tbody   = document.querySelector(`#tab-${prefix} tbody`);
  if (!tbody) return;
  const matched = [...tbody.querySelectorAll('tr')].filter(r => r.dataset.match === '1').length;
  const page    = _pages[prefix];
  const total   = Math.max(1, Math.ceil(matched / PAGE_SIZE));
  pager.classList.toggle('d-none', matched <= PAGE_SIZE);
  if (matched === 0) { pager.innerHTML = ''; return; }
  const start = (page - 1) * PAGE_SIZE + 1;
  const end   = Math.min(page * PAGE_SIZE, matched);
  let html = `<small class="text-muted me-2">${start}–${end} of ${matched}</small>`;
  html += `<ul class="pagination pagination-sm mb-0">`;
  html += `<li class="page-item${page === 1 ? ' disabled' : ''}">`;
  html += `<a class="page-link" href="#" onclick="_goPage('${prefix}',${page - 1});return false">‹</a></li>`;
  for (const p of _pageRange(page, total)) {
    if (p === '…') {
      html += `<li class="page-item disabled"><span class="page-link">…</span></li>`;
    } else {
      html += `<li class="page-item${p === page ? ' active' : ''}">`;
      html += `<a class="page-link" href="#" onclick="_goPage('${prefix}',${p});return false">${p}</a></li>`;
    }
  }
  html += `<li class="page-item${page === total ? ' disabled' : ''}">`;
  html += `<a class="page-link" href="#" onclick="_goPage('${prefix}',${page + 1});return false">›</a></li>`;
  html += `</ul>`;
  pager.innerHTML = html;
}

function _pageRange(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
  const set    = new Set([1, Math.max(1, current - 1), current,
                          Math.min(total, current + 1), total]);
  const sorted = [...set].sort((a, b) => a - b);
  const result = [];
  let prev = 0;
  for (const p of sorted) {
    if (p - prev > 1) result.push('…');
    result.push(p);
    prev = p;
  }
  return result;
}

function _goPage(prefix, page) {
  const tbody = document.querySelector(`#tab-${prefix} tbody`);
  if (!tbody) return;
  const matched    = [...tbody.querySelectorAll('tr')].filter(r => r.dataset.match === '1').length;
  const totalPages = Math.max(1, Math.ceil(matched / PAGE_SIZE));
  _pages[prefix]   = Math.max(1, Math.min(page, totalPages));
  _renderPage(prefix);
  _renderPager(prefix);
}

function filterTables(type, nameA, nameB) {
  activeGraphType = type; activeGraphA = nameA; activeGraphB = nameB;
  applyFilters();
}

function applySourceFilter() {
  activeSource = document.getElementById('source-select').value;
  applyFilters();
}

function applyRatingFilter() {
  activeMinRating = parseInt(document.getElementById('rating-select').value || '0', 10);
  applyFilters();
}

function rateBC(id, val, el) {
  el.closest('tr').dataset.rating = parseInt(val, 10);
  fetch('/bc/rate/' + id, {method: 'POST', body: new URLSearchParams({rating: val})});
  applyFilters();
}

function rateBB(id, val, el) {
  el.closest('tr').dataset.rating = parseInt(val, 10);
  fetch('/bb/rate/' + id, {method: 'POST', body: new URLSearchParams({rating: val})});
  applyFilters();
}

function rateCC(id, val, el) {
  el.closest('tr').dataset.rating = parseInt(val, 10);
  fetch('/cc/rate/' + id, {method: 'POST', body: new URLSearchParams({rating: val})});
  applyFilters();
}

function showFilterBar(label) {
  document.getElementById('filter-label').textContent = label;
  document.getElementById('filter-bar').classList.remove('d-none');
}

function clearFilter() {
  activeGraphType = null; activeGraphA = null; activeGraphB = null;
  applyFilters();
  document.getElementById('filter-bar').classList.add('d-none');
  network.unselectAll();
}

// Click a badge in the table → select & focus that node in the graph
function focusGraphNode(label, group) {
  const match = nodes.get({ filter: n => n.label === label && n.group === group });
  if (!match.length) return;
  const nodeId = match[0].id;
  network.selectNodes([nodeId]);
  network.focus(nodeId, { scale: 1.2, animation: { duration: 400, easingFunction: 'easeInOutQuad' } });
}

document.addEventListener('click', function(e) {
  const badge = e.target.closest('.badge-business, .badge-company');
  if (!badge) return;
  // Only act on badges inside table rows (not the legend)
  if (!badge.closest('tbody')) return;
  const label = badge.textContent.trim();
  const group = badge.classList.contains('badge-company') ? 'company' : 'business';
  focusGraphNode(label, group);
});

network.on('click', function(params) {
  if (params.nodes.length > 0) {
    const node  = nodes.get(params.nodes[0]);
    const label = node.label;
    const group = node.group;
    if (group === 'company') {
      filterTables('company', label, null);
      showFilterBar('Company: ' + label);
      // Switch to whichever tab has visible rows: bc or cc
      const bcVisible = [...document.querySelectorAll('#tab-bc tbody tr')]
                        .some(r => r.style.display !== 'none');
      switchTab(bcVisible ? '#tab-bc' : '#tab-cc');
    } else {
      filterTables('business', label, null);
      showFilterBar('Business: ' + label);
      const bcVisible = [...document.querySelectorAll('#tab-bc tbody tr')]
                        .some(r => r.style.display !== 'none');
      switchTab(bcVisible ? '#tab-bc' : '#tab-bb');
    }
  } else if (params.edges.length > 0) {
    const edge     = edges.get(params.edges[0]);
    const fromNode = nodes.get(edge.from);
    const toNode   = nodes.get(edge.to);
    if (!edge.dashes) {
      // bc edge: from=business → to=company
      filterTables('bc-edge', fromNode.label, toNode.label);
      showFilterBar(fromNode.label + ' → ' + toNode.label);
      switchTab('#tab-bc');
    } else if (fromNode.group === 'company' && toNode.group === 'company') {
      // cc edge
      filterTables('cc-edge', fromNode.label, toNode.label);
      showFilterBar(fromNode.label + ' → ' + toNode.label);
      switchTab('#tab-cc');
    } else {
      // bb edge
      filterTables('bb-edge', fromNode.label, toNode.label);
      showFilterBar(fromNode.label + ' → ' + toNode.label);
      switchTab('#tab-bb');
    }
  } else {
    clearFilter();
  }
});

// ── image lightbox ─────────────────────────────────────────────────────────
function showImg(src) {
  document.getElementById("imgModalSrc").src = src;
  new bootstrap.Modal(document.getElementById("imgModal")).show();
}

// ── AI mine helpers ────────────────────────────────────────────────────────
// setExplValue can be overridden by the inline script to redirect value
// into an EasyMDE instance rather than the raw textarea.
window.setExplValue = window.setExplValue || function(id, val) {
  document.getElementById(id).value = val;
};

async function callMine(url, entityA, entityB, commentId, explId, urlFormId, errId, spinnerId, sourceTextId) {
  const spinner = document.getElementById(spinnerId);
  const errDiv  = document.getElementById(errId);
  spinner.classList.remove("d-none");
  errDiv.innerHTML = "";
  try {
    const resp = await fetch("/api/summarize", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ url, entity_a: entityA, entity_b: entityB }),
    });
    const data = await resp.json();
    if (data.error) { errDiv.textContent = data.error; return; }
    document.getElementById(commentId).value = data.comment || "";
    window.setExplValue(explId, data.explanation || "");
    if (urlFormId) document.getElementById(urlFormId).value = url;
    if (sourceTextId) document.getElementById(sourceTextId).value = data.source_text || "";
    _showMinePrompt(errDiv, data._system_prompt, data._user_prompt, data.source_text);
  } catch(e) {
    errDiv.textContent = "Network error: " + e.message;
  } finally {
    spinner.classList.add("d-none");
  }
}

function _showMinePrompt(container, systemPrompt, userPrompt, sourceText) {
  if (!systemPrompt && !userPrompt && !sourceText) return;
  const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  let html = '';
  if (sourceText) {
    html +=
      `<details style="font-size:.75rem;margin-top:4px">` +
      `<summary style="cursor:pointer;color:#6c757d">📄 Fetched article text</summary>` +
      `<div style="background:#f6f8fa;border-radius:4px;padding:8px;margin-top:4px;` +
      `max-height:200px;overflow-y:auto;white-space:pre-wrap;word-break:break-word;font-family:monospace;color:#333">` +
      `${esc(sourceText)}</div></details>`;
  }
  if (systemPrompt || userPrompt) {
    html +=
      `<details style="font-size:.75rem;margin-top:4px">` +
      `<summary style="cursor:pointer;color:#6c757d">🔍 Prompt sent to MiniMax</summary>` +
      `<div style="background:#f6f8fa;border-radius:4px;padding:8px;margin-top:4px;` +
      `white-space:pre-wrap;word-break:break-word;font-family:monospace;color:#333">` +
      `<strong>SYSTEM:</strong>\n${esc(systemPrompt||'')}\n\n<strong>USER:</strong>\n${esc(userPrompt||'')}` +
      `</div></details>`;
  }
  container.innerHTML = html;
}

function mineBC() {
  const bizSel = document.getElementById("bc-form-biz");
  const coSel  = document.getElementById("bc-form-co");
  callMine(
    document.getElementById("bc-mine-url").value,
    bizSel.selectedOptions[0]?.text || bizSel.value,
    coSel.selectedOptions[0]?.text  || coSel.value,
    "bc-form-comment", "bc-form-expl", "bc-form-url", "bc-mine-err", "bc-mine-spinner",
    "bc-form-source-text"
  );
}
function mineBB() {
  const fromSel = document.getElementById("bb-form-from");
  const toSel   = document.getElementById("bb-form-to");
  callMine(
    document.getElementById("bb-mine-url").value,
    fromSel.selectedOptions[0]?.text || fromSel.value,
    toSel.selectedOptions[0]?.text   || toSel.value,
    "bb-form-comment", "bb-form-expl", "bb-form-url", "bb-mine-err", "bb-mine-spinner",
    "bb-form-source-text"
  );
}
function mineCC() {
  const fromSel = document.getElementById("cc-form-from");
  const toSel   = document.getElementById("cc-form-to");
  callMine(
    document.getElementById("cc-mine-url").value,
    fromSel.selectedOptions[0]?.text || fromSel.value,
    toSel.selectedOptions[0]?.text   || toSel.value,
    "cc-form-comment", "cc-form-expl", "cc-form-url", "cc-mine-err", "cc-mine-spinner",
    "cc-form-source-text"
  );
}

// ── BC row selection & compare ───────────────────────────────────────────────
function _bcUpdateSelectBar() {
  const checked = document.querySelectorAll('#tab-bc .bc-row-select:checked');
  const bar     = document.getElementById('bc-compare-bar');
  const count   = document.getElementById('bc-select-count');
  bar.classList.toggle('d-none', checked.length < 1);
  count.textContent = `${checked.length} row${checked.length === 1 ? '' : 's'} selected`;
}

document.getElementById('bc-select-all').addEventListener('change', function() {
  document.querySelectorAll('#tab-bc .bc-row-select').forEach(cb => {
    // only toggle visible rows
    if (cb.closest('tr').style.display !== 'none') cb.checked = this.checked;
  });
  _bcUpdateSelectBar();
});

document.getElementById('tab-bc').addEventListener('change', function(e) {
  if (e.target.classList.contains('bc-row-select')) _bcUpdateSelectBar();
});

function bcClearSelection() {
  document.querySelectorAll('#tab-bc .bc-row-select').forEach(cb => cb.checked = false);
  document.getElementById('bc-select-all').checked = false;
  _bcUpdateSelectBar();
}

async function compareBC() {
  const ids = [...document.querySelectorAll('#tab-bc .bc-row-select:checked')]
              .map(cb => parseInt(cb.dataset.id));
  if (ids.length < 2) {
    document.getElementById('bc-compare-err').textContent = 'Select at least 2 rows.';
    return;
  }
  const spinner = document.getElementById('bc-compare-spinner');
  const errDiv  = document.getElementById('bc-compare-err');
  spinner.classList.remove('d-none');
  errDiv.textContent = '';
  try {
    const resp = await fetch('/api/bc-compare', {
      method:  'POST',
      headers: {'Content-Type': 'application/json'},
      body:    JSON.stringify({ ids }),
    });
    const data = await resp.json();
    if (data.error) { errDiv.textContent = data.error; return; }
    document.getElementById('bcCompareBody').innerHTML = marked.parse(data.markdown || '');
    document.getElementById('bcComparePrompt').textContent = data._user_prompt || '';
    new bootstrap.Modal(document.getElementById('bcCompareModal')).show();
  } catch(e) {
    errDiv.textContent = 'Network error: ' + e.message;
  } finally {
    spinner.classList.add('d-none');
  }
}

// ── zsxq import ─────────────────────────────────────────────────────────────
async function importZsxq() {
  const spinner   = document.getElementById("zsxq-spinner");
  const errDiv    = document.getElementById("zsxq-err");
  const resultsEl = document.getElementById("zsxq-results");
  const logEl     = document.getElementById("zsxq-log");

  errDiv.textContent = "";
  resultsEl.classList.add("d-none");
  logEl.textContent  = "";
  logEl.classList.remove("d-none");
  spinner.classList.remove("d-none");

  function appendLog(msg) {
    logEl.textContent += msg + "\n";
    logEl.scrollTop = logEl.scrollHeight;
  }

  function fillList(ulId, items) {
    const ul = document.getElementById(ulId);
    ul.innerHTML = "";
    (items && items.length ? items : []).forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
    if (!items || !items.length) ul.innerHTML = "<li class='text-muted'>none</li>";
  }

  try {
    const resp = await fetch("/api/zsxq-import", { method: "POST" });
    if (!resp.ok) { errDiv.textContent = `Server error (HTTP ${resp.status})`; return; }

    const reader  = resp.body.getReader();
    const decoder = new TextDecoder();
    let   buf     = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });

      // SSE lines arrive as "data: {...}\n\n"
      const parts = buf.split("\n\n");
      buf = parts.pop();   // keep any incomplete tail

      for (const part of parts) {
        const line = part.trim();
        if (!line.startsWith("data:")) continue;
        let evt;
        try { evt = JSON.parse(line.slice(5).trim()); } catch { continue; }

        if (evt.type === "log") {
          appendLog(evt.msg);
        } else if (evt.type === "error") {
          errDiv.textContent = evt.msg;
        } else if (evt.type === "done") {
          appendLog(`\nDone. Processed ${evt.processed}, skipped ${evt.skipped}.`);
          document.getElementById("zsxq-stats").textContent =
            `Processed ${evt.processed} new rows, skipped ${evt.skipped} already-imported.`;
          fillList("zsxq-res-companies",  evt.added.companies);
          fillList("zsxq-res-businesses", evt.added.businesses);
          fillList("zsxq-res-bc",         evt.added.bc_links);
          document.getElementById("zsxq-res-errors").textContent =
            (evt.errors && evt.errors.length) ? "Warnings: " + evt.errors.join("; ") : "";
          resultsEl.classList.remove("d-none");
        }
      }
    }
  } catch(e) {
    errDiv.textContent = "Network error: " + e.message;
  } finally {
    spinner.classList.add("d-none");
  }
}

// ── PDF import ──────────────────────────────────────────────────────────────
async function importPDF() {
  const fileInput = document.getElementById("pdf-file-input");
  const spinner   = document.getElementById("pdf-spinner");
  const errDiv    = document.getElementById("pdf-err");
  const resultsEl = document.getElementById("pdf-results");

  errDiv.textContent = "";
  resultsEl.classList.add("d-none");

  if (!fileInput.files.length) {
    errDiv.textContent = "Please select a PDF file first.";
    return;
  }

  const formData = new FormData();
  formData.append("pdf", fileInput.files[0]);

  spinner.classList.remove("d-none");
  try {
    const resp = await fetch("/api/pdf-import", { method: "POST", body: formData });
    let data;
    try {
      data = await resp.json();
    } catch (_) {
      errDiv.textContent = `Server error (HTTP ${resp.status}) — check file size or server logs.`;
      return;
    }

    if (data.error) {
      errDiv.textContent = data.error;
      return;
    }

    // Populate results
    function fillList(ulId, items) {
      const ul = document.getElementById(ulId);
      ul.innerHTML = "";
      if (!items || !items.length) {
        ul.innerHTML = "<li class='text-muted'>none</li>";
        return;
      }
      items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
      });
    }

    fillList("pdf-res-companies",  data.added.companies);
    fillList("pdf-res-businesses", data.added.businesses);
    fillList("pdf-res-bc",         data.added.bc_links);

    const errEl = document.getElementById("pdf-res-errors");
    errEl.textContent = (data.errors && data.errors.length)
      ? "Warnings: " + data.errors.join("; ")
      : "";

    resultsEl.classList.remove("d-none");
  } catch(e) {
    errDiv.textContent = "Network error: " + e.message;
  } finally {
    spinner.classList.add("d-none");
  }
}

// ── Init: seed data-match + pagers on page load ─────────────────────────────
applyFilters();
