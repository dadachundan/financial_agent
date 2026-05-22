# 凌云光技术股份有限公司 (Luster LightTech Group, SSE:688400) — Research Report

**Date:** 2026-05-16
**Ticker:** SSE:688400 (Shanghai STAR Market, 科创板)
**Subject company:** 凌云光技术股份有限公司 (Luster LightTech Group Co., Ltd.; English brand "Luster")
**Sector:** Machine vision / industrial AI (工业人工智能), with a meaningful optical-communications-trading sleeve
**HQ:** Haidian District, Beijing
**Founded:** August 2002 (joint-stock conversion September 2020)
**Listed:** 6 July 2022
**Auditor:** Tianjian (天健会计师事务所)
**Sponsor:** China International Capital Corporation (CICC, 中金公司)

---

## 1. Company Overview

凌云光 (Luster LightTech, ticker SSE:688400) is one of the two or three Chinese national champions in industrial machine vision. The company sells what management describes as "视觉 + AI" — a stack that runs from vision components (industrial cameras, lenses, light sources, frame grabbers) through vision systems (camera + algorithm + integration into a single inspection station) up to full intelligent-inspection equipment (turnkey machines used on factory floors). On the side, it operates a long-standing optical-communications distribution business and is pushing into newer photonics niches such as Optical Circuit Switching (OCS) for AI data-centres. The company was founded in 2002 in Beijing by 姚毅 (Yao Yi), 杨艺 (Yang Yi), and 卢源远 (Lu Yuanyuan), all veterans of the Beijing predecessor entity 北京凌云光通技术有限公司 that had started a 1995 distribution relationship with Teledyne DALSA (then a stand-alone Canadian sensor company, now part of Teledyne Technologies). That distribution franchise is still the anchor of the components business, and Luster has built itself outwards from it for two decades. The IPO in July 2022 on the STAR Market raised primary capital and gave it the balance sheet to consolidate the Chinese vision-systems market and, in January 2025, to close the all-cash acquisition of the Danish industrial-camera maker JAI A/S — the first material China-outbound deal in machine-vision history ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 22).

**Headline FY2025 financials (RMB):**

| Metric | FY2025 | FY2024 | YoY |
|---|---:|---:|---:|
| Revenue | 2,911.67 M | 2,233.78 M | +30.35% |
| Net profit (attributable) | 161 M | 107 M | +50.70% |
| Non-GAAP net profit | 123 M | 66 M | +86.05% |
| Gross margin (consolidated) | 34.79% | 34.66% | +13 bps |
| R&D spend (P&L + capitalised) | 510.5 M | 444.3 M | +14.89% |
| R&D / revenue | 17.53% | 19.89% | -2.36 pp |
| Operating cash flow | 146.8 M | 191.0 M | -23.15% |
| Headcount (year-end) | 1,896 | n/a | n/a |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), pp. 38-40, 51, 68.

**Valuation snapshot (as of mid-May 2026).** Per the [Investing.com Luster LightTech page](https://www.investing.com/equities/luster-lighttech) and cross-checked against [Eastmoney quote 688400](http://quote.eastmoney.com/kcb/688400.html), the stock trades around RMB 63 with 460.98 million shares outstanding (post the April 2025 cancellation of 2.52 million buy-back shares — [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 115) for a market capitalisation of roughly RMB 29.0 billion (≈ US$ 4.0 billion). TTM P/E sits in the 100–180× range depending on whether one uses the trailing FY25 attributable EPS of RMB 0.35 (giving ~180×) or Investing.com's non-GAAP-blended EPS of RMB 0.77 (~82×). TTM P/S is roughly 10×, P/B ≈ 5.4×. The Chinese machine-vision peer set — 奥普特 (OPT, SSE:688686), 天准科技 (Tianzhun, SSE:688003), 矩子科技 (Test Research, SHE:300802), 海康机器人 (Hikrobot, recently re-listed) — trades in a TTM-P/E range of roughly 45–80× and TTM-P/S range of 6–10× ([Eastmoney sector page](https://data.eastmoney.com/bkzj/BK1037.html)). Luster therefore trades at a premium to the median Chinese vision peer, with the entire excess multiple resting on three narratives: (1) FY25 was the bottom of a 3C / consumer-electronics capex cycle and the operating leverage will compound through FY26–FY27, (2) the JAI acquisition durably re-rates the components business toward Cognex/Keyence gross-margin profiles, and (3) the FZMotion optical-motion-capture line gives Luster a credible "embodied-AI / humanoid-robotics" toll-road. The first is reasonable, the second is plausible but unproven, and the third is, in our judgement, where most of the multiple-expansion-risk sits — FZMotion is still a single-digit-percent-of-revenue product and competitors (OptiTrack, Vicon, NOKOV) are mature. We treat anything above 100× TTM P/E as a multiple-compression risk that belongs in Section 9.

**Strategic positioning in one paragraph.** Luster sits at the intersection of three secular Chinese industrial demand stacks: (a) Apple-supply-chain inspection (camera modules, displays, glass), (b) new-energy and EV battery inspection (CATL, Eve, BYD lines), and (c) the emerging embodied-AI / humanoid-robotics tooling stack (motion-capture, training-data acquisition). The fourth stack — optical communications for AI infrastructure (OCS, photonic wire bonding, OIO) — is being seeded but is not yet a P&L driver. Among Chinese competitors, Luster is the only listed pure-play that combines self-developed CMOS-based industrial cameras (post-JAI), self-developed vision algorithms (the F.Brain deep-learning platform and the older VisionWARE 6.x library), and self-developed inspection equipment under one roof. 奥普特 is stronger in light sources and lenses; 海康机器人 dominates volume cameras; 天准科技 is more an applied-systems integrator; Hikrobot leads in volume. Only 凌云光 has a serious end-to-end stack at the high-mix / high-spec end of the Chinese market.

---

## 2. Business Model and Products

Luster reports through two reporting segments — **机器视觉 (Machine Vision)** and **光通信 (Optical Communications)** — which we describe in turn. FY25 revenue mix was 80.6% machine vision (RMB 2,345.86 M, +44.72% YoY) and 19.4% optical communications (RMB 565.68 M, -7.70% YoY), with consolidated gross margins of 35.95% and 29.95% respectively ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 39).

