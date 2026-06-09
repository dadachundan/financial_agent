---
name: initiating-coverage
description: Create institutional-quality equity research initiation reports through a 5-task workflow. Tasks must be executed individually with verified prerequisites - (1) company research, (2) financial modeling, (3) valuation analysis, (4) chart generation, (5) final report assembly. Each task produces specific deliverables (markdown docs, Excel models, charts, or a final markdown report). Tasks 3-5 have dependencies on earlier tasks.
---

# Initiating Coverage

Create institutional-quality equity research initiation reports through a structured 5-task workflow. Each task must be executed separately with verified inputs.

## Overview

This skill produces comprehensive first-time coverage reports following institutional standards (JPMorgan, Goldman Sachs, Morgan Stanley format). Tasks are executed individually, each verifying prerequisites before proceeding.

**Default Font**: Times New Roman throughout all documents (unless user specifies otherwise).

---

## ⚠️ CRITICAL: One Task at a Time

**THIS SKILL OPERATES IN SINGLE-TASK MODE ONLY.**

### If User Requests Full Pipeline

When user requests:
- "Create a coverage initiation report for [Company]"
- "Write an initiation report for [Company]"
- "Do the entire equity research process for [Company]"
- "Complete all 5 tasks for [Company]"
- Any request that implies running multiple tasks or the entire workflow

**REQUIRED RESPONSE:**

1. **Ask which specific task to perform:**
   ```
   I can help you create an equity research initiation report for [Company].
   This involves 5 separate tasks that need to be completed individually:

   1. Company Research - Research business, management, industry
   2. Financial Modeling - Build projection model
   3. Valuation Analysis - DCF and comparable companies
   4. Chart Generation - Create 25-35 charts
   5. Report Assembly - Compile final report

   Which task would you like to start with?
   ```

2. **When user explicitly requests all tasks together:**
   ```
   I understand you'd like to complete the entire initiation report pipeline.
   Currently, this skill supports executing one task at a time, which allows
   for better quality control and review at each stage.

   We're working on a seamless end-to-end workflow that will make this process
   more automated, but for now, we'll need to complete each task separately.

   Would you like to start with Task 1 (Company Research)?
   ```

3. **Never automatically assume which task to start** - always ask user to confirm.

4. **Never execute multiple tasks in sequence** - complete one task, deliver outputs, then wait for next user request.

### Task Execution Rules

- ✅ Execute exactly ONE task per user request
- ✅ Always verify prerequisites before starting a task
- ✅ Deliver task outputs and confirm completion
- ✅ Wait for user to explicitly request the next task
- ❌ Never chain multiple tasks together automatically
- ❌ Never assume user wants to proceed to next task
- ❌ Never execute Tasks 3-5 without verifying required inputs exist

### ⚠️ Deliverables Policy: NO SHORTCUTS

**DELIVER ONLY THE SPECIFIED OUTPUTS. DO NOT CREATE EXTRA DOCUMENTS.**

Each task specifies exact deliverables. Do NOT create:
- ❌ "Completion summaries"
- ❌ "Executive summaries"
- ❌ "Quick reference guides"
- ❌ "Next steps documents"
- ❌ "Task completion reports"
- ❌ Any other "helpful" documentation not explicitly specified

**Why**: These extras waste context and are not part of the professional workflow.

**What TO deliver**:
- ✅ Task 1: Research document (.md) — **NOTHING ELSE**
- ✅ Task 2: Financial model (.xlsx) — **NOTHING ELSE**
- ✅ Task 3: Valuation analysis (.md) + Excel tabs added to Task 2 file — **NOTHING ELSE**
- ✅ Task 4: Charts zip file (.zip) — **NOTHING ELSE**
- ✅ Task 5: Final report (.md) — **NOTHING ELSE**

**If a deliverable is not listed above, DO NOT CREATE IT.**

---

## Task Selection

Select which task to execute:

| Task | Name | Prerequisites | Output |
|------|------|--------------|--------|
| **1** | Company Research | Company name/ticker | 6-8K word document |
| **2** | Financial Modeling | 10-K or financials access | Excel model (6 tabs) |
| **3** | Valuation Analysis | Financial model (Task 2) | Valuation + price target |
| **4** | Chart Generation | Tasks 1, 2, 3 + external data | 25-35 PNG/JPG charts |
| **5** | Report Assembly | ALL previous tasks (1-4) | 30-50 page markdown report |

---

## How to Use This Skill

### User Request Patterns and Responses

**Pattern 1: User specifies a specific task**
```
User: "Use initiating-coverage, Task 1 for Tesla"
Response: ✅ Execute Task 1 immediately
```

**Pattern 2: User asks for "initiation report" or "full pipeline"**
```
User: "Create a coverage initiation report for Tesla"
Response: ❌ DO NOT start any task automatically
         ✅ Ask which task to start with (see template above)
```

**Pattern 3: User wants to do "all tasks" or "entire workflow"**
```
User: "I want to complete all 5 tasks for Tesla"
Response: ❌ DO NOT chain tasks together
         ✅ Explain one-at-a-time limitation (see template above)
         ✅ Ask if they want to start with Task 1
```

### Correct Usage Examples

**Executing a single task:**
```
"Use initiating-coverage skill, Task 1 for Tesla"
"Do Task 2 of initiating-coverage for Tesla"
"Run Task 3 for Tesla using the initiating-coverage skill"
```

**Completing full report (requires 5 separate requests):**
```
Request 1: "Do Task 1 for Tesla" → Complete → Deliver outputs
Request 2: "Do Task 2 for Tesla" → Complete → Deliver outputs
Request 3: "Do Task 3 for Tesla" → Complete → Deliver outputs
Request 4: "Do Task 4 for Tesla" → Complete → Deliver outputs
Request 5: "Do Task 5 for Tesla" → Complete → Deliver outputs
```

### Task Execution Order

For a complete initiation report, tasks must be executed in separate user requests following this order:

```
Request 1: Task 1 - Company Research (independent)
           ↓ [User reviews outputs and requests next task]
Request 2: Task 2 - Financial Modeling (independent)
           ↓ [User reviews outputs and requests next task]
Request 3: Task 3 - Valuation Analysis (requires Task 2 output)
           ↓ [User reviews outputs and requests next task]
Request 4: Task 4 - Chart Generation (requires Tasks 2 & 3 outputs)
           ↓ [User reviews outputs and requests next task]
Request 5: Task 5 - Report Assembly (requires ALL previous task outputs)
```

**Note**: Tasks 1 and 2 can be run in any order. Tasks 3-5 have strict dependencies and must verify inputs before proceeding.

