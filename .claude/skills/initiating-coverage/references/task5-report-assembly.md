# Task 5: Report Assembly - Detailed Workflow

This document provides step-by-step instructions for executing Task 5 (Report Assembly) of the initiating-coverage skill.

## Task Overview

**Purpose**: Write and assemble the comprehensive final markdown report.

**Prerequisites**: ⚠️ Verify before starting - ALL PREVIOUS TASKS REQUIRED
- **Required**: Company research from Task 1
- **Required**: Financial model from Task 2
- **Required**: Valuation analysis from Task 3
- **Required**: Chart files from Task 4

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS ALL TASKS 1-4 ARE COMPLETE**

This is the final assembly task. It cannot be completed without all previous work products.

**IF ANY OF TASKS 1, 2, 3, OR 4 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (6-8K words)
- Task 2: Financial model with all 6 tabs
- Task 3: Valuation analysis with price target and recommendation
- Task 4: Charts zip file with 25-35 charts

Do not attempt to create placeholder content, substitute missing sections, or assemble an incomplete report. The report requires ALL inputs to be publication-ready.

**Output**: Comprehensive Equity Research Report (`.md`)
- Word count: 10,000-15,000 words (MINIMUM 10,000 — equivalent to 30-50 paginated pages)
- Charts: 25-35 image references via `![caption](path/to/chart.png)`
- Tables: 12-20 comprehensive markdown tables
- Saved at `reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md` so it renders in the Claude Reports viewer alongside `company-research`, `earnings-analysis`, and `sec-report-summary` outputs.

---

## 🔥 CRITICAL INSTRUCTION: SPARE NO TOKENS OR EFFORT

**THIS IS THE FINAL DELIVERABLE. GO ALL OUT. NO SHORTCUTS. NO ABBREVIATIONS.**

After completing 4 previous tasks, this final task assembles everything into publication-ready institutional research. **This must be PERFECT.**

### Absolute Requirements

**DO:**
- ✅ **Use ENTIRE token budget if needed** - This is what it's for
- ✅ **Write EVERY section in FULL** - Not summaries, not placeholders, FULL CONTENT
- ✅ **Include ALL 25-35 charts** - Embed every single chart from Task 4 throughout the document
- ✅ **Create ALL 12-20 tables** - Extract every financial table from Excel, don't skip any
- ✅ **Copy ALL 6-8K words from Task 1** - Use Company 101 content verbatim (40-50% of report)
- ✅ **Write 2,000-3,000 words on Projection Assumptions** - Product-by-product, region-by-region detail
- ✅ **Write 1,500-2,000 words on Scenario Analysis** - Specific Bull/Base/Bear parameters
- ✅ **Achieve 10,000-15,000 total words** - This is a MINIMUM, not a suggestion
- ✅ **Produce 30-50 pages minimum** - Text-dense with charts every 200-300 words
- ✅ **Professional institutional quality** - Indistinguishable from JPMorgan/Goldman Sachs

**NEVER:**
- ❌ "This section would include..." - WRITE THE ACTUAL SECTION
- ❌ "Charts would be inserted here..." - INSERT THE ACTUAL CHARTS
- ❌ "See financial model for details..." - EXTRACT AND WRITE THE DETAILS
- ❌ "For brevity, we'll summarize..." - NO SUMMARIZING, WRITE IN FULL
- ❌ Skip sections to conserve tokens - USE WHATEVER TOKENS ARE NEEDED
- ❌ Create abbreviated versions - EVERY SECTION MUST BE COMPLETE
- ❌ Reference external files instead of including content - INCLUDE EVERYTHING

### Quality Standard

**This report will be read by institutional investors making million-dollar decisions.**

It must be:
- **Complete**: Every section written in full with no placeholders
- **Comprehensive**: All data extracted and included, all charts embedded
- **Professional**: Proper formatting, citations, tables, charts throughout
- **Thorough**: Deep analysis with specific numbers, detailed assumptions, complete scenarios
- **Dense**: 60-80% page coverage with text and visuals on every page

**Creating the final work product of a 6-10 hour equity research process. Make it count.**

---

## Input Verification (CRITICAL)

**BEFORE STARTING - ALL TASKS MUST BE COMPLETE:**

### Task 1 Verification:
- [ ] Company research document exists? (6-8K words)
- [ ] Management bios complete? (300-400 words × 3-4 execs)
- [ ] Competitive analysis complete? (5-10 competitors)
- [ ] Risk assessment complete? (8-12 risks)

### Task 2 Verification:
- [ ] Financial model exists and can be opened?
- [ ] Model has projections (5 years)?
- [ ] Scenarios exist (Bull/Base/Bear)?
- [ ] Revenue by product table complete (20-30 rows)?
- [ ] Revenue by geography table complete (15-20 rows)?

### Task 3 Verification:
- [ ] Valuation analysis complete?
- [ ] Price target determined?
- [ ] Recommendation set? (BUY/HOLD/SELL)
- [ ] DCF analysis complete with sensitivity table?
- [ ] Comparable companies analysis complete with statistical summary?

### Task 4 Verification:
- [ ] 25-35 chart files exist?
- [ ] All 4 mandatory charts present?
  - [ ] Revenue by product (stacked area)
  - [ ] Revenue by geography (stacked bar)
  - [ ] DCF sensitivity (heatmap)
  - [ ] Valuation football field
- [ ] Chart files accessible and can be opened?
- [ ] Chart index created?

**IF ANY VERIFICATION FAILS**: Stop and complete missing task first.

---

## Report Specifications

### Length Requirements
- **Pages**: 30-50 (MINIMUM 30 pages)
- **Word Count**: 10,000-15,000 words (MINIMUM 10,000 words)
- **Charts**: 25-35 embedded PNG/JPG images
- **Tables**: 12-20 comprehensive financial tables
- **Density**: 60-80% page coverage

### Critical Sections with Word Counts

| Section | Minimum | Target | Critical? |
|---------|---------|--------|-----------|
| Investment Summary (Page 1) | 500 | 700 | |
| Investment Thesis | 800 | 1,200 | |
| Risk Factors | 600 | 900 | |
| Company Description | 800 | 1,200 | |
| Management Bios | 1,000 | 1,400 | |
| Products & Services | 700 | 1,000 | |
| **Projection Assumptions** | **2,000** | **3,000** | ⭐ YES |
| **Scenario Analysis** | **1,500** | **2,000** | ⭐ YES |
| Financial Analysis | 1,200 | 1,800 | |
| Valuation Methodology | 800 | 1,200 | |

**Total: 10,000-15,000 words**

---

## Report Structure

### Page 1: Investment Summary (CRITICAL PAGE)

**This is the most important page. Must have:**

1. **"INITIATING COVERAGE" header** (NOT "Company Update")
2. **Thesis-focused title** (e.g., "AI Platform Leader Positioned for 40% CAGR")
3. **Rating box** with:
   - Rating (BUY/OUTPERFORM/HOLD/UNDERPERFORM/SELL)
   - Current price
   - Target price
   - 52-week range
   - Market cap
   - Enterprise value
4. **Research analyst information** with credentials
5. **Stock price performance chart** (Figure 1)
6. **3-4 detailed investment bullets** with ■ character
   - Each bullet has **bold topic header** + 3-5 sentences
   - Lead with key numbers
7. **Financial summary table** (2-3 years historical + 2-3 years projected)
   - Years noted as "A" for actual, "E" for estimate

**Bullet Format Example:**
```
■ **Vertical SaaS leadership and regulatory moat should enable $50bn+ TAM by 2030.**
Deep domain expertise in healthcare IT, strong customer retention (95%+ net revenue retention),
and cross-sell capabilities have driven Acme Health's market expansion. With the healthcare IT
market expected to reach $50bn+ by 2030, Acme Health is well-positioned to capture share given
its regulatory moat and high switching costs. Management has indicated that 70% of current
revenue comes from enterprise hospital systems, suggesting strong product-market fit.
```

### Pages 2-5: Investment Thesis & Risks

**Investment Thesis (800-1,200 words)**
- 3-5 key thesis pillars
- Each pillar: 200-300 words
- Lead with key statistic
- Quantify financial impact
- Include timeline

**Risk Assessment (600-900 words)**
- 8-12 identified risks
- Organized by category:
  - Company-specific risks (4-6)
  - Industry/market risks (3-4)
  - Financial risks (2-3)
  - Macroeconomic risks (2-3)
- Each risk: 50-100 word description

### Pages 6-17: Company 101

**Company Description (800-1,200 words)**
- What the company does (plain English)
- Business model and monetization
- Geographic presence
- Scale metrics

