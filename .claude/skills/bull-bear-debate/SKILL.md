---
name: bull-bear-debate
description: Run a multi-round bull-vs-bear debate over a ticker using the four analyst reports (market, sentiment, news, fundamentals) as evidence. Use when the user wants "the bull case vs bear case", "debate this trade", or as part of a full trading workflow after analyst reports are ready.
argument-hint: <ticker> [--rounds N] [--asset-type stock|crypto]
allowed-tools: [Read, Write]
---

# Bull / Bear Researcher Debate

Stage a conversational debate between a **Bull Analyst** and a **Bear Analyst** over `<ticker>`. The debate proceeds for `--rounds N` rounds (default 2 if the orchestrator does not specify). Each round = one Bull turn then one Bear turn.

For `--asset-type stock` use "stock" as the target label; for `--asset-type crypto` use "asset" (and note that the fundamentals report may be incomplete).

## Prerequisites

This skill needs four analyst reports in the conversation context as markdown blobs:

- `market_report` — from [[market-analyst]]
- `sentiment_report` — from [[sentiment-analyst]]
- `news_report` — from [[news-analyst]]
- `fundamentals_report` — from [[fundamentals-analyst]]

**If any report is missing**, run the corresponding analyst skill(s) first — invoke the missing ones in parallel (one Agent subagent per skill, single message with multiple tool calls) before starting the debate. The analyst skills have no further prerequisites.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- The four analyst reports listed above.
- `debate_history` — running transcript, empty on round 1.
- `--rounds N` — debate length (default 2).
- `--asset-type` — `stock` or `crypto`.

## Per-turn instructions

### Bull turn

You are a Bull Analyst advocating for investing in the {stock|asset}. Build a strong, evidence-based case emphasizing growth potential, competitive advantages, and positive market indicators. Address concerns and counter bearish arguments effectively.

Focus on:
- **Growth potential** — market opportunities, revenue projections, scalability.
- **Competitive advantages** — unique products, branding, dominant positioning.
- **Positive indicators** — financial health, industry trends, recent positive news.
- **Bear counterpoints** — critically analyze the most recent bear argument with specific data and sound reasoning; address concerns thoroughly and show why the bull perspective holds stronger merit.
- **Engagement** — conversational style. Engage directly with the bear's points; debate rather than just list data.

Resources to leverage explicitly: market report, sentiment report, news report, fundamentals report, the prior debate history, and the most recent bear argument.

Prefix the turn with `Bull Analyst:` and append it to `debate_history`.

### Bear turn

You are a Bear Analyst making the case against investing in the {stock|asset}. Present a well-reasoned argument emphasizing risks, challenges, and negative indicators.

Focus on:
- **Risks and challenges** — market saturation, financial instability, macro threats.
- **Competitive weaknesses** — weaker positioning, declining innovation, competitor threats.
- **Negative indicators** — adverse financial data, market trends, recent negative news.
- **Bull counterpoints** — critically analyze the most recent bull argument; expose weaknesses or over-optimistic assumptions.
- **Engagement** — conversational style. Engage with the bull's points directly.

Prefix the turn with `Bear Analyst:` and append it to `debate_history`.

## Output

Return the complete `debate_history` markdown — alternating `Bull Analyst:` and `Bear Analyst:` paragraphs, in order, for `2 × rounds` turns total.

The orchestrator passes this transcript to the [[research-manager]] skill next.

See [debate methodology](../../../references/debate_methodology.md) for additional guidance on tone and engagement.

## Persist output

After producing the transcript, write it to `reports/<TICKER>_<TRADE-DATE>/bull-bear-debate.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.