### 2.1 Machine Vision — three product tiers

Within machine vision, FY25 revenue split by product class is the most important number in the report:

| Product line (machine vision) | FY25 revenue (RMB M) | YoY | GM |
|---|---:|---:|---:|
| 视觉器件 Vision components (cameras, lenses, light sources, frame grabbers) | 378.63 | +219.21% | 32.06% |
| 视觉系统 Vision systems (camera + algorithm + station) | 735.99 | +6.39% | 40.15% |
| 智能视觉装备 Intelligent vision equipment (turnkey lines) | 1,191.32 | +53.72% | 34.49% |
| 服务收入 Services (training, maintenance, integration) | 39.93 | +12.37% | 38.95% |
| **Machine-vision sub-total** | **2,345.86** | **+44.72%** | **35.95%** |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 40.

**Vision components (RMB 379 M, +219% YoY).** This line tripled in FY25 almost entirely because of the JAI consolidation — JAI A/S was acquired in November 2024 and consolidated from 1 January 2025. JAI brings a premium industrial-camera line strong in line-scan, multi-spectral, and area-scan cameras for the European, Japanese, and Korean markets ([JAI A/S product portfolio](https://www.jai.com/products)). Pre-JAI, Luster's own-brand components were largely Chinese-market-only, and the components line was sub-RMB 120 M; post-JAI, Luster owns a globally-recognised brand and has effectively closed the gap on the European camera tier (Basler, IDS, Allied Vision). The trade-off is that JAI consolidates at a lower gross margin than Luster's standalone vision-systems and vision-equipment lines because it carries European manufacturing and engineering cost — hence the 32% segment GM here vs the 40% on vision systems. The "vision components" tier also still includes Luster's distribution of third-party brands such as Teledyne DALSA, FLIR, Xenics, PCO, Andor, ZEISS, Pleora, Datalogic, Ximea, LMI, Vision Research and roughly 50 others ([Luster English imaging partner page](https://en.lusterinc.com/imaging/partners/)).

**Vision systems (RMB 736 M, +6% YoY).** The vision-system line packages cameras, light sources, motion stages, controllers, and Luster's own algorithm stack into a single "inspection station." These are sold most heavily into consumer-electronics camera-module inspection (where Luster has been an Apple-supply-chain preferred supplier since 2016), display assembly, and printing / packaging quality control. Gross margin of 40.15% is the highest in the company and reflects the price the customer pays for "ready-to-use" vs "build-your-own." The +6% growth in FY25 is the soft spot in the company — vision-system revenue grew almost 50% in FY23 then fell sharply in FY24 with the Apple-supply-chain capex pause, and FY25's mid-single-digit recovery suggests the recovery has been narrower than headlines imply. Management commentary on p. 21 of the 2025 annual report attributes this to "战略产品聚焦" (strategic product focus) — i.e. Luster is deliberately walking away from low-margin, project-based system sales and pushing toward a more productised, standardised system catalogue.

**Intelligent vision equipment (RMB 1,191 M, +54% YoY).** The "turn-key inspection machine" line is now the largest single product class. Three sub-applications dominate: (a) **lithium-battery inspection** — surface defect, dimensional, and X-ray inspection for prismatic, pouch, and cylindrical cells; CATL (宁德时代) is the headline customer here, and management called out FY25 new-energy-related revenue as a high-double-digit grower ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 22); (b) **printing & packaging inspection** — a long-standing Luster franchise where it is the Chinese single-product champion (单项冠军产品, awarded by MIIT in 2022), with the Swiss group BOBST as a strategic partner; and (c) **3C / consumer-electronics inspection equipment** — entire vertical lines that go inside Foxconn / Luxshare / AAC / Goertek factories to do camera-module assembly inspection, display-panel inspection, and component sorting. Gross margin of 34.49% is healthy for capital equipment, suggesting Luster has pricing power inside its installed base.

**Services (RMB 40 M, +12%).** Small line, mostly customer-success / training. Not material to the thesis.

### 2.2 Optical Communications — two distinct sub-businesses

| Optical-comm product | FY25 revenue (RMB M) | YoY | GM |
|---|---:|---:|---:|
| 光通信产品 (distribution + self-developed) | 565.68 | -7.70% | 29.95% |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 40.

The optical-comm line is two businesses bundled: (a) a long-standing **distribution agency** representing foreign optical-component brands in China, which has been the historic revenue driver but is now in structural decline because (i) Chinese fibre-network capex peaked years ago and (ii) US-China export-control overlays have made the agency model less reliable; and (b) a **newer self-developed component line** focused on AI-data-centre photonics — most notably Optical Circuit Switching (OCS), Optical I/O (OIO), and photonic wire bonding. The Q1 2026 report explicitly states: "传统业务受国际环境影响" (legacy business affected by international environment), pointing to the US-China overlay ([2026 年第一季度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225286215.PDF), p. 2). The new-tech sub-line is small but is the primary "AI infrastructure" call option in the segment.

### 2.3 Geographic mix

| Region | FY25 revenue (RMB M) | YoY | GM |
|---|---:|---:|---:|
| 境内 (China domestic) | 2,517.58 | +22.24% | 33.74% |
| 境外 (Overseas) | 393.96 | +126.03% | 41.44% |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 40.

The doubling of overseas revenue is the JAI effect — JAI's existing European, Japanese, and Korean book lifted the overseas line from RMB 174 M to RMB 394 M overnight. The overseas gross margin of 41.4% is meaningfully above domestic 33.7%, which validates the strategic case for the JAI deal: high-mix, high-spec international camera customers pay better than Chinese smartphone-OEM project tenders.

### 2.4 Sales model

Luster sells direct to most large strategic accounts (Apple supply chain, CATL, BOE) and through distributors for components in the long-tail of small Chinese factories and labs. Sales cycles for intelligent-vision equipment can be 6–18 months; for vision-system stations, 3–9 months; for components, off-the-shelf or stocked. Contracts are generally PO-by-PO rather than multi-year framework — this is normal for Chinese capital equipment but means revenue visibility is lower than for SaaS-like comparables.

---

## 3. Management and Governance

### 3.1 Key executives

**姚毅 Yao Yi (61) — Chairman & General Manager, Co-founder.** Beijing Jiaotong University trained, taught at the photonic-wave lab there from 1995–1997, then served as executive director / GM of the Beijing-LingyunGuangtong predecessor entity from 1997–2002, before co-founding the current Luster in August 2002. He owns 200.24 M shares = **43.44% of share capital** as of year-end 2025, easily the controlling shareholder and 实际控制人 (de-facto controller). Yao won a 2012 国家技术发明一等奖 (State Technology Invention First Prize) for "Stereo Video Reconstruction and Display Technology" and two State Science & Technology Progress Second Prizes (2016, 2019). His FY25 pre-tax compensation was RMB 844,100 — low for a chairman/GM of a RMB 29-billion-market-cap company, which is governance-positive (he is paid in equity, not salary) ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 58).

