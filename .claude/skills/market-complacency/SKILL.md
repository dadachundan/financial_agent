---
name: market-complacency
description: Score how much risk the market is currently under-pricing — a composite "complacency dashboard" of credit spreads (HY/IG/CCC OAS), equity vol (VIX, VVIX, VIX term slope, SKEW), rate vol (MOVE), risk-premium compression (ERP, HYG/LQD), sentiment (AAII bull-bear, NAAIM exposure, put/call), breadth (% above 200dma), and valuation (Shiller CAPE). Each indicator gets a percentile rank vs its own 10-year history; a low percentile on a "low = risk under-priced" indicator counts as complacency. Produces an ~800–1,500 word English markdown report in Citi-BMC style: a headline **flag count** (X red + Y amber / N indicators), a historical-calibration table (Mar-00 / Oct-07 / Feb-20 / Dec-21 / Now), and 8–12 interactive charts. Use when the user asks "is the market complacent?", "is risk under-priced right now?", "are credit spreads too tight?", "where are we vs 2007 / January 2018 / Q1 2020?", or anything in the under-priced-risk / late-cycle / euphoria family.
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

The skill produces a Citi-BMC-style **flag count** headline (`X red + Y amber / N indicators`) backed by a per-indicator breakdown of which signals are flashing and which are not.

## When NOT to use

- The user wants a single-ticker call — use [[trader-plan]] / [[portfolio-decision]] / [[take-profit-lab]].
- The user wants to know *what to short* — this skill says "risk is mispriced", not "here is the vehicle". Hand off to [[idea-generation]] for short-bias screens.
- The user wants the inverse — a *panic / capitulation* read. This skill handles both ends of the same axis: the verdict tier "Panicked" maps to the bottom decile of the same composite score. There is no separate "/market-fear" skill.
- The question is about a single sector's stress (e.g. "are regional banks in trouble?") — use [[sector-overview]] with a stress lens; the macro complacency dashboard won't pick up sub-sector dislocation.
- The user wants a forecast of *when* the regime turns — this skill is a **state read**, not a timing model. Complacency can persist for quarters; the dashboard tells you the regime, not the trigger.
- The user asks about equity-market exuberance/froth through the GS Kickstart lens (Momentum factor returns, IPO counts, speculative-trading indicator, net equity issuance) — that is [[market-status]]. This skill is the cross-asset risk-UNDER-PRICING lens (credit spreads, vol, risk premia); the two are complementary, not interchangeable.

## Core methodology

### The complacency axis — flag count is the headline metric

For each indicator, define a direction such that **higher complacency percentile = more complacent** (risk under-priced). The headline metric is the Citi-BMC-style **flag count** (per `scripts/build_dashboard.py`):

- **Red (full flag, 1.0)** — complacency percentile ≥ 80 (most-complacent quintile vs own 10y history)
- **Amber (half flag, 0.5)** — complacency percentile ≥ 60
- **Flag count = n_red + 0.5 × n_amber**, reported over the active flag-eligible denominator (`flag_max` in the indicators CSV)

Empirically anchored flag-count bands (see § "Why flag count beats composite"): **0–4** quiet / **5–7** building / **8–9** elevated / **10–11** acceleration zone (lift 1.32–1.90× on 90d −10% drawdowns) / **12+** extreme. Citi's published heuristic: "once the count reaches double digits, it has historically tended to rise more rapidly."

A weighted composite 0–100 is still computed internally by the build script (for backtest continuity and the historical CSV) but it is **never reported** — the backtest proved it statistically uninformative (max lift 0.68×; see § Output Format and § "Why flag count beats composite").

### Indicators (the dashboard)

Twelve indicators across six categories. The "complacency direction" column states whether *low* or *high* readings count as complacency.

| # | Indicator | Source | Complacency direction | Why it signals complacency |
|---|---|---|---|---|
| **Credit (under-pricing default risk)** | | | | |
| 1 | **HY OAS** (ICE BofA US High Yield) | FRED `BAMLH0A0HYM2` | **Low** = complacent | Bottom-decile HY spreads have historically preceded credit-cycle turns (Q2 2007 at 2.4%, Jan 2020 at 3.4%) |
| 2 | **IG OAS** (ICE BofA US Corporate) | FRED `BAMLC0A0CM` | **Low** = complacent | Same logic, investment-grade tier |
| 3 | **CCC OAS** (ICE BofA US CCC & Lower) | FRED `BAMLH0A3HYC` | **Low** = complacent | The weakest tier — the first to widen when the cycle turns. Bottom-decile CCC = the strongest single-indicator complacency tell |
| 3b | **CCC − HY OAS spread** (derived) | FRED `BAMLH0A3HYC − BAMLH0A0HYM2` | **Low** = complacent | Added in v2 after a backtest showed the original dashboard missed late-cycle credit-tier divergence. When CCC is wide *relative to* HY, the weakest tier is cracking even as broad HY stays tight — historically ~12 months before the 2007 turn and ~6 months before Q4 2018. Today's spread (June 2026) is at the 99th percentile, signaling divergence is in progress. |
| 3f | **BB − B OAS dispersion** (derived) | FRED `BAMLH0A1HYBB − BAMLH0A2HYB` | **Low** = complacent | Added in v11, mirroring **GS Global Credit Trader's** credit-tier dispersion framework (BB-vs-B differential near record = "quality-chasing within HY"). A *tight* BB−B differential means investors are reaching down the quality ladder for yield — the late-cycle quality-chasing tell that broad HY OAS hides. *Where FRED's post-2023 ICE BofA window blocks the BB/B sub-indices, document the limitation inline (same muscle as the BAA10Y workaround) and fall back to the CCC−HY tier where available.* |
| 3g | **Rising-star / fallen-angel net $** (narrative) | Moody's / S&P public rating-migration releases (web-searched per run) | wide net-fallen-angel = complacent | Added in v11 as a *narrative cross-check*, not a weighted flag, per **GS Global Credit Trader**. When fallen-angel $ volume exceeds rising-star $ volume while HY OAS stays tight, the weakest credit is migrating *down* even as prices stay calm — the cross-asset divergence diagnostic the skill prizes. Quote the net $ figure with its source-chain link; do not weight it (no clean long-history series). |
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
| **Speculative & Leverage Positioning** (added v11 — see § "Learning from sell-side institutional research") | | | | |
| 14 | **CFTC asset-manager / managed-money net S&P 500 e-mini futures** | CFTC Commitments-of-Traders (free weekly) | **High** net-long = complacent | The single biggest gap-fill. Mirrors **UBS's** "asset-manager S&P 500 futures net long near 10-yr record / 95th percentile" gauge. Percentile-rank the net-long position vs 10y. Restores the positioning axis that is currently dark because AAII + NAAIM both fail to fetch. Source via the free CFTC weekly Legacy / TFF report; cite the report URL and percentile per project rules. |
| 15 | **FINRA margin debt ÷ S&P 500 level** | FINRA margin-statistics.xlsx (already cached for Figure 2) | **High** = complacent | Promote the already-cached margin-debt series from the Figure-2-only set into the active positioning flag. Mirrors **MS / GS-EM** "margin-financing balances at record" gauge. Margin-debt-to-index near 10y high = leveraged crowding. No new fetch needed — the data is already pulled. |
| 16 | **CBOE equity put/call (21d MA)** | CBOE equitypc.csv (already cached) | **Low** ratio = complacent | Already cached; promote to the active positioning set. A low 21-day put/call MA = no hedging demand, the options-market positioning corollary of low VVIX. |

