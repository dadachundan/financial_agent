#!/usr/bin/env python3
"""Render zsxq PDF pages to PNGs so Claude can read them visually.

Use this when `extract_pdf.py` returns empty text for a page (the PDF
is scanned / image-only / the page is a chart). Render to PNG and feed
the path back to Claude via the Read tool — Claude is multimodal and
will read the page contents directly.

Usage:
    # Render every page
    python3 render_pdf_pages.py --file-id 184124515551842

    # Render specific pages
    python3 render_pdf_pages.py --file-id 184124515551842 --pages 1,3-5

    # Only render pages with no extractable text (the common case)
    python3 render_pdf_pages.py --file-id 184124515551842 --only-empty

Output: writes PNGs to a temp dir and prints one absolute path per
line, with the page number. Example:
    /tmp/zsxq_render_184124515551842/p01.png  page=1
    /tmp/zsxq_render_184124515551842/p03.png  page=3

Then in Claude: use the Read tool on each PNG path.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "zsxq.db"


def _lookup_path(file_id: int) -> str | None:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    row = conn.execute(
        "SELECT local_path FROM pdf_files WHERE file_id = ?", (file_id,)
    ).fetchone()
    conn.close()
    return row[0] if row and row[0] else None


def _parse_pages(spec: str, total: int) -> list[int]:
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return [p for p in pages if 1 <= p <= total]


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file-id", type=int)
    g.add_argument("--path", type=str)
    ap.add_argument("--pages", type=str, default="",
                    help="comma-separated 1-indexed pages/ranges, e.g. '1,3-5'")
    ap.add_argument("--only-empty", action="store_true",
                    help="render only pages where get_text() returns <20 chars")
    ap.add_argument("--zoom", type=float, default=2.0,
                    help="render zoom factor (default 2.0 = ~150dpi-ish)")
    ap.add_argument("--out-dir", type=str, default="",
                    help="output dir (default /tmp/zsxq_render_<file_id>)")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF (fitz) is required: pip install pymupdf")

    if args.file_id is not None:
        path_str = _lookup_path(args.file_id)
        if not path_str:
            sys.exit(f"file_id {args.file_id} not in {DB_PATH}")
        path = Path(path_str)
        default_out = f"/tmp/zsxq_render_{args.file_id}"
    else:
        path = Path(args.path)
        default_out = f"/tmp/zsxq_render_{path.stem}"

    if not path.exists():
        sys.exit(f"PDF not on disk: {path}")

    out_dir = Path(args.out_dir or default_out)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(path))
    total = doc.page_count

    if args.pages:
        targets = _parse_pages(args.pages, total)
    else:
        targets = list(range(1, total + 1))

    if args.only_empty:
        def _looks_empty(t: str) -> bool:
            s = t.strip()
            if len(s) < 20:
                return True
            has_ws = any(c.isspace() for c in s)
            has_cjk = any("一" <= c <= "鿿" for c in s)
            if not has_ws and not has_cjk and len(s) < 200:
                return True
            return False
        kept = []
        for p in targets:
            txt = doc[p - 1].get_text() or ""
            if _looks_empty(txt):
                kept.append(p)
        targets = kept

    mat = fitz.Matrix(args.zoom, args.zoom)
    for p in targets:
        pix = doc[p - 1].get_pixmap(matrix=mat)
        out_path = out_dir / f"p{p:02d}.png"
        pix.save(str(out_path))
        print(f"{out_path}  page={p}")

    doc.close()
    if not targets:
        print("# no pages rendered (all had extractable text, or filter excluded them)",
              file=sys.stderr)


if __name__ == "__main__":
    main()
