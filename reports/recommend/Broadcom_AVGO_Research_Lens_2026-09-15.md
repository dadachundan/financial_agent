# Broadcom (AVGO) — zsxq Research Lens Reading List

**Generated:** 2026-09-15 · **Ticker:** AVGO (Broadcom Inc.) · **Lens:** http://localhost:5001/zsxq/research-lens?ticker=AVGO

**Sources:** `db/stock_price_target.db` → table `price_targets` (**79 AVGO rows**, one per ticker × broker × report — 56 carry a price target, the other 23 are rating-only, and all 79 have a frozen report-date close) joined to `db/zsxq.db` → table `pdf_files` (the PDFs themselves, on disk under `/Users/x/Downloads/zsxq_reports/`).

**Scan method:** trigram full-text search of the zsxq PDF library for `AVGO` / `Broadcom` (`lens_scan.py AVGO --name "Broadcom" --limit 120 --summary-chars 1200`) → **122 candidates**. Triage kept **87** that carry a rating or a price target *on AVGO* (58 that argue a case, 20 that carry a real call inside a sector note, plus 9 more recovered from the re-triage below) and dropped 35 — 29 that only mention the name in passing, 13 with no AVGO content at all (comp-table rows, read-across notes about other companies, sector pieces that cite Broadcom once), and 5 first-pass "unreadable" files that OCR later resolved as mentions-only. Of the 87, four turned out to be Chinese translations or byte-identical twins of other keepers and were folded away, leaving the **83 scored below**. Every one was read in full from its local PDF, except **two whose bytes are missing from disk** (below; they are the only gaps in the book).

**Feed shape:** an extraordinarily one-sided book that has been *raised* into a 29% drawdown. Of the 80 entries that carry a house rating, **every single one is Buy, Overweight or Outperform** — there is no Neutral and no Sell anywhere in the AVGO corpus. Price targets only ever moved up, with one exception (HSBC). And yet the stock peaked at **$480.81 on 2026-06-02** and closed **$339.27 on 2026-09-15** — and the newest target in the book, Bernstein's **$575** dated 14 Sep 2026, sits **+69.5%** above that close. The lens below is ordered by how much you learn about Broadcom per minute of reading, not by how strongly the house rates it.

---

## How to read the score

| Score | Meaning |
|---|---|
| **8–10** | Primary AVGO work: proprietary data or a quantified argument about Broadcom itself. Read it. |
| **6–7** | Real AVGO content (a full page, a channel check, an SOTP) inside a report about something else, or a short but genuinely fresh AVGO read. Worth the time. |
| **4–5** | A few sharp AVGO datapoints — a CoWoS allocation, a TPU unit number — but Broadcom is a comp row. Skim that section only. |
| **0–3** | Broadcom is a name in a table or a line on a chart. The report may be excellent; it is not AVGO research. Skip unless you want the theme. |

The score weights four things: (1) **is there an AVGO thesis at all** — rating + why, or just a row in a valuation table; (2) **insight density** — proprietary/channel data vs restated consensus; (3) **data support** — exhibits, models, SOTP builds, verbatim management quotes; (4) **event context** — was it written around a print, a deal or a regulatory trigger (a dated, testable call) or in a quiet patch. Length earns nothing: the 41-pp Bernstein data-center tracker scores 3, the 22-pp UBS OpenAI-day model update scores 9.

**Score distribution across the 83 entries:** 9/10 → 15 · 8/10 → 19 · 7/10 → 14 · 6/10 → 8 · 5/10 → 4 · 4/10 → 7 · 3/10 → 9 · 2/10 → 5 · 1/10 → 2.

---

## The book at a glance

The latest persisted call from each house (Bernstein and J.P. Morgan both refreshed in the last month; UBS has not published a readable AVGO target since 18 May):

| House | Latest persisted call | Date | PT | Report-date close | Implied upside |
|---|---|---|---|---|---|
| Bernstein | Outperform | 2026-09-14 | **$575** | $344.72 | +66.8% |
| Goldman Sachs | Buy | 2026-09-08 | **$540** | $368.56 | +46.5% |
| J.P. Morgan | Overweight | 2026-08-19 | **$580** | $362.48 | +60.0% |
| Morgan Stanley | Overweight | 2026-08-10 | **$502** | $422.40 | +18.8% |
| Citi | Buy | 2026-06-04 | **$500** | $418.25 | +19.5% |
| HSBC | Buy | 2026-05-26 | **$450** | $421.34 | +6.8% |
| UBS | Buy | 2026-05-18 | **$490** | $420.05 | +16.7% |
| BofA | Buy | 2026-05-13 | **$450** | $416.13 | +8.1% |

---

## Ranked list — every AVGO report, best read first

