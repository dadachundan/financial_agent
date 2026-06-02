"""graph_mirror.py — SQLite store backing the financial knowledge graph.

Originally a read-only mirror of a graphiti-core / KuzuDB graph store. After
the LLM-driven ingest pipeline was removed (2026-06-02) this file became the
*only* graph DB in the project. Entities and edges are curated by hand via
`manual_graph.py`; the Flask viewer at `/zep/` reads from here directly.

WAL mode is kept on so a long-running Flask process can read while
`manual_graph` writes from another process or session.
"""

import json
import random
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

from db_paths import db_path

# Mirror lives in the canonical db/ dir (overridable via FINAGENT_DB_DIR).
_DEFAULT_MIRROR = db_path("graph_mirror.db")


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
    # Drop the legacy pending_deletions queue if a previous schema created it.
    # It was a holding area for KuzuDB writes blocked by the ingest write lock;
    # now that KuzuDB is gone, the table has no producers or consumers.
    conn.execute("DROP TABLE IF EXISTS pending_deletions")
    conn.commit()


# ── Edge name backfill (kept for legacy rows that have empty src/tgt names) ──

def backfill_edge_names(conn: sqlite3.Connection) -> None:
    """Fill in src_name/tgt_name for edges where the name field is blank."""
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


def get_stats(conn: sqlite3.Connection) -> dict:
    n  = conn.execute("SELECT COUNT(*) FROM entities WHERE (isolated=0 OR isolated IS NULL)").fetchone()[0]
    e  = conn.execute("SELECT COUNT(*) FROM edges WHERE (deprecated=0 OR deprecated IS NULL)").fetchone()[0]
    ep = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
    c  = conn.execute("SELECT COUNT(*) FROM communities").fetchone()[0]
    return {"node_count": n, "edge_count": e, "episode_count": ep, "community_count": c}


