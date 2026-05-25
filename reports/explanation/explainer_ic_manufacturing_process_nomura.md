# How a Chip Is Actually Made — A Plain-English Walkthrough

*Based on Nomura's "Integrated circuit manufacturing process and corresponding materials" diagram (Fig. 22).*

A modern chip starts life as ordinary beach sand and ends as a fingernail-sized square holding billions of microscopic switches. The journey takes roughly 12 weeks, 500–1,500 process steps, and one of the most expensive factories humans have ever built. The Nomura diagram compresses that journey into four big stages. Here is what is actually happening at each one, in language a non-engineer can follow.

The whole thing is called **"front-end" wafer fabrication** — "front-end" because we are still building the chip itself; the "back-end" (cutting it up, sticking it in a plastic package, soldering it to a circuit board) happens later in different factories.

---

## Stage 1 — Material Fab: Turning Sand into a Mirror-Flat Silicon Disc

Goal: produce a perfectly pure, perfectly flat silicon **wafer** — the canvas everything else gets painted on. Picture a CD-sized disc of polished metal.

### Step 1 — Polycrystalline silicon 多晶硅 (raw material: sand 硅砂)
Sand is mostly silicon dioxide (SiO₂). Chemists strip the oxygen off and refine the silicon until it is **99.9999999%** pure (nine nines — "9N"). At this point it looks like grey gravel made of many tiny crystals stuck together. That is "polycrystalline" or "polysilicon" (多晶硅).

> *Everyday analogy:* think of it as turning beach sand into a lump of pure rock candy, except instead of sugar it's silicon and instead of "sweet" the goal is "absurdly pure."

**Who dominates (semi-grade polysilicon 电子级多晶硅):** Wacker 瓦克化学 (Germany) is the global #1, with Hemlock Semiconductor (US, JV of Corning & Shin-Etsu) and Tokuyama 德山 (Japan) the other two big players. China's GCL 协鑫 and Tongwei 通威 dominate solar-grade polysilicon but are still climbing the purity curve to break into semi-grade. The top three Western/Japanese players hold ~70%+ of electronic-grade supply.

### Step 2 — Silicon melted 硅熔融 (uses: special gas 特种气体)
The polysilicon chunks are loaded into a quartz crucible and melted at ~1,420 °C. The "special gas" is an inert gas like argon, pumped into the chamber to keep oxygen out — any oxygen that sneaks in would contaminate the silicon.

**Who dominates (electronic specialty gases 电子特气):** Four Western/Japanese majors — Air Liquide 液化空气 (France), Linde 林德 (UK/Germany), Air Products 空气化工产品 (US), Taiyo Nippon Sanso 大阳日酸 (Japan) — collectively hold ~60–70% of the global electronic-gas market. Inside China, 华特气体 (Huate Gas), 金宏气体 (Jinhong Gas), 中船特气 (CSSC Specialty Gases) and 凯美特 (Kemet) are the rising local champions, supplying SMIC, Hua Hong and YMTC.

### Step 3 — Single-crystalline silicon ingot 单晶硅锭 (uses: seed crystal doping 籽晶掺杂)
A tiny "seed" of perfect silicon crystal is dipped into the molten silicon and **slowly pulled upward while rotating**. The atoms below line up with the seed's crystal structure as they solidify, growing one giant single crystal — a sausage-shaped **ingot** ~30 cm wide and 1–2 m long. This is the **Czochralski process 直拉法** ("Cz pull").

"Doping 掺杂" means tiny amounts of boron or phosphorus are added to the melt to give the silicon the basic electrical character a chip needs.

> *Everyday analogy:* like pulling a rock-candy stick out of sugar syrup so the sugar crystals grow in one neat direction instead of in random clumps.

### Step 4 — Slicing 切片 (uses: slicing liquid 切割液)
The ingot is sawn into thin, round wafers — typically **0.775 mm thick, 300 mm across** — using a wire saw flooded with "slicing liquid" (an abrasive slurry that does the actual cutting; the wire itself is just a guide).

### Step 5 — Grinding and polishing 研磨抛光 (uses: grinding & polishing slurry 研磨/抛光液)
The freshly cut wafer is rough, like sandpaper. It is ground flat, then polished with progressively finer slurries (basically a milkshake of nano-sized abrasive particles in a chemical bath) until the surface is **flatter than a billiard table scaled up to the size of Texas** — variations of just a few nanometres across 300 mm.

