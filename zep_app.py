#!/usr/bin/env python3
"""
zep_app.py — Flask blueprint for the financial knowledge graph viewer.

Backend: SQLite at db/graph_mirror.db (single source of truth).
Entities and edges are curated by Claude (the agent) via manual_graph.py;
there is no automated ingest pipeline and no graph DB beyond SQLite.

Routes (all under /zep prefix when registered in main.py):
    GET  /          — Search + entity browser
    GET  /search    — JSON: {query} → {nodes, edges, episodes}   (FTS5)
    GET  /entities  — JSON: list all entity nodes (paginated)
    GET  /edges     — JSON: list all relationship edges (paginated)
    GET  /stats     — JSON: {node_count, edge_count, episode_count, community_count}
    GET  /communities         — JSON: paginated community list
    GET  /communities/<id>    — JSON: community detail + members
    POST /build-communities   — SSE stream: label-propagation (no LLM)
    GET  /ingest, POST /upload-pdf, /entities/isolate-persons,
    POST /refresh-mirror, POST /clear                            — 410 Gone
"""

import json
import os
import sys
from pathlib import Path

from flask import Blueprint, current_app, render_template, render_template_string, jsonify, request, Response
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
# _find_project_root() (above) walks up to .git so worktrees share data;
# db_dir() lets tests redirect everything to /tmp/.
_HONORED_ROOT = db_dir() if "FINAGENT_DB_DIR" in os.environ else (_find_project_root() / "db")
ZSXQ_DB      = _HONORED_ROOT / "zsxq.db"

import threading
import graph_mirror as _mirror

# Thread-local storage — each Flask worker thread gets its own SQLite connection.
# SQLite connections cannot be shared across threads (check_same_thread=True default).
_mirror_local = threading.local()


def _get_mirror():
    """Return a per-thread SQLite mirror connection."""
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


# ── Routes ─────────────────────────────────────────────────────────────────────

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

    # Mirror FTS is the primary search — exact and prefix matching is reliable for
    # entity names, ticker symbols, hyphenated terms (COVID-19), and fact text.
    # Graphiti vector search is only tried as a fallback when FTS finds nothing
    # (handles purely semantic / concept queries that have no literal text match).
    result = _mirror.search(_get_mirror(), query, limit)
    if result["nodes"] or result["edges"] or result["episodes"]:
        result["_source"] = "mirror-fts"
        return jsonify(result)

    # Mirror FTS is the only search backend; graphiti semantic fallback removed.
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


@zep_bp.route("/edges/<uuid>/deprecate", methods=["POST"])
def deprecate_edge(uuid):
    """Mark a relationship as deprecated in the mirror."""
    body   = request.get_json(silent=True) or {}
    reason = (body.get("reason") or "RELATION_NONSENSE").strip()[:200]
    found  = _mirror.deprecate_edge(_get_mirror(), uuid, reason)
    if not found:
        return jsonify({"ok": False, "error": "edge not found"}), 404
    return jsonify({"ok": True, "uuid": uuid, "reason": reason})


@zep_bp.route("/entities/<uuid>/rate", methods=["POST"])
def rate_entity(uuid):
    """Set a star rating (0–5) on an entity in the mirror."""
    body   = request.get_json(silent=True) or {}
    rating = max(0, min(5, int(body.get("rating", 0))))
    found  = _mirror.rate_entity(_get_mirror(), uuid, rating)
    if not found:
        return jsonify({"ok": False, "error": "entity not found"}), 404
    return jsonify({"ok": True, "uuid": uuid, "rating": rating})


@zep_bp.route("/entities/<uuid>", methods=["PATCH"])
def edit_entity(uuid):
    """Update entity name and summary in the mirror."""
    body    = request.get_json(silent=True) or {}
    name    = body.get("name", "").strip()
    summary = body.get("summary", "").strip()
    if not name:
        return jsonify({"ok": False, "error": "name is required"}), 400

    found = _mirror.update_entity(_get_mirror(), uuid, name, summary)
    if not found:
        return jsonify({"ok": False, "error": "entity not found"}), 404
    return jsonify({"ok": True, "uuid": uuid, "name": name, "summary": summary})


