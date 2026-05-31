---
name: compare-companies
description: Produce 5,000–15,000 word head-to-head comparisons of **2 to 4 public (or private) companies** in both English AND Chinese — focused on whether their products directly compete, who wins which moat dimension, how their customer bases overlap, and what advantage each holds over the others. Two separate markdown files are saved to `reports/compare/` — one in English (`<A>_vs_<B>.md` or `<A>_vs_<B>_vs_<C>.md`) and one in Simplified Chinese (`..._zh.md`). Use when the user asks to "compare X and Y", "X vs Y vs Z", "head-to-head", "side-by-side", or "do these N compete" — e.g. "compare SNPS and CDNS", "AMD vs NVDA", "Databricks vs Snowflake vs Oracle", "LRCX vs AMAT vs ASML side-by-side".
---

# Compare Companies

Head-to-head deliverable: a **5,000–15,000 word** markdown report that does NOT re-tell each company's story — it interrogates the **delta**. The report's job is to answer seven specific questions the reader will have.

**Supports 2 to 4 companies (N=2, 3, or 4).** The binary (N=2) case is the canonical reference — `reports/compare/SNPS_vs_CDNS.md`. For N=3 (three-way) and N=4 (four-way), the same skeleton scales: tables grow to N columns, the TL;DR table to N rows, the bottom-line section to N strategic-posture paragraphs. Word-count target scales by N: **5,000–9,000 words for N=2; 7,000–12,000 for N=3; 10,000–15,000 for N=4.** Beyond N=4 the head-to-head sharpness collapses entirely — split into pairwise reports or use `/sector-overview` instead.

Throughout this spec, "A vs B" is the canonical 2-way framing; whenever you see it, mentally generalize to "A vs B vs C (vs D)". Where N-way (3+) requires a structurally different table or phrasing, the spec calls it out explicitly with an "**N-way:**" tag.

0. **In 60 seconds, what are each side's advantages and disadvantages?** (TL;DR table right after the title — see §0.)
1. **Do their products directly compete, or are they more complementary?** (Per-product overlap matrix — see §5.1.)
2. **What is each company's actual moat — quantified, not asserted?** (Seven-subsection moat anatomy — see §5.2–5.7.)
3. **Who are their customers, and where do those customer bases overlap?** (Customer concentration + named-win comparison — see §6.)
4. **What advantage does each have over the others?** (Dimension-by-dimension scorecard — see §7. For N≥3, rows record per-pair edges or a 1st/2nd/3rd ranking.)
5. **Which one should the reader bet on, and why?** (Synthesis — see §8. For N≥3, N strategic-posture paragraphs.)
6. **Who else matters in this space?** (3–7 other big players surveyed alongside, with their position vs. the focal set quantified — see §5.8. For N=2 the focal "set" is the pair; for N=3 or 4, §5.8 covers companies *beyond* the focal N.)

A comparison report that only restates each company's pitch is a failure. The reader has already read both companies' marketing material; they came to you for the delta.

**Discoverability discipline.** Most readers will scan the TL;DR + scorecard + bottom line and stop. The detailed sections (§1–§10) are evidence for the scannable layer — write them assuming the reader will skim. Tables beat paragraphs; numbers beat adjectives; explicit section cross-references (§5.5, §6) help a skimmer drill into the one section they care about.

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim — read its **Core principle** section before drafting. Summary of the comparison-specific failure modes:

- **Never invent a head-to-head fact.** "Synopsys has 60% interface IP share, Cadence has 25%" is checkable; if IPnest's actual number for Cadence is "not separately broken out", say so, not 25%.
- **Never invent a product-overlap claim.** "Synopsys VCS competes with Cadence Xcelium" is checkable (both are functional-verification simulators). "Synopsys VCS competes with Cadence Genus" is wrong (Genus is logic synthesis). Build the overlap matrix from each vendor's product pages — do not improvise.
- **Share-leadership claims need a third-party source.** "CDNS leads in PCB" needs an IPnest / Gartner / TechInsights cite, not a 10-K cite. The 10-K never says "we lead". Same rule as company-research §"do NOT misattribute sell-side opinions to filings".
- **When two sources disagree on a head-to-head number** (e.g. SemiAnalysis says one thing, an IPnest secondary citation says another), name both and prefer the primary / more-recent.
- **The analyst's own model is NOT a source.** Never write "(Source: our model)" or "(estimate, our analysis)" for a comparison fact.

## Report language

**Default behavior: ALWAYS produce both English AND Simplified Chinese (zh-CN).** Never Traditional Chinese, Japanese, or Korean for the prose. Same rule as [[company-research]] — read its "Report language" section before drafting.

Each company pair gets **two separate, complete comparison reports** — one in English, one in Simplified Chinese. Both are produced in a single workflow run and saved to `reports/compare/`. Generate the English version first, then the Chinese version. Both files independently meet the 5,000–9,000 word target (Chinese counted in characters).

**Explicit user override (highest priority).** The user can request a single language only with any of these phrasings; honor it without asking:

| User says | Override to single language |
|---|---|
| `"... in English only"`, `"English report only"`, `"just English"`, `"--lang en"`, `"--en-only"` | English only (skip Chinese) |
| `"... in Chinese only"`, `"用中文即可"`, `"只要中文"`, `"--lang zh"`, `"--zh-only"` | Simplified Chinese only (skip English) |
| No override | **Both languages** (default — produce two separate report files) |

