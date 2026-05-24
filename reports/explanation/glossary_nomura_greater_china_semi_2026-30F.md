# Glossary — Nomura *Greater China Semi: A guide to Semi renaissance in 2026~30F*

> Companion to the Nomura Anchor Report dated **2026-05-21** (139 pages, file_id `184121852855252`).
> Use this as a primer **before** opening the PDF. Each term has a plain-English explanation, a one-line "what to know for this report," and (where useful) a page pointer.

---

## 0. How to read the report

| If you only have 30 min, read these pages | What you get |
|---|---|
| **p. 1-3** | Cover + recommended-stock table (8 names, price targets) |
| **p. 4-5** | Executive summary + technology timeline (Fig. 3 + Fig. 4) |
| **p. 6-12** | The seven technical themes (skim section headers, look at figures) |
| **p. 13-14** | TSMC capex + localization (the big macro catalyst) |
| **p. 15-17** | One-paragraph thesis per recommended stock |
| **p. 18-30** | Material market size, share by company, share by region |
| **p. 80+** | Company-by-company deep dives (each gets ~10-15 pages) |

Pages with **figures (charts/tables)** are usually more informative per minute than pages of text — the report is heavy on data visualizations.

---

## 1. Process node naming (the "Nm" code)

The smaller the number, the more advanced the node. Up through ~28nm the number meant the actual transistor gate length; below that it became a **marketing label** that doesn't map to any single physical dimension.

| Label | Era | Lead foundry node |
|---|---|---|
| **N7 / 7nm** | 2018-2019 HVM | TSMC, Samsung |
| **N5 / 5nm** | 2020 HVM | TSMC iPhone-12 / M1 era |
| **N3 / 3nm** | 2022-2023 HVM | TSMC iPhone-15 |
| **N2 / 2nm** | 2025-2026 HVM | TSMC — **first GAA node** |
| **A16** | 2026-2027 HVM | TSMC — **first BPD node** |
| **A14** | 2028F | TSMC roadmap |
| **A10** | 2029-2030F | First **High-NA EUV** node (Nomura assumption) |
| **A7 / A5 / A3 / A2** | 2031F+ | Speculative roadmap extension (Fig. 72) |

- "**A**" prefix = **Ångström** (10 Å = 1 nm). TSMC switched from "nm" to "Å" at A16 to keep the numbers marketing-friendly.
- **HVM** = High-Volume Manufacturing (the node is shipping in millions of wafers, not just prototypes).

---

## 2. Lithography — the hardest section of the report

Lithography = "printing" the transistor pattern onto silicon using light. The smaller the wavelength of light, the finer the pattern.

### 2.1 Light source / scanner

| Term | Meaning | One-liner |
|---|---|---|
| **DUV** | Deep Ultra-Violet (193nm wavelength) | Mature lithography, used for ≥7nm nodes. Workhorse machines = ASML's NXT series. |
| **EUV** | Extreme Ultra-Violet (13.5nm wavelength) | Used from 7nm onwards. Single ASML EUV machine = ~$200mn. |
| **Low-NA EUV** | NA = 0.33 | Today's mainstream EUV — used at N7/N5/N3/N2/A16. |
| **High-NA EUV** | NA = 0.55 | Next-gen EUV. One machine ~$350mn. **Won't go mainstream until 2029-30F (A10 node)** per Nomura — this is a key timing assumption in the report. |
| **NA** | Numerical Aperture | A measure of how steeply the lens can focus light. Higher NA = finer patterns but stronger geometric constraints. |
| **DUV → EUV → High-NA EUV** | The historical scaling path of light sources | See Fig. 5 (p. 6) — pitch goes from ~70nm (DUV) to ~16nm (High-NA EUV). |

### 2.2 Photoresist (PR) — the "ink" that prints the pattern

