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
Page boundaries appear as `===== Page N =====`. With `--header`, an
additional line is emitted listing pages whose text extraction came
back empty:

```
# empty-text pages (likely scanned/image-only — render with render_pdf_pages.py): 1,2,3,...
```

Use this hint to drive step 3b.

### 3b. Fall back to visual reading for image-only pages or charts

Bank PDFs in zsxq are often a **mix**: some pages have selectable
text, others are flattened images (cover, charts, exhibits, occasional
scanned editions). **The first page is the highest-value one** —
banks pack the thesis, target prices, and ratings into page 1, and
it's the page most likely to be rasterized. Always make sure you have
real content for page 1; if its text is empty/garbled, render it.

For each page that came back empty (or any page you suspect is a chart
holding key numbers), render it to a PNG and **read the PNG directly
with the Read tool — you are multimodal**. Do not try OCR locally
unless `tesseract` / `paddleocr` / `easyocr` is actually installed
(usually it isn't).

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
blow context:** prioritize p1 (always), the final 1-2 pages
(disclosure summary / target-price box), and any page whose
neighbours' text mentions a table/exhibit you need. If even that
isn't enough, fall back to the `summary` column on the row — banks
or zsxq curators often paste the full 翻译精华 there, and it's a
legitimate substitute when the PDF itself is unreadable. Be explicit
about that switch in your answer.

### 3c. Charts

Charts live inside the page images, so the same render → Read flow
covers them. When reading a chart:

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
- If `extract_pdf.py --header` reports "empty-text pages: …", that
  page is rasterized — go to step 3b and render it.
- This skill answers questions about **one** PDF per invocation. For
  multi-file synthesis, run the skill per file and stitch the answers
  yourself.
