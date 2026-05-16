---
name: company-research
description: Produce a deep 6,000–8,000 word company research report (business, management, products, customers, industry, competitive landscape, TAM, risks) for a public or private company. Output is saved as markdown to the project-level `reports/` folder. Use when the user asks to "research", "deep-dive", "profile", or "initiate coverage on" a specific company or ticker — e.g. "research Tesla", "deep dive on PLTR", "company research for SZSE:002050".
---

# Company Research - Detailed Workflow

This document provides step-by-step instructions for executing (Company Research) of the initiating-coverage skill.

## Task Overview

**Purpose**: Research company's business, management, competitive position, industry, and risks.

**Prerequisites**: ✅ None (fully independent)
- Company name or ticker symbol only

**Output**: Company Research Document (6,000-8,000 words)

---

## Data Sources to Gather

### Primary Sources (Company)

**Pick the filing source by company domicile — SEC EDGAR only covers US issuers.**

- **US public companies → SEC EDGAR:**
  - Latest 10-K: Business description, risk factors, MD&A, financials
  - Recent 10-Qs: Quarterly updates
  - DEF 14A (Proxy): Executive compensation, board composition
  - 8-Ks: Material events, acquisitions, management changes
  - Local helper: `fetch_financial_report.py` (DB: `db/financial_reports.db`)

- **Chinese A-share / HK companies → cninfo (巨潮资讯) — NOT SEC EDGAR:**
  - Annual report (年度报告), Q1/Q3 quarterly reports (季度报告), semi-annual report (半年度报告)
  - Prospectus / listing docs, board announcements, material event disclosures
  - Ticker format: `SZSE:002050`, `SSE:688802`, `HKEX:2513`
  - Local helper: `fetch_cninfo_report.py` (DB: `db/cninfo_reports.db`). Run from `/Users/x/projects/financial_agent` so files land in `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/`.
  - Direct portal: https://www.cninfo.com.cn/ (Chinese-language disclosures are authoritative; English IR summaries on the company site are secondary).

- **Taiwanese companies (TWSE / TPEx) → MOPS (公開資訊觀測站):**
  - Portal: https://mops.twse.com.tw/ (English: https://mops.twse.com.tw/mops/web/index)
  - Annual report (年報), Q1–Q3 financial reports, material information announcements (重大訊息)
  - Also check the company's IR site for English investor decks and the TWSE/TPEx market filings page.

- **Japanese companies → EDINET + TDnet:**
  - EDINET (金融庁): https://disclosure2.edinet-fsa.go.jp/ — Yuho (有価証券報告書, annual), Shihanki (四半期報告書, quarterly), Rinji (臨時報告書, material events). English UI available.
  - TDnet (TSE timely disclosure): https://www.release.tdnet.info/ — earnings short reports (決算短信), press releases.
  - Many large issuers publish English IR PDFs ("Integrated Report", "Financial Results") directly on their IR site — use those for narrative; keep EDINET filings as the primary financial source.

- **Korean companies → DART (전자공시시스템):**
  - Portal: https://dart.fss.or.kr/ (English: https://englishdart.fss.or.kr/)
  - Business Report (사업보고서, annual), Half-year Report (반기보고서), Quarterly Report (분기보고서), Material Fact Reports (주요사항보고서)
  - Cross-check the company's global IR site for English earnings releases and presentations.

- **Other non-US jurisdictions:** default to the country's official regulator/exchange disclosure portal (e.g. SEDAR+ for Canada, ASX announcements for Australia, LSE RNS for UK, BSE/NSE for India). Do NOT fall back to SEC EDGAR unless the company is a 20-F / 6-K filer there.

- **Company Website & IR:**
  - Investor presentations
  - Earnings transcripts (last 2-3 quarters)
  - Press releases
  - Product documentation

- **For Private Companies:**
  - Company website and blog
  - Press releases and media coverage
  - LinkedIn for management bios
  - Crunchbase or PitchBook for funding history

### Secondary Sources (Industry/Competitive)
- Competitor websites and SEC filings
- Industry research reports (Gartner, Forrester, IDC, etc.)
- News articles and trade publications
- Market research reports
- LinkedIn profiles for key executives

### Key Information to Extract

**Key Information:**
- Company founding date, headquarters, employee count
- Revenue size and growth trajectory (if available)
- Product portfolio and pricing
- Customer segments and case studies
- Management backgrounds and track records
- Competitive landscape and market share
- Industry trends and growth drivers
- Regulatory considerations
- High-level financial metrics (from 10-K prose, not detailed extraction)

---

## Step-by-Step Research Workflow

### Step 1: Initial Data Collection

1. **Start with company website**
   - Read About/Company pages
   - Review product pages
   - Identify customer case studies
   - Note key metrics mentioned (employees, customers, etc.)

