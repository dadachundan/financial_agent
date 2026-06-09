# Moat Anatomy — Eight-Subsection Template

This is the analytical centerpiece of every compare-companies report. The user's recurring complaint about prior comparison reports has been that they assert "moat" without quantifying it. This template forces the analyst to pull the disclosed numbers, build the matrices, and name the specific franchises — not write adjectives.

**Total moat-section length target scales by N:** 1,500–2,500 words for N=2; 2,200–3,500 for N=3; 3,000–5,000 for N=4. If your draft has the moat section shorter than any other section in the report, the priority is wrong.

**N-way reminder.** Every table in this section is "side-by-side" — that means **N-column** when N≥3. Every "both" / "neither" / "one side or the other" phrasing in the prose generalizes to "all three" / "two of the three" / "only A and C" — name the specific subset, do not pretend N=2 when N=3+.

## Common discipline (applies to all seven subsections)

- **Every claim is a disclosed number or a third-party citation — not an adjective.** "Dominant" / "leader" / "strong" / "fortress-grade" can appear as section labels but must be backed by a specific number in the prose.
- **When a number is not disclosed, write `not disclosed` — do not estimate to fill the cell.**
- **Side-by-side tables, not stacked paragraphs.** The user is looking at the comparison; the table is the deliverable.
- **Two-edged framing wherever real.** If diversification is driven by losing a major customer, say so. If margin expansion came from one-time mix, say so. Bull-only narratives are not credible.
- **Comparability caveat wherever two numbers are juxtaposed.** Before drawing a verdict from "A: X vs B: Y", flag any way the two are *not* apples-to-apples — mismatched fiscal-period ends, single-arm vs controlled trial, organic vs M&A-inflated growth, GAAP vs non-GAAP, different segment definitions, different revenue-recognition bases. Mirror Morgan Stanley's ASCO discipline: MS names the single-arm and chemo-resistant-enrollment bias *before* comparing AK112 ORR 61.7% vs BNT327 ORR 37.2%, rather than presenting them as a clean head-to-head. A juxtaposed pair the reader reads as like-for-like, when it isn't, is a hidden hallucination.
- **Anchor the "who's winning" read on the forward path, not just the last quarter.** A verdict resting only on the last reported period is weaker than one resting on the 1–3yr forward CAGR / margin trajectory each name is on (mirror DB Huayan: 55% rev CAGR 2025-28E, NPM to ~10% by 2028E). Each forward figure cites the filing/guidance it came from — never the analyst's own model.

## §5.1 — Customer concentration

What to pull from each filing:

- **>10% customer disclosure** — required for US issuers under ASC 280-10-50-42 (segment-reporting note, usually Note 19 or Note 1). If the prior-year was disclosed but the current year is silent, the 10-K is *implying* no customer crossed the threshold — say so.
- **Top-1 / top-5 cumulative share** — China A-share / HK 年度报告 mandate `前五大客户` and `客户集中度`. Japan Yuho discloses `主要な販売先` by segment. Korea 사업보고서 has `주요 매출처`. US 10-Ks only force the 10% line, so top-N is usually "not disclosed".
- **Geographic mix** — Note 19 / segment-reporting geographic table on US 10-Ks. Build the full year-over-year row for any region material to the comparison (typically: US, China, Korea, Japan, Europe, RoW).
- **Multi-year concentration trend** — at minimum 3 years; lifts up "the trajectory" as a discussion point.
- **Channel partner concentration if material** — for OEM-channel businesses, the >10% reseller / distributor disclosure can be more informative than direct-customer concentration.

What to look for in the prose:

- Is the diversification *genuine* (acquired customer-base broadening the denominator) or *forced* (the historical top-1 customer reduced spend)? Distinguish — the difference matters to a forward read.
- Is geographic concentration shifting? (e.g. SNPS: Korea overtook China in FY25.)
- Is there a customer-becoming-competitor risk on the horizon? (hyperscaler ASIC insourcing, big-retailer private-label, automaker in-house battery cells, etc.)

