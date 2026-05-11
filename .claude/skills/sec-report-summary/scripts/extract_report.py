#!/usr/bin/env python3
"""Extract the narrative text from a single SEC filing for in-context summarization.

Usage:
    python3 extract_report.py --id 682
    python3 extract_report.py --path /abs/path/to/10-K.htm --form 10-K

For 10-K it returns Item 1 (Business) + Item 1A (Risk Factors).
For 10-Q it returns Item 2 (MD&A) + Item 1A Part II.
For 8-K it returns substantive items (1.01, 2.02, 5.02, …).
Falls back to a raw text dump if no sections are detected.

Reuses the production extractors in `ingest.graphiti_ingest` so the output
matches what the knowledge-graph pipeline indexes.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "financial_reports.db"

# Reuse the project's extractors
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ingest"))
from ingest.graphiti_ingest import (  # type: ignore  # noqa: E402
    extract_html_text,
    extract_text,
)


def _lookup_by_id(report_id: int) -> tuple[Path, str, dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT id, ticker, company_name, form_type, filed_date, "
        "period_of_report, period, local_path, accession_no "
        "FROM reports WHERE id = ?",
        (report_id,),
    ).fetchone()
    conn.close()
    if not row:
        sys.exit(f"No report with id={report_id}")
    if not row["local_path"]:
        sys.exit(f"Report {report_id} has no local_path")
    path = Path(row["local_path"])
    if not path.exists():
        sys.exit(f"File not found: {path}")
    return path, row["form_type"] or "", dict(row)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, help="report id from the reports table")
    ap.add_argument("--path", help="explicit file path (use with --form)")
    ap.add_argument("--form", default="10-K",
                    help="form type when using --path (default 10-K)")
    ap.add_argument("--max-chars", type=int, default=60_000,
                    help="truncate output to this many chars (default 60k)")
    ap.add_argument("--header", action="store_true",
                    help="prepend a short metadata header (ticker / form / dates)")
    args = ap.parse_args()

    if args.id is not None:
        path, form, meta = _lookup_by_id(args.id)
    elif args.path:
        path, form, meta = Path(args.path), args.form, {}
    else:
        sys.exit("provide --id or --path")

    suffix = path.suffix.lower()
    if suffix in (".htm", ".html", ".txt"):
        text = extract_html_text(path, form_type=form, max_chars=args.max_chars)
    elif suffix == ".pdf":
        text = extract_text(path, max_chars=args.max_chars)
    else:
        text = path.read_text(encoding="utf-8", errors="replace")

    text = (text or "").strip()
    if len(text) > args.max_chars:
        text = text[: args.max_chars] + "\n\n[…truncated…]"

    if args.header and meta:
        head = (
            f"# {meta.get('ticker')} — {meta.get('form_type')}  "
            f"(filed {meta.get('filed_date')}, period {meta.get('period_of_report')})\n"
            f"id={meta.get('id')}  accession={meta.get('accession_no')}\n"
            f"path={meta.get('local_path')}\n"
            f"---\n"
        )
        sys.stdout.write(head)

    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
