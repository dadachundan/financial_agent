#!/usr/bin/env python3
"""Batch-upload PDFs into db/notes.db, mirroring the Notes drag-drop UI.

Usage:
    python3 upload_pdfs.py                          # all .pdf in ~/Downloads (top-level)
    python3 upload_pdfs.py --source ~/some/dir
    python3 upload_pdfs.py --copy                   # copy instead of move
    python3 upload_pdfs.py --dry-run                # report what would happen, no writes
    python3 upload_pdfs.py file1.pdf file2.pdf      # specific files only

Per file we:
  1. Skip non-PDFs and anything already living under MANUAL_REPORT_DIR.
  2. Dedupe against notes.name (same filename → skip).
  3. Parse filename → type / quarter / report_date / ticker.
  4. Move (or copy) to MANUAL_REPORT_DIR/<ticker>/ (fallback "unknown"),
     auto-renaming on collision.
  5. INSERT into notes table.

Output is JSON-friendly per-file lines plus a final summary, so Claude
can pick up counts and any errors at a glance.
"""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path

_UNKNOWN_BUCKET = "unknown"

PROJECT_ROOT = Path(__file__).resolve().parents[3].parent  # .claude/skills/earnings-upload-to-db/scripts → financial_agent/
sys.path.insert(0, str(PROJECT_ROOT))

from notes_app import (  # noqa: E402  (sys.path tweak above)
    DB_PATH,
    MANUAL_REPORT_DIR,
    _parse_filename_meta,
    get_conn,
    init_db,
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


def _unique_dest(dest_dir: Path, filename: str) -> Path:
    dest = dest_dir / filename
    i = 1
    while dest.exists():
        dest = dest_dir / f"{Path(filename).stem}_{i}.pdf"
        i += 1
    return dest


def upload(source: Path, copy: bool, dry_run: bool, explicit: list[Path]) -> dict:
    init_db()
    pdfs = _collect_pdfs(source, explicit)

    conn = get_conn()
    existing = {r[0] for r in conn.execute("SELECT name FROM notes").fetchall()}
    conn.close()

    added: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for src in pdfs:
        if _already_managed(src):
            skipped.append({"file": str(src), "reason": "already in MANUAL_REPORT_DIR"})
            continue
        if src.name in existing:
            skipped.append({"file": str(src), "reason": "filename already in DB"})
            continue

        meta = _parse_filename_meta(src.stem)
        bucket = (meta.get("ticker") or _UNKNOWN_BUCKET).strip() or _UNKNOWN_BUCKET
        dest_dir = MANUAL_REPORT_DIR / bucket

        if dry_run:
            added.append({
                "file": str(src),
                "would_move_to": str(dest_dir / src.name),
                "meta": meta,
            })
            continue

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = _unique_dest(dest_dir, src.name)
            if copy:
                shutil.copy2(src, dest)
            else:
                shutil.move(str(src), dest)
        except Exception as exc:
            errors.append({"file": str(src), "error": f"file op failed: {exc}"})
            continue

        try:
            now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            conn = get_conn()
            cur = conn.execute(
                """INSERT INTO notes (name, local_path, created_at, type, quarter, report_date, ticker)
                   VALUES (?,?,?,?,?,?,?)""",
                (dest.name, str(dest), now,
                 meta.get("type"), meta.get("quarter"),
                 meta.get("report_date"), meta.get("ticker")),
            )
            note_id = cur.lastrowid
            conn.commit()
            conn.close()
        except Exception as exc:
            errors.append({"file": str(src), "error": f"db insert failed: {exc}"})
            continue

        existing.add(dest.name)
        added.append({
            "file": str(src),
            "saved_as": str(dest),
            "note_id": note_id,
            "meta": meta,
        })

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
