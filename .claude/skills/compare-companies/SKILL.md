---
name: compare-companies
description: Produce 5,000–15,000 word head-to-head comparisons of **2 to 4 public (or private) companies** in both English AND Chinese — focused on whether their products directly compete, who wins which moat dimension, how their customer bases overlap, and what advantage each holds over the others. Two separate markdown files are saved to `reports/compare/` — one in English (`<A>_vs_<B>.md` or `<A>_vs_<B>_vs_<C>.md`) and one in Simplified Chinese (`..._zh.md`). Use when the user asks to "compare X and Y", "X vs Y vs Z", "head-to-head", "side-by-side", or "do these N compete" — e.g. "compare SNPS and CDNS", "AMD vs NVDA", "Databricks vs Snowflake vs Oracle", "LRCX vs AMAT vs ASML side-by-side".
---

# Compare Companies

Head-to-head deliverable: a **5,000–15,000 word** markdown report that does NOT re-tell each company's story — it interrogates the **delta**. The report's job is to answer seven specific questions the reader will have.

**Supports 2 to 4 companies (N=2, 3, or 4).** The binary (N=2) case is the canonical reference — `reports/compare/SNPS_vs_CDNS.md`. For N=3 (three-way) and N=4 (four-way), the same skeleton scales: tables grow to N columns, the TL;DR table to N rows, the bottom-line section to N strategic-posture paragraphs. Word-count target scales by N: **5,000–9,000 words for N=2; 7,000–12,000 for N=3; 10,000–15,000 for N=4.** Beyond N=4 the head-to-head sharpness collapses entirely — split into pairwise reports or use `/sector-overview` instead.

Throughout this spec, "A vs B" is the canonical 2-way framing; whenever you see it, mentally generalize to "A vs B vs C (vs D)". Where N-way (3+) requires a structurally different table or phrasing, the spec calls it out explicitly with an "**N-way:**" tag.

0. **In 60 seconds, what are each side's advantages and disadvantages?** (TL;DR table right after the title — see §0.)
1. **Do their products directly compete, or are they more complementary?** (Per-product overlap matrix — see §5.0.)
2. **What is each company's actual moat — quantified, not asserted?** (Seven-subsection moat anatomy — see §5.1–5.7.)
3. **Who are their customers, and where do those customer bases overlap?** (Customer concentration + named-win comparison — see §5.1.)
4. **What advantage does each have over the others?** (Dimension-by-dimension scorecard — see §9. For N≥3, rows record per-pair edges or a 1st/2nd/3rd ranking.)
5. **Which one should the reader bet on, and why?** (Synthesis — see §10. For N≥3, N strategic-posture paragraphs.)
6. **Who else matters in this space?** (3–7 other big players surveyed alongside, with their position vs. the focal set quantified — see §5.8. For N=2 the focal "set" is the pair; for N=3 or 4, §5.8 covers companies *beyond* the focal N.)

A comparison report that only restates each company's pitch is a failure. The reader has already read both companies' marketing material; they came to you for the delta.

**Discoverability discipline.** Most readers will scan the TL;DR + scorecard + bottom line and stop. The detailed sections (§1–§10) are evidence for the scannable layer — write them assuming the reader will skim. Tables beat paragraphs; numbers beat adjectives; explicit section cross-references (§5.5, §6) help a skimmer drill into the one section they care about.

## Guardrails (at-a-glance — the rules with the worst failure modes)

Compact index of the load-bearing don't-dos enforced throughout this skill. Each rule has been the cause of a real defect in past compare-companies reports.

- **Do not invent a head-to-head fact.** Share numbers, product overlap claims, customer-overlap counts must each come from a checkable source. See § "Core principle".
- **Do not cite the subject's 10-K for a share-leadership claim.** 10-Ks never say "we lead"; relabel as `*Analyst view:*` and cite IPnest / Gartner / IDC at a specific URL. See § "Specific failure mode: do NOT misattribute sell-side opinions to filings" in [[company-research]].
- **Do not cite `reports/company/<X>/...md` as the source of a number.** That's a derived work; follow its inline citation to the primary source and cite that instead. See § "Numerical Accuracy".
- **Do not let a scorecard cell say `depends`, `arguably`, `slightly`, `mixed`, `potentially`, or `could`.** Pick a side / a rank / "Tied" / "Neither". See Required deliverable 4.
- **Do not skip §5.8 ("Other big players").** Listing only the focal N misrepresents the industry; surface 3–7 other players classified into Primary / Adjacent / Acquisition target / Domestic-market alternative, with the moat-anatomy tables extended for Primary competitors. See Required deliverable 6.
- **Do not write a side's bet that paraphrases another side's bet.** Bottom-line bets must be orthogonal; if they aren't, you haven't found the delta. See Required deliverable 5.
- **Do not skip the Data Used manifest** at the end of each report. The compare-specific manifest must list both sides' primary filings + the third-party share sources that anchor §5.4. See `references/report_structure.md` → "Data Used".
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim — read its **Core principle** section before drafting. Summary of the comparison-specific failure modes:

- **Never invent a head-to-head fact.** "Synopsys has 60% interface IP share, Cadence has 25%" is checkable; if IPnest's actual number for Cadence is "not separately broken out", say so, not 25%.
- **Never invent a product-overlap claim.** "Synopsys VCS competes with Cadence Xcelium" is checkable (both are functional-verification simulators). "Synopsys VCS competes with Cadence Genus" is wrong (Genus is logic synthesis). Build the overlap matrix from each vendor's product pages — do not improvise.
- **Share-leadership claims need a third-party source.** "CDNS leads in PCB" needs an IPnest / Gartner / TechInsights cite, not a 10-K cite. The 10-K never says "we lead". Same rule as company-research §"do NOT misattribute sell-side opinions to filings".
- **When two sources disagree on a head-to-head number** (e.g. SemiAnalysis says one thing, an IPnest secondary citation says another), name both and prefer the primary / more-recent.
- **The analyst's own model is NOT a source.** Never write "(Source: our model)" or "(estimate, our analysis)" for a comparison fact.

## Report language

**Default behavior: ALWAYS produce both English AND Simplified Chinese (zh-CN).** Never Traditional Chinese, Japanese, or Korean for the prose. Same rule as [[company-research]] — read its "Report language" section before drafting.

