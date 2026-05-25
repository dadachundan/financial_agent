"""SQLite-backed inline (selection-anchored) comments for the PDF viewer.

Each row anchors a comment to a slice of text (or a rectangle) on a specific
page of a PDF identified by (source, file_id). `source` is one of 'zsxq',
'sec', 'cn', 'manual' so the same viewer can render any of the four PDF
libraries without primary-key collisions. Anchoring uses:

- A Hypothes.is-style TextQuoteSelector (quote + ~30-char prefix + suffix) for
  re-locating the selection inside the PDF.js text layer on reload, even if the
  layout shifts slightly between sessions.
- A rect (PDF page coords, in CSS pixels at scale=1) as a fallback anchor for
  scanned pages where the text layer is sparse or for region-style highlights.

If neither anchor re-locates on reload, the comment shows in the orphan tray
but is never deleted.

Stored in db/notes.db (next to report_inline_comments) so the PDFs on disk
stay untouched. One row per comment; multiple per (source, file_id, page).

If the `source` column is missing from an existing `pdf_inline_comments`
table, run `python migrate_add_source_to_pdf_tables.py` once — `init_db()`
won't auto-migrate live user data (see CLAUDE.md DB-safety rule).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from threading import Lock

from db_paths import db_path

DB_PATH = db_path("notes.db")
_LOCK = Lock()
_INITED = False


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    global _INITED
    if _INITED:
        return
    with _LOCK:
        if _INITED:
            return
        with _conn() as conn:
            # Fresh table — created with the `source` column from the start.
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pdf_inline_comments (
                  id          INTEGER PRIMARY KEY AUTOINCREMENT,
                  source      TEXT NOT NULL DEFAULT 'zsxq',
                  file_id     INTEGER NOT NULL,
                  page        INTEGER NOT NULL,
                  quote       TEXT NOT NULL DEFAULT '',
                  prefix      TEXT NOT NULL DEFAULT '',
                  suffix      TEXT NOT NULL DEFAULT '',
                  rect_json   TEXT,
                  body        TEXT NOT NULL,
                  created_at  TEXT NOT NULL,
                  updated_at  TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_pic_file_id "
                "ON pdf_inline_comments(file_id)"
            )
            # Pre-existing tables may not have `source` yet — bring them
            # up to date with a purely-additive ADD COLUMN (sets all
            # existing rows to 'zsxq', which matches what they were).
            # Same self-healing pattern as `CREATE TABLE IF NOT EXISTS`.
            cols = {r[1] for r in conn.execute("PRAGMA table_info(pdf_inline_comments)")}
            if "source" not in cols:
                print(
                    "[pdf_inline_comments] adding `source` column "
                    "(default 'zsxq') to existing table"
                )
                conn.execute(
                    "ALTER TABLE pdf_inline_comments "
                    "ADD COLUMN source TEXT NOT NULL DEFAULT 'zsxq'"
                )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_pic_source_file "
                "ON pdf_inline_comments(source, file_id)"
            )
            conn.commit()
        _INITED = True


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_to_dict(r: sqlite3.Row) -> dict:
    rect = None
    if r["rect_json"]:
        try:
            rect = json.loads(r["rect_json"])
        except Exception:
            rect = None
    # `source` may be absent on pre-migration rows; default to 'zsxq' to match
    # historical reality (the table only held zsxq data before).
    try:
        source = r["source"] or "zsxq"
    except (IndexError, KeyError):
        source = "zsxq"
    return {
        "id": r["id"],
        "source": source,
        "file_id": r["file_id"],
        "page": r["page"],
        "quote": r["quote"],
        "prefix": r["prefix"],
        "suffix": r["suffix"],
        "rect": rect,
        "body": r["body"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
    }


def list_for_file(source: str, file_id: int) -> list[dict]:
    init_db()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM pdf_inline_comments WHERE source=? AND file_id=? "
            "ORDER BY page ASC, id ASC",
            (source, file_id),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def create(
    source: str,
    file_id: int,
    page: int,
    quote: str,
    prefix: str,
    suffix: str,
    rect: dict | None,
    body: str,
) -> dict:
    init_db()
    now = _now()
    rect_json = json.dumps(rect) if rect else None
    with _LOCK, _conn() as conn:
        cur = conn.execute(
            "INSERT INTO pdf_inline_comments "
            "(source, file_id, page, quote, prefix, suffix, rect_json, body, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (source, file_id, page, quote, prefix, suffix, rect_json, body, now, now),
        )
        new_id = cur.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT * FROM pdf_inline_comments WHERE id=?", (new_id,)
        ).fetchone()
    return _row_to_dict(row)


def update(comment_id: int, body: str) -> dict | None:
    init_db()
    now = _now()
    with _LOCK, _conn() as conn:
        conn.execute(
            "UPDATE pdf_inline_comments SET body=?, updated_at=? WHERE id=?",
            (body, now, comment_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM pdf_inline_comments WHERE id=?", (comment_id,)
        ).fetchone()
    return _row_to_dict(row) if row else None


def delete(comment_id: int) -> bool:
    init_db()
    with _LOCK, _conn() as conn:
        cur = conn.execute(
            "DELETE FROM pdf_inline_comments WHERE id=?", (comment_id,)
        )
        conn.commit()
        return cur.rowcount > 0
