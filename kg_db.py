"""
kg_db.py — Database connection, schema, and seed data for the knowledge graph.
"""

import sqlite3
from pathlib import Path

# Resolved at import time so callers can do: from kg_db import get_db, init_db
_DB_PATH: Path | None = None   # set by knowledge_graph.main()


def set_db_path(path: Path) -> None:
    global _DB_PATH
    _DB_PATH = path


def get_db_path() -> Path:
    if _DB_PATH is None:
        raise RuntimeError("DB path not set; call kg_db.set_db_path() first")
    return _DB_PATH


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ── Schema ────────────────────────────────────────────────────────────────────

_DDL = """
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
"""

_MIGRATIONS = [
    "ALTER TABLE business_company ADD COLUMN rating INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE business_business ADD COLUMN rating INTEGER NOT NULL DEFAULT 0",
    # Track which zsxq.db file_ids have already been imported
    """CREATE TABLE IF NOT EXISTS zsxq_imported (
        file_id     INTEGER PRIMARY KEY,
        imported_at TEXT    NOT NULL DEFAULT (datetime('now'))
    )""",
    "ALTER TABLE business_company ADD COLUMN created_at TEXT DEFAULT (datetime('now'))",
    "ALTER TABLE business_business ADD COLUMN created_at TEXT DEFAULT (datetime('now'))",
]


def init_db(upload_dir: Path) -> None:
    upload_dir.mkdir(parents=True, exist_ok=True)
    with get_db() as conn:
        conn.executescript(_DDL)
        for stmt in _MIGRATIONS:
            try:
                conn.execute(stmt)
            except Exception:
                pass  # column already exists


# ── Seed data ─────────────────────────────────────────────────────────────────

