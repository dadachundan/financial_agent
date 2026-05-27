# Compare-companies — Report Structure

The final report has a TL;DR section + 10 numbered sections + a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **5,000–9,000 words**. The moat anatomy (§5) is the longest section and the analytical centerpiece; if it ends up shorter than any other section, the priority is wrong.

Embed **4–8 visuals** (Mermaid blocks + 1–2 matplotlib PNGs for quantitative trends). Every chart gets a citation directly below.

**Bilingual reminder.** By default, the skill produces both English (`<A>_vs_<B>.md`) and Simplified Chinese (`<A>_vs_<B>_zh.md`) editions. This structure spec applies to **both** files — same 10-section skeleton, same word-count target, same chart count. The structural skeleton stays identical; only the prose language differs. Section headers translate (e.g. `## §5 The moat anatomy` ↔ `## §5 护城河剖析`); citation URLs are identical between files; link titles preserve original language (`10-K` stays `10-K` in both, `年度报告` stays `年度报告` in both). See the SKILL.md "Report language" section for the bilingual workflow rules.

## Per-section spec

### §0 — TL;DR — At-a-glance advantages and disadvantages (~250 words) — REQUIRED FIRST SECTION

**Placement: directly after the source-filings block, before the first `---` separator and before §1.** This is the first thing the reader sees, and for most readers it's the only thing they'll read end-to-end. Treat it as the headline of the report.

**Format — a 3-column markdown table:**

```markdown
## TL;DR — At-a-glance advantages and disadvantages

|  | ✓ Advantages | ✗ Disadvantages |
|---|---|---|
| **Company A (TICKER)** | • <bullet> (§N)<br>• <bullet> (§N)<br>• ... (5–8 bullets) | • <bullet> (§N)<br>• <bullet> (§N)<br>• ... (5–8 bullets) |
| **Company B (TICKER)** | • <bullet> (§N)<br>• ... (5–8 bullets) | • <bullet> (§N)<br>• ... (5–8 bullets) |

**Who is each one for?** <one-paragraph distillation framing the choice as: pick A for X, pick B for Y, or run both because Z>. The detailed evidence for every TL;DR claim follows in §1–§10 below.
```

**Per-bullet rules:**

- Lead with a number or specific noun, not an adjective. `$13.5B debt locks buyback for ~2 years (§7)` beats `Heavy debt load`.
- End with a `(§N)` section reference so a skimmer can drill straight into the evidence section.
- 5–8 bullets per cell. Fewer than 5 = under-explored; more than 8 = padding.
- Symmetric honesty: Disadvantages cell must have at least (Advantages count − 2) bullets. If you found 7 advantages and 1 disadvantage, you didn't look hard enough at §5.7 Cracks.
- No hedge words ("arguably", "potentially", "may", "could").
- No analyst self-references ("our model", "estimate", "本模型").
- Bold the most important compound noun phrase in each bullet (`**$13.5B debt locks buyback for ~2 years**`) so the table scans at a glance.

**"Who is each one for?" paragraph — required:**

Three sharp options: pick A for ___, pick B for ___, or *both* (the dual-vendor reality common in duopolies). Avoid both-sidesism ("both have merit") — the reader came for a recommendation framework, not equivocation.

**Worked example:** [`reports/compare/SNPS_vs_CDNS.md`](../../../../reports/compare/SNPS_vs_CDNS.md) — the canonical TL;DR for SNPS vs CDNS, with 7 advantages × 6 disadvantages per side, all referenced into §1–§10.

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

### §5 — The moat anatomy (1,800–3,000 words) — THE LONGEST SECTION

**Eight** subsections. **See `references/moat_anatomy.md` for the per-subsection content spec.** Headline subsections (each ~200–400 words, except §5.8 which scales with the number of other players covered):

- 5.1 Customer concentration — both just diversified, but for opposite reasons
- 5.2 Backlog and recurring mix — both fortress-grade
- 5.3 Channel / foundry / distribution lock-in **(extend tables with columns for each Primary competitor)**
- 5.4 Tool-level / sub-segment market share — where the de-facto monopolies live **(extend tables with columns for each Primary competitor that leads a sub-segment)**
- 5.5 IP / patent / data-corpus franchise share **(extend tables with the dominant non-focal-pair player — e.g. Arm in design IP)**
- 5.6 Why a customer picks one over the other
- 5.7 Cracks worth naming on each side
- **5.8 Other big players in this space (NEW — Required deliverable 6)** — 3–7 other meaningful players named, each Primary competitor gets a 100–300 word paragraph; classified as Primary / Adjacent / Acquisition target / Domestic-market alternative.

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

- [ ] **§0 TL;DR table** (3-col advantages/disadvantages) — placed before §1
- [ ] **§0 "Who is each one for?" paragraph** — three sharp options, no both-sidesism
- [ ] §1 framing table (verbatim 10-K language)
- [ ] §2 mermaid timeline of strategic pillars
- [ ] §3 AI side-by-side (tool / tailwind)
- [ ] §4 revenue mermaid bar chart + scoreboard table
- [ ] §5.1 product overlap matrix (DIRECTLY COMPETE / COMPLEMENTARY / NON-OVERLAPPING)
- [ ] §5.1 customer concentration table side-by-side (top-1 / top-5 / >10%)
- [ ] §5.2 backlog / recurring mix table
- [ ] §5.3 foundry-node × vendor matrix (semis) OR channel matrix (consumer/SaaS) OR formulary matrix (pharma) **— with column for each Primary competitor**
- [ ] §5.4 tool-level segment share table **— with column for each Primary competitor that leads a sub-segment**
- [ ] §5.5 IP franchise share table **— with the dominant non-focal-pair player included**
- [ ] **§5.8 other-big-players section** with 3–7 named, each Primary competitor in a 100–300 word paragraph, classification labels visible
- [ ] §6 M&A / capital-allocation table
- [ ] §7 debt / buyback / dividend table
- [ ] §8 distinctive risks table
- [ ] §9 scorecard table

If a comparison runs in a non-semis domain (consumer brands, biotech, industrial), adapt §5.3 to channel partners / payer formularies / OEM design-ins instead of foundry certifications. The structural question — *what makes a customer's switch costly* — is the same.

## Worked example: SNPS_vs_CDNS (May 2026 rewrite)

The current production example of this skill's output is `reports/compare/SNPS_vs_CDNS.md` (387 lines, ~8,500 words). It follows this template exactly and is the reference for what "done" looks like. When unsure about depth, density, or table format, open that file.
