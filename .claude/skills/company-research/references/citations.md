# Inline Citations — Required Throughout the Report

Do **not** save citations for the end. Every non-trivial factual claim — revenue figures, market share, management background, customer names, growth rates, quoted strategy language, risk drivers, moat evidence — must be attributed inline at the point it appears.

## Format: markdown links to real URLs

Every inline citation is a clickable markdown link: `[Title in original language](https://real-website-url)`.

**Do not use bare `(Source: ...)` parentheticals without a URL.** Every link must point to the actual document on the actual web: SEC EDGAR document URL, the specific cninfo PDF URL, the company IR page for an earnings transcript, the news-article permalink, the industry-report landing page. Do not fabricate URLs — if you cannot locate the real link, surface that fact inline rather than guessing.

## Examples (inline within flowing prose)

- US filing: `revenue grew 34% YoY ([Tesla 10-K FY2024, p. 42](https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/tsla-20241231.htm))`
- China A-share filing: `industrial cobot shipments rose 41% ([安培龙 2024 年度报告, 第 28 页](https://static.cninfo.com.cn/finalpage/2025-04-20/1222612345.PDF))`
- HK filing: `gross margin expanded 220bps ([比亚迪 2024 年报, p. 87](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0327/2025032700234.pdf))`
- Earnings call: `CEO flagged a Tier-1 ramp ([Q4-2024 earnings call transcript, 2025-03-12](https://ir.example.com/events/2025-03-12-q4-call))`
- Company website / IR page: `the flagship product is the X1 module ([Anpeilong product page](https://www.anpeilong.com/products/x1))`
- News article: `Reuters reported a 2025 capacity expansion ([Reuters, 2025-02-14](https://www.reuters.com/...))`
- Industry report: `global market reached $42B in 2024 ([Gartner, "Industrial Robotics Market Forecast, 2025–2030", 2025-01](https://www.gartner.com/...))`
- LinkedIn (management bio): `previously SVP of Engineering at Foxconn ([LinkedIn](https://www.linkedin.com/in/...))`

## Rules

- **Preserve the original language of the title.** Chinese filing titles stay `年度报告` / `年报` / `季度报告`; Japanese stay `有価証券報告書` / `決算短信`; Korean stay `사업보고서`. US filings stay `10-K` / `10-Q` / `DEF 14A` / `8-K`. Do not translate link text.
- **Use canonical permalinks**: the SEC EDGAR document URL (not the company search page), the specific cninfo PDF URL (not the cninfo homepage), the specific article URL (not the publisher homepage). For locally-cached PDFs, use the live web URL of the same document, not the local path.
- Include enough specificity in the link title to identify the document (filing year, page number when relevant, publication date).
- **Every section** (Company Overview through Risk Assessment) must contain inline markdown-link citations — not just the final References block.
- Management bios cite the DEF 14A / proxy, LinkedIn, or interview source per claim. Competitor analysis cites each competitor's own filing or website. TAM/industry numbers cite the specific research firm and report year with a real URL.
- Direct quotations are quoted in the original language; add a short translation in parentheses only if load-bearing for the reader.
- Distinguish primary sources (company filings, transcripts) from secondary (news, third-party research). Prefer primary.
- If a fact has no verifiable URL (e.g. private interview, ephemeral snapshot), state that inline rather than inventing a link.

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
