# Meta Platforms (META) — zsxq Research Lens Reading List

**Generated:** 2026-09-15 · **Ticker:** META (Meta Platforms) · **Lens:** http://localhost:5001/zsxq/research-lens?ticker=META

**Sources:** `db/stock_price_target.db` → table `price_targets` (50 META rows, one per ticker × broker × report — 49 with a frozen report-date close) joined to `db/zsxq.db` → table `pdf_files` (the PDFs themselves, on disk under `/Users/x/Downloads/zsxq_reports/`).

**Scan method:** trigram full-text search of the 13,515-row zsxq PDF library for `META` / `Meta Platforms` (`lens_scan.py META --name "Meta Platforms" --limit 120 --summary-chars 1500`) → **126 candidates** → **57 carry a real META call** (a rating or a price target on the ticker) and were read in full from their local PDFs. The other 69 are comp-table rows, sector notes that mention Meta without a call, read-across notes about other companies, or one mis-filed currency note. Of the 57: **50 carry a price target** that is now persisted, 7 do not (five Morgan Stanley flow weeklies, one Morgan Stanley capacity note with no PT printed, and the corrupt Bernstein file below).

**Feed shape:** an unusually *long* but unusually *shallow* set. 49 of the 50 persisted calls are positive — 21 rate 8/10 or better, and there is not a single Sell or Underweight in the book; the only Neutral (J.P. Morgan, 12 Jul 2026) lasted two months before the 10 Sep upgrade. But only **39 of 57** reports actually argue a META case; **18** merely cite the name — mostly Morgan Stanley's *Where Are We Trading Now* weeklies and sector notes where Meta is a row or a paragraph. The list below is ordered by how much you learn about Meta per minute of reading, not by how strongly the house rates it.

---

## How to read the score

| Score | Meaning |
|---|---|
| **8–10** | Primary META work: proprietary data or a quantified argument about Meta itself. Read it. |
| **6–7** | Real META content (a full page, a channel check, an SOTP) inside a report about something else, or a short but genuinely fresh META read. Worth the time. |
| **4–5** | A few sharp META datapoints — a capacity figure, an ad-load number — but Meta is a comp row. Skim that section only. |
| **0–3** | Meta is a name in a table or a line on a chart. The report may be excellent; it is not META research. Skip unless you want the theme. |

The score weights four things: (1) **is there a META thesis at all** — rating + why, or just a row in a valuation table; (2) **insight density** — proprietary/channel data vs restated consensus; (3) **data support** — exhibits, models, SOTP builds, verbatim management quotes; (4) **event context** — was it written around a print, a deal or a regulatory trigger (a dated, testable call) or in a quiet patch. Length earns nothing: the 71-pp Morgan Stanley ownership study scores 3, the 10-pp Goldman settlement note scores 8.

---

## Ranked list

