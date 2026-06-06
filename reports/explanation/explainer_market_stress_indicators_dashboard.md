# Market Stress Indicators — What They Represent and When They're Useful

*A field guide to the 14 indicators on the `/indicators/` dashboard. Source: [indicators/data_fetcher.py](../../indicators/data_fetcher.py) (catalogue + thresholds), [indicators/app.py](../../indicators/app.py) (Flask blueprint). Last updated 2026-06-06.*

---

## What this dashboard is for

The `/indicators/` page is a **market-stress monitor** — a single screen that answers one question: *is the financial system calm, cautious, or under stress right now?* It tracks 14 series across four families — **Liquidity**, **Credit**, **Volatility**, and **Cross-Asset** — refreshing from yfinance (and FRED for credit spreads) on a 15-minute cache, with a 45-day sparkline behind each tile.

Six of the 14 indicators carry hard thresholds and light up a **traffic-light dot** (green → yellow → red); the other eight are *context* indicators with no threshold (grey/neutral) that you read by direction and in combination with the rest. The scoring is deliberately simple — each thresholded indicator declares a `direction` ("up" = higher is worse, e.g. VIX; "down" = lower is worse, e.g. the yield-curve slope) plus a `caution` and `stress` level, and `compute_signal()` maps the latest value onto green/yellow/red ([indicators/data_fetcher.py](../../indicators/data_fetcher.py)).

The point of putting them on one screen is that **no single indicator is reliable alone** — credit, volatility, funding, and cross-asset prices each see a different facet of the same stress, and they tend to confirm (or contradict) one another. The "how to read regimes" section at the end is where the dashboard earns its keep.

---

## Liquidity — the price and shape of money

### 3M T-Bill Yield (`^IRX`) · *context, no threshold*

**What it represents.** The yield on a 3-month US Treasury bill is the cleanest read on the *front end* of the curve. Because a 3-month bill matures so soon, its yield tracks the market's expectation of the average Fed funds rate over the next quarter, plus a small premium for bill supply and demand. Rising = the market expects tighter policy (or there's a scramble for cash); falling = easing expectations or a flight to the safest possible asset.

**When it's useful.** Two cases stand out. First, **policy-cycle tracking**: across the 2022–23 hiking cycle the 3M bill climbed from near zero to above 5% as the Fed tightened at its most aggressive pace in decades ([CNBC, 2022-09-01](https://www.cnbc.com/amp/2022/09/01/forex-markets-currencies-yen-federal-reserve-interest-rate-hikes.html)). Second, and more subtly, **debt-ceiling stress**: in the May 2023 standoff, Treasury bills maturing right around the projected early-June "X-date" carried a visible default-risk premium versus neighbouring maturities — investors demanded extra yield to hold the paper most at risk if Congress failed to act ([Bloomberg, 2023-05-22](https://www.bloomberg.com/news/features/2023-05-22/debt-ceiling-deadline-tracker-the-grow-fear-premium-in-treasury-bill-markets)) — and the distortion unwound once Treasury flagged a June 5 X-date and a deal was struck ([CNBC, 2023-05-26](https://www.cnbc.com/2023/05/26/treasury-says-it-wont-run-out-money-until-at-least-june-5-buying-time-for-debt-ceiling-talks.html)). When the 3M bill moves for reasons *other* than the Fed, that's the signal.

### 10Y – 3M Spread (`^TNX − ^IRX`) · *threshold: yellow ≤ 0.5pp, red ≤ 0.0pp (inverted)*

**What it represents.** This is the slope of the yield curve — the 10-year yield minus the 3-month bill — and it is the single most-watched recession indicator in macro. The logic: the 3-month bill tracks current policy, while the 10-year embeds the market's long-run growth and inflation expectations, so a *negative* spread means investors expect the Fed to be cutting rates well below today's level — i.e. they're forecasting a downturn ([Federal Reserve Bank of St. Louis, 2023-09](https://www.stlouisfed.org/on-the-economy/2023/sep/what-probability-recession-message-yield-spreads)).

