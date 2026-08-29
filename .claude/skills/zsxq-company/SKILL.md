---
name: zsxq-company
description: Read all relevant zsxq broker PDFs for one company/ticker, summarize each report's bull or bear stance, and prepare a debate-ready view from the user's local research library. Use when the user asks for zsxq-company, company-level broker report synthesis, or wants to discuss a ticker from their zsxq PDFs.
---

# zsxq Company Report Synthesis

Use this skill when the user gives one company parameter such as `MRVL`,
`NVDA`, `TSM`, or a company name and wants the local zsxq PDF library pulled
into the conversation: which reports are bullish, which are bearish, why, and
what disagreement is worth debating.

The source of truth is the local database `db/zsxq.db` plus the downloaded PDFs
referenced by `pdf_files.local_path`. Do not use web search for the report
content unless the user explicitly asks for outside context.

**Interpreter:** run project scripts with `/opt/anaconda3/bin/python3`.

## Workflow

### 1. Resolve the company parameter

Normalize the user's parameter to an uppercase ticker when it looks like a
listed US ticker. Keep the original string as an alternate search term.

If the user gives only the skill name with no company, ask for the company or
ticker. Otherwise proceed directly.

### 2. Build the report queue

Use the helper script from the project root:

```bash
/opt/anaconda3/bin/python3 .claude/skills/zsxq-company/scripts/find_company_reports.py MRVL --limit 30
```

The script searches the structured ticker fields, existing `pdf_cards`, and
ranked zsxq FTS text. It emits JSON with `rows` containing `file_id`, `name`,
`topic_title`, `summary`, `bank`, `create_time`, `page_count`, `tickers`,
`local_path`, `local_exists`, `pdf_url`, and retrieval `reasons`.

Prefer rows where:

- `local_exists` is true.
- the ticker/card match is direct, not only a fuzzy text hit.
- the title or summary is company-specific rather than broad sector coverage.
- the report is substantive enough to carry a thesis.

If the queue is huge, read the best 8-12 first and tell the user that the rest
are lower-priority candidates. If fewer than 3 local PDFs exist, read all local
matches and say the library is sparse.

### 3. Read each PDF

For each selected `file_id`, use the existing zsxq analyzer scripts:

```bash
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --file-id <file_id>
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id <file_id> --header --max-chars 120000
```

If extraction reports image-only pages, run OCR and re-extract:

```bash
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py --file-id <file_id>
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id <file_id> --header --max-chars 120000
```

For cover pages, recommendation tables, valuation bridges, or charts where text
is ambiguous, render the relevant pages and inspect the images:

```bash
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/render_pdf_pages.py --file-id <file_id> --pages 1
```

### 4. Classify each report's stance

For every report actually read, produce a compact per-report card:

- **Stance:** Bullish / Bearish / Mixed / Neutral / Not enough evidence.
- **Why:** the report's explicit thesis, not your outside opinion.
- **Key evidence:** growth drivers, margin/estimate revisions, valuation,
  cycle/channel checks, customer exposure, AI/data-center assumptions, risks.
- **Valuation call:** rating, price target, upside/downside, or valuation
  framework when present.
- **What would change the view:** catalysts or risk triggers the report names.
- **Citation:** include file_id and page numbers for claims pulled from the PDF.

Treat broad sector reports as useful only for the parts that mention the focal
company. Do not force a bull/bear label if the report is only an industry
overview with no stock call.

### 5. Synthesize the debate map

After the per-report cards, summarize:

- Bull camp: the repeated arguments and which reports support them.
- Bear camp: the repeated arguments and which reports support them.
- Core disagreement: the assumptions that actually drive the spread between
  views, such as AI accelerator attach rate, custom silicon risk, gross margin,
  networking cycle timing, inventory digestion, or valuation multiple.
- Questions for the user: 3-5 debate prompts that would let the next exchange
  be sharper after the user reads selected PDFs.

Keep the answer useful for a human investor deciding what to read next. Lead
with the report-by-report summary, then the synthesis.

