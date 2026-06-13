# GF Score (GuruFocus-style) — fundamental health scorecard

A five-axis scorecard that distils a company's fundamentals into one **0–100 composite** plus a **radar/pentagon** picture, modelled on [GuruFocus's GF Score™](https://www.gurufocus.com/term/gf-score). It is a structured *second read* of the same evidence the report already gathered — like the Section-10 investor lenses, **it is an analytical overlay, not a new data source and not an endorsement.** The five components are: **Financial Strength · Profitability · Growth · GF Value (valuation) · Momentum**, each ranked **0–10**; the composite maps to GuruFocus's outperformance bands.

This is the canonical spec. company-research, compare-companies, and the other skills that emit a GF Score all import it. Read it before writing a GF Score block.

---

## The honesty rule — what this is and is NOT (read first)

GuruFocus's real GF Score is **proprietary** — its exact component weights come from a backtest (2006–2021) that GuruFocus does not publish, and the number is computed from their own data feed. We cannot reproduce that exact number, and we do not pretend to.

So this scorecard is an **independently-computed, GuruFocus-*style* reproduction**: a transparent rubric whose every input metric is sourced from the filings / market data the report already cites, whose weights are stated openly, and whose 0–10 mappings are written down below so a reader can re-derive every number. Treat it exactly like the investor-lens scorecards:

1. **The five sub-scores and the composite are the analyst's own rubric output — label them `*Analyst view:*` / `*分析师观点：*`.** Never attach a filing citation to a *score*. (A 10-K contains no "Profitability rank"; attaching one is the misattribution failure the skill already forbids.)
2. **Every underlying metric must carry its own inline citation** in the surrounding prose — ROE / margins / leverage to the filing (page-level), multiples to the market-data source, price returns to yfinance / `indicators.db`. A score with no cited metrics behind it is unsourced opinion.
3. **Never write "(Source: GuruFocus)" / "GF Score: 95 (GuruFocus)" unless you actually pulled GuruFocus's published number** from the per-ticker page `https://www.gurufocus.com/term/gf-score/<TICKER>` and are citing *that page*. If you do pull the real one, present it **separately** as a cross-check (`GuruFocus official GF Score: 94/100 ([GuruFocus](https://www.gurufocus.com/term/gf-score/GOOGL))`) and label our computed one `GF Score (GuruFocus-style, *Analyst view:*)`. Do not silently merge the two. **Note: GuruFocus is Cloudflare-protected and returns `403` to `curl`/`urllib`/WebFetch even with a browser UA — that is a bot-block, NOT a dead link. Confirm the page in a real browser (or the user's GuruFocus login); do not "fix" these URLs as broken during a Step-10 link check.**
4. **Never write "(Source: our model)" / "(模型估算)"** for the score — cite the inputs, not the rubric. Same rule as everywhere else in the skill.
5. **Trademark honesty.** "GF Score™" and "GF Value™" are GuruFocus marks. Our heading is **"GF Score (GuruFocus-style)"** and the radar footer says "not GuruFocus™ official number" — keep that disclosure; don't drop it to look cleaner.

If you cannot source a component's metrics at all (e.g. a pre-revenue private company with no margins), **score that axis `n/a` and say so** — do not invent a plausible number, and note in the composite that it was computed on the available axes only (or skip the composite and show only the axes you can defend).

---

## The five dimensions — what each measures, its metrics, and the 0–10 rubric

