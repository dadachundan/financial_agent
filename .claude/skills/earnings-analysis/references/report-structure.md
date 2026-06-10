# Report Structure and Templates

This document provides complete page-by-page templates and formatting requirements for the earnings update report (markdown default; DOCX only on explicit user request — see SKILL.md § "Output Specification").

## Complete Report Structure

**REPORT STRUCTURE:**

> - **Further viewing / 延伸观看** — 1–3 validated explainer videos for hard-to-visualize concepts (the product / process / end-market driving the beat/miss), in their own slot, never a citation (see SKILL.md § "Further viewing — explainer videos").

---

## PAGE 1: EARNINGS SUMMARY

**Top Section - Header (JPM `Price (date) / Prior PT` convention):**
```
[COMPANY NAME] ([TICKER])
[QUARTER] [YEAR] EARNINGS UPDATE — [verdict + action, e.g. "Broad-based beat and raise; Reit OW, PT to $502"]

[Current Date]

ACTION HEADER (line 1 — all five elements):
[Maintain/Raise/Lower] [Rating]; PT $XXX → $YYY (+ZZ% vs $WW.WW close [date]); [valuation basis, e.g. 17.3x FY27E EPS]

Rating: [MAINTAIN/RAISE/LOWER] [RATING]
Price (as of [date]): $XX.XX          ← always date the price
Prior PT: $XXX  →  New PT: $YYY        ← always show the move
Implied upside: +ZZ% (vs dated close above)
Valuation basis: [multiple × out-year EPS / SOTP / DCF]
```

**Top Section - Market Data box (compact, broker page-1 standard — all derivable from yfinance):**
```
MARKET DATA
─────────────────────────────────────────────────
Close (YYYY-MM-DD)        $XXX.XX
52-wk range               $XX.XX – $XXX.XX
Market cap                $XXXB
Enterprise value          $XXXB
Dividend yield            X.X%
FYE                       [month]
Perf abs / vs SPX         1M +X%/+X% · 6M +X%/+X% · 12M +X%/+X% · YTD +X%/+X%

Source: Yahoo Finance (yfinance), as of YYYY-MM-DD
```

**Top Section - Quick Summary Box:**
```
EARNINGS SUMMARY
─────────────────────────────────────────────────
Q[X] [YEAR] RESULTS: [BEAT / INLINE / MISS]

                Reported    Est      Variance
Revenue         $X,XXX      $X,XXX   +$XXX (+X%)
EPS (Adj)       $X.XX       $X.XX    +$X.XX (+X%)

Key Takeaways:
■ [Takeaway 1 - one sentence]
■ [Takeaway 2 - one sentence]
■ [Takeaway 3 - one sentence]
```

**Main Content - Investment Impact (3-4 bullets):**

Use ■ character with **bold headers** and paragraph-length explanations:

```
■ **Results beat on strong [segment/geography/product], maintaining positive momentum**

Q[X] revenue of $X.XB exceeded our $X.XB estimate by X% and consensus by X%,
driven primarily by [specific driver]. [Segment] revenue grew X% YoY (vs. our
X% estimate), while [segment] grew X% (vs. X% estimate). Management highlighted
[specific products/initiatives] as key growth drivers and maintained confident
tone on outlook. The beat demonstrates [thesis point], reinforcing our positive
view.

■ **Margins expanded XXbps YoY despite [headwind], showcasing operational leverage**

[Detailed margin analysis paragraph...]

■ **Guidance raised / maintained / lowered - implies [interpretation]**

[Detailed guidance analysis paragraph...]

■ **Maintaining [RATING] with [raised/unchanged] $XXX price target**

[Investment conclusion paragraph...]
```

**Bottom Section - Key Changes / Updated Estimates Table (boxed, page-1 anchor — not an afterthought):**

This is the **structural anchor** of the page, modeled on JPM's boxed "Key Changes" header table. Lead it with a **one-line headline magnitude statement** carrying a result-driven reason, then the boxed Prev / Cur / %Chg table.

