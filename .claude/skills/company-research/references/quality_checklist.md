# Quality Standards & Success Criteria

## Content Depth
- Each section meets its minimum word-count target (see `report_structure.md`).
- Analysis is substantive, not just descriptive.
- Specific examples and quantitative data, not generic statements.
- Sources cited **inline at the paragraph level** — every substantive paragraph carries at least one inline markdown-link citation, not just one per section (see `citations.md`).
- **Pre-submit citation count check:** `grep -oE '\[[^]]+\]\(http[^)]+\)' <report>.md | wc -l` should yield ≥40 for a 6,000–10,000 word report. Reports below the threshold have unsourced paragraphs — find and cite them before submitting.
- Objectivity and balance.

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
- The issuer's own product table is **embedded as a rendered PNG image** at the top of Section 4 (use `.claude/skills/company-research/scripts/render_10k_section.py`), with a 10-K citation in the caption.
- The same table is also reproduced as a markdown table immediately below the image (for searchability and link targets).
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
- Section 4 word count is in the upper half of section ranges (≥1,000 words) — *if Section 6 is longer than Section 4, the priority is wrong*; cut Section 6 and expand Section 4.

## Company Overview — Valuation Snapshot
- Current price, market cap, TTM P/E, and TTM P/S reported (plus P/B for capital-heavy businesses, EV/EBITDA for leveraged / cyclical names).
- 3-year multiple range and sector / peer median (3–5 named comps) provided for context.
- Negative P/E is decomposed: cash-burning growth vs. one-off charge vs. cyclical trough vs. structural decline — with the specific filing line item cited.
- Stretched multiples (P/E > 50× or > 2× sector median, P/S > 15× or > 3× sector median) are explained with a named cause (sector premium, depressed earnings, narrative, M&A, small float) and a citation — not left dangling.
- If the multiple is extreme enough to be a risk (P/E > 50× without clear earnings path, P/S > 20× outside top-quartile growth), Section 9 includes a valuation / multiple-compression risk.

## Customers & Go-to-Market
- Top-1 and top-5 customer share of revenue quantified from the latest annual filing (or explicitly noted as undisclosed).
- 3-year concentration trend captured when the disclosure history allows.
- Top customers named when disclosed; contract structure (multi-year vs. PO-by-PO) noted.
- If top-1 > 20% or top-5 > 50%, the report flags it in Section 5 **and** carries it into Section 9 as a material risk.

## Risk Assessment
- 8–12 distinct risks across all four categories (see `risk_taxonomy.md`).
- 50–100 word description per risk.
- Impact quantified where possible.
- Mitigating factors noted.
- Customer-concentration risk is evaluated in every report (not optional) — included with quantified top-1 / top-5 % whenever top-1 > 10% or top-5 > 30%.

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
- [ ] A `<details>`-folded verification log appended after the References section, listing what was checked and any residual unknowns.

## Success Criteria — checklist before declaring done

1. Total word count is 6,000–10,000 (verify with `wc -w`). Don't pad to hit a number — if the content runs lean, ship it; if it runs long with real substance, that's fine.
2. **4–8 charts/diagrams embedded** — mix of matplotlib PNGs (`reports/charts/<company>_<name>.png`, referenced via `![alt](charts/...)`) and Mermaid blocks (` ```mermaid ` fences). Each chart has a markdown-link citation directly beneath it.
3. **Guidance-change banner present at the top of the report when applicable.** If the latest earnings release / 业绩预告 / 8-K shows a raise, cut, color-bearing reaffirmation, or initiation of full-year guidance, the report opens with a `> **Update:**` blockquote (old vs. new range, disclosure date as a markdown-link citation, one-sentence driver). Omit entirely if no change.
2. All 9 sections present with their target word counts.
3. Substantive analysis, not just description.
4. Specific examples and quantitative data throughout.
5. Sources cited **inline** at the point each fact appears, plus a consolidated References list at the end.
6. Reader finishes able to understand:
   - What the company does and how it makes money
   - **Every product the company sells (from a thorough company-website walk) and which specific products have a competitive advantage — including moat type and closest named competitor product**
   - Background of the founder and current CEO
   - Company's competitive position
   - Market opportunity size
   - Key risks to consider
