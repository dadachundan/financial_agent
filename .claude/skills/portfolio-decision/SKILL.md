---
name: portfolio-decision
description: Produce the final PortfolioDecision — synthesizes the risk-analyst debate into a final 5-tier rating with executive summary and investment thesis, appends to the persistent memory log, and returns the final report. Use as the last step of a trading workflow, after risk-debate.
argument-hint: <ticker> <YYYY-MM-DD> [--asset-type stock|crypto]
allowed-tools: [Bash, Read, Write]
---

# Portfolio Manager

As the **Portfolio Manager**, synthesize the risk analysts' debate and deliver the final trading decision. Be decisive and ground every conclusion in specific evidence from the analysts.

## Prerequisites

This skill needs three upstream artifacts:

- `risk_debate_history` — from [[risk-debate]]
- `trader_investment_plan` — from [[trader-plan]]
- `investment_plan` — from [[research-manager]]

**If `risk_debate_history` is missing**, invoke [[risk-debate]] first. That will cascade through [[trader-plan]], [[research-manager]], [[bull-bear-debate]], and the four analyst skills as needed.

`past_context` is loaded by this skill itself from the memory log — no prerequisite skill needed, but the log file may be empty on first ever run.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- `<ticker>`, `<trade_date>`, `<asset_type>` — instrument context.
- `investment_plan` — the [[research-manager]] ResearchPlan.
- `trader_investment_plan` — the [[trader-plan]] TraderProposal.
- `risk_debate_history` — the full transcript from [[risk-debate]].
- `past_context` — lessons from prior decisions, fetched up front:
  ```bash
  python scripts/memory_log.py read --ticker <ticker>
  ```

## Rating scale (use exactly one)

See [rating taxonomy](../../../references/rating_taxonomy.md).

- **Buy** — Strong conviction to enter or add to position.
- **Overweight** — Favorable outlook; gradually increase exposure.
- **Hold** — Maintain current position; no action needed.
- **Underweight** — Reduce exposure; take partial profits.
- **Sell** — Exit position or avoid entry.

If `past_context` is non-empty, incorporate its lessons; otherwise rely solely on the current analysis.

## Output schema (produce this markdown exactly)

```markdown
**Rating**: <Buy | Overweight | Hold | Underweight | Sell>

**Executive Summary**: <Concise action plan covering entry strategy, position sizing, key risk levels, and time horizon. Two to four sentences.>

**Investment Thesis**: <Detailed reasoning anchored in specific evidence from the analysts' debate. Incorporate prior lessons from past_context if any; otherwise rely solely on the current analysis.>

**Price Target**: <optional — number in the instrument's quote currency, or omit the line>

**Time Horizon**: <optional — e.g. "3-6 months", or omit the line>
```

## Persist output

After producing the markdown, write it to `reports/<TICKER>_<TRADE-DATE>/portfolio-decision.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.

## Memory write

After the file is written, append it to the decision log:

```bash
python scripts/memory_log.py append \
    --ticker <TICKER> \
    --trade-date <YYYY-MM-DD> \
    --decision-file reports/<TICKER>_<TRADE-DATE>/portfolio-decision.md
```

This creates a `pending` entry that a later reflection job can update with realized returns. See [memory format](../../../references/memory_format.md) for schema details.