---

## Task 1: Company Research

**Purpose**: Research company's business, management, competitive position, industry, and risks.

**Prerequisites**: ✅ None (fully independent)
- Company name or ticker symbol

**This task is delegated to the top-level `company-research` skill.** It already produces a 6,000–10,000 word document with mandatory inline citations, a References block, and per-section sourcing — exactly what Tasks 4 and 5 need. Do not duplicate that workflow here.

### Step 1 — Prerequisite check: does a research doc already exist?

Before running `/company-research`, look in `reports/company/` for an existing document for this ticker. The folder slug is `<Company>_<EXCHANGE><CODE>` (e.g. `Hesai_NASDAQ_HSAI`, `BYD_SZSE002594`, `Anpeilong`).

```bash
ls reports/company/ | grep -i "<ticker-or-name>"
# If a folder matches:
ls "reports/company/<Slug>/" | grep -E "_Research_Document_|_公司研究_"
```

**Decision tree:**

- **User explicitly asked to re-generate Task 1** (e.g. "re-run Task 1", "regenerate the research", "fresh research doc"): always re-run `/company-research`, regardless of what exists on disk. This override beats every rule below.
- **A matching `*_Research_Document_*.md` or `*_公司研究_*.md` exists and is ≤ 1 month old** (compare report date in filename, or file mtime if the filename date is ambiguous): ✅ Reuse it as Task 1's output. Note the path. Confirm with the user, then proceed (or wait for the user to request Task 2).
- **A file exists but is > 1 month old, OR no file exists:** Run `/company-research` to produce a fresh document. Tell the user:
  > "Existing research at `reports/company/<Slug>/` is > 1 month old (or missing). Running `/company-research <Company>` to refresh — that skill produces the 6,000–10,000 word document Task 1 expects. After it finishes, I'll register the output."

  Then invoke the skill (e.g. via the Skill tool with `skill: "company-research"`, `args: "<Company or ticker>"`).

### Step 2 — Register the output

Once a research document exists at `reports/company/<Slug>/<Slug>_Research_Document_<Date>.md` (or `_公司研究_` for Chinese), Task 1 is complete. Record the file path so Tasks 4 and 5 can read it.

**Output**: Company Research Document (6,000–10,000 words, produced by `/company-research`)
- Company overview & history, management bios, products & services, customers & GTM, industry overview, competitive landscape, TAM, risks, References block — see the company-research skill's `references/report_structure.md` for the full spec.

**File path**: `reports/company/<Slug>/<Slug>_Research_Document_<Date>.md` (English) or `reports/company/<Slug>/<Slug>_公司研究_<Date>.md` (Chinese).

**⚠️ DELIVER ONLY THIS 1 FILE. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:** the company-research skill enforces full word count, full bios, full competitor list, full risk taxonomy, and mandatory inline citations + References. Do not bypass that skill by writing a shorter research doc inline.

**Verification before proceeding to Task 4 or 5**: the registered research document file actually exists on disk at the path above and contains a References block.

---

## Task 2: Financial Modeling

**Purpose**: Extract historical financials and build comprehensive Excel financial model with projections and scenarios.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Access to company financial data
  - For public companies: Latest 10-K from SEC EDGAR
  - For private companies: Financial statements or available estimates
  - OR: Pre-extracted historical financials provided by user
- **Optional**: Company research (Task 1) for business context

**Input Verification**:
```
BEFORE STARTING - Select approach:

Option A: Extract financials (most common)
- [ ] Have access to 10-K or financial statements?
- [ ] Ready to extract 3-5 years of data?

Option B: User provided pre-extracted financials
- [ ] Historical financials file received?
- [ ] Contains income statement, cash flow, balance sheet (3-5 years)?

Optional:
- [ ] Company research (Task 1) complete for context?
```

**Process**:
1. Verify access to financial data
2. Load detailed instructions from references/task2-financial-modeling.md
3. **Step 1**: Extract historical financials (if needed)
4. **Step 2+**: Build projection model with 6 essential tabs
5. Deliver Excel model

**Output**: Excel Financial Model (.xlsx)
- 6 essential tabs:
  1. **Revenue Model** - Product breakdown (20-30 rows) + Geography breakdown (15-20 rows)
  2. **Income Statement** - Full P&L with 40-50 line items, historical (3-5 years) + projected (5 years)
  3. **Cash Flow Statement** - Operating/Investing/Financing activities, historical + projected
  4. **Balance Sheet** - Assets/Liabilities/Equity, historical + projected
  5. **Scenarios** - Bull/Base/Bear comparison table
  6. **DCF Inputs** - Prepared for Task 3 valuation

**File name**: `[Company]_Financial_Model_[Date].xlsx` — written to `reports/company/<Slug>/model/`.

### Update-in-place rule — at most one financial model per company

Before writing, check `reports/company/<Slug>/model/` for an existing model and update it in place rather than creating a parallel dated copy.

```bash
ls "reports/company/<Slug>/model/" 2>/dev/null | grep -E "_Financial_Model_.*\.xlsx$"
```

- **Exactly one match** → open that workbook (XLSX skill) and edit its tabs in place. Keep the filename even if its embedded date is stale — git history records the actual revision date. Update the cover/header cell that displays "As of <date>" to today.
- **Multiple matches** (legacy state) → update the most recent by mtime, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new workbook with today's date in the filename.

Task 3 adds tabs to this same workbook, so updating in place keeps Task 2 and Task 3 outputs co-located.

**⚠️ DELIVER ONLY THIS 1 FILE. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ If extracting financials: Extract ALL line items from 3 financial statements (3-5 years)
- ✅ Build ALL 6 projection tabs completely with full detail
- ✅ Create detailed revenue model with 20-30 product rows AND 15-20 geography rows
- ✅ Build complete income statement with 40-50 line items (not abbreviated)
- ✅ Include full cash flow statement and balance sheet with all line items
- ✅ Complete ALL three scenarios (Bull/Base/Bear) with different parameters
- ❌ Do not create simplified/abbreviated versions
- ❌ Do not skip any of the 6 essential tabs
- ❌ Do not skip historical financials extraction if needed

**Verification before proceeding to Task 3**:
- [ ] Historical financials extracted (if needed) or provided
- [ ] Excel file created and can be opened
- [ ] Model has all 6 essential tabs (Revenue Model, Income Statement, Cash Flow, Balance Sheet, Scenarios, DCF Inputs)
- [ ] Historical data (3-5 years) incorporated
- [ ] Projections complete (5 years forward)
- [ ] Scenarios complete (Bull/Base/Bear)

