"""
kg_db.py — Database connection, schema, and seed data for the knowledge graph.
"""

import sqlite3
from pathlib import Path

# Resolved at import time so callers can do: from kg_db import get_db, init_db
_DB_PATH: Path | None = None   # set by knowledge_graph.main()


def set_db_path(path: Path) -> None:
    global _DB_PATH
    _DB_PATH = path


def get_db_path() -> Path:
    if _DB_PATH is None:
        raise RuntimeError("DB path not set; call kg_db.set_db_path() first")
    return _DB_PATH


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ── Schema ────────────────────────────────────────────────────────────────────

_DDL = """
CREATE TABLE IF NOT EXISTS companies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS businesses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    description TEXT    NOT NULL DEFAULT ''
);

-- Company participates in / focuses on a business
CREATE TABLE IF NOT EXISTS business_company (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    company_id  INTEGER NOT NULL REFERENCES companies(id)  ON DELETE CASCADE,
    comment     TEXT    NOT NULL DEFAULT '',
    explanation TEXT    NOT NULL DEFAULT '',
    image_path  TEXT    NOT NULL DEFAULT '',
    source_url  TEXT    NOT NULL DEFAULT '',
    UNIQUE(business_id, company_id)
);

-- Two businesses are related
CREATE TABLE IF NOT EXISTS business_business (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    business_from INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    business_to   INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    comment       TEXT    NOT NULL DEFAULT '',
    explanation   TEXT    NOT NULL DEFAULT '',
    image_path    TEXT    NOT NULL DEFAULT '',
    source_url    TEXT    NOT NULL DEFAULT '',
    UNIQUE(business_from, business_to)
);
"""

_MIGRATIONS = [
    "ALTER TABLE business_company ADD COLUMN rating INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE business_business ADD COLUMN rating INTEGER NOT NULL DEFAULT 0",
    # Track which zsxq.db file_ids have already been imported
    """CREATE TABLE IF NOT EXISTS zsxq_imported (
        file_id     INTEGER PRIMARY KEY,
        imported_at TEXT    NOT NULL DEFAULT (datetime('now'))
    )""",
    "ALTER TABLE business_company ADD COLUMN created_at TEXT",
    "ALTER TABLE business_business ADD COLUMN created_at TEXT",
    # Auto-set created_at on INSERT via triggers (SQLite doesn't allow datetime('now') as ALTER TABLE default)
    """CREATE TRIGGER IF NOT EXISTS bc_set_created_at
       AFTER INSERT ON business_company WHEN NEW.created_at IS NULL
       BEGIN UPDATE business_company SET created_at = datetime('now') WHERE id = NEW.id; END""",
    """CREATE TRIGGER IF NOT EXISTS bb_set_created_at
       AFTER INSERT ON business_business WHEN NEW.created_at IS NULL
       BEGIN UPDATE business_business SET created_at = datetime('now') WHERE id = NEW.id; END""",
    "ALTER TABLE business_company ADD COLUMN source_text TEXT NOT NULL DEFAULT ''",
    "ALTER TABLE business_business ADD COLUMN source_text TEXT NOT NULL DEFAULT ''",
]


def init_db(upload_dir: Path) -> None:
    upload_dir.mkdir(parents=True, exist_ok=True)
    with get_db() as conn:
        conn.executescript(_DDL)
        for stmt in _MIGRATIONS:
            try:
                conn.execute(stmt)
            except Exception:
                pass  # column already exists


# ── Seed data ─────────────────────────────────────────────────────────────────

def seed_db() -> None:
    """Insert minimal seed data if all tables are empty."""
    with get_db() as conn:
        if conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0] > 0:
            return

        conn.execute(
            "INSERT OR IGNORE INTO companies (name, description) VALUES (?, ?)",
            ("NVDA", "NVIDIA — GPU & AI accelerator leader"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO businesses (name, description) VALUES (?, ?)",
            ("GPU", "Graphics Processing Unit — massively parallel compute"),
        )
        nvda_id = conn.execute("SELECT id FROM companies  WHERE name='NVDA'").fetchone()["id"]
        gpu_id  = conn.execute("SELECT id FROM businesses WHERE name='GPU'").fetchone()["id"]
        conn.execute(
            "INSERT OR IGNORE INTO business_company (business_id, company_id, comment) VALUES (?,?,?)",
            (gpu_id, nvda_id, "NVIDIA's core revenue driver"),
        )
