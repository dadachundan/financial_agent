#!/usr/bin/env python3
"""OCR a zsxq PDF using Apple Vision (via ocrmac).

Use this when `extract_pdf.py --header` reports `# empty-text pages: …`,
i.e. the PDF (or some of its pages) is rasterized. ocrmac runs Apple's
Vision framework on the Neural Engine — fast (~100-500 ms/page on
M-series), accurate on English, and free.

Usage:
    # OCR every empty-text page and cache to db/zsxq.db.pdf_files.ocr_text
    python3 ocr_pdf.py --file-id 184124515551842

    # Force re-OCR even if cached
    python3 ocr_pdf.py --file-id 184124515551842 --force

    # OCR specific pages only
    python3 ocr_pdf.py --file-id 184124515551842 --pages 1-5

    # Don't write to DB (print only)
    python3 ocr_pdf.py --file-id 184124515551842 --no-cache

Output (stdout): page-separated text in the same format as
extract_pdf.py — `===== Page N =====` markers. Pages that already
have selectable text are passed through from fitz; pages without are
OCR'd. The combined result is also stored on the row at
`pdf_files.ocr_text` keyed by file_id so future `extract_pdf.py` calls
get the cached text for free.
"""
from __future__ import annotations

import argparse
import io
import sqlite3
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "zsxq.db"


def _ensure_columns(conn: sqlite3.Connection) -> None:
    cols = {row[1] for row in conn.execute("PRAGMA table_info(pdf_files)").fetchall()}
    if "ocr_text" not in cols:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN ocr_text TEXT")
    if "ocr_at" not in cols:
        conn.execute("ALTER TABLE pdf_files ADD COLUMN ocr_at TEXT")
    conn.commit()


def _lookup_row(conn: sqlite3.Connection, file_id: int) -> dict | None:
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT file_id, local_path, ocr_text FROM pdf_files WHERE file_id = ?",
        (file_id,),
    ).fetchone()
    return dict(row) if row else None


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


def _looks_empty(t: str) -> bool:
    s = t.strip()
    if len(s) < 20:
        return True
    has_ws = any(c.isspace() for c in s)
    has_cjk = any("一" <= c <= "鿿" for c in s)
    if not has_ws and not has_cjk and len(s) < 200:
        return True
    return False


def _ocr_page(pix_png: bytes, languages: list[str]) -> str:
    """Run Apple Vision OCR on PNG bytes, return text in reading order."""
    from ocrmac import ocrmac
    from PIL import Image
    img = Image.open(io.BytesIO(pix_png))
    annotations = ocrmac.OCR(
        img, recognition_level="accurate", language_preference=languages
    ).recognize()
    # annotations is list of (text, confidence, bbox). bbox is (x, y, w, h)
    # in normalized [0,1] coords with origin BOTTOM-LEFT. Sort top-to-bottom
    # then left-to-right so reading order is sane for single-column pages.
    def sort_key(ann):
        _, _, bbox = ann
        x, y, w, h = bbox
        # bottom-left origin → flip y so top of page sorts first
        return (round((1 - y - h) * 100), round(x * 100))
    annotations.sort(key=sort_key)
    return "\n".join(t for t, _conf, _ in annotations if t.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file-id", type=int)
    g.add_argument("--path", type=str)
    ap.add_argument("--pages", type=str, default="",
                    help="comma-separated 1-indexed pages/ranges, e.g. '1-5,9'")
    ap.add_argument("--zoom", type=float, default=2.0,
                    help="render zoom for the OCR input (default 2.0)")
    ap.add_argument("--languages", type=str, default="en-US,zh-Hans",
                    help="comma-separated Vision language preferences")
    ap.add_argument("--force", action="store_true",
                    help="re-OCR even if pdf_files.ocr_text already populated")
    ap.add_argument("--no-cache", action="store_true",
                    help="print only, do not write back to the DB")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF (fitz) is required")

    # Resolve PDF path + existing cache
    cached: str | None = None
    if args.file_id is not None:
        conn = sqlite3.connect(DB_PATH)
        _ensure_columns(conn)
        row = _lookup_row(conn, args.file_id)
        if not row:
            sys.exit(f"file_id {args.file_id} not in {DB_PATH}")
        if not row["local_path"] or not Path(row["local_path"]).exists():
            sys.exit(f"PDF not on disk: {row['local_path']}")
        path = Path(row["local_path"])
        cached = row["ocr_text"]
    else:
        conn = None
        path = Path(args.path)
        if not path.exists():
            sys.exit(f"PDF not on disk: {path}")

    if cached and not args.force and not args.pages:
        # Already done — just print it back.
        sys.stdout.write(cached)
        if not cached.endswith("\n"):
            sys.stdout.write("\n")
        if conn is not None:
            conn.close()
        return

    languages = [s.strip() for s in args.languages.split(",") if s.strip()]
    doc = fitz.open(str(path))
    total = doc.page_count
    targets = _parse_pages(args.pages, total) if args.pages else list(range(1, total + 1))

    mat = fitz.Matrix(args.zoom, args.zoom)
    parts: list[str] = []
    ocr_used = 0
    t0 = time.time()
    for p in targets:
        page = doc[p - 1]
        native_text = (page.get_text() or "").strip()
        parts.append(f"===== Page {p} =====")
        if _looks_empty(native_text):
            pix = page.get_pixmap(matrix=mat)
            text = _ocr_page(pix.tobytes("png"), languages)
            ocr_used += 1
            parts.append(text)
        else:
            parts.append(native_text)
        parts.append("")
    doc.close()
    elapsed = time.time() - t0

    combined = "\n".join(parts)

    # Cache to DB
    if args.file_id is not None and conn is not None and not args.no_cache:
        # Only write back when we OCR'd the full document (no --pages slice)
        if not args.pages:
            conn.execute(
                "UPDATE pdf_files SET ocr_text = ?, ocr_at = datetime('now') WHERE file_id = ?",
                (combined, args.file_id),
            )
            conn.commit()
        conn.close()

    sys.stdout.write(combined)
    if not combined.endswith("\n"):
        sys.stdout.write("\n")
    print(f"\n# ocr_pages={ocr_used}/{len(targets)}  elapsed={elapsed:.1f}s",
          file=sys.stderr)


if __name__ == "__main__":
    main()
