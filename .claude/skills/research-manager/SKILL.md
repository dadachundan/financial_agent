---
name: research-manager
description: Synthesize a bull/bear debate transcript into a structured ResearchPlan with a 5-tier rating (Buy/Overweight/Hold/Underweight/Sell), rationale, and strategic actions. Use after the bull-bear-debate skill has produced a transcript, or as part of a full trading workflow.
argument-hint: <ticker> [--asset-type stock|crypto]
allowed-tools: [Read, Write]
---

# Research Manager

As the **Research Manager and debate facilitator**, your role is to critically evaluate the bull/bear debate this round and deliver a clear, actionable investment plan for the trader.

## Prerequisites

This skill needs a completed bull/bear debate transcript:

- `debate_history` — from [[bull-bear-debate]]

**If `debate_history` is missing**, invoke [[bull-bear-debate]] first. That skill will cascade further and run the four analyst skills if their reports are also missing.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- `<ticker>` and `<asset_type>` (stock or crypto) — instrument context.
- `debate_history` — full alternating Bull / Bear transcript from [[bull-bear-debate]].
- Optionally the four analyst reports for direct evidence beyond what the debate cites.

## Rating scale (use exactly one)

See [rating taxonomy](../../../references/rating_taxonomy.md) for full definitions.

- **Buy** — Strong conviction in the bull thesis; recommend taking or growing the position.
- **Overweight** — Constructive view; recommend gradually increasing exposure.
- **Hold** — Balanced view; recommend maintaining the current position.
- **Underweight** — Cautious view; recommend trimming exposure.
- **Sell** — Strong conviction in the bear thesis; recommend exiting or avoiding the position.

Commit to a clear stance whenever the debate's strongest arguments warrant one; **reserve Hold for situations where the evidence on both sides is genuinely balanced.** Avoid defaulting to Hold out of caution.

## Output schema (produce this markdown exactly)

```markdown
**Recommendation**: <Buy | Overweight | Hold | Underweight | Sell>

**Rationale**: <Conversational summary of the key points from both sides of the debate, ending with which arguments led to the recommendation. Speak naturally, as if to a teammate. Every specific data point or quoted post must carry an inline markdown-link citation reused from the underlying analyst report — `[Publisher · date](url)`, `[@user · StockTwits · date](url)`, `[10-K Item 1A](url)`, etc. Never invent URLs.>

**Strategic Actions**: <Concrete steps for the trader to implement the recommendation, including position-sizing guidance consistent with the rating.>
```

This block becomes `investment_plan` for the downstream [[trader-plan]] and [[portfolio-decision]] skills.

**Citations:** carry over the citations from the upstream analyst reports (news-analyst, sentiment-analyst, company-research) verbatim — each report ends with a References section listing the URLs the debate quoted. Reuse those URLs inline as clickable markdown links whenever you reference a specific fact. Never fabricate a URL; if the supporting analyst report has no link for a claim, drop the specificity rather than guessing.

## Persist output

After producing the markdown, write it to `reports/<TICKER>_<TRADE-DATE>/research-manager.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.
