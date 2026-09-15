# GE Vernova (GEV) — zsxq Research Lens Reading List

**Generated:** 2026-09-15 · **Ticker:** GEV (GE Vernova) · **Lens:** http://localhost:5001/zsxq/research-lens?ticker=GEV

**Sources:** `db/stock_price_target.db` → table `price_targets` (15 GEV rows, one per ticker × broker × report) joined to `db/zsxq.db` → table `pdf_files` (the PDFs themselves, on disk under `/Users/x/Downloads/zsxq_reports/`).

**Scan method:** trigram full-text search of the 13,515-row zsxq PDF library for `GEV` / `GE Vernova` → 71 candidate PDFs → 15 carry an explicit GEV rating or price target (the rest are read-across or comp-table mentions of Siemens Energy, Yingliu, Weichai, Hitachi, Dongfang, Harbin). All 15 were read in full and digested one by one.

**Feed shape:** GEV is a **crowded consensus long** — 13 of 15 calls are Buy/OW/Outperform, and the two Holds (HSBC) are pure valuation calls, not thesis disagreement. But the *evidence density* is wildly uneven: only **6 of 15** reports actually argue a GEV case; the other **9** are comp-table rows and one-line "top pick" mentions inside notes about other companies. This list is ordered by how much you actually learn about GEV per minute of reading.

---

## How to read the score

| Score | Meaning |
|---|---|
| **8–10** | Primary GEV work: proprietary data or a quantified argument about GEV itself. Read it. |
| **6–7** | Real GEV content (a full page, a channel survey, an SOTP) inside a report about something else, or a short but genuinely fresh GEV read. Worth the time. |
| **4–5** | A few sharp GEV datapoints — a backlog number, a capacity figure — but GEV is a comp row. Skim the GEV paragraph only. |
| **0–3** | GEV is a name in a table or a line on a chart. The report may be excellent; it is not GEV research. Skip unless you want the theme. |

The score weights four things: (1) **is there a GEV thesis at all** — rating + why, or just a row in a valuation table; (2) **insight density** — proprietary/channel data vs restated consensus; (3) **data support** — exhibits, models, SOTP builds, verbatim management quotes; (4) **event context** — was it written around a print, a deal or a regulatory trigger (which makes it a dated, testable call) or in a quiet patch.

---

## Ranked list

