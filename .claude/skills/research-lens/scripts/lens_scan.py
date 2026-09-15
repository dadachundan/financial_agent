#!/usr/bin/env python3
"""Step 1 of the research-lens skill: gather every artifact about one ticker.

Usage:
    python3 lens_scan.py GEV
    python3 lens_scan.py GEV --name "GE Vernova" --limit 80
    python3 lens_scan.py 603308.SS --summary-chars 1200

Output: JSON to stdout with four blocks —

  candidates    every zsxq PDF that plausibly mentions the ticker
                (BM25-ranked FTS5 trigram search over the 13.5k-row
                library), annotated with whether we already hold a
                price target for it and whether it is already digested.
  price_targets existing `db/stock_price_target.db.price_targets` rows
                for the ticker — the read-only pre-pass that lets the
                caller spot same-institute revisions and cross-broker
                dispersion before re-reading anything.
  digests       the subset of `reference/report_digests.json` whose
                file_id is among the candidates — so a re-run only has
                to read the PDFs still missing a digest.
  counts        the headline numbers for the triage.

This script only reads. It never writes the DBs; price targets go in
through `scripts/persist_pts.py` and digests through
`reference/report_digests.json` (see SKILL.md).

Interpreter: run with /opt/anaconda3/bin/python3 (bare `python3` on this
box is 3.9 and lacks yfinance — see CLAUDE.md / the
`feedback_anaconda_python_db_scripts` rule).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

# Walk up to the project root (the dir containing db_paths.py) and import it,
# so FINAGENT_DB_DIR redirection reaches this script (CLAUDE.md DB-safety rule).
_here = Path(__file__).resolve()
PROJECT_ROOT = None
for _anc in _here.parents:
    if (_anc / "db_paths.py").exists():
        PROJECT_ROOT = _anc
        sys.path.insert(0, str(_anc))
        break
if PROJECT_ROOT is None:
    sys.exit("could not locate the project root (no db_paths.py in any parent)")
from db_paths import db_path  # noqa: E402

import zsxq_fts  # noqa: E402  (project retrieval layer; read-only FTS5)

DIGEST_PATH = PROJECT_ROOT / "reference" / "report_digests.json"


# ── ticker → search terms ──────────────────────────────────────────────────────
# Mirrors zsxq_viewer._ticker_search_terms so the skill's candidate set matches
# what the /research-lens page itself would query.

def ticker_search_terms(ticker: str) -> list[str]:
    raw = (ticker or "").strip().upper()
    if not raw:
        return []
    compact = raw
    for prefix in ("SSE:", "SZSE:", "HKEX:", "NASDAQ:", "NYSE:",
                   "SSE", "SZSE", "HKEX"):
        compact = compact.replace(prefix, "")
    compact = compact.strip()
    core = compact.split(".")[0]
    terms = {raw, compact, core}
    if core.isdigit() and len(core) == 6:
        terms.update({f"{core}.SS", f"{core}.SH", f"{core}.SZ",
                      f"SSE{core}", f"SZSE{core}"})
    if core.isdigit() and len(core) == 4:
        terms.update({f"{core}.HK", f"HKEX{core}", core.zfill(4),
                      f"{core.zfill(4)}.HK"})
    return sorted(t for t in terms if t)


# ── readers ────────────────────────────────────────────────────────────────────

def read_price_targets(ticker: str, terms: list[str]) -> tuple[list[dict], str | None]:
    """Existing PT rows for the ticker, plus the company name they imply."""
    pt_db = db_path("stock_price_target.db")
    if not pt_db.exists():
        return [], None
    placeholders = ",".join("?" for _ in terms)
    like_terms = [f"%{t}%" for t in terms]
    conn = sqlite3.connect(f"file:{pt_db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            f"""
            SELECT company_ticker, company_name, research_institute, rating,
                   price_target, target_currency, catalyst, report_file_id,
                   report_pdf_filename, report_url, report_date,
                   report_date_price, price_currency, upside_pct
            FROM price_targets
            WHERE upper(company_ticker) IN ({placeholders})
               OR {" OR ".join("upper(company_ticker) LIKE ?" for _ in like_terms)}
            ORDER BY report_date DESC, report_file_id DESC
            """,
            (*terms, *like_terms),
        ).fetchall()
    finally:
        conn.close()
    out = [dict(r) for r in rows]
    name = next((r["company_name"] for r in out if r["company_name"]), None)
    return out, name


def fetch_pdfs_by_id(file_ids: list[int], summary_chars: int) -> list[dict]:
    """Hydrate specific pdf_files rows, bypassing the text search.

    Needed because a report we already hold a price target for is the
    strongest possible evidence of a real call, yet its text may rank
    below the BM25 cutoff (e.g. a note whose summary never spells the
    ticker out). Those rows get unioned into the candidate set.
    """
    if not file_ids:
        return []
    zdb = db_path("zsxq.db")
    placeholders = ",".join("?" for _ in file_ids)
    conn = sqlite3.connect(f"file:{zdb}?immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            f"""
            SELECT file_id, name, topic_title, summary, bank, create_time,
                   page_count, tickers, local_path
            FROM pdf_files WHERE file_id IN ({placeholders})
            """,
            file_ids,
        ).fetchall()
    finally:
        conn.close()
    out = []
    for r in rows:
        summary = r["summary"] or ""
        if summary_chars and len(summary) > summary_chars:
            summary = summary[:summary_chars].rstrip() + "…"
        out.append({
            "file_id": r["file_id"], "name": r["name"],
            "topic_title": r["topic_title"], "summary": summary,
            "bank": r["bank"], "create_time": r["create_time"],
            "page_count": r["page_count"], "tickers": r["tickers"],
            "local_path": r["local_path"], "score": None,
            "has_card": False, "card_primary_ticker": None,
            "card_theme": None,
            "pdf_url": zsxq_fts._pdf_url(r["file_id"], r["name"]),
        })
    return out


def read_digests() -> dict:
    try:
        payload = json.loads(DIGEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Gather zsxq PDFs + PT rows + digests for one ticker.")
    ap.add_argument("ticker", help="ticker in yfinance form, e.g. GEV, 603308.SS")
    ap.add_argument("--name", action="append", default=[],
                    help="extra company-name search term (repeatable), e.g. "
                         "--name 'GE Vernova'. Auto-filled from the existing "
                         "PT rows when omitted.")
    ap.add_argument("--limit", type=int, default=80,
                    help="max candidate PDFs to return (default 80)")
    ap.add_argument("--summary-chars", type=int, default=900,
                    help="truncate each candidate summary to N chars "
                         "(0 = no cap, default 900)")
    args = ap.parse_args()

    ticker = args.ticker.strip().upper()
    terms = ticker_search_terms(ticker)
    pt_rows, pt_name = read_price_targets(ticker, terms)

    # Name terms: explicit flags win, else the name the PT rows already carry.
    names = [n for n in args.name if n.strip()]
    if not names and pt_name:
        names = [pt_name]

    query = " ".join([ticker, *names]) if names else ticker
    candidates = zsxq_fts.search(query, limit=args.limit,
                                 summary_chars=args.summary_chars)

    # Union in every PDF we already hold a price target for: a PT row is the
    # strongest evidence of a real call, but its report may rank below the
    # BM25 cutoff and would otherwise silently drop out of the candidate set.
    pt_file_ids = {r["report_file_id"] for r in pt_rows if r["report_file_id"]}
    known_ids = {c["file_id"] for c in candidates}
    extra_ids = sorted(pt_file_ids - known_ids)
    if extra_ids:
        candidates.extend(fetch_pdfs_by_id(extra_ids, args.summary_chars))

    digests = read_digests()

    for c in candidates:
        fid = c["file_id"]
        digest = digests.get(str(fid))
        c["has_pt_row"] = fid in pt_file_ids
        c["has_digest"] = digest is not None
        c["digest_score"] = digest.get("score") if digest else None
        c["has_pdf"] = bool(c.get("local_path")) and Path(c["local_path"]).exists()

    digested = sum(1 for c in candidates if c["has_digest"])
    called = sum(1 for c in candidates if c["has_pt_row"])
    out = {
        "ticker": ticker,
        "company_name": pt_name or (names[0] if names else ticker),
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "search_terms": {"ticker": terms, "name": names, "query": query},
        "counts": {
            "candidates": len(candidates),
            "with_pt_row": called,
            "already_digested": digested,
            "missing_digest": len(candidates) - digested,
            "pt_rows": len(pt_rows),
            "digests_in_registry": len([k for k in digests if k != "_comment"]),
        },
        "price_targets": pt_rows,
        "candidates": candidates,
        "digests": {str(c["file_id"]): digests[str(c["file_id"])]
                    for c in candidates if c["has_digest"]},
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