**When it's useful.** The New York Fed publishes a monthly recession-probability series built on exactly this spread — the Estrella–Mishkin probit model, `P(recession) = Φ(−0.5333 − 0.6629 × spread)`, from their 1996 study ([NY Fed, "The Yield Curve as a Predictor of U.S. Recessions"](https://www.newyorkfed.org/medialibrary/media/research/current_issues/ci2-7.pdf)). An inversion of the 10Y–3M spread has preceded essentially every US recession since the 1970s, with a lead time that varies from roughly 6 to 24 months. It is a **slow-burn, leading** indicator — it tells you the regime is fragile, not that the break is today. The 2022–2024 inversion was the deepest and longest on record, which is precisely why it must be read alongside the fast-moving credit and volatility gauges rather than in isolation.

---

## Credit — is the bond market repricing default?

### HY Spread / OAS (FRED `BAMLH0A0HYM2`) · *threshold: yellow ≥ 4.5%, red ≥ 6.5%*

**What it represents.** The ICE BofA US High Yield Option-Adjusted Spread is the extra yield investors demand to hold below-investment-grade ("junk") corporate bonds over a matched Treasury curve, adjusted for embedded options. It is the **single cleanest read on credit stress** — when investors fear defaults, they demand more compensation, and the spread widens fast.

**When it's useful.** HY OAS is the canonical "credit cracks before equities" gauge. It set its **all-time record of 21.82% in December 2008** during the Global Financial Crisis ([Trading Economics / ICE BofA via FRED](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-high-yield-option-adjusted-spread-fed-data.html)), and spiked above 10% in late March 2020 during the COVID crash ([FRED: BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)). For context on how compressed "calm" looks, the same series sat at just 2.75% in June 2026 ([Trading Economics](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-high-yield-option-adjusted-spread-fed-data.html)). The dashboard's 4.5% caution / 6.5% stress thresholds bracket the zone where HY spreads stop being benign and start signalling a genuine credit event — a level reached in 2008, 2011 (euro crisis), 2015–16 (energy bust), and March 2020.

### IG Spread / OAS (FRED `BAMLC0A0CM`) · *threshold: yellow ≥ 1.3%, red ≥ 2.0%*

**What it represents.** The investment-grade counterpart — the OAS on BBB-and-better US corporate bonds. IG spreads are far tighter and slower-moving than HY, so when *they* widen materially, stress has spread from the speculative fringe into the core of the credit market, hitting even the highest-quality issuers.

**When it's useful.** IG OAS is the "this is now systemic" confirmation. Its **all-time high was 6.56% in December 2008**, versus just 0.74% in the calm of May 2026 ([Trading Economics / ICE BofA](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-corporate-master-option-adjusted-spread-fed-data.html)). In March 2020 the dislocation reached even pristine credits: AAA-rated IG fund spreads jumped from 0.92% at end-February to 2.44% by March 20, and BBB spreads leapt from 1.67% to 4.80% by March 23 ([Investment Company Institute](https://www.ici.org/viewpoints/22-view-bondfund-survey-4)). When the dashboard's IG tile turns yellow/red *at the same time* as HY, you are no longer looking at an idiosyncratic junk-bond problem — the whole corporate-credit channel is seizing.

### HY Bond ETF (`HYG`) and IG Bond ETF (`LQD`) · *context, no threshold*

**What they represent.** HYG (iShares iBoxx High Yield) and LQD (iShares iBoxx Investment Grade) are the most-liquid, exchange-traded proxies for the junk and IG bond markets. Their value on the dashboard is that they trade *continuously and intraday*, whereas the underlying bonds trade by appointment — so an ETF that gaps lower, or trades at a **discount to its net asset value**, is an early, real-time tell that dealers can't absorb the selling.

