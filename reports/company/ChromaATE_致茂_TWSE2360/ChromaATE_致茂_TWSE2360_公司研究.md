# 公司研究报告：Chroma ATE 致茂电子（TWSE:2360）

**日期（as of）：2026-06-11** · 首次覆盖（initiation）· 报告语言：简体中文（技术/财务术语保留英文）

> *分析师观点：* **评级：Hold（持有）· 12 个月目标价 NT$2,450（较 2026-06-10 收盘 NT$2,210 上行 +11%）· 估值方法：48× 2027E EPS NT$50.7（forward P/E × target multiple）**
> 市值 NT$936.1bn（约 US$30bn）· 52 周区间 NT$341.5–2,795 · TWSE:2360 · 数据来源：[Yahoo Finance 2360.TW，2026-06-10](https://finance.yahoo.com/quote/2360.TW/)
>
> | 倍数 / Multiple（*分析师观点：* 前瞻列） | FY2025A | FY2026E | FY2027E |
> |---|---|---|---|
> | P/E（报告口径 EPS） | 79.8×（EPS 27.70，含一次性收益） | 57.3×（EPS 38.6E） | 43.6×（EPS 50.7E） |
> | P/E（剔除一次性收益的核心口径） | ~109×（核心 EPS ≈20.2，推导见 1A） | 同上 | 同上 |
> | P/S | 33.1×（营收 NT$28.31bn） | 17.2× | 13.2× |
> | PEG（以 FY26E EPS 增速 ~+91% 计） | — | ~0.6 | — |
>
> 相对表现（截至 2026-06-10，[Yahoo Finance / yfinance](https://finance.yahoo.com/quote/2360.TW/)）：1M **−9.4%**（TAIEX +7.0%，相对 −16.4pp）· 6M **+172.5%**（TAIEX +63.1%，相对 +109.4pp）· YTD **+177.6%**（TAIEX +52.3%）· 12M **+566.6%**（TAIEX +101.0%，相对 +465.6pp）
>
> **核心论点（thesis pillars）**——（1）致茂是 AI 算力建设中“测试侧”的稀缺标的：AI 服务器电源测试（PSU/BBU/HVDC power rack）+ GPU system-level test (SLT, 系统级测试) + advanced packaging (先进封装) 量测 + CPO (co-packaged optics, 共封装光学) 光子测试四线并进；（2）业绩动能极强——2026Q1 营收同比 +73% 创纪录、4–5 月营收同比 +129%（美元口径），Q2 跟踪超共识约 20%；（3）但 12 个月 +567% 的股价已计入大量乐观预期：TTM P/S 28×、相对 TWSE 的 P/E 溢价 2.6×（5 年均值 1.3×），且卖方目标价分歧极大（NT$1,660–2,800，价差 69%）；（4）在强基本面与高估值的拉锯下给予 Hold——等待更好的进场点，关键跟踪变量是 SLT 上修幅度与 2027 年 AI capex 的持续性。

> **Update——2026 年度展望（2026-02-25 初次给出）+ 经营动能确认：** 管理层在 2025Q4 法说会给出 2026 年定性指引：“Business will present another year of growth in 2026, both Test Instruments & ATS and Semiconductor / Photonics received a strong demand from customers”，并点名 AI server power（含 HVDC）、ESS、SLT（AI/HPC/ASIC）、advanced packaging 量测与 CPO 为增长驱动（[2025Q4 法说会简报, Slide 14, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。此后动能持续验证：5 月合并营收 NT$45.50 亿，同比 +133.1%，前 5 月累计 NT$212.75 亿、同比 +94.4%（[TechNews 科技新报, 2026-06-05](https://finance.technews.tw/2026/06/05/chroma-2360-202605-financial-report/)）。

---

## 目录

1. [公司概览](#1-公司概览)（含投资论点导语 + 估值快照）
1A. [估值与目标价](#1a-估值与目标价)（前瞻模型 · PT 推导 · 牛/基准/熊 · 卖方观点演变）
2. [公司历史](#2-公司历史)
3. [管理团队](#3-管理团队)
4. [产品与服务](#4-产品与服务)（本报告最重要章节）
5. [客户与上市策略](#5-客户与上市策略)
6. [行业概览](#6-行业概览)
7. [竞争格局](#7-竞争格局)
8. [市场机会（TAM）](#8-市场机会tam)
9. [风险评估](#9-风险评估)
9.5 [关键分歧与催化剂](#95-关键分歧与催化剂)
10. [投资风格透视](#10-投资风格透视)

---

## 1. 公司概览

*分析师观点：* 本报告对致茂电子（Chroma ATE Inc., TWSE:2360）首次覆盖给予 **Hold（持有）评级、12 个月目标价 NT$2,450（+11%）**。为什么是现在？因为致茂正处在一个罕见的多引擎共振点上：AI 数据中心把“电力”和“芯片”两条供应链同时推向测试设备——每一台 PSU (power supply unit, 电源供应器)、BBU (battery backup unit, 备援电池)、HVDC (high-voltage direct current, 高压直流) power rack 出厂前要上致茂的电源测试机，每一颗 NVIDIA/AMD/Google 的 AI 芯片封装后要过致茂的 SLT (system-level test, 系统级测试)，每一片 CoWoS 载板要经过致茂的 2D/3D 量测，2H26 起 CPO 光引擎还要新增四道测试 insertion。2026Q1 营收同比 +73% 创单季纪录、毛利率 63%（[2026Q1 法说会简报, Slide 5, 2026-04-30](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）。但 12 个月 +567% 的涨幅之后，估值已经走到了历史区间之外，卖方内部分歧巨大（详见 1A 卖方观点演变）——基本面与价格的赛跑是本篇的核心命题。

**公司是做什么的？** 致茂电子创立于 1984 年，自有品牌“Chroma”，公司在 2025Q4 法说会中自述为：“Chroma Group founded in 1984, a world leading own brand and design of high precision test & measurement instruments, automated test systems, intelligent manufacturing systems and test & automation turnkey solutions provider. Businesses cover test and measurement instruments and ATS for electronics, ICT, EV/ESS, AI and Semiconductor”（[2025Q4 法说会简报, Slide 5, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。2025 年报（FY2025）进一步定义业务范围：“CHROMA ATE INC. is a driving force behind emerging technology industries and a trusted partner of world-class customers”，主要应用市场包括 AI、semiconductors/ICs、energy storage（储能）、electric vehicles（电动车）、green energy batteries、LED、太阳能、photonics（光子学）、flat panel displays、video & color、power electronics（功率电子）、passive components（被动元件）、electrical safety（电气安规）等（[致茂 2025 Annual Report（年报英文版）, p.100](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

**怎么赚钱？** 收入结构按年报口径分两类：test equipment（测试设备）占 FY2025 合并营收 95.96%、automated equipment（自动化设备，子公司 MAS）占 3.12%、其他 0.92%（[致茂 2025 年报, p.100](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。按法说会的母公司产品口径，FY2025 母公司销售 NT$22,012mn 中 Test Instruments & ATS（测试仪器与自动测试系统，电源测试为主）占 48%（NT$10,545mn，同比 +55%）、Semiconductor / Photonics Test Solutions 占 44%（NT$9,759mn，同比 +40%）、Turnkey 2%、Service & Others 6%（[2025Q4 法说会简报, Slide 13, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。这是一门“卖精密仪器 + 高毛利”的生意：FY2025 合并 gross margin (毛利率) 61%、operating margin (经营利润率) 32%（[2025Q4 法说会简报, Slide 10](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。

**规模与地理分布。** FY2025 合并营收 NT$28,311mn（+31% YoY，历史新高）、归母净利 NT$11,692mn、EPS NT$27.70（+122%，含 3Q25 一次性资产处分收益 NT$3,185mn）；集团员工 3,802 人（2025 年末），总部研发人员占比 35%（[2025Q4 法说会简报, Slides 5/6/10, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。出口占比 82%（FY2025 出口销售 NT$23,266mn / 内销 18%），客户遍及全球（[致茂 2025 年报, p.113](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。2026Q1 单季：营收 NT$11,859mn（+73% YoY / +38% QoQ）、毛利率 63%、经营利益 NT$4,797mn（40% margin）、归母净利 NT$3,864mn、EPS NT$9.12（+81%），年化 ROE 51%（剔除一次性收益）、净现金结构（[2026Q1 法说会简报, Slides 5/6, 2026-04-30](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）。

```mermaid
xychart-beta
    title "致茂合并营收（NT$ mn）：2021–2025A + 2026E/2027E（E 为分析师预估）"
    x-axis ["2021", "2022", "2023", "2024", "2025", "2026E", "2027E"]
    y-axis "NT$ mn" 0 --> 80000
    bar [17584, 22067, 18676, 21604, 28311, 54500, 70800]
```

数据来源：2021–2025A 见 [2025Q4 法说会简报, Slide 6, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)；2026E/2027E 为*分析师观点*（推导见 1A）。

```mermaid
xychart-beta
    title "毛利率与经营利润率（%，合并口径；2026E/2027E 为分析师预估）"
    x-axis ["2023", "2024", "2025", "2026E", "2027E"]
    y-axis "%" 20 --> 70
    line [58, 59, 61, 62.5, 62]
    line [13.5, 25.4, 32.5, 38.5, 39]
```

数据来源：上线为 gross margin（2023–25 见 [2025Q4 法说会简报, Slide 6](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)），下线为 operating margin（FY2024 25.4% = 5,482/21,604、FY2025 32.5% = 9,198/28,311，见 [同简报 Slide 10](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)；FY2023 经营利润率为母公司与合并报表推算近似值，标注为约数）；2026E/2027E 为*分析师观点*。

**估值快照（TTM，2026-06-10）。** 现价 NT$2,210、市值 NT$936.1bn；TTM P/E 80.7×（trailing EPS 27.4，含一次性收益；剔除后核心 TTM P/E 约 100×+）、TTM P/S 28.1×、forward P/E 37.7×、股息率 0.88%（[Yahoo Finance 2360.TW key statistics, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)）。同业对比（同日，[Yahoo Finance](https://finance.yahoo.com/quote/2360.TW/)）：Advantest（6857.T）TTM P/E 49.3× / P/S 16.2×；Teradyne（TER）64.5× / 14.4×；Keysight（KEYS）52.3× / 9.1×；台达电（2308.TW）95.2× / 9.6×。**为什么倍数这么高？** 三个原因：（a）AI 测试设备是当前台股最强的盈利上修主线之一——*分析师观点：* UBS 在 5 月将致茂新增入台股最偏好组合，给予 Buy、目标价 NT$2,600（[UBS — Taiwan Equity Strategy, 2026-05-09, 偏好组合表](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)）；（b）盈利基数正在快速抬升（Q1 EPS 已达去年全年核心 EPS 的约 45%）；（c）*分析师观点：* Bernstein 指出致茂当前交易在 52× forward P/E、相对 TWSE 的 P/E 达 2.6×，而 5 年均值仅 1.3×、+1SD 也只有 1.7×——估值溢价是历史区间的两倍（[Bernstein — TW suppliers monthly sales, 2026-06-07, Exhibits 7–8](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。该倍数水平已构成估值压缩风险，正式列入第 9 章。

## 1A. 估值与目标价

本章全部前瞻数字（营收/利润率/EPS 预估、目标价、情景目标价）均为*分析师观点*，外部输入逐项注明来源；预估本身不附带任何财报引用。

### (a) 前瞻财务预估表（FY2025A–FY2028E）

| 指标（*分析师观点：* 预估列） | FY2025A | FY2026E | FY2027E | FY2028E | 25–28E CAGR |
|---|---|---|---|---|---|
| 营收（NT$ mn） | 28,311 | 54,500 | 70,800 | 81,400 | +42% |
| — YoY % | +31% | +93% | +30% | +15% | |
| Gross margin 毛利率 % | 61.5% | 62.5% | 62.0% | 61.5% | |
| Operating margin % | 32.5% | 38.5% | 39.0% | 39.0% | |
| 归母净利（NT$ mn） | 11,692（含一次性） | 16,370 | 21,500 | 24,700 | |
| EPS（NT$，basic） | 27.70（核心 ≈20.2） | 38.6 | 50.7 | 58.2 | +42%（vs 核心） |
| ROE %（年化、剔除一次性） | 29% | ~45% | ~40% | ~35% | |
| FCF（NT$ mn） | 6,686 | ~11,000 | ~17,000 | ~20,500 | |
| 净现金/(负债) | 净现金 | 净现金 | 净现金 | 净现金 | |

预估的外部基础：FY2025A 全部数字来自 [2025Q4 法说会简报, Slides 10/11, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)（FCF NT$6,686mn、净现金、ROE 29% 剔除一次性收益均为简报披露）；核心 EPS ≈20.2 为推导值（= (11,692 − 3,185) / 423.6mn 股，处分收益 NT$3,185mn 见 [2025Q4 法说会简报, Slide 9 注](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)，按税前金额近似）。FY2026E 营收构建：Q1 实际 NT$11,859mn（[2026Q1 法说会简报, Slide 5](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）+ Q2 取 *分析师观点：* Bernstein 基于历史季节性推算的区间中值 NT$14.9bn（“2Q26 sales should reach NT$13.8-15.6B (+115% to +141% YoY), with the NT$14.9B midpoint c.20% above cons.”，[Bernstein — TW suppliers monthly sales, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）+ 2H26 较 1H26 +8%（参照 2025 年 H2/H1 = 1.20 的季节性，见 [2025Q4 法说会简报, Slide 9/10](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)，保守取低）。利润率假设锚定 Q1 实际（GM 63% / OPM 40%，[2026Q1 法说会简报, Slide 5](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）并为下半年成本与新品爬坡留出缓冲。FY2027–28E 增速参照（i）管理层定性指引（SLT/量测/CPO/HVDC 四驱动，[2025Q4 法说会简报, Slide 14](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）与（ii）*分析师观点：* J.P. Morgan 的行业框架——致茂 SLT、metrology、datacenter power testing 三条线“each at 40%+ CAGR”（[J.P. Morgan — Asia PCB, CCL, Substrate, Testing, and Passive Components, 2026-04-10, p.19](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。

**利润率桥（FY2025 32.5% → FY2026E 38.5% OPM，+600bps，*分析师观点：*）：** 规模杠杆（营收近翻倍而 G&A/R&D 增速远低于营收，Q1 已验证：营收 +73% 而 G&A +32%、R&D +33%，[2026Q1 法说会简报, Slide 5](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）贡献约 +500bps；高毛利 SLT/量测占比提升贡献约 +100bps；新品（CPO 测试机）爬坡费用部分抵消。

### (b) 目标价推导（показать арифметику → 直接给算式）

**方法：forward P/E × target multiple。** PT = 2027E EPS NT$50.7 × 48× = **NT$2,434 ≈ NT$2,450**（较 2026-06-10 收盘 NT$2,210 上行 +11%）。

**为什么是 48×？** 对标五家可比公司（TTM P/E，2026-06-10，[Yahoo Finance](https://finance.yahoo.com/quote/2360.TW/)）：Advantest 49.3×、Teradyne 64.5×（forward 36.6×）、Keysight 52.3×（forward 27.3×）、台达电 95.2×（forward 33.9×）。致茂 FY2025–27E 核心 EPS CAGR 约 +58%（20.2→50.7），显著高于 Advantest/Teradyne 的成长曲线，支撑其 forward 倍数高于 Teradyne 的 36.6×；但 48× 低于 *分析师观点：* Morgan Stanley 的 50×（“PT of NT$2,800, based on 50x 2027e P/E vs. current valuation of 46x 2027e”，[Morgan Stanley — Investor Presentation: AI Still Taking Center Stage, 2026-06-05, p.3](http://xs-macbook-air.local:5001/zsxq/pdf/214528851488581/Morgan%20Stanley-Investor%20Presentation%EF%BC%9AAI%20Still%20Taking%20Center%20Stage-260605.pdf)），高于 *分析师观点：* Bernstein 的 38×（[Bernstein — model updates across the AI supply chain, 2026-03-16, Chroma 章节](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)）——取中偏上，反映 Q1 后盈利上修但兼顾历史相对估值已达 2 倍均值的事实。

### (c) 牛 / 基准 / 熊情景

| 情景（*分析师观点：*） | 关键假设 | 2027E EPS | 倍数 | PT | vs 现价 2,210 |
|---|---|---|---|---|---|
| 牛市 Bull | Rubin SLT 上修 + CPO 四道 insertion 全面放量 + HVDC 订单超预期 | NT$58 | 55× | NT$3,190 | **+44%** |
| 基准 Base | 中性预估；Q2 超共识兑现，2027 +30% | NT$50.7 | 48× | NT$2,450 | **+11%** |
| 熊市 Bear | 2027 AI capex 消化期 + SLT 竞争分流 + 倍数回归 | NT$42 | 35× | NT$1,470 | **−33%** |

### (d) 共识对标

*分析师观点：* 按 Bernstein 2026-06-07 的估值图（“Chroma is trading at 52x forward P/E and 42x on 2027 consensus EPS”，[Bernstein — TW suppliers monthly sales, 2026-06-07, Exhibit 7](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)），以 2026-06-05 收盘 NT$2,565 反推，市场共识 2027E EPS ≈ NT$61（= 2,565 ÷ 42，两个输入均来自该报告）。本报告 2027E EPS NT$50.7 **低于该推导共识约 17%**、高于 Bernstein 自身的 NT$43.66（[Bernstein — AI Value Chain: Vera Rubin, 2026-06-08, ticker 表](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)）、低于 Morgan Stanley 的 NT$55.57（[Morgan Stanley — AI Still Taking Center Stage, 2026-06-05, 估值表](http://xs-macbook-air.local:5001/zsxq/pdf/214528851488581/Morgan%20Stanley-Investor%20Presentation%EF%BC%9AAI%20Still%20Taking%20Center%20Stage-260605.pdf)）——即本报告的盈利假设在 Street 区间中位略偏保守。

### 卖方观点演变（Sell-side view evolution）

机械预检：`db/stock_price_target.db`（只读）现存 2360.TW 两条 PT 记录——Bernstein 2026-03-16 Outperform NT$1,660（报告日收盘 1,450，+14.5%）与 Morgan Stanley 2026-06-05 Overweight NT$2,800（报告日收盘 2,565，+9.2%）；叠加 UBS 报告内表格（Buy NT$2,600），PT 离散度：min 1,660 / 中位 2,600 / max 2,800，**极差达 69%**。

**按机构的观点时间线（报告日期以文件名 -YYMMDD 为准；报告日收盘价来自 yfinance/PT 库）：**

| 机构 | 日期 | 评级 / 目标价 | 报告日收盘 | 隐含上行 | 核心论点 / 修订 |
|---|---|---|---|---|---|
| Bernstein | 2026-03-16 | Outperform · **NT$1,660（自 970 大幅上调 +71%）** | 1,450 | +14.5% | 目标 P/E 31×→38×、2027E EPS 31.4→43.7；“AI SLT revenue to nearly triple in 2026”；触发因素：4Q25 业绩 + Vera Rubin/AMD/Google 新芯片（[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)） |
| J.P. Morgan | 2026-04-10 | 行业深度（该 PDF 未列 PT） | 行业框架 | — | SLT / metrology / DC power testing 三线 “each at 40%+ CAGR”；“Chroma is the leader in AI data center power testing”（[J.P. Morgan, 2026-04-10, pp.19–23](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)） |
| UBS | 2026-05-09 | **Buy · NT$2,600**（新增入最偏好组合） | 2,325（报告表内价格） | +11.8% | AI 盈利上修主线；价值链定位 “Advantest FT, Chroma SLT”（[UBS, 2026-05-09](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)） |
| UBS | 2026-05-12 | 月度追踪（评级/PT 不变） | 2,440 | — | “Equipment was the outperformer with Chroma and Hon Precision both 40% of consensus”——4 月单月即完成季度共识 40%（[UBS, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/212452255428221/UBS-APAC%20Technology%EF%BC%9ATaiwan%20Tech%20April%20sales%EF%BC%9A%20Supply%20chain%20momentum%20continues%20with%20Q226%20tracking%20ahead-260512.pdf)） |
| Citi | 2026-05-12 | 行业点评（无单独 PT） | — | — | 将 Chroma 列入 AI 光学领域值得关注个股（[Citi 中国科技, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/184124548444512/%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%EF%BC%9A%E4%BB%8E%E7%BE%8E%E5%9B%BD%E4%BA%91%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E5%95%86%E8%B5%84%E6%9C%AC%E6%94%AF%E5%87%BA%E5%8F%8A%E5%85%89%E5%AD%A6%E5%90%8C%E4%B8%9A%E8%AF%84%E8%AE%BA%E4%B8%AD%E5%BE%97%E5%88%B0%E7%9A%84%E5%90%AF%E7%A4%BA.pdf)） |
| Bernstein | 2026-06-04 | Outperform（Computex 后重申、列入超配） | 2,620 | −36.6%（PT 1,660 未动） | Computex 实地调研：AI 设备需求拉动；风险提示 AI 芯片需求疲软、EV 渗透放缓、行业内卷（[Bernstein, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)） |
| Morgan Stanley | 2026-06-05 | **Overweight · NT$2,800** | 2,565 | +9.2% | “PT of NT$2,800, based on 50x 2027e P/E vs. current valuation of 46x 2027e”；四驱动：GPU SLT 新周期、先进封装量测、transceiver/CPO 光子测试、FT handler 与 burn-in oven 增量（[Morgan Stanley, 2026-06-05, p.3](http://xs-macbook-air.local:5001/zsxq/pdf/214528851488581/Morgan%20Stanley-Investor%20Presentation%EF%BC%9AAI%20Still%20Taking%20Center%20Stage-260605.pdf)） |
| Bernstein | 2026-06-07/08 | Outperform · NT$1,660（**PT 已显著落后股价**） | 2,565 | **−35.3%** | Apr–May 营收 +129%、Q2 超共识 ~20%后明言 “We will revisit our model”——即自身模型待上修（[Bernstein, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)） |

**机构间分歧（不可揉合成假共识）：** 三家给 PT 的机构同为“看多”评级，但 PT 区间 NT$1,660–2,800 相差 69%——分歧不在方向而在“估值锚”：

| 机构 | 日期 | 评级 / PT | 核心论点 | 什么证据能证明其正确 |
|---|---|---|---|---|
| Bernstein | 2026-06-07 | Outperform / 1,660（38× 2027E 43.7） | 业务确定性强但估值纪律优先；自认模型待修 | 若 Q2 实际落在其 13.8–15.6B 区间且 2027 共识回落，38× 锚有效 |
| UBS | 2026-05-09 | Buy / 2,600 | 台股 AI 盈利上修周期未完，致茂是设备端最强动能 | 若 6–7 月营收继续 >100% YoY、SLT 指引上修兑现 |
| Morgan Stanley | 2026-06-05 | Overweight / 2,800（50× 2027e 55.57） | 多引擎（电源/SLT/量测/CPO/burn-in）支撑高倍数 | 若 CPO 2H26 出货 + HVDC 机柜测试放量，使 2027E EPS 接近 55–60 |

### (e) 摇摆变量（swing variables）

本案的关键压力测试点有二：**（1）SLT 预测上修的幅度与持续性**——CFO 在 Q1 法说会明言 “We are seriously considering revising up our SLT forecast”（[BigGo Finance — Q1 2026 earnings call 摘要, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)），上修兑现与否直接决定 2027E EPS 落在 NT$44 还是 NT$61；**（2）目标倍数能否守住**——当前相对 TWSE P/E 溢价 2.6×（5 年均值 1.3×，*分析师观点：* [Bernstein, 2026-06-07, Exhibit 8](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)），任何 AI capex 边际转弱都可能触发倍数而非盈利的剧烈回撤。

---

## 2. 公司历史

致茂电子 1984 年 11 月创立于台湾，创办人黄欽明（Leo Huang）以自有品牌 “Chroma” 切入精密量测仪器，1996 年 12 月 21 日在台湾证券交易所上市（股票代号 2360），现总部位于桃园市龟山区文茂路 88 号（[维基百科 — 致茂电子（访问于 2026-06-11）](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E8%8C%82%E9%9B%BB%E5%AD%90)）。公司四十年的主线是“跟着台湾电子业的每一波终端迁移卖测试”：从早期的电源供应器测试、视频与色彩测试（display 产业），到 2010 年代的 LED/太阳能/被动元件，再到 2015 年后的 EV/电池、2020 年后的半导体与 AI（[致茂 2025 年报, pp.100–109](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

```mermaid
timeline
    title 致茂电子关键里程碑
    1984 : 黄欽明创立致茂电子，自有品牌 Chroma
    1996 : 台湾证券交易所上市（TWSE：2360）
    2010s : 产品线扩展至 LED、太阳能、被动元件、EV/电池测试
    2022 : 并购美国 ESS（Environmental Stress Systems），强化半导体测试温控能力
    2023 : 品牌战略更新，愿景 Empowering future technologies for a better world
    2025 : 营收 NT$28.3bn 创历史新高；AI 服务器电源测试 + GPU SLT 双引擎确立
    2026 : 组织重整，曾一士接任 CEO；Q1 营收创单季新高（+73% YoY）
```

图表来源：[维基百科 — 致茂电子（访问于 2026-06-11）](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E8%8C%82%E9%9B%BB%E5%AD%90)、[致茂 2025 年报, p.111](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)、[DIGITIMES, 2025-12-04](https://www.digitimes.com/news/a20251204PD200/chroma-ate-ic-testing-equipment-governance.html)、[2025Q4 法说会简报, Slide 5](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)。

三次关键战略转折：**（1）从仪器到“仪器 + 自动化 + Turnkey”**——集团整合子公司 MAS（Modular Assembly System），把量测设备、自动化系统与 MES 软件打包成 turnkey solutions，主要服务电池芯化成（battery cell formation）等场景（[致茂 2025 年报, p.106](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）；**（2）2022 年并购美国 ESS（Environmental Stress Systems）**，补强半导体测试中的温度强制（temperature forcing）技术——这是今天 King Cobra 温控系统支撑高 TDP GPU 测试的能力来源之一（[维基百科 — 致茂电子（访问于 2026-06-11）](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E8%8C%82%E9%9B%BB%E5%AD%90)）；**（3）2026 年 1 月组织重整**——年报明言 “the Company underwent an organizational adjustment in January 2026...to pursue higher milestones under the leadership of the new management team”（[致茂 2025 年报, p.111](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)），创办人交棒专业经理人。

近两年发展浓缩为一句话：2023 年营收还在消化 EV/电池下行（NT$18,676mn，−13%），2024 年恢复 +16%，2025 年 AI 双引擎点火 +31% 创新高，2026 年前 5 个月直接 +94.4%（[2025Q4 法说会简报, Slide 6](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)；[TechNews, 2026-06-05](https://finance.technews.tw/2026/06/05/chroma-2360-202605-financial-report/)）。

## 3. 管理团队

**创办人兼董事长：黄欽明（Leo Huang）。** 1984 年创立致茂并领导公司四十余年，截至 2026-03-31 个人持股 10,859,897 股（2.55%），为公司第五大股东（[致茂 2026 年股东会主要股东名册](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2026_Chroma_major_shareholders-EN.pdf)）。他将公司从电源测试仪器作坊带到“全球精密量测与智能自动化方案商”，曾获《Harvard Business Review》台湾区最佳 CEO 第 15 名及 ERSO Award（[致茂官网新闻室](https://www.chromaate.com/en/newsroom/news154)；[Chroma Group — Forbes 专访 Leo Huang](https://www.chroma-group.com/newsexpress-en/driving-innovation-forbes-interviewed-chroma-chairman-and-ceo-leo-huang)）。2025 年 12 月 3 日董事会通过交棒决议：黄欽明卸任 CEO、保留董事长职务，聚焦集团治理与长期战略（[DIGITIMES, 2025-12-04](https://www.digitimes.com/news/a20251204PD200/chroma-ate-ic-testing-equipment-governance.html)）。

**现任 CEO：曾一士（I-Shih Tseng）博士，2026-01-01 起任总裁兼 CEO。** 台湾大学机械工程学士、宾州州立大学（Penn State）机械工程博士；1998 年加入致茂，深耕半导体测试设备开发近三十年，接任前职务为“president of the integrated system solutions and optical inspection systems business units”兼董事，管辖 VLSI test systems、SoC 平台、光学元件测试与 PXI/PXIe IC 测试平台，并兼任集团关联公司 ADIVIC 董事长、Testar Electronics 与 Innovative Nanotech 董事（[DIGITIMES, 2025-12-04](https://www.digitimes.com/news/a20251204PD200/chroma-ate-ic-testing-equipment-governance.html)）。由“半导体测试 BU 总裁”出任集团 CEO，本身就是公司向半导体/AI 测试倾斜的组织信号——与年报短期计划第一条“Accelerate the development of Metrology solution required for advanced semiconductor/advanced packaging processes”互为印证（[致茂 2025 年报, p.111](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。2026Q1 起法说会已由 CFO Paul Ying 与新团队主持（[2026Q1 法说会简报, Slide 1, 2026-04-30](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）。

## 4. 产品与服务

> 本章为全报告权重最高章节。致茂的产品树极宽（年报列出 19 条产品线），但 2026 年的投资故事集中在四个高速引擎：**AI 服务器电源测试、GPU SLT、先进封装量测、CPO 光子测试**。以下先给出发行人自己的产品矩阵，再逐一拆解。

### 4.1 发行人自述的产品矩阵（年报原文重排）

下表逐行转录自 [致茂 2025 年报 “Current products of the Company”, pp.100–102](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)（产品线名称保留年报英文原文）：

| 年报产品线（原文） | 代表产品（年报原文节选） | 下游应用 |
|---|---|---|
| Power electronics test solutions | DC/AC electronic load, Regenerative AC/DC load, AC power source, bidirectional DC power supply, digital power meter, SoftPanel™ | 信息/通信、电源、充电桩 |
| **Power supply & BBU test solutions for servers** | Server PSU/Rectifier testing, power shelf testing, rack power testing, **HVDC server power supply test**, BBU module/shelf testing, BMS testing | **AI 数据中心** |
| Electric vehicle test solutions | EV 部件 ATS、充电测试、battery simulator、电驱测试 | EV |
| Battery test and automation solution | 电芯化成系统、电池包/模组实验室与产线测试、BMS 测试 | EV/ESS |
| Energy storage & power conversion (ESS/PCS) | PCS 自动测试系统、battery simulator | 储能 |
| Passive component / Electrical safety | LCR meter、变压器测试、hipot tester、partial discharge tester | 被动元件/安规 |
| Video & color / FPD / LED | Video pattern generator、color analyzer、FPD tester | 显示 |
| Photonics Test Solution | **Wafer-level testing；Packaging level testing**（激光二极管/光引擎） | 3D sensing、光通信、**CPO** |
| Automatic optical inspection (AOI) | 自动光学检测系统 | 半导体/电子 |
| **Semiconductor/IC test solutions** | **SoC testing system、VLSI test system、IC test handler、Profile measurement system（量测）** | AI/HPC 芯片 |
| RF / PXI | RF 测试、PXI semiconductor/IC test system | 无线/IC |
| Smart manufacturing / Turnkey | IMS 智能制造系统、产线自动化组装与测试 | 智能工厂 |
| Molecular diagnostics | 全自动核酸纯化/qPCR 系统 | 医疗 |

```mermaid
graph TD
    A["Chroma ATE 致茂电子<br/>FY2025 母公司销售 NT$22,012mn"] --> B["Test Instruments & ATS<br/>48% 母公司销售 · +55% YoY"]
    A --> C["Semiconductor / Photonics<br/>44% 母公司销售 · +40% YoY"]
    A --> D["Turnkey Solutions 2%"]
    A --> E["Service & Others 6%"]
    B --> B1["AI 服务器电源测试<br/>PSU / Power Shelf / BBU / HVDC"]
    B --> B2["EV / ESS / 电池测试"]
    B --> B3["功率电子 / 安规 / 被动元件 / 显示"]
    C --> C1["SLT 系统级测试 + FT handler<br/>3160-H / 3200-HD / King Cobra"]
    C --> C2["先进封装量测 Metrology<br/>798X (CoWoS/WMCM) · 799X (CoPoS)"]
    C --> C3["光子学 / CPO 测试<br/>587XX · 5860X · 586XX"]
```

图表来源：分部数据见 [2025Q4 法说会简报, Slide 13, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)；产品型号见 [2025Q4 法说会简报, Slides 16–21](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)。

### 4.2 综合：四个引擎如何咬合成一条 AI 工作流

一座 AI 数据中心从芯片到电力的建设链条上，致茂出现四次：**芯片端**——GPU 封装完成后先过致茂的 FT handler/SLT（验证芯片在系统工况下的功能与热表现），其上游 CoWoS/面板级封装产线用致茂量测机控制 TSV/RDL 精度；**互连端**——2H26 起 CPO 光引擎在 wafer、die、光引擎、交换机四道工序上新增致茂光子测试 insertion；**电力端**——机柜里的每台 PSU、power shelf、BBU 与 800V HVDC power rack 出厂前要在致茂的回馈式（regenerative）电源测试系统上完成满载/瞬态/异常模拟；**储能端**——数据中心与电网侧 ESS 的电芯化成与 PCS 测试再次用到致茂的电池自动化产线。一条 “GPU→光互连→电源→储能” 的链上四次收费，是致茂区别于单一环节设备商的结构性特征（产品线与应用对应关系见 [致茂 2025 年报, pp.100–109](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)；AI 服务器电源测试应用说明见 [Chroma USA — Testing an AI Server Power System](https://www.chromausa.com/applications/ai-server-test/)）。

### 4.3 AI 服务器电源测试（ATS 分部的核心增量）

年报对该产品线的官方描述：

> “These solutions comprehensively address the specifications testing and dynamic simulation requirements for both the power supply input and output, covering server power supply PSUs, power shelves, rack power, BBU bi-directional DC/DC converters, battery modules, and motherboard low-voltage, high-current DC/DC converters.”（[致茂 2025 年报, p.104](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）

**中文释义 / Plain-language gloss:** AI 机柜的功耗已到 220kW/柜级别，电力路径是 电网→power shelf（电源柜）→PSU→板级 DC/DC→GPU，断电保护靠 BBU。每一级电源设备出厂前都要被“假装成真实负载”地拷机：致茂的 regenerative grid simulator（回馈式电网模拟器，Model 61800，105kVA）模拟电网端的电压跌落/频率扰动，bidirectional DC source（双向直流源，Model 62000D，0–2000V/0–540A）和 DC electronic load（直流电子负载，Model 63200A/63700H）模拟负载端的抽载与回馈，Model 8000 ATS 把整套流程自动化、功率覆盖到 1.8MW（[2025Q4 法说会简报, Slide 20, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)；[Chroma 8000 Server PSU/Rectifier ATS 产品页](https://www.chromaate.com/en/product/server_power_psu_rectifier_ats_8000_587)）。“回馈式（regenerative）”是关键卖点——测试中消耗的电能回收再利用，直接降低客户电费与散热负担（[致茂 2025 年报, p.108](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。BBU 测试则覆盖 cell→module→BBU→capacitor shelf (EDLC/LIC) 全层级（[2025Q4 法说会简报, Slide 21](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。战略弹性来自 NVIDIA 主导的 **800VDC 架构迁移**——Computex 2026 上 800V 高压直流机柜成为核心展品，HVDC 化意味着电源测试设备的电压等级、功率密度与单价同步上移（*分析师观点：* [Bernstein — Computex takeaways, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)；致茂 1.44MW 级 HVDC 验证方案见 [Chroma USA — HVDC AI Server Power Testing](https://www.chromausa.com/hvdc-ai-server-power-testing-chroma-dc-load-enables-1-44mw-level-verification/)）。

*分析师观点：* 竞争优势判定——**有（moat：产品广度 + 回馈式技术 + 与 ODM/电源厂的长期绑定）**。J.P. Morgan 直言 “Chroma is the leader in AI data center power testing”，并指其在 HVDC、BBU、DC converter、rack 级电源测试各品类均有完整产品（[J.P. Morgan, 2026-04-10, pp.22–23](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）；可比竞品来自 Keysight（PSU/电子负载，[Keysight 官网](https://www.keysight.com/)）与 ITECH 等，但在 AI 服务器电源 ATS 的成套方案上同业目录深度不及致茂。

### 4.4 半导体测试：SLT + FT handler + 量测（Metrology）

**SLT / FT handler。** 2025Q4 法说会产品页给出旗舰规格：Advanced Package FT Test Handler **3160-H**（“Dual-site, 3000W cooling, Small footprint, Optical Auto-Alignment”）、High Density Testing Platform **3200-HD**（“At-speed full-power test, Optical inspection, Multi-zone CDU cooling”）、温度强制系统 **King Cobra**（“-70℃~+150℃@Tc, Up to 5000W heat dissipation”）；同页引用行业估计：GPU TDP 从 Hopper 700W → Blackwell 1000–1400W → **Rubin 1800–>3000W**（[2025Q4 法说会简报, Slide 16, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。

**中文释义 / Plain-language gloss:** SLT（system-level test, 系统级测试）是把封装好的芯片放进“模拟整机”环境里跑真实工作负载——比传统 ATE 的电学测试更接近实际使用场景。AI 芯片为什么离不开 SLT？因为 chiplet + HBM 堆叠让单封装复杂度暴涨，缺陷漏出代价（一块 Rubin GPU 约 US$55k，*分析师观点：* [Bernstein — Vera Rubin, 2026-06-08, p.3](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)）远高于多花几分钟测试。而 TDP 奔向 3000W 意味着测试时要把芯片“按在”精确温度点上散掉 3–5kW 热——这正是 King Cobra 5000W 散热与 3160-H 3000W cooling 的护城河所在。CFO 在 Q1 法说会确认 “Top three AI/HPC companies—NVIDIA, AMD, Google—have adopted Chroma's SLT solutions”，且 AMD 在拉长测试时间、追加订单（[BigGo Finance — Q1 2026 earnings call 摘要, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)）。*分析师观点：* J.P. Morgan 的模型直接按 “Nvidia GPU SLT equipment (Chroma 100% share)” 假设建模——即在 NVIDIA GPU SLT 设备上致茂目前没有第二供应商（这是 JPM 估计，非公司披露；[J.P. Morgan, 2026-04-10, p.18](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。

**量测（Metrology）。** 旗舰为 2D/3D Wafer Metrology System **Model 798X**（wafer-level，对应 CoWoS & WMCM）与 **Model 799X**（panel-level，对应 CoPoS/PLP），量测对象为 “TSV、VIA、RDL、Overlay”（[2025Q4 法说会简报, Slide 17](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。**中文释义 / Plain-language gloss:** TSV（through-silicon via, 硅通孔）和 RDL（redistribution layer, 重布线层）是先进封装里芯片间的“垂直电梯井”和“水平马路”，CoWoS 产能每开一条线就要配若干台量测机做线宽/对位（overlay）抽检。*分析师观点：* Bernstein 估计在台积电与 OSAT 的 CoWoS capex 拉动下，致茂量测收入 2026 年翻倍至约 NT$3bn、2027 年达 NT$4bn（占公司营收 high-single-digit %；该拆分为 Bernstein 估计，公司未披露此口径，[Bernstein, 2026-03-16, Chroma 章节](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)）。

*分析师观点：* 竞争优势判定——SLT/FT handler **有（moat：热管理技术 + 顶级客户共同开发的切换成本）**；量测 **部分（partial）**——KLA/Onto 等在前道量测占据主导，致茂的缝隙在封装段的 2D/3D 形貌量测（竞品参照 [Onto Innovation 官网](https://ontoinnovation.com/)、[KLA 官网](https://www.kla.com/)）。

### 4.5 光子学 / CPO 测试（新增长极）

年报披露的官方表述：

> “With the rapid expansion of AI applications, data traffic in AI data centers has surged...silicon photonics and CPO technologies have flourished and are being widely adopted for AI applications. The Company has also proactively invested in related fields, and its photonics test solution will soon launch silicon photonics and CPO models.”（[致茂 2025 年报, p.109](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）

产品组合（2025Q4 法说会）：**587XX 系列** PIC Wafer Test Solution（光子集成电路晶圆测试）、**5860X 系列** External Laser Light Source（外置激光源）、**586XX 系列** Light Engine O/E Test + CPO Switch Test + Laser Reliability Test（[2025Q4 法说会简报, Slide 18, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。**中文释义 / Plain-language gloss:** CPO（co-packaged optics, 共封装光学）把光引擎直接封进交换机 ASIC 基板，测试从“插拔式光模块测一次”变成 EPIC wafer（EIC+PIC）→ PIC die → light engine（光引擎）→ CPO switch 四道 insertion，每道都要光（光功率/波长）电（S 参数）热（激光器 burn-in）联测——这恰好横跨致茂三十年积累的激光二极管测试（源自 iPhone 3D sensing 时代的 VCSEL burn-in）与温控能力。CFO 在 Q1 法说会披露商业化进度：CPO 四道 insertion 中 1–3 道（PIC、EIC、光引擎测试）已收到 purchase orders，第 4 道（optical light-in/out）也已确认 PO，并表示 “Do not underestimate our contribution from CPO”（[BigGo Finance — Q1 2026 earnings call 摘要, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)）。*分析师观点：* Bernstein 预计 CPO 测试设备 2H26 开始出货、2027 年贡献公司营收约 5%（占半导体测试设备 high-teens %），封装级 OE tester ASP 约 US$1–1.5M（[Bernstein, 2026-03-16, Chroma 章节](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)）。

*分析师观点：* 竞争优势判定——**部分→有（moat：激光测试 know-how 的复用 + 先发 PO）**；竞品动态尚在早期，Citi 把致茂与 ASMPT 等并列为 AI 光学设备关注名单（[Citi 中国科技, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/184124548444512/%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%EF%BC%9A%E4%BB%8E%E7%BE%8E%E5%9B%BD%E4%BA%91%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E5%95%86%E8%B5%84%E6%9C%AC%E6%94%AF%E5%87%BA%E5%8F%8A%E5%85%89%E5%AD%A6%E5%90%8C%E4%B8%9A%E8%AF%84%E8%AE%BA%E4%B8%AD%E5%BE%97%E5%88%B0%E7%9A%84%E5%90%AF%E7%A4%BA.pdf)）。

### 4.6 EV / 电池 / ESS 与长尾产品线（基本盘与周期缓冲）

电池测试覆盖电芯化成（formation）、>1200A 大电流电芯验证、>1500V/>1.5MW 电池包系统验证（[致茂 2025 年报, p.105](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）；turnkey 业务以电池芯产线为主，*分析师观点：* J.P. Morgan 的分部表注明该业务“used to be Chinese battery makers, now more for non-Chinese”（客户结构从中国电池厂转向非中国客户；[J.P. Morgan, 2026-04-10, p.19](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。2026 年中国 ESS（储能）项目回暖成为 ATS 之外的边际贡献——*分析师观点：* Bernstein 将 “China ESS battery projects” 列为 4–5 月营收超预期的三大动力之一（[Bernstein, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。显示/安规/被动元件等长尾产品线增速平缓，但贡献了设备业务的客户广度与服务收入基础（Service & Others 占母公司销售 6%，[2025Q4 法说会简报, Slide 13](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。

**旗舰与近 12 个月新品。** 当前业绩的三大旗舰：AI 服务器电源测试 ATS（Model 8000 平台 + 61800/62000D/63200A 仪器群）、SLT/FT handler（3160-H/3200-HD/King Cobra）、先进封装量测（798X/799X）。FY2025 年报“Major R&D outcomes”清单中的新品包括 7980 系列 2D/3D wafer metrology、61800 系列回馈式电网模拟电源、63202A 超低压直流电子负载、58635/58636 光子晶圆探针测试平台等（[致茂 2025 年报, pp.109–110](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

**延伸观看 / Further viewing**（教学辅助，非引用来源，不承载任何数字）：

- [Chroma 官方：2-in-1 双向直流源 + 回馈式负载（至 1.8MW）——AI 服务器/HVDC 电源测试设备长什么样](https://www.youtube.com/watch?v=KNxlcPxIqGM)
- [Chroma 官方（荷兰）：3160C Tri-Temp 八工位 IC 测试 handler——封装芯片如何被自动上料、控温、分 bin](https://www.youtube.com/watch?v=gSdygQOqk-w)
- [Chroma 官方：61815 回馈式电网模拟器——如何向被测电源“假装”一个会跌落、会扰动的电网](https://www.youtube.com/watch?v=voNbfGHGlsA)

## 5. 客户与上市策略

**客户集中度（合并营收口径，必须量化）。** FY2025 年报披露：**Customer A 销售额 NT$5,100,376 千元，占合并营收 18.02%**（FY2024：NT$3,585,354 千元、16.60%），与公司无关联关系，且为近两年唯一占比 ≥10% 的客户；年报对增长原因的说明只有一句——“Mainly due to the increase in demand for SLT testing equipment”（[致茂 2025 年报, p.119](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。公司未披露 Customer A 身份，也未披露前五大客户合计占比——这一“不披露”本身是披露事实。*分析师观点：* 结合 SLT 驱动的措辞与 J.P. Morgan “Nvidia GPU SLT equipment (Chroma 100% share)” 的建模假设（[J.P. Morgan, 2026-04-10, p.18](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)），市场普遍推断 Customer A 为某 AI 芯片龙头，但这是推断而非公司披露。Customer A 占比 18% 未到本报告 20% 的“重大”阈值但已逼近，列入第 9 章风险。供应商侧无单一 >10% 集中（[致茂 2025 年报, p.119](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

```mermaid
pie title FY2025 母公司销售按产品分部（分母：母公司销售 NT$22,012mn）
    "Test Instruments & ATS（48%）" : 48
    "Semiconductor / Photonics（44%）" : 44
    "Service & Others（6%）" : 6
    "Turnkey Solutions（2%）" : 2
```

图表来源：[2025Q4 法说会简报, Slide 13, 2026-02-25](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)。注意分母为母公司销售（不含海外子公司），与上文 Customer A 的合并营收分母不同，两组百分比不可直接相加。

**客户结构与终端画像。** 致茂的 SLT 客户覆盖 AI/HPC 芯片前三强——CFO 在 Q1 法说会确认 NVIDIA、AMD、Google 均已采用其 SLT 方案（[BigGo Finance, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)）；电源测试客户为服务器电源/ODM 链（PSU、power shelf、BBU 制造商），量测客户为台积电与 OSAT（*分析师观点：* “strong capex guidance from TSMC and OSATs will double Chroma's metrology sales”，[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)），电池/turnkey 客户为全球电池厂与车厂。

**上市策略（go-to-market）。** 年报的表述是“自有品牌 + 直销与海外子公司/代理并行”：“our company and its subsidiaries are actively expanding their marketing networks and strengthening operational bases in Europe and America, not only through overseas subsidiaries but also by increasing the establishment of overseas agents and distributors”，并通过新加坡子公司布局东南亚（[致茂 2025 年报, p.112](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。与 Tier-1 客户共同开发是核心打法——年报短期计划明列 “Reinforce collaboration with Tier 1 customers on testing development...break through technical bottlenecks to meet their test quality standards”（[致茂 2025 年报, p.111](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。FY2025 出口占 82%、内销 18%（[致茂 2025 年报, p.113](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

**产能。** 管理层在 Q1 法说会表示保留两栋扩产大楼，提供“sufficient capacity for three to five years of growth”（[BigGo Finance, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)）——测试设备组装为轻资产模式，产能瓶颈低于晶圆设备同业。

## 6. 行业概览

**行业定义。** 致茂处在电子测试与量测（test & measurement）行业，年报自述其上中下游关系：公司向上游采购零部件（PCB、IC、机箱等），中游完成设计组装，以自有品牌出售给下游半导体/IC、EV 与功率电子、储能与绿电电池、显示、光电/光通信五大产业（[致茂 2025 年报, p.105](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

**市场规模与增速。** 半导体测试设备（致茂半导体业务的可比口径）：SEMI 年终预测显示 2025 年全球测试设备销售额 **US$11.2bn（+48.1%）**，2026 年再增 **+12.0%**、2027 年 **+7.1%**；整体半导体设备市场 2025/2026/2027 年分别为 US$133bn/145bn/156bn，SEMI CEO 表示 “Investments to support AI demand have been stronger than anticipated since our midyear forecast”（[SEMI 年终设备预测（PR Newswire 转发）, 2025-12-16](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)）。AI 服务器电源测试无公开第三方口径，*分析师观点：* J.P. Morgan 估计 AI server power（PSU 等）TAM 以 80%+ CAGR 扩张（[J.P. Morgan, 2026-04-10, p.21](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。

**核心驱动一：测试强度（test intensity）随 AI 芯片复杂度上升。** *分析师观点：* J.P. Morgan 概括为“1) longer testing time (unit growth); 2) higher TDP (ASP growth)”——测试时间拉长带来设备台数增长，TDP 上升带来单机价值量增长（[J.P. Morgan, 2026-04-10, p.18](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。公司侧的印证：GPU TDP 路线图（Hopper 700W → Rubin 1800–>3000W）直接画进了致茂的法说会产品页（[2025Q4 法说会简报, Slide 16](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）。

**核心驱动二：AI 数据中心的“电力侧资本开支”。** *分析师观点：* Bernstein 测算一个 1GW Vera Rubin 数据中心总 capex 约 **US$47bn**（机柜硬件 US$32bn + 外部基础设施 US$15bn），单机柜成本约 US$9.1M、功耗 220kW（[Bernstein — Vera Rubin, 2026-06-08, pp.1–3](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)）。电源、散热在每个机柜里各占约 US$15 万成本，电力设备的量价齐升直接转化为电源测试设备需求——这是致茂 ATS 分部 2026Q1 同比 +145% 的行业背景（分部数据见 [2026Q1 法说会简报, Slide 8](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）。

**核心驱动三：技术架构迁移创造新测试品类。** 800VDC 电源架构（2026 下半年起放量）、CPO 光互连（2H26 出货、2027–28 放量）、面板级封装 CoPoS 都不是存量替代而是新增 insertion——*分析师观点：* Bernstein 在 Computex 调研中确认 800V 机柜为本届展会核心产品、台达等已落地适配 NVIDIA 标准（[Bernstein — Computex takeaways, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)）。

**行业结构。** 测试设备业“小批量、多品种”的特性（年报：“Instrument products are typically produced in small amounts and wide varieties, making mass production difficult”，[致茂 2025 年报, p.113](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）决定了行业高度碎片化、按细分品类各有寡头：大型 SoC/存储 ATE 由 Advantest/Teradyne 双寡头把持，通用仪器由 Keysight 主导，而致茂在 AI 电源测试 ATS、SLT handler、封装段量测等利基（niche）品类建立份额。规制环境的主要变量是出口管制——测试设备目前不在美国对华半导体管制的核心清单内，但地缘供应链再平衡影响客户的扩产地点选择（年报风险表述见 [致茂 2025 年报, p.113](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。

## 7. 竞争格局

年报对竞争的官方表述是品类逻辑而非对手名单：

> “As the Company and its subsidiaries have been developing the instruments and automation industry for many years, there are high barriers to entry in terms of product technology, and each product technology can maintain its leading position. However...it shall continue to expand its product base and technical product capability, collaborate with tier-one manufacturers...and invest in companies with unique testing technology.”（[致茂 2025 年报, p.109](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）

公司年报未点名竞争对手。以下对标名单为*分析师观点*（基于 J.P. Morgan 测试设备同业估值表的可比集合：Chroma ATE、Advantest、Teradyne、Keysight、Delta Elec，[J.P. Morgan, 2026-04-10, p.26](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）：

| 竞争者 | 主战场 | 与致茂的交叉 | 关键事实 |
|---|---|---|---|
| Advantest（6857.T） | SoC/存储 ATE 双寡头之一 | FT 段相邻：*分析师观点：* UBS 价值链图将 AI 测试平台标注为 “Advantest FT, Chroma SLT”——前道 FT 归 Advantest、SLT 归致茂（[UBS, 2026-05-09](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)） | TTM P/E 49.3×（[Yahoo Finance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)） |
| Teradyne（TER） | SoC ATE 双寡头之二、机器人 | 若进入 AI SLT 将正面竞争 | TTM P/E 64.5×、forward 36.6×（[Yahoo Finance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)） |
| Keysight（KEYS） | 通用电子量测仪器 | 电源测试仪器、光通信测试交叉 | TTM P/E 52.3×（[Yahoo Finance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)） |
| 台达电（2308.TW） | 电源/散热产品商（同时是致茂电源测试的潜在客户群） | 同处 AI 电源生态、非直接测试竞品 | *分析师观点：* Bernstein AI 供应链首选（[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)） |
| ITECH / NH Research（NI 旗下）等 | 电源测试仪器 | 直流电源/电子负载单机交叉 | 在成套 AI 服务器电源 ATS 上目录深度有限（*分析师观点*） |
| 鸿劲精密 Hon Precision（7769.TW） | 测试 socket/插拔件 | CPO insert test 等相邻环节、非设备直接竞品 | 与致茂同被 UBS 列为 4 月动能最强设备类公司（[UBS, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/212452255428221/UBS-APAC%20Technology%EF%BC%9ATaiwan%20Tech%20April%20sales%EF%BC%9A%20Supply%20chain%20momentum%20continues%20with%20Q226%20tracking%20ahead-260512.pdf)） |

```mermaid
xychart-beta
    title "同业 TTM P/E 对比（2026-06-10，Yahoo Finance）"
    x-axis ["Chroma 2360", "Advantest", "Teradyne", "Keysight", "Delta 2308"]
    y-axis "TTM P/E (x)" 0 --> 100
    bar [80.7, 49.3, 64.5, 52.3, 95.2]
```

图表来源：[Yahoo Finance（各公司 key statistics 页，2026-06-10）](https://finance.yahoo.com/quote/2360.TW/)。注：致茂 TTM EPS 含一次性资产处分收益，剔除后核心 TTM P/E 更高（约 100×+，推导见 1A）。

**致茂的竞争优势**（*分析师观点*，证据见第 4 章）：（1）**热-电-光-自动化的跨域整合**——年报称公司维持 “leading key technologies and highly integrated capabilities in the optical, mechanical, electronic, temperature control and software fields”（[致茂 2025 年报, p.100](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)），SLT 的本质壁垒正是 3000W+ 散热下的精确温控；（2）**与前三大 AI 芯片客户的共同开发关系**（NVIDIA/AMD/Google 均采用其 SLT，[BigGo Finance, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)）形成切换成本；（3）**产品组合多元**平滑单一品类周期（Bernstein：“Chroma's diversified portfolio should help smooth quarterly swings”，[Bernstein, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。**脆弱点：** SLT 若被 ATE 双寡头（Advantest/Teradyne）以“FT+SLT 一体化”方案侵蚀，或大客户自建测试方案，高份额假设将受冲击——Bernstein 把 “Increasing competition in the AI chip SLT market” 列为目标价三大下行风险之一（[Bernstein, 2026-06-07, 风险节](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。

## 8. 市场机会（TAM）

**SAM 第一层：半导体测试设备。** SEMI 口径 2025 年 US$11.2bn（+48.1%）、2026E +12.0% ≈ US$12.5bn（推导：11.2 × 1.12）、2027E +7.1% ≈ US$13.4bn（[SEMI 年终预测（PR Newswire）, 2025-12-16](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)）。致茂的半导体/光子分部 FY2025 营收 NT$9,759mn ≈ US$0.31bn（[2025Q4 法说会简报, Slide 13](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)），即在全球测试设备盘子中份额尚低、渗透空间大——致茂主攻的 SLT/handler/量测属于该口径中增速最快的子集（*分析师观点：* J.P. Morgan 三线 40%+ CAGR 框架，[J.P. Morgan, 2026-04-10, p.19](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。

```mermaid
xychart-beta
    title "SEMI：全球半导体设备 vs 测试设备销售额（US$ bn）"
    x-axis ["2025", "2026E", "2027E"]
    y-axis "US$ bn" 0 --> 170
    bar [133, 145, 156]
    bar [11.2, 12.5, 13.4]
```

图表来源：[SEMI 年终设备预测（PR Newswire 转发）, 2025-12-16](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)；测试设备 2026E/2027E 为以 SEMI 增速（+12.0%/+7.1%）对 2025 基数的推导值。大柱为设备总额、小柱为测试设备子项，同轴同单位。

**SAM 第二层：AI 数据中心电力测试。** 该利基无公开第三方 TAM 口径——*分析师观点：* J.P. Morgan 估计 AI server power TAM 以 80%+ CAGR 扩张、且每代机柜电源价值量上升（[J.P. Morgan, 2026-04-10, p.21](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）。以 Bernstein 的 1GW = US$47bn capex 测算为锚（[Bernstein — Vera Rubin, 2026-06-08](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)），电源链（PSU/shelf/BBU/HVDC）每 GW 的设备验证与产线测试需求是结构性新增市场，致茂 ATS 分部 FY2025 NT$10,545mn（+55%）→ 2026Q1 单季 NT$5,390mn（+145% YoY）的曲线即其映射（[2026Q1 法说会简报, Slide 8](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)）。

**SOM 与渗透路径。** 公司策略是“跟着 insertion 数走”：SLT（已渗透前三大 AI 芯片客户）→ 量测（跟 CoWoS/CoPoS 扩产）→ CPO 四道 insertion（2H26 出货起步）→ HVDC 机柜级测试（800VDC 迁移）。每个新 insertion 都把 SOM 向 SAM 推进一格；*分析师观点：* Bernstein 模型下 2027 年 CPO 一项即可贡献公司营收 ~5%（[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)）。需要诚实标注的边界：以上 TAM 链条高度依赖 AI capex 的持续性——SEMI 的 2027 年测试设备增速已放缓至 +7.1%（[SEMI（PR Newswire）, 2025-12-16](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)），第二层利基的 80%+ CAGR 是卖方估计而非已实现事实。

## 9. 风险评估

**公司特定风险（4 项）**

1. **客户集中度（中-高）。** Customer A 占 FY2025 合并营收 18.02%（FY2024 16.60%），增长动力为 SLT 设备需求（[致茂 2025 年报, p.119](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。趋势上行且品类单一（SLT），若该客户测试策略转向（自研/第二供应商/减少 SLT 覆盖率），冲击集中。缓解：NVIDIA/AMD/Google 三家均已导入 SLT（[BigGo Finance, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)），客户基础在扩宽。

2. **SLT 竞争加剧（中）。** *分析师观点：* Bernstein 将 “Increasing competition in the AI chip SLT market” 列为 PT 下行风险（[Bernstein, 2026-06-07, 风险节](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）；J.P. Morgan 当前按 NVIDIA GPU SLT 100% 份额建模（[J.P. Morgan, 2026-04-10, p.18](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)）——份额只可能向下。缓解：热管理 know-how 与共同开发粘性。

3. **管理交接执行（低-中）。** 创办人黄欽明 2026-01-01 交棒 CEO 曾一士并启动组织重整（[DIGITIMES, 2025-12-04](https://www.digitimes.com/news/a20251204PD200/chroma-ate-ic-testing-equipment-governance.html)；[致茂 2025 年报, p.111](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）。四十年创办人时代结束后的战略与文化连续性待验证。缓解：曾一士 1998 年起在司 28 年、出身核心增长业务。

4. **设备订单的颠簸性（lumpiness）（中）。** Bernstein 提示 “equipment companies' sales tend to be lumpy”（[Bernstein, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）；5 月营收已现环比 −6.5%（[TechNews, 2026-06-05](https://finance.technews.tw/2026/06/05/chroma-2360-202605-financial-report/)）。月度数据的高波动会被高估值放大为股价波动。

**行业/市场风险（3 项）**

5. **AI capex 周期回落（高影响）。** 致茂 2026 年增量几乎全部来自 AI（电源/SLT/量测/CPO）。*分析师观点：* Bernstein 把 “Lower-than-expected demand for AI chips from hyperscalers, AI startups and enterprises” 列为第一下行风险（[Bernstein, 2026-06-07, 风险节](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。SEMI 2027 测试设备增速已降档至 +7.1%（[SEMI（PR Newswire）, 2025-12-16](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)）。

6. **技术路线不确定性（中）。** CPO 量产节奏屡有推迟先例——*分析师观点：* Bernstein Computex 调研指 NVIDIA 现阶段主推铜缆、CPO 主要规划在远距互连与后代平台（[Bernstein — Computex, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)）；若 CPO/HVDC 迁移推迟，新品类收入贡献顺延。

7. **EV/电池终端疲弱（中）。** 海外子公司/turnkey 业务挂钩中国电池与 EV capex，2023–24 已经历一轮下行（*分析师观点：* [Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)）；Bernstein 亦把 “Slower-than-expected EV penetration pace” 列入风险（[Bernstein, 2026-06-07](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。

**财务风险（2 项）**

8. **估值/倍数压缩（本案最大单一风险）。** TTM P/S 28.1×、TTM P/E 80.7×（[Yahoo Finance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)）；*分析师观点：* 相对 TWSE P/E 2.6× vs 5 年均值 1.3×（[Bernstein, 2026-06-07, Exhibit 8](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。触发因素：增长减速信号、AI 板块轮动、利率上行、指引不及预期。1M −9.4%（同期 TAIEX +7.0%）显示动能已在松动（[Yahoo Finance/yfinance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)）。

9. **汇率（中）。** 出口占 82%（[致茂 2025 年报, p.113](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)），美元计价收入为主，新台币升值直接压缩毛利与换算后营收（Bernstein 月度营收同比口径即特别注明 “in US$ terms”，[Bernstein, 2026-06-07](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）。

**宏观风险（1 项）**

10. **地缘政治与贸易政策（中）。** 年报指出 2025 年环境受 “persistent geopolitical and trade policy uncertainties” 与美中科技竞争影响（[致茂 2025 年报, p.103](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)）；台海风险、关税与客户供应链迁移都会改变设备采购时点与地点。

## 9.5 关键分歧与催化剂

**分歧一——“Bernstein 的 PT 比现价低 35%，是不是聪明钱在说估值到头了？”** *分析师观点：* 不尽然。Bernstein 的 NT$1,660 建立在 3 月模型（2027E EPS 43.7）上，其 6 月 7 日报告在确认 Q2 超共识 20% 后已明言 “We will revisit our model”（[Bernstein, 2026-06-07, p.1](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)）——这是“估计滞后”而非“看空转向”，其评级始终是 Outperform。但该分歧的另一面同样真实：股价对盈利上修的抢跑幅度（12M +567%，[yfinance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)）远大于任何一家的 PT 调整速度。

**分歧二——“AI 测试设备会不会在 2027 被 capex 消化期反噬？”** *分析师观点：* 测试强度的结构性上升提供部分对冲——TDP 与测试时长把“每颗芯片的测试设备需求”推高（J.P. Morgan：unit growth + ASP growth 双轮，[J.P. Morgan, 2026-04-10, p.18](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)），且 CPO/HVDC 是 2027–28 才放量的新 insertion。但若 hyperscaler capex 绝对额转负，没有结构故事能完全免疫——这正是熊市情景 PT NT$1,470 的世界。

**分歧三——“SLT 100% 份额可持续吗？”** *分析师观点：* 不应按可持续建模（本报告 2027–28E 已隐含份额自然稀释）。护城河在热管理与共同开发粘性，但 Advantest/Teradyne 的体量优势真实存在；跟踪信号是 AMD/Google 下一代芯片的 SLT 订单归属与任何“FT+SLT 捆绑”方案的出现（FT/SLT 分工现状见 UBS 价值链标注 “Advantest FT, Chroma SLT”，[UBS, 2026-05-09](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)）。

**催化剂日历（未来 12 个月，建议配合 catalyst-calendar 技能持续跟踪）：**

| 时间（约） | 事件 | 对论点的意义 |
|---|---|---|
| 每月 10 日前 | TWSE 月营收公告 | 验证 Q2 落点 vs Bernstein 区间 NT$13.8–15.6bn（超出区间上沿 = 牛市情景开启） |
| 2026-07 末 | 2026Q2 法说会 | **SLT 全年预测是否正式上修**（CFO 已预告“seriously considering”，[BigGo, 2026-04-30](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)） |
| 2H26 | CPO 测试机首批出货 | 第四引擎从 PO 变收入（[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)） |
| 4Q26 起 | Vera Rubin 机柜量产 + 800VDC 电源架构导入 | ATS 与 SLT 双引擎的 2027 订单可见度（[Bernstein — Computex, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)） |
| 2027-02 | FY2026 全年业绩 + 2027 展望 | 2027E EPS 共识（~NT$61 推导值）兑现度检验 |
| 不定期 | 台积电 CoWoS/CoPoS capex 指引 | 量测业务翻倍假设的外部锚（[Bernstein, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)） |

## 10. 投资风格透视

**周期快照**（来源：indicators.db 本地快照（FRED BAMLH0A0HYM2 / BAMLC0A0CM / ^TNX + yfinance），as of 2026-06-05，HY/IG OAS as of 2026-06-04）：VIX 21.51；10Y 美债 4.536%；HY OAS 274bp；IG OAS 74bp。信用利差处于历史紧端（HY <300bp 通常对应风险偏好亢奋），VIX 居中偏高，无风险利率处于 5 年区间上沿——对高倍数成长股是“盈利必须兑现”的环境。

**10.1 Buffett 记分卡。** *视角观点:* **Watchlist（观察名单，60/100）。**

| 维度（25 分制） | 得分 | 依据（均引自前文） |
|---|---|---|
| 业务可理解性/可预测性 | 15 | 设备业周期性强（2023 年营收 −13%），但测试是芯片/电源出厂的强制环节 |
| 护城河 | 19 | GM 61%+、剔除一次性 ROE 29%（[2025Q4 简报 Slide 11](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)）、热管理与客户共同开发粘性 |
| 管理层 | 21 | 创办人执掌 40 年、派息率 70%、净现金、无频繁摊薄（[2025Q4 简报 Slide 7](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)） |
| 估值 | 5 | FCF yield ≈0.7%（FY25 FCF 6,686 / 市值 936,136）远低于 10Y 4.54%+200bp 门槛 |

证据链：质量分高（管理 + 护城河合计 40/50）而估值分接近归零——典型“好公司、贵价格”。失效模式：若 2026E FCF 随盈利翻倍至 NT$11bn+，FCF yield 升至 ~1.2%，估值分仍不及格——该 lens 对超高速成长期公司系统性偏严。

**10.2 Munger 记分卡。** *视角观点:* **中性（5.9/10）。** 加权：护城河 7.5×35% + 管理 8×25% + 可预测性 4×25% + 估值 2×15% = **5.93**。倒置检验（inversion，强制）：最可能摧毁论点的单一情景是——**大客户在下一代平台把 SLT 改为内部方案或双供应商，同时撞上 2027 年 AI capex 消化期**：收入端（SLT 近三倍增长假设）与估值端（2.6× 相对溢价）同时崩塌，对应熊市情景 −33% 甚至更深。失效模式：高质量分依赖卖方对份额的估计（JPM 100% share），非公司披露。

**10.3 Damodaran 记分卡。** *视角观点:* **看空（价格显著超出故事支撑值；MoS ≈ −60%～−70%）。**

```
营收 CAGR（5 年 → 终值）：~25% → 4.5%（封顶于 Rf）
终值 operating margin：30%（当前 39% 高点回归常态化）
再投资率：~27%（= 终值增速 8% ÷ ROIC 30%，过渡期）
WACC：11.0%（= Rf 4.536%（indicators.db，as of 2026-06-05）+ β 1.3 × ERP 5.0%）
终值增长率：3.5%（≤ Rf）
内在价值区间：NT$250–400bn
市值（2026-06-10）：NT$936bn
安全边际（MoS）：约 −57% ～ −73%
```

证据链：即便给足 5 年 25% 营收 CAGR 与 30% 终值利润率，DCF 也只能解释当前市值的三到四成——市场定价隐含的是“AI 测试强度十年不衰 + 份额不稀释”的故事。与本报告 12 个月 Hold/PT 2,450 的张力需要明示：**PT 是市场倍数锚定的 12 个月交易性目标，DCF 是长久期内在价值——两者的差值就是市场当前支付的“动能溢价”。**失效模式：若 CPO/HVDC 把可持续增速平台抬到远超本假设的水平，内在价值区间会系统性上移。

**10.4 Howard Marks 周期姿态。** *视角观点:* **防守（Defense，约 62/100）。** 分项：HY OAS 274bp → 高亢奋（~75）；IG OAS 74bp → 同向（~75）；VIX 21.5 → 中性（~45）；10Y 处 5 年区间上沿（~60）；台股情绪——TAIEX 12 个月 +101%（[yfinance, 2026-06-10](https://finance.yahoo.com/quote/2360.TW/)）→ 偏热（~65）。反向证据（强制）：VIX 21.5 并未到自满区（<13），说明期权市场仍在付费对冲——与信用利差的极度乐观互相矛盾，姿态打分按“混合偏防守”而非“硬防守”。该姿态压低 10.1–10.3 中任何看多倾向的可执行性，与本报告 Hold 评级一致。失效模式：把姿态当择时——它是仓位风格标签，不是时点信号。

---

## Data Used / 数据来源清单

**Primary filings（一手文件）**
- 致茂 2025 Annual Report 年报英文版（2026 年股东会版本，147 页）。Source: [chromaate.com investor 频道](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)。
- 2026 年股东会主要股东名册（截至 2026-03-31）。Source: [chromaate.com](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2026_Chroma_major_shareholders-EN.pdf)。
- 台湾发行人，无 SEC 文件（Step 0.5 sec-report-summary 不适用）。

**Investor-relations materials（IR 材料）**
- 2026Q1 法说会简报（2026-04-30，9 页）：[20260430_Q1_quarterly_reports_presentation_en.pdf](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)。
- 2025Q4 法说会简报（2026-02-25，22 页，含公司简介/产品/2026 展望）：[20260225_Q4_quarterly_reports_presentation_en.pdf](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)。
- Q1 2026 法说会问答摘要（BigGo Finance, 2026-04-30）。公司无公开 investor day 资料（缺口见下）。

**Market data（市场数据，均取自 2026-06-10）**
- 致茂及同业（Advantest/Teradyne/Keysight/Delta/Hon Precision）价格、市值、P/E、P/S：Yahoo Finance / yfinance。
- 相对表现基准：TAIEX（^TWII，yfinance）。
- 报告日收盘价核对（2026-03-16/05-08/06-04/06-05/06-10）：yfinance 历史收盘。

**Third-party research（第三方研究）**
- SEMI 年终半导体设备预测（2025-12-16，PR Newswire 转发）。

**Institute research（本地 `db/zsxq.db`，均标注 *分析师观点：*）**
- 检索别名 3 个（"2360" / "Chroma" / "致茂"），命中 27 行（去重后约 20 份），未触发 downloader 补抓；引用 9 份（2026-03-16 至 2026-06-08）：
- [`814528815844812` — Bernstein：AI Value Chain — Vera Rubin 1GW 成本解析, 2026-06-08](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)
- [`814528815844822` — Bernstein：TW suppliers monthly sales（Largan & Chroma）, 2026-06-07](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)
- [`214528851488581` — Morgan Stanley：AI Still Taking Center Stage（亚太投资人简报）, 2026-06-05](http://xs-macbook-air.local:5001/zsxq/pdf/214528851488581/Morgan%20Stanley-Investor%20Presentation%EF%BC%9AAI%20Still%20Taking%20Center%20Stage-260605.pdf)
- [`415288418481128` — Bernstein：2026 台北 Computex 调研要点, 2026-06-04](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)
- [`212452255428221` — UBS：Taiwan Tech April sales, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/212452255428221/UBS-APAC%20Technology%EF%BC%9ATaiwan%20Tech%20April%20sales%EF%BC%9A%20Supply%20chain%20momentum%20continues%20with%20Q226%20tracking%20ahead-260512.pdf)
- [`184124548444512` — Citi：中国科技——美国云厂商 capex 与光学同业启示, 2026-05-12](http://xs-macbook-air.local:5001/zsxq/pdf/184124548444512/%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%EF%BC%9A%E4%BB%8E%E7%BE%8E%E5%9B%BD%E4%BA%91%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E5%95%86%E8%B5%84%E6%9C%AC%E6%94%AF%E5%87%BA%E5%8F%8A%E5%85%89%E5%AD%A6%E5%90%8C%E4%B8%9A%E8%AF%84%E8%AE%BA%E4%B8%AD%E5%BE%97%E5%88%B0%E7%9A%84%E5%90%AF%E7%A4%BA.pdf)
- [`812458124211512` — UBS：Taiwan Equity Strategy, 2026-05-09](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)
- [`585548152542554` — J.P. Morgan：Asia PCB/CCL/Substrate/Testing/Passives 行业全景, 2026-04-10](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)
- [`212222825221841` — Bernstein：AI 供应链模型更新（Delta 首选）, 2026-03-16](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)

**Macro / cycle inputs（仅用于第 10 章）**
- VIX 21.51、10Y 4.536%（as of 2026-06-05）；HY OAS 274bp、IG OAS 74bp（as of 2026-06-04）。Source: indicators.db 本地快照（FRED + yfinance）。

**Stale notices / coverage gaps（缺口与陈旧提示）**
- 公司无公开 investor day deck；IR 材料以季度法说会简报为主，本报告以 Q1-26 + Q4-25 两份简报覆盖（合计引用 15+ 次）。
- Customer A 身份未披露；前五大客户合计占比未披露（台湾年报仅强制披露 ≥10% 客户）。
- 2027E 共识 EPS（~NT$61）为自 Bernstein 估值图反推的派生值，非数据库直读。
- CommonWealth Magazine 英文版报道（2025-11-24）与 SEMI 官网原始新闻稿因反爬虫 403 未能直接核读，SEMI 数据改以 PR Newswire 官方转发稿核实；不影响正文任何数字。
- FY2023 经营利润率为推算近似值（合并报表口径），图中已标注。

---

## 参考资料

**公司官方（均访问于 2026-06-11）**

- [致茂 2025 Annual Report（年报英文版，2026 股东会）](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2025_Chroma_ATE_Annual_Report-EN.pdf)
- [2026Q1 法说会简报（2026-04-30）](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2026/20260430_Q1_quarterly_reports_presentation_en.pdf)
- [2025Q4 法说会简报（2026-02-25）](https://www.chromaate.com/downloads/investors/pdf/quarterly_reports/2025/20260225_Q4_quarterly_reports_presentation_en.pdf)
- [2026 年股东会主要股东名册（截至 2026-03-31）](https://www.chromaate.com/downloads/investors/pdf/shareholder/2026/2026_Chroma_major_shareholders-EN.pdf)
- [About Chroma（公司官网）](https://www.chromaate.com/en/chroma/aboutchroma)
- [投资人专区——季度业绩页](https://www.chromaate.com/en/investors/quarterly_results)
- [投资人专区——股东专区页](https://www.chromaate.com/en/investors/stock/shareholder)
- [Chroma 8000 Server PSU/Rectifier ATS 产品页](https://www.chromaate.com/en/product/server_power_psu_rectifier_ats_8000_587)
- [Cobra Temperature Forcing System 产品页](https://www.chromaate.com/en/product/cobra_temperature_forcing_system_31000R_331)
- [Chroma USA — Testing an AI Server Power System（应用页）](https://www.chromausa.com/applications/ai-server-test/)
- [Chroma USA — HVDC AI Server Power Testing：1.44MW 级验证](https://www.chromausa.com/hvdc-ai-server-power-testing-chroma-dc-load-enables-1-44mw-level-verification/)
- [致茂官网新闻室 — Leo Huang 获 ERSO Award](https://www.chromaate.com/en/newsroom/news154)
- [Chroma Group — Forbes 专访董事长 Leo Huang](https://www.chroma-group.com/newsexpress-en/driving-innovation-forbes-interviewed-chroma-chairman-and-ceo-leo-huang)

**本地机构研究（zsxq，按发布日期倒序；均为 *分析师观点：* 类引用）**

- 2026-06-08 · [Bernstein — AI Value Chain：Vera Rubin 1GW 数据中心成本解析](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844812/Bernstein-AI%20Value%20Chain%EF%BC%9AHow%20much%20does%20a%20GW%20of%20Vera%20Rubin%20data%20center%20capacity%20actually%20cost%EF%BC%9F-260608.pdf)
- 2026-06-07 · [Bernstein — TW suppliers monthly sales：Largan & Chroma 大超共识](http://xs-macbook-air.local:5001/zsxq/pdf/814528815844822/Bernstein-Asia%20Tech%20Hardware%EF%BC%9ATW%20suppliers%20monthly%20sales%EF%BC%9A%20Largan%20and%20Chroma%20monthly%20sales%20tracking%20well%20above%20consensus-260607.pdf)
- 2026-06-05 · [Morgan Stanley — Investor Presentation：AI Still Taking Center Stage](http://xs-macbook-air.local:5001/zsxq/pdf/214528851488581/Morgan%20Stanley-Investor%20Presentation%EF%BC%9AAI%20Still%20Taking%20Center%20Stage-260605.pdf)
- 2026-06-04 · [Bernstein — 2026 台北 Computex 调研要点](http://xs-macbook-air.local:5001/zsxq/pdf/415288418481128/Bernstein-Asia%20Tech%20Hardware%20%26%20Semi%EF%BC%9A%20key%20takeaways%20from%20the%202026%20Taipei%20Computex-260604.pdf)
- 2026-05-12 · [UBS — Taiwan Tech April sales：供应链动能延续](http://xs-macbook-air.local:5001/zsxq/pdf/212452255428221/UBS-APAC%20Technology%EF%BC%9ATaiwan%20Tech%20April%20sales%EF%BC%9A%20Supply%20chain%20momentum%20continues%20with%20Q226%20tracking%20ahead-260512.pdf)
- 2026-05-12 · [Citi — 中国科技：美国云厂商 capex 与光学同业启示](http://xs-macbook-air.local:5001/zsxq/pdf/184124548444512/%E4%B8%AD%E5%9B%BD%E7%A7%91%E6%8A%80%EF%BC%9A%E4%BB%8E%E7%BE%8E%E5%9B%BD%E4%BA%91%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E5%95%86%E8%B5%84%E6%9C%AC%E6%94%AF%E5%87%BA%E5%8F%8A%E5%85%89%E5%AD%A6%E5%90%8C%E4%B8%9A%E8%AF%84%E8%AE%BA%E4%B8%AD%E5%BE%97%E5%88%B0%E7%9A%84%E5%90%AF%E7%A4%BA.pdf)
- 2026-05-09 · [UBS — Taiwan Equity Strategy：AI 盈利上修支撑上行](http://xs-macbook-air.local:5001/zsxq/pdf/812458124211512/UBS-Taiwan%20Equity%20Strategy%EF%BC%9AAI~driven%20earnings%20upgrades%20support%20further%20upside%20amid%20rising%20volatility-260509.pdf)
- 2026-04-10 · [J.P. Morgan — Asia PCB/CCL/Substrate/Testing/Passives 行业全景](http://xs-macbook-air.local:5001/zsxq/pdf/585548152542554/J.P.%20Morgan-Asia%20PCB%EF%BC%8C%20CCL%EF%BC%8C%20Substrate%EF%BC%8C%20Testing%EF%BC%8C%20and%20Passive%20Components-260410.pdf)
- 2026-03-16 · [Bernstein — Asia Tech Hardware：AI 供应链模型更新](http://xs-macbook-air.local:5001/zsxq/pdf/212222825221841/Bernstein-Asia%20Tech%20Hardware%EF%BC%9AAsia%20Tech%20Hardware%EF%BC%9A%20model%20updates%20across%20the%20AI%20supply%20chain%EF%BC%9B%20Delta%20remains%20our%20top%20pick-260316.pdf)

**市场数据（均访问于 2026-06-11，数据截至 2026-06-10）**

- [Yahoo Finance — Chroma ATE 2360.TW](https://finance.yahoo.com/quote/2360.TW/)

**行业研究 / 新闻（按发布日期倒序）**

- 2026-06-05 · [TechNews 科技新报 — 致茂 5 月营收月减 6.5%](https://finance.technews.tw/2026/06/05/chroma-2360-202605-financial-report/)
- 2026-04-30 · [BigGo Finance — 致茂 2026Q1 法说会：营收 NT$11.8B 创纪录、EPS 9.12、SLT 预测拟上修](https://finance.biggo.com/news/TW_2360.TW_2026-04-30)
- 2025-12-16 · [SEMI 年终半导体设备预测（PR Newswire）— 2027 年 US$156bn 创纪录](https://www.prnewswire.com/news-releases/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-in-2027-semi-reports-302640433.html)
- 2025-12-04 · [DIGITIMES — Chroma appoints I-Shih Tseng as new CEO](https://www.digitimes.com/news/a20251204PD200/chroma-ate-ic-testing-equipment-governance.html)

**百科 / 词条（访问于 2026-06-11）**

- [维基百科（中文）— 致茂电子](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E8%8C%82%E9%9B%BB%E5%AD%90)

**延伸观看（教学辅助，非引用来源）**

- [Chroma 官方 — 2-in-1 双向直流源 + 回馈式负载（至 1.8MW）](https://www.youtube.com/watch?v=KNxlcPxIqGM)
- [Chroma 官方（荷兰）— 3160C Tri-Temp 八工位 IC 测试 handler](https://www.youtube.com/watch?v=gSdygQOqk-w)
- [Chroma 官方 — 61815 回馈式电网模拟器](https://www.youtube.com/watch?v=voNbfGHGlsA)

---

<details>
<summary>Verification log (Step 10) — 2026-06-11</summary>

**URL check** — 报告内全部 28 个外部 URL 于 2026-06-11 经 curl（真实浏览器 UA）逐一检查：26 个返回 200/301/302；`zh.wikipedia.org` 与 `chroma-group.com` 对脚本 UA 返回 2xx；`crunchbase.com` 类反爬来源未引用。SEMI 官网原稿 403（Cloudflare），已改引 PR Newswire 官方转发稿（200）。详见下方残留项。

**Step 0.5 sec-report-summary** — n/a（台湾发行人，非美股；按 SKILL 规则跳过）。

**Further-viewing URLs** — 3 条 YouTube 链接均以浏览器 UA 验证 200，频道归属确认为 Chroma ATE / Chroma ATE Netherlands 官方频道；不承载任何数字。

**SEC filenames** — n/a（无 SEC 引用）。

**财报/法说会数字 spot-checks（claim → 原文位置）：**
- FY2025 合并营收 NT$28,311mn、+31% YoY ✓（Q4 简报 Slide 10 P&L：“Net Sales 28,311 ... 21,604 ... 31%”）
- 2026Q1 营收 NT$11,859mn、+73% YoY、+38% QoQ；GM 63%；EPS 9.12 ✓（Q1 简报 Slide 5）
- Q1 ATS 分部 NT$5,390mn、+145% YoY、+105% QoQ ✓（Q1 简报 Slide 8）
- Customer A FY2025 NT$5,100,376 千元 = 18.02%（FY2024 16.60%），“Mainly due to the increase in demand for SLT testing equipment” ✓（年报 p.119，PDF 第 124 页原文逐字核对）
- 出口 82% / 内销 18% ✓（年报 p.113 表：23,265,764 / 28,310,935）
- R&D 费用 NT$2,556,457 千元 = 营收 9% ✓（年报 p.109 表）
- 3Q25 一次性处分收益 NT$3,185mn ✓（Q4 简报 Slide 9 脚注原文 “gain from disposal of residential apartment held for sale (to employees) of NTD 3,185 million”）
- 5 月营收 NT$45.50 亿、−6.5% MoM、+133.1% YoY、前 5 月 NT$212.75 亿 +94.4% ✓（TechNews 原文逐字）
- SEMI：测试设备 2025 US$11.2bn +48.1%、2026 +12.0%、2027 +7.1%；总设备 133/145/156 ✓（PR Newswire 转发稿）
- GPU TDP Hopper 700W → Blackwell 1000–1400W → Rubin 1800–>3000W ✓（Q4 简报 Slide 16，注明 Source: NVIDIA GTC 2025/CES 2026, Industry Estimates）

**zsxq 数字 string-match（对 OCR/抽取原文，非 翻译精华）：**
- “Apr-May sales of NT$9.4B, up 129% YoY in US$ terms” ✓（file_id 814528815844822 OCR 文本 p.1）
- “NT$13.8-15.6B (+115% to +141% YoY), with the NT$14.9B midpoint c.20% above cons.” ✓（同上）
- “52x forward P/E and 42x on 2027 consensus EPS”、“2.6x against TWSE”、“1.3x (5-Yr Avg)” ✓（同上 Exhibits 7–8 OCR）
- “We rate Chroma ATE Outperform, with PT = NT$1,660” / “38x against our 2027 EPS estimate of NT$43.7” ✓（同上 p.4–5）
- Bernstein 2026-03-16：“AI SLT revenue to nearly triple in 2026”、“double Chroma's metrology sales to ~NT$3B in 2026 and NT$4B in 2027”、“35% / 52% CAGR”、“PT to NT$1,660 (from NT$970)”、“38x (from 31x)”、EPS “NT$43.7 (vs. old NT$31.4)” ✓（file_id 212222825221841 抽取文本）——**已修正翻译精华的一处错误：精华作“量测翻倍至 30 亿美元”，原文为 ~NT$3B（新台币）**
- MS：“Chroma (2360.TW, OW, PT NT$2,800)”、“based on 50x 2027e P/E vs. current valuation of 46x 2027e” ✓（file_id 214528851488581 p.3-4 抽取）
- JPM：“Chroma is the leader in AI data center power testing.”、“Nvidia GPU SLT equipment shipment (Chroma 100% share)”、“each at 40%+ CAGR”、“TAM 80%+ CAGR” ✓（file_id 585548152542554 pp.18–22 抽取 + p.19 段表 4× 放大 vision 核读）
- UBS：“Chroma ATE 2360.TW … 2,325.00 2,600.00 Buy” ✓（file_id 812458124211512 OCR p.偏好组合表）；“Equipment was the outperformer with Chroma and Hon Precision both 40% of consensus” ✓（file_id 212452255428221 OCR）
- Bernstein Vera Rubin：“~$9.1M rack”、“$47bn”（机柜 32 + 基建 15）、“GPU…$55k per GPU”、EPS 列 “27.50 / 33.22 / 43.66”、P/E “93.3 / 77.2 / 58.8” ✓（file_id 814528815844812 抽取文本）

**借入卖方 PT 与报告日价格配对** — Bernstein 2026-03-16：PT 1,660 vs 当日收盘 1,450（+14.5%，stock_price_target.db `report_date_price`/`upside_pct`）✓；MS 2026-06-05：PT 2,800 vs 收盘 2,565（+9.2%，同库）✓；UBS 2026-05-09：PT 2,600 vs 报告表内价格 2,325（+11.8%，两数同源于该 PDF 表格；yfinance 2026-05-08 收盘为 2,230，已在正文标注价格口径为“报告表内价格”）✓；Bernstein 2026-06-07/08 沿用 PT 1,660 vs 06-05 收盘 2,565（−35.3%，推导）✓。

**Analyst-view 标注审计** — 全部评级/目标价/前瞻预估/份额估计/TAM 增速/竞争力判定均带 *分析师观点：*/*视角观点:* 标签；零条卖方观点挂接财报引用；“leader in AI data center power testing”、“100% share” 等领导地位/份额表述全部归属 J.P. Morgan 而非公司年报。年报中“each product technology can maintain its leading position”为公司自述、以原文块引呈现并标明出处。报告自身预估无任何 “(Source: our model)” 类自引用。

**卖方观点演变** — `db/stock_price_target.db` 只读预检先行（3 行命中，其中 2360.TW 2 行）✓；按机构时间线含同机构自我修订（Bernstein 970→1,660 + “will revisit our model”）与触发因素 ✓；跨机构分歧表（Bernstein 1,660 / UBS 2,600 / MS 2,800，极差 69%）✓；全部观点带日期 + `/zsxq/pdf/<file_id>/<filename>` 直链 ✓。

**zsxq 直链路由** — 9 条引用均为 `find_pdf.py` 输出的 `pdf_url`（`/zsxq/pdf/<file_id>/<URL-encoded-name>` 直接下载路由），`local_exists: true` 全部确认；无 `/zsxq-pdf/`（死路由）或 `/zsxq/pdf-viewer/`（HTML 页）形式。

**Institute research 计数** — 检索 3 个别名（2360 / Chroma / 致茂），命中 27 行（去重约 20 份），引用 9 份；未触发 downloader 补抓（本地覆盖充足）。

**内部一致性** — 第 1 章竞争表述与第 7 章一致（SLT/电源测试利基领先 = 卖方观点；公司自述 = 年报块引）；第 2 章时间线与第 1/3 章叙事一致；客户集中度第 5 章（18.02% 合并口径）与第 9 章风险一致；产品 mermaid 树与 4.3–4.6 小节口径一致；母公司分部 pie（分母 NT$22,012mn）与 Customer A（分母合并 NT$28,311mn）已显式区分分母。

**残留未知 / 未尽核验：**
- Customer A 身份为市场推断（卖方建模），公司未披露——正文已明示。
- 2027E 共识 EPS ≈ NT$61 为派生值（2,565 ÷ 42，两输入均出自 Bernstein 2026-06-07 报告），非共识数据库直读——正文已标注推导式。
- UBS 报告表内价格 2,325 与 yfinance 2026-05-08 收盘 2,230 存在差异（疑为盘中价或不同基准日），正文按“报告表内价格”引用并在本日志披露。
- FY2023 经营利润率（13.5%）为合并报表推算近似值，图注已标示。
- CommonWealth（cw.com.tw）与 SEMI 官网原文因 403 未直接核读；SEMI 数据经 PR Newswire 官方转发稿核实，CommonWealth 未引用。
- 公司无公开 investor day deck（IR 覆盖以两份季度法说会简报为主）——absence logged。

</details>
