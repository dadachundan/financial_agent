---
name: thesis-tracker
description: Maintain and update investment theses for portfolio positions and watchlist names. Track key data points, catalysts, and thesis milestones over time. Use when updating a thesis with new information, reviewing position rationale, or checking if a thesis is still intact. Triggers on "update thesis for [company]", "is my thesis still intact", "thesis check", "add data point to [company]", or "review my positions".
---

# Thesis Tracker

**Language:** English-only by default (this is a tracking / monitoring skill, matching the project's tracking-skills English-default rule). Produce bilingual / Simplified-Chinese output only on explicit request (`in Chinese`, `bilingual`, `--lang zh`).

## Storage & persistence (MUST)

Cross-session persistence lives in markdown — one living file per position at `reports/thesis/<TICKER>_thesis.md` (create `reports/thesis/` if missing; English ticker first per the project filename rule). NEVER store thesis state in any project DB. Fixed file layout:

- **Thesis header block** — statement, pillars, risks, verdict-ladder definition, scenario grid, KPI-panel definition (Step 1)
- **Update Log** — append-only dated entries, newest first (Step 2)
- **Current scorecard + KPI panel** — re-printed in full on every check-in (Steps 3–5); consistency of the metric set is the whole value of the tracker

Markdown only — no Word output (the report viewer surfaces `.md`). Commit + push after every check-in (Conventional Commit, e.g. `feat(reports/thesis): ...`). Portfolio mode = enumerate `reports/thesis/*.md`.

## Workflow

### Step 1: Define or Load Thesis

If creating a new thesis:
- **Company**: Name and ticker
- **Position**: Long or Short
- **Thesis statement**: 1-2 sentence core thesis (e.g., "Long ACME — margin expansion from pricing power + operating leverage as mix shifts to software")
- **Key pillars**: 3-5 supporting arguments
- **Key risks**: 3-5 risks that would invalidate the thesis
- **Catalysts**: Upcoming events that could prove/disprove the thesis (earnings, product launches, regulatory decisions)
- **Target price / valuation**: What's it worth if the thesis plays out
- **Stop-loss trigger**: What would make you exit

If updating an existing thesis, load it by Reading `reports/thesis/<TICKER>_thesis.md` — never ask the user to restate the thesis — then process the new data point or development from the request (ask only if none was given).

### Step 2: Update Log

For each new data point or development:

- **Date**: When this happened
- **Data point**: What changed (earnings beat, management departure, competitor move, etc.)
- **Thesis impact**: Does this strengthen, weaken, or neutralize a specific pillar?
- **Action**: No change / Increase position / Trim / Exit
- **Updated conviction**: High / Medium / Low

### Step 3: Thesis Scorecard

Maintain a running scorecard:

| Pillar | Original Expectation | Current Status | Trend |
|--------|---------------------|----------------|-------|
| Revenue growth >20% | On track | Q3 was 22% | Stable |
| Margin expansion | Behind | Margins flat YoY | Concerning |
| New product launch | Pending | Delayed to Q2 | Watch |

**Optional — GF Score health row.** Beneath the pillar scorecard, track a **GF Score (GuruFocus-style): prior → current** line (the five-axis fundamental composite, 0–100) so fundamental health is trended alongside the thesis pillars — e.g. "GF Score 65 → 72 (+7) since last check, driven by the Profitability + Momentum axes." Re-print the **same five axes every check-in** (metric-set consistency is the whole value of a tracker). Spec + radar helper: [`reference/gf_score.md`](reference/gf_score.md); sub-scores are `*Analyst view:*`, never attributed to GuruFocus.

### Step 4: Catalyst Calendar

Track upcoming catalysts:

| Date | Event | Expected Impact | Notes |
|------|-------|-----------------|-------|
| | | | |

### Step 5: Output

Thesis summary suitable for:
- Morning meeting discussion
- Portfolio review
- Risk committee presentation

Format: concise markdown (no Word) — each check-in updates `reports/thesis/<TICKER>_thesis.md` in place per the Storage & persistence rules above, re-printing the scorecard, recent updates, and current conviction level.

### Step 6: Verify & log

Before committing each check-in:

1. HTTP-check every NEW URL with a real-browser User-Agent — `200 OK` only; drop or replace failures per the link-validation rule.
2. Spot-check 3–5 KPI-panel / delta-table numbers — each must string-match its same-row citation.
3. Re-derive each scenario value (multiple × scenario-EPS) and each upside/downside %.
4. Append `<details><summary>Verification log — YYYY-MM-DD</summary>...</details>` to the Update Log entry. Spec: `reference/citations.md`.

## Further viewing — explainer videos (optional, but default to including)

When this thesis turns on something a reader would struggle to picture from prose alone — the product or mechanism central to the tracked thesis (a humanoid robot's actuators / harmonic reducers / ball-screws / force sensors, a chip-stacking or etch/deposition flow, a surgical-robot wrist, a drug's mechanism of action), a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the thesis note is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: `reference/citations.md` § "Further viewing — explainer videos".

## Learning from sell-side institutional research

The "thesis-revisit" note is a mature sell-side report type (MS *Risk Reward Update*, GS *Beyond the Cycle / View intact*, Bernstein *LT thesis intact*, JPM single-stock revisits, Citi *On Track to Reach [milestone]*, GS *Conviction List – Directors' Cut*). Fold these into the steps above:

- **Lead with a top-line VERDICT, not a buried scorecard (Bernstein "thesis intact" / JPM "Stay Neutral" / GS "View intact").** Put a fixed-ladder call as the first line of Step 5 output and as a one-clause headline: **Thesis: INTACT / AT-RISK / BROKEN** (≈ Intact / Impaired / Invalidated), plus the unchanged-or-new rating, the price target with **upside/downside % to the current price**, and a one-clause reason. Use the fixed verdict ladder (intact / at-risk / broken; reiterate / upgrade / downgrade) — never free-form adjectives. Define the ladder once in Step 1.

- **Open Step 3 with a "WHAT'S CHANGED" From→To delta table (MS *Risk Reward Update*).** Rows = Rating, Price Target, Bull / Base / Bear case value, key EPS years; columns = **Prior → Current (Δ)**. Tag which inputs are new ("Updated Components: EPS"). Follow it immediately with a one-line **Reason for change** naming the trigger event and magnitude — e.g. *"post-1Q26 results: cut FY26–28 EPS 2–4% on lower GPM; PT and scenario values fall 3–4%."* The scorecard sits below this block.

- **Quantify every status — forbid bare "on track / behind / concerning" (sell-side rigor).** Each scorecard pillar must show *print + original expectation + delta*: e.g. *"Rev growth >20%: Q3 actual 22% vs >20% target = on track"*; *"Margin: flat YoY vs +150bps expected = behind by ~150bps"*. Mirror Citi's *"on track to 1TWh / Rmb100bn (2Q tracking ~260GWh, ~Rmb24.3bn NP)"*.

- **Make Step 4 a TWO-SIDED trigger table (JPM/DiDi "triggers that change the rating").** Columns: Date | Event | KPI to watch | **Confirms thesis if** (numeric threshold) | **Breaks thesis if** (numeric threshold) | Action. Each catalyst carries the specific next-period number that flips conviction up vs down (e.g. *"2Q26 intl loss < Rmb29bn AND domestic mobility EBITA margin holds >4%"*). Every threshold numeric and falsifiable — this replaces the single stop-loss price as the only exit rule.

- **Add a bull/base/bear SCENARIO VALUATION grid (MS scenario block) + a fixed KPI panel (Bernstein GLP-1 / GS Robotaxi trackers).** In Step 1 define the three scenarios as *target multiple × scenario-EPS = value (upside % to spot)* with a one-line driver each (show the multiple, the EPS, and the % so it's re-derivable); roll it forward each revisit and print it in Step 5. Also lock 3–6 recurring **KPI panel** metrics at thesis creation, name the single **core indicator** that defines the thesis, and re-print the identical panel with period-over-period deltas (QoQ/YoY + a rolling figure) on every check-in — consistency of the metric set is the whole value of a tracker.

- **Split NEAR-TERM noise from the LONG-TERM thesis (Bernstein Costco "gas fuels near-term upside while LT thesis intact").** Tag each Step 2 datapoint and Step 3 pillar by **Horizon: near-term / structural**, and have the verdict state which bucket drove any change — so a delayed launch (near-term) doesn't whipsaw a structural-margin call. Reconcile each dated target the prior note set (FY revenue, units, profit, launch date) against the latest run-rate (ahead / on-track / behind + gap), Citi-style.

- **Portfolio mode = run the tracked book as an equal-weight set (GS *Conviction List – Directors' Cut*).** When reviewing multiple positions, report cumulative return vs a stated benchmark since each call's inception, an Add/Remove log this period, and 2–3 codified lessons ("stick with winners that beat on the first print; cut losers fast"). Any return chart must carry the in-chart data-source footer and clip the x-axis to the data range per the project chart rules. Optionally add a **consensus-positioning** line (house PT/rating vs Street mean PT and % buy/hold/sell) to contextualize a reaffirmed thesis against crowding — **when you cite that Street mean PT (a borrowed target), pair it with the price on the consensus's as-of date + the implied upside** (`Street mean $288 vs $232 @ 2026-06-03 → +24%`), not just vs today; your own tracked PT keeps its `upside/downside % to the current price`.

- **Source every number in the delta table, KPI panel, scenario grid, and milestone reconciliation.** Each datapoint needs an inline deep-URL citation where the number literally appears (filing / press release / data provider); the analyst's own scenario model is **not** a source; every derived figure (YoY, % to spot, multiple × EPS) must show its inputs so it's re-derivable. Follows the project's paragraph-level citation and numerical-accuracy standards — see `reference/citations.md`.

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

- A thesis should be falsifiable — if nothing could disprove it, it's not a thesis
- Track disconfirming evidence as rigorously as confirming evidence
- Review theses at least quarterly, even when nothing dramatic has happened
- If the user manages multiple positions, offer to do a full portfolio thesis review
- Store thesis data in `reports/thesis/<TICKER>_thesis.md` (see Storage & persistence above) so it can be referenced across sessions
