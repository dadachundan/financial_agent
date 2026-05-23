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

### 4. Products & Services (700–1,500 words) — **anchored to the issuer's own product table, quoted verbatim, written pedagogically (mixed language OK), ending with a synthesis paragraph**

This is the section where reports most often degrade into either a flat product catalog or sell-side commentary dressed up as fact. Use the following structure to avoid both failure modes.

**(a) Anchor to the issuer's own product matrix — and embed the original page image, not just a reproduction.**

Most semiconductor / industrial / hardware / pharma issuers publish a product matrix in the 10-K / 年度报告 / Yuho Item 1 Business section — typically organized as Market → Process/Application → Technology → Products (or an equivalent for the industry: Therapeutic Area → Indication → Modality → Product, etc.).

**Two things must appear in 4.1:**
  1. **The 10-K's actual rendered table as a PNG image**, embedded via markdown (`![…](charts/<ticker>_10k_products_table.png)`), with a caption citing the 10-K. Render it with the helper script below (`render_10k_section.py`). The image is what makes Section 4 look authoritative — the reader can see the original filing source.
  2. **A markdown reproduction of the same table** below the image, so the content is searchable / accessible to screen-readers and so quoted product names can be linked.

If the issuer does not publish such a table, build one from the website's product navigation (citing the website) and label it explicitly as analyst-constructed.

**(b) Walk each row with verbatim 10-K quotes + native-language pedagogy.**

For each product family in the matrix, follow this exact three-part pattern:

  1. **10-K verbatim (block quote).** Quote the 10-K's Product Family description directly — use `> "…"` markdown block-quote syntax with the inline 10-K citation right above the quote. Verbatim text from the issuer is by definition non-fabricated and gives the reader Lam's own explanation of what the product does.
  2. **Native-language pedagogical explanation** (introduced with a heading like `**中文释义：**` for Chinese audience, or no special heading for English-language reports — but in either case clearly labeled as the analyst's plain-language gloss, *not* attributed to the 10-K). This is where the analyst earns their pay: explain in 3–6 sentences (a) the underlying physics / process / mechanism using analogies where helpful, (b) how this product differs from its sibling products in the same matrix, and (c) the strategic inflection currently driving demand. **Mixing Chinese into a primarily English report is encouraged when the topic is deeply technical** — Chinese has dense, idiomatic vocabulary for semiconductor process steps (薄膜、刻蚀、互连、字线、栅极, etc.) that compresses what English needs several sentences to explain. Don't be shy about it.
  3. ***Analyst view:* sentence** — competitive context only, cited to the competitor's filing or website or a third-party research source, never to the subject's 10-K. Specific competitor product names (e.g. AMAT's NOKOTA, Producer, Endura) belong here.

**(c) End the section with a synthesis paragraph that shows how the product categories interact.** This is what makes a research report *pedagogical* rather than a catalog. For semicap, it's the Deposition → Etch → Clean → Deposition manufacturing cycle. For other industries, the equivalent: how the products compose a single customer workflow / use case / treatment regimen / installation. One paragraph; 3–5 sentences; explicit about which products sit at each step. Optionally include a small Mermaid LR or TD graph showing the loop.

**(d) Required elements regardless of structure:**
  - **Per-product competitive-advantage assessment.** For each material product, a one-clause verdict (yes / partial / no) plus the moat type (technology / IP / patents, scale, switching costs, network effects, regulatory, distribution, ecosystem lock-in) — under the `*Analyst view:*` label.
  - **Flagship vs. long-tail.** Identify the 1–3 products driving the current business (state revenue / unit-mix share if disclosed; otherwise flag as analyst estimate).
  - **Roadmap & recent launches.** Products launched, repositioned, or sunset in the last 12 months — with the company press release as the citation. If a new platform was launched (e.g. Akara, ALTUS Halo), block-quote the press release the same way you block-quote the 10-K.
  - **Recurring / aftermarket / services business.** Many issuers have a separate business group outside the product matrix (CSBG for Lam, Services for AMAT, etc.). Treat that as its own subsection — describe what it consists of, how it's reported in the financials, why it dampens cyclicality, and the recurring-revenue economics.

**Rendering the issuer's product table as a PNG (for step (a))**

The 10-K HTML is downloaded locally to `financial_reports/<TICKER>/` by `fetch_financial_report.py`. To render the products page to PNG, use playwright + chromium (one-time installation: `pip install playwright && python3 -m playwright install chromium`):

```python
from playwright.sync_api import sync_playwright
INPUT_HTML  = '/Users/x/projects/financial_agent/financial_reports/<TICKER>/<10-K-filename>.htm'
OUTPUT_PNG  = 'reports/company/<Slug>/charts/<ticker>_10k_products_table.png'
ANCHOR_TEXT = 'SABRE'  # or any unique product-name string from the table
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 2000}, device_scale_factor=2)
    page.goto(f'file://{INPUT_HTML}')
    tbl = page.locator('table').filter(has_text=ANCHOR_TEXT).first
    tbl.scroll_into_view_if_needed(timeout=5000)
    bb = tbl.bounding_box()
    page.screenshot(path=OUTPUT_PNG, clip={
        'x': max(0, bb['x']-20), 'y': max(0, bb['y']-80),
        'width': min(1200, bb['width']+40), 'height': min(2000, bb['height']+100)})
    browser.close()
```

For SEC HTML 10-Ks the table extracts cleanly. For Chinese 年度报告 (cninfo PDFs), use `fitz` (PyMuPDF) to render the relevant page to PNG instead. Save the PNG into `reports/company/<Slug>/charts/` so the relative `![](charts/...)` reference resolves.

**Example structure (semiconductor capital equipment, mixed English / Chinese in the body, used for the LRCX report):**
```
4.1 The 10-K product matrix [PNG embed of 10-K rendered table + verbatim markdown reproduction]
4.2 Synthesis — how the categories interact [3–5 sentence narrative + small Mermaid LR graph]
4.3 Deposition [for each product family: 10-K block quote → 中文释义 → *Analyst view:*]
4.4 Etch [same pattern, per product family]
4.5 Clean [same pattern]
4.6 [Recurring service business — CSBG / Services / aftermarket]
4.7 Flagship franchises and recent launches
```

**Adapting for non-semicap industries:**
- For **pharma / biotech**, group by Therapeutic Area; block-quote the 10-K's product narrative for each marketed drug; the pedagogical color explains the mechanism of action, the patient population, the position vs SoC.
- For **industrial automation / robotics**, group by Cell / Line / Plant level; block-quote the product-family description; the pedagogical color explains where in the customer's workflow the product sits and what it integrates with.
- For **fintech / SaaS**, group by use case; block-quote the 10-K's customer / segment narrative; the pedagogical color explains what category of work this software replaces and what the API surface looks like.

The pattern (issuer's own table → verbatim quote → analyst-labeled pedagogical gloss → analyst-labeled competitive view → synthesis at the end) is industry-agnostic.

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
