# Task 3: Valuation Analysis - Detailed Workflow

This document provides step-by-step instructions for executing Task 3 (Valuation Analysis) of the initiating-coverage skill.

## Task Overview

**Purpose**: Perform comprehensive valuation using DCF, comparables, and precedent transactions.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Financial model from Task 2
  - Projected income statements
  - Projected cash flows
  - Revenue and EBITDA forecasts
  - DCF inputs (unlevered FCF)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASK 2 IS COMPLETE**

This task requires the financial model from Task 2. Starting without it will result in incomplete work.

**IF TASK 2 IS NOT COMPLETE**: Stop immediately and inform the user that Task 2 (Financial Modeling) must be completed first. Do not attempt to proceed or create placeholder valuations.

**Output**: Valuation Analysis (4-6 pages + Excel tabs)
- DCF analysis with sensitivity tables
- Comparable companies analysis
- Precedent transactions (if applicable)
- Valuation football field
- Price target and recommendation

---

## ⚠️ MANDATORY: Source Citations

The valuation feeds Task 5's report. Every external data point (peer multiples, risk-free rate, ERP, beta, terminal growth, precedent transaction multiples) must carry a source through to the final DOCX. If sources are missing here, Task 5's Sources & References appendix cannot be built.

**Required:**
- Inline citation after every macro/market assumption — risk-free rate, ERP, beta, terminal growth rate, WACC components — naming the data provider and date: e.g. `Risk-free rate of 4.3% ([US 10Y Treasury, FRED, 2026-05-19](https://fred.stlouisfed.org/series/DGS10))`.
- The Excel `Comparable Companies` tab must include a `Source` column per row (e.g. "FactSet 2026-05-19", "10-K FY2024", "Yahoo Finance 2026-05-19").
- The Excel `DCF` assumption table must include a `Source` column per row.
- The markdown ends with a `## Sources` section listing every distinct source with date + URL, organized into Task 5's six categories (SEC Filings / Earnings Materials / Company Materials / Industry & Market Research / News & Trade Publications / Data Providers).

**Unacceptable:** "Source: Company data", "Industry estimates" without naming the firm, untraceable peer multiples with no provider or date.

---

## Input Verification

**BEFORE STARTING - CHECK:**
- [ ] Task 2 complete? (Financial model exists)
- [ ] Model file path/location known?
- [ ] Can access projected financials from model?

**Required from model:**
- [ ] Projected FCF (5 years)
- [ ] Revenue projections
- [ ] EBITDA projections
- [ ] Terminal year metrics
- [ ] Balance sheet data (debt, cash, shares)

**IF VERIFICATION FAILS**: Stop and complete Task 2 (Financial Modeling) before proceeding.

---

## Detailed Methodology Reference

For deep dive on valuation methodologies, formulas, and theory, see:
**[valuation-methodologies.md](valuation-methodologies.md)**

This workflow document focuses on execution steps. Reference the methodology file for:
- DCF theory and formulas
- WACC calculation details
- Terminal value methods
- Comparable companies theory
- Precedent transactions theory

---

## Step-by-Step Valuation Workflow

### Step 1: Extract Data from Financial Model

**From Task 2's financial model, extract:**

1. **Projected Financials (5 years)**
   - Revenue by year (2025E-2029E)
   - EBITDA by year
   - EBIT by year
   - Tax rate
   - D&A by year
   - CapEx by year
   - Change in NWC by year

2. **Unlevered Free Cash Flow**
   ```
   Extract from DCF Inputs tab in financial model:

                   2025E   2026E   2027E   2028E   2029E
   EBIT            $XXX    $XXX    $XXX    $XXX    $XXX
   × (1 - Tax Rate)
   = NOPAT         $XXX    $XXX    $XXX    $XXX    $XXX
   + D&A           $XXX    $XXX    $XXX    $XXX    $XXX
   - CapEx         ($XX)   ($XX)   ($XX)   ($XX)   ($XX)
   - Chg in NWC    ($XX)   ($XX)   ($XX)   ($XX)   ($XX)
   = Unlevered FCF $XXX    $XXX    $XXX    $XXX    $XXX
   ```

3. **Balance Sheet Data (current)**
   - Total debt
   - Cash & equivalents
   - Net debt (Debt - Cash)
   - Diluted shares outstanding

