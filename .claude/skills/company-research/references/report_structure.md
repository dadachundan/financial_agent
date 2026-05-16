# Report Structure — Section-by-Section Spec

The final report has 9 sections plus a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **6,000–10,000 words** (sections may run longer than the per-section ranges below if there's genuine substance; do not pad to hit a number).

Embed **4–8 charts** across the report (mix of matplotlib PNGs and Mermaid blocks). Suggested placement:

| Section | Chart |
|---|---|
| 1 Overview | Revenue + gross margin trend (PNG, 3–5 yr, dual-axis) |
| 2 History | Mermaid `timeline` block |
| 4 Products | Mermaid `graph TD` product tree |
| 5 Customers | Mermaid `pie` — top 3–5 customer concentration |
| 7 Competitive | Mermaid `quadrantChart` **or** peer-comparison bars (PNG) |
| 8 TAM | Market-size growth chart (PNG) |

Every chart needs a citation directly underneath in the same markdown-link format used in prose. PNGs go in `reports/charts/<company>_<name>.png`.

## Section word counts and content

### 1. Company Overview (800–1,200 words)
- What does the company do? (plain English)
- How do they make money? (business model)
- Where do they operate? (geographic presence)
- How large are they? (revenue, employees, customers)
- Key metrics and scale indicators
- **Valuation snapshot (REQUIRED).** Current price, market cap, **TTM P/E**, **TTM P/S** (plus P/B for capital-heavy businesses and EV/EBITDA for leveraged / cyclical names). Include the 3-year range of each multiple and the sector / peer median (3–5 named comps) so today's number has context. Cite the market-data source (Yahoo Finance / Eastmoney / Kabutan / DART, etc.) with a direct URL.
  - **If P/E is negative** → state why: cash-burning growth, one-off charge (impairment, litigation, write-down), cyclical trough, or structural decline. Name the specific income-statement line driving the loss and cite the filing.
  - **If P/E > 50× TTM (or > 2× sector median) or P/S > 15× (or > 3× sector median)** → name the cause: high-growth sector premium (AI infra, GLP-1, EV battery, advanced packaging — say which), temporarily depressed earnings, narrative / sector-proxy premium, M&A speculation, or small-float distortion. **Cite evidence** (sell-side note, earnings-call language, peer that re-rated similarly, sector ETF flows). Do not leave the multiple unexplained.
  - **If P/E < 8× or P/S is unusually low** → say whether it's a value trap, cyclical peak, governance concern, or genuine mispricing.
  - For private companies, substitute the latest funding-round post-money valuation and implied revenue multiple if disclosed; if not, state "private; no disclosed valuation."

### 2. Company History (400–700 words)
- Founding story (who, when, why, where) — 1 short paragraph
- Mermaid `timeline` block covering 5–10 major milestones (replaces a prose recap of every dated event)
- 2–3 strategic pivots or transformations, each in 1–2 sentences explaining the *why*, not just the *what*
- Key acquisitions (bullet list with year + rationale)
- Recent developments (last 1–2 years) — keep tight; details that affect the current thesis can move to Section 4 / 5 / 7 / 8 instead of bloating history.

### 3. Management Team (600–900 words)
**CEO / founder is the most important bio — spend the most depth there.** A strong founder-CEO can be the single biggest determinant of long-run outcome; everyone else is supporting cast.

- **CEO or founder bio: 250–350 words** (deeper if the company is founder-led or the CEO is unusually consequential — Musk-tier, founder-with-supervoting, recent-arrival-with-mandate). Cover: prior 2–3 roles, *what specifically they accomplished* (numbers, not titles), education, years in industry, tenure at this company, ownership stake, comp structure, public profile / interviews / writing. If founder, also: founding thesis and whether they still own materially.
- **CFO bio: 150–200 words.** Prior roles, IPO / M&A / capital-markets track record, tenure, any prior public-company CFO experience.
- **1–2 other executives (COO / CTO / CPO / heads of key segments): 80–120 words each.** Pick whoever is most material to the thesis — e.g. the CTO at a chip company, the chief revenue officer at a sales-led SaaS, the head of the largest segment at a conglomerate.
- **Governance footer (80–150 words):** board composition and independence, insider ownership %, comp structure (cash vs. equity, performance-linked %), any related-party transactions or governance flags. Bullet form is fine.
- **Management track record assessment (50–100 words):** one-paragraph synthesis — has this team delivered before? Where are the gaps?

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

### 5. Customers & Go-to-Market (500–800 words)
- Customer segments and profiles
- **Customer concentration (REQUIRED).** Quantify top-1 and top-5 customer share of revenue from the latest annual filing, plus the 3-year trend if available. Name the top customers when disclosed. Cite the specific filing section (e.g. `年度报告` § 前五名客户, 10-K segment note, Yuho `主要な販売先`). State the contract structure (master agreement vs. PO-by-PO, multi-year vs. annual) and whether any top customer is also a competitor / vertically integrating. **If top-1 > 20% or top-5 > 50%, flag it explicitly here and carry it into Section 9 as a material risk.** If the company does not disclose, say so — do not skip.
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
