# Investor-lens scorecards (optional Section 10 of the report)

Four named scoring rubrics that interpret the **same data already cited in Sections 1–9** through a specific value-investing framework. The lenses are analytical overlays, not persona role-play; their job is to give the reader a quick second opinion on the report's findings without re-running the research.

Adapted from the [LLMQuant investor-lens skill collection](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-investor-lenses) (MIT licensed).

## When to include this section

Include in any initiation-style company report where the audience is a buy/sell decision-maker. **Optional** for product-only / strategic-context reports where no investment recommendation is implied. When in doubt, include — the section is short (~600–1,000 words total) and gives the reader a structured second read of the evidence.

Skip if the user has explicitly said "no lens scorecards" / "skip Section 10" / similar.

## Output shape (in the report)

A new Section 10 — "**Investor-lens scorecards / 投资风格透视**" — placed **between Section 9 Risk Assessment and the References block**. Four subsections, ~150–250 words each:

- 10.1 Buffett scorecard (0–100 quality + price discipline)
- 10.2 Munger scorecard (0–10 weighted quality)
- 10.3 Damodaran scorecard (story-plus-numbers DCF margin of safety)
- 10.4 Howard Marks cycle posture (0–100 offense ↔ defense)

Each subsection structure:

1. **Verdict** — one-line bold verdict using the lens's verdict bands (e.g. `**Buffett verdict: Watchlist (score 62/100).**`).
2. **Scorecard table** — 3–5 row markdown table with the lens's components, the underlying number, and the contribution.
3. **Evidence** — 2–3 sentences naming the most load-bearing input(s), each carrying an inline citation to the same source already cited in Sections 1–9 (do not introduce new citations here — re-use what the report already established).
4. **Failure mode** — one sentence on what would flip the verdict the other way (a missing 10-K disclosure, a stale third-party number, a regime that doesn't fit the lens).

Verdict labels follow the existing analyst-view discipline: prefix with `*Lens view:*` (English) / `*视角观点:*` (Chinese). **Never** write "Buffett would buy this" / "巴菲特会买" / "Damodaran's fair value is $X" — these are scorecards through a named lens, not endorsements or replicas.

## The four lenses

### 10.1 Buffett scorecard — quality at a sensible price

**What it scores.** Whether the business is understandable, durably moated, well-managed, and available at a sensible price relative to long-term alternatives (the 10-year Treasury).

**Inputs (all already cited in earlier sections):**

| Component | Inputs from earlier sections |
|---|---|
| Business / circle of competence | Section 4 product description, Section 6 industry, Section 9 cyclicality / regulation risks |
| Moat | Section 4 differentiation paragraphs, Section 7 share / leadership claims, Section 5 customer-stickiness disclosures |
| Management | Section 3 founder + CEO bios (capital allocation track record, buyback / dividend / leverage history) |
| Valuation | Section 1 valuation snapshot — TTM P/E, FCF yield, 3-yr multiple band; 10Y yield from `indicators.db` |

**Score 0–100, equal-weighted 4 × 25:**

| Component | What earns it points | What docks it |
|---|---|---|
| **Business** (25) | Stable, predictable, low-regulatory-overhang, customer demand visible 10 yr ahead | Heavy cyclicality, technology-disruption exposure, opaque revenue mix |
| **Moat** (25) | Pricing power evident in margins, ROIC > WACC by ≥5 pts for 5+ yr, customer switching cost or scale advantage | Eroding share, gross-margin compression, commoditization, no obvious entry barrier |
| **Management** (25) | Founder-led or long-tenured CEO; buybacks at low multiples; dilution <2%/yr; clean balance sheet; M&A discipline | Frequent dilution, large M&A at high multiples, governance footers, unexplained executive turnover |
| **Valuation** (25) | FCF yield ≥ (10Y yield + 200 bp); P/E in lower half of 3-yr band; multiples ≤ sector median | FCF yield below 10Y; P/E in top decile of 3-yr band; multiples >2× sector median without clear growth premium |

**Verdict bands:**

- **75–100** → Holdable at the right price (`*Lens view:* Buffett-style holdable.`)
- **55–74** → Watchlist; quality or valuation gap remains.
- **Below 55** → Avoid for Buffett-style ownership.

**Failure modes to call out in the subsection:**

- A high score with no FCF history → the business hasn't proved it generates owner's earnings yet; valuation isn't legible.
- A high score with rapid product-cycle exposure (semicaps, biotech, consumer electronics) → outside the circle; flag explicitly.
- A high Management score with <5 yr CEO tenure → insufficient track record; downgrade to "watchlist".

### 10.2 Munger scorecard — weighted quality + inversion

**What it scores.** Same underlying data as Buffett, but weighted toward *durability of the business* over *price*, with a built-in inversion check ("what would have to be true for this thesis to fail?").

**Weighted scoring, 0–10 per component:**

| Component | Weight | What earns 10 | What earns 0 |
|---|---|---|---|
| Moat strength | 35% | Pricing power + ≥15% ROIC sustained 10 yr + clear structural advantage | Margin / share erosion or no observable moat |
| Management quality | 25% | Founder-led or long-tenured, capital-allocation track record visible | Frequent dilution, M&A at high multiples, governance flags |
| Business predictability | 25% | Income statement 10 yr forward describable within a factor of 2 | Heavy cyclicality, product-cycle dependency, regulatory overhangs |
| Valuation | 15% | FCF yield > 10Y + 200 bp; multiples ≤ sector median | FCF yield < 10Y, top-decile multiples without growth pace |

Compute weighted score: `Σ (component × weight)` → final 0–10 number.

**Verdict bands:**

- **≥ 7.5** → `*Lens view:* Munger-style holdable (high quality + acceptable price).`
- **5.5–7.4** → Neutral; mixed evidence.
- **≤ 5.4** → Avoid for Munger-style ownership.

**Inversion check (mandatory sentence in the subsection):** name the single scenario that most plausibly destroys the thesis (customer concentration breaking, technology transition, regulatory action, capital structure stress). If you can't name one, you haven't inverted hard enough — go back to Section 9.

**Failure modes:**

- Score ≥7.5 with valuation in the top decile → quality is real but you're paying full price; downgrade to neutral.
- High moat score sourced only to the subject's 10-K Competition section (not third-party share data) → relabel as `*Analyst view:*`, not a Munger-confirmed moat.

### 10.3 Damodaran scorecard — story-plus-numbers DCF

**What it scores.** Whether the report's narrative implies a defensible intrinsic value and how that value compares to today's market cap.

**Three components, score out of 8 total:**

| Component | Max | Inputs |
|---|---|---|
| Growth & reinvestment | 4 | Revenue CAGR (Section 1), ROIC (Section 1 valuation snapshot or Section 9 financials), reinvestment rate = revenue growth ÷ ROIC. Penalize when reinvestment > 100% (no FCF). |
| Risk profile | 3 | Beta (yfinance), debt/equity (Section 1), interest coverage. Penalize <2× coverage or D/E > 1 unless industry norm. |
| Relative valuation | 1 | TTM P/E vs 3-yr median; sector multiple percentile (Section 1 valuation snapshot). |

**Margin of safety** is the primary verdict — derive an intrinsic-value range from the report's own growth/margin/Rf assumptions, then compare to current market cap:

`MoS = (Intrinsic value − Market cap) / Market cap`

- `Rf` → 10Y Treasury from `indicators.db` (`tnx`), state the as-of date inline.
- `ERP` → state assumption (5.0% is Damodaran's published default for developed markets; cite his published estimate if available — if not, just state the assumption).
- `Terminal growth` → must be ≤ `Rf`; never above the risk-free rate.

**Verdict bands:**

- **MoS ≥ +25%** → `*Lens view:* Damodaran-style bullish (margin of safety sufficient).`
- **MoS between −25% and +25%** → Neutral; price-and-value close.
- **MoS ≤ −25%** → Bearish; price exceeds story-supported value.

**Required explicit assumptions block** (in the subsection):

```
Revenue CAGR (5 yr → terminal): X% → Y%
Operating margin (terminal): Z%
Reinvestment rate: W% (= growth / ROIC)
WACC: AA% (= Rf BB% + beta CC × ERP 5.0%)
Terminal growth: DD% (≤ Rf)
Intrinsic value range: $E–F B
Market cap (as of YYYY-MM-DD): $G B
Margin of safety: ±H%
```

**Failure modes:**

- Terminal growth > `Rf` → fix it (cap at `Rf`) and re-score.
- WACC plug with no defended components → list each component and where it came from.
- Reinvestment > 100% with bullish verdict → contradiction; you're claiming growth without funding it.

### 10.4 Howard Marks cycle posture — market regime, not company-specific

**What it scores.** Where the market itself sits on the offense/defense spectrum, regardless of the company. Useful sanity check on Section 1's valuation snapshot — a high-quality company can still be a bad entry point in a euphoric regime.

**This is the only lens that does NOT depend on company-specific evidence.** It's a market-cycle overlay that contextualizes the other three.

**Inputs — all from `indicators.db` (FRED + yfinance):**

| Component | Source | What 0 (panic) looks like | What 100 (euphoria) looks like |
|---|---|---|---|
| Volatility | `vix` snapshot | VIX > 35 sustained | VIX < 13 sustained |
| Credit spreads | `hy_oas` (FRED BAMLH0A0HYM2) | HY OAS > 700 bp | HY OAS < 300 bp |
| Rates regime | `tnx` snapshot vs 5-yr range | Bottom decile of 5-yr range | Top decile of 5-yr range |
| Market valuation | S&P 500 trailing P/E vs 10-yr percentile | < 25th percentile | > 75th percentile |
| Sentiment / breadth | AAII Bull−Bear; market breadth (% > 200-day MA) | Bearish, breadth < 30% | Bullish, breadth > 80% |

Map each component to 0–100, take a simple average for the headline score, and report the components separately so disagreements are visible.

**Posture bands:**

- **0–24** → Hard offense (`*Lens view:* fear regime — add risk if other lenses agree`).
- **25–39** → Offense.
- **40–59** → Neutral.
- **60–74** → Defense.
- **75–100** → Hard defense (`*Lens view:* euphoria regime — trim risk regardless of company-specific verdict`).

**Required contrary-evidence note:** name one component that argues against the headline score (e.g. "VIX at 14 says complacency, but HY OAS at 540 bp says credit market disagrees"). If all five components agree, say so — that's itself the signal.

**Failure modes:**

- Using the cycle score as a market-timing guarantee → it's a regime label, not a date.
- Forcing offense or defense when components conflict → the report should say "mixed" and explain the disagreement, not synthesize a compromise number.

## Guardrails (apply to all four lenses)

- **Never invent inputs.** Every number in a scorecard table must already be cited somewhere in Sections 1–9 of the same report, or come from `indicators.db` with an as-of date stated inline. If a required input is missing, write `not disclosed` in the cell and downgrade the score for that component — don't substitute a plausible-looking estimate.
- **Never claim the lens-namesake "would buy" this stock.** The verdict is the *scorecard's* output, not the named investor's endorsement. Use `Buffett-style scorecard verdict: ___` (not `Buffett would: ___`).
- **Re-use existing citations.** A lens subsection that introduces new inline citations means you skipped Sections 1–9 evidence — go back and use what's already cited. The only new citation each lens may legitimately introduce is the one for the cycle inputs from `indicators.db` (state the as-of date).
- **Separate facts from interpretation.** The Scorecard table is interpretation; the Evidence sentence chain (with citations) is fact. Keep them visually distinct.
- **Disagreement across lenses is information, not a defect.** If Buffett says Avoid (poor valuation) but Damodaran says Bullish (story supports MoS > 25%), call it out — that disagreement is more useful than a forced consensus.
- **Stale-data discipline.** Cycle inputs older than 30 days → re-pull from `indicators.db` and re-score. Valuation inputs older than 3 trading days → flag as stale.
- **No "Source: our model"** — applies here as much as anywhere else in the report. The scorecards are framework-driven scores, not new model output.

## Implementation tips

- Pull the indicator snapshot once at the top of Section 10 and reference it across all four lenses (`indicators.db` snapshot as of YYYY-MM-DD: VIX = `__`, 10Y Treasury = `__`, HY OAS = `__`).
- The cycle posture (10.4) should be **computed first** because it gates the verdicts above — a defensive cycle should mute "Bullish" verdicts in lenses 10.1–10.3 (note the disagreement explicitly).
- Place the section between Section 9 Risk Assessment and the References block in both the English and Chinese reports — same lens, two natively-written prose passes (not a literal translation).
- Section 10 word count: **600–1,000 words total** (150–250 per lens). Significantly shorter than Section 4 / Section 6; this is a verdict summary, not new analysis.

## What this section does NOT do

- It does not replace Section 9 (Risk Assessment) — the lenses are second opinions on quality and price, not a structured risk decomposition.
- It does not substitute for a price target or recommendation — those come from [[trader-plan]] and [[portfolio-decision]] in the trading-analysis pipeline. The lens scorecards are inputs to that decision, not its output.
- It does not introduce new data sources beyond what Sections 1–9 cited + the `indicators.db` cycle snapshot — if a lens needs an input that wasn't already gathered, the right fix is to go back and gather it in the right section, not to one-shot-cite it inside Section 10.