2. **Gather regulatory filings (if public) — route by domicile:**
   - **US issuer:** SEC EDGAR — latest 10-K, most recent 10-Q, latest DEF 14A, recent 8-Ks. Use `fetch_financial_report.py`.
   - **Chinese A-share / HK issuer:** cninfo (巨潮资讯) — latest 年度报告, most recent 季度报告 / 半年度报告, recent 重大事项公告. Use `fetch_cninfo_report.py` from the main project dir. Do **not** look for these on SEC EDGAR.
   - **Taiwanese issuer:** MOPS (公開資訊觀測站) — latest annual report, latest quarterly report, material information announcements.
   - **Japanese issuer:** EDINET for Yuho (annual) and Shihanki (quarterly); TDnet for 決算短信 and timely disclosures; company IR site for English integrated report.
   - **Korean issuer:** DART — latest Business Report (사업보고서), Half-year / Quarterly Report, recent Material Fact Reports.
   - **Other jurisdictions:** use the country's official disclosure portal (SEDAR+, ASX, LSE RNS, BSE/NSE, etc.).
   - Note filing dates and the source portal used for each document.

3. **Read earnings materials**
   - Latest earnings transcript
   - Most recent investor presentation
   - Press releases from last 12 months

4. **Document basic facts**
   - Founding date and story
   - Headquarters location
   - Employee count
   - Products/services
   - Key customers

### Step 2: Business Model Analysis

1. **Map revenue streams**
   - What does the company sell?
   - How is it priced? (subscription, transaction, license, etc.)
   - Who pays?
   - What are typical deal sizes?

2. **Understand customer segments**
   - Enterprise vs. SMB vs. consumer
   - Industries served
   - Geographic distribution
   - Customer concentration (top 10 customers)

3. **Document go-to-market**
   - Direct sales vs. channel partners
   - Sales cycle length
   - Customer acquisition strategy
   - Distribution model

4. **Identify unit economics**
   - LTV/CAC if available
   - Gross margins
   - Net revenue retention
   - Payback periods

### Step 3: Management Research

**For each of 3-4 key executives:**

1. **Identify key leaders**
   - CEO (always required)
   - CFO (always required)
   - COO, CTO, or other C-suite (2 additional)

2. **Research each executive**
   - Find LinkedIn profile
   - Review DEF 14A for background
   - Search for press interviews
   - Note tenure at company

3. **Write 300-400 word bio including:**
   - Current role and responsibilities
   - Prior roles and companies (last 2-3 positions)
   - Key accomplishments and track record
   - Education and credentials
   - Years of experience in industry
   - Time at current company

4. **Assess governance**
   - Board composition and independence
   - Key board members and their backgrounds
   - Insider ownership percentage
   - Executive compensation structure

### Step 4: Competitive Intelligence

1. **Identify 5-10 competitors**
   - Direct competitors (same products/markets)
   - Indirect competitors (substitute solutions)
   - Emerging competitors (disruptors)
   - Check 10-K for company's own list of competitors

2. **Research each competitor**
   - Visit competitor website
   - Review their SEC filings (if public)
   - Note key products and positioning
   - Identify differentiators
   - Estimate market share (if data available)

3. **Create competitive framework**
   - Map on key dimensions (price, features, scale, etc.)
   - Identify company's competitive advantages
   - Note competitive vulnerabilities
   - Assess switching costs and network effects

4. **Document competitive insights**
   - Who are the market leaders?
   - Where does this company rank?
   - What are unique differentiators?
   - What are competitive threats?

### Step 5: Industry Analysis

1. **Define the industry**
   - Industry classification (NAICS/SIC)
   - Scope and boundaries
   - Related/adjacent industries

2. **Size the market**
   - Total addressable market (TAM)
   - Serviceable addressable market (SAM)
   - Serviceable obtainable market (SOM)
   - Current penetration rate

3. **Research growth drivers**
   - Historical market growth rate
   - Projected growth rate (next 3-5 years)
   - Key trends accelerating/decelerating growth
   - Technology changes impacting industry

4. **Understand industry structure**
   - Fragmented vs. consolidated
   - Barriers to entry
   - Supplier/buyer power
   - Threat of substitutes
   - Regulatory environment

### Step 6: Risk Assessment

Identify 8-12 risks across four categories. For each risk, write 50-100 words.

**Company-Specific Risks (4-6 risks):**
- Execution risk (can management deliver?)
- Customer concentration (top customers)
- Key person dependency
- Product/technology obsolescence
- Geographic concentration
- Integration risk (if recent M&A)

**Industry/Market Risks (3-4 risks):**
- Competitive intensity
- Regulatory changes
- Technology disruption
- Market saturation

**Financial Risks (2-3 risks):**
- Profitability timeline
- Funding requirements
- Debt levels and covenants
- Cash burn rate (if unprofitable)

**Macroeconomic Risks (2-3 risks):**
- Economic sensitivity (cyclical vs. defensive)
- Interest rate sensitivity
- Foreign exchange exposure
- Geopolitical factors

**For each risk:**
- Describe the risk clearly
- Quantify impact if possible
- Note likelihood/severity
- Identify mitigating factors

### Step 7: Synthesis and Writing

**Write document following this structure:**

1. **Company Overview** (800-1,200 words)
   - What does the company do? (plain English)
   - How do they make money? (business model)
   - Where do they operate? (geographic presence)
   - How large are they? (revenue, employees, customers)
   - Key metrics and scale indicators

