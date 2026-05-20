---
name: trading-analysis
description: Run the full TradingAgents pipeline end-to-end on a ticker and trade date — four analyst reports, bull/bear debate, research plan, trader proposal, risk debate, and final portfolio decision. Use when the user says "analyze <ticker>", "should I buy <ticker>", "run trading analysis on X for <date>", or invokes /trading-analysis directly.
argument-hint: <ticker> <YYYY-MM-DD> [--asset-type stock|crypto] [--depth 1|2|3] [--analysts market,sentiment,news,fundamentals]
allowed-tools: [Agent, Bash, Read, Write]
---

# Trading Analysis Orchestrator

Run the complete TradingAgents pipeline: collect four analyst reports in parallel, run a bull/bear debate, produce a research plan, generate a trader proposal, run a risk debate, and emit the final portfolio decision.

## Inputs

- `<ticker>` — e.g. `NVDA`, `BTC-USD`.
- `<trade_date>` — `YYYY-MM-DD`, the as-of date for the analysis.
- `--asset-type` — `stock` (default) or `crypto`.
- `--depth` — research depth controlling debate rounds. `1` = 1 round bull-bear + 1 round risk; `2` = 2 + 1; `3` = 3 + 2. Default `2`.
- `--analysts` — comma-separated subset of `market,sentiment,news,fundamentals` to run. Default = all four.

## Pipeline

### Step 1 — Analyst reports (in parallel)

For each enabled analyst, spawn a subagent in parallel using the Agent tool with the matching skill prompt. Pass `<ticker>`, `<trade_date>`, and `<asset_type>` to each:

- [[market-analyst]] → `market_report`
- [[sentiment-analyst]] → `sentiment_report`
- [[news-analyst]] → `news_report`
- [[fundamentals-analyst]] → `fundamentals_report`

Wait for all four to return (or skip any analyst not in `--analysts`).

### Step 2 — Bull/Bear debate

Invoke [[bull-bear-debate]] with all four reports and `--rounds {depth_bull_rounds}` where:
- depth=1 → 1, depth=2 → 2, depth=3 → 3.

Output: `debate_history`.

### Step 3 — Research Manager

Invoke [[research-manager]] with `debate_history` and the four reports.

Output: `investment_plan` (markdown ResearchPlan).

### Step 4 — Trader

Invoke [[trader-plan]] with `investment_plan`.

Output: `trader_investment_plan` (markdown TraderProposal).

### Step 5 — Risk debate

Invoke [[risk-debate]] with `trader_investment_plan` and the four reports. Rounds:
- depth=1 → 1, depth=2 → 1, depth=3 → 2.

Output: `risk_debate_history`.

### Step 6 — Portfolio Manager (final decision)

Invoke [[portfolio-decision]] with `investment_plan`, `trader_investment_plan`, `risk_debate_history`, and past context loaded by that skill from `memory/trading_memory.md`.

Output: `final_trade_decision` (markdown PortfolioDecision).

### Step 7 — Final report assembly

By this point each sub-skill has written its own section to disk under `reports/<TICKER>_<TRADE-DATE>/`:

```
reports/<TICKER>_<TRADE-DATE>/
├── market-analyst.md
├── sentiment-analyst.md
├── news-analyst.md
├── fundamentals-analyst.md
├── bull-bear-debate.md
├── research-manager.md
├── trader-plan.md
├── risk-debate.md
└── portfolio-decision.md
```

Assemble `full_report.md` as a single markdown document with these top-level sections, in order:

1. Header: `# Trading Analysis: <TICKER> @ <TRADE-DATE>` plus a one-sentence executive line pulled from the PortfolioDecision's Executive Summary.
2. `## Market Analyst Report` — contents of `market-analyst.md` (or full `market_report` from context).
3. `## Sentiment Analyst Report` — contents of `sentiment-analyst.md`.
4. `## News Analyst Report` — contents of `news-analyst.md`.
5. `## Fundamentals Analyst Report` — contents of `fundamentals-analyst.md`.
6. `## Bull / Bear Debate` — contents of `bull-bear-debate.md`.
7. `## Research Plan` — contents of `research-manager.md`.
8. `## Trader Proposal` — contents of `trader-plan.md`.
9. `## Risk Debate` — contents of `risk-debate.md`.
10. `## Portfolio Decision` — contents of `portfolio-decision.md`.

Write the assembled markdown to `reports/<TICKER>_<TRADE-DATE>/full_report.md` using the Write tool, then print the full report to the user.

The PortfolioDecision step has already persisted the final decision to `memory/trading_memory.md` as well.

## Notes

- **Parallelism for step 1** — issue the four Agent calls in a single response (multiple tool_use blocks) so they execute concurrently. Sequential analyst execution wastes wall-clock time.
- **Crypto specifics** — when `--asset-type crypto`, fundamentals may come back `<unavailable>`; the downstream skills already handle this gracefully.
- **Failure modes** — if a fetcher script returns an error string instead of data, the analyst skill surfaces it in its report. Continue the pipeline; do not abort.