| Score | Report | Pp · Date | GEV stance & PT | Price on date → upside | Open |
|---|---|---|---|---|---|
| **8/10** | **J.P. Morgan** — Yingliu Electromechanical-A: *Read-across from GE Vernova's 2Q26 results* | 9 · 07-23 | OW, PT **$1,302** (+26%) | $1,031.19 → **+26.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584281422521424/J.P.%20Morgan-Yingliu%20Electromechanical%20~A%EF%BC%88603308%EF%BC%89Read~across%20from%20GE%20Vernova%E2%80%99s%202Q26%20results-260723.pdf) |
| **7/10** | **Morgan Stanley** — Siemens Energy AG: *The capacity conundrum… Stay OW* | 22 · 01-26 | OW, PT **$822** | $665.25 → **+23.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214514824525141/Morgan%20Stanley-Siemens%20Energy%20AG%EF%BC%88ENR1n.DE%EF%BC%89The%20capacity%20conundrum.%20Less%20of%20a%20focus%20for%202026%EF%BC%8C%20but%20close%20monitoring%20required.%20Stay%20OW.-260126.pdf) |
| **7/10** | **Jefferies** — Digital Infrastructure: *All the Data Center Demand in the World, Still Not Enough Supply* | 32 · 06-05 | Buy, no PT | $933.13 → n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584251128411224/Jefferies-USA%20-%20Digital%20Infrastructure%EF%BC%9AAll%20the%20Data%20Center%20Demand%20in%20the%20World%EF%BC%8C%20Still%20Not%20Enough%20Supply-260605.pdf) |
| **6/10** | **HSBC** — US Nuclear: *SMRs to fuel AI dominance* | 59 · 04-24 | **Hold**, PT **$740** (−36%) | $1,149.19 → **−35.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415518585855828/HSBC-US%20Nuclear%EF%BC%9ASMRs%20to%20fuel%20AI%20dominance-260424.pdf) |
| **6/10** | **Bernstein** — US Industrials: *30 exhibits on cooling & electrical equip. procurement in NA Data Centers* | 27 · 08-20 | Outperform, PT **$1,298** | $966.01 → **+34.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412841521854558/Bernstein-U.S.%20Multi%20Industry%20%26%20Electrical%20Equipment%20US%20Industrials%EF%BC%9A%2030%20exhibits%20on%20the%20state%20of%20cooling%20and%20electrical%20equip.%20procurement%20in%20North%20American%20Data%20Centers-260820.pdf) |
| **6/10** | **J.P. Morgan** — Weichai Power A/H: *Positive read-throughs from BE, Innio, GE Vernova* | 14 · 07-29 | OW, PT **$1,330** (+48%) | $900.28 → **+47.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584285418514214/J.P.%20Morgan-Weichai%20Power%20~%20A%20H%20%EF%BC%88000338%EF%BC%89Positive%20read~throughs%20from%20BE%EF%BC%8C%20Innio%EF%BC%8C%20GE%20Vernova%EF%BC%9A%20%20SOFC%EF%BC%8C%20Gas%20Engines%EF%BC%8C%20BTM%20Demand%EF%BC%9B%20stay%20OW-260729.pdf) |
| **5/10** | **J.P. Morgan** — Clean Energy and Power Infrastructure: *2026 March Madness* | 21 · 03-09 | OW, PT **$1,000** (top pick) | $829.17 → **+20.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585551114124884/J.P.%20Morgan-Clean%20Energy%20and%20Power%20Infrastructure%202026%20March%20Madness-260309.pdf) |
| **5/10** | **UBS** — China Energy Transition: *Buy China Power Equipment* | 45 · 03-13 | Buy, PT **$936** (benchmark) | $804.12 → **+16.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585551445584884/UBS-China%20Energy%20Transition%20Buy%20China%20Power%20Equipment%EF%BC%9A%20Strong%20EPS%20upside%20from%20domestic%20and%20export%20business-260313.pdf) |
| **5/10** | **Bernstein** — Americas Energy & Transition: *The Peaker you can't see* | 20 · 06-30 | Outperform, PT **$1,206** | $1,174.86 → **+2.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412424445241828/Bernstein-Americas%20Energy%20%26%20Transition%EF%BC%9A%20The%20Peaker%20you%20can%27t%20see~Can%20VPPs%20become%20the%20MVP%20in%20the%20U.S.%EF%BC%9F-260630.pdf) |
| **4/10** | **HSBC** — China power equipment: *How Chinese gas turbines go overseas* | 18 · 03-06 | **Hold**, PT **$740** (−6%) | $788.35 → **−6.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415554212511288/HSBC-China%20power%20equipment%EF%BC%9AHow%20Chinese%20gas%20turbines%20go%20overseas-260306.pdf) |
| **4/10** | **J.P. Morgan** — Yingliu Electromechanical: *Customer updates reinforce OW case* | 10 · 06-18 | OW, PT **$1,302** (comp row) | $1,109.73 → **+17.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214524525528511/J.P.%20Morgan-Yingliu%20Electromechanical%EF%BC%88603308%EF%BC%89Customer%20updates%20reinforce%20OW%20case-260618.pdf) |
| **4/10** | **UBS** — US Electrical Equipment & Multi-Industry: *Top 10 takes from earnings* | 12 · 05-03 | Buy, no PT | $1,062.41 → n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415248452524448/UBS-US%20Electrical%20Equipment%20%26%20Multi~Industry%EF%BC%9ATop%2010%20takes%20from%20earnings%20%EF%BC%88so%20far...%EF%BC%89-260503.pdf) |
| **3/10** | **Bernstein** — Global Capital Goods: *Powering AI: The modular advantage* | 57 · 09-14 | Outperform, PT **$1,298** | $874.76 → **+48.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214822528121111/Bernstein-Global%20Capital%20Goods%20Powering%20AI%EF%BC%9A%20The%20modular%20advantage~how%20value%20shifts%20and%20who%20captures%20it-260914.pdf) |
| **3/10** | **Goldman Sachs** — GS SUSTAIN: *AI DATA CENTERS* | 36 · 08-06 | Buy (basket member), no PT | $1,000.30 → n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584284828815454/Goldman%20Sachs-GS%20SUSTAIN%EF%BC%9A%20AI%20DATA%20CENTERS%EF%BC%9APower%20demand%EF%BC%8C%20cyclical%20progression%20and%20Sustainability%20implications-260806.pdf) |
| **3/10** | **Goldman Sachs** — US Conviction List: *Directors' Cut, April 2026* | 75 · 04-01 | **not on the list** (supplier mention only) | $894.78 → n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585545825518884/Goldman%20Sachs-US%20CONVICTION%20LIST~DIRECTORS%E2%80%99%20CUT%EF%BC%9AApril%202026%20Update-260401.pdf) |

