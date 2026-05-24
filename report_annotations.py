"""SQLite-backed user annotations (rating + comment) for the /reports/ index.

One row per unique report `pair_key` — the same identifier reports_viewer uses
to collapse EN/ZH/DOCX siblings — so an annotation follows the report no matter
which language file you opened it through.

Stored separately from the markdown source (db/report_annotations.db) so users
can rate / comment without polluting the generated report files.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from threading import Lock

from db_paths import db_path

DB_PATH = db_path("report_annotations.db")
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
                CREATE TABLE IF NOT EXISTS annotations (
                  pair_key            TEXT PRIMARY KEY,
                  rating              INTEGER,
                  comment             TEXT,
                  rated_at            TEXT,
                  comment_updated_at  TEXT
                )
                """
            )
            conn.commit()
        _INITED = True


def get_all() -> dict[str, dict]:
    """Return `{pair_key: {rating, comment, rated_at, comment_updated_at}}` for every row."""
    init_db()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT pair_key, rating, comment, rated_at, comment_updated_at FROM annotations"
        ).fetchall()
    return {r["pair_key"]: dict(r) for r in rows}


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def set_rating(pair_key: str, rating: int) -> None:
    """Set rating 1-5 for a row; rating=0 clears it."""
    init_db()
    rating = max(0, min(5, int(rating or 0)))
    with _LOCK, _conn() as conn:
        if rating == 0:
            conn.execute(
                "INSERT INTO annotations(pair_key, rating, rated_at) VALUES(?, NULL, NULL) "
                "ON CONFLICT(pair_key) DO UPDATE SET rating=NULL, rated_at=NULL",
                (pair_key,),
            )
        else:
            conn.execute(
                "INSERT INTO annotations(pair_key, rating, rated_at) VALUES(?, ?, ?) "
                "ON CONFLICT(pair_key) DO UPDATE SET rating=excluded.rating, rated_at=excluded.rated_at",
                (pair_key, rating, _now()),
            )
        conn.commit()


def set_comment(pair_key: str, comment: str) -> None:
    init_db()
    comment = (comment or "").strip()
    with _LOCK, _conn() as conn:
        if comment:
            conn.execute(
                "INSERT INTO annotations(pair_key, comment, comment_updated_at) VALUES(?, ?, ?) "
                "ON CONFLICT(pair_key) DO UPDATE SET comment=excluded.comment, comment_updated_at=excluded.comment_updated_at",
                (pair_key, comment, _now()),
            )
        else:
            conn.execute(
                "INSERT INTO annotations(pair_key, comment, comment_updated_at) VALUES(?, NULL, NULL) "
                "ON CONFLICT(pair_key) DO UPDATE SET comment=NULL, comment_updated_at=NULL",
                (pair_key,),
            )
        conn.commit()
