#!/usr/bin/env python3
"""Strip a per-recipient anti-piracy watermark applied via PDF incremental update.

Some PDF distributors (notably zsxq sellers re-saving via macOS Preview's
"AppendMode") draw a steganographic fingerprint on top of a research PDF and
save it as an *incremental update* — i.e. the original revision is left intact
at the start of the file, and a small trailer at the end rewrites a few page
objects to point at watermark-only content streams.

Symptom: macOS Preview (strictly compliant) honors the update and renders the
first few pages as blank, while Android viewers that ignore incremental updates
show the original content.

The fix is to truncate the file right after the first `%%EOF` marker, dropping
the incremental update and leaving the original revision behind.

Usage:
    python3 strip_pdf_watermark.py <input.pdf> [output.pdf]

If <output.pdf> is omitted, writes to <input>.original.pdf next to the input.
"""

from __future__ import annotations

import sys
from pathlib import Path


def strip_incremental_updates(src: Path, dst: Path) -> dict:
    data = src.read_bytes()
    eof = b"%%EOF"
    markers: list[int] = []
    start = 0
    while True:
        idx = data.find(eof, start)
        if idx == -1:
            break
        markers.append(idx)
        start = idx + len(eof)
    if not markers:
        raise ValueError(f"{src}: not a valid PDF (no %%EOF marker found)")
    if len(markers) == 1:
        raise ValueError(
            f"{src}: only one revision present — nothing to strip "
            "(this file has no incremental update)"
        )
    cut = markers[0] + len(eof)
    if cut < len(data) and data[cut : cut + 1] in (b"\n", b"\r"):
        cut += 1
        if data[cut - 1 : cut] == b"\r" and data[cut : cut + 1] == b"\n":
            cut += 1
    dst.write_bytes(data[:cut])
    return {
        "src_size": len(data),
        "dst_size": cut,
        "revisions_stripped": len(markers) - 1,
    }


def verify(path: Path) -> dict:
    import fitz

    doc = fitz.open(path)
    try:
        page_count = doc.page_count
        first_text = doc.load_page(0).get_text()[:120]
        first_images = len(doc.load_page(0).get_images(full=True))
    finally:
        doc.close()
    return {
        "pages": page_count,
        "page1_text_preview": first_text,
        "page1_image_count": first_images,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0 if len(argv) >= 2 else 2
    src = Path(argv[1]).expanduser()
    if not src.is_file():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 1
    if len(argv) >= 3:
        dst = Path(argv[2]).expanduser()
    else:
        dst = src.with_name(src.stem + ".original" + src.suffix)
    try:
        stats = strip_incremental_updates(src, dst)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"wrote {dst}")
    print(
        f"  stripped {stats['revisions_stripped']} incremental update(s) "
        f"({stats['src_size']:,} -> {stats['dst_size']:,} bytes, "
        f"-{stats['src_size'] - stats['dst_size']:,})"
    )
    try:
        info = verify(dst)
    except Exception as e:
        print(f"warning: could not verify output with PyMuPDF: {e}", file=sys.stderr)
        return 0
    print(
        f"  verified: {info['pages']} pages, page 1 has "
        f"{info['page1_image_count']} image(s); "
        f"text preview: {info['page1_text_preview']!r}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