| Score | Report | Pp · Date | META stance & PT | Price on date → upside | Open |
|---|---|---|---|---|---|
| **10/10** | **Morgan Stanley** — *4 products to turn Meta back into an AI winner* | 21 · 26-06-02 | OW, PT **$775** | $597.08 → **+29.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184152881185882/Morgan%20Stanley-Meta%20Platforms%20Inc%20%EF%BC%88META.US%EF%BC%894%20Products%20to%20Turn%20Meta%20Back%20into%20an%20%22AI%20Winner%22-260602.pdf) |
| **9/10** | **J.P. Morgan** — *The models and agents are here — upgrading to Overweight, $820 PT* | 23 · 26-09-10 | OW, PT **$820** | $644.38 → **+27.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412882548858148/J.P.%20Morgan-Meta%20Platforms%20Inc%EF%BC%88META.US%EF%BC%89The%20Models%20and%20Agents%20are%20Here%EF%BC%9B%20Upgrading%20to%20Overweight%EF%BC%8C%20%24820%20PT-260910.pdf) |
| **9/10** | **Bernstein** — *US Internet mega 1Q26 earnings: more similar than different* | 29 · 26-04-30 | OP, PT **$850** | $611.34 → **+39.0%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585585554848484/Bernstein-US%20Internet%20mega%201Q26%20earnings%20More%20similar%20than%20different-260430.pdf) |
| **9/10** | **Bernstein** — *Investment memo: pumping AI iron* | 21 · 26-01-27 | OP, PT **$870** | $671.77 → **+29.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585524122548114/Bernstein-Meta%20Investment%20Memo-Pumping%20AI%20Iron-260127.pdf) |
| **9/10** | **Morgan Stanley** — *3 catalysts to outperformance and the bull case in '26* | 18 · 25-12-11 | OW, PT **$750** | $651.02 → **+15.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812844241442842/Morgan%20Stanley-Meta%20Platforms%20Inc%20%EF%BC%88META.US%EF%BC%893%20Catalysts%20to%20Outperformance%20and%20the%20Bull%20Case%20in%20%2726-251211.pdf) |
| **8/10** | **Goldman Sachs** — *Q2'26 review: near-term ROIC evidence, long-term compute-spend visibility missing* | 10 · 27-07-30 | Buy, PT **$725** | report-date price n/a | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814512485518222/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%28META%29%20Q2%E2%80%9926%20Review-Core%20Business%20Provides%20Evidence%20of%20Near-Term%20ROIC%20but%20Lack%20of%20Visibility%20into%20Long-Term%20Compute%20Spend%20Persists-270730.pdf) |
| **8/10** | **Goldman Sachs** — *Social-media lawsuit overhang reduced with settlement* | 12 · 26-08-26 | Buy, PT **$725** | $576.14 → **+25.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814885454888182/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%EF%BC%88META.US%EF%BC%89%20Social%20Media%20Lawsuit%20Overhang%20Reduced%20With%20Settlement%EF%BC%9B%20Compelling%20Risk%20Reward%20with%20Focused%20on%20Increased%20AI%20Clarity%20in%20Coming%20Months-260826.pdf) |
| **8/10** | **Morgan Stanley** — *North America core strong now; more call options soon* | 16 · 26-07-30 | OW, PT **$775** | $539.03 → **+43.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214512485518521/Morgan%20Stanley-Meta%20Platforms%20Inc%20-%20North%20America%20Core%20Strong%20Now%3B%20More%20Call%20Options%20%22Soon%22-260730.pdf) |
| **8/10** | **Deutsche Bank** — *Meta ambitions need Meta scale* | 18 · 26-07-24 | Buy, PT **$800** | $595.19 → **+34.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/181285882225212/Deutsche%20Bank-Meta%EF%BC%88META.US%EF%BC%89Meta%20Ambitions%20Need%20Meta%20Scale-260724.pdf) |
| **8/10** | **Morgan Stanley** — *5 takes on the neocloud vs hyperscaler opportunity* | 16 · 26-07-01 | OW, PT **$775** | $612.91 → **+26.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412424458858248/Morgan%20Stanley-Meta%20Platforms%20Inc%20-%20North%20America%205%20Takes%20On%20The%20Neocloud%20vs%20Hyperscaler%20Opportunities-260701.pdf) |
| **8/10** | **Morgan Stanley** — *Headcount reductions and the neocloud backup optionality* | 17 · 26-05-17 | OW, PT **$775** | $613.66 → **+26.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812454818812842/Morgan%20Stanley-Meta%20Platforms%20Inc%20%EF%BC%88META.US%EF%BC%89Headcount%20Reductions%20and%20the%20Neocloud%20Backup%20Optionality-260517.pdf) |
| **8/10** | **Morgan Stanley** — *Internet 1Q26: GOOGL, AMZN and META surprises and learnings* | 39 · 26-04-30 | OW, PT **$775** | $611.34 → **+26.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184484441818142/MS-Internet%20North%20America%20GOOGL%2C%20AMZN%2C%20and%20META%20Surprises%20and%20Learnings-260430.pdf) |
| **8/10** | **UBS** — *Product development benefits still ahead of us* | 20 · 26-04-30 | Buy, PT **$865** | $611.34 → **+41.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415515525514288/UBS-Meta%20Platforms%EF%BC%88META.US%EF%BC%89Product%20Development%20Benefits%20Still%20Ahead%20of%20Us-260430.pdf) |
| **8/10** | **Bernstein** — *Digital ads 1Q26: it's good to be big, right?* | 37 · 26-04-27 | OP, PT **$900** | $677.99 → **+32.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585585212452214/Bernstein-U.S.%20Internet%EF%BC%9ADigital%20Ads%201Q26%EF%BC%9A%20It%27s%20good%20to%20be%20big%EF%BC%8C%20right%EF%BC%9F-260427.pdf) |
| **8/10** | **Deutsche Bank** — *Early sparks of Meta superintelligence (translated note)* | 17 · 26-04-18 | Buy, PT **$920** | $687.91 → **+33.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212215841851281/%E4%B8%AD%E6%96%87%E7%89%88-%E5%BE%B7%E6%84%8F%E5%BF%97%E9%93%B6%E8%A1%8C%E2%80%94Meta%E2%80%94Meta%E8%B6%85%E7%BA%A7%E6%99%BA%E8%83%BD%E7%9A%84%E6%97%A9%E6%9C%9F%E7%81%AB%E8%8A%B1-%E8%AF%91%E6%96%87.pdf) |
| **8/10** | **Morgan Stanley** — *Key themes and numbers into GOOGL/META/AMZN earnings* | 37 · 26-04-14 | OW, PT **$775** | $661.88 → **+17.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812241152554422/Morgan%20Stanley-Key%20Themes%20and%20Numbers%20into%20GOOG%20META%20AMZN%20Earnings-260414.pdf) |
| **8/10** | **Morgan Stanley** — *Meet Meta's Muse* | 14 · 26-04-09 | OW, PT **$775** | $627.81 → **+23.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585544818582814/Morgan%20Stanley-Meta%20Platforms%20Inc%EF%BC%88META.US%EF%BC%89Meet%20Meta%E2%80%99s%20Muse-260409.pdf) |
| **8/10** | **Goldman Sachs** — *Framing recent news reports against our strategic-focus view* | 14 · 26-03-22 | Buy, PT **$835** | $593.11 → **+40.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585554125282254/GS-Meta%20Platforms%20Inc.%20%28META%29%20Framing%20Recent%20News%20Reports%20Against%20Our%20View%20of%20Strategic%20Focus%20Areas-260322.pdf) |
| **8/10** | **Goldman Sachs** — *Q4'25 review: AI impact in the core, investments still scaling* | 10 · 26-01-29 | Buy, PT **$835** | $737.00 → **+13.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184421485882582/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%EF%BC%88META.US%EF%BC%89%20Q4%E2%80%9925%20Review%EF%BC%9A%20Demonstrating%20the%20Impact%20of%20AI%20in%20the%20Core%20Operations%20while%20Continuing%20to%20Scale%20Investments-260129.pdf) |
| **8/10** | **UBS** — *Stronger signals of AI benefits to emerge in 2026* | 21 · 26-01-29 | Buy, PT **$872** | $737.00 → **+18.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415542518118428/UBS-Meta%20Platforms%EF%BC%88META.US%EF%BC%89Stronger%20Signals%20of%20AI%20Benefits%20to%20Emerge%20in%202026-260129.pdf) |
| **8/10** | **Citi** — *IG/Reels ad-load tracker: 3Q reaches 27.1%, +230bp q/q* | 31 · 25-10-13 | Buy, PT **$915** | $713.84 → **+28.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212851582885211/CITI-Meta%20Platforms%20Inc%20%EF%BC%88META.US%EF%BC%89%20IG%20SR%20Tracking%20Suggests%203Q%20Ad%20Load%20Reaches%2027.1%25%EF%BC%8C%20%2B230bp%20Q%20Q%EF%BC%8C%20as%20Engagement%20Expands%20%26%20Online%20Adv.%20Trends%20Remain%20Healthy-251013.pdf) |
| **7/10** | **Morgan Stanley** — *Muse has arrived: what matters next* | 15 · 26-09-09 | OW, PT **$775** | $653.69 → **+18.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584115845522224/Morgan%20Stanley-Meta%20Platforms%20Inc%20Muse%20Has%20Arrived%20What%20Matters%20Next-260909.pdf) |
| **7/10** | **Bernstein** — *Digital ads in 2Q26: AI benefits accrue elsewhere* | 36 · 26-08-20 | OP, PT **$800** | $545.83 → **+46.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/181528411415422/Bernstein-U.S.%20Internet%EF%BC%9ADigital%20Ads%20in%202Q26%EF%BC%9A%20AI%20benefits%20accrue%20elsewhere-260820.pdf) |
| **7/10** | **Bernstein** — *Meta 2Q26: avoiding TikTok 2.0* | 25 · 26-07-29 | OP, PT **$800** | $585.61 → **+36.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814512485518552/Bernstein-Meta%20Platforms%20Inc.%EF%BC%88META.US%EF%BC%89Meta%202Q26%EF%BC%9A%20Avoiding%20TikTok%202.0-260729.pdf) |
| **7/10** | **Jefferies** — *Vision Mini dive: when AI moves to the face* | 39 · 26-07-20 | Buy, PT **$825** | $645.85 → **+27.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584281284811824/Jefferies-Meta%20Platforms%EF%BC%88META.US%EF%BC%89Vision%20Mini%20Dive%EF%BC%9A%20When%20AI%20Moves%20to%20the%20Face-260720.pdf) |
| **7/10** | **Deutsche Bank** — *A silver lining* | 13 · 26-07-01 | Buy, PT **$810** | $612.91 → **+32.2%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214545515812141/Deutsche%20Bank-Meta%EF%BC%88META.US%EF%BC%89A%20Silver~Lining-260701.pdf) |
| **7/10** | **Deutsche Bank** — *Subscription rollout creates the first clear consumer-AI monetization layer* | 14 · 26-05-28 | Buy, PT **$810** | $634.70 → **+27.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585412255148214/Deutsche%20Bank-Meta%EF%BC%88META.US%EF%BC%89Subscription%20Rollout%20Creates%20First%20Clear%20Consumer%20AI%20Monetization%20Layer-260528.pdf) |
| **7/10** | **Goldman Sachs** — *Q1'26 review: core outgrows the industry, long-term AI visibility needed* | 10 · 26-04-30 | Buy, PT **$830** | $611.34 → **+35.8%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812212242215182/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%EF%BC%88META.US%EF%BC%89%20Q1%E2%80%9926%20Review%EF%BC%9A%20Core%20Business%20Continues%20to%20Outgrow%20Industry%EF%BC%9B%20Visibility%20Into%20Long~Term%20AI%20Strategy%20Needed%20for%20Investor%20Sentiment-260430.pdf) |
| **7/10** | **BofA** — *1Q26 preview: expecting a beat, macro sensitivity and AI cost benefits* | 18 · 26-04-20 | Buy, PT **$820** | $670.29 → **+22.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585582845254554/BofA%20Securities-Meta%20Platforms%20Inc%EF%BC%88META.OQ%EF%BC%891Q%20preview%EF%BC%9A%20Expecting%20a%20beat%EF%BC%8C%20macro%20sensitivity%20%26%20AI%20costs%20benefits%20in%20focus-260420.pdf) |
| **7/10** | **Bernstein** — *Will Muse Spark restore investor belief in the AI story?* | 27 · 26-04-08 | OP, PT **$900** | $611.85 → **+47.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812244181215242/Bernstein-Meta%20Platforms%20Inc.%EF%BC%88META.US%EF%BC%89Meta%EF%BC%9A%20Will%20this%20Muse%20Spark%20investor%20belief%20in%20their%20AI%20story%EF%BC%9F-260408.pdf) |
| **7/10** | **J.P. Morgan** — *Major AI acceleration — revenue and expense acceleration* | 19 · 26-01-29 | OW, PT **$825** | $737.00 → **+11.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415542254244488/J.P.%20Morgan-Meta%20Platforms%20Inc%EF%BC%88META.US%EF%BC%89Major%20AI%20Acceleration%EF%BC%8C%20Revenue%20Acceleration%EF%BC%8C%20and%20Expense%20Acceleration-260129.pdf) |
| **7/10** | **Citi** — *1st impression: ad revenue +23% y/y ex-FX; '26 capex higher than expected* | 12 · 26-01-28 | Buy, PT **$850** | $667.54 → **+27.3%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812254845242142/Citi-Meta%20Platforms%20Inc%20%28META.O%29%201st%20Impression-Ad%20Revs%20%2B23%25%20Y-Y%20ex-FX%20on%20Holiday%20Strength%20%26%201Q%20Guidance%20Better%3B%20%E2%80%9926%20CapEx%20%26%20Expenses%20Higher%20Than%20Expected-260128.pdf) |
| **7/10** | **Goldman Sachs** — *Q3'25 review: strong Family-of-Apps, investment commentary overhangs* | 9 · 25-10-30 | Buy, PT **$815** | $664.74 → **+22.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212881221142241/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%EF%BC%88META.US%EF%BC%89%20Q3%E2%80%9925%20Review%EF%BC%9A%20Strong%20Family%20of%20Apps%20Operating%20Performance%EF%BC%9B%20Investment%20Commentary%20Overhangs%20the%20Stock-251030.pdf) |
| **6/10** | **Goldman Sachs** — *The introduction of Muse AI* | 10 · 26-09-13 | Buy, PT **$725** | $648.03 → **+11.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814822528124822/Goldman%20Sachs-Meta%20Platforms%20Inc.%20%28META%29%20The%20Introduction%20of%20Muse%20AI-260913.pdf) |
| **6/10** | **Bernstein** — *All in all just another settlement in the Internet regulatory wall* | 17 · 26-08-27 | OP, PT **$800** | $571.10 → **+40.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412884214485118/Bernstein-US%20Internet%EF%BC%9A%20All%20in%20all%20just%20another%20settlement%20in%20the%20Internet%20regulatory%20wall-260827.pdf) |
| **6/10** | **J.P. Morgan** — *AI outlook flips as Muse Spark 1.1 advances; incrementally positive but stay Neutral* | n/a · 26-07-12 | Neutral, PT **$725** | $669.21 → **+8.3%** | — *(no PDF)* |
| **6/10** | **Morgan Stanley** — *How much capacity will $2tn of hyperscaler capex bring by '27?* | 58 · 26-05-17 | OW, PT $775 — **not persisted**, `(META, MS, 2026-05-17)` clash | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424181184514/Morgan%20Stanley-How%20Much%20Capacity%20Will%20%242%20Trillion%20of%20Hyperscaler%20Capex%20Bring%20By%20%E2%80%9927%EF%BC%9F-260517.pdf) |
| **6/10** | **UBS** — *US Internet 1Q26 online-advertising preview: navigating the air pocket* | 65 · 26-04-21 | Buy, PT **$908** | $668.22 → **+35.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585582851255514/UBS-US%20Internet%201Q26%20Online%20Advertising%20Preview%EF%BC%9A%20Navigating%20the%20Air%20Pocket-260421.pdf) |
| **6/10** | **Morgan Stanley** — *AI efficiency winds starting to pick up* | 10 · 26-03-15 | OW, PT **$825** | $612.62 → **+34.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/184444528445552/Morgan%20Stanley-META%EF%BC%9A%20AI%20Efficiency%20Winds%20Starting%20to%20Pick%20Up-260315.pdf) |
| **5/10** | **Morgan Stanley** — *How could open-weight models impact GenAI ROIC?* | 18 · 26-08-12 | OW, PT **$775** | $578.85 → **+33.9%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412411184581448/Morgan%20Stanley-Internet%EF%BC%9AHow%20Could%20Open~Weight%20Models%20Impact%20GenAI%20ROIC%EF%BC%9F-260812.pdf) |
| **5/10** | **Bernstein** — *Meta's will-they-won't-they neocloud ambitions* | 15 · 26-07-01 | OP, PT **$850** | $612.91 → **+38.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814545528828442/Bernstein-Meta%27s%20will%20they-won%27t%20they%20neocloud%20ambitions%20%28situationships%20don%27t%20usually%20end%20well%29-260701.pdf) |
| **5/10** | **UBS** — *Does the excess-capacity sale reduce EPS-compression risk?* | 13 · 26-07-01 | Buy, PT **$865** | $612.91 → **+41.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584242251151554/UBS-Meta%20Platforms%20Does%20Excess%20Capacity%20Sale%20Reduce%20EPS%20Compression%20Risk--260701.pdf) |
| **5/10** | **HSBC** — *AI-driven revenue growth can continue* | 9 · 26-04-21 | Buy, PT **$905** | $668.22 → **+35.4%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585581115424244/HSBC-Meta%20Platforms%20%EF%BC%88META.US%EF%BC%89Buy%EF%BC%9A%20AI~driven%20revenue%20growth%20can%20continue-260421.pdf) |
| **5/10** | **Bernstein** — *The world's first AI-oriented organization* | 17 · 26-03-16 | OP, PT **$900** | $626.87 → **+43.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415555881424548/Bernstein-U.S.%20Internet%20Meta-The%20world%27s%20first%20AI-oriented%20organization--260316.pdf) |
| **5/10** | **HSBC** — *Fast-growing ad revenue boosted by AI* | 8 · 25-10-21 | Buy, PT **$905** | $731.37 → **+23.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415882825512488/HSBC-Meta%20Platforms%20%EF%BC%88META.US%EF%BC%89Buy%EF%BC%9AFast%20growing%20ad%20revenue%20boosted%20by%20AI-251021.pdf) |
| **5/10** | **J.P. Morgan** — *Glasses move a step closer to the next form factor of computing* | 17 · 25-09-18 | OW, PT **$875** | $777.70 → **+12.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812858822455242/J.P.%20Morgan-Meta%20Platforms%20Inc%EF%BC%88META.US%EF%BC%89Glasses%20Move%20a%20Step%20Closer%20to%20the%20Next%20Form%20Factor%20of%20Computing%EF%BC%9B%20Reiterate%20Overweight%20%26%20%24875%20PT-250918.pdf) |
| **4/10** | **Morgan Stanley** — *Where are we trading now: Micro vs AI vs Macro* | 16 · 26-07-28 | no PT — comp-sheet row, no rating or target in the body | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/214512248122521/Morgan%20Stanley-Internet%EF%BC%9AWhere%20Are%20We%20Trading%20Now%EF%BC%9AMicro%20vs%20AI%20vs%20Macro-260728.pdf) |
| **4/10** | **Bernstein** — *Data-center project pipeline (April '26): capacity, construction, cancellations* | 41 · 26-05-20 | OP, PT **$850** | $604.50 → **+40.6%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424811815484/Bernstein-US%20Industrials%20%26%20Tech%EF%BC%9A%20The%20Data%20Center%20Project%20Pipeline%20~%20Capacity%EF%BC%8C%20Construction%20%26%20Cancellations%20%EF%BC%88April%20%2726%EF%BC%89-260520.pdf) |
| **3/10** | **Morgan Stanley** — *How much revenue per GW could the capacity ahead generate?* | 21 · 26-05-27 | OW, PT **$775** | $634.67 → **+22.1%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/812485554284452/Morgan%20Stanley-Internet%EF%BC%9AHow%20Much%20Revenue%20per%20GW%20Could%20Be%20Generated%20with%20the%20Capacity%20Ahead%EF%BC%9F-260527.pdf) |
| **3/10** | **Morgan Stanley** — *Large-cap institutional ownership 1Q26: under-ownership narrows* | 71 · 26-05-19 | OW, PT **$775** | $602.05 → **+28.7%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424552455544/MS-US%20Technology%20%20Large-Cap%20Institutional%20Ownership%201Q26%20Mega-Cap%20Tech%20Under-Ownership%20Narrows-260519.pdf) |
| **3/10** | **Morgan Stanley** — *What does ChatGPT's agentic pivot mean for the ecosystem?* | 25 · 26-03-12 | OW, PT **$825** | $637.04 → **+29.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/212228411484441/Morgan%20Stanley-What%20Does%20ChatGPT%27s%20Agentic%20Pivot%20Mean%20for%20the%20Ecosystem%EF%BC%9F-260312.pdf) |
| **3/10** | **Bernstein** — *US Internet: AI bear narratives compound, but is a floor forming?* | 17 · 26-03-05 | OP, PT **$900** | $659.39 → **+36.5%** | [download](http://xs-macbook-air.local:5001/zsxq/pdf/585552414545124/Bernstein-US%20Emerging%20Internet%EF%BC%9AUS%20Internet%EF%BC%9A%20AI%20bear%20narratives%20compound%EF%BC%8C%20but%20finding%20a%20floor%EF%BC%9F-260305.pdf) |
| **2/10** | **Morgan Stanley** — *Where are we trading now: heading into EPS, focused on AI ROIC* | 15 · 26-07-14 | no PT — flow weekly, rating carried since 03/20/2023 | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/412414588854248/Morgan%20Stanley-Where%20Are%20We%20Trading%20Now%EF%BC%9A%20Heading%20into%20EPS%EF%BC%8C%20Focused%20on%20AI%20ROIC-260714.pdf) |
| **1/10** | **Morgan Stanley** — *Where are we trading now: entering 2Q earnings* | 15 · 26-07-21 | no PT — flow weekly, META appears only in the coverage list | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/584281555254814/Morgan%20Stanley-Internet%EF%BC%9AWhere%20Are%20We%20Trading%20Now%EF%BC%9A%20Entering%202Q%20Earnings-260721.pdf) |
| **1/10** | **Bernstein** — *Digital ads 2Q26: AI identity crisis (PDF corrupt at source)* | n/a · 26-07-21 | no PT — unreadable (PDF corrupt at source) | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/814518284545142/Bernstein-U.S.%20Internet%EF%BC%9ADigital%20Ads%202Q26%EF%BC%9A%20AI%20Identity%20crisis-260721.pdf) |
| **1/10** | **Morgan Stanley** — *Where are we trading now: AI hardware vs AI software flow* | 15 · 26-06-09 | no PT — flow weekly, rating carried since 03/20/2023 | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/181245828524552/Morgan%20Stanley-Internet%EF%BC%9AWhere%20Are%20We%20Trading%20Now%EF%BC%9A%20As%20AI%20Hardware%20vs%20AI%20Software%20Flow%20Debates%20Continue-260609.pdf) |
| **1/10** | **Morgan Stanley** — *Where are we trading now: into the summer of AI* | 15 · 26-06-03 | no PT — flow weekly, rating carried since 03/20/2023 | no PT row | [download](http://xs-macbook-air.local:5001/zsxq/pdf/415288428281848/Morgan%20Stanley-Internet%EF%BC%9AWhere%20Are%20We%20Trading%20Now%EF%BC%9A%20Into%20the%20Summer%20of%20AI-260603.pdf) |

> Note: a **58th** META call exists but has no surface — Morgan Stanley's *How Much Capacity Will $2 Trillion of Hyperscaler Capex Bring By '27?* (58 pp, file `585424181184514`, 17 May 2026, OW / $775). It shares `(META, Morgan Stanley, 2026-05-17)` with the headcount note, and `uq_ticker_broker_date` keeps only one row per broker per day — the headcount note (8/10) won. The same date-and-PT collision, the same call, so nothing is lost numerically: [download](http://xs-macbook-air.local:5001/zsxq/pdf/585424181184514/Morgan%20Stanley-How%20Much%20Capacity%20Will%20%242%20Trillion%20of%20Hyperscaler%20Capex%20Bring%20By%20%E2%80%9927%EF%BC%9F-260517.pdf).

---

## Why each one rates what it rates — and what it is actually worth

### 10/10 — Morgan Stanley, 26-06-02 · *4 products to turn Meta back into an AI winner* (21 pp)

**Why bullish/bearish:** Overweight, Top Pick, PT $775 (~30% upside to the $600.47 close of 1 Jun 2026); bull $1,000 (28x '27), bear $450 (14x). Four products, each worth $1-3 to '28 EPS on top of ~$35.79: Meta AI search $2.89, subscriptions $1.92, core ad upside $0.94, neocloud $2.97 → $38.76. Search: 1bn MAU × 1 query/day × 10% commercial rate at $0.30/query = $11bn revenue, 8% of '28 EPS, with sensitivities to $30bn+/20%+ EPS (GOOGL search is $225bn) — META's query/commercial rates are deliberately a fifth of GOOGL's. Subscriptions: Meta One tiers $7.99-$49.99, Instagram/Facebook/WhatsApp Plus $2.99-$3.99; 60mn subs at $10 ARPU ≈ $7bn revenue / ~5% '28 EPS. Core ads grow 21%/18% in '27/'28; 1% ad upside ≈ $3.5bn revenue / ~2.5% EPS. Neocloud: management said selling compute externally was "definitely on the table" at the 27 May shareholder meeting.

**Insight density:** Proprietary TAM-sizing models and sensitivity grids; references a leaked Meta ad deck.

**Data support:** 14 exhibits — EPS bridge, search/subscription/MW sensitivity tables, tier pricing table, valuation build.

**Event context:** Quiet patch, but anchored to the 27 May shareholder meeting and the All-America vote.

**Why 10:** the densest primary META monetization work in the batch.

---

### 9/10 — J.P. Morgan, 26-09-10 · *The models and agents are here — upgrading to Overweight, $820 PT* (23 pp)

**Why bullish/bearish:** UPGRADED to Overweight from Neutral; December-2027 price target raised to $820 from $640. The old target was 18x 2028E GAAP EPS; the new one is 23x 2028E GAAP EPS of $35.44, which JPM calls potentially conservative. Price $653.69 on 09 Sep 26 → +25.4% upside. This is the most recent rating action on META. The "show me" on models has been delivered. Meta Superintelligence Labs set out in summer 2025 to reach the frontier within a year and has effectively done it — Muse Spark 1.1 in July, 1.3 by September, competitive with Claude and GPT across agentic, coding, instruction-following and long-context benchmarks, with Watermelon next and post-Watermelon models already scaling on the Prometheus GW cluster in Ohio. The monetization unlock is Muse, the consumer agent launched across iOS/Android/web: it runs in its own virtual computer, browses and navigates UIs (purchases, bookings, forms, email/text) across Instagram, WhatsApp, Spotify, DoorDash, Etsy, Reddit, Yelp and Outlook/Gmail, hit #3 among free US App Store apps on day two with usage at 10x testing cohorts, and is free (100m weekly tokens) with $20/mo (500m) and $100/mo (3bn) tiers — JPM expects a take-rate/commission model plus subscriptions inside a TAM it sizes in the tens of trillions. Model API access is the second lever, priced competitively to drive volume. Offsets stated plainly: JPM models 2027 capex of $243bn (+70%) and 2028 capex of $284bn (+17%), both well above consensus, and FCF of roughly negative $65-70bn in each of 2027 and 2028.

**Insight density:** Proprietary is the upgrade framework and the estimate reset (2026E adj EPS $36.46, 2027E $41.08, 2028E adj $46.07 vs GAAP $35.44); the product facts are company disclosure. Genuinely new early engagement datapoints (app-store rank, 10x cohort usage).

**Data support:** Full JPM model (revenue $254.3bn '26E to $354.4bn '28E; EBIT margin 46.1% '26E to 43.2% '28E), Artificial Analysis model-comparison exhibit, US App Store ranking exhibit, Muse use-case/task-flow exhibit, valuation at 23x 2028E GAAP EPS.

**Event context:** Written the day after the Muse AI launch and roughly two weeks before Meta Connect; meta shares were +20% off their lows but -1% YTD against the S&P's +12%.

**Why 9:** the dated, reasoned upgrade that anchors the current bull case on the name.

---

### 9/10 — Bernstein, 26-04-30 · *US Internet mega 1Q26 earnings: more similar than different* (29 pp)

**Why bullish/bearish:** META Outperform, PT $850 cut from $900 (2027e EV/Sales 8x → 7x) on unclear AI-product progress and soft 2Q guidance. 1Q26 revenue $56.3B +33% (+29% FxN), ad revenue +33% with impressions +19%/price +12%, Other (business messaging) +74%, EBIT $22.87B +30% Y/Y, 41% margin, GAAP EPS $10.44 on one-time tax ($7.31 ex-items). Bear-side details: 2Q guide mid-point decelerates 33%→25% (23% FxN); FY26 expense guide unchanged despite headcount cuts; capex raised $10B to $125–145B on memory/supply-chain costs; DAP fell to 3.56B Q/Q (WhatsApp Russia limits, Iran war — sequential growth ex-those two markets). Bull case rests on revenue leverage, the shipped Muse Spark model with consumer-AI/e-commerce focus, and Susan Li's ability to flex 2027 capex down. "We'd be buyers of Meta's dip."

**Insight density:** Semi-proprietary — line-by-line actual vs Bernstein vs consensus, plus estimate-revision tables; no new channel data.

**Data support:** Earning dashboard, 1Q26 actuals vs B/E vs consensus, full META model (FY26 revenue $255.1B, capex $134.3B, FCF -$0.3B; FY27 FCF $15.5B), capital-intensity and headcount exhibits, managed quotes.

**Event context:** Written hours after the 29 April print.

**Why 9:** the primary post-print META read, with both the model and the reason for the PT cut.

---

### 9/10 — Bernstein, 26-01-27 · *Investment memo: pumping AI iron* (21 pp)

**Why bullish/bearish:** Outperform, PT $870, unchanged (set 30 Oct 2025); META $672.36 on 26 Jan 2026 → +29% upside, implying 24x 2027E P/E. A barbell on the Avocado model. If it is competitive Meta rejoins the AI-winner cohort; if hopelessly behind it can wind down and partner (Anthropic flagged as ideal); the most likely "close but not quite" is the feared middle, forcing a longer, un-ROIC-able investment cycle. The ownership case rests on the core: ad growth ran from 16% Y/Y in 1Q25 to 26% in 3Q25, with AI ad products (GEM, Andromeda, Lattice) delivering 4-14% quality and conversion lifts. Bernstein models $155B+ FY26 expenses against Street's ~$150B, capex up $35-40B, and cuts FY26E EPS to $30.67 (from $31.05) on revenue of $241.6B — 2.3% above consensus.

**Insight density:** Proprietary — a 20-25% ROIC estimate on AI-to-core spend, the expense debate quantified, and the $15B Scale AI price tag read as Llama's admission of failure.

**Data support:** 13 exhibits including old/new/consensus revision tables, the AI ad-product scorecard, M7 dispersion and a full model; CTO-at-Davos and Susan Li podcast references.

**Event context:** A pre-4Q25-print investment memo, positioning explicitly into the guidance.

**Why 9:** the deepest primary META work in the set, with a testable framework and quantified revisions.

---

### 9/10 — Morgan Stanley, 25-12-11 · *3 catalysts to outperformance and the bull case in '26* (18 pp)

**Why bullish/bearish:** Overweight, PT cut to $750 from $820 (bull $1,000, bear $450); implies ~23x '27 EPS, 12% upside to the $650.13 close (10 Dec 2025). Three catalysts. (1) Revenue revisions — MS is 2%/4% ahead of Street for '26/'27. (2) A '26 opex "clearing event": MS raises '26/'27 GAAP opex 5%/6% to $155bn/$187bn and capex to $115bn/$135bn, cutting '26/'27 EPS ~8%/8% to $29.35/$33.02; the point is a credible floor of ~$30/$33 EPS that starts tactical buying at ~22x NTM (down from ~28x earlier in '25, vs GOOGL's 33% premium, a 3-yr high). (3) Superintelligence-team model/product nodes — a frontier model (likely Blackwell-trained) possibly this spring; success drives the $1,000 bull case at ~27-28x.

**Insight density:** Proprietary bottom-up opex model (hyperscaler deals, D&A, energy, headcount), not channel checks; no survey n=.

**Data support:** NTM P/E history, the opex build table, bull/base/bear valuation splitting multiples and DCF (8% WACC, 3% terminal), growth-adjusted comp table, full prior-vs-current model, risk-reward with options-implied probabilities (29.5% >$750, 17.7% <$450).

**Event context:** Pre-print — positioned ahead of the January 4Q opex guide, with sentiment explicitly negative.

**Why 9:** primary, quantified META work with a dated, testable op-ex-guide catalyst.

---

### 8/10 — Goldman Sachs, 27-07-30 · *Q2'26 review: near-term ROIC evidence, long-term compute-spend visibility missing* (10 pp)

**Why bullish/bearish:** Buy reiterated; 12-month PT cut to $725 from $815. Price $585.61 (29 Jul close), +23.8% upside. Core ad evidence is strong — Q2'26 revenue $60.80bn (+28% YoY), advertising $59.36bn (+27.5%), US & Canada ad revenue +31%, Advantage+ at $75bn ARR. The problem is spend visibility: management raised FY26 capex to $130-145bn, reiterated maximising capacity through 2026-27 and gave no long-term capital plan, so GS lifted cumulative 2027-28 capex ~14% (to $220.2bn and $231.2bn) and cut 2026E EPS to $31.65 from $33.28 and 2027E EPS to $31.39 from $35.69. Q2 GAAP operating income of $18.78bn (30.9% margin, -228bps vs GSe) and EPS $6.18 (-8.4% vs GSe) absorbed ~$3.6bn of one-time charges, of which $2.4bn litigation.

**Insight density:** The capex/ROIC framework, scenario weights and the "neocloud" monetization debate are analyst constructs; Q2 actuals and guidance are company data.

**Data support:** Exhibit 1 revenue/capex/D&A/expense growth 2023-31E (capital intensity peaks at 70.9% in 2027E); Exhibit 2 Q2 actuals vs GS/consensus/guidance; Exhibit 3 estimate changes by segment; Exhibit 4 valuation table — downside $355, base $725, upside $935.

**Event context:** Q2'26 print of 29 Jul; the stock was -12.5% over 3m and -27.2% vs the S&P over 12m and trades ~17x updated 2027 GAAP EPS ex-cash. Debates framed as spend pace, AI monetization and financing.

**Why 8:** hard numbers, transparent estimate changes and a full scenario table behind the PT cut.

---

### 8/10 — Goldman Sachs, 26-08-26 · *Social-media lawsuit overhang reduced with settlement* (12 pp)

**Why bullish/bearish:** Buy reiterated; 12-month PT $725, unchanged. Price $576.14, +25.8% upside. The 26 Aug settlement with 52 state and territorial attorneys general caps the youth-safety overhang: Meta pays up to $17.1bn and commits to a two-hour daily teen time limit, Night Access/School/Productivity modes, disabling like counts and cosmetic filters by default, non-personalized feeds, age-verification resourcing and limited U13 data; GS notes press reports of plaintiffs seeking $1.4trn. Separately, GS models external compute monetization: at ~7GW of capacity by YE26 and ~12.5GW by YE27, leasing excess capacity could add $9.3-56.2bn of 2027 revenue, from "neocloud" bare-metal deals to a full hyperscaler offering. Core ads — forecast +27% in 2026 and +21% in 2027 versus ~9% two-year CAGR for global ex-China digital ad spend — are framed as ROIC proof.

**Insight density:** The GW/revenue-per-GW scenario and neocloud-vs-hyperscaler taxonomy are proprietary; settlement terms come from the announcement and press reports, roadmap items partly from The Information and Business Insider.

**Data support:** Exhibit 1 external compute monetization scenario (GWs, $bn, sourced to 451 Research/Reuters); Exhibit 2 recent AI product roadmap; standard financials (2026E EPS $31.65, capex $138.4bn) and the 26.0x/45.0x valuation blend.

**Event context:** Triggered by the settlement announcement; shares were -23.6% over 12m and -35.7% vs the S&P on capex and lawsuit overhangs. Catalysts: Meta Connect on 9/23 and foundational model releases.

**Why 8:** the only note in the set that sizes an unmodelled AI revenue stream in dollars, alongside a real overhang removal.

---

### 8/10 — Morgan Stanley, 26-07-30 · *North America core strong now; more call options soon* (16 pp)

**Why bullish/bearish:** Overweight, Top Pick; PT $775 (no revision shown; 23X the average of $34/$35 '27/'28 EPS). The core moat is still compounding — 3.6bn DAFU, 2bn Instagram DAUs — and the 3Q guide's $64bn top end implies 26% y/y ex-FX, an acceleration on a two-year stacked basis (51% in 3Q vs 48% in 2Q). Management said "soon" 12 times on the call about product updates, and MS sizes four call options — neocloud $2.97, Meta AI Search $2.89, subscriptions $1.88, API $1.22 — worth up to $9 (~25%) on its $34.59 '28 EPS; realizing half alone puts the stock at ~14X '28. MS '27/'28 EPS rose +2%/+4%; revenue '26 $255.9bn, capex $144.7bn '26 rising to $250bn '28, with FCF negative in '27 (-$26.2bn).

**Insight density:** Mostly restated 2Q commentary plus MS modeling; the one original artifact is the 4-product sizing from its 2 Jun 2026 note. No channel checks or survey.

**Data support:** Prior-vs-current model table, full income statement/balance sheet/cash flow, the call-option EPS bridge, risk-reward with options-implied probabilities.

**Event context:** Around the 2Q print (Jul 29 close $585.61), with Meta Connect (Sep 23/24) framed as the next catalyst.

**Why 8:** a genuine META-primary note with a quantified EPS bridge and full model.

---

### 8/10 — Deutsche Bank, 26-07-24 · *Meta ambitions need Meta scale* (18 pp)

**Why bullish/bearish:** Buy maintained; PT cut to $800 from $810 (-1%), on 24x FY27E GAAP EPS. Price $606.10 at 23 Jul 2026. 2Q26 revenue estimate raised to $60.5bn from $60.3bn (~27% y/y), near the top of $58-61bn guidance, on "overwhelmingly positive" ad checks citing ROAS and conversion gains from Gem, Andromeda, adaptive ranking and Advantage+. The post-Iran macro recovery held, helped by GLP-1/peptide verticals. Subscriptions ($7.99/$19.99 AI, $14.99/$49.99 creator) are modelled at $4.5-15.6bn FY27 revenue and $1.30-4.60 EPS; business agents run 10mn weekly conversations, up tenfold this year. Reported 7GW of 2026 capacity rising to 14GW in 2027 lifts DB's FY27 capex to ~$210-215bn (from ~$183bn); at $35bn/GW that implies $245bn, but partner-funded Hyperion and internal silicon imply ~$165bn directly funded.

**Insight density:** Proprietary ad checks and the capex-per-GW bridge; the Alphabet read-through, subscription pricing and the Anthropic cloud talks (~$10bn) are restated.

**Data support:** Sensor Tower Instagram engagement (Fig 1), 2Q26 outlook (Fig 2), estimate changes (Fig 3).

**Event context:** Pre-print, with Meta trading near 16x NTM EPS versus the S&P 500 at about 21x.

**Why 8:** dense, numerically explicit preview with its own capex bridge.

---

### 8/10 — Morgan Stanley, 26-07-01 · *5 takes on the neocloud vs hyperscaler opportunity* (16 pp)

**Why bullish/bearish:** Overweight, Top Pick, PT $775 (unchanged; bull $1,000, bear $450), 37.6% upside to the $563.29 close (30 Jun 2026), ~23x '27 EPS of ~$34. Written on a Bloomberg report that Meta plans a cloud business (a Bedrock-like hosted API serving Muse models, plus a raw-silicon neocloud offer) inside Meta Compute. MS argues the neocloud half is the easy half: META brings on ~2GW/~3.5GW owned-operated IT capacity in '26/'27 on a ~3GW YE25 base while renting ~2.5GW from Coreweave/Nebius/GCP/ORCL, versus AMZN/GOOGL adding 5GW/9GW in '27. Modelling: every 250MW leased for one year at $40/W is ~$3 (8%) of '28 EPS; the whole sensitivity grid runs $1.49-$11.88 EPS (4-33%). A full hyperscaler API is a "show me" — Muse scored poorly on TerminalBench and SWE Bench Verified, and META lacks enterprise GTM. Capex modelled at $175bn/$205bn in '27/'28 vs $145bn in '26.

**Insight density:** Proprietary capacity and $/Watt sensitivity model ("interactive Meta Neocloud model"), not consensus restatement.

**Data support:** Capacity-additions chart, two sensitivity tables, hyperscaler capex stack ($1.2tn '27), full bull/base/bear build, risk-reward page.

**Event context:** Same-day reaction to a press report; META had not commented.

**Why 8:** primary META optionality work built on its own GW model, though triggered by a headline.

---

### 8/10 — Morgan Stanley, 26-05-17 · *Headcount reductions and the neocloud backup optionality* (17 pp)

**Why bullish/bearish:** Overweight, Top Pick, PT $775 (unchanged, 25% upside to the $614.23 close of 15 May 2026); '27 EPS ~$34.16. A model refresh, not a new thesis. (1) A 10% headcount cut (~8K) effective May → $800mn one-time charge and ~$2bn/$3.5bn opex savings in 2H26/FY27, calibrated on the '22-'23 Year of Efficiency RIF (21K heads, ~$2.1bn charges, ~$100k/head) and ~$450k opex/head; reports of ~16K would add ~$3.5bn '27 savings, ~$1.20 EPS. (2) '27 net headcount growth cut from 5% to ~3.5% after 6,000 job postings closed. (3) '26/'27 capex raised 7%/6% (~$10bn each) to $144.9bn/$174.5bn, lifting '27 D&A 9%. Net: '26 EPS +3.7% to $32.83, '27 flat. The "backup safety valve": 4.4/3.9GW added in '26/'27 could be rented for $10-15bn a year, ~8% '28 EPS upside.

**Insight density:** Proprietary headcount-cost and cost-of-revenue models; social-media reports flagged as unconfirmed.

**Data support:** D&A/cloud-deal cost build, opex-per-head table, prior-vs-current bridge, bull/base/bear build.

**Event context:** Written the weekend after RIF reports, ahead of Meta Conversations (3 Jun) and Connect (23-24 Sep).

**Why 8:** disciplined, fully quantified META estimate work with management-silence caveats.

---

### 8/10 — Morgan Stanley, 26-04-30 · *Internet 1Q26: GOOGL, AMZN and META surprises and learnings* (39 pp)

**Why bullish/bearish:** Overweight / Top Pick, META's $775 PT unchanged (the only PT moves are AMZN $300→$330 and GOOGL $330→$375); consensus mean $847.08. META's 1Q26 revenue was $56.31bn, 0.8% below MS's $56.76bn estimate, but adjusted EPS beat 8.4% ($9.11 vs $8.41); GAAP EPS of $10.44 was flattered by a -23.1% tax rate, while cost of revenue ex-SBC landed 30% below plan and gross margin hit 82.4%. The bull case runs on AI-driven core gains — Facebook video time +8%, Instagram Reels time +10%, price per ad +12%, impressions +19%, 8m+ advertisers using GenAI creative tools, Value Optimization Suite at $20bn ARR, 10m weekly business-AI conversations — plus Muse-enabled products and a RIF: a memo flagged a 10% workforce cut (~8,000) and 6,000 open roles, worth $0.50-$1.50 per 10% cut on the ~$34 '27 EPS, with capex rising ~$10bn this year. META trades at 19.1x NTM P/E versus a 20.4x 10-year average, and 0.9-1.4x '27 PEG versus a 1.8-2.0x peer median.

**Insight density:** Fresh company-reported engagement/monetization KPIs and an internal RIF memo, not a channel check.

**Data support:** Actual-vs-estimate table, KPI exhibit, NTM P/E chart, peer PEG tables — but MS's META model is explicitly "under review" with no updated META P&L.

**Event context:** Post-print, written the morning after GOOGL/AMZN reported.

**Why 8:** dense, dated META read.

---

### 8/10 — UBS, 26-04-30 · *Product development benefits still ahead of us* (20 pp)

**Why bullish/bearish:** Buy maintained; price target cut to $865 (prior $908) on unchanged 26x FY-ending-1Q28E GAAP diluted EPS of $33.26 (prior $34.93). Price $669.12 (29 Apr 2026); ~40% upside. 1Q26 revenue/EPS of $56.3B/$10.44 beat UBSe $55.9B/$7.19 and consensus $55.5B/$6.68, with impressions +19% y/y (up 1ppt q/q). The 2Q26 guide of $58-61B (midpoint $59.5B) is merely in line with the Street, which the authors argue is not proof that GenAI ad benefits are priced in: only OpEx and CapEx sit in models at 19x 2027 GAAP EPS, while revenue benefits remain unmodelled. Higher costs do bite — 2027E/2028E EPS fall 5%/7% to $32.98/$34.98, though 2026E rises to $32.67.

**Insight density:** Proprietary is the revenue-versus-cost bridge and the asymmetric setup; the four GenAI pillars and price-target math are recycled from prior notes.

**Data support:** Figures 1-2 (estimate changes, 1Q26 vs UBSe), 3-4, 5-7 (valuation, upside $1,022/downside $533, 2.6x skew), full statements.

**Event context:** 1Q26 print; CapEx guidance raised to $125-145B (from $115-135B) and no buyback executed.

**Why 8:** precise estimate bridge and an explicit, checkable bull case.

---

### 8/10 — Bernstein, 26-04-27 · *Digital ads 1Q26: it's good to be big, right?* (37 pp)

**Why bullish/bearish:** META Outperform, PT $900, unchanged ahead of the print (33% upside to $675; 50/50 2027e EV/Sales 8x + DCF 10%/3.5%). META and AMZN are the top picks. Expects Meta to beat its own strong 1Q26 guide of $53.5–56.5B (+26–34% Y/Y) on resilient US consumer demand and a ~4ppt ROW FX tailwind; B/E 1Q26 revenue $56.5B vs consensus $55.5B (+2%), EBIT $19.5B, DAP 3.613B. Risks printed plainly: March softness, FX fading in 2Q, and ROAS normalizing toward ad prices — pressuring 2Q guidance. Capex guidance likely unchanged; AI-tool efficiency plus RIFs support EPS upside and 2027 FCF acceleration. Youth-regulatory risk called "overstated" (teens ~1% of revenue; causation harder than tobacco's physical harms), with second-order policy effects the real long-term risk.

**Insight density:** Proprietary third-party checks — Pathmatics: Temu spend on Meta -17% Y/Y, Shein +16%; Tinuiti impressions +17%/CPM -3%; Sensor Tower FB downloads -8% US, -13% ROW, IG -6%/-15%; Similarweb.

**Data support:** Full META model (FY26 revenue $255.2B, EPS $31.12, capex $127.6B, FCF $11.1B), an FY18–FY26 expense-guidance track record, AI-product brainstorm, 2x2 valuation framework.

**Event context:** Pre-print preview, two days before 1Q26 results.

**Why 8:** real pre-print work with channel data and a full model.

---

### 8/10 — Deutsche Bank, 26-04-18 · *Early sparks of Meta superintelligence (translated note)* (17 pp)

**Why bullish/bearish:** Buy, PT $920 maintained; Key changes revise only FY26 EPS and revenue; no PT revision. Price $662.49 at 14 Apr 2026. Pre-print. An ad-check call with Inventus Media's Andrew McLean showed Meta spend +6.0% in 1Q26 versus +5.5% expected, with 2Q26 accelerating ~40bps to +6.4% y/y versus consensus's ~230bps deceleration on a ~210bps tougher comp. DB lifts 1Q26 revenue to $56.4bn (+33% y/y) from $55.4bn and GAAP operating income to $21.1bn (37.5% margin). Muse Spark, MSL's first model, is natively multimodal, uses "an order of magnitude" less compute than Llama 4 Maverick, and its closed-source shift unlocks Ray-Ban glasses, healthcare and Shopping Mode.

**Insight density:** Proprietary agency checks and the claim that ad-load redistribution alone drove 4x the Facebook revenue impact of pure ad-load increases in 2H25; Muse Spark specifications and CoreWeave terms are restated.

**Data support:** Sensor Tower DAU/time-spent charts (Figs 1-4), 1Q26 model (Fig 5), estimate-change table (Fig 6), P/NTM EPS versus S&P 500 (Fig 7).

**Event context:** Pre-earnings, after a pullback DB calls a buying opportunity; New Mexico and Los Angeles litigation weigh on sentiment.

**Why 8:** primary ad-channel evidence plus a full model refresh.

---

### 8/10 — Morgan Stanley, 26-04-14 · *Key themes and numbers into GOOGL/META/AMZN earnings* (37 pp)

**Why bullish/bearish:** Overweight, META is the team's Top Pick (pecking order META, AMZN, GOOGL), PT $775 vs the 13-Apr close of $634.53 (+22.1%), ~23x '27 P/E; no PT revision shown. Consensus mean $846.35, and the bull/base/bear cases are $1,000 (~26x) / $775 / $450 (~14x). MS models 34%/28% y/y revenue growth in 1Q/2Q and 28%/21% for '26/'27 (FY26 revenue $256.7bn, ad revenue $250.2bn), but the new Nebius/CoreWeave cloud deals raise '27 cost of revenue ($25.9bn of cloud-deal CoR vs $1.1bn in '25) and cut '27 GAAP EPS ~6% to $34.19 from $36.31, with $2.4bn of annual NBIS expense and up to $5.4bn of incremental annual CoR; FCF falls 7% to $23.7bn. Headcount cuts are the offset: every 10% reduction could add $1-$2 of EPS.

**Insight density:** MS's own bottom-up model plus industry/company conversations; no channel checks or n= survey on META.

**Data support:** Prior-vs-current META model, PT build (multiples + DCF at 8% WACC/3% terminal) with consensus distribution, cloud-cost and opex builds, peer PEG table, two risk-reward pages. MS is 17% above consensus on '27 META capex ($164.9bn vs $141.2bn).

**Event context:** Pre-earnings, written into the GOOG/META/AMZN 1Q26 prints, with April branded-ad softness flagged.

**Why 8:** primary, quantified META work with a fresh valuation build.

---

### 8/10 — Morgan Stanley, 26-04-09 · *Meet Meta's Muse* (14 pp)

**Why bullish/bearish:** Overweight, Top Pick; PT $775 (below the $825 in MS's 15 Mar 2026 note in this batch). Muse Spark (ex-"Avocado"), META's first homegrown model out of Meta Superintelligence Labs, is the "first step in re-rating." Benchmarks sit slightly below leading models but the gap is smaller than investors feared, so META's edge shifts to productization: shopping mode is already live with multi-modal, reasoning-driven shoppable links drawing on META's user/influencer content, which MS thinks lifts conversion where trust is the gating factor. Muse Spark is closed source but offered via API to select partners, so API revenue is "not priced at 17X '27 EPS." META trades at 17x '27 EPS ($36.3, 16% '25-'27 CAGR) and 1.1x '27 PEG versus a 2.4x peer median — a ~54% discount; the $775 PT implies 21x '27 and still a ~42% PEG discount.

**Insight density:** Analysts' own hands-on product trial plus MS's recurring surveys/trackers (trust gating agentic purchase adoption) — semi-proprietary, no new n= disclosed.

**Data support:** Shopping-mode screenshots, NTM P/E history chart, PEG comp table vs AAPL/MSFT/GOOGL/AMZN/NFLX, DCF (8% WACC, 3% terminal).

**Event context:** Model-launch day (Apr 8 close $612.42).

**Why 8:** META-specific, with a real product read and a clean valuation frame.

---

### 8/10 — Goldman Sachs, 26-03-22 · *Framing recent news reports against our strategic-focus view* (14 pp)

**Why bullish/bearish:** Buy reiterated; 12-month price target unchanged at $835. Price $593.66 at the 20 Mar close, 40.7% upside. A news-driven defence. GS argues three press reports were misread: the Horizon Worlds change is a de-emphasis of legacy VR, not an end to Reality Labs; a Superintelligence Lab model delay was always baked in — GS modeled at least 9-12 months (May/June 2026) to stand up the lab publicly and anchors on the CEO's 2H26-into-2027 framing. It then quantifies three illustrative cost scenarios. Scenario 1 (year-end headcount -15% in 2026, +5% in 2027-28; non-D&A cost per head +6%) lifts 2026 EPS to $31.81 (+10.5% vs GSe) and 2027 to $41.23 (+22.7%). Scenario 2 (Reality Labs expenses down HSD-LDD% with 10% reinvested) adds ~L-MSD%, 2026 EPS $29.62 (+2.9%). Scenario 3 (flat non-D&A opex) implies 30%+ in 2026 and 40-50% in 2027-28, flagged low probability.

**Insight density:** Proprietary is the scenario framework and the valuation framing; the triggering news reports and guidance are restated. No base-case estimates changed.

**Data support:** Exhibits 1-4 (scenario tables and sensitivity grids), Exhibit 5 (2023-2031E revenue/capex/D&A), Exhibit 7 (downside $540/base $835/upside $1,175).

**Event context:** Since 29 Jan, the day after Q4'25 results, META fell 20% versus the S&P's 7% on AI/compute capex ROI concerns; shares trade at ~20x/~17x 2026/27 GAAP EPS ex-cash.

**Why 8:** a timely, quantified response to what is actually moving the stock.

---

### 8/10 — Goldman Sachs, 26-01-29 · *Q4'25 review: AI impact in the core, investments still scaling* (10 pp)

**Why bullish/bearish:** Buy reiterated; 12-month PT $835. Price $672.36 (28 Jan 26) → ~+24% upside; downside/base/upside $540/$835/$1,175. The Q4'25 print reset the debate from growth to spend. Metadata points were strong, but guidance opened a gap: 2026 total GAAP expenses of $162-169bn (+38-44% y/y at the midpoint) and capex of $115-135bn (GSe $132.2bn, +83% y/y), both above consensus, with Reality Labs' ~$6.0bn quarterly loss guided to persist through 2026. GS's contribution is Exhibit 2, an illustrative implied-FY26-revenue triangulation off the expense guide, plus the capital-intensity path: D&A alone is modelled to climb steeply as the 2025-26 build lands, so reported margins compress even if the core accrues.

**Insight density:** The implied-revenue triangulation in Exhibit 2 and the D&A-driven capital-intensity path are proprietary; guidance and actuals are restated.

**Data support:** Exhibit 1 (revenue/capex/D&A/expense model to 2031E), Exhibit 2 (illustrative implied FY26 revenue), Exhibit 3 (Q4 actuals vs GS/consensus/guidance), Exhibit 4 (estimate changes), Exhibit 5 (downside $540/base $835/upside $1,175).

**Event context:** Written on the Q4'25 print; the stock had fallen 11.0% over three months and 13.8% versus the S&P over 12 months beforehand.

**Why 8:** the guidance-inversion exhibit is a real analytical contribution and the estimate bridge is fully shown.

---

### 8/10 — UBS, 26-01-29 · *Stronger signals of AI benefits to emerge in 2026* (21 pp)

**Why bullish/bearish:** Buy reiterated; PT raised to $872 (prior $830), unchanged 26x on FY-ending-4Q27E GAAP diluted EPS of $33.52 (prior $31.94). Price $719.65 (28 Jan 2026). 4Q25 revenue/EPS $59.9B/$8.88 beat UBSe $58.2B/$7.95 and consensus $58.3B/$8.19; impressions +18% y/y while conversions grew faster than impressions — the core claim, and the mechanism that keeps ROAS improving even as ad load decelerates. 1Q26 guidance of $53.5-56.5B (mid $55.0B) tops Street's $51.2B, and 2026 ad-dollar growth implied near $52B funds a higher cost base ($165.5B expense/$125B capex versus consensus $150B/$110B) while still lifting EPS to $30.28/$33.52/$35.55 for 2026-28.

**Insight density:** Proprietary is the conversions-versus-impressions ROAS inference and the "costs modelled, revenue optionality not" framing; the five GenAI pillars and guidance are restated.

**Data support:** Figures 1-2 (estimate changes, 4Q25 vs UBSe), 3-7 (impressions, price per ad, valuation; upside $1,047/downside $610, 3.0x skew), full statements.

**Event context:** 4Q25 results, framed as a "clearing event" now that 2026 OpEx/CapEx parameters are set.

**Why 8:** genuine estimate revisions plus a falsifiable impressions/conversions mechanism.

---

### 8/10 — Citi, 25-10-13 · *IG/Reels ad-load tracker: 3Q reaches 27.1%, +230bp q/q* (31 pp)

**Why bullish/bearish:** Buy reiterated, TP $915, 29.7% upside off the $705.30 close of 10 Oct 25; no prior-PT change disclosed, plus a new 90-day Upside Catalyst Watch. Bull $1,139, bear $638. Citi's manual panel — ads logged across the first 50 Reels per session, recording placement, advertiser size and vertical — shows IG Sponsored Reels ad load at 27.1% in 3Q25, +230bp Q/Q, +460bp Y/Y, the fastest since 4Q22, reaching 28.8% in September. With ad load expected to decelerate, the growth lever shifts to CTR/relevance. 3Q25E revenue $50.3B (+24% Y/Y) vs $49.3B consensus.

**Insight density:** Proprietary Reels panel plus Revealbot CPMs; Tinuiti and Sensor Tower data restated.

**Data support:** 30 exhibits: cumulative ad load 4Q22-3Q25, session distribution, advertiser and vertical mix, Reels model ($63B by '27E).

**Event context:** Pre-earnings, IG past 3B MAU, Sora/Vibes share-of-time worry.

**Why 8:** dated, falsifiable proprietary panel.

---

### 7/10 — Morgan Stanley, 26-09-09 · *Muse has arrived: what matters next* (15 pp)

**Why bullish/bearish:** Overweight, Top Pick; PT $775 (unchanged). Muse, META's standalone consumer AI agent (ex-"Hatch"), opens the $30tn consumer agentic TAM MS maps across retail/travel, ads, AV/rideshare, delivery, logistics and wearables. It handles shopping, travel, tickets, scheduling and email; purchases need user verification; it is a separate app that does not yet feed META's ad system. MS argues scaled distribution plus unique social datasets (FB/IG/Messenger/WhatsApp, even Gmail) and a free entry price give META an edge, with the Watermelon model due this Fall. The mechanism is unpriced optionality: META trades at 18X '28 EPS, and MS '26 EPS of $31.80 sits only marginally above consensus $31.41, with '26 constant-currency growth of 26.6%.

**Insight density:** Analyst hands-on use of the launch product and MS's own $30tn TAM framework, but no survey, channel check or n=; largely a framing piece with a GOOGL read-across.

**Data support:** TAM exhibit ($29tn 2023 → $32tn 2028), Muse integration screenshots, plus two risk-reward pages (META and GOOGL $400 PT).

**Event context:** The day after the Muse launch (Sep 8 close $613.48); explicitly a "what matters next" watchlist, since FB Shopping, the Metaverse and MetaAI disappointed.

**Why 7:** useful product/optionality framing and competitor read-across, but no new META numbers.

---

### 7/10 — Bernstein, 26-08-20 · *Digital ads in 2Q26: AI benefits accrue elsewhere* (36 pp)

**Why bullish/bearish:** META Outperform, PT $800/share — stated in the coverage summary on p2 and in the ticker table; unchanged from the 29 Jul cut. META closed $546.03 on 19 Aug. A sector note, but META's page is substantive: "Still need to see it to believe it, but risk-reward remains attractive." Core performance stays strong — 2Q26 revenue +27% y/y, and META takes 47% of incremental digital-ad dollars against a 38% share — while AI spend stays heavy through at least 2027 and is only early to monetize (business messaging, paid model APIs, subscriptions). At ~15x 2027E EPS, one consumer-AI win re-rates the stock; the AI-ROIC debate is what keeps it cheap. The note also flags Meta's AI ambitions against the broader basket's deceleration as 3Q guidance laps last year's AI-driven gains.

**Insight density:** Genuinely proprietary for the sector — Pathmatics US ad-spend tracker (Temu US +389% y/y, Shein US +89%), a vertical tailwind/headwind tracker and post-print consensus-revision exhibits — though the META paragraph itself is commentary.

**Data support:** 32 exhibits plus a full META P&L/FCF model (FY26E revenue $256bn, EPS $32.27, capex $140.3bn, FCF -$8.9bn); valuation 50/50 6.7x 2027E EV/Sales + DCF (WACC 10%, g 3.5%).

**Event context:** Written into the 2Q26 print season, after META fell 7% the day after its own result.

**Why 7:** the best META exhibit set in the batch, but the call itself is a reiteration.

---

### 7/10 — Bernstein, 26-07-29 · *Meta 2Q26: avoiding TikTok 2.0* (25 pp)

**Why bullish/bearish:** Outperform, PT $800 (from $850), implying 22x 2027E P/E; 2027E EV/Sales trimmed 0.3x to 6.7x. Price $585.61 → +37%. Core fine, AI unproven. 2Q26 revenue +28% Y/Y ($60.8B), ads +27% ($59.4B) on impressions +14% and pricing +12%; DAP 3.6B; Other revenue +73% to $1B; Advantage+ past $75B ARR. Guidance: 3Q $61-64B (+19-25%, 1% FX headwind), FY26 expenses $165-169B, capex tightened to $130-145B. FY26E EPS cut 5% to $32.27 and FY27E 3% to $36.68 on one-time legal and tax. The stock is ~15x next year's EPS: "you get paid to own Meta at 15x". The bull mechanism is optionality — Meta is last-man-standing in consumer AI, and one breakout product, or triple-digit Other revenue, re-rates it.

**Insight density:** Largely restated company disclosure with Bernstein-vs-consensus beat/miss tables; no proprietary tracker. The "TikTok 2.0" framing — Meta arming up because TikTok and ChatGPT caught it out — is an original argument, not new data.

**Data support:** 19 exhibits — estimate revision table (new vs old vs consensus), P&L model, geo, impression, pricing, capex and headcount charts.

**Event context:** The day after the 2Q26 print — a dated, testable call carrying a PT cut.

**Why 7:** the primary post-print note on META with a full revised model, but mostly company-sourced inputs.

---

### 7/10 — Jefferies, 26-07-20 · *Vision Mini dive: when AI moves to the face* (39 pp)

**Why bullish/bearish:** Buy reiterated, PT $825, +28% versus the $646.01 prior close; DCF-derived, implying ~23x 2027E EPS. No PT change in this note — the last move was 05/04/2026, cutting $1,000 (set 01/29/2026) to $825. Scenarios: upside $1,097 (+70%, 26x $42.18 EPS), downside $443 (-31%, 17x $26.84). The team bought and wore three models (Ray-Ban Meta Gen2 $379, Oakley Meta $499, Ray-Ban Display + Neural Band $799) for five months. Assuming Apple-Watch-like adoption, base case is ~35-45M units at ~$400 ASP = ~$14-18B hardware revenue; bull case ~75M units (30% of the iPhone base). Evidence: 7M+ units sold in 2025, daily users tripling y/y, Meta AI MAUs ~1B, EssilorLuxottica reportedly doubling capacity to 20M in 2026, Meta One subscriptions live.

**Insight density:** Proprietary is the hands-on testing — skiing/golf use, 10-minute setup, speaker distortion, ~5/10 battery on the Display. Restated: earnings-call quotes, Bloomberg's EU-delay report, EssilorLuxottica commentary.

**Data support:** Exhibit 1 units×ASP matrix ($6.0B-$55.3B), bear/base/bull scenario table, Meta AI MAU chart, Reality Labs revenue ramp ($2.4B 2025A to $5.1B 2030E), income statement, balance sheet, cash flow.

**Event context:** Written after 1Q26, post the June-2026 launches ($299 Adventurer/Fury, $399 Starfire) and the EU launch delay. Stock $646.01; 52-week $796.25-$520.26.

**Why 7:** real primary-source product evidence with quantified optionality, but no estimate changes.

---

### 7/10 — Deutsche Bank, 26-07-01 · *A silver lining* (13 pp)

**Why bullish/bearish:** Buy, PT $810 unchanged (last set 30 Apr 2026). Price $563.29 at 30 Jun 2026. A Bloomberg report that Meta is building a cloud infrastructure business selling raw AI compute plus hosted model access (Bedrock-like) drives the note. DB's read: Meta monetizes older Nvidia GB200/GB300 and inference capacity while reserving Rubin-era systems for training, implying "disciplined capacity utilization" and "high-flow-through revenue optionality" rather than a retreat from frontier models. FY27 scenarios assume 8.0/9.75/11.5GW of capacity, 1.2-2.7GW of excess, 75% sold at $10-15bn per GW, giving $9-30bn incremental revenue (~$17.5bn base), OI margins of 35.2-38.4% versus 34.8% Street (+44 to +361bps), and EPS of $36.51-$42.59 versus $35.12 consensus (+4-21%). Blue Owl funds 80% of the Hyperion JV.

**Insight density:** Proprietary capacity build-up, $/GW pricing framework and margin math; the Bloomberg report and Prometheus/Hyperion gigawatt disclosures are restated.

**Data support:** Figure 1 FY27E scenarios A/B/C spanning capacity, revenue, operating income and EPS.

**Event context:** News-driven note the morning of 1 July 2026, framed by $125-145bn capex guidance and the AI capex ROI debate.

**Why 7:** a clean, auditable scenario model on a single news trigger.

---

### 7/10 — Deutsche Bank, 26-05-28 · *Subscription rollout creates the first clear consumer-AI monetization layer* (14 pp)

**Why bullish/bearish:** Buy, PT $810 unchanged. Price $635.26 at 27 May 2026. The Meta One rollout (Instagram/Facebook Plus $3.99, WhatsApp Plus $2.99, Meta One Plus $7.99, Premium $19.99, Essential $14.99, Advanced $49.99) creates a direct revenue line against AI usage and answers the "AI costs without AI revenue" overhang. DB's 2027 scenario assumes 1-3% consumer penetration, 0.5-2% AI and 1-3% creator/business at $3.50/$10/$24 blended ARPU, with 90% incremental margins, yielding $4.5-15.6bn incremental revenue ($8.99bn base) and $1.32-$4.59 incremental EPS, 3.9-13.4% above the $34.31 base. Snap's ~5.2% penetration is the benchmark; Meta's 3.6bn DAP and 250-350mn business accounts are the distribution edge.

**Insight density:** Proprietary penetration/ARPU sensitivity model; Sensor Tower Meta AI data (DAUs from under 100K in Nov 2024 to +10mn by May 2026) and Alex Wang's podcast remarks are restated.

**Data support:** Figures 1-3 (Sensor Tower downloads, DAUs, sessions around the 8 Apr 2026 Muse Spark launch), Figure 4 2027 sensitivity table.

**Event context:** Subscription launch after a post-Muse Spark usage step-up, against $125-145bn 2026 capex guidance.

**Why 7:** a useful monetization framework, though near-term revenue is immaterial.

---

### 7/10 — Goldman Sachs, 26-04-30 · *Q1'26 review: core outgrows the industry, long-term AI visibility needed* (10 pp)

**Why bullish/bearish:** Buy reiterated; PT cut to $830 from $840 (13-Apr-26). Price $669.12, +24.0% upside. Q1'26 FXN advertising revenue grew 29% YoY on impression gains and revenue landed at the top of the $53.5-56.5bn guide, but operating income missed GS and consensus. Capital intensity is the risk: FY26 capex guidance rose to $125-145bn from $115-135bn, with a $107bn step-up in cloud commitments and Q1 expenses +35% YoY despite ~10% headcount cuts; Reality Labs lost ~$4bn. GS cut the EV/GAAP EBIT multiple to 24.0x from 26.0x, the post-2022 mega-cap tech average, on lower confidence in the EBIT trajectory.

**Insight density:** Estimate rework and multiple logic are proprietary; Muse Spark and engagement commentary is restated.

**Data support:** Exhibit 1 revenue/capex/D&A/expense growth 2023-31E; Exhibit 2 actuals vs GS/consensus/guidance; Exhibit 3 revisions (2026E EPS $33.28 from $28.64); Exhibit 4 downside/base/upside $500/$830/$1,020.

**Event context:** 29 Apr print; trades ~18x updated 2027 GAAP EPS ex-cash, with Q1 EPS $10.44 flattered by an $8.03bn tax benefit.

**Why 7:** full earnings review with explicit estimate and multiple changes.

---

### 7/10 — BofA, 26-04-20 · *1Q26 preview: expecting a beat, macro sensitivity and AI cost benefits* (18 pp)

**Why bullish/bearish:** Reiterate BUY, price objective cut to $820 from $885 (-7%), on unchanged 2027E GAAP EPS with the multiple cut to 24x from 26x for broader market compression. Price $688.55, 52-week range $479.80-796.25. Despite the sector-preview framing, every analytical section is META-dedicated; other names appear only as a Snap (4/15) read-across and a back-page disclosure row. Expects a 4/29 beat — 1Q revenue/EPS $56.0bn/$7.44 vs Street $55.4bn/$6.64, ad revenue $54,785M (+32% Y/Y, +28% ex-FX). Checks show 1Q spend in line with advertiser expectations, no Middle East pullback, and job postings down 33% q/q implying expense discipline and another EPS beat; 2Q guidance is modelled at $57.5-60.5bn with the '26 expense range unchanged. Risks: macro-driven 2Q guidance and a higher capex skew ($115-135bn; CoreWeave $21bn to 2032, AMD up to 6GW). Muse Spark is the product catalyst.

**Insight density:** Proprietary is the Meta job-postings tracker (average openings -33% q/q vs -16% in 4Q) and the FX basket table; Sensor Tower DAU data and the product-news log are third-party recap.

**Data support:** Eight exhibits — BofA vs Street key metrics and estimates, FB/IG DAU trends, job postings, FX, and a sum-of-parts valuation (20x 2027 GAAP EPS, 17x ex-Reality Labs, 45x P/FCF vs the S&P at 20x).

**Event context:** 20 April 2026, price $688.55 (market cap $1.79tn), nine days before results and after 4/17 Reuters news of a possible 10% May layoff.

**Why 7:** genuinely META-specific and number-rich, but largely estimate-setting and news recap around one proprietary tracker.

---

### 7/10 — Bernstein, 26-04-08 · *Will Muse Spark restore investor belief in the AI story?* (27 pp)

**Why bullish/bearish:** Outperform, PT $900, unchanged (last set 28 Jan 2026). Written on launch day, META closed $612.42 → +47% to target. The mechanism is model → product. Muse Spark lands in Artificial Analysis' top 5, token-efficient (58M output tokens to run the Intelligence Index vs 157M for Claude Opus 4.6, 120M GPT-5.4) and the second-best vision model (80.5% MMMU-Pro vs Gemini 3.1 Pro's 82.4%), so the "can Meta build a frontier model?" overhang lifts. But the note insists a good model is table stakes; the upside is shipping AI features to 3B+ users, 200M+ creators and 10M+ advertisers, with Advantage+ ($60B ARR) and WhatsApp business messaging ($1B+ ARR) as the monetization surfaces. FY26E EPS $30.87, FY27E $37.15 on revenue of $255B/$307B.

**Insight density:** Proprietary hands-on testing — the analysts ran Meta AI, ChatGPT and Gemini side by side on calorie estimation and shopping, with screenshots. Not channel checks or a survey, but genuinely first-hand.

**Data support:** 20 exhibits, mostly side-by-side app screenshots plus benchmark charts; valuation is 50/50 2027E EV/Sales 8x and a DCF (WACC 10%, g 3.5%); verbatim Zuckerberg and Alex Wang Threads quotes.

**Event context:** Launch-day note (8 Apr 2026), timed between Anthropic's Mythos no-show and an expected OpenAI response; no print.

**Why 7:** fresh primary product work and hands-on testing on META, but no estimate or PT change and the thesis is unchanged.

---

### 7/10 — J.P. Morgan, 26-01-29 · *Major AI acceleration — revenue and expense acceleration* (19 pp)

**Why bullish/bearish:** Overweight maintained. The Q4'25 review keeps META a top pick; the note's focus is the estimate reset rather than a target change. JPM frames the quarter as "major AI acceleration, revenue acceleration and expense acceleration". The revenue side beat, but 2026 expenses of $162-169bn (+38-44%) and capex of $115-135bn (+65-94%) both topped JPM's $155-160bn/$115-125bn expectations; GAAP EPS was cut 3-4% for 2026/27 (no buybacks, a 4Q debt raise) and 2026 free cash flow is only about +$5bn. The bull mechanism JPM defends is engagement-driven efficiency: output per engineer rose 30% with AI-coding power users +80% y/y, which it reads as evidence that the spend is being absorbed productively rather than merely spent.

**Insight density:** Proprietary is the estimate reset (old-vs-new table), the "three things the stock needed" framework and the JPME-versus-actual reconciliation; guidance is company restatement.

**Data support:** 4Q25 results-vs-JPME table, 1Q26E-2027E estimate-change table, full model pages.

**Event context:** 4Q25 print and management calls; shares +7% after-hours, though JPM flags pushback. Stock YTD +1.3%, 12m -0.8%, 52-week $796.25-$479.80.

**Why 7:** sharp reconciliation of the beat against the spend guide, but the bull case itself is company-supplied.

---

### 7/10 — Citi, 26-01-28 · *1st impression: ad revenue +23% y/y ex-FX; '26 capex higher than expected* (12 pp)

**Why bullish/bearish:** Buy reiterated, TP $850 unchanged (set 30 Oct 2025 per the ratings history; no revision in this flash). Price $668.73, +27.1% share-price / +27.4% total return. Bull $1,036 (+55%), bear $560 (-16%). A clean 4Q25 beat with a better 1Q guide: revenue $59.9B (+24% Y/Y, +23% ex-FX), 2.5% above consensus and ~1.5% above the high end of guidance; advertising +23% ex-FX on impressions +18% and pricing +6%; GAAP EPS $8.88 vs $8.21 consensus; operating income $24.7B (41.3% margin). 1Q26 revenue guidance of $53.5-56.5B is ~7% above consensus. Offsets: '26 expenses $162-169B (+41% Y/Y at the midpoint, ~9% above Citi) and '26 capex $115-135B (~13% above consensus); FOA operating income $30.8B (52.2%) missed Citi's $31.5B, while Reality Labs revenue of $955M beat its $542M estimate.

**Insight density:** Mostly company results benchmarked against Citi's own model; proprietary content is the variance framework and forward estimates, not a new dataset. The call watch-list is judgement.

**Data support:** Figure 1 line-by-line 4Q25 actual/projection variances (total revenue $59,893M vs $58,902M; FOA ad revenue $58,137M vs $57,582M), guidance framing, bull/base/bear cases, and valuation at ~25x 2027E GAAP EPS of $33.79, ~13x 2027E EV/EBITDA.

**Event context:** 4Q25 print, 28 Jan 2026 16:00 ET; price $668.73, market cap $1,685,552M, versus an October 2025 high near $770. The prior Catalyst Watch was removed 9 Nov 2025 at $590.32.

**Why 7:** accurate, fast post-print wrap, but almost entirely company numbers plus Citi's model.

---

### 7/10 — Goldman Sachs, 25-10-30 · *Q3'25 review: strong Family-of-Apps, investment commentary overhangs* (9 pp)

**Why bullish/bearish:** Buy reiterated (rating since 12 Sep 2021); 12-month PT $815 vs the $751.67 price of 29 Oct 2025 → +8.4% upside. No PT change stated. Q3'25 showed the core still compounding — 3.5bn Family-of-Apps daily actives, 3bn Instagram monthly actives, 150m Threads DAU and time spent +30%/+10%/+5% y/y on Instagram, Threads and Facebook — with growing Advantage+ adoption and AI-driven ad efficiency supporting above-industry ad growth at scale. The overhang is the investment cycle: management raised both ends of the 2025 expense and capex guides, so GS now models ~$117.2bn of total GAAP expenses against the $116-118bn guide and ~$71.1bn of capex against $70-72bn, and introduced 2026 language of significantly faster expense growth and meaningfully larger capex growth. GS's estimates imply ~$400bn of cumulative capex from 2023 through 2027, a cycle it expects to persist at least 12-24 months while D&A, stock comp and technical-infrastructure leases keep GAAP expenses elevated for longer.

**Insight density:** Proprietary is the estimate reset and the cumulative-capex framing; the operating KPIs and the guidance are company restatement. No channel checks or survey.

**Data support:** Full GS model (income statement, balance sheet, cash flow), new-vs-old estimates with P/E of 26.3x/23.7x on 2025E/2026E, free cash flow turning negative across the forecast, and three-year price performance.

**Event context:** Written on the 30 Oct 2025 Q3'25 print, when the stock was near $752 and before the 2026 investment guide de-rated it below $600.

**Why 7:** the cleanest early statement of the capex-versus-core tension that later dominated the tape, but no proprietary operating data.

---

### 6/10 — Goldman Sachs, 26-09-13 · *The introduction of Muse AI* (10 pp)

**Why bullish/bearish:** Buy reiterated; PT $725, unchanged from 30-Jul-26. Price $648.03 (11 Sep close), +11.9% upside; no estimate revisions. Muse AI, Meta's first full-scale consumer agent app (iOS/Android, muse.ai, WhatsApp), runs on Muse Spark 1.3 for long-horizon agentic tasks, priced as subscription — Free (100m weekly tokens), Power $20/mo (500m), Maximum $100/mo (3bn). Each agent sits in an isolated Linux container (Muse Secure VM); Sentinel governs permissions; Stripe/Link enables agentic commerce. The mechanism GS sells is distribution over model quality: Meta's billions of DAU beat startups; META and GOOGL are the coverage names with distribution, intelligence and compute.

**Insight density:** The "conversation-to-action" framing is GS's own; tiers, Sentinel and Stripe are restated company disclosure, with no TAM model.

**Data support:** No new exhibits; reuses GS forecasts (2026E revenue $255.4bn, EPS $31.65; capex $138.4bn to $213.6bn in 2027E) and the 26.0x EV/GAAP EBIT plus 45.0x EV/FCF-SBC blend.

**Event context:** Written the evening of the 13 Sep launch, weeks after the litigation settlement; shares -13.7% over 12m, -25.8% vs the S&P. Catalysts: Connect 9/23, model releases.

**Why 6:** useful product detail, but no model, estimate or PT change.

---

### 6/10 — Bernstein, 26-08-27 · *All in all just another settlement in the Internet regulatory wall* (17 pp)

**Why bullish/bearish:** META Outperform, PT $800, unchanged here (prior: $850 → $800 on 2026-07-29). The ~$18B teen-addiction settlement with 48 states + DC/PR/AS/NMI removes Meta's largest legal overhang. Only ~70% ($12.7B) is unconditional; ~30% ($5.3B) is contingent on YouTube and TikTok matching. Meta books ~$10B expense in 3Q26 (~4% of 2026E revenue) ≈ NPV of the unconditional leg; guidance otherwise stands. Impact is modest: default 2-hour limit vs ~1 hour/day actual teen usage, teens <1% of revenue, FB/IG only, WhatsApp and AI untouched. Terms ratchet tighter if peers join (2h→1h, Night Mode 10pm→7am).

**Insight density:** No proprietary data — legal analysis plus a Big Tobacco precedent (Canada: $23B, 27 years, ~11% of the US MSA).

**Data support:** Ticker table, rating history, valuation method (50/50 2027e EV/Sales 6.7x + DCF). Residual exposure: >2,400 MDL suits, >10,000 claims, 1,200–1,300 school districts, Breathitt County ~$27M (Meta $9M).

**Event context:** Day after the 26 Aug settlement; next catalyst September Meta Connect.

**Why 6:** clean event read and damages map, but no proprietary work and no estimate change.

---

### 6/10 — J.P. Morgan, 26-07-12 · *AI outlook flips as Muse Spark 1.1 advances; incrementally positive but stay Neutral* (no local PDF)

> **Summary-only** — the PDF is not in the local library; the digest is derived from the zsxq summary.

**Why bullish/bearish:** Neutral maintained; 12-month PT $725, built on 21x 2027E GAAP EPS of $34.19. "Incrementally positive, but remain neutral" — the note's own title. Since the late-June low META has rebounded 23% (S&P 500 +3%) on three things: a better AI narrative, the Muse Spark 1.1 release, and the first signs of external AI monetization. Muse Spark 1.1 closes much of the agentic/coding gap to Anthropic, OpenAI and Google (several benchmarks above Gemini; the next model, Watermelon, is framed as GPT-5.5-class), and the public-preview Meta Model API is priced at roughly 25% of the leading labs — cheap enough to buy enterprise share at high incremental margin. Compute plans are ahead of the Street's model (≈7 GW in 2026 doubling to ≈14 GW in 2027), and the report cites SpaceX renting compute to Anthropic/Google at a $30-50/W premium versus a $10-20/W industry average as evidence that spare capacity can be monetized. The bear case is unchanged: capex of $142bn in 2026 (+104% y/y) and $202bn in 2027 (+42%) crushes free cash flow ($1.38bn in 2026, −$18.8bn in 2027), and the monetization is unproven — JPM wants evidence on internal model penetration, developer/enterprise adoption and LLM share shifts before upgrading.

**Insight density:** Consensus-plus — a dated, quantified framing of the AI debate with JPM's own capex/consensus math; the original datapoint is the third-party compute-rental pricing comparison, not proprietary channel work. The Neutral stance is itself informative: it is the "before" of JPM's 10 Sep 2026 upgrade to Overweight, $820.

**Data support:** None verifiable — this digest is derived from the zsxq Chinese summary (translated highlights, ~2,500 characters covering the model, monetization, financial and risk sections). The PDF is not in the local library (`local_path` is null, `has_pdf` false), so no exhibits, model or estimates pages could be read; treat every number here as summary-sourced.

**Event context:** Written after the late-June AI-sentiment trough and around Muse Spark 1.1 (plus the Meta Model API preview), ahead of the 29 Jul 2Q26 print — a sentiment-inflection note rather than a print note.

**Why 6:** a real, dated META call on the exact axis (AI monetization) that JPM upgraded on two months later, and useful as the Neutral anchor in the dispersion table; marked down because the evidence is a summary, not a PDF, and one that a full read could not be checked against.

---

### 6/10 — Morgan Stanley, 26-05-17 · *How much capacity will $2tn of hyperscaler capex bring by '27?* (58 pp)

> No PT row: it shares `(META, Morgan Stanley, 2026-05-17)` with the headcount note, and the DB keeps one row per broker per day.

**Why bullish/bearish:** Overweight / Top Pick, PT $775 (~23x '27 P/E), unchanged; consensus mean $825.72. META has no separate call beyond the templated risk-reward page. META's own capex adds 1.4 GW (2025) / 1.9 GW (2026) / 3.4 GW (2027); grossing up its external compute deals with CRWV/NBIS/ORCL/GOOGL/AMZN, MS estimates an effective ~4 GW in '26 and '27 — notable for a company with no hyperscale business, so the return depends on productizing models (the "MetaClaw" agent) and monetizing 1P data. META capex: $72.2bn (2025) to $144.9bn (2026E) to $174.5bn (2027E); $85bn, or 55%, of '26 capex is forward build for '27+ GW, the most forward-loaded alongside AMZN/MSFT (GOOGL only 10%). Roughly 75-80% of incremental '27 capacity is still NVIDIA; ~$25bn/yr of hyperscaler opex grosses to ~3 GW.

**Insight density:** Proprietary bottom-up cost-per-GW and GW models built with MS's semis/hardware teams, not restated consensus.

**Data support:** GW-add and chip-mix charts, cost-per-GW by architecture, a META-specific capex exhibit (interactive model offered), risk-reward page.

**Event context:** Quiet patch — no META print; thematic note in the capex/ROIC debate.

**Why 6:** real META-specific GW/capex analysis, but META is one of four names.

---

### 6/10 — UBS, 26-04-21 · *US Internet 1Q26 online-advertising preview: navigating the air pocket* (65 pp)

**Why bullish/bearish:** Sector preview covering six names; META remains Buy with the price target raised to $908 (prior $872) on 26x 2Q27E-1Q28E GAAP EPS of $34.93. META is roughly 11 of 65 pages (p20-30), not a standalone note. Meta was the largest budget outperformer in the eight ad-expert checks: META budgets +11.5% y/y in 1Q26 versus 10.8% expected, Instagram beating by 293bps, credited to Reels plus Advantage+ (GenAI creative, Andromeda ranking). 2026 revenue is trimmed ~1% for macro, but EPS is unchanged for 2026 and +3% for 2027 on lower D&A; ~$50B of annual ad-dollar growth is modelled. Job-postings and Sensor Tower pages are META-specific; other sections are not META evidence.

**Insight density:** Proprietary UBS Evidence Lab technical job postings (33% above 1Q18) and expert/sensor data; the five-pillar thesis is restated.

**Data support:** Figures 1, 44-71 spanning revision tables, quarterly models, UBS-vs-consensus, ad checks, upside $1,088/downside $514.

**Event context:** 1Q26 preview before the 29 Apr print; META at $671 (20 Apr 2026).

**Why 6:** real META evidence, but one section of a broader preview.

---

### 6/10 — Morgan Stanley, 26-03-15 · *AI efficiency winds starting to pick up* (10 pp)

**Why bullish/bearish:** Overweight; PT $825 (11x '27 EBITDA, implying ~23x '27 EPS; PT averages a multiples valuation $806 and DCF $844 at 8% WACC / 3% terminal growth). Weekend media reports that META plans to cut ~20% of staff (~16k) could yield $3bn-$13bn of savings at $200k-$800k per head, i.e. 3-11% upside to MS's '27 EBIT (text says 5-10%) — and headcount costs are ~80% of META's opex ($131bn of $165bn total opex in '26E). Management's own line: META saw a "30% increase in output per engineer since the start of 2025, with the majority of that growth coming from adoption of agentic coding." MS frames this as offsetting accelerating GenAI capex/opex, lifting the near-term EPS floor while preserving long-term torque. Bear/base/bull PTs $500/$825/$1,100 on base '27 EPS of $36.63.

**Insight density:** No proprietary data — it aggregates media reports (XYZ -40%, ORCL, ADSK -7%, AMZN) and MS's own opex-per-head math, cautioning against using the ~$1.2mn ex-D&A opex per employee as the savings rate.

**Data support:** Three exhibits — headcount-cost build, RIF sensitivity table, full multiples-plus-DCF PT build.

**Event context:** Triggered by a weekend press report on job cuts; no print, no deal.

**Why 6:** META-specific scenario math, but rumor-driven and thin on new information.

---

### 5/10 — Morgan Stanley, 26-08-12 · *How could open-weight models impact GenAI ROIC?* (18 pp)

**Why bullish/bearish:** Overweight / Top Pick; PT $775, "~23X P/E on the average of our $34/$35 EPS in 27/28" (bull $1,000, bear $450) vs $599.10 on 12-Aug-26 → +29.4%. Consensus mean $755.23, range $580–$1,000. No revision shown. Open-weight models — Meta's Muse Spark 1.2 shipped the week before, and Muse Spark 1.1 blended pricing ($1.58/mn tokens) feeds the model-layer build — cut token prices, so throughput and differentiation decide ROIC; MS's base case (~$1.75/mn tokens, 2,000–3,500 tokens/sec/GPU on GB300) still yields ~20–60% ROIC on 1GW of owned GB300. The META ask: "watch what Meta continues to ship in its new suite of Muse models" — Meta's own pricing is the pressure being measured. Standing page keeps ~27% '26 META ad-revenue growth.

**Insight density:** Genuinely proprietary unit economics (interactive GenAI ROIC models, pricing/throughput ranges) — but the ROIC grids are AMZN/GOOGL; META supplies the pricing datapoint, not the analysis.

**Data support:** Exhibits 1–3 (cost stack, revenue/GW, ROIC grid at 60–69% NOPAT margins, 21–34% ROIC), price-target history, META risk-reward page.

**Event context:** A reaction note to Muse Spark 1.2 and the 11-Aug ROIC feedback piece; no META print.

**Why 5:** the clearest read on how Meta's own Muse pricing pressures GenAI ROIC, but no META P&L work.

---

### 5/10 — Bernstein, 26-07-01 · *Meta's will-they-won't-they neocloud ambitions* (15 pp)

**Why bullish/bearish:** No new META call. META appears in the ticker table with the standing Outperform, PT $850 (30 Jun 2026 close $563.29, -42.5% relative; 2026E EPS $33.54, 2027E $37.04; 16.8x/15.2x EV/EBITDA); the body states "We rate Meta Outperform." This is a CoreWeave quick take (Underperform, PT $67). Its META claim is that reports of Meta developing a cloud-infrastructure business are not a META problem — they give investors "some semblance of rationality around the cadence and ROIC of the spend, that's been a major hangup over recent stock performance." Supporting scale: Meta sits on ~20GW of data-centre footprint today with ~14GW more coming online, and its $35.2B of CoreWeave contracts (over a third of CRWV's backlog; about half including Microsoft's ~$14B) come from a customer that will compete at renewal. Zuckerberg had already put reselling excess compute "on the table"; Google is reportedly throttling Meta's capacity.

**Insight density:** Proprietary Bernstein Global Data Center Model GW build, but nothing proprietary on META's P&L.

**Data support:** Five exhibits (Meta capacity 2020-30E, CRWV deal table, hyperscaler GW, new supply, leased/owned split) plus META valuation methodology (7x 2027E EV/Sales + DCF).

**Event context:** Reactive — published the day the neocloud news hit.

**Why 5:** two useful META capex datapoints and the ROIC-narrative argument, but META is a supporting character.

---

### 5/10 — UBS, 26-07-01 · *Does the excess-capacity sale reduce EPS-compression risk?* (13 pp)

**Why bullish/bearish:** Buy reiterated, price target unchanged at $865 (26x, unchanged); no estimate revisions pending company confirmation. Price $601.85 (1 Jul 2026). Bloomberg reported Meta may sell raw compute capacity or access to hosted AI models. UBS argues this is not new — Zuckerberg floated both on 27 May 2026 and 29 Oct 2025 — and that either option attacks the "duration problem": selling capacity or model access yields revenue sooner than waiting for Meta Business Agents and Meta AI to scale, easing fears that 2027 EPS stays flat or compresses versus 2026 ($32.67 vs $32.98 modelled). META traded at 17x 2027 GAAP EPS before the article.

**Insight density:** Mostly a pragmatic rebuttal of a "pivot" worry; the EPS-duration argument and the 17x datapoint are the only original content, quotes are restated.

**Data support:** Cover highlights table (revenue, EPS, net debt to 12/30E), valuation metrics, price-target history ($865 since 30 Apr 2026); no new model.

**Event context:** Bloomberg news item; stock near the low end of a $790.00-525.72 52-week range.

**Why 5:** short, no fresh numbers, thesis and quotes already public.

---

### 5/10 — HSBC, 26-04-21 · *AI-driven revenue growth can continue* (9 pp)

**Why bullish/bearish:** Maintain Buy, target price USD905, unchanged (previous target USD905), +31.4% upside. Methodology 25x FY26e P/E on FY26e non-GAAP EPS of USD38.5, less a 5% regulatory discount (implied USD953). Price USD688.55 at 17 Apr 2026. Pre-Q1 preview. HSBC frames the Q4 guide — Q1 revenue USD53.5-56.5bn (+26.4-33.5% y/y, 4% FX tailwind) vs Visible Alpha consensus USD55.4bn (+31%), FY26 expenses USD162-169bn (cons USD163.9bn), capex USD115-135bn (cons USD125.2bn), operating income above FY25a, tax 13-16%. HSBC sits below consensus: Q1 revenue USD54,915m (-1.0%), advertising USD53,199m (-1.9%), GAAP EPS USD6.42 (-3.6%); FY26 revenue USD249,908m, operating income USD85,993m (+3.3%), capex USD122,455m. It flags Muse Spark as Meta's most powerful closed-source model, the USD21bn CoreWeave deal through 2032, AMD's up-to-6GW Instinct deployment and the Broadcom MTIA co-design through 2029, against OpenAI's reported USD100bn 2030 ad ambition.

**Insight density:** The consensus-revision analysis since 7 February (2026e revenue -0.3%, operating income -1.4%, EPS -1.7%, capex +1.3%) is the only differentiated work; HSBC's own estimates are untouched.

**Data support:** Four consensus-change charts, HSBCe-vs-consensus table, valuation table, full statements.

**Event context:** Written ahead of the 29 April Q1 print; no new catalyst priced in.

**Why 5:** a short pre-earnings preview with unchanged numbers and a restated bull case.

---

### 5/10 — Bernstein, 26-03-16 · *The world's first AI-oriented organization* (17 pp)

**Why bullish/bearish:** Outperform, PT $900, unchanged (ticker table dated 13 Mar 2026, META $613.71 → +47%). Only four pages carry content; thirteen are disclosure and rating-history boilerplate. An operating-model argument, not a numbers argument. Reports of a ~20% headcount cut are read as an AI-driven re-org rather than bloat-trimming, following a 50:1 employee-to-manager stretch target versus the 7-15:1 industry norm. Bernstein estimates $2-4B of 2026 cost savings and $5-8B in 2027, worth 3-5% EPS upside in 2026 and 4-7% in 2027 — but assumes Meta pockets them, which they doubt, expecting redeployment into AI. The bigger prize is the second "AI winner" path: embedding AI deep enough in the core that the moat widens beyond dispute.

**Insight density:** Modest proprietary work — open-role technical mix scraped from career sites (Meta 70% technical vs Anthropic 46%, OpenAI 56%, Google 68%) and revenue/capex-per-employee series since ChatGPT launched.

**Data support:** Three exhibits, no model or valuation update; one Zuckerberg quote about projects now needing a single talented person.

**Event context:** Written around press reports of the job cuts, ahead of anything testable; no print.

**Why 5:** sharp org-level datapoints and explicit EPS math, but a short thematic think-piece with an unchanged PT.

---

### 5/10 — HSBC, 25-10-21 · *Fast-growing ad revenue boosted by AI* (8 pp)

**Why bullish/bearish:** Maintain Buy; target price $905, unchanged (previous target $905). Share price $716.92 at 17 Oct 2025, +26.2% upside. The TP applies 26x to 2026e non-GAAP EPS of $36.79 and takes a 5% regulatory discount off the implied $952. A pre-print preview — Q3'25 results were due 30 Oct. HSBC forecasts third-quarter revenue of $48,526m, 2.0% below Visible Alpha consensus of $49,526m, and diluted GAAP EPS of $6.60 versus $6.70 consensus. The mechanism is scale: AI leverage over first-party signals from a 3.4bn user base, which HSBC says carries it to 31.6% of the global digital ad market by 2030e from 25.2% in 2025e, via mid-single-digit impression growth and low-double-digit pricing. Smart glasses and WhatsApp monetisation are the optionality, and the report expects Meta's development of a computing platform via smart glasses.

**Insight density:** Proprietary inputs are the forecast drivers (2026e Family ARPP $61.3, ad revenue $220.0bn) and the 2030e share build; company guidance and consensus are restated. Rating and TP are unchanged, last set 15 Sep 2025.

**Data support:** Q3'25 preview table (revenue, expenses, operating income, EPS, capex versus guidance and consensus), consensus-change charts since Q2, full financial statements, valuation table.

**Event context:** Published ahead of the Q3'25 print; 52-week range $484.66-$790.00 with the stock at $716.92.

**Why 5:** a useful guidance recap, but it adds little beyond consensus and carries no new valuation work.

---

### 5/10 — J.P. Morgan, 25-09-18 · *Glasses move a step closer to the next form factor of computing* (17 pp)

**Why bullish/bearish:** Reiterate Overweight; Dec-26 PT $875, unchanged (no revision). Basis ~25.5x 2027E GAAP EPS of $34.17, DCF-supported (~12% WACC, ~66x terminal FCF multiple, +8% terminal growth); META stays a Best Idea. Price $775.72 on 17 Sep 25. Meta Connect showed AI glasses moving toward the next computing form factor — Meta Ray-Ban Display, the first AI glasses with a neural interface (Meta Neural Band EMG wristband), six hours mixed use/30 hours total, shipping 9/30 at $799; next-gen Ray-Ban Meta at $379 with ~2x battery (up to eight hours) and 3K video; Oakley Meta Vanguard $499 (Oct 21) and HSTN $399; Horizon Studio/Engine/TV. Millions of Ray-Ban Meta units sold within a 10+ year investment cycle, yet JPM still models Reality Labs losses of $19B in 2025 and $21B in 2026 plus capex of $71B 2025 (+90%, $66-72B guide) and $105B 2026 (+49%).

**Insight density:** Largely restatement of keynote specs and pricing; proprietary only in the RL loss/capex path, the 25.5x multiple and DCF assumptions. No estimate changes.

**Data support:** No new exhibits — income statement and summary model pages only.

**Event context:** Meta Connect 2025 keynote; stock +32.5% YTD and +44.6% over 12m, 52-week range $796.25-$479.80 — a momentum print with no numbers moved.

**Why 5:** competent event recap, but no change to estimates or PT and little incremental analysis.

---

### 4/10 — Morgan Stanley, 26-07-28 · *Where are we trading now: Micro vs AI vs Macro* (16 pp)

**Why bullish/bearish:** None — META carries no rating or price target in the body. It is a comp-sheet row; the coverage list shows Overweight (as of 20-Mar-23) with price $593.87 on 27-Jul-26 and no PT printed. Weekly drawdown review — Internet -7%, led by META and GOOGL at -7.9%/-7.8%; META +6.7% over one month but -9.8% YTD. Valuations as of 24-Jul-26: 18x '27 EPS, -12% vs its TTM average (AMZN 20x/-25%, GOOGL 21x/-19%); NTM EV/EBITDA 9.4x vs 12.4x (2-yr) and 12.0x (3-yr) averages, i.e. -24%/-22%; on MS's SBC-as-cash adjustment '26 EV/EBITDA rises 10.2x → 12.1x (+19%); short interest 1.7%, third-lowest in the list.

**Insight density:** Restated FactSet/Compustat market data plus MS's own SBC-as-cash re-based multiples — no proprietary META fieldwork.

**Data support:** ~40-name comp sheet, performance and short-interest exhibits, Exhibit 4 (AMZN/GOOGL/META vs history), SBC exhibits 8–11, interactive comp sheet; no META model.

**Event context:** Written into a -7% Internet week as the 2Q26 tape settled — positioning/market context, not a META trigger.

**Why 4:** META gets its own valuation column and the "cheapest vs own history" framing, but no argument.

---

### 4/10 — Bernstein, 26-05-20 · *Data-center project pipeline (April '26): capacity, construction, cancellations* (41 pp)

**Why bullish/bearish:** META appears only as a hyperscaler capex datapoint in the inaugural monthly data-center capacity tracker. In April Meta broke ground on 1.1 GW of new capacity, the most of any hyperscaler (vs Amazon 534 MW); Meta is 27% of hyperscaler capacity under construction (Amazon 32%, Google 23%, Microsoft 14%) and 19% of hyperscaler active capacity (~5 GW); Meta owns the vast majority of the 4.5 GW of hyperscaler behind-the-meter capacity under construction. Offsetting: Meta added -0.5 GW to pipeline this month and holds 10% of hyperscaler pipeline vs Amazon's 45%.

**Insight density:** Genuinely proprietary — first instalment of an Aterio-sourced monthly build tracker (pipeline 294.9 GW, +14 GW M/M, +214% Y/Y; 58.6 GW under construction; 32.4 GW stranded; 114.9 GW BTM), with an electrical TAM build (PWR $3,981B, VRT $914B, SU.FP $787B, ETN $690B).

**Data support:** 68 exhibits and a dashboard; no META model or earnings exhibits.

**Event context:** Quiet patch — a calendar tracker, no Meta-specific trigger.

**Why 4:** skim the three META datapoints (1.1 GW starts, 27% construction share, BTM lead); the ticker is otherwise a comp row.

---

### 3/10 — Morgan Stanley, 26-05-27 · *How much revenue per GW could the capacity ahead generate?* (21 pp)

**Why bullish/bearish:** Overweight / Top Pick; PT $775 (bull $1,000, bear $450) vs $612.34 on 26-May-26 → +26.6%. No revision shown; MS sits below the $822.60 consensus mean (range $614–$1,015). The report's model (bottom-up cost/GW across 9 chip generations; ~14GW/20GW incremental hyperscaler capacity in '26/'27; $11–14bn incremental revenue per incremental GW) covers AWS/Google Cloud only — META is absent. Its page carries the META thesis: ~28% ad-revenue growth in '26 as AI lifts Reels engagement/monetization, at ~23x '27 P/E via DCF (~8% WACC, ~3% terminal).

**Insight density:** Proprietary for hyperscalers (capacity models, backlog files, capacity deals at ~$20bn+/GW); restated standing prose for META.

**Data support:** Six hyperscaler exhibits; META gets bull/base/bear, MS-vs-consensus FY26e (revenue $256.7bn vs $253.1bn; EPS $32.83 vs $32.85), ownership and positioning.

**Event context:** Quiet patch; no META print, deal or regulatory trigger.

**Why 3:** META is a bolted-on Top Pick page inside someone else's capex argument.

---

### 3/10 — Morgan Stanley, 26-05-19 · *Large-cap institutional ownership 1Q26: under-ownership narrows* (71 pp)

**Why bullish/bearish:** META carries the same Overweight / Top Pick and $775 PT; this note adds no new META call (consensus mean $825.72; $775 equals +26.8% against the 18-May close of $611.21). In this 71-page 13F study META appears in four exhibits only. Its active-institutional weighting versus its S&P 500 weight was -0.15% exiting 1Q26 — only marginally under-owned — after a 19bp q/q improvement, the fourth-largest of the 28 names tracked. Mega-cap tech under-ownership narrowed to -125bp from -137bp at 4Q25; META now sits outside the heavily under-owned group (NVDA -2.39%, AAPL -2.32%, MSFT -1.86%, AMZN -1.24%). Since MS's quant work finds low active ownership versus the S&P 500 predicts relative outperformance, META's technical tailwind has largely faded. The templated risk-reward page repeats 55.8% active ownership, HF sector long/short 2.7x (from 2.8x), HF net exposure 12.9% (13.9%).

**Insight density:** Proprietary 13F data on the top ~100 active managers, 1Q09-1Q26, with a significance test — but nothing META-idiosyncratic.

**Data support:** Four ownership exhibits plus boilerplate META risk-reward pages; no META model.

**Event context:** Quiet patch, the quarterly ownership update after 1Q26 filings.

**Why 3:** META is a data point in a positioning study, not research on the name.

---

### 3/10 — Morgan Stanley, 26-03-12 · *What does ChatGPT's agentic pivot mean for the ecosystem?* (25 pp)

**Why bullish/bearish:** Overweight; PT $825 (bull $1,100, bear $500) vs $654.86 on 12-Mar-26 → +26.0%. Consensus mean $852.79, range $676–$1,144. No revision, and the note is not a META call. Defensive read-across from ChatGPT's pivot to link-out. AlphaWise's tracker shows Meta AI used by 19% of US respondents in Feb-26 (22% in Oct-25) against ChatGPT 46%/Gemini 32%, with only ~5% of respondents buying on a Meta AI recommendation vs 18% on ChatGPT. Facebook/Instagram/Pinterest hold ~13–16% as the first app for product research or price comparison vs Google's 56–57%; MS argues those incumbents keep engagement growing off far larger bases, so they are harder to disrupt. The standing META page shows MS '26e EPS $32.23 vs mean $29.62 — above the Street — on revenue $260.3bn vs $250.1bn.

**Insight density:** Proprietary AlphaWise recurring survey (Oct-25→Feb-26 waves; n not printed); the META datapoints are survey side-effects, not META research.

**Data support:** Ten exhibits (adoption, purchase rates, trust reasons, take-rate comparison) plus the full META risk-reward page.

**Event context:** Written around ChatGPT's agentic pivot; META is a bystander.

**Why 3:** useful Meta AI adoption and incumbent-durability datapoints, no META thesis.

---

### 3/10 — Bernstein, 26-03-05 · *US Internet: AI bear narratives compound, but is a floor forming?* (17 pp)

**Why bullish/bearish:** META Outperform, PT $900 (ticker table; META $667.73 on 4 Mar 2026). No revision — this is the standing call carried through a basket note. A basket-level "is a floor forming?" note, not a META argument. Median internet EV/NTM EBITDA compressed 16x (Nov) to 11.8x, near prior troughs; META itself barely de-rated (13.7x to 13.2x, -3%) and screens as quality: 2027E GAAP P/E 19.4x on ~17% 2026-28 EPS CAGR, PEG 1.1x, and META tops the basket on 2026 revenue revisions (+6% vs a 2% median). The offset is capex: a 2027E FCF multiple of 85x for META (AMZN 89x, GOOGL 97x) — Bernstein wants AI ROI and FCF re-acceleration before mega-caps re-rate.

**Insight density:** Consensus screens and relative-multiple work; no proprietary META data.

**Data support:** Ten exhibits — multiple-compression table, GAAP P/E/PEG table, EV/Sales vs growth+margin regression (R² 81%), FCF revisions, 2027E FCF multiples, and a 13-name ticker table (META O $900; 2026E EPS 23.49, 2027E 30.87).

**Event context:** Quiet patch after the January-February derating (median name -19% vs S&P) — a sentiment call, not a print reaction.

**Why 3:** META is a row in basket valuation tables; the note is about the sector's AI de-rating.

---

### 2/10 — Morgan Stanley, 26-07-14 · *Where are we trading now: heading into EPS, focused on AI ROIC* (15 pp)

**Why bullish/bearish:** Overweight (since 03/20/2023); no price target; coverage price $669.21 (07/10/26). META led the week +14.8% in a flat Internet tape, and the note's entire META comment is that it and AMZN, "+15%/+1%", led — the driver is never explained. Valuation is the other hook: 20x '26 EPS, -15% versus TTM average, 10.7x NTM EV/EBITDA, -14%/-11% versus 2-/3-year averages. The header promises "Focused on AI ROIC" yet META's AI capex and free cash flow go unanalysed — the comp sheet shows FCF yield of just 0.8%/0.9%.

**Insight density:** Nothing proprietary on META; the ROIC framing stays thematic and sector-level.

**Data support:** Comp-sheet row ($669.21, $1.72tn, 11.4x/9.1x EV/EBITDA, 20.4x P/E, 1.6% short interest), SBC-as-cash bridge 11.4x to 13.5x (+19% versus +36% median), price-performance tables.

**Event context:** Pre-2Q-earnings ("Heading into EPS"), but with no META print preview or estimate revision.

**Why 2:** META's +14.8% week and FCF collapse are the only usable facts.

---

### 1/10 — Morgan Stanley, 26-07-21 · *Where are we trading now: entering 2Q earnings* (15 pp)

**Why bullish/bearish:** Overweight (since 03/20/2023); no price target; coverage price $645.85 (07/20/26). META fell 3.5% in a -4% Internet week, and the standing "cheap" framing is the whole META argument: 20x '26 EPS, -16% versus TTM average; 10.3x NTM EV/EBITDA, -17%/-14% versus 2-/3-year averages. Titled "Entering 2Q Earnings", the note still says nothing about META's print, guidance or AI capex. The one genuinely new META fact is a cut: '27 EPS $34.16 to $32.99, pushing 2027 FCF yield to NM.

**Insight density:** Restated consensus; no proprietary META data, no preview of the coming quarter.

**Data support:** Comp-sheet row ($646.01, $1.66tn, 11.0x/8.7x EV/EBITDA, 19.9x P/E, 1.6% short interest), SBC bridge 11.0x to 13.1x (+19% versus +36% median), performance tables.

**Event context:** Written days before META's 2Q print — the closest thing to event context in the set — yet with no META-specific preview.

**Why 1:** META is a row plus a consensus estimate trim; the earnings preview is absent.

---

### 1/10 — Bernstein, 26-07-21 · *Digital ads 2Q26: AI identity crisis (PDF corrupt at source)* (no local PDF)

> **Corrupt at source** (no xref/`%%EOF`; only disclosure pages 36-38 survive) — score 1, no call readable.

**Why bullish/bearish:** Not readable from this file — the PDF is truncated at source (no xref, no `%%EOF`; the zsxq server re-download is byte-identical), leaving only disclosure pages 36-38 intact. No quotable META rating/PT. Context only: the 1 July CoreWeave note carries META Outperform/$850, and the 20 Aug note's rating-history chart dates that $850 to 30 Apr 2026, still live on 21 July. Unrecoverable — all research pages are blank; running headers identify the 2Q26 digital-ads preview ("AI Identity crisis", Mark Shmulik, 21 July 2026).

**Insight density:** Cannot be assessed.

**Data support:** None surviving.

**Event context:** Pre-print sector preview, a week before META's 2Q26 print (PT cut to $800 on 29 Jul).

**Why 1:** corrupt file; nothing on META readable.

---

### 1/10 — Morgan Stanley, 26-06-09 · *Where are we trading now: AI hardware vs AI software flow* (15 pp)

**Why bullish/bearish:** Overweight, held since 03/20/2023. The note carries no META price target — only the rating and the 06/08/26 price, $585.39. No argument is made about META itself; the case is purely relative. It fell 6.2% on the week versus GOOGL -3.1% and PINS +6.8%, and at 18x '26 EPS sits at the widest discount of the trio, -27% versus its TTM average (AMZN 26x/-19%, GOOGL 25x/-2%). Exhibit 4 repeats it implicitly: 9.7x NTM EV/EBITDA is -23%/-20% versus 2-/3-year averages while GOOGL trades at a +26% premium.

**Insight density:** Restated consensus — no channel checks, trackers or survey; estimates unchanged at $32.83/$34.16, all inputs FactSet.

**Data support:** One comp-sheet row ($593.00, $1.52tn cap, 10.1x/8.1x EV/EBITDA, 0.9%/1.0% FCF yield, 18.1x P/E, 1.5% short interest), the SBC-as-cash bridge (10.1x to 12.0x, +19% versus +36% digital-media median), performance tables.

**Event context:** Quiet patch — a pure flow-and-multiple weekly, no print, deal or regulatory hook.

**Why 1:** META is a table row in a note about AI hardware-versus-software flows.

---

### 1/10 — Morgan Stanley, 26-06-03 · *Where are we trading now: into the summer of AI* (15 pp)

**Why bullish/bearish:** Overweight (since 03/20/2023); no price target disclosed, coverage-list price $597.63 (06/02/26). META is the week's leader at +3.6% (GOOGL -0.7%; RDDT +24.2% on the SHOP integration), yet the note draws no conclusion. Its only META framing is valuation: 19x '26 EPS, -23% versus TTM average, and 10.4x NTM EV/EBITDA against 2-/3-year averages of 12.6x/12.1x (-18%/-14%). That positions META as the cheap mega-cap next to GOOGL on 18.1x and a +31% premium, but it is never argued in prose.

**Insight density:** Consensus and FactSet arithmetic only; zero proprietary META work — no ad checks, no Reels/WhatsApp data.

**Data support:** Comp-sheet row ($632.51, $1.62tn, 10.7x/8.6x '26/'27 EV/EBITDA, 0.8%/1.0% FCF yield, 19.3x P/E, 1.5% short interest), SBC bridge 10.7x to 12.8x (+19% versus +36% median), sector performance tables.

**Event context:** Quiet patch; the "Into the Summer of AI" title is a sector-flow theme, with no META catalyst.

**Why 1:** META appears only in exhibits and a single relative-multiple line.

---

## Disagreement flags — where the set actually splits

> ⚠️ **Goldman Sachs $725 (13 Sep) vs UBS $865 (1 Jul) vs Bernstein $800 (20 Aug) — a 19% spread on fair value at the same share price.** GS has cut its multiple twice (26x → 24x → 23x on 2027E) and its PT from $835 to $725, because management raised FY26 capex to $130–145bn, lifted 2027-28 spend ~14% and gave **no long-term capital plan** — GS's word for the gap is a "show me". UBS and Deutsche Bank read the same spending as *optionality*: if Meta rents out excess capacity, EPS compression risk falls (UBS $865, DB $810 → $800). Bernstein sits between the two, holding $800 on 22x 2027E with the line "still need to see it to believe it, but risk-reward remains attractive". Do not average these; the split *is* the signal, and the date on each matters more than the level.

> ⚠️ **J.P. Morgan reversed itself: Neutral $725 (12 Jul) → Overweight $820 (10 Sep).** The 12 Jul note kept Neutral on 21x 2027E GAAP EPS of $34.19 while conceding the AI narrative had flipped; the 10 Sep note upgraded on 23x **2028E** EPS of $35.44 as Muse shipped and the Model API opened. That is a two-month round trip on the same evidence base — a reminder that the sell side's *rating* lagged the *product*.

> ⚠️ **The neocloud is simultaneously ROIC-validating and unfunded.** Bernstein (1 Jul) argues reports of a Meta cloud business give investors "some semblance of rationality around the cadence and ROIC of the spend"; DB quantifies $9–30bn of 2027 revenue at $10–15bn per GW and 75% sold; Morgan Stanley calls it worth $2.97 of its $34.59 '28 EPS; Goldman labels the full hyperscaler-API version a "show me" and keeps it outside its base case. Same news, four different weights — the honest read is that the option is real and its size is not knowable yet.

> ⚠️ **Nobody is a bear.** 49 of the 50 persisted calls are Buy / Overweight / Outperform (the 50th is J.P. Morgan's Neutral, 12 Jul), and the lowest PT in the book — $725, Goldman Sachs, 13 Sep — still implies **+11.9%** from its own $648.03 report-date close. That is a one-sided ratings distribution against a stock that fell from ~$800 to ~$540 between January and July.

> ⚠️ **The price-target trend is down while the narrative is up.** Morgan Stanley: $825 (Mar) → $775 (Apr onward). Bernstein: $900 → $850 (30 Apr) → $800 (29 Jul). Goldman: $835 → $830 → $725. Deutsche Bank: $920 → $810 → $800. UBS: $872 → $908 (Apr, the top of the range) → $865. Estimate cuts, not rating cuts, are where the AI-spend debate actually shows up.

---

## What renders on `/research-lens` — and what does not

The lens reads `price_targets` with `ORDER BY report_date DESC LIMIT 18`, so with **50 META rows only the 18 most recent render** (META's 18 run from 2026-09-13 back to 2026-06-02). The other **39 digests below never show on the page** — they are in `reference/report_digests.json` and in this file, but the page cannot reach them:

- **2026-07-28** — Morgan Stanley — *Where are we trading now: Micro vs AI vs Macro* (4/10) — *no PT row*
- **2026-07-21** — Morgan Stanley — *Where are we trading now: entering 2Q earnings* (1/10) — *no PT row*
- **2026-07-21** — Bernstein — *Digital ads 2Q26: AI identity crisis (PDF corrupt at source)* (1/10) — *no PT row*
- **2026-07-14** — Morgan Stanley — *Where are we trading now: heading into EPS, focused on AI ROIC* (2/10) — *no PT row*
- **2026-06-09** — Morgan Stanley — *Where are we trading now: AI hardware vs AI software flow* (1/10) — *no PT row*
- **2026-06-03** — Morgan Stanley — *Where are we trading now: into the summer of AI* (1/10) — *no PT row*
- **2026-05-28** — Deutsche Bank — *Subscription rollout creates the first clear consumer-AI monetization layer* (7/10)
- **2026-05-27** — Morgan Stanley — *How much revenue per GW could the capacity ahead generate?* (3/10)
- **2026-05-20** — Bernstein — *Data-center project pipeline (April '26): capacity, construction, cancellations* (4/10)
- **2026-05-19** — Morgan Stanley — *Large-cap institutional ownership 1Q26: under-ownership narrows* (3/10)
- **2026-05-17** — Morgan Stanley — *Headcount reductions and the neocloud backup optionality* (8/10)
- **2026-05-17** — Morgan Stanley — *How much capacity will $2tn of hyperscaler capex bring by '27?* (6/10) — *no PT row*
- **2026-04-30** — Bernstein — *US Internet mega 1Q26 earnings: more similar than different* (9/10)
- **2026-04-30** — Morgan Stanley — *Internet 1Q26: GOOGL, AMZN and META surprises and learnings* (8/10)
- **2026-04-30** — UBS — *Product development benefits still ahead of us* (8/10)
- **2026-04-30** — Goldman Sachs — *Q1'26 review: core outgrows the industry, long-term AI visibility needed* (7/10)
- **2026-04-27** — Bernstein — *Digital ads 1Q26: it's good to be big, right?* (8/10)
- **2026-04-21** — UBS — *US Internet 1Q26 online-advertising preview: navigating the air pocket* (6/10)
- **2026-04-21** — HSBC — *AI-driven revenue growth can continue* (5/10)
- **2026-04-20** — BofA — *1Q26 preview: expecting a beat, macro sensitivity and AI cost benefits* (7/10)
- **2026-04-18** — Deutsche Bank — *Early sparks of Meta superintelligence (translated note)* (8/10)
- **2026-04-14** — Morgan Stanley — *Key themes and numbers into GOOGL/META/AMZN earnings* (8/10)
- **2026-04-09** — Morgan Stanley — *Meet Meta's Muse* (8/10)
- **2026-04-08** — Bernstein — *Will Muse Spark restore investor belief in the AI story?* (7/10)
- **2026-03-22** — Goldman Sachs — *Framing recent news reports against our strategic-focus view* (8/10)
- **2026-03-16** — Bernstein — *The world's first AI-oriented organization* (5/10)
- **2026-03-15** — Morgan Stanley — *AI efficiency winds starting to pick up* (6/10)
- **2026-03-12** — Morgan Stanley — *What does ChatGPT's agentic pivot mean for the ecosystem?* (3/10)
- **2026-03-05** — Bernstein — *US Internet: AI bear narratives compound, but is a floor forming?* (3/10)
- **2026-01-29** — Goldman Sachs — *Q4'25 review: AI impact in the core, investments still scaling* (8/10)
- **2026-01-29** — UBS — *Stronger signals of AI benefits to emerge in 2026* (8/10)
- **2026-01-29** — J.P. Morgan — *Major AI acceleration — revenue and expense acceleration* (7/10)
- **2026-01-28** — Citi — *1st impression: ad revenue +23% y/y ex-FX; '26 capex higher than expected* (7/10)
- **2026-01-27** — Bernstein — *Investment memo: pumping AI iron* (9/10)
- **2025-12-11** — Morgan Stanley — *3 catalysts to outperformance and the bull case in '26* (9/10)
- **2025-10-30** — Goldman Sachs — *Q3'25 review: strong Family-of-Apps, investment commentary overhangs* (7/10)
- **2025-10-21** — HSBC — *Fast-growing ad revenue boosted by AI* (5/10)
- **2025-10-13** — Citi — *IG/Reels ad-load tracker: 3Q reaches 27.1%, +230bp q/q* (8/10)
- **2025-09-18** — J.P. Morgan — *Glasses move a step closer to the next form factor of computing* (5/10)

Two further rendering caveats: the Goldman 2Q'26 review (`814512485518222`) is dated **2027-07-30** because the source filename ends `-270730.pdf` (a typo — the zsxq `create_time` is 2026-07-30), so it takes the newest slot in the page's 18-row window and its report-date price is null; and the J.P. Morgan 12 Jul note (`584248885824284`) is **summary-only** — it renders, but there is no PDF behind it to open.

---

## How the data is stored (as of 2026-09-15)

**Two databases, one join key.** The Research Lens page reads from both.

### 1. `db/zsxq.db` — the PDF library

One row per downloaded PDF in **`pdf_files`** (`file_id` primary key, `name`, `topic_title`, `summary`, `local_path`, `bank`, `page_count`, `tickers`, `claude_rating`, `ocr_text`, `create_time`), plus the FTS5 trigram index **`pdf_files_fts`** that the META scan ran against. The DB stores only the pointer to the bytes — the PDFs live under `/Users/x/Downloads/zsxq_reports/<YYYY_MM_DD>/`.

### 2. `db/stock_price_target.db` — the calls

One row in **`price_targets`** per **(ticker × broker × report)** — META now has **50 rows** (was 17 at the start of this session: 33 inserted, 17 refreshed with the full-PDF read). Columns: `company_ticker`, `company_name`, `research_institute`, `rating`, `price_target`, `target_currency`, `catalyst`, `report_file_id` (join key to `pdf_files.file_id`), `report_pdf_filename`, `report_url`, `report_date`, **`report_date_price`** (the frozen point-in-time close), `report_date_market_cap`, `price_currency`, `upside_pct`, `created_at`.

Two unique keys guard against duplicates: `UNIQUE(company_ticker, research_institute, report_file_id)` and `uq_ticker_broker_date (ticker, broker, report_date)` — the second is why only one of the two Morgan Stanley 2026-05-17 notes surfaces. Writes go **only** through `scripts/persist_pts.py` → `stock_price_target_db.upsert_target()` (`--replace` used here, because a full-PDF read outranks a summary-only row); extraction rules live in `reference/pt_extraction.md`. **This DB matches `.gitignore`'s `*.db` and is not committed** — tonight's 50-row update exists on this machine only.

### 3. Per-report digests → `reference/report_digests.json`

Keyed by **stringified `file_id`**, one object per report with exactly `score`, `why`, `insight`, `data`, `event`. Loaded by `zsxq_viewer._report_digests()` (mtime-cached) and attached to each report in `_research_lens_reports()`. The file now holds **73 entries** — the 16 pre-existing GEV digests plus these 57 META ones; the merge preserved every pre-existing key. `db/stock_price_target.db` is gitignored, but this JSON is tracked, so the prose *is* versioned.

### 4. What is *not* stored — the price series

Daily OHLC is never persisted. The lens pulls the daily series **live from yfinance** on each page load for the window (earliest `report_date` − 14 days … latest + 14 days). Only the close **on** the report date is frozen into the row (`report_date_price`), which is what makes every `upside_pct` above auditable months later. The chart is therefore only as good as yfinance on the day you open it — and because the Goldman row is stamped 2027-07-30, the page asks yfinance for a window running out to Aug 2027 (the bars themselves stop at today), and that row plots no marker.

---

*All 56 readable META PDFs were read in full, one at a time, including two that needed OCR; the 57th is summary-only and the corrupt Bernstein file was scored as unreadable. Every rating, price target, report-date price and page count above was regenerated directly from `price_targets` and `pdf_files`.*