> Note: a **sixteenth** JPM note dated 2026-03-09 — *The Sustainable Investor: Make the Grid Great Again* (61 pp, file `184445214585182`) — carries the same GEV OW / $1,000 call and is the better read of the two (full SOTP build, rate **6/10**). It is **not** on the lens because the DB's `uq_ticker_broker_date` key keeps only one row per (ticker, broker, report_date). [download](http://xs-macbook-air.local:5001/zsxq/pdf/184445214585182/J.P.%20Morgan-The%20Sustainable%20Investor%EF%BC%9AMake%20the%20Grid%20Great%20Again-260309.pdf)

---

## Why each one rates Overweight / Hold — and what it's actually worth

### 8/10 — J.P. Morgan, 07-23 · *Read-across from GE Vernova's 2Q26 results* (9 pp)

**Why bullish:** Written the day after GEV's own 2Q26 print (22–23 Jul), it is the only report in the set built on GEV's fresh numbers. JPM's case: "GEV signed ~20GW of new gas power contracts and raised its FY26E exit expectation for gas backlog+SRA to at least 125GW versus at least 110GW previously"; "1H26 gas equipment order pricing running >20% above 4Q25 levels," with 2H26 at "the higher end of the 10–20% uplift range"; and a quantified supply/demand bridge — FY26 supply ~64GW vs demand ~115–120GW, FY27 ~70GW vs ~110–120GW, FY28 ~80GW, tightening only around FY30. GEV also "outlined a pathway to 30GW of annual gas output by 2030 via lean and incremental machinery within the existing footprint."

**Insight density:** Highest of the set — pricing trajectory, backlog bridge and a capacity pathway, all sourced from GEV's own call. One caveat: the printed Q/Q deltas ("gas backlog expanded 44GW to 53GW; SRAs increased 56GW to 63GW") don't reconcile with the "100GW to 116GW" total quoted on the same page — a typo worth flagging, not a thesis-breaker.

**Data support:** 2 exhibits — Figure 1 (GEV backlog + SRAs) and Table 1 (17-name gas-turbine comps).

**Event context:** Same-week read-across on the 2Q26 print; the single most *time-sensitive* document here.

**Why 8:** Nine pages, but this is the only place you get post-2Q26 GEV pricing and backlog numbers outside the company's own deck — and it is dated, so it is a testable call.

---

### 7/10 — Morgan Stanley, 01-26 · *Siemens Energy AG — The capacity conundrum* (22 pp)

**Why bullish:** "GEV OW, TP $822" (p.1) — a maintained call, not an argued one. The value of the note is that its primary work is a **gas-turbine supply model** that directly governs GEV's pricing power. Demand: 2025 single-cycle GT orders ~88GW vs ~50GW supply (76% ahead); the big-3 (GEV/ENR/MHI) hold ~80% of capacity; data centres were just 25% of 2025 orders (22/88GW).

**Why the note is also the bear case:** capacity doubles to 75GW by 2028 and 97GW of gas by 2030; "price cracks" start in small/mid DC primary power after 2026. Exhibit 3 shows GEV's gas backlog + slot reservations at 50→54→62GW (1Q25→3Q25) vs Siemens Energy's 50→58→70GW — **GEV is no longer the clear scale leader**, and it adds only ~4GW of small/mid capacity in 2028–30. Longer term the grid-hook-up constraint favours GEV's H-frames as DC load turns baseload.

**Insight density:** A differentiated supply model with five explicit caveats (MHI doubling = 8.6GW of the 22GW 2028–30 step-up; engine GW not all DC-reachable; blade/vane tightness). GEV itself is valuation-only: 18.2× 2028 EV/EBITA, 26.6× PE vs ENR's 33% PE discount.

**Event context:** Published two days **before** GEV 4Q25 (28 Jan 2026) and flags it as a catalyst — a rare pre-print framing.

**Why 7:** The most useful *negative* evidence on GEV's competitive position in the whole set, from a house that is simultaneously OW. You learn more about GEV's risk here than from any of the Buy-rated thematic notes.

---

