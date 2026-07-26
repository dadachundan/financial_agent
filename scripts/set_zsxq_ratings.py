#!/usr/bin/env python3
"""Persist agent-curated ``claude_rating`` stars onto ``db/zsxq.db`` rows.

Shared helper used by the zsxq recommender skills (`/zsxq-recommend`,
`/zsxq-ideas`, and any skill that surfaces a reading list). Whenever
Claude recommends (or triages away) a zsxq PDF, it should record its
verdict as a 1-5 star ``claude_rating`` so the judgement is durable and
visible in the `/zsxq` viewer and downstream ranking.

Rating convention (project-wide, set by the user):

    3, 4, 5  → worth reading   (5 = must-read, 4 = strong, 3 = solid)
    1, 2     → not worth reading (2 = skippable, 1 = noise / off-topic)
    0        → explicitly "seen, no signal" (rarely needed)
    null     → clears the rating

This is the ONLY sanctioned write path for the ``claude_rating`` column
besides ``zsxq_common.set_claude_rating`` itself (which this script
calls). Per the CLAUDE.md DB-safety rules, never write ``claude_rating``
with raw SQL — always go through here or the helper.

The agent emits a JSON array of ``{file_id, rating}`` records on stdin::

    python3 scripts/set_zsxq_ratings.py <<'JSON'
    [
      {"file_id": 184124282514242, "rating": 5},
      {"file_id": 184152128158222, "rating": 4},
      {"file_id": 184152151455852, "rating": 2}
    ]
    JSON

Each record may carry an optional ``"note"`` (ignored by the DB — it's
just there so the agent's emitted JSON is self-documenting).

Output: JSON summary on stdout ``{considered, updated, missing,
errored, rows:[{file_id, rating, ok, reason}]}`` where ``missing`` counts
file_ids not present in ``pdf_files``.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

# Walk up to the project root (the dir containing db_paths.py) and import it,
# so FINAGENT_DB_DIR redirection reaches this script (CLAUDE.md DB-safety rule).
_here = Path(__file__).resolve()
for _anc in _here.parents:
    if (_anc / "db_paths.py").exists():
        sys.path.insert(0, str(_anc))
        break

from db_paths import db_path  # noqa: E402
from zsxq_common import set_claude_rating  # noqa: E402

DB_PATH = db_path("zsxq.db")


def main() -> None:
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit("no JSON on stdin")
    try:
        records = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"invalid JSON on stdin: {e}")
    if not isinstance(records, list):
        sys.exit("stdin JSON must be a list of {file_id, rating} objects")

    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH, timeout=30)
    results: list[dict] = []
    updated = missing = errored = 0
    try:
        for rec in records:
            fid = rec.get("file_id")
            rating = rec.get("rating")
            row = {"file_id": fid, "rating": rating}
            if fid is None:
                row.update(ok=False, reason="missing file_id")
                errored += 1
                results.append(row)
                continue
            try:
                changed = set_claude_rating(conn, int(fid), rating)
            except (ValueError, TypeError) as e:
                row.update(ok=False, reason=str(e))
                errored += 1
                results.append(row)
                continue
            if changed:
                row.update(ok=True, reason="updated")
                updated += 1
            else:
                row.update(ok=False, reason="file_id not in pdf_files")
                missing += 1
            results.append(row)
    finally:
        conn.close()

    json.dump(
        {
            "considered": len(records),
            "updated": updated,
            "missing": missing,
            "errored": errored,
            "rows": results,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
