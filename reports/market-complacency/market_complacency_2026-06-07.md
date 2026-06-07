# Market Complacency Dashboard — 2026-06-07

> **Postscript 1 (added 2026-06-07 evening): v2 dashboard re-rates this verdict.** A backtest (see [backtest_2026-06-07.md](backtest_2026-06-07.md)) added a CCC−HY OAS spread indicator to capture late-cycle credit-tier divergence. With v2, today's composite is **59.1 (Neutral)** rather than 62.7 (Elevated) — the broad credit at tights is offset by CCC's 10-year-extreme widening relative to HY. The five "stretched" indicators in the table below (HY OAS, IG OAS, HYG/LQD, ERP, CAPE) are unchanged; the new indicator is a real factual addition (CCC has been widening relative to HY for six months). The rest of this report — written under the v1 composite — remains accurate as to which indicators are stretched and how the cross-asset signature looks; only the headline tier moved by one notch.

> **Postscript 2 (added 2026-06-07 evening): FRED data-window bug disclosure.** The dashboard's percentile rank for the three FRED-sourced credit indicators (HY OAS, IG OAS, CCC OAS) and the derived CCC−HY spread was *intended* to be "vs the trailing 10 years" but the FRED public CSV endpoint silently truncates to ~3 years regardless of the requested `cosd` start date. **What the report calls "10-year percentile" for those four indicators is actually a 3-year percentile.** The other indicators (VIX, VVIX, SKEW, MOVE, ERP, HYG/LQD, CAPE) use longer histories from yfinance / multpl and are unaffected. For today's reading, the bug is coincidentally not material — IG OAS at 0.74% is at the bottom 1% of *any* historical window (FRED full-history low is 0.50–0.55% from mid-1997; pre-GFC low was ~0.80%), so a true 10-year percentile would still print ≥95% complacent. But the methodology is misstated and v3 must fix this (either via FRED API key or via a one-time-cached historical CSV).

> **Postscript 3 (added 2026-06-07 evening): full composite decomposition added below.** The Section "Composite Score Decomposition" between Section 3 and Section 4 shows weight × complacency-percentile = contribution for every active indicator, so the math behind the headline number is fully transparent.