### 7/10 — Jefferies, 06-05 · *All the Data Center Demand in the World, Still Not Enough Supply* (32 pp)

**Why bullish:** "GE Vernova Inc (GEV: $963.33, BUY)", one of 23 "Top Picks to Play DC Supply Chain Tightness" — no PT anywhere in the PDF. Substance: "GEV reported Q1 2026 orders of $18.3B (+71% organically) with total backlog reaching $163B… Electrification booked $2.4B in data center equipment orders in Q1 alone, exceeding all of 2025 combined"; "GEV now expects combined gas turbine backlog and slot reservation agreements to reach at least 110 GW by year-end 2026." Transformers are the hard constraint (>24–36 month lead times; 2026E ceiling 13.2GW) and GEV's DC-relevant transformer revenue CAGRs 79.6% ('23–'26) and 20.0% ('26–'30E), with the Prolec JV consolidation adding share — "GEV's standard product market share gain opportunity still is not fully reflected in forward estimates."

**Insight density:** A proprietary six-constraint supply model, a 12GW 2025 delivery deficit, Aterio / Data Center Hawk channel data, $770B CY26E hyperscaler capex. The GEV datapoints are company disclosure, but the *framework* around them is original.

**Data support:** 38 exhibits, two GEV-specific (Ex. 27/28).

**Event context:** Post-1Q26, and it folds in the Prolec JV — before 2Q26.

**Why 7:** Best available answer to "what is actually constraining GEV's revenue," with numbers, and it is the only report that quantifies GEV's transformer/electrification mix separately from gas.

---

### 6/10 — HSBC, 04-24 · *US Nuclear: SMRs to fuel AI dominance* (59 pp)

**Why Hold:** "GE Vernova (GEV US, Hold, TP USD740.00, CMP USD991.30)", priced at the close of 21 Apr 2026 — TP sits ~25% *below* the market, with no estimate change and no GEV earnings model. The Hold is a pure valuation verdict, asserted rather than re-underwritten, and it predates GEV's 1Q26 print (22 Apr) by one day.

**What you actually learn (all constructive, oddly):** FOAK BWRX-300 (300 MW) under construction at OPG Darlington, "commissioning targeted for 2029"; TVA's Clinch River filing for 800 MW of SMRs with a "USD400m DOE grant"; SMR "could be USD2bn business by early-to-mid 2030s" with revenue that "could pull forward"; up to "USD40bn of Japanese government investments" behind GEV-Hitachi SMRs in Tennessee/Alabama; an installed base of "65 large boiling water reactors"; CEO Strazik's "5 GW" uprate opportunity.

**Insight density:** Genuinely differentiated on SMR commercialisation — funding, counterparties, dates. Thin on earnings impact.

**Event context:** Priced one day before 1Q26; HSBC's newest GEV note listed is 30 Jan 2026, i.e. the Hold is a stale view by publication.

**Why 6:** A real GEV company page (p.36) with dated, funded nuclear catalysts — the SMR optionality nobody else in this set sizes. Discounted because nuclear is not GEV's earnings driver and the 25% TP gap is never justified.

---

### 6/10 — Bernstein, 08-20 · *30 exhibits on the state of cooling and electrical equip. procurement* (27 pp)

**Why Outperform:** "GEV O USD 987.46 → PT $1,298" — the call is maintained, and the evidence is a **primary channel survey** (n=50, ~40% hyperscalers). GEV wins >20% of power spend for 14% of respondents (22% of hyperscalers), versus Schneider at 64%; GEV sits in the leading group on SST purchase intent.

**Insight density:** New, survey-based share data on exactly the question that matters — whether GEV is gaining or losing data-centre electrical share. The honest caveat is that GEV's slice is three share bars and two SST charts; the report's centre is Schneider/Vertiv/Eaton.

**Data support:** 27 pp, ~30 exhibits.

**Event context:** ~1 month after 2Q26; no GEV-specific trigger.

**Why 6:** The only *forward survey* evidence on GEV's competitive share in the set, and it is mildly uncomfortable — a 14%/64% share split is not the profile of a share-gainer in electrical.

---

### 6/10 — J.P. Morgan, 07-29 · *Weichai Power: Positive read-throughs from BE, Innio, GE Vernova* (14 pp)

