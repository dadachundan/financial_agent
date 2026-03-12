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

// ── Table filtering ─────────────────────────────────────────────────────────
let activeSource     = '';
let activeMinRating  = 0;
let activeGraphType  = null, activeGraphA = null, activeGraphB = null;

function switchTab(href) {
  const el = document.querySelector('a[href="' + href + '"]');
  if (el) bootstrap.Tab.getOrCreateInstance(el).show();
}

function applyFilters() {
  // BC table
  document.querySelectorAll('#tab-bc tbody tr').forEach(row => {
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
    row.style.display = show ? '' : 'none';
  });
  // BB table
  document.querySelectorAll('#tab-bb tbody tr').forEach(row => {
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
    row.style.display = show ? '' : 'none';
  });
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

network.on('click', function(params) {
  if (params.nodes.length > 0) {
    const node  = nodes.get(params.nodes[0]);
    const label = node.label;
    const group = node.group;
    if (group === 'company') {
      filterTables('company', label, null);
      showFilterBar('Company: ' + label);
      switchTab('#tab-bc');
    } else {
      filterTables('business', label, null);
      showFilterBar('Business: ' + label);
      // Switch to whichever tab has visible rows
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
async function callMine(url, entityA, entityB, commentId, explId, errId, spinnerId) {
  const spinner = document.getElementById(spinnerId);
  const errDiv  = document.getElementById(errId);
  spinner.classList.remove("d-none");
  errDiv.textContent = "";
  try {
    const resp = await fetch("/api/summarize", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ url, entity_a: entityA, entity_b: entityB }),
    });
    const data = await resp.json();
    if (data.error) { errDiv.textContent = data.error; return; }
    document.getElementById(commentId).value = data.comment    || "";
    document.getElementById(explId).value    = data.explanation || "";
  } catch(e) {
    errDiv.textContent = "Network error: " + e.message;
  } finally {
    spinner.classList.add("d-none");
  }
}

function mineBC() {
  callMine(
    document.getElementById("bc-mine-url").value,
    document.getElementById("bc-mine-biz").value,
    document.getElementById("bc-mine-co").value,
    "bc-form-comment", "bc-form-expl", "bc-mine-err", "bc-mine-spinner"
  );
}
function mineBB() {
  callMine(
    document.getElementById("bb-mine-url").value,
    document.getElementById("bb-mine-from").value,
    document.getElementById("bb-mine-to").value,
    "bb-form-comment", "bb-form-expl", "bb-mine-err", "bb-mine-spinner"
  );
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