Examples:
- `compare SNPS and CDNS` → two files: `SNPS_vs_CDNS.md` + `SNPS_vs_CDNS_zh.md`
- `AMD vs NVDA` → two files: `AMD_vs_NVDA.md` + `AMD_vs_NVDA_zh.md`
- `compare SNPS and CDNS in English only` → English file only; skip Chinese
- `比亚迪 vs 蔚来 用中文即可` → Chinese file only; skip English
- `安培龙 vs 汇川技术` (no override) → two files: English + Chinese

**Bilingual mode (default) produces two complete, separate files**, not one interleaved document. Both files share the same underlying research — citations, charts, data, TL;DR claims, scorecard verdicts — but write the prose natively in each language; do not literal-translate one from the other. Each is a fully independent, high-quality report suitable for publication.

**Filename convention for the Chinese edition:** append `_zh` immediately before `.md`. Examples:
- `reports/compare/SNPS_vs_CDNS.md` (English) + `reports/compare/SNPS_vs_CDNS_zh.md` (Chinese)
- `reports/compare/LRCX_vs_AMAT.md` + `reports/compare/LRCX_vs_AMAT_zh.md`
- `reports/compare/安集科技_SSE688019_vs_鼎龙股份_SZSE300054.md` already in Chinese — when generating the English companion, name it `Anjizhike_SSE688019_vs_Dinglong_SZSE300054.md` per the English/pinyin-in-filename rule.

**Language-specific instructions when drafting:**

- **English report** — full prose per the structure in `references/report_structure.md`. Standard business English, accessible to global equity investors. Preserve original-language titles for non-English citations (e.g., `比亚迪 BYD 2024 年度报告`, `Sumitomo 統合報告書`). Bilingual technical terms in parentheses where helpful (`advanced packaging (先进封装)`), but bilingualism is optional in English prose — what matters is clarity for English readers. Section headers in English (TL;DR, Moat anatomy, Bottom line, etc.).
- **Chinese report** — full prose in Simplified Chinese (zh-CN). Write as if for Chinese investors. Use **bilingual technical terms** per [[company-research]]'s rule (English / Chinese gloss on first mention, e.g. `毛利率 (gross margin)`, `RPO (剩余履约义务)`, `Tier-1 供应商`). Section headers in Chinese (TL;DR — 优劣势速览, 护城河剖析, 底线判断, etc.). Bilingual terms are MANDATORY in Chinese, not optional. Keep ticker codes, acronyms, and product code-names in their original form: `SNPS`, `CDNS`, `H200`, `RMB`, `bp`, `YoY`.

A Chinese reader should find the Chinese report as natural and fluent as an English reader finds the English report. Neither version is the canonical "source"; they share data, not prose.

**Chinese names in English reports / English names in Chinese reports:** Chinese companies may appear in their original Chinese form alongside an English / pinyin gloss on first mention, e.g. `安培龙 (Anpeilong, SZSE:002050)`, `比亚迪 (BYD)`, `宁德时代 (CATL)`. After first mention, either form is fine. Symmetrically, US/EU company names appear in their native English form in the Chinese report alongside a Chinese gloss on first mention if a commonly-used translation exists (`Synopsys (新思科技)`, `NVIDIA (英伟达)`, `AMD (超威半导体)`).

## The seven required deliverables

A compare-companies report MUST contain all seven. Missing any one of them is a defect — the user has explicitly asked for each.

### Required deliverable 0 — TL;DR table at the top (§0)

**Placement: directly after the source-filings block, before the first `---` separator and before §1.** This is the first thing the reader sees, and for most readers it's the only thing they'll read end-to-end. Treat it as the headline of the report.

**Format: a 3-column markdown table with one row per company (N rows total for an N-way comparison):**

