---
name: market-complacency
description: Score how much risk the market is currently under-pricing — a composite "complacency dashboard" of credit spreads (HY/IG/CCC OAS), equity vol (VIX, VVIX, VIX term slope, SKEW), rate vol (MOVE), risk-premium compression (ERP, HYG/LQD), sentiment (AAII bull-bear, NAAIM exposure, put/call), breadth (% above 200dma), and valuation (Shiller CAPE). Each indicator gets a percentile rank vs its own 10-year history; a low percentile on a "low = risk under-priced" indicator counts as complacency. Produces a 3,000–5,000 word English markdown report with a one-line **Complacency Verdict** (Stretched / Elevated / Neutral / Cautious / Panicked), a composite 0–100 score, an indicator-by-indicator table with current vs decile context, 6–10 charts, and a list of historical precedents at similar score levels. Use when the user asks "is the market complacent?", "is risk under-priced right now?", "are credit spreads too tight?", "where are we vs 2007 / January 2018 / Q1 2020?", or anything in the under-priced-risk / late-cycle / euphoria family.
---

# Market Complacency

Quantify how much risk the market is currently under-pricing. The motivating observation: *exceptionally low HY OAS credit spreads historically signal complacency — investors under-price default risk in weaker corporate balance sheets just before regimes turn.* But credit spreads are only one symptom. Complacency shows up across **credit + vol + risk-premium + sentiment + breadth + valuation** simultaneously; reading any one in isolation gives false positives. This skill aggregates the cross-asset signal into one dashboard and one verdict.

This is a **regime / macro lens**, not a single-name call. Use it to inform position sizing, hedge ratios, and cash levels — not to pick a ticker.

## When to use

The user says any of:

- "Is the market complacent right now?"
- "Are credit spreads too tight?"
- "Is risk being under-priced?"
- "Where are we vs January 2018 / Q4 2007 / Q1 2020?"
- "How euphoric is positioning?"
- "Should I add hedges?" (this skill informs the answer; it does not size the hedge)
- "Complacency score" / "complacency dashboard" / "/market-complacency"

The skill produces a **Complacency Verdict** (5-tier) backed by a composite percentile score and a per-indicator breakdown of which signals are flashing and which are not.

## When NOT to use

- The user wants a single-ticker call — use [[trader-plan]] / [[portfolio-decision]] / [[take-profit-lab]].
- The user wants to know *what to short* — this skill says "risk is mispriced", not "here is the vehicle". Hand off to [[idea-generation]] for short-bias screens.
- The user wants the inverse — a *panic / capitulation* read. This skill handles both ends of the same axis: the verdict tier "Panicked" maps to the bottom decile of the same composite score. There is no separate "/market-fear" skill.
- The question is about a single sector's stress (e.g. "are regional banks in trouble?") — use [[sector-overview]] with a stress lens; the macro complacency dashboard won't pick up sub-sector dislocation.
- The user wants a forecast of *when* the regime turns — this skill is a **state read**, not a timing model. Complacency can persist for quarters; the dashboard tells you the regime, not the trigger.

## Core methodology

### The complacency axis

For each indicator, define a direction such that **lower percentile = more complacent** (risk under-priced). Then the composite score is a simple weighted average of complacency percentiles, mapped to a 0–100 scale where:

- **0–20**: Panicked (risk *over*-priced — capitulation regime, usually a contrarian buy signal)
- **20–40**: Cautious (risk fairly priced; modest hedging)
- **40–60**: Neutral
- **60–80**: Elevated (risk under-priced on several axes; trim, add hedges)
- **80–100**: Stretched (risk under-priced across the board; late-cycle euphoria signature)

### Indicators (the dashboard)

Twelve indicators across six categories. The "complacency direction" column states whether *low* or *high* readings count as complacency.

