# Figure 1 — Kickstart-style 9-indicator calibration table

Drop-in HTML template for the Figure 1 calibration table in
`reports/market-status/market_status_<DATE>.md`. Mirrors GS Exhibit 3 layout:
Dot-Com Bubble / 2021 / Current columns; rows grouped by share-prices /
trading-activity / investor-sentiment / corporate-sentiment.

**Cell-fill classes** (defined in the `<style>` block at the top of the
report):

| Class | Background | Foreground | When to apply |
|---|---|---|---|
| `.ms-red`   | `#f4a8a8` | `#5a0000` | Exuberance percentile ≥ 80 (top quintile vs ~30y history) |
| `.ms-amber` | `#ffd17a` | `#5a3300` | Exuberance percentile 60–80 |
| `.ms-green` | `#b6e3b6` | `#1a4d1a` | Exuberance percentile ≤ 30 (contra-signal — bearish positioning, not exuberant) |
| `.ms-now`   | white     | inherit   | Apply `border-left: 2px solid #888` — column separator on the Current column |

Plain (no class) — anything 30–60.

## Template

```html
<style>
.ms-table { border-collapse: collapse; width: 100%; font-size: 0.92em; margin: 0.5em 0 1em 0; }
.ms-table th, .ms-table td { border: 1px solid #ddd; padding: 6px 10px; text-align: center; }
.ms-table th { background: #f0f0f0; font-weight: 600; }
.ms-table td.indicator { text-align: left; }
.ms-table td.category { text-align: left; background: #f5f5f5; font-weight: 600; }
.ms-red   { background: #f4a8a8; color: #5a0000; font-weight: 600; }
.ms-amber { background: #ffd17a; color: #5a3300; font-weight: 600; }
.ms-green { background: #b6e3b6; color: #1a4d1a; font-weight: 600; }
.ms-now   { border-left: 2px solid #888 !important; }
</style>

<table class="ms-table">
  <thead>
    <tr>
      <th>Indicator (rank vs history since 1995)</th>
      <th>Dot-Com (Mar 2000)</th>
      <th>Post-COVID (Dec 2021)</th>
      <th class="ms-now">Current</th>
    </tr>
  </thead>
  <tbody>
    <!-- Share prices -->
    <tr><td colspan="4" class="category">Share prices</td></tr>
    <tr>
      <td class="indicator"><a href="https://www.ishares.com/us/products/251614/ishares-msci-usa-momentum-factor-etf">Momentum factor 3M return (MTUM − SPY proxy)</a></td>
      <td class="ms-red">100</td>
      <td class="ms-amber">76</td>
      <td class="ms-now ms-red">{{ momentum_3m.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.bespokepremium.com/think-big-blog/">S&P 500 52-week market breadth</a> <em>(inverted — narrow = exuberant)</em></td>
      <td class="ms-red">100</td>
      <td class="ms-red">95</td>
      <td class="ms-now ms-red">{{ breadth_52w.exuberance_pct }}</td>
    </tr>

    <!-- Trading activity -->
    <tr><td colspan="4" class="category">Trading activity</td></tr>
    <tr>
      <td class="indicator">GS Speculative Trading Indicator</td>
      <td class="ms-red">100</td>
      <td class="ms-red">99</td>
      <td class="ms-now ms-red">{{ spec_trade.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.cboe.com/us/options/market_statistics/">CBOE Equity Put/Call ratio (21-day MA)</a> <em>(inverted)</em></td>
      <td class="ms-red">100</td>
      <td class="ms-red">97</td>
      <td class="ms-now ms-green">{{ put_call.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.finra.org/finra-data/short-sale-volume-data">Short interest, median S&P 500 stock</a> <em>(inverted)</em></td>
      <td class="ms-red">96</td>
      <td class="ms-red">89</td>
      <td class="ms-now ms-green">{{ short_interest.exuberance_pct }}</td>
    </tr>

    <!-- Investor sentiment -->
    <tr><td colspan="4" class="category">Investor sentiment</td></tr>
    <tr>
      <td class="indicator"><a href="https://som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices">Yale US Stock Market Confidence (Buy-on-Dips − Valuation)</a></td>
      <td class="ms-red">100</td>
      <td class="ms-red">96</td>
      <td class="ms-now ms-red">{{ yale_confidence.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.aaii.com/sentimentsurvey">AAII Bull-Bear spread (3-month MA)</a></td>
      <td class="ms-red">99</td>
      <td class="ms-red">92</td>
      <td class="ms-now ms-green">{{ aaii_bullbear.exuberance_pct }}</td>
    </tr>

    <!-- Corporate sentiment -->
    <!-- GS nuance: split COUNT vs PROCEEDS (IPO proceeds can hit records while
         count is near average) and GROSS vs NET-of-buyback issuance (net stays
         low when buybacks exceed new supply). The count/value divergence is
         what GS uses to say supply pressure is still contained — encode both. -->
    <tr><td colspan="4" class="category">Corporate sentiment</td></tr>
    <tr>
      <td class="indicator"><a href="https://www.renaissancecapital.com/IPO-Center/Stats">Number of US IPOs (YTD annualised, > $25M) — <em>count</em></a></td>
      <td class="ms-red">100</td>
      <td class="ms-red">87</td>
      <td class="ms-now">{{ ipo_count.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.renaissancecapital.com/IPO-Center/Stats">US IPO proceeds (YTD annualised, $bn) — <em>value</em></a></td>
      <td class="ms-red">100</td>
      <td class="ms-red">90</td>
      <td class="ms-now">{{ ipo_proceeds.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.sifma.org/resources/research/us-equity-issuance-and-trading-volumes/">Gross US equity issuance (12m rolling, % of market cap)</a></td>
      <td class="ms-red">100</td>
      <td class="ms-red">99</td>
      <td class="ms-now ms-amber">{{ gross_issuance.exuberance_pct }}</td>
    </tr>
    <tr>
      <td class="indicator"><a href="https://www.sifma.org/resources/research/us-equity-issuance-and-trading-volumes/">Net US equity issuance (gross − buybacks, 12m rolling, % of market cap)</a></td>
      <td class="ms-red">100</td>
      <td class="ms-red">99</td>
      <td class="ms-now ms-amber">{{ net_issuance.exuberance_pct }}</td>
    </tr>

    <!-- Composite -->
    <tr>
      <td class="indicator"><strong>Median (composite)</strong></td>
      <td><strong>100</strong></td>
      <td><strong>95</strong></td>
      <td class="ms-now"><strong>{{ composite_score }}</strong></td>
    </tr>
  </tbody>
</table>
```

