---
name: compare-companies
description: Produce a 5,000–9,000 word head-to-head comparison of two public (or private) companies — focused on whether their products directly compete, who wins which moat dimension, how their customer bases overlap, and what advantage each holds over the other. Output saved as markdown to `reports/compare/<A>_vs_<B>.md`. Use when the user asks to "compare X and Y", "X vs Y", "head-to-head", "side-by-side", or "do these two compete" — e.g. "compare SNPS and CDNS", "AMD vs NVDA", "LRCX vs AMAT side-by-side".
---

# Compare Companies

Head-to-head deliverable: a 5,000–9,000 word markdown report that does NOT re-tell each company's story — it interrogates the **delta**. The report's job is to answer six specific questions the reader will have:

0. **In 60 seconds, what are each side's advantages and disadvantages?** (TL;DR table right after the title — see §0.)
1. **Do their products directly compete, or are they more complementary?** (Per-product overlap matrix — see §5.1.)
2. **What is each company's actual moat — quantified, not asserted?** (Seven-subsection moat anatomy — see §5.2–5.8.)
3. **Who are their customers, and where do those customer bases overlap?** (Customer concentration + named-win comparison — see §6.)
4. **What advantage does each have over the other?** (Dimension-by-dimension scorecard — see §7.)
5. **Which one should the reader bet on, and why?** (Synthesis — see §8.)

A comparison report that only restates each company's pitch is a failure. The reader has already read both companies' marketing material; they came to you for the delta.

**Discoverability discipline.** Most readers will scan the TL;DR + scorecard + bottom line and stop. The detailed sections (§1–§10) are evidence for the scannable layer — write them assuming the reader will skim. Tables beat paragraphs; numbers beat adjectives; explicit section cross-references (§5.5, §6) help a skimmer drill into the one section they care about.

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim — read its **Core principle** section before drafting. Summary of the comparison-specific failure modes:

- **Never invent a head-to-head fact.** "Synopsys has 60% interface IP share, Cadence has 25%" is checkable; if IPnest's actual number for Cadence is "not separately broken out", say so, not 25%.
- **Never invent a product-overlap claim.** "Synopsys VCS competes with Cadence Xcelium" is checkable (both are functional-verification simulators). "Synopsys VCS competes with Cadence Genus" is wrong (Genus is logic synthesis). Build the overlap matrix from each vendor's product pages — do not improvise.
- **Share-leadership claims need a third-party source.** "CDNS leads in PCB" needs an IPnest / Gartner / TechInsights cite, not a 10-K cite. The 10-K never says "we lead". Same rule as company-research §"do NOT misattribute sell-side opinions to filings".
- **When two sources disagree on a head-to-head number** (e.g. SemiAnalysis says one thing, an IPnest secondary citation says another), name both and prefer the primary / more-recent.
- **The analyst's own model is NOT a source.** Never write "(Source: our model)" or "(estimate, our analysis)" for a comparison fact.

## The six required deliverables

A compare-companies report MUST contain all six. Missing any one of them is a defect — the user has explicitly asked for each.

### Required deliverable 0 — TL;DR table at the top (§0)

**Placement: directly after the source-filings block, before the first `---` separator and before §1.** This is the first thing the reader sees, and for most readers it's the only thing they'll read end-to-end. Treat it as the headline of the report.

**Format: a 3-column markdown table with a row per company:**

```markdown
## TL;DR — At-a-glance advantages and disadvantages

|  | ✓ Advantages | ✗ Disadvantages |
|---|---|---|
| **Company A** | • <punchy bullet with number + §-ref> <br>• ... (5–8 bullets) | • <punchy bullet with number + §-ref> <br>• ... (5–8 bullets) |
| **Company B** | • ... (5–8 bullets) | • ... (5–8 bullets) |

**Who is each one for?** <one-paragraph distillation — pick A for X, pick B for Y, or run both because Z>. The detailed evidence for every TL;DR claim follows in §1–§10 below.
```