| Term | Meaning | Why it matters |
|---|---|---|
| **Photoresist (PR)** | Light-sensitive chemical coating on the wafer. Gets developed away to leave the pattern. | Every lithography step needs PR. Material value rises sharply with each new node. |
| **g-line / i-line** | Old visible-light PR | Used for very mature nodes. |
| **KrF** | Krypton Fluoride (248nm) PR | Used for ~130nm-90nm. |
| **ArF** | Argon Fluoride (193nm) PR | Used for 90nm down to ~7nm via immersion. |
| **EUV PR** | Photoresist for EUV light | Current chemically amplified resist (CAR) — works up to ~20nm pitch. |
| **MOR** (Metal Oxide Resist) | Tin-oxide based photoresist | **Required for High-NA EUV** — at <16nm pitch the old CAR-style PR is physically too thick. MOR can be much thinner. See Fig. 14-15 (p. 10). |
| **High-NA MOR** | MOR specifically for High-NA EUV | One of the biggest new-material opportunities in the report — AEMC, Dinglong are positioned for this. |
| **CAR** (Chemically Amplified Resist) | The dominant PR chemistry since the 1990s | Hits a physical limit at High-NA EUV. |
| **BARC** (Bottom Anti-Reflective Coating) | A layer underneath the PR | Stops light reflection from the substrate that would blur the pattern. Part of the "PR auxiliary" market. |
| **PR auxiliary** | Developer, EBR (Edge-Bead Remover), rinse, cleaner, etc. | The ecosystem of chemicals around PR. AEMC is a Taiwan-based PR-auxiliary leader. |

### 2.3 Photomask — the "stencil"

| Term | Meaning |
|---|---|
| **Photomask** | The transparent quartz plate carrying the chip's pattern. Light shines through it onto the wafer. |
| **Blank** | An unwritten photomask (just quartz + multilayer + absorber). |
| **EUV mask / EUV blank** | A reflective (not transparent) mask used for EUV. Has 40+ Mo/Si multilayer mirrors. |
| **Absorber** | The "ink" layer of the mask that blocks/attenuates light. **Today = TaBN; for High-NA may switch to Ru/Mo-based** (Fig. 67-69, p. 38-39). |
| **attPSM** (Attenuated Phase-Shifting Mask) | A mask that doesn't fully block light but shifts its phase to sharpen the pattern. |
| **Stitch overlay** | Stitching together exposures on a chip too large for one High-NA EUV field. Adds a tolerance/yield challenge. |

---

## 3. Transistor architecture — how the switch is built

A transistor = a gate that turns electron flow on/off. As nodes shrink, the gate-to-channel contact area shrinks, so the design has to evolve.

| Term | Meaning | When mainstream |
|---|---|---|
| **Planar** | Gate sits flat on a 2D channel | ~28nm and older |
| **FinFET** | Channel is a vertical "fin" — gate wraps three sides | 16nm / 14nm to 5nm — Apple's M-series CPUs |
| **GAA / GAAFET** (Gate-All-Around FET) | Gate wraps all four sides of the channel | **N2 (2025-2026) onwards** — main story of the report |
| **Nanowire / Nanosheet / Forksheet** | Three flavors of GAA channel geometry | Nanosheet is the dominant industry choice. Forksheet = future. |
| **CFET** (Complementary FET) | Stacks NMOS and PMOS transistors **vertically** | The post-GAA bet (~2030F+). Doubles density without further pitch shrink. |
| **Metal pitch** | The minimum distance between two metal lines | The "real" scaling metric — see Fig. 5 (p. 6). Has gone from 70nm at N16 to ~16nm at A10. |

### 3.1 Backside Power Delivery (BPD) — the second-biggest story

| Term | Meaning |
|---|---|
| **BPD** | Moves the power network from above the transistor (where it competes with signal wires) to **the backside of the silicon wafer** |
| **BEOL** (Back-End-Of-Line) | The wiring layers on top of the transistor — copper lines, vias, ILD |
| **FEOL** (Front-End-Of-Line) | The transistor itself + the immediate gate stack |
| **nTSV** (nano-Through-Silicon Via) | A vertical hole drilled through the thinned wafer to connect frontside to backside |
| **PPA** (Power, Performance, Area) | The three KPIs every node tries to improve |
| **TSMC A16** | The first commercial BPD node | Coming ~2026-2027 HVM |
| Why it matters | BPD requires **a second silicon wafer + wafer bonding + grinding to ~1µm + selective etch** — doubles content for Kinik (reclaim wafer), GWC (more silicon used), Anji/Dinglong (more CMP), Besi (more bonding tools). See Fig. 8 (p. 8). |

---

## 4. Fab process steps — the "verbs" of chipmaking

