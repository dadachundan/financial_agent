---
name: theme-research
description: Build and maintain thematic equity baskets (e.g. humanoid-robotics-sensors, GLP-1 supply chain, advanced packaging, EV battery) — each theme is a single English markdown file at `reports/themes/<slug>_theme.md` containing the tracked-tickers table (ticker, role, justification, added-date), thesis, performance, drift signals, and Data Used manifest (Chinese companion `<slug>_主题研究.md` available on explicit request). The skill creates new themes, refreshes existing ones with movers/laggards + recent news + valuation drift, and surfaces drift signals (tickers no longer fitting; new tickers worth adding). It mines the user's local zsxq broker-report library (`db/zsxq.db`) as a first-class source — candidate names, the TAM anchor, conviction ranks, and broker price targets — at both create and refresh, reading the original PDF text via the read-only zsxq helper scripts. Distinct from `sector-overview` (one-shot landscape essay) — themes are *tracked baskets* that get refreshed. Use when the user says "build a theme on X", "track the X basket", "refresh my <theme> basket", "what's moving in my <theme>?", or "what themes do I have?"
---

# Theme Research

A theme = **named basket of tracked tickers + keywords**, written as a single markdown file. Themes are *living* artifacts — they get refreshed periodically as movers shift and the keyword set evolves. Distinct from [[sector-overview]] (one-shot essay on a sector landscape) and from a watchlist (no analytical depth, just price tracking).

Adapted from the [LLMQuant theme research workflow](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-portfolio/workflows/theme-research.md) (MIT), re-pointed at a markdown-file convention under `reports/themes/` instead of LLMQuant's hosted theme storage. The file format matches the rest of your `reports/` tree — pure markdown, no YAML, viewer-renderable at `localhost:5001/reports`.

## When to use

The user says any of:

- "Build a theme on humanoid robotics sensors"
- "Track the GLP-1 supply chain basket"
- "Refresh my advanced-packaging basket"
- "What's moving in my AI infrastructure theme?"
- "Add SZSE:002050 to my robotics-sensors theme"
- "Drop NVDA from my AI infrastructure theme"
- "List my themes"
- "Run a theme on EV battery cell chemistry — focus on solid-state"

Four modes:

| Mode | Trigger phrasings | What happens |
|---|---|---|
| **Create** | "build a theme on X", "start tracking X", "new theme: X" | Builds a new `<slug>_theme.md` from scratch |
| **Refresh** | "refresh my X theme", "what's moving in X", "update X basket" | Reads the existing theme file, re-pulls market data + news + valuation, surfaces drift, updates the Performance / Recent events / Drift signals sections in place |
| **Mutate** | "add/drop <ticker> to <theme>", "rename theme X to Y", "delete theme X" | Edits the **Tracked tickers** table only; does not re-run the data pull or rewrite prose unless the user explicitly asks |
| **List** | "list my themes", "what themes do I have" | Walks `reports/themes/*_theme.md` and summarizes each from its top-of-file metadata |

## When NOT to use

- The user asks for a one-shot industry essay with no intent to track — use [[sector-overview]].
- The user wants a comparison of a closed N companies — use [[compare-companies]].
- The user wants a deep dive on a single company — use [[company-research]].
- The "theme" maps cleanly to an existing ETF the user can hold (e.g. "AI infrastructure" → XLY+XLK or just SOXX) and they're not trying to build alpha vs the ETF — recommend the ETF instead and skip the basket overhead.

## Core principle: themes are *tracked*, not just *researched*

A theme is not just a sector essay — it's a basket of named tickers with explicit justifications and a refresh cadence. The skill's value is in **drift detection**: are the tickers I picked 6 months ago still the right tickers? Has a new entrant emerged? Has a former member become structurally impaired or moved out of the theme?

This is the discipline that distinguishes a useful theme tracker from a stale watchlist. The **Tracked tickers** table records *why* each ticker was added — and the refresh workflow surfaces whether that justification still holds.

## Theme file structure (single markdown file per theme)

Every theme is one file: `reports/themes/<slug>_theme.md` (English default). Chinese companion `reports/themes/<slug>_主题研究.md` is created only when the user opts in.

```markdown
# Humanoid Robotics Sensors / 人形机器人传感器

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en

## What's New

*The delta since you last looked — newest refresh on top. Older entries collapse into the archive below so this stays short.*

**2026-06-30 refresh (vs 2026-05-31):**
- **Added** SZSE:300354 Donghua Testing (core) — 6-D force sensor entered mass production ([cninfo, 2026-06](https://...)).
- **Dropped** HKEX:9863 Leapmotor — humanoid program shelved ([HKEX 2026-06](https://...)).
- **Movers:** basket +8.2% since last refresh vs CSI 300 +2.1%; Anpeilong +19% on the Tesla order print.
- **New broker call:** GS initiated Anpeilong Buy, PT ¥120 vs ¥96 @ 2026-06-05 → +25% ([GS, zsxq #...](http://xs-macbook-air.local:5001/zsxq/pdf/.../<filename>)).
- **TAM revision:** 2027E pool lifted to ≈$3.6bn from ≈$3.1bn (prior refresh) — +$0.5bn from the force-torque sub-bucket on faster dexterous-hand adoption ([forecaster, 2026-06](https://...)).
- **Thesis drift:** none — basket still reflects the original BOM-expansion bet.

<details><summary>Earlier refreshes</summary>

**2026-05-31 — basket created** (2 tickers: Anpeilong core, Leapmotor adjacent).

</details>

## Thesis

**Anchor — humanoid-robot sensor TAM:** 2025 ≈$1.2bn → 2026E ≈$2.1bn (+75%) → 2027E ≈$3.6bn (+71%) → 2028E ≈$5.4bn (+50%) *(illustrative — cite a named forecaster)* ([forecaster, 2026](https://...)). Sub-buckets: force-torque ~45% · tactile ~25% · IMU/vision ~30%; geo China ~55% vs ex-China ~45%. **Swing factor:** force-torque (per-unit count climbs fastest as dexterous hands proliferate); `core` names ride that bucket.

Sensor suppliers for humanoid robots — force / torque sensors, IMUs, tactile sensors, vision-system components, and supporting MCUs. The bet is that humanoid build-out from Tesla Optimus, Figure, Unitree, Xpeng, and several Chinese OEMs creates a 5–10× per-unit sensor BOM vs incumbent industrial-robot designs, with the cost curve playing out fastest among A-share pure-play suppliers that already have force-sensor design wins.

## Scope rules

In: standalone force-torque sensor suppliers; tactile-sensor specialists; humanoid-MCU suppliers; companies with disclosed humanoid-program supplier status.

Out: diversified auto-electronics names without a disclosed humanoid SKU; pure-play actuator names (separate theme); CV / vision-software pure-plays without hardware exposure (separate theme).

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| SZSE:002050 | Anpeilong (安培龙) | core | Largest A-share standalone force-torque sensor supplier; design-wins at Tesla Optimus tier-1 + multiple Chinese humanoid programs ([cninfo 投资者交流活动记录, 2026-04](https://...)). | 2026-05-31 |
| HKEX:9863 | Leapmotor (零跑汽车) | adjacent | EV OEM with announced humanoid program; humanoid-derived sensor demand is <5% of base auto business but the roadmap is on the public record ([HKEX 2026-Q1 results](https://...)). | 2026-05-31 |

## Exclusions

| Ticker | Reason |
|---|---|
| NASDAQ:TSLA | Humanoid Optimus is <1% of Tesla revenue and intermingles with auto / energy — too diluted to track as a humanoid-pure-play. |

## Keywords

humanoid robotics / 人形机器人 · force-torque sensor / 力矩传感器 · tactile sensor / 触觉传感器 · IMU / 惯性测量单元 · robotics MCU / 机器人主控

## Performance (since last refresh)

<refresh-driven; replaced in place each refresh; benchmark required (S&P 500 / CSI 300 / sector ETF) with comparable window>

### Basket scorecard

<refresh-driven; MS Three Actionable Ideas style — batting average across the basket: % of names positive over the window · % beating the benchmark · best/worst named contributor + their return · cumulative basket outperformance in bps since inception (where snapshots.jsonl has ≥2 lines). All from yfinance + the snapshot history.>

## Recent events

<refresh-driven; bulleted list of material 8-K / 公告 / press releases since last_refreshed, each inline-cited>

## Drift signals

<refresh-driven; the value-add of refresh — flag tickers fitting less well, new entrants worth considering, stale justifications, macro / regulatory factors that have moved the thesis>

## Leading indicators

<refresh-driven; 2–4 upstream signals that move BEFORE the basket members and would crack the thesis first — never the member stock prices. Each: signal · latest reading + as-of date · direction · what it implies for the anchor or a name. Include a side-by-side line where ≥2 members guide the same forward metric. Source-chain each to its primary issuer. Below the macro signals, a **per-ticker operating-data table** (Bernstein *Barometer* style): per name, the latest operating print (shipments YoY/MoM · order-book · penetration % · capacity), each cited to its primary issuer — the leading-indicator spine, separate from price.>

## Catalysts (next 3–6 months)

<refresh-driven; each catalyst = event + transmission mechanism + timing window + which TAM sub-bucket or tracked name it moves. Format: `<event> (<mechanism → effect on which sub-bucket>), <timing>`. Prefer catalysts that are leading indicators of the anchor. A bare calendar entry with no mechanism is a defect.>

## Data Used / 数据来源清单

<mandatory manifest — see Output Format section below>

## References

<every URL cited inline>

## History

- 2026-05-31 — created with initial 2-ticker basket (Anpeilong core, Leapmotor adjacent)
- 2026-05-31 — first refresh pass
```