**Bullet discipline (applies to every cell):**

- **Lead with a number or specific noun, not an adjective.** "$13.5B debt locks buyback for ~2 years" beats "Heavy debt load". "Tensilica DSP IP leader: >1.5B HiFi DSPs/year, 160+ licensees" beats "Strong DSP IP".
- **Each bullet ends with a `(§N)` section reference** so a skimmer can drill straight into the evidence section (no anchor links needed — section numbers are enough).
- **5–8 bullets per cell.** Fewer than 5 means under-explored; more than 8 means you're padding.
- **Symmetric honesty.** Every Disadvantages cell must have at least as many bullets as its paired Advantages cell minus 2. If you found 7 advantages for A and only 1 disadvantage, you haven't looked hard enough — go back to §5.7 (Cracks worth naming).
- **No hedge words.** Banned: "arguably", "potentially", "may", "could", "is generally considered". If you can't commit, drop the bullet.
- **No analyst self-references.** No "(Source: our model)", "(estimate)", "(本模型)", etc. Every TL;DR claim must be supported by a citation in the corresponding §N body section — the TL;DR doesn't need its own citation but every fact must be cited *somewhere* in the report.

**Closing one-paragraph "Who is each one for?"** Three options framed sharply: pick A for ___, pick B for ___, or *both* (the dual-vendor reality for duopolies). Avoid both-sidesism ("both have merit") — the reader came for a recommendation framework, not equivocation.

See [`reports/compare/SNPS_vs_CDNS.md`](../../../reports/compare/SNPS_vs_CDNS.md) for the canonical worked example.

### Required deliverable 1 — Product overlap matrix (§5.1)

A three-column matrix mapping every meaningfully-shipping product on each side to one of three buckets:

| Product category | Company A's product | Company B's product | Status |
|---|---|---|---|
| Static-timing signoff | Synopsys PrimeTime | Cadence Tempus | **DIRECTLY COMPETE** |
| Custom analog layout | Synopsys Custom Compiler | Cadence Virtuoso | DIRECTLY COMPETE (CDNS dominant) |
| Multi-physics structural FEA | Ansys Mechanical | MSC Nastran (Hexagon D&E, in close) | DIRECTLY COMPETE |
| TCAD (process simulation) | Synopsys Sentaurus | — | NON-OVERLAPPING (SNPS only) |
| Enterprise PCB | Synopsys (light footprint) | Cadence Allegro X (deep) | COMPLEMENTARY (CDNS leads) |

See `references/product_overlap_matrix.md` for the full template, exhaustive examples, and how to source each row.

The matrix is the single most-cited section of the final report — readers paste it into competitive-positioning decks. Build it carefully and exhaustively. **Bury or generalize it, and the rest of the report becomes opinion.**

### Required deliverable 2 — Moat anatomy (§5.2–5.8)

Seven subsections, each anchored to specific disclosed numbers, not adjectives. Proven structure from the SNPS-vs-CDNS rewrite (May 2026):

1. **Customer concentration** — top-1 / top-5 / >10% disclosures from both 10-Ks; geographic mix table side-by-side; multi-year trend; **call out who is *more* exposed** and whether diversification is genuine or driven by losing a major customer.
2. **Backlog & recurring mix** — RPO / non-cancellable backlog $; backlog ÷ revenue ratio; duration ladder (<12mo / 13–36mo / >36mo); % recurring / ratable; typical contract length; multi-year trend.
3. **Channel / foundry / distribution lock-in** — for semis: per-foundry, per-node certification matrix. For consumer/SaaS: distribution partners, hyperscaler marketplace presence, OEM design-ins. For pharma: payer formulary coverage. For industrial: Tier-1 OEM relationships.
4. **Tool-level / sub-segment market share** — every published share number from a credible third-party source (Gartner, IDC, IPnest, IQVIA, IBISWorld, etc.) — never invented. Each row of the table is "segment → leader → estimated share → source".
5. **IP / patent / data-corpus franchise** — IP portfolio size, segment leadership claims (with third-party citations), proprietary data assets, patent fortress depth (expiry date span), exclusive licenses.
6. **Why a customer picks one over the other** — distilled decision framework (5–7 numbered drivers); concrete dual-vendor evidence at top-3 named customers; explicit quote from a third-party industry observer on customer behavior.
7. **Cracks worth naming** — the cracks each side's CEO would *not* highlight: shareholder lawsuits, executive departures, segment underperformance, regulatory overhangs, customer losses, churn signals.

