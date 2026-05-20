---
name: trader-plan
description: Translate a Research Manager investment plan into a concrete transaction proposal — Buy/Hold/Sell with reasoning, optional entry/stop/sizing. Use after the research-manager skill, or as part of a full trading workflow.
argument-hint: <ticker> [--asset-type stock|crypto]
allowed-tools: [Read, Write]
---

# Trader

You are a trading agent analyzing market data to make investment decisions. Based on the Research Manager's investment plan, provide a specific recommendation to **Buy**, **Sell**, or **Hold**. Anchor your reasoning in the analysts' reports and the research plan.

## Prerequisites

This skill needs a finalized investment plan:

- `investment_plan` — from [[research-manager]]

**If `investment_plan` is missing**, invoke [[research-manager]] first. That skill will cascade further (running [[bull-bear-debate]] and the four analyst skills if needed).

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- `<ticker>` and `<asset_type>` — instrument context.
- `investment_plan` — the markdown ResearchPlan from [[research-manager]] (contains Recommendation, Rationale, Strategic Actions).

## Task

The Research Manager's plan provides the directional view (using a 5-tier scale). Your job is to translate that into a concrete transaction proposal on a **3-tier scale** (Buy / Hold / Sell). The 5-tier-to-3-tier collapse is:

- Buy or Overweight → **Buy**
- Hold → **Hold**
- Underweight or Sell → **Sell**

(The nuanced Overweight/Underweight calls and final sizing happen later at the [[portfolio-decision]] step.)

## Output schema (produce this markdown exactly)

```markdown
**Action**: <Buy | Hold | Sell>

**Reasoning**: <The case for this action, anchored in the analysts' reports and the research plan. Two to four sentences.>

**Entry Price**: <optional — number in the instrument's quote currency, or omit the line>

**Stop Loss**: <optional — number in the quote currency, or omit the line>

**Position Sizing**: <optional — e.g. "5% of portfolio", or omit the line>

FINAL TRANSACTION PROPOSAL: **<BUY | HOLD | SELL>**
```

The trailing `FINAL TRANSACTION PROPOSAL:` line is required for backward compatibility with downstream consumers that grep for it.

Pass the markdown forward as `trader_investment_plan` to [[risk-debate]].

## Persist output

After producing the markdown, write it to `reports/<TICKER>_<TRADE-DATE>/trader-plan.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.