```markdown
## TL;DR — At-a-glance advantages and disadvantages

|  | ✓ Advantages | ✗ Disadvantages |
|---|---|---|
| **Company A** | • <punchy bullet with number + §-ref> <br>• ... (5–8 bullets) | • <punchy bullet with number + §-ref> <br>• ... (5–8 bullets) |
| **Company B** | • ... (5–8 bullets) | • ... (5–8 bullets) |
| **Company C** (N≥3 only) | • ... (5–8 bullets) | • ... (5–8 bullets) |
| **Company D** (N=4 only) | • ... (5–8 bullets) | • ... (5–8 bullets) |

**Who is each one for?** <one-paragraph distillation — for N=2 frame as "pick A for X, pick B for Y, or run both because Z"; for N=3+ frame as "pick A for X, pick B for Y, pick C for Z, or run a hybrid because W". Always name the role each one wins; avoid both-sidesism even with N companies.> The detailed evidence for every TL;DR claim follows in §1–§10 below.
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

An **(N+1)-column** matrix mapping every meaningfully-shipping product across all N sides to a status bucket. For N=2 the binary classification is enough (DIRECTLY COMPETE / DIRECTLY COMPETE w/ dominant / COMPLEMENTARY / NON-OVERLAPPING). **For N=3+, the Status column gains a row-pattern grammar** because direct-compete-ness varies by pair:

| Product category | A | B | C | Status |
|---|---|---|---|---|
| Cloud data warehouse | Databricks SQL | Snowflake | Oracle ADW + HeatWave | ALL THREE COMPETE (SNOW dominant — Gartner CDW MQ leader) |
| Lakehouse / open-format engine | Databricks Lakehouse | Snowflake Iceberg Tables | — | **A vs B compete; C absent** |
| Traditional RDBMS / OLTP | — | — | Oracle Database 23ai | NON-OVERLAPPING (ORCL only — incumbent OLTP) |
| AI / ML platform | Mosaic AI | Cortex | Oracle AI (OCI Gen AI) | ALL THREE COMPETE (A dominant for fine-tuning per Forrester Wave 2025) |
| Enterprise applications (ERP/HCM/CX) | — | — | Oracle Fusion Apps | NON-OVERLAPPING (ORCL only) |

**Status-cell grammar (use these phrasings verbatim — they're scannable):**

- `ALL THREE COMPETE` / `ALL FOUR COMPETE` — every side ships in the category.
- `ALL THREE COMPETE (X dominant)` — clear leader per a third-party source.
- `A vs B compete; C absent` / `A and C compete; B absent` — only some sides ship; spell out which by letter.
- `COMPLEMENTARY (X leads)` — multiple sides ship but only one is the real choice.
- `NON-OVERLAPPING (X only)` — exactly one side ships; the strategic asymmetry.

See `references/product_overlap_matrix.md` for the full template, exhaustive examples, and how to source each row.

The matrix is the single most-cited section of the final report — readers paste it into competitive-positioning decks. Build it carefully and exhaustively. **Bury or generalize it, and the rest of the report becomes opinion.**

### Required deliverable 2 — Moat anatomy (§5.2–5.8)

Seven subsections, each anchored to specific disclosed numbers, not adjectives. Proven structure from the SNPS-vs-CDNS rewrite (May 2026). **For N≥3, every subsection's tables grow to N columns; the analytical questions stay the same.** When a side doesn't disclose a number that others do, write `not disclosed` in that side's cell — don't estimate or omit the column.

1. **Customer concentration** — top-1 / top-5 / >10% disclosures from each 10-K (or 年度报告 / Yuho); geographic mix table side-by-side across all N companies; multi-year trend; **call out who is *most* exposed** (for N=3+, name the rank) and whether each side's diversification is genuine or driven by losing a major customer.
2. **Backlog & recurring mix** — RPO / non-cancellable backlog $; backlog ÷ revenue ratio; duration ladder (<12mo / 13–36mo / >36mo); % recurring / ratable; typical contract length; multi-year trend.
3. **Channel / foundry / distribution lock-in** — for semis: per-foundry, per-node certification matrix. For consumer/SaaS: distribution partners, hyperscaler marketplace presence, OEM design-ins. For pharma: payer formulary coverage. For industrial: Tier-1 OEM relationships.
4. **Tool-level / sub-segment market share** — every published share number from a credible third-party source (Gartner, IDC, IPnest, IQVIA, IBISWorld, etc.) — never invented. Each row of the table is "segment → leader → estimated share → source".
5. **IP / patent / data-corpus franchise** — IP portfolio size, segment leadership claims (with third-party citations), proprietary data assets, patent fortress depth (expiry date span), exclusive licenses.
6. **Why a customer picks one over the other** — distilled decision framework (5–7 numbered drivers); concrete dual-vendor evidence at top-3 named customers; explicit quote from a third-party industry observer on customer behavior.
7. **Cracks worth naming** — the cracks each side's CEO would *not* highlight: shareholder lawsuits, executive departures, segment underperformance, regulatory overhangs, customer losses, churn signals.

See `references/moat_anatomy.md` for the per-subsection content spec, what to grep for in each filing type, and the failure modes to avoid.

### Required deliverable 3 — Customer comparison (§6)

Not just "do they have the same customers" — quantify and overlap across all N sides:

- Top-1 / top-5 / >10% customer disclosures from each company, side-by-side (N columns)
- Geographic mix table (N columns)
- Multi-year concentration trend (3 years if available, per company)
- **Named-win comparison** — which named customers each side has disclosed in the last 12 months; for N≥3 use a 3-or-4-column table where each row is a customer and each cell is "named win at this side / not named / known not a customer".
- **Overlap analysis** — for the top 5–10 customers visible at any side, identify the **multi-vendor reality**: which customers use 2 of the N (and which pair), which use all N, and which are single-vendor (cite a third-party source for any single-vendor claim; do not assume). For N=3+ a small Venn or a "customer × vendor" grid is more legible than prose.
- Hyperscaler ASIC insourcing / customer-becoming-competitor watchlist if relevant to any side
- Channel partners (resellers, system integrators, distributors) if material

### Required deliverable 4 — Dimension-by-dimension scorecard (§7)

**N=2 (binary):** A flat 3-column markdown table — **Dimension | Edge | Why** — with 15–25 rows. Edge picks one side, "Tied", or "Neither". No hedge words.

**N=3 or N=4:** Switch to a flat (N+2)-column table: **Dimension | A | B | C [| D] | Why**. Each company cell holds either a **rank** (`1`, `2`, `3` with `=` for ties) **or** a checkmark grid (`✓` for winner, blank for not-winner). The "Why" column carries the one-clause justification with a number. Example for N=3:

| Dimension | DBX | SNOW | ORCL | Why |
|---|---|---|---|---|
| Operating margin (FY25) | 3 | 2 | **1** | ORCL 31% non-GAAP op-margin vs SNOW 9% vs DBX cash-flow positive but operating loss [10-K refs] |
| AI/ML platform breadth | **1** | 2 | 3 | DBX Mosaic AI = end-to-end fine-tuning; SNOW Cortex narrower; ORCL bundled with OCI infra |
| Open-format lock-out cost | **1** | 2 | 3 | DBX Delta+Iceberg = portable; SNOW now Iceberg-friendly but native is proprietary; ORCL native is most locked-in |

Cover at minimum: scale, growth quality, margin, recurring mix, backlog, customer diversification, the **3–5 key moat dimensions** for the industry (product/IP/distribution sub-segments), channel coverage, balance sheet, capital flexibility, legal/regulatory overhang, integration/M&A risk, AI narrative clarity. For N=3+, add 2–4 rows that surface **pair-specific** verdicts where a global rank obscures the picture (e.g. "DBX vs SNOW only — open-format lock-out", "ORCL vs hyperscalers — enterprise app moat"). Mark these rows by appending the pair name in the Dimension column. **Hedge words banned in every cell** — "arguably", "slightly", "depends" disqualify the row.

### Required deliverable 5 — Bottom-line synthesis (§8)

**N paragraphs (one per company)**, each shaped the same way:

1. "Company A is betting that __ matters more than __" — one-paragraph distillation of A's strategic posture, with the specific downside scenario named.
2. "Company B is betting that __ matters more than __" — same shape, different framing.
3. (N≥3) "Company C is betting that __ matters more than __" — same shape, third framing. For N-way the bets must be *distinct* — if A's and C's "bets" are paraphrases of each other, collapse them or rewrite so each side's bet is genuinely orthogonal.

Then one closing paragraph that names **what the reader should watch in the next 4–8 quarters** to know which bet is winning. For N≥3 this paragraph should explicitly name **which side wins under which observable condition** (e.g. "If hyperscaler customers continue pulling fine-tuning workloads onto open-format lakes, A wins; if enterprise IT continues consolidating into SQL-first cloud DW, B wins; if existing OLTP customers reject moving to a separate analytics stack, C wins."). Avoid both-sidesism ("all three could win"); name the specific catalysts that move each verdict.

### Required deliverable 6 — Other big players in the space (§5.8 + table columns)

A focal-N view of a multi-player industry is misleading by itself. Every report must identify **3–7 other meaningful players** in the focal set's competitive space (i.e. players *beyond* the N being compared) and surface them in two places: as additional columns in the moat-anatomy tables where they materially affect the picture, and as a dedicated subsection §5.8 with 100–300 words per Primary competitor.

**For N=2 the "other big players" are everyone outside the pair.** For N=3 or N=4 the bar is higher: the focal set already covers more of the industry, so the "other big players" are the *next-tier* relevant names — the hyperscalers in a Databricks-vs-Snowflake-vs-Oracle report, Siemens EDA in a 3-way EDA report, ASML/KLA/TEL in a 3-way semicap report. If the focal set already includes the obvious 3–4 leaders, §5.8 may shrink to 2–3 paragraphs covering specialists, regional alternatives, and adjacent-paradigm threats. Do not list the same company as both a focal-N member and a §5.8 entry.

**Discovery — three sources, in this order:**

1. **Each side's 10-K Item 1 / 年度报告 / Yuho competition section** — quote the named competitor list verbatim. This is the authoritative starting point.
2. **The relevant segment leaderboards** — IPnest for design IP, Gartner Magic Quadrant for enterprise software, IDC / IBISWorld for hardware, TrendForce for semis, IQVIA / EvaluatePharma for pharma, SemiAnalysis / SemiWiki for niche semi sub-segments.
3. **Recent industry-research notes** — last 12 months only — that name the full vendor universe.

**Classification — every other player resolves to one of four buckets:**

| Bucket | Definition | How to surface |
|---|---|---|
| **Primary competitor** | Overlaps directly on at least one moat dimension where A or B holds a franchise. Examples: Siemens EDA vs SNPS/CDNS in EDA; Arm vs SNPS in processor IP; TEL/KLA/ASML vs LRCX/AMAT in semicap. | Dedicated 200–300 word paragraph in §5.8 + column added to §5.3 / §5.4 / §5.5 tables wherever they meaningfully share share. |
| **Adjacent player** | Overlaps on a smaller segment or a different end-market. Examples: Keysight RF/microwave EDA; Schrödinger molecular simulation. | One-sentence mention in §5.8 only; no table columns. |
| **Acquisition target** | Has been or will be absorbed by A or B during or near the comparison's reporting period. Examples: Ansys (acquired by SNPS July 2025); Hexagon D&E (closing into CDNS Q1 2026). | Described as "now part of A" rather than as an independent player — note the close date and the post-close segment. |
| **Domestic-market alternative** | Regional vendors limited by export controls, talent depth, or PDK access. Examples: Empyrean, X-EPIC, Primarius in Chinese EDA; Tsinghua Unigroup in Chinese DRAM. | Call out as a §8 regional risk; no §5.8 paragraph. |

**Where each Primary competitor surfaces in the report:**

| Section | What to add |
|---|---|
| §0 TL;DR | One sentence in the "Who is each one for?" paragraph if a third party meaningfully changes the choice (e.g. "the third option is Siemens EDA for physical verification"). |
| §5.3 Foundry / channel / formulary matrix | Add a column for each Primary competitor that ships in the matrix — for EDA, Siemens always appears; for semicap, ASML, KLA, TEL all appear. Omitting these makes the matrix misleading. |
| §5.4 Tool-level share | Add a column for each Primary competitor that *leads* a sub-segment. E.g. Siemens Calibre at ~85% physical verification — without this column the table tells the reader the focal pair owns everything, which is wrong. |
| §5.5 IP / patent / data franchise share | Add the dominant non-focal-pair player. E.g. Arm at ~40% of Design IP — without this, the IP share table is misleading because it suggests SNPS-vs-CDNS is the whole market. |
| **§5.8 — The broader competitive landscape (NEW REQUIRED SUBSECTION inside the moat anatomy)** | 100–300 words per Primary competitor: what they do, where they overlap with A or B, their estimated share, structural position (leader / specialist / challenger), recent strategic moves (M&A, divestitures, leadership). |
| §9 Scorecard | Optional: 1–2 rows showing where the third party would beat *both* A and B (e.g. "Physical verification | Siemens (Calibre ~85%) — neither A nor B leads"). |

**Quantity rule:** at minimum 3 other players in §5.8, at maximum 7. Fewer than 3 means under-explored; more than 7 dilutes the focal pair's contrast.

**Failure modes:**

- Listing other players without explaining how they affect the A-vs-B choice → pointless context; remove or expand.
- Treating §5.8 as a separate report → keep each Primary competitor's treatment to 100–300 words.
- Inventing players not in any cited source → every named other player must come from a 10-K competitor list or a third-party industry source.
- Forgetting to extend the §5.3 / §5.4 / §5.5 tables → the §5.8 paragraphs alone are not enough; the tables must visually show that the focal pair operates inside a larger ecosystem.

## Report structure (TL;DR + 10 sections)

See `references/report_structure.md` for the full section-by-section spec, word-count targets, required tables and charts, and an example outline from SNPS_vs_CDNS.

Quick summary (every section's tables grow to N columns when N≥3):

0. **TL;DR — At-a-glance advantages and disadvantages** (Required deliverable 0; 3-column table with N rows + "Who is each one for?" paragraph; ~250 words for N=2, ~350 for N=3, ~450 for N=4; placed before §1)
1. One-line self-description side-by-side (N-column table — verbatim 10-K Item 1 / 年度报告 framing)
2. Strategic pillars side-by-side (timeline or pillar table; N tracks)
3. AI narrative — tool vs. tailwind (N-column table)
4. Segment structure & financial scoreboard (N-column scoreboard; mermaid xychart bar chart with N grouped bars per metric)
5. **The moat anatomy** (8 subsections — Required deliverables 2 + 6; the longest section by word count). Subsections: 5.1 customer concentration · 5.2 backlog & recurring mix · 5.3 channel/foundry/distribution lock-in · 5.4 tool-level segment share · 5.5 IP/patent/data franchise share · 5.6 why a customer picks one over the other · 5.7 cracks worth naming · **5.8 other big players in this space** (players *beyond* the focal N)
6. The big bet (M&A, R&D, capital deployment — what each side is doing right now to expand TAM; N-column table)
7. Capital allocation (debt, buyback, dividend, M&A optionality; N-column table)
8. Distinctive risks (front-of-risk-factors comparison; what each 10-K leads with; N-column table)
9. Side-by-side scorecard (Required deliverable 4) — for N=2 a 3-col Edge table; for N≥3 a (N+2)-col rank-or-checkmark table
10. Bottom line — **N different bets** (Required deliverable 5) — N strategic-posture paragraphs + 1 catalyst paragraph
11. References block (every URL deduplicated, grouped: primary filings A / primary filings B / [primary filings C] / [primary filings D] / industry research / press / regulatory)

## Citations

Same standard as [[company-research]]. Read its `references/citations.md` before drafting — those rules apply verbatim. Summary:

- **Paragraph-level coverage.** Every substantive paragraph carries ≥1 inline markdown-link citation. Tables, captions, and TOC entries are exempt; nothing else is.
- **Deep URLs only.** Link to the specific SEC EDGAR document, the specific cninfo PDF, the specific Yole / Gartner / IPnest report page. Never a homepage.
- **Source-chain labels** when a third-party number appears in a primary filing — e.g. `[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/...)`.
- **Preserve original language in link titles** — Chinese filings stay `年度报告`, US filings stay `10-K`, Japanese stay `有価証券報告書`.
- **Freshness:** discard web sources older than ~12 months for industry data; include the publication date in the link title (`[Reuters, 2025-08-12](https://...)`).
- **Density target: ≥40 inline citations** across the body of a 5,000–9,000 word comparison.

## Numerical Accuracy (MANDATORY — every number traces to the original source, not a research doc)

The project-wide **Numerical Accuracy** rule in `/Users/x/projects/financial_agent/CLAUDE.md` ("every numerical claim must trace to a URL cited in that same paragraph where the number literally appears as a string") applies verbatim to comparison reports. Re-read that section before drafting. Compare-specific failure modes on top of the base rule:

1. **Never cite `reports/company/<X>/...md` as the source of a number.** The Prerequisites step has you read each side's prior research doc as structured *input* — but those research docs are themselves derived work. Citing one of them in a comparison shifts the verification chain instead of completing it ("the number is in the research doc, which got it from… ?"). When a number originated in the research doc you just read, follow its inline citation to the primary source (the 10-K page, the IPnest report URL, the vendor product page, the press release) and cite **that** in the comparison. If the research doc has no inline citation for the number, treat the number as unverified — re-derive it from a primary source or drop the claim.

2. **Cross-company comparisons require both sides' originals to contain the comparable figure.** A row that says "A: 47% gross margin vs B: 32% gross margin" needs **two** primary citations — A's 10-K (or 年度报告 / Yuho) for the 47% and B's filing for the 32%. A bundled "[Stratechery](...)" cite isn't enough unless that article actually quotes both numbers verbatim. Mismatched period-ends (A's FY24 vs B's FY25) must be disclosed in the cell.

3. **Third-party share numbers must cite the third party, not the company that quoted it.** "SNPS has 50% interface-IP share (10-K)" is wrong — the 10-K never says "we lead". Cite IPnest, Gartner, IDC, etc. directly, with the specific report URL and date. Use the source-chain label only when the third-party report is paywalled and the primary filing quotes it verbatim (`[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/...)`).

4. **Derived deltas must be labelled.** "A grew 3× faster than B" is a comparison of two reported growth rates — write it as `~3× (A's 28% YoY vs B's 9% YoY — both from each company's Q4 release)` so a reader can re-derive, and cite both releases in the same paragraph. Never quote the multiple as if it came from a single source that only contains one of the inputs.

5. **Scorecard "Edge" verdicts need underlying-paragraph citations.** A scorecard row like "Operating margin | A | 28% vs 19%" is a summary of a §4 paragraph claim. The body paragraph must already have both numbers cited inline; the scorecard cell inherits those citations and does not need its own. But if the scorecard names a number that's *not* in the body, that's an unsourced claim — add the citation to the body, or drop the number from the scorecard.

6. **Spot-check before commit.** Before saving either language file, pick 5 random numbers across the TL;DR / moat anatomy / scorecard and string-match each against the URLs in its paragraph (`curl -s URL | grep -F "47%"`). If a number doesn't string-match in any URL cited in that paragraph, fix the paragraph — don't ship. Compare-specific extension: the spot-check must include at least one number that came from each side's prior research doc, to confirm you traced it back to the original rather than just copy-pasting the research-doc paragraph.

If a number can't be sourced to a primary original (only to the research doc, only to a paywalled secondary, only to an analyst's tweet), either remove it or replace it with a phrasing that the available primary sources actually support ("materially higher" instead of "47% higher" if you only have the qualitative trend). Never leave a derived-from-research-doc number in a comparison report without re-citing the primary.