Each company pair gets **two separate, complete comparison reports** — one in English, one in Simplified Chinese. Both are produced in a single workflow run and saved to `reports/compare/`. Generate the English version first, then the Chinese version. Both files independently meet the N-scaled target (5,000–9,000 for N=2; 7,000–12,000 for N=3; 10,000–15,000 for N=4 — Chinese counted in characters; see `references/report_structure.md`).

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
- China A-share pair: `Anjizhike_SSE688019_vs_Dinglong_SZSE300054.md` + `Anjizhike_SSE688019_vs_Dinglong_SZSE300054_zh.md` — **the Chinese edition also leads with the English/pinyin stem** (global filename rule: every report filename starts with an ASCII English/pinyin token, even when the prose is Chinese). A legacy all-Chinese filename like `安集科技_SSE688019_vs_鼎龙股份_SZSE300054.md` is non-compliant — consolidate it per the Update-in-place rule.

**Language-specific instructions when drafting:**

- **English report** — full prose per the structure in `references/report_structure.md`. Standard business English, accessible to global equity investors. Preserve original-language titles for non-English citations (e.g., `比亚迪 BYD 2024 年度报告`, `Sumitomo 統合報告書`). Bilingual technical terms in parentheses where helpful (`advanced packaging (先进封装)`), but bilingualism is optional in English prose — what matters is clarity for English readers. Section headers in English (TL;DR, Moat anatomy, Bottom line, etc.).
- **Chinese report** — full prose in Simplified Chinese (zh-CN). Write as if for Chinese investors. Use **bilingual technical terms** per [[company-research]]'s rule (English / Chinese gloss on first mention, e.g. `毛利率 (gross margin)`, `RPO (剩余履约义务)`, `Tier-1 供应商`). Section headers in Chinese (TL;DR — 优劣势速览, 护城河剖析, 底线判断, etc.). Bilingual terms are MANDATORY in Chinese, not optional. Keep ticker codes, acronyms, and product code-names in their original form: `SNPS`, `CDNS`, `H200`, `RMB`, `bp`, `YoY`.

A Chinese reader should find the Chinese report as natural and fluent as an English reader finds the English report. Neither version is the canonical "source"; they share data, not prose.

**Chinese names in English reports / English names in Chinese reports:** Chinese companies may appear in their original Chinese form alongside an English / pinyin gloss on first mention, e.g. `安培龙 (Anpeilong, SZSE:002050)`, `比亚迪 (BYD)`, `宁德时代 (CATL)`. After first mention, either form is fine. Symmetrically, US/EU company names appear in their native English form in the Chinese report alongside a Chinese gloss on first mention if a commonly-used translation exists (`Synopsys (新思科技)`, `NVIDIA (英伟达)`, `AMD (超威半导体)`).

## The required deliverables

A compare-companies report MUST contain deliverables 0–6 (the seven core deliverables below). Missing any one of them is a defect — the user has explicitly asked for each. Deliverables 7–9 (relative-valuation scoreboard, order-of-preference line, catalyst differential) are specified under "Learning from sell-side institutional research" further down and are also required; they were added to absorb sell-side relative-value rigor.

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

### Required deliverable 1 — Product overlap matrix (§5.0 — opens the moat section, immediately before §5.1)

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

### 延伸观看 / Further viewing — explainer videos (optional, but default to including)

When this report turns on whether two products *actually substitute* — and the answer lives in their **internal mechanics** the reader can't picture from prose (two robot joints — a harmonic-drive vs a cycloidal actuator; two lithography light-sources — DUV immersion vs EUV; two battery cell formats — prismatic LFP vs cylindrical 4680; two foundry transistor architectures — FinFET vs gate-all-around) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* why the products do or don't compete, not just read the verdict. Default to including them whenever the overlap matrix (§5.0) hinges on a hard-to-visualize mechanism; omit only when the comparison is purely numeric with nothing worth visualizing.