See `references/moat_anatomy.md` for the per-subsection content spec, what to grep for in each filing type, and the failure modes to avoid.

### Required deliverable 3 — Customer comparison (§6)

Not just "do they have the same customers" — quantify and overlap:

- Top-1 / top-5 / >10% customer disclosures from both companies, side-by-side
- Geographic mix table
- Multi-year concentration trend (3 years if available)
- **Named-win comparison** — which named customers each side has disclosed in the last 12 months
- **Overlap analysis** — for the top 5–10 customers visible at either side, which use both vendors and which are single-vendor (cite a third-party source for any single-vendor claim; do not assume)
- Hyperscaler ASIC insourcing / customer-becoming-competitor watchlist if relevant to either side
- Channel partners (resellers, system integrators, distributors) if material

### Required deliverable 4 — Dimension-by-dimension scorecard (§7)

A flat 3-column markdown table with 15–25 rows: **Dimension | Edge | Why**. Each row must:

- Name a specific dimension (Top-line scale, Operating margin, Backlog visibility, Foundry coverage, Interface IP share, Custom-analog leader, …)
- Pick one side or "Tied" or "Neither" — no hedge words
- Justify in one short clause with a number where available

Cover at minimum: scale, growth quality, margin, recurring mix, backlog, customer diversification, key moat dimensions (1–4 product/IP segments), channel coverage, balance sheet, capital flexibility, legal/regulatory overhang, integration risk, AI narrative clarity.

### Required deliverable 5 — Bottom-line synthesis (§8)

Two paragraphs:

1. "Company A is betting that __ matters more than __" — one-paragraph distillation of A's strategic posture, with the specific downside scenario named.
2. "Company B is betting that __ matters more than __" — same shape, opposite framing.

Then one closing paragraph that names **what the reader should watch in the next 4–8 quarters** to know which bet is winning. Avoid both-sidesism ("both could win"); name the specific catalyst that will move the verdict.

## Report structure (TL;DR + 10 sections)

See `references/report_structure.md` for the full section-by-section spec, word-count targets, required tables and charts, and an example outline from SNPS_vs_CDNS.

Quick summary:

0. **TL;DR — At-a-glance advantages and disadvantages** (Required deliverable 0; 3-column table + "Who is each one for?" paragraph; ~250 words; placed before §1)
1. One-line self-description side-by-side
2. Strategic pillars side-by-side (timeline / pillar table)
3. AI narrative — tool vs. tailwind
4. Segment structure & financial scoreboard (revenue, margin, growth, segment mix)
5. **The moat anatomy** (7 subsections — Required deliverable 2; the longest section by word count)
6. The big bet (M&A, R&D, capital deployment — what each side is doing right now to expand TAM)
7. Capital allocation (debt, buyback, dividend, M&A optionality)
8. Distinctive risks (front-of-risk-factors comparison; what each 10-K leads with)
9. Side-by-side scorecard (Required deliverable 4)
10. Bottom line — two different bets (Required deliverable 5)
11. References block (every URL deduplicated, grouped: primary filings A / primary filings B / industry research / press / regulatory)

## Citations

Same standard as [[company-research]]. Read its `references/citations.md` before drafting — those rules apply verbatim. Summary:

- **Paragraph-level coverage.** Every substantive paragraph carries ≥1 inline markdown-link citation. Tables, captions, and TOC entries are exempt; nothing else is.
- **Deep URLs only.** Link to the specific SEC EDGAR document, the specific cninfo PDF, the specific Yole / Gartner / IPnest report page. Never a homepage.
- **Source-chain labels** when a third-party number appears in a primary filing — e.g. `[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/...)`.
- **Preserve original language in link titles** — Chinese filings stay `年度报告`, US filings stay `10-K`, Japanese stay `有価証券報告書`.
- **Freshness:** discard web sources older than ~12 months for industry data; include the publication date in the link title (`[Reuters, 2025-08-12](https://...)`).
- **Density target: ≥40 inline citations** across the body of a 5,000–9,000 word comparison.

## Prerequisites

This skill builds on [[company-research]]. **Before drafting any new content, always check the local `reports/company/` folder for prior research** — this is the most-asked question about this skill and the most common source of duplicated work if skipped.

```bash
# Step 1 — Resolve each side to a slug and check for existing research
ls "reports/company/" | grep -iE "(<Name_A>|<Ticker_A>)"
ls "reports/company/" | grep -iE "(<Name_B>|<Ticker_B>)"

# Step 2 — For each match, list what's inside the slug folder
ls "reports/company/<Slug_A>/" 2>/dev/null
ls "reports/company/<Slug_B>/" 2>/dev/null
```

The relevant files inside each slug folder, by language:

| Language | Filename pattern |
|---|---|
| English | `<Slug>_Research_Document.md` |
| Simplified Chinese | `<Slug>_公司研究.md` or `<Slug>_研究报告.md` |
| Bilingual | both of the above coexist; pick the language matching the comparison report's language |

**Decision rules after the ls:**

1. **Both research docs exist and are <12 months old** → read them in full; do NOT regenerate. The compare-companies report consumes them as structured input — Section 4 (Products), Section 5 (Customers), and Section 7 (Competitive Landscape) of each research doc become starting points for §5.1 (product matrix) and §6 (customer comparison) of the comparison.
2. **One side exists, the other is missing** → invoke [[company-research]] on the missing side first. Do not draft the comparison without both deep dives in hand; an uncited compare-companies report will fail the citation density target.
3. **Both exist but one or both are >12 months old** → invoke [[company-research]] on each stale side to refresh; the skill updates the existing file in place (no parallel copies).
4. **Neither exists** → run [[company-research]] on both sides first, then proceed. Expect this path to take significantly longer than path (1) — flag the user at the start so they can decide whether to wait or split the work over multiple sessions.

In all four paths, **also pull the latest 10-K / 年度报告 / Yuho for each side**, and the most recent 10-Q / 季度报告 / quarterly update — see `fetch_financial_report.py` (US) / `fetch_cninfo_report.py` (China A-share / HK). The comparison often needs raw numbers (RPO duration ladder, segment-by-region cuts, customer concentration footnotes) that the prior research doc summarized.

For US issuers, the skill also benefits from [[sec-report-summary]] output at `reports/earnings/<TICKER>_*.md` — it's a sub-step of company-research, so if research was run recently the SEC narrative is already on disk. For non-US issuers (China A-share / HK / Taiwan / Japan / Korea), build the multi-year evolution threads directly from domicile-portal filings.

**Verification before writing:** the first thing the analyst should report back to the user is the result of the existence check above — "Found research for A (<date>), missing for B, will run company-research on B first" — so the user can interject if they have a preference (skip stale-check, defer the missing side, etc.).

## Workflow

### Step 0 — Parse inputs and check existing research

User input forms accepted:
- `compare-companies SNPS CDNS`
- `compare SNPS and CDNS`
- `SNPS vs CDNS`
- `Synopsys vs Cadence` (then resolve to tickers)

For each side, resolve to a canonical `<Slug>` (matching the company-research slug convention: `<Name>_<EXCHANGE><CODE>` or `<Name>_<EXCHANGE>_<CODE>`). Preserve the user's left-right order — that becomes the file naming and the column ordering throughout the report.

Then check:
```bash
ls reports/company/<Slug_A>/ reports/company/<Slug_B>/ 2>/dev/null
```

