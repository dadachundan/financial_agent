---
name: trading-analysis
description: Run the full TradingAgents pipeline end-to-end on a ticker and trade date — three analyst reports (sentiment, news, company-research), bull/bear debate, research plan, trader proposal, risk debate, and final portfolio decision. Use when the user says "analyze <ticker>", "should I buy <ticker>", "run trading analysis on X for <date>", or invokes /trading-analysis directly.
argument-hint: <ticker> <YYYY-MM-DD> [--asset-type stock|crypto] [--depth 1|2|3] [--analysts sentiment,news,company-research]
allowed-tools: [Agent, Bash, Read, Write]
---

# Trading Analysis Orchestrator

Run the complete TradingAgents pipeline: collect three analyst reports in parallel, run a bull/bear debate, produce a research plan, generate a trader proposal, run a risk debate, and emit the final portfolio decision.

## Inputs

- `<ticker>` — e.g. `NVDA`, `BTC-USD`.
- `<trade_date>` — `YYYY-MM-DD`, the as-of date for the analysis. If `<trade_date>` is not a trading day, resolve the reference session to the last completed close and state both dates in every stage header (`Trade date 2026-05-23 (Sat) · reference close 2026-05-22`); pass the resolved reference date to all stages so they share one anchor price/date instead of each improvising its own.
- `--asset-type` — `stock` (default) or `crypto`.
- `--depth` — research depth controlling debate rounds. `1` = 1 round bull-bear + 1 round risk; `2` = 2 + 1; `3` = 3 + 2. Default `2`.
- `--analysts` — comma-separated subset of `sentiment,news,company-research` to run. Default = all three.

## Pipeline

### Step 1 — Analyst reports (memory-safe scheduling)

For each enabled analyst, spawn an Agent-tool subagent with the matching skill prompt. Pass `<ticker>`, `<trade_date>`, and `<asset_type>` to each. **Scheduling MUST follow the CLAUDE.md 16 GB memory-watch rules:**

- If the company-research cache (below) misses, run the [[company-research]] subagent **ALONE first** — it is the heavy 6,000–10,000-word skill and must never share a fan-out.
- [[sentiment-analyst]] + [[news-analyst]] may run as a 2-wide pair ONLY if the memory watcher is running (`pgrep -lf mem-watch-16gb.sh` returns a PID) AND free RAM is >60% (`memory_pressure | grep -i 'free percentage'`); otherwise run them sequentially too.
- Pre-flight for any 2-wide launch: start `/tmp/mem-watch-16gb.sh` first (script in CLAUDE.md); stop it (`pkill -f mem-watch-16gb.sh`) when Step 1 completes.

The enabled analysts and their outputs:

- [[sentiment-analyst]] → `sentiment_report`
- [[news-analyst]] → `news_report`
- [[company-research]] → `company_research_report` — deep institutional-grade fundamental coverage (business, management, products, customers, competition, TAM, risks). **Before spawning, check `reports/company/` for an existing report on this ticker** by globbing `reports/company/*_<TICKER>/` and selecting the most-recently-modified match (see [`output_path.md`](../../../references/output_path.md)). If a `*_Research_Document.md` inside is less than 30 days old, read it and pass its contents as `company_research_report` instead of re-running — company-research is a 6,000–10,000-word deep dive that takes ~10–30 min. The deep-dive lives at the company-folder root and is *not* copied into `trading/<TRADE-DATE>/`; the assembly step (Step 7) reads it directly from `<company-folder>/<*>_Research_Document.md`.

Wait for all three to return (or skip any analyst not in `--analysts`).

### Step 2 — Bull/Bear debate

Invoke [[bull-bear-debate]] with all three reports and `--rounds {depth_bull_rounds}` where:
- depth=1 → 1, depth=2 → 2, depth=3 → 3.

Output: `debate_history`.

### Step 3 — Research Manager

Invoke [[research-manager]] with `debate_history` and the three reports.

Output: `investment_plan` (markdown ResearchPlan).

### Step 4 — Trader

Invoke [[trader-plan]] with `investment_plan`.

Output: `trader_investment_plan` (markdown TraderProposal).

### Step 5 — Risk debate

Invoke [[risk-debate]] with `trader_investment_plan` and the three reports. Rounds:
- depth=1 → 1, depth=2 → 1, depth=3 → 2.

Output: `risk_debate_history`.

### Step 6 — Portfolio Manager (final decision)