| # | Indicator | Source | Complacency direction | Why it signals complacency |
|---|---|---|---|---|
| **Credit (under-pricing default risk)** | | | | |
| 1 | **HY OAS** (ICE BofA US High Yield) | FRED `BAMLH0A0HYM2` | **Low** = complacent | Bottom-decile HY spreads have historically preceded credit-cycle turns (Q2 2007 at 2.4%, Jan 2020 at 3.4%) |
| 2 | **IG OAS** (ICE BofA US Corporate) | FRED `BAMLC0A0CM` | **Low** = complacent | Same logic, investment-grade tier |
| 3 | **CCC OAS** (ICE BofA US CCC & Lower) | FRED `BAMLH0A3HYC` | **Low** = complacent | The weakest tier — the first to widen when the cycle turns. Bottom-decile CCC = the strongest single-indicator complacency tell |
| **Equity-volatility (under-pricing equity tail risk)** | | | | |
| 4 | **VIX** | yfinance `^VIX` | **Low** = complacent | <13 = bottom decile; VIX <12 in Jan 2018 and Jan 2020 immediately preceded vol shocks |
| 5 | **VVIX** (vol-of-vol) | yfinance `^VVIX` | **Low** = complacent | <80 = market not even worried about *change* in vol — a deeper complacency signal than VIX alone |
| 6 | **VIX term slope** (VIX9D ÷ VIX3M) | derived | **Low ratio** = complacent | Deep contango (<0.85) means short-dated vol is much cheaper than 3-month — no near-term hedging demand |
| 7 | **SKEW** (CBOE SKEW Index) | yfinance `^SKEW` | **Low** = complacent | SKEW measures the cost of OTM puts; a low SKEW means investors aren't bidding for crash protection. Caveat: the relationship is noisier than VIX — use percentile rank, not absolute level |
| **Rate-volatility (under-pricing duration / rate risk)** | | | | |
| 8 | **MOVE Index** (ICE BofAML US Bond Vol) | yfinance `^MOVE` | **Low** = complacent | <80 = unusually low Treasury vol; pairs with low VIX as a "nothing-can-go-wrong" signature across asset classes |
| **Risk-premium compression** | | | | |
| 9 | **Equity Risk Premium** = SPY trailing earnings yield − 10Y Treasury yield | derived | **Low / negative** = complacent | Stocks priced for perfection vs the risk-free rate; <2pp historically associated with poor 5y forward returns |
| 10 | **HYG/LQD ratio** | derived (yfinance) | **High** = complacent | HY outperforming IG = risk-on flow; rising 6-month rate-of-change is a momentum-of-complacency tell |
| **Sentiment / positioning** | | | | |
| 11 | **AAII Bull-Bear Spread** | AAII weekly survey (CSV) | **High** = complacent | Retail bull-bear >20pp historically a contrarian late-cycle signal; >30pp very stretched. Optional — surveys are gappy; skip if the AAII CSV fetch fails |
| 12 | **NAAIM Exposure Index** | NAAIM weekly (CSV) | **High** = complacent | Active managers' net long exposure; >90 = max-long crowding. Optional — same caveat as AAII |
| **Valuation (under-pricing through-cycle drawdown)** | | | | |
| 13 | **Shiller CAPE** (cyclically adjusted P/E) | Shiller's monthly CSV (Yale) | **High** = complacent | Long-cycle valuation; >30 historically associated with thin forward returns. Slow-moving — use as a "background" weight, not a trigger |

**Required vs optional**. Indicators 1–10 are *required* — the composite score must include all ten. Indicators 11–13 are *optional* enrichment — if the upstream CSV is unreachable, drop them from the composite and disclose in the Data Used manifest. Never silently degrade the score without telling the reader.

### Per-indicator percentile mapping

For each indicator with at least 5 years of clean history (target: 10 years), compute:

1. **Current value** — most recent valid observation.
2. **10-year percentile rank** — where today sits in the distribution of the last 10 years. For "low = complacent" indicators, *complacency percentile = 100 − value percentile*; for "high = complacent" indicators, *complacency percentile = value percentile*.
3. **Decile label** — "1st decile (most complacent)" / "5th (median)" / "10th (least complacent)".
4. **Stretched flag** — true if the complacency percentile ≥ 90 (i.e. today is in the most-complacent decile vs the last 10 years for this indicator).

### Composite score

Weighted average of complacency percentiles. Weights reflect the indicators' historical track record as cycle-turn signals (calibrated from 2000–2025, with weights summing to 1.0):

| Indicator | Weight |
|---|---|
| HY OAS | 0.15 |
| IG OAS | 0.07 |
| CCC OAS | 0.10 |
| VIX | 0.10 |
| VVIX | 0.05 |
| VIX term slope | 0.05 |
| SKEW | 0.05 |
| MOVE | 0.08 |
| ERP | 0.10 |
| HYG/LQD ratio | 0.05 |
| AAII bull-bear (optional) | 0.05 |
| NAAIM exposure (optional) | 0.05 |
| Shiller CAPE | 0.10 |

