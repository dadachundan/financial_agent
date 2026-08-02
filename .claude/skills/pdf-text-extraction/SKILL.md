---
name: pdf-text-extraction
description: Three-tier flow for extracting text from image-only / scanned PDF pages in this project (rasterized cover pages, exhibit-only slides, fully-scanned reports) where fitz.get_text() returns empty. Use ocrmac (Apple Vision) by default, Marker for layout/tables, Claude vision only for charts — never Tesseract. Load when a PDF page yields no text and you need OCR, or when deciding how to read a scanned filing.
---

# PDF Text Extraction (image-only / scanned reports)

When a PDF page returns empty text from `fitz.get_text()` (rasterized
cover pages, exhibit-only slides, the occasional fully-scanned report),
use the three-tier flow — never try Tesseract:

1. **Default: `ocrmac`** (Apple Vision framework on the Neural Engine).
   ~1 s/page on M-series, ~98%+ on clean English/Chinese, zero RAM
   overhead. Already wrapped in
   `.claude/skills/zsxq-analyze/scripts/ocr_pdf.py`, which writes the
   result back to `pdf_files.ocr_text` so re-runs are free.
2. **Layout-tier upgrade: Marker** (built on Surya, PyTorch+MPS). Use
   only when ocrmac scrambles the reading order or when you need
   tables-as-markdown — e.g. multi-column research notes or dense
   financial tables. Not wired in yet; add when the need first comes
   up.
3. **Vision LM (Claude multimodal) for charts.** When the meaning
   lives in a chart, axis labels alone aren't enough — render the
   page via `render_pdf_pages.py` and Read the PNG directly. Use
   sparingly because vision tokens are ~$0.03/page.

The corresponding DB columns on `pdf_files` are `ocr_text` (cached
page-marked text) and `ocr_at` (timestamp). Both are added by
`ocr_pdf.py` on first use — no manual migration.
