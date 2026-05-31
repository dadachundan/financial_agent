# Investor-lens scorecards (optional Section 10 of the report)

Four named scoring rubrics that interpret the **same data already cited in Sections 1–9** through a specific value-investing framework. The lenses are analytical overlays, not persona role-play; their job is to give the reader a quick second opinion on the report's findings without re-running the research.

Adapted from the [LLMQuant investor-lens skill collection](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-investor-lenses) (MIT licensed).

## When to include this section

Include in any initiation-style company report where the audience is a buy/sell decision-maker. **Optional** for product-only / strategic-context reports where no investment recommendation is implied. When in doubt, include — the section is short (~600–1,000 words total for the default four lenses) and gives the reader a structured second read of the evidence.

Skip if the user has explicitly said "no lens scorecards" / "skip Section 10" / similar.

## Output shape (in the report)

A new Section 10 — "**Investor-lens scorecards / 投资风格透视**" — placed **between Section 9 Risk Assessment and the References block**.

**Default (the four core lenses)** — included whenever Section 10 is on:

- 10.1 Buffett scorecard (0–100 quality + price discipline)
- 10.2 Munger scorecard (0–10 weighted quality)
- 10.3 Damodaran scorecard (story-plus-numbers DCF margin of safety)
- 10.4 Howard Marks cycle posture (0–100 offense ↔ defense)

**Optional packs (sections 10.5–10.9)** — include when the report's character calls for them. Each pack is ~150–250 additional words per lens; the user can request any subset by name ("include the Lynch lens", "include the Burry lens", "use the growth pack"), or the analyst can include them based on the company's fit (see "When each optional lens is most useful" below).

| Lens | Pack | When most useful |
|---|---|---|
| 10.5 Lynch GARP | Growth | Mid-cap consumer / industrial growers, ten-bagger candidates, PEG-anchored stories |
| 10.6 Fisher scuttlebutt | Growth | Compounders with multi-decade runway; reports that already cite customer/ex-employee/supplier evidence |
| 10.7 Burry forensic deep value | Distressed / contrarian | Hated sectors, suspected value traps, balance-sheet-led theses |
| 10.8 Druckenmiller liquidity-regime | Macro | Asymmetric setups where macro liquidity is the dominant variable (rate-sensitive sectors, cyclicals at inflection, regime-bound theses) |
| 10.9 Cathie Wood Wright's Law | Growth | Hard-to-DCF disruption stories (AI, robotics, EV, genomics, energy storage); reports where five-year TAM is the main story |

When the optional packs are included, the verdict labels follow the same `*Lens view:*` / `*视角观点:*` convention. **Never write `Lynch would buy`, `林奇会买`, `Burry would short`, `Cathie Wood projects X`, etc.** — these are scorecards through a named framework, not endorsements.

**Each subsection (core or optional) follows the same shape:**

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

## Optional lens packs (10.5–10.9 — include on request or by fit)

Each optional lens is ~150–250 words in the report and follows the same verdict-first shape as the core four. Default Section 10 includes 10.1–10.4 only; the lenses below are added when the company's character calls for them (see the routing table in "Output shape" above) or when the user asks by name.

### 10.5 Lynch GARP — growth-at-a-reasonable-price + ten-bagger discipline

**What it scores.** Whether the company's growth is fairly priced (PEG-anchored), the underlying story is simple enough to tell in two minutes, the balance sheet is clean, and the stock's Lynch category is consistent with the report's framing.

**Lynch's six categories (the analyst must pick one, on the record):**

| Category | Typical signature | Lynch's pricing rule |
|---|---|---|
| Slow grower | Mature, dividend-paying, <5% revenue growth | Yield + safety; PEG less relevant |
| Stalwart | Large, predictable ~10% grower | PEG 1.0–1.5 acceptable |
| Fast grower | 20–25%+ revenue growth, ten-bagger hunting ground | PEG ≤ 1.0 strong; > 2.0 weak |
| Cyclical | Auto / steel / chemicals; profits swing with cycle | Buy near cyclical trough P/E (not peak); avoid the value-trap of peak EPS |
| Turnaround | Recovery from distress | Watch for inflection signals; size small until thesis confirms |
| Asset play | Hidden real estate / patents / cash | Book value > market cap with catalyst |

