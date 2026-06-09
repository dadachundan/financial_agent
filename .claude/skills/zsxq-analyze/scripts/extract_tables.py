#!/usr/bin/env python3
"""
extract_tables.py — Pull *structured* tables out of a zsxq PDF as markdown.

The text extractors (extract_pdf.py / ocr_pdf.py) flatten tables into a stream
of reading-order words, destroying row/column structure — useless for the
head-to-head comparison tables broker reports are full of. This script uses
PyMuPDF's built-in table finder (``page.find_tables()``, no new dependency) to
recover the grid and emit GitHub-flavoured markdown tables, one per detected
table, each labelled with its page number.

It only works on PDFs that carry a real text layer (most English sell-side
notes). For image-only / scanned pages ``find_tables`` finds nothing — the
script says so and points you to ``render_pdf_pages.py`` so you can render the
page to PNG and read the table visually (Claude is multimodal).

Usage:
    python3 extract_tables.py --file-id 585525425551554
    python3 extract_tables.py --file-id 585525425551554 --pages 3-6
    python3 extract_tables.py --path /path/to.pdf --pages 7 --json
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sqlite3
import sys
from pathlib import Path

# Walk up to the project root (the dir containing db_paths.py) and import it.
_here = Path(__file__).resolve()
for _anc in _here.parents:
    if (_anc / "db_paths.py").exists():
        sys.path.insert(0, str(_anc))
        break
from db_paths import db_path  # noqa: E402

import fitz  # PyMuPDF  # noqa: E402

DB_PATH = db_path("zsxq.db")


def _resolve_path(file_id: int | None, path: str | None) -> tuple[Path, str]:
    if path:
        p = Path(path)
        return p, p.name
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    row = conn.execute(
        "SELECT local_path, name FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    conn.close()
    if not row or not row[0]:
        raise SystemExit(f"No local_path for file_id {file_id}")
    return Path(row[0]), row[1]


def _parse_pages(spec: str | None, page_count: int) -> list[int]:
    """Parse '1,3-5' into 0-indexed page numbers; default = all pages."""
    if not spec:
        return list(range(page_count))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a) - 1, int(b)))
        elif part:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < page_count]


def extract(path: Path, pages: list[int], min_rows: int = 2,
            min_density: float = 0.3) -> list[dict]:
    """Return a list of {page, index, rows, cols, markdown} for detected tables.

    Sparse detections (mostly-empty grids, the usual chart-misread artefact) are
    dropped via *min_density* — the fraction of non-empty cells required.
    PyMuPDF prints layout advisories to stdout; we redirect those to stderr so
    the caller's stdout (JSON / markdown) stays clean and parseable.
    """
    results: list[dict] = []
    with contextlib.redirect_stdout(sys.stderr):
        doc = fitz.open(str(path))
        for pno in pages:
            page = doc.load_page(pno)
            try:
                finder = page.find_tables()
            except Exception:
                continue
            for ti, tbl in enumerate(finder.tables):
                data = tbl.extract()
                if not data or len(data) < min_rows:
                    continue
                total = sum(len(r) for r in data)
                nonempty = sum(1 for r in data for cell in r if cell and str(cell).strip())
                if total == 0 or nonempty / total < min_density:
                    continue
                results.append({
                    "page": pno + 1,
                    "index": ti,
                    "rows": len(data),
                    "cols": max((len(r) for r in data), default=0),
                    "markdown": tbl.to_markdown(),
                })
        doc.close()
    return results


def _pages_with_text(path: Path, pages: list[int]) -> tuple[int, int]:
    """Count how many requested pages carry a usable text layer (for the hint)."""
    doc = fitz.open(str(path))
    text_pages = 0
    for pno in pages:
        if len(doc.load_page(pno).get_text("text").strip()) >= 20:
            text_pages += 1
    doc.close()
    return text_pages, len(pages)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract structured tables from a zsxq PDF as markdown.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file-id", type=int)
    g.add_argument("--path")
    ap.add_argument("--pages", help="e.g. '3-6' or '1,4,7' (1-indexed); default all")
    ap.add_argument("--min-rows", type=int, default=2, help="skip tables with fewer rows")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    path, name = _resolve_path(args.file_id, args.path)
    if not path.exists():
        raise SystemExit(f"File not found on disk: {path}")

    doc = fitz.open(str(path))
    page_count = doc.page_count
    doc.close()
    pages = _parse_pages(args.pages, page_count)

    tables = extract(path, pages, args.min_rows)

    if args.json:
        print(json.dumps({"file": name, "page_count": page_count,
                          "table_count": len(tables), "tables": tables},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"# Tables in {name}  ({len(tables)} found across {len(pages)} page(s))\n")
    if tables:
        for t in tables:
            print(f"## Page {t['page']} · table {t['index']} "
                  f"({t['rows']}×{t['cols']})\n")
            print(t["markdown"])
            print()
    else:
        text_pages, total = _pages_with_text(path, pages)
        if text_pages == 0:
            print("No tables found — these pages have **no text layer** "
                  "(image-only / scanned).")
            print("→ Render them and read the tables visually:")
            ident = f"--file-id {args.file_id}" if args.file_id else f"--path {path}"
            print(f"   python3 render_pdf_pages.py {ident} "
                  f"--pages {args.pages or '1-' + str(page_count)}")
            print("   then Read the PNG(s) — you are multimodal.")
        else:
            print(f"No grid-like tables detected ({text_pages}/{total} pages "
                  "have text). The data may be prose or chart-only; try "
                  "extract_pdf.py for narrative numbers or render_pdf_pages.py "
                  "for charts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
