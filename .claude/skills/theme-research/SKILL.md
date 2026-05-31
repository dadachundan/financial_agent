---
name: theme-research
description: Build and maintain thematic equity baskets (e.g. humanoid-robotics-sensors, GLP-1 supply chain, advanced packaging, EV battery) — each theme is a named set of tickers + keywords stored under `reports/themes/<slug>/registry.yaml`, with a companion English research note `<slug>_theme_research.md` (Chinese companion `<slug>_主题研究.md` available on explicit request). The skill creates new themes, refreshes existing ones with movers/laggards + recent news + valuation drift, and surfaces drift signals (tickers no longer fitting; new tickers worth adding). Distinct from `sector-overview` (one-shot landscape essay) — themes are *tracked baskets* that get refreshed. Use when the user says "build a theme on X", "track the X basket", "refresh my <theme> basket", "what's moving in my <theme>?", or "what themes do I have?"
---

# Theme Research

A theme = **named basket of tracked tickers + keywords**, with a small registry file and a bilingual companion research note. Themes are *living* artifacts — they get refreshed periodically as movers shift and the keyword set evolves. Distinct from [[sector-overview]] (one-shot essay on a sector landscape) and from a watchlist (no analytical depth, just price tracking).

Adapted from the [LLMQuant theme research workflow](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-portfolio/workflows/theme-research.md) (MIT), re-pointed at a file-system registry under `reports/themes/<slug>/` instead of LLMQuant's hosted theme storage.

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

Three modes:

| Mode | Trigger phrasings | What happens |
|---|---|---|
| **Create** | "build a theme on X", "start tracking X", "new theme: X" | Builds initial registry + research note from scratch |
| **Refresh** | "refresh my X theme", "what's moving in X", "update X basket" | Reads existing registry, re-pulls market data + news + valuation, surfaces drift, updates research note in place |
| **Mutate** | "add/drop <ticker> to <theme>", "rename theme X to Y", "delete theme X" | Edits the registry only; does not re-write the research note unless the user explicitly asks |
| **List** | "list my themes", "what themes do I have" | Enumerates `reports/themes/*/registry.yaml` and summarizes each |

## When NOT to use

- The user asks for a one-shot industry essay with no intent to track — use [[sector-overview]].
- The user wants a comparison of a closed N companies — use [[compare-companies]].
- The user wants a deep dive on a single company — use [[company-research]].
- The "theme" maps cleanly to an existing ETF the user can hold (e.g. "AI infrastructure" → XLY+XLK or just SOXX) and they're not trying to build alpha vs the ETF — recommend the ETF instead and skip the basket overhead.

## Core principle: themes are *tracked*, not just *researched*

A theme is not just a sector essay — it's a basket of named tickers with explicit justifications and a refresh cadence. The skill's value is in **drift detection**: are the tickers I picked 6 months ago still the right tickers? Has a new entrant emerged? Has a former member become structurally impaired or moved out of the theme?

This is the discipline that distinguishes a useful theme tracker from a stale watchlist. The `registry.yaml` records *why* each ticker was added — and the refresh workflow surfaces whether that justification still holds.

## Registry file format