Alongside the markdown file, each theme keeps a machine-readable **snapshot sidecar** `reports/themes/<slug>_theme.snapshots.jsonl` — one append-only JSON line per refresh. This is the *tracking backbone*: the next refresh diffs against the last line to author the `## What's New` block, and you can trace the basket's evolution programmatically without parsing prose or git. It is NOT a set of dated full-report copies — just a compact state vector per refresh.

### What's New + snapshot sidecar (trackability)

The whole point of a *tracked* basket is answering "what did I know before, what's new?" Two artifacts deliver that, both updated every refresh — and **never** by spawning dated copies of the report:

1. **`## What's New` section** (top of the md, under the metadata line) — the human-facing delta. Each refresh **prepends** a dated block (tickers added / dropped / role-changed, biggest movers vs benchmark since last refresh, *new* broker calls & catalysts, **TAM revisions** (anchor old→new + driver), thesis drift). The previous block rolls into a `<details>` archive so the section stays short. Keep ~5–8 bullets per refresh; link each claim.

2. **`<slug>_theme.snapshots.jsonl`** — the machine record. Append exactly one line per refresh:

   ```json
   {"date":"2026-06-30","tickers":[{"t":"SZSE:301413","role":"core"},{"t":"NASDAQ:HSAI","role":"core"}],"perf":{"basket_1y":80.2,"bench":"CSI300","bench_1y":33.3,"since_last_refresh":8.2},"evidence_file_ids":[184152244582842,212485814114811],"n_events":6,"note":"added Donghua; dropped Leapmotor"}
   ```

   Field contract: `date` (ISO), `tickers` (the full current set with roles — so a diff vs the prior line yields added/dropped/role-changed for free), `perf` (basket vs a named benchmark + return since last refresh), `evidence_file_ids` (zsxq/source IDs this refresh leaned on), `n_events`, `note` (one line), and an **optional `tam` object** capturing the Thesis anchor so a TAM revision diffs the same deterministic way `tickers` does: `"tam":{"unit":"$bn","forecaster":"<named source>","path":{"2026":148,"2027":175,"2028":198}}`. The create-pass writes the first (baseline) line; on refresh, a changed `tam.path` vs the prior line *is* the `## What's New` TAM-revision bullet.

**How "what's new" is computed:** on refresh, read the last JSONL line, set-diff its `tickers` against the current set, compare `perf`, and list `evidence_file_ids` not seen before → that *is* the `## What's New` block. Deterministic, no eyeballing two long reports.

**Point-in-time recall** is git, not file sprawl: `git show <sha>:reports/themes/<slug>_theme.md` reconstructs any past state, and `git log --oneline -- reports/themes/<slug>_theme.snapshots.jsonl` lists every refresh commit. This is why one canonical file + the sidecar beats dated `_2026-06-30.md` copies (which duplicate the ticker table, drift apart, and clutter the viewer).

### Thesis — lead with a quantified anchor (TAM / spend / volume pool)

A thesis that asserts growth without a number is a vibe, not a forecast — it can't be falsified, drift-checked, or diffed across refreshes. So **every Thesis MUST open with a quantified anchor**: one headline pool the theme is a bet on — TAM, total spend, or unit/volume (dollars, GWh, magnet tonnage, script volume, shipped units …) — stated as a **dated, multi-year trajectory with YoY decomposition**, each year attributed to a **named third-party forecaster** (industry-research firm, government statistics office, trade body, or a cited sell-side note) via a deep URL. Per the project rule, **the analyst's own model is never the source** — cite the forecaster; if none publishes a number for the pool, say so and fall back to the nearest cited proxy rather than fabricate a trajectory. Format:

> `<pool> 2025 $122bn → 2026E $148bn (+21%) → 2027E $175bn (+18%) → 2028E $198bn (+13%)` ([Forecaster, date](deep-url))

(A semicap basket anchors on WFE dollars; a GLP-1 theme on branded-sales or script volume; rare earths on NdFeB magnet tonnage; EV battery on GWh demand.)

**Sector-specific anchor shapes — match the anchor to how the business actually earns money.** A one-off dollar/volume TAM is right for a *capex / consumption* theme (semis WFE, EV GWh, magnet tonnage). It is the *wrong* anchor for two common theme types:

- **Recurring-revenue / installed-base ("razor-and-blade") themes** — surgical robotics, analytical & life-science instruments, diagnostics, dialysis, payments terminals, aftermarket-heavy industrials. Here the falsifiable anchor is **installed base × utilization × recurring attach**, not the one-time system TAM. Decompose revenue into **systems (placements) / consumables & instruments / service**, and lead the thesis with the *recurring* pool — that is the moat and the flywheel, and the one a drift-check must track. The swing factor is usually **utilization** (procedures or runs per installed system), not unit system sales. (E.g. a surgical-robotics basket anchors on procedure volume + installed base + the recurring-revenue mix — ISRG's da Vinci is ~85% recurring — *not* on "systems sold this year".) Map each `core` name to whether it is levered to placements (early S-curve) or to the installed-base annuity (mature).
- **Regulated-product themes** — medtech, biopharma, defense. The anchor must be gated by the **approval + reimbursement funnel**: a device/drug with no clearance and no reimbursement code has ~zero addressable TAM regardless of the market-size headline. State the approval stage and reimbursement status alongside the TAM, and treat the funnel as the swing factor.

Whichever shape applies, hold it to the same discipline as a dollar TAM — dated, multi-year, third-party-sourced, never the analyst's own model.

**Decompose the anchor into 2–5 sub-buckets**, each with its own dated path and source, plus a **geographic cut where natural** (e.g. ex-China vs China) — rendered as a compact inline list or 3-column table, not a second essay. **Name the swing factor**: the one sub-bucket whose revision moves the headline most (for a WFE basket that is DRAM; for a GLP-1 theme it may be oral formulations; for rare earths, magnet-grade oxide). Map each `core`/`enabler` ticker to the sub-bucket it rides, so the reader sees which names are levered to the swing factor — this reuses the role taxonomy rather than adding a parallel structure.

Also add a one-line **value-chain / process-step map** — which layer of the supply chain each tracked name occupies, as a compact inline list, *not* buried in the per-ticker Justification cells (e.g. for WFE: litho ASML · etch LRCX/AMEC/NAURA · deposition Kokusai/Piotech/TEL · metrology KLAC/Lasertec · test Advantest · dicing DISCO; for a GLP-1 theme: API · fill-finish · device · distribution; for EV battery: cathode · anode · electrolyte · cell · pack). A process step / value-chain layer that **no** tracked name occupies is a coverage gap and a candidate-add signal the sub-bucket cut alone misses.

**Make the anchor an AUDITABLE BUILD, not a cited headline (mandatory where the source discloses the drivers).** A sourced headline TAM the reader cannot re-derive is a *half-anchor* — desks publish the model, not just the conclusion. Three obligations:
1. **Bottom-up demand build whose rows sum to the headline.** Reproduce a compact `units × content-per-unit` table — e.g. AI-ASIC/GPU shipped units × substrate-area-or-$/chip; installed base × consumable attach; scripts × net-price — each driver row cited to the source exhibit+page, columns = the anchor years. The reader must be able to stress one input (what does a 10% unit miss do to the pool?).
2. **Two-sided supply/demand balance for any imbalance thesis.** If the thesis rests on a shortage / glut / utilization (most capacity-constrained baskets), present the balance as a **demand series AND a supply/capacity series in the same units** (mm², kt, sheets/mo, units) with the ratio as the visible *quotient* — never the ratio/gap alone. The ratio is a derived series; the project Chart rule requires its components be plotted. A supply line is a **capacity-by-named-player × year** build (it doubles as a "who is adding capacity" read).
3. **Content-per-unit ladder + pricing→EPS bridge.** Carry the spec ladder (layer-count / area / grade × $/unit by product generation) — it is the *mechanism* behind the CAGR — and connect the pricing/ASP lever to at least the **swing-factor names' margin/EPS** (`price +20% → OPM breakeven→25%→35% → ~90% EPS CAGR`), so the price path is not a free-floating industry stat disconnected from the valuation snapshot.

**Track the anchor over time.** When a refresh's forecaster republishes and the anchor moves, the `## What's New` block carries a **TAM-revision** bullet — old→new for each affected out-year **plus the explicit % magnitude** (mirror how JPM/Bernstein print revisions: *"TAM raised +37% to $1.7trn 2028E, driver = CPU DRAM bit-demand"*; Bernstein battery 2030 +~10%), the delta attributed to a named driver (e.g. `2027E pool lifted +11% to $175bn from $158bn — +$3.4bn from <driver sub-bucket>, [Forecaster, date](url)`); if the forecaster didn't republish, carry the number forward and say so. The optional `tam` field in the snapshot sidecar (above) makes this revision diff the same deterministic way the ticker set already does.

### Slug rules

- Kebab-case (`humanoid-robotics-sensors`, not `humanoidRoboticsSensors` or `humanoid_robotics_sensors`).
- English / pinyin first. Optional `_中文名` suffix if it aids discoverability (`humanoid-robotics-sensors_人形机器人传感器`).
- Lowercase only.
- No date in slug.
- Avoid generic words like `tech`, `growth`, `ai` alone — themes work best when scoped narrowly (`ai-infrastructure-power-cooling` beats `ai`).

### Top-of-file metadata line

Always present, single line under the H1 title:

```
**Created:** YYYY-MM-DD · **Last refreshed:** YYYY-MM-DD · **Last mutated:** YYYY-MM-DD · **Refresh cadence:** monthly · **Languages tracked:** en[, zh]
```

- **Created** — date the theme file was first written.
- **Last refreshed** — date of the most recent data pull (price / news / drift). Updated by `Step 4` of the workflow.
- **Last mutated** — date of the most recent registry-only edit (add/drop ticker, rename slug, change role). Updated by `Step 5` of the workflow. Distinct from "Last refreshed" — mutations are cheap, refreshes are expensive.
- **Refresh cadence** — informational only (the agent uses this to flag themes that have gone stale beyond their stated cadence). One of `weekly`, `monthly`, `quarterly`, `on-event`.
- **Languages tracked** — `en` (default), `en, zh`, or `zh` (Chinese-only). Tells the refresh workflow which file(s) to update.

### Ticker role taxonomy

- **`core`** — pure-play exposure; the theme's defining names.
- **`adjacent`** — partial exposure or expanding into the theme; not pure-play but worth tracking.
- **`enabler`** — supplier / component / IP licensor that benefits when the theme builds out.
- **`hedge`** — counter-position that benefits when the theme breaks (rare; mostly relevant for thematic short books).

If a ticker doesn't cleanly fit, write a one-sentence justification and pick the closest role. Don't invent new roles per theme — discipline matters.

The role tag is static; the Thesis adds a **time axis** on top of it (*who benefits when* — see *Learning from sell-side institutional research*): enablers / equipment monetize first along the anchor curve, end-product names later, each with a dated gate (UE-breakeven, GM-turns-positive, a penetration-% threshold). Map each name to its stage in the Thesis, not as a new role.

### Conviction ranking (within the basket — sourced, never the skill's own)

Beyond the categorical role tag, capture any **ordered preference** a named external analyst has published over the basket members, e.g. *"Bernstein prefers A > B > C: A = broadest exposure + cheapest; B = upgrade-cycle leverage; C = lags this year, sets up next."* Three rules:

1. **Always attributed, never self-authored.** Per the project rule, the skill's own model is NOT a source — so the rank must cite a named report/analyst via deep-URL or zsxq `file_id`. If you want to record the agent's own read, label it explicitly *"Analyst view (this note):"* and keep it visibly separate from the cited rank.
2. **Each rung carries a one-clause why** tied to that name's moat/threat Justification cell, so the order is legible, not bare. Where two credible sources disagree, show both (*"GS: A>B; MS: B>A — split on the swing-factor sub-bucket"*) rather than picking a winner.
3. **Price targets show their derivation.** If a tracked name carries a sell-side PT, capture it as `PT = <multiple>× applied to <EPS / metric base> ([analyst, date](url))` — a bare PT with no method is not acceptable, mirroring the "cite the inputs, not the model" rule.

Keep the ranking in `## Thesis` (a closing preference sentence) or as a one-line lead-in to the Tracked tickers table — **not a new table column** (preserve the 5-column parse contract). A new broker re-rank IS `## What's New` material; record the source in `## References`. (This generalizes: a humanoid basket ranks its sensor suppliers, a GLP-1 basket its CDMOs — the rank is the cited analyst's, not invented.)

### Valuation snapshot (surface the PT store inside the file)

The skill persists sell-side PT / rating calls to `stock_price_target_db` — but the theme *file* (the thing the user actually reads) must also **show** them, or it is valuation-blind for every name. When ≥1 tracked name carries sell-side coverage, include a mandatory **`## Valuation snapshot`** table — **one row per tracked name**, rendered *separately* from the 5-column Tracked-tickers table (which stays a clean parse target — do NOT add valuation columns there). Columns:

`Ticker · Rating · Px @ note date · PT · Upside% (vs note date) · current px · fwd multiple (P/E or sector-appropriate) · own ~10yr-avg multiple · FY1 / FY2 EPS (or the forward metric)`

Rules:
- **Populate from the helper, don't hand-transcribe** — read the rows back from `stock_price_target_db` so the table and the `/pt` viewer agree.
- **The "Px @ note date" column is mandatory and is the load-bearing price, not today's spot.** It is `report_date_price` from `stock_price_target_db` (the **"Px @ Report"** column in `/pt`) — the stock's price on the day the note was published, which is what fixes the upside the analyst actually called. `Upside%` is `upside_pct` (PT vs that report-date price), matching `/pt` exactly. Keep a separate `current px` column for live context (how much of the move already happened); never collapse the two or let today's spot stand in for the report-date price. If `report_date_price` is null, write `n/a` in that cell — don't backfill it with the current price.
- **Capture both forward years (FY1 AND FY2 multiple) — mandatory, not "where supplied".** The FY1→FY2 compression is the bull/bear pivot; if a note gives only one year, derive the other from its EPS estimate or state why the cell is blank. A single-forward-year snapshot is incomplete.
- **Populate the own-history average multiple for EVERY covered name** (10yr or upcycle avg). A blank own-avg cell must say *why* (no coverage / pre-profit / pre-IPO), never be left empty for a subset of names — the priced-for-perfection read is only legible when the whole column is filled.
- **Normalize the cross-section so the basket sorts cheap→dear like-for-like.** One stated forward year for the comparison column, **plus at least one growth-adjusted or cross-sectional metric (PEG, EPS-CAGR, or EV/EBITDA)** — a column of bare P/Es at mixed forward years (some FY1, some FY2, some SOTP) is not a peer-comp; flag SOTP-only names explicitly.
- **Date every row and segregate stale PTs.** Each PT/rating row carries an **as-of date**; a PT older than the refresh window or visibly overtaken by price (current price through the target) is moved to a labelled *"stale — pending refresh"* sub-section, never blended into the live Upside% column where it implies a downside the analyst never called.
- **Show PT derivation** where the source gives it (`PT = <multiple>× applied to <EPS / metric base>`), per the Conviction-ranking rule — at least for the names where the note states it.
- **Capture the bull/base/bear PT triplet** where the note gives one (MS Hesai bull $53 / base $30 / bear $11.5; WULF $103 / $66.5 / $15) — render it in the PT cell, each leg citing the originating note. This is the per-name face of the theme's scenario architecture (see *Learning from sell-side institutional research*); a single base PT loses the downside floor the desk publishes.
- **Render the rating line at desk density** (HSBC/MS style): rating, the report-date price, PT, and computed upside% on one line (e.g. *Buy · TP 450k vs 349k @ 2026-05-20 = +29%*) — the `vs` price is the price on the note's date (`report_date_price`), so the +29% is the upside the analyst published; append `now NNNk` if you want to show the live spot too.
- **On revision, show old→new in the cell** (`PT $340 (was $325)`); a revised PT/EPS is `## What's New` material.
- Pre-profit names use P/S or EV/Sales and say so. Every rating / PT cites its originating note (deep-URL or zsxq `file_id`). If no tracked name has sell-side coverage, omit the section and note "no sell-side coverage" in Data Used.

### Tracked tickers table — the source of truth

The table at the top of the file is the canonical ticker list. Every mutation (add / drop / role change / justification re-grounding) edits a row in this table — not the prose elsewhere in the file. Workflows depend on parsing this table:

- `list` mode reads the top-of-file metadata of each `reports/themes/*_theme.md` (no per-ticker parse needed).
- `mutate` mode runs `Edit` on a single row (or appends a new one).
- `refresh` mode reads the ticker list, pulls data for each, then updates the data-driven sections below (Performance / Recent events / Drift signals).

The table columns are fixed: **Ticker | Name | Role | Justification | Added**. The Justification cell always contains at least one inline markdown link to a primary source naming the ticker as a theme participant. **Beyond proving participation, the cell must do two things:** (a) state the **moat** — the specific product niche / share / cost or IP edge that makes this name hard to displace (not "leader in X" but "sole supplier of Y, ~Z% share"), and (b) name the **threat** — the specific competitor, substitute, customer-insourcing, or policy shift that would erode that edge first (e.g. a mask-inspection name: "sole actinic supplier, ~50% share — threat = a rival's actinic launch in dev"). Where the dominant risk is **customer-insourcing** — the OEM / hyperscaler self-designing the component (the modal 2026 theme risk: BYD/NIO/XPeng/Li in-house ADAS chips vs Horizon; Google/Amazon/MS ASICs vs Nvidia) — name it explicitly *and* the incumbent's structural counter (e.g. Horizon's near-100%-margin BPU IP-licensing pivot; irreplaceability for sub-scale OEMs), not a generic competitor. Where the threat is on the public record, inline-cite it too. A cell that says "largest player, well positioned" with no named threat is a stub — rewrite it; if you can't name a threat, you don't understand the position well enough to size conviction in it. **Keep moat + threat INSIDE the Justification cell — never as new columns** — to preserve the fixed 5-column parse contract that `list`/`mutate`/`refresh` rely on. If you can't articulate a one-sentence role with a citation, the ticker doesn't belong in the basket yet.

## Language (English default; Chinese opt-in)

**Default behavior: write the English file only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need a Chinese companion for every refresh.

- English (default): `reports/themes/<slug>_theme.md`
- Chinese (opt-in only): `reports/themes/<slug>_主题研究.md`

**Chinese opt-in (any of these triggers the Chinese companion alongside the English file):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

