# Inline Citations — Required Throughout the Report

**Paragraph-level coverage is the standard, not section-level.** Every substantive paragraph — any paragraph making a factual, quantitative, or external-source claim — must contain at least one inline markdown-link citation. The user's stated trust standard: "for each paragraph, I hope there is citation, otherwise I don't trust the paragraph." A paragraph with zero inline citations is read as unsourced opinion.

Do **not** save citations for the end. Every non-trivial factual claim — revenue figures, market share, management background, customer names, growth rates, quoted strategy language, risk drivers, moat evidence, industry framing, valuation context, qualitative analysis — must be attributed inline at the point it appears.

**Density target: ≥1 citation per paragraph across all 9 sections, plus the References block at the end.** A 6,000–10,000 word report at ~150 words per paragraph yields ~40–70 paragraphs; expect ~50–100 inline citations across the body. Reports landing under 40 inline citations have insufficient sourcing — go back and cite uncited paragraphs before submitting.

**IR sub-density target: ≥8–12 of those citations point at investor-relations materials** (earnings decks, investor day decks, conference presentations, Integrated Reports, Mid-term Plans, IPO prospectuses, shareholder letters) when the company has an active IR program. See § "Investor-relations materials — slide-level citation discipline" below for the format and per-section coverage rules.

## Format: markdown links to real URLs

Every inline citation is a clickable markdown link: `[Title in original language](https://real-website-url)`.

**Do not use bare `(Source: ...)` parentheticals without a URL.** Every link must point to the actual document on the actual web: SEC EDGAR document URL, the specific cninfo PDF URL, the company IR page for an earnings transcript, the news-article permalink, the industry-report landing page. Do not fabricate URLs — if you cannot locate the real link, surface that fact inline rather than guessing.

## SEC EDGAR URL construction — never construct filenames by pattern

US filings live at:
`https://www.sec.gov/Archives/edgar/data/<CIK-no-leading-zeros>/<accession-no-dashes>/<filename>`

The `<filename>` field is **opaque** — issuers use whatever convention they like. Real examples:

| Filing | Real filename |
|---|---|
| Lam Research 2025 10-K | `lrcx-20250629.htm` |
| Tesla 2024 10-K | `tsla-20241231.htm` |
| Lam Research 2008 10-K | `f43373e10vk.htm` |
| Lam Research 2025 DEF 14A | `ny20050572x2_def14a.htm` |
| Lam Research 8-K exhibit | `lrcx_exx991xmayx21x2024.htm` |

**Synthetic patterns are 404s.** Names like `2025_10K_<accession>.htm`, `2025_DEF%2014A_DEF%2014A_<accession>.htm`, `<doctype>_<filing>_<accession>.htm` are LLM hallucinations that do not exist on EDGAR. Do not invent.

**Always look up the real filename via the EDGAR submissions JSON API:**

```bash
curl -sS -A "Research Analyst <your-email>" \
  "https://data.sec.gov/submissions/CIK<10-digit-zero-padded-CIK>.json" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d['filings']['recent']
for i, f in enumerate(r['form']):
    if f in ('10-K','10-Q','8-K','DEF 14A','20-F','6-K','S-1'):
        print(f, r['accessionNumber'][i], r['filingDate'][i], r['primaryDocument'][i])
"
```

The `primaryDocument` field is the real cover-document filename. For 8-K **exhibits** (where the cover doc is not the exhibit you want — e.g. Exhibit 99.1 press release), fetch the filing's directory listing:

```bash
curl -sS -A "..." "https://www.sec.gov/Archives/edgar/data/<CIK>/<accession-no-dashes>/index.json"
```

The `directory.item[*].name` array lists every file in the filing.

**Note on CIK leading zeros.** Some SEC URLs use 10-digit zero-padded CIKs (`/0000707549/`), others use stripped (`/707549/`). The SEC server transparently 301-redirects between them, so both forms work — pick one convention and stick with it.

**Find a company's CIK:** if you don't have it, use the EDGAR ticker-to-CIK lookup at `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<TICKER>&type=10-K` and read the URL of the first result.

**If you cannot resolve the real filename**, cite the filing index page (`.../index.html`) — that page is always real — rather than inventing a document URL.

## Examples (inline within flowing prose)

