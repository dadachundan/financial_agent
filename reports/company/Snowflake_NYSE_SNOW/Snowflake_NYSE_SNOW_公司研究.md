# 公司研究报告: Snowflake Inc. (NYSE: SNOW)

**日期:** 2026-05-29 (依据 FY27 Q1 业绩更新)
**作者:** financial_agent / company-research skill
**代码:** NYSE: SNOW
**财年截止:** 1 月 31 日 (FY26 = 截至 2026 年 1 月 31 日的财年; Q1 FY27 = 截至 2026 年 4 月 30 日的三个月)
**报告语言: 简体中文 (英文版同时存在于本目录)**

> **更新——Q1 FY27 业绩 + 全年指引上调 (2026-05-27):** Snowflake 录得**产品营业收入 13.343 亿美元 (同比 +34%)** —— CEO Sridhar Ramaswamy 称之为"公司历史上最强的环比美元金额增长" —— 总营业收入 **13.9 亿美元 (同比 +33%)**, **净美元留存率 (NRR) 126%** (环比扩张), **TTM 产品营业收入超过 100 万美元的客户达 779 家 (同比 +29%, 季度净增 46 家, 去年同期为 26 家)**, **Forbes Global 2000 客户 813 家**, **剩余履约义务 (RPO) 92.1 亿美元 (同比 +38%)**。季度净增客户 616 家 (同比 +38%), 其中 G2000 新增 13 家。AI 普及度指标 (2026 年 4 月末四周滚动平均): **逾 13,600 个账户**使用 Snowflake AI 能力; **Snowflake Intelligence 账户环比翻倍以上**; **Cortex Code 在逾 7,100 个账户中使用**。季内战略行动: **AWS 多年合约扩容至 60 亿美元**以加速企业 AI; 深化与 **OpenAI** 的联合创新; 将 SAP 合作正式落地 (GA); 并于 2026 年 5 月签署最终协议收购 **Natoma** —— 一家面向 AI Agent 的企业级模型上下文协议 (Model Context Protocol, MCP) 平台。基于上述, 管理层**上调全年 FY27 指引**: **产品营业收入由 56.60 亿美元 (+27%) 上调至 58.40 亿美元 (+31%)**; **非 GAAP 营业利润率由 12.5% 上调至 13.5%**; 非 GAAP 产品毛利率维持 75%; 调整后 FCF 利润率维持 23%。**Q2 FY27 指引: 产品营业收入 14.15–14.20 亿美元 (同比 +30%)**, 非 GAAP 营业利润率 12.5%。Q1 GAAP 营业亏损 3.262 亿美元 (-23.4% 营收占比); 非 GAAP 营业利润 1.658 亿美元 (11.9%); 经营性现金流 2.432 亿美元; 自由现金流 2.328 亿美元; 调整后 FCF 2.655 亿美元。来源: [Snowflake Q1-FY27 业绩新闻稿, 2026-05-27](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm)。
>
> **前次横幅——FY2027 指引启动并重申 (2026-02-25, 于 2026-03-31 再次确认):** 管理层最初启动 FY27 全年**产品营业收入指引为 56.60 亿美元 (同比 +27%)**, 非 GAAP 营业利润率 12.5%, 非 GAAP 产品毛利率 75%, 非 GAAP 调整后 FCF 利润率 23%。Q1 FY27 业绩 + AI / G2000 势头触发了上述上调。来源: [Snowflake Q4-FY2026 业绩新闻稿, 2026-02-25](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm)。

## 目录
1. 公司概览
2. 公司历史
3. 管理团队
4. 产品与服务
5. 客户与上市策略
6. 行业概览
7. 竞争格局
8. 市场机会 (TAM)
9. 风险评估
10. 参考资料

---

## 1. 公司概览

