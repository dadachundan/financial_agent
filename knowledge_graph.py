#!/usr/bin/env python3
"""
knowledge_graph.py — Tech-industry knowledge graph web app.

Entity types
------------
  Company  : e.g. NVIDIA, AMD, Intel, Samsung, TSMC …
  Business : e.g. GPU, CPU, Memory, Manufacturing, TPU, Compiler …

Relationships
-------------
  business_company  : a company participates in a business
  business_business : two businesses are related

Each relationship carries:
  - comment      short one-liner
  - explanation  rich multi-paragraph text
  - image_path   optional uploaded image
  - source_url   optional news / article URL used to derive the comment

Usage
-----
    python knowledge_graph.py
    python knowledge_graph.py --db kg.db --port 5001

Then open http://localhost:5001
"""

import argparse
import json
import os
import sqlite3
import uuid
from pathlib import Path

from flask import (Flask, abort, jsonify, redirect,
                   render_template_string, request, send_from_directory, url_for)

# ── App & defaults ─────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
DEFAULT_DB  = SCRIPT_DIR / "knowledge_graph.db"
UPLOAD_DIR  = SCRIPT_DIR / "kg_uploads"
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024   # 16 MB
DB_PATH: Path = DEFAULT_DB


# ── Database helpers ───────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS companies (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            description TEXT    NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS businesses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            description TEXT    NOT NULL DEFAULT ''
        );

        -- Company participates in / focuses on a business
        CREATE TABLE IF NOT EXISTS business_company (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
            company_id  INTEGER NOT NULL REFERENCES companies(id)  ON DELETE CASCADE,
            comment     TEXT    NOT NULL DEFAULT '',
            explanation TEXT    NOT NULL DEFAULT '',
            image_path  TEXT    NOT NULL DEFAULT '',
            source_url  TEXT    NOT NULL DEFAULT '',
            UNIQUE(business_id, company_id)
        );

        -- Two businesses are related
        CREATE TABLE IF NOT EXISTS business_business (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            business_from INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
            business_to   INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
            comment       TEXT    NOT NULL DEFAULT '',
            explanation   TEXT    NOT NULL DEFAULT '',
            image_path    TEXT    NOT NULL DEFAULT '',
            source_url    TEXT    NOT NULL DEFAULT '',
            UNIQUE(business_from, business_to)
        );
        """)


def seed_db():
    """Insert example data if the tables are empty."""
    with get_db() as conn:
        if conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0] > 0:
            return

        companies = [
            ("NVIDIA",   "GPU & AI accelerator leader"),
            ("AMD",      "CPU and GPU designer"),
            ("Intel",    "CPU, GPU, and fab company"),
            ("Samsung",  "Memory, storage, and mobile chips"),
            ("TSMC",     "World's largest contract semiconductor foundry"),
            ("Micron",   "DRAM and NAND flash memory"),
            ("Qualcomm", "Mobile and edge AI processors"),
            ("Google",   "Cloud, AI, and TPU developer"),
            ("Apple",    "Custom silicon and consumer devices"),
            ("ASML",     "EUV lithography machines for chip manufacturing"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO companies (name, description) VALUES (?, ?)", companies
        )

        businesses = [
            ("GPU",            "Graphics Processing Unit — massively parallel compute"),
            ("CPU",            "Central Processing Unit — general-purpose compute"),
            ("Memory",         "DRAM / HBM / cache — high-speed data storage"),
            ("Manufacturing",  "Semiconductor fab and wafer production"),
            ("TPU",            "Tensor Processing Unit — AI/ML inference & training"),
            ("Compiler",       "Software that translates code to hardware instructions"),
            ("EUV Lithography","Extreme-UV patterning tools for advanced nodes"),
            ("Networking",     "High-speed interconnects (NVLink, InfiniBand, etc.)"),
            ("Storage",        "NAND flash, SSDs, persistent memory"),
            ("Mobile SoC",     "System-on-chip for smartphones and edge devices"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO businesses (name, description) VALUES (?, ?)", businesses
        )

        def bid(name):
            return conn.execute("SELECT id FROM businesses WHERE name=?", (name,)).fetchone()["id"]

        def cid(name):
            return conn.execute("SELECT id FROM companies WHERE name=?", (name,)).fetchone()["id"]

        bc_links = [
            ("GPU",            "NVIDIA",   "NVIDIA's core revenue driver; leads datacenter GPU market",
             "NVIDIA designs the H100/H200/B200 GPU series and dominates the AI accelerator market. Revenue from Data Center GPUs exceeded 80 % of total revenue in 2024.", ""),
            ("GPU",            "AMD",      "AMD Radeon and Instinct lines compete across gaming and AI",
             "AMD's MI300X HBM-stacked GPU targets large-language-model inference and competes directly with NVIDIA's H100.", ""),
            ("GPU",            "Intel",    "Intel Arc GPUs and Xe graphics target gaming and HPC",
             "Intel re-entered the discrete GPU market with Arc Alchemist and continues developing Xe2 for HPC and AI workloads.", ""),
            ("CPU",            "Intel",    "Intel's foundational business since 1968",
             "Intel's Core and Xeon product lines power the vast majority of PCs and servers globally, though market share has been pressured by AMD Zen architecture.", ""),
            ("CPU",            "AMD",      "AMD Ryzen and EPYC challenge Intel across desktop and server",
             "AMD's EPYC server CPUs have taken double-digit market share from Intel Xeon by offering more cores per socket at competitive pricing.", ""),
            ("CPU",            "Apple",    "Apple Silicon (M-series) integrates CPU, GPU, and NPU",
             "Apple's M-series chips use ARM cores with a unified memory architecture, delivering industry-leading performance-per-watt in laptops and desktops.", ""),
            ("CPU",            "Qualcomm", "Qualcomm Snapdragon CPU cores power mobile devices globally",
             "Qualcomm's Oryon CPU cores (acquired from Nuvia) are now shipping in Snapdragon X Elite for PC and premium Android devices.", ""),
            ("Memory",         "Samsung",  "Samsung is the world's largest DRAM and NAND producer",
             "Samsung supplies HBM3e to NVIDIA and SK Hynix competes alongside it; Samsung also manufactures its own NAND for enterprise SSDs.", ""),
            ("Memory",         "Micron",   "Micron supplies DRAM, HBM, and NAND to hyperscalers",
             "Micron's HBM3e is qualified for NVIDIA H200 and GB200, making it a critical memory supplier for AI infrastructure build-outs.", ""),
            ("Manufacturing",  "TSMC",     "TSMC manufactures chips for Apple, NVIDIA, AMD, and others",
             "TSMC's N3 (3 nm) and N2 (2 nm) processes represent the global frontier; all leading AI chips are fabbed there.", ""),
            ("Manufacturing",  "Samsung",  "Samsung Foundry competes with TSMC on leading-edge nodes",
             "Samsung Foundry's SF3 (3 nm GAA) process targets high-performance mobile and server chips in competition with TSMC N3.", ""),
            ("Manufacturing",  "Intel",    "Intel Foundry Services (IFS) aims to regain process leadership",
             "Intel 18A (1.8 nm class) uses RibbonFET and PowerVia backside power delivery; Microsoft and others are sampling it in 2025.", ""),
            ("TPU",            "Google",   "Google TPUs power Search, Translate, and Vertex AI",
             "Google Trillium (TPU v6) delivers 4.7× the compute of TPU v5e and runs Gemini model training and inference at hyperscale.", ""),
            ("Compiler",       "NVIDIA",   "NVCC and cuDNN/TensorRT compile CUDA and AI workloads",
             "The CUDA toolchain — NVCC, cuDNN, TensorRT, and Triton — forms the dominant software stack for GPU-based AI workloads.", ""),
            ("Compiler",       "Google",   "XLA compiler optimises TPU and GPU workloads for ML",
             "XLA (Accelerated Linear Algebra) powers JAX and TensorFlow, and is now used by PyTorch/XLA to target both TPU and GPU.", ""),
            ("EUV Lithography","ASML",     "ASML holds a monopoly on EUV scanners used at sub-5 nm nodes",
             "ASML's High-NA EUV (EXE:5000) enables sub-2 nm patterning; delivery to TSMC and Intel began in 2024 for N2/18A processes.", ""),
            ("Networking",     "NVIDIA",   "NVIDIA InfiniBand and NVLink connect GPUs in AI clusters",
             "NVIDIA's acquisition of Mellanox gave it InfiniBand; combined with NVLink 5 in Blackwell, it controls both intra- and inter-node GPU networking.", ""),
            ("Storage",        "Samsung",  "Samsung supplies SSDs and flash to OEMs worldwide",
             "Samsung 990 Pro NVMe SSDs and QLC V-NAND are widely deployed in AI storage pipelines and consumer devices.", ""),
            ("Storage",        "Micron",   "Micron NAND underpins enterprise and consumer SSDs",
             "Micron's 232-layer NAND enables high-density enterprise SSDs used in AI training data lakes.", ""),
            ("Mobile SoC",     "Qualcomm", "Snapdragon SoCs are in the majority of Android flagships",
             "Snapdragon 8 Elite integrates Oryon CPU, Adreno GPU, and Hexagon NPU delivering on-device AI at sub-10W.", ""),
            ("Mobile SoC",     "Apple",    "Apple A-series chips set performance benchmarks for mobile",
             "Apple A18 Pro (3 nm) powers iPhone 16 Pro with a 16-core Neural Engine capable of 35 TOPS for on-device AI.", ""),
        ]
        for bname, cname, comment, explanation, _ in bc_links:
            conn.execute(
                """INSERT OR IGNORE INTO business_company
                   (business_id, company_id, comment, explanation)
                   VALUES (?,?,?,?)""",
                (bid(bname), cid(cname), comment, explanation),
            )

        bb_links = [
            ("GPU",            "Memory",         "GPUs require high-bandwidth memory (HBM) to feed thousands of cores",
             "H100 uses HBM3 with 3.35 TB/s bandwidth; without that memory bandwidth the GPU compute units would stall waiting for data."),
            ("GPU",            "Networking",     "Multi-GPU clusters need fast interconnects (NVLink/InfiniBand)",
             "Training large models requires all-reduce operations across hundreds of GPUs; NVLink 5 offers 1.8 TB/s bidirectional bandwidth per GPU."),
            ("GPU",            "Compiler",       "CUDA / ROCm compilers translate AI workloads to GPU instructions",
             "NVCC and the Triton compiler lower Python-level tensor operations into PTX and SASS assembly that the GPU executes."),
            ("TPU",            "Compiler",       "XLA and MLIR compilers are essential to program TPU hardware",
             "TPUs have no native C++ API; all computation must go through XLA's HLO IR, making the compiler a first-class citizen of TPU programming."),
            ("TPU",            "Memory",         "TPUs embed HBM for high-throughput tensor operations",
             "TPU v5p uses HBM2e at 459 GB/s per chip; this bandwidth is critical for matrix-multiply operations during transformer model training."),
            ("CPU",            "Memory",         "CPUs depend on DRAM and cache hierarchy for instruction throughput",
             "Modern CPUs stall for hundreds of cycles on a DRAM access (>100 ns); multi-level caches (L1/L2/L3) hide this latency to keep cores fed."),
            ("CPU",            "Compiler",       "LLVM / GCC compilers generate optimised CPU machine code",
             "Auto-vectorisation in LLVM maps loop bodies to AVX-512 SIMD instructions, multiplying throughput without code changes."),
            ("Manufacturing",  "EUV Lithography","Advanced semiconductor nodes require ASML EUV scanners",
             "Patterns at 5 nm and below require multiple EUV exposures; High-NA EUV reduces the number of multi-patterning steps needed for 2 nm."),
            ("Memory",         "Storage",        "DRAM (volatile) and NAND (non-volatile) together form the memory hierarchy",
             "The memory-storage hierarchy: registers → L1/L2/L3 cache → DRAM → NVMe SSD. Moving data between DRAM and NVMe incurs a 10–100× latency penalty."),
            ("Mobile SoC",     "CPU",            "Mobile SoCs integrate CPU cores (often ARM-based) on the same die",
             "Snapdragon 8 Elite packages Oryon CPU cores, Adreno GPU, Hexagon DSP, and 5G modem on a single TSMC 3 nm die."),
            ("Mobile SoC",     "GPU",            "Mobile SoCs include integrated GPU for graphics and ML acceleration",
             "Adreno 830 inside Snapdragon 8 Elite doubles AI performance versus Adreno 750, enabling real-time generative AI on device."),
            ("GPU",            "Manufacturing",  "Leading GPU dies are fabbed at TSMC/Samsung advanced nodes",
             "NVIDIA's GB100 Blackwell die is fabbed at TSMC N4P; the die area exceeds 800 mm² requiring CoWoS-L advanced packaging."),
            ("CPU",            "Manufacturing",  "High-performance CPUs require cutting-edge fabs for smaller transistors",
             "Intel Lunar Lake uses TSMC N3 for compute tiles; AMD Zen 5 CCDs are also fabbed at TSMC N4 for density and efficiency."),
            ("EUV Lithography","Memory",         "DRAM scaling beyond 1z nm requires EUV patterning",
             "Samsung and SK Hynix have adopted EUV for DRAM at 1z and 1a nm nodes to achieve the cell density needed for HBM stacking."),
        ]
        for bfrom, bto, comment, explanation in bb_links:
            conn.execute(
                """INSERT OR IGNORE INTO business_business
                   (business_from, business_to, comment, explanation)
                   VALUES (?,?,?,?)""",
                (bid(bfrom), bid(bto), comment, explanation),
            )


# ── File upload helper ─────────────────────────────────────────────────────────

def save_upload(file_field):
    """Save an uploaded file; return relative path or '' if none."""
    f = request.files.get(file_field)
    if not f or not f.filename:
        return ""
    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return ""
    fname = uuid.uuid4().hex + ext
    f.save(UPLOAD_DIR / fname)
    return fname


# ── LLM summarisation endpoint ─────────────────────────────────────────────────

@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """
    POST JSON { "url": "...", "entity_a": "...", "entity_b": "...", "rel_type": "bc"|"bb" }
    Returns   { "comment": "...", "explanation": "..." }

    Uses MiniMax to read the web page and derive a concise relationship summary.
    Falls back gracefully if the API key is missing.
    """
    import re, urllib.request, urllib.error
    from minimax import call_minimax, MINIMAX_API_KEY

    data = request.get_json(force=True)
    url      = (data.get("url")      or "").strip()
    entity_a = (data.get("entity_a") or "").strip()
    entity_b = (data.get("entity_b") or "").strip()

    if not url or not entity_a or not entity_b:
        return jsonify({"error": "url, entity_a and entity_b are required"}), 400

    # 1) Fetch the page text
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(200_000).decode("utf-8", errors="replace")
    except Exception as exc:
        return jsonify({"error": f"Could not fetch URL: {exc}"}), 502

    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()[:8000]

    # 2) Call MiniMax
    if not MINIMAX_API_KEY:
        return jsonify({
            "comment":     f"[API key missing] Relationship between {entity_a} and {entity_b}",
            "explanation": text[:400],
        })

    system_prompt = (
        "You are analysing a web article about the semiconductor / tech industry. "
        "Given article text and two entities, return a JSON object with exactly two keys: "
        "\"comment\" (one sentence ≤ 20 words summarising the relationship) and "
        "\"explanation\" (two to four sentences with detail, citing specific facts). "
        "Return only valid JSON, no markdown fences."
    )
    user_msg = (
        f"Article text (truncated):\n\"\"\"\n{text}\n\"\"\"\n\n"
        f"Describe the relationship between \"{entity_a}\" and \"{entity_b}\" "
        "based ONLY on the article above."
    )

    try:
        reply, _elapsed, _raw = call_minimax(
            messages=[
                {"role": "system", "name": "MiniMax AI", "content": system_prompt},
                {"role": "user",   "name": "User",       "content": user_msg},
            ],
            temperature=0.2,
            max_completion_tokens=512,
        )
        result = json.loads(reply.strip())
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"LLM error: {exc}"}), 500


# ── Graph JSON builder ─────────────────────────────────────────────────────────

def build_graph_json(conn):
    nodes, edges = [], []
    for row in conn.execute("SELECT id, name, description FROM companies"):
        nodes.append({
            "id":    f"c{row['id']}",
            "label": row["name"],
            "title": row["description"],
            "color": {"background": "#0d6efd", "border": "#084298"},
            "font":  {"color": "#084298"},
            "group": "company",
        })
    for row in conn.execute("SELECT id, name, description FROM businesses"):
        nodes.append({
            "id":    f"b{row['id']}",
            "label": row["name"],
            "title": row["description"],
            "color": {"background": "#fd7e14", "border": "#a04c00"},
            "font":  {"color": "#a04c00"},
            "group": "business",
        })
    for row in conn.execute(
            "SELECT business_id, company_id, comment FROM business_company"):
        edges.append({
            "from":   f"b{row['business_id']}",
            "to":     f"c{row['company_id']}",
            "title":  row["comment"],
            "color":  {"color": "#6c757d", "highlight": "#0d6efd"},
            "dashes": False,
        })
    for row in conn.execute(
            "SELECT business_from, business_to, comment FROM business_business"):
        edges.append({
            "from":   f"b{row['business_from']}",
            "to":     f"b{row['business_to']}",
            "title":  row["comment"],
            "color":  {"color": "#e64545", "highlight": "#e64545"},
            "dashes": True,
        })
    return json.dumps({"nodes": nodes, "edges": edges})


# ── Main page renderer ─────────────────────────────────────────────────────────

def render_main(active_tab="bc"):
    conn = get_db()
    companies  = conn.execute("SELECT * FROM companies  ORDER BY name").fetchall()
    businesses = conn.execute("SELECT * FROM businesses ORDER BY name").fetchall()
    bc_links = conn.execute("""
        SELECT bc.id, b.name AS business_name, c.name AS company_name,
               bc.comment, bc.explanation, bc.image_path, bc.source_url
        FROM business_company bc
        JOIN businesses b ON b.id = bc.business_id
        JOIN companies  c ON c.id = bc.company_id
        ORDER BY b.name, c.name
    """).fetchall()
    bb_links = conn.execute("""
        SELECT bb.id, bf.name AS from_name, bt.name AS to_name,
               bb.comment, bb.explanation, bb.image_path, bb.source_url
        FROM business_business bb
        JOIN businesses bf ON bf.id = bb.business_from
        JOIN businesses bt ON bt.id = bb.business_to
        ORDER BY bf.name, bt.name
    """).fetchall()
    graph_json = build_graph_json(conn)
    conn.close()
    return render_template_string(
        TEMPLATE,
        companies=companies,
        businesses=businesses,
        bc_links=bc_links,
        bb_links=bb_links,
        graph_json=graph_json,
        active_tab=active_tab,
    )


# ── HTML template ──────────────────────────────────────────────────────────────

TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tech Knowledge Graph</title>
  <link href="/static/bootstrap.min.css" rel="stylesheet">
  <script src="/static/vis-network.min.js"></script>
  <style>
    body { background:#f0f2f5; padding:20px 16px; }
    h2   { font-weight:700; }

    #graph-container {
      width:100%; height:520px; background:#fff;
      border:1px solid #dee2e6; border-radius:8px;
      margin-bottom:24px; position:relative;
    }
    #graph { width:100%; height:100%; }
    #legend {
      position:absolute; top:12px; right:12px;
      background:rgba(255,255,255,.92); border:1px solid #ccc;
      border-radius:6px; padding:8px 12px; font-size:.78rem; line-height:2;
    }
    .dot { display:inline-block; width:12px; height:12px;
           border-radius:50%; margin-right:5px; vertical-align:middle; }

    .table { background:#fff; font-size:.82rem; }
    th { white-space:nowrap; }
    td { vertical-align:middle; }
    .comment-col { max-width:280px; }
    .expl-col    { max-width:320px; font-size:.78rem; color:#555; }
    .img-thumb   { max-height:60px; max-width:90px; border-radius:4px; cursor:pointer; }

    .nav-tabs .nav-link { font-size:.88rem; }
    .tab-content {
      background:#fff; border:1px solid #dee2e6;
      border-top:none; border-radius:0 0 8px 8px;
      padding:20px; margin-bottom:24px;
    }

    .badge-company  { background:#0d6efd; color:#fff; padding:3px 7px; border-radius:4px; font-size:.78rem; }
    .badge-business { background:#fd7e14; color:#fff; padding:3px 7px; border-radius:4px; font-size:.78rem; }

    /* mine-from-url panel */
    .mine-panel {
      background:#f8f9fa; border:1px solid #dee2e6;
      border-radius:6px; padding:12px 16px; margin-bottom:16px;
    }
    .mine-panel h6 { font-size:.82rem; margin-bottom:8px; }

    /* modal image */
    #imgModal img { max-width:100%; }
  </style>
</head>
<body>
<div class="container-fluid" style="max-width:1260px">

  <h2 class="mb-1">Tech Industry Knowledge Graph</h2>
  <p class="text-muted mb-3" style="font-size:.85rem">
    <span class="badge-company">Company</span> connect to businesses &nbsp;|&nbsp;
    <span class="badge-business">Business</span> can connect to each other &nbsp;|&nbsp;
    Hover edges for comments &nbsp;|&nbsp; Click nodes to filter
  </p>

  <!-- ── Graph ── -->
  <div id="graph-container">
    <div id="graph"></div>
    <div id="legend">
      <span class="dot" style="background:#0d6efd"></span>Company<br>
      <span class="dot" style="background:#fd7e14"></span>Business<br>
      <span style="border-bottom:2px solid #888;display:inline-block;width:20px;margin-right:5px;vertical-align:middle"></span>Biz → Company<br>
      <span style="border-bottom:2px dashed #e64545;display:inline-block;width:20px;margin-right:5px;vertical-align:middle"></span>Biz → Biz
    </div>
  </div>

  <!-- ── Tabs ── -->
  <ul class="nav nav-tabs" id="mainTab">
    <li class="nav-item">
      <a class="nav-link {% if active_tab=='bc' %}active{% endif %}" data-bs-toggle="tab" href="#tab-bc">
        Business → Company
      </a>
    </li>
    <li class="nav-item">
      <a class="nav-link {% if active_tab=='bb' %}active{% endif %}" data-bs-toggle="tab" href="#tab-bb">
        Business → Business
      </a>
    </li>
    <li class="nav-item">
      <a class="nav-link {% if active_tab=='entities' %}active{% endif %}" data-bs-toggle="tab" href="#tab-entities">
        Manage Entities
      </a>
    </li>
  </ul>

  <div class="tab-content">

    <!-- ══ Tab: Business ↔ Company ══ -->
    <div class="tab-pane fade {% if active_tab=='bc' %}show active{% endif %}" id="tab-bc">
      <h5>Business → Company relationships</h5>

      <!-- Mine from URL -->
      <div class="mine-panel">
        <h6>🔍 Mine from web news (optional)</h6>
        <div class="row g-2 align-items-end">
          <div class="col-3">
            <label class="form-label mb-1" style="font-size:.78rem">News article URL</label>
            <input id="bc-mine-url" class="form-control form-control-sm" placeholder="https://…">
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Business</label>
            <select id="bc-mine-biz" class="form-select form-select-sm">
              {% for b in businesses %}<option value="{{b.name}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Company</label>
            <select id="bc-mine-co" class="form-select form-select-sm">
              {% for c in companies %}<option value="{{c.name}}">{{c.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <button class="btn btn-sm btn-secondary" onclick="mineBC()">
              <span id="bc-mine-spinner" class="spinner-border spinner-border-sm d-none"></span>
              Summarise with AI
            </button>
          </div>
          <div class="col-auto text-danger small" id="bc-mine-err"></div>
        </div>
      </div>

      <!-- Add form -->
      <form method="post" action="/bc/add" enctype="multipart/form-data"
            class="border rounded p-3 mb-3" style="background:#fafafa">
        <div class="row g-2 mb-2">
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Business</label>
            <select name="business_id" id="bc-form-biz" class="form-select form-select-sm" required>
              {% for b in businesses %}<option value="{{b.id}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Company</label>
            <select name="company_id" id="bc-form-co" class="form-select form-select-sm" required>
              {% for c in companies %}<option value="{{c.id}}">{{c.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-4">
            <label class="form-label mb-1" style="font-size:.78rem">Short comment <span class="text-danger">*</span></label>
            <input name="comment" id="bc-form-comment" class="form-control form-control-sm"
                   placeholder="One-liner summary" required>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Source URL (optional)</label>
            <input name="source_url" id="bc-form-url" class="form-control form-control-sm"
                   placeholder="https://…">
          </div>
        </div>
        <div class="row g-2 align-items-end">
          <div class="col-6">
            <label class="form-label mb-1" style="font-size:.78rem">Detailed explanation (optional)</label>
            <textarea name="explanation" id="bc-form-expl" class="form-control form-control-sm"
                      rows="3" placeholder="Multi-paragraph detail…"></textarea>
          </div>
          <div class="col-3">
            <label class="form-label mb-1" style="font-size:.78rem">Image (optional, ≤16 MB)</label>
            <input type="file" name="image" class="form-control form-control-sm"
                   accept=".png,.jpg,.jpeg,.gif,.webp,.svg">
          </div>
          <div class="col-auto">
            <button class="btn btn-sm btn-primary">Add link</button>
          </div>
        </div>
      </form>

      <!-- Table -->
      <div class="table-responsive">
        <table class="table table-bordered table-hover table-sm">
          <thead class="table-light">
            <tr>
              <th>Business</th><th>Company</th>
              <th class="comment-col">Comment</th>
              <th class="expl-col">Explanation</th>
              <th>Image</th><th>Source</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
          {% for r in bc_links %}
          <tr>
            <td><span class="badge-business">{{r.business_name}}</span></td>
            <td><span class="badge-company">{{r.company_name}}</span></td>
            <td class="comment-col">{{r.comment}}</td>
            <td class="expl-col">{{r.explanation[:120] if r.explanation else '—'}}{% if r.explanation|length > 120 %}…{% endif %}</td>
            <td>
              {% if r.image_path %}
              <img src="/uploads/{{r.image_path}}" class="img-thumb"
                   onclick="showImg('/uploads/{{r.image_path}}')" title="Click to enlarge">
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.source_url %}
              <a href="{{r.source_url}}" target="_blank" style="font-size:.75rem">link</a>
              {% else %}—{% endif %}
            </td>
            <td>
              <form method="post" action="/bc/delete/{{r.id}}" style="display:inline">
                <button class="btn btn-sm btn-outline-danger">✕</button>
              </form>
            </td>
          </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
    </div><!-- /tab-bc -->

    <!-- ══ Tab: Business ↔ Business ══ -->
    <div class="tab-pane fade {% if active_tab=='bb' %}show active{% endif %}" id="tab-bb">
      <h5>Business → Business relationships</h5>

      <!-- Mine from URL -->
      <div class="mine-panel">
        <h6>🔍 Mine from web news (optional)</h6>
        <div class="row g-2 align-items-end">
          <div class="col-3">
            <label class="form-label mb-1" style="font-size:.78rem">News article URL</label>
            <input id="bb-mine-url" class="form-control form-control-sm" placeholder="https://…">
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">From Business</label>
            <select id="bb-mine-from" class="form-select form-select-sm">
              {% for b in businesses %}<option value="{{b.name}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">To Business</label>
            <select id="bb-mine-to" class="form-select form-select-sm">
              {% for b in businesses %}<option value="{{b.name}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <button class="btn btn-sm btn-secondary" onclick="mineBB()">
              <span id="bb-mine-spinner" class="spinner-border spinner-border-sm d-none"></span>
              Summarise with AI
            </button>
          </div>
          <div class="col-auto text-danger small" id="bb-mine-err"></div>
        </div>
      </div>

      <!-- Add form -->
      <form method="post" action="/bb/add" enctype="multipart/form-data"
            class="border rounded p-3 mb-3" style="background:#fafafa">
        <div class="row g-2 mb-2">
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">From Business</label>
            <select name="business_from" id="bb-form-from" class="form-select form-select-sm" required>
              {% for b in businesses %}<option value="{{b.id}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">To Business</label>
            <select name="business_to" id="bb-form-to" class="form-select form-select-sm" required>
              {% for b in businesses %}<option value="{{b.id}}">{{b.name}}</option>{% endfor %}
            </select>
          </div>
          <div class="col-4">
            <label class="form-label mb-1" style="font-size:.78rem">Short comment <span class="text-danger">*</span></label>
            <input name="comment" id="bb-form-comment" class="form-control form-control-sm"
                   placeholder="One-liner summary" required>
          </div>
          <div class="col-auto">
            <label class="form-label mb-1" style="font-size:.78rem">Source URL (optional)</label>
            <input name="source_url" id="bb-form-url" class="form-control form-control-sm"
                   placeholder="https://…">
          </div>
        </div>
        <div class="row g-2 align-items-end">
          <div class="col-6">
            <label class="form-label mb-1" style="font-size:.78rem">Detailed explanation (optional)</label>
            <textarea name="explanation" id="bb-form-expl" class="form-control form-control-sm"
                      rows="3" placeholder="Multi-paragraph detail…"></textarea>
          </div>
          <div class="col-3">
            <label class="form-label mb-1" style="font-size:.78rem">Image (optional, ≤16 MB)</label>
            <input type="file" name="image" class="form-control form-control-sm"
                   accept=".png,.jpg,.jpeg,.gif,.webp,.svg">
          </div>
          <div class="col-auto">
            <button class="btn btn-sm btn-primary">Add link</button>
          </div>
        </div>
      </form>

      <!-- Table -->
      <div class="table-responsive">
        <table class="table table-bordered table-hover table-sm">
          <thead class="table-light">
            <tr>
              <th>From</th><th>To</th>
              <th class="comment-col">Comment</th>
              <th class="expl-col">Explanation</th>
              <th>Image</th><th>Source</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
          {% for r in bb_links %}
          <tr>
            <td><span class="badge-business">{{r.from_name}}</span></td>
            <td><span class="badge-business">{{r.to_name}}</span></td>
            <td class="comment-col">{{r.comment}}</td>
            <td class="expl-col">{{r.explanation[:120] if r.explanation else '—'}}{% if r.explanation|length > 120 %}…{% endif %}</td>
            <td>
              {% if r.image_path %}
              <img src="/uploads/{{r.image_path}}" class="img-thumb"
                   onclick="showImg('/uploads/{{r.image_path}}')" title="Click to enlarge">
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.source_url %}
              <a href="{{r.source_url}}" target="_blank" style="font-size:.75rem">link</a>
              {% else %}—{% endif %}
            </td>
            <td>
              <form method="post" action="/bb/delete/{{r.id}}" style="display:inline">
                <button class="btn btn-sm btn-outline-danger">✕</button>
              </form>
            </td>
          </tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
    </div><!-- /tab-bb -->

    <!-- ══ Tab: Manage Entities ══ -->
    <div class="tab-pane fade {% if active_tab=='entities' %}show active{% endif %}" id="tab-entities">
      <div class="row">

        <!-- Companies -->
        <div class="col-md-6">
          <h5>Companies</h5>
          <form method="post" action="/company/add" class="row g-2 mb-3">
            <div class="col-5">
              <input name="name" class="form-control form-control-sm" placeholder="Name" required>
            </div>
            <div class="col-5">
              <input name="description" class="form-control form-control-sm" placeholder="Description">
            </div>
            <div class="col-auto">
              <button class="btn btn-sm btn-outline-primary">Add</button>
            </div>
          </form>
          <table class="table table-bordered table-sm">
            <thead class="table-light"><tr><th>Name</th><th>Description</th><th></th></tr></thead>
            <tbody>
            {% for c in companies %}
            <tr>
              <td><strong>{{c.name}}</strong></td>
              <td style="color:#555;font-size:.8rem">{{c.description}}</td>
              <td>
                <form method="post" action="/company/delete/{{c.id}}" style="display:inline">
                  <button class="btn btn-sm btn-outline-danger">✕</button>
                </form>
              </td>
            </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>

        <!-- Businesses -->
        <div class="col-md-6">
          <h5>Businesses / Domains</h5>
          <form method="post" action="/business/add" class="row g-2 mb-3">
            <div class="col-5">
              <input name="name" class="form-control form-control-sm" placeholder="Name" required>
            </div>
            <div class="col-5">
              <input name="description" class="form-control form-control-sm" placeholder="Description">
            </div>
            <div class="col-auto">
              <button class="btn btn-sm btn-outline-warning">Add</button>
            </div>
          </form>
          <table class="table table-bordered table-sm">
            <thead class="table-light"><tr><th>Name</th><th>Description</th><th></th></tr></thead>
            <tbody>
            {% for b in businesses %}
            <tr>
              <td><strong>{{b.name}}</strong></td>
              <td style="color:#555;font-size:.8rem">{{b.description}}</td>
              <td>
                <form method="post" action="/business/delete/{{b.id}}" style="display:inline">
                  <button class="btn btn-sm btn-outline-danger">✕</button>
                </form>
              </td>
            </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>

      </div>
    </div><!-- /tab-entities -->
  </div><!-- /tab-content -->
</div><!-- /container -->

<!-- Image lightbox modal -->
<div class="modal fade" id="imgModal" tabindex="-1">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-body text-center p-2">
        <img id="imgModalSrc" src="" alt="Image">
      </div>
    </div>
  </div>
</div>

<script src="/static/bootstrap.bundle.min.js"></script>
<script>
// ── vis-network graph ──────────────────────────────────────────────────────
const graphData = {{ graph_json | safe }};
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

// ── image lightbox ─────────────────────────────────────────────────────────
function showImg(src) {
  document.getElementById("imgModalSrc").src = src;
  new bootstrap.Modal(document.getElementById("imgModal")).show();
}

// ── AI mine helpers ────────────────────────────────────────────────────────
function nameToId(selectEl, nameMap) {
  return selectEl.value;   // bc/bb selects already bind to name strings
}

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
</script>
</body>
</html>
"""


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_main()


