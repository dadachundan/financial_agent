---
name: earnings-preview
description: Build pre-earnings analysis with estimate models, scenario frameworks, and key metrics to watch. Use before a company reports quarterly earnings to prepare positioning notes, set up bull/bear scenarios, and identify what will move the stock. Triggers on "earnings preview", "what to watch for [company] earnings", "pre-earnings", "earnings setup", or "preview Q[X] for [company]".
---

# Earnings Preview

**Language:** English-only by default (this is a fast-turnaround, monitoring-style note, matching the project's tracking-skills English-default rule). Produce bilingual / Simplified-Chinese output only on explicit request (`in Chinese`, `bilingual`, `--lang zh`).

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

### Step 4: Setup & Positioning

Cover YTD / relative performance, valuation vs. the name's own 3–5yr history (forward P/E, EV/EBIT, PEG), crowdedness / short-interest / factor exposure where available, and an explicit statement of **the market bar** — what the buy-side already expects (the whisper) vs. published sell-side consensus. Close with the trade: what you would buy or sell into the print. (Sell-side analogs in the Learning section below.)

### Step 5: Catalyst Checklist

Identify the 3-5 things that will determine the stock's reaction:

1. [Metric] vs. [consensus/whisper number] — why it matters
2. [Guidance item] — what the buy-side expects to hear
3. [Narrative shift] — any strategic changes, M&A, restructuring

### Step 6: Output

A 1,000–2,500-word (2–4 page) into-the-print note. Required skeleton (the canonical layout per the Learning section below):

- Header Data Block (rating | 12m PT | last price | implied move) + multi-year estimate strip
- Bolded 3–5 sentence thesis — the call AND the setup
- House vs. Consensus vs. Guide table with `vs Cons` delta column
- Estimate Changes (Prev / Cur / % revision) table
- Bull/base/bear scenario table with quantified reaction bands
- Setup & Positioning (Step 4)
- Sell-side view evolution (卖方观点演变) — required when ≥2 zsxq broker previews cover the name (who-expects-what table + into-the-print revisions; see the Learning section)
- Upside / Downside risk lists + catalyst checklist

A literal one-page quick preview is an explicit opt-in mode only (user says "quick preview" / "one-pager") — never the default.

**File location (MUST):** save to `reports/earnings/<TICKER>_Q<X>FY<YY>_preview_<YYYY-MM-DD>.md` (English ticker first per the project filename rule; the `_preview` marker distinguishes it from post-print `earnings-analysis` updates in the same bucket). Commit + push in the same task (Conventional Commit, e.g. `feat(reports/earnings): ...`). The post-print scorecard (loop closure via `earnings-analysis`) reads this file back — an unsaved preview cannot be graded.

### Step 7: Verify & log

Before saving/committing:

1. HTTP-check every URL with a real-browser User-Agent — `200 OK` only; drop or replace failures per the link-validation rule.
2. Spot-check 3–5 numbers (consensus EPS/revenue, implied move, historical reaction stats) — each must string-match the URL cited in the same paragraph.
3. Confirm every house figure is paired with its consensus / prior / guide counterpart.
4. Conditional — when ≥2 zsxq broker previews covered the name: confirm the sell-side view-evolution block landed (every institute view dated + `/zsxq/pdf/` cited, into-the-print revisions arrow'd with triggers, no blended consensus across disagreeing notes).
5. Append `<details><summary>Verification log — YYYY-MM-DD</summary>...</details>` listing each check. Spec: `.claude/skills/company-research/references/citations.md`.

## Further viewing — explainer videos (optional, but default to including)

When this preview turns on something a reader would struggle to picture from prose alone — the product or segment in focus for the upcoming print when its mechanics matter to the setup (a new chip / device architecture, a manufacturing or scientific process, the unit economics of a subscription or marketplace model, a market-structure concept that drives the KPI you're watching) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the preview is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Learning from sell-side institutional research

The patterns below are distilled from how Goldman Sachs, Morgan Stanley, UBS, J.P. Morgan, Bernstein, Deutsche Bank, Citi, BofA and Jefferies build into-the-print previews (Jefferies "[Ticker] [Quarter] Preview", MS "Into the Print", UBS "[Ticker] Preview · Evidence Lab inside", JPM "Key Changes", Bernstein "[Ticker] [Quarter] preview"). The single load-bearing differentiator vs. a generic preview is the **quantified gap — house vs. consensus vs. guide, shown line-by-line with a delta column.** Everything else hangs off that gap. Apply these on top of the workflow above; preserve every existing rule (citations, numerical-accuracy, chart source annotations, language defaults, file naming).

**Lead with a Header Data Block, not prose (Step 6 / new lead element).** Mirror Jefferies/JPM/MS/UBS/Bernstein: open with a compact key-value block — **Rating | 12m Price Target (current vs. PRIOR) with % to PT | last price (as-of date) | 52-week high–low | market cap | ADV** — then a multi-year FY estimate strip (**Revenue / EBIT or EBITDA / Adj Net Profit / EPS for 2 actual + 2 estimate years**). State the valuation method on the PT line (e.g. "34x next-FY EPS", "SOTP", "DCF WACC 12%"). Keep the standing Rating/PT/upside line near the top so the reader sees the call without scrolling. The `% to PT` is computed against the dated `last price` above (today), which satisfies the report-date-price rule for *your own* PT — **but any *borrowed* PT you quote (consensus mean target, a named broker's PT) must show the price on *its* note's date + the upside it fixed** (`consensus $130 vs $96 @ 2026-05-20 → +35%`), not just vs today's last price.

**Open with a bolded 3–5 sentence thesis (the call AND the setup in one breath).** Jefferies/MS lead with a verdict like "meets reduced rev/GM cons but misses EBIT by ~35%; cons still too high, too early to bottom-fish, results May 26." State the call, the gap to consensus, and the trade into the print up front — do not bury it in a generic output list.

**House vs. Consensus vs. Guide table with an explicit `vs Cons` delta column (Step 1 + Step 6).** This replaces the plain consensus table. Carry the delta on **every** line — revenue (total + by segment), gross margin (total + by segment), EBIT, EPS — plus a "vs guide range (low/mid/high)" note since institutions position forecasts against the company's own guide, not just consensus (Jefferies "JEFe vs Cons", JPM revenue "versus consensus"). Consensus must be cited to a deep URL the agent actually fetched and that string-matches the figure — e.g. the Yahoo Finance analysis page, a stockanalysis.com forecast page, or a dated zsxq broker PDF labelled *Analyst view:* (cite via the `/zsxq/pdf/<file_id>/<name>` direct-download route). NEVER attribute a number to Visible Alpha / Bloomberg / FactSet unless quoting a secondary source that itself prints it (use a source-chain label). Always date-stamp the consensus snapshot; each house number must be paired with its consensus/prior/guide counterpart per the numerical-accuracy rule.

**Sell-side view evolution (卖方观点演变) — mandatory when ≥2 zsxq broker previews cover the name (Step 4 + Step 6).** Pre-print disagreement IS the setup signal — never blend the notes into a fake consensus. Render a who-expects-what table next to Setup & Positioning: `| Institute | Date | Rating / PT | Estimate vs Cons | Swing factor they flag / what would prove them right |` — every row dated (the filename's `-YYMMDD` suffix is the authoritative pub date; sanity-check against `create_time`) and cited via the `/zsxq/pdf/<file_id>/<name>` direct-download route. Call out **into-the-print revisions** explicitly — an institute that updated numbers/PT within the last month is a signal; give the stated trigger (channel checks, order data, a peer's print) and render it as a dated arrow (`UBS $120 (26-05) → $135 (26-06, post-peer beat)`); a 2026-03 view and a 2026-06 view from the same institute are two different views, not duplicates. Detect revisions and PT dispersion (min/median/max, spread %) mechanically BEFORE re-reading any PDF — STRICTLY read-only pre-pass: `/opt/anaconda3/bin/python3` with `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`, `SELECT research_institute, rating, price_target, target_currency, report_date, report_file_id, upside_pct FROM price_targets WHERE company_ticker=? ORDER BY research_institute, report_date` (writes stay exclusively with `scripts/persist_pts.py`). Where institutes read the same datapoint oppositely (opposite ratings, PTs >20% apart), keep both rows and let the bull/bear scenario table say whose evidence resolves it.

**Add an Estimate Changes (Prev vs. Cur, % revision) table (Step 1 + Step 6).** A preview usually moves numbers — show before/after. Mirror JPM "Key Changes (Prev/Cur/%)" and Jefferies "Change to JEFe". Place it as a sibling to the House-vs-Cons table.

**Decompose any guide-change call into named $ and % contributions (Step 2).** Bernstein-Adobe pattern: "Q1 beat +$0.16, buyback +$0–3.50, M&A ~$0." Each input must trace to a source containing that number; label the summed figure as a derived calc per the numerical-accuracy rule.

**Quantify the Stock Reaction column — make it a band, not an adjective (Step 3).** Tie each scenario row to (a) the **options-implied move** computed from the at-the-money straddle and (b) the **historical average 1-day post-print move** over the last 4–8 quarters, and anchor each row to the specific KPI threshold that triggers it. Templates: Bernstein Akeso ("HR 0.70–0.72 → +10–20%; HR > 0.75 → −10–20%"), UBS Canada Goose ("balanced upside/downside skew, historical ±11.7%"). Replace "stock could move" with a percentage band tied to a named scenario.

**Setup & Positioning section (Step 4 in the workflow above).** Cover YTD / relative performance, valuation vs. the name's own 3–5yr history (forward P/E, EV/EBIT, PEG), crowdedness / short-interest / factor exposure where available (JPM Style/Quant %-rank panel; UBS "crowdedness below sector average"), and an explicit statement of **the market bar** — what the buy-side already expects (the whisper) vs. published sell-side consensus, as a third column alongside house and consensus. Frame the deliverable as "what we would buy or sell into the print." This upgrades the thin one-line "Trading setup."

**Attempt named alt-data / channel checks before generic web search (Step 1).** Cite deep URLs: app/web panels (Sensor Tower, SimilarWeb), card-spend trackers, sector trackers (STR RevPar, Planespotters deliveries, semis: DRAM/NAND contract prices, WFE $), and the prior-quarter call transcript for guidance language. Broker proprietary labs (UBS Evidence Lab, Deutsche Bank DBDig survey, GS surveys) are the analog edge — when their reads come from the local `db/zsxq.db` library, label them `*Analyst view:*` and never blend them into a primary-filing citation.

**Sector / multi-name catalyst-preview mode (second operating mode).** When previewing a coverage universe rather than a single name, produce a **dated catalyst/event grid** that rates each upcoming catalyst by importance (High / Very important) and expected surprise direction, plus a per-name **beat / in-line / miss** call with vs-cons deltas (MS "Catalyst Preview: What's Ahead?", GS sector "1Q results preview", UBS sector "Earnings Preview"). Respect the skill's English-default convention for this tracking-style output. **Boundary with [[catalyst-calendar]]:** catalyst-calendar owns the calendar itself (dated grids across event types over a universe); this mode exists only for per-name into-the-print *calls* (beat / in-line / miss with vs-cons deltas and scenario bands) on names reporting in the window. Route pure scheduling requests to catalyst-calendar, and accept its handoffs for the names worth a call.

**Split Risks into Upside vs. Downside bullet blocks (Step 5).** GS Moderna / MS Broadcom / Bernstein convention: two explicit lists rather than one catalyst checklist, each risk tied to its KPI and the scenario it would push the print toward.

**Title encodes the call and the hook (Step 6).** Not just ticker/quarter — e.g. "Memory Cost Pressure Not Yet Peaked; Cons Still Too High", "It's A Tricky One", "We See a Balanced Upside/Downside Skew", "Roadmap to Profitability". Numbers are always paired — every house figure shown next to consensus, prior, or guide ("PT raised 475→490", "EPS $3.05 vs cons $2.90"); a standalone number reads as incomplete. Date-stamp every estimate and consensus snapshot.

**Build in loop closure (Important Notes).** Institutional previews are accountable — banks publish a post-print scorecard (JPM "As We Previewed, [Ticker] Delivered…") grading the call against the actual print. After results, chain to the `earnings-analysis` skill as the natural follow-up so the preview's calls get graded.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the subject of the output — the ticker, theme, sector, ETF holdings, deal, or any name that materially drives the analysis — sits in **AI** (foundation models, AI software/agents, AI infrastructure: datacenter compute, networking, power), **robotics** (humanoids, industrial automation, AMRs, actuators / reducers / sensors / end-effectors), or **semiconductors** (fabless, foundry, IDM, memory/HBM, equipment/WFE, materials, EDA/IP, advanced packaging), give those names a **detailed narrative treatment**, not summary bullets:

- **Write full narrative prose** for the sector-relevant sections — mechanism and causality ("X drives Y because Z"), not headline restating. Bullets may organize the prose but never replace it.
- **Cover the sector-specific dimensions that apply:**
  - *Technology position & roadmap* — process node / architecture / model-capability cadence vs named competitors (e.g., N2 vs 18A, HBM3E→HBM4, GB200→Rubin, Optimus gen-3 vs Figure 03).
  - *Supply-chain position* — key suppliers and customers up/down the chain, single-source chokepoints (TSMC/CoWoS, EUV, HBM), where pricing power sits, content-per-unit ($ per GPU / per robot / per vehicle).
  - *AI demand linkage* — the explicit path from AI capex to this name's P&L (orders → backlog → revenue recognition) with the actual disclosed numbers, never a generic "AI beneficiary" label.
  - *Robotics linkage* — design-win status, which platforms (Tesla Optimus, Figure, Unitree, domestic Chinese OEMs), volume and timeline realism vs the hype cycle.
  - *Cycle context* — where the semi / memory-pricing / AI-capex cycle stands right now and what that implies for forward estimates.
  - *Geopolitics & export controls* — US BIS rules, China localization, tariff exposure, entity-list status where relevant.
- **Quantify the narrative.** Each dimension covered should carry at least one sourced number (TAM, ASP, capacity, units, share). All figures obey the project's numerical-accuracy rule — every number traces to a URL or PDF page cited in the same paragraph.
- **Engage the sell-side view.** Where the zsxq library or other broker sources are in scope for this skill, the AI/robotics/semi narrative must engage the institute view (PTs, estimate revisions, cross-broker disagreement) rather than ignoring it.

This rule **deepens** the skill's existing output format — it never replaces or shortens the required structure. For subjects outside these sectors, the skill's baseline depth applies unchanged.

## Important Notes

- Consensus estimates change — always note the source and date of estimates
- "Whisper numbers" from buy-side surveys are often more relevant than published consensus
- Historical earnings reactions help calibrate expectations (search for "[company] earnings reaction history")
- Options-implied move tells you what the market expects — compare to your scenarios