**Required vs optional**. Indicators 1–10 are *required* — the composite score must include all ten. Indicators 11–13 are *optional* enrichment — if the upstream CSV is unreachable, drop them from the composite and disclose in the Data Used manifest. Never silently degrade the score without telling the reader. Indicators 14–16 (Speculative & Leverage Positioning, added v11) are also *optional* enrichment: 15 (FINRA margin debt) and 16 (CBOE put/call) reuse data already cached for Figure 2, so they should populate whenever those caches do; 14 (CFTC net-long) requires a fresh weekly pull and degrades gracefully if the COT feed is unreachable. Before adding any of 14–16 to the *weighted* composite, run the standard backtest discipline (see § "Backtest discipline") — until validated, surface them as Figure 2 / narrative flags only, not weighted composite inputs, so the backtest-validated flag set is not diluted.

### Per-indicator percentile mapping

For each indicator with at least 5 years of clean history (target: 10 years), compute:

1. **Current value** — most recent valid observation.
2. **10-year percentile rank** — where today sits in the distribution of the last 10 years. For "low = complacent" indicators, *complacency percentile = 100 − value percentile*; for "high = complacent" indicators, *complacency percentile = value percentile*.
3. **Decile label** — "1st decile (most complacent)" / "5th (median)" / "10th (least complacent)".
4. **Stretched flag** — true if the complacency percentile ≥ 90 (i.e. today is in the most-complacent decile vs the last 10 years for this indicator).

### Composite score (internal / backtest artifact — NEVER reported)

The build script computes a weighted average of complacency percentiles for backtest continuity and the daily-history CSV only. **It must never appear in the report** (see § Output Format — "The composite score, anywhere" is forbidden). Weights, kept for script documentation (calibrated from 2000–2025, summing to 1.0):

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

### Historical precedents (internal — NOT a report block)

The build script still computes composite-proximity precedents (dates within ±5 points, with SPY 6/12/24-month forward returns) into `oneoff/market_complacency_<DATE>_precedents.csv`. **The precedents table was removed from the report format in v9 (user-rejected — small sample, noisy, no clean takeaway; see § Output Format).** Use the CSV only as background context when writing the Take's base-rate line; never embed the table.

## Learning from sell-side institutional research

The skill's direct analog is **Citi's Bear Market Checklist (BMC)** — already mirrored in Figure 2's column structure and the flag-count headline. A methodology pass across 38 sell-side complacency reports (Citi BMC, UBS Global Strategy, J.P. Morgan US High Grade Credit, GS Global Credit Trader / Mortgage & Structured Products Trader / Weekly Fund Flows, MS / Bernstein Asia positioning, Nomura macro-stress) surfaced concrete, transferable upgrades. Apply these — they sharpen *what the dashboard reads* and *how the Take is phrased*, without bloating the Citi-style report.

**Add a Speculative & Leverage Positioning category (highest-value gap).** The skill's only positioning inputs (AAII, NAAIM) BOTH fail to fetch (403 / 404), so the entire positioning axis is currently dark — yet **UBS / JPM-Asia / MS** treat positioning percentiles as a *first-class, often leading* complacency signal. Fill it from feeds the skill can actually reach: CFTC Commitments-of-Traders asset-manager net S&P 500 e-mini (UBS's "95th percentile, near 10-yr record" gauge), FINRA margin-debt ÷ S&P 500 (already cached — promote it), and the cached CBOE put/call 21d MA. See INDICATORS rows 14–16.

**Read credit-tier dispersion beyond CCC−HY (GS Global Credit Trader).** The sharpest "quality-chasing inside HY" tell is the BB−B OAS differential, plus a rising-star / fallen-angel net-$ narrative cross-check. A *tight* BB−B differential = investors reaching down the quality ladder; a wide one = the weakest tier cracking under a calm HY headline. See INDICATORS rows 3f–3g. Where the post-2023 ICE BofA FRED window blocks the BB/B sub-indices, document the limitation inline and fall back to CCC−HY.

