"""Per-page OCR cache for the in-browser PDF viewer.

For PDFs with no embedded text (image-only / scanned), the viewer needs
positioned word boxes to inject as a synthetic text layer so native browser
text selection works the way it does in Apple Preview (which is just calling
Apple Vision under the hood).

This module exposes:
- get(file_id, page) -> list[dict] | None   (cached words; None if missing)
- compute(file_id, page, local_path) -> list[dict]   (OCRs the page via fitz
  + ocrmac, caches the result, returns it)
- compute_and_cache_lazy(...)               (compute() but skip if cached)

Each word dict is `{text, x, y, w, h}` in *normalised* page coords (0..1,
origin TOP-LEFT — already flipped from ocrmac's bottom-left convention so
the frontend doesn't have to know). The viewer multiplies by the rendered
viewport size to position each <span>.

Storage: db/notes.db, table pdf_page_ocr (file_id INT, page INT, words_json
TEXT, ocr_at TEXT, PRIMARY KEY (file_id, page)).
"""
from __future__ import annotations

import io
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from threading import Lock

DB_PATH = Path(__file__).parent / "db" / "notes.db"
_LOCK = Lock()
_INITED = False


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    global _INITED
    if _INITED:
        return
    with _LOCK:
        if _INITED:
            return
        with _conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pdf_page_ocr (
                  file_id    INTEGER NOT NULL,
                  page       INTEGER NOT NULL,
                  words_json TEXT NOT NULL,
                  ocr_at     TEXT NOT NULL,
                  PRIMARY KEY (file_id, page)
                )
                """
            )
            conn.commit()
        _INITED = True


def get(file_id: int, page: int) -> list[dict] | None:
    init_db()
    with _conn() as conn:
        row = conn.execute(
            "SELECT words_json FROM pdf_page_ocr WHERE file_id=? AND page=?",
            (file_id, page),
        ).fetchone()
    if not row:
        return None
    try:
        return json.loads(row["words_json"])
    except Exception:
        return None


def _save(file_id: int, page: int, words: list[dict]) -> None:
    init_db()
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with _LOCK, _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO pdf_page_ocr (file_id, page, words_json, ocr_at) "
            "VALUES (?, ?, ?, ?)",
            (file_id, page, json.dumps(words, separators=(",", ":")), now),
        )
        conn.commit()


def compute(file_id: int, page: int, local_path: str, *, zoom: float = 2.0,
            languages: tuple[str, ...] = ("en-US", "zh-Hans")) -> list[dict]:
    """OCR a single page and cache the result. Returns the words list."""
    import fitz  # type: ignore
    from ocrmac import ocrmac  # type: ignore
    from PIL import Image  # type: ignore

    doc = fitz.open(local_path)
    try:
        if page < 1 or page > doc.page_count:
            raise ValueError(f"page {page} out of range 1..{doc.page_count}")
        pg = doc[page - 1]
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        anns = ocrmac.OCR(
            img, recognition_level="accurate", language_preference=list(languages),
        ).recognize()
    finally:
        doc.close()

    # ocrmac returns [(text, confidence, bbox)] where bbox = (x, y, w, h) in
    # normalised [0,1] coords with origin BOTTOM-LEFT. We flip y so the
    # frontend gets top-left origin (more natural for DOM positioning).
    words: list[dict] = []
    for ann in anns:
        text, _conf, bbox = ann
        if not text or not text.strip():
            continue
        x, y, w, h = bbox
        words.append({
            "t": text,
            # round to 4 decimals → ~0.1px precision at 1000px page width;
            # cuts JSON payload to ~30% of full-precision floats.
            "x": round(x, 4),
            "y": round(1 - y - h, 4),  # flip y → top-left origin
            "w": round(w, 4),
            "h": round(h, 4),
        })
    # Sort by reading order (top-to-bottom, then left-to-right) so when the
    # browser builds a selection across our spans, the resulting string is
    # in natural reading order.
    words.sort(key=lambda d: (round(d["y"] * 200), round(d["x"] * 200)))
    _save(file_id, page, words)
    return words


def compute_if_missing(file_id: int, page: int, local_path: str) -> list[dict]:
    cached = get(file_id, page)
    if cached is not None:
        return cached
    return compute(file_id, page, local_path)
