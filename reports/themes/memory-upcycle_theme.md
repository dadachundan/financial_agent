# Memory / DRAM-NAND / HBM Up-Cycle

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en, zh

## Thesis

The 2025-2028 memory super-cycle is now the highest-conviction, longest-duration supply-demand mismatch in semis. JPMorgan's January 2026 framing — combined market cap of leading memory manufacturers approaching $1.0 trillion in 2026 and $1.5 trillion in 2027, with the memory TAM reaching $420 billion and a separately-sized $90 billion HBM TAM by 2027, plus a $220 billion AI-DRAM and $70 billion AI-NAND TAM by 2028 — anchors a structurally tight regime that no other semis vertical can match for visibility ([JPMorgan 2026 Storage Outlook via Tiger Brokers, 2026-01](https://www.itiger.com/news/1184881753); [Memory supercycle through 2028, Blocks & Files, 2026-01-21](https://www.blocksandfiles.com/ai-ml/2026/01/21/memory-semiconductor-supercycle-set-to-run-through-2028/4090501)). The proximate driver is HBM: SK Hynix has now sold out 2026 DRAM, NAND, *and* HBM capacity to NVIDIA and the hyperscalers ([SK Hynix sold out 2026, Notebookcheck, 2026](https://www.notebookcheck.net/SK-hynix-sells-out-its-DRAM-NAND-and-HBM-chip-supply-to-Nvidia-through-2026-as-AI-demand-outpaces-Samsung-and-Micron-s-capacity.1151402.0.html)), Micron has its full FY2026 HBM allocation booked and is guiding Q3 revenue of $33.5 billion at 81% gross margin ([Seeking Alpha, Micron Q3 FY26 guidance, 2026](https://seekingalpha.com/news/4566187-micron-signals-33_5b-q3-revenue-target-and-81-percent-gross-margin-guidance-driven-by-ai)), and the industry has shifted from one-year contracts to 3-5-year long-term agreements ([TrendForce, Samsung/Hynix LTAs, 2026-04-09](https://www.trendforce.com/news/2026/04/09/news-from-annual-deals-to-3-5-year-ltas-samsung-and-sk-hynix-reportedly-reset-big-tech-memory-contracts/)). HBM bit-share is now consuming enough DRAM wafer area to crowd out conventional DDR5/LPDDR/niche supply, lifting *every* downstream price-point: Adata's chairman expects DRAM and NAND contract prices to climb >40% in 2Q26 alone ([DigiTimes, Adata 2Q26 pricing, 2026-05](https://www.digitimes.com/news/a20260507PD240/adata-dram-nand-flash-revenue.html)), Winbond reported Q1 FY26 gross margin of 53.4% with niche DRAM revenue share at 47% and capacity sold out through 2027 ([BigGo Finance Winbond Q1 FY26, 2026-05-05](https://finance.biggo.com/news/TW_2344.TW_2026-05-05); [PBX Science Winbond sold-out 2027, 2026](https://pbxscience.com/global-dram-crisis-intensifies-winbond-capacity-sold-out-through-2027-as-ai-demand-reshapes-memory-market/)), and Macronix ended a ten-quarter losing streak with NAND revenue up 382% YoY ([BigGo Finance Macronix Q1 FY26, 2026-04-27](https://finance.biggo.com/news/TW_2337.TW_2026-04-27)).

The cycle is structurally distinct from the 2017-2018 super-cycle on three vectors. First, HBM is a fundamentally different product than commodity DRAM — each HBM3E/HBM4 stack consumes roughly 3-5× the wafer area per gigabyte vs DDR5 and ties up advanced-packaging slots not available to conventional DRAM ([SK Hynix HBM4 launch, EE Times, 2026](https://www.eetimes.com/sk-hynix-maintains-memory-leadership-with-first-hbm4/)). Second, demand is backed by ratable multi-year hyperscaler commitments rather than smartphone-cycle wave dynamics. Third, the supply side cannot respond — JPM models 8-12% HBM supply gaps through 2027 ([JPM Global Memory Market, 2026-01](https://www.scribd.com/document/987308211/JPM-Global-Memory-Market-2026-01-23-5183421)) and BofA characterizes 2026 as a "supercycle similar to the 1990s boom" with DRAM revenue +51% YoY and NAND +45% YoY ([DigiTimes Adata, 2026-02](https://www.digitimes.com/news/a20260205PD200/2026-revenue-adata-chips-price.html)).

The basket bets on the four ways to capture this: the three integrated HBM/DRAM/NAND leaders (Hynix, Samsung, Micron) plus freshly-listed Kioxia and recently spun-out Sandisk on the NAND side; Taiwanese specialty-memory long-tail beneficiaries (Winbond, Macronix) catching big-three niche-node spillover; the China memory chain (GigaDevice, Hua Hong) building out CXMT/YMTC capacity under sanctions pressure; and the global equipment incumbents (AMAT, LRCX, Tokyo Electron) plus HBM-test gatekeeper Advantest. The vulnerability is supply-side response in 2027-2028 — Samsung Pyeongtaek P4 and SK Hynix M15X bring HBM wafer starts onstream by 2H27, and CXMT's HBM3 mass-production plan for late-2026 is the wildcard ([Tom's Hardware CXMT HBM3](https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly)). Drift watch: separate price-takers (Hynix, Micron, Winbond) from equipment names whose forward bookings already discount a 2028-2030 build-out — the latter group has the biggest air-pocket risk if AI capex stutters.

## Scope rules

**In:** integrated DRAM/NAND manufacturers; HBM-specific suppliers; specialty / niche DRAM and NAND designers benefiting from spillover demand; China memory-fab chain (memory-design houses, foundry exposed to memory mix, equipment suppliers shipping into CXMT / YMTC / Hua Hong); global wafer-fab-equipment incumbents whose memory exposure is >25% of revenue or whose HBM advanced-packaging tools are the binding constraint; memory test / probe houses (Advantest, Hangzhou Changchuan) where HBM testing is a disclosed growth axis.

**Out:** logic foundries unless dedicated memory (TSMC, UMC excluded — they participate in HBM via CoWoS but the thesis is captured via Tokyo Electron and AMAT); ABF substrate, MLCC, and AI-passives names (covered in a separate `ai-passives-packaging` theme); cloud / hyperscale software (separate "AI infrastructure" theme); pure-play AI accelerators with HBM dependency (NVDA, AVGO) — these belong in a dedicated "AI-accelerator" theme; private memory makers (CXMT, YMTC, Bain-controlled Kioxia is in because it now lists publicly as 285A.T). EDA names (SNPS, CDNS) and pure consulting/analytics belong to other themes.

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| KS:000660 | SK Hynix | core | Global HBM market-share leader (~50-62% in 2026 with UBS forecasting ~70% in HBM4 for NVIDIA Rubin); 2026 DRAM + NAND + HBM capacity sold out to NVIDIA and hyperscalers; world-first HBM4 development completed ([SK Hynix 2026 Outlook, news.skhynix.com, 2026](https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/); [SK Hynix sold out 2026, Notebookcheck, 2026](https://www.notebookcheck.net/SK-hynix-sells-out-its-DRAM-NAND-and-HBM-chip-supply-to-Nvidia-through-2026-as-AI-demand-outpaces-Samsung-and-Micron-s-capacity.1151402.0.html); [SK Hynix HBM4 mass-production, news.skhynix.com](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/)). | 2026-05-31 |
| KS:005930 | Samsung Electronics | core | #2 HBM share (25-40%) trailing Hynix but with the largest captive DRAM/NAND wafer base and the most aggressive HBM4 catch-up plan via Pyeongtaek P4; the leverage on a single-quarter HBM share recapture is the largest in the basket ([Counterpoint via Astute Group, HBM share 2026](https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/); [SK Hynix vs Samsung HBM4, TrendForce, 2026-01-28](https://www.trendforce.com/news/2026/01/28/news-sk-hynix-reportedly-to-supply-about-two-thirds-of-nvidia-hbm4-samsung-targets-early-delivery/)). | 2026-05-31 |
| NASDAQ:MU | Micron | core | HBM franchise sold out through CY2026 to hyperscalers; Q3 FY26 revenue guide $33.5B with ~81% gross margin; FY26 revenue guide raised to $31.5-33.5B; the only US-listed pure-play in HBM/DRAM/NAND with full disclosure ([Micron Q2 FY26 prepared remarks, IR](https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357); [Seeking Alpha Q3 FY26 guide, 2026](https://seekingalpha.com/news/4566187-micron-signals-33_5b-q3-revenue-target-and-81-percent-gross-margin-guidance-driven-by-ai); [Micron FY26 10-Q, SEC](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000006/mu-20260226.htm)). | 2026-05-31 |
| TYO:285A | Kioxia | core | World's #2 NAND share (~17% by bit) with FY26 revenue +37% YoY to ¥2,338bn and operating profit roughly doubled YoY; Bain-controlled (51.1%) Toshiba-spinoff IPO'd late 2024 on TSE; the cleanest NAND pure-play exposure outside Sandisk ([Kioxia IR, 2026](https://www.kioxia-holdings.com/en-jp/ir.html); [Kioxia FY26 results, Quartr](https://quartr.com/companies/kioxia-holdings-corporation_19501)). | 2026-05-31 |
| NASDAQ:SNDK | Sandisk | core | Western Digital flash-business spinoff completed 2025-02-21; now independent pure-play NAND with ~16% global bit share; 1Y price return +4,397% on the rerating from "buried-inside-WDC" to independent supercycle bid ([WDC 8-K Sandisk spinoff, SEC, 2025-02-21](https://www.sec.gov/Archives/edgar/data/0000106040/000010604025000012/wdc8-khardxspin.htm)). | 2026-05-31 |
| NASDAQ:WDC | Western Digital | adjacent | Post-spinoff WDC retains the HDD-only business plus near-line storage; less of a memory bet than a "AI data-storage capacity" bet, but the multi-year nearline HDD shortage co-moves with the NAND cycle. Q1 FY26 revenue $2.82bn +27% YoY ([WDC Q1 FY26 release, SEC, 2025-10](https://www.sec.gov/Archives/edgar/data/0000106040/000162828025047539/a4ex991-pressreleaseq126.htm)). | 2026-05-31 |
| TPE:2344 | Winbond Electronics | core | Niche-DRAM and specialty-flash beneficiary of supercycle spillover; Q1 FY26 revenue NT$38.25bn, gross margin 53.4%, DRAM revenue share jumped to 47% (GM 56.6%); Kaohsiung 12-inch capacity expanding from 15K to 24K wpm; capacity sold out through 2027; FY26 capex NT$40bn ([Winbond Q1 FY26 earnings call, BigGo, 2026-05-05](https://finance.biggo.com/news/TW_2344.TW_2026-05-05); [Winbond capacity sold out 2027, PBX Science, 2026](https://pbxscience.com/global-dram-crisis-intensifies-winbond-capacity-sold-out-through-2027-as-ai-demand-reshapes-memory-market/)). MS 2026 AAI 峰会反馈 cited as a multi-year-price-cycle conviction add ([MS Winbond reflection, zsxq 812485545245422](#)). | 2026-05-31 |
| TPE:2337 | Macronix International | core | ROM + NAND + NOR specialty player ending ten-quarter losing streak in Q1 FY26: revenue NT$10.5bn (+71% YoY), gross margin 40.8% from 17% prior year, NAND revenue (incl. eMMC) +382% YoY now 30% of mix; capacity fully loaded H2 with monthly price hikes ([Macronix Q1 FY26 earnings call, BigGo, 2026-04-27](https://finance.biggo.com/news/TW_2337.TW_2026-04-27); [Macronix turnaround, BigGo, 2026](https://finance.biggo.com/news/5nS3zp0BLfE1EzqPutm5)). | 2026-05-31 |
| SSE:603986 | GigaDevice 兆易创新 | core | A-share memory-design pure-play (NOR Flash, SLC NAND, niche DRAM); Q1 FY26 revenue 4.19bn RMB up ~120% YoY with net profit +510% YoY; the most-leveraged A-share name to niche-memory pricing rising into 2027 ([GigaDevice Q1 FY26 results, Futubull, 2026](https://news.futunn.com/en/post/73397393/the-memory-chip-industry-celebrates-stellar-earnings-with-gigadevice-03986); [GigaDevice niche DRAM/NAND outlook, DigiTimes, 2026-05-21](https://www.digitimes.com/news/a20260521VL208/gigadevice-dram-nand-2026-niche)). | 2026-05-31 |
| HK:1347 | Hua Hong Semiconductor 华虹半导体 | enabler | Specialty foundry with memory (embedded NVM) + analog/power exposure; Fab9A ramped, Fab9B construction starts 2026; Q1 FY26 capex $924.9M for 12-inch expansion; the China memory-fab buildout's only listed foundry-side play. MS 2026 AAI 峰会 cited the multi-year price cycle and aggressive long-term revenue guidance ([Hua Hong Q1 FY26 summary, Quartr, 2026](https://quartr.com/events/hua-hong-semiconductor-limited-1347-q1-2026_FgI1osS0); [Hua Hong AI demand strategy, DigiTimes, 2026-05](https://www.digitimes.com/news/a20260515VL202/hua-hong-semiconductor-technology-demand-semiconductor-industry-market.html); MS Hua Hong AAI feedback zsxq 812485545245152). | 2026-05-31 |
| NASDAQ:AMAT | Applied Materials | enabler | Largest global WFE incumbent with disclosed HBM-edge tool franchise; DRAM/NAND combined exposure ~25-30% of revenue; the Bernstein 战略决策大会 takeaway emphasized memory-tool re-acceleration into 2027 ([Bernstein AMAT strategy day, zsxq 212485522841821]; [Photronics signals AMAT-tier demand, DigiTimes, 2026](https://www.digitimes.com/news/a20260116PD217/demand-advantest-equipment-hbm-2026.html)). | 2026-05-31 |
| NASDAQ:LRCX | Lam Research | enabler | The single most memory-exposed of the WFE-3; etch & deposition franchise into 3D NAND and DRAM is ~50% of revenue; UHAR etching for next-gen 3D NAND is the choke point. Memory-tool re-acceleration is the consensus rebuild driver ([MS Semiconductor Capital Equipment Japan reflection, zsxq 184152218151852]). | 2026-05-31 |
| TYO:8035 | Tokyo Electron | enabler | FY26 net sales JPY 2,443.5bn record high, DRAM customers 31% of sales; advanced packaging segment guided +60%+ growth on HBM, EUV, GAA; HBM-interconnect etching forecast JPY 500bn by 2030; bonders/3D-integration tools another JPY 500bn ([Tokyo Electron Q4 FY26 transcript, Investing.com, 2026](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441); MS Semi Capital Equipment Japan zsxq 184152218151852). | 2026-05-31 |
| TYO:6857 | Advantest | enabler | The HBM tester gatekeeper — long-test-time HBM3E/HBM4 is a structural revenue tail; FY26 (March 2027) guide +26% revenue with SoC tester market +32%; T2000 AiR2X + M5241 Memory Handler next-gen rollout in 2026 ([Advantest FY26 guide, RCRWireless, 2026-01-30](https://www.rcrwireless.com/20260130/test-measurement/advantest-rises-with-the-ai-tide); [Advantest ATE backlog, DigiTimes, 2026-01-16](https://www.digitimes.com/news/a20260116PD217/demand-advantest-equipment-hbm-2026)). | 2026-05-31 |

**Geographic / role mix (14 tickers):** US 6 (43%) · Japan 3 (21%) · Korea 2 (14%) · Taiwan 2 (14%) · Hong Kong 1 (7%) · China A-share 1 (7%)*. Role: core 8, enabler 6.
*GigaDevice (SSE) and Hua Hong (HK) both anchor China-fab exposure.

## Exclusions

| Ticker | Reason |
|---|---|
| Private: CXMT (长鑫存储), YMTC (长江存储) | Not investable; CXMT is China's #4 global DRAM producer with HBM3 mass-production planned for end-2026; YMTC pushes Xtacking 4.0 267-layer NAND and is preparing an A-share listing ([CXMT Wikipedia](https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies); [YMTC 267-layer Xtacking, DigiTimes, 2025-09](https://www.digitimes.com/news/a20250924PD216/ymtc-nand-nand-flash-production-memory.html); [YMTC A-share, KrAsia, 2025](https://kr-asia.com/ymtc-moves-toward-a-share-listing-amid-memory-chip-supercycle)). Surfaced in IPO watch list. |
| NASDAQ:KLAC | Memory exposure lowest of the WFE-4 incumbents (~20% of revenue); marginal HBM dollar accrues to LRCX/AMAT/8035. Reconsider if memory mix rises >25%. |
| NASDAQ:NVDA, NASDAQ:AVGO | HBM-dependent end customers, not suppliers. Belong in a dedicated AI-accelerator theme. |
| NASDAQ:PSTG, NASDAQ:NTAP | Storage *integrators* — margin profile is software/platform, not raw NAND pricing. Separate "all-flash datacenter" theme. |
| NASDAQ:PLAB, NASDAQ:TER | Photronics' mask franchise too-indirect at +94% 1Y vs basket median >700%; Teradyne's memory exposure subordinate to SoC franchise. Borderline; reconsider on memory-handler design-win disclosures. |
| TPE:8299 (Phison), TPE:5289 (Innodisk), TPE:8271 (Apacer), TPE:3260 (Adata) | Module / SSD / controller pass-through plays — outsized 1Y returns (Apacer +405%, Innodisk +712%, Adata +389%, Phison +424%) but thesis is downstream ASP pass-through, not capacity-share. Tracked via watch list ([Phison COMPUTEX 2025](https://www.phison.com/en/category/article/press-releases/phisons-worlds-first-6nm-ai-computing-ssd-solution-wins-computex-2025-best-choice-golden-award)). |
| SSE:002371 (NAURA), SH:688012 (AMEC), SH:688072 (Piotech), SZSE:300604 (Hangzhou Changchuan) | Chinese WFE + memory-test handler shipping into CXMT/YMTC; bona-fide memory-equipment beneficiaries but best tracked in a dedicated `china-domestic-wfe` theme — different cadence than the global HBM/DRAM cycle ([TrendForce China memory expansion, 2026-04-21](https://www.trendforce.com/news/2026/04/21/news-china-memory-expansion-lifts-domestic-equipment-suppliers-amec-wuhan-jingce-hwatsing-acm-in-focus/); [TrendForce NAURA/AMEC 35% adoption, 2026-01-12](https://www.trendforce.com/news/2026/01/12/news-chinas-domestic-chip-equipment-adoption-beats-2025-target-at-35-led-by-naura-amec/)). |
| SZSE:300223 (Ingenic) | Specialty memory designer; thesis-fit intact but dominated by GigaDevice. Watch list. |
| SH:688795 (Moore Threads 摩尔线程) | China GPU first IPO with HBM-dependent KUAE orders, but equity story is GPU-design not memory ([Moore Threads IPO, STCN, 2025-11](https://www.stcn.com/article/detail/3494223.html)). AI-accelerator theme. |
| NASDAQ:SNPS, NASDAQ:CDNS | EDA. Out of scope per user direction ([MS SNPS 2027 zsxq 812485522841582]). |

## Keywords

memory super-cycle / 存储超级周期 · DRAM / NAND / HBM · high-bandwidth memory · HBM3E / HBM4 · 12-Hi / 16-Hi stack · niche DRAM / 利基 DRAM · 3D NAND / Xtacking · long-term agreement (LTA) / 长期协议 · hyperscaler memory contract · CXMT / YMTC · memory capex / 存储资本开支 · ATE / memory tester · advanced packaging / HBM TSV · UHAR etch · wafer-fab equipment (WFE).

## Performance (as of 2026-05-31, since-inception snapshot)

Returns are simple price returns from yfinance with `auto_adjust=True`, computed against the 2026-05-29 close (last trading day on or before the anchor). The basket is multi-market; benchmarks reported separately by geography.

**Equal-weight basket returns:** 3-month +74.9% · YTD 2026 +188.1% · trailing 1-year +992.3%.

**Benchmark returns over the same windows:**

| Benchmark | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| S&P 500 (SPY) | +10.6% | +11.0% | +29.8% |
| PHLX Semiconductor (^SOX) | +58.4% | +74.1% | +169.6% |
| SOXX (iShares Semi) | +61.6% | +81.5% | +179.5% |
| KOSPI (^KS11) | +35.7% | +96.7% | +214.2% |
| Hang Seng (2800.HK) | −4.9% | −3.6% | +10.8% |
| CSI 300 (510300.SS) | +4.2% | +6.3% | +30.5% |

**Per-ticker performance, sorted by 1-year return:**

| Ticker | 1Y | YTD | 3M | Close (local) |
|---|---|---|---|---|
| NASDAQ:SNDK | +4,397.2% | +515.8% | +166.8% | 1,694.98 |
| TYO:285A (Kioxia) | +3,037.2% | +531.0% | +210.5% | 65,850 |
| KS:000660 (SK Hynix) | +1,045.6% | +245.3% | +119.9% | 2,333,000 |
| NASDAQ:MU | +930.4% | +208.0% | +135.6% | 971.00 |
| NASDAQ:WDC | +934.9% | +183.1% | +90.0% | 531.21 |
| TPE:2344 (Winbond) | +797.3% | +74.9% | +29.7% | 158.00 |
| TPE:2337 (Macronix) | +672.6% | +284.1% | +51.4% | 166.50 |
| KS:005930 (Samsung) | +474.0% | +147.2% | +46.7% | 317,000 |
| HK:1347 (Hua Hong) | +410.4% | +98.4% | +66.7% | 161.30 |
| SSE:603986 (GigaDevice) | +317.6% | +118.3% | +55.9% | 467.01 |
| NASDAQ:LRCX | +296.7% | +72.1% | +36.2% | 318.18 |
| TYO:6857 (Advantest) | +256.4% | +33.5% | −2.4% | 26,170 |
| NASDAQ:AMAT | +189.2% | +67.8% | +21.0% | 450.06 |
| TYO:8035 (Tokyo Electron) | +132.4% | +54.2% | +20.2% | 52,420 |

**Read of the dispersion:** Sandisk and Kioxia 1Y outliers (+4,397% and +3,037%) reflect IPO/spinoff revaluation from non-public baselines, not pure memory-cycle moves. Stripping them, median 1Y is ~+470% (SK Hynix), median 3M +52% (Macronix). DRAM/NAND price-takers (Hynix, Micron, Samsung, Winbond, Macronix) average +783% 1Y vs equipment incumbents (AMAT, LRCX, 8035, 6857) at +219%. Equipment lagged because it re-rated *earlier* (2024 H2) on the first HBM TAM upgrade and has been consolidating while price-takers re-rate as contract prices print. Dispersion argues against equal-weighting for actual sizing — the four equipment names plus Advantest offer the cleanest convexity to a 2026-27 capex re-acceleration without priced-in HBM premium.

## Recent events (since basket inception)

Inception write; covers prior ~90 days that informed ticker selection. Future refreshes will cover the window since the previous `Last refreshed`.

- **SK Hynix 2026 DRAM/NAND/HBM sold out + Microsoft DDR5 LTA talks worth tens of trillions of won** ([Notebookcheck, 2026](https://www.notebookcheck.net/SK-hynix-sells-out-its-DRAM-NAND-and-HBM-chip-supply-to-Nvidia-through-2026-as-AI-demand-outpaces-Samsung-and-Micron-s-capacity.1151402.0.html); [TrendForce LTAs reset, 2026-04-09](https://www.trendforce.com/news/2026/04/09/news-from-annual-deals-to-3-5-year-ltas-samsung-and-sk-hynix-reportedly-reset-big-tech-memory-contracts/)).
- **Micron Q2 FY26 + Q3 guide $33.5B revenue at 81% GM:** HBM sold out through CY2026; data-center revenue +150% YoY ([Micron Q2 FY26 IR](https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357); [Seeking Alpha guide, 2026](https://seekingalpha.com/news/4566187-micron-signals-33_5b-q3-revenue-target-and-81-percent-gross-margin-guidance-driven-by-ai)).
- **Winbond Q1 FY26 (2026-05-05):** revenue NT$38.25bn, GM 53.4%, DRAM share 47%, capacity sold-out through 2027; Kaohsiung 15K → 24K wpm expansion; FY26 capex NT$40bn ([BigGo](https://finance.biggo.com/news/TW_2344.TW_2026-05-05)).
- **Macronix Q1 FY26 (2026-04-27):** 10-quarter losing streak ends; revenue +71% YoY, NAND +382% YoY; GM 40.8% from 17% prior ([BigGo](https://finance.biggo.com/news/TW_2337.TW_2026-04-27)).
- **GigaDevice Q1 FY26:** revenue +120% YoY, net profit +510% YoY ([Futubull](https://news.futunn.com/en/post/73397393/the-memory-chip-industry-celebrates-stellar-earnings-with-gigadevice-03986); [DigiTimes 2026-05-21](https://www.digitimes.com/news/a20260521VL208/gigadevice-dram-nand-2026-niche)).
- **Hua Hong Q1 FY26:** Fab9A ramped, Fab9B construction starts 2026; capex $924.9M for 12-inch ([Quartr](https://quartr.com/events/hua-hong-semiconductor-limited-1347-q1-2026_FgI1osS0)). MS 2026 AAI 峰会 conviction call on multi-year price cycle.
- **Tokyo Electron Q4 FY26:** record net sales JPY 2,443.5bn; DRAM 31% of sales; advanced-packaging guided +60%+; JPY 500bn HBM-interconnect etch target by 2030 ([Investing.com transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441)).
- **Advantest FY26 (Mar-2027 fiscal) guide +26% revenue, SoC tester market +32%; M5241 Memory Handler ships Q2 2026** ([RCRWireless, 2026-01](https://www.rcrwireless.com/20260130/test-measurement/advantest-rises-with-the-ai-tide); [DigiTimes ATE backlog, 2026-01](https://www.digitimes.com/news/a20260116PD217/demand-advantest-equipment-hbm-2026)).
- **SK Hynix HBM4 world-first development + mass-production ready** ([news.skhynix.com](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/); [TrendForce, 2026-01-28](https://www.trendforce.com/news/2026/01/28/news-sk-hynix-reportedly-to-supply-about-two-thirds-of-nvidia-hbm4-samsung-targets-early-delivery/)).
- **Adata 2Q26 chairman guide: DRAM + NAND contract prices each +40% in 2Q26**, cloud giants have locked up 2027 output ([DigiTimes, 2026-05](https://www.digitimes.com/news/a20260507PD240/adata-dram-nand-flash-revenue.html)).
- **Sandisk independence (2025-02-21) + Kioxia listing (late-2024 TSE) created two new pure-play NAND equities** ([WDC 8-K/A, SEC](https://www.sec.gov/Archives/edgar/data/0000106040/000010604025000012/wdc8-khardxspin.htm)).
- **CXMT HBM3 mass-production planned end-2026** — the wildcard, China-domestic HBM via CXMT + NAURA/Maxwell assembly tools ([Tom's Hardware](https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly)).

## Drift signals

Inception write — drift detection becomes the value-add starting from the *next* refresh. Initial flags for next month's pass:

- **Equipment vs price-taker dispersion (basket internal):** 1Y return gap between price-takers (SK Hynix +1,045%, Micron +930%) and equipment incumbents (AMAT +189%, 8035 +132%) is the largest single read. Watch AMAT / LRCX / 8035 *backlog* disclosures vs DRAM / NAND ASP momentum — if memory-equipment bookings re-accelerate into a confirmed 2027 capex cycle, equipment names compress the gap; if not, price-takers stay the high-beta engine.
- **CXMT HBM3 end-2026 mass-production is a binary watch.** Successful ramp would supply 5-8% of incremental HBM bit-demand from a politically-isolated source, reset Samsung HBM4 catch-up math, and flatter NAURA/AMEC/Piotech into a re-entry candidate. Delay/yield failure tightens the global HBM crunch further.
- **HBM4 supplier reshuffle 2H 2026:** UBS forecasts SK Hynix ~70% HBM4 share for NVIDIA Rubin, but Samsung is pushing early delivery and Micron has a 12-Hi HBM4 path. A single-quarter share reshuffle would re-rate Samsung vs Hynix by 15-25%. Track Samsung P4 wafer-start and Micron HBM4 sampling.
- **Watch list (public, considered not added):** NAURA (002371) / AMEC (688012) / Piotech (688072) / Hangzhou Changchuan (300604) → dedicated `china-domestic-wfe` theme; Phison (8299) / Innodisk (5289) / Apacer (8271) / Adata (3260) → module/controller pass-through (already +400-700% 1Y, priced); Ingenic (300223) → dominated by GigaDevice; KLAC → reconsider if memory mix >25%.
- **Watch list (private — surface for IPO):** CXMT (HKEX listing rumored 2026-27, would be top-3 basket member); YMTC (preparing A-share listing per recent reports, would rank top-5) ([CXMT Wikipedia](https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies); [YMTC KrAsia 2025](https://kr-asia.com/ymtc-moves-toward-a-share-listing-amid-memory-chip-supercycle)).
- **Macro risk to thesis:** basket-wide 1Y +992% already prices in ~18 months of thesis. Next leg requires *fresh* HBM contract-price prints, *fresh* LTA disclosures, or *fresh* China-fab announcements. An earnings-cycle air pocket (July-Aug 2026) would compress the basket faster than any idiosyncratic move. Watch 90-day rolling vol on SK Hynix + Micron as basket-drawdown leading indicator.
- **Stale-justification flag:** Hua Hong (1347.HK) Justification references MS' 2026 AAI feedback — verify at next refresh whether multi-year-price-cycle conviction holds against Q2 FY26 numbers.

## Catalysts (next 3-6 months)

- **SK Hynix + Samsung Q2 2026 earnings (late-July):** incremental HBM4 share, FY26-27 LTA reveals; Samsung P4 ramp + NVIDIA qualification status.
- **Micron Q4 FY26 (end-August):** first FY27 commentary; CY27 HBM allocation not yet guided.
- **Kioxia + Sandisk Q2 (August):** cleanest NAND pure-play prints since spinoff/IPO cycles.
- **Hua Hong Q2 FY26 (August):** Fab9B construction milestones; Huali Micro deal close.
- **CXMT HBM3 mass-production launch (end-2026):** wildcard for global HBM supply curve.
- **NVIDIA Rubin + HBM4 design-win disclosures (Q4 2026 - Q1 2027):** definitive read on SK Hynix vs Samsung HBM4 share.
- **YMTC / CXMT A-share or HKEX listing filings:** any IPO prospectus drop = immediate basket-mutation trigger.

## Data Used / 数据来源清单

**Market data**
- yfinance `auto_adjust=True` for prices, returns, market cap, sector — pulled 2026-05-31 against 2026-05-29 close.
- Benchmarks: SPY (S&P 500), ^SOX (PHLX Semiconductor), SOXX (iShares Semi), ^KS11 (KOSPI), 2800.HK (Hang Seng ETF), 510300.SS (CSI 300 ETF).

**Per-ticker primary / industry sources** (cited inline; consolidated in References)
- 000660 SK Hynix: corporate 2026 outlook + HBM4 mass-production release; Notebookcheck sold-out coverage.
- 005930 Samsung: Counterpoint HBM share; TrendForce HBM4 race.
- MU Micron: Q2 FY26 IR prepared remarks; Q3 FY26 guide; FY26 10-Q SEC.
- 285A Kioxia: Kioxia IR + Quartr FY26 results.
- SNDK Sandisk: WDC 8-K spinoff filing SEC.
- WDC Western Digital: Q1 FY26 release SEC.
- 2344 Winbond: Q1 FY26 BigGo + PBX Science capacity sold-out coverage.
- 2337 Macronix: Q1 FY26 BigGo + turnaround commentary.
- 603986 GigaDevice: Q1 FY26 Futubull + DigiTimes niche-memory outlook.
- 1347 Hua Hong: Q1 FY26 Quartr + DigiTimes AI strategy; MS Hua Hong 2026 AAI feedback (zsxq 812485545245152).
- AMAT: Bernstein strategy day (zsxq 212485522841821); DigiTimes memory-tool demand signals.
- LRCX: MS Semi Capital Equipment Japan reflection (zsxq 184152218151852); MS Taiwan (zsxq 415284812111518).
- 8035 Tokyo Electron: Q4 FY26 transcript Investing.com.
- 6857 Advantest: FY26 guide RCRWireless + DigiTimes ATE backlog.

**Industry research (theme-level)**
- JPMorgan 2026 Storage Outlook ($1.0T 2026 / $1.5T 2027 market cap, $90B HBM TAM by 2027): [Tiger Brokers summary, 2026-01](https://www.itiger.com/news/1184881753); [JPM Global Memory Market 2026-01-23](https://www.scribd.com/document/987308211/JPM-Global-Memory-Market-2026-01-23-5183421).
- [Memory supercycle through 2028 (Blocks & Files), 2026-01-21](https://www.blocksandfiles.com/ai-ml/2026/01/21/memory-semiconductor-supercycle-set-to-run-through-2028/4090501).
- [TrendForce 3-5 yr LTAs reset, 2026-04-09](https://www.trendforce.com/news/2026/04/09/news-from-annual-deals-to-3-5-year-ltas-samsung-and-sk-hynix-reportedly-reset-big-tech-memory-contracts/); [TrendForce China memory expansion, 2026-04-21](https://www.trendforce.com/news/2026/04/21/news-china-memory-expansion-lifts-domestic-equipment-suppliers-amec-wuhan-jingce-hwatsing-acm-in-focus/); [Tom's Hardware CXMT HBM3 end-2026](https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly).
- zsxq evidence: JPM 全球存储市场 (184152588584282 + 212485541484181, flagship); GS 中国智能手机 4 月 (812485545248882); MS Hua Hong AAI 2026 (812485545245152); MS Winbond 华邦 AAI 2026 (812485545245422); MS Semi Cap Equipment Japan (184152218151852) + Taiwan (415284812111518); MS Photronics (415284812112558); Bernstein AMAT 战略决策大会 (212485522841821); MS SNPS 2027 (812485522841582).

**Macro backdrop (as of 2026-05-25 latest, from `db/indicators.db`)**
- VIX: 16.68 (low-vol regime supportive of duration-extending growth bets).
- 10Y Treasury (TNX): 4.59% (2026-05-22) — elevated but stable; not a headwind for cyclical re-rates so long as earnings re-acceleration prints.
- HYG (high-yield ETF proxy): 79.91 (2026-05-22) — credit spreads tight, risk-on regime intact.
- DXY: 98.99 (2026-05-25) — soft USD; tailwind for translation of KRW / JPY / TWD names in the basket.

**Cross-coverage (existing in-house research, if any)**
- None at inception — no `reports/company/` folder yet for any basket member. Adding company-research deep-dives for SK Hynix and Micron would be the highest-value follow-ups; Tokyo Electron and Advantest the next.

**Stale notices / coverage gaps**
- Market-cap snapshots from `market_cap_cache.db` not pulled at inception — next refresh should add cap-weighted basket performance as a complement to equal-weight.
- 1Y returns for Sandisk and Kioxia capture the IPO / spinoff revaluation; pure "memory cycle" beta starting from listing date would be a cleaner comp at the next refresh.
- The basket has no exposure to Asia memory-module / SSD assemblers (Apacer, Adata, Innodisk, Phison) by design — flagged in Drift signals as a watch-list pivot if module margins start re-rating independently.
- No coverage of YMTC / CXMT (private) — flagged in Exclusions and surfaced for IPO-trigger mutation.

## References

All URLs cited inline above; this is the consolidated index for quick scanning. (Some industry-research items also appear earlier in the Data Used manifest.)

**Thesis / industry research:** [JPM 2026 Storage Outlook (Tiger)](https://www.itiger.com/news/1184881753) · [JPM Global Memory 2026-01-23](https://www.scribd.com/document/987308211/JPM-Global-Memory-Market-2026-01-23-5183421) · [Memory supercycle 2028 (Blocks & Files)](https://www.blocksandfiles.com/ai-ml/2026/01/21/memory-semiconductor-supercycle-set-to-run-through-2028/4090501) · [TrendForce LTAs reset](https://www.trendforce.com/news/2026/04/09/news-from-annual-deals-to-3-5-year-ltas-samsung-and-sk-hynix-reportedly-reset-big-tech-memory-contracts/) · [Adata 2Q26 +40% pricing (DigiTimes)](https://www.digitimes.com/news/a20260507PD240/adata-dram-nand-flash-revenue.html) · [Adata 2026 supercycle outlook (DigiTimes)](https://www.digitimes.com/news/a20260205PD200/2026-revenue-adata-chips-price.html) · [Samsung memory shortages (Network World)](https://www.networkworld.com/article/4113772/samsung-warns-of-memory-shortages-driving-industry-wide-price-surge-in-2026.html).

**SK Hynix:** [2026 Outlook (corp)](https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/) · [HBM4 mass-production release](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/) · [HBM4 first dev (EE Times)](https://www.eetimes.com/sk-hynix-maintains-memory-leadership-with-first-hbm4/) · [Counterpoint via Astute HBM share](https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/) · [Hynix-Samsung HBM4 race (TrendForce)](https://www.trendforce.com/news/2026/01/28/news-sk-hynix-reportedly-to-supply-about-two-thirds-of-nvidia-hbm4-samsung-targets-early-delivery/) · [Sold-out 2026 (Notebookcheck)](https://www.notebookcheck.net/SK-hynix-sells-out-its-DRAM-NAND-and-HBM-chip-supply-to-Nvidia-through-2026-as-AI-demand-outpaces-Samsung-and-Micron-s-capacity.1151402.0.html).

**Micron / Kioxia / Sandisk / WDC:** [Micron Q2 FY26 IR](https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357) · [Micron Q3 FY26 guide (Seeking Alpha)](https://seekingalpha.com/news/4566187-micron-signals-33_5b-q3-revenue-target-and-81-percent-gross-margin-guidance-driven-by-ai) · [Micron FY26 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000006/mu-20260226.htm) · [Kioxia IR](https://www.kioxia-holdings.com/en-jp/ir.html) · [Kioxia FY26 (Quartr)](https://quartr.com/companies/kioxia-holdings-corporation_19501) · [WDC 8-K Sandisk spinoff (SEC)](https://www.sec.gov/Archives/edgar/data/0000106040/000010604025000012/wdc8-khardxspin.htm) · [WDC Q1 FY26 (SEC)](https://www.sec.gov/Archives/edgar/data/0000106040/000162828025047539/a4ex991-pressreleaseq126.htm).

**Winbond / Macronix / GigaDevice / Hua Hong:** [Winbond Q1 FY26 (BigGo)](https://finance.biggo.com/news/TW_2344.TW_2026-05-05) · [Winbond sold-out 2027 (PBX)](https://pbxscience.com/global-dram-crisis-intensifies-winbond-capacity-sold-out-through-2027-as-ai-demand-reshapes-memory-market/) · [Macronix Q1 FY26 (BigGo)](https://finance.biggo.com/news/TW_2337.TW_2026-04-27) · [Macronix turnaround (BigGo)](https://finance.biggo.com/news/5nS3zp0BLfE1EzqPutm5) · [GigaDevice Q1 FY26 (Futubull)](https://news.futunn.com/en/post/73397393/the-memory-chip-industry-celebrates-stellar-earnings-with-gigadevice-03986) · [GigaDevice niche DRAM/NAND (DigiTimes)](https://www.digitimes.com/news/a20260521VL208/gigadevice-dram-nand-2026-niche) · [Hua Hong Q1 FY26 (Quartr)](https://quartr.com/events/hua-hong-semiconductor-limited-1347-q1-2026_FgI1osS0) · [Hua Hong AI strategy (DigiTimes)](https://www.digitimes.com/news/a20260515VL202/hua-hong-semiconductor-technology-demand-semiconductor-industry-market.html).

**Equipment / test (AMAT, LRCX, 8035, 6857):** [Tokyo Electron Q4 FY26 transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-tokyo-electron-q4-2026-beats-estimates-stock-surges-93CH-4654441) · [Advantest FY26 guide (RCRWireless)](https://www.rcrwireless.com/20260130/test-measurement/advantest-rises-with-the-ai-tide) · [Advantest ATE backlog (DigiTimes)](https://www.digitimes.com/news/a20260116PD217/demand-advantest-equipment-hbm-2026).

**China memory chain (excluded / watch):** [CXMT HBM3 end-2026 (Tom's Hardware)](https://www.tomshardware.com/pc-components/dram/chinese-semiconductor-industry-gears-up-for-domestic-hbm3-production-by-the-end-of-2026-cxmt-to-produce-chips-while-naura-maxwell-and-u-preseason-design-tools-for-assembly) · [CXMT (Wikipedia)](https://en.wikipedia.org/wiki/ChangXin_Memory_Technologies) · [YMTC Xtacking 267-layer (DigiTimes)](https://www.digitimes.com/news/a20250924PD216/ymtc-nand-nand-flash-production-memory.html) · [YMTC A-share listing (KrAsia)](https://kr-asia.com/ymtc-moves-toward-a-share-listing-amid-memory-chip-supercycle) · [TrendForce China memory expansion](https://www.trendforce.com/news/2026/04/21/news-china-memory-expansion-lifts-domestic-equipment-suppliers-amec-wuhan-jingce-hwatsing-acm-in-focus/) · [TrendForce NAURA/AMEC 35% adoption](https://www.trendforce.com/news/2026/01/12/news-chinas-domestic-chip-equipment-adoption-beats-2025-target-at-35-led-by-naura-amec/) · [Phison COMPUTEX 2025 E28](https://www.phison.com/en/category/article/press-releases/phisons-worlds-first-6nm-ai-computing-ssd-solution-wins-computex-2025-best-choice-golden-award) · [Moore Threads IPO (STCN)](https://www.stcn.com/article/detail/3494223.html) · [Moore Threads investor record (cninfo)](http://dataclouds.cninfo.com.cn/shgonggao/investor/2026/20260519/739c32d90caa624b7329df0a7da48fea.pdf).

## History

- 2026-05-31 — theme created with 14-ticker basket (8 core, 6 enabler) following user request "Build a theme on the 2025-2028 memory super-cycle". Cuts vs seed universe: excluded NVDA / AVGO (AI-accelerator theme), PSTG / NTAP (all-flash datacenter theme), KLAC (memory mix too low), PLAB (too-indirect mask exposure), TER (memory mix subordinate to SoC), Adata / Innodisk / Apacer / Phison (module pass-through — watch list), NAURA / AMEC / Piotech / Hangzhou Changchuan (consolidating in dedicated `china-domestic-wfe` theme), Ingenic (dominated by GigaDevice on the China niche-memory axis), Moore Threads (GPU not memory). Adds vs seed: Winbond 2344.TW and Macronix 2337.TW (Taiwanese specialty memory long-tail). CXMT and YMTC excluded as private — flagged for IPO-trigger mutation.
