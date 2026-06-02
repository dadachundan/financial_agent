"""
manual_graph.py — Curate the knowledge graph by hand (no LLM, no API).

This module replaces the LLM-driven graphiti ingest pipeline. Entities and
edges are inserted directly into the SQLite mirror at ``db/graph_mirror.db``,
which is what the viewer at ``/zep/`` reads. There is no automated extraction
— Claude (the agent) reads the source documents and decides what to add.

Usage from the REPL or another script::

    from manual_graph import add_entity, add_edge, find_entity, set_episode_for_edge

    # Idempotent: case-insensitive by name. Existing entity is returned, not duplicated.
    nvda = add_entity("NVIDIA",
                      labels=["Company"],
                      summary="Fabless GPU vendor; dominant in AI training silicon.",
                      ticker="NVDA")
    tsmc = add_entity("TSMC",  labels=["Company"], ticker="TSM")

    # Edge lookup happens by entity name, both directions, case-insensitive.
    add_edge("TSMC", "NVIDIA",
             relation="MANUFACTURES_FOR",
             fact="TSMC fabricates NVIDIA's H100 and Blackwell GPUs at N4/N3.")

The functions return dicts with the canonical UUIDs so a calling script can
chain follow-ups (e.g. attach a source episode).

Conventions
-----------
- ``labels`` is a list of strings — typically ``["Company"]`` or ``["Product"]``.
- ``relation`` is an ALL_CAPS verb phrase (e.g. ``MANUFACTURES_FOR``,
  ``COMPETES_WITH``, ``IS_SUBSIDIARY_OF``, ``ACQUIRED``, ``SUPPLIES``).
- ``fact`` is a one-sentence English description of *why* the edge exists. It
  is what gets rendered in the viewer's edge tooltip.
- ``source`` is an optional citation slug (e.g. ``"NVDA_10-K_FY25"``) that
  gets recorded into the edges' ``episodes_json`` so the viewer can show
  provenance. Use :func:`add_episode` to register a source first.

Look up an entity before creating an edge if you're worried about exact
casing — :func:`find_entity` does a case-insensitive search.
"""

from __future__ import annotations

import json
import sqlite3
import uuid as _uuid
from pathlib import Path
from typing import Iterable, Optional

import graph_mirror as _gm

_DB_PATH = Path(__file__).parent / "db" / "graph_mirror.db"


# ── Connection helper ────────────────────────────────────────────────────────

def _conn() -> sqlite3.Connection:
    """Return a connection to the mirror DB with the schema ensured."""
    c = _gm.get_conn(_DB_PATH)
    _gm.ensure_schema(c)
    return c


# ── Entity helpers ───────────────────────────────────────────────────────────

def find_entity(name: str, *, conn: Optional[sqlite3.Connection] = None) -> Optional[dict]:
    """Look up an entity by name (case-insensitive). Returns its row or None."""
    close = False
    if conn is None:
        conn = _conn()
        close = True
    row = conn.execute(
        "SELECT uuid, name, labels_json, summary, isolated, ticker, rating "
        "FROM entities WHERE LOWER(name) = LOWER(?) LIMIT 1",
        (name,),
    ).fetchone()
    if close:
        conn.close()
    return dict(row) if row else None


