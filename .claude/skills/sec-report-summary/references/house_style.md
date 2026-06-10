# Sell-side house style — durable patterns for the SEC filing digest

Style anchors mined from how the major desks construct a "results review /
read-across" note. Named **report series only** — never hardcode file_ids
(they churn). Apply these to the multi-year SEC filing summary; they keep
SKILL.md lean while giving a concrete form to copy.

## 1. Thesis-first opener

Open with a 2–4 sentence synthesized stance (constructive / cautious / mixed
+ the single reason), THEN the detail. Never lead with raw per-period bullets.

- **GS "results review" / "results read-across"** — thesis-first opening, then
  the beat/miss and the deltas.
- **Citi "China Internet 1Q26 Wrap & Outlook"** — backward recap paired with an
  explicit forward outlook in the same note.

For a filing digest, the "thesis" is the single most important multi-year shift
+ its direction + the 2–3 deltas that drive it. Filing-sourced only.

## 2. Magnitude + driver in one clause

Every delta carries its driver in the same clause — magnitude AND cause, never
one without the other.

- **GS NC-company results** — "OP +4% YoY, increase limited by ¥8.4bn higher
  stock-comp"; "Auto revenue −4% YoY, first decline in six years, as OEMs cut
  IT capex".
- **J.P. Morgan "Another strong beat in FX reserves"** — decompose a beat/miss
  into its components (exports strong + imports soft + price up), not just the
  aggregate.

## 3. Track everything OLD → NEW

The product is "what changed vs the last snapshot." Render estimates, guidance,
payout ratio, fwd P/E, EPS CAGR, capex as `old → new`.

- **Bernstein estimate-revision notes** ("raising 2026 demand to 2.6 TWh, +45%";
  "capex guidance raised 8pp") — state old→new explicitly, each tied to a driver.
- **GS "Index Rebalancing Review"** — "fwd P/E 16.6x → 16.7x, EPS CAGR 13.7% →
  13.9%" — the what-changed-vs-last-snapshot delta IS the deliverable.

## 4. Forward outlook is not optional

Pair the backward results recap with the forward half in the same note.

- **UBS "AGM takeaways: 2030 strategy & 2026 outlook"** — pit the multi-year
  strategic target (2030 volume / profit / payout-ratio goals) against the
  current-year guidance to show trajectory, not just a point estimate.
- **Citi "Wrap & Outlook"** — segment-by-segment forward outlook with a named
  catalyst / inflection per segment.

For a 10-K (which carries less explicit guidance than a call), mine the Item 7
MD&A "Outlook" / "Trends" subsection and any 8-K Item 2.02 exhibit.

## 5. Threshold-crossing callouts as the headline signal

Surface inflection points where a metric crosses a meaningful line — the most
decision-useful read of a multi-year filing.

- **Nomura BABA/BIDU "Takeaways from NIFA conference"** — "Baidu AI revenue 52%
  of core, first time >half; +49% YoY" — the mix-shift-crossing-a-threshold
  narrative, exactly a 10-K segment-evolution story.
- **GS NC-results** — "first decline in six years".

Rank the Changes section by thesis-impact; lead with these crossings and
explicitly down-rank boilerplate.

## 6. Segment delta table as the spine

Render a compact structured table (segment × this FY / last FY / YoY% / driver)
BEFORE the prose, with charts hanging off it.

- **GS "results read-across" / NC-company blocks** — each segment is a tight,
  self-contained block with its own metric + driver + forward inflection.

## 7. Risk-factor evolution rigor

Diff Item 1A vs the prior year; classify each material change ADDED / DROPPED /
ESCALATED, name the category (cyber, AI / AI-regulation, tariffs, climate,
supply concentration, litigation), and flag net-new categories by name + first
year of appearance.

## 8. Keep third-party forecasts separate

Industry forecasts (Yole / TrendForce / Kioxia / Gartner) are labeled supporting
anchors only — kept visually separate from the company's own reported numbers,
never blended into a filing citation.

## Style discipline (cross-cutting)

- Lead with the consequence, support with the number — desk-read density, no
  throat-clearing.
- Use explicit directional verbs: raised / cut / added / dropped / escalated —
  never vague "evolved".
- State the comparison baseline every time ("vs FY24", "first time since 2021")
  so a number is never context-free.
- Name dated catalysts / inflections (breakeven fiscal year, regulatory
  effective date) rather than "in the future".
- **Further viewing** — 1–3 validated explainer videos for hard-to-visualize
  concepts (the product / manufacturing process, an unfamiliar business model),
  in their own slot, never a citation, never carrying a number (see SKILL.md).
