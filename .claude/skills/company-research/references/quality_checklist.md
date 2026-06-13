# Quality Standards & Success Criteria

## Content Depth
- Each section meets its minimum word-count target (see `report_structure.md`).
- Analysis is substantive, not just descriptive.
- Specific examples and quantitative data, not generic statements.
- Sources cited **inline at the paragraph level** — every substantive paragraph carries at least one inline markdown-link citation, not just one per section (see `citations.md`).
- **Pre-submit citation count check:** `grep -oE '\[[^]]+\]\(http[^)]+\)' <report>.md | wc -l` should yield ≥40 for a 6,000–10,000 word report. Reports below the threshold have unsourced paragraphs — find and cite them before submitting.
- Objectivity and balance.

## Investor-relations coverage (separate from the ≥40 inline-citation bar)

IR materials are first-class primary sources — see SKILL.md § "Investor presentations are first-class primary sources" and citations.md § "Investor-relations materials — slide-level citation discipline" for the full rules.

- [ ] **At least 8–12 distinct IR-material citations** across the body when the company has a public IR program. Count via `grep -oE '\[[^]]*(deck|Slide|earnings deck|Investor Day|investor day|統合報告書|Integrated Report|Mid-term Plan|中期経営計画|业绩说明会|投资者关系活动|招股说明书|Shareholder Letter|Earnings Presentation|说明会 PPT)[^]]*\]\(http' <report>.md | wc -l`. Reports under 8 IR citations have under-used IR materials — go back and find the right slides.
- [ ] **Section 1, 4, 6, 8 each contain at least 1 IR citation** when slides exist that cover that ground. Section 8 typically contains the heaviest IR citation density (2+) because the TAM build slide is the most-cited single source.
- [ ] **Latest 2 quarterly earnings decks AND the latest investor-day deck** are each cited at least once. If only 1 of the 3 is cited, that's under-use.
- [ ] **For Japanese / Korean / European issuers with an Integrated Report or Mid-term Plan**, that document generated 5+ citations on its own (TAM, segment KPIs, capex plan, ESG, geographic strategy).
- [ ] **Every IR citation is slide-level / page-level, not deck-level.** Format check: `grep -E '\[[^]]*(deck|Investor Day|統合報告書|Mid-term Plan)[^]]*\]\(' <report>.md | grep -vE '(Slide|p\.|第 [0-9]+ 页|, p [0-9])'` should return no lines.
- [ ] **TAM citations sourced from IR decks use chain labels** (`citing Yole/Gartner/IDC`) — the click lands on the company's own slide, not the research firm's homepage.
- [ ] If the company has no public IR materials, the verification log explicitly states "no public IR program; relied on filings + third-party research" — absence is logged, not hidden.

## Institute-research (local zsxq) coverage

Local sell-side notes from `db/zsxq.db` are the project's first stop for the analyst view — see SKILL.md § "Local institute-research library" and § "Source hierarchy". This bar is separate from the IR bar above (IR = company's own materials, primary; zsxq = broker notes, sell-side).

