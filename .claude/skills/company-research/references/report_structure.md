# Report Structure — Section-by-Section Spec

The final report has 9 sections plus a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **6,000–10,000 words** (sections may run longer than the per-section ranges below if there's genuine substance; do not pad to hit a number).

Embed **4–8 charts** across the report (mix of matplotlib PNGs and Mermaid blocks). Suggested placement:

| Section | Chart | IR-deck slide that often anchors it |
|---|---|---|
| 1 Overview | Revenue + gross margin trend (PNG, 3–5 yr, dual-axis) | Latest earnings-deck "Revenue + Margin Bridge" slide |
| 2 History | Mermaid `timeline` block | Investor day "Our journey" slide (when present) |
| 4 Products | Mermaid `graph TD` product tree | Investor day product-portfolio slide |
| 5 Customers | Mermaid `pie` — top 3–5 customer concentration | Investor day customer-logo / cohort slide |
| 7 Competitive | Mermaid `quadrantChart` **or** peer-comparison bars (PNG) | Investor day "Why we win" / feature-matrix slide |
| 8 TAM | Market-size growth chart (PNG) | Investor day TAM build slide (the single most useful IR slide) |

Every chart needs a citation directly underneath in the same markdown-link format used in prose. PNGs go in `reports/charts/<company>_<name>.png`. **When an IR deck has the data behind a chart, embed the rendered IR slide as a PNG (using `render_10k_section.py`-style page screenshot for PDFs) instead of rebuilding the chart from scratch** — the slide is the most authoritative form of the chart, the company endorses the numbers, and the reader can trace the source. Cite the slide directly underneath.

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
- **IR primary input:** Latest 1–2 quarterly earnings deck (revenue + margin bridge slide, segment-mix slide, capital-allocation slide). At least one citation in this section should be to a recent earnings-deck slide; cite the slide number explicitly.
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

### 4. Products & Services (700–1,500 words) — **THE most important section of the report**

> **Priority note:** Section 4 is the single most consequential chapter of the entire research report — see SKILL.md § "The Products & Services chapter is the most important section of the report" for the full rationale. **A weak Section 4 cannot be recovered by polishing the other sections.** Sections 5 (Customers), 6 (Industry), 7 (Competition), 8 (TAM), and 9 (Risks) all reference back to *what the company makes and how it sits in the customer's workflow*; if Section 4 is generic, every downstream section becomes hand-waving. Budget your time and word count accordingly: this section deserves more research effort than any other.

**Two requirements: precise and explanatory.**
- *Precise* = anchored to the issuer's own product matrix (embedded as an image + reproduced as markdown), with verbatim 10-K quotes for each product family, exact product names with trademark symbols, and competitor / share / leadership claims clearly labeled as analyst view (not attributed to the 10-K).
- *Explanatory* = for each product, three pedagogical beats (what it physically does → how it differs from sibling products → strategic inflection driving demand); bilingual technical terminology (Chinese AND English side-by-side) for cross-border-investing audiences; a synthesis paragraph at the end showing how the product categories compose a single customer workflow.

This is the section where reports most often degrade into either a flat product catalog or sell-side commentary dressed up as fact. Use the following structure to avoid both failure modes.

**(a) Anchor to the issuer's own product matrix — and embed the original page image, not just a reproduction.**

Most semiconductor / industrial / hardware / pharma issuers publish a product matrix in the 10-K / 年度报告 / Yuho Item 1 Business section — typically organized as Market → Process/Application → Technology → Products (or an equivalent for the industry: Therapeutic Area → Indication → Modality → Product, etc.).

**Two things must appear in 4.1:**
  1. **The 10-K's actual rendered table as a PNG image**, embedded via markdown (`![…](charts/<ticker>_10k_products_table.png)`), with a caption citing the 10-K. Render it with the helper script below (`render_10k_section.py`). The image is what makes Section 4 look authoritative — the reader can see the original filing source.
  2. **A markdown reproduction of the same table** below the image, so the content is searchable / accessible to screen-readers and so quoted product names can be linked.

If the issuer does not publish such a table, build one from the website's product navigation (citing the website) and label it explicitly as analyst-constructed.

**(b) Walk each row with verbatim 10-K quotes + bilingual pedagogy.**

For each product family in the matrix, follow this exact three-part pattern:

  1. **10-K verbatim (block quote).** Quote the 10-K's Product Family description directly — use `> "…"` markdown block-quote syntax with the inline 10-K citation right above the quote. Verbatim text from the issuer is by definition non-fabricated and gives the reader Lam's own explanation of what the product does.
  2. **Bilingual pedagogical explanation** introduced with the label `**中文释义 / Plain-language gloss:**`. Clearly labeled as the analyst's plain-language gloss, *not* attributed to the 10-K. This is where the analyst earns their pay: explain in 3–6 sentences (a) the underlying physics / process / mechanism using analogies where helpful, (b) how this product differs from its sibling products in the same matrix, and (c) the strategic inflection currently driving demand.
     - **For every technical term, give both Chinese AND English side-by-side** in the form `Chinese / English` or `English / Chinese` or `Chinese (English)`. Examples: `dielectric / 介质`, `通孔 (via)`, `wordline / 字线`, `CMP (chemical-mechanical planarization, 化学机械抛光)`, `gate-all-around (GAA, 栅极环绕)`. This serves bilingual readers (often the same reader: a Chinese-native analyst working in English-speaking firms, or vice versa) and prevents either-language vocabulary gaps from blocking comprehension.
     - **Code-switching freely is fine** — sentences can start in one language and end in the other, e.g., "SABRE 做的是 **电镀铜 / Cu electroplating (ECD)** —— 通过 electrochemical reaction 把 copper 长在 wafer 上, forming the **互连线 / interconnect**…". This compressed style is denser than either monolingual version because it leverages each language's strengths: Chinese for compact process names, English for proper-noun technologies and IUPAC chemistry.
     - For non-Chinese-reading audiences (e.g. company-research reports targeting US-domestic-only consumers), you may use the heading `**Plain-language gloss:**` alone and skip Chinese — but for any cross-border-investing context (any Chinese-listed company, any US semicap/EV/battery/biotech name with significant Chinese supply chain) the bilingual form is preferred.
  3. ***Analyst view:* sentence** — competitive context only, cited to the competitor's filing or website or a third-party research source, never to the subject's 10-K. Specific competitor product names (e.g. AMAT's NOKOTA, Producer, Endura) belong here.

**(c) End the section with a synthesis paragraph that shows how the product categories interact.** This is what makes a research report *pedagogical* rather than a catalog. For semicap, it's the Deposition → Etch → Clean → Deposition manufacturing cycle. For other industries, the equivalent: how the products compose a single customer workflow / use case / treatment regimen / installation. One paragraph; 3–5 sentences; explicit about which products sit at each step. Optionally include a small Mermaid LR or TD graph showing the loop.

**(d) Required elements regardless of structure:**
  - **Per-product competitive-advantage assessment.** For each material product, a one-clause verdict (yes / partial / no) plus the moat type (technology / IP / patents, scale, switching costs, network effects, regulatory, distribution, ecosystem lock-in) — under the `*Analyst view:*` label.
  - **Flagship vs. long-tail.** Identify the 1–3 products driving the current business (state revenue / unit-mix share if disclosed; otherwise flag as analyst estimate).
  - **Roadmap & recent launches.** Products launched, repositioned, or sunset in the last 12 months — with the company press release as the citation. If a new platform was launched (e.g. Akara, ALTUS Halo), block-quote the press release the same way you block-quote the 10-K.
  - **Recurring / aftermarket / services business.** Many issuers have a separate business group outside the product matrix (CSBG for Lam, Services for AMAT, etc.). Treat that as its own subsection — describe what it consists of, how it's reported in the financials, why it dampens cyclicality, and the recurring-revenue economics.
  - **IR primary input:** Section 4 should draw from the investor day deck's product / roadmap slides, the latest earnings deck's product-segment slides, and any industry-conference deck where the CEO walked product roadmap. **At least 2 IR-deck citations in Section 4** when the company publishes IR materials — typically the latest investor day deck (roadmap and TAM slides) plus the latest quarterly deck (segment-mix slide). Block-quote the slide text when the company's own framing is load-bearing, the same way you block-quote the 10-K.

**Rendering the issuer's product table as a PNG (for step (a))**

A reusable helper script lives at `.claude/skills/company-research/scripts/render_10k_section.py`. It takes a local 10-K HTML path, an anchor string (any unique text inside the target element — usually a product name), and an output path; it screenshots the located element at retina resolution and saves a PNG.

**One-time setup** (skip if playwright is already installed in the project):

```bash
pip install playwright
python3 -m playwright install chromium
```

**Usage:**

```bash
# Default: anchor by a product name inside the target <table>
python3 .claude/skills/company-research/scripts/render_10k_section.py \
    --html financial_reports/LRCX/<10-K-filename>.htm \
    --anchor SABRE \
    --output reports/company/<Slug>/charts/<ticker>_10k_products_table.png

# Or: specify a CSS selector directly
python3 .claude/skills/company-research/scripts/render_10k_section.py \
    --html financial_reports/<TICKER>/<10-K-filename>.htm \
    --selector "table.products" \
    --output reports/company/<Slug>/charts/<ticker>_10k_products_table.png \
    --pad-top 150  # extra header padding if the section title doesn't fit
```

**How it works internally:**
1. Launches headless chromium via playwright.
2. Loads the local 10-K HTML file via `file://` URL — works with the HTML SEC EDGAR serves; no network round-trip needed since the file is cached locally by `fetch_financial_report.py`.
3. Locates the target element either by `--anchor` (text-content filter on `<table>`) or by `--selector` (CSS selector).
4. Calls `page.screenshot(clip=bounding_box + padding)` to crop just the element + small padding to include the section heading and any caption.
5. Saves at `device_scale_factor=2` (retina) for crisp PNGs.

**Choosing a good anchor.** Pick a unique product or product-family name that appears only inside the target `<table>` — e.g. for Lam's product table, `SABRE` works because it's a unique product family. For Apple, `iPhone` would be too generic (appears across many tables); use a more specific anchor like `Mac Studio` or a sentence from a unique paragraph. If no unique anchor exists, fall back to `--selector` with a CSS path.

**For Chinese 年度报告 (cninfo PDFs)**, use `fitz` (PyMuPDF) to render the relevant page to PNG instead — see the project's `render_pdf_pages.py` pattern. The helper script above is HTML-only.

Save all rendered PNGs into `reports/company/<Slug>/charts/` so the relative `![](charts/...)` reference resolves from the markdown report.

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
- **NEVER mix segment-level customer concentration with consolidated / group-level customer concentration.** Every customer-share number must be labelled with its denominator ("X% of consolidated revenue" vs "X% of <Segment> segment revenue") — never an unqualified "X% of revenue" when more than one denominator could apply. Segment-level customer lists must carry a "(segment-level; not aggregated to group-level)" qualifier inline. A customer pie chart must use one denominator only — do not draw a single chart whose slices mix consolidated and segment-level shares. The filing's named top-5 (e.g. Samsung's 사업보고서 alphabetical list at ~14% group aggregate) overrides any reconstructed sell-side / supply-chain composite that disagrees. See the SKILL.md "Customer concentration" rule for the full spec and the Samsung-2024 worked example.
- **IR primary input:** IR decks often name customers the filing only references by category (e.g. "a leading hyperscaler"). Pull customer-logo slides, customer-cohort retention charts, geographic-mix Sankeys, NRR cohort charts from the latest investor day deck and recent quarterly decks — typically 1–2 IR citations in this section.
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
- **IR primary input:** Management's industry framing — every IR deck has 2–4 slides setting up the industry context (often clearer than the company's own filing). Pull these from the latest investor day deck and key industry-conference appearances. At least 1 IR citation here.

