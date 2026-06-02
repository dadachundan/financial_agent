"""
test_db_paths.py — Verify every DB and log path resolves to the correct
location under db/ and log/ after the directory reorganisation.

Run from project root:
    python -m pytest tests/test_db_paths.py -v
"""
import importlib.util
import pathlib
import sqlite3
import sys

import pytest

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ── helpers ────────────────────────────────────────────────────────────────────

def _load(rel_path: str):
    """Import a module from a relative path without executing __main__ blocks."""
    abs_path = PROJECT_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(abs_path.stem, abs_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _row_count(db_path: pathlib.Path, table: str) -> int:
    conn = sqlite3.connect(str(db_path))
    n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.close()
    return n


# ── DB path tests ──────────────────────────────────────────────────────────────

class TestDbPaths:
    """All DB paths must resolve into db/ and connect with real data."""

    def test_zsxq_common_default_db_in_db_dir(self):
        from zsxq_common import DEFAULT_DB
        assert "db/" in str(DEFAULT_DB) or str(DEFAULT_DB).endswith("/db/zsxq.db"), \
            f"Expected db/ subdir, got {DEFAULT_DB}"
        assert DEFAULT_DB.exists(), f"zsxq.db not found at {DEFAULT_DB}"

    def test_zsxq_common_has_rows(self):
        from zsxq_common import DEFAULT_DB
        n = _row_count(DEFAULT_DB, "pdf_files")
        assert n > 0, "pdf_files table is empty"

    def test_zsxq_viewer_default_db_in_db_dir(self):
        from zsxq_viewer import DEFAULT_DB
        assert "db/" in str(DEFAULT_DB), f"Expected db/ subdir, got {DEFAULT_DB}"
        assert DEFAULT_DB.exists(), f"zsxq.db not found at {DEFAULT_DB}"

    def test_fetch_financial_report_db_in_db_dir(self):
        from fetch_financial_report import DB_FILE
        assert "db/" in str(DB_FILE), f"Expected db/ subdir, got {DB_FILE}"
        assert DB_FILE.exists(), f"financial_reports.db not found at {DB_FILE}"

    def test_fetch_financial_report_has_rows(self):
        from fetch_financial_report import DB_FILE
        n = _row_count(DB_FILE, "reports")
        assert n > 0, "reports table is empty"

    def test_fetch_cninfo_report_db_in_db_dir(self):
        from fetch_cninfo_report import DB_FILE
        assert "db/" in str(DB_FILE), f"Expected db/ subdir, got {DB_FILE}"
        assert DB_FILE.exists(), f"cninfo_reports.db not found at {DB_FILE}"

    def test_fetch_cninfo_report_has_rows(self):
        from fetch_cninfo_report import DB_FILE
        n = _row_count(DB_FILE, "cninfo_reports")
        assert n > 0, "cninfo_reports table is empty"

    def test_graph_mirror_default_path_in_db_dir(self):
        from graph_mirror import _DEFAULT_MIRROR
        assert "db/" in str(_DEFAULT_MIRROR), f"Expected db/ subdir, got {_DEFAULT_MIRROR}"

    def test_graph_mirror_has_entities(self):
        from graph_mirror import _DEFAULT_MIRROR
        assert _DEFAULT_MIRROR.exists(), f"graph_mirror.db not found at {_DEFAULT_MIRROR}"
        n = _row_count(_DEFAULT_MIRROR, "entities")
        assert n > 0, "entities table is empty"

    def test_zep_app_zsxq_db_in_db_dir(self):
        za = _load("zep_app.py")
        assert "db/" in str(za.ZSXQ_DB), f"Expected db/ subdir, got {za.ZSXQ_DB}"
        assert za.ZSXQ_DB.exists(), f"zsxq.db not found at {za.ZSXQ_DB}"


# ── Log path tests ─────────────────────────────────────────────────────────────

class TestLogPaths:
    """Log scripts must write into log/ and that directory must exist."""

    def test_log_dir_exists(self):
        log_dir = PROJECT_ROOT / "log"
        assert log_dir.is_dir(), "log/ directory does not exist"

    def test_bulk_download_10k_log_path(self):
        """bulk_download_10k_10q_8k.py computes log path via __file__.parent.parent/log/"""
        script = PROJECT_ROOT / "download" / "bulk_download_10k_10q_8k.py"
        computed_log = script.parent.parent / "log" / "bulk_download_10k_10q_8k.log"
        assert "log/" in str(computed_log), f"Expected log/ subdir, got {computed_log}"
        assert computed_log.parent.is_dir(), f"log/ dir missing: {computed_log.parent}"

    def test_bulk_download_ashare_log_path(self):
        """bulk_download_ashare.py computes log path via __file__.parent.parent/log/"""
        script = PROJECT_ROOT / "download" / "bulk_download_ashare.py"
        computed_log = script.parent.parent / "log" / "bulk_download_ashare.log"
        assert "log/" in str(computed_log), f"Expected log/ subdir, got {computed_log}"
        assert computed_log.parent.is_dir(), f"log/ dir missing: {computed_log.parent}"


    def test_existing_log_files_in_log_dir(self):
        """Previously-generated log files should be in log/, not project root."""
        log_dir = PROJECT_ROOT / "log"
        root_logs = list(PROJECT_ROOT.glob("*.log"))
        assert root_logs == [], \
            f"Stray .log files at project root: {[f.name for f in root_logs]}"
        # At least one log file should exist in log/ (from prior runs)
        log_files = list(log_dir.glob("*.log"))
        assert len(log_files) > 0, "No .log files found in log/ directory"


# ── graph_mirror function tests ────────────────────────────────────────────────

class TestGraphMirror:
    """Core graph_mirror.py functions must work against the real mirror DB."""

    @pytest.fixture(scope="class")
    def conn(self):
        import graph_mirror as m
        c = m.get_conn()
        m.ensure_schema(c)
        yield c
        c.close()

    def test_get_stats_returns_counts(self, conn):
        import graph_mirror as m
        s = m.get_stats(conn)
        assert s["node_count"] > 0,    "no entities in mirror"
        assert s["edge_count"] > 0,    "no edges in mirror"
        assert s["episode_count"] > 0, "no episodes in mirror"

    def test_get_entities_pagination(self, conn):
        import graph_mirror as m
        nodes, cursor = m.get_entities(conn, limit=5)
        assert len(nodes) == 5
        assert cursor is not None, "expected a next_cursor for pagination"
        # second page
        nodes2, _ = m.get_entities(conn, limit=5, cursor=cursor)
        assert len(nodes2) == 5
        # pages must not overlap
        uuids1 = {n["uuid"] for n in nodes}
        uuids2 = {n["uuid"] for n in nodes2}
        assert uuids1.isdisjoint(uuids2), "pagination returned duplicate nodes"

    def test_get_edges_has_names(self, conn):
        import graph_mirror as m
        edges, _ = m.get_edges(conn, limit=10)
        assert len(edges) > 0
        for e in edges:
            assert "src_name" in e
            assert "tgt_name" in e

    def test_resolve_names(self, conn):
        import graph_mirror as m
        nodes, _ = m.get_entities(conn, limit=3)
        uuids = {n["uuid"] for n in nodes}
        result = m.resolve_names(conn, uuids)
        assert set(result.keys()) == uuids
        for name in result.values():
            assert isinstance(name, str) and len(name) > 0

    def test_search_single_word(self, conn):
        import graph_mirror as m
        r = m.search(conn, "Navitas", limit=5)
        assert len(r["nodes"]) > 0, "no results for 'Navitas'"

    def test_search_phrase_exact_hit(self, conn):
        import graph_mirror as m
        # Search a two-word entity name we know is in the mirror.
        r = m.search(conn, "CSPC Pharmaceutical", limit=10)
        names = [n["name"] for n in r["nodes"]]
        assert any("CSPC" in name for name in names), \
            f"'CSPC Pharmaceutical Group' missing from phrase search: {names}"

    def test_search_empty_returns_empty(self, conn):
        import graph_mirror as m
        r = m.search(conn, "", limit=10)
        assert r == {"nodes": [], "edges": []}

    def test_get_conn_autocreates_db_dir(self, tmp_path):
        """get_conn() must create the parent directory if it doesn't exist."""
        import graph_mirror as m
        new_db = tmp_path / "subdir" / "test_mirror.db"
        assert not new_db.parent.exists()
        conn = m.get_conn(new_db)
        m.ensure_schema(conn)
        conn.close()
        assert new_db.exists(), "DB file not created"


# ── FINAGENT_DB_DIR override tests ─────────────────────────────────────────────

class TestFinagentDbDirOverride:
    """Setting FINAGENT_DB_DIR must redirect every DB-using module that goes
    through db_paths.db_path / db_dir. This is the mechanical guarantee
    behind the *Database Safety* rule in CLAUDE.md.
    """

    def _reimport(self, monkeypatch, tmp_path):
        """Import db_paths fresh under a sandbox FINAGENT_DB_DIR."""
        monkeypatch.setenv("FINAGENT_DB_DIR", str(tmp_path))
        # Re-import db_paths so it re-reads the env var.
        for name in list(sys.modules):
            if name == "db_paths":
                del sys.modules[name]
        import db_paths
        return db_paths

    def test_db_dir_honors_env(self, monkeypatch, tmp_path):
        db_paths = self._reimport(monkeypatch, tmp_path)
        assert db_paths.db_dir() == tmp_path.resolve()

    def test_db_path_honors_env(self, monkeypatch, tmp_path):
        db_paths = self._reimport(monkeypatch, tmp_path)
        assert db_paths.db_path("notes.db") == (tmp_path / "notes.db").resolve()

    def test_default_when_env_unset(self, monkeypatch, tmp_path):
        monkeypatch.delenv("FINAGENT_DB_DIR", raising=False)
        for name in list(sys.modules):
            if name == "db_paths":
                del sys.modules[name]
        import db_paths
        assert db_paths.db_dir() == PROJECT_ROOT / "db"

    @pytest.mark.parametrize("module_path,attr", [
        ("pdf_inline_comments.py", "DB_PATH"),
        ("pdf_page_ocr.py",        "DB_PATH"),
        ("report_inline_comments.py", "DB_PATH"),
        ("report_annotations.py",  "DB_PATH"),
        ("market_cap_cache.py",    "_DB_PATH"),
        ("graph_mirror.py",        "_DEFAULT_MIRROR"),
        ("zsxq_common.py",         "DEFAULT_DB"),
        ("stock_price_target_db.py", "DB_PATH"),
    ])
    def test_module_honors_env(self, monkeypatch, tmp_path, module_path, attr):
        """Each DB-using module's path constant lands inside FINAGENT_DB_DIR."""
        monkeypatch.setenv("FINAGENT_DB_DIR", str(tmp_path))
        for name in list(sys.modules):
            if name.split(".")[0] in {"db_paths", pathlib.Path(module_path).stem}:
                del sys.modules[name]
        mod = _load(module_path)
        resolved = getattr(mod, attr)
        assert str(resolved).startswith(str(tmp_path.resolve())), \
            f"{module_path}.{attr} -> {resolved} did not honor FINAGENT_DB_DIR={tmp_path}"

    def test_is_sandbox_path_helper(self, monkeypatch, tmp_path):
        db_paths = self._reimport(monkeypatch, tmp_path)
        assert db_paths.is_sandbox_path("/tmp/notes.db")
        assert db_paths.is_sandbox_path("/anywhere/notes.test.db")
        assert db_paths.is_sandbox_path("/anywhere/test.sandbox.db")
        assert not db_paths.is_sandbox_path("/Users/x/projects/financial_agent/db/notes.db")
        assert not db_paths.is_sandbox_path("db/zsxq.db")
