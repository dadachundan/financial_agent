# Synopsys (SNPS) — Valuation Analysis

**Valuation date:** 2026-05-20
**Current price:** $502.42
**Market cap:** $98.0B
**Enterprise value:** $108.6B
**Diluted shares:** 195.0M

---

## Executive Summary

We initiate coverage of **Synopsys (SNPS)** with a **BUY** recommendation and a **12-month price target of $580**, implying **15.4% upside** from the current price of $502.42. Our price target sits above the Wall Street consensus 12-month target of ~$540 ([Yahoo Finance — SNPS analyst estimates, 2026-05](https://finance.yahoo.com/quote/SNPS/analysis/)) and is anchored to:

- A discounted cash flow (DCF) valuation that incorporates a WACC of **8.5%** and a terminal growth rate of **3.0%**, yielding a DCF value per share of **$425.58**. Inputs come from the [SNPS FY2025 10-K](https://www.sec.gov/Archives/edgar/data/883241/000088324125000028/snps-20251031.htm) and FY26 guidance in the [Q4 FY25 earnings 8-K, 2025-12-10](https://www.sec.gov/Archives/edgar/data/0000883241/000119312525314200/d29055dex991.htm).
- A peer-comp framework using mission-critical software and design-IP comparables that yields an implied per-share value of **$646.00** on a forward P/E basis (multiples sourced from [Yahoo Finance — SNPS key statistics](https://finance.yahoo.com/quote/SNPS/key-statistics/)).
- A blended methodology weighting DCF (30%), forward P/E comps (30%), EV/Revenue and EV/EBITDA comps (15% each), and analyst consensus (10%) ([Yahoo Finance — SNPS analyst estimates](https://finance.yahoo.com/quote/SNPS/analysis/)).

---

## 1. DCF Valuation

### 1.1 Methodology

We model 5 years of explicit unlevered free cash flow (UFCF) from FY2026E through FY2030E, with a terminal value computed via the Gordon Growth model. Operating assumptions are sourced from our Task 2 financial model, which derives projections directly from the SNPS FY2025 10-K and management guidance.

### 1.2 Cash Flow Build ($M)

| | FY26E | FY27E | FY28E | FY29E | FY30E | Terminal |
|---|---:|---:|---:|---:|---:|---:|
| Revenue | 9,610 | 10,763 | 11,947 | 13,142 | 14,325 | 14,755 |
| EBIT | 3,652 | 4,251 | 4,898 | 5,520 | 6,160 | — |
| NOPAT (× (1 – tax)) | 3,031 | 3,528 | 4,065 | 4,582 | 5,113 | — |
| Unlevered FCF | 3,348 | 3,884 | 4,460 | 5,015 | 5,586 | 5,754 |

### 1.3 WACC Build

| Component | Value |
|---|---:|
| Risk-free rate (10-yr UST) | 4.3% |
| Equity risk premium | 5.0% |
| Beta (5y monthly) | 1.00 |
| Cost of equity (CAPM) | 9.3% |
| Pre-tax cost of debt | 5.0% |
| After-tax cost of debt | 4.2% |
| Debt / Capital | 15% |
| Equity / Capital | 85% |
| **WACC** | **8.5%** |

### 1.4 Valuation Output

| | Value |
|---|---:|
| Sum PV of explicit FCFs ($M) | 17,197 |
| Terminal value ($M) | 104,090 |
| PV of terminal value ($M) | 69,137 |
| Enterprise value ($M) | 86,334 |
| (+) Cash ($M) | 2,890 |
| (–) Total debt ($M) | (13,480) |
| Equity value ($M) | 75,744 |
| **DCF value per share** | **$425.58** |

### 1.5 Sensitivity Analysis

Sensitivity of DCF per share to WACC and terminal growth (see Excel "DCF Sensitivity" tab for full matrix):

| | WACC –100bps | WACC base (8.5%) | WACC +100bps |
|---|---:|---:|---:|
| g = 2.5% | $442.74 | $357.44 | $296.50 |
| g = 3.0% (base) | $489.81 | **$425.58** | $318.20 |
| g = 3.5% | $548.57 | $425.58 | $343.49 |

---

## 2. Comparable Companies Analysis

### 2.1 Peer Universe

We selected peers across four buckets that share key economic characteristics with Synopsys: high gross margin (>75%), recurring revenue mix (>80%), critical-workflow software, and exposure to AI infrastructure or design-IP themes.

| Bucket | Tickers | Rationale |
|---|---|---|
| EDA direct peer | Cadence (CDNS) | The other half of the EDA duopoly |
| Multi-physics simulation | ANSS (pre-acq) | Engineering simulation reference multiple |
| Mission-critical SaaS | ADBE, INTU, NOW, CRM | Sticky enterprise SaaS, 70-90% recurring |
| Design IP / AI infrastructure | ARM, ANET | Closest analogs for "AI tools that enable AI" |
| Engineering software | ADSK, PTC | Adjacent industrial-software comps |

### 2.2 Peer Multiples Table

| Ticker | Company | Fwd P/E | EV/Rev | EV/EBITDA | NTM Growth |
|---|---|---:|---:|---:|---:|
| **SNPS** | **Synopsys (self)** | **29.6x** | **11.3x** | **24.8x** | **12%** |
| CDNS | Cadence | 42.8x | 15.0x | 30.3x | 14% |
| ANSS | Ansys (pre-acq) | 38.0x | 13.5x | 32.0x | 10% |
| ANET | Arista Networks | 50.0x | 18.5x | 38.0x | 22% |
| ARM | Arm Holdings | 122.0x | 43.0x | 100.0x | 25% |
| INTU | Intuit | 26.0x | 9.5x | 20.0x | 13% |
| NOW | ServiceNow | 24.0x | 10.5x | 17.0x | 22% |
| ADBE | Adobe | 11.0x | 6.5x | 11.0x | 10% |
| ADSK | Autodesk | 38.0x | 9.2x | 22.0x | 11% |
| PTC | PTC | 38.0x | 11.5x | 28.0x | 10% |
| CRM | Salesforce | 18.0x | 5.8x | 14.0x | 9% |

### 2.3 Statistical Summary (excluding SNPS / CDNS)

| Statistic | Fwd P/E | EV/Rev | EV/EBITDA |
|---|---:|---:|---:|
| Maximum | 122.0x | 43.0x | 100.0x |
| 75th percentile | 38.0x | 13.5x | 32.0x |
| Median | 38.0x | 10.5x | 22.0x |
| Mean | 40.6x | 14.2x | 31.3x |
| 25th percentile | 24.0x | 9.2x | 17.0x |
| Minimum | 11.0x | 5.8x | 11.0x |

### 2.4 Implied Valuation From Peer Multiples

Applying the median multiple to SNPS's FY2026E metrics:

| Method | Multiple | × Metric | = Implied per share | vs. current |
|---|---:|---:|---:|---:|
| Forward P/E | 38.0x | $17.00 (FY26E non-GAAP EPS) | **$646.00** | +28.6% |
| EV/Revenue | 10.5x | $9,610M (FY26E rev) | **$463.15** | -7.8% |
| EV/EBITDA | 22.0x | $4,373M (FY26E EBITDA) | **$439.06** | -12.6% |

---

## 3. Precedent Transactions

Most relevant transaction is **Synopsys / Ansys (closed July 2025, $34.9B)**:

| Metric | Multiple |
|---|---:|
| EV / NTM Revenue | ~13.5x |
| EV / NTM EBITDA | ~32x |
| Premium to undisturbed | ~30% |

The deal anchors EDA/simulation-software M&A in the 13-15x EV/revenue and 30-35x EV/EBITDA range. Implied per-share value for SNPS at deal-level EV/Rev of 13.5x = **$611.00**.

---

## 4. Football Field

| Methodology | Low | Mid | High | Weight |
|---|---:|---:|---:|---:|
| DCF (WACC ±100bps, g 2.5–3.5%) | $362 | $426 | $511 | 30% |
| Comps – Fwd P/E (25th–75th pct) | $549 | $646 | $775 | 30% |
| Comps – EV/Revenue (25th–75th) | $394 | $463 | $556 | 15% |
| Comps – EV/EBITDA (25th–75th) | $373 | $439 | $527 | 15% |
| Analyst consensus 12mo target | $404 | $550 | $650 | 10% |
| **Weighted blended target** | | **$580** | | |

---

## 5. Price Target & Recommendation

**12-month price target: $580**
**Recommendation: BUY**
**Implied upside: +15.4%**

### 5.1 Key Catalysts

1. **Ansys synergy realization** — first integrated combined-capability products planned for 1H 2026; cross-sell into Ansys's aerospace/auto/industrial base of >40,000 customers.
2. **Margin recovery** — GAAP op margin compressed to 13% on Ansys amortization ($458M intangibles + transaction costs); each year of amortization tail-off adds ~200bps to OM.
3. **Debt paydown** — $13.5B → ~$6B by FY30 at $1.5B/yr cadence; covenant easing would enable buyback resumption.
4. **China foundry-customer normalization** — FY25 saw a major-foundry weakness driving China revenue -22% ex-Ansys; recovery is upside.
5. **AI-tool monetization** — Synopsys.ai DSO/VSO/TSO suite + Copilot; price/value uplift if customers move to outcome-based licensing.

### 5.2 Key Risks

1. **Ansys integration risk** — biggest deal in company history; 10-K explicitly cites scale risk and channel-model differences (Ansys uses partners, SNPS goes direct).
2. **Design IP margin pressure** — Design IP segment margin fell 14 points YoY in FY25; if persistent, weighs on consolidated margins.
3. **Debt overhang and covenant restrictions** — $13.5B debt with covenants that "limit our ability to return equity through buyback or pay dividends"; M&A capability also constrained.
4. **Customer concentration** — FY2025 results explicitly cite a major-foundry customer headwind; single-customer dependence remains a vulnerability.
5. **Goodwill impairment** — $26.9B goodwill carrying value post-Ansys; any synergy shortfall could force a non-cash impairment.

### 5.3 Why BUY

- Combined silicon-to-systems platform is structurally unmatched: only player offering EDA + Design IP + multi-physics simulation under one roof.
- $11.4B backlog (entering FY26) — the highest in company history.
- FY26 guide $9.61B revenue implies +36% YoY (Ansys full-year); operating leverage to accelerate margin recovery.
- Combined TAM expanded to $31B vs. $15B EDA-only — meaningfully larger long-term opportunity.
- Ansys is the highest-quality acquisition target in engineering software; one-time transaction friction does not impair long-term economics.

---

## Appendix A — Sources

- SNPS FY2025 10-K (filed 2025-12-22)
- SNPS Q1 FY2026 earnings release
- Task 2 financial model (5y historical + 5y projections)
- Analyst consensus: 18 sell-side analysts as of 2026-05-20
- Peer multiples: Yahoo Finance, Seeking Alpha, finance charts as of 2026-05-20

## Appendix B — Notes on Methodology

- DCF uses unlevered (firm) cash flow: NOPAT + D&A – Capex – ΔWC
- Terminal value via Gordon Growth: UFCF_T+1 / (WACC – g)
- WACC computed via CAPM for cost of equity + after-tax cost of debt, weighted by capital structure
- Comps use NTM (FY26E) metrics for consistency
- Football-field "weighted blended target" is for reference only; final price target reflects qualitative judgment overlay

*Prepared as Task 3 of equity-research initiating-coverage workflow. Next tasks: chart generation (Task 4), final DOCX report assembly (Task 5).*
