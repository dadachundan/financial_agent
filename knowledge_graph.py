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
  - rating       0–5 integer

Usage
-----
    python knowledge_graph.py
    python knowledge_graph.py --db kg.db --port 5001

Then open http://localhost:5001
"""

import argparse
import urllib.error
from pathlib import Path

from flask import (Flask, jsonify, redirect, render_template,
                   request, send_file, send_from_directory, url_for)

import kg_db
import kg_models
import kg_services

# ── App & defaults ─────────────────────────────────────────────────────────────

SCRIPT_DIR       = Path(__file__).parent
DEFAULT_DB       = SCRIPT_DIR / "knowledge_graph.db"
UPLOAD_DIR       = SCRIPT_DIR / "kg_uploads"
DEFAULT_ZSXQ_DB  = SCRIPT_DIR / "zsxq.db"

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024   # 50 MB


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": "File too large (max 50 MB)"}), 413


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return _render_main()


@app.route("/uploads/<path:fname>")
def serve_upload(fname):
    return send_from_directory(UPLOAD_DIR, fname)


# ── Company CRUD ───────────────────────────────────────────────────────────────

@app.route("/company/add", methods=["POST"])
def company_add():
    name = request.form.get("name", "").strip()
    desc = request.form.get("description", "").strip()
    if name:
        with kg_db.get_db() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO companies (name, description) VALUES (?,?)",
                (name, desc),
            )
    return redirect(url_for("index") + "#tab-entities")


@app.route("/company/delete/<int:cid>", methods=["POST"])
def company_delete(cid):
    with kg_db.get_db() as conn:
        conn.execute("DELETE FROM companies WHERE id=?", (cid,))
    return redirect(url_for("index") + "#tab-entities")


# ── Business CRUD ──────────────────────────────────────────────────────────────

@app.route("/business/add", methods=["POST"])
def business_add():
    name = request.form.get("name", "").strip()
    desc = request.form.get("description", "").strip()
    if name:
        with kg_db.get_db() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO businesses (name, description) VALUES (?,?)",
                (name, desc),
            )
    return redirect(url_for("index") + "#tab-entities")


@app.route("/business/delete/<int:bid>", methods=["POST"])
def business_delete(bid):
    with kg_db.get_db() as conn:
        conn.execute("DELETE FROM businesses WHERE id=?", (bid,))
    return redirect(url_for("index") + "#tab-entities")


# ── Business ↔ Company CRUD ────────────────────────────────────────────────────

@app.route("/bc/add", methods=["POST"])
def bc_add():
    business_id = int(request.form["business_id"])
    company_id  = int(request.form["company_id"])
    comment     = request.form.get("comment", "").strip()
    explanation = request.form.get("explanation", "").strip()
    source_url  = request.form.get("source_url", "").strip()
    rating      = kg_services._parse_rating(request.form.get("rating"))
    image_path  = kg_services.save_upload(request.files, "image", UPLOAD_DIR)
    with kg_db.get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO business_company "
            "(business_id, company_id, comment, explanation, image_path, source_url, rating) "
            "VALUES (?,?,?,?,?,?,?)",
            (business_id, company_id, comment, explanation, image_path, source_url, rating),
        )
    return redirect(url_for("index"))


@app.route("/bc/rate/<int:rid>", methods=["POST"])
def bc_rate(rid):
    rating = kg_services._parse_rating(request.form.get("rating"))
    with kg_db.get_db() as conn:
        conn.execute("UPDATE business_company SET rating=? WHERE id=?", (rating, rid))
    return "", 204


@app.route("/bc/delete/<int:rid>", methods=["POST"])
def bc_delete(rid):
    with kg_db.get_db() as conn:
        row = conn.execute(
            "SELECT image_path FROM business_company WHERE id=?", (rid,)
        ).fetchone()
        if row and row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_company WHERE id=?", (rid,))
    return redirect(url_for("index"))


# ── Business ↔ Business CRUD ───────────────────────────────────────────────────

@app.route("/bb/add", methods=["POST"])
def bb_add():
    bfrom       = int(request.form["business_from"])
    bto         = int(request.form["business_to"])
    comment     = request.form.get("comment", "").strip()
    explanation = request.form.get("explanation", "").strip()
    source_url  = request.form.get("source_url", "").strip()
    rating      = kg_services._parse_rating(request.form.get("rating"))
    image_path  = kg_services.save_upload(request.files, "image", UPLOAD_DIR)
    with kg_db.get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO business_business "
            "(business_from, business_to, comment, explanation, image_path, source_url, rating) "
            "VALUES (?,?,?,?,?,?,?)",
            (bfrom, bto, comment, explanation, image_path, source_url, rating),
        )
    return redirect(url_for("index") + "#tab-bb")


@app.route("/bb/rate/<int:rid>", methods=["POST"])
def bb_rate(rid):
    rating = kg_services._parse_rating(request.form.get("rating"))
    with kg_db.get_db() as conn:
        conn.execute("UPDATE business_business SET rating=? WHERE id=?", (rating, rid))
    return "", 204


@app.route("/bb/delete/<int:rid>", methods=["POST"])
def bb_delete(rid):
    with kg_db.get_db() as conn:
        row = conn.execute(
            "SELECT image_path FROM business_business WHERE id=?", (rid,)
        ).fetchone()
        if row and row["image_path"]:
            (UPLOAD_DIR / row["image_path"]).unlink(missing_ok=True)
        conn.execute("DELETE FROM business_business WHERE id=?", (rid,))
    return redirect(url_for("index") + "#tab-bb")


# ── API: LLM summarisation ─────────────────────────────────────────────────────

@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """
    POST JSON { "url": "...", "entity_a": "...", "entity_b": "..." }
    Returns   { "comment": "...", "explanation": "..." }
    """
    data = request.get_json(force=True)
    url      = (data.get("url")      or "").strip()
    entity_a = (data.get("entity_a") or "").strip()
    entity_b = (data.get("entity_b") or "").strip()

    if not url or not entity_a or not entity_b:
        return jsonify({"error": "url, entity_a and entity_b are required"}), 400

    try:
        result = kg_services.llm_summarize_url(url, entity_a, entity_b)
        return jsonify(result)
    except urllib.error.URLError as exc:
        return jsonify({"error": f"Could not fetch URL: {exc}"}), 502
    except Exception as exc:
        return jsonify({"error": f"Error: {exc}"}), 500


# ── API: PDF import ────────────────────────────────────────────────────────────

@app.route("/api/pdf-import", methods=["POST"])
def api_pdf_import():
    """
    POST multipart { "pdf": <file> }
    Returns { "added": {...}, "errors": [...] }
    """
    pdf_file = request.files.get("pdf")
    if not pdf_file or not pdf_file.filename:
        return jsonify({"error": "No PDF file provided"}), 400
    if Path(pdf_file.filename).suffix.lower() not in kg_services.ALLOWED_PDF_EXT:
        return jsonify({"error": "Only .pdf files are accepted"}), 400

    # Save PDF for source reference
    import uuid
    pdf_bytes = pdf_file.read()
    pdf_stored_name = uuid.uuid4().hex + ".pdf"
    (UPLOAD_DIR / pdf_stored_name).write_bytes(pdf_bytes)
    pdf_source_url = f"/uploads/{pdf_stored_name}"

    try:
        raw_text = kg_services.extract_pdf_text(pdf_bytes)
    except Exception as exc:
        return jsonify({"error": f"PDF extraction failed: {exc}"}), 500

    if not raw_text:
        return jsonify({"error": "No text could be extracted from the PDF"}), 422

    try:
        extracted = kg_services.llm_extract_entities(raw_text)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503 if "API key" in str(exc) else 500
    except Exception as exc:
        return jsonify({"error": f"LLM/parse error: {exc}"}), 500

    with kg_db.get_db() as conn:
        added, errors = kg_services.upsert_pdf_entities(conn, extracted, pdf_source_url)

    return jsonify({"added": added, "errors": errors})


# ── API: zsxq.db batch import ──────────────────────────────────────────────────

@app.route("/api/zsxq-import", methods=["POST"])
def api_zsxq_import():
    """
    POST (no body required)
    Reads unprocessed rows from zsxq.db, calls MiniMax on each summary,
    upserts entities into knowledge_graph.db.
    Returns { "processed": N, "skipped": N, "added": {...}, "errors": [...] }
    """
    try:
        with kg_db.get_db() as conn:
            result = kg_services.zsxq_import_batch(conn)
        return jsonify(result)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:
        return jsonify({"error": f"Import error: {exc}"}), 500


@app.route("/zsxq-pdf/<int:file_id>")
def zsxq_pdf(file_id: int):
    """Serve a local PDF from zsxq.db by file_id."""
    import sqlite3
    try:
        conn = sqlite3.connect(kg_services.get_zsxq_db_path())
        row = conn.execute(
            "SELECT local_path FROM pdf_files WHERE file_id=?", (file_id,)
        ).fetchone()
        conn.close()
    except Exception as exc:
        return f"DB error: {exc}", 500

    if not row or not row[0]:
        return "PDF not found", 404

    local_path = Path(row[0])
    if not local_path.exists():
        return f"File not on disk: {local_path}", 404

    return send_file(local_path, mimetype="application/pdf")


# ── Page renderer ──────────────────────────────────────────────────────────────

def _render_main(active_tab: str = "bc"):
    conn = kg_db.get_db()
    companies  = conn.execute("SELECT * FROM companies  ORDER BY name").fetchall()
    businesses = conn.execute("SELECT * FROM businesses ORDER BY name").fetchall()
    bc_links = conn.execute("""
        SELECT bc.id, b.name AS business_name, c.name AS company_name,
               bc.comment, bc.explanation, bc.image_path, bc.source_url, bc.rating
        FROM business_company bc
        JOIN businesses b ON b.id = bc.business_id
        JOIN companies  c ON c.id = bc.company_id
        ORDER BY b.name, c.name
    """).fetchall()
    bb_links = conn.execute("""
        SELECT bb.id, bf.name AS from_name, bt.name AS to_name,
               bb.comment, bb.explanation, bb.image_path, bb.source_url, bb.rating
        FROM business_business bb
        JOIN businesses bf ON bf.id = bb.business_from
        JOIN businesses bt ON bt.id = bb.business_to
        ORDER BY bf.name, bt.name
    """).fetchall()
    graph_json = kg_models.build_graph_json(conn)
    conn.close()

    sources = sorted(set(
        r["source_url"] for r in list(bc_links) + list(bb_links) if r["source_url"]
    ))
    return render_template(
        "index.html",
        companies=companies,
        businesses=businesses,
        bc_links=bc_links,
        bb_links=bb_links,
        graph_json=graph_json,
        active_tab=active_tab,
        sources=sources,
    )


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Tech knowledge-graph web app")
    parser.add_argument("--db",      default=str(DEFAULT_DB),      help="SQLite DB path")
    parser.add_argument("--zsxq-db", default=str(DEFAULT_ZSXQ_DB), help="zsxq.db path")
    parser.add_argument("--port", type=int, default=5001,  help="HTTP port (default 5001)")
    parser.add_argument("--host", default="0.0.0.0",       help="Bind host")
    args = parser.parse_args()

    kg_db.set_db_path(Path(args.db))
    kg_services.set_zsxq_db_path(Path(args.zsxq_db))
    kg_db.init_db(UPLOAD_DIR)
    kg_db.seed_db()

    print(f"Knowledge graph running at http://localhost:{args.port}")
    from minimax import MINIMAX_API_KEY
    key_status = "set" if MINIMAX_API_KEY else "missing — add MINIMAX_API_KEY to config.py"
    print(f"MiniMax API key: {key_status}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
