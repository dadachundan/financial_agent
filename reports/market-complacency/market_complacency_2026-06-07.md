# Market Complacency Dashboard — 2026-06-07

> **Dashboard's Take.** **Flag count 8 / 20 — Citi-BMC style: 7 red + 2 amber + 11 off.** US equities are at near-term highs with clear valuation exuberance. **Three slow-moving indicators (CAPE 41.6, S&P 500 DY 1.06%, Moody's BAA−10Y 1.54pp) are at or past the levels that triggered the worst US bear markets of the post-1995 era** — yet the yield curve is positive at +38bp, equity vol is mid-range, and SKEW at 152 is in the contra zone (hedges already bid). The signature is **"dot-com-extreme valuation + already-bid hedges"** — not a uniform sell signal. Action: trim peaks, tighten stops, prefer put-spreads over naked puts, exit CCC credit, skip outright shorts. Empirical base rate at flag-count 6-10: median 12m forward SPY +14%, ~30% probability of a >20% drawdown within 24 months.

## Figure 2. Bear Market Checklist — Historical Calibration

Today vs the start of past bear markets and recent peaks. **Red = full flag, 🟠 = half flag, blank = off.** Adapted from [Citi BMC Figure 2](https://www.citivelocity.com).

| Indicator (click for source / historical chart) | **Mar-00** | **Oct-07** | **Feb-20** | **Dec-21** | **Now** |
|---|:---:|:---:|:---:|:---:|:---:|
| **Global Equity Valuations** | | | | | |
| [Trailing PE (SPX)](https://www.multpl.com/s-p-500-pe-ratio) | 🔴 33 | 17 | 🟠 19 | 🟠 21 | 🔴 **32** |
| [S&P 500 Dividend Yield](https://www.multpl.com/s-p-500-dividend-yield) | 🔴 1.16 | 1.77 | 1.79 | 🔴 1.29 | 🔴 **1.06** |
| [Shiller CAPE](https://www.multpl.com/shiller-pe) | 🔴 43 | 🟠 27 | 31 | 🔴 38 | 🔴 **42** |
| Equity Risk Premium (pp) — [S&P 500 E/P](https://www.multpl.com/s-p-500-earnings-yield) − [10Y](https://fred.stlouisfed.org/series/DGS10) | n/a | +0.5 | +1.7 | +2.0 | 🔴 **−1.34** |
| **Yield Curve** | | | | | |
| [10Y − 2Y (bp)](https://fred.stlouisfed.org/series/T10Y2Y) | 🔴 −47 | 🟠 +54 | +27 | +79 | +38 |
| **Sentiment** | | | | | |
| [Margin Debt / SPX](https://www.finra.org/investors/insights/margin-statistics) | 200 | 243 | 184 | 🟠 191 | **181** (mid) |
| **Corporate Behaviour** | | | | | |
| [US Capex YoY (%)](https://fred.stlouisfed.org/series/PNFI) | 🟠 9.7 | 🟠 8.0 | +1.1 | 🟠 7.9 | 🟠 **8.4** |
| [US M&A (last 12m % of Mkt cap)](https://www.bain.com/insights/topics/m-and-a-report/) | 🔴 11.4 | 🔴 8.1 | 4.4 | 🟠 5.0 | **3.7** |
| [US IPO (last 12m % of DM Mkt cap)](https://www.renaissancecapital.com/IPO-Center/Stats) | 🔴 0.7 | 🟠 0.4 | 0.2 | 🟠 0.6 | **0.4** |
| **Profitability** | | | | | |
| [EPS dist from rolling-10y peak (%)](https://www.multpl.com/s-p-500-earnings) | 0 | −13 | −6 | 0 | 🟠 **0** |
| **Balance sheets / credit markets** | | | | | |
| [Moody's BAA − 10Y (pp)](https://fred.stlouisfed.org/series/BAA10Y) | 🟠 2.30 | 🟠 1.99 | 🟠 2.38 | 🟠 1.85 | 🔴 **1.54** |
| [HY OAS (%)](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) *(ICE BofA, 2023+; Citi pre-2023)* | 6.00 | 6.00 | 🟠 4.80 | 3.37 | 🔴 **2.74** |
| [IG OAS (%)](https://fred.stlouisfed.org/series/BAMLC0A0CM) *(same caveat)* | 1.75 | 1.75 | 🟠 1.21 | 0.90 | 🔴 **0.74** |
| [CCC OAS](https://fred.stlouisfed.org/series/BAMLH0A3HYC) − HY spread (pp) *(derived; ICE BofA only 2023+)* | n/a | n/a | n/a | n/a | 🟢 **6.72** (10y max — contra) |
| [HYG](https://finance.yahoo.com/quote/HYG/) / [LQD](https://finance.yahoo.com/quote/LQD/) ratio *(HYG launched Apr 2007)* | n/a | 0.635 | 0.582 | 0.611 | 🔴 **0.734** (19y high) |
| **Equity / Rate Vol** | | | | | |
| [VIX](https://finance.yahoo.com/quote/%5EVIX/) | 24.1 | 18.5 | 🚨 40.1 | 17.2 | 21.5 |
| [SKEW](https://finance.yahoo.com/quote/%5ESKEW/) | 113 | 117 | 131 | 154 | 🟢 **152** (contra) |
| [MOVE](https://finance.yahoo.com/quote/%5EMOVE/) | n/a | 90 | 110 | 77 | 75 |
| [VIX9D](https://finance.yahoo.com/quote/%5EVIX9D/) / [VIX3M](https://finance.yahoo.com/quote/%5EVIX3M/) *(VIX9D launched 2011)* | n/a | n/a | 🚨 1.77 (COVID panic) | 0.61 | 🟢 **1.10 backwardated** (contra) |
| **# Flags (this dashboard / 20)** | n/a* | n/a* | n/a* | n/a* | **8.0** |
| **# Flags (Citi BMC / 18)** | 17.5 | 13.0 | 5.5 | 8.5 | 10.0 (Global), 11.5 (US) |

*Pre-2007 totals incomplete — VVIX, SKEW, MOVE histories shorter than the dashboard's lookback.

🟢 = contra-signal (low complacency rating despite high absolute value — "already-bid hedges" or "credit-tier divergence")

**Today's calibration**: CAPE is within 1 point of the March 2000 dot-com peak. Dividend yield is *below* the dot-com low. Moody's BAA−10Y is the tightest of any reference date. But: yield curve is positive, SKEW is contra (top-decile crash demand), VIX slope backwardated, CCC widening relative to HY (10y max). **No clean historical precedent** — past bears started with one or the other, not both.

## Under the Hood

Indicator histories with bear-market shading and last-10y percentile reference lines. **Click any source link below the chart** to view the canonical free historical chart for that indicator.

![Figure 3: Long-history credit (Moody's BAA−10Y + HY OAS reference points)](../charts/market_complacency_2026-06-07_hy_oas.png)
*Sources: [FRED Moody's BAA−10Y (BAA10Y, 1986+)](https://fred.stlouisfed.org/series/BAA10Y) · [FRED ICE BofA HY OAS (BAMLH0A0HYM2, 2023+)](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) · [TradingEconomics HY OAS long-history chart](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-high-yield-option-adjusted-spread-fed-data.html)*

![Figure 4: Long-history IG credit — Moody's AAA−10Y vs BAA−10Y + dispersion](../charts/market_complacency_2026-06-07_ig_ccc.png)
*Sources: [FRED Moody's AAA−10Y (AAA10Y, 1983+)](https://fred.stlouisfed.org/series/AAA10Y) · [FRED Moody's BAA−10Y (BAA10Y, 1986+)](https://fred.stlouisfed.org/series/BAA10Y) — Replaces the FRED-restricted ICE BofA IG/CCC overlay (both 2023+ only). The BAA − AAA dispersion (grey) is the long-history analog of "CCC − HY spread": widens before credit-cycle turns. GFC peak (>6pp BAA, ~3.5pp dispersion) and COVID spike (BAA to 4.3pp) clearly visible.*

![Figure 5: Shiller CAPE](../charts/market_complacency_2026-06-07_cape.png)
*Source: [multpl.com Shiller PE Ratio (monthly, 1871+)](https://www.multpl.com/shiller-pe) · derived from [Robert Shiller's Yale dataset](http://www.econ.yale.edu/~shiller/data.htm).*

![Figure 6: Equity Risk Premium](../charts/market_complacency_2026-06-07_erp.png)
*Sources: [multpl S&P 500 Earnings Yield](https://www.multpl.com/s-p-500-earnings-yield) (E/P component) · [FRED 10Y Treasury (DGS10, 1962+)](https://fred.stlouisfed.org/series/DGS10) (bond yield component). ERP = E/P − 10Y, derived monthly in the build script.*

![Figure 7: VIX & VVIX](../charts/market_complacency_2026-06-07_vix_vvix.png)
*Sources: [CBOE VIX (1990+) via Yahoo Finance](https://finance.yahoo.com/quote/%5EVIX/) · [CBOE VVIX (2007+) via Yahoo Finance](https://finance.yahoo.com/quote/%5EVVIX/) · canonical reference: [CBOE VIX page](https://www.cboe.com/tradable_products/vix/).*

![Figure 8: VIX Term Slope (VIX9D / VIX3M)](../charts/market_complacency_2026-06-07_vix_slope.png)
*Sources: [CBOE VIX9D (2011+)](https://finance.yahoo.com/quote/%5EVIX9D/) · [CBOE VIX3M (2008+)](https://finance.yahoo.com/quote/%5EVIX3M/). Ratio < 1 = contango (calm); ≥ 1 = backwardation (front-month fear).*

![Figure 9: MOVE Index](../charts/market_complacency_2026-06-07_move.png)
*Source: [ICE BofAML MOVE Index via Yahoo Finance (2002+)](https://finance.yahoo.com/quote/%5EMOVE/) — the rate-vol analog of VIX, measuring 1-month implied vol on US Treasuries.*

![Figure 10: Per-Indicator Complacency Bars](../charts/market_complacency_2026-06-07_indicators_bar.png)
*Source: per-indicator 10-year rolling complacency percentile from `scripts/build_dashboard.py`. Inputs documented in the Data Used manifest below.*

## Data Used / 数据来源清单

Flag count and indicator percentiles computed in [`.claude/skills/market-complacency/scripts/build_dashboard.py`](../../.claude/skills/market-complacency/scripts/build_dashboard.py). Sources:

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
| Sentiment | Margin debt | [FINRA margin-statistics.xlsx](https://www.finra.org/sites/default/files/2021-03/margin-statistics.xlsx) (monthly back to 1997) |
| Equity / Rate Vol | VIX, VVIX, VIX9D, VIX3M, SKEW, MOVE | Yahoo Finance |
| Cross-reference | Citi BMC | [Citi Global Equity Strategy](https://www.citivelocity.com) "Bear Market Checklist: Exuberance Building" 2026-06-05 |