- US filing: `revenue grew 34% YoY ([Tesla 10-K FY2024, p. 42](https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/tsla-20241231.htm))`
- China A-share filing: `industrial cobot shipments rose 41% ([安培龙 2024 年度报告, 第 28 页](https://static.cninfo.com.cn/finalpage/2025-04-20/1222612345.PDF))`
- HK filing: `gross margin expanded 220bps ([比亚迪 2024 年报, p. 87](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0327/2025032700234.pdf))`
- Earnings call transcript: `CEO flagged a Tier-1 ramp ([Q4-2024 earnings call transcript, 2025-03-12](https://ir.example.com/events/2025-03-12-q4-call))`
- **Earnings deck (per slide):** `Data-center revenue mix rose to 62% in Q4 ([Q4-FY2024 earnings deck, Slide 7 — Segment Mix, 2025-03-12](https://ir.example.com/.../q4-fy24-deck.pdf))`
- **Investor Day deck (per slide):** `Management's TAM build reaches $58B by 2028 ([Lam Research Investor Day 2024, Slide 23 — TAM Build (citing Yole 2024)](https://investor.lamresearch.com/.../investor-day-2024.pdf))`
- **Industry-conference deck (per slide):** `New customer cohorts now contribute 38% of bookings ([CEO at JPMorgan Healthcare 2025, Slide 14, 2025-01-13](https://ir.example.com/.../jpm-hc-2025.pdf))`
- **Japanese Integrated Report:** `Synthetic resin segment ROIC reached 14% ([Sumitomo Chemical 統合報告書 2024, p. 47](https://www.sumitomo-chem.co.jp/.../integrated_report_2024.pdf))`
- **Japanese Mid-term Plan:** `Capex of JPY 600bn through FY2027 targets advanced-material capacity ([Shin-Etsu 中期経営計画 2024-2027, Slide 18](https://www.shinetsu.co.jp/.../mtp_2024-2027.pdf))`
- **Korean Investor Presentation:** `Foundry utilization recovered to 78% in Q4 ([Samsung Electronics Q4 2024 Earnings Presentation, p. 12](https://www.samsung.com/.../earnings_q4_2024.pdf))`
- **A-share 业绩说明会 / 投资者交流活动记录:** `公司表示机器人业务客户数已扩至 42 家 ([安培龙 2024 年度业绩说明会 PPT, 第 9 页, 2025-04-22](https://static.cninfo.com.cn/...))`, `管理层确认 H2 产能爬坡按计划推进 ([安培龙 投资者关系活动记录表 2025-03-15, 第 4 页](https://static.cninfo.com.cn/...))`
- **IPO prospectus / S-1 / 招股说明书:** `招股书披露公司 2021 年前五大客户合计占比 53.7% ([安培龙 招股说明书, 2022-08-15, 第 1-1-189 页](https://static.cninfo.com.cn/...))`
- **CEO shareholder letter:** `Bezos framed AWS as a "primitives" business, not a managed-services business ([Amazon 2014 Shareholder Letter](https://www.aboutamazon.com/.../2014-letter-to-shareholders))`
- Company website / IR page: `the flagship product is the X1 module ([Anpeilong product page](https://www.anpeilong.com/products/x1))`
- News article: `Reuters reported a 2025 capacity expansion ([Reuters, 2025-02-14](https://www.reuters.com/...))`
- Industry report: `global market reached $42B in 2024 ([Gartner, "Industrial Robotics Market Forecast, 2025–2030", 2025-01](https://www.gartner.com/...))`
- **Institute research (local zsxq library):** `*Analyst view:* 摩根士丹利维持 Overweight、目标价 $288（较 2026-06-03 收盘 $232 上行 +24%），估值基于 2027E EPS $13.08 × 22× PE ([Morgan Stanley — NVIDIA Computex keynote & analyst Q&A, 2026-06-03, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812488522252442/Morgan%20Stanley-NVIDIA%20Corp.%EF%BC%88NVDA.US%EF%BC%89Computex%20NVDA%20keynote%20%26%20financial%20analyst%20Q%26A-260603.pdf))` — sell-side, so labeled `*Analyst view:*`, routed via `/zsxq/pdf-viewer/<file_id>` (the old `/zsxq-pdf/` form is a dead 404), broker + date + page in the link text, never attached to a filing. **The PT is always paired with the stock's price on the note's date + the implied upside** (`report_date_price` / `upside_pct` from `stock_price_target_db`, shown at `/pt`) — a bare borrowed PT with no report-date price is not a citation, it's a number with no anchor. `report-date price n/a` if yfinance has no close for that date; never substitute today's spot.
- LinkedIn (management bio): `previously SVP of Engineering at Foxconn ([LinkedIn](https://www.linkedin.com/in/...))`

## Rules

