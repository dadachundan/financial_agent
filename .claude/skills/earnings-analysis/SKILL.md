---
name: earnings-analysis
description: Create professional equity research earnings update reports (8-12 pages, 3,000-5,000 words) analyzing quarterly results for companies already under coverage. Fast-turnaround format focusing on beat/miss analysis, key metrics, updated estimates, and revised thesis. Includes 1-3 summary tables and 8-12 charts. Use when user requests "earnings update", "quarterly update", "earnings analysis", "Q1/Q2/Q3/Q4 results", or post-earnings report.
---

# Equity Research Earnings Update

Create professional **EARNINGS UPDATE REPORTS** analyzing quarterly results for companies already under coverage, following institutional standards (JPMorgan, Goldman Sachs, Morgan Stanley format).

**Key Characteristics:**
- **Length**: 8-12 page equivalent
- **Word Count**: 3,000-5,000 words
- **Tables**: 1-3 summary tables (NOT comprehensive)
- **Figures**: 8-12 charts
- **Turnaround**: 1-2 days (within 24-48 hours of earnings)
- **Audience**: Clients already familiar with the company
- **Focus**: What's NEW - beat/miss, updated estimates, thesis impact
- **Format**: Markdown (default — see § "Output Specification"); DOCX only on explicit user request
- **Language**: bilingual by default — English report plus a Simplified Chinese companion at `..._zh.md` (the Chinese text keeps financial / technical terms in English alongside the gloss, e.g. `gross margin (毛利率)`, matching the company-research convention; the Further-viewing heading becomes `**Further viewing / 延伸观看**`). Produce a single language only when the user explicitly asks ("English only", "中文即可").

**Two format variants** (pick by turnaround need):
- **Deep update (default)** — the full-length (8-12 page equivalent) markdown report described above.
- **Note** — a fast-turnaround ~2-4 page numbered note matching how GS / JPM / MS actually ship same-day reviews: **boxed tables, bulleted segment lines, numbered top-level sections (1 Results · 2 Forward visibility · 3 Guidance · 4 Valuation · 5 Risks)**, Action Header on line 1. Same rigor (every number triangulated, every claim cited) — just tighter. Use for same-day reactions; the deep variant for the full estimate/thesis re-cut.

## When to Use

Use when the user requests:
- "Create an earnings update for [Company] Q3 2024"
- "Analyze [Company]'s quarterly results"
- "Post-earnings report for [Company]"
- "Q1/Q2/Q3/Q4 update for [Company]"

**Do NOT use if:**
- User requests "initiation report" → Use different skill
- Company is not already covered → Need initiation first

**User requests "flash note" / "quick take" / same-day reaction → use the **Note** variant of this skill** (2-4 pages, numbered sections, Action Header on line 1 — see Key Characteristics). It is this skill, not a different one.

**Matched-pair with earnings-preview.** This review is the back half of a JPM-style "As We Previewed → As [Co] Delivered" pair. If an `earnings-preview` note (or any prior estimate) exists for this quarter, **open the review by reconciling what was called vs what printed** (see references/workflow.md Step 3). Cross-link the preview in the Sources block.

## Guardrails (at-a-glance — the rules with the worst failure modes)

Compact index of the load-bearing don't-dos enforced throughout this skill.

- **Do not use earnings dates / numbers from training data.** Always search for the latest release and verify it's within 3 months of today. See Phase 1 "🚨 TRAINING DATA IS OUTDATED 🚨".
- **Do not write a beat/miss number without citing the consensus source by name + date.** "Beat consensus" is meaningless without "Bernstein FQ1-26 preview, 2026-02-02" or "Yahoo Finance analyst estimates, accessed YYYY-MM-DD". **Never write "Bloomberg/FactSet consensus" — no terminal exists in this project**; see § "Consensus & sell-side sources in this project".
- **Do not invent 10-Q line items.** Every metric in the report traces to a specific page of the 10-Q, the earnings release, or the call transcript. If the company doesn't break out a metric (e.g. segment-by-region revenue), say so explicitly.
- **Do not write a guidance change ("raised", "cut", "color-bearing reaffirmation") without citing both the old guide and the new guide.** Both must be linked to their respective primary sources, not paraphrased.
- **Do not let a forward estimate update be ungrounded.** Every Old → New estimate line in the report must name the specific result that drove the change ("Q3 services margin came in 280 bp ahead; raised FY services margin estimate by 50 bp"). **No estimate revision without a result-driven reason clause — "our model" / "our analysis" is never a valid reason** (CLAUDE.md "Numerical Accuracy"; the reason must name the specific result).
- **Do not bury the stock reaction.** A beat that sold off (or a miss that rallied) must be reconciled explicitly. See § "6. Reaction Reconciliation".
- **Do not omit URLs.** Every source in the Sources block is a clickable hyperlink (SEC EDGAR for filings, IR site for the earnings release/deck/transcript). Plain text references are a defect.
- **Do not skip the Data Used manifest** at the end of the report (Phase 4 output spec). The markdown report carries both the Sources block and the structured manifest so the data inventory is legible at a glance.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Critical Requirements