### Step 6 — Cleaning 清洗 (uses: deionized water 去离子水)
Every speck of dust, every metal ion, every fingerprint molecule is washed off using **ultra-pure deionized (DI) water** plus chemicals. A modern fab uses millions of litres of DI water per day, and the water is purer than anything you can buy as "distilled" at a pharmacy.

**Who dominates (Steps 3–6, 300 mm silicon wafer 12寸硅片):** Just **five companies make ~95% of the world's leading-edge 300 mm wafers** — Shin-Etsu 信越化学 (Japan, ~28%), SUMCO 胜高 (Japan, ~22%), GlobalWafers 环球晶圆 (Taiwan, ~15%), Siltronic 世创 (Germany, ~12%), SK Siltron 鲜京矽特隆 (Korea, ~12%). It is one of the most concentrated supply chains in semiconductors — even more so than lithography. China's 沪硅产业 (NSIG / National Silicon Industry Group) and 立昂微 (Lion) are the leading domestic challengers but still well below 5% global share at leading nodes.

The output of Stage 1: a mirror-shiny, perfectly flat silicon wafer. Now we can start building circuits on it.

---

## Stage 2 — Wafer Fab Part A: Photolithography & Etching (the "Printing" Stage)

This stage **repeats 50–100 times** during the construction of a single chip. Each pass lays down one layer of the chip's pattern, the way a printer makes a colour image one ink layer at a time.

### Step 7 — Applying photoresist 涂胶 (uses: photoresist 光刻胶)
The wafer is spun like a record while a syrup-like, light-sensitive chemical called **photoresist 光刻胶** is dripped onto it. The spinning flings the photoresist out into a film just a few hundred nanometres thick — about 1/500th the thickness of a human hair.

> *Everyday analogy:* a glaze on a doughnut, but the glaze reacts to light.

**Who dominates (photoresist 光刻胶):** Japan basically owns this market — **JSR 捷时雅 (~25%), Tokyo Ohka Kogyo / TOK 东京应化 (~25%), Shin-Etsu 信越化学 (~17%), Sumitomo Chemical 住友化学, Fujifilm 富士胶片** together hold ~80%+ of all semiconductor photoresist, and ~100% of the EUV photoresist market. DuPont 杜邦 (US) covers some KrF/ArF segments. China is far behind — 南大光电 (Nata Opto-electronic), 彤程新材 (Red Avenue) and 晶瑞电材 (Crystal Clear) are domesticating KrF / i-line resists, but EUV remains out of reach. **Coater/developer equipment**: Tokyo Electron / TEL 东京电子 controls **~90%+** of the global coater/track market — essentially a monopoly.

### Step 8 — Exposing photoresist 曝光 (uses: lithography machine 光刻机, e.g. ASML's EUV)
A **photomask 光罩** (think: a stencil holding the pattern of one layer of the chip) is placed between a light source and the wafer. Light shines through the mask, projecting the pattern onto the photoresist. Wherever the light hits, the photoresist's chemistry flips.

The cutting-edge tool here is an **EUV (extreme ultraviolet 极紫外) lithography machine** from ASML — a machine the size of a bus that costs **$200–400 million each** and uses light with a wavelength of 13.5 nm, generated by zapping droplets of molten tin with a laser 50,000 times per second.

**Who dominates (lithography 光刻):** **ASML 阿斯麦 (Netherlands) — 100% monopoly on EUV** and ~90% of advanced DUV (immersion ArFi). It is the single most concentrated link in the entire chip supply chain. Nikon 尼康 (Japan) and Canon 佳能 (Japan) still sell to older nodes (i-line, KrF) and Canon is pushing nano-imprint lithography (NIL) as an EUV alternative for memory. China's 上海微电子 / SMEE has shipped 90 nm DUV tools and is reportedly developing 28 nm — still 2–3 generations behind ASML. **Photomask 光罩:** Toppan (Japan), DNP (Japan), Photronics (US) lead the merchant market; TSMC, Intel, Samsung make their own at leading nodes.

### Step 9 — Developing resist 显影 (uses: developing solution 显影液)
A liquid "developer" washes away one type of photoresist (the exposed parts for "positive" resist, the unexposed parts for "negative" resist). What is left behind on the wafer is a **physical 3-D copy of the mask's pattern**, made of photoresist, sitting on top of whatever material is below it.

