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
