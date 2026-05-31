#!/usr/bin/env python3
"""Dump the 翻译精华 (summary column) for a set of zsxq file_ids into one
markdown evidence bundle — the per-cluster source pack used by the
**Theme-build** mode of the `zsxq-ideas` skill.

The point of this script: when you build (or enrich) a downstream report
from a cluster of zsxq reports, you must cite the *specific broker content*
(target prices, deal structures, forecasts) — not just the report title.
This bundle is the guaranteed source floor: the curated 翻译精华 summary that
zsxq pastes onto each row already carries the headline numbers. For deeper
extraction, run `zsxq-analyze/scripts/extract_pdf.py --file-id <id>` on the
flagships afterwards.

Usage:
    # Dump a cluster's summaries to stdout
    python3 evidence_bundle.py --file-ids 184152244582842,212485811815581

    # Write to a file (one per theme is the usual pattern)
    python3 evidence_bundle.py \
        --file-ids 184152244582842,212485811815581,184152218155882 \
        --out /tmp/zsxq_evidence/ai-power-electrification.md \
        --slug ai-power-electrification

Output: markdown, one block per file_id (file_id | bank | pages | tickers,
the topic title, and the full summary). Empty summaries are flagged with a
hint to run extract_pdf.py. DB is opened read-only (mode=ro) — this script
never writes to db/zsxq.db (see CLAUDE.md § Database Safety).
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH = PROJECT_ROOT / "db" / "zsxq.db"


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def build(file_ids: list[int], slug: str | None) -> str:
    conn = _connect()
    blocks: list[str] = []
    got = 0
    for fid in file_ids:
        row = conn.execute(
            "SELECT file_id, bank, topic_title, name, page_count, tickers, summary "
            "FROM pdf_files WHERE file_id = ?",
            (fid,),
        ).fetchone()
        if row is None:
            blocks.append(f"## file_id {fid}\n(NOT FOUND IN db/zsxq.db)\n")
            continue
        summary = (row["summary"] or "").strip()
        if summary:
            got += 1
            body = summary
        else:
            body = (
                "(empty summary — run "
                f"`extract_pdf.py --file-id {fid} --header` for full text; "
                "OCR with `ocr_pdf.py` first if pages are image-only)"
            )
        blocks.append(
            f"## file_id {row['file_id']} | bank={row['bank']} | "
            f"pages={row['page_count']} | tickers={row['tickers']}\n"
            f"TITLE: {row['topic_title'] or row['name']}\n"
            f"SUMMARY (翻译精华):\n{body}\n"
        )
    conn.close()

    header = f"# zsxq evidence bundle: {slug or 'cluster'}\n\n"
    header += (
        f"{len(file_ids)} reports, {got} with non-empty summaries. "
        "Cite each broker number inline to its file_id via "
        "`http://localhost:5001/zsxq-pdf/<file_id>` — never cite the title alone.\n\n"
    )
    return header + "\n---\n".join(blocks)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--file-ids",
        required=True,
        help="Comma-separated zsxq file_ids (the cluster from zsxq-recommend).",
    )
    ap.add_argument("--out", help="Write to this path instead of stdout.")
    ap.add_argument("--slug", help="Theme slug for the bundle header.")
    args = ap.parse_args()

    try:
        file_ids = [int(x) for x in args.file_ids.split(",") if x.strip()]
    except ValueError:
        sys.exit("--file-ids must be a comma-separated list of integer file_ids")
    if not file_ids:
        sys.exit("no file_ids parsed from --file-ids")

    out = build(file_ids, args.slug)

    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        non_empty = out.count("SUMMARY (翻译精华):\n") - out.count(
            "(empty summary"
        )
        print(f"{len(file_ids)} reports -> {dest} ({len(out)} chars)")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
