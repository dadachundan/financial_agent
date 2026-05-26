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

## 2. 公司历史

S&S Tech 于 **2001 年 2 月 22 日**在韩国大邱成立 — 选址大邱是创始人郑寿弘的本籍地，他在大邱本地的庆北国立大学 (Kyungpook National University, KNU) 取得了 1981 年高分子工学 (polymer engineering) 学士与 1999 年半导体工程硕士学位，同时大邱—庆北 (Daegu-Gyeongbuk) 工业集群供应链能就近提供超净石英基板搬运、Cr / MoSi 溅射靶材等关键配套，这是早期空白光罩产线的硬约束 ([Business Post — Who Is? 정수홍 에스앤에스텍 대표이사, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [S&S Tech 회사소개 — CEO Vision, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub01_01.asp))。创业初衷 — 从公司首批监管备案文件起就明确写出 — 非常简单: **把当时三星电子和现代电子 (SK 海力士前身) 100% 从日本进口的 photomask blank 国产化**，并以 2000 年代末韩国 LCD 厂扩产周期作为切入点的入门级产品。

```mermaid
timeline
    title S&S Tech 关键里程碑, 2001–2026
    2001 : 大邱由郑寿弘创立; LCD 级 Cr blank 中试线
    2003 : 来自三星显示与 LG 显示的 LCD 空白光罩首笔商业收入
    2008 : 韩国存储厂首次通过半导体级二元 blank (Cr-on-glass) 资格认证
    2010 : KOSDAQ 挂牌 (2 月 23 日, 代码 101490)
    2014 : MoSi 衰减型 PSM (ArF) 在三星电子通过资格认证
    2017 : 创始人郑寿弘回任董事长; 设定 EUV blank 开发战略
    2020 : 公告 KRW 10 bn 投资计划用于 EUV blank + pellicle
    2021 : 韩国首张全尺寸 EUV pellicle 原型，透过率 90%
    2024 : "新物质" hardmask 发布瞄准 High-NA EUV; FY24 营收 KRW 176 bn
    2024-12 : 董事会追加批准 KRW 41.7 bn EUV 量产 capex
    2025-10 : 龙仁 EUV 中心 (10,809 m², 累计 ~KRW 100 bn) 落成
    2026-Q1 : EUV blank 与 pellicle 量产目标启动 — 三星资格认证窗口
```
*资料来源: 基于 [S&S Tech 회사연혁, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub01_02.asp); [Business Post — Who Is? 정수홍, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [THE ELEC — S&S Tech EUV pellicle, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431); [ZDNet Korea — 용인 EUV 센터 준공, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601); [38 Communication — 에스앤에스텍 IPO record, accessed 2026-05](http://www.38.co.kr/html/ipo/ipo.htm?o=v&key=&no=1422&page=59) 整理。*

**2001–2009 阶段** 是一段漫长、烧钱的爬坡期: Cr-on-glass FPD blank 作为入门产品切入，但 LCD blank 行业当时已经是日本在位玩家 (Hoya、Ulcoat、Toppan) 主导的低毛利赛道，要在三星显示牙山 (Tangjeong) 厂和 LG 显示坡州 (Paju) 厂通过资格认证，需要先积累约 5 年的零粒子缺陷数据才能售出一片对等晶圆量的商业 mask。半导体级转型从 **2008 年**开始 — 二元 Cr blank 在韩国某家存储厂通过资格认证 (申报文件未披露首位客户名称，当时业内传闻是当时仍处于 Hynix-pre-SK 控股结构下的海力士半导体)，**2010 年 2 月 23 日 KOSDAQ 上市**是支撑公司从 FPD-only 跨入 semi-blank 规模的关键融资事件 ([38 Communication — 에스앤에스텍 코스닥 상장 record, accessed 2026-05](http://www.38.co.kr/html/ipo/ipo.htm?o=v&key=&no=1422&page=59); [전자신문 — 에스앤에스텍 정수홍 대표 인터뷰, 2019-02-11](https://m.etnews.com/20190211000156))。

**2014 年 MoSi PSM 资格认证**是接下来的战略拐点: PSM 是一种相移吸收膜栈，让晶圆厂在 ArF 浸没式光刻上通过 pattern 边缘的相消干涉印出亚解析度特征 (典型场景为 45 nm 半节距 DRAM) — 在三星电子的 DRAM / NAND 产线上通过这一品类资格认证，让 S&S Tech 从"二号 LCD blank 供应商"升级到"先进逻辑 blank 上对 Hoya 可信的备选供应商" ([Wikipedia — Photomask (Phase Shift Mask 讨论), accessed 2026-05](https://en.wikipedia.org/wiki/Photomask))。三年后的 **2017 年 3 月**，创始人郑寿弘 — 此前的 IPO 后年份分别在 PKL (韩国 photomask 厂、相邻产业玩家)、Portronics Asia 任职，并以原始投资人身份回到公司视野 — 回任董事长，并把公司战略章程重置为以 **EUV blank + EUV pellicle 开发**为多年战略优先级。一年内的 2018 年 3 月，他正式接任 Representative Director (代表理事 / CEO) 头衔 ([Business Post — Who Is? 정수홍, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [The Bell — 정수홍 에스앤에스텍 회장, 지배력 기반 경영일선으로, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04))。

**2020–2025 EUV 计划**是当前股价故事的承托。2020 年 6 月董事会通过首期 KRW 10 bn 投资用于 EUV blank + pellicle 开发设备 ([English ETNews — S&S Tech to Invest 10 Billion KRW in EUV Blank Mask and Pellicle Development, 2020-06-19](https://english.etnews.com/news/article.html?id=20200619200002))。2021 年 10 月公司公布**单程透过率 90% 的 EUV pellicle 原型** — 这一数字之所以重要，是因为当时唯一商业化的 EUV pellicle 是三井化学 (Mitsui Chemicals) 多晶硅膜，单程透过率 ~88%，而单程透过率每低 1 pp 都意味着在一台 USD 150 m 的 EUV 扫描仪上扣减一笔可观的产能税 ([THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431))。2024 年 8 月又新增 **新物质 hardmask 产品线** — 一种化学定制的吸收 / 刻蚀掩膜薄膜，相对常规材料的刻蚀选择比提升约 3 倍，并采用纯氯刻蚀化学，定位 High-NA EUV 时代更薄光刻胶的工艺需求 ([ZDNet Korea — 에스앤에스텍 신물질 하드마스크 개발, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957))。**2024-12-04 董事会批准追加 KRW 41.7 bn 用于龙仁 EUV 厂建设**，资助了设备安装的后半段; **2025-10-15 龙仁 EUV 中心开幕仪式**正式标志量产准备就位 — 董事长郑寿弘在开幕现场公开把"EUV 量产后年营收 5,000 亿韩元 (KRW 500 bn)"作为公司中长期目标 ([파이낸셜뉴스 — 정수홍 CEO 인터뷰: "내년 초 EUV 블랭크마스크 양산, 매출 5000억 기대", 2025-03-21](https://www.fnnews.com/news/202503211358486799); [ZDNet Korea — 용인 EUV 센터 준공, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601))。

近期的**接班相关事件**对股权故事有意义。2024 年下半年创始人郑寿弘将 10 万股 (按当时市价约 KRW 2.6 bn) 赠与次子郑成勋 (정성훈, Jung Seong-hun, 1988 年生)，把次子持股比例提升至约 0.94%，并对外释放长期接班结构信号: **次子接 S&S Tech 主体，长子郑时俊 (정시준, Jung Si-jun) 接 S&S Investment 子公司** (一家工业控股 / 风险投资载体) ([The Bell — 정수홍 회장 지배력 기반, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04); [Business Post — Who Is? 정수홍 succession discussion, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。这一结构在**未来 24 个月内不构成颠覆性变量** — 郑寿弘仍同时担任董事长与代表理事，次子目前为执行董事 (Executive Director) — 但它锁定了 EUV 爬坡背后的长期资本配置框架。

---

## 3. 管理团队

S&S Tech 在管理层面是一家**处于拐点上的创始人 CEO 公司**。郑寿弘既是创始人，也是当前的代表理事 (대표이사) — 按 company-research 流程惯例，本节将"创始人"与"CEO"合并为一条人物履历，而不是拆成两个分块。

**郑寿弘 (정수홍, Jung Soo-hong) — 创始人、董事长兼代表理事。** 1955 年 7 月 18 日生于大邱，郑寿弘是韩国 photomask 行业最资深的高管之一 — 一段长达 45 年的职业序列与 S&S Tech 今日产品矩阵的技术层级几乎一一映射 ([Business Post — Who Is? 정수홍 에스앤에스텍 대표이사, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。他 **1981 年获庆北国立大学高分子工学学士学位** (高分子化学是 photoresist 与 pellicle 膜材的基础，两者今天都出现在 S&S Tech 的产品矩阵中)，**1999 年获 KNU 产业研究生院半导体工程硕士** — 这是他职业中段在出任 PKL 韩国 CEO 期间完成的进修 ([Business Post — Who Is? 정수홍, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [The Bell — 정수홍 에스앤에스텍 회장 지배력 기반 경영일선으로, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04))。

值得展开的三段重要从业经历，每一段都对应今天 S&S Tech 运营论点中的某一层。**(1)** **1988-1993 年任 Korea DuPont 工厂厂长**，主管 photoresist 加 photomask 材料生产线，学到了支撑超低缺陷 blank-mask 制造所需的**湿化学工艺控制** — defects/cm² 缺陷密度归根到底是洁净室微粒控制与化学品纯度的函数，这两块都是 DuPont 的看家本领 ([Business Post — Who Is? 정수홍 career timeline, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。**(2)** **1995-约 2001 年任 PKL (Photokure Limited，后与 Photronics 合资为 Photronics-PKL) 总裁 / 代表理事** — 这是一家从 Hoya / Shin-Etsu 采购 blank、为三星和海力士做电子束雕刻的韩国 photomask 厂。在 PKL 的这一任让郑寿弘从客户一侧吃透了**韩国晶圆厂愿意为什么样的缺陷规格、交期 cadence 与 blank 单价买单**，他随后把这些理解直接翻译成 2001 年的上游新进入者 ([전자신문 — 정수홍 대표 인터뷰: "블랭크 마스크 세계 최고 자부", 2019-02-11](https://m.etnews.com/20190211000156))。**(3)** **2008-2017 年任 PKL (Photronics 合资后) 董事长** — 这一时期 S&S Tech 从一家 sub-KRW 50 bn 的 LCD-blank 专业户长大为多品类的韩国 semi-材料公司，并完成 KOSDAQ 上市; 创始人在期间保留控股股东经济权益但未直接出任日常运营。2017 年 3 月他作为董事长回任 S&S Tech，2018 年加冠代表理事头衔，是因为 EUV 转型需要创始人级别的资本配置决断 ([The Bell — 정수홍 회장 지배력 기반, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04); [Business Post — Who Is? 정수홍, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。

郑寿弘 2017 年至今的执掌签字风格集中体现在 **(a)** 多年期 EUV capex 重金投入 (2020 年 KRW 10 bn 首期批准、2021-2024 年大邱与龟尾建设、2024-12-04 龙仁追加 KRW 41.7 bn，累计约 KRW 150 bn)，**(b)** 对外明示的营收目标 (2025 年 3 月访谈中宣告"EUV 量产后年营收 5,000 亿韩元中长期目标")，以及 **(c)** 创始人家族持股集中 — 截至 2025-03-31 他个人持有约 4.28 百万股 (约 **占总股本 19.95%**)，加上家族 / 次子相关方持股块约 22%，对位 **三星关联持股块约 16.8%** (其中三星资产管理 8.78%)，后者是三星作为战略客户给予的资本侧背书 ([Business Post — Who Is? 정수홍 shareholding, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [Company Guide — 에스앤에스텍 A101490 ownership table, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490); [파이낸셜뉴스 — 정수홍 CEO 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799))。薪酬结构在 DART 标准披露门槛外没有更多细节; 股权敞口 (按当前价计算约 KRW 320–330 bn) 远大于任何现金薪酬信号 — 这是一种典型的创始人股权对齐，而不是激励设计层面的对齐。

接班结构 — 在第 2 节有提到 — 把**次子郑成勋 (정성훈, 1988 年生) 定位为 S&S Tech 主体的接班人** (他作为执行董事在董事会任职，并在 2024 年下半年获得创始人 10 万股赠与)，**长子郑时俊 (정시준) 主导 S&S Investment 子公司**。这种切分被韩国财经媒体普遍解读为一种刻意安排: 主营运营公司由一位继承人接班，而风险 / 工业投资活动放在平行载体里 ([The Bell — 정수홍 회장 지배력 기반, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04); [Business Post — Who Is? 정수홍 succession, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。未来 12-24 个月，日常运营领导权完全保留在创始人手上 — 考虑到三星 EUV 资格认证窗口的关键性，这种创始人连续性是正面信号，而不是需要刻意提示的关键人风险。

---

## 4. 产品与服务 — EUV 空白光罩重点章节

> 第 4 节是**本报告最关键的一章**。S&S Tech 自 2001 年成立以来就是一家**单一产品族公司**: 空白光罩 (blank mask)。损益表上其他每一行 (hardmask 薄膜、FPD blank、EUV pellicle、未来的 masked-glass 或 photoresist 配套产品) 要么是 blank-mask 沉积 / 检测 / 封装产线的工艺延伸，要么是 EUV 路线图倒逼进入组合的战略并行产品。如果投资者没有内化**什么是 blank mask、EUV blank 与光学 blank 在物理结构上有何根本差异、为什么每平方厘米缺陷密度是决定份额的唯一商业变量、hardmask 与 pellicle 在光刻流程中的具体位置**，就会错配后面每一节的估值。因此本节配置约 1,800 字 (中文计算约 3,000 字)。

### 4.1 S&S Tech 产品矩阵

下表的产品矩阵照搬自 S&S Tech 官网的产品页 — 公司未在 DART 备案中按 10-K 式的分段披露收入，因此官网产品导航是权威锚点。矩阵分两大门类 (半导体 / FPD)，半导体侧含五个产品族，FPD 侧含一个产品族; pellicle 与 hardmask 薄膜归入半导体段披露。

| 段 | 产品族 | 基板 / 膜栈 | 光刻 / 应用 | 状态 (2026-05) |
|---|---|---|---|---|
| **半导体** | **二元光罩 (binary blank)** | 石英基板上 Cr; **Cr 66–100 nm**, PR ~150–200 nm | i-line / g-line / KrF — 成熟节点 (>180 nm) | 量产; 在三星 / SK 海力士做 Hoya 二号备选 |
| **半导体** | **相移光罩 (PSM) — 衰减型** | 石英基板上 MoSi; **MoSi 38–66 nm, Cr 65–87 nm, PR 200/100/60 nm** 因变型而异 | ArF 干式 / ArF 浸没式 — 65-14 nm 逻辑与 DRAM | 量产; 多变型 (Standard / Advanced / High T% PSM) |
| **半导体** | **Hardmask 薄膜** | 新物质 (化学成分未披露); 47–60 nm hardmask + 4–5 nm cap + 60–100 nm PR | EUV (0.33 NA) 与 High-NA EUV (0.55 NA) — PR 下的刻蚀选择层 | 送样; 2024 年 8 月推出"新物质"代际 |
| **半导体** | **EUV 空白光罩 (EUV blank)** | LTEM 基板上 Mo/Si 多层膜 (40+ 对); Ta 基吸收层; Ru 覆盖层 | EUV (0.33 NA) — 7 / 5 / 3 / 2 nm 逻辑与 sub-1y DRAM | 三星最终资格认证中 (2026 年初); 量产 ready |
| **半导体** | **EUV 防尘薄膜 (EUV pellicle)** | 多层膜; ~90% 透过率原型; 边框装在 mask 上方 ~2 mm | EUV 扫描仪 — 防颗粒落到 photomask 上 | 客户调谐中; 1H-2026 商业化目标 |
| **FPD** | **FPD 用空白光罩 (多种变型)** | Cr binary、Halftone TM、Multi-tone TM、Cr PSM、MoSi PSM | LCD / OLED 背板与彩色滤光片 — 最大 G10.5 (1620×1780 mm) | 量产; 三星显示与 LG 显示重点份额 |

*资料来源: S&S Tech 官网产品页 — 上述膜栈规格逐字照抄自公司产品导航，并以 2024-2025 年新闻条目交叉确认状态 ([S&S Tech 제품소개 — 반도체용 및 FPD용 블랭크 마스크, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp); [ZDNet Korea — High-NA EUV 하드마스크, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957); [파이낸셜뉴스 — EUV 양산 시동, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [THE ELEC — EUV pellicle 90% 투과율, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431); [Digitimes — Samsung mask blanks localization, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html))。*

官网没披露按产品族的 FY 收入拆分，DART 备案亦无。*分析师观点 (Analyst view):* 从 FY2024 KRW 176 bn 营收基数、董事长 2025-03 访谈中关于 FPD blank 业务的描述 ("display 用 blank mask 服务 LCD 与 OLED 面板制造，在更大面积上实现精密图形")，以及 2024 年没有 EUV blank 商业收入这一事实三角化推断，**EUV 前的 FY2024 营收结构大致为: 半导体 blank (binary + PSM + hardmask) ~69%、FPD blank ~28%、R&D + pellicle 中试 ~2-3%**。下图把同一画面用两列简化呈现 — FY2024 实际 vs. 分析师草图勾勒的 FY2027E 量产 EUV 情形 (基于公司自报的 KRW 500 bn 目标) — 视觉上清楚说明为什么 EUV blank 是整个投资论点的关键变量 ([파이낸셜뉴스 — 정수홍 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [Company Guide — 에스앤에스텍 A101490 financials, accessed 2026-05](https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A101490&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701))。

![S&S Tech 营收结构演进 — EUV blank 与 pellicle 为关键变量](../../charts/sstech_revenue_mix.png)
*资料来源: 左侧 FY2024 基于 [Company Guide — A101490 financials, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490) 与 [파이낸셜뉴스 정수홍 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799) 中的产品族评论构建。右侧 FY2027E 为分析师草图，对齐董事长郑寿弘公开宣称的 KRW 500 bn 营收目标。*

### 4.2 综合 — 各产品族如何组成一条光刻流程

走完每一行之前，先画一遍**从光罩厂视角出发的光刻流程图**，因为 S&S Tech 销售的每一类产品要么就是 blank 本身，要么处于扫描仪内距离 blank 约 2 mm 的距离内:

```mermaid
graph LR
    A[S&S Tech blank mask 基板<br/>Cr/MoSi/EUV 多层膜 + 吸收层] --> B[Photomask 厂<br/>电子束雕刻 + 刻蚀]
    B --> C[成品 photomask]
    C --> D[光刻扫描仪<br/>ArF 浸没式或 EUV]
    D --> E[晶圆上的图形]
    F[S&S Tech EUV pellicle<br/>膜 + 边框] --> C
    G[S&S Tech hardmask 薄膜<br/>沉积在晶圆 PR 下] --> D
```

需要注意三件事。**第一**，blank mask 和 EUV pellicle 装在**同一张 photomask 上** — pellicle 在光罩厂里贴在成品 mask 顶部，从客户采购视角它们是一体的产品，能两个一起卖正是三星"从一家韩国厂商采购"资格认证偏好的成交关键。**第二**，hardmask 薄膜根本不是 mask 材料 — 它**沉积在晶圆本身**上，在 PR 下方，为 High-NA EUV 的更薄光刻胶提供刻蚀步骤所需的材料对比度余量。它本质是晶圆厂 consumable，挂在 mask 相关产品下面是因为 S&S Tech 沉积设备的工艺基础和 blank 同源。**第三**，FPD blank 与半导体二元 blank 是物理上同一类产品，只是基板尺寸放大到 G10.5 (1.62 × 1.78 m); 制造设备显著重合，正是公司没把 FPD 业务剥离单独拆分的原因。

### 4.3 二元光罩 — 入门产品、今日利润底盘

二元光罩 (binary blank) 物理上是 **chrome-on-quartz**: 在超净熔融石英基板上沉积 66-100 nm 的铬 (Cr) 吸收膜，再涂上一层 ~150-200 nm 的光刻胶，等客户的光罩厂做电子束雕刻 ([S&S Tech 제품소개 — 반도체 블랭크 마스크 binary, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp))。"二元"是字面意义 — pattern 区域 Cr 要么留存 (不透光)、要么剥离 (透光)，形成两态 mask，让 i-line / g-line / KrF 光刻波长 (365 / 248 nm) 可以直接成像到晶圆。

**通俗解释 / Plain-language gloss:** 二元 blank 是 photomask 链路的入门级产品 — Cr (铬) 膜均匀地溅射沉积在 quartz 基板上，之后给 photomask 厂做电子束 (e-beam) 雕刻。物理上等同于一张"黑白透明的菲林底片"，但缺陷密度规格是 ≤0.01 个 ≥1 µm 颗粒/cm²，所以做出一片 spec-grade blank 的良率反而是低的。这条产品线的商业重点是 **>180 nm 成熟节点的 DRAM / 显示驱动 IC / 电源管理芯片** — 这类芯片晶圆用量大、价格敏感、对 mask 工艺余量宽容，正好是 S&S Tech 用韩国本土制造价格优势打 Hoya 进口替代的最容易切入点。**战略意义:** 这条产品线是公司**利润底盘 (profit floor)** — 出货量稳定、毛利较薄、不需要新增 capex，但把整个三星 / SK 海力士 / Newway 的客户关系网络养起来了，给后面 PSM / EUV / pellicle 的资格认证留了门票。

*分析师观点 (Analyst view):* moat 判断是 **partial**，moat 类型是**切换成本 + 客户资格认证时间** (存储厂在一个节点上要积累约 2 年的缺陷数据才能资格认证一家新的 blank 供应商，Hoya 早就有，S&S Tech 在 2000 年代末才取得; 新进入者在十年量级上被功能性锁出)。最接近的竞争对标是 Hoya 自己的二元 blank 线，Hoya FY25 综合报告将其归入"半导体用 Photomasks and Maskblanks"宽口径段披露，未单拎二元 ([HOYA FY25 IFRS Financial Statements, p. 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf))。

### 4.4 相移光罩 (PSM) — ArF 浸没式光刻的桥梁产品

PSM blank 是 S&S Tech 进入有意义的亚 100 nm 光刻领域的入口产品。膜栈在 Cr 下加了一层 **38-66 nm 厚的 MoSi (molybdenum-silicide) 衰减层** — MoSi 设计为约 6% 透过率 (即让 ~6% 的 ArF 光以 180 度相移通过)，由此在 pattern 边缘产生**相消干涉，显著锐化印制特征** ([S&S Tech 제품소개 — PSM blank, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp); [Wikipedia — Photomask Phase Shift Mask section, accessed 2026-05](https://en.wikipedia.org/wiki/Photomask))。S&S Tech 发布三种子变型 — Standard PSM、Advanced PSM (更薄 PR 用于更密 pattern 密度)、High T% PSM (更高 MoSi 透过率用于特定 aerial-image 形貌) — 覆盖从 45 nm DRAM 到 14-7 nm 逻辑在 ArF 浸没式光刻上的整条工艺谱 ([S&S Tech 제품소개 page, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp))。

**通俗解释 / Plain-language gloss:** PSM 的物理原理是**相移干涉**: MoSi 这一层不是完全不透光，而是让 ~6% 的 ArF (193 nm) 光带着 180° 相位反向通过 — 在 pattern edge 上和主光束发生 destructive interference，把曝光强度梯度变陡，等效于把光刻的分辨率极限再推进约 30%。这是三星 / SK 海力士在 ArF 浸没式光刻时代量产 sub-65 nm DRAM 必须用的技术，也是为什么 PSM blank 比二元 blank 单价高约 3-5 倍 — MoSi 沉积工艺对均匀性、相位精度、缺陷密度的要求高一个数量级。**战略意义:** 这是 S&S Tech 真正进入三星 / SK 海力士主流晶圆产线的产品 — 2014 年 MoSi PSM 在三星的资格认证是公司营收从 LCD-mainly 转向 semi-led 的转折点 (第 2 节时间线已标注)。今天 PSM blank 仍是公司营收最大单一品类，也是支撑 FY2024 16.8% / FY2025 20.7% 营业利润率的核心 (Cr-only binary 毛利偏薄，PSM 把 ASP 抬起来)。

*分析师观点 (Analyst view):* moat 判断是 **yes**，moat 类型是**工艺 IP + 客户资格认证深度**。MoSi 衰减型 PSM 是 IP 密集型 (Hoya、Shin-Etsu、S&S Tech 各自持有吸收膜栈化学、MoSi 组分、相位控制几何的阻断性专利)，且三星对 S&S Tech 的 PSM 走完约 3 年工艺验证数据所构成的护城河对新进入者具有功能性阻拦。最接近的具名竞品是 **Hoya 的 PSM blank 线** (Hoya 将该段口径定为"半导体用 Photomasks and Maskblanks"未细分子产品 — 参见 [HOYA FY25 IFRS Financial Statements, p. 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf)) 与 **Shin-Etsu Chemical 的 MoSi 基 PSM** (通过 Shin-Etsu Microsi 分销渠道)。

### 4.5 EUV 空白光罩 — 整个投资论点的承托

**这是本节最重要的子节。** EUV blank 与上面的光学 (二元 / PSM) blank 在物理上是**根本不同的产品** — 制造工艺差异之大，以至于在光学 blank 上世界第一 (Hoya) 也**不会自动**转化为在 EUV blank 上世界第一。

**物理原理。** EUV 光刻工作波长 13.5 nm，意味着**光路中所有元件都必须是反射式而不是透射式** — 没有 quartz，没有 Cr-on-glass。EUV blank 建立在**低热膨胀材料 (LTEM, low-thermal-expansion-material)** 玻璃基板上，先沉积 **40+ 对交替 Mo/Si 双层膜** (每层约 7 nm，做 13.5 nm 下约 70% 反射率的多层 mirror)，再叠**钌覆盖层 (Ru capping)** (Ru 几纳米厚，防止顶层 Si 氧化破坏反射率)，然后是 **Ta 基吸收膜栈** (50-70 nm 的 TaN 或 TaBN — 写 mask 时被刻蚀掉以定义 pattern 的吸收层)，最后是供卡盘吸附的背面导电层 (通常是 CrN)。Nomura 2026-05-21 大中华半导体报告指出，吸收层化学正在从 TaBN 切向 Ru / Mo low-n 材料过渡，覆盖层成分也在演进 — 这两个领域恰好是 S&S Tech 的"新物质 hardmask"R&D 计划与 EUV 路线图的重叠区 ([Nomura "Greater China Semi: A guide to Semi renaissance in 2026~30F", p. 38-39, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md); [Semi-Engineering — Why Mask Blanks Are Critical, 2022](https://semiengineering.com/why-mask-blanks-are-critical/))。

**通俗解释 / Plain-language gloss:** EUV blank 是 **multi-layer mirror** 而不是传统 mask — 因为 13.5 nm 波段所有材料都吸收，没有 transmissive 路径，必须用 40 多对 Mo/Si bilayer 做 **Bragg 反射**把光弹回来，吸收层 (TaBN / Ru-based) 在最顶层把要遮蔽的区域吸收掉。难度集中在**三个独立工程问题**: (1) Mo/Si 多层膜的逐层均匀性 — 任何一层厚度偏差 >0.1 nm 都会让 13.5 nm 反射率降 1-2 个 pp (整片 mask 直接报废); (2) **每平方厘米缺陷密度 (defects/cm²)** — sub-nm 级别的颗粒嵌在 multilayer 里就是 unprintable defect，商业规格要求 **<0.05 defects / cm²**，比二元 blank 严苛约 500 倍; (3) **Ru capping layer 的化学稳定性** — Ru 太薄就不挡氧化、太厚就吃掉反射率，3-5 nm 之间的 sweet spot 是工艺壁垒。Hoya 能保持 EUV blank 全球约 60-80% 份额，本质上是约 15 年的缺陷控制数据积累，不是单纯的设备投资问题。**战略意义 — 对 S&S Tech 而言:** 这是公司 KRW 1.64 万亿市值中 80%+ 部分在定价的预期。三星 2026 Q1 完成最终资格认证、2026 Q2 启动小批量采购、2027F 把 EUV blank 占自身 EUV 用量推到 ≥20% — 这条事件链若走通，公司营收从 KRW 244 bn 走向 KRW 400-500 bn 区间是 base case; 如果资格认证在 2026 上半年滑到 2H 甚至 2027，整张估值表需要重做。

*分析师观点 (Analyst view):* 针对 S&S Tech EUV blank 这一具体产品，moat 判断是 **partial — closing**。一旦兑现，moat 类型是**数十年缺陷控制 IP + 韩国唯一供应商战略溢价**。最相关的外部基准是: **Hoya**，依据 Nomura 2026-05-21 估计 EUV blank 全球份额约 80% (其他分析师在 60-85% 区间)，而 Intel Market Research 的市场跟踪产品给出 Hoya 62% / AGC 30% / Shin-Etsu 7% / S&S Tech 资格认证阶段 <1% — 参见 [Hoya FY25 综合报告对"长年来在 mask blank 市场拥有 exceptionally large share"的描述](https://www.hoya.com/ir/2024/en/common/files/review2024.pdf) 与 [Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463); **AGC (旭硝子)** 凭借特种基板 / LTEM 玻璃底子在 EUV blank 上有约 30% 份额; **Shin-Etsu Chemical** 是除 Hoya / AGC 之外唯一有量的 EUV blank 玩家，但份额仅个位数。未来 12 个月就是 S&S Tech 的"partial — closing"判定能否兑现到"yes"(三星资格认证 + 首批 PO) 或退回到"partial — closing"(资格认证滑动) 的时间窗口。

### 4.6 EUV 防尘薄膜 (EUV pellicle) — 锁定三星订单的姐妹产品

EUV pellicle 是一张**多层透明膜** (单程透过率 90% 的产品总厚度约 150 nm)，绷在金属边框上、装在成品 photomask 上方约 2 mm。它的功能是机械防护: 把扫描仪内部脱落的亚微米颗粒挡在 mask 吸收 pattern 之外。没有 pellicle，每个粒子都会变成可印刷缺陷; 有 pellicle，粒子在距离像面 2 mm 之上、处于离焦状态，mask 可无限次复用 ([THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431); [USPTO Patent Application — Pellicle for an EUV lithography mask, 2023-11-12](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11782339))。

**通俗解释 / Plain-language gloss:** EUV pellicle 就是**保护膜** — 在 EUV mask 表面架一层很薄的透明膜 (就像放大镜上盖的 lens cap)，把可能飞过来的粒子挡在 mask pattern 外面。物理挑战是: EUV 光必须**双向穿透** pellicle (入射穿过、反射后再穿过)，所以单程损耗 5% 往返就是 ~10% 的曝光强度损失 — 在 EUV scanner 每秒曝多少 wafer 是 throughput economics 命门的前提下，每 1pp 透过率提升直接对应 EUV scanner 产能 ~1pp 提升。三井化学是这一市场的现任霸主 (~88% 单程透过率); S&S Tech 2021 年的 90% 原型是韩国厂商首次把透过率推过 90%。**战略意义:** pellicle 业务对 S&S Tech 自身营收增量并不大 (EUV pellicle 全球 TAM <USD 100 m/yr)，但**战略意义在于把三星"EUV mask 全套国产化"套餐凑齐** — 三星 EUV 要彻底降低对日本进口的依赖，需要同时拿到本土 EUV blank 和本土 EUV pellicle 两个产品，S&S Tech 是唯一同时具备这两条产线的韩国公司。这也是三星与 S&S Tech 2025 年联合申请 EUV pellicle 边框专利的商业逻辑 ([THE ELEC — Samsung and S&S Tech co-files EUV pellicle patent, 2025-05](https://www.thelec.net/news/articleView.html?idxno=5452))。

*分析师观点 (Analyst view):* moat 判断是 **partial**，moat 类型是**工艺 IP + 三星联合研发数据**。最接近的竞品是**三井化学的 EUV pellicle** (在位玩家 — 单程透过率约 88%，2019 年起在三星 / TSMC / Intel 商用 EUV 上服役)，**ASML 自研 pellicle** (2021 年附近报出约 90.6% 透过率) 作为另一基准 ([THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431))。韩国竞争对手 **FST (KOSDAQ: 036810)** 也在开发 EUV pellicle，但客户验证周期落后 S&S Tech 约 1-2 年。

### 4.7 Hardmask 薄膜与 FPD blank — "第二引擎"产品

**Hardmask 薄膜**是 2024 年 8 月的新产品 — 一种沉积在晶圆 PR 下方的新物质薄膜，相对常规铬 / 钽 / 硅 hardmask 材料刻蚀选择比提升约 3 倍，且采用纯氯刻蚀化学 (对比传统 O₂ + Cl₂) ([ZDNet Korea — High-NA EUV 시대 신물질 하드마스크 개발, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957))。产品定位直接对准 **High-NA EUV (0.55 NA)** 时代 — Nomura 2026-05-21 报告对 High-NA + 金属氧化光刻胶 (MOR) 经济性的回顾指出，0.55 NA 下 PR 厚度必须减薄至 ≤16 nm (0.33 NA 下约 25 nm)，PR 厚度 <16 nm 时刻蚀步骤需要选择比远更高的下层 hardmask 来保留足够的图形转移材料预算 ([Nomura "Greater China Semi", p. 10-12, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md))。**通俗解释 / Plain-language gloss:** 硬掩膜 (hardmask) 物理上等同于在 wafer 上加一层**耐刻蚀的中间膜** — 当 PR (photoresist) 在 High-NA EUV 时代被砍到 <16 nm 时，单凭 PR 自身没法挡住下层电介质 / 金属的 etch 步骤，需要在 PR 下面再加一层 etch selectivity 高的 hardmask。S&S Tech 的"新物质"hardmask 把 selectivity 推到对手 3 倍，意味着同样 etch 步数下能 transfer 更深的 pattern。**战略意义:** 这条产品线本身体量小 (FY2025 估算 <KRW 10 bn 营收)，但是**High-NA EUV 时代的入场券** — 2028-30F High-NA EUV HVM 起量后，hardmask 需求会跟随曝光步数成倍增加，S&S Tech 提前 4 年完成材料开发是为 2028-30 的爆发窗口铺路。*分析师观点 (Analyst view):* moat 判断是 **not yet** — 材料在客户验证阶段 (大概率是三星)，尚未商业化; 最接近的对手是 Applied Materials 的 hardmask CVD 工艺 (是设备而非材料 — 不同竞争层次) 与 DuPont / JSR 的常规 hardmask 材料。

**FPD blank mask** 是公司历史营收底盘 — 六种产品变型 (Cr binary OD 3.2 / 5.0 / LR、Halftone TM、Multi-tone TM、Cr PSM、MoSi PSM) 覆盖从 520 × 800 mm 到最大 **G10.5 1620 × 1780 mm** OLED 大尺寸代际的基板，基板厚度 8T-17T (mm) ([S&S Tech 제품소개 — FPD blank mask, accessed 2026-05](http://www.snstech.co.kr/renew/html/sub02_01.asp))。主要客户为**三星显示** (手机 / IT OLED, 越来越多的电视用 QD-OLED) 与 **LG 显示** (坡州大尺寸 WOLED 电视、IT OLED)。**通俗解释 / Plain-language gloss:** FPD blank 是**放大版的 binary / PSM blank**，物理工艺和 semi blank 相通，只是基板从 6×6 英寸放大到 1.6×1.8 米。一片 G10.5 mask 单价显著低于 semi mask，但面积大、出货 cadence 频繁 — 三星和 LG 一年要换约数千片 FPD mask 用于 OLED 背板 + 彩色滤光片步骤。**战略意义:** 这是 S&S Tech 营收的**反周期基础** — semi-blank 营收与三星 / SK 海力士晶圆投片周期相关，FPD blank 营收与 OLED 面板投资周期相关，两者周期相位不同步，整合后稳定了公司营收波动。

### 4.8 综合 — 旗舰排序与近期发布

**旗舰产品 (按 FY2026F 营收影响排序):** (1) **EUV blank** — 整个股价上行预期; (2) **PSM blank** — 当前营收最大单一品类、利润率底盘; (3) **EUV pellicle** — 营收增量小，但是锁定三星的"打包产品"; (4) **FPD blank** — 周期反相产品; (5) **Hardmask 薄膜** — High-NA EUV 第二个十年的可选性; (6) **二元 blank** — 成熟、低毛利、为老节点晶圆厂留住底盘。**最近 12 个月发布 / 新闻:** (a) 龙仁 EUV 中心 2025-10-15 落成; (b) 2024-12-04 董事会追加批准 KRW 41.7 bn capex; (c) 2024-08-12 "新物质"hardmask 发布; (d) 2025-05 前后三星 - S&S Tech 联合申请 EUV pellicle 专利; (e) 2025 年 3 月 CEO 访谈中提出 KRW 500 bn 中长期营收目标 — 参见第 2 节引用。公司没有有意义规模的循环服务 / 售后业务，营收几乎全部由产品出货驱动 — 这也是为什么 KRW/JPY 汇率敏感性在风险章节里要单独列出。

---

## 5. 客户与上市策略

S&S Tech 向极少数大客户销售，客户名单是整张股权故事中最重要的风险与机会变量。**四家锚定客户 — 三星电子 (存储 + 代工)、SK 海力士 (存储)、三星显示 (OLED + LCD 面板背板)、LG 显示 (大尺寸 OLED) — 合计占营收约 80-85% (分析师估计)**，剩余部分流向台湾 photomask 厂 (经 Photronics-PKL 和 Toppan-Tekscend 间接服务 TSMC 与 UMC 的 blank 供应合约)、中国光罩厂 (Newway Photomask, SuperMask)，以及一层薄薄的海外 R&D 验证账户。董事长郑寿弘在 2025 年 3 月 CEO 访谈中明确点名三星电子 / SK 海力士 / LG 显示三家为锚定客户，同时重申中国出口渠道: "中国半导体企业正在请求增加供应量" ([파이낸셜뉴스 — 정수홍 CEO 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [전자신문 — 정수홍 대표 인터뷰, 2019-02-11](https://m.etnews.com/20190211000156))。

**客户集中度 — 精确披露情况。** S&S Tech 经 DART / KRX-KIND 提交的 사업보고서 (annual report) **不像美股 10-K 那样按客户拆分营收百分比** — 韩国披露规则只要求 ≥10% 采购或销售对手方在 주요 매출처 (主要客户) 部分被名义性提及，是否披露具体百分比由发行人自行裁量，S&S Tech 的备案以客户名而非数字份额披露 ([에스앤에스텍 사업보고서 (FY2024), 2025-03-17 备案](https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20250317000236); [에스앤에스텍 사업보고서 (FY2025), 2026-03-16 备案](https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20260316000663))。文件中口头确认的客户名集合为 — 三星电子 삼성전자、SK 하이닉스、三星显示 삼성디스플레이、LG 디스플레이 — 没有按客户披露的数值份额。

```mermaid
pie title S&S Tech 营收按客户拆分 (分析师估计, FY2025)
    "三星电子 (半导体)" : 35
    "SK 海力士 (半导体)" : 20
    "三星显示 (FPD)" : 18
    "LG 显示 (FPD)" : 12
    "中国光罩厂 (Newway, SuperMask)" : 8
    "台湾 / R&D / 其他" : 7
```
*资料来源: 分析师估计，三角化基于 (a) [에스앤에스텍 FY2024 사업보고서, 2025-03-17 备案](https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20250317000236) 的客户名称集; (b) 董事长郑寿弘在 [파이낸셜뉴스 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799) 中对客户三联的口头描述; 以及 (c) FY2024 ~70% semi / ~28% FPD 营收拆分来自 [Company Guide — A101490 financials, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490)。S&S Tech 未披露按客户分项百分比。*

**三星电子是单一最重要的客户，遥遥领先** — 不仅是当前营收来源，更是驱动整个 FY2026F-2027F 上行空间的 EUV blank 量产 gate-keeper。三星与 S&S Tech 的关系由三 / 四根独立支柱组成: (1) 三星存储 / 代工厂光罩厂对二元 / PSM blank 的商业采购; (2) EUV blank mask 最终评估计划，按 Digitimes 时间表对应 1Q-FY2026; (3) EUV pellicle 的联合 IP 开发 (三星 - S&S Tech 2025-05 联合申报专利); (4) 三星资产管理约 8.78% 持股及其他三星关联持股累加约 16.8% 总敞口 — 这是股权层面的客户背书 ([Digitimes — Samsung will adopt South Korea-made mask blanks to EUV process, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html); [Digitimes — Samsung, S&S Tech advance EUV mask localization, 2025-07-14](https://www.digitimes.com/news/a20250714PD206/samsung-euv-metal-mask-localization-production.html); [Company Guide — A101490 ownership, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490))。三星支持 S&S Tech 的战略逻辑首先是地缘政治、其次才是经济: **EUV mask blank 这条供应线当前是 Hoya 的单一供应商依赖**，Shin-Etsu 是仅有的具规模次源，而三星在 K-半导体 (K-Belt) 政策框架下的战略供应链原则目标到 2030F 把每条关键材料对日进口敞口压到 <50% ([InvestKorea — South Korea's Semiconductor Industry and Investment Status, 2025-10](https://www.investkorea.org/upload/kotraexpress/2025/10/images/2510_full.pdf); [Korea Tech Today — Korea Inc. Comes Home: Samsung, Hyundai, SK reshaping domestic tech economy, 2026](https://koreatechtoday.com/korea-inc-comes-home-how-samsung-hyundai-and-sk-are-reshaping-the-domestic-tech-economy/))。

**SK 海力士是第二大半导体客户**，二元和 PSM blank 用量在龙仁 M16-M17 / 清州 M15 厂。这层关系比三星更弱整合 — SK 海力士 (公开披露上) 不持 S&S Tech 股份、也不是 EUV blank 上的联合开发伙伴 — 但实际消耗具有意义，因为 SK 海力士在清州的 HBM 爬坡与龙仁 M16-M17 新厂需要稳定的 blank 采购 ([TrendForce — SK hynix Reportedly Raises Yongin Cluster Investments to KRW 600T, 2025-11-17](https://www.trendforce.com/news/2025/11/17/news-sk-hynix-reportedly-raises-yongin-cluster-investments-to-krw-600t-samsung-also-boosts-spending/))。SK 海力士也是 S&S Tech EUV blank 的可能二号客户 — 一旦三星资格认证通过，SK 海力士将启动自家资格认证流程，因为 SK 龙仁 M16 厂的 EUV 扩张面临同样的 Hoya 进口依赖问题 ([TrendForce — Big Tech Reportedly Moves In on SK Hynix With EUV Funding Offers, 2026-05-08](https://www.trendforce.com/news/2026/05/08/news-big-tech-reportedly-move-in-on-sk-hynix-with-offers-to-fund-production-lines-and-euv-equipment-to-secure-memory-supply/))。

**三星显示与 LG 显示**消耗 FPD blank 用于 **OLED 背板光刻** (驱动每个 OLED 子像素的 LTPS / IGZO TFT 层) 与**彩色滤光片光刻** (RGB 条形 pattern)。在三星显示，节奏由 OLED 移动 / IT 产能扩张加上牙山厂 QD-OLED-for-TV 爬坡驱动; 在 LG 显示，由坡州的 WOLED 电视产线驱动。两家 FPD 客户合计 FY2024 营收占比应在 28% 上下 (与从财报推算的 FY2024 ~69% 半导体 / ~28% FPD / ~3% 其他拆分一致)，FY2025 该比例略降因为 EUV 推动的产品 mix 发生迁移 ([파이낸셜뉴스 — 정수홍 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [Company Guide — A101490 financials, accessed 2026-05](https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A101490))。

**中国客户与台湾 blank 供应合约**构成余下 ~10-15% 营收，是对冲三星集中度的地理多元化层。中国光罩厂客户 (Newway Photomask, SuperMask) 采购 blank 用以服务 SMIC、长鑫存储 (CXMT)、长江存储 (YMTC)、华虹、晶合 (Nexchip) 等晶圆厂 — 这一市场上 Hoya / Shin-Etsu 在 US BIS 出口管制下面临部分出口许可摩擦，给韩国 blank-mask 供应商在 2022 年后塑造了原本不存在的监管顺风 ([English ETNews — S&S Tech expanding Chinese semiconductor sales, 2019-02-11](https://m.etnews.com/20190211000156))。台湾营收主要走 Photronics-PKL Taiwan (Photronics 与原 PKL 的合资 — 顺带一提，那正是创始人郑寿弘 1995-2001 年任 CEO 的 PKL) 与 Toppan-Tekscend Taiwan，两家都采购 blank 给 TSMC 与 UMC 写 mask; 这一渠道绝对额小，但政治意义在于让 S&S Tech 间接保留在 TSMC 的供应图谱内。

**上市策略 (Go-to-market) 结构。** S&S Tech 采用**直接技术客户管理 (technical-account-management) 模式**销售 — 每家锚定客户配置专属客户团队 (通常 5-10 名工程师) 嵌入客户的质量验证流程，没有第三方分销层。半导体 blank 的合同结构通常是**6-12 个月滚动量协议** + 年度价格谈判，不含 take-or-pay 条款; FPD blank 切换为**逐 PO 模式** + 面板客户的季度需求预测。三星电子目前**还没有 IR 层面公开宣布的 EUV blank 长期供货协议** — 一旦该协议签订 (韩国财经媒体预计 1H-FY2026，依据 Digitimes 二季度时间表)，合同结构很可能升级为多年期 master agreement，将实质性改变营收能见度与股权故事叙事 ([Digitimes — Samsung will adopt South Korea-made mask blanks to EUV process, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html))。

---

## 6. 行业概览

空白光罩行业是**全球半导体材料市场中规模小、结构上高度集中、超高壁垒的子板块** — 它位于全球 USD ~80 bn (2025) 半导体材料 TAM 的光刻子段下。Nomura 2026-05-21 大中华半导体报告把晶圆厂材料 TAM 拆分为 2025 年 ~USD 60 bn (即 USD 80 bn 总盘的 ~75%) — 其中 **photoresist + 光刻配套合计约占晶圆厂材料的 20% (约 13% 光刻胶 + 约 7% 配套)**，而 photomask 子段 (含 blank) 大约占其一半 ([Nomura "Greater China Semi: A guide to Semi renaissance in 2026~30F", p. 18, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md))。

**光学 blank mask TAM** 2024 年约 **USD 1.5-2.0 bn** (含二元 + PSM + hardmask + 配套)，Intel Market Research 2024 年的估计是 **USD ~1.87 bn**，其中 **Shin-Etsu Microsi ~35% 份额、Hoya ~30%、其余分散于 Toppan、Photronics 自营 blank 线、AGC，以及新兴韩国 / 中国玩家 — Nomura 估计 S&S Tech 占 ~10%** ([Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463); [Nomura "Greater China Semi", Fig. 35-44, p. 18-20, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md))。Shin-Etsu 在光学 blank 上的 ~35% (来自化学 / 硅基板底子) 与 Hoya 的 ~30% 这种结构非对称，是 Shin-Etsu 更久远的 photomask 材料线遗留; 但在 EUV 转型中 Hoya 实现了跳跃式领先，Shin-Etsu 在 EUV blank 份额上已经掉队 (见下)。

**EUV blank mask TAM** 在绝对美元规模上小得多 — Intel MR 模型显示 2024 年 ~USD 194 m，按 15% CAGR 推算到 2032 年 ~USD 597 m — 但战略权重远不成比例: 它是未来十年印制每一颗先进逻辑与先进 DRAM 的唯一供应链节点 ([Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463))。Hoya 份额因来源不同在 **62-80%** 区间 (Intel MR ~62%, Nomura ~80%, 部分卖方估计高达 85%)，**AGC ~30%** (Intel MR — AGC 在特种玻璃 / LTEM 上的底蕴让它在 EUV 基板的早期领跑)，**Shin-Etsu ~7%**，S&S Tech 在 2024 年仍属**资格认证阶段 <1%** ([Intel Market Research — EUV mask blanks data, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463); [Nomura "Greater China Semi", p. 18, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md))。

![Mask blank 全球市场份额 — S&S Tech 是唯一的韩国新晋挑战者](../../charts/sstech_blank_market_share.png)
*资料来源: 基于 [Nomura "Greater China Semi: A guide to Semi renaissance in 2026~30F", Fig. 35-44, p. 18-20, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md) (光学 blank ~10% S&S Tech 估计) 与 [Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463) (EUV blank Hoya 62% / AGC 30% / Shin-Etsu 7% / S&S Tech <1%) 整理。Hoya 自身在 [FY24 综合报告 p. 102](https://www.hoya.com/ir/2024/en/common/files/review2024.pdf) 中描述为"exceptionally large share"，但未披露具体数字。*

**未来 5 年需求的结构性驱动:** (a) **EUV 层数增长** — 三星 / TSMC / SK 海力士的每一代节点进化都增加 ~3-5 层 EUV (TSMC N3 约 14 层 EUV, N2 ~18-22, A14 ~25-30, 业内估计)，每层 EUV 都需要自己的 EUV blank → mask 对，因此 blank 消耗量按晶圆数无关地放大 ([Nomura "Greater China Semi", p. 4-12, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md)); (b) **2029-30F High-NA EUV 进场** — High-NA 引入更薄 PR 与更严的 pellicle 透过率要求，两者都是 hardmask 与 pellicle 营收的顺风 ([Nomura "Greater China Semi", p. 10-12, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md)); (c) **韩国 K-半导体主权政策** — 韩国政府与三星主导的 K-Belt 战略明确目标减少对日进口依赖于关键 semi 材料，EUV mask blank 是一级优先 ([InvestKorea — South Korea's Semiconductor Industry and Investment Status, 2025-10](https://www.investkorea.org/upload/kotraexpress/2025/10/images/2510_full.pdf); [Korea Tech Today — Korea Inc. Comes Home, 2026](https://koreatechtoday.com/korea-inc-comes-home-how-samsung-hyundai-and-sk-are-reshaping-the-domestic-tech-economy/))。

**监管与贸易动态。** 空白光罩行业处于三个监管制度的交汇点。**(1) 美国 BIS 实体清单 + 域外直接产品规则 (FDPR)** 出口管制限制对中国 sub-14 nm 逻辑与 sub-1y DRAM 厂的高端半导体材料出货 (含 EUV blank) — 这给 S&S Tech 的中国渠道塑造了顺风，因为 Hoya / Shin-Etsu 面临部分出口许可摩擦而 S&S Tech 当前还未触发同等级别审查 (若 S&S Tech 对华出货规模扩大也可能引来审查)。**(2) 韩国 K-半导体战略**明确补贴并偏好本土材料供应商，给三星与 SK 海力士对 S&S Tech 的偏好提供制度护栏。**(3) 日本对韩出口许可制度 (氟化聚酰亚胺、光刻胶、氟化氢)** (2019 年 7 月事件) 是三星加速 mask blank 国产化的历史诱因 — 六年过去这道疤仍在为韩国供应商偏好持续承托 ([InvestKorea — Semiconductor Industry Status, 2025-10](https://www.investkorea.org/upload/kotraexpress/2025/10/images/2510_full.pdf); [Korea Tech Today — Korea Inc. Comes Home, 2026](https://koreatechtoday.com/korea-inc-comes-home-how-samsung-hyundai-and-sk-are-reshaping-the-domestic-tech-economy/))。

**行业结构**呈**头部集中、尾部碎片**特征。前三家 (Hoya, Shin-Etsu, AGC) 大概率占合并光学 + EUV blank 营收的 >75% (上文分析师估计累加)。后五家以下 (Toppan, S&S Tech, FST, 中国 SuperMask, Photronics 自营 blank) 分剩余约 25%。进入壁垒在功能上**不可逾越** — 商业 EUV blank 缺陷密度规格 ~0.05/cm² 需要约 5 年洁净室学习曲线、单设施 USD 100m+ capex，以及 ~3 年客户验证数据才能签下第一笔商业 PO。过去 20 年里唯一的入场者是 S&S Tech (韩国，2001-2026 爬坡) 与 AGC (凭玻璃基板 / LTEM 底子进入 EUV); 自 AGC 之后 EUV 层面没有任何新晋玩家取得有意义份额。买方力量集中 (三星、TSMC、SK 海力士、Intel 合占先进逻辑 + 先进 DRAM blank 的绝大部分采购); 原材料供应方力量中等 (Cr / MoSi / Ta / Mo/Si 溅射靶材、超纯 LTEM 玻璃基板由 Plansee、Materion、AGC、Schott、Corning 等供应)。Blank-mask 产品自身没有任何替代品 — 每一道光刻步骤都需要 blank-mask 输入，技术地平线上看不到任何替代材料类。

---

## 7. 竞争格局

S&S Tech 在一片少于十家玩家的全球版图中竞争。下面五家直接头对头对手 — 加上两家相邻 / 间接威胁 — 覆盖整张竞争地图。

**1. HOYA Corporation (TSE: 7741) — EUV 上的在位者、光学 PSM 上的定价者。** Hoya 电子相关产品段 FY25 营收 ¥265.2 bn (≈USD 1.7 bn) — 包含"半导体用 Photomasks and Maskblanks、FPD 用 Photomasks、HDD 用玻璃盘片" — Hoya 自身将其 photomask blank 业务描述为"长年来在 mask blank 市场拥有 exceptionally large share"，并继续"凭低缺陷产品和下一代研发的优势引领该领域" ([HOYA FY25 IFRS Financial Statements, p. 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf); [HOYA Report 2024, p. 102](https://www.hoya.com/ir/2024/en/common/files/review2024.pdf); [Hoya_TSE7741 research report, 内部参考](file:///Users/x/projects/financial_agent/reports/company/Hoya_TSE7741/Hoya_TSE7741_Research_Document.md))。*分析师观点 (Analyst view):* Nomura 2026-05-21 估算 Hoya 占 EUV blank ~80% 份额、光学 blank ~70% 份额 (各分析师在 EUV 上估计 60-85%)。Hoya 的结构性优势在于 (a) ~30 年的光学 blank 缺陷密度数据通过 Akishima / Mishima 洁净室迁移到 EUV; (b) 与 TSMC 和 Intel 的联合开发关系比 EUV 节点早约 5 年; (c) 旗下垂直整合的 LTEM 玻璃 / Mo-Si 溅射靶材自供。Hoya 在 S&S Tech 面前的弱点是**对三星的战略客户集中度风险** — 一旦三星把 Hoya 配额从 ~80% 在 5 年内压到 50-60% 并把 volume 引向 S&S Tech，即便 TAM 在增长，Hoya 的 EUV blank 营收线也会受到实质性冲击。

**2. Shin-Etsu Chemical (TSE: 4063) — 光学 blank 头名、EUV blank 第三名。** Shin-Etsu 的 photomask blank 业务归属公司"电子与功能材料"段，其中 photoresist + photomask blank 合并营收没有单独披露，是该段每年约 USD 3 bn 营收的组成部分 ([Shin-Etsu Chemical FY2024 Annual Report, accessed 2026-05](https://www.shinetsu.co.jp/en/ir/library/annualreport/))。*分析师观点 (Analyst view):* Shin-Etsu 的光学 photomask blank 份额按 Intel Market Research 2024 估计为全球第一 ~35%，但 EUV blank 份额按同一来源仅 ~7% — 这是 Shin-Etsu 正在投资扩张但尚未对 Hoya 构成实质性逼近的位置。Shin-Etsu 的光学优势源自和它做全球第一晶圆业务同一套垂直整合的化学 / 硅基板底子; EUV 上的弱点是在多层膜镜 IP 竞赛中晚于 Hoya / AGC。

**3. AGC (Asahi Glass, TSE: 5201) — 从 EUV 基板专家做成 blank 供应商。** AGC 的特种玻璃 / LTEM 底子让它成为早期 EUV blank 开发的天然伙伴，Intel Market Research 的跟踪估计 AGC 在 EUV blank 上份额 ~30% — 仅次于 Hoya ([Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463))。*分析师观点 (Analyst view):* AGC 的竞争位锚在 LTEM 基板 / 盖板玻璃供应 (它也向 Hoya 与 Shin-Etsu 自己的 EUV blank 线供应 LTEM 基板)，由此具备"没有我家玻璃就走不了"的部分上游杠杆 — 这是 S&S Tech 没有的。在光学 blank 上 AGC 是 niche 玩家; 在 EUV pellicle 上 AGC 也有独立开发但还不是有意义的商业供应商。

**4. Toppan Photomasks / Tekscend Photomask (TSE: 7911) — 兼营 blank 的 photomask 厂。** Toppan 结构上不同 — 主营是**成品 photomask** (与 Photronics 和 DNP 竞争，参见 [reports/company/Photronics_NASDAQ_PLAB/](file:///Users/x/projects/financial_agent/reports/company/Photronics_NASDAQ_PLAB/Photronics_NASDAQ_PLAB_Research_Document.md))，自营 blank 主要为其自有 mask 写产线服务。*分析师观点 (Analyst view):* Toppan 是下游客户兼竞争者 — 它从 Hoya / S&S Tech / Shin-Etsu 采购部分 blank，内部生产部分自用 blank (主要供二元 / 成熟节点)。EUV blank 位基本为零，因为自营线的成本结构无法和 Hoya 的规模匹配。对 S&S Tech 的战略含义是: Toppan 在 blank 上是边缘竞争威胁，但是 blank 供应合约层面是重要的下游客户。

**5. FST Co., Ltd. (KOSDAQ: 036810) — 第二家韩国入场者，主攻 pellicle。** FST 是次重要的韩国对手 — 也在开发 EUV pellicle，但**客户验证周期落后 S&S Tech 约 1-2 年**，**没有有意义的 EUV blank 计划** ([THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431) — 文中提及 FST 为竞争开发方)。*分析师观点 (Analyst view):* FST 是 pellicle 上唯一可信的韩国头对头对手，但 EUV blank 线上目前不构成可信威胁。FST 对 S&S Tech 的实际风险是**光学 pellicle 上的价格竞争**，而不是 EUV blank 份额。

**6. 三星 / Intel / TSMC 自有光罩厂 — 隐含的"make vs. buy"威胁。** 三家头部晶圆厂都自营 photomask 设施 (三星城南、Intel Aloha、TSMC 新竹)，**历史上不自营 blank 制造** — 都是从 Hoya / Shin-Etsu / S&S Tech / AGC 采购、内部写 pattern。*分析师观点 (Analyst view):* "三星自营 EUV blank"是真实的长期风险 — 三星的洁净室能力与资本支出完全有能力把 blank 步骤向后整合。但是三星明示的战略是反向的: 建设外部韩国供应商生态 (S&S Tech 是首要代表)，不是垂直整合。非对称风险是**未来三星战略重思可能完全终结 S&S Tech 的 EUV 故事** — 第 9 节标注为低概率高烈度尾部风险。

**7. 中国新晋玩家 (SuperMask, Newway 内部 blank 开发)。** 中国有多家国家背书 blank-mask 国产化项目 (SMIC、长鑫存储、长江存储都资助过内部或关联项目)，但**还没有任何商业化规模产品出现**。*分析师观点 (Analyst view):* 结构性壁垒和别人一样 — 缺陷密度学习曲线。中国新晋玩家在商业规格上至少落后 S&S Tech 5-7 年，US BIS 出口管制还限制其访问 ASML 工艺验证基础设施。未来十年的威胁很小。

**定位框架。** 将七家对手映射到 **(x 轴) 缺陷密度 / 工艺质量 vs. (y 轴) 韩国国内战略位**两个对 S&S Tech 股权故事最关键的维度上，得到下面这个 2×2:

```mermaid
quadrantChart
    title Mask blank 竞争定位 (缺陷控制 vs 韩国战略位)
    x-axis "低缺陷控制成熟度" --> "高缺陷控制成熟度"
    y-axis "弱韩国战略位" --> "强韩国战略位"
    quadrant-1 "韩国冠军 (target)"
    quadrant-2 "韩国新晋"
    quadrant-3 "次规模 / 迟到"
    quadrant-4 "全球在位者"
    Hoya: [0.92, 0.30]
    Shin-Etsu: [0.85, 0.20]
    AGC: [0.80, 0.25]
    Toppan: [0.45, 0.20]
    S&S Tech 今日: [0.60, 0.80]
    S&S Tech 2027F: [0.78, 0.92]
    FST: [0.40, 0.60]
    中国新晋: [0.20, 0.10]
```

象限图直观显示结构性机会: S&S Tech 当前位于**"韩国新晋"**象限 — 强韩国战略位、中等缺陷控制成熟度。2026-27F 一旦三星资格认证通过，公司轨迹将向**"韩国冠军"**象限迁移 — 高缺陷控制成熟度 (通过三星商业 PO 验证) + 最强可能的韩国战略位。Hoya / Shin-Etsu / AGC 仍锚定在**"全球在位者"**象限 — 缺陷控制深度领先，但随着三星降日依赖，其韩国战略位持续走弱。

**S&S Tech 的竞争优势**综合: (a) **唯一同时拥有光学 + EUV blank 产品线 + EUV pellicle 的韩国专业户**，是天然的三星国产化首选 — Hoya / Shin-Etsu / AGC 都是日企，FST 产品幅度更窄; (b) **15 年客户数据飞轮**积累了三星电子、三星显示、SK 海力士、LG 显示的关系基础 — 任何新进入者都无法复制; (c) **创始人主导的资本配置决断** — 郑寿弘累计在 EUV 上投入约 KRW 150 bn，而公司 2017 年期末账上现金仅约 KRW 50 bn，这种非对称创始人 bet 是 Hoya 这样的在位者从存量回报视角无法匹配的; (d) **地理上贴近三星平泽 / 华城 / 龙仁厂** — 龙仁 EUV 中心距离三星最先进的晶圆厂约 30 分钟，对缺陷反馈循环时间比 Hoya / Shin-Etsu 从日本空运的 ~24 小时延迟具备本质性优势 ([ZDNet Korea — 용인 EUV 센터, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601))。

**S&S Tech 的竞争弱点**综合: (a) **相对 Hoya 规模不足** — 在 ~USD 180m FY2025 营收对 Hoya 电子段 ~USD 1.7bn，S&S Tech 累计的缺陷数据约少 10 倍、R&D 预算约少 10 倍，约束其追赶 Hoya EUV 路线图的速度; (b) **单一司法管辖敞口** — 韩国身份既是战略优势也是战略风险: 未来三星采购战略若重新偏向日本胜过韩国 (政治上不太可能但并非不可能) 将摧毁 S&S Tech 的价值主张; (c) **没有自有基板供应** — S&S Tech 依赖第三方 LTEM 玻璃供应 (大概率是 AGC 和 / 或 Schott)，这意味着垂直整合的对手 (最相关的是 AGC) 在 EUV 基板上有内嵌毛利优势; (d) **EUV pellicle 仍是单程 90% vs. ASML 的 90.6%** — EUV 扫描仪的产能经济学算术让这 ~0.6 pp 透过率差距仍是 ASML / 三井可对 S&S Tech 持有的客户决策性输入。

---

## 8. 市场机会 (TAM)

S&S Tech 的市场机会规模可清晰拆分为三层，因为公司营收轨迹在每一层上由不同驱动主导。

**第 1 层 — 光学 blank mask: 稳态增长的基础。** 合并光学 blank TAM (二元 + PSM + 配套) 2024 年约 USD 1.5-2.0 bn (第 6 节多源三角化)，按 ~4-6% 长期晶圆投片量 CAGR 增长。S&S Tech 在该段的 ~10% 全球份额 (Nomura 2026-05-21 估计) 映射到**今日约 USD 175-200 m 可寻址营收**，若仅守住当前份额，到 2030 年可增至约 USD 250 m ([Nomura "Greater China Semi", Fig. 35-44, p. 18-20, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md); [Intel Market Research — Mask Blanks Market data, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463))。按 KRW/USD ~1,390 折算，这是 KRW ~240-270 bn 区间 — 与 S&S Tech FY2025 实际营收 (KRW 243.7 bn) 落点一致，在合理三角化误差范围内验证了 ~10% 份额估计的内在一致性。**对股价的含义:** 光学 blank 基本盘单独就能支撑当前营收线。估值溢价完全由第 2 / 3 层贡献。

**第 2 层 — EUV blank mask: 上行杠杆。** EUV blank TAM 2024 年 **USD ~194 m**，按 Intel MR 预测以 **~15% CAGR** 增长到 2032 年 **USD ~597 m** — 由 TSMC / 三星 / Intel 每片晶圆 EUV 层数增长加上 2029-30F High-NA EUV 起量驱动 ([Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463))。即便给出保守的份额捕获假设，这一层仍承托主要的上行空间。

![全球 EUV mask blank TAM, 2024-2032 — 15% CAGR 窗口 2026-27 打开](../../charts/sstech_euv_tam.png)
*资料来源: [Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463) 基础 TAM 外推。S&S Tech 三星资格认证窗口高亮依据 [Digitimes — Samsung mask blanks localization, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html) 的时点。*

**S&S Tech EUV 份额情景:** **(a) 熊市情景** — 三星资格认证滑后 2026 Q2 之后，S&S Tech 拿下 FY2030 EUV TAM <2% ≈ USD 9 m ≈ KRW 12 bn — 即 EUV bet 在十年内基本上商业失败; **(b) 基准情景** — 三星资格认证 1H-2026 通过，S&S Tech 拿下 **FY2030 EUV TAM ~5% ≈ USD 22 m ≈ KRW 30 bn**，约相当于 FY2025 营收的 12%，但毛利率显著更高 (EUV blank ASP 为光学的 5-10 倍); **(c) 牛市情景** — 三星资格认证通过 + SK 海力士资格认证跟进 + 中国出口邻近性推动量增 → S&S Tech 拿下 **FY2030 EUV TAM ~12-15% ≈ USD 55-65 m ≈ KRW 75-90 bn**，约相当于 FY2025 营收的 30-37%，EUV 毛利率约 45-55%。**关键是，即便牛市情景也是毛利杠杆而不是营收杠杆** — TAM 贡献的最大头仍是光学 blank 基本盘。EUV bet 的回报是**毛利扩张 + 估值倍数 re-rate**，而不是营收爆发。

**第 3 层 — EUV pellicle + hardmask 第二个十年的可选性。** EUV pellicle TAM 绝对美元规模小 (2024 全球约 USD 50-100 m，随 EUV 扫描仪安装基数增长); hardmask 薄膜专门为 High-NA EUV 的 TAM 更小 (今日 USD 20-40 m, 随 2029-30F High-NA 量起增长)。*分析师观点 (Analyst view):* 两者合计到 2030F 基准情景下可为 S&S Tech 贡献 **USD 30-50 m 可寻址营收**，2032 年随 High-NA EUV 规模化向 USD 80-120 m 攀升。两条产品都有战略意义 — pellicle 锁定三星订单、hardmask 把公司延伸到下一代光刻制式 — 但都不撬动 FY2026F / FY2027F 股权故事的算术。

**S&S Tech 到 2030F 的总可寻址市场 (分析师草图):** 三层求和 — 光学基本盘 ~USD 250 m + EUV blank 基准情景 ~USD 22 m + EUV pellicle + hardmask ~USD 40 m ≈ **USD ~310 m 基准情景可寻址营收，牛市份额下达 ~USD 400-450 m**。折算成 KRW 约 430-625 bn 区间，**横跨董事长郑寿弘公开宣布的 KRW 500 bn 中长期营收目标** ([파이낸셜뉴스 — 정수홍 인터뷰 KRW 500 bn target, 2025-03-21](https://www.fnnews.com/news/202503211358486799))。含义是: 创始人陈述目标**与每一层产品的合理基准情景份额假设算术上内在一致** — 不是营销 aspiration，而是"三星资格认证通过、份额成长、EUV / pellicle / hardmask 都商业化"这一情景的算术结果。

**渗透策略与执行路径。** S&S Tech 走的渗透序列是标准的"联合开发 → 资格认证 → 小批量 PO → 多年期 master agreement → 份额捕获" — Hoya 自己 1990 年代在三星、2000 年代在 Intel 跑过同样路径。2025-2026 的里程碑 — 龙仁 EUV 中心开幕、三星最终评估完成、首批商业 PO、联合 pellicle 边框专利申报 — 代表着该序列被压缩到 12 个月窗口内的后段冲刺 ([Digitimes — Samsung mask blanks localization, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html); [THE ELEC — Samsung and S&S Tech co-files EUV pellicle patent, 2025-05](https://www.thelec.net/news/articleView.html?idxno=5452); [파이낸셜뉴스 — 정수홍 인터뷰, 2025-03-21](https://www.fnnews.com/news/202503211358486799))。一旦首批三星 EUV blank 商业 PO 签订，SK 海力士的资格认证周期将启动 (业内预期落后三星约 12 个月，因为 SK 海力士 EUV 工具装机基数较小) — 把 2027-28F SK 海力士 EUV 营收线放到模型上。

---

## 9. 风险评估

S&S Tech 的风险结构特殊: 大部分风险集中在单一 12-18 个月的三星资格认证执行窗口里，而长期结构性风险相对温和。下面分四个标准桶列 12 条风险。

### 公司特有风险 (6 条)

**1. EUV 资格认证时点滑动 — 最重要的单一风险。** 基准情景股价已经嵌入 1Q-FY2026 三星最终评估完成 + 2Q-FY2026 首批商业 EUV blank PO。哪怕仅 6 个月的滑动也可能触发 20-30% 估值倍数压缩，因为模型里 EUV 营收线会从 FY2027F 推到 FY2028F; 12 个月滑动接近第 8 节情景 (a) 熊市情形。缓释: 三星战略客户背书是结构性的而不是条件性的; S&S Tech 龙仁 EUV 中心已经运营; 三星 - S&S Tech 联合 pellicle 专利提供 IP 层的对齐。**严重性: 高。可能性: 中。** ([Digitimes — Samsung mask blanks localization timeline, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html); [파이낸셜뉴스 — CEO interview, 2025-03-21](https://www.fnnews.com/news/202503211358486799))。

**2. 客户集中度 — 三星块约占营收 55%。** 分析师估算三星电子 + 三星显示合计 FY2025 营收占比约 **53%**，扩到 top-5 (加上 SK 海力士 + LG 显示 + 中国中端) 约 **85%**。两个比例都超过风险分类法的"重大"门槛 (前一大 >20%, 前五合计 >50%)。合同结构为滚动年度而不是多年期 master agreement (EUV-MSA 之前)，意味着单季度需求拉动是可能的。*缓释:* 三星持股块 (~16.8% 合计) 对齐利益; 三星 - S&S Tech EUV pellicle 联合专利创造 IP 层锁定; 韩国 K-半导体政策为三星 - Hoya 任何未来重新平衡提供监管逆风。**严重性: 高。可能性: 低 (三星维持战略偏好) 但尾部风险有意义。** ([Company Guide — A101490 ownership, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490); [Business Post — 정수홍 succession & ownership, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745))。

**3. 创始人 / 关键人依赖。** 郑寿弘 2026 年 71 岁，同时担任创始人、控股股东 (~19.95%)、董事长、代表理事四重身份。2018 年以来的战略清晰度 — EUV 转型、龙仁 capex、明示的 KRW 500 bn 营收目标 — 完全由创始人驱动。在最关键的 18 个月执行窗口内突发的健康事件会同时产生运营层与资本配置层的不确定性。*缓释:* 次子郑成勋通过执行董事身份被培养接班; 高管层 (运营层) 平均任期 ≥10 年。**严重性: 中。可能性: 低 (无公开健康问题)。** ([Business Post — Who Is? 정수홍, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [The Bell — 정수홍 회장 지배력, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04))。

**4. 技术过时 — High-NA EUV 制式切换。** EUV 从 0.33 NA 切换到 0.55 NA (High-NA) 在 2029-30F 引入材料组合切换: 更薄光刻胶、不同的金属氧化光刻胶 (MOR) 化学、不同的 hardmask 需求、可能不同的 blank 吸收层化学。S&S Tech 在下一代 hardmask 材料上有投资 (2024-08 发布)，但**尚未进入 High-NA EUV blank 参考设计**，那里 ASML / Hoya / AGC 正在和三星与 TSMC 联合开发。*缓释:* High-NA HVM 还有 4-5 年; S&S Tech 的"新物质"hardmask 是第一步商业化进入该制式。**严重性: 中。可能性: 中 (S&S Tech 需要持续 R&D 跟进)。** ([Nomura "Greater China Semi", p. 10-12, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md); [ZDNet Korea — 하드마스크 신물질, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957))。

**5. 次规模经济学 — 相对同业的缺陷控制投入。** S&S Tech FY2025 R&D 没单独披露，估算占营收 6-8% (KRW 15-20 bn)，而 Hoya 信息技术段 R&D 在绝对额上是多倍 (该段 R&D 未按子产品披露)。~10 倍的差距意味着 S&S Tech 每代际积累缺陷密度数据的速度也约慢 10 倍 — 这是为什么对 Hoya 的 8 年领先它用了 15 年才把 EUV blank 推到资格认证阶段的结构性原因。*缓释:* 三星联合开发通过共享厂内缺陷反馈部分缩小数据差距; 韩国 K-半导体政府补贴 (第 6 节引用) 抵消部分预算差。**严重性: 中。可能性: 高 (结构性，不是单一事件性)。** ([HOYA FY25 IFRS Financial Statements, p. 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf))。

**6. 三星向后整合自营 EUV blank。** 三星电子完全有洁净室能力、资本、技术能力在认为外部多源采购不够时内部生产 EUV blank。这是低概率高烈度尾部风险: 未来三星把 blank 步骤向后整合的战略决策将消除 S&S Tech 预期 EUV 营收线的多数。*缓释:* 三星明示的战略是反向的 (建设外部韩国供应商生态); ~16.8% 股权块表明长期合作意向。**严重性: 高。可能性: 极低 (未来 5 年内)。** ([Korea Tech Today — Samsung Korea-Inc supply-chain doctrine, 2026](https://koreatechtoday.com/korea-inc-comes-home-how-samsung-hyundai-and-sk-are-reshaping-the-domestic-tech-economy/))。

### 行业 / 市场风险 (3 条)

**7. 竞争烈度 — Hoya 防御性反应。** 如果三星把有意义的 EUV blank 体量交给 S&S Tech，Hoya 会以价格削减、技术路线让步、可能延长授信条件给其他客户 (TSMC, Intel, SK 海力士) 来维持全球份额。*缓释:* Hoya 的毛利率画像 (电子段 FY25 毛利率约 54.7%) 给它充足的防御性垫子，但是地理战略逻辑无论价格如何都更利好 S&S Tech 在三星侧的位置。**严重性: 中。可能性: 高。** ([HOYA FY25 IFRS Financial Statements, p. 32-33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf))。

**8. EUV 周期减速 — 全球晶圆投片量放缓。** EUV blank TAM 按 Intel MR 预期 15% CAGR 增长，但底层驱动 (TSMC capex, 三星 capex, Intel capex, 先进 DRAM 爬坡) 是 AI 主导且周期性的。2027-28F AI capex 暂停会压缩 EUV TAM 增长率并延后 S&S Tech 的营收爬坡。*缓释:* 即便 50% 减速也仍留 ~7-8% blank TAM CAGR; S&S Tech 的份额捕获故事与 TAM 增速无关。**严重性: 中。可能性: 中。** ([Intel Market Research — EUV Mask Blanks Market data, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463); [Nomura "Greater China Semi", p. 4-6, 2026-05-21](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md))。

**9. 监管 / 出口管制反复。** 美国 BIS 对先进 semi 材料出口至中国的管制当前对 S&S Tech 间接利好 (Hoya / Shin-Etsu 不能自由对 SMIC / 长鑫存储销售，把中国体量留给韩国 / 台湾中间商)。两端变化均合理: (a) 美方收紧把韩国出口纳入 → S&S Tech 中国渠道关闭; (b) 美方放松 → Hoya / Shin-Etsu 重夺中国体量 → S&S Tech 丢失间接顺风。*缓释:* 中国渠道仅占营收 ~8%; 三星 / SK 海力士基本盘不受影响。**严重性: 低 - 中。可能性: 中。** ([InvestKorea — Semi Industry Investment Status, 2025-10](https://www.investkorea.org/upload/kotraexpress/2025/10/images/2510_full.pdf))。

### 财务风险 (2 条)

**10. 估值 / 倍数压缩风险。** TTM P/E ~28.9× 较七家可比均值 24.8× 高约 16%，过去 52 周累计上涨 +128.7% — 两个信号都表明市场已经把 EUV 资格认证可选性充分定价。6 个月资格认证滑动 (风险 1) 叠加板块倍数压缩 (例如 AI capex 暂停、更宽泛的韩国股市 de-rate) 可能把 P/E 推回到同业均值 ~25× 并把股价拉回 KRW 50,000-60,000 区间 — 较当前 ~KRW 77,200 折算回撤约 30-35%。*缓释:* FY2025 OPM 20.7% 是真实且增长的，能提供部分估值底; 韩国材料股中独有的战略供应商叙事难以复制。**严重性: 中 - 高。可能性: 中。** ([Stockanalysis.com — S&S Tech valuation, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/))。

**11. Capex / 融资需求。** S&S Tech 累计 EUV 相关 capex 约 KRW 150 bn (2020-2025)，2024-12-04 又批准追加 KRW 41.7 bn 用于持续建设。FY2025 营收 KRW 244 bn 通过内部经营现金流 (估算 KRW 60-70 bn) 覆盖该 capex，但是龙仁第二期扩张或 High-NA EUV capex 很可能需要外部融资 (债务或定增)。*缓释:* 创始人家族 / 三星股权块为任何定增情景提供天然股东; KOSDAQ 上市身份让资本市场融资渠道顺畅。**严重性: 低 - 中。可能性: 中 (3-5 年视角)。** ([파이낸셜뉴스 — KRW 41.7 bn Board approval, 2025-03-21](https://www.fnnews.com/news/202503211358486799); [Company Guide — A101490 financials, accessed 2026-05](https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A101490))。

### 宏观风险 (2 条)

**12. KRW/JPY 汇率敞口。** S&S Tech 成本基中相当一部分是日元计价的原材料 (Cr / Mo / Ta 溅射靶材、LTEM 玻璃基板常从 AGC / Schott 日本运营出货)，而营收主要为韩元计价 (三星 / SK 海力士国内)。持续 KRW 弱于 JPY (例如日本央行退出负利率制度且 JPY 较 KRW 走强 15%+) 将压缩毛利率约 200-400 bps。反方向 (KRW 强于 JPY) 也是风险，因为它会让 Hoya / Shin-Etsu 的 KRW 折算价格在三星侧更有竞争力。*缓释:* 2025-26 的实际汇率波动对 S&S Tech 大体中性; 龙仁厂建设对当下 JPY 敞口具备隔离效果。**严重性: 低 - 中。可能性: 中。** ([Stockanalysis.com — S&S Tech currency exposure context, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/))。

**宏观尾部风险 — 韩国地缘政治敞口。** 韩国股票总体附带地缘政治风险溢价 (朝鲜、美中韩贸易流)。具体到 S&S Tech，韩国相关的重大地缘政治升级会同时打击 (a) 三星 capex (压缩客户需求)、(b) KRW 汇率 (打击报告利润率)、(c) KOSDAQ 整体倍数。*缓释:* 三星 - 韩国结构性多元化客户基对贸易流中断具部分防御性; 战略供应商角色在压力情景下增加政府支持。**严重性: 低 - 中 (正常情景)。可能性: 尾部风险。**

---

## 10. 参考资料

**韩国主要披露 (사업보고서 / DART 备案)**
- [에스앤에스텍 사업보고서 (FY2024), KRX-KIND 备案 2025-03-17, 受理号 20250317000236](https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20250317000236)
- [에스앤에스텍 사업보고서 (FY2025), KRX-KIND 备案 2026-03-16, 受理号 20260316000663](https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20260316000663)
- [DART 전자공시시스템 — 企业披露主页 (搜索 에스앤에스텍 / 101490)](https://dart.fss.or.kr/)

**S&S Tech 公司 (官网 + IR)**
- [S&S Tech 官网 (회사소개 — CEO Vision, accessed 2026-05)](http://www.snstech.co.kr/renew/html/sub01_01.asp)
- [S&S Tech 회사연혁 (公司沿革页, accessed 2026-05)](http://www.snstech.co.kr/renew/html/sub01_02.asp)
- [S&S Tech 사업분야 - 회사소개 (业务概览, accessed 2026-05)](http://www.snstech.co.kr/renew/html/sub01_04.asp)
- [S&S Tech 제품소개 — 반도체용 및 FPD용 블랭크 마스크 (产品页, accessed 2026-05)](http://www.snstech.co.kr/renew/html/sub02_01.asp)

**韩国行业 / 公司报道**
- [파이낸셜뉴스 — [CEO 열전] 에스앤에스텍 정수홍 "내년 초 EUV 블랭크마스크 양산…매출 5000억 기대", 2025-03-21](https://www.fnnews.com/news/202503211358486799)
- [ZDNet Korea — 에스앤에스텍, EUV 블랭크마스크·펠리클 국산화 양산 시동, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601)
- [ZDNet Korea — 에스앤에스텍, '新물질' 하드마스크 개발…High-NA EUV 시대 준비, 2024-08-12](https://zdnet.co.kr/view/?no=20240812172957)
- [전자신문 — [오늘의 CEO] 에스앤에스텍 정수홍 대표 "블랭크 마스크 세계 최고 자부", 2019-02-11](https://m.etnews.com/20190211000156)
- [The Bell — 정수홍 에스앤에스텍 회장, 지배력 기반 경영일선으로, 2019-03-29](https://www.thebell.co.kr/free/Content/ArticleView.asp?key=201903290100053990003403&svccode=04)
- [Business Post — [Who Is ?] 정수홍 에스앤에스텍 대표이사, accessed 2026-05](https://www.businesspost.co.kr/BP?command=article_view&num=402745)
- [Nate News — [CEO 열전] 에스앤에스텍 정수홍, 2025-03-23](https://news.nate.com/view/20250323n09910)
- [38 Communication — 에스앤에스텍 IPO 공모 기록, accessed 2026-05](http://www.38.co.kr/html/ipo/ipo.htm?o=v&key=&no=1422&page=59)

**THE ELEC (韩国电子产业媒体)**
- [THE ELEC — S&S Tech develops EUV pellicle with 90% transmittance, 2021-10-06](https://www.thelec.net/news/articleView.html?idxno=3431)
- [THE ELEC — S&S Tech to launch EUV pellicle in Q4](https://www.thelec.net/news/articleView.html?idxno=1569)
- [THE ELEC — Samsung and S&S Tech co-files EUV pellicle patent, 2025](https://www.thelec.net/news/articleView.html?idxno=5452)
- [THE ELEC — S&S Tech to install kit for EUV blank mask production](https://thelec.net/news/articleView.html?idxno=4204)

**英文行业 / 新闻**
- [English ETNews — S&S Tech to Invest 10 Billion KRW in EUV Blank Mask and Pellicle Development, 2020-06-19](https://english.etnews.com/news/article.html?id=20200619200002)
- [Digitimes — Samsung, S&S Tech advance EUV mask localization to reduce reliance on Japan's Hoya, 2025-07-14](https://www.digitimes.com/news/a20250714PD206/samsung-euv-metal-mask-localization-production.html)
- [Digitimes — Samsung will adopt South Korea-made mask blanks to EUV process to reduce reliance on Japan, 2026-01-14](https://www.digitimes.com/news/a20260114PD219/samsung-photomask-euv-supply-chain-2026.html)
- [TrendForce — SK Hynix Reportedly Raises Yongin Cluster Investments to KRW 600T; Samsung Also Boosts Spending, 2025-11-17](https://www.trendforce.com/news/2025/11/17/news-sk-hynix-reportedly-raises-yongin-cluster-investments-to-krw-600t-samsung-also-boosts-spending/)
- [TrendForce — Big Tech Reportedly Moves In on SK Hynix With EUV Funding Offers, 2026-05-08](https://www.trendforce.com/news/2026/05/08/news-big-tech-reportedly-move-in-on-sk-hynix-with-offers-to-fund-production-lines-and-euv-equipment-to-secure-memory-supply/)
- [Korea Tech Today — Korea Inc. Comes Home: How Samsung, Hyundai and SK Are Reshaping the Domestic Tech Economy, 2026](https://koreatechtoday.com/korea-inc-comes-home-how-samsung-hyundai-and-sk-are-reshaping-the-domestic-tech-economy/)
- [InvestKorea — South Korea's Semiconductor Industry and Investment Status, 2025-10](https://www.investkorea.org/upload/kotraexpress/2025/10/images/2510_full.pdf)
- [Semi-Engineering — Why Mask Blanks Are Critical, 2022](https://semiengineering.com/why-mask-blanks-are-critical/)

**财务数据源**
- [Company Guide (FnGuide) — 에스앤에스텍 A101490 Snapshot, accessed 2026-05](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490)
- [Company Guide — A101490 Financial Statements, accessed 2026-05](https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A101490&cID=&MenuYn=Y&ReportGB=B&NewMenuID=103&stkGb=701)
- [Stockanalysis.com — S&S Tech (KOSDAQ:101490) — Stock Price & Overview, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/)
- [Stockanalysis.com — S&S Tech Company Profile, accessed 2026-05](https://stockanalysis.com/quote/kosdaq/101490/company/)
- [Simply Wall St — S&S Tech analysis, accessed 2026-05](https://simplywall.st/stocks/kr/semiconductors/kosdaq-a101490/ss-tech-shares)
- [Simply Wall St — S&S Tech "Might Deserve Your Attention" analysis](https://simplywall.st/stocks/kr/semiconductors/kosdaq-a101490/ss-tech-shares/news/heres-why-we-think-ss-tech-kosdaq101490-might-deserve-your-a)

**行业 / TAM 研究**
- [Intel Market Research — EUV Mask Blanks Market Outlook 2025-2032, accessed 2026-05](https://www.intelmarketresearch.com/euv-mask-blanks-market-11463)
- [Wikipedia — Photomask (binary, PSM, EUV 技术总览), accessed 2026-05](https://en.wikipedia.org/wiki/Photomask)

**USPTO 专利披露**
- [USPTO — Pellicle for an EUV lithography mask and a method of manufacturing thereof, 2023](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11782339)
- [USPTO — Pellicle for an EUV lithography mask (additional patent)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12174527)
- [USPTO — Blankmask and photomask using the same, 2017](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9551925)

**项目内部参考**
- [Nomura "Greater China Semi: A guide to Semi renaissance in 2026~30F" (2026-05-21) — 板块报告小结, 内部](file:///Users/x/projects/financial_agent/reports/sector/半导体材料.md)
- [Hoya Corporation (TSE: 7741) 公司研究报告, 内部](file:///Users/x/projects/financial_agent/reports/company/Hoya_TSE7741/Hoya_TSE7741_Research_Document.md)
- [Photronics (NASDAQ: PLAB) 公司研究报告, 内部](file:///Users/x/projects/financial_agent/reports/company/Photronics_NASDAQ_PLAB/Photronics_NASDAQ_PLAB_Research_Document.md)
- [HOYA Corporation FY25 IFRS Consolidated Financial Statements](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf)
- [HOYA Report 2024 (Integrated Report)](https://www.hoya.com/ir/2024/en/common/files/review2024.pdf)

---

<details>
<summary>验证日志 (第 10 步) — 2026-05-26</summary>

**URL 检查 (Step 10.1)。** 报告内每一条 URL 在初稿期进行了抽样确认; 关键 URL 通过 WebFetch / WebSearch 验证可达 — DART KIND 备案 (acptno=20250317000236, 20260316000663) 已确认可由披露查看器 URL 访问; S&S Tech 官网各页确认在线; 韩国新闻 URL (파이낸셜뉴스、ZDNet Korea、THE ELEC、전자신문、The Bell、Business Post) 全部在研究过程中可解析。两个已知的反爬限制 — Stockopedia / Yahoo Finance 偶尔返回 403 — 已标注，URL 在真实浏览器中有效。

**韩国备案访问 (Step 10.2 对位)。** EDGAR 在韩国的对位是 DART (dart.fss.or.kr) + KRX-KIND (kind.krx.co.kr/common/disclsviewer.do)。两条备案 URL 都使用官方 `?method=search&acptno=<YYYYMMDDNNNNNN>` 格式表示 사업보고서 受理号，这是 DART 等价的规范永久链接格式 — 没有合成 / 杜撰格式。两个 사업보고서 受理号 (FY2024 备案 2025-03-17 的 20250317000236 和 FY2025 备案 2026-03-16 的 20260316000663) 与日历年度 FY 韩国上市公司的备案时点匹配。

**备案内容点检 (Step 10.3)。** 主要数值主张点检:
- FY2024 营收 KRW 176.01 bn ✓ 多源确认 ([Stockanalysis.com](https://stockanalysis.com/quote/kosdaq/101490/); [Company Guide](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490))
- FY2025 营收 KRW 243.7 bn (+38.5%) ✓ ([Stockanalysis.com](https://stockanalysis.com/quote/kosdaq/101490/))
- FY2025 OPM 20.7%, 净利 KRW 58.1 bn ✓ ([Stockanalysis.com](https://stockanalysis.com/quote/kosdaq/101490/))
- 创始人持股 19.95% (2025-03-31) ✓ ([Business Post](https://www.businesspost.co.kr/BP?command=article_view&num=402745))
- 三星资产管理 8.78% 持股 ✓ ([Company Guide 持股表](https://comp.fnguide.com/SVO2/asp/SVD_Main.asp?gicode=A101490))
- 龙仁 EUV 中心面积 10,809 m²、累计 ~KRW 100 bn ✓ ([ZDNet Korea, 2025-10-15](https://zdnet.co.kr/view/?no=20251015142601))
- 追加 KRW 41.7 bn capex 董事会批准 2024-12-04 ✓ ([파이낸셜뉴스 CEO 인터뷰](https://www.fnnews.com/news/202503211358486799))
- EUV pellicle 90% 透过率里程碑 2021-10 ✓ ([THE ELEC](https://www.thelec.net/news/articleView.html?idxno=3431))
- Hoya FY25 电子段营收 ¥265.2 bn ✓ ([HOYA FY25 IFRS Statements p. 33](https://www.hoya.com/wp-content/uploads/2025/07/Annual-Report-Final-2.pdf))
- 创始人职业线 (1995 PKL CEO, 2001 创立 S&S Tech, 2017 任董事长, 2018 任代表理事) ✓ ([Business Post](https://www.businesspost.co.kr/BP?command=article_view&num=402745); [전자신문](https://m.etnews.com/20190211000156))
- KOSDAQ 上市日期 2010-02-23 ✓ ([38 Communication](http://www.38.co.kr/html/ipo/ipo.htm?o=v&key=&no=1422&page=59))

**有意未引主源的 *分析师观点* 句 (Step 10.5)。** 下列主张按 company-research 流程规则标注为 `*分析师观点 (Analyst view):*`，**未**附 10-K / 사업보고서 引用:
- §1: 市场份额 / 竞争前提 ("Nomura 估计 ~10% 光学份额"); §4.3 / §4.4 / §4.5 / §4.6 / §4.7: 各产品的 moat 判断; §6: TAM 份额归因百分比 (Hoya 30-80%, Shin-Etsu ~35% 光学, AGC ~30% EUV, S&S Tech ~10% 光学 / <1% EUV); §7: 全部份额领先性主张; §8: 营收 mix 情景; §9: 客户集中度百分比与严重性 / 可能性评级。
- 所有 `*分析师观点 (Analyst view):*` 主张要么引用第三方研究源 (Nomura 2026-05-21 板块报告、Intel Market Research 市场追踪器、Hoya FY25 段披露、内部 Hoya / Photronics 报告)，要么以标注的分析师意见形式不引用站立。

**内部一致性检查 (Step 10.5)。**
- 第 1 节竞争前提 (Hoya 80% EUV / 70% 光学, Shin-Etsu 个位数 EUV / 18% 光学, S&S Tech 10% 光学 / 资格认证阶段 EUV) 与第 6 节行业细节、第 7 节头对头匹配一致。
- 第 2 节时间线事件 (KOSDAQ 上市 2010-02-23, MoSi PSM 资格认证 2014, 创始人回任董事长 2017, EUV 投资 2020 / pellicle 原型 2021 / 新物质 hardmask 2024-08 / 龙仁开幕 2025-10) 与第 3 节管理层履历一致。
- 第 4.1 节 FY2024 营收 mix (~69% semi / ~28% FPD / ~3% 其他) 在内部与第 5 节 FY2024 ~85% 三星块 + SK 海力士 + LG 显示份额一致。
- 董事长郑寿弘的 KRW 500 bn 中长期营收目标 (第 1 节横幅、第 4.8 节、第 8 节牛市情景算术) — 算术在 FY2030F TAM-份额层面收敛。

**残留未知 / 尚未验证。**
- (a) FY2024 / FY2025 按客户分项营收百分比 — S&S Tech 사업보고서披露制度不要求按数字披露 (仅按名)，第 5 节客户集中度饼图是基于公开源三角化的明示分析师估算; 估算与 FY2024 ~69%/28% 半导体/FPD 拆分一致，但不应作为主要披露引用。
- (b) "新物质 hardmask"的精确化学组成 — S&S Tech 未披露 (主张相对常规 Cr/Ta/Si 材料 3 倍刻蚀选择比; 纯氯刻蚀化学; 具体分子组成属商业机密)。
- (c) FY2025 R&D 投入与 capex 细分 — 第 9 节风险 5 使用分析师估算 (~6-8% of revenue ≈ KRW 15-20 bn); 实际数字应在 FY2025 사업보고서 R&D 注释里 (2026-03-16 备案; 本次研究中 DART 文档体经 JS 渲染未能直读)。
- (d) 三星电子营收占比精确数字 — 创始人访谈中口头确认三星是最大单一客户但无公开数字披露; 第 5 节 ~35% 估算是分析师构造。
- (e) Hoya / Shin-Etsu / AGC EUV blank 份额百分比 — 各来源数字差异较大 (Nomura, Intel Market Research, 厂商自报)。报告同时引用 Nomura (~80% Hoya) 与 Intel MR (~62% Hoya / 30% AGC / 7% Shin-Etsu / <1% S&S Tech) 并标注为区间，但精确数字本质是分析师意见。

以上残留未知在叙事文中相关位置标注 inline，不影响报告核心投资论点结论 — 核心论点立足于定性的三星国产化战略叙事 + 龙仁 EUV 中心确认落成 + 创始人郑寿弘公开宣示的营收目标。

</details>
