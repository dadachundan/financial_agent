---
name: market-status
description: Goldman-Sachs-Weekly-Kickstart-style market-exuberance dashboard. Scores how much of a late-cycle euphoria the equity market is currently expressing — using the same 9 indicators GS uses to "evaluate exuberance" (Momentum factor returns, S&P 500 52-week market breadth, GS Speculative Trading Indicator, CBOE Put/Call ratio, median short interest, Yale Stock Market Confidence Indices, AAII Investor Sentiment, US IPO count, Net US equity issuance) plus the broader Kickstart dashboard pages (Sentiment Indicator, Financial Conditions Index, fund flows, GDP nowcast, VIX, realized correlation, SPX vs equal-weight, factor & sector returns, top movers, P/E and ERP, top-10 concentration). Each indicator gets a percentile rank vs its own ~30-year history; a single composite Exuberance Score (0–100) maps to a 5-tier verdict (Frothy / Stretched / Elevated / Neutral / Subdued). Produces a 3,000–5,000 word English markdown report mirroring the GS US Weekly Kickstart layout — Verdict box up top, 9-indicator calibration table (Dot-Com / 2021 / Current), Share-prices / Trading-activity / Investor-sentiment / Corporate-sentiment narrative blocks, plus a "Macro & Cross-Asset" dashboard panel. Use when the user asks "is the market in exuberance?", "is this dot-com / 2021 again?", "are we frothy?", "what does the Kickstart-style dashboard say?", "/market-status", "AI bubble check", "is the rally overextended?", or anything in the bull-market-peak / momentum-mania / late-cycle-euphoria family.
---

# Market Status

