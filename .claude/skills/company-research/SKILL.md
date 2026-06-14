---
name: company-research
description: Produce deep 6,000–10,000 word company research reports in Simplified Chinese by default (business, management, products, customers, industry, competitive landscape, TAM, risks) for a public or private company. The Chinese report keeps technical / industry / financial terms in English alongside their Chinese gloss (e.g. `gross margin (毛利率)`, `gate-all-around (GAA)`). An English-language report is produced ONLY when the user explicitly asks (`in English`, `English only`, `--lang en`, `--en-only`, `bilingual`, `also in English`). Primary sources first (company website, filings, IR decks); also searches the local institute-research library (`db/zsxq.db`, ~6,900 broker PDFs) first for the sell-side view — price targets, estimates, channel checks, bear case — labeled as `*Analyst view:*` and never blended into a filing citation. Output saved to `reports/company/<Company_Ticker>/` under the project root. Use when the user asks to "research", "deep-dive", "profile", or "initiate coverage on" a specific company or ticker — e.g. "research Tesla", "deep dive on PLTR", "company research for SZSE:002050".
---

# Company Research

Deep research deliverable: a 6,000–10,000 word markdown report covering business, management, products, customers, industry, competitive landscape, TAM, and risks. Input is just a company name or ticker.

**Methodology: website-first.** This skill prioritizes the company's official sources (website, investor relations, press releases, filings) over third-party research. The company's own website is the starting point and ground truth for what it actually sells; regulatory filings provide audited financials and legal risk details; analyst research comes third. This approach yields reports grounded in primary sources rather than analyst consensus or journalistic interpretation.

## Core principle: accuracy over completeness — never hallucinate

This is the **single most important rule** and overrides every other instruction in this skill. The report is read by investors making real decisions; a single fabricated number, executive name, customer name, page reference, market-share figure, or URL destroys the credibility of the entire document.

**Hard rules:**

- **Never invent specific facts.** Revenue figures, growth rates, customer names, competitor market shares, executive backgrounds, board members, founding dates, product launch dates, TAM numbers, page numbers in filings, URLs — every one of these must come from a source you actually verified. If you didn't read it, don't write it.
- **If the data is not available, say so.** Write `disclosure not found` / `not disclosed in 10-K` / `cninfo filing does not break this out` / `private — not disclosed`. Omitting a section or stating an absence is **always preferable to inventing a plausible-looking number**.
- **No "this is probably around X."** No back-of-envelope estimates dressed as facts. If you need to estimate, mark it explicitly (`est., based on [reasoning]`) and show the math.
- **Cross-check every quantitative claim against its citation.** Before pasting "revenue grew 34% YoY" with a 10-K link, confirm the 10-K actually shows 34%. The citation must support the claim — not vaguely cover the topic.
- **Page numbers and dates must be exact.** If you cite `2024 年度报告, 第 28 页`, page 28 must be where the figure actually lives. If unsure, drop the page reference and cite the document only.
- **No fabricated URLs** (this echoes the citation rule). For SEC filings, always look up the real filename via the EDGAR submissions JSON API (`https://data.sec.gov/submissions/CIK<10-digit-padded>.json` — see `reference/citations.md`); never invent synthetic filename patterns like `2025_10K_<accession>.htm` — those are 404s.
- **Direct quotations must be verbatim.** If you can't quote exactly, paraphrase and drop the quote marks. When writing about official company website data or regulatory filings, **default to quoting the original text rather than paraphrasing.** This ensures readers can verify every claim against the source.
- **Distinguish primary (filings, transcripts) from secondary (news, third-party) sources.** When two sources disagree, prefer the primary and note the discrepancy briefly.

## Guardrails (at-a-glance — the rules with the worst failure modes)

Compact index of the load-bearing don't-dos enforced throughout this skill. Each links to the detailed section that owns it; **none of these are new rules** — they are the project-history failure modes worth seeing on one page.

- **Do not invent numbers, executives, customers, product names, page references, or URLs.** Write `disclosure not found` instead. See **Core principle** above and `references/quality_checklist.md`.
- **Do not attach a 10-K citation to a sell-side opinion.** "Lam is the global #1 in etch" is an analyst view, not 10-K language; label `*Analyst view:*` and either cite a real third-party source (Yole / Gartner / IDC at a specific report URL) or leave uncited. See § "Specific failure mode: do NOT misattribute sell-side opinions to filings".
- **Do not invent SEC URLs.** Resolve every filename via the EDGAR submissions JSON (`https://data.sec.gov/submissions/CIK<padded>.json`); never construct `2025_10K_<accession>.htm`-style patterns — those are 404s. See Step 10.2.
- **Do not write a customer-share number without its denominator.** "X% of revenue" is wrong when more than one denominator could apply — always "X% of consolidated revenue" or "X% of <Segment> segment revenue". A segment-level customer (e.g. NVIDIA in DS Memory) is never silently presented as a consolidated top-5 customer. See Step 3.
- **Do not paraphrase 10-K / 年度报告 / Yuho product descriptions.** Block-quote verbatim with the citation directly above. Paraphrase is where fabrication enters. See § "The Products & Services chapter is the most important section…".
- **Do not present analyst-constructed verdicts as `Buffett would buy`, `巴菲特会买`, or `Damodaran's fair value is`.** Investor-lens scorecards (Section 10) use the lens *as a rubric*, not as an endorsement. See `references/investor_lenses.md`.
- **Do not skip the Step 10 verification pass.** Every URL HTTP-checked, every SEC filename resolved, ≥5 10-K-cited numbers spot-checked, executive names confirmed against 8-K / DEF 14A. The verification log is the deliverable's contract with the reader. See Step 10.
- **Do not write "(Source: our model)" / "(estimate, our analysis)" / "(本模型)" anywhere in the report.** Cite the external inputs the model is built on, not the model. See the project-wide Numerical Accuracy rule in [`CLAUDE.md`](../../../CLAUDE.md).
- **Do not attribute the GF Score (Section 1B) to GuruFocus, and do not attach a filing citation to any GF sub-score.** The GF Score (GuruFocus-style) is the analyst's own rubric — label it `*Analyst view:*`, cite each underlying metric (margins / leverage / CAGR / multiples / returns) inline, and only carry a GuruFocus citation if you actually pulled their published number from `gurufocus.com/term/gf-score/<TICKER>` (shown separately). See `reference/gf_score.md`.
- **Do not skip the Data Used manifest** (see `references/report_structure.md` → "Data Used" block). A report that lists ≥40 inline citations but no data manifest is harder for the reader to triage — the manifest is one block, not duplication.
- **Do not run destructive SQL against `db/*.db`.** Read-only — `SELECT`, `.schema`, `PRAGMA`. Test-writes go via `FINAGENT_DB_DIR=/tmp/...`. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Source hierarchy: official company data first

**Prioritize the company's own official sources over third-party research.** The company's website, SEC filings, investor materials, and press releases are the ground truth; analyst reports, news articles, and third-party research are supporting evidence.

**Source priority (highest to lowest):**

1. **Company official website** — product pages (specifications, use cases, pricing if disclosed), About / Company pages, leadership bios, customer case studies, blog/newsroom (last 12 months for launches and announcements). **When citing website content, quote or closely paraphrase the exact text** so readers can verify against the live source.
2. **Regulatory filings** — 10-K / 10-Q / 8-K (US), 年度报告 / 季度报告 (China), Yuho / Shihanki (Japan), etc. These are legally binding and audited (filings, not soft estimates). **Quote verbatim from the filing** whenever possible, especially for product definitions, customer names, risk factors, and segment breakdowns. Block-quote long passages with the citation directly above.
3. **Investor relations materials** — earnings call transcripts, earnings decks, investor-day presentations, annual integrated reports, capital-markets-day decks. These are prepared by the company's own IR team and often contain the most direct business context. **Quote management's own words from transcripts and decks** rather than summarizing or interpreting what they said.
4. **Press releases and announcements** — official channel for product launches, customer wins, partnerships, guidance changes. **Quote press releases verbatim** for specific announcements and dates.
5. **Conference presentations** — when the company's own executives present at industry conferences (JPM, SEMICON, etc.), these are quasi-official sources. **Quote or screenshot the actual slides** rather than paraphrasing the executive's point.
6. **Sell-side / institute research** (Morgan Stanley, Goldman Sachs, J.P. Morgan, Bernstein, UBS, Citi, Deutsche Bank, HSBC, Nomura, plus market-sizing firms Yole, Gartner, IDC, TechInsights, TrendForce, etc.) — used for market-sizing, competitive positioning, consensus estimates / price targets, and industry trends when the company's filings don't provide the detail. Can paraphrase with citation, but prefer direct quotes when a number or claim is novel or contested. **There is a large local library of this material in `db/zsxq.db` (6,900+ broker PDFs) — search it FIRST, before web-searching for analyst notes.** See § "Local institute-research library" below for the search-and-cite workflow.
7. **News and web sources** — news articles, blog posts, third-party analysis. Use only for recent developments and confirmation, not as a primary claim source.

**When the company's website lacks detail**, fall back to regulatory filings (which are more complete and audited); only then reach for third-party research. A product feature list from the company's website beats an analyst's product description; a management quote from an earnings transcript beats a paraphrased interpretation from a news article.

**Default: quote the original text.** When writing from official sources (website product pages, 10-K product descriptions, earnings transcripts, press releases), the default move is to quote or closely preserve the original language, not to synthesize or paraphrase. This is what distinguishes primary-source research from derivative commentary.

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

- **Anchor to the issuer's own product matrix.** Most 10-Ks / 年度报告 / Yuho contain a Product matrix or Product Family table in Item 1 Business. **Reproduce it verbatim as a markdown table (MANDATORY)**, quoting the issuer's own row / column labels; optionally also embed the rendered original as a PNG via the helper at `.claude/skills/company-research/scripts/render_10k_section.py` when visual proof adds value. The markdown reproduction is the searchable, citable anchor and is required regardless; the PNG never substitutes for it. If the issuer does not publish such a table, build one from the company website (cited) and label it as analyst-constructed.
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
- No verbatim markdown reproduction of the issuer's own product matrix → the section reads like analyst opinion without primary anchor; reproduce the table verbatim to fix (the optional PNG embed via `render_10k_section.py` does not substitute for it).

See `references/report_structure.md` § Section 4 for the per-row template, and `references/quality_checklist.md` for the pre-submit checklist.

## 延伸观看 / Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — a mechanical assembly (a humanoid robot's actuators / harmonic (strain-wave) reducers / ball-screws / force sensors), a semiconductor etch–deposition flow, HBM die-stacking, a surgical-robot wrist, a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing. Section 4 is the natural home — it is where the report explains hard-to-visualize product mechanics.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**延伸观看 / Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept. English-only reports use `**Further viewing**`.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(B站，部分地区或需登录)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: `reference/citations.md` § "Further viewing — explainer videos".

## Investor presentations are first-class primary sources — use exhaustively when available

After 10-Ks / 年度报告 / Yuho, **investor-relations materials are the next-most-load-bearing source category** — often *more* informative than the formal filings for what research readers care most about: segment-mix economics, the TAM/SAM views the company itself endorses, customer-cohort disclosures, capital-allocation roadmaps, capacity build-out plans, and management's own framing of the moat. **Whenever IR materials exist, treat collecting them as a non-optional Step 1 task and cite them aggressively throughout the report** — quarterly earnings deck + transcript, the latest investor-day / capital-markets-day deck, conference presentations, the annual integrated report / ESG report / Mid-term Plan (especially for JP/KR/EU issuers), the shareholder letter, and the IPO prospectus / S-1 / 招股说明书 if within ~5–10 years.

**Density bar:** ≥8–12 distinct IR-material citations across the body when the company has a public IR program; ≥1 in each of Sections 1/4/6/8; the latest 2 quarterly decks AND the latest investor-day deck each cited at least once. Cite at the **slide level** (`[… Investor Day 2024 deck, Slide 23 — TAM build](url)`), chain-cite the underlying research when the deck credits Yole/Gartner/IDC, and keep transcript (CEO/CFO words) vs. deck (chart/number) as separate sources. If the company has effectively no IR program, say so in the verification log and lean on filings + third-party research.

> **Full spec — what to collect, where to find it per domicile (US / China-HK / Taiwan / Japan / Korea / private), the per-section "what IR slides unlock" table, and the slide-level citation discipline: [`references/ir_materials.md`](references/ir_materials.md).**

## Local institute-research library (`db/zsxq.db`) — search it FIRST for any sell-side view

The project carries a large local library of **institute / sell-side research PDFs** in `db/zsxq.db` (table `pdf_files`, ~6,900 rows and growing) — single-name notes, sector reports, supply-chain channel checks, and conference takeaways from Morgan Stanley, Goldman Sachs, J.P. Morgan, Bernstein, UBS, Citi, Deutsche Bank, HSBC, Nomura, and others. **Before you web-search for any analyst opinion, consensus estimate, price target, or industry datapoint, search this local library first** — it is faster, the source travels with the project (the user can click straight to the PDF in their viewer), and it is exactly the material that answers "what does the Street think" for Sections 2 / 6 / 7 / 8 / 9. Treat searching it as a non-optional data-collection task (it is **Step 0.7** of the workflow).

**This material is SELL-SIDE — the strictest citation discipline in this skill applies.** Everything pulled from `db/zsxq.db` is an analyst opinion, not a primary fact. It must be labeled `*Analyst view:*` / `*分析师观点：*` and **must never be attached to a filing citation** (see § "Specific failure mode: do NOT misattribute sell-side opinions to filings"). A Morgan Stanley target-price or a "85% AI-GPU share" estimate is an MS view; cite it to the MS note, not to the 10-K.

### How to search the library (by every alias, not just the ticker)

The lookup helper is `find_pdf.py` from the `zsxq-analyze` skill. Run a **separate `--query` for each alias** — ticker, English name, AND native-language name — because broker filenames and the curated summaries use a mix:

```bash
cd /Users/x/projects/financial_agent
# US ticker, English name, and Chinese name are DIFFERENT result sets — run all three.
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "NVDA"   --limit 60
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "NVIDIA" --limit 60
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "英伟达"  --limit 60
# Also sweep supply-chain / competitor / theme terms — sector notes that don't name the
# subject in the title often carry the most useful channel-check data in the summary:
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "Blackwell" --limit 40
/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "AI server" --limit 40
```

`--query` does a case-insensitive `LIKE` across `name / topic_title / summary / tags / comment`, sorted `create_time DESC`. Rows come back as JSON with `file_id, name, topic_title, summary, page_count, create_time, bank, local_path, local_exists`. Apply the **12-month freshness rule** (§ Citations): keep recent notes; ignore stale ones except for founding/structural facts. For a US name like NVDA this typically returns dozens of MS / GS / JPM / Bernstein notes — keep the 5–15 most relevant and most recent.