**Why bullish:** "GE Vernova GEV US OW 943.38 1330.00 41%" — and the PT was **raised from $1,302 to $1,330 in the six days** since the 07-23 note. Content: "GE Vernova reported strong 2Q orders of $24.2B, well above expectations"; expansion to 20GW of gas power "is complete, targeting 24 GW in FY28 and 30 GW by 2030"; "FY26 FCF guidance raised to $11.5–12.5B, up from $6.5–7.5B previously"; data-centre orders at record levels with pricing power and supply constraints "persistent."

**Insight density:** ~2 paragraphs restating the 2Q26 print. The differentiated value is the **three-company triangulation** — Bloom Energy DC orders >2× all FY25, Innio data-centre book-to-bill 6.3× with capacity to 5GW by YE26 and 10GW by 2030 — evidence that behind-the-meter demand is not rolling over.

**Data support:** 2 exhibits (AIDC power comparison; machinery sector comparison).

**Event context:** Six days after 2Q26; also follows Weichai Group's 21 Jul A-share increase.

**Why 6:** Thin on GEV per se, but it captures a **PT revision in flight** ($1,302 → $1,330 inside a week) and the cleanest cross-check on whether the AI-power order cycle is decelerating.

---

### 5/10 — J.P. Morgan, 03-09 · *Clean Energy and Power Infrastructure: 2026 March Madness* (21 pp)

**Why Overweight:** GEV is a **top pick** — "owing to backlog visibility, increasing pricing in pipeline, and solid cash flow/balance sheet"; page-9 box "GEV/OW/$215bn cap/$1,000 PT"; coverage row "GE Vernova, GEV, Strouse, OW, $815.01, $1,000".

**Evidence:** "GEV backlog+SRA 83 GW at YE25, up from 36 GW at YE24"; "Global YTD orders up 72% y/y. North America orders up 160% y/y"; "increased pricing provides visibility into margin upside"; "gas turbine capacity sold out thru YE29 during 1H26."

**Insight density / data:** A 2025-in-review recap; ~7 exhibits over ~10 content pages, one GEV table row. The 83GW / +72% / +160% figures are the whole GEV payload.

**Event context:** Priced 6 Mar 2026, ~5 weeks after 4Q25; flags pending FEOC guidance, Section 232 and AD/CVD tariffs.

**Why 5:** Five readable bullets with three useful numbers, no new analysis. The **twin note from the same day** (`184445214585182`, *Make the Grid Great Again*, 61 pp) carries the full SOTP — 20× FY29E Power EBITDA, 6× FY29E Wind (discount to Vestas), 16× FY28E Electrification — and is the one to read if you read only one JPM March document: **6/10**.

---

### 5/10 — UBS, 03-13 · *China Energy Transition: Buy China Power Equipment* (45 pp)