- Both research docs present and <12 months old → proceed to Step 1.
- Either is missing → invoke [[company-research]] on the missing side, then proceed.
- Either is stale (>12 months) → invoke [[company-research]] to refresh (it auto-updates in place).

### Step 1 — Sync latest filings (always run)

Run the fetch script for each side per the company-research §"Step 0 — Sync filings" routing rules (US → `fetch_financial_report.py`; China A-share / HK → `fetch_cninfo_report.py`; Japan / Korea / Taiwan / etc. → domicile portal).

### Step 2 — Build the product overlap matrix (Required deliverable 1)

This is the highest-priority artifact and the section most likely to be fabricated. Discipline:

1. Open each vendor's product / solutions navigation tree on their corporate website (not just the IR site).
2. Enumerate every product family / SKU family / platform name with its one-sentence vendor-supplied description. Aim for 20–40 line items per side for a mid-size industrial / software company; fewer for a single-product startup.
3. Pair each row to its closest counterpart on the other side. If no clear counterpart exists, mark as **NON-OVERLAPPING (X only)**.
4. For each paired row, classify:
   - **DIRECTLY COMPETE** — both products solve the same customer problem at the same point in the customer's workflow, and customers actually treat them as substitutes.
   - **DIRECTLY COMPETE (X dominant)** — same as above, but one side has clear share leadership per a third-party source.
   - **COMPLEMENTARY** — both products exist in the category but one side has only a token / unmaintained offering; the other is the obvious choice; customers rarely RFP both.
   - **NON-OVERLAPPING** — one side does not meaningfully ship in this category.
5. Cite each vendor product page (deep URL) and, where a third-party share / leadership claim is made, cite the third-party source (Gartner / IPnest / IDC / TrendForce — specific report URL).

See `references/product_overlap_matrix.md` for the full template and SNPS-vs-CDNS worked example.

### Step 3 — Build the moat anatomy (Required deliverable 2)

Seven subsections per the spec in `references/moat_anatomy.md`. For each side, grep / search the latest 10-K / 年度报告 / Yuho for the specific keywords listed there (e.g. `"10%" "major customer"` for concentration; `"backlog" "remaining performance obligation" "non-cancellable"` for RPO; `"time-based" "ratable" "subscription"` for recurring mix).

Pull every published third-party share number that exists for the segment from IPnest / Gartner / IDC / IBISWorld / TrendForce / EvaluatePharma / etc. If a number is not publicly disclosed, write `not disclosed` — do not invent.

The moat section is the **longest section** by word count (typically 1,500–2,500 words for an industrial / software comparison). If the rest of the report is longer than the moat section, the priority is wrong.

### Step 4 — Customer comparison (Required deliverable 3)

Pull customer concentration from each filing per the regional rules in company-research §"Step 3 — Business model analysis". Build the side-by-side concentration table. Then pull named wins from each side's last 4 quarters of press releases + earnings transcripts; build the overlap commentary.

### Step 5 — Dimension-by-dimension scorecard (Required deliverable 4)

A flat 3-column table; 15–25 rows. Every row needs an "Edge" verdict (one side, "Tied", or "Neither") and a numeric or specific justification in the "Why" column. Hedge words like "arguably", "slightly", "potentially" are banned in the Edge column.

### Step 6 — Bottom-line synthesis (Required deliverable 5)

Two paragraphs per the spec above + the closing "what to watch" paragraph. Avoid both-sidesism — name the specific catalyst.

### Step 7 — Verification pass

Apply the same Step 10 verification flow from [[company-research]] — URL check, SEC filename resolution, 10-K claim spot-checks, executive-name verification, self-audit checklist. Append a `<details>` verification log at the end of the report.

**Compare-specific additional checks:**