4. **Scenario Data**
   - Bull case revenue CAGR and terminal margin
   - Base case revenue CAGR and terminal margin
   - Bear case revenue CAGR and terminal margin

### Step 1b: Choose the PRIMARY valuation method by archetype

**Before building the DCF, decide which method actually drives the price target.** The legacy DCF-50 / Comps-40 / Precedent-10 weighting is a *reconciliation* default; it is NOT how the sell-side library prices most initiations. A study of 24 real initiations (GS, MS, UBS, JPM, Bernstein, Nomura, Citi, BofA, DB, HSBC) shows ~80% anchor the PT on a **forward target multiple applied to an out-year (FY+2/FY+3) EPS or EBITDA** — not a blended DCF. Pick ONE primary method matched to the archetype and justify the choice in one sentence; keep the others as cross-checks.

| Company archetype | PRIMARY method | Library exemplar |
|---|---|---|
| Profitable growth equity (industrials / semis / hardware / consumer) | **Forward target multiple on FY+2/FY+3 EPS or EBITDA**; DCF as cross-check only | JPM Yingliu 40x 2028E EPS; Nomura Victory Giant 27x 2027E; Citi Hon Precision 36x avg-2027/28E; GS Co-Tech 22x 2028E; UBS Tao 20x 2027E |
| Clinical-stage / pre-revenue biotech | **rNPV (PTS-weighted)** or probability-weighted DCF blended with M&A value | GS Hemab 70% DCF / 30% M&A, 16% WACC; Bernstein US SMID Biotech PTS model |
| Two-distinct-growth-curve business | **SOTP** — mature segment on P/S or P/E, emerging segment on out-year-TAM DCF | DB Huayan: mature cobot 12x 2026 P/S + humanoid-component DCF on 2030 1m-unit TAM |
| Holding company / heavy cross-holdings | **NAV with an explicit discount** | Bernstein SoftBank NAV −25% |
| Long-duration infra / utility / regulated cash flows | **Multi-year DCF** | UBS Zhongfu DCF WACC 7.3%; GS Tinavi 10-yr DCF 9% discount / 3% terminal |

For the deep recipe on each method (forward-target-multiple, SOTP, NAV-discount, rNPV), see **[valuation-methodologies.md](valuation-methodologies.md)**. The DCF workflow below (Step 2) still runs for every name as the intrinsic-value cross-check — but for a profitable growth equity, the *headline* PT comes from Step 5b's forward target multiple, with the DCF reconciled against it rather than weighted 50%.

### Step 2: Build DCF Analysis

#### A. Calculate WACC

**1. Determine Risk-Free Rate**
   - Use 10-year Treasury yield (check current rate)
   - Example: 4.0-4.5% as of late 2024

**2. Determine Cost of Equity (CAPM)**
   ```
   Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

   Inputs:
   - Risk-Free Rate: [Current 10-year Treasury, e.g., 4.2%]
   - Beta: [Company beta from Bloomberg/FactSet or peer average]
   - Equity Risk Premium: 5-6% (historical average)

   Example:
   Cost of Equity = 4.2% + 1.3 × 5.5% = 11.35%
   ```

**3. Determine Cost of Debt**
   ```
   Cost of Debt = Current borrowing rate or implied yield on bonds

   For private companies:
   Cost of Debt = Risk-Free Rate + Credit Spread (based on rating)

   Example:
   Cost of Debt (pre-tax) = 6.5%
   Cost of Debt (after-tax) = 6.5% × (1 - 25% tax rate) = 4.875%
   ```

**4. Determine Capital Structure**
   ```
   Use market values (not book values):

   Market Value of Equity (E) = Share Price × Shares Outstanding
   Market Value of Debt (D) = Total Debt (use book value if bonds not traded)
   Total Value (V) = E + D

   Weight of Equity = E / V
   Weight of Debt = D / V

   Example:
   E = $5,000M (90.9%)
   D = $500M (9.1%)
   V = $5,500M (100%)
   ```

**5. Calculate WACC**
   ```
   WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))

   Example:
   WACC = (90.9% × 11.35%) + (9.1% × 6.5% × (1 - 25%))
   WACC = 10.32% + 0.44% = 10.76%

   Round to: 10.8% for base case
   ```

#### B. Calculate Terminal Value