Quantify where the US equity market sits on a single late-cycle-euphoria axis,
using the same nine indicators Goldman Sachs uses to "evaluate exuberance" in
the Weekly Kickstart ([2026-06-05 issue](https://www.goldmansachs.com/insights/topics/portfolio-strategy)).
The motivating observation from the GS report:

> "A collection of indicators generally signals exuberance that registers above
> historical averages today but below the levels reached at market peaks in
> 2000 and 2021. … we evaluate nine metrics across four categories that
> exhibited a median 100th percentile rank vs. history in 2000 and 95th
> percentile rank in 2021. Today, those measures rank in the 86th percentile
> since 1995."
>
> — Goldman Sachs US Weekly Kickstart, 5 June 2026

This skill reproduces that calibration table with **public-data proxies** and
adds the broader Kickstart dashboard pages (Financial Conditions, fund flows,
GDP, vol, correlation, factor & sector returns, top movers, P/E & ERP).

This is a **regime / macro lens** — not a single-name call. It pairs with the
project's existing [[market-complacency]] skill (credit-led under-priced-risk
read), which approaches the same axis from a different angle.

## When to use

The user says any of:

- "Is the market in exuberance / froth right now?"
- "Is this dot-com / 2021 again?"
- "Is the AI rally overextended?"
- "Run the GS Kickstart-style dashboard"
- "Bull-market-peak check"
- "/market-status"
- "Market sentiment dashboard"
- "Are we in late-cycle euphoria?"

The skill produces an **Exuberance Verdict** (5-tier) backed by a composite
percentile score and a per-indicator breakdown calibrated against the two
clean historical exuberance peaks (Q1 2000, Q4 2021).

## When NOT to use

- The user wants a single-ticker call — use [[trader-plan]] / [[portfolio-decision]] / [[take-profit-lab]].
- The user wants a *credit / under-priced risk* read specifically — use [[market-complacency]] (credit-led, HY/IG/CCC OAS focused).
- The user wants a *sector-specific* froth read (e.g. "are semis frothy?") — use [[sector-overview]] with a stress lens.
- The user wants to know *when* the bull market ends — exuberance can persist for quarters (GS: "Speculative mania is a poor timing indicator"). This skill is a **state read**, not a timing model.
- The user wants short-bias candidates — hand off to [[idea-generation]] after the verdict prints.

## Core methodology

### The exuberance axis

For each of the nine GS headline indicators, define a direction such that
**higher complacency-percentile = more exuberant**. Then the composite is a
simple weighted average of those percentiles, mapped to a 0–100 scale where:

- **0–20**: Subdued (bearish positioning, broad pessimism — contrarian buy)
- **20–40**: Neutral
- **40–60**: Elevated (signs of optimism but no broad froth)
- **60–80**: Stretched (multiple GS indicators in the 80–95 percentile band — late-cycle territory)
- **80–100**: Frothy (≥ 5 of 9 indicators in the top decile — 2000 / 2021-style euphoria)

### The 9 GS Kickstart indicators (Exhibit 3 of the source PDF)

| # | Indicator | GS direction | Public source | GS 2000 %tile | GS 2021 %tile |
|---|---|---|---|---|---|
| **Share prices** | | | | | |
| 1 | **Momentum factor return** (3M rolling) | High = exuberant | yfinance `MTUM` (iShares MSCI USA Momentum Factor ETF) — rolling 3M total return vs SPY same window | 100 | 76 |
| 2 | **S&P 500 52-week market breadth** | Narrow = exuberant (inverted) | Compute from yfinance SPX constituents — diff between SPX-distance-from-52wk-high and median-constituent-distance-from-52wk-high. Equivalent published series: NYSE breadth indices | 100 | 95 |
| **Trading activity** | | | | | |
| 3 | **GS Speculative Trading Indicator** | High = exuberant | Proprietary — proxy: equal-weighted return of (ARKK + IPO + BUZZ + RNMC) ÷ SPY rolling 3M. When proxy diverges materially from the last published GS chart, the agent overrides with a WebSearch-sourced absolute level (the GS chart is published roughly monthly in the Kickstart) | 100 | 99 |
| 4 | **CBOE Equity Put/Call ratio** (21-day MA) | Low = exuberant (inverted) | Cboe `equitypc.csv` is stale (Oct 2019). Live path: yfinance `^CPC` (CBOE Total Put/Call) — proxy for the equity series. Fallback: WebSearch for "CBOE equity put/call latest" weekly value | 100 | 97 |
| 5 | **Short interest, median S&P 500 stock** (% of market cap) | Low = exuberant (inverted) | FINRA short-interest summary monthly. Substitute when the file is gated: WebSearch for "S&P 500 median short interest 2026" or "NYSE short interest" | 96 | 89 |
| **Investor sentiment** | | | | | |
| 6 | **Yale US Stock Market Confidence Indices** (Buy-on-Dips − Valuation Confidence) | High = exuberant | Yale ICF — monthly published at [som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices](https://som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices). Six-month MA of investor and individual investor sub-indices | 100 | 96 |
| 7 | **AAII Investor Sentiment** (Bull − Bear, 3-month MA) | High = exuberant | aaii.com weekly survey. CSV blocked (HTTP 403 since 2025) — WebSearch fallback for the latest weekly print | 99 | 92 |
| **Corporate sentiment** | | | | | |
| 8 | **Number of US IPOs (YTD annualised, > $25M deal value)** | High = exuberant | Renaissance Capital IPO Center stats — annual count. Reads via WebSearch (Renaissance refreshes weekly during the IPO window) | 100 | 87 |
| 9 | **Net US public equity issuance** (12m rolling, % of market cap) | High = exuberant | SIFMA Quarterly Equity Issuance Survey. Substitute: FRED `IPONSUE`-style series do not exist — WebSearch for "SIFMA US equity issuance Q1 2026 quarterly" | 100 | 99 |

The composite is a **weighted average** of the nine indicators' exuberance percentiles. Weights default to equal (1/9 each) so the score remains a faithful average of GS's own categories — the only deviation is dropping an indicator if it cannot be sourced in a given run (with re-normalisation and a disclosure in Data Used).

### Broader dashboard panel (qualitative — not part of the composite)

The GS Kickstart's middle pages carry a much larger dashboard. The skill pulls and renders the following as **context tables and charts** that anchor the report's narrative blocks:

- **GS US Equity Sentiment Indicator** — combines 9 positioning measures. Proprietary; WebSearch for latest value.
- **GS Financial Conditions Index (US FCI)** — proprietary. Public substitute: Chicago Fed NFCI (FRED `NFCI`) tracks the same axis.
- **Cumulative 12-month mutual-fund + ETF flows** (equities / bonds / money-markets) — ICI weekly. WebSearch for the latest aggregate.
- **10-year US Treasury yield** — FRED `DGS10`.
- **Fed-funds market pricing at year-end 2026** — CME FedWatch. WebSearch for current implied rate.
- **Consensus forward 4Q real US GDP growth** — Atlanta Fed `GDPNow` (real-time nowcast) or Bloomberg consensus.
- **S&P 500 3-month implied volatility (VIX3M)** + spot VIX — yfinance `^VIX` and `^VIX3M`.
- **S&P 500 3-month realized average stock correlation** — derived from yfinance top-50 SPX members' rolling 3M correlation matrix.
- **Concentration of top-10 names in S&P 500 market cap and earnings** — derived from yfinance SPX constituents.
- **Forward 12-month P/E** — multpl.com monthly + factor ETFs for cross-index NTM PE.
- **S&P 500 yield gap** = (forward EPS yield) − (real 10Y TIPS yield) — derived. FRED `DFII10` for the TIPS yield.
- **EPS revision breadth** — FactSet/IBES is paywall; WebSearch for the latest FactSet Earnings Insight number.
- **Sector returns + sector forward P/E** — yfinance sector ETFs (XLK / XLF / XLY / XLP / XLV / XLI / XLE / XLB / XLU / XLRE / XLC).
- **Factor returns (Momentum / Value / Growth)** — yfinance `MTUM` / `IWD` / `IWF`.
- **Top-10 weekly movers** (largest + smallest 5-day total return among SPX) — derived from yfinance.

### Per-indicator percentile mapping

For each indicator with ≥ 10 years of clean history (target: 30 years, matching the GS Exhibit 3 "since 1995" base):

1. **Current value** — most recent valid observation.
2. **Historical percentile rank** — where today sits in the full available history (30y for the headline 9; 10y for the broader panel).
3. **Exuberance percentile** — for "low = exuberant" indicators, `100 − raw_pct`; otherwise `raw_pct`.
4. **Decile label** — "1st (least exuberant)" through "10th (most exuberant)".
5. **Top-decile flag** — true if exuberance percentile ≥ 90.

### Composite score

Equal-weighted mean of the 9 headline indicators' exuberance percentiles (each 0–100). If an indicator cannot be sourced, drop it from the active set and disclose the count in the Data Used manifest. The composite tier bands are:

| Range | Verdict | What it means |
|---|---|---|
| 80–100 | **Frothy** | Late-stage bull peak signature — 2000 / 2021-style. ≥ 5 of 9 indicators in top decile. |
| 60–80 | **Stretched** | Above historical averages on most axes; below prior peaks. The current GS read (June 2026). |
| 40–60 | **Elevated** | Mild optimism; a couple of axes warm, most neutral. |
| 20–40 | **Neutral** | No edge either way. |
| 0–20 | **Subdued** | Broad pessimism / capitulation — contrarian buy regime. |

**Acceleration note (calibration observation, not a timing call).** Mirroring Citi BMC's "once the score breaks its band it tends to accelerate," crossing from **Stretched → Frothy** (≈ 80) historically precedes faster deterioration than a comparable move at lower bands. State it as a band-crossing observation, never as a forecast — see the [Learning from sell-side institutional research](#learning-from-sell-side-institutional-research) section and the "state read, not timing model" guardrail.

### Historical anchors

The skill must explicitly anchor today's reading against three clean historical peaks plus today, mirroring GS Exhibit 3 columns:

- **Dot-Com peak** (Mar 2000)
- **Post-COVID peak** (Dec 2021)
- **Today**

For each headline indicator, the calibration table shows the exuberance percentile at each anchor. **Historical anchors come from the GS PDF directly when the percentiles are unambiguous** — the script does not need to back-fill 1995 history for every indicator. When the script can compute the historical percentile from a long-history series (Momentum / VIX / put-call / 10Y), it does so; when only a current value is reliably fetchable (AAII / Yale / IPO count / net issuance), the script quotes the GS percentile for the historical columns and computes only the current column directly.

## Learning from sell-side institutional research

The GS Kickstart is the primary analog, but the broader sell-side exuberance literature (GS, Citi, Morgan Stanley, J.P. Morgan, Bernstein) sharpens several blocks. Apply these named moves on top of the 9-indicator core — they deepen the read without adding new data sources.

- **Earnings-led vs multiple-led diagnostic (the call's spine).** Mirror the GS "Evaluating exuberance" core argument — its whole "not yet a systemic top" verdict rests on fwd-EPS being *up more than price* (e.g. fwd-EPS +16% YTD vs index +8% YTD → "rally is earnings-led, not theme-led"). Report fwd-EPS revision % YTD against index price return YTD as an explicit named diagnostic, and label the froth: **earnings-backed = more durable; multiple-driven = more fragile.** Compute it in Step 3 and let it color the verdict — this is the one diagnostic that changes what the composite *means*, not just its level.

- **Flows decomposed by holder type (biggest structural gap).** Mirror the Morgan Stanley *China/HK Flows & Positioning Tracker* and the GS Kickstart flows page: replace the single ICI line with a holder-type table — domestic institutional, retail margin/leverage (FINRA margin debt + put/call as the retail-leverage read), ETF growth-vs-dividend rotation, and equity-futures net positioning where a public proxy exists (foreign-active-vs-passive too, where applicable). Each line carries a percentile-vs-history and a deep-URL source. Per J.P. Morgan *"Positioning Looks Stretched Only in Isolated Pockets,"* express positioning as a single history percentile and then decompose into **crowded pockets vs under-owned pockets** (e.g. mega-cap-AI / leveraged single-stock ETFs crowded vs broad-market underowned) — and frame stretched-but-not-extreme as "buy-the-dip until proven otherwise," not a sell signal.

- **Breadth as cross-sectional DISPERSION, not just % above 200dma.** Mirror J.P. Morgan Quant *"Calm Surface, Violent Undercurrents"*: a quiet index can mask a 10-year-high in single-stock dispersion. Add a **median-stock-vs-index return** and **single-stock realized vol vs index realized vol** read (both derivable from the top-50 SPX members already pulled for the correlation calc). State the insight explicitly when the spread is wide — index flat while the median stock is down is a froth tell that % above 200dma misses.

- **IPO COUNT vs PROCEEDS, and gross vs net-of-buyback issuance.** Mirror the GS nuance: IPO *proceeds* at records but IPO *count* near average, and *net* issuance low because buybacks exceed new supply. Encode both sub-metrics on the corporate-financing leg with their own percentiles so the "supply pressure" flag reflects the count/value divergence rather than a single read — this is what GS uses to say supply pressure is still contained.

- **Region / segment split of the composite.** Mirror Citi's Bear Market Checklist region decomposition (US 11.5 vs Europe 5): add a "where is the froth concentrated" line splitting **mega-cap AI vs the broad market**, so the single US composite isn't read as uniform. Tie concentration to its 2000 benchmark explicitly — quote top-10 weight at *each* historical anchor (GS: today's concentration is high but still *below* 2000), not just today.

- **Forward-path context — the level the Street is underwriting.** Every analog couples the exuberance read to an explicit forward index path. Report the published Street / GS **year-end + 12m SPX point target and the EPS-growth assumption behind it** (sourced via WebSearch with a date), framed as *"the level of exuberance the Street is currently underwriting"* — **explicitly NOT the skill's own forecast** (preserves the "no timing / price call" guardrail and the "analyst's model is not a source" rule; cite GS / consensus, never "our model").

- **Behavioral acceleration rule (calibration observation, not a timing call).** Mirror Citi BMC's memorable one-liners ("once the checklist breaks its band it tends to accelerate"; "when more flags turn red, stop buying the dip"). For this skill's 0–100 composite, carry a one-line note that crossing from **Stretched → Frothy** historically precedes faster deterioration — clearly labeled as a calibration observation, consistent with the "state read, not timing model" guardrail.

- **House idiom — valuation in standard-deviations, gauges with absolute levels.** Quote every valuation in standard-deviations-from-history (and PEG), never a bare multiple — "fwd 12m P/E 22.3x = +3.4 s.d. vs 10y" is the desk idiom and exactly the project's "no absolute threshold without percentile context" rule. Name proprietary gauges explicitly with an absolute level + percentile every time (GS Speculative Trading Indicator, Citi BMC score, MS MSASI); when proxying a proprietary series, say so and show the proxy's own percentile.

## Data sources

### Hard data (no WebSearch required)

| Indicator | Source | Helper |
|---|---|---|
| Momentum factor (3M) | yfinance `MTUM` | `yfinance.download` |
| Put/Call ratio | yfinance `^CPC` (CBOE Total Put/Call) | `yfinance.download` |
| VIX / VIX3M | yfinance `^VIX`, `^VIX3M` | `yfinance.download` |
| 10Y / 2Y / TIPS yields | FRED `DGS10`, `DGS2`, `DFII10` | `indicators.data_fetcher._fetch_fred_range` |
| Fed funds upper | FRED `DFEDTARU` | same |
| Chicago Fed NFCI | FRED `NFCI` | same |
| Atlanta Fed GDPNow | FRED `GDPNOW` | same |
| S&P 500 + EW SPX | yfinance `^GSPC`, `RSP` | `yfinance.download` |
| Factor ETFs | yfinance `MTUM`, `IWD`, `IWF`, `IPO`, `ARKK`, `BUZZ`, `RNMC` | `yfinance.download` |
| Sector ETFs | yfinance `XLK`, `XLF`, `XLY`, `XLP`, `XLV`, `XLI`, `XLE`, `XLB`, `XLU`, `XLRE`, `XLC` | `yfinance.download` |
| Shiller CAPE | multpl.com monthly | inline scraper |
| Multpl trailing PE | multpl.com monthly | inline scraper |
| Multpl S&P 500 dividend yield | multpl.com monthly | inline scraper |

### WebSearch fallback (no clean public series)

The build script flags these as `requires_websearch: true` in the JSON output. The agent then runs WebSearch and patches the JSON before writing the report.

| Indicator | Search query template | Why fallback |
|---|---|---|
| GS Speculative Trading Indicator | `"Speculative Trading Indicator" Goldman Sachs 2026 current` | Proprietary; chart republished monthly in Kickstart |
| S&P 500 52-week market breadth | `S&P 500 stocks within 5% of 52-week high site:wsj.com OR site:bespokepremium.com 2026` | Composite calc is expensive; latest read is widely cited |
| Median S&P 500 stock short interest | `S&P 500 median short interest 2026 FactSet OR FINRA OR Goldman` | FINRA aggregate is monthly; "median" cut is sell-side |
| Yale Stock Market Confidence Index | `Yale Stock Market Confidence Index latest one-year confidence individual` | Yale ICF site has the data but JSON endpoint is unstable |
| AAII bull-bear | `AAII bull bear sentiment latest week percentage` | aaii.com XLS returns 403 since 2025 |
| Number of US IPOs YTD | `Renaissance Capital US IPO count 2026 YTD` | Need annualised current value |
| Net US equity issuance | `SIFMA US equity issuance 2026 quarterly volume` | SIFMA report PDFs require human navigation |
| EPS revision breadth | `FactSet Earnings Insight S&P 500 revision breadth latest` | FactSet PDFs |
| Fed-funds 2026 YE implied | `CME FedWatch year-end 2026 implied fed funds rate` | CME endpoint requires JS |
| GS US FCI level | `Goldman Sachs Financial Conditions Index US 2026 latest` | proprietary |
| Forward 12-month EPS growth (SPX) | `S&P 500 2027 consensus EPS growth FactSet` | sell-side aggregator |
| Street SPX point target (year-end + 12m) | `Goldman Sachs S&P 500 year-end 2026 12-month price target` | forward-path context — "level the Street is underwriting"; cite GS / consensus, never "our model"; **pair the target with the SPX level on the strategist note's date + the implied % move** (`GS 7,200 vs 6,150 @ 2026-05-30 → +17%`), not just vs today — a bare index target with no anchor isn't actionable |
| fwd-EPS revision breadth vs YTD price | `S&P 500 forward EPS revision YTD vs index return 2026` | earnings-led-vs-multiple-led diagnostic |

The build script writes a `_websearch_queue.json` alongside the data JSON. The agent picks it up in Step 2 and resolves each entry.

### Database write rule

**Read-only against `db/indicators.db`.** The skill does not write to any project DB — every cache lives in `oneoff/market_status_<DATE>_*.csv`. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Workflow

### Step 0 — Sanity check the request

Confirm the user wants a *macro / regime* read, not a single-ticker call. If the prompt names a ticker ("is NVDA exuberant?"), redirect to [[take-profit-lab]] or [[company-research]].

If the user wants a *credit-led* under-priced-risk read specifically (HY OAS / VIX-driven), use [[market-complacency]] instead.

### Step 1 — Run the build script

```bash
# As-of today (default)
python3 .claude/skills/market-status/scripts/build_status.py

# Specific date
python3 .claude/skills/market-status/scripts/build_status.py --date 2026-06-07

# Skip the heavy per-constituent breadth + concentration calc (faster)
python3 .claude/skills/market-status/scripts/build_status.py --date 2026-06-07 --quick
```

What it does:
1. Pulls all hard-data indicators (yfinance + FRED + multpl).
2. Computes the 30-year and 10-year percentile ranks per indicator.
3. Writes the headline 9-indicator calibration table (with GS-anchor values for historical columns when reliable; live values for the current column).
4. Renders charts for the GS Kickstart's main exhibits (Momentum + AI overlay, breadth, Speculative Trading proxy, put/call, short interest, IPO count, net issuance, AAII, Yale, FCI, GDP nowcast, VIX, correlation, factor returns, sector returns, top movers).
5. Emits `_websearch_queue.json` with the list of indicators that need WebSearch fallback.
6. Writes a structured JSON summary to `oneoff/market_status_<DATE>_summary.json`.

Outputs (idempotent — same date → same outputs):

- `oneoff/market_status_<DATE>_indicators.csv` — per-indicator current value, percentile, decile, top-decile flag.
- `oneoff/market_status_<DATE>_calibration.csv` — 9-row calibration (Dot-Com / 2021 / Current) percentile table.
- `oneoff/market_status_<DATE>_panel.csv` — broader dashboard panel (FCI / NFCI / GDP / VIX / etc.) current values.
- `oneoff/market_status_<DATE>_top_movers.csv` — weekly top/bottom 5 SPX movers.
- `oneoff/market_status_<DATE>_sectors.csv` — sector ETF 1W / 1M / 3M / 12M / YTD returns.
- `oneoff/market_status_<DATE>_summary.json` — composite score, tier, active indicator count, output paths.
- `oneoff/market_status_<DATE>_websearch_queue.json` — fallback queue for the agent.
- `reports/charts/market_status_<DATE>_*.png` — 12-15 charts.

### Step 2 — Resolve the WebSearch queue (the agent's job)

The agent (Claude in this conversation) reads `_websearch_queue.json` and runs WebSearch for each entry. For each result, the agent:

1. Captures a current numerical value with a source URL and a publication date.
2. Patches `oneoff/market_status_<DATE>_summary.json` — fills `value`, `percentile`, `source_url`, `source_date` for that indicator.
3. Re-computes the composite if any of the headline 9 had been missing.

**Do not skip this step.** A composite computed only from the hard-data indicators understates the exuberance score (because the WebSearch indicators tend to be among the most stretched in a Frothy regime). The Data Used manifest must record every WebSearch citation.

### Step 3 — Inspect for surprises

Before writing the report, scan the calibration table and the broader panel for:

1. **Cross-category divergence** — e.g. share-price indicators all in the top decile but corporate-sentiment indicators (IPO count, net issuance) mid-decile. The narrative blocks must call this out.
2. **A single indicator carrying the composite** — if the composite is 78 but 8 of 9 indicators are mid-50s and one is 100, the composite is misleading.
3. **Stale data on a WebSearch indicator** — if the WebSearch result is older than 30 days, prefer a more recent secondary source.
4. **Earnings-led vs multiple-led diagnostic** — compute fwd-EPS revision % YTD against index price return YTD (the GS "rally is earnings-led, not theme-led" check). Label the froth: earnings-backed (EPS ≥ price) = more durable; multiple-driven (price ≫ EPS) = more fragile. This colors the verdict's *meaning*, not just its level — see the [Learning from sell-side institutional research](#learning-from-sell-side-institutional-research) section.

### Step 4 — Write the report

Save to `reports/market-status/market_status_<YYYY-MM-DD>.md`. Target 3,000–5,000 words plus 10–15 charts plus 3 tables. Structure mirrors the GS Kickstart:

1. **Exuberance Verdict** — single bold blockquote (≤ 200 words). First line is the verdict ("**Stretched — exuberance score 68 / 100, 86th percentile vs history since 1995**"). Then 2-3 sentences naming the most-stretched and most-contra indicators with absolute levels. Then one line of action (3-5 verbs). Mirror Citi-BMC and GS-Kickstart "summary box" style.
   - **Bull-market-ending triggers checklist** (mini-table, exempt from the ≤ 200-word prose limit — like Figure 1). Mirror the GS US Weekly Kickstart "Evaluating exuberance" lead-in and Citi's Bear Market Checklist: a 3-row table checking the three classic termination triggers, each marked **Not-yet / Marginal / Flagged** with its sourced metric: (a) **fundamentals/earnings weakening** (fwd-EPS revision breadth turning negative); (b) **surge in new equity supply** (IPO proceeds + net-of-buyback issuance); (c) **Fed / financial-conditions tightening** (NFCI + fed-funds path). GS's June-2026 read marks all three only "marginally elevated → not yet a systemic top" — the checklist makes the verdict a checklist, not just a score.
   - **Counter-signal line** (mandatory, one sentence). Mirror Citi BMC's "what is NOT yet flagged" and GS's note that median short interest sits at a multi-decade *high* (lots of money still short = not full euphoria): name the headline indicators currently in the bottom / mid decile so the read is never one-sided. Reinforces the existing "never assert this looks like 2000 / 2021" guardrail.
2. **Figure 1. Kickstart-style 9-indicator calibration table** — exactly the layout of GS Exhibit 3. Columns: Dot-Com Bubble / 2021 / Current. Rows grouped by Share-prices / Trading-activity / Investor-sentiment / Corporate-sentiment. Cells coloured: red if exuberance pct ≥ 80, amber 60–80, green ≤ 30, plain otherwise. Cite the public source URL inline per row.
3. **§ Share-price action** — narrative paragraph + Momentum chart (`*_momentum.png`) + Breadth chart (`*_breadth.png`). 200-300 words.
4. **§ Trading activity** — narrative paragraph + Speculative Trading proxy chart + Put/Call chart + Short-interest chart. 300-400 words.
5. **§ Investor sentiment** — narrative paragraph + AAII chart + Yale chart + GS Sentiment Indicator chart. 300-400 words.
6. **§ Corporate sentiment** — narrative paragraph + IPO chart + Net-issuance chart. 200-300 words.
7. **§ Macro & cross-asset panel** — single block with sub-sections for: 10Y + fed-funds path / GDP / VIX & VVIX / **flows decomposed by holder type** (institutional / retail margin-leverage / ETF growth-vs-dividend / futures net positioning — mirror the MS *China/HK Flows & Positioning Tracker*, with crowded-vs-under-owned pockets per JPM *"Stretched Only in Isolated Pockets"*) / breadth incl. **cross-sectional dispersion** (median-stock-vs-index, single-stock vs index realized vol — JPM *"Calm Surface, Violent Undercurrents"*) & top-10 concentration **quoted at each historical anchor** / S&P 500 P/E + ERP **in standard-deviations-from-history** / sector returns + factor returns + top movers. 600-900 words. See the [Learning from sell-side institutional research](#learning-from-sell-side-institutional-research) section.
8. **§ Historical anchor — "What does today look like?"** — a short close that names 2-3 historical analogs (with their forward 12-month SPX returns) and explicitly states the calibration limit ("the dashboard described the regime N of N historical times; it predicted the path 0 of N times").
   - **Forward-path context line** — report the published Street / GS year-end + 12m SPX point target and the EPS-growth assumption behind it (WebSearch with a date), framed as *"the level of exuberance the Street is currently underwriting"* — **explicitly NOT the skill's own forecast**. Cite GS / consensus, never "our model".
   - **One-line earnings-led note** — restate the Step-3 fwd-EPS-vs-price diagnostic ("earnings-backed froth is more durable than multiple-driven froth").
   - **Paired 利好 / 利空 (catalysts vs downside-risks) bullet block** — mirror every GS regional Kickstart's closing pair: a compact, scannable two-column set of bullets, each **dated and carrying a deep-URL source** (satisfies paragraph-level citation). Replaces diffuse prose with the desk format.
9. **`## Data Used / 数据来源清单`** — manifest of every source URL + the WebSearch citations.

### Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — what an exuberance indicator actually measures (how the GS Speculative Trading Indicator is constructed, what the CBOE equity put/call ratio captures, how net-of-buyback equity issuance is derived, how a momentum factor is built), a market-structure concept, an unfamiliar positioning measure, or any mechanism behind a number in the dashboard — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### Step 5 — Verify and clean up

- Spot-check ≥ 3 numbers in the report against the indicators CSV.
- Confirm every percentile in the calibration table matches the script's output.
- Confirm every WebSearch citation has both a URL and a publication date.
- Stop any test servers used during chart rendering.
- Commit and push per the project's standard workflow (`fix:` / `feat:` Conventional Commits, no Co-authored-by footer).

## Output Format (mandatory blocks)

Mirror the GS Kickstart's structure precisely — the report is the daily-scan artifact, and matching the format institutional readers already know is the point.

Mandatory blocks, in order:

1. **Exuberance Verdict** (blockquote, ≤ 200 words) + **bull-market-ending triggers mini-table** (fundamentals / new-supply / Fed, each Not-yet / Marginal / Flagged) + **counter-signal line** (≥ 1 indicator in the bottom / mid decile)
2. **`## Figure 1. Exuberance — 9-indicator calibration` (HTML table, raw HTML — not markdown with emoji dots)**
3. **`## Share-price action`** (narrative + 2 charts)
4. **`## Trading activity`** (narrative + 3 charts)
5. **`## Investor sentiment`** (narrative + 3 charts)
6. **`## Corporate sentiment`** (narrative + 2 charts)
7. **`## Macro & cross-asset panel`** (sub-sections + 4-6 charts)
8. **`## Historical anchor`** (short close)
9. **`## Data Used / 数据来源清单`**

### Figure 1 styling

Like the [[market-complacency]] Figure 2 BMC table: raw HTML with inline-style cell backgrounds — not markdown with emoji dots. Required class palette:

- `.ms-red` — `background: #f4a8a8; color: #5a0000` (exuberance pct ≥ 80)
- `.ms-amber` — `background: #ffd17a; color: #5a3300` (60–80)
- `.ms-green` — `background: #b6e3b6; color: #1a4d1a` (≤ 30 — counter-signal: bearish positioning)
- `.ms-now` — `border-left: 2px solid #888` (column separator on the Now column)

Each indicator row gets a markdown link to its public source.

### Chart styling (mandatory — applies to every chart-producing call)

Per the global CLAUDE.md rules:

1. Every chart has a source annotation in the bottom margin.
2. X-axis is clipped to the intersection of all plotted series' valid data — not the union.
3. Latest data point must cover "now" — spot-check before saving.
4. For derived charts, plot the source/component series in the same chart.
5. Multi-series charts: `first = max(d.min() for d in all_series); last = min(d.max() for d in all_series)`.

### What NOT to include

Forbidden blocks (rejected in prior similar skill iterations):

- ❌ Long composite-decomposition tables — implicit in Figure 1.
- ❌ Multiple postscript / version-history blocks — those belong in git commit messages.
- ❌ A separate "Action Implications" prose section — the verdict line carries the action.
- ❌ "What Would Invalidate This Read" multi-paragraph block — collapse into a 2-sentence note in the Historical anchor section.
- ❌ Per-chart narrative paragraphs between charts within the same section — keep the narrative at the section opener.
- ❌ The composite score quoted as a single number without the per-indicator breakdown.

## Guardrails

- **Never call the Claude API or any LLM API.** Per [`CLAUDE.md`](../../../CLAUDE.md): the agent (this conversation) does the analysis directly. The script is pure pandas + yfinance + urllib.
- **Never write to any `db/*.db` file.** Read-only against `db/indicators.db`. New indicator caches live in `oneoff/`.
- **Never silently drop a headline-9 indicator from the composite without disclosure.** If GS Speculative Trading proxy fails AND WebSearch returns no result, the report must say "composite computed from 8 of 9 GS indicators" in the verdict and the Data Used block.
- **Never assert "this looks like 2000 / 2021".** The calibration table does that work — let the reader pattern-match. Naming a specific historical analog in the verdict is over-confident.
- **Always carry the counter-signal line.** The Verdict must include one sentence naming the headline indicators currently in the bottom / mid decile (the "not yet flagged" evidence — mirror Citi BMC and GS's multi-decade-high short-interest note). A one-sided read that lists only the stretched indicators is rejected.
- **Never use absolute thresholds without percentile context.** "VIX is 18" means nothing without "which is the 32nd percentile of the last 10 years". The indicator tables must always carry both.
- **Stale data — explicit removal rule.** Same as market-complacency: if any used multpl page is more than 60 days stale, the indicator is removed from the active set with re-normalization and a note. Every report run must spot-check the publication dates.
- **No "Source: our model" anywhere.** Cite the script path for derived calcs, the underlying FRED / yfinance / multpl / Yale / AAII / Renaissance / SIFMA URLs for the inputs.
- **Never claim the dashboard predicts the *timing* of a regime turn.** It is a state read. Exuberance can persist for quarters — GS quotes Greenspan's "irrational exuberance" speech of Dec 1996 as preceding the Dot-Com peak by more than 3 years.
- **WebSearch citations must include the publication date.** A bare URL without a date is not a citation. The Data Used manifest lists each WebSearch result as `[Title, YYYY-MM-DD](URL)`.
- **Numerical accuracy:** per CLAUDE.md, every number in a paragraph must trace to a URL cited in that same paragraph where the number literally appears.

## Output location

Save to `reports/market-status/market_status_<YYYY-MM-DD>.md` under the project root (create the directory if missing — first report establishes it). The viewer at `http://localhost:5001/reports` will surface it under a new "MARKET-STATUS" type (or as "OTHER" until the viewer's bucket map is updated).

Supplementary deliverables:

- Charts: `reports/charts/market_status_<DATE>_*.png` + `*.html` (interactive Plotly time-series).
- Build script: `.claude/skills/market-status/scripts/build_status.py` (reusable via `--date YYYY-MM-DD`).
- Generated CSVs / JSON: `oneoff/market_status_<DATE>_*.{csv,json}`.

### Update-in-place rule

One report per date. If `reports/market-status/market_status_<YYYY-MM-DD>.md` already exists for today's date, update it in place rather than creating a parallel copy. Across dates, keep separate files — the historical sequence of verdicts is itself useful context.

## Related skills

- [[market-complacency]] — credit-led under-priced-risk read; complement, not replacement.
- [[take-profit-lab]] — single-ticker exit discipline; takes the macro exuberance read as one input.
- [[sector-overview]] — sub-sector stress.
- [[idea-generation]] — turns a "frothy" read into specific short / hedge candidates.
- [[portfolio-decision]] — final position rating; uses the verdict as one macro input.

## Source PDF reference

Goldman Sachs US Weekly Kickstart, "Evaluating exuberance", 5 June 2026 (Ben Snider et al.) — used as the indicator catalog and the 2000 / 2021 percentile anchor source. Reproduction restricted; do NOT redistribute the PDF; do cite the issue date and lead author in every report run.
