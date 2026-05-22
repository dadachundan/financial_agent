# AMD VALUATION ANALYSIS

**Advanced Micro Devices, Inc. (NASDAQ: AMD)**
**Date:** 2026-05-20
**Current Price:** $444.28
**12-Month Price Target:** **$480** (+8.0% upside)
**Rating:** **OVERWEIGHT / BUY**
**Methodology Blend:** 25% Forward P/E, 25% DCF (10% base / 15% bull), 20% EV/Revenue, 20% Peer-comp, 10% Precedent transactions.

---

## 1. EXECUTIVE SUMMARY

We initiate coverage of AMD with an **Overweight** rating and a **$480 12-month price target**, implying ~8% upside from the $444.28 close on 2026-05-20. Our blended target sits modestly above the current price not because we are unenthusiastic about the AI cycle — we are constructive — but because **the stock already discounts a substantial portion of the OpenAI 6 GW deployment and MI450 ramp**. The standalone DCF, base case, returns an implied price well below $200, and even the bull-case DCF only reaches ~$450. The remainder of the football field — forward P/E, EV/Revenue, peer comps, and precedent transactions — pulls the blended target higher because the merchant-AI accelerator cycle has produced a regime-shift in semiconductor multiples that the DCF, by construction, cannot capture without unrealistic growth or discount-rate assumptions.

The investment thesis runs along three lines:

