# IC 后段 (Back-End) 流程白话讲解 — Probing / Assembly / Test

> Source figure: **Nomura research — "Fig. 23: Integrated circuit packaging process and corresponding materials"**.
> 这篇是给非半导体行业的人看的科普,把图里的三个后段步骤 (Probing → Assembly → Test) 用最简单的话讲清楚,并标注每一步全球哪几家公司说了算。

---

## 0. 先搞清楚 "Back-End" 是什么 (大背景)

做一颗芯片大致分两段:

| 段 | 做什么 | 形容 |
|---|---|---|
| **Front-End (前段) / Fab / 晶圆制造** | 在一块圆形硅晶圆 (silicon wafer, 直径 200mm 或 300mm) 上,用光刻、刻蚀、薄膜沉积,刻出几百颗 / 几千颗芯片的电路 | "在硅片上盖楼" |
| **Back-End (后段) / OSAT / 封装测试** | 把晶圆上每一颗 "裸 die" 测试好坏 → 切下来 → 装进塑料/陶瓷外壳 → 再测一次 → 装盒发货 | "把楼搬出工地、装进集装箱、贴标签、出口" |

Nomura 这张图画的就是**整个 Back-End**,分成三个连续工序: **Probing → Assembly → Test**。下面逐个拆开讲。

---

## 1. Probing — Wafer Sort (晶圆测试 / 中测 / CP test)

### 一句话讲清楚
晶圆刚做完时,上面密密麻麻几百颗芯片有好有坏。**Probing 就是用一排比头发还细的金属探针 (probe needles / 探针),戳在每颗 die 的接触点上,通电跑一遍简化版的测试,把好的 die 和坏的 die 在地图上标出来。**

然后用一把超精密的钻石刀片 (或激光) 把整张晶圆**切成一颗颗独立的芯片**——这叫 **dicing (切割)**。切的时候喷的那种水叫 **dicing liquid (切割液)**,作用是降温、冲走硅屑、防止刀片粘屑。

### 为什么要做?
- 切完之后再发现一颗 die 是坏的,前面所有钱 (封装材料、人工) 都白花了。所以**先在晶圆上把坏 die 标记 + 剔除**,只把好的拿去做下一步,叫 **KGD (Known-Good Die, 已知好品)**。
- HBM 高带宽内存 (HBM) 这类要把 8~12 颗 die 叠起来的产品,只要其中一颗是坏的,整堆 HBM 就报废,所以 KGD 测试越来越关键。

### 这一步谁说了算? (设备 + 材料 + 服务)

**Wafer Prober (探针台 / 探测机)** — 把晶圆放上去、自动让探针逐颗 die 接触
- **东京精密 Tokyo Seimitsu / Accretech (日)** — 全球 #1,约 50% 份额
- **Tokyo Electron / TEL (日)** — #2
- **长川科技 Changchuan (中国 SZ:300604)** — 中国本土最强 prober,也是国产突围方向
- **精测电子、华峰测控** — 中国国产替代第二梯队

**Probe Card (探针卡)** — 真正接触晶圆的那一排针 (一张卡可能上万根针)
- **FormFactor (美 NASDAQ:FORM)** — 全球 #1
- **MJC (Micronics Japan) / Japan Electronic Materials (日)**
- **韩国 Korea Instruments / Microfriend (韩)**
- **强一半导体、和林微纳 (中国)** — 国产化主力

**Dicing 切割设备 (划片机)**
- **DISCO (日 TSE:6146)** — **全球绝对垄断,精密切割机~80% 份额**,几乎所有晶圆都靠它切。这是日本"隐形冠军"的典型例子
- **Tokyo Seimitsu (日)** — DISCO 的小弟
- **大族激光 Han's Laser (中国)** — 在激光切割路径有份额

**Dicing liquid (切割液 / 冷却液)**
- 一般是**去离子水 + 表面活性剂**,这块没什么超级垄断者,主要由 **Cabot Microelectronics (CMC Materials, 现属 Entegris)、JSR、Showa Denko、安集科技 (中国 SH:688019)** 这类湿电子化学品大厂供应

