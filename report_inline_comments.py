"""SQLite-backed inline (selection-anchored) comments for the /reports/ MD viewer.

Each row anchors a comment to a slice of text in a rendered markdown report
using a Hypothes.is-style TextQuoteSelector: the exact quote plus ~30 chars
of prefix and suffix. On reload the frontend re-locates the quote in the
(possibly regenerated) document; if it can't be found, the comment is shown
as an "orphan" in a sidebar but never deleted.

Stored in db/notes.db (alongside the PDF-notes table) so the markdown
source stays untouched. One row per comment; multiple per report.
"""
from __future__ import annotations

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
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS report_inline_comments (
                  id              INTEGER PRIMARY KEY AUTOINCREMENT,
                  report_path     TEXT NOT NULL,
                  quote           TEXT NOT NULL,
                  prefix          TEXT NOT NULL DEFAULT '',
                  suffix          TEXT NOT NULL DEFAULT '',
                  heading_anchor  TEXT,
                  body            TEXT NOT NULL,
                  created_at      TEXT NOT NULL,
                  updated_at      TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_ric_report_path "
                "ON report_inline_comments(report_path)"
            )
            conn.commit()
        _INITED = True


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_to_dict(r: sqlite3.Row) -> dict:
    return {
        "id": r["id"],
        "quote": r["quote"],
        "prefix": r["prefix"],
        "suffix": r["suffix"],
        "heading_anchor": r["heading_anchor"],
        "body": r["body"],
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
    }


def list_for_report(report_path: str) -> list[dict]:
    init_db()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM report_inline_comments WHERE report_path=? "
            "ORDER BY id ASC",
            (report_path,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def create(
    report_path: str,
    quote: str,
    prefix: str,
    suffix: str,
    heading_anchor: str | None,
    body: str,
) -> dict:
    init_db()
    now = _now()
    with _LOCK, _conn() as conn:
        cur = conn.execute(
            "INSERT INTO report_inline_comments "
            "(report_path, quote, prefix, suffix, heading_anchor, body, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (report_path, quote, prefix, suffix, heading_anchor, body, now, now),
        )
        new_id = cur.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT * FROM report_inline_comments WHERE id=?", (new_id,)
        ).fetchone()
    return _row_to_dict(row)


def update(comment_id: int, body: str) -> dict | None:
    init_db()
    now = _now()
    with _LOCK, _conn() as conn:
        conn.execute(
            "UPDATE report_inline_comments SET body=?, updated_at=? WHERE id=?",
            (body, now, comment_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM report_inline_comments WHERE id=?", (comment_id,)
        ).fetchone()
    return _row_to_dict(row) if row else None


def delete(comment_id: int) -> bool:
    init_db()
    with _LOCK, _conn() as conn:
        cur = conn.execute(
            "DELETE FROM report_inline_comments WHERE id=?", (comment_id,)
        )
        conn.commit()
        return cur.rowcount > 0
