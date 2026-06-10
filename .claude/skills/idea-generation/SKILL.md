# Idea Generation

description: Systematic stock screening and investment idea sourcing. Combines quantitative screens, thematic research, and pattern recognition to surface new long and short ideas. Use when looking for new ideas, running screens, or conducting thematic sweeps. Triggers on "idea generation", "stock screen", "find ideas", "what looks interesting", "screen for", "new ideas", or "pitch me something".

## Workflow

### Step 1: Define Search Criteria

Ask the user for parameters:
- **Direction**: Long ideas, short ideas, or both
- **Market cap**: Large, mid, small, micro
- **Sector**: Specific sector or cross-sector
- **Style**: Value, growth, quality, special situation, event-driven
- **Geography**: US, international, global
- **Theme**: Any specific thematic angle (AI, reshoring, aging demographics, etc.)

### Step 2: Quantitative Screens

Run screens based on the style:

**Value Screen**
- P/E below sector median
- EV/EBITDA below historical average
- Free cash flow yield >5%
- Price/book below 1.5x
- Insider buying in last 90 days
- Dividend yield above market average

**Growth Screen**
- Revenue growth >15% YoY
- Earnings growth >20% YoY
- Revenue acceleration (growth rate increasing)
- Expanding margins
- High return on invested capital (>15%)
- Strong net retention (>110% for SaaS)

**Quality Screen**
- Consistent revenue growth (5+ years)
- Stable or expanding margins
- ROE >15%
- Low debt/equity
- High free cash flow conversion
- Insider ownership >5%

**Short Screen**
- Declining revenue or decelerating growth
- Margin compression
- Rising receivables / inventory vs. sales
- Insider selling
- Valuation premium to peers without justification
- High short interest with deteriorating fundamentals
- Accounting red flags (auditor changes, restatements)

**Special Situation Screen**
- Recent IPOs / SPACs with lockup expirations
- Spin-offs in last 12 months
- Companies emerging from restructuring
- Activist involvement
- Management changes at underperforming companies

### Step 3: Thematic Sweep

For thematic ideas, research the theme and identify beneficiaries:

1. Define the thesis (e.g., "AI infrastructure spending accelerates through 2026")
2. Map the value chain — who benefits directly vs. indirectly?
3. Identify pure-play vs. diversified exposure
4. Assess which names are already "priced in" vs. under-appreciated
5. Look for second-order beneficiaries that the market hasn't connected to the theme

### Step 4: Idea Presentation

For each idea that passes the screen, present:

**[Long/Short] · [Conviction: High / Watchlist] · [Company Name] ([Ticker]) — [One-Line Thesis]**

Lead with the action, mirroring the **MS "Three Actionable Ideas"** header (the recommendation comes first, not buried under the metric table). One decision-first line.

| Metric | Value | vs. Peers |
|--------|-------|-----------|
| Market cap | | |
| EV/EBITDA (NTM) | | |
| P/E (NTM) | | |
| Revenue growth | | |
| EBITDA margin | | |
| FCF yield | | |
| 12-month price target | | implied upside/downside % vs last close |
| Valuation basis | | e.g. "2027E 24× P/E" / "DCF WACC 9%" |

**Thesis (3-5 bullets):**
- Why this is mispriced — frame as the **GS "free call option"** asymmetry: what the price *currently implies* and why that's wrong (GS on S-Oil: "price implies sub-mid-cycle diesel cracks → the duration of high cracks is a free option").
- What the market is missing
- The single **dated** catalyst that re-rates it (next print / investor day / data read-out — give the date), plus the priced-in test (how much of the bear case is already in the price)

**Asymmetry:** upside (to bull-case PT) vs downside (to bear-case PT) — an explicit `+X% / −Y%` skew vs last close, not a one-sided target.

**Key Risks:**
- What would make this wrong (the falsifiable conditions)

**Suggested Next Steps:**
- Build full model? Deep-dive diligence? Expert call? Hand the ticker to [[company-research]] / [[trader-plan]].

### Further viewing — explainer videos (optional, but default to including)

