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

### Step 0 — Check the local report cache first (do this before going to the web)

Before downloading anything, check whether recent filings are already on disk. Re-downloading wastes time and bandwidth, and the local copy is what `db/financial_reports.db` / `db/cninfo_reports.db` already indexes.

- **US issuers** → `ls /Users/x/projects/financial_agent/financial_reports/<TICKER>/` (e.g. `financial_reports/NVDA/`). Look for the most recent 10-K, 10-Q, DEF 14A, 8-K.
- **Chinese A-share / HK issuers** → `ls /Users/x/projects/financial_agent/cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/` (e.g. `cninfo_reports/SZSE/002050_安培龙/`). Look for the most recent 年度报告, 季度报告, 半年度报告, 重大事项公告.
- The DBs hold the same listing: `sqlite3 db/financial_reports.db "SELECT ticker, report_type, report_date, filename FROM reports WHERE ticker='NVDA' ORDER BY report_date DESC LIMIT 10;"` and equivalently for cninfo.

**Freshness rule — fetch only if the cache is stale:**

- Annual report (10-K / 年度报告) older than **~13 months** → fetch the latest.
- Quarterly report (10-Q / 季度报告 / 半年度报告) older than **~4 months** → fetch the latest.
- Material events (8-K / 重大事项公告) — always check whether anything has been filed in the last 6 months; fetch if missing.
- If the cache covers the period you need, **use the local PDF** — do not re-download.

**To fetch (only when needed):**

- **US:**
  ```bash
  cd /Users/x/projects/financial_agent
  python3 fetch_financial_report.py <TICKER>
  ```
- **China A-share / HK:**
  ```bash
  cd /Users/x/projects/financial_agent
  python3 -c "import fetch_cninfo_report as cr; cr.init_db(); [print(m) for m in cr._run_download('SZSE:002050', cr.ALL_CATEGORIES)]"
  ```
  Always run from the main project dir so files land in `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/` and not in a worktree.

Read PDFs with `fitz` / Read tool. For image-only / scanned pages, follow the OCR flow in the project CLAUDE.md (ocrmac → Marker → vision-LM, never Tesseract).

### Step 1 — Initial data collection

1. **Thoroughly analyze the company website** (do not skim — this is the primary source of ground truth on what the company actually sells).
   - Read every About / Company / Mission page; note founders' framing.
   - **Walk the entire product / solutions navigation tree.** Enumerate every distinct product, SKU family, or service line — even 10–30+ items. Do not collapse them.
   - For each product page, capture: official name + variants/tiers, one-sentence description, target customer, pricing model if disclosed, key specs/differentiators the company highlights, any "new"/"flagship" badges.
   - Identify named customers, homepage logos, partner/integration lists, customer case studies.
   - Capture leadership / Team page (names, titles, prior employers) — feed into Step 3.
   - Read blog / newsroom for the **last 12 months** to detect launches, sunsets, repositioning.
   - For non-English companies, read the **native-language site** (e.g. `company.com.cn`) — English IR pages are often a stripped subset and miss SKUs.
2. **Regulatory filings** — start from the local cache pulled in Step 0; only fetch fresh if the cache is stale (see freshness rules above). Route by domicile per the data-sources table. Note filing dates and the portal used.
3. **Earnings materials** — latest transcript, latest investor presentation, last 12 months of press releases.
4. **Document basic facts** — founding date, HQ, employees, products/services, key customers.

### Step 2 — Valuation snapshot (always pull P/E and P/S)

Before business-model analysis, capture where the market is pricing the stock today. **Required for every public company; for private companies, substitute the latest funding-round post-money valuation and revenue multiple if disclosed.**

Pull from a market-data source:
- **US** → Yahoo Finance (`finance.yahoo.com/quote/<TICKER>/key-statistics`), Stockanalysis.com, or `yfinance` Python lib.
- **China A-share / HK** → Eastmoney 东方财富 (`quote.eastmoney.com/<code>.html`), Sina Finance (`finance.sina.com.cn`), or Tonghuashun (`10jqka.com.cn`). Use TTM (滚动) figures, not 静态 (static last-FY) — the static number is a year stale by the time you read it.
- **Taiwan** → Goodinfo (`goodinfo.tw`) or TWSE.
- **Japan** → Kabutan (`kabutan.jp`), Nikkei (`nikkei.com`).
- **Korea** → Naver Finance (`finance.naver.com`).