def add_entity(
    name: str,
    *,
    labels: Optional[Iterable[str]] = None,
    summary: str = "",
    ticker: str = "",
    rating: int = 0,
    market_cap_usd: Optional[float] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    """Insert (or update) an entity. Returns ``{uuid, name, created: bool}``.

    Idempotent by name (case-insensitive). If an entity already exists, its
    ``summary`` and ``ticker`` are filled in only when blank — existing
    curation is never overwritten silently.
    """
    if not name or not name.strip():
        raise ValueError("entity name is required")
    name = name.strip()

    close = False
    if conn is None:
        conn = _conn()
        close = True

    try:
        existing = find_entity(name, conn=conn)
        if existing:
            # Fill in blanks only — never clobber curated fields.
            updates, params = [], []
            if summary and not (existing["summary"] or "").strip():
                updates.append("summary = ?"); params.append(summary[:2000])
            if ticker and not (existing["ticker"] or "").strip():
                updates.append("ticker = ?"); params.append(ticker)
            if rating and (existing["rating"] or 0) == 0:
                updates.append("rating = ?"); params.append(int(rating))
            if market_cap_usd is not None:
                updates.append("market_cap_usd = ?"); params.append(float(market_cap_usd))
            if updates:
                params.append(existing["uuid"])
                conn.execute(
                    f"UPDATE entities SET {', '.join(updates)}, "
                    f"updated_at = datetime('now') WHERE uuid = ?",
                    params,
                )
                conn.commit()
            return {"uuid": existing["uuid"], "name": existing["name"], "created": False}

        uid = str(_uuid.uuid4())
        labels_json = json.dumps(list(labels or ["Entity"]))
        conn.execute(
            "INSERT INTO entities (uuid, name, labels_json, summary, ticker, "
            "rating, market_cap_usd, isolated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
            (uid, name, labels_json, summary[:2000], ticker, int(rating),
             market_cap_usd),
        )
        conn.commit()
        return {"uuid": uid, "name": name, "created": True}
    finally:
        if close:
            conn.close()


# ── Edge helpers ─────────────────────────────────────────────────────────────

def add_edge(
    src_name: str,
    tgt_name: str,
    *,
    relation: str,
    fact: str,
    source: str = "",
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    """Insert an edge between two entities (looked up by name).

    Raises ``ValueError`` if either entity is missing — call :func:`add_entity`
    first to make the failure explicit (we don't auto-create entities from
    edge writes because the labels / summary would be empty).

    ``relation`` is stored in the edge's ``name`` column (the verb phrase the
    viewer renders). ``fact`` is the long-form one-sentence justification.
    ``source`` (optional) is appended to ``episodes_json`` — pass a short
    slug like ``"NVDA_10-K_FY25"`` and call :func:`add_episode` separately to
    register the document.
    """
    if not relation.strip():
        raise ValueError("relation (verb phrase) is required")

    close = False
    if conn is None:
        conn = _conn()
        close = True

    try:
        src = find_entity(src_name, conn=conn)
        tgt = find_entity(tgt_name, conn=conn)
        if src is None:
            raise ValueError(f"source entity not found: {src_name!r} — add_entity() first")
        if tgt is None:
            raise ValueError(f"target entity not found: {tgt_name!r} — add_entity() first")

        eid = str(_uuid.uuid4())
        episodes = json.dumps([source]) if source else "[]"
        conn.execute(
            "INSERT INTO edges (uuid, name, fact, src_uuid, src_name, "
            "tgt_uuid, tgt_name, episodes_json, deprecated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)",
            (eid, relation.strip().upper(), fact[:4000],
             src["uuid"], src["name"], tgt["uuid"], tgt["name"], episodes),
        )
        conn.commit()
        return {"uuid": eid, "src": src["name"], "tgt": tgt["name"],
                "relation": relation.strip().upper()}
    finally:
        if close:
            conn.close()


# ── Episode / source helpers ─────────────────────────────────────────────────

def add_episode(
    slug: str,
    *,
    name: str = "",
    source_desc: str = "",
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    """Register a source document (10-K, research note, slide deck, …).

    The ``slug`` becomes the uuid (use a deterministic string like
    ``"NVDA_10-K_FY25"`` so re-runs are idempotent). ``source_desc`` is shown
    in the viewer when the edge tooltip is opened.
    """
    close = False
    if conn is None:
        conn = _conn()
        close = True
    try:
        conn.execute(
            "INSERT INTO episodes (uuid, name, source_desc) VALUES (?, ?, ?) "
            "ON CONFLICT(uuid) DO UPDATE SET "
            "  name = CASE WHEN excluded.name != '' THEN excluded.name ELSE episodes.name END, "
            "  source_desc = CASE WHEN excluded.source_desc != '' THEN excluded.source_desc ELSE episodes.source_desc END",
            (slug, name or slug, source_desc),
        )
        conn.commit()
        return {"uuid": slug, "name": name or slug}
    finally:
        if close:
            conn.close()


# ── Bulk convenience ─────────────────────────────────────────────────────────

def add_entities(rows: list[dict], *, conn: Optional[sqlite3.Connection] = None) -> list[dict]:
    """Idempotently add many entities at once.

    Each row is a dict accepted by :func:`add_entity`. Returns a list of
    ``{uuid, name, created}`` results in input order.
    """
    close = False
    if conn is None:
        conn = _conn()
        close = True
    try:
        return [add_entity(**r, conn=conn) for r in rows]
    finally:
        if close:
            conn.close()


def add_edges(rows: list[dict], *, conn: Optional[sqlite3.Connection] = None) -> list[dict]:
    """Add many edges at once. Each row is a dict accepted by :func:`add_edge`."""
    close = False
    if conn is None:
        conn = _conn()
        close = True
    try:
        out = []
        for r in rows:
            try:
                out.append(add_edge(**r, conn=conn))
            except ValueError as exc:
                out.append({"error": str(exc), "row": r})
        return out
    finally:
        if close:
            conn.close()


def stats() -> dict:
    """Return the current node / edge counts in the mirror."""
    c = _conn()
    try:
        n_ent = c.execute(
            "SELECT COUNT(*) FROM entities WHERE (isolated=0 OR isolated IS NULL)"
        ).fetchone()[0]
        n_iso = c.execute("SELECT COUNT(*) FROM entities WHERE isolated=1").fetchone()[0]
        n_edg = c.execute(
            "SELECT COUNT(*) FROM edges WHERE (deprecated=0 OR deprecated IS NULL)"
        ).fetchone()[0]
        n_ep  = c.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
        return {"entities": n_ent, "isolated": n_iso, "edges": n_edg, "episodes": n_ep}
    finally:
        c.close()