Each axis is scored **0–10** (10 = best). For every axis: pull the listed metrics from sources the report already cites, place the company in the anchored band, and **write down the 2–4 metrics that drove the number** (that's the "reasons why this score" the reader needs). Where a metric is missing, drop it and score on the rest — note the gap.

> **Direction reminder for GF Value:** higher GF Value rank = **cheaper relative to fair value** (good), not more expensive. This is counter-intuitive and must be stated in the report so a reader doesn't read "GF Value 9/10" as "expensive". All five axes share the convention *farther from center = better*.

### 1. Financial Strength (财务实力)

**Measures** balance-sheet resilience and distress risk — can the company fund itself and survive a downturn.

**Metrics** (cite each to the latest 10-K / 10-Q / 年度报告 balance sheet + cash-flow statement, page-level):
- Cash-to-Debt (cash & equivalents ÷ total debt)
- Net Debt / EBITDA (or Debt / EBITDA)
- Interest coverage (EBIT ÷ interest expense)
- Equity-to-Asset (or Debt-to-Equity)
- Altman Z-Score (distress proxy) — compute and show the inputs, or cite if a source carries it
- *(optional)* Piotroski F-Score, debt maturity wall / liquidity runway

**0–10 rubric (anchors — interpolate):**
| Score | Profile |
|---|---|
| 9–10 | Net cash; Z-Score > 3; interest coverage > 15× (or no debt); equity-to-asset high |
| 7–8 | Low leverage (Net Debt/EBITDA < 1.5×); coverage > 8×; Z-Score 2.5–3 |
| 5–6 | Moderate leverage (1.5–3×); coverage 3–8×; Z-Score 1.8–2.5 |
| 3–4 | Elevated leverage (3–5×); coverage 1.5–3×; Z-Score < 1.8 (grey zone) |
| 0–2 | Distress: Net Debt/EBITDA > 5× or negative EBITDA; coverage < 1.5×; negative equity; Z-Score < 1.1 |

### 2. Profitability (盈利能力)

**Measures** the quality and durability of earnings — does the business earn high returns, consistently.

**Metrics** (cite to the income statement / MD&A; ROIC vs WACC reuses the Section-1A WACC):
- Operating margin (+ 3-yr trend, + vs industry)
- Net margin
- ROE
- ROIC (and whether ROIC > WACC, by how many points)
- Gross-margin level and trend
- Consistency: years profitable out of the last 10 / earnings predictability

**0–10 rubric:**
| Score | Profile |
|---|---|
| 9–10 | Margins top-quartile for the sector; ROIC > WACC by ≥10 pts; profitable every year; expanding margins |
| 7–8 | Above-median margins; ROIC clears WACC by 5–10 pts; stable/rising; ≤1 loss year in 10 |
| 5–6 | Around-median margins; ROIC ≈ WACC; flat trend |
| 3–4 | Below-median margins; ROIC < WACC; thin or eroding |
| 0–2 | Loss-making on an operating basis; ROIC deeply negative; structurally unprofitable |

### 3. Growth (成长性)

**Measures** the rate at which the top and bottom line compound — historical and the forward estimate.

**Metrics** (history cited to filings; the forward number reuses the **Section-1A forward model / consensus**, labeled `*Analyst view:*`):
- 3-yr and 5-yr **revenue CAGR**
- 3-yr and 5-yr **EPS (or EBITDA) CAGR**
- Forward growth estimate (the report's own FY1E–FY3E revenue/EPS CAGR, or sourced consensus)
- *(optional)* book-value / FCF growth, growth consistency (std-dev of YoY)

**0–10 rubric:**
| Score | Profile |
|---|---|
| 9–10 | Revenue & EPS CAGR > 25–30%, sustained, with a credible forward path of similar magnitude |
| 7–8 | 15–25% CAGR, durable; forward estimate ≥ 12% |
| 5–6 | 7–15% CAGR; mid-single-to-low-double-digit forward |
| 3–4 | 0–7% CAGR; low-growth / GDP-ish |
| 0–2 | Shrinking revenue or EPS; negative forward outlook |

> A loss-maker can still score high on Growth (revenue compounding fast) while scoring low on Profitability — that divergence is exactly what the radar is meant to show; do not "smooth" it.

### 4. GF Value / Valuation (估值) — *higher = cheaper vs fair value*

**Measures** how cheap the stock is **relative to a fair-value anchor** — its own multiple history, peers, and an intrinsic estimate. GuruFocus's "GF Value" is their proprietary intrinsic line; we substitute a **transparent valuation rank** built from inputs the report already has.

**Metrics** (cite to the Section-1 valuation snapshot / Section-1A model / peer comps):
- Forward & TTM **P/E vs the stock's own 3–5-yr history percentile**
- Forward P/E vs **peer median** (the 3–5 comps already in Section 1/1A)
- PEG (P/E ÷ forward growth)
- EV/EBITDA and/or P/S vs own history + peers
- **Margin of safety** vs the Section-1A intrinsic / DCF / PT range (reuse the Damodaran MoS when Section 10 is present)

**0–10 rubric (10 = deeply undervalued):**
| Score | Profile |
|---|---|
| 9–10 | Trades well below fair-value anchor; multiples in bottom quartile of own history AND below peers; MoS ≥ +30% |
| 7–8 | Modestly cheap; below own median and ≤ peer median; MoS +10–30% |
| 5–6 | Fairly valued; multiples ≈ own median ≈ peers; MoS ±10% |
| 3–4 | Rich; upper-quartile of own history or > peer median without commensurate growth; MoS −10 to −30% |
| 0–2 | Extremely stretched; top-decile multiples / blue-sky priced; MoS < −30% |

> **PEG cross-check:** a high P/E paired with a high enough growth rate can still earn a mid valuation score (PEG ≈ 1). State the PEG so a reader sees *why* a 50× name isn't automatically a 2/10.

### 5. Momentum (动量)

**Measures** price and estimate momentum — is the market already voting up.

**Metrics** (reuse the **Section-1A relative-performance line** — 1M/6M/YTD/12M absolute + vs benchmark — cited to yfinance / `indicators.db`):
- 6-month and 12-month **price return, absolute AND relative to the benchmark** (S&P 500 / sector ETF / CSI 300 / Hang Seng as fits the listing)
- Relative strength vs benchmark (12-1 month)
- Distance from 52-week high/low; price vs 200-day MA
- *(optional)* earnings-estimate-revision trend (up/down), RSI(14) level

**0–10 rubric:**
| Score | Profile |
|---|---|
| 9–10 | Strong absolute uptrend AND beating the benchmark by a wide margin over 6–12M; above rising 200dma; near highs; estimates rising |
| 7–8 | Outperforming the benchmark; constructive trend |
| 5–6 | In line with the benchmark; sideways |
| 3–4 | Lagging the benchmark; below 200dma |
| 0–2 | Sharp absolute downtrend; deep underperformance; near 52-wk lows; estimates falling |

> Momentum is the most time-sensitive axis. Price inputs older than ~3 trading days → re-pull and re-score; state the as-of date.

---

## The composite 0–100 and the bands

**Default weights (`*Analyst view:*`, transparent reproduction — NOT GuruFocus's proprietary weighting):**

| Axis | Weight |
|---|---|
| Financial Strength | 20% |
| Profitability | 25% |
| Growth | 25% |
| GF Value | 15% |
| Momentum | 15% |

**Formula (show the arithmetic in the report):**
```
weighted_avg(0–10) = Σ(axis_score × weight) / Σ(weights)
GF Score (0–100)   = round( weighted_avg × 10 )
```
Worked example — FS 8 · Prof 10 · Growth 9 · Value 4 · Mom 8 → `(8·20 + 10·25 + 9·25 + 4·15 + 8·15)/100 = 8.15 → 82/100`.

You may adjust weights for a specific business (e.g. tilt to Growth + Value for a deep-value turnaround) — but **state the weights you used** every time. The helper script's `--weights` flag carries them; the table footer prints them.

**Band labels (verbatim from GuruFocus — use exactly):**
| Composite | Band |
|---|---|
| **91–100** | Highest outperformance potential |
| **81–90** | Good outperformance potential |
| **71–80** | Likely to have average performance |
| **51–70** | Poor future performance potential |
| **0–50** | Worst future performance potential, or not enough data |

GuruFocus's published framing — keep it as the one-line interpretation under the score: *"The GF Score is closely correlated with the long-term performance of stocks (backtested 2006–2021); higher GF Scores generally generated higher returns."* Cite it to [GuruFocus's GF Score page](https://www.gurufocus.com/term/gf-score) when you state it.

---

## The radar/pentagon visual — inline SVG via the helper

Render the pentagon with the helper script — it emits **inline `<svg>`** (which the report viewer passes straight through to `innerHTML`, the same path the Step-10 `<details>` logs ride on) plus the markdown scorecard table. It is stdlib-only (no matplotlib — safe for the per-agent memory budget) and bakes the **required `--source` annotation** into the SVG footer per the project chart rule.

```bash
cd /Users/x/projects/financial_agent
# Single company → filled pentagon + table
/opt/anaconda3/bin/python3 scripts/gf_score.py \
  --name NVDA --scores 8,10,9,4,8 \
  --source "NVDA FY25 10-K · Yahoo Finance · indicators.db, as of 2026-06-13"

# Compare (2–4 companies) → overlaid radar with a per-company legend
/opt/anaconda3/bin/python3 scripts/gf_score.py \
  --series "NVDA:8,10,9,4,8" --series "AMD:6,7,8,6,5" --series "INTC:5,4,3,7,3" \
  --source "FY25 10-Ks · Yahoo Finance, as of 2026-06-13"
```

- **Input order is always `fs,prof,growth,value,mom`** (the five axes in this doc's order). Scores 0–10.
- `--source` is **required** and travels inside the image (chart gets screenshotted / iframe-embedded without its caption). Keep it concise (it sits on one footer line).
- `--weights 20,25,25,15,15` overrides the composite weights (must sum to 100); `--lang en|zh|bi` sets the table language; `--emit svg|table|both`.
- Paste the emitted `<svg>…</svg>` block directly into the markdown, then the markdown table beneath it. Do **not** wrap the SVG in a code fence — it must render, not display as source.

**How-to-read note (include once, under the radar):**
> 离中心越远，该维度得分越高 / *The farther a point sits from the centre, the better the company scores on that axis; the larger the pentagon's area, the higher the overall GF Score.* (Mirrors the GuruFocus widget.)

If for any reason inline SVG can't be used, the markdown table alone (with the Unicode `████░░` bars the helper emits) is an acceptable fallback — but the radar is the signature visual the user asked for; default to including it.

---

## Output shape in the report

The block is short — **~350–600 words** for a single company. Structure:

1. **Verdict line (bold).** `*Analyst view:* **GF Score (GuruFocus-style): 82/100 — Good outperformance potential (81–90 band).**` Optionally append the real GuruFocus number as a separate cross-check if you pulled it.
2. **The radar `<svg>`** (from the helper) + the **how-to-read note**.
3. **The 5-row scorecard table** (from the helper) — per-axis 0–10 + the composite row.
4. **Per-dimension rationale — one short paragraph per axis (the "reasons why this score").** Each paragraph: the score, the 2–4 metrics that drove it (each with its inline citation), and one sentence of interpretation. This is the heart of the block — a score with no reasons is not acceptable.
5. **Composite arithmetic line** — show `(FS·20 + Prof·25 + …)/100 → NN/100` and the weights used, so the number is reproducible.
6. **One-line caveat / failure mode** — the axis most likely to flip (e.g. "Momentum is doing the heavy lifting; a single bad print re-rates it down 3 points") and any `n/a` axis.

**Placement:**
- **company-research** → a dedicated **Section 1B — GF Score (GuruFocus-style)**, right after Section 1A (Valuation & Price Target), so the whole decision layer (rating/PT → valuation → fundamental scorecard) sits together near the top, mirroring the GuruFocus summary widget. It is independent of the optional Section-10 lenses (do not bury it inside Section 10).
- **compare-companies** → see the multi-company variant below; place it with the §4.5 relative-valuation scoreboard (the financial/valuation cluster) or as its own scorecard section before the moat anatomy.

---

## Multi-company variant (compare-companies and panels)

When scoring 2–4 names side by side:

- **One overlaid radar** (helper with repeated `--series`) so the shapes are directly comparable, with a legend carrying each name's composite. Distinct colours per company.
- **A per-company column table** — axes as rows, companies as columns, composite row at the bottom (the helper emits this when given ≥2 `--series`).
- **A "who wins each axis" line** — for each of the five axes, name the leader and the one-clause why (cited), then the composite ranking. This is the GF-Score analogue of the §9 side-by-side scorecard; keep it consistent with the report's order-of-preference call (don't let the GF ranking silently contradict the §10 bottom-line verdict — if they diverge, say why, e.g. "X scores higher on fundamentals but Y wins on valuation entry point").
- **Comparability caveats apply** (same as the moat tables): GAAP vs non-GAAP margins, organic vs M&A-inflated growth, different fiscal-year ends, ADR vs local-line momentum — flag the non-comparability before drawing the axis verdict.

---

## Guardrails (the load-bearing don'ts)

- **The score is `*Analyst view:*`; the metrics are cited.** Never a filing citation on a score; never an uncited metric behind one.
- **Never attribute the computed score to GuruFocus.** Only a number actually pulled from gurufocus.com may carry a GuruFocus citation, and it's shown separately.
- **Higher GF Value = cheaper.** State this in-text every time so the direction isn't misread.
- **`n/a` an axis you can't source** — don't fabricate. Note it in the composite.
- **Every number in the rationale string-matches its cited source** (project Numerical-Accuracy rule) — spot-check ROE / margin / CAGR / return against the URL before committing.
- **Keep it consistent with the rest of the report.** The Growth axis should agree with the Section-1A forward model; the Value axis with the Section-1 multiples and the PT's implied upside; Momentum with the header's relative-performance line. A GF Score that contradicts the report's own numbers is a defect.
- **Re-pull price-sensitive inputs.** Momentum / valuation inputs older than ~3 trading days → refresh and re-score; state the as-of date.
- **State the weights** whenever they deviate from the 20/25/25/15/15 default.
- **Bilingual gloss** in Chinese reports: `Financial Strength (财务实力)`, `Profitability (盈利能力)`, `Growth (成长性)`, `GF Value (估值)`, `Momentum (动量)`, `GF Score (综合评分)`.