### 7. Competitive Landscape (700–1,000 words)
- Analysis of 5–10 key competitors (direct, indirect, emerging)
- Market positioning framework (price / features / scale dimensions)
- Company's competitive advantages
- Competitive vulnerabilities
- Market share analysis
- **IR primary input:** Investor day "Why we win" slides, side-by-side feature matrices, share-trajectory charts. **Handle with care** — these slides are self-serving by design — but the underlying data points are citable, and the *omission* of a key competitor on a competitive-positioning slide is itself signal. Often 1 IR citation here.

### 8. Market Opportunity / TAM (500–700 words)
- TAM sizing and methodology
- SAM and SOM
- Market growth projections
- Company's serviceable market and share opportunity
- Penetration strategy
- **IR primary input — most-cited source in this section.** The IR deck's TAM build slide is almost always the most-cited single TAM source in the report; management has done the build-up work and chained-cited the underlying research firm (Yole, Gartner, IDC, etc.). Cite the deck as primary with a source-chain label (e.g. `[Company Investor Day 2024 deck, Slide 23 — TAM (citing Yole 2024)](URL)`); chain-cite the underlying research firm as secondary. **Minimum 2 IR citations in Section 8** for any issuer that publishes a TAM build — typically the latest investor day deck plus the latest annual / Integrated Report.

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