Capture: current price, market cap, **TTM P/E**, **TTM P/S**, plus P/B for capital-heavy businesses (banks, insurers, REITs, heavy industrials) and EV/EBITDA for leveraged or cyclical names. Note the 3-year (or since-IPO if shorter) range of each multiple so today's number has context.

**Then compare to peers and sector median.** Pull 3–5 closest comps' P/E and P/S; cite the source. The sector median anchors whether today's multiple is normal, stretched, or compressed.

**Interpret negative or extreme multiples — do not just report the number.** If you see:
- **Negative P/E** → the company is unprofitable on a TTM basis. Decompose: is it cash-burning growth (high-S&M, pre-scale SaaS, biotech R&D, pre-revenue hardware), a one-off (impairment, goodwill write-down, litigation charge), cyclical trough (semis, commodities, autos in a down year), or structural decline? Quote the line item from the latest 10-K / 年报 / Yuho that drives the loss.
- **Very high P/E (rule of thumb: > 50× TTM, or > 2× sector median)** or **very high P/S (> 15×, or > 3× sector median)** → name the cause. Common drivers: (a) genuine high-growth sector the market is pricing for years of compounding (AI infra, GLP-1, EV battery, advanced packaging), (b) earnings temporarily depressed (cyclical trough, heavy reinvestment, recent dilution), (c) thematic / narrative premium (the stock is a sector proxy even if fundamentals lag), (d) M&A or take-private speculation, (e) small float / illiquidity inflating the multiple. **Say which one — and back it with a citation** (sell-side note, earnings call language, sector ETF flows, a comparable that re-rated similarly).
- **Very low P/E (< 8×) or low P/S** → also worth a sentence: value trap (declining business, dividend at risk), cyclical peak (earnings unsustainable), governance / accounting concern, or genuine mispricing.

Feed the verdict into Section 1 (Company Overview → Valuation snapshot) and, if the multiple is stretched enough to be a risk (P/E > 50× with no clear earnings path, P/S > 20× outside top-quartile growth), into Section 9 as a valuation / multiple-compression risk.

### Step 3 — Business model analysis