**Company History (800-1,200 words)**
- Founding story
- Timeline of major milestones
- Strategic pivots
- Recent developments

**Management Team (1,000-1,400 words)**
- 300-400 word bio for each of 3-4 key executives
- Include: role, background, accomplishments, education
- Governance structure

**Products & Services (700-1,000 words)**
- Detailed product portfolio
- Features and differentiation
- Target customers
- Pricing models

**Customers & Go-to-Market (500-700 words)**
- Customer segments
- Distribution channels
- Sales strategy
- Key partnerships

**Industry Overview (800-1,200 words)**
- Industry definition and scope
- Market size and growth
- Key trends
- Regulatory environment

**Competitive Landscape (700-1,000 words)**
- 5-10 key competitors
- Market positioning
- Competitive advantages
- Market share analysis

**TAM Analysis (500-700 words)**
- Total addressable market sizing
- Market growth projections
- Company's serviceable market

### Pages 18-30: Financial Analysis

**Historical Financial Analysis (1,200-1,800 words)**
- Revenue trends and drivers
- Margin evolution
- Cash flow analysis
- Key metrics trajectory
- Historical context

**Projection Assumptions (2,000-3,000 words)** ⭐ CRITICAL

**MUST be extremely detailed. Structure:**

**A. Revenue by Product Assumptions (1,000-1,500 words)**

For EACH major product category:
```
[Product Category A] Revenue Assumptions

We project [Product A] revenue to grow from $XXM in 2024A to $XXM in 2029E,
representing a XX% CAGR. This growth is driven by:

1. [Driver 1 with specific quantification]
   - Specific metric: from XX to XX
   - Timeline: achieving YY by 2026E
   - Basis: [source or rationale]

2. [Driver 2 with specific quantification]
3. [Driver 3 with specific quantification]
[... 8-12 detailed points total for this product ...]

Specific assumptions by year:
- 2025E: XX% growth driven by [specific factors]
- 2026E: XX% growth as [specific factors]
- 2027-2029E: XX% CAGR as [longer-term factors]

Key risks to these assumptions include [specific risks].
```

**Repeat for EACH major product category.**

**B. Geographic Revenue Assumptions (500-800 words)**

For EACH major region:
```
[Region] Revenue Assumptions

We project [Region] revenue to grow XX% CAGR from 2024-2029E, reaching $XXM, driven by:

1. [Market dynamic with quantification]
2. [Distribution expansion with specifics]
3. [Competitive positioning]
[... 6-8 detailed points total for this region ...]
```

**Repeat for EACH major geographic region.**

**C. Other Key Assumptions (500-700 words)**
- Gross margin evolution (with specific drivers and bridge)
- Operating expense assumptions (R&D, S&M, G&A as % of revenue)
- Working capital assumptions (DSO, DIO, DPO with specific days)
- CapEx as % of sales (with justification)
- Tax rate assumptions

**Scenario Analysis (1,500-2,000 words)** ⭐ CRITICAL

**MUST have specific parameters for each scenario. Structure:**

**Bull Case (500-700 words)**
```
Bull Case: [Title describing key optimistic scenario]

Probability: XX%

Key Assumptions:
- Revenue CAGR (2024-2029E): XX% (vs. XX% base case)
- 2029E Revenue: $X,XXXm (vs. $X,XXXm base)
- 2029E EBITDA Margin: XX% (vs. XX% base)
- Key product growth: XX% CAGR (vs. XX% base)
- Geographic expansion: [specific milestones and timeline]
- Market share: XX% by 2029E (vs. XX% base)

Catalysts Required for Bull Case:
1. [Specific catalyst] - Expected timing: [date/quarter]
2. [Specific catalyst] - Expected timing: [date/quarter]
3. [Specific catalyst] - Expected timing: [date/quarter]

Detailed Rationale:
[200-300 words explaining what needs to happen for bull case to materialize.
Be specific about product launches, market conditions, competitive dynamics, etc.]

Valuation Implications:
- DCF Value: $XX per share (XX% upside from current)
- Trading Comps: XX.Xx EV/EBITDA implies $XX per share
- Bull Case Target: $XX per share
```

**Base Case (300-500 words)**
```
Base Case: [Title describing most likely scenario]

Probability: XX%

Key Assumptions:
[Similar structure to Bull Case with base assumptions]

Rationale:
[Explain why this is most likely scenario]

Valuation:
- DCF Value: $XX per share
- Trading Comps: $XX per share
- Base Case Target: $XX per share (weighted average)
```

**Bear Case (500-700 words)**
```
Bear Case: [Title describing downside scenario]

Probability: XX%

Key Assumptions:
[Similar structure with downside parameters]

Downside Triggers:
1. [Specific risk event] - Likelihood: [%]
2. [Specific risk event] - Likelihood: [%]
3. [Specific risk event] - Likelihood: [%]

Rationale:
[200-300 words on what would cause bear case]

Valuation Implications:
- DCF Value: $XX per share (XX% downside from current)
- Trading Comps: $XX per share
- Bear Case Target: $XX per share
```

**Scenario Comparison (200-300 words)**
- Comprehensive comparison table with key metrics
- Analysis of probability-weighted outcomes
- Risk/reward assessment
- Path dependency discussion

**Growth Drivers (800-1,200 words)**
- 3-5 key growth drivers
- Each quantified with specific opportunity size
- Timeline and milestones
- Supporting data from model

### Pages 31-40: Valuation Analysis

**Valuation Methodology (800-1,200 words)**

**DCF Analysis (300-400 words)**
- Methodology explanation
- Key assumptions:
  - WACC: X.X% (calculation breakdown)
  - Terminal growth: X.X% (rationale)
  - Terminal margin: XX% (justification)
- Sensitivity analysis discussion
- DCF value: $XX per share

**Comparable Companies (300-400 words)**
- Peer selection rationale (why these 5-10 companies)
- Statistical summary (max/75th/median/25th/min)
- Multiple selection (why EV/EBITDA vs. EV/Revenue vs. P/E)
- Premium/discount justification (why target deserves premium/discount)
- Comparable companies value: $XX per share

**Precedent Transactions (200-300 words, if applicable)**
- Transaction relevance
- Control premium analysis
- Precedent transactions value: $XX per share

**Valuation Reconciliation (200-300 words)**
- Weighting rationale (e.g., DCF 50%, Comps 40%, Precedent 10%)
- Weighted average calculation
- Valuation range (low/base/high)
- Final price target: $XX

**Price Target & Recommendation (300-500 words)**
- Final recommendation (BUY/OUTPERFORM/HOLD/UNDERPERFORM/SELL)
- Price target: $XX (XX% upside from current $XX)
- Time horizon: 12 months
- Key catalysts (3-5 with specific timeframes)
- Key risks to price target (3-5 with impact quantification)

### Pages 41-50: Appendices

**Data Sources & References**
- All sources listed with dates
- Organized by category:
  - SEC Filings (with EDGAR links)
  - Earnings Calls (with transcript links)
  - Company Materials
  - Industry Reports
  - News Articles
- **ALL URLs must be clickable hyperlinks**

**Detailed Financial Model Assumptions**
- Comprehensive assumptions detail
- Calculation methodologies
- Data sources for historical figures

**Additional Supporting Tables**
- Extended financial projections
- Detailed comparable companies data
- Sensitivity analyses

---

## Report Assembly Philosophy

**CRITICAL PRINCIPLE 1**: A good equity research report is **text-dense with lots of illustrating images**.

**Target density**: 60-80% page coverage
- Every page should have BOTH text AND visuals
- Charts should be interspersed throughout text, not grouped
- Average 1 chart per page minimum (30-50 pages = 25-35+ charts)
- Tables should break up large text blocks

**CRITICAL PRINCIPLE 2**: Write the report directly as markdown with the Write/Edit tools.

**REQUIRED TOOLS**:
- **Write / Edit tools** — Author the final `.md` directly. No DOCX skill, no python-docx, no intermediate Word document.
- **XLSX skill** — Read data from Excel files
  - Extract tables from Task 2 financial model
  - Read Task 3 valuation tabs
  - Pull historical financials from Task 1
