# Earnings Preview

description: Build pre-earnings analysis with estimate models, scenario frameworks, and key metrics to watch. Use before a company reports quarterly earnings to prepare positioning notes, set up bull/bear scenarios, and identify what will move the stock. Triggers on "earnings preview", "what to watch for [company] earnings", "pre-earnings", "earnings setup", or "preview Q[X] for [company]".

## Workflow

### Step 1: Gather Context

- Identify the company and reporting quarter
- Pull consensus estimates via web search (revenue, EPS, key segment metrics)
- Find the earnings date and time (pre-market vs. after-hours)
- Review the company's prior quarter earnings call for any guidance or commentary

### Step 2: Key Metrics Framework

Build a "what to watch" framework specific to the company:

**Financial Metrics:**
- Revenue vs. consensus (total and by segment)
- EPS vs. consensus
- Margins (gross, operating, net) — expanding or contracting?
- Free cash flow
- Forward guidance vs. consensus

**Operational Metrics** (sector-specific):
- Tech/SaaS: ARR, net retention, RPO, customer count
- Retail: Same-store sales, traffic, basket size
- Industrials: Backlog, book-to-bill, price vs. volume
- Financials: NIM, credit quality, loan growth, fee income
- Healthcare: Scripts, patient volumes, pipeline updates

### Step 3: Scenario Analysis

Build 3 scenarios with stock price implications:

| Scenario | Revenue | EPS | Key Driver | Stock Reaction |
|----------|---------|-----|------------|----------------|
| Bull | | | | |
| Base | | | | |
| Bear | | | | |

For each scenario:
- What would need to happen operationally
- What management commentary would signal this
- Historical context — how has the stock moved on similar prints?

### Step 4: Catalyst Checklist

Identify the 3-5 things that will determine the stock's reaction:

1. [Metric] vs. [consensus/whisper number] — why it matters
2. [Guidance item] — what the buy-side expects to hear
3. [Narrative shift] — any strategic changes, M&A, restructuring

### Step 5: Output

One-page earnings preview with:
- Company, quarter, earnings date
- Consensus estimates table
- Key metrics to watch (ranked by importance)
- Bull/base/bear scenario table
- Catalyst checklist
- Trading setup: recent stock performance, implied move from options

## Further viewing — explainer videos (optional, but default to including)

