#!/usr/bin/env python3
"""One-shot migration: reorganise existing notes PDFs into per-ticker folders.

For every row in db/notes.db we:
  1. Re-derive the ticker from the filename via _parse_filename_meta
     (which now uses db/name_to_ticker.json for symbol mapping).
  2. Compute the target path MANUAL_REPORT_DIR/<ticker>/<filename>.
  3. If the file exists at the old path and old != new, move it
     (auto-renaming on collision).
  4. Update notes.ticker and notes.local_path.
  5. After all moves, remove any now-empty top-level subfolders of
     MANUAL_REPORT_DIR (e.g. the old YYYY-MM-DD dirs).

Usage:
    python3 migrate_to_ticker_buckets.py --dry-run     # report only
    python3 migrate_to_ticker_buckets.py               # apply
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3].parent
sys.path.insert(0, str(PROJECT_ROOT))

from notes_app import (  # noqa: E402
    MANUAL_REPORT_DIR,
    _parse_filename_meta,
    get_conn,
    ticker_to_bucket,
)


def _unique_dest(dest_dir: Path, filename: str) -> Path:
    dest = dest_dir / filename
    i = 1
    while dest.exists():
        dest = dest_dir / f"{Path(filename).stem}_{i}.pdf"
        i += 1
    return dest


def migrate(dry_run: bool) -> dict:
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, local_path, ticker FROM notes ORDER BY id"
    ).fetchall()

    moved: list[dict] = []
    db_only: list[dict] = []
    unchanged: list[dict] = []
    missing: list[dict] = []
    errors: list[dict] = []

    for r in rows:
        note_id = r["id"]
        name = r["name"]
        old_path = Path(r["local_path"]) if r["local_path"] else None
        old_ticker = r["ticker"]

        meta = _parse_filename_meta(Path(name).stem)
        new_ticker = (meta.get("ticker") or "unknown").strip() or "unknown"
        new_dir = MANUAL_REPORT_DIR / ticker_to_bucket(new_ticker)

        # Decide target path
        if old_path and old_path.exists():
            if old_path.parent == new_dir:
                # Already in the right folder — only DB column may need refresh
                if old_ticker == new_ticker:
                    unchanged.append({"id": note_id, "name": name, "ticker": new_ticker})
                    continue
                if not dry_run:
                    conn.execute("UPDATE notes SET ticker=? WHERE id=?", (new_ticker, note_id))
                db_only.append({
                    "id": note_id, "name": name,
                    "old_ticker": old_ticker, "new_ticker": new_ticker,
                })
                continue

            new_path = _unique_dest(new_dir, name) if not dry_run else new_dir / name
            try:
                if not dry_run:
                    new_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(old_path), new_path)
                    conn.execute(
                        "UPDATE notes SET local_path=?, ticker=? WHERE id=?",
                        (str(new_path), new_ticker, note_id),
                    )
                moved.append({
                    "id": note_id, "name": name,
                    "from": str(old_path), "to": str(new_path),
                    "old_ticker": old_ticker, "new_ticker": new_ticker,
                })
            except Exception as exc:
                errors.append({"id": note_id, "name": name, "error": str(exc)})
            continue

        # File missing on disk — just update DB columns
        if old_ticker != new_ticker:
            if not dry_run:
                conn.execute("UPDATE notes SET ticker=? WHERE id=?", (new_ticker, note_id))
            db_only.append({
                "id": note_id, "name": name,
                "old_ticker": old_ticker, "new_ticker": new_ticker,
                "note": "file missing on disk",
            })
        else:
            missing.append({"id": note_id, "name": name, "local_path": str(old_path or "")})

    if not dry_run:
        conn.commit()
    conn.close()

    # Sweep top-level dirs under MANUAL_REPORT_DIR that contain only macOS junk
    swept_dirs: list[str] = []
    if not dry_run and MANUAL_REPORT_DIR.exists():
        for sub in sorted(MANUAL_REPORT_DIR.iterdir()):
            if not sub.is_dir():
                continue
            entries = list(sub.iterdir())
            if all(e.name in {".DS_Store", "Thumbs.db"} for e in entries):
                try:
                    for e in entries:
                        e.unlink()
                    sub.rmdir()
                    swept_dirs.append(str(sub))
                except Exception:
                    pass

    return {
        "dry_run": dry_run,
        "total_rows": len(rows),
        "moved_count": len(moved),
        "db_only_count": len(db_only),
        "unchanged_count": len(unchanged),
        "file_missing_count": len(missing),
        "error_count": len(errors),
        "swept_empty_dirs": swept_dirs,
        "moved": moved,
        "db_only": db_only,
        "file_missing": missing,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = migrate(dry_run=args.dry_run)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
