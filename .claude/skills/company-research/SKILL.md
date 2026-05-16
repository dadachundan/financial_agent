---
name: company-research
description: Produce a deep 6,000–8,000 word company research report (business, management, products, customers, industry, competitive landscape, TAM, risks) for a public or private company. Output is saved as markdown to the project-level `reports/` folder. Use when the user asks to "research", "deep-dive", "profile", or "initiate coverage on" a specific company or ticker — e.g. "research Tesla", "deep dive on PLTR", "company research for SZSE:002050".
---

# Company Research

Deep research deliverable: a 6,000–8,000 word markdown report covering business, management, products, customers, industry, competitive landscape, TAM, and risks. Input is just a company name or ticker.

## Report language

The report is written in **exactly one of two languages**: Simplified Chinese or English. Never Traditional Chinese, never Japanese, never Korean.

**The rule follows the company's primary listing / filings, not its country of origin:**

- **Simplified Chinese (zh-CN)** — when the primary filings are in Chinese:
  - A-share: `SSE:` / `SZSE:` issuers (filings: 年度报告, 季度报告 on cninfo)
  - HK main board / GEM: `HKEX:` issuers (filings: 年報, mostly bilingual but Chinese is authoritative)
  - Taiwan: `TWSE:` / `TPEx:` issuers (filings: 年報 on MOPS, in Traditional Chinese — translate analysis to Simplified Chinese; keep source titles original per citation rule)
- **English** — for everything else, including:
  - US-listed companies (NYSE / NASDAQ), regardless of country of origin. This includes **Chinese ADRs and US-listed Chinese companies** (e.g. BABA, PDD, BIDU, JD, NIO) whose primary filings are 10-K / 20-F / 6-K in English on SEC EDGAR. Even if the company also has an A-share or HK listing, if the user gives a US ticker, the report is in English.
  - Japan, Korea, Europe, ASEAN, India, Australia, Canada, etc.
- **Dual-listed companies**: language follows the listing the user named. `BABA` → English (US ADR); `9988.HK` / `HKEX:9988` → Simplified Chinese (HK listing). When ambiguous, default to English.
- Domicile alone is not the deciding factor; the **filing language** is. Country of origin matters only when the company is unlisted in the US and primarily files in Chinese.
- Prompt language never overrides this rule: a user asking in English about `SZSE:002050` still gets a Chinese report; a user asking in Chinese about Tesla or BABA still gets an English report.
- When writing in Chinese, use Chinese section headers (公司概览, 公司历史, 管理团队, 产品与服务, 客户与上市策略, 行业概览, 竞争格局, 市场机会, 风险评估, 参考资料) and target 6,000–8,000 字 (counting Chinese characters).
- Filenames: Chinese reports may use Simplified Chinese characters in `[Company]`; English reports use ASCII. Examples: `reports/安培龙_SZSE002050_公司研究_2026-05-16.md`, `reports/Tesla_Research_Document_2026-05-16.md`, `reports/Alibaba_BABA_Research_Document_2026-05-16.md`.

## Citations preserve the original source language

Regardless of the report's main language, **cite each source in the language it was published in.** Do not translate source titles, document names, exchange portals, or direct quotations — translating drifts away from the authoritative wording and makes the citation un-verifiable.

- Chinese filings stay Chinese in citations: `(来源: 2024 年度报告, 第 28 页, cninfo SZSE:002050)`, `(Source: 2024 年度报告, p. 28, cninfo SZSE:002050)` — both are fine; the **document title** must remain `年度报告`, not "Annual Report".
- Japanese filings: keep `有価証券報告書`, `四半期報告書`, `決算短信` as-is.
- Korean filings: keep `사업보고서`, `반기보고서`, `분기보고서`.
- US filings: `10-K`, `10-Q`, `DEF 14A`, `8-K` stay in English even in a Chinese-language report.
- Direct quotations are quoted in the original language. Add a short translation in parentheses only if the quote is load-bearing for a non-speaker reader.
- News articles / industry reports: keep the original title; add an English/Chinese gloss in brackets only if helpful.
- URLs are never translated.

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

File name: `reports/[Company]_Research_Document_[YYYY-MM-DD].md` — Simplified Chinese characters allowed in `[Company]` for CN/HK/TW reports; ASCII only for English reports. No Japanese kana / kanji or Korean hangul in filenames.
Examples:
- `reports/Tesla_Research_Document_2024-10-27.md`
- `reports/安培龙_SZSE002050_公司研究_2026-05-16.md`
- `reports/Toyota_TSE7203_Research_Document_2026-05-16.md` (Japanese issuer → English report)

Always write to the main project's `reports/` directory — never to a worktree, `~/Downloads`, or any other location.
