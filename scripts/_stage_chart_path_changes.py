"""Stage only the chart-path rewrites without touching pre-existing edits.

Several .md files in the working tree have two unrelated kinds of edits
sitting together:
  1. The chart-path rewrite from restore_broken_chart_refs.py
     (`](../../charts/X)` → `](charts/X)`).
  2. Citation-backfill changes from prior agent work that were never
     committed.

This script stages only kind (1): for each affected .md file we take the
HEAD blob, apply the path rewrite, hash it, and update the index — the
working-tree file is left exactly as is so the kind (2) edits remain
visible for review.

Run from the repo root after restore_broken_chart_refs.py.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

OLD = b"](../../charts/"
NEW = b"](charts/"


def run(*args, **kw):
    return subprocess.run(args, check=True, capture_output=True, **kw)


def main():
    # All .md files under reports/ that differ from HEAD. core.quotePath=false
    # keeps non-ASCII paths (Chinese folder names) unquoted in the listing.
    diff = run("git", "-c", "core.quotePath=false",
               "diff", "--name-only", "HEAD", "--", "reports/").stdout.decode()
    candidates = [Path(p) for p in diff.strip().splitlines() if p.endswith(".md")]

    staged = 0
    skipped = 0
    for p in candidates:
        head = run("git", "show", f"HEAD:{p}").stdout
        if OLD not in head:
            skipped += 1
            continue
        rewritten = head.replace(OLD, NEW)
        # Stage the HEAD+rewrite version without touching the working tree.
        blob_hash = run("git", "hash-object", "-w", "--stdin", input=rewritten).stdout.decode().strip()
        run("git", "update-index", "--cacheinfo", f"100644,{blob_hash},{p}")
        staged += 1

    print(f"Staged path-only rewrites: {staged}")
    print(f"Skipped (no chart refs at HEAD): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
