#!/usr/bin/env python3
"""
zep_app.py — Flask blueprint for the Zep-powered knowledge graph UI.

Replaces knowledge_graph.py (SQLite KG) and rag_query.py (ChromaDB RAG).
All entity extraction and relationship discovery is handled by Zep Cloud.

Routes (all under /zep prefix when registered in main.py):
    GET  /          — Search + entity browser
    GET  /search    — JSON: {query, scope} → GraphSearchResults
    GET  /entities  — JSON: list all entity nodes (paginated)
    GET  /edges     — JSON: list all relationship edges (paginated)
    GET  /stats     — JSON: {node_count, edge_count, episode_count}
    GET  /ingest    — SSE stream: run zep_ingest for newly-added PDFs
"""

import os
import subprocess
import sys
from pathlib import Path

from flask import Blueprint, render_template, jsonify, request, Response, redirect, url_for
import nav_widget2 as _nw2

SCRIPT_DIR = Path(__file__).parent

zep_bp = Blueprint(
    "zep",
    __name__,
    template_folder=str(SCRIPT_DIR / "templates"),
    static_folder=str(SCRIPT_DIR / "static"),
)

GRAPH_ID = "financial-pdfs"

# ── Lazy Zep client ────────────────────────────────────────────────────────────

_zep_client = None


def _get_zep():
    global _zep_client
    if _zep_client is not None:
        return _zep_client

    # Load API key from config.py
    api_key = ""
    for parent in [SCRIPT_DIR] + list(SCRIPT_DIR.parents):
        cfg = parent / "config.py"
        if cfg.exists():
            ns: dict = {}
            exec(cfg.read_text(), ns)
            api_key = ns.get("ZEP_API_KEY", "")
            if api_key:
                break

    if not api_key:
        return None

    from zep_cloud.client import Zep
    _zep_client = Zep(api_key=api_key)
    return _zep_client


def _zep_ok() -> bool:
    return _get_zep() is not None


# ── Helpers ────────────────────────────────────────────────────────────────────

def _node_to_dict(node) -> dict:
    return {
        "uuid": node.uuid_,
        "name": node.name,
        "labels": node.labels or [],
        "summary": node.summary or "",
        "score": node.score,
    }


def _edge_to_dict(edge) -> dict:
    return {
        "uuid": edge.uuid_,
        "name": edge.name or "",
        "fact": edge.fact or "",
        "source_node_uuid": edge.source_node_uuid,
        "target_node_uuid": edge.target_node_uuid,
        "episodes": edge.episodes or [],
        "valid_at": str(edge.valid_at) if edge.valid_at else None,
        "score": edge.score,
    }


def _episode_to_dict(ep) -> dict:
    return {
        "uuid": ep.uuid_,
        "source_description": ep.source_description or "",
        "processed": ep.processed,
        "created_at": str(ep.created_at) if ep.created_at else None,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@zep_bp.route("/")
def index():
    has_key = _zep_ok()
    return render_template(
        "zep.html",
        has_key=has_key,
        nav_html=_nw2.NAV_HTML,
        url_patch_js=_nw2.URL_PATCH_JS,
    )


@zep_bp.route("/search")
def search():
    zep = _get_zep()
    if not zep:
        return jsonify({"error": "ZEP_API_KEY not configured"}), 503

    query = request.args.get("q", "").strip()
    scope = request.args.get("scope", "edges")   # "nodes" | "edges" | "episodes"
    limit = min(int(request.args.get("limit", 30)), 100)

    if not query:
        return jsonify({"nodes": [], "edges": [], "episodes": []}), 200

    try:
        results = zep.graph.search(
            query=query,
            graph_id=GRAPH_ID,
            scope=scope,
            limit=limit,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    nodes    = [_node_to_dict(n) for n in (results.nodes    or [])]
    edges    = [_edge_to_dict(e) for e in (results.edges    or [])]
    episodes = [_episode_to_dict(ep) for ep in (results.episodes or [])]

    return jsonify({"nodes": nodes, "edges": edges, "episodes": episodes})


@zep_bp.route("/entities")
def entities():
    zep = _get_zep()
    if not zep:
        return jsonify({"error": "ZEP_API_KEY not configured"}), 503

    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor", None)

    try:
        nodes = zep.graph.node.get_by_graph_id(
            GRAPH_ID,
            limit=limit,
            uuid_cursor=cursor or None,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "nodes":       [_node_to_dict(n) for n in nodes],
        "next_cursor": nodes[-1].uuid_ if len(nodes) == limit else None,
    })


@zep_bp.route("/edges")
def edges():
    zep = _get_zep()
    if not zep:
        return jsonify({"error": "ZEP_API_KEY not configured"}), 503

    limit  = min(int(request.args.get("limit", 200)), 500)
    cursor = request.args.get("cursor", None)

    try:
        edge_list = zep.graph.edge.get_by_graph_id(
            GRAPH_ID,
            limit=limit,
            uuid_cursor=cursor or None,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "edges":       [_edge_to_dict(e) for e in edge_list],
        "next_cursor": edge_list[-1].uuid_ if len(edge_list) == limit else None,
    })