@app.route("/uploads/<path:fname>")
def serve_upload(fname):
    return send_from_directory(UPLOAD_DIR, fname)


# Company CRUD
@app.route("/company/add", methods=["POST"])
def company_add():
    name = request.form["name"].strip()
    desc = request.form.get("description", "").strip()
    if name:
        with get_db() as conn:
            conn.execute("INSERT OR IGNORE INTO companies (name, description) VALUES (?,?)", (name, desc))
    return redirect(url_for("index") + "#tab-entities")


@app.route("/company/delete/<int:cid>", methods=["POST"])
def company_delete(cid):
    with get_db() as conn:
        conn.execute("DELETE FROM companies WHERE id=?", (cid,))
    return redirect(url_for("index") + "#tab-entities")


# Business CRUD
@app.route("/business/add", methods=["POST"])
def business_add():
    name = request.form["name"].strip()
    desc = request.form.get("description", "").strip()
    if name:
        with get_db() as conn:
            conn.execute("INSERT OR IGNORE INTO businesses (name, description) VALUES (?,?)", (name, desc))
    return redirect(url_for("index") + "#tab-entities")


@app.route("/business/delete/<int:bid>", methods=["POST"])
def business_delete(bid):
    with get_db() as conn:
        conn.execute("DELETE FROM businesses WHERE id=?", (bid,))
    return redirect(url_for("index") + "#tab-entities")


