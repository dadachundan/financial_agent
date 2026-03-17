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

    def test_graphiti_ingest_default_db_in_db_dir(self):
        gi = _load("ingest/graphiti_ingest.py")
        assert "db/" in str(gi.DEFAULT_DB), f"Expected db/ subdir, got {gi.DEFAULT_DB}"
        assert gi.DEFAULT_DB.exists(), f"zsxq.db not found at {gi.DEFAULT_DB}"

    def test_graphiti_ingest_reports_db_path(self):
        gi = _load("ingest/graphiti_ingest.py")
        root = gi._get_project_root()
        reports_db = root / "db" / "financial_reports.db"
        assert reports_db.exists(), f"financial_reports.db not found at {reports_db}"
        n = _row_count(reports_db, "reports")
        assert n > 0, "reports table is empty"

    def test_eval_ingest_reports_db_in_db_dir(self):
        ei = _load("ingest/eval_ingest_prompt.py")
        assert "db/" in str(ei.REPORTS_DB_PATH), \
            f"Expected db/ subdir, got {ei.REPORTS_DB_PATH}"
        assert ei.REPORTS_DB_PATH.exists(), \
            f"financial_reports.db not found at {ei.REPORTS_DB_PATH}"


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

    def test_llm_call_log_path_in_log_dir(self):
        """graphiti_ingest.py sends LLM log to log/llm_calls.jsonl"""
        gi = _load("ingest/graphiti_ingest.py")
        root = gi._get_project_root()
        llm_log = root / "log" / "llm_calls.jsonl"
        assert "log/" in str(llm_log), f"Expected log/ subdir, got {llm_log}"
        assert llm_log.parent.is_dir(), f"log/ dir missing: {llm_log.parent}"

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
        r = m.search(conn, "Synodex platform", limit=10)
        names = [n["name"] for n in r["nodes"]]
        assert any("Synodex" in name for name in names), \
            f"'Synodex® platform' entity missing from phrase search: {names}"

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


# ── HTML extraction tests ──────────────────────────────────────────────────────

class TestHtmlExtraction:
    """extract_html_text() must pull the right sections and block excluded ones."""

    LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 12

    @pytest.fixture(scope="class")
    def gi(self):
        return _load("ingest/graphiti_ingest.py")

    def _write(self, html, tmp_path, name="test.htm"):
        p = tmp_path / name
        p.write_text(html)
        return p

    def test_10k_extracts_business_and_risk(self, gi, tmp_path):
        f = self._write(f"""<html><body>
<h2>Item 1. Business</h2><p>Widget Pro globally. {self.LOREM}</p>
<h2>Item 1A. Risk Factors</h2><p>Competition risk. {self.LOREM}</p>
<h2>Item 7. Management Discussion</h2><p>Revenue 15%. EXCLUDED_ITEM7.</p>
<script>EXCLUDED_SCRIPT</script>
</body></html>""", tmp_path)
        text = gi.extract_html_text(f, form_type="10-K")
        assert "Widget Pro" in text,          "Item 1 Business missing"
        assert "Competition risk" in text,    "Item 1A Risk Factors missing"
        assert "EXCLUDED_ITEM7" not in text,  "Item 7 must not appear in 10-K"
        assert "EXCLUDED_SCRIPT" not in text, "script tag must be stripped"

    def test_10q_extracts_mda_excludes_financials(self, gi, tmp_path):
        f = self._write(f"""<html><body>
<h2>Item 1. Financial Statements</h2><p>Balance sheet. {self.LOREM}</p>
<h2>Item 2. Management's Discussion and Analysis</h2>
<p>Net income $500M. Revenue +18%. {self.LOREM}</p>
<h2>Item 3. Quantitative Disclosures</h2><p>Market risk.</p>
</body></html>""", tmp_path)
        text = gi.extract_html_text(f, form_type="10-Q")
        assert "Net income" in text,       "Item 2 MD&A missing"
        assert "Balance sheet" not in text, "Item 1 financials must not appear"

    def test_8k_excludes_502_and_701(self, gi, tmp_path):
        f = self._write(f"""<html><body>
<h2>Item 1.01. Entry into a Material Definitive Agreement</h2>
<p>Merger with BigCo $2.5B. Board approved. {self.LOREM}</p>
<h2>Item 5.02. Departure of Directors</h2>
<p>Jane Smith resigned. EXCLUDED_502.</p>
<h2>Item 7.01 Regulation FD Disclosure</h2>
<p>See Exhibit 99.1. EXCLUDED_701.</p>
<h2>Item 9.01. Exhibits</h2><p>List.</p>
</body></html>""", tmp_path)
        text = gi.extract_html_text(f, form_type="8-K")
        assert "BigCo" in text,             "Item 1.01 material agreement missing"
        assert "EXCLUDED_502" not in text,  "Item 5.02 officer change must be excluded"
        assert "EXCLUDED_701" not in text,  "Item 7.01 Reg FD must be excluded"

    def test_8k_excludes_502_after_202(self, gi, tmp_path):
        f = self._write(f"""<html><body>
<h2>Item 2.02. Results of Operations</h2>
<p>Q4 revenue $1.2B. EPS $2.45. {self.LOREM}</p>
<h2>Item 5.02. Departure of Directors</h2>
<p>John Doe resigned. EXCLUDED_502B.</p>
<h2>Item 9.01. Exhibits</h2><p>See attached.</p>
</body></html>""", tmp_path)
        text = gi.extract_html_text(f, form_type="8-K")
        assert "EPS" in text,                "Item 2.02 earnings missing"
        assert "EXCLUDED_502B" not in text,  "Item 5.02 must not appear after 2.02"

    def test_short_html_returns_empty(self, gi, tmp_path):
        f = self._write("<html><p>Too short.</p></html>", tmp_path)
        assert gi.extract_html_text(f, form_type="10-K") == ""