- [ ] **TL;DR is present, placed before §1, and contains 5–8 bullets per cell.** Every bullet leads with a specific number/noun (not an adjective) and ends with a `(§N)` section reference. The Disadvantages column for each side has at least (Advantages count − 2) bullets — no whitewash.
- [ ] **TL;DR "Who is each one for?" paragraph** names three options sharply (pick A for X, pick B for Y, or both because Z) — no both-sidesism.
- [ ] **Prior research consulted before drafting.** Ran `ls reports/company/` for each side; if a doc existed, read it before writing anything new. Did not duplicate work.
- [ ] The product overlap matrix has at least one row in each of the four buckets (DIRECTLY COMPETE, DIRECTLY COMPETE w/ dominant, COMPLEMENTARY, NON-OVERLAPPING) — if all rows are "DIRECTLY COMPETE", you've under-explored the matrix.
- [ ] Every "share leader" claim in the moat anatomy has a third-party citation; none use a 10-K cite.
- [ ] The customer-comparison section names ≥3 customers visible at *both* sides (the dual-vendor reality), backed by either each vendor's customer-page listing or a third-party article.
- [ ] The scorecard has no row that says "depends" / "complex" / "mixed" — every row picks a side, "Tied", or "Neither".
- [ ] The bottom line names a concrete catalyst with a date or quarter, not "the next several years".
- [ ] Every TL;DR claim is supported by an inline citation somewhere in the body (the TL;DR cells themselves are exempt from per-bullet citations since they're a scannable summary, but the underlying fact must be cited in §N).

## Output location

Save to `reports/compare/<A>_vs_<B>.md` under the project root. Preserve the user's left-right ordering — do not alphabetize. The viewer (http://localhost:5001/reports) surfaces files under `reports/compare/`.

**Filename convention — no date suffix:**

- US tickers: `SNPS_vs_CDNS.md`, `LRCX_vs_AMAT.md`, `AMD_vs_NVDA.md`
- Mixed-domicile or non-US: include the exchange prefix when the bare ticker is ambiguous — `BYD_HKEX1211_vs_TSLA_NASDAQ.md`, `安培龙_SZSE002050_vs_汇川技术_SZSE300124.md`
- Multi-company batched comparison (3+): not supported by this skill — split into pairwise comparisons.

**Update-in-place rule** — at most one comparison file per ordered pair. If `<A>_vs_<B>.md` exists, update it in place. If `<B>_vs_<A>.md` exists with the same pair in the other order, ask the user which canonical order to keep before writing.

Filename language follows the report language per the company-research language rule. Comparisons of US companies → English. Comparisons of two China A-share companies → Simplified Chinese. Mixed (one US, one A-share) → ask the user; default to English with the Chinese company's name in original form on first mention.

## Reference docs (read on demand)

- `references/report_structure.md` — full 10-section template, word-count targets, required tables and charts, SNPS-vs-CDNS worked outline.
- `references/moat_anatomy.md` — the 7-subsection moat template with per-subsection content spec, grep keywords, and failure modes.
- `references/product_overlap_matrix.md` — how to build the directly-compete matrix, four-bucket classification rubric, sourcing rules, worked SNPS-vs-CDNS example.

Also read on demand from the parent skill:

- `.claude/skills/company-research/references/citations.md` — citation rules apply verbatim.
- `.claude/skills/company-research/references/quality_checklist.md` — pre-submit checklist (compare-companies adds its own checks above, but the company-research base list still applies).

## What this skill does NOT do

- It does **not** re-tell each company's story from scratch — the per-company deep dives live in [[company-research]] outputs. Reference them; don't duplicate them.
- It does **not** produce a recommendation in the trading sense (Buy/Hold/Sell with price targets) — that's [[trading-analysis]] and [[portfolio-decision]]. The bottom-line section identifies which bet is winning, not which stock to buy at today's price.
- It does **not** cover three or more companies in one file — split into pairwise comparisons. A 3-way compare loses the head-to-head sharpness that makes pairwise comparisons useful.
- It does **not** repeat content from the per-company research docs verbatim — if you find yourself copy-pasting from one of the source research docs, you're missing the comparison angle. Rewrite to highlight the delta.
