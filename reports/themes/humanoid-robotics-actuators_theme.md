# Humanoid Robotics Actuators / 人形机器人执行器

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en

## Thesis

This basket owns the joint-actuator side of the humanoid BOM — every torque-producing, force-amplifying, motion-translating part of the robot below the perception stack. It is the natural pair to [`humanoid-robotics-sensors`](humanoid-robotics-sensors_theme.md), which tracks the perception layer. A humanoid robot uses roughly 14–40 rotary reducers, 6–14 planetary roller screws, 28–40 joint modules and dozens of hollow-cup / frameless / BLDC motors per unit; Tesla's Optimus Gen-3 design is disclosed to require 14 harmonic + 12 planetary reducers plus dual finger drives in each 24-DoF dexterous hand ([人形机器人减速器全解析, 2025](https://www.sina.cn/news/detail/5294801543235159.html); [Tesla Optimus V3 hand production-ready, 2026-02-17](https://www.basenor.com/blogs/news/tesla-optimus-v3-production-starts-this-summer-full-timeline)). The actuator BOM dollar value is several times the sensor BOM and lives in fewer hands — the basket concentrates around the scarce-supply names in three categories: ball-screw / planetary-roller-screw makers, harmonic / cycloidal (RV) reducer makers, and integrated joint-module / servo-motor specialists.