def get_entities(conn: sqlite3.Connection, limit: int = 200,
                 cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
    cols = "uuid, name, labels_json, summary, rating"
    extra_cols = {r[1] for r in conn.execute("PRAGMA table_info(entities)").fetchall()}
    has_mc = "market_cap_usd" in extra_cols
    has_tk = "ticker" in extra_cols
    if has_mc: cols += ", market_cap_usd"
    if has_tk: cols += ", ticker"
    if cursor:
        rows = conn.execute(
            f"SELECT {cols} FROM entities "
            "WHERE uuid > ? AND (isolated=0 OR isolated IS NULL) ORDER BY uuid LIMIT ?",
            (cursor, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            f"SELECT {cols} FROM entities "
            "WHERE (isolated=0 OR isolated IS NULL) ORDER BY uuid LIMIT ?", (limit,)
        ).fetchall()
    items = []
    for r in rows:
        d = {"uuid": r["uuid"], "name": r["name"],
             "labels": json.loads(r["labels_json"] or "[]"),
             "summary": r["summary"] or "",
             "rating": r["rating"] or 0}
        if has_mc: d["market_cap_usd"] = r["market_cap_usd"]
        if has_tk: d["ticker"] = r["ticker"] or ""
        items.append(d)
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


# Reports root used to repair stale `mdreport_<rel>` paths whose on-disk
# filename has since changed (e.g. when a `_<date>` suffix was dropped).
_REPORTS_DIR = Path(__file__).parent / "reports"


# Matches `EXCHANGE` + numeric/code suffix inside a company directory name,
# e.g. `SSE688279`, `NASDAQ_AMD`, `HKEX2050`, `KRX005930`. Used to find a
# sibling directory after a rename like
# `SamsungElectronics_KRX005930 → Samsung_KRX005930`.
_TICKER_TOKEN_RE = re.compile(
    r"(SSE|SZSE|HKEX|NASDAQ|NYSE|AMEX|TSE|TWSE|KRX|XETR|EPA|AEX|ASX|LSE)_?([A-Z0-9.]+)",
    re.IGNORECASE,
)


def _pick_md(parent: Path, prefer_zh: bool) -> Optional[Path]:
    """Pick the best research-doc markdown inside *parent*, or None."""
    if not parent.is_dir():
        return None
    candidates: list[Path] = []
    if prefer_zh:
        candidates += sorted(parent.glob("*_Research_Document*_zh.md"))
        candidates += sorted(parent.glob("*_公司研究*.md"))
        candidates += sorted(parent.glob("*_研究报告*.md"))
    else:
        candidates += sorted(
            p for p in parent.glob("*_Research_Document*.md")
            if not p.name.endswith("_zh.md")
        )
    if not candidates:
        candidates = sorted(parent.glob("*.md"))
    return candidates[-1] if candidates else None


def _resolve_mdreport_rel(rel: str) -> str:
    """Return a reports-relative path that exists on disk.

    Episode rows were seeded with filenames like
    `company/Unitree/Unitree_Research_Document_2026-05-16.md`; many of those
    files have since been renamed to drop the date suffix
    (`Unitree_Research_Document.md`), and a few company directories were
    themselves renamed (`SamsungElectronics_KRX005930 → Samsung_KRX005930`).
    When the stored path is missing, fall back to a sibling research
    markdown — first in the same directory, then in any sibling directory
    that shares one of the original tickers — so the link in the UI still
    opens the right report without requiring a DB rewrite.
    """
    if (_REPORTS_DIR / rel).is_file():
        return rel

    target = _REPORTS_DIR / rel
    prefer_zh = rel.endswith("_zh.md")

    same_dir_hit = _pick_md(target.parent, prefer_zh)
    if same_dir_hit is not None:
        return str(same_dir_hit.relative_to(_REPORTS_DIR))

    # Directory itself was renamed — look for a sibling directory under the
    # same parent (e.g. `reports/company/`) that contains any of the same
    # ticker tokens (`KRX005930`, `SSE601238`, ...).
    grandparent = target.parent.parent
    if grandparent.is_dir():
        tokens = {m.group(0).upper() for m in _TICKER_TOKEN_RE.finditer(target.parent.name)}
        if tokens:
            for sibling in sorted(grandparent.iterdir()):
                if not sibling.is_dir() or sibling == target.parent:
                    continue
                sib_tokens = {m.group(0).upper() for m in _TICKER_TOKEN_RE.finditer(sibling.name)}
                if tokens & sib_tokens:
                    hit = _pick_md(sibling, prefer_zh)
                    if hit is not None:
                        return str(hit.relative_to(_REPORTS_DIR))
    return rel


def _episode_url(name: str) -> Optional[str]:
    """Convert episode name → viewer URL, or None if unknown format.

    Supported name prefixes:
      pdf_<file_id>        → ZSXQ PDF viewer
      report_<int>         → SEC filing viewer
      mdreport_<rel-path>  → markdown research doc viewer (reports_viewer.py)
    """
    if name.startswith("pdf_"):
        return f"/zsxq/pdf/{name[4:]}"
    if name.startswith("report_"):
        try:
            int(name[7:])
            return f"/sec/file/{name[7:]}"
        except ValueError:
            pass
    if name.startswith("mdreport_"):
        rel = _resolve_mdreport_rel(name[len("mdreport_"):])
        return f"/claude-reports/view/{rel}"
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
    """FTS5 search across entity names/summaries and edge facts."""
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
    """Generate (name, summary) for a community without any LLM call.

    member_rows: list of (entity_name, entity_summary) tuples.

    Strategy:
      - Name = first 3 member names joined with " / " (capped to 60 chars).
      - Summary = up to 5 names, each followed by a one-line snippet of its
        own entity summary (first 80 chars), separated by " · ".
    """
    if not member_rows:
        return "Community", ""

    # Sort by presence of summary first, then by name length descending so
    # well-documented hubs lead the label.
    ordered = sorted(
        member_rows,
        key=lambda r: (0 if (r[1] or "").strip() else 1, -len(r[0] or "")),
    )

    name_parts = [r[0] for r in ordered[:3] if r[0]]
    name = " / ".join(name_parts)[:60] or "Community"

    snippets = []
    for n, s in ordered[:5]:
        s = (s or "").strip().split(". ")[0][:80]
        snippets.append(f"{n}: {s}" if s else n)
    summary = " · ".join(snippets)[:500]

    return name, summary


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
    Safe to call after manual_graph.add_entity() when communities already exist.
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


def get_entity_community(conn: sqlite3.Connection,
                         entity_uuid: str) -> Optional[dict]:
    """Return the community an entity belongs to, or None if unassigned."""
    row = conn.execute(
        """SELECT c.id, c.name, c.summary, c.member_count
           FROM community_members cm
           JOIN communities c ON c.id = cm.community_id
           WHERE cm.entity_uuid = ?""",
        (entity_uuid,),
    ).fetchone()
    if not row:
        return None
    return {"id": row["id"], "name": row["name"],
            "summary": row["summary"] or "", "member_count": row["member_count"]}


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


def add_to_community_from_seed(conn: sqlite3.Connection,
                               community_id: int,
                               seed_uuid: str) -> dict:
    """BFS-flood from seed_uuid and add all reachable entities to an existing community.

    Entities already in a different community are moved to this one.
    Returns {"id": community_id, "added": N, "member_count": total}.
    """
    # Verify community exists
    row = conn.execute("SELECT id, member_count FROM communities WHERE id=?",
                       (community_id,)).fetchone()
    if row is None:
        raise ValueError(f"Community {community_id} not found")

    # BFS over non-deprecated edges (bidirectional)
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

    # Filter to real, non-isolated entities
    existing = {
        r["uuid"] for r in conn.execute(
            "SELECT uuid FROM entities WHERE isolated = 0 AND uuid IN ({})".format(
                ",".join("?" * len(visited))
            ),
            list(visited),
        ).fetchall()
    } if visited else set()

    # Assign to this community (override any prior membership)
    for uuid in existing:
        conn.execute(
            "INSERT OR REPLACE INTO community_members (entity_uuid, community_id) VALUES (?, ?)",
            (uuid, community_id),
        )

    # Update member_count
    new_count = conn.execute(
        "SELECT COUNT(*) FROM community_members WHERE community_id=?",
        (community_id,),
    ).fetchone()[0]
    conn.execute("UPDATE communities SET member_count=? WHERE id=?",
                 (new_count, community_id))
    conn.commit()
    return {"id": community_id, "added": len(existing), "member_count": new_count}


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


def merge_entities(conn: sqlite3.Connection,
                   source_uuid: str,
                   target_uuid: str) -> dict:
    """Merge source entity into target: re-point all edges, delete source.

    All edges that referenced source_uuid are updated to reference target_uuid.
    Self-loops created by the merge are removed.
    Returns {"edges_updated": N}.
    """
    tgt_row = conn.execute(
        "SELECT name FROM entities WHERE uuid=?", (target_uuid,)
    ).fetchone()
    if tgt_row is None:
        raise ValueError(f"Target entity {target_uuid} not found")
    tgt_name = tgt_row["name"]

    # Re-point edges
    c1 = conn.execute("UPDATE edges SET src_uuid=?, src_name=? WHERE src_uuid=?",
                      (target_uuid, tgt_name, source_uuid)).rowcount
    c2 = conn.execute("UPDATE edges SET tgt_uuid=?, tgt_name=? WHERE tgt_uuid=?",
                      (target_uuid, tgt_name, source_uuid)).rowcount

    # Remove self-loops
    conn.execute("DELETE FROM edges WHERE src_uuid = tgt_uuid AND src_uuid = ?",
                 (target_uuid,))

    # Remove source entity and its community membership
    conn.execute("DELETE FROM community_members WHERE entity_uuid=?", (source_uuid,))
    conn.execute("DELETE FROM entities WHERE uuid=?", (source_uuid,))

    conn.commit()
    return {"edges_updated": c1 + c2}


def add_edge(conn: sqlite3.Connection,
             uuid: str,
             src_uuid: str, src_name: str,
             tgt_uuid: str, tgt_name: str,
             name: str, fact: str) -> dict:
    """Insert a manually-created edge into the mirror."""
    conn.execute(
        """INSERT OR REPLACE INTO edges
           (uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name,
            updated_at, deprecated, episodes_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), 0, '[]')""",
        (uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name),
    )
    conn.commit()
    return {"uuid": uuid}
