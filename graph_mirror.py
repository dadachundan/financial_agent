"""graph_mirror.py — SQLite mirror of the KuzuDB knowledge graph.

Why this exists
---------------
KuzuDB allows only one writer at a time.  While graphiti_ingest.py holds the
write lock, the Flask web server cannot open its own KuzuDB connection, causing
every web request to block (or error) until ingestion finishes.

This module maintains a lightweight SQLite shadow copy that is:
  • Written by graphiti_ingest.py after every add_episode() call
  • Read by the Flask web server (zep_app.py) for all entity/edge browsing
  • Opened in WAL mode → concurrent reads during writes, zero blocking

The mirror is *eventually consistent*: it lags the live KuzuDB by at most one
episode.  That is perfectly acceptable for a browsing/search UI.
"""

import json
import sqlite3
from pathlib import Path
from typing import Optional

# Mirror lives next to knowledge_graph/ directory
_DEFAULT_MIRROR = Path(__file__).parent / "graph_mirror.db"


# ── Connection ────────────────────────────────────────────────────────────────

def get_conn(mirror_path: Path = _DEFAULT_MIRROR) -> sqlite3.Connection:
    """Return a WAL-mode SQLite connection to the mirror DB."""
    conn = sqlite3.connect(str(mirror_path), timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


# ── Schema ────────────────────────────────────────────────────────────────────

_DDL = """
CREATE TABLE IF NOT EXISTS entities (
    uuid        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    labels_json TEXT DEFAULT '[]',
    summary     TEXT DEFAULT '',
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS edges (
    uuid        TEXT PRIMARY KEY,
    name        TEXT DEFAULT '',
    fact        TEXT DEFAULT '',
    src_uuid    TEXT DEFAULT '',
    src_name    TEXT DEFAULT '',
    tgt_uuid    TEXT DEFAULT '',
    tgt_name    TEXT DEFAULT '',
    updated_at  TEXT DEFAULT (datetime('now'))
);

-- FTS5 for entity name / summary search
CREATE VIRTUAL TABLE IF NOT EXISTS entities_fts
    USING fts5(name, summary, content='entities', content_rowid='rowid');

-- FTS5 for edge fact / name search
CREATE VIRTUAL TABLE IF NOT EXISTS edges_fts
    USING fts5(name, fact, src_name, tgt_name, content='edges', content_rowid='rowid');

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS entities_ai
    AFTER INSERT ON entities BEGIN
        INSERT INTO entities_fts(rowid, name, summary)
        VALUES (new.rowid, new.name, new.summary);
    END;

CREATE TRIGGER IF NOT EXISTS entities_au
    AFTER UPDATE ON entities BEGIN
        INSERT INTO entities_fts(entities_fts, rowid, name, summary)
        VALUES ('delete', old.rowid, old.name, old.summary);
        INSERT INTO entities_fts(rowid, name, summary)
        VALUES (new.rowid, new.name, new.summary);
    END;

CREATE TRIGGER IF NOT EXISTS edges_ai
    AFTER INSERT ON edges BEGIN
        INSERT INTO edges_fts(rowid, name, fact, src_name, tgt_name)
        VALUES (new.rowid, new.name, new.fact, new.src_name, new.tgt_name);
    END;

CREATE TRIGGER IF NOT EXISTS edges_au
    AFTER UPDATE ON edges BEGIN
        INSERT INTO edges_fts(edges_fts, rowid, name, fact, src_name, tgt_name)
        VALUES ('delete', old.rowid, old.name, old.fact, old.src_name, old.tgt_name);
        INSERT INTO edges_fts(rowid, name, fact, src_name, tgt_name)
        VALUES (new.rowid, new.name, new.fact, new.src_name, new.tgt_name);
    END;
"""


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(_DDL)
    conn.commit()


# ── Write helpers (called from graphiti_ingest.py) ────────────────────────────

def upsert_entities(conn: sqlite3.Connection, nodes: list) -> None:
    """Write/update entity nodes from a graphiti add_episode() result."""
    rows = []
    for n in nodes:
        rows.append((
            str(n.uuid),
            n.name or "",
            json.dumps(list(n.labels or [])),
            (n.summary or "")[:2000],
        ))
    if rows:
        conn.executemany(
            """INSERT INTO entities(uuid, name, labels_json, summary)
               VALUES (?,?,?,?)
               ON CONFLICT(uuid) DO UPDATE SET
                 name        = excluded.name,
                 labels_json = excluded.labels_json,
                 summary     = excluded.summary,
                 updated_at  = datetime('now')""",
            rows,
        )
        conn.commit()


def upsert_edges(conn: sqlite3.Connection, edges: list,
                 name_map: Optional[dict] = None) -> None:
    """Write/update relationship edges from a graphiti add_episode() result.

    name_map: {uuid -> name} for resolving source/target entity names.
    If not provided, src_name/tgt_name will be empty (filled later by
    the periodic reconcile, or looked up via the entities table).
    """
    if name_map is None:
        name_map = {}
    rows = []
    for e in edges:
        src_uuid = str(e.source_node_uuid or "")
        tgt_uuid = str(e.target_node_uuid or "")
        rows.append((
            str(e.uuid),
            e.name or "",
            (e.fact or "")[:4000],
            src_uuid,
            name_map.get(src_uuid, ""),
            tgt_uuid,
            name_map.get(tgt_uuid, ""),
        ))
    if rows:
        conn.executemany(
            """INSERT INTO edges(uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name)
               VALUES (?,?,?,?,?,?,?)
               ON CONFLICT(uuid) DO UPDATE SET
                 name      = excluded.name,
                 fact      = excluded.fact,
                 src_uuid  = excluded.src_uuid,
                 src_name  = CASE WHEN excluded.src_name != '' THEN excluded.src_name ELSE src_name END,
                 tgt_uuid  = excluded.tgt_uuid,
                 tgt_name  = CASE WHEN excluded.tgt_name != '' THEN excluded.tgt_name ELSE tgt_name END,
                 updated_at = datetime('now')""",
            rows,
        )
        conn.commit()


def backfill_edge_names(conn: sqlite3.Connection) -> None:
    """Fill in src_name/tgt_name for edges where name is still blank."""
    conn.execute("""
        UPDATE edges SET src_name = (
            SELECT name FROM entities WHERE uuid = edges.src_uuid
        ) WHERE src_name = '' AND src_uuid != ''
    """)
    conn.execute("""
        UPDATE edges SET tgt_name = (
            SELECT name FROM entities WHERE uuid = edges.tgt_uuid
        ) WHERE tgt_name = '' AND tgt_uuid != ''
    """)
    conn.commit()


# ── Read helpers (called from zep_app.py) ────────────────────────────────────

def get_stats(conn: sqlite3.Connection) -> dict:
    n = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    e = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    return {"node_count": n, "edge_count": e, "episode_count": 0}


def get_entities(conn: sqlite3.Connection, limit: int = 200,
                 cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
    if cursor:
        rows = conn.execute(
            "SELECT uuid, name, labels_json, summary FROM entities "
            "WHERE uuid > ? ORDER BY uuid LIMIT ?", (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT uuid, name, labels_json, summary FROM entities "
            "ORDER BY uuid LIMIT ?", (limit,)
        ).fetchall()
    items = [
        {"uuid": r["uuid"], "name": r["name"],
         "labels": json.loads(r["labels_json"] or "[]"),
         "summary": r["summary"] or ""}
        for r in rows
    ]
    next_cursor = items[-1]["uuid"] if len(items) == limit else None
    return items, next_cursor


def get_edges(conn: sqlite3.Connection, limit: int = 300,
              cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
    if cursor:
        rows = conn.execute(
            "SELECT uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name "
            "FROM edges WHERE uuid > ? ORDER BY uuid LIMIT ?", (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name "
            "FROM edges ORDER BY uuid LIMIT ?", (limit,)
        ).fetchall()
    items = [dict(r) for r in rows]
    next_cursor = items[-1]["uuid"] if len(items) == limit else None
    return items, next_cursor


def resolve_names(conn: sqlite3.Connection,
                  uuids: set[str]) -> dict[str, str]:
    """Return {uuid: name} for a set of entity UUIDs."""
    if not uuids:
        return {}
    placeholders = ",".join("?" * len(uuids))
    rows = conn.execute(
        f"SELECT uuid, name FROM entities WHERE uuid IN ({placeholders})",
        list(uuids),
    ).fetchall()
    return {r["uuid"]: r["name"] for r in rows}


def search(conn: sqlite3.Connection, query: str,
           limit: int = 30) -> dict:
    """FTS5 search across entity names/summaries and edge facts.

    Returns {"nodes": [...], "edges": [...]} in the same shape as
    zep_app's graphiti search response.
    """
    # Build a safe FTS5 query — wrap each word with * prefix wildcard
    words = [w.strip() for w in query.split() if w.strip()]
    if not words:
        return {"nodes": [], "edges": []}

    fts_query = " OR ".join(f'"{w}"*' for w in words)

    # Entity search
    try:
        entity_rows = conn.execute(
            """SELECT e.uuid, e.name, e.labels_json, e.summary,
                      bm25(entities_fts) AS score
               FROM entities_fts
               JOIN entities e ON entities_fts.rowid = e.rowid
               WHERE entities_fts MATCH ?
               ORDER BY score LIMIT ?""",
            (fts_query, limit),
        ).fetchall()
    except Exception:
        entity_rows = []

    nodes = [
        {"uuid": r["uuid"], "name": r["name"],
         "labels": json.loads(r["labels_json"] or "[]"),
         "summary": r["summary"] or "",
         "score": r["score"]}
        for r in entity_rows
    ]

    # Edge search
    try:
        edge_rows = conn.execute(
            """SELECT ed.uuid, ed.name, ed.fact,
                      ed.src_uuid, ed.src_name, ed.tgt_uuid, ed.tgt_name,
                      bm25(edges_fts) AS score
               FROM edges_fts
               JOIN edges ed ON edges_fts.rowid = ed.rowid
               WHERE edges_fts MATCH ?
               ORDER BY score LIMIT ?""",
            (fts_query, limit),
        ).fetchall()
    except Exception:
        edge_rows = []

    edges = [
        {"uuid":             r["uuid"],
         "name":             r["name"] or "",
         "fact":             r["fact"] or "",
         "source_node_uuid": r["src_uuid"],
         "source_node_name": r["src_name"] or "",
         "target_node_uuid": r["tgt_uuid"],
         "target_node_name": r["tgt_name"] or "",
         "score":            r["score"]}
        for r in edge_rows
    ]

    return {"nodes": nodes, "edges": edges, "episodes": []}