The defining demand signal is Tesla Optimus Gen-3, where Fremont mass-production conversion started 2026-01-21 with year-end 50k–100k unit target and a long-run 1 mn-unit Fremont design capacity; Giga Texas adds another 10-million-unit target for 2027 ([Tesla Optimus production timeline](https://optimusk.blog/blog/tesla-optimus-production-timeline/)). Add the Chinese cohort (Unitree, Zhipu / 智元, Xpeng, Galaxy General, UBTECH, Agibot, DeepRobotics) with 200,000+ aggregate 2026 production targets disclosed across investor days. The bet is that A-share and Japanese pure-plays in lead-screw, harmonic-drive and joint-module manufacturing are the bottleneck the volume ramp runs through — and a handful of these names will book real humanoid revenue in 2026, separating from the broader concept-stock pack.

The vulnerability is the same as the sensors basket — Optimus Gen-3 timelines have slid more than once, and a 12-month-window air pocket is the most likely way this basket disappoints. Drift watch: separate the names whose humanoid revenue is *already in the printed quarter* (Tuopu RMB 13.59 mn FY2025 actuator revenue, Sanhua $685M Tesla actuator order) from those still in sample-stage (Beitebao, Wuzhou Xinchun, most Chinese harmonic-drive names). The Japanese leaders (Harmonic Drive Systems, Nabtesco) are the cleanest "humanoid TAM call" — they already supply 14 harmonic + RV reducers per Tesla Optimus body via Tier-1 integrators — but their multiples now embed an outcome the printed P&Ls do not yet show.

## Scope rules

**In:** rotor + stator + ball-screw + roller-screw + planetary-roller-screw makers; harmonic-drive and cycloidal-drive (RV) reducer makers; servo-motor, hollow-cup and frameless-motor specialists; humanoid joint-module integrators; BLDC motor-drive-IC houses whose chips ship into humanoid joint actuators; companies named in Tesla Optimus / Figure / Unitree / Xpeng / Zhipu / Galaxy General / UBTECH actuator supply chains. Both pure-play designers and diversified Tier-1s qualify if there is a *named, dated* humanoid customer or design-win in the public record.

**Out:** pure-play sensor names (already in [`humanoid-robotics-sensors`](humanoid-robotics-sensors_theme.md)); industrial-robot OEMs unless they are dominantly humanoid-exposed (Estun, Inovance, and Leadshine therefore belong in the sensors basket as adjacents, not here); auto T1s without humanoid actuator disclosure; thermal-management or connector houses one layer removed from the actuator socket (银轮股份 002126, 鸿日达 301285); private companies (surfaced in Watch List, not basket); diversified-conglomerate names with humanoid optionality but no disclosed actuator SKU (德昌电机 0179.HK, flagged for the bear case below). When a ticker appears in both baskets (Sanhua 002050, and historically Estun / Inovance / Leadshine, though those latter three sit in sensors as adjacents) the Justification cell flags the dual exposure — but each basket carries its own ticker rationale.

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| SSE:603009 | Beitebao 北特科技 | core | A-share planetary-roller-screw pure-play; Tesla Tier-2 supplier; RMB 1.85 bn Kunshan PRS R&D + production base (signed 2024-10-14, topped out 2025-11, formal production 2026, 2.6 mn PRS sets p.a. design capacity) ([21财经, 2024-10-15](https://m.21jingji.com/article/20241016/992611936967b7c1177fc2167efd6798.html); [上交所 募集说明书](https://static.sse.com.cn/stock/disclosure/announcement/c/202512/603009_20251205_7ZC1.pdf); [和讯网, 2025-12-04](https://stock.hexun.com/2025-12-04/222627420.html)). | 2026-05-31 |
| SSE:603667 | Wuzhou Xinchun 五洲新春 | core | Bearing-and-screw chain player retooling for humanoid; June 2025 RMB 1.0 bn private placement plan to fund 70k-humanoid-unit capacity — 980k PRS sets / 2.1 mn micro ball-screws / 70k humanoid-bearings p.a. at Xinchang Zhejiang; shipments via Tier-1 to "globally-known humanoid OEMs" ([21经济网, 2025-06-17](https://www.21jingji.com/article/20250617/herald/05cf32584a26e6fdfc4a7e696cbf7333.html); [东吴证券深度](https://pdf.dfcfw.com/pdf/H3_AP202503041644047989_1.PDF)). | 2026-05-31 |
| SSE:688017 | Leaderdrive 绿的谐波 | core | Largest-domestic harmonic-reducer pure-play (~25% China share); 9M-2025 revenue +47% YoY, with humanoid pilots Unitree / UBTECH / Fourier and Tier-1 routes into Tesla Optimus disclosed in 2024–2025 investor-day language; 178× TTM P/E on the re-rating. In-house coverage at [Leaderdrive](../company/Leaderdrive_SSE688017/Leaderdrive_SSE688017_Research_Document.md) ([2024 年报](http://static.cninfo.com.cn/finalpage/2025-04-29/1223107562.PDF); [2025 三季报](http://static.cninfo.com.cn/finalpage/2025-10-30/1224173896.PDF)). | 2026-05-31 |
| SZSE:002896 | Zhongdadi 中大力德 | core | Only domestic enterprise simultaneously mass-producing planetary, harmonic *and* RV reducers; 2025 Zhipu / 智元 Yuanwang A2 win for 50k planetary reducer orders (50% of program); main UBTECH supplier (63% reducer allocation); *only* domestic supplier to pass Tesla Optimus four-round verification, harmonic-reducer mass-production prep in H2 2025; 2025 robot revenue share expected >15% ([九方智投深度](https://www.9fzt.com/detail/sz_002896_10_794787750990.html); [新浪财经, 2025-12-25](https://finance.sina.com.cn/roll/2025-12-25/doc-inhczhsf8870193.shtml)). | 2026-05-31 |
| SZSE:002472 | Shuanghuan 双环传动 | core | Subsidiary 环动科技 is China #1 RV reducer (~45% domestic, ~18% global share); pre-IPO carve-out filed Oct 2025; humanoid customers Estun / EFORT / Kenuop / Siasun + Tesla Optimus pipeline via Tuopu joint-module co-development ([新浪财经 环动科技招股书, 2025-10-06](https://finance.sina.com.cn/roll/2025-10-06/doc-infsyftk5550847.shtml); [开源证券 国产减速器](https://m.zhitongcaijing.com/contentnew/appcontentdetail.html?content_id=764917)). | 2026-05-31 |
| TSE:6324 | Harmonic Drive Systems | core | Global #1 harmonic-reducer house — every Tesla Optimus body carries 14 harmonic units, with Figure / Boston Dynamics Atlas using HDS-licensed designs. FY2026 (Mar) revenue ¥59.6 bn (+7% YoY); humanoid inquiries from Figure / Tesla noted in management commentary; medium-term plan targets ¥90 bn / ¥15 bn OP by FY2027 ([Quartr Q4 2026](https://quartr.com/companies/harmonic-drive-systems-inc_15793); [Note Vol.3 analysis, 2026](https://note.com/aikabu_analysis/n/n90955489852e?hl=en-US)). | 2026-05-31 |
| TSE:6268 | Nabtesco | core | Global #1 RV-reducer house (~35% of articulated-robot RVs globally) — the geometry humanoid OEMs are buying for hip / shoulder joints. Announced 2× RV-reducer capacity expansion targeting 2026; FY2026 guidance ¥327 bn revenue (+6.2%); RVmini and Monocrank launches December 2025 explicitly sized for humanoid wrist / finger-base joints ([Nabtesco RVmini Monocrank, 2025-12-02](https://www.nabtesco.com/en/news/20251202-17329/); [Morningstar mid-term outlook](https://www.morningstar.com/company-reports/1250118-nabtesco-to-benefit-from-solid-midterm-outlook-for-precision-reduction-gears)). | 2026-05-31 |
| SSE:603728 | Mingzhi 鸣志电器 | enabler | Hollow-cup motor specialist; passed Tesla C-round certification with Optimus volume production expected from Q1 2026; humanoid customers 3+ in China and 3+ in US; pricing advantage RMB 1,200–2,300/unit vs Swiss Maxon ~RMB 4,000 ([21经济网 灵巧手风起, 2025-09-05](https://www.21jingji.com/article/20250905/herald/63d173a45e39ee6294130a5745298b75.html); [和讯网, 2025-02-27](https://stock.hexun.com/2025-02-27/217589133.html)). | 2026-05-31 |
| SZSE:300660 | Jiangsu Leili 江苏雷利 | enabler | Micro-motor leader (FY2024 revenue RMB 3.52 bn, +14% YoY); humanoid platform spans hollow-cup motors (6mm dia, 100k RPM), linear transmission, frameless torque motors + rope-driven 22-DoF dexterous hands; Anhui Zhongke Lingxi JV (2024-09); RMB 1.286 bn convertible-bond raise approved 2025 ([新浪财经, 2024-11-28](https://finance.sina.com.cn/stock/bxjj/2024-11-28/doc-incxqzhu9730153.shtml); [stcn, 2025](http://stcn.com/article/detail/2241690.html)). | 2026-05-31 |
| SSE:688160 | Buke 步科股份 | enabler | Cleanest disclosed humanoid-joint-motor shipment volume in the basket: 9M-2025 frameless-torque-motor shipments 43,000 units (+187% YoY) and servo-module shipments 62,000 (+128%); already supplies leading domestic humanoid customers in batch order; Changzhou phase-1 ramping to 1 mn motors p.a. by 2026, phase-2 to 1.81 mn p.a. ([腾讯新闻, 2025-05-12](https://news.qq.com/rain/a/20250512A0789Z00); [步科 2025-Q3 业绩说明会](https://file.finance.qq.com/finance/hs/pdf/2025/09/05/0541f3368a3611f0af55fa163e39923a.pdf)). | 2026-05-31 |
| NASDAQ:ALNT | Allient | enabler | US BLDC / brushless servo / coreless motor maker with explicit humanoid product page and April 2026 whitepaper *A Selection Guide to Motors for Humanoid Robotics Systems*; May 2026 humanoid-joints webinar. No disclosed OEM customer name but the positioning and conference cadence make it the cleanest US-listed pure-play motion-control name with humanoid ambition ([Allient humanoid motors](https://allient.com/humanoid-robot-motors-and-motion-solutions/); [RoboticsTomorrow whitepaper, 2026-04-23](https://www.roboticstomorrow.com/news/2026/04/23/allient-inc-publishes-new-whitepaper-on-motor-selection-for-humanoid-robotics-systems/26473)). | 2026-05-31 |
| NYSE:MOG-A | Moog | enabler | Precision motion-control franchise — servovalves, actuators, control systems; explicit Mobile Robotics commercial vertical with ruggedized motion products; record Q1 FY2026 and strong Q2 FY2026 with mobile-robotics demand cited as an upside vector. Humanoid revenue not separately disclosed; inclusion rests on platform exposure + aerospace-grade-servovalve fit for humanoid hydraulic / pneumatic joints ([8-K Q1 FY26](https://www.sec.gov/Archives/edgar/data/0000067887/000162828026004305/ex991-13026.htm); [8-K Q2 FY26](https://www.sec.gov/Archives/edgar/data/0000067887/000162828026027030/ex991-42426.htm); [Robotics page](https://www.moog.com/innovation/Robotics.html)). | 2026-05-31 |
| TSE:6506 | Yaskawa | enabler | World #3 industrial-robotics OEM + top-tier servo-motor franchise — Sigma-X servo-drive series (2025) is the production motor every humanoid OEM evaluates against domestic Chinese alternatives; MOTOMAN NEXT on NVIDIA Jetson + Isaac; 2025-12-01 SoftBank MOU on physical-AI robots for office / hospital / school environments ([Sigma-X servo](https://www.yaskawa.com/products/motion/sigma-x-servo-products); [MOTOMAN NEXT on Jetson, Robot Report](https://www.therobotreport.com/yaskawa-new-motoman-next-runs-on-wind-river-linux/); [SoftBank MOU](https://www.yaskawa-global.com/newsrelease/news/178574)). | 2026-05-31 |
| SSE:688279 | FortiorTech 峰岹科技 | enabler | China #1 fabless BLDC motor-drive IC house (6th globally 2023, only Chinese top-10 entrant); Jan 2025 strategic cooperation with Sanhua Holding for humanoid hollow-cup-motor JV; FU75XX RISC-V dual-core MCU targets dexterous-hand + joint-actuator sockets; 1Q26 revenue +46% YoY. In-house coverage at [FortiorTech](../company/FortiorTech_SSE688279/FortiorTech_SSE688279_Research_Document.md) ([2025年报](https://static.cninfo.com.cn/finalpage/2026-03-27/); [峰岹×三花框架](https://m.21jingji.com/timeline/58991b67a7f9458572ae9ae7f44e6189.html)). | 2026-05-31 |
| SZSE:002050 | Sanhua 三花智控 | adjacent | Tesla Optimus rotary-joint *exclusive* supplier and linear-actuator total-assembly supplier; received the $685M Tesla order (2025-10-15) for ~43k robots' worth of linear actuators (RMB ~28k Sanhua content / Optimus body); Mexico plant 1 mn-actuator p.a. capacity targeted for 2026 Tesla ramp; FortiorTech JV for hollow-cup motors. **Dual-listed in [`humanoid-robotics-sensors`](humanoid-robotics-sensors_theme.md)** — actuator modules integrate IMU + position-sensing, flagged here as basket's largest disclosed Optimus exposure. In-house coverage at [Sanhua](../company/Sanhua_SZSE002050/Sanhua_SZSE002050_Research_Document.md) ([36Kr EN, 2025-10-15](https://eu.36kr.com/en/p/3510288514980998); [财富号, 2026-01](https://caifuhao.eastmoney.com/news/20260101071344517537190)). | 2026-05-31 |
| SSE:601689 | Tuopu 拓普集团 | adjacent | T2-One Tesla Optimus supplier (linear-actuator yields 99.2%); robot-actuator BU spun out as stand-alone segment; FY2025 disclosed humanoid actuator revenue RMB 13.59 mn — first A-share to print a numeric robot revenue line; 2026 Mexico plant launch primarily for Tesla. In-house coverage at [Tuopu](../company/Tuopu_SSE601689/Tuopu_SSE601689_Research_Document.md) ([2025 年报, 第35页](http://static.cninfo.com.cn/finalpage/2026-03-23/1224398501.PDF); [Futubull Optimus Gen-3](https://news.futunn.com/en/post/61458095/top-group-601689-tesla-optimus-gen3-humanoid-robot-accelerates-ai)). | 2026-05-31 |
| SZSE:300100 | Shuanglin 双林股份 | adjacent | March 2025 launched China's first reverse-type planetary roller screw aimed at humanoid linear actuators; samples to Tesla + Chinese humanoid OEMs but *no formal SOP design-win yet*; 2025-01 acquired 无锡科之鑫 (thread-grinder maker) to collapse the roller-screw process bottleneck. In-house coverage at [Shuanglin](../company/双林股份_SZSE300100/双林股份_SZSE300100_Research_Document.md) ([2025 年报](http://www.cninfo.com.cn/new/disclosure/stock?stockCode=300100); [艾邦机器人](https://www.aibangbots.com/a/1363)). | 2026-05-31 |
| HKEX:1021 | Hua Yan Robotics 华沿机器人 | adjacent | China's largest cobot exporter by overseas revenue + the only leading Chinese cobot maker selling **core motion components externally** (joint modules with proprietary motors at +30% torque density per unit volume vs incumbents); IPO 2026-03-30 at HKD 17, raised HKD 1.48 bn, HKD 128 mn earmarked for humanoid core-motion-components. Cornerstones: Hillhouse, GF Fund, Morgan Stanley ([新浪财经, 2026-03-30](https://finance.sina.com.cn/wm/2026-03-30/doc-inhsueeu4004952.shtml); [Huayan IR](https://www.huayan-robotics.com/about-us/news/2560.html)). | 2026-05-31 |

**Geographic / role mix (18 tickers):** China A-share 12 (67%) · Japan 3 (17%) · United States 2 (11%) · Hong Kong 1 (6%). Role: core 7 (39%), enabler 7 (39%), adjacent 4 (22%).

## Exclusions

| Ticker | Reason for exclusion |
|---|---|
| BSE:873593 | 鼎智科技 (Dingzhi Technology) — micro-motor + roller-screw maker on **Beijing Stock Exchange**, not yfinance-trackable. The seed mistakenly used SZSE:301215, which is actually 中汽股份 / CATARC (auto-test-track operator). Re-evaluate if BSE tickers become available in yfinance ([东方财富](https://emcreative.eastmoney.com/app_fortune/article/index.html?artCode=20251230181758656820640&postId=1646639639); [深交所 中汽股份](https://emweb.eastmoney.com/f10_v2/OperationsRequired.aspx?code=SZ301215)). |
| HKEX:0179 | 德昌电机 (Johnson Electric) — JPMorgan flagged "humanoid 进展缓慢" in 2026-Q1. Official humanoid-joint product exists (15 Nm/kg torque density, 0.1 arcmin backlash, Dongjie JV with 上海机电 at 2025 WAIC) but no disclosed customer name, no quantified humanoid revenue, and CCM-motor AI-infrastructure demand now dominates the equity story. Re-evaluate when a named Optimus / Figure / Unitree win is disclosed ([Johnson Electric humanoid](https://www.johnsonelectric.cn/solutions/humanoid-robot); [Dongjie JV, 2025-08](https://www.johnsonelectric.cn/news/jointelligence-officially-unveiled-in-shanghai)). |
| SZSE:301285 | 鸿日达 (Hongrida) — connector maker, not an actuator / motor / reducer name. Up 310% 1Y as a humanoid-concept bid but the BOM exposure is in 3C / NEV precision structural components, not joint actuators ([东方财富 经营分析](https://emweb.eastmoney.com/PC_HSF10/BusinessAnalysis/Index?type=web&code=SZ301285); [国盛证券 2024 深度](https://pdf.dfcfw.com/pdf/H3_AP202410241640450937_1.pdf)). |
| SZSE:002126 | 银轮股份 (Yinlun) — thermal-management specialist with humanoid "1+4+N" roadmap (thermal + rotary-joint + actuator + dexterous-hand modules). Actuator-module is real R&D but the equity is fundamentally a vehicle-thermal-management name; humanoid exposure one layer removed from the joint socket ([九方智投](https://www.9fzt.com/detail/sz_002126_3_800184707392.html); [stcn IR 2025-Q3](https://file.finance.qq.com/finance/hs/pdf/2025/08/27/1224590583.PDF)). |
| SSE:603915 | 国茂股份 (Guomao) — China #1 general-purpose reducer with humanoid harmonic-reducer R&D, 艾克斯智节 joint-module JV, and DeepRobotics exclusive supply. Held off because humanoid contribution is <0.1% of FY25 net income and the in-house [Guomao research](../company/国茂股份_SSE603915/国茂股份_SSE603915_Research_Document.md) flags 45× TTM P/E as already pricing the optionality. Re-evaluate when a humanoid customer name + dollar revenue prints. |
| Private | Bota Systems, Robotiq, Flexiv, Figure AI, Agility Robotics, Unitree, Boston Dynamics, Galbot, Agibot, Zhipu, Galaxy General — not investable; humanoid OEMs drive demand for the actuator BOM but aren't suppliers themselves; Flexiv is a hybrid (own-joint + own-OEM). Any IPO is an immediate basket-mutation candidate. |

## Keywords

humanoid robotics / 人形机器人 · planetary roller screw / 行星滚柱丝杠 · ball screw / 滚珠丝杠 · harmonic reducer / 谐波减速器 · cycloidal RV reducer / RV减速器 · hollow-cup motor / 空心杯电机 · frameless torque motor / 无框力矩电机 · BLDC motor driver / BLDC 电机驱动芯片 · joint module / 关节模组 · linear actuator / 直线执行器 · dexterous hand / 灵巧手 · Tesla Optimus · embodied AI / 具身智能

## Performance (as of 2026-05-31, since-inception snapshot)

Returns are simple price returns from yfinance with `auto_adjust=True`, computed against the 2026-05-29 close (last trading day before 2026-05-31 anchor). The basket is multi-market; benchmarks are reported separately by geography rather than blended. 华沿机器人 (1021.HK) IPO'd 2026-03-30 and is excluded from the 1Y / YTD aggregate calculations because the window is shorter than the inclusion window — its since-IPO return is reported separately.

**Equal-weight basket returns (17 tickers, ex-1021.HK):** 3-month +4.3% · YTD 2026 +11.5% · trailing 1-year +61.7%.

**Median 1-year return:** +30.2% (well below the mean — the basket's 1Y aggregate is pulled up by Allient, Leaderdrive, Nabtesco, Harmonic Drive Systems, Yaskawa, and Moog — see dispersion read below).

**Benchmark returns over the same windows:**

| Benchmark | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| S&P 500 (SPY) | +10.5% | +11.0% | +29.8% |
| CSI 300 (510300.SS) | +4.0% | +4.3% | +30.2% |
| Hang Seng (2800.HK) | −5.2% | −3.6% | +9.5% |
| TOPIX (1305.T NEXT FUNDS ETF) | +3.9% | +14.9% | +43.8% |

**Per-ticker performance, sorted by 1-year return:**

| Ticker | Name | Role | 1Y | YTD | 3M | Close (local) |
|---|---|---|---|---|---|---|
| NASDAQ:ALNT | Allient | enabler | +161.0% | +42.6% | +21.5% | 79.16 |
| SSE:688017 | Leaderdrive 绿的谐波 | core | +159.5% | +60.2% | +29.1% | 306.00 |
| TSE:6268 | Nabtesco | core | +136.1% | +44.5% | +13.7% | 5,533 |
| TSE:6324 | Harmonic Drive Systems | core | +126.5% | +103.6% | +71.1% | 7,800 |
| TSE:6506 | Yaskawa | enabler | +111.7% | +46.1% | +34.3% | 7,208 |
| NYSE:MOG-A | Moog | enabler | +95.2% | +44.3% | +4.4% | 359.97 |
| SSE:603667 | Wuzhou Xinchun 五洲新春 | core | +80.6% | −3.3% | −10.6% | 71.76 |
| SZSE:002050 | Sanhua 三花智控 | adjacent | +74.8% | −17.5% | −10.8% | 46.34 |
| SZSE:002896 | Zhongdadi 中大力德 | core | +30.2% | −14.3% | −9.4% | 75.82 |
| SSE:688160 | Buke 步科股份 | enabler | +28.6% | −24.3% | −10.8% | 110.93 |
| SSE:601689 | Tuopu 拓普集团 | adjacent | +25.5% | −18.4% | −9.3% | 62.40 |
| SZSE:002472 | Shuanghuan 双环传动 | core | +21.7% | −16.5% | −6.0% | 39.23 |
| SZSE:300660 | Jiangsu Leili 江苏雷利 | enabler | +13.3% | −21.7% | −18.8% | 42.49 |
| SSE:688279 | FortiorTech 峰岹科技 | enabler | +8.5% | +8.2% | +11.2% | 216.94 |
| SSE:603728 | Mingzhi 鸣志电器 | enabler | +7.3% | −14.4% | −11.5% | 61.32 |
| SSE:603009 | Beitebao 北特科技 | core | −1.5% | −1.2% | −9.4% | 48.26 |
| SZSE:300100 | Shuanglin 双林股份 | adjacent | −30.3% | −22.1% | −15.9% | 30.51 |
| HKEX:1021 | Hua Yan Robotics 华沿机器人 | adjacent | n/a (since IPO 2026-03-30) | +6.0% | +6.0% | 19.51 |

**Read of the dispersion:** The 1Y window is dominated by **non-China leaders** — Allient (+161%), Nabtesco (+136%), Harmonic Drive Systems (+127%), Yaskawa (+112%), Moog (+95%) — plus Leaderdrive (+160%), the only A-share name that participated. The Chinese pack split sharply: Wuzhou Xinchun (+81%) and Zhongdadi (+30%) were rewarded for production-capacity announcements but **derated YTD** as the broader concept basket gave back CES 2026 gains, while Beitebao (−2%) and Shuanglin (−30%) underperformed despite legitimate wins because neither has booked humanoid revenue. The basket sits in roughly two halves: a "platform leverage already in the print" group (HDS, Nabtesco, Yaskawa, ALNT, MOG, Leaderdrive) that has rebased and is consolidating, and a "sample-stage / capacity-buildout" group (Beitebao, Wuzhou Xinchun, Shuanghuan, Buke, Tuopu, Sanhua, Shuanglin) that has corrected hard YTD pending real revenue prints. At the median, 1Y returns are in line with CSI 300 and below SPY / TOPIX.

## Recent events (since basket inception)

This is the inception write; "recent events" covers the prior ~90 days that informed ticker selection. Future refreshes will cover the window since the previous `Last refreshed` date.

- **Tesla Optimus Gen-3 hand production-ready (2026-02-17) / Fremont mass-production conversion (2026-01-21):** Year-end 50k–100k unit target, long-run 1 mn-unit Fremont design capacity — the largest demand driver for every ticker ([Tesera timeline](https://www.tesery.com/blogs/news/elon-musk-reveals-aggressive-production-timeline-for-tesla-optimus-3); [Basenor full timeline](https://www.basenor.com/blogs/news/tesla-optimus-v3-production-starts-this-summer-full-timeline)).
- **Hua Yan Robotics IPO (HKEX:1021) priced HKD 17, listed 2026-03-30:** 5,063× oversubscribed; raised HKD 1.48 bn net, ~HKD 128 mn earmarked for humanoid core-motion-components; cornerstones include Hillhouse, GF Fund, Morgan Stanley ([新浪财经, 2026-03-30](https://finance.sina.com.cn/wm/2026-03-30/doc-inhsueeu4004952.shtml)).
- **Beitebao 北特科技 Kunshan PRS base topped out (2025-11-24):** Formal production targeted Q1 2026; 2.6 mn PRS sets annual design capacity ([和讯网, 2025-12-04](https://stock.hexun.com/2025-12-04/222627420.html); [上交所 募集说明书](https://static.sse.com.cn/stock/disclosure/announcement/c/202512/603009_20251205_7ZC1.pdf)).
- **Nabtesco RVmini / Monocrank launch (2025-12-02):** Compact precision reduction gears explicitly sized for smaller humanoid joints — addresses the gap between standard articulated-robot RVs and humanoid wrist / finger-base sockets ([Nabtesco release](https://www.nabtesco.com/en/news/20251202-17329/)).
- **Tesla / Sanhua $685M Optimus order (2025-10-15):** Linear-actuator total-assembly order for ~43,000 robots at ~RMB 28k Sanhua content / Optimus body; Mexico plant 1 mn-units/yr ramping ([36Kr EN](https://eu.36kr.com/en/p/3510288514980998)).
- **Shuanghuan 002472 carve-out IPO of 环动科技 filed (2025-10-06):** Standalone RV-reducer pure-play prospectus filed — the implicit asset the market has been pricing into the parent multiple ([新浪财经](https://finance.sina.com.cn/roll/2025-10-06/doc-infsyftk5550847.shtml)).
- **Zhongdadi Zhipu Yuanwang A2 50k-unit reducer order (2025):** ~50% of Zhipu's reducer demand at program scale; UBTECH allocation ~63% reducer share also disclosed ([九方智投](https://www.9fzt.com/detail/sz_002896_10_794787750990.html)).
- **Yaskawa x SoftBank physical-AI MOU (2025-12-01):** MOTOMAN NEXT on NVIDIA Jetson + Wind River Linux as hardware base for office / hospital / school robots ([Yaskawa release](https://www.yaskawa-global.com/newsrelease/news/178574)).
- **Allient humanoid-robotics whitepaper (2026-04-23):** *A Selection Guide to Motors for Humanoid Robotics Systems* — marketing signal of product roadmap ([RoboticsTomorrow](https://www.roboticstomorrow.com/news/2026/04/23/allient-inc-publishes-new-whitepaper-on-motor-selection-for-humanoid-robotics-systems/26473)).

## Drift signals

This is the inception write — drift detection becomes the value-add starting from the *next* refresh. Initial flags for next month's pass:

- **Chinese-pure-play vs Japanese-incumbent valuation spread is wide and widening.** Japanese names (HDS, Nabtesco, Yaskawa) and Leaderdrive (A-share) re-rated >100% over 1Y on the same humanoid TAM narrative, while comparable Chinese pure-plays (Beitebao, Wuzhou Xinchun, Shuanghuan, Shuanglin) are flat to down 30%. If Tesla's 2026 Optimus production lands ≥75k units the Chinese pack should re-rate to converge; if it lands below 30k the Japanese pack is over-extended and the spread closes from the other end.
- **Shuanghuan 002472 vs Shuanglin 300100 — different companies.** 双环传动 (002472) is the RV-reducer scale leader via 环动科技 (core); 双林股份 (300100) is the reverse-PRS sample-stage name (adjacent). The 环动科技 carve-out IPO (filed Oct 2025) will create a pure-play to track — consider replacing the parent 002472 once it lists.
- **Beitebao −1.5% / Shuanglin −30% 1Y is the largest sample-stage drag.** Both are in capacity-buildout mode with no booked humanoid revenue. Beitebao Kunshan first-product shipment (Q1 2026) and Shuanglin sample-to-design-win conversion are the Q2 FY26 earnings-call items to watch.
- **Watch list (public — flagged but not added at inception):** 兆威机电 (SZSE:003021, dexterous-hand micro-reducer named with Xiaomi / Tesla customers); 震裕科技 (SZSE:300953, motor iron-core + reverse-PRS small-batch with multiple humanoid OEMs); 丰立智能 (SZSE:301368, mini reducers / harmonic for Star Motion Era / Unitree / Sanhua); 恒立液压 (SSE:601100, micro-screw North-American humanoid audit Oct 2025); 鼎智科技 (BSE:873593, micro-motor + roller-screw pure-play but BSE listing). Add at next refresh if any clears the inclusion bar (named humanoid customer + disclosed shipment volume).
- **Watch list (private / pre-IPO):** 环动科技 carve-out (China RV pure-play, listing imminent); 国茂精密 sub-listing (DeepRobotics ecosystem); any Figure / Agility / Unitree IPO would be a major demand-side basket-mutation event.
- **Single-modality risk in the Japanese incumbent bucket.** HDS, Nabtesco and Yaskawa ran +112% to +136% 1Y, but Harmonic Drive's FY2026 net margin collapsed to 2.7% and the ¥90 bn / ¥15 bn OP medium-term plan has not been re-validated. A material miss on humanoid order intake in any of the three's next quarterly would compress the basket faster than any single Chinese pure-play.
- **Optimus-Gen-3 timeline anchors the whole thesis.** Every paragraph above keys off the 2026-H2 mass-production start. If the Tesla Q2 FY26 call slips the date, several `core` and `adjacent` rationales need re-grounding next refresh.

## Catalysts (next 3–6 months)

- **Tesla Q2 FY26 earnings (mid-July 2026):** Optimus Gen-3 production-pull guidance — every basket name keys off this print.
- **Beitebao Kunshan plant first-product shipment (Q1–Q2 2026):** A named Optimus PRS shipment converts the equity from "concept" to "Tesla supplier with revenue line".
- **环动科技 IPO (H2 2026):** Pure-play RV-reducer carve-out of 双环传动 — instrument-creation event that will likely re-rate parent 002472.
- **Harmonic Drive Systems Q1 FY27 (Aug 2026) and Nabtesco Q1–Q2 FY26 (Aug / Nov 2026):** First quarters where Optimus Gen-3 humanoid orders should mechanically start showing up in the order book; HDS ¥90 bn / ¥15 bn OP medium-term plan needs validation, Nabtesco 2× RV-reducer capacity-expansion plan set against humanoid demand.
- **CES 2027 (Jan) / China International Industry Fair (Q3 2026):** Typical venues for new humanoid joint-module reveals — watch for Tuopu / Sanhua / Mingzhi / Leaderdrive product launches.
- **Optimus Gen-3 dedicated supplier qualification disclosures:** A Tesla 8-K Item 1.01 naming an actuator supplier or a Sanhua / Tuopu follow-on order beyond the $685M Q4 2025 print would be the cleanest basket-moving event.

## Data Used / 数据来源清单

**Market data**
- yfinance `auto_adjust=True` for prices, returns, market cap, sector — pulled 2026-05-31 (last trading day 2026-05-29).
- Benchmarks: SPY (S&P 500), 510300.SS (CSI 300 ETF), 2800.HK (Hang Seng ETF), 1305.T (NEXT FUNDS TOPIX ETF — substituted for 1306.T which returned split-adjusted-broken data in yfinance).

**Per-ticker primary sources** — already cited inline in the Tracked tickers and Recent events tables above; in-house company research used as structured input is listed in the Cross-coverage block below. The Per-ticker manifest of unique primary sources used at inception:
- A-share names rely on cninfo annual reports + 业绩说明会 transcripts + 21财经 / 新浪 / stcn / 和讯 / 九方智投 / 财富号 industry notes for humanoid disclosures.
- Japanese names rely on company IR (Nabtesco news room, Yaskawa news room) + Quartr / Morningstar / Note / Dividend Japan secondary analysis.
- US names (Allient, Moog) rely on SEC 8-K filings + product / whitepaper releases (RoboticsTomorrow, company sites).
- HK Hua Yan Robotics relies on listing prospectus + 2026-03 IPO coverage (新浪财经, Cyber Quote, Huayan Robotics IR).

**Industry research (theme-level)**
- [东方证券 人形机器人系列报告：丝杠，核心传动部件，人形机器人开启成长空间, 2023-10](https://zhongzhihui.oss-cn-beijing.aliyuncs.com/industryPdf/20231025-%E4%B8%9C%E6%96%B9%E8%AF%81%E5%88%B8-%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%B3%BB%E5%88%97%E6%8A%A5%E5%91%8A%EF%BC%9A%E4%B8%9D%E6%9D%A0%EF%BC%9A%E6%A0%B8%E5%BF%83%E4%BC%A0%E5%8A%A8%E9%83%A8%E4%BB%B6%EF%BC%8C%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%BC%80%E5%90%AF%E6%88%90%E9%95%BF%E7%A9%BA%E9%97%B4.pdf) — used for lead-screw and roller-screw supplier mapping.
- [华安证券 减速器行业深度：机器人核心部件，国产替代及应用拓宽空间广阔, 2024-01](https://pdf.dfcfw.com/pdf/H3_AP202401101617055729_1.pdf) — used for harmonic / RV / planetary reducer supplier landscape.
- [东吴证券 灵巧之"手"，解锁人形机器人黄金赛道, 2025-04-26](https://pdf.dfcfw.com/pdf/H3_AP202504261662702285_1.pdf) — used for dexterous-hand and micro-motor supplier landscape (industry deep #7).
- [艾邦机器人 国内人形机器人谐波减速器 23 家供应商介绍](https://www.aibangbots.com/a/2094) — used for cross-checking domestic harmonic-reducer competitive set.
- [艾邦机器人 人形机器人推进丝杠国产化 30+ 相关供应商盘点](https://www.aibangbots.com/a/2259) — used for cross-checking domestic lead-screw / PRS competitive set.
- [Tesla Optimus production timeline (Optimusk blog), 2026](https://optimusk.blog/blog/tesla-optimus-production-timeline/) — used for the 2026-H2 mass-production schedule that anchors the basket thesis.
- [Tesla Optimus 3 production timeline (Tesera), 2026](https://www.tesery.com/blogs/news/elon-musk-reveals-aggressive-production-timeline-for-tesla-optimus-3) — used for the 2026 50k–100k unit target.

**zsxq theme-level evidence (referenced via in-process notes, not opened during this run)**
- `415284812112548` — Deutsche "华沿机器人 1021.HK — 协作机器人与人形机器人核心部件龙头, 首予买入评级" (p. 61, deep dive) — informed the 1021.HK inclusion rationale.
- `212485545441811` — 券商研报 "机器人行业深度：丝杠制造壁垒高企，人形机器人催化丝杠市场规模跃升" (p. 25) — anchors the lead-screw scarcity thesis.
- `415284811814428` — 券商研报 "机械行业技术壁垒与发展路径：人形机器人核心零部件" (p. 16) — cross-reference for sub-component selection.
- `212485541451481` — JPM 比亚迪 1211.HK 科技日 — 自研芯片与人形机器人 — informed the Optimus competitive supply-chain context.
- `415284421241248` — JPM 德昌电机 0179.HK — AI 基建加速放量，人形机器人进展缓慢 — primary source for the 0179.HK exclusion rationale in the Exclusions table.
- `415284811821248` + `812485545248282` — MS "人形机器人：新视界 / 人形机器人即将进入你的彭博终端" (both p. 35) — broader industry context for the 2026 production-ramp narrative.

**Macro backdrop (as of 2026-05-25 latest, from `db/indicators.db`)**
- VIX: 16.68 (low-vol regime).
- 10Y Treasury (TNX): 4.558% (2026-05-22).
- HYG (high-yield credit ETF proxy): 79.91 (2026-05-22).
- DXY: 98.99 (2026-05-25, USD soft) — supports non-US basket components on translation.
- 3M T-Bill: 3.585% (2026-05-22).
- 10Y-2Y yield spread: 0.973% (2026-05-22).

**Cross-coverage (existing in-house company research read as structured input, not cited inline)**
- [reports/company/Leaderdrive_SSE688017/](../company/Leaderdrive_SSE688017/Leaderdrive_SSE688017_Research_Document.md) (Leaderdrive)
- [reports/company/Tuopu_SSE601689/](../company/Tuopu_SSE601689/Tuopu_SSE601689_Research_Document.md) (Tuopu)
- [reports/company/Sanhua_SZSE002050/](../company/Sanhua_SZSE002050/Sanhua_SZSE002050_Research_Document.md) (Sanhua) — also in sensors basket
- [reports/company/FortiorTech_SSE688279/](../company/FortiorTech_SSE688279/FortiorTech_SSE688279_Research_Document.md) (FortiorTech)
- [reports/company/双林股份_SZSE300100/](../company/双林股份_SZSE300100/双林股份_SZSE300100_Research_Document.md) (Shuanglin)
- [reports/company/国茂股份_SSE603915/](../company/国茂股份_SSE603915/国茂股份_SSE603915_Research_Document.md) (Guomao — Excluded)

**Stale notices / coverage gaps**
- No in-house company-research yet for Beitebao (SSE:603009), Wuzhou Xinchun (SSE:603667), Zhongdadi (SZSE:002896), Shuanghuan (SZSE:002472), Mingzhi (SSE:603728), Jiangsu Leili (SZSE:300660), Buke (SSE:688160), or the three Japanese names (HDS / Nabtesco / Yaskawa) — these are the eight names where the next deep dive would tighten the basket the most. Beitebao and the Japanese trio are top priority given they carry the largest position in the inception write.
- Hua Yan Robotics (HKEX:1021) IPO'd only 2026-03-30; the 1Y / YTD return windows are not yet directly comparable to the rest of the basket and the company has not yet reported a full quarter as a listed entity. First Q1 2026 print expected ~August 2026.
- Market-cap field returned `None` from yfinance for several A-share tickers in this batch; values would need to be supplemented from `market_cap_cache.db` or per-issuer IR pages for any weighted-basket calculation (next refresh).
- 鼎智科技 (BSE:873593) is a relevant pure-play but Beijing Stock Exchange tickers are not yfinance-trackable — the basket is structured around yfinance-resolvable instruments to keep refresh cadence cheap. If yfinance adds BSE coverage, re-evaluate inclusion.
- Harmonic Drive Systems FY2026 net margin collapsed to 2.7% while revenue grew 7%; the stock's +127% 1Y move embeds an EPS recovery that has not yet started. Single-modality risk flagged in Drift signals.

## References

(Anchor URLs only — full URL set is in the Tracked tickers, Recent events, and Data Used sections above.)

**Theme anchors (Tesla Optimus + industry deep-dives):**
- [Tesla Optimus production timeline (Optimusk)](https://optimusk.blog/blog/tesla-optimus-production-timeline/) · [Tesla Optimus 3 timeline (Tesera)](https://www.tesery.com/blogs/news/elon-musk-reveals-aggressive-production-timeline-for-tesla-optimus-3) · [Basenor Tesla Optimus V3 full timeline, 2026](https://www.basenor.com/blogs/news/tesla-optimus-v3-production-starts-this-summer-full-timeline) · [人形机器人减速器全解析 (新浪)](https://www.sina.cn/news/detail/5294801543235159.html)
- [东方证券 丝杠：核心传动部件, 2023-10](https://zhongzhihui.oss-cn-beijing.aliyuncs.com/industryPdf/20231025-%E4%B8%9C%E6%96%B9%E8%AF%81%E5%88%B8-%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%B3%BB%E5%88%97%E6%8A%A5%E5%91%8A%EF%BC%9A%E4%B8%9D%E6%9D%A0%EF%BC%9A%E6%A0%B8%E5%BF%83%E4%BC%A0%E5%8A%A8%E9%83%A8%E4%BB%B6%EF%BC%8C%E4%BA%BA%E5%BD%A2%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%BC%80%E5%90%AF%E6%88%90%E9%95%BF%E7%A9%BA%E9%97%B4.pdf) · [华安证券 减速器深度, 2024-01](https://pdf.dfcfw.com/pdf/H3_AP202401101617055729_1.pdf) · [东吴证券 灵巧手深度, 2025-04-26](https://pdf.dfcfw.com/pdf/H3_AP202504261662702285_1.pdf) · [艾邦机器人 23家谐波减速器](https://www.aibangbots.com/a/2094) · [艾邦机器人 30+丝杠](https://www.aibangbots.com/a/2259)

**Material disclosures cited in Recent events:**
- [36Kr EN — Tesla / Sanhua $685M Optimus order, 2025-10-15](https://eu.36kr.com/en/p/3510288514980998) · [Nabtesco RVmini Monocrank launch, 2025-12-02](https://www.nabtesco.com/en/news/20251202-17329/) · [21经济网 五洲新春 募资10亿, 2025-06-17](https://www.21jingji.com/article/20250617/herald/05cf32584a26e6fdfc4a7e696cbf7333.html) · [新浪财经 环动科技招股书速读, 2025-10-06](https://finance.sina.com.cn/roll/2025-10-06/doc-infsyftk5550847.shtml) · [Yaskawa x SoftBank MOU, 2025-12-01](https://www.yaskawa-global.com/newsrelease/news/178574) · [新浪财经 华沿机器人 IPO, 2026-03-30](https://finance.sina.com.cn/wm/2026-03-30/doc-inhsueeu4004952.shtml) · [上交所 北特科技 募集说明书, 2025-12](https://static.sse.com.cn/stock/disclosure/announcement/c/202512/603009_20251205_7ZC1.pdf)

All other URLs (per-ticker primary sources, industry research, exclusions rationale) are inline-cited in the Tracked tickers and Data Used / 数据来源清单 sections above.

## History

- 2026-05-31 — theme created with 18-ticker basket (7 core, 7 enabler, 4 adjacent) following user request "Build a humanoid-robotics-actuators theme as complement to the existing sensors basket"; initial Performance / Recent events / Drift signals populated. Excluded: 鼎智科技 BSE:873593 (BSE listing not yfinance-trackable; seed had wrong SZSE ticker which is actually 中汽股份 CATARC), 德昌电机 HKEX:0179 (JPM "humanoid 进展缓慢" datapoint, no disclosed customer), 鸿日达 SZSE:301285 (connector maker, wrong category), 银轮股份 SZSE:002126 (thermal-management one layer removed), 国茂股份 SSE:603915 (humanoid revenue still <0.1% of group, ecosystem-stake only via DeepRobotics). Hua Yan Robotics HKEX:1021 added despite very short price history (IPO 2026-03-30) because its joint-module business is the relevant exposure and there's deep zsxq-evidence Deutsche initiating-buy report. Sanhua SZSE:002050 flagged as dual-listing with the sensors basket.
