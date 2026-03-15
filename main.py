#!/usr/bin/env python3
"""
main.py — Unified FinAgent web app (all 4 tools on one port).

Routes
------
  /      -> redirect to /kg
  /kg/*  -> Knowledge Graph
  /zsxq/* -> ZSXQ Viewer
  /sec/* -> US SEC Reports (10-K / 10-Q / 8-K)
  /cn/*  -> A-share / HK CNINFO Reports

Usage
-----
    python main.py [--port 5001]
    Then open  http://localhost:5001
"""

import argparse
import sys
from pathlib import Path

from flask import Flask, redirect, jsonify, request as freq

import md_comment_widget as mcw

# -- Import sub-app blueprints -------------------------------------------------
# knowledge_graph imports minimax which inserts the parent project dir at
# sys.path[0]; re-insert this worktree dir afterwards so that local copies
# of zsxq_viewer, fetch_financial_report, etc. take priority.
_WORKTREE_DIR = str(Path(__file__).parent)
from knowledge_graph        import kg_bp, UPLOAD_DIR as _KG_UPLOAD
from knowledge_graph        import kg_db as _kg_db, kg_services as _kg_svc
from knowledge_graph        import DEFAULT_ZSXQ_DB as _ZSXQ_DB_DEFAULT
if _WORKTREE_DIR in sys.path:
    sys.path.remove(_WORKTREE_DIR)
sys.path.insert(0, _WORKTREE_DIR)
import zsxq_viewer as _zsxq_viewer_mod
zsxq_bp = _zsxq_viewer_mod.zsxq_bp
from fetch_financial_report import sec_bp, init_db as _sec_init
from fetch_cninfo_report    import cn_bp,  init_db as _cn_init

SCRIPT_DIR  = Path(__file__).parent
UPLOADS_DIR = SCRIPT_DIR / "uploads"

# -- Build unified app ---------------------------------------------------------
app = Flask(__name__,
            template_folder=str(SCRIPT_DIR / "templates"),
            static_folder=str(SCRIPT_DIR / "static"))
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

# One shared MCW blueprint for all image-upload routes (/upload-image, /uploads/...)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))

# Sub-app blueprints
app.register_blueprint(kg_bp,   url_prefix="/kg")
app.register_blueprint(zsxq_bp, url_prefix="/zsxq")
app.register_blueprint(sec_bp,  url_prefix="/sec")
app.register_blueprint(cn_bp,   url_prefix="/cn")


@app.route("/")
def index():
    return redirect("/kg")


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "File too large (max 50 MB)"}), 413


# Map blueprint name -> URL prefix for context injection
_BP_PREFIXES = {
    "kg":   "/kg",
    "zsxq": "/zsxq",
    "sec":  "/sec",
    "cn":   "/cn",
}


@app.context_processor
def _inject_base():
    """Inject _base (e.g. '/kg') into every Jinja2 template context."""
    bps = list(freq.blueprints)
    prefix = _BP_PREFIXES.get(bps[0], "") if bps else ""
    return dict(_base=prefix)


# -- Entry point ---------------------------------------------------------------
if __name__ == "__main__":
    # Initialise all databases
    import sqlite3 as _sqlite3
    def _db_has_rows(p: Path, table: str) -> bool:
        """Return True if the SQLite file exists and the table has at least one row."""
        try:
            con = _sqlite3.connect(p)
            n = con.execute(
                f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?"
                , (table,)
            ).fetchone()[0]
            if n == 0:
                con.close()
                return False
            n = con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            con.close()
            return n > 0
        except Exception:
            return False

    # For each DB: if the local (worktree) copy is empty, fall back to the
    # parent project's copy which has the real downloaded data.
    _PARENT = SCRIPT_DIR.parent.parent.parent  # financial_agent/

    def _resolve_db(filename: str, table: str) -> Path:
        local = SCRIPT_DIR / filename
        if not _db_has_rows(local, table):
            parent_copy = _PARENT / filename
            if parent_copy.exists() and _db_has_rows(parent_copy, table):
                print(f"  [db] {filename}: using parent project copy ({parent_copy})")
                return parent_copy
        return local

    _ZSXQ_DB    = _resolve_db("zsxq.db",              "pdf_files")
    _SEC_DB     = _resolve_db("financial_reports.db",  "reports")
    _CN_DB      = _resolve_db("cninfo_reports.db",     "cninfo_reports")

    _zsxq_viewer_mod.DB_PATH = _ZSXQ_DB

    import fetch_financial_report as _sec_mod
    import fetch_cninfo_report    as _cn_mod
    _sec_mod._DB_PATH = _SEC_DB
    _cn_mod._DB_PATH  = _CN_DB

    _kg_db.set_db_path(SCRIPT_DIR / "knowledge_graph.db")
    _kg_svc.set_zsxq_db_path(_ZSXQ_DB)
    _kg_db.init_db(_KG_UPLOAD)
    _kg_db.seed_db()
    _sec_init()
    _cn_init()

    parser = argparse.ArgumentParser(description="Unified FinAgent web app")
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    print(f"FinAgent unified app ->  http://localhost:{args.port}")
    print(f"  /kg    -> Knowledge Graph")
    print(f"  /zsxq  -> ZSXQ Viewer")
    print(f"  /sec   -> US Reports (SEC EDGAR)")
    print(f"  /cn    -> CN Reports (CNINFO)")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