```
HEADLINE: FY27/28/29 Adj EPS raised an avg +41% on stronger AI-server scale and DRAM pricing pass-through.
          ← magnitude + direction + RESULT-driven reason (never "our model")

KEY CHANGES (FYE [month]) — boxed
─────────────────────────────────────────────────────────────────
                     FY2024E (OLD)  FY2024E (NEW)  %Chg    FY2025E (NEW)
Revenue ($M)         XX,XXX         XX,XXX         +X%     XX,XXX
Revenue Growth (%)   X.X%           X.X%           +XXbps  X.X%
Gross Margin (%)     XX.X%          XX.X%          +XXbps  XX.X%
EBITDA ($M)          X,XXX          X,XXX          +X%     X,XXX
EBITDA Margin (%)    XX.X%          XX.X%          +XXbps  XX.X%
Adj EPS ($)          X.XX           X.XX           +X%     X.XX
FCF ($M)             X,XXX          X,XXX          +X%     X,XXX
P/E (x)              XX.Xx          XX.Xx          -X%     XX.Xx

Note: "E" = Estimate. Old estimates from [prior report date].
Source: Company data, [Firm Name] estimates.
```

**Quarterly Forecasts grid (JPM standard) — EPS-by-quarter forward grid with A/E flags carried across years.** Distinct from the QoQ revenue-progression table on Pages 2-3; this one carries Adj EPS forward and flags the just-reported quarter "A":

```
QUARTERLY FORECASTS (Adj EPS)
─────────────────────────────────────────────────────────────────
              Q1        Q2        Q3        Q4        FY
FY24          X.XX(A)   X.XX(A)   X.XX(A)   X.XX(A)   X.XX(A)
FY25          X.XX(A)   X.XX(A)   X.XX(A)←  X.XX(E)   X.XX(E)   ← reported quarter flagged "A"
FY26          X.XX(E)   X.XX(E)   X.XX(E)   X.XX(E)   X.XX(E)

Source: [Firm Name] estimates.
```

---

## PAGES 2-3: DETAILED RESULTS ANALYSIS

Break down results by:

### Revenue Analysis (1 page)
- Total revenue beat/miss explanation
- Segment/geographic/product breakdown
- YoY and sequential trends
- Comparison to guidance (if provided)

**Table: Quarterly Revenue Progression**
```
                        Q[X-3]  Q[X-2]  Q[X-1]  Q[X]    YoY Chg  QoQ Chg
Total Revenue ($M)      X,XXX   X,XXX   X,XXX   X,XXX   +X%      +X%
  [Segment A] ($M)      XXX     XXX     XXX     XXX     +X%      +X%
  [Segment B] ($M)      XXX     XXX     XXX     XXX     +X%      +X%
  [Segment C] ($M)      XXX     XXX     XXX     XXX     +X%      +X%

Note: Q[X] = [Quarter] [Year]
Source: Company reports, [Firm Name] analysis
```

### Profitability Analysis (1 page)
- Gross margin analysis (drivers, trends)
- Operating margin analysis
- Below-the-line items (interest, tax, etc.)
- EPS reconciliation (adjusted vs. GAAP)

**Table: Margin Analysis**
```
                        Q[X-3]  Q[X-2]  Q[X-1]  Q[X]    YoY Chg
Gross Margin (%)        XX.X%   XX.X%   XX.X%   XX.X%   +XXbps
Operating Margin (%)    XX.X%   XX.X%   XX.X%   XX.X%   +XXbps
Net Margin (%)          XX.X%   XX.X%   XX.X%   XX.X%   +XXbps

Key Drivers:
+ [Positive driver 1]
+ [Positive driver 2]
- [Negative driver 1]
- [Negative driver 2]
```

**Embed 2-3 charts on these pages:**
- Chart 1: Quarterly revenue progression
- Chart 2: Quarterly EPS progression
- Chart 3: Margin trends

---

## PAGES 4-5: KEY METRICS & GUIDANCE

### Business Metrics (1 page)
- Customer count, ARPU, units, store count, etc.
- Whatever metrics company emphasizes
- Comparison to expectations
- Trends and outlook

**Table: Key Operating Metrics**
```
                        Q[X-3]  Q[X-2]  Q[X-1]  Q[X]    YoY Chg  Our Est  Var
[Metric 1]              XXX     XXX     XXX     XXX     +X%      XXX      +X%
[Metric 2]              XXX     XXX     XXX     XXX     +X%      XXX      +X%
[Metric 3]              XXX     XXX     XXX     XXX     +X%      XXX      +X%

Source: Company reports
```

