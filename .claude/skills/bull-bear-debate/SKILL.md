---
name: bull-bear-debate
description: Run a multi-round bull-vs-bear debate over a ticker using the three analyst reports (sentiment, news, company-research) as evidence. Use when the user wants "the bull case vs bear case", "debate this trade", or as part of a full trading workflow after analyst reports are ready.
argument-hint: <ticker> [--rounds N] [--asset-type stock|crypto]
allowed-tools: [Read, Write]
---

# Bull / Bear Researcher Debate

Stage a conversational debate between a **Bull Analyst** and a **Bear Analyst** over `<ticker>`. The debate proceeds for `--rounds N` rounds (default 2 if the orchestrator does not specify). Each round = one Bull turn then one Bear turn.

For `--asset-type stock` use "stock" as the target label; for `--asset-type crypto` use "asset" (and note that the company-research report may be abbreviated since the deep-dive structure assumes a corporate issuer).

## Prerequisites

This skill needs three analyst reports in the conversation context as markdown blobs:

- `sentiment_report` — from [[sentiment-analyst]]
- `news_report` — from [[news-analyst]]
- `company_research_report` — from [[company-research]] (deep institutional-grade coverage of business, management, products, customers, competition, TAM, risks)

**If any report is missing**, run the corresponding analyst skill(s) first — invoke the missing ones in parallel (one Agent subagent per skill, single message with multiple tool calls) before starting the debate. The analyst skills have no further prerequisites.

**Before re-running [[company-research]]** (a 10–30 min, 6,000–10,000-word deep dive), check for a cached report first:

Glob `reports/company/*_<TICKER>/` and pick the most-recently-modified match (see [`output_path.md`](../../../references/output_path.md)). Folders follow `<Company>_<EXCHANGE><TICKER>` (e.g. `AMD_NASDAQ_AMD`, `Tesla_NASDAQ_TSLA`, `安培龙_SZSE002050`). Read the `*_Research_Document.md` / `*_公司研究.md` / `*_研究报告.md` file at the folder root. If its mtime is < 30 days old, use it as `company_research_report`.

Only invoke [[company-research]] fresh if no cache hits. `sentiment_report` and `news_report` are short-lived by design — always run those analyst skills fresh.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- The three analyst reports listed above.
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

Resources to leverage explicitly: sentiment report, news report, company-research report, the prior debate history, and the most recent bear argument.

**Citations:** when you cite a specific data point, headline, post, or filing passage, reproduce the underlying URL from the analyst report's References section as a clickable markdown link inline — e.g. "the [Q1 results press release](https://...) confirms 85% YoY revenue growth" or "as one user put it on [StockTwits](https://stocktwits.com/...) — 'easy $260 from here'". Never invent URLs; if the underlying analyst report has no link for a claim, paraphrase generally instead of citing a specific source.

Prefix the turn with `Bull Analyst:` and append it to `debate_history`.

### Bear turn

You are a Bear Analyst making the case against investing in the {stock|asset}. Present a well-reasoned argument emphasizing risks, challenges, and negative indicators.

Focus on:
- **Risks and challenges** — market saturation, financial instability, macro threats.
- **Competitive weaknesses** — weaker positioning, declining innovation, competitor threats.
- **Negative indicators** — adverse financial data, market trends, recent negative news.
- **Bull counterpoints** — critically analyze the most recent bull argument; expose weaknesses or over-optimistic assumptions.
- **Engagement** — conversational style. Engage with the bull's points directly.

**Citations:** same rule as the Bull turn — reproduce URLs from the analyst reports as inline markdown links whenever you cite specific evidence; never invent URLs.

Prefix the turn with `Bear Analyst:` and append it to `debate_history`.

## Output

Return the complete `debate_history` markdown — alternating `Bull Analyst:` and `Bear Analyst:` paragraphs, in order, for `2 × rounds` turns total.

The orchestrator passes this transcript to the [[research-manager]] skill next.

See [debate methodology](../../../references/debate_methodology.md) for additional guidance on tone and engagement.

## Persist output

After producing the transcript, write it to `<company-folder>/trading/<TRADE-DATE>/bull-bear-debate.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.

Resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md): glob `reports/company/*_<TICKER>/` and pick the most-recently-modified match; fall back to `reports/company/<TICKER>/` if none exists.