When an idea card covers something a reader would struggle to picture from prose alone — the product or technology underlying a surfaced idea (e.g. a humanoid robot's actuators / harmonic reducers / force sensors, an advanced-packaging or lithography step, an unfamiliar SaaS / marketplace business model, or a market-structure concept) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the idea is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the idea card the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### Step 5: Output

- Shortlist of 5-10 ideas with one-page summaries
- Screening criteria and methodology documented
- Comparison table across all ideas
- Prioritized list: which ideas to research first

## Learning from sell-side institutional research

How GS / Morgan Stanley / Citi build the *idea-list* report type (mined from the local `db/zsxq.db` broker library — MS "Three Actionable Ideas", GS "Conviction List / Directors' Cut", GS "Connecting the Dots", Citi high-conviction calls). Each lesson sits ON TOP of the project's citation, numerical-accuracy, and chart-source rules — every price target / estimate quoted in actual output is labelled `*Analyst view:*` (never sourced to a filing) and every number string-matches a cited URL.

- **Curate to a tight, action-first short list (MS "Three Actionable Ideas").** The flagship product is *three* genuinely actionable ideas, not a 30-name screen dump. Lead each with the recommendation; the screen is the funnel, the short list is the deliverable. Prefer 3–10 high-conviction names over a long unranked table.
- **Run the short list as a tracked equal-weight basket with explicit ADD / REMOVE discipline (GS "Conviction List — Directors' Cut").** Each refresh names what was *added* and *removed that month, with the date and the reason* (GS removed Futu on 5/25 after a 3-week drawdown; added S-Oil on an FCF-inflection call). Carry the basket's **cumulative performance vs an equal-weight benchmark** since inception (GS: +87% since Jun-2023, ahead of S&P 500 EW). This turns "ideas" into an accountable, diff-able portfolio — pair with [[thesis-tracker]] for the scorecard.
- **Bucket ideas under 3–6 macro themes, not a flat list (GS "Conviction List" five themes / "Connecting the Dots").** GS groups names under themes — *AI & power, productivity & margins, inflation & rates, consumer resilience, geopolitics & militarization*. Organize your short list the same way so the reader sees the bet, not just the tickers.
- **Every idea carries a 12-month price target + rating + implied upside % + valuation basis (GS S-Oil: Buy, 147,000 KRW, +37%, FCF-yield-to-18%-by-2027).** A screen surfaces candidates; an *idea* states the target and the math. Put the valuation method in the line ("2027E 24× P/E", "DCF WACC 9%"). Label sell-side ratings/PTs `*Analyst view:*` — **and when the PT is *borrowed* from a dated broker note (zsxq library or a cited sell-side report), pair it with the stock's price on that note's date + the upside it fixed** (`GS S-Oil Buy, 147,000 KRW vs 107,000 @ 2026-05-22 → +37%`), not today's spot. The report-date close + upside are stored in `stock_price_target_db` (`report_date_price` / `upside_pct`, surfaced at `/pt`); read them back. A borrowed PT with no report-date price is not actionable — `report-date price n/a` only when yfinance has no close for that date.
- **For a thematic idea, rank the value chain in preference order and pick the top name per tier (Citi battery-materials).** Citi's call wasn't "buy lithium" — it was `锂资源 (lithium resource) > 正极 (cathode) > 电池 (cell) > 电解液 (electrolyte) > 隔膜 (separator)`, with a top pick per tier and a quantified theme target (lithium carbonate to ¥250k/t by Aug–Sep). In Step 3, replace "map the value chain" with a *ranked* value chain + a quantified theme target.
- **Frame the mispricing as a "free option" asymmetry (GS house signature).** State what the current price implies, why the market is wrong, and the upside-vs-downside skew — not a one-sided "it's cheap." The free-option device (you're paid to wait; the optionality is unpriced) is GS's most repeated idea-pitch move.
- **Codify GS's published "lessons learned" into the maintenance loop.** GS's three rules: *ride the winners that beat on the first print* (they keep beating), *cut losers fast after a miss* (don't average down a broken thesis), *earnings drive price long-term*. Wire these into the idea-review cadence (the [[take-profit-lab]] / [[thesis-tracker]] handoff).
- **Source candidates from the broker conviction lists themselves.** Before/alongside the quantitative screens, mine `db/zsxq.db` for the latest MS "Three Actionable Ideas" / GS "Conviction List" adds — exactly what [[zsxq-ideas]] automates. idea-generation is its Step-4 presentation layer, so match this house-style card format so the two compose cleanly.

## Important Notes

- Screens surface candidates, not conclusions — every screen output needs fundamental work
- The best ideas often come from intersections (e.g., quality company at value price due to temporary headwind)
- Avoid crowded trades — check ownership data, short interest, and how many analysts cover the name
- Contrarian ideas need a catalyst — being early without a catalyst is the same as being wrong
- Track idea hit rates over time — which screens and approaches produce the best ideas?
- Short ideas need higher conviction — timing is harder and risk is asymmetric
