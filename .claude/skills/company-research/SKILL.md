---
name: company-research
description: Produce a deep 6,000–10,000 word company research report (business, management, products, customers, industry, competitive landscape, TAM, risks) for a public or private company. Output is saved as markdown to the project-level `reports/` folder. Use when the user asks to "research", "deep-dive", "profile", or "initiate coverage on" a specific company or ticker — e.g. "research Tesla", "deep dive on PLTR", "company research for SZSE:002050".
---

# Company Research

Deep research deliverable: a 6,000–10,000 word markdown report covering business, management, products, customers, industry, competitive landscape, TAM, and risks. Input is just a company name or ticker.

## Report language

**Always write the report's prose in English**, regardless of the company's domicile, listing, or the language of its primary filings. The user's prompt language does not change this — a request in Chinese about `SZSE:002050` still gets an English report.

**Chinese names and bilingual technical terms are allowed inline:**
- **Chinese company names** (the subject company or a Chinese competitor / customer / partner) may appear in their original Chinese form alongside an English / pinyin gloss on first mention, e.g. `安培龙 (Anpeilong, SZSE:002050)`, `比亚迪 (BYD)`, `宁德时代 (CATL)`. After the first mention, either form is fine.
- **Technical terms** with no clean English equivalent (industry jargon, regulatory categories, product certifications, government program names) may be written bilingually, e.g. `"专精特新" (specialized, refined, distinctive, novel — MIIT designation for niche SMEs)`, `国六排放标准 (China VI emission standard)`. Prefer English when an established English term exists.
- Direct quotations from Chinese filings stay in Chinese (per the citation rule); add a parenthetical English translation if the quote is load-bearing.

Source citations preserve the **original** language of the document (see "Citations preserve the original source language" below) — e.g. `(Source: 2024 年度报告, p. 28)` inside English-language prose. Do not translate source titles.

Filenames may include Chinese characters when the subject company is Chinese: `reports/安培龙_SZSE002050_Research_Document_2026-05-16.md` is fine; `reports/Tesla_Research_Document_2024-10-27.md` is fine. No Japanese kana / kanji or Korean hangul in filenames.

## Citations

Every inline citation is a **clickable markdown link to the real source URL** — `[Title in original language](https://real-url)` — never a bare `(Source: ...)` parenthetical. Link titles preserve the original language (`年度报告`, `10-K`, `決算短信`, `사업보고서`); URLs are canonical permalinks (the actual SEC EDGAR document URL, the specific cninfo PDF, the article permalink — not homepages). No fabricated URLs — if you cannot find the real link, say so inline.

See [`references/citations.md`](references/citations.md) for the full rules, per-source examples, and the final References-block format. **Read it before drafting.**

## Reference docs (read on demand)

- `references/report_structure.md` — section-by-section word counts, per-section content spec, and the full output template. **Read before writing.**
- `references/citations.md` — inline-citation rules and example.
- `references/risk_taxonomy.md` — the 8–12 risks across 4 buckets used in Section 9.
- `references/quality_checklist.md` — quality standards and the pre-submit success checklist.

---

## Data sources — route filings by domicile

**SEC EDGAR only covers US issuers. Do not look for non-US filings there.**