Invoke [[portfolio-decision]] with `investment_plan`, `trader_investment_plan`, `risk_debate_history`, and past context loaded by that skill from `memory/trading_memory.md`.

Output: `final_trade_decision` (markdown PortfolioDecision).

### Step 7 — Final report assembly

By this point each sub-skill has written its own section to disk under the resolved `<company-folder>/trading/<TRADE-DATE>/`:

```
reports/company/<COMPANY_FOLDER>/
├── <COMPANY_FOLDER>_Research_Document.md   ← time-invariant (from company-research)
├── charts/                                  ← optional, from company-research
├── valuation/                               ← optional, from initiating-coverage
└── trading/<TRADE-DATE>/                    ← time-variant pipeline outputs
    ├── sentiment-analyst.md
    ├── news-analyst.md
    ├── bull-bear-debate.md
    ├── research-manager.md
    ├── trader-plan.md
    ├── risk-debate.md
    ├── portfolio-decision.md
    └── full_report.md                       ← written by this step
```

See [`output_path.md`](../../../references/output_path.md) for how `<company-folder>` is resolved from `<TICKER>`.

Assemble `full_report.md` as a single markdown document with these top-level sections, in order:

1. Header: `# Trading Analysis: <TICKER> @ <TRADE-DATE>` plus a one-sentence executive line pulled from the PortfolioDecision's Executive Summary.
2. `## Sentiment Analyst Report` — contents of `sentiment-analyst.md` (same dir).
3. `## News Analyst Report` — contents of `news-analyst.md` (same dir).
4. `## Company Research Report` — contents of the `<COMPANY_FOLDER>_Research_Document.md` at the company-folder root (one level up from `trading/<TRADE-DATE>/`).
5. `## Bull / Bear Debate` — contents of `bull-bear-debate.md`.
6. `## Research Plan` — contents of `research-manager.md`.
7. `## Trader Proposal` — contents of `trader-plan.md`.
8. `## Risk Debate` — contents of `risk-debate.md`.
9. `## Portfolio Decision` — contents of `portfolio-decision.md`.

Write the assembled markdown to `<company-folder>/trading/<TRADE-DATE>/full_report.md` using the Write tool, then print the full report to the user.

The PortfolioDecision step has already persisted the final decision to `memory/trading_memory.md` as well.

### Step 8 — Completion checklist (mandatory)

A run that skips Step 7 or this checklist is an **incomplete task** — do not declare done until all three pass (a past AMD run shipped 7 stage files but no `full_report.md` because nothing verified completeness):

1. `ls <company-folder>/trading/<TRADE-DATE>/` and confirm every enabled stage file **plus `full_report.md`** exists. If any is missing, re-run that stage before finishing.
2. Confirm the memory log got the new entry: `python scripts/memory_log.py list` shows `[<TRADE-DATE> | <TICKER> | <Rating>] pending`.
3. Stage, commit (Conventional Commit, e.g. `feat(trading): <TICKER> <TRADE-DATE> full pipeline — <Rating>`), and push to `main` — per the project-wide always-commit rule.

### Further viewing — explainer videos (delegated convention)

This orchestrator mainly delegates; it does not author prose of its own. Each constituent report skill it chains (company-research, news-analyst, sentiment-analyst, bull-bear-debate, etc.) follows the shared **Further viewing — explainer videos** convention: where a section covers something hard to picture from prose alone (a robot's actuators / reducers / force sensors, a manufacturing or scientific process, a complex product architecture or market-structure concept), it embeds **1–3 short validated explainer videos** (YouTube / Bilibili) in their own slot — never as a citation, never carrying a number. No action is required here in the orchestrator; just preserve those video blocks verbatim when assembling `full_report.md` (do not strip or renumber them). See each sub-skill's SKILL.md for the full block.

## Notes

- **Scheduling for step 1** — never issue a fan-out that includes [[company-research]]; run it alone first when its cache misses. sentiment + news may pair 2-wide only under the watcher + free-RAM conditions stated in Step 1; the default is sequential. A swapped-to-death 16 GB machine loses far more wall-clock time than sequential analysts ever do.
- **Crypto specifics** — when `--asset-type crypto`, `company-research` will produce a thin/abbreviated report (the deep-dive structure assumes a corporate issuer); the downstream skills already handle this gracefully.
- **Failure modes** — if a fetcher script returns an error string instead of data, the analyst skill surfaces it in its report. Continue the pipeline; do not abort.