---

## 2. Assembly — Packaging and Assembly (封装 / 组装)

### 一句话讲清楚
切下来的裸 die 像一块玻璃片那么脆,而且接触点细到肉眼看不见,**根本没法直接焊到电路板上**。
**封装 = 给芯片"穿衣服 + 拉电线 + 装散热盖"**:
1. 把 die 粘到一片叫 **substrate (载板 / 基板)** 的小电路板上;
2. 用比头发还细的金线 / 铜线把 die 上的接触点和 substrate 上的脚连起来 (**wire bonding 引线键合**),或者直接把 die 翻过来用焊球贴上去 (**flip-chip 倒装**);
3. 灌入一团黑色塑料 (**epoxy molding compound, EMC, 环氧塑封料**) 把里面封死,变成你常见的那种黑色芯片;
4. 高端芯片再贴一片金属盖 (**heat spreader / IHS, 散热盖**) 帮它散热。

图里写的 "**surface chemicals, resin and foil (表面化学品、树脂、金属箔)**" 就是这一步用到的三大类耗材:
- **Resin (树脂)** = 环氧塑封料 EMC,把芯片密封起来;
- **Foil (金属箔)** = 铜箔/金线/铜线,做导电连线;
- **Surface chemicals** = 助焊剂 (flux)、底部填充胶 (underfill)、清洗液等。

### 高端封装的故事 (CoWoS / HBM / 2.5D / 3D)
**最近 3 年最火的封装词** = **CoWoS (Chip-on-Wafer-on-Substrate)**。NVIDIA 的 H100 / B200 之所以一卡难求,瓶颈不在台积电先进制程,而在 CoWoS 产能——因为每颗 GPU 都要把 GPU die + 8 颗 HBM 内存堆在一片硅 interposer (硅中介层) 上,再黏到 substrate 上。这是**先进封装 (Advanced Packaging)**,跟传统封装完全不是一个量级的复杂度。

### 这一步谁说了算?

**封装服务公司 (OSAT = Outsourced Semiconductor Assembly and Test, 外包封测)**
按全球营收排名:
1. **ASE Technology 日月光 (台 TWSE:3711 / NYSE:ASX)** — 全球 #1,~30% 份额
2. **Amkor (美 NASDAQ:AMKR)** — #2
3. **JCET 长电科技 (中 SH:600584)** — #3,**中国大陆 #1**,2015 年收购新加坡星科金朋
4. **Powertech Technology 力成 (台 TWSE:6239)** — #4,DRAM 封装强
5. **TFME 通富微电 (中 SZ:002156)** — AMD 的主要封装代工
6. **HuaTian 华天科技 (中 SZ:002185)** — 中国 OSAT 第三家
7. **SPIL 矽品 (台)** — 已被 ASE 合并

**Advanced packaging — CoWoS / SoIC 2.5D/3D 先进封装**
- **TSMC 台积电 (台 TWSE:2330 / NYSE:TSM)** — **绝对垄断 CoWoS,~ 90%+ 份额**,根本订不到产能
- **Samsung 三星 (韩)** — I-Cube,小份额
- **Intel (美)** — Foveros / EMIB,主要自用
- **ASE 日月光** — VIPack,刚起步

**Substrate (载板)** — 一片小型 PCB,把 die 连到主板
- **Unimicron 欣兴电子 (台 TWSE:3037)** — ABF 载板全球 #1
- **Nanya PCB 南亚电路 (台)、Kinsus 景硕 (台)** — 台湾三大
- **Ibiden (日 TSE:4062)、Shinko Electric (日)** — 日本系,Intel 主供
- **Samsung Electro-Mechanics (韩)、LG Innotek (韩)** — 韩系
- **深南电路 SCC 兴森科技 (中)** — 中国国产替代,主要做低端 / 国内手机芯片

**Bonding wire (键合丝)**
- **Heraeus 贺利氏 (德)** — 全球金线 / 铜线 #1
- **Tanaka 田中贵金属 (日)、Doublink (德)、Nippon Steel (日)** — 主要竞争者

