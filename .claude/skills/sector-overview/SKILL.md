---
name: sector-overview
description: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".
---

# Sector Overview

**Scope boundary:** this skill owns the *multi-company* industry/landscape essay. Distinct from `theme-research` (tracked, refreshed baskets → `reports/themes/`), `company-research` (one issuer → `reports/company/<Slug>/`), and `zsxq-analyze` (digest of one named broker PDF). If the deliverable is a single company's brief or a single PDF's digest, it does not belong in `reports/sector/`.

## Guardrails (at-a-glance — the rules with the worst failure modes)

- **Do not invent TAM numbers or growth rates.** Every market-size figure traces to a specific named source — research firm + report title + publication date — with the URL. "TAM ~$X B" with no source is a defect. See § "Important Notes".
- **Do not paraphrase a sell-side opinion as a primary-source fact.** "X is the share leader" is an analyst view unless a cited third-party leaderboard (IPnest, Gartner Magic Quadrant, IDC tracker, IBISWorld, IQVIA, TrendForce) says so at a specific URL. Label `*Analyst view:*` otherwise.
- **Do not let "TAM" hide the difference between addressable, served, and obtainable.** Distinguish TAM / SAM / SOM in the market-size section; mixing them is the single most common failure of sector overviews.
- **Do not cite content-farm reposts (CSDN / 知乎专栏 / 百度有驾 / 搜狐自媒体) for numbers.** Source hierarchy for any quantitative claim: (1) the primary filing or industry-body tracker release; (2) a broker PDF in the local zsxq library, cited via the direct-download route with a page pin (see Step 1.5); (3) reputable financial press with publication date. If only a repost is reachable, label the chain explicitly — `[GGII 2025 蓝皮书，经新浪转载](URL)` — and flag it under Stale notices / coverage gaps in the Data Used manifest.
- **Do not skip the Data Used manifest** at the end of the report (see block below).
- **Do not ignore freshness.** Sector reports age fast — discard web sources older than 12 months unless they're landmark research. Include publication dates in link titles.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Workflow

> **House-style templates:** the durable sell-side schemas referenced throughout the workflow below (Industry-View rating scale, bolded executive lead-in layer, top-picks table, value-chain priced table, supply/demand-balance template, believe-X/show-Y debate template, "What's Changed" box) are collected in [`references/house_style.md`](references/house_style.md). Reuse them rather than re-deriving each run.

### Step 0: Verdict & Industry View header (mandatory — write this first)

Mirror the **Morgan Stanley / GS / Citi sector-note signature**: institutions open on a *stance*, not on scope. Before any prose, the report carries a header block:

- **Sector Verdict** — one directional line carried in the report *title* where possible (Citi "Prefer Sungrow & Deye"; GS "Stronger, Broader Capex Boom"; HSBC "Our top pick in the China DC sector"). A neutral landscape essay still gets a one-line house take.
- **Industry View** — a fixed 3-tier rating on the MS scale: **Attractive / In-Line / Cautious**. State it explicitly; do not bury it in prose.
- **As-of date** — the report is a living document (see update-in-place rule); date the stance.
- **4–6 bolded, verb-first executive lead-in bullets** that each map to a body section (MS pattern: "**Upgrading…**", "**Accelerating…**", "**Prefer X over Y…**", "**Key debate we resolve…**", "**Keep OW on…**"). This scannable executive layer is the single most consistent structural signature across the MS/GS/Citi/UBS library — make every bullet telegraphic and section-anchored.

Keep ratings traceable: a sell-side firm's "Attractive" stays *Analyst view:* unless self-derived from the evidence in this report.

### Step 1: Define Scope

- **Sector / subsector**: What industry and how narrowly defined?
- **Purpose**: Client report, internal research, pitch material, idea generation
- **Depth**: High-level overview (5-10 pages) or deep dive (20-30 pages)
- **Angle**: Neutral landscape vs. thematic thesis (e.g., "AI infrastructure buildout")
- **Universe**: Public companies only, or include private?

### Step 1.5: Mine the zsxq broker library first (mandatory)

Before web research, pull the sell-side view of the sector from the local library (`db/zsxq.db`, ~7,000 broker PDFs) — read-only:

```bash
cd /Users/x/projects/financial_agent
/opt/anaconda3/bin/python3 zsxq_fts.py --query "<sector keywords — Chinese terms work best>" --limit 20
```

- Deep-read the 2–3 most relevant sector PDFs; use them for TAM anchors, supply/demand numbers, capacity roadmaps, sub-segment forecasts, and top-pick TPs (always labelled `*Analyst view:*`).
- **Citation rule:** every zsxq-sourced claim links the PDF via the direct-download route printed by `zsxq_fts.py` as `pdf_url` — `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>` — with a page pinpoint: `[Nomura 大中华半导体复兴指南, p. 13](pdf_url)`. Never `localhost`, never `/zsxq/pdf-viewer/<id>` (HTML viewer, won't download on iPad), never the dead `/zsxq-pdf/<id>`. A page reference like "(p. 4)" with no clickable PDF link is a citation defect.
- **Boundary:** a chapter-by-chapter digest of ONE zsxq PDF is `/zsxq-analyze` territory, not a sector overview — this skill synthesizes across multiple sources.

### Step 2: Market Overview

**Market Size & Growth**
- Total addressable market (TAM) with source. Present TAM as a forward, sourced, *revisable BUILD* — not a static number (Nomura/DB style: "2030 China DC power 805 TWh, **+46% vs prior**, = 6% of national load"). State the % revision and the base; never a bare TAM. (Reinforces — does not loosen — the no-invented-TAM guardrail.)
- Historical growth rate (5-year CAGR)
- Forecast growth rate and key assumptions
- **Decompose any sector-health print into price vs volume** (Bernstein WSTS style: "revenue +106% YoY but units flat — driven by ASP, memory +364%"). Never quote a sector growth number without splitting price from volume.
- **Benchmark every MoM/YoY against the typical seasonal pattern or 10-yr average** (SIA style: "−2.2% MoM vs −11.3% typical"). A growth print with no cycle/seasonality anchor is incomplete.
- Market segmentation (by product, **geography/region as a first-class axis**, end market, customer type). Where the sector splits by region — capacity by country, export share by market, hub-by-hub demand — require a region-by-region breakdown (UBS China-vs-Indonesia-vs-Middle-East aluminum; ASEAN hub-by-hub IDC; autos export-share-by-market), not geography as one throwaway dimension.

**Supply / Demand Balance** (distinct from the TAM section)

Build the supply side *symmetrically* against demand drivers — UBS/Bernstein style:
- Capacity adds in native units (kwpm / GW / Mt / MW pipeline), **by region and by year** (fab-by-fab kwpm roadmaps; national capacity ceilings like China aluminum 45.5/46Mt; ASEAN IDC 2–3GW/yr net adds).
- State the resulting **gap** between supply build and demand growth.
- Where relevant, spell out the **"new supply compresses returns / success cannibalizes IRR"** dynamic (Bernstein primer signature).
- Quantify penetration-rate and share trajectories with explicit years (NEV penetration 60% 2026; L2+ ADAS 32% 2026; export share 15%→16.5% by 2030) — not vague "who is gaining share".

**Industry Structure**
- Fragmented vs. consolidated — top 5 market share
- **Value chain — walk it node-by-node as a PRICED/TIERED table, not a single bullet.** Each node: who plays | where margin accrues | unit price / economics (Citi solar poly→wafer→cell→module ¥/W; IDC colocation vs neocloud $/MW capex + payback; 托管 vs Neocloud revenue 8–10×). The point is to show *where* margin pools, with numbers at each node.
- **Sub-segment ranking (mandatory, explicit, ordered).** Rank the sub-segments by attractiveness with a one-line *why* each — GS "prefer DESS over modules"; "cloud semis > legacy memory > PC semis"; Citi "prefer Sungrow & Deye". An ordered preference is required; generic "segmentation" is not a ranking.
- Business model types (subscription, transaction, licensing, services)
- Barriers to entry (capital, regulatory, technical, network effects)

**Key Trends & Drivers**
- Secular tailwinds (3-5 major trends)
- Headwinds and risks
- Technology disruption vectors
- Regulatory developments
- M&A activity and consolidation trends

### Step 3: Competitive Landscape

**Top-picks table** (for top 5–10 players) — every UBS/Citi/GS note ends here. Use the institutional column set, not a bare landscape grid:

| Ticker | Rating | 12m Target Price | Upside % | Valuation method | One-line rationale | Up-risk / Down-risk |
|--------|--------|------------------|----------|------------------|--------------------|---------------------|
| | | | | | | |

- **Valuation method travels with the number, in the cell** (UBS/Citi style: "2027E 28x PE" / "DCF, WACC 9%, terminal 4%" / "EV/EBITDA discount to peer"). Tag the multiple year (2027E PE 28x).
- **Pair up-risk AND down-risk per name** — never a one-sided risk list.
- Keep every TP / multiple traceable to a cited source per the project's numerical-accuracy rule (the number must string-match the cited URL). **Label any sell-side rating / TP as `*Analyst view:*` unless self-derived** from this report's own evidence.

A fuller business descriptor still follows below the table; the table is the scannable verdict layer.

For each company, brief profile:
- Business description (2-3 sentences)
- Strategic positioning and moat
- Recent developments (earnings, M&A, product launches)
- Valuation snapshot (P/E, EV/EBITDA, EV/Revenue)

**Competitive Dynamics**
- How do companies compete? (price, product, service, distribution)
- Who is gaining/losing share and why?
- Disruption risk from new entrants or adjacent players

### Step 4: Valuation Context

- Sector trading multiples (current and historical range)
- Premium/discount drivers (growth, margins, market position)
- Recent M&A transaction multiples
- How does the sector compare to the broader market?
- **Project-level unit economics alongside trading multiples** — where the sector is project/asset-based (energy, IDC, mining, capital equipment), don't stop at multiples. Require sourced **IRR** (BESS 8–12%), **ROIC** (ASEAN IDC 9–12%), **capex per unit** ($8–15M/MW colocation vs $45M neocloud), **payback** (~5yr), and the **build-cost path** ($7000→$3000/kW) — the Bernstein/UBS economics-first primer signature. Keep the multiples too; add the economics.
- **Position house numbers against the street** (forecast-revision discipline): state prior estimate, new estimate, the driver, and the resulting EPS/OP delta vs consensus ("2027 OP +12% above Bloomberg consensus").

### Step 5: Investment Implications

- Where are the best risk/reward opportunities?
- What thematic bets can be expressed through this sector?

**Key Debates We Resolve** (its own numbered sub-section — the report's spine, not a thin bullet)

Frame 2–4 named debates as **"the market believes X; the evidence shows Y"** (MS "Hefei Paradox": market believes X, we show Y; Nomura: "a 2–3 year transition before industrial AI scales"). Give each debate a stance and the *data that settles it*. This is the institutional analog of bull/bear — promote it above a generic bull-vs-bear list.

- **Scenario / timeline framing for the cycle** — dated milestones, not vague "long-term": "transition 2–3 years then inflection"; "risk-off until shaft-sinking de-risks ~mid-2027".
- Catalysts that could change the sector narrative

### Step 5.5: Charts (mandatory — 3–6 minimum per report)

Charts are a numbered deliverable, not garnish — the sell-side benchmark packs dozens of exhibits per note, and a forecast table rendered as a fenced-code ASCII block is a defect.

- **Pick 3–6 that fit the sector:** market-size build (by year × segment), sub-segment growth trajectories, valuation comp scatter (P/E vs growth), share/penetration trends, region/hub capacity-vs-demand bars, BOM-cost or build-cost decline path.
- **Implementation:** matplotlib via `/opt/anaconda3/bin/python3`; save PNGs to `reports/charts/<topic-slug>_<chart>.png` (existing repo convention); embed with `![](../charts/<file>.png)`.
- **Every chart carries the project's mandatory in-chart data-source footer annotation** and, for multi-series charts, an x-axis clipped to the intersection of all plotted series' valid data (global chart rules in `CLAUDE.md`).
- A forecast sourced from multiple firms gets a grouped-bar chart — never an ASCII table.

### 延伸观看 / Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — the sector's core technology or process (how an EUV scanner exposes a wafer, how a GLP-1 drug acts on the gut–brain axis, how a data-center liquid-cooling loop removes heat, how a humanoid robot's actuators / harmonic reducers / force sensors work), a manufacturing or scientific process, a complex value-chain architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**延伸观看 / Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept. English-only reports use `**Further viewing**`.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(B站，部分地区或需登录)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### Step 6: Output

**Save to** `reports/sector/<topic-slug>_<YYYY-MM-DD>.md` (relative to the project root — `/Users/x/projects/financial_agent/reports/sector/`). `<topic-slug>` MUST start with an English or pinyin slug — the project-wide filename rule (`CLAUDE.md` § "Research Report Filenames"); pure-Chinese filenames are unsearchable and not acceptable. An optional Chinese component may follow the English one: e.g. `humanoid_robot_sensors_人形机器人传感器_2026-05-16.md`, `semiconductor_materials_半导体材料_2026-05-24.md`, `ai-infrastructure-buildout_2026-06-01.md`. Pre-save naming check: (1) first slug component is English/pinyin; (2) date suffix present on new files; (3) when refreshing a legacy pure-Chinese filename, `git mv` it to a compliant name in the same commit and note the rename in the What's-Changed box. Supplementary deliverables (Word, PowerPoint, Excel appendix) can sit next to the markdown using the same `<topic-slug>` prefix.

**Folder scope:** `reports/sector/` holds multi-company industry/landscape reports produced by this skill ONLY. A single-company brief or valuation snapshot belongs in `reports/company/<Slug>/` next to the deep-dive; a digest of one named broker PDF follows the `/zsxq-analyze` output convention; tracked baskets live in `reports/themes/` (`theme-research`).

Deliverables:
- Markdown sector overview (primary, always)
- Optional: Word document or PowerPoint with:
  - Market overview and sizing
  - Competitive landscape map
  - Company comparison table
  - Valuation summary
  - Key charts: market growth, share trends, valuation history
- Optional: Excel appendix with detailed company data

**Language (default: bilingual).** Deep-research skills keep a bilingual default — English primary at `reports/sector/<topic-slug>_<YYYY-MM-DD>.md` plus a Simplified Chinese companion `<topic-slug>_<YYYY-MM-DD>_zh.md` (mirroring `compare-companies`). The Chinese file keeps technical / financial / industry terms in English alongside the Chinese gloss (e.g. `gross margin (毛利率)`). Produce a single language only when the user explicitly asks ("English only", "中文", `--lang …`); the language the user happens to phrase the request in does NOT silently override the default.

### Data Used / 数据来源清单 (mandatory at the end of every report)

A structured manifest of evidence categories + dates + freshness. Goes immediately before the References block (or, if the report has no separate References block, at the end). Format:

```markdown
## Data Used / 数据来源清单

**Market sizing**
- Gartner / IDC / IBISWorld / IQVIA / Yole / TrendForce report titles + publication dates + URLs. Note the TAM / SAM / SOM scope of each.
- **Prefer recurring industry-body datasets as the named spine** for sizing/health claims — institutions anchor every sector claim to one: WSTS / SIA monthly semis sales, SEMI WFE forecasts, TrendForce / TSR storage-production trackers, IPnest / Gartner / IDC share trackers, Riglogix offshore-rig day-rates & utilization, SCFI / Shanghai freight indices. Cite the tracker (with the print date), not the firm homepage.

**Growth & forecasts**
- Each forward growth rate cited to a named research firm or company-disclosed projection with publication date. Recent industry-research notes (last 12 months) preferred.
- **Channel checks / expert calls / conference takeaways are cited as dated, attributed evidence — not unsourced "analyst view"** ("visited 8 listed solar firms + ~20 supply-chain experts at SNEC, June 3–5"; "industry checks indicate…"). Make the check a citation: date + venue + who. Conference reads (COMPUTEX, GTC, SNEC, AIC, EU Auto Conf) are a recurring, legitimate sector-read vehicle when sourced this way.

**Competitive landscape**
- Top 5–10 players covered — each anchored to their latest 10-K / 年度报告 / Yuho (filing date) and IR materials (deck dates). Recent M&A transactions cited to press releases.

**Valuation context**
- Sector trading multiples as of YYYY-MM-DD; recent comparable M&A transaction multiples; sources (Yahoo Finance / Capital IQ / Bloomberg / mergermarket).

**Stale notices / coverage gaps**
- <bulleted list — TAM source paywalled, private-company financials not disclosed, regulatory data delayed, or "none">.
```

The manifest distinguishes evidence categories from the consolidated References list. References list every URL cited inline; Data Used summarizes the source categories + freshness.

### Update-in-place rule — at most one report per topic

Reports under `reports/sector/` are tracked in git and meant to be living documents. **Before writing, check whether a report for this topic already exists** and update it in place rather than creating a parallel dated copy.

```bash
ls reports/sector/ 2>/dev/null | grep -i "<topic-slug-or-keyword>"
```

- **Exactly one match for this topic** → overwrite it at the same path. Keep the existing filename even if its embedded date is stale — git history records the actual revision date. Update the document's "as of" header to today.
- **Multiple matches for the same topic** (legacy state) → update the most recent by mtime, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new file using today's date in the filename.

If the user asks for a clearly different angle on the same sector (e.g. "China robotics — *export* angle" vs. an existing "China robotics — *domestic adoption* angle"), use a distinct `<topic-slug>` so the reports stay separate. The "one per topic" rule applies per topic-slug, not per sector.

**"What's Changed" revision box (required when refreshing an existing report).** Sector primers are living documents; the delta is the value. When updating in place, surface an old-vs-new box near the top — TAM / CAGR / top-pick ratings / target prices side by side, each with the driver (Nomura forecast-revision table style: "we raise 2026 WFE from $143bn to $149bn (+27% YoY)… **driver:** memory capex"). This operationalizes the update-in-place rule — don't silently overwrite the old numbers.

```markdown
## What's Changed (since <prior as-of date>)
| Metric | Old | New | Driver |
|--------|-----|-----|--------|
| TAM (2030) | … | … | … |
| Sector CAGR | … | … | … |
| Top pick / rating | … | … | … |
| 12m TP (<name>) | … | … | … |
```

### Step 7: Pre-save compliance gate & verification (mandatory — a report missing any item is not done)

**Compliance checklist** — tick every box and echo the result into the verification log:

- [ ] Verdict + Industry View header with 4–6 bolded lead-in bullets (Step 0)
- [ ] Supply/demand-balance section (Step 2)
- [ ] Ordered sub-segment ranking (Step 2)
- [ ] Top-picks table — Rating / TP / Upside / valuation method / up- & down-risk, `*Analyst view:*` labels (Step 3)
- [ ] 3–6 charts embedded (Step 5.5)
- [ ] Filename starts with English/pinyin slug + date (Step 6)
- [ ] Data Used manifest with stale-notices block
- [ ] Verification log appended (below)

**Verification — run before saving:**

1. **HTTP-check every external URL** with a real-browser User-Agent; `200 OK` only, per the global link-validation rules in `CLAUDE.md`. Retry timeouts at 30s; drop any link that confirms 4xx/5xx.
2. **Check every internal cross-report link resolves** with `ls` — sibling reports are linked by relative path (`../company/<Slug>/<file>.md`); never guess a sibling report's filename.
3. **Spot-check 3–5 numbers per major section** — string-match each against the URL cited *in the same paragraph*. Derived/scenario tables (e.g. forward-PE premium ranges, interpolated sub-segment forecasts) either show the calc inline with both inputs cited, or get cut.
4. **Append the verification log** at the end of the report (the "(Step 10)" label is the project-wide log convention from the company-research spec — keep it verbatim):

```markdown
<details><summary>Verification log (Step 10) — YYYY-MM-DD</summary>
- URL checks: N external URLs checked, all 200 (list any dropped/replaced)
- Internal links: N checked, all resolve
- Number spot-checks: "X = N from <URL>": ✓ string-matches | ✗ NOT in source — fixed
- Compliance gate: 8/8 items present
</details>
```

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

## Important Notes

- Source all market size data — cite the research firm or methodology
- Distinguish between TAM hype and realistic addressable market
- Sector overviews age fast — note the date and flag data that may be stale
- Charts are mandatory — see Step 5.5 for the minimum set (3–6), tooling, save path, and the in-chart data-source footer / x-axis-intersection rules.
- If for a client, tailor the "so what" to their specific situation (M&A target identification, competitive positioning, market entry)