**Interpreter & DB-lock fallback.** Always invoke these scripts with `/opt/anaconda3/bin/python3` — the bare `python3` on PATH lacks project deps (browser_cookie3, PyPDF2 / ocrmac) and fails read-only `mode=ro` DB opens (this exact failure derailed a real run mid-report; see project memory `feedback_anaconda_python_db_scripts.md`). If `find_pdf.py` still errors because the user's live `:5001` Flask holds `db/zsxq.db`, fall back to a SELECT-only immutable read for triage — `sqlite3.connect('file:db/zsxq.db?mode=ro&immutable=1', uri=True)` — which stays read-only and consistent with the project DB-safety tiers, and record the fallback in the Step 10 verification log.

### The library has two layers — triage on the summary, then READ THE PDF

1. **`topic_title` + `summary` (the curated 翻译精华) is for TRIAGE, not for citing.** For most rows the summary is a clean Chinese digest that already states the **broker, rating, price target, valuation basis, and 2–4 thesis points** — enough to decide *which notes matter* and to grab a headline PT/rating fast. Example row (`file_id 812488522252442`): *维持 Overweight / 首选推荐，目标价 $288 … 基准情形基于 2027E EPS $13.08 × 22 倍 PE … AI GPU 市占率稳居 ~85%* — broker (MS), rating, PT, valuation math, share estimate, without opening the PDF. **But the 翻译精华 is a curated secondary translation — for anything you put in the report, quote the *original extracted text*, not the digest** (same guardrail as `theme-research` / `zsxq-ideas`).
2. **Open and READ the PDF for any note that matters — image-only is NOT a blocker.** Many broker PDFs are scanned (every page returns empty text from `fitz`), but the content is fully recoverable; never skip a note because "the text is empty." Use the three-tier flow from the project CLAUDE.md / `zsxq-analyze` skill (ocrmac → Marker → vision-LM; never Tesseract):
   ```bash
   # Tier 1 — OCR image-only pages (Apple Vision / ocrmac, ~1s/page, cached to pdf_files.ocr_text; free on re-run)
   /opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py     --file-id <id>
   # Then extract — auto-merges the OCR cache for empty pages
   /opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id <id> --header
   # Tier 3 — for charts / dense tables where meaning is visual: render the page, then READ the PNG yourself (you, Claude, are the extractor — no external API)
   /opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/render_pdf_pages.py --file-id <id> --pages 4-6
   ```
   (Tier 2, Marker, is for scrambled multi-column reading order or tables-as-markdown — reach for it when ocrmac garbles a dense financial table.) **String-match every number you quote against the OCR'd / extracted / vision-read original text — no number enters the report that you have not seen as a literal string in the source PDF.** The summary alone is never sufficient sourcing for a hard number.

### What the library unlocks, by report section

| Section | What a broker note in `db/zsxq.db` typically supplies (label all as *Analyst view:*) |
|---|---|
| **2. Valuation & PT** | Consensus / target price, the bull-base-bear PT scenarios, the valuation basis (forward EPS × multiple), the **consensus estimate to benchmark your forward model against** (the UBS/Nomura "+16% vs Street" move), where the analyst sits vs the Street. Pair with the actual multiples + forward model from Step 2. |
| **6. Industry** | Channel checks, unit/ASP/capex forecasts, end-market build-out timing, supply-chain reads (memory, substrate, CoWoS, lead-times) that filings never disclose. |
| **7. Competitive** | Side-by-side share estimates, who's winning which socket, ASIC-vs-GPU framing, second-source dynamics. (Share numbers are estimates — never cite them to the subject's 10-K.) |
| **8. TAM** | Sell-side TAM/SAM build-ups with their assumptions; chain-cite the underlying research firm when the note credits Yole/Gartner/TrendForce. |
| **9. Risks / 9.5 Debates** | The bear case in the analyst's own words — what the skeptics worry about (memory price cuts, China demand, ASIC encroachment), with the specific trigger — feeds both the Section 9 risk inventory and the Section 9.5 key-debates rebuttals. |
| **Channel checks** | Proprietary channel-check data as a first-class evidence class — shipment trackers (NE Times monthly SoC shipments), Frost & Sullivan / Yole rankings, credit-card spend panels, App-download / Google-Trends momentum. Cite as *Analyst view:* via the broker note and **flag it as channel-check-derived** so the reader knows the provenance. Every sell-side analog leans on these. |
| **Bull/Bear & lenses** | The note's own scenario tree feeds the optional Section 10 lenses and any bull-bear framing directly. |

### Citation format for `db/zsxq.db` sources

Cite the **local viewer URL** so the user can click straight to the PDF they own, and put broker + date + page in the link text:

```
*Analyst view:* 摩根士丹利维持 NVDA 增持（Overweight）评级、目标价 $288，估值基于 2027E EPS $13.08 × 22× PE（[Morgan Stanley — NVIDIA Computex keynote & analyst Q&A, 2026-06-03, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812488522252442/Morgan%20Stanley-NVIDIA%20Corp.%EF%BC%88NVDA.US%EF%BC%89Computex%20NVDA%20keynote%20%26%20financial%20analyst%20Q%26A-260603.pdf)）。
```

- **Canonical route (verified 200, direct download): `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>`** — the `<filename>` is `pdf_files.name` URL-encoded. **Paste the `pdf_url` field that `find_pdf.py` now emits verbatim** — don't hand-build it. This route serves raw `application/pdf`, so tapping it on iPad opens/downloads the PDF natively. Do **NOT** use `/zsxq/pdf-viewer/<file_id>` (the PDF.js viewer page — it returns `text/html` and does **not** download on iPad), and do **NOT** use the oldest `/zsxq-pdf/<file_id>` form (dead 404). Put the page number in the link **text** (`p.N`); appending `#page=N` to the URL is harmless and is honored by native PDF viewers.
- **Always include the broker and the note date in the link title** — `[Morgan Stanley — <title>, YYYY-MM-DD, p.N](…)` — never the bare title or a naked URL.
- **Pair every borrowed broker PT with the stock's price on the note's date (mandatory).** A `目标价 $288` lifted from a 2026-06-03 MS note is uninterpretable without the price NVDA traded at *on 2026-06-03* — that report-date price is what fixes the upside MS actually called, and it is NOT the same as the report header's current spot. Write it as `目标价 $288（较 2026-06-03 收盘 $232 上行 +24%）`. The report-date close + upside are already stored in `stock_price_target_db` (`report_date_price` / `upside_pct`, looked up by `scripts/persist_pts.py`) and shown at `/pt` — read them back, or look up the yfinance close on the note's date. If the report-date price is unavailable, write `report-date price n/a` rather than substituting today's spot. (The report's own 12-month PT in the header keeps showing today's current price, as already specified — this rule is specifically for *borrowed* sell-side PTs.)
- **Quote the original-language source text alongside the number.** The summary digests are Chinese; the underlying PDFs may be English — preserve whichever language the source uses.
- These local URLs are user-machine-only (they will 404 for anyone else), so a finished report should still anchor its *hard facts* to public primary sources (filings, IR decks). Use zsxq citations specifically for the analyst-opinion/estimate/channel-check layer they uniquely provide.

### If the local library is thin, fetch more — then re-search

If `find_pdf.py` returns few or stale rows for the subject (common for small / non-US / newly-covered names), top up the library from the web, then re-run the searches above:

```bash
cd /Users/x/projects/financial_agent
# Targeted: pull recent broker notes that mention the subject by ticker / name
/opt/anaconda3/bin/python3 download/zsxq_downloader.py --count 100 --query NVDA
# General top-up of the recent feed (the user's standing command):
/opt/anaconda3/bin/python3 download/zsxq_downloader.py --count 100 --query lite
```

The downloader is idempotent (records `query_term`, dedups on `file_id`), saves PDFs locally, and indexes them into `db/zsxq.db` so the next `find_pdf.py` sees them. Note in the verification log how many zsxq notes you found vs fetched.

### The "density bar" for institute-research citations

- **At least 3–6 distinct `db/zsxq.db` citations** in the body when the subject has any meaningful local coverage (a US large-cap like NVDA will have dozens of candidate notes — there is no excuse for zero).
- **At least one in Section 2 (the PT/consensus line) and one in Section 9 (the bear case)** whenever the notes support it.
- **Every one labeled `*Analyst view:*` / `*分析师观点：*`** and cited to the `/zsxq/pdf/<file_id>/<filename>` direct-download route — never blended into a filing citation.
- If the library genuinely has nothing on the subject even after a `--query` top-up, say so in the verification log; don't pad with web-searched analyst blogs in its place.

### 卖方观点演变 (Sell-side view evolution) — mandatory when ≥2 zsxq notes cover the subject

Whenever the report draws on **≥2 `db/zsxq.db` broker notes for the same company**, it MUST carry a `卖方观点演变 (Sell-side view evolution)` subsection — place it in Section 2 beside the consensus / PT benchmark line (or in Section 9.5 when the debate framing fits better). Four requirements:

1. **Mechanical pre-pass FIRST — read `db/stock_price_target.db` before re-reading any PDF.** STRICTLY READ-ONLY: `/opt/anaconda3/bin/python3` with `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`; SELECT all rows for the ticker (columns: `research_institute, rating, price_target, target_currency, report_date, report_file_id, upside_pct`). This mechanically surfaces same-institute revisions and the PT dispersion (min / median / max, spread %) before any PDF work. Writes to this DB remain exclusively via `scripts/persist_pts.py` (Tier-2 helper).
2. **Per-institute view timeline (按机构的观点时间线).** Order each institute's notes by report date — the filename's `-YYMMDD` suffix is the authoritative publication date (sanity-check against `create_time`). Per entry: institute, date, rating, PT, key estimates, one-line thesis. **Explicitly call out self-revisions** — upgrade / downgrade, PT raised / cut from X to Y, thesis pivot — and the stated trigger (earnings print, policy change, channel checks, order data). A 2026-03 PT and a 2026-06 PT from the same institute are two different views, not duplicates.
3. **Cross-institute disagreement (机构间分歧) — never blend contradictory views into a fake consensus.** When institutes disagree (opposite ratings, PTs >20% apart, conflicting reads of the same datapoint), render a disagreement table: `机构 | 日期 | 评级 / 目标价 | 核心论点 | 什么证据能证明其正确` (Institute | Date | Rating / PT | Core argument | What evidence would prove them right).
4. **Every view dated and cited.** Each institute view carries (institute, report date, `/zsxq/pdf/<file_id>/<filename>` direct-download link) per the citation format above, and the report-date-price pairing rule applies to every PT quoted in the timeline.

## Investor-lens scorecards (optional Section 10 of the report)

After Sections 1–9 establish the facts, named scoring rubrics give the reader a structured second opinion on the same evidence. **Four core lenses (default)** — **Buffett** (quality at a sensible price, 0–100), **Munger** (weighted quality + inversion, 0–10), **Damodaran** (story-plus-numbers DCF margin of safety, ±%), and **Howard Marks cycle** (market regime offense↔defense, 0–100). **Five optional lenses (add by company fit or on request)** — **Lynch GARP** (10.5, PEG + category), **Fisher scuttlebutt** (10.6, qualitative 15-point growth), **Burry forensic deep value** (10.7, hated-sector + downside-first), **Druckenmiller liquidity-regime** (10.8, macro liquidity + asymmetric sizing), **Cathie Wood Wright's Law** (10.9, cost-curve + 5-year TAM re-pricing). All nine are analytical overlays on data already cited in earlier sections; none are persona role-play. Adapted from the [LLMQuant investor-lens skill collection](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-investor-lenses) (MIT).

**When to include:** any initiation-style report where the audience is a buy/sell decision-maker. Skip only when the user explicitly says "no lens scorecards" / "skip Section 10". The section is short (600–1,000 words total) and worth the small cost.

**Placement:** new Section 10 between Section 9 Risk Assessment and the References block, in both the English and Chinese reports. Verdicts are labelled `*Lens view:*` / `*视角观点:*` per the existing analyst-view discipline — never `Buffett would buy`, `巴菲特会买`, or `Damodaran's fair value is`.

**Key inputs already in your tree:**
- Sections 1–9 facts (re-use, do not introduce new inline citations inside Section 10).
- `indicators.db` snapshot (VIX, 10Y Treasury via `^TNX`, HY OAS via FRED BAMLH0A0HYM2, IG OAS) for the cycle posture and Damodaran's risk-free rate. State the as-of date inline.
- **Canonical citation form for the cycle snapshot (MANDATORY — it is local data, not a web source).** Cite as plain text: `（来源：indicators.db 本地快照（FRED BAMLH0A0HYM2 / ^TNX + yfinance），as of YYYY-MM-DD）` (English reports: `(Source: indicators.db local snapshot (FRED BAMLH0A0HYM2 / ^TNX + yfinance), as of YYYY-MM-DD)`). Optionally link each *series name* to its specific FRED series page (e.g. `https://fred.stlouisfed.org/series/BAMLH0A0HYM2`). **NEVER attach an `indicators.db` snapshot label to a filing URL** — a 200-OK 10-K that doesn't contain the quoted yield is worse than a 404 — **and NEVER link to `localhost`** (user-facing local URLs use `xs-macbook-air.local`, and the snapshot needs no local link at all).

**See [`references/investor_lenses.md`](references/investor_lenses.md) for the nine rubrics in detail — scoring components, verdict bands, required-assumption blocks, failure modes, the routing rules for picking optional lenses by company type, and the guardrails that apply to all nine.**

## GF Score (GuruFocus-style) fundamental scorecard — Section 1B

