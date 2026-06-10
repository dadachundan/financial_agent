# Sell-side sector-note house-style templates

Durable templates distilled from a 24-report survey of GS / MS / UBS / J.P. Morgan / Bernstein / Citi / Nomura / BofA / Deutsche Bank / HSBC sector notes. Reuse these schemas so the skill doesn't re-derive them each run. Each is tagged with the bank + series it came from. None of these loosen the project's citation, numerical-accuracy, no-invented-TAM, or chart-annotation rules — they sit on top of them.

---

## 1. Industry-View rating scale (MS signature)

Fixed 3-tier scale, stated at the very top, before prose:

> **Industry View: Attractive / In-Line / Cautious**

Source series: *MS "<Region> <Sector> Overview / Deep Dive"* (e.g. "China Autos & Shared Mobility", "Greater China Semiconductors"). A sell-side firm's rating stays `*Analyst view:*` unless self-derived from this report's evidence.

---

## 2. Bolded executive lead-in layer (MS / GS / Citi / UBS universal signature)

Open the body with **4–6 verb-first, bolded, telegraphic bullets**, each mapping to a body section:

> - **Upgrading** the sector to Attractive on the capex-cycle inflection (§ Supply/Demand).
> - **Prefer X over Y** — cloud semis > legacy memory > PC (§ Sub-segment ranking).
> - **Key debate we resolve:** the market believes A; the data shows B (§ Key Debates).
> - **Keep OW on** <name> into the Q3 print (§ Top picks).

Source series: *MS "Upgrading… / Accelerating… / Implications of… / Keep OW on…"* lead-ins; mirrored by GS ("Stronger, Broader Capex Boom"), Citi ("Prefer Sungrow & Deye"), UBS "Takeaways".

---

## 3. Top-picks table schema (UBS / Citi / GS — every note ends here)

| Ticker | Rating | 12m Target Price | Upside % | Valuation method | One-line rationale | Up-risk / Down-risk |
|--------|--------|------------------|----------|------------------|--------------------|---------------------|

- Valuation method *in the cell*: "2027E 28x PE" / "DCF, WACC 9%, terminal 4%" / "EV/EBITDA discount to peer".
- Up-risk AND down-risk per name — never one-sided.
- TP / multiple must string-match a cited source; sell-side rating/TP labelled `*Analyst view:*` unless self-derived.

Source series: *UBS "<Sector> Sector: Takeaways"*, *Citi "Prefer X & Y"*, *GS "<Company> Deep Dive"*.

---

## 4. Value-chain priced/tiered table (Citi / Bernstein / HSBC)

Walk the chain node-by-node, with economics at each node:

| Node | Who plays | Where margin accrues | Unit price / economics |
|------|-----------|----------------------|------------------------|

Examples: Citi solar poly→wafer→cell→module (¥/W per node); IDC colocation vs neocloud ($/MW capex + payback); 托管 vs Neocloud (revenue 8–10×).

Source series: *Citi "PRC Solar Sector"* price-by-tier table; *Bernstein "…primer for investors on their economics"*.

---

## 5. Supply / Demand Balance template (UBS / Bernstein)

Build the supply side symmetrically against demand — distinct from the TAM section:

- **Supply build** in native units, by region and by year: kwpm fab roadmaps, GW pipelines, Mt capacity ceilings, MW net adds.
- **Demand drivers** with penetration/share trajectories quantified by year.
- **Gap** between the two, stated explicitly.
- **"New supply compresses returns / success cannibalizes IRR"** dynamic where relevant.
- **Price-vs-volume decomposition** for any growth print ("revenue +106% YoY but units flat — driven by ASP").
- **Seasonality/cycle benchmark**: every MoM/YoY vs the typical seasonal pattern or 10-yr average ("−2.2% MoM vs −11.3% typical").

Source series: *UBS supply/demand-balance channel-check notes*; *Bernstein WSTS / Global Semis Tracker*.

---

## 6. "Believe-X / show-Y" debate template (MS / Nomura)

Frame 2–4 named debates as the report's spine:

> **Debate <n>: <named debate>.** *The market believes* <X>. *The evidence shows* <Y> — <the data that settles it>. **Stance:** <call>.

Add dated cycle milestones, not vague "long-term": "transition 2–3 years then inflection"; "risk-off until shaft-sinking de-risks ~mid-2027".

Source series: *MS "Hefei Paradox"*; *Nomura "2–3 year transition before industrial AI scales"*.

---

## 7. "What's Changed" revision box (Nomura / DB — for update-in-place refreshes)

| Metric | Old | New | Driver |
|--------|-----|-----|--------|
| TAM (2030) | … | … | … |
| Sector CAGR | … | … | … |
| Top pick / rating | … | … | … |
| 12m TP (<name>) | … | … | … |

State old vs new vs driver: "we raise 2026 WFE from $143bn to $149bn (+27% YoY)". Position house numbers against consensus ("2027 OP +12% above Bloomberg consensus").

Source series: *Nomura "Global <Sector> Monthly" forecast-revision table*; *DB sector demand-forecast revisions ("+46% to 2030 DC power")*.

---

## 8. Named industry-body datasets (the sizing spine)

Anchor every sizing/health claim to a recurring tracker, cited with its print date — not a firm homepage:

WSTS / SIA (semis sales) · SEMI (WFE forecasts) · TrendForce / TSR (storage production) · IPnest / Gartner / IDC (share trackers) · Riglogix (rig day-rates & utilization) · SCFI / Shanghai (freight indices) · IQVIA / IBISWorld (pharma / industry).

Channel checks & conference takeaways (COMPUTEX, GTC, SNEC, AIC, EU Auto Conf) are dated, attributed citations — date + venue + who — never unsourced "analyst view".

Source series: *Bernstein WSTS Tracker*; *J.P. Morgan "Component Data" / TSR trackers*; *GS "SIA April data"*.

---

## 9. Further viewing / 延伸观看 (teaching aid, not a citation)

- **延伸观看 / Further viewing** — 1–3 validated explainer videos for hard-to-visualize concepts (the sector's core technology or process), in their own slot, never a citation (see SKILL.md).