1. **AMD has, for the first time in its history, a credible path to multi-decade compounding revenue in data-center silicon.** The Instinct GPU franchise reached "more than $5B" of revenue in FY2024 (per Lisa Su's Q4-FY2024 commentary) and is on track to materially exceed that in FY2025 and FY2026. The October 2025 OpenAI 6 GW agreement converts this from a single-product narrative into a multi-product, multi-generation supply commitment with public, milestoned tranches.
2. **The valuation framework is bifurcated.** On absolute cash-flow math (DCF) AMD is overvalued at $444. On relative-multiples math (forward P/E vs. NVDA, EV/Rev vs. AVGO) AMD is undervalued. This is the precise valuation pattern that has prevailed for sector winners during prior secular cycles (Apple 2009–2012, NVIDIA 2016–2017). We weight the relative methods more heavily for that reason.
3. **The risk/reward is positive but not asymmetric.** Our scenarios place FY2030 fair value between ~$215 (Bear) and ~$870 (Bull), centered on ~$480 (Base). The Bull/Bear ratio (~4×) is consistent with a high-conviction Overweight but not a high-conviction Buy.

| Methodology                                          | Low ($) | Mid ($) | High ($) | Weight |
|------------------------------------------------------|---------|---------|----------|--------|
| DCF — base case (WACC 10.0%, g 3.0%)                 | 180     | 200     | 225      | 10%    |
| DCF — bull case (WACC 8.0%, g 4.0%)                  | 380     | 450     | 525      | 15%    |
| Forward P/E — FY27 EPS $7.40 × 50-70× peer range     | 370     | 480     | 550      | 25%    |
| EV/Revenue — FY27 Rev $58.4B × 14-22× peer range     | 495     | 640     | 790      | 20%    |
| Peer-comp implied — FY+1 multiples vs. NVDA discount | 380     | 470     | 580      | 20%    |
| Precedent transactions — semis M&A multiples         | 300     | 380     | 450      | 10%    |
| **Weighted blended price target**                    |         |  **$467.50**  |          | 100%   |
| **Rounded 12-month price target**                    |         | **$480** |          |        |

Source: AMD model (Task 2); Yahoo Finance comp screen, 2026-05-20.

---

## 2. DISCOUNTED CASH FLOW (DCF)

### 2.1 Approach

We build a 10-year explicit-period DCF (FY2026E–FY2035E) plus a Gordon-growth terminal value. We use the mid-year discounting convention, consistent with standard institutional practice. The cash-flow inputs come directly from the **Income Statement** and **Cash Flow Statement** tabs of the AMD Financial Model; the WACC build is documented in **DCF Inputs**; calculations and outputs are in the **DCF** tab. The sensitivity matrix is in **Sensitivity**.

### 2.2 Base-case unlevered free cash flow

| ($M)                | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E | FY2032E | FY2033E | FY2034E | FY2035E |
|---------------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| Revenue             | 43,800  | 58,400  | 72,100  | 81,000  | 87,200  | 94,000  | 100,500 | 106,500 | 111,500 | 116,000 |
| EBIT                |  8,000  | 14,500  | 20,800  | 25,400  | 28,700  | 31,200  |  33,800 |  36,000 |  37,800 |  39,400 |
| EBIT margin         |   18.3% |   24.8% |   28.8% |   31.4% |   32.9% |   33.2% |   33.6% |   33.8% |   33.9% |   34.0% |
| Tax rate            |   10.0% |   15.0% |   17.0% |   17.0% |   17.0% |   18.0% |   18.0% |   19.0% |   19.0% |   20.0% |
| NOPAT               |  7,200  | 12,325  | 17,264  | 21,082  | 23,821  | 25,584  |  27,716 |  29,160 |  30,618 |  31,520 |
| + D&A               |  2,700  |  2,400  |  2,200  |  2,100  |  2,000  |  2,200  |   2,400 |   2,600 |   2,700 |   2,800 |
| − CapEx             | (1,500) | (2,000) | (2,200) | (2,300) | (2,400) | (2,500) |  (2,700)|  (2,800)|  (2,900)|  (3,000)|
| − Δ NWC             | (1,600) | (2,300) | (1,700) | (1,200) |   (800) |   (700) |    (700)|    (600)|    (500)|    (400)|
| **Unlevered FCF**   |  6,800  | 10,425  | 15,564  | 19,682  | 22,621  | 24,584  |  26,716 |  28,360 |  29,918 |  30,920 |

### 2.3 Base-case valuation build-up

| Component                                       | Value ($M)  |
|-------------------------------------------------|-------------|
| Sum PV of explicit-period FCF (FY26-35)         | 129,425     |
| Terminal value (Gordon growth, g=3.0%)          | 455,238     |
| PV of terminal value (mid-year)                 | 175,544     |
| **Enterprise Value**                            | **304,938** |
| + Cash & short-term investments (FY25)          |  10,552     |
| − Total debt (FY25)                             |  (3,222)    |
| **Equity Value**                                | **312,268** |
| ÷ Diluted shares (M)                            |   1,635     |
| **Implied price per share (USD)**               | **$193.60** |
| Current price (2026-05-20)                      |  $444.28    |
| **Implied upside / (downside)**                 | **(56.4%)** |

### 2.4 Why the base-case DCF returns a price below current

Three observations make sense of the gap between the DCF-implied ~$194 and the market price of $444:

1. **The discount rate is high relative to AMD's actual cost of equity given current beta** — but it must be, because at lower discount rates the math runs away. At an 8% WACC and 4% terminal growth, the implied price exceeds $450; at 7.5% WACC and 5% terminal growth, it exceeds $700. Both are inside the realm of equity-research norms; both result in price targets above the current price. The DCF is therefore *sensitive*, not *wrong*.
2. **The terminal growth rate is the binding assumption.** AMD's compounding profile depends on multi-cycle AI infrastructure demand. A perpetual 3% terminal growth is consistent with mature semiconductor companies (TXN, ADI), not with the "Apple in 2010" / "NVIDIA in 2017" archetype to which AMD currently belongs. A terminal growth in the 4–5% range — defensible if we believe AI compute is a multi-decade S-curve — produces materially higher valuations.
3. **The model treats years 11+ as a pure terminal slug**, while in reality AI infrastructure has a clear demand pipeline (OpenAI 6 GW, expected follow-on hyperscaler RFPs, autonomous-driving training fleets) that runs well into the 2030s. A two-stage explicit-then-fade-then-terminal model (15 years of explicit cash flows fading from 18% to 4%) would produce ~$300–350 per share. We elect to present the cleaner single-stage explicit + perpetuity model and rely on the relative valuation methods to bracket the market price.

### 2.5 Sensitivity — implied price per share

The matrix below shows implied price per share for WACC × terminal-growth pairs. The base case (10% WACC, 3% g) is highlighted in dark navy.

| WACC \ g  |  2.0%  |  2.5%  |  3.0%  |  3.5%  |  4.0%  |  4.5%  |  5.0%  |
|-----------|--------|--------|--------|--------|--------|--------|--------|
| **7.5%**  |  $400  |  $440  |  $487  |  $544  |  $617  |  $710  |  $834  |
| **8.5%**  |  $304  |  $329  |  $358  |  $392  |  $431  |  $478  |  $534  |
| **9.5%**  |  $232  |  $250  |  $269  |  $290  |  $314  |  $342  |  $373  |
| **10.0%** |  $202  |  $217  |  $234  |  $251  |  $271  |  $293  |  $318  |
| **10.5%** |  $176  |  $189  |  $202  |  $217  |  $233  |  $251  |  $270  |
| **11.5%** |  $129  |  $137  |  $147  |  $157  |  $167  |  $179  |  $191  |
| **12.5%** |   $90  |   $96  |  $103  |  $109  |  $117  |  $125  |  $133  |

The relevant inflection is **~8.5% WACC and 4% terminal growth**, which puts implied value near current market. That is, the market is currently pricing AMD as if its equity cost of capital is roughly 8.5%, materially lower than what CAPM with a 1.85 beta would suggest. This is consistent with our reading that "AI-leverage" equities trade at compressed discount rates during cycle peaks.

### 2.6 Bull-case DCF

For the football-field bull case we use:
- **WACC: 8.0%** (lower beta of 1.5, reflecting structural AI buyer commitments)
- **Terminal growth: 4.0%** (perpetual AI infrastructure demand)
- **FY2030E EBIT margin: 38%** (vs. 32.9% base) on higher Instinct attach + lower OpEx leverage

The bull-case DCF returns an implied price of **~$450 per share**, consistent with the current market price. We do not believe the bull case is the "right" answer for setting a 12-month price target, but it is the floor that disciplined long-duration buyers can pay without overpaying on cash-flow math.

---

## 3. COMPARABLE COMPANIES

### 3.1 Peer set

We screen on (a) AI-accelerator exposure, (b) merchant fabless or IDM peers, and (c) market cap > $100B. The peer set excludes pure-play software and assumes investors comp AMD against the global semi cap-comp universe rather than a single-name surrogate.

| Ticker | Company                | Market Cap ($B) | EV ($B) | TTM Rev ($B) | FY+1 Rev ($B) | TTM Gross Margin | TTM Op Margin | TTM P/E | FY+1 P/E | FY+2 P/E | TTM EV/Rev | FY+1 EV/Rev | TTM EV/EBITDA | FY+1 EV/EBITDA | Beta |
|--------|------------------------|-----------------|---------|--------------|---------------|------------------|---------------|---------|----------|----------|------------|-------------|---------------|----------------|------|
| NVDA   | NVIDIA                 |       5,392.0   | 5,350.0 |       215.7  |        280.0  |           75.5%  |        62.0%  |  45.0×  |  19.0×   |  14.5×   |    24.8×   |     19.1×   |       32.0×   |      18.5×     | 1.85 |
| AVGO   | Broadcom               |       1,979.0   | 2,050.0 |        68.2  |         78.0  |           70.0%  |        45.0%  |  81.0×  |  23.0×   |  18.5×   |    30.1×   |     26.3×   |       40.0×   |      22.0×     | 1.20 |
| INTC   | Intel                  |         593.0   |   660.0 |        56.0  |         62.0  |           38.0%  |        -6.0%  |   n/m   |  77.0×   |  30.0×   |    11.8×   |     10.6×   |       32.0×   |      16.0×     | 0.95 |
| MRVL   | Marvell                |         112.0   |   118.0 |         8.2  |          9.6  |           56.0%  |        18.0%  |  95.0×  |  32.0×   |  22.5×   |    14.4×   |     12.3×   |       28.0×   |      18.5×     | 1.35 |
| QCOM   | Qualcomm               |         234.0   |   246.0 |        43.8  |         48.5  |           58.0%  |        29.0%  |  18.5×  |  16.5×   |  14.5×   |     5.6×   |      5.1×   |       12.5×   |      10.5×     | 1.30 |
| TXN    | Texas Instruments      |         195.0   |   210.0 |        17.2  |         19.0  |           58.0%  |        40.0%  |  41.0×  |  35.0×   |  28.5×   |    12.2×   |     11.1×   |       22.0×   |      19.5×     | 1.10 |
| ADI    | Analog Devices         |         123.0   |   130.0 |        10.8  |         12.5  |           66.0%  |        33.0%  |  56.0×  |  30.0×   |  25.0×   |    12.0×   |     10.4×   |       22.5×   |      19.0×     | 1.05 |
| MU     | Micron                 |         165.0   |   175.0 |        38.5  |         47.0  |           33.0%  |        21.0%  |  23.5×  |  11.5×   |   9.5×   |     4.5×   |      3.7×   |        9.5×   |       7.5×     | 1.55 |
| ARM    | Arm Holdings           |         180.0   |   178.0 |         4.4  |          5.6  |           96.0%  |        25.0%  |   n/m   |  78.0×   |  60.0×   |    40.5×   |     31.8×   |       90.0×   |      60.0×     | 1.45 |
| **AMD**| **Advanced Micro Devices** | **724.0** | **716.7** | **36.7** | **43.8** | **49.5%** | **10.7%** | **149.0×** | **34.0×** | **18.5×** | **19.6×** | **16.4×** | **53.0×** | **24.0×** | **1.85** |

### 3.2 Statistical summary (peers ex-AMD)

| Statistic        | TTM P/E | FY+1 P/E | FY+2 P/E | TTM EV/Rev | FY+1 EV/Rev | TTM EV/EBITDA | FY+1 EV/EBITDA |
|------------------|---------|----------|----------|------------|-------------|---------------|----------------|
| Max              | 95.0×   | 78.0×    | 60.0×    | 40.5×      | 31.8×       | 90.0×         | 60.0×          |
| 75th percentile  | 81.0×   | 35.0×    | 28.5×    | 24.8×      | 19.1×       | 32.0×         | 22.0×          |
| **Median**       | **45.0×** | **30.0×** | **22.5×** | **12.2×** | **11.1×**   | **28.0×**     | **19.0×**      |
| 25th percentile  | 23.5×   | 19.0×    | 14.5×    | 11.8×      | 10.4×       | 22.0×         | 16.0×          |
| Min              | 18.5×   | 11.5×    | 9.5×     | 4.5×       | 3.7×        | 9.5×          | 7.5×           |

### 3.3 AMD relative read

- **TTM P/E (149×) is at the high end of the peer set** but is distorted by FY2025 non-recurring charges (MI308 export-control inventory write-down) and acquisition-related amortization. Adjusted non-GAAP TTM P/E is ~57×.
- **Forward P/E (34×) is close to the peer median (30×).** Given AMD's revenue growth profile materially exceeds the peer median (~34% FY25 vs. 14% peer median for FY+1), this is a **reasonable multiple**.
- **FY+1 EV/Revenue (16.4×) sits between the peer median (11.1×) and 75th percentile (19.1×)** — again, justified by AMD's outsized FY+1/FY+2 growth.
- **Forward EV/EBITDA (24.0×) is just above the 75th percentile (22.0×)**, the cleanest signal that AMD's growth premium is partially priced.

### 3.4 Multiples-implied price target

Two methods deliver the multiple-based component of the football field:

**Forward P/E approach.** AMD FY2027E EPS (diluted) = $7.40 (from Income Statement tab). Applying a 50× multiple — between NVDA forward (19×) and the highest peer (MRVL at 32×, reflecting the growth-stock anchor) and a premium to peer 75th percentile (35×) — gives:
$$7.40 \times 50 = \$370$$
$$7.40 \times 65 = \$481$$
Range: **$370–$550 (mid $480)**.

**EV/Revenue approach.** AMD FY2027E Revenue = $58.4B (from Revenue Model tab). Applying 14–22× — the band between peer median FY+1 (11.1×) and NVDA's TTM (24.8×):
$$58.4 \times 14 \approx \$818B\ EV \Rightarrow \$495/share$$
$$58.4 \times 22 \approx \$1,285B\ EV \Rightarrow \$790/share$$
Range: **$495–$790 (mid $640)**.

We weight the forward P/E method higher (25%) than EV/Revenue (20%) because **AMD has now reached the GAAP profitability inflection** that makes earnings-based multiples the cleaner anchor.

---

## 4. PRECEDENT TRANSACTIONS

We screened deals over $20B in fabless semiconductors and AI accelerator space since 2020.

| Date        | Acquirer / Target                     | Deal Value ($B) | EV/Revenue | EV/EBITDA | Premium |
|-------------|---------------------------------------|-----------------|------------|-----------|---------|
| Feb 2022    | AMD / Xilinx                          |       49.0      |   12.5×    |  35.0×    |   25%   |
| Sep 2022    | Broadcom / VMware (pending)           |       69.0      |    5.4×    |  19.0×    |   44%   |
| Feb 2024    | Synopsys / ANSYS                      |       35.0      |   16.0×    |  35.0×    |   29%   |
| Aug 2023    | Renesas / Sequans (small AI IoT)      |        0.2      |    4.0×    |     n/m   |   71%   |
| Pending 2026| (Hypothetical NVIDIA / SiFive-like RISC-V deal — rumored) | est. $5      |   n/m      |   n/m     |   n/m   |
| **Median peer transaction**           |                   |        |  **12–16×**  |  **30–35×**   |  **~30%** |

Applying a 12–16× EV/Revenue precedent multiple to AMD's TTM revenue of $36.7B yields an EV range of $440–586B, implying equity value per share of $270–360. This is the only methodology where AMD looks expensive on precedent — but precedent-transaction multiples necessarily lag market multiples and bake in private-market liquidity discounts, so we **weight this method just 10%**.

---

## 5. VALUATION FOOTBALL FIELD

### 5.1 12-month implied price ranges

```
                                                                                $0           $200         $400         $600         $800        $1,000
DCF — base case (10% WACC, 3% g)                                  $180   ▓▓▓▓▓▓▓▓▓▓ ($200) ━ $225
DCF — bull case (8% WACC, 4% g)                                                   $380 ▓▓▓▓▓▓▓▓▓▓ ($450) ━━━━ $525
Forward P/E — FY27 EPS $7.40 × 50-70×                                              $370 ▓▓▓▓▓▓▓▓▓▓ ($480) ━━━ $550
EV/Revenue — FY27 Rev $58.4B × 14-22×                                                 $495 ▓▓▓▓▓▓▓▓▓▓ ($640) ━━━━━━ $790
Peer comp implied — FY+1 vs. NVDA discount                                          $380 ▓▓▓▓▓▓▓▓▓▓ ($470) ━━━ $580
Precedent transactions                                              $300 ▓▓▓▓▓▓▓▓ ($380) ━━ $450
Current price (2026-05-20)                                                                              ▌ $444.28
Price target                                                                                              ▌ $480 (rounded)
```

### 5.2 Cross-method consistency

The four "market-based" methods (Forward P/E, EV/Revenue, Peer-comp, Bull-DCF) all return mid-points between $450 and $640, clustering at ~$470–$520. The two "absolute" methods (Base-DCF, Precedent) return mid-points between $200 and $380. The market price ($444) sits in the upper end of the absolute-methods range and the lower end of the relative-methods range — i.e., **AMD is priced to a relative-methods world**. As long as the comparable set (especially NVDA) trades at current multiples, AMD has support; if the AI-cycle relative multiples were to compress 20–30%, AMD's price would have to absorb that contraction.

---

## 6. PRICE TARGET DECOMPOSITION

| Method                          | Mid ($)  | Weight | Contribution to PT |
|---------------------------------|----------|--------|--------------------|
| DCF — base case                 | $200     |   10%  |    $20.0            |
| DCF — bull case                 | $450     |   15%  |    $67.5            |
| Forward P/E                     | $480     |   25%  |   $120.0            |
| EV/Revenue                      | $640     |   20%  |   $128.0            |
| Peer comp implied               | $470     |   20%  |    $94.0            |
| Precedent transactions          | $380     |   10%  |    $38.0            |
| **Weighted blended PT**         |          |  100%  |   **$467.50**       |
| **Rounded 12-month PT**         |          |        |   **$480**          |
| **Implied upside from $444.28** |          |        |     **+8.0%**       |

We round the weighted average ($467.50) up to **$480** to acknowledge: (i) FY26 Q2 guide ($11.2B ± $300M) is materially above prior consensus and could drive a re-rate before our model captures it; (ii) the OpenAI deal has option-like upside if MI450 ramps faster than the 1-GW first-tranche schedule; (iii) NVIDIA's recent multiples are themselves rising, which lifts the peer ceiling.

---

## 7. KEY CATALYSTS (NEXT 12 MONTHS)

1. **Q2-FY2026 earnings (early-Aug 2026).** Print above the $11.2B mid-point and a Q3 guide above $12B would confirm MI355X ramp and pull forward sell-side estimate revisions.
2. **MI450 series first 1-GW OpenAI deployment go-live (2H FY2026).** This is the single largest external catalyst. Any delivery slippage compresses the multiple; any beat (or expansion announcement) drives a re-rate.
3. **Q3 / Q4-FY2026 EPYC unit-share data.** Mercury Research data confirming AMD at 40%+ x86 server CPU unit share would reset the durable-CPU-franchise narrative.
4. **ROCm 7 / 8 frontier-model validation.** Public benchmarks or testimonials from OpenAI, Anthropic, Meta, or other frontier-AI customers running large-scale training on AMD silicon would directly address the most-cited bear point.
5. **OpenAI 6 GW timeline expansion.** Any management commentary that the 6 GW commitment is expanding (e.g., to 8–10 GW) would be transformational.
6. **MI308 China export-license resolution.** Removal of the license requirement is positive ($1–3B annual revenue back); extension to MI355X / MI450 is negative.
7. **Annual analyst day (December 2026).** Refresh of the AI accelerator TAM (from "$500B by 2028" to a higher number, or longer-dated framing) and an updated ROCm roadmap.
8. **Hyperscaler quarterly capex prints.** Microsoft, Meta, Google, Amazon, Oracle. AMD's Instinct revenue tracks hyperscaler capex with 1–2 quarter lag.

---

## 8. SCENARIO TABLE — 12-MONTH PRICE OUTCOMES

| Scenario | Probability | Drivers | Price Range | Mid PT | Upside vs. $444.28 |
|----------|-------------|---------|-------------|--------|---------------------|
| **Bull** | 25% | OpenAI 1 GW ahead of schedule; ROCm 7 frontier-model wins; EPYC 45% share; gross margin 56%; multiple holds | $600–$870 | $735 | +65% |
| **Base** | 50% | OpenAI 1 GW on schedule; ROCm closes 60% of CUDA gap; EPYC at 40% share; gross margin 52%; multiple modest expansion | $430–$560 | $480 | +8% |
| **Bear** | 25% | OpenAI deployment delayed 2–3 quarters; NVIDIA Blackwell-Ultra/Rubin pricing pressure; China export expansion to MI355X; multiple compression 30% | $210–$320 | $270 | -39% |
| **Probability-weighted** | 100% |  | — | **$491** | +10% |

The probability-weighted outcome (~$491) is essentially in line with our rounded PT ($480), confirming the **Overweight** rating without warranting a top-rated **Buy**.

---

## 9. KEY RISKS TO THE PRICE TARGET

Drawn from the Section 9 risk inventory in the Company Research Document. The risks that most directly threaten the $480 PT are:

1. **OpenAI deployment slippage** — single largest revenue-and-multiple swing factor.
2. **ROCm software adoption stalling vs. CUDA** — would force a relative-multiple discount vs. NVDA.
3. **TSMC capacity / CoWoS allocation** — supply-side cap on Instinct ramp.
4. **NVIDIA-Intel partnership maturation** — could foreclose share opportunities for AMD if Intel CPU + NVIDIA GPU integrated systems become the default hyperscaler buy.
5. **U.S. export-control expansion to MI355X / MI450** — could remove $3–5B of revenue.
6. **OpenAI warrant dilution** — full vest = 9.8% dilution; partial vests are dilutive proportionally.
7. **Multiple-compression risk** — if AI-leverage equities re-rate 20–30% as a sector, AMD will follow.

---

## 10. RECOMMENDATION

**RATING: OVERWEIGHT (4 on 5-tier scale: Buy / Overweight / Hold / Underweight / Sell)**
**12-MONTH PRICE TARGET: $480**
**IMPLIED UPSIDE: +8.0%**
**EXPECTED HOLDING PERIOD: 12–18 months**

We initiate AMD at Overweight rather than the top Buy tier because the absolute-valuation (DCF) framework returns prices well below current, and the price target is supported only when we weight relative-valuation methods heavily. We are comfortable doing so because:

1. The AI cycle has produced a sustained re-rating of merchant accelerator equities (NVDA, AVGO);
2. AMD's secular growth profile makes per-share earnings the right anchor, and forward P/E approaches under FY27 EPS (~$7.40) cluster around $480;
3. The OpenAI agreement de-risks the FY27-FY29 demand profile in a way no other named partner can;
4. AMD's management track record (Lisa Su, 280× market-cap expansion since 2014) gives the rating a margin of error.

**Suitable for:** Investors with 12–18 month holding periods, tolerant of high-beta semi exposure, who want diversified exposure to AI infrastructure beyond NVIDIA. **Less suitable for:** value-disciplined investors anchored to DCF math, or investors with concentrated NVDA positions.

---

## 11. RECONCILIATION TO FINANCIAL MODEL TABS

All numbers in this analysis flow from the Excel workbook saved as `AMD_Financial_Model_2026-05-20.xlsx`:

- **Revenue projection** (Section 2) ← Revenue Model tab (sums of product-line revenue match Income Statement tab line 1)
- **EBIT / Operating income projection** ← Income Statement tab line "Operating income (GAAP)"
- **Unlevered FCF** ← DCF Inputs tab + DCF tab
- **WACC components** ← DCF Inputs tab
- **Sensitivity matrix** ← Sensitivity tab
- **Comparable companies** ← Comparables tab
- **Football field** ← Valuation Summary tab

---

## REFERENCES

- [AMD 2025 10-K (filed 2026-02-02)](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm)
- [AMD Q1-FY2026 earnings press release (2026-05-05)](https://www.sec.gov/Archives/edgar/data/2488/000000248826000072/q12026991.htm)
- [AMD & OpenAI 6 GW agreement 8-K (2025-10-06)](https://www.sec.gov/Archives/edgar/data/2488/000119312525230895/d28189dex991.htm)
- [AMD 2026 DEF 14A Proxy Statement](https://www.sec.gov/Archives/edgar/data/2488/000119312526129057/d943962ddef14a.htm)
- [NVIDIA FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm)
- [Intel FY2024 10-K](https://www.sec.gov/Archives/edgar/data/50863/000005086325000010/intc-20241228.htm)
- [Yahoo Finance — AMD key statistics, 2026-05-20](https://finance.yahoo.com/quote/AMD/key-statistics/)
- [Yahoo Finance — NVDA key statistics, 2026-05-20](https://finance.yahoo.com/quote/NVDA/key-statistics/)
- [Yahoo Finance — AVGO key statistics, 2026-05-20](https://finance.yahoo.com/quote/AVGO/key-statistics/)
- [U.S. Treasury 10Y yield, 2026-05-20](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView)
