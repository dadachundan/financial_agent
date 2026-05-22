# Citation Backfill — Agent Prompt Template

You are backfilling inline citations on a single research report so it meets the project's current citation standard. Work on the file at `{REPORT_PATH}` (absolute: `/Users/x/projects/financial_agent/{REPORT_PATH}`).

## Standard you must meet

Read `.claude/skills/company-research/references/citations.md` for the authoritative spec. The key rules:

1. **Every substantive paragraph in the body needs ≥1 inline markdown-link citation.** A paragraph making any factual, quantitative, or external-source claim and carrying zero inline links is unsourced. Headings, tables, chart captions, and short bridge sentences are exempt; everything else is not.
2. **Use deep URLs, never homepages.** The link must land on the specific document/article/page that contains the claim. `yolegroup.com` or `gartner.com` as a target is a non-citation; the specific report landing page or — better — the primary filing that quotes Yole/Gartner is the right link.
3. **Source-chain labels for third-party numbers quoted in primary filings.** If a Yole/Gartner/IDC number appears in the company's 10-K, cite the filing with a chain label: `[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/...)`, not Yole's homepage.
4. **Preserve original language in link titles.** Chinese filings stay `年度报告` / `年报`; Japanese stay `有価証券報告書`; US stay `10-K` / `10-Q`. Do not translate.
5. **Include the publication date in the link title** for news/research sources: `[Reuters, 2025-08-12](https://...)` not `[Reuters article](https://...)`.
6. **Freshness: discard web sources older than ~12 months** unless they are founding facts, landmark research, or filings (filings are exempt). If a 2025 source covers the same fact as a 2022 source, cite the 2025 one — re-search rather than reuse stale links.
7. **The analyst's own model is NOT a source.** Never write `(Source: our model)`, `(estimate, based on our analysis)`, `(模型估算)`, or equivalents. If a claim is a model output, cite the external inputs the model is built on (10-K segment data + an industry forecast).
8. **No bare `(Source: ...)` parentheticals without a URL.** Every citation is a clickable markdown link `[Title](https://real-url)`.

## Procedure

1. **Read the full report.** Note the company/ticker, the report language (EN or ZH — `_zh.md` suffix or Chinese filename means ZH).
2. **Audit paragraphs.** Walk the body section by section (Company Overview through Risk Assessment, plus any TAM/competitive/management sections). For each paragraph, ask: does it carry a factual claim, AND does it lack any `[...](http...)` link? If yes, it's uncited and needs a citation.
3. **Strip violations from existing citations:**
   - Remove or replace any `(Source: our model)` / `(模型估算)` / `(estimate, our analysis)` style self-references — the model is the analyst's view, not a source. Replace with external sources or leave the claim uncited.
   - Replace homepage links (`yolegroup.com`, `gartner.com`, `company.com` without a path) with deep URLs to the specific document. If you cannot find a deep URL, replace with the primary filing that quoted the number (source-chain pattern).
   - Replace bare `(Source: ...)` parentheticals with proper markdown links.
4. **For each uncited paragraph, find a verifiable URL via web search.** Prefer in this order:
   - Primary filings: SEC EDGAR (US), HKEXnews (HK), cninfo (CN A-share, e.g. `static.cninfo.com.cn/finalpage/...PDF`), the company's IR earnings transcript page.
   - Reputable news with permalink and recent date.
   - Industry research firms' specific report landing pages (Gartner / IDC / Yole / Counterpoint / TrendForce / etc.).
   - Government / regulator releases (NDRC, MIIT, SEC, FCC, etc.).
   - Company website pages with the actual product/data (not homepage).
   - LinkedIn for management bios.
5. **Add the citation inline at the point of claim.** Use the exact format from the spec. Keep titles in original language.
6. **If, after searching, no verifiable source exists for a paragraph,** soften the claim or leave it uncited — never fabricate a URL.
7. **Preserve the report's language.** If the file ends in `_zh.md` or is in Chinese, all your added link titles should be in Chinese where the source is Chinese. For an English file, English titles for English sources; Chinese titles for Chinese sources (do not translate Chinese source titles).
8. **Do not change the prose** beyond what's needed to insert citations or fix violations. This is a citation pass, not a rewrite.

## Tools you have

- `WebSearch` and `WebFetch` for sourcing.
- `Read` / `Edit` / `Grep` on the local report.
- The DBs `db/financial_reports.db` (US filings) and `db/cninfo_reports.db` (CN/HK filings) hold filings the user has already downloaded — querying these is the fastest way to find primary filing URLs for Chinese companies. Use `sqlite3` via Bash to look up by ticker/code.

## Done criteria

Before reporting done:

1. Run a final count: paragraphs needing citation vs paragraphs with citation. Target ≥90% of substantive paragraphs cited. If you got there, you're done.
2. Confirm no `(Source: our model)` / `(模型估算)` / homepage-only links remain.
3. Confirm every citation is a clickable `[Title](https://...)` markdown link.

## Report back

Return a single message with:
- File path
- Before: URL count / paragraph coverage %
- After: URL count / paragraph coverage %
- Number of (a) added citations, (b) replaced/stripped violations
- Any paragraphs you intentionally left uncited because no source existed (1-line note each)
- Under 200 words total.