**Method 1: Perpetuity Growth (Preferred)**
```
Terminal Value = FCF(2029) × (1 + g) / (WACC - g)

Where:
- FCF(2029) = Final year unlevered FCF from model
- g = Perpetual growth rate (typically 2.0-3.0%)
  - Should not exceed long-term GDP growth
  - Use 2.5% as base case

Example:
FCF(2029) = $500M
g = 2.5%
WACC = 10.8%

Terminal Value = $500M × (1.025) / (0.108 - 0.025)
Terminal Value = $512.5M / 0.083 = $6,175M
```

**Method 2: Exit Multiple (Alternative)**
```
Terminal Value = EBITDA(2029) × Exit Multiple

Where:
- Exit Multiple = Current peer trading median (e.g., 12-15x EBITDA)

Example:
EBITDA(2029) = $800M
Exit Multiple = 13x

Terminal Value = $800M × 13x = $10,400M
```

**Choose one method or average both.**

#### C. Discount Cash Flows to Present Value

```
PV of Projected FCF = Σ [FCFt / (1 + WACC)^t] for t = 1 to 5

Example:
Year    FCF      Discount    PV of FCF
        ($M)     Factor      ($M)
2025    $250     1/(1.108)^1 = 0.9026    $226
2026    $320     1/(1.108)^2 = 0.8147    $261
2027    $390     1/(1.108)^3 = 0.7353    $287
2028    $450     1/(1.108)^4 = 0.6636    $299
2029    $500     1/(1.108)^5 = 0.5988    $299
                              Total PV:  $1,372M

PV of Terminal Value = Terminal Value / (1 + WACC)^5
PV of Terminal Value = $6,175M / (1.108)^5 = $6,175M × 0.5988 = $3,697M

Enterprise Value = $1,372M + $3,697M = $5,069M
```

#### D. Calculate Equity Value and Price Per Share

```
Enterprise Value                 $5,069M
- Net Debt (Debt - Cash)         ($450M)
+ Non-operating Assets           $0M
- Minority Interest              $0M
- Preferred Stock                $0M
= Equity Value                   $4,619M

Diluted Shares Outstanding       100M

Price Per Share = $4,619M / 100M = $46.19

Current Stock Price: $42.00
Implied Upside: 10.0%
```

#### E. DCF Sensitivity Analysis **CRITICAL**

**Table 1: WACC vs. Terminal Growth Rate**

Create 2-way sensitivity table:
```
Price Per Share ($)     Terminal Growth Rate
WACC        1.5%    2.0%    2.5%    3.0%    3.5%
9.0%        $52     $55     $59     $63     $68
9.5%        $48     $51     $54     $58     $62
10.0%       $45     $48     $51     $54     $57
10.5%       $42     $45     $47     $50     $53
11.0%       $40     $42     $44     $47     $50
11.5%       $38     $40     $42     $44     $47
12.0%       $36     $38     $40     $42     $44

Base Case: WACC = 10.8%, g = 2.5% → $46
Format as heatmap: Green (high values) → Yellow → Red (low values)
```

**Table 2: Revenue CAGR vs. Terminal EBITDA Margin**
```
Price Per Share ($)     Terminal EBITDA Margin (2029E)
Revenue CAGR    28%     30%     32%     34%     36%
15%             $38     $42     $46     $50     $54
20%             $42     $46     $51     $56     $61
25%             $46     $51     $56     $62     $68
30%             $51     $56     $62     $68     $75
35%             $56     $62     $68     $75     $83

Base Case: Rev CAGR = 25%, EBITDA Margin = 32% → $56
```

### Step 3: Comparable Companies Analysis

#### A. Select Comparable Companies

**Selection Criteria:**
- Same industry/sector (primary requirement)
- Similar business model
- Comparable size (market cap, revenue)
- Similar growth profile
- Similar geographies

**Identify 5-10 peer companies:**
1. [Peer 1] - Direct competitor
2. [Peer 2] - Direct competitor
3. [Peer 3] - Adjacent player
4. [Peer 4] - Similar business model
5. [Peer 5] - Regional competitor
6. [Add 3-5 more]

**Document rationale for each peer selected.**

#### B. Gather Peer Financial Data

