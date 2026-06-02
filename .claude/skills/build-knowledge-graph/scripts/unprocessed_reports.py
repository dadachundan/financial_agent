#!/usr/bin/env python3
"""
unprocessed_reports.py — List markdown reports not yet in the knowledge graph.

Compares ``reports/**/*.md`` against the citation slugs already present in
``episodes.uuid`` of ``db/graph_mirror.db``. Prints the unprocessed paths
sorted by mtime (newest first) so the user / agent can prioritise recent work.

The slug-matching is **heuristic**, not precise. We don't store the absolute
path in episodes — we store a short citation slug like ``NVDA_research_2026-06-02``
or ``CSPC_research_2026-06-02``. To decide whether a report has been processed
we look at the episode's ``source_desc`` field, which the skill convention is
to populate with the relative path under ``reports/``.

Usage::

    python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py
    python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py --subdir company
    python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py --limit 30
    python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py --json    # machine-readable

Reads `db/graph_mirror.db` only. Never writes.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


# ── Find the project root ─────────────────────────────────────────────────────
def _project_root() -> Path:
    p = Path(__file__).resolve()
    while p != p.parent:
        if (p / ".git").is_dir():
            return p
        p = p.parent
    # Fallback if .git isn't there (unusual for this repo).
    return Path("/Users/x/projects/financial_agent")


ROOT       = _project_root()
REPORTS    = ROOT / "reports"
MIRROR_DB  = ROOT / "db" / "graph_mirror.db"


# ── Canonical selection of one .md per company ───────────────────────────────
def _cjk_score(p: Path) -> int:
    import re
    return len(re.findall(r"[一-鿿]", p.stem))


def _select_canonical(folder: Path) -> Path | None:
    """For a company folder, return the canonical markdown.

    Mirrors the convention in CLAUDE.md (English + Chinese reports coexist):
    prefer ``_zh.md`` / ``_CN.md``; otherwise prefer the file with the most
    CJK characters in the stem; otherwise the first .md alphabetically.
    """
    mds = sorted(folder.glob("*.md"))
    if not mds:
        return None
    zh = [p for p in mds if p.stem.endswith(("_zh", "_CN"))]
    if zh:
        return zh[0]
    chinese_named = [p for p in mds if _cjk_score(p) > 0]
    if chinese_named:
        chinese_named.sort(key=lambda p: (-_cjk_score(p), p.name))
        return chinese_named[0]
    return mds[0]


def collect_reports(subdir: str | None = None) -> list[Path]:
    """Return the list of reports to consider for ingestion."""
    selected: list[Path] = []

    if subdir in (None, "company"):
        cdir = REPORTS / "company"
        if cdir.exists():
            for sub in sorted(cdir.iterdir()):
                if not sub.is_dir():
                    continue
                pick = _select_canonical(sub)
                if pick is not None:
                    selected.append(pick)

    if subdir in (None, "sector", "compare", "earnings", "themes"):
        targets = [subdir] if subdir else ["sector", "compare", "earnings", "themes"]
        for sd in targets:
            d = REPORTS / sd
            if d.exists():
                selected.extend(sorted(d.glob("*.md")))

    return selected


# ── Compare against episodes.source_desc ──────────────────────────────────────
def already_ingested_paths() -> set[str]:
    if not MIRROR_DB.exists():
        return set()
    conn = sqlite3.connect(str(MIRROR_DB))
    try:
        rows = conn.execute("SELECT source_desc FROM episodes").fetchall()
    finally:
        conn.close()
    out: set[str] = set()
    for (sd,) in rows:
        if not sd:
            continue
        # Match by the report's relative path under reports/, which is the
        # convention in CLAUDE.md's manual_graph.add_episode() example.
        # `source_desc` is typically the full project-relative path
        # ("reports/company/X/X_公司研究.md"); we extract the basename pair
        # so we tolerate either form.
        out.add(sd.strip())
        out.add(Path(sd).name)
    return out


def filter_unprocessed(reports: list[Path]) -> list[Path]:
    ingested = already_ingested_paths()
    out: list[Path] = []
    for p in reports:
        rel = str(p.relative_to(ROOT))
        if rel in ingested or p.name in ingested:
            continue
        out.append(p)
    return out


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(
        description="List markdown reports not yet ingested into db/graph_mirror.db.",
    )
    ap.add_argument(
        "--subdir",
        choices=["company", "sector", "compare", "earnings", "themes"],
        help="Restrict to one subdirectory under reports/.",
    )
    ap.add_argument("--limit", type=int, default=0,
                    help="Cap output at N reports (0 = all).")
    ap.add_argument("--json", action="store_true",
                    help="Output a JSON array of relative paths instead of a human table.")
    args = ap.parse_args()

    reports = collect_reports(args.subdir)
    unprocessed = filter_unprocessed(reports)
    unprocessed.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    total_unprocessed = len(unprocessed)            # before --limit truncates display

    if args.limit:
        unprocessed = unprocessed[: args.limit]

    if args.json:
        json.dump([str(p.relative_to(ROOT)) for p in unprocessed],
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    total_considered = len(reports)
    print(f"Reports considered : {total_considered}")
    print(f"Already in graph   : {total_considered - total_unprocessed}")
    print(f"Unprocessed        : {total_unprocessed}")
    if args.limit and total_unprocessed > args.limit:
        print(f"Showing            : {len(unprocessed)} (newest by mtime; --limit {args.limit})")
    print()
    if not unprocessed:
        print("All caught up.")
        return

    print(f"{'mtime':>19}  path")
    print(f"{'-'*19}  {'-'*60}")
    from datetime import datetime
    for p in unprocessed:
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        rel = p.relative_to(ROOT)
        print(f"{mtime:>19}  {rel}")


if __name__ == "__main__":
    main()