**Why Buy:** "GE Vernova* GEV.N Buy 936.0 841.3 227,143 36.5 48% 12.7 40%" (Figure 19) — Buy, PT $936 vs $841.3, 2027e P/E 36.5×, 2026–28e net-profit CAGR 48%, ROE 40%. GEV is the **re-rating benchmark**: Chinese names (Dongfang/Harbin, EPS CAGR 28–36% vs GEV's 16%) should re-rate toward GEV's multiple even though they grow faster.

**Evidence:** "GE Vernova's Q425 orders jumped 79% YoY," accelerating from +39% in 9M25; Siemens' EUR1bn expansion lands only in 2028, so supply stays tight "into 2030 and beyond."

**The genuinely additive GEV work:** Figure 8 SOTP — Power EBIT $5,406m and Electrification+Wind $2,989m at 20–25× implies **42–45× 2027e PE for GEV's gas-turbine segment**, the market's discount reflecting "the drag from GE Vernova's loss-making wind turbine business." Plus the PE-discount series: Dongfang/Harbin's discount to GEV narrowed to 43% from a 52% average (PEG 76%→65%).

**Event context:** Post-4Q25 (+79% source), Siemens capacity news, US hyperscaler capex upgraded +59% YoY for 2026e.

**Why 5:** The Figure 8 SOTP and the wind-drag quantification are worth real time for a GEV owner, but GEV's own Buy is asserted in a 45-page China report.

---

### 5/10 — Bernstein, 06-30 · *The Peaker you can't see: Can VPPs become the MVP in the U.S.?* (20 pp)

**Why Outperform:** "GEV O USD 1,045.17 → PT $1,206" — sustained via **indirect optionality**: FERC Order 2222 and the virtual-power-plant market, in which GEV's FLEXIQ EMS is positioned. The note contains no GEV financials.

**Insight density:** Strong on the VPP/peaker theme, essentially zero GEV-specific analysis. The link between VPP growth and GEV's earnings is asserted, not modelled.

**Data support:** ~20 pp; no GEV exhibits.

**Event context:** Between 1Q26 and 2Q26; no GEV trigger.

**Why 5:** Read it for the demand-flexibility theme and GEV's optional EMS position; do not read it for a GEV position.

---

### 4/10 — HSBC, 03-06 · *China power equipment: How Chinese gas turbines go overseas* (18 pp)

**Why Hold:** "GE Vernova GEV US Hold 841.27 740.0 −12% 226,747 47.6x 57.5x 40.6x 47% 31% 33% 20.5x 15.6x 11.7x 55% 1.05" — the **only Hold among the overseas producers** (Siemens Energy Buy +11%; Mitsubishi NR). The negative is valuation, −12% to target.

**The twist — tightness is the report's whole backbone:** GEV "Capacity sold out through 2029, delivery slots stretching well into late 2030s… Order backlog was 83GW as end-CY2025"; ~20GW capacity by mid-2026, ~24GW by 2028; 4–5 year lead times at GEV/Siemens/Mitsubishi are precisely why Chinese OEMs get a window. GEV is the **bull-case ceiling**: Dongfang's aggressive case assumes "ASP/margin similar to GE Vernova" and still yields only 30% upside (GEV 5.0–5.5 vs Dongfang 2.0–5.0 RMB/watt).

**Event context:** Post-4Q25 (the 83GW figure); trigger is Dongfang's early-2026 deposit for 10 G50 units from a Canadian data-centre customer.

**Why 4:** A handful of sharp capacity datapoints (sold-out-through-2029, 20→24GW) inside a China-OEM note where GEV is one comp row.

---

### 4/10 — J.P. Morgan, 06-18 · *Yingliu Electromechanical: Customer updates reinforce OW case* (10 pp)

**Why Overweight:** Not argued — GEV appears only in Table 2, "Global gas turbine components and OEM comps": "GE Vernova GEV US OW 1,049 1,302 24% 281,850 60% 50 44 32" — OW, PT $1,302, 24% upside, ~$282bn cap, YTD +60%, P/E 50×/44×/32× FY26/27/28E.

**Why it can still matter:** GEV is the **valuation yardstick** — Yingliu trades "at 29x FY28E P/E, below Howmet, GE Vernova and Jereh," so GEV's 32× FY28E is the premium being measured against. And the demand frame: "AI capex spending of US$5.5T through 2030, up from US$5.1T," data-centre power capacity "raised to 138GW through 2030 from 122GW," and gas-turbine demand "expected to exceed 100GW annually from 2026 to 2035 while 2026 manufacturing capacity is only 64GW."

**Event context:** After 1Q26 and before 2Q26; triggers were Baker Hughes' 2026–31 renewal, a Siemens Energy management visit, and a rotation out of AI-power names.

**Why 4:** Ten minutes for the gas-turbine supply-chain read; zero GEV-specific research.

---

### 4/10 — UBS, 05-03 · *US Electrical Equipment & Multi-Industry: Top 10 takes from earnings* (12 pp)

**Why Buy:** "GE Vernova Inc — GEV.N — Buy — US$1,062.95 — 01 May 2026" — **no price target anywhere in the PDF**; valuation described only as "a combination of relative P/E, EV/EBITDA, and EV/sales."

**Why bullish (two sentences):** "Our estimates went up the most for NVT, GEV and VRT"; "GEV and VRT are the most direct beneficiaries of our structural growth outlook," ahead of JCI, TT, MOD, NVT. Support is sector-level only: AI-exposed industrials +14% organic vs +1% non-AI, a record 45pp dispersion.

**Why 4:** Skimmable and honest, but for GEV it is two sentences with no numbers, no PT and no primary work — and it is the only rated report here with no target to test.

---

### 3/10 — Bernstein, 09-14 · *Powering AI: The modular advantage* (57 pp, 81 exhibits)

**Why the score is low despite the size:** "U.S Power and Energy Transition: We rate GEV Outperform (PT $1,298)" — and then **no GEV thesis**. Value capture is attributed to Schneider, Vertiv and Eaton ("the big-3"). GEV's only substantive appearance is Exhibit 17: "Bloom Energy has outperformed GEV by almost 150pp ytd" (GEV +44% vs Bloom +191%), a price-return chart with no view expressed. Background only: heavy-duty gas turbines solved the grid-connection bottleneck (5–7 years → 1.5–2 years); the next binding constraint is construction/MEP.

**What it is good for:** Highly differentiated on modularisation — a bottom-up credibility-adjusted pipeline of ~126GW for 2026–30, $0.9B/GW incremental PV with ~25% to OEMs, $1.9B/GW power-module TAM, ~3pp share shift. Excellent theme piece; near-zero GEV content.

**Event context:** ~2 months after 2Q26, in the window where GEV lagged fuel-cell peers; no GEV trigger cited.

**Why 3:** 57 pages and 81 exhibits in which GEV is a comp-table row and a line on a chart. The freshest report in the set is also one of the emptiest for GEV — a good example of why "newest" ≠ "most useful."

---

### 3/10 — Goldman Sachs, 08-06 · *GS SUSTAIN: AI DATA CENTERS* (36 pp)

**Why Buy:** Not argued. Exhibit 34 lists "GEV GE Vernova United States 271.1 $1017.96 92% 69% ✓ Power generation, renewable energy −23%" — Buy-rated in the Reliability basket, CROCI 92nd percentile, sales growth 69th percentile, and the awkward footnote that sustainable funds are −23% overweight. Disclosure appendix: "GE Vernova (Buy, $1,018.53)."

**The one GEV datapoint:** "GE Vernova highlighted on its July 22 2Q26 earnings call that by the end of 2026 it expects to have more than 50% of its 2031 capacity contracted."

**Useful backdrop:** 2030 global data-centre power demand +170% vs 2025 (raised from +117%), ~1,100 TWh cumulative; hyperscaler capex + R&D >$1trn in 2026e; parts constraints pushing behind-the-meter gas to ~30% of data-centre growth through 2030; US power demand +3.5% CAGR to 2030.

**Why 3:** A strong thematic read on AI power demand in which GEV is a Buy-rating row, one quoted sentence and one of 36 exhibits. The 2031-contracted figure is the only thing a GEV owner needs to take away.

---

### 3/10 — Goldman Sachs, 04-01 · *US Conviction List: Directors' Cut, April 2026* (75 pp)

**Why the score is low:** **GEV is not on the list.** The April additions are Citizens Financial and Carlisle; the removals are BAC and HSY. GEV carries no rating, no target and no price in the document. It appears twice as a **supplier reference**:
- DUK (Buy, PT $142): "DUK's ability to build at scale with its partnership with GEV gives it a competitive advantage" — the utility "secured 20 natural gas turbines" into the 2030s.
- NVT (Buy, PT $150): "the long cycle value chain (e.g., gas turbine suppliers such as GEV) is booking DC orders out to 2030," so NVT's order acceleration (orders +30% after +65%) is "just the beginning."

**Why 3:** A 75-page monthly list GEV is not on. Its only use is as independent confirmation that utilities and electrical OEMs are still booking GEV-linked orders into the 2030s. The April macro backdrop (Brent $85/bbl, Strait of Hormuz flows at 6% of normal) is interesting but not GEV.

---

## Disagreement flags — where the set actually splits

> ⚠️ **HSBC Hold $740 vs the rest of the street.** HSBC is the **only** house below the market: $740 against a $1,149.19 close on 24 Apr (**−35.6%**) and $788.35 on 6 Mar (**−6.1%**) — and it never re-underwrote after 1Q26 or 2Q26. Meanwhile JPM went $1,000 → $1,302 → $1,330 and Bernstein to $1,298. That is a **~80% spread on fair value** at the same share price. Note *why*: HSBC's Hold is a valuation verdict on a report built to argue that gas-turbine capacity is sold out through 2029 — its own evidence contradicts its rating. Do not average them; the split *is* the signal.

> ⚠️ **Backlog numbers don't reconcile across the set.** GEV backlog + SRA: **36GW** (YE24) → **83GW** (YE25, HSBC/JPM) → **110GW** year-end 2026 target (Jefferies, May) → **125GW** raised target (JPM, 23 Jul). The 4Q25 print itself is quoted as both "83GW backlog" and "50→54→62GW" of gas backlog + reservations (MS, Jan). Some of this is definitional (total backlog vs gas backlog vs SRA); some looks like error. Treat any single GW figure with care.

> ⚠️ **Rating inflation on thin evidence.** 13 of 15 calls are Buy/OW/Outperform, but only 6 reports argue a GEV position. The two largest reports (Bernstein 57 pp, GS 75 pp) contain ~zero GEV analysis while carrying a positive rating. The rated universe here is far more confident than the underlying research is deep.

---

## How the data is stored (as of 2026-09-15)

**Two databases, one join key.** The Research Lens page reads from both.

### 1. `db/zsxq.db` — the PDF library (~255 MB)

One row per downloaded PDF in **`pdf_files`** (13,515 rows; 13,159 with a `local_path`, 12,198 with a summary, 13,117 with a page count, 388 OCR-cached).

| Column | What it is |
|---|---|
| `file_id` | Primary key — zsxq's own document ID |
| `name`, `topic_title`, `summary` | Filename, forum thread title, and the Chinese 精华翻译 summary |
| `local_path` | Where the PDF bytes actually live — `/Users/x/Downloads/zsxq_reports/<YYYY_MM_DD>/…` (the DB stores only the pointer, **not** the PDF) |
| `bank`, `page_count`, `tickers` | Source broker, page count, extracted tickers |
| `ai_related`, `robotics_related`, `semiconductor_related`, `energy_related` | Classification flags |
| `user_rating`, `claude_rating` | 1–5 stars; 3/4/5 = "worth reading", written **only** through `scripts/set_zsxq_ratings.py` → `zsxq_common.set_claude_rating()` |
| `comment`, `ocr_text`, `ocr_at` | Manual note and the OCR cache |
| `create_time` | Ingestion time |

Plus an **FTS5 trigram index `pdf_files_fts`** (13,515 rows) — this is what the GEV grep ran against — and `pdf_cards` (6 rows, no embeddings yet).

### 2. `db/stock_price_target.db` — the calls (~5.8 MB)

One row in **`price_targets`** per **(ticker × broker × report)** — 5,842 rows, 1,830 distinct tickers, 3,803 with a numeric price target. GEV now has **15 rows** (was 3 before this session).

| Column | What it is |
|---|---|
| `company_ticker`, `company_name`, `research_institute`, `rating`, `price_target`, `target_currency` | The call |
| `catalyst` | Free-text catalyst note |
| `report_file_id` → **join to `pdf_files.file_id`** | The PDF this call came from |
| `report_pdf_filename`, `report_url` | Filename and source link |
| `report_date` | Publication date |
| `report_date_price`, `report_date_market_cap`, `price_currency` | **Point-in-time** price and cap — the close on the report date |
| `upside_pct` | Computed from the two above — **reproducible offline** |
| `created_at` | Row insert time |

Two unique keys guard against duplicates: `UNIQUE(company_ticker, research_institute, report_file_id)` and `uq_ticker_broker_date (ticker, broker, report_date)` — the latter is why only one of the two JPM 2026-03-09 notes surfaces. Writes go **only** through `scripts/persist_pts.py` → `stock_price_target_db.upsert_target()` (default `INSERT OR IGNORE`; `--replace` for the analyze path; `--no-prices` to skip yfinance). Extraction rules: `reference/pt_extraction.md`.

### 3. What is *not* stored — the price series

**Daily OHLC is never persisted.** The lens (`zsxq_viewer.py` → `_research_lens_reports()` + `_research_lens_price_history()`, template `templates/research_lens.html`) pulls the daily series **live from yfinance** on each page load, for the window (earliest `report_date` − 14 days … latest + 14 days). It fetches up to `LIMIT 18` reports ordered by `report_date DESC`, dedupes by `file_id`, re-sorts ascending and caps at 18. Markers need a finite price — `chartValue()` uses the yfinance close on the date, falling back to `report.price` — and stacked markers cluster into one diamond.

The point-in-time close **on** the report date is the exception: it is frozen into the row (`report_date_price`), which is what makes `upside_pct` auditable months later without re-fetching anything.

**Practical consequence:** the chart is only as good as yfinance on the day you open it. Delete the DB row and you lose the report; the PDF survives on disk but nothing points at it.

**Also note:** `db/stock_price_target.db` is **gitignored** (`.gitignore` `*.db`; only `db/zsxq.db`, `db/notes.db`, `db/alert_monitor.db` are re-included) — so tonight's 12-row update exists on this machine only and is not in version control. The PDFs themselves are likewise outside the repo.

---

*All 15 reports were read in full from their local PDFs; every rating, price target and page count above was verified directly against `price_targets` and `pdf_files`.*
