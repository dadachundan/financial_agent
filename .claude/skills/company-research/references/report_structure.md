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

## Top-of-report banner — guidance changes (REQUIRED when present)

**Before the Table of Contents**, scan the latest earnings release / 业绩预告 / 业绩快报 / 季度报告 / 半年度报告 / 年度报告 / 8-K guidance update for any change to **full-year guidance** versus the prior outlook. If the company has:

- **Raised** full-year guidance (revenue, EPS, GM, or any disclosed full-year KPI), or
- **Cut** full-year guidance, or
- **Reaffirmed** guidance after a meaningful operating change, or
- **Initiated** guidance for the first time

→ open the report with a one-paragraph callout block highlighting the change. Use a `> **Update:**` blockquote so it visually separates from Section 1.

**Required content of the callout:**
- Direction (raised / cut / reaffirmed / initiated) + the specific metric and the old vs. new range
- The filing or call where it was disclosed (markdown link to the real URL)
- One sentence on the implied YoY change vs. the prior guide
- One sentence on the stated driver (management's words, briefly)

**Example (English-language report):**

```
> **Update — FY2025 guidance raised (2025-08-12):** Management raised full-year
> revenue guidance to USD 6.2–6.4B (from USD 5.9–6.1B) and raised non-GAAP
> EPS to USD 4.10–4.25 (from USD 3.85–4.00) on the back of stronger
> data-center demand and a faster H200 ramp.
> Source: [Q2-FY2025 earnings press release, 2025-08-12](https://...).
```

**Example (Chinese company, English report):**

```
> **Update — 上调 FY2025 全年业绩指引 (2025-08-15):** 公司将 2025 年营收
> 指引上调至 RMB 12.5–13.0 bn (原 RMB 11.5–12.0 bn)，归母净利润指引上调
> 至 RMB 2.1–2.3 bn (原 RMB 1.85–2.0 bn)，主因机器人业务订单加速及
> Tier-1 客户放量。
> Source: [2025 年半年度业绩预告, 2025-08-15](https://static.cninfo.com.cn/...).
```

If there is **no recent guidance change** to highlight, omit the banner entirely — do not add a placeholder. Guidance that's purely a re-affirmation with no new color isn't worth the banner.

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

### 3. Management Team (300–500 words)
**Cover the founder and the current CEO only — nothing else.** No CFO, no other executives, no governance footer, no track-record synthesis. Keep this chapter tight.

- **Founder bio: 200–300 words.** Prior 2–3 roles with *what specifically they accomplished* (numbers, not titles), education, founding thesis, ownership stake today, and whether still operationally involved.
- **Current CEO bio: 200–300 words.** Same depth: prior 2–3 roles with concrete accomplishments, education, tenure at this company, ownership stake, comp structure.
- **If founder is still CEO, write one combined bio (300–450 words)** — don't split into two.

### 4. Products & Services (700–1,200 words) — **anchored to the issuer's own product table, written pedagogically, ending with a synthesis paragraph**

This is the section where reports most often degrade into either a flat product catalog or sell-side commentary dressed up as fact. Use the following structure to avoid both failure modes.

**(a) Anchor to the issuer's own product matrix.** Most semiconductor / industrial / hardware / pharma issuers publish a product matrix in the 10-K / 年度报告 / Yuho Item 1 Business section — typically organized as Market → Process/Application → Technology → Products (or an equivalent for the industry: Therapeutic Area → Indication → Modality → Product, etc.). **Reproduce that table verbatim as the spine of Section 4** with a 10-K citation. This grounds the section in primary disclosure and prevents the model from inventing categories or revenue percentages. If the issuer does not publish such a table, build one from the website's product navigation (citing the website) and label it explicitly as analyst-constructed.

**(b) Walk each row with pedagogical color — three brief beats per product family.** For each row in the matrix, write a paragraph that covers:
  1. **What it does** in the manufacturing / value-chain flow (concrete physical role — "lays down copper interconnect", "drills channel holes in 3D NAND", "punches TSVs through silicon for HBM stacks"). Use analogies where they help a non-specialist reader.
  2. **How it differentiates from sibling products in the same matrix** (different application, different process step, different node). The reader should leave able to explain why a fab needs SABRE *and* ALTUS *and* VECTOR, not just "Lam sells deposition tools."
  3. **Strategic significance** — what technology inflection, customer, or end-market is currently driving demand (HBM ramp, GAA logic transition, advanced-packaging build-out, etc.). Cite the press release / 10-K Products text / earnings-call language for the inflection.

**(c) Keep competitive commentary in a separate sentence labeled `*Analyst view:*`** and cite to a third-party source or the competitor's own filing — never the subject's 10-K — per the citation discipline in Step 5 of SKILL.md. Specific competitor product names (e.g. AMAT's NOKOTA, Producer, Endura) belong here, not in the product-row description.

**(d) End the section with a synthesis paragraph that shows how the product categories interact.** This is what makes a research report *pedagogical* rather than a catalog. For semicap, it's the Deposition → Etch → Clean → Deposition manufacturing cycle. For other industries, the equivalent: how the products compose a single customer workflow / use case / treatment regimen / installation. One paragraph; 3–5 sentences; explicit about which products sit at each step.

**(e) Required elements regardless of structure:**
  - **Per-product competitive-advantage assessment.** For each material product, a one-clause verdict (yes / partial / no) plus the moat type (technology / IP / patents, scale, switching costs, network effects, regulatory, distribution, ecosystem lock-in) — under the `*Analyst view:*` label.
  - **Flagship vs. long-tail.** Identify the 1–3 products driving the current business (state revenue / unit-mix share if disclosed; otherwise flag as analyst estimate).
  - **Roadmap & recent launches.** Products launched, repositioned, or sunset in the last 12 months — with the company press release as the citation.
  - **Recurring / aftermarket / services business.** Many issuers have a separate business group outside the product matrix (CSBG for Lam, Services for AMAT, etc.). Treat that as its own subsection — describe what it consists of, how it's reported in the financials, why it dampens cyclicality, and the recurring-revenue economics.

**Example structure (semiconductor capital equipment):**
```
4.1 The 10-K product matrix [verbatim table from 10-K Item 1, cited]
4.2 Synthesis — how the categories interact [3–5 sentence narrative of the chip-build cycle]
4.3 Deposition [walk each product row with pedagogical color]
4.4 Etch [same]
4.5 Clean [same]
4.6 [Recurring service business — CSBG / Services / aftermarket]
4.7 Flagship franchises and recent launches
```

Adapt the equivalent structure for non-semicap industries: e.g. for pharma, group by Therapeutic Area; for industrial automation, by Cell / Line / Plant level.

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

3. MANAGEMENT TEAM (300–500 words)
[Founder name]
[200–300 word bio — prior roles, founding thesis, ownership, current role]
[Current CEO name] — skip if same person as founder
[200–300 word bio — prior roles, tenure, ownership, comp]

4. PRODUCTS & SERVICES (700–1,200 words)
[4.1 Verbatim product matrix from the issuer's 10-K / 年报 / Yuho
     (Market / Process-Application / Technology / Products), cited.
 4.2 Synthesis paragraph: how the categories interact in a customer workflow.
 4.3-4.5 (per major market in the matrix): walk each product row with
   - what it physically does in the manufacturing / value-chain flow
   - how it differentiates from sibling products in the same matrix
   - strategic significance: technology inflection or customer wave driving demand
   - *Analyst view:* — competitive-advantage verdict + moat type +
     closest named competitor product (cited to competitor's filing or website,
     NOT the subject's 10-K).
 4.X Recurring / aftermarket / services group (CSBG-equivalent), if applicable.
 4.Y Flagship 1-3 franchises + last-12-months launches.]

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
