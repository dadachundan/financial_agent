# Available Skills — Graph View

Snapshot of every skill registered for this project, grouped by role and dependency chain. Keep this file in sync whenever a skill is added, removed, or its prerequisites change (see [CLAUDE.md](CLAUDE.md) → "Available Skills").

Last updated: 2026-05-23

---

## 1. Trading-analysis pipeline (the spine — explicit dependencies)

This is the only chain with **machine-enforced** upstream skills (declared via `[[wikilink]]` references in each SKILL.md's `## Prerequisites` block). Each downstream skill auto-cascades upstream if its prerequisite is missing.

```
                  ┌──────────────────┐
                  │ trading-analysis │  ← orchestrator (runs whole chain)
                  └────────┬─────────┘
                           │ fans out 3 analysts in parallel
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────────┐ ┌─────────────┐ ┌────────────────────┐
│ sentiment-analyst│ │ news-analyst│ │  company-research  │
└────────┬─────────┘ └──────┬──────┘ └──────────┬─────────┘
         └──────────────────┼───────────────────┘
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
| [trading-analysis](.claude/skills/trading-analysis/SKILL.md) | — (orchestrator) | Runs the whole pipeline end-to-end |
| [sentiment-analyst](.claude/skills/sentiment-analyst/SKILL.md) | — | 7-day sentiment report (Yahoo / StockTwits / Reddit) |
| [news-analyst](.claude/skills/news-analyst/SKILL.md) | — | Macro + ticker news, past 30 days |
| [company-research](.claude/skills/company-research/SKILL.md) | — | 6–10k word deep dive |
| [bull-bear-debate](.claude/skills/bull-bear-debate/SKILL.md) | 3 analyst reports | Multi-round debate transcript |
| [research-manager](.claude/skills/research-manager/SKILL.md) | `bull-bear-debate` | ResearchPlan + 5-tier rating |
| [trader-plan](.claude/skills/trader-plan/SKILL.md) | `research-manager` | Buy/Hold/Sell proposal |
| [risk-debate](.claude/skills/risk-debate/SKILL.md) | `trader-plan` + 3 analyst reports | 3-way risk transcript |
| [portfolio-decision](.claude/skills/portfolio-decision/SKILL.md) | `risk-debate`, `trader-plan`, `research-manager` | Final rating (terminal) |

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
| [zsxq-recommend](.claude/skills/zsxq-recommend/SKILL.md) | Surface candidate `file_id`s from the recent feed |
| [zsxq-analyze](.claude/skills/zsxq-analyze/SKILL.md) | Deep-read one PDF and answer a question about it |

## 3. Coverage-lifecycle workflows (no hard deps — logical order)

```
idea-generation → initiating-coverage → earnings-preview → earnings-analysis → model-update
                       │                                                            │
                       └─────── builds on ───┐                                       │
                                             ▼                                       ▼
                                     company-research                         thesis-tracker
```

- [initiating-coverage](.claude/skills/initiating-coverage/SKILL.md) is a 5-task workflow whose Task-1 is essentially `company-research`.
- [earnings-preview](.claude/skills/earnings-preview/SKILL.md) → [earnings-analysis](.claude/skills/earnings-analysis/SKILL.md) → [model-update](.claude/skills/model-update/SKILL.md) is the quarterly cycle for a name already under coverage.
- [thesis-tracker](.claude/skills/thesis-tracker/SKILL.md) is the long-running journal that consumes results from the others.
- [idea-generation](.claude/skills/idea-generation/SKILL.md) seeds the funnel.

## 4. Standalone, no dependencies

| Skill | Purpose |
|---|---|
| [sector-overview](.claude/skills/sector-overview/SKILL.md) | Industry-level landscape report |
| [sec-report-summary](.claude/skills/sec-report-summary/SKILL.md) | Multi-year 10-K/Q/8-K digest from `db/financial_reports.db` |
| [canslim-screener](/Users/x/.claude/skills/canslim-screener/SKILL.md) | William O'Neil CANSLIM screen (lives in `~/.claude`, not project) |
| [catalyst-calendar](.claude/skills/catalyst-calendar/SKILL.md) | Upcoming earnings / events |
| [morning-note](.claude/skills/morning-note/SKILL.md) | 7 am desk note |
| [earnings-upload-to-db](.claude/skills/earnings-upload-to-db/SKILL.md) | PDF ingest into `db/notes.db` (data-plumbing, not analysis) |

---

## Key observations

- **Only the trading-analysis chain has machine-enforced deps** (the `## Prerequisites` blocks with `[[…]]` wikilinks). Everything else is independent — run them in any order.
- **`company-research` is the most reused artifact** — both the trading pipeline and `initiating-coverage` (Task 1) build on it.
- **`trading-analysis` is the only true orchestrator**; `initiating-coverage` is 5 sequential tasks the user runs explicitly, not a one-shot pipeline.
- **Two data-source skills feed everything else indirectly**: `earnings-upload-to-db` → `db/notes.db`, and `zsxq-recommend` / `zsxq-analyze` → `db/zsxq.db`. They're not called by other skills, but the artifacts they produce are read by analysts.

---

## Maintenance

Update this file when any of the following change:

1. A skill is **added** under `.claude/skills/` — add a row to the relevant section.
2. A skill is **removed** — delete its row and any references.
3. A skill's **`## Prerequisites`** block changes (new `[[wikilink]]` upstream skill, or one removed) — update the arrow in section 1.
4. The orchestrator behavior of [trading-analysis](.claude/skills/trading-analysis/SKILL.md) changes (e.g. a new analyst joins the parallel fan-out).

Also bump the "Last updated" date at the top.
