---
name: company-research
description: Produce a deep 6,000–10,000 word company research report (business, management, products, customers, industry, competitive landscape, TAM, risks) for a public or private company. Output is saved as markdown to `reports/company/<Company_Ticker>/` under the project root. Use when the user asks to "research", "deep-dive", "profile", or "initiate coverage on" a specific company or ticker — e.g. "research Tesla", "deep dive on PLTR", "company research for SZSE:002050".
---

# Company Research

Deep research deliverable: a 6,000–10,000 word markdown report covering business, management, products, customers, industry, competitive landscape, TAM, and risks. Input is just a company name or ticker.

## Core principle: accuracy over completeness — never hallucinate

This is the **single most important rule** and overrides every other instruction in this skill. The report is read by investors making real decisions; a single fabricated number, executive name, customer name, page reference, market-share figure, or URL destroys the credibility of the entire document.

**Hard rules:**

- **Never invent specific facts.** Revenue figures, growth rates, customer names, competitor market shares, executive backgrounds, board members, founding dates, product launch dates, TAM numbers, page numbers in filings, URLs — every one of these must come from a source you actually verified. If you didn't read it, don't write it.
- **If the data is not available, say so.** Write `disclosure not found` / `not disclosed in 10-K` / `cninfo filing does not break this out` / `private — not disclosed`. Omitting a section or stating an absence is **always preferable to inventing a plausible-looking number**.
- **No "this is probably around X."** No back-of-envelope estimates dressed as facts. If you need to estimate, mark it explicitly (`est., based on [reasoning]`) and show the math.
- **Cross-check every quantitative claim against its citation.** Before pasting "revenue grew 34% YoY" with a 10-K link, confirm the 10-K actually shows 34%. The citation must support the claim — not vaguely cover the topic.
- **Page numbers and dates must be exact.** If you cite `2024 年度报告, 第 28 页`, page 28 must be where the figure actually lives. If unsure, drop the page reference and cite the document only.
- **No fabricated URLs** (this echoes the citation rule). For SEC filings, always look up the real filename via the EDGAR submissions JSON API (`https://data.sec.gov/submissions/CIK<10-digit-padded>.json` — see `references/citations.md`); never invent synthetic filename patterns like `2025_10K_<accession>.htm` — those are 404s.
- **Direct quotations must be verbatim.** If you can't quote exactly, paraphrase and drop the quote marks.
- **Distinguish primary (filings, transcripts) from secondary (news, third-party) sources.** When two sources disagree, prefer the primary and note the discrepancy briefly.

### Specific failure mode: do NOT misattribute sell-side opinions to filings

