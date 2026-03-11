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
ALLOWED_EXT     = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
ALLOWED_PDF_EXT = {".pdf"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024   # 50 MB
DB_PATH: Path = DEFAULT_DB


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "File too large (max 50 MB)"}), 413


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
        result["prompt"] = {"system": system_prompt, "user": user_msg}
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"LLM error: {exc}"}), 500


# ── PDF import endpoint ────────────────────────────────────────────────────────

@app.route("/api/pdf-import", methods=["POST"])
def api_pdf_import():
    """
    POST multipart { "pdf": <file> }
    Extracts text from first 3 pages, asks MiniMax to identify companies
    (with tickers) and businesses, then upserts entities + relationships into DB.
    Returns { "added": { "companies": [...], "businesses": [...], "bc_links": [...] },
              "errors": [...] }
    """
    import io
    import pdfplumber
    from minimax import call_minimax, MINIMAX_API_KEY

    pdf_file = request.files.get("pdf")
    if not pdf_file or not pdf_file.filename:
        return jsonify({"error": "No PDF file provided"}), 400
    if Path(pdf_file.filename).suffix.lower() not in ALLOWED_PDF_EXT:
        return jsonify({"error": "Only .pdf files are accepted"}), 400

    # 1) Extract text from first 3 pages and persist the PDF
    try:
        pdf_bytes = pdf_file.read()
        pages_text = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages[:3]:
                t = page.extract_text() or ""
                pages_text.append(t.strip())
        raw_text = "\n\n".join(pages_text).strip()
    except Exception as exc:
        return jsonify({"error": f"PDF extraction failed: {exc}"}), 500

    if not raw_text:
        return jsonify({"error": "No text could be extracted from the PDF"}), 422

    # Save the PDF so the source link works later
    safe_stem = Path(pdf_file.filename).stem[:60]  # keep original name prefix
    pdf_fname = f"{uuid.uuid4().hex}_{safe_stem}.pdf"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    (UPLOAD_DIR / pdf_fname).write_bytes(pdf_bytes)
    pdf_source_url = f"/uploads/{pdf_fname}"

    # 2) Call MiniMax
    if not MINIMAX_API_KEY:
        return jsonify({"error": "MINIMAX_API_KEY not configured"}), 503

    system_prompt = (
        "You are a financial-document analyser specialising in the tech/semiconductor industry. "
        "Given document text, extract:\n"
        "  1. Companies mentioned — prefer ticker symbols (e.g. NVDA, AMD, TSMC); "
        "     if a ticker is not obvious, use the company name.\n"
        "  2. Business domains / verticals each company operates in "
        "(e.g. GPU, CPU, Memory, Manufacturing, Cloud, AI, Networking, Storage, Mobile SoC, EUV Lithography, etc.).\n\n"
        "Return ONLY valid JSON with this exact structure (no markdown fences):\n"
        "{\n"
        '  "companies": [{"ticker": "NVDA", "name": "NVIDIA", "description": "..."}],\n'
        '  "businesses": [{"name": "GPU", "description": "..."}],\n'
        '  "relationships": [{"company_ticker": "NVDA", "business": "GPU", "comment": "one-liner"}]\n'
        "}"
    )
    user_msg = (
        f"Document text (first 3 pages):\n\"\"\"\n{raw_text[:6000]}\n\"\"\"\n\n"
        "Extract companies, businesses, and their relationships as JSON."
    )

    print("\n" + "="*60)
    print("PDF IMPORT — MiniMax prompt")
    print("="*60)
    print("[SYSTEM]", system_prompt)
    print("[USER]",   user_msg)
    print("="*60 + "\n")

    try:
        reply, _elapsed, _raw = call_minimax(
            messages=[
                {"role": "system", "name": "MiniMax AI", "content": system_prompt},
                {"role": "user",   "name": "User",       "content": user_msg},
            ],
            temperature=0.1,
            max_completion_tokens=1024,
        )
        print("PDF IMPORT — MiniMax reply:", reply[:500])
        # Strip optional markdown fences
        clean = reply.strip()
        if clean.startswith("```"):
            clean = "\n".join(clean.splitlines()[1:])
        if clean.endswith("```"):
            clean = clean[: clean.rfind("```")]
        extracted = json.loads(clean.strip())
    except Exception as exc:
        print(f"PDF IMPORT — MiniMax error: {exc}")
        return jsonify({"error": f"LLM/parse error: {exc}", "raw_reply": reply if 'reply' in dir() else ""}), 500

    # 3) Upsert into DB
    added_companies   = []
    added_businesses  = []
    added_bc          = []   # plain "A ↔ B" strings (legacy)
    added_bc_detail   = []   # "A ↔ B — comment" strings
    errors            = []

    with get_db() as conn:
        # Upsert companies
        for co in extracted.get("companies", []):
            ticker = (co.get("ticker") or co.get("name") or "").strip()
            desc   = (co.get("description") or "").strip()
            if not ticker:
                continue
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO companies (name, description) VALUES (?,?)",
                    (ticker, desc),
                )
                added_companies.append(ticker)
            except Exception as exc:
                errors.append(f"company {ticker}: {exc}")

        # Upsert businesses
        for biz in extracted.get("businesses", []):
            bname = (biz.get("name") or "").strip()
            bdesc = (biz.get("description") or "").strip()
            if not bname:
                continue
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO businesses (name, description) VALUES (?,?)",
                    (bname, bdesc),
                )
                added_businesses.append(bname)
            except Exception as exc:
                errors.append(f"business {bname}: {exc}")

        # Upsert relationships
        for rel in extracted.get("relationships", []):
            ticker  = (rel.get("company_ticker") or "").strip()
            bname   = (rel.get("business") or "").strip()
            comment = (rel.get("comment") or "").strip()
            if not ticker or not bname:
                continue
            try:
                co_row = conn.execute(
                    "SELECT id FROM companies WHERE name=?", (ticker,)
                ).fetchone()
                biz_row = conn.execute(
                    "SELECT id FROM businesses WHERE name=?", (bname,)
                ).fetchone()
                if co_row and biz_row:
                    conn.execute(
                        """INSERT OR IGNORE INTO business_company
                           (business_id, company_id, comment, explanation, source_url)
                           VALUES (?,?,?,?,?)""",
                        (biz_row["id"], co_row["id"], comment, "", pdf_source_url),
                    )
                    added_bc.append(f"{ticker} ↔ {bname}")
                    detail = f"{ticker} ↔ {bname}"
                    if comment:
                        detail += f" — {comment}"
                    added_bc_detail.append(detail)
                else:
                    errors.append(f"rel {ticker}↔{bname}: entity not found in DB")
            except Exception as exc:
                errors.append(f"rel {ticker}↔{bname}: {exc}")

    return jsonify({
        "added": {
            "companies":     added_companies,
            "businesses":    added_businesses,
            "bc_links":      added_bc,
            "bc_links_detail": added_bc_detail,
        },
        "errors": errors,
        "prompt": {"system": system_prompt, "user": user_msg},
    })


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
            "shape": "square",
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
        SELECT bc.id, bc.business_id, bc.company_id,
               b.name AS business_name, c.name AS company_name,
               bc.comment, bc.explanation, bc.image_path, bc.source_url
        FROM business_company bc
        JOIN businesses b ON b.id = bc.business_id
        JOIN companies  c ON c.id = bc.company_id
        ORDER BY b.name, c.name
    """).fetchall()
    bb_links = conn.execute("""
        SELECT bb.id, bb.business_from, bb.business_to,
               bf.name AS from_name, bt.name AS to_name,
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

  <!-- ── Active filter indicator ── -->
  <div id="filter-bar" class="d-none mb-2 d-flex align-items-center gap-2">
    <span style="font-size:.78rem;color:#555">Filtering by:</span>
    <span id="filter-label" class="badge bg-secondary" style="font-size:.78rem"></span>
    <button class="btn btn-sm btn-link p-0 text-muted" style="font-size:.75rem" onclick="clearFilter()">✕ clear</button>
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
    <li class="nav-item">
      <a class="nav-link {% if active_tab=='pdf' %}active{% endif %}" data-bs-toggle="tab" href="#tab-pdf">
        Import from PDF
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
        <div id="bc-mine-prompt-wrap" class="d-none mt-1">
          <button class="btn btn-sm btn-link p-0 text-muted" style="font-size:.75rem" onclick="toggleEl('bc-mine-prompt-detail')">▶ Show prompt</button>
          <div id="bc-mine-prompt-detail" class="d-none mt-1 border rounded p-2" style="background:#f8f9fa">
            <div style="font-size:.7rem;font-weight:600;color:#555">SYSTEM</div>
            <pre id="bc-mine-prompt-system" style="font-size:.7rem;white-space:pre-wrap;max-height:100px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:4px;border-radius:3px"></pre>
            <div style="font-size:.7rem;font-weight:600;color:#555">USER</div>
            <pre id="bc-mine-prompt-user"   style="font-size:.7rem;white-space:pre-wrap;max-height:130px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:4px;border-radius:3px"></pre>
          </div>
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
            <td>
              <span class="badge-business">{{r.business_name}}</span>
              <form method="post" action="/business/delete/{{r.business_id}}" style="display:inline">
                <button class="btn btn-link text-danger p-0 ms-1" style="font-size:.7rem;line-height:1"
                        title="Delete business {{r.business_name}}">✕</button>
              </form>
            </td>
            <td>
              <span class="badge-company">{{r.company_name}}</span>
              <form method="post" action="/company/delete/{{r.company_id}}" style="display:inline">
                <button class="btn btn-link text-danger p-0 ms-1" style="font-size:.7rem;line-height:1"
                        title="Delete company {{r.company_name}}">✕</button>
              </form>
            </td>
            <td class="comment-col">{{r.comment}}</td>
            <td class="expl-col">
              {% if r.explanation %}
                {% if r.explanation|length > 120 %}
                  <span class="expl-preview" onclick="showExpl('{{r.business_name}} → {{r.company_name}}', this.dataset.full)" data-full="{{r.explanation|e}}" style="cursor:pointer">{{r.explanation[:120]}}… <span class="text-primary" style="font-size:.75rem">▶ more</span></span>
                {% else %}
                  {{r.explanation}}
                {% endif %}
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.image_path %}
              <img src="/uploads/{{r.image_path}}" class="img-thumb"
                   onclick="showImg('/uploads/{{r.image_path}}')" title="Click to enlarge">
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.source_url and (r.source_url.startswith('http') or r.source_url.startswith('/')) %}
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
        <div id="bb-mine-prompt-wrap" class="d-none mt-1">
          <button class="btn btn-sm btn-link p-0 text-muted" style="font-size:.75rem" onclick="toggleEl('bb-mine-prompt-detail')">▶ Show prompt</button>
          <div id="bb-mine-prompt-detail" class="d-none mt-1 border rounded p-2" style="background:#f8f9fa">
            <div style="font-size:.7rem;font-weight:600;color:#555">SYSTEM</div>
            <pre id="bb-mine-prompt-system" style="font-size:.7rem;white-space:pre-wrap;max-height:100px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:4px;border-radius:3px"></pre>
            <div style="font-size:.7rem;font-weight:600;color:#555">USER</div>
            <pre id="bb-mine-prompt-user"   style="font-size:.7rem;white-space:pre-wrap;max-height:130px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:4px;border-radius:3px"></pre>
          </div>
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
            <td>
              <span class="badge-business">{{r.from_name}}</span>
              <form method="post" action="/business/delete/{{r.business_from}}" style="display:inline">
                <button class="btn btn-link text-danger p-0 ms-1" style="font-size:.7rem;line-height:1"
                        title="Delete business {{r.from_name}}">✕</button>
              </form>
            </td>
            <td>
              <span class="badge-business">{{r.to_name}}</span>
              <form method="post" action="/business/delete/{{r.business_to}}" style="display:inline">
                <button class="btn btn-link text-danger p-0 ms-1" style="font-size:.7rem;line-height:1"
                        title="Delete business {{r.to_name}}">✕</button>
              </form>
            </td>
            <td class="comment-col">{{r.comment}}</td>
            <td class="expl-col">
              {% if r.explanation %}
                {% if r.explanation|length > 120 %}
                  <span class="expl-preview" onclick="showExpl('{{r.from_name}} → {{r.to_name}}', this.dataset.full)" data-full="{{r.explanation|e}}" style="cursor:pointer">{{r.explanation[:120]}}… <span class="text-primary" style="font-size:.75rem">▶ more</span></span>
                {% else %}
                  {{r.explanation}}
                {% endif %}
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.image_path %}
              <img src="/uploads/{{r.image_path}}" class="img-thumb"
                   onclick="showImg('/uploads/{{r.image_path}}')" title="Click to enlarge">
              {% else %}—{% endif %}
            </td>
            <td>
              {% if r.source_url and (r.source_url.startswith('http') or r.source_url.startswith('/')) %}
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

    <!-- ══ Tab: Import from PDF ══ -->
    <div class="tab-pane fade {% if active_tab=='pdf' %}show active{% endif %}" id="tab-pdf">
      <h5>Import entities &amp; relationships from PDF</h5>
      <p class="text-muted" style="font-size:.85rem">
        Upload a PDF report (e.g. annual report, earnings filing). Text from the first 3 pages
        is sent to AI to extract companies (tickers), business domains, and their relationships,
        which are then added to the knowledge graph.
      </p>

      <div class="border rounded p-3 mb-3" style="background:#fafafa;max-width:540px">
        <div class="mb-3">
          <label class="form-label" style="font-size:.85rem;font-weight:600">PDF file</label>
          <input type="file" id="pdf-file-input" class="form-control form-control-sm" accept=".pdf">
          <div class="form-text">Only the first 3 pages are analysed.</div>
        </div>
        <button class="btn btn-sm btn-primary" onclick="importPDF()">
          <span id="pdf-spinner" class="spinner-border spinner-border-sm d-none me-1"></span>
          Extract &amp; Import with AI
        </button>
        <span class="text-danger small ms-2" id="pdf-err"></span>
      </div>

      <!-- Results -->
      <div id="pdf-results" class="d-none">
        <h6>Import results</h6>
        <div class="row g-3">
          <div class="col-md-4">
            <div class="card card-body p-2">
              <div class="text-muted" style="font-size:.75rem;font-weight:600">COMPANIES ADDED</div>
              <ul id="pdf-res-companies" class="mb-0 ps-3" style="font-size:.82rem"></ul>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card card-body p-2">
              <div class="text-muted" style="font-size:.75rem;font-weight:600">BUSINESSES ADDED</div>
              <ul id="pdf-res-businesses" class="mb-0 ps-3" style="font-size:.82rem"></ul>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card card-body p-2">
              <div class="text-muted" style="font-size:.75rem;font-weight:600">RELATIONSHIPS ADDED</div>
              <ul id="pdf-res-bc" class="mb-0 ps-3" style="font-size:.82rem"></ul>
            </div>
          </div>
        </div>
        <div id="pdf-res-errors" class="text-danger small mt-2"></div>
        <!-- Prompt viewer -->
        <div class="mt-2">
          <button class="btn btn-sm btn-link p-0 text-muted" onclick="toggleEl('pdf-prompt-detail')">
            ▶ Show prompt sent to model
          </button>
          <div id="pdf-prompt-detail" class="d-none mt-2 border rounded p-2" style="background:#f8f9fa">
            <div class="mb-1" style="font-size:.72rem;font-weight:600;color:#555">SYSTEM</div>
            <pre id="pdf-prompt-system" class="mb-2" style="font-size:.72rem;white-space:pre-wrap;max-height:140px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:6px;border-radius:4px"></pre>
            <div class="mb-1" style="font-size:.72rem;font-weight:600;color:#555">USER</div>
            <pre id="pdf-prompt-user"   class="mb-0" style="font-size:.72rem;white-space:pre-wrap;max-height:200px;overflow-y:auto;background:#fff;border:1px solid #ddd;padding:6px;border-radius:4px"></pre>
          </div>
        </div>
        <div class="mt-3">
          <a href="/" class="btn btn-sm btn-outline-secondary">Reload graph to see changes</a>
        </div>
      </div>
    </div><!-- /tab-pdf -->

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