@zep_bp.route("/edges/<uuid>", methods=["PATCH"])
def edit_edge(uuid):
    """Update edge relation name and fact in the mirror."""
    body = request.get_json(silent=True) or {}
    name = body.get("name", "").strip()
    fact = body.get("fact", "").strip()
    if not fact:
        return jsonify({"ok": False, "error": "fact is required"}), 400

    found = _mirror.update_edge(_get_mirror(), uuid, name, fact)
    if not found:
        return jsonify({"ok": False, "error": "edge not found"}), 404
    return jsonify({"ok": True, "uuid": uuid, "name": name, "fact": fact})


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


@zep_bp.route("/entities/merge", methods=["POST"])
def merge_entities_ep():
    """Merge source entity into target: re-point all edges, delete source."""
    body = request.get_json(silent=True) or {}
    src  = (body.get("source_uuid") or "").strip()
    tgt  = (body.get("target_uuid") or "").strip()
    if not src or not tgt:
        return jsonify({"ok": False, "error": "source_uuid and target_uuid required"}), 400
    if src == tgt:
        return jsonify({"ok": False, "error": "source and target must be different"}), 400
    try:
        result = _mirror.merge_entities(_get_mirror(), src, tgt)
        return jsonify({"ok": True, **result})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@zep_bp.route("/edges", methods=["POST"])
def create_edge_ep():
    """Create a manual edge between two entities."""
    import uuid as _uuid_mod
    body     = request.get_json(silent=True) or {}
    src_uuid = (body.get("source_uuid") or "").strip()
    tgt_uuid = (body.get("target_uuid") or "").strip()
    name     = (body.get("name") or "RELATES_TO").strip()
    fact     = (body.get("fact") or "").strip()
    src_name = (body.get("source_name") or "").strip()
    tgt_name = (body.get("target_name") or "").strip()
    if not src_uuid or not tgt_uuid:
        return jsonify({"ok": False, "error": "source_uuid and target_uuid required"}), 400
    edge_uuid = str(_uuid_mod.uuid4())
    result = _mirror.add_edge(_get_mirror(), edge_uuid,
                              src_uuid, src_name, tgt_uuid, tgt_name, name, fact)
    return jsonify({"ok": True, **result})


@zep_bp.route("/entities/<uuid>/isolate", methods=["POST"])
def isolate_entity(uuid):
    """Mark an entity as isolated in the mirror."""
    found = _mirror.isolate_entity(_get_mirror(), uuid)
    if not found:
        return jsonify({"ok": False, "error": "entity not found"}), 404
    return jsonify({"ok": True, "uuid": uuid})


@zep_bp.route("/stats")
def stats():
    s = _mirror.get_stats(_get_mirror())
    s["graph_exists"] = True
    return jsonify(s)


@zep_bp.route("/ingest")
def ingest_stream():
    """Removed — automatic ingest is gone. Curate the graph via manual_graph.py."""
    return jsonify({
        "error": "Automatic ingest has been removed. Add entities and edges "
                 "manually via manual_graph.add_entity / add_edge."
    }), 410


@zep_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    """Removed — PDF auto-extraction is gone. Read the source manually."""
    return jsonify({
        "error": "PDF auto-extraction has been removed. Read the document "
                 "yourself and curate entities via manual_graph.py."
    }), 410


@zep_bp.route("/refresh-mirror", methods=["POST"])
def refresh_mirror():
    """Removed — there is no upstream KuzuDB to backfill from anymore."""
    return jsonify({
        "error": "refresh-mirror has been removed. The SQLite mirror is the "
                 "single source of truth."
    }), 410


@zep_bp.route("/entities/isolate-persons", methods=["POST"])
def isolate_persons():
    """Removed — bulk LLM-based person isolation is gone.

    Use the per-entity isolate button in the UI, or call
    `_mirror.isolate_entity(conn, uuid)` from a curated script.
    """
    return jsonify({
        "error": "Bulk auto-isolation has been removed. Isolate persons "
                 "manually via the UI or graph_mirror.isolate_entity()."
    }), 410


@zep_bp.route("/clear", methods=["POST"])
def clear_graph():
    """Removed — bulk-clearing the graph is no longer supported.

    The legacy KuzuDB store is left intact; delete files manually if needed.
    The SQLite mirror is the source of truth — clear it with SQL.
    """
    return jsonify({
        "error": "Bulk clear has been removed. Manage the graph directly via "
                 "graph_mirror.* or by editing db/graph_mirror.db."
    }), 410