**When they're useful.** The defining episode is March 2020. As the corporate-bond market froze, HYG and LQD swung to unusual discounts to NAV, and the dislocation was severe enough that the Federal Reserve took the unprecedented step of buying corporate-bond ETFs directly. The **Secondary Market Corporate Credit Facility (SMCCF), announced March 23, 2020**, was authorised to purchase IG ETFs such as LQD; on April 9 the Fed expanded it to include high-yield ETFs such as HYG; and ETF buying began May 12, 2020 ([Federal Reserve — SMCCF](https://www.federalreserve.gov/monetarypolicy/smccf.htm); [NY Fed — SMCCF](https://www.newyorkfed.org/markets/secondary-market-corporate-credit-facility); [ETF.com, 2020](https://www.etf.com/sections/features-and-news/federal-reserve-will-buy-junk-bond-etfs)). When HYG/LQD fall sharply *and* the credit-spread tiles are widening, the two are confirming the same stress from different angles — one from dealer quotes, one from index marks.

---

## Volatility — what the options market is paying for protection

### VIX (`^VIX`) · *threshold: yellow ≥ 20, red ≥ 30*

**What it represents.** The Cboe Volatility Index is the market's expectation of S&P 500 volatility over the next 30 days, implied from the prices of SPX options. It is the canonical "fear gauge": calm markets sit in the low-to-mid teens, a reading above 20 marks elevated stress, and above 30 marks acute stress.