**Inputs (already cited in earlier sections):**

| Component | Inputs |
|---|---|
| Growth analysis | Section 1 revenue CAGR + most-recent quarter print; Section 6 industry growth |
| Valuation (PEG, P/E) | Section 1 valuation snapshot — TTM P/E + revenue/EPS growth forward estimate; PEG = P/E ÷ growth rate |
| Fundamentals | Section 1 D/E (target <0.5), FCF positive, net cash bonus |
| Sentiment | Section 9 if it covers institutional ownership; otherwise note "institutional ownership data not in this report" |
| Insider activity | DEF 14A / Form 4 disclosures; if not in the report, write `insider activity not pulled` and downgrade by 1 point |

**Scoring, weighted 0–10:**

- Growth analysis — 30%
- Valuation (PEG, P/E vs growth) — 25%
- Fundamentals (debt, margins, FCF) — 20%
- Sentiment — 15%
- Insider activity — 10%

**Verdict bands:**

- **≥ 7.5** → `*Lens view:* Lynch-style GARP candidate.`
- **4.5–7.4** → Neutral.
- **≤ 4.4** → Avoid for Lynch-style ownership.

**Required category statement (mandatory sentence in the subsection):** "This is a <category>" with one sentence of evidence. If the analyst cannot pick a category cleanly, that itself is a Lynch failure — the framework requires the prior categorization.

**Failure modes:**

- Fast-grower verdict with PEG > 2.0 → contradictory; the rule is the rule, downgrade.
- "Cheap cyclical" thesis at peak EPS → cyclical-trap warning; the bull verdict requires trough-cycle pricing.
- Story you can't tell in two minutes → the lens fails by Lynch's own criterion; relabel as analyst view.

### 10.6 Fisher scuttlebutt — qualitative 15-point growth checklist

**What it scores.** Whether the company passes Fisher's structural 15-point screen, with extra weight on qualitative evidence ("scuttlebutt") that goes beyond filings — customer interviews, ex-employee accounts, supplier perspectives, competitor concessions.

**Fisher's 15 points (the screen)** — pulled from his original framework, scored across:

- Product/service runway for multi-year sales growth (Section 4 + Section 6).
- Management long-term orientation (Section 3 founder/CEO tenure + capital allocation history).
- R&D investment with track record of commercial output (Section 4 — does each product have a launch date and revenue trajectory?).
- Sales organization quality (Section 5 customer-acquisition discipline).
- Profit margins, maintainable / improvable (Section 1 multi-year trend).
- Labor / personnel relations (typically not in Section 9 unless governance issues exist — flag absence).
- Executive depth beyond CEO (Section 3 limits to CEO + founder; flag explicitly that Fisher's depth check is incomplete in this report).
- Accounting quality (Section 9 if there's a footnote concern).
- Long-range earnings outlook vs quarter-chasing (Section 6 + management's stated guidance horizon).
- Equity financing dilution risk (Section 1 share-count trend).
- Management honesty about setbacks (Section 3 — does the report quote any management discussion of recent misses or pivots?).

**Inputs (already cited in earlier sections):** Section 3 (management), Section 4 (R&D + product runway), Section 5 (sales/customer org), Section 6 (industry runway), Section 1 (margins + financial trend), Section 9 (risks for accounting / governance issues).

**Scoring, weighted 0–10:**

- Growth & quality — 30%
- Margins & stability — 25%
- Management efficiency — 20%
- Valuation — 15%
- Insider activity — 5%
- Sentiment — 5%

**Verdict bands:**

- **≥ 7.5** → `*Lens view:* Fisher-style outstanding company (multi-year hold candidate).`
- **4.5–7.4** → Neutral.
- **≤ 4.4** → Below Fisher's bar.

**Required scuttlebutt note (mandatory sentence in the subsection):** name at least one cited piece of evidence that came from outside the filings — a customer interview / case study, an ex-employee quote, a supplier interview, a competitor concession, an industry-conference takeaway. If only filings are cited, **downgrade the score by 1 point** and explicitly write "no scuttlebutt-style evidence in this report; Fisher's qualitative depth check incomplete."

**Failure modes:**

- "Bargain-price" thesis → Fisher does not insist on bargain pricing; downgrade if the bull verdict depends on a low multiple.
- Pure-filings-only with no qualitative depth → the lens degrades to "Buffett-style scorecard"; relabel.
- Score ≥ 7.5 with high share-issuance trend → Fisher penalizes dilutive financing; downgrade by 1 point.

### 10.7 Burry forensic deep value — hated sector + strong balance sheet + downside-first

**What it scores.** Whether the setup is genuinely contrarian (sector / name is hated by consensus) AND fundamentals are strong (FCF yield, balance sheet) AND the downside is explicitly bounded by a defensible balance sheet.

**Inputs (already cited in earlier sections):**

| Component | Inputs |
|---|---|
| Value (FCF yield, EV/EBIT) | Section 1 valuation snapshot — FCF yield + EV/EBIT (compute from EV ÷ TTM EBIT if not stated explicitly) |
| Balance sheet | Section 1 D/E + net cash position |
| Insider activity | DEF 14A / Form 4 (cited in Section 3 if covered); if not pulled, write `insider activity not pulled` |
| Contrarian sentiment | Section 6 industry sentiment + Section 9 narrative — count of negative consensus headlines (last 90 days) AND a fundamentals-hold check |

**Scoring (sum to 12):**

| Component | Max | Rule |
|---|---|---|
| Value (FCF yield, EV/EBIT) | 6 | FCF yield ≥ 15% = 6; ≥ 12% = 5; ≥ 8% = 4; < 8% = 0–3 |
| Balance sheet (D/E, net cash) | 3 | D/E < 0.5 = 3; < 1.0 = 2; ≥ 1.0 = 0–1; net cash → cap at 3 |
| Insider activity | 2 | Insider buying in last 90 days = 2; only stock grants = 0; net selling = 0 |
| Contrarian sentiment | 1 | ≥ 3 negative consensus signals in last 90 days AND fundamentals hold = 1 |

**Verdict bands (scaled):**

- **≥ 9/12 (75%)** → `*Lens view:* Burry-style forensic value candidate.`
- **5–8/12** → Neutral.
- **≤ 4/12** → Below Burry's bar.

**Required downside-first paragraph (mandatory in the subsection):** name the single worst-defensible scenario from Section 9, and explain how the balance sheet survives it (or doesn't). If the report cannot articulate this, **the lens cannot return bullish** — downgrade to neutral with the reason stated.

**Failure modes:**

- "Loved sector + cheap on multiple" → not Burry; the discount is structural, not contrarian. Use Buffett or Damodaran instead.
- Bullish verdict without the downside-first paragraph → contradicts Burry's discipline; force downgrade.
- Buying because management is forecasting a turnaround → Burry ignores management's forecast; cite filings only.
- High FCF yield with deteriorating revenue → cash today doesn't guarantee cash tomorrow; check the trajectory before scoring.

### 10.8 Druckenmiller liquidity-regime — macro liquidity + asymmetric sizing + same-day exit

**What it scores.** Whether the macro liquidity regime supports adding risk, whether the position fits an asymmetric (3:1+) risk/reward setup, and whether the analyst can name a specific same-day-exit trigger.

**Inputs (already cited in earlier sections):**

| Component | Inputs |
|---|---|
| Growth / momentum | Section 1 revenue acceleration + price momentum (last 3 / 6 / 12 month return) |
| Risk / reward | Section 1 valuation upside (cite the Damodaran intrinsic range from 10.3 when present) vs Section 9 downside scenarios — must be ≥ 3:1 |
| Valuation | Section 1 valuation snapshot |
| Sentiment | Section 6 / Section 9 — extremes only count when fundamentals confirm |
| Insider activity | Form 4 — supporting signal only |
| Macro liquidity context | `indicators.db` snapshot — 10Y Treasury direction (rising / falling / flat), HY OAS direction, central bank stance (tightening / pausing / cutting), with as-of date |

**Scoring, weighted 0–10:**

- Growth / momentum — 35%
- Risk / reward — 20%
- Valuation — 20%
- Sentiment — 15%
- Insider activity — 10%

**Verdict bands:**

- **≥ 7.5** → `*Lens view:* Druckenmiller-style asymmetric setup.`
- **4.5–7.4** → Neutral.
- **≤ 4.4** → Below Druckenmiller's bar.

**Required macro context paragraph (mandatory in the subsection):** state the current liquidity regime in one sentence — Fed tightening / pausing / cutting + HY OAS direction + 10Y direction, with as-of date. **Bullish verdicts that contradict a tightening regime ("don't fight the Fed")** must call out the disagreement and explain the override, or downgrade.

**Required same-day-exit trigger (mandatory in the subsection):** name the specific observable that would cause an immediate exit (e.g. "Q3 revenue prints under $X B", "10Y Treasury breaks above Y%", "HY OAS exceeds Z bp"). If the analyst can't articulate one, downgrade — Druckenmiller's discipline is the exit rule, not the entry.

**Failure modes:**

- Bullish into a tightening regime with no override rationale → fighting the Fed; downgrade.
- No 3:1 risk/reward math → not a Druckenmiller setup; this lens does not apply.
- No same-day-exit trigger → no Druckenmiller discipline; downgrade.
- Over-hedged position → Druckenmiller hedges risks he can't tolerate, not returns he doesn't trust; flag the over-hedge.

### 10.9 Cathie Wood Wright's Law — disruptive cost-curve + five-year TAM re-pricing + convergence

**What it scores.** Whether the company benefits from a Wright's-Law cost-curve (cost per unit declines with cumulative production), whether the five-year-forward TAM is materially larger than today's TAM at the post-curve price point, and whether the company sits at the intersection of multiple disruptive platforms (genomics × AI, AI × robotics, energy storage × autonomous mobility, etc.).

**Inputs (already cited in earlier sections):**

| Component | Inputs |
|---|---|
| Wright's Law trajectory | Section 4 (is the product subject to a cost-curve? — semis, batteries, sequencing, AI compute, storage) + Section 6 (industry cost-trend data) |
| Today's TAM vs five-year TAM | Section 8 TAM build — must include forward TAM at post-curve prices, not just today's TAM |
| Innovation intensity | Section 1 (revenue growth ≥20%); Section 4 (R&D as % of revenue ≥15%); Section 6 (R&D intensity vs industry) |
| Capital allocation | Section 1 share count trend (heavy dilution = compounding-engine drag) |
| Convergence opportunity | Section 6 / Section 7 — does the company sit at the intersection of multiple disruption platforms? |

**Scoring (composite 0–10):**

| Sub-axis | Weight | Components |
|---|---|---|
| Disruptive potential | 40% | Revenue acceleration trajectory; R&D intensity ≥15%; margin expansion |
| Innovation-driven growth | 30% | R&D trend; FCF reinvested in capex (not buybacks); minimal dilution |
| Valuation (growth-biased DCF) | 30% | DCF with 20% revenue growth / 15% discount over 5-year horizon; implied multiple vs current |

**Verdict bands:**

- **≥ 7.0** → `*Lens view:* Cathie-Wood-style disruptive innovation candidate.`
- **3.0–6.9** → Neutral / mixed.
- **≤ 2.9** → Below the disruption bar.

**Required Wright's Law math (mandatory in the subsection):** show today's unit-cost (or proxy), the implied unit-cost in 5 years at the historical learning rate, today's TAM at today's price, and the projected TAM at the post-curve price. Without this math, the lens cannot return bullish — disruption claims need the curve.

**Required convergence note (mandatory in the subsection):** name at least one adjacent disruptive platform the company benefits from. If the company is single-platform-only, that's a Cathie-Wood-bearish signal (one platform = vulnerability to displacement).

**Failure modes:**

- "20% revenue growth = bullish" without TAM re-pricing → arithmetic, not innovation; downgrade.
- Bullish on a commoditized name where cost decline is driven by competition (not Wright's-Law-led adoption) → not a disruption thesis.
- Heavy share dilution to fund growth → kills the compounding engine; downgrade by 1 point.
- "Three-platform convergence" claim without sources → relabel as analyst view; require citation per platform.

## Guardrails (apply to all nine lenses — core + optional)

- **Never invent inputs.** Every number in a scorecard table must already be cited somewhere in Sections 1–9 of the same report, or come from `indicators.db` with an as-of date stated inline. If a required input is missing, write `not disclosed` in the cell and downgrade the score for that component — don't substitute a plausible-looking estimate.
- **Never claim the lens-namesake "would buy" this stock.** The verdict is the *scorecard's* output, not the named investor's endorsement. Use `Buffett-style scorecard verdict: ___` (not `Buffett would: ___`). Applies to all nine — `Lynch would buy`, `林奇会买`, `Burry would short`, `Druckenmiller would size large`, `Cathie Wood projects X` are all out of bounds.
- **Re-use existing citations.** A lens subsection that introduces new inline citations means you skipped Sections 1–9 evidence — go back and use what's already cited. The only new citation each lens may legitimately introduce is the one for the cycle inputs from `indicators.db` (state the as-of date).
- **Separate facts from interpretation.** The Scorecard table is interpretation; the Evidence sentence chain (with citations) is fact. Keep them visually distinct.
- **Disagreement across lenses is information, not a defect.** If Buffett says Avoid (poor valuation) but Damodaran says Bullish (story supports MoS > 25%), call it out — that disagreement is more useful than a forced consensus.
- **Stale-data discipline.** Cycle inputs older than 30 days → re-pull from `indicators.db` and re-score. Valuation inputs older than 3 trading days → flag as stale.
- **No "Source: our model"** — applies here as much as anywhere else in the report. The scorecards are framework-driven scores, not new model output.

## Implementation tips

- Pull the indicator snapshot once at the top of Section 10 and reference it across all included lenses (`indicators.db` snapshot as of YYYY-MM-DD: VIX = `__`, 10Y Treasury = `__`, HY OAS = `__`).
- The cycle posture (10.4) should be **computed first** because it gates the verdicts in lenses 10.1–10.3 (and 10.8 Druckenmiller) — a defensive cycle should mute "Bullish" verdicts in the company-specific lenses (note the disagreement explicitly).
- Place the section between Section 9 Risk Assessment and the References block in both the English and Chinese reports — same lenses, two natively-written prose passes (not a literal translation).
- **Section 10 word count by lens count:**
  - **Core only (10.1–10.4)**: 600–1,000 words total (~150–250 per lens). Default.
  - **Core + 1 optional pack lens**: 750–1,250 words.
  - **Core + all 5 optional lenses (10.1–10.9)**: 1,500–2,500 words — significant addition. Use only when the company's character requires multi-lens treatment (e.g. a hard-to-DCF growth name that needs Cathie Wood + Lynch + Damodaran together).
- **Picking optional lenses by company type** — quick routing rules so the analyst doesn't have to ponder:
  - Mid-cap consumer / industrial grower in a known category → add **Lynch (10.5)**.
  - Decade-runway compounder with customer/supplier scuttlebutt in the report → add **Fisher (10.6)**.
  - Hated sector, suspected value trap, or balance-sheet-led contrarian thesis → add **Burry (10.7)**.
  - Macro-liquidity-sensitive name (rate-sensitive sector, cyclical at inflection, regime-bound thesis) → add **Druckenmiller (10.8)**.
  - Hard-to-DCF disruption story (AI, robotics, EV, genomics, energy storage) → add **Cathie Wood (10.9)**.
  - When in doubt: include none of the optional packs; the core four are sufficient.

## What this section does NOT do

- It does not replace Section 9 (Risk Assessment) — the lenses are second opinions on quality and price, not a structured risk decomposition.
- It does not substitute for a price target or recommendation — those come from [[trader-plan]] and [[portfolio-decision]] in the trading-analysis pipeline. The lens scorecards are inputs to that decision, not its output.
- It does not introduce new data sources beyond what Sections 1–9 cited + the `indicators.db` cycle snapshot — if a lens needs an input that wasn't already gathered, the right fix is to go back and gather it in the right section, not to one-shot-cite it inside Section 10.