## Prerequisites

This skill builds on [[company-research]]. **Before drafting any new content, always check the local `reports/company/` folder for prior research** — this is the most-asked question about this skill and the most common source of duplicated work if skipped.

```bash
# Step 1 — Resolve each side to a slug and check for existing research.
# ALWAYS case-insensitive (-i) and match on the TICKER, not just the name:
# folder casing is inconsistent in this repo (e.g. the XPeng report lives at
# `Xpeng_NYSE_XPEV/`, NOT `XPeng_…`), so a case-sensitive `*XPeng*` glob misses it.
ls reports/company/ | grep -iE "<Ticker_A>|<Name_A>"
ls reports/company/ | grep -iE "<Ticker_B>|<Name_B>"

# Step 2 — For each match, list what's inside the slug folder.
# Use the EXACT folder name printed by Step 1 — don't retype it from memory,
# the casing must match on a case-sensitive filesystem.
ls "reports/company/<exact-folder-from-step-1>/" 2>/dev/null
```

**Two gotchas that have caused a wasted full research run** (claiming a report was "missing" when it existed):
- **Casing varies** — match case-insensitively on the ticker (`grep -iE XPEV`), never a case-sensitive name glob.
- **Both filename conventions exist** — a Chinese report may be `<Slug>_公司研究.md` (skill default) **or** `<Slug>_Research_Document_zh.md` (English-template name + `_zh`). Match on the ticker, not the convention.
- **Never `ls A B C` in one command** — in zsh a single non-matching glob aborts the whole command (`nomatch`), so a real match on another path is never printed. Check each side in its own command (as above).

