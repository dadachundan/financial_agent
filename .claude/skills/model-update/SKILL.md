---
name: model-update
description: Update financial models with new data — quarterly earnings, management guidance, macro changes, or revised assumptions. Adjusts estimates, recalculates valuation, and flags material changes. Use after earnings, guidance updates, or when assumptions need refreshing. Triggers on "update model", "plug earnings", "refresh estimates", "update numbers for [company]", "new guidance", or "revise estimates".
---

# Model Update

**Language:** English-only by default (this is a fast-turnaround, monitoring-style note, matching the project's tracking-skills English-default rule). Produce bilingual / Simplified-Chinese output only on explicit request (`in Chinese`, `bilingual`, `--lang zh`).

## Workflow

### Step 0: The Lead (write this first, it goes at the top)

The note must OPEN with a one-line title + a 3–4 sentence bridge so the reader knows the call before reading a paragraph. This is the single most consistent pattern across GS / Citi / MS / UBS / Jefferies.

**Title — encode the action** (mirror GS Shengyi "CCL pricing uptrend continues; TP up to Rmb146.3; Buy", Citi Yunnan "Model Update; Revising TP Up to Rmb84.4", Jefferies IFX "AI Power to Drive Revenue and Margin Upside – Raising PT to €96"):

```
<Company> (TICKER): <one-line thesis>; TP <up/down/unchanged> to <X> (from <Y>); <maintain/upgrade to/downgrade to> <Rating>
```

**Bridge — the first 3–4 sentences** state: what changed → why → the resulting estimate move → and close with the explicit action: *"We raise/lower our 12-month TP to X (from Y) and maintain/upgrade/downgrade to <Rating>."* Put the magnitude in these opening lines — `+1%/5%/6%`, `raise TP by 14.8%`, `from $155` — not buried in the body. Attach implied up/downside to the current price right beside the TP (e.g. `TP HK$128 vs HK$78.25, +63.6%`).

Keep rating verbs explicit and consistent: **maintain / reiterate / upgrade to / downgrade to / initiate at** <tier>. A rating change leads the title (BofA "Upgrade CGN to Buy"; MS "Upgrade to EW") — never a one-liner buried at the end.

### Step 1: Identify What Changed

Determine the update trigger:
- **Earnings release**: New quarterly actuals to plug in
- **Guidance change**: Company updated forward outlook
- **Estimate revision**: Analyst changing assumptions based on new data
- **Macro update**: Interest rates, FX, commodity prices changed
- **Event-driven**: M&A, restructuring, new product, management change
- **Mechanical / non-fundamental**: Bonus issue, stock split, share-count change, or FX-only translation. These scale EPS and TP **proportionally with no thesis change** — and the note must say so explicitly. Model on JPM Envicool "Model update for bonus issue" (EPS −23% from dilution, TP scaled proportionally, rating reiterated). Skip the Driver Bridge and Scenario blocks; state plainly that the revision is mechanical and the rating is reiterated.

**Locate the prior baseline before touching numbers (MUST).** The Old column of the Step-3 revision grid must come from a real prior, located in this order: (a) the ticker's most recent model-update / earnings-analysis note under `reports/earnings/`, (b) the initiating-coverage model under `reports/company/<slug>/`, or (c) a dated zsxq broker note labelled *Analyst view:* (read back from `db/stock_price_target.db` / the `/pt` viewer via existing helpers — read-only). If NO prior house estimate exists, say so explicitly and either bootstrap a baseline labelled as new — printing `n/a (first note)` in the Old columns — or hand off to [[initiating-coverage]]. NEVER invent a prior.

### Step 2: Plug New Data

#### After Earnings
Update the model with reported actuals:

| Line Item | Prior Estimate | Actual | Delta | Notes |
|-----------|---------------|--------|-------|-------|
| Revenue | | | | |
| Gross Margin | | | | |
| Operating Expenses | | | | |
| EBITDA | | | | |
| EPS | | | | |
| [Key metric 1] | | | | |
| [Key metric 2] | | | | |

**Segment Detail** (if applicable):
- Update each segment's revenue and margin
- Note any segment mix shifts

**Balance Sheet / Cash Flow Updates**:
- Cash and debt balances
- Share count (buybacks, dilution)
- Capex actual vs. estimate
- Working capital changes

### Step 3: Revise Forward Estimates

Based on the new data, adjust forward estimates. Use a **three-year FY1E / FY2E / FY3E grid with Old / New / Chg(%) sub-columns** — mirror GS "Exhibit 1: Earnings revisions". Always print BOTH old and new; never just the new number. Include the margin rows (GM% / OPM% / NM%) alongside the absolute lines, because a revenue-up / margin-down revision is a common, informative shape (GS Shengyi raises revenue but trims GM):

| | FY1E Old | FY1E New | Chg% | FY2E Old | FY2E New | Chg% | FY3E Old | FY3E New | Chg% |
|---|---|---|---|---|---|---|---|---|---|
| Revenue | | | | | | | | | |
| Gross Profit | | | | | | | | | |
| GM% | | | | | | | | | |
| Operating Profit | | | | | | | | | |
| OPM% | | | | | | | | | |
| Net Income | | | | | | | | | |
| NM% | | | | | | | | | |
| EPS | | | | | | | | | |

**Earnings revision (the prose twin of the table):** State the per-line, per-year % deltas verbally, e.g. *"revenue +1%/5%/6%, net income +1%/4%/5% for FY26–28E."* Express revisions as percentages by year — % is how the desk reads magnitude — and let the multi-year shape expose whether the revision is near-term or out-year weighted (MS Micron EPS +4%/+48% for 26/27E flags an out-year story).

**vs Consensus (required, not optional):** State how the revised house estimates sit versus Street consensus, in % or pp, by year, naming above/below — e.g. *"FY27 EPS +11% above consensus"* (GS Taiwan EPS 7/5/6pp above consensus; Jefferies IFX FY27–28 +11% above). Add a deep-URL citation to the consensus source so the number traces to where it literally appears (per the project's paragraph-level citation rule). Keep company guidance vs house estimate clearly attributed — guidance is the company's, house numbers are the analyst's (reuse the project's *Analyst view:* convention for "we model / we expect").

#### Driver Bridge (what moved the number)

Decompose every revision into **named causal levers**, each tied to its numeric contribution to the estimate delta — this is the analytical core the analogs all carry (GS leads with bold driver sub-heads like "CCL industry pricing in continuous uptrend" before the numbers table). Don't write the revision as undifferentiated prose:

| Lever | Direction | Driver evidence (with citation) | Est. impact |
|---|---|---|---|
| Volume / units | | e.g. raised shipment guide 15→16bn sqm | |
| Price / ASP | | e.g. channel-check price hike +RMB0.7–0.95/m | |
| Mix | | | |
| Margin | | | |
| FX | | | |
| Share count | | buybacks / dilution / bonus issue | |

Tie each lever to its source the way the desks do: company actuals + guidance as the trigger (quote raised guidance verbatim), channel checks / price surveys for the ASP lever, cross-asset / macro inputs (FX, tariff cost, raw-material) when they move the model. Reconcile reported actuals (beat/miss per line) **before** projecting forward.

### Step 4: Valuation Impact

Recalculate valuation with updated estimates:

| Valuation Method | Prior | Updated | Change |
|-----------------|-------|---------|--------|
| DCF fair value | | | |
| P/E (NTM EPS × target multiple) | | | |
| EV/EBITDA (NTM EBITDA × target multiple) | | | |
| **Price Target** | | | |

**State the TP as an explicit derivation line** (every analog does — GS, Citi, MS, UBS):

```
TP = <base-year metric> × <multiple> = <X>; prior multiple <M>; TP change <±%>
```

e.g. *"raise 12m TP by 14.8% to Rmb146.3, based on 38.7x 2027E P/E (previously …)"* or UBS CAT *"$900, basis 2027E EPS $29.95 × 30x."* Always show the **prior multiple in parens** and the **% move in the TP** — never just the new TP.

**Justify the multiple against a reference** — the stock's own history in std-dev terms (Citi Yunnan "3.09x 2026E P/B, −0.4 s.d. below mean"), peers/sector (BofA "12x 2027E vs sector"), or PEG. Add an inline deep-URL citation to the source of that comparison (history series, peer comp table). Per the project rule, **do NOT write "Source: our model"** for the multiple — cite the external comp / history input the multiple is anchored to.

### Step 4b: Scenario Analysis (Bull / Base / Bear)

Attach **three price targets, each with its own multiple AND its own flexed estimate** — build bull/bear by flexing BOTH the estimate and the exit multiple, not one (MS Micron 1650/1050/675; UBS CAT 1173/900/626; Citi Yunnan optimistic/base/pessimistic). Show the implied up/downside to the current price for each:

| Scenario | Key flexed assumption | Multiple | Implied TP | Up/downside vs current |
|---|---|---|---|---|
| Bull | e.g. ASP +X%, volume +Y% | | | |
| Base | central case | | | |
| Bear | e.g. ASP −X%, volume −Y% | | | |

### Step 5: Summary & Action

**Estimate Change Summary:** This is the body recap of the Step 0 lead — don't bury the action here, it belongs up top.
- One paragraph: what changed, why, and what it means for the stock
- Is this a thesis-changing event or noise?

**Rating / Price Target:**
- Maintain or change rating?
- New price target (if changed) with methodology
- Upside/downside to current price

### Step 5b: Risks (Upside / Downside)

Split risks into **two explicit lists** at the end and note **which direction each risk threatens the TP** (JPM convention):

- **Upside risks:** factors that would push estimates / TP above base case.
- **Downside risks:** factors that would push them below.

Mirror the asymmetry the analogs surface (UBS CAT "Key things to watch" + risks; JPM labels which risk threatens the TP in which direction).

### Step 6: Output

- Primary deliverable: a markdown note at `reports/earnings/<TICKER>_model_update_<YYYY-MM-DD>.md` (English ticker first per the project filename rule) containing the estimate change summary and the updated price target derivation. Markdown only — no Word output (the report viewer surfaces `.md`).
- Updated Excel model only if the user supplied an existing model to update.
- Commit + push in the same task (Conventional Commit, e.g. `feat(reports/earnings): ...`). Successive model-update notes for the same ticker form the estimate-revision history the Important Notes tell you to track.

### Step 7: Verify & log

Before saving/committing:

1. HTTP-check every URL with a real-browser User-Agent — `200 OK` only; drop or replace failures per the link-validation rule.
2. Spot-check ≥5 numbers — including the consensus figure, the guidance quote, and at least one Driver-Bridge lever input — each must string-match the URL cited in the same paragraph.
3. Re-derive the TP line arithmetic (base-year metric × multiple) and each Chg% cell in the revision grid.
4. Append `<details><summary>Verification log — YYYY-MM-DD</summary>...</details>` listing each check. Spec: `.claude/skills/company-research/references/citations.md`.

### Further viewing — explainer videos (optional, but default to including)

When this note hinges on something a reader would struggle to picture from prose alone — the product or segment whose mechanics are actually moving the estimate (a humanoid robot's actuators / harmonic reducers / force sensors, an HBM stack, a CCL lamination line, a turbine or power-conversion module, an unfamiliar business model, or a market-structure shift behind the revision) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* what changed, not just read about it. Default to including them whenever the driver mechanics matter to the estimate change; omit only when the revision is purely numeric (e.g. a mechanical bonus-issue / split scaling) with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in (e.g. beside the Driver Bridge lever it illustrates), or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

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

- Always reconcile your estimates to the company's reported figures before projecting forward
- Note any non-recurring items and whether your estimates are GAAP or adjusted
- Track your estimate revision history — it shows your analytical progression
- If the quarter was noisy, separate signal from noise in your estimate changes
- Check consensus after updating — how do your revised estimates compare to the Street?
- Share count matters — dilution from stock comp, converts, or buybacks can materially affect EPS

## Learning from sell-side institutional research

The "model-update / revising-TP" note is a tightly standardized sell-side type (analyzed across 21 notes from Citi, GS, Morgan Stanley, J.P. Morgan, UBS, Jefferies, BofA). The desk layout is consistent enough to treat as a template — apply it.

**The canonical layout (top to bottom):**
1. **Action-encoding title** — `Company (TICKER): <thesis>; TP up/down to <X>; <Rating>` (Step 0).
2. **3–4 sentence bridge** ending in the explicit TP + rating action (Step 0).
3. **Bold driver sub-heads** — one short paragraph per causal lever, *before* the numbers table (GS "Positive on AI CCL migrations"). This is the Driver Bridge in prose form.
4. **"Earnings revision:" paragraph** — exact per-line per-year % deltas (Step 3 prose twin).
5. **"Exhibit: Earnings revisions" grid** — FY1/FY2/FY3 Old/New/Chg, with margin rows (Step 3 table).
6. **"Valuation:" line** — TP %move + (base metric × multiple) + prior multiple in parens (Step 4).
7. **Bull / Base / Bear** — three TPs, each with its own multiple + implied up/downside (Step 4b).
8. **Upside / Downside risks** — split lists, direction-of-threat noted (Step 5b).

**Quarterly forecast grid for US-coverage names:** when the revision is driven by the *shape* of the quarters (not just the annual level), add a Q1–Q4 Old/New forecast grid (JPM Nextpower) so the reader sees the intra-year re-phasing. The compressed JPM "Key Changes (Prev / Cur / Δ)" box is the sidebar version of the Step-3 grid for space-constrained notes.

**House voice & formatting (apply every time):**
- Print BOTH old and new — and the prior multiple — never just the new figure. `from $155`, `(previously 38.7x)`, `old 80.9 → 84.4`.
- Attach implied up/downside to the current price beside the TP. `现价64.37, +31.1%`; `HK$128 vs HK$78.25, +63.6%`.
- Express revisions as **% by year**, not just absolute level changes.
- Show margin rows (GM% / OPM% / NM%) alongside the absolute lines.
- Keep rating verbs explicit: maintain / reiterate / upgrade to / downgrade to / initiate at.
- Keep company guidance vs house estimate clearly attributed — reuse the project's *Analyst view:* labeling for "we model / we expect" so house numbers are never mistaken for reported fact.

**Cross-references to global rules (do not weaken):** every numerical claim must trace inline to a URL that literally contains the number (numerical-accuracy rule); each substantive paragraph carries a deep-URL citation (paragraph-level citation rule). If the note produces any chart (e.g. an estimate-revision-history chart), the in-chart data-source footer is mandatory per the global chart-annotation rule.