### 0. Action Header ⭐ (institutional first line)

**The report's very first line is a one-line Action Header** encoding all five elements, modeled on JPM's `Price (date) / Prior PT` header and the UBS/GS implied-upside convention:

1. **Rating action** (Maintain / Raise / Lower + the rating)
2. **Prior PT → New PT** (always show the move, even if unchanged → "Maintain $XXX")
3. **Implied upside %** vs a **dated current price** (e.g. "+48% vs HK$78.25 close 1-Jun-26")
4. **Valuation basis** (the multiple or method that produces the PT — "17.3x FY27E EPS", "30x normalized EPS", "SOTP")

> *Example:* **Maintain Buy; PT HK$112 → HK$116 (+48% vs HK$78.25 close 1-Jun-26); 17.3x FY27E EPS.**

Your own PT here is dated to *this* report, so the dated current close already satisfies the report-date-price rule for it. **But if you cite a *borrowed* PT — a consensus mean target or a named broker's PT from a dated note — pair *that* one with the price on *its* date + the upside it implied** (`consensus mean $130 vs $96 @ 2026-05-20 → +35%`), never just vs today's close; a borrowed PT with no report-date anchor isn't actionable.

The title line itself should also encode the verdict + driver + action ("Broad-based beat and raise — Reit OW, PT to $502"), not just "Q3 Earnings Update". See best-practices.md headlines.

### 1. Speed & Timeliness
- Publish within 24-48 hours of earnings release
- Focus on NEW information only
- Don't rehash company background extensively

### 2. Beat/Miss Analysis
- Lead with whether company beat or missed estimates
- Quantify variances (e.g., "Revenue beat by $120M or 3%")
- Explain WHY results differed from expectations

### 3. Summary Format
- Keep tables to 1-3 (summary only, not comprehensive)
- No full P&L/Cash Flow/Balance Sheet (just key metrics)
- Assume reader has seen initiation report

### 4. Citations & Source Attribution ⭐⭐⭐ MANDATORY

**CRITICAL**: Properly cite all data with SPECIFIC sources and CLICKABLE HYPERLINKS.

**Include specific citations WITH CLICKABLE LINKS in every figure and table:**

```
Source: Q3 2024 10-Q filed November 8, 2024; Company earnings release
        [Hyperlink "10-Q" to: https://www.sec.gov/cgi-bin/viewer?accession=...]
        [Hyperlink "earnings release" to: https://investor.company.com/news/q3-2024]
```

**HOW HYPERLINKS SHOULD APPEAR IN WORD:**
- Document names appear as blue, underlined clickable links
- Reader can Ctrl+Click to open source directly
- Not plain text URLs - formatted hyperlinks with display text

**REQUIRED SOURCES LIST:**