The relevant files inside each slug folder, by language:

| Language | Filename pattern |
|---|---|
| English | `<Slug>_Research_Document.md` |
| Simplified Chinese | `<Slug>_公司研究.md`, `<Slug>_研究报告.md`, **or** `<Slug>_Research_Document_zh.md` |
| Bilingual | both an EN and a ZH file coexist; pick the language matching the comparison report's language |

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

User input forms accepted (2 to 4 companies):
- `compare-companies SNPS CDNS` (N=2)
- `compare SNPS and CDNS` (N=2)
- `SNPS vs CDNS` (N=2)
- `Synopsys vs Cadence` (N=2; resolve to tickers)
- `compare Databricks vs Snowflake vs Oracle` (N=3)
- `AWS vs Azure vs GCP vs OCI` (N=4)
- `compare X Y Z` (N=3 with implicit conjunction)

**Determine N from the input.** Count the comma- / "vs" / "and"-separated entities. **Reject N=1 (use [[company-research]] instead) and N≥5 (use `/sector-overview`, or split into pairwise reports).** For N between 2 and 4, proceed.

For each side, resolve to a canonical `<Slug>` (matching the company-research slug convention: `<Name>_<EXCHANGE><CODE>` or `<Name>_<EXCHANGE>_<CODE>`). Preserve the user's left-right order — that becomes the file naming and the column ordering throughout the report.