When this preview turns on something a reader would struggle to picture from prose alone — the product or segment in focus for the upcoming print when its mechanics matter to the setup (a new chip / device architecture, a manufacturing or scientific process, the unit economics of a subscription or marketplace model, a market-structure concept that drives the KPI you're watching) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the preview is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Learning from sell-side institutional research

The patterns below are distilled from how Goldman Sachs, Morgan Stanley, UBS, J.P. Morgan, Bernstein, Deutsche Bank, Citi, BofA and Jefferies build into-the-print previews (Jefferies "[Ticker] [Quarter] Preview", MS "Into the Print", UBS "[Ticker] Preview · Evidence Lab inside", JPM "Key Changes", Bernstein "[Ticker] [Quarter] preview"). The single load-bearing differentiator vs. a generic preview is the **quantified gap — house vs. consensus vs. guide, shown line-by-line with a delta column.** Everything else hangs off that gap. Apply these on top of the workflow above; preserve every existing rule (citations, numerical-accuracy, chart source annotations, language defaults, file naming).

**Lead with a Header Data Block, not prose (Step 5 / new lead element).** Mirror Jefferies/JPM/MS/UBS/Bernstein: open with a compact key-value block — **Rating | 12m Price Target (current vs. PRIOR) with % to PT | last price (as-of date) | 52-week high–low | market cap | ADV** — then a multi-year FY estimate strip (**Revenue / EBIT or EBITDA / Adj Net Profit / EPS for 2 actual + 2 estimate years**). State the valuation method on the PT line (e.g. "34x next-FY EPS", "SOTP", "DCF WACC 12%"). Keep the standing Rating/PT/upside line near the top so the reader sees the call without scrolling. The `% to PT` is computed against the dated `last price` above (today), which satisfies the report-date-price rule for *your own* PT — **but any *borrowed* PT you quote (consensus mean target, a named broker's PT) must show the price on *its* note's date + the upside it fixed** (`consensus $130 vs $96 @ 2026-05-20 → +35%`), not just vs today's last price.

**Open with a bolded 3–5 sentence thesis (the call AND the setup in one breath).** Jefferies/MS lead with a verdict like "meets reduced rev/GM cons but misses EBIT by ~35%; cons still too high, too early to bottom-fish, results May 26." State the call, the gap to consensus, and the trade into the print up front — do not bury it in a generic output list.

**House vs. Consensus vs. Guide table with an explicit `vs Cons` delta column (Step 1 + Step 5).** This replaces the plain consensus table. Carry the delta on **every** line — revenue (total + by segment), gross margin (total + by segment), EBIT, EPS — plus a "vs guide range (low/mid/high)" note since institutions position forecasts against the company's own guide, not just consensus (Jefferies "JEFe vs Cons", JPM revenue "versus consensus"). Cite the named consensus source and its as-of date inline (e.g. "Source: Visible Alpha, [house] estimates"); each house number must be paired with its consensus/prior/guide counterpart per the numerical-accuracy rule.

**Add an Estimate Changes (Prev vs. Cur, % revision) table (Step 1 + Step 5).** A preview usually moves numbers — show before/after. Mirror JPM "Key Changes (Prev/Cur/%)" and Jefferies "Change to JEFe". Place it as a sibling to the House-vs-Cons table.

**Decompose any guide-change call into named $ and % contributions (Step 2).** Bernstein-Adobe pattern: "Q1 beat +$0.16, buyback +$0–3.50, M&A ~$0." Each input must trace to a source containing that number; label the summed figure as a derived calc per the numerical-accuracy rule.

**Quantify the Stock Reaction column — make it a band, not an adjective (Step 3).** Tie each scenario row to (a) the **options-implied move** computed from the at-the-money straddle and (b) the **historical average 1-day post-print move** over the last 4–8 quarters, and anchor each row to the specific KPI threshold that triggers it. Templates: Bernstein Akeso ("HR 0.70–0.72 → +10–20%; HR > 0.75 → −10–20%"), UBS Canada Goose ("balanced upside/downside skew, historical ±11.7%"). Replace "stock could move" with a percentage band tied to a named scenario.

**Add a Setup & Positioning section (new step between Step 3 and Step 4; renumber).** Cover YTD / relative performance, valuation vs. the name's own 3–5yr history (forward P/E, EV/EBIT, PEG), crowdedness / short-interest / factor exposure where available (JPM Style/Quant %-rank panel; UBS "crowdedness below sector average"), and an explicit statement of **the market bar** — what the buy-side already expects (the whisper) vs. published sell-side consensus, as a third column alongside house and consensus. Frame the deliverable as "what we would buy or sell into the print." This upgrades the thin one-line "Trading setup."

**Attempt named alt-data / channel checks before generic web search (Step 1).** Cite deep URLs: app/web panels (Sensor Tower, SimilarWeb), card-spend trackers, sector trackers (STR RevPar, Planespotters deliveries, semis: DRAM/NAND contract prices, WFE $), and the prior-quarter call transcript for guidance language. Broker proprietary labs (UBS Evidence Lab, Deutsche Bank DBDig survey, GS surveys) are the analog edge — when their reads come from the local `db/zsxq.db` library, label them `*Analyst view:*` and never blend them into a primary-filing citation.

**Sector / multi-name catalyst-preview mode (second operating mode).** When previewing a coverage universe rather than a single name, produce a **dated catalyst/event grid** that rates each upcoming catalyst by importance (High / Very important) and expected surprise direction, plus a per-name **beat / in-line / miss** call with vs-cons deltas (MS "Catalyst Preview: What's Ahead?", GS sector "1Q results preview", UBS sector "Earnings Preview"). Respect the skill's English-default convention for this tracking-style output.

**Split Risks into Upside vs. Downside bullet blocks (Step 4).** GS Moderna / MS Broadcom / Bernstein convention: two explicit lists rather than one catalyst checklist, each risk tied to its KPI and the scenario it would push the print toward.

**Title encodes the call and the hook (Step 5).** Not just ticker/quarter — e.g. "Memory Cost Pressure Not Yet Peaked; Cons Still Too High", "It's A Tricky One", "We See a Balanced Upside/Downside Skew", "Roadmap to Profitability". Numbers are always paired — every house figure shown next to consensus, prior, or guide ("PT raised 475→490", "EPS $3.05 vs cons $2.90"); a standalone number reads as incomplete. Date-stamp every estimate and consensus snapshot.

**Build in loop closure (Important Notes).** Institutional previews are accountable — banks publish a post-print scorecard (JPM "As We Previewed, [Ticker] Delivered…") grading the call against the actual print. After results, chain to the `earnings-analysis` skill as the natural follow-up so the preview's calls get graded.

## Important Notes

- Consensus estimates change — always note the source and date of estimates
- "Whisper numbers" from buy-side surveys are often more relevant than published consensus
- Historical earnings reactions help calibrate expectations (search for "[company] earnings reaction history")
- Options-implied move tells you what the market expects — compare to your scenarios
