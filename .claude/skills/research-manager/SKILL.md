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

**Anchor the tier to the base-case target, not debate sentiment alone** (the sell-side PT-vs-current gate): Buy/Overweight when the base-case target implies meaningful upside *and* the bull pillars outweigh the bear risks; Underweight/Sell when the target implies downside *or* the bear thesis dominates; Hold only when base-case upside is small *and* risk is genuinely two-sided. State the call as a **direction** relative to the prior round's rating (Initiate / Upgrade X→Y / Downgrade X→Y / Maintain) — the research-manager runs in a multi-round pipeline, so the prior rating is available; label it `Initiate` when none exists.

## Output schema (produce this markdown exactly)

```markdown
**Recommendation**: <Buy | Overweight | Hold | Underweight | Sell>

**Rating Action**: <Initiate | Upgrade X→Y | Downgrade X→Y | Maintain> — <1–2 dated catalysts that would confirm or break the thesis: investor day, product ramp, earnings, project COD, etc.>

**Price Target & Scenario Band**:
- Base: <12-month target> vs current <price> = <±% upside/downside>. Valuation basis: <method + parameters, e.g. SOTP; 28x mid-cycle EPS; DCF WACC 9.7% / g 2%; ~1x P/NAV vs peers 1.5–2x>.
- Bull: <target> — <one-sentence driver that produces it>.
- Bear: <target> — <one-sentence driver that produces it>.

**Rationale** (2–3 titled pillars):
1. **<Pillar name>** — <one-line claim + its strongest cited evidence from the debate>.
2. **<Pillar name>** — <…>.
3. **<Pillar name>** — <…>.

**Strategic Actions**: <Concrete steps for the trader to implement the recommendation, including position-sizing guidance consistent with the rating.>

**Key Risks**:
- *Upside risks*: <bulleted list — carry the bull case forward even on a Sell>.
- *Downside risks*: <bulleted list — carry the bear case forward even on a Buy>.
```

This block becomes `investment_plan` for the downstream [[trader-plan]] and [[portfolio-decision]] skills.

**Citations:** carry over the citations from the upstream analyst reports (news-analyst, sentiment-analyst, company-research) verbatim — each report ends with a References section listing the URLs the debate quoted. Reuse those URLs inline as clickable markdown links whenever you reference a specific fact. Never fabricate a URL; if the supporting analyst report has no link for a claim, drop the specificity rather than guessing.

## Learning from sell-side institutional research

The fixed institutional rating note is a 5-block skeleton — **(1) rating + PT + %-upside headline, (2) titled thesis pillars, (3) valuation/methodology, (4) dated catalysts, (5) symmetric upside/downside risks** — assembled here from the closest bank analogs. Apply these surgically; they sharpen the schema above without loosening any citation, numerical-accuracy, or language rule.

- **Lead with the call, then the support (Morgan Stanley "Three Actionable Ideas" / GS "Conviction List" compression).** Rating + base-case PT + % upside + the rating *direction* belong in the first lines, before any reasoning. State the direction explicitly (`Downgrade Overweight→Equal-weight`), never just the new end-state — the reader needs to see what moved.

- **Quantify the rating with a Bull/Base/Bear PT band (Morgan Stanley "Risk Reward Update").** This is the missing quantitative backbone and it maps directly onto the bull/bear debate the skill already consumes. Each leg is a one-line valuation expression yielding a number and a % vs current — MS SanDisk flexes *both* the multiple and the EPS for a cyclical (bear 25x × $44 = $1,100 / base 28x × $62.5 = $1,750 / bull 31x × $85 = $2,635). For crypto / no-clean-earnings names, express the band in the debate's own driver thresholds (e.g. flows, hashrate, regulatory outcome) rather than an EPS multiple. **Constraint: every number in the band must trace inline to a source the upstream analyst reports actually cite. If the debate provides no basis for a numeric target, state the band qualitatively and say so — never fabricate a multiple.**

- **Compress the rationale into 2–3 named pillars (J.P. Morgan rating-change / Bernstein initiation).** Each pillar is a titled, numbered mini-thesis — one claim + its strongest cited evidence — scannable in ten seconds (cf. Tesla's *vertical-integration moat / Robotaxi / Optimus*), not a flowing paragraph where a claim can hide. Keep the existing inline-citation rule on every data point.

- **Name the valuation basis inline (UBS / HSBC / GS PT-move discipline).** One short sentence: the method *and* its key parameters, with the multiple's position vs the stock's own history where available — UBS Accton "NT$3,400, 27x 2027–28E P/E, top of the stock's historical 10–31x range"; GS Lundin "C$48.2, ~1x P/NAV vs peers 1.5–2x". This makes the target auditable in a glance. **Constraint: the analyst's own model is NOT a source — cite the external inputs (filing segment data + the multiple from the company-research report's `*Analyst view:*` section), never `(our model)`.** The house base-case PT here is yours, stated vs current price (today). But **any *borrowed* PT carried over from the upstream `*Analyst view:*` block must show the stock's price on that note's date + the upside it fixed** (`UBS NT$3,400 vs NT$2,780 @ 2026-05-18 → +22%`), not today's spot — the report-date price comes from `stock_price_target_db` (`report_date_price` / `upside_pct`, at `/pt`).

- **Tie the call to dated catalysts (J.P. Morgan "Positive Catalyst Watch" / Bernstein dated-catalyst list).** Name 1–2 specific upcoming events (investor day, ramp, project COD, earnings) that would confirm or break the thesis — this converts a static rating into a time-bound, falsifiable call and is the home for "what would change my mind."

- **Carry a symmetric risk block (universal MS / UBS / Bernstein / HSBC convention).** Terse bulleted *Upside risks* / *Downside risks*, never a hedging paragraph — so the losing side of the debate survives explicitly: an upside-risk list even on a Sell, a downside-risk list even on a Buy. Each risk reuses a debate citation.

## Persist output

Write the markdown to `<company-folder>/trading/<TRADE-DATE>/research-manager.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