If an optional indicator is missing, re-normalize weights so the active set still sums to 1.0 — disclose in the Data Used manifest.

The composite is a scalar 0–100. Map to the 5-tier verdict via the bands above.

### Historical precedents

After computing today's composite, look up the dates in the last 25 years when the composite was within ±5 points of today's level. List up to 8 precedents, each annotated with what happened in the *following* 6 / 12 / 24 months (SPY total return + max drawdown). This is the report's most valuable single block — it tells the reader "the last 5 times the dashboard read 78, here's what came next".

This is **not** a forecast — it's a base-rate reference. Calibration must be explicit: "the dashboard predicted the path *0 of 5 times*; it described the regime *5 of 5 times*."

## Data sources (project-specific)

### Already in `indicators/data_fetcher.py`

The following are already pulled by the project's `indicators` module — reuse `indicators.data_fetcher.fetch_all()` and `_fetch_fred_range()` rather than re-implementing:

- HY OAS (FRED `BAMLH0A0HYM2`), IG OAS (FRED `BAMLC0A0CM`)
- VIX (`^VIX`), VVIX (`^VVIX`), VIX9D / VIX3M (`_RATIO_^VIX9D_^VIX3M`)
- HYG, LQD, SPY, 10Y yield (`^TNX`)

### Add to the skill (not yet in the indicators module)

These are pulled inside the skill's own `oneoff/market_complacency_<DATE>.py` script. **Do not** modify the indicators module from this skill — keep the addition scoped to the report run. If the user later asks to promote one of these to the live dashboard, that is a separate task.

- **CCC OAS** — FRED series `BAMLH0A3HYC` (ICE BofA US CCC & Lower OAS). Pull via the existing `_fetch_fred_range()` helper.
- **SKEW** — yfinance `^SKEW`. Yahoo carries CBOE's daily SKEW back to 1990.
- **MOVE** — yfinance `^MOVE` (ICE BofAML US Bond Market OAS, the rate-vol analog of VIX). Yahoo data starts 2002.
- **Shiller CAPE** — Robert Shiller's monthly CSV at `http://www.econ.yale.edu/~shiller/data/ie_data.xls` (Excel). Cache locally as `oneoff/shiller_cape.csv` and refresh monthly.
- **AAII Bull-Bear** (optional) — weekly CSV at `https://www.aaii.com/files/surveys/sentiment.xls`. Cache locally; refresh weekly.
- **NAAIM Exposure** (optional) — weekly CSV at `https://www.naaim.org/programs/naaim-exposure-index/`. Often gated; skip if not reachable.

### Derived indicators

- **Equity Risk Premium** — SPY trailing earnings yield minus 10Y Treasury yield. Pull SPY trailing EPS from yfinance (`yf.Ticker("SPY").info["trailingEps"]` divided by current price), then subtract `^TNX/100`. If the SPY EPS lookup is flaky, fall back to S&P 500 trailing EPS from `https://www.multpl.com/s-p-500-earnings/table/by-month` (CSV scrape).
- **HYG/LQD ratio** — `HYG.Close / LQD.Close` over 10 years; complacency percentile = rank vs trailing 10y.

### Database write rule (no exceptions)