Map revenue streams (what's sold, pricing, who pays, deal size), customer segments (enterprise/SMB/consumer, industries, geography, concentration), go-to-market (direct vs. channel, sales cycle, acquisition strategy), and unit economics (LTV/CAC, gross margins, NRR, payback) where available.

**Customer concentration — quantify it, do not just describe it.** Most jurisdictions require disclosure of large-customer exposure; pull the numbers and judge the risk.

- **US 10-K** → ASC 280-10-50-42 requires naming customers ≥10% of consolidated revenue in segment notes; the "Customer Concentration" risk factor often gives more color. Search the 10-K for "10%", "major customer", "customer concentration".
- **China A-share / HK 年度报告** → mandatory section reports `前五名客户合计销售金额` and `占年度销售总额比例` (top-5 customer sales and % of total revenue), and often the top single customer's share. Search the PDF for `前五大客户`, `前五名客户`, `客户集中度`.
- **Taiwan 年報** → top-5 customers typically disclosed (`主要客戶`).
- **Japan Yuho (有価証券報告書)** → `主要な販売先` lists customers ≥10% of net sales by segment.
- **Korea 사업보고서 (DART)** → `주요 매출처` / top customer disclosure in the business overview.
- **Private / no filing** → press releases, case studies, customer logos on the site, and interviews; flag explicitly that the number is estimated, not disclosed.

Capture: top-1 customer % of revenue, top-5 %, multi-year trend (3 years if available), whether top customers are named, contract structure (master agreement vs. PO-by-PO, multi-year vs. annual), and whether any top customer is also a competitor / vertically integrating / building in-house. **If top-1 > 20% or top-5 > 50%, treat as a material risk and call it out in both Section 5 and Section 9.** If disclosure is missing or vague, say so — do not paper over it.

### Step 4 — Management research

**The CEO / founder is the most important bio — spend the most depth there.** A strong founder-CEO is often the single biggest long-run driver; the rest of the team is supporting cast.

1. **CEO / founder (250–350 word bio, deeper if founder-led / supervoting / unusually consequential).** Pull from LinkedIn, DEF 14A / proxy, press interviews, podcasts, shareholder letters. Capture prior 2–3 roles with *what they specifically accomplished* (numbers not titles), education, tenure at this company, ownership stake, comp structure, public profile. If founder, also the founding thesis and whether they still own materially.
2. **CFO (150–200 words).** Prior roles, IPO / M&A / capital-markets track record, prior public-company CFO experience.
3. **1–2 other execs (80–120 words each).** Pick by thesis relevance — CTO at a chip co, CRO at sales-led SaaS, head of largest segment at a conglomerate.
4. **Governance (80–150 words).** Board composition / independence, insider ownership %, comp structure (cash vs. equity, perf-linked %), related-party transactions, governance flags.
5. **Track record synthesis (50–100 words).** Has this team delivered before? Where are the gaps?

### Step 5 — Competitive intelligence

1. Identify 5–10 competitors — direct, indirect, emerging. Cross-check the company's 10-K / 年度报告 for its own competitor list.
2. For each: visit website, review filings if public, note products, differentiators, market-share estimates.
3. Build a positioning framework (price / features / scale). Identify advantages, vulnerabilities, switching costs, network effects.

### Step 6 — Industry analysis

Define the industry (NAICS/SIC, scope, adjacent industries). Size the market (TAM/SAM/SOM, penetration). Research growth drivers (historical and projected rates, key trends, tech changes). Understand structure (fragmented vs. consolidated, barriers, supplier/buyer power, substitutes, regulation).

### Step 7 — Risk assessment

Identify 8–12 risks across 4 buckets (company-specific, industry/market, financial, macro). See `references/risk_taxonomy.md` for the full taxonomy. 50–100 words per risk: describe, quantify, note mitigants.

### Step 8 — Charts and diagrams (add 4–8 visuals)

A report this length needs visual anchors. **Add 4–8 charts/diagrams** across the document. Two flavors — use both:

**A. PNG charts via matplotlib (quantitative trends).** Generate with a Python script, save into `reports/charts/<company>_<chart>.png`, embed via `![alt](charts/<company>_<chart>.png)`. Pattern-match from existing scripts in `oneoff/` (`anpeilong_3yr_chart.py`, `cdns_5yr_chart.py`). End the script with `plt.savefig(path, dpi=150, bbox_inches="tight")`.

Suggested: 3–5 yr revenue + gross margin trend (dual-axis); segment revenue mix (stacked bar); TTM P/E vs. 3-yr range vs. sector median; peer comparison bars; latest 8–12 quarter trend if seasonality matters.

**B. Mermaid diagrams (structural / qualitative).** Markdown-native; the web viewer and GitHub render them inline. Wrap in a ` ```mermaid ` fence. Use for:

- **Timeline** (Section 2 History): `timeline` block — founding → IPO → segment launches → recent milestones
- **Product portfolio tree** (Section 4 Products): `graph TD` mapping company → segments → product families → SKUs
- **Customer concentration** (Section 5): `pie title FY2024 revenue by top customers` with the top 3–5 customers + "All other"
- **Competitive positioning** (Section 7): `quadrantChart` (2×2) on price vs. feature-breadth, or `graph LR` for value-chain position
- **Org / governance** (Section 3): optional `graph TD` for board / management reporting lines

**Placement summary** (also in `references/report_structure.md`):
| Section | Chart |
|---|---|
| 1 Overview | Revenue + margin trend (PNG) |
| 2 History | Mermaid timeline |
| 4 Products | Mermaid product tree |
| 5 Customers | Mermaid customer-concentration pie |
| 7 Competitive | Mermaid quadrant **or** peer-comparison bars (PNG) |
| 8 TAM | Market-size growth chart (PNG) |

**Every chart gets a citation right below it** — same markdown-link format as prose, e.g. `Source: [安培龙 2024 年度报告, 第 32 页](https://static.cninfo.com.cn/...)`. No chart without a source.

### Step 9 — Synthesis and writing

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
