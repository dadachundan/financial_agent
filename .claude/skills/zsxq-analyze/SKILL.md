---
name: zsxq-analyze
description: Analyze a PDF stored in db/zsxq.db (the zsxq report library) and answer the user's question about it. Use whenever the user references a zsxq PDF by file_id, filename, or topic keyword — e.g. "what stocks does file_id 184124282514242 recommend?", "summarize the Deloitte report from zsxq", "/zsxq-analyze what does <name> say about robotics". Pair: `/zsxq-recommend` finds candidate file_ids to feed into this skill.
---

# Analyze zsxq PDF

Given a question that references a PDF in the zsxq library
(`db/zsxq.db`, table `pdf_files`), locate the file, extract its text,
and answer the question in-context. **You — Claude — do the analysis
in-context.** The scripts only look up rows and extract text; do not
call any external LLM (no MiniMax, no API).

## Workflow

### 1. Parse the request

Pull two things out of the user's prompt:

- **An identifier** for the PDF. One of:
  - a numeric `file_id` (15+ digit number, e.g. `184124282514242`)
  - a filename / topic substring (e.g. `Deloitte 2026`, `自动驾驶`)
- **The actual question** — what they want answered (stocks named,
  summary, thesis, risks, …). Strip the identifier out of the question
  text before answering.

**Default question (when the user only gives an identifier):**
summarize the report and highlight the key takeaways. Lead with a 3-5
bullet TL;DR, then a section-by-section précis, then a short
"highlights / what's notable" block (surprises, contrarian calls,
named stocks, hard numbers). Cite page numbers when you make specific
claims.

### 2. Find the PDF row

```bash
# Exact file_id
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py \
    --file-id 184124282514242

# Substring query against name / topic_title / summary / tags / comment
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py \
    --query "Deloitte 2026" --limit 5
```

Output: JSON `{count, rows:[{file_id, name, topic_title, summary,
local_path, file_size, page_count, create_time, tickers, tags, comment,
ai_robotics_analysis, categories_analysis, bank, group_id, claude_rating,
user_rating, local_exists}, ...]}`. Rows sort by `create_time DESC`.

Decision rules:

- 0 rows → tell the user nothing matched and show what they searched.
- 1 row → use it.
- >1 row in `--query` mode → if one is an obvious match (substring of
  `name` very close), use it; otherwise show the user the top 3
  candidates (file_id + name + create_time) and ask which one.
- `local_exists == false` → the PDF row exists but the file is gone
  from disk. Tell the user the path and stop — do not fabricate.

### 3. Extract the PDF text

```bash
python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py \
    --file-id 184124282514242 --header
```

Useful flags:

- `--pages 1-5,12` — only certain pages. Use this when the question is
  narrow (e.g. "what's on the recommendation page") and the PDF is
  large.
- `--max-chars 80000` — cap combined output. Defaults to no cap; set
  this if the file is huge and the question is general.
- `--header` — prepend a one-line metadata header (file_id, name,
  topic, page count). Recommended whenever you'll quote the text back.

Extractor preference order: PyMuPDF (`fitz`) → `pdfplumber` → `PyPDF2`.
Page boundaries appear as `===== Page N =====`. If a per-page OCR
cache exists on the row (`pdf_files.ocr_text`, populated by
`ocr_pdf.py`), it is **silently merged in** for any page where
fitz/pdfplumber/PyPDF2 returned nothing — so once a PDF has been
OCR'd, every subsequent `extract_pdf.py` is free and instant.

With `--header`, an additional line is emitted listing pages whose
text extraction came back empty *and* are not in the OCR cache:

```
# empty-text pages (image-only — run ocr_pdf.py --file-id <id> to cache OCR, then re-extract; or render_pdf_pages.py for visual reading): 1,2,3,...
```

Use this hint to drive step 3b (OCR) and 3c (visual reading).

### 3b. OCR image-only pages (default for English/Chinese bank PDFs)

`ocr_pdf.py` uses Apple's Vision framework (`ocrmac`) on the M-series
Neural Engine — ~1 s/page, ~98%+ accuracy on clean prints, free, no
external API. **Run this whenever step 3 reports empty pages**:

```bash
# OCR the whole PDF and cache to db/zsxq.db.pdf_files.ocr_text
python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py \
    --file-id 184124515551842

# Limit to specific pages (won't update the cache)
python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py \
    --file-id 184124515551842 --pages 1-3,7

# Re-OCR even if cached
python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py \
    --file-id 184124515551842 --force
```

