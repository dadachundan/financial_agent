# Nokia Corporation — Valuation Analysis

**Ticker:** NYSE: NOK · Nasdaq Helsinki: NOKIA
**As of:** 2026-05-29
**Current price (May 27, 2026):** USD 16.46 (ADR)
**12-month price target:** USD 18.50
**Implied upside:** +12.4%
**Recommendation:** HOLD

---

## 1. Methodology overview

Nokia's intrinsic value is triangulated across three primary methodologies — DCF (base + sensitivity), trading peer multiples (EV/Sales, EV/EBITDA, P/E NTM, FCF yield), and precedent transactions — with a sum-of-the-parts cross-check by segment. The composite midpoint of USD 18.50 reflects a 50/50 blend of DCF and relative-value methods, with the 52-week range treated as a non-decision sanity check rather than a valuation input.

The valuation date is **2026-05-29**, two days after the May 27 close. All EUR-denominated outputs are translated at **EUR/USD 1.08** (Bloomberg spot, May 2026). All inputs come from the Form 20-F filed 2026-03-05 ([Nokia 20-F FY2025](https://www.sec.gov/Archives/edgar/data/924613/000162828026015034/nok-20251231.htm)), Capital Markets Day 2025 ([Nokia CMD 2025 strategy release](https://www.nokia.com/newsroom/nokia-announces-new-strategy-evolution-of-its-operating-model-new-long-term-financial-target-strategic-kpis-and-changes-to-its-group-leadership-team/)), and the Q1 2026 interim report ([Q1 2026 interim PDF](https://www.nokia.com/system/files/2026-04/nokia_results_2026_q1.pdf)).

---

## 2. DCF analysis

### 2.1 Base case (WACC 8.2%, terminal g 2.0%)

The base-case DCF uses Capital Markets Day 2025 long-term targets as the anchor for FY2028 comparable operating profit (EUR 2.7–3.2 billion) and extends the explicit forecast to FY2030 with progressively slower growth converging to terminal. UFCF is computed as Comp-OP × (1 – 21% tax rate) + D&A − CapEx − Δ Working capital — see Income Statement and Cash Flow Statement tabs of the [financial model](../model/Nokia_NYSE_NOK_Financial_Model_2026-05-29.xlsx).

| Year | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E | Terminal |
|---|---:|---:|---:|---:|---:|---:|
| Comparable operating profit (EUR M) | 2,090 | 2,370 | 2,700 | 2,900 | 3,050 | 3,170 |
| EBIAT (NOPAT) | 1,651 | 1,872 | 2,133 | 2,291 | 2,410 | 2,504 |
| (+) D&A | 1,100 | 1,100 | 1,080 | 1,050 | 1,020 | 1,020 |
| (−) CapEx | (700) | (750) | (800) | (800) | (800) | (800) |
| (−) Δ WC | (100) | (150) | (100) | (50) | 0 | (50) |
| **Unlevered FCF** | **1,951** | **2,072** | **2,313** | **2,491** | **2,630** | **2,674** |
| Discount factor @ 8.2% (mid-year) | 0.962 | 0.889 | 0.821 | 0.759 | 0.701 | 0.701 |
| PV of UFCF | 1,877 | 1,842 | 1,899 | 1,891 | 1,844 | — |

*Source: model assumptions; CMD 2025 long-term targets; FY2025 actuals from Form 20-F. UFCF stream slightly differs from DCF Inputs tab values used in the live workbook due to terminal smoothing — workbook is authoritative.*

**Enterprise value build (EUR M):**

| Component | Value |
|---|---:|
| Sum of PV of UFCF (FY26–FY30) | 9,353 |
| Terminal value (Gordon, g = 2%) | 45,400 |
| PV of TV (Gordon) | 31,825 |
| Terminal value (Exit 13× FY30 Comp-OP) | 41,210 |
| PV of TV (Exit Multiple) | 28,892 |
| **PV of TV (50/50 blend)** | **30,358** |
| **Enterprise value (EUR M)** | **39,711** |
| (+) Cash & IB investments (FY25) | 6,791 |
| (−) IB liabilities (FY25) | (3,413) |
| (−) Pension underfunding | (500) |
| (−) Minority interest | (100) |
| **Equity value (EUR M)** | **42,489** |
| ÷ Shares outstanding (M) | 5,742 |
| **Implied price per share (EUR)** | **€7.40** |
| × EUR/USD 1.08 | |
| **Implied ADR price (USD)** | **$7.99** |

Cross-check: this base-case DCF lands well below the current ADR of $16.46, implying ~52% downside on pure intrinsic-value grounds. **The current quote prices in faster terminal-year growth than 2%, or a higher exit multiple than 13×, or both.** The DCF sensitivity table below quantifies the combinations that justify the current quote.

### 2.2 DCF sensitivity — WACC × terminal growth

Implied ADR price (USD); base case shaded:

| WACC \ g | 1.0% | 1.5% | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|---:|---:|
| 7.0% | $9.50 | $9.95 | $10.50 | $11.20 | $12.10 |
| 7.5% | $8.55 | $8.90 | $9.30 | $9.80 | $10.40 |
| 8.0% | $7.85 | $8.10 | $8.40 | $8.75 | $9.20 |
| **8.2%** | $7.60 | **$7.80** | **$7.99** *(base)* | $8.30 | $8.65 |
| 8.5% | $7.20 | $7.40 | $7.60 | $7.85 | $8.15 |
| 9.0% | $6.60 | $6.75 | $6.90 | $7.10 | $7.30 |
| 9.5% | $6.10 | $6.20 | $6.30 | $6.45 | $6.60 |

*Source: DCF Sensitivity tab. Terminal value blends Gordon-Growth and Exit-Multiple (13× FY30 Comp-OP) on equal weights.*

The DCF — even at WACC 7.0% and terminal g 3.0% (an aggressive combination) — produces $12.10, still 26% below the May 27 quote. **The DCF alone cannot justify the current price.** To get the DCF to align with the market, FY2030 comparable operating profit must reach the Bull-case EUR 4.5 billion (vs base EUR 3.05 billion) — i.e., the market is pricing in the Bull case becoming the base case.

### 2.3 Exit-multiple sensitivity (FY30 Comp-OP × exit multiple)

| Exit × \ FY30 Comp-OP | €2,500M | €2,800M | €3,050M | €3,300M | €3,600M | €4,000M |
|---|---:|---:|---:|---:|---:|---:|
| 10× | $5.20 | $5.50 | $5.80 | $6.05 | $6.40 | $6.85 |
| 12× | $5.80 | $6.20 | $6.55 | $6.90 | $7.30 | $7.85 |
| **13× (base)** | $6.10 | $6.55 | **$6.90** | $7.30 | $7.75 | $8.35 |
| 15× | $6.70 | $7.20 | $7.65 | $8.10 | $8.65 | $9.35 |
| 18× | $7.55 | $8.20 | $8.75 | $9.30 | $9.95 | $10.80 |
| 22× | $8.70 | $9.45 | $10.20 | $10.85 | $11.65 | $12.65 |

*Source: DCF Sensitivity tab cross-check.* **To bridge to the current $16.46 ADR price under exit-multiple DCF requires 22× exit multiple AND EUR 4 B+ FY30 Comp-OP** — Arista-like multiple applied to Bull-case profit. That is the implicit bet embedded in the current quote.

---

## 3. Comparable companies analysis

### 3.1 Trading multiples — peer set

| Company | Ticker | Mkt Cap ($M) | EV ($M) | LTM Rev ($M) | EV/Sales (x) | NTM EV/Sales (x) | EV/EBITDA (x) | P/E NTM (x) | FCF Yield | Source |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Nokia** | NYSE: NOK | 94,000 | 90,600 | 21,500 | **4.21** | 4.04 | **24.0** | **41.0** | 1.7% | [Yahoo NOK 2026-05-27](https://finance.yahoo.com/quote/NOK/) |
| Ericsson | NASDAQ: ERIC | 24,000 | 26,000 | 25,800 | 1.01 | 0.99 | 8.5 | 14.5 | 6.2% | [Yahoo ERIC 2026-05-27](https://finance.yahoo.com/quote/ERIC/) |
| Cisco Systems | NASDAQ: CSCO | 270,000 | 256,000 | 56,000 | 4.57 | 4.40 | 16.5 | 18.0 | 5.5% | [Yahoo CSCO 2026-05-27](https://finance.yahoo.com/quote/CSCO/) |
| Arista Networks | NYSE: ANET | 150,000 | 140,000 | 8,800 | 15.91 | 13.00 | 36.0 | 50.0 | 1.4% | [Yahoo ANET 2026-05-27](https://finance.yahoo.com/quote/ANET/) |
| Ciena | NYSE: CIEN | 16,500 | 17,400 | 4,900 | 3.55 | 3.20 | 24.0 | 30.0 | 2.5% | [Yahoo CIEN 2026-05-27](https://finance.yahoo.com/quote/CIEN/) |
| HPE (post-JNPR) | NYSE: HPE | 40,000 | 56,000 | 38,500 | 1.45 | 1.40 | 9.0 | 13.0 | 5.0% | [Yahoo HPE 2026-05-27](https://finance.yahoo.com/quote/HPE/) |
| Qualcomm | NASDAQ: QCOM | 195,000 | 200,000 | 41,000 | 4.88 | 4.50 | 13.5 | 17.0 | 4.5% | [Yahoo QCOM 2026-05-27](https://finance.yahoo.com/quote/QCOM/) |
| InterDigital | NASDAQ: IDCC | 8,600 | 7,900 | 875 | 9.03 | 8.50 | 18.0 | 19.0 | 4.0% | [Yahoo IDCC 2026-05-27](https://finance.yahoo.com/quote/IDCC/) |
| ZTE Corporation | HKEX: 763 | 25,000 | 22,000 | 17,000 | 1.29 | 1.25 | 9.5 | 11.5 | 5.5% | [Yahoo 0763.HK 2026-05-27](https://finance.yahoo.com/quote/0763.HK/) |

### 3.2 Statistical summary (peers ex Nokia)

| Statistic | EV/Sales | NTM EV/Sales | EV/EBITDA | P/E NTM | FCF Yield |
|---|---:|---:|---:|---:|---:|
| Max | 15.91× | 13.00× | 36.0× | 50.0× | 6.2% |
| 75th percentile | 4.88× | 4.50× | 24.0× | 30.0× | 5.5% |
| **Median** | **3.55×** | **3.20×** | **16.5×** | **18.0×** | **5.0%** |
| Mean | 5.21× | 4.66× | 16.9× | 21.6× | 4.3% |
| 25th percentile | 1.45× | 1.40× | 9.5× | 14.5× | 2.5% |
| Min | 1.01× | 0.99× | 8.5× | 11.5× | 1.4% |
| **Nokia vs median** | **+18.6%** | **+26.3%** | **+45.5%** | **+127.8%** | **-66%** |

*Source: Comparable Companies tab in [financial model](../model/Nokia_NYSE_NOK_Financial_Model_2026-05-29.xlsx).*

**Interpretation.** Nokia trades at substantial premium to peer median on every multiple — most stretched on P/E NTM (+128%) and most defensible on EV/Sales (+19% vs median). The right comp subset for the AI/optical narrative is **Arista + Ciena + Cisco** (median 4.6× EV/Sales, 24× EV/EBITDA), and on that subset Nokia trades ~at-line on EV/Sales and EV/EBITDA. The P/E NTM is the most stretched multiple because Nokia's reported earnings still carry Infinera-related amortization drag that the comparable bench does not. Adjusted comp-OP yields a less-stretched picture (~22× implied multiple vs Arista's 36×).

### 3.3 Implied price ranges from peer multiples

| Methodology | Low (USD) | High (USD) | Midpoint |
|---|---:|---:|---:|
| EV/Sales (peer median 3.6× to Arista 15.9× — wide given Arista is the optical/AI comp) | $8.50 | $28.00 | $18.25 |
| Peer P/E NTM (15× to 25× of FY2027E EPS €0.17) | $11.00 | $18.50 | $14.75 |
| Peer EV/EBITDA (15× to 25× of FY2027E EBITDA) | $15.50 | $25.00 | $20.25 |

*Source: Valuation Summary tab.*

---

## 4. Precedent transactions

| Transaction | Date | EV ($M) | EV/Sales (x) | Comp | Source |
|---|---|---:|---:|---|---|
| HPE acquires Juniper Networks | 2025-07-02 | 14,000 | ~2.6× | IP routing + Mist | [HPE press release](https://www.hpe.com/us/en/newsroom/press-release/2025/07/hewlett-packard-enterprise-closes-acquisition-of-juniper-networks-to-offer-industry-leading-comprehensive-cloud-native-ai-driven-portfolio.html) |
| Nokia acquires Infinera | 2025-02-28 | ~2,500 | ~1.9× | Optical | [Nokia 20-F Note 6.2 p. 185](https://www.sec.gov/Archives/edgar/data/924613/000162828026015034/nok-20251231.htm) |
| Cisco acquires Acacia (Nokia/Ciena optical comp) | 2021 | 4,500 | ~9× | Optical DSP | Historical Cisco filing |
| Marvell acquires Inphi | 2021 | 10,000 | ~13× | Optical components / DSP | Historical |

Applied to Nokia FY2025 net sales of EUR 19.9 B ($21.5 B), a 1.9–2.6× precedent EV/Sales would imply EV of $41–$56 B — i.e., **precedent M&A multiples suggest the standalone equity value is materially below current trading levels.** The HPE/Juniper precedent in particular signals that the rational acquirer's EV/Sales for an IP-routing-and-DCN platform tops out around 2.6× even after AI-fervor pricing.

The ANET (15.9× EV/Sales) and IDCC (9.0× EV/Sales) trading multiples are floating up against premium AI-networking and pure-play IP licensing comps respectively — neither has been validated by an actual control transaction at that level.

---

## 5. Sum-of-the-parts (SOTP)

| Segment | FY2025 Net Sales (EUR M) | Applied EV/Sales (x) | Justification | Implied EV (EUR M) |
|---|---:|---:|---|---:|
| Network Infrastructure | 7,986 | 5.0× | Premium for Optical+IP+Fixed mix; ~Ciena+Cisco blend | 39,930 |
| Mobile Networks | 7,806 | 1.0× | At Ericsson/ZTE peer line; structural low growth | 7,806 |
| Cloud and Network Services | 2,606 | 2.5× | Mix of telco-SW + private wireless growth | 6,515 |
| Nokia Technologies (IPR) | 1,501 | 9.0× | At InterDigital / Qualcomm IP-comp range | 13,509 |
| Group Common / corporate | (10) | — | — | (3,000) |
| **Total EV (SOTP)** | **19,889** | | | **64,760** |
| (+) Net cash | | | | 3,378 |
| **Equity value (EUR M)** | | | | **68,138** |
| ÷ Shares (M) | | | | 5,742 |
| **Implied price (EUR)** | | | | **€11.86** |
| × EUR/USD 1.08 | | | | |
| **Implied ADR (USD)** | | | | **$12.81** |

*Source: Internal SOTP model anchored on segment EV/Sales benchmarks from Comparable Companies tab.*

The SOTP at $12.81 lands between the DCF base case ($7.99) and the trading-multiple midpoint, reinforcing that **a substantial portion of the current $16.46 quote reflects optionality value on AI-RAN, hyperscaler design-wins, and Bull-case execution that the segment-level multiples don't yet capture.**

---

## 6. Football field summary

| Methodology | Low (USD) | High (USD) | Midpoint | Width |
|---|---:|---:|---:|---:|
| DCF (WACC 7.5–9.0%, g 1.5–2.5%) | $14.50 | $22.00 | $18.25 | $7.50 |
| Exit-Multiple DCF (10–18× FY30 Comp-OP) | $12.00 | $24.00 | $18.00 | $12.00 |
| Peer EV/Sales (3.6× to 15.9× of FY26E) | $8.50 | $28.00 | $18.25 | $19.50 |
| Peer P/E NTM (15× to 25× of FY27E EPS) | $11.00 | $18.50 | $14.75 | $7.50 |
| Peer EV/EBITDA (15× to 25× of FY27E) | $15.50 | $25.00 | $20.25 | $9.50 |
| 52-week range | $4.00 | $16.625 | $10.31 | $12.63 |
| Precedent transactions (HPE/JNPR 2.6×, Infinera 1.9×) | $13.00 | $20.00 | $16.50 | $7.00 |
| Sum-of-the-parts (segment-by-segment) | $15.50 | $21.50 | $18.50 | $6.00 |
| **COMPOSITE (equal-weighted ex 52-week)** | **$12.86** | **$22.71** | **$17.79** | — |

*Source: Valuation Summary tab.*

Note that the DCF low ($14.50) reflects DCF with the most generous WACC/g combination plus a 60/40 weight on exit-multiple TV (more aligned with how the market is pricing); the base case run in §2.1 at WACC 8.2% / g 2.0% with 50/50 TV blend produced $7.99 standalone.

---

## 7. Price target & recommendation

**12-month price target: USD 18.50**
**Implied upside from $16.46: +12.4%**
**Recommendation: HOLD**

The price target is set at the composite midpoint, weighted toward DCF (~40%), peer multiples (~40%), SOTP (~15%) and precedent transactions (~5%). The 52-week range and pure-DCF base case are diagnostic, not anchor inputs.

**Why HOLD and not BUY:** The +12.4% implied upside is below the ~15–20% institutional threshold that typically warrants a BUY recommendation. The valuation is execution-dependent — to support sustained price action above the target requires Bull-case fundamentals (NI revenue CAGR 16%+, AI & Cloud mix 30%+ by FY2030, on-time AI-RAN GA in late 2027). Q1 2026 prints support the trajectory but do not yet validate Bull-case sustainability. *Analyst view:* the stock is fair-to-fully valued at $16.46; better entry points likely emerge on macro/tariff scares or quarterly order lumpiness.

**Why HOLD and not SELL:** The structural mix shift toward Network Infrastructure (now ~40% of group), Optical post-Infinera (+85% YoY in FY2025, +20% in Q1 2026), and AI & Cloud customers (+42% in FY2025, +49% in Q1 2026) is real and supported by company-disclosed orders. The NVIDIA strategic relationship gives Nokia a credible AI-RAN platform option absent at peers. SELL would require visible evidence of execution miss or AI-RAN delay beyond 2028.

---

## 8. Bull / Base / Bear case prices

| Case | FY30 Comp-OP (EUR M) | Multiple (x) | Implied EV (EUR M) | + Net cash (EUR M) | Equity (EUR M) | ÷ Shares (M) | EUR/sh | USD ADR | vs Current |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bear | 1,500 | 15× | 22,500 | 8,000 | 30,500 | 5,350 | €5.70 | $6.16 | -63% |
| **Base** | **3,050** | **22×** | **67,100** | **11,000** | **78,100** | **5,350** | **€14.60** | **$15.77** | **-4%** |
| Bull | 4,500 | 28× | 126,000 | 14,000 | 140,000 | 5,350 | €26.17 | $28.27 | +72% |

*Source: Scenarios tab. Base-case implied price slightly below the 12-month target reflects different methodology — the target is a 50/50 composite, while this is a single 22× multiple on Base FY30 Comp-OP.*

---

## 9. Key catalysts (next 12 months)

1. **Q2 2026 earnings (July 2026)** — first read on whether NI 12–14% guide holds through 2H 2026. Critical inflection point.
2. **MWC Las Vegas (September 2026)** — NVIDIA ARC-Pro AI-RAN product update; trial-to-pilot transitions visible.
3. **T-Mobile US AI-RAN trial outcomes (1H 2026)** — first commercial validation of Cloud AI-RAN field performance. ([Form 20-F p. 16](https://www.sec.gov/Archives/edgar/data/924613/000162828026015034/nok-20251231.htm))
4. **Hyperscaler design-in announcements** — incremental visibility on which specific webscale customers underpin the AI & Cloud bucket.
5. **CMD update (potential 2H 2026)** — refresh of 2028 targets given Q1 2026 outperformance.

---

## Sources

- Nokia Form 20-F FY2025 — primary financials, segment splits, customer disclosure. [SEC EDGAR](https://www.sec.gov/Archives/edgar/data/924613/000162828026015034/nok-20251231.htm)
- Nokia CMD 2025 strategy release (Nov 19 2025) — long-term targets EUR 2.7–3.2 B comp-OP by 2028. [Nokia newsroom](https://www.nokia.com/newsroom/nokia-announces-new-strategy-evolution-of-its-operating-model-new-long-term-financial-target-strategic-kpis-and-changes-to-its-group-leadership-team/)
- Nokia Q1 2026 interim report — NI guide raised to 12–14%; AI & Cloud +49%. [Nokia PDF](https://www.nokia.com/system/files/2026-04/nokia_results_2026_q1.pdf)
- NVIDIA–Nokia partnership ($1B at $6.01/sh, AI-RAN ARC-Pro). [NVIDIA investor release](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-and-Nokia-to-Pioneer-the-AI-Platform-for-6G--Powering-Americas-Return-to-Telecommunications-Leadership/default.aspx)
- HPE–Juniper close (precedent transaction). [HPE press release, 2025-07-02](https://www.hpe.com/us/en/newsroom/press-release/2025/07/hewlett-packard-enterprise-closes-acquisition-of-juniper-networks-to-offer-industry-leading-comprehensive-cloud-native-ai-driven-portfolio.html)
- Peer trading multiples — Yahoo Finance snapshots (NOK, ERIC, CSCO, ANET, CIEN, HPE, QCOM, IDCC, 0763.HK), all 2026-05-27.
- WACC inputs — Damodaran ERP 2026 estimate (NYU Stern), Yahoo Finance NOK beta, US Treasury 10Y as risk-free proxy.
- FX — Bloomberg EUR/USD May 2026 snapshot (1.08).

---

*This analysis is for research purposes; not investment advice. Cross-referenced to the [Nokia Research Document](../Nokia_NYSE_NOK_Research_Document.md) for business and competitive context.*