**This skill writes TWO files: the English `<A>_vs_<B>.md` uses the English heading `## Further viewing — explainer videos`; the Chinese `..._zh.md` uses the bilingual heading `## 延伸观看 / Further viewing`.** The video list itself is shared between both files (same URLs); only the heading and the caption language differ.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**延伸观看 / Further viewing**` bullet list at the end of the section the concept lives in (most naturally beside the §5.0 overlap matrix row whose mechanism is in question), or a single `📺` note beside the hard concept. English-only reports use `**Further viewing**`.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(B站，部分地区或需登录)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: `.claude/skills/company-research/references/citations.md` § "Further viewing — explainer videos" (this skill has no local `references/citations.md` — the spec lives in the parent skill).

### Required deliverable 2 — Moat anatomy (§5.1–5.7; §5.8 is Required deliverable 6)

Seven analytical subsections (§5.1–§5.7), each anchored to specific disclosed numbers, not adjectives. Proven structure from the SNPS-vs-CDNS rewrite (May 2026). **For N≥3, every subsection's tables grow to N columns; the analytical questions stay the same.** When a side doesn't disclose a number that others do, write `not disclosed` in that side's cell — don't estimate or omit the column.

1. **Customer concentration** — top-1 / top-5 / >10% disclosures from each 10-K (or 年度报告 / Yuho); geographic mix table side-by-side across all N companies; multi-year trend; **call out who is *most* exposed** (for N=3+, name the rank) and whether each side's diversification is genuine or driven by losing a major customer.
2. **Backlog & recurring mix** — RPO / non-cancellable backlog $; backlog ÷ revenue ratio; duration ladder (<12mo / 13–36mo / >36mo); % recurring / ratable; typical contract length; multi-year trend.
3. **Channel / foundry / distribution lock-in** — for semis: per-foundry, per-node certification matrix. For consumer/SaaS: distribution partners, hyperscaler marketplace presence, OEM design-ins. For pharma: payer formulary coverage. For industrial: Tier-1 OEM relationships.
4. **Tool-level / sub-segment market share** — every published share number from a credible third-party source (Gartner, IDC, IPnest, IQVIA, IBISWorld, etc.) — never invented. Each row of the table is "segment → leader → estimated share → source".
5. **IP / patent / data-corpus franchise** — IP portfolio size, segment leadership claims (with third-party citations), proprietary data assets, patent fortress depth (expiry date span), exclusive licenses.
6. **Why a customer picks one over the other** — distilled decision framework (5–7 numbered drivers); concrete dual-vendor evidence at top-3 named customers; explicit quote from a third-party industry observer on customer behavior.
7. **Cracks worth naming** — the cracks each side's CEO would *not* highlight: shareholder lawsuits, executive departures, segment underperformance, regulatory overhangs, customer losses, churn signals.

See `references/moat_anatomy.md` for the per-subsection content spec, what to grep for in each filing type, and the failure modes to avoid.

### Required deliverable 3 — Customer comparison (lives in §5.1 — do NOT improvise a §5.1b / §6.5 home for it)

This deliverable is carried by the §5.1 customer-concentration subsection, expanded. Not just "do they have the same customers" — quantify and overlap across all N sides:

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

## Learning from sell-side institutional research

These are the disciplines a desk-grade relative-value note carries that the base skill above did not yet force. Each is grounded in a specific house pattern (Morgan Stanley, Deutsche Bank, J.P. Morgan, Goldman Sachs, Jefferies, Barclays, Citi). They sit on top of every existing rule — citation density, numerical accuracy, the no-sized-price-target boundary, the bilingual default — none of which is relaxed.

### Required deliverable 7 — Relative-valuation scoreboard (§4.5)

**The single biggest gap vs every institute analog: the skill scores moats but never tabulates what each name *costs*.** Add a first-class side-by-side multiples table, placed at the top of the report with the TL;DR (the multiples + the rating + the next catalyst are what a desk reads first), spec'd in `references/report_structure.md` §4.5.

- **Mirror Deutsche Bank's Huayan Robotics benchmark line:** DB justifies a target P/S of 12× by naming it against Dobot 15×, the HK-listed robot-peer average 12×, and the global cobot median 50× *in one breath* — not in isolation. The table is one row per name × columns for **forward PE / P/S / EV/EBITDA / PEG / div yield / FCF yield**, PLUS a **peer-median column** and a **3-yr-range column** so cheap/expensive reads like-for-like.
- **Pick the right yardstick for the regime and say which (Barclays "Pricing a capex supercycle"):** Barclays argues EV/EBITDA / EV-EBIT beats PE in capex-heavy windows and shows the cross-sectional return evidence. State which multiple is the fair yardstick for *this* pair and why — EV/Sales pre-profit, EV/EBITDA capex-heavy, PEG high-growth, PE for stable cash compounders.
- **Close the loop the moat table opens:** don't just report that A trades at a premium to B — say **whether the premium/discount is justified** by the moat/growth differential (DB: Huayan's 12× P/S is a *discount* to Dobot's 15× and that is wrong, because Dobot builds humanoids but isn't profitable while Huayan is). Moats are quantified in §5 but never reconciled against the multiple spread; this section does the reconciliation.
- **Forward estimates strip (required — the levels behind the multiples):** directly below the multiples table, a second table of **FY+1 / FY+2 / FY+3 revenue and net profit (or net margin) per name** — the per-name multi-year estimate levels that anchor every broker comparison (mirror GS "China Surgical Robots" Exhibits 1–2: sales & NP 2023→2028E per name). A "49.5% CAGR" in prose with no estimates table to scan fails the sell-side bar. Each cell is sourced to company guidance (cite the filing / IR deck) or to a broker estimate labeled `*Analyst view:*` (cite the `/zsxq/pdf/<file_id>/` note or a public deep URL) — **never the analyst's own model.** Mismatched fiscal years disclosed in-cell; cells with no published estimate get `not published`, not an invention.
- **Citation discipline (unchanged):** every multiple cites a deep URL that literally contains the number (Yahoo Finance / Eastmoney / Kabutan / Naver quote page) as of a stated date; the analyst's own model is never the source (cite the filing for the inputs, the quote page for the price); mismatched fiscal-period ends are disclosed in-cell.
- **Borrowed PT discipline (this skill ships no sized PT of its own, but it *may quote* one as evidence):** when a broker / sell-side PT is cited to support a relative-value point, pair it with the stock's price on that note's date + the implied upside (`MS PT $288 vs $232 @ 2026-06-03 → +24%`), not today's spot — a bare borrowed PT with no report-date anchor is uninterpretable. The report-date price + upside live in `stock_price_target_db` (`report_date_price` / `upside_pct`, shown at `/pt`).

### Required deliverable 8 — Order-of-preference line in the TL;DR (§0)

After the "Who is each one for?" paragraph, add **one committed ordinal line** ranking the N names by conviction, with a one-clause why per name.

- **Mirror Morgan Stanley's "Order of Preference" spine ("China and the Miners"):** MS writes a single ranked ladder — `BHP > DRR > RIO > FMG`, tagging the `#1 most preferred` and a one-clause rationale per name. The compare skill ranks advantages *per dimension* but never commits to an ordinal preference *across the set*; institutes always do, even in non-trading notes.
- **Format:** `Preference order: A > C > B` (or `A and B co-equal > C`), each name followed by a one-clause "preferred because / least-preferred because" tag. Lead each name's body treatment with that same one-line clause before the evidence (DB's "top-five cobot maker, most profitable HK-listed robot name" one-sentence tag).
- **Stays inside the boundary:** this is a relative ranking of conviction, not a trading call — the no-hedge-word rule and the no-sized-price-target rule both still hold. Banned: "arguably", "slightly", "could". You must commit to an order.

### Required deliverable 9 — Catalyst differential (extends §10)

Turn the prose-only "what to watch" into a **per-name dated catalyst table** so the reader sees which name has the nearer-term swing factor.

- **Mirror JPM's "Positive Catalyst Watch" + DB Huayan's dated catalysts:** JPM names a dated catalyst per name (QCOM June 24 Investor Day); DB lists Huayan's "1H26 results Aug; Stock Connect inclusion early Sept". One column per name × rows for the next 2–3 dated catalysts: **next results date, investor/analyst day, index-inclusion window, product launch / data readout, regulatory decision**.
- **Source each catalyst** to the company IR calendar or a dated filing (freshness + deep-URL rules apply). No undated "ongoing AI tailwind" entries — every row carries a date or a dated window.

### Optional lens — Relative-positioning / pair-trade (extends §10)

When the N names are genuine substitutes, add one paragraph framing the preferred name as the long and the least-preferred as the funding leg.

