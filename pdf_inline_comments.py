"""SQLite-backed inline (selection-anchored) comments for the zsxq PDF viewer.

Each row anchors a comment to a slice of text (or a rectangle) on a specific
page of a PDF identified by zsxq pdf_files.file_id, using:

- A Hypothes.is-style TextQuoteSelector (quote + ~30-char prefix + suffix) for
  re-locating the selection inside the PDF.js text layer on reload, even if the
  layout shifts slightly between sessions.
- A rect (PDF page coords, in CSS pixels at scale=1) as a fallback anchor for
  scanned pages where the text layer is sparse or for region-style highlights.

If neither anchor re-locates on reload, the comment shows in the orphan tray
but is never deleted.

Stored in db/notes.db (next to report_inline_comments) so the PDF on disk
stays untouched. One row per comment; multiple per (file_id, page).
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from threading import Lock

DB_PATH = Path(__file__).parent / "db" / "notes.db"
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
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pdf_inline_comments (
                  id          INTEGER PRIMARY KEY AUTOINCREMENT,
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
    return {
        "id": r["id"],
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


def list_for_file(file_id: int) -> list[dict]:
    init_db()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM pdf_inline_comments WHERE file_id=? "
            "ORDER BY page ASC, id ASC",
            (file_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def create(
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
            "(file_id, page, quote, prefix, suffix, rect_json, body, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (file_id, page, quote, prefix, suffix, rect_json, body, now, now),
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
