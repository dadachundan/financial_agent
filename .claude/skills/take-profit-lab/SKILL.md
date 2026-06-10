---
name: take-profit-lab
description: Quantify exit discipline for a ticker — hold forever, tier out at milestones, trailing stops, or volatility-aware exits — using a historical-entry-cohort backtest on yfinance-adjusted prices. Produces a 3,000–5,000 word markdown report with strategy-comparison table + 6–10 charts + concrete sell levels from the user's cost basis when supplied. Use when the user asks "should I take profit on X?", "when do I sell X?", "is X a buy-and-hold or a tier-out?", "trailing stop on X", or anything in the exit-discipline / take-profit family. Complements `trader-plan` (entry) and `portfolio-decision` (final rating) — this skill specifically owns the *exit* question.
---

# Take-Profit Lab

Quantify exit discipline for a single ticker (stock or ETF). The question this skill answers is **not** "buy or sell today?" — that's [[trader-plan]] / [[portfolio-decision]]. The question is: **once you own this, what is the rule for getting out?**

Adapted from the [LLMQuant take-profit-lab workflow](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-equities/workflows/take-profit-lab.md) (MIT), re-pointed at this project's existing data sources (yfinance + `indicators.db` + `market_cap_cache.db`).

## When to use

The user says any of:

- "Should I take profit on NVDA?"
- "When do I sell TSLA?"
- "Is META a buy-and-hold or do I tier out?"
- "What's the trailing stop on this?"
- "Hold or harvest? — analyze QQQ" (works for ETFs too)
- "Take-profit analysis for X"
- "Run a hold-vs-tier-out comparison on X"

The skill produces an **Exit Verdict** (hold / tier / strict-exit / avoid-long-hold) backed by a historical backtest across multiple exit strategies and translated into concrete sell levels.

## When NOT to use

- The user wants an entry recommendation — use [[trader-plan]].
- The user wants a 5-tier Buy/Overweight/Hold rating — use [[portfolio-decision]] (which sits at the end of the [[trading-analysis]] pipeline).
- The user wants long-form fundamentals coverage — use [[company-research]].
- The ticker is illiquid (median 30-day $ volume < $1M) or has < 3 years of clean adjusted-price history — flag it, decline gracefully. The backtest needs path-dependency signal that short history can't provide.
- The asset is a leveraged ETF (TQQQ, SOXL, SQQQ, etc.) and the user hasn't acknowledged volatility decay — see Guardrails below.

## Core methodology

The exit-rule landscape is searched over five strategy families:

| Strategy | Rule | What it optimizes for |
|---|---|---|
| **Hold** | Never sell. | Maximum CAGR if drift dominates; baseline for everything else. |
| **Tiered exit** | Sell 25/50/75% of position at +50% / +100% / +150% gains from entry. | Lock in profit while keeping skin in the game; capture multiple legs. |
| **Strict exit** | Sell 100% at a target gain (+50%, +100%, or +200%). | Booking a fixed multiple without re-entry; the "milestone" rule. |
| **Trailing stop** | Sell 100% when price drops ≥X% from peak since entry (X ∈ {15, 20, 25, 30}). | Capture the trend, exit on regime change; behavioral discipline. |
| **Volatility-aware** | Trailing stop = `k × ATR` for k ∈ {2, 3, 4}, computed on a 30-day window. | Wider stops in noisy regimes, tighter in calm regimes. |

For each strategy, run a **historical entry-cohort backtest**: assume entry on every trading day in the available history (or last 10 years, whichever is shorter), apply the rule, and aggregate outcomes across the entry-cohort distribution.

### Headline metrics per strategy

- **CAGR (median across entry cohorts)** — the expected long-run return per rule.
- **Max drawdown** — worst peak-to-trough loss any cohort lived through.
- **Win rate** — % of cohorts that exited at a gain.
- **Rollercoaster rate** — % of entry cohorts that reached ≥+50% gain at some point AND then gave back ≥50% of peak profit before exit. **This is the path-pain metric the skill exists to surface** — hold-CAGR alone hides the fact that 30% of cohorts had to ride a peak gain all the way back to flat before exit.
- **Tail (5th percentile and 95th percentile)** — bottom-tail and top-tail cohort outcomes, not just the median.
- **Active-exit improvement vs hold** — `(strategy CAGR − hold CAGR) / |hold CAGR|`, expressed as a percentage. A negative number means the rule costs you return; a positive number means it pays.

### Exit-verdict bands

The headline output. Map the aggregate of the five strategy families to one of four states:

- **Holdable** — Hold strategy dominates: rollercoaster rate < 15%, hold-CAGR within 1 pt of best active rule, max drawdown < 35%. Action: buy-and-hold; review annually.
- **Tier-preferred** — Tiered or strict exit beats hold on at least one of (CAGR, rollercoaster rate, Sharpe). The drift is real but path pain is too. Action: pre-commit to tier levels at entry.
- **Trailing-stop preferred** — Trailing-stop / vol-aware strategies dominate hold on max drawdown by ≥10 pts at no cost to CAGR. The asset has trend-followable regime shifts. Action: trailing stop at the best-fit width; widen if cost basis allows.
- **Structurally unsuitable for buy-and-hold** — Hold strategy's tail outcomes include >50% drawdowns the 95th-percentile cohort never recovers from, or rollercoaster rate > 40%. Action: short-leash exit or avoid as a long-hold position.

## Learning from sell-side institutional research

The trim decision here is reached via a **price-path backtest, not a forward-EPS/DCF model** — so this skill must never print a fundamental price target, peer-multiple, or scenario EPS it didn't compute, and must punt "is the run justified by fundamentals?" to [[company-research]]. But the *framing* the desks use to communicate a trim is directly transferable. Borrow the packaging, keep the backtest as the only source of edge.

- **Risk-Reward Ladder — mirror the Morgan Stanley "Risk Reward Update."** MS never reports a single number; it reports a Bull / Base / Bear ladder, each carrying an explicit signed % move from spot (Base −3.5%, Bull +48.7%, Bear −37.7%). Reframe the existing entry-cohort distribution the same way using **only backtest outputs**: **Base** = median cohort outcome path, **Bull** = 75th/95th-percentile path, **Bear** = 5th-percentile / max-drawdown path. Convert each to a price from the current price and a signed % move. This is a **mandatory output block** — present it as a small table AND as a chart (current-price dot + three horizontal scenario lines, mirroring the MS Risk-Reward chart; add it to the Step 3 inventory). Every number traces to the strategies CSV; the chart carries the standard in-image `Source: yfinance (adjusted, <date>); backtest oneoff/take_profit_<TICKER>.py` annotation. **No fabricated forward-EPS or DCF anchor** — the ladder is the cohort distribution, restated in the reader's native "upside left vs downside to give back."

- **Performance-since-entry vs a benchmark — mirror the GS single-stock downgrade trim trigger.** GS de-rates by anchoring to a dated entry and attributing performance ("since being added to our Buy list Aug 6 2025, the share price has been flat vs CSI300 +18%") — the trim is about *price-path skew at the current level*, not a thesis break. When a **cost basis is supplied**, compute return-since-entry vs a benchmark over the same window (SPY for US, QQQ for tech-heavy, the relevant HK/A-share index) and locate that run-up in the percentile distribution of this ticker's historical extensions. Frame the trigger as GS/Bernstein do: *"you are up X% since $<basis> (vs SPY +Y%); this extension sits in the Zth percentile of historical run-ups, and from comparable extensions the median cohort gave back W% before exit — hence take some off, keep a runner."* Pure yfinance math, no fundamental model, no DB writes. Add a **"Performance vs benchmark since entry"** line to the Data Used manifest.

- **WHAT'S CHANGED delta box — mirror the MS one-line reason-for-change.** MS leads every update with old→new ("Following 1Q26 results, we cut 2026-30 EPS by 2-4%… PT and scenario values fall 3-4%"). The skill's update-in-place rule currently overwrites silently. **Require a "WHAT'S CHANGED since last run" delta box as the first block** of every refresh: prior verdict → current verdict, prior sell levels → current, prior as-of realized vol → current, plus a one-line reason-for-change naming the single thing that moved the verdict. On the first run, state `initiation — no prior`. Keep the de-rate decision visibly separate from the thesis: state explicitly whether the verdict moved **on price-path alone** (the rule changed because the price ran, not because the company broke).

- **Trim-not-exit verb register — mirror the GS/Bernstein/UBS disciplined-trim ladder.** The banks trim *into strength without calling a top* ("profit-taking pressure," "getting to a more balanced risk-reward") rather than firing a "sell signal." Map each exit-verdict band to a discrete named action verb the reader executes, pairing upside-left with downside-give-back symmetrically — e.g. Tier-preferred → *"TRIM INTO STRENGTH, KEEP A RUNNER: take 25/50/75% at $__/$__/$__; you keep ~X% upside to the 95th-pct path while cutting the median give-back from W% to V%."* Match the desks' humility — never call a top.