> *Everyday analogy:* like darkroom photo developing — the latent image becomes visible.

**Who dominates (developer 显影液 — TMAH):** Tokyo Ohka 东京应化, JSR 捷时雅, Mitsubishi Chemical 三菱化学 (all Japan) supply most of the world's TMAH developer. Equipment is the same Tokyo Electron 东京电子 coater/track that handled Step 7.

### Step 10 — Implanting ions 离子注入 and removing photoresist 去胶 (uses: ion implanter 离子注入机, photoresist solvent 剥离液)
Now the photoresist works as a **shield**. Wherever it covers the silicon, the silicon is protected; wherever the developer washed it away, the silicon is exposed.

**Ion implantation 离子注入:** the wafer is bombarded with charged atoms (boron, phosphorus, arsenic) accelerated by an electric field. The ions slam into the exposed silicon and embed themselves a few hundred atoms deep, changing the silicon's electrical properties locally. This is how the "source 源极" and "drain 漏极" regions of a transistor — the parts that actually carry current — get their personality.

Afterwards, a **photoresist solvent** ("stripper 剥离液") chemically dissolves the remaining photoresist mask, leaving only the modified silicon.

**Who dominates (ion implantation 离子注入):** Applied Materials 应用材料 (US, via its 1997 acquisition of Varian) holds **~70–75%** of the global ion implanter market; Axcelis Technologies 安舍利斯 (US) is the strong #2 with ~20%, especially in high-energy and silicon-carbide implant. China's 中科信 (CETC) and 万业企业 (Wanye / Kingstone) are building local alternatives. **Strippers 剥离液**: Entegris 恩特格里斯 (US), BASF 巴斯夫 (Germany), Kanto Chemical 关东化学 (Japan).

### Step 11 — Etching 蚀刻/刻蚀 (uses: hard mask 硬掩膜, etching gas 蚀刻气体, mask removal chemical 去胶剂)
On the next pass, instead of implanting ions, we **carve away material**. A hard mask (usually silicon nitride 氮化硅 or silicon oxide 二氧化硅) and another photoresist layer protect the parts we want to keep. Then either:

- **Wet etching 湿法蚀刻** — corrosive liquid (e.g. hydrofluoric acid 氢氟酸) eats the exposed material; or
- **Dry / plasma etching 干法/等离子蚀刻** — a fluorine- or chlorine-containing gas is ionised into a plasma, and the energised ions blast away material atom-by-atom with extraordinary precision.

Plasma etching is what lets us cut features just a few atoms wide.

After etching, the mask is dissolved off with another stripper chemical.

> *Everyday analogy:* steps 7–11 are like silk-screen printing T-shirts, except the "ink" is sometimes a beam of atoms and sometimes a corrosive gas, and the "design" is repeated 50+ times in slightly different forms to build a 3-D structure on the wafer.

**Who dominates (etch equipment 蚀刻设备):** Three names split nearly the whole market — **Lam Research 泛林集团 (US, ~50%), Tokyo Electron 东京电子 (~25%), Applied Materials 应用材料 (~20%)**. Lam is especially dominant in conductor etch and the high-aspect-ratio channel-hole etching that 3D NAND depends on. China's **中微公司 / AMEC (Advanced Micro-Fabrication Equipment)** is the breakout local champion — its dielectric etchers are qualified at TSMC's 5 nm node and it now competes head-to-head with TEL/Lam in select etch steps; 北方华创 / Naura is the broader local platform. **Etching gas 蚀刻气体**: Showa Denko 昭和电工 / Resonac (NF₃, the big one), Air Liquide, Linde, Kanto Denka, 中船特气 (CSSC) for NF₃ in China.

---

## Stage 3 — Wafer Fab Part B: Building the Transistor Itself

The transistor is the basic switch of a chip — billions of them, each ~5 nm long, form the logic that runs your phone. To build one, three sub-layers have to be assembled on top of the doped silicon from Stage 2.

### Step 12 — Creating a gate dielectric 栅介质 and electrode 栅电极 (uses: polycrystalline silicon 多晶硅)
A transistor has a "gate 栅极" that turns the switch on or off. The gate sits on top of an extremely thin insulating layer (the **gate dielectric** — historically silicon dioxide, just a few atoms thick). On top of that goes the **gate electrode** itself.