**EMC 环氧塑封料**
- **Sumitomo Bakelite 住友电木 (日)** — 全球 #1,~ 30% 份额
- **Hitachi Chemical (日,现属 Resonac)、Showa Denko (日)、KCC (韩)** — 二三名
- **华海诚科、长电科技自供** — 中国国产替代

**Underfill / DAF (底部填充胶 / 芯片粘接膜)**
- **Henkel 汉高 (德)、Namics (日)、Hitachi Chemical (日)** — 海外
- **德邦科技 (中 SH:688035)** — 国产化龙头

---

## 3. Test — Testing and Retail Packaging (终测 / FT / Final Test)

### 一句话讲清楚
封装做完了,但还要再测一遍——因为前面切割、键合、塑封过程中,可能有些芯片被弄坏了。
**Final Test (终测) 就是把封好的成品芯片插进一台像吐司机大小的测试机 (handler) 里,自动一颗颗送进去,跑一套完整的电性测试 + 高低温测试**,把芯片按**速度等级 / 良率等级**分类 (**binning, 分箱**),比如 Intel CPU 同一片 wafer 出来的 die,跑得快的归到 i9,慢一点的降级为 i7 / i5——这叫 **speed binning**。

测试合格的芯片打上激光标记 (品牌、型号、批号),然后装进托盘 / Tray 或卷带 / Tape & Reel,最终装箱发到客户工厂或零售渠道——这就是图里写的 **Retail packaging (零售包装)**,比如你在京东买到的盒装 Intel CPU 就是这一步装的。

### 这一步谁说了算?

**ATE (Automated Test Equipment, 自动测试机 / 测试设备)** — 整个产业链里最贵的设备,一台动辄几百万美元
- **Advantest 爱德万 (日 TSE:6857)** — **全球 ~50% 份额**,SoC 测试 / AI 芯片测试绝对老大,NVIDIA H100/B200、Apple A 系列都靠它
- **Teradyne 泰瑞达 (美 NASDAQ:TER)** — #2,~ 35%,内存测试 + 通信芯片强
- **Cohu (美 NASDAQ:COHU)** — 模拟 / 功率半导体测试,handler 设备 #1
- **华峰测控 (中 SH:688200)** — **中国本土模拟测试机 #1**
- **长川科技 (中 SZ:300604)** — 数字 SoC 测试 + handler,A 股国产测试机龙头
- **精测电子 (中 SZ:300567)** — 显示 + 半导体测试

**Test Socket (测试座) + Handler (分选机) — ATE 的配件**
- **ISC International 韩 (韩 KOSDAQ:095340)、LEENO Industrial (韩)** — 测试座
- **Cohu (Delta Design 品牌, 美)、Advantest (子公司)、Yokowo (日)** — handler
- **华兴源创 (中 SH:688001)、长川科技** — 国产化主力

**测试服务 (OSAT 里的 T 部分)**
- **KYEC 京元电子 (台 TWSE:2449)** — **全球最大纯测试代工厂**,NVIDIA H100/B200 大部分终测在它家
- 其他大 OSAT (ASE、Amkor、JCET、TFME) 也都做测试,但 KYEC 是少有的"只做测试不做封装"的纯玩家

**激光打标 / 镭雕**
- **大族激光 Han's Laser (中 SZ:002008)、Rofin / Coherent (美)** — 激光设备

**零售包装 (Tray / Tape & Reel + 盒装)**
- 一般由芯片设计公司自己做最后一步盒装 (e.g. Intel 自己印盒子),或者交给小型 packaging house。这一步**不存在巨头**,价值量很低。

---

## 4. 速查表 — 三步走 + 龙头公司一览

