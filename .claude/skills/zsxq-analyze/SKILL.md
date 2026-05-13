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
Page boundaries appear as `===== Page N =====`.

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
- This skill answers questions about **one** PDF per invocation. For
  multi-file synthesis, run the skill per file and stitch the answers
  yourself.