Failure modes:

- Writing "no major customer concentration" without pulling the >10% disclosure — verify.
- Stacking top-5 numbers across both sides when only one side discloses top-5 — be explicit when a side doesn't disclose.
- Claiming a customer is the top-1 by name when the 10-K doesn't name them — analyst triangulation, label accordingly.

## §5.2 — Backlog and recurring mix

What to pull:

- **Remaining performance obligation (RPO) / backlog** — usually in the Revenue note (Note 5 on US 10-Ks).
- **Non-cancellable portion** — distinguish total backlog from non-cancellable; some companies disclose only one.
- **Duration ladder** — % expected to be recognized in <12 months, 12–24 months, >24 months. Some companies disclose 13–36 / >36 instead.
- **Backlog ÷ revenue ratio** — the most useful single metric for visibility. Industrial / SaaS norm is 1.0–1.2×; >1.5× is fortress-grade.
- **% recurring / ratable / subscription revenue** — usually in MD&A Revenue Composition or in the deferred-revenue footnote.
- **Typical contract length** — usually called out in the revenue-recognition policy note (e.g. "TSL contracts are generally 2–3 years").
- **% of next-year revenue covered by beginning-of-year backlog** — sometimes disclosed in earnings-call CFO commentary; the strongest single visibility metric.
- **Multi-year trend** — 5-year backlog CAGR, recurring-mix trend year-over-year.

What to look for:

- A *falling* recurring mix can be bullish — if it's driven by faster-growing hardware / IP recognized up-front, not by customer churn. Name the driver.
- A *jumping* backlog can be M&A-driven; separate organic from acquired growth.
- Deferred revenue trends often telegraph FY revenue 6–12 months out.

Failure modes:

- Confusing "deferred revenue" with "RPO" — they are not the same. RPO includes future committed billings; deferred revenue only includes amounts already billed.
- Quoting backlog without the duration ladder — the duration is what makes backlog comparable.
- Treating a backlog jump as growth without separating M&A consolidation.

## §5.3 — Channel / foundry / distribution lock-in

Domain-specific. Pick the right matrix:

- **Semiconductors:** foundry-node × vendor matrix (TSMC A16/N2P, Intel 18A/18A-P, Samsung SF2, Rapidus 2nm, GF 22FDX/12LP+). For each, which side is certified and which tools/flows.
- **Pharma:** payer formulary coverage matrix (CMS, big PBM coverage tiers, EU NICE / G-BA acceptance, country reimbursement status).
- **Consumer / retail:** distribution matrix (Amazon, Walmart, Costco, Target, regional grocers; DTC % of revenue; international country coverage).
- **SaaS / enterprise:** hyperscaler marketplace presence (AWS Marketplace, Azure, GCP), partner ecosystem (Salesforce AppExchange, Microsoft Partner Network), SI consulting relationships (Deloitte, Accenture).
- **Industrial automation:** Tier-1 OEM relationships, factory-of-record install bases, regulatory certifications (UL, CE, CCC).
- **EV / mobility:** OEM design-in matrix per vehicle program, battery JV structure, charging-network partnerships.

The deliverable: a node × vendor (or formulary × drug, or channel × SKU) matrix that any reader can scan in 30 seconds to see who is present where. **Both sides usually appear in most cells at the top of the industry** — that's the normal state for a duopoly+1. The matrix's value is naming the few asymmetries.

For each row: cite the specific certification press release / formulary disclosure / partnership announcement, deep-URL only.

Failure modes:

- "Both companies are certified at every leading-edge node" without naming the nodes or showing the matrix — give the reader the table.
- Using a homepage URL ("https://www.tsmc.com/") for a node-certification claim — find the specific press release.

## §5.4 — Tool-level / sub-segment market share

The cleanest moat measure for any duopoly-or-tighter market structure: which sub-segment does each side actually dominate?

What to pull:

- **Wally Rhines / SEMI ESD Alliance** for EDA segments.
- **IPnest** for design IP (interface IP, processor IP, foundation IP) — annual report published mid-year.
- **Gartner Magic Quadrant** for enterprise software segments.
- **IDC / IBISWorld / TrendForce** for hardware segments, regional shares, end-market segmentations.
- **EvaluatePharma / IQVIA** for pharma franchise shares.
- **Wood Mackenzie / S&P Global / Rystad** for energy / commodities.
- **SemiAnalysis / SemiWiki primary research** for EDA / semi sub-segments (often the only public source for share splits inside private categories).

The deliverable: a table of `segment → leader → estimated share → source`. Every row needs a real third-party citation.

If a sub-segment share isn't published anywhere, write `not disclosed` and explain why analyst consensus exists (e.g. "no publicly published share split for Xcelium / VCS / Questa; all three are characterized as 'industry-dominant' in trade press").

**Critical**: never attach a "leader" claim to a 10-K citation. The 10-K never says "we lead" — that's analyst opinion. Cite the third-party source or label as `*Analyst view:*` (uncited).

## §5.5 — IP / patent / data-corpus franchise share

What to pull:

- **Patent fortress depth** — count of issued US patents + foreign patents from the IP-fortress disclosure in the 10-K (usually a paragraph in Item 1 Business "Proprietary Rights"); expiration date span.
- **IP segment leadership claims** — interface IP, processor IP, foundation IP (for semis); molecular libraries / formulation IP (pharma); proprietary models / training data (AI/SaaS).
- **Data-corpus moat** — for AI / ML / data-driven businesses, the historic dataset is often the deepest moat. Quantify it where possible (years of customer data, billion-row datasets, exclusive feed access).
- **IP divestitures / acquisitions in the period** — the inversion signal. If A is *acquiring* a category B is *divesting*, that's the most useful single sentence in the report.

Failure modes:

- Counting patents without expiration spans — "3,800 patents" alone is meaningless; "expiring through 2044" makes it informative.
- Attributing "industry-leading" IP claims to the 10-K — the 10-K never says that; cite a third party.

## §5.6 — Why a customer picks one over the other

The most-asked customer-side question. Two artifacts required:

**(a) Distilled decision framework** — 5–7 numbered drivers, each ranked by typical weight in the customer's decision. Example from SNPS-vs-CDNS:

1. Foundry node certification
2. Function (timing signoff → PrimeTime; custom analog → Virtuoso; …)
3. IP need (PCIe / HBM / UCIe / DSP / foundation)
4. Existing tool-of-record at this design site (dominates everything else)
5. Pricing leverage (customers run dual-vendor on purpose)

**(b) Dual-vendor evidence at top-3 named customers** — concrete examples of the largest customers running both sides. Cite vendor press releases, customer earnings calls, conference presentations. The standard finding for a duopoly is "top-10 customers all run both vendors on purpose"; if your industry has a different pattern, name it.

A useful third-party quote on customer behavior, if you can find one, anchors the section. Examples: SemiAnalysis on EDA customer behavior, IQVIA on payer-mix dynamics, In Practise interview series, Wing VC sector primers.

## §5.7 — Cracks worth naming on each side

The credibility-builder. Every report has a structural bias toward both-sides positive framing — this subsection forces honest naming of cracks.

What to look for, on each side:

- **Shareholder class actions** filed in the period (Item 3 Legal Proceedings)
- **Senior-executive departures** in the last 12 months (the "Executive Officers" sub-section of 10-K Item 1; 8-K Item 5.02 filings)
- **Segment underperformance** that may not be highlighted in the press release (margin compression, revenue decline, write-downs)
- **Regulatory overhangs** with specific clocks (BIS Compliance Monitor through YYYY-MM-DD, EU AI Act effective YYYY-MM-DD, FDA AdCom on YYYY-MM-DD)
- **Customer losses** named in earnings calls or competitor wins
- **Workforce reductions** (timing, headcount, severance charge)
- **Auditor change / restatement** anywhere in the last 24 months