Every theme lives under `reports/themes/<slug>/registry.yaml`. The slug uses kebab-case with the English / pinyin name first, optionally followed by `_中文名` (per the project's filename rule):

```yaml
# reports/themes/humanoid-robotics-sensors/registry.yaml
theme: humanoid-robotics-sensors
name_en: Humanoid Robotics Sensors
name_zh: 人形机器人传感器
description_en: |
  Sensor suppliers for humanoid robots — force / torque sensors, IMUs,
  tactile sensors, vision-system components, and supporting MCUs.
description_zh: |
  人形机器人传感器供应商——力 / 力矩传感器、IMU、触觉传感器、
  视觉系统元件,以及相关 MCU。
created: 2026-05-31
last_updated: 2026-05-31
last_refreshed: 2026-05-31
keywords:
  - humanoid robotics / 人形机器人
  - force-torque sensor / 力矩传感器
  - tactile sensor / 触觉传感器
  - IMU / 惯性测量单元
  - robotics MCU / 机器人主控
tickers:
  - ticker: SZSE:002050
    name_en: Anpeilong
    name_zh: 安培龙
    role: core
    justification_en: |
      Largest A-share standalone force-torque sensor supplier;
      design-wins at Tesla Optimus tier-1 + multiple Chinese humanoid
      programs (per cninfo 投资者交流活动记录, 2026-04).
    justification_zh: |
      A 股最大独立力矩传感器供应商;特斯拉 Optimus 一级供应链与多家
      中国人形机器人项目设计中标(cninfo 投资者交流活动记录,2026-04)。
    added: 2026-05-31
  - ticker: HKEX:9863
    name_en: Leapmotor
    name_zh: 零跑汽车
    role: adjacent
    justification_en: |
      EV OEM with announced humanoid program; included as adjacency
      (its humanoid-derived sensor demand is still <5% of its base
      auto business, but the roadmap is on the public record).
    justification_zh: |
      已宣布人形机器人项目的电动车整车厂;作为邻接标的纳入
      (人形机器人衍生传感器需求目前仍占其汽车主业 5% 以下,
      但路线图已公开披露)。
    added: 2026-05-31
exclusions:  # optional — explicit "we considered this and rejected it"
  - ticker: NASDAQ:TSLA
    reason_en: |
      Humanoid Optimus is < 1% of Tesla revenue and intermingles with
      auto / energy — too diluted to track as a humanoid-pure-play.
    reason_zh: |
      人形机器人 Optimus 占特斯拉收入不足 1%,且与汽车 / 能源业务混合
      ——稀释程度过高,不作为人形机器人纯标的跟踪。
metadata:
  refresh_cadence: monthly  # informal — agent uses it to flag stale themes
  source_of_truth: cninfo + HKEX + 雪球 + management 路演记录
```

### Slug rules

- Kebab-case (`humanoid-robotics-sensors`, not `humanoidRoboticsSensors` or `humanoid_robotics_sensors`).
- English / pinyin first. Optional `_中文名` suffix if it aids discoverability (`humanoid-robotics-sensors_人形机器人传感器`).
- Lowercase only.
- No date in slug (the registry has `created` + `last_updated` fields).
- Avoid generic words like `tech`, `growth`, `ai` alone — themes work best when scoped narrowly (`ai-infrastructure-power-cooling` beats `ai`).

### Ticker role taxonomy

- **`core`** — pure-play exposure; the theme's defining names.
- **`adjacent`** — partial exposure or expanding into the theme; not pure-play but worth tracking.
- **`enabler`** — supplier / component / IP licensor that benefits when the theme builds out.
- **`hedge`** — counter-position that benefits when the theme breaks (rare; mostly relevant for thematic short books).

If a ticker doesn't cleanly fit, write a one-sentence justification and pick the closest role. Don't invent new roles per theme — discipline matters.

## Research note (English default; Chinese opt-in)

**Default behavior: write the English note only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need a Chinese companion for every refresh.

- English (default): `reports/themes/<slug>/<slug>_theme_research.md`
- Chinese (opt-in only): `reports/themes/<slug>/<slug>_主题研究.md`

**Chinese opt-in (any of these triggers the Chinese companion alongside the English note):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

Once a Chinese companion exists for a theme, subsequent refreshes update both files unless the user says otherwise. The registry.yaml `metadata.languages: [en, zh]` field records which languages this theme is currently tracked in.

Target word count: **2,000–4,000 words per language** (less than [[sector-overview]]'s landscape essay — themes are focused, not exhaustive).

Standard structure:

1. **Thesis (200–400 words)** — what's the bet behind this theme? Why does it cluster? What's the macro / technology / regulatory tailwind?
2. **Scope rules (100–200 words)** — what counts as a member and what doesn't. The "exclusions" reasoning belongs here.
3. **Tracked tickers** — for each ticker in the registry, one paragraph: company, role in the theme, exposure %, latest data point. Quote the company's own positioning language when possible.
4. **Performance (last refresh window)** — movers and laggards since last_refreshed; YTD and 1Y returns; relative to a stated benchmark (S&P 500 / CSI 300 / sector ETF).
5. **Recent events** — new product launches, customer wins, capacity announcements, M&A in the theme since last refresh. Cite each inline.
6. **Drift signals** — tickers fitting less well now (segment mix shift, declining theme exposure); new candidates worth adding next refresh; macro / regulatory factors that have moved the thesis.
7. **Catalysts in the next 3–6 months** — dated events to watch (earnings calls, product launches, regulatory milestones).
8. **Data Used** manifest (mandatory; see block below).
9. **References** — every URL cited inline.

**Bilingual writing rule (per [[company-research]]):** Chinese reports use both languages for technical terms on first mention (`力矩传感器 / force-torque sensor`, `主控 MCU / robotics-MCU`). Tickers, regulator names, and acronyms stay in original form.

## Data sources

### Primary (always-available)

- **yfinance** for price history, current price, sector classification, market cap. Use `auto_adjust=True` for performance comparisons.
- **`indicators.db`** for macro backdrop at refresh time (VIX, 10Y Treasury, HY OAS) — pulled once per refresh and referenced across the note.
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

For **refresh**: resolve the slug. Case-insensitive match on the directory name; if multiple matches (e.g. `humanoid-robotics-sensors` and `humanoid-robotics-actuators`), ask which.

For **mutate**: confirm the change scope (add/drop ticker, rename, delete) and the affected slug before editing.

For **list**: scan `reports/themes/*/registry.yaml`, parse the YAML headers, emit a table.

### Step 1 (Create only) — Initial ticker set

For a new theme:

1. Web-search for the theme keywords + "pure play" / "leader" / "supplier" / industry-research notes from the last 12 months.
2. Pull the latest 3 industry-research items naming participants in the space.
3. Cross-reference with [[sector-overview]] outputs if one exists for the broader sector.
4. Propose 5–10 candidate tickers, each with: ticker / name / role / one-sentence justification / one inline citation to a source naming them as a participant.
5. **Surface the proposed list to the user before writing the registry.** Themes are most valuable when the user has agreed to the scope; pre-committing to a 10-ticker basket without confirmation creates drift the user didn't sign up for.
6. On confirmation, write the registry.yaml + the bilingual research note. Run Step 4 (refresh data pass) immediately so the new note has live numbers.

### Step 2 (Refresh) — Pull updated data

For every ticker in the registry:

1. Pull latest price + return since `last_refreshed` from yfinance.
2. Pull current market cap + sector + valuation multiples.
3. Scan for material 8-K / 公告 / press-release events since `last_refreshed`.
4. Compute theme-aggregate performance (cap-weighted basket return; equal-weighted basket return; vs benchmark).
5. Pull `indicators.db` snapshot (VIX, 10Y, HY OAS) for the regime backdrop.

### Step 3 (Refresh) — Surface drift signals

Drift detection is the value-add of refresh. Surface:

- **Theme exposure shift** — if a ticker's segment mix has moved away from the theme (e.g. a sensor company spinning off its sensor business). Flag and propose `role` change or removal.
- **New entrants** — tickers named in recent industry research that aren't in the registry. Propose for next refresh (don't auto-add).
- **Underperformer outliers** — tickers > 30% behind the basket median return over the refresh window. Surface the reason (idiosyncratic news, sector rotation, broken thesis).
- **Stale justifications** — if a ticker's `justification_en` references a source older than 12 months, flag for re-grounding.

### Step 4 (Refresh / Create) — Update the research note

Rewrite the bilingual research note with:
- Updated tracked-ticker paragraphs (last-refresh data point).
- Updated performance section.
- New "Recent events" since `last_refreshed`.
- New drift signals.
- Updated catalyst list.
- Refreshed Data Used manifest with new as-of dates.

Update `last_refreshed: YYYY-MM-DD` in the registry.

### Step 5 (Mutate) — Registry-only edits

For add/drop/rename:
1. Edit `registry.yaml` directly.
2. Add a one-line entry to a `metadata.history` field if it doesn't already exist:
   ```yaml
   metadata:
     history:
       - YYYY-MM-DD added <ticker> as <role> — <reason>
       - YYYY-MM-DD dropped <ticker> — <reason>
       - YYYY-MM-DD renamed slug from <old> to <new>
   ```
3. **Do NOT regenerate the research note** unless the user explicitly says "also refresh the note". Registry edits are cheap; note edits are not.
4. Bump `last_updated` (different from `last_refreshed` — `updated` tracks registry changes; `refreshed` tracks data pulls).

### Step 6 — Write or update files

Both English and Chinese notes by default. Single-language override via `--en-only` / `--zh-only` / `English only` / `用中文即可`.

Save:
- `reports/themes/<slug>/registry.yaml`
- `reports/themes/<slug>/<slug>_theme_research.md` (English)
- `reports/themes/<slug>/<slug>_主题研究.md` (Chinese)

Charts (optional): `reports/charts/theme_<slug>_*.png`.

### Step 7 — Verify

- Re-read the registry YAML to confirm valid syntax.
- Spot-check ≥3 ticker performance numbers in the note vs yfinance.
- Confirm all inline URLs in the note return HTTP 200 (sample 5).
- Stop any test servers used during chart rendering.

## Output Format (mandatory blocks per research note)

1. **Thesis statement** at the top (one paragraph).
2. **Scope rules** — what's in / out / why.
3. **Tracked tickers** table + one paragraph each.
4. **Performance section** with benchmark comparison.
5. **Drift signals** section — explicit, not buried.
6. **`## Data Used / 数据来源清单`** manifest.
7. **`## Guardrails for this theme`** — what would invalidate the basket.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Registry**
- reports/themes/<slug>/registry.yaml (last_updated YYYY-MM-DD, last_refreshed YYYY-MM-DD)

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
- [reports/company/<Slug>/...md](../../company/<Slug>/...md) (last updated YYYY-MM-DD) — read as structured input for the <ticker> paragraph, not cited inline.

**Stale notices / coverage gaps**
- <bulleted list — ticker without recent IR refresh, missing third-party source for a candidate, or "none">.
```

## Guardrails

- **Themes drift.** A 6-month-old basket may no longer reflect the original thesis. Always run the refresh workflow before quoting performance — never cite stale tickers as "the current theme".
- **Pure-plays beat conglomerates for theme tracking.** Tesla in a humanoid theme is mostly noise; an SOC supplier with 80% humanoid exposure is signal. The `role: core` tag should be rare; `adjacent` and `enabler` are the more common labels.
- **Every ticker has a written justification.** No "obvious" additions. If you can't articulate the role in one sentence with a citation, the ticker doesn't belong yet.
- **Performance comparisons need a stated benchmark.** "The basket is up 22%" is meaningless without "vs S&P 500 +14% / CSI 300 +8% over the same window".
- **Drift signals are the deliverable.** A refresh note that doesn't surface any drift signals after 90 days of market action is a defect — go back and look harder.
- **Do not silently mutate the registry.** Every registry change carries a metadata.history line with the date + reason.
- **Do not use a theme to chase performance retroactively.** Don't add a ticker to the basket "because it's been ripping for 3 months" — only add if it fits the original thesis. Performance-driven additions destroy the analytical value.
- **Do not regenerate the research note on every registry edit.** Notes are expensive; registry edits are cheap. Only refresh the note when the user explicitly asks or the data is materially stale.
- **Do not invent industry-research citations.** Every named research firm + report needs a real, verifiable URL.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Output location

Save to `reports/themes/<slug>/` under the project root. Create the `reports/themes/` directory if missing (first theme establishes it).

Standard directory layout per theme:

```
reports/themes/<slug>/
├── registry.yaml                          # the source of truth — tickers + roles + justifications
├── <slug>_theme_research.md               # English research note
├── <slug>_主题研究.md                       # Chinese research note
└── (optional) charts/                     # if charts are theme-specific, otherwise put in reports/charts/
```

Charts can also sit in `reports/charts/theme_<slug>_*.png` per the existing project convention; using a per-theme `charts/` subdir is allowed when the chart count is high (>6).

### Update-in-place rule

One registry, one English note, one Chinese note per slug. Refresh updates them in place — never create dated parallel copies. Git history is the audit trail; the `metadata.history` field in the registry is the narrative log of intentional changes.

If the same theme conceptually exists under multiple slugs (e.g. `humanoid-robotics` and `humanoid-robotics-sensors`), the **narrower** slug wins. Promote the broader slug's content into the narrower one and delete the broader directory (ask the user first).

## What this skill does NOT do

- It does not produce a one-shot industry essay — that's [[sector-overview]].
- It does not produce a head-to-head comparison of theme members — that's [[compare-companies]] (run on a 2–4 subset of the basket).
- It does not produce a deep dive on any single member — that's [[company-research]] (run on the ticker; the theme note links to it).
- It does not auto-add or auto-drop tickers based on performance. All registry changes are user-confirmed.
- It does not produce a sized portfolio recommendation. A theme is *what to watch*, not *how much to hold* — sizing is [[trader-plan]] / [[portfolio-decision]] territory.
- It does not predict the theme's outperformance vs benchmark. Performance is *reported*, not forecast.
- It does not maintain alerts or notifications. The "refresh cadence" in the registry is informational only; the user runs the refresh manually (or via [[loop]] for periodic automation).