def seed_db() -> None:
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
            ("GPU",             "Graphics Processing Unit — massively parallel compute"),
            ("CPU",             "Central Processing Unit — general-purpose compute"),
            ("Memory",          "DRAM / HBM / cache — high-speed data storage"),
            ("Manufacturing",   "Semiconductor fab and wafer production"),
            ("TPU",             "Tensor Processing Unit — AI/ML inference & training"),
            ("Compiler",        "Software that translates code to hardware instructions"),
            ("EUV Lithography", "Extreme-UV patterning tools for advanced nodes"),
            ("Networking",      "High-speed interconnects (NVLink, InfiniBand, etc.)"),
            ("Storage",         "NAND flash, SSDs, persistent memory"),
            ("Mobile SoC",      "System-on-chip for smartphones and edge devices"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO businesses (name, description) VALUES (?, ?)", businesses
        )

        def bid(name):
            return conn.execute("SELECT id FROM businesses WHERE name=?", (name,)).fetchone()["id"]

        def cid(name):
            return conn.execute("SELECT id FROM companies WHERE name=?", (name,)).fetchone()["id"]

        bc_links = [
            ("GPU",             "NVIDIA",   "NVIDIA's core revenue driver; leads datacenter GPU market",
             "NVIDIA designs the H100/H200/B200 GPU series and dominates the AI accelerator market. Revenue from Data Center GPUs exceeded 80 % of total revenue in 2024."),
            ("GPU",             "AMD",      "AMD Radeon and Instinct lines compete across gaming and AI",
             "AMD's MI300X HBM-stacked GPU targets large-language-model inference and competes directly with NVIDIA's H100."),
            ("GPU",             "Intel",    "Intel Arc GPUs and Xe graphics target gaming and HPC",
             "Intel re-entered the discrete GPU market with Arc Alchemist and continues developing Xe2 for HPC and AI workloads."),
            ("CPU",             "Intel",    "Intel's foundational business since 1968",
             "Intel's Core and Xeon product lines power the vast majority of PCs and servers globally, though market share has been pressured by AMD Zen architecture."),
            ("CPU",             "AMD",      "AMD Ryzen and EPYC challenge Intel across desktop and server",
             "AMD's EPYC server CPUs have taken double-digit market share from Intel Xeon by offering more cores per socket at competitive pricing."),
            ("CPU",             "Apple",    "Apple Silicon (M-series) integrates CPU, GPU, and NPU",
             "Apple's M-series chips use ARM cores with a unified memory architecture, delivering industry-leading performance-per-watt in laptops and desktops."),
            ("CPU",             "Qualcomm", "Qualcomm Snapdragon CPU cores power mobile devices globally",
             "Qualcomm's Oryon CPU cores (acquired from Nuvia) are now shipping in Snapdragon X Elite for PC and premium Android devices."),
            ("Memory",          "Samsung",  "Samsung is the world's largest DRAM and NAND producer",
             "Samsung supplies HBM3e to NVIDIA and SK Hynix competes alongside it; Samsung also manufactures its own NAND for enterprise SSDs."),
            ("Memory",          "Micron",   "Micron supplies DRAM, HBM, and NAND to hyperscalers",
             "Micron's HBM3e is qualified for NVIDIA H200 and GB200, making it a critical memory supplier for AI infrastructure build-outs."),
            ("Manufacturing",   "TSMC",     "TSMC manufactures chips for Apple, NVIDIA, AMD, and others",
             "TSMC's N3 (3 nm) and N2 (2 nm) processes represent the global frontier; all leading AI chips are fabbed there."),
            ("Manufacturing",   "Samsung",  "Samsung Foundry competes with TSMC on leading-edge nodes",
             "Samsung Foundry's SF3 (3 nm GAA) process targets high-performance mobile and server chips in competition with TSMC N3."),
            ("Manufacturing",   "Intel",    "Intel Foundry Services (IFS) aims to regain process leadership",
             "Intel 18A (1.8 nm class) uses RibbonFET and PowerVia backside power delivery; Microsoft and others are sampling it in 2025."),
            ("TPU",             "Google",   "Google TPUs power Search, Translate, and Vertex AI",
             "Google Trillium (TPU v6) delivers 4.7× the compute of TPU v5e and runs Gemini model training and inference at hyperscale."),
            ("Compiler",        "NVIDIA",   "NVCC and cuDNN/TensorRT compile CUDA and AI workloads",
             "The CUDA toolchain — NVCC, cuDNN, TensorRT, and Triton — forms the dominant software stack for GPU-based AI workloads."),
            ("Compiler",        "Google",   "XLA compiler optimises TPU and GPU workloads for ML",
             "XLA (Accelerated Linear Algebra) powers JAX and TensorFlow, and is now used by PyTorch/XLA to target both TPU and GPU."),
            ("EUV Lithography", "ASML",     "ASML holds a monopoly on EUV scanners used at sub-5 nm nodes",
             "ASML's High-NA EUV (EXE:5000) enables sub-2 nm patterning; delivery to TSMC and Intel began in 2024 for N2/18A processes."),
            ("Networking",      "NVIDIA",   "NVIDIA InfiniBand and NVLink connect GPUs in AI clusters",
             "NVIDIA's acquisition of Mellanox gave it InfiniBand; combined with NVLink 5 in Blackwell, it controls both intra- and inter-node GPU networking."),
            ("Storage",         "Samsung",  "Samsung supplies SSDs and flash to OEMs worldwide",
             "Samsung 990 Pro NVMe SSDs and QLC V-NAND are widely deployed in AI storage pipelines and consumer devices."),
            ("Storage",         "Micron",   "Micron NAND underpins enterprise and consumer SSDs",
             "Micron's 232-layer NAND enables high-density enterprise SSDs used in AI training data lakes."),
            ("Mobile SoC",      "Qualcomm", "Snapdragon SoCs are in the majority of Android flagships",
             "Snapdragon 8 Elite integrates Oryon CPU, Adreno GPU, and Hexagon NPU delivering on-device AI at sub-10W."),
            ("Mobile SoC",      "Apple",    "Apple A-series chips set performance benchmarks for mobile",
             "Apple A18 Pro (3 nm) powers iPhone 16 Pro with a 16-core Neural Engine capable of 35 TOPS for on-device AI."),
        ]
        for bname, cname, comment, explanation in bc_links:
            conn.execute(
                "INSERT OR IGNORE INTO business_company "
                "(business_id, company_id, comment, explanation) VALUES (?,?,?,?)",
                (bid(bname), cid(cname), comment, explanation),
            )

        bb_links = [
            ("GPU",             "Memory",          "GPUs require high-bandwidth memory (HBM) to feed thousands of cores",
             "H100 uses HBM3 with 3.35 TB/s bandwidth; without that memory bandwidth the GPU compute units would stall waiting for data."),
            ("GPU",             "Networking",      "Multi-GPU clusters need fast interconnects (NVLink/InfiniBand)",
             "Training large models requires all-reduce operations across hundreds of GPUs; NVLink 5 offers 1.8 TB/s bidirectional bandwidth per GPU."),
            ("GPU",             "Compiler",        "CUDA / ROCm compilers translate AI workloads to GPU instructions",
             "NVCC and the Triton compiler lower Python-level tensor operations into PTX and SASS assembly that the GPU executes."),
            ("TPU",             "Compiler",        "XLA and MLIR compilers are essential to program TPU hardware",
             "TPUs have no native C++ API; all computation must go through XLA's HLO IR, making the compiler a first-class citizen of TPU programming."),
            ("TPU",             "Memory",          "TPUs embed HBM for high-throughput tensor operations",
             "TPU v5p uses HBM2e at 459 GB/s per chip; this bandwidth is critical for matrix-multiply operations during transformer model training."),
            ("CPU",             "Memory",          "CPUs depend on DRAM and cache hierarchy for instruction throughput",
             "Modern CPUs stall for hundreds of cycles on a DRAM access (>100 ns); multi-level caches (L1/L2/L3) hide this latency to keep cores fed."),
            ("CPU",             "Compiler",        "LLVM / GCC compilers generate optimised CPU machine code",
             "Auto-vectorisation in LLVM maps loop bodies to AVX-512 SIMD instructions, multiplying throughput without code changes."),
            ("Manufacturing",   "EUV Lithography", "Advanced semiconductor nodes require ASML EUV scanners",
             "Patterns at 5 nm and below require multiple EUV exposures; High-NA EUV reduces the number of multi-patterning steps needed for 2 nm."),
            ("Memory",          "Storage",         "DRAM (volatile) and NAND (non-volatile) together form the memory hierarchy",
             "The memory-storage hierarchy: registers → L1/L2/L3 cache → DRAM → NVMe SSD. Moving data between DRAM and NVMe incurs a 10–100× latency penalty."),
            ("Mobile SoC",      "CPU",             "Mobile SoCs integrate CPU cores (often ARM-based) on the same die",
             "Snapdragon 8 Elite packages Oryon CPU cores, Adreno GPU, Hexagon DSP, and 5G modem on a single TSMC 3 nm die."),
            ("Mobile SoC",      "GPU",             "Mobile SoCs include integrated GPU for graphics and ML acceleration",
             "Adreno 830 inside Snapdragon 8 Elite doubles AI performance versus Adreno 750, enabling real-time generative AI on device."),
            ("GPU",             "Manufacturing",   "Leading GPU dies are fabbed at TSMC/Samsung advanced nodes",
             "NVIDIA's GB100 Blackwell die is fabbed at TSMC N4P; the die area exceeds 800 mm² requiring CoWoS-L advanced packaging."),
            ("CPU",             "Manufacturing",   "High-performance CPUs require cutting-edge fabs for smaller transistors",
             "Intel Lunar Lake uses TSMC N3 for compute tiles; AMD Zen 5 CCDs are also fabbed at TSMC N4 for density and efficiency."),
            ("EUV Lithography", "Memory",          "DRAM scaling beyond 1z nm requires EUV patterning",
             "Samsung and SK Hynix have adopted EUV for DRAM at 1z and 1a nm nodes to achieve the cell density needed for HBM stacking."),
        ]
        for bfrom, bto, comment, explanation in bb_links:
            conn.execute(
                "INSERT OR IGNORE INTO business_business "
                "(business_from, business_to, comment, explanation) VALUES (?,?,?,?)",
                (bid(bfrom), bid(bto), comment, explanation),
            )
