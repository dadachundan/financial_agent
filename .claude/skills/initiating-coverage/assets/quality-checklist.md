# Quality Control Checklist for Initiation Reports

Before delivering an initiation report, verify all items below are complete.

## Critical Minimums - Reports Must Meet These

**CRITICAL DO NOT DELIVER IF:**
- ❌ Markdown report fewer than 10,000 words (`wc -w`) → INCOMPLETE
- ❌ Fewer than 25 embedded chart references (`![](charts/…)`) → INCOMPLETE
- ❌ Fewer than 12 comprehensive tables → INCOMPLETE
- ❌ No XLS financial model → MISSING DELIVERABLE
- ❌ Charts are text descriptions, not actual PNG/JPG files referenced from the .md → MAJOR FAILURE
- ❌ Fewer than 150 inline markdown links in the body (see SKILL.md FAIL 2) → INCOMPLETE

## Deliverables Checklist

- [ ] Markdown report file created at the slug root: `reports/company/<Slug>/[Company]_Initiation_Report_[Date].md`
- [ ] XLS financial model file created
- [ ] Both files named properly: `[Company]_Initiation_Report_[Date].md` and `[Company]_Financial_Model_[Date].xlsx`

## Markdown Report - Length & Content

**Length Verification:**
- [ ] Word count is 10,000-15,000 words (`wc -w reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`)
- [ ] If under 10,000 words: STOP and add more content

**Visual Elements:**
- [ ] 25-35 charts referenced via `![caption](charts/…)` (count them: _____ charts)
- [ ] All charts are actual PNG/JPG image files on disk in `charts/` (NOT text descriptions)
- [ ] 12-20 comprehensive tables included (count them: _____ tables)
- [ ] Charts and tables interspersed throughout, not grouped at end

**Chart Requirements:**
- [ ] Revenue by product chart: Stacked Area format ✓
- [ ] Revenue by geography chart: Stacked Bar format ✓
- [ ] DCF sensitivity: 2-way Heat Map with color coding ✓
- [ ] Valuation football field: Horizontal bar chart ✓
- [ ] All other charts are actual image files ✓

**Table Requirements:**
- [ ] Full Income Statement (40-50 rows) with 5 years historical + 5 years projected
- [ ] Full Cash Flow Statement (30-40 rows)
- [ ] Full Balance Sheet (35-45 rows)
- [ ] Revenue by product table (20-30 rows)
- [ ] Revenue by geography table (15-20 rows)
- [ ] Revenue by channel table (10-15 rows)
- [ ] Comparable companies table with statistical summary (max/75th/median/25th/min)
- [ ] DCF calculation table (30-40 rows)
- [ ] WACC calculation table (8-10 rows)
- [ ] Two sensitivity tables
- [ ] 2-3 additional financial/competitive tables

## Markdown Report - Structure

**Page 1 Requirements:**
- [ ] "INITIATING COVERAGE" header present (NOT "Company Update")
- [ ] Thesis-focused title (NOT event-driven like "Strong Q4 Results")
- [ ] Rating box with rating, price, target price, 52-week range, market cap, EV
- [ ] 3-4 paragraph-length bullets with ■ character and bold headers
- [ ] Financial & valuation metrics table with 2-3 years historical, 2 years projected
- [ ] Table shows "A" suffix for actuals, "E" suffix for estimates
- [ ] Source lines on all visuals

**Content Sections:**
- [ ] Table of Contents (Page 2)
- [ ] Investment Thesis & Risks (3-5 pages)
- [ ] Company Overview (6-12 pages) including:
  - [ ] Company description
  - [ ] History and milestones
  - [ ] Management bios (300-400 words EACH for 3-4 executives)
  - [ ] Products/services detail
  - [ ] Competitive landscape
- [ ] Financial Analysis & Projections (10-15 pages)
- [ ] Valuation Analysis (8-12 pages)
- [ ] Assumptions section (2,000-3,000 words documenting ALL projection assumptions)
- [ ] Scenario Analysis (1,500-2,000 words with Bull/Base/Bear parameters)
- [ ] Appendices including Data Sources & References page

## Markdown Report - Formatting

**Figure & Table Formatting:**
- [ ] Every figure has a caption line: `*图 N: [title].*` / `*Figure N: [title].*`
- [ ] Every figure has a hyperlinked source line below: `*Source: [label](url), [date]*` (per SKILL.md Citation Standards)
- [ ] Sequential figure numbering (Figure 1, 2, 3... no gaps)
- [ ] Every table is a proper markdown table with a header row
- [ ] Every table has a hyperlinked source line directly under it
- [ ] All years use "A" for actual, "E" for estimate notation

**Professional Formatting:**
- [ ] Consistent heading hierarchy (`#` / `##` / `###`) throughout
- [ ] Dense layout: text, charts, and tables interleaved — roughly one visual per 200-300 words
- [ ] Renders cleanly in the Claude Reports viewer (relative `charts/` image paths resolve)

## Citations & Sources ⭐⭐⭐ CRITICAL

**Source Attribution:**
- [ ] Every figure has specific source with document name and date
- [ ] Every table has specific source with document reference
- [ ] Key statistics throughout text have footnotes with sources
- [ ] NOT just generic "Company data" - must be specific

