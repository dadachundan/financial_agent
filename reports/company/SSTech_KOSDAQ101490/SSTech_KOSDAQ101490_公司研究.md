# S&S Tech (에스앤에스텍, KOSDAQ: 101490) — 公司研究

*截至 2026-05-26 — 首次覆盖*

> **更新 — 龙仁 (Yongin) EUV 中心 2025-10-15 落成，EUV 空白光罩 / 光罩坯料 (blank mask) 与 EUV 防尘薄膜 (EUV pellicle) 量产从 FY2026 一季度启动。** S&S Tech 于 2025-10-15 在京畿道龙仁举行专属 EUV 制造园区开幕仪式 — 一座六层、10,809 m² 的厂房，累计投入约 KRW 100 bn (~USD 72 m)，再叠加董事会 2024-12-04 决议追加的约 KRW 41.7 bn 资本支出 — 目标是在 2026 年初启动通过三星 (Samsung) 资格认证的 EUV 空白光罩与 EUV 防尘薄膜量产。创始人兼董事长郑寿弘 (정수홍, Jung Soo-hong) 已公开指引，EUV 商业化中长期可推动年营收从当前 KRW ~244 bn 量级上行至 KRW 300 bn–500 bn 区间 ([ZDNet Korea — 에스앤에스텍, EUV 블랭크마스크·펠리클 국산화 양산 시동, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601); [파이낸셜뉴스 — 에스앤에스텍 정수홍 인터뷰 "내년 초 EUV 블랭크마스크 양산", 2025-03-21](https://www.fnnews.com/news/202503211358486799); [Digitimes — Samsung, S&S Tech advance EUV mask localization, 2025-07-14](https://www.digitimes.com/news/a20250714PD206/samsung-euv-metal-mask-localization-production.html))。

---

## 目录

1. 公司概览
2. 公司历史
3. 管理团队
4. 产品与服务 — EUV 空白光罩重点章节
5. 客户与上市策略
6. 行业概览
7. 竞争格局
8. 市场机会 (TAM)
9. 风险评估
10. 参考资料

---

## 1. 公司概览

S&S Tech (에스앤에스텍，KOSDAQ: 101490) 是韩国唯一一家专注于 **空白光罩 / 光罩坯料 (blank mask)** 的特种材料供应商 — 这是半导体与平板显示晶圆厂将光刻图形写到硅片之前的最上游物理材料。空白光罩从材料厂运到独立的 photomask 厂 (光罩厂) 做电子束 (e-beam) 雕刻，之后再装到曝光机 (lithography scanner) 里完成图形转移。公司 **2001 年 2 月 22 日**在大邱 (Daegu) 由郑寿弘 (정수홍) 创立，2010 年 2 月 23 日在 KOSDAQ 上市，FY2025 期末共有 307 名员工，分布在大邱母厂、龟尾 (Gumi) 加工线，以及 2025 年 10 月落成的新建龙仁 EUV 中心 ([S&S Tech 公司简介, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub01_01.asp); [Stockanalysis.com — S&S Tech (KOSDAQ:101490) company profile](https://stockanalysis.com/quote/kosdaq/101490/company/); [ZDNet Korea — 용인 EUV 센터 준공, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601))。

产品矩阵的底层物理工序只有一个步骤: **在超净石英基板或低热膨胀材料 (LTEM, low-thermal-expansion material) 基板上沉积一层不透光的吸收膜栈 (光学版用 Cr / MoSi、EUV 版用 Ta 基吸收层加 Ru 钌覆盖层)，之后做化学机械抛光 (CMP) 把表面平整度推到 <1 nm，再涂光刻胶 (PR, photoresist) 并做缺陷检测**。空白光罩就是 photomask 厂的起点 — Photronics、Toppan/Tekscend、三星 / SK 海力士 / Intel 的自有光罩厂从 S&S Tech / Hoya / Shin-Etsu / AGC 采购 blank，用电子束写入芯片版图、刻蚀吸收层，再把成品 photomask 出货给晶圆厂 ([Semi-Engineering — Why Mask Blanks Are Critical, 2022](https://semiengineering.com/why-mask-blanks-are-critical/); [S&S Tech 제품소개 페이지, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp))。Blank 处于每一个 transistor 图形的最上游 — 如果哪怕一个略大于印制特征尺寸几分之一的粒子落在吸收层上，整张光罩就会报废 — 这也是为什么 **每平方厘米缺陷密度 (defects/cm²)** 是这一产品最重要的商业维度。

产品族 — 详见第 4 节 — 分为 **(a) 半导体空白光罩** (含成熟节点 i-line / KrF 用的 **二元光罩 (binary blank)**、ArF 浸没式光刻用的 **MoSi 衰减型相移光罩 (phase-shift mask, PSM)**，以及含 Mo/Si 多层膜加 Ta 基吸收层加 Ru 覆盖层的 **EUV 空白光罩 (EUV blank)**)，**(b) FPD 用空白光罩** (覆盖 G10.5 尺寸的 LCD / OLED 背板与彩色滤光片步骤)，**(c) 硬掩膜材料 (hardmask)** (一种在光刻胶下面化学定制的薄膜，能为先进图形提供刻蚀选择比，2024 年 8 月针对 High-NA EUV 推出了"新物质"代际)，以及 **(d) EUV 防尘薄膜 (EUV pellicle)** — 一张张在 mask 上方约 2 mm 处的高分子 / CNT 透明膜，挡住可能飞落在曝光像面上的颗粒 ([S&S Tech 제품소개 — 반도체용 블랭크 마스크 / FPD용 블랭크 마스크, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp); [ZDNet Korea — High-NA EUV 시대 신물질 하드마스크 개발, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957); [THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431))。

营收随韩国存储 / 代工厂晶圆投片量线性变化，同时叠加三星显示 (Samsung Display) / LG 显示 (LG Display) 面板向 OLED 切换的结构性增量; **FY2025 营收为 KRW 243.7 bn (+38.5% YoY)，营业利润 KRW 50.4 bn (OPM 20.7%)，净利 KRW 58.1 bn** — 这是公司同时跨过 KRW 200 bn 营收线和 20% 营业利润率线的第一个年度，对应过去四年的复合序列 KRW 89 bn (2021) → 117 bn (2022) → 150 bn (2023) → 176 bn (2024) → 244 bn (2025) ([Company Guide — 에스앤에스텍 A101490 Snapshot, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490); [Stockanalysis.com — S&S Tech 价格 + 财务, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/))。作对比参考，FY2025 营收**约相当于 Hoya 电子相关板块的 3%** (Hoya 该板块 FY25 营收 ¥265.2 bn ≈ USD 1.7 bn vs. S&S Tech 的 ~USD 180 m)，**但增速差异约 3 倍倾向 S&S Tech**，反映三星正在同步降低韩国对进口 mask blank 的依赖 ([HOYA FY25 IFRS Financial Statements, pp. 31, 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf))。

![S&S Tech 营收与营业利润率走势, FY2021–FY2025](../../charts/sstech_revenue_opm.png)
*资料来源: 基于 [Company Guide — 에스앤에스텍 A101490 Snapshot, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490) 与 [Stockanalysis.com — S&S Tech overview, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/) 整理 — FY2025 KRW 243.7 bn 营收，OPM 20.7%。*

![S&S Tech 营业利润与净利, FY2021–FY2025 (KRW bn)](../../charts/sstech_op_net.png)
*资料来源: 基于 [Company Guide — A101490 Financial Statements, accessed 2026-05](https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A101490&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701) 整理 — FY2025 营业利润 KRW 50.4 bn，净利 KRW 58.1 bn (净利 > 营业利润反映 FY2025 披露的投资性损益)。*

地理结构方面，客户基础**约 85% 韩国国内** (半导体侧为三星电子与 SK 海力士; FPD 侧为三星显示与 LG 显示)，剩余部分销往**中国存储 / 代工厂光罩厂 (Newway Photomask, SuperMask) 及台湾 photomask 厂** — 公司历史上不在 DART 披露按客户分项收入，董事长郑寿弘在 2025-03-21 CEO 访谈中口头描述三星 / SK 海力士 / LG 显示三家为"锚定客户" ([파이낸셜뉴스 — 에스앤에스텍 정수홍 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [전자신문 — 에스앤에스텍 정수홍 대표 인터뷰, 2019-02-11](https://m.etnews.com/20190211000156))。出货集中在韩国—中国—台湾客户群，意味着 S&S Tech 的营收节奏跟着 **K-半导体战略 (K-Belt 半导体主权战略)** 的晶圆厂资本周期走得比全球泛亚太 semi-cap 周期更紧 — 三星平泽 P4 时点、SK 海力士龙仁 M16-M17 时点、以及中国 Newway 扩产节奏对其季度波动的影响远大于任何全球性指标。

**估值快照 (截至 2026-05-26)。** S&S Tech 当前股价 **KRW ~77,200 / 股**，市值约 **KRW 1.64 万亿 (~USD 1.18 bn，按 KRW/USD 1,390)**，过去 52 周累计上涨 **+128.7%**，股价从 KRW 31,800 涨至 2026 年初 52 周高点 KRW 108,400 ([Stockanalysis.com — S&S Tech 价格与估值, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/))。基于 TTM (FY2025) 业绩，股票当前估值为 **P/E ~28.9×** (KRW 58.1 bn 净利 / 1.64 万亿市值)、**P/S ~6.7×**、**P/B ~5.1×**、**ROE ~27%** (基于 FY25 基数)，股息率约 **0.25%** ([Stockanalysis.com — S&S Tech statistics, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/); [Simply Wall St — S&S Tech ROE analysis, accessed 2026-05](https://simplywall.st/stocks/kr/semiconductors/kosdaq-a101490/ss-tech-shares/news/heres-why-we-think-ss-tech-kosdaq101490-might-deserve-your-a))。TTM P/E 较七家可比 (mask-blank / 韩国材料 / 日本 photomask) 公司均值 ~24.8× **高约 +16%** (Hoya 27.5×, Shin-Etsu 18.0×, AGC 12.5×, Toppan 14.0×, Dongjin Semichem 50.8×, FST 22.0×, S&S Tech 28.9×) — 这一温和溢价是市场为 EUV 资格认证 (qualification) 的可选性付费，但还没把它当作 base case 收入来定价 ([Stockanalysis.com — Hoya / Shin-Etsu / AGC / Toppan / Dongjin / FST 行情, accessed 2026-05](https://stockanalysis.com/list/kosdaq-stocks/); [Company Guide — Dongjin Semichem A005290 valuation, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A005290))。

![TTM P/E — S&S Tech vs. mask-blank / 韩国材料 / 日本 photomask 可比公司, 2026-05](../../charts/sstech_peer_pe.png)
*资料来源: 基于 [Stockanalysis.com — S&S Tech (KOSDAQ:101490), accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/), [Yahoo Finance — 7741.T / 4063.T / 5201.T / 7911.T, accessed 2026-05](https://finance.yahoo.com/quote/7741.T/), [Company Guide — Dongjin Semichem A005290, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A005290), 与 [Company Guide — FST A036810, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A036810) 整理。*

*分析师观点 (Analyst view):* 近端 de-rate 触发因素是 **三星 EUV 资格认证 (qualification) 时点滑动**。如果三星 2026 年 1 / 2 月的最终评估里程碑滑后 ≥6 个月，股价可能回吐过去一年 +128% 涨幅，因为当前 ~6.7× P/S 估值已经把 EUV 收入计入 FY2027F。反之，如果三星在 1H-FY2026 发出首批吨数级采购订单 (PO)，估值倍数可能向 Dongjin Semichem 50× 区间上行 — 详见第 8 节 (TAM) 与第 9 节 (风险)。

---