- **Mirror GS Japan SMID (long shareholder-benefit + ≥3% div / short no-benefit low-div) and JPM China Quant (long +3% / short −4.2% / L/S +7.2%):** state the explicit thesis for why the spread should converge or diverge, cite the two names' trailing relative return to a deep URL, and name the observable that would invalidate the spread.
- **Label it a relative-positioning observation, not a sized trade** — no notional, no leverage, no entry/stop. This is the natural actionable output of a "who wins" comparison and stays inside the no-sized-trading-call boundary.

### Cross-cutting disciplines (fold into existing sections)

- **Comparability caveat wherever two numbers are juxtaposed (Morgan Stanley ASCO takeaways):** MS names the single-arm-trial and chemo-resistant-enrollment bias *before* comparing AK112 ORR 61.7% vs BNT327 ORR 37.2%. The skill already flags mismatched fiscal-period ends; generalize to a standing caveat for **single-arm vs controlled, organic vs M&A-inflated, GAAP vs non-GAAP, different segment definitions** — flag the non-comparability in-cell before drawing the verdict. (See `references/moat_anatomy.md` "Common discipline" and Numerical Accuracy item 2.)
- **Anchor every relative-value verdict on the FORWARD path, not just the last quarter (DB Huayan: 55% rev CAGR 2025-28E, NPM to ~10% by 2028E):** a "who's winning" call resting only on the last reported quarter is weaker than one resting on the 1–3yr forward CAGR / margin trajectory each name is on. Each forward figure cites the filing/guidance it came from — never the analyst's own model. The scorecard "Why" column and the bottom-line bets should both lean on the forward estimate.
- **Rank quality against NAMED peers, not in isolation (DB Huayan ranks adj-NPM vs Dobot −10%, UBTECH −35%, Geekplus 1%, Estun 0%):** extend the §5 scoreboard quality rows to the §5.8 peer set so "best-in-class" is visible against real names, not asserted.
- **Carry a "priced in?" line in the bottom line (Morgan Stanley "TCL valuation already reflects the panel up-cycle"; Barclays "current price hugs target"):** each name's §10 verdict should state whether its edge is already reflected in the relative multiple — cross-reference the §4.5 scoreboard. Keeps the skill honest about whether a "winner" is also a better investment at today's relative price, without crossing into a sized trading call.

## Local institute-research library (`db/zsxq.db`) — search it FIRST for the relative-value layer

A head-to-head note lives or dies on its **relative-value evidence**: who the Street ranks #1, the borrowed price targets that anchor §4.5, the conviction order (`GS favours MedBot > EdgeMed > TINAVI`), the channel checks, and the per-name bear cases. That evidence is overwhelmingly **sell-side**, and the project carries a large local library of it — `db/zsxq.db` (table `pdf_files`, ~6,900 broker PDFs from Morgan Stanley, Goldman Sachs, J.P. Morgan, Bernstein, UBS, Citi, Deutsche Bank, HSBC, Nomura, and Chinese houses). **Search it FIRST — for every one of the N names AND for head-to-head / sector notes that rank them against each other — before web-searching for any analyst opinion, consensus estimate, price target, or conviction ranking.** This is **Step 0.7** of the workflow and it is non-optional whenever any compared name has meaningful local coverage.

Do **not** assume the upstream `company-research` doc already captured this. A comparison asks a *different* question than a single-name deep dive — it needs the **cross-name** notes (a GS "China Surgical Robots — initiate MedBot/EdgeMed at Buy" note, a sector initiation that ranks the set, an expert call that says two names are "operationally similar") that a per-company research run may never have pulled. Run the searches fresh for the comparison.

**This material is SELL-SIDE — the strictest citation discipline in this skill applies.** Everything from `db/zsxq.db` is an analyst opinion, not a primary fact. Label it `*Analyst view:*` / `*分析师观点：*` and **never blend it into a filing citation** (same rule as company-research §"do NOT misattribute sell-side opinions to filings"). A GS Buy / TP HK$45 or a "16% of China national bidding" share estimate is a GS view; cite it to the GS note, not to the company's annual report.

**The lookup helper is `find_pdf.py` from the `zsxq-analyze` skill.** Run a separate `--query` per alias for **each** name — ticker, English name, AND native-language name — plus head-to-head / sector / theme terms that surface notes ranking the set:

```bash
# Per-name (run for every one of the N sides)
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "MedBot"   --limit 40
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "微创机器人" --limit 40
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "2252"     --limit 40
# Cross-name / sector — the notes that RANK the set against each other (unique to compare)
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "surgical robot" --limit 60
python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "China Medtech going global" --limit 30
```

Then, exactly as in company-research:

1. **Triage on `topic_title` + `summary` (the curated 翻译精华), cite the original extracted text.** The summary already states broker / rating / PT / valuation basis / 2–4 thesis points — enough to pick the notes that matter and grab a headline PT/rating fast. But it is a curated secondary translation; for anything that goes in the report, quote the **original extracted text**, not the digest.
2. **Open and READ the PDF for any note that matters — image-only is NOT a blocker.** Use the three-tier flow (`ocr_pdf.py` ocrmac → Marker → `render_pdf_pages.py` + vision-LM; never Tesseract). `extract_pdf.py --file-id <id> --header` dumps page-marked text.
3. **Persist every PT call you find** (the deep read overwrites any summary-only row) — the borrowed-PT discipline in Required deliverable 7 reads the report-date price + upside back from `stock_price_target_db` (`report_date_price` / `upside_pct`, shown at `/pt`). A borrowed PT with no report-date anchor is uninterpretable.

**Where the zsxq layer feeds the comparison deliverables:**

| Deliverable | What a zsxq broker / sector note supplies (label all `*Analyst view:*`) |
|---|---|
| **§0 Order-of-preference line** (Req. 8) | The Street's own conviction ranking across the set — e.g. a GS sector note that orders `MedBot (Buy) > EdgeMed (Buy) > TINAVI (Neutral)`. Mirror it or argue against it, but cite it. |
| **§4.5 Relative-valuation scoreboard** (Req. 7) | Borrowed PTs + the valuation basis (P/S, DCF, target multiple), consensus estimates, the "premium justified?" peer-median framing (the DB Huayan benchmark line). |
| **§5.4 / §5.5 share & franchise** | Sell-side share estimates (bid-win share, installed-base counts, overseas-order tallies) that company filings never state ("we lead"). Cite the broker, never the 10-K / 年度报告. |
| **§5.6 why-a-customer-picks** | Expert-call colour on system integration, training, switching behaviour (the JPM "operationally similar" read). |
| **§9 / §10 Catalyst differential** (Req. 9) | Dated catalysts the desk is watching (results, profitability-breakeven quarter, index inclusion, registration milestones). |
| **Channel checks** | Proprietary shipment trackers / tender-win data / utilization surveys as a first-class evidence class — cite via the broker note and flag as channel-check-derived. |