---

## Task 3: Valuation Analysis

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

**Input Verification**:
```
BEFORE STARTING:
- [ ] Task 2 complete? (Financial model exists)
- [ ] Model file path/location known?
- [ ] Can access projected financials from model?

Required from model:
- [ ] Projected FCF (5 years)
- [ ] Revenue projections
- [ ] EBITDA projections
- [ ] Terminal year metrics
```

**Process**:
1. Verify financial model is accessible
2. Load detailed instructions from references/task3-valuation.md
3. Execute valuation workflow
4. Deliver valuation analysis

**Output**: Valuation Analysis (4-6 pages + Excel tabs)
- DCF analysis with sensitivity tables
- Comparable companies (5-10 peers with statistical summary)
- Precedent transactions (if applicable)
- Valuation football field
- **Price target**: $XX.XX
- **Recommendation**: BUY/HOLD/SELL
- **Upside**: XX%
- Key catalysts (3-5)

**Files**:
- `[Company]_Valuation_Analysis_[Date].md` (written analysis document) — saved under `reports/company/<Slug>/valuation/`
- Excel tabs added to `[Company]_Financial_Model_[Date].xlsx` (from Task 2)
  - DCF tab with calculations
  - Sensitivity analysis tab
  - Comparable companies tab
  - Valuation summary tab

### Update-in-place rule — at most one valuation analysis per company

Before writing, check `reports/company/<Slug>/valuation/` for an existing analysis and update it in place rather than creating a parallel dated copy.

```bash
ls "reports/company/<Slug>/valuation/" 2>/dev/null | grep -E "_Valuation_Analysis_.*\.md$"
```

- **Exactly one match** → overwrite it at the same path. Keep the filename even if its embedded date is stale — git history records the actual revision date. Update the document's internal date / "as of" header to today.
- **Multiple matches** (legacy state) → update the most recent by mtime, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new file using today's date.

The Excel tabs (DCF, Sensitivity, Comps, Valuation Summary) are added to the **existing** workbook from Task 2 — not a new file — so the update-in-place rule for the model (Task 2) automatically covers them too.

**⚠️ DELIVER ONLY: 1 markdown file + 4 tabs added to existing Excel. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ Complete full DCF analysis with sensitivity matrix (not simplified)
- ✅ Analyze ALL 5-10 comparable companies with full data
- ✅ Include statistical summary in comps table (max/75th/median/25th/min)
- ✅ Create complete sensitivity analysis tab with multiple WACC and terminal growth scenarios
- ✅ Write full 4-6 pages of valuation analysis (not abbreviated)
- ✅ Research and justify price target with specific methodology
- ❌ Do not skip comparable company analysis
- ❌ Do not create simplified DCF without sensitivity

**⚠️ SOURCE CITATIONS ARE MANDATORY** (see Citation Standards below):
- ✅ Every peer multiple in the comps table has a source column (e.g. "FactSet, 2026-05-19" or "10-K FY2024")
- ✅ Every macro/market assumption (risk-free rate, ERP, beta, terminal growth) is cited inline
- ✅ The Excel `Comparable Companies` tab includes a `Source` column per row
- ✅ The Excel `DCF` tab's assumptions table includes a `Source` column per row (already required by Task 2 template)
- ✅ The markdown ends with a **Sources** subsection listing every source used

**Verification before proceeding to Task 4**:
- [ ] Price target determined
- [ ] Valuation uses multiple methods (DCF + Comps minimum)
- [ ] DCF sensitivity table complete
- [ ] Comparable companies table includes statistical summary

---

## Task 4: Chart Generation

**Purpose**: Generate 25-35 professional financial charts for the report.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Company research from Task 1
  - Company history and milestones (for timeline charts)
  - Management team and org structure (for org charts)
  - Product portfolio (for product charts)
  - Customer segmentation (for customer charts)
  - Competitive landscape (for competitive charts)
  - TAM analysis (for market size charts)
- **Required**: Financial model from Task 2 (with Task 3 valuation tabs added)
  - Revenue by product/geography data (Task 2 tabs)
  - Margin trends (Task 2 tabs)
  - Scenario comparison data (Task 2 tabs)
  - DCF sensitivity table (Task 3 tab in same Excel file)
  - Comparable companies data (Task 3 tab in same Excel file)
  - Valuation ranges (Task 3 tab in same Excel file)
- **Required**: External market data
  - Historical stock price data (Yahoo Finance, Bloomberg, etc.)
  - Historical valuation multiples (for historical trend charts)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASKS 1, 2, AND 3 ARE COMPLETE**

This task requires outputs from all three previous tasks. Starting without them will result in incomplete charts.

**IF ANY OF TASKS 1, 2, OR 3 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (for 9 charts)
- Task 2: Financial model with all 6 tabs (for 8 charts)
- Task 3: Valuation tabs added to the model (for 6 charts)
- External data access (for 2 charts)

Do not attempt to create placeholder charts or skip charts due to missing data.

**Input Verification**:
```
BEFORE STARTING:
- [ ] Task 1 complete? (Company research exists)
- [ ] Task 2 complete? (Financial model exists)
- [ ] Task 3 complete? (Valuation analysis exists)
- [ ] Can access external market data sources?

Required from Task 1:
- [ ] Company history and milestones (for charts 05, 06)
- [ ] Management team structure (for chart 07)
- [ ] Product portfolio details (for chart 08)
- [ ] Customer segmentation data (for chart 09)
- [ ] Competitive landscape analysis (for charts 16, 17, 18)
- [ ] TAM sizing and market data (for chart 15)

Required from Task 2:
- [ ] Revenue by product (historical + projected) - for chart 03 ⭐
- [ ] Revenue by geography (historical + projected) - for chart 04 ⭐
- [ ] Income statement with margins (for charts 02, 10, 11)
- [ ] Cash flow statement (for chart 12)
- [ ] Scenario comparison data (for chart 14)

Required from Task 3:
- [ ] DCF sensitivity matrix - for chart 28 ⭐
- [ ] DCF components (for chart 29)
- [ ] Comparable companies data (for charts 30, 31)
- [ ] Valuation ranges - for chart 32 ⭐

Required from External Sources:
- [ ] Historical stock price data (for chart 01)
- [ ] Historical valuation multiples (for chart 34)
```

**Process**:
1. Verify model and valuation outputs are accessible
2. Load detailed instructions from references/task4-chart-generation.md
3. Execute chart generation workflow
4. Package all charts into a zip file
5. Deliver zip file

**Output**: 25-35 Professional Chart Files (PNG/JPG, 300 DPI) packaged in zip

