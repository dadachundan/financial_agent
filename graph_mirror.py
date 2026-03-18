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
import random
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

# Mirror lives next to knowledge_graph/ directory
_DEFAULT_MIRROR = Path(__file__).parent / "db" / "graph_mirror.db"


# ── Connection ────────────────────────────────────────────────────────────────

def get_conn(mirror_path: Path = _DEFAULT_MIRROR) -> sqlite3.Connection:
    """Return a WAL-mode SQLite connection to the mirror DB."""
    mirror_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(mirror_path), timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


# ── Schema ────────────────────────────────────────────────────────────────────

_DDL = """
CREATE TABLE IF NOT EXISTS episodes (
    uuid        TEXT PRIMARY KEY,
    name        TEXT DEFAULT '',
    source_desc TEXT DEFAULT '',
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS entities (
    uuid        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    labels_json TEXT DEFAULT '[]',
    summary     TEXT DEFAULT '',
    isolated    INTEGER DEFAULT 0,
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS edges (
    uuid            TEXT PRIMARY KEY,
    name            TEXT DEFAULT '',
    fact            TEXT DEFAULT '',
    src_uuid        TEXT DEFAULT '',
    src_name        TEXT DEFAULT '',
    tgt_uuid        TEXT DEFAULT '',
    tgt_name        TEXT DEFAULT '',
    episodes_json   TEXT DEFAULT '[]',
    deprecated      INTEGER DEFAULT 0,
    deprecated_reason TEXT DEFAULT '',
    updated_at      TEXT DEFAULT (datetime('now'))
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

-- ── Community subgraph (Zep paper §3) ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS communities (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL DEFAULT '',
    summary      TEXT    NOT NULL DEFAULT '',
    member_count INTEGER NOT NULL DEFAULT 0,
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS community_members (
    entity_uuid  TEXT    NOT NULL,
    community_id INTEGER NOT NULL,
    PRIMARY KEY (entity_uuid),
    FOREIGN KEY (entity_uuid)  REFERENCES entities(uuid)  ON DELETE CASCADE,
    FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_cm_cid ON community_members(community_id);

CREATE VIRTUAL TABLE IF NOT EXISTS communities_fts
    USING fts5(name, summary, content='communities', content_rowid='rowid');

CREATE TRIGGER IF NOT EXISTS communities_ai
    AFTER INSERT ON communities BEGIN
        INSERT INTO communities_fts(rowid, name, summary)
        VALUES (new.rowid, new.name, new.summary);
    END;

CREATE TRIGGER IF NOT EXISTS communities_au
    AFTER UPDATE ON communities BEGIN
        INSERT INTO communities_fts(communities_fts, rowid, name, summary)
        VALUES ('delete', old.rowid, old.name, old.summary);
        INSERT INTO communities_fts(rowid, name, summary)
        VALUES (new.rowid, new.name, new.summary);
    END;
"""


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(_DDL)
    # Migrate existing DBs: add columns if absent
    existing_edges = {r[1] for r in conn.execute("PRAGMA table_info(edges)").fetchall()}
    if "episodes_json" not in existing_edges:
        conn.execute("ALTER TABLE edges ADD COLUMN episodes_json TEXT DEFAULT '[]'")
    if "deprecated" not in existing_edges:
        conn.execute("ALTER TABLE edges ADD COLUMN deprecated INTEGER DEFAULT 0")
    if "deprecated_reason" not in existing_edges:
        conn.execute("ALTER TABLE edges ADD COLUMN deprecated_reason TEXT DEFAULT ''")
    existing_ent = {r[1] for r in conn.execute("PRAGMA table_info(entities)").fetchall()}
    if "isolated" not in existing_ent:
        conn.execute("ALTER TABLE entities ADD COLUMN isolated INTEGER DEFAULT 0")
    if "rating" not in existing_ent:
        conn.execute("ALTER TABLE entities ADD COLUMN rating INTEGER DEFAULT 0")
    # Pending-deletions queue (for ops attempted while ingest holds the Kuzu lock)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pending_deletions (
            uuid       TEXT NOT NULL,
            type       TEXT NOT NULL CHECK(type IN ('edge', 'entity')),
            reason     TEXT NOT NULL DEFAULT '',
            queued_at  TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()


def queue_deletion(conn: sqlite3.Connection, uuid: str, type_: str, reason: str = "") -> None:
    """Queue a Kuzu deletion to be applied once ingest releases the write lock."""
    conn.execute(
        "INSERT INTO pending_deletions (uuid, type, reason) VALUES (?, ?, ?)",
        (uuid, type_, reason),
    )
    conn.commit()


