---
name: theme-research
description: Build and maintain thematic equity baskets (e.g. humanoid-robotics-sensors, GLP-1 supply chain, advanced packaging, EV battery) — each theme is a single English markdown file at `reports/themes/<slug>_theme.md` containing the tracked-tickers table (ticker, role, justification, added-date), thesis, performance, drift signals, and Data Used manifest (Chinese companion `<slug>_主题研究.md` available on explicit request). The skill creates new themes, refreshes existing ones with movers/laggards + recent news + valuation drift, and surfaces drift signals (tickers no longer fitting; new tickers worth adding). Distinct from `sector-overview` (one-shot landscape essay) — themes are *tracked baskets* that get refreshed. Use when the user says "build a theme on X", "track the X basket", "refresh my <theme> basket", "what's moving in my <theme>?", or "what themes do I have?"
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
- **New broker call:** GS initiated Anpeilong Buy, PT ¥120 ([GS, zsxq #...](http://xs-macbook-air.local:5001/zsxq/pdf-viewer/...)).
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

## Recent events

<refresh-driven; bulleted list of material 8-K / 公告 / press releases since last_refreshed, each inline-cited>

## Drift signals

<refresh-driven; the value-add of refresh — flag tickers fitting less well, new entrants worth considering, stale justifications, macro / regulatory factors that have moved the thesis>

## Leading indicators

<refresh-driven; 2–4 upstream signals that move BEFORE the basket members and would crack the thesis first — never the member stock prices. Each: signal · latest reading + as-of date · direction · what it implies for the anchor or a name. Include a side-by-side line where ≥2 members guide the same forward metric. Source-chain each to its primary issuer.>

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

**Decompose the anchor into 2–5 sub-buckets**, each with its own dated path and source, plus a **geographic cut where natural** (e.g. ex-China vs China) — rendered as a compact inline list or 3-column table, not a second essay. **Name the swing factor**: the one sub-bucket whose revision moves the headline most (for a WFE basket that is DRAM; for a GLP-1 theme it may be oral formulations; for rare earths, magnet-grade oxide). Map each `core`/`enabler` ticker to the sub-bucket it rides, so the reader sees which names are levered to the swing factor — this reuses the role taxonomy rather than adding a parallel structure.

**Track the anchor over time.** When a refresh's forecaster republishes and the anchor moves, the `## What's New` block carries a **TAM-revision** bullet — old→new for each affected out-year, the delta attributed to a named driver (e.g. `2027E pool lifted to $175bn from $158bn — +$3.4bn from <driver sub-bucket>, [Forecaster, date](url)`); if the forecaster didn't republish, carry the number forward and say so. The optional `tam` field in the snapshot sidecar (above) makes this revision diff the same deterministic way the ticker set already does.

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

### Conviction ranking (within the basket — sourced, never the skill's own)

Beyond the categorical role tag, capture any **ordered preference** a named external analyst has published over the basket members, e.g. *"Bernstein prefers A > B > C: A = broadest exposure + cheapest; B = upgrade-cycle leverage; C = lags this year, sets up next."* Three rules:

1. **Always attributed, never self-authored.** Per the project rule, the skill's own model is NOT a source — so the rank must cite a named report/analyst via deep-URL or zsxq `file_id`. If you want to record the agent's own read, label it explicitly *"Analyst view (this note):"* and keep it visibly separate from the cited rank.
2. **Each rung carries a one-clause why** tied to that name's moat/threat Justification cell, so the order is legible, not bare. Where two credible sources disagree, show both (*"GS: A>B; MS: B>A — split on the swing-factor sub-bucket"*) rather than picking a winner.
3. **Price targets show their derivation.** If a tracked name carries a sell-side PT, capture it as `PT = <multiple>× applied to <EPS / metric base> ([analyst, date](url))` — a bare PT with no method is not acceptable, mirroring the "cite the inputs, not the model" rule.

Keep the ranking in `## Thesis` (a closing preference sentence) or as a one-line lead-in to the Tracked tickers table — **not a new table column** (preserve the 5-column parse contract). A new broker re-rank IS `## What's New` material; record the source in `## References`. (This generalizes: a humanoid basket ranks its sensor suppliers, a GLP-1 basket its CDMOs — the rank is the cited analyst's, not invented.)

### Tracked tickers table — the source of truth

The table at the top of the file is the canonical ticker list. Every mutation (add / drop / role change / justification re-grounding) edits a row in this table — not the prose elsewhere in the file. Workflows depend on parsing this table:

- `list` mode reads the top-of-file metadata of each `reports/themes/*_theme.md` (no per-ticker parse needed).
- `mutate` mode runs `Edit` on a single row (or appends a new one).
- `refresh` mode reads the ticker list, pulls data for each, then updates the data-driven sections below (Performance / Recent events / Drift signals).

The table columns are fixed: **Ticker | Name | Role | Justification | Added**. The Justification cell always contains at least one inline markdown link to a primary source naming the ticker as a theme participant. **Beyond proving participation, the cell must do two things:** (a) state the **moat** — the specific product niche / share / cost or IP edge that makes this name hard to displace (not "leader in X" but "sole supplier of Y, ~Z% share"), and (b) name the **threat** — the specific competitor, substitute, customer-insourcing, or policy shift that would erode that edge first (e.g. a mask-inspection name: "sole actinic supplier, ~50% share — threat = a rival's actinic launch in dev"). Where the threat is on the public record, inline-cite it too. A cell that says "largest player, well positioned" with no named threat is a stub — rewrite it; if you can't name a threat, you don't understand the position well enough to size conviction in it. **Keep moat + threat INSIDE the Justification cell — never as new columns** — to preserve the fixed 5-column parse contract that `list`/`mutate`/`refresh` rely on. If you can't articulate a one-sentence role with a citation, the ticker doesn't belong in the basket yet.

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
2. **zsxq-backed notes cite via the file_id convention** already used by What's-New and snapshot `evidence_file_ids`: `[<broker> <title>, zsxq #<file_id>](http://xs-macbook-air.local:5001/zsxq/pdf-viewer/<file_id>)`, and record the file_id in the refresh's snapshot line.

Project freshness still applies: discard broker notes older than ~12 months for selection (except founding facts). A revised TAM or re-ranking from a fresh note is itself `## What's New` material.

## Workflow

### Step 0 — Identify intent

Parse the user input to one of the modes (create / refresh / mutate / list). When ambiguous, ask one short clarifying question — never assume "refresh" when the user might mean "create new".

For **create**: extract the proposed theme name + scope. If the user gave only a name, propose 5–10 candidate tickers with one-sentence justifications and confirm before building.

For **refresh**: resolve the slug. Case-insensitive match against `reports/themes/*_theme.md`; if multiple matches (e.g. `humanoid-robotics-sensors_theme.md` and `humanoid-robotics-actuators_theme.md`), ask which.

For **mutate**: confirm the change scope (add/drop ticker, rename, delete) and the affected slug before editing.

For **list**: scan `reports/themes/*_theme.md`, parse the top-of-file metadata line from each, emit a summary table.

### Step 1 (Create only) — Initial ticker set

For a new theme:

1. Web-search for the theme keywords + "pure play" / "leader" / "supplier" / industry-research notes from the last 12 months.
2. Pull the latest 3 industry-research items naming participants in the space — and the multi-year TAM / spend forecast that anchors the Thesis (see *Thesis — lead with a quantified anchor*); a sell-side thematic note often supplies both the names and the anchor.
3. Cross-reference with [[sector-overview]] outputs if one exists for the broader sector.
4. Propose 5–10 candidate tickers, each with: ticker / name / role / one-sentence justification / one inline citation to a source naming them as a participant.
5. **Surface the proposed list to the user before writing the file.** Themes are most valuable when the user has agreed to the scope; pre-committing to a 10-ticker basket without confirmation creates drift the user didn't sign up for.
6. On confirmation, write `<slug>_theme.md` with the full structure described above. Run Step 4 (refresh data pass) immediately so the new file has live numbers.

### Step 2 (Refresh) — Pull updated data

For every ticker in the **Tracked tickers** table:

1. Pull latest price + return since `Last refreshed` from yfinance.
2. Pull current market cap + sector + valuation multiples.
3. Scan for material 8-K / 公告 / press-release events since `Last refreshed`.
4. Compute theme-aggregate performance (cap-weighted basket return; equal-weighted basket return; vs benchmark).
5. Pull `indicators.db` snapshot (VIX, 10Y, HY OAS) for the regime backdrop.
6. Pull the theme's 2–4 **leading indicators** — the upstream volume / price / capacity / guidance series that lead the members (and each member's own most-recent guidance on the shared forward metric) — with latest readings + as-of dates. These populate the `## Leading indicators` block and are the first place the thesis cracks.

### Step 3 (Refresh) — Surface drift signals

Drift detection is the value-add of refresh. Surface:

- **Theme exposure shift** — if a ticker's segment mix has moved away from the theme (e.g. a sensor company spinning off its sensor business). Flag and propose `role` change or removal in the **Tracked tickers** table.
- **New entrants** — tickers named in recent industry research that aren't in the basket. Propose for next mutation (don't auto-add).
- **Underperformer outliers** — tickers > 30% behind the basket median return over the refresh window. Surface the reason (idiosyncratic news, sector rotation, broken thesis).
- **Stale justifications** — if a ticker's Justification cell references a source older than 12 months, flag for re-grounding in the next mutation.
- **Valuation drift** — for each `core`/`adjacent` name, report the forward multiple (P/E, or the sector-appropriate one — EV/EBITDA, P/S for pre-profit) on **two relative axes**: vs the name's own ~10yr (or max-available) average, AND vs a stated sector/market benchmark — e.g. `<name> 37.5x fwd vs 10yr avg 17.7x; +36% vs <sector ETF>, +71% vs SPX`. When the **basket-median** multiple sits materially above its own history, raise an explicit **priced-for-perfection / air-pocket flag** and name the demand assumption — tied to the Thesis TAM anchor — whose disappointment would trigger a de-rate. A bare multiple with no own-history and benchmark context is a defect.