**王文涛 Wang Wentao (52) — Vice Chairman, Vice GM, Co-founder.** Joined the Beijing predecessor as a sales manager in November 2001 and was a co-founder of the current entity in 2002. Holds 13.68 M shares (= 2.97%). FY25 compensation RMB 1,026,100. Sits on the council of the China Optical Engineering Society. In 2025 he was appointed to directorships at Photonicx AI Pte. Ltd. (Singapore) and Stardust Photonics Technology Pte. Ltd. — Singapore-domiciled JV vehicles tied to Luster's overseas photonics strategy ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 62).

**杨艺 Yang Yi (56) — Director, Vice GM, Co-founder.** The female co-founder of the company; prepared the predecessor entity's incorporation from 1996 and served as supervisor 1996–2002 before co-founding the current company. Holds 23.54 M shares (= 5.11%). FY25 compensation RMB 942,400. She is Vice Chair of the China Machine Vision Industry Union (机器视觉产业联盟, CMVU) — the de facto industry body — which gives Luster strong "policy-corridor" visibility. She also sits on the board of 长光辰芯 (Changchun Changguang Chenxin Microelectronics), the Chinese CMOS sensor company that ICAP-listed in 2024 and is the highest-profile domestic competitor to Sony's IMX-series sensors.

**顾宝兴 Gu Baoxing (46) — CFO and Board Secretary.** Joined Luster in September 2018. Before Luster, ten years at Huawei in increasingly senior finance roles: finance manager for Optical Network Product Line (2007–2012), finance manager Europe regional HQ (Vodafone account), CFO Huawei UAE subsidiary (2012–2016), Director of Group Supply-Chain Finance (2016–2017). FY25 compensation RMB 1,764,100, the highest among management — a sign that Yao Yi pays expertise hires market rates even while paying himself founder-equity rates. His Huawei pedigree is critical: it brings the IPD (Integrated Product Development) finance discipline that Luster needed to migrate from project-shop to product-company. ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 60.)

**赵严 Zhao Yan (50) — former Vice GM (resigned as director 2025-09-16).** Joined the company in 2004; ran successively the optics department, the system design centre, the industrial-vision business unit, and the display BU. Holds 5.31 M shares. Sold 773,010 shares in FY25, a small but worth-noting insider sale.

**邬欣然 Wu Xinran (47), 李宁 Li Ning (42), 吴耀杰 Wu Yaojie — Assistants to the GM.** All long-tenured insiders (15–20 years each) who run the operating business units (consumer-electronics BU, intelligent-industry BU, strategy & marketing). FY25 compensation in the RMB 1.5–1.9 million range — productively paid line managers.

### 3.2 Board composition and independence

The board has nine seats (eight directors + employee-rep director) with three independent directors:

- **王琨 Wang Kun** — Associate Professor at Tsinghua SEM (school of economics & management); board career on multiple A-share boards including Goertek (歌尔股份).
- **西小虹 Xi Xiaohong** — Investment management / private-equity background; founding council member of the China Independent Non-Executive Director Association.
- **孙富春 Sun Fuchun (62)** — Tenured professor at Tsinghua Computer Science Department, Vice President of the China Artificial Intelligence Society. He is the most technically credentialed independent director and arguably the AI/robotics "halo" the company uses externally.

Two non-independent / shareholder-rep directors are noteworthy:
- **邬曦 Wu Xi (45)** — Partner, Executive President, and CIO of Dachen Capital (达晨创投), Luster's pre-IPO PE investor. Harvard visiting scholar 2019–2020.
- **许兴仁 Xu Xingren (50)** — General Manager of the iPEBG business group at Foxconn Industrial Internet (工业富联) from March 2025; he is the Foxconn director, sitting on Luster's board as nominee of 富联裕展 (FII subsidiary), which holds the pre-IPO strategic stake.

**Independence assessment.** Board structure meets STAR-Market requirements (≥1/3 independent directors; audit committee chaired by an independent director). Yao Yi simultaneously holding both Chairman and General Manager roles is flagged on p. 55 of the 2025 annual report as triggering Article 72 of the Listed Company Governance Rules — the company defends the dual-role with a standard set of "separation of authority" provisions. We rate the governance as **acceptable but founder-controlled**: Yao Yi at 43.4% has effective veto over every board decision, and minority-shareholder protection rests on the independence of the three independent directors and on STAR Market enforcement, not on board arithmetic.

### 3.3 Insider ownership and selling pressure

