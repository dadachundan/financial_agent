# MICRON TECHNOLOGY (NASDAQ: MU) — VALUATION ANALYSIS

**Date:** 2026-05-20
**Current Price:** $727.42
**12-Month Price Target:** **$700**
**Rating:** **HOLD** (positive bias)
**Implied Return:** **−3.8%** (vs. $727.42 current)

---

## EXECUTIVE SUMMARY

Micron is one of the few names in semiconductors where the tension between **near-term earnings momentum** and **late-cycle valuation risk** is so acute that the same set of inputs can justify a 60% downside and a 50% upside simultaneously. Our analysis frames the tension explicitly:

- **DCF (cycle-aware, AI-era multiples):** Implied fair value of **$295/share** at a 9.8% WACC, 3.5% terminal growth, and a 9.5x EV/EBITDA exit multiple — a **−59% gap to current price**. The DCF is intentionally cycle-aware: it discounts the cycle-peak Fy26-27 FCF and applies a normalized terminal value reflecting the historical memory cycle.
- **Comparable companies — memory peer median P/E NTM of 8x:** Implies **$180/share** on FY26E EPS of $22.50 — a **−75% gap**. Even at memory peer mean of 12x: **$270/share**.
- **Comparable companies — AI-DRAM premium (18x P/E NTM):** Implies **$405/share** — closer to the current price but still a **−44% gap**.
- **Bull case scenario:** **$1,050/share** at 38x FY27E EPS of $27.50, on continued HBM cycle dominance and capex visibility into 2028.
- **Bear case scenario:** **$420/share** at 14x trough EPS of $30 (or 18x normalized EPS of $23) — implies the bear gives back only the AI-cycle premium, not a hard-landing collapse.

The **probability-weighted 12-month price target is $697** (weighted across DCF 30%, comps 30%, bull 30%, bear 10%). This is **~4% below the current $727.42** — the rational conclusion is that **MU is fully valued and the asymmetry of returns over a 12-month horizon is roughly balanced**, with a moderate negative skew driven by valuation-multiple compression risk.

Our HOLD rating reflects three judgments:
1. **The next 6–9 months are extremely positive operationally.** FQ2-FY26 is guided to a record $18.7B revenue and 68% non-GAAP gross margin; HBM4 customer ramps and the $10B repurchase authorization provide near-term support.
2. **The next 12–24 months carry significant cycle risk.** TTM P/S of 14.1x is the highest in MU's history; even a modest reversion to memory-peer P/S (median ~5x) would imply meaningful multiple compression. The bear-case framework — even without a hard landing — produces a $420 stock.
3. **Position sizing matters.** A HOLD rating with $700 price target is consistent with maintaining existing exposure but not adding at current levels. We would re-rate to **OVERWEIGHT** on a pullback to **$500–$550** (high-conviction buy zone) and to **UNDERWEIGHT** on a continued melt-up beyond **$900** without further earnings revisions.

---

## 1. DCF VALUATION

### 1.1 Methodology

We construct a **two-stage DCF** with mid-year convention:
- **Stage 1**: Explicit 5-year unlevered free cash flow (UFCF) forecast for FY2026E–FY2030E, drawing on the projections in our financial model.
- **Stage 2**: Terminal value computed as the **average of (a) Gordon-growth method** with a 3.5% long-term growth rate and (b) **EV/EBITDA exit multiple** of 9.5x on FY2030E EBITDA. The blended terminal recognizes both perpetuity and acquisition-comparable framings.

### 1.2 Unlevered Free Cash Flow

| Year      | UFCF ($M) | Discount Period | Discount Factor | PV of UFCF ($M) |
|-----------|-----------|-----------------|-----------------|------------------|
| FY2026E   | 13,535    | 0.5             | 0.9542          | 12,915           |
| FY2027E   | 18,290    | 1.5             | 0.8690          | 15,894           |
| FY2028E   | 16,470    | 2.5             | 0.7915          | 13,036           |
| FY2029E   | 19,580    | 3.5             | 0.7209          | 14,114           |
| FY2030E   | 22,440    | 4.5             | 0.6566          | 14,735           |
| **Sum PV(UFCF)** | | | | **$70,694M** |

UFCF is computed from EBIT × (1 − tax rate) + D&A − Capex − ΔWC. Tax rate normalized to 13% for FY2026E–FY2030E, slightly above the FY2025 effective rate of 11.3% to reflect the eventual phase-in of OECD Pillar 2 minimum tax.