In older chips, the gate electrode was made of polycrystalline silicon (polysilicon) — the same stuff from Step 1 but deposited as a thin film.

> *Everyday analogy:* the gate dielectric is like a non-stick coating on a frying pan, and the gate electrode is the lid you put on top to control what happens underneath.

**Who dominates (CVD thin-film deposition 化学气相沉积):** **Applied Materials 应用材料 (~40%)** is the broad leader across CVD/PVD, with **Lam Research 泛林 (~20%)** and **Tokyo Electron 东京电子 (~20%)** sharing the rest of the chemical-deposition market. **ASM International 先晶半导体 (Netherlands, distinct from ASML)** dominates the more specialised epitaxy and ALD niches. In China, **北方华创 / Naura** is the leading local CVD/PVD player; **拓荆科技 / Piotech** is the focused ALD/CVD pure-play.

### Step 13 — Insulating the transistor 隔离
Each transistor has to be electrically isolated from its neighbours, otherwise current would leak sideways across the chip. Trenches are etched between transistors and filled with insulating oxide — a process called **STI (shallow trench isolation 浅沟槽隔离)**.

**Who dominates (STI fill 沟槽填充):** The same trio — Applied Materials, Lam, TEL — sell the HDP-CVD / HARP / FCVD tools that fill the trenches. The fill materials (TEOS, ozone, silane) come from gas majors Air Liquide / Linde / Air Products / 雅克科技 (Yoke).

### Step 14 — HIGH-K / Metal gate formation 高K金属栅 (uses: High-K dielectric 高K介质 and high-purity gas 高纯前驱体)
At sub-45 nm nodes, the old silicon-dioxide / polysilicon gate stack started leaking current like a colander. The industry switched to:

- **High-K dielectric 高K介质** — a material like **hafnium oxide HfO₂ 氧化铪** that blocks leakage much better than SiO₂. "High-K" just means "high dielectric constant 高介电常数" — it stores more electric field per unit thickness.
- **Metal gate 金属栅极** — replaces the polysilicon gate with metals like titanium nitride 氮化钛 or tungsten 钨, which work better with the high-K layer.

These layers are deposited using **ALD (atomic layer deposition 原子层沉积)** — a method that lays down films **one atomic layer at a time** by alternately pulsing two gases into the chamber. The "high-purity gas" callout in the diagram refers to the precursor gases (前驱体) that supply those atoms (think hafnium tetrachloride HfCl₄ for hafnium oxide).

> *Everyday analogy:* upgrading from a thin paper coffee filter to a high-tech ceramic one — same job, but it stops leaks that the cheaper version couldn't.

**Who dominates (ALD equipment 原子层沉积设备):** **ASM International 先晶半导体 (Netherlands)** is the **clear #1 in ALD** (~50%+ share at leading edge), with Tokyo Electron 东京电子, Lam Research 泛林, and Applied Materials 应用材料 sharing the rest. Korea's Wonik IPS and China's **拓荆科技 / Piotech** and **微导纳米 / Leadmicro** are the rising local challengers. **High-K precursors 高K前驱体 (HfCl₄, TEMAH, TDMAH)**: Air Liquide 液化空气, Versum / Merck 默克, Tanaka Chemical 田中化学 (Japan), 雅克科技 / Yoke (China — via its Korean subsidiary UP Chemical).

---

## Stage 4 — Wafer Fab Part C: Metallisation (Wiring the Chip Together)

Billions of transistors are useless unless you can wire them to each other. Modern chips have **10–20 layers** of metal wiring stacked vertically, like the road network of a city laid on top of itself ten times.

### Step 15 — Metal deposition 金属沉积 (uses: copper 铜 and other metals, copper electroplating solution 电镀液)
Channels are etched into an insulating layer (called the "inter-layer dielectric 层间介质"). Then **copper 铜** is deposited into those channels.

The deposition uses **electroplating 电镀**: the wafer is dipped into a copper-sulfate solution and an electric current pulls copper ions out of the solution onto the wafer surface, where they pile up and fill the trenches. Other metals — barrier layers of tantalum (Ta) and tantalum nitride (TaN) that stop copper from contaminating the silicon — are deposited too, using a method called **PVD (physical vapour deposition 物理气相沉积)** or sputtering 溅射.

Copper replaced aluminium around 1998 because it conducts electricity ~40% better, which lets the chip run faster.