- **US** → SEC EDGAR: latest 10-K, recent 10-Qs, DEF 14A, recent 8-Ks. Helper: `fetch_financial_report.py` (DB: `db/financial_reports.db`).
- **China A-share / HK** → cninfo (巨潮资讯, https://www.cninfo.com.cn/): 年度报告, 季度报告 / 半年度报告, 重大事项公告. Ticker format `SZSE:002050`, `SSE:688802`, `HKEX:2513`. Helper: `fetch_cninfo_report.py` — run from `/Users/x/projects/financial_agent` so files land in `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/`. Chinese-language disclosures are authoritative; English IR pages are secondary.
- **Taiwan (TWSE / TPEx)** → MOPS (公開資訊觀測站, https://mops.twse.com.tw/): 年報, Q1–Q3 reports, 重大訊息.
- **Japan** → EDINET (https://disclosure2.edinet-fsa.go.jp/) for Yuho (有価証券報告書) + Shihanki (四半期報告書); TDnet (https://www.release.tdnet.info/) for 決算短信. English IR PDFs ("Integrated Report") on the company site for narrative.
- **Korea** → DART (https://dart.fss.or.kr/, English: https://englishdart.fss.or.kr/): 사업보고서, 반기보고서, 분기보고서, 주요사항보고서.
- **Other** → country's official portal (SEDAR+ Canada, ASX Australia, LSE RNS UK, BSE/NSE India). Do NOT fall back to SEC EDGAR unless the issuer is a 20-F / 6-K filer.
- **Private companies** → company website + blog, press coverage, LinkedIn for bios, Crunchbase/PitchBook for funding history.

Secondary sources (any domicile): competitor websites and filings, Gartner/Forrester/IDC industry reports, trade press, LinkedIn for executive bios.

---

## Workflow

### Step 1 — Initial data collection

1. **Thoroughly analyze the company website** (do not skim — this is the primary source of ground truth on what the company actually sells).
   - Read every About / Company / Mission page; note founders' framing.
   - **Walk the entire product / solutions navigation tree.** Enumerate every distinct product, SKU family, or service line — even 10–30+ items. Do not collapse them.
   - For each product page, capture: official name + variants/tiers, one-sentence description, target customer, pricing model if disclosed, key specs/differentiators the company highlights, any "new"/"flagship" badges.
   - Identify named customers, homepage logos, partner/integration lists, customer case studies.
   - Capture leadership / Team page (names, titles, prior employers) — feed into Step 3.
   - Read blog / newsroom for the **last 12 months** to detect launches, sunsets, repositioning.
   - For non-English companies, read the **native-language site** (e.g. `company.com.cn`) — English IR pages are often a stripped subset and miss SKUs.
2. **Regulatory filings** — route by domicile per the table above. Note filing dates and the portal used.
3. **Earnings materials** — latest transcript, latest investor presentation, last 12 months of press releases.
4. **Document basic facts** — founding date, HQ, employees, products/services, key customers.

### Step 2 — Business model analysis

Map revenue streams (what's sold, pricing, who pays, deal size), customer segments (enterprise/SMB/consumer, industries, geography, concentration), go-to-market (direct vs. channel, sales cycle, acquisition strategy), and unit economics (LTV/CAC, gross margins, NRR, payback) where available.

**Customer concentration — quantify it, do not just describe it.** Most jurisdictions require disclosure of large-customer exposure; pull the numbers and judge the risk.

- **US 10-K** → ASC 280-10-50-42 requires naming customers ≥10% of consolidated revenue in segment notes; the "Customer Concentration" risk factor often gives more color. Search the 10-K for "10%", "major customer", "customer concentration".
- **China A-share / HK 年度报告** → mandatory section reports `前五名客户合计销售金额` and `占年度销售总额比例` (top-5 customer sales and % of total revenue), and often the top single customer's share. Search the PDF for `前五大客户`, `前五名客户`, `客户集中度`.
- **Taiwan 年報** → top-5 customers typically disclosed (`主要客戶`).
- **Japan Yuho (有価証券報告書)** → `主要な販売先` lists customers ≥10% of net sales by segment.
- **Korea 사업보고서 (DART)** → `주요 매출처` / top customer disclosure in the business overview.
- **Private / no filing** → press releases, case studies, customer logos on the site, and interviews; flag explicitly that the number is estimated, not disclosed.

Capture: top-1 customer % of revenue, top-5 %, multi-year trend (3 years if available), whether top customers are named, contract structure (master agreement vs. PO-by-PO, multi-year vs. annual), and whether any top customer is also a competitor / vertically integrating / building in-house. **If top-1 > 20% or top-5 > 50%, treat as a material risk and call it out in both Section 5 and Section 9.** If disclosure is missing or vague, say so — do not paper over it.

### Step 3 — Management research

For each of 3–4 key executives (CEO + CFO required; pick 1–2 more from C-suite):
1. Find LinkedIn, DEF 14A / proxy bio, press interviews. Note tenure.
2. Write a 300–400 word bio: current role, prior 2–3 roles, accomplishments, education, years in industry, time at company.
3. Assess governance: board composition/independence, key board members, insider ownership, comp structure.

### Step 4 — Competitive intelligence

1. Identify 5–10 competitors — direct, indirect, emerging. Cross-check the company's 10-K / 年度报告 for its own competitor list.
2. For each: visit website, review filings if public, note products, differentiators, market-share estimates.
3. Build a positioning framework (price / features / scale). Identify advantages, vulnerabilities, switching costs, network effects.

### Step 5 — Industry analysis

Define the industry (NAICS/SIC, scope, adjacent industries). Size the market (TAM/SAM/SOM, penetration). Research growth drivers (historical and projected rates, key trends, tech changes). Understand structure (fragmented vs. consolidated, barriers, supplier/buyer power, substitutes, regulation).

### Step 6 — Risk assessment

Identify 8–12 risks across 4 buckets (company-specific, industry/market, financial, macro). See `references/risk_taxonomy.md` for the full taxonomy. 50–100 words per risk: describe, quantify, note mitigants.

### Step 7 — Synthesis and writing

Read `references/report_structure.md` for the 9-section spec and full output template. Read `references/citations.md` before drafting — inline citations are required in every section, not just at the end. Before declaring done, run through `references/quality_checklist.md` and verify total word count with `wc -w`.

---

## Output location

Save to the **project-level `reports/` folder**: `/Users/x/projects/financial_agent/reports/`. Create it if missing.

File name: `reports/[Company]_Research_Document_[YYYY-MM-DD].md` — `[Company]` may use Chinese characters for Chinese companies; otherwise ASCII. No Japanese kana / kanji or Korean hangul.
Examples:
- `reports/Tesla_Research_Document_2024-10-27.md`
- `reports/安培龙_SZSE002050_Research_Document_2026-05-16.md`
- `reports/Anpeilong_SZSE002050_Research_Document_2026-05-16.md`
- `reports/Toyota_TSE7203_Research_Document_2026-05-16.md`

Always write to the main project's `reports/` directory — never to a worktree, `~/Downloads`, or any other location.
