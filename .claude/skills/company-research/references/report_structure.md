# Report Structure — Section-by-Section Spec

The final report has 9 sections plus a References block. Word counts are loose targets — verify with `wc -w` before declaring done. Total target: **6,000–10,000 words** (sections may run longer than the per-section ranges below if there's genuine substance; do not pad to hit a number).

Embed **4–8 Mermaid diagrams** across the report — **Mermaid only, no matplotlib PNGs.** (Disabled project-wide 2026-06-03 to cut per-agent memory footprint; see SKILL.md § Step 8 for the rationale. Mermaid covers every chart type the report needs, including quantitative trends via `xychart-beta`.) Suggested placement:

| Section | Mermaid block | IR-deck slide that often anchors it |
|---|---|---|
| 1 Overview | `xychart-beta` revenue trend + a separate gross-margin chart (3–5 yr; two stacked blocks — `xychart-beta` has one y-axis, never % and currency together) | Latest earnings-deck "Revenue + Margin Bridge" slide |
| 2 History | `timeline` block — founding → milestones | Investor day "Our journey" slide (when present) |
| 4 Products | `graph TD` product portfolio tree | Investor day product-portfolio slide |
| 5 Customers | `pie` — top 3–5 customer concentration (one denominator) | Investor day customer-logo / cohort slide |
| 7 Competitive | `quadrantChart` **or** `xychart-beta` peer-comp bars | Investor day "Why we win" / feature-matrix slide |
| 8 TAM | `xychart-beta` market-size growth | Investor day TAM build slide (the single most useful IR slide) |

Every chart needs a citation directly underneath in the same markdown-link format used in prose. **When an IR deck has the data behind a chart, embed the rendered IR slide as a PNG** (using `render_10k_section.py`-style page screenshot for PDFs, which is a one-shot playwright-chromium screenshot — not matplotlib chart-gen) **instead of rebuilding the chart from scratch** — the slide is the most authoritative form of the chart, the company endorses the numbers, and the reader can trace the source. Cite the slide directly underneath. Legacy per-chart PNGs in `reports/charts/` from before 2026-06-03 can be reused in their original reports; do not regenerate them as Mermaid.

## Investment summary header (rating + price target) — REQUIRED, at the very top

**Above the TOC (and above the guidance banner), open with a standardized header block** — the Deutsche Bank / GS / Citi cover-page pattern that opens every institutional single-name note. See SKILL.md § "Learning from sell-side institutional research" for the rationale. The whole block is **the analyst's own forward view — label it `*Analyst view:*` / `*分析师观点：*` and never attach a filing citation to the rating, the PT, or the implied upside%** (a 10-K contains no price target; attaching one is the misattribution failure the skill forbids).

**Required fields:**
- **Rating** — pick one scale and state it: `Buy / Hold / Sell` or `Overweight / Neutral / Underweight`. One rating, defined.
- **12-month Price Target** + **current price** + **implied upside / downside %**.
- **Valuation method, one line** (e.g. `2027E EPS $13.08 × 22× P/E`, or `DCF, WACC 9.5%, terminal g 2.5%`, or `SOTP across 6 segments`).
- **Market cap**, **52-week range**, **ticker / exchange**.
- **Forward valuation matrix (institutional cover-page element — the Bernstein/GS/UBS block).** A compact one-row-per-metric mini-table of the key *forward* multiples across last-actual / FY1E / FY2E (and FY3E if modeled): at minimum **P/E**, plus the 2–3 that fit the business (`PEG`, `EV/EBITDA`, `EV/FCF`, `EV/Sales`; `P/B` for capital-heavy names). This shows the multiple *compressing as estimates grow* — information a single TTM number hides (Bernstein's ISRG cover showed Adj P/E 58.9× → 52.0× → 44.9× across F25A/F26E/F27E). The forward columns are `*Analyst view:*`; the last-actual column is sourced.
- **Relative-performance line.** Absolute price return over **1M / 6M / YTD / 12M** *and the same windows for the benchmark* (S&P 500 / sector ETF / CSI 300 / Hang Seng as fits the listing), plus the relative (stock − benchmark). Institutional notes lead with this — it tells the reader instantly whether the name is a sector-relative winner or laggard (Bernstein: ISRG −13.9% 12M absolute vs SPX +13.6% → −27.5% relative). Source the price data (yfinance / Eastmoney / Kabutan / etc.).
- **2–4 thesis pillars**, one sentence each — the call and why it works.

**Example (English report):**

```
> *Analyst view:* **Rating: Buy · 12-mo PT: $36 (+47% vs $24.50 spot) · Method: 70% rNPV-DCF (16% WACC) + 30% M&A value**
> Market cap $4.2B · 52-wk range $14–$31 · NASDAQ: COAG
>
> **Thesis pillars** — (1) Best-in-class bleeding-disorder pipeline with two Phase-3 assets; (2) under-appreciated FVIID optionality the Street hasn't modeled; (3) 16% WACC already prices in trial risk, leaving asymmetric upside; (4) takeout candidate at a 30% probability-weighted premium.
```

**Example (Chinese company, Chinese report):**

```
> *分析师观点：* **评级：Overweight（增持）· 12 个月目标价 HK$28.2（较现价 HK$19.2 上行 +47%）· 估值方法：2028E EPS × 40× P/E**
> 市值 HK$15.8bn · 52 周区间 HK$12–HK$24 · HKEX:1021
>
> **核心论点（thesis pillars）**——（1）领先的 cobot 核心零部件技术；（2）市场低估的 humanoid robot 零部件期权价值（2028E 占集团营收约 30%）；（3）渠道调研显示已切入 EngineAI/AGIBOT/Galbot 供应链；（4）40× 目标 P/E 对标 Howmet 的 37×，由更高的 EPS CAGR 支撑。
```

Derive every number in this block from Step 2b. If the company is private or genuinely un-targetable (pre-revenue, no comparable basis), state `Rating / PT: not applicable — <reason>` rather than inventing a number.

## Top-of-report banner — guidance changes (REQUIRED when present)

**Before the Table of Contents**, scan the latest earnings release / 业绩预告 / 业绩快报 / 季度报告 / 半年度报告 / 年度报告 / 8-K guidance update for any change to **full-year guidance** versus the prior outlook. If the company has:

- **Raised** full-year guidance (revenue, EPS, GM, or any disclosed full-year KPI), or
- **Cut** full-year guidance, or
- **Reaffirmed** guidance after a meaningful operating change, or
- **Initiated** guidance for the first time

→ open the report with a one-paragraph callout block highlighting the change. Use a `> **Update:**` blockquote so it visually separates from Section 1.

**Required content of the callout:**
- Direction (raised / cut / reaffirmed / initiated) + the specific metric and the old vs. new range
- The filing or call where it was disclosed (markdown link to the real URL)
- One sentence on the implied YoY change vs. the prior guide
- One sentence on the stated driver (management's words, briefly)

**Example (English-language report):**

```
> **Update — FY2025 guidance raised (2025-08-12):** Management raised full-year
> revenue guidance to USD 6.2–6.4B (from USD 5.9–6.1B) and raised non-GAAP
> EPS to USD 4.10–4.25 (from USD 3.85–4.00) on the back of stronger
> data-center demand and a faster H200 ramp.
> Source: [Q2-FY2025 earnings press release, 2025-08-12](https://...).
```

**Example (Chinese company, English report):**

```
> **Update — 上调 FY2025 全年业绩指引 (2025-08-15):** 公司将 2025 年营收
> 指引上调至 RMB 12.5–13.0 bn (原 RMB 11.5–12.0 bn)，归母净利润指引上调
> 至 RMB 2.1–2.3 bn (原 RMB 1.85–2.0 bn)，主因机器人业务订单加速及
> Tier-1 客户放量。
> Source: [2025 年半年度业绩预告, 2025-08-15](https://static.cninfo.com.cn/...).
```

If there is **no recent guidance change** to highlight, omit the banner entirely — do not add a placeholder. Guidance that's purely a re-affirmation with no new color isn't worth the banner.

## Section word counts and content

### 1. Company Overview (800–1,200 words)
- **Investment thesis lead paragraph (REQUIRED, first paragraph — BLUF house style).** Before any "what the company does" prose, open with the call: restate the rating + 12-month PT + upside%, the why-now, and the 2–4 thesis pillars in flowing sentences (the header block above is the at-a-glance version; this is the narrative version). Mirrors the Deutsche Bank / J.P. Morgan note that opens with "Buy, TP HK$28.2" + three bolded sub-heads rather than a description. Labeled `*Analyst view:*` / `*分析师观点：*`; the descriptive overview follows it.
- What does the company do? (plain English)
- How do they make money? (business model)
- Where do they operate? (geographic presence)
- How large are they? (revenue, employees, customers)
- Key metrics and scale indicators
- **IR primary input:** Latest 1–2 quarterly earnings deck (revenue + margin bridge slide, segment-mix slide, capital-allocation slide). At least one citation in this section should be to a recent earnings-deck slide; cite the slide number explicitly.
- **Valuation snapshot (REQUIRED).** Current price, market cap, **TTM P/E**, **TTM P/S** (plus P/B for capital-heavy businesses and EV/EBITDA for leveraged / cyclical names). Include the 3-year range of each multiple and the sector / peer median (3–5 named comps) so today's number has context. Cite the market-data source (Yahoo Finance / Eastmoney / Kabutan / DART, etc.) with a direct URL.
  - **If P/E is negative** → state why: cash-burning growth, one-off charge (impairment, litigation, write-down), cyclical trough, or structural decline. Name the specific income-statement line driving the loss and cite the filing.
  - **If P/E > 50× TTM (or > 2× sector median) or P/S > 15× (or > 3× sector median)** → name the cause: high-growth sector premium (AI infra, GLP-1, EV battery, advanced packaging — say which), temporarily depressed earnings, narrative / sector-proxy premium, M&A speculation, or small-float distortion. **Cite evidence — start with the local zsxq broker note surfaced in Step 0.7** (the Street's own PT / valuation-basis line, labeled `*Analyst view:*` and cited to `/zsxq/pdf/<file_id>/<filename>`), then earnings-call language, a peer that re-rated similarly, or sector ETF flows. This is the Section 2 zsxq citation the density bar calls for. Do not leave the multiple unexplained.
  - **If P/E < 8× or P/S is unusually low** → say whether it's a value trap, cyclical peak, governance concern, or genuine mispricing.
  - For private companies, substitute the latest funding-round post-money valuation and implied revenue multiple if disclosed; if not, state "private; no disclosed valuation."

### 1A. Valuation & Price Target (500–900 words) — the decision layer

A dedicated chapter, distinct from the Section 1 TTM snapshot (which is backward-looking). This is the forward, decision-grade analysis that mirrors every institutional analog. Built from Step 2b. **Everything in this chapter is the analyst's own forward view — every projected number, the PT, and the scenario PTs are labeled `*Analyst view:*` / `*分析师观点：*` and NEVER carry a filing citation.** Cite the *inputs* to each projection (filing segment data + management guidance + an industry forecast) inline; never write `(Source: our model)`.

**(a) Forward financial-estimates table (REQUIRED) — 3 years out (5 if the model supports it).** Revenue, gross margin, operating-or-net margin, EPS, per year, with YoY growth — **plus a cash-flow / balance-sheet layer: an FCF (or FCF yield) row and a net cash/(debt) row for all names, and for loss-making companies a cash-runway line (quarters, at current burn)**. Broker initiations always carry this layer (the GS Tinavi model forecasts FCF yield, net debt/equity, working-capital days alongside EPS) — for cash-burning names the decision variable IS the runway, not the EPS path. Cash/debt comes from the latest balance sheet and burn from the cash-flow statement (cited inline); projected cells stay `*Analyst view:*`. When the company guides quarterly, a next-4-quarters revenue/EPS path is recommended (not required). Model the **segment mix shift** — each business line its own revenue path + margin trajectory, then summed (the Tesla 6-way / Horizon licensing→hardware pattern) — not a single blended top-line. Tie each margin move to a driver (mix shift / operating leverage / pricing power). Template:

```
| Metric (*Analyst view:*) | FY24A | FY25E | FY26E | FY27E | CAGR |
|---|---|---|---|---|---|
| Revenue (RMB mn)         | 2,900 | 4,100 | 6,800 | 11,300 | +57% |
|   — YoY %                |       | +41%  | +66%  | +66%   |      |
| Gross margin %           | 36%   | 38%   | 41%   | 43%    |      |
| Operating margin %       | 8%    | 11%   | 15%   | 19%    |      |
| Net margin %             | 12%   | 14%   | 18%   | 22%    |      |
| EPS                      | 0.35  | 0.62  | 1.40  | 2.90   | +102% |
| ROIC %                   | 9%    | 11%   | 14%   | 17%    |      |
| FCF (RMB mn) / FCF yield | −120  | −60   | 180   | 640    |      |
| Net cash/(debt) (RMB mn) | 850   | 790   | 920   | 1,480  |      |
| [loss-makers] Cash runway (qtrs @ current burn) | … | | | |  |
```
(Each projected cell's basis cited inline: e.g. revenue ramp from the company's order-backlog disclosure + management's 2030 guidance + an industry-forecast number — all real, sourced inputs, with the projection labeled analyst view.) **Include a CAGR column and an ROIC row** — institutional models always carry both (Bernstein's ISRG model headlined Revenue/Operating-Earnings/Net-Earnings CAGRs + ROIC right on the cover).

**Granularity & the margin bridge (institutional depth — the Bernstein ISRG 4Q25 model).** Where the data supports it, carry the trailing **~4–8 quarters alongside the annual columns** (institutional models run quarterly *and* annual, line-itemized by revenue segment) — the quarterly cadence is what lets a reader see the inflection, not just the annual endpoints. And add a one-row-per-driver **margin bridge** that decomposes the YoY gross-margin / operating-margin change into named drivers with their **bps magnitudes** — e.g. `GM −110bps = tariffs −95bps · higher dV5/Ion mix −40bps · facility depreciation −30bps · product-cost reductions +55bps`. "Margins improve" without the bridge is not analysis. Each driver traces to a filing / earnings-call statement cited inline; the projected bps are `*Analyst view:*`.

**(b) Price-target derivation (REQUIRED) — show the arithmetic.** State the method and walk estimate → PT:
- **Forward-PE × target multiple:** `<FY27E> EPS × <target>x = <PT>`. **Justify the multiple against 3–5 named comps** (the J.P. Morgan Yingliu-40x-vs-Howmet-37x move, defended on a 55%-vs-23% EPS-CAGR gap). A multiple with no comp justification is not a derivation.
- **DCF:** WACC = Rf + β × ERP; **Rf = the 10Y from `indicators.db`** (reuse the Section-10 wiring; state the as-of date), ERP stated, terminal growth ≤ Rf. Show the intrinsic-value range and margin of safety vs. market cap.
- **SOTP:** value each segment on its own multiple, sum, reconcile to per-share.
- **rNPV (biotech):** risk-adjust each asset's peak sales by an explicit probability-of-success; state the PTS and the weighting (e.g. GS Hemab: 70% rNPV-DCF + 30% M&A value).

**(c) Bull / base / bear scenario table (REQUIRED) — three PTs, each tied to its swing assumption.** Base = central estimates; bull = faster attach / penetration or a higher multiple; bear = price war / margin compression. Report upside / downside % on each (the Morgan Stanley Hesai $53 / $30 / $11.5 and Citi Yunnan-Energy 3-scenario pattern). Template:

```
| Scenario (*Analyst view:*) | Key assumption | PT | vs spot |
|---|---|---|---|
| Bull  | Auto attach ramps to 80%, multiple holds 28× | $53 | +162% |
| Base  | Central estimates, 22× on 2027E EPS         | $30 | +48%  |
| Bear  | Price war compresses lidar GM to floor, de-rate to 12× | $11.5 | −43% |
```

**(d) Consensus benchmark (when sourced material carries it).** State where the report's forward estimates sit vs the Street (above / below, by how much) — the UBS / Nomura "+16% vs Street" move. Source the consensus figure to the zsxq broker note (`*Analyst view:*`, `/zsxq/pdf/<file_id>/<filename>`) or a dated public source; **never invent a consensus number.** When the company gives forward guidance, present this as a **Guide vs Consensus vs Own-estimate table** (the Bernstein Exhibit-1 format) — one row per guided metric:

```
| Metric (FY26E)   | Company guide | Consensus | This report (*Analyst view:*) |
|---|---|---|---|
| Procedure growth | 13%–15%       | 15.2%     | 15.1% |
| Gross margin     | 67%–68%       | 67.2%     | 67.5% |
| Opex growth YoY  | 11%–15%       | 14.1%     | 13.7% |
| EPS              | —             | $10.02    | $10.11 |
```
The company-guide column cites the earnings release; the consensus column is `*Analyst view:*` sourced to the zsxq note / a dated public source; the "this report" column is the analyst's own forward view.

**(e) Swing variables.** Name the 1–2 assumptions the call hinges on (MS Hesai: lidar-GM floor + auto attach rate), so the reader knows what to pressure-test.

**(f) On a refresh, decompose what changed (estimate-revision transparency).** Institutional notes track their own revisions in the open — when updating an existing report, state the prior figure beside the new one (`PT $750 (was $740)`, `FY27E EPS $11.72 (was $11.61)`) and **attribute the PT move to its components: how much came from the estimate change vs. the multiple change.** Bernstein's $750 = 64× (unchanged) × a raised FY27E EPS — so the entire PT increase was the estimate, not a re-rating; saying so tells the reader the call is earnings-driven, not multiple-driven. All `*Analyst view:*`.

**IR / zsxq input:** the broker notes from Step 0.7 supply the Street's PT, valuation basis, and bull/bear to benchmark against — cite them `*Analyst view:*`. This is the Section 2 zsxq citation the SKILL density bar calls for.

### 1B. GF Score (GuruFocus-style) fundamental scorecard (350–600 words) — the at-a-glance health read

A compact five-axis scorecard — modelled on [GuruFocus's GF Score™](https://www.gurufocus.com/term/gf-score) — that distils the fundamentals into one **0–100 composite** plus a **radar/pentagon**. It sits here, right after 1A, so the whole decision layer (rating/PT → valuation → fundamental scorecard) reads together near the top, like the GuruFocus summary widget. **It is an analytical overlay on data already gathered, NOT a new data source and NOT an endorsement** — the five sub-scores and the composite are `*Analyst view:*` / `*分析师观点：*`; every underlying metric carries its own inline citation. Full rubric, the 0–10 anchors per axis, weights, band labels, and the honesty rules are in **[`references/gf_score.md`](gf_score.md) — read it before writing this section.** Include in every initiation-style report unless the user says "skip the GF Score".

**The five axes (each 0–10):** Financial Strength (财务实力) · Profitability (盈利能力) · Growth (成长性) · GF Value / valuation (估值，*higher = cheaper vs fair value*) · Momentum (动量). Their inputs are already in your tree: Financial Strength + Profitability from the filings (Section 1 / Step 1–2), Growth from the Section-1A forward model, GF Value from the Section-1 multiples + Section-1A intrinsic range, Momentum from the header's relative-performance line.

**Required content, in order:**
1. **Verdict line** — `*Analyst view:* **GF Score (GuruFocus-style): NN/100 — <band>.**` Optionally append GuruFocus's real number as a *separate* cross-check if you actually pulled it from `gurufocus.com/term/gf-score/<TICKER>` (never merge the two).
2. **The radar `<svg>`** from the helper (`scripts/gf_score.py`, inline SVG — paste it un-fenced so it renders) + the one-line how-to-read note (*farther from centre = better; bigger pentagon = higher score*).
3. **The 5-row scorecard table** from the helper (per-axis 0–10 + composite row).
4. **Per-dimension rationale — one short paragraph per axis stating WHY that score**, naming the 2–4 metrics that drove it, each with its inline citation (ROE / margins / leverage → filing page; multiples → market-data URL; price returns → yfinance / `indicators.db`). *A score with no reasons behind it is not acceptable — this is the part the reader most wants.*
5. **Composite arithmetic line** — `(FS·20 + Prof·25 + Growth·25 + Value·15 + Mom·15)/100 → NN/100`, with the weights used (default 20/25/25/15/15; state any deviation).
6. **One-line caveat** — the axis most likely to flip, and any `n/a` axis.

**Consistency:** the Growth axis must agree with the Section-1A forward model, GF Value with the Section-1 multiples + the PT's implied upside, Momentum with the header relative-performance line. A GF Score that contradicts the report's own numbers is a defect. Generate the helper's `--source` from the same filings/market-data the rationale cites.

### 2. Company History (400–700 words)
- Founding story (who, when, why, where) — 1 short paragraph
- Mermaid `timeline` block covering 5–10 major milestones (replaces a prose recap of every dated event)
- 2–3 strategic pivots or transformations, each in 1–2 sentences explaining the *why*, not just the *what*
- Key acquisitions (bullet list with year + rationale)
- Recent developments (last 1–2 years) — keep tight; details that affect the current thesis can move to Section 4 / 5 / 7 / 8 instead of bloating history.

### 3. Management Team (300–500 words)
**Cover the founder and the current CEO only — nothing else.** No CFO, no other executives, no governance footer, no track-record synthesis. Keep this chapter tight.

- **Founder bio: 200–300 words.** Prior 2–3 roles with *what specifically they accomplished* (numbers, not titles), education, founding thesis, ownership stake today, and whether still operationally involved.
- **Current CEO bio: 200–300 words.** Same depth: prior 2–3 roles with concrete accomplishments, education, tenure at this company, ownership stake, comp structure.
- **If founder is still CEO, write one combined bio (300–450 words)** — don't split into two.

### 4. Products & Services (700–1,500 words) — **THE most important section of the report**

> **Priority note:** Section 4 is the single most consequential chapter of the entire research report — see SKILL.md § "The Products & Services chapter is the most important section of the report" for the full rationale. **A weak Section 4 cannot be recovered by polishing the other sections.** Sections 5 (Customers), 6 (Industry), 7 (Competition), 8 (TAM), and 9 (Risks) all reference back to *what the company makes and how it sits in the customer's workflow*; if Section 4 is generic, every downstream section becomes hand-waving. Budget your time and word count accordingly: this section deserves more research effort than any other.

**Two requirements: precise and explanatory.**
- *Precise* = anchored to the issuer's own product matrix (embedded as an image + reproduced as markdown), with verbatim 10-K quotes for each product family, exact product names with trademark symbols, and competitor / share / leadership claims clearly labeled as analyst view (not attributed to the 10-K).
- *Explanatory* = for each product, three pedagogical beats (what it physically does → how it differs from sibling products → strategic inflection driving demand); bilingual technical terminology (Chinese AND English side-by-side) for cross-border-investing audiences; a synthesis paragraph at the end showing how the product categories compose a single customer workflow.

This is the section where reports most often degrade into either a flat product catalog or sell-side commentary dressed up as fact. Use the following structure to avoid both failure modes.

**(a) Anchor to the issuer's own product matrix.**

Most semiconductor / industrial / hardware / pharma issuers publish a product matrix in the 10-K / 年度报告 / Yuho Item 1 Business section — typically organized as Market → Process/Application → Technology → Products (or an equivalent for the industry: Therapeutic Area → Indication → Modality → Product, etc.).

**What must appear in 4.1:**
  1. **A verbatim markdown reproduction of the issuer's table (MANDATORY)**, with the 10-K citation directly above it — searchable, accessible to screen-readers, and quotable so product names can be linked.
  2. ***Optionally*, the 10-K's actual rendered table as a PNG image** (`![…](charts/<ticker>_10k_products_table.png)`, rendered with the helper script below, caption citing the 10-K) when visual proof of the primary anchor adds value. The PNG never substitutes for the markdown reproduction.

If the issuer does not publish such a table, build one from the website's product navigation (citing the website) and label it explicitly as analyst-constructed.

**(b) Walk each row with verbatim 10-K quotes + bilingual pedagogy.**

For each product family in the matrix, follow this exact three-part pattern:

  1. **10-K verbatim (block quote).** Quote the 10-K's Product Family description directly — use `> "…"` markdown block-quote syntax with the inline 10-K citation right above the quote. Verbatim text from the issuer is by definition non-fabricated and gives the reader Lam's own explanation of what the product does.
  2. **Bilingual pedagogical explanation** introduced with the label `**中文释义 / Plain-language gloss:**`. Clearly labeled as the analyst's plain-language gloss, *not* attributed to the 10-K. This is where the analyst earns their pay: explain in 3–6 sentences (a) the underlying physics / process / mechanism using analogies where helpful, (b) how this product differs from its sibling products in the same matrix, and (c) the strategic inflection currently driving demand.
     - **For every technical term, give both Chinese AND English side-by-side** in the form `Chinese / English` or `English / Chinese` or `Chinese (English)`. Examples: `dielectric / 介质`, `通孔 (via)`, `wordline / 字线`, `CMP (chemical-mechanical planarization, 化学机械抛光)`, `gate-all-around (GAA, 栅极环绕)`. This serves bilingual readers (often the same reader: a Chinese-native analyst working in English-speaking firms, or vice versa) and prevents either-language vocabulary gaps from blocking comprehension.
     - **Code-switching freely is fine** — sentences can start in one language and end in the other, e.g., "SABRE 做的是 **电镀铜 / Cu electroplating (ECD)** —— 通过 electrochemical reaction 把 copper 长在 wafer 上, forming the **互连线 / interconnect**…". This compressed style is denser than either monolingual version because it leverages each language's strengths: Chinese for compact process names, English for proper-noun technologies and IUPAC chemistry.
     - For non-Chinese-reading audiences (e.g. company-research reports targeting US-domestic-only consumers), you may use the heading `**Plain-language gloss:**` alone and skip Chinese — but for any cross-border-investing context (any Chinese-listed company, any US semicap/EV/battery/biotech name with significant Chinese supply chain) the bilingual form is preferred.
  3. ***Analyst view:* sentence** — competitive context only, cited to the competitor's filing or website or a third-party research source, never to the subject's 10-K. Specific competitor product names (e.g. AMAT's NOKOTA, Producer, Endura) belong here.

**(c) End the section with a synthesis paragraph that shows how the product categories interact.** This is what makes a research report *pedagogical* rather than a catalog. For semicap, it's the Deposition → Etch → Clean → Deposition manufacturing cycle. For other industries, the equivalent: how the products compose a single customer workflow / use case / treatment regimen / installation. One paragraph; 3–5 sentences; explicit about which products sit at each step. Optionally include a small Mermaid LR or TD graph showing the loop.

**(d) Required elements regardless of structure:**
  - **Per-product competitive-advantage assessment.** For each material product, a one-clause verdict (yes / partial / no) plus the moat type (technology / IP / patents, scale, switching costs, network effects, regulatory, distribution, ecosystem lock-in) — under the `*Analyst view:*` label.
  - **Flagship vs. long-tail.** Identify the 1–3 products driving the current business (state revenue / unit-mix share if disclosed; otherwise flag as analyst estimate).
  - **Roadmap & recent launches.** Products launched, repositioned, or sunset in the last 12 months — with the company press release as the citation. If a new platform was launched (e.g. Akara, ALTUS Halo), block-quote the press release the same way you block-quote the 10-K.
  - **Recurring / aftermarket / services business.** Many issuers have a separate business group outside the product matrix (CSBG for Lam, Services for AMAT, etc.). Treat that as its own subsection — describe what it consists of, how it's reported in the financials, why it dampens cyclicality, and the recurring-revenue economics.
  - **IR primary input:** Section 4 should draw from the investor day deck's product / roadmap slides, the latest earnings deck's product-segment slides, and any industry-conference deck where the CEO walked product roadmap. **At least 2 IR-deck citations in Section 4** when the company publishes IR materials — typically the latest investor day deck (roadmap and TAM slides) plus the latest quarterly deck (segment-mix slide). Block-quote the slide text when the company's own framing is load-bearing, the same way you block-quote the 10-K.
  - **延伸观看 / Further viewing** — 1–3 validated explainer videos for hard-to-visualize concepts (a humanoid robot's harmonic reducers, an etch–deposition flow, HBM die-stacking, a surgical-robot wrist), in their own slot at the end of the section, never a citation and never carrying a number (see SKILL.md § "延伸观看 / Further viewing" and `references/citations.md`).

**Rendering the issuer's product table as a PNG (for step (a))**

A reusable helper script lives at `.claude/skills/company-research/scripts/render_10k_section.py`. It takes a local 10-K HTML path, an anchor string (any unique text inside the target element — usually a product name), and an output path; it screenshots the located element at retina resolution and saves a PNG.

**One-time setup** (skip if playwright is already installed in the project):

```bash
pip install playwright
/opt/anaconda3/bin/python3 -m playwright install chromium
```

**Usage:**

```bash
# Default: anchor by a product name inside the target <table>
/opt/anaconda3/bin/python3 .claude/skills/company-research/scripts/render_10k_section.py \
    --html financial_reports/LRCX/<10-K-filename>.htm \
    --anchor SABRE \
    --output reports/company/<Slug>/charts/<ticker>_10k_products_table.png

# Or: specify a CSS selector directly
/opt/anaconda3/bin/python3 .claude/skills/company-research/scripts/render_10k_section.py \
    --html financial_reports/<TICKER>/<10-K-filename>.htm \
    --selector "table.products" \
    --output reports/company/<Slug>/charts/<ticker>_10k_products_table.png \
    --pad-top 150  # extra header padding if the section title doesn't fit
```

**How it works internally:**
1. Launches headless chromium via playwright.
2. Loads the local 10-K HTML file via `file://` URL — works with the HTML SEC EDGAR serves; no network round-trip needed since the file is cached locally by `fetch_financial_report.py`.
3. Locates the target element either by `--anchor` (text-content filter on `<table>`) or by `--selector` (CSS selector).
4. Calls `page.screenshot(clip=bounding_box + padding)` to crop just the element + small padding to include the section heading and any caption.
5. Saves at `device_scale_factor=2` (retina) for crisp PNGs.

**Choosing a good anchor.** Pick a unique product or product-family name that appears only inside the target `<table>` — e.g. for Lam's product table, `SABRE` works because it's a unique product family. For Apple, `iPhone` would be too generic (appears across many tables); use a more specific anchor like `Mac Studio` or a sentence from a unique paragraph. If no unique anchor exists, fall back to `--selector` with a CSS path.

**For Chinese 年度报告 (cninfo PDFs)**, use `fitz` (PyMuPDF) to render the relevant page to PNG instead — see the project's `render_pdf_pages.py` pattern. The helper script above is HTML-only.

Save all rendered PNGs into `reports/company/<Slug>/charts/` so the relative `![](charts/...)` reference resolves from the markdown report.

**Example structure (semiconductor capital equipment, mixed English / Chinese in the body, used for the LRCX report):**
```
4.1 The 10-K product matrix [PNG embed of 10-K rendered table + verbatim markdown reproduction]
4.2 Synthesis — how the categories interact [3–5 sentence narrative + small Mermaid LR graph]
4.3 Deposition [for each product family: 10-K block quote → 中文释义 → *Analyst view:*]
4.4 Etch [same pattern, per product family]
4.5 Clean [same pattern]
4.6 [Recurring service business — CSBG / Services / aftermarket]
4.7 Flagship franchises and recent launches
```

**Adapting for non-semicap industries:**
- For **pharma / biotech**, group by Therapeutic Area; block-quote the 10-K's product narrative for each marketed drug; the pedagogical color explains the mechanism of action, the patient population, the position vs SoC.
- For **industrial automation / robotics**, group by Cell / Line / Plant level; block-quote the product-family description; the pedagogical color explains where in the customer's workflow the product sits and what it integrates with.
- For **fintech / SaaS**, group by use case; block-quote the 10-K's customer / segment narrative; the pedagogical color explains what category of work this software replaces and what the API surface looks like.

The pattern (issuer's own table → verbatim quote → analyst-labeled pedagogical gloss → analyst-labeled competitive view → synthesis at the end) is industry-agnostic.

### 5. Customers & Go-to-Market (500–800 words)
- Customer segments and profiles
- **Customer concentration (REQUIRED).** Quantify top-1 and top-5 customer share of revenue from the latest annual filing, plus the 3-year trend if available. Name the top customers when disclosed. Cite the specific filing section (e.g. `年度报告` § 前五名客户, 10-K segment note, Yuho `主要な販売先`). State the contract structure (master agreement vs. PO-by-PO, multi-year vs. annual) and whether any top customer is also a competitor / vertically integrating. **If top-1 > 20% or top-5 > 50%, flag it explicitly here and carry it into Section 9 as a material risk.** If the company does not disclose, say so — do not skip.
- **NEVER mix segment-level customer concentration with consolidated / group-level customer concentration.** Every customer-share number must be labelled with its denominator ("X% of consolidated revenue" vs "X% of <Segment> segment revenue") — never an unqualified "X% of revenue" when more than one denominator could apply. Segment-level customer lists must carry a "(segment-level; not aggregated to group-level)" qualifier inline. A customer pie chart must use one denominator only — do not draw a single chart whose slices mix consolidated and segment-level shares. The filing's named top-5 (e.g. Samsung's 사업보고서 alphabetical list at ~14% group aggregate) overrides any reconstructed sell-side / supply-chain composite that disagrees. See the SKILL.md "Customer concentration" rule for the full spec and the Samsung-2024 worked example.
- **IR primary input:** IR decks often name customers the filing only references by category (e.g. "a leading hyperscaler"). Pull customer-logo slides, customer-cohort retention charts, geographic-mix Sankeys, NRR cohort charts from the latest investor day deck and recent quarterly decks — typically 1–2 IR citations in this section.
- Distribution channels
- Sales strategy and cycle
- Key partnerships
- Customer case studies (named wins)

### 6. Industry Overview (800–1,200 words)
- Industry definition and scope
- Market size and structure
- Growth rates (historical and projected)
- Key trends and drivers
- Regulatory environment
- Industry dynamics (fragmentation, supplier/buyer power, substitutes)
- **IR primary input:** Management's industry framing — every IR deck has 2–4 slides setting up the industry context (often clearer than the company's own filing). Pull these from the latest investor day deck and key industry-conference appearances. At least 1 IR citation here.

### 7. Competitive Landscape (700–1,000 words)
- Analysis of 5–10 key competitors (direct, indirect, emerging)
- Market positioning framework (price / features / scale dimensions)
- Company's competitive advantages
- Competitive vulnerabilities
- Market share analysis
- **IR primary input:** Investor day "Why we win" slides, side-by-side feature matrices, share-trajectory charts. **Handle with care** — these slides are self-serving by design — but the underlying data points are citable, and the *omission* of a key competitor on a competitive-positioning slide is itself signal. Often 1 IR citation here.

### 8. Market Opportunity / TAM (500–700 words)
- TAM sizing and methodology
- SAM and SOM
- Market growth projections
- Company's serviceable market and share opportunity
- Penetration strategy
- **IR primary input — most-cited source in this section.** The IR deck's TAM build slide is almost always the most-cited single TAM source in the report; management has done the build-up work and chained-cited the underlying research firm (Yole, Gartner, IDC, etc.). Cite the deck as primary with a source-chain label (e.g. `[Company Investor Day 2024 deck, Slide 23 — TAM (citing Yole 2024)](URL)`); chain-cite the underlying research firm as secondary. **Minimum 2 IR citations in Section 8** for any issuer that publishes a TAM build — typically the latest investor day deck plus the latest annual / Integrated Report.

### 9. Risk Assessment (600–900 words)
- 8–12 distinct risks across 4 buckets (see `risk_taxonomy.md`)
- 50–100 words per risk: describe, quantify impact if possible, note mitigants
- Cover all four categories
- **Bear case from the local zsxq library.** Where the library has coverage (Step 0.7), ground at least one risk in the analyst's own framing — what the skeptics actually worry about (e.g. memory price cuts, China demand, ASIC encroachment) and the specific trigger — labeled `*Analyst view:*` and cited to `/zsxq/pdf/<file_id>/<filename>`. This is the Section 9 zsxq citation the SKILL density bar calls for.

### 9.5. Key debates & catalysts (300–600 words) — defend the thesis, then list the triggers

Distinct from the Section 9 risk *inventory*: Section 9 catalogues the downside taxonomy; **9.5 defends the thesis against the specific arguments the bears make** (the Morgan Stanley 市场核心分歧 / Hesai three-debate pattern) and lists the dated forward triggers. See SKILL.md § "Learning from sell-side institutional research".

- **Key debates (2–4).** For each: the bear's argument in one sentence, then the analyst's rebuttal with cited evidence. Format as `**Debate 1 — <one-line bear claim>.** *Analyst view:* <rebuttal + citation>.` Ground at least one in the local zsxq bear case where coverage exists (Step 0.7), labeled `*Analyst view:*` and cited to `/zsxq/pdf/<file_id>/<filename>`.
- **Catalyst calendar (next 12 months).** A dated list of forward triggers — earnings prints, product launches, trial readouts, capacity milestones, regulatory decisions, contract wins (the GS Hemab "Phase-3 start H2-26, FVIID data late-26" / Bernstein catalyst-calendar pattern). Each entry: `<approx date> — <event> — <why it moves the thesis>`. Point the reader to the `catalyst-calendar` skill for ongoing tracking.

Keep the risk taxonomy itself in Section 9 — debates defend the thesis, the catalyst list is forward triggers, the risk inventory is the downside map. Do not duplicate; cross-reference where they touch.

### 10. Investor-lens scorecards (optional — 600–2,500 words depending on lens set)
- Skip only when the user has explicitly said "no lens scorecards" / "skip Section 10".
- Open with a one-paragraph cycle snapshot from `indicators.db` (VIX, 10Y Treasury, HY OAS) — state the as-of date; this snapshot feeds the company-specific lenses.
- **Default (core four, 600–1,000 words total):** ~150–250 words each — **10.1 Buffett scorecard**, **10.2 Munger scorecard**, **10.3 Damodaran scorecard**, **10.4 Howard Marks cycle posture**.
- **Optional packs (10.5–10.9, +150–250 words each):** add when the company fits per `investor_lenses.md` § "Implementation tips" routing rules — **10.5 Lynch GARP** (mid-cap growers), **10.6 Fisher scuttlebutt** (compounders with qualitative evidence), **10.7 Burry forensic deep value** (hated sectors / suspected value traps), **10.8 Druckenmiller liquidity-regime** (macro-sensitive setups), **10.9 Cathie Wood Wright's Law** (disruption stories where DCF breaks).
- Each subsection: bolded verdict line → 3–5 row scorecard table → 2–3 sentence evidence chain (re-using citations from Sections 1–9) → per-lens required block (Damodaran assumptions / Munger inversion / Lynch category / Fisher scuttlebutt note / Burry downside-first / Druckenmiller macro context + exit trigger / Cathie Wood Wright's Law math + convergence) → one-sentence failure mode.
- Verdicts use the `*Lens view:*` / `*视角观点:*` label. Never `Buffett would buy`, `Lynch would chase`, `林奇会买`, `Burry would short`, `Damodaran's fair value is`, `Cathie Wood projects X`.
- See `investor_lenses.md` for the nine rubrics, verdict bands, required-block specs per lens, and the picking-by-company-type table.

### Data Used / 数据来源清单 (mandatory at the end of the body, before References)
A short structured manifest of what data this report stands on — separate from the inline citations, which prove *where* each claim came from. The manifest answers *what categories of evidence the analyst pulled at all*, which periods they cover, and what's missing. 8–15 bullets. Format:

```markdown
## Data Used / 数据来源清单

**Primary filings**
- 10-K FY2024 (filed YYYY-MM-DD), 10-Q Q3 FY2024 (filed YYYY-MM-DD), DEF 14A 2024 (filed YYYY-MM-DD); recent 8-Ks YYYY-MM-DD to YYYY-MM-DD. Source: SEC EDGAR.
- [or for non-US:] 年度报告 2024 (filed YYYY-MM-DD), 半年度报告 (filed YYYY-MM-DD), 業績說明會 PPT YYYY-MM-DD. Source: cninfo (巨潮).

**Investor-relations materials**
- Q3 FY2024 earnings deck (released YYYY-MM-DD); Investor Day YYYY deck; Q3 transcript YYYY-MM-DD. Source: company IR site.
- (Japan / Korea only) Integrated Report YYYY (統合報告書, released YYYY-MM-DD); Mid-term Plan YYYY-YYYY (中期経営計画).

**Market data**
- TTM P/E, P/S, P/B, EV/EBITDA as of YYYY-MM-DD. Source: Yahoo Finance / Eastmoney / Kabutan / Naver Finance.
- Peer multiples (N=3–5 names) as of YYYY-MM-DD. Source: same.

**Third-party research**
- Gartner CDW Magic Quadrant YYYY (published YYYY-MM-DD); Yole Wafer Equipment Forecast YYYY (published YYYY-MM-DD); IPnest Design IP YYYY (published YYYY-MM-DD); etc.

**Institute research (local `db/zsxq.db`)**
- Searched N aliases (ticker / English / 中文); used M broker notes (Morgan Stanley / Goldman / J.P. Morgan / Bernstein / …) dated YYYY-MM-DD to YYYY-MM-DD. **Each file_id is itself a clickable direct-download link** — one bullet per note, formatted `` [`<file_id>` — <broker>：<title>, <date>](<pdf_url>) `` (paste `find_pdf.py`'s `pdf_url`; never leave bare file_id numbers — user feedback 2026-06-10). Labeled *Analyst view:* throughout. (Or: "no local coverage even after a `--query` top-up.")

**Macro / cycle inputs (Section 10 only)**
- 10Y Treasury yield (`^TNX`) snapshot as of YYYY-MM-DD; HY OAS (FRED BAMLH0A0HYM2) snapshot as of YYYY-MM-DD; VIX snapshot as of YYYY-MM-DD. Source: `indicators.db` (FRED + yfinance).

**Stale notices / coverage gaps**
- <bulleted list of inputs the analyst tried to pull but couldn't, or that returned data older than 12 months; or "none" if all inputs are fresh>.
- E.g.: "Top-1 customer % not separately broken out in Q3 10-Q; relied on FY2023 10-K disclosure (>12 months old)."
- E.g.: "Industry TAM source (Yole 2026 forecast) paywalled; cited management's TAM build from Investor Day deck instead."
```

The manifest sits between Section 10 (or Section 9 if Section 10 is skipped) and the References block. It is **not** a substitute for the References block — References list every URL cited inline; Data Used summarizes the *categories* of evidence and their freshness.

## Output Template

```
COMPANY RESEARCH REPORT: [Company Name]
Date: [YYYY-MM-DD]

> *Analyst view:* INVESTMENT SUMMARY — Rating: [Buy/Hold/Sell or OW/N/UW] ·
> 12-mo PT: [$X] ([+/−Y% vs spot]) · Method: [one-line] · Mkt cap [$] ·
> 52-wk [range] · [TICKER:EXCH]
>
> | 倍数 / Multiple (*Analyst view:* fwd cols) | FY-1A | FY1E | FY2E |
> |---|---|---|---|
> | P/E | … | … | … |
> | [+2–3 fitting: PEG / EV/EBITDA / EV/FCF / EV/Sales / P/B] | … | … | … |
>
> Rel. performance: 1M … · 6M … · YTD … · 12M … vs [benchmark] (relative: …) — [price source cited]
> Thesis pillars — (1) … (2) … (3) … (4) …
[Guidance-change banner here when applicable]

TABLE OF CONTENTS
1. Company Overview (incl. investment-thesis lead)
1A. Valuation & Price Target (forward estimates · PT derivation · bull/base/bear)
1B. GF Score (GuruFocus-style) fundamental scorecard (radar + 5-axis 0–10 + composite)
2. Company History
3. Management Team
4. Products & Services
5. Customers & Go-to-Market
6. Industry Overview
7. Competitive Landscape
8. Market Opportunity (TAM)
9. Risk Assessment
9.5. Key debates & catalysts
10. Investor-lens scorecards (optional)

======================================

1. COMPANY OVERVIEW (800–1,200 words)
[Investment-thesis lead paragraph first (*Analyst view:* — call + why-now + pillars),
 then the descriptive overview + TTM valuation snapshot.]

1A. VALUATION & PRICE TARGET (500–900 words)
[*Analyst view:* throughout, no filing citation on any projection/PT.
 (a) Forward financial-estimates table — revenue / GM / margin / EPS, 3 yrs out, with the inputs cited.
 (b) PT derivation showing the arithmetic — forward-EPS × target-multiple (justified vs 3–5 comps) / DCF / SOTP / rNPV.
 (c) Bull / base / bear PT table, each with its swing assumption + upside%.
 (d) Consensus benchmark (vs Street, when sourced).
 (e) The 1–2 swing variables the call hinges on.]

1B. GF SCORE (GuruFocus-style) FUNDAMENTAL SCORECARD (350–600 words)
[*Analyst view:* throughout — sub-scores + composite are the analyst's rubric, never a filing cite;
 every underlying metric carries its own inline citation. See references/gf_score.md.
 (1) Verdict line: GF Score NN/100 — <band> (optional separate GuruFocus-official cross-check).
 (2) Radar <svg> from scripts/gf_score.py (paste un-fenced) + how-to-read note.
 (3) 5-row scorecard table (Financial Strength / Profitability / Growth / GF Value / Momentum, each 0–10) + composite.
 (4) Per-axis rationale — one paragraph each stating WHY that score, with the driving metrics cited inline.
 (5) Composite arithmetic + weights (default 20/25/25/15/15). (6) One-line caveat / any n/a axis.]

2. COMPANY HISTORY (400–700 words)
[Content]

3. MANAGEMENT TEAM (300–500 words)
[Founder name]
[200–300 word bio — prior roles, founding thesis, ownership, current role]
[Current CEO name] — skip if same person as founder
[200–300 word bio — prior roles, tenure, ownership, comp]

4. PRODUCTS & SERVICES (700–1,500 words)
[4.1 Verbatim product matrix from the issuer's 10-K / 年报 / Yuho
     (Market / Process-Application / Technology / Products), cited.
 4.2 Synthesis paragraph: how the categories interact in a customer workflow.
 4.3-4.5 (per major market in the matrix): walk each product row with
   - what it physically does in the manufacturing / value-chain flow
   - how it differentiates from sibling products in the same matrix
   - strategic significance: technology inflection or customer wave driving demand
   - *Analyst view:* — competitive-advantage verdict + moat type +
     closest named competitor product (cited to competitor's filing or website,
     NOT the subject's 10-K).
 4.X Recurring / aftermarket / services group (CSBG-equivalent), if applicable.
 4.Y Flagship 1-3 franchises + last-12-months launches.
 4.Z **延伸观看 / Further viewing** — 1–3 validated explainer-video links
     (each HTTP-checked 200 with a browser UA, never carrying a number);
     or omit, with the reason stated in the verification log.]

5. CUSTOMERS & GO-TO-MARKET (500–700 words)
[Content]

6. INDUSTRY OVERVIEW (800–1,200 words)
[Content]

7. COMPETITIVE LANDSCAPE (700–1,000 words)
[Content]

8. MARKET OPPORTUNITY (500–700 words)
[Content]

9. RISK ASSESSMENT (600–900 words)
Company-Specific Risks:
[4–6 risks with descriptions]
Industry/Market Risks:
[3–4 risks with descriptions]
Financial Risks:
[2–3 risks with descriptions]
Macroeconomic Risks:
[2–3 risks with descriptions]

9.5. KEY DEBATES & CATALYSTS (300–600 words)
[2–4 bear arguments, each with an *Analyst view:* rebuttal + cited evidence;
 then a dated 12-month catalyst list (event → date → why it moves the thesis).
 Distinct from the Section 9 risk inventory — debates defend the thesis.]

10. INVESTOR-LENS SCORECARDS (optional — 600–1,000 words total)
[One-paragraph cycle snapshot from `indicators.db` (VIX, 10Y, HY OAS) as of YYYY-MM-DD.]
10.1 Buffett scorecard (verdict / table / evidence / failure mode)
10.2 Munger scorecard (verdict / table / inversion check / evidence / failure mode)
10.3 Damodaran scorecard (verdict / assumption block / table / evidence / failure mode)
10.4 Howard Marks cycle posture (verdict / component table / contrary evidence / failure mode)

======================================

DATA USED / 数据来源清单
[Structured manifest per the spec above — primary filings, IR materials,
 market data, third-party research, macro inputs, stale notices / gaps.]

======================================

REFERENCES
[Consolidated, deduplicated list of every source cited inline above,
 organized by source type, each entry with date and URL/local path.
 Vertical bullet lists only — one source per line, never `·`-separated
 run-on strings. Dated groups (news, broker notes) lead each bullet
 with `YYYY-MM-DD ·` and sort newest-first; undated evergreen pages
 (official site, wiki, market-data pages) carry an access date in the
 group heading. See citations.md § "Final References Section".]

======================================

<details>
<summary>Verification log (Step 10) — YYYY-MM-DD</summary>
[Step 10.6 log per SKILL.md — URL check · Step 0.5 disposition ·
 Further-viewing URLs · SEC filenames · 10-K spot-checks · analyst-view
 sentences · zsxq counts · residual unknowns. The <summary> line is the
 exact English string above, even in Chinese reports.]
</details>
```