@zep_bp.route("/stats")
def stats():
    zep = _get_zep()
    if not zep:
        return jsonify({"has_key": False})

    try:
        graph_info = zep.graph.get(graph_id=GRAPH_ID)
    except Exception:
        return jsonify({
            "has_key": True, "graph_exists": False,
            "node_count": 0, "edge_count": 0, "episode_count": 0,
        })

    try:
        nodes = zep.graph.node.get_by_graph_id(GRAPH_ID, limit=1)
        edges = zep.graph.edge.get_by_graph_id(GRAPH_ID, limit=1)
        episodes = zep.graph.episode.get_by_graph_id(GRAPH_ID)
        ep_count = len(episodes.episodes) if episodes and episodes.episodes else 0
    except Exception:
        nodes, edges, ep_count = [], [], 0

    # Get real counts by paging with large limit
    def _count_all(getter):
        total, cursor = 0, None
        while True:
            try:
                page = getter(GRAPH_ID, limit=500, uuid_cursor=cursor)
            except Exception:
                break
            if not page:
                break
            total += len(page)
            if len(page) < 500:
                break
            cursor = page[-1].uuid_
        return total

    node_count = _count_all(zep.graph.node.get_by_graph_id)
    edge_count = _count_all(zep.graph.edge.get_by_graph_id)

    return jsonify({
        "has_key":       True,
        "graph_exists":  True,
        "node_count":    node_count,
        "edge_count":    edge_count,
        "episode_count": ep_count,
    })


@zep_bp.route("/ingest")
def ingest_stream():
    """SSE stream: run zep_ingest.py for any un-indexed PDFs."""
    zep = _get_zep()
    if not zep:
        def _no_key():
            yield "data: ERROR: ZEP_API_KEY not configured in config.py\n\n"
            yield "data: done: true\n\n"
        return Response(_no_key(), mimetype="text/event-stream")

    def _gen():
        yield f"data: Starting zep_ingest.py ...\n\n"
        ingestor = SCRIPT_DIR / "zep_ingest.py"
        proc = subprocess.Popen(
            [sys.executable, "-u", str(ingestor)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        for line in proc.stdout:
            yield f"data: {line.rstrip()}\n\n"
        proc.wait()
        yield f"data: done: true\n\n"

    return Response(_gen(), mimetype="text/event-stream")


# ── Standalone entry point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    from flask import Flask
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    app = Flask(__name__, template_folder=str(SCRIPT_DIR / "templates"))
    app.register_blueprint(zep_bp)

    from nav_widget2 import nav_bp
    app.register_blueprint(nav_bp)

    @app.context_processor
    def _inject_base():
        return dict(_base="")

    print(f"Zep Knowledge Graph  →  http://localhost:{args.port}/")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
