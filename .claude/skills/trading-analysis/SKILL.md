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
- `<trade_date>` — `YYYY-MM-DD`, the as-of date for the analysis.
- `--asset-type` — `stock` (default) or `crypto`.
- `--depth` — research depth controlling debate rounds. `1` = 1 round bull-bear + 1 round risk; `2` = 2 + 1; `3` = 3 + 2. Default `2`.
- `--analysts` — comma-separated subset of `sentiment,news,company-research` to run. Default = all three.

## Pipeline

### Step 1 — Analyst reports (in parallel)

For each enabled analyst, spawn a subagent in parallel using the Agent tool with the matching skill prompt. Pass `<ticker>`, `<trade_date>`, and `<asset_type>` to each:

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

## Notes

- **Parallelism for step 1** — issue the three Agent calls in a single response (multiple tool_use blocks) so they execute concurrently. Sequential analyst execution wastes wall-clock time.
- **Crypto specifics** — when `--asset-type crypto`, `company-research` will produce a thin/abbreviated report (the deep-dive structure assumes a corporate issuer); the downstream skills already handle this gracefully.
- **Failure modes** — if a fetcher script returns an error string instead of data, the analyst skill surfaces it in its report. Continue the pipeline; do not abort.