| Term | Meaning | Why it matters in this report |
|---|---|---|
| **ALD** (Atomic Layer Deposition) | Deposits material one atomic layer at a time | Needed for GAA, BPD, and most leading-edge films. ALD volumes scale faster than node count. |
| **CVD** (Chemical Vapor Deposition) | Deposits material from a gas-phase chemical reaction | Workhorse deposition technique. |
| **PVD / Sputtering** | Physically blasts metal atoms onto the wafer using ion bombardment | Used for metal layers. Targets = pure metal disks consumed in the process. |
| **CMP** (Chemical Mechanical Planarization / Polishing) | Polishes the wafer flat using slurry + a pad | Critical between layers. **Each new node adds ~20-30% more CMP steps** (Anji, Dinglong, Kinik all benefit). |
| **CMP slurry** | The liquid abrasive + chemistry used in CMP | Anji is China's leader; Cabot/DuPont/Versum globally. |
| **CMP pad** | The polishing surface | Dinglong is the China leader; DuPont/3M globally. |
| **CMP pad conditioner** (DBU = Diamond Body Unit) | A diamond-coated disk that keeps the pad surface "fresh" | **Kinik has ~80% share at TSMC's N2 node** vs 3M — see p. 105. |
| **Etching (anisotropic vs isotropic)** | Removes material — directionally (vertical) or all-around (selective) | GAA requires both, in alternating steps (Fig. 7, p. 7). |
| **ICP** (Inductively Coupled Plasma) | A type of plasma etching reactor used for anisotropic etching | |
| **RPS** (Remote Plasma Source) | A reactor used for isotropic / selective etching | |
| **Wafer thinning / grinding** | Polishing the wafer down to ~50µm or thinner | Needed for 3D stacking, BPD, advanced packaging. |
| **Reclaim wafer / test wafer** | Used wafers polished back to a usable state for test/dummy purposes | Kinik's "SBU" business. Volume scales with BPD + wafer bonding. |

---

## 5. Advanced packaging — the "second pillar"

When transistor scaling slows, you instead stack/connect multiple chips with sophisticated packaging.

| Term | Meaning |
|---|---|
| **2.5D packaging** | Multiple dies sit side-by-side on a common interposer (silicon or organic) |
| **3D packaging** | Dies stacked vertically and connected through the silicon |
| **SoIC** (System on Integrated Chips) | TSMC's brand for 3D die stacking using hybrid bonding | The single most strategic packaging tech for AI chips. **AMD EPYC = 7 CCDs in SoIC (Fig. 9, p. 8).** |
| **CoWoS** (Chip-on-Wafer-on-Substrate) | TSMC's 2.5D packaging brand | Used for NVIDIA H100/B200, all major AI accelerators. Capacity = the #1 bottleneck of the AI buildout. |
| **CoPoS** | Successor to CoWoS — uses a panel-style substrate instead of a wafer-style interposer | Expected ~2028. |
| **EMIB / EMIB-T** | Intel's bridge-style packaging | Smaller silicon bridges embedded in the substrate. Intel + Ibiden + Unimicron supply chain. |
| **Hybrid bonding** | Bonds two wafers (or chip-to-wafer) via copper-copper + SiO₂-SiO₂ direct bonding | No solder bumps needed. Densest interconnect possible. **Besi is the equipment leader.** |
| **D2D / C2W / W2W** | Die-to-die / chip-to-wafer / wafer-to-wafer | Three flavors of hybrid bonding. W2W = highest throughput but least flexible. |
| **TSV** (Through-Silicon Via) | A vertical metal interconnect through a silicon die | Used for HBM stacks and 3D packaging. |
| **RDL** (Re-Distribution Layer) | A layer of fine wiring that "re-routes" pads from one pattern to another | Built on top of a substrate or interposer. |
| **Underfill** | Liquid resin between two stacked dies that mechanically locks them | |
| **ABF** (Ajinomoto Build-up Film) | The current high-end packaging substrate material | Made by Japan's Ajinomoto. Cost ~USD 200 per advanced unit. |
| **Glass Core Substrate** | A glass plate replacing ABF as the substrate core | Better heat, lower warpage, lower signal loss. **Broadcom = lead customer, ramp 2027-28F.** See p. 11, 85-88. |
| **TGV** (Through-Glass Via) | A laser-drilled hole through glass + copper plating | The hardest step in glass-core substrate. Current cost ~USD 400-500 per unit (vs target ≤USD 400). |
| **RDL delamination** | Copper traces peeling off the glass surface | The biggest technical bottleneck for glass-core mass production (Fig. 146, p. 86). |

