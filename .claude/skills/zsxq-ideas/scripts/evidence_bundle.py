#!/usr/bin/env python3
"""Build an *extraction manifest* for a cluster of zsxq file_ids — the
planning artifact for the **Theme-build** mode of the `zsxq-ideas` skill.

IMPORTANT — what counts as a source:
  The PRIMARY source for any downstream report is the **original PDF text**,
  obtained via `zsxq-analyze/scripts/extract_pdf.py` (which auto-merges the
  `ocr_text` cache for image-only pages). Many bank PDFs in this library are
  image-only (fitz returns nothing) and must be OCR'd first with
  `ocr_pdf.py`. The `summary` column (zsxq's 翻译精华 highlight blurb) is a
  curated, often re-translated SECONDARY source — it can paraphrase or drop
  numbers, so it is a LAST-RESORT fallback only (use it when extract + OCR +
  visual-render all fail, e.g. a pure-chart page), and label it as such.

This script does NOT dump original text (75 reports of full text is too
large for one bundle). It emits, per file_id: metadata + the extraction
STATUS (text-ready / OCR-cached / needs-OCR) + the exact extract command to
run, so a theme-build agent reads each report's *original* text on demand.
The summary is included only as clearly-labelled fallback context.

Usage:
    python3 evidence_bundle.py --file-ids 184152244582842,212485811815581 \
        --slug ai-power-electrification --out /tmp/zsxq_evidence/ai-power.md

DB is opened read-only (mode=ro) — this script never writes (see CLAUDE.md
§ Database Safety). NOTE: making text available may require running
`ocr_pdf.py` separately, which DOES populate the sanctioned `ocr_text`
cache; this script only reports whether that step is still needed.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH = PROJECT_ROOT / "db" / "zsxq.db"
EXTRACT = ".claude/skills/zsxq-analyze/scripts/extract_pdf.py"
OCR = ".claude/skills/zsxq-analyze/scripts/ocr_pdf.py"


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(f"file:{DB_PATH}?immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _status(row: sqlite3.Row) -> str:
    """text-ready | ocr-cached | needs-ocr | no-local-file"""
    if (row["oc"] or 0) > 200:
        return "ocr-cached"
    p = row["local_path"]
    if not p or not os.path.exists(p):
        return "no-local-file"
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(p)
        n = min(5, doc.page_count)
        chars = sum(len(doc[i].get_text().strip()) for i in range(n))
        doc.close()
        return "text-ready" if chars > 300 else "needs-ocr"
    except Exception:
        return "needs-ocr"


def build(file_ids: list[int], slug: str | None) -> str:
    conn = _connect()
    blocks, need_ocr = [], []
    for fid in file_ids:
        row = conn.execute(
            "SELECT file_id, bank, topic_title, name, page_count, tickers, "
            "local_path, LENGTH(COALESCE(ocr_text,'')) oc, summary "
            "FROM pdf_files WHERE file_id = ?",
            (fid,),
        ).fetchone()
        if row is None:
            blocks.append(f"## file_id {fid}\n(NOT FOUND IN db/zsxq.db)\n")
            continue
        st = _status(row)
        if st == "needs-ocr":
            need_ocr.append(str(fid))
        summary = (row["summary"] or "").strip()
        fallback = (
            f"\nFALLBACK ONLY (zsxq 翻译精华 — curated/translated, NOT original "
            f"text; use only if extract+OCR+render all fail, and label it):\n{summary}\n"
            if summary
            else ""
        )
        blocks.append(
            f"## file_id {row['file_id']} | bank={row['bank']} | "
            f"pages={row['page_count']} | tickers={row['tickers']} | status={st.upper()}\n"
            f"TITLE: {row['topic_title'] or row['name']}\n"
            f"PRIMARY SOURCE — extract the original text:\n"
            f"  python3 {EXTRACT} --file-id {row['file_id']} --header"
            + (
                f"\n  (image-only — first: python3 {OCR} --file-id {row['file_id']})"
                if st == "needs-ocr"
                else ""
            )
            + fallback
        )
    conn.close()

    header = f"# zsxq extraction manifest: {slug or 'cluster'}\n\n"
    header += (
        f"{len(file_ids)} reports. **Primary source = original PDF text via "
        f"extract_pdf.py** (OCR image-only ones first). The 翻译精华 summary is "
        f"fallback-only. Cite each broker number inline to its file_id via "
        f"`http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>` "
        f"(put the page as `p.N` in the link text — `extract_pdf.py` marks pages "
        f"as `===== Page N =====`), and string-match every "
        f"number against the EXTRACTED text — never the title or the summary.\n"
    )
    if need_ocr:
        header += (
            f"\n**{len(need_ocr)} reports need OCR first** (image-only): "
            f"{','.join(need_ocr)}\n"
            f"Batch: `for f in {' '.join(need_ocr)}; do python3 {OCR} --file-id $f; done`\n"
        )
    return header + "\n---\n".join(blocks)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file-ids", required=True, help="Comma-separated zsxq file_ids.")
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
        print(f"{len(file_ids)} reports -> {dest} ({len(out)} chars)")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
