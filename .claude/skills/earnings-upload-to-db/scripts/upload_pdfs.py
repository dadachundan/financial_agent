#!/usr/bin/env python3
"""Batch-upload PDFs into db/notes.db, mirroring the Notes drag-drop UI.

Usage:
    python3 upload_pdfs.py                          # all .pdf in ~/Downloads (top-level)
    python3 upload_pdfs.py --source ~/some/dir
    python3 upload_pdfs.py --copy                   # copy instead of move
    python3 upload_pdfs.py --dry-run                # report what would happen, no writes
    python3 upload_pdfs.py file1.pdf file2.pdf      # specific files only

The dedup/parse/bucket/insert pipeline lives in notes_app.ingest_pdf,
shared with the Flask /notes/upload route. This script just walks a
source dir, filters obvious skips, and hands each file to that helper
with a `shutil.move` (or `shutil.copy2`) saver.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3].parent  # .claude/skills/earnings-upload-to-db/scripts → financial_agent/
sys.path.insert(0, str(PROJECT_ROOT))

from notes_app import (  # noqa: E402  (sys.path tweak above)
    DB_PATH,
    MANUAL_REPORT_DIR,
    _parse_filename_meta,
    get_conn,
    ingest_pdf,
    init_db,
    ticker_to_bucket,
)


def _collect_pdfs(source: Path, explicit: list[Path]) -> list[Path]:
    if explicit:
        return [p.resolve() for p in explicit if p.suffix.lower() == ".pdf" and p.is_file()]
    if not source.is_dir():
        raise SystemExit(f"Source is not a directory: {source}")
    return sorted(p.resolve() for p in source.glob("*.pdf") if p.is_file())


def _already_managed(path: Path) -> bool:
    try:
        path.relative_to(MANUAL_REPORT_DIR.resolve())
        return True
    except ValueError:
        return False


def _dry_run_preview(src: Path) -> dict:
    """Same dedup + bucket logic ingest_pdf would apply, but read-only."""
    conn = get_conn()
    dup = conn.execute("SELECT id FROM notes WHERE name=?", (src.name,)).fetchone()
    conn.close()
    if dup:
        return {"status": "skipped", "reason": f"already in database: {src.name}"}
    meta = _parse_filename_meta(src.stem)
    bucket = ticker_to_bucket((meta.get("ticker") or "").strip() or "unknown")
    return {
        "status": "would_add",
        "would_move_to": str(MANUAL_REPORT_DIR / bucket / src.name),
        "meta": meta,
    }


def upload(source: Path, copy: bool, dry_run: bool, explicit: list[Path]) -> dict:
    init_db()
    pdfs = _collect_pdfs(source, explicit)

    added: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for src in pdfs:
        if _already_managed(src):
            skipped.append({"file": str(src), "reason": "already in MANUAL_REPORT_DIR"})
            continue

        if dry_run:
            preview = _dry_run_preview(src)
            if preview["status"] == "skipped":
                skipped.append({"file": str(src), "reason": preview["reason"]})
            else:
                added.append({
                    "file": str(src),
                    "would_move_to": preview["would_move_to"],
                    "meta": preview["meta"],
                })
            continue

        def saver(dest: Path, _src: Path = src) -> None:
            if copy:
                shutil.copy2(_src, dest)
            else:
                shutil.move(str(_src), dest)

        result = ingest_pdf(src.name, saver)
        if result["status"] == "added":
            added.append({
                "file": str(src),
                "saved_as": str(result["dest"]),
                "note_id": result["note_id"],
                "meta": result["meta"],
            })
        elif result["status"] == "skipped":
            skipped.append({"file": str(src), "reason": result["reason"]})
        else:
            errors.append({"file": str(src), "error": result["error"]})

    return {
        "db": str(DB_PATH),
        "dest_root": str(MANUAL_REPORT_DIR),
        "dry_run": dry_run,
        "mode": "copy" if copy else "move",
        "scanned": len(pdfs),
        "added_count": len(added),
        "skipped_count": len(skipped),
        "error_count": len(errors),
        "added": added,
        "skipped": skipped,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", type=Path,
                        help="Specific PDF paths (if omitted, scans --source)")
    parser.add_argument("--source", type=Path, default=Path.home() / "Downloads",
                        help="Directory to scan (default ~/Downloads)")
    parser.add_argument("--copy", action="store_true",
                        help="Copy instead of move (default: move)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would happen without touching disk or DB")
    args = parser.parse_args()

    result = upload(
        source=args.source.expanduser(),
        copy=args.copy,
        dry_run=args.dry_run,
        explicit=[p.expanduser() for p in args.files],
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
