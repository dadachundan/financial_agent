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

**If `risk_debate_history` is missing**, invoke [[risk-debate]] first. That will cascade through [[trader-plan]], [[research-manager]], [[bull-bear-debate]], and the three analyst skills (sentiment-analyst, news-analyst, company-research) as needed.

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

## Resolve stale pending entries (run BEFORE the past_context read)

The track-record feature and the **Key estimate changes** block only work if pending entries ever get resolved — nothing else in the pipeline closes the loop. Check `python scripts/memory_log.py list --pending`; for any pending entry **on this ticker older than ~14 days**:

1. Compute the raw return (yfinance close on the entry's trade date vs the latest close) and the alpha vs SPY over the same window.
2. Write a 3–5 sentence reflection yourself, in conversation — what the call got right/wrong and why (no LLM API, per the project rule) — and save it to a temp file.
3. Close the loop with the sanctioned helper (the log is a markdown file — no DB rules implicated):
   ```bash
   python scripts/memory_log.py resolve --ticker <TICKER> --trade-date <YYYY-MM-DD> \
       --raw-return <X> --alpha-return <Y> --holding-days <N> --reflection-file <tmp>
   ```
Then fetch `past_context` — it will now carry resolved entries the rating can learn from.

## Rating scale (use exactly one)

See [rating taxonomy](../../../references/rating_taxonomy.md).

- **Buy** — Strong conviction to enter or add to position.
- **Overweight** — Favorable outlook; gradually increase exposure.
- **Hold** — Maintain current position; no action needed.
- **Underweight** — Reduce exposure; take partial profits.
- **Sell** — Exit position or avoid entry.

**Conviction intensity (a layer ABOVE the tier).** The 5 tiers state *direction*; a separate qualifier states *intensity* so a 51% Buy and a max-conviction Buy don't look identical. Tag every decision **Conviction: High / Moderate / Low**, and optionally flag a **Top Pick**. Reserve High conviction for calls where the evidence corroborates across the breadth of the analyst debate (bull, bear, and risk analysts converging). This mirrors how sell-side signals intensity outside the discrete rating — GS "Conviction List", Citi "Top Pick", Bernstein "Best Idea", Nomura's numeric "X/5" score.

If `past_context` is non-empty, incorporate its lessons; otherwise rely solely on the current analysis. When `past_context` holds resolved entries for this ticker, surface a one-line **track record** (hit rate / realized-vs-benchmark across resolved calls) the way GS reports the Conviction List's cumulative return vs an equal-weight benchmark, and apply its three lessons: stay with winners that beat early, cut losers fast, earnings drive prices.

## Output schema (produce this markdown exactly)

```markdown
**Rating**: <Buy | Overweight | Hold | Underweight | Sell> · **Conviction**: <High | Moderate | Low> <· Top Pick (optional flag)>

**Executive Summary**: <Concise action plan covering entry strategy, position sizing, and time horizon. Two to four sentences. MUST state the quantified upside/downside skew in one sentence — "~X% to the base-case target, ~Y% downside to the bear case; risk-reward ~Z:1" — and an explicit **invalidation level** (a stop/price that would falsify the thesis). Where the analysts supplied a dividend yield, decompose total expected return as "price appreciation X% + dividend yield D% = total return T%".>

**Investment Thesis**: <Detailed reasoning anchored in specific evidence from the analysts' debate. Every substantive paragraph leads with a bolded mini-section topic sentence (e.g. **Earnings revision:**, **Margin trajectory:**) so the argument is skimmable. Every figure is paired with its driver in the same sentence (never a bare number), and every specific data point, quote, or filing reference carries an inline markdown-link citation — `[Publisher · date](url)`, `[@user · StockTwits · date](url)`, `[10-K Item 7](url)`, etc. — reused from the upstream analyst reports' References sections. Never invent URLs. Incorporate prior lessons from past_context if any; otherwise rely solely on the current analysis.>

**Fundamental health — GF Score** (only when an upstream company-research / initiating-coverage doc supplies one): <the GuruFocus-style five-axis composite, e.g. "78/100 — Likely average; Profitability + Growth strong, GF Value weak (richly priced), Momentum positive". Pulled from the upstream research doc's Section 1B — label `*Internal research:*`, restate the axes/score, cite the underlying metrics, and **never attribute the number to GuruFocus**. Spec: [reference/gf_score.md](reference/gf_score.md). Omit if no upstream GF Score exists — do not compute one from scratch here.>

**Downside risks**: <bulleted list — each risk one clause carrying its own inline citation>
**Upside catalysts**: <bulleted list — each catalyst one clause carrying its own inline citation>

**Price Target** (base case): <number in the instrument's quote currency, written as `multiple × earnings base` with the multiple anchored to the name's own history — e.g. "Rmb127 = 22× 2026E EPS, ~0.5 SD above the 5-yr mean". Cite inline the upstream analyst report that contains both the multiple and the earnings figure. Never a bare number with no derivation (collides with the project numerical-accuracy rule). If upstream gave no PT, state the derivation explicitly rather than inventing one; omit only if no defensible basis exists.>

**Scenario span** (carry all three; the base case equals the Price Target above):

| Scenario | Price target | Multiple × earnings base | % vs current |
|---|---|---|---|
| Bull | <PT> | <e.g. 33× cycle-adjusted EPS> | +<X>% |
| Base | <PT> | <multiple × base> | +<X>% |
| Bear | <PT> | <e.g. 27× trough EPS> | −<Y>% |

<Every cell traces inline to its upstream-analyst source. For cyclicals, use cycle-adjusted / mid-cycle EPS as the base so the span reflects earnings-cycle position, not just the multiple.>

**Key estimate changes** (only when a prior memory-log entry exists for this ticker): <old → new rating/PT with the delta and a one-clause trigger — JPM "Key Changes" style. Pull prior values from past_context.>

**Time Horizon**: <e.g. "12-month price target; 3-6 month holding horizon", with a target date — never open-ended>
```

**Link form — repo-root-relative only.** This report is duplicated verbatim into `memory/trading_memory.md`, so cross-artifact links must be repo-root-relative (`reports/company/<folder>/valuation/…`, `reports/company/<folder>/trading/<date>/sentiment-analyst.md`) or the viewer URL (`http://xs-macbook-air.local:5001/claude-reports/…`) — never directory-relative (`../../valuation/…`, `sentiment-analyst.md`), which dangle from memory/'s location.

**In-repo model artifacts are not external sources.** An in-repo valuation / initiating-coverage doc may anchor the scenario math, but it must be labeled `*Internal research:*`, its derivation restated inline (`multiple × earnings base`), and the external inputs it is built on cited alongside — it never substitutes for an external citation (the analyst's own model is NOT a source).

## Verification log (required — last block of the report)

portfolio-decision is the artifact copied into the memory log and read by the user, so it carries the pipeline's verification gate. End the report with a compact `<details><summary>Verification log — YYYY-MM-DD</summary>…</details>` block listing:

1. **PT derivation recomputed** — multiple × earnings base re-multiplied, and any averaging/midpoint math re-done (a shipped report once called $340 "midway between $331 and $385"; the midpoint is $358).
2. **Every % vs current recomputed** off the dated reference close.
3. **3 headline numbers re-checked** for literal presence in their cited upstream URLs/reports (`✓ string-matches` / `✗ NOT in source — fixed`).
4. **All repo-relative links resolved** with `ls`.

## Further viewing — explainer videos (optional, but default to including)

If the final thesis hinges on a product or mechanism the reader may not be able to picture — a humanoid robot's actuators / harmonic reducers / force sensors, a chip-packaging or lithography step, an unfamiliar revenue model, a derivatives or market-structure construct the call depends on — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* the thing the rating turns on, not just read about it. Default to including them whenever the decision rests on such a concept; omit only when the call is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in (typically beside the Investment Thesis paragraph that introduces it), or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Learning from sell-side institutional research

A study of how GS, Morgan Stanley, UBS, J.P. Morgan, Citi, Bernstein, and Nomura construct portfolio-decision notes. Apply these to sharpen the output above — they reinforce, never relax, the project's numerical-accuracy and citation rules.

- **Three things travel together, non-negotiably (every bank, every name): a rating, a price target *with its derivation*, and a bull/base/bear span.** A rating shipped alone reads as opinion. The schema above now requires all three — keep them together; a PT is `multiple × earnings base`, the multiple anchored to the name's *own* history in SD terms (Citi: "PB 3.09× 2026E, 0.4 SD below mean"), not an absolute number.
- **Lead with one thesis-bearing headline.** Fuse `TICKER + the single strongest thesis clause + rating + PT` into a line that carries the call on its own — GS-style: "Shengyi Tech (600183): CCL pricing uptrend on AI demand; TP Rmb127; Buy, High conviction." Put it as the first line of the Executive Summary.
- **Convert the point rating into a risk-reward skew.** The Citi/MS/UBS habit: never a bare rating — always "~X% to base target, ~Y% to bear, ~Z:1 reward-to-risk." That one sentence is what *justifies* the chosen tier and conviction.
- **Split risks into two symmetric lists** — Downside risks vs Upside catalysts (UBS/MS) — each item one clause with its own citation. Do not bury risks in thesis prose.
- **Decompose total expected return when a dividend exists** (UBS: "price appreciation 20.8% + dividend yield 1.1% = total return 21.9%"), and name an explicit invalidation level — make the Executive Summary's "key risk levels" a concrete number, not prose.
- **"Free call option" framing** for convex optionality the market isn't paying for (GS S-Oil petrochem recovery) — a clean way to label asymmetric upside in the thesis.
- **House voice:** decisive single-clause verdicts ("Maintain Buy", "Top Pick") never hedged (reinforces the existing *don't-default-to-Hold* rule); bolded mini-section topic sentences as the skeleton; every figure paired with its driver in the same sentence; time-bound everything (12-mo PT + horizon + target date).

## Persist output

Write the markdown to `<company-folder>/trading/<TRADE-DATE>/portfolio-decision.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.

## Memory write

After the file is written, append it to the decision log (pass the resolved file path to `--decision-file`):

```bash
python scripts/memory_log.py append \
    --ticker <TICKER> \
    --trade-date <YYYY-MM-DD> \
    --decision-file <company-folder>/trading/<YYYY-MM-DD>/portfolio-decision.md
```

This creates a `pending` entry that a later reflection job can update with realized returns. See [memory format](../../../references/memory_format.md) for schema details.
