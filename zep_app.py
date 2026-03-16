#!/usr/bin/env python3
"""
zep_app.py — Flask blueprint for the graphiti-core knowledge graph UI.

Backend: local graphiti-core (KuzuDB + bge-m3 + MiniMax).
No cloud dependencies — the full graph lives in ./graphiti_db/.

Routes (all under /zep prefix when registered in main.py):
    GET  /          — Search + entity browser
    GET  /search    — JSON: {query} → {nodes, edges, episodes}
    GET  /entities  — JSON: list all entity nodes (paginated via KuzuDB)
    GET  /edges     — JSON: list all relationship edges (paginated via KuzuDB)
    GET  /stats     — JSON: {node_count, edge_count, episode_count}
    GET  /ingest        — SSE stream: run graphiti_ingest.py for newly-added PDFs
    POST /upload-pdf    — SSE stream: accept PDF upload and index it directly
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, render_template, render_template_string, jsonify, request, Response
import nav_widget2 as _nw2

SCRIPT_DIR = Path(__file__).parent


def _find_project_root() -> Path:
    """Return the main git repo root, even when running from a worktree."""
    p = SCRIPT_DIR.resolve()
    while p != p.parent:
        git = p / ".git"
        if git.exists() and git.is_dir():
            return p
        p = p.parent
    return SCRIPT_DIR


GRAPH_DIR    = _find_project_root() / "db" / "graphiti_db"
ZSXQ_DB      = _find_project_root() / "db" / "zsxq.db"
GROUP_ID     = "financial-pdfs"
# SQLite mirror — always readable, even while ingest holds the KuzuDB write lock
import threading
import graph_mirror as _mirror

# Thread-local storage — each Flask worker thread gets its own SQLite connection.
# SQLite connections cannot be shared across threads (check_same_thread=True default).
_mirror_local    = threading.local()
_mirror_backfill_done = False          # run backfill at most once per process


def _get_mirror():
    """Return a per-thread SQLite mirror connection, backfilling once on first use."""
    global _mirror_backfill_done
    conn = getattr(_mirror_local, "conn", None)
    if conn is None:
        conn = _mirror.get_conn()
        _mirror.ensure_schema(conn)
        _mirror_local.conn = conn

    # One-time backfill from KuzuDB if mirror looks empty (first run / upgrade)
    if not _mirror_backfill_done:
        _mirror_backfill_done = True   # set early to prevent re-entry on concurrent req
        n_ent = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        n_ep  = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
        if (n_ent == 0 or n_ep == 0) and GRAPH_DIR.exists():
            print("[mirror] incomplete — backfilling from KuzuDB …", flush=True)
            # Reuse graphiti's existing kuzu.Database object to avoid exclusive-lock conflict
            existing_kuzu_conn = None
            try:
                import kuzu as _kuzu
                g = _get_graphiti()
                if g is not None and hasattr(g, "graph_driver") and \
                        hasattr(g.graph_driver, "db"):
                    existing_kuzu_conn = _kuzu.Connection(g.graph_driver.db)
            except Exception:
                pass
            ne, ned = _mirror.backfill_from_kuzu(
                conn, GRAPH_DIR, GROUP_ID, kuzu_conn=existing_kuzu_conn
            )
            print(f"[mirror] backfill done: {ne} entities, {ned} edges", flush=True)
    return conn


zep_bp = Blueprint(
    "zep",
    __name__,
    template_folder=str(SCRIPT_DIR / "templates"),
    static_folder=str(SCRIPT_DIR / "static"),
)


# ── Async ↔ sync bridge ────────────────────────────────────────────────────────

def _run(coro):
    """Run an async coroutine from a synchronous Flask route."""
    return asyncio.run(coro)


# ── Lazy graphiti singleton ────────────────────────────────────────────────────

_graphiti = None


def _get_graphiti():
    global _graphiti
    if _graphiti is None:
        if not GRAPH_DIR.exists():
            return None   # not yet indexed
        try:
            from minimax_llm_client import get_graphiti
            _graphiti = get_graphiti()
        except Exception:
            return None
    return _graphiti


def _graph_ready() -> bool:
    return GRAPH_DIR.exists() and GRAPH_DIR.stat().st_size > 4096


# ── KuzuDB direct query helpers ────────────────────────────────────────────────
# Used for /entities, /edges, /stats (browsing, not semantic search).

def _kuzu_conn():
    """Return a KuzuDB connection that shares the graphiti instance's Database object.

    Opening a second kuzu.Database in read-only mode fails with a shadow-pages
    error whenever the graphiti instance (write mode) is also open.  Reusing the
    same kuzu.Database avoids that conflict entirely.
    Returns (conn, kdb) — caller must hold kdb reference to prevent GC.
    """
    import kuzu
    g = _get_graphiti()
    if g is not None and hasattr(g, "graph_driver") and hasattr(g.graph_driver, "db"):
        kdb  = g.graph_driver.db
        conn = kuzu.Connection(kdb)
        return conn, kdb
    # Fallback: graphiti not yet initialised — open our own read-write connection.
    kdb  = kuzu.Database(str(GRAPH_DIR))
    conn = kuzu.Connection(kdb)
    return conn, kdb


def _kuzu_rows(result) -> list[dict]:
    """Convert a kuzu QueryResult into a list of plain dicts."""
    rows = []
    col_names = result.get_column_names()
    while result.has_next():
        row = result.get_next()
        rows.append(dict(zip(col_names, row)))
    return rows


# ── Serialisers ────────────────────────────────────────────────────────────────

def _node_to_dict(node) -> dict:
    """Serialise a graphiti EntityNode."""
    return {
        "uuid":    node.uuid,
        "name":    node.name or "",
        "labels":  node.labels or [],
        "summary": node.summary or "",
        "score":   getattr(node, "score", None),
    }


def _edge_to_dict(edge) -> dict:
    """Serialise a graphiti EntityEdge."""
    return {
        "uuid":             edge.uuid,
        "name":             edge.name or "",
        "fact":             edge.fact or "",
        "source_node_uuid": edge.source_node_uuid or "",
        "target_node_uuid": edge.target_node_uuid or "",
        "valid_at":         str(edge.valid_at) if getattr(edge, "valid_at", None) else None,
        "score":            getattr(edge, "score", None),
    }


def _ep_to_dict(ep) -> dict:
    """Serialise a graphiti EpisodicNode."""
    name = getattr(ep, "name", "") or ""
    # "pdf_{file_id}"  → ZSXQ PDF  (/zsxq/pdf/<file_id>)
    # "report_{id}"    → SEC filing (/sec/file/<id>)
    file_id   = None
    report_id = None
    if name.startswith("pdf_"):
        try:
            file_id = int(name[4:])
        except ValueError:
            pass
    elif name.startswith("report_"):
        try:
            report_id = int(name[7:])
        except ValueError:
            pass
    return {
        "uuid":               ep.uuid,
        "name":               name,
        "file_id":            file_id,
        "report_id":          report_id,
        "source_description": getattr(ep, "source_description", "") or "",
        "created_at":         str(ep.created_at) if getattr(ep, "created_at", None) else None,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@zep_bp.route("/")
def index():
    return render_template(
        "zep.html",
        has_key=_graph_ready(),
        nav_html=_nw2.NAV_HTML,
        url_patch_js=render_template_string(_nw2.URL_PATCH_JS, _base="/zep"),
    )


@zep_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    limit = min(int(request.args.get("limit", 30)), 100)

    if not query:
        return jsonify({"nodes": [], "edges": [], "episodes": []}), 200

    # Try graphiti semantic search first (vector-ranked); fall back to SQLite FTS
    # if KuzuDB is locked by the ingestor (non-blocking for the web server).
    g = _get_graphiti()
    if g is not None:
        try:
            results = _run(g.search_(query=query, group_ids=[GROUP_ID]))
            nodes    = [_node_to_dict(n)  for n in (results.nodes    or [])[:limit]]
            edges    = [_edge_to_dict(e)  for e in (results.edges    or [])[:limit]]
            episodes = [_ep_to_dict(ep)   for ep in (results.episodes or [])[:limit]]
            # Resolve missing edge endpoint names via mirror (never blocks)
            missing_uuids = set()
            for e in edges:
                if e["source_node_uuid"]: missing_uuids.add(e["source_node_uuid"])
                if e["target_node_uuid"]: missing_uuids.add(e["target_node_uuid"])
            uuid_to_name = {n["uuid"]: n["name"] for n in nodes}
            missing_uuids -= set(uuid_to_name)
            if missing_uuids:
                uuid_to_name.update(_mirror.resolve_names(_get_mirror(), missing_uuids))
            for e in edges:
                e["source_node_name"] = uuid_to_name.get(e["source_node_uuid"], "")
                e["target_node_name"] = uuid_to_name.get(e["target_node_uuid"], "")
            return jsonify({"nodes": nodes, "edges": edges, "episodes": episodes,
                            "_source": "graphiti"})
        except Exception as _ge:
            print(f"[search] graphiti unavailable ({_ge}); falling back to mirror FTS",
                  file=sys.stderr)

    # Mirror FTS fallback — always available, even during ingestion
    result = _mirror.search(_get_mirror(), query, limit)
    result["_source"] = "mirror-fts"
    return jsonify(result)


@zep_bp.route("/entities")
def entities():
    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor") or None
    nodes, next_cursor = _mirror.get_entities(_get_mirror(), limit, cursor)
    return jsonify({"nodes": nodes, "next_cursor": next_cursor})


@zep_bp.route("/edges")
def edges():
    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor") or None
    edge_list, next_cursor = _mirror.get_edges(_get_mirror(), limit, cursor)
    # Rename mirror fields to match the API shape the frontend expects
    for e in edge_list:
        e["source_node_uuid"] = e.pop("src_uuid", "")
        e["source_node_name"] = e.pop("src_name", "")
        e["target_node_uuid"] = e.pop("tgt_uuid", "")
        e["target_node_name"] = e.pop("tgt_name", "")
    return jsonify({"edges": edge_list, "next_cursor": next_cursor})


@zep_bp.route("/stats")
def stats():
    s = _mirror.get_stats(_get_mirror())
    s["graph_exists"] = True
    return jsonify(s)


@zep_bp.route("/ingest")
def ingest_stream():
    """SSE stream: run graphiti_ingest.py for any un-indexed PDFs and SEC filings."""
    def _gen():
        yield "data: Starting graphiti_ingest.py ...\n\n"
        ingestor = SCRIPT_DIR / "ingest" / "graphiti_ingest.py"
        proc = subprocess.Popen(
            [sys.executable, "-u", str(ingestor),
             "--source", "all", "--form-type", "10-K", "10-Q"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        for line in proc.stdout:
            yield f"data: {line.rstrip()}\n\n"
        proc.wait()
        # Reset the singleton so it reloads the updated graph
        global _graphiti
        _graphiti = None
        yield "data: done: true\n\n"

    return Response(_gen(), mimetype="text/event-stream")


@zep_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    """Accept a PDF upload and index it into graphiti (SSE stream response)."""
    import pdfplumber

    f = request.files.get("pdf")
    if f is None or not f.filename:
        return jsonify({"error": "No PDF file provided"}), 400

    orig_name = f.filename

    # Save to temp file before entering the generator (request data is consumed here)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    f.save(tmp.name)
    tmp.close()
    tmp_path = Path(tmp.name)

    def _gen():
        yield f"data: Received: {orig_name}\n\n"
        yield "data: Extracting text…\n\n"
        try:
            pages = []
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        pages.append(t.strip())
            text = "\n\n".join(pages)[:80_000]
        except Exception as e:
            yield f"data: ✗ Text extraction failed: {e}\n\n"
            yield "data: done: true\n\n"
            tmp_path.unlink(missing_ok=True)
            return

        if len(text) < 200:
            yield "data: ⚠  No extractable text (image-only or DRM PDF)\n\n"
            yield "data: done: true\n\n"
            tmp_path.unlink(missing_ok=True)
            return

        yield f"data: {len(text):,} chars extracted. Indexing…\n\n"

        try:
            global _graphiti
            g = _get_graphiti()
            if g is None:
                from minimax_llm_client import get_graphiti as _gg
                _graphiti = _gg()
                g = _graphiti

            result = asyncio.run(g.add_episode(
                name=f"upload_{Path(orig_name).stem}",
                episode_body=text,
                source_description=f"PDF: {orig_name}",
                reference_time=datetime.now(timezone.utc),
                group_id=GROUP_ID,
            ))
            n_nodes = len(result.nodes)
            n_edges = len(result.edges)
            _graphiti = None  # reset so next read sees updated graph
            yield f"data: ✓ Done — {n_nodes} entities, {n_edges} relationships extracted\n\n"
        except Exception as e:
            yield f"data: ✗ Indexing error: {e}\n\n"
        finally:
            tmp_path.unlink(missing_ok=True)

        yield "data: done: true\n\n"

    return Response(_gen(), mimetype="text/event-stream")


@zep_bp.route("/clear", methods=["POST"])
def clear_graph():
    """Delete graphiti_db and reset graphiti_indexed_at in zsxq.db."""
    import sqlite3

    global _graphiti
    _graphiti = None  # drop the in-process singleton

    errors = []

    # 1. Delete the graph DB files (main + WAL)
    try:
        GRAPH_DIR.unlink(missing_ok=True)
        Path(str(GRAPH_DIR) + ".wal").unlink(missing_ok=True)
    except Exception as e:
        errors.append(f"Could not delete graph DB: {e}")

    # 2. Reset indexed timestamps so all PDFs queue for re-indexing
    try:
        if ZSXQ_DB.exists():
            conn = sqlite3.connect(ZSXQ_DB)
            conn.execute("UPDATE pdf_files SET graphiti_indexed_at = NULL")
            conn.commit()
            conn.close()
    except Exception as e:
        errors.append(f"Could not reset zsxq.db: {e}")

    if errors:
        return jsonify({"ok": False, "errors": errors}), 500
    return jsonify({"ok": True})


# LLM log routes removed — monitoring moved to Langfuse cloud.


# ── Standalone entry point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from flask import Flask

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    app = Flask(__name__, template_folder=str(SCRIPT_DIR / "templates"))
    app.register_blueprint(zep_bp)

    @app.context_processor
    def _inject_base():
        return dict(_base="")

    print(f"Graphiti Knowledge Graph  →  http://localhost:{args.port}/")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