After filling in values, swap the `ms-red` / `ms-amber` / `ms-green` /
empty classes on the Current column based on the actual computed percentile
(see thresholds above). The pre-set classes in the template above are a
guide based on the 2026-06-07 reference run — re-evaluate each run.

## Analog calibration sources

The Dot-Com (100th) / Post-COVID (95th) anchor columns this Figure mirrors
trace to two named sell-side scorecards — cite them rather than the
hardcoded reference-run values:

- **GS US Weekly Kickstart, "Evaluating exuberance"** — the 4-category /
  9-indicator scorecard with a *median 100th percentile vs history in 2000
  and 95th in 2021*; today ranks ~86th since 1995. This Figure reproduces
  GS Exhibit 3 directly.
- **Citi Global Equity Strategy, "Bear Market Checklist"** — an 18-factor
  amber/red scorecard calibrated vs the 2000 and 2007 peaks, with a
  region split (US vs Europe). Mirror its "what is NOT yet flagged" column
  and its acceleration rule ("once the score breaks its band it tends to
  accelerate") in the report's Verdict.

Anchor the historical columns to this methodology, not to a prior run's
numbers, so each refresh re-derives the calibration from a citable source.

## Verdict-line examples

| Composite | Tier | One-line opener |
|---|---|---|
| 80–100 | Frothy | "**Frothy — exuberance 86 / 100, top decile across 5 of 9 GS indicators**" |
| 60–80  | Stretched | "**Stretched — exuberance 68 / 100; above historical averages but below 2000 / 2021 peaks**" |
| 40–60  | Elevated | "**Elevated — exuberance 52 / 100; signs of optimism on share-price action, no broad froth elsewhere**" |
| 20–40  | Neutral | "**Neutral — exuberance 28 / 100; sentiment surveys close to long-run averages**" |
| 0–20   | Subdued | "**Subdued — exuberance 14 / 100; bearish positioning across 6 of 9 indicators — contrarian-buy regime**" |