### Step 4 (Refresh / Create) — Update the file's data-driven sections

**First, compute the delta** so the refresh is trackable: read the last line of `<slug>_theme.snapshots.jsonl` (the prior state), set-diff its `tickers` against the current set, compare `perf`, and note `evidence_file_ids` not seen before. That delta drives the `## What's New` block. (On a create-pass there's no prior line — the delta is "basket created".)

Rewrite the following sections of `<slug>_theme.md` in place:

- **What's New** — **prepend** a dated block with the computed delta (tickers added/dropped/role-changed, biggest movers vs benchmark since last refresh, new broker calls/catalysts, **TAM revisions** (anchor old→new + named driver), thesis drift); roll the previous block into the `<details>` archive. Keep it to ~5–8 linked bullets.
- **Performance** — movers / laggards / benchmark comparison for the refresh window.
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

1. **Re-mine the source library wider than the original cluster.** For zsxq-backed themes that means a *strict-keyword* search of the recent ~600–800 DB rows on (a) tracked-ticker names/codes AND (b) theme-specific terms (HBM / NOR / SST / cobot / GLP-1 …) — not the loose generic terms (AI / data center / 算力) that cluster-time keyword matches use. Loose keywords are the right tool for *clustering*; strict keywords are the right tool for *refresh-mining* an already-named theme, because they pick up reports that cover known tickers under terminology the original cluster missed.
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

Charts (optional): `reports/charts/theme_<slug>_*.png` per the existing project convention.

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
7. **## Exclusions** table (optional but recommended — explicit "we considered this and rejected it").
8. **## Keywords** — bilingual where natural.
9. **## Performance** (refresh-driven).
10. **## Recent events** (refresh-driven).
11. **## Drift signals** (refresh-driven — the value-add).
12. **## Leading indicators** (refresh-driven — the early-warning layer; 2–4 upstream signals that lead the members, incl. side-by-side member guidance on the shared forward metric).
13. **## Catalysts** (next 3–6 months, refresh-driven — event + mechanism + timing + which sub-bucket).
14. **## Data Used / 数据来源清单** (manifest — see block below).
15. **## References** (every URL cited inline).
16. **## History** (mutation log; append-only).

Plus the **`<slug>_theme.snapshots.jsonl`** sidecar (one JSON line per create/refresh/mutate) — not part of the md, but mandatory and committed alongside it.

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

## Guardrails

- **Themes drift.** A 6-month-old basket may no longer reflect the original thesis. Always run the refresh workflow before quoting performance — never cite stale tickers as "the current theme".
- **Pure-plays beat conglomerates for theme tracking.** Tesla in a humanoid theme is mostly noise; an SOC supplier with 80% humanoid exposure is signal. The `role: core` tag should be rare; `adjacent` and `enabler` are the more common labels.
- **Every ticker has a written justification.** No "obvious" additions. If you can't articulate the role in one sentence with a citation, the ticker doesn't belong yet.
- **The Thesis leads with a quantified, sourced anchor.** A theme whose thesis states no dated, third-party-sourced TAM / spend / volume trajectory is not ready to ship — the anchor is what makes the bet falsifiable and the drift-check meaningful. The analyst's own model is never the anchor's source.
- **Every Justification cell names a moat AND a threat.** "Largest player, well positioned" with no named competitor / substitute / policy threat is a stub — if you can't name what breaks the position first, you can't size conviction in it.
- **Performance comparisons need a stated benchmark.** "The basket is up 22%" is meaningless without "vs S&P 500 +14% / CSI 300 +8% over the same window".
- **Multiples are relative, never bare.** Every quoted valuation multiple carries both its own-history comparison and a benchmark comparison. A basket trading rich vs its own history must carry a priced-for-perfection / air-pocket flag tied to the Thesis TAM anchor — the same way performance carries a benchmark.
- **Drift signals are the deliverable.** A refresh that doesn't surface any drift signals after 90 days of market action is a defect — go back and look harder.
- **Catalysts carry a mechanism, not just a date.** A dated event with no transmission story to the TAM anchor or a named tracked ticker is a calendar entry, not a catalyst — it doesn't belong in the Catalysts section.
- **Conviction rankings are sourced, never self-authored.** Any ordered preference over basket members cites a named external analyst; the agent's own read is labelled "Analyst view" and kept visibly separate. (The project rule: the skill's own model is not a source.)
- **Do not silently mutate the Tracked tickers table.** Every mutation carries a corresponding `## History` line with the date + reason.
- **Do not use a theme to chase performance retroactively.** Don't add a ticker to the basket "because it's been ripping for 3 months" — only add if it fits the original thesis. Performance-driven additions destroy the analytical value.
- **Do not regenerate the file's data-driven sections on every mutation.** Mutations are cheap; refreshes are expensive. Only refresh the data when the user explicitly asks or the data is materially stale.
- **Do not rewrite the Thesis or Scope rules during a refresh.** Those are stable across refreshes; changing them is a deliberate thesis re-grounding that requires user confirmation.
- **Do not invent industry-research citations.** Every named research firm + report needs a real, verifiable URL.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

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

Charts live in the existing `reports/charts/theme_<slug>_*.png` location, **not** alongside the theme file.

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
