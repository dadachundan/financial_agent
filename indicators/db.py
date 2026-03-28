"""SQLite persistence for indicator snapshots and history."""

import json
import sqlite3
import time
from pathlib import Path

_DB_PATH: Path = Path(__file__).parent.parent / "db" / "indicators.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    id        INTEGER PRIMARY KEY,
    fetched_at INTEGER NOT NULL,           -- unix timestamp
    data_json  TEXT    NOT NULL            -- full serialised fetch_all() result
);

CREATE TABLE IF NOT EXISTS history (
    symbol  TEXT    NOT NULL,
    date    TEXT    NOT NULL,              -- YYYY-MM-DD
    value   REAL,
    PRIMARY KEY (symbol, date)
);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


# ── snapshots ────────────────────────────────────────────────────────────────

def save_snapshot(data: dict) -> None:
    """Persist a full fetch_all() result with current timestamp."""
    conn = get_conn()
    conn.execute(
        "INSERT INTO snapshots (fetched_at, data_json) VALUES (?, ?)",
        (int(time.time()), json.dumps(data)),
    )
    # Keep only the last 20 snapshots
    conn.execute(
        "DELETE FROM snapshots WHERE id NOT IN "
        "(SELECT id FROM snapshots ORDER BY fetched_at DESC LIMIT 20)"
    )
    conn.commit()

    # Also persist history rows
    for ind_id, rec in data.items():
        for pt in rec.get("history", []):
            try:
                conn.execute(
                    "INSERT OR REPLACE INTO history (symbol, date, value) VALUES (?, ?, ?)",
                    (ind_id, pt["date"], pt["value"]),
                )
            except Exception:
                pass
    conn.commit()
    conn.close()


def get_latest_snapshot() -> tuple[dict | None, int]:
    """Return (data_dict, fetched_at_unix). data_dict is None if no snapshot exists."""
    conn = get_conn()
    row = conn.execute(
        "SELECT data_json, fetched_at FROM snapshots ORDER BY fetched_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if row is None:
        return None, 0
    return json.loads(row["data_json"]), row["fetched_at"]


def snapshot_age_seconds() -> int:
    """Seconds since last snapshot, or very large number if none exists."""
    _, ts = get_latest_snapshot()
    if ts == 0:
        return 10 ** 9
    return int(time.time()) - ts


def get_history(ind_id: str) -> list[dict]:
    """Return [{date, value}, ...] sorted by date for a given indicator id."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT date, value FROM history WHERE symbol=? ORDER BY date",
        (ind_id,),
    ).fetchall()
    conn.close()
    return [{"date": r["date"], "value": r["value"]} for r in rows]