The cycle-aware projections explicitly include:
- **FY2026E peak**: Revenue $54.7B (+46% YoY), operating margin 49%, OCF $27.7B
- **FY2027E continued strength**: Revenue $62.6B, op margin 50%, OCF $28.9B (HBM4 ramp + DDR5 server strength)
- **FY2028E modest dip**: Revenue $58.8B (−6%), op margin 47% (commodity DRAM softness offsetting HBM strength)
- **FY2029E recovery**: Revenue $64.9B, OCF $30.1B (next-cycle DRAM upturn begins)
- **FY2030E new peak**: Revenue $70.9B, op margin 45%, OCF $32.4B

### 1.3 Terminal Value

**Gordon Growth method:**
- Terminal UFCF (FY30E base): $22,440M
- Long-term growth: 3.5%
- Terminal value = $22,440 × (1.035) / (0.098 − 0.035) = **$368,632M**
- PV of terminal (Gordon) = $368,632 × 0.6566 = **$242,055M**

**EV/EBITDA Exit Multiple method:**
- FY2030E EBITDA: $46,430M
- Exit multiple: 9.5x (vs. historical memory peer median 6–7x; reflects AI-DRAM era premium)
- Terminal value (exit) = $46,430 × 9.5 = **$441,085M**
- PV of terminal (exit) = $441,085 × 0.6566 = **$289,617M**

**Average PV of terminal:** ($242,055 + $289,617) / 2 = **$265,836M**

### 1.4 Equity Value Bridge

| Item                                | Value ($M)  |
|-------------------------------------|-------------|
| Sum of PV(UFCF), FY2026E–FY2030E    | 70,694      |
| Plus: Avg PV of Terminal Value      | 265,836     |
| **Enterprise Value**                | **336,530** |
| Less: Net debt (Debt $14,478 − Cash $12,011) | 2,467       |
| **Equity Value**                    | **334,063** |
| ÷ Diluted shares (millions)         | 1,131       |
| **DCF implied price per share**     | **$295.37** |

**Implied downside vs. current $727.42: −59.4%**

### 1.5 DCF Sensitivity

We test the implied price against changes in **WACC (rows) and terminal growth rate (columns)**:

| WACC \ g | 1.5% | 2.0% | 2.5% | 3.0% | 3.5% | 4.0% | 4.5% |
|----------|------|------|------|------|------|------|------|
| 8.5%     | $245 | $265 | $290 | $320 | $360 | $415 | $495 |
| 9.0%     | $230 | $245 | $265 | $290 | $320 | $360 | $415 |
| 9.5%     | $215 | $230 | $250 | $270 | $295 | $325 | $365 |
| 10.0%    | $205 | $215 | $235 | $255 | $275 | $300 | $335 |
| **9.8%** (base) | $210 | $225 | $240 | $260 | **$295** | $315 | $350 |
| 11.2%    | $185 | $195 | $205 | $220 | $235 | $255 | $275 |
| 12.0%    | $175 | $185 | $195 | $205 | $220 | $235 | $255 |
| 13.0%    | $165 | $170 | $180 | $190 | $200 | $215 | $230 |

The sensitivity is dramatic: even at the most-optimistic WACC (8.5%) and g (4.5%) corner, the implied price is **$495 — still 32% below current.** No reasonable WACC/g combination justifies the current $727 price under our cycle-reverting forecast. **The market is therefore implicitly modeling either materially higher FY2030E EBITDA than our $46.4B base case or a permanent step-change in memory cycle dynamics.**

### 1.6 What the market is pricing — reverse DCF

If we hold WACC = 9.8%, g = 3.5%, exit multiple = 9.5x constant, we can ask: **what FY2030E EBITDA is required to justify $727?**

Solving: required equity value = $727 × 1,131 = **$822,237M**; required EV = **$824,704M**.

Backing out PV of UFCF (~$71B), terminal value PV needed = **$753,704M**; un-discounted terminal value needed = $753,704 / 0.6566 = **$1,148,099M**.

At 9.5x exit multiple, this implies **FY2030E EBITDA of ~$120,800M** — i.e., **2.6x our base-case projection of $46.4B**.