After this runs once, `extract_pdf.py` will automatically pick up the
cached text — no need to read OCR output directly. Just re-run
`extract_pdf.py --file-id … --header`.

OCR limitations to keep in mind:

- **Reading order on multi-column pages may scramble** — ocrmac sorts
  lines top-to-bottom by visual position, which is fine for
  single-column slides (most bank reports) but garbles 2-column
  research notes. For those, use step 3c.
- **Tables come out as flat lines of text**, not structured cells. If
  you specifically need a table's values cell-by-cell, fall back to
  step 3c on that page.
- **Charts are not readable by OCR at all** — only the title, axis
  labels, and any printed annotations come through. Trends, bar
  heights, and visual takeaways need step 3c.

### 3c. Fall back to visual reading for charts (and OCR-hostile pages)

Use this for pages where OCR is structurally insufficient: charts,
complex tables, multi-column research notes, exhibit-heavy slides.
**The first page is also the highest-value one** — banks pack the
thesis, target prices, and ratings into p. 1, so even with the OCR
cache present, glancing at the rendered p. 1 is worth ~50 ms of your
attention because the visual layout (call-out boxes, badges) carries
extra signal that flat text loses.

Render the page(s) to PNG and **read each PNG with the Read tool —
you are multimodal**.

```bash
# Render only the pages where text extraction was empty
python3 .claude/skills/zsxq-analyze/scripts/render_pdf_pages.py \
    --file-id 184124282514242 --only-empty

# Or render specific pages (e.g. p1 cover + p7 chart)
python3 .claude/skills/zsxq-analyze/scripts/render_pdf_pages.py \
    --file-id 184124282514242 --pages 1,7
```

Output is one line per rendered page, e.g.
`/tmp/zsxq_render_184124282514242/p01.png  page=1`. Then call the
**Read tool** on each PNG path — that gives you the page contents
visually (text, table values, chart titles + axis labels + visible
data points). Quote what you actually see; don't invent precise
numbers off a chart, but ranges and qualitative shape are fair.

**When the PDF is entirely image-only and rendering every page would
blow context:** OCR'ing (step 3b) gives you cheap full-text access
for free, so reach for visual reading only on the specific pages
that have charts or complex layout. If even that isn't enough, fall
back to the `summary` column on the row — banks or zsxq curators
often paste the full 翻译精华 there. Be explicit about the switch in
your answer.

When reading a chart visually:

- Capture the chart title, axis labels and units, the legend, and the
  shape of the series ("X rises from ~5% to ~30% between 2020 and
  2026").
- Pull any explicit data labels printed on the chart (banks often
  annotate the most recent point).
- Don't fabricate decimals — if the line is between two gridlines,
  say "~12%", not "12.4%".

### 4. Answer the question

Read the extracted text and answer **only what the user asked**. Quote
page numbers when you cite specific claims (e.g. "p. 12: …"). If the
PDF doesn't contain an answer, say so — don't pad with general industry
knowledge.

When the user asked for stocks / tickers specifically:

- Prefer the explicit list in the PDF.
- Cross-check against the `tickers` column already stored on the row
  (when present, it's been pre-tagged) and reconcile any mismatch.

## Notes

- DB is read-only here. Never write to `db/zsxq.db` from this skill.
- Local paths typically live under
  `/Users/x/Downloads/zsxq_reports/YYYY_MM_DD/<file>.pdf`.
- For Chinese PDFs, `fitz` usually returns clean UTF-8; if you see
  garbled output, the extractor probably fell through to `PyPDF2` —
  add `pdfplumber` or `pymupdf` to the env and re-run.
- If `extract_pdf.py --header` reports "empty-text pages: …" and no
  OCR cache exists, the standard play is **3b first** (OCR with
  `ocr_pdf.py`, then re-run `extract_pdf.py`). Go to 3c (render to
  PNG, Read visually) only when OCR is insufficient — charts, dense
  tables, multi-column layouts.
- `ocrmac` requires macOS (Apple Vision framework) — `pip install
  ocrmac` already done locally. On a non-Mac box, fall through to 3c.
- This skill answers questions about **one** PDF per invocation. For
  multi-file synthesis, run the skill per file and stitch the answers
  yourself.