Then check each side **independently and case-insensitively**, matching on the ticker or name. Do NOT combine into one `ls A B C` — in zsh a single non-matching glob aborts the whole command (`nomatch`), so a real match on another side is silently never printed. Casing also varies (e.g. `Xpeng_NYSE_XPEV/`), so always use `grep -i`:
```bash
for q in "<Ticker_A>|<Name_A>" "<Ticker_B>|<Name_B>" "<Ticker_C>|<Name_C>"; do   # extend to N
  echo "== $q =="
  ls reports/company/ | grep -iE "$q" || echo "  (no existing research — run company-research for this side)"
done
```

For **each** of the N companies:
- Research doc present and <12 months old → proceed to Step 1.
- Missing → invoke [[company-research]] on that side, then proceed.
- Stale (>12 months) → invoke [[company-research]] to refresh (it auto-updates in place).

When N=3 or N=4, the prerequisite-checking phase is the most likely point at which the workflow stalls — surface the result for the user up-front ("Found research for A (May 28), B (May 29), C (May 27); missing for D — will run company-research on D first") so they can choose whether to wait or split the work over multiple sessions.

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

### Step 6.5 — Write the English report, then the Chinese companion (default workflow)

**Default: produce two complete, independent comparison reports — one in English, one in Simplified Chinese.** Generate the English version first (Steps 2–6 build a single English draft), then produce the Chinese companion as a second pass over the same underlying research.