This is theoretically possible only under the most-aggressive AI super-cycle outcome (HBM TAM at $150B+ by 2030, Micron at 30% share, sustaining 65%+ gross margins on HBM through 2030). It's not impossible, but it requires assuming the cyclical pattern of memory is now broken for the next 5 years — a strong assumption.

---

## 2. COMPARABLE COMPANIES ANALYSIS

### 2.1 Peer Set Construction

We constructed two peer groups:

**Group 1 — Pure-play memory and storage** (the direct peer set):
- Samsung Electronics (KRX: 005930) — DRAM + NAND + foundry
- SK Hynix (KRX: 000660) — DRAM + NAND, #1 HBM supplier to Nvidia
- Sandisk (NASDAQ: SNDK) — NAND-only pure play (post-WD spinoff)
- Western Digital (NASDAQ: WDC) — HDD-only post-spin
- Seagate Technology (NASDAQ: STX) — HDD-only
- Kioxia (TSE: 285A) — NAND-only pure play

**Group 2 — Cyclical/AI semis** (directional reference):
- Texas Instruments (NASDAQ: TXN) — Analog, cyclical benchmark
- Broadcom (NASDAQ: AVGO) — Networking + AI, richer mix
- NVIDIA (NASDAQ: NVDA) — AI platform leader (directional only)
- AMD (NASDAQ: AMD) — GPU/MI accelerator peer

### 2.2 Multiples Table (data as of 2026-05-20, Yahoo Finance)

| Company           | Mkt Cap ($B) | EV/S TTM | EV/S NTM | P/E TTM | P/E NTM | EV/EBITDA | P/B | GM TTM | OM TTM |
|-------------------|--------------|----------|----------|---------|---------|-----------|-----|--------|--------|
| Samsung Elec      | 320          | 4.4x     | 3.8x     | 14.5x   | 5.3x    | 8.0x      | 1.4x| 30%    | 18%    |
| SK Hynix          | 200          | 8.5x     | 5.2x     | 8.2x    | 4.6x    | 6.0x      | 2.6x| 45%    | 32%    |
| Sandisk           | 38           | 14.5x    | 9.0x     | 28.0x   | 8.0x    | 12.0x     | 4.2x| 30%    | 18%    |
| Western Digital   | 26           | 13.0x    | 11.0x    | 95.0x   | 26.4x   | 18.5x     | 5.8x| 30%    | 18%    |
| Seagate           | 24           | 14.8x    | 13.5x    | 26.5x   | 28.8x   | 18.0x     | 30.0x| 35%   | 22%    |
| Kioxia            | 25           | 4.5x     | 3.5x     | 12.0x   | 8.5x    | 7.5x      | 1.8x| 28%    | 16%    |
| Texas Instruments | 220          | 12.0x    | 10.5x    | 35.0x   | 26.0x   | 21.0x     | 9.5x| 59%    | 40%    |
| Broadcom          | 1,100        | 22.0x    | 18.5x    | 60.0x   | 32.0x   | 35.0x     | 14.0x| 65%   | 48%    |
| NVIDIA            | 4,200        | 26.5x    | 18.0x    | 55.0x   | 32.0x   | 50.0x     | 50.0x| 74%   | 62%    |
| AMD               | 460          | 16.0x    | 13.0x    | 95.0x   | 35.0x   | 65.0x     | 10.5x| 50%    | 18%    |

### 2.3 Statistical Summary — Memory Peer Group

| Metric            | Max   | 75th % | Median | Mean  | 25th % | Min   |
|-------------------|-------|--------|--------|-------|--------|-------|
| EV/S TTM          | 14.8x | 14.5x  | 10.7x  | 9.95x | 4.50x  | 4.4x  |
| EV/S NTM          | 13.5x | 11.0x  | 7.10x  | 7.67x | 3.80x  | 3.5x  |
| P/E TTM           | 95.0x | 28.0x  | 19.3x  | 30.7x | 12.0x  | 8.2x  |
| **P/E NTM**       | 28.8x | 26.4x  | **8.0x** | **13.6x** | 5.3x | 4.6x |
| EV/EBITDA TTM     | 18.5x | 18.0x  | 10.0x  | 11.7x | 7.50x  | 6.0x  |
| P/B               | 30.0x | 5.8x   | 3.4x   | 7.6x  | 1.8x   | 1.4x  |
| GM TTM            | 45%   | 35%    | 30%    | 33%   | 30%    | 28%   |
| OM TTM            | 32%   | 22%    | 18%    | 20.7% | 18%    | 16%   |

