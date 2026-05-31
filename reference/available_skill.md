# Available Skills — Graph View

Snapshot of every skill registered for this project, grouped by role and dependency chain.

> **Keep this file in sync.** Whenever a skill is added, removed, or its `## Prerequisites` block changes under `.claude/skills/`, update this file in the same commit and bump the "Last updated" date below. See the [Maintenance](#maintenance) section at the bottom for the checklist.

Last updated: 2026-05-31 (LLMQuant/skills cross-pollination: (1) **`company-research`** gains an optional Section 10 — "Investor-lens scorecards" — with Buffett / Munger / Damodaran / Howard Marks cycle rubrics adapted from the [LLMQuant investor-lens collection](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-investor-lenses); rubrics live in `references/investor_lenses.md`, plumbed to existing data (Sections 1–9 + `indicators.db` for VIX/10Y/HY OAS). (2) **NEW skill `take-profit-lab`** — exit-discipline backtest (hold / tier-out / strict-exit / trailing stop / vol-aware) on yfinance-adjusted prices; complements [[trader-plan]] (entry) and [[portfolio-decision]] (final rating); reports go to `reports/take-profit/<TICKER>_<YYYY-MM-DD>.md`. (3) **All four research skills** (`company-research`, `compare-companies`, `earnings-analysis`, `sector-overview`) now carry an at-a-glance `## Guardrails` block summarizing the load-bearing don't-dos + a mandatory `## Data Used / 数据来源清单` manifest at the end of every report (categories + dates + freshness, complementing the existing inline citations).

Earlier: 2026-05-31 (`compare-companies` N-way support 2-4 companies; prior-research existence check hardened across `compare-companies` + `company-research`)

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

## 2. Pair: zsxq report library

```
┌──────────────────┐     file_id     ┌──────────────────┐
│ zsxq-recommend   │ ─────────────▶  │   zsxq-analyze   │
│ (find PDFs)      │                 │ (deep-read 1 PDF)│
└──────────────────┘                 └──────────────────┘
```

Both read `db/zsxq.db`. Recommend reads metadata only; analyze extracts the full PDF text (via `ocrmac` if needed).

| Skill | Purpose |
|---|---|
| [zsxq-recommend](../.claude/skills/zsxq-recommend/SKILL.md) | Surface candidate `file_id`s from the recent feed |
| [zsxq-analyze](../.claude/skills/zsxq-analyze/SKILL.md) | Deep-read one PDF and answer a question about it |

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
- [idea-generation](../.claude/skills/idea-generation/SKILL.md) seeds the funnel.
- [compare-companies](../.claude/skills/compare-companies/SKILL.md) takes **2 to 4** `company-research` outputs and produces an N-way head-to-head comparison focused on the delta — product overlap matrix (N+1 columns), moat anatomy (N-column tables), customer overlap, dimension-by-dimension scorecard (rank-based for N≥3). **Default behavior: two files per tuple — English at `reports/compare/<A>_vs_<B>[_vs_<C>...].md` and Simplified Chinese at `reports/compare/<...>_zh.md`** (5–9k words for N=2; 7–12k for N=3; 10–15k for N=4; natively authored in each language). Users can override to single-language with `--en-only` / `--zh-only`. If a research doc is missing or stale, it invokes `company-research` on the missing side first. N≥5 not supported — split into multiple pairwise reports or use `sector-overview`.

## 4. Standalone, no dependencies

| Skill | Purpose |
|---|---|
| [sector-overview](../.claude/skills/sector-overview/SKILL.md) | Industry-level landscape report |
| [take-profit-lab](../.claude/skills/take-profit-lab/SKILL.md) | Exit-discipline backtest on a single ticker (hold / tier / trailing stop / vol-aware); complements `trader-plan` (entry) and `portfolio-decision` (final rating) — owns the *exit* question |
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
