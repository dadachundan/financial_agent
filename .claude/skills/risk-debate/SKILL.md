---
name: risk-debate
description: Stage a three-way risk debate (Aggressive / Conservative / Neutral analysts) over a Trader's transaction proposal. Use after the trader-plan skill, or as part of a full trading workflow.
argument-hint: [--rounds N]
allowed-tools: [Read, Write]
---

# Risk Management Debate

Stage a three-way debate among an **Aggressive**, **Conservative**, and **Neutral** Risk Analyst over the Trader's transaction proposal. The debate runs for `--rounds N` rounds (default 1). Each round = one Aggressive turn, one Conservative turn, one Neutral turn (in that order).

## Learning from sell-side institutional research

The bank analog for this report type is the **per-ticker risk-reward note** (Morgan Stanley *Risk Reward Update*) plus the **strategist scenario note** (Citi FX risk-sentiment ladder, UBS *Deal or No Deal* scenario trades, Goldman same-facts/different-input relativity). The transferable machinery — apply it on top of the existing conversational voice, not instead of it:

- **Mirror MS *Risk Reward Update*: every voice lands a quantified scenario number, not just a named risk.** MS pins Bull / Base / Bear price targets and shows the math (SanDisk: Bull 31× × cycle-EPS $85 = $2,635 / Base 28× × $62.50 = $1,750 / Bear 25× × $44 = $1,100). The debate must produce the same triplet — Aggressive owns Bull, Conservative owns Bear, Neutral owns Base — each decomposed driver-first (`Bear $185 = 20× × $9.24 EPS on low-single-digit organic growth`). See **## Scenario quantification (required)** below.
- **Operationalize GS same-facts/different-input relativity: the three voices disagree by *weighting*, not by rhetoric.** GS runs identical facts through hi/lo inputs ($3,500 vs $5,500/oz gold) and ranks the stock under each. Here, each analyst states rough odds on base/bull/bear and the Neutral turn reconciles to a house-weighted lean — a falsifiable fork (which input scenario you weight), not a tonal difference. See **## Divergent weighting, shared facts** below.
- **Borrow the Citi green→yellow→red trigger ladder for the Neutral turn.** Citi grades risk sentiment with *named, checkable* escalation triggers (POLLS composite at 18, put/call at a 10yr low, single-stock-vs-index vol dispersion >2.5×) and an explicit "what flips us yellow→red" list. The Neutral analyst must produce this ladder — what specifically escalates the firm from neutral to bearish, each threshold tied to a data point and (where possible) a date.
- **Close like a strategist, not a worrier: the Conservative turn must express downside concretely.** UBS maps each scenario to a trade with carry/duration/convexity called out; Citi pairs each read with a hedge (JPY strangle, SEK/NZD puts); GS Asia overlays price a zero-cost put-spread collar on named concentration risk (TWSE 41% in TSMC). The Conservative analyst must propose at least one concrete mitigation — tighter size, an explicit stop off the trader-plan, a pair trade, or a collar — never abstract "be cautious."
- **Anchor against the crowd when an upstream report supplies it (MS consensus overlay, Citi POLLS).** MS overlays the sell-side consensus PT distribution and rating split (e.g. 88% OW / 0% EW / 13% UW) so the house view is positioned vs consensus. Pull positioning / consensus / option-market reads (hedge-fund net exposure, put/call percentile, VIX term slope) *only* from what an upstream report actually contains, with inline deep-URL citations — never fabricate a consensus or positioning number. **When you quote a *specific* borrowed PT (the consensus mean target or a named broker's PT), pair it with the stock's price on that note's date + the implied upside** (`Street mean $288 vs $232 @ 2026-06-03 → +24%`), not today's close — the report-date price is what makes the borrowed call legible (`report_date_price` / `upside_pct` from `stock_price_target_db`, at `/pt`). The debate's own Bull/Base/Bear targets stay stated vs current price.

**Calibrate to percentiles, not adjectives** (`IG spreads at the 2nd percentile of 10yr history` beats `spreads are very tight`), and **name the single biggest risk as the swing factor** rather than leaving all risks equally weighted — both are universal in the analogs. Every quantified claim still obeys the project numerical-accuracy rule: it must inline-trace to a source (trader-plan target, company-research valuation, or a filing) that *literally contains the number* — no analyst-invented figures.

## Divergent weighting, shared facts

The three voices work from the **same** evidence (trader plan + three analyst reports) and disagree by **weighting different scenarios**, not by selectively citing facts. Each analyst states rough odds on the base/bull/bear set in their turn — e.g. Aggressive `50/40/10` (base/bull/bear), Conservative `35/15/50`, Neutral the house calibration. This turns three monologues into a real debate: the fork is auditable (which scenario you weight), not vibes.

## Scenario quantification (required)

Each round must produce a Bull / Base / Bear triplet, with one number owned by each voice and decomposed **driver-first**:

- **Bull (Aggressive):** target = multiple × bull-scenario EPS, or implied move vs the trader-plan entry/stop. Open with the driver, then the number: `Bull $2,635 = 31× × cycle-EPS $85 on a memory up-cycle`.
- **Base (Neutral):** the house base case — target multiple × base EPS, or % EPS delta vs base = 0 by construction.
- **Bear (Conservative):** de-rate / earnings-cut path — `Bear $185 = 20× × $9.24 EPS on low-single-digit organic growth`.

Every number must inline-trace to the upstream report that literally contains it (trader-plan target/stop, company-research valuation multiple or EPS, or a filing), per the numerical-accuracy rule — no analyst-invented figures. If the upstream reports don't supply a base for a given number, say so and frame the scenario in the terms the sources *do* support (e.g. "up sharply vs the $X entry" rather than a fabricated target).

## Prerequisites

This skill needs the trader's proposal plus the three analyst reports:

- `trader_investment_plan` — from [[trader-plan]]
- `sentiment_report` / `news_report` / `company_research_report` — from the three analyst skills

**If `trader_investment_plan` is missing**, invoke [[trader-plan]] first; that will cascade up through [[research-manager]] and [[bull-bear-debate]] as needed (and the analyst reports along the way).

**If only the analyst reports are missing** (e.g. you have a trader plan from a separate workflow), invoke the missing analyst skills in parallel.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- `trader_investment_plan` — the [[trader-plan]] proposal.
- Three analyst reports: `sentiment_report`, `news_report`, `company_research_report`.
- `risk_debate_history` — running transcript, empty on round 1.
- `--rounds N` — debate length (default 1).

## Per-turn instructions

**Multi-round anchor (`--rounds N` ≥ 2):** open each round after the first with a one-line "What's changed since last round" note — which assumption or data point moved the scenario numbers — mirroring the MS *Risk Reward Update* "WHAT'S CHANGED" From→To block. Round 2+ must advance the debate (revised odds, a moved scenario target, a newly-tripped ladder trigger), not restate round 1.

### Aggressive Risk Analyst

As the Aggressive Risk Analyst, your role is to actively champion high-reward, high-risk opportunities, emphasizing bold strategies and competitive advantages. When evaluating the trader's plan, focus intently on the potential upside, growth potential, and innovative benefits — even when these come with elevated risk. Use the market data and sentiment analysis to strengthen arguments and challenge opposing views. Respond directly to each point made by the conservative and neutral analysts with data-driven rebuttals and persuasive reasoning. Highlight where their caution might miss critical opportunities or where their assumptions may be overly conservative.

**Own the Bull number.** Land one quantified Bull-case scenario target, decomposed driver-first (`Bull $X = multiple × bull-EPS …`, or implied move vs the trader-plan entry/stop), and state your rough odds (e.g. `50/40/10` base/bull/bear) — per **## Scenario quantification (required)**. Calibrate with percentiles, not adjectives; land at least one quantified claim that inline-traces to a source containing the number.

Argue conversationally, as if speaking — no special formatting. Prefix the turn with `Aggressive Analyst:` and append to `risk_debate_history`.

**Citations:** when citing specific evidence from any of the upstream reports, reproduce the URL from that report's References section as a clickable markdown link inline. Never invent URLs.

### Conservative Risk Analyst

As the Conservative Risk Analyst, your primary objective is to protect assets, minimize volatility, and ensure steady, reliable growth. Prioritize stability, security, and risk mitigation. Critically examine high-risk elements; point out where the trader's plan may expose the firm to undue risk and where more cautious alternatives could secure long-term gains. Counter the Aggressive and Neutral analysts' arguments, highlighting where their views may overlook threats or fail to prioritize sustainability.

**Own the Bear number and propose one concrete mitigation.** Land one quantified Bear-case target, decomposed driver-first (`Bear $X = de-rated multiple × cut-EPS …`), and state your rough odds (e.g. `35/15/50` base/bull/bear). Then propose **at least one concrete hedge / mitigation structure** — tighter size, an explicit stop off the trader-plan, a pair trade, or a collar (model on UBS scenario trades with carry/convexity, Citi's JPY strangle / SEK-NZD puts, GS's zero-cost put-spread collar on named concentration risk) — never abstract "be cautious." Quantified claims trace to a source per the numerical-accuracy rule.

Argue conversationally. Prefix `Conservative Analyst:`. Same citation rule as the Aggressive turn — preserve URLs from the upstream reports as inline markdown links; never invent.

### Neutral Risk Analyst

As the Neutral Risk Analyst, provide a balanced perspective, weighing both the potential benefits and risks of the trader's plan. Prioritize a well-rounded approach — evaluate upsides and downsides while factoring in broader market trends, potential economic shifts, and diversification strategies. Challenge both the Aggressive and Conservative analysts: point out where each may be overly optimistic or overly cautious. Advocate for a moderate, sustainable strategy.

**Own the Base number, build the trigger ladder, reconcile the odds.** Land the house Base-case target (decomposed driver-first per **## Scenario quantification (required)**) and reconcile the three voices' rough odds into a single house-weighted lean. Then deliver a **Risk ladder (green / yellow / red)**: a list of *named, checkable* signals that escalate the firm from neutral toward bearish, each tied to a specific data point and (where possible) a date — model on Citi's green→yellow→red (e.g. positioning composite at a threshold, put/call at a multi-year extreme, vol dispersion >2.5×), including an explicit "what flips us yellow→red." Where an upstream report supplies positioning / consensus / option-market context (house view vs consensus PT and rating split, hedge-fund net exposure, put/call percentile, VIX term slope), use it to calibrate — cite only what a report actually contains, with inline deep-URL citations; never fabricate a consensus or positioning number.

Argue conversationally. Prefix `Neutral Analyst:`. Same citation rule — reuse URLs from upstream reports; never invent.

## Output

Return the complete `risk_debate_history` markdown — `Aggressive Analyst:` / `Conservative Analyst:` / `Neutral Analyst:` paragraphs, in order, for `3 × rounds` turns total.

After the turns, append a **Debate verdict** block (mirrors MS tagging one downside bullet as "the largest risk"):

- **Probability-weighted lean** — the house base/bull/bear odds and the resulting Buy/Hold/Sell tilt.
- **Biggest swing factor** — the single risk that most moves the outcome, named explicitly (not all risks weighted equally).
- **Two separate lists, never merged** — *Upside catalysts* and *Downside risks* kept apart, each item dated where a catalyst resolves it (investor day, earnings, policy window).

The orchestrator passes this transcript to [[portfolio-decision]] next.

## Persist output

Write the transcript to `<company-folder>/trading/<TRADE-DATE>/risk-debate.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
