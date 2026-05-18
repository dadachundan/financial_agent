#!/usr/bin/env python3
"""
seed_graph.py — Insert hand-curated entities + relations into graph_mirror.db.

Each JSON file represents one "episode" (= one source report) and supplies:
    {
      "episode": {
          "name":        "md_company_CATL_...",         # unique episode id
          "source_desc": "Research Report: CATL ..."
      },
      "entities": [
          { "name": "CATL", "labels": ["Company"], "summary": "..."},
          { "name": "Tesla", ...},
          ...
      ],
      "edges": [
          { "src": "CATL", "tgt": "Tesla",
            "name": "SUPPLIES",
            "fact": "CATL supplies LFP cells for the Tesla Model 3 Shanghai build." },
          ...
      ]
    }

Dedup: entities are matched case-insensitively on `name`.  An existing entity's
summary is left untouched (the first seed wins) — pass --overwrite-summary to
replace.  Edge `src` / `tgt` strings are resolved against this case-insensitive
entity index; unresolved edges are skipped with a warning.

Run:
    python3 tools/seed_graph.py path/to/episode.json
    python3 tools/seed_graph.py episodes/*.json
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid as _uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import graph_mirror as _gm  # noqa: E402


def _resolve_existing_entity(conn, name_lc: str) -> tuple[str, str] | None:
    row = conn.execute(
        "SELECT uuid, name FROM entities WHERE LOWER(name) = ?", (name_lc,)
    ).fetchone()
    return (row["uuid"], row["name"]) if row else None


def load_episode(conn, payload: dict, *, overwrite_summary: bool = False) -> dict:
    """Insert one episode worth of entities + edges. Returns counts."""
    ep         = payload.get("episode", {})
    entities   = payload.get("entities") or []
    edges      = payload.get("edges") or []
    ep_name    = (ep.get("name") or "").strip()
    if not ep_name:
        raise ValueError("episode.name required")
    source_desc = ep.get("source_desc") or ep.get("source_description") or ""

    # Reuse episode UUID if this name already exists (idempotent re-runs).
    existing = conn.execute(
        "SELECT uuid FROM episodes WHERE name = ?", (ep_name,)
    ).fetchone()
    if existing:
        ep_uuid = existing["uuid"]
    else:
        ep_uuid = str(_uuid.uuid4())
        conn.execute(
            "INSERT INTO episodes (uuid, name, source_desc) VALUES (?, ?, ?)",
            (ep_uuid, ep_name, source_desc),
        )

    # ── Entities ──────────────────────────────────────────────────────────────
    name_to_uuid: dict[str, str] = {}   # lowercase name → uuid
    name_to_canonical: dict[str, str] = {}
    n_new = n_existing = 0
    for ent in entities:
        raw_name = (ent.get("name") or "").strip()
        if not raw_name:
            continue
        name_lc = raw_name.lower()
        summary = (ent.get("summary") or "").strip()[:2000]
        labels  = ent.get("labels") or []
        labels_json = json.dumps(list(labels))

        hit = _resolve_existing_entity(conn, name_lc)
        if hit:
            u, canonical = hit
            if overwrite_summary and summary:
                conn.execute(
                    "UPDATE entities SET summary = ?, labels_json = ?, "
                    "updated_at = datetime('now') WHERE uuid = ?",
                    (summary, labels_json, u),
                )
            name_to_uuid[name_lc] = u
            name_to_canonical[name_lc] = canonical
            n_existing += 1
            continue

        u = str(_uuid.uuid4())
        conn.execute(
            "INSERT INTO entities (uuid, name, labels_json, summary) "
            "VALUES (?, ?, ?, ?)",
            (u, raw_name, labels_json, summary),
        )
        name_to_uuid[name_lc] = u
        name_to_canonical[name_lc] = raw_name
        n_new += 1

    # ── Edges ─────────────────────────────────────────────────────────────────
    n_edges = n_skipped = 0
    ep_json_one = json.dumps([ep_uuid])
    for ed in edges:
        src_raw = (ed.get("src") or ed.get("source") or "").strip()
        tgt_raw = (ed.get("tgt") or ed.get("target") or "").strip()
        if not src_raw or not tgt_raw:
            n_skipped += 1
            continue
        src_lc, tgt_lc = src_raw.lower(), tgt_raw.lower()

        # Lookup, falling back to the global entities table for entities we
        # didn't redefine in this episode.
        def _resolve(name_lc: str, name_raw: str) -> tuple[str, str] | None:
            if name_lc in name_to_uuid:
                return name_to_uuid[name_lc], name_to_canonical[name_lc]
            hit = _resolve_existing_entity(conn, name_lc)
            return hit  # may be None

        def _autocreate(name_lc: str, name_raw: str) -> tuple[str, str]:
            """Insert a placeholder entity so the edge can still be recorded."""
            u = str(_uuid.uuid4())
            conn.execute(
                "INSERT INTO entities (uuid, name, labels_json, summary) "
                "VALUES (?, ?, '[]', '')",
                (u, name_raw),
            )
            name_to_uuid[name_lc] = u
            name_to_canonical[name_lc] = name_raw
            return u, name_raw

        src = _resolve(src_lc, src_raw) or _autocreate(src_lc, src_raw)
        tgt = _resolve(tgt_lc, tgt_raw) or _autocreate(tgt_lc, tgt_raw)

        u = str(_uuid.uuid4())
        conn.execute(
            "INSERT INTO edges "
            "(uuid, name, fact, src_uuid, src_name, tgt_uuid, tgt_name, episodes_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (u, (ed.get("name") or "RELATES_TO").strip(),
             (ed.get("fact") or "").strip(),
             src[0], src[1], tgt[0], tgt[1], ep_json_one),
        )
        n_edges += 1

    conn.commit()
    return {
        "episode":            ep_name,
        "entities_new":       n_new,
        "entities_existing":  n_existing,
        "edges":              n_edges,
        "edges_skipped":      n_skipped,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", help="JSON file(s)")
    ap.add_argument("--overwrite-summary", action="store_true",
                    help="Replace summary on existing entities with the one in this file.")
    args = ap.parse_args()

    conn = _gm.get_conn()
    _gm.ensure_schema(conn)

    grand = {"entities_new": 0, "entities_existing": 0, "edges": 0, "edges_skipped": 0}
    for raw in args.paths:
        for p in sorted(Path().glob(raw)) or [Path(raw)]:
            if not p.exists():
                print(f"⚠  not found: {p}", file=sys.stderr)
                continue
            payload = json.loads(p.read_text(encoding="utf-8"))
            stats   = load_episode(conn, payload,
                                   overwrite_summary=args.overwrite_summary)
            print(f"✓ {p.name}: +{stats['entities_new']} new ent, "
                  f"{stats['entities_existing']} existing, "
                  f"{stats['edges']} edges "
                  f"({stats['edges_skipped']} skipped)")
            for k in grand:
                grand[k] += stats[k]

    print(f"\nTotal: +{grand['entities_new']} new entities, "
          f"{grand['entities_existing']} matched existing, "
          f"{grand['edges']} edges, {grand['edges_skipped']} edges skipped.")


if __name__ == "__main__":
    main()