| Score | Report | Pp · Date | AVGO stance & PT | Price on date → upside | Open |
|---|---|---|---|---|---|
| **9/10** | **UBS** — *Updating Model after a Series of Supply Chain Checks And New Details on OpenAI Partnership.…* | 22 · 2025-10-14 | Buy, PT **$415** | $342.21 → **+21.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585128242148154/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89Updating%20Model%20after%20a%20Series%20of%20Supply%20Chain%20Checks%20And%20New%20Details%20on%20OpenAI%20Partnership.%20Remain%20Bullish-251014.pdf) |
| **9/10** | **UBS** — *US Semiconductors and Semi Equipment： SemiBytes， AVGO Tweaks， TSMC Capex， US China Update* | 17 · 2025-10-20 | Buy, PT **$415** | $347.29 → **+19.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585114112555244/UBS-US%20Semiconductors%20and%20Semi%20Equipment%EF%BC%9ASemiBytes%EF%BC%8CAVGO%20Tweaks%EF%BC%8C%20TSMC%20Capex%EF%BC%8C%20US%20%20China%20Update-251020.pdf) |
| **9/10** | **HSBC** — *Buy： Potent mix of ASIC and networking upside* | 19 · 2025-11-24 | Buy, PT **$535** | $375.85 → **+42.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812824512185242/HSBC-Broadcom%20Inc%20%EF%BC%88AVGO.US%EF%BC%89Buy%EF%BC%9A%20Potent%20mix%20of%20ASIC%20and%20networking%20upside-251124.pdf) |
| **9/10** | **UBS** — *US Semiconductors and Semi Equipment： SemiBytes： Thoughts on TPU and AVGO Preview，…* | 23 · 2025-11-30 | Buy, PT **$472** | $400.71 → **+17.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212842881484811/UBS-US%20Semiconductors%20and%20Semi%20Equipment%EF%BC%9ASemiBytes%EF%BC%9A%20Thoughts%20on%20TPU%20and%20AVGO%20Preview%EF%BC%8C%20Technology%20Conference%20Preview-251130.pdf) |
| **9/10** | **HSBC** — *Buy： AI narrative and earnings still not fully priced in* | 13 · 2025-12-08 | Buy, PT **$535** | $398.86 → **+34.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184511584282412/HSBC-Broadcom%20Inc%20%EF%BC%88AVGO.US%EF%BC%89Buy%EF%BC%9A%20AI%20narrative%20and%20earnings%20still%20not%20fully%20priced%20in-251208.pdf) |
| **9/10** | **J.P. Morgan** — *Google TPU Outlook Getting Stronger FY26 And FY27； 18 Month Lead Implies Shrinking…* | 11 · 2026-01-25 | OW, PT **$475** | $318.88 → **+49.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585524212515484/J.P.%20Morgan-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Google%20TPU%20Outlook%20Getting%20Stronger%20FY26%20And%20FY27%EF%BC%9B%2018%20Month%20Lead%20Implies%20Shrinking%20Negligible%20Volumes%20For%20COT%20Initiatives%EF%BC%9B%20Reit%20OW-260125.pdf) |
| **9/10** | **Morgan Stanley** — *AVGO FAQ： What will it take for the stock to outperform？* | 19 · 2026-02-03 | OW, PT **$462** | $319.15 → **+44.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184428515258212/Morgan%20Stanley-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89AVGO%20FAQ%EF%BC%9A%20What%20will%20it%20take%20for%20the%20stock%20to%20outperform%EF%BC%9F-260203.pdf) |
| **9/10** | **UBS** — *Increasing Estimates On TPU Unit Inflection； C2027E EPS -$18* | 31 · 2026-02-10 | Buy, PT **$475** | $339.19 → **+40.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585512125541514/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89Increasing%20Estimates%20On%20TPU%20Unit%20Inflection%EF%BC%9B%20C2027E%20EPS%20-%2418-260210.pdf) |
| **9/10** | **UBS** — *Strong Results & Guidance； Raise Estimates， Maintain $475 PT* | 27 · 2026-03-05 | Buy, PT **$475** | $331.55 → **+43.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585552414545114/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89%20Strong%20Results%20%26%20Guidance%EF%BC%9B%20Raise%20Estimates%EF%BC%8C%20Maintain%20%24475%20PT-260305.pdf) |
| **9/10** | **UBS** — *Increasing 2027 TPU Units Once Again* | 22 · 2026-04-13 | Buy, PT **$475** | $379.15 → **+25.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812241252442142/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89Increasing%202027%20TPU%20Units%20Once%20Again-260413.pdf) |
| **9/10** | **Citi** — *Preview – Raising TP to $500； Maintain Buy* | 21 · 2026-05-12 | Buy, PT **$500** | $418.64 → **+19.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585425518412254/CITI-Broadcom%20Inc%20%EF%BC%88AVGO.US%EF%BC%89%20Preview%20%E2%80%93%20Raising%20TP%20to%20%24500%EF%BC%9B%20Maintain%20Buy-260512.pdf) |
| **9/10** | **UBS** — *FQ2-26 (Apr) Preview-Raising PT, Adjusting Estimates* | 21 · 2026-05-18 | Buy, PT **$490** | $420.05 → **+16.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184121514242442/UBS-Broadcom%20Inc.%20FQ2-26%20%28Apr%29%20Preview-Raising%20PT%2C%20Adjusting%20Estimates-260518.pdf) |
| **9/10** | **Citi** — *Management Callback Notes* | 11 · 2026-06-04 | Buy, PT **$500** | $418.25 → **+19.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184155521585442/CITI-Broadcom%20Inc%20%EF%BC%88AVGO.US%EF%BC%89%20Management%20Callback%20Notes-260604.pdf) |
| **9/10** | **Morgan Stanley** — *North America Expectations miss amid very strong demand* | 17 · 2026-06-04 | OW, PT **$502** | $418.25 → **+20.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812488522258422/MS-Broadcom%20Inc.%20-%20North%20America%20Expectations%20miss%20amid%20very%20strong%20demand-260604.pdf) |
| **9/10** | **Morgan Stanley** — *In Defense of AVGO’s ASIC Share* | 16 · 2026-07-14 | OW, PT **$502** | $389.11 → **+29.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/181282245822542/Morgan%20Stanley-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89In%20Defense%20of%20AVGO%E2%80%99s%20ASIC%20Share-260714.pdf) |
| **8/10** | **Mizuho** — *MizuhoSecuritiesUSALLC_AIServerSupplyChainCall-UpsidetoAVGO, SomeChallengesWithPeers-AdjPTs* | 9 · 2025-05-16 | OP, PT **$250** | $232.64 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214884222148151/MizuhoSecuritiesUSALLC_AIServerSupplyChainCall-UpsidetoAVGO%2CSomeChallengesWithPeers-AdjPTs.pdf) |
| **8/10** | **Goldman Sachs** — *Very strong quarter and AI customer traction， tempered by lack of guide~up for FY26* | 8 · 2025-12-11 | Buy, PT **$450** | $404.11 → **+11.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184511858188112/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9A%20Very%20strong%20quarter%20and%20AI%20customer%20traction%EF%BC%8C%20tempered%20by%20lack%20of%20guide~up%20for%20FY26-251211.pdf) |
| **8/10** | **Bernstein** — *FQ425 recap~The fickle heart's desire...* | 24 · 2025-12-12 | OP, PT **$475** | $357.92 → **+32.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812844488525112/Bernstein-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89FQ425%20recap~The%20fickle%20heart%27s%20desire...-251212.pdf) |
| **8/10** | **Morgan Stanley** — *AI acceleration into 2026* | 16 · 2025-12-12 | OW, PT **$462** | $357.92 → **+29.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184511848484422/Morgan%20Stanley-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89AI%20acceleration%20into%202026-251212.pdf) |
| **8/10** | **UBS** — *CEO CFO Meeting Suggests Friday's Move Is a Buying Opportunity* | 23 · 2025-12-15 | Buy, PT **$475** | $337.92 → **+40.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212841582144421/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89CEO%20CFO%20Meeting%20Suggests%20Friday%27s%20Move%20Is%20a%20Buying%20Opportunity-251215.pdf) |
| **8/10** | **J.P. Morgan** — *Semiconductors Semi Cap Equipment： 2026 Outlook： Expect Another Year Of Stock…* | 34 · 2025-12-16 | OW, no PT | $339.40 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415821588115258/J.P.%20Morgan-Semiconductors%20Semi%20Cap%20Equipment%EF%BC%9A2026%20Outlook%EF%BC%9A%20Expect%20Another%20Year%20Of%20Stock%20Outperformance%EF%BC%9B%20Continued%20Strong%20AI%20Spending%20And%20Accelerating%20Cyclical%20Recovery%20In%20Industrial%20Auto%EF%BC%9B%20Favor%20AVGO%EF%BC%8C%20MRVL%EF%BC%8C%20ADI%EF%BC%8C%20MU%EF%BC%8C%20KLAC%EF%BC%8C%20SNPS-251216.pdf) |
| **8/10** | **Bernstein** — *Vegas baby...Takeaways from a CES investor meeting with the Semiconductor Solutions Group…* | 15 · 2026-01-09 | OP, PT **$475** | $343.70 → **+38.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184422412422542/Bernstein-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Vegas%20baby...Takeaways%20from%20a%20CES%20investor%20meeting%20with%20the%20Semiconductor%20Solutions%20Group%20President-260109.pdf) |
| **8/10** | **Goldman Sachs** — *AMERICAS TECHNOLOGY AI Unit Economics： GPUs vs. ASICs and the inference cost curve~Buy AVGO…* | 14 · 2026-01-20 | Buy, PT **$450** | $331.38 → **+35.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184424284452142/Goldman%20Sachs-AMERICAS%20TECHNOLOGY%20AI%20Unit%20Economics%EF%BC%9A%20GPUs%20vs.%20ASICs%20and%20the%20inference%20cost%20curve~Buy%20AVGO%20and%20NVDA-260120.pdf) |
| **8/10** | **UBS** — *Thinking Through SOTP Amid Software Deep Dive + EPS Preview* | 25 · 2026-02-23 | Buy, PT **$475** | $329.13 → **+44.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212281541224421/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89Thinking%20Through%20SOTP%20Amid%20Software%20Deep%20Dive%20%2B%20EPS%20Preview-260223.pdf) |
| **8/10** | **Goldman Sachs** — *Very strong guidance and commentary on key debates should drive stock higher - Buy* | 8 · 2026-03-04 | Buy, PT **$480** | $316.36 → **+51.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812225452244522/GS-Broadcom%20Inc.%20%28AVGO%29-Very%20strong%20guidance%20and%20commentary%20on%20key%20debates%20should%20drive%20stock%20higher%20-%20Buy-260304.pdf) |
| **8/10** | **Bernstein** — *FQ126 recap~Line 'em up and knock 'em down...* | 24 · 2026-03-05 | OP, PT **$525** | $331.55 → **+58.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184442151414552/Bernstein-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89%20FQ126%20recap~Line%20%27em%20up%20and%20knock%20%27em%20down...-260305.pdf) |
| **8/10** | **Goldman Sachs** — *Partnership with Meta further reinforces Broadcom’s technology advantage in custom silicon…* | 8 · 2026-04-14 | Buy, PT **$480** | $380.18 → **+26.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184418854484452/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%20Partnership%20with%20Meta%20further%20reinforces%20Broadcom%E2%80%99s%20technology%20advantage%20in%20custom%20silicon%20and%20AI%20networking~Buy-260414.pdf) |
| **8/10** | **J.P. Morgan** — *Expanded Meta Partnership Drives Confidence In A Strong Multi~Year Revenue Ramp； Adds To…* | 11 · 2026-04-15 | OW, PT **$500** | $396.09 → **+26.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415514885481218/J.P.%20Morgan-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Expanded%20Meta%20Partnership%20Drives%20Confidence%20In%20A%20Strong%20Multi~Year%20Revenue%20Ramp%EF%BC%9B%20Adds%20To%20Multi~GW%20Deals%20That%20Include%20Google%20Anthropic%20OpenAI-260415.pdf) |
| **8/10** | **J.P. Morgan** — *Maintains Lead In AI Networking Silicon； Next~Gen 3nm Tomahawk 6 Strong Ramp 2H26…* | 11 · 2026-06-02 | OW, PT **$500** | $480.81 → **+4.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415288442528448/J.P.%20Morgan-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Maintains%20Lead%20In%20AI%20Networking%20Silicon%EF%BC%9B%20Next~Gen%203nm%20Tomahawk%206%20Strong%20Ramp%202H26%202027~Fastest%20Ramp%20In%20Broadcom%20History%E2%80%A6AI%20Networking%20to%20Deliver%20%2445B%2B%20in%20FY27%E2%80%A6.Up-2x%EF%BC%9BReit%20OW-260602.pdf) |
| **8/10** | **Citi** — *Buyers of Pullback; Improved AI Visibility into 2028* | 15 · 2026-06-03 | Buy, PT **$500** | $478.47 → **+4.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184155215151152/Citi-Broadcom%20Inc%20%28AVGO.O%29%20Buyers%20of%20Pullback%3B%20Improved%20AI%20Visibility%20into%202028-260603.pdf) |
| **8/10** | **Goldman Sachs** — *Strong AI revenue momentum for 2027， despite modest near~term shortfall relative to…* | 9 · 2026-06-03 | Buy, PT **$525** | $478.47 → **+9.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184155215151812/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9A%20Strong%20AI%20revenue%20momentum%20for%202027%EF%BC%8C%20despite%20modest%20near~term%20shortfall%20relative%20to%20elevated%20expectations-260603.pdf) |
| **8/10** | **Bernstein** — *FQ226 recap~Wait for it...* | 24 · 2026-06-04 | OP, PT **$550** | $418.25 → **+31.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415288425488488/Bernstein-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Broadcom%20%EF%BC%88AVGO%EF%BC%89%EF%BC%9A%20FQ226%20recap~Wait%20for%20it...-260604.pdf) |
| **8/10** | **J.P. Morgan** — *Ignore The Noise - TPU v9 2nm ASIC Program On Track For CY28 Ramp - NO Delays; Secures Next…* | 10 · 2026-06-16 | OW, PT **$580** | $376.11 → **+54.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214522118552541/JPM-Broadcom%20Inc%20Ignore%20The%20Noise%20-%20TPU%20v9%202nm%20ASIC%20Program%20On%20Track%20For%20CY28%20Ramp%20-%20NO%20Delays%3B%20Secures%20Next%20Four%20Generations%20of%20TPU%20%28And%20Increasing%20Revenues%29%20On%20Prior%20GOOG-AVGO%20Five-Year%20Agreement-260616.pdf) |
| **8/10** | **J.P. Morgan** — *Samsung Multi~Year Memory Foundry MOU Implies - $1 Trillion of Cumulative Broadcom AI…* | 9 · 2026-07-27 | OW, PT **$580** | $383.22 → **+51.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814512851551822/J.P.%20Morgan-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89Samsung%20Multi~Year%20Memory%20Foundry%20MOU%20Implies%20-%20%241%20Trillion%20of%20Cumulative%20Broadcom%20AI%20Revenues%20Over%20the%20Next%205%20Years%20in%20Our%20View%EF%BC%9B%20Reiterate%20OW-260727.pdf) |
| **7/10** | **Goldman Sachs** — *Partnership with OpenAI reinforces Broadcom’s technology advantage in custom silicon* | 7 · 2025-10-13 | Buy, PT **$380** | $354.71 → **+7.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212851554142411/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89Partnership%20with%20OpenAI%20reinforces%20Broadcom%E2%80%99s%20technology%20advantage%20in%20custom%20silicon-251013.pdf) |
| **7/10** | **Goldman Sachs** — *4Q Preview： Expect solid quarter with strong momentum driving upside to AI revenue in 2026* | 6 · 2025-11-25 | Buy, PT **$435** | $382.88 → **+13.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812824888284282/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9A%204Q%20Preview%EF%BC%9A%20Expect%20solid%20quarter%20with%20strong%20momentum%20driving%20upside%20to%20AI%20revenue%20in%202026-251125.pdf) |
| **7/10** | **Goldman Sachs** — *1Q Preview： Expect a solid quarter， with continued AI momentum* | 6 · 2026-02-19 | Buy, PT **$450** | $332.76 → **+35.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184451881122882/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9A%201Q%20Preview%EF%BC%9A%20Expect%20a%20solid%20quarter%EF%BC%8C%20with%20continued%20AI%20momentum-260219.pdf) |
| **7/10** | **BofA** — *US Semiconductors Scaling AI with Photons-Primer on Optical Interconnects* | 46 · 2026-03-09 | Buy, PT **$450** | $344.48 → **+30.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415558411588228/Bofa-US%20Semiconductors%20Scaling%20AI%20with%20Photons-Primer%20on%20Optical%20Interconnects-260309.pdf) |
| **7/10** | **J.P. Morgan** — *Semiconductors： OFC Conference： Strong CY26~CY27 Optical Networking Setup， High Innovation，…* | 10 · 2026-03-19 | OW, PT **$500** | $318.67 → **+56.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585555812552214/J.P.%20Morgan-Semiconductors%EF%BC%9AOFC%20Conference%EF%BC%9A%20Strong%20CY26~CY27%20Optical%20Networking%20Setup%EF%BC%8C%20High%20Innovation%EF%BC%8CCopper%20and%20Optical%20Both%20Viable%20Paths%EF%BC%9BAVGO%20MRVL%20Best%20Positioned-260319.pdf) |
| **7/10** | **UBS** — *US Semiconductors： Stellar Optics and Fast~Paced Networking at OFC 2026* | 21 · 2026-03-22 | Buy, no PT | $309.37 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812224852525182/UBS-US%20Semiconductors%EF%BC%9AStellar%20Optics%20and%20Fast~Paced%20Networking%20at%20OFC%202026-260322.pdf) |
| **7/10** | **Bernstein** — *Many major multi Meta MTIA...* | 11 · 2026-04-15 | OP, PT **$525** | $396.09 → **+32.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812241182212282/Bernstein-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9AMany%20major%20multi%20Meta%20MTIA...-260415.pdf) |
| **7/10** | **UBS** — *Thoughts On Google’s TPU v8 Generation* | 14 · 2026-04-22 | Buy, PT **$475** | $421.98 → **+12.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415518828288188/UBS-Broadcom%20Inc.%EF%BC%88AVGO.US%EF%BC%89Thoughts%20On%20Google%E2%80%99s%20TPU%20v8%20Generation-260422.pdf) |
| **7/10** | **Goldman Sachs** — *1Q Preview： Expect strong guidance， with focus on FY27 AI revenue and XPU customer…* | 7 · 2026-05-19 | Buy, PT **$500** | $410.42 → **+21.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424481442544/Goldman%20Sachs-Broadcom%20Inc.%20%EF%BC%88AVGO.US%EF%BC%89%EF%BC%9A%201Q%20Preview%EF%BC%9A%20Expect%20strong%20guidance%EF%BC%8C%20with%20focus%20on%20FY27%20AI%20revenue%20and%20XPU%20customer%20engagements-260519.pdf) |
| **7/10** | **Morgan Stanley** — *Semiconductors Weekly Earnings Week 7 AVGO Preview* | 24 · 2026-05-31 | OW, PT **$485** | $446.06 → **+8.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585412584454154/MS-Semiconductors%20Weekly%20Earnings%20Week%207%20AVGO%20Preview-260531.pdf) |
| **7/10** | **J.P. Morgan** — *Asian Tech： Key takeaways from Broadcom’s Apr~Q results* | 8 · 2026-06-04 | OW, no PT | $418.25 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585411124181524/J.P.%20Morgan-Asian%20Tech%EF%BC%9AKey%20takeaways%20from%20Broadcom%E2%80%99s%20Apr~Q%20results-260604.pdf) |
| **7/10** | **Bernstein** — *Global Memory Global Memory， NVIDIA & Broadcom： Quick thoughts on strategic partnerships* | 16 · 2026-07-27 | OP, PT **$550** | $383.22 → **+43.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412415482585488/Bernstein-Global%20Memory%20Global%20Memory%EF%BC%8C%20NVIDIA%20%26%20Broadcom%EF%BC%9A%20Quick%20thoughts%20on%20strategic%20partnerships-260727.pdf) |
| **7/10** | **J.P. Morgan** — *FY26 AI Sales On Track For $56B+ （up 180% Y Y+）； TPU Design Win Roadmap Remains Intact；…* | 9 · 2026-08-19 | OW, PT **$580** | $362.48 → **+60.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412841581841558/J.P.%20Morgan-Broadcom%20Inc%EF%BC%88AVGO.US%EF%BC%89FY26%20AI%20Sales%20On%20Track%20For%20%2456B%2B%20%EF%BC%88up%20180%25%20Y%20Y%2B%EF%BC%89%EF%BC%9B%20TPU%20Design%20Win%20Roadmap%20Remains%20Intact%EF%BC%9B%20Market%20Continues%20To%20Ignore%2012%20Years%20of%20Solid%20TPU%20Execution%20And%205%20Year%20TPU%20Agreement%EF%BC%9B%20Reit%20OW-260819.pdf) |
| **7/10** | **Goldman Sachs** — *Americas Technology： Semiconductors： Communacopia + Technology Conference 2026 ~ Day 1…* | 9 · 2026-09-08 | Buy, PT **$540** | $368.56 → **+46.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814882142255512/Goldman%20Sachs-Americas%20Technology%EF%BC%9A%20Semiconductors%EF%BC%9A%20Communacopia%20%2B%20Technology%20Conference%202026%20~%20Day%201%20Takeaways-260908.pdf) |
| **6/10** | **BofA** — *US Semiconductors TPU intensifies competitive race, but in a rising tide, Buy NVDA, AVGO…* | 8 · 2025-11-25 | Buy, PT **$400** | $382.88 → **+4.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812824852411512/Bofa-US%20Semiconductors%20TPU%20intensifies%20competitive%20race%2C%20but%20in%20a%20rising%20tide%2C%20Buy%20NVDA%2C%20AVGO%2C%20AMD-251125.pdf) |
| **6/10** | **B&M (巴芒投研, independent)** — *财报前瞻* | 9 · 2025-12-07 | no house call | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415825112552188/Broadcom%20Inc.%20%28AVGO%29%20_%E8%B4%A2%E6%8A%A5%E5%89%8D%E7%9E%BB.pdf) |
| **6/10** | **Morgan Stanley** — *Semiconductors： Weekly： Expect a strong AVGO outlook* | 21 · 2025-12-08 | OW, PT **$443** | $398.86 → **+11.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415822481542548/Morgan%20Stanley-Semiconductors%EF%BC%9AWeekly%EF%BC%9A%20Expect%20a%20strong%20AVGO%20outlook-251208.pdf) |
| **6/10** | **Bernstein** — *U.S. Semiconductors and Semiconductor Capital Equipment Bernstein Semi Cycle Tearsheet： Too…* | 74 · 2026-03-23 | OP, PT **$525** | $322.00 → **+63.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415552884525188/Bernstein-U.S.%20Semiconductors%20and%20Semiconductor%20Capital%20Equipment%20Bernstein%20Semi%20Cycle%20Tearsheet%EF%BC%9A%20Too%20much%20of%20a%20good%20thing%EF%BC%9F-260323.pdf) |
| **6/10** | **J.P. Morgan** — *TSMC（2330.TW） CoWoS and advanced back~end updates* | 16 · 2026-04-08 | OW, no PT | $350.08 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585548242148184/J.P.%20Morgan-TSMC%EF%BC%882330.TW%EF%BC%89CoWoS%20and%20advanced%20back~end%20updates-260408.pdf) |
| **6/10** | **J.P. Morgan** — *TSMC CoWoS and advanced back-end updates* | 16 · 2026-04-09 | OW, no PT | $354.35 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585544852854554/JPM-TSMC%20CoWoS%20and%20advanced%20back-end%20updates-260409.pdf) |
| **6/10** | **BofA** — *US Semiconductors-AI 2030-Stronger for longer for compute, memory, networking* | 32 · 2026-05-13 | Buy, PT **$450** | $416.13 → **+8.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415245581284888/Bofa-US%20Semiconductors-AI%202030-Stronger%20for%20longer%20for%20compute%2Cmemory%2C%20networking-260513.pdf) |
| **6/10** | **Morgan Stanley** — *Semiconductors Takeaways from our meetings in Taiwan* | 12 · 2026-06-01 | OW, no PT | $459.24 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212485214424151/MS-Semiconductors%20Takeaways%20from%20our%20meetings%20in%20Taiwan-260601.pdf) |
| **5/10** | **B&M (巴芒投研, independent)** — *公司财报前瞻分析* | 6 · 2025-09-03 | no house call | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212515215481551/Broadcom%20Inc.%28AVGO%29%20%E5%85%AC%E5%8F%B8%E8%B4%A2%E6%8A%A5%E5%89%8D%E7%9E%BB%E5%88%86%E6%9E%90.pdf) |
| **5/10** | **J.P. Morgan** — *Semiconductors Semi Cap Equipment： 1Q26 Preview： Sustained AI Demand， Broadening Cyclical…* | 26 · 2026-04-17 | OW, no PT | $405.90 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812215841548482/J.P.%20Morgan-Semiconductors%20Semi%20Cap%20Equipment%EF%BC%9A1Q26%20Preview%EF%BC%9A%20Sustained%20AI%20Demand%EF%BC%8C%20Broadening%20Cyclical%20Recovery%EF%BC%8C%20Structural%20WFE%20and%20Memory%20Tailwinds%20Underpin%20Continued%20Expectation%20of%20Semis%20Outperformance-260417.pdf) |
| **5/10** | **Bernstein** — *Qualcomm Inc（QCOM.US）： FQ226 recap~We hope they put on a good show in June...* | 22 · 2026-04-30 | OP, PT **$525** | $416.77 → **+26.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184484414482182/Bernstein-Qualcomm%20Inc%EF%BC%88QCOM.US%EF%BC%89%EF%BC%9AFQ226%20recap~We%20hope%20they%20put%20on%20a%20good%20show%20in%20June...-260430.pdf) |
| **5/10** | **Morgan Stanley** — *Semiconductors - North America Selloff of US memory stocks creates a compelling entry point* | 16 · 2026-07-20 | OW, no PT | $378.16 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814518551225542/Morgan%20Stanley-Semiconductors%20-%20North%20America%20Selloff%20of%20US%20memory%20stocks%20creates%20a%20compelling%20entry%20point-260720.pdf) |
| **4/10** | **Bernstein** — *Asia Tech Hardware： Future of Tech~Mapping the CPO value chain* | 33 · 2026-03-04 | OP, PT **$475** | $316.36 → **+50.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585552425544844/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AFuture%20of%20Tech~Mapping%20the%20CPO%20value%20chain-260304.pdf) |
| **4/10** | **BofA** — *NVIDIA Corporation（NVDA.OQ） Back to Basics： Boosting cash returns could be another rerating…* | 10 · 2026-04-27 | Buy, no PT | $417.54 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812212581148252/BofA%20Securities-NVIDIA%20Corporation%EF%BC%88NVDA.OQ%EF%BC%89Back%20to%20Basics%EF%BC%9A%20Boosting%20cash%20returns%20could%20be%20another%20rerating%20catalyst-260427.pdf) |
| **4/10** | **J.P. Morgan** — *Semiconductors CY26 Data Center Capex Revised Higher and Strong Initial Growth Outlook of…* | 10 · 2026-04-27 | OW, no PT | $417.54 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212218144282451/JPM-Semiconductors%20CY26%20Data%20Center%20Capex%20Revised%20Higher%20and%20Strong%20Initial%20Growth%20Outlook%20of%2040%25%20for%20CY27%3B%20Positive%20Across%20the%20Semiconductor%20AI%20Value%20Chain%20-%20Potential%20for%20Continued%20Upward%20Revisions-260427.pdf) |
| **4/10** | **Bernstein** — *Global Semiconductors and Semiconductor Capital Equipment~ What to make of an earnings…* | 17 · 2026-05-11 | OP, PT **$525** | $427.75 → **+22.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212452855548581/Bernstein-Global%20Semiconductors%20and%20Semiconductor%20Capital%20Equipment~%20What%20to%20make%20of%20an%20earnings%20supercycle%EF%BC%9F-260511.pdf) |
| **4/10** | **Bernstein** — *U.S. Semiconductors and Semiconductor Capital Equipment U.S. Semiconductors： Deconstructing…* | 18 · 2026-05-12 | OP, PT **$525** | $418.64 → **+25.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184124515551182/Bernstein-U.S.%20Semiconductors%20and%20Semiconductor%20Capital%20Equipment%20U.S.%20Semiconductors%EF%BC%9A%20Deconstructing%202026%20%EF%BC%88so%20far...%EF%BC%89-260512.pdf) |
| **4/10** | **Morgan Stanley** — *Semiconductors Weekly Meta GPU context; May SIA* | 20 · 2026-07-06 | OW, no PT | $373.90 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584242452855154/Morgan%20Stanley-Semiconductors%20%20Weekly%20Meta%20GPU%20context%3B%20May%20SIA-260706.pdf) |
| **4/10** | **Morgan Stanley** — *Semiconductors Weekly： Earnings Week 4 （QNT， CBRS， ADI）； June SIA* | 31 · 2026-08-10 | OW, PT **$502** | $422.40 → **+18.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814511485214442/Morgan%20Stanley-Semiconductors%20Weekly%EF%BC%9A%20Earnings%20Week%204%20%EF%BC%88QNT%EF%BC%8C%20CBRS%EF%BC%8C%20ADI%EF%BC%89%EF%BC%9B%20June%20SIA-260810.pdf) |
| **3/10** | **UBS** — *Global I O Smartphones： January ’26 Sell~Through： China impacted by base effect， but…* | 16 · 2026-03-06 | Buy, no PT | $329.27 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415554221241418/UBS-Global%20I%20O%20Smartphones%EF%BC%9AJanuary%20%E2%80%9926%20Sell~Through%EF%BC%9A%20China%20impacted%20by%20base%20effect%EF%BC%8C%20but%20non~China%20also%20flat%20YoY-260306.pdf) |
| **3/10** | **UBS** — *Equity Strategy： The Theme~ometer： AI Chips and Memory， Still Attractive* | 19 · 2026-04-16 | Buy, no PT | $397.84 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212215882582251/UBS-Equity%20Strategy%EF%BC%9AThe%20Theme~ometer%EF%BC%9A%20AI%20Chips%20and%20Memory%EF%BC%8C%20Still%20Attractive-260416.pdf) |
| **3/10** | **Morgan Stanley** — *Global Technology Asia Pacific Global Technology 2026 Outlook – A Tale of Two Halves* | 59 · 2026-04-27 | OW, no PT | $417.54 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585581844515444/MS-Global%20Technology%20Asia%20Pacific%20Global%20Technology%202026%20Outlook%20%E2%80%93%20A%20Tale%20of%20Two%20Halves-260427.pdf) |
| **3/10** | **UBS** — *GlobalFoundries Inc（GFS.US） 1Q 2Q A Little Ahead Before Thursday's Analyst Day* | 26 · 2026-05-05 | Buy, no PT | $426.68 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212458845284481/UBS-GlobalFoundries%20Inc%EF%BC%88GFS.US%EF%BC%891Q%202Q%20A%20Little%20Ahead%20Before%20Thursday%27s%20Analyst%20Day-260505.pdf) |
| **3/10** | **Bernstein** — *US Industrials & Tech： The Data Center Project Pipeline ~ Capacity， Construction &…* | 41 · 2026-05-20 | OP, PT **$525** | $417.10 → **+25.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424811815484/Bernstein-US%20Industrials%20%26%20Tech%EF%BC%9A%20The%20Data%20Center%20Project%20Pipeline%20~%20Capacity%EF%BC%8C%20Construction%20%26%20Cancellations%20%EF%BC%88April%20%2726%EF%BC%89-260520.pdf) |
| **3/10** | **HSBC** — *Marvell Technology （MRVL.US） Upgrade to Buy： Ready to ride the AI~networking super~cycle* | 17 · 2026-05-26 | Buy, PT **$450** | $421.34 → **+6.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212451114448851/HSBC-Marvell%20Technology%20%EF%BC%88MRVL.US%EF%BC%89Upgrade%20to%20Buy%EF%BC%9A%20Ready%20to%20ride%20the%20AI~networking%20super~cycle-260526.pdf) |
| **3/10** | **Morgan Stanley** — *Semiconductors Weekly Earnings Week 6 (SMTC, MRVL)* | 26 · 2026-08-24 | OW, no PT | $358.76 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814885581242252/Morgan%20Stanley-Semiconductors%20Weekly%20Earnings%20Week%206%20%28SMTC%2C%20MRVL%29-260824.pdf) |
| **3/10** | **J.P. Morgan** — *Semiconductors July WSTS： Seasonal M M Downtick Skewed by Memory Lumpiness； Industry Sales…* | 15 · 2026-09-08 | OW, no PT | $368.56 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584115845524114/J.P.%20Morgan-Semiconductors%20July%20WSTS%EF%BC%9A%20Seasonal%20M%20M%20Downtick%20Skewed%20by%20Memory%20Lumpiness%EF%BC%9B%20Industry%20Sales%20Outlook%20Now%20-%20%241.7T%20in%202026%20and%20-%242T%20in%202027-260908.pdf) |
| **3/10** | **Bernstein** — *U.S. Semiconductors and Semicap Equipment~Can you put the AI genie back in the bottle？* | 13 · 2026-09-14 | OP, PT **$575** | $344.72 → **+66.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/181544228852442/Bernstein-U.S.%20Semiconductors%20and%20Semicap%20Equipment~Can%20you%20put%20the%20AI%20genie%20back%20in%20the%20bottle%EF%BC%9F-260914.pdf) |
| **2/10** | **B&M (巴芒投研, independent)** — *财报前瞻* | 14 · 2026-03-03 | no house call | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585552248512424/AVGO_%E8%B4%A2%E6%8A%A5%E5%89%8D%E7%9E%BB.pdf) |
| **2/10** | **Goldman Sachs** — *Advanced Micro Devices Inc. (AMD)-Upgrade to Buy as Agentic AI drives server CPU tailwinds…* | 15 · 2026-05-05 | Buy, no PT | $426.68 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585421128481424/GS-Advanced%20Micro%20Devices%20Inc.%20%28AMD%29-Upgrade%20to%20Buy%20as%20Agentic%20AI%20drives%20server%20CPU%20tailwinds%3B%20we%20see%20datacenter%20GPU%20upside%20in%202027%20%26%20beyond-260505.pdf) |
| **2/10** | **J.P. Morgan** — *摩根大通-半导体设备-TMC会议总结： 第一季度业绩后动能持续-AI推理拐点、广泛周期性复苏、稳健内存上行周期、WFE周期拉长， 维持超配该板块* | 35 · 2026-05-23 | OW, no PT | $413.49 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812451582582452/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%8D%8A%E5%AF%BC%E4%BD%93%E8%AE%BE%E5%A4%87-TMC%E4%BC%9A%E8%AE%AE%E6%80%BB%E7%BB%93%EF%BC%9A%E7%AC%AC%E4%B8%80%E5%AD%A3%E5%BA%A6%E4%B8%9A%E7%BB%A9%E5%90%8E%E5%8A%A8%E8%83%BD%E6%8C%81%E7%BB%AD-AI%E6%8E%A8%E7%90%86%E6%8B%90%E7%82%B9%E3%80%81%E5%B9%BF%E6%B3%9B%E5%91%A8%E6%9C%9F%E6%80%A7%E5%A4%8D%E8%8B%8F%E3%80%81%E7%A8%B3%E5%81%A5%E5%86%85%E5%AD%98%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E3%80%81WFE%E5%91%A8%E6%9C%9F%E6%8B%89%E9%95%BF%EF%BC%8C%E7%BB%B4%E6%8C%81%E8%B6%85%E9%85%8D%E8%AF%A5%E6%9D%BF%E5%9D%97.pdf) |
| **2/10** | **Morgan Stanley** — *NVIDIA Corp.（NVDA.US） Computex NVDA keynote & financial analyst Q&A* | 13 · 2026-06-03 | OW, no PT | $478.47 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812488522252442/Morgan%20Stanley-NVIDIA%20Corp.%EF%BC%88NVDA.US%EF%BC%89Computex%20NVDA%20keynote%20%26%20financial%20analyst%20Q%26A-260603.pdf) |
| **2/10** | **Citi** — *US Semiconductors and Semiconductor Equipment： Summer Sell~off； Fundamentals Intact； Prefer…* | 11 · 2026-07-24 | Buy, no PT | $381.92 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412418114448428/CITI-US%20Semiconductors%20and%20Semiconductor%20Equipment%EF%BC%9ASummer%20Sell~off%EF%BC%9B%20Fundamentals%20Intact%EF%BC%9B%20Prefer%20Semi%20Caps%20to%20Semis-260724.pdf) |
| **1/10** | **Morgan Stanley** — *摩根士丹利—半导体： 半导体库存追踪——逐比特分析* | 16 · 2026-04-18 | OW, no PT | $405.90 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184482518211182/%E6%91%A9%E6%A0%B9%E5%A3%AB%E4%B8%B9%E5%88%A9%E2%80%94%E5%8D%8A%E5%AF%BC%E4%BD%93%EF%BC%9A%E5%8D%8A%E5%AF%BC%E4%BD%93%E5%BA%93%E5%AD%98%E8%BF%BD%E8%B8%AA%E2%80%94%E2%80%94%E9%80%90%E6%AF%94%E7%89%B9%E5%88%86%E6%9E%90.pdf) |
| **1/10** | **Morgan Stanley** — *Semiconductor Inventory Tracker： Not Restocking Yet* | 16 · 2026-07-01 | OW, no PT | $369.34 · upside n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412424414544448/Morgan%20Stanley-Semiconductor%20Inventory%20Tracker%EF%BC%9A%20Not%20Restocking%20Yet-260701.pdf) |