**Distinguish "tight and complacent" from "tight and earned" (JPM US High Grade core method).** Tight spreads alone don't prove complacency — JPM's whole argument is whether the tightness is *justified* by leverage / coverage / rating migration. In the Figure 2 "Today's calibration" paragraph, pair the credit flag with one free fundamental anchor (FRED nonfinancial-corporate-debt/GDP, or BBB-share-of-IG / Moody's downgrade-upgrade direction). Direction: tight spreads + deteriorating leverage = genuinely complacent; tight spreads + improving coverage = less alarming. Keep to the published-number standard (every figure string-matches its cited URL).

**Always carry a forward, NAMED invalidation trigger (UBS convention).** UBS never ships a complacency read without a specific threshold that would flip the regime ("spreads widen non-linearly IF breakeven inflation breaks 2.65–2.75% or the supply-chain index +1.2σ"). The Citi-style rewrite deleted the old "what would invalidate" block — a real regression vs the analog. v11 re-adds it as ONE sentence at the end of the Dashboard's Take box (see § Output Format block 1). Name the level, the indicator, and where to verify it — not a paragraph.

**Lead the Take with the gauge's own-history percentile, THEN the absolute level (UBS / JPM / Citi house phrasing).** Institutions state the percentile first — "US IG at the 2nd percentile, extremely tight (96bp)" — not "96bp, which is low." The skill already computes percentiles; sharpen the most-stretched-indicators sentence in the Dashboard's Take to name the 1–2 most-stretched indicators' OWN-history percentiles, not just absolute levels.

**Promote index concentration / breadth into the active set (Bernstein Asia Quant, GS / MS strategy).** Every Asia-strategy and quant note leads with concentration (top-5 = 66% of cap; growth-vs-value dispersion at decade extreme). The skill lists "% above 200dma" as backlog but never ships it. Add a top-10 S&P 500 weight or %-above-200dma flag (both computable free) — narrow breadth under new highs is a textbook complacency divergence. See § "BMC indicators" backlog → shipped.

**Add a weekly fund-flow direction read (GS Weekly Fund Flows / JPM EM Money Trail).** Persistent large inflows into risk = complacent; outflows = de-risking. Use a free proxy the skill can fetch (ICI weekly equity-fund flows, or a HYG/LQD/SPY AUM-flow proxy from yfinance), percentile-rank the 4-week trend. "Large weekly outflows historically precede index weakness" (GS). Narrative cross-check, not necessarily a weighted flag.

**Carry the GSCPI macro-stress lead as a narrative cross-check (Nomura).** The NY Fed Global Supply Chain Pressure Index is free (FRED-mirrored) and gives a forward macro-stress read the price series can't see by construction. State Nomura's empirical lead rule with its horizon: "inflation peaks ~6 months after the supply-chain-pressure peak." Use it in the Figure 2 calibration narrative, not as a weighted flag, so it doesn't dilute the backtest-validated flag set.

**Cross-check market calm against consumer-credit delinquencies (GS Mortgage & Structured Products Trader).** A calm-price / rising-delinquency divergence is a documented complacency tell the macro vol/credit series miss. Add a one-line cross-check from free FRED series (credit-card delinquency `DRCCLACBS`, auto delinquency `DRALACBS`); flag the UMich-confidence-vs-delinquency divergence GS highlights. Low weight / narrative only.

**Structural / analytical conventions to mirror, from the analog set:**
- **Surface cross-category divergence explicitly** (calm vol + cracking credit tier). Both Citi BMC and GS Credit Trader make tier/category divergence the *headline* diagnostic — the skill already prizes this; keep it load-bearing.
- **Pair each price signal with its fundamental backdrop in the same block** (JPM: "tight spreads + 1.1x leverage") so the reader judges whether tightness is earned.
- **State empirical lead/lag rules with their horizon** ("inflation peaks ~6mo after GSCPI peak"; "flag count tends to accelerate past 10") so the reader gets a base rate, not a forecast — consistent with the existing "let the calibration table do the analogizing" guardrail.
- **Treat positioning percentiles and flows as LEADING, not lagging, signals** — UBS notes the largest spread-compression historically happens when CTAs were SHORT, i.e. positioning *context* changes the signal's meaning. Read positioning alongside price, not as confirmation of it.

Implementation order: positioning category (rows 14–16) + credit-tier dispersion (rows 3f–3g) + the named invalidation trigger are the **high-priority** items already wired into the table and Output Format above. The credit-fundamental overlay, fund-flow, GSCPI, concentration, and consumer-credit items are **medium/low-priority narrative cross-checks** — add them in the Figure 2 calibration paragraph or as optional rows, keeping every value percentile-calibrated and source-cited per project rules, and *never* diluting the backtest-validated flag set with unvalidated weighted flags.

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

**Positioning, flows & breadth (added v11 — see § "Learning from sell-side institutional research"):**

- **CFTC Commitments-of-Traders** (positioning) — free weekly Legacy / Traders-in-Financial-Futures report (`https://www.cftc.gov/dea/newcot/FinFutWk.txt` and the COT report pages). Pull asset-manager / managed-money net S&P 500 e-mini futures; percentile-rank the net-long vs 10y (UBS "95th percentile" gauge). Restores the positioning axis that AAII + NAAIM leave dark.
- **Index concentration / breadth** — top-10 S&P 500 weight and/or `% of S&P 500 above its 200-day MA`, both computable free from yfinance constituents (move from the backlog table below into the active set; narrow breadth under new highs is a textbook complacency divergence — every Bernstein / GS / MS Asia note leads with it).
- **Weekly fund-flow direction** — free proxy via ICI weekly equity-fund flows, or a HYG/LQD/SPY AUM-flow proxy from yfinance; percentile-rank the 4-week trend (GS Weekly Fund Flows / JPM EM Money Trail). Persistent risk-on inflows = complacent. Narrative cross-check.
- **NY Fed Global Supply Chain Pressure Index (GSCPI)** — free, FRED-mirrored (`GSCPI`). Macro-stress lead with Nomura's "+6-month inflation lead" rule. Narrative cross-check in the Figure 2 calibration, not a weighted flag.
- **Consumer-credit delinquencies** — FRED credit-card `DRCCLACBS` and auto `DRALACBS` delinquency rates. Calm market prices alongside rising delinquencies = a documented complacency divergence (GS Mortgage & Structured Products Trader). One-line cross-check, not a weighted flag.

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
/opt/anaconda3/bin/python3 .claude/skills/market-complacency/scripts/build_dashboard.py

# Specific date
/opt/anaconda3/bin/python3 .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07

# Different lookback window (default 10 years)
/opt/anaconda3/bin/python3 .claude/skills/market-complacency/scripts/build_dashboard.py --date 2026-06-07 --window-years 15
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

1. ~~`*_composite.png`~~ — **BANNED from the report** (composite is forbidden anywhere; see § Output Format). The script currently still generates it — see Guardrails: remove or gate behind `--debug`; never embed.
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
`Source: <FRED series ID / yfinance ticker / multpl URL>, as of <YYYY-MM-DD>; flag count and percentiles computed in .claude/skills/market-complacency/scripts/build_dashboard.py.`

### Step 5 — Write the report

Save to `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` under the project root.

**The single source of truth for the report's structure, length, and banned blocks is § "Output Format (mandatory blocks — Citi BMC style)" below.** Follow it exactly: Dashboard's Take → Figure 2 calibration table → Under the Hood charts → (optional Further viewing) → Data Used. Do NOT resurrect the pre-v7 9-block format (Complacency Verdict / Composite Score & Tier / Cross-asset signature / Historical precedents / Action implications / What-would-invalidate) — every one of those blocks was explicitly removed in the v7–v9 Citi-style rewrite and several were user-rejected by name.

### Step 6 — Verify and clean up

- Re-run the script; confirm it is idempotent (same date input → identical output).
- Spot-check ≥3 numbers in the report against the indicators CSV (`grep -F "<number>" oneoff/market_complacency_<DATE>_indicators.csv`).
- Confirm every percentile in the indicator table matches the script's output exactly.
- **Grep the Take's base-rate numbers against the backtest artifact before committing** (`grep -F "<number>" oneoff/backtest_flag_vs_composite_<DATE>.csv` or the linked backtest file) — an unsourced base-rate line violates the project's numerical-accuracy rule.
- **Open ≥2 generated PNGs (one dashboard chart, one backtest chart) and confirm (a) the in-image source footer is present and (b) the title's stated time span matches the plotted data span.**
- Stop any test servers used during chart rendering.
- Commit and push per the project's standard workflow.

## Output Format (mandatory blocks — Citi BMC style)

The report must mirror the structure of Citi's Bear Market Checklist report (cite the current edition via the local zsxq library — see § "Comparison to Citi's Bear Market Checklist (BMC)"; **never link the citivelocity.com homepage**) — punchy summary box up top, single historical-calibration table, "Under the Hood" charts grid, brief action box, data manifest. **Target length: ~800-1,500 words of prose plus 10-12 charts plus 2-3 tables. Previous iterations ran 4,000-5,500 words and readers complained "too noisy, too long."**

Mandatory blocks, in this order:

1. **Dashboard's Take** — single bold blockquote at the top, ≤200 words. Mirrors Citi's "CITI'S TAKE" box. Structure:
   - **First line must be the flag count.** Example: `**Flag count 7.5 / 19 — Citi-BMC style: 7 red + 1 amber + 11 off.**` Backtest-validated metric (lift 1.32× at T=10, 1.90× at T=11). **The denominator is the number of active flag-eligible indicators on the run date — read it from the `flag_max` column of `oneoff/market_complacency_<DATE>_indicators.csv`, never hardcode it.** Always state the denominator, and never compare raw counts across dates with different denominators without noting the change.
   - **One trajectory sentence** sourced from the flag-count history CSV (`oneoff/market_complacency_<DATE>_flag_count_history.csv`): where today's count sits vs its own history ("highest since <date>" or percentile since 2001) and the 1-month direction — Citi's house framing ("frothiest since the GFC, with flags rising steadily"). Name which indicators newly flagged or un-flagged vs the prior report date, linking the prior report file.
   - 1-2 sentences naming the most-stretched indicators with absolute levels (e.g., "CAPE 41.6, S&P 500 DY 1.06%, Moody's BAA−10Y 1.54pp at or past pre-bear levels"), not percentile ranks.
   - 1-2 sentences on what's contra (yield curve positive, SKEW already bid, etc.)
   - 1 line on action (3-5 verbs)
   - 1 line on empirical base rate at this flag-count range (median fwd SPY, drawdown probability) — **must end with a markdown link to the backtest artifact that literally contains those numbers** (e.g. `[flag-count backtest](../../oneoff/backtest_flag_vs_composite_<DATE>.csv)` or the backtest report file). An unlinked base-rate number violates the numerical-accuracy rule; Step 6 greps it.
   - **One final line — the named invalidation / non-linear-widening trigger** (re-added in v11; see § "Learning from sell-side institutional research"). Mirror UBS Global Strategy's convention of naming a *specific, sourced threshold* that would flip the regime, e.g. `*Trigger to watch:* HY OAS re-rates if BB−B dispersion breaks its 90th pct or 10s2s re-inverts.` One sentence only — not a return of the multi-paragraph "what would invalidate" block. State the level, the indicator, and where to verify it.
   - **No prose outside this block until after Figure 2.**
   - **Both the composite score and the flag-count chart are forbidden.** The composite is hand-weighted noise (backtest verified: max lift 0.68× at 90d / 0.98× at 180d). The flag-count chart was the proposed replacement (Figure 1 in v8) but the user rejected it in v9 as "inaccurate" — Plotly annotation positions drifted from the data, the "Now" arrow pointed off the actual data point, and the reference-line labels collided at the bottom of the chart. **Neither chart appears in the report.** Script state (verified 2026-06-10): `_make_flag_count_html` is commented out, but `_make_composite_html` and the `*_composite.png` savefig are **still wired in** — their outputs must never be embedded, and the calls should be removed or gated behind `--debug` (see Guardrails).

2. **`## Figure 2. Bear Market Checklist — Historical Calibration`** — a SINGLE comparison table mirroring Citi BMC Figure 2. Columns: Mar-00, Oct-07, Feb-20, Dec-21, **Now**. Rows: indicators grouped by category (Valuations / Yield Curve / Sentiment / Corp Behaviour / Profitability / Credit / Vol).

   **The table MUST be raw HTML with inline-style cell backgrounds** — not markdown with emoji dots in front of values. Citi's BMC table is the visual model: full-cell fill for each flag, not "🔴 33" floating next to the value. The viewer's marked.js passes raw HTML through, so a `<table>` with CSS classes works. Required class palette (defined in a `<style>` block at the top of the table):
   - `.bmc-red` — `background: #f4a8a8; color: #5a0000` (full flag — stretched / complacent)
   - `.bmc-amber` — `background: #ffd17a; color: #5a3300` (half flag — caution)
   - `.bmc-green` — `background: #b6e3b6; color: #1a4d1a` (contra-signal — e.g., SKEW high, CCC spread wide, VIX backwardation — divergence side of the regime)
   - `.bmc-stress` — `background: #c44; color: #fff` (vol-spike stress; e.g., VIX 40 during COVID)
   - `.bmc-na` — `color: #999` (n/a — data not available)
   - `.now` — `border-left: 2px solid #888` (column separator on the Now column)

   Cells without a flag get no class (plain white). Markdown emoji dots (🔴 🟠 🟢) are FORBIDDEN in Figure 2 — including in the legend line — they don't fill the cell, they crowd the value, and they render inconsistently across viewers.

   **The line under the table heading must state the flag rule in words, without emoji:** "Red (full flag) = indicator's complacency percentile ≥ 80 vs its own 10y history; amber (half flag) = ≥ 60; green = contra-signal; blank = off. Flag count = reds + 0.5 × ambers." This defines the colors in-report exactly as Citi does (their Figure 2 states the amber/red threshold mechanism explicitly).

   **Every indicator row must have a markdown link to the public source** for that indicator's historical chart: `[Indicator name](url)`. Reader should be able to click any row to verify the cited values against the canonical free chart (multpl, FRED, FINRA, Yahoo, Bain, Renaissance Capital, etc.).

   **Never use vague placeholders like "high" / "low" / "mid" when concrete numbers exist.** For each historical column, either (a) cite Citi BMC Figure 2's published number directly (Citi published the actual figures for valuation / M&A / IPO / RoE / capex / credit spreads — use them), (b) compute from the long-history source (Margin Debt from FINRA xlsx; HYG/LQD from yfinance for dates after HYG launched April 2007; BAA10Y from FRED back to 1986), or (c) explicitly cite the data limitation in italics next to the indicator name when no value is available (e.g., *"ICE BofA only 2023+"* or *"HYG launched April 2007"*).

   End with a "Today's calibration" paragraph: which historical references today matches, and what makes today distinctive (e.g., "no clean historical precedent — past bears started with one or the other, not both"). v11 adds two required clauses, drawn from the sell-side analog set (see § "Learning from sell-side institutional research"):
   - **State the 1–2 most-stretched indicators' OWN-history percentiles FIRST, then the absolute level** (UBS / JPM / Citi house phrasing: "US IG at the 2nd percentile, extremely tight (96bp)" — percentile before level).
   - **Pair the credit flag with one free fundamental anchor** so the reader can judge whether tight spreads are *earned* or *complacent* (JPM US High Grade method): cite FRED nonfinancial-corporate-debt/GDP, or BBB-share-of-IG / Moody's downgrade-upgrade direction. Tight + deteriorating leverage = genuinely complacent; tight + improving coverage = less alarming. Keep to the published-number standard (every figure string-matches its cited URL).
   - *Optional narrative cross-checks* (use when they sharpen the read, never as weighted flags): the NY Fed GSCPI macro-stress lead ("inflation peaks ~6mo after the supply-chain-pressure peak", Nomura) and the calm-price / rising-consumer-delinquency divergence (FRED `DRCCLACBS` / `DRALACBS`, GS Mortgage & Structured Products Trader).

3. **`## Under the Hood`** — sequence of 8-12 small charts with one-line captions only. NO narrative paragraphs between charts. Charts in order: long-history credit (BAA−10Y), IG credit tiers (AAA + BAA + dispersion), CAPE, ERP, VIX/VVIX, VIX term slope, MOVE, per-indicator bars. Each rendered by `scripts/build_dashboard.py` into `reports/charts/`.

   **Time-series charts must be embedded as interactive Plotly iframes** with rangeselector buttons (1Y / YTD / 5Y / 10Y / ALL) so the reader can adjust the timespan without leaving the page. Use `_make_interactive_chart()` in the build script — it produces a `<chart-slug>.html` file with rangeselector + range-slider + bear-market shading + threshold lines. Markdown embed pattern:
   ```html
   <iframe src="../charts/market_complacency_<DATE>_<slug>.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>
   ```
   The per-indicator bar chart (Figure 10) stays as a static PNG since it has no time axis.

   **Every chart must have a source-link caption immediately below it** in italics, listing the canonical public data source(s) as markdown links + a "[Static PNG](url)" fallback link for non-HTML renderers. Example: `*Figure N. <title>. Sources: [FRED BAA10Y](https://fred.stlouisfed.org/series/BAA10Y) · [TradingEconomics HY OAS](...). [Static PNG](../charts/<slug>.png).*`. When a chart uses a series with a data limitation (e.g., ICE BofA OAS only from 2023+), the caption must note the limitation and point to the long-history proxy used.

   **Mandatory chart styling — bear-market shading** (Citi BMC Figure 3+ style). Every time-series chart must have light-grey vertical bars (`axvspan(alpha=0.20, color="#888888")`) over the major US bear-market windows so the reader has visual context for "what was happening in those periods." The build script defines `BEAR_PERIODS` and `_shade_bears(ax)` helper that applies five reference windows: 1990-07/10 (Iraq/recession), 2000-03/2002-10 (dot-com), 2007-10/2009-03 (GFC), 2020-02/2020-03 (COVID), 2022-01/2022-10 (Fed pivot). Charts that are NOT time-series (per-indicator bars, precedents scatter, etc.) skip the shading.

   **Mandatory chart styling — in-image source footer on every PNG** (CLAUDE.md chart rule #1). Every matplotlib PNG — the static fallbacks, the per-indicator bar chart, and ALL backtest charts from `scripts/backtest_dashboard.py` — must render its data source inside the figure, e.g. `fig.text(0.99, 0.01, "Source: FRED BAMLH0A0HYM2 · yfinance ^VIX · multpl Shiller PE", ha="right", fontsize=7, color="#888")`. This is the same required-`sources`-parameter contract `_make_interactive_chart()` already enforces for the Plotly HTML charts — a markdown caption outside the image is a backup, not a substitute, because PNGs get viewed in isolation. **PNG titles must state the actual plotted data span, derived from the series' min/max dates — never hardcoded** (past bug: cape.png titled "2001–2026" over an 1871+ x-axis). Step 6 verifies both on ≥2 generated PNGs.

### Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — how a market-structure indicator is actually constructed and what it implies (how the MOVE index is built from a yield-curve-weighted basket of Treasury-option implied vols, what CCC OAS measures and why the weakest credit tier widens first, how the CBOE SKEW index prices the cost of OTM-put crash protection, why a VIX term-structure in contango signals no near-term hedging demand) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where (this skill's Citi-style layout):** ONE compact `**Further viewing**` bullet list (1–3 links), placed immediately BEFORE the Data Used section. Never inside the Dashboard's Take, never between Under-the-Hood charts (the no-prose-between-charts rule wins), never after Data Used.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

4. **`## Data Used / 数据来源清单`** — single source table grouping every indicator by category with its source URL. NO per-indicator paragraphs.

The user has explicitly rejected (v9 user feedback) the following blocks as not useful:
- ❌ Action Implications (the 5-row posture table) — the reader can derive postures from the flag count + Citi anchor; restating them in prose adds noise
- ❌ Historical Precedents (the date-by-date forward-return table) — small sample, noisy, no clean takeaway
- ❌ Backtest validation — precision numbers (~22% at T=10) are too low to motivate action; the report shouldn't read like a justification
- ❌ Caveats list — the bear-market shading on charts + the data-limitation italics in Figure 2 carry the necessary disclaimers; a separate prose section is redundant

Do NOT add these sections back unless the user explicitly asks. The report must end at Data Used, optionally preceded by the single Further-viewing block (see above — that is its only legal slot).

### What NOT to include in Citi-style mode

The following blocks from prior iterations are explicitly *forbidden* in the new format unless the user asks for them:

- ❌ Long "Composite Score Decomposition" tables — implicit in Figure 2 calibration. If the reader wants the weighted math, they can run the script.
- ❌ Long "Cross-Asset Signature" narrative paragraphs — collapsed into the Dashboard's Take + Figure 2.
- ❌ "What This Verdict Is NOT" multi-paragraph block — collapsed into the Caveats list.
- ❌ "What Would Invalidate This Read" multi-paragraph block — collapsed into Caveats. **Exception (v11):** the single named invalidation / non-linear-widening trigger line at the *end of the Dashboard's Take box* IS permitted and required — that one sentence is the UBS-style forward trigger, not the old multi-paragraph block. The ban is on the prose section, not on the one-line threshold.
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

### Data Used / 数据来源清单 (mandatory — single source table, no per-indicator paragraphs)

```markdown
## Data Used / 数据来源清单

Flag count and indicator percentiles computed in [`.claude/skills/market-complacency/scripts/build_dashboard.py`](../../.claude/skills/market-complacency/scripts/build_dashboard.py). Sources:

| Category | Indicator | Source |
|---|---|---|
| Credit | HY / IG / CCC OAS, BAA10Y | FRED via API: [BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2), [BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), [BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC), [BAA10Y](https://fred.stlouisfed.org/series/BAA10Y) |
| Yield Curve | 10Y − 2Y | FRED [T10Y2Y](https://fred.stlouisfed.org/series/T10Y2Y) |
| Valuation | CAPE, DY, Trailing PE | multpl monthly tables (Shiller PE / DY / PE) |
| Risk Premium | ERP, HYG/LQD | derived: multpl trailing-PE E/P − `^TNX` (NEVER `yf.Ticker("SPY").info["trailingEps"]` — unreliable, see § Derived indicators) + Yahoo Finance closes |
| Corp Behaviour | Capex YoY, IPO, M&A | FRED [PNFI](https://fred.stlouisfed.org/series/PNFI), Renaissance Capital / Bain → cached `.claude/skills/market-complacency/data/*.csv` |
| Sentiment | Margin debt | FINRA margin-statistics.xlsx |
| Equity / Rate Vol | VIX, VVIX, VIX9D, VIX3M, SKEW, MOVE | Yahoo Finance |
| Backtest | Flag-count base rates | [flag-count backtest](../../oneoff/backtest_flag_vs_composite_<DATE>.csv) |
| Cross-reference | Citi BMC | zsxq direct-download link to the current edition (see § Comparison to Citi's BMC) |

<one-line stale notices / fetch failures, e.g. "AAII 403, NAAIM 404 — positioning rows degraded to n/a">
```

Adapt rows to the run's active indicator set; every row keeps a clickable deep URL. No composite-methodology or precedents-methodology bullets — those are internal artifacts (see § Core methodology).

## Guardrails

- **Stale data is forbidden — `eps_peak` indicator removed in v10.** Per the user's hard rule ("if the data is stale, you shouldn't use it"): [multpl.com/s-p-500-earnings](https://www.multpl.com/s-p-500-earnings) lags GAAP finalization by 6-12 months. As of June 2026 their latest data point is Sep 30, 2025 = $239.98 — 8 months stale. **The `eps_peak` indicator that depended on this page has been removed** from the INDICATORS catalog and from Figure 2. The CAPE indicator (which uses multpl's Shiller PE page, also updated within 2 days) already captures the cycle-peak signal. **Other multpl pages used by the dashboard are CURRENT** (within 2 days as of June 2026): Trailing PE, Dividend Yield, Shiller PE all just need current price ÷ trailing-finalized-earnings so they refresh daily. Only the raw Earnings page waits for the GAAP-finalized number. **Every report run must** spot-check each multpl page's latest date before using it. If any used multpl page is more than 60 days stale, that indicator must be removed from the active set (with re-normalization and a comment in INDICATORS) and the report must note the removal. Re-add an EPS-based indicator only when a free monthly current TTM EPS feed is identified.

- **The build script must not emit artifacts for banned charts.** As of 2026-06-10 `build_dashboard.py` still calls `_make_composite_html` and saves `*_composite.png` even though the composite is forbidden in the report — on the next script touch, remove those calls (or gate behind a `--debug` flag) and replace the composite reference line/legend in the per-indicator bar chart with the amber=60 / red=80 flag-threshold lines (the reported metric). When a chart is removed from the report format, delete its generated HTML+PNG from `reports/charts/` in the same commit — no orphan artifacts (the rejected `flag_count.html` lingered as working-tree debris).
- **Never call the Claude API or any LLM API.** Per [`CLAUDE.md`](../../../CLAUDE.md): the agent (Claude in this conversation) does the analysis directly; no `anthropic.Anthropic()`, no `openai`, no LLM client. The script is pure pandas + yfinance + urllib for the FRED / Shiller / AAII / NAAIM CSV fetches.
- **Never write to any `db/*.db` file.** Read-only against `db/indicators.db`. New indicators added by this skill live in `oneoff/` CSV cache files, not the project database. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".
- **Never silently drop a required indicator from the composite.** If HY OAS, IG OAS, CCC OAS, VIX, VVIX, VIX term slope, SKEW, MOVE, ERP, or HYG/LQD fails to fetch, the script must error out and the report must not be written. (Optional indicators — AAII, NAAIM, CAPE — are the only ones the report may degrade gracefully on.)
- **Never report a flag count without disclosing the active denominator.** If indicators failed to fetch, the denominator (`flag_max`) shrinks — the Take's first line and the Data Used block must both carry the actual `N` and note the failures.
- **Never claim the dashboard predicts the *timing* of a regime turn.** It is a state read. Complacency can persist for quarters — the dashboard flagged heavily through most of 2017 before the Feb 2018 vol shock. The Dashboard's Take must never phrase the flag count as a timing call (the old "What this verdict is NOT" prose block was removed in the Citi-style rewrite; the discipline lives in the Take's wording).
- **Never extrapolate a single indicator into a regime call.** A low HY OAS alone is not "complacency" — it is *one* signal among twelve. The cross-asset signature paragraph is the report's load-bearing analysis; the headline verdict without it is misleading.
- **Never use absolute thresholds without percentile context.** "VIX is 12" means nothing without "which is the 7th percentile of the last 10 years". The indicator table must show both. Absolute levels rot as the regime evolves; percentiles are self-calibrating.
- **Never include indicators with <5y clean history in the composite.** Short-history indicators can be discussed narratively but cannot be weighted. CCC OAS itself was reconstructed by ICE in different eras; verify the FRED series goes back the full 10y before weighting it.
- **Never assert "this looks like 2007 / 2018 / 2020".** Let the precedents table do that work — list the dates with their forward returns and let the reader pattern-match. Naming specific historical analogs in the verdict is over-confident.
- **No "Source: our model" / "(estimate)" / "(本模型)"** anywhere. The composite is computed in `.claude/skills/market-complacency/scripts/build_dashboard.py`; cite the script path for the composite, cite the underlying FRED / yfinance / multpl / AAII / NAAIM URLs for the inputs.
- **ICE BofA OAS series window — real upstream restriction.** When the build script has access to a FRED API key (via `config.FRED_API_KEY`), it uses the JSON API for reliable pulls. Investigation in v3 confirmed the limited-history issue is NOT a CSV truncation — it's the actual series. The series metadata for `BAMLH0A0HYM2` / `BAMLC0A0CM` / `BAMLH0A3HYC` declares `observation_start: 2023-06-06` because ICE BofA re-licensed the indices in mid-2023 and FRED's pre-2023 archive was retired. Even the API key cannot recover pre-2023 history for these series. **The dashboard's mitigation is the v3 addition of Moody's BAA−10Y** (FRED `BAA10Y`, 1986-2026, ~10,000 daily obs) which is the canonical long-history IG-credit spread and gives the composite genuine cycle-aware credit context for pre-2023 dates. Every report must disclose this constraint in the Data Used section. The non-FRED indicators (VIX/VVIX/SKEW/MOVE/HYG/LQD/CAPE/ERP) are not affected.

## Output location

Save to `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` under the project root (create the `reports/market-complacency/` folder if missing — first report establishes the directory). The viewer at `http://xs-macbook-air.local:5001/reports` will surface it under a new "MARKET-COMPLACENCY" type (or as "OTHER" until the viewer's bucket map is updated).

Supplementary deliverables sit in standard locations:

- Charts: `reports/charts/market_complacency_<DATE>_*.png`.
- Composite build script: `.claude/skills/market-complacency/scripts/build_dashboard.py` (reusable across dates via `--date YYYY-MM-DD`). Generated CSVs: `oneoff/market_complacency_<DATE>_indicators.csv`, `oneoff/market_complacency_<DATE>_precedents.csv`, `oneoff/market_complacency_<DATE>_composite_history.csv`. The script is self-contained and idempotent.
- Date-stamped CSV caches written by the build script: `oneoff/sp500_trailing_pe_<DATE>.csv`, `oneoff/shiller_cape_<DATE>.csv`, `oneoff/aaii_sentiment_<DATE>.csv`, `oneoff/naaim_exposure_<DATE>.csv`. Reruns on the same date are free; reruns on a different date re-fetch from source.

### Update-in-place rule

One report per date. If `reports/market-complacency/market_complacency_<YYYY-MM-DD>.md` already exists for today's date, update it in place rather than creating a parallel copy. Across dates, keep separate files — the historical sequence of verdicts is itself useful context.

## Comparison to Citi's Bear Market Checklist (BMC)

Every report must include a cross-reference to Citi's BMC when a current edition is available (Citi publishes refreshes ~quarterly). The BMC is the institutional analog of this dashboard with 18 indicators across valuation / yield curve / sentiment / corporate behaviour / profitability / balance sheets-and-credit. The skill's `scripts/build_dashboard.py` outputs a Citi-BMC-style **flag count** (amber if complacency_pct ≥ 60, red if ≥ 80; total = 0.5 × n_amber + 1.0 × n_red) alongside the continuous composite, so cross-comparison is direct.

**Citation rule (mandatory, each run):** resolve the current BMC edition from the user's local zsxq library —

```bash
/opt/anaconda3/bin/python3 zsxq_fts.py --query "Bear Market Checklist" --limit 5
```

— and cite it with the **direct-download route** printed as `pdf_url`: `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>` (e.g. the 2026-06-05 edition is file_id `181245528155282`). NEVER `/zsxq/pdf-viewer/<id>` and NEVER the paywalled `citivelocity.com` homepage — a homepage link is a non-citation. If the edition is absent from zsxq, write a labeled, link-free reference: `Citi BMC (paywalled, edition YYYY-MM-DD)`.

Citi historical reference flags (cite when relevant):

| Date | Citi BMC flags / 18 | Note |
|---|---:|---|
| Mar 2000 | 17.5 | Dot-com peak |
| Oct 2007 | 13 | Pre-GFC peak |
| Feb 2020 | 5.5 | Pre-COVID peak (interesting that this was low) |
| Dec 2021 | 8.5 | Post-COVID peak |
| Jun 2026 | 10 (Global), 11.5 (US), 5 (Europe) | "Frothiest since GFC, not yet overexuberant" |

Citi's explicit guidance: "once the count reaches double digits, it has historically tended to rise more rapidly." That heuristic should be quoted in any report whose flag count is approaching 10. This dashboard's proportional equivalent to Citi's 18-flag denominator is `flag_count × 18 / flag_max` — compute it from the run's indicators CSV, never hardcode it (the denominator changes as indicators are added or fail to fetch).

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
| IPO Activity (% of Mkt cap) | `ipo_pct`: annual US IPO proceeds / SPX level | [Renaissance Capital IPO Stats page](https://www.renaissancecapital.com/IPO-Center/Stats) → manually cached `.claude/skills/market-complacency/data/ipo_proceeds_annual.csv` |
| M&A Activity (% of Mkt cap) | `ma_pct`: annual US M&A volume / SPX level | [Bain 2025 M&A report](https://www.bain.com/about/media-center/press-releases/20252/global-ma-stages-great-rebound-in-2025-with-$4.8-trillion-deal-value-to-mark-second-highest-total-on-record) + [S&P Global Q1 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/global-m-and-a-by-the-numbers-q1-2026) → manually cached `.claude/skills/market-complacency/data/ma_volume_annual.csv` |

**Refresh workflow for v6 indicators**: each report run, the agent uses WebSearch to find:
- "Renaissance Capital 2026 YTD IPO count proceeds" — update last row of `.claude/skills/market-complacency/data/ipo_proceeds_annual.csv`
- "Bain global M&A 2026 Q1 announced volume" — update last row of `.claude/skills/market-complacency/data/ma_volume_annual.csv`

The annual data is forward-filled to monthly in the build script (`scripts/build_dashboard.py` `fetch_ipo_pct` / `fetch_ma_pct`). The percentile rank is computed against the trailing 10y monthly window so the indicator behaves like every other one in the composite. **Note that today's readings (IPO 7th decile, M&A 8th decile) are NOT complacent** — deal-making activity in 2026 is well below 2021 peaks despite valuation extremes.

**Promoted to active candidates in v11 (free feeds confirmed reachable — see § "Learning from sell-side institutional research"):**

| Citi BMC factor | This dashboard equivalent | Data source |
|---|---|---|
| Speculative positioning | CFTC asset-manager net S&P 500 e-mini futures, percentile-ranked vs 10y (UBS "95th pct" gauge) | [CFTC Commitments-of-Traders weekly](https://www.cftc.gov/dea/newcot/FinFutWk.txt) |
| (Levkovich component) Margin debt | Promote the already-cached FINRA margin-debt ÷ S&P 500 from Figure-2-only into the active positioning flag (MS / GS-EM "margin balances at record") | [FINRA margin-statistics.xlsx](https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx) |
| Index concentration / breadth | Top-10 S&P 500 weight and/or % above 200dma (Bernstein Asia Quant; narrow breadth under new highs) | yfinance constituents — computable free |
| Equity Fund Flows | 4-week equity-fund flow trend, percentile-ranked (GS Weekly Fund Flows / JPM EM Money Trail) | ICI weekly equity-fund flows, or HYG/LQD/SPY AUM-flow proxy (yfinance) |

**Still in the backlog (need paid feeds or non-trivial engineering):**

| Citi BMC factor | Tried | Status |
|---|---|---|
| Forward PE | multpl 404; gurufocus 403; Yardeni PDF binary extraction failed; macromicro current value via WebSearch | WebSearch returns a current snapshot (22-26 range across sources) but no clean free historical CSV. v7 candidate: hardcode current value with confidence interval, compute proxy historical via SPX/multpl-trailing-EPS × consensus-EPS-growth-forecast |
| Aggregate RoE | yfinance per-constituent rollup; SPDR S&P 500 fundamentals page | 500-ticker rollup expensive; need a cached pipeline. Backlog. |
| Analyst Bullishness | Refinitiv I/B/E/S | Paywall |
| Levkovich Index | Citi proprietary | Components partly approximated by margin debt + put/call; full reconstruction needs ETF flows + analyst data |
| Asset/Equity (Financials) | XLF holdings, FactSet | XLF rollup computable but per-constituent balance-sheet data needed |
| Net Debt/EBITDA (ex-Fins) | FactSet | Paywall |

When data sources are added in future versions, run the standard backtest discipline (see below) to validate they improve the predictive metric on top of v4.

## Backtest discipline

**The ONE canonical validation metric is flag-count lift** on the 90d/−10% and 180d/−15% SPY drawdown events, computed by `oneoff/backtest_flag_vs_composite.py` — the numbers the Output Format section relies on (1.32×/1.90× at T=10/11 on 90d; 1.78×/2.41× on 180d; see § "Why flag count beats composite"). Re-run it against the run's flag-count history:

```bash
/opt/anaconda3/bin/python3 oneoff/backtest_flag_vs_composite.py
```

**Any indicator add / remove / threshold change must be validated by re-running this flag-vs-composite backtest BEFORE shipping, quoting before/after flag-count lift at T=10/11.** Unvalidated candidates stay narrative-only (see § Indicators rows 14–16).

**Superseded historical analysis — do not cite as governing:** the composite-tier threshold sweep in `scripts/backtest_dashboard.py` and the conclusions of [`reports/market-complacency/backtest_2026-06-07.md`](../../../reports/market-complacency/backtest_2026-06-07.md) (e.g. "Stretched tier lift 1.10", "keep v2 as the default") predate the v8/v9 flag-count pivot. The flag-vs-composite comparison showed the composite is worse than random at every threshold (max 0.68× at 90d), so composite-tier lift is no longer the bar for anything. Two lessons from that backtest remain valid and carry over:

- **The dashboard hit 4 of 7 major SPY drawdowns at the peak; 8 of 11 on QQQ.** The structural misses (GFC, 2022 bear, COVID) were exogenous-shock events the dashboard cannot see by construction.
- **The dashboard is a *regime descriptor*, not a *drawdown predictor*.** Report writeups must calibrate expectations accordingly — quote the empirical drawdown probabilities at today's flag-count range from the flag-count backtest, not anecdotal "this looks like 2007" comparisons.

## What this skill does NOT do

- It does not pick a ticker — that's [[trader-plan]] / [[idea-generation]].
- It does not size a hedge — the "Action implications" block names the *kind* of hedge (put spread vs VIX call vs cash raise) but not the *dollar amount*. Sizing depends on portfolio context outside this skill.
- It does not forecast regime turns — see Guardrails.
- It does not analyze a specific sector's stress — [[sector-overview]] with a stress lens does that.
- It does not write the new indicators (CCC OAS, SKEW, MOVE, CAPE, AAII, NAAIM) into the live `indicators` dashboard at `http://xs-macbook-air.local:5001`. That promotion is a separate engineering task; this skill keeps the additions scoped to the report run.

## Related skills

- [[market-status]] — the sibling GS-Kickstart-style *equity exuberance* dashboard (momentum, IPOs, speculative trading, issuance). This skill owns cross-asset risk-under-pricing (credit / vol / risk premia); route froth-through-the-equity-lens questions there.
- [[take-profit-lab]] — single-ticker exit discipline. The macro complacency read is one input to the per-ticker exit decision.
- [[sector-overview]] — sub-sector stress; complements the macro dashboard.
- [[idea-generation]] — turns a "complacency is high" read into specific short / hedge candidates.
- [[portfolio-decision]] — final position rating; the complacency verdict is one of its macro inputs.
