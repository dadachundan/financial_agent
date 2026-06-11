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
    --id <REPORT_ID> --header
```

Flags:
- `--id <int>` (looks up `local_path` + `form_type` from the DB)
- `--path <file>` `--form 10-K` (alternative: extract a specific file)
- `--max-section <N>` per-section cap (default 30,000 chars). Each
  Item 1 / 1A / 7 / MD&A is independently truncated at this size.
- `--deep` disable the per-section cap entirely. Use this when you
  need the full Item 1A for cross-year risk-factor evolution analysis,
  or the full MD&A for revenue/segment trend work. **Default
  recommendation: use `--deep` for multi-year analyses, default cap
  for single-quarter / last-4-quarter summaries.**
- `--header` prepend a one-line metadata header (recommended).

What gets extracted:

| Form | Sections returned |
|---|---|
| 10-K | Item 1 (Business) + Item 1A (Risk Factors) + **Item 7 (MD&A)** |
| 10-Q | Item 2 (MD&A) + Item 1A Part II (Risk Factors update) |
| 8-K  | Items 1.01, 2.01, 2.02, 8.01 (skips 5.02 / 7.01 noise) |

The extractor lives in `scripts/sec_text.py` (skill-local) and imports
only the HTML-cleaning + section-regex primitives from
`ingest.sec_extract`. The assembly (which items, how much) is owned
by the skill — that's why this skill returns Item 7 even though
the shared extractor's default section set skips it.

**When reading Item 7 (MD&A), specifically capture the "Outlook" / "Trends" /
"Factors affecting future results" subsection** — it carries the filing's
forward-looking language and is the raw material for step 3b's guidance deltas.
8-K Item 2.02 exhibits, when present, often carry the most explicit guidance.

**Performance:** read filings sequentially, not all at once. For a
10×10-K run, that's ~10 separate `extract_report.py` calls. You may
run them in parallel from a single tool-use block to save wall time.

### 3. Summarize, in this order

**Open with a Thesis / What changed box (3–5 sentences) BEFORE any per-filing block.** Every sell-side note opens with a synthesized "so-what" stance, not raw per-period bullets — mirror the **GS results-review opener** and **Citi "China Internet Wrap & Outlook"**: state the single most important multi-year shift, its direction (improving / deteriorating / mixed), and the 2–3 deltas that drive it. Keep it filing-sourced only (no external news, per the guardrail below) and attach an inline SEC EDGAR citation to the filing that evidences the headline shift. See [references/house_style.md](references/house_style.md) for the durable patterns.

```markdown
> **Thesis (FY20→FY25): mix-shift improving, margin trajectory mixed.** Services crossed from 18% → 26% of revenue (first time >¼) as hardware unit growth flattened ([FY25 10-K](https://www.sec.gov/...)). Buyback cadence held but the new authorization stepped down. Item 1A added a net-new AI-regulation risk category in FY24. The thesis-relevant read is X.
```

For each filing (newest first), write a short block. The header **must** include a clickable SEC EDGAR link so the reader can verify against the canonical filing:

```markdown
### FY2025 10-K — [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<TICKER>&type=10-K&dateb=&owner=include&count=40) (filed 2025-10-31, period 2025-09-27, [local file](file:///<local_path>))
- **Business**: <2–3 sentence what-they-do snapshot, calling out new segments,
  product lines, or geographic shifts introduced this year.>
- **Key risks**: <3–5 of the most consequential / distinctive risk factors —
  skip generic ones like "general economic conditions" unless newly emphasized.
  **Diff Item 1A against the prior 10-K and tag each material change
  `ADDED` / `DROPPED` / `ESCALATED`, naming the category** (cyber, AI / AI-regulation,
  tariffs, climate, supply concentration, litigation status). Call out any
  NET-NEW risk category by name and the year it first appeared.>
- **New this year**: <bullets only if something genuinely changed vs the prior
  filing — new disclosures, restructurings, segment renames, new litigation,
  AI/regulatory language, etc.>
```

URL construction: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<TICKER>&type=<FORM>` returns the EDGAR listing of that form for that ticker (the user can sort by date to find the specific filing). The `local_path` and `accession_no` come from `list_reports.py`'s JSON output. If you cite a specific passage in prose (e.g. "the Item 1A risk factor on AI regulation"), repeat the SEC EDGAR link inline so the user can pivot to the source.

### 3b. Track forward guidance & capital-return deltas

A backward results recap without the forward half is only half the deliverable — mirror the **UBS "AGM takeaways: 2030 strategy & 2026 outlook"** and **Citi "Wrap & Outlook"** framing. From each filing, extract and track `OLD → NEW`:

- **Forward guidance / multi-year targets** — pull "Outlook" / "Trends" / "Factors affecting future results" language from the **Item 7 MD&A** (10-Ks carry less explicit guidance than earnings calls, so mine these subsections), and from **8-K Item 2.02** earnings exhibits when present.
- **Capital-return policy** — buyback authorization size, dividend, payout ratio — tracked as a delta (e.g. `payout target 65% → >70%`).
- **Capex / investment outlook** — direction and magnitude, with the stated driver.

Frame the trajectory the way UBS pits a 2030 target against current-year guidance — a point estimate alone misses the trend.

Then a final **Changes over the years** section. **Rank by thesis-impact: lead with the 2–3 changes that move the multi-year thesis** (a segment crossing a mix threshold, a net-new risk category, a capital-return policy shift) and explicitly de-prioritize boilerplate — the GS notes spend their words on the 2–3 things that matter. **Surface threshold-crossings first** as the headline signal, borrowing the **Nomura BIDU "AI revenue 52% of core, first time >half"** and **GS NC-results "first decline in six years"** framing — these inflection points are the most decision-useful read of a multi-year filing.

**Every change bullet must pair the MAGNITUDE with the ATTRIBUTED DRIVER in one clause.** A bullet that states a direction without a number is incomplete unless the filing genuinely gives no number. Mirror the **GS NC-results** clause form — magnitude *and* cause, never one without the other:

- ✅ "Auto segment revenue **−4% YoY in FY27, first decline in six years**, as OEMs cut IT capex ([FY27 10-K](https://www.sec.gov/...))."
- ✅ "Services crossed **18% → 26% of revenue (first time >¼) over FY20–FY25**, driven by subscription attach ([FY25 10-K](https://www.sec.gov/...))."
- ❌ "The auto segment declined and services grew." (no magnitude, no driver, no baseline)

Examples of what to look for (each as a magnitude+driver bullet):
- Segment reporting changes (new segments added, others merged)
- Geographic mix shifts (e.g. China revenue going from highlight to risk)
- Risk-factor evolution (new categories appearing — cyber, AI, climate, tariffs)
- Product-line transitions, sunset products
- Capital allocation language (buybacks, dividends, M&A appetite)
- Headcount / employee disclosures
- Litigation or regulatory matters that appear, persist, or resolve

## Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — the company's product or manufacturing process behind the filings, an unfamiliar business model or market-structure concept, or any point where the YoY narrative turns on a technical change a reader can't visualize from the 10-K text alone — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: [.claude/skills/company-research/references/citations.md](../company-research/references/citations.md) § "Further viewing — explainer videos" (this skill's own `references/` holds only `house_style.md`).

## Output format

A single Markdown document. Put the per-report blocks newest → oldest,
then the "Changes over the years" section at the end. Title it
`# <Company Name> (<TICKER>) — SEC filings summary, <oldest year>–<newest year>`.

**Always write the summary to** `reports/earnings/<TICKER>_<YYYYMMDD>.md`
(relative to the project root — `/Users/x/projects/financial_agent/reports/earnings/`).
Create the `reports/earnings/` directory if it doesn't exist. After writing the file,
print its path in chat and inline the report content for the user to read.

### Mandatory blocks — a report missing any of these without justification is not done

1. **Thesis / What-changed box** (3–5 sentences, before any per-filing block).
2. **Cross-year segment delta table** (spec below).
3. **Per-filing blocks** newest → oldest, each with a clickable SEC EDGAR link and `ADDED` / `DROPPED` / `ESCALATED` risk-factor tags.
4. **Section-3b guidance & capital-return delta block** (`OLD → NEW` for guidance, buyback/dividend, capex) — or an explicit one-liner `n/a: no guidance / capital-return / capex outlook disclosed in the filings reviewed` when genuinely absent. **Silent omission is a defect** (the RKLB 2026-06-09 run shipped without it).
5. **Changes over the years** section, ranked by thesis impact.
6. **2–4 Mermaid diagrams** (spec below).
7. **Further viewing** block — or an explicit omission justification (purely numeric report).
8. **Folded verification log** — `<details><summary>Verification log — YYYY-MM-DD</summary>` appendix recording the 3–5 delta spot-checks the numerical-traceability guardrail already requires, each as `"X = N from <filing>": ✓ string-matches / ✗ fixed`.

### Update-in-place rule — at most one SEC summary per ticker

Reports under `reports/earnings/` are tracked in git and meant to be living documents. **Before writing, check whether a summary for this ticker already exists** and update it in place rather than creating a parallel dated copy.

```bash
ls reports/earnings/ 2>/dev/null | grep -Ei "^<TICKER>(_[0-9]+)?\.md$"
```

(The `(_[0-9]+)?` matters: legacy outputs like `QCOM.md` have no date suffix — a date-only regex returns zero matches and would create exactly the parallel copy this rule forbids.)

- **Exactly one match** → overwrite it at the same path. Keep the existing filename even if its embedded date is stale or missing — git history records the actual revision date; do not rename `QCOM.md` to `QCOM_<date>.md`. Update the document's title-line date range and any "as of" header to today. **Before overwriting, read the file's first ~5 lines and confirm it is a sec-report-summary output** (title/header says "SEC filings summary" or "via the sec-report-summary skill"); if the matched file is a different report type sharing the namespace, do NOT overwrite — write the digest as `<TICKER>_SEC_<YYYYMMDD>.md` and tell the user about the collision.
- **Multiple matches** (legacy state) → update the most recent by filename date, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new file using today's `YYYYMMDD`.

To view rendered (with charts): the user's running viewer at
`http://xs-macbook-air.local:5001/reports/` renders Markdown with
Mermaid + GitHub styling. (The scripts' internal `API_BASE` probe stays
`localhost` — it's a machine-local fallback — but any URL surfaced to
the user uses the `.local` hostname per the project rule.)

### Always include a cross-year segment delta table

A compact structured delta table is the spine institutional notes render *before* the prose — mirror the **GS "results read-across"** segment block. Render it in Markdown (the source-of-truth), with the Mermaid charts hanging off it for visualization. Rows = reportable segments; columns = latest-FY revenue, prior-FY revenue, YoY %, and a one-line driver:

| Segment | FY25 rev | FY24 rev | YoY % | Driver |
|---|---|---|---|---|
| Services | $96.2bn | $85.2bn | +13% | subscription attach, App Store |
| iPhone | $201.2bn | $200.6bn | +0.3% | unit growth flat, ASP up ([FY25 10-K](https://www.sec.gov/...)) |

Any chart derived from this table must carry the data-source footer annotation per the project chart rule (e.g. "Source: AAPL FY25 10-K, Item 8 segment note").

### Always include Mermaid diagrams

Plain prose summaries are hard to skim. Each report must include 2-4
Mermaid diagrams that make the numbers visual. Pick the ones that fit
the data you actually have:

- **Quarterly revenue / net income trend** — single bar series for
  revenue + line series for net income on one `xychart-beta`. (Mermaid
  *does* support one bar + one line in the same xychart, but does
  **NOT** support multiple bar series — the last `bar` line wins.)
- **Segment mix pie** — `pie showData title <Title>` (no quotes around
  the title; pie syntax treats quotes as literal text).
- **YoY growth bar chart** — single bar series of YoY % per segment.
  Better than a side-by-side comparison because xychart-beta only
  renders one series.
- **Strategic/tax event timeline** — Mermaid `timeline` with one entry
  per quarter (or year), `:` separators between events within a quarter.

Mermaid syntax cheats that bite:
- `pie title …` — bare title, no quotes (else they show literally).
- `xychart-beta` — only one data series renders; collapse multi-period
  comparisons into a single derived series (e.g. YoY %).
- `timeline` — colons inside event text need escaping or rephrasing.

Aim for charts that *summarize* a section, not duplicate the table just
above. The RKLB report at `reports/earnings/RKLB_20260609.md` is a working
reference for the Mermaid usage if you need an example (note it predates
the Section-3b / verification-log mandatory blocks — don't copy those
omissions).

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
- **Numerical traceability** (reinforces the project Numerical-Accuracy rule):
  every YoY / QoQ delta in a per-filing block or the Changes section must trace
  to the **specific filing it is attributed to** — the filing whose SEC EDGAR
  link sits in that block — where the number string-matches the extracted text,
  *or* be labeled as a cross-year calc with both inputs sourced (e.g.
  `26% = 96.2 / 370 (both FY25 10-K)`). **Spot-check 3–5 deltas against the
  extracted filing text before writing the file.** Cross-link:
  [.claude/skills/company-research/references/citations.md](../company-research/references/citations.md).
- **Language default: English.** This skill digests US SEC filings, so it
  defaults to English headers / EDGAR links and does NOT inherit
  company-research's Chinese default. Produce Chinese only on explicit request.