---

## Per-report digests

### 9/10 — UBS — *Updating Model after a Series of Supply Chain Checks And New Details on OpenAI Partnership.…*
`22 pp · 2025-10-14 · Buy, PT $415 · $342.21 → +21.3%`

**Why bullish/bearish.** Mechanism: the OpenAI 10GW rack program on top of Google/Meta unit growth. Models ~$49bn C26 AI revenue, Google approaching 3mn units ($21bn), Meta ~0.5mn, OpenAI ~$90bn F26-F29; PT to $415 on ~41x semis EV/FCF.

**Insight density.** Genuinely proprietary: UBS's own TSMC CoWoS estimate, hyperscaler ASIC die/wafer-cost tables, revenue-per-GW math, Google/Meta unit checks — not restated consensus.

**Data support.** Figures 1-8: OpenAI opportunity sizing, new-vs-old estimates, quarterly model, hyperscaler ASIC tables, SOTP, comps; C27 EPS ~10% above Street.

**Event context.** Written the day of the OpenAI-Broadcom 10GW announcement; a pre-print model update with the PT walked higher on the deal.

### 9/10 — UBS — *US Semiconductors and Semi Equipment： SemiBytes， AVGO Tweaks， TSMC Capex， US China Update*
`17 pp · 2025-10-20 · Buy, PT $415 · $347.29 → +19.5%`

**Why bullish/bearish.** Buy on AVGO, PT $415. UBS re-models custom compute, lifting CY27E revs/EPS to $132.6B/$13.56 versus Street's $121.3B/$12.88, while CY26E EPS of $10.11 already matches Street — so upside sits in 2027. Customer #4's $10B rack order is not OpenAI.

**Insight density.** Proprietary model work: hyperscaler ASIC die costs, wafer pricing and turnkey TAM per program (Figures 4-5), plus UBS-vs-Street bridges. Agentic-AI memory and telemetry channel checks from OCP Summit.

**Data support.** New-vs-old estimate table, quarterly summary model, SOTP at 41x EV/FCF semis and 33x software, hyperscaler ASIC project exhibits, Buy/PT history.

**Event context.** Written 20 Oct 2025 after OCP Summit and AVGO's 14 Oct PT raise to $415; UBS pre-positions for a Trump-Xi meeting and a possible China compute reopening.

### 9/10 — HSBC — *Buy： Potent mix of ASIC and networking upside*
`19 pp · 2025-11-24 · Buy, PT $535 · $375.85 → +42.3%`

**Why bullish/bearish.** FY26e/FY27e ASIC revenue raised 46%/63% to $44.7bn/$72bn, 44%/59% above consensus, on CoWoS allocation of 150k→250k wafers and Google TPU units of 3.1m (from 1.7m); FY26e EPS $11.68 is within 5% of consensus FY27e.

**Insight density.** Proprietary CoWoS wafer, net-die, unit and ASP build by customer; $14bn ASIC revenue per GW on the OpenAI deal; 40–45% share expectation in 1.6T DSP.

**Data support.** Exhibits 1–21: FY26e ASIC revenue by customer, consensus-revision tables, quarterly P&L model, networking sensitivity, valuation table.

**Event context.** Written 24 Nov 2025 after the 13 Oct OpenAI 10GW deal and the fourth-customer (Anthropic) announcement, ahead of the Dec FQ4 print.

### 9/10 — UBS — *US Semiconductors and Semi Equipment： SemiBytes： Thoughts on TPU and AVGO Preview，…*
`23 pp · 2025-11-30 · Buy, PT $472 · $400.71 → +17.8%`

**Why bullish/bearish.** Custom ASIC drives the story: UBS models Custom Compute +181% in CY26 with Google TPUs +72% (5x HBM content per unit) plus a new "Customer #4" rack program in 2H26 and OpenAI ramping late CY26, lifting FY27 EPS to $13.56.

**Insight density.** High: channel checks with hyperscale engineers (TPU 30-40% TCO edge), an NVDA IR call-back, CoWoS data showing higher TPU units, and a customer-level build (Google $26.8B, META, OpenAI, ByteDance).

**Data support.** Ironwood vs Trillium/GB200 spec table, quarterly segment model, FQ4 and FY26-28 estimates vs Street, and a SOTP (41x EV/FCF semis, 33x software) building the $472 target.

**Event context.** AVGO FQ4 print on 12/11 AMC; preview keyed to Ironwood TPUv7 volume, "Customer 4" rack-scale gross margin detail and OpenAI ramp timing.

### 9/10 — HSBC — *Buy： AI narrative and earnings still not fully priced in*
`13 pp · 2025-12-08 · Buy, PT $535 · $398.86 → +34.1%`

**Why bullish/bearish.** FY26e/FY27e ASIC revenue of $44.7bn/$72bn sits 38%/40% above consensus, taking AI revenue to $55.8bn (+180% y/y) then $88.2bn; FY27e EPS $16.72 (+32% above street), TP just 32x it for 37% upside.

**Insight density.** Proprietary CoWoS/net-die/unit/ASP build by customer (TPU 3.1m units FY26e, Meta 900k, Anthropic ~$5bn); consensus revision tracker since the Gemini 3 launch.

**Data support.** Exhibits: FY26e ASIC revenue by customer, quarterly P&L, AI-networking sensitivity, HSBC vs consensus AI revenue, forward-PE and valuation/risk pages.

**Event context.** Written 8 Dec 2025 as a 4QFY25 preview (print 11 Dec), after the Gemini 3 launch repriced AI ASIC demand.

### 9/10 — J.P. Morgan — *Google TPU Outlook Getting Stronger FY26 And FY27； 18 Month Lead Implies Shrinking…*
`11 pp · 2026-01-25 · OW, PT $475 · $318.88 → +49.0%`

**Why bullish/bearish.** Primary research lifts CY27 Google TPU deployment to 6-7M units (prior 5M; 3.5M in CY26), 95%+ powered by Broadcom's 3nm Sunfish ASIC, with multi-billion POs booked for the 2H26 ramp and Zebrafish COT 18 months behind.

**Insight density.** Genuinely proprietary: revised TPU unit forecast, supplier-share math, chip codenames (Ironwood/Hammer, Sunfish/Hellcat, Zebrafish), first-silicon timing, CoWoS/HBM/substrate constraints, 14 designs shipped in 12 years.

**Data support.** Valuation build (32x CY26 exit EPS ~$15.00), full FY24-26 income statement, balance sheet, quarterly model and ratios, PT/rating history table.

**Event context.** Post-December print, pre-January report; AI backlog still growing, Meta 3nm Athena/Iris on track, Google COT noise, tight advanced-substrate and HBM supply.

### 9/10 — Morgan Stanley — *AVGO FAQ： What will it take for the stock to outperform？*
`19 pp · 2026-02-03 · OW, PT $462 · $319.15 → +44.8%`

**Why bullish/bearish.** Bullish, though MS prefers NVDA: Google's MediaTek TPU is "risk silicon" with bugs, so TPU share loss is tail risk — CoT maybe ~20% by 2030, binary; the $21bn Anthropic rack orders are over 40% of FY AI revenue but look transitory, so margins normalize.

**Insight density.** Proprietary: MTK chip returned in April, ~$1bn CY26 MTK revenue; AVGO HBM locked through 2027; MS base case versus their Greater China team's 2.5mn MediaTek TPU units in 2027.

**Data support.** Eight exhibits (AI-semi relative performance, TPU unit split, MS vs consensus GM, implied CY27 AI P/E, PEG); bull/base/bear $592/$462/$291 at 48x/35x/26x 2027e ModelWare EPS.

**Event context.** No print — a theme piece answering "OK, what about Broadcom?" after their NVDA underperformance note, written into this year's AVGO underperformance and ahead of the 22-26 Apr shareholder meeting.

### 9/10 — UBS — *Increasing Estimates On TPU Unit Inflection； C2027E EPS -$18*
`31 pp · 2026-02-10 · Buy, PT $475 · $339.19 → +40.0%`

**Why bullish/bearish.** TPU units above 5m in C2027E (vs ~3.7m in C2026E) drive AI revenue to ~$60B F26E, ~$106B F27E and ~$150B F28E, lifting C2027E EPS past $18; PT held at $475 on ~25x software and ~30x semis EV/FCF.

**Insight density.** Proprietary unit split by vendor (AVGO 3,670k C26 / 5,180k C27 vs MediaTek 300k / 2,000k), Google ~$30B of TPU revenue, COT dilution quantified at ~8% EPS.

**Data support.** Figure 9 unit model, Figure 14 COT dilution bridge, TPU-vs-GPU architecture deep dive, expert calls, income statement and balance sheet.

**Event context.** 10 Feb 2026 estimates raise following supply-chain and expert-call work; frames the OpenAI ASIC (late 2026) and Anthropic ASIC (2H27) ramp.

### 9/10 — UBS — *Strong Results & Guidance； Raise Estimates， Maintain $475 PT*
`27 pp · 2026-03-05 · Buy, PT $475 · $331.55 → +43.3%`

**Why bullish/bearish.** Estimates raised hard (FY27 AI to $132.7B from $106.4B; FY27 EPS $21.14) on bottom-up ~6mn TPU units and management's ~10GW at ~$10-15B/GW. Networking ~35% of AI revenue, ~$43B; Anthropic's ~3GW (~$40B) turns less rack-heavy, so margins hold.

**Insight density.** Genuinely proprietary: TPU units by node (v5p-v9 Pumafish, MediaTek Zebrafish), per-customer AI revenue by quarter, revenue-per-GW reset from $20B+ to $10-15B, plus a MediaTek/AVGO design-win comparison.

**Data support.** Figure 1 unit model, per-quarter and per-customer AI/networking/compute builds, FQ1/FQ2 variance vs Street, a TPU-vs-GPU spec table, a software/semis SOTP ($144 + $342/share) and full statements.

**Event context.** Post-print (FQ1-26, 4 Mar close $317.53); the hook is the new FY27 over-$100B AI guide and the changing Anthropic rack structure, i.e. guidance rather than a deal or regulatory trigger.

### 9/10 — UBS — *Increasing 2027 TPU Units Once Again*
`22 pp · 2026-04-13 · Buy, PT $475 · $379.15 → +25.3%`

**Why bullish/bearish.** Own supply-chain checks lift C27 TPU units to ~7MM from ~6MM, driving F27/C27 revenue to $195B/$212B (from $182B/$195B), F27 AI revenue to $145B (from $133B) and GCP TPU spend to $26B/$61B/$79B for C26/C27/C28 (from $26B/$46B/$61B).

**Insight density.** Pure proprietary: a TPU unit model by node (v5–v9, AVGO vs MediaTek), own GCP spend estimates, and FY27 EPS $22.56 vs Street $17.69 (+28%) — not restated consensus.

**Data support.** Figures 1–3 TPU units/new-vs-old/UBS-vs-Street, summary model (Fig 4), TPU-vs-GPU spec tables (Figs 6–7), SOTP and comps (Figs 8–9), plus Anthropic run-rate $30B and 1,000+ >$1MM ARR customers.

**Event context.** Written days after the AVGO–Google agreement extended to 2031 with rack-level supply assurance, and the Google/Anthropic ~3.5GW TPU expansion — event-driven, not a print.

### 9/10 — Citi — *Preview – Raising TP to $500； Maintain Buy*
`21 pp · 2026-05-12 · Buy, PT $500 · $418.64 → +19.4%`

**Why bullish/bearish.** Higher TPU volumes lift FY28 AI sales 40% to $180B (Google alone $107.8B), AI mix rising from ~49% of sales now to ~81% by F4Q28, driving FY28 EPS of $25.23 (+34%); PT is just 20x that. Anthropic shifts from racks to chips (chips ~20–25% of rack sales, better GM).

**Insight density.** Proprietary: Sparse Core moving from logic die to SerDes chiplet in TPU v8i, the Citi AI Summit keynote with Broadcom's Charlie Kawwas, and a customer-by-customer AI revenue build.

**Data support.** Figs 1–9, full P&L/cash-flow/balance-sheet model, per-customer FY25–F28 AI revenue table, TPU 8t/8i block diagrams, verbatim Kawwas quotes.

**Event context.** Preview written 12 May 2026 ahead of the 3 June April-quarter print; framed by Google's 2026 capex raise to $180–190B and MediaTek's post-earnings ASIC revision.

### 9/10 — UBS — *FQ2-26 (Apr) Preview-Raising PT, Adjusting Estimates*
`21 pp · 2026-05-18 · Buy, PT $490 · $420.05 → +16.7%`

**Why bullish/bearish.** Anthropic's order converted from racks to standard ASICs: contribution cut from ~$21bn/~$23bn (C26/C27) to ~$8bn/~$22bn, but at much higher margin, with revenue per GW now tracking GCP TPU at the bottom of the $10-20bn/GW range. AI networking trimmed to $24bn/$44.6bn; FY27 AI $145bn→$133bn, EPS $21.14.

**Insight density.** Proprietary: TPU units cut to ~3.7MM C26 / 6.8MM C27; calls AVGO the v8i supplier from the GCP announcement (288GB HBM, 384MB SRAM); Meta XPU $0.8B→$3B→$8B→$13B; OpenAI $5B F27/$16B F28.

**Data support.** UBS summary model, TPU unit exhibit, UBS-vs-Street table, full P&L/balance sheet/cash flow, and an EV/FCF SOTP: 12x CY27 software FCF $40.7B plus 30x semis FCF $68.0B.

**Event context.** Pre-print ahead of the April quarter (FQ2-26). Triggers are the Anthropic rack-to-ASIC conversion and GCP's TPU v8i/v8t launch. UBS models FQ2 $22.0B/$2.38 and FQ3 AI revenue $13.6B.

### 9/10 — Citi — *Management Callback Notes*
`11 pp · 2026-06-04 · Buy, PT $500 · $418.25 → +19.5%`

**Why bullish/bearish.** Management sees FY27 AI "more than $100B"; 2028 XPU units exceed GPUs at the five scaled LLM buyers; Meta ramps 2H27, OpenAI's own XPU 2H27 into F28; Singapore advanced packaging starts August, months early; gross margin floor 74%; PT 20x F28 EPS.

**Insight density.** Pure management channel — unreported specifics (Singapore packaging pulled forward, VMware core-count pricing, HBM pass-through, MediaTek "low end only"), not consensus restatement.

**Data support.** No exhibits or model; valuation stated as 20x F28 EPS (low end of 20-40x), risks quantify Google at 35-40% of sales, full PT history.

**Event context.** Callback two days after the FQ2-26 print; triggers are the FY27 >$100B AI debate, Tomahawk/Ethernet scale-up and the MediaTek TPU-share question.

### 9/10 — Morgan Stanley — *North America Expectations miss amid very strong demand*
`17 pp · 2026-06-04 · OW, PT $502 · $418.25 → +20.0%`