A 10-K / 年度报告 / Yuho is a legal disclosure document. It almost never contains:
- Specific competitor product names (e.g. AMAT's "NOKOTA", "Producer", "Endura")
- Share-leadership claims about itself ("Lam is the leader", "dominant in X", "near-monopoly share")
- Revenue percentages by sub-product category (e.g. "Etch is 45% of Systems revenue")
- Co-leader / #1 / #2 rankings

These are sell-side analyst assessments. **Do not attach a 10-K citation to a sentence that makes one of these claims unless the 10-K verbatim says it.** Instead, prefix the sentence with `*Analyst view:*` (English) or `*分析师观点：*` (Chinese) and either leave it uncited or cite a real industry-research source (Yole, Gartner, IDC) at a specific URL.

What the 10-K Competition section typically does contain — and what you CAN cite to it — is a high-level list of named competitors (e.g. "Our primary competitors in the etch market are Applied Materials, Hitachi Ltd., and Tokyo Electron"). Quote that verbatim with a 10-K citation; do not embellish.

**When in doubt, omit.** A shorter, fully-sourced report is far more valuable than a padded one with invented detail. Length targets in `references/report_structure.md` are guides, not licenses to fabricate.

## The Products & Services chapter is the most important section of the report

After the "accuracy over completeness" rule, this is the next-highest-priority instruction. **Section 4 (Products & Services) is the single most consequential chapter in the entire report**, and a report that under-invests in Section 4 cannot be recovered by polishing the other sections.

**Why Section 4 carries this weight:**

1. **It is the analytical foundation for everything else.** A reader cannot evaluate Section 5 (Customers — *why* do customers buy this?), Section 6 (Industry — *what market* is the company in?), Section 7 (Competitive Landscape — *who* competes on *what*?), Section 8 (TAM — *what slice* of the market does the company actually serve?), or Section 9 (Risks — *which* products are most at risk?) without first understanding what the company actually makes and how it sits in its customer's workflow. Bury or generalize Section 4, and every downstream section becomes hand-waving.

2. **It is the chapter most often fabricated by the generating model.** Section 4 is exactly the kind of content where the model is tempted to invent plausible-sounding specifics: product feature lists that sound right, competitor product names that exist somewhere but not in the cited filing, revenue-by-product percentages that are never disclosed, "Lam is the leader in X" claims with a 10-K citation that doesn't say that. The Step 10 verification pass exists primarily because of how often Section 4 fails.

3. **It is the chapter that distinguishes a serious research report from a Wikipedia summary.** Sections 1, 2, 3, 6, 8 can be written by anyone with a Bloomberg terminal and a wiki crawler. Section 4, done well, requires reading the issuer's 10-K product table line by line, quoting it verbatim, and explaining what each product physically *does* in the customer's manufacturing / clinical / software flow. The reader's ability to say "now I understand why this company matters to its customers" is built or lost here.

**The two requirements for Section 4 — be precise, and be explanatory.**

### Precise

- **Anchor to the issuer's own product matrix.** Most 10-Ks / 年度报告 / Yuho contain a Product matrix or Product Family table in Item 1 Business. **Embed the rendered original table as a PNG image** via the helper at `.claude/skills/company-research/scripts/render_10k_section.py`, *and* reproduce it as a markdown table immediately below. The image is the visual proof that Section 4 is anchored to primary disclosure; the markdown reproduction is the searchable copy. If the issuer does not publish such a table, build one from the company website (cited) and label it as analyst-constructed.
- **Quote the issuer's own product descriptions verbatim** for each row of the matrix. Use `>` markdown block-quote syntax with the inline 10-K citation directly above the quote. Verbatim text from the issuer is by definition non-fabricated, and it gives the reader Lam's / 三星's / Pfizer's own explanation of what the product does in their words. **Do not paraphrase the 10-K — quote it.** Paraphrase is where fabrication enters.
- **Every product name spelled exactly as the issuer spells it**, including trademark symbols (®, ™), capitalization conventions, and platform-name prefixes (e.g. `ALTUS®`, not `Altus`; `Sense.i®`, not `Sense-i`).
- **Every technical specification** (e.g. "etches channels >10µm deep at <0.1% CD deviation and 2.5× faster", "delivers 50%+ reduction in word-line resistance", "100× faster plasma response") comes verbatim from the issuer's press release or 10-K, with a citation. Numbers without a source are deleted.
- **Competitor product names are cited to the competitor's own filing or website**, never to the subject company's 10-K. The subject's 10-K Competition section lists competitor *companies*, not products.
- **Analyst opinions are clearly labeled** as `*Analyst view:*` (or `*分析师观点：*`) and either cite a real industry-research source (Yole, Gartner, IDC, TrendForce — at a specific report URL) or stand uncited. They are never wrapped in a fake 10-K citation.

### Explanatory

- **Walk every product family with three pedagogical beats.** For each row in the issuer's matrix, write a paragraph that covers:
  1. **What it physically does** in the customer's value-chain flow. Concrete physical role — not marketing prose. ("Electroplates copper to form the interconnect lines that carry signals between transistors", not "delivers advanced metallization solutions".)
  2. **How it differentiates from sibling products** in the same matrix. The reader should leave able to explain why a fab needs SABRE *and* ALTUS *and* VECTOR — not just "Lam sells deposition tools". Cross-reference to the other rows: "Unlike SABRE (which plates copper for interconnect), ALTUS deposits tungsten or molybdenum for the deeper contacts and word-lines…"
  3. **Strategic significance**: what technology inflection, customer build-out, or end-market wave is currently driving demand (HBM ramp, GAA logic transition, 400-layer NAND, advanced-packaging build-out, GLP-1 prescription growth, etc.). Cite the press release / 10-K Products text / earnings-call language for the inflection.
- **For technical concepts, give both Chinese AND English side by side**, in `Chinese / English` or `English / Chinese` or `Chinese (English)` form. Examples: `dielectric / 介质`, `wordline / 字线`, `gate-all-around (GAA, 栅极环绕)`, `high aspect ratio (HAR, 高纵横比)`, `wafer-level packaging (WLP, 晶圆级封装)`. Code-switching freely within a sentence is encouraged — each language carries the term it expresses most compactly. The bilingual gloss is introduced with `**中文释义 / Plain-language gloss:**` so the reader knows it's the analyst's gloss, not 10-K text. (For US-domestic-only audiences with no Chinese exposure, you may drop the Chinese; but for any cross-border-investing context, bilingual is the preferred form.)
- **End the section with a synthesis paragraph that shows how the product categories interact.** For semicap: the Deposition → Etch → Clean → Deposition manufacturing cycle. For pharma: discovery → preclinical → clinical → marketed. For industrial automation: cell → line → plant. Optionally a small Mermaid graph showing the loop. This is the "now you understand why each product matters" payoff.
- **Use analogies where they accelerate understanding.** "TSVs are the vertical 'elevator shafts' between stacked DRAM die"; "bevel cleaning is like trimming the wafer's edge before particles flake back onto the device area"; "Striker ALD is the atomic-precision insulator tool used where SiO₂ gapfill has zero tolerance for voids." Analogies are uncited (they're the analyst's pedagogical device) — but they must be physically accurate, not loose metaphors.

**Length and depth target for Section 4: 700–1,500 words** — meaningfully longer than every other section except possibly Industry Overview. If your draft has Section 4 at 500 words and Section 6 at 1,200 words, the priority is wrong; cut Section 6 and expand Section 4.

**Specific failure modes that disqualify Section 4 — fix before declaring done:**

- A flat list of product names with no explanation of what each does → not a research report, it's a product catalog.
- Competitive-position language ("dominant", "leader", "co-leader", "near-monopoly share") attached to a 10-K citation → misattribution; relabel as analyst view.
- Revenue percentages by sub-product category attributed to the 10-K → fabrication unless the company actually publishes the split; label as analyst estimate.
- Specific competitor product names (e.g. "AMAT's NOKOTA") attached to the subject's 10-K → wrong citation chain; cite competitor's own filing.
- Marketing language from the company's homepage substituted for 10-K verbatim quotes ("delivers cutting-edge solutions for advanced manufacturing") → not what 10-K says; replace with verbatim quote.
- A "synthesis" paragraph that just repeats the section structure rather than showing how products interact → re-write to show the actual customer workflow / cycle.
- No image embed of the issuer's own product table → the section reads like analyst opinion without primary anchor; run `render_10k_section.py` to fix.

See `references/report_structure.md` § Section 4 for the per-row template, and `references/quality_checklist.md` for the pre-submit checklist.

## Report language

Two options only: **Simplified Chinese (zh-CN)** or **English**. Never Traditional Chinese, Japanese, or Korean for the prose.

**Decision rule:**

- **Listed in China / HK / Taiwan AND primary financial reports are in Chinese → write the report in Simplified Chinese.**
  - China A-share (`SSE:` / `SZSE:`) → always Chinese (filings: 年度报告, 季度报告 — all in Chinese).
  - HK (`HKEX:`) → Chinese when the issuer files in Chinese as primary (most mainland-domiciled HK names: 比亚迪, 安踏, 美团, etc.). For HK issuers whose primary filings are English (HSBC, Prudential, AIA, Standard Chartered, etc.) → English.
  - Taiwan (`TWSE:` / `TPEx:`) → Simplified Chinese for the prose (translate Traditional Chinese filings into Simplified; source titles stay in their original Traditional form per the citation rule).
- **Everything else → English.** US listings (including Chinese ADRs like BABA, PDD, JD, NIO whose 10-K / 20-F are in English), Japan, Korea, Europe, ASEAN, India, etc.
- Domicile alone does not decide it — the **listing + filing language** does. A user's prompt language alone does not override (a request phrased in Chinese about Tesla still defaults to English; a request phrased in English about `SZSE:002050` still defaults to Chinese).

**Explicit user override (highest priority).** The user can pin the language with any of these phrasings; honor it without asking:

| User says | Force output |
|---|---|
| `"... in English"`, `"write in English"`, `"English report"`, `"--lang en"`, `"--en"` | English only |
| `"... in Chinese"`, `"用中文"`, `"中文报告"`, `"写成中文"`, `"--lang zh"`, `"--zh"` | Simplified Chinese only |
| `"in both English and Chinese"`, `"bilingual"`, `"中英双语"`, `"both languages"`, `"Chinese and English"`, `"--lang en+zh"`, `"--bilingual"` | **Both** — produce two separate report files |

Examples:
- `research SZSE:002050 in English` → English report (override beats auto-rule)
- `research Tesla 用中文` → Chinese report (override beats auto-rule)
- `research NVDA in both English and Chinese` → two files: English + Chinese
- `research 比亚迪 bilingual` → two files: Chinese + English
- `research 比亚迪` (no override) → Chinese (auto-rule: HK + Chinese filings)
- `research NVDA` (no override) → English (auto-rule: US listing)

**Bilingual mode produces two complete, separate files in the same output folder**, not one interleaved document. Each file independently meets the 6,000–10,000 word target (Chinese counted in characters). Filenames follow the per-language convention (no date suffix — see the "Filenames" section below):

- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md` (English)
- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_公司研究.md` (Chinese)

Both files share the same underlying research — citations, charts, data — but write the prose natively in each language; do not literal-translate one from the other.

If the user gives no explicit instruction, fall back to the auto-rule above. If the override is ambiguous (e.g. "English summary, Chinese body"), ask one quick clarifying question rather than guessing.

**Bilingual technical terms (Chinese reports):** since most sources you cite will be Chinese, but many technical / industry / regulatory terms originate in English (or have established English equivalents), **use both** on first mention and either thereafter. Examples:
- `EV / 电动车`, `半导体 (semiconductor)`, `先进封装 (advanced packaging)`, `数据中心 GPU (data-center GPU)`, `OEM / ODM`, `Tier-1 供应商`, `毛利率 (gross margin)`, `自由现金流 (free cash flow)`, `专精特新 ("specialized, refined, distinctive, novel" — MIIT designation)`.
- Keep ticker codes and acronyms in their original form: `SZSE:002050`, `H200`, `RMB`, `USD`, `bp`, `YoY`, `QoQ`.

**Chinese names in English reports:** Chinese companies (subject, competitor, customer, partner) may appear in their original Chinese form alongside an English / pinyin gloss on first mention, e.g. `安培龙 (Anpeilong, SZSE:002050)`, `比亚迪 (BYD)`, `宁德时代 (CATL)`. After first mention, either form is fine.

**Direct quotations** stay in their original language regardless of the report's main language — add a short translation in parentheses only if the quote is load-bearing.

**Filenames (no date suffix):**
- Chinese reports: Simplified Chinese characters allowed in `[Company]` — `reports/company/安培龙_SZSE002050/安培龙_SZSE002050_公司研究.md`.
- English reports: ASCII — `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md`, `reports/company/Alibaba_HKEX9988/Alibaba_HKEX9988_Research_Document.md`.
- Never Japanese kana / kanji or Korean hangul in filenames.
- Do **not** append `_YYYY-MM-DD` to research-doc filenames. Only one EN file and one ZH file exist per company, so a date in the filename adds no signal and clutters the slug folder. Put today's date inside the document as an "as of" header instead; git history tracks the actual revision date.

**Section headers (Chinese reports):** 公司概览, 公司历史, 管理团队, 产品与服务, 客户与上市策略, 行业概览, 竞争格局, 市场机会, 风险评估, 参考资料.

## Citations

**Paragraph-level citation coverage is the standard.** Every substantive paragraph — any paragraph making a factual, quantitative, or external-source claim — must contain at least one inline markdown-link citation. The user's stated trust standard: *"for each paragraph, I hope there is citation, otherwise I don't trust the paragraph."* This includes qualitative analysis paragraphs (industry framing, competitive positioning, management assessment) — cite the 10-K / 年度报告 / Yuho section, the earnings transcript, or the industry research that supports the framing.

Every inline citation is a **clickable markdown link to the real source URL** — `[Title in original language](https://real-url)` — never a bare `(Source: ...)` parenthetical. Link titles preserve the original language (`年度报告`, `10-K`, `決算短信`, `사업보고서`); URLs are canonical permalinks (the actual SEC EDGAR document URL, the specific cninfo PDF, the article permalink — not homepages). No fabricated URLs — if you cannot find the real link, say so inline.

**Density target: ≥40 inline citations across the body of a 6,000–10,000 word report.** Reports landing under 40 have insufficient sourcing — go back and cite uncited paragraphs before submitting.

**Prefer recent web sources.** For non-filing web citations (news, industry reports, third-party rankings, analyst notes), default to sources from the **last 12 months**. Discard older web sources unless they're founding/historical facts or still-authoritative landmark research. Always include the publication date in the link title so vintage is visible: `[Reuters, 2025-08-12](https://...)`.

See [`references/citations.md`](references/citations.md) for the full rules, per-source examples, freshness exceptions, and the final References-block format. **Read it before drafting.**

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

### Step 0 — Sync filings (always run the fetch script first)

**Default behavior: run the fetch script before reading anything.** The scripts are idempotent — they check the source portal (SEC EDGAR / cninfo) for new filings and download only what's missing locally. Existing files are skipped. Mtime-based freshness checks can miss a filing that just dropped, so don't rely on them as a "skip the fetch" shortcut.

**Always run first:**

- **US issuers:**
  ```bash
  cd /Users/x/projects/financial_agent
  python3 fetch_financial_report.py <TICKER>
  ```
- **China A-share / HK issuers:**
  ```bash
  cd /Users/x/projects/financial_agent
  python3 -c "import fetch_cninfo_report as cr; cr.init_db(); [print(m) for m in cr._run_download('SZSE:002050', cr.ALL_CATEGORIES)]"
  ```
  Run from the main project dir so files land in `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/` and not in a worktree.

**Then list what's on disk** (the fetch will have refreshed it):

- **US:** `ls /Users/x/projects/financial_agent/financial_reports/<TICKER>/` — confirm latest 10-K, 10-Q, DEF 14A, recent 8-Ks.
- **China A-share / HK:** `ls /Users/x/projects/financial_agent/cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/` — confirm 年度报告, 季度报告, 半年度报告, 重大事项公告.
- Or query the DB: `sqlite3 db/financial_reports.db "SELECT ticker, report_type, report_date, filename FROM reports WHERE ticker='NVDA' ORDER BY report_date DESC LIMIT 10;"` (and equivalently for cninfo).

**Sanity check what the fetch returned:**

- Annual report (10-K / 年度报告) should be ≤ 13 months old. If the newest on disk is older, the company may be delinquent or the script may have missed a filing — investigate before proceeding.
- Quarterly (10-Q / 季度报告 / 半年度报告) should be ≤ 4 months old. Same rule.
- For Chinese issuers, also confirm whether a 业绩预告 / 业绩快报 has been filed since the last full report — these often pre-announce a guidance change relevant to Step 1's banner check.

**Skip the re-fetch only if:** you already ran the script earlier in this same session for this ticker. Otherwise always run it — it's idempotent and cheap.

Read PDFs with `fitz` / Read tool. For image-only / scanned pages, follow the OCR flow in the project CLAUDE.md (ocrmac → Marker → vision-LM, never Tesseract).

### Step 1 — Initial data collection

1. **Thoroughly analyze the company website** (do not skim — this is the primary source of ground truth on what the company actually sells).
   - Read every About / Company / Mission page; note founders' framing.
   - **Walk the entire product / solutions navigation tree.** Enumerate every distinct product, SKU family, or service line — even 10–30+ items. Do not collapse them.
   - For each product page, capture: official name + variants/tiers, one-sentence description, target customer, pricing model if disclosed, key specs/differentiators the company highlights, any "new"/"flagship" badges.
   - Identify named customers, homepage logos, partner/integration lists, customer case studies.
   - From the leadership / Team page, capture **only the founder and current CEO** (name, title, prior employers) — feed into Step 4. Skip the rest of the team.
   - Read blog / newsroom for the **last 12 months** to detect launches, sunsets, repositioning.
   - For non-English companies, read the **native-language site** (e.g. `company.com.cn`) — English IR pages are often a stripped subset and miss SKUs.
2. **Regulatory filings** — start from the local cache pulled in Step 0; only fetch fresh if the cache is stale (see freshness rules above). Route by domicile per the data-sources table. Note filing dates and the portal used.
3. **Earnings materials** — latest transcript, latest investor presentation, last 12 months of press releases. **Specifically look for any change to full-year guidance** (raised / cut / reaffirmed-with-color / initiated) — capture the old range, new range, disclosure date, and stated driver. If a change exists, it goes in the top-of-report banner described in `references/report_structure.md` (before the TOC), not buried in Section 1. For Chinese issuers, also check 业绩预告 / 业绩快报 — these often pre-announce a guidance change before the formal 半年度 / 年度报告.
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

**Cover the founder and the current CEO only — nothing else.** Skip CFO, other executives, governance footer, and track-record synthesis. The management chapter should be short and focused.

- **Founder (200–300 words).** Pull from LinkedIn, DEF 14A / proxy, press interviews, podcasts, shareholder letters. Capture prior 2–3 roles with *what they specifically accomplished* (numbers not titles), education, founding thesis, ownership stake today, and whether still operationally involved.
- **Current CEO (200–300 words).** Same depth: prior 2–3 roles with concrete accomplishments, education, tenure at this company, ownership stake, comp structure.
- **If founder is still CEO, write one combined bio (300–450 words)** — don't split into two.

### Step 5 — Competitive intelligence

1. Identify 5–10 competitors — direct, indirect, emerging. **Open the company's 10-K / 年度报告 Competition section and quote its competitor list verbatim** — that is the authoritative starting point; any name you add beyond it must be sourced separately. For US issuers the Competition section is typically a paragraph under Item 1 Business. For Chinese issuers, look for `主要竞争对手` or similar in the 年度报告.
2. For each: visit website, review filings if public, note products, differentiators, market-share estimates.
3. Build a positioning framework (price / features / scale). Identify advantages, vulnerabilities, switching costs, network effects.

**Citation discipline for competitive positioning:**

- **Share-leadership claims belong to analysts, not filings.** Do NOT write "Lam is the global #1 in etch ([10-K])" unless the 10-K verbatim says "we are the global #1 in etch" — almost no 10-K says that about itself. Move share / leadership claims under an `*Analyst view:*` label and either cite a third-party research source (Yole, Gartner, TechInsights — at the specific report URL, not the firm's homepage) or leave uncited.
- **Specific competitor product names need their own citation.** "AMAT's NOKOTA platform" is real but is NOT in the LRCX 10-K — the LRCX 10-K only names "Applied Materials" as a competitor. If you want to name an AMAT product, cite AMAT's own 10-K / website where that product is named.
- **Segment-revenue percentages must be labeled.** If you write "Etch is ~45% of Systems revenue", that is an analyst estimate unless the company actually publishes the breakdown — mark it `(analyst estimate; not disclosed)` and do not cite the 10-K for the percentage.
- **Internal consistency:** the competitive-position claims in Section 1 must match the detail in Section 4 (Products) and Section 7 (Competitive Landscape). If Section 1 says "Lam is the only Western supplier of X" but Section 7 says "Lam is #2 behind SCREEN of Japan in X", one of them is wrong. Fix during writing — do not ship contradictions.

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

Read `references/report_structure.md` for the 9-section spec and full output template. Read `references/citations.md` before drafting — inline citations are required in every section, not just at the end.

### Step 10 — Verification pass (mandatory before declaring done)

**A report that has not been verified is not done.** The generating model has a documented pattern of:

- Fabricating SEC URLs (synthetic filenames like `2025_10K_<accession>.htm` that don't exist on EDGAR)
- Attributing analyst opinions to the 10-K ("Lam is regarded as ahead", "dominant moat", "near-monopoly share", "co-leader")
- Inventing competitor product names not present in any cited filing
- Inventing specific market-share percentages and segment-revenue splits
- Inventing executive names and management-transition details

Step 10 catches these before the report ships. **Skip Step 10 only if the user has explicitly waived it.**

#### 10.1 — Verify every URL resolves

```bash
REPORT=reports/company/<Slug>/<filename>.md
for url in $(grep -oE 'https?://[^)]+' "$REPORT" | sort -u); do
  code=$(curl -sSL -A "Research Analyst <your-email>" --max-time 12 -o /dev/null -w "%{http_code}" "$url")
  echo "$code  $url"
done | grep -v '^200 ' | grep -v '^301 ' | grep -v '^302 '
```

Any 404 must be either fixed (find the real URL) or removed. 403 and 406 are usually anti-bot blocks (semi.org, Yahoo Finance, congress.gov, LinkedIn) — confirm those URLs work in a real browser before keeping them.

#### 10.2 — Verify SEC filenames came from the EDGAR submissions JSON

For US issuers, every SEC URL has the form:
`https://www.sec.gov/Archives/edgar/data/<CIK>/<accession-no-dashes>/<filename>`

The `<filename>` is opaque — `lrcx-20250629.htm`, `tsla-20241231.htm`, `f43373e10vk.htm`, `ny20050572x2_def14a.htm`. **Never construct it by pattern.** Look it up via the EDGAR submissions API:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://data.sec.gov/submissions/CIK<10-digit-zero-padded-CIK>.json" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d['filings']['recent']
for i, f in enumerate(r['form']):
    if f in ('10-K', '10-Q', '8-K', 'DEF 14A', '20-F', '6-K'):
        print(f, r['accessionNumber'][i], r['filingDate'][i], r['primaryDocument'][i])
"
```

For 8-K *exhibits* (the cover doc is rarely the exhibit you want), fetch the filing's directory listing:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://www.sec.gov/Archives/edgar/data/<CIK>/<accession-no-dashes>/index.json"
```

If you cannot resolve a real filename, cite the filing index page (`.../index.html`) instead of inventing one.

#### 10.3 — Verify 10-K-cited claims actually appear in the 10-K

Spot-check every paragraph that cites the 10-K. Cache the 10-K once:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<primaryDoc>" > /tmp/10k.htm
```

For each cited number / fact, grep:

```bash
grep -ioE '.{40}<search-string>.{200}' /tmp/10k.htm | sed -E 's/<[^>]+>/ /g; s/&nbsp;/ /g; s/[[:space:]]+/ /g'
```

If the number / claim isn't in the 10-K, the citation is wrong. Either find the real source or drop the claim.

**Specific patterns to grep for and check:**
- `"primary competitor"` / `"主要竞争对手"` — verify the report's competitor list matches the 10-K Competition section verbatim
- `"approximately X%"` for any percentage cited — make sure the actual percentage appears
- Revenue line items (`Systems Revenue`, `Customer Support`) for segment % claims
- Restructuring / headcount claims (`Note 20`, `restructuring`)
- Customer concentration (`major customer`, `customer concentration`)

#### 10.4 — Verify executive names against 8-Ks / DEF 14A

Every named executive must appear by exactly that name in the cited filing. Grep the cached 8-K / DEF 14A:

```bash
curl -sS -A "..." "<8-K URL>" | sed -E 's/<[^>]+>/ /g' | grep -i "<executive name>"
```

If the name isn't in the filing, the citation is fabricated. Remove the claim or find the right filing.

#### 10.5 — Self-audit checklist

Before declaring done, confirm each line:

- [ ] All URLs return HTTP 200 (or known-good 301 / 302 redirect)
- [ ] All SEC URLs end in filenames pulled from the EDGAR submissions JSON
- [ ] No "dominant" / "leader" / "monopoly" / "co-leader" / "near-monopoly share" claim is attached to a 10-K citation unless the 10-K says it verbatim
- [ ] No revenue-by-sub-segment percentage (e.g. "Etch is 45% of Systems") is attached to a 10-K citation — these are analyst estimates, label them as such
- [ ] No specific competitor product name (e.g. "AMAT NOKOTA") is attached to the *subject's* 10-K — at minimum it should cite the competitor's own filing or website
- [ ] No fabricated executive names — every named exec is confirmed in an 8-K or DEF 14A
- [ ] No `(Source: our model)` / `(Source: our analysis)` / `(模型估算)` self-references
- [ ] Internal consistency: Section 1's competitive claim matches Section 7's; Section 2 timeline matches Section 1 prose; restructuring counts in narrative match the timeline
- [ ] Numbers spot-checked against the 10-K (at least: revenue, gross margin, customer concentration, geographic mix, segment %, restructuring headcount)

#### 10.6 — Append a verification log to the report

After the References section, append a `<details>` block listing what was checked. This makes verification visible to the reader and forces honesty about residual unknowns:

```markdown
<details>
<summary>Verification log (Step 10) — YYYY-MM-DD</summary>

**URL check** — all <N> URLs HTTP-checked YYYY-MM-DD; all return 200 / known-good 301.

**SEC filenames** — resolved from EDGAR submissions JSON for CIK <padded>; primary docs: 10-K = `<filename>`, latest 10-Q = `<filename>`, DEF 14A = `<filename>`.

**10-K spot-checks** (claim → location in 10-K):
- Revenue $XB ✓ (MD&A Results of Operations)
- Gross margin XX% ✓ (MD&A)
- Top customer concentration NN%/MM% ✓ (Note 19 / Segment Reporting)
- Geographic mix ✓ (Results of Operations geographic table)
- Restructuring headcount ✓ (Note 20)

**Analyst-view sentences** (intentionally not cited to a primary source):
- Section 1: "<paragraph fragment>" — uncited; supported by industry observation.
- Section 4.1 / 4.2 / 4.3: share-leadership claims labeled `*Analyst view:*` per skill rule.

**Residual unknowns / not yet verified:**
- <bulleted list, or "none">

</details>
```

If the log shows residual unknowns the user cares about, fix them before declaring done.

---

## Output location

Save to **`reports/company/<Slug>/`** under the project root: `/Users/x/projects/financial_agent/reports/company/<Slug>/<filename>.md`. The viewer (http://localhost:5001/reports) groups by this folder structure. Create the folder if missing.

**`<Slug>`** is everything that comes before `_Research_Document` / `_公司研究` / `_研究报告` in the filename — i.e. the company name plus primary ticker, joined with `_`. The filename itself is repeated inside the slug folder (one folder per company holds EN and / or ZH).

File name follows the report language — **no date suffix**:
- **Chinese reports**: `[Company-中文名]_[EXCHANGE][CODE]_公司研究.md` — Simplified Chinese characters allowed.
- **English reports**: `[Company]_[EXCHANGE][CODE]_Research_Document.md` — ASCII only.
- Never Japanese kana / kanji or Korean hangul in filenames.
- **Do not append `_YYYY-MM-DD` to research-doc filenames.** Only one EN file and one ZH file exist per company, so a date in the filename adds no signal and clutters the slug folder. Put today's date inside the document as an "as of" header at the top instead; git history tracks the actual revision date.

Examples:
- `reports/company/安培龙_SZSE002050/安培龙_SZSE002050_公司研究.md` (A-share, Chinese report)
- `reports/company/比亚迪_HKEX1211/比亚迪_HKEX1211_公司研究.md` (HK filing in Chinese)
- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md` (US, English)
- `reports/company/Alibaba_HKEX9988/Alibaba_HKEX9988_Research_Document.md` (HK, English)
- `reports/company/Toyota_TSE7203/Toyota_TSE7203_Research_Document.md` (Japan, English)
- Tickerless private companies: use just the company name as slug, e.g. `reports/company/Unitree/Unitree_Research_Document.md`.

EN and ZH versions of the same report share one slug folder — ZH adds the suffix `_zh` (preferred) or `_CN` before `.md`, e.g. `Tesla_NASDAQ_TSLA_Research_Document_zh.md`.

Other report types live in sibling folders the viewer also surfaces:
- `reports/sector/<topic>_<YYYY-MM-DD>.md` for thematic / industry overviews
- `reports/compare/<A>_vs_<B>_<YYYYMMDD>.md` for head-to-head comparisons
- `reports/earnings/<TICKER>_<YYYYMMDD>.md` for quarterly earnings notes

Always write under the main project's `reports/` directory — never to a worktree, `~/Downloads`, or any other location.

### Update-in-place rule — at most one research doc per company per language

Reports under `reports/` are checked into git and are meant to be living documents. **Before writing, check whether a research doc for this company already exists** in `reports/company/<Slug>/`, and update it in place rather than creating a parallel copy.

```bash
ls "reports/company/<Slug>/" 2>/dev/null | grep -E "_Research_Document(_zh|_CN)?\.md|_公司研究(_zh|_CN)?\.md|_研究报告(_zh|_CN)?\.md"
```

- **Exactly one match for this language** (`_Research_Document` = EN, `_公司研究` / `_研究报告` = ZH) → overwrite it at the same path. Update the document's internal "as of" date header to today; git history records the actual revision dates.
- **Multiple matches for the same language** (legacy state — old dated copies from before this rule) → consolidate into the canonical no-date filename (`<Slug>_Research_Document.md` for EN, `<Slug>_公司研究.md` for ZH), updating the most recent one and listing the older duplicates so the user can confirm deletion. Do not auto-delete.
- **Zero matches** → create a new file at the canonical no-date path. Do **not** add a `_YYYY-MM-DD` suffix to the filename.

EN and ZH editions are separate categories — one of each per company is fine, sharing the same slug folder. After writing, print the final path so the user can confirm whether it was an update or a fresh create.