| Holder | Shares | % |
|---|---:|---:|
| Yao Yi (founder, Chairman/GM) | 200.24 M | 43.44% |
| Yang Yi (co-founder) | 23.54 M | 5.11% |
| Wang Wentao (co-founder) | 13.68 M | 2.97% |
| Zhao Yan (former Vice GM) | 5.31 M | 1.15% |
| 富联裕展 (Foxconn Industrial Internet subsidiary) | ≈ 9.8 M | 2.12% |
| 31,269 public ordinary shareholders | balance | ~ 45% |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), pp. 116-117.

**Key lock-up event of 2025:** On 7 July 2025 the IPO-lockup tranche held by Yao Yi and Yang Yi (223.78 M shares, 48.28% of capital) released into free float. Both founders publicly committed to a "无减持承诺" (no-reduction commitment), but the technical overhang is unavoidable — anyone modelling supply/demand of paper through FY26–FY27 should treat this as the dominant variable. 富联裕展 has separately disclosed a small reduction plan in April 2026.

---

## 4. Products in Detail (Walking the Product Tree)

Beyond the segment-and-tier classification in Section 2, Luster's actual product catalogue runs deeper. The company's English site ([en.lusterinc.com](https://en.lusterinc.com/)) and Chinese site ([lusterinc.com](https://www.lusterinc.com/)) enumerate the following:

**Industrial cameras (vision components).** Own-brand "LUSTER" area-scan and line-scan cameras; the full JAI A/S catalogue (Apex, Wave, Sweep, Fusion, Spark, Spectro, Go series — line-scan, multi-spectral, area-scan, 3D, and prism-based 2-CCD/3-CCD cameras for colour-and-NIR or hyperspectral); distributed brands (Teledyne DALSA Linea / Piranha / Genie line; FLIR Blackfly / Oryx; Andor; PCO; Photonis; Vision Research Phantom; Ximea; LMI Gocator 3D; etc.).

**Optics & light sources.** Self-developed engineered illumination (dome, ring, coaxial, bar, line-scan illumination); Telecentric lenses (自研 + 代理 Computar / Schneider / Edmund / ZEISS); LED + laser-based structured-light projectors for 3D inspection.

**Frame grabbers and vision controllers.** Self-developed PCIe frame grabbers; partnership with Teledyne DALSA Xtium series for high-bandwidth line-scan applications; embedded vision controllers running VisionWARE.

**VisionWARE algorithm library (v6.3).** ~18 toolboxes (~200 individual tools): traditional 2D image processing (geometric matching, blob, edge, OCR), 3D point-cloud processing (registration, segmentation, primitive fitting), and a deep-learning module that wraps F.Brain models for defect detection, classification, and segmentation. VisionWARE is sold both bundled with Luster systems and as a standalone SDK licence.

**F.Brain deep-learning platform.** A 2023-introduced workbench for training and deploying defect-detection neural networks; supports few-shot learning, anomaly detection on unbalanced data, and on-edge inference. F.Brain is now the AI engine underneath both the system-tier and equipment-tier offerings ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 22).

**FZMotion optical motion capture (the "humanoid robot" line).** A multi-camera infrared optical motion-capture system functionally analogous to OptiTrack/Vicon, used (a) to capture human motion as training data for humanoid robots, (b) for film/VFX virtual production, and (c) for biomechanics / sports labs. FZMotion was the system used to capture the routine that drove the Unitree H1 humanoid-robot performance "秧Bot" at the 2025 CCTV Spring Festival Gala — a marketing event that drove the stock's narrative re-rating in February 2025. ([Sohu coverage of Unitree partnership](https://www.sohu.com/a/877788995_121924584).)

**Lithium-battery inspection equipment.** Surface defect, electrode tab, OCV/OCR, dimensional, weld-seam X-ray, and final-product appearance inspection for prismatic and pouch cells. Customers include CATL (宁德时代). Management said FY25 new-energy revenue grew strongly (no explicit % disclosed for the calendar year, but 1H25 release said new-energy +45% YoY).

**Display inspection equipment.** OLED Mura defect, AOI, Cell test, Demura — supplied to BOE (京东方), TCL CSOT, Tianma, Visionox.

**Printing & packaging inspection equipment.** Web inspection, label inspection, security-printing inspection. Partnership with BOBST Group (Switzerland). This is where Luster won its "single product champion" designation (2022) — the only product category where the company is unambiguously the global / Chinese number one.

**Semiconductor packaging inspection (emerging).** AOI for advanced packaging, wafer-level inspection. Small revenue base; the competitive set here (KLA, Camtek, ASML, AppliedMaterials) is daunting.

**Optical-communications products (emerging).** OCS all-optical switches for AI data-centre fabrics; Optical I/O (OIO) and photonic wire bonding for board-level optical compute; EDFAs; fibre-splicing instruments.

The breadth is striking — Luster runs four distinct industrial verticals (3C electronics, display, new-energy, printing/packaging) plus two emerging adjacencies (semiconductor inspection, optical communications) plus one narrative call-option (humanoid-robotics tooling). The risk of breadth is execution dilution; the upside is that no single end-market collapse (consumer electronics in FY24 being the recent test case) can take the whole company down.

---

## 5. Customers and Concentration

This is the single most important — and most surprising — section of the report. Luster discloses in its annual report a remarkably **low** customer-concentration profile by Chinese industrial-capital-equipment standards:

| Rank | FY25 revenue (RMB M) | % of FY25 sales | Related party? |
|---:|---:|---:|---|
| #1 | 376.84 | **12.94%** | **Yes** |
| #2 | 167.94 | 5.77% | No |
| #3 | 75.38 | 2.59% | No |
| #4 | 58.65 | 2.01% | No |
| #5 | 57.13 | 1.96% | No |
| **Top 5 total** | **735.94** | **25.28%** | — |

Source: [2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 42.

**Three observations.**

**(1) Top-5 at 25% is well below industry norm.** For comparison, the Chinese listed industrial-AI / vision peer set typically discloses top-5 customer concentration in the 40–55% range and top-1 above 15%. Luster's 25.28% / 12.94% is structurally lower — a benefit of running four distinct end-markets simultaneously, each with multiple large buyers.

**(2) The #1 customer is a related party at 12.94%.** The annual report does not name the customer, but the dots connect cleanly to Foxconn Industrial Internet (工业富联) and its sub-entity 富联裕展 (which holds Luster's 2.12% pre-IPO strategic stake and provides the board director 许兴仁). The same group has a joint venture with Luster called 富联凌云光科技 (Shenzhen-based, established 2020). So Luster is **simultaneously equity-owned by, JV-partnered with, and a vendor to** the Foxconn Industrial Internet group, which is the largest assembler in the Apple supply chain. This relationship is the central feature of Luster's customer book and the central risk: it gives Luster preferred access to the world's largest electronics-assembly platform, and it makes the company sensitive to (a) Foxconn's own capex cycle, which mirrors Apple iPhone-form-factor refresh cycles, and (b) any deterioration in the Apple-China supply-chain relationship. Note also that the top-1 in FY24 (during the Apple-capex pause) was meaningfully smaller — the rebound to 12.94% in FY25 is itself a signal that the Apple-chain capex has reopened.

**(3) The remaining top-5 are unconcentrated.** No #2-#5 customer is above 6%. That breadth suggests Luster's CATL, BOE, BYD, Goertek, Luxshare, AAC, and CCTV/Migu relationships are diversified across multiple counterparties, none of which alone is decisive.

**Tradeoff vs Apple-tier supplier 立讯精密 (Luxshare) / AAC.** Both Luxshare and AAC report Apple-direct concentration above 70% — Luster, sitting one step upstream, has the same end-customer exposure (the Apple iPhone) but expressed across multiple direct buyers (Foxconn, Luxshare, AAC, Goertek, BYD Electronics), which materially diversifies the counterparty book even though the underlying demand driver is the same iPhone form-factor cycle. **For the purposes of risk analysis we treat the Apple-iPhone capex cycle, not customer-name concentration, as the central concentration risk** (Section 9.1).

**Supplier concentration is also low.** Top-5 suppliers were RMB 304.29 M = 16.50% of total purchases, none related party ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 42). The largest implicit single dependency — Teledyne DALSA as a sensor / camera supplier — is not in the top-5 by purchase value after Luster brought JAI camera capacity in-house.

---

## 6. Industry and Market

### 6.1 Defining the industry

Machine vision sits at the intersection of optics, sensors, computing, and AI. The narrow definition (cameras + lenses + lights + frame grabbers + algorithm software) is what's typically meant in industry market-sizing. The broader definition adds **vision systems** (camera + algorithm packaged as a station) and **intelligent inspection equipment** (turnkey machines on factory floors). Luster operates across the full breadth. The China Machine Vision Industry Union (CMVU / 中国机器视觉产业联盟) — of which Luster's co-founder Yang Yi is Vice Chair — is the authoritative industry body for Chinese sizing.

### 6.2 Market size and growth

**Global:** Per [Grand View Research](https://www.grandviewresearch.com/industry-analysis/machine-vision-market), the global machine-vision market was approximately US$ 14–16 billion in 2024 and is projected to grow at ~8–10% CAGR through 2030. Coherent Market Insights and MarketsandMarkets give comparable ranges. Pulling in the broader "industrial-imaging plus 3D plus embedded-vision" stack expands the addressable market to US$ 25 billion+.

**China:** CMVU and a range of Chinese sell-side notes size China's industrial machine-vision market at roughly **RMB 18–22 billion in 2024**, growing at 12–15% CAGR — a faster rate than the global average, driven by (a) the lithium-battery and EV capex cycle, (b) semiconductor onshoring (advanced packaging), (c) display capacity build (OLED, MicroLED), and (d) the new embodied-AI / humanoid-robotics tooling pull. If one assumes ~13% CAGR, China reaches roughly RMB 35–45 billion by 2030.

**Luster's share.** Against an RMB 20 billion 2024 China market, Luster's FY25 machine-vision revenue of RMB 2,346 M implies roughly a **10–12% share of the Chinese market**, putting it in the top three behind Hikrobot (海康机器人, ≈ RMB 4–5 billion 2024 sales but with most revenue in volume components) and roughly even with OPT (奥普特, FY24 revenue ≈ RMB 0.9 billion but on track for ≈ RMB 1.3 billion FY25 per company guidance). In high-mix, equipment-led applications (vs volume components) Luster is plausibly the **number-one Chinese player by revenue**.

### 6.3 Demand drivers

- **Lithium-battery and new-energy** — CATL, BYD, Eve, Sunwoda, Gotion all expanded inspection-equipment capex aggressively in FY24-FY25 as battery yields became the bottleneck for the EV ramp. Luster grew its new-energy revenue +45% YoY in 1H25.
- **Apple-iPhone cycle** — the FY24 capex pause caused Luster's FY24 revenue decline of -15%; the FY25 rebound reflects renewed iPhone form-factor and camera-module activity. Foldable iPhone (rumoured 2026/2027) and Apple Vision Pro 2 are the next demand catalysts.
- **Embodied AI / humanoid robotics** — the most narrative-driven driver. FZMotion sales to Unitree, UBTech, and 智元 (Agibot) for training-data acquisition; demand for component-level vision in humanoid-robot perception stacks (cameras + 3D + algorithm). Real revenue is still small but the multiple lives here.
- **OCS / optical communications** — Google has deployed OCS in production data centres; if AWS, Microsoft, and Meta follow, the TAM expands from the low single-digit billion-USD to potentially > US$ 10 billion by 2030.
- **Semiconductor packaging** — HBM, chiplet, 2.5D / 3D packaging all require vision-based final inspection. KLA dominates; Luster is a marginal entrant.

### 6.4 Competitive structure

The Chinese industrial-machine-vision market is **fragmented at the components tier and consolidating at the equipment tier**.

| Competitor (global) | Position | FY24 revenue (approx.) | Approx. global share |
|---|---|---:|---:|
| **Keyence (6861.T)** | Components + sensors, premium pricing | US$ 8.7 B group revenue (vision est. > US$ 2 B) | ~14% |
| **Cognex (CGNX)** | Vision software + smart cameras, US leader | US$ 0.91 B | ~11% |
| **Teledyne (TDY) / DALSA** | Cameras, line-scan, sensors | vision est. ~ US$ 1 B | ~7% |
| **Basler (BSL.DE)** | Industrial cameras (volume tier) | EUR 0.16 B | ~3% |
| **Omron** | Sensors + vision stations | n/a | ~2% |

| Competitor (China) | Position | FY24 revenue | Notes |
|---|---|---:|---|
| **Hikrobot 海康机器人** | Volume cameras + mobile robots; spinoff of Hikvision | RMB ~ 4–5 B | Listed mid-2024; STAR Market premium multiple |
| **奥普特 OPT (SSE:688686)** | Components (light sources, lenses), the most "pure-play" comp | RMB ~ 0.9 B | Profitable, lower-growth |
| **凌云光 Luster (SSE:688400)** | End-to-end, top of equipment tier | RMB 2.92 B (FY25) | Subject company |
| **天准科技 Tianzhun (SSE:688003)** | Applied systems / 3D measurement | RMB ~ 1 B | Apple-supply-chain exposure |
| **矩子科技 Test Research (SHE:300802)** | AOI, SPI for PCB | RMB ~ 0.5 B | Smaller, niche |
| **大恒图像 Daheng** | Components, distribution | n/a | Unlisted |

Source: company filings and industry reports. Global market-share figures from Coherent Market Insights and industry sizing notes; sell-side reports note that the published share rankings vary materially by methodology (top-line revenue vs vision-only revenue vs unit shipments).

**Luster's specific positioning.** Among the Chinese listed names, Luster is the **only one that simultaneously owns a tier-1 European-brand industrial-camera line (JAI), a self-developed deep-learning algorithm stack, and an installed base of intelligent-inspection equipment in the Apple / CATL / BOE supply chains**. Hikrobot is bigger but is more volume-oriented; OPT is pure-play components without equipment scale; Tianzhun is more project-services. The closest global analogues are Cognex and Keyence — Cognex on algorithms-and-smart-cameras, Keyence on premium components-and-sensors. Luster trades at premium multiples to Cognex (TTM P/E ~30× per Cognex's FY24 numbers) but at premium-discount to Keyence (TTM P/E ~30× per Keyence FY24).

---

## 7. Total Addressable Market (TAM)

Aggregating the addressable pools:

| TAM bucket | 2024 size (approx.) | 2030 size (approx.) | CAGR | Luster relevance |
|---|---:|---:|---:|---|
| Global machine vision (narrow) | US$ 14–16 B | US$ 25–30 B | ~9% | Direct competitor pool |
| **China machine vision** | **RMB 18–22 B** | **RMB 35–45 B** | **~13%** | **Primary home market** |
| Global industrial cameras (sub-segment of above) | ~US$ 3 B | ~US$ 5 B | ~9% | JAI relevance |
| Global optical-motion-capture | ~US$ 0.2 B | ~US$ 0.5–1.0 B | ~20%+ | FZMotion direct |
| Embodied-AI / humanoid-robotics enabling tooling | early-stage / unmeasured | $multi-B by 2030 | n/a | Optionality |
| Optical Circuit Switching (OCS) | ~US$ 0.3 B | US$ 2–5 B | 30%+ | Optional |
| Semiconductor packaging inspection | ~US$ 1.5 B | ~US$ 3 B | ~12% | Marginal entrant |

The TAM picture is favourable: Luster's primary market grows mid-teens, its components sub-market grows high-single-digits, and the optionality buckets (humanoid robotics, OCS, semi packaging) are all upward-skewed. At Luster's FY25 revenue of ~RMB 2.9 billion against an RMB 18–22 billion China TAM, **the company captures roughly 13–16% of its primary serviceable market** — high enough that further share gains will get harder, and the next leg of growth has to come from (a) Chinese-market growth itself, (b) overseas expansion via JAI, and/or (c) new TAM unlocked by humanoid robotics and AI infrastructure.

---

## 8. Recent Operating Performance and Q1 2026 Update

### 8.1 Multi-year financial trajectory

| (RMB million) | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|
| Revenue | ~2,650 | ~2,640 | 2,233.78 | 2,911.67 |
| Revenue growth | n/a | ~0% | -15.4% | +30.4% |
| Net profit (attributable) | ~204 | ~164 | 107 | 161 |
| Net-profit growth | n/a | -20% | -35% | +50.7% |
| Non-GAAP net profit | ~150 | ~122 | 66 | 123 |
| Gross margin | 28.2% | 30.9% | 34.7% | 34.8% |
| R&D / revenue | n/a | n/a | 19.9% | 17.5% |

Pre-FY24 numbers reconstructed from prior annual reports and FY24 disclosures.

The shape of the multi-year P&L tells the central story: a flat 2022–2023, a sharp 2024 trough as the Apple-supply-chain capex cycle paused and consumer-electronics inventory destocked, then a strong 2025 rebound driven by (a) re-acceleration of 3C capex, (b) new-energy / battery capex strength, (c) the JAI consolidation adding ≈ RMB 250 million of revenue, and (d) operating leverage that turned a 30% revenue lift into a 50% net-profit lift.

### 8.2 Q1 2026 update (filed 28 April 2026)

Per the [2026 年第一季度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225286215.PDF):

- Q1 2026 revenue: **RMB 597 M (-2.79% YoY)** — slight headline decline.
- Q1 2026 attributable net profit: **RMB 200 M (+1,233% YoY)** — but this is misleading; the large jump comes from a **RMB 173 M fair-value gain** on Luster's investment in 智谱华章 (Zhipu AI, the leading Chinese foundation-model startup). Luster's overseas subsidiary served as a cornerstone investor in Zhipu's most recent funding round.
- Q1 2026 non-GAAP net profit (excluding the Zhipu gain): RMB 46.5 M (+562% YoY) — the meaningful number.
- Machine vision Q1 revenue: RMB 476 M (+3.13% YoY) — modest growth.
- Optical-communications revenue: declined, attributed to "international environment" (= US-China export-control pressure on the distribution book).
- Overseas revenue +23% YoY — JAI consolidation continuing to deliver.

The Q1 print is more mixed than the 2025 full-year print. The Zhipu fair-value gain dominates the headline; the underlying operating business is growing only low-single-digits in Q1. The market will look to Q2 and 1H 2026 to confirm whether the FY25 acceleration is durable.

### 8.3 Capital raise

In November 2025 Luster filed for a private placement to a specific list of investors ("向特定对象发行 A 股股票") to fund capacity expansion and AI/OCS R&D — full details in the [SSE announcement 688400_20251120](https://static.sse.com.cn/stock/disclosure/announcement/c/202511/688400_20251120_HX3W.pdf). The placement adds dilution risk over FY26–FY27 alongside the founder lock-up release.

---

## 9. Risk Assessment

We identify ten risks across the four standard buckets — company-specific, industry/market, financial, macro.

### 9.1 Apple-supply-chain capex cyclicality (Company-specific)
The FY24 revenue decline of 15% maps almost cleanly to the Apple-iPhone capex pause and consumer-electronics inventory correction. Roughly 40–50% of Luster's vision-system and intelligent-equipment revenue ultimately depends on the iPhone capex cycle (via Foxconn, Luxshare, AAC, Goertek). A future Apple-pause — whether driven by an iPhone-cycle plateau, a soft form-factor refresh, or geopolitically-driven supply-chain reorientation — would compress Luster's revenue 10-20% in the affected year and disproportionately compress profit because the impacted business is mostly the highest-margin vision-systems tier. Mitigant: customer-name-level concentration is low (top-1 only 12.94%, even if all customers are end-Apple-driven), the new-energy and printing & packaging verticals have grown to roughly 30%+ of revenue and partially counterweight, and management has explicitly diversified into humanoid robotics and OCS.

### 9.2 Related-party transactions and Foxconn dependency (Company-specific)
The largest customer at 12.94% of FY25 sales is a related party — almost certainly Foxconn Industrial Internet (工业富联). This generates an unusual triple linkage: Foxconn is simultaneously **equity holder** of Luster (2.12% via 富联裕展), **board nominator** (one director seat), **JV partner** (富联凌云光), **and largest customer**. Related-party transactions are disclosed and audited, but the structural conflict — Foxconn's interest as a customer is to extract margin, while as an equity holder it benefits from Luster keeping it — is permanently present. If Foxconn ever reduces its strategic stake (a small reduction was announced in April 2026) the customer-relationship signal would also weaken. Mitigant: pricing of related-party transactions is independently audited; the volume of related-party revenue is fully disclosed each year; Foxconn's strategic incentive to maintain the relationship is real (Luster's IP gives Foxconn an edge on Apple bids).

### 9.3 Goodwill impairment from JAI acquisition (Company-specific / Financial)
The 2025 annual report explicitly flags JAI goodwill as an impairment risk ([2025 年年度报告](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF), p. 38). If JAI's European/Japanese-Korean customer book weakens (camera-market mature, competition from Chinese components moving into Europe), Luster would write down the goodwill — a non-cash but optically large hit that historically de-rates Chinese names sharply. Mitigant: 2025 JAI performance was reportedly above pre-acquisition expectations after Luster restructured JAI's governance and refocused on strategic customers.

### 9.4 Founder lock-up release and equity overhang (Financial / Market)
The IPO-lockup tranche of 223.78 million shares (48.28% of capital, held by Yao Yi and Yang Yi) released on 7 July 2025. Both founders have publicly committed not to reduce, but the option to do so now exists. Together with the November 2025 private-placement filing and the small 富联裕展 reduction plan in April 2026, the technical supply backdrop is the heaviest it has been since IPO. Mitigant: Yao Yi has personally committed in public filings to "do not reduce"; the founder's incentive at 43% ownership is firmly aligned with long-term holders.

### 9.5 Valuation / multiple compression (Financial / Market)
At TTM P/E in the 100–180× range (depending on EPS basis) and TTM P/S ~10×, Luster trades at a premium to its Chinese vision peers and to global comps (Cognex, Keyence, Basler all at < 40× P/E). The premium is justified only by the consensus assumption that FY26 grows another 25–40% and FY27 a similar pace — i.e. that the FY24-trough is one-off and the embodied-AI narrative converts to revenue. If FY26 disappoints (e.g. Q1 already showed only +3% machine-vision revenue), the multiple compresses 30-50% even without an earnings miss. This is, in our judgement, the largest single source of investor return-risk.

### 9.6 Competitive intensity from Hikrobot, OPT, and global incumbents (Industry / Market)
The Chinese vision market is **adding** capacity faster than it is consolidating: Hikrobot's mid-2024 re-listing funded aggressive volume-component expansion at price points Luster cannot match; OPT continues to win lights-and-lenses share; Cognex and Keyence retain stickiness in semiconductor and FA applications where Luster has minimal share. Long-run, the market may bifurcate into a high-volume tier (Hikrobot, Basler) and a high-spec equipment tier (Luster, Keyence, Cognex) — but the transition period will be margin-compressive across the board. Mitigant: Luster's end-to-end stack is genuinely differentiated and the F.Brain/VisionWARE algorithm moat is hard to replicate.

### 9.7 Optical-communications distribution business decline (Industry / Macro)
The optical-comm segment fell -7.7% YoY in FY25 and continued to fall in Q1 2026, explicitly attributed to "international environment" — i.e. US-China export controls on advanced optical and semiconductor components. This is a 19% revenue segment and will likely continue to shrink before the new self-developed OCS / OIO / photonic-wire-bonding products are large enough to replace it. Mitigant: the company is actively shifting from distribution to own-product in this segment; new-product growth at >50% can offset the legacy decline if the rate sustains.

### 9.8 Humanoid-robotics narrative monetisation gap (Industry / Market)
FZMotion is real revenue but small — likely well under 5% of revenue. Most of Luster's "humanoid-robotics" narrative premium is forward-looking. If 2026-2027 Chinese humanoid-robotics commercialisation disappoints (Unitree, UBTech, Agibot fail to commercialise at scale), the narrative-driven multiple-expansion of February 2025 onward unwinds. Mitigant: even without humanoid robotics, the broader industrial-vision-AI story remains intact.

### 9.9 Key-person risk on Yao Yi (Company-specific / Governance)
Yao Yi is simultaneously Chairman, General Manager, controlling shareholder (43%), and the primary public-facing figure. He is also 61 years old. The company has not articulated a succession plan publicly. A sudden departure — for any reason — would be a serious disruption. Mitigant: Wang Wentao and Yang Yi have ~20 years' tenure and could step into operational leadership; the technical CTOs (Jin Gang, Bao Zhenjian) are credible interim successors for the AI-research side.

### 9.10 Macro / China-stimulus dependence (Macro)
Roughly 86% of revenue is China-domestic. Chinese industrial capex is cyclical and policy-sensitive (battery subsidies, semiconductor onshoring stimulus, consumer-electronics rebates). A sharp Chinese stimulus pullback or a deflationary capex cycle would hit Luster across all four verticals simultaneously. Mitigant: the JAI overseas book takes overseas share from ~7% to ~14% of revenue and is on a high-double-digit growth path.

---

## 10. Summary Investment View

凌云光 is, in our judgement, the most strategically positioned Chinese listed machine-vision company. The combination of (a) end-to-end stack — components (post-JAI), algorithms (F.Brain / VisionWARE), and equipment — under one roof, (b) deep entrenchment in the Apple supply chain via the Foxconn relationship, (c) diversified end-market footprint across consumer electronics, new-energy, display, printing, and emerging humanoid robotics, (d) founder-led with 43% insider ownership, (e) low customer-name concentration (top-5 only 25%), and (f) a credible AI-infrastructure call-option through the OCS and photonic-wire-bonding product seeds, makes the company well-anchored on fundamentals. The principal risk is valuation: at 100×-plus TTM P/E the stock has priced in two to three years of compounding revenue growth at the FY25 +30% rate, and any quarterly disappointment (Q1 2026 +3% machine-vision-only growth is the first warning) compresses the multiple before any earnings miss. Investors should size the position acknowledging that the next 18 months are a multiple-test, not a fundamentals-test.

---

## References

1. **[2025 年年度报告 (Annual Report)](https://static.cninfo.com.cn/finalpage/2026-04-29/1225251946.PDF)** — filed with SSE on 28 April 2026. Primary source for financials, customer concentration (p. 42), product mix (p. 40), management bios (pp. 58-62), employee data (p. 68), governance discussion (pp. 53-56), share ownership (pp. 114-117), and stated risks (pp. 36-38).
2. **[2026 年第一季度报告 (Q1 2026 Report)](https://static.cninfo.com.cn/finalpage/2026-04-29/1225286215.PDF)** — filed with SSE on 28 April 2026. Primary source for Q1 2026 update, Zhipu AI fair-value gain disclosure, segment Q1 performance.
3. **[2024 年年度报告 (Prior Annual Report)](https://static.cninfo.com.cn/finalpage/2025-04-29/1223391818.PDF)** — filed with SSE on 29 April 2025. Used for FY24 baseline and FY24 segment splits.
4. **[2025 年半年度报告 (1H 2025 Report)](https://static.cninfo.com.cn/finalpage/2025-08-29/1224291822.PDF)** — filed with SSE on 28 August 2025. Used for new-energy YoY commentary.
5. **[Private placement disclosure 2025-11-20](https://static.sse.com.cn/stock/disclosure/announcement/c/202511/688400_20251120_HX3W.pdf)** — SSE filing on private-placement preparation.
6. **[Luster English website partner list](https://en.lusterinc.com/imaging/partners/)** — primary source for distributed-brand catalogue.
7. **[Luster Chinese corporate site](https://www.lusterinc.com/)** — primary source for product walk and ESG / company-history pages.
8. **[Eastmoney quote page for SSE:688400](http://quote.eastmoney.com/kcb/688400.html)** — primary source for current price, market cap, multiples.
9. **[Investing.com Luster LightTech profile](https://www.investing.com/equities/luster-lighttech)** — used for cross-checking share-count and multiple data.
10. **[Grand View Research — China Machine Vision Market](https://www.grandviewresearch.com/horizon/outlook/machine-vision-market/china)** — China TAM sizing.
11. **[Coherent Market Insights — Machine Vision System Market](https://www.coherentmarketinsights.com/industry-reports/machine-vision-system-market)** — global TAM and share rankings.
12. **[Sohu coverage of Unitree partnership](https://www.sohu.com/a/877788995_121924584)** — humanoid-robotics narrative source.
13. **[Sina Finance — Unitree clarification](https://finance.sina.com.cn/tech/roll/2025-02-21/doc-inemezhr8508090.shtml)** — relationship structure clarification.
14. **[STCN — Luster customer disclosure article](https://stcn.com/article/detail/1733603.html)** — secondary source for customer list.
15. **[JAI A/S product portfolio](https://www.jai.com/products)** — JAI camera-line reference.
