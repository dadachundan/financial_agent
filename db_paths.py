"""Single source of truth for ``*.db`` file locations.

Every Python module in this project that opens a SQLite database MUST
resolve its path through :func:`db_path` (or :func:`db_dir`). That way,
setting the environment variable ``FINAGENT_DB_DIR`` redirects ALL
databases at once to a sandbox directory — which is the only approved
mechanism for testing code that writes to a DB, per the *Database
Safety* rule in :file:`CLAUDE.md`.

Example — test a feature without touching real data::

    cp db/notes.db /tmp/test-dbs/notes.db          # one-time per session
    cp db/zsxq.db  /tmp/test-dbs/zsxq.db
    FINAGENT_DB_DIR=/tmp/test-dbs python main.py --port 5002
    # ... exercise the feature, write to /tmp/test-dbs/* freely ...
    rm -rf /tmp/test-dbs

If ``FINAGENT_DB_DIR`` is unset, modules fall back to ``./db/`` next to
this file — exactly the historical behaviour. No production code paths
change.
"""
from __future__ import annotations

import os
import sqlite3
import time
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent
_DEFAULT_DB_DIR: Path = PROJECT_ROOT / "db"


def db_dir() -> Path:
    """Return the directory holding all ``*.db`` files.

    Honors the ``FINAGENT_DB_DIR`` environment variable; falls back to
    ``<project_root>/db``. The returned path is absolute and resolved.
    Directory creation is left to the caller — this function is pure.
    """
    env = os.environ.get("FINAGENT_DB_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return _DEFAULT_DB_DIR


def db_path(filename: str) -> Path:
    """Resolve a single ``*.db`` file path. Equivalent to ``db_dir() / filename``.

    Always use this rather than constructing the path manually; that's
    what lets ``FINAGENT_DB_DIR`` redirect tests cleanly.
    """
    return db_dir() / filename


def is_sandbox_path(path: str | Path) -> bool:
    """True if ``path`` looks like a sandbox / test database location.

    Used by helper scripts that want to gate destructive operations on a
    DB file location (see *Database Safety* in CLAUDE.md). A path is
    considered sandboxed if it starts with ``/tmp/`` or its filename
    ends with ``.test.db`` / ``.sandbox.db``.
    """
    s = str(path)
    name = Path(s).name
    return s.startswith("/tmp/") or name.endswith((".test.db", ".sandbox.db"))


# ── Durability / crash-safety hardening ─────────────────────────────────
#
# Motivation: on 2026-07-26 ``db/notes.db`` became "database disk image is
# malformed" — the ``pdf_inline_comments`` B-tree had a contiguous run of
# *zero-filled* leaf pages that the interior page still pointed at. That is
# the signature of a torn / lost write: pages were allocated and the pointer
# flushed, but the leaf contents never reached disk before the process was
# killed (the 16 GB M4 Air OOM/jetsam-kills under memory pressure). WAL mode
# alone does not prevent this when ``synchronous`` is too low, because the
# main-db file can be left half-written during a checkpoint. ``harden()``
# closes that window; ``backup_db()`` gives a rotating fallback so a future
# torn write is recoverable instead of silently lost.


def harden(conn: sqlite3.Connection) -> sqlite3.Connection:
    """Apply crash-safety PRAGMAs to a freshly-opened connection.

    - ``journal_mode=WAL``   — concurrent readers while one process writes.
    - ``synchronous=FULL``   — fsync the WAL on every commit AND the main db
      on checkpoint, so a SIGKILL mid-checkpoint can't leave zeroed pages.
      These DBs are tiny + low-write, so the fsync cost is irrelevant.
    - ``busy_timeout=5000``  — wait out a concurrent writer instead of
      raising ``database is locked`` (multiple processes open notes.db).
    - ``wal_autocheckpoint=256`` — keep the WAL bounded (~1 MB at 4 KB pages).

    Idempotent and safe to call on every connect. Returns ``conn`` so it can
    be chained: ``conn = harden(sqlite3.connect(path))``.
    """
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=FULL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA wal_autocheckpoint=256")
    return conn


def backup_db(name: str, *, keep: int = 5) -> Path | None:
    """Make a consistent rotating backup of a DB using SQLite's online
    backup API (safe even while the DB is being written).

    Backups land next to the source as ``<name>.bak-YYYYmmdd-HHMMSS`` and the
    newest ``keep`` are retained. Skips sandbox DBs (``FINAGENT_DB_DIR`` /
    ``/tmp``) and missing files. Returns the backup path, or ``None`` if
    skipped. Callers should invoke this at startup (see ``init_db``) — it is
    cheap for these small DBs and gives a recoverable fallback for the
    torn-write failure mode documented above.
    """
    src = db_path(name)
    if is_sandbox_path(src) or not src.exists():
        return None
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = src.with_name(f"{src.name}.bak-{stamp}")
    try:
        s = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
        d = sqlite3.connect(dest)
        with d:
            s.backup(d)
        d.close()
        s.close()
    except sqlite3.Error:
        # A corrupt source can't be backed up — don't mask the real error.
        dest.unlink(missing_ok=True)
        return None
    # Rotate: keep only the newest ``keep`` backups.
    backups = sorted(src.parent.glob(f"{src.name}.bak-*"), reverse=True)
    for old in backups[keep:]:
        old.unlink(missing_ok=True)
    return dest