def drain_pending_deletions(conn: sqlite3.Connection) -> list:
    """Return all queued deletions and clear the table."""
    rows = conn.execute(
        "SELECT uuid, type, reason FROM pending_deletions ORDER BY rowid"
    ).fetchall()
    conn.execute("DELETE FROM pending_deletions")
    conn.commit()
    return rows


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
        ep_list  = getattr(e, "episodes", None) or []
        ep_json  = json.dumps([str(u) for u in ep_list])
        rows.append((
            str(e.uuid),
            e.name or "",
            (e.fact or "")[:4000],
            src_uuid,
            name_map.get(src_uuid, ""),
            tgt_uuid,
            name_map.get(tgt_uuid, ""),
            ep_json,
        ))
    if rows:
        conn.executemany(
            """INSERT INTO edges(uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name, episodes_json)
               VALUES (?,?,?,?,?,?,?,?)
               ON CONFLICT(uuid) DO UPDATE SET
                 name          = excluded.name,
                 fact          = excluded.fact,
                 src_uuid      = excluded.src_uuid,
                 src_name      = CASE WHEN excluded.src_name != '' THEN excluded.src_name ELSE src_name END,
                 tgt_uuid      = excluded.tgt_uuid,
                 tgt_name      = CASE WHEN excluded.tgt_name != '' THEN excluded.tgt_name ELSE tgt_name END,
                 episodes_json = CASE WHEN excluded.episodes_json != '[]' THEN excluded.episodes_json ELSE episodes_json END,
                 updated_at    = datetime('now')""",
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

def upsert_episode(conn: sqlite3.Connection, episode) -> None:
    conn.execute(
        """INSERT INTO episodes(uuid, name, source_desc)
           VALUES (?,?,?)
           ON CONFLICT(uuid) DO NOTHING""",
        (str(episode.uuid), getattr(episode, "name", "") or "",
         getattr(episode, "source_description", "") or ""),
    )
    conn.commit()


def get_stats(conn: sqlite3.Connection) -> dict:
    n  = conn.execute("SELECT COUNT(*) FROM entities WHERE (isolated=0 OR isolated IS NULL)").fetchone()[0]
    e  = conn.execute("SELECT COUNT(*) FROM edges WHERE (deprecated=0 OR deprecated IS NULL)").fetchone()[0]
    ep = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
    c  = conn.execute("SELECT COUNT(*) FROM communities").fetchone()[0]
    return {"node_count": n, "edge_count": e, "episode_count": ep, "community_count": c}


def get_entities(conn: sqlite3.Connection, limit: int = 200,
                 cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
    if cursor:
        rows = conn.execute(
            "SELECT uuid, name, labels_json, summary, rating FROM entities "
            "WHERE uuid > ? AND (isolated=0 OR isolated IS NULL) ORDER BY uuid LIMIT ?",
            (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT uuid, name, labels_json, summary, rating FROM entities "
            "WHERE (isolated=0 OR isolated IS NULL) ORDER BY uuid LIMIT ?", (limit,)
        ).fetchall()
    items = [
        {"uuid": r["uuid"], "name": r["name"],
         "labels": json.loads(r["labels_json"] or "[]"),
         "summary": r["summary"] or "",
         "rating": r["rating"] or 0}
        for r in rows
    ]
    next_cursor = items[-1]["uuid"] if len(items) == limit else None
    return items, next_cursor


def rate_entity(conn: sqlite3.Connection, uuid: str, rating: int) -> bool:
    """Set a 1-5 star rating on an entity (0 = unrated). Returns True if found."""
    rating = max(0, min(5, rating))
    cur = conn.execute(
        "UPDATE entities SET rating=?, updated_at=datetime('now') WHERE uuid=?",
        (rating, uuid),
    )
    conn.commit()
    return cur.rowcount > 0


def update_entity(conn: sqlite3.Connection, uuid: str,
                  name: str, summary: str) -> bool:
    """Update entity name and summary. Returns True if found."""
    cur = conn.execute(
        "UPDATE entities SET name=?, summary=?, updated_at=datetime('now') WHERE uuid=?",
        (name.strip(), summary.strip(), uuid),
    )
    conn.commit()
    return cur.rowcount > 0


def update_edge(conn: sqlite3.Connection, uuid: str,
                name: str, fact: str) -> bool:
    """Update edge relation name and fact. Returns True if found."""
    cur = conn.execute(
        "UPDATE edges SET name=?, fact=?, updated_at=datetime('now') WHERE uuid=?",
        (name.strip(), fact.strip(), uuid),
    )
    conn.commit()
    return cur.rowcount > 0


def _episode_url(name: str) -> Optional[str]:
    """Convert episode name → viewer URL, or None if unknown format."""
    if name.startswith("pdf_"):
        return f"/zsxq/pdf/{name[4:]}"
    if name.startswith("report_"):
        try:
            int(name[7:])
            return f"/sec/file/{name[7:]}"
        except ValueError:
            pass
    return None


def resolve_edge_sources(conn: sqlite3.Connection,
                         episodes_json: str) -> list[dict]:
    """Return [{label, url}] for a JSON array of episode UUIDs.

    url is None when no viewer route is known for the episode type.
    """
    try:
        uuids = json.loads(episodes_json or "[]")
    except Exception:
        return []
    if not uuids:
        return []
    ph = ",".join("?" * len(uuids))
    rows = conn.execute(
        f"SELECT name, source_desc FROM episodes WHERE uuid IN ({ph})", uuids
    ).fetchall()
    return [
        {"label": r[1] or r[0], "url": _episode_url(r[0])}
        for r in rows if (r[0] or r[1])
    ]


def deprecate_edge(conn: sqlite3.Connection, uuid: str, reason: str = "RELATION_NONSENSE") -> bool:
    """Mark an edge as deprecated with a reason.  Returns True if edge found."""
    cur = conn.execute(
        "UPDATE edges SET deprecated=1, deprecated_reason=?, updated_at=datetime('now') WHERE uuid=?",
        (reason, uuid),
    )
    conn.commit()
    return cur.rowcount > 0


def isolate_entity(conn: sqlite3.Connection, uuid: str) -> bool:
    """Mark an entity as isolated (hidden from UI) and deprecate all its edges.

    Returns True if the entity was found and updated.
    Isolated entities are excluded from all search results, entity browsers,
    stats counts, and LLM entity extraction prompts.
    """
    cur = conn.execute(
        "UPDATE entities SET isolated=1, updated_at=datetime('now') WHERE uuid=?",
        (uuid,),
    )
    if cur.rowcount == 0:
        conn.commit()
        return False
    # Deprecate every edge that involves this entity
    conn.execute(
        """UPDATE edges
              SET deprecated=1, deprecated_reason='ENTITY_ISOLATED', updated_at=datetime('now')
            WHERE src_uuid=? OR tgt_uuid=?""",
        (uuid, uuid),
    )
    conn.commit()
    return True


def get_entity_edges(conn: sqlite3.Connection, entity_uuid: str) -> list:
    """Return all non-deprecated edges directly connected to an entity (by UUID).

    Used when clicking a graph node — guarantees results match exactly what
    the graph visualisation shows, regardless of entity name or FTS index state.
    """
    rows = conn.execute(
        """SELECT uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name,
                  episodes_json, deprecated, deprecated_reason
             FROM edges
            WHERE (src_uuid=? OR tgt_uuid=?)
              AND (deprecated=0 OR deprecated IS NULL)
            ORDER BY uuid""",
        (entity_uuid, entity_uuid),
    ).fetchall()
    items = []
    for r in rows:
        d = dict(r)
        d["sources"] = resolve_edge_sources(conn, d.pop("episodes_json", "[]"))
        d["source_node_uuid"] = d.pop("src_uuid", "")
        d["source_node_name"] = d.pop("src_name", "")
        d["target_node_uuid"] = d.pop("tgt_uuid", "")
        d["target_node_name"] = d.pop("tgt_name", "")
        items.append(d)
    return items


def get_isolated_entity_names(conn: sqlite3.Connection) -> list:
    """Return names of all isolated entities (used to inject into LLM prompts)."""
    rows = conn.execute(
        "SELECT name FROM entities WHERE isolated=1 ORDER BY name"
    ).fetchall()
    return [r[0] for r in rows]


def get_edges(conn: sqlite3.Connection, limit: int = 300,
              cursor: Optional[str] = None,
              include_deprecated: bool = False) -> tuple[list[dict], Optional[str]]:
    dep_filter = "" if include_deprecated else " AND (deprecated = 0 OR deprecated IS NULL)"
    if cursor:
        rows = conn.execute(
            f"SELECT uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name, "
            f"episodes_json, deprecated, deprecated_reason "
            f"FROM edges WHERE uuid > ?{dep_filter} ORDER BY uuid LIMIT ?", (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            f"SELECT uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name, "
            f"episodes_json, deprecated, deprecated_reason "
            f"FROM edges WHERE 1=1{dep_filter} ORDER BY uuid LIMIT ?", (limit,)
        ).fetchall()
    items = []
    for r in rows:
        d = dict(r)
        d["sources"] = resolve_edge_sources(conn, d.pop("episodes_json", "[]"))
        items.append(d)
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
    # Build FTS5 query:
    #   1. Exact phrase first (highest relevance)  e.g. "Synodex platform"
    #   2. All-words AND fallback                  e.g. Synodex* AND platform*
    #   3. Any-word OR fallback                    e.g. Synodex* OR platform*
    # Use phrase match when query has multiple words so "Synodex® platform"
    # doesn't match random docs that merely contain "platform".
    words = [w.strip() for w in query.split() if w.strip()]
    if not words:
        return {"nodes": [], "edges": []}

    # Escape special FTS5 chars in individual words
    def _esc(w: str) -> str:
        return w.replace('"', '""')

    if len(words) == 1:
        fts_query = f'"{_esc(words[0])}"*'
    else:
        phrase   = '"' + " ".join(_esc(w) for w in words) + '"'
        and_part = " AND ".join(f'"{_esc(w)}"*' for w in words)
        or_part  = " OR ".join(f'"{_esc(w)}"*' for w in words)
        # Try phrase first; if no results the caller will widen to AND/OR
        fts_query = f"{phrase} OR ({and_part}) OR ({or_part})"

    # Entity search (exclude isolated)
    try:
        entity_rows = conn.execute(
            """SELECT e.uuid, e.name, e.labels_json, e.summary,
                      bm25(entities_fts) AS score
               FROM entities_fts
               JOIN entities e ON entities_fts.rowid = e.rowid
               WHERE entities_fts MATCH ?
                 AND (e.isolated = 0 OR e.isolated IS NULL)
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

    # Edge search (exclude deprecated + edges involving isolated entities)
    try:
        edge_rows = conn.execute(
            """SELECT ed.uuid, ed.name, ed.fact,
                      ed.src_uuid, ed.src_name, ed.tgt_uuid, ed.tgt_name,
                      ed.episodes_json,
                      bm25(edges_fts) AS score
               FROM edges_fts
               JOIN edges ed ON edges_fts.rowid = ed.rowid
               WHERE edges_fts MATCH ?
                 AND (ed.deprecated = 0 OR ed.deprecated IS NULL)
                 AND NOT EXISTS (SELECT 1 FROM entities WHERE uuid=ed.src_uuid AND isolated=1)
                 AND NOT EXISTS (SELECT 1 FROM entities WHERE uuid=ed.tgt_uuid AND isolated=1)
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
         "sources":          resolve_edge_sources(conn, r["episodes_json"] or "[]"),
         "score":            r["score"]}
        for r in edge_rows
    ]

    # ── Episodes: collect from matched edges + direct source_desc search ──────
    # 1. Gather all episode UUIDs referenced by the matched edges
    ep_uuids: set[str] = set()
    for r in edge_rows:
        try:
            ep_uuids.update(str(u) for u in json.loads(r["episodes_json"] or "[]"))
        except Exception:
            pass

    # 2. Also search source_desc directly (handles queries in any language
    #    that match the document name/description even without FTS)
    ep_by_desc: list = []
    try:
        like_q = f"%{query}%"
        ep_by_desc = conn.execute(
            "SELECT uuid, name, source_desc FROM episodes "
            "WHERE source_desc LIKE ? OR name LIKE ? LIMIT ?",
            (like_q, like_q, limit),
        ).fetchall()
    except Exception:
        pass

    for r in ep_by_desc:
        ep_uuids.add(r[0])

    # 3. Fetch full episode rows for all collected UUIDs
    episodes: list[dict] = []
    if ep_uuids:
        ph = ",".join("?" * len(ep_uuids))
        ep_rows = conn.execute(
            f"SELECT uuid, name, source_desc FROM episodes WHERE uuid IN ({ph})",
            list(ep_uuids),
        ).fetchall()
        episodes = [
            {"uuid": r[0], "name": r[1] or "",
             "source_desc": r[2] or "",
             "url": _episode_url(r[1] or "")}
            for r in ep_rows
        ]

    return {"nodes": nodes, "edges": edges, "episodes": episodes}


# ── Community subgraph — label propagation + LLM summaries ───────────────────

def _parse_name_summary(text: str, fallback_rows: list) -> tuple[str, str]:
    """Parse 'NAME: ...\nSUMMARY: ...' from LLM output with graceful fallback."""
    name = ""
    summary = ""
    for line in text.splitlines():
        if line.startswith("NAME:") and not name:
            name = line[5:].strip()
        elif line.startswith("SUMMARY:") and not summary:
            summary = line[8:].strip()
    if not name:
        name = fallback_rows[0][0][:60] if fallback_rows else "Community"
    if not summary:
        summary = text.strip()[:500]
    return name, summary


def _summarize_community(member_rows: list) -> tuple[str, str]:
    """Generate (name, summary) for a community via MiniMax map-reduce.

    member_rows: list of (entity_name, entity_summary) tuples.
    """
    from minimax import call_minimax

    CHUNK = 5
    with_content = [(n, s) for n, s in member_rows if s.strip()]
    if not with_content:
        name = " / ".join(r[0] for r in member_rows[:4])
        return name, ""

    def _fmt(rows):
        return "\n\n".join(f"Entity: {n}\nSummary: {s}" for n, s in rows)

    sys_msg  = {"role": "system", "name": "MiniMax AI",
                "content": "You summarise knowledge graph communities concisely."}
    reduce_prompt = (
        "Based on these entity summaries, write:\n"
        "1. A 3-5 word topic name for this community.\n"
        "2. A 2-3 sentence community summary.\n\n"
        "Format exactly as:\nNAME: <name>\nSUMMARY: <summary>\n\n"
    )

    if len(with_content) <= CHUNK:
        text, _, _ = call_minimax(
            messages=[sys_msg, {"role": "user", "name": "User",
                                "content": reduce_prompt + _fmt(with_content)}],
            temperature=0.2, max_completion_tokens=256,
        )
    else:
        # Map: summarise each chunk
        partials = []
        for i in range(0, len(with_content), CHUNK):
            chunk = with_content[i:i + CHUNK]
            t, _, _ = call_minimax(
                messages=[
                    sys_msg,
                    {"role": "user", "name": "User",
                     "content": "Summarise these related entities in 1-2 sentences:\n\n" + _fmt(chunk)},
                ],
                temperature=0.2, max_completion_tokens=150,
            )
            if t.strip():
                partials.append(t.strip())
        # Reduce
        reduce_input = "\n\n".join(partials)
        text, _, _ = call_minimax(
            messages=[sys_msg, {"role": "user", "name": "User",
                                "content": reduce_prompt + reduce_input}],
            temperature=0.2, max_completion_tokens=256,
        )

    return _parse_name_summary(text, member_rows)


def build_communities(conn: sqlite3.Connection):
    """Full label propagation + LLM summarisation.

    Generator — yields progress strings so callers can stream them.
    Implements the algorithm from the Zep paper (arxiv 2501.13956):
      Phase 1: load graph
      Phase 2: label propagation until convergence (shuffle each pass)
      Phase 3: group entities by final label
      Phase 4: LLM summaries + write to DB
    """
    # Phase 1 — load graph
    all_uuids = [r[0] for r in conn.execute("SELECT uuid FROM entities").fetchall()]
    if not all_uuids:
        yield "No entities found — nothing to cluster."
        return

    adj: dict[str, list[str]] = defaultdict(list)
    for row in conn.execute(
        "SELECT src_uuid, tgt_uuid FROM edges "
        "WHERE src_uuid != '' AND tgt_uuid != ''"
    ).fetchall():
        adj[row[0]].append(row[1])
        adj[row[1]].append(row[0])

    yield f"Phase 1: loaded {len(all_uuids)} entities, {len(adj)} with edges"

    # Phase 2 — label propagation
    labels: dict[str, str] = {u: u for u in all_uuids}
    MAX_ITER = 50
    for iteration in range(MAX_ITER):
        changed = 0
        order = all_uuids[:]
        random.shuffle(order)
        for uuid in order:
            neighbours = adj.get(uuid, [])
            if not neighbours:
                continue
            counts = Counter(labels[n] for n in neighbours if n in labels)
            if not counts:
                continue
            best = counts.most_common(1)[0][0]
            if labels[uuid] != best:
                labels[uuid] = best
                changed += 1
        if changed == 0:
            yield f"Phase 2: converged after {iteration + 1} iterations"
            break
    else:
        yield f"Phase 2: reached max {MAX_ITER} iterations"

    # Phase 3 — group by final label
    buckets: dict[str, list[str]] = defaultdict(list)
    for uuid, label in labels.items():
        buckets[label].append(uuid)

    yield f"Phase 3: {len(buckets)} communities identified"

    # Phase 4 — write to DB + LLM summaries (skip singletons)
    MIN_MEMBERS = 2  # isolated entities with no edges are excluded entirely
    real_buckets = sorted(
        [(label, uuids) for label, uuids in buckets.items() if len(uuids) >= MIN_MEMBERS],
        key=lambda kv: -len(kv[1]),
    )
    skipped = len(buckets) - len(real_buckets)
    yield f"Phase 4: {len(real_buckets)} multi-member communities ({skipped} singletons skipped)"

    conn.execute("DELETE FROM community_members")
    conn.execute("DELETE FROM communities")
    conn.commit()

    total = len(real_buckets)
    all_member_rows: list[tuple[str, int]] = []  # (entity_uuid, community_id)

    for i, (label, member_uuids) in enumerate(real_buckets):
        yield f"Summarising community {i + 1}/{total} ({len(member_uuids)} members)…"

        # Fetch entity names + summaries for this community
        ph = ",".join("?" * len(member_uuids))
        rows = conn.execute(
            f"SELECT name, summary FROM entities WHERE uuid IN ({ph})",
            member_uuids,
        ).fetchall()
        member_rows = [(r[0], r[1] or "") for r in rows]

        if len(member_uuids) < 3:
            # 2-member community — skip LLM, just name A / B
            name    = " / ".join(r[0] for r in member_rows[:2])
            summary = ""
        else:
            try:
                name, summary = _summarize_community(member_rows)
            except Exception as exc:
                name    = member_rows[0][0] if member_rows else "Community"
                summary = ""
                yield f"  ⚠ LLM error: {exc}"

        cur = conn.execute(
            "INSERT INTO communities(name, summary, member_count) VALUES (?,?,?)",
            (name, summary, len(member_uuids)),
        )
        cid = cur.lastrowid
        all_member_rows.extend((uuid, cid) for uuid in member_uuids)
        conn.commit()

    conn.executemany(
        "INSERT OR REPLACE INTO community_members(entity_uuid, community_id) VALUES (?,?)",
        all_member_rows,
    )
    conn.commit()
    yield f"Done — {total} communities built ({skipped} singletons excluded)"


def assign_entity_community(conn: sqlite3.Connection, entity_uuid: str) -> None:
    """Incremental label propagation for a single new/updated entity (no LLM).

    Assigns the entity to the plurality community of its neighbours.
    Safe to call after every upsert_entities() when communities already exist.
    """
    # Get neighbours
    rows = conn.execute(
        "SELECT tgt_uuid FROM edges WHERE src_uuid=? AND tgt_uuid!='' "
        "UNION "
        "SELECT src_uuid FROM edges WHERE tgt_uuid=? AND src_uuid!=''",
        (entity_uuid, entity_uuid),
    ).fetchall()
    neighbour_uuids = [r[0] for r in rows]

    if not neighbour_uuids:
        # Isolated entity — create a stub community only if not already assigned
        existing = conn.execute(
            "SELECT community_id FROM community_members WHERE entity_uuid=?",
            (entity_uuid,),
        ).fetchone()
        if existing:
            return
        name_row = conn.execute(
            "SELECT name FROM entities WHERE uuid=?", (entity_uuid,)
        ).fetchone()
        name = name_row[0] if name_row else entity_uuid[:8]
        cur = conn.execute(
            "INSERT INTO communities(name, summary, member_count) VALUES (?,?,1)",
            (name, ""),
        )
        conn.execute(
            "INSERT OR REPLACE INTO community_members(entity_uuid, community_id) VALUES (?,?)",
            (entity_uuid, cur.lastrowid),
        )
        conn.commit()
        return

    # Find plurality community among neighbours
    ph = ",".join("?" * len(neighbour_uuids))
    cm_rows = conn.execute(
        f"SELECT community_id FROM community_members WHERE entity_uuid IN ({ph})",
        neighbour_uuids,
    ).fetchall()
    if not cm_rows:
        return  # neighbours not yet assigned — skip

    best_cid = Counter(r[0] for r in cm_rows).most_common(1)[0][0]

    old = conn.execute(
        "SELECT community_id FROM community_members WHERE entity_uuid=?",
        (entity_uuid,),
    ).fetchone()
    if old:
        if old[0] == best_cid:
            return  # no change
        conn.execute(
            "UPDATE communities SET member_count = member_count - 1 WHERE id=?",
            (old[0],),
        )

    conn.execute(
        "INSERT OR REPLACE INTO community_members(entity_uuid, community_id) VALUES (?,?)",
        (entity_uuid, best_cid),
    )
    conn.execute(
        "UPDATE communities SET member_count = member_count + 1 WHERE id=?",
        (best_cid,),
    )
    conn.commit()


def get_communities(conn: sqlite3.Connection, limit: int = 100,
                    cursor: Optional[int] = None) -> tuple[list[dict], Optional[int]]:
    """Paginated community list. First page sorted by member_count DESC."""
    if cursor is not None:
        rows = conn.execute(
            "SELECT id, name, summary, member_count FROM communities "
            "WHERE id > ? ORDER BY id LIMIT ?", (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, summary, member_count FROM communities "
            "ORDER BY member_count DESC LIMIT ?", (limit,)
        ).fetchall()
    items = [
        {"id": r["id"], "name": r["name"],
         "summary": r["summary"] or "", "member_count": r["member_count"]}
        for r in rows
    ]
    next_cursor = items[-1]["id"] if len(items) == limit else None
    return items, next_cursor


def get_community_members(conn: sqlite3.Connection,
                          community_id: int) -> list[dict]:
    """Return all entities belonging to a community, ordered by name."""
    rows = conn.execute(
        """SELECT e.uuid, e.name, e.labels_json, e.summary, e.rating
           FROM community_members cm
           JOIN entities e ON e.uuid = cm.entity_uuid
           WHERE cm.community_id = ?
           ORDER BY e.name""",
        (community_id,),
    ).fetchall()
    return [
        {"uuid": r["uuid"], "name": r["name"],
         "labels": json.loads(r["labels_json"] or "[]"),
         "summary": r["summary"] or "",
         "rating": r["rating"] or 0}
        for r in rows
    ]


# ── Manual community creation ────────────────────────────────────────────────

def create_community_from_seed(conn: sqlite3.Connection,
                                name: str,
                                seed_uuid: str) -> dict:
    """Create a community seeded by one entity; BFS assigns all connected entities.

    Traverses non-deprecated edges in both directions recursively.
    Returns {"id": community_id, "member_count": N}.
    """
    # BFS over the edge graph (bidirectional, skip deprecated)
    visited: set[str] = set()
    queue = [seed_uuid]
    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)
        rows = conn.execute(
            """SELECT src_uuid, tgt_uuid FROM edges
               WHERE deprecated = 0
                 AND (src_uuid = ? OR tgt_uuid = ?)""",
            (current, current),
        ).fetchall()
        for r in rows:
            for neighbour in (r["src_uuid"], r["tgt_uuid"]):
                if neighbour and neighbour not in visited:
                    queue.append(neighbour)

    # Remove entities that don't exist or are isolated
    existing = {
        r["uuid"] for r in conn.execute(
            "SELECT uuid FROM entities WHERE isolated = 0 AND uuid IN ({})".format(
                ",".join("?" * len(visited))
            ),
            list(visited),
        ).fetchall()
    } if visited else set()

    member_count = len(existing)

    # Upsert community
    cur = conn.execute(
        "INSERT INTO communities (name, summary, member_count) VALUES (?, '', ?)",
        (name, member_count),
    )
    cid = cur.lastrowid

    # Assign members — remove prior membership for each entity (one community at a time)
    for uuid in existing:
        conn.execute(
            "INSERT OR REPLACE INTO community_members (entity_uuid, community_id) VALUES (?, ?)",
            (uuid, cid),
        )

    conn.commit()
    return {"id": cid, "member_count": member_count}


def remove_community_bfs(conn: sqlite3.Connection,
                          community_id: int,
                          seed_uuid: str) -> int:
    """BFS from seed_uuid, removing all reachable community members from community_id.

    Only traverses edges between entities that are currently in the same community.
    Returns count of removed memberships.
    """
    # Collect all members of the community for BFS scoping
    member_set = {
        r["entity_uuid"] for r in conn.execute(
            "SELECT entity_uuid FROM community_members WHERE community_id = ?",
            (community_id,),
        ).fetchall()
    }
    if seed_uuid not in member_set:
        return 0

    # BFS restricted to current community members
    visited: set[str] = set()
    queue = [seed_uuid]
    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)
        rows = conn.execute(
            """SELECT src_uuid, tgt_uuid FROM edges
               WHERE deprecated = 0
                 AND (src_uuid = ? OR tgt_uuid = ?)""",
            (current, current),
        ).fetchall()
        for r in rows:
            for neighbour in (r["src_uuid"], r["tgt_uuid"]):
                if neighbour and neighbour not in visited and neighbour in member_set:
                    queue.append(neighbour)

    # Remove visited entities from the community
    placeholders = ",".join("?" * len(visited))
    conn.execute(
        f"DELETE FROM community_members WHERE community_id = ? AND entity_uuid IN ({placeholders})",
        [community_id, *visited],
    )
    # Update member_count
    conn.execute(
        "UPDATE communities SET member_count = (SELECT COUNT(*) FROM community_members WHERE community_id = ?) WHERE id = ?",
        (community_id, community_id),
    )
    conn.commit()
    return len(visited)


# ── One-time backfill from KuzuDB ─────────────────────────────────────────────

def backfill_from_kuzu(mirror_conn: sqlite3.Connection,
                       graph_dir: Path,
                       group_id: str = "financial-pdfs",
                       kuzu_conn=None) -> tuple[int, int]:
    """Populate the mirror from KuzuDB.

    If kuzu_conn is provided (an existing kuzu.Connection), it is reused — this
    avoids the exclusive-lock conflict when the web server already holds a write
    connection.  Otherwise a read-only Database is opened (safe when no writer
    is active, e.g. from a standalone backfill script).

    Returns (n_entities, n_edges) written.
    """
    import json as _json

    if not graph_dir.exists():
        return 0, 0

    conn = kuzu_conn
    if conn is None:
        try:
            import kuzu
            kdb  = kuzu.Database(str(graph_dir), read_only=True)
            conn = kuzu.Connection(kdb)
        except Exception as e:
            print(f"[mirror] backfill: could not open KuzuDB: {e}")
            return 0, 0

    def _rows(result):
        cols = result.get_column_names()
        out  = []
        while result.has_next():
            out.append(dict(zip(cols, result.get_next())))
        return out

    # ── entities ──────────────────────────────────────────────────────────────
    n_ent = 0
    try:
        batch = []
        # Try to fetch rating from KuzuDB; if the column doesn't exist yet, fall back.
        try:
            rows = _rows(conn.execute(
                "MATCH (n:Entity) WHERE n.group_id = $gid "
                "RETURN n.uuid, n.name, n.labels, n.summary, n.rating",
                {"gid": group_id},
            ))
            has_rating = True
        except Exception:
            rows = _rows(conn.execute(
                "MATCH (n:Entity) WHERE n.group_id = $gid "
                "RETURN n.uuid, n.name, n.labels, n.summary",
                {"gid": group_id},
            ))
            has_rating = False
        for r in rows:
            labels = r.get("n.labels") or []
            if isinstance(labels, str):
                try: labels = _json.loads(labels)
                except Exception: labels = []
            batch.append((
                r["n.uuid"] or "",
                r["n.name"] or "",
                _json.dumps(list(labels)),
                (r.get("n.summary") or "")[:2000],
                int(r.get("n.rating") or 0) if has_rating else 0,
            ))
        if batch:
            mirror_conn.executemany(
                """INSERT INTO entities(uuid, name, labels_json, summary, rating)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(uuid) DO UPDATE SET
                     name=excluded.name, labels_json=excluded.labels_json,
                     summary=excluded.summary,
                     rating=CASE WHEN excluded.rating > 0 THEN excluded.rating ELSE rating END""",
                batch,
            )
            mirror_conn.commit()
            n_ent = len(batch)
    except Exception as e:
        print(f"[mirror] backfill entities error: {e}")

    # ── edges ──────────────────────────────────────────────────────────────────
    n_edg = 0
    try:
        batch = []
        rows = _rows(conn.execute(
            "MATCH (s:Entity)-[:RELATES_TO]->(e:RelatesToNode_)-[:RELATES_TO]->(t:Entity) "
            "WHERE e.group_id = $gid "
            "RETURN e.uuid, e.name, e.fact, e.episodes, s.uuid AS src, s.name AS src_name, "
            "       t.uuid AS tgt, t.name AS tgt_name",
            {"gid": group_id},
        ))
        for r in rows:
            ep_raw  = r.get("e.episodes") or []
            ep_json = json.dumps([str(u) for u in ep_raw]) if ep_raw else "[]"
            batch.append((
                r["e.uuid"] or "",
                r["e.name"] or "",
                (r.get("e.fact") or "")[:4000],
                r.get("src") or "",
                r.get("src_name") or "",
                r.get("tgt") or "",
                r.get("tgt_name") or "",
                ep_json,
            ))
        if batch:
            mirror_conn.executemany(
                """INSERT INTO edges(uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name, episodes_json)
                   VALUES (?,?,?,?,?,?,?,?)
                   ON CONFLICT(uuid) DO UPDATE SET
                     name=excluded.name, fact=excluded.fact,
                     src_uuid=excluded.src_uuid, src_name=excluded.src_name,
                     tgt_uuid=excluded.tgt_uuid, tgt_name=excluded.tgt_name,
                     episodes_json=CASE WHEN excluded.episodes_json != '[]' THEN excluded.episodes_json ELSE episodes_json END""",
                batch,
            )
            mirror_conn.commit()
            n_edg = len(batch)
    except Exception as e:
        print(f"[mirror] backfill edges error: {e}")

    # ── episodes ──────────────────────────────────────────────────────────────
    try:
        ep_rows = _rows(conn.execute(
            "MATCH (e:Episodic) WHERE e.group_id = $gid "
            "RETURN e.uuid, e.name, e.source_description",
            {"gid": group_id},
        ))
        ep_batch = [
            (r["e.uuid"] or "", r.get("e.name") or "",
             r.get("e.source_description") or "")
            for r in ep_rows
        ]
        if ep_batch:
            mirror_conn.executemany(
                "INSERT INTO episodes(uuid, name, source_desc) VALUES (?,?,?) "
                "ON CONFLICT(uuid) DO NOTHING",
                ep_batch,
            )
            mirror_conn.commit()
    except Exception as e:
        print(f"[mirror] backfill episodes error: {e}")

    return n_ent, n_edg
