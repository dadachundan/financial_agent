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


GRAPH_DIR = _find_project_root() / "graphiti_db"
GROUP_ID   = "financial-pdfs"

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
    return GRAPH_DIR.exists()


# ── KuzuDB direct query helpers ────────────────────────────────────────────────
# Used for /entities, /edges, /stats (browsing, not semantic search).

def _kuzu_conn():
    """Open a fresh read-only KuzuDB connection.
    Returns (conn, kdb) — caller must hold kdb reference to prevent GC.
    """
    import kuzu
    kdb  = kuzu.Database(str(GRAPH_DIR), read_only=True)
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
    return {
        "uuid":               ep.uuid,
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
        url_patch_js=render_template_string(_nw2.URL_PATCH_JS),
    )


@zep_bp.route("/search")
def search():
    if not _graph_ready():
        return jsonify({"error": "Graph not yet indexed. Run graphiti_ingest.py first."}), 503

    query = request.args.get("q", "").strip()
    limit = min(int(request.args.get("limit", 30)), 100)

    if not query:
        return jsonify({"nodes": [], "edges": [], "episodes": []}), 200

    g = _get_graphiti()
    if g is None:
        return jsonify({"error": "Could not initialise graphiti. Check logs."}), 500

    try:
        results = _run(g.search_(
            query=query,
            group_ids=[GROUP_ID],
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Limit results
    nodes    = [_node_to_dict(n)  for n in (results.nodes    or [])[:limit]]
    edges    = [_edge_to_dict(e)  for e in (results.edges    or [])[:limit]]
    episodes = [_ep_to_dict(ep)   for ep in (results.episodes or [])[:limit]]

    return jsonify({"nodes": nodes, "edges": edges, "episodes": episodes})


@zep_bp.route("/entities")
def entities():
    if not _graph_ready():
        return jsonify({"nodes": [], "next_cursor": None})

    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor") or None

    try:
        conn, _kdb = _kuzu_conn()  # hold _kdb to prevent GC
        if cursor:
            q = (f"MATCH (n:Entity) WHERE n.group_id = $gid AND n.uuid > $cursor "
                 f"RETURN n.uuid, n.name, n.summary ORDER BY n.uuid LIMIT {limit}")
            rows = _kuzu_rows(conn.execute(q, {"gid": GROUP_ID, "cursor": cursor}))
        else:
            q = (f"MATCH (n:Entity) WHERE n.group_id = $gid "
                 f"RETURN n.uuid, n.name, n.summary ORDER BY n.uuid LIMIT {limit}")
            rows = _kuzu_rows(conn.execute(q, {"gid": GROUP_ID}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    nodes = [
        {"uuid": r["n.uuid"], "name": r["n.name"] or "", "summary": r["n.summary"] or ""}
        for r in rows
    ]
    next_cursor = nodes[-1]["uuid"] if len(nodes) == limit else None
    return jsonify({"nodes": nodes, "next_cursor": next_cursor})


@zep_bp.route("/edges")
def edges():
    if not _graph_ready():
        return jsonify({"edges": [], "next_cursor": None})

    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor") or None

    try:
        conn, _kdb = _kuzu_conn()  # hold _kdb to prevent GC
        if cursor:
            q = (f"MATCH (s:Entity)-[:RELATES_TO]->(e:RelatesToNode_)-[:RELATES_TO]->(t:Entity) "
                 f"WHERE e.group_id = $gid AND e.uuid > $cursor "
                 f"RETURN e.uuid, e.name, e.fact, s.uuid AS src, t.uuid AS tgt "
                 f"ORDER BY e.uuid LIMIT {limit}")
            rows = _kuzu_rows(conn.execute(q, {"gid": GROUP_ID, "cursor": cursor}))
        else:
            q = (f"MATCH (s:Entity)-[:RELATES_TO]->(e:RelatesToNode_)-[:RELATES_TO]->(t:Entity) "
                 f"WHERE e.group_id = $gid "
                 f"RETURN e.uuid, e.name, e.fact, s.uuid AS src, t.uuid AS tgt "
                 f"ORDER BY e.uuid LIMIT {limit}")
            rows = _kuzu_rows(conn.execute(q, {"gid": GROUP_ID}))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    edge_list = [
        {
            "uuid":             r["e.uuid"],
            "name":             r["e.name"] or "",
            "fact":             r["e.fact"] or "",
            "source_node_uuid": r["src"],
            "target_node_uuid": r["tgt"],
        }
        for r in rows
    ]
    next_cursor = edge_list[-1]["uuid"] if len(edge_list) == limit else None
    return jsonify({"edges": edge_list, "next_cursor": next_cursor})


@zep_bp.route("/stats")
def stats():
    if not _graph_ready():
        return jsonify({
            "graph_exists": False,
            "node_count": 0, "edge_count": 0, "episode_count": 0,
        })

    try:
        conn, _kdb = _kuzu_conn()  # hold _kdb to prevent GC
        node_count = _kuzu_rows(
            conn.execute("MATCH (n:Entity) WHERE n.group_id = $gid RETURN count(*)",
                         {"gid": GROUP_ID})
        )[0]["COUNT_STAR()"]
        edge_count = _kuzu_rows(
            conn.execute(
                "MATCH (:Entity)-[:RELATES_TO]->(e:RelatesToNode_)-[:RELATES_TO]->(:Entity) "
                "WHERE e.group_id = $gid RETURN count(*)",
                {"gid": GROUP_ID},
            )
        )[0]["COUNT_STAR()"]
        ep_count = _kuzu_rows(
            conn.execute("MATCH (e:Episodic) WHERE e.group_id = $gid RETURN count(*)",
                         {"gid": GROUP_ID})
        )[0]["COUNT_STAR()"]
    except Exception as ex:
        return jsonify({
            "graph_exists": True,
            "node_count": 0, "edge_count": 0, "episode_count": 0,
            "error": str(ex),
        })

    return jsonify({
        "graph_exists":  True,
        "node_count":    node_count,
        "edge_count":    edge_count,
        "episode_count": ep_count,
    })


@zep_bp.route("/ingest")
def ingest_stream():
    """SSE stream: run graphiti_ingest.py for any un-indexed PDFs."""
    def _gen():
        yield "data: Starting graphiti_ingest.py ...\n\n"
        ingestor = SCRIPT_DIR / "graphiti_ingest.py"
        proc = subprocess.Popen(
            [sys.executable, "-u", str(ingestor)],
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