**English draft first** — save as `reports/compare/<A>_vs_<B>.md`. Run all of Step 7 (verification) on the English draft before starting the Chinese companion. A defective English draft will propagate its defects into Chinese — fix it once, in English, before translating the analytical work.

**Chinese companion second** — save as `reports/compare/<A>_vs_<B>_zh.md`. Re-author the prose natively in Simplified Chinese — do NOT machine-translate the English file. Both files share:
- The same TL;DR claims, scorecard verdicts, product-overlap matrix rows, moat-anatomy numbers, customer-overlap lists, "other big players" classifications, and bottom-line catalysts.
- The same citations (URLs identical; link titles preserve original language — `10-K` stays `10-K` in the Chinese report, `年度报告` stays `年度报告` in the English report).
- The same charts (mermaid blocks identical other than axis labels translated where appropriate).

But each file has natively-authored prose in its own language. Section headers translate (`## TL;DR — At-a-glance advantages and disadvantages` ↔ `## TL;DR — 优劣势速览`; `## §5 The moat anatomy` ↔ `## §5 护城河剖析`; `## Bottom line — two different bets` ↔ `## 底线判断 — 两种不同押注`). Bilingual technical terms are MANDATORY in the Chinese edition (`毛利率 (gross margin)`, `RPO (剩余履约义务)`, `Tier-1 供应商`) — see the "Report language" section earlier in this skill for the canonical gloss list.

**If the user overrode to a single language** (`--en-only` / `--zh-only` / `English only` / `用中文即可` / etc.), skip the other-language step entirely and produce only the requested file.

### Step 7 — Verification pass (run for BOTH languages)

Apply the same Step 10 verification flow from [[company-research]] — URL check, SEC filename resolution, 10-K claim spot-checks, executive-name verification, self-audit checklist. Append a `<details>` verification log at the end of **each** report (English log in the English file, Chinese log in the Chinese file — both follow the same structure; minor differences are fine if e.g. different translated source citations were spot-checked).

**Compare-specific additional checks (apply to BOTH the English and Chinese reports unless the user overrode to a single language):**

