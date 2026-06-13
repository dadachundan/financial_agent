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

**If `investment_plan` is missing**, invoke [[research-manager]] first. That skill will cascade further (running [[bull-bear-debate]] and the three analyst skills — sentiment-analyst, news-analyst, company-research — if needed).

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

Pull the **dated catalyst** (event + date + expected estimate delta) and the **Bull/Base/Bear scenario targets** from the upstream research-manager / analyst reports. If they are absent there, mine the local broker library `db/zsxq.db` (~6,900 sell-side PDFs) for a sell-side scenario set, catalyst date, and conviction rank — label anything borrowed from it `*Analyst view:*` and keep it out of any primary-filing citation (per [company-research citation standard](reference/citations.md)). **Never invent a catalyst date, a scenario target, or a current price** — if no source supplies one, say so and fall back to the "No dated catalyst" / single-point wording.

**Sell-side view evolution (卖方观点演变) — required whenever ≥2 zsxq notes cover the ticker.** Before setting the Risk-Reward levels, run the mechanical pre-pass — STRICTLY read-only (`/opt/anaconda3/bin/python3`, `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`; writes stay exclusively with `scripts/persist_pts.py`): `SELECT research_institute, rating, price_target, target_currency, report_date, report_file_id, upside_pct FROM price_targets WHERE company_ticker=? ORDER BY research_institute, report_date`. Use it two ways:

- **PT dispersion (min / median / max, spread %) sanity-frames Entry / Targets / Stop** — a Bull Target above *every* institute's PT (or a Bear Target / Stop Loss below all of them) needs an explicit one-line justification in **Reasoning** (what does this plan see that the whole street missed?). Flag same-institute revisions — PT raised/cut X → Y with the note's stated trigger; a fresh self-revision toward the trade's direction is conviction evidence, one against it belongs in the opposing 利好/利空 bullets. The filename's `-YYMMDD` suffix is the authoritative pub date; a 2026-03 PT and a 2026-06 PT from the same institute are two different dated views, not duplicates — and conflicting institutes get named on each side, never averaged into a fake consensus.
- **Artifact:** a 4–8-line **Sell-side view evolution (卖方观点演变)** note — the dispersion line + any dated revisions, each view cited as (institute, report date, `/zsxq/pdf/<file_id>/<urlencoded-name>` direct-download link) — inserted between **Risk-Reward** and **Reasoning**. Additive to the schema, like the conviction tag. Each borrowed PT still anchors to the report-date price per the "Anchor every number" rule below.

Fetch the **Current Price** anchor yourself — dated close + 52-week range via yfinance, never from news-article prose (the Risk-Reward asymmetry math is only as good as this anchor):

```bash
/opt/anaconda3/bin/python3 -c "import yfinance as yf, datetime as dt; h=yf.Ticker('<ticker>').history(period='1y'); h=h[h.index.date<=dt.date.fromisoformat('<trade_date>')]; print(round(h['Close'].iloc[-1],2), h.index[-1].date(), round(h['Close'].min(),2), round(h['Close'].max(),2))"
```

Cite it as `[Yahoo Finance quote](https://finance.yahoo.com/quote/<ticker>/)` as of the printed date (the last completed session when the pipeline's `<trade_date>` is a non-trading day — state both dates). The schema's `**Current Price**` line must come from this fetch.

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

## Further viewing — explainer videos (optional, but default to including)

When this proposal hinges on something a reader would struggle to picture from prose alone — the product or mechanism behind the trade (a humanoid robot's actuators / harmonic reducers / force sensors, an HBM stack or advanced-packaging flow, a surgical-robot end-effector, a battery cell-to-pack architecture), the catalyst the thesis turns on, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* what the trade is actually long or short, not just read about it. Default to including them on any topic; omit only when the proposal is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

> Full spec: [`reference/citations.md`](reference/citations.md) § "Further viewing — explainer videos".

## Learning from sell-side institutional research

The bare Buy/Hold/Sell + flat entry/stop is a desk shorthand; sell-side tactical notes carry a fuller anatomy that the schema above borrows. Apply these named house patterns:

- **Mirror Morgan Stanley "Risk Reward Update": three named scenarios, each with its own target and a labeled % move off a dated current price.** Bull/Base/Bear is the spine — not a single point estimate. Show each target's valuation basis (e.g. `28x cycle-EPS` or DCF CoE/perpetual-growth) so it is reconstructible, and close with an explicit asymmetry line (`+48.7% to bull vs −37.7% to bear`). The **Stop Loss is the bear-case level**, justified — not a round-number guess; the take-profit is the bull/base level.

- **Mirror J.P. Morgan "Positive Catalyst Watch": the catalyst is a first-class, DATED field, kept separate from the standing rating.** Name the event, its date/window, the expected fundamental outcome, and a one-word landing probability (`high/medium/low`). Write events scannably as `Event (Date, importance)` — `Investor Day (June 24, high)`. A rating can stay Hold while the name is "on Positive Catalyst Watch into <date>".

- **Mirror the universal "利好 / 利空" close: symmetric labeled risk bullets, bear case at equal billing.** Every Risk Reward Update, Catalyst Watch, and Conviction-List entry ends with explicit upside-risks AND downside-risks (2–3 each), not a single "risks" afterthought.

- **Grade conviction, never ship it bare** (GS "Conviction List", Citi "Top Pick", Bernstein "Best Idea", MS "Three Actionable Ideas"). One crisp actionable line — rating + the single catalyst + the target — before any deeper rationale, and a named conviction tag rather than a binary Buy/Hold/Sell.

- **Anchor every number to a reference** (the desk standard): a target price is always shown with its `%up/downside` off a dated current price and against the 52-week range; consensus context (rating/PT distribution, the bank's estimate-vs-consensus delta) shows where the trade is differentiated vs crowded. A bare target with no spot anchor is a non-call. **For a *borrowed* `*Analyst view:*` scenario target or PT mined from `db/zsxq.db`, the anchoring price is the stock's price on *that note's date*, not just today's spot** (`Bull $288 vs $232 @ 2026-06-03 → +24%`) — the report-date price is what shows the upside the analyst actually called and how much has since played out; pull it from `stock_price_target_db` (`report_date_price` / `upside_pct`, at `/pt`). Your own plan's targets stay anchored to the dated current price.

### Basket mode (optional — future multi-ticker runs)

The current pipeline is single-ticker. If `trader-plan` is ever run across a basket, add a **strategy-scorecard** convention so the process is accountable over time — mirror MS "Three Actionable Ideas" (cumulative/excess return, avg holding-period return, **hit rate** = % positive / % beat benchmark) and GS "Conviction List Directors' Cut" (dated add/remove churn with the reason, e.g. "added May 3, removed May 25 on price underperformance"). Each basket entry still carries its own %upside-to-target.

## Persist output

Write the markdown to `<company-folder>/trading/<TRADE-DATE>/trader-plan.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
