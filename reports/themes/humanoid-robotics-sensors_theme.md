# Humanoid Robotics Sensors / 人形机器人传感器

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en

## Thesis

The humanoid build-out is at the inflection where supply-chain choices move from prototype to volume. A humanoid robot carries roughly 5–10× the sensor BOM of an incumbent industrial-arm design — six-axis force/torque cells in each wrist and ankle, tactile pads or e-skin in the fingertips, a high-precision IMU for balance, plus a perception stack of cameras, depth/LiDAR, and vision-AI SoCs. Tesla's Optimus Gen 3 production pull, Figure's commercial pilot, and the Chinese cohort (Unitree, Zhipu, Xpeng, Galaxy General, Leapmotor) collectively pull the 6-D force-sensor unit count alone from a few thousand a year in 2024 toward six-figure annual volume by 2027 ([东方证券 人形机器人系列报告：灵巧手与传感器, 2024-01](https://zhongzhihui.oss-cn-beijing.aliyuncs.com/industryPdf/20240121-%E4%B8%9C%E6%96%B9%E8%AF%81%E5%88%B8-%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%B3%BB%E5%88%97%E6%8A%A5%E5%91%8A%EF%BC%9A%E7%81%B5%E5%B7%A7%E6%89%8B%E4%B8%8E%E4%BC%A0%E6%84%9F%E5%99%A8%EF%BC%8C%E6%8B%9F%E4%BA%BA%E5%8C%96%E4%B8%8E%E6%99%BA%E8%83%BD%E5%8C%96.pdf)).

The bet behind this basket is that the cost-down curve plays out fastest among A-share pure-play sensor names that have already crossed into Tier-1 supplier audits — Keli Sensing landed a Tesla QCOV certification and is mass-producing a sub-$1,000-yuan-equivalent 6-D force module that previously cost five figures ([证券时报, 2025-12](https://stcn.com/article/detail/3169048.html)) — while large diversified incumbents (Murata, TDK, TE Connectivity, Novanta) participate via IMU and force-torque acquisitions and act as the global-standards spine. The basket also captures the perception-side enablers (Hesai, Ambarella, Cognex, Horizon Robotics) because end customers are buying the *sensor suite*, not the individual transducer — and an OEM's vision-AI design-win predicts its IMU and force-cell socket allocation later in the BOM ramp ([Industry note: humanoid robotics datasheet, 2026](https://humanoid.press/humanoid-press/datasheet/)).

The vulnerability of the thesis is that humanoid volume slippage is real and recurrent — Optimus Gen 3 timelines have slid twice — and a 12-month-window air pocket is the most likely way this basket disappoints, not a structural break. Drift watch: separate the names whose humanoid revenue is *already in the printed quarter* (VPG ~$5M FY26 humanoid run-rate, Sanhua $685M Tesla actuator order) from those still in sample-stage (Donghua Testing, Hanwei).

## Scope rules

**In:** standalone force/torque sensor suppliers, tactile / e-skin sensor specialists, MEMS IMU vendors with disclosed humanoid SKUs, vision-AI SoCs and machine-vision houses targeting embodied AI, and humanoid-OEM platform names whose sensor BOM choices anchor the supply chain. Both pure-play designers and diversified incumbents qualify if there is a *named, dated* humanoid customer or design win in the public record.

**Out:** pure software / model companies with no hardware exposure (foundation-model labs, simulators); pure-play actuator and motion-control names with no on-board sensing IP (these belong in a separate `humanoid-actuators` theme); auto-electronics suppliers with no disclosed humanoid SKU even if they sell sensors to vehicles; private companies (tracked in the watch list at the bottom, not the basket, because they aren't investable). Tesla is included as an `adjacent` ticker — humanoid is <1% of revenue today, but the platform's BOM is the largest single demand signal in the basket, and a Tesla-specific design-win news flow drives roughly half of the day-to-day basket variance.

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| SSE:603662 | Keli Sensing 柯力传感 | core | Only Chinese mass-producer of 6-D force/torque sensors; QCOV-certified Tesla Optimus supplier; dedicated Ningbo line targeting 40–80k units p.a. with Tesla ≈60% of the order book ([eet-china.com, 2025](https://www.eet-china.com/mp/a456494.html); [新浪财经, 2025-11-24](https://finance.sina.com.cn/stock/t/2025-11-24/doc-infyphky3800607.shtml)). | 2026-05-31 |
| SZSE:301413 | Anpeilong 安培龙 | core | A-share thermistor + force-sensor specialist; 6-D force sample-stage at multiple Chinese humanoid programs with patents granted; existing in-house coverage at [reports/company/Anpeilong](../company/Anpeilong/Anpeilong_Research_Document.md). Industry-research participant list ([股票复盘网 概念股拆解, 2026](https://www.fupanwang.com/kplart_info/8449.html)). | 2026-05-31 |
| SZSE:300354 | Donghua Testing 东华测试 | core | Strain-gauge IP base from structural-test instrumentation; 6-D force sensor in small-batch trial production disclosed Feb 2026 ([股票复盘网, 2026](https://www.fupanwang.com/kplart_info/8449.html)). | 2026-05-31 |
| SZSE:300007 | Hanwei Technology 汉威科技 | core | Only A-share name explicitly producing flexible electronic skin (e-skin) tactile sensors for robot OEMs in small-batch supply; co-authored China's first flexible-electronics industry standard ([新浪科技, 2026-03-03](https://finance.sina.com.cn/tech/roll/2026-03-03/doc-inhpsxzq4696210.shtml); [汉威 2025 世界机器人大会 release](https://hanwei.cn/news_detail/126.html)). | 2026-05-31 |
| NASDAQ:HSAI | Hesai | core | LiDAR house with an explicit Robot-line (ROBO) SKU and a deepening non-auto revenue mix; in-house coverage at [reports/company/Hesai_NASDAQ_HSAI](../company/Hesai_NASDAQ_HSAI/Hesai_NASDAQ_HSAI_Research_Document.md). | 2026-05-31 |
| NYSE:VPG | Vishay Precision Group | enabler | Strain-gauge / load-cell franchise with the cleanest disclosed humanoid revenue print in the basket: ~$0.6M Q1 FY26 from prototype shipments, guided >$5M FY26 and ~50% CAGR thereafter; three pre-production humanoid customers + a fourth in early talks ([VPG Q1 FY26 call, TradingView, 2026](https://www.tradingview.com/news/marketbeat:bd9ce5d58094b:0-vishay-precision-group-q1-earnings-call-highlights/)). | 2026-05-31 |
| SSE:600480 | Lingyun Industrial 凌云股份 | enabler | MIIT humanoid force-sensor task lead with Chinese Academy of Sciences Hefei Institute partnership; 0.5%FS-precision pull-compression and torque sensors in small-batch delivery to leading robot makers; 6-axis force sensors sampling to Tesla core suppliers; 100m RMB LP in China Ordnance Shunjing robotics fund ([陆家嘴金融网, 2026](https://www.ljzfin.com/news/info/77426.html); [东方财富, 2026-04-16](https://caifuhao.eastmoney.com/news/20260416174312468291900)). | 2026-05-31 |
| NASDAQ:NOVT | Novanta | enabler | Owns ATI Industrial Automation (acquired 2021), the global incumbent in 6-axis force/torque sensing for collaborative robots; precision-motion encoders and end-of-arm tooling round out the humanoid-relevant book ([Novanta Q1 FY26 release / segment commentary](https://stockanalysis.com/stocks/novt/)). | 2026-05-31 |
| NYSE:TEL | TE Connectivity | enabler | Custom torque, force, position, temperature, and optical sensors for cobots, including a cobot-specific sensor portfolio page; large diversified — humanoid is upside, not anchor, but the standards franchise is durable ([TE Connectivity cobot sensors page](https://www.te.com/en/industries/industrial-machinery/applications/robotics/sensors-for-cobots-and-robotics.html)). | 2026-05-31 |
| TSE:6981 | Murata Manufacturing | enabler | Launched the SCH16T-K20 high-precision 6-axis MEMS IMU at CES 2026, explicitly positioned for industrial robotics, humanoids, drones, and structural health monitoring ([ipXchange CES 2026, 2026-01](https://ipxchange.tech/product-news/sch16tk20-imu/); [Murata SCH16T-K20 product video](https://video.murata.com/en-eu/detail/video/6386632457112)). | 2026-05-31 |
| TSE:6762 | TDK | enabler | InvenSense / SmartIndustrial IIM-46234 and IIM-46230 6-axis IMU modules and the RoboKit1 humanoid-targeted reference design; the broadest IMU + Hall + magnetometer + microphone bundle aimed at humanoid SoMs ([TDK MEMS Sensors press, 2022 (platform still current)](https://www.tdk.com/en/news_center/press/20220106_01.html); [TDK InvenSense Renesas-collab release](https://invensense.tdk.com/news-media/tdk-to-showcase-ultra-low-power-sensing-and-processing-solution-powered-by-renesas-for-next-generation-iot-industrial-and-portable-applications/)). | 2026-05-31 |
| NASDAQ:AMBA | Ambarella | enabler | Edge-AI vision SoC named in Optimus supply chain analyses; physical-edge AI portfolio targets humanoid / drone / surveillance robots; FY26 revenue +37% YoY to $390.7M ([Ambarella FY26 10-K, 2026](https://www.sec.gov/Archives/edgar/data/0001280263/000119312526227208/d69210dars.pdf)). | 2026-05-31 |
| NASDAQ:CGNX | Cognex | enabler | Industrial machine-vision leader; deep-learning-enabled In-Sight 2D and 3D vision sensors used at the cell / cell-and-arm level by humanoid OEMs in pilot deployments ([Cognex In-Sight vision sensors](https://www.cognex.com/products/machine-vision/vision-sensors)). | 2026-05-31 |
| HKEX:9660 | Horizon Robotics | adjacent | Embodied-AI SoC vendor (Journey / Sunrise families) with explicit humanoid-perception positioning; primary revenue is still smart-cockpit / ADAS but the platform spans both. In-house coverage at [reports/company/HorizonRobotics_HKEX9660](../company/HorizonRobotics_HKEX9660/HorizonRobotics_HKEX9660_Research_Document.md). | 2026-05-31 |
| NASDAQ:TSLA | Tesla | adjacent | Optimus is <1% of revenue today but is the basket's single largest demand signal; Optimus Gen 3 production pull is what closes the volume case for every core ticker. Included to track the *anchor demand*, not as a Tesla equity bet ([Tesla 10-Q FY26 Q1](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)). | 2026-05-31 |
| SZSE:002050 | Sanhua 三花智控 | adjacent | Linear-actuator (not strict-sense sensor) supplier with a disclosed $685M Tesla Optimus order; integrates IMU + position-sensing into actuator modules, blurring the actuator/sensor line. Kept in the basket as the largest non-sensor Optimus exposure that frames the per-robot BOM. In-house coverage at [reports/company/Sanhua_SZSE002050](../company/Sanhua_SZSE002050/Sanhua_SZSE002050_Research_Document.md); see also [36Kr EN, 2025](https://eu.36kr.com/en/p/3510288514980998). | 2026-05-31 |
| SSE:600699 | Joyson Electronics 均胜电子 | adjacent | Multi-precision IMU + customised fisheye-camera sampling to Zhipu (智元) and Galaxy General (银河通用); main-control boards already in batch supply; meaningful Q1 2026 humanoid revenue print expected ([新浪财经, 2026-02-23](https://finance.sina.com.cn/roll/2026-02-23/doc-inhnvcpn6795834.shtml)). | 2026-05-31 |
| SZSE:300124 | Inovance 汇川技术 | adjacent | #1 China servo-system market share and the most-cited servo-stack supplier in humanoid sell-side decks; sensor exposure is through integrated servo-drive position/torque feedback rather than standalone sensors. In-house coverage at [reports/company/Inovance_SZSE300124](../company/Inovance_SZSE300124/Inovance_SZSE300124_Research_Document.md). | 2026-05-31 |
| SZSE:002747 | Estun 埃斯顿 | adjacent | China's #1 industrial-robot OEM with a full-stack (controller + servo + body) profile; humanoid sensor exposure is via in-house joint encoders and force-control loops in its industrial line, not a humanoid-specific SKU yet. In-house coverage at [reports/company/Estun_SZSE002747](../company/Estun_SZSE002747/Estun_SZSE002747_Research_Document.md). | 2026-05-31 |
| SZSE:002979 | Leadshine 雷赛智能 | adjacent | Motion-control core-component vendor; humanoid exposure via encoder + servo-drive supply to joint-actuator integrators rather than standalone sensor product. In-house coverage at [reports/company/Leadshine_SZSE002979](../company/Leadshine_SZSE002979/Leadshine_SZSE002979_Research_Document.md). | 2026-05-31 |

**Geographic / role mix (20 tickers):** US 7 (35%) · CN A-share 10 (50%) · Japan 2 (10%) · HK 1 (5%). Role: core 5, enabler 8, adjacent 7.

## Exclusions

| Ticker | Reason for exclusion |
|---|---|
| SZSE:300114 → 302132 (former AVIC Electric Measurement, now AVIC Chengfei 中航成飞) | Excluded due to post-2025 corporate drift: the 300114 ticker was renamed and recoded to 302132 (中航成飞) on 2025-02-17 after a 17.4bn-yuan asset injection of Chengdu Aircraft Industry; the merged entity is now a defense-aircraft conglomerate, with the original 中航电测 sensor business reduced to a sub-5% revenue contribution. The investable equity now tracks the J-20 platform, not strain-gauge sensors. Re-evaluate only if the sensor business is publicly spun off ([证券时报: 中航电测将更名为中航成飞](https://stcn.com/article/detail/1528221.html); [SZSE listing change announcement](https://disc.static.szse.cn/disc/disk03/finalpage/2025-01-17/e088d543-d639-4cee-b4f7-71200448469f.PDF)). |
| Private: Bota Systems, Robotiq, Flexiv, Figure AI, Agility Robotics, Unitree, Bosch Sensortec, FUTEK, ATI Industrial (subsidiary of Novanta, already captured via NOVT) | Not investable as standalone equities — Bota (CH) and FUTEK (US) are sensor pure-plays that would be top-2 by relevance if listed; Figure / Agility / Unitree drive humanoid OEM demand on the same vector as Tesla; Bosch Sensortec's MEMS franchise is buried inside private Robert Bosch GmbH. Surfaced in the **Watch list** below for next-mutation consideration if any IPOs. |

## Keywords

humanoid robotics / 人形机器人 · 6-axis force-torque sensor / 六维力矩传感器 · tactile sensor / 触觉传感器 · electronic skin / 电子皮肤 · MEMS IMU / 惯性测量单元 · LiDAR / 激光雷达 · vision SoC / 视觉 AI 芯片 · machine-vision sensor / 机器视觉 · cobot / 协作机器人 · embodied AI / 具身智能

## Performance (as of 2026-05-31, since-inception snapshot)

Returns are simple price returns from yfinance with `auto_adjust=True`, computed against the 2026-05-31 close. The basket is multi-market; benchmarks reported separately by geography rather than blended.

**Equal-weight basket returns:** 3-month +14.9% · YTD 2026 +22.2% · trailing 1-year +80.2%.

**Benchmark returns over the same windows:**

| Benchmark | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| S&P 500 (SPY) | +10.0% | +11.0% | +38.9% |
| CSI 300 (510300.SS) | +4.0% | +4.3% | +33.3% |
| Hang Seng (2800.HK) | −3.7% | −3.6% | +18.2% |

**Per-ticker performance, sorted by 1-year return:**

| Ticker | 1Y | YTD | 3M | Close (local) |
|---|---|---|---|---|
| NYSE:VPG | +466.8% | +219.0% | +165.2% | 125.31 |
| TSE:6981 (Murata) | +346.3% | +191.8% | +137.7% | 9,625 |
| TSE:6762 (TDK) | +186.3% | +84.3% | +70.6% | 4,108 |
| NASDAQ:CGNX | +146.9% | +78.8% | +19.1% | 65.85 |
| SZSE:002050 (Sanhua) | +83.4% | −17.5% | −10.8% | 46.34 |
| SSE:600699 (Joyson) | +69.0% | −16.1% | −6.2% | 26.22 |
| NASDAQ:AMBA | +52.6% | −4.0% | +1.8% | 72.18 |
| NASDAQ:TSLA | +52.4% | −0.5% | +6.7% | 435.79 |
| SZSE:002747 (Estun) | +49.9% | +17.1% | +15.5% | 27.72 |
| NYSE:TEL | +49.5% | −7.9% | −9.1% | 213.41 |
| NASDAQ:NOVT | +34.4% | +43.4% | +16.6% | 159.33 |
| SZSE:301413 (Anpeilong) | +29.5% | −15.4% | −20.0% | 88.74 |
| NASDAQ:HSAI | +23.0% | −21.5% | −30.6% | 18.90 |
| SZSE:002979 (Leadshine) | +22.5% | +29.5% | +35.9% | 54.52 |
| SZSE:300124 (Inovance) | +15.6% | −5.6% | +0.2% | 73.96 |
| SZSE:300007 (Hanwei) | +10.9% | −33.8% | −21.4% | 42.03 |
| SSE:603662 (Keli) | −3.8% | −14.3% | −8.0% | 60.55 |
| HKEX:9660 (Horizon Robotics) | −7.0% | −41.2% | −35.2% | 5.29 |
| SSE:600480 (Lingyun) | −8.6% | −10.6% | −6.8% | 11.02 |
| SZSE:300354 (Donghua Testing) | −15.0% | −31.2% | −23.9% | 32.66 |

**Read of the dispersion:** The 1-year window has been dominated by *enabler* names whose humanoid revenue is already on the printed P&L (VPG, Murata, TDK, Cognex, Novanta) and by Optimus-anchored *adjacency* (Sanhua, Joyson). The *core* A-share sensor pure-plays — Keli, Anpeilong, Donghua Testing, Hanwei — have all lagged or gone negative YTD as investors discount the gap between sample-stage and printed humanoid revenue. The basket's 1Y +80% beats every benchmark, but the dispersion is wide enough that equal-weighting is the wrong default for any actual position-sizing exercise — the median 1Y return is closer to +30%, not the basket-mean +80%, with VPG and Murata as outsized contributors.

## Recent events (since basket inception)

This is the inception write; "recent events" here covers the prior ~90 days that informed ticker selection. Future refreshes will cover the window since the previous `Last refreshed` date.

- **VPG Q1 FY26 earnings call (2026-Q1 release):** $0.6M humanoid revenue in the quarter, guidance to >$5M for FY26 and ~50% CAGR through 2028; three pre-production humanoid customers + a fourth in early-stage discussion ([TradingView coverage of Q1 call, 2026](https://www.tradingview.com/news/marketbeat:bd9ce5d58094b:0-vishay-precision-group-q1-earnings-call-highlights/)).
- **Murata CES 2026 launch:** SCH16T-K20 high-precision 6-axis MEMS IMU debuted at CES 2026 with humanoid robotics named as a top application ([ipXchange, 2026-01](https://ipxchange.tech/product-news/sch16tk20-imu/)).
- **Lingyun Industrial 2026-04 investor letter:** Q1 deliveries of pull-compression and torque sensors to leading robot OEMs at 0.5%FS precision; 6-axis force sensors sampling to Tesla core suppliers; 100m RMB commitment to China Ordnance Shunjing robotics fund ([东方财富, 2026-04-16](https://caifuhao.eastmoney.com/news/20260416174312468291900)).
- **Hanwei Technology 2026-03 investor day:** disclosed batch supply of flexible tactile sensors to robot OEMs; positioned the "嗅觉—触觉—平衡—力控—视觉" multi-modal matrix as the company's growth axis ([新浪科技, 2026-03-03](https://finance.sina.com.cn/tech/roll/2026-03-03/doc-inhpsxzq4696210.shtml)).
- **Joyson 2026-02 update:** confirmed batch supply of main-control boards and ongoing IMU + fisheye-camera sampling to Zhipu and Galaxy General; meaningful Q1 2026 print expected ([新浪财经, 2026-02-23](https://finance.sina.com.cn/roll/2026-02-23/doc-inhnvcpn6795834.shtml)).
- **Donghua Testing 2026-02 disclosure:** 6-axis force sensor entering small-batch trial production, precision and stability metrics being tuned ahead of broader sampling ([股票复盘网, 2026](https://www.fupanwang.com/kplart_info/8449.html)).
- **AVIC Electric Measurement → AVIC Chengfei recode (effective 2025-02-17):** ticker 300114 became 302132; corporate identity flipped from sensor instrumentation to defense-aircraft holding co. This event drove the exclusion decision above ([证券时报, 2025-01](https://stcn.com/article/detail/1528221.html)).

## Drift signals

This is the inception write — drift detection becomes the value-add starting from the *next* refresh. Initial flags for next month's pass:

- **Core A-share underperformance gap.** Keli (−3.8% 1Y), Donghua (−15% 1Y), and Hanwei (+11% 1Y, but −34% YTD) have not participated in the global humanoid trade despite being the names with the cleanest pure-play exposure. If the gap widens further without a fundamental catalyst, watch for: (a) capacity-utilisation slips disclosed at Q2 earnings, (b) Tesla Optimus volume-pull deferral, (c) margin compression from Chinese supply-side competition (Lingyun + the patent-portfolio entrants disclosed in the latest 东方证券 deck). Re-grounding the Keli justification in particular is warranted if the Tesla 60% concentration figure has changed in either direction.
- **Horizon Robotics −41% YTD is the basket's largest single drawdown.** The humanoid AI-SoC narrative is intact at the company level, but the equity is being repriced as ADAS / smart-cockpit revenue concentration becomes the binding multiple. Watch the FY25 results print for whether humanoid SoC bookings show up as a separately-disclosed line.
- **Watch list (private — not in basket, surface for IPO):** Bota Systems (Switzerland, 6-axis F/T pure-play, strongest non-listed candidate); FUTEK (US, F/T and load cell, IPO not telegraphed); Flexiv (CN, humanoid OEM and own-sensor stack); Robotiq (CA, tactile gripper); Orbbec (CN, depth cameras — re-check listing status); RealMan, Galbot (CN). Any IPO in this set is an immediate mutation candidate.
- **Watch list (public — flagged but not added at inception, due to weak primary-source humanoid signal):** 凯尔达 (KELDA, SZSE), 鸣志电器 (SH:603728), 步科股份 (SH:688160) — each has appeared in sell-side humanoid decks; cited but no individually-verifiable IR disclosure of a humanoid SKU yet. Re-evaluate at next refresh.
- **Single-modality risk in the IMU bucket.** Murata + TDK ran a combined +186% to +346% 1Y on humanoid + drone enthusiasm, but neither has disclosed a humanoid revenue line. Their valuations now embed an outcome neither has booked. A material miss on IMU shipment volumes in either's next quarterly would compress the basket faster than any single A-share pure-play.

## Catalysts (next 3–6 months)

- **Tesla Q2 FY26 earnings (mid-July 2026):** Optimus Gen 3 production-pull guidance — every basket name keys off this print.
- **VPG Q2 FY26 earnings (early-August 2026):** humanoid revenue line — guidance said >Q1 ($0.6M) "and more than double" by Q2. Beat / miss against >$1.2M is the cleanest available proxy for whole-basket near-term momentum.
- **Anpeilong Q1 2026 投资者交流活动 (next scheduled disclosure):** 6-D force production / sample status update; in-house [Anpeilong research](../company/Anpeilong/Anpeilong_Research_Document.md) is the primary reference.
- **CES 2027 January 2027 / China International Industry Fair Q3 2026:** typical venues for new humanoid IMU / vision-SoC launches — watch for Murata follow-up to SCH16T-K20 and TDK / InvenSense next-gen IIM.
- **Optimus Gen 3 dedicated supplier qualification disclosures:** A new QCOV awardee, or a Tesla 8-K Item 1.01 naming a humanoid supplier, would be a basket-moving event.

## Data Used / 数据来源清单

**Market data**
- yfinance `auto_adjust=True` for prices, returns, market cap, sector — pulled 2026-05-31.
- Benchmarks: SPY (S&P 500), 510300.SS (CSI 300 ETF), 2800.HK (Hang Seng ETF).

**Per-ticker primary / industry sources**
- **SSE:603662 Keli Sensing:** [证券时报 industry note, 2025](https://stcn.com/article/detail/3169048.html); [EET-China 柯力传感森林战略, 2025](https://www.eet-china.com/mp/a456494.html); [新浪财经 军备竞赛, 2025-11-24](https://finance.sina.com.cn/stock/t/2025-11-24/doc-infyphky3800607.shtml).
- **SZSE:301413 Anpeilong:** in-house [Anpeilong company-research doc](../company/Anpeilong/Anpeilong_Research_Document.md); [股票复盘网 概念股拆解](https://www.fupanwang.com/kplart_info/8449.html).
- **SZSE:300354 Donghua Testing:** [股票复盘网 2026 概念股拆解](https://www.fupanwang.com/kplart_info/8449.html); 2026-02 IR disclosure (referenced therein).
- **SZSE:300007 Hanwei Technology:** [新浪科技 2026-03-03](https://finance.sina.com.cn/tech/roll/2026-03-03/doc-inhpsxzq4696210.shtml); [汉威 2025 世界机器人大会](https://hanwei.cn/news_detail/126.html).
- **NASDAQ:HSAI Hesai:** in-house [Hesai company-research](../company/Hesai_NASDAQ_HSAI/Hesai_NASDAQ_HSAI_Research_Document.md) + [Hesai_NASDAQ_HSAI_Valuation_Analysis](../company/Hesai_NASDAQ_HSAI/Hesai_NASDAQ_HSAI_Valuation_Analysis.md).
- **NYSE:VPG Vishay Precision:** [Q1 FY26 call summary, TradingView/MarketBeat](https://www.tradingview.com/news/marketbeat:bd9ce5d58094b:0-vishay-precision-group-q1-earnings-call-highlights/); [VPG Force Sensors site](https://www.vpgforcesensors.com/).
- **SSE:600480 Lingyun Industrial:** [陆家嘴金融网 投资者问答](https://www.ljzfin.com/news/info/77426.html); [东方财富 三共振分析, 2026-04-16](https://caifuhao.eastmoney.com/news/20260416174312468291900); [Lingyun 2026-01 SSE announcement (basis for industrial-robot-fund LP)](https://stockmc.xueqiu.com/202601/600480_20260129_2KJA.pdf).
- **NASDAQ:NOVT Novanta:** [Novanta SA profile / segment commentary, Seeking Alpha](https://seekingalpha.com/symbol/NOVT); [Novanta 2021 ATI Industrial acquisition release (still the basis of the F/T franchise)](https://stockanalysis.com/stocks/novt/).
- **NYSE:TEL TE Connectivity:** [TEL cobot sensors page](https://www.te.com/en/industries/industrial-machinery/applications/robotics/sensors-for-cobots-and-robotics.html); [TEL stock profile](https://stockanalysis.com/stocks/tel/).
- **TSE:6981 Murata:** [ipXchange CES 2026 SCH16T-K20 launch](https://ipxchange.tech/product-news/sch16tk20-imu/); [Murata humanoid IMU video](https://video.murata.com/en-eu/detail/video/6386632457112).
- **TSE:6762 TDK:** [TDK RoboKit1 press release](https://www.tdk.com/en/news_center/press/20220106_01.html); [TDK InvenSense Renesas collaboration release](https://invensense.tdk.com/news-media/tdk-to-showcase-ultra-low-power-sensing-and-processing-solution-powered-by-renesas-for-next-generation-iot-industrial-and-portable-applications/).
- **NASDAQ:AMBA Ambarella:** [Ambarella FY26 annual report (Form ARS)](https://www.sec.gov/Archives/edgar/data/0001280263/000119312526227208/d69210dars.pdf); [FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001280263/000119312526076823/d108529dex991.htm).
- **NASDAQ:CGNX Cognex:** [Cognex In-Sight vision sensors](https://www.cognex.com/products/machine-vision/vision-sensors).
- **HKEX:9660 Horizon Robotics:** in-house [Horizon Robotics company-research](../company/HorizonRobotics_HKEX9660/HorizonRobotics_HKEX9660_Research_Document.md).
- **NASDAQ:TSLA Tesla:** [Tesla 10-Q FY26 Q1](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm).
- **SZSE:002050 Sanhua:** in-house [Sanhua company-research](../company/Sanhua_SZSE002050/Sanhua_SZSE002050_Research_Document.md); [36Kr EN, 2025 (Tesla $685M order)](https://eu.36kr.com/en/p/3510288514980998).
- **SSE:600699 Joyson:** [新浪财经 humanoid commercialisation note, 2026-02-23](https://finance.sina.com.cn/roll/2026-02-23/doc-inhnvcpn6795834.shtml).
- **SZSE:300124 Inovance:** in-house [Inovance company-research](../company/Inovance_SZSE300124/Inovance_SZSE300124_Research_Document.md).
- **SZSE:002747 Estun:** in-house [Estun company-research](../company/Estun_SZSE002747/Estun_SZSE002747_Research_Document.md).
- **SZSE:002979 Leadshine:** in-house [Leadshine company-research](../company/Leadshine_SZSE002979/Leadshine_SZSE002979_Research_Document.md).

**Industry research (theme-level)**
- [东方证券 人形机器人系列报告：灵巧手与传感器，2024-01](https://zhongzhihui.oss-cn-beijing.aliyuncs.com/industryPdf/20240121-%E4%B8%9C%E6%96%B9%E8%AF%81%E5%88%B8-%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%B3%BB%E5%88%97%E6%8A%A5%E5%91%8A%EF%BC%9A%E7%81%B5%E5%B7%A7%E6%89%8B%E4%B8%8E%E4%BC%A0%E6%84%9F%E5%99%A8%EF%BC%8C%E6%8B%9F%E4%BA%BA%E5%8C%96%E4%B8%8E%E6%99%BA%E8%83%BD%E5%8C%96.pdf) — used for ticker-set construction (sensor-by-sensor supplier maps for Chinese humanoid programs).
- [六维力和力矩传感器行业报告：类人力控核心组件 (2024-03)](https://www.jtcopper.com/wp-content/uploads/2024/03/%E5%85%AD%E7%BB%B4%E5%8A%9B%E5%92%8C%E5%8A%9B%E7%9F%A9%E4%BC%A0%E6%84%9F%E5%99%A8%E8%A1%8C%E4%B8%9A%E6%8A%A5%E5%91%8A%EF%BC%9A%E7%B1%BB%E4%BA%BA%E5%8A%9B%E6%8E%A7%E6%A0%B8%E5%BF%83%E7%BB%84%E4%BB%B6%EF%BC%8C%E4%BA%A7%E4%B8%9A%E6%8E%A8%E8%BF%9B%E9%99%8D%E6%9C%AC%E6%8F%90%E8%B4%A8.pdf) — used for 6-D force sensor market sizing and supplier comparison.
- [CMRA humanoid robot tactile sensor company overview (~20 companies)](https://cnmra.com/a-global-overview-of-nearly-20-humanoid-robot-tactile-sensor-companies/) — used for tactile/e-skin landscape.
- [Tesla Optimus & humanoid supply chain analysis (36Kr EN)](https://eu.36kr.com/en/p/3510288514980998) — used for Optimus supplier callouts.

**Macro backdrop (as of 2026-05-25 latest, from `db/indicators.db`)**
- VIX: 16.68 (low-vol regime).
- 10Y Treasury (TNX): 4.59% (2026-05-22).
- HYG (high-yield credit ETF proxy): 79.91 (2026-05-22).
- DXY: 98.99 (2026-05-25, USD soft) — supports non-US basket components on translation.

**Cross-coverage (existing in-house company research read as structured input, not cited inline)**
- [reports/company/Anpeilong/](../company/Anpeilong/Anpeilong_Research_Document.md) (Anpeilong)
- [reports/company/Sanhua_SZSE002050/](../company/Sanhua_SZSE002050/Sanhua_SZSE002050_Research_Document.md) (Sanhua)
- [reports/company/Hesai_NASDAQ_HSAI/](../company/Hesai_NASDAQ_HSAI/Hesai_NASDAQ_HSAI_Research_Document.md) (Hesai)
- [reports/company/HorizonRobotics_HKEX9660/](../company/HorizonRobotics_HKEX9660/HorizonRobotics_HKEX9660_Research_Document.md) (Horizon Robotics)
- [reports/company/Inovance_SZSE300124/](../company/Inovance_SZSE300124/Inovance_SZSE300124_Research_Document.md) (Inovance)
- [reports/company/Estun_SZSE002747/](../company/Estun_SZSE002747/Estun_SZSE002747_Research_Document.md) (Estun)
- [reports/company/Joyson_SSE600699/](../company/Joyson_SSE600699/Joyson_SSE600699_Research_Document.md) (Joyson)
- [reports/company/Leadshine_SZSE002979/](../company/Leadshine_SZSE002979/Leadshine_SZSE002979_Research_Document.md) (Leadshine)

**Stale notices / coverage gaps**
- No in-house company-research yet for Keli Sensing (SSE:603662), Donghua Testing (SZSE:300354), Hanwei Technology (SZSE:300007), Lingyun Industrial (SSE:600480) — these are the four A-share names where the next deep dive would tighten the basket the most.
- Market-cap field returned `None` from yfinance for all tickers in this batch; values would need to be supplemented from `market_cap_cache.db` or per-issuer IR pages for any weighted-basket calculation (next refresh).
- Murata and TDK humanoid revenue is not separately disclosed; their inclusion rests on platform-level (SCH16T-K20, RoboKit1) positioning rather than booked revenue, and is a watch-item for over-extension.

## References

(Every URL inline-cited above, consolidated for quick scanning.)

- [东方证券 人形机器人系列报告, 2024-01](https://zhongzhihui.oss-cn-beijing.aliyuncs.com/industryPdf/20240121-%E4%B8%9C%E6%96%B9%E8%AF%81%E5%88%B8-%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%B3%BB%E5%88%97%E6%8A%A5%E5%91%8A%EF%BC%9A%E7%81%B5%E5%B7%A7%E6%89%8B%E4%B8%8E%E4%BC%A0%E6%84%9F%E5%99%A8%EF%BC%8C%E6%8B%9F%E4%BA%BA%E5%8C%96%E4%B8%8E%E6%99%BA%E8%83%BD%E5%8C%96.pdf)
- [证券时报 (Keli industry note), 2025](https://stcn.com/article/detail/3169048.html)
- [EET-China (Keli sensor-forest strategy), 2025](https://www.eet-china.com/mp/a456494.html)
- [新浪财经 (Keli arms race), 2025-11-24](https://finance.sina.com.cn/stock/t/2025-11-24/doc-infyphky3800607.shtml)
- [股票复盘网 (Donghua + Hanwei + concept stocks)](https://www.fupanwang.com/kplart_info/8449.html)
- [新浪科技 (Hanwei tactile sensors), 2026-03-03](https://finance.sina.com.cn/tech/roll/2026-03-03/doc-inhpsxzq4696210.shtml)
- [汉威 2025 世界机器人大会 release](https://hanwei.cn/news_detail/126.html)
- [Tesla 10-Q FY26 Q1 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)
- [Ambarella FY26 annual report (SEC ARS)](https://www.sec.gov/Archives/edgar/data/0001280263/000119312526227208/d69210dars.pdf)
- [Ambarella FY26 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001280263/000119312526076823/d108529dex991.htm)
- [VPG Q1 FY26 call summary (TradingView/MarketBeat)](https://www.tradingview.com/news/marketbeat:bd9ce5d58094b:0-vishay-precision-group-q1-earnings-call-highlights/)
- [Murata SCH16T-K20 launch (ipXchange CES 2026)](https://ipxchange.tech/product-news/sch16tk20-imu/)
- [Murata humanoid IMU video](https://video.murata.com/en-eu/detail/video/6386632457112)
- [TDK RoboKit1 press release](https://www.tdk.com/en/news_center/press/20220106_01.html)
- [TDK InvenSense Renesas collaboration](https://invensense.tdk.com/news-media/tdk-to-showcase-ultra-low-power-sensing-and-processing-solution-powered-by-renesas-for-next-generation-iot-industrial-and-portable-applications/)
- [Cognex In-Sight vision sensors](https://www.cognex.com/products/machine-vision/vision-sensors)
- [TE Connectivity cobot sensors page](https://www.te.com/en/industries/industrial-machinery/applications/robotics/sensors-for-cobots-and-robotics.html)
- [Novanta profile (Seeking Alpha)](https://seekingalpha.com/symbol/NOVT)
- [Lingyun investor Q&A (陆家嘴金融网)](https://www.ljzfin.com/news/info/77426.html)
- [Lingyun 三共振 analysis (东方财富), 2026-04-16](https://caifuhao.eastmoney.com/news/20260416174312468291900)
- [Lingyun SSE 2026-01 announcement (industrial-robot fund LP)](https://stockmc.xueqiu.com/202601/600480_20260129_2KJA.pdf)
- [Joyson humanoid commercialisation note (新浪财经), 2026-02-23](https://finance.sina.com.cn/roll/2026-02-23/doc-inhnvcpn6795834.shtml)
- [Tesla / Sanhua $685M Optimus order (36Kr EN), 2025](https://eu.36kr.com/en/p/3510288514980998)
- [AVIC Electric Measurement → Chengfei rename (证券时报), 2025-01](https://stcn.com/article/detail/1528221.html)
- [SZSE 300114 → 302132 listing-change announcement](https://disc.static.szse.cn/disc/disk03/finalpage/2025-01-17/e088d543-d639-4cee-b4f7-71200448469f.PDF)
- [CMRA humanoid tactile sensor company overview (~20 companies)](https://cnmra.com/a-global-overview-of-nearly-20-humanoid-robot-tactile-sensor-companies/)
- [六维力和力矩传感器行业报告, 2024-03](https://www.jtcopper.com/wp-content/uploads/2024/03/%E5%85%AD%E7%BB%B4%E5%8A%9B%E5%92%8C%E5%8A%9B%E7%9F%A9%E4%BC%A0%E6%84%9F%E5%99%A8%E8%A1%8C%E4%B8%9A%E6%8A%A5%E5%91%8A%EF%BC%9A%E7%B1%BB%E4%BA%BA%E5%8A%9B%E6%8E%A7%E6%A0%B8%E5%BF%83%E7%BB%84%E4%BB%B6%EF%BC%8C%E4%BA%A7%E4%B8%9A%E6%8E%A8%E8%BF%9B%E9%99%8D%E6%9C%AC%E6%8F%90%E8%B4%A8.pdf)

## History

- 2026-05-31 — theme created with 20-ticker basket (5 core, 8 enabler, 7 adjacent) following user request "Build a theme on humanoid robotics sensors"; initial Performance / Recent events / Drift signals populated. AVIC Electric Measurement excluded after post-merger drift to defense-aircraft holding (300114 → 302132 recode 2025-02-17).
