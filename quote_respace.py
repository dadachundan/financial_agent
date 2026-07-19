"""Display-time repair for pre-fix squished PDF-highlight quotes.

Some PDFs lay out justified body text via per-glyph TJ positioning instead
of explicit space glyphs, so PDF.js's own text-layer extraction never
inserts spaces — "we know most of it" comes out as "weknowmostofit". The
capture-side fix (07485e3, pdf_viewer.py) routes new selections through an
OCR word-box fallback so freshly-created highlights get a readable `quote`.

Rows created *before* that fix already have the squished text frozen into
`pdf_inline_comments.quote` — a Tier-1, read-only table (see CLAUDE.md DB
Safety rules). This module never rewrites that row; it only re-derives a
readable string for display, using the page's cached OCR word boxes
(`pdf_page_ocr`, Tier-2) plus the highlight's own `rect_json` to find which
OCR lines the highlight covers.
"""
from __future__ import annotations

import json

import pdf_page_ocr as _ppo

_GARBLED_TOKEN_LEN = 20


def _looks_garbled(quote: str) -> bool:
    tokens = quote.split()
    return any(len(t) >= _GARBLED_TOKEN_LEN for t in tokens)


def respace(
    quote: str,
    *,
    source: str,
    file_id: int,
    page: int,
    rect_json: str | None,
    local_path: str | None,
) -> str:
    """Return a readable quote for display, falling back to `quote` as-is
    whenever the repair can't be attempted (missing rect/OCR/PDF, or the
    quote doesn't look garbled in the first place)."""
    if not quote or not rect_json or not local_path or not page:
        return quote
    if not _looks_garbled(quote):
        return quote
    try:
        rect = json.loads(rect_json)
        x, y, w, h = float(rect["x"]), float(rect["y"]), float(rect["w"]), float(rect["h"])
    except Exception:
        return quote

    lines = _ppo.get(source, file_id, page)
    if not lines:
        return quote

    try:
        import fitz  # type: ignore
        doc = fitz.open(local_path)
        try:
            if page < 1 or page > doc.page_count:
                return quote
            pg_rect = doc[page - 1].rect
            pw, ph = pg_rect.width, pg_rect.height
        finally:
            doc.close()
    except Exception:
        return quote
    if pw <= 0 or ph <= 0:
        return quote

    rx0, ry0, rx1, ry1 = x / pw, y / ph, (x + w) / pw, (y + h) / ph
    pad = 0.004
    matched = []
    for ln in lines:
        try:
            lx0, ly0 = float(ln["x"]), float(ln["y"])
            lx1, ly1 = lx0 + float(ln["w"]), ly0 + float(ln["h"])
        except Exception:
            continue
        if ly1 >= ry0 - pad and ly0 <= ry1 + pad and lx1 >= rx0 - pad and lx0 <= rx1 + pad:
            matched.append(ln)
    if not matched:
        return quote

    matched.sort(key=lambda d: (round(float(d["y"]) * 2000), round(float(d["x"]) * 2000)))
    text = " ".join(m["t"].strip() for m in matched if (m.get("t") or "").strip())
    return text or quote