<!-- Explanation expand modal -->
<div class="modal fade" id="explModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="modal-header py-2 px-3">
        <h6 class="modal-title mb-0" id="explModalTitle"></h6>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body px-3 py-2" id="explModalBody" style="white-space:pre-wrap;font-size:.88rem;line-height:1.6"></div>
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

// ── Table filtering from graph clicks ──────────────────────────────────────
function switchTab(href) {
  const el = document.querySelector('a[href="' + href + '"]');
  if (el) bootstrap.Tab.getOrCreateInstance(el).show();
}

function filterTables(type, nameA, nameB) {
  // BC table
  document.querySelectorAll('#tab-bc tbody tr').forEach(row => {
    if (!type) { row.style.display = ''; return; }
    const biz = row.querySelector('.badge-business')?.textContent.trim();
    const co  = row.querySelector('.badge-company')?.textContent.trim();
    let show = false;
    if (type === 'company')  show = co  === nameA;
    if (type === 'business') show = biz === nameA;
    if (type === 'bc-edge')  show = biz === nameA && co === nameB;
    row.style.display = show ? '' : 'none';
  });
  // BB table
  document.querySelectorAll('#tab-bb tbody tr').forEach(row => {
    if (!type) { row.style.display = ''; return; }
    const cells = row.querySelectorAll('.badge-business');
    const from  = cells[0]?.textContent.trim();
    const to    = cells[1]?.textContent.trim();
    let show = false;
    if (type === 'business') show = from === nameA || to === nameA;
    if (type === 'bb-edge')  show = from === nameA && to === nameB;
    row.style.display = show ? '' : 'none';
  });
}