- **Read tool** — Open .md and .png inputs
  - Read: `reports/company/<Slug>/<Slug>_Research_Document_[Date].md` (English) or `reports/company/<Slug>/<Slug>_公司研究_[Date].md` (Chinese — produced by the `/company-research` skill)
  - Read: `[Company]_Financial_Model_[Date].xlsx` (via XLSX skill)
  - Reference (don't read): `charts/chart_01.png`, `charts/chart_02.png`, etc. — these are linked from the .md, not embedded.
- **Write tool** — Output: `reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`

**DO NOT**: Manually copy/paste or describe what should be done. Do NOT use the DOCX skill — the output is a single markdown file.
**DO**: Use Read/XLSX to ingest data, then Write/Edit to author the `.md` report.

**Content Reuse Strategy**:
- **Task 1 content (40-50% of report)**: Read .md file → Copy sections into the report → Insert chart references
- **Task 2/3 data (30-40% of report)**: Read .xlsx file → Extract tables as markdown pipe tables → Write interpretation
- **Original writing (10-20% of report)**: Investment thesis, projection assumptions, scenario analysis

**This approach**:
- Maximizes efficiency (no rewriting 6-8K words that are already good)
- Maintains quality (Task 1 content is substantive, professional analysis)
- Focuses effort on value-add (quantitative interpretation and investment thesis)
- Produces a file that renders in the Claude Reports viewer and version-controls cleanly in git (line-level diffs, no binary churn)

---

## Step-by-Step Report Assembly Workflow

### Step 1: Organize All Inputs and Verify Files

**Verify all input files exist:**

Use Claude's file operations to check:
- `reports/company/<Slug>/<Slug>_Research_Document_[Date].md` (English) or `reports/company/<Slug>/<Slug>_公司研究_[Date].md` (Chinese — produced by the `/company-research` skill) (Task 1)
- `[Company]_Historical_Financials_[Date].xlsx` (Task 1)
- `[Company]_Financial_Model_[Date].xlsx` (Task 2 with Task 3 tabs)
- `[Company]_Valuation_Analysis_[Date].md` (Task 3)
- `[Company]_Charts_[Date].zip` (Task 4) - **Extract this first**

**Step 1a: Extract Charts from Zip File**

Before proceeding, extract all chart files from the Task 4 zip:
- Locate `[Company]_Charts_[Date].zip`
- Extract all contents into `reports/company/<Slug>/charts/` so the .md's relative `![](charts/chart_XX.png)` references resolve
- Verify 25-35 PNG files were extracted
- Verify chart_index.txt is present

**Expected folder structure after extraction:**
```
reports/company/<Slug>/
├── <Slug>_Research_Document_[Date].md  (from /company-research — Task 1)
├── [Company]_Historical_Financials_[Date].xlsx
├── [Company]_Financial_Model_[Date].xlsx (Task 2 + Task 3 tabs)
│   ├── [Task 2 tabs: Revenue Model, Income Statement, Scenarios, etc.]
│   └── [Task 3 tabs: DCF, Sensitivity, Comps, Valuation Summary]
├── [Company]_Valuation_Analysis_[Date].md  (Task 3)
├── [Company]_Charts_[Date].zip               (Task 4 deliverable, kept for archival)
├── charts/                                   (extracted from zip — referenced from the .md)
│   ├── chart_01_stock_price.png
│   ├── chart_02_revenue_growth.png
│   ├── chart_03_revenue_by_product.png ⭐
│   ├── chart_04_revenue_by_geography.png ⭐
│   ├── ... (21-31 more charts)
│   ├── chart_28_dcf_sensitivity.png ⭐
│   ├── chart_32_valuation_football_field.png ⭐
│   └── chart_index.txt
├── sources_and_urls.txt
└── <Slug>_Initiation_Report_<Date>.md       ← Task 5 output (this file)
```

**Note**: Chart references in the .md use the relative path `charts/chart_XX.png`. Keep the `charts/` folder co-located with the .md so the links resolve when viewing in Claude Reports or any markdown renderer.

**Open and inspect files using Claude skills:**

1. **Read Task 1 markdown file** - Use Read tool to view content
2. **Open Task 2/3 Excel file** - Use XLSX skill to inspect tabs:
   - Verify required tabs exist: Revenue Model, Income Statement, Scenarios, DCF, Sensitivity Analysis, Comparable Companies
3. **Read Task 3 markdown file** - Use Read tool to view valuation analysis
4. **Check chart files** - Verify all 25-35 PNG files present

**Note**: Task 2's financial model file now contains both the original modeling tabs (from Task 2) AND the valuation tabs (added by Task 3). This single Excel file contains all quantitative data needed for report assembly.

### Step 2: Extract Tables from Excel Using XLSX Skill

**Use Claude's XLSX skill to extract data from Excel files:**

#### Table 1: Page 1 Summary Financials

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Income Statement` tab
3. Extract key rows: Revenue, Gross Profit, EBITDA, Net Income, EPS, FCF
4. Extract years: 2022A, 2023A, 2024A, 2025E, 2026E, 2027E
5. Create summary table with growth rates and margins

#### Table 2: Full Income Statement (40-50 line items)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read entire `Income Statement` tab
3. Extract all line items (40-50 rows)
4. Extract columns for historical (2020A-2024A) + projected years (2025E-2029E)
5. Include all margins and growth rates

#### Table 3: Revenue by Product (20-30 rows)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Revenue Model` tab
3. Navigate to product section (typically starts ~row 5)
4. Extract 20-30 rows showing each product category
5. Include columns: Product name, historical years, projected years, % of Total, YoY Growth

#### Table 4: Revenue by Geography (15-20 rows)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Revenue Model` tab
3. Navigate to geography section (typically starts ~row 40)
4. Extract 15-20 rows showing each geographic region
5. Include columns: Region, historical years, projected years, % of Total, YoY Growth

#### Table 5: Comparable Companies
**Extract from:** Task 3 valuation tabs in Task 2's financial model (`Comparable Companies` tab)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Comparable Companies` tab (added by Task 3)
3. Extract full table with company names as row headers
4. **CRITICAL**: Verify statistical summary rows are present at bottom:
   - Maximum
   - 75th Percentile
   - Median
   - 25th Percentile
   - Minimum
5. If statistical summary is missing, report ERROR

**Expected format:**
```
Company      Ticker  Mkt Cap  EV/Rev  EV/Rev  EV/EBITDA  EV/EBITDA  P/E   Rev     EBITDA
                     ($B)     LTM     NTM     LTM        NTM        NTM   Growth  Margin
[5-10 peers plus target, then statistical summary]
```

#### Additional Tables (7-15 more)
**Extract from Task 2 financial model (with Task 3 tabs):**

Use XLSX skill to extract these tables:

**DCF Assumptions Table** (Task 3 `DCF` tab)
- Open `[Company]_Financial_Model_[Date].xlsx`
- Read from DCF tab
- Extract columns A-C (Assumption, Value, Source)
- Extract first 20 rows

**DCF Sensitivity Matrix** (Task 3 `Sensitivity Analysis` tab)
- Read from Sensitivity Analysis tab
- Extract full sensitivity matrix
- WACC values as row headers
- Terminal growth rates as column headers

**Scenario Comparison Table** (Task 2 `Scenarios` tab)
- Read from Scenarios tab
- Extract full scenario table
- Metrics as row headers (Revenue, EBITDA, Margins, etc.)
- Columns: Bull, Base, Bear

**Estimates vs Consensus Table** (from Task 3 Step 3c, or build from the model + a consensus pull)
- Extract the analyst's FY+1..FY+3 revenue / EPS / margin and the matching sell-side consensus (FactSet / Bloomberg / Yahoo Finance)
- Render as a markdown table with explicit %-deltas per metric per year, plus a one-line "why the Street is wrong"
- **Each consensus figure carries a dated data-provider citation; the analyst's own estimate is labelled as an estimate and is NEVER cited as a source** (project "model is not a source" rule)
- This becomes a named **"Estimates vs Consensus"** subsection inside the Investment Thesis — it is the spine of an initiation, not an afterthought

**Other supporting tables to extract:**
- Cash flow statement
- Balance sheet highlights
- Key metrics dashboard
- Margin bridge
- Working capital schedule
- TAM sizing table
- Market share table

**Create all 12-20 tables with proper formatting.**

### Step 3: Write Quantitative Sections

These sections interpret the financial model.

**Write in this order:**

#### A. Financial Analysis (1,200-1,800 words)
- Analyze historical performance from model
- Discuss trends in revenue, margins, cash flow
- Reference specific charts and tables
- Lead with numbers

#### B. Projection Assumptions (2,000-3,000 words) ⭐ CRITICAL
- Follow detailed structure from Report Structure section above
- Must be product-by-product (8-12 points per product)
- Must be region-by-region (6-8 points per region)
- Must include margin, opex, capex, working capital assumptions
- **This section separates amateur from professional analysis**

#### C. Scenario Analysis (1,500-2,000 words) ⭐ CRITICAL
- Follow detailed structure from Report Structure section above
- Bull case: specific parameters, catalysts, probability, valuation
- Base case: most likely scenario with rationale
- Bear case: downside triggers and parameters
- Comparison table and analysis
- **Must have specific quantified parameters for each scenario**

#### D. Growth Drivers (800-1,200 words)
- 3-5 key drivers with quantified opportunities
- Timeline and milestones
- Evidence from model

#### E. Valuation Methodology (800-1,200 words)
- DCF explanation with assumptions
- Comparables rationale
- Precedent transactions (if applicable)
- Reconciliation and weighting
- Price target derivation

### Step 4: Write Synthesis Sections

**Write in this order:**

#### A. Investment Thesis (800-1,200 words)
- 3-5 key pillars
- Each pillar: 200-300 words
- Lead with key statistic
- Quantify financial impact
- Include timeline

#### B. Risk Assessment (600-900 words)
- Pull from Task 1 research document
- Organize into 4 categories
- 8-12 risks total
- Each risk: 50-100 words

#### C. Price Target & Recommendation (300-500 words)
- Final recommendation
- Price target with upside %
- Key catalysts with timeframes
- Key risks to target

#### D. Investment Summary (500-700 words) - WRITE LAST
- Page 1 content
- 3-4 detailed bullets with bold headers
- Complete synthesis of all findings
- **Write this section LAST after full analysis complete**

### Step 5: Integrate Company Content from Task 1

**CRITICAL INSTRUCTION**: Use Task 1 research document almost verbatim. DO NOT rewrite.

**The company research from Task 1 (6-8K words) is already professional, substantive analysis. Objective:**
1. **Copy markdown verbatim** — Task 1 is already in markdown; no format conversion needed
2. **Insert chart references inline** — Add `![caption](charts/chart_XX.png)` references from Task 4 throughout the text
3. **Minor style adjustments** — Ensure consistent heading levels with rest of report

**Extract these sections from Task 1 research document:**
- Company description (800-1,200 words) → **Use verbatim, insert company overview charts**
- Company history (800-1,200 words) → **Use verbatim, insert timeline chart**
- Management bios (1,000-1,400 words) → **Use verbatim, insert org chart if available**
- Products & services (700-1,000 words) → **Use verbatim, insert product portfolio charts**
- Customers & GTM (500-700 words) → **Use verbatim, insert customer segmentation charts**
- Industry overview (800-1,200 words) → **Use verbatim, insert market size evolution charts**
- Competitive landscape (700-1,000 words) → **Use verbatim, insert competitive positioning charts**
- TAM analysis (500-700 words) → **Use verbatim, insert TAM sizing charts**
- Risk assessment (600-900 words) → **Use verbatim, format as Investment Thesis & Risks section**

**Chart Integration Strategy:**
- Every 200-300 words of text → Insert 1 chart
- Company 101 section (pages 6-17) should have 8-12 charts interspersed
- Place charts immediately after the paragraph that discusses the topic
- **Result**: Dense, visually rich pages (60-80% coverage)

### Step 6: Assemble Markdown Report

**CRITICAL**: Output is a single `.md` file. Use Write/Edit tools — NOT the DOCX skill.

**Assembly Order (Most Efficient):**

#### Phase A: Create Skeleton & Reserve Page 1 Section
1. Create the .md file at `reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`
2. Write the top-of-document header block (title, date, analyst, ticker)
3. Reserve a placeholder for the Investment Summary section — fill in last after all analysis is complete
4. Add a top-level Table of Contents (markdown anchors auto-generate in renderers)

#### Phase B: Copy Task 1 Content + Insert Chart References
**This is 40-50% of the report - mostly copy/paste + chart insertion**

1. **Open the working .md file with Edit/Write**

2. **Read Task 1 markdown file**
   - Use Read tool: `reports/company/<Slug>/<Slug>_Research_Document_[Date].md` (English) or `reports/company/<Slug>/<Slug>_公司研究_[Date].md` (Chinese — produced by the `/company-research` skill)
   - Identify sections by markdown headers (`## Section Title`)

3. **Copy each section verbatim into the report, inserting chart references:**

Task 1 is already markdown — no format conversion needed. Just copy section bodies and add `![caption](charts/chart_XX.png)` lines at the documented spots. All Task 1 inline citations (`[label](url)`) carry through unchanged.

**SECTION 1: Investment Thesis & Risks**
- Add `## Investment Thesis & Risks` heading
- Copy 'Risk Assessment' section body from Task 1 verbatim (already markdown — no conversion)
- Add `### Investment Thesis` subheading
- Write new investment thesis content (800-1,200 words based on all analysis)

**SECTION 2: Company 101**
Copy each section from Task 1 verbatim — Task 1 already uses the same markdown syntax (headings, bullets, bold, inline links) the final report uses.

- **Company Overview**
  - Add `## Company Overview` heading
  - Copy 'Company Overview' section body from Task 1
  - Insert chart reference: `![图 5: 公司业务概览](charts/chart_05_company_overview.png)`

- **Company History**
  - Add `## Company History` heading
  - Copy 'Company History' section body from Task 1
  - Insert: `![图 6: 公司发展历程](charts/chart_06_company_timeline.png)`

- **Management Team**
  - Add `## Management Team` heading
  - Copy 'Management Team' section body from Task 1
  - Insert: `![图 7: 管理团队组织结构](charts/chart_07_org_structure.png)`

- **Products & Services**
  - Add `## Products & Services` heading
  - Copy first paragraph from Task 1
  - Insert: `![图 8: 产品组合](charts/chart_08_product_portfolio.png)`
  - Copy remaining paragraphs

- **Customers & Go-to-Market**
  - Add `## Customers & Go-to-Market` heading
  - Copy section from Task 1
  - Insert: `![图 9: 客户细分](charts/chart_09_customer_segments.png)`

- **Industry Overview**
  - Add `## Industry Overview` heading
  - Copy first paragraph from Task 1
  - Insert: `![图 10: 市场规模演变](charts/chart_10_market_size_evolution.png)`
  - Copy remaining paragraphs
  - Insert: `![图 11: 行业趋势](charts/chart_11_industry_trends.png)`

- **Competitive Landscape**
  - Add `## Competitive Landscape` heading
  - Copy first paragraph from Task 1
  - Insert: `![图 16: 竞争格局定位](charts/chart_16_competitive_positioning.png)`
  - Copy remaining paragraphs
  - Insert: `![图 17: 市场份额](charts/chart_17_market_share.png)`

- **Market Opportunity**
  - Add `## Market Opportunity` heading
  - Copy 'Market Opportunity' section body from Task 1
  - Insert: `![图 15: TAM 规模](charts/chart_15_TAM_sizing.png)`

**Result after Phase B**: Company 101 sections complete (~6-8K words, 8-12 chart references inserted)

**Key Point**: Task 1 already uses the target markdown format. Phase B is mostly file concatenation plus inserting one-line image references. No DOCX skill, no formatting conversion.

#### Phase C: Add Financial Analysis with Data from Task 2
**This requires NEW WRITING interpreting quantitative data**

Use the XLSX skill to read data, then Write/Edit to author the markdown:

**SECTION 3: Financial Analysis**

1. **Add `## Financial Analysis` heading**

2. **Historical Financial Analysis (1,200-1,800 words) - NEW WRITING**
   - Add `### Historical Performance` subheading
   - Use XLSX skill to open `[Company]_Financial_Model_[Date].xlsx`
   - Read `Income Statement` tab to extract historical data
   - Read `Revenue Model` tab to extract revenue trends
   - Calculate key metrics (e.g., Revenue CAGR from 2020-2024)
   - Write analytical paragraphs interpreting the trends (1,200-1,800 words)
   - Lead with specific numbers: "Revenue grew from $XXM in 2020 to $XXM in 2024, representing a XX% CAGR. This growth was driven by..."
   - Insert: `![图 2: 收入增长轨迹](charts/chart_02_revenue_growth_trajectory.png)`

3. **Create markdown table: Full Income Statement**
   - Add `#### Historical Income Statement` subheading
   - Use XLSX skill to extract the entire Income Statement tab (40-50 rows)
   - Render as a markdown pipe table with columns: line item + historical years (2020A-2024A) + projected (2025E-2029E)
   - Include all line items: Revenue, COGS, Gross Profit, Operating Expenses, EBITDA, Net Income, etc.
   - Add source line directly below the table: `*Source: [Company Financial Model](path-or-url), <date>*`

4. **Add mandatory charts and tables for Revenue breakdown:**
   - Insert: `![图 3: 按产品收入(堆叠面积)](charts/chart_03_revenue_by_product.png)` ⭐ MANDATORY
   - **Markdown table: Revenue by Product (20-30 rows)**
     - Use XLSX skill to extract from Revenue Model tab (product section, typically rows 5-35)
     - Pipe table with: Product name | historical years | projected years | % of Total | YoY Growth

   - Insert: `![图 4: 按地区收入(堆叠柱状)](charts/chart_04_revenue_by_geography.png)` ⭐ MANDATORY
   - **Markdown table: Revenue by Geography (15-20 rows)**
     - Use XLSX skill to extract from Revenue Model tab (geography section, typically rows 40-60)
     - Pipe table with: Region | historical years | projected years | % of Total

5. **Add additional financial charts:**
   - `![图 10: 毛利率演变](charts/chart_10_gross_margin_evolution.png)`
   - `![图 11: EBITDA 利润率进展](charts/chart_11_ebitda_margin_progression.png)`
   - `![图 12: 自由现金流趋势](charts/chart_12_free_cash_flow_trend.png)`

6. **Projection Assumptions (2,000-3,000 words) ⭐ CRITICAL - NEW WRITING**
   - Add `### Projection Assumptions` subheading
   - Use XLSX skill to read Scenarios tab to inform assumptions
   - Use XLSX skill to read Revenue Model tab for specific product/geography projections
   - Add `#### Revenue Assumptions by Product` subheading
   - Write detailed product-by-product assumptions (8-12 points per major product)
   - Write detailed region-by-region assumptions (6-8 points per major region)
   - Include margin, opex, capex, working capital assumptions
   - **Total: 2,000-3,000 words of specific, quantified assumptions**

7. **Scenario Analysis (1,500-2,000 words) ⭐ CRITICAL - NEW WRITING**
   - Add `### Scenario Analysis` subheading
   - Use XLSX skill to extract scenario data from Scenarios tab
   - Extract Bull/Base/Bear parameters for key metrics (2029E Revenue, EBITDA Margin, etc.)
   - Write Bull Case (500-700 words): specific parameters, catalysts, probability, valuation
   - Write Base Case (300-500 words): most likely scenario with rationale
   - Write Bear Case (500-700 words): downside triggers, parameters, probability, valuation
   - Write Scenario Comparison (200-300 words)
   - Insert: `![图 14: 情景对比](charts/chart_14_scenario_comparison.png)`
   - **Markdown table: Scenario Comparison**
     - Use XLSX skill to extract from Scenarios tab
     - Pipe table with Bull/Base/Bear columns and key metrics as rows

8. **Growth Drivers (800-1,200 words) - NEW WRITING**
   - Add `### Key Growth Drivers` subheading
   - Write 3-5 key drivers with specific quantified opportunities
   - Include timelines and milestones
   - Reference specific data from financial model

**Result after Phase C**: Financial Analysis section complete (~5-7K words, 7-8 chart references, 6-8 markdown tables)

**Key Point**: Use XLSX skill to READ data from Task 2's Excel file, use the data to inform NEW analytical writing, and render extracted tables as markdown pipe tables in the `.md` file.

#### Phase D: Add Valuation Analysis from Task 3
**Mix of copying Task 3 analysis + inserting data from Excel**

Use Read for Task 3 markdown, XLSX skill for Excel tabs, Write/Edit to author the report .md:

**SECTION 4: Valuation Analysis**

1. **Add `## Valuation Analysis` heading**

2. **Read Task 3 markdown file**
   - Use Read tool: `[Company]_Valuation_Analysis_[Date].md`
   - Identify sections by markdown headers: DCF Analysis, Comparable Companies, Price Target

3. **DCF Analysis section**
   - Add `### DCF Analysis` subheading
   - Copy 'DCF Analysis' section body from Task 3 verbatim (already markdown)
   - Insert: `![图 28: DCF 敏感性热图](charts/chart_28_dcf_sensitivity_heatmap.png)` ⭐ MANDATORY

   - **Markdown table: DCF Key Assumptions**
     - Add `#### DCF Key Assumptions` subheading
     - Use XLSX skill to open `[Company]_Financial_Model_[Date].xlsx`
     - Read DCF tab (columns A-C, first 20 rows: Assumption, Value, Source)
     - Render as a markdown pipe table — keep the `Source` column

   - **Markdown table: DCF Sensitivity Matrix**
     - Use XLSX skill to read Sensitivity Analysis tab
     - Extract full sensitivity matrix (WACC values as row labels, terminal growth as column labels)
     - Render as a markdown pipe table showing valuation at different parameter combinations

   - Insert: `![图 29: DCF 瀑布图](charts/chart_29_dcf_waterfall.png)`

4. **Comparable Companies section**
   - Add `### Comparable Companies Analysis` subheading
   - Copy 'Comparable Companies' section body from Task 3 verbatim (already markdown)

   - **Markdown table: Comparable Companies ⭐ CRITICAL**
     - Add `#### Comparable Companies` subheading
     - Use XLSX skill to read Comparable Companies tab
     - Extract full table including:
       - 5-10 peer companies plus target company
       - Statistical summary rows (Maximum, 75th Percentile, Median, 25th Percentile, Minimum)
     - Render as a markdown pipe table with all columns: Ticker, Market Cap, EV/Revenue (LTM & NTM), EV/EBITDA (LTM & NTM), P/E (NTM), Revenue Growth, EBITDA Margin
     - **Verify statistical summary rows are present**
     - Use bold (`**Median**`) on summary-row labels — markdown doesn't support row shading, so bold is the visual hierarchy you have

   - Insert: `![图 31: 同业估值倍数对比](charts/chart_31_peer_multiples_comparison.png)`

5. **Valuation Summary**
   - Insert: `![图 32: 估值橄榄球场图](charts/chart_32_valuation_football_field.png)` ⭐ MANDATORY

   - **Markdown table: Valuation Summary**
     - Use XLSX skill to read Valuation Summary tab
     - Extract valuation methods (DCF, Comps, Precedent Transactions if applicable)
     - Render as a markdown pipe table: Method | Low Case | Base Case | High Case | Weight | Weighted Value

6. **Price Target & Recommendation**
   - Add `### Price Target and Recommendation` subheading
   - Copy 'Price Target' section body from Task 3 verbatim
   - Should include: Final recommendation (BUY/HOLD/SELL), price target with % upside, key catalysts, key risks

**Result after Phase D**: Valuation section complete (~3-4K words, 5-6 chart references, 4-5 markdown tables)

**Key Point**: Use Read tool for Task 3's .md file to get written analysis (copy verbatim — it's already markdown), and use XLSX skill to READ from Task 3's Excel tabs (which were added to Task 2's model file) to create markdown pipe tables.

