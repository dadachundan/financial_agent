# Scenario PT framework — house-style template

This is the durable template distilled from sell-side single-stock "bull / base / bear" notes. The bull-bear-debate skill borrows the **output** (a three-target Risk-Reward scorecard) while keeping the multi-round conversational debate as the means of getting there.

## The three-target structure

Three cases, not two — **bull / base / bear, each with its OWN price target**. The **base case IS the headline 12-month PT**; bull and bear bracket it. Lead the note with a one-line verdict box: **rating + base-case PT + implied upside/downside % vs last close + valuation method**.

Exemplars (named report series, no file_ids):

- **Morgan Stanley "Risk Reward Update"** — the single closest analog. One PT per case, each shown as `multiple × forward-year EPS` (SanDisk bull 31× × $85 = $2,635; base 28× × $62.50 = $1,750; bear 25× × $44 = $1,100). Names the swing variable per case; some carry explicit scenario probabilities (AAPL 30% / 65% / 5%).
- **UBS scenario-analysis block** (Caterpillar, Futu, Kioxia) — rating + PT + implied upside, then an upside/base/downside three-line scenario each as `multiple × forward EPS` (CAT $1,173 / $900 / $626 = 35× / 30× / 26× × 2027E EPS), plus the key assumption delta per case.
- **Jefferies three-target initiation** (Sumitomo Electric) — base ¥20,600 / bull ¥23,800 / bear ¥11,200, each tied to a forward multiple and a one-line driver.
- **J.P. Morgan named bull/base deep-dives** (Insta360 "View from 2030"; DiDi "bear tail thins, bull case still unproven") — explicit conditions that must ALL hold for the bull case, plus upgrade/downgrade-trigger lists.
- **Bernstein asymmetry notes** (Novo Nordisk; GitLab) — quantifies risk/reward ("+34% upside vs −38% downside"), names the over-priced bull input, and assigns event probabilities (RVMD 86% success / 14% fail).

## PT decomposition — `multiple × forward-EPS`

Every case PT must decompose into its drivers so it is auditable: `case-PT = (valuation multiple) × (forward-year EPS or per-case metric)`. Reproduce this verbatim (AVGO bull 30× = $619, bear 20× = $298). Build the **bear PT as a real valuation** (lower multiple × lower forward EPS), never a worry list. Ground each case in a FY+1 / FY+2 / FY+3 estimate ladder (revenue, EPS, gross/operating margin); the bull/bear case is driven by perturbing these.

Keep three numbers visually distinct, never blended: **company guidance**, **consensus / Bloomberg-street**, and **the analyst's own estimate** (mirrors the project `*Analyst view:*` labelling rule). Use consensus as a credibility anchor ("MS EPS ~13% above consensus FY3/27").

## Valuation-method menu (name the method per PT)

| Method | When used |
|---|---|
| **P/E × forward EPS** | Default for profitable, stable-multiple names; the dominant Risk-Reward form. |
| **DCF (WACC + terminal growth)** | Long-duration / pre-peak-margin names (e.g. WACC 11.2% / TGV 3%). State both inputs. |
| **Residual Income Model (RIM)** | Financials / book-value-driven names (Futu, YOFC). |
| **SOTP** | Multi-segment conglomerates — value each segment on its own multiple (Weichai). |
| **FCF-yield** | Cyclicals / capital-returners (Kioxia 10% FY3/28 FCF yield). |

## Swing variables — the same lever at different values

Both sides argue the **same** 2–4 levers set high (bull) vs low (bear), not disjoint topics. GS commodity-relativity (gold $3,500 vs $5,500 across a coverage list); UBS Futu (paying-client CAGR 17.2% / 15.2% / MCC-exit). Cite each swing-variable value to a source that literally contains it (consensus, CRU / Riglogix / Yole-style forecasters, the `*Analyst view:*` block). Stress one swing variable at a time with reported sensitivity (JPM "+$20/bbl per month of Hormuz delay").

## Probability weighting & asymmetry math

Attach a rough probability to each case (sum to 100%). Compute a **probability-weighted EV-PT** (`Σ prob × PT`) and an explicit **upside : downside ratio** vs last close. This is the differentiator that turns two opinions into an actionable EV call — only MS (AAPL 30/65/5) and Bernstein (Novo +34% / −38%) do it consistently.

## Priced-in test

The strongest bear case shows the **bull case is already the price** via implied-growth / positioning math (YOFC: "current price implies ~25bn/qtr net profit vs 4.95bn actual — a 4–5× jump — too hard"; MS positioning: active ownership %, HF L/S, net exposure). Each side states how much of the *opposing* case is already embedded in the current price.

## Two-list risk convention

End with **two explicit bulleted lists**, distinct from the body argument:

- **Upside risks** — what could push the stock above the base case.
- **Downside risks** — what could push it below.

## Triggers (dated, falsifiable)

Close with dated catalysts mapped to the case each confirms, split high-priority (real worry) vs low-priority (not yet) — the HSBC "What would make us bearish?" / Citi "Bear Market Checklist" template. Each trigger maps to an upgrade or downgrade condition.

## Further viewing (separate from citations)

- **Further viewing** — 1–3 validated explainer videos for hard-to-visualize concepts the debate hinges on, in their own slot, never a citation and never carrying a number (see SKILL.md `## Further viewing`).