**Forward-visibility metrics (the leading indicators the banks lead with — add where disclosed):**

- **Backlog / bookings / order-book** — a leading indicator distinct from revenue (Dell $51.3B AI backlog, +$24B new orders this quarter; Broadcom $60bn POs with a by-customer GW schedule). Show the level, the sequential add, and book-to-bill if derivable. If the company doesn't disclose it, say so.
- **Per-unit economics by quarter** — for platform / turnaround names, the unit-economics trajectory IS the thesis (Meituan per-order profit Rmb/order by quarter; DiDi China-mobility per-order EBITA margin 4.6%). Add a unit-economics row trending the per-unit number toward breakeven.

```
FORWARD VISIBILITY
─────────────────────────────────────────────────────────────────
                        Q[X-3]  Q[X-2]  Q[X-1]  Q[X]    QoQ add
Backlog / bookings ($M) XXX     XXX     XXX     XXX     +XXX
Per-order profit (Rmb)  X.X     X.X     X.X     X.X     —       ← path to breakeven
Book-to-bill (x)        X.X     X.X     X.X     X.X

Source: Company reports / earnings call
```

- **Path-to-normalized-profit bridge** — for loss-making / turnaround names, state the out-year normalized number with its build (UBS Meituan FY28 normalized Rmb42bn = delivery 27 + IHT 22 − new initiatives −7). See workflow.md Step 9.

**Balance sheet & capital return (standing mini-block — NOT optional-appendix material; Bernstein keeps standing exhibits for buyback / inventory days / net debt every quarter):**
```
BALANCE SHEET & CAPITAL RETURN
─────────────────────────────────────────────────────────────────
                            Q[X-1]      Q[X]
Buyback ($M)                XXX         XXX     (remaining authorization $X.XB)
Dividend ($M / per share)   XXX / X.XX  XXX / X.XX
Inventory ($M / days)       X,XXX / XXX X,XXX / XXX
Net cash (debt) ($M)        X,XXX       X,XXX

Source: 10-Q / earnings release
```

### Guidance & Outlook — a CO-EQUAL block, not a footnote (1 page)

**The forward guide is frequently the real story while the print is table stakes** (GS Dell, DB Oracle, Broadcom FQ3). Treat the guidance block as **co-equal with the print block** — and split it into **next-quarter** and **full-year**, each shown **three ways: vs prior guide, vs Street, AND vs our model**, with a one-line achievability take. This is the GS/DB standard the skill previously folded into a single table.

**If guidance provided — GUIDANCE vs PRIOR vs STREET vs OURS:**
```
GUIDANCE vs PRIOR vs STREET vs OURS
─────────────────────────────────────────────────────────────────
                     New Guide       Prior Guide   vs Street   vs Ours
NEXT-QTR Revenue     $XX-XXB (mid $X) $XX-XXB       +X% vs $X   +X% vs $X
NEXT-QTR EPS         $X.XX-X.XX       n/a           +X% vs $X   +X% vs $X
NEXT-QTR [Segment A] implied ~$X.XB   —             −X% vs $X   −X% vs $X   ← labeled calc
NEXT-QTR [Segment B] implied ~$X.XB   —             +X% vs $X   in line
FY Revenue           $XX-XXB (mid $X) $XX-XXB       +X% vs $X   +X% vs $X
FY EPS               $X.XX-X.XX       $X.XX-X.XX    +X% vs $X   +X% vs $X

Our Take (achievability): [one line — sandbag/stretch read vs track record;
  and, for up-cycle raises, the binding constraint: supply- vs demand-constrained]
```

**Decompose the guide by segment where possible (Bernstein QCOM FQ1-26 standard).** Where the company guides a segment — or the total guide plus held-flat assumptions lets you imply one — derive the implied segment number, **label it as a calc with both inputs cited**, and show it vs Street and vs our model (Bernstein: "QCT guided $8.8-9.4B mid $9.1B well below consensus $9.8B; Handsets seen ~$6B well below the Street at ~$6.87B; Auto implied ~$1.3B above Street $1,158M"). The segment-implied decomposition is usually where the actual story lives. Cross-reference workflow.md Step 8.