2. **Company History** (800-1,200 words)
   - Founding story (who, when, why, where)
   - Timeline of major milestones
   - Strategic pivots or transformations
   - Key acquisitions
   - Recent developments (last 1-2 years)

3. **Management Team** (1,000-1,400 words)
   - 300-400 word bio for each of 3-4 executives
   - Board composition and governance
   - Insider ownership
   - Management track record assessment

4. **Products & Services** (700-1,000 words)
   - Detailed product portfolio
   - Key features and capabilities
   - Product differentiation
   - Target customers and use cases
   - Pricing models and typical deal sizes

5. **Customers & Go-to-Market** (500-700 words)
   - Customer segments and profiles
   - Distribution channels
   - Sales strategy and cycle
   - Key partnerships
   - Customer case studies

6. **Industry Overview** (800-1,200 words)
   - Industry definition and scope
   - Market size and structure
   - Growth rates (historical and projected)
   - Key trends and drivers
   - Regulatory environment
   - Industry dynamics

7. **Competitive Landscape** (700-1,000 words)
   - Analysis of 5-10 key competitors
   - Market positioning framework
   - Company's competitive advantages
   - Competitive vulnerabilities
   - Market share analysis

8. **Market Opportunity** (500-700 words)
   - TAM sizing and methodology
   - Market growth projections
   - Company's serviceable market
   - Market share opportunity
   - Penetration strategy

9. **Risk Assessment** (600-900 words)
   - Company-specific risks (4-6)
   - Industry/market risks (3-4)
   - Financial risks (2-3)
   - Macroeconomic risks (2-3)
   - Each risk: 50-100 word description

**Data Sources Section**
- List all sources used
- Include dates and URLs
- Organize by source type

---

## Quality Standards

### Content Depth
- Each section must meet minimum word count targets
- Analysis should be substantive, not just descriptive
- Use specific examples and quantitative data
- Cite sources throughout
- Maintain objectivity and balance

### Management Bios
- 300-400 words per executive for 3-4 key executives
- Must include: current role, prior experience, key accomplishments, education
- Provide enough detail to assess track record and capabilities

### Competitive Analysis
- Must analyze 5-10 specific competitors
- Include both direct and indirect competitors
- Assess relative positioning on key dimensions
- Identify company's competitive advantages and vulnerabilities
- Use specific data and examples

### Risk Assessment
- Must identify 8-12 distinct risks across all four categories
- Each risk needs 50-100 word description
- Quantify impact where possible
- Note mitigating factors
- Cover all four risk categories

### Writing Quality
- Professional, analytical tone
- Lead with key insights
- Use concrete examples and data
- Avoid generic statements
- Proper citations throughout

---

## Output Format

```
COMPANY RESEARCH REPORT: [Company Name]
Date: [Date]
Analyst: [Your name if applicable]

TABLE OF CONTENTS
1. Company Overview
2. Company History
3. Management Team
4. Products & Services
5. Customers & Go-to-Market
6. Industry Overview
7. Competitive Landscape
8. Market Opportunity (TAM)
9. Risk Assessment

======================================

1. COMPANY OVERVIEW (800-1,200 words)

[Content]

2. COMPANY HISTORY (800-1,200 words)

[Content]

3. MANAGEMENT TEAM (1,000-1,400 words)

[Name], [Title]
[300-400 word bio]

[Repeat for 3-4 key executives]

[Governance section]

4. PRODUCTS & SERVICES (700-1,000 words)

[Content]

5. CUSTOMERS & GO-TO-MARKET (500-700 words)

[Content]

6. INDUSTRY OVERVIEW (800-1,200 words)

[Content]

7. COMPETITIVE LANDSCAPE (700-1,000 words)

[Content]

8. MARKET OPPORTUNITY (500-700 words)

[Content]

9. RISK ASSESSMENT (600-900 words)

Company-Specific Risks:
[4-6 risks with descriptions]

Industry/Market Risks:
[3-4 risks with descriptions]

Financial Risks:
[2-3 risks with descriptions]

Macroeconomic Risks:
[2-3 risks with descriptions]

======================================

DATA SOURCES
[List all sources with dates and URLs]
```

---

## Success Criteria

A successful Task 1 completion should deliver:

1. Meet 6,000-8,000 word target (verify word count)
2. Include all 9 required sections with target word counts
3. Provide substantive analysis, not just description
4. Use specific examples and quantitative data
5. Cite all sources properly
6. Enable reader to understand:
   - What the company does and how it makes money
   - Quality and track record of management team
   - Company's competitive position
   - Market opportunity size
   - Key risks to consider

---

## File Naming Convention

Save the output to the **project-level `reports/` folder** at `/Users/x/projects/financial_agent/reports/`. Create the folder if it does not yet exist.

File name:

`reports/[Company]_Research_Document_[Date].md`

Example: `reports/Tesla_Research_Document_2024-10-27.md`

Always write to the main project's `reports/` directory — never to a worktree, `~/Downloads`, or any other location.
