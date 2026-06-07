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
| 3b | **CCC − HY OAS spread** (derived) | FRED `BAMLH0A3HYC − BAMLH0A0HYM2` | **Low** = complacent | Added in v2 after a backtest showed the original dashboard missed late-cycle credit-tier divergence. When CCC is wide *relative to* HY, the weakest tier is cracking even as broad HY stays tight — historically ~12 months before the 2007 turn and ~6 months before Q4 2018. Today's spread (June 2026) is at the 99th percentile, signaling divergence is in progress. |
| 3c | **Moody's BAA − 10Y Treasury** | FRED `BAA10Y` | **Low** = complacent | Added in v3. The ICE BofA OAS series (HY/IG/CCC) only go back to 2023-06 because FRED re-licensed them in mid-2023 — they have no pre-2023 history available, even with the FRED API key. BAA10Y is the canonical long-history IG-credit spread (1986-2026, 40 years, 10,000+ daily obs). Correlates 0.56 with IG OAS in their overlap window; runs ~70-80bp wider on average because BAA covers only the BBB tier whereas IG OAS blends AAA/AA/A/BBB. Including it gives the composite a genuine cycle-aware credit signal for pre-2023 dates that the ICE BofA series alone can't provide. |
| 3d | **Yield curve slope (10Y − 2Y)** | FRED `T10Y2Y` | **Low** = complacent | Added in v4 after reading Citi's BMC report (Jun 5, 2026). FRED daily data back to 1976. The most-cited bear-market lead indicator in finance — the curve has inverted before every US recession since 1969. Citi BMC reference points: Mar 2000 −50bp (red), Oct 2007 0bp (red), Feb 2020 +13bp (amber), Dec 2021 +90bp (off), today +41bp (off in their framework). The percentile-rank treatment in this dashboard captures the "late-cycle flattening" complacency case well; it does NOT cleanly distinguish between "deep inversion = recession warning" and "very steep = early cycle." Acceptable trade-off given a single-axis percentile is the dashboard's data model. |
| 3e | **S&P 500 Dividend Yield** | multpl.com monthly | **Low** = complacent | Added in v4 from Citi BMC. Long history (back to 1871 via Shiller). Low DY = stocks expensive relative to cash returns. Citi BMC thresholds: amber ~2.1%, red ~1.3%. Today's value 1.06% is at the 10y minimum (100% complacency). The interpretation overlaps with CAPE and ERP but DY is the simplest "yield-on-equity" measure and worth tracking separately because retail investors anchor on it. |
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
| HY OAS | 0.13 |
| IG OAS | 0.06 |
| CCC OAS | 0.08 |
| CCC − HY OAS spread | 0.05 |
| Moody's BAA − 10Y (long-history credit) | 0.05 |
| Yield curve (10Y − 2Y) | 0.05 |
| S&P 500 Dividend Yield (optional) | 0.05 |
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

These are pulled by the skill's reusable build script `scripts/build_dashboard.py` (see § Workflow Step 1). **Do not** modify the indicators module from this skill — keep the addition scoped to the report run. If the user later asks to promote one of these to the live dashboard, that is a separate task.

- **CCC OAS** — FRED series `BAMLH0A3HYC` (ICE BofA US CCC & Lower OAS). Pull via the existing `_fetch_fred_range()` helper.
- **SKEW** — yfinance `^SKEW`. Yahoo carries CBOE's daily SKEW back to 1990.
- **MOVE** — yfinance `^MOVE` (ICE BofAML US Bond Market OAS, the rate-vol analog of VIX). Yahoo data starts 2002.
- **Shiller CAPE** — Robert Shiller's Yale spreadsheet at `http://www.econ.yale.edu/~shiller/data/ie_data.xls` stopped refreshing in September 2023. The build script uses [`multpl.com/shiller-pe/table/by-month`](https://www.multpl.com/shiller-pe/table/by-month) as the primary live source (computationally equivalent) and falls back to the Yale spreadsheet only if multpl is unreachable.
- **AAII Bull-Bear** (optional) — weekly CSV at `https://www.aaii.com/files/surveys/sentiment.xls`. Cache locally; refresh weekly. As of late 2025 the public URL returns HTTP 403 — the build script logs the failure and re-normalizes weights over the active indicators.
- **NAAIM Exposure** (optional) — weekly XLSX at `https://www.naaim.org/wp-content/uploads/2014/04/NAAIM-Exposure-Index-Data.xlsx`. The legacy public URL currently returns HTTP 404; NAAIM moved distribution behind a member portal. Same graceful-degrade behavior as AAII.