#### Phase E: Add Appendices & Finalize

Use Write/Edit to append the appendix sections to the .md file:

**SECTION 5: Appendices**

1. **Sources & References ⭐⭐⭐ MANDATORY — DO NOT SKIP**

   This is the single section that, when missing, most commonly degrades a report from "institutional-quality" to "opinion piece". The skill is configured to fail final delivery if this appendix is missing or has fewer than 20 entries.

   **How to build it:**

   a. **Pull sources from upstream:**
      - Open the Task 1 research document (`reports/company/<Slug>/<Slug>_Research_Document_[Date].md` or `<Slug>_公司研究_[Date].md`) — copy its `## References` block (the company-research skill produces a References section at the end of every report).
      - Open `[Company]_Valuation_Analysis_[Date].md` (Task 3) — copy its `## Sources` section.
      - Open `[Company]_Financial_Model_[Date].xlsx` — scan the `Source` column in the DCF tab and Comparable Companies tab for any sources not already captured.
      - De-duplicate.

   b. **Write the appendix in the .md file:**

   ```markdown
   ## Sources & References

   ### SEC Filings
   - [10-K FY2024](https://www.sec.gov/...) — 2025-02-20 — primary source for FY2024 financials, segment breakdown, risk factors
   - [DEF 14A 2024](https://www.sec.gov/...) — 2024-04-15 — exec compensation, board composition
   - …more entries

   ### Earnings Materials
   - [Q4 2024 Earnings Call transcript](https://seekingalpha.com/...) — 2025-02-15 — guidance, EU expansion plan
   - [Q4 2024 Earnings Presentation](https://ir.company.com/...) — 2025-02-15 — segment results, KPIs
   - …more entries

   ### Company Materials
   - [Investor Day 2024 deck](https://ir.company.com/...) — 2024-09-10 — 5-year strategy, TAM framing
   - …more entries

   ### Industry & Market Research
   - [Gartner Magic Quadrant for X](https://...) — 2024-08-22 — competitive positioning (subscription required)
   - [McKinsey Global LiDAR Market Report](https://...) — 2024-Q3 — TAM sizing, ASP trends
   - …more entries

   ### News & Trade Publications
   - [WSJ — "[Headline]"](https://www.wsj.com/...) — 2025-01-12 — context for product launch
   - …more entries

   ### Data Providers
   - [Yahoo Finance — historical price data](https://finance.yahoo.com/quote/TICKER/history) — accessed 2025-XX-XX
   - FactSet — peer trading multiples as of [date] (subscription required)
   - …more entries
   ```

   **Hard requirements:**
   - **Minimum 20 distinct entries** across all six categories combined.
   - **Every entry that has a public URL must be a markdown link** `[label](url)`, not a bare URL or plain text.
   - **Every entry has a date** in YYYY-MM-DD format (or YYYY-Qx for quarterly reports).
   - **Every entry has a 1-line description** of what it sourced in the report body.
   - Subscription-only sources are acceptable but must be labelled "(subscription required)".

   **Verify before moving on:**
   - [ ] Sources & References appendix exists as a `## Sources & References` heading
   - [ ] ≥20 entries total
   - [ ] All six category subheadings present (even if some have only 1-2 entries)
   - [ ] Test 3-5 random links by clicking them in the Claude Reports viewer — they open the correct page