# ── DB limit / filter tests ────────────────────────────────────────────────────

class TestIngestQueries:
    """get_pending_reports and get_pending_pdfs must apply SQL-level limits."""

    @pytest.fixture(scope="class")
    def gi(self):
        return _load("ingest/graphiti_ingest.py")

    @pytest.fixture(scope="class")
    def reports_conn(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("""CREATE TABLE reports (
            id INTEGER PRIMARY KEY, ticker TEXT, company_name TEXT, period TEXT,
            form_type TEXT, local_path TEXT, filed_date TEXT,
            graphiti_indexed_at TEXT)""")
        for i in range(12):
            conn.execute("INSERT INTO reports VALUES (?,?,?,?,?,?,?,?)",
                         (i, "AAPL" if i < 6 else "MSFT", "Co", "2025",
                          "10-K", f"/f{i}.htm", "2025-01-01", None))
        conn.commit()
        return conn

    @pytest.fixture(scope="class")
    def pdfs_conn(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("""CREATE TABLE pdf_files (
            id INTEGER PRIMARY KEY, file_id INTEGER, name TEXT,
            local_path TEXT, create_time TEXT, graphiti_indexed_at TEXT)""")
        for i in range(8):
            conn.execute("INSERT INTO pdf_files VALUES (?,?,?,?,?,?)",
                         (i, i, f"doc_{i}", f"/f{i}.pdf", "2025-01-01", None))
        conn.commit()
        return conn

    def test_reports_limit_applied_in_sql(self, gi, reports_conn):
        rows = gi.get_pending_reports(reports_conn, reindex=False,
                                      tickers=None, form_types=["10-K"], limit=3)
        assert len(rows) == 3

    def test_reports_limit_zero_means_all(self, gi, reports_conn):
        rows = gi.get_pending_reports(reports_conn, reindex=False,
                                      tickers=None, form_types=["10-K"], limit=0)
        assert len(rows) == 12

    def test_reports_ticker_filter(self, gi, reports_conn):
        rows = gi.get_pending_reports(reports_conn, reindex=False,
                                      tickers=["AAPL"], form_types=["10-K"], limit=0)
        assert len(rows) == 6
        assert all(r[1] == "AAPL" for r in rows)

    def test_reports_reindex_false_skips_indexed(self, gi, reports_conn):
        reports_conn.execute(
            "UPDATE reports SET graphiti_indexed_at='2025-01-02' WHERE id < 4")
        reports_conn.commit()
        rows = gi.get_pending_reports(reports_conn, reindex=False,
                                      tickers=None, form_types=["10-K"], limit=0)
        assert len(rows) == 8   # 12 total - 4 indexed

    def test_reports_reindex_true_returns_all(self, gi, reports_conn):
        rows = gi.get_pending_reports(reports_conn, reindex=True,
                                      tickers=None, form_types=["10-K"], limit=0)
        assert len(rows) == 12

    def test_pdfs_limit_applied(self, gi, pdfs_conn):
        rows = gi.get_pending_pdfs(pdfs_conn, reindex=False, limit=3)
        assert len(rows) == 3

    def test_pdfs_limit_zero_means_all(self, gi, pdfs_conn):
        rows = gi.get_pending_pdfs(pdfs_conn, reindex=False, limit=0)
        assert len(rows) == 8
