# Quality Standards & Success Criteria

## Content Depth
- Each section meets its minimum word-count target (see `report_structure.md`).
- Analysis is substantive, not just descriptive.
- Specific examples and quantitative data, not generic statements.
- Sources cited **inline** throughout the body, not only at the end (see `citations.md`).
- Objectivity and balance.

## Management Bios
- 300–400 words per executive for 3–4 key executives.
- Each bio includes current role, prior experience, key accomplishments, education.
- Enough detail to assess track record and capabilities.

## Competitive Analysis
- 5–10 specific competitors analyzed.
- Both direct and indirect competitors.
- Relative positioning on key dimensions assessed.
- Company's competitive advantages and vulnerabilities identified.
- Specific data and examples, not generalities.

## Products & Services
- Every product on the company website enumerated (no collapsing).
- Per-product competitive-advantage verdict (yes / partial / no) with moat type.
- Closest named competitor product called out for each material product.
- Flagship 1–3 products clearly distinguished from long-tail.
- Last-12-month launches / sunsets noted.

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

## Success Criteria — checklist before declaring done

1. Total word count is 6,000–10,000 (verify with `wc -w`). Don't pad to hit a number — if the content runs lean, ship it; if it runs long with real substance, that's fine.
2. **4–8 charts/diagrams embedded** — mix of matplotlib PNGs (`reports/charts/<company>_<name>.png`, referenced via `![alt](charts/...)`) and Mermaid blocks (` ```mermaid ` fences). Each chart has a markdown-link citation directly beneath it.
2. All 9 sections present with their target word counts.
3. Substantive analysis, not just description.
4. Specific examples and quantitative data throughout.
5. Sources cited **inline** at the point each fact appears, plus a consolidated References list at the end.
6. Reader finishes able to understand:
   - What the company does and how it makes money
   - **Every product the company sells (from a thorough company-website walk) and which specific products have a competitive advantage — including moat type and closest named competitor product**
   - Quality and track record of management team
   - Company's competitive position
   - Market opportunity size
   - Key risks to consider