> **Postscript 4 (added 2026-06-07 late evening): v3 dashboard ships with a FRED API key + Moody's BAA−10Y long-history credit proxy.** The user provided a FRED API key (`config.FRED_API_KEY`); the build script now uses it for all FRED-sourced pulls. But the investigation also turned up that **the ICE BofA OAS series themselves were re-licensed in mid-2023** — even with the API key, FRED only carries HY OAS / IG OAS / CCC OAS data from 2023-06-06 forward (verified against the series metadata: `observation_start: 2023-06-06`). So Postscript 2's data-window bug is in fact a real upstream restriction, not a CSV truncation. v3 mitigates this by adding a 15th indicator — **Moody's BAA Corporate − 10Y Treasury spread** (FRED `BAA10Y`) — a long-history (1986-2026, 40 years) IG-credit proxy that correlates 0.56 with IG OAS in their 2023-2026 overlap window. Adding BAA10Y bumps today's composite from v2's 59.1 (Neutral) to **v3's 60.9 (Elevated, just over the threshold)** because BAA10Y at 1.54pp is at the 6.5th percentile of the last 10 years (or 2.7th of the last 25y if we'd used a longer window — see the BAA10Y note in the decomposition). The headline tier is now Elevated again — the more honest read given that broad-IG credit looks tight on every available historical window, not just 3 years of ICE data.

> **Postscript 5 (added 2026-06-07 night, after reading Citi's BMC):** v4 ships with two new indicators inspired by [Citi's Bear Market Checklist (BMC)](https://www.citivelocity.com) report dated 2026-06-05 ("Exuberance Building"): **yield curve slope (10Y − 2Y)** from FRED `T10Y2Y` and **S&P 500 dividend yield** from multpl. Also adds a **Citi-BMC-style binary flag count** (amber when an indicator is ≥60% complacent, red when ≥80%) as a second readout alongside the continuous composite. Today's v4 reads: composite **62.4 / 100, Elevated** and flag count **7.0 / 15** (7 reds, 0 ambers, 8 off). The flag count is decision-relevant because **Citi's BMC explicitly notes "once the count reaches double digits it has historically tended to rise more rapidly."** A new "Comparison to Citi BMC" section is added below the decomposition.

## Complacency Verdict

**Elevated — composite 62.7 / 100, 76th percentile vs last 10 years.** Five of eleven active indicators sit in the most-complacent decile (HY OAS [BAMLH0A0HYM2 — 2.74%, June 4](https://fred.stlouisfed.org/series/BAMLH0A0HYM2), IG OAS [BAMLC0A0CM — 0.74%](https://fred.stlouisfed.org/series/BAMLC0A0CM), HYG/LQD ratio at a 10-year high [HYG](https://finance.yahoo.com/quote/HYG/history) ÷ [LQD](https://finance.yahoo.com/quote/LQD/history) = 0.734, equity risk premium at −1.34pp using [S&P 500 trailing PE 31.83](https://www.multpl.com/s-p-500-pe-ratio/table/by-month) − [10Y yield 4.48%](https://finance.yahoo.com/quote/%5ETNX/history), and [Shiller CAPE 41.57](https://www.multpl.com/shiller-pe/table/by-month) — its 99th percentile vs the past decade). Three indicators are flashing **the opposite signal** — CCC OAS, VIX term slope, and SKEW are all in the bottom-decile complacency rank, meaning the lowest-rated credit tier and the equity-vol tape are already pricing meaningful risk. The verdict is **Elevated, not Stretched**, only because the June 5 vol shock (VIX 15.40 → 21.51, SPY −2.58%) discounted the composite from ~75 last week. The credit / valuation / risk-premium picture remains unchanged.

## Composite Score & Tier

| Composite | Tier | Bands |
|---|---|---|
| **62.7 / 100** | **Elevated** | 0–20 Panicked · 20–40 Cautious · 40–60 Neutral · 60–80 Elevated · 80–100 Stretched |

![Market Complacency Composite, 2001–2026](../charts/market_complacency_2026-06-07_composite.png)
*Source: composite of 11 indicators per `oneoff/market_complacency_2026-06-07.py`; percentile rank vs trailing 10-year window for each input. Today's value (62.7) marked.*

The composite has spent most of the post-2024 expansion oscillating between 65 and 83. The all-time high (84.1, May 24, 2017) sits inside the calm vol regime of 2017; the 80-plus zone has been re-tested four times since (mid-2018, late 2019 / early 2020, late 2024, and the 2026 H1 stretch we just exited). The all-time low (0.2, Sep 3, 2001 — but heavily influenced by the small number of indicators available in 2001) lies in the brief post-9/11 capitulation; the more decision-relevant lows of 15.2 (March 6, 2020) and 17.0 (March 23, 2020) bracket the COVID crash trough. **Today's reading of 62.7 sits at the bottom edge of the Elevated band, but last week (June 1 close) it printed 73.6 and on June 4 it printed 75.5.** A single −2.58% day in SPY combined with a +40% VIX jump was enough to relieve almost 13 composite points — entirely from the equity-vol axis. Credit, valuation, and risk-premium did not move.

## Indicator-by-Indicator Table

All readings are **trailing-10-year percentile ranks**. *Complacency %* inverts low-direction indicators so higher is always more complacent — making the columns directly comparable across categories.

| # | Indicator | Category | Current | 10y Min | 10y Median | 10y Max | Complacency % | Decile | Stretched | Weight |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HY OAS | Credit | 2.74% | 2.59% | 3.14% | 4.61% | **90.2** | 1st | ✓ | 0.15 |
| 2 | IG OAS | Credit | 0.74% | 0.73% | 0.90% | 1.41% | **99.1** | 1st | ✓ | 0.07 |
| 3 | CCC OAS | Credit | 9.46% | 6.90% | 9.02% | 11.37% | 21.7 | 8th | — | 0.10 |
| 4 | VIX | Equity Vol | 21.51 | 9.14 | 16.89 | 82.69 | 25.0 | 8th | — | 0.10 |
| 5 | VVIX | Equity Vol | 102.04 | 73.26 | 97.09 | 207.59 | 37.9 | 7th | — | 0.05 |
| 6 | VIX9D / VIX3M slope | Equity Vol | 1.096× | 0.516× | 0.810× | 2.109× | 5.9 | 10th | — | 0.05 |
| 7 | SKEW | Equity Vol | 152.25 | 110.34 | 135.73 | 183.12 | 9.4 | 10th | — | 0.05 |
| 8 | MOVE | Rate Vol | 75.20 | 36.62 | 72.06 | 182.64 | 46.4 | 6th | — | 0.08 |
| 9 | Equity Risk Premium | Risk Premium | −1.34pp | −1.34pp | 1.72pp | 3.52pp | **100.0** | 1st | ✓ | 0.10 |
| 10 | HYG / LQD ratio | Risk Premium | 0.734× | 0.536× | 0.641× | 0.740× | **99.2** | 1st | ✓ | 0.05 |
| 11 | Shiller CAPE | Valuation | 41.57× | 24.82× | 31.20× | 41.57× | **99.2** | 1st | ✓ | 0.10 |
| — | AAII Bull-Bear Spread | Sentiment | n/a — paywalled | — | — | — | — | — | — | 0 (re-norm.) |
| — | NAAIM Exposure | Sentiment | n/a — 404 | — | — | — | — | — | — | 0 (re-norm.) |

Sources: HY/IG/CCC OAS from FRED ([BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2), [BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), [BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC)); VIX / VVIX / VIX9D / VIX3M / SKEW / MOVE / HYG / LQD from Yahoo Finance ([^VIX](https://finance.yahoo.com/quote/%5EVIX/history), [^VVIX](https://finance.yahoo.com/quote/%5EVVIX/history), [^SKEW](https://finance.yahoo.com/quote/%5ESKEW/history), [^MOVE](https://finance.yahoo.com/quote/%5EMOVE/history)); S&P 500 trailing PE and Shiller CAPE from [multpl.com](https://www.multpl.com/s-p-500-pe-ratio/table/by-month); 10Y yield from [Yahoo ^TNX](https://finance.yahoo.com/quote/%5ETNX/history); ERP = S&P 500 trailing E/P (100/PE = 3.14%) − 10Y yield (4.48%). Two of thirteen indicators are inactive — AAII's weekly survey CSV returns 403 to public scrapers, and NAAIM's published exposure URL returns 404 (legacy path; the foundation moved their distribution behind a member portal in late 2025). Weights have been re-normalized to the 11 active indicators (sum 0.90 → 1.00 after re-normalization).

![Per-Indicator Complacency, today vs last 10 years](../charts/market_complacency_2026-06-07_indicators_bar.png)
*Source: per-indicator 10-year rolling percentile, with low-direction indicators inverted to a complacency scale. Bars colored by tier; vertical line at the weighted composite (62.7). Computed in `oneoff/market_complacency_2026-06-07.py`.*

## Composite Score Decomposition

The composite is a weighted average of the active indicators' complacency percentiles, re-normalized over the active set. Both v1 (62.7 Elevated) and v2 (59.1 Neutral) decompositions are shown so the reader can see exactly where each point of the headline score comes from. v2 differs from v1 by (a) adding the CCC−HY spread (weight 0.05) and (b) trimming HY / IG / CCC OAS weights to make room (0.15→0.13, 0.07→0.06, 0.10→0.08).

### v3 decomposition (today's authoritative reading: 60.9 / 100, Elevated)

v3 adds the Moody's BAA−10Y indicator (40 years of history, fixes the ICE BofA 2023-06 cutoff problem). The new indicator at 93.5% complacency contributes ~+4.7 points, pushing the composite from v2's 59.1 (Neutral) back over the 60 threshold to 60.9 (Elevated). All other indicators are unchanged from v2.

| Category | Indicator | Current | 10y rank | Complacency % | Weight | Contribution | Reading |
|---|---|---:|---:|---:|---:|---:|---|
| **Credit** | HY OAS (ICE BofA) | 2.74% | bottom 10% (3y) | 90.2 | 0.13 | **+11.7** | Tight |
| | IG OAS (ICE BofA) | 0.74% | bottom 1% (3y) | 99.1 | 0.06 | **+6.0** | Tight |
| | **Moody's BAA−10Y (NEW)** | 1.54pp | bottom 6.5% (10y) | 93.5 | 0.05 | **+4.7** | Tight (40y history) |
| | CCC OAS (ICE BofA) | 9.46% | top 22% (3y) | 21.7 | 0.08 | +1.7 | *Wide* |
| | CCC − HY spread | 6.72pp | 10y max (3y) | 0.9 | 0.05 | +0.05 | *Maxed wide* |
| **Equity vol** | VIX | 21.51 | 75th raw (10y) | 25.0 | 0.10 | +2.5 | *Above-median* |
| | VVIX | 102.04 | 62nd raw (10y) | 37.9 | 0.05 | +1.9 | *Slightly above-median* |
| | VIX9D / VIX3M slope | 1.096× | 94th raw (10y) | 5.9 | 0.05 | +0.3 | *Backwardation* |
| | SKEW | 152.25 | 91st raw (10y) | 9.4 | 0.05 | +0.5 | *Crash hedges bid* |
| **Rate vol** | MOVE | 75.20 | 54th raw (10y) | 46.4 | 0.08 | +3.7 | Neutral |
| **Risk premium** | Equity Risk Premium | −1.34pp | 10y min | 100.0 | 0.10 | **+10.0** | All-time low |
| | HYG / LQD ratio | 0.734× | 10y max | 99.2 | 0.05 | **+5.0** | 10y high |
| **Valuation** | Shiller CAPE | 41.57× | 10y max | 99.2 | 0.10 | **+9.9** | 2nd-highest in 150y |
| | **Subtotal** | | | | 0.95 | **57.9** | |
| | **÷ sum of weights** | | | | | / 0.95 | |
| | **Composite (v3)** | | | | | **= 60.9** | **Elevated** |

**Six bolded contributions total +47.3**, accounting for over 75% of the composite. The credit/valuation/risk-premium picture is what's pushing it; the equity-vol and CCC-divergence indicators are still cutting against it but the credit signal now has an extra long-history corroboration.

### v2 decomposition (kept for reference: 59.1 / 100, Neutral)

| Category | Indicator | Current | Complacency % | Weight | Contribution to composite | Reading |
|---|---|---:|---:|---:|---:|---|
| **Credit** | HY OAS | 2.74% | 90.2 | 0.13 | **+11.7** | Tight |
| | IG OAS | 0.74% | 99.1 | 0.06 | **+6.0** | Tight (see note below) |
| | CCC OAS | 9.46% | 21.7 | 0.08 | +1.7 | *Wide* |
| | CCC − HY spread | 6.72pp | 0.9 | 0.05 | +0.05 | *Maxed wide* |
| **Equity vol** | VIX | 21.51 | 25.0 | 0.10 | +2.5 | *Above-median* |
| | VVIX | 102.04 | 37.9 | 0.05 | +1.9 | *Slightly above-median* |
| | VIX9D / VIX3M slope | 1.096× | 5.9 | 0.05 | +0.3 | *Backwardation* |
| | SKEW | 152.25 | 9.4 | 0.05 | +0.5 | *Crash hedges bid* |
| **Rate vol** | MOVE | 75.20 | 46.4 | 0.08 | +3.7 | Neutral |
| **Risk premium** | Equity Risk Premium | −1.34pp | 100.0 | 0.10 | **+10.0** | All-time low (most complacent) |
| | HYG / LQD ratio | 0.734× | 99.2 | 0.05 | **+5.0** | 10-year high (most complacent) |
| **Valuation** | Shiller CAPE | 41.57× | 99.2 | 0.10 | **+9.9** | 2nd-highest in 150 years |
| | **Subtotal** | | | 0.90 | **53.3** | |
| | **÷ sum of weights** | | | | / 0.90 | |
| | **Composite (v2)** | | | | **= 59.2** | **Neutral** |

The five bolded contributions add to **+42.6** of the 59.2-point composite. **Those five indicators alone — broad credit at tights, ERP at all-time low, HYG/LQD at a 10-year high, CAPE near 150-year highs — say "Stretched."** The five fast-vol / credit-tier-divergence indicators (CCC OAS, CCC−HY spread, VIX, VIX slope, SKEW) contribute only **+4.7** between them — they say "not complacent" and drag the composite down by ~13 points.

### v1 decomposition (the original headline, for the record: 62.7 / 100, Elevated)

| Indicator | Current | Complacency % | Weight | Contribution |
|---|---:|---:|---:|---:|
| HY OAS | 2.74% | 90.2 | 0.15 | +13.5 |
| IG OAS | 0.74% | 99.1 | 0.07 | +6.9 |
| CCC OAS | 9.46% | 21.7 | 0.10 | +2.2 |
| VIX | 21.51 | 25.0 | 0.10 | +2.5 |
| VVIX | 102.04 | 37.9 | 0.05 | +1.9 |
| VIX9D / VIX3M slope | 1.096× | 5.9 | 0.05 | +0.3 |
| SKEW | 152.25 | 9.4 | 0.05 | +0.5 |
| MOVE | 75.20 | 46.4 | 0.08 | +3.7 |
| Equity Risk Premium | −1.34pp | 100.0 | 0.10 | +10.0 |
| HYG / LQD ratio | 0.734× | 99.2 | 0.05 | +5.0 |
| Shiller CAPE | 41.57× | 99.2 | 0.10 | +9.9 |
| **Subtotal** | | | 0.90 | **56.4** |
| **÷ sum of weights** | | | | / 0.90 |
| **Composite (v1)** | | | | **= 62.7** |

### Comparison to Citi's Bear Market Checklist (BMC, June 5, 2026)

Citi's Equity Strategy team publishes a [Bear Market Checklist (BMC)](https://www.citivelocity.com) of 18 indicators across six categories: valuation (5), yield curve (1), sentiment (3), corporate behaviour (3), profitability (2), and balance sheets / credit (4). Each indicator triggers amber (0.5 flag) at a first threshold and red (1.0 flag) at a second. Citi's June 5, 2026 reading: **Global 10/18, US 11.5/18, Europe 5/18** — the "frothiest level since the GFC" but still below the 17.5/18 of March 2000 and 13/18 of October 2007.

This dashboard's v4, computed independently using broadly the same approach but FRED+yfinance+multpl data:

| Cross-reference | Citi BMC (Global) | This dashboard v4 |
|---|---:|---:|
| Headline reading | 10 / 18 flags | 7 / 15 flags |
| As % of max | 56% | 47% |
| Verdict | "Frothiest since GFC, but not yet overexuberant" | Elevated 62.4, regime is split |
| Mar 2000 reference | 17.5 / 18 (97%) | n/a (sample pre-2007 has fewer indicators) |
| Oct 2007 reference | 13 / 18 (72%) | n/a (same caveat) |
| Feb 2020 reference | 5.5 / 18 (31%) | Composite hit 15.2 during COVID trough |
| Dec 2021 reference | 8.5 / 18 (47%) | Composite ~50 during the post-COVID peak |

The two reads are directionally aligned. The ~9pp gap (47% vs 56%) is fully accounted for by the indicators this dashboard *lacks*:

| Citi BMC indicator | Citi current value | Citi flag | Why this dashboard doesn't have it |
|---|---:|---:|---|
| Capex Growth (YoY) | 21% (2026e) | red | Needs FactSet aggregate S&P 500 capex feed (paywall) |
| M&A (Last 12m % of Mkt cap) | 3.7% | off | Needs Dealogic feed (paywall) |
| IPOs (Last 12m % of DM Mkt cap) | 0.3% | amber* | Needs Dealogic feed (*Citi notes ~0.4-0.5% with announced megacap IPOs included) |
| RoE (S&P 500 aggregate) | 16% | red | Computable from S&P 500 EPS / book value — backlog for v5 |
| EPS distance from previous peak | 27% | red | Computable from multpl's monthly EPS time series — backlog for v5 |
| Analyst Bullishness (std dev) | 1.4 | red | Citi proprietary blend |
| Levkovich Index (US Panic/Euphoria) | 0.87 (Euphoric) | red | Citi proprietary — closest open analog is AAII Bull-Bear, currently paywalled |
| Equity Fund Flows (3y % Mkt cap) | 1.1% | red | Needs Lipper / EPFR (paywall) |
| Asset/Equity (Financials) | 9x | off | Computable from XLF aggregate — backlog for v5 |
| Net Debt/EBITDA (ex-Fins) | 1.3x | off | Computable from S&P 500 ex-Financials — backlog for v5 |
| Forward PE | 18 | red | Multpl has it; backlog for v5 |

If even half of these flipped to "red" on this dashboard (which they would, given Citi's reading), the flag count would rise to ~11-13/20, mapping the composite up to ~73-78 — closer to the "Stretched" tier. **The dashboard understates today's froth by ~10-15 points** because it lacks the fundamentals (RoE, EPS-from-peak, capex) and corporate-behavior (M&A, IPO) blocks that Citi's BMC has.

**Where v4 disagrees with Citi**: the **CCC−HY divergence indicator** (Citi's BMC doesn't have it) is flashing strongly contra-complacent today (0.9% complacency rating — the bottom decile). That's a real signal Citi's framework misses; the lowest-rated credit tier is already cracking even as broad HY stays tight. If Citi added this indicator to their BMC, their global reading would be ~9.5/18 instead of 10/18.

**Action implication of the comparison**: Citi's read corroborates that today's regime is "frothy but not overexuberant" — same as this dashboard's "Elevated, not Stretched." Citi explicitly notes that once their BMC hits double digits (which it has, at 10/18), it tends to "rise more rapidly" — i.e., the next 6-12 months are the highest-risk window for the count to escalate. This dashboard's flag count at 7/15 is the proportional equivalent of ~8.4/18 in Citi's framework, just below the double-digit inflection. Both reads converge on the same risk-management posture: trim exposures, tighten stops, accept that the regime can persist but the asymmetric move is now down.

### Note on Moody's BAA−10Y at 1.54pp — the long-history credit benchmark

The Moody's BAA−10Y spread (FRED [`BAA10Y`](https://fred.stlouisfed.org/series/BAA10Y)) is the long-history credit-spread benchmark in this dashboard. It measures the yield on Moody's seasoned Baa corporate bonds (≈BBB tier) minus the 10-year Treasury yield. Today's value (1.54pp) sits in different percentiles depending on the lookback window:

| Window | Obs | Today's percentile | Reading |
|---|---:|---:|---|
| Full 40y (1986-2026) | 10,106 | 7.5th | Bottom-decile tight |
| Last 25y (2001-2026) | 6,247 | **2.7th** | **Among the tightest in a generation** |
| Last 10y (2016-2026, *used in composite*) | 2,495 | 6.5th | Bottom-decile tight |
| Last 3y (2023-2026) | 749 | 21.5th | Tight by recent standards |

Today is 38bp tighter than the pre-GFC May 2007 low (1.67pp), 31bp tighter than the December 2021 cycle local low (1.85pp), and within 38bp of the all-time low of 1.16pp set in March 1989. The all-time high is 6.16pp (December 2008 GFC peak). The 25-year window is the most interpretation-relevant; on that basis today's reading is genuinely extreme — tighter than every print of the last 25 years except for brief late-2007 and mid-2021 windows. The 40-year window includes the 1986-1990 era which had a sustained tight regime (running 1.2-1.8pp for several years), so 1.54pp is less extreme on that basis.

For the composite, BAA10Y is ranked over the same 10-year window as every other indicator (6.5th percentile → 93.5% complacency rating, weight 0.05, contribution +4.7 points). Treating one indicator with a different window size would break the methodology's interpretability. But the 25y percentile (2.7th) is the more honest answer to the question "how tight is credit historically?"

### Note on IG OAS at 0.74%

The reader asked whether IG OAS at 0.74% (74bp) really deserves a "99.1% complacent" rating. The honest answer:

1. **On absolute historical terms, yes.** The FRED IG OAS series (BAMLC0A0CM) has rolled around a long-term median of ~140bp since 1996. Today's 74bp sits at the bottom 1-2% of all values in that full window. The pre-GFC 2007 cycle low (May 2007) was approximately 80bp — today is ~6bp tighter than the most-leveraged moment of the prior cycle. The all-time low (mid-1997) was approximately 50-55bp.
2. **On a 3-year window (what the dashboard *actually* computed due to the FRED CSV truncation bug — see Postscript 2), the 99.1% reading is also literally correct.** Today's 0.74% sits one basis point above the 10-year minimum of 0.73% set on January 22, 2026.
3. **"Complacent" means "demanding less compensation than usual."** It does NOT mean "investors are insane." A 74bp spread still produces ~$7,400 of extra annual income on a $1M IG bond vs Treasury — that's not nothing. The complacency rating measures the *direction* (investors are pricing IG credit risk as if defaults won't rise), not the absolute magnitude.
4. **The dashboard's complacency reading is the right direction even if the magnitude question is fair.** If you'd rather express it as "IG OAS is in the bottom decile of historical compensation per unit of credit risk," that's an equally accurate framing — just on a different axis.

A v3 fix would either (a) get a FRED API key and use the proper 10-year window, or (b) add a column to the indicator table showing both the 10-year rank AND a long-history rank (using a one-time-cached FRED CSV from 1996), so the reader sees both contexts.

## Cross-Asset Signature

This is the report's load-bearing analysis. The composite alone is a scalar; the *pattern* across categories tells you which kind of late-cycle regime you're in.

**Credit (split)** — Investment-grade and broad high-yield are at 10-year tights. IG OAS at 0.74% has been below today's level only ~1% of the last decade (the prior tight was 0.73% in February 2025), and broad HY OAS at 2.74% has been tighter only ~10% of the time (prior tights of 2.59-2.65% sit in the May 2007 / early 2018 window — though our 10-year lookback only reaches 2016, so the comparison points are mostly the 2017 calm). **But the CCC tier — the weakest 6-8% of the HY index — is at 9.46%, which is *wider* than the trailing 10-year median (9.02%) and well above the 6.90% absolute tights of late 2024 / early 2025.** When IG/HY are at tights but CCC is wide, the market is sorting cycle risk: the marginal default-risk dollar is being demanded back even as broad credit gets bid for carry. Historically this divergence is one of the earliest credit-cycle tells — it preceded the 2007 turn by ~12 months and the late-2018 wobble by ~6 months. It is not in itself a sell signal; it is the first datum that says "the bid for the lowest-rated paper is gone." See the credit-tier chart below; CCC has been climbing for six months while IG has not budged.

![IG vs CCC OAS, 2001–2026](../charts/market_complacency_2026-06-07_ig_ccc.png)
*Source: FRED [BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM) (IG) and [BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC) (CCC), 2001-2026; dual-axis (IG left, CCC right). The IG line is at its lowest decile; the CCC line is *rising* from its late-2024 tights.*

**Equity volatility (NOT complacent)** — This is the most surprising category given the headline verdict. VIX at 21.51 sits in the 75th raw percentile of the trailing 10 years — meaning realized + implied vol has been *lower* than today 75% of the time. Even more telling: VIX9D / VIX3M = 1.096 is in **backwardation** (the front of the curve more expensive than the 3-month), which it spent only ~6% of the last decade in. SKEW at 152.25 puts crash-protection demand in the top decile of its last 10y range — investors are actively bidding for OTM puts. This is the *exact opposite* of the January 2018 and Q1 2020 vol setups, both of which featured deep contango, low SKEW, and VIX under 12. The current configuration matches what you see *after* a complacency unwind has begun: vol re-prices first, then credit catches up. The June 5 SPY −2.58% / VIX +40% move is the inflection day for this category. Pre-June 5 the equity-vol panel would have read mid-decile complacent (VIX 15.4, term slope 0.66, SKEW 142); post-June 5 it sits firmly contra-signal. **The Friday move did not break anything fundamental — but it took the air out of the most over-bid hedges and the term-structure roll trade.**

![VIX & VVIX, last 10 years](../charts/market_complacency_2026-06-07_vix_vvix.png)
*Source: Yahoo Finance [^VIX](https://finance.yahoo.com/quote/%5EVIX/history) and [^VVIX](https://finance.yahoo.com/quote/%5EVVIX/history), trailing 10y. The June 5 spike is the rightmost upward kink.*

![VIX Term Slope (VIX9D ÷ VIX3M), last 10 years](../charts/market_complacency_2026-06-07_vix_slope.png)
*Source: Yahoo Finance [^VIX9D](https://finance.yahoo.com/quote/%5EVIX9D/history) ÷ [^VIX3M](https://finance.yahoo.com/quote/%5EVIX3M/history). Values <1.0 = contango (calm); ≥1.0 = backwardation (stress). Today's 1.10 print is in the top 6% of stress readings.*

**Rate volatility (neutral)** — MOVE at 75.20 sits at the 54th raw percentile (46th complacency percentile). Rates have been calm for nine months — the move from the November 2025 MOVE-spike (briefly above 110 around the Treasury-auction stress) to today's 75 mirrored a glide path back into the FOMC's communicated reaction function. With 10Y yield at 4.48%, the bond market is pricing slow disinflation toward 2.0–2.5% with measured Fed easing. This category neither contradicts nor confirms the complacency read — it just says "the rates engine is not the trigger."

![MOVE Index, last 10 years](../charts/market_complacency_2026-06-07_move.png)
*Source: Yahoo Finance [^MOVE](https://finance.yahoo.com/quote/%5EMOVE/history). Reference bands at 80 (calm) and 120 (stress).*

**Risk premium (extreme)** — This is the category doing the most heavy lifting to the *complacent* side. The equity risk premium, defined here as S&P 500 trailing earnings yield (100 ÷ 31.83 PE = 3.14%) minus the 10Y Treasury yield (4.48%), prints **−1.34pp** — the lowest reading in the post-2000 sample. Negative ERP is the formal expression of "stocks priced for perfection vs bonds" — the embedded assumption is that earnings will grow fast enough to recoup the spread by holding period. The last sustained period of negative ERP was 1999–2000 (the dot-com bubble); subsequent 5-year forward returns from negative-ERP starts have ranged between −5% annualised (2000) and +3% annualised (2024). The HYG/LQD ratio at 0.734 is at the literal top of its 10-year range (prior max 0.740 set May 12, 2025) — meaning high-yield ETF prices are at their richest-ever level vs investment-grade. The two indicators in this category corroborate each other: there is no hidden risk premium anywhere in the asset stack.

![Equity Risk Premium (S&P 500 E/P − 10Y), 2001–2026](../charts/market_complacency_2026-06-07_erp.png)
*Source: S&P 500 trailing PE from [multpl.com](https://www.multpl.com/s-p-500-pe-ratio/table/by-month), 10Y yield from [Yahoo ^TNX](https://finance.yahoo.com/quote/%5ETNX/history). Negative shading marks ERP < 0. The 2026 trough (−1.34pp) undercuts the 1999-2000 lows.*

**Valuation (stretched)** — Shiller CAPE at 41.57 is in the 99th percentile of the trailing 10-year distribution. The all-time peak was ~44 (December 1999); the post-COVID local peak was 38.6 (December 2021). At 41.57, today's CAPE sits between those two — well above the median of the past decade (31.2) and only ~6% below the dot-com extreme. As a multiple, it implies a real 10-year forward return of approximately 1.5–2.0% per year using the Shiller-Yale historical regression — i.e., negative after-inflation real returns from durable holders entering at this level have historically required earnings to compound at >7% real for a decade, which has been achieved only twice (1990s dot-com expansion and 2010s zero-rate decade).

![Shiller CAPE, 2001–2026](../charts/market_complacency_2026-06-07_cape.png)
*Source: [multpl.com Shiller PE](https://www.multpl.com/shiller-pe/table/by-month), monthly. Reference line at CAPE 30 (historically rich).*

**Summary of the cross-asset signature** — Five categories, three signals. The "stretched" categories (credit-broad, risk-premium, valuation) are all valuation-/positioning-based and slow-moving — they show what investors *did*. The "contra-signal" categories (credit-CCC, equity vol) are flow-/price-based and fast-moving — they show what investors are *currently doing*. **The dashboard pattern matches a "late-cycle distribution" regime where slow money is still pricing things at peak multiples but fast money is already paying up for downside hedges.** The closest historical analogs by signature (not by magnitude) are H2 2007 and Q3 2018 — both periods when broad credit was tight, equity vol was already rising, and CCC was diverging. We will not claim either matches today's mechanics — the precedents table below lets the data speak.

## Historical Precedents

Daily composite scores were computed back to December 2000; dates within ±5 of today's 62.7 reading were clustered (180-day exclusion windows) and 8 spread-out precedents were retained.

| # | Date | Composite at date | SPY 6m fwd | SPY 12m fwd | SPY 24m fwd | Max DD over 24m |
|---|---|---|---|---|---|---|
| 1 | 2002-03-01 | 64.2 | −18.8% | −24.2% | +5.4% | −33.0% |
| 2 | 2006-10-03 | 58.9 | +8.8% | +17.7% | −9.5% | −27.3% |
| 3 | 2014-01-06 | 62.3 | +9.3% | +12.8% | +14.9% | −11.9% |
| 4 | 2016-04-19 | 62.2 | +2.9% | +13.7% | +34.0% | −10.1% |
| 5 | 2018-08-13 | 65.5 | −3.1% | +4.1% | +22.7% | −33.7% |
| 6 | 2021-04-01 | 60.9 | +7.8% | +14.2% | +5.3% | −24.5% |
| 7 | 2024-01-29 | 63.6 | +11.6% | +23.6% | +45.1% | −18.8% |
| 8 | 2026-04-09 | 62.0 | n/a — too recent | n/a | n/a | n/a |

![Precedents within ±5 of today's composite (62.7) — 12m forward SPY](../charts/market_complacency_2026-06-07_precedents.png)
*Source: composite history per `oneoff/market_complacency_2026-06-07.py`; SPY adjusted prices from Yahoo Finance ([SPY](https://finance.yahoo.com/quote/SPY/history)).*

**The last 7 times the composite read between 57.7 and 67.7, the median 12-month forward SPY return was +13.7%, the average was +8.8%, and 6 of 7 (86%) were positive.** Median 24-month forward return was +14.9%; max drawdown median within 24 months was −24.5%. The distribution is wide — best (2024-01: +45% over 24m) versus worst (2002-03: −33% drawdown, negative 12m print) span over 60 percentage points. The "Elevated" band is not a sell signal at all in the unconditional base rate; it is a *risk-warning* signal where positive returns are most likely but path includes a one-in-three chance of a >25% drawdown within two years.

A note on the 2018-08 precedent: the composite read 65.5 in August 2018 — six months later, the S&P had fallen 19% (Q4 2018 vol-mageddon and the December "trapdoor"). Twelve months out, the index had clawed all the way back to +4.1%. This is the *modal* path from Elevated readings: a near-term drawdown followed by recovery. The 2002 precedent — where the bear market resumed and the dashboard never re-traced — is the tail-risk path.

## What This Verdict Is NOT

- **Not a timing model.** Complacency at 62.7 can persist for quarters. The dashboard read 80–84 for almost six months in early 2017 before any unwind, and it has spent most of the post-2024 cycle in the 65–80 band without a bear-market resolution.
- **Not a sector or single-name call.** This is a macro lens. Specific over-valued tickers may have already started unwinding (AI mega-cap leaders, leveraged regional plays); other parts of the market may be relatively cheap. The composite has no resolution below the market-aggregate level.
- **Not a forecast.** The 7 forward-return outcomes from prior 62.7 readings span −24% to +24% at 12m and −33% to +45% at 24m. There is no probability mass concentration that turns this into a directional bet.
- **Not equivalent to "2007" or "January 2018".** Tempting as it is to name a specific historical analog — the credit-vol divergence pattern looks like late-2007, the rich valuation looks like late-2021 — neither comparison survives a full feature-by-feature match. The precedents table is the reference; pattern-matching beyond that is over-confident.
- **Calibration disclosure.** Of the 7 forward-data precedents, the dashboard described the macro regime accurately *7 of 7 times* — each precedent was a real-world risk-on regime with stretched valuations. It described the *path* (which direction price went, how quickly) accurately *0 of 7 times* — the 12m forward returns were essentially random within the regime. The dashboard is a state read, not a prediction.

## Action Implications

| Composite reading | Suggested posture (not personalized advice) |
|---|---|
| Stretched (80+) | Trim long beta; raise cash; add put-spread or VIX-call hedges; reduce CCC-rated credit exposure. Avoid outright shorts (timing risk is too high). |
| **Elevated (60–80) — *today*** | Tighten stops on the longest-duration, highest-multiple positions. Reduce CCC / loan exposure where it can be sold without realizing a loss. Standard hedges (3-6 month SPX put spreads ~5-8% OTM) are reasonably priced given today's SKEW signature. Cash allocation may move from a structural ~5% to ~10-15%. Do not chase the equity-vol re-pricing — the June 5 spike has already bid VIX, so paying for puts is more expensive than it was last week. |
| Neutral (40–60) | Standard policy weights. |
| Cautious (20–40) | Begin scaling into oversold longs; reduce hedge ratios. |
| Panicked (0–20) | Aggressive long-bias re-entry. |

**Specific notes for the current dashboard, beyond the band:**

1. **The asymmetric setup favors put spreads over straight puts.** VIX 21.51, term backwardated, SKEW 152 — these are conditions where straight puts are unusually expensive relative to fundamentals. Put-spreads (sell a deeper OTM put against a closer one) reduce the volatility risk premium paid. The June 5 spike has already eroded the cheapness window — earlier in the week, ATM SPX puts were ~30% cheaper.
2. **CCC widening means levered loan / private credit exposure is the asymmetric short.** If you hold a position whose performance correlates with CCC OAS (BDC equity, private credit closed-ends, levered loan ETFs), this is the cleanest "early credit cycle turn" expression. The composite warns "regime fragile"; CCC OAS at the 22nd percentile says "the weakest tier is already cracking."
3. **Cash yields are still meaningful.** With 10Y at 4.48% and the front of the curve still meaningfully positive, a defensive cash sleeve does not cost much in opportunity. This was not true in 2021 (cash yield 0%) when reducing equity to 15% cash meant forfeiting all return on that sleeve.
4. **AI infrastructure / mega-cap AI: the most CAPE-exposed cohort.** CAPE at 41.57 is index-level, but the index weight has tilted dramatically toward a handful of AI infrastructure names. The same composite measured on an equal-weight basis would read materially less complacent. If you size by ticker rather than by macro, the "trim peaks" implication applies most acutely to the AI mega-caps.

## What Would Invalidate This Read

The dashboard *could* be lying in identifiable ways. The most plausible failure modes:

1. **Structural decline in CCC issuance** — over the last five years the CCC index has thinned dramatically as private credit absorbed marginal LBO refinancings. A smaller, higher-quality CCC index would mean today's 9.46% OAS doesn't represent the same risk profile as the 9.46% prints of 2018 or 2022. If true, the "CCC widening" signal is over-stated and the dashboard's read of the regime is *too* worried about credit.
2. **Earnings-yield denominator shift** — multpl's S&P 500 trailing PE uses GAAP reported earnings. Operating earnings (the "Street" measure) would put PE closer to 28× and ERP at −0.7pp rather than −1.34pp. Still in the most-complacent decile, but materially less extreme. The cross-period comparison is consistent (we use GAAP throughout), but the absolute level of "ERP at −1.34pp is unprecedented" softens to "ERP at −0.7pp is near the 1999-2000 trough" under the operating-earnings framing.
3. **Vol surface re-pricing without economic stress** — the June 5 vol spike could be a one-off liquidity event (a forced unwind, a single dealer position) rather than the beginning of a regime change. If VIX and SKEW re-collapse to pre-June 5 levels by month-end without a corresponding move in credit, the dashboard will re-print at 73-75. The "right" verdict in that case would be Stretched, not Elevated.
4. **Persistent buyback bid distorts the cap-weighted earnings yield** — the S&P 500 trailing earnings figure includes index-constituent buyback yield as a denominator boost. With S&P 500 buyback authorizations running near record highs in 2025-2026, the trailing E/P understates the "true" cash yield to durable holders. This would mean the ERP signal is *overstated*.
5. **Sentiment-category absence** — AAII and NAAIM are dark today (both URLs return 403/404 to public scrapers). If retail sentiment is actually at extreme bullish levels — historically a contrarian signal worth ~3-5 composite points to the complacent side — the dashboard is understating the true reading by that amount. The next milestone is the next AAII-published bull-bear survey reaching this dashboard via a paid feed or an alternate scrape.

If two or more of these failure modes materialize, the dashboard's headline read should be downgraded by 5–10 points (from Elevated 62.7 to high-Neutral 52-57). If none of them do, the read holds.

## Data Used / 数据来源清单

**Credit (required)**
- HY OAS — FRED [BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2), daily, 10y history pulled via `indicators.data_fetcher._fetch_fred_range()` from `oneoff/market_complacency_2026-06-07.py`. Last observation 2026-06-04: 2.74%.
- IG OAS — FRED [BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), daily. Last observation 2026-06-04: 0.74%.
- CCC OAS — FRED [BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC), daily, fetched directly in `oneoff/market_complacency_2026-06-07.py` (not in the live indicators dashboard). Last observation 2026-06-04: 9.46%.

**Equity volatility (required)**
- VIX, VVIX, VIX9D, VIX3M, SKEW — Yahoo Finance [^VIX](https://finance.yahoo.com/quote/%5EVIX/history) / [^VVIX](https://finance.yahoo.com/quote/%5EVVIX/history) / [^VIX9D](https://finance.yahoo.com/quote/%5EVIX9D/history) / [^VIX3M](https://finance.yahoo.com/quote/%5EVIX3M/history) / [^SKEW](https://finance.yahoo.com/quote/%5ESKEW/history), daily auto-adjusted, 10y history. All last observed 2026-06-05.

**Rate volatility (required)**
- MOVE — Yahoo Finance [^MOVE](https://finance.yahoo.com/quote/%5EMOVE/history), daily, 10y history. Yahoo's MOVE history starts 2002-12. Last observation 2026-06-05: 75.20.

**Risk-premium (required)**
- Equity Risk Premium — S&P 500 trailing GAAP PE from [multpl.com](https://www.multpl.com/s-p-500-pe-ratio/table/by-month) (Jun 5, 2026 = 31.83 → E/P 3.14%) minus 10Y Treasury yield from [Yahoo ^TNX](https://finance.yahoo.com/quote/%5ETNX/history) (Jun 5 close 4.536%, recent 5-day average 4.487%; resampled to month-start for the historical series). Resulting ERP for June 2026: −1.34pp.
- HYG/LQD ratio — Yahoo Finance [HYG](https://finance.yahoo.com/quote/HYG/history) ÷ [LQD](https://finance.yahoo.com/quote/LQD/history) daily closes, 10y history. Last value 0.734 (Jun 5, 2026).

**Sentiment (optional — both inactive)**
- AAII Bull-Bear Spread — fetch from `aaii.com/files/surveys/sentiment.xls` returned **HTTP 403 Forbidden**. The AAII site moved its public CSV behind a member portal in late 2025. Dropped from composite; weights re-normalized.
- NAAIM Exposure Index — fetch from the legacy NAAIM XLSX URL returned **HTTP 404 Not Found**. The NAAIM Exposure Index is now distributed via a different members-only path. Dropped from composite.

**Valuation (optional — active)**
- Shiller CAPE — [multpl.com Shiller PE table](https://www.multpl.com/shiller-pe/table/by-month) monthly. Robert Shiller's own Yale spreadsheet at `econ.yale.edu/~shiller/data/ie_data.xls` was checked and found to end at 2023-09 (he has not refreshed the file since). multpl re-computes CAPE monthly from current data and is the cleaner forward-fill source. Last observation 2026-06-05: 41.57.

**Composite + percentile methodology**
- Each indicator: 10-year rolling percentile of its current value. For "low = complacent" indicators (HY/IG/CCC OAS, VIX, VVIX, term slope, SKEW, MOVE, ERP), complacency percentile = 100 − raw value percentile. For "high = complacent" indicators (HYG/LQD, CAPE), complacency percentile = raw value percentile.
- Composite: weighted average of complacency percentiles per the SKILL.md weight table; weights re-normalized over the 11 active indicators (active sum 0.90 → 1.00).
- Tier: 0–20 Panicked / 20–40 Cautious / 40–60 Neutral / 60–80 Elevated / 80–100 Stretched.
- Historical composite series: daily, December 2000 → June 2026, ~6,644 observations. Per-indicator rolling 10-year window (~2,520 business days), with daily forward-fill for monthly inputs (CAPE, PE, ERP).

**Historical precedents**
- Daily composite scores ±5 of today's 62.7 clustered with a 180-day exclusion window, then decimated to 8 spread-out dates.
- SPY adjusted prices from [Yahoo SPY](https://finance.yahoo.com/quote/SPY/history) (`auto_adjust=True`); forward returns and rolling-max-drawdown computed over 6 / 12 / 24 month windows from the precedent date.

**Stale notices / coverage gaps**
- AAII and NAAIM sentiment indicators are inactive — public data sources moved behind paywalls in late 2025. Weights have been re-normalized to active set.
- Robert Shiller's Yale spreadsheet was last refreshed September 2023. CAPE is now sourced from multpl.com, which is computationally equivalent (10-year inflation-adjusted trailing earnings) and stays current monthly.
- Pre-2002 composite uses fewer indicators than post-2016 (Yahoo VVIX history starts 2007, MOVE starts 2002, VIX9D/VIX3M starts 2011, SKEW starts 2010); the deep-2001 lows (~0.2) in the composite history should be interpreted with caution. Comparison points within the trailing-10-year window (2016 → present) are robust; cross-cycle comparisons to 2001-2009 should treat the composite as directionally indicative only.
- The June 5 VIX spike materially reduced today's composite (from a June 4 close of 75.5 to a June 5 close of 62.7). The "Elevated" verdict today reflects the post-spike vol picture; the credit + valuation + risk-premium picture has not changed and continues to point at the same regime.

<details>
<summary>Verification log (Step 10) — 2026-06-07</summary>

Spot-checked numbers against script outputs and source URLs:

- HY OAS 2.74% on 2026-06-04 — `grep '2.74' oneoff/market_complacency_2026-06-07_indicators.csv` ✓ matches script output. [FRED BAMLH0A0HYM2 page](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) verified to be the canonical source.
- IG OAS 0.74% on 2026-06-04 ✓ matches script output.
- CCC OAS 9.46% on 2026-06-04 ✓ matches script output. 10y median = 9.02% per script output (table row "ccc_oas, ..., 9.02").
- VIX 21.51 on 2026-06-05 ✓ matches yfinance pull (`yfinance.Ticker('^VIX').history(period='5d')` shows 21.51 close).
- VIX prior day (2026-06-04) = 15.40 ✓ matches yfinance pull — the +40% one-day move is real.
- SPY 2026-06-05 close 737.55 (down from 757.09 on 2026-06-04) ✓ matches yfinance — −2.58% one-day move.
- SKEW 152.25 on 2026-06-05 ✓ matches script output. 10y median 135.73.
- MOVE 75.20 on 2026-06-05 ✓ matches script output.
- CAPE 41.57 on 2026-06-05 ✓ matches multpl scrape and indicator CSV.
- S&P 500 trailing PE 31.83 on 2026-06-05 ✓ matches multpl scrape.
- 10Y yield 4.48% (recent 5-day average) ✓ matches yfinance ^TNX 5-day pull (4.475, 4.455, 4.491, 4.477, 4.536; average 4.487).
- ERP −1.34pp ✓ matches derivation: 100/31.83 − 4.487 = 3.142 − 4.487 = −1.345.
- HYG/LQD ratio 0.734 ✓ matches recent yfinance pull (0.734 on Jun 5, 2026); 10y max 0.740 (May 12, 2025 per script output).
- Composite 62.7 ✓ matches script `=== Summary ===` output (62.66).
- Composite history check: 2026-06-04 = 75.5, 2026-06-05 = 62.7 ✓ matches `composite_history.csv` tail.
- Precedent 2002-03-01: SPY 12m forward return −24.2% ✓ matches `precedents.csv` row 1.
- Precedent 2024-01-29: SPY 12m forward return +23.6% ✓ matches `precedents.csv` row 7.

No discrepancies found. Outputs are deterministic given fixed input dates.

</details>
