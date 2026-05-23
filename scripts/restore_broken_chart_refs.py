"""One-shot script: restore charts deleted in 423d8f7 and rewrite refs.

Background. Commit 215399f migrated chart PNGs from the shared
`reports/charts/` folder into per-doc `<doc_dir>/charts/` subdirs based on
a manifest, then 423d8f7 deleted everything that wasn't in the manifest
as "orphans". Several reports were added between the manifest build and
those commits — their .md files still reference `](../../charts/<name>.png)`
and the route's shared-folder fallback was removed, so every such image
is broken at /claude-reports/view/.

This script:
1. Finds every .md under reports/ that still uses `](../../charts/*.png)`.
2. For each chart filename, runs `git show 423d8f7^:reports/charts/<name>`
   to recover the deleted PNG bytes.
3. Writes it into `<doc_dir>/charts/<name>` (creating the dir if needed).
4. Rewrites the .md to use the per-doc `charts/<name>` convention.

Run from the repo root. Idempotent — only touches files with the broken
`../../charts/` pattern. Skips (and reports) any chart that no longer
exists in 423d8f7^ so the user can decide what to do with it.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
RECOVERY_REV = "423d8f7^"
REF_RE = re.compile(r"\]\(\.\./\.\./charts/([^)]+)\)")


def find_affected_md_files() -> list[Path]:
    out = subprocess.run(
        ["grep", "-rlE", r"\]\(\.\./\.\./charts/", str(REPORTS)],
        capture_output=True, text=True, check=False,
    )
    return [Path(p) for p in out.stdout.strip().splitlines() if p]


_SIBLING_CACHE: dict[str, Path] | None = None


def _sibling_chart_index() -> dict[str, Path]:
    """Map basename → existing per-doc charts/<basename> on disk.

    Some PNGs were moved out of reports/charts/ by 215399f before the
    orphan-cleanup ran, so `git show 423d8f7^:reports/charts/<name>` can't
    recover them. In that case we copy from whatever sibling doc already
    owns the file (the Sanhua HKEX/SZSE cross-reference case).
    """
    global _SIBLING_CACHE
    if _SIBLING_CACHE is not None:
        return _SIBLING_CACHE
    idx: dict[str, Path] = {}
    for p in REPORTS.rglob("charts/*.png"):
        idx.setdefault(p.name, p)
    _SIBLING_CACHE = idx
    return idx


def restore_blob(name: str, dest: Path) -> bool:
    """Restore a deleted chart PNG to `dest`. Tries two sources in order:
    1. `git show 423d8f7^:reports/charts/<name>` (orphan-cleanup snapshot).
    2. An existing per-doc `<other_doc>/charts/<name>` on disk (PNGs that
       were migrated away from the shared folder before the cleanup).
    Returns True on success.
    """
    git_path = f"{RECOVERY_REV}:reports/charts/{name}"
    proc = subprocess.run(
        ["git", "show", git_path],
        capture_output=True, check=False,
    )
    if proc.returncode == 0:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(proc.stdout)
        return True

    sibling = _sibling_chart_index().get(name)
    if sibling and sibling != dest:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(sibling.read_bytes())
        return True

    return False


def process(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    refs = REF_RE.findall(text)
    if not refs:
        return {"path": md_path, "refs": [], "restored": [], "missing": []}

    doc_dir = md_path.parent
    charts_dir = doc_dir / "charts"
    restored, missing = [], []
    for name in sorted(set(refs)):
        dest = charts_dir / name
        if dest.exists():
            restored.append(name)
            continue
        if restore_blob(name, dest):
            restored.append(name)
        else:
            missing.append(name)

    # Only rewrite paths whose PNG we managed to restore (so we don't trade
    # one broken ref for another). If any are still missing, log and skip
    # the path rewrite for those specific files.
    if missing:
        return {"path": md_path, "refs": refs, "restored": restored, "missing": missing}

    new_text = REF_RE.sub(r"](charts/\1)", text)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
    return {"path": md_path, "refs": refs, "restored": restored, "missing": []}


def main():
    affected = find_affected_md_files()
    print(f"Found {len(affected)} affected .md files")

    total_refs = 0
    total_restored = 0
    docs_with_missing = []
    all_missing: set[str] = set()

    for md in affected:
        r = process(md)
        rel = md.relative_to(ROOT)
        total_refs += len(set(r["refs"]))
        total_restored += len(r["restored"])
        if r["missing"]:
            docs_with_missing.append((rel, r["missing"]))
            all_missing.update(r["missing"])
            print(f"  ⚠ {rel}: missing {len(r['missing'])} — {r['missing']}")

    print("")
    print(f"Restored: {total_restored} chart copies across {len(affected)} docs")
    print(f"Missing PNGs (not in {RECOVERY_REV}): {len(all_missing)}")
    if all_missing:
        print(f"  filenames: {sorted(all_missing)}")
    print(f"Docs left partially broken: {len(docs_with_missing)}")
    return 0 if not docs_with_missing else 1


if __name__ == "__main__":
    sys.exit(main())