- **Symmetric Upside/Downside risk lists — mirror the universal bank closing.** Every note across all 10 banks pairs quantified upside-to-target with an explicit, *named* downside-risks list; a one-sided risk section is never acceptable. The current Failure modes arm is one-sided (what invalidates the verdict). Add an explicit **"Upside risk to taking profit"** arm — what you forgo if you trim and the drift continues, quantified as the 95th-pct cohort's forgone CAGR — alongside the existing downside / regime-mismatch arm.

- **Extension / richness percentile — mirror the Bernstein "near a 5-year P/E high" anchor.** Bernstein/UBS/MS never write "looks expensive"; richness is always quantified against a reference ("X turns vs peers at Y," "top of its 5-year band"). This skill has no fundamental valuation input, so anchor richness to the ticker's **own price-path history**: where the current price sits vs its history of (a) distance above the 200-day MA and (b) trailing drawdown-from-peak, each expressed as a **percentile**. Use it as the "how stretched" number so any "stretched" claim carries a figure and a reference (reinforcing the project's numerical-accuracy rule). Fold the optional `indicators.db` regime read (VIX / HY-OAS) into the same paragraph so regime context sits alongside the extension percentile.

## Data sources (project-specific)

### Required

- **yfinance** (`pip install yfinance` — assumed already available) for **adjusted-for-dividends-and-splits** OHLCV history. Always use `auto_adjust=True` so dividends and splits are baked in — unadjusted prices give wrong backtest results. Look-back: 10 years or full available history, whichever is shorter.
- **Realized volatility** — compute inline from yfinance daily returns: `σ(t) = std(daily log returns over trailing 30 days) × √252`.
- **ATR (Average True Range)** — compute inline from yfinance OHLC: standard 14-day or 30-day Wilder's ATR.

### Optional but recommended

- **`indicators.db`** for the regime backdrop (VIX, HY OAS, 10Y Treasury) at the report's as-of date. Lets the recommendation note when the current regime differs from the average regime in the backtest history (e.g. "current VIX = 14, but backtest history includes 2020 and 2022 where VIX > 35"). Pull via `indicators/data_fetcher.fetch_all()`.
- **`market_cap_cache.db`** for the ticker's current market cap and liquidity bucket (cap-tier influences which strategies are tractable — micro-caps with thin liquidity can't realistically execute tiered exits without price impact).

### Not needed

- No fundamentals, no filings, no IR materials. This skill is **price-history + exit-rules only**. If the user asks "is this a value trap or a real exit signal?" — that's a `company-research` question, not a take-profit question. Pointing them at [[company-research]] is the right answer.

## Workflow

### Step 0 — Resolve ticker + check cost basis

The user input forms accepted:

- `take-profit NVDA` (no cost basis — backtest over historical entry cohorts only)
- `take-profit NVDA cost-basis 120` (use $120 as the entry assumption; report concrete sell levels from there)
- `should I take profit on NVDA from $120?` (free-form; parse out ticker + cost basis)

Resolve the ticker to a canonical symbol:
- US — uppercase letters only (`NVDA`, `META`). Pre-IPO / OTC symbols flagged.
- ETFs — same treatment (`SPY`, `QQQ`, `VOO`, `VTI`).
- HK / China A-share — convert to yfinance format (`9988.HK`, `002050.SZ`, `600519.SS`). Verify yfinance returns history; if empty, switch to `cninfo_reports` + manual price ladder.

If the user didn't supply a cost basis, run the entry-cohort backtest **without** a personal anchor — the report still produces an Exit Verdict, but the "Action Plan" section says "to translate this into concrete sell levels, re-run with `cost-basis $X` once you have your entry price."

### Step 1 — Pull adjusted price history + realized vol

Write a one-off Python script (under `oneoff/take_profit_<TICKER>.py`) that:

1. Pulls `yfinance.Ticker("<SYMBOL>").history(period="10y", auto_adjust=True)`.
2. Sanity-checks the result: ≥ 750 trading days, no obvious gaps, current price within 5% of latest close.
3. Computes daily log returns, 30-day rolling realized volatility, 14-day Wilder's ATR, peak-to-trough drawdowns.
4. Saves a clean DataFrame (CSV) under `oneoff/take_profit_<TICKER>_history.csv` for the backtest step.

**Do not** mock or fabricate price data. If yfinance returns garbage (illiquid ticker, delisted, suspended), the right output is "cannot run — insufficient clean history; here's the regime context only."

### Step 2 — Run the entry-cohort backtest

In the same `oneoff/take_profit_<TICKER>.py` script, for each strategy in the table above:

1. Enumerate every trading day in the look-back window as a hypothetical entry day. If the look-back is 10 years that's ~2,500 entry cohorts per strategy.
2. For each cohort, simulate the strategy from that entry day until either the exit rule triggers OR the look-back ends. If the look-back ends without an exit, mark-to-market at the final close.
3. Per cohort: hold-period return, peak gain, peak-to-exit drawdown, exit reason, CAGR-equivalent.
4. Aggregate across cohorts: median CAGR, win rate, rollercoaster rate (defined above), max drawdown (worst cohort), 5th/95th percentile tail.

Output a strategy-comparison DataFrame and save it as `oneoff/take_profit_<TICKER>_strategies.csv`.

### Step 3 — Generate charts (6–10 visuals)

Save under `reports/charts/take_profit_<TICKER>_*.png` (DPI 150, `bbox_inches="tight"`). Suggested chart inventory:

1. **Adjusted price + 200-day MA** — anchor chart, 10-yr view.
2. **Rolling realized volatility** — show regime shifts.
3. **Rolling max drawdown** — shows the worst path a long-only holder lived through.
4. **CAGR by strategy** — bar chart, hold vs each active rule.
5. **Max drawdown by strategy** — bar chart, same set.
6. **Rollercoaster rate by strategy** — bar chart highlighting which rules avoid the path pain.
7. **CAGR distribution (entry-cohort histogram)** — hold-only, with median + 5th/95th percentile lines.
8. **Strategy-vs-hold scatter** — each strategy as a point, x = CAGR, y = max drawdown. Closer to top-left wins.
9. *(Optional)* **Trailing-stop sweep** — CAGR vs stop width for X ∈ {10, 15, 20, 25, 30, 40}%.
10. *(Optional)* **Vol-aware stop sweep** — CAGR vs k for k ∈ {2, 3, 4, 5} × ATR.

Each chart's caption ends with: `Source: yfinance (adjusted, <YYYY-MM-DD>); strategy backtest in oneoff/take_profit_<TICKER>.py.`

### Step 4 — Write the report

Save to `reports/take-profit/<TICKER>_<YYYY-MM-DD>.md` under the project root. Target 3,000–5,000 words; structure:

1. **Exit Verdict** (one-line bold verdict + 50-word rationale).
2. **Headline Metrics** — table summarizing CAGR, max drawdown, win rate, rollercoaster rate across the five strategy families. Highlight the winner in each column.
3. **Strategy Comparison** — narrative tour of which rules dominate which dimensions. For each strategy: a short paragraph with its number from Step 2 and what trade-off it represents.
4. **Path-pain analysis** — extended treatment of the rollercoaster rate. *This is the section that distinguishes this skill from "just look at CAGR."*
5. **Regime context** — one paragraph comparing the current `indicators.db` regime (VIX, HY OAS, 10Y) to the average regime in the backtest history. If the current regime is materially different from the backtest base rate, flag it.
6. **Action Plan** — concrete sell levels if a cost basis was supplied, OR a "compute this with cost basis = $X" framework if not. Includes:
   - Tier levels: "sell 25% at $___, 50% at $___, 75% at $___" derived from the user's cost basis × the best-fitting tier multiples.
   - Trailing stop: "set initial stop at $___ (X% below current price)" sized to the best-fitting trailing-stop width.
   - Review cadence: "re-run quarterly OR when realized vol crosses ___ OR when the cost-basis-relative gain crosses ___".
7. **Failure modes** — what would invalidate this analysis: regime change vs backtest base rate, structural fundamental break that the price history can't see, illiquidity at exit.
8. **Data Used** manifest (mandatory — see "Data Used" block below).

### Step 5 — Verify and clean up

- Re-run the script to confirm it's idempotent.
- Spot-check ≥3 numbers in the report against the strategies CSV (`grep -F "<number>" oneoff/take_profit_<TICKER>_strategies.csv`).
- Stop any test servers used during chart rendering.
- Commit and push per the project's standard workflow.

## Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — how a trailing stop actually trails the peak, how a volatility-targeted (ATR-sized) exit widens and tightens with regime, how tiered scaling-out books partial profit while keeping a runner, or any other exit-discipline mechanic the reader may not know cold — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Output Format (mandatory blocks)

Every report must contain:

1. **Exit Verdict** at the top (bold, one line).
2. **Headline metrics table** — CAGR / max drawdown / win rate / rollercoaster rate for each strategy.
3. **6–10 embedded charts** with inline captions and source attribution.
4. **Action Plan** — concrete sell levels (if cost basis supplied) or a parameterized formula.
5. **`## Data Used / 数据来源清单`** manifest — sources + dates + freshness, see block format below.
6. **`## Guardrails for this verdict`** — what would invalidate the analysis.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Price history**
- yfinance adjusted OHLCV for <TICKER>, <start-date> to <end-date> (auto_adjust=True). N = <X> trading days.