- **Preserve the original language of the title.** Chinese filing titles stay `年度报告` / `年报` / `季度报告`; Japanese stay `有価証券報告書` / `決算短信`; Korean stay `사업보고서`. US filings stay `10-K` / `10-Q` / `DEF 14A` / `8-K`. Do not translate link text.
- **Use the most-direct verifiable URL — never a homepage.** Canonical permalinks: the specific SEC EDGAR document URL (not the EDGAR search page), the specific cninfo PDF URL (not the cninfo homepage), the specific article URL (not the publisher homepage), the specific Gartner / Yole / IDC report page (not the firm's marketing homepage). A citation that links to `yolegroup.com` is functionally a non-citation: the reader can't verify the specific number. For subscription-only sources, link to the report's product page (where the abstract is public) and label `(报告需订阅)` / `(subscription required)`.
- **Source-chain labels when a third party is quoted in a primary filing.** If you're citing a Yole / Gartner / IDC number that the company itself quotes in its 10-K or earnings release, the right citation is the primary filing with a chain-label: `[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/.../tm269592d1_ex99-1.htm)` — not a link to Yole's homepage. The click lands on the verifiable filing where the third-party number actually appears.
- Include enough specificity in the link title to identify the document (filing year, page number when relevant, publication date).
- **Every paragraph in every section** (Company Overview through Risk Assessment) must contain at least one inline markdown-link citation. Section-level "I cited it once in this section" is not enough — the user reads paragraph by paragraph and judges trust at the paragraph level.
- **The analyst's own estimate is NOT a citable source.** Never write `(estimate, based on our model)`, `(Source: our analysis)`, `(来源: 模型估算)`, or any equivalent that points back at the analyst's own work. When you write "we estimate the SAM at $4bn" or "we project FY26E revenue of X", cite the external basis the estimate is built on — the company's latest 10-K, recent earnings guidance, an industry forecast: `we estimate the SAM at $4bn (built on [10-K FY2024 segment data](https://...) + [Gartner 2025 forecast](https://...))`. If there's no defensible external basis, leave the claim uncited rather than fabricate a self-referential source.
- Management bios cite the DEF 14A / proxy, LinkedIn, or interview source per claim. Competitor analysis cites each competitor's own filing or website. TAM/industry numbers cite the specific research firm and report year with a real URL.
- Direct quotations are quoted in the original language; add a short translation in parentheses only if load-bearing for the reader.
- Distinguish primary sources (company filings, transcripts) from secondary (news, third-party research). Prefer primary.
- **Local zsxq broker notes are sell-side — the strictest discipline in the skill.** Label `*Analyst view:*` / `*分析师观点：*`; cite to `http://xs-macbook-air.local:5001/zsxq/pdf-viewer/<file_id>` (NOT the dead `/zsxq-pdf/` route); put broker + date + page (`p.N`) in the link text (the viewer does not auto-scroll on `#page=`); quote the *extracted original PDF text* via OCR / vision read, not the curated 翻译精华 `summary`; and **never attach a zsxq note to a filing citation**. Full workflow in SKILL.md § "Local institute-research library".
- If a fact has no verifiable URL (e.g. private interview, ephemeral snapshot), state that inline rather than inventing a link.

## Investor-relations materials — slide-level citation discipline

Investor decks (quarterly earnings deck, investor day deck, conference appearances) and IR publications (Integrated Report, Mid-term Plan, ESG / sustainability report) are first-class primary sources for company-research reports — frequently *more* informative than the formal filing for the things readers care most about (TAM the company endorses, segment economics, customer cohorts, capex roadmap). See SKILL.md § "Investor presentations are first-class primary sources" for the full collection bar; the citation rules below apply once you have the materials in hand.

**Slide-level granularity, not deck-level.** A 60-slide investor day PDF is a document, not a citation. Cite the specific slide: `[Lam Research Investor Day 2024 deck, Slide 23 — TAM Build](https://ir.lamresearch.com/.../investor-day-2024.pdf)`. For Integrated Reports / Mid-term Plans, cite the page number the same way: `[Sumitomo Chemical 統合報告書 2024, p. 47](https://...)`. The slide / page number is what makes the citation verifiable — a deck-level link forces the reader to skim 60 slides.

**Include the event date and slide topic in the link title.** Format: `[<Company> <Event-or-Doc-Name>, <Slide / Page>, <YYYY-MM-DD>](URL)`. Examples:
- `[NVIDIA GTC 2025 keynote, Slide 42 — Blackwell roadmap, 2025-03-18](https://nvidia.com/.../gtc25-keynote.pdf)`
- `[Tesla Q4-2024 earnings deck, Slide 11 — Energy storage backlog, 2025-01-29](https://ir.tesla.com/.../q4-2024-update.pdf)`
- `[Samsung Electronics Q3 2024 Earnings Presentation, p. 8 — Memory ASP, 2024-10-31](https://www.samsung.com/.../q3-2024-earnings.pdf)`

**Source-chain TAM citations.** Most IR decks pull TAM numbers from Yole / Gartner / IDC / TechInsights / Bloomberg-NEF. The right citation is the *deck* with a chain label, not the underlying research firm's homepage:

- ✅ `[Hesai Investor Day 2024, Slide 14 — Lidar TAM (citing Yole 2024)](https://ir.hesai.com/.../investor-day-2024.pdf)` → reader clicks through to Hesai's own deck and sees Yole credited on the slide
- ❌ `[Yole Group](https://www.yolegroup.com/)` → homepage; reader cannot verify the number
- ❌ `[Yole, "Lidar Market 2024"](https://www.yolegroup.com/product/lidar-2024/)` → if the report is paywalled and the analyst has not actually read it, citing the product page falsely implies access; prefer the source-chain form

**Canonical URLs only — chase redirects to the PDF or hosted page.** IR sites use redirect-tag URLs (`/news-events/...`, `/financials/...`) that may rotate. When the deck is hosted as a PDF, link to the PDF directly. For US issuers, the 8-K Exhibit 99.2 on EDGAR is the most durable host — prefer it over the IR-site copy for quarterly decks when both exist.

**Transcript vs. deck are separate citations on the same event.** Cite the transcript when quoting CEO / CFO language; cite the deck when referencing a chart or numeric callout. Same earnings event often generates 4–6 distinct citations: opening prepared remarks (transcript), Q&A response (transcript), revenue mix slide (deck), guidance bridge slide (deck), capital allocation slide (deck).

**Density bar — minimum 8–12 IR citations in a finished report.** A 6,000–10,000 word company-research report on a public company with an active IR program must reach **at least 8 distinct IR-material citations** across the body (separate from filings, news, third-party research). Reports below the bar have under-used IR materials — go back and find the right slides. Reports on Japanese / Korean / European issuers with an Integrated Report or Mid-term Plan should typically reach **12+ IR citations** because those documents are unusually source-dense.

**Coverage by section.** When IR slides exist that cover the section's content, the section *must* contain at least one IR citation:
- Section 1 (Overview) — latest-quarter KPI bridge or capital-allocation slide
- Section 4 (Products) — roadmap slide or product-family-mix chart
- Section 6 (Industry) — management's industry framing slide
- Section 8 (TAM) — the IR deck's TAM build slide is the most-cited source in most reports

If a section that *should* have IR coverage lacks it, that is a quality defect — fix before submitting.

## Freshness rule for web sources

When citing **web sources other than filings** (news articles, industry reports, blog posts, analyst notes, third-party rankings, government press releases, sell-side research summaries):

- **Prefer the most recent available source.** If a 2025 source covers the same fact as a 2022 source, cite the 2025 one. Re-search rather than reuse an old link.
- **Sources older than ~12 months are stale by default — discard them unless one of the exceptions below applies.** Industries move, market shares re-shuffle, regulations change, and a 2022 number quoted today reads as careless.
- **Exceptions where older is fine:**
  - Founding / historical facts (when the company was founded, the year of an IPO, year of an acquisition) — these don't get newer.
  - Landmark research that's still the authoritative reference and hasn't been superseded (cite once, note vintage explicitly).
  - Long-cycle industry structural data where annual fluctuation is small (sub-industry definitions, regulatory framework histories).
- **For TAM / market-size citations**, use the most recent forecast you can find. Gartner/IDC/Forrester refresh quarterly to annually; a 2020 forecast cited in 2026 is not credible.
- Filings themselves are exempt from the 12-month rule — the most recent annual is the most recent annual, even if filed 11 months ago. Apply the freshness rule to *web sources around* filings: news, commentary, analyst takes, etc.
- **Local zsxq broker notes follow the same 12-month rule** — keep recent notes, drop stale ones except for founding / structural facts. Each note's vintage is in its `create_time` / filename date; prefer the freshest note when several cover the same call.
- Always include the **publication date** in the link title so a reader can immediately see vintage: `[Reuters, 2025-08-12](https://...)`, not `[Reuters article](https://...)`.

## Final References Section

At the end of the document, include a consolidated, deduplicated list of all sources used, organized by source type. Each entry is also a markdown link to the real URL, with publication date. This is **in addition to**, not a replacement for, the inline links.

## Full inline example (within a section)

```
Anpeilong's robotics segment revenue rose 41% YoY in FY2024 to RMB 2.83 bn,
driven primarily by industrial cobot shipments to automotive OEMs
([安培龙 2024 年度报告, 第 28 页](https://static.cninfo.com.cn/finalpage/2025-04-20/1222612345.PDF)).
Management attributed roughly half of the growth to a single Tier-1 supplier ramp
([Q4-2024 earnings call transcript, 2025-03-12](https://ir.anpeilong.com/2025-03-12-q4-call)).
```