**Why bullish/bearish.** Bullish, despite the Q2 revenue "miss" ($22.187bn, +47.9% y/y): AI revenue grew only 30% in April but reaccelerates to ~200% y/y in July, Q3 guides to $29.4bn versus Street $28.3bn, and FY27 AI is framed "well above" $100bn against MSe $118bn.

**Insight density.** MS-vs-consensus bridges (FY26 EPS $11.59 versus $11.26; sales $105.746bn versus $104.182bn) plus a MediaTek-share sensitivity that keeps AVGO at ≥80% of the ASIC SAM, and options-implied scenario odds (>$637 ~8.2%, <$308 ~33.6%).

**Data support.** Full income statement, balance sheet and cash-flow models to FY28, quarter variance exhibits, MS-versus-Street tables, and the bull/bear build (31x $20.55 to $637; 20x $15.40 to $308).

**Event context.** Q2 print night, 4 Jun 2026; stock closed $479.23 on 3 Jun. Triggers: April-quarter AI growth of just 30%, the "rack-to-chip transition", and Google's more precise customer-owned-tooling language.

### 9/10 — Morgan Stanley — *In Defense of AVGO’s ASIC Share*
`16 pp · 2026-07-14 · OW, PT $502 · $389.11 → +29.0%`

**Why bullish/bearish.** TPU share holds ~80%: MediaTek's 3nm entry cannot displace a scaled platform given HBM locked under contract, packaging (CoWoS vs unproven EMIB) and Google's reliability bar. FY27 AI revenue ~$120bn, TPU ~75% of 10GW at $10-12bn/GW (~$80bn); FY28 at least 15GW with TPU fading to ~60%.

**Insight density.** Proprietary: MS's own XPU-GW-per-customer and AI-revenue/GW models, Taiwan supply-chain checks on CoWoS/EMIB/substrate, MediaTek's 15-20% long-term share target, and an open split with MS's own MediaTek analyst.

**Data support.** Three build exhibits (customer XPU GW 2026-28, AI revenue vs GW, driver model), bull/base/bear $637/$502/$308 around a 28x CY27e $17.92 EPS PT build, plus options-implied probabilities.

**Event context.** Not print-driven: a July rebuttal to the year-to-date MediaTek share-loss overhang; also discloses MS advised Broadcom on its June 9, 2026 AI XPV Platform with Apollo and Blackstone.

### 8/10 — Mizuho — *MizuhoSecuritiesUSALLC_AIServerSupplyChainCall-UpsidetoAVGO, SomeChallengesWithPeers-AdjPTs*
`9 pp · 2025-05-16 · OP, PT $250 · $232.64 · upside n/a`

**Why bullish/bearish.** Bullish: AVGO's 2026E TSMC CoWoS allocation of ~95k wafers could exceed 100k if OpenAI's Strawberry and Apple's Baltra ramp; TPUv7p ships more than 2x MediaTek's v7e units at higher ASPs, widening custom-silicon SAM beyond $60-90B by 2027E on ~70-80% ASIC share.

**Insight density.** Channel checks rather than consensus: customer-by-customer CoWoS wafer model (AVGO/Google 85k to 95k), ASIC award/SOP roadmap across Google, AWS, Meta, OpenAI and Apple, plus MediaTek v7e yield problems.

**Data support.** Two supply tables — AVGO CoWoS allocation 2023-27E and AI-accelerator shipments; ASIC partner/SOP exhibit; comp table (22.5x C26E EV/EBITDA, 27.1x P/E).

**Event context.** Hosted ahead of NVDA/AVGO/CRDO/DELL prints; framed by Trump's Middle East tour deals (HUMAIN, G42) offsetting H20 China headwinds.

### 8/10 — Goldman Sachs — *Very strong quarter and AI customer traction， tempered by lack of guide~up for FY26*
`8 pp · 2025-12-11 · Buy, PT $450 · $404.11 → +11.4%`

**Why bullish/bearish.** Mechanism: Google TPU momentum plus scarce custom-silicon supply. AI semis +74% YoY to $6.5bn; 1Q guide $8.2bn vs Street $6.9bn; $73bn backlog over 18 months; Anthropic added an $11bn FY26 order; fifth XPU customer signed.

**Insight density.** Print data plus GS model revisions; no channel survey, but the management disclosures (backlog, fifth customer, Anthropic order, rack-margin dilution) are fresh specifics.

**Data support.** Exhibits 1-2 (variance, guidance), new-vs-old estimates by segment, PT table: 38x $12.00 normalized EPS, bull $533 / bear $217.

**Event context.** Written on the FQ4-25 print, with the stock expected to pull back because management gave no FY26 AI guide-up despite ~100% Q1 growth.

### 8/10 — Bernstein — *FQ425 recap~The fickle heart's desire...*
`24 pp · 2025-12-12 · OP, PT $475 · $357.92 → +32.7%`

**Why bullish/bearish.** FQ425 beat at $18.0B/$1.95 (Street $17.5B/$1.87) with AI semis ~$6.5B, +74% YoY; FQ126 AI guided to $8.2B, +100% YoY and $1.4bn above Street; extra $10B Anthropic plus a fifth customer imply >$50B FY26 AI revenue, against FY26/27 model of $52.7B/$90.0B.

**Insight density.** Largely analyst-repeated company disclosure; genuinely own is the >$50B FY26 AI inference and the gross-margin dilution framing from AI component pass-throughs.

**Data support.** Exhibits 1–17 (segment variance, GM/OPM/FCF paths, inventory, net debt) plus income-statement and cash-flow models; PT at ~32x FY27 EPS.

**Event context.** Published 12 Dec 2025, hours after the 11 Dec FQ4 print and FQ1 guide, explaining the ~5% aftermarket drop despite the beat.

### 8/10 — Morgan Stanley — *AI acceleration into 2026*
`16 pp · 2025-12-12 · OW, PT $462 · $357.92 → +29.1%`

**Why bullish/bearish.** January-quarter AI guidance of $8.2bn is >20% above MS, with $21bn of Anthropic orders shipping in 2h26 and $73bn AI backlog shippable in 18 months; numbers rise materially even after assuming mid-40% rack gross margins. Multiple cut 41x→35x still lifts PT.

**Insight density.** Fresh datapoints: MS's own mid-40% rack-margin assumption, the AI-portion implied multiple at ~2x NVIDIA, and 1h27 sequential math off the backlog; still, MS prefers NVDA.

**Data support.** Exhibits 1–5 (FQ4 variance, projected income statement/balance sheet/cash flow), bull/base/bear $592/$462/$291 with options-implied probabilities.

**Event context.** Written overnight on the 11 Dec 2025 FQ4 print and sell-side call, incorporating the second $11bn Anthropic order and the new customer #5 (explicitly not OpenAI).

### 8/10 — UBS — *CEO CFO Meeting Suggests Friday's Move Is a Buying Opportunity*
`23 pp · 2025-12-15 · Buy, PT $475 · $337.92 → +40.6%`

**Why bullish/bearish.** The $73B AI backlog will ship in ~12 rather than 18 months; total backlog $110bn→$162bn in FQ4; AI revenue >$60B in F26 (nearly 3x), AI networking bookings $3bn→~$12bn, XPU GM ~55%, rack GM 45–50%, FY27 EPS $14.15.

**Insight density.** Management-sourced and proprietary: the rack/XPU/networking gross-margin ladder, ~60% AVGO content per AI rack, Google direct-to-foundry risk dismissed for five years.

**Data support.** Estimate-revision tables, FY27 and CY26–27 models, PT built on ~33x software and ~32x semis EV/FCF; no new exhibits beyond the model.

**Event context.** 15 Dec 2025, after the 12 Dec in-person CEO/CFO meeting and Friday's post-print selloff, which UBS called a buying opportunity.

### 8/10 — J.P. Morgan — *Semiconductors Semi Cap Equipment： 2026 Outlook： Expect Another Year Of Stock…*
`34 pp · 2025-12-16 · OW, no PT · $339.40 · upside n/a`

**Why bullish/bearish.** Bullish: FY26 AI revenue $55-60bn+ (from ~$20bn FY25: $11-12bn Google, $6bn AI networking, $1.5bn Meta, $1bn ByteDance), FY27 above $100bn, 50%+ CAGR; AVGO captures $25-30bn per GW, including OpenAI's 10GW at ~$25bn/GW; EBIT margin 65.8% to 68.2%.

**Insight density.** Bottom-up AI revenue bridge by customer plus a proprietary $28-35bn/GW NVDA versus $25-30bn/GW AVGO sizing framework; surrounding capex and rating commentary is consensus-adjacent.

**Data support.** Comp table (28.4x C26E P/E, $115bn C26E revenue), EBIT-margin and payout tables, DC-capex vs. AI-spend charts, custom ASIC pipeline exhibit.

**Event context.** 16 Dec 2025 outlook; live catalysts are OpenAI's 10GW AVGO engagement and projected 50%+ 2026 hyperscaler capex growth.

### 8/10 — Bernstein — *Vegas baby...Takeaways from a CES investor meeting with the Semiconductor Solutions Group…*
`15 pp · 2026-01-09 · OP, PT $475 · $343.70 → +38.2%`

**Why bullish/bearish.** Mechanism: Broadcom's roadmap is the only credible way to match Nvidia's pace, so customer-owned-tooling fears are overblown. TPU v7 goes to "many many millions" in 2026; the $73bn order is "significantly higher" now; FY27 EPS $14.86.

**Insight density.** Primary-source management commentary: Google v8 pulled in 3 months while MediaTek slipped 9, TPU v9 engagement, own substrate fab with 1.9-year payback, interposer-less TPU patents.

**Data support.** Quarterly income-statement and cash-flow models to FY28, ticker/valuation table; PT = ~32x FY27 pro-forma EPS of $14.86.

**Event context.** Hosted CES investor meeting with Charlie Kawwas, president of the Semiconductor Solutions Group, amid rising competition and COT concerns.

### 8/10 — Goldman Sachs — *AMERICAS TECHNOLOGY AI Unit Economics： GPUs vs. ASICs and the inference cost curve~Buy AVGO…*
`14 pp · 2026-01-20 · Buy, PT $450 · $331.38 → +35.8%`

**Why bullish/bearish.** GS's cost-per-token curve shows Google/Broadcom TPU v7 at ~70% lower cost than v6, at or below Nvidia GB200 NVL72, with Anthropic's $21bn Broadcom orders shipping mid-2026; AI networking upside looks underappreciated after GS's Asia trip.

**Insight density.** Proprietary: GS's own accelerator cost model (ASP/TDP assumptions per SKU) plus post-Asia checks; AVGO-specific incremental content is estimate revisions (FY26 AI semis +3.3% to $52.1B) and the consensus gap.

**Data support.** Exhibit 6 shows the GB200 build-up ($0.27 per mn tokens) with capex, rack ASP, utilization and depreciation laid out; AVGO new-vs-old estimate table runs through FY28.

**Event context.** Published after AWS re:Invent and ahead of late-January hyperscaler earnings; no AVGO print, with recent stock weakness framed as a buying opportunity.

### 8/10 — UBS — *Thinking Through SOTP Amid Software Deep Dive + EPS Preview*
`25 pp · 2026-02-23 · Buy, PT $475 · $329.13 → +44.3%`

**Why bullish/bearish.** Backing software out at 12x/19x/12x C27 multiples leaves semis at 17x EV/EBITDA, 20x P/E and 23x EV/FCF — one turn above peers; SOTP of 25x software FCF + 30x semis FCF gives $483/share EV, PT $475.

**Insight density.** UBS software team's VMware churn work (2026/27 renewals, lapping VCF upsell, AI coding tools) weighed against AI revenue tripling to >$60B in F26.

**Data support.** Figures 1–10: SOTP tables and sensitivity, peer multiple comps, HOLT, plus unit and estimate preview tables.

**Event context.** 23 Feb 2026, two weeks before the 4 Mar FQ126 print; a response to the software-driven de-rating, with Anthropic rack GM dilution the swing issue.

### 8/10 — Goldman Sachs — *Very strong guidance and commentary on key debates should drive stock higher - Buy*
`8 pp · 2026-03-04 · Buy, PT $480 · $316.36 → +51.7%`

**Why bullish/bearish.** Bullish on lowest-inference-cost leadership: FY27 AI semis "significantly in excess of $100bn" across up to 10GW (GS $130bn vs $86.6bn prior); six custom-silicon engagements ramping (Google TPU v7, Meta, Anthropic 3GW, OpenAI 1GW); components secured through FY28; racks no longer margin-dilutive.

**Insight density.** Largely company guidance plus GS variance work; the fresh bits are the 40% AI-networking mix (up from ~30%), the Anthropic 3GW and OpenAI 1GW FY27 ramps, and the FY28 supply lock.

**Data support.** Four exhibits (FQ1 variance, FQ2 guidance, new vs old estimates, PT build); FY26/27/28 AI semis $60bn/$130bn/$170bn; PT $480 = 30x normalized EPS $16.00 (from 38x/$12.00).

**Event context.** Written the evening of the FQ1-26 print (revenue $19.3bn, AI semis $8.4bn +106% y/y); FQ2 guided to $22.0bn revenue and $10.7bn AI semis — print-driven, no deal or regulatory trigger.

### 8/10 — Bernstein — *FQ126 recap~Line 'em up and knock 'em down...*
`24 pp · 2026-03-05 · OP, PT $525 · $331.55 → +58.3%`

**Why bullish/bearish.** FQ1-26 $19.31B/$2.05 beat; AI $8.4B, +106% YoY, networking about a third of AI sales. Management set line of sight to ~10GW FY27 shipments (Anthropic ~3GW, OpenAI ~1GW, "multiple" Meta, strong Google) and "significantly in excess" of $100B AI revenue; GM-dilution and CoT fears were rebutted.

**Insight density.** First-hand call detail rather than consensus: the customer-level GW split, networking at a third to 40% of AI sales, IR's HBM-passthrough margin nuance, and the CoT/VMware disintermediation defence.

**Data support.** 19 exhibits: results/guidance variance, segment margins, FCF bridge, inventory and leverage, plus an updated FY26/27 model (FY27 revenue $154.7B, EPS $17.73) and the 30x-FY27 $525 build.

**Event context.** Written the morning after the FQ1-26 print; the stock was down over 20% since the prior earnings on CoT, margin-dilution and software-disruption fears that the call addressed.

### 8/10 — Goldman Sachs — *Partnership with Meta further reinforces Broadcom’s technology advantage in custom silicon…*
`8 pp · 2026-04-14 · Buy, PT $480 · $380.18 → +26.3%`

**Why bullish/bearish.** Meta's multi-year MTIA partnership (initial >1GW, supply to 2029) plus Google/Anthropic a week earlier broadens the XPU base; networking rides along. GS FY27/28 EPS are ~14% above Street, PT = 30x normalized EPS $16; FY26E revenue $107.2B, FY27E $180.7B.

**Insight density.** House model and the ~14%-above-Street FY27/28 EPS call (vs Visible Alpha consensus); no channel or supply-chain data — it is a same-day deal-reaction note.

**Data support.** Full income statement, balance sheet and cash-flow forecasts FY26-28, the 30x × $16 normalized-EPS build, EPS $10.37/$19.18/$24.39 out-years; deal terms only, no management quotes.

**Event context.** Published the evening of Broadcom's 14 Apr 2026 Meta MTIA announcement, a week after the Google/Anthropic note; Hock Tan steps off Meta's board into an advisory role.

### 8/10 — J.P. Morgan — *Expanded Meta Partnership Drives Confidence In A Strong Multi~Year Revenue Ramp； Adds To…*
`11 pp · 2026-04-15 · OW, PT $500 · $396.09 → +26.2%`

**Why bullish/bearish.** Bullish on the Meta multi-year, multi-generational, multi-GW MTIA agreement through 2029: first gigawatt in 2027 means $12-15bn of Broadcom revenue; five programs (Athena/Iris/Arke at 3nm, Astrid/Apollo at 2nm) ramp over three years; conviction FY27 AI revenue "significantly exceeds $120B+".

**Insight density.** Proprietary beyond the announcement: MTIA program names, process nodes and ramp timing from JPM's prior work, plus Hock Tan stepping off Meta's board into an advisory role.

**Data support.** Full annual and quarterly model (FY26E revenue $109,978mn, adj. EPS $12.29; FY27E $166,491mn, $19.61); Dec-26 PT of $500 is 24.5x their CY27 EPS of ~$20.45.

**Event context.** Written one day after the Meta agreement, following the Google/Anthropic deal note a week earlier and on the heels of the March FQ1 print — deal-driven, no new print.

### 8/10 — J.P. Morgan — *Maintains Lead In AI Networking Silicon； Next~Gen 3nm Tomahawk 6 Strong Ramp 2H26…*
`11 pp · 2026-06-02 · OW, PT $500 · $480.81 → +4.0%`

**Why bullish/bearish.** Tomahawk 6 (3nm, 102.4Tbps, 1.6T optics) is nearly sold out for next year and ramps faster than any prior Broadcom networking product, shipping 6-9 months ahead of Nvidia and 12 months+ ahead of Marvell/Cisco; networking reaches $45bn+, ~28% of AI revenue.

**Insight density.** Mostly roadmap synthesis with some fresh specifics: T6 sell-out, Condor 3nm 200G SERDES and Davisson CPO, Jericho 4/Tomahawk Ultra ramp, 70% share held. No channel checks.

**Data support.** Figures 1-2 on the two-year Tomahawk cadence and T4/T5/T6 specs, $500 = 24.5x CY27 EPS ~$20.45, PT/rating history table; no full model in this note.

**Event context.** Quiet patch, no print; competitive-positioning piece timed with the Extel All-America survey voting window.

### 8/10 — Citi — *Buyers of Pullback; Improved AI Visibility into 2028*
`15 pp · 2026-06-03 · Buy, PT $500 · $478.47 → +4.5%`

**Why bullish/bearish.** Apr-Q in line ($22.2B sales, $2.44 EPS); bookings $30B+ against $11B shipped; FY26 AI sales ~$56B and >$100B reiterated for FY27 with FY28 visibility improving; Jul-Q gross margin guided down 300bp to 74.0% as AI ASIC mix rises 30%→38%, yet F28 EPS held at $25.25.

**Insight density.** Guidance-versus-consensus bridge on sales, AI sales and both margins; customer-level GW schedules (OpenAI 1.3GW in 2027, Meta 3GW, $6B of POs) and locked HBM pricing, with above-consensus F26/F27/F28 EPS.

**Data support.** Full P&L, balance sheet and cash-flow model to F28; F2Q26 results and F3Q26 guidance-versus-consensus exhibits; segment exhibit; bull/bear page.

**Event context.** Filed 03 Jun 26 (disseminated 04 Jun) right after the F2Q26 print, stock at $413.21 following a pullback — a dated post-print call.

### 8/10 — Goldman Sachs — *Strong AI revenue momentum for 2027， despite modest near~term shortfall relative to…*
`9 pp · 2026-06-03 · Buy, PT $525 · $478.47 → +9.7%`

**Why bullish/bearish.** AI semis scaled to $133bn/$193bn in FY27/28 on ~10GW of deployments: six XPU engagements (Google, Meta, Anthropic, OpenAI plus two unnamed with $6bn of POs), Anthropic adding 5GW from FY27, Meta 1GW in 2H27. Components secured through FY27; inventory built $3.0bn→$4.3bn. PT 30x normalized EPS $17.50.

