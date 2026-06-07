# Market Complacency Dashboard — 2026-06-07

> **Dashboard's Take.** **Flag count 7.5 / 19 — Citi-BMC style: 7 red + 1 amber + 11 off.** US equities are at near-term highs with clear valuation exuberance. **Three slow-moving indicators (CAPE 41.6, S&P 500 DY 1.06%, Moody's BAA−10Y 1.54pp) are at or past the levels that triggered the worst US bear markets of the post-1995 era** — yet the yield curve is positive at +38bp, equity vol is mid-range, and SKEW at 152 is in the contra zone (hedges already bid). The signature is **"dot-com-extreme valuation + already-bid hedges"** — not a uniform sell signal. Action: trim peaks, tighten stops, prefer put-spreads over naked puts, exit CCC credit, skip outright shorts. Empirical base rate at flag-count 6-10: median 12m forward SPY +14%, ~30% probability of a >20% drawdown within 24 months.

## Figure 2. Bear Market Checklist — Historical Calibration

Today vs the start of past bear markets and recent peaks. **Red = full flag, 🟠 = half flag, blank = off.** Adapted from [Citi BMC Figure 2](https://www.citivelocity.com).

<style>
.bmc-table { border-collapse: collapse; width: 100%; font-size: 0.92rem; margin: 0.5rem 0 1rem; }
.bmc-table th, .bmc-table td { padding: 6px 10px; border: 1px solid #d7dadc; text-align: center; vertical-align: middle; }
.bmc-table th { background: #f4f4f4; }
.bmc-table td.label, .bmc-table th.label { text-align: left; }
.bmc-table tr.section td { background: #fafafa; font-weight: 700; }
.bmc-red    { background: #f4a8a8 !important; color: #5a0000; font-weight: 700; }
.bmc-amber  { background: #ffd17a !important; color: #5a3300; font-weight: 700; }
.bmc-green  { background: #b6e3b6 !important; color: #1a4d1a; font-weight: 700; }
.bmc-stress { background: #c44; color: #fff; font-weight: 700; }
.bmc-na     { color: #999; }
.bmc-table td.now { border-left: 2px solid #888; }
</style>

<table class="bmc-table">
<thead>
<tr><th class="label">Indicator (click for source / historical chart)</th>
<th>Mar-00</th><th>Oct-07</th><th>Feb-20</th><th>Dec-21</th><th>Now</th></tr>
</thead>
<tbody>

<tr class="section"><td class="label" colspan="6">Global Equity Valuations</td></tr>
<tr><td class="label"><a href="https://www.multpl.com/s-p-500-pe-ratio">Trailing PE (SPX)</a></td>
<td class="bmc-red">33</td><td>17</td><td class="bmc-amber">19</td><td class="bmc-amber">21</td><td class="bmc-red now">32</td></tr>
<tr><td class="label"><a href="https://www.multpl.com/s-p-500-dividend-yield">S&amp;P 500 Dividend Yield</a></td>
<td class="bmc-red">1.16</td><td>1.77</td><td>1.79</td><td class="bmc-red">1.29</td><td class="bmc-red now">1.06</td></tr>
<tr><td class="label"><a href="https://www.multpl.com/shiller-pe">Shiller CAPE</a></td>
<td class="bmc-red">43</td><td class="bmc-amber">27</td><td>31</td><td class="bmc-red">38</td><td class="bmc-red now">42</td></tr>
<tr><td class="label">Equity Risk Premium (pp) — <a href="https://www.multpl.com/s-p-500-earnings-yield">S&amp;P 500 E/P</a> − <a href="https://fred.stlouisfed.org/series/DGS10">10Y</a></td>
<td class="bmc-na">n/a</td><td>+0.5</td><td>+1.7</td><td>+2.0</td><td class="bmc-red now">−1.34</td></tr>

<tr class="section"><td class="label" colspan="6">Yield Curve</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/T10Y2Y">10Y − 2Y (bp)</a></td>
<td class="bmc-red">−47</td><td class="bmc-amber">+54</td><td>+27</td><td>+79</td><td class="now">+38</td></tr>

<tr class="section"><td class="label" colspan="6">Sentiment</td></tr>
<tr><td class="label"><a href="https://www.finra.org/investors/insights/margin-statistics">Margin Debt / SPX</a></td>
<td>200</td><td>243</td><td>184</td><td class="bmc-amber">191</td><td class="now">181 <span style="color:#999">(mid)</span></td></tr>

<tr class="section"><td class="label" colspan="6">Corporate Behaviour</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/PNFI">US Capex YoY (%)</a></td>
<td class="bmc-amber">9.7</td><td class="bmc-amber">8.0</td><td>+1.1</td><td class="bmc-amber">7.9</td><td class="bmc-amber now">8.4</td></tr>
<tr><td class="label"><a href="https://www.bain.com/insights/topics/m-and-a-report/">US M&amp;A (last 12m % of Mkt cap)</a></td>
<td class="bmc-red">11.4</td><td class="bmc-red">8.1</td><td>4.4</td><td class="bmc-amber">5.0</td><td class="now">3.7</td></tr>
<tr><td class="label"><a href="https://www.renaissancecapital.com/IPO-Center/Stats">US IPO (last 12m % of DM Mkt cap)</a></td>
<td class="bmc-red">0.7</td><td class="bmc-amber">0.4</td><td>0.2</td><td class="bmc-amber">0.6</td><td class="now">0.4</td></tr>

<tr class="section"><td class="label" colspan="6">Profitability <span style="font-weight:normal;font-style:italic;color:#888">(EPS-from-peak row removed v10 — <a href="https://www.multpl.com/s-p-500-earnings">multpl earnings page</a> is 8mo stale; CAPE row above already captures the cycle-peak signal.)</span></td></tr>

<tr class="section"><td class="label" colspan="6">Balance sheets / credit markets</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/BAA10Y">Moody's BAA − 10Y (pp)</a></td>
<td class="bmc-amber">2.30</td><td class="bmc-amber">1.99</td><td class="bmc-amber">2.38</td><td class="bmc-amber">1.85</td><td class="bmc-red now">1.54</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/BAMLH0A0HYM2">HY OAS (%)</a> <span style="font-style:italic;color:#888;font-size:.85em">(ICE BofA 2023+; Citi pre-2023)</span></td>
<td>6.00</td><td>6.00</td><td class="bmc-amber">4.80</td><td>3.37</td><td class="bmc-red now">2.74</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/BAMLC0A0CM">IG OAS (%)</a> <span style="font-style:italic;color:#888;font-size:.85em">(same caveat)</span></td>
<td>1.75</td><td>1.75</td><td class="bmc-amber">1.21</td><td>0.90</td><td class="bmc-red now">0.74</td></tr>
<tr><td class="label"><a href="https://fred.stlouisfed.org/series/BAMLH0A3HYC">CCC OAS</a> − HY spread (pp) <span style="font-style:italic;color:#888;font-size:.85em">(derived; ICE BofA 2023+)</span></td>
<td class="bmc-na">n/a</td><td class="bmc-na">n/a</td><td class="bmc-na">n/a</td><td class="bmc-na">n/a</td><td class="bmc-green now">6.72 <span style="color:#1a4d1a;font-weight:normal;font-size:.85em">(10y max — contra)</span></td></tr>
<tr><td class="label"><a href="https://finance.yahoo.com/quote/HYG/">HYG</a> / <a href="https://finance.yahoo.com/quote/LQD/">LQD</a> ratio <span style="font-style:italic;color:#888;font-size:.85em">(HYG launched Apr 2007)</span></td>
<td class="bmc-na">n/a</td><td>0.635</td><td>0.582</td><td>0.611</td><td class="bmc-red now">0.734 <span style="color:#5a0000;font-weight:normal;font-size:.85em">(19y high)</span></td></tr>

<tr class="section"><td class="label" colspan="6">Equity / Rate Vol</td></tr>
<tr><td class="label"><a href="https://finance.yahoo.com/quote/%5EVIX/">VIX</a></td>
<td>24.1</td><td>18.5</td><td class="bmc-stress">40.1</td><td>17.2</td><td class="now">21.5</td></tr>
<tr><td class="label"><a href="https://finance.yahoo.com/quote/%5ESKEW/">SKEW</a></td>
<td>113</td><td>117</td><td>131</td><td>154</td><td class="bmc-green now">152 <span style="color:#1a4d1a;font-weight:normal;font-size:.85em">(contra)</span></td></tr>
<tr><td class="label"><a href="https://finance.yahoo.com/quote/%5EMOVE/">MOVE</a></td>
<td class="bmc-na">n/a</td><td>90</td><td>110</td><td>77</td><td class="now">75</td></tr>
<tr><td class="label"><a href="https://finance.yahoo.com/quote/%5EVIX9D/">VIX9D</a> / <a href="https://finance.yahoo.com/quote/%5EVIX3M/">VIX3M</a> <span style="font-style:italic;color:#888;font-size:.85em">(VIX9D launched 2011)</span></td>
<td class="bmc-na">n/a</td><td class="bmc-na">n/a</td><td class="bmc-stress">1.77 <span style="font-weight:normal;font-size:.85em">(COVID panic)</span></td><td>0.61</td><td class="bmc-green now">1.10 <span style="color:#1a4d1a;font-weight:normal;font-size:.85em">backwardated (contra)</span></td></tr>

<tr class="section"><td class="label"># Flags (this dashboard / 19)</td>
<td class="bmc-na">n/a*</td><td class="bmc-na">n/a*</td><td class="bmc-na">n/a*</td><td class="bmc-na">n/a*</td><td class="now"><strong>7.5</strong></td></tr>
<tr class="section"><td class="label"># Flags (Citi BMC / 18)</td>
<td>17.5</td><td>13.0</td><td>5.5</td><td>8.5</td><td class="now">10.0 Global, 11.5 US</td></tr>
</tbody></table>

*Pre-2007 totals incomplete — VVIX, SKEW, MOVE histories shorter than the dashboard's lookback.

🟢 = contra-signal (low complacency rating despite high absolute value — "already-bid hedges" or "credit-tier divergence")

**Today's calibration**: CAPE is within 1 point of the March 2000 dot-com peak. Dividend yield is *below* the dot-com low. Moody's BAA−10Y is the tightest of any reference date. But: yield curve is positive, SKEW is contra (top-decile crash demand), VIX slope backwardated, CCC widening relative to HY (10y max). **No clean historical precedent** — past bears started with one or the other, not both.

## Under the Hood

Each chart is **interactive** — use the 1Y / YTD / 5Y / 10Y / ALL buttons (top-left) or the bottom range-slider to adjust the time span. Bear-market shading marked in grey. Static PNG fallback links provided in each caption.

<iframe src="../charts/market_complacency_2026-06-07_credit_baa.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 3. Long-history credit — Moody's BAA−10Y, 1986+. Sources: [FRED BAA10Y](https://fred.stlouisfed.org/series/BAA10Y) · [TradingEconomics HY OAS long-history](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-high-yield-option-adjusted-spread-fed-data.html). [Static PNG](../charts/market_complacency_2026-06-07_hy_oas.png) (with HY OAS reference points annotated).*

<iframe src="../charts/market_complacency_2026-06-07_ig_credit.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 4. IG credit tiers — Moody's AAA−10Y (1983+) vs BAA−10Y (1986+) with BAA−AAA dispersion on the right axis. Sources: [FRED AAA10Y](https://fred.stlouisfed.org/series/AAA10Y) · [FRED BAA10Y](https://fred.stlouisfed.org/series/BAA10Y). [Static PNG](../charts/market_complacency_2026-06-07_ig_ccc.png).*

<iframe src="../charts/market_complacency_2026-06-07_cape.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 5. Shiller CAPE, 1871+. Source: [multpl.com Shiller PE](https://www.multpl.com/shiller-pe) · derived from [Robert Shiller's Yale dataset](http://www.econ.yale.edu/~shiller/data.htm). [Static PNG](../charts/market_complacency_2026-06-07_cape.png).*

<iframe src="../charts/market_complacency_2026-06-07_erp.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 6. Equity Risk Premium = S&P 500 E/P − 10Y Treasury. Sources: [multpl S&P 500 Earnings Yield](https://www.multpl.com/s-p-500-earnings-yield) · [FRED DGS10](https://fred.stlouisfed.org/series/DGS10). [Static PNG](../charts/market_complacency_2026-06-07_erp.png).*

<iframe src="../charts/market_complacency_2026-06-07_vix_vvix.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 7. VIX (1990+) & VVIX (2007+). Sources: [Yahoo ^VIX](https://finance.yahoo.com/quote/%5EVIX/) · [Yahoo ^VVIX](https://finance.yahoo.com/quote/%5EVVIX/) · [CBOE VIX page](https://www.cboe.com/tradable_products/vix/). [Static PNG](../charts/market_complacency_2026-06-07_vix_vvix.png).*

<iframe src="../charts/market_complacency_2026-06-07_vix_slope.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 8. VIX Term Slope — VIX9D÷VIX3M (canonical, 2011+) + VIX÷VIX3M long-history proxy (2006+). Sources: [Yahoo ^VIX9D](https://finance.yahoo.com/quote/%5EVIX9D/) · [Yahoo ^VIX3M](https://finance.yahoo.com/quote/%5EVIX3M/) · [Yahoo ^VIX](https://finance.yahoo.com/quote/%5EVIX/). Ratio < 1 = contango (calm); ≥ 1 = backwardation (front-month fear). [Static PNG](../charts/market_complacency_2026-06-07_vix_slope.png).*

<iframe src="../charts/market_complacency_2026-06-07_move.html" width="100%" height="500" style="border:0;border-radius:6px;"></iframe>

*Figure 9. MOVE Index (rate vol), 2002+ — Yahoo's earliest free data. Source: [Yahoo ^MOVE](https://finance.yahoo.com/quote/%5EMOVE/). MOVE was created in 1988 by Merrill Lynch but free pre-2002 history is not available. [Static PNG](../charts/market_complacency_2026-06-07_move.png).*

![Figure 10: Per-Indicator Complacency Bars](../charts/market_complacency_2026-06-07_indicators_bar.png)
*Source: per-indicator 10-year rolling complacency percentile from `scripts/build_dashboard.py`. Bar chart (no time axis — interactive version not applicable).*

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