### Derived indicators

- **Equity Risk Premium** — S&P 500 trailing earnings yield minus 10Y Treasury yield. The build script computes E/P as `100 / trailing PE` using the monthly trailing PE series from [`multpl.com/s-p-500-pe-ratio/table/by-month`](https://www.multpl.com/s-p-500-pe-ratio/table/by-month) (GAAP, fresh through the current month), then subtracts the monthly average of `^TNX` from yfinance. `yf.Ticker("SPY").info["trailingEps"]` is not reliable (returns `None` in many sessions) — do not depend on it. multpl is the canonical source.
- **HYG/LQD ratio** — `HYG.Close / LQD.Close` over 10 years; complacency percentile = rank vs trailing 10y.

### Database write rule (no exceptions)

This skill **only reads** from the indicators stack. Do **not** write to `db/indicators.db` or any other `db/*.db` — see [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety". If a new indicator needs persisting, the user must promote it to the live dashboard in a separate task that goes through `indicators/db.py`.

## Workflow

### Step 0 — Sanity check the request

Confirm the user wants a *macro / regime* read, not a single-ticker call. If the prompt names a ticker ("is NVDA complacent?"), redirect: this skill measures market-wide complacency; for single-name expensiveness use [[take-profit-lab]] or [[company-research]] § valuation.

If the user is asking specifically about *credit* complacency only (no equity/vol context), still run the full dashboard — the credit-only read is in the per-indicator table, and the cross-asset context is the report's edge over reading a single FRED chart.

### Step 1 — Run the build script

Steps 1-3 (pull required indicators, pull optional enrichment, find historical precedents) and Step 4 (chart generation) are all handled by the **reusable** build script at `.claude/skills/market-complacency/scripts/build_dashboard.py`.

Run it from the project root:

```bash
# As-of today (default)
python3 .claude/skills/market-complacency/scripts/build_dashboard.py

# Specific date
python3 .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07

# Different lookback window (default 10 years)
python3 .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07 --window-years 15
```

What it does:
1. Pulls 10 required + 3 optional indicators (HY/IG/CCC OAS via FRED; VIX/VVIX/VIX9D/VIX3M/SKEW/MOVE/HYG/LQD/SPY/^TNX via yfinance; S&P 500 trailing PE + CAPE via multpl; AAII/NAAIM via XLSX scrape).
2. Computes per-indicator 10-year complacency percentile (inverted for "low = complacent" indicators).
3. Builds the weighted composite (re-normalizing weights over the active indicators when optional ones are missing).
4. Computes the full daily historical composite back to ~December 2000 (saved to a CSV for charting and precedent matching).
5. Finds up to 8 spread-out precedents within ±5 of today's composite, computes SPY 6 / 12 / 24-month forward returns + max drawdown for each.
6. Renders 6–10 PNG charts to `reports/charts/market_complacency_<DATE>_*.png`.
7. Prints a structured JSON summary (composite, tier, active indicator count, output paths) to stdout.

Outputs (idempotent — same date input → same outputs):
- `oneoff/market_complacency_<DATE>_indicators.csv` — full per-indicator table.
- `oneoff/market_complacency_<DATE>_precedents.csv` — precedents with SPY forward returns.
- `oneoff/market_complacency_<DATE>_composite_history.csv` — daily composite back to ~2001.
- `oneoff/{sp500_trailing_pe,shiller_cape,aaii_sentiment,naaim_exposure}_<DATE>.csv` — per-source raw caches (date-stamped so reruns on different dates don't collide).
- `reports/charts/market_complacency_<DATE>_*.png` — 10 charts (composite, hy_oas, ig_ccc, vix_vvix, vix_slope, move, erp, indicators_bar, precedents, cape).

The script never writes to `db/*.db` and never calls an LLM API. All path resolution is via `Path(__file__).resolve().parents[4]` — runs unmodified from any working directory.

### Step 2 — Read the outputs

The agent (Claude in conversation) reads the three CSVs and the printed JSON summary, then writes the narrative report in Step 5. The build script does NOT write the report — that stays the agent's responsibility so the qualitative analysis (cross-asset signature paragraph, action implications, what-would-invalidate) gets fresh judgement each run.

### Step 3 — Inspect for surprises

Before writing the report, scan the indicator table for unexpected divergences. Two things to flag in the narrative:

1. **A material day-over-day move in any single indicator** — e.g. VIX jumping >25% on a single session. Compare the last 2-3 days of the composite history; a single bad day can drop the composite 10+ points entirely from the equity-vol axis.
2. **Cross-category divergence** — e.g. credit at tights but CCC widening, or equity vol at lows but SKEW elevated. The cross-asset signature paragraph (§ Step 5.4) lives or dies on identifying these.

### Step 4 — Chart inventory (already generated by the build script)

The build script in Step 1 already wrote all 10 charts to `reports/charts/market_complacency_<DATE>_*.png` at DPI 150 with `bbox_inches="tight"`. The full inventory the report should embed:

1. `*_composite.png` — composite, 2001–present, 5-tier bands shaded, today marked. **Headline chart.**
2. `*_hy_oas.png` — HY OAS, 25-year history with 5th / 50th / 95th 10y percentile reference lines.
3. `*_ig_ccc.png` — IG vs CCC overlay (dual-axis). Credit-tier divergence is visible here when present.
4. `*_vix_vvix.png` — VIX + VVIX overlay, last 10 years.
5. `*_vix_slope.png` — VIX term slope (VIX9D / VIX3M), last 10 years, with contango / backwardation bands.
6. `*_move.png` — MOVE Index, last 10 years.
7. `*_erp.png` — ERP (S&P 500 E/P − 10Y), 2001–present, negative regions shaded.
8. `*_indicators_bar.png` — per-indicator complacency percentile bar chart, with composite line.
9. ~~`*_precedents.png`~~ — REMOVED in v9 (was keyed to the dropped composite metric; 7 scattered points showed no pattern).
10. `*_cape.png` — Shiller CAPE, 2001–present, with reference line at CAPE 30.

Each chart caption in the report should end with:
`Source: <FRED series ID / yfinance ticker / multpl URL>, as of <YYYY-MM-DD>; composite computed in .claude/skills/market-complacency/scripts/build_dashboard.py.`

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

## Output Format (mandatory blocks — Citi BMC style)

The report must mirror the structure of [Citi's Bear Market Checklist report](https://www.citivelocity.com) — punchy summary box up top, single historical-calibration table, "Under the Hood" charts grid, brief action box, data manifest. **Target length: ~800-1,500 words of prose plus 10-12 charts plus 2-3 tables. Previous iterations ran 4,000-5,500 words and readers complained "too noisy, too long."**

Mandatory blocks, in this order:

1. **Dashboard's Take** — single bold blockquote at the top, ≤200 words. Mirrors Citi's "CITI'S TAKE" box. Structure:
   - **First line must be the flag count.** Example: `**Flag count 8 / 21 — Citi-BMC style: 7 red + 2 amber + 12 off.**` Backtest-validated metric (lift 1.32× at T=10, 1.90× at T=11).
   - 1-2 sentences naming the most-stretched indicators with absolute levels (e.g., "CAPE 41.6, S&P 500 DY 1.06%, Moody's BAA−10Y 1.54pp at or past pre-bear levels"), not percentile ranks.
   - 1-2 sentences on what's contra (yield curve positive, SKEW already bid, etc.)
   - 1 line on action (3-5 verbs)
   - 1 line on empirical base rate at this flag-count range (median fwd SPY, drawdown probability)
   - **No prose outside this block until after Figure 2.**
   - **The composite score is forbidden.** It was a hand-weighted average that the backtest proved is statistically uninformative (max lift 0.68× at 90d / 0.98× at 180d — at or below the base rate). Never mention it in Dashboard's Take or any headline. The composite chart is also forbidden from Figure 1; use the flag-count chart.

2. **Figure 1: Flag count + SPY overlay** — the headline chart, mirroring [Citi BMC Figure 1](https://www.citivelocity.com) which shows the BMC red-flag count alongside MSCI ACWI price. Required elements:

   - **Dual y-axis**: SPY price (left, blue), flag count 0–21 (right, red)
   - **Annotated reference dates**: March 2000, October 2007, Feb 2020, Dec 2021, and Now
   - **Two reference lines** on the flag-count axis: dashed at 10 (Citi's "double-digits = acceleration zone" — independently validated by this dashboard's backtest), dotted at 17.5 (Citi Mar-00 peak)
   - **Rangeselector buttons**: 1Y / YTD / 5Y / 10Y / ALL with `method='relayout'` and hardcoded date ranges (Plotly's `stepmode='todate'` is buggy)
   - **Bottom range-slider** for fine-grained zoom

   Markdown embed:
   ```html
   <iframe src="../charts/market_complacency_<DATE>_flag_count.html" width="100%" height="560" style="border:0;border-radius:6px;"></iframe>
   ```

   **The composite chart is forbidden** — do not embed `*_composite.html` or `*_composite.png` in any new report. The build script still generates them for legacy callers and time-series continuity in `oneoff/`, but they must not appear in the user-facing report.

   The viewer at `localhost:5001/claude-reports/` serves `.html` and `.htm` from `reports/` via the `_EMBED_EXTS` allowlist. Static markdown renderers (GitHub, Obsidian) will show the iframe as empty.

3. **`## Figure 2. Bear Market Checklist — Historical Calibration`** — a SINGLE comparison table mirroring Citi BMC Figure 2. Columns: Mar-00, Oct-07, Feb-20, Dec-21, **Now**. Rows: indicators grouped by category (Valuations / Yield Curve / Sentiment / Corp Behaviour / Profitability / Credit / Vol). Cells colored 🔴 red / 🟠 amber / off using standard thresholds. **A 🟢 marker is also valid** — use it for contra-signal off-flags (e.g., SKEW high, CCC spread wide, VIX backwardation) so the reader sees the cross-asset divergence at a glance.

   **Every indicator row must have a markdown link to the public source** for that indicator's historical chart: `[Indicator name](url)`. Reader should be able to click any row to verify the cited values against the canonical free chart (multpl, FRED, FINRA, Yahoo, Bain, Renaissance Capital, etc.).

   **Never use vague placeholders like "high" / "low" / "mid" when concrete numbers exist.** For each historical column, either (a) cite Citi BMC Figure 2's published number directly (Citi published the actual figures for valuation / M&A / IPO / RoE / capex / credit spreads — use them), (b) compute from the long-history source (Margin Debt from FINRA xlsx; HYG/LQD from yfinance for dates after HYG launched April 2007; BAA10Y from FRED back to 1986), or (c) explicitly cite the data limitation in italics next to the indicator name when no value is available (e.g., *"ICE BofA only 2023+"* or *"HYG launched April 2007"*).

   End with a 2-sentence "Today's calibration" paragraph: which historical references today matches, and what makes today distinctive (e.g., "no clean historical precedent — past bears started with one or the other, not both").

4. **`## Under the Hood`** — sequence of 8-12 small charts with one-line captions only. NO narrative paragraphs between charts. Charts in order: HY OAS, IG vs CCC overlay, CAPE, ERP, VIX/VVIX, VIX term slope, MOVE, per-indicator bars, precedents scatter. Each rendered by `scripts/build_dashboard.py` into `reports/charts/`.

   **Mandatory chart styling — bear-market shading** (Citi BMC Figure 3+ style). Every time-series chart must have light-grey vertical bars (`axvspan(alpha=0.20, color="#888888")`) over the major US bear-market windows so the reader has visual context for "what was happening in those periods." The build script defines `BEAR_PERIODS` and `_shade_bears(ax)` helper that applies five reference windows: 1990-07/10 (Iraq/recession), 2000-03/2002-10 (dot-com), 2007-10/2009-03 (GFC), 2020-02/2020-03 (COVID), 2022-01/2022-10 (Fed pivot). Charts that are NOT time-series (per-indicator bars, precedents scatter, etc.) skip the shading.

5. **`## Data Used / 数据来源清单`** — single source table grouping every indicator by category with its source URL. NO per-indicator paragraphs.

The user has explicitly rejected (v9 user feedback) the following blocks as not useful:
- ❌ Action Implications (the 5-row posture table) — the reader can derive postures from the flag count + Citi anchor; restating them in prose adds noise
- ❌ Historical Precedents (the date-by-date forward-return table) — small sample, noisy, no clean takeaway
- ❌ Backtest validation — precision numbers (~22% at T=10) are too low to motivate action; the report shouldn't read like a justification
- ❌ Caveats list — the bear-market shading on charts + the data-limitation italics in Figure 2 carry the necessary disclaimers; a separate prose section is redundant

Do NOT add these sections back unless the user explicitly asks. The report must end at Data Used.

### What NOT to include in Citi-style mode

The following blocks from prior iterations are explicitly *forbidden* in the new format unless the user asks for them:

- ❌ Long "Composite Score Decomposition" tables — implicit in Figure 2 calibration. If the reader wants the weighted math, they can run the script.
- ❌ Long "Cross-Asset Signature" narrative paragraphs — collapsed into the Dashboard's Take + Figure 2.
- ❌ "What This Verdict Is NOT" multi-paragraph block — collapsed into the Caveats list.
- ❌ "What Would Invalidate This Read" multi-paragraph block — collapsed into Caveats.
- ❌ Separate "Comparison to Citi BMC" section — Citi reference is implicit in Figure 2's column structure and one line in Caveats.
- ❌ Multiple postscript blocks documenting version-history — those belong in git commit messages and CHANGELOG, not in the live report.
- ❌ Per-chart narrative paragraphs interspersed between Under-the-Hood charts.
- ❌ Step-by-step verification logs as `<details>` blocks — moved to commit messages.
- ❌ **The composite score, anywhere.** The backtest proved it's statistically uninformative (max lift 0.68× at 90d / 0.98× at 180d — at or below base rate). Anywhere a single-number summary is needed, use the **flag count** (lift 1.32–2.41× at T=10-11). Do NOT write "composite 59 / Neutral" or "composite at top edge of Elevated." Do NOT embed the composite chart. Do NOT include tier-band tables keyed to composite ranges (0-20 Panicked / 20-40 Cautious / etc) — those bands have no empirical anchor. Use flag-count thresholds (0-4 / 5-7 / 8-9 / 10-11 / 12+) which DO have empirical anchors.

### Why flag count beats composite — confirmed by backtest

Backtest on SPY 2001-2026 (`oneoff/backtest_flag_vs_composite.py`):

| Property | Composite | Flag count |
|---|---|---|
| Computation | Weighted avg of 19 percentile ranks | Sum of binary thresholds |
| Weight sensitivity | Doubling any weight shifts score 5-10 points | Doubling weights changes nothing |
| Indicator correlation | Triple-counts correlated signals | Same — but the discrete count makes it visible |
| Time-scale issue | Averages CAPE (decadal) and VIX (seconds) | Each tier is independent — no averaging |
| Mean compression | Always lands near 50 with 19 inputs | Bimodal — many indicators clustered red/amber or all off |
| **Empirical lift (90d, -10% dd)** | **Max 0.68×** at T=40 — *worse than random at every threshold* | **1.32× at T=10, 1.90× at T=11** |
| **Empirical lift (180d, -15% dd)** | **Max 0.98×** at T=70 | **1.78× at T=10, 2.41× at T=11** |
| Cross-asset divergence | Hidden by the average | Visible as `7 red + 2 amber + 12 off` |
| Interpretability | "What does 59.5 mean?" | "8 indicators flagging vs Mar-00's 17.5" — direct historical anchor |
| Citi's published anchor | None | "Double-digits = acceleration zone" — independently confirmed by this backtest |

The composite is statistically uninformative. The flag count at ≥10 has roughly 2× the base-rate probability of preceding a meaningful drawdown.

### Rationale for the Citi-style rewrite (v7)

User feedback over multiple iterations: "too noisy, format messy, and too long; use exact Citi report style; after Figure 2 BMC table, then have under the hood table, it is much easier to visualize." The new format does three things:

1. **Front-loads the conclusion** — Dashboard's Take + Figure 2 give the reader the entire verdict in the first scroll. Total time-to-decision under 1 minute.
2. **Maximizes information density per scroll** — single big calibration table + visual grid of charts replaces 3,000 words of cross-asset narrative.
3. **Mirrors a format institutional readers already trust** — Citi's BMC layout is decades-old and well-tested. Aligning the visual structure makes the dashboard's reading directly cross-referenceable with the most-cited sell-side framework.

The deeper analytical detail (per-indicator percentile context, composite weights, backtest stats) lives in `scripts/build_dashboard.py` and `oneoff/*.csv` for readers who want to dig in. The *report* is the daily-scan artifact.

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
- Daily composite score 2000-01-01 → today, computed by `.claude/skills/market-complacency/scripts/build_dashboard.py`.
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
- **No "Source: our model" / "(estimate)" / "(本模型)"** anywhere. The composite is computed in `.claude/skills/market-complacency/scripts/build_dashboard.py`; cite the script path for the composite, cite the underlying FRED / yfinance / multpl / AAII / NAAIM URLs for the inputs.
- **ICE BofA OAS series window — real upstream restriction.** When the build script has access to a FRED API key (via `config.FRED_API_KEY`), it uses the JSON API for reliable pulls. Investigation in v3 confirmed the limited-history issue is NOT a CSV truncation — it's the actual series. The series metadata for `BAMLH0A0HYM2` / `BAMLC0A0CM` / `BAMLH0A3HYC` declares `observation_start: 2023-06-06` because ICE BofA re-licensed the indices in mid-2023 and FRED's pre-2023 archive was retired. Even the API key cannot recover pre-2023 history for these series. **The dashboard's mitigation is the v3 addition of Moody's BAA−10Y** (FRED `BAA10Y`, 1986-2026, ~10,000 daily obs) which is the canonical long-history IG-credit spread and gives the composite genuine cycle-aware credit context for pre-2023 dates. Every report must disclose this constraint in the Data Used section. The non-FRED indicators (VIX/VVIX/SKEW/MOVE/HYG/LQD/CAPE/ERP) are not affected.

## Output location

Save to `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` under the project root (create the `reports/market-complacency/` folder if missing — first report establishes the directory). The viewer at `http://localhost:5001/reports` will surface it under a new "MARKET-COMPLACENCY" type (or as "OTHER" until the viewer's bucket map is updated).

Supplementary deliverables sit in standard locations:

- Charts: `reports/charts/market_complacency_<DATE>_*.png`.
- Composite build script: `.claude/skills/market-complacency/scripts/build_dashboard.py` (reusable across dates via `--date YYYY-MM-DD`). Generated CSVs: `oneoff/market_complacency_<DATE>_indicators.csv`, `oneoff/market_complacency_<DATE>_precedents.csv`, `oneoff/market_complacency_<DATE>_composite_history.csv`. The script is self-contained and idempotent.
- Date-stamped CSV caches written by the build script: `oneoff/sp500_trailing_pe_<DATE>.csv`, `oneoff/shiller_cape_<DATE>.csv`, `oneoff/aaii_sentiment_<DATE>.csv`, `oneoff/naaim_exposure_<DATE>.csv`. Reruns on the same date are free; reruns on a different date re-fetch from source.

### Update-in-place rule

One report per date. If `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` already exists for today's date, update it in place rather than creating a parallel copy. Across dates, keep separate files — the historical sequence of verdicts is itself useful context.

## Comparison to Citi's Bear Market Checklist (BMC)

Every report must include a cross-reference to Citi's BMC when a current edition is available (Citi publishes refreshes ~quarterly). The BMC is the institutional analog of this dashboard with 18 indicators across valuation / yield curve / sentiment / corporate behaviour / profitability / balance sheets-and-credit. The skill's `scripts/build_dashboard.py` outputs a Citi-BMC-style **flag count** (amber if complacency_pct ≥ 60, red if ≥ 80; total = 0.5 × n_amber + 1.0 × n_red) alongside the continuous composite, so cross-comparison is direct.

Citi historical reference flags (cite when relevant):

| Date | Citi BMC flags / 18 | Note |
|---|---:|---|
| Mar 2000 | 17.5 | Dot-com peak |
| Oct 2007 | 13 | Pre-GFC peak |
| Feb 2020 | 5.5 | Pre-COVID peak (interesting that this was low) |
| Dec 2021 | 8.5 | Post-COVID peak |
| Jun 2026 | 10 (Global), 11.5 (US), 5 (Europe) | "Frothiest since GFC, not yet overexuberant" |

Citi's explicit guidance: "once the count reaches double digits, it has historically tended to rise more rapidly." That heuristic should be quoted in any report whose flag count is approaching 10 (this dashboard's proportional equivalent is ~8.4/15).

### BMC indicators — what we have and what's still missing

**Shipped in v5 from free public sources:**

| Citi BMC factor | This dashboard equivalent | Data source |
|---|---|---|
| EPS from previous peak | `eps_peak`: EPS distance from rolling 10y max | [multpl monthly trailing EPS](https://www.multpl.com/s-p-500-earnings/table/by-month) |
| Capex Growth (YoY) | `capex_yoy`: US PNFI YoY | FRED `PNFI` (quarterly back to 1947) |
| (Levkovich component) Margin debt | `margin_debt_pct`: FINRA margin debt / S&P 500 level | [FINRA margin-statistics.xlsx](https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx) |
| (Levkovich component) Put/Call | `put_call`: CBOE equity put/call 21d MA | [cdn.cboe.com equitypc.csv](https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv) (stale Oct 2019; useful for backtest only) |

**Shipped in v6 via WebSearch-sourced annual data (cached in `oneoff/`):**

| Citi BMC factor | This dashboard equivalent | Data source |
|---|---|---|
| IPO Activity (% of Mkt cap) | `ipo_pct`: annual US IPO proceeds / SPX level | [Renaissance Capital IPO Stats page](https://www.renaissancecapital.com/IPO-Center/Stats) → manually cached `oneoff/ipo_proceeds_annual.csv` |
| M&A Activity (% of Mkt cap) | `ma_pct`: annual US M&A volume / SPX level | [Bain 2025 M&A report](https://www.bain.com/about/media-center/press-releases/20252/global-ma-stages-great-rebound-in-2025-with-$4.8-trillion-deal-value-to-mark-second-highest-total-on-record) + [S&P Global Q1 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/global-m-and-a-by-the-numbers-q1-2026) → manually cached `oneoff/ma_volume_annual.csv` |

**Refresh workflow for v6 indicators**: each report run, the agent uses WebSearch to find:
- "Renaissance Capital 2026 YTD IPO count proceeds" — update last row of `ipo_proceeds_annual.csv`
- "Bain global M&A 2026 Q1 announced volume" — update last row of `ma_volume_annual.csv`

The annual data is forward-filled to monthly in the build script (`scripts/build_dashboard.py` `fetch_ipo_pct` / `fetch_ma_pct`). The percentile rank is computed against the trailing 10y monthly window so the indicator behaves like every other one in the composite. **Note that today's readings (IPO 7th decile, M&A 8th decile) are NOT complacent** — deal-making activity in 2026 is well below 2021 peaks despite valuation extremes.

**Still in the backlog (need paid feeds or non-trivial engineering):**

| Citi BMC factor | Tried | Status |
|---|---|---|
| Forward PE | multpl 404; gurufocus 403; Yardeni PDF binary extraction failed; macromicro current value via WebSearch | WebSearch returns a current snapshot (22-26 range across sources) but no clean free historical CSV. v7 candidate: hardcode current value with confidence interval, compute proxy historical via SPX/multpl-trailing-EPS × consensus-EPS-growth-forecast |
| Aggregate RoE | yfinance per-constituent rollup; SPDR S&P 500 fundamentals page | 500-ticker rollup expensive; need a cached pipeline. Backlog. |
| Analyst Bullishness | Refinitiv I/B/E/S | Paywall |
| Levkovich Index | Citi proprietary | Components partly approximated by margin debt + put/call; full reconstruction needs ETF flows + analyst data |
| Equity Fund Flows | Lipper, EPFR, ICI | ICI has monthly mutual-fund flow data free but not equity-specific in tractable format |
| Asset/Equity (Financials) | XLF holdings, FactSet | XLF rollup computable but per-constituent balance-sheet data needed |
| Net Debt/EBITDA (ex-Fins) | FactSet | Paywall |

When data sources are added in future versions, run the standard backtest discipline (see below) to validate they improve the predictive metric on top of v4.

## Backtest discipline

A backtest script lives at `.claude/skills/market-complacency/scripts/backtest_dashboard.py`. Run it against any composite history CSV to validate or invalidate dashboard changes:

```bash
python3 .claude/skills/market-complacency/scripts/backtest_dashboard.py \
  --composite-history oneoff/market_complacency_<DATE>_composite_history.csv \
  --benchmark SPY \
  --as-of <DATE>
```

The June 2026 backtest (see [`reports/market-complacency/backtest_2026-06-07.md`](../../../reports/market-complacency/backtest_2026-06-07.md)) found:

- **The Stretched tier (80+) is the only tier with predictive lift** — precision 22% vs 20% base rate (lift 1.10) on the 90-day -10% drawdown event. The 60-80 Elevated tier is empirically indistinguishable from Neutral.
- **The dashboard hit 4 of 7 major SPY drawdowns at the peak; 8 of 11 on QQQ.** The structural misses (GFC, 2022 bear, COVID) were exogenous-shock events the dashboard cannot see by construction.
- **The dashboard is a *regime descriptor*, not a *drawdown predictor*.** Report writeups must calibrate expectations accordingly — quote the empirical drawdown probabilities at today's tier from the backtest, not anecdotal "this looks like 2007" comparisons.

Any change to the indicator set or weights must be validated by re-running the backtest BEFORE shipping. The v2 dashboard (adding CCC − HY OAS spread) was kept after the backtest showed it modestly improved the Stretched-tier lift (1.01 → 1.10) and produced a more accurate read on the 2026-06-07 regime (Neutral, not Elevated). Future indicator additions (% S&P above 200dma, composite rate-of-change, sentiment proxies) must clear the same bar.

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