**Insight density.** Mostly management commentary replayed through GS's variance tables; the fresh item is the customer-by-customer GW map and the call that FY26 AI ($57bn) slipped only on delayed new-customer ramps.

**Data support.** Exhibits: quarterly variance vs GS/Street, guidance vs consensus, new-vs-old estimates table (FY26-28 AI, revenue, EPS), bull/base/bear P/E PT build, full GS forecast grid.

**Event context.** FQ2-26 print (3 June): revenue $22.2bn in line, AI $10.8bn +143% Y/Y; the FQ3 AI guide of $16.0bn missed GS $17.4bn and Street $16.4bn even as total revenue guidance beat.

### 8/10 — Bernstein — *FQ226 recap~Wait for it...*
`24 pp · 2026-06-04 · OP, PT $550 · $418.25 → +31.5%`

**Why bullish/bearish.** FQ2-26 beat ($22.2B/$2.44); AI semis ~$10.8B, +143% YoY. The reiterated FY27 $100B AI guide is read as conservatism, not share loss: ~10GW ships 2H-weighted, implying a materially higher FY28 run-rate, and Anthropic racks were dropped (lower revenue, lower margin); Google/Meta LTAs stay robust.

**Insight density.** Restated company and consensus figures with Bernstein variance tables; the fresh calls: FQ3 AI ~$16B undershoots Street only because Anthropic racks left the mix, and non-AI semis are finally recovering.

**Data support.** 19 exhibits: results/guidance variance vs Street, segment GM/OPM, FCF build, inventory and net debt, plus a full FY26-28 income statement, balance sheet and cash flow model; AI revenue $56.0B/$108.7B/$168.5B.

**Event context.** Written hours after the FQ2-26 print and FQ3 guide; the stock fell ~14% after hours on the AI guidance miss and the decision to reiterate rather than raise FY27 $100B.

### 8/10 — J.P. Morgan — *Ignore The Noise - TPU v9 2nm ASIC Program On Track For CY28 Ramp - NO Delays; Secures Next…*
`10 pp · 2026-06-16 · OW, PT $580 · $376.11 → +54.2%`

**Why bullish/bearish.** TPU v9 2nm (4 compute die, 16 HBM stacks, 400Gbps SerDes) still ramps in CY28 with no delay; Broadcom qualifies v8i "Sunfish" now while Google's COT "Zebrafish" v8t stalls — an 18-month lead; the March GOOG deal locks TPU v8-v11 and rising annual revenue through 2031.

**Insight density.** Supply-chain primary research: named program specs, design-start timing, COT yield risk on EMIB packaging and an 18-months+ lead claim — a differentiated rebuttal, not restated consensus.

**Data support.** No model or exhibits; cites prior notes, a PT built on 20-25x (23x) $25.35 FY27-exit earnings power, and the rating history table.

**Event context.** 16 Jun 26, AVGO at $376.71, written into a wave of delay/cancellation headlines from sell-siders and Asia press — a dated, falsifiable call.

### 8/10 — J.P. Morgan — *Samsung Multi~Year Memory Foundry MOU Implies - $1 Trillion of Cumulative Broadcom AI…*
`9 pp · 2026-07-27 · OW, PT $580 · $383.22 → +51.3%`

**Why bullish/bearish.** Samsung supplies 75-85% of AVGO's HBM DRAM; the MOU's >$200B of Samsung memory/foundry content (90-95% HBM) implies >$1T cumulative Broadcom AI revenue over 2026-2030, a 60%+ CAGR, plus $40-50B of Samsung-foundry chip sales.

**Insight density.** Proprietary bridge from a supplier's public MOU to a >$1T AVGO AI-revenue pool; the 75-85% HBM share and $40-50B foundry estimate are JPM's own, not consensus.

**Data support.** No exhibits or model; valuation is 20-25x (23x) $25.35 of FY27-exit earnings power. Of nine pages, the argument is three paragraphs and the rest disclosure.

**Event context.** Written 27 Jul 26, two days after Samsung announced the MOU, with AVGO at $381.90 — a news-driven reiteration, not a print.

### 7/10 — Goldman Sachs — *Partnership with OpenAI reinforces Broadcom’s technology advantage in custom silicon*
`7 pp · 2025-10-13 · Buy, PT $380 · $354.71 → +7.1%`

**Why bullish/bearish.** Bullish on the OpenAI 10GW custom accelerator and networking deal deploying 2H26 to end-2029: GS builds ~$10-15bn of revenue and ~$1.00-1.50 of EPS per GW ($9,000 ASP, 900-1,200k units), incremental to the earlier OpenAI disclosure, while flagging OpenAI's funding risk.

**Insight density.** Proprietary only in the per-GW scenario table, which stress-tests three ASIC-versus-GPU power-efficiency cases; the rest is reaction to the joint release and AMD's rival 6GW OpenAI deal.

**Data support.** Exhibit 1 per-GW model with explicit inputs (Nvidia $35k/GW, 80/20 compute/networking split, $9,000 ASP, 55% blended GM); PT $380 at 38x normalized EPS $10.00, up from $9.50.

**Event context.** Published the same day Broadcom and OpenAI announced the 10GW partnership; AMD's offsetting OpenAI deal and the absence of disclosed financing are the framing.

### 7/10 — Goldman Sachs — *4Q Preview： Expect solid quarter with strong momentum driving upside to AI revenue in 2026*
`6 pp · 2025-11-25 · Buy, PT $435 · $382.88 → +13.6%`

**Why bullish/bearish.** Expects FY26 AI revenue guidance above the ~100% YoY consensus on Google/OpenAI XPU ramps (XPU revenue +160% YoY) plus Tomahawk 6 networking; $435 is 38x normalized EPS of $11.50, 15.1% upside to $377.96.

**Insight density.** No channel checks: positioning colour plus GS's own numbers. FY26/27 total revenue sits 3%/21% above Street and AI semis 10%/38% above, but the edge is model, not data.

**Data support.** Exhibit 1 GS-vs-Street by segment for FY4Q25-FY27E, GS forecast table, new FY28-30 EPS $17.35/$20.00/$22.40, PT build and risks.

**Event context.** Ahead of the early-December FQ4 print; triggers are FY26 AI guidance, Google/OpenAI contributions, XPU gross-margin dilution, set against strong Gemini 3 and Nvidia datapoints.

### 7/10 — Goldman Sachs — *1Q Preview： Expect a solid quarter， with continued AI momentum*
`6 pp · 2026-02-19 · Buy, PT $450 · $332.76 → +35.2%`

**Why bullish/bearish.** Mechanism: XPU rack timing back-loads the upside. GS FY26 AI revenue $54.1bn is 6% above Street; FY26E EPS $11.07 vs Street $10.34; upside to both quarter and guide, more of it in 2H.

**Insight density.** Mainly consensus framing: the four call items are the FY26 AI guide, XPU customers, margin dilution, software disruption. GS estimates sit 4-6% above Street off checks, not new data.

**Data support.** Exhibit 1 GS-vs-Street summary by segment for FY1Q26-FY27E; GS forecast table; $450 = 38x normalized EPS of $12.00.

**Event context.** Pre-print note ahead of the FQ1-26 report, written into "peak CapEx" worries and fears that AI disrupts Broadcom's software business; price $333.51, not the $400s.

### 7/10 — BofA — *US Semiconductors Scaling AI with Photons-Primer on Optical Interconnects*
`46 pp · 2026-03-09 · Buy, PT $450 · $344.48 → +30.6%`

**Why bullish/bearish.** Bullish: AVGO owns the non-NVDA CPO roadmap — Humbolt to Bailly (TH5, 51.2TB/s) to Davisson (TH6, 102.4TB/s) with 3.5x power savings and 40% lower cost per bit; Meta logged 15mn device hours on Bailly with ~2.5mn-hour MTBF versus under 1mn for pluggables.

**Insight density.** Proprietary bottoms-up optics/networking model ($73bn optics TAM by CY30), but AVGO-specific evidence is third-party (Meta OCP 2025, Besi bonding) rather than ticker channel work.

**Data support.** Full CPO/OCS supply-chain profiles, TAM builds with ASP and unit tables, AVGO CPO roadmap exhibit, Meta reliability data; PO based on CY27E EPS.

**Event context.** Primer published 9 Mar 2026 off OFC 2025/OCP 2025 disclosures; no AVGO print or deal — CPO revenue inflection pushed to CY27/28.

### 7/10 — J.P. Morgan — *Semiconductors： OFC Conference： Strong CY26~CY27 Optical Networking Setup， High Innovation，…*
`10 pp · 2026-03-19 · OW, PT $500 · $318.67 → +56.9%`

**Why bullish/bearish.** Broadcom's switching/routing backlog has grown above $15B as Tomahawk 6 (102Tbps) starts ramping, and JPM saw 400G-per-lane PAM4 DSP for 1.6T plus Davison co-packaged optics on Tomahawk 6 at OFC.

**Insight density.** Meetings-derived datapoints from OFC rather than restated consensus: the >$15B backlog, 400G/lane DSP roadmap, AEC reach (5m, optimizing to 6m) and CPO progress are AVGO-specific.

**Data support.** No AVGO model or exhibit: support is a qualitative product-by-product bullet plus module-maker industry forecasts (80-90M 800G/1.6T units in 2026, 150-160M in 2027).

**Event context.** Optical Fiber Communication conference in Los Angeles, where JPM met Broadcom, Marvell and MACOM; the Tomahawk 6 upgrade cycle and 1.6T ramp drive the CY26-CY27 setup.

### 7/10 — UBS — *US Semiconductors： Stellar Optics and Fast~Paced Networking at OFC 2026*
`21 pp · 2026-03-22 · Buy, no PT · $309.37 · upside n/a`

**Why bullish/bearish.** Bullish on AVGO networking/optics: Tomahawk 6 in full production volume, the first Taurus 400G/lane DSP already shipped (2x radix at 1.6T), CPO through reliability testing, 50M lasers a year from internal fabs, and AVGO's view that optical scale-up crosses over below 10pJ/bit in 2028.

**Insight density.** Booth tour with AVGO IR and an optical-systems VP: fresh production and shipment datapoints, socketed-CPO signal-integrity limits, and AVGO's 10pJ/bit crossover versus the 5pJ/bit industry view.

**Data support.** No AVGO model; product detail (Davisson TH6-based CPO switch, interoperable NPO, OCI MSA, 6m AECs, PCIe switch) plus the AVGO PT history (Buy, $475 as of 15 Dec 2025).

**Event context.** OFC 2026 during GTC week, where AVGO announced TH6 volume production and the first 400G/lane DSP shipment — a product-cycle event, not a financial print.

### 7/10 — Bernstein — *Many major multi Meta MTIA...*
`11 pp · 2026-04-15 · OP, PT $525 · $396.09 → +32.5%`

**Why bullish/bearish.** Meta's multi-year extension covers >1GW initially, multiple MTIA generations for training and inference plus networking, through at least 2029; Hock moves off Meta's board to an advisory role. Bernstein says the FY27 ~$100B AI guide looks light — each ~$10B of AI revenue is ~$1/share EPS.

**Insight density.** Mostly restatement of the 14 Apr Meta release and AVGO's March guidance; the fresh angles are the board-conflict read and the $10B-AI-revenue-to-$1-EPS sensitivity.

**Data support.** No model build — FY26/F27E EPS $11.38/$17.73, EBIT $52.4B/$88.7B, FCF $55.1B/$85.3B, verbatim quotes from the Meta announcement, rating/PT history chart.

**Event context.** Written hours after Meta's 14 Apr 2026 MTIA partnership announcement, with Hock Tan stepping off Meta's board.

### 7/10 — UBS — *Thoughts On Google’s TPU v8 Generation*
`14 pp · 2026-04-22 · Buy, PT $475 · $421.98 → +12.6%`

**Why bullish/bearish.** At Cloud Next '26 Google split TPU v8: single-die v8t for training (MediaTek) and dual-die v8i for latency-sensitive inference (AVGO), with 288GB HBM and 384MB SRAM (~3x gen-over-gen), ~80% better perf/$, and inference pod scale up from 256 to 1,152 TPUs.

**Insight density.** Fresh proprietary attribution of the v8 chips to suppliers, built on UBS's earlier Zebrafish/Sunfish work; model unchanged, so the value is the read-across to ARM (2x CPU hosts) and Semtech (copper).

**Data support.** Figure 1 v8-vs-Ironwood spec table (pod size, FP8 EFlops, HBM bandwidth/capacity) from company data; rating/PT history to $475; no new model.

**Event context.** Written on Google's Cloud Next '26 TPU v8 launch; UBS explicitly says little here is new versus its own estimates.

### 7/10 — Goldman Sachs — *1Q Preview： Expect strong guidance， with focus on FY27 AI revenue and XPU customer…*
`7 pp · 2026-05-19 · Buy, PT $500 · $410.42 → +21.8%`

**Why bullish/bearish.** Sees upside to both quarter and guidance, with incremental FY27 colour pulling Street AI numbers higher. GS models AI semis $57.3bn FY26 and $132.6bn FY27 (revenue 4%/12% above Street); $500 is 30x normalized EPS of $17.

**Insight density.** No proprietary data: the edge is the size of GS's above-Street AI estimates and margin framing; the three call items (AI guidance, XPU engagements, margins) are consensus questions.

**Data support.** Estimate-change table with GS-vs-Street revenue, gross margin, operating income, EPS and AI/Non-AI/software segments for FY2Q26-FY27, GS forecast table, PT history.

**Event context.** Ahead of the fiscal 1Q (June) print; focus on FY26/27 AI revenue detail, new XPU customer onboarding, competition at key accounts, XPU margin dilution, Tomahawk 6 ramp.

### 7/10 — Morgan Stanley — *Semiconductors Weekly Earnings Week 7 AVGO Preview*
`24 pp · 2026-05-31 · OW, PT $485 · $446.06 → +8.7%`

**Why bullish/bearish.** Rack deployments — most of the ~$21bn Anthropic opportunity — slid out of 2H26 into 2027, so JulyQ AI revenue drops from $19.5bn to $16.9bn (56% q/q); MS argues capacity is reallocated, not lost. CY26/CY27 AI $74bn/$133bn; only 10-15% of TPU content realistically at risk to MediaTek.

**Insight density.** Thin on new data: "exceptionally strong" networking checks and a ~$20bn/GW framework MS itself calls bull-case. The one differentiated judgement caps realistic CoT share loss at 10-15% of TPU content.

**Data support.** MS-vs-consensus quarter table, risk-reward with bull/base/bear PTs ($619/$485/$298) and options-implied probabilities, MS-vs-Street EPS and revenue table, sector inventory, DOI and short-interest exhibits.

**Event context.** AVGO reports after the close on 3 June; the print is expected to meet elevated expectations rather than beat and raise. Same note carries the week's inventory, DOI and short-interest data.

### 7/10 — J.P. Morgan — *Asian Tech： Key takeaways from Broadcom’s Apr~Q results*
`8 pp · 2026-06-04 · OW, no PT · $418.25 · upside n/a`

**Why bullish/bearish.** Overweight. Bullish on AVGO's ramp — AI revenue $10.8B in 2Q26 (+143% YoY, 49% of total), 2H doubling to ~$56B FY26 and >$100B FY27, bookings >$30B. But JPM reads the absent numerical 2027 upside, plus MediaTek pulling ASIC guidance forward, as a real TPU share concession.

**Insight density.** Supplies what the company did not: Asia checks identify the two unnamed customers as ByteDance and SoftBank/ARM (~$6B purchase orders) and confirm 3-5 year LTAs on substrates, HBM and CCL.

**Data support.** Management quotes on Google, Anthropic, OpenAI (late-2026 production) and Meta (1GW MTIA order); non-AI semis $4.2B, +6% YoY, guided ~$4.5B; Tomahawk 6 and a 200Tb switch tape-out.

**Event context.** Written the day after Broadcom's Apr-Q (2Q26) print, translating it for the Taiwan, Korea and Japan supply chain.

### 7/10 — Bernstein — *Global Memory Global Memory， NVIDIA & Broadcom： Quick thoughts on strategic partnerships*
`16 pp · 2026-07-27 · OP, PT $550 · $383.22 → +43.5%`

**Why bullish/bearish.** Samsung-Broadcom MOU covers ~$200bn of memory (including HBM) plus foundry/advanced packaging through 2030 (2nm and below, 2.3D Cube-E/-R, 2.5D Cube-S) for AI/networking silicon, easing supply constraints behind AVGO's $100bn+ AI guide next year. PT is 25x average FY27/28 pro-forma EPS of $22.17.

**Insight density.** Fresh read: maps Samsung's Cube-E/-R and Cube-S packaging onto TSMC CoWoS-L/-R/-S, flags that whether AVGO's AI ASIC moves to Samsung wafers is still unclear, and argues TSMC's demand queue protects its earnings.

**Data support.** Two exhibits comparing Samsung and TSMC advanced-packaging variants; consensus memory revenue exhibit ($0.9Tn/$1.3Tn/$1.3Tn CY26-28); ticker table with AVGO 2026E/2027E EPS $11.60/$18.69.

**Event context.** Korean government AI Summit in San Francisco, 24 July 2026, where Samsung, SK hynix, NVIDIA and Broadcom signed MOUs, following the 7 July SK hynix-NVIDIA LOI.

### 7/10 — J.P. Morgan — *FY26 AI Sales On Track For $56B+ （up 180% Y Y+）； TPU Design Win Roadmap Remains Intact；…*
`9 pp · 2026-08-19 · OW, PT $580 · $362.48 → +60.0%`

**Why bullish/bearish.** FY26 AI revenue on track at $56B+ (up 180%+ Y/Y) and 2x-2.5x in FY27; TPU v8i ramping and v9 2nm set for early CY28; Tomahawk 5/6 demand exceeds supply with TH6 sold out through next year; Alchip/GUC and AMD/MRVL serve COT support and attach chips, not core TPU design.