**When it's useful.** VIX is the fast, coincident measure of equity fear — it tells you the panic is *now*. Its **highest-ever closing value, 82.69, was set on March 16, 2020** during the COVID crash ([CNBC, 2020-03-16](https://www.cnbc.com/2020/03/16/wall-streets-fear-gauge-hits-highest-level-ever.html); [VIX — Wikipedia](https://en.wikipedia.org/wiki/VIX)). That close edged past the GFC's closing peak of **80.74 on November 21, 2008**, though the **all-time intraday high of 89.53 (October 24, 2008)** still stands — March 16, 2020 reached 83.56 intraday ([VIX — Wikipedia](https://en.wikipedia.org/wiki/VIX); [Macroption](https://www.macroption.com/vix-all-time-high/)). More recently, VIX is also useful for catching *fast, mechanical* shocks: on **August 5, 2024** it spiked above 60 intraday — a level not seen since the COVID crash — as a Bank of Japan policy shift triggered a violent unwind of yen-funded carry trades, with Japan's TOPIX falling 12% that day before the VIX receded over the following sessions ([BIS Bulletin No. 90, 2024](https://www.bis.org/publ/bisbull90.pdf)). The contrast between 2020 (a sustained crisis) and 2024 (a one-day spike that quickly faded) is exactly why you read the VIX *level* together with the term-structure indicator below.

### VVIX (`^VVIX`) · *threshold: yellow ≥ 100, red ≥ 120*

**What it represents.** VVIX is the "volatility of volatility" — the implied volatility of *VIX options themselves*, computed with the same methodology as VIX but applied to VIX option prices. In plain terms: VIX measures fear in stocks; VVIX measures uncertainty about *how fearful the market will become* — i.e. demand for tail-hedges on volatility itself.

**When it's useful.** In calm markets VVIX generally trades in the rough vicinity of 80–100; the dashboard flags readings above 100 (caution) and above 120 (stress) as elevated fear about future volatility moves ([indicators/data_fetcher.py](../../indicators/data_fetcher.py)). Extreme prints are rare and cluster on genuine dislocations — VVIX spiked far above its normal range during both the February 2018 "Volmageddon" and the March 2020 COVID crash ([Cboe — VVIX dashboard](https://www.cboe.com/us/indices/dashboard/vvix/)). VVIX is most useful as a *leading* tell within the vol complex — it can spike before VIX does, because sophisticated players bid up VIX-option protection in anticipation of a volatility event. A high VVIX with a still-moderate VIX is a warning that the market itself doesn't trust the calm.

### VIX Term Slope (`^VIX9D ÷ ^VIX3M`) · *threshold: yellow ≥ 1.0, red ≥ 1.15*

**What it represents.** This ratio compares 9-day implied vol (VIX9D) to 3-month implied vol (VIX3M). In normal, calm markets the curve is in **contango** — near-term vol is *lower* than longer-term vol, so the ratio sits below 1.0. When the ratio rises above 1.0 the curve has flipped into **backwardation**: traders are paying *more* for immediate protection than for protection three months out, which only happens when they fear something acute and imminent. It is one of the sharpest "panic is here *today*" signals on the board.

**When it's useful.** The textbook case is **February 5, 2018 ("Volmageddon")**, when the VIX more than doubled intraday — from ~18 at the open to above 37 at the close, the largest single-day VIX increase ever ([Six Figure Investing](https://www.sixfigureinvesting.com/2019/02/what-caused-the-february-5th-2018-volatility-spike-xiv-termination/)). The front end of the VIX-futures curve gapped violently into backwardation, which is exactly what destroyed the short-volatility products that were structurally long contango/"roll yield": Credit Suisse's **XIV note lost ~97% of its value that day and was liquidated**, with holders paid a final value on February 15, 2018 ([CFA Institute — "Volmageddon and the Failure of Short Volatility Products"](https://rpc.cfainstitute.org/research/financial-analysts-journal/2021/volmageddon-failure-short-volatility-products)). A term slope above 1.0–1.15 is the dashboard's way of flagging that the options market has stopped pricing a gentle mean-reversion and started pricing a near-term shock.

---

## Cross-Asset — context for *what kind* of stress this is

These five have no thresholds. They don't generate a red/green signal on their own; you read them by direction and, crucially, in combination — because the *pattern* across them tells you whether a sell-off is a growth scare, a funding crisis, an inflation shock, or something US-specific.

### S&P 500 (`SPY`)
The primary risk-asset benchmark and the thing every other indicator is ultimately trying to explain. Falling SPY with the credit and vol tiles lit is a confirmed risk-off; falling SPY with credit calm is more likely a valuation/rotation move than a systemic one.

### 10Y Treasury Yield (`^TNX`)
Long-term rates. Rising can mean two opposite things — tightening/inflation fear, or growth optimism — which is why it's context, not a signal. The *tell* is what it does relative to equities and the dollar: yields falling hard alongside a stock sell-off is the classic flight-to-safety; yields *rising* into a sell-off (as in 2022) is the more dangerous "no place to hide" regime where bonds stop hedging stocks.

### US Dollar (`DX-Y.NYB`, DXY)
The dollar index is the world's funding-stress barometer. Because so much global debt is dollar-denominated, a scramble for dollars *is* a crisis. Two illustrative episodes: in **March 2020** the global "dash for cash" drove such acute dollar-funding strains that the Fed re-activated and expanded central-bank swap lines on March 15, 2020 and added the FIMA repo facility on March 31 ([NY Fed — Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/2020/05/have-fed-swap-lines-reduced-dollar-funding-strains-during-the-covid-19-outbreak/); [ECB Economic Bulletin, 2020](https://www.ecb.europa.eu/press/economic-bulletin/focus/2020/html/ecb.ebbox202005_01~4a2c044d31.en.html)); and in **2022** the dollar climbed to a 20-year high as the Fed out-hiked its peers and the euro slid toward parity ([CNBC, 2022-09-01](https://www.cnbc.com/amp/2022/09/01/forex-markets-currencies-yen-federal-reserve-interest-rate-hikes.html)). A rising DXY *during* a sell-off confirms a risk-off / funding-stress regime.

### Gold (`GLD`)
The classic safe-haven and inflation/debasement hedge. Gold rising during a risk-off tells you the stress has a monetary or geopolitical character rather than a pure-growth one. Gold crossed **$2,000/oz during the 2020 pandemic**, then went on a historic run — breaking **$3,000 on March 14, 2025** and **$4,000 in October 2025**, driven by central-bank buying and safe-haven demand ([World Gold Council — gold hits $3,000](https://www.gold.org/goldhub/gold-focus/2025/03/you-asked-we-answered-gold-hits-3000-what-comes-next); [World Gold Council — gold hits $4,000](https://www.gold.org/goldhub/gold-focus/2025/10/gold-hits-us4000oz-trend-or-turning-point)). The diagnostic combination: rising gold *and* a falling dollar points to a US-specific or debasement worry; rising gold *and* a rising dollar points to broad geopolitical fear.

### WTI Crude Oil (`CL=F`)
A real-time proxy for global growth and demand. Collapsing oil signals demand destruction; spiking oil signals a supply/inflation shock. The most extreme demonstration of oil-as-demand-signal: on **April 20, 2020 the front-month (May) WTI contract closed at −$37.62 a barrel** — falling $55.90 on the day, the first negative print in history — as collapsing pandemic demand met full storage tanks at the Cushing, Oklahoma delivery point ([Congressional Research Service](https://www.congress.gov/crs_external_products/IN/PDF/IN11354/IN11354.1.pdf); [U.S. EIA](https://www.eia.gov/todayinenergy/detail.php?id=46336)). Falling oil alongside falling equities and a rising dollar is the signature of a global demand contraction.

---

## Putting it together — reading the regime

The dashboard's value is in the **joint pattern**, not any single dot. A few canonical reads:

1. **Credit *and* volatility red at once = a genuine risk-off.** HY OAS through 6.5% *with* VIX above 30 is the highest-conviction "this is a real crisis" combination on the board (2008, March 2020). Either one alone is a warning; both together is the event.

2. **Credit usually warns before volatility confirms.** HY/IG spreads tend to widen *ahead* of the equity-vol spike — credit desks reprice default risk before the index options fully catch up. A yellow HY OAS with a still-calm VIX is the dashboard telling you to watch for the vol catch-up.

3. **The term slope is the "today" tell.** VIX *level* tells you fear is elevated; the **VIX9D/VIX3M ratio flipping above 1.0 (backwardation)** tells you the fear is *acute and imminent*. The cleanest panic signature is a high VIX **and** an inverted term structure (Feb 2018, March 2020) — versus a high VIX in contango, which is more often a fast spike that mean-reverts (much of the August 5, 2024 move collapsed by the close).

4. **VVIX can lead the whole vol complex.** A VVIX spike above 120 while VIX is still moderate means hedgers are pre-positioning for a volatility event — treat it as an early warning, not a coincident one.

5. **Cross-asset tells you *what kind* of stress.** Same equity sell-off, very different regimes:
   - **Rising DXY + falling oil + falling gold** → a global growth scare / dollar-funding squeeze (March 2020 in its first, "dash-for-cash" phase).
   - **Falling DXY + rising gold** → a US-specific, monetary, or debasement worry rather than a flight *into* dollars.
   - **Rising 10Y yield *into* the sell-off** → the dangerous "stocks and bonds down together" regime (2022) where Treasuries stop hedging equities.

6. **Liquidity is the slow clock; credit and vol are the fast clocks.** An inverted **10Y–3M curve** can flag a fragile regime 6–24 months ahead of trouble, but it won't tell you the day. When the slow clock (inverted curve) and the fast clocks (HY OAS widening, VIX rising, term slope inverting) align, that's the dashboard's strongest aggregate signal.

---

## Quick reference

| Indicator | Family | What it measures | Dashboard signal | Calm vs. stress | Marquee example |
|---|---|---|---|---|---|
| 3M T-Bill (`^IRX`) | Liquidity | Front-end funding cost / Fed expectations | context | tracks policy; spikes near debt-ceiling X-dates | 2023 debt-ceiling bill premium |
| 10Y–3M Spread | Liquidity | Yield-curve slope; recession model input | red ≤ 0.0pp (inverted) | positive = normal; negative = recession signal | inverted before 2001, 2008; 2022–24 |
| HY OAS (`BAMLH0A0HYM2`) | Credit | Junk-bond default premium | red ≥ 6.5% | ~2.75% (Jun 2026) vs 21.82% (Dec 2008) | GFC record 21.82% |
| IG OAS (`BAMLC0A0CM`) | Credit | High-grade credit premium | red ≥ 2.0% | ~1% calm vs 6.56% (Dec 2008) | March 2020 BBB → 4.80% |
| HYG / LQD | Credit | Tradeable junk / IG ETF proxies | context | discount-to-NAV = dealer stress | Fed SMCCF bought both, 2020 |
| VIX (`^VIX`) | Volatility | 30-day S&P implied vol ("fear gauge") | red ≥ 30 | teens = calm; >30 = acute | record close 82.69 (Mar 16 2020) |
| VVIX (`^VVIX`) | Volatility | Vol-of-vol (uncertainty about VIX) | red ≥ 120 | ~80–100 calm; >120 extreme | far above range, 2018 & 2020 |
| VIX Term Slope | Volatility | VIX9D ÷ VIX3M (curve shape) | red ≥ 1.15 | <1 contango (calm); >1 backwardation | Feb 2018 "Volmageddon" |
| SPY | Cross-Asset | Equity benchmark | context | the thing being explained | — |
| 10Y Yield (`^TNX`) | Cross-Asset | Long rates | context | direction vs stocks/dollar matters | rose *into* the 2022 sell-off |
| DXY | Cross-Asset | Dollar / global funding stress | context | rising in sell-off = funding stress | 20-year high in 2022 |
| Gold (`GLD`) | Cross-Asset | Safe-haven / debasement hedge | context | rising = monetary/geopolitical fear | $3,000 (Mar 2025), $4,000 (Oct 2025) |
| WTI (`CL=F`) | Cross-Asset | Growth / demand proxy | context | falling = demand contraction | −$37.62 (Apr 20 2020) |

---

<details>
<summary>Verification log — 2026-06-06</summary>

Numbers spot-checked against the cited URL that carries them (string-match where the source was fetchable):

- **VIX 82.69 close, 2020-03-16** — ✓ string-matches [CNBC](https://www.cnbc.com/2020/03/16/wall-streets-fear-gauge-hits-highest-level-ever.html) and [Wikipedia: VIX](https://en.wikipedia.org/wiki/VIX) ("closed at 82.69").
- **VIX intraday all-time high 89.53 (2008-10-24); intraday 83.56 (2020-03-16); closing record 80.74 (2008-11-21)** — ✓ WebFetch-confirmed on [Wikipedia: VIX](https://en.wikipedia.org/wiki/VIX) (all three quoted verbatim) / [Macroption](https://www.macroption.com/vix-all-time-high/).
- **HY OAS record 21.82% (Dec 2008); 2.75% (Jun 2026)** — ✓ WebFetch-confirmed on [Trading Economics / ICE BofA](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-high-yield-option-adjusted-spread-fed-data.html). COVID peak softened to "above 10%" (qualitative), sourced to the [FRED series](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) — FRED 403s automated fetch, so the precise ~10.9% daily peak was *not* re-verified and the precise decimal was dropped.
- **IG OAS record 6.56% (Dec 2008); 0.74% (May 2026)** — ✓ WebFetch-confirmed on [Trading Economics / ICE BofA](https://tradingeconomics.com/united-states/bofa-merrill-lynch-us-corporate-master-option-adjusted-spread-fed-data.html). **AAA 0.92→2.44% (Mar 20 2020); BBB 1.67→4.80% (Mar 23 2020)** — ✓ curl string-match on [ICI](https://www.ici.org/viewpoints/22-view-bondfund-survey-4).
- **SMCCF announced 2020-03-23; HY ETFs added 2020-04-09; ETF buying began 2020-05-12** — sourced to [Fed](https://www.federalreserve.gov/monetarypolicy/smccf.htm) / [NY Fed](https://www.newyorkfed.org/markets/secondary-market-corporate-credit-facility) / [ETF.com](https://www.etf.com/sections/features-and-news/federal-reserve-will-buy-junk-bond-etfs) (per search summaries; dates widely documented, not individually re-fetched).
- **Aug 5 2024: VIX above 60 intraday; TOPIX −12%; yen-carry unwind; VIX then receded** — ✓ PDF string-match on [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.pdf) ("VIX spiked to levels above 60"; "On Monday 5 August the TOPIX lost 12%"). **Correction:** an earlier draft attributed "65 intraday / +180% / closed ~38 / BoJ +15bp Jul 31 / USD-JPY 149.94→143.89" to BIS — *none of those figures appear in the BIS bulletin* and were removed.
- **Volmageddon, Feb 5 2018: VIX ~18→>37 (largest single-day jump); XIV −97%, liquidated, final value Feb 15 2018** — sourced to [Six Figure Investing](https://www.sixfigureinvesting.com/2019/02/what-caused-the-february-5th-2018-volatility-spike-xiv-termination/) / [CFA Institute](https://rpc.cfainstitute.org/research/financial-analysts-journal/2021/volmageddon-failure-short-volatility-products) (per search string-match; not re-fetched).
- **VVIX** — definition (vol-of-vol / implied vol of VIX options) sourced to [Cboe](https://www.cboe.com/us/indices/dashboard/vvix/). **Correction:** precise crisis levels (">170 Feb 2018", ">200 Mar 2020") and "normal 80–100 / >120 / <70" were in an earlier draft but no fetchable source string-matched them — softened to "calm ~80–100" (anchored to the dashboard's caution=100 threshold in code) and the 2018/2020 spikes stated qualitatively.
- **WTI close −$37.62 (fell $55.90 on the day), 2020-04-20, first negative print, Cushing** — ✓ PDF string-match on [CRS IN11354](https://www.congress.gov/crs_external_products/IN/PDF/IN11354/IN11354.1.pdf). **Correction:** the commonly-quoted CME *settlement* is −$37.63; the CRS text states a −$37.62 *close*, and the EIA page (chart-based) does not carry the number — report now uses the CRS figure and cites CRS as primary.
- **DXY 20-year high in 2022** — sourced to the [CNBC, 2022-09-01](https://www.cnbc.com/amp/2022/09/01/forex-markets-currencies-yen-federal-reserve-interest-rate-hikes.html) headline. **Correction:** the precise "114.78 on September 27, 2022" figure was removed — that CNBC article is dated September 1 (it predates the September 27 peak) and 403s automated fetch, so the figure could not be tied to the cited URL.
- **Gold $3,000 on 2025-03-14; $4,000 in Oct 2025** — ✓ curl string-match ("3,000", "14 March") on [World Gold Council](https://www.gold.org/goldhub/gold-focus/2025/03/you-asked-we-answered-gold-hits-3000-what-comes-next); $4,000 per [WGC, 2025-10](https://www.gold.org/goldhub/gold-focus/2025/10/gold-hits-us4000oz-trend-or-turning-point).
- **Fed swap lines expanded 2020-03-15; FIMA repo 2020-03-31** — sourced to [NY Fed Liberty Street](https://libertystreeteconomics.newyorkfed.org/2020/05/have-fed-swap-lines-reduced-dollar-funding-strains-during-the-covid-19-outbreak/) / [ECB](https://www.ecb.europa.eu/press/economic-bulletin/focus/2020/html/ecb.ebbox202005_01~4a2c044d31.en.html).
- **10Y–3M Estrella–Mishkin probit, NY Fed monthly model** — ✓ [NY Fed](https://www.newyorkfed.org/medialibrary/media/research/current_issues/ci2-7.pdf) / [St. Louis Fed](https://www.stlouisfed.org/on-the-economy/2023/sep/what-probability-recession-message-yield-spreads).
- **Debt-ceiling 2023: X-date June 5; bill default-risk premium** — X-date ✓ [CNBC](https://www.cnbc.com/2023/05/26/treasury-says-it-wont-run-out-money-until-at-least-june-5-buying-time-for-debt-ceiling-talks.html) (headline); premium ✓ [Bloomberg](https://www.bloomberg.com/news/features/2023-05-22/debt-ceiling-deadline-tracker-the-grow-fear-premium-in-treasury-bill-markets) (headline). **Correction:** the precise "~5.8% record 4-week auction, highest since 2000" was removed (Bloomberg paywalled / not verified against a primary auction record).

Dashboard thresholds in the tables match [indicators/data_fetcher.py](../../indicators/data_fetcher.py) exactly (hy_oas 4.5/6.5; ig_oas 1.3/2.0; vix 20/30; vvix 100/120; vix_slope 1.0/1.15; yield_spread direction="down" 0.5/0.0).

</details>