2. **Additional Tables**
   - Add `## Additional Tables` heading
   - Add extended financial projections (markdown pipe tables)
   - Add detailed assumptions tables
   - Add any supporting tables that didn't fit in main sections

#### Phase F: Write the Investment Summary Section
**NOW fill in the Investment Summary placeholder reserved in Phase A — after all analysis complete**
- INITIATING COVERAGE label (e.g. `**INITIATING COVERAGE — BUY**` at the top)
- **Desk identifier / data block** (the standardized institutional Page-1 header — see `assets/report-template.md` § Layout Structure): Rating · "Initiating Coverage" · report date · EXCHANGE:TICKER (+ Reuters/Bloomberg) · current price (as-of date) · 12-month PT · implied upside/(downside)% · 52-week range · sector/industry · benchmark index level · analyst (+ CFA). For a NEUTRAL/SELL the upside field reads "Implied Downside %".
- **Key indicators (FY1) mini-table** (ROE, net debt/equity, BVPS, P/B, operating margin) + a **1m/3m/12m absolute-and-relative performance row** — each figure inline-cited (price/52-wk/performance → dated Yahoo Finance link; ratios → the underlying filing)
- The PT line in house form: `[Rating], 12-month PT [curr][X] = [multiple]× [FY+n]E [EPS/EBITDA], target date [Mon-YYYY], implying [Y]% upside/downside vs [price] ([date])`
- 3-4 detailed bullets synthesizing entire report (use `- ` bullets, each with a bolded header line and 3-5 sentences) — one bullet is the Estimates-vs-Consensus differentiated view
- Financial summary markdown table
- Insert: `![图 1: 股价走势](charts/chart_01_stock_price.png)`