- [ ] **At least 3–6 distinct `db/zsxq.db` citations** across the body when the name has local coverage (a US large-cap like NVDA will have dozens of candidate notes — zero is not acceptable). Count via `grep -oE '\[[^]]+\]\(http://[^)]*zsxq/pdf/[0-9]+[^)]*\)' <report>.md | wc -l`.
- [ ] **At least 1 zsxq citation in Section 2** (the PT / consensus / valuation-basis line) and **1 in Section 9** (the bear case in the analyst's own words).
- [ ] **Every zsxq citation is labeled `*Analyst view:*` / `*分析师观点：*`**, uses the `/zsxq/pdf/<file_id>/<filename>` route (not the dead `/zsxq-pdf/` form), carries broker + date + page in the link text, and is never attached to a filing. Format check: `grep -nE '/zsxq-pdf/' <report>.md` should return no lines.
- [ ] **Every number quoted from a zsxq note string-matches** the OCR'd / extracted original PDF text (not just the 翻译精华 summary).
- [ ] **Every borrowed broker PT is paired with the stock's price on the note's date + the implied upside** (`目标价 $288（较 2026-06-03 收盘 $232 上行 +24%）`) — sourced from `stock_price_target_db` (`report_date_price` / `upside_pct`, shown at `/pt`) or a yfinance close on the note's date. A bare borrowed PT with no report-date price is a fail. `report-date price n/a` is acceptable only when yfinance has no close for that date; today's spot is never a substitute.
- [ ] If the library genuinely has nothing on the name even after a `--query` top-up, the verification log says so explicitly — absence is logged, not hidden.

## Management Bios
- **Cover the founder and the current CEO only — nothing else.** No CFO, no other executives, no governance footer, no track-record synthesis.
- Founder bio: 200–300 words. Current CEO bio: 200–300 words. If founder is still CEO, write one combined bio (300–450 words).
- Each bio includes current role, prior 2–3 roles with *what specifically they accomplished* (numbers, not titles), education, tenure, ownership stake.

## Competitive Analysis
- 5–10 specific competitors analyzed.
- Both direct and indirect competitors.
- Relative positioning on key dimensions assessed.
- Company's competitive advantages and vulnerabilities identified.
- Specific data and examples, not generalities.

## Products & Services — the most important section (highest priority)

**Section 4 carries more weight than any other section.** It is the analytical foundation for Sections 5–9; if it is generic or fabricated, the rest of the report is hand-waving. A report that under-invests here cannot be recovered by polishing the other chapters. See SKILL.md § "The Products & Services chapter is the most important section of the report" for the full rationale and the precise + explanatory criteria.

**Precision checks (must pass):**
- The issuer's own product table is **reproduced verbatim as a markdown table** at the top of Section 4 with the 10-K citation directly above it (searchable, linkable). This is mandatory.
- *Optionally*, the original rendered table is also embedded as a PNG (via `.claude/skills/company-research/scripts/render_10k_section.py`, caption citing the 10-K) when visual proof adds value — the PNG never substitutes for the markdown reproduction.
- For each row in the matrix, the issuer's own product-family description is **block-quoted verbatim** from the 10-K / 年度报告 / Yuho with the inline citation directly above the quote.
- Every product name spelled exactly as the issuer spells it, including ® / ™ marks and platform-name prefixes (`ALTUS®`, `Sense.i®`, not `Altus` / `Sense-i`).
- Every technical specification (depth, speed, resistance, layer count, throughput) comes verbatim from the issuer's filing or press release, with a citation. No invented numbers.
- Competitor product names cite the competitor's own filing / website — never the subject's 10-K.
- "Dominant" / "leader" / "co-leader" / "near-monopoly share" claims are labeled `*Analyst view:*` and cite an industry-research source (Yole, Gartner, IDC) or stand uncited. They never carry a 10-K citation.
- Revenue-by-sub-product-category percentages (e.g. "Etch is ~45% of Systems revenue") labeled `(analyst estimate)` unless the company publishes the split.

**Explanation checks (must pass):**
- For each material product family, three pedagogical beats present:
  1. **What it physically does** in the customer's value-chain flow (concrete physical role, not marketing prose);
  2. **How it differs from sibling products** in the same matrix (explicit cross-reference);
  3. **Strategic significance** (which technology inflection / customer wave is driving demand).
- For technical concepts, **bilingual terminology** in `Chinese / English` form (introduced with `**中文释义 / Plain-language gloss:**`). Code-switching within sentences is encouraged for cross-border-investing audiences.
- **Synthesis paragraph at the end** showing how the product categories compose a single customer workflow (e.g. Deposition → Etch → Clean → Deposition for semicap; discovery → preclinical → clinical → marketed for pharma). Optional small Mermaid graph showing the loop.
- Per-product **competitive-advantage verdict** (yes / partial / no) plus moat type — under the `*Analyst view:*` label.
- **Flagship 1–3 products** clearly distinguished from long-tail.
- **Last-12-month launches / sunsets** noted, each cited to a real press release URL.
- **延伸观看 / Further viewing slot present** — 1–3 explainer-video links in their own `**延伸观看 / Further viewing**` block (Section 4 default), each HTTP-checked 200 with a real-browser UA, none carrying a number or entering the citation chain — OR the verification log states why the report has nothing worth visualizing.
- Section 4 word count is in the upper half of section ranges (≥1,000 words) — *if Section 6 is longer than Section 4, the priority is wrong*; cut Section 6 and expand Section 4.

## Company Overview — Valuation Snapshot
- Current price, market cap, TTM P/E, and TTM P/S reported (plus P/B for capital-heavy businesses, EV/EBITDA for leveraged / cyclical names).
- 3-year multiple range and sector / peer median (3–5 named comps) provided for context.
- Negative P/E is decomposed: cash-burning growth vs. one-off charge vs. cyclical trough vs. structural decline — with the specific filing line item cited.
- Stretched multiples (P/E > 50× or > 2× sector median, P/S > 15× or > 3× sector median) are explained with a named cause (sector premium, depressed earnings, narrative, M&A, small float) and a citation — not left dangling.
- If the multiple is extreme enough to be a risk (P/E > 50× without clear earnings path, P/S > 20× outside top-quartile growth), Section 9 includes a valuation / multiple-compression risk.

## Valuation, price target & forward estimates (rating / PT / scenarios)

The decision layer that mirrors institutional sell-side notes — see SKILL.md § "Learning from sell-side institutional research" and `report_structure.md` § "Investment summary header" + § 1A. **Guardrail running through every check below: the rating, the price target, the scenario PTs, and every projected estimate are the analyst's own forward view — labeled `*Analyst view:*` / `*分析师观点：*` and NEVER attached to a filing citation.** Checks:

- [ ] **Investment-summary header present** at the very top (above TOC / banner): rating, 12-month PT, current price, implied upside / downside %, one-line valuation method, market cap, 52-week range, ticker/exchange, 2–4 thesis pillars — the whole block labeled `*Analyst view:*`.
- [ ] **Forward valuation matrix present in the header** — at minimum P/E across last-actual / FY1E / FY2E, plus the 2–3 multiples that fit the business (PEG / EV/EBITDA / EV/FCF / EV/Sales / P/B for capital-heavy names); forward columns `*Analyst view:*`, the last-actual column sourced.
- [ ] **Relative-performance line present in the header** — 1M / 6M / YTD / 12M absolute return + the same windows for the benchmark + the relative (stock − benchmark), with the price source cited.
- [ ] **A defined rating** on one stated scale (`Buy/Hold/Sell` or `OW/N/UW`), not a vague verdict. (Private / un-targetable names: header states `Rating / PT: not applicable — <reason>`.)
- [ ] **Section 1 opens with an investment-thesis lead paragraph** (call + why-now + pillars) before the descriptive overview.
- [ ] **Forward financial-estimates table spans ≥3 years** (revenue / gross margin / operating-or-net margin / EPS, with YoY, **plus an FCF (or FCF yield) row and a net cash/(debt) row — and for loss-making names a cash-runway line (quarters, at current burn)**) — each projected cell `*Analyst view:*`; each driver's basis cited inline (filing segment data + balance sheet / cash-flow statement + guidance + an industry forecast). No `(Source: our model)` / `(模型估算)`.
- [ ] **The price target's derivation is shown** — forward-EPS × target-multiple, or DCF, or SOTP, or rNPV — with the arithmetic from estimate to PT, not just a number.
- [ ] **The target multiple is justified against 3–5 named comps** (the J.P. Morgan 40x-vs-Howmet-37x move). A multiple with no comp justification fails.
- [ ] **DCF WACC's risk-free rate is sourced to `indicators.db`** (the 10Y), with the as-of date stated; terminal growth ≤ risk-free rate.
- [ ] **Bull / base / bear PTs present**, each tied to its differentiating assumption, each with upside / downside %. All three `*Analyst view:*`.
- [ ] **Consensus benchmark stated** when sourced material carries it (where the report's estimates sit vs the Street); the consensus figure sourced to a zsxq note or a dated public source — never invented.
- [ ] **The 1–2 swing variables** the call hinges on are named.
- [ ] **No filing citation is attached to the rating, the PT, or any projected number.** Format check: scan the header + Section 1A — every PT / estimate / scenario line carries `*Analyst view:*` / `*分析师观点：*`, none carries a 10-K / 年度报告 / Yuho link.

## GF Score (GuruFocus-style) scorecard (Section 1B)

See `reference/gf_score.md` for the full rubric. Include in every initiation-style report unless the user said "skip the GF Score". Checks:

- [ ] **Section 1B present**, right after Section 1A — verdict line (`GF Score NN/100 — <band>`), the radar, the 5-axis table, the per-axis rationale, the composite arithmetic.
- [ ] **The radar renders** — the inline `<svg>` (from `scripts/gf_score.py`) is pasted **un-fenced** (not inside a ``` code block) so it displays as a chart, not source. The `--source` annotation is baked into the SVG footer.
- [ ] **All five axes scored 0–10** (Financial Strength / Profitability / Growth / GF Value / Momentum), or explicitly `n/a` with a stated reason; the **composite 0–100** maps to the correct GuruFocus band (91–100 / 81–90 / 71–80 / 51–70 / 0–50).
- [ ] **The composite arithmetic is shown** with the weights used (default 20/25/25/15/15); any deviation is stated.
- [ ] **Each axis has a one-paragraph rationale stating WHY that score**, naming the 2–4 driving metrics, **each with an inline citation** (margins / leverage / ROIC → filing page; multiples → market-data URL; returns → yfinance / `indicators.db`). No axis scored without reasons.
- [ ] **The sub-scores and composite are labeled `*Analyst view:*` / `*分析师观点：*`** and **no filing citation is attached to any score.** Format check: the GF Score table / verdict line carries no 10-K / 年度报告 / Yuho link.
- [ ] **The computed score is NOT attributed to GuruFocus.** A GuruFocus citation appears only if the real published number was pulled from `gurufocus.com/term/gf-score/<TICKER>`, and then it's shown as a *separate* cross-check (not merged). The "not GuruFocus™ official number" disclosure in the SVG footer is intact.
- [ ] **GF Value direction is stated** (`higher = cheaper vs fair value`) so a high GF-Value score isn't misread as "expensive".
- [ ] **Internal consistency:** Growth ↔ the Section-1A forward model; GF Value ↔ the Section-1 multiples + PT implied upside; Momentum ↔ the header relative-performance line. No GF axis contradicts the report's own numbers.

## Key debates & catalysts (Section 9.5)

Distinct from the Section 9 risk inventory — see `report_structure.md` § 9.5 and `risk_taxonomy.md`. Checks:

- [ ] **2–4 key debates present**, each as a one-line bear argument + an `*Analyst view:*` rebuttal with cited evidence (at least one grounded in the local zsxq bear case where coverage exists).
- [ ] **A dated 12-month catalyst list present** (event → approx date → why it moves the thesis), with a pointer to the `catalyst-calendar` skill.
- [ ] Section 9.5 does **not** merely restate the Section 9 risk taxonomy — it argues the thesis against specific bear points; the comprehensive downside map stays in Section 9.

## Customers & Go-to-Market
- Top-1 and top-5 customer share of revenue quantified from the latest annual filing (or explicitly noted as undisclosed).
- 3-year concentration trend captured when the disclosure history allows.
- Top customers named when disclosed; contract structure (multi-year vs. PO-by-PO) noted.
- If top-1 > 20% or top-5 > 50%, the report flags it in Section 5 **and** carries it into Section 9 as a material risk.
- **Every customer-share number is labelled with its denominator** ("X% of consolidated revenue" vs "X% of <Segment> segment revenue"); no unqualified "X% of revenue" when more than one denominator could apply.
- **Segment-level customer lists carry the "(segment-level; not aggregated to group-level)" qualifier inline.** A segment-level customer (e.g. NVIDIA in DS Memory) is never silently presented as if it were a consolidated top-5 customer.
- **Customer pie charts use one denominator only.** No single chart mixes consolidated and segment-level shares — if both are needed, draw two separate charts each with its denominator stated in the title.
- **The filing's named top-5 (alphabetical list, ranked list, or aggregate %) is the answer.** When the consolidated top-5 disclosure exists (Samsung 사업보고서, A-share 年报 `前五名客户`, etc.), the report does not append a sell-side / supply-chain composite that disagrees, and does not silently substitute a segment-level customer list for the group-level disclosure.
- **Every customer figure in Section 5 carries an inline citation in the paragraph that contains it** — citing the source once in a Section 4 table or in the References block does NOT cover a Section 5 paragraph that re-states the number.

## Risk Assessment
- 8–12 distinct risks across all four categories (see `risk_taxonomy.md`).
- 50–100 word description per risk.
- Impact quantified where possible.
- Mitigating factors noted.
- Customer-concentration risk is evaluated in every report (not optional) — included with quantified top-1 / top-5 % whenever top-1 > 10% or top-5 > 30%.

## Investor-lens scorecards (Section 10, when included)

See `investor_lenses.md` for the nine rubrics and verdict bands (four core 10.1–10.4 + five optional 10.5–10.9). Checks:

- [ ] Cycle snapshot block opens Section 10 — VIX, 10Y Treasury (`^TNX`), HY OAS (FRED BAMLH0A0HYM2) values with as-of date, all sourced to `indicators.db`.
- [ ] **10.4 (cycle posture) is computed first** and any disagreement with the company-specific verdicts (10.1, 10.2, 10.3, plus 10.8 Druckenmiller when included) is called out explicitly. No forced consensus.
- [ ] Each lens subsection has the verdict-first shape: bolded verdict line → 3–5 row scorecard table → 2–3 sentence evidence chain → per-lens required block (see below) → one-sentence failure mode.
- [ ] **Every input in every scorecard table is already cited in Sections 1–9** (or comes from the `indicators.db` snapshot with as-of date). No new inline citations introduced inside Section 10.
- [ ] Per-lens required blocks present where the lens is included:
  - [ ] **10.2 Munger** — mandatory inversion sentence ("the single scenario that most plausibly destroys the thesis is ___").
  - [ ] **10.3 Damodaran** — assumption block: revenue CAGR, terminal margin, reinvestment rate, WACC components (Rf + β × ERP), terminal growth (≤ Rf), intrinsic-value range, market cap, margin of safety. Terminal growth never above the risk-free rate.
  - [ ] **10.5 Lynch** — category statement ("this is a `<slow-grower/stalwart/fast-grower/cyclical/turnaround/asset-play>`") with one sentence of evidence.
  - [ ] **10.6 Fisher** — scuttlebutt note: at least one cited piece of evidence from outside the filings (customer interview, ex-employee quote, supplier interview, competitor concession, industry-conference takeaway). If only filings, downgrade by 1 point and label it.
  - [ ] **10.7 Burry** — downside-first paragraph naming the worst-defensible scenario and how the balance sheet survives it. Bullish verdicts require this paragraph.
  - [ ] **10.8 Druckenmiller** — macro context paragraph (Fed stance + HY OAS direction + 10Y direction, with as-of date) AND a named same-day-exit trigger. Bullish into a tightening regime requires explicit override rationale.
  - [ ] **10.9 Cathie Wood** — Wright's Law math (today's unit-cost, 5yr post-curve unit-cost, today's TAM, post-curve TAM) AND a convergence note naming at least one adjacent disruptive platform.
- [ ] Verdicts use `*Lens view:*` (English) / `*视角观点:*` (Chinese). No `Buffett would buy`, `Lynch would chase`, `林奇会买`, `Burry would short`, `Druckenmiller would size large`, `Cathie Wood projects X`, or similar persona endorsements.
- [ ] **Section 10 word count matches lens count:**
  - Core only → 600–1,000 words total.
  - Core + 1 optional → 750–1,250.
  - Core + all 5 optional → 1,500–2,500.

## Data Used / 数据来源清单 manifest (mandatory)

See `report_structure.md` → "Data Used" block for the format. Checks:

- [ ] Manifest block sits between the last body section (Section 10 or Section 9) and the References block, in **every** report produced (Chinese by default; both Chinese and English when bilingual mode is on).
- [ ] All categories present: Primary filings · Investor-relations materials · Market data · Third-party research · Institute research (local `db/zsxq.db` — list found-vs-fetched, or state "no local coverage") · Macro / cycle inputs (when Section 10 is included).
- [ ] Each entry carries a publication or filing date.
- [ ] **Stale notices / coverage gaps** subsection lists what couldn't be pulled or was older than 12 months, or explicitly states "none". A missing-or-empty stale-notices block is a defect — the inventory must acknowledge what isn't there.
- [ ] The manifest does **not** duplicate the References block — References list every URL cited inline; Data Used summarizes evidence categories and freshness.

## Writing Quality
- Professional, analytical tone.
- Lead with key insights.
- Concrete examples and data.
- Proper citations throughout (inline).

## Verification pass (mandatory — see SKILL.md Step 10)

The generating model has a documented pattern of fabricating SEC URLs, attributing analyst opinions to filings, inventing competitor product names, inventing market-share percentages, and inventing executive names. **Run Step 10 verification before declaring done.**

Required before declaring done:

- [ ] Every URL in the report HTTP-checked (`curl -sSL -o /dev/null -w "%{http_code}" <url>`); any 404 fixed or removed.
- [ ] Every SEC URL has a real filename pulled from the EDGAR submissions JSON (`https://data.sec.gov/submissions/CIK<padded>.json`) — no synthetic `<doctype>_<accession>.htm` patterns.
- [ ] No "dominant" / "leader" / "monopoly" / "co-leader" / "near-monopoly share" / "global #1" claim is attached to a 10-K citation unless the 10-K verbatim says it. These are analyst opinions; label them `*Analyst view:*` (English) or `*分析师观点：*` (Chinese) and either cite a third-party research source or leave uncited.
- [ ] No revenue-by-sub-segment percentage (e.g. "Etch is ~45% of Systems revenue") is attached to a 10-K citation — these are analyst estimates unless the company actually publishes the breakdown.
- [ ] No specific competitor *product* name (e.g. "AMAT NOKOTA", "Producer", "Endura") is attached to the subject's own 10-K — at minimum cite the competitor's filing or website. The subject's 10-K Competition section typically lists competitor *companies*, not products.
- [ ] Every named executive is confirmed in an 8-K or DEF 14A. Grep the cited filing for the exact name.
- [ ] Internal consistency: Section 1's competitive framing matches Section 7's; Section 2 timeline matches Section 1 prose; restructuring counts in narrative match the timeline numbers; product classifications (e.g. "Akara conductor vs dielectric etch") are consistent across the mermaid graph, Section 4 subsections, and Section 5 references.
- [ ] At least five 10-K-cited financial numbers spot-checked against the actual 10-K (revenue, gross margin, customer concentration, geographic mix, segment %, restructuring headcount, R&D as % of revenue, cash returned).
- [ ] **Step 0.5 sec-report-summary disposition recorded** (US issuers): the verification log states `ran (output: reports/earnings/<TICKER>_<date>.md)` or `skipped (<reason>)` — never silently omitted.
- [ ] **Link-title ↔ URL consistency checked**: every link whose title names a source (indicators.db, FRED, Yahoo, a broker, a filing) resolves to that source's domain — a 200-OK URL paired with the wrong title (e.g. `[indicators.db 快照](https://www.sec.gov/...)`) is a fail.
- [ ] A `<details>`-folded verification log appended after the References section, listing what was checked and any residual unknowns — with the `<summary>` line as the exact English string `Verification log (Step 10) — YYYY-MM-DD` (even in Chinese reports; tooling greps for it).

## Success Criteria — checklist before declaring done

1. Total word count is 6,000–10,000 (verify with `wc -w`). Don't pad to hit a number — if the content runs lean, ship it; if it runs long with real substance, that's fine.
2. **4–8 Mermaid diagrams embedded** — Mermaid only, no matplotlib PNGs (disabled 2026-06-03 for memory; see SKILL.md § Step 8). Use ` ```mermaid ` fences with `xychart-beta` (trends, bars), `pie`, `timeline`, `graph TD`, `quadrantChart`. Each chart has a markdown-link citation directly beneath it. **No Mermaid chart mixes units (%, currency, count) on one y-axis** — `xychart-beta` has a single axis; split revenue and margin into two stacked charts (see SKILL.md § Step 8). (Legacy PNGs from before 2026-06-03 may be reused in their original reports.)
3. **Guidance-change banner present at the top of the report when applicable.** If the latest earnings release / 业绩预告 / 8-K shows a raise, cut, color-bearing reaffirmation, or initiation of full-year guidance, the report opens with a `> **Update:**` blockquote (old vs. new range, disclosure date as a markdown-link citation, one-sentence driver). Omit entirely if no change.
2. All 9 sections present with their target word counts.
3. Substantive analysis, not just description.
4. Specific examples and quantitative data throughout.
5. Sources cited **inline** at the point each fact appears, plus a consolidated References list at the end.
6. Reader finishes able to understand:
   - **The call** — the rating, the 12-month price target, the implied upside%, and the 2–4 thesis pillars behind it (the investment-summary header + Section 1 lead)
   - **The forward model** — the 3-year revenue / margin / EPS trajectory, how the PT was derived, and the bull / base / bear scenarios (Section 1A)
   - What the company does and how it makes money
   - **Every product the company sells (from a thorough company-website walk) and which specific products have a competitive advantage — including moat type and closest named competitor product**
   - Background of the founder and current CEO
   - Company's competitive position
   - Market opportunity size
   - Key risks to consider