**For each comparable, gather:**
- Current stock price
- Shares outstanding (diluted)
- Market capitalization
- Total debt and cash (for EV calculation)
- Enterprise value
- LTM (Last Twelve Months) financials:
  - Revenue
  - EBITDA
  - EBIT
  - Net Income
- NTM (Next Twelve Months) consensus estimates
- Revenue growth rate
- EBITDA margin

**Data sources:**
- FactSet, CapitalIQ, Bloomberg (preferred)
- Company 10-Ks/10-Qs for actuals
- Consensus estimates from Yahoo Finance, Seeking Alpha (if pro tools unavailable)

#### C. Calculate Valuation Multiples

**For each peer, calculate:**
```
EV/Revenue (LTM) = Enterprise Value / LTM Revenue
EV/Revenue (NTM) = Enterprise Value / NTM Revenue (est.)
EV/EBITDA (LTM) = Enterprise Value / LTM EBITDA
EV/EBITDA (NTM) = Enterprise Value / NTM EBITDA (est.)
P/E (NTM) = Market Cap / NTM Net Income (est.)
```

#### D. Create Comparable Companies Table (MANDATORY FORMAT)

```
COMPARABLE COMPANIES ANALYSIS

Company      Ticker  Mkt Cap  EV/Rev  EV/Rev  EV/EBITDA  EV/EBITDA  P/E   Rev     EBITDA  Source
                     ($B)     LTM     NTM     LTM        NTM        NTM   Growth  Margin
Peer A       PRA     45.2     3.5x    3.2x    15.2x      13.8x      25x   18%     23%     FactSet 2026-05-19
Peer B       PRB     32.8     3.2x    2.9x    14.1x      12.5x      22x   15%     23%     FactSet 2026-05-19
Peer C       PRC     28.5     2.8x    2.6x    12.8x      11.2x      20x   12%     22%     FactSet 2026-05-19
Peer D       PRD     52.1     4.1x    3.7x    17.5x      15.2x      29x   22%     23%     FactSet 2026-05-19
Peer E       PRE     38.9     3.6x    3.3x    15.8x      14.1x      25x   17%     23%     FactSet 2026-05-19
Peer F       PRF     41.2     3.7x    3.4x    16.1x      13.9x      26x   19%     23%     FactSet 2026-05-19
Peer G       PRG     35.5     3.3x    3.0x    14.5x      12.8x      23x   16%     22%     FactSet 2026-05-19

[Target]     TRGT    38.0     3.4x    3.1x    14.8x      13.0x      24x   17%     23%     Model + FactSet

STATISTICAL SUMMARY
Maximum              52.1     4.1x    3.7x    17.5x      15.2x      29x   22%     23%
75th Percentile      45.2     3.7x    3.4x    16.1x      14.1x      26x   19%     23%
Median               38.9     3.5x    3.2x    15.2x      13.8x      25x   17%     23%
25th Percentile      32.8     3.2x    2.9x    14.1x      12.5x      22x   15%     22%
Minimum              28.5     2.8x    2.6x    12.8x      11.2x      20x   12%     22%

Note: Market data as of [Date]. LTM = Last Twelve Months. NTM = Next Twelve Months.
Source: [FactSet — peer trading multiples, 2026-05-19](https://...) (subscription required); peer 10-K filings for fiscal-year figures.
```

**Source column is MANDATORY.** Carry it through to the DOCX table in Task 5. Replace the placeholder dates above with the actual access date when running the task.

**CRITICAL**: The statistical summary (max/75th/median/25th/min) is MANDATORY.

#### E. Apply Multiples to Target Company

**Choose primary multiple (typically EV/EBITDA for mature companies):**

```
Target Company NTM EBITDA = $550M (from financial model)

Apply Median Peer Multiple:
Peer Median EV/EBITDA (NTM) = 13.8x
Implied EV = $550M × 13.8x = $7,590M

Apply 25th Percentile (Conservative):
25th Percentile EV/EBITDA (NTM) = 12.5x
Implied EV = $550M × 12.5x = $6,875M

Apply 75th Percentile (Optimistic):
75th Percentile EV/EBITDA (NTM) = 14.1x
Implied EV = $550M × 14.1x = $7,755M

Valuation Range (Comps): $6,875M - $7,755M
Midpoint: $7,315M

Convert to Equity Value:
Implied EV (Median)        $7,590M
- Net Debt                 ($450M)
= Implied Equity Value     $7,140M

Shares Outstanding         100M
Implied Price/Share        $71.40
```

