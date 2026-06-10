# 存储超级周期 / Memory Up-Cycle

**Created:** 2026-05-31 · **Last refreshed:** 2026-06-10 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en, zh

## What's New

*自上次查看以来的增量信息——按时间倒序排列。*

**2026-06-10 刷新（对比 2026-05-31）：**

- **首个回调窗口：等权篮子 −3.2%（中位数 −4.3%），同期 SOX −4.9% / 标普 −4.1% / KOSPI −4.5%**——与全市场回调同步而非更差，但内部剧烈轮动：**设备股上涨（Tokyo Electron +18.0%、AMAT +10.4%）、原厂回调（SK Hynix −12.2%、旺宏 −18.9%、华虹 −14.9%、美光 −8.1%）**——正是建仓时预判的"设备 vs 原厂"差距收敛（yfinance，05-29 → 06-10 收盘）。
- **SOCAMM 事件是本窗口的核心扰动**：SemiAnalysis（6/4-5）报道英伟达把 Vera Rubin NVL72 的 SoCAMM2 DRAM 容量从 55TB 砍到 28TB/机柜（192GB → 96GB 模组）；Citi 判断 *"no change to SoCAMM2 demand"*（系供给约束而非需求转弱，[Citi, zsxq #584251528855554 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/584251528855554/CITI-Global%20Semiconductors%EF%BC%9AAssessing%20the%20Impact%20of%20NVDA%E2%80%99s%20Rubin%20SoCAMM2%20Capacity%20Reduction-260607.pdf#page=1)）；JPM 称该噪声 *"misleading"*，维持 DRAM bit 需求 **+33%/+34%（2026/27E）**，并把回调定性为 *"a good buying opportunity from a midterm horizon"*（[JPM, zsxq #584251482281424 p.1-3](http://xs-macbook-air.local:5001/zsxq/pdf/584251482281424/J.P.%20Morgan-Memory%20Market%20Update%EF%BC%9ASOCAMM%20content%20noise%20offers%20a%20buying%20opportunity%EF%BC%9B%20thoughts%20on%20NVDA~SKH%20partnership%20and%20takeaways%20from%20Computex%202026-260608.pdf#page=1)）。
- **目标价上调潮，但街价在追市**：MS 美光 **$520 → $1,050**（29.5x × 穿越周期 EPS $35）、闪迪 **$1,100 → $1,750**（28x × $62.50）（[MS, zsxq #585412884821284 p.1/p.3](http://xs-macbook-air.local:5001/zsxq/pdf/585412884821284/MS-Semiconductors%20-%20North%20America%20Raising%20estimates-PTs%20for%20memory%20stocks%20as%20demand%20continues%20to%20outpace%20supply-260603.pdf#page=1)）；GS 美光 **$400 → $900**（18x × 正常化 EPS $50，[GS, zsxq #412458524148888 p.2](http://xs-macbook-air.local:5001/zsxq/pdf/412458524148888/GS-Micron%20Technology%20Inc.%20%28MU%29_%203Q%20Preview_%20Another%20strong%20quarter%20reflects%20extension%20of%20tight%20supply_demand%20through%202027-260608.pdf#page=2)）；BofA 闪迪 **$1,550 → $2,100**（~10x C27E EPS $199，[BofA, zsxq #181245182285222 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/181245182285222/Bofa-Sandisk%20Corporation%20Supply-Demand%20balance%20remains%20tight%2C%20pricing%20strong%3B%20PO%20to%20%242100-260608.pdf#page=1)）。注意 MS 上调后的美光 PT 仍低于发布日股价（$1,050 vs $1,079.57 @ 06-03）。6 条 PT 已写入 `stock_price_target_db`（见估值快照）。
- **首个减速信号上线**：Bernstein 5 月月度追踪确认 2QCY26 DRAM 合约价 **+64% QoQ**（PC +46 / 服务器 +53 / 手机 ~80 / 消费 ~85）、NAND 混合 **~+60% QoQ**，但预期 3QCY26 *"decelerate significantly to 10-20% QoQ"*、价格 *"normalize from 2HCY27 and into CY28"*（[Bernstein, zsxq #212485115581121 p.1/p.4](http://xs-macbook-air.local:5001/zsxq/pdf/212485115581121/Bernstein-Global%20Memory%EF%BC%9AMEMORY%20TRACKER%20%EF%BC%88May%EF%BC%89%EF%BC%9A%20Price%20hike%20c.%2060%25%20QoQ%20in%202QCY26%EF%BC%8C%20but%20likely%20at%20a%20slower%20pace%20in%202HCY26-260602.pdf#page=1)）。
- **铠侠投资者日（06-02）上调 NAND 需求锚**：CY25-28 bit 需求 CAGR **20% → 22%**（主要来自 eSSD；[Bernstein, zsxq #415284114485228 p.1-2](http://xs-macbook-air.local:5001/zsxq/pdf/415284114485228/Bernstein-Global%20Memory%EF%BC%9AKIOXIA%20Investor%20Day%EF%BC%9A22%25%20bit%20CAGR%20good%20enough%EF%BC%9F-260602.pdf#page=1)）；同日 MS OW ¥110,000 vs Bernstein ¥17,000——同一事件、139% 的分歧。
- **领先指标创纪录**：韩国 5 月 DRAM 出口 **+370% YoY**——*"the highest figure since tracking began in January 2008"*；NAND 芯片 +207% YoY（[GS, zsxq #812485454488152 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485454488152/Goldman%20Sachs-South%20Korea%20Tech%EF%BC%9A%20May%202026%20export%20tracker%EF%BC%9A%20Record~high%20DRAM%20exports%20with%20370%25%20yoy%20growth-260601.pdf#page=1)）。
- **格式升级**：中英两份文件同步至最新主题规范（估值快照 + 卖方观点演变 + 篮子记分卡 + 领先指标 + 4 张图表）；英文版补齐 5-31 扩容（此前仅落在中文版）；ticker 前缀统一为 KRX/TSE/TWSE/HKEX 规范。
- **宏观切换**：VIX 16.68 → **21.51**（2026-06-05，`indicators.db`）——建仓时的低波动顺风已消失。

<details><summary>更早记录</summary>

**2026-05-31 — 基于原始 PDF 文本（OCR 后）的重写 + 篮子扩容 14→16 + 来源 13→22 份 zsxq 报告。** 整篇报告改用原文（不再依赖 zsxq 翻译精华——经核对，翻译精华会四舍五入并丢失关键数字），每个券商数字均附 PDF 页码 + 原文逐字引用。

新增两只标的：
- **TWSE:2408 南亚科 Nanya Technology**（core）——MS 在《大中华区半导体——传统存储器：即将迎来超预期上涨》中将其与华邦电子一并 **上调至 Overweight** ([MS — Old Memory: Upside Surprise, zsxq #212451114418521 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1) — *"Winbond and Nanya to OW"*；目标股票 *"Nanya Technology Corp. (2408.TW)"*)，是台股 DRAM 纯标的；过去一年 +835.3%。
- **SZSE:301308 江波龙 Longsys**（adjacent）——A 股 NAND 模组龙头，作为 YMTC / CXMT 国产存储扩产周期的下游配套代理；过去一年 +648.5%。卖方 zsxq 报告中仅在覆盖名单出现（未见专项首推），列为 adjacent 而非 core，理由透明披露。

新增信号：
- **UBS 首次覆盖铠侠（285A.T）：Buy，PT ¥79,000**，定调 *"Peak is not here yet"* ([UBS — Kioxia, zsxq #812485584818522 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1) — *"likely to rise qoq for the next six quarters before peaking in Q3 2027 (about 1.5 years)"*) — 给出了具体的周期峰值时点（2027 Q3）和持续度（未来六个季度环比续涨）。
- **MS 内存扩产 + 华为 τ 定律双催化**（[zsxq #415241112254128](http://xs-macbook-air.local:5001/zsxq/pdf/415241112254128/MS-Greater%20China%20Semiconductors%20Double%20Catalysts%20from%20Memory%20Expansion%20and%20Huawei%27s%20t%20%28Tau%29-Law-260527.pdf#page=1) — *"Implications of Huawei's t (Tau)-Law for WFE: On May 25, Huawei published a … 3D IC breakthrough"*) — YMTC 上海扩产加速 + 5 月 25 日华为 3D IC 突破，是国产存储设备需求的明确催化剂。
- **Bernstein "存储产能扩张浪潮"**（[zsxq #184128224215212 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1) — *"CXMT and YMTC are forced to switch away from US supply chain"*）——CXMT 与 YMTC 强制切换至本土设备链，是 2027/28 国产 WFE 资本开支上修的核心逻辑。
- **UBS 美光：长期协议（LTA）加速落地，PT 上调至 \$1,625**，预期 EPS *"comfortably >$100 throughout the period"* through FY2029 ([UBS — MU, zsxq #585428582552154 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/585428582552154/UBS-Micron%20Technology%20Inc%20LTAs%20Gain%20Traction%3B%20PT%20to%20%241%2C625%20with%20EPS%20Remaining%20Well%20-%24100-260526.pdf#page=1))。
- **GS 华虹半导体：12 英寸产能扩张 + AI 应用驱动，维持 Buy**（[GS — Hua Hong, zsxq #812485541485582 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485541485582/Goldman%20Sachs-Hua%20Hong%20%EF%BC%881347.HK%EF%BC%89%EF%BC%9A%2012~inch%20capacity%20increasing%EF%BC%9B%20AI%20applications%20drive%20demand%20and%20loading%EF%BC%9B%20Buy-260529.pdf#page=1)）；MS AAI 反馈强调 *"Multi-year Pricing Cycle and Aggressive Long-term Revenue Guidance"* ([MS — Hua Hong AAI, zsxq #212485545245181 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485545245181/Morgan%20Stanley-Hua%20Hong%20Semiconductor%20Ltd%EF%BC%881347.HK%EF%BC%89Asia%20AI%20Summit%202026%20Feedback%EF%BC%9A%20Multi~year%20Pricing%20Cycle%20and%20Aggressive%20Long~term%20Revenue%20Guidance%20in%20Focus-260528.pdf#page=1)) ——**纠正**上次基于 zsxq 摘要的旧版本：旧版本曾把 file_id 812485545245152 误标为 "MS Hua Hong AAI"，该文实为 MS 同仁堂（600085 中药），现已剔除。

业绩重算（16 只标的）：1Y **+1,086.4%**（中位数 **+672.6%**）、YTD **+169.0%**、3M **+69.7%**。1Y 较 14 只篮子（+992%）进一步上行，主要由 SNDK / Kioxia 上市后基期效应以及新增的两只放大；中位数仍是更可靠的体感数字。**对比同期 KOSPI +232.5% / SOXX +210.4% / SOX +202.9%**——主动篮子相对 SOX 类被动半导体仍领先 ~800-880pp 的中位数差距，但回撤集中度极高（任一只大权重 −30% 单季拐点都会显著拉低）。

**2026-05-31 — 篮子创立** (14 只标的：8 core / 6 enabler；当时基于 zsxq 翻译精华摘要构建；本次重写已用 OCR 原文替换全部引用)。

</details>

## 主题逻辑

存储行业自 2024H2 启动新一轮上行周期，但本次与历史周期最大的不同是 **AI 推理对 HBM/eSSD/DDR5 形成的结构性需求叠加 PC/智能机/汽车的常规复苏共振**，把"周期"拉长成更接近"超级周期"的轮廓。摩根大通的全球存储模型把这点量化得最清楚：**2028 年存储市场 TAM 上修至 1.7 万亿美元**，较此前模型上调 **+37%~53%**，DRAM/NAND 合约价同比 **+220-250%**，HBM bit-CAGR **+85%**，三年累计资本开支 **\$450bn**，**存储已占 CSP 硬件资本开支的 52%**（[JPM — Global Memory, zsxq #184152588584282 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1) + [复制版 #212485541484181 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485541484181/J.P.%20Morgan-Global%20Memory%20Market-CPU%20adds%20fuel%20to%20the%20%E2%80%98higher%20and%20longer%E2%80%99%20upcycle%20thesis%20and%2028E%20TAM%20at%20%241.7trn%3B%20valuation%20framework%20transition%20in%20progress-260529.pdf#page=1) — *"2028E TAM revisions of +37-53%"*；*"$450B 3-yr capex"*；*"52% of CSP hardware capex"*）。eSSD（数据中心 SSD）TAM 价值 **>\$300bn**，HBM 让 DRAM 晶圆向 HBM 的分配从 **24%→31%**（同一篇 p.1）。

![JPM 存储 TAM 新旧模型对比](../charts/theme_memory-upcycle_anchor.png)

第二条主线是 **AI 推理（inference）对 CPU 的再次需要**：[JPM 计算机推理与 Agentic AI](http://xs-macbook-air.local:5001/zsxq/pdf/212485811841111/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A1%8C%E4%B8%9A%E4%B8%93%E9%A2%98%E7%A0%94%E7%A9%B6%EF%BC%9A%E6%8E%A8%E7%90%86%E4%B8%8EAgentic%20AI%E6%B5%AA%E6%BD%AE%E4%B8%8B%EF%BC%8CCPU%E9%87%8D%E5%9B%9EAI%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E6%A0%B8%E5%BF%83%E4%B8%AD%E6%9E%A2.pdf#page=1) 论证 CPU 回到 AI 基础设施的核心中枢——推理负载靠 CPU 编排、AI 代理负载需要海量上下文驻留——共同把 **CPU:GPU 配比** 从训练阶段的 1:8 拉回 1:1～1:2，对应每台服务器的 DRAM/NAND 用量阶跃。摩根大通因此把整个上行周期定调为 **"higher-for-longer"**——估值框架正在从过去 "周期长度 8 季" 切换到 "12-16 季"。

第三条主线是 **行业供给同时绷紧**：[UBS 首次覆盖铠侠](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1) 给出最具体的周期视角——*"Peak is not here yet… likely to rise qoq for the next six quarters before peaking in Q3 2027 (about 1.5 years)"*——这是 zsxq 整批存储研报里唯一把"峰值时点"具体到季度的卖方判断。MS 大中华区半导体团队则在 [《大中华区半导体——传统存储器：即将迎来超预期上涨》](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1) 中把华邦电子（Winbond）与南亚科（Nanya）一并上调至 OW——*"We think wider supply/demand will boost earnings… Winbond and Nanya to OW"*；SLC NAND 在 AI 服务器 BBU / NIC 上的需求 + 老节点产能向 HBM/DDR5 切换共同造成传统存储器的"挤压式"上涨。

中国端的故事是 **国产替代加速**：[MS 内存扩产 + 华为 τ 定律](http://xs-macbook-air.local:5001/zsxq/pdf/415241112254128/MS-Greater%20China%20Semiconductors%20Double%20Catalysts%20from%20Memory%20Expansion%20and%20Huawei%27s%20t%20%28Tau%29-Law-260527.pdf#page=1) 报告 5 月 25 日华为发布 3D IC 突破——*"Huawei's t (Tau)-Law"*——叠加 YMTC 上海扩产加速，构成国产存储 + 国产存储设备的双重催化；[Bernstein 中国半导体——存储产能扩张浪潮](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1) 进一步指出 *"both CXMT and YMTC are forced to switch away from US supply chain"*——把 2027/28 国产 WFE 资本开支预期上修。这条主线为篮子中的兆易创新（603986）+ 华虹（1347.HK）+ 新增的江波龙（301308）提供更厚的国产周期 β。

最后是 **下游传导**：智能机和 PC 端的存储成本压力是消费股 Q1-Q2 业绩的核心干扰项。[杰富瑞——小米 Q1 业绩前瞻](http://xs-macbook-air.local:5001/zsxq/pdf/585428511282514/Jefferies-Xiaomi%EF%BC%881810.HK%EF%BC%89%EF%BC%9A1Q26%20Preview%EF%BC%9A%20Memory%20Cost%20Pressure%20Not%20Yet%20Peaked%EF%BC%9B%20Cons%20Still%20Too%20High-260525.pdf#page=1) 与 [Bernstein——小米 Q1 业绩](http://xs-macbook-air.local:5001/zsxq/pdf/585428811251444/Bernstein-Xiaomi%20Corp%EF%BC%881810.HK%EF%BC%89Xiaomi%20Q1%EF%BC%9A%20Resilience%20on%20display%20amid%20memory%20cycle%EF%BC%9B%20fundamentals%20reinforced%20%E2%80%94%20reiterate%20Outperform-260527.pdf#page=1) 都把"存储成本压力"列为 Q1-Q2 毛利率最主要压制项；GS 4 月中国智能机出货 +12% YoY / +25% MoM 的反弹 ([GS — China Smartphone, zsxq #812485545248882 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485545248882/Goldman%20Sachs-China%20Smartphones%EF%BC%9A%20Apr%20shipments%20%2B12%25%20YoY%20%2B25%25%20MoM%EF%BC%9B%202Q%20memory%20cost%20pressures%20remained-260528.pdf#page=1)) 与存储涨价同时出现，说明终端能在一定程度上承接价格。这条传导链不会让存储原厂的上行周期"更甜"——但它确认了"价格-体感"已经传到消费端，意味着合约价的环比加速不是空中楼阁。MS 的充足度框架把这条传导量化为 2027E 双边平衡：AI 优先分配之后，**PC 缺口 ~15%（≈−58mn 台；19bn Gb = PC 需求的 13%）、智能机缺口 ~12%（≈−134mn 部）**（[MS — Chipflation, zsxq #184152882245822 p.3/p.7-8](http://xs-macbook-air.local:5001/zsxq/pdf/184152882245822/MS-Global%20Technology%20Chipflation%20%E2%80%93%20Navigating%20A%20Memory%20Crisis-260602.pdf#page=7)）。

![2027E 消费端存储供需缺口（MS 充足度框架）](../charts/theme_memory-upcycle_sd_balance.png)

**延伸观看（Further viewing——教学辅助，非引用源，不承载任何数字）**

- [SK hynix 官方 HBM 入门（TSV 堆叠结构动画）](https://news.skhynix.com/become-a-semiconductor-expert-with-sk-hynix-hbm/)——直观理解 HBM 每 GB 消耗数倍晶圆面积的物理基础，即"晶圆分配挤压"的来源。
- [Branch Education — How does Computer Memory Work?（DRAM 单元与存储层级 3D 动画）](https://www.youtube.com/watch?v=7J7X7aZvMXQ)——理解 "bit 供需" 之前最好的视觉底子。

## 范围界定

**纳入**：(a) DRAM/NAND/HBM 的整合原厂（SK Hynix、Samsung、Micron、Kioxia、Sandisk、WDC、YMTC/CXMT 的上市代理）；(b) DRAM/NAND 专用产能但非领先节点（GigaDevice、Winbond、Macronix、Nanya）——属于"传统存储器挤压上涨"的最直接受益；(c) 存储相关晶圆代工 / 配套（华虹 1347.HK 在 12 英寸成熟节点的 AI 应用占比上升）；(d) 关键存储设备（AMAT、LRCX、TEL、Advantest 的存储 WFE 敞口）；(e) NAND 模组（江波龙作为 YMTC 配套代理）。所有标的必须有 2025-2026 一次卖方 / IR 的存储业务点名。

**剔除**：(a) AI 加速器（NVDA、AVGO）——独立主题（数据中心算力），属于存储的下游而非存储本身；(b) 全闪存数据中心整合商（PSTG、NTAP）——独立的"硬件 + 软件"主题；(c) KLAC、PLAB、TER——存储敞口次要或被 SoC 端摊薄；(d) 存储模组 / 控制器纯标的 Adata、Innodisk、Apacer、Phison——pass-through 模型，毛利不上行；(e) 中国国产存储设备前道领军 NAURA、AMEC、Piotech、华海清科——已整合至 `china-domestic-wfe` 独立主题（如建立）；(f) Ingenic、摩尔线程——被 GigaDevice / GPU 主题主导；(g) CXMT、YMTC——未上市，若上市将作为篮子变动的触发条件。

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| KRX:000660 | SK Hynix 海力士 | core | DRAM 全球龙头 + HBM3E/HBM4 几乎独家供应英伟达 GB200/GB300；[JPM Global Memory zsxq #184152588584282 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1) 把 SK Hynix 列为 *"net winners in the higher-for-longer cycle"*。1Y +1,189.5%——价格已包含周期再定价，但 HBM 中期产能已锁定到 2026 年底。 | 2026-05-31 |
| KRX:005930 | Samsung Electronics 三星电子 | core | 唯一同时具备 DRAM/NAND/Foundry/Display 的整合存储原厂；HBM4 量产时点是 Samsung 重夺市场份额的关键变量，[JPM Global Memory zsxq #184152588584282 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1) 将其列为受益方。2026 年罢工悬而未决 ([JPM #812451582581222](http://xs-macbook-air.local:5001/zsxq/pdf/812451582581222/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E4%B8%89%E6%98%9F%E7%94%B5%E5%AD%90%EF%BC%88005930.KS%EF%BC%89%E6%88%8F%E5%89%A7%E6%80%A7%E5%92%8C%E8%A7%A3%E8%90%BD%E5%B9%95%EF%BC%8C%E7%BD%A2%E5%B7%A5%E6%82%AC%E8%80%8C%E6%9C%AA%E5%86%B3%E4%B8%BB%E8%A6%81%E9%97%AE%E9%A2%98%E5%9F%BA%E6%9C%AC%E6%B6%88%E9%99%A4%EF%BC%8C%E5%8F%AF%E9%80%A2%E4%BD%8E%E5%90%B8%E7%BA%B3.pdf#page=1)) 已基本释放——结构性 catch-up 仍可期。 | 2026-05-31 |
| NASDAQ:MU | Micron 美光 | core | 美国唯一存储原厂，HBM3E 已切入英伟达供应链，**UBS 长期协议 LTAs 加速落地，PT 上调至 \$1,625**，预期 EPS *"comfortably >\$100 throughout the period"* through FY2029 ([UBS — MU, zsxq #585428582552154 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/585428582552154/UBS-Micron%20Technology%20Inc%20LTAs%20Gain%20Traction%3B%20PT%20to%20%241%2C625%20with%20EPS%20Remaining%20Well%20-%24100-260526.pdf#page=1) — *"LTAs Gain Traction; PT to \$1,625 with EPS… long term agreements (LTAs) across the entire memory complex"*)。1Y +1,139.0%。 | 2026-05-31 |
| TSE:285A | Kioxia 铠侠 | core | NAND 纯标的（西部数据 NAND 业务 spin-off 后唯一独立日本上市），**UBS 首次覆盖 Buy，PT ¥79,000**，定调 *"Peak is not here yet"*——*"likely to rise qoq for the next six quarters before peaking in Q3 2027 (about 1.5 years)"* ([UBS — Kioxia, zsxq #812485584818522 p.1-2](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1))；MS 在 2026 日本峰会另设 PT ¥70,000 ([MS — Kioxia zsxq #415241445451248 p.7](http://xs-macbook-air.local:5001/zsxq/pdf/415241445451248/Morgan%20Stanley-KIOXIA%20Holdings%20%EF%BC%88285A.T%EF%BC%89Japan%20Summit%202026%20Feedback-260521.pdf#page=7))。1Y +3,391.5% 系上市后基期效应。 | 2026-05-31 |
| NASDAQ:SNDK | SanDisk | core | NAND 纯标的（WDC 2025 年 spin-off）；与 Kioxia 在 NAND 产能上深度协作，与 Kioxia 同步受益于上行周期。1Y +5,152.5% 系 spin-off 后非市场基期形成的统计假象，应以中位数体感而非均值。 | 2026-05-31 |
| NASDAQ:WDC | Western Digital | core | 剥离 NAND 之后聚焦 HDD——HDD 的"数据中心仓库"需求在 [MS 日本电子元器件—4 月 HDD/SSD 数据](http://xs-macbook-air.local:5001/zsxq/pdf/212485814114481/Morgan%20Stanley-Electronic%20Components%20Apr%20HDD%20SSD%20Data%EF%BC%9A%20Continuing%20Strong%20Data%20Center%20Demand-260529.pdf#page=1) 中得到验证（*"HDD/SSD data confirms strong data center demand"*）。 | 2026-05-31 |
| SSE:603986 | GigaDevice 兆易创新 | core | A 股 NOR Flash + 利基 DRAM + MCU 龙头。NOR 在 AI 服务器 / BBU 用量阶跃，与华邦同为 NOR 行业上行的双标的。 | 2026-05-31 |
| HKEX:1347 | Hua Hong 华虹半导体 | enabler | **GS 维持 Buy**——*"12-inch capacity increasing; AI applications drive demand and capacity utilization"* ([GS — Hua Hong, zsxq #812485541485582 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485541485582/Goldman%20Sachs-Hua%20Hong%20%EF%BC%881347.HK%EF%BC%89%EF%BC%9A%2012~inch%20capacity%20increasing%EF%BC%9B%20AI%20applications%20drive%20demand%20and%20loading%EF%BC%9B%20Buy-260529.pdf#page=1))；**MS 2026 亚洲 AI 峰会反馈**关注 *"Multi-year Pricing Cycle and Aggressive Long-term Revenue Guidance"* ([MS — Hua Hong AAI, zsxq #212485545245181 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485545245181/Morgan%20Stanley-Hua%20Hong%20Semiconductor%20Ltd%EF%BC%881347.HK%EF%BC%89Asia%20AI%20Summit%202026%20Feedback%EF%BC%9A%20Multi~year%20Pricing%20Cycle%20and%20Aggressive%20Long~term%20Revenue%20Guidance%20in%20Focus-260528.pdf#page=1))——多年价格周期 + 激进的长期收入指引成为焦点。是篮子里成熟节点 + AI 应用占比上升的代表。 | 2026-05-31 |
| TWSE:2408 | Nanya Technology 南亚科 | core | **MS 在《大中华区半导体——传统存储器：即将迎来超预期上涨》中上调至 OW**——*"Winbond and Nanya to OW"* ([MS — Old Memory: Upside Surprise, zsxq #212451114418521 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1))。台股 DRAM 纯标的，与 Winbond 同为"老节点存储挤压上涨"的双品种。1Y +835.3%。 | 2026-05-31 |
| TWSE:2344 | Winbond 华邦电子 | core | NOR + SLC NAND + 利基 DRAM 三栖。**MS AAI 反馈：OW，目标价 NT\$222**（~54% upside），现有 NOR 产能 30kwpm + SLC NAND 15kwpm，**各扩产 10kwpm**（合计 +20kwpm），16nm DRAM 从 2-3K → 5K → 16K wpm 路径清晰，*"500-600 NOR chips per Vera Rubin rack"*——英伟达 Vera Rubin 平台对 NOR 的用量重新放大 ([MS — Winbond AAI, zsxq #812485545245422 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485545245422/Morgan%20Stanley-Winbond%20Electronics%20Corp%20%EF%BC%882344.TW%EF%BC%89Asia%20AI%20Summit%202026%20Feedback-260528.pdf#page=1))。 | 2026-05-31 |
| TWSE:2337 | Macronix 旺宏 | core | NAND/NOR Flash；十个亏损季的连胜终结，NAND +382% YoY；与 Winbond 一同成为传统存储器 NAND 上涨的代理。 | 2026-05-31 |
| SZSE:301308 | Longsys 江波龙 | adjacent | A 股 NAND/DRAM **模组龙头**，作为 YMTC（NAND） + CXMT（DRAM）国产存储扩产的下游模组配套代理——[Bernstein zsxq #184128224215212 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1) 把 *"CXMT and YMTC are forced to switch away from US supply chain"* 列为国产存储链上行的定调判断。zsxq 报告中无单独研究覆盖，列为 adjacent 而非 core 以保持论据透明（1Y +648.5%）。 | 2026-05-31 |
| NASDAQ:AMAT | Applied Materials | enabler | **Bernstein 跑赢大盘，目标价 \$525**——逻辑 + DRAM + 先进封装合计 *"~80% of 2026 incremental WFE"*，~50% 增量逻辑端开支落入 AMAT ([Bernstein — AMAT SDC, zsxq #212485522841821 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485522841821/Bernstein-Applied%20Materials%20%EF%BC%88AMAT.US%EF%BC%89%EF%BC%9A%20Key%20takeaways%20from%20Bernstein%27s%20SDC-260528.pdf#page=1))。 | 2026-05-31 |
| NASDAQ:LRCX | Lam Research | enabler | NAND 蚀刻 + DRAM 上行周期主要受益方；[MS 半导体资本设备—日本调研 zsxq #184152218151852](http://xs-macbook-air.local:5001/zsxq/pdf/184152218151852/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9AJapan%20Takeaways-260529.pdf#page=1) 指出 *"Kioxia FY27 capex ¥450bn, TEL GM 45%→50% by FY28"*——日韩存储原厂资本开支的提速直接利好 LRCX。 | 2026-05-31 |
| TSE:8035 | Tokyo Electron | enabler | 日本存储 WFE 龙头；[MS 半导体资本设备—日本调研](http://xs-macbook-air.local:5001/zsxq/pdf/184152218151852/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9AJapan%20Takeaways-260529.pdf#page=1) 中 *"TEL GM 45%→50% by FY28"* 是直接读数；铠侠 FY27 ¥450bn 资本开支是关键拉动。 | 2026-05-31 |
| TSE:6857 | Advantest | enabler | HBM 测试 + AI 加速器测试双引擎；[MS 半导体资本设备—台湾调研 zsxq #415284812111518](http://xs-macbook-air.local:5001/zsxq/pdf/415284812111518/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9ATaiwan%20Takeaways-260529.pdf#page=1) 指出测试瓶颈是台湾产业链的主要约束。 | 2026-05-31 |

**地理 / 角色分布（16 只标的）：** 韩国 2 (13%) · 美国 4 (25%) · 台湾 3 (19%) · 日本 3 (19%) · 香港 1 (6%) · A 股 2 (13%) · 美国 NAND 纯标的 2 (12%, SNDK+WDC)。角色：core 11、enabler 4、adjacent 1。

## Valuation snapshot / 估值快照

行情来自 `stock_price_target_db`（2026-05-01 以来各机构最新一条；`/pt` 同源）——**Px @ note 为发布日股价**（`report_date_price`），锁定分析师实际给出的 upside；*现价* 为 2026-06-10 收盘（yfinance）。Fwd P/E = FY1 一致预期（yfinance `.info`，2026-06-10 拉取）。完整表格、逐列脚注（FY1E/FY2E、own-avg 推导、stale 隔离）见英文版 [memory-upcycle_theme.md](memory-upcycle_theme.md) § Valuation snapshot——两份文件同源于同一 PT store，数值一致。要点行（评级 · 发布日价 vs PT = upside · 现价 · FY1 fwd P/E）：

- **NASDAQ:MU**：GS Buy · $900 vs $949.28 @ 06-08 = **−5.2%** · 现 $891.88 · 8.0x —— PT 分歧 n=6：$510 / $925 / $1,625，**价差 121%**
- **NASDAQ:SNDK**：BofA Buy · $2,100 vs $1,642 @ 06-08 = **+27.9%** · 现 $1,643.23 · 9.0x —— MS 牛/基/熊 **$2,635 / $1,750 / $1,100**（[MS RR, zsxq #184155215151842 p.2](http://xs-macbook-air.local:5001/zsxq/pdf/184155215151842/Morgan%20Stanley-SanDisk%20Corporation.%EF%BC%88SNDK.US%EF%BC%89Risk%20Reward%20Update-260603.pdf#page=2)）
- **KRX:000660**：MS ₩2,600,000 vs ₩1,839,692 @ 05-18 = +41.3% · 现 ₩2,048,000 · 5.0x —— 分歧 ₩1.15m / ₩2.35m / ₩4.0m（Nomura 街最高）
- **KRX:005930**：GS Buy · ₩320,000 vs ₩292,500 @ 05-22 = +9.4% · 现 ₩302,500 · 5.3x
- **TSE:285A**：MS OW · ¥110,000 vs ¥77,540 @ 06-02 = +41.9% · 现 ¥70,500 —— 分歧 ¥17k / ¥67k / ¥110k，**价差 139%**（篮内最宽）
- **HKEX:1347**：GS Buy HK$174 vs MS EW HK$118 vs BofA Underperform HK$63 —— 真实基本面分歧 · 现 HK$137.30
- **TWSE:2408 / 2344**：MS OW NT$380（+17.3% @ 05-28）/ NT$222（+54.2% @ 05-28）· 现 NT$333 / NT$149 · fwd 5.8x / 5.6x
- **设备组**：AMAT Bernstein OP $525（+7.1% @ 06-02）· LRCX OP $340（+1.7%）· TEL GS Buy ¥62,000（+1.8% @ 06-03）· Advantest Bernstein OP ¥39,200（+55.0% @ 05-21）
- *陈旧（不入活表）*：WDC 三条均为 05-01/03（GS/UBS Neutral $400/$375 已被现价 $490.09 击穿）；Citi SK Hynix ₩310,000（05-11）疑为提取/单位异常，剔除出分歧统计。

![估值：原厂 4-9x vs 设备 30-48x 远期 P/E](../charts/theme_memory-upcycle_valuation.png)

### 卖方观点演变（Sell-side view evolution）

**美光（MU）——五家机构五周内的时间线，分歧本质是估值框架而非事实**：BofA Buy $950（05-15）→ Citi Buy $840（05-18）→ UBS Buy **$1,625**（05-26，街最高，*"EPS comfortably >$100"* through FY2029）→ Bernstein Outperform **$510**（06-02，2x 两年期 fwd BVPS——账面价值锚）→ **MS 自我修正 $520 → $1,050（+102%，06-03）** → **GS 自我修正 $400 → $900（+125%，06-08）**。一周内两家机构 PT 翻倍且新 PT 仍低于各自发布日股价——"追市"形态；真正的分歧是 MS/GS/JPM 切换到**穿越周期 EPS / P/S-on-TAM 框架**（JPM 报告副标题即 *"valuation framework transition in progress"*），而 **Bernstein 坚守账面价值锚**（同一方法给出铠侠 ¥17,000、三星 ₩225,000、海力士 ₩1,150,000，均远低于市价，[Bernstein p.8](http://xs-macbook-air.local:5001/zsxq/pdf/415284114485228/Bernstein-Global%20Memory%EF%BC%9AKIOXIA%20Investor%20Day%EF%BC%9A22%25%20bit%20CAGR%20good%20enough%EF%BC%9F-260602.pdf#page=8)）。框架之争的胜负即篮子胜负。

**铠侠（285A）——同一事件、一天内的镜像分歧**：GS Neutral ¥48,000（05-16）→ Citi Buy/High-Risk ¥73,000（05-17）→ BofA Buy ¥61,000（05-18）→ UBS 首覆 Buy ¥79,000（05-28）→ **06-02 投资者日当天：MS OW ¥110,000 vs Bernstein ¥17,000**。Bernstein 标题自带熊问：*"22% bit CAGR good enough?"*——上调后的需求锚是否已被 +3,200% 的 1Y 股价透支。

**华虹（1347.HK）——非框架性的真实分歧**：GS Buy HK$174（05-29）vs MS Equal-weight HK$118（05-28）vs Bernstein OP / Nomura Neutral HK$100（05-14）vs **BofA Underperform HK$63**（05-15）。多头定价"多年价格周期 + 激进长期收入指引"；空头定价 CXMT/YMTC 扩产后的成熟节点过剩。本窗口 −14.9% 说明市场短期站在空头一边。本窗口无任何 tracked name 出现同机构下调——PT 浪潮仍单边向上，本身即需监控的后周期信号。

## 排除标的

| Ticker | 排除原因 |
|---|---|
| NASDAQ:NVDA, NASDAQ:AVGO, NASDAQ:AMD | AI 加速器——属于存储的下游，独立的"AI Compute"主题。 |
| NYSE:PSTG, NASDAQ:NTAP | 全闪存数据中心整合商——独立的"硬件 + 软件"主题，与存储原厂的周期 β 不同。 |
| NASDAQ:KLAC, NASDAQ:PLAB, NYSE:TER | 存储敞口稀释——KLAC 制程检测对存储节点占比偏低、PLAB 光罩与 SoC 主导、TER 测试已并入 Advantest 同 bucket 选择。 |
| TWSE:Adata 3260, 5289 Innodisk, 8271 Apacer, 8299 Phison | NAND/DRAM 模组与控制器 pass-through 模型——价格上涨同步压成本，毛利率上行有限；列为 watch 名单待 NAND/DRAM 价格趋稳后再评。 |
| SZSE:002371 NAURA, SSE:688012 AMEC, SSE:688072 Piotech, SZSE:300604 Hangzhou Changchuan, SSE:688120 华海清科 | 整合至 `china-domestic-wfe` 独立主题。 |
| SZSE:300223 Ingenic | GigaDevice 已主导篮子的 A 股存储敞口。 |
| SSE:688795 摩尔线程 | GPU 标的，非存储；归入算力 / AI 加速器主题。 |
| CXMT, YMTC | 未上市，无法投资——一旦 IPO 列为篮子变动触发条件（IPO mutation trigger）。 |

## 关键词

DRAM · NAND · HBM3E / HBM4 · 合约价 / contract price · SLC NAND · NOR Flash · 12 英寸成熟节点 · YMTC / 长江存储 · CXMT / 长鑫 · WFE / 半导体资本开支 · 长期协议 / LTA · 超级周期 / supercycle · Vera Rubin · BBU · 国产替代 / domestic substitution · τ 定律 / Tau-Law

## 表现（自上次刷新：2026-05-29 → 2026-06-10）

窗口收益（yfinance `auto_adjust=True` 收盘价）：**等权篮子 −3.2% · 中位数 −4.3%**，同期 **SOX −4.9% · SOXX −4.8% · 标普 500 −4.1% · KOSPI −4.5% · 恒生 ETF −2.0% · 沪深 300 ETF −2.0%**——建仓以来首个回撤窗口，与全市场回调同步而非更差。**领涨**：Tokyo Electron **+18.0%**（¥61,830）、AMAT **+10.4%**、铠侠 +7.1%、兆易创新 +3.0%、LRCX +1.1%；**领跌**：旺宏 **−18.9%**、华虹 **−14.9%**、SK Hynix **−12.2%**、美光 −8.1%、江波龙 −7.9%、WDC −7.7%。涨跌分界与主题逻辑中的"阶段一原厂 / 阶段二设备"完全重合：原厂在 SOCAMM 噪声中回吐重定价，设备股因产能响应叙事（TEL 06-03 GS 电话会重申 WFE 需求强劲）继续上行。

![篮子窗口收益 vs 基准](../charts/theme_memory-upcycle_performance.png)

### 篮子记分卡（Basket scorecard）

| 指标 | 本窗口（05-29 → 06-10） |
|---|---|
| 上涨标的 | **5 / 16（31%）** |
| 跑赢 SOX（−4.9%） | **9 / 16（56%）** |
| 最佳贡献 | Tokyo Electron **+18.0%** |
| 最差贡献 | 旺宏 **−18.9%** |
| 等权 vs SOX | −3.2% vs −4.9% → **+170 bps** |
| 自跟踪起点（2026-05-31 基线）累计超额 | **+170 bps**（首个计量窗口） |

### 趋势背景（截至 2026-05-29 的扩容时点快照，建仓回溯参考）

价格采用 yfinance `auto_adjust=True`。本次扩容（14 → 16 只）后重算了全部基期。**篮子均值受 SNDK + Kioxia 的 spin-off / IPO 后基期效应严重抬高**——中位数（**+672.6%**）是更可靠的体感数字。

**等权篮子收益：** 3M **+69.7%** · YTD 2026 **+169.0%** · 1Y **+1,086.4%**（中位数 **+672.6%**）

**同期基准收益：**

| 基准 | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| SPY（标普 500） | +10.0% | +11.0% | +38.9% |
| ^SOX（费城半导体） | +56.5% | +74.1% | +202.9% |
| SOXX（iShares 半导体 ETF） | +59.6% | +81.5% | +210.4% |
| ^KS11（韩国综合） | +34.4% | +96.7% | +232.5% |
| 510300.SS（沪深 300 ETF） | +4.0% | +4.3% | +33.3% |

**单标的 1Y 排序（数据来源：yfinance）：**

| Ticker | 1Y | YTD | 3M | 收盘价（本币） |
|---|---|---|---|---|
| NASDAQ:SNDK | +5,152.5% | +515.8% | +160.0% | 1,694.98 |
| TSE:285A 铠侠 | +3,391.5% | +480.2% | +210.0% | 65,850 |
| NASDAQ:WDC | +1,204.1% | +183.1% | +88.3% | 531.21 |
| KRX:000660 SK 海力士 | +1,189.5% | +245.3% | +112.3% | 2,333,000 |
| NASDAQ:MU 美光 | +1,139.0% | +208.0% | +133.8% | 971.00 |
| TWSE:2344 Winbond 华邦 | +911.6% | +74.9% | +29.7% | 158.00 |
| TWSE:2408 Nanya 南亚科 *NEW* | +835.3% | +67.6% | +21.5% | 347.00 |
| TWSE:2337 Macronix 旺宏 | +696.7% | +284.1% | +51.4% | 166.50 |
| SZSE:301308 江波龙 *NEW* | +648.5% | +94.6% | +83.9% | 551.29 |
| KRX:005930 Samsung 三星 | +478.1% | +147.2% | +45.7% | 317,000 |
| HKEX:1347 华虹 | +366.9% | +98.4% | +64.8% | 161.30 |
| TSE:6857 Advantest | +359.9% | +23.8% | -6.8% | 26,170 |
| NASDAQ:LRCX | +347.8% | +72.1% | +33.3% | 318.18 |
| SSE:603986 兆易创新 | +307.1% | +98.4% | +51.2% | 467.01 |
| NASDAQ:AMAT | +201.5% | +67.8% | +19.9% | 450.06 |
| TSE:8035 Tokyo Electron | +152.1% | +43.3% | +16.8% | 52,420 |

**分布解读：** 篮子均值（+1,086%）被 SNDK + Kioxia 的 spin-off / IPO 基期效应（两者均始于 2025 中段、统计上属于"非正常基期"）严重拉高——剥离这两只看，**中位数 +673% 是更可靠的体感**——与 SOX +203% / KOSPI +233% 相比，主动篮子相对被动半导体仍有 ~440-470pp 的中位数领先，符合 *"存储原厂跑赢半导体大盘"* 的逻辑预设。**结构性观察：** DRAM/NAND 三巨头（SK Hynix、Samsung、Micron）+ 老节点专用产能（Winbond、Nanya、Macronix）的 1Y 平均 +1,007% vs 存储设备四巨头（AMAT、LRCX、TEL、Advantest）的 +265%——后者 *"先行重定价"*（2024H2 HBM TAM 提升时已升）、目前在消化前段涨幅；前者 *"现报价 in print"*，正在把合约价兑现到 P&L。对周期再加速更敏感的弹性仓位仍在 IDM 端，但设备股是周期延长（"higher-for-longer"）时回撤更可控的二阶 β。

## 近期事件

**2026-06-10 刷新窗口（05-29 → 06-10）：**

- **英伟达 Vera Rubin SoCAMM2 容量削减**（SemiAnalysis 6/4-5）：55TB → 28TB/NVL72 机柜（192GB → 96GB 模组、CPU 侧 1,536GB → 768GB）；Citi：供给约束所致、*"no change to SoCAMM2 demand"*、供应商本就只能满足约 60% 的 SoCAMM2 总需求（[Citi, zsxq #584251528855554 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/584251528855554/CITI-Global%20Semiconductors%EF%BC%9AAssessing%20the%20Impact%20of%20NVDA%E2%80%99s%20Rubin%20SoCAMM2%20Capacity%20Reduction-260607.pdf#page=1)）；JPM：96GB 模组的量补足、回调是 *"buying opportunity"*（[JPM, zsxq #584251482281424 p.1-3](http://xs-macbook-air.local:5001/zsxq/pdf/584251482281424/J.P.%20Morgan-Memory%20Market%20Update%EF%BC%9ASOCAMM%20content%20noise%20offers%20a%20buying%20opportunity%EF%BC%9B%20thoughts%20on%20NVDA~SKH%20partnership%20and%20takeaways%20from%20Computex%202026-260608.pdf#page=1)）。
- **铠侠投资者日（06-02）**：NAND bit 需求 CAGR（CY25-28）上调至 **22%**（原 20%，主要来自 eSSD）；Bernstein 反问 *"22% and JPY470B"* 是否配得上重估后的股价（[Bernstein, zsxq #415284114485228 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/415284114485228/Bernstein-Global%20Memory%EF%BC%9AKIOXIA%20Investor%20Day%EF%BC%9A22%25%20bit%20CAGR%20good%20enough%EF%BC%9F-260602.pdf#page=1)）。
- **MS《Chipflation》全球洞见（06-02）+ 投资者演示（06-08）**：存储价格一年 +6 倍；市场二元分层（AI 优先 vs 消费配给）；2027E PC/智能机缺口 −15%/−12%（−58mn 台 / −134mn 部）（[MS, zsxq #184152882245822 p.1/p.3](http://xs-macbook-air.local:5001/zsxq/pdf/184152882245822/MS-Global%20Technology%20Chipflation%20%E2%80%93%20Navigating%20A%20Memory%20Crisis-260602.pdf#page=1)）。
- **2QCY26 合约价定档（Bernstein 5 月追踪，06-02）**：DRAM +64% QoQ（PC +46 / 服务器 +53 / 手机 ~80 / 消费 ~85）；NAND 混合 ~+60%；利基 DRAM 单月 +10-20%；3Q 预期减速至 +10-20% QoQ（[zsxq #212485115581121 p.1/p.4-5](http://xs-macbook-air.local:5001/zsxq/pdf/212485115581121/Bernstein-Global%20Memory%EF%BC%9AMEMORY%20TRACKER%20%EF%BC%88May%EF%BC%89%EF%BC%9A%20Price%20hike%20c.%2060%25%20QoQ%20in%202QCY26%EF%BC%8C%20but%20likely%20at%20a%20slower%20pace%20in%202HCY26-260602.pdf#page=1)）。
- **韩国 5 月出口（GS，06-01）**：DRAM **+370% YoY**——1 月 2008 年序列开始以来纪录；NAND 芯片 +207% YoY（[zsxq #812485454488152 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485454488152/Goldman%20Sachs-South%20Korea%20Tech%EF%BC%9A%20May%202026%20export%20tracker%EF%BC%9A%20Record~high%20DRAM%20exports%20with%20370%25%20yoy%20growth-260601.pdf#page=1)）。
- **PT 上调潮写入 `/pt`**：MS 美光 $1,050 / 闪迪 $1,750（06-03）；GS 美光 $900（06-08）；BofA 闪迪 $2,100（06-08）；Bernstein 铠侠 ¥17,000 / 美光 $510（06-02）。
- **TEL 电话会（GS，06-03）**：重申 WFE 需求强劲 + 2026 年份额继续提升——窗口 +18% 背后的阶段二确认（[zsxq #812485141841252 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485141841252/Goldman%20Sachs-Tokyo%20Electron%20%EF%BC%888035.T%EF%BC%89%EF%BC%9A%20Conf.%20call%20takeaways%EF%BC%9A%20Reaffirms%20strong%20WFE%20demand%20and%20continued%20share%20gains%20in%202026-260603.pdf#page=1)）。
- **CXMT 上市进展**：05-27 过会（科创板，~¥295 亿）——IPO 触发条款进入实时跟踪（[Caixin, 2026-05-28](https://www.caixinglobal.com/2026-05-28/changxin-clears-key-hurdle-for-record-star-market-ipo-102448359.html)）。

<details><summary>建仓窗口事件存档（≤2026-05-31）</summary>

- **UBS 首次覆盖铠侠（285A.T）— Buy，PT ¥79,000**，定调 *"Peak is not here yet"*；具体路径：*"likely to rise qoq for the next six quarters before peaking in Q3 2027 (about 1.5 years)"* ([UBS — Kioxia, zsxq #812485584818522 p.1-2](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1))。是 zsxq 整批存储研报里唯一明确给出"峰值时点"的卖方判断。
- **MS《大中华区半导体——传统存储器：即将迎来超预期上涨》——华邦 + 南亚同步上调至 OW**：*"Old Memory: Upside Surprise… Winbond and Nanya to OW"*；*"We think wider supply/demand will boost earnings. SLC NAND…"* ([MS, zsxq #212451114418521 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1))。
- **UBS 美光 PT 上调至 \$1,625，EPS 长期 >\$100**——LTAs 全链条加速落地 ([UBS — MU, zsxq #585428582552154 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/585428582552154/UBS-Micron%20Technology%20Inc%20LTAs%20Gain%20Traction%3B%20PT%20to%20%241%2C625%20with%20EPS%20Remaining%20Well%20-%24100-260526.pdf#page=1) — *"LTAs Gain Traction; PT to \$1,625… EPS to remain comfortably >\$100 throughout the period"*).
- **GS 华虹半导体维持 Buy**——*"12-inch capacity increasing; AI applications drive demand and capacity utilization"* ([GS — Hua Hong, zsxq #812485541485582 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485541485582/Goldman%20Sachs-Hua%20Hong%20%EF%BC%881347.HK%EF%BC%89%EF%BC%9A%2012~inch%20capacity%20increasing%EF%BC%9B%20AI%20applications%20drive%20demand%20and%20loading%EF%BC%9B%20Buy-260529.pdf#page=1))；**MS AAI 反馈：多年价格周期 + 激进长期收入指引** ([MS — Hua Hong AAI, zsxq #212485545245181 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485545245181/Morgan%20Stanley-Hua%20Hong%20Semiconductor%20Ltd%EF%BC%881347.HK%EF%BC%89Asia%20AI%20Summit%202026%20Feedback%EF%BC%9A%20Multi~year%20Pricing%20Cycle%20and%20Aggressive%20Long~term%20Revenue%20Guidance%20in%20Focus-260528.pdf#page=1))。
- **MS 内存扩产 + 华为 τ（Tau）定律双催化**——华为 5 月 25 日发布 3D IC 突破：*"Implications of Huawei's t (Tau)-Law for WFE: On May 25, Huawei published a … 3D IC breakthrough"* ([MS, zsxq #415241112254128 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/415241112254128/MS-Greater%20China%20Semiconductors%20Double%20Catalysts%20from%20Memory%20Expansion%20and%20Huawei%27s%20t%20%28Tau%29-Law-260527.pdf#page=1))；YMTC 上海扩产同步加速。是篮子里国产存储链的双重日历催化。
- **Bernstein 中国半导体——存储产能扩张浪潮**：*"both CXMT and YMTC are forced to switch away from US supply chain… we revised up memory capex in 2027/28"* ([Bernstein, zsxq #184128224215212 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1))。把 2027/28 国产 WFE 资本开支预期上修。
- **JPM 全球存储模型上调：2028E TAM \$1.7 trillion / +37-53% revision**——DRAM/NAND 合约价 +220-250% YoY、HBM bit-CAGR +85%、三年累计资本开支 \$450bn、存储占 CSP 硬件资本开支 52% ([JPM, zsxq #184152588584282 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1))。
- **MS Winbond AAI：OW，PT NT\$222（~54% upside）**；NOR 30kwpm + SLC NAND 15kwpm 现产能，**各扩产 5kwpm（合计 +10kwpm）**；16nm DRAM 2-3K → 5K → 16K wpm 扩张路径；*"500-600 NOR chips per Vera Rubin rack"* ([MS — Winbond AAI, zsxq #812485545245422 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485545245422/Morgan%20Stanley-Winbond%20Electronics%20Corp%20%EF%BC%882344.TW%EF%BC%89Asia%20AI%20Summit%202026%20Feedback-260528.pdf#page=1))。
- **Bernstein AMAT SDC：Outperform，目标价 \$525**——逻辑 + DRAM + 先进封装合计 *"~80% of 2026 incremental WFE"*；存储原厂资本开支提速直接利好 ([Bernstein — AMAT, zsxq #212485522841821 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485522841821/Bernstein-Applied%20Materials%20%EF%BC%88AMAT.US%EF%BC%89%EF%BC%9A%20Key%20takeaways%20from%20Bernstein%27s%20SDC-260528.pdf#page=1))。
- **下游传导**：杰富瑞与 Bernstein 同周双标小米 Q1 业绩——*"Resilience on display amid memory cycle"*——存储成本压力是 Q1-Q2 毛利率最主要压制项，但能由终端价格部分承接 ([Bernstein — 小米 Q1, zsxq #585428811251444 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/585428811251444/Bernstein-Xiaomi%20Corp%EF%BC%881810.HK%EF%BC%89Xiaomi%20Q1%EF%BC%9A%20Resilience%20on%20display%20amid%20memory%20cycle%EF%BC%9B%20fundamentals%20reinforced%20%E2%80%94%20reiterate%20Outperform-260527.pdf#page=1)；[Jefferies — 小米 Q1 前瞻, zsxq #585428511282514 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/585428511282514/Jefferies-Xiaomi%EF%BC%881810.HK%EF%BC%89%EF%BC%9A1Q26%20Preview%EF%BC%9A%20Memory%20Cost%20Pressure%20Not%20Yet%20Peaked%EF%BC%9B%20Cons%20Still%20Too%20High-260525.pdf#page=1))。GS 4 月中国智能机出货 +12% YoY / +25% MoM ([zsxq #812485545248882 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485545248882/Goldman%20Sachs-China%20Smartphones%EF%BC%9A%20Apr%20shipments%20%2B12%25%20YoY%20%2B25%25%20MoM%EF%BC%9B%202Q%20memory%20cost%20pressures%20remained-260528.pdf#page=1))。
- **JPM 三星电子（005930）罢工解除**——*"Dramatic agreement closes, strike concerns largely removed; can buy on dips"* ([JPM, zsxq #812451582581222 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812451582581222/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E4%B8%89%E6%98%9F%E7%94%B5%E5%AD%90%EF%BC%88005930.KS%EF%BC%89%E6%88%8F%E5%89%A7%E6%80%A7%E5%92%8C%E8%A7%A3%E8%90%BD%E5%B9%95%EF%BC%8C%E7%BD%A2%E5%B7%A5%E6%82%AC%E8%80%8C%E6%9C%AA%E5%86%B3%E4%B8%BB%E8%A6%81%E9%97%AE%E9%A2%98%E5%9F%BA%E6%9C%AC%E6%B6%88%E9%99%A4%EF%BC%8C%E5%8F%AF%E9%80%A2%E4%BD%8E%E5%90%B8%E7%BA%B3.pdf#page=1))。

</details>

## 漂移信号

**2026-06-10 刷新：**

- **建仓时预判的"设备 vs 原厂"分化兑现——现在要判断它的含义**。设备组（TEL +18.0 / AMAT +10.4 / LRCX +1.1 / Advantest −3.6）对原厂组（−4% 至 −19%）的窗口差正在收敛 1Y 差距。若 JPM/Citi 对 SOCAMM 的"噪声"判断正确，原厂回调即买点；若内容削减扩散（更多 96GB 换 192GB、PC OEM 降配——MS 弹性表显示低端手机/PC 弹性 1.6-1.7），**"单机容量（content-per-unit）"将成为新的 de-rate 轴**，原厂上行被封顶。盯下一份 SemiAnalysis 级拆解 + 美光 06-25 指引中的 SOCAMM 措辞。
- **De-rate 量化（具名底线，非空泛提示）**：美光 $891.88 对 Bernstein 熊锚 $510（2x 两年 fwd BVPS）= **−43%**；对 MS 穿越周期公允 $1,050 = +18%——价差本身就是框架之赌。闪迪 $1,643.23 对 MS 熊案 $1,100 = **−33%**（牛案 $2,635 = +60%）。触发熊径的具名假设：**2HCY27 见顶时点**（Bernstein 与 UBS 均如此标定）提前到 2026——即 3QCY26 合约价落在 +10-20% 区间下沿或更低。
- **首个减速信号已上线**：Bernstein "2Q +60%、2H 放缓"是数据序列里第一个二阶导拐点，而篮子 1Y 中位数仍 +516%——典型的周期中后段构型。交叉验证：领先指标里韩国出口仍在创纪录——"动量 vs 二阶导"的张力是 3Q 合约价检验的核心。
- **华虹的 Justification 需要重新落地**：现有论据引 GS Buy + MS AAI 关注，但 MS 实际仅 Equal-weight（PT HK$118 低于发布日股价）、BofA 给 Underperform HK$63；本窗口 −14.9%（篮内倒数第二）。下次 mutate：要么用 CXMT/YMTC 扩产关联的新一手来源重锚 enabler 论据，要么降级 watch。
- **WDC 覆盖已陈旧**（最新 PT 05-03；现价击穿两条 Neutral 目标价）——下次刷新重拉，不引用旧 upside。
- **CXMT IPO 不再是假设**（05-27 过会）。招股书落地即触发：评估纳入（按相关度大概率前三），并重审南亚科 / 兆易创新 threat 单元——CXMT 供给正是其利基 DRAM 熊案。
- **宏观切换**：VIX 16.68 → 21.51（06-05）。"低波动支持久期下注"的建仓前提不再成立，篮子对指数回撤的 β 上升。
- **上行风险（对称列示）**：(a) 中国 CSP LTA 落签（Bernstein：仍在谈判）将延长可见性、重估原厂；(b) 美光 06-25 业绩——GS 预期指引高出街价约 $8bn；(c) NVDA-SKH 合作（JPM 06-08）落地为量的承诺。

<details><summary>建仓时点的初始观察（2026-05-31 存档）</summary>

- **基期效应 ≠ 周期再加速**：SNDK 1Y +5,152% 与 Kioxia +3,391% 是上市 / spin-off 后非正常基期形成的统计假象，应**始终在均值旁同步给出中位数（+672.6%）**——这条已写入 What's New，篮子内任何讨论都应以此为准。
- **存储设备 vs 存储原厂的领先 - 跟随关系**：设备股（AMAT、LRCX、TEL、Advantest）已在 2024H2 完成主升、目前在消化前段涨幅；原厂正在合约涨价兑现到 P&L 阶段。**风险倒置**——下一阶段若周期延长（"higher-for-longer"），设备股的二阶弹性可能反超原厂。
- **国产存储链的政策风险**：华为 τ 定律 + CXMT/YMTC 切换本土设备链的逻辑链条短期受催化推动，但 **任何美方设备管制收紧或本土设备良率不达预期** 都会迅速反向——江波龙作为下游模组代理对此最敏感（无 zsxq 单独覆盖、纯粹政策 β）。
- **HBM 接下来的供给瓶颈在哪**：JPM 模型隐含 HBM 持续紧缺，但**南亚 / Winbond 上调至 OW 的逻辑是"老节点存储被 HBM 挤压式抽走产能"**——如果 HBM 良率突破或产能扩张超预期，"挤压逻辑"反而会松弛，老节点存储溢价收窄。Q3/Q4 SK Hynix HBM4 量产读数是关键检验点。
- **下游消费端能否持续承接**：小米 Q1 毛利体感"展现韧性"是积极信号——但 GS 4 月中国智能机 +25% MoM 是节假日 + 政策刺激的合力，**6-7 月旺季后的体感才是真正的检验**。
- **Watch 名单**：Adata、Innodisk、Apacer、Phison（NAND/DRAM 模组与控制器）——pass-through 模型限制毛利上行，但**若 NAND/DRAM 合约价 Q3 后趋稳，模组商的库存周转回正可能形成第二波 β**。再评条件：合约价同比涨幅回落至 +30% 以下区间。

</details>

## 领先指标

宏观/上游信号在前（它们先于股价开裂），个股运营数据在后：

| 信号 | 最新读数 | 截至 | 方向 | 含义 |
|---|---|---|---|---|
| 韩国 DRAM 出口 | **+370% YoY——2008 年 1 月序列开始以来纪录**（[GS, zsxq #812485454488152 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/812485454488152/Goldman%20Sachs-South%20Korea%20Tech%EF%BC%9A%20May%202026%20export%20tracker%EF%BC%9A%20Record~high%20DRAM%20exports%20with%20370%25%20yoy%20growth-260601.pdf#page=1)） | 2026-05 | ↑ | 海力士/三星收入动量未减，连续 4 个月 >200% |
| 2QCY26 DRAM 合约价 QoQ | **+64%**（PC +46 / 服务器 +53 / 手机 ~80 / 消费 ~85）（[Bernstein p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485115581121/Bernstein-Global%20Memory%EF%BC%9AMEMORY%20TRACKER%20%EF%BC%88May%EF%BC%89%EF%BC%9A%20Price%20hike%20c.%2060%25%20QoQ%20in%202QCY26%EF%BC%8C%20but%20likely%20at%20a%20slower%20pace%20in%202HCY26-260602.pdf#page=1)） | 5 月合约 | ↑ 但**二阶导 ↓**（3Q 预期 +10-20%） | 3Q 印证是减速检验 |
| 2QCY26 NAND 混合合约价 QoQ | **~+60%**（手机 NAND/SSD +70-80%、晶圆 +25%）（同篇 p.4-5） | 5 月合约 | ↑ | 闪迪/铠侠 2Q ASP 顺风 |
| DRAM bit 需求（JPMe） | **+33%/+34%（2026/27E）**（[JPM p.1](http://xs-macbook-air.local:5001/zsxq/pdf/584251482281424/J.P.%20Morgan-Memory%20Market%20Update%EF%BC%9ASOCAMM%20content%20noise%20offers%20a%20buying%20opportunity%EF%BC%9B%20thoughts%20on%20NVDA~SKH%20partnership%20and%20takeaways%20from%20Computex%202026-260608.pdf#page=1)） | 06-08 | →（SOCAMM 后重申） | 需求锚扛过了内容削减惊吓 |
| 日本 HDD/SSD 渠道（4 月） | *"Continuing Strong Data Center Demand"*（[MS, zsxq #212485814114481 p.1](http://xs-macbook-air.local:5001/zsxq/pdf/212485814114481/Morgan%20Stanley-Electronic%20Components%20Apr%20HDD%20SSD%20Data%EF%BC%9A%20Continuing%20Strong%20Data%20Center%20Demand-260529.pdf#page=1)） | 2026-04 | ↑ | WDC nearline + eSSD 双确认 |

个股运营数据（各自具名来源）：**美光**——GS 预期 FY26Q3 超预期 + 8 月季指引 rev/GM/EPS $48.8bn/86.1%/$29.95 vs 街价 $40.4bn/84.0%/$23.68、~20% HBM 份额（[GS p.1](http://xs-macbook-air.local:5001/zsxq/pdf/412458524148888/GS-Micron%20Technology%20Inc.%20%28MU%29_%203Q%20Preview_%20Another%20strong%20quarter%20reflects%20extension%20of%20tight%20supply_demand%20through%202027-260608.pdf#page=1)）；**铠侠**——bit CAGR 22%（CY25-28）+ FY27 资本开支 ¥450bn；**闪迪**——>60% NAND 供给仍可随行就市重定价、BofA F27 rev/EPS $44bn/$188；**华邦**——NOR 30k+10k wpm / SLC NAND 15k+10k wpm 扩产、16nm DRAM 2-3K→5K→16K wpm、500-600 颗 NOR/Vera Rubin 机柜；**南亚科**——利基 DRAM 5 月合约价 +10-20% MoM（其主营品类）；**TEL**——GM 45%→50%（FY28 路径）+ GS 电话会重申。

## 未来催化剂（未来 3–6 个月）

- **美光 FY26Q3 业绩 + 8 月季指引（2026-06-25）**——（涨价兑现 → 服务器/AI DRAM 摆动桶；GS 预期指引高出街价约 $8bn；SOCAMM 措辞是 content-per-unit 的风向标）——**最近的有日期催化剂，并对海力士/三星形成 read-across**。
- **3QCY26 合约价印证（7-9 月）**——（减速检验：Bernstein 模型 +10-20% QoQ；高于区间 = 周期延长，低于 = 2HCY27 见顶前移 → 全体原厂的 de-rate 轴）。
- **HBM4 量产时点**：SK Hynix Q3 业绩、Samsung Q3 业绩——HBM4 良率与量产 timeline 是 2026H2-2027H1 的核心定价变量。
- **JPM 全球存储模型 Q3 update**——TAM 上修后的关键检验点：DRAM/NAND 合约价 Q2 印证、HBM bit shipment Q2 印证。
- **铠侠 FY26 Q1 业绩（2026 年 7-8 月发布）**——UBS PT ¥79,000 隐含的 6 季度 QoQ 增长的第一季印证。
- **CXMT / YMTC 资本开支 + 国产设备订单**——Bernstein 把 2027/28 资本开支上修，本土设备股（独立主题）的订单印证；江波龙作为下游配套代理同步跟踪。
- **三星电子 HBM4 客户认证**——是否能从 SK Hynix 手中夺回 HBM 份额是 Samsung 的核心 catch-up 变量。
- **华虹 12 英寸 HH9 产能爬坡**——AI 应用占比从目前 ~15% 提升至 2027E ~25%+ 的路径印证（MS AAI 提及的"激进长期收入指引"）。

## Data Used / 数据来源清单

**市场数据**
- yfinance `auto_adjust=True`：2026-06-10 拉取（刷新窗口锚定 2026-05-29 收盘）；估值 `.info`（fwd P/E、市值）同日拉取。建仓时点快照（趋势背景小节）系 2026-05-31 拉取。
- 基准：SPY（标普 500）、^SOX（费城半导体）、SOXX、^KS11（韩国综合）、2800.HK（恒生 ETF）、510300.SS（沪深 300 ETF）。

**本次刷新新增 zsxq 报告（2026-06-10，11 份；2 份先 OCR）**
- [MS — Chipflation 06-02 (#184152882245822)](http://xs-macbook-air.local:5001/zsxq/pdf/184152882245822/MS-Global%20Technology%20Chipflation%20%E2%80%93%20Navigating%20A%20Memory%20Crisis-260602.pdf#page=1) + [投资者演示 06-08 (#412458811521158)](http://xs-macbook-air.local:5001/zsxq/pdf/412458811521158/Morgan%20Stanley-Investor%20Presentation%EF%BC%9A%20Global%20Technology%EF%BC%8CChipflation-260608.pdf) — 价格 +6 倍 / 2027 消费缺口建模。
- [Bernstein — Memory Tracker May (#212485115581121, OCR)](http://xs-macbook-air.local:5001/zsxq/pdf/212485115581121/Bernstein-Global%20Memory%EF%BC%9AMEMORY%20TRACKER%20%EF%BC%88May%EF%BC%89%EF%BC%9A%20Price%20hike%20c.%2060%25%20QoQ%20in%202QCY26%EF%BC%8C%20but%20likely%20at%20a%20slower%20pace%20in%202HCY26-260602.pdf#page=1) — 2Q 合约价定档 + 3Q 减速预期。
- [MS — 北美存储 PT 上调 (#585412884821284)](http://xs-macbook-air.local:5001/zsxq/pdf/585412884821284/MS-Semiconductors%20-%20North%20America%20Raising%20estimates-PTs%20for%20memory%20stocks%20as%20demand%20continues%20to%20outpace%20supply-260603.pdf#page=1) + [MS — 闪迪 Risk Reward (#184155215151842)](http://xs-macbook-air.local:5001/zsxq/pdf/184155215151842/Morgan%20Stanley-SanDisk%20Corporation.%EF%BC%88SNDK.US%EF%BC%89Risk%20Reward%20Update-260603.pdf#page=2) — MU/SNDK PT + 牛基熊三案。
- [GS — 美光 3Q 前瞻 (#412458524148888)](http://xs-macbook-air.local:5001/zsxq/pdf/412458524148888/GS-Micron%20Technology%20Inc.%20%28MU%29_%203Q%20Preview_%20Another%20strong%20quarter%20reflects%20extension%20of%20tight%20supply_demand%20through%202027-260608.pdf#page=1) · [BofA — 闪迪 PO $2,100 (#181245182285222)](http://xs-macbook-air.local:5001/zsxq/pdf/181245182285222/Bofa-Sandisk%20Corporation%20Supply-Demand%20balance%20remains%20tight%2C%20pricing%20strong%3B%20PO%20to%20%242100-260608.pdf#page=1) · [Bernstein — 铠侠投资者日 (#415284114485228)](http://xs-macbook-air.local:5001/zsxq/pdf/415284114485228/Bernstein-Global%20Memory%EF%BC%9AKIOXIA%20Investor%20Day%EF%BC%9A22%25%20bit%20CAGR%20good%20enough%EF%BC%9F-260602.pdf#page=1)。
- [JPM — SOCAMM 更新 (#584251482281424)](http://xs-macbook-air.local:5001/zsxq/pdf/584251482281424/J.P.%20Morgan-Memory%20Market%20Update%EF%BC%9ASOCAMM%20content%20noise%20offers%20a%20buying%20opportunity%EF%BC%9B%20thoughts%20on%20NVDA~SKH%20partnership%20and%20takeaways%20from%20Computex%202026-260608.pdf#page=1) · [Citi — Rubin SoCAMM2 (#584251528855554, OCR)](http://xs-macbook-air.local:5001/zsxq/pdf/584251528855554/CITI-Global%20Semiconductors%EF%BC%9AAssessing%20the%20Impact%20of%20NVDA%E2%80%99s%20Rubin%20SoCAMM2%20Capacity%20Reduction-260607.pdf#page=1) · [GS — 韩国 5 月出口 (#812485454488152)](http://xs-macbook-air.local:5001/zsxq/pdf/812485454488152/Goldman%20Sachs-South%20Korea%20Tech%EF%BC%9A%20May%202026%20export%20tracker%EF%BC%9A%20Record~high%20DRAM%20exports%20with%20370%25%20yoy%20growth-260601.pdf#page=1)。
- 每个载重数字均与提取后的原文逐字核对；翻译精华仅作筛选。

**写入的数据存储（Tier-2 helper）**
- `stock_price_target_db` — 本次刷新经 `scripts/persist_pts.py --replace` 写入 **6 条 PT**（MS MU $1,050 / MS SNDK $1,750 / GS MU $900 / BofA SNDK $2,100 / Bernstein 铠侠 ¥17,000 / Bernstein MU $510），`/pt` 可见。

**图表（本次刷新渲染，4 张，图内均带来源脚注）**
- [theme_memory-upcycle_anchor.png](../charts/theme_memory-upcycle_anchor.png) — JPM TAM 新旧模型对比 + 子桶驱动。
- [theme_memory-upcycle_performance.png](../charts/theme_memory-upcycle_performance.png) — 窗口个股收益 vs 等权/SOX/SPY 线。
- [theme_memory-upcycle_valuation.png](../charts/theme_memory-upcycle_valuation.png) — 原厂 vs 设备远期 P/E + MS 穿越周期参考线。
- [theme_memory-upcycle_sd_balance.png](../charts/theme_memory-upcycle_sd_balance.png) — 2027E 消费端存储需求 vs 配给后供给（MS 充足度框架）。

**zsxq 报告（按 file_id；每个数字均已对 OCR 后原文逐字核对，附 PDF 页码）**

主题级 / 模型设定：
- [JPM — Global Memory: Bigger TAM Yet (zsxq #184152588584282)](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1) p41 — 2028E TAM \$1.7T / +37-53% / DRAM-NAND +220-250% / HBM-CAGR 85% / \$450bn 3-yr capex / 52% CSP capex。
- [JPM 副本 (zsxq #212485541484181)](http://xs-macbook-air.local:5001/zsxq/pdf/212485541484181/J.P.%20Morgan-Global%20Memory%20Market-CPU%20adds%20fuel%20to%20the%20%E2%80%98higher%20and%20longer%E2%80%99%20upcycle%20thesis%20and%2028E%20TAM%20at%20%241.7trn%3B%20valuation%20framework%20transition%20in%20progress-260529.pdf#page=1) p41 — 同上。
- [MS — Old Memory: Upside Surprise (zsxq #212451114418521)](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1) p27 — Winbond + Nanya 上调至 OW，SLC NAND 紧缺逻辑。
- [MS — Memory Expansion + Huawei τ-Law (zsxq #415241112254128)](http://xs-macbook-air.local:5001/zsxq/pdf/415241112254128/MS-Greater%20China%20Semiconductors%20Double%20Catalysts%20from%20Memory%20Expansion%20and%20Huawei%27s%20t%20%28Tau%29-Law-260527.pdf#page=1) p34 — YMTC 上海扩产加速 + Huawei 3D IC 5/25 突破。
- [Bernstein — China Semicap: Memory Capacity Expansion (zsxq #184128224215212)](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1) p19 — CXMT/YMTC 切换本土设备链，2027/28 资本开支上修。
- [JPM — CPU/Agentic AI (zsxq #212485811841111)](http://xs-macbook-air.local:5001/zsxq/pdf/212485811841111/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A1%8C%E4%B8%9A%E4%B8%93%E9%A2%98%E7%A0%94%E7%A9%B6%EF%BC%9A%E6%8E%A8%E7%90%86%E4%B8%8EAgentic%20AI%E6%B5%AA%E6%BD%AE%E4%B8%8B%EF%BC%8CCPU%E9%87%8D%E5%9B%9EAI%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E6%A0%B8%E5%BF%83%E4%B8%AD%E6%9E%A2.pdf#page=1) p36 — CPU 回到 AI 基础设施核心，存储 / 内存配比放大。

单标的 / 单事件：
- [UBS — Kioxia Initiation: Peak is not here yet (zsxq #812485584818522)](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1) p41 — Kioxia Buy PT ¥79,000，周期 2027 Q3 见顶。
- [MS — Kioxia 2026 Japan Summit (zsxq #415241445451248)](http://xs-macbook-air.local:5001/zsxq/pdf/415241445451248/Morgan%20Stanley-KIOXIA%20Holdings%20%EF%BC%88285A.T%EF%BC%89Japan%20Summit%202026%20Feedback-260521.pdf#page=1) p14 — Kioxia PT ¥70,000。
- [UBS — Micron LTAs to \$1,625 (zsxq #585428582552154)](http://xs-macbook-air.local:5001/zsxq/pdf/585428582552154/UBS-Micron%20Technology%20Inc%20LTAs%20Gain%20Traction%3B%20PT%20to%20%241%2C625%20with%20EPS%20Remaining%20Well%20-%24100-260526.pdf#page=1) p28 — Micron PT \$1,625，LTAs / EPS >\$100。
- [GS — Hua Hong 12-inch (zsxq #812485541485582)](http://xs-macbook-air.local:5001/zsxq/pdf/812485541485582/Goldman%20Sachs-Hua%20Hong%20%EF%BC%881347.HK%EF%BC%89%EF%BC%9A%2012~inch%20capacity%20increasing%EF%BC%9B%20AI%20applications%20drive%20demand%20and%20loading%EF%BC%9B%20Buy-260529.pdf#page=1) p10 — Buy；12 英寸 + AI 应用驱动产能利用率。
- [MS — Hua Hong AAI (zsxq #212485545245181)](http://xs-macbook-air.local:5001/zsxq/pdf/212485545245181/Morgan%20Stanley-Hua%20Hong%20Semiconductor%20Ltd%EF%BC%881347.HK%EF%BC%89Asia%20AI%20Summit%202026%20Feedback%EF%BC%9A%20Multi~year%20Pricing%20Cycle%20and%20Aggressive%20Long~term%20Revenue%20Guidance%20in%20Focus-260528.pdf#page=1) p8 — 多年价格周期 + 激进长期收入指引。
- [MS — Winbond AAI (zsxq #812485545245422)](http://xs-macbook-air.local:5001/zsxq/pdf/812485545245422/Morgan%20Stanley-Winbond%20Electronics%20Corp%20%EF%BC%882344.TW%EF%BC%89Asia%20AI%20Summit%202026%20Feedback-260528.pdf#page=1) p8 — OW PT NT\$222、NOR/NAND 产能扩张、Vera Rubin NOR 用量。
- [Bernstein — AMAT SDC (zsxq #212485522841821)](http://xs-macbook-air.local:5001/zsxq/pdf/212485522841821/Bernstein-Applied%20Materials%20%EF%BC%88AMAT.US%EF%BC%89%EF%BC%9A%20Key%20takeaways%20from%20Bernstein%27s%20SDC-260528.pdf#page=1) p15 — AMAT Outperform PT \$525。
- [JPM — Samsung Electronics: Strike resolution (zsxq #812451582581222)](http://xs-macbook-air.local:5001/zsxq/pdf/812451582581222/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E4%B8%89%E6%98%9F%E7%94%B5%E5%AD%90%EF%BC%88005930.KS%EF%BC%89%E6%88%8F%E5%89%A7%E6%80%A7%E5%92%8C%E8%A7%A3%E8%90%BD%E5%B9%95%EF%BC%8C%E7%BD%A2%E5%B7%A5%E6%82%AC%E8%80%8C%E6%9C%AA%E5%86%B3%E4%B8%BB%E8%A6%81%E9%97%AE%E9%A2%98%E5%9F%BA%E6%9C%AC%E6%B6%88%E9%99%A4%EF%BC%8C%E5%8F%AF%E9%80%A2%E4%BD%8E%E5%90%B8%E7%BA%B3.pdf#page=1) p10 — 罢工和解 / 可逢低吸纳。
- [MS — Semicap Equipment Japan (zsxq #184152218151852)](http://xs-macbook-air.local:5001/zsxq/pdf/184152218151852/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9AJapan%20Takeaways-260529.pdf#page=1) p7 — Kioxia FY27 capex ¥450bn / TEL GM 45%→50% by FY28。
- [MS — Semicap Equipment Taiwan (zsxq #415284812111518)](http://xs-macbook-air.local:5001/zsxq/pdf/415284812111518/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9ATaiwan%20Takeaways-260529.pdf#page=1) p7 — 测试瓶颈定调。
- [MS — Photronics (zsxq #415284812112558)](http://xs-macbook-air.local:5001/zsxq/pdf/415284812112558/Morgan%20Stanley-Semiconductor%20Production%20Equipment%EF%BC%9AImplications%20from%20Photronics%27%20Feb~Apr%20Results-260529.pdf#page=1) p5 — 光罩需求印证（剔除出篮子但保留为周期信号）。
- [GS — China Smartphone Apr (zsxq #812485545248882)](http://xs-macbook-air.local:5001/zsxq/pdf/812485545248882/Goldman%20Sachs-China%20Smartphones%EF%BC%9A%20Apr%20shipments%20%2B12%25%20YoY%20%2B25%25%20MoM%EF%BC%9B%202Q%20memory%20cost%20pressures%20remained-260528.pdf#page=1) p13 — 4 月出货 +12% YoY / +25% MoM。

下游传导：
- [Bernstein — Xiaomi Q1 Memory Cycle Resilience (zsxq #585428811251444)](http://xs-macbook-air.local:5001/zsxq/pdf/585428811251444/Bernstein-Xiaomi%20Corp%EF%BC%881810.HK%EF%BC%89Xiaomi%20Q1%EF%BC%9A%20Resilience%20on%20display%20amid%20memory%20cycle%EF%BC%9B%20fundamentals%20reinforced%20%E2%80%94%20reiterate%20Outperform-260527.pdf#page=1) p21 — Xiaomi Q1 体感韧性。
- [Jefferies — Xiaomi Q1 Preview (zsxq #585428511282514)](http://xs-macbook-air.local:5001/zsxq/pdf/585428511282514/Jefferies-Xiaomi%EF%BC%881810.HK%EF%BC%89%EF%BC%9A1Q26%20Preview%EF%BC%9A%20Memory%20Cost%20Pressure%20Not%20Yet%20Peaked%EF%BC%9B%20Cons%20Still%20Too%20High-260525.pdf#page=1) p19 — 存储成本压力。

历史交叉（保留以备后续 refresh 增量）：
- [Moore Threads (zsxq #184152212118182)](http://xs-macbook-air.local:5001/zsxq/pdf/184152212118182/%E6%91%A9%E5%B0%94%E7%BA%BF%E7%A8%8B-U%28688795%29%E6%B7%B1%E5%BA%A6%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A%EF%BC%9A%E5%85%A8%E6%A0%88%E5%BC%95%E9%A2%86%EF%BC%8C%E6%99%BA%E7%AE%97%E7%A0%B4%E5%B1%80.pdf#page=1) p42 — A 股 GPU 标的，篮子外但属同一 AI 计算供应链。
- [JPM 迈为股份 (zsxq #812485814114252)](http://xs-macbook-air.local:5001/zsxq/pdf/812485814114252/J.P.%20Morgan-Maxwell%20~A%EF%BC%88300751%EF%BC%89While%20orders%20improve%EF%BC%8C%20share%20price%20has%20priced~in%20blue%20sky%20scenario%EF%BC%9B%20maintain%20UW-260529.pdf#page=1) p12 — 减持评级，半导体设备 IDM 端二阶逻辑。
- [MS Synopsys (zsxq #812485522841582)](http://xs-macbook-air.local:5001/zsxq/pdf/812485522841582/Morgan%20Stanley-Synopsys%20Inc%EF%BC%88SNPS.US%EF%BC%892027%20Set~up%20Yet%20to%20Emerge-260528.pdf#page=1) p15 — EDA 周期 / 估值压力，非存储但同 AI 半导体链。

**已剔除的来源**：file_id 812485545245152（MS 同仁堂 600085——非存储；原版本曾误标为"MS Hua Hong AAI"，已纠正）。

**宏观背景（来自 indicators.db，2026-06-05 最新值）**
- VIX **21.51**（建仓时 16.68——低波动前提已失效）/ TNX 4.536% / DXY 100.07 / HYG 79.43。

**stale notice / 覆盖缺口**
- 江波龙（SZSE:301308）在 zsxq 整批存储研报中无单独研究覆盖，仅出现在分析师覆盖名单中——列为 adjacent 而非 core，理由透明披露。
- HBM4 量产 timeline 与三星 catch-up timeline 是篮子的核心 EPS swing variable，但 zsxq 库目前没有专项前瞻——下次 refresh 应主动检索。

## 参考来源

- [JPM Global Memory zsxq #184152588584282](http://xs-macbook-air.local:5001/zsxq/pdf/184152588584282/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E5%85%A8%E7%90%83%E5%AD%98%E5%82%A8%E5%B8%82%E5%9C%BA%EF%BC%9ACPU%E4%B8%BA%E6%9B%B4%E9%AB%98%E6%9B%B4%E4%B9%85%E7%9A%84%E4%B8%8A%E8%A1%8C%E5%91%A8%E6%9C%9F%E6%B7%BB%E6%9F%B4%E5%8A%A0%E8%96%AA%EF%BC%8C2028%E5%B9%B4%E6%80%BB%E6%BD%9C%E5%9C%A8%E5%B8%82%E5%9C%BA%E8%A7%84%E6%A8%A1%E8%BE%BE1.7%E4%B8%87%E4%BA%BF%E7%BE%8E%E5%85%83%EF%BC%9B%E4%BC%B0%E5%80%BC%E6%A1%86%E6%9E%B6%E8%BD%AC%E5%9E%8B%E8%BF%9B%E8%A1%8C%E6%97%B6-260529.pdf#page=1)
- [JPM Global Memory 副本 zsxq #212485541484181](http://xs-macbook-air.local:5001/zsxq/pdf/212485541484181/J.P.%20Morgan-Global%20Memory%20Market-CPU%20adds%20fuel%20to%20the%20%E2%80%98higher%20and%20longer%E2%80%99%20upcycle%20thesis%20and%2028E%20TAM%20at%20%241.7trn%3B%20valuation%20framework%20transition%20in%20progress-260529.pdf#page=1)
- [MS Old Memory: Upside Surprise zsxq #212451114418521](http://xs-macbook-air.local:5001/zsxq/pdf/212451114418521/MS-Greater%20China%20Semiconductors%20-%20Asia%20Pacific%20Old%20Memory-Upside%20Surprise%20%20Ahead-260528.pdf#page=1)
- [MS Memory Expansion + Huawei τ zsxq #415241112254128](http://xs-macbook-air.local:5001/zsxq/pdf/415241112254128/MS-Greater%20China%20Semiconductors%20Double%20Catalysts%20from%20Memory%20Expansion%20and%20Huawei%27s%20t%20%28Tau%29-Law-260527.pdf#page=1)
- [Bernstein China Semicap: Memory zsxq #184128224215212](http://xs-macbook-air.local:5001/zsxq/pdf/184128224215212/Bernstein-China%20Semiconductors%20China%20Semicap%EF%BC%9A%20The%20surging%20memory%20capacity%20expansion-260521.pdf#page=1)
- [JPM CPU/Agentic AI zsxq #212485811841111](http://xs-macbook-air.local:5001/zsxq/pdf/212485811841111/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A1%8C%E4%B8%9A%E4%B8%93%E9%A2%98%E7%A0%94%E7%A9%B6%EF%BC%9A%E6%8E%A8%E7%90%86%E4%B8%8EAgentic%20AI%E6%B5%AA%E6%BD%AE%E4%B8%8B%EF%BC%8CCPU%E9%87%8D%E5%9B%9EAI%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E6%A0%B8%E5%BF%83%E4%B8%AD%E6%9E%A2.pdf#page=1)
- [UBS Kioxia Initiation zsxq #812485584818522](http://xs-macbook-air.local:5001/zsxq/pdf/812485584818522/UBS-Kioxia%20Holdings%20Corp%20Peak%20is%20not%20here%20yet-260528.pdf#page=1)
- [MS Kioxia 2026 Japan Summit zsxq #415241445451248](http://xs-macbook-air.local:5001/zsxq/pdf/415241445451248/Morgan%20Stanley-KIOXIA%20Holdings%20%EF%BC%88285A.T%EF%BC%89Japan%20Summit%202026%20Feedback-260521.pdf#page=1)
- [UBS Micron LTAs zsxq #585428582552154](http://xs-macbook-air.local:5001/zsxq/pdf/585428582552154/UBS-Micron%20Technology%20Inc%20LTAs%20Gain%20Traction%3B%20PT%20to%20%241%2C625%20with%20EPS%20Remaining%20Well%20-%24100-260526.pdf#page=1)
- [GS Hua Hong 12-inch zsxq #812485541485582](http://xs-macbook-air.local:5001/zsxq/pdf/812485541485582/Goldman%20Sachs-Hua%20Hong%20%EF%BC%881347.HK%EF%BC%89%EF%BC%9A%2012~inch%20capacity%20increasing%EF%BC%9B%20AI%20applications%20drive%20demand%20and%20loading%EF%BC%9B%20Buy-260529.pdf#page=1)
- [MS Hua Hong AAI zsxq #212485545245181](http://xs-macbook-air.local:5001/zsxq/pdf/212485545245181/Morgan%20Stanley-Hua%20Hong%20Semiconductor%20Ltd%EF%BC%881347.HK%EF%BC%89Asia%20AI%20Summit%202026%20Feedback%EF%BC%9A%20Multi~year%20Pricing%20Cycle%20and%20Aggressive%20Long~term%20Revenue%20Guidance%20in%20Focus-260528.pdf#page=1)
- [MS Winbond AAI zsxq #812485545245422](http://xs-macbook-air.local:5001/zsxq/pdf/812485545245422/Morgan%20Stanley-Winbond%20Electronics%20Corp%20%EF%BC%882344.TW%EF%BC%89Asia%20AI%20Summit%202026%20Feedback-260528.pdf#page=1)
- [Bernstein AMAT SDC zsxq #212485522841821](http://xs-macbook-air.local:5001/zsxq/pdf/212485522841821/Bernstein-Applied%20Materials%20%EF%BC%88AMAT.US%EF%BC%89%EF%BC%9A%20Key%20takeaways%20from%20Bernstein%27s%20SDC-260528.pdf#page=1)
- [JPM Samsung Strike Resolution zsxq #812451582581222](http://xs-macbook-air.local:5001/zsxq/pdf/812451582581222/%E6%91%A9%E6%A0%B9%E5%A4%A7%E9%80%9A-%E4%B8%89%E6%98%9F%E7%94%B5%E5%AD%90%EF%BC%88005930.KS%EF%BC%89%E6%88%8F%E5%89%A7%E6%80%A7%E5%92%8C%E8%A7%A3%E8%90%BD%E5%B9%95%EF%BC%8C%E7%BD%A2%E5%B7%A5%E6%82%AC%E8%80%8C%E6%9C%AA%E5%86%B3%E4%B8%BB%E8%A6%81%E9%97%AE%E9%A2%98%E5%9F%BA%E6%9C%AC%E6%B6%88%E9%99%A4%EF%BC%8C%E5%8F%AF%E9%80%A2%E4%BD%8E%E5%90%B8%E7%BA%B3.pdf#page=1)
- [MS Semicap Japan zsxq #184152218151852](http://xs-macbook-air.local:5001/zsxq/pdf/184152218151852/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9AJapan%20Takeaways-260529.pdf#page=1)
- [MS Semicap Taiwan zsxq #415284812111518](http://xs-macbook-air.local:5001/zsxq/pdf/415284812111518/Morgan%20Stanley-Semiconductor%20Capital%20Equipment%EF%BC%9ATaiwan%20Takeaways-260529.pdf#page=1)
- [MS Photronics zsxq #415284812112558](http://xs-macbook-air.local:5001/zsxq/pdf/415284812112558/Morgan%20Stanley-Semiconductor%20Production%20Equipment%EF%BC%9AImplications%20from%20Photronics%27%20Feb~Apr%20Results-260529.pdf#page=1)
- [GS China Smartphone zsxq #812485545248882](http://xs-macbook-air.local:5001/zsxq/pdf/812485545248882/Goldman%20Sachs-China%20Smartphones%EF%BC%9A%20Apr%20shipments%20%2B12%25%20YoY%20%2B25%25%20MoM%EF%BC%9B%202Q%20memory%20cost%20pressures%20remained-260528.pdf#page=1)
- [Bernstein Xiaomi Q1 Memory zsxq #585428811251444](http://xs-macbook-air.local:5001/zsxq/pdf/585428811251444/Bernstein-Xiaomi%20Corp%EF%BC%881810.HK%EF%BC%89Xiaomi%20Q1%EF%BC%9A%20Resilience%20on%20display%20amid%20memory%20cycle%EF%BC%9B%20fundamentals%20reinforced%20%E2%80%94%20reiterate%20Outperform-260527.pdf#page=1)
- [Jefferies Xiaomi Q1 Preview zsxq #585428511282514](http://xs-macbook-air.local:5001/zsxq/pdf/585428511282514/Jefferies-Xiaomi%EF%BC%881810.HK%EF%BC%89%EF%BC%9A1Q26%20Preview%EF%BC%9A%20Memory%20Cost%20Pressure%20Not%20Yet%20Peaked%EF%BC%9B%20Cons%20Still%20Too%20High-260525.pdf#page=1)
- [Moore Threads zsxq #184152212118182](http://xs-macbook-air.local:5001/zsxq/pdf/184152212118182/%E6%91%A9%E5%B0%94%E7%BA%BF%E7%A8%8B-U%28688795%29%E6%B7%B1%E5%BA%A6%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A%EF%BC%9A%E5%85%A8%E6%A0%88%E5%BC%95%E9%A2%86%EF%BC%8C%E6%99%BA%E7%AE%97%E7%A0%B4%E5%B1%80.pdf#page=1)
- [JPM 迈为股份 zsxq #812485814114252](http://xs-macbook-air.local:5001/zsxq/pdf/812485814114252/J.P.%20Morgan-Maxwell%20~A%EF%BC%88300751%EF%BC%89While%20orders%20improve%EF%BC%8C%20share%20price%20has%20priced~in%20blue%20sky%20scenario%EF%BC%9B%20maintain%20UW-260529.pdf#page=1)
- [MS Synopsys zsxq #812485522841582](http://xs-macbook-air.local:5001/zsxq/pdf/812485522841582/Morgan%20Stanley-Synopsys%20Inc%EF%BC%88SNPS.US%EF%BC%892027%20Set~up%20Yet%20to%20Emerge-260528.pdf#page=1)

## 历史

- 2026-05-31 — 篮子建立（14 只标的：8 core / 6 enabler），基于 zsxq 翻译精华摘要。
- 2026-05-31 — 第一次 refresh + 扩容 14→16（添加南亚科 2408.TW core、江波龙 301308.SZ adjacent）；全部 22 份 zsxq 引用换为 OCR 原文，每个数字附 PDF 页码 + 原文逐字引用；纠正一处 file_id 812485545245152 的误标（实为 MS 同仁堂，已剔除）；中文版同步建立。
- 2026-06-10 — 刷新 + 格式升级：中英两份文件同步至最新主题规范（What's New 倒序归档、估值快照 + 卖方观点演变、篮子记分卡、领先指标表、4 张图表、ticker 前缀 KRX/TSE/TWSE/HKEX 规范化）；英文版补齐 5-31 扩容内容（此前仅落中文版）；新挖 11 份 zsxq 报告；6 条 PT 写入 `/pt`；SOCAMM 事件 + 首个合约价减速信号记入漂移观察。

<details><summary>Verification log (Step 7) — 2026-06-10</summary>

- 元数据行解析 ✓（Last refreshed 2026-06-10；en, zh）；Tracked tickers 表 16 行 × 5 列 ✓，全部 ticker 前缀符合 KRX/TSE/TWSE/HKEX/NASDAQ/SSE/SZSE 规范（TYO:×6、TPE:×6 已替换）。
- snapshot sidecar：2026-06-10 新行 JSON 合法 ✓、ticker 集与本表一致（16/16，规范前缀）✓（sidecar 为中英共享，验证记录见英文版日志）。
- 业绩抽查 vs yfinance：TEL +18.0%、SK Hynix −12.2%、旺宏 −18.9%、等权 −3.2% ✓。
- 数字→原文逐字核对（≥5，其中 ≥2 来自 OCR 原文）：64%/46%/53%/~80%/~85%（#212485115581121 p.1，OCR）✓；$1,050/29.5x/$35（#585412884821284）✓；PO $2,100 / $199（#181245182285222）✓；+370% yoy / January 2008（#812485454488152）✓；22% CAGR / ¥17,000 / $510（#415284114485228）✓；12-15% short / 58mn / 134mn / 19bn Gb（#184152882245822）✓；牛 $2,635 / 熊 $1,100（#184155215151842 p.2）✓。
- URL 检查：2 条 zsxq 直链文件名与 find_pdf.py `pdf_url` 逐字一致 ✓（#585412884821284、#212485115581121）；SK hynix 新闻室 200 ✓；YouTube 7J7X7aZvMXQ 200 + 可播放 ✓。
- 图表 4 张（anchor / performance / valuation / sd_balance），图内来源脚注齐备，已逐张内嵌于所属小节并列入 Data Used ✓。
- 写入存储：`stock_price_target_db` +6 条（persist_pts.py --replace；3 insert / 3 replace）。
- 残留未知：MS Old-Memory readacross（#812488554854482）PDF 不在本地盘——未引用，下次刷新补挖；WDC PT 行陈旧（已隔离）；Citi SK Hynix ₩310k 疑异常（已剔除并标记）。

</details>