> *Everyday analogy:* like rivers of liquid metal being poured into a tiny etched roadmap, then frozen in place. Repeat 10–20 times, each layer above slightly different from the one below, with vertical tunnels ("vias 通孔") connecting them.

**Who dominates (PVD sputter 物理气相沉积):** **Applied Materials 应用材料 dominates PVD with ~70–85% share** via its Endura platform — one of the most monopoly-like positions in fab equipment. **Electroplating 电镀 (ECD)**: Lam Research 泛林 (Sabre tool, ~60%) and Applied Materials share the equipment market; **Atotech 安美特 (now part of MKS Instruments 万机仪器, US)** and DuPont / Dow lead the copper-plating chemistry; in China, **安集科技 / Anji Microelectronics** also supplies plating additives. **Tungsten 钨 deposition** for contacts/vias: dominated by Lam Research's WCVD tools.

### Step 16 — Polishing 抛光 and connecting with metal layers (uses: CMP slurry 抛光液 and pad 抛光垫)
After electroplating, the wafer surface looks like a lumpy hill — too much copper sits above the trenches. **CMP — Chemical Mechanical Polishing 化学机械抛光** — combines an abrasive slurry with a chemical solvent on a rotating pad to flatten the wafer back to mirror-smoothness. The copper now sits flush with the surrounding insulator, ready for the next layer of metal to be built on top.

> *Everyday analogy:* CMP is like sanding down a wood inlay until the inlay and the surrounding wood are perfectly level — except at nanometre precision and with chemicals that selectively soften copper or oxide.

**Who dominates (CMP equipment 抛光设备):** A near-duopoly — **Applied Materials 应用材料 (~65%) and Ebara 荏原 (Japan, ~30%)**. China's **华海清科 / Hwatsing** is the breakout local CMP-tool player and has shipped to SMIC and YMTC. **CMP slurry 抛光液**: **CMC Materials (Cabot Microelectronics, acquired by Entegris 恩特格里斯 in 2022)** is the #1 globally, with **Versum / Merck 默克 (Germany)**, **Fujimi 富士美 (Japan)**, **Hitachi Chemical / Resonac 力森诺科 (Japan)** the other majors. In China, **安集科技 / Anji Microelectronics** is the clear domestic leader in copper-CMP slurry — qualified at SMIC and Hua Hong. **CMP pad 抛光垫**: **Dow / DuPont 陶氏 (US) holds ~80%+ of the global pad market** (the IC1000 family is the industry standard); China's **鼎龙股份 / Dinglong** is the leading domestic pad supplier.

Repeat the entire deposit-pattern-etch-deposit-polish cycle ten-plus times to stack all the wiring layers. Then the wafer is finally done.

---

## A Cross-Cutting Tool That Watches Everything: Process Control 量测/检测

The Nomura diagram doesn't show it, but **every few steps the wafer is inspected** — measured for film thickness, defects, overlay error, critical-dimension uniformity. Without this, fabs would be running blind.