**Citation format (identical to company-research).** Cite the **local direct-download route** so the user can tap straight to the PDF they own, broker + date + page in the link text — paste the `pdf_url` field `find_pdf.py` emits verbatim, do not hand-build it:

```
*Analyst view:* 高盛对 MicroPort MedBot（2252.HK）首次覆盖给予买入（Buy）、目标价 HK$45（[Goldman Sachs — China Surgical Robots initiation, 2026-04-21, p.5](http://xs-macbook-air.local:5001/zsxq/pdf/212215118214521/Goldman%20Sachs-CHINA%20SURGICAL%20ROBOTS%20Going~global%20%EF%BC%88ex~US%EF%BC%89%20as%20core%20growth%20drivers%EF%BC%9B%20Initiate%20Medbot%EF%BC%8C%20EdgeMed%20at%20Buy-260421.pdf#page=5)）。
```

- Use `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>` (raw `application/pdf`, downloads on iPad) — **never** `/zsxq/pdf-viewer/<id>` (HTML viewer) or the dead `/zsxq-pdf/<id>`. Page number in the link **text** (`p.N`).
- These local URLs are user-machine-only (they 404 for anyone else), so anchor the report's **hard facts** to public primary sources (HKEX / cninfo / SEC filings, IR decks) and use zsxq specifically for the analyst-opinion / estimate / conviction-ranking / channel-check layer it uniquely provides.

**Density bar:** at least **3–6 distinct `db/zsxq.db` citations per side** when a name has meaningful local coverage, plus **at least one cross-name / sector note** that ranks the set — every one labeled `*Analyst view:*` and cited to the `/zsxq/pdf/<file_id>/<filename>` route, never blended into a filing citation. **Top-up rule:** if `find_pdf.py` returns few or stale rows for a name (common for small / newly-listed / non-US issuers), top up from the web first — `python3 download/zsxq_downloader.py --count 100 --query "<name>"` (idempotent, dedups on `file_id`) — then re-run the searches. Note in the verification log how many zsxq notes you found vs fetched per side.

### Sell-side view evolution (卖方观点演变) — mandatory whenever ≥2 zsxq notes cover any compared name

Both language files carry the subsection (English file: "Sell-side view evolution"; Chinese file: 卖方观点演变), placed with the §4.5 borrowed-PT evidence or beside the §0 order-of-preference discussion. Requirements:

1. **Mechanical pre-pass FIRST — read `db/stock_price_target.db` before re-reading any PDF.** STRICTLY READ-ONLY: `/opt/anaconda3/bin/python3` with `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`; SELECT all rows for **each compared ticker** (columns: `research_institute, rating, price_target, target_currency, report_date, report_file_id, upside_pct`) to detect same-institute revisions and compute per-name PT dispersion (min / median / max, spread %). Writes stay exclusively via `scripts/persist_pts.py` (the Tier-2 helper behind item 3 above).
2. **Per-name, per-institute timeline.** For each compared name, order each institute's notes by report date — the filename's `-YYMMDD` suffix is the authoritative publication date (sanity-check against `create_time`). Per entry: institute, date, rating, PT, key estimates, one-line thesis. **Explicitly call out self-revisions** — upgrade / downgrade, PT raised / cut from X to Y, thesis pivot — and the stated trigger (earnings print, policy change, channel checks, order data). A 2026-03 PT and a 2026-06 PT from the same institute are two different views, not duplicates.
3. **Cross-institute disagreement PER NAME — never blend contradictory views into a fake consensus.** When institutes disagree on a name (opposite ratings, PTs >20% apart, conflicting reads of the same datapoint), render a disagreement table: Institute | Date | Rating / PT | Core argument | What evidence would prove them right.
4. **Cross-NAME preference calls (unique to this skill).** When the same institute ranks the compared set against each other ("GS prefers MedBot over EdgeMed"), those dated calls belong in the §0 order-of-preference discussion (Required deliverable 8) — and if an institute's preference order *changed* between notes, say so with both dates.
5. **Every view dated and cited.** Each institute view carries (institute, report date, `/zsxq/pdf/<file_id>/<filename>` direct-download link) per the citation format above; the borrowed-PT report-date-price discipline (Required deliverable 7) applies to every PT in the timeline.

## Report structure (TL;DR + 10 sections)

See `references/report_structure.md` for the full section-by-section spec, word-count targets, required tables and charts, and an example outline from SNPS_vs_CDNS.