**Insight density.** Program-by-program status (Meta's 5 MTIA, OpenAI Jalapeno, Anthropic TPU v7-v9, ByteDance/Alibaba, SoftBank/ARM, Apple, SambaNova) plus a competitor-by-competitor disambiguation; the 18-month-lead and $1T lines repeat June.

**Data support.** No model or exhibits; cites prior notes, the Samsung note's >$1T cumulative-AI-revenue math, and the 14-of-Google's-designs track record.

**Event context.** 19 Aug 26, AVGO at $362.48 — a quiet-patch rebuttal to competitive-noise headlines (Alchip/GUC awards, CoWoS-cut chatter); no print.

### 7/10 — Goldman Sachs — *Americas Technology： Semiconductors： Communacopia + Technology Conference 2026 ~ Day 1…*
`9 pp · 2026-09-08 · Buy, PT $540 · $368.56 → +46.5%`

**Why bullish/bearish.** Bullish: management reaffirmed FY27/FY28 AI revenue of $115bn/$230bn, at least 100% growth and supply-constrained; the $35bn XPV partnership with Blackstone/Apollo can support over 20GW; a 1GW cluster generates ~$30bn revenue against ~$10bn annual opex.

**Insight density.** Fresh management-sourced datapoints — XPV financing structure, 20GW capacity, frontier vs. open-weight economics (~75% of industry revenue on similar training spend) — not restated consensus.

**Data support.** Verbatim Hock Tan takeaways; no model or exhibits; PT basis 30x normalized EPS with four listed downside risks.

**Event context.** Live conference presentation 8 Sep 2026; the debate is whether $115bn FY27 AI revenue is achievable given land, power and shell bottlenecks.

### 6/10 — BofA — *US Semiconductors TPU intensifies competitive race, but in a rising tide, Buy NVDA, AVGO…*
`8 pp · 2025-11-25 · Buy, PT $400 · $382.88 → +4.5%`

**Why bullish/bearish.** TPU ramp and Anthropic are incremental AVGO ASIC demand — BofA models ~100%+ YoY AI sales growth in CY26, calls the 38x CY26 PE a justified premium, and flags the bear case that Google licensing TPUs directly would cut AVGO's ASIC TAM.

**Insight density.** Fresh angle but no proprietary data: the AVGO view rests on TPU/Anthropic project expectations, while the note's quantified work (AI TAM to $1.2tn by 2030, NVDA EPS power $20+) is NVDA-centric.

**Data support.** AVGO is a comp in Exhibit 1's TAM/EPS-power model; support comes from the PO basis (37x CY26E, 10x-38x historical range) and the stock table ($377.96, $400 PO).

**Event context.** Written after Google's Gemini 3 launch, Anthropic's Claude Opus 4.5 release and press reports of Google renting TPUs to Meta in 2026 and on-premise deployments in 2027.

### 6/10 — B&M (巴芒投研, independent) — *财报前瞻*
`9 pp · 2025-12-07 · no house call · no PT row`

**Why bullish/bearish.** Q3 backlog $110B, half AI-linked; Q4 AI revenue guided to $6.2B (+66% y/y) inside ~$17.4B total (+24%); FY26 AI guide assumed >$30B against GS's $45.4B (+128%); VMware mix lifts margin; stock $390.24, 28-30x forward.

**Insight density.** No proprietary or channel data whatsoever — restates GS, Mizuho, Morgan Stanley, Forbes, CNBC, TipRanks; its only original output is the author's own Q4/FY26 assumption set.

**Data support.** Dated news timeline with analyst PTs plus an explicit Q4 model ($17.4B revenue, $6.2B AI, 75-77% non-GAAP GM, 60-67% EBITDA margin); no exhibits or SOTP.

**Event context.** Pre-print preview before Q4 FY25 results, written after the 24/28 Nov 2025 Google-TPU and Gemini 3 rally (+11%, +16%) and the Microsoft custom-silicon reports of 6 Dec.

### 6/10 — Morgan Stanley — *Semiconductors： Weekly： Expect a strong AVGO outlook*
`21 pp · 2025-12-08 · OW, PT $443 · $398.86 → +11.1%`

**Why bullish/bearish.** AI revenue modelled at $6.2bn (+19% q/q) in OctQ and $6.7bn (+9%) in JanQ; the bigger inflection is 2H26, when AVGO ships $10bn of racks to Customer #4, which MS identifies as Anthropic via its Google Cloud deal. ASIC revenue to double in FY26 and FY27; PT 41x MW EPS $10.79.

**Insight density.** Asia channel checks show the TPU supply chain being revised higher. Sharp caveat: 4/5 of AVGO's ASIC customers have TPU ties, so TPU upside partly substitutes other ASIC programmes. Otherwise the standing thesis.

**Data support.** MS-vs-consensus table with segment and gross-margin detail, risk-reward with bull/bear PTs ($592/$282), MW EPS and DOI drivers table, sector inventory and short-interest exhibits.

**Event context.** Pre-print for the 11 December FQ4-25 report; otherwise a quiet patch, with the Anthropic–Google Cloud rack deal the news hook and the 2H26 rack shipment the next catalyst.

### 6/10 — Bernstein — *U.S. Semiconductors and Semiconductor Capital Equipment Bernstein Semi Cycle Tearsheet： Too…*
`74 pp · 2026-03-23 · OP, PT $525 · $322.00 → +63.0%`

**Why bullish/bearish.** Bullish: OP with $525 PT (29.6x 2027E EPS $17.73). Calls AVGO's $100B AI revenue guide extremely conservative, sees "real" CY27 EPS of $20+ and thus ~15x or less, with software, cash deployment and superb margins/FCF as the 2026 accelerants.

**Insight density.** Mostly own-model work, no AVGO channel check; the fresh content is the cycle framing ($100B is conservative) and the EPS path (11.38 in 2026E, 17.73 in 2027E) versus peers.

**Data support.** Full AVGO income statement, balance sheet and cash flow exhibits through 2028E (revenue $102,981M / $154,651M / $196,988M), ticker table with PT, relative performance and Q4 beat/miss table.

**Event context.** Quarterly cycle check after a Q4 where AVGO beat revenue by 0.3% and guided the next quarter +5.2%; AI trade stalling even as estimates moved up.

### 6/10 — J.P. Morgan — *TSMC（2330.TW） CoWoS and advanced back~end updates*
`16 pp · 2026-04-08 · OW, no PT · $350.08 · upside n/a`

**Why bullish/bearish.** Bullish on AVGO's ASIC franchise via supply chain: JPM lifts Broadcom CoWoS consumption to 250K wafers in 2026 and 400K in 2027, with TPU shipments of 4.3M/6.9M units (Sunfish/Pumafish), plus Meta MTIA returning to Broadcom. MediaTek's lower-cost TPUv8x/Zebrafish is the competitive watch item.

**Insight density.** Channel checks, not consensus restatement: revised Broadcom CoWoS wafer allocation, TPU v7/v8ax unit forecasts, MediaTek split for v8x, and TPUv9 Pumafish (Broadcom 3D SoIC) versus Humufish (MediaTek/Intel EMIB).

**Data support.** CoWoS allocation table by customer 2023-27E, TPU unit build table, advanced back-end supply-chain map naming Broadcom sockets (Ironwood, Sunfish, Pumafish, MTIA Arke/Phoebe, OpenAI Titan, Tomahawk 6).

**Event context.** Earlier-dated twin of the 9 April note (pre-correction text; shipped 08 Apr 10:25pm HKT); same packaging-capacity and TPU order-visibility trigger, no AVGO-specific event.

### 6/10 — J.P. Morgan — *TSMC CoWoS and advanced back-end updates*
`16 pp · 2026-04-09 · OW, no PT · $354.35 · upside n/a`

**Why bullish/bearish.** Bullish on AVGO's ASIC franchise via supply chain: JPM lifts Broadcom CoWoS consumption to 250K wafers in 2026 and 400K in 2027, with TPU shipments of 4.3M/6.9M units (Sunfish/Pumafish), plus Meta MTIA returning to Broadcom. MediaTek's lower-cost TPUv8x/Zebrafish is the competitive watch item.

**Insight density.** Channel checks, not consensus restatement: revised Broadcom CoWoS wafer allocation, TPU v7/v8ax unit forecasts, MediaTek split for v8x, and TPUv9 Pumafish (Broadcom 3D SoIC) versus Humufish (MediaTek/Intel EMIB).

**Data support.** CoWoS allocation table by customer 2023-27E, TPU unit build table, advanced back-end supply-chain map naming Broadcom sockets (Ironwood, Sunfish, Pumafish, MTIA Arke/Phoebe, OpenAI Titan, Tomahawk 6).

**Event context.** Post-1Q26 pre-print packaging update; trigger is the upward CoWoS/SoIC capacity revision and TPU order visibility. No AVGO print or deal of its own.

### 6/10 — BofA — *US Semiconductors-AI 2030-Stronger for longer for compute, memory, networking*
`32 pp · 2026-05-13 · Buy, PT $450 · $416.13 → +8.1%`

**Why bullish/bearish.** BofA's build lifts AVGO accelerator sales power from $16.2bn CY25 to $47.2bn CY26E, $89.5bn CY27E and $135.3bn CY28E — implied share up from 8% to 16% of a $1.2Tn CY30 accelerator TAM. Recent Google/Meta frame contracts underwrite FY27 consensus of $110bn AI sales; PO is 26x CY27E P/E.

**Insight density.** The TAM build (IT spend, $1.7Tn AI DC, HBM content, optics) is proprietary, but AVGO gets only an accelerator-share row plus the frame-contract point — no AVGO estimate change, model or channel check.

**Data support.** Exhibit 2 tabulates AI DC TAM by component to CY30E; Exhibit 3 gives vendor accelerator sales power (AVGO row); PO basis is 26x CY27E P/E and $60bn net debt.

**Event context.** Three weeks before the early-June print, written on cloud capex momentum (CY26 +68% YoY) and the Google/Meta frame contracts — a framing note, not an AVGO catalyst.

### 6/10 — Morgan Stanley — *Semiconductors Takeaways from our meetings in Taiwan*
`12 pp · 2026-06-01 · OW, no PT · $459.24 · upside n/a`

**Why bullish/bearish.** Bullish on share defence: MS expects AVGO to hold 80%+ of its ASIC customers, consistent with MediaTek's stated 15-20% long-term target; MediaTek buying HBM outside AVGO's contracts costs more, so the 80/20 split feels right near term.

**Insight density.** Meeting-based and genuinely fresh: supply-chain contacts see a strong TPU ramp and no readiness for majority MediaTek share before 2028, and supply-chain HBM pricing versus AVGO's contract prices is a new angle.

**Data support.** No AVGO model; valuation line only (28x CY27e ModelWare EPS $17.33), explicit AVGO upside/downside risk list, and MS's own internal team disagreement on MediaTek share.

**Event context.** Meetings at and adjacent to MS's Taiwan AI summit just before publication; no AVGO print or deal — AVGO's own "significant majority share" guidance is the anchor.

### 5/10 — B&M (巴芒投研, independent) — *公司财报前瞻分析*
`6 pp · 2025-09-03 · no house call · no PT row`

**Why bullish/bearish.** Expects a beat on Q3 FY25 revenue of $15.8-16.2B (+25%) and AI chips stepping $4.4B→$5.1B q/q (+16%) per guidance; gross margin above 65%; VMware software +25% y/y to $6.6B with Walmart as a flagship VCF win.

**Insight density.** Zero proprietary data — every datapoint is already public through TipRanks, Forbes and Investopedia; consensus and risks are restated generically.

**Data support.** An assumption block (revenue band, >65% margin floor, FY25 guidance raise) plus price $298.24 and ~108.85x GAAP P/E; no exhibits, model or management quotes.

**Event context.** Written 3 Sep 2025, days before the FQ3-25 print, just after Nvidia's late-August report dragged AVGO down ~7%.

### 5/10 — J.P. Morgan — *Semiconductors Semi Cap Equipment： 1Q26 Preview： Sustained AI Demand， Broadening Cyclical…*
`26 pp · 2026-04-17 · OW, no PT · $405.90 · upside n/a`

**Why bullish/bearish.** Bullish and specific for a sector note: the switching/routing backlog has grown above $15bn as Tomahawk 6 (102Tbps) ramps, and AI revenue that hit $20bn in FY25 (Google TPU, Meta MTIA) should reach $65bn+ in FY26 and "well in excess of $120B" in FY27.

**Insight density.** Channel checks carry the load — HBM sold out for CY26 with CY27 contracting talks, optical module units 40-45M to 80-90M to 150-160M; the AVGO backlog and AI-revenue datapoints sit inside that sector frame.

**Data support.** AVGO is one row of the comp table (OW, $398.47, C26E EPS $14.78 = 27.0x; JPM 2Q26E EPS $3.60 versus Street $3.20), plus dividend, JPM-versus-consensus and VMware M&A-history lines.

**Event context.** 1Q26 earnings-season preview of 17 Apr 2026: datacenter capex above 70% y/y in 2026 and Nvidia's $1T+ Blackwell/Rubin orders argue AI capex beats the low-teens 2027 Street view.

### 5/10 — Bernstein — *Qualcomm Inc（QCOM.US）： FQ226 recap~We hope they put on a good show in June...*
`22 pp · 2026-04-30 · OP, PT $525 · $416.77 → +26.0%`

**Why bullish/bearish.** Bullish relative call: buy NVDA or AVGO "at likely cheaper real valuations with numbers going up instead of down". QCOM is "a very late entry to the ASIC / AI space (get in line behind NVDA, AVGO, AMD, MRVL, Cerebras, Arm...)". $525 = ~30x FY2027 pro-forma EPS $17.73.

**Insight density.** Largely restated: QCOM model refresh plus the late-entrant ASIC barrier thesis are house views; the AVGO lines are the standard valuation-block reiteration, not new work.

**Data support.** QCOM exhibits 1-14 and itemized FY26-28 estimate changes; AVGO has one target sentence (30x $17.73) and a risk bullet list.

**Event context.** QCOM's FQ226 print with a very weak FQ326 guide and a hyperscaler ASIC disclosure ahead of the June analyst day; AVGO's own catalysts are absent.

### 5/10 — Morgan Stanley — *Semiconductors - North America Selloff of US memory stocks creates a compelling entry point*
`16 pp · 2026-07-20 · OW, no PT · $378.16 · upside n/a`

**Why bullish/bearish.** Bullish: "the best value in the market comes from the compute names, notably NVDA and AVGO", with memory merely catching up. AVGO is valued at 28x CY2027e ModelWare EPS $17.92, roughly 26x non-GAAP EPS of $19.59, in-line or below the AI peer group.

**Insight density.** Strong on memory — data-centre purchasing checks, 3q prices up 25%+, LTA structure, NVIDIA LPDDR5 de-speccing. AVGO adds no new datapoint of its own.

**Data support.** Memory risk-reward pages, MS-vs-consensus tables, DRAM spot versus Micron EV/S chart; AVGO gets only the valuation-methodology block and risk bullets.

**Event context.** July selloff in US memory stocks and Micron's price-ceiling comment; AVGO itself is silent — no print, deal or regulatory news.

### 4/10 — Bernstein — *Asia Tech Hardware： Future of Tech~Mapping the CPO value chain*
`33 pp · 2026-03-04 · OP, PT $475 · $316.36 → +50.1%`

**Why bullish/bearish.** Bullish, thinly: Broadcom's TH6 switch ships this year, the Broadcom/Corning Bailly CPO whitepaper anchors the platform, and Broadcom is among the customers shifting from GlobalFoundries to TSMC's COUPE. Nothing in the note models AVGO or justifies the $475 target.

**Insight density.** The proprietary work is an Nvidia-chain teardown (Quantum X800-Q3450 BOM ~$70K; OE 44-45%, ELS 13%, MPO 8%, switch chip 17%); Broadcom itself gets no original channel or cost data.

**Data support.** CPO BOM build-up, a comparison (CPO OE+ELS ≥10% above 1.6T transceivers) and supplier maps — all Nvidia-chain; AVGO's support is qualitative plus the ticker table ($313.84, target $475).

**Event context.** March-2026 CPO supply-chain deep dive keyed to TSMC's COUPE ramp and Nvidia's X800 CPO switch; Broadcom's own catalyst is the TH6 shipping this year.

### 4/10 — BofA — *NVIDIA Corporation（NVDA.OQ） Back to Basics： Boosting cash returns could be another rerating…*
`10 pp · 2026-04-27 · Buy, no PT · $417.54 · upside n/a`

**Why bullish/bearish.** Constructive as a benchmark: AVGO returned an average 92% of FCF in CY22–25 versus NVIDIA's 47%, with PEG 0.35x against 0.36x — the cash-return standard NVIDIA is asked to match. AVGO is also a stated risk: "rising competition from merchant (AMD) and ASIC (AVGO, Google, AWS) chips".

**Insight density.** Proprietary ownership and FCF-return series: dividend yield 0.62% with 47% of equity-income funds holding AVGO, second only to Microsoft. The AVGO lines are screen outputs, not AVGO work.

**Data support.** Peer comp table (33.3x/22.2x CY26/27E PE, EV/FCF 36.3x/23.5x, 58.4% sales and 63.4% EPS CAGR), equity-income ownership table, FCF-return table; no AVGO model.

**Event context.** NVIDIA earnings preview centred on capital-return policy; AVGO sits in the comparison set with no catalyst of its own.

### 4/10 — J.P. Morgan — *Semiconductors CY26 Data Center Capex Revised Higher and Strong Initial Growth Outlook of…*
`10 pp · 2026-04-27 · OW, no PT · $417.54 · upside n/a`

**Why bullish/bearish.** Constructive but not AVGO-specific: faster hyperscaler capex (CY26 +63%, CY27 +40%) plus a mix shift toward custom ASICs supports AVGO's $100B+ FY27 AI revenue and its XPU pipeline (Google/Anthropic TPU, Meta MTIA, OpenAI). AVGO is listed among top AI picks.

**Insight density.** Thin on AVGO: restates Broadcom's own $100B+ FY27 disclosure and adds JPM/650 Group capex forecasts and installed-power data; no AVGO channel check or estimate revision.

**Data support.** Three capex exhibits (top-4 CSPs, tier-2 CSPs/neoclouds, North America installed capacity); covered-companies list showing AVGO $422.76 / Overweight; no AVGO model or PT.

**Event context.** Trigger is the IT Hardware team's raised CY26 and initial CY27 capex outlook; quiet patch for AVGO itself between its FQ1 print and the next catalyst.

### 4/10 — Bernstein — *Global Semiconductors and Semiconductor Capital Equipment~ What to make of an earnings…*
`17 pp · 2026-05-11 · OP, PT $525 · $427.75 → +22.7%`

**Why bullish/bearish.** Bernstein decomposes the SOX's 66% YTD / 162% YoY move as ~100% earnings, not multiple (SOX P/FE 28x, -2% YTD). AVGO, with the GPU/ASIC group, has seen muted multiple expansion versus earnings and screens at "mid-teens P/FE on realistic CY27 EPS" ($17.73 CY27E).

**Insight density.** Sector-level work is proprietary (return split into EPS versus multiple; memory EPS +386% with multiples -21%, GPU/ASIC +56%/+35%). AVGO itself contributes a table row, a top-pick tag and one valuation line.

**Data support.** Exhibits 1-9 on SOX returns, 69% YTD NTM EPS growth and sub-segment drivers, plus a full ticker table: AVGO 2026E/2027E EPS $11.38/$17.73 at 37.8x/24.3x. No AVGO model.

**Event context.** Written after a blowout semis earnings season and a five-week vertical rally in the index; AVGO's own print is not the trigger — a quiet patch for the name.

### 4/10 — Bernstein — *U.S. Semiconductors and Semiconductor Capital Equipment U.S. Semiconductors： Deconstructing…*
`18 pp · 2026-05-12 · OP, PT $525 · $418.64 → +25.4%`

**Why bullish/bearish.** Outperform, PT $525. AVGO is bullish only as a preferred name: Bernstein says AVGO and NVDA screen cheap at "mid-teens P/FE on realistic CY27E EPS" and that a strong 2025 AI trajectory accelerates into 2026 on software, cash deployment and margins. The arguments are industry-wide.

**Insight density.** The proprietary work is industry-level WSTS analysis — Q1 revenues $299B, +79% YoY, memory +238% YoY at 46% of sales, industry ASPs +57% — with no AVGO channel data.

**Data support.** Eleven WSTS exhibits on revenue, units and ASPs; AVGO tearsheet only — EPS $6.82/$11.38/$17.73, P/E 62.8x/37.6x/24.2x at $428.43.

**Event context.** Quiet patch for AVGO — an interim industry look after Q1-26 WSTS data, published a month before any AVGO print.

### 4/10 — Morgan Stanley — *Semiconductors Weekly Meta GPU context; May SIA*
`20 pp · 2026-07-06 · OW, no PT · $373.90 · upside n/a`

**Why bullish/bearish.** Constructive: OW with bear/base/bull $308/$502/$637, base upside +39%, MS CY26e EPS $13.68 vs Street $12.89. The core call cuts the other way, though — sublettable GPU compute favours NVIDIA ubiquity because "ASIC capacity is much harder to sublet".

**Insight density.** Genuine industry work (SIA monthly variance, Meta cloud checks, DRAM/NAND vs MS estimates); the AVGO content is exhibit-level MS numbers rather than fresh AVGO-specific research.

**Data support.** Risk-reward table, MS vs Street EPS/revenue table, 2025-27 revenue and EPS CAGR charts, market-share table; no AVGO model or management quotes.

**Event context.** May SIA release plus Bloomberg's Meta cloud-unit report that pressured semis; no AVGO catalyst — quiet patch.

### 4/10 — Morgan Stanley — *Semiconductors Weekly： Earnings Week 4 （QNT， CBRS， ADI）； June SIA*
`31 pp · 2026-08-10 · OW, PT $502 · $422.40 → +18.8%`

**Why bullish/bearish.** Constructive: Overweight with bear/base/bull $308/$502/$637 against $427.76, +17% to base, grouped with NVDA and CBRS as the leading-edge logic preference. The house view is slightly below consensus on AVGO — CY27e EPS $19.59 versus Street $20.64.

**Insight density.** Real industry work on Quantum, Cerebras and Analog Devices results plus the June SIA print; the AVGO content is exhibit-level MS-versus-Street comparison rather than fresh AVGO research.

**Data support.** Risk-reward table, MS vs Street screen (revenue $180,289m vs $184,695m), 2025–27e revenue and EPS CAGR charts at 62% and 64%, short interest 1.4% of float; no AVGO model.

**Event context.** Week-4 earnings wrap and the June SIA release; no AVGO print, deal or regulatory trigger.

### 3/10 — UBS — *Global I O Smartphones： January ’26 Sell~Through： China impacted by base effect， but…*
`16 pp · 2026-03-06 · Buy, no PT · $329.27 · upside n/a`

**Why bullish/bearish.** Bullish by list entry: Broadcom sits among UBS's most preferred names, analyst Timothy Arcuri, Buy at US$332.77 with a US$475 target, and is named with ASE, Hon Hai, MediaTek, Micron, Samsung and TSMC as the supply-chain exposure to own. No AVGO mechanism is given.

**Insight density.** Deep handset channel work — China base effect, flat non-China units, memory-shortage downside to handset builds, Apple and Samsung insulation — none of which touches AVGO's AI or infrastructure drivers.

**Data support.** Handset unit and sell-through exhibits; AVGO gets the most-preferred row plus valuation columns (26E P/E 26.2x, 27E 15.0x, 26E/27E P/BV 15.58/9.28, priced 5 Mar 2026).

**Event context.** January smartphone sell-through print against a memory shortage; no AVGO event — quiet patch.

### 3/10 — UBS — *Equity Strategy： The Theme~ometer： AI Chips and Memory， Still Attractive*
`19 pp · 2026-04-16 · Buy, no PT · $397.84 · upside n/a`

**Why bullish/bearish.** Constructive but impersonal: AVGO scores 0.50 in the AI-Exposed Semis theme — regime 0.81, earnings 0.40, valuations 0.36, sentiment 0.31 — with 7.8% one-month earnings revisions and crowding rank 26. The signal is the theme, not the company.

**Insight density.** Proprietary quantamental REVS framework — machine-read EPS versus consensus, CTA momentum, crowding — applied to a theme basket. There is no AVGO-specific analysis, estimate change or thesis.

**Data support.** One screen table (market cap $1,764bn, factor scores) and the disclosure line AVGO.O Buy, US$380.78, 14 Apr 2026. No AVGO exhibit, model or quote.

**Event context.** Strategy-level thematic refresh on AI chips and memory; no AVGO catalyst — quiet patch.

### 3/10 — Morgan Stanley — *Global Technology Asia Pacific Global Technology 2026 Outlook – A Tale of Two Halves*
`59 pp · 2026-04-27 · OW, no PT · $417.54 · upside n/a`

**Why bullish/bearish.** Constructive but second choice: "stay OW on NVIDIA, Broadcom and Mediatek, with a preference for NVDA despite rising ASIC enthusiasm", on NVIDIA's industry-highest cloud ROI as Vera Rubin ramps in 2H26. No AVGO estimate, mechanism or valuation is given.

**Insight density.** Deck-level supply-chain work (HBM TAM build, total ASIC volume 5.8mn units in 2026e, +15%, ABF undersupply from 2027); AVGO benefits only as an unnamed ASIC supplier.

**Data support.** HBM/ASIC/ABF model slides and sector pick tables; no AVGO exhibit, estimate line or management quote anywhere.

**Event context.** 2026 outlook framing (strong 1H, demand-destruction risk into 2H26); no AVGO catalyst — quiet patch.

### 3/10 — UBS — *GlobalFoundries Inc（GFS.US） 1Q 2Q A Little Ahead Before Thursday's Analyst Day*
`26 pp · 2026-05-05 · Buy, no PT · $426.68 · upside n/a`

**Why bullish/bearish.** Mild relative bullishness: UBS prefers AVGO over GFS as the networking beneficiary with less smartphone baggage, and reads GFS's positive networking tone across to AVGO/MRVL/SMTC — but explicitly calls it "not really incremental", so nothing new on AVGO.

**Insight density.** No AVGO data. The networking read-across is flagged as already known, and GFS's SiGe/CPO and advanced-packaging commentary accrues to the ecosystem rather than being quantified for AVGO.

**Data support.** AVGO appears in the valuation/risk boilerplate (EV/FCF; M&A and dividend-yield risk) and in the disclosure price table (Buy, $427.36, 5 May 2026).

**Event context.** GFS 1Q26 results ahead and its Thursday analyst day; the AVGO mention is a relative-preference aside with no AVGO-specific catalyst.

### 3/10 — Bernstein — *US Industrials & Tech： The Data Center Project Pipeline ~ Capacity， Construction &…*
`41 pp · 2026-05-20 · OP, PT $525 · $417.10 → +25.9%`

**Why bullish/bearish.** Bernstein's inaugural monthly data-centre capacity tracker; it argues no single-name case, so both names are comp rows. META: broke ground on 1.1 GW in April, the most of any hyperscaler, 27% of hyperscaler capacity under construction (~5 GW active), but added -0.5 GW to pipeline. AVGO: Outperform, PT $525, EPS $6.82/$11.38/$17.73 in the semis ticker table only.

**Insight density.** Genuinely proprietary on the theme: an Aterio-sourced build tracker (pipeline 294.9 GW, +214% Y/Y; 58.6 GW under construction; 32.4 GW stranded; 114.9 GW behind-the-meter) and an electrical TAM build. No proprietary data on either ticker's own share.

**Data support.** 68 exhibits and a dashboard, plus an electrical TAM table (PWR $3,981B, VRT $914B, SU.FP $787B, ETN $690B per MW x pipeline). No META or AVGO model, target build or management quote.

**Event context.** A calendar tracker, not an event note: quiet patch for both names, no print, deal or regulatory hook. Shared entry - this PDF is read by both the META and the AVGO lens.

### 3/10 — HSBC — *Marvell Technology （MRVL.US） Upgrade to Buy： Ready to ride the AI~networking super~cycle*
`17 pp · 2026-05-26 · Buy, PT $450 · $421.34 → +6.8%`

**Why bullish/bearish.** Bullish in the table, cautious in the argument: HSBC limits Marvell to 50% of the 1.6T DSP market because "competition will intensify with the availability of Broadcom's 800G and 1.6T DSP solutions". AVGO is the share constraint, not the call — no AVGO estimate, mechanism or valuation is offered.

**Insight density.** Proprietary on Marvell only: optical DSP share splits, CXL and ASIC content, FY27/28 EPS $4.07/$7.12. The AVGO datapoint is a competitive assumption inside the Marvell model, not AVGO research.

**Data support.** Marvell segment models and share exhibits; AVGO gets one line in Exhibit 10, companies mentioned (CMP $414.14, TP $450.00, Buy, priced 22 May 2026).

**Event context.** Marvell pre-print upgrade two days before its results, framed on the AI-networking super-cycle; no AVGO print, deal or regulatory trigger.

### 3/10 — Morgan Stanley — *Semiconductors Weekly Earnings Week 6 (SMTC, MRVL)*
`26 pp · 2026-08-24 · OW, no PT · $358.76 · upside n/a`

**Why bullish/bearish.** Valuationally supportive by comparison: the MRVL target goes to $224 on a 45x CY27 multiple, but Marvell "still trades at more than 2x the multiple of AVGO and NVDA", making AVGO the cheaper ASIC expression. MS stays just below consensus, CY27e EPS $19.59 versus Street $20.68.

**Insight density.** Genuine Marvell work — Maia and Google TPU attach, a shift to more singles-and-doubles ASIC programmes, the April-quarter model. AVGO receives no research of its own, only the comparative multiple line.

**Data support.** Exhibit-level only: MS vs Street screen (revenue $180,289m vs $185,581m), 2025–27e revenue and EPS CAGR of 62% and 64%, short interest 1.3% of float at 21 Aug; no AVGO risk-reward or target.

**Event context.** Marvell pre-earnings preview week with an investor day flagged; nothing AVGO-specific — quiet patch.

### 3/10 — J.P. Morgan — *Semiconductors July WSTS： Seasonal M M Downtick Skewed by Memory Lumpiness； Industry Sales…*
`15 pp · 2026-09-08 · OW, no PT · $368.56 · upside n/a`

**Why bullish/bearish.** Overweight, no PT in the note. AVGO surfaces twice — in the compute list (NVDA, AVGO, AMD, INTC, MRVL) and the networking list (AVGO, MRVL, ALAB) — as a way to play a semis market JPM now models at $1.73T in 2026 and >$2T in 2027. No company argument.

**Insight density.** Proprietary WSTS monthly parsing — July sales $142B, -10% M/M but +129% YoY, DRAM ASPs +259% YoY — yet nothing on AVGO itself.

**Data support.** Thirty-four WSTS figures on sales, units, ASPs and seasonality; AVGO has a coverage-list line only, with no estimates or PT.

**Event context.** Monthly WSTS data drop (July 2026) plus company commentary over the prior 90 days; no AVGO print or event.

### 3/10 — Bernstein — *U.S. Semiconductors and Semicap Equipment~Can you put the AI genie back in the bottle？*
`13 pp · 2026-09-14 · OP, PT $575 · $344.72 → +66.8%`

**Why bullish/bearish.** Outperform, PT $575. Bernstein argues an AI "pacing slowdown" need not cut spending since inference demand already exceeds compute supply, and names AVGO a preferred play on a 2026 AI trajectory "set to markedly accelerate into 2027 and 2028." No AVGO argument beyond that.

**Insight density.** Nothing proprietary on AVGO; the news is Amodei's essay and its weekend amplification by Altman, Musk and Nadella. AVGO EPS and P/E figures are tear-sheet consensus, not new work.

**Data support.** Ticker table with AVGO EPS $6.82/$11.64/$18.63 and P/E 53.1x/31.1x/19.4x at $361.99; one-line investment implication. No model or exhibit on AVGO.

**Event context.** Published 14 Sep 2026 reacting to the weekend Amodei safety essay — a sector-sentiment piece, not an AVGO event.

### 2/10 — B&M (巴芒投研, independent) — *财报前瞻*
`14 pp · 2026-03-03 · no house call · no PT row`

**Why bullish/bearish.** No rating or PT is stated. The deck compiles dated AVGO headlines and TipRanks/Forbes items — Jefferies' Curtis on Alphabet and Broadcom, Mizuho's Jordan Klein on AVGO, a 19 Feb Forbes piece on AVGO questions and a 26 Feb Forbes piece — but the Chinese text is garbled and no stance survives.

**Insight density.** Pure aggregation, sourced from TipRanks, Forbes and CNBC headlines dated 5-28 Feb 2026. No proprietary data, and no analyst argument is recoverable from the OCR damage.

**Data support.** A dated headline index and source list (TipRanks, Forbes, CNBC); page 13 also references a VMware/OpenAI link. No model, exhibits or estimates.

**Event context.** Written 3 Mar 2026, two days before Broadcom's Jan-Q print — a preview/round-up rather than a post-print call.

### 2/10 — Goldman Sachs — *Advanced Micro Devices Inc. (AMD)-Upgrade to Buy as Agentic AI drives server CPU tailwinds…*
`15 pp · 2026-05-05 · Buy, no PT · $426.68 · upside n/a`

**Why bullish/bearish.** Not an AVGO call: GS says it "continues to view Broadcom (Buy - on CL) and Nvidia (Buy) as best positioned to outperform computing peers", while every number in the note (AMD server CPU TAM, 2027 datacenter GPU upside) belongs to AMD. No AVGO estimates, no AVGO thesis.

**Insight density.** Nothing AVGO-specific: the proprietary work (CPU share model, inference demand forecast) is AMD's, and Broadcom shows up as a comparison row in relative-P/E exhibits.

**Data support.** AVGO sits in Exhibit 9 (NVDA/AMD/AVGO NTM P/E) and Exhibit 14 (AMD's relative premium), plus the disclosure line "Broadcom Inc. (Buy, $417.43)" — a price, not a target.

**Event context.** AMD's upgrade day, 5 May 2026, driven by agentic-AI server CPU demand. No AVGO print or AVGO event in window; the $417.43 is simply the prior close.

### 2/10 — J.P. Morgan — *摩根大通-半导体设备-TMC会议总结： 第一季度业绩后动能持续-AI推理拐点、广泛周期性复苏、稳健内存上行周期、WFE周期拉长， 维持超配该板块*
`35 pp · 2026-05-23 · OW, no PT · $413.49 · upside n/a`

**Why bullish/bearish.** Overweight, no PT. AVGO is named in JPM's top-pick list (OW AVGO, MRVL, MU, KLAC, AMAT, CDNS, SNPS, ALAB, MKSI) and priced at $417.76 in Companies Discussed. Every page of conference takeaways belongs to another company; AVGO gets no thesis, estimate or datapoint.

**Insight density.** Conference-derived channel colour is rich — KLAC's "best visibility in a decade", MU's 5-year DRAM SCA, SNDK's $42B book — but none of it touches AVGO.

**Data support.** Per-company write-ups quoting management directly; AVGO appears only in the top-picks line and the price/rating list at $417.76.

**Event context.** JP Morgan's 54th annual TMC conference, 18-20 May 2026, three weeks after the Q1 prints; AVGO's own quarter is not the subject.

### 2/10 — Morgan Stanley — *NVIDIA Corp.（NVDA.US） Computex NVDA keynote & financial analyst Q&A*
`13 pp · 2026-06-03 · OW, no PT · $478.47 · upside n/a`

**Why bullish/bearish.** Overweight (since 06/09/2024, no PT in this note). AVGO is bullish only as context: MS values NVDA at ~22x CY27 EPS, "in-line with the broader market and a discount to compute semis peers (AMD/AVGO/INTC)". The whole note is Nvidia's Computex keynote, Vera CPU and RTX Spark.

**Insight density.** Useful NVDA insights — 85% GPU share, a $20B standalone CPU guide, and why ASICs may outgrow GPUs — none of which is AVGO analysis.

**Data support.** NVDA bull/base/bear of $330/$288/$160 with a full risk-reward build; AVGO's only numbers are the $481.57 price and a 2024-vintage Overweight rating.

**Event context.** Filed 3 Jun 2026 immediately after NVIDIA's Computex keynote and Taiwan analyst Q&A; a quiet patch for AVGO.

### 2/10 — Citi — *US Semiconductors and Semiconductor Equipment： Summer Sell~off； Fundamentals Intact； Prefer…*
`11 pp · 2026-07-24 · Buy, no PT · $381.92 · upside n/a`

**Why bullish/bearish.** Bullish by name-drop only. Alphabet's raised FY26 capex of $195–205bn, $15bn higher at the midpoint, with FY27 to "increase significantly", is read as positive "specifically for CLS, AVGO, and NVDA in our coverage". No sizing, mechanism or valuation for AVGO.

**Insight density.** Restated sector framing — sell-off versus unchanged estimates, semicap versus semis. AVGO contributes nothing beyond appearing in the capex-spend list.

**Data support.** None on AVGO: no exhibit, model or management quote. Only the companies-mentioned line (AVGO.O, US$392.47, rating 1, 23 Jul 26) plus the standard disclosure block.

**Event context.** Post-sell-off sector check around the late-July hyperscaler capex updates; no AVGO event.

### 1/10 — Morgan Stanley — *摩根士丹利—半导体： 半导体库存追踪——逐比特分析*
`16 pp · 2026-04-18 · OW, no PT · $405.90 · upside n/a`

**Why bullish/bearish.** Bullish by association only. AVGO is named with NVDA and ALAB as the compute/networking exposure MS prefers as trailing-edge capacity tightens and memory costs inflate. No AVGO estimate, target or mechanism of its own appears.

**Insight density.** Proprietary inventory work: customer, distributor and producer DOIs, auto-OEM lean-out, April price hikes. AVGO contributes nothing — it is a name in the recommendation string.

**Data support.** Ten-plus DOI exhibits and q/q, y/y inventory-change tables; coverage page shows AVGO Overweight since 06/09/2024 at $396.72, no target.

**Event context.** Post-4Q reporting inventory update with broadening price hikes; no AVGO print, deal or regulatory trigger in the window.

### 1/10 — Morgan Stanley — *Semiconductor Inventory Tracker： Not Restocking Yet*
`16 pp · 2026-07-01 · OW, no PT · $369.34 · upside n/a`

**Why bullish/bearish.** Bullish by association only. AVGO is grouped with NVDA and CBRS as the compute/networking exposure MS favours where supply/demand is tightening, versus memory and semicap. No AVGO-specific number or argument is offered.

**Insight density.** Real channel work on distributor lean-out and producer builds, but restated consensus for the compute group; AVGO itself is a name, not a datapoint.

**Data support.** Stacked-DOI and inventory-change exhibits; coverage table lists AVGO Overweight (06/09/2024) with price but no target.

**Event context.** Post-1Q inventory refresh with tightening supply but no restocking; nothing AVGO-specific — quiet patch.

---

## Where the houses disagree

> ⚠️ **There is no bear in this book.** All **80** entries that carry a house rating are Buy (36), Overweight (30) or Outperform (14) — not a single Neutral and not a single Sell across the whole AVGO corpus, from October 2025 to September 2026. The only three entries with no rating at all are the three independent `巴芒投研` pre-print aggregators. Whatever the debate is on this name, the sell side is not having it.

> ⚠️ **The current book spans $450 to $580 — a 29% spread on fair value.** HSBC (**$450**, 26 May) and BofA (**$450**, 13 May) at the bottom; J.P. Morgan (**$580**, set 16 Jun and reiterated 27 Jul and 19 Aug) and Bernstein (**$575**, 14 Sep) at the top. At the 15 Sep close of $339.27 those imply **+32.6%** and **+71.0%**. This is not a disagreement about the quarter; it is a disagreement about how much of the custom-ASIC franchise is already in the price.

> ⚠️ **HSBC is the only house to cut, and it cut 16%.** HSBC carried **$535** through November–December 2025 ("potent mix of ASIC and networking upside", "AI narrative and earnings still not fully priced in", both 9/10), then re-based to **$450** on 26 May 2026. Caveat worth knowing: that $450 rides inside a **Marvell** upgrade note (`212451114448851`, scored 3/10) — on AVGO it is a read-across, not a fresh thesis, so the *level* is HSBC's current AVGO view but the *argument* belongs to MRVL.

> ⚠️ **The newest target and the highest target are not the same document.** The most recent AVGO target in the book is Bernstein's **$575**, dated **14 Sep 2026** — but it sits in a 3/10 *sector* note ("Can you put the AI genie back in the bottle?"), a one-line refresh of a number set months earlier. The highest **primary** call is J.P. Morgan's **$580** (`214522118552541`, 8/10, 16 Jun): *"Ignore the Noise — TPU v9 2nm ASIC program on track for CY28 ramp, no delays."*

> ⚠️ **The two biggest single-step raises are both event-driven and both testable.** UBS took **$415 → $472** (+13.7%) on **30 Nov 2025** in its SemiBytes TPU preview, and J.P. Morgan took **$500 → $580** (+16%) on **16 Jun 2026** on the expanded Meta partnership and the TPU v9 program. Every other revision in the book is a nudge.

> ⚠️ **Morgan Stanley publishes most often (7 targets) and moves least.** $443 (8 Dec 2025) → $462 → $485 → **$502**, flat since 4 Jun 2026 through the July drawdown, the June peak and the September slide. It is arguably the cleanest marker of where consensus stopped moving.

> ⚠️ **The upside column is a trap on this name.** Broadcom peaked at **$480.81 on 2 Jun 2026** and closed **$339.27 on 15 Sep 2026**, −29% from the high. So the implied upsides above run from **+4.0%** (J.P. Morgan, $500 against a $480.81 close on 2 Jun) to **+66.8%** (Bernstein, $575 against $344.72 on 14 Sep) — that spread is the *stock's* journey, not the analysts' disagreement. The frozen report-date closes in the DB span **$309.37–$480.81**.

> ⚠️ **Identical ratings hide a 27x–41x multiple debate.** UBS prices the semis segment at ~41x EV/FCF and software at 33x; Goldman normalises to 38x forward EPS with a bull case of **$533** against a bear of **$217**; Bernstein works off ~32x FY27 EPS; Mizuho, at the bottom of the book, uses 22.5x C26E EV/EBITDA. Same "Buy", very different amounts of optimism embedded.

---

## What renders on `/research-lens` — and what does not

The lens reads `price_targets` with `ORDER BY report_date DESC, report_file_id DESC LIMIT 18`, so with **79 AVGO rows only the 18 newest render on the page**. AVGO's 18 run from **2026-09-14 back to 2026-06-04**. All 18 are in the ranked list above and all 18 have digests. The other **65 digests below never show on the page** — they are in `reference/report_digests.json` and in this file, but the page cannot reach them:

- **2026-06-03** — Citi — *Buyers of Pullback; Improved AI Visibility into 2028* (8/10) — *PT $500*
- **2026-06-03** — Goldman Sachs — *Strong AI revenue momentum for 2027， despite modest near~term shortfall relative to…* (8/10) — *PT $525*
- **2026-06-03** — Morgan Stanley — *NVIDIA Corp.（NVDA.US） Computex NVDA keynote & financial analyst Q&A* (2/10) — *rating only*
- **2026-06-02** — J.P. Morgan — *Maintains Lead In AI Networking Silicon； Next~Gen 3nm Tomahawk 6 Strong Ramp 2H26…* (8/10) — *PT $500*
- **2026-06-01** — Morgan Stanley — *Semiconductors Takeaways from our meetings in Taiwan* (6/10) — *rating only*
- **2026-05-31** — Morgan Stanley — *Semiconductors Weekly Earnings Week 7 AVGO Preview* (7/10) — *PT $485*
- **2026-05-26** — HSBC — *Marvell Technology （MRVL.US） Upgrade to Buy： Ready to ride the AI~networking super~cycle* (3/10) — *PT $450*
- **2026-05-23** — J.P. Morgan — *摩根大通-半导体设备-TMC会议总结： 第一季度业绩后动能持续-AI推理拐点、广泛周期性复苏、稳健内存上行周期、WFE周期拉长， 维持超配该板块* (2/10) — *rating only*
- **2026-05-20** — Bernstein — *US Industrials & Tech： The Data Center Project Pipeline ~ Capacity， Construction &…* (3/10) — *PT $525*
- **2026-05-19** — Goldman Sachs — *1Q Preview： Expect strong guidance， with focus on FY27 AI revenue and XPU customer…* (7/10) — *PT $500*
- **2026-05-18** — UBS — *FQ2-26 (Apr) Preview-Raising PT, Adjusting Estimates* (9/10) — *PT $490*
- **2026-05-13** — BofA — *US Semiconductors-AI 2030-Stronger for longer for compute, memory, networking* (6/10) — *PT $450*
- **2026-05-12** — Citi — *Preview – Raising TP to $500； Maintain Buy* (9/10) — *PT $500*
- **2026-05-12** — Bernstein — *U.S. Semiconductors and Semiconductor Capital Equipment U.S. Semiconductors： Deconstructing…* (4/10) — *PT $525*
- **2026-05-11** — Bernstein — *Global Semiconductors and Semiconductor Capital Equipment~ What to make of an earnings…* (4/10) — *PT $525*
- **2026-05-05** — UBS — *GlobalFoundries Inc（GFS.US） 1Q 2Q A Little Ahead Before Thursday's Analyst Day* (3/10) — *rating only*
- **2026-05-05** — Goldman Sachs — *Advanced Micro Devices Inc. (AMD)-Upgrade to Buy as Agentic AI drives server CPU tailwinds…* (2/10) — *rating only*
- **2026-04-30** — Bernstein — *Qualcomm Inc（QCOM.US）： FQ226 recap~We hope they put on a good show in June...* (5/10) — *PT $525*
- **2026-04-27** — BofA — *NVIDIA Corporation（NVDA.OQ） Back to Basics： Boosting cash returns could be another rerating…* (4/10) — *rating only*
- **2026-04-27** — J.P. Morgan — *Semiconductors CY26 Data Center Capex Revised Higher and Strong Initial Growth Outlook of…* (4/10) — *rating only*
- **2026-04-27** — Morgan Stanley — *Global Technology Asia Pacific Global Technology 2026 Outlook – A Tale of Two Halves* (3/10) — *rating only*
- **2026-04-22** — UBS — *Thoughts On Google’s TPU v8 Generation* (7/10) — *PT $475*
- **2026-04-18** — Morgan Stanley — *摩根士丹利—半导体： 半导体库存追踪——逐比特分析* (1/10) — *rating only*
- **2026-04-17** — J.P. Morgan — *Semiconductors Semi Cap Equipment： 1Q26 Preview： Sustained AI Demand， Broadening Cyclical…* (5/10) — *rating only*
- **2026-04-16** — UBS — *Equity Strategy： The Theme~ometer： AI Chips and Memory， Still Attractive* (3/10) — *rating only*
- **2026-04-15** — J.P. Morgan — *Expanded Meta Partnership Drives Confidence In A Strong Multi~Year Revenue Ramp； Adds To…* (8/10) — *PT $500*
- **2026-04-15** — Bernstein — *Many major multi Meta MTIA...* (7/10) — *PT $525*
- **2026-04-14** — Goldman Sachs — *Partnership with Meta further reinforces Broadcom’s technology advantage in custom silicon…* (8/10) — *PT $480*
- **2026-04-13** — UBS — *Increasing 2027 TPU Units Once Again* (9/10) — *PT $475*
- **2026-04-09** — J.P. Morgan — *TSMC CoWoS and advanced back-end updates* (6/10) — *rating only*
- **2026-04-08** — J.P. Morgan — *TSMC（2330.TW） CoWoS and advanced back~end updates* (6/10) — *rating only*
- **2026-03-23** — Bernstein — *U.S. Semiconductors and Semiconductor Capital Equipment Bernstein Semi Cycle Tearsheet： Too…* (6/10) — *PT $525*
- **2026-03-22** — UBS — *US Semiconductors： Stellar Optics and Fast~Paced Networking at OFC 2026* (7/10) — *rating only*
- **2026-03-19** — J.P. Morgan — *Semiconductors： OFC Conference： Strong CY26~CY27 Optical Networking Setup， High Innovation，…* (7/10) — *PT $500*
- **2026-03-09** — BofA — *US Semiconductors Scaling AI with Photons-Primer on Optical Interconnects* (7/10) — *PT $450*
- **2026-03-06** — UBS — *Global I O Smartphones： January ’26 Sell~Through： China impacted by base effect， but…* (3/10) — *rating only*
- **2026-03-05** — UBS — *Strong Results & Guidance； Raise Estimates， Maintain $475 PT* (9/10) — *PT $475*
- **2026-03-05** — Bernstein — *FQ126 recap~Line 'em up and knock 'em down...* (8/10) — *PT $525*
- **2026-03-04** — Goldman Sachs — *Very strong guidance and commentary on key debates should drive stock higher - Buy* (8/10) — *PT $480*
- **2026-03-04** — Bernstein — *Asia Tech Hardware： Future of Tech~Mapping the CPO value chain* (4/10) — *PT $475*
- **2026-03-03** — B&M (巴芒投研, independent) — *财报前瞻* (2/10) — *no PT row*
- **2026-02-23** — UBS — *Thinking Through SOTP Amid Software Deep Dive + EPS Preview* (8/10) — *PT $475*
- **2026-02-19** — Goldman Sachs — *1Q Preview： Expect a solid quarter， with continued AI momentum* (7/10) — *PT $450*
- **2026-02-10** — UBS — *Increasing Estimates On TPU Unit Inflection； C2027E EPS -$18* (9/10) — *PT $475*
- **2026-02-03** — Morgan Stanley — *AVGO FAQ： What will it take for the stock to outperform？* (9/10) — *PT $462*
- **2026-01-25** — J.P. Morgan — *Google TPU Outlook Getting Stronger FY26 And FY27； 18 Month Lead Implies Shrinking…* (9/10) — *PT $475*
- **2026-01-20** — Goldman Sachs — *AMERICAS TECHNOLOGY AI Unit Economics： GPUs vs. ASICs and the inference cost curve~Buy AVGO…* (8/10) — *PT $450*
- **2026-01-09** — Bernstein — *Vegas baby...Takeaways from a CES investor meeting with the Semiconductor Solutions Group…* (8/10) — *PT $475*
- **2025-12-16** — J.P. Morgan — *Semiconductors Semi Cap Equipment： 2026 Outlook： Expect Another Year Of Stock…* (8/10) — *rating only*
- **2025-12-15** — UBS — *CEO CFO Meeting Suggests Friday's Move Is a Buying Opportunity* (8/10) — *PT $475*
- **2025-12-12** — Bernstein — *FQ425 recap~The fickle heart's desire...* (8/10) — *PT $475*
- **2025-12-12** — Morgan Stanley — *AI acceleration into 2026* (8/10) — *PT $462*
- **2025-12-11** — Goldman Sachs — *Very strong quarter and AI customer traction， tempered by lack of guide~up for FY26* (8/10) — *PT $450*
- **2025-12-08** — HSBC — *Buy： AI narrative and earnings still not fully priced in* (9/10) — *PT $535*
- **2025-12-08** — Morgan Stanley — *Semiconductors： Weekly： Expect a strong AVGO outlook* (6/10) — *PT $443*
- **2025-12-07** — B&M (巴芒投研, independent) — *财报前瞻* (6/10) — *no PT row*
- **2025-11-30** — UBS — *US Semiconductors and Semi Equipment： SemiBytes： Thoughts on TPU and AVGO Preview，…* (9/10) — *PT $472*
- **2025-11-25** — Goldman Sachs — *4Q Preview： Expect solid quarter with strong momentum driving upside to AI revenue in 2026* (7/10) — *PT $435*
- **2025-11-25** — BofA — *US Semiconductors TPU intensifies competitive race, but in a rising tide, Buy NVDA, AVGO…* (6/10) — *PT $400*
- **2025-11-24** — HSBC — *Buy： Potent mix of ASIC and networking upside* (9/10) — *PT $535*
- **2025-10-20** — UBS — *US Semiconductors and Semi Equipment： SemiBytes， AVGO Tweaks， TSMC Capex， US China Update* (9/10) — *PT $415*
- **2025-10-14** — UBS — *Updating Model after a Series of Supply Chain Checks And New Details on OpenAI Partnership.…* (9/10) — *PT $415*
- **2025-10-13** — Goldman Sachs — *Partnership with OpenAI reinforces Broadcom’s technology advantage in custom silicon* (7/10) — *PT $380*
- **2025-09-03** — B&M (巴芒投研, independent) — *公司财报前瞻分析* (5/10) — *no PT row*
- **2025-05-16** — Mizuho — *MizuhoSecuritiesUSALLC_AIServerSupplyChainCall-UpsidetoAVGO, SomeChallengesWithPeers-AdjPTs* (8/10) — *PT $250*

---

## How the data is stored (as of 2026-09-15)

**Two databases, one join key.** The Research Lens page reads from both.

### 1. `db/zsxq.db` — the PDF library

One row per downloaded PDF in **`pdf_files`** (`file_id` primary key, `name`, `topic_title`, `summary`, `local_path`, `bank`, `page_count`, `tickers`, `claude_rating`, `ocr_text`, `create_time`), plus the FTS5 trigram index that this scan ran against. The DB stores only the pointer to the bytes — the PDFs live under `/Users/x/Downloads/zsxq_reports/<YYYY_MM_DD>/`. **Two AVGO candidates have no bytes on disk** and so could not be read: `812458524245552` (UBS *SemiBytes*, ISM PMI/AVGO note, dated 2026-05-04) and `814885554885252` (UBS *SemiBytes, AVGO Preview* — financing, NVDA vertical integration, Terafab, 2026-08-24). Both are UBS, and the second one is exactly the report that would have explained why UBS's last readable target is 18 May; their price targets are therefore **not** in the book.

### 2. `db/stock_price_target.db` — the calls

One row in **`price_targets`** per **(ticker × broker × report)** — AVGO now has **79 rows** (was 15 at the start of this session: the run reported 64 inserted and 16 refreshed from the full-PDF read, 0 errors). Columns: `company_ticker`, `company_name`, `research_institute`, `rating`, `price_target`, `target_currency`, `catalyst`, `report_file_id` (join key to `pdf_files.file_id`), `report_pdf_filename`, `report_url`, `report_date`, **`report_date_price`** (the frozen point-in-time close), `report_date_market_cap`, `price_currency`, `upside_pct`, `created_at`.

Two unique keys guard against duplicates: `UNIQUE(company_ticker, research_institute, report_file_id)` and `uq_ticker_broker_date (ticker, broker, report_date)`. This run hit **no** date collisions on AVGO (unlike META, which lost a note to a same-day sibling) — every one of the 79 rows is a distinct broker-date.

Writes go **only** through `scripts/persist_pts.py` → `stock_price_target_db.upsert_target()` (`--replace` used here, because a full-PDF read outranks a summary-only row); extraction rules live in `reference/pt_extraction.md`. **This DB matches `.gitignore`'s `*.db` and is not committed** — tonight's 79-row update exists on this machine only.

### 3. Per-report digests → `reference/report_digests.json`

Keyed by **stringified `file_id`**, one object per report with exactly `score`, `why`, `insight`, `data`, `event`. Loaded by `zsxq_viewer._report_digests()` (mtime-cached) and attached to each report in `_research_lens_reports()`. The file now holds **156 entries** — the AVGO merge added **82** and updated **1** on top of the 74 pre-existing keys (GEV, META and earlier lenses), and the merge preserved every pre-existing key (backup at `reference/report_digests.json.bak-20260915T214024Z`). `db/stock_price_target.db` is gitignored, but this JSON is tracked, so the prose *is* versioned.

One caveat worth knowing: the registry is keyed by `file_id` alone, **not by ticker**. `585424811815484` (Bernstein's *Data Center Project Pipeline*, April '26) carries price targets for both AVGO and META, so its digest had to be written as a **combined AVGO+META entry** (score 3) to stop one lens page showing the other ticker's text.

### 4. What is *not* stored — the price series

Daily OHLC is never persisted. The lens pulls the daily series **live from yfinance** on each page load for the window (earliest `report_date` − 14 days … latest + 14 days). Only the close **on** the report date is frozen into the row (`report_date_price`), which is what makes every `upside_pct` above auditable months later. The chart is therefore only as good as yfinance on the day you open it.

---

## Method notes and known gaps

- **One non-broker source is in the list but not in the DB.** Three `B&M (巴芒投研)` pre-print pieces (`415825112552188` 6/10, `212515215481551` 5/10, `585552248512424` 2/10) are independent Chinese-language aggregators with no research house behind them. They carry no rating, no target and no `bank` field, so `persist_pts.py` cannot file them; they are scored and read here, and nothing is persisted.
- **Mizuho is excluded from the DB on purpose.** `214884222148151` (*AI Server Supply Chain Call — Upside to AVGO*, 9 pp, **Outperform, $250** vs a $232.64 close) is a genuine 8/10 call dated **2025-05-16**. Its filename carries no `-YYMMDD` suffix, so `persist_pts.py` resolves its report date from the zsxq `create_time` and would stamp it 2026-09-13 — turning a +7.5% call into a fake −28%. Rather than write a knowingly mis-dated row, it is scored and listed here with its true date and price, and left out of `price_targets`.
- **Four file_ids were dropped as duplicates** (no row, no digest entry): `812241481112182` (Chinese translation of UBS `812241252442142`), `812215841544152` (translation of Morgan Stanley `184482518211182`), `585425822812214` (byte-identical BofA twin of `415245581284888`, true date 2026-05-13) and `412424445241228` (the same Morgan Stanley inventory tracker as `412424414544448`).
- **A pre-OCR re-triage recovered 9 reports.** 14 candidates were first triaged "unreadable" because the PDFs were image-only; once Apple-Vision OCR text existed for all 14, a second pass promoted 9 of them to real AVGO calls (and confirmed 5 as mentions-only, dropped).
- **Rating vocabulary:** the book uses Buy (36), Overweight (30) and Outperform (14); no house in the corpus carries a Neutral or Sell on AVGO.

---

*All 85 readable AVGO PDFs were read in full, ~33 of them after OCR because the source files were image-only. Every rating, price target, report-date price and page count above was regenerated directly from `price_targets` and `pdf_files`; the two missing UBS files and the four duplicates are the only candidates not represented.*