Snowflake Inc. 是总部位于美国加州门洛帕克 (Menlo Park) 的云软件公司, 构建并运营**AI 数据云 (AI Data Cloud)**——一套完全托管的多云数据平台 (multi-cloud data platform), 融合了存储与计算分离架构的数据仓库 (data warehouse) 引擎、基于开放表格式的数据湖仓 (data lakehouse)、数据交易市场 (marketplace)、应用平台, 以及自 2024 年起推出的第一方 AI / 大语言模型 (LLM, large language model) 层——其名称为 **Snowflake Cortex**。公司将其使命定义为"调动全世界的数据 (mobilize the world's data)", 让企业能够在统一受治理的平台上整合分析 (analytics)、数据工程 (data engineering)、应用以及 AI, 而非在数据仓库、数据湖、向量数据库和机器学习训练栈之间拼接出一系列孤岛 ([Snowflake 10-K FY2026, "Overview"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

**业务模式。** Snowflake 的几乎全部营业收入来自**基于消费的容量协议 (consumption-priced capacity arrangements)**: 客户在一至三年合约期承诺一笔固定美元的支出, 然后通过 Snowflake credit 在运行仓库、训练任务、Cortex 推理调用 (inference call)、Snowpark 容器、数据共享传输等过程中逐步消耗。因此定价直接跟踪工作负载使用——查询越多、计算越多、数据移动越多, 消耗的 credit 越多——公司的工作是让这些 credit 价格足够便宜, 让客户把更多工作负载留在 Snowflake, 而不是迁移到 BigQuery、Databricks 或开源替代品。FY26 **产品营业收入为 44.723 亿美元 (占总营收 95%)**, 专业服务为 2.116 亿美元 (占 5%) ([Snowflake 10-K FY2026, Note 3 — Revenue](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

**规模。** Snowflake FY26 末实现**总营业收入 46.8 亿美元 (同比 +29%)、产品营业收入 44.7 亿美元 (同比 +29%)**, 且前两个财年也均录得 29% 增速——FY26 10-K 专门点出了这一罕见的连续三年保持同等增速记录——**总客户数 13,328 家**、**TTM 产品营业收入超过 100 万美元的客户 733 家**、**Forbes Global 2000 (G2K) 客户 790 家** (约占 FY26 营业收入 43%), 以及**剩余履约义务 (Remaining Performance Obligations, RPO) 约 97.7 亿美元**, 同比 +42% ([Snowflake 10-K FY2026, "Our Strategy" 与 Note 3](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm); [Q4-FY26 新闻稿, 2026-02-25](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm))。截至财年末, 公司在 36 个国家拥有 **9,060 名员工**, 运营 **13 个区域云部署**, 通过 Snowgrid 跨域网格协同。

**地区结构。** 美国客户贡献 35.240 亿美元 (FY26 营业收入的 75.2%), 其他美洲 1.253 亿美元 (2.7%), EMEA (欧洲、中东、非洲) 7.637 亿美元 (16.3%), 亚太与日本 (APJ) 2.710 亿美元 (5.8%)。除美国外, 单一国家营业收入均未超过 10% ([Snowflake 10-K FY2026, Note 3 — Revenue by Geographic Area](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

**Q1 FY27 实绩 (2026-05-27 披露)。** Q1 重置了 FY27 的全年轨迹: **产品营业收入 13.343 亿美元 (同比 +34%)** (相较初始指引隐含的 +27% 明显超预期), **总营业收入 13.9 亿美元 (同比 +33%)**, **NRR 126%** (环比扩张), **RPO 92.1 亿美元 (同比 +38%)**, **季度净增客户 616 家 (同比 +38%)**, **TTM 产品营业收入 >100 万美元的客户达 779 家** —— 其中**季度净增 46 家, 接近 Q1 FY26 净增 26 家的 2 倍** ([Snowflake Q1-FY27 8-K, 2026-05-27](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm))。CFO Brian Robins 将驱动力概括为"AI 加速核心数据平台业务"叠加"一方 AI 产品采用度增长"两条主线。具体 AI 普及度披露 (2026 年 4 月末四周滚动平均): **逾 13,600 个账户**使用 Snowflake AI 能力; **Snowflake Intelligence 账户环比翻倍以上**; **Cortex Code 在逾 7,100 个账户中使用** ([Q1-FY27 8-K, 2026-05-27](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm))。CEO Sridhar Ramaswamy 将战略定位描述为 Snowflake 正从"企业数据与上下文的可信底座"转型为"Agentic Enterprise (智能体企业) 的控制平面 (control plane)"。战略行动: **AWS 多年合约扩容至 60 亿美元**, 深化与 **OpenAI** 的联合创新, **SAP 合作进入 GA (一般可用) 阶段**, 并于 2026 年 5 月签署最终协议收购 **Natoma** —— 一家面向 AI Agent 的企业级 **Model Context Protocol (MCP) 平台** —— 将 Snowflake 治理框架扩展至 AI Agent 的操作 (action), 而不仅是数据本身 ([Q1-FY27 8-K, 2026-05-27](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm))。据此, 管理层**将全年 FY27 产品营业收入指引由 56.60 亿美元 (+27%) 上调至 58.40 亿美元 (+31%)、非 GAAP 营业利润率由 12.5% 上调至 13.5%**, 非 GAAP 产品毛利率 (75%) 与调整后 FCF 利润率 (23%) 维持不变 ([Q1-FY27 8-K, 2026-05-27](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000027/fy2027q1earnings.htm))。Q1 GAAP 营业亏损 3.262 亿美元 (-23.4% 利润率); 非 GAAP 营业利润 1.658 亿美元 (11.9% 利润率); 经营性现金流 2.432 亿美元 (17.5%); 自由现金流 2.328 亿美元; 调整后 FCF 2.655 亿美元 (19.1%)。CFO Robins 主导下的首个全年指引上调清晰传递出: 初始 FY27 指引保守, AI 驱动的工作负载正将消费拉至公司初始模型未充分捕捉的水平。

![营业收入趋势 FY21–FY26](charts/snow_revenue_gm_trend.png)
*来源: [Snowflake 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm); 历史合计数据出自 10-K FY22 ([FY22](https://www.sec.gov/Archives/edgar/data/1640147/000164014722000023/snow-20220131.htm))、FY23 ([FY23](https://www.sec.gov/Archives/edgar/data/1640147/000164014723000030/snow-20230131.htm))、FY24 ([FY24](https://www.sec.gov/Archives/edgar/data/1640147/000164014724000101/snow-20240131.htm)) 以及 FY25 ([FY25](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000052/snow-20250131.htm))。*

**盈利能力轮廓。** Snowflake 在 GAAP 口径下仍处亏损, 且是**有意为之**: FY26 报告营业亏损 14.352 亿美元 (营收占比 -31%) 和净亏损 13.04 亿美元 (-28%), 与 FY25 的 14.56 亿美元营业亏损和 12.89 亿美元净亏损相当。这一差距的主体是**股权激励 (Stock-Based Compensation, SBC), FY26 为 16.09 亿美元, 占营收的 34% (FY25 占比 41%)**——这是公司在工程师现金支出与股权稀释之间有意为之的权衡, 而公司正在明确努力压降这一比例。剔除 SBC 后景象大不相同: **FY26 非 GAAP 自由现金流 (FCF) 为 11.203 亿美元 (营收占比 24%)**, 高于 FY25 的 8.841 亿美元和 FY24 的 7.789 亿美元, **经营活动产生的净现金流为 12.219 亿美元** ([Snowflake 10-K FY2026, "Key Business Metrics"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。资产负债表显示**40.3 亿美元的现金及可交易证券**, 对应 27.4 亿美元到期日为 2027 与 2029 年的零息可转换债券, 公司自筹资金状况充裕 ([Yahoo Finance, SNOW 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics))。

**估值快照 (截至 2026-05-20)。** SNOW 收于 **166.97 美元**, 市值 **579 亿美元**, 企业价值 **564 亿美元** ([Yahoo Finance, SNOW 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics))。

- **TTM P/E: 无意义 (负值)。** GAAP 口径的过去十二个月 EPS 约为 –3.83 美元 (净亏损 13.0 亿美元 / 加权平均流通股数约 3.4 亿股), 因此市盈率要么未定义, 要么——当被报告时——为一个无意义的大负数。**这一亏损绝非一次性扣减。** 损益分解: 在 46.84 亿美元营业收入上录得 31.46 亿美元毛利 (整体毛利率 67%, **产品毛利率 72%**), 但被 20.62 亿美元销售与营销 (S&M, 营收占比 44%)、19.69 亿美元研发 (R&D, 占比 42%) 和 5.50 亿美元一般及行政费用 (G&A, 占比 12%) 完全吸收——总营业费用 45.81 亿美元 对应 46.84 亿美元营收。根本驱动是**股权激励 (16.1 亿美元, 营收占比 34%)** 压制每一行损益, 再加上为承接多百万美元消费承诺投入的重金市场开拓。这是**烧钱*成长***, 而非周期低谷或结构性衰退: 经营性现金流 12.2 亿美元, 自由现金流 11.2 亿美元。剔除 SBC 后, 公司在非 GAAP 口径下稳健盈利 (FY26 非 GAAP 营业利润率约 9%, FY27 指引至 12.5%)。
- **TTM P/S ≈ 12.4 倍, EV/营业收入 ≈ 12.0 倍** ([Yahoo Finance, SNOW 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics))。这一估值显著低于 SNOW 自身的 3 年 P/S 区间——2021 年该股交易在 30 倍销售额以上, 2023–2024 年大部分时间在 ~15–20 倍 ([Macrotrends SNOW P/S 历史](https://www.macrotrends.net/stocks/charts/SNOW/snowflake/price-sales))——反映了从 2020/2021 ZIRP 高点起经历的多年估值下修, 在 2025 日历年 AI 需求重新点燃 AI 数据云叙事后已部分恢复。
- **远期 P/E ≈ 68.9 倍**, 基于一致预期的非 GAAP EPS ([Yahoo Finance, SNOW 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics))。

**同业估值对比 (TTM P/S 与 EV/Revenue, 2026 年 5 月快照):**

| 代码 | 公司 | LTM 营业收入 | 最近一季产品/总营收增速 | TTM P/S | EV/Rev | 备注 |
|---|---|---|---|---|---|---|
| **SNOW** | Snowflake | 46.8 亿美元 | Q4 FY26 产品 +30% | **12.4×** | **12.0×** | 消费+AI 数据云叙事 |
| DDOG | Datadog | 36.7 亿美元 | Q1 2026 +28% | 20.6× | 19.6× | 利润率最佳; 可观测性护城河 |
| MDB | MongoDB | 24.6 亿美元 | Atlas 指引 +21–23% | 10.8× | 9.8× | 同组中最慢, FCF 转正 |
| ORCL | Oracle | 640 亿美元 | LTM +9% | 8.4× | 10.5× | 盈利的超大市值公司; OCI AI 顺风 |
| MSFT | Microsoft | 3,180 亿美元 | Azure +12–14% | 9.8× | 10.0× | Fabric 是最直接的企业级竞争对手 |
| GOOG | Alphabet | 4,220 亿美元 | LTM +13% | 11.0× | 11.0× | BigQuery 是最直接的技术竞争对手 |
| PLTR | Palantir | 52.2 亿美元 | 同比 +30% | 62.9× | 61.5× | 纯叙事溢价; 估值高 SNOW 5 倍 |

来源: [Yahoo Finance, SNOW 关键统计指标](https://finance.yahoo.com/quote/SNOW/key-statistics); [Yahoo Finance, DDOG](https://finance.yahoo.com/quote/DDOG/key-statistics); [Yahoo Finance, MDB](https://finance.yahoo.com/quote/MDB/key-statistics); [Yahoo Finance, ORCL](https://finance.yahoo.com/quote/ORCL/key-statistics); [Yahoo Finance, MSFT](https://finance.yahoo.com/quote/MSFT/key-statistics); [Yahoo Finance, GOOG](https://finance.yahoo.com/quote/GOOG/key-statistics); [Yahoo Finance, PLTR](https://finance.yahoo.com/quote/PLTR/key-statistics)。MDB 与 DDOG 数据的内部交叉核对, 参见此前的 MongoDB 研究报告 ([reports/company/MongoDB_NASDAQ_MDB, 2026-05-20](MongoDB_NASDAQ_MDB_Research_Document_2026-05-20.md))。

![SNOW 与同业对比——TTM P/S 与 EV/Revenue](charts/snow_ps_peer_compare.png)
*来源: [Yahoo Finance 关键统计指标页面, SNOW / DDOG / MDB / ORCL / MSFT / GOOG / PLTR, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics)。*

**对估值倍数的判断。** SNOW 以**约 12 倍销售额**交易于一家增速 29%、FCF 利润率约 24% 的业务上, 同时是企业数据团队对"云数据仓库"的头号品牌认知——估值水平介于 Datadog 的 20 倍 (同组中利润率最佳, 增速相近) 和 MongoDB 的约 10 倍 (增速更慢, FCF 利润率相当) 之间。相比 2021 年峰值的 30 倍以上, 估值**大致压缩了一半**, 即便经历了 2024 年大部分时间从 10 倍以下起经 Cortex 驱动的再估值。相对 ORCL、MSFT 和 GOOG (8–11 倍) 的溢价反映的是: (a) 若 Snowflake 通过 Cortex 抢占增量 AI / 推理工作负载, 则消费上升空间; (b) Snowflake Marketplace 和 Native Apps 平台层的可选性; 以及 (c) 假定中的长跑道 AI 数据云 TAM。相对 DDOG 的折价反映了: (i) Snowflake 的 GAAP 亏损轮廓 vs DDOG 的温和 GAAP 盈利; (ii) 更重的超大规模云服务商 (hyperscaler) 依赖 (SNOW 产品的实质大多数运行在 AWS 上, 而 AWS 同时是竞争对手); (iii) Databricks 持续的竞争阴影。估值倍数要重新提升至 15 倍以上, 可能需要 Cortex / AI 消费驱动重新加速至约 30% 增长, 或经营杠杆向 20%+ 非 GAAP 营业利润率有说服力地推进。

如果 Cortex / AI 工作负载不及预期, 而 Databricks 的 AI 数据平台势头继续, 今天的 12 倍 P/S 将面临向 MDB 同组的 10 倍或更低压缩的风险, 尤其当股权激励对 GAAP 亏损的拖累持续时。我们将其作为估值/估值压缩风险纳入第 9 章。

## 2. 公司历史

Snowflake 于 **2012 年 8 月**以"Snowflake Computing, Inc."为名注册成立, 创始人为三位资深数据库专家: **Benoit Dageville** 和 **Thierry Cruanes**——两人此前均为 Oracle 数据库引擎的高级架构师, 以及 **Marcin Żukowski**——向量化查询初创公司 Vectorwise (后被 Actian 收购) 的联合创始人。创业洞察是: 为本地硬件设计的数据库引擎——包括 Dageville 和 Cruanes 在 Oracle 整个职业生涯所打造的那些——从根本上与云不匹配。它们优化了单一、昂贵、与本地存储紧耦合的单体计算节点, 而云提供了几乎无限、弹性、廉价的对象存储 (Amazon S3) 以及按需启动任意计算容量的能力。Snowflake 的标志性架构选择——**计算与存储分离**, 多个独立的"虚拟仓库 (virtual warehouse)"并发读取同一共享对象存储——正源于这一洞察, 并在 14 年后仍是平台的根基 ([Snowflake 10-K FY2026, "Our Technology"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。Sutter Hill Ventures 在 2012 年完成首轮种子投资, 并引入 **Mike Speiser** 任创始 CEO; Speiser 至今仍任首席独立董事, 随后于 2014 年将运营权交给 **Bob Muglia** (前微软服务器与工具事业部总裁), 后者于 2015 年完成 AWS 上的 GA (一般可用版本) 发布。

```mermaid
timeline
    title Snowflake 里程碑——创立至 FY26
    2012 : Snowflake Computing 在圣马刁由 Dageville、Cruanes、Żukowski 共同创立
    2014 : Bob Muglia 出任 CEO; 走出隐身模式
    2015 : 首版 AWS GA 发布
    2018 : 登陆 Azure
    2019 : Frank Slootman 出任 CEO (5 月); 登陆 Google Cloud
    2020 : 9 月 16 日在 NYSE 上市, IPO 价 120 美元——当时史上最大软件 IPO
    2021 : Snowpark for Java/Scala 发布; Snowflake Data Marketplace 扩张
    2022 : Snowpark for Python 发布; 3 月以 8 亿美元收购 Streamlit; 授权 20 亿美元回购
    2023 : Snowpark Container Services 发布; 5 月以约 1.85 亿美元收购 Neeva——AI 搜索/嵌入团队
    2024 : Sridhar Ramaswamy 于 2 月接替 Frank Slootman 出任 CEO; Cortex AI 发布; 收购 Reka 与 Datavolo; 再次授权 25 亿美元回购
    2025 : Snowflake Postgres 公布; 6 月收购 Crunchy Data; 9 月任命 Brian Robins 为 CFO; 宣布收购 Observe.ai 并 GA Snowflake Intelligence
    2026 : Q4 FY26 收官——产品营收 12.3 亿美元 / +30%, RPO 97.7 亿美元 / +42%; FY27 指引启动 (56.6 亿美元 / +27%)
```
*来源: [Snowflake 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm); [Snowflake S-1, 2020](https://www.sec.gov/Archives/edgar/data/1640147/000119312520203923/d18353ds1.htm); [Snowflake Q4-FY26 新闻稿, 2026-02-25](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm); [Snowflake 8-K, CRO 任命, 2026-03-31](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000013/ex991_pressreleasex033126.htm)。*

**战略转向——14 年三次转型。**

第一次是**云原生数据库 → 多云数据平台**。Snowflake 起步时只支持 AWS。加入 Azure (2018) 和 Google Cloud (2019) 在战略上代价昂贵——每家超大规模云服务商同时也是头号竞争对手——但它把公司从 AWS 的人质转变为一个 lock-in (锁定) 跨越多云的厂商, 这是企业数据团队 (尤其是受监管要求采用多云的) 选择 Snowflake 作为标准的最常被引用的原因之一。

第二次是**Frank Slootman 时代 (2019 年 5 月 – 2024 年 2 月) 的运营纪律塑造**。Slootman 是 Data Domain / ServiceNow 的资深运营老将, 带领工程主导的公司完成 2020 年 9 月的 IPO (当时史上最大软件 IPO, 开盘 245 美元 vs IPO 价 120 美元), 然后推动财务纪律、规模化客户成功以及他公开称之为"战或逃 (fight-or-flight)"的优先级排序。在其任内, 营业收入从 FY20 的约 2.64 亿美元增至 FY24 的约 28.1 亿美元 ([Snowflake S-1, 2020](https://www.sec.gov/Archives/edgar/data/1640147/000119312520203923/d18353ds1.htm); [Snowflake 10-K FY2024](https://www.sec.gov/Archives/edgar/data/1640147/000164014724000101/snow-20240131.htm))。

第三次——也是定义今日投资逻辑的——是**数据仓库 → AI 数据云**。在 2024 年宣布, 由 **2024 年 2 月 28 日 Sridhar Ramaswamy 出任 CEO** 加速推进, 这次转向将 Snowflake 从一个 SQL 数据仓库厂商重塑为一个统一平台, 让企业在自己第一方受治理的数据上同时运行分析*与* AI。Cortex AI (LLM 函数、检索增强生成 (RAG, retrieval-augmented generation) 原语、Snowflake Intelligence 代理)、Snowpark Container Services、Native Apps 以及对开放表格式 (Apache Iceberg) 的集成是其技术化身。**Neeva (2023 年 5 月, AI 搜索/嵌入, 约 1.85 亿美元)**、**TruEra (2024 年 5 月, AI 可观测性)**、**Datavolo (2024 年 11 月, 基于 NiFi 的数据集成, 约 2.5 亿美元)**、**Crunchy Data (2025 年 6 月, 用于 Snowflake Postgres 的 Postgres 发行版)** 以及 **Mountain (前 Mobilize.Net) 数据库迁移工具收购**是这一并购脉络的具体落地 ([Snowflake 10-K FY2026, Note 4 — Acquisitions](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

**按时间排列的收购及其逻辑。** 大多数交易是中小规模的"技术吸纳 (acqui-tech)"型, 而非变革性——Snowflake 没有做过数十亿美元级别的整合; 单笔最大交易仍是约 8 亿美元的 Streamlit。

- **Streamlit (2022 年 3 月, 约 8 亿美元)** ——Python Web 应用框架; 现作为 Cortex Agents 和 Native Apps 的内嵌前端; 在开发者心智份额上至关重要。
- **Mountain / Mobilize.Net (2023 年 2 月)** ——数据库迁移工具, 被吸收为 SnowConvert ([10-K FY2026, Note 4](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。
- **Neeva (2023 年 5 月, 约 1.85 亿美元)** ——Sridhar Ramaswamy 此前的公司; Cortex Search 的基础。九个月后 Ramaswamy 被任命为 CEO。
- **Reka AI (2024)** ——对这家多模态基础模型初创公司的少数股权投资; 普遍被解读为模型管线对冲, 在 Snowflake 转向模型中立立场之前。
- **TruEra (2024 年 5 月)** ——为 Cortex 提供的 LLM 评估 / 安全护栏 (guardrails)。
- **Datavolo (2024 年 11 月)** ——基于 Apache NiFi 的数据集成; Snowflake Openflow 的底层技术。
- **Crunchy Data (2025 年 6 月)** ——Postgres 发行版; Snowflake Postgres 的基础。
- **TensorStax (FY26)** ——数据工程自主 AI 代理 (autonomous AI agents), 已整合到 Cortex Agents。
- **Observe.ai (FY26 宣布)** ——AI 驱动的可观测性; "Observe by Snowflake"的基础, 也是公司切入"500 亿美元+ IT 运维市场"叙事的支点 ([Q4-FY26 新闻稿](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm))。

**近 12 个月动态。** 新任 CFO (Brian Robins, 前 GitLab CFO, 2025 年 9 月 22 日就任以接替 Mike Scarpelli)、新任 CRO (Jonathan "JB" Beaulier, 内部晋升, 自 2026 年 3 月 31 日生效, 接替 Michael Gannon)、产品速度 (FY26 10-K 与 Q4 新闻稿强调**fiscal 2026 推出 430+ 项新功能**)、Cortex Agents / Snowflake Intelligence / Snowflake Postgres / Openflow / Snowpark Connect for Apache Spark 的 GA, 以及与 **Anthropic、OpenAI 和 Google** 基础模型扩展原生访问的合作 ([Q4-FY26 新闻稿, 2026-02-25](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm); [Snowflake 8-K, CFO 任命, 2025-09-03](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000181/ex991_pressrelease.htm); [Snowflake 8-K, CRO 任命, 2026-03-31](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000013/ex991_pressreleasex033126.htm))。

## 3. 管理团队

**Sridhar Ramaswamy——首席执行官 (CEO) 与董事 (自 2024 年 2 月 28 日)。** Ramaswamy 是 Snowflake 历史上第二位非创始人 CEO, 可以说是董事会迄今做出的最具影响的单次招聘。从背景看, 他是**数据库研究员转广告与搜索基础设施运营者再到创业者**。在 Brown 大学获得理论计算机科学博士学位、并曾任教职研究员后, 他于 **2003 年 4 月加入 Google**, 在 Google 工程团队工作 15 年, 最终担任 **2013 年 3 月至 2018 年 10 月的高级副总裁兼广告与电商业务负责人**——在该岗位负责约 1,000 亿美元+年化营收的业务 (Google 广告体系) 以及背后数千名工程师的团队。他于 2018 年离开 Google 共同创立 **Neeva**——一个无广告消费搜索初创公司, 在被 Snowflake 于 **2023 年 5 月**收购前转向对话/AI 搜索, Ramaswamy 加入 Snowflake 任 **AI 高级副总裁** ([Snowflake 2026 DEF 14A, "Sridhar Ramaswamy" 董事简介](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm))。当 Frank Slootman 在 2024 年 2 月底宣布退休时, 董事会从内部提拔 Ramaswamy; 官方 8-K 解释这一选择为"其打造类别定义性技术的实证记录以及深厚的 AI 专业能力"。

投资者应如何看待他: Ramaswamy 属于那种能站得住脚地说出*应构建哪些 AI 产品*的 CEO——他在深度学习重塑 Google 收入引擎的时期任职 Google 广告基础设施高管, 并在 LLM 成为基本要求之前就已联合创办了一家消费 AI 搜索产品。他同时也是一家小型消费初创公司的创始 CEO, 而非身经百战的上市公司 SaaS 操盘手——FY24 和 FY25 股价 (相对接任前峰值显著回落) 以及分析师日评论都反映了任期初期的执行打折扣, 只是近期才开始反转。他的 **FY26 综合薪酬合计 2,231 万美元** (基础薪资 75 万美元, 股票奖励 2,079 万美元, 现金奖金 77.2 万美元), 相比 FY25 的 1.016 亿美元 (首年签约授予) ([Snowflake 2026 DEF 14A, 薪酬汇总表](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm))。其受益所有权为 **651,328 股 (<1%)**, 包括 60 天内可行权的 447,957 份期权——是有意义但非创始人级别的持股。支持 Ramaswamy 的理由: 他兼具技术可信度 (博士学位, 15 年在 Google 广告做 ML / RL, Neeva 创始人) 与运营可信度, 足以引领 AI 数据云转型。反对他的理由: 他不是数据库出身的创始人, 之前未在如此规模上担任过上市公司 CEO, 而 FY25 的计算定价削减和增长放缓叙事都在他任内发生。他大约还有 18–24 个月的"AI 兑现"时间, 在此之前叙事要么再获估值提升, 要么破裂。

**Brian Robins——首席财务官 (CFO) (自 2025 年 9 月 22 日)。** Robins 是**专为云软件公司在"不计代价的增长"转向"有运营杠杆的增长"的拐点而生的专业 CFO**。他曾于 **2020 年 10 月至 2025 年 9 月任 GitLab Inc. 的 CFO**, 加入 GitLab 时正好主导其 2021 年 10 月的 IPO, 并陪伴公司度过上市后早期阶段; 营业收入从 FY22 的约 2 亿美元增长至最近财年的约 7.6 亿美元, GitLab 在他任内从大幅 GAAP 亏损转向非 GAAP 盈利。在 GitLab 之前, 他曾任 **Sisense Ltd. CFO (2019 年 10 月 – 2020 年 10 月)** ——一家商业智能软件公司, 更早还在包括 **Cylance** (被 BlackBerry 收购)、**AlienVault** (被 AT&T 收购) 以及 **EMC Documentum** 在内的公司担任高级财务岗位。他获得 Lipscomb 大学金融学学士学位以及范德堡大学 MBA ([Snowflake 2026 DEF 14A, 执行官简介](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm); [Snowflake 8-K, CFO 任命, 2025-09-03](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000181/ex991_pressrelease.htm))。董事会选他的具体理由是, 据 CEO Ramaswamy 所言, 其"对运营严谨与长期高增长的深度承诺与 Snowflake 的战略方向完美匹配"——也就是说, 他被聘来缩小 SBC 差距, 并把非 GAAP FCF 利润率转化为 GAAP 营业利润率扩张。其 **FY26 签约包包含约 2,500 万美元的初始新员工股权授予**, 在代理声明中已披露。在 GitLab 的业绩纪录极具相关性: 那家公司是与 Snowflake 在相似规模上最接近的可比——靠近消费模式、SBC 较重、具创始人 DNA 的云软件业务。

**Benoit Dageville——创始人兼首席架构师, 董事。** Dageville 是三位联合创始人之一, 也是技术重心所在。他于 **2019 年 5 月至 2025 年 10 月任 President of Products**, **2012 年 8 月至 2019 年 5 月任 CTO**; 2025 年末他回归到创始人兼首席架构师头衔——这是有意之举, 让他可以专注于长跨度的平台架构工作 (Polaris 目录、Iceberg 集成、下一代查询引擎), 而非日常产品管理 ([Snowflake 2026 DEF 14A, 董事简介](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm))。他持有 **4,485,067 股 (普通股的 1.3%)**, 是创始团队中仍在运营岗位上的最高级人物 (另一位联合创始人 Thierry Cruanes 任高级工程岗位; Marcin Żukowski 类似)。Dageville 是平台方向的事实上的技术发言人, 也是为何硬件级工程师 (Bellevue/Menlo Park 引擎团队, 加上柏林 / 多伦多 / 华沙 / 圣何塞分支组成的合计 2,424 名 R&D 员工——截至 FY26 数据) 持续选择 Snowflake 而非超大规模云服务商数据库团队的原因之一。

**Christian Kleinerman——执行副总裁兼产品管理负责人 (EVP, Product Management)。** 在 Snowflake 任职已久的领导 (2018 年加入), 主管 Cortex、Snowpark、Marketplace、Iceberg 集成、Native Apps 以及完整开发者平台的产品组织。此前为 Google 资深产品负责人 (BigQuery) 和 Microsoft SQL Server 负责人。他是最有可能在 Snowflake Summit 登台、并设定公开路线图的高管。根据 2026 年代理声明持股 693,058 股 (<1%)。

**Jonathan "JB" Beaulier——首席收入官 (CRO) (自 2026 年 3 月 31 日生效)。** Beaulier 是 Snowflake 十年老兵, 此前最近任职为 GVP, U.S. Majors Sales (美国大客户销售集团副总裁)。董事会在 Michael Gannon——2025 年 3 月接任 CRO——以"个人原因"离职后晋升他 ([Snowflake 8-K, "Appoints Jonathan Beaulier as Chief Revenue Officer; Reaffirms Guidance", 2026-03-31](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000013/ex991_pressreleasex033126.htm))。这一选择信号是延续而非颠覆: 董事会不希望在 AI 叙事重新加速的中段, 在 18 个月内进行第三次销售领导层重置。

**Vivek Raghunathan——SVP, 工程与支持 (Engineering and Support, 自 2024 年 9 月)。** 替代 Grzegorz Czajkowski (2024 年 7 月辞职); 负责 Snowflake 13 个区域部署的生产工程平台。

**治理与董事会。** 11 人董事会由 **Mark Garrett** (Adobe 与 Brocade 前 CFO, 审计委员会主席) 与 **Michael L. Speiser** (Sutter Hill Ventures 董事总经理, 首席独立董事, 也是最初的种子投资人) 共同领导 ([Snowflake 2026 DEF 14A, 董事矩阵](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm))。其他董事包括 **Frank Slootman** (董事长兼前 CEO, 约 2.2% 经济权益, 760 万股)、**Jayshree Ullal** (Arista Networks CEO)、**Kelly Kramer** (Cisco 前 CFO)、**Bill Scannell** (Dell Technologies, 2025 年 5 月加入)、**Teresa Briggs** (Deloitte 前副主席)、**Mark McLaughlin** (Palo Alto Networks 前 CEO) 以及 **Benoit Dageville**。结构上为**单一类别普通股**——Snowflake 在 2025 年 7 月将 A 类普通股更名为"普通股", 消除了 IPO 后已自动终止的双重股权遗留 ([Snowflake 10-K FY2026, "Stockholders' Equity"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。内部人持股集中于 Slootman (2.2%)、Dageville (1.3%) 和 Speiser (约 0.8%); 截至 2026 年 4 月 30 日, 所有现任董事和执行官合计持有 1,709 万股, 即**普通股的 4.8%**。**Vanguard** 持股 5.1%; **BlackRock** 在 FY26 某时点持股超过 5%, 同时也是 Snowflake 的客户, 拥有 4,500 万美元的合约支出 (代理声明中讨论的一项已披露的类似关联方关系) ([Snowflake 2026 DEF 14A, "BLACKROCK, INC." 章节](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm))。董事会于**2023 年 2 月授权 20 亿美元股票回购**, 并于 **2024 年 8 月追加授权 25 亿美元**, 该计划延期至 2027 年 3 月——Snowflake 一直是其自身股票的有意义回购者, 专门用于抵消 SBC 稀释。

**履历综合判断。** Snowflake 的高级管理团队如今建立在两根支柱上: (1) 创始人 / 首席架构师 / 工程核心 (Dageville、Cruanes、Kleinerman、Raghunathan), 掌握技术平台与 IP; 以及 (2) Ramaswamy / Robins / Beaulier / Garrett 财务与上市策略层, 专门为执行运营杠杆与 AI 叙事阶段而引入。Slootman 时代的运营底盘 (Scarpelli, Degnan) 在过去 18 个月内已完全更替——围绕新战略的彻底重建。Ramaswamy 在 Google 与 Robins 在 GitLab 的履历令人印象深刻, 但尚未经历 *Snowflake 检验*; 接下来 4–6 个季度将决定这个团队能否在维持产品增速 27% 的同时实现 FY27 12.5% 营业利润率目标。

## 4. 产品与服务

Snowflake 的产品矩阵, 依据 FY26 10-K 的"Products"章节与 snowflake.com 上的实时产品导航, 端到端可分为五层: (1) **核心数据平台** (数据仓库 + 数据湖仓), (2) **AI / ML** (Cortex AI、Snowflake Intelligence), (3) **数据工程** (Snowpark、Openflow), (4) **应用** (Native Apps、Streamlit), 以及 (5) **协作 / 共享** (Marketplace、Data Cloud)。所有产品都作为同一基于消费 credit 平台的一部分销售——没有独立的 SKU 定价。

```mermaid
graph TD
    Co["Snowflake — AI Data Cloud"] --> Core["核心数据平台"]
    Co --> AI["AI / ML"]
    Co --> DE["数据工程"]
    Co --> App["应用"]
    Co --> Share["共享与协作"]
    Core --> Wh["虚拟仓库 (multi-cluster, 存储与计算分离)"]
    Core --> Ice["Iceberg Tables (开放表格式数据湖仓)"]
    Core --> Hor["Horizon Catalog (治理、血缘、策略)"]
    Core --> Pol["Polaris Catalog (Iceberg REST, 多引擎)"]
    Core --> Pg["Snowflake Postgres (事务型; Crunchy Data 技术, FY26 GA)"]
    AI --> Cortex["Cortex AI — LLM 函数、RAG、Cortex Search"]
    AI --> Agents["Cortex Agents — 结构化+非结构化数据的智能体工作流"]
    AI --> Intel["Snowflake Intelligence — 自然语言数据代理"]
    AI --> Models["原生 Anthropic / OpenAI / Google 模型; 遗留 Arctic"]
    AI --> Code["Cortex Code — AI 编码代理"]
    DE --> Snowpark["Snowpark (Python, Java, Scala)"]
    DE --> SCS["Snowpark Container Services"]
    DE --> Spark["Snowpark Connect for Apache Spark"]
    DE --> OF["Snowflake Openflow (Datavolo / 基于 NiFi 的接入)"]
    DE --> Dyn["Dynamic Tables, Streams & Tasks"]
    App --> Streamlit["Streamlit in Snowflake"]
    App --> NativeApps["Native Apps Framework"]
    App --> Workspaces["Workspaces / Notebooks"]
    Share --> Marketplace["Snowflake Marketplace (数据 + 应用 + LLM)"]
    Share --> Sharing["Secure Data Sharing"]
    Share --> Snowgrid["Snowgrid (跨区域、跨云复制)"]
```
*来源: [Snowflake 10-K FY2026, "Our Platform"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm); [Snowflake "Platform" 产品页](https://www.snowflake.com/en/product/platform/); [Snowflake "Cortex AI" 产品页](https://www.snowflake.com/en/data-cloud/snowflake-cortex/)。*

**1. 核心数据平台——数据仓库+数据湖仓基础层。**

**Snowflake Data Warehouse / 标准仓库 (Standard Warehouses)** ——最初的消费产品: 基于 SQL、列式存储、计算与存储分离, 因此每个"虚拟仓库"是独立调整大小的计算集群, 读取共享对象存储数据。按 credit 定价, 经过 60 秒下限后按秒计费。FY26 新增了**第二代标准仓库 (Generation 2 Standard Warehouses)**、**交互式表 (Interactive Tables)** 和**交互式仓库 (Interactive Warehouses)**, 面向更低时延的应用工作负载 ([10-K FY2026, "Our Platform"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。*竞争优势: 是, 技术 + 生态护城河。* 最接近的竞争对手: **Google BigQuery** 与 **Amazon Redshift Serverless**。在跨云移植性与并发上达到或优于水平; 生态领先; 在性价比上已不再显著领先——自 2022 年起 BigQuery 与 Redshift 已缩小差距。

**Iceberg Tables** ——开放表格式支持, 让客户能将数据保留在自己对象存储中的 Apache Iceberg 中, 通过 Snowflake 引擎查询。针对 Databricks Delta/Iceberg 数据湖仓主导地位的防御性回应。*竞争优势: 部分。* 最接近的竞争对手 **Databricks** (收购了 Iceberg 创始人的公司 Tabular); Snowflake 自 FY25 起在 Iceberg 上达到对等水平。

**Polaris Catalog** (2024 年开源, FY26 GA) ——Iceberg REST 目录, 让多个引擎 (Snowflake、Trino、Spark、Flink) 读取同一受治理表。战略性定位, 使 Snowflake 即便在 Databricks 同时存在于数据上时仍保持分析层。*竞争优势: 部分——战略性而非利润池。* 最接近的竞争对手 **Databricks Unity Catalog**。

**Horizon Catalog** ——跨所有 Snowflake 账户的第一方治理、血缘、分类与访问策略层。*竞争优势: 是, 规模 + 生态。* 最接近的竞争对手 **Unity Catalog**。

**Snowflake Postgres** (FY26 早期 GA, 基于 Crunchy Data 技术) ——面向事务工作负载的托管 Postgres。*竞争优势: 无。* Aurora、Cloud SQL、Cosmos DB 已深度扎根; Snowflake 的卖点是"同一治理平面上的 Postgres"——是一个统一性论据, 而非功能领先。

**2. AI / ML——Cortex 与 Snowflake Intelligence。**

**Snowflake Cortex AI** ——内嵌在数据仓库中的 LLM 和 ML 层: 用于摘要、情感分析、翻译、分类的 SQL 函数; Cortex Search (基于 Neeva 团队的 IP); Cortex Fine-Tuning; Cortex Agents (FY26 GA); Cortex Code (AI 编码代理, FY26 GA) ([Q4-FY26 新闻稿](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm))。战略为**模型中立 (model neutrality)** ——原生支持 Anthropic、OpenAI、Google、Meta 和 Mistral; 第一方"Arctic"模型已被弱化。*竞争优势: 部分。* 最接近的竞争对手: 企业 RAG 上是 **Databricks Mosaic AI + Vector Search**; 智能体编排上是 **Microsoft Fabric + Copilot Studio**; 原始模型推理上是 **Bedrock / Vertex / Azure OpenAI**。差异化点: "数据已经在这里, 受治理且可查询"——对 790 家 G2K 客户而言是真正的优势。劣势: 前沿模型推理本质上是超大规模云服务商工作负载, 而 Snowflake 为 Cortex 调用所需的底层 GPU 计算向 AWS/Azure/GCP 付费。

**Snowflake Intelligence** (FY26 GA) ——面向业务用户的自然语言→数据答案托管代理。*竞争优势: 是, 生态。* 最接近的竞争对手 **Microsoft Copilot for Power BI / Fabric**。

**3. 数据工程——Snowpark 与 Openflow。**

**Snowpark** (Python, Java, Scala) ——平台内非 SQL 代码的开发者框架: DataFrame API、UDF (用户自定义函数)、ML 训练、批处理推理。**Snowpark Container Services** (2023 年 GA, FY26 期间扩展) 在 Snowflake 安全边界内运行任意容器工作负载 (包括 GPU 训练与推理)。**Snowpark Connect for Apache Spark** (FY26 GA) 通过 Snowflake 引擎执行 Spark 应用——直接对 Databricks Spark 业务进行防御。*竞争优势: 部分。* 最接近的竞争对手 **Databricks Workflows + Mosaic AI + Spark**; 在 Spark/ML 的广度上落后, 在数据仓库集成与零运维 SQL 用户体验上领先。

**Snowflake Openflow** (FY26 GA, 基于 Datavolo/NiFi) ——托管数据集成与流式接入。*竞争优势: 部分。* 最接近的竞争对手 **Fivetran + Airbyte + Confluent**; SNOW 的卖点是"同一受治理平面下的数据接入", 而非最优功能。

**4. 应用——Streamlit 与 Native Apps。**

**Streamlit in Snowflake** ——内嵌 Streamlit (2022 年收购), 让数据团队基于 Snowflake 数据交付 Python Web 应用, 由 Snowflake 角色治理。是 Cortex Agents 与大型 Snowflake 客户内部大部分数据工具的首选前端。*竞争优势: 是, 心智份额护城河。* 最接近的竞争对手 **Databricks Apps**; SNOW 领先, 因为 Streamlit 同时也是受欢迎的开源框架。

**Native Apps Framework** ——独立软件供应商 (ISV) 构建运行在客户 Snowflake 账户内的应用, 共享客户数据而无需移动它。Capital One Slingshot 是典型例子。*竞争优势: 是, 网络效应护城河。* 最接近的对照物是面向 SaaS 应用的 **AWS Marketplace**, 但 Native Apps 的"在客户数据上运行"模型有显著差异化。

**Workspaces / Notebooks** (FY26 GA) ——Snowsight 内统一的笔记本 + 类 IDE 体验。*竞争优势: 部分。* 最接近的竞争对手 **Databricks Notebooks** (纯功能深度领先, 受治理数据集成落后)。

**5. 共享与协作——Marketplace 与 Snowgrid。**

**Snowflake Marketplace** ——数百个实时第三方数据集、Native Apps 以及 (FY26+) LLM 的目录, 在客户的 Snowflake 账户内就地消费 ([10-K FY2026, "Snowflake Marketplace"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。最被低估的战略资产: 它创造了数据网络效应, 让客户继续留在 Snowflake, 因为 LiveRamp 身份、S&P 市场数据、FactSet、天气与地理数据离手一键之遥。*竞争优势: 是, 网络效应护城河。* 在可比规模上没有直接竞争对手。

**Snowgrid** ——跨区域 / 跨云复制网格, 将 Snowflake 13 个区域部署连接到一个受治理命名空间中。*竞争优势: 是, 规模 + 技术。* 没有直接竞争对手具备可比的多云覆盖。

**旗舰 vs 长尾。** 在经济上推动 Snowflake 的 1–3 个旗舰产品仍是 (a) **仓库 / SQL 数据仓库**, 仍是 credit 消费的主导驱动; (b) **Snowpark** (Python / 容器), 自 2023 年以来一直是 credit 增长故事, 也是数据工程与 ML 工作负载的主要入口; 以及 (c) **Cortex AI + Snowflake Intelligence**, 是整个 FY26–FY28 叙事所依赖的产品。Marketplace 与 Native Apps 是战略可选性, 而非当下的营收贡献; Snowflake Postgres 是功能完备性举措; Iceberg + Polaris + Horizon 是防御性必备项。

**最近发布与产品速度。** Q4 FY26 发布说明明确指出 **fiscal 2026 推出 430+ 项新功能**, 头条 GA 包括 Cortex Agents (第二代)、第二代标准仓库、Interactive Tables / Warehouses、Workspaces、Managed MCP Server、Snowflake Openflow、Snowpark Connect for Apache Spark、Snowflake Postgres、Snowflake Cortex Code 与 Semantic View Autopilot ([Snowflake 10-K FY2026, "Recently launched capabilities"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm); [Q4-FY26 新闻稿](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm))。未披露重大产品下架。

## 5. 客户与上市策略

Snowflake 的客户基础对于这个规模的公司而言异常多元: FY26 末**总客户数 13,328 家**, 覆盖各规模组织, 从单团队 Snowflake-Standard 用户到运行数千个并发仓库的跨国企业 ([Snowflake 10-K FY2026, "Our Customers"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

**客户分组与集中度。** 截至 2026 年 1 月 31 日:

- **TTM 产品营收 > 100 万美元的客户 733 家** ——较一年前的 580 家增长 (+27% YoY), 而六年累计较 FY21 的 77 家增长约 10 倍。
- **Forbes Global 2000 (G2K) 客户 790 家** ——较 750 家增长 (+5% YoY), 贡献约**FY26 营业收入的 43%**。
- **在 FY24、FY25 或 FY26 中, 没有单一客户或一组客户占营业收入或应收账款 10% 或以上** ([Snowflake 10-K FY2026, Note 3 — "Significant Customers"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。

对于这个规模的 SaaS 公司而言, 这是真正较低的客户集中度——前一大与前五大客户份额均低于 FY26 10-K 必须披露的 10% 门槛。G2K 队列占营收的 43% 是最接近集中度担忧的地方, 但它是一个*队列*而非单一客户, 且该队列同比 +5% 的增速是所有披露指标中最小的 (vs. 100 万美元+客户的 +27% 与总营收 +29%), 反映出 Snowflake 现已渗透 G2K 三分之一以上, 增量增长必须来自非 G2K 中端市场扩张或现有 G2K 消费加速。

![客户分组 FY21–FY26](charts/snow_customer_cohorts.png)
*来源: [Snowflake 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) 与过去年度文件 ([FY25](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000052/snow-20250131.htm)、[FY24](https://www.sec.gov/Archives/edgar/data/1640147/000164014724000101/snow-20240131.htm)、[FY23](https://www.sec.gov/Archives/edgar/data/1640147/000164014723000030/snow-20230131.htm)、[FY22](https://www.sec.gov/Archives/edgar/data/1640147/000164014722000023/snow-20220131.htm)、[FY21](https://www.sec.gov/Archives/edgar/data/1640147/000164014721000073/snow-20210131.htm))。*

```mermaid
pie title FY2026 营业收入按客户分组
    "Forbes Global 2000 客户 (~43%)" : 43
    "其他所有客户 (~57%)" : 57
```
*来源: [Snowflake 10-K FY2026, "Our Customers" 章节](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm)。*

**净收入留存率 (NRR, Net Revenue Retention)。** FY26 末 NRR 为 **125%**, 较 FY25 的 126% 与 FY24 的 131% 略有下行, 显著低于 158% (FY23) 与 178% (FY22) 的峰值。这一轨迹反映了 (a) 大数法则 (基数已是 47 亿美元而非 12 亿美元), (b) 2023–2024 年间企业客户的消费优化举措压低了 NRR, 以及 (c) 客户书的成熟化。最近五个季度减速似已稳定在 125–126% 区间, 对这个规模的云软件业务而言仍是同业最佳。管理层在 Q4 FY26 电话会议上将 NRR 下限定在"约 125%"上, 维持至 AI 驱动的重新加速阶段。

![NRR 趋势 FY21–FY26](charts/snow_nrr_trend.png)
*来源: [Snowflake 10-K FY2026, "Key Business Metrics" 表](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) (NRR 按 TTM 消费基础计算)。*

**主要企业客户名单。** 直接出自 FY26 SEC 文件与 Q4 新闻稿: **Capital One** (Snowflake 长期数百万美元的账户, 也是 Marketplace Native App Slingshot 的开发者)、**Thomson Reuters** (数据与分析现代化)、**BlackRock** (FY26 期间 5%+ 持股, 自 2021 年起为 Snowflake 客户, 2024 年 1 月签订 4,500 万美元五年合同, 加 2025 年额外技术服务协议)、**Canva**、**Siemens**、**JetBlue Airways**、**Adobe**、**Pfizer**、**Western Union**、**Albertsons**、**AT&T**、**Mastercard** 与 **Anthem** (后一组在过去年度文件与 Snowflake 案例库中提及; 参见 [Snowflake 客户页](https://www.snowflake.com/en/customers/))。合约结构通常是**一至三年承诺消费合同 (容量协议)**, 在合同期内按比例确认年度营收, 国际账户以客户当地货币计价。多数 G2K 账户是主服务协议下的多年合同, 而非按 PO 一笔笔签。

**地理分布。** 如上所示, FY26 美国贡献营收的 75%, EMEA 16%, 亚太与日本 6%, 其他美洲 3%。EMEA 与 APJ 在百分比基础上增速快于美国, 但基数较小。

![地理营收结构 FY24–FY26](charts/snow_geo_mix.png)
*来源: [Snowflake 10-K FY2026, Note 3 — Revenue by Geographic Area](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm)。*

**上市策略 (Go-to-Market) 动作。** Snowflake 通过混合模式销售, 结合直销企业销售团队 (Snowflake 的命名账户团队——Mike Gannon, 现为 JB Beaulier 的 CRO 组织)、有意义的**系统集成商 (SI) 渠道** (Accenture、Deloitte、KPMG、Slalom、Capgemini、Wipro、EPAM 等——Snowflake 品牌的 SI 合作伙伴关系列在 Snowflake Partner Network), 以及与 AWS、Azure 和 Google Cloud 的**超大规模云服务商联合销售**——Snowflake 交易可通过每家云的 marketplace 完成, 并可抵扣客户已承诺的云支出。后者是 GTM 中最被低估的环节: 客户可以用 AWS Marketplace 积分购买 Snowflake, 使得在已与云承诺签约的企业内购买变得简单 ([Snowflake 10-K FY2026, "Sales and Marketing"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。FY26 S&M 费用为 **20.62 亿美元, 占营收 44%**, 其中**销售员工数据 FY26 10-K 明确说明与营收同步增长** (公司未披露确切销售代表人数, 但总员工数从 FY25 末的约 7,800 增至 FY26 末的 9,060)。新 G2K 账户的销售周期通常 9–18 个月; 基础内的扩展交易是持续进行的。

**关键合作伙伴。** 基础模型合作: **Anthropic** (Claude 系列于 Cortex)、**OpenAI** (GPT 系列原生支持)、**Google Cloud / Gemini** (模型访问)、**Mistral**、**Meta** (Llama) 以及 **NVIDIA** (NeMo, NIM 微服务)。实施合作伙伴: **Accenture、Deloitte、KPMG、EY、Slalom、Capgemini、Wipro、EPAM**。数据合作伙伴: Marketplace 上数百家提供商, 包括 **LiveRamp** (身份)、**S&P Global Market Intelligence**、**FactSet**、**Experian**、**Weather Source**、**AccuWeather**、**CoreLogic** (房地产) 以及众多垂直行业专家 ([Snowflake Marketplace 落地页](https://www.snowflake.com/en/data-cloud/marketplace/); [Q4-FY26 新闻稿, 合作伙伴关系标注](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm))。

## 6. 行业概览

Snowflake 处于过去十年间逐渐合并为一体的三个行业的交叉点: **云数据仓库 (cloud data warehouses)**、**数据湖 / 数据湖仓 (data lakes / lakehouses)** 以及 **AI / ML 平台**。每一个在 2018 年都是独立的产品类别; 今天, 在后 ChatGPT 时代, 边界已模糊到大多数分析师直接将合并空间称为"**云数据与 AI 平台**"市场。

**行业定义与范围。** 云数据与 AI 平台市场包括 (a) **云数据仓库** (Snowflake、BigQuery、Redshift、Synapse、Teradata Vantage), (b) **数据湖仓** (Databricks、开放 Iceberg/Delta 生态、数据仓库厂商的湖仓产品), (c) **数据工程与 ETL** (Fivetran、Airbyte、Confluent), (d) **AI / ML 模型服务** (Bedrock、Azure OpenAI、Vertex AI), 以及 (e) **AI 原生企业平台** (Databricks Mosaic、Snowflake Cortex、Microsoft Fabric)。正式分类对应 NAICS 518210 与 511210。

**市场规模——TAM 视角。** 三种可信的估算:

- **IDC 2024 全球数据平台软件市场预测** ——2024 年约 1,200 亿美元 → 2028 年约 2,500 亿美元, 年复合 CAGR 约 20% ([IDC FutureScape Worldwide Data Platforms 2024 Predictions](https://www.idc.com/getdoc.jsp?containerId=US51393623))。
- **Gartner 2025 云数据库管理系统 (CDBMS) 魔力象限** ——2024 年 CDBMS 市场约 920 亿美元, 预计 2030 年超过 2,000 亿美元; Snowflake、Microsoft、Google、AWS、Databricks、Oracle 与 SAP 是七大"领导者", SNOW 位居右上 ([Gartner 新闻稿, 2025-01](https://www.gartner.com/en/newsroom/press-releases))。
- **Snowflake 自身 2024 年 6 月 / 2025 年 9 月投资者日 TAM** ——2028 年达 3,420 亿美元, 覆盖分析、AI/ML、数据工程、应用、协作、事务、可观测性和网络安全。

三者三角化为 2028 年约 2,000–3,500 亿美元的市场, 云数据支出增速约为整体 IT 的 3 倍。

**增长驱动。** 第一是**分析、ML 和推理工作负载从本地栈持续迁移到云原生平台** ——Gartner 在 2024 年估计只有约 50% 的分析工作负载已迁移到云 DBMS, 另一半作为多年迁移 TAM 留存。第二是 **AI 工作负载顺风**: 模型训练、RAG、智能体应用以及围绕它们的数据准备 / 特征工程, 都需要一个统一的数据平面, 而这个平面正在被选择——*此刻*。基础模型厂商 (OpenAI、Anthropic、Google) 有意将 AI 工作负载推回数据平台, 因为专有的企业数据存在那里。第三是**监管数据主权**: GDPR、EU Data Act、印度 DPDPA、中国 PIPL 以及美国州级隐私法规, 都推动客户选择能够执行行级 / 列级治理并在区域内运行的平台, 这在结构上利好 Snowflake (13 个区域部署, 多云) 和 Databricks (类似架构), 不利于单云专项解决方案。

**行业结构。** 顶部集中, 中部分散。**超大规模云服务商 (AWS、Azure、GCP)** 在结构上控制 GPU / 计算 / 存储, 既可能是记录平台 (BigQuery、Redshift、Synapse/Fabric、OCI), 也可能是 SNOW 与 Databricks 的底层基础设施。**Snowflake 与 Databricks** 是客户在希望跨云时考虑的两个"中立"平台品牌 (FY26 10-K 指出 Snowflake 业务的"实质大多数"运行在 AWS 上, 但客户也选择 Azure 和 GCP)。**Oracle、Microsoft (Fabric) 和 Google (BigQuery)** 则是第二梯队顶部——成熟、盈利, 但各自有结构性折中 (Oracle 安装基础在本地且仅部分迁移; Fabric 仅 Azure; BigQuery 仅 GCP)。再往下是专项老牌 (**Teradata、Cloudera、MongoDB、Confluent、MongoDB Atlas vector、Elastic**) 与 AI 原生挑战者 (**Pinecone、Weaviate、Chroma、Modal、Anyscale**)。

**监管。** 多为间接性影响: GDPR / CCPA / 州级隐私法律对客户数据; **欧盟人工智能法案 (EU AI Act)** (2026 年全面生效) 对 AI 系统施加义务, 包括数据血缘与偏见文档——推动客户选择已经强制执行这些控制的平台 (Horizon Catalog)。先进 GPU 的出口管制 (BIS 2022 年 10 月 / 2023 / 2025 年更新) 主要是超大规模云服务商问题, 而非 Snowflake 问题, 但间接影响 Snowflake 销售透过的模型训练计算的成本与可用性。SOC 2 Type II、FedRAMP、HITRUST、IRAP 与类似认证是基本要求。

**定价动态。** 行业内的消费定价在美元/credit 的水平上保持大致稳定, 但**平台通过性能改进主动降低了每工作负载的 credit 消耗** ——Snowflake 在 2024 年末公开披露并在 2025 年期间重申, 引擎在相同查询上已变得明显更快, 这实际上降低了客户支付的每查询成本。再加上客户主动的消费优化, 让 NRR 从 178% (FY22) 降至今日的 125% 下限。Databricks 走了类似的闭环。前景风险是, 如果 GPU 效率提升超过 AI 工作负载增长, 同样的动态可能在 AI 推理上重演。

**替代品与买方议价能力。** 替代品包括 (a) **基于超大规模云服务商底层原语的开源 Spark / Trino / DuckDB / Iceberg 栈自建方案 (DIY)**, (b) **超大规模云原生服务** (BigQuery、Synapse/Fabric、Redshift), 能够捆绑入客户既有云承诺, 以及 (c) 针对窄场景的**专项厂商** (向量数据库的 Pinecone、流式的 Confluent 等)。最大型企业拥有最高买方议价能力, 它们会协商多年容量承诺并使用 SI 合作伙伴评估替代方案——但切换成本也最高, 因为把数据 + 应用 + 治理 + 角色 + 权限从一个平台搬走是个 12 个月、几十名 FTE 的工程。

## 7. 竞争格局

FY26 10-K 本身的竞争对手披露异常坦诚: Snowflake 点名 **AWS、Azure、GCP** 为主要的公有云竞争对手, 称其"基本上在所有市场上都参与竞争", 并加上"不那么稳固的公有云与私有云公司"、"现有的传统数据库或大数据解决方案厂商"、"现有的可观测性解决方案提供商"以及"新进入者或新兴者" ([Snowflake 10-K FY2026, "Competition"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm))。我们将描绘十个最具战略相关性的竞争对手。

```mermaid
quadrantChart
    title 云数据平台——广度 vs AI 工作负载定位 (分析师视图, 2026 年 5 月)
    x-axis "窄 / SQL 仓库" --> "广 / 统一数据 + AI"
    y-axis "纯分析" --> "AI 原生"
    quadrant-1 "广 + AI 原生"
    quadrant-2 "AI 原生但窄"
    quadrant-3 "窄 + 分析"
    quadrant-4 "广 + 分析"
    "Snowflake": [0.78, 0.72]
    "Databricks": [0.86, 0.85]
    "Microsoft Fabric": [0.74, 0.62]
    "Google BigQuery / Vertex": [0.72, 0.74]
    "AWS Redshift / Bedrock": [0.66, 0.58]
    "Oracle OCI / ADW": [0.55, 0.42]
    "MongoDB Atlas": [0.32, 0.55]
    "Teradata Vantage": [0.45, 0.28]
    "Confluent": [0.28, 0.40]
    "Pinecone": [0.15, 0.62]
```
*来源: 作者的定位视图, 锚定 [Snowflake 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) 披露的产品覆盖与 AI 工作负载定位; [Databricks "Data Intelligence Platform" 页](https://www.databricks.com/product/data-intelligence-platform); [Gartner 2025 CDBMS 魔力象限新闻稿, 2025-01](https://www.gartner.com/en/newsroom/press-releases)。*

**1. Databricks (私有公司, 核心竞争对手)。** Databricks 是 Snowflake 在客户对话中提及最多的平台, 尽管按 SEC 披露惯例被归入"不那么稳固的公有云与私有云公司"。Databricks 在 AWS、Azure 和 GCP 上运行一个竞争性的数据湖仓 + Mosaic AI + Unity Catalog 栈; 该公司历史上在 ML / 训练 / 流式上领先而在 SQL 分析上落后, 通过 2024–2025 年对 Tabular (Iceberg 创始人) 的收购以及持续的激进功能开发, 在 SQL 一端显著加速。Databricks 在 **2024 年 12 月以 620 亿美元投后估值完成 100 亿美元 Series J** ([Databricks 新闻稿, 2024-12-17](https://www.databricks.com/company/newsroom/press-releases/databricks-secures-10-billion-financing-led-thrive-capital))。行业估计 Databricks 进入 2025 年时的 ARR 年化约 37 亿美元, 至 2025 年末约 40–50 亿美元 (私有、未经审计; 据资金轮次相关的 Bloomberg 报道), 意味着 Databricks 现在与 Snowflake 的营收规模仅相差一个倍数, 且增长更快。SNOW 上方的竞争阴影真实而持续: 每个季度分析师日的 Q&A 都会辩论"谁拿哪种工作负载?", 共识答案一直是"SNOW 拿 SQL / 治理 / 易用性, Databricks 拿 ML / 训练 / 开放格式 / 数据工程。" Snowflake 的 Iceberg + Polaris + Snowpark Connect 战略显式被设计用于守护 SQL 阵地, 同时在 Databricks 取胜的场景中保留数据桌上的一席。

**2. Microsoft Fabric + Azure。** Fabric (2023 年发布) 捆绑 OneLake (Delta 存储)、Synapse、Data Factory、Power BI 与 Copilot。"始终在线 (always-on)"定价与 Power BI / Office 365 集成, 使其成为以 Microsoft 为中心的企业的默认选择。劣势: 仅 Azure。SNOW 的回应: 跨云与 Copilot 互操作。Microsoft 同时也是 SNOW 在 Azure Marketplace 上的合作伙伴。

**3. Google BigQuery + Vertex AI。** 架构上最接近 Snowflake 的对照——存储与计算分离、无服务器、列式——并与 Gemini、Vertex AI 和 Google 的 ML 栈紧密集成。以 GCP 为中心的企业的默认选择。单云。CEO Ramaswamy 在 Google 工作 15 年, 从内部熟知 BigQuery。

**4. AWS Redshift + Bedrock。** Redshift 是 AWS 传统的数据仓库; Bedrock 是模型服务层。结构性张力: Snowflake 产品的实质大多数运行在 AWS 上, 因此 SNOW 在 Redshift 对分析查询的竞争中, 仍向 AWS 付费基础设施——FY26 10-K 在其风险因素中标注了这一点。AWS Marketplace 联合销售是强大的 GTM 杠杆, 但底层依赖是 Snowflake 承担的最大非产品风险。

**5. Oracle (OCI + Autonomous Database + Oracle 23ai)。** 五年 OCI 资本重构 (包括 OpenAI Stargate JV) 加上 23ai 的向量 / AI 特性, 让 Oracle 在受监管行业以及 Oracle-ERP 安装基础账户中具备可信度。Oracle 的盈利能力和 OCI 的 GPU 建设给了其 AI 训练上的成本优势。在分析用户体验、开发者心智份额和生态上落败。

**6. MongoDB (NASDAQ: MDB)。** 相邻而非直接竞争: Atlas 在运营工作负载上与 Snowflake Postgres 竞争, Atlas Vector Search (以及 Voyage AI 收购) 在 RAG 上与 Cortex Search 重叠。MDB 在 Q4 FY26 产品增速 +27% → Atlas 指引 +21–23% (24.6 亿美元营收), 大约是 SNOW 规模的一半, 增速更慢 ([MongoDB 研究报告, 2026-05-20](MongoDB_NASDAQ_MDB_Research_Document_2026-05-20.md); [MongoDB Q4 FY2026 新闻稿, 2026-03-02](https://www.sec.gov/Archives/edgar/data/0001441816/000162828026013199/mdb-13126xex991xrelease.htm))。MDB 的 P/S 约 10.8 倍, 紧随 SNOW 的 12.4 倍。

**7. Datadog (NASDAQ: DDOG)。** 在 Observe by Snowflake 之后, 现在是可观测性 + AI 数据层的竞争对手。DDOG Q1 2026 +28%, LTM 36.7 亿美元, FCF 利润率约 26%——同组中最佳利润率 ([DDOG Q1 2026 8-K, 2026-05](https://www.sec.gov/Archives/edgar/data/0001561550/000162828026031677/ex-991x20260331x8k.htm))。TTM P/S 20.6 倍——可比组中最高。

**8. Confluent (现已归入 IBM)。** 以 Kafka 为锚的流式竞争对手。IBM 于 2026 年 3 月完成对 Confluent 的收购; Confluent + IBM watsonx 是流式 AI 玩法, 既补充也竞争于 Snowflake Openflow。

**9. Teradata、Cloudera、SAP。** Snowflake 已替代的传统老牌 (Teradata 通过 SnowConvert), 处于缓慢衰退中。SAP Datasphere 仅在 SAP-ERP 锚定账户内有可信度。

**10. Pinecone、Weaviate、Chroma。** 专业向量数据库 (vector DB), 与 Cortex Search 在 RAG 上竞争。SNOW 的优势: 数据已经在平台上; 它们的优势: 最优向量索引性能。

**Snowflake 的竞争优势。** (a) **跨云中立性** ——AWS、Azure、GCP 都无法匹敌。(b) **Snowflake Marketplace 数据网络效应** ——数百家数据提供商创造引力。(c) **同业最佳的 SQL 用户体验与并发** ——多仓库架构意味着分析工作负载不会与事务或 ML 工作负载争资源。(d) **品牌与类别拥有** ——"Snowflake"对许多企业数据团队而言仍是"云数据仓库"的默认术语。(e) **治理 + Iceberg 互通** ——Horizon + Polaris 让 Snowflake 在数据开放时仍能作为分析层。(f) **客户集中度极低** (无 10% 客户)。

**竞争漏洞。** (a) **AI 工作负载相对 Databricks 的定位** ——Databricks 在 ML / 训练上仍领先, Mosaic AI 的 RAG / 代理栈在企业牵引力上可比。(b) **超大规模云服务商依赖** ——尤其 AWS 既是 Snowflake 最大的基础设施成本, 也是直接的 Redshift 竞争对手。(c) **股权激励拖累** ——FY26 占营收 34%, 比成熟 SaaS 高一个数量级, 压制 GAAP 业绩和股数增长。(d) **Cortex 货币化风险** ——AI 数据云论断依赖 AI / 推理成为实质 credit 消费, 而 AI 推理的单位经济性 (在 GPU 利润率由超大规模云服务商赚取的情况下) 在结构上比仓库分析更难。(e) **NRR 下限 125%** ——多年下行已稳定, 但跌破 120% 将显著改变长期增长方程。

## 8. 市场机会 (TAM)

最常被引用的 TAM 数字是 **Snowflake 自身的 2028 年 3,420 亿美元 TAM**, 在 2024 年 6 月投资者日提出并在 2025 年 9 月投资者日重申。分解涵盖分析 (约 500 亿美元)、AI / ML (约 700 亿美元, 包含模型训练与推理)、数据工程 (约 500 亿美元)、应用 (约 600 亿美元)、协作 / Marketplace (约 120 亿美元) 以及相邻垂直——事务 (Postgres, 约 300 亿美元)、可观测性 (约 500 亿美元) 与网络安全 (约 200 亿美元) ([Snowflake Investor Relations, "Investor Day 2024 deck"](https://investors.snowflake.com/events-and-presentations/events/event-details/snowflake-investor-day-2024))。2028 年数据从 2023 年提出的 2,900 亿美元 (2027 年) 上调, 反映了 AI 工作负载与 Observe by Snowflake / Crunchy Data 相邻领域的加入。

**与第三方估算的三角化。** Gartner 2025 云 DBMS 魔力象限将 2024 年云 DBMS 市场规模定为约 920 亿美元, 至 2030 年 CAGR 约 22%, 暗示 2028 年约 2,500 亿美元, 2030 年约 3,000 亿美元。IDC 2024 全球数据平台预测 (2024 年 Q4 发布) 将全球数据平台软件市场定为 2024 年约 1,200 亿美元, 到 2028 年增长至约 2,500 亿美元。两个数字都*低于* Snowflake 的 3,420 亿美元——Snowflake 的 TAM 更大, 因为它显式包含分析机构归入独立类别的可观测性和网络安全等相邻类别 ([Gartner 2025 CDBMS 新闻稿, 2025-01](https://www.gartner.com/en/newsroom/press-releases); [IDC FutureScape, 2024-Q4](https://www.idc.com/getdoc.jsp?containerId=US51393623))。诚实的解读是, *传统*云数据与 AI 平台 TAM (仓库 + 数据湖仓 + AI / ML) 到 2028 年更接近 2,500 亿美元, 而 Snowflake 的 3,420 亿美元在此基础上叠加了约 900 亿美元的相邻市场可选性。

**可服务可获取市场 (SAM) 与可服务可获得市场 (SOM)。** Snowflake 的 FY26 营收 46.8 亿美元约占 2026 年云数据 + AI 平台市场 2,300–2,500 亿美元的 **2%**, 留出大量跑道。SAM——剔除超大规模云锁定的工作负载、不会迁移的本地迁移和与 SAP / Oracle-ERP 绑定的分析后的可寻址部分——目前更接近 800–1,100 亿美元, 对应 Snowflake 的份额更接近 4–6%。更长跑道的 SOM, 假设 Snowflake 在 AI / 数据湖仓工作负载上从 Databricks 和超大规模云服务商手中赢得份额, FY30 营收实现 300–400 亿美元是合理的——如果 FY27 27% 增速逐步降至 18–20% 且 FY30 落在约 100–120 亿美元水平。这一运行率仍将让 Snowflake 在 2030 年远低于 TAM 的 5%。

![RPO 与 FCF 轨迹 FY22–FY26](charts/snow_rpo_fcf.png)
*来源: [Snowflake 10-K FY2026 "Key Business Metrics"](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) (FCF) 与过去年度 10-K ([FY25](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000052/snow-20250131.htm)、[FY24](https://www.sec.gov/Archives/edgar/data/1640147/000164014724000101/snow-20240131.htm)、[FY23](https://www.sec.gov/Archives/edgar/data/1640147/000164014723000030/snow-20230131.htm)、[FY22](https://www.sec.gov/Archives/edgar/data/1640147/000164014722000023/snow-20220131.htm))。*

**TAM 内的增长驱动。** 三个最大的前向杠杆是 (a) **通过 Cortex 实现 AI 工作负载货币化** ——当在 Snowflake 驻留数据上运行时, 每次推理调用、每次嵌入生成、每次智能体工作流都转化为 Snowflake credit 消费, (b) **Snowpark / 容器扩展至 ML 训练与 Spark 工作负载** ——历史上被 Databricks 锁定的工作负载, 以及 (c) **Marketplace + Native Apps 营收增量** ——Snowflake 在第三方应用与数据营收中抽成, 作为消费之上的高毛利覆盖层。最不确定的杠杆是 Cortex AI 推理: 单位经济学计算混杂 (Snowflake 为底层 GPU 周期向超大规模云服务商付费), 而客户即便数据存在 Snowflake, 也可能选择直接在 Bedrock / Vertex / Azure OpenAI 上运行 AI 推理。

**渗透策略。** Snowflake 未来两年的上市策略优先 (1) **在现有 G2K 队列内扩展** (2,000 中已达 790 意味着 60%+ 的全球企业宇宙仍未被开发), (2) **AI 工作负载** (Cortex + Snowflake Intelligence) 作为已安装账户的新 credit 消费故事, (3) **国际增长** (EMEA 在 FY26 增长 33% vs. 美国 28%; APJ 增长 44%), 以及 (4) **相邻工作负载扩展** (Postgres、Observe、Openflow)。FY27 指引 56.6 亿美元 +27% 暗示公司期望所有四个杠杆继续发力——但最慢的是 G2K 客户数, FY26 仅增长 5%, 表明 G2K 新 logo 获取阶段可能正在接近饱和。

## 9. 风险评估

### 公司特定风险

**1. Databricks 竞争压力与 AI 工作负载定位 (高)。** Databricks 是 Snowflake 自身销售活动中提及最多的竞争对手, 也是最可能抢占增量 AI 工作负载份额的公司。Databricks 的 Mosaic AI、Spark 原生数据工程以及 Unity Catalog 在企业中获得牵引力, 即便 Snowflake 已发布 Cortex 与 Polaris 作为回应。Databricks 在 2024 年 12 月以 620 亿美元投后估值完成 Series J, 并正接近 2025/2026 的 IPO, 隐含倍数可能高于 SNOW。如果 Snowflake 在 AI / ML / 训练工作负载份额上大量输给 Databricks, 支撑 12 倍 P/S 倍数的 Cortex 论断就会破裂。缓解: Iceberg + Polaris 让 SNOW 仍保持查询引擎角色; Snowpark Container Services 扩展非 SQL 工作负载; Marketplace 数据网络效应真正具备防御性。

**2. 超大规模云服务商依赖与基础设施成本 (重大)。** Snowflake 产品的"实质大多数"运行在 AWS 上, 其余在 Azure 和 GCP。每家超大规模云服务商同时也是直接竞争对手 (Redshift、Synapse / Fabric、BigQuery)。Snowflake 对三家都签有多年最低采购承诺; FY26 10-K 指出未能履行这些承诺可能对业绩造成重大影响。如果 AWS 大幅提价、限制容量或更积极地以 SNOW 为代价投资于 Redshift / Bedrock 联合销售, 影响将是重大的。缓解: 多云分布; 营收的约 75% 来自美国, 多数大客户重视跨云移植性。

**3. AI 推理单位经济性 (重大)。** Cortex AI 推理为 Snowflake 赚取 credit, 但底层 GPU 计算以超大规模云利润率从 AWS / Azure / GCP 采购。如果 AI 消费随着时间成为 credit 中的实质部分, 而这些 credit 的毛利率显著低于分析查询 credit, 公司的 72% 产品毛利率即便营收增长也可能下行。缓解: 公司正在投资效率 (具体而言 FY26 "第二代"仓库和 Cortex 效率改进), 如果 AI 工作负载在治理与数据共位上有差异化, 则存在定价权。

**4. NRR 下限与消费优化 (重大)。** NRR 在过去五个季度稳定在 125–126%, 较 FY22 的 178% 下行后已企稳。当前下限取决于 AI 工作负载增加*新*消费来抵消持续的客户端优化。如果 AI 顺风不及预期——特别是 Cortex 货币化令人失望——NRR 可能跌破 120%, 这将压缩长期增长并下修股价。缓解: 已稳定五个季度; Cortex GA + Snowflake Intelligence + Snowpark 扩展都增加新的消费表面。

**5. 股权激励拖累 (重大)。** SBC 在 FY26 占营收 34%, 较 FY25 的 41% 下降, 但仍远高于同业。SBC 维持 GAAP 亏损轮廓、稀释股东 (45 亿美元回购授权仅部分抵消)、压低 GAAP 营业利润率。Brian Robins 被聘用部分目的是解决这一问题。缓解: FY26 SBC 同比下降 7 个百分点; 回购计划降低股数增长; FY27 指引意味着营业利润率进展。

**6. 高层领导过渡风险 (中等)。** Snowflake 在 24 个月内已更换 CEO (2024 年 2 月)、CFO (2025 年 9 月)、CRO (两次: 2025 年 3 月与 2026 年 3 月) 与工程 SVP (2024 年 9 月)——几乎完成了 Slootman 时代的运营领导层换血。新团队尚未一起完成完整财年。缓解: Ramaswamy 自 2024 年 2 月任职至今; Robins 拥有强劲的 GitLab 履历; Beaulier 是内部晋升, 保留了关系。

### 行业 / 市场风险

**7. 来自超大规模云服务商与 Microsoft Fabric 的竞争强度 (重大)。** Microsoft Fabric (Azure 锚定, 与 Power BI 和 Office 365 捆绑)、Google BigQuery + Gemini (单云但技术非常强)、AWS Redshift + Bedrock (最大安装基础) 都正面竞争。每家都有近乎无限的 R&D 预算和计算上的结构性成本优势。缓解: Snowflake 的跨云中立性与易用性差异化; 超大规模云服务商的单云锁定对某些客户是特性, 对另一些客户是缺陷。

**8. 来自前沿模型厂商的 AI 平台颠覆 (中等)。** OpenAI、Anthropic 与 Google 已发布并持续扩展企业数据产品表面 (OpenAI Enterprise、Anthropic Claude for Work、Gemini for Workspace), 触及 Snowflake 的领域。一个未来——其中基础模型厂商*即*平台, 而 Snowflake 被降级为数据存储 SKU——如果客户决定"模型即产品", 是非微不足道的风险。缓解: 企业数据具有粘性; 治理与血缘要求 (欧盟人工智能法案、内部审计) 利好 Snowflake 的结构。

**9. 监管与数据主权敞口 (中等)。** GDPR、EU Data Act、印度 DPDPA、中国 PIPL 与美国州级隐私法律, 都创造了复杂的按区域治理要求。欧盟人工智能法案 (2026 年全面生效) 增加偏见 / 血缘 / 文档义务。虽然这些在结构上利好 Snowflake, 但监管失误 (数据泄露、跨境传输处理不当) 代价可能极高。缓解: 13 个区域部署; Horizon Catalog; SOC 2 / FedRAMP / IRAP 认证。

### 财务风险

**10. 估值 / 倍数压缩风险 (重大)。** SNOW 在 GAAP 亏损业务上交易在 12.4 倍 TTM P/S, 较 MDB 高约 26%, 较 MSFT / GOOG / ORCL 中位数高约 28%。跌破 120% NRR、Cortex 重大失望或 Databricks 进一步份额增长, 可能将倍数压缩至 MDB 的 10 倍或更低——意味着仅倍数层面就有约 20%+ 下行空间, 还未计入增长再评级。反之, 重新加速至 30% 加上营业利润率扩张至 15%+, 可能将倍数重新评级至 15–18 倍。这种不对称性大致对称。68.9 倍远期 P/E 同样与 FY27 12.5% 营业利润率和 23% FCF 利润率所暗示的非 GAAP EPS 扩张挂钩。

**11. GAAP 亏损与 SBC 稀释 (重大)。** 从 FY26 –13.0 亿美元净亏损走向 GAAP 盈利的路径, 要么需要营收增长超过营业费用增长 (FY27 指引意味着进展, +27% 营收和适度的 opex 增长), 要么需要 SBC 占营收比例的有意义降低 (已从 41% 降至 34%)。两者均失败可能压缩股权叙事, 即便现金流仍然强劲。缓解: FY27 指引明确包含了营业利润率进展; 回购计划部分抵消稀释。

**12. 可转债再融资 (低-中等)。** Snowflake 拥有 2027 与 2029 年到期的零息可转换优先票据。2027 年的再融资条件将反映当时利率和 SNOW 股价轨迹。缓解: 40.3 亿美元现金 + 证券远超 27.4 亿美元总债务; 转换在今日股价下完全不在价内, capped-call 对冲限制稀释。

### 宏观经济风险

**13. 企业 IT 支出周期性 (中等)。** 云数据支出在企业 IT 中属于较有韧性的类别之一, 但不免疫于广泛预算削减。2026 年美国发生重大衰退将放缓新客户获取并减少扩展消费——FY24–FY25 的 NRR 压缩已经显示出消费优化在更紧预算周期中的运作。缓解: 关键工作负载定位和多年容量承诺限制任何单季度的下行。

**14. 地缘政治与中美科技脱钩 (低-中等)。** Snowflake APJ 业务为 2.71 亿美元 (约营收 6%), 集中于澳大利亚、日本、新加坡、韩国。直接中国敞口最小。出口管制与科技脱钩间接影响 Snowflake AI 产品所依赖的 GPU 的成本与可用性。缓解: 亚洲足迹小, 暴露间接而非直接。

**15. 利率与外汇敏感性 (低)。** 更高利率压缩增长倍数 (Snowflake 2022 年最大估值下修发生在实际收益率上行期间)。外汇暴露主要是 EMEA + APJ 营收的 EUR / GBP / JPY; 公司部分对冲。Beta 约 1.08 ([Yahoo Finance, SNOW 关键统计指标](https://finance.yahoo.com/quote/SNOW/key-statistics))。

## 10. 参考资料 (汇总)

以下条目为本报告所有事实性主张的核心来源。所有 URL 经过验证并以英文标题保留, 以便交叉检查。

**Snowflake SEC 文件 (主要):**

- [Snowflake 10-K, 截至 2026 年 1 月 31 日财年, 2026 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm)
- [Snowflake DEF 14A, 2026 委托书, 2026 年 6 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000019/snow-20260605xdef14a.htm)
- [Snowflake 10-K, 截至 2025 年 1 月 31 日财年, 2025 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000052/snow-20250131.htm)
- [Snowflake 10-K, 截至 2024 年 1 月 31 日财年, 2024 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014724000101/snow-20240131.htm)
- [Snowflake 10-K, 截至 2023 年 1 月 31 日财年, 2023 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014723000030/snow-20230131.htm)
- [Snowflake 10-K, 截至 2022 年 1 月 31 日财年, 2022 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014722000023/snow-20220131.htm)
- [Snowflake 10-K, 截至 2021 年 1 月 31 日财年, 2021 年 3 月提交](https://www.sec.gov/Archives/edgar/data/1640147/000164014721000073/snow-20210131.htm)
- [Snowflake S-1 IPO 招股说明书, 2020-08](https://www.sec.gov/Archives/edgar/data/1640147/000119312520203923/d18353ds1.htm)
- [Snowflake Q4 FY2026 业绩新闻稿, 2026-02-25 (8-K)](https://www.sec.gov/Archives/edgar/data/1640147/000162828026011631/fy2026q4earnings.htm)
- [Snowflake Q3 FY2026 业绩新闻稿, 2025-12-03 (8-K)](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000207/fy2026q3earnings.htm)
- [Snowflake 8-K, CFO Brian Robins 任命, 2025-09-03](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000181/ex991_pressrelease.htm)
- [Snowflake 8-K, CRO Jonathan Beaulier 任命与 FY27 指引重申, 2026-03-31](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000013/ex991_pressreleasex033126.htm)
- [Snowflake 8-K, 董事 Bill Scannell 任命, 2025-05-08](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000078/pressrelease-scannellbodan.htm)

**Snowflake 公司 / 投资者关系:**

- [Snowflake — Platform 产品页](https://www.snowflake.com/en/product/platform/)
- [Snowflake — Cortex AI 产品页](https://www.snowflake.com/en/data-cloud/snowflake-cortex/)
- [Snowflake — Marketplace 落地页](https://www.snowflake.com/en/data-cloud/marketplace/)
- [Snowflake — Customers 页](https://www.snowflake.com/en/customers/)
- [Snowflake — Investor Relations / Investor Day 2024 deck](https://investors.snowflake.com/events-and-presentations/events/event-details/snowflake-investor-day-2024)

**同业交叉引用:**

- [reports/company/MongoDB_NASDAQ_MDB 研究报告, 2026-05-20](MongoDB_NASDAQ_MDB_Research_Document_2026-05-20.md)
- [MongoDB 10-K FY2026](https://www.sec.gov/Archives/edgar/data/0001441816/000162828026016799/mdb-20260131.htm)
- [MongoDB Q4 FY2026 新闻稿, 2026-03-02](https://www.sec.gov/Archives/edgar/data/0001441816/000162828026013199/mdb-13126xex991xrelease.htm)
- [Datadog Q1 2026 业绩 8-K, 2026-05](https://www.sec.gov/Archives/edgar/data/0001561550/000162828026031677/ex-991x20260331x8k.htm)
- [Databricks Series J 新闻稿, 2024-12-17](https://www.databricks.com/company/newsroom/press-releases/databricks-secures-10-billion-financing-led-thrive-capital)
- [Databricks "Data Intelligence Platform" 产品页](https://www.databricks.com/product/data-intelligence-platform)

**市场数据:**

- [Yahoo Finance, SNOW 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/SNOW/key-statistics)
- [Yahoo Finance, DDOG 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/DDOG/key-statistics)
- [Yahoo Finance, MDB 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/MDB/key-statistics)
- [Yahoo Finance, ORCL 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/ORCL/key-statistics)
- [Yahoo Finance, MSFT 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/MSFT/key-statistics)
- [Yahoo Finance, GOOG 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/GOOG/key-statistics)
- [Yahoo Finance, PLTR 关键统计指标, 2026 年 5 月](https://finance.yahoo.com/quote/PLTR/key-statistics)
- [Macrotrends, SNOW 市销率历史](https://www.macrotrends.net/stocks/charts/SNOW/snowflake/price-sales)

**行业研究:**

- [Gartner 2025 云数据库管理系统魔力象限 — 新闻稿, 2025-01](https://www.gartner.com/en/newsroom/press-releases)
- [IDC FutureScape Worldwide Data Platforms 2024 Predictions](https://www.idc.com/getdoc.jsp?containerId=US51393623)