**Justify Premium/Discount:**
- Target is growing 17% vs. peer median 17% → In-line
- Target EBITDA margin 23% vs. peer median 23% → In-line
- Target market position → [Justify premium/discount]
- **Conclusion**: Apply median multiple (no adjustment)

### Step 3b: Forward Target Multiple & Multiple Justification (PRIMARY for growth-equity archetype)

For the profitable-growth-equity archetype (the majority of names), this — not the DCF — produces the headline price target. The house pattern: apply a chosen multiple to an **out-year (FY+2/FY+3)** EPS or EBITDA, and justify the multiple three ways.

**A. Apply the multiple to an out-year, not NTM.**
```
Target FY+3 (2028E) EPS = $4.10 (from financial model)
Chosen target multiple   = 40x
Implied 2028E value      = $164  → discount back to a 12-month (e.g. Dec-2027) target
Target date / PT         = Dec-2027 PT $128 (40x 2028E EPS, discounted)
```
Date the target to the period when the out-year multiple is "earned" (JPM Yingliu: "Dec-2027 target, 40x 2028E EPS"; Citi: "36x avg 2027/28E EPS").

**B. Target-multiple justification (MANDATORY — three anchors).** The chosen multiple must be defended against ALL THREE, each with an inline deep-URL citation:

1. **The stock's own historical valuation band** — e.g. "+1 SD above the 10-yr up-cycle mean" / "within the historical 10-31x range" / "= the A-share's own historical median." Cite the data source for the band (the stock's price history on a dated data-provider page).
2. **At least one named global peer's current multiple** — e.g. "vs Howmet 37x." Cite that peer's filing or a dated FactSet/Yahoo page, NOT the peer's homepage.
3. **The EPS/earnings-CAGR-vs-peers gap** that earns the premium/discount — e.g. "justified by 55% EPS CAGR > peers' 23%."

Library patterns to mirror verbatim:
- JPM Yingliu: "40x 2028E vs Howmet 37x, justified by 55% EPS CAGR > peers' 23%"
- GS Co-Tech: "22x 2028E = +1 SD above the 10-yr up-cycle mean"
- Nomura Victory Giant: "27x 2027E = the A-share's own historical median P/E"

Never apply a peer-median multiple without all three anchors. The analyst's own model is NOT one of the anchors and is never cited as a source (project "model is not a source" rule).

### Step 3c: Estimates vs Consensus (MANDATORY thesis pillar)

An initiation exists to assert a **differentiated out-year number**. Table the analyst's forecasts against sell-side consensus for FY+1..FY+3, state the %-delta, and explain why the Street is wrong — this is the analytical spine of the report, not an afterthought.

```
ESTIMATES VS CONSENSUS

Metric            FY+1 (2026E)        FY+2 (2027E)        FY+3 (2028E)
                  Ours  Cons  Δ%      Ours  Cons  Δ%      Ours  Cons  Δ%
Revenue ($M)      1,180 1,120 +5%     1,510 1,380 +9%     1,940 1,690 +15%
EPS ($)           2.10  2.00  +5%     3.05  2.70  +13%    4.10  2.95  +39%
EBITDA margin     24%   23%   +1pt    27%   25%   +2pt    30%   27%   +3pt

Why the Street is wrong: [1-2 sentences naming the specific driver consensus
under-models — e.g. "consensus underestimates MRDIMM penetration / overseas
order intake / margin from the 2027 capacity ramp."]

Source (consensus): [FactSet consensus, 2026-05-19](https://...) (subscription required)
                    OR [Yahoo Finance analyst estimates](https://finance.yahoo.com/quote/TICKER/analysis), 2026-05-19
Our estimates = analyst model (label as estimate; NOT a citable source).
```

Library patterns: Bernstein Montage "2028E EPS Rmb6.25 vs consensus 4.49, +39%"; UBS Tao "+12-15% above consensus"; UBS Zhongfu per-year EPS-vs-consensus rows. Each **consensus** figure needs a dated data-provider citation. The analyst's own number is labelled an estimate and is never cited as a source. This table carries through to Task 5 as a named "Estimates vs Consensus" subsection in the Investment Thesis.

