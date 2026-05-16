# Report Structure — Section-by-Section Spec

The final report has 9 sections plus a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **6,000–10,000 words** (sections may run longer than the per-section ranges below if there's genuine substance; do not pad to hit a number).

## Section word counts and content

### 1. Company Overview (800–1,200 words)
- What does the company do? (plain English)
- How do they make money? (business model)
- Where do they operate? (geographic presence)
- How large are they? (revenue, employees, customers)
- Key metrics and scale indicators

### 2. Company History (800–1,200 words)
- Founding story (who, when, why, where)
- Timeline of major milestones
- Strategic pivots or transformations
- Key acquisitions
- Recent developments (last 1–2 years)

### 3. Management Team (1,000–1,400 words)
- 300–400 word bio for each of 3–4 executives (CEO + CFO required; pick 1–2 more from COO/CTO/CPO/etc.)
- Each bio: current role, prior 2–3 roles, key accomplishments, education, years in industry, tenure at company
- Board composition and independence
- Insider ownership percentage
- Management track record assessment

### 4. Products & Services (700–1,000 words) — **grounded in a thorough company-website walk, not a generic summary**
- **Full product portfolio enumeration.** List every distinct product / service line found on the website. Group by segment if the company organizes them that way, but do not omit minor SKUs.
- For each major product: what it does, target customer, key features, pricing model (if disclosed), typical deal size
- **Per-product competitive-advantage assessment (REQUIRED).** For each material product, explicitly answer:
  - Does this product have a competitive advantage? (yes / partial / no)
  - If yes, what *kind* of moat: technology / IP / patents, cost leadership, scale, network effects, switching costs, brand, regulatory / certification, distribution, data, ecosystem lock-in
  - Evidence (market share, named wins, benchmarks, gross-margin profile, third-party reviews) — cite inline
  - Closest competing product from a named competitor, plus a one-line compare (ahead / behind / at parity)
- **Flagship vs. long-tail.** Identify the 1–3 products driving the business vs. legacy/experimental. State revenue or unit-mix share if disclosed.
- **Roadmap & recent launches.** Note products launched, repositioned, or sunset in the last 12 months.
- Cite the company website (specific product URL) and any third-party benchmark inline for each claim.

### 5. Customers & Go-to-Market (500–700 words)
- Customer segments and profiles
- Distribution channels
- Sales strategy and cycle
- Key partnerships
- Customer case studies (named wins)

### 6. Industry Overview (800–1,200 words)
- Industry definition and scope
- Market size and structure
- Growth rates (historical and projected)
- Key trends and drivers
- Regulatory environment
- Industry dynamics (fragmentation, supplier/buyer power, substitutes)

### 7. Competitive Landscape (700–1,000 words)
- Analysis of 5–10 key competitors (direct, indirect, emerging)
- Market positioning framework (price / features / scale dimensions)
- Company's competitive advantages
- Competitive vulnerabilities
- Market share analysis

### 8. Market Opportunity / TAM (500–700 words)
- TAM sizing and methodology
- SAM and SOM
- Market growth projections
- Company's serviceable market and share opportunity
- Penetration strategy

### 9. Risk Assessment (600–900 words)
- 8–12 distinct risks across 4 buckets (see `risk_taxonomy.md`)
- 50–100 words per risk: describe, quantify impact if possible, note mitigants
- Cover all four categories

## Output Template

```
COMPANY RESEARCH REPORT: [Company Name]
Date: [YYYY-MM-DD]

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

1. COMPANY OVERVIEW (800–1,200 words)
[Content]

2. COMPANY HISTORY (800–1,200 words)
[Content]

3. MANAGEMENT TEAM (1,000–1,400 words)
[Name], [Title]
[300–400 word bio]
[Repeat for 3–4 executives]
[Governance section]

4. PRODUCTS & SERVICES (700–1,000 words)
[Full enumeration of every product from the company website,
 grouped by segment. For each material product:
   - What it does, target customer, pricing
   - Competitive-advantage verdict (yes / partial / no) + moat type
   - Evidence + closest named competitor product (one-line compare)
 Then call out the 1–3 flagship products driving the business,
 and note product launches / sunsets in the last 12 months.]

5. CUSTOMERS & GO-TO-MARKET (500–700 words)
[Content]

6. INDUSTRY OVERVIEW (800–1,200 words)
[Content]

7. COMPETITIVE LANDSCAPE (700–1,000 words)
[Content]

8. MARKET OPPORTUNITY (500–700 words)
[Content]

9. RISK ASSESSMENT (600–900 words)
Company-Specific Risks:
[4–6 risks with descriptions]
Industry/Market Risks:
[3–4 risks with descriptions]
Financial Risks:
[2–3 risks with descriptions]
Macroeconomic Risks:
[2–3 risks with descriptions]

======================================

REFERENCES
[Consolidated, deduplicated list of every source cited inline above,
 organized by source type, each entry with date and URL/local path.]
```
