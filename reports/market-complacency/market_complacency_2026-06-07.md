# Market Complacency Dashboard — 2026-06-07

> **Dashboard's Take.** US equities are at near-term highs with clearer signs of valuation exuberance. The dashboard composite stands at **59.5 / 100, top edge of Neutral**, with flag count **8.0 / 21** (Citi-BMC style: 7 red + 2 amber + 12 off). On three slow-moving indicators (CAPE, dividend yield, Moody's BAA−10Y) we are at or past the levels that triggered the worst US bear markets of the post-1995 era — yet the yield curve is positive, equity vol is mid-range and SKEW is already in the contra zone. **The signature is "dot-com-extreme valuation + already-bid hedges"** — not a uniform sell signal. Action: trim peaks, tighten stops, prefer put-spreads over naked puts, exit CCC credit, skip outright shorts. Empirical base rate at this composite range: median 12m forward SPY +14%, ~30% probability of a >20% drawdown within 24 months.

![Figure 1: Composite vs SPY Drawdown](../charts/market_complacency_2026-06-07_composite.png)
*Figure 1. Composite (0–100) overlaid on SPY drawdown depth, 2001–2026. Source: composite per `.claude/skills/market-complacency/scripts/build_dashboard.py`; SPY adjusted close from [Yahoo SPY](https://finance.yahoo.com/quote/SPY/history).*

## Figure 2. Bear Market Checklist — Historical Calibration

Today vs the start of past bear markets and recent peaks. **Red = full flag, 🟠 = half flag, blank = off.** Adapted from [Citi BMC Figure 2](https://www.citivelocity.com).

| | **Mar-00** | **Oct-07** | **Feb-20** | **Dec-21** | **Now** |
|---|:---:|:---:|:---:|:---:|:---:|
| **Global Equity Valuations** | | | | | |
| Trailing PE (SPX) | 🔴 33 | 17 | 🟠 19 | 🟠 21 | 🔴 **32** |
| S&P 500 Dividend Yield | 🔴 1.16 | 1.77 | 1.79 | 🔴 1.29 | 🔴 **1.06** |
| Shiller CAPE | 🔴 43 | 🟠 27 | 31 | 🔴 38 | 🔴 **42** |
| Equity Risk Premium (pp) | n/a | +0.5 | +1.7 | +2.0 | 🔴 **−1.34** |
| **Yield Curve** | | | | | |
| 10Y − 2Y (bp) | 🔴 −47 | 🟠 +54 | +27 | +79 | +38 |
| **Sentiment** | | | | | |
| Margin Debt / SPX | — | — | — | 🔴 high | 181 (mid) |
| CBOE Put/Call (21d) | — | — | — | — | 0.66 (stale Oct 2019) |
| **Corporate Behaviour** | | | | | |
| US Capex YoY (%) | 🟠 9.7 | 🟠 8.0 | +1.1 | 🟠 7.9 | 🟠 **8.4** |
| US M&A / Mkt cap | 🔴 high | 🔴 high | 4.4 | 🟠 5.0 | 3.7 |
| US IPO / Mkt cap | 🔴 high | 🟠 high | 0.2 | 🟠 0.5 | 0.3 |
| **Profitability** | | | | | |
| EPS dist from rolling-10y peak (%) | 0 | −13 | −6 | 0 | 🟠 **0** |
| **Balance sheets / credit markets** | | | | | |
| Moody's BAA − 10Y (pp) | 🟠 2.30 | 🟠 1.99 | 🟠 2.38 | 🟠 1.85 | 🔴 **1.54** |
| HY OAS (%) | 6.00 | 6.00 | 🟠 4.80 | 3.37 | 🔴 **2.74** |
| IG OAS (%) | 1.75 | 1.75 | 🟠 1.21 | 0.90 | 🔴 **0.74** |
| CCC − HY spread (pp) | n/a | n/a | n/a | n/a | 🟢 **6.72** (10y max — contra) |
| HYG / LQD ratio | n/a | n/a | low | mid | 🔴 **0.734** |
| **Equity / Rate Vol** | | | | | |
| VIX | 24.1 | 18.5 | 🚨 40.1 | 17.2 | 21.5 |
| SKEW | 113 | 117 | 131 | 154 | 🟢 **152** (contra) |
| MOVE | n/a | 90 | 110 | 77 | 75 |
| VIX9D / VIX3M | n/a | n/a | n/a | n/a | 🟢 **1.10 backwardated** (contra) |
| **# Flags (this dashboard / 21)** | n/a* | n/a* | n/a* | n/a* | **8.0** |
| **# Flags (Citi BMC / 18)** | 17.5 | 13.0 | 5.5 | 8.5 | 10.0 (Global), 11.5 (US) |

*Pre-2007 totals incomplete — VVIX, SKEW, MOVE histories shorter than the dashboard's lookback.

🟢 = contra-signal (low complacency rating despite high absolute value — "already-bid hedges" or "credit-tier divergence")

**Today's calibration**: CAPE is within 1 point of the March 2000 dot-com peak. Dividend yield is *below* the dot-com low. Moody's BAA−10Y is the tightest of any reference date. But: yield curve is positive, SKEW is contra (top-decile crash demand), VIX slope backwardated, CCC widening relative to HY (10y max). **No clean historical precedent** — past bears started with one or the other, not both.

## Under the Hood

Indicator histories with caution / stress thresholds and shading where applicable.

![Figure 3: HY OAS](../charts/market_complacency_2026-06-07_hy_oas.png)

![Figure 4: IG vs CCC OAS](../charts/market_complacency_2026-06-07_ig_ccc.png)

![Figure 5: Shiller CAPE](../charts/market_complacency_2026-06-07_cape.png)

![Figure 6: Equity Risk Premium](../charts/market_complacency_2026-06-07_erp.png)

![Figure 7: VIX & VVIX](../charts/market_complacency_2026-06-07_vix_vvix.png)

![Figure 8: VIX Term Slope](../charts/market_complacency_2026-06-07_vix_slope.png)

![Figure 9: MOVE Index](../charts/market_complacency_2026-06-07_move.png)

![Figure 10: Per-Indicator Complacency Bars](../charts/market_complacency_2026-06-07_indicators_bar.png)

![Figure 11: Historical Precedents Scatter](../charts/market_complacency_2026-06-07_precedents.png)

## Action Implications

| Verdict tier | Suggested posture |
|---|---|
| Stretched (80+) | Trim long beta; raise cash; add put-spread or VIX-call hedges; reduce CCC. **Avoid outright shorts** (timing risk too high). |
| **Elevated (60–80)** | Tighten stops on longest-duration positions; reduce CCC; standard hedges (3–6m SPX put spreads ~5-8% OTM). |
| **Neutral top edge — today** | Trim peaks (CAPE-sensitive cohort first), tighten stops, raise cash to 10–15% (10Y at 4.48% means opportunity cost is modest). |
| Neutral (40–60) | Standard policy weights. |
| Cautious / Panicked (< 40) | Scaling in; reduce hedges; aggressive long-bias at panicked. |

**Specific notes for today**: (1) SKEW at 152 makes naked puts expensive — **put-spreads beat puts**. (2) **CCC OAS divergence** is the cleanest "early credit cycle turn" expression — BDC equity, levered loan ETFs, private credit closed-ends are asymmetric short candidates. (3) **Cash now pays 4.5%** — opportunity cost of defensive cash sleeve is materially lower than in 2021.

## Historical Precedents

Daily composite scores within ±5 of today's 59.5:

| Date | Composite | SPY 6m | 12m | 24m | Max DD 24m |
|---|---:|---:|---:|---:|---:|
| 2004-02-18 | 56.7 | −4.2% | +6.8% | +15.8% | −7.5% |
| 2006-02-27 | 64.6 | +1.6% | +14.2% | +10.9% | −16.0% |
| 2013-07-17 | 57.1 | +11.1% | +20.2% | +31.4% | −7.3% |
| 2016-07-13 | 57.2 | +6.8% | +15.8% | +35.1% | −10.1% |
| 2018-10-10 | 62.9 | +4.7% | +6.7% | +28.4% | **−33.7%** |
| 2021-08-06 | 57.7 | +2.1% | −5.2% | +5.0% | −24.5% |
| 2023-11-14 | 61.7 | +17.5% | +34.8% | +56.2% | −18.8% |
| 2025-12-15 | 66.5 | n/a | n/a | n/a | n/a |

**Median 12m forward SPY: +14.2%. 6 of 7 (86%) positive. Median max DD within 24m: −18.8%. Two precedents had >20% DD (2018-10 / 2021-08).**

## Caveats

- **Low PE doesn't protect against a bear** — GFC and COVID both blew through low-PE markets. CAPE near dot-com levels says *"the eventual drawdown is likely deeper,"* not *"a drawdown is imminent."*
- **Dashboard is a regime descriptor, not a drawdown predictor.** Backtest precision at composite ≥ 80 = 22% vs 20.3% base rate, lift just 1.1×.
- **Not a forecast / not a timing model / not a sector call.** The Elevated/Neutral-top zone can persist for quarters.
- **2 of 21 indicators dark** (AAII / NAAIM upstream paywalls), composite re-normalized over the active 19.
- **ICE BofA OAS series limited to 2023-06 onward** (FRED re-licensing) — Moody's BAA−10Y carries the long-history credit signal back to 1986.

## Data Used / 数据来源清单

Composite computed in [`.claude/skills/market-complacency/scripts/build_dashboard.py`](../../.claude/skills/market-complacency/scripts/build_dashboard.py). Sources:

| Category | Indicator | Source |
|---|---|---|
| Credit | HY / IG / CCC OAS, BAA10Y | FRED via API: [BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2), [BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), [BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC), [BAA10Y](https://fred.stlouisfed.org/series/BAA10Y) |
| Yield Curve | 10Y − 2Y | FRED [T10Y2Y](https://fred.stlouisfed.org/series/T10Y2Y) |
| Valuation | CAPE, DY, Trailing PE | [multpl.com](https://www.multpl.com/shiller-pe/table/by-month), [DY](https://www.multpl.com/s-p-500-dividend-yield/table/by-month), [PE](https://www.multpl.com/s-p-500-pe-ratio/table/by-month) |
| Profitability | EPS distance from peak | [multpl monthly trailing EPS](https://www.multpl.com/s-p-500-earnings/table/by-month) |
| Risk Premium | ERP, HYG/LQD | derived (E/P − 10Y) + Yahoo Finance |
| Corp Behaviour | Capex YoY | FRED [PNFI](https://fred.stlouisfed.org/series/PNFI) |
| Corp Behaviour | IPO activity | [Renaissance Capital IPO Stats](https://www.renaissancecapital.com/IPO-Center/Stats) → cached `.claude/skills/market-complacency/data/ipo_proceeds_annual.csv` |
| Corp Behaviour | M&A volume | [Bain 2025 M&A report](https://www.bain.com/about/media-center/press-releases/20252/global-ma-stages-great-rebound-in-2025-with-$4.8-trillion-deal-value-to-mark-second-highest-total-on-record) + [S&P Global Q1 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/04/global-m-and-a-by-the-numbers-q1-2026) → cached |
| Sentiment | Margin debt | [FINRA margin-statistics.xlsx](https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx) |
| Sentiment | CBOE Put/Call (stale Oct 2019) | [cdn.cboe.com equitypc.csv](https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv) |
| Equity / Rate Vol | VIX, VVIX, VIX9D, VIX3M, SKEW, MOVE | Yahoo Finance |
| Cross-reference | Citi BMC | [Citi Global Equity Strategy](https://www.citivelocity.com) "Bear Market Checklist: Exuberance Building" 2026-06-05 |