### Step 4: Precedent Transactions (Optional)

**Note**: Only if M&A is relevant for this sector/company.

#### A. Identify Relevant Transactions

**Search for 5-10 M&A deals:**
- Same industry, last 3-5 years
- Similar size (0.5x to 2x target's size)
- Announced and closed deals

**Example:**
```
PRECEDENT TRANSACTIONS ANALYSIS

Date     Target        Acquirer      Deal     EV/Rev  EV/EBITDA  Premium  Rationale
                                    Value($B)  LTM     LTM
Q1 2024  Comp A       Strategic      $5.2B    4.2x    16.5x      35%      Consolidation
Q3 2023  Comp B       PE Firm        $3.8B    3.8x    14.2x      28%      Platform
Q4 2023  Comp C       Strategic      $4.5B    4.0x    15.8x      32%      Geographic
Q2 2023  Comp D       Strategic      $6.1B    4.5x    17.2x      38%      Strategic fit
Q1 2023  Comp E       PE Firm        $3.2B    3.5x    13.5x      25%      Carve-out

Median                                        4.0x    15.8x      32%

Source: CapitalIQ, company filings, press releases.
```

#### B. Apply to Target Company

```
Target Company LTM EBITDA = $500M
Precedent Median EV/EBITDA (LTM) = 15.8x

Implied EV (Precedent) = $500M × 15.8x = $7,900M

Note: Precedent multiples typically 10-20% higher than trading comps
due to control premium and synergies.
```

### Step 5: Valuation Reconciliation

#### A. Create Valuation Summary Table

```
VALUATION SUMMARY

Method                  Low     Base    High    Weight  Weighted Value
DCF Analysis            $42     $46     $51     50%     $23.00
Trading Comps (NTM)     $64     $71     $78     40%     $28.40
Precedent Trans.        $70     $79     $88     10%     $7.90
                                                        -------
Weighted Average Target                         100%    $59.30

Rounded Price Target: $59.00

Current Price (as of [Date]):    $42.00
Upside to Target:                40% ($59.00 / $42.00 - 1)
```

#### B. Determine Weighting Rationale

**Typical Weighting:**
- DCF: 40-60% (higher when forecasts reliable)
- Trading Comps: 25-40% (reflects market sentiment)
- Precedent Trans: 10-25% (lower unless M&A likely)

**For this example:**
- DCF 50%: High confidence in projections
- Comps 40%: Robust peer set
- Precedent 10%: M&A unlikely near-term

#### C. Create Valuation Football Field Chart

```
VALUATION FOOTBALL FIELD

Method                  Low ◄────────── Range ──────────► High

DCF Analysis            $42 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $51

Trading Comps (NTM)     $64 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $78

Precedent Trans.        $70 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $88
                                          ↑
                                    Current: $42
─────────────────────────────────────────────────────────
Valuation Range         $42                          $88
Price Target: $59 (weighted average)

Color code:
- DCF: Blue
- Trading Comps: Green
- Precedent Trans: Orange
- Vertical line at current price: Red dashed
- Vertical line at target: Black solid
```

#### D. Scenario-Based Valuations

```
VALUATION BY SCENARIO

Scenario    Probability  Revenue  EBITDA    DCF      Comps    Weighted
                        CAGR     Margin    Value    Multiple  Avg
Bear Case   20%         18%      28%       $38      11.5x     $42
Base Case   60%         25%      32%       $46      13.8x     $59
Bull Case   20%         32%      36%       $58      16.0x     $82

Expected Value (probability-weighted): $59
```

#### D2. PT Scenario Ladder (three datable price targets — house-facing output)

Distinct from the internal DCF grid above, also produce bull/base/bear **as price targets**, each driven by a specific **multiple × out-year-EPS** combination so the football field is reproducible (Bernstein Arm "base $300 / bull $390"). Each row must state the assumption delta, the resulting out-year EPS/EBITDA, the multiple applied, and the implied share price:

```
PT SCENARIO LADDER

Scenario  Prob.  Driving assumption delta            2028E EPS  Multiple  Implied PT
Bull      20%    Overseas orders +X; margin +3pt     $5.10      44x       $190
Base      60%    Order book as contracted            $4.10      40x       $128
Bear      20%    Capacity ramp slips; ASP −Y%        $2.80      30x       $ 70

Each PT is re-derivable: PT = multiple × out-year EPS (discounted to the target date).
```

This ladder feeds Task 4's football field and Task 5's scenario section. For a Neutral/Sell call the base PT sits at or below the current price — the ladder still works, the bear PT just becomes the headline.

### Step 6: Final Price Target & Recommendation

**Write the PT line in the house form.** State the rating, the multiple, the out-year it is applied to, the target date, and the implied move against a dated close — all in one breath:

```
[Rating], 12-month PT [currency][X] = [multiple]× [FY+n]E [EPS/EBITDA],
target date [Mon-YYYY], implying [Y]% [upside/downside] vs [price] ([date]).
```

Examples from the library: JPM "OW, Dec-2027 target 40x 2028E EPS"; Citi "Buy, TP NT$11,000 on 36x avg-2027/28E EPS"; Bernstein A+H dual-PT "44x A / 56.4x H on 2BF EPS." For a **Neutral/Sell** the same skeleton reads "implying −X% **downside**" and the rating is NEUTRAL / UNDERPERFORM / SELL (e.g. Bernstein Summit "UP, TP $7.7, −57%").

```
═══════════════════════════════════════════════════════════
INVESTMENT RECOMMENDATION
═══════════════════════════════════════════════════════════

Current Price:          $42.00 (as of [Date])
Price Target:           $128.00 — 40x 2028E EPS, Dec-2027 target
Implied Upside/(Downside): +40.5%

Rating:                 BUY / OUTPERFORM
                       (or NEUTRAL / UNDERPERFORM / SELL — downside PTs
                        are first-class; the skeleton reads "implied downside %")

Primary Method:        Forward target multiple on FY+3 (2028E) EPS
                       (per archetype table, Step 1b). DCF (above) reconciled
                       as cross-check, NOT 50%-weighted, for a growth equity.
Multiple Justification: 40x vs [peer] 37x [cite] · +1 SD above 10-yr mean [cite]
                       · 55% EPS CAGR > peers' 23% (Step 3b's three anchors).

Time Horizon:          12 months

───────────────────────────────────────────────────────────
12-MONTH CATALYST CALENDAR (each catalyst DATED)
───────────────────────────────────────────────────────────

Every catalyst MUST carry a quarter/month and be a concrete event the reader
can wait for — write "Cape-1 COD 4Q26", NOT "new product launch." Mirror
Bernstein Fervo "Cape-1 COD 4Q26, 15MW single-well validation"; GS Hemab
"sutacimig GT Ph3 start H2-2026; FVIID Ph2 readout late-2026/early-2027";
GS surgical-robots "3Q26 overseas-order update." Cross-reference the
catalyst-calendar skill for the dated-event format.

1. 3Q26 — Overseas order-book update (next print of contracted $ / GW)
2. 4Q26 — Lead product / project COD or volume milestone
3. 1H27 — Margin inflection from the capacity ramp (target XX% EBITDA)
4. 2H27 — Regulatory / approval decision (NMPA/FDA/CE) or index inclusion
5. FY27 — Out-year EPS print that confirms (or breaks) the est-vs-consensus gap

For a Sell/Neutral, reframe this list as "what breaks the thesis" — the dated
events that would VALIDATE the downside case rather than the upside.

───────────────────────────────────────────────────────────
KEY RISKS TO PRICE TARGET
───────────────────────────────────────────────────────────

(For a SELL/UNDERPERFORM initiation, flip this section to "Upside risks to
our Sell" — the symmetric mirror: the dated events / scenarios that would
force a higher PT and invalidate the short thesis. Bernstein Summit / AEON
downside initiations carry exactly this mirrored risk block.)

Downside Risks:
1. Competitive Pressure (High probability, -15% impact)
   - New entrant launched competing product
   - Could pressure pricing and market share

2. Execution Risk (Medium probability, -10% impact)
   - New product launch delays or underperformance
   - Management turnover

3. Macro Slowdown (Medium probability, -20% impact)
   - Economic recession would impact customer spending
   - Operating leverage would reverse

4. Regulatory Risk (Low probability, -25% impact)
   - Potential new regulations in key market
   - Would increase compliance costs

Upside Risks:
1. M&A Bid (Low probability, +35% impact)
   - Strategic acquirer pays control premium

2. Beat-and-Raise (Medium probability, +10% impact)
   - Consistent outperformance vs. estimates

═══════════════════════════════════════════════════════════
```

---

## Quality Standards

### DCF Quality Checks
- [ ] WACC properly calculated with documented components
- [ ] Terminal value reasonable (< 70% of total enterprise value)
- [ ] Sensitivity analysis covers realistic ranges (±200-300bps for WACC, ±100bps for terminal growth)
- [ ] Unlevered FCF properly calculated from EBIT
- [ ] Enterprise to equity value bridge correct
- [ ] Share count is diluted shares, not basic

### Comparables Quality Checks
- [ ] 5-10 comparable companies selected
- [ ] Peer selection defensible (document why each peer was chosen)
- [ ] Statistical summary included (max/75th/median/25th/min) - MANDATORY
- [ ] Multiple selection appropriate (EV/EBITDA for mature, EV/Revenue for high-growth)
- [ ] Premium/discount justified with specific factors
- [ ] Data sourced properly with dates noted

### Overall Valuation Quality Checks
- [ ] At least 2 valuation methods used (DCF + Comps minimum)
- [ ] Weighting explained and appropriate
- [ ] Valuation range provided (low/base/high), not just point estimate
- [ ] Scenarios analyzed (Bull/Base/Bear)
- [ ] Sanity checks performed (see below)
- [ ] All assumptions documented with rationale

---

## Sanity Checks

**Always perform these validation checks:**

1. **Historical Multiple Check**
   - Is implied multiple in line with company's historical trading range?
   - If not, explain why

2. **Peer Comparison**
   - Is premium/discount vs. peers justified by fundamentals?
   - Check: growth, margins, market position

3. **Implied Growth Check**
   - What growth is market pricing in at current price?
   - Is that reasonable given company trajectory?

4. **Market Cap Reasonableness**
   - Does total market cap make sense given company size and peers?
   - Would company be too large/small relative to industry?

5. **Terminal Value Check**
   - Is terminal value < 60-70% of total enterprise value?
   - If > 70%, projections may not be long enough

6. **WACC Reasonableness**
   - Is WACC 8-14% range for typical companies?
   - Tech/high-growth: 10-14%
   - Mature/stable: 7-10%

7. **Implied Returns Check**
   - What IRR from current price to target over 12 months?
   - Is that consistent with recommendation rating?

---

## Output Files

Create the following deliverables:

### 1. Valuation Analysis Document
**File**: `[Company]_Valuation_Analysis_[Date].md` (written analysis)

**Contents** (4-6 pages):
- Executive summary with price target
- DCF analysis (1 page) with sensitivity table
- Comparable companies analysis (1 page) with statistical summary
- Precedent transactions (0.5 page) if applicable
- Valuation summary and football field (0.5 page)
- Investment recommendation (1 page)
- Key catalysts and risks (1 page)

### 2. Excel Valuation Tabs
**Add to Task 2's financial model file:** `[Company]_Financial_Model_[Date].xlsx`

**IMPORTANT**: Do NOT create a separate Excel file. Add these tabs to the existing financial model from Task 2. This keeps all quantitative data in one place.

**Tabs to add:**
- DCF tab with full calculations
- Sensitivity analysis tab
- Comps tab with peer data
- Precedent transactions tab (if applicable)
- Valuation summary tab

---

## Success Criteria

A successful valuation analysis should:
1. Use at least 2 methods (DCF + Comps minimum)
2. Include comprehensive DCF sensitivity analysis (2-way tables)
3. Include statistical summary in comps (max/75th/median/25th/min)
4. Provide valuation range (low/base/high), not point estimate
5. Document all key assumptions with clear rationale
6. Perform sanity checks
7. Arrive at defensible price target
8. Provide clear buy/hold/sell recommendation
9. Identify 3-5 key catalysts
10. Identify 3-5 key risks
11. Be auditable and transparent

---

## Next Steps

After completing Task 3, the valuation analysis will be used for:
- **Task 4 (Charts)**: Create DCF sensitivity heatmaps, valuation football field, scenario comparison charts
- **Task 5 (Report Assembly)**: Integrate valuation analysis into final report

The price target and recommendation are the foundation of the final investment recommendation in the equity research report.
