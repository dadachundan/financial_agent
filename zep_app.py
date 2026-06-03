#!/usr/bin/env python3
"""
zep_app.py — Flask blueprint for the financial knowledge graph viewer.

**Read-only.** The viewer never writes to `db/graph_mirror.db`. All curation
goes through `manual_graph.py` (called by Claude the agent). The previous
edit / rate / merge / isolate / community-create routes were removed
2026-06-02 because the user does not curate from the UI.

Backend: SQLite at `db/graph_mirror.db` in rollback-journal mode (single
file on disk). Writes from `manual_graph` briefly block reads — the user
doesn't refresh the viewer during writes, so concurrency isn't needed.

Routes (all under /zep prefix when registered in main.py, all GET):
    /                          — Search + entity browser SPA
    /search?q=…                — FTS5 → {nodes, edges, episodes}
    /entities                  — Paginated entity list
    /edges                     — Paginated edge list
    /entities/<uuid>/edges     — Edges for one entity (click-through)
    /entities/<uuid>/community — Community this entity belongs to
    /stats                     — {node_count, edge_count, episode_count, community_count}
    /communities               — Paginated community list
    /communities/<id>          — Community detail + members
    /entities/unassigned       — Entities not in any community
    /entities/community-map    — {uuid: community_id} bulk map
"""

import json
import os
import sys
from pathlib import Path

from flask import Blueprint, current_app, render_template, render_template_string, jsonify, request
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


from db_paths import db_dir, db_path

# Honor FINAGENT_DB_DIR if set; otherwise fall back to the git-root db/.
_HONORED_ROOT = db_dir() if "FINAGENT_DB_DIR" in os.environ else (_find_project_root() / "db")
ZSXQ_DB      = _HONORED_ROOT / "zsxq.db"

import threading
import graph_mirror as _mirror

# Thread-local storage — each Flask worker thread gets its own SQLite connection.
# SQLite connections cannot be shared across threads (check_same_thread=True default).
_mirror_local = threading.local()


def _get_mirror():
    """Return a per-thread SQLite mirror connection (read-only usage)."""
    conn = getattr(_mirror_local, "conn", None)
    if conn is None:
        conn = _mirror.get_conn()
        _mirror.ensure_schema(conn)
        _mirror_local.conn = conn
    return conn


zep_bp = Blueprint(
    "zep",
    __name__,
    template_folder=str(SCRIPT_DIR / "templates"),
    static_folder=str(SCRIPT_DIR / "static"),
)


# ── Readiness ─────────────────────────────────────────────────────────────────

def _graph_ready() -> bool:
    """True iff the mirror has at least one active entity to display."""
    try:
        n = _get_mirror().execute(
            "SELECT 1 FROM entities WHERE (isolated=0 OR isolated IS NULL) LIMIT 1"
        ).fetchone()
        return n is not None
    except Exception:
        return False


# ── Routes (all GET — viewer is read-only) ────────────────────────────────────

@zep_bp.route("/")
def index():
    return render_template(
        "zep.html",
        has_key=_graph_ready(),
        nav_html=_nw2.NAV_HTML,
        url_patch_js=render_template_string(
            _nw2.URL_PATCH_JS,
            _base=current_app.config.get("ZEP_BASE", "/zep"),
        ),
    )


@zep_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    limit = min(int(request.args.get("limit", 30)), 100)

    if not query:
        return jsonify({"nodes": [], "edges": [], "episodes": []}), 200

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


@zep_bp.route("/entities/<uuid>/edges")
def entity_edges(uuid):
    """All non-deprecated edges directly connected to this entity (by UUID).
    Used when clicking a graph node — exact match, no FTS ambiguity.
    """
    edges = _mirror.get_entity_edges(_get_mirror(), uuid)
    return jsonify({"edges": edges, "uuid": uuid})


@zep_bp.route("/entities/<uuid>/community")
def entity_community(uuid):
    """Return the community this entity belongs to (or empty object if none)."""
    result = _mirror.get_entity_community(_get_mirror(), uuid)
    return jsonify(result or {})


@zep_bp.route("/stats")
def stats():
    s = _mirror.get_stats(_get_mirror())
    s["graph_exists"] = True
    return jsonify(s)


# ── Community subgraph routes (all GET) ───────────────────────────────────────

@zep_bp.route("/communities")
def communities():
    """Paginated community list, sorted by member_count DESC on first page."""
    limit  = min(int(request.args.get("limit", 100)), 500)
    cursor = request.args.get("cursor")
    cursor = int(cursor) if cursor else None
    items, next_cursor = _mirror.get_communities(_get_mirror(), limit, cursor)
    return jsonify({"communities": items, "next_cursor": next_cursor})


@zep_bp.route("/communities/<int:cid>")
def community_detail(cid: int):
    """Single community with its member entities."""
    conn = _get_mirror()
    row  = conn.execute(
        "SELECT id, name, summary, member_count FROM communities WHERE id=?", (cid,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    result            = dict(row)
    result["members"] = _mirror.get_community_members(conn, cid)
    return jsonify(result)


@zep_bp.route("/entities/unassigned")
def unassigned_entities():
    """Entities that don't belong to any community."""
    conn = _get_mirror()
    rows = conn.execute(
        "SELECT e.uuid, e.name, e.summary FROM entities e "
        "WHERE NOT EXISTS (SELECT 1 FROM community_members cm WHERE cm.entity_uuid = e.uuid) "
        "AND (e.isolated = 0 OR e.isolated IS NULL) "
        "ORDER BY e.name LIMIT 500"
    ).fetchall()
    return jsonify({"entities": [dict(r) for r in rows]})


@zep_bp.route("/entities/community-map")
def entity_community_map():
    """Return {uuid: community_id} for all assigned entities, plus community id→name map."""
    conn = _get_mirror()
    rows = conn.execute(
        "SELECT cm.entity_uuid, cm.community_id, c.name "
        "FROM community_members cm JOIN communities c ON c.id = cm.community_id"
    ).fetchall()
    entity_map = {r["entity_uuid"]: r["community_id"] for r in rows}
    comm_names = {str(r["community_id"]): r["name"] for r in rows}
    return jsonify({"entity_map": entity_map, "community_names": comm_names})


# ── Standalone entry point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from flask import Flask

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    app = Flask(__name__, template_folder=str(SCRIPT_DIR / "templates"))
    app.config["ZEP_BASE"] = ""   # standalone: no URL prefix
    app.register_blueprint(zep_bp)

    @app.context_processor
    def _inject_base():
        return dict(_base="")

    print(f"Knowledge Graph Viewer  →  http://localhost:{args.port}/  (read-only)")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