# LLM log routes removed — monitoring moved to Langfuse cloud.


# ── Community subgraph routes ──────────────────────────────────────────────────

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


@zep_bp.route("/communities/<int:cid>/members", methods=["POST"])
def add_community_member(cid: int):
    """BFS-flood from seed_uuid into an existing community."""
    body = request.get_json(silent=True) or {}
    seed = (body.get("seed_uuid") or "").strip()
    if not seed:
        return jsonify({"ok": False, "error": "seed_uuid required"}), 400
    try:
        result = _mirror.add_to_community_from_seed(_get_mirror(), cid, seed)
        return jsonify({"ok": True, **result})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@zep_bp.route("/communities/<int:cid>/members/<uuid>", methods=["DELETE"])
def remove_community_member(cid: int, uuid: str):
    """BFS flood-fill removal: remove entity and all connected entities from community cid."""
    conn = _get_mirror()
    # Verify community exists
    row = conn.execute("SELECT id FROM communities WHERE id=?", (cid,)).fetchone()
    if row is None:
        return jsonify({"ok": False, "error": "community not found"}), 404
    removed = _mirror.remove_community_bfs(conn, cid, uuid)
    return jsonify({"ok": True, "removed": removed})


@zep_bp.route("/communities/<int:cid>", methods=["DELETE"])
def delete_community(cid: int):
    """Delete a community and unassign all its members."""
    conn = _get_mirror()
    row = conn.execute("SELECT id FROM communities WHERE id=?", (cid,)).fetchone()
    if row is None:
        return jsonify({"ok": False, "error": "not found"}), 404
    conn.execute("DELETE FROM communities WHERE id=?", (cid,))
    conn.commit()
    return jsonify({"ok": True})


@zep_bp.route("/communities/bulk-delete-singletons", methods=["DELETE"])
def delete_singleton_communities():
    """Delete all communities with member_count <= 1."""
    conn = _get_mirror()
    count = conn.execute(
        "SELECT COUNT(*) FROM communities WHERE member_count <= 1"
    ).fetchone()[0]
    conn.execute("DELETE FROM communities WHERE member_count <= 1")
    conn.commit()
    return jsonify({"ok": True, "deleted": count})


@zep_bp.route("/entities/community-map")
def entity_community_map():
    """Return {uuid: community_id} for all assigned entities, plus community id→name map."""
    conn = _get_mirror()
    rows = conn.execute(
        "SELECT cm.entity_uuid, cm.community_id, c.name "
        "FROM community_members cm JOIN communities c ON c.id = cm.community_id"
    ).fetchall()
    entity_map = {r["entity_uuid"]: r["community_id"] for r in rows}
    comm_names = {}
    for r in rows:
        comm_names[str(r["community_id"])] = r["name"]
    return jsonify({"entity_map": entity_map, "community_names": comm_names})


@zep_bp.route("/communities", methods=["POST"])
def create_community():
    """Create a community seeded by one entity; BFS assigns all connected entities."""
    body = request.get_json(silent=True) or {}
    name = (body.get("name") or "").strip()[:200]
    seed = (body.get("seed_uuid") or "").strip()
    if not name:
        return jsonify({"ok": False, "error": "name required"}), 400
    if not seed:
        return jsonify({"ok": False, "error": "seed_uuid required"}), 400
    result = _mirror.create_community_from_seed(_get_mirror(), name, seed)
    return jsonify({"ok": True, **result})


@zep_bp.route("/build-communities", methods=["POST"])
def build_communities_stream():
    """SSE stream: run full label propagation + LLM community summaries."""
    def _gen():
        # Use a dedicated connection (not the thread-local one) so the large
        # DELETE + INSERT batch doesn't interfere with concurrent reads.
        conn = _mirror.get_conn()
        _mirror.ensure_schema(conn)
        try:
            for msg in _mirror.build_communities(conn):
                yield f"data: {msg}\n\n"
        except Exception as exc:
            yield f"data: ERROR: {exc}\n\n"
        finally:
            conn.close()
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
    app.config["ZEP_BASE"] = ""   # standalone: no URL prefix
    app.register_blueprint(zep_bp)

    @app.context_processor
    def _inject_base():
        return dict(_base="")

    print(f"Graphiti Knowledge Graph  →  http://localhost:{args.port}/")
    app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