Cite in every earnings update:
- ✅ Earnings release (with date and URL)
- ✅ 10-Q filing (with filing date and EDGAR link)
- ✅ Earnings call transcript (with date)
- ✅ Investor presentation/supplemental materials (if available)
- ✅ Consensus estimates source — named + dated, from the project sources below (NOT "Bloomberg/FactSet": no terminal exists)
- ✅ Prior guidance (from previous quarter's materials)

**Consensus & sell-side sources in this project** ⭐ (the only citable Street numbers):

This project has no Bloomberg/FactSet terminal. **Never write "Bloomberg consensus" / "FactSet consensus" unless the figure traces to a reachable URL that literally contains it** (CLAUDE.md "Numerical Accuracy"). Source the Street in this order:

1. **Search the local broker library FIRST (`db/zsxq.db` — read-only, Tier 2).** Broker **preview + recap** notes for the quarter carry Street-by-segment numbers, the whisper, PT moves, and the reaction explanation that feeds § "6. Reaction Reconciliation" (e.g. Bernstein QCOM FQ1-26 recap: "$12.3B/$3.50 vs Street at $12.2B/$3.41", "FQ2 guided $10.6B vs Street $11.2B and us $10.9B"):
   ```bash
   cd /Users/x/projects/financial_agent
   /opt/anaconda3/bin/python3 zsxq_fts.py --query "<TICKER> recap" --limit 20
   /opt/anaconda3/bin/python3 zsxq_fts.py --query "<中文名> 业绩" --limit 20
   /opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "<TICKER>" --limit 40
   ```
   Read the matched preview/recap PDFs (OCR image-only pages via the `zsxq-analyze` `ocr_pdf.py` — ocrmac, never Tesseract). Cite them with the direct-download `pdf_url` that `find_pdf.py` prints (`http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>` — NEVER `/zsxq/pdf-viewer/<id>` or the dead `/zsxq-pdf/<id>`), **always labeled `*Analyst view:*` and never blended into a filing citation** (same convention as company-research).
2. **If zsxq has no coverage:** the Yahoo Finance analyst-estimates page for the ticker, or a named + dated press article that literally prints the consensus figure.

**REFERENCE SECTION WITH CLICKABLE HYPERLINKS:**

Include "Sources" section at end of report:

```
SOURCES & REFERENCES

Earnings Materials (Q3 2024):
• Earnings Release (November 7, 2024)
  [Hyperlink entire line to: https://investor.company.com/news/q3-2024-earnings]

• Form 10-Q (Filed November 8, 2024)
  [Hyperlink to: https://www.sec.gov/cgi-bin/viewer?accession=...]

• Earnings Call Transcript (November 7, 2024)
  [Hyperlink to: https://seekingalpha.com/article/...]

• Investor Presentation (November 7, 2024)
  [Hyperlink to: https://investor.company.com/presentations/q3-2024.pdf]
```

**VERIFICATION CHECKLIST:**
- [ ] Every figure has source with specific document and date
- [ ] Every table has source with document reference
- [ ] Beat/miss analysis cites consensus source with date
- [ ] Guidance changes cite current and prior guidance sources
- [ ] Key statistics have footnotes
- [ ] Sources section lists all materials with URLs
- [ ] ALL URLs are CLICKABLE HYPERLINKS (not plain text)
- [ ] All SEC filings hyperlinked to EDGAR viewer

**Project rules that also apply (markdown-output runs).** The hyperlink guidance above is DOCX-centric. When the output is markdown, the project-wide rules in [`CLAUDE.md`](../../../CLAUDE.md) and [.claude/skills/company-research/references/citations.md](../company-research/references/citations.md) govern — do not under-comply because this skill's examples are Word-shaped:
- **Paragraph-level inline citations with deep URLs** — link the specific EDGAR document / IR release / deck / transcript, never a homepage.
- **Every numerical beat/miss/guide figure string-matches a URL cited in the same paragraph** (CLAUDE.md "Numerical Accuracy"). A "+9% beat" must trace to a source that literally contains "9%".
- **Every chart carries an in-image `Source:` footer annotation** (CLAUDE.md chart rules), in addition to the figure caption.
- Defer to those files rather than restating them here, to avoid drift.

### 5. Updated Estimates
- Update forward estimates based on results
- Show old vs. new estimates clearly
- Explain what changed and why
- **Lead with the headline magnitude**: state the estimate revision as one line with direction + magnitude + a **result-driven reason clause** before the Old/New table (GS-style "FY27/28/29 EPS raised an avg +41% on stronger AI-server scale and pricing pass-through"). **The reason must name the specific result that drove it — never "our model".**

### 6. Reaction Reconciliation ⭐ (why the stock moved)

A required paragraph reconciling the **share-price reaction with the print** — the single most common real-world post-print question. Handle the counter-intuitive cases explicitly:

- **A beat that sold off** — guide below the buy-side whisper (Broadcom-style: in-line guide vs an elevated whisper), or a smaller-than-usual beat after a big run-up (CrowdStrike-style: beat shrank after a ~70% 6-week run). State the run-up, the whisper, and which one the tape was trading.
- **A miss that rallied** — bad print already discounted, or forward guide / backlog reset the narrative.

Name the dated move ("stock −7% next day on the FQ3 guide despite the FQ2 beat") and attribute it to the specific line the market keyed on. Do not leave the reaction unexplained.

## Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — the product, process, or end-market driving the beat/miss when the quarter turns on something mechanical or technical (a new node ramp, a new device, a process yield change), a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: [.claude/skills/company-research/references/citations.md](../company-research/references/citations.md) § "Further viewing — explainer videos".

## Learning from sell-side institutional research

A methodology review of post-results reviews from Goldman Sachs, Morgan Stanley, J.P. Morgan, UBS, Citi, Deutsche Bank, and Bernstein. These banks' notes share a verdict-first, triangulated, reconcile-to-PT discipline. Adopt the high-signal patterns below; the per-section mechanics live in the reference files.

- **Verdict-first, like a GS "F[n]Q review".** The title and first line state beat/miss + driver + rating/PT action together ("Broad-based beat and raise — Reit OW, PT to $502"). See § "0. Action Header" and best-practices.md.
- **Triangulate every headline number three ways — GS/Bernstein/DB house trait.** Each metric shows **vs YoY, vs the bank's own estimate, AND vs the guidance midpoint** in one place. The skill already compares to estimate + YoY; the third anchor (**vs guide midpoint**) is what these banks lead with — add it. Two reference columns (own est + Street), not one.
- **Estimate revision is a headline magnitude, then a boxed table — GS/JPM.** Lead with one line ("FY27/28/29 EPS raised avg +41% on AI-server scale + DRAM pass-through"), then a page-1 boxed **Key Changes** (Prev / Cur / %Chg per forward-year Adj EPS + Revenue). The reason clause must name the result, never "our model".
- **The forward guide is often the real story — GS Dell / DB Oracle.** Treat **next-quarter + full-year guidance as a co-equal block**, separate from the print block, each shown vs prior guide / vs Street / vs your model with a one-line achievability take. See report-structure.md "GUIDANCE vs PRIOR vs STREET".
- **Valuation visibly reconciles to the PT — UBS/Citi SOTP, MS single-multiple.** For multi-segment names, a SOTP build (segment EBIT × multiple → per-share lines summing to the headline PT); for single-line names, an explicit `multiple × out-year EPS` build (MS "28x FY27"). Don't just "mention DCF/comps". See report-structure.md PAGES 8-10.
- **Explain the stock reaction — especially a beat that sold off (Broadcom / CrowdStrike pattern).** See § "6. Reaction Reconciliation".
- **Decompose the beat — Bernstein UMC method.** Split the variance into **FX vs underlying** and **one-time / pull-forward vs sustainable** (Bernstein UMC: of ~3% beat, +1.2pt was FX; Hon Hai pull-forward vs real AI ramp). See workflow.md Step 5.
- **Lead with forward-visibility metrics the banks lead with.** **Backlog / bookings / order-book** (Dell $51.3B AI backlog, +$24B new orders), **per-unit economics by quarter** for platform/turnaround names (Meituan per-order Rmb; DiDi per-order EBITA margin), and a **path-to-normalized-profit bridge** (UBS Meituan FY28 normalized Rmb42bn = delivery 27 + IHT 22 − new −7). The current Key Operating Metrics table omits these. See report-structure.md PAGES 4-5.
- **Guidance-credibility framing — Marvell "conservative haircut", Oracle guide-vs-Street.** Beyond a checklist line: assess sandbag-vs-stretch against the company's track record, and for up-cycle raises name the **binding constraint (supply- vs demand-constrained — GS Dell "supply-constrained, not demand-constrained")**, a different bull case than a demand beat. See workflow.md Step 8 / Step 5.
- **Peer read-across with stated transmission logic — UBS Credo→BizLink, GS Broadcom→Toppan.** "Compare to peers" is not enough; carry one company's print into another's estimates and state the mechanism (AEC trend, substrate demand). See workflow.md Step 6.
- **Quantify competitive share where the call hinges on it — MS Broadcom ASIC ~80% long-run vs MediaTek+Google 15-20%; Marvell 60-65% in 1.6T DSP.** Replace qualitative thesis prose with a numbered share line + trajectory. See report-structure.md PAGES 6-7.
- **Ship a tight note when speed matters.** The analogs are ~2-4 page numbered notes, not 8-12 page essays. See the "Note" variant in Key Characteristics.

## High-Level Workflow

The earnings update process follows 5 phases:

### Phase 1: Data Collection (30-60 minutes)

**🚨🚨🚨 CRITICAL: TRAINING DATA IS OUTDATED 🚨🚨🚨**

**BEFORE STARTING - COMPLETE THESE 4 STEPS IN ORDER:**
1. **CHECK TODAY'S DATE** - Write down the current date
2. **SEARCH FOR LATEST** - Use web search: "[Company] latest earnings results"
3. **VERIFY THE DATE** - Confirm earnings release is within last 3 months
4. **CHECK TRANSCRIPT DATE** - Verify transcript date matches release date

**COMMON MISTAKE**: Using outdated earnings calls from training data instead of searching for the latest.

**REQUIREMENTS:**
- ✅ Search for latest earnings - do NOT rely on training data
- ✅ Write down today's date and the release date found
- ✅ Verify release date is within 3 months of today
- ✅ Verify transcript date matches release date
- ✅ If dates don't match or are old (>3 months), search again

**See [references/workflow.md](references/workflow.md)** for detailed search procedures and verification steps.

### Phase 2: Analysis (2-3 hours)
- Beat/miss analysis for each key metric
- Segment/geographic/product breakdown
- Margin and guidance analysis
- Update financial model and estimates

**See [references/workflow.md](references/workflow.md)** for detailed analysis framework.

### Phase 3: Chart Generation (1-2 hours)
Create 8-12 charts focusing on quarterly trends and what's new:
- Quarterly revenue progression
- Quarterly EPS progression
- Quarterly margin trends
- Revenue by segment/geography
- Key operating metrics
- Beat/miss summary
- Estimate revisions
- Valuation charts

**See [references/workflow.md](references/workflow.md)** for chart specifications.

### Phase 4: Report Creation (2-3 hours)
Write the markdown report (8-12 page equivalent) with specific structure; DOCX only on explicit user request.

**See [references/report-structure.md](references/report-structure.md)** for complete page-by-page templates and formatting requirements.

**High-level structure:**
- Page 1: Earnings summary with rating and price target
- Pages 2-3: Detailed results analysis
- Pages 4-5: Key metrics & guidance
- Pages 6-7: Updated investment thesis
- Pages 8-10: Valuation & estimates
- Pages 11-12: Appendix (optional)

### Phase 5: Quality Check & Delivery (30 minutes)
Verify content, formatting, accuracy, and timeliness before delivery.

**See [references/best-practices.md](references/best-practices.md)** for quality checklist and common mistakes to avoid.

**Then (mandatory, in order):**
1. **Append the in-report verification log** — `<details><summary>Verification log (Step 10) — YYYY-MM-DD</summary>` block per workflow.md Step 15 (the `<summary>` string is exact — project tooling greps for it; same contract as company-research).
2. **Commit without asking**: stage → commit (Conventional Commit, e.g. `feat(reports/earnings): QCOM FQ2-26 earnings update`; no Co-authored-by footer) → push to `main`.

## Primary-source-first & development-over-time rule (MANDATORY)

The user's standing preference for every report-producing skill: **reference the 10-K / 10-Q / original investor-relations materials as much as possible, cite them at page level, and present the material so the reader can see the company's development over time — what's new this period.**

1. **Source-preference order for any company fact.** (1) The company's own filings — 10-K / 10-Q / 8-K / DEF 14A / 20-F / 6-K / S-1 on EDGAR, or the non-US equivalent (年度报告 via cninfo, HKEX annual report, 有価証券報告書, 사업보고서); (2) original IR materials — earnings press release, earnings / investor-day deck, call transcript, shareholder letter; (3) third-party industry research; (4) news. Never cite a news rewrite for a fact that lives in a filing or an IR original — chase the original. Sell-side / zsxq broker notes are NOT displaced by this rule: they remain the separate `*Analyst view:*` layer (with their own page-level cites) and are never blended into the company-fact layer.

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

## Output Specification

**Primary Deliverable**: Markdown report (3,000-5,000 words ≈ 8-12 page equivalent)
**File Path**: `reports/earnings/<TICKER>_Q<N>FY<YY>_earnings_update_<YYYY-MM-DD>.md`
**Example**: `reports/earnings/QCOM_Q1FY26_earnings_update_2026-02-05.md`
**Chinese companion** (bilingual default): same path with `_zh.md` suffix.

- Ticker-first filename satisfies the project English-filename rule (CLAUDE.md "Research Report Filenames").
- The `_earnings_update_` suffix is load-bearing: `reports/earnings/` is shared with `sec-report-summary`'s `<TICKER>_<YYYYMMDD>.md` living filing summaries — **never collide with or overwrite those files**.
- Charts are matplotlib PNGs under `reports/charts/`, embedded by relative path (see workflow.md Step 12).
- **DOCX is opt-in only** — produce `[Company]_Q[Quarter]_[Year]_Earnings_Update.docx` only when the user explicitly asks for a Word document; the markdown file remains the canonical, committed copy.

**Contents:**
- Page 1: Summary with rating, price target, key takeaways
- Pages 2-3: Detailed results analysis
- Pages 4-5: Key metrics and guidance
- Pages 6-7: Updated thesis assessment
- Pages 8-10: Valuation and estimates
- Pages 11-12: Appendix (optional)
- 8-12 embedded charts
- 1-3 summary tables
- Complete sources section with clickable hyperlinks
- Verification log `<details>` block at the very end (see Phase 5)

**Optional Deliverable**: XLS model update (optional for earnings updates)

### Data Used / 数据来源清单 (mandatory at the end of every report)

A structured manifest of evidence categories + dates + freshness. Goes at the end of the report (DOCX appendix or markdown footer), separate from but complementing the existing "SOURCES & REFERENCES" hyperlinked block. Format:

```markdown
## Data Used / 数据来源清单

**Quarterly results (the quarter under analysis)**
- Q<N> FY<YY> earnings release (released YYYY-MM-DD); 10-Q filed YYYY-MM-DD; earnings call transcript YYYY-MM-DD; earnings deck YYYY-MM-DD; investor presentation if separate.

**Prior-period anchors (for QoQ / YoY comparison)**
- Q<N-1> FY<YY> release YYYY-MM-DD; Q<N> FY<YY-1> release YYYY-MM-DD; latest 10-K (FY filed YYYY-MM-DD).

**Consensus + guidance**
- Consensus snapshot (zsxq broker preview/recap note with file_id, or Yahoo Finance analyst estimates) as of YYYY-MM-DD (pre-release). Prior FY guide from Q<N-1> release / call (issued YYYY-MM-DD); new FY guide from Q<N> release / call (issued YYYY-MM-DD).

**Market data**
- Closing price YYYY-MM-DD (before release); next-day reaction YYYY-MM-DD. TTM multiples as of YYYY-MM-DD. Source: Yahoo Finance (yfinance).

**Cross-coverage context**
- Latest [reports/company/<Slug>/<filename>.md](../../../reports/company/<Slug>/<filename>.md) (last updated YYYY-MM-DD) — read as structured input for thesis-impact section, not cited inline.

**Stale notices / coverage gaps**
- <bulleted list — sell-side estimate not available, transcript not yet published, segment break-out withheld, or "none">.
```

Place this block immediately above the SOURCES & REFERENCES section. The manifest summarizes categories + freshness; SOURCES & REFERENCES lists every URL cited inline.

## Key Differences from Initiation Report

| Aspect | Earnings Update | Initiation Report |
|--------|----------------|-------------------|
| **Length** | 8-12 pages | 30-50 pages |
| **Words** | 3,000-5,000 | 10,000-15,000 |
| **Tables** | 1-3 summary | 12-20 comprehensive |
| **Figures** | 8-12 | 25-35 |
| **Turnaround** | 1-2 days | 3-6 weeks |
| **Scope** | Quarterly results | Complete company |
| **Focus** | What's NEW | Everything |
| **Company Background** | Brief mention | 6-10 pages |
| **XLS Model** | Optional | Required |

## Resources

### references/workflow.md
Detailed Phase 1-5 instructions with step-by-step procedures for data collection, analysis, chart generation, and report creation.

### references/report-structure.md
Complete page-by-page templates, table formats, and formatting requirements for the DOCX report.

### references/best-practices.md
Examples of good/bad headlines, tips for success, common mistakes to avoid, and comprehensive quality checklist.

## Dependencies

**Required:**
- Python (matplotlib, pandas, seaborn) for chart generation

**Optional:**
- DOCX skill (only when the user explicitly requests a Word copy)
- XLS skill for model updates (not required for earnings updates)
