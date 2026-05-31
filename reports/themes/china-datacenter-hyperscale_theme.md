# China Data Center & Hyperscale Operators / 中国数据中心与超级云算运营商

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en

## Thesis

The China data-center trade has flipped from a 2022–2024 *supply-glut, single-digit-yield* story into a 2025–2026 *order-momentum-leading-build-out* story. Goldman Sachs' Q1 2026 China-DC review summarised it as "产能扩张与上架节奏偏缓但订单动能依旧强劲" — capacity expansion and rack-up cadence are slow, but order momentum remains strong; GS flags cloud + data centre as the top sub-sector in China internet, with GDS and VNET as named picks ([Goldman Sachs via futubull, 2026](https://news.futunn.com/en/post/71011256/goldman-sachs-cloud-and-data-center-sectors-are-the-top)). The Q1 prints back that view: GDS booked >340MW YTD by the call, cumulative committed 1.8GW, FY26 sales target ≥500MW, 3-yr capex RMB 30–50bn ([GDS Q1 2026 6-K](https://www.sec.gov/Archives/edgar/data/0001526125/000110465926064164/tm2614459d3_ex99-1.htm); [Sahm Capital call, 2026-05-20](https://www.sahmcapital.com/news/content/gds-holdings-q1-2026-earnings-call-transcript-2026-05-20)). VNET — the other GS pick — printed wholesale revenue +58.1% YoY and 519MW of new YTD orders including a single 400MW Beijing-area ticket; CATL then announced a near-US$1bn / 38.1% stake purchase that re-frames the equity as a battery-to-power-to-compute play ([VNET Q1 2026 IR, 2026](https://ir.21vianet.com/news-releases/news-release-details/vnet-reports-unaudited-first-quarter-2026-financial-results); [Bamboo Works on CATL/VNET, 2026](https://thebambooworks.com/after-years-on-the-sidelines-vnet-seizes-on-chinas-ai-moment-with-new-catl-tie-up/)).