**4 MANDATORY Charts** (must be present) ⭐:
- chart_03: Revenue by product (stacked area)
- chart_04: Revenue by geography (stacked bar)
- chart_28: DCF sensitivity (2-way heatmap)
- chart_32: Valuation football field (horizontal bars)

**25 REQUIRED Charts** (specific list):
- Investment Summary: chart_01
- Financial Performance: charts 02, 03⭐, 04⭐, 10, 11, 12, 14
- Company 101: charts 05, 06, 07, 08, 09, 15, 16
- Competitive/Market: charts 17, 18
- Scenario Analysis: chart 13
- Valuation: charts 28⭐, 29, 30, 31, 32⭐, 33, 34

**10 OPTIONAL Charts** (for 26-35 range):
- charts 19-27, 35 (customer acquisition, unit economics, product roadmap, etc.)

**IMPORTANT**: Task 5 embeds ALL charts created (25-35) for visual density (1 chart per 200-300 words).

**File naming**: `chart_01_description.png`, `chart_02_description.png`, etc.

**Deliverable**: `[Company]_Charts_[Date].zip` containing all 25-35 chart files + chart_index.txt

**⚠️ DELIVER ONLY THIS 1 ZIP FILE. NO completion summaries, no separate chart lists, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ Create ALL 25 required charts minimum (specific list provided in task4-chart-generation.md)
- ✅ Include ALL 4 mandatory charts:
  - chart_03: Revenue by product (stacked area) ⭐
  - chart_04: Revenue by geography (stacked bar) ⭐
  - chart_28: DCF sensitivity (heatmap) ⭐
  - chart_32: Valuation football field ⭐
- ✅ Optional: Add 1-10 more charts to reach 26-35 total for greater visual density
- ✅ Generate professional-quality charts at 300 DPI (not low-res placeholders)
- ✅ Create unique, well-formatted charts for each visualization
- ✅ Package all charts in zip file with chart index
- ❌ Do not create only 10-15 charts (minimum is 25)
- ❌ Do not skip any of the 4 mandatory charts
- ❌ Do not use low-quality/placeholder images

**Verification before proceeding to Task 5**:
- [ ] Minimum 25 chart files created (required)
- [ ] All 4 mandatory charts present:
  - [ ] chart_03: Revenue by product ⭐
  - [ ] chart_04: Revenue by geography ⭐
  - [ ] chart_28: DCF sensitivity ⭐
  - [ ] chart_32: Valuation football field ⭐
- [ ] All charts open and display correctly
- [ ] Charts saved at 300 DPI (print quality)
- [ ] Chart index created listing all files with categories
- [ ] All charts packaged in zip file
- [ ] File naming follows convention: chart_##_description.png

---

## Task 5: Report Assembly

**Purpose**: Write and assemble the comprehensive final markdown report.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Company research from Task 1
  - All 6-8K words of content
  - Management bios
  - Competitive analysis
  - Risk assessment
- **Required**: Financial model from Task 2
  - Excel workbook
  - All projections and scenarios
- **Required**: Valuation analysis from Task 3
  - Price target and recommendation
  - DCF, comps, precedent transactions
  - All valuation data
- **Required**: Chart files from Task 4
  - Zip file containing all 25-35 PNG/JPG files
  - Chart index included in zip

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS ALL TASKS 1-4 ARE COMPLETE**

This is the final assembly task. It cannot be completed without all previous work products.

**IF ANY OF TASKS 1, 2, 3, OR 4 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (6-8K words)
- Task 2: Financial model with all 6 tabs
- Task 3: Valuation analysis with price target and recommendation
- Task 4: Charts zip file with 25-35 charts

Do not attempt to create placeholder content, substitute missing sections, or assemble an incomplete report. The report requires ALL inputs to be publication-ready.

**Input Verification**:
```
BEFORE STARTING - ALL TASKS MUST BE COMPLETE:

Task 1 Verification:
- [ ] Company research document exists? (6-8K words)
- [ ] Management bios complete? (300-400 words × 3-4 execs)
- [ ] Competitive analysis complete? (5-10 competitors)
- [ ] Risk assessment complete? (8-12 risks)

Task 2 Verification:
- [ ] Financial model exists and can be opened?
- [ ] Model has projections (5 years)?
- [ ] Scenarios exist (Bull/Base/Bear)?

Task 3 Verification:
- [ ] Valuation analysis complete?
- [ ] Price target determined?
- [ ] Recommendation set? (BUY/HOLD/SELL)
- [ ] DCF and comps complete?

Task 4 Verification:
- [ ] Chart zip file exists?
- [ ] Can extract/access all 25-35 chart files from zip?
- [ ] All 4 mandatory charts present?
  - [ ] Revenue by product (stacked area)
  - [ ] Revenue by geography (stacked bar)
  - [ ] DCF sensitivity (heatmap)
  - [ ] Valuation football field
- [ ] Chart files accessible and can be opened?

IF ANY VERIFICATION FAILS: Stop and complete missing task first.
```

**Process**:
1. **CRITICAL**: Verify ALL prerequisites before starting
2. Load detailed instructions from references/task5-report-assembly.md
3. Execute report assembly workflow:
   - **Use Write/Edit tools** to author the final `.md` file directly
   - **Use XLSX skill** to read Excel data from Task 2/3
   - **Use Read tool** to read Task 1 and Task 3 markdown files
   - Read Task 1 .md file → Copy sections into the report → Insert chart references inline
   - Read Task 2 .xlsx file → Extract tables → Write quantitative analysis as markdown tables
   - Read Task 3 .md file + Excel tabs → Copy/adapt valuation analysis
   - Reference Task 4 .png chart files throughout using `![caption](path/to/chart.png)` markdown image syntax
   - Create text-dense report with charts interspersed every 200-300 words