Quick summary (every section's tables grow to N columns when N≥3):

0. **TL;DR — At-a-glance advantages and disadvantages** (Required deliverable 0; 3-column table with N rows + "Who is each one for?" paragraph; ~250 words for N=2, ~350 for N=3, ~450 for N=4; placed before §1)
1. One-line self-description side-by-side (N-column table — verbatim 10-K Item 1 / 年度报告 framing)
2. Strategic pillars side-by-side (timeline or pillar table; N tracks)
3. AI narrative — tool vs. tailwind (N-column table)
4. Segment structure & financial scoreboard (N-column scoreboard; mermaid xychart bar chart with N grouped bars per metric)
4.5. **Relative-valuation scoreboard** (Required deliverable 7) — N-row multiples table (fwd PE / P/S / EV/EBITDA / PEG / div yield / FCF yield) + peer-median + 3-yr-range columns; **forward-estimates strip** (FY+1/FY+2/FY+3 revenue & net profit per name); fair-yardstick paragraph; premium-justified-or-not verdict. Placed up top with the TL;DR.
5. **The moat anatomy** (§5.0 + 8 subsections — Required deliverables 1 + 2 + 6; the longest section by word count). Subsections: **5.0 product overlap matrix** (Req. 1) · 5.1 customer concentration + full customer comparison (Req. 3) · 5.2 backlog & recurring mix · 5.3 channel/foundry/distribution lock-in · 5.4 tool-level segment share · 5.5 IP/patent/data franchise share · 5.6 why a customer picks one over the other · 5.7 cracks worth naming · **5.8 other big players in this space** (players *beyond* the focal N)
6. The big bet (M&A, R&D, capital deployment — what each side is doing right now to expand TAM; N-column table)
7. Capital allocation (debt, buyback, dividend, M&A optionality; N-column table)
8. Distinctive risks (front-of-risk-factors comparison; what each 10-K leads with; N-column table)
9. Side-by-side scorecard (Required deliverable 4) — for N=2 a 3-col Edge table; for N≥3 a (N+2)-col rank-or-checkmark table
10. Bottom line — **N different bets** (Required deliverable 5) — N strategic-posture paragraphs (each with a "priced in?" line) + 1 catalyst paragraph + the **catalyst-differential table** (Required deliverable 9) + optional relative-positioning / pair-trade lens
11. References block (every URL deduplicated, grouped: primary filings A / primary filings B / [primary filings C] / [primary filings D] / industry research / press / regulatory)

## Chart rules (mandatory — every visual, both language files)

The project-wide chart rules in `~/.claude/CLAUDE.md` § "Chart generation rules" apply verbatim. Compare-specific application:

- **Visual count scales by N:** 4–8 for N=2; 6–10 for N=3; 8–14 for N=4 (mermaid blocks + matplotlib PNGs combined — see `references/report_structure.md`). A 2-visual N=3 report is a defect.
- **Every matplotlib / Plotly PNG MUST render its data source as an in-image footer annotation** (e.g. `Source: ISRG FY2025 10-K · GS 2026-04-21`). Charts get screenshotted and iframe-embedded without their surrounding caption — the source must travel inside the image. The markdown caption below the image is a backup, never the primary mechanism. When writing/updating a chart helper, the source annotation is a **required** parameter, not optional.
- **Every mermaid block gets an italic `*Source: …*` caption line immediately below the block** — the in-image mechanism isn't available in mermaid, so the caption is mandatory there.
- **Never plot series differing by >20× on a shared linear axis** — it renders the smaller names invisible (e.g. ISRG $10,064.7M vs MedBot $77M on a 0→11,000 axis = two invisible bars). Use a log scale, an indexed/normalized series (e.g. rebased to 100), or split panels. mermaid `xychart-beta` has **no log axis** — for extreme gaps, split the chart or switch the metric (growth %, mix %) instead of flattening it.
- **Verify the rightmost data point is fresh vs the report's dateline** before embedding; swap or drop stale series per the global no-stale-data rule.

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

2. **Cross-company comparisons require both sides' originals to contain the comparable figure — and a comparability caveat whenever the two numbers are not apples-to-apples.** A row that says "A: 47% gross margin vs B: 32% gross margin" needs **two** primary citations — A's 10-K (or 年度报告 / Yuho) for the 47% and B's filing for the 32%. A bundled "[Stratechery](...)" cite isn't enough unless that article actually quotes both numbers verbatim. Mismatched period-ends (A's FY24 vs B's FY25) must be disclosed in the cell — and more generally, **flag any non-comparability before drawing the verdict**: single-arm vs controlled trial, organic vs M&A-inflated growth, GAAP vs non-GAAP, different segment definitions, different revenue-recognition bases. Mirror Morgan Stanley's ASCO discipline — MS names the single-arm and chemo-resistant-enrollment bias *before* comparing AK112 ORR 61.7% vs BNT327 ORR 37.2%, rather than presenting the two ORRs as a clean head-to-head. A juxtaposed pair of numbers that the reader will read as like-for-like, when they aren't, is a hidden hallucination.

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

1. **Both research docs exist and are <12 months old** → read them in full; do NOT regenerate. The compare-companies report consumes them as structured input — Section 4 (Products), Section 5 (Customers), and Section 7 (Competitive Landscape) of each research doc become starting points for §5.0 (product matrix) and §5.1 (customer comparison) of the comparison.
2. **One side exists, the other is missing** → invoke [[company-research]] on the missing side first. Do not draft the comparison without both deep dives in hand; an uncited compare-companies report will fail the citation density target.
3. **Both exist but one or both are >12 months old** → invoke [[company-research]] on each stale side to refresh; the skill updates the existing file in place (no parallel copies).
4. **Neither exists** → run [[company-research]] on both sides first, then proceed. Expect this path to take significantly longer than path (1) — flag the user at the start so they can decide whether to wait or split the work over multiple sessions.

In all four paths, **also pull the latest 10-K / 年度报告 / Yuho for each side**, and the most recent 10-Q / 季度报告 / quarterly update — see `fetch_financial_report.py` (US) / `fetch_cninfo_report.py` (China A-share / HK). The comparison often needs raw numbers (RPO duration ladder, segment-by-region cuts, customer concentration footnotes) that the prior research doc summarized.

In all four paths, **also search the local institute-research library `db/zsxq.db` fresh for the comparison** (Workflow Step 0.7) — do not rely on the upstream company-research doc having captured the cross-name notes. A comparison needs the broker conviction ranking across the set, the borrowed PTs for §4.5, the head-to-head expert calls, and the per-name bear cases — sell-side material that a single-name research run may never have pulled. See § "Local institute-research library (`db/zsxq.db`)" for the workflow; label everything `*Analyst view:*`.

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

### Step 0.7 — Search the local institute-research library for ALL N names (always run)

Before touching websites, **search `db/zsxq.db` for broker notes on every compared name AND for the cross-name / sector notes that rank them against each other** — this is the project's local sell-side library and the fastest way to learn the Street's conviction order, borrowed PTs, and channel checks. Run one `find_pdf.py --query` per alias (ticker, English name, native-language name) for each side, plus head-to-head / sector / theme terms. See § "Local institute-research library (`db/zsxq.db`)" above for the full search-triage-cite workflow, the deliverable-by-deliverable feed table, and the citation format. Label everything `*Analyst view:*`; if a side returns few/stale rows, top up via `download/zsxq_downloader.py --query "<name>"` then re-search. This step is what populates the §0 order-of-preference line, the §4.5 borrowed PTs, and the §10 catalyst differential with real Street evidence instead of invented rankings.

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
- [ ] **Order-of-preference line present** immediately after "Who is each one for?" — a committed ordinal ranking (`A > C > B`) with a one-clause why per name, no hedge words (Required deliverable 8).
- [ ] **§4.5 Relative-valuation scoreboard present** — multiples table (fwd PE / P/S / EV/EBITDA / PEG / div yield / FCF yield) with peer-median + 3-yr-range columns; a paragraph naming the fair yardstick for this pair; a verdict on whether the premium/discount is justified. Every multiple cites a deep quote-page URL containing the number as of a stated date; no "(our model)" source (Required deliverable 7).
- [ ] **§10 Catalyst-differential table present** — per-name dated catalysts; every cell carries a date / dated window / `—`; each catalyst sourced to an IR calendar or dated filing (Required deliverable 9).
- [ ] **"Priced in?" line in each §10 posture paragraph** — states whether the name's edge is already in its relative multiple, cross-referencing §4.5.
- [ ] **Comparability caveat** flagged wherever two juxtaposed numbers aren't apples-to-apples (fiscal-end / GAAP-vs-non-GAAP / single-arm / organic-vs-M&A / segment-definition).
- [ ] **Prior research consulted before drafting.** Ran `ls reports/company/` for each side; if a doc existed, read it before writing anything new. Did not duplicate work.
- [ ] **Local zsxq library searched fresh for the comparison (Step 0.7).** Ran `find_pdf.py` per-name (all aliases) AND for cross-name / sector notes; pulled the Street's conviction ranking + borrowed PTs from `db/zsxq.db`. Body carries ≥3–6 `*Analyst view:*` zsxq citations per side (where coverage exists) plus ≥1 cross-name/sector note, each cited to the `/zsxq/pdf/<file_id>/<filename>` direct-download route and never blended into a filing citation. Verification log notes zsxq notes found vs fetched per side.
- [ ] **When ≥2 zsxq notes cover any compared name:** the Sell-side view evolution (卖方观点演变) subsection is present in BOTH language files — `db/stock_price_target.db` read-only pre-pass ran first, per-name per-institute timeline ordered by the filename `-YYMMDD` date with self-revisions + triggers called out, disagreement table rendered per name where institutes conflict (no fake consensus), dated cross-name preference calls folded into the §0 order-of-preference discussion, every view dated + cited to its `/zsxq/pdf/<file_id>/<filename>` link (see § "Sell-side view evolution (卖方观点演变)").
- [ ] The product overlap matrix uses the N-way status grammar (`ALL N COMPETE` / `A vs B compete, C absent` / `NON-OVERLAPPING (X only)` / etc.). Every row has been classified — no `unclear` or `mixed` rows. At least one row each is `ALL N COMPETE`, `NON-OVERLAPPING`, and at least one mid-state status (a side absent or a side dominant).
- [ ] Every "share leader" claim in the moat anatomy has a third-party citation; none use a 10-K cite.
- [ ] The customer-comparison section names ≥3 customers visible at *multiple* sides (the multi-vendor reality), backed by either each vendor's customer-page listing or a third-party article.
- [ ] The scorecard has no row that says "depends" / "complex" / "mixed" — every row picks a side / a rank / "Tied" / "Neither". For N≥3, ranks are explicit (1/2/3 with `=` allowed for ties) — no row leaves any company unranked.
- [ ] The bottom line has **N strategic-posture paragraphs** (not 2), and the closing catalyst paragraph names which side wins under which observable condition. No "all N could win" hedging.
- [ ] Every TL;DR claim is supported by an inline citation somewhere in the body (the TL;DR cells themselves are exempt from per-bullet citations since they're a scannable summary, but the underlying fact must be cited in §N).
- [ ] **§5.8 names 3–7 other big players** (players *beyond* the focal N) in the focal set's space, classified as Primary competitor / Adjacent / Acquisition target / Domestic-market alternative. At least 3 Primary competitors get 100–300 word paragraphs. **No double-listing** — a company is either in the focal N or in §5.8, never both.
- [ ] **§5.3, §5.4, §5.5 tables extended** with columns for each Primary competitor (§5.8 names) that materially affects the share picture. For an N=3 report that already covers most of the industry, this may mean only 1–2 additional columns; for an N=2 report it may mean 2–4.
- [ ] **Every "other big player" named came from a verifiable source** — 10-K competitor list, IPnest / Gartner / IDC / IBISWorld / TrendForce / IQVIA leaderboard, or recent industry-research note. No inventions.
- [ ] **(N≥3) Word count meets the scaled target** — 7,000–12,000 for N=3; 10,000–15,000 for N=4. Run `wc -w <file>` (English) before declaring done. Chinese files are counted in CJK characters, not `wc -w` (which undercounts CJK ~4×): `python3 -c "import re,sys;print(len(re.findall(r'[一-鿿]',open(sys.argv[1]).read())))" <file>`.
- [ ] **Visual count meets the per-N target** — 4–8 (N=2), 6–10 (N=3), 8–14 (N=4) mermaid blocks + PNGs combined (see § "Chart rules").
- [ ] **Every PNG has an in-image source footer; every mermaid block has a `*Source: …*` caption line below it; no >20× scale gap plotted on a shared linear axis** (see § "Chart rules").
- [ ] **§4.5 Forward estimates strip present** — FY+1/FY+2/FY+3 revenue and net profit (or margin) per name, every cell sourced to guidance or an `*Analyst view:*` broker estimate, none to "our model" (Required deliverable 7).
- [ ] **Further-viewing block present** beside the §5.0 row whose mechanism is hard to visualize (1–3 videos, all HTTP-checked `200` with a real-browser UA, none carrying a number) — OR a one-line waiver in the verification log stating the comparison is purely numeric with nothing worth visualizing.
- [ ] **Section numbering matches the canonical skeleton** (§5.0 overlap matrix · §5.1–5.7 moat · §5.8 other players · §6 big bet · §9 scorecard · §10 bottom line) — no improvised §N.5 / §Nb sections.
- [ ] **Data Used / 数据来源清单 manifest present between §10 and References in BOTH language files** — enumerates all N sides' primary filings, the third-party share sources anchoring §5.4/§5.5, the market-data as-of date, the zsxq broker notes used, the prior research docs consumed as structured input, and stale notices / coverage gaps (or "none").
- [ ] **Both output filenames start with an ASCII English/pinyin token** — verify with `[[ $(basename <file>) =~ ^[A-Za-z0-9] ]]`; a leading CJK character fails the report (global filename rule).

**Bilingual-specific checks (skip when the user overrode to a single language):**

- [ ] **Both files exist** — `reports/compare/<A>_vs_<B>.md` AND `reports/compare/<A>_vs_<B>_zh.md` are present at the canonical paths and each independently hits the N-scaled target (5,000–9,000 for N=2; 7,000–12,000 for N=3; 10,000–15,000 for N=4 — Chinese counted in CJK characters per the command above).
- [ ] **Language mode recorded in the verification log** — every report's log states the mode (`bilingual default` / `EN-only` / `ZH-only`); when single-language, quote the user's override phrasing verbatim (e.g. `EN skipped per user request "用中文即可"`). A single-language report with no recorded override is a defect, not an override.
- [ ] **Mechanical pair check pasted into the log** — run `ls reports/compare/<stem>*` after writing and paste the output, confirming either both files exist or the recorded override explains the missing one.
- [ ] **Data parity between the two files** — TL;DR claims, scorecard verdicts, product-overlap rows, moat-anatomy numbers, named-customer overlaps, "other big players" classifications, and bottom-line catalysts are the same in both. Use `diff` on the table cells if needed.
- [ ] **Prose is natively authored, not machine-translated** — the Chinese report flows naturally; section headers are translated; bilingual technical terms appear on first mention (`毛利率 (gross margin)`, `RPO (剩余履约义务)`).
- [ ] **Citation URLs are identical between the two files**; only link titles preserve original language (a US `10-K` stays `10-K` in both files; a `年度报告` stays `年度报告` in both files).
- [ ] **Both files have their own Step-10 verification log.**

## Output location

Save both reports under `reports/compare/` at the project root. Preserve the user's left-right ordering in both filenames — do not alphabetize. The viewer (http://xs-macbook-air.local:5001/reports) surfaces files under `reports/compare/`. (Any viewer or zsxq URL placed in a report or in the final user-facing summary must use the `xs-macbook-air.local` host, never `localhost` — `localhost` 404s on the user's iPad.)

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
- N=2 China A-share pair: `Anjizhike_SSE688019_vs_Dinglong_SZSE300054.md` (English) + `Anjizhike_SSE688019_vs_Dinglong_SZSE300054_zh.md` (Chinese — English/pinyin stem mandatory even for the `_zh` edition)
- N=2 mixed-domicile: `BYD_HKEX1211_vs_TSLA_NASDAQ.md` + `BYD_HKEX1211_vs_TSLA_NASDAQ_zh.md`
- N=3 mixed: `Databricks_vs_SNOW_vs_ORCL.md` + `Databricks_vs_SNOW_vs_ORCL_zh.md`
- N=3 semicap: `LRCX_vs_AMAT_vs_ASML.md` + `LRCX_vs_AMAT_vs_ASML_zh.md`
- N=4 hyperscaler infra: `AWS_vs_Azure_vs_GCP_vs_OCI.md` + ..._zh.md
- N=5 or more: NOT SUPPORTED by this skill — split into multiple pairwise reports (or use `/sector-overview` for a survey).

**Update-in-place rule** — at most one English file and one Chinese file per ordered tuple. If `<A>_vs_<B>_vs_<C>.md` (or `_zh.md`) exists, update it in place. If a file exists with the same tuple in a different order (e.g. `<C>_vs_<A>_vs_<B>.md`), ask the user which canonical order to keep before writing — preserving the user's left-right ordering from their request takes precedence. When a Chinese edition exists at a legacy path (e.g. an all-Chinese-slug filename from before this rule), consolidate it into the `<EnglishStem>_zh.md` canonical name and list the legacy file so the user can confirm deletion. Do not auto-delete. **The consolidation is not deferrable:** when any operation touches a tuple whose existing file has a pure-Chinese stem, the run MUST execute it in that run — write the English-stem file(s), carry the legacy content into `<EnglishStem>_zh.md`, list the legacy path for user-confirmed deletion — not note it for "later".

**Legacy N≥5 files** — if an existing `reports/compare/` file covers N≥5 names (e.g. a 7-way), do NOT update it in place under this skill: it predates the N≤4 cap. Tell the user and offer (a) migration to `reports/sector/` via `/sector-overview`, or (b) splitting into 2–4-way reports. On migration, also strip any `reports/company/*.md` "Source documents" citations per the Numerical Accuracy rule.

**Single-language override** — if the user requested `--en-only`, only the `<...>.md` file is written; if `--zh-only`, only `<...>_zh.md`. The default (no override) always produces both.

## Reference docs (read on demand)

- `references/report_structure.md` — full 10-section template, word-count targets, required tables and charts, SNPS-vs-CDNS worked outline.
- `references/moat_anatomy.md` — the 8-subsection (§5.1–§5.8) moat template with per-subsection content spec, grep keywords, and failure modes.
- `references/product_overlap_matrix.md` — how to build the directly-compete matrix, four-bucket classification rubric, sourcing rules, worked SNPS-vs-CDNS example.

Also read on demand from the parent skill:

- `.claude/skills/company-research/references/citations.md` — citation rules apply verbatim.
- `.claude/skills/company-research/references/quality_checklist.md` — pre-submit checklist (compare-companies adds its own checks above, but the company-research base list still applies).

## What this skill does NOT do

- It does **not** re-tell each company's story from scratch — the per-company deep dives live in [[company-research]] outputs. Reference them; don't duplicate them.
- It does **not** produce a recommendation in the trading sense (Buy/Hold/Sell with **sized price targets**) — that's [[trading-analysis]] and [[portfolio-decision]]. The bottom-line section identifies which bet is winning, not which stock to buy at today's price. **It MAY, however, commit to a relative ranking of conviction** (an ordinal "order of preference" line — see "Learning from sell-side institutional research") and offer an optional **relative-positioning / pair-trade lens** (long the preferred / fund with the least-preferred), because those are relative verdicts, not sized trading calls. The boundary is: no dollar price targets, no position sizing, no Buy/Hold/Sell on a single name in isolation — a ranked preference across the compared set is in-scope.
- It does **not** cover 5 or more companies in one file — at N=5+ the head-to-head sharpness collapses entirely and the report becomes a survey. For 5+, either split into multiple pairwise / 3-way reports or use [[sector-overview]] for a wide-lens treatment.
- It does **not** repeat content from the per-company research docs verbatim — if you find yourself copy-pasting from one of the source research docs, you're missing the comparison angle. Rewrite to highlight the delta.