Note the explicit **guide-midpoint** column — beat/miss must be triangulated against YoY, our estimate, AND the guide midpoint (Bernstein/DB/GS lead with the midpoint). For the credibility / sandbag-vs-stretch and supply-vs-demand framing behind "Our Take", see workflow.md Step 8.

**Embed 2-3 charts:**
- Chart 4: Key metrics trends
- Chart 5: Guidance vs. Street comparison
- Chart 6: Revenue by segment/geography

---

## PAGES 6-7: UPDATED INVESTMENT THESIS

### Thesis Impact Assessment (1-2 pages)

For each key thesis pillar, assess impact of results:

**Where the call hinges on market share, state the number and trajectory — not qualitative prose** (MS: Broadcom ASIC ~80% long-run share vs MediaTek+Google 15-20%; Marvell 60-65% in 1.6T DSP). Replace "we believe [Co] is gaining share" with a quantified share line + direction.

```
■ **Thesis Pillar 1: [Original thesis statement]**

Status: [STRENGTHENED / UNCHANGED / WEAKENED]

Q[X] results [supported / challenged] this thesis pillar because [specific
evidence from results]. [Detailed analysis of 150-200 words explaining how
results impact this specific thesis element. Where share-driven, quantify:
"share ~XX% long-run vs peers at YY-ZZ%, trending up on [driver]".]

■ **Thesis Pillar 2: [Original thesis statement]**

[Similar analysis]

■ **Thesis Pillar 3: [Original thesis statement]**

[Similar analysis]
```

### Risks Update (0.5 pages)
- Any new risks identified?
- Have existing risks been mitigated or worsened?
- Brief assessment

**Embed 1-2 charts:**
- Chart 7: Valuation vs. historical
- Chart 8: Estimate revision comparison

---

## PAGES 8-10: VALUATION & ESTIMATES

### Updated Valuation (1-2 pages)

**DCF Update:**
```
Updated DCF inputs based on Q[X] results:
- Revenue growth FY24E: X.X% → X.X% (raised/lowered)
- EBIT margin FY24E: XX.X% → XX.X%
- Terminal growth: X.X% (unchanged)
- WACC: X.X% (unchanged)

Updated DCF fair value: $XXX (prior: $XXX)
```

**Comparable Companies:**
```
[Company] trades at XX.Xx NTM P/E vs. peer median of XX.Xx (-X% discount).
Given [rationale], we believe [premium/discount/inline] valuation is warranted.
```

**Price Target Methodology — the build must visibly sum to the headline PT (UBS/Citi SOTP, MS single-multiple):**

Do not merely "mention DCF/comps". Show an explicit build that reconciles to the printed PT.

**Any PT change must be decomposed into multiple change vs estimate change** (Bernstein: "PT $200→$175 = de-rate 18x→17x, on FY27E EPS $11.15→$10.38") — never print just the new PT; the reader must see which lever moved and by how much.

For **multi-segment names**, a SOTP build where each line is `EBIT × multiple → per-share value`, summing to the PT (UBS Meituan / Citi DiDi standard):
```
SOTP → PRICE TARGET
─────────────────────────────────────────────────────────────────
Segment            FY[n]E EBIT   Multiple   EV ($M)   Per share
[Segment A]        X,XXX         XXx        XX,XXX    $XX
[Segment B]        X,XXX         XXx        XX,XXX    $XX
[Segment C / net cash]                      X,XXX     $X
─────────────────────────────────────────────────────────────────
Sum → Price Target                                    $XXX   ← must equal headline PT

Source: [Firm Name] estimates.
```

For **single-line names**, an explicit `multiple × out-year EPS` build (MS "28x FY27"; GS "30x normalized EPS"):
```
Our $XXX PT (prior $XXX) = XX.Xx × FY[n]E Adj EPS of $X.XX.
(or: weighted XX% DCF / XX% NTM P/E XX.Xx vs peers XX.Xx / XX% EV/EBITDA — each component shown and summing to $XXX.)

Implied upside: +XX% from current price of $XXX (close [date]).
```

See workflow.md Step 10 for the build mechanics.

### Updated Estimates Detail

Provide updated estimates for at least current year and next year:

```
DETAILED ESTIMATE UPDATES
─────────────────────────────────────────────────────────────────
                            FY2024E                 FY2025E
                     Old      New      Change    New Estimate
Revenue ($B)         XX.X     XX.X     +X.X%     XX.X
  [Segment A]        XX.X     XX.X     +X.X%     XX.X
  [Segment B]        XX.X     XX.X     +X.X%     XX.X

Gross Profit ($B)    XX.X     XX.X     +X.X%     XX.X
Gross Margin (%)     XX.X%    XX.X%    +XXbps    XX.X%

EBITDA ($B)          X.X      X.X      +X.X%     X.X
EBITDA Margin (%)    XX.X%    XX.X%    +XXbps    XX.X%

Operating Income     X.X      X.X      +X.X%     X.X
Op Margin (%)        XX.X%    XX.X%    +XXbps    XX.X%

Net Income ($B)      X.X      X.X      +X.X%     X.X
EPS - Adjusted ($)   X.XX     X.XX     +X.X%     X.XX
EPS - GAAP ($)       X.XX     X.XX     +X.X%     X.XX
FCF ($B)             X.X      X.X      +X.X%     X.X

P/E (x)              XX.Xx    XX.Xx              XX.Xx
EV/EBITDA (x)        XX.Xx    XX.Xx              XX.Xx

Source: [Firm Name] estimates
```

**Embed 1-2 charts:**
- Chart 9: P/E or EV/EBITDA bands
- Chart 10: Price target walk (old → new)

---

## PAGES 11-12: APPENDIX (Optional)

### Detailed Quarterly Models (if space allows)
- Income statement detail
- Cash flow highlights
- Balance sheet highlights

### Call Transcript Highlights (optional)
- Key Q&A excerpts
- Notable management quotes

### Peer Comparison (if peers have reported)
- How results compare to competitors
- Market share implications

**Embed final charts:**
- Chart 11: Peer comparison
- Chart 12: Additional supporting charts

---

## FORMATTING REQUIREMENTS

### 1. Page 1 Requirements
- Clear rating (MAINTAIN OUTPERFORM, RAISE TO BUY, etc.)
- Updated price target prominently displayed
- Summary table with old/new estimates
- 3-4 paragraph-length bullets with ■ character

### 2. All Tables Requirements
- Source line at bottom
- Clear column headers
- Shading for header rows

### 3. All Charts Requirements
- "Figure X - [Title]" caption above
- "Source: [Source]" line below
- Professional styling

### 4. Year Notation
- Use A for actual (Q3'24A)
- Use E for estimate (Q4'24E)

### 5. Writing Style
- Lead with numbers ("Revenue grew 15% to $1.2B" not "Strong revenue growth")
- Use "vs." not "versus"
- Be direct and concise
- Focus on what's NEW

### 6. Hyperlink Requirements ⭐⭐⭐
- ALL URLs must be clickable hyperlinks in Word
- Blue, underlined text that opens on Ctrl+Click
- Display text meaningful (not raw URL)
- Every source citation should have clickable link where applicable
- No plain text URLs - always format as hyperlinks

## Citation Examples for Specific Content

### For Beat/Miss Analysis:
```
Revenue of $2.45B beat consensus of $2.39B by $60M (2.5%)¹

¹ *Analyst view:* [Bernstein Q3 preview, 2024-11-02](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>) (Street $2.39B);
  Company [earnings release, November 7, 2024](https://investor.company.com/news/q3-2024-earnings)
```
(Never "Bloomberg/FactSet consensus" — no terminal exists; the consensus figure must string-match a URL cited in the same paragraph. See SKILL.md § "Consensus & sell-side sources in this project".)

### For Guidance:
```
Management raised FY2024 revenue guidance to $9.8-10.0B from prior $9.5-9.7B²

² Q3 2024 Earnings Call, November 7, 2024, CFO prepared remarks
  [Hyperlink "Earnings Call" to: https://seekingalpha.com/article/...]
  Prior guidance from Q2 earnings call August 8, 2024
  [Hyperlink "Q2 earnings call" to August transcript]
```

### For Key Metrics:
```
Enterprise customers grew 23% YoY to 845, with net revenue retention at 128%³

³ Q3 2024 10-Q, page 23
  [Hyperlink "10-Q" to: https://www.sec.gov/cgi-bin/viewer?accession=...]
  Q3 2024 Investor Presentation slide 8
  [Hyperlink "Investor Presentation" to PDF]
```