#### Phase G: Verify Anchors & TOC
- Markdown renderers (including Claude Reports) auto-generate the TOC from `##`/`###` headings — no manual page numbers needed
- If you wrote a manual TOC at the top, verify the anchor slugs match each heading
- Confirm chart paths resolve relative to the .md file location

**Key formatting requirements:**
- Use `#`, `##`, `###` headings consistently — the renderer handles font/sizing
- Section dividers via `---` between major sections (optional, for readability)
- All 25-35 charts referenced via `![caption](charts/chart_XX.png)` throughout the text
- All 12-20 tables as markdown pipe tables inline with text
- **All URLs as markdown links** `[label](url)` (NOT bare URLs)
- **Visual density** - Every "page-worth" of text (~250 words) followed by a chart, table, or list

**Visual Density Strategy:**
```
Good section layout example:
## Section Header
Text paragraph (200 words) … ([source](url))
![图 N: …](charts/chart_NN.png)
Text paragraph (200 words) … ([source](url))
| col | col | col |   ← markdown table
| ... | ... | ... |
*Source: [label](url), date*
Text paragraph (200 words) … ([source](url))
![图 N+1: …](charts/chart_NN+1.png)

BAD - Avoid:
- Long stretches of pure text with no visuals
- Charts grouped at end of sections instead of inline
- Markdown tables wider than ~10 columns (renderers wrap awkwardly — split into two tables)
```

**Result**: 30-50 page worth of content (10,000-15,000 words) that is text-dense with illustrating chart references throughout

---

## File Operations Summary

**Throughout the entire assembly process, use the Read tool, XLSX skill, and Write/Edit tools:**