# Business ↔ Company CRUD
@app.route("/bc/add", methods=["POST"])
def bc_add():
    business_id = int(request.form["business_id"])
    company_id  = int(request.form["company_id"])
    comment     = request.form.get("comment", "").strip()
    explanation = request.form.get("explanation", "").strip()
    source_url  = request.form.get("source_url", "").strip()
    image_path  = save_upload("image")
    with get_db() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO business_company
               (business_id, company_id, comment, explanation, image_path, source_url)
               VALUES (?,?,?,?,?,?)""",
            (business_id, company_id, comment, explanation, image_path, source_url),
        )
    return redirect(url_for("index"))


@app.route("/bc/delete/<int:rid>", methods=["POST"])
def bc_delete(rid):
    with get_db() as conn:
        row = conn.execute("SELECT image_path FROM business_company WHERE id=?", (rid,)).fetchone()
        if row and row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_company WHERE id=?", (rid,))
    return redirect(url_for("index"))


# Business ↔ Business CRUD
@app.route("/bb/add", methods=["POST"])
def bb_add():
    bfrom       = int(request.form["business_from"])
    bto         = int(request.form["business_to"])
    comment     = request.form.get("comment", "").strip()
    explanation = request.form.get("explanation", "").strip()
    source_url  = request.form.get("source_url", "").strip()
    image_path  = save_upload("image")
    with get_db() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO business_business
               (business_from, business_to, comment, explanation, image_path, source_url)
               VALUES (?,?,?,?,?,?)""",
            (bfrom, bto, comment, explanation, image_path, source_url),
        )
    return redirect(url_for("index") + "#tab-bb")


@app.route("/bb/delete/<int:rid>", methods=["POST"])
def bb_delete(rid):
    with get_db() as conn:
        row = conn.execute("SELECT image_path FROM business_business WHERE id=?", (rid,)).fetchone()
        if row and row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_business WHERE id=?", (rid,))
    return redirect(url_for("index") + "#tab-bb")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    global DB_PATH
    parser = argparse.ArgumentParser(description="Tech knowledge-graph web app")
    parser.add_argument("--db",   default=str(DEFAULT_DB), help="SQLite DB path")
    parser.add_argument("--port", type=int, default=5001,  help="HTTP port (default 5001)")
    parser.add_argument("--host", default="0.0.0.0",       help="Bind host")
    args = parser.parse_args()
    DB_PATH = Path(args.db)

    init_db()
    seed_db()
    print(f"Knowledge graph running at http://localhost:{args.port}")
    from minimax import MINIMAX_API_KEY
    key_status = "set" if MINIMAX_API_KEY else "missing — add MINIMAX_API_KEY to config.py"
    print(f"MiniMax API key: {key_status}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
