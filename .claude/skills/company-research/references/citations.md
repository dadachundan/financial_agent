# Inline Citations — Required Throughout the Report

**Paragraph-level coverage is the standard, not section-level.** Every substantive paragraph — any paragraph making a factual, quantitative, or external-source claim — must contain at least one inline markdown-link citation. The user's stated trust standard: "for each paragraph, I hope there is citation, otherwise I don't trust the paragraph." A paragraph with zero inline citations is read as unsourced opinion.

Do **not** save citations for the end. Every non-trivial factual claim — revenue figures, market share, management background, customer names, growth rates, quoted strategy language, risk drivers, moat evidence, industry framing, valuation context, qualitative analysis — must be attributed inline at the point it appears.

**Density target: ≥1 citation per paragraph across all 9 sections, plus the References block at the end.** A 6,000–10,000 word report at ~150 words per paragraph yields ~40–70 paragraphs; expect ~50–100 inline citations across the body. Reports landing under 40 inline citations have insufficient sourcing — go back and cite uncited paragraphs before submitting.

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
- Earnings call: `CEO flagged a Tier-1 ramp ([Q4-2024 earnings call transcript, 2025-03-12](https://ir.example.com/events/2025-03-12-q4-call))`
- Company website / IR page: `the flagship product is the X1 module ([Anpeilong product page](https://www.anpeilong.com/products/x1))`
- News article: `Reuters reported a 2025 capacity expansion ([Reuters, 2025-02-14](https://www.reuters.com/...))`
- Industry report: `global market reached $42B in 2024 ([Gartner, "Industrial Robotics Market Forecast, 2025–2030", 2025-01](https://www.gartner.com/...))`
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
