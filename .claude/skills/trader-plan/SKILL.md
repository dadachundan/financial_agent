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

Pull the **dated catalyst** (event + date + expected estimate delta) and the **Bull/Base/Bear scenario targets** from the upstream research-manager / analyst reports. If they are absent there, mine the local broker library `db/zsxq.db` (~6,900 sell-side PDFs) for a sell-side scenario set, catalyst date, and conviction rank — label anything borrowed from it `*Analyst view:*` and keep it out of any primary-filing citation (per [company-research citation standard](../company-research/references/citations.md)). **Never invent a catalyst date, a scenario target, or a current price** — if no source supplies one, say so and fall back to the "No dated catalyst" / single-point wording.

Allowed conviction tags for the `**Action**` line: `high conviction`, `catalyst-driven`, `valuation`, or `on Positive Catalyst Watch into <date>`.

## Output schema (produce this markdown exactly)

```markdown
**Action**: <Buy | Hold | Sell> — <conviction tag: "high conviction" | "catalyst-driven" | "valuation" | "on Positive Catalyst Watch into <date>">

**Catalyst**: <the specific near-term event — "QCOM Investor Day (June 24)" — its date/window, the expected fundamental outcome (e.g. "DC revenue-target raise → consensus EPS up"), and a one-word landing probability (high | medium | low). If none exists, write exactly: "No dated catalyst — thesis is valuation/positioning-driven.">

**Risk-Reward** (off a dated Current Price — never a bare target):
- **Current Price**: <number, as of YYYY-MM-DD> · 52-week range <low>–<high>
- **Bull Target**: <number> (<+X% off current>) — <valuation basis, e.g. "28x cycle-EPS $62.50">
- **Base Target**: <number> (<±X% off current>) — <valuation basis>
- **Bear Target**: <number> (<−X% off current>) — <valuation basis; this level defines the Stop Loss>
- **Asymmetry**: <one line, e.g. "+22% to bull vs −11% to bear = ~2:1 skew">

**Reasoning**: <3–6 sentences in a fixed three-part structure: (1) the catalyst-to-thesis link — what dated event moves estimates/price, and whether it's already priced; (2) where this differs from consensus / what the edge is; (3) the bear-case level that defines the stop. Every scenario level and catalyst number carries an inline markdown-link citation reused from the upstream analyst / research-manager report — never invent one, and each number must string-match its cited source per the project numerical-accuracy rule.>

**Upside risks** (利好):
- <2–3 labeled bullets, each with an inline citation>

**Downside risks** (利空):
- <2–3 labeled bullets, each with an inline citation — give the bear case equal billing>

**Entry Price**: <optional — number in the instrument's quote currency, or omit the line>

**Stop Loss**: <the Bear Target level above (justified by the bear case), or omit the line>

**Position Sizing**: <optional — e.g. "5% of portfolio", or omit the line>

FINAL TRANSACTION PROPOSAL: **<BUY | HOLD | SELL>**
```

The trailing `FINAL TRANSACTION PROPOSAL:` line is required for backward compatibility with downstream consumers that grep for it. The `**Action**` conviction tag is additive — keep the trailing line a bare BUY/HOLD/SELL.

Pass the markdown forward as `trader_investment_plan` to [[risk-debate]].

## Learning from sell-side institutional research

The bare Buy/Hold/Sell + flat entry/stop is a desk shorthand; sell-side tactical notes carry a fuller anatomy that the schema above borrows. Apply these named house patterns:

- **Mirror Morgan Stanley "Risk Reward Update": three named scenarios, each with its own target and a labeled % move off a dated current price.** Bull/Base/Bear is the spine — not a single point estimate. Show each target's valuation basis (e.g. `28x cycle-EPS` or DCF CoE/perpetual-growth) so it is reconstructible, and close with an explicit asymmetry line (`+48.7% to bull vs −37.7% to bear`). The **Stop Loss is the bear-case level**, justified — not a round-number guess; the take-profit is the bull/base level.

- **Mirror J.P. Morgan "Positive Catalyst Watch": the catalyst is a first-class, DATED field, kept separate from the standing rating.** Name the event, its date/window, the expected fundamental outcome, and a one-word landing probability (`high/medium/low`). Write events scannably as `Event (Date, importance)` — `Investor Day (June 24, high)`. A rating can stay Hold while the name is "on Positive Catalyst Watch into <date>".

- **Mirror the universal "利好 / 利空" close: symmetric labeled risk bullets, bear case at equal billing.** Every Risk Reward Update, Catalyst Watch, and Conviction-List entry ends with explicit upside-risks AND downside-risks (2–3 each), not a single "risks" afterthought.

- **Grade conviction, never ship it bare** (GS "Conviction List", Citi "Top Pick", Bernstein "Best Idea", MS "Three Actionable Ideas"). One crisp actionable line — rating + the single catalyst + the target — before any deeper rationale, and a named conviction tag rather than a binary Buy/Hold/Sell.

- **Anchor every number to a reference** (the desk standard): a target price is always shown with its `%up/downside` off a dated current price and against the 52-week range; consensus context (rating/PT distribution, the bank's estimate-vs-consensus delta) shows where the trade is differentiated vs crowded. A bare target with no spot anchor is a non-call.

### Basket mode (optional — future multi-ticker runs)

The current pipeline is single-ticker. If `trader-plan` is ever run across a basket, add a **strategy-scorecard** convention so the process is accountable over time — mirror MS "Three Actionable Ideas" (cumulative/excess return, avg holding-period return, **hit rate** = % positive / % beat benchmark) and GS "Conviction List Directors' Cut" (dated add/remove churn with the reason, e.g. "added May 3, removed May 25 on price underperformance"). Each basket entry still carries its own %upside-to-target.

## Persist output

Write the markdown to `<company-folder>/trading/<TRADE-DATE>/trader-plan.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
