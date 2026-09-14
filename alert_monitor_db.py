"""SQLite storage for the alert monitor (``db/alert_monitor.db``).

One table, ``alerts``. Every alert is a row and they all behave the same way:
the TradingView seeds the app ships with are simply the rows inserted on first
run, and alerts added from the UI are appended beside them. Nothing afterwards
distinguishes a seeded row from an added one.

Deleting never removes a row -- it stamps ``obsolete_at``, so the history (what
was tracked, when it was added, when it was retired) survives. ``created_at``
is when the alert was added, ``obsolete_at`` is NULL while the alert is live.

Paths resolve through :func:`db_paths.db_path`, so ``FINAGENT_DB_DIR``
redirects writes to a sandbox copy during tests, per the *Database Safety* rule
in :file:`CLAUDE.md`.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from db_paths import backup_db, db_path, harden

DB_NAME = "alert_monitor.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS alerts (
    id            TEXT PRIMARY KEY,
    ticker        TEXT NOT NULL,             -- display ticker, e.g. "6869", "MSFT"
    yf_symbol     TEXT NOT NULL,             -- yfinance symbol, e.g. "6869.HK"
    description   TEXT NOT NULL,             -- "6869 Crossing 100.5"
    alert_price   REAL NOT NULL,
    company       TEXT NOT NULL DEFAULT '',
    exchange      TEXT NOT NULL DEFAULT '',  -- short venue label, e.g. "HKEX"
    exchange_full TEXT NOT NULL DEFAULT '',  -- "Hong Kong Stock Exchange"
    created_at    TEXT NOT NULL,             -- when the alert was added (local ISO 8601)
    obsolete_at   TEXT                       -- when it was deleted; NULL = still live
);

CREATE INDEX IF NOT EXISTS idx_alerts_symbol   ON alerts(yf_symbol);
CREATE INDEX IF NOT EXISTS idx_alerts_obsolete ON alerts(obsolete_at);

-- A live alert is unique per (symbol, price). Deleting one frees the pair
-- again, which is why the index is partial.
CREATE UNIQUE INDEX IF NOT EXISTS uq_alerts_live
    ON alerts(yf_symbol, alert_price) WHERE obsolete_at IS NULL;
"""

FIELDS = ("id", "ticker", "yf_symbol", "description", "alert_price",
          "company", "exchange", "exchange_full", "created_at", "obsolete_at")


class DuplicateAlert(Exception):
    """A live alert already exists for this (symbol, price)."""


def now_iso() -> str:
    """Timestamp used for ``created_at`` / ``obsolete_at``."""
    return datetime.now().isoformat(timespec="seconds")


def _path() -> Path:
    """Resolve the DB file at call time so FINAGENT_DB_DIR is always honoured."""
    return db_path(DB_NAME)


@contextmanager
def _conn():
    """Open the DB, apply the schema, hand out a connection."""
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = harden(sqlite3.connect(path))
    con.row_factory = sqlite3.Row
    try:
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


def _as_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {key: row[key] for key in FIELDS}


def list_alerts(include_obsolete: bool = False) -> list[dict[str, Any]]:
    """Alerts in the order they were added, oldest first."""
    sql = "SELECT * FROM alerts"
    if not include_obsolete:
        sql += " WHERE obsolete_at IS NULL"
    sql += " ORDER BY created_at, rowid"
    with _conn() as c:
        return [_as_dict(row) for row in c.execute(sql)]


def count(include_obsolete: bool = True) -> int:
    sql = "SELECT COUNT(*) FROM alerts"
    if not include_obsolete:
        sql += " WHERE obsolete_at IS NULL"
    with _conn() as c:
        return c.execute(sql).fetchone()[0]


def get_alert(alert_id: str) -> dict[str, Any] | None:
    with _conn() as c:
        row = c.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
    return _as_dict(row) if row else None


def find_live(yf_symbol: str, alert_price: float) -> dict[str, Any] | None:
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM alerts WHERE obsolete_at IS NULL"
            " AND yf_symbol = ? AND alert_price = ?",
            (yf_symbol, alert_price),
        ).fetchone()
    return _as_dict(row) if row else None


def insert_alert(row: dict[str, Any]) -> dict[str, Any]:
    """Add one alert. Raises :class:`DuplicateAlert` on a live symbol/price clash."""
    values = {
        "id": str(row["id"]),
        "ticker": str(row["ticker"]),
        "yf_symbol": str(row["yf_symbol"]),
        "description": str(row["description"]),
        "alert_price": float(row["alert_price"]),
        "company": str(row.get("company") or ""),
        "exchange": str(row.get("exchange") or ""),
        "exchange_full": str(row.get("exchange_full") or ""),
        "created_at": str(row.get("created_at") or now_iso()),
        "obsolete_at": str(row.get("obsolete_at") or "") or None,
    }
    cols = ", ".join(values)
    marks = ", ".join("?" for _ in values)
    try:
        with _conn() as c:
            c.execute(f"INSERT INTO alerts ({cols}) VALUES ({marks})", list(values.values()))
    except sqlite3.IntegrityError as exc:
        raise DuplicateAlert(str(exc)) from exc
    return values


def set_obsolete(alert_id: str, when: str | None = None) -> str | None:
    """Mark a live alert obsolete. None if it is missing or already obsolete."""
    stamp = when or now_iso()
    with _conn() as c:
        cur = c.execute(
            "UPDATE alerts SET obsolete_at = ? WHERE id = ? AND obsolete_at IS NULL",
            (stamp, alert_id),
        )
        return stamp if cur.rowcount else None


def clear_obsolete(alert_id: str) -> bool:
    """Bring an obsolete alert back. False if missing or already live.

    Raises :class:`DuplicateAlert` when a live alert already tracks the same
    symbol and price.
    """
    try:
        with _conn() as c:
            cur = c.execute(
                "UPDATE alerts SET obsolete_at = NULL WHERE id = ? AND obsolete_at IS NOT NULL",
                (alert_id,),
            )
            return cur.rowcount > 0
    except sqlite3.IntegrityError as exc:
        raise DuplicateAlert(str(exc)) from exc


def init_db(seeds: Iterable[dict[str, Any]] = ()) -> bool:
    """Create the table, back up an existing one, seed a fresh one.

    Returns True when the table was empty, i.e. when ``seeds`` were just
    inserted -- the caller uses that to know a fresh install needs migrating.
    Idempotent and safe to call on every start.
    """
    existed = _path().exists()
    with _conn():
        pass  # the context manager applies SCHEMA
    if existed:
        backup_db(DB_NAME)
    if count() > 0:
        return False
    stamp = now_iso()
    for row in seeds:
        item = dict(row)
        item["created_at"] = item.get("created_at") or stamp
        try:
            insert_alert(item)
        except DuplicateAlert:
            pass
    return True


if __name__ == "__main__":
    # Smoke test
    print(f"DB = {_path()}")
    print(f"Alerts: {count()} total, {count(include_obsolete=False)} live")
    for alert in list_alerts(include_obsolete=True):
        state = f"obsolete {alert['obsolete_at']}" if alert["obsolete_at"] else "live"
        print(f"  {alert['id']:<24} {alert['description']:<28} added {alert['created_at']} ({state})")
