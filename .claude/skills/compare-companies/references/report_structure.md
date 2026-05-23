# Compare-companies — Report Structure

The final report has 10 sections plus a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **5,000–9,000 words**. The moat anatomy (§5) is the longest section and the analytical centerpiece; if it ends up shorter than any other section, the priority is wrong.

Embed **4–8 visuals** (Mermaid blocks + 1–2 matplotlib PNGs for quantitative trends). Every chart gets a citation directly below.

## Per-section spec

### §1 — One-line self-description (200–400 words)

A side-by-side table of each company's own framing taken verbatim from their most recent 10-K / 年度报告 / Yuho Item 1 Business:

| | Company A | Company B |
|---|---|---|
| Framing (verbatim from 10-K) | "..." | "..." |
| Tagline | ... | ... |
| Implicit pivot | ... | ... |

One follow-up paragraph: what is each side trying to signal with its framing, and what's the implicit pivot from a prior self-description (5–10 years ago)? Cite each side's 10-K Item 1 Business with a deep URL.

### §2 — Strategic pillars (200–400 words)

A `mermaid timeline` block showing each side's current strategic pillars side-by-side (often each company publishes 3–5 pillars in its 10-K Strategy section or annual letter). Below the timeline, a 1–2 paragraph comparison: who has the more crisply marketed doctrine, what's been added or sunset since the prior year, whether the pillars are operational ("lead, grow, scale") or product-led ("AI in every workflow").

### §3 — AI narrative — tool vs. tailwind (300–500 words)

The single most-asked comparison question in 2025–2026. Side-by-side table:

| Lens | Company A | Company B |
|---|---|---|
| AI-as-tool (using AI internally) | ... named products | ... named products |
| AI-as-tailwind (selling into AI demand) | ... segments | ... segments |

Cite each side's specific AI product pages and AI-investor-day language. Avoid generic AI-bull boilerplate — name the products and the verticals.

### §4 — Segment structure & financial scoreboard (400–600 words)

A `mermaid xychart-beta` bar chart of FY revenue by segment for each side (so the segment-mix difference is visible at a glance). Then a financial scoreboard table:

| Metric | A (latest FY) | B (latest FY) | Spread / Note |
|---|---|---|---|
| Total revenue | ... | ... | ... |
| YoY growth (and organic ex-M&A if relevant) | ... | ... | ... |
| Operating income / margin | ... | ... | ... |
| RPO / backlog | ... | ... | ... |
| China revenue (if material) | ... | ... | ... |
| Other regionally material lines | ... | ... | ... |

Then a paragraph per side walking the segment structure with citation to the segment-reporting note in the 10-K.

### §5 — The moat anatomy (1,500–2,500 words) — THE LONGEST SECTION

Seven subsections. **See `references/moat_anatomy.md` for the per-subsection content spec.** Headline subsections (each ~200–400 words):

- 5.1 Customer concentration — both just diversified, but for opposite reasons
- 5.2 Backlog and recurring mix — both fortress-grade
- 5.3 Channel / foundry / distribution lock-in
- 5.4 Tool-level / sub-segment market share — where the de-facto monopolies live
- 5.5 IP / patent / data-corpus franchise share
- 5.6 Why a customer picks one over the other
- 5.7 Cracks worth naming on each side

**Required deliverable 1 (product overlap matrix)** sits inside this section as §5.1 or just before — see `references/product_overlap_matrix.md`.

### §6 — The big bet (400–600 words)

What is each side doing *right now* to expand TAM beyond the moat? M&A, organic R&D, capital deployment, geographic expansion. A side-by-side table contrasting the strategy (e.g. "one mega-deal" vs "many bolt-ons"), plus narrative on what each is buying and what it implies for the next 24 months. Cite the M&A press releases, S-4s, 8-Ks, and the most recent 10-K language on integration risk.

### §7 — Capital allocation (300–500 words)

Side-by-side table of debt level, buyback authorization remaining, dividend, recent M&A spend, next-24-month capital optionality, effective tax rate. Then a one-paragraph translation per side: what is the capital-allocation posture actually telling the reader?

### §8 — Distinctive risks (300–500 words)

A side-by-side risk table covering the dimensions where the two sides materially diverge: customer concentration, integration risk, debt overhang, regulatory exposure (US export-control, EU AI Act, FDA, antitrust), domestic competitor density, currency mix, etc. Avoid the standard 10-K risk-factor catalogue — focus only on differences.

### §9 — Side-by-side scorecard (Required deliverable 4) (200–400 words; mostly a table)

A flat 3-column markdown table with 15–25 rows. Every row has Dimension | Edge | Why. Banned in the Edge column: "arguably", "slightly", "potentially", "depends". Allowed: one side's name, "Tied", or "Neither".

The scorecard's job is to give a senior reader a 60-second overview. Lead with the strongest moat dimensions; cover financial, product, channel, balance-sheet, and overhang dimensions.

### §10 — Bottom line — two different bets (Required deliverable 5) (300–500 words)

Two strategic paragraphs:

1. "Company A is betting that **X** matters more than **Y**" — distill A's posture, name the downside scenario.
2. "Company B is betting that **X** matters more than **Y**" — same shape, opposite framing.

Then a closing paragraph that names **the specific catalyst** (event, date, KPI) that will move the verdict in the next 4–8 quarters. Avoid both-sidesism ("both can win", "depends on execution"). Name the catalyst.

### References (no word count)

Deduplicated, grouped:

- Primary filings — Company A (CIK / stock-code)
- Primary filings — Company B
- Industry research (third-party share data — IPnest, Gartner, IDC, IBISWorld, TrendForce, etc.)
- Press / regulatory (press releases, DOJ / SEC / EU actions, court filings)
- Other commentary (SemiAnalysis, SemiWiki, In Practise, Wing VC, etc.)

Every entry is a markdown link with a date in the title where the source has a publication date.

## Tables and charts checklist

- [ ] §1 framing table (verbatim 10-K language)
- [ ] §2 mermaid timeline of strategic pillars
- [ ] §3 AI side-by-side (tool / tailwind)
- [ ] §4 revenue mermaid bar chart + scoreboard table
- [ ] §5.1 product overlap matrix (DIRECTLY COMPETE / COMPLEMENTARY / NON-OVERLAPPING)
- [ ] §5.1 customer concentration table side-by-side (top-1 / top-5 / >10%)
- [ ] §5.2 backlog / recurring mix table
- [ ] §5.3 foundry-node × vendor matrix (semis) OR channel matrix (consumer/SaaS) OR formulary matrix (pharma)
- [ ] §5.4 tool-level segment share table
- [ ] §5.5 IP franchise share table
- [ ] §6 M&A / capital-allocation table
- [ ] §7 debt / buyback / dividend table
- [ ] §8 distinctive risks table
- [ ] §9 scorecard table

If a comparison runs in a non-semis domain (consumer brands, biotech, industrial), adapt §5.3 to channel partners / payer formularies / OEM design-ins instead of foundry certifications. The structural question — *what makes a customer's switch costly* — is the same.

## Worked example: SNPS_vs_CDNS (May 2026 rewrite)

The current production example of this skill's output is `reports/compare/SNPS_vs_CDNS.md` (387 lines, ~8,500 words). It follows this template exactly and is the reference for what "done" looks like. When unsure about depth, density, or table format, open that file.