Once a Chinese companion exists for a theme, subsequent refreshes update both files unless the user says otherwise. The top-of-file **Languages tracked** metadata field records the current state (`en`, `en, zh`, or `zh`). The Tracked tickers table is **identical** across both files (same rows, same justifications — the citation URLs don't translate); only the prose sections (Thesis, Scope rules, Performance summary, Drift signals, Catalysts) are written natively in each language.

**Adding a Chinese companion to an existing English theme** (`build a Chinese version of <slug>`, `<slug> 主题中文版`, etc.): write the new `<slug>_主题研究.md` natively, copy the Tracked-tickers / Exclusions / Performance tables + all citation URLs verbatim from the EN file, and **in the same commit flip the EN file's `Languages tracked: en` → `en, zh`** so future refreshes know to update both. Source quotes inside Justification cells stay in their original PDF language regardless of the language wrapping them (an English broker quote stays English even inside Chinese prose).

Target word count: **2,000–4,000 words per language** (less than [[sector-overview]]'s landscape essay — themes are focused, not exhaustive).

## Data sources

### Primary (always-available)

- **yfinance** for price history, current price, sector classification, market cap. Use `auto_adjust=True` for performance comparisons.
- **`indicators.db`** for macro backdrop at refresh time (VIX, 10Y Treasury, HY OAS) — pulled once per refresh and referenced across the file.
- **`market_cap_cache.db`** for current market caps.
- **Existing research docs** at `reports/company/<Slug>/` — if a tracked ticker has a recent company-research doc, read it as structured input (not cited inline; surfaced in Data Used manifest).

### Issuer / event data

- **SEC EDGAR** for US issuers — recent 8-Ks for product launches, M&A, guidance changes.
- **cninfo (巨潮)** for A-share / HK issuers — 业绩说明会 PPT, 重大事项公告, 投资者关系活动记录表.
- **HKEX news room** for HK issuers.
- **Company IR sites** for the freshest deck disclosures.
- **`stock_price_target_db` (the canonical PT store, surfaced at `/pt`)** — when a refresh surfaces a sell-side **rating / price-target** call on a tracked name (from a zsxq PDF or a cited note), persist it via the existing helper `stock_price_target_db.upsert_target(row, replace=...)` (or `scripts/persist_pts.py`). Required keys: `company_ticker, company_name, research_institute, report_file_id, report_date` (plus `rating, price_target, target_currency, report_date_price` where known). It is idempotent on `(company_ticker × research_institute × report_file_id)`, auto-computes `upside_pct`, and surfaces the call at `/pt` alongside calls mined by the zsxq skills. The theme markdown keeps the prose mention + inline citation; the DB keeps the structured, queryable record — **do not invent a parallel PT table inside the theme file.** This is a Tier-2 write via the sanctioned helper, **never raw SQL**, per [`CLAUDE.md`](../../../CLAUDE.md) § Database Safety. Note it in the Data Used manifest as a store the refresh wrote to.

### News and sentiment

- **WebSearch** for recent press, industry-research notes (last 90 days for refresh window).
- **[[news-analyst]]** as a sub-step for high-value tickers when the user explicitly asks for sentiment scoring.

### Sell-side thematic notes (first-class seed + refresh source)

Broker thematic notes (Bernstein, MS, GS, UBS, and the user's zsxq library) are often the single richest seed for a theme — they supply the candidate ticker list, the conviction ranking, the multi-year TAM anchor, and the per-name moat/threat reads. Use them at **create** (seed selection) and **refresh** (re-mine for re-rankings and TAM revisions). Cite them two ways, never as a bare homepage:

1. **Source-chain the underlying number.** When the basket leans on a broker's TAM, forecast, or ranking, cite the chain so the reader sees primary-data → broker-model — e.g. `[Broker theme note 引用 Gartner/SEMI/trade-body data](deep-URL)`, not the broker's site root. (Same shape for any theme: a GLP-1 TAM chains through the epidemiology source the broker built on; a rare-earth volume through the trade-body data.) A broker number whose primary input is invisible is a half-citation.
2. **zsxq-backed notes cite via the file_id + page convention** already used by What's-New and snapshot `evidence_file_ids`: `[<broker> <title>, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)` (page in the link text is load-bearing — see *Local zsxq report library* § citation convention), and record the file_id in the refresh's snapshot line.

Project freshness still applies: discard broker notes older than ~12 months for selection (except founding facts). A revised TAM or re-ranking from a fresh note is itself `## What's New` material.

### Local zsxq report library (`db/zsxq.db`) — a first-class local source, mined at create AND refresh

The user's zsxq library is a **local cache of broker / sell-side PDFs** (`db/zsxq.db`, table `pdf_files`) — the single richest non-public seed for a basket. **Mine it directly from this skill** at both *create* (candidate names, conviction ranking, the TAM anchor, per-name moat/threat reads) and *refresh* (new broker calls, PT / rating revisions, re-rankings, TAM revisions) — do not lean on web search alone, and do not require the user to route through [[zsxq-ideas]] first. The same scripts the zsxq skills use are the data layer here; this skill only *reads* them (the DB is read-only — see Guardrails).

**Three mechanical steps** (all read-only on `db/zsxq.db`):

1. **Surface candidate reports — metadata only, no PDF open.** Two complementary lookups:

   ```bash
   # PRIMARY for a named theme — targeted query across the WHOLE library.
   # Run one --query per alias: each tracked-ticker code, English name, native
   # name, AND each theme-specific term (HBM3 / NOR Flash / cobot / GLP-1 …).
   # (Same tool company-research uses in its Step 0.7 — see that skill's
   #  § "Local institute-research library".)
   python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --query "<ticker-name-or-tech-term>" --limit 40

   # RECENCY window — recent feed for clustering (create) or "since last refresh".
   python3 .claude/skills/zsxq-recommend/scripts/list_recent.py --limit 300 --summary-chars 600
   python3 .claude/skills/zsxq-recommend/scripts/list_recent.py --since <Last-refreshed-date>   # refresh: only newer rows
   ```

   `find_pdf.py --query` and `list_recent.py --subject` are both a single case-insensitive LIKE across name/topic_title/summary/tags/comment. Use **`find_pdf.py` per alias** to seed a named theme (it searches the full library, not just the recent window); use **`list_recent.py`** for the recency-windowed jobs — clustering the recent feed at create, and pulling only rows newer than `Last refreshed` at refresh. Each row carries `file_id, bank, topic_title, summary, tickers, page_count, create_time, claude_rating`. Strict per-alias keywords are the right tool for an already-named theme; loose generic terms (AI / 算力 / data center) over-match off-theme reports and belong to *cluster-time* discovery ([[zsxq-ideas]]'s job).

2. **Build the extraction manifest** for the chosen cluster — it reports, per report, whether the original text is text-ready / OCR-cached / needs-OCR, and emits the exact extract command:

   ```bash
   python3 .claude/skills/zsxq-ideas/scripts/evidence_bundle.py \
       --file-ids <comma-sep file_ids> --slug <theme-slug> \
       --out /tmp/zsxq_evidence/<theme-slug>.md
   ```

3. **Read the ORIGINAL PDF text for anything you cite** (the `summary` is triage-only — see below). Most bank PDFs here are image-only (fitz returns nothing); OCR them first (sequential, to avoid SQLite write-contention on the sanctioned `ocr_text` cache), then extract:

   ```bash
   for f in <needs-ocr file_ids from the manifest>; do
       python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py --file-id $f
   done
   python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id <id> --header --max-chars 40000
   # still empty (pure charts)? render_pdf_pages.py + Read the PNG visually.
   # only if THAT fails too: fall back to the 翻译精华 summary, labelled as such.
   ```

**The curated `summary` (翻译精华) is the triage layer; the extracted original text is the citation source.** Read the `summary` first — for most rows it already carries the broker + rating + price target + valuation basis + 2–4 thesis points, enough to decide which PDFs are worth opening (same first-read company-research relies on in its Step 0.7). But the summary is re-translated and can drop or round numbers (e.g. "超5万亿美元" for a precise "US$5,454bn"), so **open the original text for any verbatim quote and for the load-bearing numbers** — the TAM anchor, PT derivations, and any figure woven into the Thesis / Justification cells / Recent events / Valuation snapshot. Every cited number must **string-match its source** (the OCR'd original text for body numbers; the summary only when the figure literally appears there and precision isn't at stake). Then cite it with the zsxq convention below, and record each mined `file_id` in the refresh's snapshot `evidence_file_ids`.

**zsxq citation convention (mandatory for every zsxq-sourced claim):**

- **file_id AND page:** `[<Bank> — <short topic>, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)`. `extract_pdf.py` marks pages as `===== Page N =====`, so every number has a known page. The **page in the link text (`p.N`) is the load-bearing part** — `p.N` is what reliably tells the reader where to look (a PDF downloaded to iPad may ignore the `#page=N` fragment); appending `#page=N` to the URL is harmless and is honored by native in-browser PDF viewers. **Route must be the direct-download `/zsxq/pdf/<file_id>/<filename>`** (paste `find_pdf.py`'s `pdf_url` field — it serves raw `application/pdf` so it opens/downloads natively on iPad) — **not** the `/zsxq/pdf-viewer/<file_id>` viewer page (returns HTML, won't download on iPad), and **not** the old `/zsxq-pdf/<file_id>` form (dead 404).
- **Quote the original-language source clause** carrying the number alongside the link (the printed English / Chinese / Japanese, NOT the summary's paraphrase). Match it verbatim to the extracted text; use `…` for elisions.
- **Cite the number, not the headline.** "MS sees Asia energy capex doubling by 2030" with no link is a non-citation; the figure needs the page-anchored link + the source quote.

This is the same convention [[zsxq-ideas]] uses (see its § *zsxq citation convention*). The boundary between the two skills: `zsxq-ideas` **theme-build mode** clusters the *whole feed* to discover and seed several baskets at once; **this skill mines the library for a single named theme** it is already building or refreshing. Either path produces the same basket file with the same citation discipline — so a user can say "build a theme on X" (this skill mines zsxq for X directly) or "build themes from my zsxq feed" (zsxq-ideas clusters, then hands each slug here).

## Workflow

### Step 0 — Identify intent

Parse the user input to one of the modes (create / refresh / mutate / list). When ambiguous, ask one short clarifying question — never assume "refresh" when the user might mean "create new".

For **create**: extract the proposed theme name + scope. If the user gave only a name, propose 5–10 candidate tickers with one-sentence justifications and confirm before building.

For **refresh**: resolve the slug. Case-insensitive match against `reports/themes/*_theme.md`; if multiple matches (e.g. `humanoid-robotics-sensors_theme.md` and `humanoid-robotics-actuators_theme.md`), ask which.

For **mutate**: confirm the change scope (add/drop ticker, rename, delete) and the affected slug before editing.

For **list**: scan `reports/themes/*_theme.md`, parse the top-of-file metadata line from each, emit a summary table.

### Step 1 (Create only) — Initial ticker set

For a new theme:

1. **Mine the local zsxq library first** (see *Local zsxq report library*). Run `list_recent.py` with a strict-keyword cut on the theme terms (pull 300–800 rows), rank the hits by relevance × bank quality × recency, build an `evidence_bundle.py` manifest for the strongest 5–15 broker PDFs, then OCR + `extract_pdf.py` their original text. The user's broker notes are the richest, freshest seed — they typically supply the candidate ticker list, the conviction ranking, the multi-year TAM anchor, and the per-name moat/threat reads in one place. Always check this *local* source before reaching for web search; if the library has nothing on-theme, say so and fall through to web research.
2. Web-search for the theme keywords + "pure play" / "leader" / "supplier" / industry-research notes from the last 12 months — to fill gaps the zsxq library didn't cover and to corroborate its broker calls.
3. Pull the latest 3 industry-research items naming participants in the space — and the multi-year TAM / spend forecast that anchors the Thesis (see *Thesis — lead with a quantified anchor*); a sell-side thematic note (often one of the mined zsxq PDFs) frequently supplies both the names and the anchor.
4. Cross-reference with [[sector-overview]] outputs if one exists for the broader sector.
5. Propose 5–10 candidate tickers, each with: ticker / name / role / one-sentence justification / one inline citation to a source naming them as a participant (prefer a page-anchored zsxq `file_id` citation where a mined broker PDF names the ticker).
6. **Surface the proposed list to the user before writing the file.** Themes are most valuable when the user has agreed to the scope; pre-committing to a 10-ticker basket without confirmation creates drift the user didn't sign up for.
7. On confirmation, write `<slug>_theme.md` with the full structure described above. Run Step 4 (refresh data pass) immediately so the new file has live numbers. Seed the snapshot sidecar's `evidence_file_ids` with the zsxq `file_id`s mined in step 1.

### Step 2 (Refresh) — Pull updated data

For every ticker in the **Tracked tickers** table:

1. Pull latest price + return since `Last refreshed` from yfinance.
2. Pull current market cap + sector + valuation multiples.
3. Scan for material 8-K / 公告 / press-release events since `Last refreshed`.
4. **Re-mine the local zsxq library** (see *Local zsxq report library*) for broker notes published since `Last refreshed`: `list_recent.py --limit 800 --subject "<tracked-ticker-name-or-theme-term>"` (strict keywords, NOT loose generic terms), exclude `file_id`s already in the prior snapshot's `evidence_file_ids`, then OCR + `extract_pdf.py` the new on-theme reports. These drive new PT / rating calls (→ `## Valuation snapshot` + a `stock_price_target_db` upsert), conviction re-ranks, TAM revisions, and `## Recent events` entries. String-match every number to the extracted original text; cite with the page-anchored zsxq convention.
5. Compute theme-aggregate performance (cap-weighted basket return; equal-weighted basket return; vs benchmark).
6. Pull `indicators.db` snapshot (VIX, 10Y, HY OAS) for the regime backdrop.
7. Pull the theme's 2–4 **leading indicators** — the upstream volume / price / capacity / guidance series that lead the members (and each member's own most-recent guidance on the shared forward metric) — with latest readings + as-of dates. These populate the `## Leading indicators` block and are the first place the thesis cracks. **Template the block as a per-ticker OPERATING-DATA table** (Bernstein *The Barometer* spine): per name, the latest monthly/quarterly operating print — unit shipments YoY/MoM, order-book growth, penetration %, capacity adds — each string-matched to its primary issuer (NE Times monthly shipments, company monthly disclosure, customs/trade-body data) and cited inline. Keep the 2–4 macro/upstream signals as header rows above the per-name rows.

### Step 3 (Refresh) — Surface drift signals

Drift detection is the value-add of refresh. Surface:

- **Theme exposure shift** — if a ticker's segment mix has moved away from the theme (e.g. a sensor company spinning off its sensor business). Flag and propose `role` change or removal in the **Tracked tickers** table.
- **New entrants** — tickers named in recent industry research that aren't in the basket. Propose for next mutation (don't auto-add).
- **Underperformer outliers** — tickers > 30% behind the basket median return over the refresh window. Surface the reason (idiosyncratic news, sector rotation, broken thesis).
- **Stale justifications** — if a ticker's Justification cell references a source older than 12 months, flag for re-grounding in the next mutation.
- **Valuation drift** — for each `core`/`adjacent` name, report the forward multiple (P/E, or the sector-appropriate one — EV/EBITDA, P/S for pre-profit) on **two relative axes**: vs the name's own ~10yr (or max-available) average, AND vs a stated sector/market benchmark — e.g. `<name> 37.5x fwd vs 10yr avg 17.7x; +36% vs <sector ETF>, +71% vs SPX`. When the **basket-median** multiple sits materially above its own history, raise an explicit **priced-for-perfection / air-pocket flag** and name the **specific demand assumption** — tied to the Thesis TAM anchor — whose disappointment would trigger a de-rate (a named line, not an abstract caveat: GLP-1 7–8mo avg therapy duration; memory price normalizing 2028; robotaxi federal-approval cap). A bare multiple with no own-history and benchmark context is a defect.

### Step 4 (Refresh / Create) — Update the file's data-driven sections

**First, compute the delta** so the refresh is trackable: read the last line of `<slug>_theme.snapshots.jsonl` (the prior state), set-diff its `tickers` against the current set, compare `perf`, and note `evidence_file_ids` not seen before. That delta drives the `## What's New` block. (On a create-pass there's no prior line — the delta is "basket created".)

Rewrite the following sections of `<slug>_theme.md` in place:

- **What's New** — **prepend** a dated block with the computed delta (tickers added/dropped/role-changed, biggest movers vs benchmark since last refresh, new broker calls/catalysts, **TAM revisions** (anchor old→new + named driver), thesis drift); roll the previous block into the `<details>` archive. Keep it to ~5–8 linked bullets.
- **Performance** — movers / laggards / benchmark comparison for the refresh window, plus the **Basket scorecard** (MS *Three Actionable Ideas* style): batting average (% of names positive over the window, % beating the benchmark), best/worst named contributor with their return, and — where `snapshots.jsonl` has ≥2 lines — cumulative basket outperformance in bps since inception. All derived from yfinance + the snapshot history.
- **Recent events** — bulleted list of material press releases / filings since the previous refresh, each inline-cited.
- **Drift signals** — output of Step 3.
- **Leading indicators** — refresh the 2–4 upstream signals from Step 2.6 (incl. side-by-side member guidance on the shared forward metric); cross-reference any indicator that has rolled over while the basket still rises in **Drift signals**.
- **Catalysts** — each as event + transmission mechanism + timing window + which TAM sub-bucket / tracked name it moves (never a bare calendar entry).
- **Data Used / 数据来源清单** — refreshed manifest with new as-of dates.
- **References** — append any new URLs cited above.

**Then append one line to `<slug>_theme.snapshots.jsonl`** capturing the new state (date, full ticker set + roles, perf vs benchmark + since-last-refresh, evidence_file_ids, n_events, one-line note) — this is what the *next* refresh diffs against. Update the `**Last refreshed:** YYYY-MM-DD` field in the top-of-file metadata.

**Retroactive baseline**: if the theme pre-dates the snapshots-sidecar convention and `<slug>_theme.snapshots.jsonl` doesn't exist yet, write **two** lines in the same commit — a synthetic baseline reconstructed from the prior `## History` line / git blame (`note: "baseline (..., superseded same day)"`) followed by the current refresh line. This gives the next refresh a real diff target instead of treating an old theme as freshly-created.

**Citation audit** is part of every refresh, not optional: before writing the new content, walk each prior `zsxq #<file_id>` citation in the file and `head` the corresponding extracted PDF (`extract_pdf.py --file-id <id> --pages 1`) to confirm the file is what it's labelled as. This caught a real mis-attribution (`#812485545245152` had been tagged "MS Hua Hong AAI" but is in fact MS 同仁堂 / Tongrentang — a TCM company). Remove and re-ground anything that doesn't survive the audit; note the fix in `## History`.

Do **not** rewrite the Thesis, Scope rules, Tracked tickers, Exclusions, or Keywords sections during a *plain* refresh — those are stable. Two exceptions where they DO get rewritten, each requiring user confirmation:

### Step 4b — Expansion refresh (sourcing-widening + basket grow)

Neither a plain refresh (data only) nor a plain mutate (tickers only). Triggered by phrasings like `widen sourcing on <slug>`, `expand the <slug> basket`, `rebuild <slug> from the original PDFs`, or when a refresh's Step 3 drift scan surfaces ≥1 ticker with conviction-grade broker coverage that wasn't in the basket. Workflow:

1. **Re-mine the source library wider than the original cluster.** For zsxq-backed themes that means a *strict-keyword* search of the recent ~600–800 DB rows on (a) tracked-ticker names/codes AND (b) theme-specific terms (HBM / NOR / SST / cobot / GLP-1 …) — not the loose generic terms (AI / data center / 算力) that cluster-time keyword matches use. Loose keywords are the right tool for *clustering*; strict keywords are the right tool for *refresh-mining* an already-named theme, because they pick up reports that cover known tickers under terminology the original cluster missed. Concretely (per *Local zsxq report library*): `python3 .claude/skills/zsxq-recommend/scripts/list_recent.py --limit 800 --subject "<term>"` per strict term, union the hits, drop `file_id`s already in the theme's `evidence_file_ids`, then `evidence_bundle.py` → OCR → `extract_pdf.py` the survivors and read their original text.
2. **Surface candidate adds (with conviction-grade evidence) to the user** before editing the Tracked tickers table. Each candidate gets a one-line justification quoting the broker call from the original PDF (e.g. *"MS upgrades Winbond and Nanya to OW"* → propose `TPE:2408` as core). The user confirms which to add — basket changes remain user-confirmed.
3. **Rewrite the Thesis** to incorporate the new conviction (this IS the exception to the "stable across refresh" rule — but only because the user opted in). Re-anchor each Thesis claim with page-cited quotes from the original PDFs.
4. **Recompute Performance for the new basket size** (Step 4 mechanics) and append a snapshot line whose `note` describes the expansion (e.g. `"expanded 14->16 (added 2408.TW core, 301308.SZ adjacent); 22 reports cited from OCR'd original PDF text"`).

The output is *one* theme file (+ Chinese companion if tracked), not a new file — `update-in-place` still holds.

### Single-theme vs multi-theme execution

For a **single-theme** rebuild (one theme at a time), prefer **direct edits** by the main loop over an agent fan-out — the agent round-trip overhead and the post-agent reconciliation pass (verifying every quote, rebuilding the snapshot, fixing partial state) costs more wall-clock than just doing the edits. Reserve agent fan-out for genuinely parallel multi-theme work (`refresh all my themes`, `build 7 themes from this cluster`).

### Step 5 (Mutate) — Tracked-tickers-table edits

For add / drop / role-change / rename:

1. **Edit the Tracked tickers table directly** (using the `Edit` tool on the markdown file). Add a row, remove a row, or change a single cell. Never rewrite the whole file for a mutation.
2. **Append a one-line entry to the `## History` section** at the bottom of the file:
   ```
   - YYYY-MM-DD — added <ticker> as <role> — <one-line reason>
   - YYYY-MM-DD — dropped <ticker> — <one-line reason>
   - YYYY-MM-DD — changed <ticker> role from <old> to <new> — <reason>
   - YYYY-MM-DD — renamed slug from <old> to <new>
   ```
3. **Do NOT regenerate the file's data-driven sections** (Performance / Recent events / Drift signals / Catalysts) unless the user explicitly says "also refresh the data". Mutations are cheap; refreshes are expensive — they pull market data, scan filings, and rewrite multiple sections.
4. **Prepend a one-line bullet to `## What's New`** (e.g. `**2026-06-15 (mutation):** added SZSE:300354 Donghua (core).`) and **append a snapshot line** to `<slug>_theme.snapshots.jsonl` with the new ticker set, `perf` carried over from the last refresh, and `note` = the mutation. This keeps the change visible in the trackability trail without a full data refresh.
5. Update `**Last mutated:** YYYY-MM-DD` in the top-of-file metadata. Do not bump `Last refreshed` — that's a different cadence and would be misleading.

### Step 6 — Write or update files

Per the language defaults: English file by default; Chinese companion only when the user opts in. The Tracked tickers table stays in lockstep across both language files when both exist.

Save:
- `reports/themes/<slug>_theme.md` (English default — always present)
- `reports/themes/<slug>_主题研究.md` (Chinese — present only when opted in)
- `reports/themes/<slug>_theme.snapshots.jsonl` (always — append one line per create / refresh / mutate; language-independent, shared across en/zh)

Charts (**required minimum set of ≥3** — see the **## Charts** section): rendered to `reports/charts/theme_<slug>_*.png` per the project Chart rules, then embedded in the file.

### Step 7 — Verify

- Re-parse the top-of-file metadata line to confirm the format is intact (dates parse, languages-tracked field valid).
- Re-parse the Tracked tickers table to confirm row count and column structure are intact.
- Confirm the `## What's New` block has a new dated entry and the prior one rolled into the archive.
- Confirm exactly one new line was appended to `<slug>_theme.snapshots.jsonl`, it is valid JSON, and its `tickers` set matches the current Tracked tickers table.
- Spot-check ≥3 ticker performance numbers in the Performance section vs yfinance.
- Confirm all inline URLs in the file return HTTP 200 (sample 5).
- Stop any test servers used during chart rendering.

## Output Format (mandatory blocks in every theme file)

Every `<slug>_theme.md` must contain, in this order:

1. **H1 title** with English name and (when relevant) Chinese name.
2. **Top-of-file metadata line** (Created · Last refreshed · Last mutated · Refresh cadence · Languages tracked).
3. **## What's New** (refresh/mutate-driven delta — newest block on top, older blocks in a `<details>` archive; the "what did I know before, what's new" surface).
4. **## Thesis** (200–400 words) — **opens with the quantified TAM / spend anchor** (dated multi-year trajectory + sub-bucket decomposition + swing factor; see *Thesis — lead with a quantified anchor*).
5. **## Scope rules** (100–200 words).
6. **## Tracked tickers** table (mandatory columns: Ticker | Name | Role | Justification | Added).
7. **## Valuation snapshot** table (mandatory when ≥1 tracked name has sell-side coverage — per-name Rating / PT / Upside% / fwd multiple vs own ~10yr avg / FY1·FY2 EPS; a *separate* table, never new columns on Tracked tickers; the in-file mirror of `stock_price_target_db`).
8. **## Exclusions** table (optional but recommended — explicit "we considered this and rejected it").
9. **## Keywords** — bilingual where natural.
10. **## Performance** (refresh-driven) — includes the **## Basket scorecard** discipline: batting average (% of names positive, % beating benchmark), best/worst named contributor, and cumulative outperformance in bps where ≥2 snapshot lines exist (mirror MS *Three Actionable Ideas*; see *Learning from sell-side institutional research*).
11. **## Recent events** (refresh-driven).
12. **## Drift signals** (refresh-driven — the value-add).
13. **## Leading indicators** (refresh-driven — the early-warning layer; 2–4 upstream signals that lead the members, incl. side-by-side member guidance on the shared forward metric).
14. **## Catalysts** (next 3–6 months, refresh-driven — event + mechanism + timing + which sub-bucket).
15. **## Data Used / 数据来源清单** (manifest — see block below).
16. **## References** (every URL cited inline).
17. **## History** (mutation log; append-only).

Plus a **required minimum set of ≥3 charts** (see the **## Charts** section) embedded in the file and listed in Data Used.

Plus the **`<slug>_theme.snapshots.jsonl`** sidecar (one JSON line per create/refresh/mutate) — not part of the md, but mandatory and committed alongside it.

### Further viewing — explainer videos (optional, but default to including)

When this theme covers something a reader would struggle to picture from prose alone — the theme's core technology (humanoid-robot tactile sensors, advanced-packaging (CoWoS) die stacking, solid-state battery construction, a GLP-1 mechanism), a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any theme; omit only when the theme is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in (typically `## Thesis`), or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Market data**
- yfinance auto_adjust=True for prices, returns, market cap, sector — pulled YYYY-MM-DD.
- market_cap_cache.db as of YYYY-MM-DD.

**Per-ticker primary sources**
- <ticker>: latest 10-K (filed YYYY-MM-DD) / 年度报告 (filed YYYY-MM-DD); IR materials YYYY-MM-DD; press releases since last refresh.
- ... one bullet per tracked ticker.

**Industry research / sell-side thematic notes (theme-level)**
- <research-firm + report title + publication date + URL> — used for ticker selection, the TAM anchor, conviction ranking, and drift detection. Source-chain the broker's TAM/forecast to its primary data (Gartner / SEMI / trade body / gov stats); zsxq notes cite via `file_id`.

**Local zsxq library (`db/zsxq.db` — read-only)**
- <N> broker PDFs mined for this theme (file_ids: …) via `find_pdf.py` / `list_recent.py` → `evidence_bundle.py` → `extract_pdf.py` (image-only ones OCR'd first). The 翻译精华 summary was the triage read; load-bearing numbers were cited from the extracted original text. "none — library had no on-theme reports this pass" if nothing matched.

**TAM anchor + leading indicators (theme-level)**
- <forecaster + pool + dated multi-year trajectory + URL> — the Thesis anchor and its sub-bucket decomposition.
- <2–4 upstream leading indicators, each + latest reading + as-of date + primary issuer> — populate `## Leading indicators`.

**Macro backdrop**
- VIX, 10Y Treasury, HY OAS as of YYYY-MM-DD. Source: `indicators.db`.

**Cross-coverage**
- [reports/company/<Slug>/...md](../company/<Slug>/...md) (last updated YYYY-MM-DD) — read as structured input for the <ticker> paragraph, not cited inline.

**Stores written (Tier-2 helpers)**
- `stock_price_target_db` — <N> sell-side PT / rating calls upserted for tracked names (idempotent on ticker × broker × file_id); surfaced at `/pt`. "none" if no new calls this refresh.

**Stale notices / coverage gaps**
- <bulleted list — ticker without recent IR refresh, missing third-party source for a candidate, or "none">.
```

## Charts (required minimum set)

A theme that ships zero charts under-delivers versus the professional notes it competes with, and the project's global Chart rules apply to *every* chart-producing skill. Every theme renders **at least three** PNGs to `reports/charts/theme_<slug>_*.png`, embedded in the file (or linked) and listed in the Data Used manifest:

1. **Anchor trajectory + sub-bucket decomposition** — the TAM / spend path as a (stacked) bar with the swing-factor sub-bucket broken out (WFE → DRAM / NAND / Logic / WLP; a GLP-1 theme → script volume by formulation; rare earths → magnet tonnage by grade). On a refresh that revised the anchor, overlay old vs new.
2. **Basket performance vs benchmark** — equal-weight (and median) basket return vs the stated benchmark over the refresh window.
3. **Valuation vs own history** — each `core` name's forward multiple as a bar against its own ~10yr average (the visual of the priced-for-perfection flag).

4. **Supply/demand balance — REQUIRED for any imbalance (shortage / glut / utilization) thesis.** Plot the **demand series and the supply/capacity series in the same units** (mm², kt, sheets/mo, units) as bars/lines, with the S/D ratio (or gap%) as the derived overlay — never the ratio alone (it is a derived series; the global Chart rule demands its components be shown). This is the visual of the auditable two-sided balance from the Thesis. For non-imbalance themes this slot is optional.

Apply the global Chart rules **verbatim**: an in-image source-footer annotation (required, not optional), x-axis clipped to the data range, the latest point covering "now", and for any derived series the component series plotted too (a bare S/D-ratio or ERP line with no component series is a defect). Render headless (matplotlib `Agg`) — static PNGs need no server; only stop a server if you started one. Add every chart path to the Data Used manifest. (Three is the floor — anchor, performance, valuation; a fourth S/D-balance chart is required for imbalance theses; a content-ladder or scenario-fan chart is encouraged.)

## Learning from sell-side institutional research

The tracked-basket notes the pros publish (MS *Three Actionable Ideas*, GS *Conviction List / Directors' Cut*, Bernstein *The Barometer*, JPM TAM-anchored thematics, Bernstein value-chain teardowns) share a discipline a watchlist lacks. Fold these into the sections noted — they sharpen existing rules, they don't replace them. Every figure still obeys the project numerical-accuracy + paragraph-citation rules: scorecard numbers derive from yfinance prints already in Data Used; scenario PTs and TAM-revision magnitudes cite the originating note; the analyst's own model is never the source.

- **Print the batting average — mirror MS *Three Actionable Ideas*.** A tracked basket carries a standing scorecard, not just a basket-vs-benchmark return: **% of names positive** over the refresh window, **% beating the stated benchmark**, the **best and worst contributor** (named, with their return), and — where the snapshots sidecar has ≥2 lines — **cumulative basket outperformance in bps since inception**. MS prints theirs even at a ~50% hit rate (54% positive / 50% beat benchmark, cumulative +9,428 bps, avg 12m relative +7.3%); credibility comes from showing the average, not hiding it. Compute all of it from yfinance + the `snapshots.jsonl` history — no new data source. Render it as a `## Basket scorecard` block (or extend `## Performance`). *A tracked basket with no batting-average is a watchlist, not a tracked basket.*

- **Frame the anchor and the core names bull/base/bear — mirror GS *Robotaxi* fleet paths + JPM Insta360 *"The View from 2030"*.** Beyond the single anchor trajectory, state an **up-case and down-case out-year** with the **single swing assumption** that moves between them, and — JPM-style — **enumerate the conditions that must ALL hold for the bull case** (Insta360: coexistence + category break-out + margin recovery). Where a tracked name carries sell-side coverage that gives a **bull/base/bear PT triplet** (MS Hesai $53 / $30 / $11.5; WULF $103 / $66.5 / $15), capture all three in the `## Valuation snapshot` cell, each citing its originating note. Anchor up/down cases cite the forecaster's high/low or are labelled *"Analyst view (this note)"* per the own-model-is-not-a-source rule. Add this as a scenario clause in `### Thesis` after the sub-bucket decomposition.

- **Size the value-chain map, don't just list it — mirror Bernstein *AI Value Chain* ($/rack teardown) + *The Bonder War*.** Upgrade the bare layer list into a **dollar-weighted value-capture map**: for each layer give its **share of the theme's dollar pool** (or a unit-economics anchor — $/rack, $/GW, $/kg API, cost-per-watt) and the **named leading supplier + that supplier's share** (Besi ~91% hybrid-bonding; the GPU $4m vs memory $3.2m vs networking $1.2m split per AI rack). Then **explicitly flag any rich-dollar layer where the basket has NO tracked exposure** as a candidate-add signal — this sharpens the existing "process step no tracked name occupies is a coverage gap" line into a dollar-weighted one. For commodity-input themes, force the **bit-share vs value-share distinction** (JPM memory: China ~18–19% bit-share but only ~10–12% value-share — quantity participation can be a value-capture trap).

- **Stage *who benefits when* — mirror GS *Robotaxi* (GM turns positive 2027–28) + MS AI-compute (CoWoS 2027, CPO mass-production 2027).** The role taxonomy is static; add a **time axis**. Sequence the basket along the multi-year anchor curve: which roles monetize **first** (enablers / equipment ride the build-out) vs **later** (end-product names), each with a **dated gate** — UE-breakeven year, gross-margin-turns-positive year, a penetration-% threshold. Map each tracked name to its stage. Add this as a short paragraph in `### Thesis` (after the swing-factor) and a one-line cross-reference in `### Ticker role taxonomy` — no new table column.

- **Make the leading-indicators block a per-ticker OPERATING-DATA table — mirror Bernstein *The Barometer*.** Today `## Leading indicators` is narrative; operationalize it as a **per-name monthly/quarterly operating print** (unit shipments YoY/MoM, order-book growth, penetration %, capacity adds) — the spine of the Barometer (NEV wholesale +10% YoY, robot-reducer output +38% YoY, LiDAR shipments +177% YoY, L2+/L3 penetration 40.6%). Keep the 2–4 macro/upstream signals as header rows. **String-match every print to its primary issuer** (NE Times monthly ADAS-SoC shipments, company monthly disclosure, customs data, trade-body GWh) and cite inline — the broker note is never the original number, it points one layer deeper.

- **Name the customer-insourcing threat AND the incumbent's counter — the dominant 2026 theme risk.** OEMs / hyperscalers self-designing the component is the modal threat across the library: BYD / NIO / XPeng / Li in-house ADAS chips vs Horizon; Google / Amazon / MS ASICs vs Nvidia. Credible incumbents have a **named counter** (Horizon's near-100%-margin BPU IP-licensing pivot; a third-party's irreplaceability for sub-scale OEMs). Where relevant, the Justification cell must name the **insourcing threat AND the structural counter**, not a generic competitor.

- **Quantify the TAM revision and name the air-pocket trigger — mirror JPM/Bernstein revision prints.** A `## What's New` TAM-revision bullet carries an **explicit % magnitude**, not just an old→new level (JPM memory *"TAM raised +37% to $1.7trn 2028E, driver = CPU DRAM bit-demand"*; Bernstein battery 2030 +~10%). And the priced-for-perfection flag in Drift signals names the **specific demand assumption whose miss de-rates the basket** (GLP-1 7–8mo avg therapy duration; memory price normalizing 2028; robotaxi federal-approval cap) — a named line, not an abstract caveat.

- **Symmetric, ordered, density — close like the desk does.** Pair **dated UPSIDE and DOWNSIDE risk bullets** (Bernstein Barometer, GS Yankuang, UBS heavy-truck) — symmetric, not a one-sided bull pitch. Render the Valuation-snapshot rating line at MS/HSBC density — **rating, current price, PT, and computed upside% on one line** (HSBC Korea: Samsung *Buy TP 450k vs 349k = +29%*). Express any conviction preference as an **ordered ranking with a one-clause why per rung and the swing variable named** (Citi battery: *lithium-resource > cathode > cell > electrolyte > separator*). And put **self-correction on the record** — the `## What's New` delta should narrate a `prior view → revised view` line (JPM DiDi: *"we cut to Neutral in March; the 1Q print pauses the loss-spiral"*).

- **Optional scenario / staging chart.** When the theme carries bull/base/bear scenarios or a staged-beneficiary curve, render a **4th chart** — a scenario fan (anchor up / base / down out-year paths) or a beneficiary-timeline strip — with the in-image source footer per the global Chart rules. Surfaces the new scenario/staging structure visually; the ≥3-chart floor (anchor / performance / valuation) is unchanged.

## Guardrails

- **A tracked basket without a batting-average is a watchlist.** A refresh that reports basket-vs-benchmark return but no hit-rate discipline (% of names positive, % beating the benchmark, best/worst named contributor, cumulative bps since inception where ≥2 snapshot lines exist) is incomplete — the scorecard is the signature of a *tracked* basket. Compute it from yfinance + `snapshots.jsonl`.
- **Risk bullets are symmetric and the value-chain map is dollar-weighted.** Every refresh closes with paired dated upside AND downside risks (not a one-sided bull pitch), and the value-chain map sizes each layer's dollar/margin pool with the named leading supplier's share — flagging any rich-dollar layer the basket has zero exposure to as a candidate-add.
- **Themes drift.** A 6-month-old basket may no longer reflect the original thesis. Always run the refresh workflow before quoting performance — never cite stale tickers as "the current theme".
- **Ships ≥3 charts and a valuation snapshot.** A theme with sell-side coverage but no `## Valuation snapshot` table, or with zero charts, is incomplete — the structured data (PTs in the DB, the anchor trajectory) must have a surfacing object in the file, not just live in a database or in prose.
- **Pure-plays beat conglomerates for theme tracking.** Tesla in a humanoid theme is mostly noise; an SOC supplier with 80% humanoid exposure is signal. The `role: core` tag should be rare; `adjacent` and `enabler` are the more common labels.
- **Every ticker has a written justification.** No "obvious" additions. If you can't articulate the role in one sentence with a citation, the ticker doesn't belong yet.
- **The Thesis leads with a quantified, sourced anchor.** A theme whose thesis states no dated, third-party-sourced TAM / spend / volume trajectory is not ready to ship — the anchor is what makes the bet falsifiable and the drift-check meaningful. The analyst's own model is never the anchor's source.
- **Every Justification cell names a moat AND a threat.** "Largest player, well positioned" with no named competitor / substitute / policy threat is a stub — if you can't name what breaks the position first, you can't size conviction in it. Where relevant, the threat must include **customer-insourcing** — the OEM / hyperscaler self-designing the component (the modal 2026 risk: BYD/NIO/XPeng/Li in-house ADAS chips vs Horizon; Google/Amazon/MS ASICs vs Nvidia) — paired with the incumbent's **named structural counter** (e.g. Horizon's near-100%-margin BPU IP-licensing pivot; irreplaceability for sub-scale OEMs), not a generic competitor.
- **Performance comparisons need a stated benchmark.** "The basket is up 22%" is meaningless without "vs S&P 500 +14% / CSI 300 +8% over the same window".
- **Multiples are relative, never bare.** Every quoted valuation multiple carries both its own-history comparison and a benchmark comparison. A basket trading rich vs its own history must carry a priced-for-perfection / air-pocket flag tied to the Thesis TAM anchor — the same way performance carries a benchmark.
- **The anchor is an auditable build, not a cited total.** Where the seeding note discloses the drivers, the Thesis must reproduce the bottom-up `units × content` build that sums to the headline pool, and — for any shortage/glut/utilization thesis — a **two-sided demand-vs-supply balance** (both series in the same units, ratio as the quotient), not just the quoted gap%. A headline TAM or an S/D ratio with no visible build/components behind it is a half-anchor the reader cannot stress-test.
- **Size the de-rate, don't just name the trigger.** The priced-for-perfection flag must translate the rich multiple into an **implied downside %** — reversion to the name's own-history average multiple, or to the lowest credible PT / cited bear case — with the floor sourced (e.g. *"29.6x vs 10.3x upcycle avg → −41% to the bear PT"*). A trigger ("de-rates if X disappoints") with no magnitude gives the reader nothing to act on.
- **Valuation snapshot is FY1+FY2, own-avg-for-every-name, and as-of-dated.** A snapshot showing a single forward year, an own-avg column populated for only a subset, or fresh and stale PTs blended into one Upside% column is incomplete — segregate stale PTs and add a growth-adjusted metric (PEG / EV-EBITDA) so the basket sorts like-for-like.
- **Drift signals are the deliverable.** A refresh that doesn't surface any drift signals after 90 days of market action is a defect — go back and look harder.
- **Catalysts carry a mechanism, not just a date.** A dated event with no transmission story to the TAM anchor or a named tracked ticker is a calendar entry, not a catalyst — it doesn't belong in the Catalysts section. For **regulated-product themes** (medtech / biopharma / defense) the highest-signal catalysts are **approval milestones** (FDA PMA / 510(k) / De Novo / IDE readouts, NMPA, CE-MDR) and **reimbursement / pricing decisions** (US DRG/CPT coding, China 医保 / provincial pricing, Japan reimbursement) — each gates revenue directly, so cite the deciding body + expected window.
- **Conviction rankings are sourced, never self-authored.** Any ordered preference over basket members cites a named external analyst; the agent's own read is labelled "Analyst view" and kept visibly separate. (The project rule: the skill's own model is not a source.)
- **Do not silently mutate the Tracked tickers table.** Every mutation carries a corresponding `## History` line with the date + reason.
- **Do not use a theme to chase performance retroactively.** Don't add a ticker to the basket "because it's been ripping for 3 months" — only add if it fits the original thesis. Performance-driven additions destroy the analytical value.
- **Do not regenerate the file's data-driven sections on every mutation.** Mutations are cheap; refreshes are expensive. Only refresh the data when the user explicitly asks or the data is materially stale.
- **Do not rewrite the Thesis or Scope rules during a refresh.** Those are stable across refreshes; changing them is a deliberate thesis re-grounding that requires user confirmation.
- **Do not invent industry-research citations.** Every named research firm + report needs a real, verifiable URL.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".
- **The local zsxq library is read-only.** Mine `db/zsxq.db` via the existing read-only helper scripts (`find_pdf.py` / `list_recent.py` / `evidence_bundle.py` / `extract_pdf.py` / `ocr_pdf.py`) — never write to it, never raw SQL (the `ocr_text` cache write inside `ocr_pdf.py` is the sole sanctioned exception, and only that script does it). Read the 翻译精华 `summary` for triage, but cite the **load-bearing numbers (TAM anchor, PTs, any figure in the Thesis/Valuation snapshot) from the extracted original text**, string-matched to the source before committing. A theme that cites zsxq report *titles* but never the broker calls *inside* them defeats the point of sourcing from the local library.

## Output location

Save to `reports/themes/` under the project root. Create the directory if missing (first theme establishes it).

**Flat layout** (matches the rest of your `reports/` tree — sector, compare, earnings, take-profit, ma, regulatory, etf all use flat layouts; only `reports/company/` uses per-slug subdirectories):

```
reports/themes/
├── humanoid-robotics-sensors_theme.md           # English (default)
├── humanoid-robotics-sensors_主题研究.md          # Chinese (opt-in only)
├── glp1-supply-chain_theme.md
├── advanced-packaging_theme.md
└── ...
```

Charts live in the existing `reports/charts/theme_<slug>_*.png` location, **not** alongside the theme file. They are a **required minimum set** (≥3 per theme — see the **## Charts** section), not optional.

### Update-in-place rule

One English file and one Chinese file (when opted-in) per slug, plus one `<slug>_theme.snapshots.jsonl` sidecar. Refresh and mutate update them **in place** — never create dated parallel copies (`_2026-06-30.md`), which would duplicate the ticker table, drift apart, and clutter the viewer.

Trackability ("what did I know before, what's new?") is delivered **without** dated copies, by three layers:
- **`## What's New`** — the human-facing delta at the top of the live file (newest refresh on top, older in the archive).
- **`<slug>_theme.snapshots.jsonl`** — the machine record (one state-vector line per refresh; the next refresh diffs against it).
- **git** — full point-in-time recall: `git show <sha>:reports/themes/<slug>_theme.md` reconstructs any past state; `git log -- <slug>_theme.snapshots.jsonl` lists every refresh. The `## History` section remains the narrative log of intentional changes.

If the same theme conceptually exists under multiple slugs (e.g. `humanoid-robotics_theme.md` and `humanoid-robotics-sensors_theme.md`), the **narrower** slug wins. Promote the broader slug's content into the narrower one and delete the broader file (ask the user first).

## What this skill does NOT do

- It does not produce a one-shot industry essay — that's [[sector-overview]].
- It does not produce a head-to-head comparison of theme members — that's [[compare-companies]] (run on a 2–4 subset of the basket).
- It does not produce a deep dive on any single member — that's [[company-research]] (run on the ticker; the theme file links to it).
- It does not auto-add or auto-drop tickers based on performance. All Tracked tickers table changes are user-confirmed.
- It does not produce a sized portfolio recommendation. A theme is *what to watch*, not *how much to hold* — sizing is [[trader-plan]] / [[portfolio-decision]] territory.
- It does not predict the theme's outperformance vs benchmark. Performance is *reported*, not forecast.
- It does not maintain alerts or notifications. The "Refresh cadence" in the top-of-file metadata is informational only; the user runs the refresh manually (or via [[loop]] for periodic automation).
- It does not introduce YAML, TOML, or any non-markdown file format. Everything is markdown that renders natively at `localhost:5001/reports`.

## Prerequisites

No machine-enforced upstream skills — these are already-installed sibling skills whose **read-only** scripts are the local zsxq data layer this skill mines at create and refresh (see *Local zsxq report library*):

- [[zsxq-recommend]] — `scripts/list_recent.py`: recent-feed metadata pull + strict-keyword cut over `db/zsxq.db` (surfaces candidate `file_id`s; no PDF open).
- [[zsxq-analyze]] — `scripts/find_pdf.py` (per-alias targeted query across the whole library — the primary surfacing tool for a named theme) + `scripts/extract_pdf.py` (original page-marked PDF text) + `scripts/ocr_pdf.py` (OCR image-only bank PDFs into the sanctioned `ocr_text` cache) + `scripts/render_pdf_pages.py` (visual fallback for pure-chart pages).
- [[zsxq-ideas]] — `scripts/evidence_bundle.py` (per-cluster extraction manifest: text-ready / OCR-cached / needs-OCR status + the extract command per report) and its **theme-build mode**, the feed-clustering front-door that seeds *several* baskets at once; this skill instead mines the library for a *single named* theme. Both write the same basket format with the same citation discipline.

The DB itself is read-only from this skill — the only sanctioned write anywhere in the chain is `ocr_pdf.py` populating its own `ocr_text` cache. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".
