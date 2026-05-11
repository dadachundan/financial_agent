---
name: sec-report-summary
description: Given a US ticker, summarize the company's SEC filings stored locally under http://localhost:5001/sec/ (db/financial_reports.db). Produces per-report highlights and a year-over-year change narrative. Use when the user asks for a multi-year SEC summary, "summarize 10-Ks for X", "how has Y changed over the years", or similar.
---

# SEC Report Summary

Given a ticker, pull the SEC filings already downloaded locally (the
`/sec/` Flask service / `db/financial_reports.db`), read each filing's
narrative text, and produce:

1. **Per-report highlights** — one tight section per filing.
2. **Changes over years** — a short narrative comparing the most recent
   filings to older ones (revenue mix shifts, new risk factors, segment
   reorganizations, capital-return changes, etc.).

You — Claude — do the summarization in-context. The scripts below only
locate and extract the relevant narrative sections; do **not** call any
external LLM (no MiniMax, no API).

## Workflow

### 1. List filings for the ticker

```bash
python3 .claude/skills/sec-report-summary/scripts/list_reports.py \
    --ticker <TICKER> --form 10-K --last 10
```

Flags:
- `--ticker AAPL` (required, uppercase)
- `--form 10-K` (default; use `10-Q` or `8-K`, or `--all` for every form)
- `--last N` (keep the N most recent; 0 = all)
- `--asc` (oldest → newest in output; default is newest first)

Output: JSON `{ticker, source, count, rows:[{id, form_type, filed_date,
period_of_report, local_path, …}, …]}`. `source` is `"api"` if the live
service at `http://localhost:5001/sec/` answered, else `"db"`.

**Default scope:** the most recent **10 × 10-K** filings. Only widen this
if the user asks ("include 10-Qs", "all years", "since 2015", etc.).

If the count is 0, tell the user there are no filings and offer to run
`fetch_financial_report.py` from the main project directory.

### 2. Extract narrative text from each filing

For each report `id` you want to summarize:

```bash
python3 .claude/skills/sec-report-summary/scripts/extract_report.py \
    --id <REPORT_ID> --max-chars 60000 --header
```

Flags:
- `--id <int>` (looks up `local_path` + `form_type` from the DB)
- `--path <file>` `--form 10-K` (alternative: extract a specific file)
- `--max-chars 60000` (truncate; default 60k)
- `--header` (prepend a one-line metadata header — recommended)

The extractor returns just the substantive sections — Item 1/1A for
10-K, Item 2/1A Part II for 10-Q, all material items for 8-K — so you
won't be wading through XBRL tables and boilerplate.

**Performance:** read filings sequentially, not all at once. For a 10×10-K
run, that's ~10 separate `extract_report.py` calls. You may run them in
parallel from a single tool-use block to save wall time.

### 3. Summarize, in this order

For each filing (newest first), write a short block:

```markdown
### FY2025 10-K (filed 2025-10-31, period 2025-09-27)
- **Business**: <2–3 sentence what-they-do snapshot, calling out new segments,
  product lines, or geographic shifts introduced this year.>
- **Key risks**: <3–5 of the most consequential / distinctive risk factors —
  skip generic ones like "general economic conditions" unless newly emphasized.>
- **New this year**: <bullets only if something genuinely changed vs the prior
  filing — new disclosures, restructurings, segment renames, new litigation,
  AI/regulatory language, etc.>
```

Then a final **Changes over the years** section: 5–10 bullets identifying
the *trajectory* across filings. Examples of what to look for:
- Segment reporting changes (new segments added, others merged)
- Geographic mix shifts (e.g. China revenue going from highlight to risk)
- Risk-factor evolution (new categories appearing — cyber, AI, climate, tariffs)
- Product-line transitions, sunset products
- Capital allocation language (buybacks, dividends, M&A appetite)
- Headcount / employee disclosures
- Litigation or regulatory matters that appear, persist, or resolve

## Output format

A single Markdown document. Put the per-report blocks newest → oldest,
then the "Changes over the years" section at the end. Title it
`# <Company Name> (<TICKER>) — SEC filings summary, <oldest year>–<newest year>`.

**Always write the summary to** `reports/<TICKER>_<YYYYMMDD>.md` (relative
to the project root — `/Users/x/projects/financial_agent/reports/`).
Create the `reports/` directory if it doesn't exist. This directory is
gitignored, so the files won't pollute the repo. After writing the file,
print its path in chat and inline the report content for the user to read.

## Defaults & guardrails

- Default form: `10-K` (annual; best for YoY comparison).
- Default count: 10 filings. Ask before going larger than 20.
- Don't blindly include every 10-Q + 10-K — that's noisy. If the user
  wants quarterly granularity, summarize the most recent 4× 10-Q only and
  combine with the surrounding 10-Ks.
- If `extract_report.py` returns empty text for a filing, note "extraction
  failed" for that row and move on — don't fabricate.
- Cite filing dates and periods explicitly so the user can cross-check.
- The narrative comes from filings; don't add external news or current
  events the user didn't ask about.