function showFilterBar(label) {
  document.getElementById('filter-label').textContent = label;
  document.getElementById('filter-bar').classList.remove('d-none');
}

function clearFilter() {
  filterTables(null, null, null);
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

// ── explanation expand ──────────────────────────────────────────────────────
function showExpl(title, text) {
  document.getElementById("explModalTitle").textContent = title;
  document.getElementById("explModalBody").textContent  = text;
  new bootstrap.Modal(document.getElementById("explModal")).show();
}

// ── helpers ─────────────────────────────────────────────────────────────────
function toggleEl(id) {
  document.getElementById(id).classList.toggle('d-none');
}

// ── AI mine helpers ────────────────────────────────────────────────────────
async function callMine(url, entityA, entityB, commentId, explId, errId, spinnerId, promptPrefix) {
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
    // Show prompt
    if (data.prompt && promptPrefix) {
      document.getElementById(promptPrefix + '-prompt-system').textContent = data.prompt.system || '';
      document.getElementById(promptPrefix + '-prompt-user').textContent   = data.prompt.user   || '';
      document.getElementById(promptPrefix + '-prompt-wrap').classList.remove('d-none');
    }
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
    "bc-form-comment", "bc-form-expl", "bc-mine-err", "bc-mine-spinner", "bc-mine"
  );
}
function mineBB() {
  callMine(
    document.getElementById("bb-mine-url").value,
    document.getElementById("bb-mine-from").value,
    document.getElementById("bb-mine-to").value,
    "bb-form-comment", "bb-form-expl", "bb-mine-err", "bb-mine-spinner", "bb-mine"
  );
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
    // Relationships: show "Ticker ↔ Business — comment" if available
    fillList("pdf-res-bc", (data.added.bc_links_detail || data.added.bc_links));

    const errEl = document.getElementById("pdf-res-errors");
    errEl.textContent = (data.errors && data.errors.length)
      ? "Warnings: " + data.errors.join("; ")
      : "";

    // Populate prompt
    if (data.prompt) {
      document.getElementById("pdf-prompt-system").textContent = data.prompt.system || '';
      document.getElementById("pdf-prompt-user").textContent   = data.prompt.user   || '';
    }

    resultsEl.classList.remove("d-none");
  } catch(e) {
    errDiv.textContent = "Network error: " + e.message;
  } finally {
    spinner.classList.add("d-none");
  }
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
        # Remember connected businesses before cascade-deleting the company
        biz_ids = [r["business_id"] for r in conn.execute(
            "SELECT business_id FROM business_company WHERE company_id=?", (cid,)
        ).fetchall()]
        conn.execute("DELETE FROM companies WHERE id=?", (cid,))
        # Clean up businesses that now have no relationships
        for bid in biz_ids:
            bc = conn.execute("SELECT COUNT(*) FROM business_company  WHERE business_id=?",  (bid,)).fetchone()[0]
            bb = conn.execute("SELECT COUNT(*) FROM business_business WHERE business_from=? OR business_to=?", (bid, bid)).fetchone()[0]
            if bc + bb == 0:
                conn.execute("DELETE FROM businesses WHERE id=?", (bid,))
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
        # Remember connected companies before cascade-deleting the business
        co_ids = [r["company_id"] for r in conn.execute(
            "SELECT company_id FROM business_company WHERE business_id=?", (bid,)
        ).fetchall()]
        conn.execute("DELETE FROM businesses WHERE id=?", (bid,))
        # Clean up companies that now have no relationships
        for cid in co_ids:
            bc = conn.execute("SELECT COUNT(*) FROM business_company WHERE company_id=?", (cid,)).fetchone()[0]
            if bc == 0:
                conn.execute("DELETE FROM companies WHERE id=?", (cid,))
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
        row = conn.execute(
            "SELECT business_id, company_id, image_path FROM business_company WHERE id=?", (rid,)
        ).fetchone()
        if not row:
            return redirect(url_for("index"))
        business_id = row["business_id"]
        company_id  = row["company_id"]
        if row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_company WHERE id=?", (rid,))
        # Clean up orphaned company
        if conn.execute("SELECT COUNT(*) FROM business_company WHERE company_id=?", (company_id,)).fetchone()[0] == 0:
            conn.execute("DELETE FROM companies WHERE id=?", (company_id,))
        # Clean up orphaned business
        bc = conn.execute("SELECT COUNT(*) FROM business_company  WHERE business_id=?",  (business_id,)).fetchone()[0]
        bb = conn.execute("SELECT COUNT(*) FROM business_business WHERE business_from=? OR business_to=?", (business_id, business_id)).fetchone()[0]
        if bc + bb == 0:
            conn.execute("DELETE FROM businesses WHERE id=?", (business_id,))
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
        row = conn.execute(
            "SELECT business_from, business_to, image_path FROM business_business WHERE id=?", (rid,)
        ).fetchone()
        if not row:
            return redirect(url_for("index") + "#tab-bb")
        bfrom = row["business_from"]
        bto   = row["business_to"]
        if row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_business WHERE id=?", (rid,))
        # Clean up orphaned businesses (check both endpoints)
        for bid in set([bfrom, bto]):
            bc = conn.execute("SELECT COUNT(*) FROM business_company  WHERE business_id=?",  (bid,)).fetchone()[0]
            bb = conn.execute("SELECT COUNT(*) FROM business_business WHERE business_from=? OR business_to=?", (bid, bid)).fetchone()[0]
            if bc + bb == 0:
                conn.execute("DELETE FROM businesses WHERE id=?", (bid,))
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