4. Save and deliver final `.md` report (single file — viewable in Claude Reports, like every other skill's output)

**Key Principles**:
- Write the report directly as markdown via Write/Edit tools (no DOCX skill, no python-docx)
- Use actual file operations (read .md/.xlsx/.png files, write .md file)
- Good equity research reports are text-dense with lots of illustrating images (60-80% visual coverage, 1+ chart per ~page-worth of text)
- Reference charts by relative path (`reports/company/<Slug>/charts/chart_XX.png`) so the rendered viewer can resolve them — keep the `charts/` folder alongside the .md so the link stays valid

**🔥 CRITICAL: GO ALL OUT ON THIS TASK**

**THIS IS THE FINAL DELIVERABLE. DO NOT TAKE SHORTCUTS.**

- ✅ **Use full token budget** - This is the culmination of all previous work
- ✅ **Write every section completely** - Do not summarize or abbreviate
- ✅ **Hit ALL minimum requirements** - 30+ pages, 10,000+ words, 25+ charts, 12+ tables
- ✅ **Be thorough on projection assumptions** - 2,000-3,000 words with product-by-product detail
- ✅ **Be comprehensive on scenarios** - 1,500-2,000 words with specific Bull/Base/Bear parameters
- ✅ **Insert ALL charts from Task 4** - Not just a few, ALL 25-35 charts throughout
- ✅ **Create ALL tables from Task 2/3** - Extract every financial table, don't skip any
- ✅ **Use Task 1 content verbatim** - Copy/paste full Company 101 sections (6-8K words)
- ✅ **Professional quality only** - This must be indistinguishable from JPMorgan/Goldman Sachs research

**NEVER:**
- ❌ "This section would include..." - WRITE THE ACTUAL SECTION
- ❌ "Charts would be inserted here..." - INSERT THE ACTUAL CHARTS
- ❌ "See financial model for details..." - EXTRACT AND INCLUDE THE DETAILS
- ❌ Skip sections due to length - Every section MUST be complete
- ❌ Abbreviate for token conservation - Use whatever tokens are needed

**This is publication-ready institutional research. Spare no effort, tokens, or detail.**

**Output**: Comprehensive Equity Research Report (`.md`)

**Specifications**:
- **Length**: 30-50 pages worth of content (MINIMUM 30 — measured by word count, not paginated since this is markdown)
- **Word count**: 10,000-15,000 words (MINIMUM 10,000)
- **Charts**: 25-35 image references via `![caption](path)`
- **Tables**: 12-20 comprehensive markdown tables
- **Format**: Markdown with inline links as `[label](url)` — viewable in Claude Reports like every other skill's output

**Structure** (markdown sections, not paginated):
- Top: Investment Summary (INITIATING COVERAGE format)
- Investment thesis & risks
- Company 101
- Financial analysis & projections
- Valuation analysis
- Appendices (Sources & References)

**File name**: `[Company]_Initiation_Report_[Date].md` — saved at the root of `reports/company/<Slug>/`. Chart PNGs from Task 4 live in `reports/company/<Slug>/charts/` so the relative `![](charts/chart_XX.png)` references resolve.

### Update-in-place rule — at most one initiation report per company

Before writing, check `reports/company/<Slug>/` for an existing initiation report and update it in place rather than creating a parallel dated copy.

```bash
ls "reports/company/<Slug>/" 2>/dev/null | grep -E "_Initiation_Report_.*\.md$"
```

- **Exactly one match** → overwrite it at the same path (Read then Write/Edit). Keep the existing filename even if its embedded date is stale — git history records the actual revision date. Update the date at the top of the document and any "as of" / "report date" fields in the body to today.
- **Multiple matches** (legacy state, including stale `.docx` from the previous DOCX-output era) → update the most recent `.md` by mtime, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new file using today's date in the filename.

**⚠️ DELIVER ONLY THIS 1 .md FILE. NO executive summaries, no "highlights" documents, no extra files.**

**⚠️ SOURCE CITATIONS ARE MANDATORY** (see Citation Standards below):
- ✅ Every figure caption AND every table has hyperlink source labels — not plain-text "Source: …" lines. Plain-text source lines fail the click-to-verify test that readers expect. Chart source lines baked into PNG images don't count: append `(外部源: [Link 1] / [Link 2])` to the caption line as markdown links.
- ✅ **EVERY substantive prose paragraph (≥ ~40 characters, not a heading / list-marker / source footer) ends with an inline markdown-link citation.** No exceptions. Page-1 investment bullets, thesis pillars, financial metrics, risk paragraphs, peer comparisons, qualitative analysis, forward-looking projections — every one. The user's stated trust standard: "for each paragraph, I hope there is citation, otherwise I don't trust the paragraph."
  - Example (factual claim): `FY2025 在 4.33 亿美元收入基础上实现 GAAP 净利润 6,200 万美元 ([FY2025 6-K](https://www.sec.gov/...))`
  - Example (figure caption): `图 15: 按细分领域的激光雷达 TAM — 2030 年扩张至 100-250 亿美元。 (外部源: [Yole Group](https://yolegroup.com/...) / [Frost & Sullivan](https://www.frost.com/...))`
  - Use the markdown italic-source convention if you want visual de-emphasis: `*Source: [label](url)*`.
- ✅ The report includes a dedicated **Sources & References** appendix listing every source, organized by category, every entry a markdown link with a date — minimum 20 entries.

**FAIL CONDITIONS — DO NOT DELIVER if any of these hit:**
- ❌ **FAIL 1**: No Sources & References appendix, or fewer than 20 entries in it. Add sources and re-save.
- ❌ **FAIL 2**: Fewer than 150 inline markdown links in the body (appendix entries don't count). A 30-50 page report has roughly 100-150 substantive paragraphs plus 25-35 figure captions plus 12-20 tables; landing under 150 links in the body means many paragraphs are uncited. Walk the body and add citations until the threshold is met.
- ❌ **FAIL 3**: Any page-1 investment-summary bullet without an inline citation, or any figure/table caption that is plain text (no hyperlink), or any peer-comparison paragraph without a peer-specific Yahoo Finance citation. These are spot-check fails — fix all instances before re-delivering.

**Final Verification** (every item must pass — any unchecked item blocks delivery):
- [ ] Word count is 10,000-15,000 (`wc -w reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md`)
- [ ] 25-35 chart references embedded via `![…](…)`
- [ ] 12-20 tables included
- [ ] Every figure caption has hyperlinked source labels (NOT plain text; chart-baked PNG source lines don't satisfy this — append `(外部源: [Link](url))` to the caption text)
- [ ] Every table has a source line directly under it with at least one hyperlink
- [ ] **Sources & References appendix exists with ≥20 entries, every entry a markdown link with a date**
- [ ] **Body has ≥150 distinct inline markdown links outside the appendix.** Verify programmatically:
  ```bash
  # Count links in the body (everything before the appendix heading)
  awk '/^##? (附录|Sources & References|Appendix)/{exit} {print}' \
    "reports/company/<Slug>/<Slug>_Initiation_Report_<Date>.md" \
    | grep -oE '\[[^]]+\]\([^)]+\)' | wc -l
  ```
  If under 150, walk the body and add citations to uncited paragraphs.
- [ ] **Every substantive prose paragraph (≥40 chars, not a heading or list marker) has an inline citation.** Spot check by reading paragraphs and confirming each ends with an `([label](url))` citation. Zero unsourced substantive paragraphs.
- [ ] Every page-1 investment-summary bullet has at least one inline citation
- [ ] Every figure caption (`图 N:` / `Figure N:`) has hyperlinked source labels
- [ ] All inline citations are markdown links (NOT bare URLs, NOT "Company data")
- [ ] Numbers match financial model exactly

**Truthfulness verification — run before delivery** (catches the model's documented fabrication patterns: synthetic SEC URLs, opinions misattributed to filings, invented competitor product names, invented executive names):

Follow the **Step 10 verification pass from the `company-research` skill** in full — see `.claude/skills/company-research/SKILL.md` § Step 10. The pass covers:

1. **URL HTTP check** — every URL returns 200 (or known-good 301/302). 404s must be fixed or removed.
2. **SEC filename audit** — every SEC URL ends in a real filename pulled from the EDGAR submissions JSON (`https://data.sec.gov/submissions/CIK<padded>.json`); no synthetic `<doctype>_<accession>.htm` patterns.
3. **10-K-cited claims spot-check** — at least five financial numbers cited to the 10-K are grep-confirmed to appear in the actual 10-K text.
4. **Opinion-attribution discipline** — no "dominant" / "leader" / "monopoly" / "co-leader" / "near-monopoly share" claim is attached to a 10-K citation unless the 10-K verbatim says it. These are analyst opinions; relabel `*Analyst view:*` and either cite a third-party research firm or leave uncited.
5. **Competitor product names** — specific product names (e.g. AMAT's NOKOTA / Producer / Endura, KLA's tools) are NOT cited to the subject company's 10-K. If named, cite the competitor's own filing or website.
6. **Executive names** — every named executive is grep-confirmed by exact name in the cited 8-K or DEF 14A.
7. **Internal consistency** — Section 1's competitive framing matches Section 7's; the history timeline matches the prose; product classifications are consistent across the mermaid graph and the section subheadings.

Append a `<details>`-folded **Verification log** after the Sources & References appendix listing what was checked and any residual unknowns. The log is short but mandatory — if it isn't present, the report has not actually been verified.

---

## Input Verification Protocol

### Why Input Verification Matters

Each task has strict prerequisites. Running a task without required inputs will:
- Waste time with incomplete work
- Produce low-quality outputs
- Require rework

**Always verify inputs before starting a task.**

### Verification Checklist by Task

**Task 1**: ✅ No verification needed (independent)

**Task 2**: Check historical financials available

**Task 3**: Check financial model exists and is accessible

**Task 4**: Check both model (Task 2) AND valuation (Task 3) exist

**Task 5**: Check ALL previous tasks complete (1, 2, 3, 4)

### What to Do if Verification Fails

```
IF prerequisites are missing:
1. Stop the current task
2. Identify which prerequisite task(s) need to be completed
3. Execute the missing task(s) first
4. Return to current task once prerequisites are met
```

### Example Verification Dialogue

```
User: "Use initiating-coverage, Task 5 for Tesla"

Claude: "Starting Task 5: Report Assembly for Tesla

VERIFICATION - Checking prerequisites:
- Task 1 (Company research)... ❌ NOT FOUND
- Task 2 (Financial model)... ❌ NOT FOUND
- Task 3 (Valuation)... ❌ NOT FOUND
- Task 4 (Charts)... ❌ NOT FOUND

⚠️ VERIFICATION FAILED

Task 5 requires ALL previous tasks to be complete.

To proceed:
1. Complete Task 1: Company Research
2. Complete Task 2: Financial Modeling
3. Complete Task 3: Valuation Analysis
4. Complete Task 4: Chart Generation
5. Then return to Task 5

Would you like to start with Task 1 first?"
```

---

## Task Reference Files

Detailed instructions for each task are in separate reference files to keep this skill lean:

- **Task 1** is delegated to the top-level `/company-research` skill — see that skill's `SKILL.md` and `references/` for the research workflow. No reference file lives in this skill for Task 1.
- **references/task2-financial-modeling.md** - Financial modeling workflow
- **references/task3-valuation.md** - Valuation methodology
  - Also see: references/valuation-methodologies.md for DCF/comps deep dive
- **references/task4-chart-generation.md** - Chart generation workflow
- **references/task5-report-assembly.md** - Report writing workflow
  - Also see: assets/report-template.md for report structure
  - Also see: assets/quality-checklist.md for quality checks

**When to load reference files**: Load ONLY the reference file associated with the specific task being performed. These files are very large - do not load multiple reference files at once. Read the appropriate task reference file at the start of the task for detailed step-by-step instructions.

---

## Quality Standards

All outputs meet institutional standards from leading investment banks (JPMorgan, Goldman Sachs, Morgan Stanley):

- **Comprehensive**: Meet all minimum requirements
- **Detailed**: Specific data and examples, not generic statements
- **Quantified**: Lead with numbers and metrics
- **Cited**: Proper sources with clickable hyperlinks
- **Professional**: Institutional-quality formatting
- **Accurate**: All numbers verified and cross-checked

### Citation Standards (applies to every task)

A report without sources is not institutional-quality research — it is an opinion piece. The skill is configured to fail delivery if sources are missing. Follow these rules at every step:

**URL must be the most-direct verifiable source — not a homepage.** A citation that links to `yolegroup.com` or `frost.com` (marketing homepage) is functionally a non-citation: the reader can't verify the specific number. Always link to either (a) the specific report / press release URL, or (b) the primary filing that quotes the third-party number. For Hesai's TAM chart that cites Yole, the right link is the Hesai FY25 6-K (where Yole's number actually appears) — labeled as `Hesai FY25 6-K 引用 Yole` so the source chain is transparent — plus a deeper Yole press-release URL if one exists. Never link a homepage and call it a citation.

**Source-chain labeling for third-party data.** When the analyst draws a number from a primary filing that itself cites a third party (e.g., Hesai's 6-K says "Yole estimates TAM at $X"), the inline label must make the chain explicit: `[FY2025 6-K 引用 Yole](rId45)` — not `[Yole](yolegroup.com)`. The click leads to the verifiable primary, not a marketing homepage.

**Per-chart source mapping (Task 5 Phase D).** Do NOT use a generic "Yole + Frost" citation on every TAM chart. Walk the chart-generation script (e.g., `build_charts_zh.py` for Task 4 in this repo's reports) and read its `source_line()` calls — they list exactly which sources each chart actually used. Build a `chart_number → [(rId, label), …]` dictionary and cite each caption with the chart-specific list. Financial-model-only charts (DCF sensitivity, scenarios, valuation football field) get `(来源: 本报告财务模型)` without a hyperlink — honest about internal sourcing.

**The analyst's own model is NOT a citable source.** Never write `(来源: 本报告模型估算)`, `(Source: our model)`, `(来源: 财务模型 DCF 标签页)`, or anything similar that points at the analyst's own workbook. The model is the analyst's view, not a source the reader can verify — labeling it as a source is functionally lying about provenance. The user's explicit rule: *"if model source, just remove it!! And it is not actual source !!"*

Decision tree for forward-looking / projection paragraphs:
- **Paragraph references both a historical fact AND a projection** (most thesis-pillar, growth-driver, and scenario paragraphs): cite only the external factual source(s) — `(来源: [FY2025 6-K](rId45) | [Yole 新闻稿](rId70))`. Drop any "model" trailer.
- **Pure forward-looking paragraph with NO external anchor at all** (rare in a well-sourced report): leave it uncited rather than fabricating a source. If the projection is meaningful, find the baseline document it's built on (10-K, latest guidance) and cite that instead.
- **Financial-model-tab figure captions** (DCF sensitivity heatmap, scenario comparison, valuation football field): no citation suffix on the caption. The chart's title plus the prose discussion already make clear it's an analyst projection.

**Inline citation format (markdown — Tasks 1 and 3):**
- After every quantitative claim: `Revenue grew 35% YoY to $234M in FY2024 ([10-K FY2024, p. 47](https://www.sec.gov/...))`.
- After every qualitative claim from an external source: `Management plans to expand into Europe by 2026 ([Q4 2024 Earnings Call, 2025-02-15](https://...))`.
- Acceptable source types (in order of preference): SEC filings (10-K, 10-Q, 8-K, DEF 14A) → earnings transcripts → company press releases → investor presentations → reputable industry reports (Gartner, IDC, McKinsey) → reputable news (WSJ, FT, Bloomberg, Reuters) → company website.
- Unacceptable: "Company data", "Industry sources", "Our estimates" without an underlying source, untraceable claims.

**Inline citation format (markdown — Task 5):**
- Every figure: caption line `*图 N: [title].*` (italic), then a source line immediately below as `*Source: [hyperlinked label](url), [date]*` (italic).
- Every table: `*Source: [hyperlinked label](url), [date]*` line directly under the table.
- **Every substantive prose paragraph gets an inline parenthetical markdown link at the end of its last sentence.** Concrete pattern:
  ```
  …<paragraph text ending with a claim> ([hyperlinked label](url))
  ```
  Example (English report):
  ```
  Revenue grew 35% YoY to $234M in FY2024, driven by AT128 ramp at the top US OEM customer. ([20-F FY2024](https://www.sec.gov/...))
  ```
  Example (Chinese report):
  ```
  FY2025 在 4.33 亿美元收入基础上实现 GAAP 净利润 6,200 万美元 ([FY2025 6-K](https://www.sec.gov/...))
  ```
  The label inside `[…]` must match the canonical name used in the Sources & References appendix — citations are not "named twice" in different forms, the appendix entry IS the canonical name. Never bare URLs in prose. Never plain "Company data" or "Industry sources" without a specific document.
- **Density target: ≥1 inline citation per substantive body paragraph, and ≥150 inline citations in the report body overall.** A 30-50 page report at 200-300 words per paragraph clears 100+ candidate paragraphs plus 25-35 figure captions plus 12-20 tables; landing under 150 inline citations means the report was assembled but not cited. Walk the body before delivery and add citations until the threshold is met.

**Mandatory Sources & References appendix (Task 5):**
- Title: "Sources & References"
- Organized by category in this order:
  1. SEC Filings (10-K, 10-Q, 8-K, DEF 14A — link to EDGAR viewer)
  2. Earnings Materials (transcripts, presentations, press releases — link to company IR)
  3. Company Materials (investor day decks, product pages, blog posts)
  4. Industry & Market Research (Gartner, IDC, McKinsey, BCG, market research firms — note "(subscription required)" where applicable)
  5. News & Trade Publications (WSJ, FT, Bloomberg, Reuters, trade press)
  6. Data Providers (Yahoo Finance, FactSet, Bloomberg, Capital IQ — note source for prices/multiples)
- Every entry: clickable hyperlink + date (YYYY-MM-DD) + 1-line description of what it sourced.
- Minimum 20 entries. A report with fewer than 20 distinct sources cited has insufficient research depth.

**How to carry sources through the pipeline:**
- Task 1 produces inline `[Source: ...](...)` citations and a Bibliography section → Task 5 reads them and copies them into prose and the appendix.
- Task 3 produces a `Source` column in the comps and DCF assumption tables → Task 5 carries the column through into the markdown tables.
- Task 2's DCF Inputs tab already has a `Source` column → Task 3 fills it in, Task 5 reads from it.
- **If Task 1 or Task 3 outputs have no sources, Task 5 will fail the final verification.** Go back and add sources to the upstream tasks before re-running Task 5.

---

## Learning from sell-side institutional research

A methodology study of 24 real initiation reports (Goldman Sachs, Morgan Stanley, UBS, J.P. Morgan, Bernstein, Nomura, Citi, BofA, Deutsche Bank, HSBC) surfaced patterns the desk-standard initiation enforces but this skill under-specifies. Fold these into the relevant task; the deep "how" lives in `references/task3-valuation.md`, `references/valuation-methodologies.md`, and `assets/report-template.md`.

**Pick the valuation method by company archetype — don't default to DCF-50/Comps-40/Precedent-10.** ~80% of the library prices the price target off a **forward target multiple on an out-year EPS/EBITDA** (JPM Yingliu 40x 2028E, Nomura Victory Giant 27x 2027E, Citi Hon Precision 36x avg-2027/28E, GS Co-Tech 22x 2028E, UBS Tao 20x 2027E); DCF leads only for biotech and regulated cash-flow names. Use the archetype decision table in task3: profitable growth equity → forward target multiple (DCF as cross-check); clinical/pre-revenue biotech → rNPV or DCF+M&A blend (GS Hemab 70/30, 16% WACC); two-growth-curve business → SOTP (DB Huayan: mature segment on P/S + emerging on out-year-TAM DCF); holdco → NAV with a stated discount (Bernstein SoftBank NAV −25%); long-duration infra/utility → multi-year DCF (UBS Zhongfu WACC 7.3%, Tinavi 10-yr DCF 9%/3%). State the chosen primary method and justify it in one sentence.

**Justify the target multiple three ways, every time.** House reports anchor the chosen multiple to (a) the stock's **own historical valuation band**, (b) at least one **named global peer's** current multiple, and (c) the **EPS-CAGR-vs-peers gap** that earns the premium/discount. Patterns to mirror verbatim: JPM Yingliu "40x 2028E vs Howmet 37x, justified by 55% EPS CAGR > peers' 23%"; GS Co-Tech "22x 2028E = +1 SD above 10-yr mean"; Nomura Victory Giant "27x = the A-share's own historical median." Each anchor carries an inline deep-URL citation (peer multiple → that peer's filing or a dated data-provider page; historical band → its data source) per the project numerical-accuracy rule. Never apply a peer-median multiple with no anchor.

**Tie the price target to a named out-year and a target date.** Replace the bare "12-month PT" with the house form: `[Rating], 12-month PT [currency][X] = [multiple]× [FY+n]E [EPS/EBITDA], target date [Mon-YYYY], implying [Y]% upside vs [price] ([date])`. Examples: JPM "Dec-2027 target, 40x 2028E EPS"; Citi "36x avg 2027/28E EPS"; Bernstein A+H dual-PT "44x A / 56.4x H on 2BF EPS." The multiple is applied to FY+2 or FY+3, not FY+1.

**Add an "Estimates vs Consensus" pillar — the spine of an initiation.** Table the analyst's out-year revenue / EPS / margin against sell-side consensus (FactSet/Bloomberg/Yahoo) for FY+1..FY+3, state the %-delta, and explain **why the Street is wrong** — that differentiated view is the reason to initiate. Mirror Bernstein Montage "2028E EPS Rmb6.25 vs consensus 4.49, +39%"; UBS Tao "+12-15% above consensus"; UBS Zhongfu per-year EPS-vs-consensus rows. Each consensus figure needs a dated data-provider citation; the analyst's own number is labelled an estimate, **never cited as a source** (honours the "model is not a source" rule).

**Page 1 is a fixed data block, not prose.** Add the desk identifier/header block (confirmed in the DB Huayan OCR): Rating | "Initiating Coverage" tag | report date | exchange:ticker (+ Reuters/Bloomberg codes) | current price (as-of date) | 12-month PT | implied upside/downside% | 52-week range | sector/industry | benchmark index level | analyst (+ CFA), plus a "Key indicators (FY1)" mini-table (ROE, net debt/equity, BVPS, P/B, operating margin) and a 1m/3m/12m absolute+relative performance row. Every figure carries an inline citation (price/52-wk/performance → dated Yahoo Finance link; ratios → the underlying filing). This extends — does not replace — the existing Page-1 rating box and investment bullets.

**Make catalysts a dated 12-month calendar, not a generic 3-5 bullet list.** Each catalyst gets a quarter/month and is a concrete event the reader can wait for: Bernstein Fervo "Cape-1 COD 4Q26"; GS Hemab "sutacimig GT Ph3 start H2-2026; FVIID Ph2 readout late-2026/early-2027"; GS surgical-robots "3Q26 overseas-order update." Write "Cape-1 COD 4Q26" — not "new product launch." Cross-reference the `catalyst-calendar` skill for the dated-event format.

**Output the scenario ladder as three datable price targets.** Distinct from the internal DCF scenario grid, give bull/base/bear **as PTs**, each driven by a specific multiple × out-year-EPS combination (ideally with a probability), so the football field is reproducible — Bernstein Arm "base $300 / bull $390." Each row states: the assumption delta, the resulting EPS/EBITDA, the multiple applied, and the implied share price.

**Support short / Sell / Neutral initiations symmetrically.** The library ships downside calls (Bernstein Summit UP TP $7.7, −57%; AEON UP −22%; GS Athub Neutral, −8%). For a negative-upside rating the Page-1 block reads "implied downside%," catalysts become "what breaks the thesis," and the risk section flips to "**upside risks to our Sell**." Don't let the template assume upside.

**Build the forward-revenue bridge from real evidence, and name TAM houses precisely.** Anchor out-year revenue on order backlog, contracted PPA/GW, capacity-expansion targets, and customer-win channel checks (DB Huayan "channel checks indicate Huayan supplies EngineAI, AGIBOT, Galbot") — not a top-down CAGR alone. Name the sizing house and attach its specific number (Frost & Sullivan, Yole, McKinsey "$4.4trn agentic-AI," Precedence Research, IDC), never "industry sources."

**Optional: multi-name / sector initiation mode.** When initiating ≥2 names in one sector, lead with the industry thesis, then a rating-distribution summary table (Company | Ticker | Rating | TP | Upside% | one-line thesis), then per-name pillars — the recurring Bernstein layout (Japan Consumer 7 names 4 OP/2 MP/1 UP; MENA Energy 6 names) and GS (Range + Athub). Each name keeps the archetype-matched valuation method. Default language English-only (consistent with tracking-style multi-name notes) unless the user opts into bilingual.

---

## Important Notes

### Task Independence

- **Task 1** can run anytime (no dependencies)
- **Task 2** can run anytime (just needs historical data)
- **Tasks 1 & 2** can run in parallel
- **Task 3** requires Task 2
- **Task 4** requires Tasks 2 & 3
- **Task 5** requires Tasks 1, 2, 3, & 4

### Session Management

**Same session**: Outputs automatically available to subsequent tasks

**Different sessions**: Reference previous task outputs explicitly
```
"Use Task 3 with the model from yesterday at [path]"
"Use Task 5 with the research document at [path]"
```

### File Organization

Recommended structure during workflow:
```
ProjectFolder/
├── Task1_Research/
│   └── [Company]_Research_Document.md
├── Task2_Model/
│   └── [Company]_Financial_Model.xlsx
├── Task3_Valuation/
│   └── [Company]_Valuation_Analysis.pdf
├── Task4_Charts/
│   ├── chart_01.png
│   └── ... (25-35 files)
└── Task5_Report/
    └── [Company]_Initiation_Report.md
```

### No End-to-End Execution

This skill does **NOT** support running all tasks automatically in sequence. Each task must be explicitly requested and verified.

**Why**: This ensures:
- Quality control at each stage
- Ability to review outputs before proceeding
- Flexibility to pause/resume workflow
- Clear verification of prerequisites

---

## Success Criteria

A successful initiation report workflow should:
1. Complete all 5 tasks in order
2. Pass all input verifications
3. Meet all quality standards
4. Produce all required deliverables
5. Numbers cross-check between outputs
6. Final report is publication-ready

**Output quality**: Institutional (JPMorgan/Goldman/Morgan Stanley level)
**Use case**: First-time comprehensive coverage of a company
