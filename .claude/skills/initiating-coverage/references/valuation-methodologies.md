# Valuation Methodologies for Equity Research

This reference document provides comprehensive guidance on the three primary valuation methodologies used in equity research: Discounted Cash Flow (DCF), Trading Comparables, and Precedent Transactions.

## Table of Contents

1. [Discounted Cash Flow (DCF) Analysis](#discounted-cash-flow-dcf-analysis)
2. [Trading Comparables Analysis](#trading-comparables-analysis)
3. [Precedent Transactions Analysis](#precedent-transactions-analysis)
4. [Forward Target Multiple on Out-Year EPS/EBITDA](#forward-target-multiple-on-out-year-epsebitda) — **primary method for most initiations**
5. [Sum-of-the-Parts (SOTP)](#sum-of-the-parts-sotp)
6. [NAV with Discount (Holding Companies)](#nav-with-discount-holding-companies)
7. [rNPV / PTS-Weighted Valuation (Clinical-Stage Biotech)](#rnpv--pts-weighted-valuation-clinical-stage-biotech)
8. [Valuation Reconciliation](#valuation-reconciliation)

> **Method selection note.** DCF and trading comps (Sections 1-2) are the workhorses, but a study of 24 real sell-side initiations shows ~80% headline the price target on a **forward target multiple on an out-year** (Section 4), with DCF as a cross-check — not a 50%-weighted blend. Biotech uses rNPV (Section 7); two-curve businesses use SOTP (Section 5); holdcos use NAV-discount (Section 6). Choose the primary method by archetype (see the table in `task3-valuation.md` Step 1b) rather than defaulting to a fixed weighting.

---

## Discounted Cash Flow (DCF) Analysis

### Overview

DCF analysis values a company based on the present value of its projected future cash flows. This is considered the most theoretically sound valuation method as it's based on fundamental value creation.

### Step-by-Step DCF Process

#### 1. Historical Financial Analysis
- Collect 3-5 years of historical financials
- Calculate historical FCF = EBIT(1-Tax Rate) + D&A - CapEx - Change in NWC
- Analyze historical growth rates and margins
- Identify trends and cyclicality

#### 2. Build Revenue Projections (5-10 years)
**Approaches:**
- **Top-down**: Start with market size (TAM) → Market share → Revenue
- **Bottom-up**: Units sold × Price per unit
- **Hybrid**: Combine multiple drivers

**Key Considerations:**
- Management guidance and historical growth
- Industry growth rates and market trends
- Competitive dynamics and market share evolution
- Product pipeline and new market opportunities
- Macroeconomic factors

#### 3. Project Operating Expenses
- **COGS**: As % of revenue (analyze historical margins)
- **SG&A**: Often semi-fixed; model as % of revenue with scale effects
- **R&D**: Critical for tech/pharma; model as % of revenue
- **D&A**: Based on CapEx assumptions

**Calculate EBIT** = Revenue - COGS - Operating Expenses

#### 4. Calculate Unlevered Free Cash Flow
```
EBIT
× (1 - Tax Rate)
= NOPAT (Net Operating Profit After Tax)
+ Depreciation & Amortization
- Capital Expenditures
- Increase in Net Working Capital
= Unlevered Free Cash Flow (UFCF)
```

**CapEx Assumptions:**
- Maintenance CapEx: Required to maintain current operations (typically 2-4% of revenue)
- Growth CapEx: Required for expansion
- Consider industry benchmarks and company guidance

**Net Working Capital:**
- NWC = (Accounts Receivable + Inventory) - Accounts Payable
- Model as % of revenue or days (DSO, DIO, DPO)
- An increase in NWC is a use of cash

#### 5. Determine Terminal Value

**Method A: Perpetuity Growth Method**
```
Terminal Value = FCF(final year) × (1 + g) / (WACC - g)
```
- g = perpetual growth rate (typically 2-3%, not exceeding GDP growth)
- Use when company has reached stable, mature growth

**Method B: Exit Multiple Method**
```
Terminal Value = EBITDA(final year) × Exit Multiple
```
- Exit multiple based on current trading comps
- More appropriate for cyclical businesses

#### 6. Calculate Weighted Average Cost of Capital (WACC)

```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))
```

**Cost of Equity (using CAPM):**
```
Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium
```
- Risk-Free Rate: 10-year Treasury yield
- Beta: Regression of stock returns vs. market (or use comparable beta)
- Equity Risk Premium: Historical average ~5-6%

**Cost of Debt:**
```
Cost of Debt = Risk-Free Rate + Credit Spread
```
- Use company's current borrowing rate or implied from bonds
- Adjust for credit rating if no bonds outstanding

**Capital Structure:**
- E/V = Market value of equity / Total value
- D/V = Market value of debt / Total value
- Use target capital structure, not current (if significantly different)

#### 7. Discount Cash Flows to Present Value

```
PV = Σ [FCFt / (1 + WACC)^t] + [Terminal Value / (1 + WACC)^n]
```

#### 8. Calculate Enterprise Value and Equity Value

```
Enterprise Value = PV of Projected FCF + PV of Terminal Value
Less: Net Debt (Total Debt - Cash)
Plus: Non-operating Assets
Less: Minority Interest
Less: Preferred Stock
= Equity Value

Price Per Share = Equity Value / Diluted Shares Outstanding
```

### DCF Sensitivity Analysis

Always perform sensitivity analysis on key variables:

1. **Two-way sensitivity table**: WACC vs. Terminal Growth Rate
2. **Revenue growth scenarios**: Base / Bull / Bear cases
3. **Margin assumptions**: Operating leverage scenarios
4. **Terminal multiple sensitivity**: If using exit multiple method

**Example Sensitivity Table:**
```
           Terminal Growth Rate
WACC      2.0%    2.5%    3.0%
8.0%      $45     $48     $52
9.0%      $40     $43     $46
10.0%     $36     $39     $41
```

### Common DCF Pitfalls to Avoid

1. **Double-counting growth**: Don't project high growth without corresponding investment (CapEx, NWC)
2. **Unrealistic terminal growth**: Should not exceed long-term GDP growth
3. **Ignoring cyclicality**: Normalize earnings for cyclical businesses
4. **Wrong cash flow definition**: Use unlevered FCF, not net income
5. **Inconsistent assumptions**: Match discount rate to cash flows (unlevered FCF → WACC)

---

## Trading Comparables Analysis

### Overview

Trading comps values a company based on how similar companies are valued in the public markets. This reflects current market sentiment and relative valuation.

### Step-by-Step Comps Process

#### 1. Select Comparable Companies

**Selection Criteria:**
- Same industry/sector (primary criterion)
- Similar business model and revenue streams
- Comparable size (market cap, revenue)
- Similar growth profile and margins
- Similar end markets and geographies

**Typical Universe:**
- Start with 8-15 companies
- Remove companies with unique circumstances
- Final set of 5-10 companies

#### 2. Gather Financial Information

**Required Data:**
- Current stock price and shares outstanding
- Latest fiscal year financial statements
- Next-year (NTM) estimates from consensus
- Historical growth rates

**Calculate Market Metrics:**
- Market Cap = Share Price × Shares Outstanding
- Enterprise Value = Market Cap + Debt + Minority Interest + Preferred - Cash
- Net Debt = Total Debt - Cash & Equivalents

#### 3. Calculate Valuation Multiples

**Enterprise Value Multiples:**
- **EV/Revenue**: Good for early-stage/high-growth companies
- **EV/EBITDA**: Most common; good for capital-intensive businesses
- **EV/EBIT**: Useful when D&A varies significantly

**Equity Value Multiples:**
- **P/E (Price/Earnings)**: Most widely used
- **P/B (Price/Book)**: Good for financial institutions
- **P/S (Price/Sales)**: For unprofitable companies

**Calculate for:**
- Last Twelve Months (LTM) - historical
- Next Twelve Months (NTM) - forward-looking (preferred)

#### 4. Analyze and Select Multiples

**Create Comparable Company Table:**

| Company | Market Cap | EV/Revenue | EV/EBITDA | EV/EBIT | P/E (NTM) | Revenue Growth | EBITDA Margin |
|---------|-----------|------------|-----------|---------|-----------|----------------|---------------|
| Comp A  | $10B      | 3.5x       | 12.0x     | 18.0x   | 22.0x     | 15%            | 28%           |
| Comp B  | $8B       | 3.0x       | 10.5x     | 16.0x   | 19.0x     | 12%            | 27%           |
| ...     | ...       | ...        | ...       | ...     | ...       | ...            | ...           |
| Median  | -         | **3.2x**   | **11.0x** | **17.0x** | **20.5x** | 13%            | 27.5%         |

**Adjustments:**
- Remove outliers (typically >2 standard deviations)
- Consider using median instead of mean (less affected by outliers)
- Weight multiples if some comps are more comparable
- Adjust for differences in growth, margins, risk

#### 5. Apply Multiples to Target Company

**Example Calculation:**
```
Target Company NTM EBITDA = $500M
Selected EV/EBITDA Multiple = 11.0x
Implied Enterprise Value = $500M × 11.0x = $5,500M

Less: Net Debt = $1,000M
Equity Value = $4,500M

Shares Outstanding = 100M
Implied Price Per Share = $45.00
```

#### 6. Select Appropriate Multiple

**Choose based on:**
- **EV/Revenue**: High-growth, unprofitable companies (tech, biotech pre-profit)
- **EV/EBITDA**: Most common; capital-intensive industries (manufacturing, telecom)
- **P/E**: Profitable companies with stable cap structure (consumer, retail)
- **Sector-specific**: P/B for banks, EV/Production for oil & gas, EV/Subscriber for media

### Premium/Discount Analysis

Apply premiums or discounts based on:
- **Growth premium**: Higher growth → higher multiple
- **Profitability**: Higher margins → higher multiple
- **Size**: Larger companies typically trade at premium (liquidity)
- **Market position**: Market leaders → premium
- **Geographic**: Developed vs. emerging markets

---

## Precedent Transactions Analysis

### Overview

Precedent transactions values a company based on prices paid for similar companies in M&A transactions. This reflects control premiums and strategic value.

### Step-by-Step Process

#### 1. Identify Relevant Transactions

**Selection Criteria:**
- Same or similar industry
- Similar size (within 0.5x to 2x target's size)
- Similar business characteristics
- Recent transactions (last 3-5 years preferred)
- Announced and closed deals (avoid withdrawn deals)

**Typical Universe:**
- 5-10 transactions minimum
- Focus on recent deals (weight more recent higher)

#### 2. Gather Transaction Details

**Required Information:**
- Transaction date (announcement and close)
- Acquisition price and structure (cash, stock, mixed)
- Target's financials at time of transaction
- Strategic rationale and synergies
- Control premium paid

**Sources:**
- SEC filings (S-4, 8-K, proxy statements)
- Press releases and investor presentations
- M&A databases (CapIQ, FactSet, Bloomberg)

#### 3. Calculate Transaction Multiples

**Same multiples as trading comps, but based on transaction value:**

```
Transaction Value = Equity Purchase Price + Assumed Debt - Cash Acquired

EV/Revenue (LTM) = Transaction Value / Target's LTM Revenue
EV/EBITDA (LTM) = Transaction Value / Target's LTM EBITDA
EV/EBIT (LTM) = Transaction Value / Target's LTM EBIT
```

**Calculate Control Premium:**
```
Control Premium = (Offer Price - Unaffected Price) / Unaffected Price
```
- Unaffected Price = Target's stock price 1-2 days before announcement
- Typical range: 20-40%

#### 4. Analyze Precedent Transactions

**Create Precedent Transactions Table:**

| Date | Target | Acquirer | Deal Value | EV/Revenue | EV/EBITDA | Premium | Rationale |
|------|--------|----------|------------|------------|-----------|---------|-----------|
| Q1'24 | CompX | BuyerA | $5.0B | 4.0x | 14.0x | 35% | Market consolidation |
| Q3'23 | CompY | BuyerB | $3.5B | 3.5x | 12.5x | 28% | Strategic fit |
| Median | - | - | - | **3.8x** | **13.0x** | **31%** | - |

#### 5. Apply to Target Company

**Important Considerations:**
- Precedent multiples typically higher than trading comps (include control premium)
- Adjust for differences in transaction rationale
- Consider market conditions at time of transactions vs. current
- Weight recent transactions more heavily

**Example Calculation:**
```
Target Company LTM EBITDA = $450M
Selected EV/EBITDA Multiple = 13.0x (precedent)
vs Trading Comps Multiple = 11.0x

Implied EV (Precedent) = $450M × 13.0x = $5,850M
Implied EV (Trading) = $450M × 11.0x = $4,950M

Implied Control Premium = $5,850M / $4,950M - 1 = 18%
```

### Adjustments to Transaction Multiples

**Consider adjusting for:**
- **Market conditions**: Bull vs. bear market (M&A activity levels)
- **Deal structure**: Strategic vs. financial buyer
- **Synergies**: Transactions with high synergies command premiums
- **Competitive dynamics**: Single vs. multiple bidders
- **Time value**: Older transactions less relevant

---

## Forward Target Multiple on Out-Year EPS/EBITDA

### Overview

The most common way the sell-side sets an initiation price target: apply a chosen multiple to an **out-year (FY+2 or FY+3)** EPS or EBITDA and discount back to a 12-month target date. Examples from the library — JPM Yingliu 40x 2028E EPS; Nomura Victory Giant 27x 2027E; Citi Hon Precision 36x avg-2027/28E; GS Co-Tech 22x 2028E; UBS Tao 20x 2027E. This differs from trading comps (Section 2), which apply an NTM peer-median multiple; here the analyst applies their *own* target multiple to their *own* out-year estimate, and the justification of that multiple is the analytical core.

### Step-by-Step

1. **Pick the out-year and metric.** FY+2 or FY+3 EPS for earnings-driven equities; out-year EBITDA for capital-intensive names. Use the analyst's model estimate, not consensus.
2. **Choose the target multiple, then justify it THREE ways (mandatory):**
   - **(a) The stock's own historical valuation band** — "+1 SD above the 10-yr up-cycle mean" (GS Co-Tech), "within the historical 10-31x range" (UBS Accton), "= the A-share's own historical median" (Nomura Victory Giant). Cite the price-history data source.
   - **(b) At least one named global peer's current multiple** — "vs Howmet 37x" (JPM Yingliu). Cite the peer's filing or a dated data-provider page, never a homepage.
   - **(c) The EPS/earnings-CAGR-vs-peers gap** that earns the premium/discount — "55% EPS CAGR > peers' 23%" (JPM Yingliu).
3. **Compute and date the PT.**
   ```
   PT (out-year) = target multiple × out-year EPS
   12-month PT   = PT discounted to the target date (e.g. Dec-2027)
   Implied move  = 12-month PT / current price − 1   (state vs a dated close)
   ```
4. **Cross-check against the DCF (Section 1).** If the DCF and the forward-multiple PT diverge >20%, reconcile in prose — usually the multiple wins for a growth equity and the DCF is the sanity floor.

### Pitfalls

- Applying the multiple to NTM instead of the out-year (defeats the point — the thesis is about the out-year earnings power).
- Quoting a peer-median multiple with no historical-band or CAGR anchor (Section 2's job, not this method's).
- Citing the analyst's own model as the source for the multiple — the multiple is an analyst judgement defended by (a)/(b)/(c), never "(Source: our model)".

---

## Sum-of-the-Parts (SOTP)

### Overview

For a business with **two distinct growth curves** valued on different bases — a mature cash-generating segment plus an emerging high-TAM segment. Exemplar: DB Huayan (Buy, TP HK$28.2) = mature cobot segment at **12x 2026 P/S** (at a discount) **+** humanoid-component segment via **DCF on a 2030 1m-unit TAM**.

### Step-by-Step

1. **Split the business into segments** that the market would value differently (mature vs. emerging; cash-flow vs. optionality).
2. **Value each segment on its own appropriate basis** — mature segment on a forward multiple (P/S, P/E, EV/EBITDA) often at a discount; emerging segment on an out-year-TAM DCF or an option-value framing.
3. **Sum the segment equity values**, subtract net debt and any holdco costs, divide by shares for the PT.
4. **Show the bridge** (segment A value + segment B value − net debt = equity value) so the reader sees where the PT comes from — same transparency rule as the derived-number citation standard.

### Pitfalls

- Double-counting overhead/corporate costs across segments.
- Valuing the emerging segment on revenue it doesn't yet have without an explicit TAM × share × ASP build and a named sizing source (Frost & Sullivan / Yole).

---

## NAV with Discount (Holding Companies)

### Overview

For holding companies and names with heavy cross-holdings, where the sum of stakes' market values overstates what minority holders can realize. Exemplar: Bernstein SoftBank — **NAV minus 25%**.

### Step-by-Step

1. **Mark each holding to market** (listed stakes at market price; unlisted at last round / comp-implied value).
2. **Sum to gross NAV**, subtract net debt at the holdco → net NAV per share.
3. **Apply a discount** reflecting governance, liquidity, tax-on-disposal, and the holdco's track record of monetization — state the discount explicitly (e.g. −25%) and justify it against the stock's own historical NAV-discount range and peer holdcos.
4. **PT = net NAV per share × (1 − discount).**

### Pitfalls

- Using book value instead of market value for listed stakes.
- Applying a discount with no anchor — justify it against the name's own historical discount band, exactly like the target-multiple anchor rule.

---

## rNPV / PTS-Weighted Valuation (Clinical-Stage Biotech)

### Overview

For pre-revenue / clinical-stage biotech, value each asset's risk-adjusted NPV by weighting peak-sales cash flows by the **probability of technical and regulatory success (PTS)** at its current phase, then sum across the pipeline. Often blended with an M&A/takeout value. Exemplars: GS Hemab (**70% DCF / 30% M&A, 16% WACC**); Bernstein US SMID Biotech PTS model (which also carries an Underperform short).

### Step-by-Step

1. **For each pipeline asset:** estimate peak sales, ramp, patent life, and the phase-appropriate PTS (e.g. Ph1→approval ~10%, Ph2 ~15-25%, Ph3 ~50-65%, filed ~85% — use published industry success rates and cite them).
2. **Build the unadjusted NPV** of each asset's cash flows at a high biotech WACC (14-18%).
3. **Multiply by PTS** → risk-adjusted NPV (rNPV) per asset.
4. **Sum rNPVs + net cash − burn**, then optionally **blend with an M&A value** (e.g. 70% rNPV / 30% takeout) to reflect acquisition optionality.
5. **Dated catalysts are the spine** — each Ph2/Ph3 readout and filing is a dated 12-month catalyst (GS Hemab "sutacimig GT Ph3 start H2-2026; FVIID Ph2 readout late-2026/early-2027").

### Pitfalls

- Using a PTS that isn't phase-appropriate or isn't sourced to a published success-rate study.
- Ignoring cash runway — a name that runs out of cash before its readout needs a financing/dilution haircut.

---

## Valuation Reconciliation

### Creating a Valuation Bridge

Present all three methods in a single framework:

**Example Valuation Summary:**

| Method | Enterprise Value | Equity Value | Price/Share | Weight | Implied Value |
|--------|------------------|--------------|-------------|--------|---------------|
| DCF Analysis | $5,200M | $4,200M | $42.00 | 50% | $21.00 |
| Trading Comps | $5,500M | $4,500M | $45.00 | 30% | $13.50 |
| Precedent Trans. | $5,850M | $4,850M | $48.50 | 20% | $9.70 |
| **Weighted Avg** | - | - | **$44.20** | - | **$44.20** |

### Weighting the Methods

**Typical Weighting:**
- **DCF**: 40-60% (fundamental value, but assumes accuracy of projections)
- **Trading Comps**: 25-40% (reflects current market sentiment)
- **Precedent Trans.**: 15-25% (less relevant unless M&A likely)

**Adjust weights based on:**
- **Confidence in forecasts**: Higher confidence → higher DCF weight
- **Market conditions**: Bull/bear market affects comps reliability
- **M&A likelihood**: Higher if company in play or industry consolidating
- **Company maturity**: Mature companies → higher weight on comps; growth → higher DCF weight

### Valuation Range

Always present a valuation range, not a point estimate:

**Approach:**
- **Base Case**: Most likely scenario
- **Bull Case**: Optimistic assumptions (revenue growth, margins)
- **Bear Case**: Conservative assumptions

**Example:**
```
Bear Case: $38 - $40
Base Case: $42 - $46
Bull Case: $48 - $52

Recommendation: BUY with target price of $45 (midpoint of base case)
```

### Sanity Checks

**Cross-check valuation with:**
1. **Historical multiples**: Is current valuation in line with history?
2. **Peer comparison**: Justified premium/discount vs. peers?
3. **Implied growth**: What growth is market pricing in?
4. **Implied returns**: IRR from current price to target price
5. **Market cap analysis**: Does total market cap make sense?

---

## Conclusion

Using all three valuation methods provides a robust framework for determining fair value:

- **DCF** provides intrinsic value based on fundamentals
- **Trading Comps** reflects current market valuation
- **Precedent Transactions** indicates M&A value and control premium

The key is to understand the assumptions driving each method and to present a well-reasoned valuation range that considers multiple scenarios and methodologies.