The output: 3–5 bullets per side, each with a specific citation. Then a closing line on what's common to both (e.g. "Both: AI-coded EDA is more likely to widen the moat than disrupt it — the incumbents own the training corpora.").

Failure modes:

- Listing only one side's cracks — every company has them; if you found 4 for A and 0 for B, you didn't look hard enough at B.
- "Cracks" being generic risk-factor boilerplate — if the same paragraph could appear in any company's 10-K, it doesn't belong here.

## §5.8 — Other big players in this space (REQUIRED — Deliverable 6)

A focal-N view of a multi-player industry is misleading by itself. Every moat anatomy must close with a survey of **3–7 other meaningful players** in the focal set's competitive space — that is, companies *beyond* the N being compared in the report. The focal set (A vs B [vs C [vs D]]) remains the protagonist; the other players are the context that prevents readers from treating the report as a complete map.

**For N=2** the "other big players" are everyone outside the pair. **For N=3 or N=4**, the focal set already covers a larger fraction of the industry, so the bar shifts: §5.8 covers the *next-tier* relevant names — for an N=3 Databricks-vs-Snowflake-vs-Oracle report, that's typically the three hyperscalers' native data+AI stacks (AWS Redshift+SageMaker, Google BigQuery+Vertex, Microsoft Fabric); for an N=3 EDA report, it's Siemens EDA + Arm + open-source / RISC-V; for an N=3 semicap report, it's TEL + KLA + ASML (whichever aren't already in the focal set). **A company is either in the focal N or in §5.8 — never both.** When the focal set already includes the obvious 3–4 leaders, §5.8 may shrink to 2–3 paragraphs covering specialists, regional alternatives, and adjacent-paradigm threats.

### Discovery — three sources, in this order

1. **10-K Item 1 / 年度报告 / Yuho competition section** of each side — quote the named competitor list verbatim. This is the authoritative starting point.
2. **Segment leaderboards** — IPnest (design IP), Gartner Magic Quadrant (enterprise software), IDC / IBISWorld (hardware), TrendForce (semis), IQVIA / EvaluatePharma (pharma), SemiAnalysis / SemiWiki (niche semi sub-segments), Wood Mackenzie / Rystad / S&P Global (energy / commodities).
3. **Recent industry-research notes** (last 12 months) that name the full vendor universe.

### Classification — every other player resolves to one of four buckets

| Bucket | Definition | How to surface |
|---|---|---|
| **Primary competitor** | Overlaps directly on at least one moat dimension where A or B holds a franchise. | Dedicated 100–300 word paragraph in §5.8 + column added to §5.3 / §5.4 / §5.5 tables wherever they meaningfully share. |
| **Adjacent player** | Overlaps on a smaller segment or different end-market. | One-sentence mention in §5.8 only; no table columns. |
| **Acquisition target** | Has been or will be absorbed by A or B during the comparison's reporting period. | Described as "now part of A" rather than as an independent player — note the close date and post-close segment. |
| **Domestic-market alternative** | Regional vendors limited by export controls, talent depth, or PDK access. | Call out as a §8 regional risk; no §5.8 paragraph. |

### Rank quality against the NAMED peer set, not in isolation

Once §5.8 has named the 3–7 other players, extend the §5 scoreboard's quality rows (profitability, margin, growth-quality) to those names so "best-in-class" is visible against real peers rather than asserted. Mirror Deutsche Bank's Huayan note, which ranks adjusted NPM against named peers in one line — Dobot −10%, UBTECH −35%, Geekplus 1%, Estun 0% — so the "most profitable HK-listed robot name" claim is checkable, not rhetorical. A focal name's "leading margin" means little until you've placed it on the same axis as the named competitors. Each peer number cites that peer's own filing (comparability caveat applies — flag GAAP vs non-GAAP, fiscal-end mismatches in-cell).

### Per-paragraph content for each Primary competitor

| Field | Source |
|---|---|
| What they do (one sentence) | Their own homepage / 10-K Item 1 Business |
| Where they overlap with A or B | Cross-reference to §5.4 (tool-level share) or §5.5 (IP share) |
| Estimated share of the overlapping segment | Third-party source (IPnest / Gartner / IDC / etc.) — never invent |
| Structural position | "Leader" (clear #1 in at least one sub-segment), "Specialist" (focused on one niche), "Challenger" (gaining share from incumbents) |
| Recent strategic moves | Last-12-months M&A, divestitures, leadership changes, major customer wins — cite press releases |
| Why they matter to the A-vs-B decision | One sentence: do they prevent A or B from claiming an entire segment? Are they an exit option for an acquirer? Are they the third option a customer would consider? |

### Worked example — SNPS vs CDNS (current production report)

The other-big-players survey in `reports/compare/SNPS_vs_CDNS.md` §5.8 covers:

- **Siemens EDA** (Primary, ~13% of EDA market) — owns Calibre physical verification at ~85% share; the structural #3 that holds the only sub-segment neither SNPS nor CDNS leads.
- **Arm Holdings** (Primary, ~40% of all design IP) — dominates CPU IP; the reason SNPS exited processor IP. Every non-Intel/AMD CPU design licenses from Arm.
- **Alphawave Semi** (Primary, ~3–4% of design IP) — interface IP specialist competing directly with SNPS on SerDes / PCIe; takeover target context.
- **Ansys** (Acquisition target → now part of SNPS) — was the #1 multi-physics vendor before the July 2025 close.
- **Hexagon AB Design & Engineering** (Acquisition target → closing into CDNS Q1 2026) — MSC Nastran + Adams; brings aerospace/auto OEMs into CDNS customer book.
- **Empyrean / X-EPIC / Primarius** (Domestic-market alternative — Chinese EDA) — collectively ~5–7% of China EDA market; structurally limited by Western EDA dependencies at advanced nodes.

### Failure modes

- Listing other players without explaining how they affect the A-vs-B choice → pointless context; expand the "why they matter" sentence or drop them.
- Treating §5.8 as a separate report → keep each Primary competitor's treatment to 100–300 words; readers came for A vs B, not A vs B vs C vs D vs E.
- Inventing players not in any cited source → every named other player must come from a 10-K competitor list or a third-party industry source.
- Forgetting to extend the §5.3 / §5.4 / §5.5 tables → the §5.8 paragraphs alone are not enough; the tables must visually show that the focal pair operates inside a larger ecosystem.
- All Primary competitors getting the same depth → vary the treatment by relevance. Siemens EDA in an SNPS-vs-CDNS comparison deserves 300 words because it's structurally a third co-equal; Schrödinger deserves one sentence.

## Verification checklist for the moat section

Before declaring §5 done:

- [ ] Every "share leader" / "dominant" / "industry-leading" claim has a third-party source, not a 10-K cite.
- [ ] Every customer-concentration percentage is pulled from a filing and verified (re-grep the source).
- [ ] Every foundry / channel / formulary certification is cited to the specific press release, not a homepage.
- [ ] Every segment market-share row has a source URL.
- [ ] No invented executive names, lawsuit titles, or product names.
- [ ] §5.7 has at least 3 bullets *each* side — symmetric honesty.
- [ ] **Every juxtaposed pair of numbers carries a comparability caveat where they aren't apples-to-apples** (fiscal-end mismatch, GAAP vs non-GAAP, single-arm vs controlled, organic vs M&A-inflated, segment-definition difference).
- [ ] **Quality rows (margin / profitability / growth) are ranked against the §5.8 named-peer set**, not asserted in isolation — each peer number cites that peer's filing.
- [ ] **§5.8 names 3–7 other big players** with the four-bucket classification labels visible. At least 3 are Primary competitors with 100–300 word paragraphs.
- [ ] **§5.3 / §5.4 / §5.5 tables extended** with columns for each Primary competitor that materially affects the share picture.
- [ ] The IP-roadmap inversion (or whatever structural shift in the period is most under-priced) is named explicitly in one of the eight subsections.