- [ ] **TL;DR is present, placed before §1, has N rows, and contains 5–8 bullets per cell.** Every bullet leads with a specific number/noun (not an adjective) and ends with a `(§N)` section reference. Each Disadvantages column has at least (Advantages count − 2) bullets — no whitewash.
- [ ] **TL;DR "Who is each one for?" paragraph** names N+1 sharp options (pick A for X, pick B for Y, pick C for Z, or run a hybrid because W) — no both-sidesism / no all-N-sidesism.
- [ ] **Prior research consulted before drafting.** Ran `ls reports/company/` for each side; if a doc existed, read it before writing anything new. Did not duplicate work.
- [ ] The product overlap matrix uses the N-way status grammar (`ALL N COMPETE` / `A vs B compete, C absent` / `NON-OVERLAPPING (X only)` / etc.). Every row has been classified — no `unclear` or `mixed` rows. At least one row each is `ALL N COMPETE`, `NON-OVERLAPPING`, and at least one mid-state status (a side absent or a side dominant).
- [ ] Every "share leader" claim in the moat anatomy has a third-party citation; none use a 10-K cite.
- [ ] The customer-comparison section names ≥3 customers visible at *multiple* sides (the multi-vendor reality), backed by either each vendor's customer-page listing or a third-party article.
- [ ] The scorecard has no row that says "depends" / "complex" / "mixed" — every row picks a side / a rank / "Tied" / "Neither". For N≥3, ranks are explicit (1/2/3 with `=` allowed for ties) — no row leaves any company unranked.
- [ ] The bottom line has **N strategic-posture paragraphs** (not 2), and the closing catalyst paragraph names which side wins under which observable condition. No "all N could win" hedging.
- [ ] Every TL;DR claim is supported by an inline citation somewhere in the body (the TL;DR cells themselves are exempt from per-bullet citations since they're a scannable summary, but the underlying fact must be cited in §N).
- [ ] **§5.8 names 3–7 other big players** (players *beyond* the focal N) in the focal set's space, classified as Primary competitor / Adjacent / Acquisition target / Domestic-market alternative. At least 3 Primary competitors get 100–300 word paragraphs. **No double-listing** — a company is either in the focal N or in §5.8, never both.
- [ ] **§5.3, §5.4, §5.5 tables extended** with columns for each Primary competitor (§5.8 names) that materially affects the share picture. For an N=3 report that already covers most of the industry, this may mean only 1–2 additional columns; for an N=2 report it may mean 2–4.
- [ ] **Every "other big player" named came from a verifiable source** — 10-K competitor list, IPnest / Gartner / IDC / IBISWorld / TrendForce / IQVIA leaderboard, or recent industry-research note. No inventions.
- [ ] **(N≥3) Word count meets the scaled target** — 7,000–12,000 for N=3; 10,000–15,000 for N=4. Run `wc -w <file>` before declaring done.

**Bilingual-specific checks (skip when the user overrode to a single language):**

- [ ] **Both files exist** — `reports/compare/<A>_vs_<B>.md` AND `reports/compare/<A>_vs_<B>_zh.md` are present at the canonical paths and each independently hits 5,000–9,000 words (Chinese counted in characters).
- [ ] **Data parity between the two files** — TL;DR claims, scorecard verdicts, product-overlap rows, moat-anatomy numbers, named-customer overlaps, "other big players" classifications, and bottom-line catalysts are the same in both. Use `diff` on the table cells if needed.
- [ ] **Prose is natively authored, not machine-translated** — the Chinese report flows naturally; section headers are translated; bilingual technical terms appear on first mention (`毛利率 (gross margin)`, `RPO (剩余履约义务)`).
- [ ] **Citation URLs are identical between the two files**; only link titles preserve original language (a US `10-K` stays `10-K` in both files; a `年度报告` stays `年度报告` in both files).
- [ ] **Both files have their own Step-10 verification log.**

## Output location

Save both reports under `reports/compare/` at the project root. Preserve the user's left-right ordering in both filenames — do not alphabetize. The viewer (http://localhost:5001/reports) surfaces files under `reports/compare/`.

**Filename convention — no date suffix; `_zh` suffix marks the Chinese edition; N-way uses `_vs_` between each side:**

| N | Language | Filename pattern |
|---|---|---|
| 2 | English | `<A>_vs_<B>.md` |
| 2 | Chinese | `<A>_vs_<B>_zh.md` |
| 3 | English | `<A>_vs_<B>_vs_<C>.md` |
| 3 | Chinese | `<A>_vs_<B>_vs_<C>_zh.md` |
| 4 | English | `<A>_vs_<B>_vs_<C>_vs_<D>.md` |
| 4 | Chinese | `<A>_vs_<B>_vs_<C>_vs_<D>_zh.md` |

**Slug discipline (applies to every position):** prefer the shortest unambiguous handle — ticker for US public (`SNOW`, `ORCL`), name for private (`Databricks`), `<Pinyin>_<EXCHANGE><CODE>` for China A-share / HK, and Romaji + exchange code for Japan / Korea / Taiwan. The English filename must lead with each side's English or pinyin name even when the underlying company is Chinese (per the global rule in `/Users/x/projects/financial_agent/CLAUDE.md` → "Research Report Filenames") — pure-Chinese filenames are unsearchable.

**Examples:**

- N=2 US pair: `SNPS_vs_CDNS.md` + `SNPS_vs_CDNS_zh.md`; `LRCX_vs_AMAT.md` + `LRCX_vs_AMAT_zh.md`; `AMD_vs_NVDA.md` + `AMD_vs_NVDA_zh.md`
- N=2 China A-share pair: `Anjizhike_SSE688019_vs_Dinglong_SZSE300054.md` (English) + `安集科技_SSE688019_vs_鼎龙股份_SZSE300054_zh.md` (Chinese)
- N=2 mixed-domicile: `BYD_HKEX1211_vs_TSLA_NASDAQ.md` + `BYD_HKEX1211_vs_TSLA_NASDAQ_zh.md`
- N=3 mixed: `Databricks_vs_SNOW_vs_ORCL.md` + `Databricks_vs_SNOW_vs_ORCL_zh.md`
- N=3 semicap: `LRCX_vs_AMAT_vs_ASML.md` + `LRCX_vs_AMAT_vs_ASML_zh.md`
- N=4 hyperscaler infra: `AWS_vs_Azure_vs_GCP_vs_OCI.md` + ..._zh.md
- N=5 or more: NOT SUPPORTED by this skill — split into multiple pairwise reports (or use `/sector-overview` for a survey).

**Update-in-place rule** — at most one English file and one Chinese file per ordered tuple. If `<A>_vs_<B>_vs_<C>.md` (or `_zh.md`) exists, update it in place. If a file exists with the same tuple in a different order (e.g. `<C>_vs_<A>_vs_<B>.md`), ask the user which canonical order to keep before writing — preserving the user's left-right ordering from their request takes precedence. When a Chinese edition exists at a legacy path (e.g. an all-Chinese-slug filename from before this rule), consolidate it into the `<EnglishStem>_zh.md` canonical name and list the legacy file so the user can confirm deletion. Do not auto-delete.

**Single-language override** — if the user requested `--en-only`, only the `<...>.md` file is written; if `--zh-only`, only `<...>_zh.md`. The default (no override) always produces both.

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
- It does **not** cover 5 or more companies in one file — at N=5+ the head-to-head sharpness collapses entirely and the report becomes a survey. For 5+, either split into multiple pairwise / 3-way reports or use [[sector-overview]] for a wide-lens treatment.
- It does **not** repeat content from the per-company research docs verbatim — if you find yourself copy-pasting from one of the source research docs, you're missing the comparison angle. Rewrite to highlight the delta.