**Reading Input Files:**
- ✓ Use Read tool: `reports/company/<Slug>/<Slug>_Research_Document_[Date].md` (English) or `reports/company/<Slug>/<Slug>_公司研究_[Date].md` (Chinese — produced by the `/company-research` skill) - Read Task 1 research
- ✓ Use XLSX skill: Open `[Company]_Financial_Model_[Date].xlsx` and read tabs - Extract tables from Task 2/3
- ✓ Use Read tool: `[Company]_Valuation_Analysis_[Date].md` - Read Task 3 analysis
- ✓ Reference (don't read): `charts/chart_XX.png` files — embedded in the .md via `![caption](charts/chart_XX.png)` relative paths

**Writing Output File:**
- ✓ Use Write tool to create the final `.md` file
- ✓ Use Edit tool for subsequent edits to specific sections
- ✓ Markdown paragraphs come straight from input .md files (Task 1, Task 3) — copy verbatim
- ✓ Markdown pipe tables — rendered from data extracted via the XLSX skill
- ✓ Chart image references via `![caption](charts/chart_XX.png)` syntax
- ✓ Save final file as `reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`

**Do NOT manually copy/paste between formats. Use:**
1. Read tool to ingest .md files (Task 1, Task 3)
2. XLSX skill to ingest .xlsx files (Task 2 with Task 3 tabs)
3. Relative-path image references for .png files (Task 4) — no need to read them
4. Write/Edit to author the final `.md` file (Task 5 output)

This approach is efficient, reproducible, version-controllable (git diffs work line-by-line), and produces a single file viewable in the Claude Reports viewer.

### Step 7: Quality Check

**Run comprehensive verification:**

```
═══════════════════════════════════════════════════════════
REPORT QUALITY CHECKLIST
═══════════════════════════════════════════════════════════

LENGTH REQUIREMENTS:
- [ ] Report is 30-50 pages (count: ____ pages)
- [ ] Word count is 10,000-15,000 (count: ____ words)
- [ ] 25-35 charts embedded (count: ____ charts)
- [ ] 12-20 tables included (count: ____ tables)

PAGE 1 FORMAT:
- [ ] "INITIATING COVERAGE" header present
- [ ] Thesis-focused title (not generic)
- [ ] Rating box complete with all elements
- [ ] Stock price chart (Figure 1) embedded
- [ ] 3-4 detailed bullets with ■ character
- [ ] Each bullet has **bold header** + 3-5 sentences
- [ ] Financial summary table included
- [ ] Years noted as "A" (actual) and "E" (estimate)

SECTION WORD COUNTS:
- [ ] Investment Thesis: 800-1,200 words ✓
- [ ] Risk Assessment: 600-900 words ✓
- [ ] Company Description: 800-1,200 words ✓
- [ ] Management Bios: 1,000-1,400 words (300-400 per exec for 3-4 execs) ✓
- [ ] Products & Services: 700-1,000 words ✓
- [ ] Financial Analysis: 1,200-1,800 words ✓
- [ ] **Projection Assumptions: 2,000-3,000 words ✓** ⭐ CRITICAL
- [ ] **Scenario Analysis: 1,500-2,000 words ✓** ⭐ CRITICAL
- [ ] Growth Drivers: 800-1,200 words ✓
- [ ] Valuation Methodology: 800-1,200 words ✓

MANDATORY CHARTS (4 TOTAL):
- [ ] Revenue by Product (stacked area) embedded ⭐
- [ ] Revenue by Geography (stacked bar) embedded ⭐
- [ ] DCF Sensitivity (heatmap) embedded ⭐
- [ ] Valuation Football Field embedded ⭐

MANDATORY TABLES:
- [ ] Page 1 financial summary table
- [ ] Full income statement (40-50 line items)
- [ ] Revenue by product table (20-30 rows)
- [ ] Revenue by geography table (15-20 rows)
- [ ] Comparable companies table with statistical summary ⭐
- [ ] DCF assumptions table
- [ ] Scenario comparison table
- [ ] Additional 5-13 tables

CITATIONS & HYPERLINKS ⭐⭐⭐ HARD FAIL IF MISSING:
- [ ] Every figure has a source line directly under it (e.g. "Source: 10-K FY2024", "Source: FactSet, 2026-05-19")
- [ ] Every table has a source line as its final row spanning all columns
- [ ] Every substantive prose paragraph has an inline citation `(Source: <hyperlinked label>)` / `(来源: …)` at the end
- [ ] **Body has ≥150 distinct inline markdown links outside the appendix** (FAIL → STOP DELIVERY). To verify:
  ```bash
  # Count [label](url) occurrences in the body (everything before the appendix heading)
  awk '/^##? (附录|Sources & References|Appendix)/{exit} {print}' \
    "reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md" \
    | grep -oE '\[[^]]+\]\([^)]+\)' | wc -l
  ```
  If the count is under 150, the report has been assembled but not adequately cited — walk the body and add citations to every uncited substantive paragraph.
- [ ] **Every substantive paragraph (≥40 chars, not heading/list marker) carries a citation** — spot check by extracting paragraphs and checking each ends with `(来源: …)` or `(外部源: …)`. Zero unsourced substantive paragraphs allowed.
- [ ] Every page-1 investment-summary bullet has an inline citation
- [ ] Every thesis-pillar paragraph has an inline citation
- [ ] Every figure caption (`图 N:` / `Figure N:`) has appended hyperlinked source labels — chart-baked PNG source lines don't count
- [ ] Every peer comparison (Robosense / Ouster / Innoviz / Aeva / Luminar / Mobileye) links to that peer's specific Yahoo Finance ticker URL, not a generic source
- [ ] All URLs are markdown links (`[label](url)`, not bare URLs) — open the .md in the Claude Reports viewer, click 5-10 random links, confirm they work
- [ ] **Sources & References appendix exists with level-1 heading** (FAIL → STOP DELIVERY)
- [ ] **Sources & References appendix has ≥20 distinct entries** (FAIL → STOP DELIVERY)
- [ ] Sources & References has all six category sub-headings (SEC Filings / Earnings Materials / Company Materials / Industry & Market Research / News & Trade Publications / Data Providers)
- [ ] Every entry in appendix has a date and a 1-line description
- [ ] No source is labelled vaguely as "Company data" or "Industry sources" — every source names a specific document

DATA ACCURACY:
- [ ] All numbers match financial model exactly
- [ ] Revenue figures consistent across all tables/text
- [ ] Price target matches valuation analysis
- [ ] All growth rates calculated correctly
- [ ] All percentages sum to 100% where applicable

CONTENT REUSE (CRITICAL):
- [ ] Task 1 content used almost verbatim (not rewritten)
- [ ] Company 101 sections (pages 6-17) copied from Task 1 with only formatting changes
- [ ] Writing effort focused on quantitative sections (financial analysis, projections, scenarios)

VISUAL DENSITY (CRITICAL):
- [ ] Every page has BOTH text AND visuals (not pure text pages)
- [ ] Charts interspersed throughout (not grouped at end)
- [ ] Average 1+ chart per page (30-50 pages = 25-35+ charts)
- [ ] Charts appear every 200-300 words of text
- [ ] 60-80% page density achieved across entire report

FORMATTING:
- [ ] Heading hierarchy uses `#`/`##`/`###` consistently (renderer handles font/size)
- [ ] Section dividers via `---` between major sections where helpful
- [ ] Chart references use `![caption](charts/chart_XX.png)` — the `charts/` folder is co-located with the .md
- [ ] Markdown pipe tables render correctly (test in Claude Reports viewer — no broken pipes, no overly wide tables)
- [ ] No raw HTML mixed in (stick to pure markdown so it renders cleanly everywhere)

WRITING QUALITY:
- [ ] Lead with numbers (not generic statements)
- [ ] Use "vs." not "versus"
- [ ] Quantify everything
- [ ] Professional tone throughout
- [ ] No typos or grammatical errors
- [ ] Specific examples (not vague statements)

═══════════════════════════════════════════════════════════
FINAL VERIFICATION
═══════════════════════════════════════════════════════════

IF ALL ITEMS CHECKED: ✓ READY FOR DELIVERY

IF ANY ITEMS UNCHECKED: ✗ FIX BEFORE DELIVERY

═══════════════════════════════════════════════════════════
```

**IF ANY ITEM FAILS, DO NOT DELIVER. Fix before proceeding.**

---

## Writing Style Guidelines

### Lead with Numbers (CRITICAL)

✓ **CORRECT**: "Revenue increased 150% YoY to $250M in Q4 2024, driven by..."
✗ **INCORRECT**: "The company saw strong revenue growth this quarter..."

✓ **CORRECT**: "EBITDA margin expanded 500bps to 30% vs. 25% in FY2023"
✗ **INCORRECT**: "EBITDA margin expanded versus the prior year"

✓ **CORRECT**: "Market share increased 3 percentage points to 18% vs. 15% in 2023"
✗ **INCORRECT**: "Market share increased compared to last year"

✓ **CORRECT**: "Management expects 40-50% revenue growth in FY2025E"
✗ **INCORRECT**: "Management expects strong revenue growth"

### Professional Writing Standards

- **Front-load**: Most important information first
- **Data-driven**: Lead with numbers and metrics
- **Specific**: Concrete examples, not generic statements
- **Objective**: Present facts, acknowledge risks
- **Confident**: State views clearly with supporting evidence
- **Active voice**: "We estimate revenue will reach $500M"
- **Precise**: Avoid "might", "could", "possibly"

### Number Formatting

**Consistency:**
- Billions: $X.XB (e.g., "$2.5B")
- Millions: $XXXM (e.g., "$250M")
- Always specify: YoY, QoQ, CAGR
- Basis points for small margin changes: "500bps"
- Year format: "2024A" (actual), "2025E" (estimate)

### Use "vs." not "versus"
✓ **CORRECT**: "Gross margin of 65% vs. 60% in prior year"
✗ **INCORRECT**: "Gross margin of 65% versus 60%"

---

## Common Pitfalls to Avoid

**⚠️ MOST COMMON MISTAKE: TAKING SHORTCUTS DUE TO LENGTH**

Many reports fail because they use placeholders like "details would be included here" or "see model for data" instead of actually writing/extracting the content. **DO NOT DO THIS.** Write every section in full. Extract every table. Embed every chart. Use whatever tokens are needed.

**⚠️ SECOND-MOST COMMON MISTAKE: MISSING SOURCES**

Many reports fail because Phase E ("Add Appendices & Finalize") gets rushed when the context window is full, and the Sources & References appendix is skipped or built with 3-5 token placeholders. **The skill is configured to fail delivery if this happens.** A report without a Sources & References appendix is not institutional-quality research — it is an opinion piece. If the upstream Task 1 and Task 3 outputs have no sources, **stop and rerun those tasks with sources** before assembling Task 5. Do not invent sources, do not skip the appendix, do not use vague labels like "Company data".

**⚠️ THIRD-MOST COMMON MISTAKE: SOURCES ONLY IN THE APPENDIX, NOT INLINE**

Readers of an institutional research report do not flip to a back-matter Sources page to verify each claim — they expect a clickable citation right next to the claim. The user's explicit trust standard: **"for each paragraph, I hope there is citation, otherwise I don't trust the paragraph."** A report that has a 20-entry Sources & References appendix but zero links in the body fails the "where's the source for *this* number" test on every paragraph.

**The skill enforces paragraph-level citation coverage.** Body inline links are counted separately from appendix links. Delivery fails if the body has fewer than **150 distinct inline markdown links** OR if any substantive paragraph (≥40 chars, not a heading/list marker) lacks a citation.

**Embed citations while writing each phase, not as a retrofit.** As you add a paragraph in Phase B/C/D below, end every substantive sentence-ending claim with an inline markdown link to the source URL listed in the Phase E appendix:

- **Factual claim:** `([短标签](url))` — e.g. `([FY2025 6-K](https://www.sec.gov/Archives/edgar/data/1869058/...))`.
- **Paragraph mixing historical fact + forward-looking projection** (most thesis-pillar and growth-driver paragraphs): cite ONLY the external factual source(s). `([FY2025 6-K](https://...) | [Yole 新闻稿](https://...))`. **Do NOT add a "model estimate" trailer.** The analyst's own model is not a citable source — labeling it as one is functionally lying about provenance. The reader already understands forward years are analyst projections.
- **Pure forward-looking paragraph with no external anchor:** leave uncited rather than fabricate a source. If the claim is meaningful, find the baseline document the projection is built on (10-K segment data, latest earnings guidance, an industry forecast) and cite that. Standalone `(来源: 本报告模型估算)` / `(Source: our model)` is BANNED — the user's explicit rule is *"if model source, just remove it"*.
- **Figure caption — external-data chart:** append `(外部源: [Link 1](url) | [Link 2](url))` with 1-3 most relevant external sources from the per-chart mapping. Chart source lines baked into PNG images don't satisfy the click-to-verify test — the caption line must carry the clickable links.
- **Figure caption — financial-model-only chart** (DCF sensitivity heatmap, scenario comparison, valuation football field, etc.): **no citation suffix on the caption.** The chart title and the prose around it already make clear it's an analyst projection; appending `(来源: 财务模型)` would be the same lie. Leave the caption clean.

Use markdown italic for source-line de-emphasis: `*Source: [label](url), date*`. The renderer's default link color provides the visual hierarchy — no inline CSS needed.

**Where citations are NOT optional (zero tolerance):**
- Every Investment Summary bullet at the top of the report (4 bullets × ≥1 citation each)
- Every paragraph in the investment thesis pillars
- Every financial-metric statement in Historical Performance and Projection Assumptions (revenue, margin, FCF, EPS, growth rate, etc.)
- Every peer comparison (Robosense / Ouster / Innoviz / Aeva / Luminar / Mobileye / etc.) — link to that peer's Yahoo Finance ticker page
- Every risk paragraph in the Risk Assessment section
- Every market-data point in Valuation Methodology (TTM multiple, peer median, terminal growth justification)
- Every qualitative analysis paragraph (industry trend, competitive positioning, management assessment) — cite the 20-F, IR materials, or industry research that supports the framing
- **Every figure caption** (`图 N:` / `Figure N:`) — append `(外部源: …)` with markdown links **using the chart-specific source mapping** (see below)
- **Every table** — source line directly under the table as `*Source: [label](url), date*`, not plain text

**Chart caption citations require a per-chart source mapping — do NOT use a generic citation on every chart.**

Walk the chart-generation script (`build_charts_zh.py` for Chinese, `build_charts.py` for English) and read its `source_line()` calls. Each call states what data the chart actually used. Build a `CHART_SOURCES = {chart_number: [(url, label), …]}` dict from those calls, then in Phase D apply the chart-specific citation. Concrete patterns from the Hesai precedent:

- Stock-price chart → `[("https://finance.yahoo.com/quote/HSAI/history", "Yahoo HSAI 历史")]`
- Company-disclosure chart (history, products, ownership, customer concentration) → `[("https://www.sec.gov/.../20-F.htm", "FY2024 20-F")]` with section/item label (e.g. `FY2024 20-F 第 7 项` for stockholders, `FY2024 20-F 客户集中度` for top-customer table)
- Operating-metric chart (revenue, margin, opex, FCF) → `[("...20-F URL...", "FY2024 20-F"), ("...6-K URL...", "FY2025 6-K")]` for historicals
- Third-party-cited chart (TAM, attach rate, market share — Yole/Frost/IDC/Gartner) → `[("...filing URL...", "<filing> 引用 Yole"), ("...yole-press-release URL...", "Yole 新闻稿")]` — link to the primary filing where the third-party number is quoted, plus a deeper third-party URL (not the homepage)
- Financial-model-only chart (DCF, scenarios, sensitivity, football field) → `[(None, "本报告财务模型 / DCF 标签页")]` — plain-text label (no link), honest about internal sourcing
- Peer-comparison chart → list every peer's Yahoo Finance ticker URL individually

**Never link a homepage and call it a citation.** `yolegroup.com`, `frost.com`, `gartner.com` are marketing pages — clicking gets the reader nothing verifiable. Use deeper URLs: the specific report's product page (subscription-only is OK if labelled as such), the press release that announces the report, or the primary filing that quotes the number.

A 30-50 page worth of content has roughly 100-150 substantive paragraphs plus 25-35 figure captions plus 12-20 tables. Cite all of them with the right per-chart sources and you land at 150-200 inline markdown links — above the threshold and verifiable on click.

1. **Rewriting Task 1 content**: DO NOT rewrite the 6-8K words from Task 1. Use almost verbatim - just reformat and add charts. Focus writing effort on quantitative sections (projections, scenarios, valuation).
2. **Sparse pages**: Every page must have BOTH text AND visuals. Target 60-80% page density. Insert charts every 200-300 words.
3. **Grouping charts at end**: Charts must be interspersed throughout text, not grouped. Place chart immediately after paragraph discussing that topic.
4. **Writing in DOCX/Word format**: This skill outputs markdown (`.md`) — do not use the DOCX skill or generate Word documents
5. **Skipping Page 1 format**: Must follow exact institutional format
6. **Generic bullets**: Page 1 bullets need bold headers + specific data
7. **Short sections**: Must meet minimum word counts
8. **Thin assumptions**: Projection Assumptions MUST be 2,000-3,000 words with product-by-product and region-by-region detail
9. **Vague scenarios**: Must have specific parameters for Bull/Base/Bear
10. **Plain text URLs**: All citations must be clickable hyperlinks
11. **Missing statistical summary**: Comps table must have max/75th/median/25th/min
12. **Charts not embedded**: All 25-35 charts must be IN document, not just referenced
13. **Numbers don't match model**: Verify all figures against source
14. **Skipping verification**: Quality check is NOT optional

---

## Success Criteria

A successful equity research report should:

1. **Meet all length requirements**
   - 30-50 pages (MINIMUM 30)
   - 10,000-15,000 words (MINIMUM 10,000)
   - 25-35 charts embedded
   - 12-20 tables included

2. **Have properly formatted Page 1**
   - "INITIATING COVERAGE" header
   - Rating box, analyst info, chart, bullets, table

3. **Meet all section word count minimums**
   - Especially Projection Assumptions (2,000-3,000) ⭐
   - And Scenario Analysis (1,500-2,000) ⭐

4. **Include all 4 mandatory charts**
   - Revenue by product (stacked area) ⭐
   - Revenue by geography (stacked bar) ⭐
   - DCF sensitivity (heatmap) ⭐
   - Valuation football field ⭐

5. **Have management bios**
   - 300-400 words each for 3-4 key executives

6. **Include comprehensive comps table**
   - With statistical summary (max/75th/median/25th/min)

7. **Have all citations as clickable hyperlinks**
   - Test multiple links to verify they work

8. **Be professionally formatted**
   - 60-80% page density
   - No markdown syntax visible
   - Charts and tables embedded properly

9. **Have numbers matching model exactly**
   - Verify all figures against Excel model

10. **Enable informed investment decision**
    - Client should understand company, valuation, risks
    - Should be indistinguishable from JPM/GS/MS research

---

## Output Files

**Primary Deliverable:**
`reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`

**Example**: `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Initiation_Report_2024-10-27.md`

**Supporting Deliverable:**
`[Company]_Financial_Model_[Date].xlsx` (from Task 2)

**Both files should be packaged together for final delivery.**

---

## Final Note

This is the culmination of all equity research work from Tasks 1-4. The output should be:
- **Comprehensive**: 30-50 pages covering all aspects
- **Professional**: Indistinguishable from major investment bank research
- **Actionable**: Enables reader to make informed investment decision
- **Publication-ready**: Can be delivered directly to clients

**Standard**: JPMorgan, Goldman Sachs, Morgan Stanley institutional equity research.

**Quality bar**: Client-ready initiation report suitable for publication.

---

## 🔥 FINAL REMINDER: NO SHORTCUTS, NO COMPROMISES

**Use whatever tokens are needed to deliver a complete, professional report.**

This is not a draft. This is not a summary. This is not an outline. This is the **FINAL PUBLICATION-READY REPORT**.

- Write every section in full (10,000-15,000 words minimum)
- Embed every chart (all 25-35 charts throughout)
- Extract and include every table (12-20 tables minimum)
- Copy all Company 101 content from Task 1 verbatim (6-8K words)
- Write detailed projection assumptions (2,000-3,000 words)
- Write comprehensive scenario analysis (1,500-2,000 words)
- Achieve 30-50 pages minimum with 60-80% page density

**If running low on tokens, that's expected and acceptable for this task. Keep going.**

This represents the complete professional work product. Deliver institutional-quality research worthy of a $1M+ investment decision.
