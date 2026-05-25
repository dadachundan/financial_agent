"""One-shot migration: add `source` column to pdf_inline_comments + pdf_page_ocr.

Both tables originally stored zsxq-only data keyed by `file_id`. Now they're
shared across four PDF sources (zsxq, sec, cn, manual) so the (source, file_id)
pair is what really identifies a document. This migration adds the column with
DEFAULT 'zsxq', which preserves existing rows correctly (they ARE zsxq data).

Idempotent — re-running is a no-op. Safe under any FINAGENT_DB_DIR.

Running this manually is OPTIONAL: pdf_inline_comments.init_db() and
pdf_page_ocr.init_db() now do the same ADD COLUMN themselves on first
import (same self-healing pattern as `CREATE TABLE IF NOT EXISTS`). The
script is kept for users who want to inspect and apply the schema change
before starting the app.

Run with:
    python migrate_add_source_to_pdf_tables.py
"""
from __future__ import annotations

import sqlite3
import sys

from db_paths import db_path


def _has_col(conn: sqlite3.Connection, table: str, col: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == col for r in rows)


def _has_index(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='index' AND name=?",
        (name,),
    ).fetchone()
    return row is not None


def main() -> int:
    notes = db_path("notes.db")
    print(f"Migrating: {notes}")
    if not notes.exists():
        print(f"  notes.db not found — nothing to migrate, skipping.")
        return 0

    conn = sqlite3.connect(notes)
    try:
        # pdf_inline_comments — add `source` column + composite index.
        if not _has_col(conn, "pdf_inline_comments", "source"):
            print("  pdf_inline_comments: ADD COLUMN source TEXT NOT NULL DEFAULT 'zsxq'")
            conn.execute(
                "ALTER TABLE pdf_inline_comments "
                "ADD COLUMN source TEXT NOT NULL DEFAULT 'zsxq'"
            )
        else:
            print("  pdf_inline_comments: 'source' column already present, skipping")
        if not _has_index(conn, "idx_pic_source_file"):
            print("  pdf_inline_comments: CREATE INDEX idx_pic_source_file(source,file_id)")
            conn.execute(
                "CREATE INDEX idx_pic_source_file "
                "ON pdf_inline_comments(source, file_id)"
            )
        else:
            print("  pdf_inline_comments: idx_pic_source_file already present, skipping")

        # pdf_page_ocr — add `source` column.
        # Note: the existing PRIMARY KEY (file_id, page) stays. In practice
        # zsxq file_ids live in the ~10^14 range and sec/cn/manual ids are
        # small (< 10^6), so cross-source collisions are extremely unlikely.
        # When one does happen, the cache silently overwrites and the next
        # page-open triggers a single fresh OCR — graceful degradation.
        if not _has_col(conn, "pdf_page_ocr", "source"):
            print("  pdf_page_ocr: ADD COLUMN source TEXT NOT NULL DEFAULT 'zsxq'")
            conn.execute(
                "ALTER TABLE pdf_page_ocr "
                "ADD COLUMN source TEXT NOT NULL DEFAULT 'zsxq'"
            )
        else:
            print("  pdf_page_ocr: 'source' column already present, skipping")

        conn.commit()
    finally:
        conn.close()

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