**Hyperlinks:** ⭐⭐⭐ MANDATORY
- [ ] ALL URLs are CLICKABLE HYPERLINKS (not plain text)
- [ ] SEC filings hyperlinked to EDGAR viewer
- [ ] Earnings transcripts hyperlinked (Seeking Alpha or company IR)
- [ ] Press releases hyperlinked to company IR page
- [ ] Presentations hyperlinked to PDF URLs
- [ ] Industry reports hyperlinked (if publicly available)
- [ ] No data provider cited that was not actually accessed (no FactSet / Bloomberg / CapitalIQ citations in this environment — use dated Yahoo Finance / SEC filing links)
- [ ] No raw URLs displayed anywhere - all formatted as `[label](url)` markdown links
- [ ] HTTP-check sample hyperlinks (200 OK with a real-browser User-Agent, per the project link-validation rule)

**Reference Page:**
- [ ] "Data Sources & References" page at end of report
- [ ] Lists ALL sources used in report
- [ ] Sources organized by category (SEC Filings, Earnings Transcripts, etc.)
- [ ] Every source has date
- [ ] Every source has clickable hyperlink (where applicable)

## XLS Financial Model - Structure

**File Structure:**
- [ ] 15+ tabs in Excel workbook
- [ ] Tabs include: Executive Summary, Assumptions, Historical Financials, Revenue Model, Operating Expenses, Income Statement, Balance Sheet, Cash Flow, Supporting Schedules, DCF Valuation, Comps Analysis, Precedent Transactions, Scenarios, Sensitivity Analysis, Charts

**Formatting:**
- [ ] Blue text for hardcoded inputs
- [ ] Black text for formulas
- [ ] Green text for links to other sheets
- [ ] Professional formatting with borders and shading
- [ ] Clear section headers and labels

**Model Functionality:**
- [ ] All numbers flow (change assumption → entire model updates)
- [ ] DCF links to assumptions and projections
- [ ] No circular references or errors
- [ ] All important cells/ranges are named
- [ ] Sensitivity tables work dynamically

## XLS Financial Model - Content

**Projections:**
- [ ] 3-5 years historical data
- [ ] 5 years forward projections (FY+1 through FY+5)
- [ ] Revenue broken down by product, geography, channel
- [ ] Full P&L with 40-50 line items
- [ ] Full cash flow with 30-40 line items
- [ ] Full balance sheet with 35-45 line items

**Valuation:**
- [ ] Complete DCF model with all calculations shown
- [ ] WACC calculation with all components
- [ ] Terminal value calculation
- [ ] Comparable companies analysis (5-10 companies)
- [ ] Precedent transactions analysis (5-10 deals)
- [ ] Scenario analysis (Bull/Base/Bear)
- [ ] Two sensitivity tables

## Cross-File Consistency

**CRITICAL**: Numbers must match EXACTLY between the .md report and XLS model

- [ ] Revenue numbers match across both files
- [ ] EPS numbers match across both files
- [ ] Margin percentages match across both files
- [ ] Valuation numbers match across both files
- [ ] Price target matches across both files
- [ ] All projected years match across both files

**Verification Method**: Spot check 10-15 key numbers between the .md report and XLS model.

## Content Quality

**Investment Thesis:**
- [ ] 3-5 clear thesis pillars
- [ ] Each pillar supported with specific data and quantification
- [ ] Financial impact quantified for each pillar
- [ ] Catalysts identified with timelines

**Analysis Depth:**
- [ ] Comprehensive business model analysis
- [ ] Detailed competitive assessment
- [ ] 3-5 year financial trends analyzed
- [ ] 8-12 risks identified and quantified
- [ ] Management team analyzed (300-400 words per executive)

**Assumptions:**
- [ ] 2,000-3,000 words documenting ALL assumptions
- [ ] Revenue growth assumptions by category/geography
- [ ] Margin assumptions with bridge showing drivers
- [ ] Working capital assumptions
- [ ] CapEx assumptions
- [ ] Each assumption has specific quantification

**Scenarios:**
- [ ] 1,500-2,000 words on scenario analysis
- [ ] Bull case with specific parameters and catalysts
- [ ] Base case with detailed rationale
- [ ] Bear case with specific triggers
- [ ] Probability assessments for each scenario

## Writing Quality

**Style:**
- [ ] Lead with numbers ("Revenue grew 15% to $1.2B" not "Strong revenue")
- [ ] Use "vs." not "versus"
- [ ] Be direct and concise
- [ ] Professional institutional tone throughout
- [ ] No informal language

**Accuracy:**
- [ ] No typos in ticker symbol
- [ ] No typos in company name
- [ ] All dates accurate
- [ ] All calculations verified
- [ ] Charts match text descriptions
- [ ] All numbers properly formatted ($ signs, % signs, commas)

## Pre-Delivery Final Check

Run through this quick final review:

1. **Deliverables**: Both .md report and XLS model created ✓
2. **Length**: 10,000-15,000 words (`wc -w`) ✓
3. **Charts**: 25-35 actual PNG/JPG files referenced via `![](charts/…)` ✓
4. **Tables**: 12-20 comprehensive tables included ✓
5. **Links**: ≥150 inline markdown links in the body; sample HTTP-checked ✓
6. **Cross-check**: Spot check 10 numbers match between .md and XLS ✓
7. **Page 1**: "INITIATING COVERAGE" header present ✓
8. **Verification log**: `<details>`-folded log appended after Sources & References ✓

If ANY item fails, DO NOT DELIVER. Go back and fix.

## Actual Count Verification

**Before delivery, fill in actual counts:**

Markdown Report:
- Word count: _____ words (MUST BE 10,000-15,000 — `wc -w`)
- Chart count: _____ `![](charts/…)` references (MUST BE 25-35)
- Table count: _____ tables (MUST BE 12-20)
- Inline body links: _____ (MUST BE ≥150)

XLS Model:
- Tab count: _____ tabs (SHOULD BE 15+)
- Model years: _____ historical + _____ projected

If any count is below minimum, STOP and add content before delivery.