**Who dominates (metrology & inspection 量测与检测):** **KLA 科磊 (US) — ~55% global share**, especially in optical defect inspection where it is essentially a monopoly. Applied Materials 应用材料 and Hitachi High-Tech 日立高新 split most of the rest (Hitachi leads e-beam metrology, ASML's HMI subsidiary leads e-beam inspection). China's **中科飞测 / Skyverse** and **上海精测 / Jingce** are building local alternatives but remain niche.

---

## What Happens After (Not in This Diagram)

The Nomura figure stops at the end of "front-end 前道." What comes next:

- **Wafer test 晶圆测试** — every chip on the wafer is electrically probed; defective ones are marked.
- **Dicing 划片** — the wafer is sawn into individual rectangular "die 裸片" (the actual chips).
- **Packaging 封装** — each die is wire-bonded or bumped to a substrate, encapsulated in plastic or ceramic — this is the black square you see on a circuit board.
- **Final test 终测** — packaged chips are tested again before shipping.

That whole stage is called **OSAT — outsourced semiconductor assembly and test 委外封装测试**, also called "back-end 后道."

**Who dominates the back-end:**
- **OSAT 封测**: **ASE 日月光 (Taiwan, ~30% global)**, **Amkor 安靠 (US, HQ in Korea origin, ~15%)**, **JCET 长电科技 (China, ~12%)**, **TongFu 通富微电 (China)**, **HuaTian 华天科技 (China)**. China holds ~38% of global OSAT revenue thanks to its big three.
- **Test equipment 测试设备**: **Teradyne 泰瑞达 (US) and Advantest 爱德万 (Japan)** are a near-duopoly with ~90%+ combined share. China's **华峰测控 / Accotest** and **长川科技 / Hangzhou Changchuan** are the local rising players.
- **Wafer dicing/probe 划片/探针**: Disco 迪斯科 (Japan) for dicing saws; FormFactor 福姆法克特 (US) for probe cards.
- **Advanced packaging 先进封装** (CoWoS, HBM stacking, chiplets): TSMC 台积电 itself for CoWoS (the AI accelerator packaging that NVIDIA depends on); ASE for fan-out and SiP. This is the new battleground — "back-end" is increasingly where the action is for AI chips.

---

## Quick Glossary of the Materials in the Diagram

| Material in diagram | What it really is | Who makes it |
|---|---|---|
| **Sand** | Quartz sand (SiO₂), refined into 9N-pure polysilicon | Wacker, GCL, Tongwei |
| **Special gas** | Argon, nitrogen, and a long list of "electronic specialty gases" (NF₃, WF₆, HBr, etc.) | Air Liquide, Linde, Air Products, 华特气体, 金宏气体 |
| **Seed crystal doping** | Boron / phosphorus added to the silicon melt to tune electrical properties | Shin-Etsu, SUMCO, GlobalWafers, 沪硅产业 |
| **Slicing liquid** | Glycol-based coolant with abrasive particles | Fujimi, Saint-Gobain |
| **Grinding & polishing slurry** | Silica- or ceria-based nano-slurry | Fujimi, Cabot, 安集科技 |
| **Deionized water** | Ultra-pure H₂O, purer than pharmaceutical grade | Made on-site at the fab |
| **Photoresist** | Light-sensitive polymer (KrF, ArF, EUV grades, each more advanced) | JSR, Tokyo Ohka, Shin-Etsu, Sumitomo, DuPont, 南大光电, 彤程新材 |
| **Developing solution** | Tetramethylammonium hydroxide (TMAH) | Same photoresist suppliers + chemicals firms |
| **Ion embedded** | Boron, phosphorus, arsenic ions accelerated into silicon | Implanter from Applied Materials |
| **Photoresist solvent** | Stripper chemical (sulfuric acid + hydrogen peroxide, or organic solvent) | Entegris, BASF |
| **Etching chemical / gas** | HF (wet), or NF₃ / CF₄ / SF₆ / Cl₂ (plasma) | Air Liquide, Linde, 华特气体, 中船特气 |
| **Mask removal chemical** | "Stripper" — sulfuric / hydrogen peroxide mix ("piranha") | Entegris, Versum / Merck |
| **Polycrystalline silicon (in wafer fab)** | Thin film of polysilicon deposited inside the fab via CVD | Made on-site using gases from Air Products etc. |
| **High-K and high-purity gas** | Hafnium / zirconium / titanium precursors (e.g. TEMAH, TDMAH) | ASM, Air Liquide, Versum |
| **Copper & other metals** | Copper, tungsten, titanium, aluminium, tantalum, cobalt | Mitsubishi Materials, Sumitomo Metal Mining |
| **Copper ion / electroplating solution** | CuSO₄ + organic additives | Atotech (now MKS), Dow, 安集科技 |
| **CMP slurry & pad** | Silica or ceria slurry; polyurethane pad | Cabot, Versum, Fujimi, 鼎龙股份, 安集科技 |

---

## The 30-Second Recap

1. **Make the wafer.** Refine sand into pure silicon, grow a giant single crystal, slice it, polish it, clean it.
2. **Print and carve, 50–100 times.** Coat with photoresist, shine UV through a mask, develop the pattern, then either bombard the exposed silicon with ions (to change its electrical character) or etch it away (to carve out shapes).
3. **Build the transistor.** Lay down a high-K insulator and a metal gate to make the actual switch.
4. **Wire it up.** Stack 10–20 layers of copper wiring, polishing flat between each one.

Each pass through this loop deposits one more nanometre-thin layer. After ~12 weeks and ~$3,000–$15,000 of processing per wafer (depending on node), you slice it up into hundreds of chips and ship them — and the silicon disc that started as a handful of sand becomes the brain inside your phone, car, fridge, and earbuds.