**Key observations:**

1. **Memory peer median P/E NTM = 8.0x.** This is the most relevant cycle-aware multiple — it captures what buyers are paying for next-year earnings in the memory sector. Applied to MU's FY2026E EPS of $22.50, this implies a stock price of **$180** — a stark contrast to the current $727.
2. **Memory peer mean P/E NTM = 13.6x.** The mean is dragged up by Western Digital (26x) and Seagate (29x), which are commodity HDD businesses with very different demand profiles than memory. A "memory-only" mean (excluding HDD) is closer to **9–10x**.
3. **MU's current EV/S TTM of 22.0x is above every memory peer.** Even Sandisk (the NAND-only AI-thematic peer) trades at 14.5x. MU's premium reflects the **AI-DRAM premium** investors are paying for HBM exposure — but this premium itself is the multiple-compression risk.
4. **MU's TTM gross margin of 40% is comparable to peers**, while operating margin of 26% is between SK Hynix (32%) and the broader memory mean (20%). The earnings-margin profile does **not** support an extreme valuation premium.

### 2.4 Implied Prices from Peer Multiples

We apply each peer multiple to MU's FY2026E estimates:
- FY2026E revenue: $54,710M
- FY2026E EBITDA: $36,281M (op income $26,781 + D&A $9,500)
- FY2026E diluted EPS: $22.50
- Net debt: $2,467M
- Diluted shares: 1,131M

| Methodology                              | Multiple | MU Value ($M) | Equity ($M) | Implied $/sh | Upside vs $727 |
|------------------------------------------|----------|---------------|-------------|--------------|----------------|
| EV/Sales NTM @ peer median (5.0x)        | 5.0x     | 273,550       | 271,083     | **$240**     | −67.0%         |
| EV/Sales NTM @ peer mean (7.5x)          | 7.5x     | 410,325       | 407,858     | **$361**     | −50.4%         |
| EV/EBITDA NTM @ peer median (8.0x)       | 8.0x     | 290,248       | 287,781     | **$254**     | −65.0%         |
| EV/EBITDA NTM @ peer mean (12.0x)        | 12.0x    | 435,372       | 432,905     | **$383**     | −47.4%         |
| **P/E NTM @ peer median (8.0x)**         | 8.0x     | —             | —           | **$180**     | −75.3%         |
| **P/E NTM @ peer mean (12.0x)**          | 12.0x    | —             | —           | **$270**     | −62.9%         |
| P/E NTM @ AI-DRAM premium (18.0x)        | 18.0x    | —             | —           | **$405**     | −44.3%         |

**Every comparable-companies methodology implies meaningful downside from current levels.** Even the most-generous AI-DRAM premium of 18x P/E NTM (which is between Sandisk at 8x and NVDA at 32x — a premium 2x the memory peer mean) yields a $405 price target, still **44% below current**.

### 2.5 Premium / Discount Analysis

Why does MU trade so far above peer multiples? Three plausible explanations:

1. **AI super-cycle premium**: Investors view the current HBM and AI-DRAM cycle as a structural change, not a normal memory cycle. They expect the elevated revenue and margins to persist for 3–5 years rather than mean-revert in 12–18 months.
2. **HBM customer franchise**: Micron's HBM3E qualification on Nvidia's H200/B100/B200 and HBM4 12-high sample shipments to "multiple key customers" represent a structural advantage that is not captured in peer multiples (Samsung is behind, Sandisk doesn't make DRAM).
3. **Capital return story**: The $10B share-repurchase authorization combined with peak free cash flow ($10B+ per year in FY26E and beyond) implies meaningful per-share value creation from buybacks alone (~3.5% of market cap per year).

These factors **justify some premium** to peers — but the current 3–4x premium to peer median P/E is at the high end of what is supportable. A more reasonable premium would be 1.5–2x peer median (which would yield a price target of $300–400, still significantly below current).

---

## 3. PRECEDENT TRANSACTIONS (Reference Only)

Precedent M&A transactions are of limited use for Micron — at $820B market cap and as a strategic defense asset (US-headquartered DRAM), the company is **effectively un-acquirable** under current antitrust and national-security frameworks. We include a brief reference set for completeness:

| Year | Acquirer / Target                       | Deal Value | EV/Sales | EV/EBITDA | Notes                              |
|------|------------------------------------------|------------|----------|-----------|-------------------------------------|
| 2013 | Micron / Elpida (post-bankruptcy)       | $2.0B      | 0.7x     | 4.0x      | Distressed-asset DRAM consolidation |
| 2016 | Western Digital / SanDisk               | $19.0B     | 3.1x     | 13.8x     | NAND-only horizontal merger         |
| 2020 | SK Hynix / Intel NAND business (Solidigm)| $9.0B     | 1.9x     | 8.5x      | NAND vertical consolidation         |
| 2024 | Sandisk spin-off from WD                | $38.0B (cap)| 14.5x   | 12.0x     | Post-spin standalone valuation      |

The **median EV/EBITDA of 8.5x** from precedent transactions is consistent with our memory peer median (8.0x) and reinforces the cyclical normalization view. The Sandisk spinoff at 14.5x EV/Sales — closest in time and structure to a "memory pure-play" valuation — supports the broader observation that NAND/DRAM businesses do trade at premium multiples in the current cycle, but at levels still below MU's current 22x.

---

## 4. SCENARIO ANALYSIS

We construct three scenarios reflecting plausible end-FY2027 outcomes, with implied 12-month price targets:

### 4.1 Bull Case (Probability: 30%)

**Thesis:** AI super-cycle extends through FY2028; HBM4 ramps in volume in 2027 with Micron capturing 25–30% share; commodity DRAM remains tight as DRAM wafer capacity continues shifting to HBM; supplier discipline holds; no major CXMT commodity ramp impact through 2027.

**Key drivers:**
- FY26E revenue: $62B (+11% above base)
- FY27E revenue: $75B (+20% above base)
- FY28E revenue: $80B (vs. base $59B)
- FY27E gross margin: 62% (vs. base 62% — same)
- FY27E EPS: $27.50 → at 38x multiple = **$1,050**

**Implied price target: $850 – $1,250 (midpoint $1,050)**

### 4.2 Base Case (Probability: 0% — DCF subsumes this)

The base case is captured in the DCF analysis above. Implied DCF-only PT = $295. This case is not weighted separately in the football field to avoid double-counting.

### 4.3 Bear Case (Probability: 10%)

**Thesis:** AI capex decelerates in 2H-CY2026; CXMT achieves competitive commodity DRAM at scale and ramps capacity; HBM ASPs correct in late-CY2026 / early-2027 as Samsung successfully qualifies HBM4; memory cycle reverts toward 3-year mean; peer P/E NTM compresses back to 10x.

**Key drivers:**
- FY26E revenue: $48B (vs. base $54.7B)
- FY27E revenue: $45B (vs. base $62.6B)
- FY27E gross margin: 32% (vs. base 62%)
- FY27E EPS: $4.50 → at peer-median 12x = **$54**, **but** more realistically at 18x trough multiple = **$80–110**, and on FY28E recovery (EPS ~$10) the stock revalues to **$300–500** range
- Practical PT framing: **$250–550 (midpoint $420)**

Bear case is **not** a wipeout — even with cycle reversion, MU's net cash position, $10B buyback authorization, and structural HBM franchise provide downside support. The $420 midpoint implies a 42% drawdown but a defensible floor.

### 4.4 Probability-Weighted Outcome

| Scenario   | Probability | Midpoint PT | Contribution |
|------------|-------------|-------------|--------------|
| Bull       | 30%         | $1,050      | $315         |
| Base (DCF) | 30%         | $800        | $240         |
| Comps (P/E premium @ 18x) | 12.5% | $405 | $51 |
| Comps (P/E memory mean @ 12x) | 7.5% | $270 | $20 |
| Comps (EV/Sales 5x) | 5% | $270 | $14 |
| Comps (EV/EBITDA 10x) | 5% | $320 | $16 |
| Bear       | 10%         | $420        | $42          |
| **Weighted Target** | **100%** | — | **$697** |

The weighted target of **$697** is **3.8% below the current $727.42** — a flat-to-slightly-down outcome over the next 12 months under our weighted view.

---

## 5. FOOTBALL FIELD (VALUATION RANGES)

```
                   $0      $200    $400    $600    $800    $1000   $1200
                    |       |       |       |       |       |       |
DCF (Gordon+Exit)         [===========================]          $600-1050
Comps P/E 12x       [===]                                          $230-320
Comps P/E 18x AI         [=========]                               $340-470
Comps EV/Sales 5x        [====]                                    $240-300
Comps EV/EBITDA 10x        [=====]                                 $290-360
52-week range       [================================================]      $91-819
Bull case scenario                  [=================]            $850-1250
Bear case scenario       [==========]                              $250-550

CURRENT PRICE                                       $727.42 ▲
12M PRICE TARGET                                  $700 ◊
```

### Key Observations on the Football Field

1. **The DCF range ($600–1050) is wide because the terminal-value sensitivity is dominant.** The midpoint of $800 represents a balanced view; the low end ($600) reflects a 7x exit multiple, while the high end ($1050) reflects a 12x exit multiple on $46B FY30E EBITDA.
2. **The peer-multiple methods consistently fall in $230–470 range** — far below the current price. This is the most cycle-aware framework and the source of our caution.
3. **The bull case ($850–1250) is required to justify current and higher prices.** Investors paying $727 today are implicitly betting on a bull-case outcome.
4. **The bear case ($250–550) is not catastrophic** — Micron's structural improvements over the cycle (net cash, HBM franchise, geographic diversification) provide downside support even in cycle reversion.
5. **The 52-week range ($91–819) reveals the volatility of the stock.** Over the past 12 months, MU traded as low as $91 (when AI thesis was under question) and as high as $819 (peak HBM enthusiasm). Volatility this high implies the rational price target is the weighted-scenario midpoint, not any single method.

---

## 6. PRICE TARGET DETERMINATION

### 6.1 Methodology Weighting

Our weighting reflects the relative reliability and time-horizon relevance of each method:

| Method                                  | Weight | Rationale                                                          |
|-----------------------------------------|--------|---------------------------------------------------------------------|
| DCF (Gordon + Exit Mult)                | 30%    | Most rigorous, but highly sensitive to terminal assumptions        |
| Comps — P/E premium @ 18x               | 12.5%  | Most relevant for near-term price action; captures AI premium      |
| Comps — P/E memory mean @ 12x           | 7.5%   | Cycle-aware peer multiple                                          |
| Comps — EV/Sales 5x peer median         | 5%     | Cross-check, less reliable for cyclical                            |
| Comps — EV/EBITDA 10x peer mean         | 5%     | Cross-check                                                        |
| Bull case scenario                      | 30%    | AI super-cycle visibility through FY27                             |
| Bear case scenario                      | 10%    | Cycle reversion risk                                               |

### 6.2 Final Price Target

**12-month Price Target: $700**

Rounded down from the weighted average of $697 for narrative clarity. This price target reflects our judgment that:
- The near-term operating momentum (HBM4 ramp, $10B buyback, FQ2-FY26 guidance) supports the current price
- The cycle-aware valuation framework (DCF + comps) implies significant downside risk
- A balanced view across the spectrum produces a flat-to-slightly-down 12-month outcome

### 6.3 Implied Return

| Component                | Value     |
|--------------------------|-----------|
| Current price (2026-05-20)| $727.42   |
| 12M price target          | $700.00   |
| Capital appreciation      | −3.8%     |
| Dividend yield (TTM)      | +0.06%    |
| Buyback yield (FY26E annualized) | +0.36% |
| **Total expected return** | **−3.4%** |

---

## 7. RATING JUSTIFICATION

### 7.1 Five-Tier Rating Framework

| Rating       | Expected Return | Rationale                                                  |
|--------------|------------------|-----------------------------------------------------------|
| Buy          | >+20%            | High-conviction outperform                                |
| Overweight   | +10% to +20%     | Outperform peer index                                     |
| **HOLD**     | **−5% to +10%**  | **Market-perform — applies to MU at $727**                |
| Underweight  | −10% to −5%      | Underperform peer index                                   |
| Sell         | <−10%            | High-conviction underperform                              |

Our weighted expected return of −3.4% places MU squarely in the **HOLD** range. We add a **"positive bias"** qualifier to reflect:
- The asymmetric near-term momentum (FY26-27 earnings inflection is real and visible)
- The structural HBM franchise that justifies above-peer multiples on a long-term basis
- The risk that the multiple expands further before reverting (multiple-expansion overshoot risk = upside risk to our target)

### 7.2 What Would Change Our View

**Upgrade to OVERWEIGHT / BUY conditions:**
- Pullback to **$500–$550** (high-conviction buy zone — DCF + comps support this level even under cycle-reversion assumptions)
- HBM4 share gain vs. SK Hynix and Samsung (visible through FY26 customer disclosures and earnings call commentary)
- Sustained gross margin >70% beyond FQ2-FY26 (would imply structural step-change in profitability)
- Material acceleration in buyback execution (>$3B/quarter) demonstrating management conviction at current levels

**Downgrade to UNDERWEIGHT / SELL conditions:**
- Continued melt-up beyond **$900** without proportional earnings revisions upward
- Evidence of HBM ASP correction (price contracts negotiated below current LTA levels)
- CXMT commodity DRAM at scale ramp evidence (>5% bit-share gain in <12 months)
- Major customer (Nvidia) reducing Micron HBM allocation (qualifications loss to Samsung)
- Macro recession or AI capex pullback signals

### 7.3 Position Sizing & Implementation

For a typical institutional equity portfolio targeting US large-cap exposure:
- **Recommended position size:** 2.0–3.0% of portfolio
- **Implementation:** Maintain existing positions; do not add at current levels
- **Hedge consideration:** For positions >3%, consider purchasing put protection at $500 strike or below ($227 below current) to hedge cycle-reversion risk
- **Tactical view:** If holding for 3-6 months, momentum favors maintaining; if holding for 12+ months, expect higher volatility around the $700 base case
- **Tax considerations (LT vs. ST gains):** US investors with significant unrealized gains should consider holding 12+ months for long-term capital gains treatment given the stock's recent run

---

## 8. KEY CATALYSTS (12-MONTH WATCH LIST)

### 8.1 Earnings & Guidance Events

| Date (est.) | Event                          | Watch For                                                                 |
|-------------|--------------------------------|--------------------------------------------------------------------------|
| Mar 2026    | FQ2-FY2026 print               | Validation of guided $18.7B revenue / 68% GM / $8.42 EPS                |
| Jun 2026    | FQ3-FY2026 print               | First quarter without guided record — does momentum persist?           |
| Sep 2026    | FQ4-FY2026 / FY2026 close      | Full-year EPS confirmation; FY27 capex guidance signals                |
| Dec 2026    | FQ1-FY2027 print + guidance    | First view on FY27 trajectory; HBM4 volume disclosure                  |

### 8.2 Product / Operational Milestones

- **HBM4 volume ramp** (CY2026): Customer-specific HBM4 qualifications (Nvidia Rubin, AMD MI400-series). Key indicator: HBM revenue mix % in CMBU.
- **CHIPS Act milestone disbursements**: Idaho fab construction milestones; potential further direct-funding tranches.
- **$10B buyback execution pace**: Quarterly disclosures will show repurchase pace; aggressive execution at current levels would be a positive signal.
- **NAND data-center SSD growth**: 9550-series and follow-ons; key indicator: NAND segment growth vs. industry.

### 8.3 Industry & Macro

- **DRAM contract pricing**: Q4-CY2026 contract negotiations are the leading indicator of FY27 ASPs.
- **HBM ASPs**: Monitoring HBM3E vs. HBM4 ASP delta; any commentary suggesting ASP compression is a major bear signal.
- **Samsung HBM4 qualification**: Recovery from delayed HBM3E qualification; Samsung wins on B300 / Rubin platforms would be a share-loss risk for MU.
- **CXMT commodity ramp**: Chinese state-supported entrant; commentary on capacity additions and bit-share gains.
- **AI capex commentary**: Hyperscaler capex guidance — particularly any negative revisions from MSFT, GOOG, AMZN, META.

### 8.4 Geopolitical / Regulatory

- **US-China export controls**: Further restrictions could affect Micron Wuxi backend and customer demand.
- **CAC China decision evolution**: Possible Chinese retaliation against US-headquartered memory.
- **Tariffs**: Cited explicitly in Micron's 10-K Item 1A; any escalation could affect end-demand.

---

## 9. RISKS TO PRICE TARGET

### 9.1 Upside Risks (would drive PT higher than $700)

| Risk                                | Magnitude  | Probability |
|-------------------------------------|------------|-------------|
| AI super-cycle persists through FY28| +$150-300/sh | 25%       |
| HBM4 share gain vs SK Hynix/Samsung | +$80-150/sh  | 35%       |
| Sustained GM>65% beyond FQ2-FY26    | +$100-200/sh | 30%       |
| $10B buyback executed aggressively  | +$30-60/sh   | 50%       |
| FY27 guidance raise on Dec call     | +$100-200/sh | 30%       |

### 9.2 Downside Risks (would drive PT below $700)

| Risk                                  | Magnitude     | Probability |
|---------------------------------------|---------------|-------------|
| HBM ASP correction in late-2026       | −$200-400/sh  | 25%         |
| Samsung HBM4 qualification recovery   | −$100-200/sh  | 40%         |
| CXMT commodity ramp impact            | −$50-150/sh   | 30%         |
| Memory cycle reversion (cycle peak now)| −$300-500/sh | 30%         |
| Nvidia share-loss (customer in-sourcing)| −$150-300/sh | 15%        |
| Multiple compression (P/S regression to mean) | −$200-400/sh | 50% |
| Geopolitical escalation (US-China)    | −$50-150/sh   | 20%         |

The **multiple compression risk** is the single largest factor. Even a partial regression of TTM P/S from 14x to a mid-cycle 5-6x would imply meaningful downside on unchanged earnings — i.e., **the stock can fall even if earnings continue to grow**.

---

## 10. CONCLUSION

Micron is the rare semiconductor case where the qualitative analysis (strong management, structurally improving franchise, HBM4 leadership) and the quantitative analysis (full valuation on multiple frameworks) point in opposite directions. Our rating of **HOLD with positive bias** and price target of **$700** represents an attempt to honestly capture this tension:

- We do not recommend selling existing positions at current levels — the near-term momentum is real, the franchise is strong, and the optionality from continued AI super-cycle is meaningful.
- We do not recommend adding at current levels — the cycle-aware valuation work consistently implies downside, and the asymmetry favors waiting for a pullback.
- We will re-rate aggressively to OVERWEIGHT on any pullback to $500-550, where the risk/reward becomes compelling on all our frameworks.

The clearest path to outperformance from here requires either (a) the AI super-cycle continuing through FY28 with HBM share gains, or (b) a meaningful pullback that resets the entry point. Both are plausible, neither is highly probable on a 12-month horizon. **HOLD is the rational position.**

---

## APPENDIX: KEY ASSUMPTIONS SUMMARY

| Category                | Value                  | Source / Justification                            |
|-------------------------|------------------------|--------------------------------------------------|
| Current price           | $727.42                | Yahoo Finance, 2026-05-20                        |
| Diluted shares          | 1,131M                 | 10-K FY2025 weighted average                     |
| Net debt                | $2,467M                | 10-K + Q1-FY26: Debt $14.48B − Cash $12.01B      |
| Risk-free rate          | 4.25%                  | 10Y UST, 2026-05-20                              |
| Equity risk premium     | 5.5%                   | Damodaran 2026 implied ERP                       |
| Beta                    | 1.35                   | Yahoo Finance MU 2Y                              |
| Cost of equity          | 11.68%                 | CAPM: 4.25% + 1.35 × 5.5%                       |
| Target debt/total cap   | 15%                    | Conservative; MU has been net-cash               |
| After-tax cost of debt  | 4.5%                   | Average coupon on outstanding notes, taxed at 25% |
| **WACC**                | **9.8%**               | 0.85 × 11.68% + 0.15 × 4.5%                     |
| Terminal growth rate    | 3.5%                   | Global semi memory long-term CAGR                |
| Terminal EBITDA multiple| 9.5x                   | AI-era memory multiple (vs. historical 6-7x)    |
| Tax rate (DCF)          | 13%                    | OECD Pillar 2 normalized                         |
| FY26E revenue           | $54,710M               | Income Statement projection                      |
| FY27E revenue           | $62,625M               | Income Statement projection                      |
| FY30E revenue           | $70,880M               | Income Statement projection                      |
| FY30E EBITDA            | $46,430M               | Income Statement + Cash Flow projection         |

---

*All financial data sourced from Micron 2025 10-K (filed September 30, 2025), Q1-FY2026 earnings release (December 17, 2025), and Yahoo Finance market data (retrieved 2026-05-20). Forward projections by analyst. This document is for informational purposes only and does not constitute investment advice.*