---

## 6. Memory — HBM, 3D NAND, wafer-bonded NAND

| Term | Meaning |
|---|---|
| **DRAM** | Dynamic RAM — the main memory in every chip |
| **HBM** (High Bandwidth Memory) | Stacks of 8-16 DRAM dies connected by TSVs, sitting next to an ASIC | Critical for AI training. SK hynix > Micron > Samsung in share. |
| **HBM3 / HBM4** | Generations of HBM. HBM4 = 2026-2027 ramp. | |
| **3D NAND** | NAND flash with hundreds of vertical cell layers (currently 200+ layers) | Samsung, SK hynix, Kioxia, Micron, YMTC. |
| **Xtacking** | YMTC's wafer-bonded NAND tech | Bonds a logic wafer + a memory cell wafer together. Different from the conventional monolithic 3D NAND approach. See Fig. 12 (p. 9). |
| **Wafer-bonded NAND** | Generic term for the same idea | Increases bandwidth and reduces die size. Drives wafer + bonding + CMP demand. |
| **DRAM-on-Logic** | A logic die with a DRAM die bonded on top via WoW | Replaces external memory bus with vertical bonded I/O. |
| **WoW / CoW** | Wafer-on-Wafer / Chip-on-Wafer bonding variants | |

---

## 7. Wafers & substrates