| 工序 | 中文别名 | 干什么 | 最核心耗材 | 设备霸主 | 服务 / 代工霸主 |
|---|---|---|---|---|---|
| **Probing** (Wafer Sort) | 晶圆测试 / 中测 / 切割 | 测出好坏 die + 切成单颗 | Dicing liquid 切割液 | **DISCO (切割) / Tokyo Seimitsu (探针台) / FormFactor (探针卡)** | OSAT 都做 (ASE / JCET / Amkor) |
| **Assembly** (Packaging) | 封装 / 组装 | 给 die 穿外壳 + 拉线 + 散热 | EMC 树脂 / 金线 / Substrate 载板 | **TSMC (CoWoS 先进封装) / ASM Pacific (键合机)** | **ASE 日月光 #1 / Amkor #2 / JCET 长电 #3** |
| **Test** (Final Test) | 终测 / FT / 分箱 / 装盒 | 再测一遍 + 速度分级 + 装盒 | 测试 socket | **Advantest #1 / Teradyne #2** | **KYEC 京元电子 (纯测试)** + 各大 OSAT |

---

## 5. 投资视角 — 哪些公司值得追踪?

- **垄断型护城河 (低 risk, 高 ROE)**
  - **DISCO (日 6146)** — 全球切割机 ~80% 份额,几十年没人撼动
  - **Advantest (日 6857)** — AI 测试机绝对老大,NVIDIA H100/B200 强相关
  - **TSMC (台 2330)** — CoWoS 90%+ 份额,封装订单等于 AI 算力订单
  - **ASE Technology 日月光 (台 3711)** — OSAT 全球 #1,规模 + 客户网络护城河

- **AI 高弹性 (跟 NVIDIA / HBM 强相关)**
  - **KYEC 京元电子 (台 2449)** — NVIDIA 终测主力,B200 上量直接受益
  - **Unimicron 欣兴 (台 3037)** — ABF 载板紧缺
  - **Advantest** — 见上

- **国产替代 (中长期主线)**
  - **长电科技 JCET (SH 600584)、通富微电 TFME (SZ 002156)** — OSAT 国产化
  - **长川科技 (SZ 300604)、华峰测控 (SH 688200)** — 测试机国产化
  - **深南电路 (SZ 002916)、兴森科技 (SZ 002436)** — 载板国产化

---

## 6. 常见疑问 (FAQ)

**Q: 那 die / chip / IC / 芯片到底有什么区别?**
A: 三个词在中文里都翻译成"芯片",但严格讲:
- **Die (裸 die / 晶粒)** = 还没封装的、刚从晶圆上切下来的小硅片
- **Chip / IC** = 已经封装好、有引脚 (lead) 或焊球 (BGA ball) 的成品
- 中文一般都叫"芯片",有歧义时说"裸 die / 封装后芯片"区分

**Q: 为什么 NVIDIA 不能自己做封装,要靠 TSMC?**
A: NVIDIA 是 **fabless (无晶圆厂)** 公司,只做芯片设计;晶圆代工 + 先进封装都外包。CoWoS 这种 2.5D 封装技术几乎全在 TSMC 手里,因为它需要把 HBM + GPU die 精度对到微米级,只有掌握前段制程的 TSMC 才能在自己的 fab 里同时做晶圆 + 中介层 + 封装。

**Q: HBM 跟封装的关系?**
A: HBM (High Bandwidth Memory, 高带宽内存) 本身是用 **TSV (硅穿孔)** 把 8~12 颗 DRAM die 堆叠起来,这是封装技术。HBM die 由 **SK Hynix / Samsung / Micron** 三家做,堆叠由它们自己完成,然后整颗 HBM 再被送到 TSMC 的 CoWoS 产线,跟 NVIDIA GPU die 一起封到 substrate 上。所以**做一颗 H100 涉及到至少 3 家封测产能** (SK Hynix HBM 堆叠 + TSMC CoWoS + 终测可能在 KYEC)。

**Q: 为什么 DISCO 这种"切割刀片"公司能赚那么多?**
A: 切割看起来简单,但要求晶圆每颗 die 之间切割缝 (scribe lane) 只有几十微米,刀片磨损度、振动、冷却液流量任何一点偏差都会让良率掉一截。DISCO 几十年积累的工艺 know-how + 客户 qualified 周期长,新厂商即使造得出刀片也卖不进去——典型的"工程师文化型"日本隐形冠军。

---

*本文为科普向解释稿,数据点 (份额、排名) 为产业普遍口径,实际投资分析请以最新财报 / 公司公告为准。*
