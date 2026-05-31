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
- **New broker call:** GS initiated Anpeilong Buy, PT ¥120 ([GS, zsxq #...](http://localhost:5001/zsxq-pdf/...)).
- **Thesis drift:** none — basket still reflects the original BOM-expansion bet.

<details><summary>Earlier refreshes</summary>

**2026-05-31 — basket created** (2 tickers: Anpeilong core, Leapmotor adjacent).

</details>

## Thesis

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

## Catalysts (next 3–6 months)

<dated events to watch — earnings dates, product launches, regulatory milestones>

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

1. **`## What's New` section** (top of the md, under the metadata line) — the human-facing delta. Each refresh **prepends** a dated block (tickers added / dropped / role-changed, biggest movers vs benchmark since last refresh, *new* broker calls & catalysts, thesis drift). The previous block rolls into a `<details>` archive so the section stays short. Keep ~5–8 bullets per refresh; link each claim.

2. **`<slug>_theme.snapshots.jsonl`** — the machine record. Append exactly one line per refresh:

   ```json
   {"date":"2026-06-30","tickers":[{"t":"SZSE:301413","role":"core"},{"t":"NASDAQ:HSAI","role":"core"}],"perf":{"basket_1y":80.2,"bench":"CSI300","bench_1y":33.3,"since_last_refresh":8.2},"evidence_file_ids":[184152244582842,212485814114811],"n_events":6,"note":"added Donghua; dropped Leapmotor"}
   ```

   Field contract: `date` (ISO), `tickers` (the full current set with roles — so a diff vs the prior line yields added/dropped/role-changed for free), `perf` (basket vs a named benchmark + return since last refresh), `evidence_file_ids` (zsxq/source IDs this refresh leaned on), `n_events`, `note` (one line). The create-pass writes the first (baseline) line.

**How "what's new" is computed:** on refresh, read the last JSONL line, set-diff its `tickers` against the current set, compare `perf`, and list `evidence_file_ids` not seen before → that *is* the `## What's New` block. Deterministic, no eyeballing two long reports.

**Point-in-time recall** is git, not file sprawl: `git show <sha>:reports/themes/<slug>_theme.md` reconstructs any past state, and `git log --oneline -- reports/themes/<slug>_theme.snapshots.jsonl` lists every refresh commit. This is why one canonical file + the sidecar beats dated `_2026-06-30.md` copies (which duplicate the ticker table, drift apart, and clutter the viewer).

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

### Tracked tickers table — the source of truth

The table at the top of the file is the canonical ticker list. Every mutation (add / drop / role change / justification re-grounding) edits a row in this table — not the prose elsewhere in the file. Workflows depend on parsing this table:

- `list` mode reads the top-of-file metadata of each `reports/themes/*_theme.md` (no per-ticker parse needed).
- `mutate` mode runs `Edit` on a single row (or appends a new one).
- `refresh` mode reads the ticker list, pulls data for each, then updates the data-driven sections below (Performance / Recent events / Drift signals).

The table columns are fixed: **Ticker | Name | Role | Justification | Added**. The Justification cell always contains at least one inline markdown link to a primary source naming the ticker as a theme participant. If you can't articulate a one-sentence role with a citation, the ticker doesn't belong in the basket yet.

## Language (English default; Chinese opt-in)

**Default behavior: write the English file only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need a Chinese companion for every refresh.

- English (default): `reports/themes/<slug>_theme.md`
- Chinese (opt-in only): `reports/themes/<slug>_主题研究.md`

**Chinese opt-in (any of these triggers the Chinese companion alongside the English file):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

Once a Chinese companion exists for a theme, subsequent refreshes update both files unless the user says otherwise. The top-of-file **Languages tracked** metadata field records the current state (`en`, `en, zh`, or `zh`). The Tracked tickers table is **identical** across both files (same rows, same justifications — the citation URLs don't translate); only the prose sections (Thesis, Scope rules, Performance summary, Drift signals, Catalysts) are written natively in each language.

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

### News and sentiment

- **WebSearch** for recent press, industry-research notes (last 90 days for refresh window).
- **[[news-analyst]]** as a sub-step for high-value tickers when the user explicitly asks for sentiment scoring.

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
2. Pull the latest 3 industry-research items naming participants in the space.
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

### Step 3 (Refresh) — Surface drift signals

Drift detection is the value-add of refresh. Surface:

- **Theme exposure shift** — if a ticker's segment mix has moved away from the theme (e.g. a sensor company spinning off its sensor business). Flag and propose `role` change or removal in the **Tracked tickers** table.
- **New entrants** — tickers named in recent industry research that aren't in the basket. Propose for next mutation (don't auto-add).
- **Underperformer outliers** — tickers > 30% behind the basket median return over the refresh window. Surface the reason (idiosyncratic news, sector rotation, broken thesis).
- **Stale justifications** — if a ticker's Justification cell references a source older than 12 months, flag for re-grounding in the next mutation.

### Step 4 (Refresh / Create) — Update the file's data-driven sections

**First, compute the delta** so the refresh is trackable: read the last line of `<slug>_theme.snapshots.jsonl` (the prior state), set-diff its `tickers` against the current set, compare `perf`, and note `evidence_file_ids` not seen before. That delta drives the `## What's New` block. (On a create-pass there's no prior line — the delta is "basket created".)

Rewrite the following sections of `<slug>_theme.md` in place:

- **What's New** — **prepend** a dated block with the computed delta (tickers added/dropped/role-changed, biggest movers vs benchmark since last refresh, new broker calls/catalysts, thesis drift); roll the previous block into the `<details>` archive. Keep it to ~5–8 linked bullets.
- **Performance** — movers / laggards / benchmark comparison for the refresh window.
- **Recent events** — bulleted list of material press releases / filings since the previous refresh, each inline-cited.
- **Drift signals** — output of Step 3.
- **Catalysts** — refreshed list of dated events in the next 3–6 months.
- **Data Used / 数据来源清单** — refreshed manifest with new as-of dates.
- **References** — append any new URLs cited above.

**Then append one line to `<slug>_theme.snapshots.jsonl`** capturing the new state (date, full ticker set + roles, perf vs benchmark + since-last-refresh, evidence_file_ids, n_events, one-line note) — this is what the *next* refresh diffs against. Update the `**Last refreshed:** YYYY-MM-DD` field in the top-of-file metadata.

Do **not** rewrite the Thesis, Scope rules, Tracked tickers, Exclusions, or Keywords sections during a refresh — those are stable across refreshes and only change via a mutation (Step 5) or a deliberate thesis re-grounding (which the user must explicitly request).

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
4. **## Thesis** (200–400 words).
5. **## Scope rules** (100–200 words).
6. **## Tracked tickers** table (mandatory columns: Ticker | Name | Role | Justification | Added).
7. **## Exclusions** table (optional but recommended — explicit "we considered this and rejected it").
8. **## Keywords** — bilingual where natural.
9. **## Performance** (refresh-driven).
10. **## Recent events** (refresh-driven).
11. **## Drift signals** (refresh-driven — the value-add).
12. **## Catalysts** (next 3–6 months, refresh-driven).
13. **## Data Used / 数据来源清单** (manifest — see block below).
14. **## References** (every URL cited inline).
15. **## History** (mutation log; append-only).

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

**Industry research (theme-level)**
- <research-firm + report title + publication date + URL> — used for ticker selection and drift detection.

**Macro backdrop**
- VIX, 10Y Treasury, HY OAS as of YYYY-MM-DD. Source: `indicators.db`.

**Cross-coverage**
- [reports/company/<Slug>/...md](../company/<Slug>/...md) (last updated YYYY-MM-DD) — read as structured input for the <ticker> paragraph, not cited inline.

**Stale notices / coverage gaps**
- <bulleted list — ticker without recent IR refresh, missing third-party source for a candidate, or "none">.
```

## Guardrails

- **Themes drift.** A 6-month-old basket may no longer reflect the original thesis. Always run the refresh workflow before quoting performance — never cite stale tickers as "the current theme".
- **Pure-plays beat conglomerates for theme tracking.** Tesla in a humanoid theme is mostly noise; an SOC supplier with 80% humanoid exposure is signal. The `role: core` tag should be rare; `adjacent` and `enabler` are the more common labels.
- **Every ticker has a written justification.** No "obvious" additions. If you can't articulate the role in one sentence with a citation, the ticker doesn't belong yet.
- **Performance comparisons need a stated benchmark.** "The basket is up 22%" is meaningless without "vs S&P 500 +14% / CSI 300 +8% over the same window".
- **Drift signals are the deliverable.** A refresh that doesn't surface any drift signals after 90 days of market action is a defect — go back and look harder.
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
