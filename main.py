#!/usr/bin/env python3
"""
main.py — Unified FinAgent web app (all 4 tools on one port).

Routes
------
  /      -> redirect to /zep
  /zep/* -> Zep Knowledge Graph (replaces /kg)
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
from flask_compress import Compress

import md_comment_widget as mcw

# -- Import sub-app blueprints -------------------------------------------------
SCRIPT_DIR  = Path(__file__).parent
UPLOADS_DIR = SCRIPT_DIR / "uploads"

from zep_app import zep_bp
import zsxq_viewer as _zsxq_viewer_mod
zsxq_bp = _zsxq_viewer_mod.zsxq_bp
from fetch_financial_report import sec_bp, init_db as _sec_init
from fetch_cninfo_report    import cn_bp,  init_db as _cn_init
from indicators.app         import indicators_bp, init_db as _ind_init
from pe.app                 import pe_bp
from monitoring.app         import price_shape_bp

# -- Build unified app ---------------------------------------------------------
app = Flask(__name__,
            template_folder=str(SCRIPT_DIR / "templates"),
            static_folder=str(SCRIPT_DIR / "static"))
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
Compress(app)

# One shared MCW blueprint for all image-upload routes (/upload-image, /uploads/...)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))

# Sub-app blueprints
app.register_blueprint(zep_bp,        url_prefix="/zep")
app.register_blueprint(zsxq_bp,       url_prefix="/zsxq")
app.register_blueprint(sec_bp,        url_prefix="/sec")
app.register_blueprint(cn_bp,         url_prefix="/cn")
app.register_blueprint(indicators_bp,   url_prefix="/indicators")
app.register_blueprint(pe_bp,           url_prefix="/pe")
app.register_blueprint(price_shape_bp,  url_prefix="/price-shape")


@app.route("/")
def index():
    return redirect("/zsxq")


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "File too large (max 50 MB)"}), 413


# Map blueprint name -> URL prefix for context injection
_BP_PREFIXES = {
    "zep":        "/zep",
    "zsxq":       "/zsxq",
    "sec":        "/sec",
    "cn":         "/cn",
    "indicators":   "/indicators",
    "price_shape":  "/price-shape",
}


@app.context_processor
def _inject_base():
    """Inject _base (e.g. '/zep') into every Jinja2 template context."""
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
        # DBs now live in db/ subdirectory; fall back to parent project's db/
        local = SCRIPT_DIR / "db" / filename
        if not _db_has_rows(local, table):
            parent_copy = _PARENT / "db" / filename
            if parent_copy.exists() and _db_has_rows(parent_copy, table):
                print(f"  [db] {filename}: using parent project copy ({parent_copy})")
                return parent_copy
        return local

    _ZSXQ_DB = _resolve_db("zsxq.db",              "pdf_files")
    _SEC_DB  = _resolve_db("financial_reports.db",  "reports")
    _CN_DB   = _resolve_db("cninfo_reports.db",     "cninfo_reports")

    _zsxq_viewer_mod.DB_PATH = _ZSXQ_DB

    import fetch_financial_report as _sec_mod
    import fetch_cninfo_report    as _cn_mod
    _sec_mod._DB_PATH = _SEC_DB
    _cn_mod._DB_PATH  = _CN_DB

    _sec_init()
    _cn_init()
    _ind_init()

    parser = argparse.ArgumentParser(description="Unified FinAgent web app")
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    print(f"FinAgent unified app ->  http://localhost:{args.port}")
    print(f"  /zep   -> Zep Knowledge Graph")
    print(f"  /zsxq  -> ZSXQ Viewer")
    print(f"  /sec   -> US Reports (SEC EDGAR)")
    print(f"  /cn    -> CN Reports (CNINFO)")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
