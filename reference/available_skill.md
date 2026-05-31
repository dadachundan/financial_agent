# Available Skills — Graph View

Snapshot of every skill registered for this project, grouped by role and dependency chain.

> **Keep this file in sync.** Whenever a skill is added, removed, or its `## Prerequisites` block changes under `.claude/skills/`, update this file in the same commit and bump the "Last updated" date below. See the [Maintenance](#maintenance) section at the bottom for the checklist.

Last updated: 2026-05-31 (round 4 — **`zsxq-ideas` gains a third mode: theme-build.** Clusters the feed (reuse fishing F1–F3), then seeds/refreshes durable `theme-research` baskets at `reports/themes/<slug>_theme.md` from the *actual broker content* — not generic web knowledge. New `scripts/evidence_bundle.py` dumps a cluster's 翻译精华 summaries into one source pack; flagships go deeper via `zsxq-analyze/extract_pdf.py`. New **zsxq citation convention** (applies to all 3 modes): cite each broker number to its `file_id` via `http://localhost:5001/zsxq-pdf/<file_id>`, never the report title alone — with a hard no-fabrication rule. Adds `[[theme-research]]` to the skill's Prerequisites. Triggers added: "build themes from zsxq", "turn my zsxq feed into baskets".)

Earlier 2026-05-31 (round 3.5): NEW skill **`zsxq-ideas`** — idea-generation funnel sourced from the zsxq report library. Two modes: themed (user names a theme → 8-12 parallel `/zsxq-analyze` fan-out → 5-10 ticker shortlist with idea-generation Step-4 presentation, saved to `reports/ideas/zsxq_<slug>_<date>.md`) and fishing (no theme → cluster the recent 200-row feed into 3-6 themes, then lite fan-out on top 2 themes for a triage shortlist). Promotes the zsxq area from "Pair" to "Trio" — `zsxq-recommend` + `zsxq-analyze` + `zsxq-ideas`. English filenames mandatory per the CLAUDE.md rule. Output is idea sourcing, not a buy rating — next step always points to `/company-research <ticker>`.

Earlier 2026-05-31: Language-default flip on the 4 monitoring/tracking skills — `etf-overlap`, `ma-event-tracker`, `theme-research`, `regulatory-risk-monitor` now default to **English only**; Chinese is opt-in via `also in Chinese` / `bilingual` / `--zh` / `用中文也输出一份`. The substantive research skills `company-research` / `compare-companies` / `earnings-analysis` / `sector-overview` keep their bilingual default. Same line applied to the earlier-added `take-profit-lab`. Recorded in [feedback_tracking_skills_english_default.md](../../.claude/projects/-Users-x-projects-financial-agent/memory/feedback_tracking_skills_english_default.md).

Earlier 2026-05-31 round 3 — investor-lens pack expansion: `references/investor_lenses.md` now covers **9 lenses** (4 core + 5 optional). Core (default): 10.1 Buffett, 10.2 Munger, 10.3 Damodaran, 10.4 Howard Marks cycle. New optional packs: **10.5 Lynch GARP** (mid-cap growers / ten-bagger discipline / Lynch six-categories), **10.6 Fisher scuttlebutt** (15-point qualitative growth + mandatory non-filing evidence note), **10.7 Burry forensic deep value** (hated-sector + downside-first; sum-to-12 scoring), **10.8 Druckenmiller liquidity-regime** (macro context + 3:1 R/R + same-day-exit trigger), **10.9 Cathie Wood Wright's Law** (cost-curve + 5yr TAM re-pricing + convergence). Routing rules in `investor_lenses.md` § "Implementation tips" tell the analyst which optional lenses fit which company type. Quality checklist + report_structure.md updated with per-lens required-block specs.

Earlier 2026-05-31 round 2: four NEW skills added — (B) **`etf-overlap`** — head-to-head ETF holdings overlap for 2–4 ETFs; SEC N-PORT primary, issuer-CSV daily fallback, yfinance last-resort. (C) **`ma-event-tracker`** — single-deal merger tracking with spread / milestones / break-risk / probability range. (D) **`theme-research`** — tracked thematic baskets backed by `reports/themes/<slug>/registry.yaml`. (E) **`regulatory-risk-monitor`** — single-case regulatory tracking (FDA / DOJ / FTC / EU / SAMR / CSRC / etc.). All four bilingual default.

Earlier 2026-05-31 round 1: (1) **`company-research`** gains an optional Section 10 — Investor-lens scorecards (Buffett / Munger / Damodaran / Howard Marks cycle) in `references/investor_lenses.md`, plumbed to `indicators.db`. (2) **NEW skill `take-profit-lab`** — exit-discipline backtest. (3) All four research skills gain `## Guardrails` + `## Data Used` manifests.

Earlier: 2026-05-31 (`compare-companies` N-way support 2-4 companies; prior-research existence check hardened)

---

## 1. Trading-analysis pipeline (the spine — explicit dependencies)

This is the only chain with **machine-enforced** upstream skills (declared via `[[wikilink]]` references in each SKILL.md's `## Prerequisites` block). Each downstream skill auto-cascades upstream if its prerequisite is missing.

```
                  ┌──────────────────┐
                  │ trading-analysis │  ← orchestrator (runs whole chain)
                  └────────┬─────────┘
                           │ fans out 3 analysts in parallel
        ┌──────────────────┼──────────────────────────────┐
        ▼                  ▼                              ▼
┌──────────────────┐ ┌─────────────┐         ┌────────────────────┐
│ sentiment-analyst│ │ news-analyst│         │  company-research  │
└────────┬─────────┘ └──────┬──────┘         └──────────┬─────────┘
         │                  │                           ▲
         │                  │            (US issuers,   │
         │                  │             Step 0.5)     │
         │                  │                ┌──────────┴─────────┐
         │                  │                │ sec-report-summary │
         │                  │                └────────────────────┘
         │                  │                           │
         └──────────────────┴───────────────────────────┘
                            ▼
                  ┌───────────────────┐
                  │ bull-bear-debate  │  needs all 3 analyst reports
                  └─────────┬─────────┘
                            ▼
                  ┌───────────────────┐
                  │ research-manager  │  consumes debate transcript
                  └─────────┬─────────┘
                            ▼
                  ┌───────────────────┐
                  │   trader-plan     │  Buy/Hold/Sell proposal
                  └─────────┬─────────┘
                            ▼
                  ┌───────────────────┐
                  │   risk-debate     │  3-way Aggressive/Conservative/Neutral
                  └─────────┬─────────┘
                            ▼
                  ┌───────────────────┐
                  │ portfolio-decision│  final 5-tier rating (terminal)
                  └───────────────────┘
```

| Skill | Prereqs | Output |
|---|---|---|
| [trading-analysis](../.claude/skills/trading-analysis/SKILL.md) | — (orchestrator) | Runs the whole pipeline end-to-end |
| [sentiment-analyst](../.claude/skills/sentiment-analyst/SKILL.md) | — | 7-day sentiment report (Yahoo / StockTwits / Reddit) |
| [news-analyst](../.claude/skills/news-analyst/SKILL.md) | — | Macro + ticker news, past 30 days |
| [sec-report-summary](../.claude/skills/sec-report-summary/SKILL.md) | — (US-only sub-skill) | Multi-year SEC filing narrative |
| [company-research](../.claude/skills/company-research/SKILL.md) | `sec-report-summary` (US issuers only, Step 0.5) | 6–10k word deep dive **× 2** (English + Chinese by default) |
| [bull-bear-debate](../.claude/skills/bull-bear-debate/SKILL.md) | 3 analyst reports | Multi-round debate transcript |
| [research-manager](../.claude/skills/research-manager/SKILL.md) | `bull-bear-debate` | ResearchPlan + 5-tier rating |
| [trader-plan](../.claude/skills/trader-plan/SKILL.md) | `research-manager` | Buy/Hold/Sell proposal |
| [risk-debate](../.claude/skills/risk-debate/SKILL.md) | `trader-plan` + 3 analyst reports | 3-way risk transcript |
| [portfolio-decision](../.claude/skills/portfolio-decision/SKILL.md) | `risk-debate`, `trader-plan`, `research-manager` | Final rating (terminal) |

## 2. Trio: zsxq report library

```
┌──────────────────┐     file_id     ┌──────────────────┐
│ zsxq-recommend   │ ─────────────▶  │   zsxq-analyze   │
│ (find PDFs)      │                 │ (deep-read 1 PDF)│
└────────┬─────────┘                 └─────────┬────────┘
         │           orchestrates both         │
         │     ┌───────────────────────────────┘
         ▼     ▼
    ┌──────────────────┐
    │   zsxq-ideas     │  ← idea-generation funnel from zsxq feed
    │ (themed/fishing) │     (fans out N parallel /zsxq-analyze)
    └──────────────────┘
```

All three read `db/zsxq.db`. `zsxq-recommend` reads metadata only; `zsxq-analyze` extracts the full PDF text (via `ocrmac` if needed); `zsxq-ideas` orchestrates both into either a 5-10 ticker shortlist with `idea-generation`'s Step-4 presentation (saved to `reports/ideas/zsxq_<slug>_<date>.md`), or — in **theme-build mode** — durable `theme-research` baskets seeded from the cluster's actual broker content (`reports/themes/<slug>_theme.md`). Theme-build is the one zsxq path that crosses into `theme-research`.

| Skill | Purpose |
|---|---|
| [zsxq-recommend](../.claude/skills/zsxq-recommend/SKILL.md) | Surface candidate `file_id`s from the recent feed |
| [zsxq-analyze](../.claude/skills/zsxq-analyze/SKILL.md) | Deep-read one PDF and answer a question about it |
| [zsxq-ideas](../.claude/skills/zsxq-ideas/SKILL.md) | Generate ideas / baskets from the zsxq feed — **themed** ("AI infra ideas from zsxq"), **fishing** ("what should I buy / pitch me something"), or **theme-build** ("build themes from zsxq" → seeds/refreshes `theme-research` baskets from real broker content via `evidence_bundle.py` + the zsxq citation convention). Themed/fishing save to `reports/ideas/`; theme-build hands off to `theme-research` at `reports/themes/` |

## 3. Coverage-lifecycle workflows (no hard deps — logical order)

```
idea-generation → initiating-coverage → earnings-preview → earnings-analysis → model-update
                       │                                                            │
                       └─────── builds on ───┐                                       │
                                             ▼                                       ▼
                                     company-research                         thesis-tracker
                                             │
                                             └── consumed by ──▶ compare-companies (head-to-head)
```

- [initiating-coverage](../.claude/skills/initiating-coverage/SKILL.md) is a 5-task workflow whose Task-1 is essentially `company-research`.
- [earnings-preview](../.claude/skills/earnings-preview/SKILL.md) → [earnings-analysis](../.claude/skills/earnings-analysis/SKILL.md) → [model-update](../.claude/skills/model-update/SKILL.md) is the quarterly cycle for a name already under coverage.
- [thesis-tracker](../.claude/skills/thesis-tracker/SKILL.md) is the long-running journal that consumes results from the others.
- [idea-generation](../.claude/skills/idea-generation/SKILL.md) seeds the funnel via generic quantitative / thematic / special-situation screens. [zsxq-ideas](../.claude/skills/zsxq-ideas/SKILL.md) seeds the same funnel from the zsxq library instead (themed or fishing). Both feed downstream `company-research` → `initiating-coverage` / `trading-analysis`.
- [compare-companies](../.claude/skills/compare-companies/SKILL.md) takes **2 to 4** `company-research` outputs and produces an N-way head-to-head comparison focused on the delta — product overlap matrix (N+1 columns), moat anatomy (N-column tables), customer overlap, dimension-by-dimension scorecard (rank-based for N≥3). **Default behavior: two files per tuple — English at `reports/compare/<A>_vs_<B>[_vs_<C>...].md` and Simplified Chinese at `reports/compare/<...>_zh.md`** (5–9k words for N=2; 7–12k for N=3; 10–15k for N=4; natively authored in each language). Users can override to single-language with `--en-only` / `--zh-only`. If a research doc is missing or stale, it invokes `company-research` on the missing side first. N≥5 not supported — split into multiple pairwise reports or use `sector-overview`.

## 4. Standalone, no dependencies

| Skill | Purpose |
|---|---|
| [sector-overview](../.claude/skills/sector-overview/SKILL.md) | Industry-level landscape report |
| [take-profit-lab](../.claude/skills/take-profit-lab/SKILL.md) | Exit-discipline backtest on a single ticker (hold / tier / trailing stop / vol-aware); complements `trader-plan` (entry) and `portfolio-decision` (final rating) — owns the *exit* question |
| [etf-overlap](../.claude/skills/etf-overlap/SKILL.md) | Head-to-head holdings overlap for 2–4 ETFs — duplicative / complementary / orthogonal verdict, sector skew, top common positions; SEC N-PORT primary, issuer CSV daily, yfinance fallback. **English default; Chinese opt-in** |
| [ma-event-tracker](../.claude/skills/ma-event-tracker/SKILL.md) | Single-deal M&A monitor — spread / milestones / break-risk map / scenario probability with named triggers; SEC EDGAR (S-4, DEFM14A, 425, 8-K) + jurisdiction antitrust portals. **English default; Chinese opt-in** |
| [theme-research](../.claude/skills/theme-research/SKILL.md) | Tracked thematic baskets — single markdown file per theme at `reports/themes/<slug>_theme.md` (Tracked tickers table + thesis + performance + drift signals); create / refresh / mutate / list modes; drift detection on theme-membership stability. **English default; Chinese opt-in** |
| [regulatory-risk-monitor](../.claude/skills/regulatory-risk-monitor/SKILL.md) | Single-case regulatory tracking on one ticker — FDA AdComm / DOJ-FTC antitrust / EU DG-COMP / SAMR / CSRC / EPA / FCC; evidence timeline + exposure map + scenario triggers. **English default; Chinese opt-in** |
| [canslim-screener](/Users/x/.claude/skills/canslim-screener/SKILL.md) | William O'Neil CANSLIM screen (lives in `~/.claude`, not project) |
| [catalyst-calendar](../.claude/skills/catalyst-calendar/SKILL.md) | Upcoming earnings / events |
| [morning-note](../.claude/skills/morning-note/SKILL.md) | 7 am desk note |
| [earnings-upload-to-db](../.claude/skills/earnings-upload-to-db/SKILL.md) | PDF ingest into `db/notes.db` (data-plumbing, not analysis) |

---

## Key observations

- **Only the trading-analysis chain has machine-enforced deps** (the `## Prerequisites` blocks with `[[…]]` wikilinks). Everything else is independent — run them in any order.
- **`company-research` is the most reused artifact** — the trading pipeline, `initiating-coverage` (Task 1), and `compare-companies` (N per N-way comparison, where N ∈ {2, 3, 4}) all build on it.
- **`sec-report-summary` is conditional**: it's a Step-0.5 sub-skill of `company-research` for US issuers only; for non-US issuers (China A-share / HK / Taiwan / Japan / Korea), `company-research` skips it and builds the historical-evolution threads directly from domicile-portal filings. It can also be invoked standalone if the user just wants the SEC narrative without the full deep dive.
- **`trading-analysis` is the only true orchestrator**; `initiating-coverage` is 5 sequential tasks the user runs explicitly, not a one-shot pipeline.
- **Two data-source skills feed everything else indirectly**: `earnings-upload-to-db` → `db/notes.db`, and `zsxq-recommend` / `zsxq-analyze` → `db/zsxq.db`. They're not called by other skills, but the artifacts they produce are read by analysts.

---

## Maintenance

Update this file when any of the following change:

1. A skill is **added** under `.claude/skills/` — add a row to the relevant section.
2. A skill is **removed** — delete its row and any references.
3. A skill's **`## Prerequisites`** block changes (new `[[wikilink]]` upstream skill, or one removed) — update the arrow in section 1.
4. The orchestrator behavior of [trading-analysis](../.claude/skills/trading-analysis/SKILL.md) changes (e.g. a new analyst joins the parallel fan-out).

Also bump the "Last updated" date at the top.