**Volatility / ATR**
- 30-day rolling realized vol, 14-day Wilder's ATR — computed inline from yfinance close-to-close returns. As-of <YYYY-MM-DD>.

**Backtest cohorts**
- Entry-cohort universe: every trading day in the look-back window, <N> cohorts per strategy. Mark-to-market at look-back end for non-exiting cohorts.

**Regime backdrop (Section 5)**
- VIX, 10Y Treasury (`^TNX`), HY OAS (FRED BAMLH0A0HYM2) as of <YYYY-MM-DD>. Source: `indicators.db` via `indicators/data_fetcher.fetch_all()`.

**Cost basis (when supplied)**
- User-supplied entry price: $<X> per share.

**Stale notices / coverage gaps**
- <bulleted list — e.g. "current VIX at 14 vs backtest mean of 21 → backtest base rate may overweight calmer regimes than today">.
```

## Guardrails

- **Never run backtests on unadjusted prices.** Splits and dividends destroy the path metrics. `yfinance.history(auto_adjust=True)` is non-negotiable.
- **Never recommend exit levels for an illiquid ticker** without a liquidity warning. Median 30-day $ volume < $1M → say so; the bid-ask alone will eat the tier-exit advantage.
- **Leveraged ETFs (TQQQ, SOXL, SQQQ, UPRO, etc.) need an explicit volatility-decay paragraph.** Their daily-rebalance mechanics mean buy-and-hold over years systematically underperforms the underlying × leverage. If the user runs take-profit on a leveraged ETF, the verdict must include "Hold is NOT a real strategy here — see vol-decay section" and the backtest must include a path-decay metric.
- **Never overfit to the single best historical rule.** Report at least three strategies' results in the headline metrics; if only the "best" rule is shown, the reader sees in-sample optimization, not robust recommendation. The rollercoaster-rate metric exists precisely so the reader can see *path pain*, not just CAGR.
- **Never use this skill for a sell *now* decision.** It outputs a *rule*, not a *trade*. If the user wants "should I sell today?" the answer is "set this rule, and you'll know when". Pointing them at [[trader-plan]] is the right move for a today-trade.
- **The price history is the source of evidence; the rules are the source of opinion. Keep them separate.** Backtest results are facts; the Exit Verdict is an interpretation. The report's structure must visually distinguish the two.
- **Regime mismatch is a load-bearing failure mode.** A backtest spanning 2015–2025 has a base-rate VIX of ~21; if the current VIX is 14 the backtest base rate overweights calmer regimes than today (and vice versa). The Regime Context section must call this out — never silently assume the future looks like the average historical day.
- **No "Source: our model" / "(estimate)" / "(本模型)"** anywhere. The model is the backtest script; cite the script path (`oneoff/take_profit_<TICKER>.py`) for the strategy numbers, the underlying yfinance for the price data.
- **Never write to `db/*.db`.** This skill only reads from `indicators.db` and `market_cap_cache.db`. No `INSERT` / `UPDATE` / `DELETE`. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Output location

Save to `reports/take-profit/<TICKER>_<YYYY-MM-DD>.md` under the project root (create the `reports/take-profit/` folder if missing — first report establishes the directory). The viewer at `http://localhost:5001/reports` will surface it under a new "TAKE-PROFIT" type (or as "OTHER" until the viewer's bucket map is updated).

Supplementary deliverables sit in standard locations:
- Charts: `reports/charts/take_profit_<TICKER>_*.png`.
- Backtest script + CSVs: `oneoff/take_profit_<TICKER>.py`, `oneoff/take_profit_<TICKER>_history.csv`, `oneoff/take_profit_<TICKER>_strategies.csv`. The script must be self-contained and re-runnable.

### Update-in-place rule

One report per ticker. If `reports/take-profit/<TICKER>_*.md` already exists, update it in place (refresh the as-of date, re-run the script, regenerate the charts). Do **not** create dated parallel copies — git history is the audit trail.

## What this skill does NOT do

- It does not generate fundamentals analysis — that's [[company-research]].
- It does not produce an entry recommendation — that's [[trader-plan]].
- It does not produce a final 5-tier rating — that's [[portfolio-decision]].
- It does not run cross-ticker portfolio optimization — that's outside this project's current skill tree (would be a hypothetical future "portfolio-lab" skill).
- It does not predict regime change — the Regime Context section flags when the current regime diverges from the backtest base rate, but the backtest is the only source of edge here. If the user wants regime forecasts, that's a different question.