The demand-anchor case rests on China hyperscaler capex acceleration. ByteDance (private; tracked indirectly) is signalling >RMB 200bn (~US$30bn) of 2026 AI capex with one read as high as US$70bn ([Digitimes, 2026-05-28](https://www.digitimes.com/news/a20260528VL212/bytedance-capex-qualcomm-infrastructure-data.html)). Alibaba pledged RMB 380bn over three years for AI + cloud and said it will exceed that figure; Cloud Intelligence Group printed +38% YoY revenue and AI-product revenue triple-digit YoY for 11 consecutive quarters ([Alibaba FY26 Q4 6-K, 2026](https://www.sec.gov/Archives/edgar/data/0001577552/000110465926060224/tm2614494d1_ex99-1.htm); [RMB 380bn announcement, 2025](https://www.alibabacloud.com/blog/alibaba-to-invest-rmb380-billion-in-ai-and-cloud-infrastructure-over-next-three-years_602007)). Tencent's Q1 2026 capex hit RMB 31.9bn (+16% YoY / +63% QoQ) with 2H 2026 guided to a "substantial increase" on more China-designed ASICs ([Yicai Global, 2026](https://www.yicaiglobal.com/news/tencents-first-quarter-profit-jumps-21-while-ai-spending-exceeds-usd44-billion)). The basket exists because the IDCs are the receiving end of those numbers and the domestic inference-chip + server-OEM names anchor the demand mix.

The thesis vulnerability is rack-up cadence, not order intake — a single quarter of slower commissioning at GDS or VNET would re-test the equity story even with cumulative bookings rising. The basket is also exposed to ASIC-availability risk: Cambricon's 2026 target of 500k AI accelerators depends heavily on SMIC's 7nm yield, currently ~20% ([Tom's Hardware, 2026](https://www.tomshardware.com/tech-industry/semiconductors/cambricon-targets-500000-ai-chips-in-2026-as-china-accelerates-domestic-hardware-push)).

## Scope rules

**In:** Chinese DC operators (NASDAQ ADRs and A-share / HK pure-plays) where IDC / wholesale-IDC is the dominant business; China hyperscaler parents (Tencent, Alibaba, Baidu) where cloud + AI capex is disclosed; two China-listed telcos whose 2026 capex pivot to computing is on the printed record; A-share inference-chip and server-OEM names publicly named as receiving counterparties of the IDC build-out.

**Out:** US hyperscalers (AWS / Azure / GCP) and US DC REITs (EQIX, DLR) — outside the China-onshore thesis; private operators (Chindata, ByteDance); semiconductor design / foundry (NVIDIA, AMD, Hua Hong) — captured in `memory-upcycle` and dedicated AI-accelerator themes; pure power-equipment plays (Jereh 002353) — in `ai-power-electrification`; AI-content / inference-application names (Kuaishou Kling AI).

**Overlap caveat (sized exposure).** This basket *deliberately overlaps* `ai-power-electrification` on gas-turbine / grid-side names and `memory-upcycle` on the Hua Hong / HBM / mature-node memory chain — do not stack equal-weights across all three. The added value of *this* basket is the **operator + demand-anchor** angle: who collects the rent (IDCs), who writes the cheque (hyperscalers + telcos), and which silicon ends up inside (inference chips + server OEMs). BOM-side names belong in the other baskets.

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| NASDAQ:GDS | GDS Holdings (万国数据) | core | Largest pure-play China wholesale IDC; Q1 2026 cumulative committed 1.8GW with >340MW YTD bookings by call date; 2026 sales target ≥500MW with RMB 30–50bn 3-yr capex; GS Asia conviction long ([GDS Q1 2026 6-K, 2026](https://www.sec.gov/Archives/edgar/data/0001526125/000110465926064164/tm2614459d3_ex99-1.htm); [Sahm Capital call, 2026-05-20](https://www.sahmcapital.com/news/content/gds-holdings-q1-2026-earnings-call-transcript-2026-05-20)). NASDAQ ADR tracked (HK primary 9698.HK not separately weighted). | 2026-05-31 |
| NASDAQ:VNET | VNET / 21Vianet (世纪互联) | core | Q1 2026 total revenue +19.8% YoY, wholesale +58.1% YoY; 519MW YTD new orders incl. one 400MW Beijing wholesale ticket; CATL near-US$1bn / 38.1% stake purchase 2026-05-13 ([VNET Q1 2026 IR, 2026](https://ir.21vianet.com/news-releases/news-release-details/vnet-reports-unaudited-first-quarter-2026-financial-results); [Sahm Capital on CATL/VNET, 2026](https://www.sahmcapital.com/news/content/catls-us1b-bet-recasts-vnet-as-ai-data-center-player-2026-05-20)). HSBC top-pick. | 2026-05-31 |
| SZSE:300383 | Beijing Sinnet (光环新网) | core | A-share IDC + cloud operator and historical AWS-China local partner; planning ~500MW of new AIDC additions in 2026 serving Baidu / Alibaba intelligent-agent compute; Q1 2026 revenue RMB 1.633bn (-10.83% YoY) reflects mid-cycle migration not structural break ([Sinnet Q1 2026 — eastmoney 4,000P+ commentary, 2026-04-22](https://emcreative.eastmoney.com/app_fortune/article/index.html?artCode=20260422222551089023030&postId=1697655624); [2025 annual report summary, 2026-04-29](https://stock.stockstar.com/notice/SN2026042900009896.shtml)). | 2026-05-31 |
| SZSE:300738 | Aofei Data (奥飞数据) | core | Wholesale + retail IDC with disclosed customer rolodex spanning Tencent / Baidu / Kuaishou / Kingsoft; Q1 2026 revenue RMB 703m (+31.15% YoY), net profit +79.19% YoY, OCF +104.65% YoY on smart-computing-centre delivery; April 2026 acceptance of RMB 2.1bn green-DC REITs application ([Aofei Q1 2026 results, sina, 2026-04-29](https://finance.sina.com.cn/roll/2026-04-29/doc-inhwczpc0981366.shtml); [strategic analysis, aigbk, 2026](https://www.aigbk.com/article/how_aofei_data_300738_benefits_from_ai_computing_lease_super_cycle/)). | 2026-05-31 |
| SSE:603881 | Sinodata / Shanghai AtHub (数据港) | core | Alibaba's primary third-party wholesale IDC partner via 5-DC build-and-operate agreement (10-yr term); Q1 2026 revenue RMB 380m (-3.76% YoY) but net profit +1.64% YoY with gross margin +8.7pp YoY as Alibaba-tied capacity matures into stable yield ([Shanghai AtHub Q1 2026 results, NBD, 2026-04-24](https://www.nbd.com.cn/articles/2026-04-24/4358733.html); [AtHub-Alibaba 5-DC mandate context, DCD](https://www.datacenterdynamics.com/en/news/shanghai-athub-to-build-and-operate-5-data-centers-for-alibaba/)). Original seed misattributed to 300523.SZ (Cheng'an Tech) — ticker corrected. | 2026-05-31 |
| HKEX:0700 | Tencent Holdings | adjacent | Q1 2026 capex RMB 31.9bn (+16% YoY / +63% QoQ); management guided to "substantial increase" in 2H 2026 on China-designed ASICs; Tencent Cloud international +40% YoY; inference-token monetisation building ([Yicai Global, 2026](https://www.yicaiglobal.com/news/tencents-first-quarter-profit-jumps-21-while-ai-spending-exceeds-usd44-billion); in-house [reports/company/Tencent_HKEX0700/](../company/Tencent_HKEX0700/)). | 2026-05-31 |
| HKEX:9988 | Alibaba Group | adjacent | Cloud Intelligence Group +38% YoY revenue in FY26 Q4; AI-product revenue triple-digit YoY for 11 consecutive quarters at RMB 8.97bn; pledged RMB 380bn 3-yr AI/cloud capex with explicit "will exceed" language ([Alibaba FY26 Q4 6-K, 2026](https://www.sec.gov/Archives/edgar/data/0001577552/000110465926060224/tm2614494d1_ex99-1.htm); in-house [reports/company/Alibaba_HKEX9988/](../company/Alibaba_HKEX9988/)). | 2026-05-31 |
| HKEX:9888 | Baidu Inc | adjacent | Q1 2026 AI Cloud revenue +79% YoY to RMB 8.8bn; GPU-cloud growth accelerated +128% → +184% YoY; AI revenue first crossed 50% of core revenue ([Baidu Q1 2026 deep-dive, futunn, 2026](https://q.futunn.com/en/feed/116610344223128); in-house [reports/company/Baidu_NASDAQ_BIDU/](../company/Baidu_NASDAQ_BIDU/)). | 2026-05-31 |
| HKEX:0941 | China Mobile | adjacent | 2026 computing-infra capex RMB 47.5bn (+21% YoY; 27% of total capex); intelligent-computing capacity guided from 10 → 17 EFLOPS in 2026; >US$4.3bn AI-server orders placed for 2026 ([Light Reading on Mobile $4.3B AI-server orders, 2026](https://www.lightreading.com/ai-machine-learning/china-mobile-orders-4-3b-in-servers-as-it-ramps-up-ai-infrastructure); [Mobile strategy narrative, simplywall](https://simplywall.st/community/narratives/hk/telecom/hkg-941/china-mobile-shares/bpo9e3nk-china-mobiles-strategy-is-centered-on-communications-computing-ai)). Cleanest large-cap telco DC pivot. | 2026-05-31 |
| HKEX:0728 | China Telecom | adjacent | 2026 total capex cut to RMB 73bn (-9.2%) but computing-power share rising to 35% (RMB 25.5bn, +26% YoY); pivot from "traffic" to "token-based" infra via Tianyi Cloud; 2025 AI-revenue base RMB 12.3bn already printed ([Caixin Global on Telecom capex pivot, 2026-03-25](https://www.caixinglobal.com/2026-03-25/china-telecom-to-boost-ai-spending-amid-capex-cut-and-slowing-growth-102426994.html)). | 2026-05-31 |
| SSE:688256 | Cambricon (寒武纪) | enabler | Q1 2026 revenue RMB 2.89bn (+160% YoY), net profit RMB 1bn (+185% YoY); 2026 shipment target 500k AI accelerators vs ~116k 2025; ByteDance ≈80% revenue concentration is the cleanest read-through to hyperscaler ASIC demand ([MarketScreener on Q1 2026 jumps, 2026](https://www.marketscreener.com/news/cambricon-s-profit-soars-185-in-q1-revenue-jumps-160-on-ai-boom-ce7f58d8d080f020); [Tom's Hardware, 2026](https://www.tomshardware.com/tech-industry/semiconductors/cambricon-targets-500000-ai-chips-in-2026-as-china-accelerates-domestic-hardware-push)). | 2026-05-31 |
| SSE:688041 | Hygon Information (海光信息) | enabler | Q1 2026 revenue RMB 4.03bn (+68.1% YoY); "Dual-Chip Strategy" (CPU + DCU) deployed in >20 industries and 300+ scenarios; named state-customer base spans the three telcos, several SOE banks, and major internet co's ([Hygon Q1 2026 results, futunn, 2026](https://news.futunn.com/en/post/69361075/hygon-information-technology-688041-2025-and-q1-2026-performance-meets)). | 2026-05-31 |
| SSE:603019 | Sugon / Dawning (中科曙光) | enabler | Q1 2026 revenue RMB 32bn (+23.7% YoY), net profit RMB 2.28bn (+22.2% YoY); full "chip-end-cloud-computing" stack including Hygon-affiliated AI silicon, servers, storage, liquid-cooled DC products and computing-services platform; May 2026 FlashNexus 9000 launch lifted cluster-IOPS 8× ([Sugon Q1 2026 results, futunn, 2026](https://news.futunn.com/post/72076714/sugon-603019-q1-2026-sees-dual-growth-in-revenue-and)). | 2026-05-31 |
| SZSE:000938 | Unisplendour / H3C (紫光股份) | enabler | 2025 full-year revenue RMB 96.7bn (+22.4% YoY); ICT-infra (H3C) segment RMB 76.8bn (+41.1% YoY) and 79.4% of group revenue; positioned as #2 China AI-server vendor and primary high-speed-switch supplier for BAT and telco AIDC build-out ([Unisplendour 2025 annual results, weeklyonstock, 2026-04-14](https://static.weeklyonstock.com/26/0414/AB2619070845770.html)). | 2026-05-31 |

**Geographic / role mix (14 tickers):** China-A 8 (57%) · HK 4 (29%) · US ADR 2 (14%). Role: core 5, adjacent 5, enabler 4.

## Exclusions

| Ticker | Reason for exclusion |
|---|---|
| Private: Chindata (WinTrix DC) | Largest private China-DC operator; Bain took it private 2023 at US$3.16bn, sold to Shenzhen Dongyangguang (HEC) consortium Sept 2025 at US$4bn — largest M&A in China-DC history ([Mingtiandi on Bain → HEC sale, 2025](https://www.mingtiandi.com/real-estate/data-centres/bain-capital-sells-chindata-china-data-centres-to-hec/)). Non-investable as equity. |
| Private: ByteDance | Single largest tenant in the basket (>RMB 200bn 2026 AI capex) but non-investable ([Digitimes, 2026-05-28](https://www.digitimes.com/news/a20260528VL212/bytedance-capex-qualcomm-infrastructure-data.html)). Reads through to Cambricon, Aofei, Sinodata. |
| NASDAQ:EQIX, NYSE:DLR | US DC REITs; out of scope by design — US DC exposure already in SPY which we use as benchmark (EQIX 1Y +24%, DLR 1Y +15%). Including them double-counts. |
| HKEX:3690 (Meituan) | Cloud / IDC is a marginal segment; no separately-tracked AI / cloud capex disclosure. Too diluted to be a DC-thesis name. |
| HKEX:1024 (Kuaishou) | Kling AI is a high-quality video-inference product (Q1 2026 revenue >RMB 650m, +300% YoY, ARR ~US$500m by March 2026) but it's an *AI-inference application* riding *somebody else's* infra ([Kuaishou Q1 2026 IR, 2026](https://www.prnewswire.com/news-releases/kuaishou-technology-announces-first-quarter-2026-unaudited-financial-results-302782888.html)). Belongs in `ai-content-monetization`. |
| HKEX:0762 (China Unicom) | Smallest of the three telcos and slowest pivot — 2026 capex cut ~8% to RMB 50bn while computing share moves to 35%; smaller absolute computing dollar than Mobile / Telecom ([Caixin Global, 2026-03-20](https://www.caixinglobal.com/2026-03-20/china-unicom-slashes-spending-pivots-harder-to-ai-102424845.html)). Re-evaluate if computing-share % beats 40%. |
| SZSE:002353 (Jereh) | DC-power gas-turbine win (~US$393m US orders Jan–Feb 2026, +50% YTD share-price move) is real but already tracked in `ai-power-electrification` — including here double-counts ([Sina on Jereh AI-power orders, 2026-02-27](https://finance.sina.com.cn/jjxw/2026-02-27/doc-inhphcxh3675282.shtml)). |
| HKEX:8178 (China Information Tech Development) | GEM-board name; price collapsed to HK$0.20, 1Y return -93%, liquidity too thin for meaningful tracking. |
| SZSE:000977 (Inspur) | #1 global AI-server share but Q1 2026 disappointment: revenue -24.3% YoY to RMB 35.5bn, OCF -RMB 7.77bn, gross margin 6.6% ([Inspur Q1 2026 reading, T-media, 2026](http://m.cniteyes.com/archives/40384)). Sugon + H3C provide cleaner enabler exposure. Watch for re-entry on Q2 margin stabilisation. |
| Dual listings (9698.HK / BABA / BIDU) | Where a US ADR and HK primary/secondary co-exist, basket tracks the more liquid line (NASDAQ ADR for GDS; HK primary for Tencent / Alibaba / Baidu). Companion line not weighted separately. |

## Keywords

China data center / 中国数据中心 · wholesale IDC / 批发型 IDC · hyperscale / 超大规模 · AIDC / AI 数据中心 · AI inference / AI 推理 · server OEM / 服务器整机 · liquid cooling / 液冷 · telco computing capex / 运营商算力资本开支 · AI accelerator / AI 加速卡 · tokens-as-a-service / Token 时代 · Tianyi Cloud / 天翼云 · Mobile Cloud / 移动云 · ASIC / 国产芯片 · Hunyuan / Qwen / Ernie / 大模型

## Performance (as of 2026-05-31, since-inception snapshot)

Returns are simple price returns from yfinance with `auto_adjust=True`, computed against the 2026-05-31 close. Tickers span US ADR, HK, and A-share venues; benchmarks reported separately.

**Equal-weight basket returns:** 3-month +2.9% · YTD 2026 +4.1% · trailing 1-year **+38.6%**.

**Benchmark returns over the same windows:**

| Benchmark | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| S&P 500 (SPY) | +10.6% | +11.0% | +30.2% |
| KraneShares CSI China Internet (KWEB) | −13.9% | −25.0% | **−14.6%** |
| Hang Seng ETF (2800.HK) | −4.5% | −3.6% | +9.4% |

**Read against benchmarks:** Basket 1Y +38.6% beats KWEB by +53pp, 2800.HK by +29pp, SPY by +8pp. The KWEB delta is the cleanest read of the alpha — KWEB carries the same hyperscalers but blends in e-commerce, gaming, and ed-tech that drag the index; the basket strips KWEB to the AI-capex-deploying half and adds IDC operators + inference chips not in the index at all.

**Per-ticker performance, sorted by 1-year return:**

| Ticker | 1Y | YTD | 3M | Close (local) |
|---|---|---|---|---|
| SSE:688256 (Cambricon) | **+188.7%** | +40.6% | +80.5% | 1,310.00 |
| SSE:688041 (Hygon) | +107.1% | +30.1% | +19.2% | 293.90 |
| NASDAQ:VNET | +87.0% | +10.6% | −6.5% | 10.08 |
| HKEX:9888 (Baidu) | +51.0% | −9.6% | +0.2% | 130.00 |
| NASDAQ:GDS | +43.1% | −7.5% | −14.2% | 35.45 |
| SSE:603019 (Sugon) | +40.0% | +0.6% | −2.6% | 87.84 |
| SSE:603881 (Sinodata / AtHub) | +34.0% | +12.4% | −7.8% | 35.40 |
| SZSE:000938 (Unisplendour / H3C) | +16.8% | +13.4% | +13.3% | 28.64 |
| HKEX:0941 (China Mobile) | +2.6% | +2.0% | +7.7% | 85.15 |
| HKEX:9988 (Alibaba) | −1.6% | −18.9% | −18.3% | 120.90 |
| SZSE:300738 (Aofei) | −1.3% | +13.9% | −6.8% | 21.76 |
| SZSE:300383 (Sinnet) | −3.1% | +5.5% | −11.8% | 13.66 |
| HKEX:0728 (China Telecom) | −6.5% | −5.3% | +4.4% | 5.18 |
| HKEX:0700 (Tencent) | −17.0% | −30.6% | −16.9% | 427.20 |

**Sub-group reads:**

| Sub-group | n | 3M | YTD | 1Y |
|---|---|---|---|---|
| Core IDCs (GDS, VNET, Sinnet, Aofei, Sinodata) | 5 | −9.4% | +7.0% | +32.0% |
| Adjacent hyperscalers + telcos (Tencent, Alibaba, Baidu, Mobile, Telecom) | 5 | −4.6% | −12.5% | +5.7% |
| Enabler chips + server OEMs (Cambricon, Hygon, Sugon, H3C) | 4 | +27.6% | +21.2% | +88.1% |

**Read of the dispersion:** The 1Y window is dominated by the *enabler* leg — Cambricon (+189%) and Hygon (+107%) carry over half the basket's lift. Within *core IDC*, VNET (+87%) is the event-driven standout (CATL tie-up + 519MW order-flow), GDS (+43%) the durable consensus-long. A-share IDCs (Sinnet, Aofei, Sinodata) sit in the +5–35% band on 1Y with bigger 3M drawdowns as Q1 prints showed the booking-vs-commissioning gap. The *adjacent* leg leaks alpha: Tencent (-17%) / Alibaba (-2%) / telco names trade lateral-to-negative despite rising absolute capex dollars — the equity story is the *margin-compression-from-AI-capex* counter-narrative the basket explicitly accepts as its hedge.

## Recent events (since basket inception)

Inception write; covers the prior ~90 days that informed ticker selection. Future refreshes will cover the window since the previous `Last refreshed` date.

- **GDS Q1 2026 (2026-05-20):** revenue RMB 3.367bn (+23.6% YoY); committed area +11.7% YoY to 725,485 sqm; cumulative committed capacity 1.8GW; YTD bookings >340MW; FY26 sales target ≥500MW; 3-yr capex RMB 30–50bn ([GDS Q1 2026 6-K](https://www.sec.gov/Archives/edgar/data/0001526125/000110465926064164/tm2614459d3_ex99-1.htm)).
- **VNET–CATL deal (2026-05-13):** CATL-linked vehicles agreed up to US$942m for as much as 38.1% of VNET; closing Q4 2026; ADR jumped >30% on news ([VNET 6-K, 2026](https://www.sec.gov/Archives/edgar/data/0001508475/000110465926059835/tm2614496d1_ex99-1.htm)).
- **VNET Q1 2026 (2026-05-20):** revenue +19.8% YoY to RMB 2.69bn; wholesale +58.1% YoY; YTD orders 519MW incl. one 400MW Beijing-area ticket; FY26 capex RMB 10–12bn ([VNET Q1 2026 IR](https://ir.21vianet.com/news-releases/news-release-details/vnet-reports-unaudited-first-quarter-2026-financial-results)).
- **Cambricon Q1 2026 (April):** revenue +160% YoY, net profit +185% YoY; 2026 shipment target 500k AI accelerators vs ~116k 2025 ([MarketScreener, 2026](https://www.marketscreener.com/news/cambricon-s-profit-soars-185-in-q1-revenue-jumps-160-on-ai-boom-ce7f58d8d080f020)).
- **Tencent Q1 2026 (2026-05-14):** capex RMB 31.9bn (+16% YoY / +63% QoQ); 2H 2026 guided to "substantial increase" on China-designed ASICs ([Yicai Global, 2026](https://www.yicaiglobal.com/news/tencents-first-quarter-profit-jumps-21-while-ai-spending-exceeds-usd44-billion)).
- **Alibaba FY26:** Cloud Intelligence Group +38% YoY; RMB 380bn 3-yr capex commitment with "will exceed" language ([Alibaba FY26 Q4 6-K](https://www.sec.gov/Archives/edgar/data/0001577552/000110465926060224/tm2614494d1_ex99-1.htm)).
- **Baidu Q1 2026:** AI Cloud +79% YoY; GPU-cloud +128% → +184% YoY; AI revenue first crossed 50% of core ([AlphaPilot, 2026](https://www.alphapilot.tech/discover/baidu-q1-2026-ai-revenue-surpasses-50-as-cloud-and-ernie-5-1-drive-growth)).
- **Telco 2026 budgets:** Telecom total capex RMB 73bn (-9.2%) with computing share to 35% (+26% YoY computing line) ([Caixin Global, 2026-03-25](https://www.caixinglobal.com/2026-03-25/china-telecom-to-boost-ai-spending-amid-capex-cut-and-slowing-growth-102426994.html)); Mobile computing capex +21% to RMB 47.5bn (27% of total); 10 → 17 EFLOPS; >US$4.3bn AI-server orders ([Light Reading, 2026](https://www.lightreading.com/ai-machine-learning/china-mobile-orders-4-3b-in-servers-as-it-ramps-up-ai-infrastructure)).
- **ByteDance 2026 AI capex revision (2026-05-27):** wires converged on >RMB 200bn / ~US$30bn, high-side scenarios at US$70bn — largest demand-pull signal in the basket ([Digitimes, 2026-05-28](https://www.digitimes.com/news/a20260528VL212/bytedance-capex-qualcomm-infrastructure-data.html); [Seeking Alpha, 2026](https://seekingalpha.com/news/4597242-bytedance-mulls-up-to-70b-in-capex-amid-ai-push)).
- **Chindata HEC sale (Sept 2025):** US$4bn — largest M&A in China-DC history; private-market base-rate ([Mingtiandi, 2025](https://www.mingtiandi.com/real-estate/data-centres/bain-capital-sells-chindata-china-data-centres-to-hec/)).

## Drift signals

This is the inception write — drift detection becomes the value-add starting from the *next* refresh. Initial flags:

- **AI-revenue-disclosure gap is the watch item.** Five of fourteen names do **not** yet separately disclose AI / cloud / IDC revenue as a clean P&L line: Sinnet, Aofei, Sinodata (by-customer but not by-AI-product), and the two telcos (capex breakdowns disclosed; AI revenue still embedded in services revenue). **This is a "watch the next earnings call" basket** — for these five names the thesis stays a forward-capex bet rather than a printed-revenue bet until H2 2026 segment disclosure improves, and the multiple-rerating thesis takes longer.
- **Rack-up cadence vs booking cadence is the GS-flagged risk.** GDS Q1 showed cumulative committed 1.8GW but utilised area grew only +12.7% YoY — the booking-to-recognition gap has widened. If GDS Q2 commissioning slips again, or VNET's 519MW YTD bookings show similar conversion lag, the operator leg will trade off the *next* booking number rather than the *cumulative* one.
- **Tencent / Alibaba margin-compression is the inverse-hedge trade.** Both names are negative on 1Y despite leading the China capex pivot; Alibaba's adj. net income fell 99.7% in FY26 Q4 to US$12m on AI investment ([WinBuzzer, 2026](https://winbuzzer.com/2026/05/15/alibaba-faces-mounting-margin-pressure-as-ai-inves-xcxwbn/)). The pattern reads like 2022 US hyperscaler capex-pain: the *deployer* takes the multiple hit while the *receiver* (IDCs, chips) rerates. If it persists, the adjacent leg structurally underperforms — but re-weighting to 0% adjacent makes the basket effectively a thematic short of Tencent / Alibaba into Cambricon / Hygon, which is not the construction the basket was built for.
- **Cambricon ASIC supply = single-point-of-failure for the enabler leg.** Cambricon's +189% 1Y embeds a 2026 ramp from 116k → 500k units, gated by SMIC 7nm yield (~20%) and HBM supply. A negative SMIC update or a ByteDance order-revision (80% concentration) would compress Cambricon faster than any other name.
- **Inspur (000977) re-add candidate.** Excluded on Q1 2026 print weakness; #1 global AI-server share is structural. Re-add at Q2 print if margins normalise to >12% on AI-server mix and OCF stabilises.
- **Watch list for future inclusion:** Kingsoft Cloud 3896.HK (on the GS list — re-evaluate); Volcengine (ByteDance cloud unit; IPO chatter recurrent); Kunlunxin (Baidu AI-chip arm — already filing per [NAI500, 2026](https://nai500.com/blog/2026/05/8-china-ai-chip-plays-to-watch-after-kunlunxin-s-filing/)). Any IPO triggers an immediate mutation.

## Catalysts (next 3–6 months)

- **GDS Q2 2026 (mid-August 2026):** commissioning-ramp print — utilised-area growth vs YTD booking — is the basket's most important single data point.
- **VNET Q2 2026 + CATL deal closing (Q4 2026):** incremental wholesale ticket size; CATL signoff; battery-storage-DC product roadmap.
- **Tencent / Alibaba / Baidu Q2 (August 2026):** Tencent's "substantial increase" 2H capex guide quantified; Alibaba's "exceed RMB 380bn" re-anchored; Baidu AI Cloud growth-deceleration test (Q1 +79% YoY — H2 base effect compresses comp).
- **Cambricon Q2 + ASIC delivery cadence:** progress to 500k 2026 target — any slip on SMIC 7nm yield or ByteDance volume revision is event-driven.
- **China telco mid-year reviews (August / September 2026):** Mobile and Telecom publish capex execution; confirm computing share %.
- **A-share IDC Q2 (August 2026):** Sinnet 500MW AIDC commissioning update; Aofei IDC REIT progression; Sinodata Alibaba-tied capacity ramp.
- **ByteDance H2 2026 capex revision wires:** further upward revision >RMB 200bn lifts the enabler leg in real time.
- **Kunlunxin IPO timeline:** if priced 2H 2026, immediate basket-mutation candidate.
- **HEC / Chindata strategic update:** could re-list in 12–24mo as the natural fifth core IDC.

## Data Used / 数据来源清单

**Market data**
- yfinance `auto_adjust=True` for prices, returns, market cap, sector — pulled 2026-05-31.
- Benchmarks: SPY (S&P 500 ETF), KWEB (KraneShares CSI China Internet ETF), 2800.HK (Hang Seng ETF).
- Anchor: 2026-05-31 close; windows 3M (~63 trading days), YTD-2026, trailing 1Y (~252 trading days).

**Per-ticker primary sources** — see Tracked tickers and References for inline URLs against each ticker's Q1 2026 results, capex guidance, and strategic disclosures.

**Industry research (theme-level)**
- [Goldman Sachs: cloud + DC top sub-sector; GDS / VNET / BABA / Kingsoft Cloud picks (futubull, 2026)](https://news.futunn.com/en/post/71011256/goldman-sachs-cloud-and-data-center-sectors-are-the-top) — central thesis.
- [TrendForce: top 9 CSPs 2026 capex US$830bn (PR Newswire, 2026-05)](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html) — global capex framing.
- [Omdia: China cloud infra Q4 2025 +26% YoY (2026-04)](https://omdia.tech.informa.com/pr/2026/apr/mainland-china-cloud-infrastructure-spending-rises-26percent-in-q4-2025-driven-by-ai-and-agent-growth) — industry backdrop.
- [Futurum AI Capex 2026 (2026)](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/) · [36Kr Q1 cloud battle (2026)](https://eu.36kr.com/en/p/3829726886847879).
- [Mingtiandi Bain → HEC Chindata US$4bn (2025)](https://www.mingtiandi.com/real-estate/data-centres/bain-capital-sells-chindata-china-data-centres-to-hec/) · [Bain Capital primary release (2025)](https://www.baincapital.com/news/bain-capital-announces-strategic-sale-wintrixs-china-operations-landmark-us4-billion) — private-market base-rate.
- [Digitimes / Bloomberg on ByteDance 2026 ~US$70bn (2026-05-28)](https://www.digitimes.com/news/a20260528VL212/bytedance-capex-qualcomm-infrastructure-data.html) — largest demand-pull signal.

**zsxq evidence (theme-level, file_ids referenced from the brief — PDFs not opened)**
- `585412184888824` — GS Q1 2026 China DC 中概股 review ("产能扩张与上架节奏偏缓但订单动能依旧强劲") — flagship thesis citation.
- `812485545245182` — HSBC VNET buy / 首选标的; `212485522841581` — MS GDS 2026亚洲AI峰会要点; `212485545245111` — UBS Baidu 2026 analyst day; `184152212415212` — UBS Tencent 2026 AIC; `415284424524258` — MS Tencent SPARK; `415284812111218` — GS 三大运营商 AI Token; `184152244582842` — MS 能源遇见算力 (DC + power); `415284424524248` — Nomura Kuaishou (supports exclusion); `415284424524118` — MS CATL 3750.HK (VNET-CATL context); `812485545441122` — 互联网传媒AI专题.

**Macro backdrop (as of 2026-05-22 / 2026-05-25 latest, from `db/indicators.db`)**
- VIX: 16.68 (low-vol regime; supports risk-asset positioning). 10Y Treasury (TNX): 4.558% (2026-05-22). HYG: 79.91 (supportive credit backdrop for capex-intensive issuers). LQD: 108.37. DXY: 98.99 (USD soft — modest tailwind on translation for non-USD basket lines). 3M T-bill: 3.585%. Yield spread (10Y - 3M): 0.973%. Gold: 413.82. Oil: 96.60. VVIX: 91.16.

**Cross-coverage (existing in-house company research read as structured input, not cited inline)**
- [reports/company/Tencent_HKEX0700/](../company/Tencent_HKEX0700/) (Tencent) · [reports/company/Alibaba_HKEX9988/](../company/Alibaba_HKEX9988/) and [reports/company/Alibaba_NYSE_BABA/](../company/Alibaba_NYSE_BABA/) (Alibaba) · [reports/company/Baidu_NASDAQ_BIDU/](../company/Baidu_NASDAQ_BIDU/) (Baidu).

**Stale notices / coverage gaps**
- No in-house company-research for GDS, VNET, Sinnet, Aofei, Sinodata, Mobile, Telecom, Cambricon, Hygon, Sugon, or Unisplendour/H3C — eleven gaps; highest-priority: GDS (flagship) and Cambricon (largest 1Y contributor + single-point-of-failure concentration).
- yfinance market-cap returned `None` for A-share / HK lines on bulk-pull; supplement from `market_cap_cache.db` at next refresh for any weighted-basket calculation.
- AI / cloud / IDC revenue not separately disclosed for five names (Sinnet, Aofei, Sinodata, Mobile, Telecom); flagged in Drift signals.
- zsxq PDFs not opened (per brief); file_ids surfaced for context only.

## References

Per-ticker primary sources are linked inline in the **Tracked tickers** justifications, **Exclusions**, and **Recent events**. Industry / theme-level sources are linked in **Data Used** above. All URLs above are unique and verified at write-time (2026-05-31).

## History

- 2026-05-31 — theme created with 14-ticker basket (5 core IDCs, 5 adjacent hyperscalers + telcos, 4 enabler chips/server-OEMs). Tickers cut from seed: Sinodata corrected from misattributed SZSE:300523 (Cheng'an Tech) to actual SSE:603881 (Shanghai AtHub); Inspur 000977, Kuaishou 1024, Meituan 3690, China Unicom 0762, Jereh 002353, and CITD 8178 dropped to Exclusions per reasons in that table; EQIX / DLR / Chindata / ByteDance excluded by scope. Equal-weight basket +38.6% 1Y vs KWEB −14.6% / 2800.HK +9.4% / SPY +30.2%; enablers +88% 1Y, cores +32% 1Y, adjacents +6% 1Y.