| Term | Meaning |
|---|---|
| **Semi wafer** | The blank silicon disk that everything is built on | 300mm (12") is the dominant size for logic and memory. |
| **300mm / 12" wafer** | 12-inch silicon wafer, ~6,000 die per wafer for a small chip | Shin-Etsu, SUMCO, GlobalWafers, Siltronic, SK Siltron, NSIG dominate (Fig. 35, p. 23). |
| **200mm / 8" wafer** | Older size, used for power chips, analog, automotive | Less relevant to this report. |
| **SOI** (Silicon-on-Insulator) | Wafer with a thin Si layer on top of an oxide layer | Reduces parasitic capacitance — used for RF and FD-SOI logic. |
| **FD-SOI** (Fully Depleted SOI) | A specific SOI variant good for ultra-low-power | Soitec's bread-and-butter. |
| **RF SOI** | SOI optimized for RF front-end chips (cellular radios) | The biggest current SOI market — every iPhone uses it. |
| **Photonic SOI / PSOI** | SOI optimized for silicon photonics (low optical loss) | Soitec's big growth driver. Used to build SiPh PICs for CPO and optical modules. |
| **InP** (Indium Phosphide) | III-V compound semiconductor used for lasers and optical detectors | Critical for 1.6T optical modules. Sumitomo Electric, AXT, JX dominate. |
| **InP substrate** | Polished InP crystal disk | **THE supply bottleneck in optical** — low yield + China indium export control. |
| **InP epi wafer** | InP substrate with epitaxial layers grown on top via MOCVD | Less constrained than substrate. |
| **GaAs / Ge / SiGe** | Other III-V or strained semiconductor materials | Various RF, optical, or strain-engineering uses. |
| **SiGe superlattice wafers** | Alternating Si/SiGe layers used to build GAA channels | Required input for N2 GAA fabs. |

---

## 8. Photonics & optical (CPO chapter)

The optical interconnect inside AI data centers is replacing copper because copper can't carry 1.6Tbps over more than ~1 meter.

| Term | Meaning |
|---|---|
| **Optical transceiver** | A pluggable module that converts electrical signals to light and vice versa | Currently 400G/800G; 1.6T ramps 2026-27. |
| **CPO** (Co-Packaged Optics) | Optical engine sitting inside the same package as the switch/ASIC | Reduces power and latency vs pluggable modules. Big content uplift for InP/SiPh. |
| **NPO** (Near-Packaged Optics) | Intermediate step — optics next to (not inside) the package | |
| **SiPh** (Silicon Photonics) | Photonic ICs built on a silicon (SOI) wafer | Foundry: TSMC, Tower, GlobalFoundries. |
| **PIC** (Photonic Integrated Circuit) | The chip itself that contains lasers, modulators, detectors | |
| **EML** (Electro-absorption Modulated Laser) | A type of laser used in conventional pluggable transceivers | InP-based. |
| **CW Laser** (Continuous Wave) | A constant-output laser used as a light source in SiPh-based transceivers | InP-based. |
| **PD / TIA** | Photodetector / Trans-Impedance Amplifier | The receiver side. Often InP or Ge-on-Si. |
| **MOCVD** (Metal-Organic Chemical Vapor Deposition) | The deposition tool used to grow epi layers on InP/GaAs | **Lead time > 1 year** — a real-world supply constraint for InP capacity. |
| **Ge on Si** | Germanium grown on silicon | Alternative to InP for some photodetector applications. |

---

## 9. Business / industry shorthand

| Term | Meaning |
|---|---|
| **Foundry** | A pure-play chip manufacturer that doesn't design its own chips | TSMC, Samsung Foundry, Intel Foundry, SMIC. |
| **IDM** (Integrated Device Manufacturer) | Designs AND manufactures its own chips | Intel, Samsung, Micron, SK hynix. |
| **Fabless** | Designs but doesn't manufacture | NVIDIA, AMD, Qualcomm, Broadcom, Apple. |
| **OSAT** (Outsourced Semiconductor Assembly and Test) | Outsourced packaging house | ASE (TW), Amkor (US), JCET (CN). |
| **HVM** | High-Volume Manufacturing | The "shipping in millions of wafers" stage. |
| **Capex** | Capital expenditure on equipment + fab buildings | TSMC's 2027F capex = ~USD 70bn per Nomura. |
| **Capex intensity** | Capex ÷ revenue | ~50% at TSMC's 1.6nm HVM peak. |
| **TAM** (Total Addressable Market) | The full market for a product category | E.g. CMP slurry TAM in China = CNY 10.5bn by 2028F. |
| **ASP** (Average Selling Price) | Per-unit revenue | |
| **BOM** (Bill of Materials) | The cost breakdown of a product | See Fig. 145 (p. 86) for glass-core BOM. |
| **Agentic AI** | AI that takes autonomous actions, not just chat completion | The Nomura demand-growth assumption — assumes Agentic AI workloads explode 2026-30F. |
| **ASIC** | Application-Specific Integrated Circuit | Custom chips for AI (e.g. Broadcom/Google TPU, AWS Trainium). |
| **SoC** (System-on-Chip) | A single chip with CPU + GPU + I/O + memory controller | Apple M-series is the archetype. |

---

## 10. Company tickers cheat sheet

Quick map of the names you'll see in the report:

### The 8 recommended stocks

| Code | Company | Business | Bank Rating |
|---|---|---|---|
| **4749 TT** | AEMC (Advanced Echem Materials) | PR auxiliary → photoresist for TSMC | Buy (initiated) |
| **1560 TT** | Kinik Company | CMP pad conditioner + reclaim wafer | Buy (initiated) |
| **4768 TT** | Ingentec | Specialty gas + TGV (glass-core) | Buy (initiated) |
| **BESI NA** | BE Semiconductor (Besi) | Hybrid bonding tools | Buy (maintained) |
| **SOI FP** | Soitec | SOI wafer (RF, FD, photonic) | Buy (maintained) |
| **6488 TT** | GlobalWafers (GWC) | 300mm silicon wafer | **Buy (upgraded from Neutral)** |
| **300054 CH** | Dinglong | CMP pad + slurry + photoresist | Buy (maintained) |
| **688019 CH** | Anji Microelectronics | CMP slurry | Buy (maintained) |

### Frequently-mentioned non-rated names

| Code | Company | Why it appears |
|---|---|---|
| **2330 TT** | TSMC | The whole report's macro anchor |
| **ASML US** | ASML | EUV / High-NA EUV monopoly |
| **MMM US** | 3M | The competitor Kinik is taking share from |
| **6146 JP** | Disco | Wafer-grinding wheel leader Kinik wants to enter |
| **4062 JP** | Ibiden | ABF substrate + EMIB-T partner for Intel |
| **6967 JP** | Shinko | ABF substrate maker |
| **4368 JP** | Fuso | Ultra-high-purity silica sol supplier — Anji's risk |
| **AMD US / NVDA US** | AMD / NVIDIA | AI chip demand customers |
| **AVGO US** | Broadcom | Lead glass-core substrate customer |
| **LITE / COHR US** | Lumentum / Coherent | Optical IDM — InP epi wafer demand drivers |
| **CBT / DD US** | Cabot / DuPont | CMP material incumbents Anji is taking share from |

---

## 11. Acronym quick-reference (alphabetical)

| Acronym | Full term |
|---|---|
| **ABF** | Ajinomoto Build-up Film |
| **ALD** | Atomic Layer Deposition |
| **ASP** | Average Selling Price |
| **BARC** | Bottom Anti-Reflective Coating |
| **BEOL** | Back-End-Of-Line |
| **BPD** | Backside Power Delivery |
| **CAR** | Chemically Amplified Resist |
| **CFET** | Complementary FET |
| **CMP** | Chemical Mechanical Polishing/Planarization |
| **CoPoS** | Chip-on-Panel-on-Substrate (successor to CoWoS) |
| **CoWoS** | Chip-on-Wafer-on-Substrate |
| **CPO** | Co-Packaged Optics |
| **CVD** | Chemical Vapor Deposition |
| **DBU** | Diamond Body Unit (= CMP pad conditioner) |
| **DUV** | Deep Ultra-Violet |
| **EMIB** | Embedded Multi-die Interconnect Bridge |
| **EML** | Electro-absorption Modulated Laser |
| **EUV** | Extreme Ultra-Violet |
| **FD-SOI** | Fully Depleted Silicon-on-Insulator |
| **FEOL** | Front-End-Of-Line |
| **GAA / GAAFET** | Gate-All-Around (FET) |
| **HBM** | High Bandwidth Memory |
| **HVM** | High-Volume Manufacturing |
| **ICP** | Inductively Coupled Plasma |
| **IDM** | Integrated Device Manufacturer |
| **InP** | Indium Phosphide |
| **MOCVD** | Metal-Organic Chemical Vapor Deposition |
| **MOR** | Metal Oxide Resist |
| **NA** | Numerical Aperture |
| **NPO** | Near-Packaged Optics |
| **nTSV** | nano-Through-Silicon Via |
| **OSAT** | Outsourced Semiconductor Assembly & Test |
| **PIC** | Photonic Integrated Circuit |
| **PPA** | Power, Performance, Area |
| **PR** | Photoresist |
| **PSPM / attPSM** | (Attenuated) Phase-Shifting Mask |
| **PSOI** | Photonic Silicon-on-Insulator |
| **PVD** | Physical Vapor Deposition (= Sputtering) |
| **RDL** | Re-Distribution Layer |
| **RPS** | Remote Plasma Source |
| **SiPh** | Silicon Photonics |
| **SoC** | System-on-Chip |
| **SoIC** | System on Integrated Chips (TSMC's 3D packaging) |
| **SOI** | Silicon-on-Insulator |
| **TAM** | Total Addressable Market |
| **TGV** | Through-Glass Via |
| **TSV** | Through-Silicon Via |
| **W2W / C2W / D2D** | Wafer/Chip/Die bonding variants |
| **WoW** | Wafer-on-Wafer |

---

## 12. Reading order suggestion

If you want to build understanding incrementally:

1. **Start here** — finish this glossary first (~20 min).
2. **Skim Fig. 3 + Fig. 4** (p. 4-5) — they list every technology + every beneficiary in one place. Treat them as the report's "executive map."
3. **Read p. 6-12 carefully**. This is the technical heart. Focus on the figures:
   - Fig. 5 (metal pitch history)
   - Fig. 6 (Planar → FinFET → GAAFET)
   - Fig. 7 (GAA formation steps)
   - Fig. 8 (BPD process flow)
   - Fig. 9 (hybrid bonding)
   - Fig. 14-15 (PR thickness vs NA)
4. **TSMC capex (p. 13-14)** — short, just two charts.
5. **Stock summaries (p. 15-17)** — three short paragraphs per name.
6. **Then pick ONE company deep dive** (whichever stock you find most interesting). Don't try to read all eight — they're each ~10-15 pages. Suggested order if you want the best ROI on reading time:
   - **Kinik** (p. 105+) — cleanest thesis, clear moat.
   - **Anji** (p. 130+) — best earnings-revision case.
   - **Ingentec** (p. 80-88) — most interesting "optionality" story (TGV).
7. **Skip the appendices** (last ~10 pages) — those are disclosures.

Pages 31-79 are the material-market deep dives (CMP, PR, etching, sputtering, electronic gases, etc.) — useful as a reference but not narratively essential.

---

*Generated 2026-05-24 from `db/zsxq.db` row `file_id=184121852855252` (OCR cached). To re-extract any page from the PDF: `python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id 184121852855252 --pages <N>`.*
