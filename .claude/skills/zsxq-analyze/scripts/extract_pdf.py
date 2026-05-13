#!/usr/bin/env python3
"""Extract text from a zsxq PDF, page by page.

Usage:
    python3 extract_pdf.py --file-id 184124282514242 [--header]
    python3 extract_pdf.py --path /path/to/file.pdf
    python3 extract_pdf.py --file-id ...  --pages 1-5,12
    python3 extract_pdf.py --file-id ...  --max-chars 80000

Reads with PyMuPDF (`fitz`) when available — falls back to `pdfplumber`,
then `PyPDF2`. Pages are printed in order separated by:

    ===== Page N =====

`--header` prepends a one-line metadata header pulled from db/zsxq.db
(file_id, name, topic_title, page_count). Use this when feeding the
output back to Claude so it knows which file it's looking at.

`--pages` is a comma-separated list of 1-indexed pages or `A-B` ranges.
If omitted, every page is extracted.

`--max-chars` truncates the combined output (after page markers) and
appends a `... [truncated]` note. 0 = no cap. Default 0.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
DB_PATH      = PROJECT_ROOT / "db" / "zsxq.db"


def _lookup_meta(file_id: int) -> dict | None:
    if not DB_PATH.exists():
        return None
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cols = {row[1] for row in conn.execute("PRAGMA table_info(pdf_files)").fetchall()}
    extra = ", ocr_text" if "ocr_text" in cols else ""
    cur = conn.execute(
        f"SELECT file_id, name, topic_title, local_path, page_count, "
        f"file_size, create_time{extra} FROM pdf_files WHERE file_id = ?",
        (file_id,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def _looks_empty(t: str) -> bool:
    s = t.strip()
    if len(s) < 20:
        return True
    has_ws = any(c.isspace() for c in s)
    has_cjk = any("一" <= c <= "鿿" for c in s)
    if not has_ws and not has_cjk and len(s) < 200:
        return True
    return False


def _parse_cached_ocr(ocr_text: str) -> dict[int, str]:
    """Parse '===== Page N =====' blocks back into a {page_num: text} dict."""
    import re
    out: dict[int, str] = {}
    if not ocr_text:
        return out
    parts = re.split(r"^===== Page (\d+) =====\s*$", ocr_text, flags=re.MULTILINE)
    # split yields [prefix, '1', body, '2', body, ...]
    for i in range(1, len(parts), 2):
        try:
            page_num = int(parts[i])
            body = parts[i + 1].rstrip()
            out[page_num] = body
        except (ValueError, IndexError):
            continue
    return out


def _parse_pages(spec: str, total: int) -> list[int]:
    """1-indexed page list from a spec like '1-3,7,10-12'."""
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            lo, hi = int(a), int(b)
            pages.extend(range(lo, hi + 1))
        else:
            pages.append(int(part))
    return [p for p in pages if 1 <= p <= total]


def _extract_with_fitz(path: Path, page_filter: list[int] | None) -> list[tuple[int, str]]:
    import fitz  # PyMuPDF
    doc = fitz.open(str(path))
    total = doc.page_count
    targets = page_filter if page_filter else list(range(1, total + 1))
    out = []
    for p in targets:
        if not (1 <= p <= total):
            continue
        text = doc[p - 1].get_text() or ""
        out.append((p, text))
    doc.close()
    return out


def _extract_with_pdfplumber(path: Path, page_filter: list[int] | None):
    import pdfplumber
    out = []
    with pdfplumber.open(str(path)) as pdf:
        total = len(pdf.pages)
        targets = page_filter if page_filter else list(range(1, total + 1))
        for p in targets:
            if not (1 <= p <= total):
                continue
            text = pdf.pages[p - 1].extract_text() or ""
            out.append((p, text))
    return out


def _extract_with_pypdf2(path: Path, page_filter: list[int] | None):
    from PyPDF2 import PdfReader
    reader = PdfReader(str(path), strict=False)
    total = len(reader.pages)
    targets = page_filter if page_filter else list(range(1, total + 1))
    out = []
    for p in targets:
        if not (1 <= p <= total):
            continue
        text = reader.pages[p - 1].extract_text() or ""
        out.append((p, text))
    return out


def extract(path: Path, page_filter: list[int] | None) -> list[tuple[int, str]]:
    last_err: Exception | None = None
    for fn in (_extract_with_fitz, _extract_with_pdfplumber, _extract_with_pypdf2):
        try:
            return fn(path, page_filter)
        except ImportError as e:
            last_err = e
            continue
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue
    sys.exit(f"could not extract from {path}: {last_err}")


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file-id", type=int)
    g.add_argument("--path", type=str)
    ap.add_argument("--pages", type=str, default="",
                    help="comma-separated 1-indexed pages/ranges, e.g. '1-3,7'")
    ap.add_argument("--max-chars", type=int, default=0,
                    help="truncate combined output (0 = no cap)")
    ap.add_argument("--header", action="store_true",
                    help="prepend one-line metadata header (requires --file-id "
                         "or a path that resolves back in the DB)")
    args = ap.parse_args()

    meta: dict | None = None
    if args.file_id is not None:
        meta = _lookup_meta(args.file_id)
        if not meta:
            sys.exit(f"file_id {args.file_id} not in {DB_PATH}")
        path = Path(meta["local_path"] or "")
    else:
        path = Path(args.path)

    if not path.exists():
        sys.exit(f"PDF not on disk: {path}")

    # Resolve total page count for --pages parsing without opening twice
    # when possible (fitz/PyMuPDF makes this cheap; we just do it inside extract).
    page_filter: list[int] | None = None
    if args.pages:
        # We need a total to bound the parse. Open with fitz quickly.
        try:
            import fitz
            doc = fitz.open(str(path))
            total = doc.page_count
            doc.close()
        except Exception:
            total = 10_000
        page_filter = _parse_pages(args.pages, total)

    pages = extract(path, page_filter)

    # Swap in cached OCR text for any page where fitz/pdfplumber/PyPDF2
    # came back empty. The cache is populated by scripts/ocr_pdf.py.
    cached_ocr = _parse_cached_ocr((meta or {}).get("ocr_text") or "")
    if cached_ocr:
        swapped = []
        for p, t in pages:
            if _looks_empty(t) and p in cached_ocr:
                swapped.append((p, cached_ocr[p]))
            else:
                swapped.append((p, t))
        pages = swapped

    parts: list[str] = []
    if args.header:
        if meta:
            parts.append(
                f"# file_id={meta['file_id']}  "
                f"name={meta['name']}  "
                f"topic={meta.get('topic_title') or ''}  "
                f"pages={meta.get('page_count') or len(pages)}"
            )
        else:
            parts.append(f"# path={path}  pages_extracted={len(pages)}")
        empty_pages = [p for p, t in pages if _looks_empty(t)]
        if empty_pages:
            parts.append(
                "# empty-text pages (image-only — run "
                f"ocr_pdf.py --file-id <id> to cache OCR, then re-extract; "
                f"or render_pdf_pages.py for visual reading): "
                f"{','.join(map(str, empty_pages))}"
            )
        parts.append("")

    for p, text in pages:
        parts.append(f"===== Page {p} =====")
        parts.append(text.rstrip())
        parts.append("")

    combined = "\n".join(parts)
    if args.max_chars and len(combined) > args.max_chars:
        combined = combined[: args.max_chars] + "\n\n... [truncated]"

    sys.stdout.write(combined)
    if not combined.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