This skill **only reads** from the indicators stack. Do **not** write to `db/indicators.db` or any other `db/*.db` — see [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety". If a new indicator needs persisting, the user must promote it to the live dashboard in a separate task that goes through `indicators/db.py`.

## Workflow

### Step 0 — Sanity check the request

Confirm the user wants a *macro / regime* read, not a single-ticker call. If the prompt names a ticker ("is NVDA complacent?"), redirect: this skill measures market-wide complacency; for single-name expensiveness use [[take-profit-lab]] or [[company-research]] § valuation.

If the user is asking specifically about *credit* complacency only (no equity/vol context), still run the full dashboard — the credit-only read is in the per-indicator table, and the cross-asset context is the report's edge over reading a single FRED chart.

### Step 1 — Pull required indicators

Write a one-off Python script at `oneoff/market_complacency_<YYYY-MM-DD>.py` that:

1. Calls `indicators.data_fetcher.fetch_all()` for the live dashboard subset (HY OAS, IG OAS, VIX, VVIX, VIX term slope, HYG, LQD, SPY, ^TNX). 45 days of context is enough for the *current value*; for the 10-year percentile, fetch the longer FRED / yfinance ranges directly.
2. For each required indicator, fetch 10 years of daily history via `_fetch_fred_range()` (FRED indicators) or `yf.Ticker(...).history(period="10y", auto_adjust=True)` (yfinance indicators).
3. Compute the current value, 10-year percentile, complacency percentile (per the direction column), decile label, and stretched flag.
4. Save the per-indicator table as `oneoff/market_complacency_<DATE>_indicators.csv`.
5. Compute the composite score and verdict tier.

### Step 2 — Pull optional enrichment

In the same script, attempt to fetch AAII, NAAIM, and Shiller CAPE. For each:

- On success, add to the dashboard with full percentile context.
- On failure (CSV unreachable, format change, paywall), log a warning, exclude from the composite, and re-normalize weights.

The script must exit cleanly even if every optional indicator fails — the required 10 are sufficient for a complete report.

### Step 3 — Find historical precedents

Compute the daily composite score across the last 25 years (back-fill: where a constituent indicator has shorter history, use only the available subset and re-normalize weights for that date). Find all dates where the historical composite was within ±5 points of today's composite. Bin by year, keep the 8 dates spread furthest apart.

For each precedent date, compute SPY total return + max drawdown over the next 6 / 12 / 24 months. Save as `oneoff/market_complacency_<DATE>_precedents.csv`.

### Step 4 — Generate charts (6–10 visuals)

Save under `reports/charts/market_complacency_<DATE>_*.png` (DPI 150, `bbox_inches="tight"`). Suggested chart inventory:

1. **Composite score, last 25 years** — line chart with the 5-tier bands shaded; today marked. The headline chart.
2. **HY OAS, last 25 years** — line with current value and the 5th / 50th / 95th percentile of last 10y marked.
3. **IG + CCC OAS overlay, last 25 years** — credit-tier divergence visible.
4. **VIX + VVIX overlay, last 10 years** — equity vol regime.
5. **VIX term slope (VIX9D/VIX3M), last 10 years** — with contango/backwardation bands.
6. **MOVE Index, last 10 years** — rate-vol regime alongside the equity-vol charts above.
7. **ERP (SPY earnings yield − 10Y), last 25 years** — risk-premium compression.
8. **Indicator deciles bar chart** — one bar per indicator showing today's complacency percentile, colored by the 5-tier band.
9. *(Optional)* **Precedent-month SPY forward returns scatter** — x = composite at precedent date, y = SPY 12m forward return.
10. *(Optional)* **AAII + NAAIM overlay** — sentiment crowding.

Each chart caption ends with: `Source: <FRED series ID / yfinance ticker>, as of <YYYY-MM-DD>; composite computed in oneoff/market_complacency_<DATE>.py.`

### Step 5 — Write the report

Save to `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` under the project root. Target 3,000–5,000 words; structure:

1. **Complacency Verdict** — one-line bold verdict (e.g. **Stretched — composite 81 / 100, 95th percentile vs last 10 years**) + 50-word rationale naming the 2–3 most-stretched indicators.
2. **Composite Score & Tier** — table summarizing today's value vs the 5-tier bands, with the headline chart inline.
3. **Indicator-by-indicator table** — one row per indicator: current value, 10y min / median / max, complacency percentile, decile label, stretched flag (✓ / —).
4. **Cross-asset signature** — narrative paragraph identifying which categories (credit / equity vol / rate vol / risk-premium / sentiment / valuation) are corroborating the headline read and which are *not*. **Divergence between categories is the most important diagnostic** — when all six categories agree the regime is unusually persistent; when they disagree, the dashboard is mid-cycle, not late-cycle. Cite the specific indicators (with their percentile ranks) that support each category's assessment.
5. **Historical precedents** — table of up to 8 dates when the composite was within ±5 points of today, with SPY total return + max drawdown over the next 6 / 12 / 24 months. Closing paragraph: "the last *N* times the composite read X, the median 12m forward SPY return was Y%, with max drawdown Z%."
6. **What this verdict is NOT** — explicit caveat block:
   - Not a timing model — complacency can persist for quarters.
   - Not a sector / single-name call — the dashboard is macro.
   - Not a forecast — the precedents are base-rate reference, not prediction.
   - Calibration note: the dashboard described the regime *N* of *N* historical times; it predicted the *path* *0* of *N* times.
7. **Action implications** — what the verdict suggests for position sizing, hedge ratios, and cash levels. Concrete examples:
   - Stretched (80+): consider trimming long beta, raising cash, adding put-spread or VIX-call hedges; do not short outright (timing risk too high).
   - Elevated (60–80): tighten stops on the longest-duration positions; reduce CCC-rated credit exposure.
   - Neutral (40–60): standard policy weights.
   - Cautious (20–40): begin scaling into oversold long positions; reduce hedge ratios.
   - Panicked (0–20): aggressive long-bias re-entry (the contrarian-buy regime).
8. **What would invalidate this read** — concrete failure modes: regime-shift in monetary policy that re-rates the entire term structure (changes the meaning of the MOVE percentile), structural decline in CCC issuance shrinking the index (changes the CCC OAS distribution), persistent buyback bid distorting ERP. List the *specific* mechanical reasons the dashboard could mislead in the current macro context.
9. **`## Data Used / 数据来源清单`** manifest — sources, dates, freshness, and any optional indicators that failed to fetch.

### Step 6 — Verify and clean up

- Re-run the script; confirm it is idempotent (same date input → identical output).
- Spot-check ≥3 numbers in the report against the indicators CSV (`grep -F "<number>" oneoff/market_complacency_<DATE>_indicators.csv`).
- Confirm every percentile in the indicator table matches the script's output exactly.
- Confirm every precedent's forward-return numbers match the precedents CSV.
- Stop any test servers used during chart rendering.
- Commit and push per the project's standard workflow.

## Output Format (mandatory blocks)

Every report must contain:

1. **Complacency Verdict** at the top (bold, one line, with composite score and percentile rank).
2. **5-tier band table** showing today's score in context.
3. **Indicator-by-indicator table** — all 10 required (+ 0–3 optional) with current value, 10y context, complacency percentile, decile, stretched flag.
4. **Cross-asset signature paragraph** — which categories agree, which diverge.
5. **Historical precedents table** with SPY forward returns.
6. **6–10 embedded charts** with inline captions and source attribution.
7. **"What this verdict is NOT" caveat block.**
8. **Action implications block.**
9. **`## Data Used / 数据来源清单`** manifest.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Credit (required)**
- HY OAS — FRED `BAMLH0A0HYM2`, 10y history pulled via `indicators.data_fetcher._fetch_fred_range()`. As-of <YYYY-MM-DD>.
- IG OAS — FRED `BAMLC0A0CM`, same provenance.
- CCC OAS — FRED `BAMLH0A3HYC`, pulled directly in this script (not yet in the live dashboard).

**Equity volatility (required)**
- VIX (`^VIX`), VVIX (`^VVIX`), VIX9D (`^VIX9D`), VIX3M (`^VIX3M`), SKEW (`^SKEW`) — yfinance, 10y daily history (`auto_adjust=True`). As-of <YYYY-MM-DD>.

**Rate volatility (required)**
- MOVE Index (`^MOVE`) — yfinance, 10y daily history. Yahoo history starts ~2002.

**Risk-premium (required)**
- Equity Risk Premium — SPY trailing earnings yield (`yf.Ticker("SPY").info["trailingEps"]` ÷ current price) minus `^TNX/100`. As-of <YYYY-MM-DD>.
- HYG/LQD ratio — derived from yfinance daily closes, 10y history.

**Sentiment (optional)**
- AAII Bull-Bear Spread — weekly survey CSV from aaii.com. <fetched ✓ / failed ✗ — reason>
- NAAIM Exposure Index — weekly CSV from naaim.org. <fetched ✓ / failed ✗ — reason>

**Valuation (optional)**
- Shiller CAPE — monthly CSV from Robert Shiller's site (`http://www.econ.yale.edu/~shiller/data/ie_data.xls`). <fetched ✓ / failed ✗ — reason>

**Composite + percentile methodology**
- 10-year rolling percentile per indicator; complacency percentile inverted for "low = complacent" indicators (per the direction column).
- Weighted composite per the SKILL.md weight table; re-normalized to the active indicator set when optional indicators are missing.

**Historical precedents**
- Daily composite score 2000-01-01 → today, computed in `oneoff/market_complacency_<DATE>.py`.
- Forward returns: SPY adjusted close (`auto_adjust=True`), 6 / 12 / 24 month windows.

**Stale notices / coverage gaps**
- <bulleted list — e.g. "AAII survey CSV returned 403, sentiment category dropped from composite; weights re-normalized">.
- <e.g. "MOVE Index history begins 2002 — pre-2002 composite uses only the equity-vol indicators that have data">.
```

## Guardrails

- **Never call the Claude API or any LLM API.** Per [`CLAUDE.md`](../../../CLAUDE.md): the agent (Claude in this conversation) does the analysis directly; no `anthropic.Anthropic()`, no `openai`, no LLM client. The script is pure pandas + yfinance + urllib for the FRED / Shiller / AAII / NAAIM CSV fetches.
- **Never write to any `db/*.db` file.** Read-only against `db/indicators.db`. New indicators added by this skill live in `oneoff/` CSV cache files, not the project database. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".
- **Never silently drop a required indicator from the composite.** If HY OAS, IG OAS, CCC OAS, VIX, VVIX, VIX term slope, SKEW, MOVE, ERP, or HYG/LQD fails to fetch, the script must error out and the report must not be written. (Optional indicators — AAII, NAAIM, CAPE — are the only ones the report may degrade gracefully on.)
- **Never report a composite without disclosing the active indicator set.** If 3 of 13 indicators failed, the report must say "composite computed from 10 of 13 indicators" in the headline verdict and the Data Used block.
- **Never claim the dashboard predicts the *timing* of a regime turn.** It is a state read. Complacency can persist for quarters — the 2017 dashboard ran 80+ for most of the year before the Feb 2018 vol shock. The "What this verdict is NOT" block is mandatory and must say this explicitly.
- **Never extrapolate a single indicator into a regime call.** A low HY OAS alone is not "complacency" — it is *one* signal among twelve. The cross-asset signature paragraph is the report's load-bearing analysis; the headline verdict without it is misleading.
- **Never use absolute thresholds without percentile context.** "VIX is 12" means nothing without "which is the 7th percentile of the last 10 years". The indicator table must show both. Absolute levels rot as the regime evolves; percentiles are self-calibrating.
- **Never include indicators with <5y clean history in the composite.** Short-history indicators can be discussed narratively but cannot be weighted. CCC OAS itself was reconstructed by ICE in different eras; verify the FRED series goes back the full 10y before weighting it.
- **Never assert "this looks like 2007 / 2018 / 2020".** Let the precedents table do that work — list the dates with their forward returns and let the reader pattern-match. Naming specific historical analogs in the verdict is over-confident.
- **No "Source: our model" / "(estimate)" / "(本模型)"** anywhere. The composite is computed in `oneoff/market_complacency_<DATE>.py`; cite the script path for the composite, cite the underlying FRED / yfinance / AAII / NAAIM / Shiller URLs for the inputs.

## Output location

Save to `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` under the project root (create the `reports/market-complacency/` folder if missing — first report establishes the directory). The viewer at `http://localhost:5001/reports` will surface it under a new "MARKET-COMPLACENCY" type (or as "OTHER" until the viewer's bucket map is updated).

Supplementary deliverables sit in standard locations:

- Charts: `reports/charts/market_complacency_<DATE>_*.png`.
- Composite script + CSVs: `oneoff/market_complacency_<DATE>.py`, `oneoff/market_complacency_<DATE>_indicators.csv`, `oneoff/market_complacency_<DATE>_precedents.csv`. The script must be self-contained and re-runnable.
- Optional CSV caches: `oneoff/shiller_cape.csv`, `oneoff/aaii_sentiment.csv`, `oneoff/naaim_exposure.csv` — refreshable independently of the report.

### Update-in-place rule

One report per date. If `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` already exists for today's date, update it in place rather than creating a parallel copy. Across dates, keep separate files — the historical sequence of verdicts is itself useful context.

## What this skill does NOT do

- It does not pick a ticker — that's [[trader-plan]] / [[idea-generation]].
- It does not size a hedge — the "Action implications" block names the *kind* of hedge (put spread vs VIX call vs cash raise) but not the *dollar amount*. Sizing depends on portfolio context outside this skill.
- It does not forecast regime turns — see Guardrails.
- It does not analyze a specific sector's stress — [[sector-overview]] with a stress lens does that.
- It does not write the new indicators (CCC OAS, SKEW, MOVE, CAPE, AAII, NAAIM) into the live `indicators` dashboard at `localhost:5001`. That promotion is a separate engineering task; this skill keeps the additions scoped to the report run.

## Related skills

- [[take-profit-lab]] — single-ticker exit discipline. The macro complacency read is one input to the per-ticker exit decision.
- [[sector-overview]] — sub-sector stress; complements the macro dashboard.
- [[idea-generation]] — turns a "complacency is high" read into specific short / hedge candidates.
- [[portfolio-decision]] — final position rating; the complacency verdict is one of its macro inputs.