A five-axis fundamental scorecard modelled on [GuruFocus's GF Score™](https://www.gurufocus.com/term/gf-score), placed as **Section 1B** (right after 1A Valuation & Price Target) so the decision layer — rating/PT → valuation → fundamental health — reads together near the top, mirroring the GuruFocus summary widget. **Include in every initiation-style report unless the user says "skip the GF Score".** The five axes, each ranked **0–10**, are **Financial Strength · Profitability · Growth · GF Value (valuation, higher = cheaper) · Momentum**; a transparent weighting maps them to a **0–100 composite** and GuruFocus's outperformance bands (91–100 highest … 0–50 worst). The signature visual is a **radar/pentagon** rendered as inline SVG by `scripts/gf_score.py` (stdlib-only, no matplotlib — safe for the memory budget; bakes the required source annotation into the image).

**It is an analytical overlay, like the Section-10 lenses — not a new data source and not an endorsement.** The honesty discipline is load-bearing: the five sub-scores and the composite are the analyst's own rubric output, labeled `*Analyst view:*` / `*分析师观点：*` and **never** carrying a filing citation; every underlying metric (ROE, leverage, CAGR, multiples, price returns) carries its own inline citation; and the computed number is **never attributed to GuruFocus** unless you actually pulled their published figure from `gurufocus.com/term/gf-score/<TICKER>` (shown separately as a cross-check). Each axis gets a one-paragraph rationale stating WHY that score — the "reasons" are the part the reader most wants. Its inputs are already in your tree (financials from Step 1–2, Growth from the 1A model, GF Value from the 1A multiples/intrinsic range, Momentum from the header relative-performance line), so it adds little marginal work.

**See [`reference/gf_score.md`](reference/gf_score.md) for the full spec — the 0–10 anchors per axis, the metric set behind each, the composite weights and band labels, the radar-helper usage, the multi-company overlay variant, and the honesty/citation guardrails. Read it before writing Section 1B.** Computed in Step 2c.

## Financial-statement visuals (Sankey / donut / DuPont) — `scripts/financial_charts.py`

The stockanalysis.com-style financials charts a reader expects: an **income-statement Sankey** (revenue → COGS / gross profit → opex / operating income → tax / net income, with revenue sources on the left), **balance-sheet** and **cash-flow Sankeys**, a revenue **donut** (by segment / geography), **historical stacked revenue bars**, and a **5-step DuPont** ROE tree. Like the GF Score radar, these are rendered as **stdlib-only inline SVG** by `scripts/financial_charts.py` (imports just `math` / `argparse`, ~0 MB resident — safe on the memory budget, never matplotlib) and the viewer injects the raw `<svg>` verbatim. Paste the emitted `<svg>` **un-fenced**.

**The defining discipline: every number you pass must come from the company's OWN statements that you read and cite** — the 10-K / 10-Q / 20-F / 年度报告 / IR-deck income statement, balance sheet, cash-flow statement, and segment note (ASC 280 / IFRS 8) for the segment / geography splits. The helper fetches nothing (no API, no XBRL auto-pull) — it only lays out the numbers you give it, so the project's "every figure traces to a source you read" rule holds. The required `--source` is baked into the image; the surrounding paragraph still carries the page-level citation. If a line item isn't disclosed, omit it — never invent it.

**Generate the full suite by default** (income / balance / cash-flow Sankeys + segment donut + geography donut + revbars + DuPont) — not just the income Sankey and one donut; omit a chart only when the underlying statement/disclosure truly doesn't exist, and note the omission in the Step 10 log.

**See [`references/financial_charts.md`](references/financial_charts.md) for the full spec — the six financial-statement subcommands, the per-subcommand CLI with worked ISRG examples, the embedding form, the per-section placement bar, and the sourcing guardrails. Read it before generating these in Step 8.** (The seventh subcommand, `moneyflow`, has its own spec in `references/money_flow.md` — see the next section.) Generated in Step 8.

## Money-flow (supply-chain) diagram — `scripts/financial_charts.py moneyflow` — REQUIRED, one per report

Beyond the financial-statement charts, **every report also gets a 3-stage "follow the dollars" money-flow map** in the dark gold-ribbon style — **who pays → what they buy → where the money pools.** It is the one diagram that shows where the company's COGS / capex actually *lands* (its suppliers, and their suppliers — the chokepoints), which a statement Sankey can't. It is the visual the user singled out as "very intuitive." Same stdlib-only inline-SVG engine (`moneyflow` subcommand, JSON-spec-driven, ~0 MB, never matplotlib); the SVG is self-contained and dark-themed, so it embeds cleanly in the otherwise-light report. It also renders the reference's **"Follow the money" card grid** (4–6 thesis cards summarizing the flow, gold-emphasized numbers) inside the same SVG. Paste it **un-fenced**.

It is **NOT a flow-conserving Sankey** — ribbon thickness is rough relative scale (the baked-in legend says so). Pick the orientation that illuminates the company (upstream/spend view for buyers & integrators; demand/revenue view for suppliers & component makers), use **solid** ribbons for money paid directly and **dashed** for money embedded in a finished part bought from someone else. **Every node must be a real, sourced counterpart** (named supplier/customer from filings, IR, teardown/channel reports, or the zsxq library — never an invented one); any `$` figure in a ribbon label must string-match a cited source; `--source` is baked into the footer; the surrounding paragraph carries the inline citations and a short sourced "follow the money" note.

**See [`references/money_flow.md`](references/money_flow.md) for the full JSON spec, the `kind` palette, the two orientations, the worked Tesla/SpaceX example, placement, and the sourcing guardrails. Read it before generating the diagram in Step 8.** Place it in **Section 4 (Products & Services)** as the supply-chain anchor, or **Section 6 (Industry)** as the value-chain visual — wherever the supply chain is actually discussed. Generated in Step 8.

## Learning from sell-side institutional research

A methodology study of 22 initiation / deep-dive notes from Goldman Sachs, Morgan Stanley, UBS, J.P. Morgan, Bernstein, Nomura, Citi, BofA, Deutsche Bank, and HSBC found one structural gap: **every institutional single-name note is a decision note built around a rating and a price target, while this skill produces a descriptive profile that stops at a TTM-multiple snapshot.** The lessons below close that gap. They are additive — every existing rule (no fabricated numbers, paragraph-level citations, `*Analyst view:*` labeling, language defaults, file-naming) holds unchanged. The defining discipline that makes this safe: **the rating, the price target, every projected estimate, and the scenario PTs are all the analyst's own forward view — they MUST be labeled `*Analyst view:*` / `*分析师观点：*` and NEVER attached to a filing citation.** A 10-K does not contain a price target; attaching one to a 10-K is the same misattribution failure the skill already forbids.

- **Open every report with a standardized header block — mirror the Deutsche Bank / GS / Citi cover page.** Before the TOC (after the optional guidance banner): **Rating** (Buy / Hold / Sell, or OW / Neutral / UW — pick one scale and state it), **12-month Price Target**, current price, implied upside / downside %, one-line valuation method, market cap, 52-week range, ticker / exchange, then the **2–4 thesis pillars** one sentence each. The whole block is labeled `*Analyst view:*` — it is a house view, not filing data. See `references/report_structure.md` § "Investment summary header".
- **Lead Section 1 with the thesis, not the description — BLUF house style (every analog does this).** The first paragraph states the call, the why-now, and the 2–4 pillars before any "what the company does" prose. Deutsche Bank's Huayan note opens "Buy, TP HK$28.2" with three bolded sub-heads; J.P. Morgan's Yingliu note opens with the scarcity-positioning thesis. Keep all 9 descriptive sections — they feed the thesis — but add the synthesis layer on top.
- **Build a forward financial model — a multi-year estimates table is non-negotiable.** Project **revenue / gross margin / operating-or-net margin / EPS 3 years forward** (the analogs run 3–5: Yingliu RMB2.9bn→11.3bn 2025–2030E ~30% CAGR; Horizon licensing-65%→hardware-47% mix shift by 2027). Each projected cell is `*Analyst view:*`; each driver's external basis is cited inline (filing segment data + management guidance + an industry forecast) per the existing "the analyst's own model is NOT a source" rule. Model the **segment mix shift** (each line gets its own revenue path + margin trajectory, then summed — Tesla's 6-way SOTP), not just a blended top-line.
- **Derive the price target and SHOW the arithmetic — mirror J.P. Morgan's Yingliu (`2028E EPS × 40x PE = RMB95`).** State the method: forward-EPS × target multiple, or DCF (WACC built from `indicators.db` 10Y + a stated ERP, terminal growth ≤ risk-free), or SOTP, or rNPV for biotech. **Justify the multiple against 3–5 named comps** — JPM defended Yingliu's 40x against Howmet's 37x on a 55%-vs-23% EPS-CAGR gap. The justification of the multiple is as load-bearing as the number itself.
- **Give three price targets — bull / base / bear — each tied to its swing assumption (Morgan Stanley Hesai $53 / $30 / $11.5; Citi Yunnan-Energy 3-scenario table).** Base = central estimates; bull = faster attach / penetration or a higher multiple; bear = price war / margin compression. Report upside / downside % on each so the reader sees risk-reward symmetry at a glance. All three labeled `*Analyst view:*`.
- **Position the forward estimates against consensus — the UBS / Nomura "+16% vs Street" move.** When the local zsxq library or other sourced material carries Street estimates or a consensus PT, state where the report's own numbers sit (above / below, by how much). UBS framed Alphabet 2027E revenue "+16% vs Street"; Nomura framed peak sales "57% above market". Source the consensus number to the zsxq note (`*Analyst view:*`) or a dated public source — **never invent a consensus figure** (this reinforces, not loosens, the numerical-accuracy rule).
- **Add a "Key debates & catalysts" block — distinct from the risk inventory (Morgan Stanley's 市场核心分歧 / Hesai three-debate pattern).** List the 2–4 arguments the bears make and rebut each; then a **dated forward-catalyst list** for the next 12 months (GS Hemab: Phase-3 start H2-26, FVIID data late-26) with a pointer to the catalyst-calendar skill for ongoing tracking. Keep the risk *taxonomy* itself in Section 9 — debates defend the thesis; risks inventory the downside.
- **Name the 1–2 swing variables the call hinges on (MS Hesai: lidar-GM floor + auto attach rate; UBS Alphabet: TPU rev-rec timing + Vertex mix).** The reader should know which assumption to pressure-test. Tie every margin-trajectory claim to its driver (mix shift / operating leverage / pricing power) — never just "margins improve".
- **Treat proprietary channel checks as a named, citeable evidence class.** When the local zsxq notes carry channel-check data (NE Times monthly shipment trackers, Frost & Sullivan rankings, credit-card spend panels, App-download / Google-Trends momentum), cite it as `*Analyst view:*` via the broker note and flag it as channel-check-derived so the reader knows its provenance. Every analog leans on channel checks; the skill has the zsxq plumbing but hadn't named this evidence type.
- **Pair every number with a comparison anchor and conviction label.** Sell-side numbers rarely appear bare: `+33% YoY`, `vs consensus +16%`, `47% upside`, `GM 36%→43%`. Conviction language is calibrated and explicitly labeled (`preferred pick` / `top idea` / `under-appreciated` / `fully priced`) — and under this skill's rules it stays an `*Analyst view:*`, never attributed to a filing.

**Cover-page & exhibit discipline (the Bernstein ISRG 4Q25 study).** A close read of one institutional single-name note — Bernstein's *"Intuitive Surgical 4Q25: Squeaky clean quarter; top pick (PT $750)"* — surfaced five concrete habits worth importing wholesale; each is now specified in `references/report_structure.md` (header block + Section 1A):
  - **A forward valuation *matrix*, not one multiple.** The cover carries P/E, PEG, EV/EBITDA, EV/FCF, EV/Sales across last-actual / FY1E / FY2E so the reader sees the multiple compress as estimates grow (ISRG Adj P/E 58.9× → 52.0× → 44.9×). Add ROIC and a CAGR column to the forward model, and run it **quarterly + annual, by revenue segment** — annual-only endpoints hide the inflection.
  - **A margin bridge with bps.** Decompose every GM / operating-margin move into named drivers with magnitudes (`GM −110bps = tariffs −95bps · richer dV5/Ion mix −40bps · facility depreciation −30bps · cost reductions +55bps`). "Margins improve" is not analysis.
  - **A Guide-vs-Consensus-vs-Own table.** When the company guides, lay company-guide / Street-consensus / this-report side by side (Bernstein Exhibit 1), each column sourced per its provenance.
  - **Revision transparency.** On a refresh, show prior beside new (`PT $750 (was $740)`, `FY27E EPS $11.72 (was $11.61)`) and attribute the PT move to estimate-change vs multiple-change (Bernstein's was 100% estimate — multiple held at 64×).
  - **Management quotes are the spine, and every exhibit caption states the conclusion.** The note anchors each thematic claim (cardiac TAM, XiR/ASC opportunity, China pricing) to a multi-sentence verbatim earnings-call Q&A block, and every chart caption states the takeaway ("ISRG guided to 67–68% GM, **above** consensus 67.2%"), not just the source. Quote management densely from transcripts; write exhibit captions as findings, not labels.

## Report language

**Default behavior: produce ONLY a Simplified Chinese (zh-CN) report.** Never Traditional Chinese, Japanese, or Korean for the prose. An English-language report is produced only when the user explicitly opts in.

**Explicit user override (highest priority).** Honor any of these phrasings without asking:

| User says | Output |
|---|---|
| No override | **Simplified Chinese only** (default — one file: `<Slug>_公司研究.md`) |
| `"... in Chinese only"`, `"用中文即可"`, `"只要中文"`, `"--lang zh"`, `"--zh-only"` | Same as default — Simplified Chinese only |
| `"... in English"`, `"English report"`, `"English only"`, `"just English"`, `"--lang en"`, `"--en-only"` | English only (skip Chinese; one file: `<Slug>_Research_Document.md`) |
| `"... in English and Chinese"`, `"both languages"`, `"bilingual"`, `"also in English"`, `"也出一份英文"`, `"加一份英文"` | Both languages — two separate files in the same folder |

Examples:
- `research SZSE:002050` → **one file: Chinese only** (default)
- `research NVDA` → **one file: Chinese only** (default)
- `research Tesla in English only` → English report only
- `research 比亚迪 用中文即可` → Chinese report only (= default)
- `research NVDA bilingual` / `research NVDA also in English` → two files: Chinese + English
- `research NVDA in English and Chinese` → two files: Chinese + English

**Single-language mode (default) produces one complete report file**, written natively in Chinese and independently meeting the 6,000–10,000 word target (counted in characters). Filename (no date suffix — see the "Filenames" section below; **English / pinyin component is mandatory**):

- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_公司研究.md` (Chinese, default)

**Bilingual mode (only when the user opts in)** produces two complete, separate files in the same output folder — not one interleaved document. Each meets the 6,000–10,000 word target independently. The pair:

- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_公司研究.md` (Chinese)
- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md` (English)

Both files share the same underlying research — citations, charts, data — but write the prose natively in each language; do not literal-translate one from the other.

**Write natural Simplified Chinese — never word-for-word calques of English headers/terms (MANDATORY).** The Chinese prose must read as if written by a native Chinese equity analyst, NOT machine-translated. The failure mode to avoid: literally rendering an English label into a Chinese compound that no Chinese analyst would write. Concrete past offenders and their fixes — do not reproduce the left column:
> - "house view" → ❌ `房观点` (房 = building!) → ✅ `本方观点` / `本报告观点`
> - "Guidance banner" → ❌ `业绩更新横幅` (横幅 = a UI banner) → ✅ `业绩更新` / `业绩快报`
> - "per-axis rationale / why these scores" → ❌ `逐轴理由` → ✅ `各维度评分理由`
> - "swing variables" → ❌ `枢纽变量` → ✅ `最该盯紧的变量` / `关键变量`
> - "multiple justification" → ❌ `倍数的辩护` (辩护 = legal defense) → ✅ `为什么用这个倍数` / `估值倍数依据`
> - "vs consensus" → ❌ `对照市场一致` (incomplete) → ✅ `与市场一致预期的对比`
>
> Rule of thumb: an English *technical term* keeps its English form + a Chinese gloss (per the list below); but an English *section heading or rhetorical label* must be re-expressed in idiomatic Chinese, not transliterated morpheme-by-morpheme. When unsure whether a Chinese rendering sounds natural, prefer the plainer, more conversational phrasing a Chinese sell-side note would use. This applies to all report-producing skills.

**Technical terms in Chinese reports — keep the English term alongside the Chinese gloss (MANDATORY).** Since most technical / industry / financial / regulatory terms originate in English (or have established English equivalents), the Chinese report **uses both languages**: English term first with the Chinese gloss in parentheses on first mention, then either form is fine thereafter. For specific named entities (products, ratings, indices, regulations), keep the English form throughout. Categories where this rule applies:

- **Financial metrics:** `gross margin (毛利率)`, `operating margin (经营利润率)`, `free cash flow / FCF (自由现金流)`, `EBITDA`, `ROIC (投资回报率)`, `ROE`, `EV/EBITDA`, `P/E`, `P/S`, `P/B`, `working capital (营运资本)`, `CapEx (资本开支)`, `R&D (研发费用)`, `SG&A`.
- **Industry / technical concepts:** `semiconductor (半导体)`, `advanced packaging (先进封装)`, `gate-all-around / GAA (栅极环绕)`, `high-bandwidth memory / HBM (高带宽内存)`, `wafer (晶圆)`, `foundry (晶圆代工)`, `data-center GPU (数据中心 GPU)`, `EV (电动车)`, `LFP / NMC battery (磷酸铁锂 / 三元电池)`, `BMS (电池管理系统)`, `Tier-1 supplier (一级供应商)`.
- **Pharma / biotech:** `GLP-1 agonist (GLP-1 激动剂)`, `IND filing (新药临床试验申请)`, `Phase III trial (三期临床)`, `mAb (单克隆抗体)`.
- **Software / SaaS:** `ARR (年度经常性收入)`, `NRR / NDR (净收入留存率)`, `CAC (获客成本)`, `LTV (用户终身价值)`, `churn (流失率)`, `multi-tenant (多租户)`.
- **Corporate / governance / regulatory:** `OEM / ODM`, `SOE (国有企业)`, `RMB / USD`, `MIIT (工信部)`, `CSRC (证监会)`, `NDRC (发改委)`, `SAMR (市场监管总局)`, `Specialized & Sophisticated SME / 专精特新`, `bp / bps (基点)`, `YoY (同比)`, `QoQ (环比)`.
- **Product names / ratings / indices stay in English throughout:** `H200`, `Blackwell`, `Sense.i®`, `ALTUS®`, `Buy/Hold/Sell`, `S&P 500`, `MSCI A50`, `CSI 300`, `Nasdaq-100`. Do not translate these.
- **Ticker codes and acronyms stay in their original form:** `SZSE:002050`, `NASDAQ:NVDA`, `HKEX:9988`.

The reason for keeping English alongside Chinese: most of the cited sources (10-K, IR decks, sell-side research, industry reports from Yole / Gartner / IDC) use the English terms — preserving them in the Chinese prose makes citations cross-checkable and prevents lossy translation of terms-of-art (e.g. translating `gross margin` as `毛利` vs `毛利率` matters; keeping `gross margin` removes the ambiguity).

**Products & Services section (Section 4):** the bilingual gloss is even denser here. See the dedicated section above for the `**中文释义 / Plain-language gloss:**` requirement.

**Chinese names in English reports (when bilingual mode is on):** Chinese companies (subject, competitor, customer, partner) may appear in their original Chinese form alongside an English / pinyin gloss on first mention, e.g. `安培龙 (Anpeilong, SZSE:002050)`, `比亚迪 (BYD)`, `宁德时代 (CATL)`. After first mention, either form is fine.

**Direct quotations** stay in their original language regardless of the report's main language — add a short translation in parentheses only if the quote is load-bearing.

**Filenames (no date suffix):**
- **MANDATORY: every filename must include the company's English / pinyin name as the first slug component** — even for Chinese reports. The English name is what makes a file findable via `grep -r Kinik` / Spotlight / the viewer's search. A filename with only Chinese characters fails this test. **Format: `[EnglishName]_[中文名]_[EXCHANGE][CODE]`** (Chinese name optional but recommended for cross-language search).
- Chinese reports: `reports/company/Kinik_中砂_TWSE1560/Kinik_中砂_TWSE1560_公司研究.md`, `reports/company/Anpeilong_安培龙_SZSE002050/Anpeilong_安培龙_SZSE002050_公司研究.md`. The English / pinyin component is **mandatory**, the Chinese name component is **strongly recommended** (so the file is findable by either name); ticker is mandatory.
- English reports: ASCII — `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md`, `reports/company/Alibaba_HKEX9988/Alibaba_HKEX9988_Research_Document.md`. For Chinese companies, may also include 中文名: `reports/company/BYD_比亚迪_HKEX1211/BYD_比亚迪_HKEX1211_Research_Document.md`.
- Never Japanese kana / kanji or Korean hangul in filenames; use Romaji / Romanization (e.g. `Toyota_TSE7203`, `Samsung_KRX005930`).
- Do **not** append `_YYYY-MM-DD` to research-doc filenames. Only one EN file and one ZH file exist per company, so a date in the filename adds no signal and clutters the slug folder. Put today's date inside the document as an "as of" header instead; git history tracks the actual revision date.

**Section headers (Chinese reports):** 公司概览, 公司历史, 管理团队, 产品与服务, 客户与上市策略, 行业概览, 竞争格局, 市场机会, 风险评估, 参考资料.

## Primary-source-first & development-over-time rule (MANDATORY)

The user's standing preference for every report-producing skill: **reference the 10-K / 10-Q / original investor-relations materials as much as possible, cite them at page level, and present the material so the reader can see the company's development over time — what's new this period.**

1. **Source-preference order for any company fact.** (1) The company's own filings — 10-K / 10-Q / 8-K / DEF 14A / 20-F / 6-K / S-1 on EDGAR, or the non-US equivalent (年度报告 via cninfo, HKEX annual report, 有価証券報告書, 사업보고서); (2) original IR materials — earnings press release, earnings / investor-day deck, call transcript, shareholder letter; (3) third-party industry research; (4) news. **Business sections especially run on the 10-K.** For business fundamentals — what the company does, segment structure, products and how they make money, customers and concentration, competition, manufacturing / supply chain, IP, regulation, headcount — the 10-K is the default first-stop source (`Item 1 Business`, `Item 1A Risk Factors`, `Item 7 MD&A`, each cited with page), refreshed by the latest 10-Q for in-year changes; non-US equivalents use the annual report's business chapter (年度报告 经营情况讨论与分析, 有価証券報告書 事業の状況). Never cite a news rewrite for a fact that lives in a filing or an IR original — chase the original. Sell-side / zsxq broker notes are NOT displaced by this rule: they remain the separate `*Analyst view:*` layer (with their own page-level cites) and are never blended into the company-fact layer.

2. **10-K / 10-Q / annual-report citations must carry page numbers.** Format: `[NVDA FY2025 10-K, p. 42 — Segment results](https://www.sec.gov/...)`. When the EDGAR HTML doc makes the print page hard to pin down, give the Item + note/section heading instead (`Item 2 MD&A — Data Center revenue`, `Note 17 — Segment Information`) so the reader lands within one page-flip of the number. A bare `[10-K](url)` with no page/section locator fails the citation bar. The same locator discipline applies to prospectuses (page), IR decks (slide number), and non-US annual reports (第 N 页 / p. N).

3. **Present development over time — "what's new".** Do not render the company as a static snapshot. Wherever the output's structure allows, frame disclosures diachronically: trace the same line item across consecutive 10-Ks / 10-Qs (segment revenue & mix, risk factors added / dropped, customer-concentration %, capacity / capex, backlog, headcount, guidance language) and state explicitly what is NEW in the latest filing versus the prior one. Preferred presentations: an evolution table (`FY23 → FY24 → FY25`, each column cited to its own filing + page) and/or a short "What changed this period / 本期新变化" callout where the section covers a recurring disclosure.

4. **English originals stay English — even in Chinese-language reports.** When the original source is English (SEC filing, English IR deck / transcript / press release), cite and quote the English original directly; do not substitute a Chinese-media rewrite for language consistency. Symmetric with the existing original-language rule: the original's language always wins, whichever it is.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the subject of the output — the ticker, theme, sector, ETF holdings, deal, or any name that materially drives the analysis — sits in **AI** (foundation models, AI software/agents, AI infrastructure: datacenter compute, networking, power), **robotics** (humanoids, industrial automation, AMRs, actuators / reducers / sensors / end-effectors), or **semiconductors** (fabless, foundry, IDM, memory/HBM, equipment/WFE, materials, EDA/IP, advanced packaging), give those names a **detailed narrative treatment**, not summary bullets:

- **Write full narrative prose** for the sector-relevant sections — mechanism and causality ("X drives Y because Z"), not headline restating. Bullets may organize the prose but never replace it.
- **Cover the sector-specific dimensions that apply:**
  - *Technology position & roadmap* — process node / architecture / model-capability cadence vs named competitors (e.g., N2 vs 18A, HBM3E→HBM4, GB200→Rubin, Optimus gen-3 vs Figure 03).
  - *Supply-chain position* — key suppliers and customers up/down the chain, single-source chokepoints (TSMC/CoWoS, EUV, HBM), where pricing power sits, content-per-unit ($ per GPU / per robot / per vehicle).
  - *AI demand linkage* — the explicit path from AI capex to this name's P&L (orders → backlog → revenue recognition) with the actual disclosed numbers, never a generic "AI beneficiary" label.
  - *Robotics linkage* — design-win status, which platforms (Tesla Optimus, Figure, Unitree, domestic Chinese OEMs), volume and timeline realism vs the hype cycle.
  - *Cycle context* — where the semi / memory-pricing / AI-capex cycle stands right now and what that implies for forward estimates.
  - *Geopolitics & export controls* — US BIS rules, China localization, tariff exposure, entity-list status where relevant.
- **Quantify the narrative.** Each dimension covered should carry at least one sourced number (TAM, ASP, capacity, units, share). All figures obey the project's numerical-accuracy rule — every number traces to a URL or PDF page cited in the same paragraph.
- **Engage the sell-side view.** Where the zsxq library or other broker sources are in scope for this skill, the AI/robotics/semi narrative must engage the institute view (PTs, estimate revisions, cross-broker disagreement) rather than ignoring it.

This rule **deepens** the skill's existing output format — it never replaces or shortens the required structure. For subjects outside these sectors, the skill's baseline depth applies unchanged.

## Citations

**Paragraph-level citation coverage is the standard.** Every substantive paragraph — any paragraph making a factual, quantitative, or external-source claim — must contain at least one inline markdown-link citation. The user's stated trust standard: *"for each paragraph, I hope there is citation, otherwise I don't trust the paragraph."* This includes qualitative analysis paragraphs (industry framing, competitive positioning, management assessment) — cite the 10-K / 年度报告 / Yuho section, the earnings transcript, or the industry research that supports the framing.

Every inline citation is a **clickable markdown link to the real source URL** — `[Title in original language](https://real-url)` — never a bare `(Source: ...)` parenthetical. Link titles preserve the original language (`年度报告`, `10-K`, `決算短信`, `사업보고서`); URLs are canonical permalinks (the actual SEC EDGAR document URL, the specific cninfo PDF, the article permalink — not homepages). No fabricated URLs — if you cannot find the real link, say so inline.

**Density target: ≥40 inline citations across the body of a 6,000–10,000 word report.** Reports landing under 40 have insufficient sourcing — go back and cite uncited paragraphs before submitting.

**Prefer recent web sources.** For non-filing web citations (news, industry reports, third-party rankings, analyst notes), default to sources from the **last 12 months**. Discard older web sources unless they're founding/historical facts or still-authoritative landmark research. Always include the publication date in the link title so vintage is visible: `[Reuters, 2025-08-12](https://...)`.

See [`reference/citations.md`](reference/citations.md) for the full rules, per-source examples, freshness exceptions, and the final References-block format. **Read it before drafting.**

## Reference docs (read on demand)

> Path note: **`reference/…`** (singular) = repo-level **shared** specs imported across skills (`citations.md`, `gf_score.md`); **`references/…`** (plural) = this skill's own local specs. They are different directories.

- `references/report_structure.md` — section-by-section word counts, per-section content spec, the investment-summary header block, the Section 2 "Valuation & Price Target" chapter (forward-estimates table + PT derivation + bull/base/bear), the Section 9.5 "Key debates & catalysts" block, and the full output template. **Read before writing.**
- `reference/citations.md` — inline-citation rules and example.
- `references/ir_materials.md` — the full investor-relations collection bar: what to collect, where to find it per domicile (US / China-HK / TW / JP / KR / private), the per-section "what IR slides unlock" table, the slide-level citation discipline, and the IR-citation density bar.
- `references/risk_taxonomy.md` — the 8–12 risks across 4 buckets used in Section 9.
- `references/investor_lenses.md` — the nine Section-10 lenses (4 core: Buffett, Munger, Damodaran, Howard Marks cycle; 5 optional: Lynch, Fisher, Burry, Druckenmiller, Cathie Wood).
- `reference/gf_score.md` — the GF Score (GuruFocus-style) Section-1B scorecard: five 0–10 axes (Financial Strength / Profitability / Growth / GF Value / Momentum), composite 0–100 + bands, the inline-SVG radar helper (`scripts/gf_score.py`), and the honesty/labeling rules.
- `references/financial_charts.md` — the stockanalysis.com-style financial-statement visuals helper (`scripts/financial_charts.py`): income / balance / cash-flow **Sankey**, revenue **donut** (segment / geography), **historical stacked bars**, and **5-step DuPont** ROE tree — all stdlib inline SVG, with per-subcommand CLI, worked ISRG examples, placement, and sourcing guardrails. **Read before using in Step 8.**
- `references/money_flow.md` — the **money-flow (supply-chain) diagram** helper (`scripts/financial_charts.py moneyflow`): the 3-stage "who pays → what they buy → where the money pools" gold-ribbon map (REQUIRED, one per report), the JSON spec, the `kind` palette, the two orientations (spend vs. demand), the worked Tesla/SpaceX example, placement (Section 4 or 6), and sourcing guardrails. **Read before using in Step 8.**
- `references/quality_checklist.md` — quality standards and the pre-submit success checklist.
- `references/verification.md` — the Step-10 bash recipes (URL check, EDGAR submissions-JSON filename lookup, 10-K claim grep, exec-name check) and the verification-log template. Read before the Step 10 pass.

---

## Data sources — website-first, then filings, then research

**Always start with the company's own website.** Then route filings by domicile. Research firms come third.

### Official company website (START HERE)

- **Product pages** — product specs, use cases, pricing, customer names, case studies, comparison matrices. **Quote the company's own product descriptions and specifications verbatim.**
- **About / Company page** — company history, mission, strategy, key statistics disclosed. **Use exact language from the company's "About" section.**
- **Leadership / Team page** — founder and CEO bios (names, titles, prior roles). **Quote bio text directly if it contains relevant background.**
- **IR site** (if exists) — earnings decks, investor-day presentations, integrated reports, annual reports, press releases. **Quote management statements from decks and transcripts; reference specific slide numbers.**
- **Blog / Newsroom** — last 12 months for launches, customer wins, guidance, announcements. **Quote press releases for product announcements, customer wins, and timeline facts.**
- **Native-language version** (for non-US/English-primary companies) — e.g. `company.com.cn`, `company.co.jp`, `company.kr` is often richer than the English version. **Read and quote from the native version; preserve original language in citations.**

### Regulatory filings (SECOND, to fill gaps and verify financials)

**SEC EDGAR only covers US issuers. Do not look for non-US filings there.**

- **US** → SEC EDGAR: latest 10-K, recent 10-Qs, DEF 14A, recent 8-Ks. Helper: `fetch_financial_report.py` (DB: `db/financial_reports.db`). **Company IR site (mandatory pull):** `investors.<company>.com` or `ir.<company>.com` → Events & Presentations (earnings decks, investor days, conference presentations), Quarterly Results (transcripts), SEC Filings → 8-K Exhibit 99.2 attachments.
- **China A-share / HK** → cninfo (巨潮资讯, https://www.cninfo.com.cn/): 年度报告, 季度报告 / 半年度报告, 重大事项公告. Ticker format `SZSE:002050`, `SSE:688802`, `HKEX:2513`. Helper: `fetch_cninfo_report.py` — run from `/Users/x/projects/financial_agent` so files land in `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/`. Chinese-language disclosures are authoritative; English IR pages are secondary. **Company IR site (mandatory pull):** company IR page (`<company>.com/investors` / `<company>.cn/investors` / 投资者关系) for 业绩说明会 PPT + 投资者交流活动记录; cninfo also files `投资者关系活动记录表` quarterly with formal Q&A logs.
- **Taiwan (TWSE / TPEx)** → MOPS (公開資訊觀測站, https://mops.twse.com.tw/): 年報, Q1–Q3 reports, 重大訊息. **Company IR site (mandatory pull):** MOPS 法人說明會 (analyst meeting decks) section + company IR page.
- **Japan** → EDINET (https://disclosure2.edinet-fsa.go.jp/) for Yuho (有価証券報告書) + Shihanki (四半期報告書); TDnet (https://www.release.tdnet.info/) for 決算短信. **Company IR site (mandatory pull):** company IR site → 「決算説明会資料」 (earnings deck per quarter), 「統合報告書」 (Integrated Report — annual; often the single richest source for narrative, TAM, segment economics), 「中期経営計画」 (Mid-term Plan — every 3–5 years; multi-year revenue / margin / capex / ROIC targets).
- **Korea** → DART (https://dart.fss.or.kr/, English: https://englishdart.fss.or.kr/): 사업보고서, 반기보고서, 분기보고서, 주요사항보고서. **Company IR site (mandatory pull):** company IR site → Earnings Release PDFs (quarterly), Investor Presentations archive, Annual Report PDF (often distinct from the DART 사업보고서 — the IR-site annual is glossier and more narrative).
- **Other** → country's official portal (SEDAR+ Canada, ASX Australia, LSE RNS UK, BSE/NSE India). Do NOT fall back to SEC EDGAR unless the issuer is a 20-F / 6-K filer. **Company IR site (mandatory pull):** every major issuer has a public IR site — collect quarterly decks + annual report + any capital-markets-day deck.
- **Private companies** → company website + blog, press coverage, LinkedIn for bios, Crunchbase/PitchBook for funding history. For IPO-stage names, the S-1 / F-1 / 招股说明书 prospectus on the local exchange portal is the deepest single source.

### Third-party research (THIRD, for market context and trends)

- **Local institute-research library `db/zsxq.db` (START HERE among third-party sources).** ~6,900 broker PDFs (Morgan Stanley, Goldman, J.P. Morgan, Bernstein, UBS, Citi, Deutsche Bank, HSBC, Nomura, …). Search it BEFORE web-searching for analyst views: `/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "<ticker / name / 中文名>"`. The curated `summary` column often already carries broker + rating + price target + thesis (no PDF parsing needed); OCR + extract the body when you need verbatim quotes. **Sell-side — label `*Analyst view:*` and cite to `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>`.** Full workflow in § "Local institute-research library" above; it is **Step 0.7** of the workflow.
- **Industry research firms** (Gartner, IDC, Yole, TrendForce, TechInsights, Forrester) — used for market-sizing, competitive positioning, and industry benchmarks the company's filings don't provide.
- **Sell-side analyst reports** (JPMorgan, Goldman, Bernstein, Needham, TechInsights) — for forward-looking commentary, peer comparisons, and thesis validation. **Note:** these are sell-side opinions, not primary facts. Check `db/zsxq.db` first (above); web-search only fills gaps the local library doesn't cover.
- **Trade press and news** — for recent developments, confirmation, and context. Only as supporting evidence, not as primary claim sources.
- **Competitor websites and filings** — when explaining competitive positioning; cite the competitor's own source, never the subject company's characterization.

**See [`references/ir_materials.md`](references/ir_materials.md) for the full IR-collection bar — every IR site listed above carries materials that should yield 8–12+ citations in the finished report.**

---

## Prerequisites

For **US issuers**, this skill runs [[sec-report-summary]] as a sub-step (Step 0.5 below). The multi-year SEC narrative it produces — per-filing highlights + a "Changes over the years" trajectory — becomes structured input for Section 4 (product evolution), Section 6 (industry trajectory), and Section 9 (risk-factor evolution). As a company-research sub-step it is an **intermediate, not a deliverable** — write it to an in-session scratch file (`/tmp/finagent-sec-summary/<TICKER>.md`), fold its content into the report body, and never commit it under `reports/` (see Step 0.5). Run it for every initiation (first write for the ticker); on a refresh of an existing report it may be skipped — but only with a stated reason recorded in the Step 10.6 verification log (see Step 0.5's run-or-log rule). Silent skipping is the failure mode.

For **non-US issuers** (China A-share / HK / Taiwan / Japan / Korea), skip the sec-report-summary step — the `/sec/` infrastructure is US-only. Build the same historical-evolution threads directly from the domicile-portal filings synced in Step 0.

---

## Workflow

### Step 0 — Sync filings (always run the fetch script first)

**Default behavior: run the fetch script before reading anything.** The scripts are idempotent — they check the source portal (SEC EDGAR / cninfo) for new filings and download only what's missing locally. Existing files are skipped. Mtime-based freshness checks can miss a filing that just dropped, so don't rely on them as a "skip the fetch" shortcut.

**Always run first:**

- **US issuers:**
  ```bash
  cd /Users/x/projects/financial_agent
  /opt/anaconda3/bin/python3 fetch_financial_report.py <TICKER>
  ```
- **China A-share / HK issuers:**
  ```bash
  cd /Users/x/projects/financial_agent
  /opt/anaconda3/bin/python3 -c "import fetch_cninfo_report as cr; cr.init_db(); [print(m) for m in cr._run_download('SZSE:002050', cr.ALL_CATEGORIES)]"
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

### Step 0.5 — Multi-year SEC narrative (US issuers only)

For US issuers, immediately after Step 0 invoke [[sec-report-summary]]'s logic with `--ticker <TICKER> --form 10-K --last 10 --deep` to produce the per-filing highlights and the "Changes over the years" trajectory.

**This is an intermediate input, not a deliverable — do NOT persist it under `reports/`.** When sec-report-summary runs *as a company-research sub-step*, override its default `reports/earnings/<TICKER>_<YYYYMMDD>.md` output and write the narrative to an in-session scratch file under `/tmp/finagent-sec-summary/<TICKER>.md` instead. Read it back, fold its content into the report body (below), then leave it — never `git add` it. The `reports/earnings/` folder is for the `earnings-analysis` skill's quarterly notes, **not** for this multi-10-K scratch summary; a committed `reports/earnings/<TICKER>_<date>.md` from this step is exactly the bug this rule exists to prevent. (A user who invokes `/sec-report-summary` *directly* still gets the persisted `reports/earnings/` deliverable — that standalone path is unchanged; only the company-research sub-step is scratch-only.)

Use that narrative as the **structured input** for:

- **Section 4 (Products & Services)** — product-line transitions, sunsets, segment renames called out in the multi-year filing comparison.
- **Section 6 (Industry)** — segment-reporting changes, geographic mix shifts (e.g. China revenue going from highlight to risk).
- **Section 9 (Risk Assessment)** — risk-factor evolution: new categories appearing (cyber, AI, climate, tariffs), persisting categories, resolved litigation.

**Cite the underlying filings inline, never the scratch file.** Each number/claim the narrative feeds into Sections 4/6/9 carries its own deep SEC EDGAR 10-K URL as the citation (per the project citation standard — a local `.md` path is not a valid source). The Data Used manifest must NOT list a `reports/earnings/...` path for this step.

**Do not re-run this step if you already produced the scratch narrative earlier in this same session** for this ticker — read the existing `/tmp/finagent-sec-summary/<TICKER>.md` instead. (There is no cross-session cache by design; an initiation is a first write, so there is rarely a prior pass to reuse.)

**Run-or-log rule (MANDATORY — silent skipping is the documented failure mode).** Run this step on every initiation (first write for the ticker). For a refresh of an existing research doc it may be skipped — it is a heavy multi-10-K pass on a 16 GB machine — but only with a stated reason. Either way, the Step 10.6 verification log MUST carry the line `**Step 0.5 sec-report-summary** — ran (in-session scratch, not persisted)` or `— skipped (<reason>)`. A US-issuer report whose log has neither is not done.

**Skip this step entirely for non-US issuers** — sec-report-summary depends on the `/sec/` Flask service + `db/financial_reports.db`, which only cover SEC filings. For China A-share / HK / Taiwan / Japan / Korea, build the historical-evolution threads directly from the domicile-portal filings synced in Step 0.

### Step 0.7 — Search the local institute-research library (always run, all domiciles)

Before touching the website, **search `db/zsxq.db` for broker notes on the subject** — this is the project's local sell-side library and it is the fastest way to learn what the Street thinks. Run one `find_pdf.py --query` per alias (ticker, English name, native-language name), plus a couple of supply-chain / competitor / theme terms:

```bash
cd /Users/x/projects/financial_agent
for q in "NVDA" "NVIDIA" "英伟达" "Blackwell" "AI server"; do
  echo "── $q ──"
  /opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "$q" --limit 40
done
```

Triage the JSON: keep the 5–15 most relevant + most recent rows (apply the 12-month freshness rule). **Read each kept row's `topic_title` + `summary` (the curated 翻译精华) first** — for most rows that already gives you the broker, rating, price target, valuation basis, and 2–4 thesis points without opening the PDF. Open the body (OCR → `extract_pdf.py`) only when you need a verbatim quote or a number the summary omits.

**If the library is thin or stale for this name**, top it up, then re-run the search:

```bash
/opt/anaconda3/bin/python3 download/zsxq_downloader.py --count 100 --query NVDA   # targeted by ticker/name
/opt/anaconda3/bin/python3 download/zsxq_downloader.py --count 100 --query lite   # general recent-feed top-up
```

Everything from this step is **sell-side opinion** — carry the `file_id`s forward and cite them as `*Analyst view:*` / `*分析师观点：*` to `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>` (never blended into a filing citation). Full search-and-cite rules: § "Local institute-research library" above. Record found-vs-fetched counts in the Step 10 verification log.

### Step 1 — Initial data collection (website-first approach)

**Start with the company's own official website; move to filings and third-party research only when the website doesn't provide sufficient depth.**

1. **Thoroughly analyze the company website** (do not skim — this is the primary source of ground truth on what the company actually sells). Spend 30–60 minutes on this; it is the foundation of Section 4 (Products) and Section 5 (Customers).
   - Read every About / Company / Mission / Vision page; note founders' framing, company history, stated strategy.
   - **Walk the entire product / solutions navigation tree exhaustively.** Enumerate every distinct product, SKU family, or service line — even 10–30+ items. Do not collapse them; the website's own categorization is the authoritative structure.
   - For each product page, capture: official name (exactly as the company spells it) + variants/tiers, one-sentence description (quote verbatim from the site), target customer segment, pricing model if disclosed, key specifications/technical details (quote or closely paraphrase the company's own language), differentiators the company highlights, any "new"/"flagship"/"market-leading" badges, product-launch date if shown. **Do not paraphrase product definitions; use the company's own words.**
   - **Identify and name every customer shown on the site** — homepage logos, case-study names, testimonials, customer list page. **Quote case-study excerpts that explain the customer's use case** — the customer's own words (not the company's gloss on the customer benefit) are the most credible form of evidence.
   - Capture partner / integration lists and ecosystem details.
   - From the leadership / Team page, capture **only the founder and current CEO** (name, title, prior employers, years in role) — feed into Step 4. Skip the rest of the team.
   - Read blog / newsroom for the **last 12 months** (scroll back month-by-month) to detect product launches, customer wins, partnerships, sunsets, repositioning, guidance changes, and restructuring.
   - For non-English companies, **read the native-language site first** (e.g. `company.com.cn`, `company.co.jp`, `company.kr`) — English IR pages are often a stripped subset and miss SKUs, regional details, and business-model nuance. After native-language sweep, check the English version for any differences.
   - **Verify product definitions match the company's own language.** If the company calls it "AI-accelerated inference appliance," do not paraphrase it as "AI inference server" or "ML hardware." Use their exact terminology in the report.
   
2. **Regulatory filings** — use filings to fill gaps not covered by the website and to verify/deepen website claims. Start from the local cache pulled in Step 0; only fetch fresh if the cache is stale (see freshness rules above). Route by domicile per the data-sources table. Note filing dates and the portal used. **When citing filing content, quote the original text verbatim** rather than synthesizing or paraphrasing.
   - For product details: 10-K / 年度报告 / Yuho Business sections go deeper on customer concentration, segment-revenue splits, product-line transitions, and legal disclosures the marketing site omits. **Quote the company's own product descriptions from the filing** (these are the official legal definitions).
   - For financials: filings are the definitive source (10-K GAAP financials are audited; website summary numbers are sometimes rounded or simplified). Pull revenue, margin, EPS, customer concentration figures **directly from the MD&A or financial statements**, not from the website's summary.
   - For risk: 10-K / 年度报告 / Yuho risk-factor sections are required reading; they detail legal, competitive, supply-chain, and macro risks the website downplays. **Quote risk factors verbatim** from the filing.
   
3. **Earnings materials and investor presentations** — see [`references/ir_materials.md`](references/ir_materials.md) for the full collection bar. **At minimum, pull every one of the following that exists; if any is missing, note it in the verification log:**
   - **Latest 2 quarterly earnings call transcripts** (most-recent first).
   - **Latest 2 quarterly earnings decks** (PDF slides accompanying each earnings call — 8-K Exhibit 99.2 for US issuers, IR site for others).
   - **Most recent annual investor day / capital markets day deck**, plus the prior one if within the last 3 years.
   - **All industry-conference presentations from the last 12 months** (JPM Healthcare, SEMICON, OFC, BofA Industrials, Goldman Communacopia, Morgan Stanley TMT, Citi Tech, etc. — whatever fits the issuer's sector).
   - **Latest annual integrated / sustainability / ESG report** if the issuer publishes one (especially Japanese / European / Korean issuers — these often contain TAM and segment narratives the formal filing skips).
   - **Latest Mid-term Plan / 中期経営計画 / Long-Range Plan** (Japan, Korea, Europe — typically refreshed every 3–5 years).
   - **IPO prospectus / S-1 / 招股说明书** if IPO was within the last ~5–10 years.
   - **Last 12 months of press releases** — scan for new product launches, customer wins, capacity announcements, M&A.
   - **Specifically look for any change to full-year guidance** (raised / cut / reaffirmed-with-color / initiated) — capture old range, new range, disclosure date, and stated driver. If a change exists, it goes in the top-of-report banner described in `references/report_structure.md` (before the TOC), not buried in Section 1. For Chinese issuers, also check 业绩预告 / 业绩快报 — these often pre-announce a guidance change before the formal 半年度 / 年度报告.
   - **Pull in the institute-research notes surfaced in Step 0.7** (`db/zsxq.db`) — the broker view of guidance, estimates, channel checks, and the bear case. Keep them clearly separate from the company's own IR materials above: IR decks/transcripts are primary (cite as fact); zsxq broker notes are sell-side (`*Analyst view:*`, cite to `/zsxq/pdf/<file_id>/<filename>`). See § "Local institute-research library".
4. **Document basic facts** — founding date, HQ, employees, products/services, key customers.

### Step 2 — Valuation, forward estimates & price target

Two parts: (2a) the backward-looking TTM snapshot — where the market prices the stock today; and (2b) the forward-looking decision layer — a multi-year estimates table, a derived 12-month price target, bull/base/bear scenarios, and a consensus benchmark. Part 2a feeds Section 1; part 2b feeds the new "Valuation & Price Target" chapter and the top-of-report investment-summary header. **The entire forward layer is the analyst's own view — every projected number, the PT, and the scenario PTs are labeled `*Analyst view:*` / `*分析师观点：*` and are NEVER attached to a filing citation** (a 10-K contains no price target; see § "Specific failure mode: do NOT misattribute sell-side opinions to filings").

#### Step 2a — Valuation snapshot (always pull P/E and P/S)

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

#### Step 2b — Forward estimates, price target & scenarios (the decision layer)

This is what turns a profile into a decision note — see § "Learning from sell-side institutional research". Build it from the segment data in the filings (Step 0–1) + management guidance + an industry forecast; the zsxq broker notes from Step 0.7 give the Street's own estimates, PT, and bull/bear to benchmark against.

1. **Forward financial-estimates table — project 3 years out** (5 if the model supports it): revenue, gross margin, operating-or-net margin, EPS, per year, with YoY growth. Each projected cell is labeled `*Analyst view:*`; cite each driver's external basis inline (filing segment data + guidance range + an industry-forecast number) — **never `(Source: our model)`**. Model the **segment mix shift** (each line its own path + margin trajectory, then summed) rather than a single blended top-line; tie each margin move to its driver (mix / operating leverage / pricing).
2. **Derive the 12-month price target and show the arithmetic.** Pick the method that fits the business and state it explicitly:
   - **Forward-PE × target multiple** (most names): e.g. `2027E EPS × <target>x = <PT>`. **Justify the multiple against 3–5 named comps** (the JPM Yingliu-40x-vs-Howmet-37x move) — a multiple with no comp justification is not a derivation.
   - **DCF** (stable cash generators): WACC = Rf + β × ERP, where **Rf is the 10Y from `indicators.db`** (reuse the Section-10 wiring; state the as-of date — cite the snapshot per the canonical plain-text form in § "Investor-lens scorecards": never a filing URL, never localhost) and ERP is stated; terminal growth ≤ Rf.
   - **SOTP** (multi-segment / conglomerates): value each segment on its own multiple, then sum.
   - **rNPV** (biotech / binary pipelines): risk-adjust each asset's peak-sales by an explicit probability-of-success; state the PTS.
3. **Bull / base / bear price targets**, each tied to its swing assumption (base = central estimates; bull = faster attach / penetration or higher multiple; bear = price war / margin compression), with upside / downside % on each. All three `*Analyst view:*`.
4. **Consensus benchmark.** Where the zsxq library (or another sourced note) carries Street estimates / a consensus PT, state where the report's forward numbers sit vs consensus (above / below, by how much) — the UBS / Nomura "+16% vs Street" move. Source the consensus figure to the zsxq note (`*Analyst view:*`, `/zsxq/pdf/<file_id>/<filename>`) or a dated public source; **never invent a consensus number.**
5. **Name the 1–2 swing variables** the call hinges on, so the reader knows which assumption to pressure-test.

These five outputs populate the new **Section 2 "Valuation & Price Target" chapter** and the **top-of-report investment-summary header** (rating + PT + upside%). See `references/report_structure.md` § "Investment summary header" and the Section-2 spec for the table template and scenario block.

#### Step 2c — GF Score (GuruFocus-style) fundamental scorecard

With the financials (Step 1–2a), the forward model (Step 2b), and the header's relative-performance line in hand, you now have every input for the **Section 1B GF Score**. Score the five axes **0–10** from the metrics you've already cited, compute the **0–100 composite**, render the radar, and write the per-axis rationale:

1. **Score the five axes** per the 0–10 anchors in [`reference/gf_score.md`](reference/gf_score.md): **Financial Strength** (cash/debt, Net Debt/EBITDA, interest coverage, Z-Score — from the balance sheet), **Profitability** (operating/net margin, ROE, ROIC vs WACC, consistency — from the income statement), **Growth** (3/5-yr revenue & EPS CAGR + the Step-2b forward estimate), **GF Value** (forward P/E vs own history + peers, PEG, MoS vs the 1A intrinsic range — *higher = cheaper*), **Momentum** (6/12-month return absolute + vs benchmark, vs 200dma — from the header relative-performance line).
2. **Render the radar + table** with the helper (paste the `<svg>` un-fenced so it renders):
   ```bash
   cd /Users/x/projects/financial_agent
   /opt/anaconda3/bin/python3 scripts/gf_score.py \
     --name <TICKER> --scores <fs>,<prof>,<growth>,<value>,<mom> \
     --source "<TICKER> FY<NN> 10-K · Yahoo Finance · indicators.db, as of YYYY-MM-DD"
   ```
3. **Write the per-axis rationale** — one paragraph per axis stating WHY that score, naming the 2–4 driving metrics with their inline citations (re-use the citations from Step 1–2). The sub-scores and composite are `*Analyst view:*`; never attach a filing citation to a score, and never attribute the number to GuruFocus unless you pulled their published figure from `gurufocus.com/term/gf-score/<TICKER>` (then show it separately).
4. **Keep it consistent** with the rest of the report — Growth ↔ the 1A forward model, GF Value ↔ the 1A multiples + PT upside, Momentum ↔ the header relative-performance line. A GF Score that contradicts the report's own numbers is a defect.

Skip only if the user said "skip the GF Score". Total time: ~5–10 minutes (the inputs are already gathered). Full rubric, weights, bands, multi-company overlay, and guardrails: [`reference/gf_score.md`](reference/gf_score.md).

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

**NEVER mix segment-level customer concentration with consolidated / group-level customer concentration. Failure mode that has bitten this skill more than once:** Samsung Electronics' 2024 사업보고서 (Business Report p. 30) discloses the consolidated top-5 customers as **Apple, Deutsche Telekom, Hong Kong Techtronics, Supreme Electronics, Verizon** with the five together at **~14% of total sales** — no individual customer's percentage broken out. Separately, Samsung supplies >60% of Google's HBM (via Broadcom) for TPUs — but that's a within-segment figure for DS Memory & HBM, *not* a group-level Google share. An earlier draft of the Samsung report mixed these into a single fabricated paragraph claiming "top-5 = Apple + NVIDIA + GOOG + MSFT + AWS = 35–45% of consolidated revenue" — off by 2–3× on aggregate, wrong on composition, and complete fiction at the >10%-single-customer level. **Rule, no exceptions:**

1. **Every customer-share number in the report must be labelled with its denominator.** Either "X% of consolidated revenue" (group-level) or "X% of <Segment> segment revenue" (segment-level) — never an unqualified "X% of revenue" when more than one denominator could apply. Tables and bullets that list customer shares must put the denominator in the column header / bullet label, not buried in a footnote.
2. **Segment-level customer lists must carry a "(segment-level; not aggregated to group-level)" qualifier** in the section that lists them — both in prose and in any chart legend / table title. A reader scanning the bullets must see at a glance that "NVIDIA / Google / AWS / Microsoft are top customers of *DS Memory*" is not the same statement as "they are top-5 of *Samsung Electronics consolidated*".
3. **Pie charts of customer concentration must use only ONE denominator per chart.** A pie that mixes "Apple 18% (consolidated)" + "NVIDIA 22% (DS Memory share)" + "Samsung Mobile 12% (intra-group)" + "Other 48%" is meaningless arithmetic — slices don't share a denominator and can't sum to 100% of anything real. If you want to show segment customer mix and group customer mix, draw two separate charts, each with its own denominator stated in the title.
4. **A top-5 customer disclosure overrides any reconstructed estimate.** When the filing names the consolidated top-5 (Samsung's 사업보고서 lists five alphabetically with ~14% in aggregate; A-share 年报 reports `前五名客户合计销售金额` exactly), that is the answer — do not append a sell-side / supply-chain composite that disagrees, do not extrapolate a different top-5 from segment-level customer reasoning. If a segment-level customer (e.g. NVIDIA in DS Memory) does NOT appear in the consolidated top-5, the correct interpretation is "that segment is too small relative to other divisions for its top customer to elevate to group-level top-5" — not "the filing's top-5 must be incomplete".
5. **The non-naming of individual customer percentages is itself a disclosure fact.** Korean 사업보고서 commonly list major customers alphabetically without ranking; Japanese Yuho sometimes name customers but not their %; A-share 年报 give the aggregate top-5 % but rarely the per-customer split. When the filing does not give a per-customer %, the report MUST say so explicitly — never fill in a per-customer percentage from supply-chain inference and label it as if it were primary.
6. **Paragraph-level inline citation applies to every customer figure.** Citing the source once in a Section 4 table or in the references block does NOT cover a Section 5 paragraph that re-states the number. Each paragraph that says "X% of revenue from customer Y" or "Samsung supplies >60% of Google's HBM" needs an inline link to the primary source *in that paragraph*, even if the same URL appears five other places in the report. (See [`citations.md`](reference/citations.md) and the project-wide Numerical Accuracy rule in `/Users/x/projects/financial_agent/CLAUDE.md`.)

Before saving Section 5, spot-check: pick three customer-share numbers in the section and confirm each one (a) has its denominator labelled, (b) has an inline citation, (c) is not silently mixing segment- and group-level figures in the same chart / bullet / paragraph.

### Step 4 — Management research

**Cover the founder and the current CEO only — nothing else.** Skip CFO, other executives, governance footer, and track-record synthesis. The management chapter should be short and focused.

- **Founder (200–300 words).** Pull from LinkedIn, DEF 14A / proxy, press interviews, podcasts, shareholder letters. Capture prior 2–3 roles with *what they specifically accomplished* (numbers not titles), education, founding thesis, ownership stake today, and whether still operationally involved.
- **Current CEO (200–300 words).** Same depth: prior 2–3 roles with concrete accomplishments, education, tenure at this company, ownership stake, comp structure.
- **If founder is still CEO, write one combined bio (300–450 words)** — don't split into two.
- **When rewriting an existing report**, also scrub *every* other named executive — CFO, segment presidents, CTO, COO, board chair, independent directors, former CEOs, IR contacts, anyone quoted in a press release — from Section 3 *and* from anywhere else they may have leaked into (Section 1 quotes, Section 2 timeline, Section 5/8 attributions, the verification log). Do not preserve them with a "trimmed" note or a "see prior draft" pointer; just delete the names. Past CEOs may stay only as anonymized historical context (e.g. "the company's late-1970s pivot from chemicals to equipment"), never as a name + tenure pairing. After rewriting, `grep` the report for any non-CEO / non-founder personal names to confirm.

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

### Step 8 — Charts and diagrams (financial-statement SVG + Mermaid)

A report this length needs visual anchors, from two complementary, **memory-safe** systems — never matplotlib:

**(A) Financial-statement visuals — `scripts/financial_charts.py` (inline SVG).** The stockanalysis.com-style charts a reader expects of a financials section: an **income-statement Sankey** (revenue → COGS / gross profit → opex / operating income → tax / net income), **balance-sheet** and **cash-flow Sankeys**, a revenue **donut** (by segment / by geography), **historical stacked revenue bars**, and a **5-step DuPont** ROE tree. Like `scripts/gf_score.py`, it is **stdlib-only** (imports just `math` / `argparse`, ~0 MB resident) and emits raw `<svg>` that the viewer renders verbatim (`reports_viewer.py` → `marked.js`, no sanitization). **Every number you pass must come from the company's OWN 10-K / 10-Q / 20-F / 年度报告 / IR deck that you read and cite** — the income statement, balance sheet, cash-flow statement, and the segment note (ASC 280 / IFRS 8). The required `--source` is baked into the image; the surrounding paragraph still carries the page-level citation. **Read [`references/financial_charts.md`](references/financial_charts.md) before using it** — it has the per-subcommand CLI, the worked ISRG examples, placement, and the sourcing guardrails. **Always generate the full suite by default — income-statement Sankey, balance-sheet Sankey, cash-flow Sankey, a revenue donut by segment AND a second donut by geography, historical revbars, and the 5-step DuPont tree.** Drop a chart ONLY when the underlying statement / disclosure genuinely doesn't exist (e.g. a private company with no balance sheet, or a single-segment issuer with no geography split) — and when you drop one, say which and why in the Step 10 verification log. "By company fit" is **no longer** a license to ship just the income Sankey + one donut; that minimalist output is a defect for any issuer that files full statements.

**(C) Money-flow (supply-chain) diagram — `scripts/financial_charts.py moneyflow` (inline SVG) — REQUIRED, one per report.** The 3-stage "follow the dollars" map (who pays → what they buy → where the money pools) the user singled out as "very intuitive" — it shows where the company's COGS / capex *lands* (suppliers, and their suppliers — the chokepoints), which the statement Sankeys can't. Same stdlib-only inline-SVG engine, JSON-spec-driven, self-contained dark theme. **NOT flow-conserving** — thickness is rough relative scale (the baked-in legend says so). Pick the orientation that fits (upstream/spend for buyers & integrators; demand/revenue for suppliers & component makers); **solid** ribbon = paid directly, **dashed** = embedded in a finished part bought from someone else. **Every node must be a real, sourced counterpart** (named supplier/customer from filings / IR / teardown-channel reports / the zsxq library — never invented); any `$` in a ribbon label must string-match a cited source. Add a **"Follow the money" card grid** (`cards` in the spec) — 4–6 short thesis cards that render *inside the same SVG* beneath the flow, each summarizing one ribbon theme, with key numbers/names wrapped in `*asterisks*` to render in gold (the reference's signature). **Read [`references/money_flow.md`](references/money_flow.md) before generating it** — full JSON spec (nodes / flows / cards), `kind` palette, two orientations, worked Tesla/SpaceX example, placement (Section 4 or 6), and sourcing guardrails. Build the spec, render to a temp file, paste the `<svg>` un-fenced with a caption + a short sourced "follow the money" paragraph (the in-image cards can't hold clickable links, so the prose carries the citations). Drop it ONLY when the value chain genuinely can't be sourced — say so in the Step-10 log.

**(B) Mermaid diagrams (markdown-native).** For the diagram types Mermaid does well — `timeline` (history), `graph TD` (product-portfolio tree, org chart), `quadrantChart` (competitive positioning), and simple `xychart-beta` trends. Mermaid is markdown-native: the viewer at `http://xs-macbook-air.local:5001/claude-reports/` and GitHub render it inline at view time. **Aim for 5–9 visuals total across (A) + (B) + (C).**

**Do NOT generate matplotlib PNG charts.** This was disabled project-wide on 2026-06-03 to cut per-agent memory footprint — every `import matplotlib.pyplot` + `savefig` held ~150-300 MB resident, and with 4-6 concurrent `/company-research` agents the cumulative load pushed the system past 90 GB and triggered OOM kills. The **only** sanctioned chart paths are (A) the stdlib-SVG helpers (`financial_charts.py`, `gf_score.py`) and (B) Mermaid — both add ~0 MB. No exceptions; do not regress to matplotlib.

**`xychart-beta` has ONE y-axis — never mix units on it.** Do NOT plot a % series and a currency series on the same chart: the % line renders on the currency scale and reads as a money amount (a 19.5% operating-margin line on a `0 --> 30` US$bn axis reads as $19.5bn; a 70.9% gross-margin line on a `0 --> 300` ¥mn axis reads as ¥70.9M). The default fix is **two stacked `xychart-beta` blocks** — revenue bars in one, the margin line in its own chart with a % axis. If a combo is truly unavoidable, the caption MUST state the line's unit and that it shares the numeric scale — but split charts are the rule, the caption rescue is the exception.

(Legacy chart PNGs in `reports/charts/` from before 2026-06-03 remain on disk and may be reused in the report via `![](charts/<file>.png)` markdown — do not delete them or regenerate them as Mermaid for old reports. The rule applies only to NEW chart generation going forward.)

**Mermaid block types — pick the right one per use case:**

- **Trend / time-series** (Section 1 revenue + margin as TWO stacked charts, Section 2 valuation history, Section 8 TAM growth, latest 8–12 quarter print): `xychart-beta` — supports `line` and `bar`, multi-series, axis labels, customizable y-range; single y-axis only (see the unit-mixing rule above). Wrap in ` ```mermaid` fence.
- **Timeline** (Section 2 History): `timeline` block — founding → IPO → segment launches → recent milestones.
- **Product portfolio tree** (Section 4 Products): `graph TD` mapping company → segments → product families → SKUs.
- **Customer concentration** (Section 5): `pie title FY2024 revenue by top customers` with the top 3–5 customers + "All other". Use ONE denominator per pie (consolidated vs segment-level — never mix).
- **Peer-comparison bars** (Section 7, Section 2 valuation): `xychart-beta` with peers on x-axis, multiple metrics (TTM P/E, P/S, EV/EBITDA) as bars.
- **Competitive positioning** (Section 7): `quadrantChart` (2×2) on price vs. feature-breadth, or `graph LR` for value-chain position.
- **Org / governance** (Section 3, optional): `graph TD` for board / management reporting lines.

**Placement summary** (echoed in `references/report_structure.md`). **SVG** = `financial_charts.py`; **MM** = Mermaid:
| Section | Visual |
|---|---|
| 1 Overview | **SVG** income-statement Sankey (`income`) — the "how it makes money" anchor; **SVG** revenue `donut` (by segment) + `revbars` (history); **MM** `xychart-beta` revenue trend + a separate gross-margin chart (two stacked blocks — never % and currency on one axis) |
| 1B GF Score | **SVG** `gf_score.py` radar (see Step 2c) |
| 2 Valuation | **SVG** `dupont` ROE tree (return decomposition); peer-multiple `xychart-beta` bars |
| 2 History | **MM** `timeline` block — founding → milestones |
| 4 Products | **SVG** `moneyflow` supply-chain money-flow map **(always — one per report)** — who pays → what they buy → where the money pools (or place in Section 6 if the chain is more an industry story); **MM** `graph TD` product portfolio tree (the 10-K product *table* screenshot via `render_10k_section.py` is optional; markdown reproduction of the table is mandatory regardless) |
| 5 Customers | **SVG** revenue `donut` (by geography); **MM** `pie` — top-3-5 customer concentration (one denominator per chart) |
| 7 Competitive | **MM** `quadrantChart` **or** `xychart-beta` peer-comp bars |
| 8 TAM | **MM** `xychart-beta` market-size growth |
| 8 / 9 Capital allocation & structure | **SVG** cash-flow (`cashflow`) Sankey **(always)** — OCF → capex / FCF / dividends / buybacks / debt; **SVG** balance-sheet (`balance`) Sankey **(always)** — assets vs liabilities + equity |

**Every chart gets a citation right below it** — same markdown-link format as prose, e.g. `Source: [安培龙 2024 年度报告, 第 32 页](https://static.cninfo.com.cn/...)`. No chart without a source.

### Step 9 — Synthesis and writing (Chinese by default; English only on explicit request)

**Default: write ONE complete Simplified Chinese (zh-CN) report.** Only produce an English report if the user explicitly opted in (`in English`, `English only`, `bilingual`, `also in English`, etc. — see the override table in the "Report language" section). When bilingual mode is on, write two complete independent reports — one Chinese, one English.

Read `references/report_structure.md` for the 9-section spec and full output template. Read `reference/citations.md` before drafting — inline citations are required in every section, not just at the end.

**Open with the decision layer, then the descriptive sections (BLUF — see § "Learning from sell-side institutional research").** Lead with the **investment-summary header** (rating + 12-month PT + upside% + valuation one-liner + 2–4 thesis pillars, all `*Analyst view:*`), then a thesis-first lead paragraph in Section 1 (the call + why-now + pillars) before the "what the company does" prose. The forward-estimates table, the PT derivation, and the bull/base/bear scenarios from Step 2b go in the **Section 2 "Valuation & Price Target"** chapter; the bear-vs-thesis rebuttals and dated catalysts go in the **Section 9.5 "Key debates & catalysts"** block. Keep all 9 descriptive sections intact — they feed the thesis; the decision layer sits on top of them, it does not replace them.

**Language-specific instructions:**

- **Chinese report (default and primary)** — full prose in Simplified Chinese (zh-CN). Write as if for Chinese investors. Section headers in Chinese (公司概览, 产品与服务, etc.). **Bilingual technical terms are MANDATORY** per the rule in the "Report language" section above: financial metrics, industry terms, regulatory bodies, product names, ratings, and indices keep the English form alongside the Chinese gloss on first mention (e.g. `gross margin (毛利率)`, `gate-all-around / GAA (栅极环绕)`, `MIIT (工信部)`), and product names / index names / rating labels stay in English throughout (e.g. `H200`, `S&P 500`, `Buy/Hold/Sell`).
- **English report (opt-in only)** — full prose per the spec in `report_structure.md`. Standard business English, accessible to global equity investors. Preserve original-language titles for non-English companies / citations (e.g., `华为 Huawei`, `2024 年度报告`, `統合報告書`). Bilingual technical terms where helpful (e.g., `advanced packaging (先进封装)`, `design-rule check (DRC, 规则检查)`), but bilingualism is optional in English prose — what matters is clarity for English readers.

In bilingual mode, both reports share the same underlying data, charts, citations — but each is written natively in its own language and grammar, not a literal translation of the other. A Chinese reader should find the Chinese report as natural and fluent as an English reader finds the English report.

### Step 9.5 — Apply investor-lens scorecards (optional Section 10)

After Sections 1–9 are drafted but before Step 10 verification, compute the scorecards described in [`references/investor_lenses.md`](references/investor_lenses.md). Workflow:

1. **Pick the lens set.** Default = the four core lenses (10.1–10.4). Add optional lenses (10.5–10.9) when the company fits them per the routing table in `investor_lenses.md` § "Implementation tips" — Lynch for mid-cap GARP candidates; Fisher for compounders with scuttlebutt evidence; Burry for hated-sector contrarian setups; Druckenmiller for macro-liquidity-sensitive names; Cathie Wood for disruption stories. **When in doubt, stick with the core four.**
2. **Pull the cycle snapshot once.** Query `indicators.db` (or call `indicators/data_fetcher.fetch_all()`) for VIX, 10Y Treasury (`^TNX`), HY OAS (FRED `BAMLH0A0HYM2`), IG OAS (FRED `BAMLC0A0CM`). State the as-of date and use this snapshot across every included lens.
3. **Compute 10.4 (Howard Marks cycle) first.** It gates the verdicts above and 10.8 Druckenmiller — a defensive regime should mute "Bullish" verdicts in 10.1, 10.2, 10.3, 10.8; call out the disagreement explicitly rather than forcing consensus.
4. **Compute the remaining included lenses** from the data already cited in Sections 1–9 — re-use existing inline citations rather than introducing new ones. If a required input is missing from earlier sections, the fix is to go back and gather it there, not one-shot-cite it inside Section 10.
5. **Write each subsection in the lens's verdict-first shape:** bolded verdict line → 3–5 row scorecard table → 2–3 sentence evidence chain reusing earlier citations → required-block per-lens (Damodaran assumptions, Munger inversion, Lynch category, Fisher scuttlebutt note, Burry downside-first, Druckenmiller macro context + exit trigger, Cathie Wood Wright's Law math + convergence note) → one-sentence failure mode.
6. **Re-use the same Section 10 in both languages.** Same scorecards, same numbers, natively-written prose in each language; the verdict labels translate (`*Lens view:*` ↔ `*视角观点:*`).

Skip this step if the user said `no lens scorecards` / `skip Section 10` / similar. Total time: ~15 minutes for the four core; +5 minutes per optional lens added.

### Step 10 — Verification pass (mandatory for BOTH languages before declaring done)

**A report that has not been verified is not done.** The generating model has a documented pattern of:

- Fabricating SEC URLs (synthetic filenames like `2025_10K_<accession>.htm` that don't exist on EDGAR)
- Attributing analyst opinions to the 10-K ("Lam is regarded as ahead", "dominant moat", "near-monopoly share", "co-leader")
- Inventing competitor product names not present in any cited filing
- Inventing specific market-share percentages and segment-revenue splits
- Inventing executive names and management-transition details
- Shipping charts that render broken even when every number is correct — nodes drawn off-canvas, a bar taller than the viewBox, labels clipped past the edge, a degenerate single-ribbon Sankey, or a Mermaid block that throws a syntax error at view time (see 10.7)

Step 10 catches these before the report ships. **Run verification on every report file produced** (default: the Chinese report; bilingual mode: both Chinese and English). **Skip Step 10 only if the user has explicitly waived it.**

#### 10.1–10.4 — Mechanical checks (recipes in [`references/verification.md`](references/verification.md))

Run all four; the bash recipes (curl/grep one-liners) live in the reference — read it before this pass:

- **10.1 — Every URL resolves.** HTTP-check each URL; 404 must be fixed or removed; 403/406 are usually anti-bot (confirm in a browser). Local zsxq URLs are user-machine-only — verify via `find_pdf.py --file-id <id>` (`local_exists: true`), and the route must be `/zsxq/pdf/<file_id>/<filename>` (not the dead `/zsxq-pdf/` or the no-download `/zsxq/pdf-viewer/`).
- **10.2 — SEC filenames came from the EDGAR submissions JSON.** The `<filename>` is opaque — never pattern-construct it; resolve it from `https://data.sec.gov/submissions/CIK<padded>.json` (8-K exhibits via the accession `index.json`). If unresolvable, cite the filing index page, not an invented filename.
- **10.3 — 10-K-cited claims actually appear in the 10-K.** Cache the primary doc once and `grep` each cited number/fact; if it isn't there, the citation is wrong — fix or drop. Grep especially competitor lists, `approximately X%`, segment line items, restructuring/headcount, customer concentration.
- **10.4 — Executive names appear verbatim in the cited 8-K / DEF 14A.** If the name isn't in the filing, the citation is fabricated — remove or re-source.

#### 10.5 — Self-audit checklist

Before declaring done, confirm each line:

- [ ] All URLs return HTTP 200 (or known-good 301 / 302 redirect)
- [ ] All SEC URLs end in filenames pulled from the EDGAR submissions JSON
- [ ] No "dominant" / "leader" / "monopoly" / "co-leader" / "near-monopoly share" claim is attached to a 10-K citation unless the 10-K says it verbatim
- [ ] No revenue-by-sub-segment percentage (e.g. "Etch is 45% of Systems") is attached to a 10-K citation — these are analyst estimates, label them as such
- [ ] No specific competitor product name (e.g. "AMAT NOKOTA") is attached to the *subject's* 10-K — at minimum it should cite the competitor's own filing or website
- [ ] No fabricated executive names — every named exec is confirmed in an 8-K or DEF 14A
- [ ] No `(Source: our model)` / `(Source: our analysis)` / `(模型估算)` self-references
- [ ] Every `db/zsxq.db` citation is labeled `*Analyst view:*` / `*分析师观点：*`, uses the `/zsxq/pdf/<file_id>/<filename>` route (not the dead `/zsxq-pdf/` form), carries broker + date + page in the link text, and is never attached to a filing; every number quoted from a zsxq note string-matches the note's summary or OCR'd text
- [ ] **When ≥2 zsxq notes were used:** the 卖方观点演变 (Sell-side view evolution) subsection is present — `db/stock_price_target.db` read-only pre-pass ran first, per-institute timeline ordered by the filename `-YYMMDD` date with self-revisions + triggers called out, disagreement table rendered where institutes conflict (no fake consensus), every view dated + cited to its `/zsxq/pdf/<file_id>/<filename>` link (see § "卖方观点演变 (Sell-side view evolution)")
- [ ] Internal consistency: Section 1's competitive claim matches Section 7's; Section 2 timeline matches Section 1 prose; restructuring counts in narrative match the timeline
- [ ] Numbers spot-checked against the 10-K (at least: revenue, gross margin, customer concentration, geographic mix, segment %, restructuring headcount)
- [ ] Link-title ↔ URL consistency: every link whose title names a source (indicators.db, FRED, Yahoo, a broker, a filing, McKinsey/Yole/Gartner) resolves to that source's domain — scan `grep -oE '\[[^]]+\]\(http[^)]+\)' <report>.md` for titles paired with the wrong domain. A 200-OK URL that doesn't contain the claimed source/number (e.g. `[indicators.db 快照](https://www.sec.gov/...)`) is a FAIL even though the reachability check passes
- [ ] **Financial-statement charts (`financial_charts.py`):** every figure in each Sankey / donut / DuPont string-matches the cited statement; the chart is pasted **un-fenced** so it renders; the `--source` footer cites the exact statement; the surrounding paragraph carries the page-level citation; no chart contains a number not traceable to a cited filing
- [ ] **Money-flow diagram (`financial_charts.py moneyflow`):** present (one per report) and pasted **un-fenced**; every node is a real, sourced counterpart (no invented suppliers); each `$` in a ribbon label string-matches a source cited in the surrounding paragraph; the `--source` footer is present; the "follow the money" caption names the chokepoint(s) and cites each link — or, if dropped, the chain-not-sourceable reason is in the log
- [ ] **Charts RENDER, not just compute (10.7 — MANDATORY):** `lint_report_charts.py` exits 0 (no SVG node / bar / label off-canvas or overflowing its viewBox) **AND** a port-5002 browser screenshot was eyeballed — every Sankey node connected (no floating bar, no node fed by a single hair-thin ribbon), every Mermaid block rendered (no red "Syntax error" box), no clipped or overlapping labels

#### 10.6 — Append a verification log to each report

After the References section in **every report produced** (the Chinese report by default; both Chinese and English in bilingual mode), append a `<details>` block listing what was checked. This makes verification visible to the reader and forces honesty about residual unknowns. **The `<summary>` line MUST be the exact English string `Verification log (Step 10) — YYYY-MM-DD` even in Chinese reports** — project tooling greps for it; a translated summary (`验证日志…`) breaks the contract. Chinese annotation may follow inside the block body. The logs may differ slightly between languages (e.g., different filings checked) but follow the same structure. **The log must include the 10.7 chart render-check line** (`lint exit 0 + :5002 screenshot eyeballed`).

**The full log template** (URL check · Step 0.5 status · further-viewing URLs · SEC filenames · 10-K spot-checks · financial-chart figure string-matches · money-flow node/label string-matches · chart render-check (10.7) · analyst-view sentences · institute-research file_ids · residual unknowns) **lives in [`references/verification.md`](references/verification.md) § 10.6 — copy it from there.** If the log shows residual unknowns the user cares about, fix them before declaring done. Every report produced (Chinese always; English when bilingual) must be verified and signed off before final submission.

#### 10.7 — Render-check every chart (visual, not just numeric — MANDATORY)

Step 10.5's chart lines confirm the *numbers* are right; they do NOT confirm the chart *renders*. A chart can carry perfectly sourced numbers and still ship broken. This substep exists because the Black Sesame (HKEX:2533) FY2025 income Sankey shipped exactly that way: operating loss was 1.76× revenue, the `income` generator placed nodes at **negative Y** and drew a **900px bar inside a 560px viewBox**, every number string-matched the filing, and "verification" passed because **nothing rendered it**. Two gates, both required, before sign-off:

**(a) Deterministic SVG-bounds lint — run first, must exit 0.**

```bash
/opt/anaconda3/bin/python3 .claude/skills/company-research/scripts/lint_report_charts.py \
  reports/company/<Slug>/<file>.md
```

It parses every inline `<svg>` (transform-aware) and FAILS on any rect / path / line / text that renders outside its own viewBox, or any bar taller than the canvas. A non-zero exit means a chart is clipped or off-canvas — fix the generator inputs / geometry and regenerate before continuing. Run it on **every** report file produced (ZH always; EN too in bilingual mode). Mermaid blocks are reported as a count only — they render in-browser, so gate (b) covers them.

- **Known failure mode — loss-making issuers.** When operating loss / total opex exceeds revenue, `financial_charts.py income` can place nodes off-canvas. For any issuer with an operating loss, inspect the income Sankey specifically. The fix that stays on-canvas and balances: draw the **operating-loss deficit as a left-side source** that — together with gross profit and other income — funds the operating-expense pool (every node then conserves flow and the loss bar flows into R&D/SG&A instead of dangling). See the Black Sesame ZH report's income Sankey for the worked 5-column layout.

**(b) Browser screenshot — launch the local viewer on port 5002 and eyeball every chart.**

Never port 5001 (the user's live instance). Start the viewer on **5002**, open the report, screenshot it, and READ the screenshot yourself:

```
preview_start (port 5002)  →  http://localhost:5002/claude-reports/view/company/<Slug>/<file>.md
preview_screenshot         →  Read the PNG  (scroll / multiple shots for a long report)
```

Confirm, chart by chart: every Sankey node is connected (no floating bars, no node fed by a single hair-thin ribbon), ribbons land somewhere, donut/radar slices look sane, labels aren't clipped or overlapping, and **every Mermaid block rendered (no red "Syntax error" box)**. Fix the source and re-screenshot anything wrong. **Stop the server when done:** `preview_stop` + `lsof -ti :5002 | xargs kill -9`.

Record the outcome in the 10.6 log as `**Chart render-check (10.7)** — lint exit 0 (N svg / M mermaid); :5002 screenshot eyeballed, all charts render, Mermaid OK`.

---

## Output location

Save to **`reports/company/<Slug>/`** under the project root: `/Users/x/projects/financial_agent/reports/company/<Slug>/<filename>.md`. The viewer (http://xs-macbook-air.local:5001/reports) groups by this folder structure. Create the folder if missing.

**`<Slug>`** is everything that comes before `_Research_Document` / `_公司研究` / `_研究报告` in the filename — i.e. the company name plus primary ticker, joined with `_`. The filename itself is repeated inside the slug folder (one folder per company holds EN and / or ZH).

File name follows the report language — **no date suffix**:
- **MANDATORY: every filename starts with an English / pinyin name** so users can `grep` or search by either language. A filename like `中砂_TWSE1560_公司研究.md` is **wrong** — it cannot be found by searching for "Kinik". Correct: `Kinik_中砂_TWSE1560_公司研究.md`.
- **Chinese reports**: `[EnglishName]_[中文名]_[EXCHANGE][CODE]_公司研究.md`. English / pinyin is **required first**; Chinese name **optional but recommended**; ticker required.
- **English reports**: `[EnglishName]_[EXCHANGE][CODE]_Research_Document.md` (ASCII only) or `[EnglishName]_[中文名]_[EXCHANGE][CODE]_Research_Document.md` for Chinese companies.
- Never Japanese kana / kanji or Korean hangul in filenames; use Romaji / Romanization.
- **Do not append `_YYYY-MM-DD` to research-doc filenames.** Only one EN file and one ZH file exist per company, so a date in the filename adds no signal and clutters the slug folder. Put today's date inside the document as an "as of" header at the top instead; git history tracks the actual revision date.

Examples:
- `reports/company/Anpeilong_安培龙_SZSE002050/Anpeilong_安培龙_SZSE002050_公司研究.md` (A-share, Chinese report)
- `reports/company/BYD_比亚迪_HKEX1211/BYD_比亚迪_HKEX1211_公司研究.md` (HK filing in Chinese)
- `reports/company/Kinik_中砂_TWSE1560/Kinik_中砂_TWSE1560_公司研究.md` (TW, Chinese report)
- `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md` (US, English)
- `reports/company/Alibaba_HKEX9988/Alibaba_HKEX9988_Research_Document.md` (HK, English)
- `reports/company/Toyota_TSE7203/Toyota_TSE7203_Research_Document.md` (Japan, English)
- Tickerless private companies: see § "Unlisted / private companies (`reports/unlisted/`)" below.

EN and ZH versions of the same report share one slug folder — ZH adds the suffix `_zh` (preferred) or `_CN` before `.md`, e.g. `Tesla_NASDAQ_TSLA_Research_Document_zh.md`.

Other report types live in sibling folders the viewer also surfaces:
- `reports/sector/<topic>_<YYYY-MM-DD>.md` for thematic / industry overviews
- `reports/compare/<A>_vs_<B>_<YYYYMMDD>.md` for head-to-head comparisons
- `reports/earnings/<TICKER>_<YYYYMMDD>.md` for quarterly earnings notes

Always write under the main project's `reports/` directory — never to a worktree, `~/Downloads`, or any other location.

### Unlisted / private companies (`reports/unlisted/`)

The repo carries a dedicated tree for private-company research at **`reports/unlisted/`** (17+ existing folders — robotics startups, Huawei, etc.). Rules:

1. **Canonical path: `reports/unlisted/<EnglishName>_<中文名>/<EnglishName>_<中文名>_公司研究.md`** — the English / pinyin component is **mandatory and comes first**, exactly as for listed names (e.g. `LimX_逐际动力/`, `MagicAtom_魔法原子/`, `Unitree_宇树科技/`). A pure-Chinese folder name (`魔法原子/`) fails the project filename rule — it cannot be found by an English search. Legacy pure-Chinese folders exist in the tree; do not replicate the pattern for new reports.
2. **Every quality block applies identically to unlisted names:** the Chinese-only language default, the Step 10 verification log, the Data Used manifest, Further viewing, and the header rule `Rating / PT: not applicable — private` (per `report_structure.md` § "Investment summary header"). Private status waives the PT, not the verification pass.
3. **Before creating a new unlisted report, check BOTH trees case-insensitively** — `ls reports/unlisted/ reports/company/ | grep -iE "<EnglishName>|<中文名>"` — a prior report may live under either convention (e.g. `reports/company/Unitree/`); update it in place rather than duplicating.

### Update-in-place rule — exactly one research doc per company per language

Reports under `reports/` are checked into git and are meant to be living documents. **Before writing, check whether research docs for this company already exist** in `reports/company/<Slug>/`, and update them in place rather than creating parallel copies.

**Default behavior: produce ONE Chinese file** (`<Slug>_公司研究.md`). Produce an English file only when the user explicitly opted in (`in English`, `English only`, `bilingual`, `also in English`, etc.). Before starting, check for existing files — **case-insensitively, matched on the ticker**, because folder casing is inconsistent in this repo (e.g. the XPeng report lives at `Xpeng_NYSE_XPEV/`, not `XPeng_…`) and a case-sensitive `<Slug>` path will miss a real hit and trigger a wasteful regeneration:

```bash
# First find the slug folder by ticker (case-insensitive), then list inside it.
ls reports/company/ | grep -iE "<Ticker>"                       # e.g. grep -iE "XPEV"
ls "reports/company/<exact-folder-printed-above>/" 2>/dev/null \
  | grep -iE "_Research_Document(_zh|_CN)?\.md|_公司研究(_zh|_CN)?\.md"
```

Note the Chinese edition may be named `<Slug>_公司研究.md` (this skill's default) **or** `<Slug>_Research_Document_zh.md` (English-template name + `_zh`); the `grep -iE` above matches both. Match on the ticker, not the naming convention.

For **each language you're generating** (Chinese by default; Chinese + English when bilingual mode is on):

- **Exactly one existing match for this language** → overwrite it at the same path. Update the document's internal "as of" date header to today; git history records the actual revision dates.
- **Multiple matches for the same language** (legacy state — old dated copies from before this rule) → consolidate into the canonical no-date filename (`<Slug>_公司研究.md` for ZH, `<Slug>_Research_Document.md` for EN), updating the most recent one and listing the older duplicates so the user can confirm deletion. Do not auto-delete.
- **Zero matches** → create a new file at the canonical no-date path. Do **not** add a `_YYYY-MM-DD` suffix to the filename.

**An existing English-language file from a prior run is NOT a trigger to refresh it.** If the user asks for "research X" today (no English opt-in), produce / refresh only the Chinese file — leave any pre-existing English file untouched, unless the user explicitly says `also refresh English` / `update bilingual` / `also in English`. Print the final path of every file produced so the user can confirm whether each was an update or a fresh create.

**Retrofit clause — every touch of a vintage report triggers a block-presence audit.** Whenever an existing report file is opened for editing for ANY reason (refresh, link fix, citation backfill, mechanical route rewrite), run a 60-second presence check against the current mandatory-block list — investment-summary header (incl. forward valuation matrix + relative-performance line), Section 1A decision layer, Section 9.5 debates & catalysts, Data Used manifest, verification log, Further viewing — and either retrofit the missing blocks in the same pass or append a `**Spec gaps (vintage <date>):**` line to the verification log naming them. Reports written under older spec vintages must not keep circulating with invisible gaps just because the editing pass was mechanical.
