---
name: zsxq-analyze
description: Analyze a PDF stored in db/zsxq.db (the zsxq report library) and answer the user's question about it. Use whenever the user references a zsxq PDF by file_id, filename, or topic keyword — e.g. "what stocks does file_id 184124282514242 recommend?", "summarize the Deloitte report from zsxq", "/zsxq-analyze what does <name> say about robotics". **Also persists any sell-side price-target (PT) calls found in the deep PDF read into `db/stock_price_target.db`** (with `--replace` semantics so the full-text extraction overwrites any prior summary-only row from `/zsxq-recommend`), surfaced in the `/pt` viewer. Pair: `/zsxq-recommend` finds candidate file_ids to feed into this skill.
---

# Analyze zsxq PDF

Given a question that references a PDF in the zsxq library
(`db/zsxq.db`, table `pdf_files`), locate the file, extract its text,
and answer the question in-context. **You — Claude — do the analysis
in-context.** The scripts only look up rows and extract text; do not
call any external LLM (no MiniMax, no API).

**Interpreter:** run all project scripts with `/opt/anaconda3/bin/python3`
(per `feedback_anaconda_python_db_scripts` — bare `python3` has failed
read-only DB opens and lacks deps like `yfinance` in some shells).

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
user_rating, local_exists, pdf_path, pdf_url}, ...]}`. Rows sort by
`create_time DESC`. **`pdf_url` is the ready-to-paste direct-download
citation URL** (`http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>`)
— paste it verbatim; never hand-build the `/zsxq/pdf-viewer/<id>` HTML
viewer URL (won't download on iPad) or the dead `/zsxq-pdf/<id>` route.

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

When the answer will be saved to a file or quoted into any `reports/`
markdown, cite specific claims with the
[zsxq citation convention](../zsxq-ideas/SKILL.md#zsxq-citation-convention):
`[<Bank> — <topic>, zsxq #<file_id> p.<N>](<pdf_url>#page=<N>)`, using
the `pdf_url` from step 2 verbatim.

When the user asked for stocks / tickers specifically:

- Prefer the explicit list in the PDF.
- Cross-check against the `tickers` column already stored on the row
  (when present, it's been pre-tagged) and reconcile any mismatch.

### 4b. 延伸观看 / Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — the specific product or technology the analyzed PDF discusses (e.g. a humanoid robot's actuators / harmonic reducers / ball-screws / force sensors, a chip-packaging or lithography step, a battery cell's internals, a surgical-robot end-effector), a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**延伸观看 / Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept. English-only reports use `**Further viewing**`.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(B站，部分地区或需登录)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### 5. Persist any PT calls (free side-effect)

The deep read in step 3 has just given you full PDF text (and possibly
OCR / visual reads of bank-style cover slides where PTs are most
visible). This is a **higher-fidelity extraction** than the
summary-only path used by `/zsxq-recommend` — page 1 / "ratings & PT"
boxes / quote tables are visible here that the curator's 翻译精华
typically only partially captures.

Whenever the PDF contains explicit broker calls — page-1 "Reiterate
Buy / TP $1,159" boxes, ratings tables, "我们维持X的Y评级，目标价Z元"
phrasings inside the body, etc. — extract one record per
(ticker × broker) pair and pipe to the **shared helper with
`--replace`** so any prior summary-only row from `/zsxq-recommend`
gets overwritten by this better data:

```bash
python3 scripts/persist_pts.py --replace <<'JSON'
[
  {"ticker":"COST","company_name":"Costco",
   "broker":"Goldman Sachs","rating":"Buy","pt":1159,"ccy":"USD",
   "catalyst":"CFO meeting — proactive cuts, 4000 SKUs, AI search",
   "file_id":212485484288281}
]
JSON
```

**Full schema, rating/currency vocabulary, what to emit vs skip, and
idempotency rules are documented in
[`reference/pt_extraction.md`](../../../reference/pt_extraction.md).**

Analyze-specific notes (the bits beyond the shared doc):

- **Use `--replace`** — that's the whole point of doing this here.
  The deep-PDF read is the authoritative source; the summary-only
  row from `/zsxq-recommend` was a best-effort placeholder.
- **One report, one analyze invocation, one persist call** — emit a
  single JSON array with all the (ticker, broker) pairs you found in
  this PDF, not one persist call per pair.
- **The `file_id` is the same for every record** — it's the PDF you're
  analyzing.
- **Page-cited PTs are higher signal** — if you can see the PT in the
  rendered first page or on a "ratings table" page, that's worth
  emitting; PTs only mentioned in prose ("our target reflects our
  view that…") without a number are not.
- If the PDF has zero broker calls (a generic macro deck, a press
  release, a TAM whitepaper), skip step 5 entirely.
- **Show the report-date price next to every PT in your answer
  (mandatory).** A bare "GS Costco Buy, TP $1,159" tells the user
  nothing about the upside the analyst saw. When you report a PT in the
  deep-read answer, pair it with the stock's price *on the report's
  date* and the implied upside: `GS Costco Buy, TP $1,159 vs $1,030 @
  2026-05-28 → +12.5%`. The numbers come free in `persist_pts.py`'s
  stdout `rows` array (`report_date_price`, `price_currency`,
  `upside_pct`) — read them back and quote them. Never substitute
  today's spot for the report-date price; write `report-date price n/a`
  if it's null. See
  [`reference/pt_extraction.md`](../../../reference/pt_extraction.md)
  § "Surfacing rule".
- **Revision & dispersion context — the single-PDF case of the project's
  "Sell-side view evolution (卖方观点演变)" convention.** After persisting,
  SELECT prior rows for the same ticker(s) — STRICTLY read-only:
  `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`,
  table `price_targets` (columns `research_institute, rating, price_target,
  target_currency, report_date, report_file_id, upside_pct`) — and report:
  (a) the revision vs the SAME institute's prior call — `中金 PT 38→45,
  +18% vs 2026-03 call` (or "first call on record"); (b) where this PT sits
  vs other institutes' live PTs on the name — min / median / max + spread %.
  Report dates come from the filename's `-YYMMDD` suffix (authoritative;
  sanity-check against `create_time`); a 2026-03 and a 2026-06 PT from the
  same institute are two different views, not duplicates. Writes to this DB
  stay exclusively via `scripts/persist_pts.py`.

Surface the script's stdout `inserted` and `total_in_db` in the final
reply, e.g. `📈 PT inserts: 3 new (1 replaced), 148 total in /pt` — and
list each call with its report-date price + upside per the rule above,
plus the revision / dispersion context where prior rows exist.

### 5b. Upsert a card into `pdf_cards` (free side-effect, like the PT persist)

After any **full deep read** (full-text extraction of the PDF — not a
narrow `--pages` question that didn't give you the report's overall
thesis), write back one structured card via `zsxq_cards.py` (project
root) — the sanctioned Tier-2 helper for `pdf_cards` (schema owned by
`zsxq_common.init_db`; idempotent upsert by `file_id`):

```bash
python3 zsxq_cards.py <<'JSON'
[{"file_id": 184124282514242, "primary_ticker": "ISRG",
  "covered_tickers": ["ISRG","SYK","MDT"], "theme": "surgical-robotics",
  "thesis": "<1-paragraph what-this-report-argues>",
  "has_comparison_table": true,
  "key_tables": "p.5 segment×player TAM grid; p.11 procedure-volume by company",
  "key_figures": "p.4 da Vinci install-base CAGR",
  "rating": "<broker call if any>"}]
JSON
```

This is what makes `/zsxq-expert`'s `has_card` reuse work — `zsxq_fts.py`
flags carded PDFs so the expert system reuses your digest instead of
re-extracting the same PDF from scratch. Every deep read that skips this
step leaves the library no smarter.

### 5c. Set `claude_rating` from the deep read (MANDATORY)

A full deep read is the **most confident** read/skip verdict you can
give a PDF — record it as a 1-5 star `claude_rating` (this overrides any
lower-fidelity summary-only rating a prior `/zsxq-recommend` run wrote,
just like `persist_pts.py --replace` does for PT rows). Rate on how much
the report is actually worth reading, given what the full text turned
out to contain:

| Stars | Meaning |
|---|---|
| **5** | must-read — differentiated data / thesis, act on it |
| **4** | strong — worth reading |
| **3** | solid — worth reading if the topic is relevant |
| **2** | skippable — thin once you read it fully |
| **1** | noise — no signal / off-topic / stale |

So `3/4/5 = worth reading`, `1/2 = not worth reading`. Write through the
shared helper (the ONLY sanctioned write path for `claude_rating` — never
raw SQL, per CLAUDE.md DB safety):

```bash
python3 scripts/set_zsxq_ratings.py <<'JSON'
[{"file_id": 184124282514242, "rating": 5}]
JSON
```

The script prints `{considered, updated, missing, errored, rows}`;
mention the rating you set in the final reply.

## Primary-source-first & development-over-time rule (MANDATORY)

The user's standing preference for every report-producing skill: **reference the 10-K / 10-Q / original investor-relations materials as much as possible, cite them at page level, and present the material so the reader can see the company's development over time — what's new this period.**

1. **Source-preference order for any company fact.** (1) The company's own filings — 10-K / 10-Q / 8-K / DEF 14A / 20-F / 6-K / S-1 on EDGAR, or the non-US equivalent (年度报告 via cninfo, HKEX annual report, 有価証券報告書, 사업보고서); (2) original IR materials — earnings press release, earnings / investor-day deck, call transcript, shareholder letter; (3) third-party industry research; (4) news. **Business sections especially run on the 10-K.** For business fundamentals — what the company does, segment structure, products and how they make money, customers and concentration, competition, manufacturing / supply chain, IP, regulation, headcount — the 10-K is the default first-stop source (`Item 1 Business`, `Item 1A Risk Factors`, `Item 7 MD&A`, each cited with page), refreshed by the latest 10-Q for in-year changes; non-US equivalents use the annual report's business chapter (年度报告 经营情况讨论与分析, 有価証券報告書 事業の状況). Never cite a news rewrite for a fact that lives in a filing or an IR original — chase the original. Sell-side / zsxq broker notes are NOT displaced by this rule: they remain the separate `*Analyst view:*` layer (with their own page-level cites) and are never blended into the company-fact layer.

2. **10-K / 10-Q / annual-report citations must carry page numbers.** Format: `[NVDA FY2025 10-K, p. 42 — Segment results](https://www.sec.gov/...)`. When the EDGAR HTML doc makes the print page hard to pin down, give the Item + note/section heading instead (`Item 2 MD&A — Data Center revenue`, `Note 17 — Segment Information`) so the reader lands within one page-flip of the number. A bare `[10-K](url)` with no page/section locator fails the citation bar. The same locator discipline applies to prospectuses (page), IR decks (slide number), and non-US annual reports (第 N 页 / p. N).

3. **Present development over time — "what's new".** Do not render the company as a static snapshot. Wherever the output's structure allows, frame disclosures diachronically: trace the same line item across consecutive 10-Ks / 10-Qs (segment revenue & mix, risk factors added / dropped, customer-concentration %, capacity / capex, backlog, headcount, guidance language) and state explicitly what is NEW in the latest filing versus the prior one. Preferred presentations: an evolution table (`FY23 → FY24 → FY25`, each column cited to its own filing + page) and/or a short "What changed this period / 本期新变化" callout where the section covers a recurring disclosure.

4. **English originals stay English — even in Chinese-language reports.** When the original source is English (SEC filing, English IR deck / transcript / press release), cite and quote the English original directly; do not substitute a Chinese-media rewrite for language consistency. Symmetric with the existing original-language rule: the original's language always wins, whichever it is.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the subject of the output — the ticker, theme, sector, ETF holdings, deal, or any name that materially drives the analysis — sits in **AI** (foundation models, AI software/agents, AI infrastructure: datacenter compute, networking, power), **robotics** (humanoids, industrial automation, AMRs, actuators / reducers / sensors / end-effectors), or **semiconductors** (fabless, foundry, IDM, memory/HBM, equipment/WFE, materials, EDA/IP, advanced packaging), give those names a **detailed narrative treatment**, not summary bullets:

- **Write full narrative prose** for the sector-relevant sections — mechanism and causality ("X drives Y because Z"), not headline restating. Bullets may organize the prose but never replace it.
- **Cover the sector-specific dimensions that apply:**
  - *Technology position & roadmap* — process node / architecture / model-capability cadence vs named competitors (e.g., N2 vs 18A, HBM3E→HBM4, GB200→Rubin, Optimus gen-3 vs Figure 03).
  - *Supply-chain position* — key suppliers and customers up/down the chain, single-source chokepoints (TSMC/CoWoS, EUV, HBM), where pricing power sits, content-per-unit ($ per GPU / per robot / per vehicle).
  - *AI demand linkage* — the explicit path from AI capex to this name's P&L (orders → backlog → revenue recognition) with the actual disclosed numbers, never a generic "AI beneficiary" label.
  - *Robotics linkage* — design-win status, which platforms (Tesla Optimus, Figure, Unitree, domestic Chinese OEMs), volume and timeline realism vs the hype cycle.
  - *Cycle context* — where the semi / memory-pricing / AI-capex cycle stands right now and what that implies for forward estimates.
  - *Geopolitics & export controls* — US BIS rules, China localization, tariff exposure, entity-list status where relevant.
- **Quantify the narrative.** Each dimension covered should carry at least one sourced number (TAM, ASP, capacity, units, share). All figures obey the project's numerical-accuracy rule — every number traces to a URL or PDF page cited in the same paragraph.
- **Engage the sell-side view.** Where the zsxq library or other broker sources are in scope for this skill, the AI/robotics/semi narrative must engage the institute view (PTs, estimate revisions, cross-broker disagreement) rather than ignoring it.

This rule **deepens** the skill's existing output format — it never replaces or shortens the required structure. For subjects outside these sectors, the skill's baseline depth applies unchanged.

## Notes

- DB writes from this skill go through the sanctioned Tier-2 helpers
  only — `ocr_pdf.py` (OCR cache), `zsxq_cards.py` (cards),
  `scripts/persist_pts.py` (PTs), `scripts/set_zsxq_ratings.py`
  (`claude_rating`). Never raw SQL against any project DB.
- All scripts here resolve `db/zsxq.db` via `db_paths.db_path()` so
  `FINAGENT_DB_DIR` redirection works; any new script added under
  `scripts/` must do the same in the same commit (CLAUDE.md DB-safety
  rule).
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
- **Watermark gotcha:** if pages extract empty AND render blank in
  `render_pdf_pages.py` while the file size looks normal, suspect a
  per-recipient anti-piracy watermark applied as a PDF *incremental
  update*. Run `scripts/strip_pdf_watermark.py <input.pdf>` (writes
  `<input>.original.pdf` next to it), then re-extract from the stripped
  copy. Do not overwrite the original file. This is not an OCR problem —
  don't burn time on 3b/3c first.
- This skill answers questions about **one named PDF** per invocation
  (file_id / filename). Route everything else to the siblings: an
  in-depth question or comparison across the library → `/zsxq-expert`;
  a buy-list / idea scan → `/zsxq-ideas`; "what should I read" feed
  triage → `/zsxq-recommend`.
