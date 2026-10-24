---
name: zsxq-company
description: Read all relevant zsxq broker PDFs for one company/ticker, always open with a per-broker price-target table + timeline chart + why each target changed, then summarize each report's bull or bear stance, and prepare a debate-ready view from the user's local research library. Use when the user asks for zsxq-company, company-level broker report synthesis, or wants to discuss a ticker from their zsxq PDFs.
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

### 3. Price-target timeline (ALWAYS FIRST in the answer)

Every zsxq-company answer **opens** with the sell-side price-target history,
before the per-report stance cards. Three parts, in this order:

**(a) PT table** — one row per (broker, report date), oldest first:

| Date | Broker | Rating | PT | Change | Valuation basis | file_id |
|---|---|---|---|---|---|---|

- `Change` = initiation / unchanged / ↑ X→Y / ↓ X→Y (with %), or "—" when the
  library holds no earlier note from that broker.
- `Valuation basis` = the method as the note states it (DCF + WACC, P/S ×
  year, SOTP legs, EV/EBITDA × year, probability weighting).
- Date = the `-YYMMDD` filename suffix (authoritative), not `create_time`.

How to collect it:

1. **Pre-pass** (read-only) over `db/stock_price_target.db` →
   `price_targets` where `company_ticker`/`company_name` match. Treat as a
   hint list only — rows can be mis-tagged, have `price_target` NULL, or
   compute `upside_pct` against the wrong currency (e.g. an HK$ TP vs the
   US$ ADS price). Never quote a DB number without confirming it in the PDF.
2. **Sweep every company-specific PDF in the queue for the PT**, not just the
   8-12 you deep-read — PT history needs all dates. Grep the first 2-3 pages
   (OCR them with `ocr_pdf.py --file-id <id> --pages 1-3` if the text layer is
   empty — many zsxq PDFs are image-only). Patterns that find the number and
   the *previous* number fast:
   - Morgan Stanley: `Price target US$`, and the **"What's Changed — From / To"**
     box (also gives bull/base/bear moves) + the "Reason for change" paragraph.
   - Goldman: `12m Price Target:` / `12M TP of HK$… (vs. previously at …)`.
   - HSBC: `TARGET PRICE` / `PREVIOUS TARGET`, "raise/cut TP to … (from …)".
   - UBS: `12m price target`, "We derive our PT of …".
   - Citi: `Target price US$` near the cover box, "Our TP of … is derived from".
   - JPM: `Price Target:` + `PT End Date`.
   - Generic: `target price|price target|TP |PT ` within ±200 chars.
3. Dedupe re-uploads (`… (1).pdf`, same broker + same date). Sector notes that
   merely list the name (e.g. "Buy Hesai/Pony/WeRide") are not PT points.
4. **Currency / share class**: when a broker covers a different listing (H-share
   vs ADS, A vs H), keep the native PT in the table and convert for the chart
   using the ADS ratio and spot FX. Validate the ratio with a broker that
   publishes both (e.g. HSBC "US$11.40 … HK$29.60 on the H-share"). Label the
   converted value as derived.

**(b) Timeline chart** — render with the helper (writes a PNG, no DB access):

```bash
/opt/anaconda3/bin/python3 .claude/skills/zsxq-company/scripts/pt_timeline.py \
  --spec <scratchpad>/pt_spec.json --out <scratchpad>/<Company>_<TICKER>_PT_timeline.png
```

The spec lists each broker's `points` (date, pt), `price_ticker` (yfinance
symbol in the same unit as the PTs, so the price line runs through today),
a required `source` footer naming the brokers + date range + price source +
any FX/ADS conversion, and `annotations` for each PT change (short "who
X→Y + one-line why"). See the docstring for the schema. Read the PNG back to
check for overlapping labels / clipped footer, adjust `dx`/`dy` or
`legend_loc`, then send it with `SendUserFile`. Write it to the scratchpad,
not `reports/`, unless the user asked to save.

**(c) Why the targets changed** — one short block per broker that moved,
quoting the note's own stated reason (estimate revisions and which years,
fleet/volume assumptions, WACC/multiple/target-year roll-over, FX, regulatory
or macro events) with file_id + page. Separate *mechanical* moves (roll-over
of valuation year, FX update) from *thesis* moves (estimate cuts, scenario
re-weights). Then one or two lines on the big picture: PT dispersion, PT vs
current price (latest yfinance close), and how stale the newest note is
relative to today. Close with gaps (brokers whose earlier PT is missing,
PDFs not downloaded, bad `stock_price_target.db` rows found).

Every number must string-match the PDF it is cited to; derived values (FX
conversions, % changes) are labelled as such.

### 4. Read each PDF

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

### 5. Classify each report's stance

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

### 6. Synthesize the debate map

After the per-report cards, summarize:

- Bull camp: the repeated arguments and which reports support them.
- Bear camp: the repeated arguments and which reports support them.
- Core disagreement: the assumptions that actually drive the spread between
  views, such as AI accelerator attach rate, custom silicon risk, gross margin,
  networking cycle timing, inventory digestion, or valuation multiple.
- Questions for the user: 3-5 debate prompts that would let the next exchange
  be sharper after the user reads selected PDFs.

Keep the answer useful for a human investor deciding what to read next.
Answer order is fixed: **(1) price-target table + timeline chart + why the
targets changed (Step 3)**, then the report-by-report stance cards, then the
synthesis.

