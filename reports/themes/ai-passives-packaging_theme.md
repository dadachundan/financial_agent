# AI Infrastructure Passives & Advanced Packaging

**Created:** 2026-05-31 · **Last refreshed:** 2026-05-31 · **Last mutated:** 2026-05-31 · **Refresh cadence:** monthly · **Languages tracked:** en, zh

## Thesis

The bottleneck for an AI accelerator rack is no longer the die — TSMC's CoWoS-L and Samsung's HBM4 lines have ramped — it is the physical-layer plumbing that wraps the die: the multi-layer ceramic capacitors that filter the kilowatts of power into the package, the ABF (Ajinomoto Build-up Film) substrate that carries the silicon to the PCB, the ultra-low-loss high-speed CCL/PCB that links GPU to switch, and the next generation of glass-core substrates that has to clear commercial mass production by 2027–2028 to support the 2nm-and-below CoPoS / FOPLP roadmap. The bet behind this basket is that each AI-server rack carries a *non-substitutable* multi-thousand-dollar bill of passives and advanced-packaging materials whose suppliers have run at full utilization since 4Q25 and have collectively raised prices 10–35% effective April 2026 — Murata announced 15–35% on AI-server high-cap MLCCs, Yageo 10–20% on high-voltage / high-capacitance lines, and substrate primes are guiding to gross-margin expansion to 22–30% in 2026 ([Astute Group, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/); [Digitimes, 2026-04-20](https://www.digitimes.com/news/a20260420PD216/revenue-pcb-abf-substrate-unimicron-ai-chip.html)).

The quantitative anchor: a single GB300 rack consumes ~30,000 MLCCs vs ~1,000 in a smartphone, and Murata's own outlook puts FY30 AI-server MLCC demand at 3.3× FY25 ([TradingKey, 2026](https://www.tradingkey.com/analysis/stocks/us-stocks/261849833-mlcc-hbm-ai-vsh-tradingkey); [Astute Group MLCC squeeze, 2026](https://www.astutegroup.com/news/general/mlcc-price-increases-threaten-ai-server-build-costs/)). On the ABF side, the substrate shortfall is projected to widen from ~10% in 2H26 to 21% in 2027 and 42% in 2028, with no new capacity online before mid-2026 — a deeper structural under-supply than the 2018 MLCC squeeze ([TradingKey ABF/Ajinomoto, 2026](https://www.tradingkey.com/analysis/stocks/us-stocks/261783966-abf-ajinomoto-nvidia-ai-supply-chain-tradingkey)). On the PCB side, NVIDIA's transition from M6 (Blackwell B100) to M7 (GB300) to M10 (Vera Rubin H2 2026, mass production 2027) is forcing CCL upgrade prices that cost 6–9× standard FR4 ([IT之家, 2026](https://www.ithome.com/0/928/995.htm); [eet-china, 2026](https://www.eet-china.com/mp/a481206.html)).

The vulnerability is twofold. First, MLCC and substrate cycles historically end faster than they start — the 2018 / 2021 episodes ended with 30–50% peak-to-trough corrections in Taiwan substrate names ([eenews europe MLCC shortage history, 2026](https://www.eenewseurope.com/en/ai-drives-mlcc-shortage/)). Second, glass-substrate commercialization is a 2027–2030 event per Intel / TSMC / Samsung's own timelines — pre-revenue exposure (Corning Glass Core, AT&S glass-core) cannot anchor near-term P&L ([Wccftech glass substrate timeline, 2026](https://wccftech.com/intel-backed-glass-substrates-tech-will-be-commercilization-ready-within-three-years/)). The basket is split 9-5-4 across `core` (Chinese MLCC + Asian high-end PCB pure-plays where pricing power is in the print), `enabler` (global substrate + ABF + materials primes), and `adjacent` (glass-substrate and photomask names where the prize is 12–24 months out).

## Scope rules

**In:** MLCC suppliers with disclosed AI-server SKU lines, ABF film and substrate fabricators in the NVIDIA / AMD / Broadcom supply chain, high-end CCL and PCB makers shipping M6+ ultra-low-loss boards for AI accelerators, glass-substrate development programs with stated commercial timelines, photomask / mask-blank houses serving advanced-logic and HBM nodes, and the ABF-monopoly resin supplier (Ajinomoto). Pure-plays and diversified incumbents both qualify if the AI-server BOM is a *named and dated* growth driver in the latest IR disclosure.

**Out:** HBM / DRAM die (separate `memory-upcycle` theme); pure auto-MLCC plays without AI-server exposure (the auto cycle is a separate vector); OSAT / packaging assembly below the substrate level; wafer makers (Shin-Etsu, SUMCO — fall under broader semi materials, not packaging passives specifically); semi-cap-equipment names like AMAT and LRCX (capex enablers, not physical-layer plumbing). Privately-held names (e.g. Powerchip) are not investable as equities and are surfaced in the Watch list at the bottom rather than the basket.

## Tracked tickers

| Ticker | Name | Role | Justification | Added |
|---|---|---|---|---|
| TSE:6981 | Murata Manufacturing 村田製作所 | core | World #1 MLCC by share; announced 15–35% price hike on AI-server high-cap MLCCs effective Apr 1 2026; FY30 AI-server MLCC demand guided at 3.3× FY25; also plans AI-server power module mass-production in 2026 targeting ¥50B by FY27 ([TrendForce, 2025-12](https://www.trendforce.com/news/2025/12/17/news-murata-reportedly-to-mass-produce-ai-server-power-modules-in-2026-targets-%C2%A550b-by-fy27); [Astute Group, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/)). **Note:** also tracked in [humanoid-robotics-sensors basket](humanoid-robotics-sensors_theme.md) for SCH16T-K20 IMU exposure; that listing rides the IMU/SoM angle, this listing rides the MLCC / AI-server power module angle — both theses are independent and additive. | 2026-05-31 |
| TSE:6762 | TDK | core | #2/3 global MLCC franchise alongside Murata + Samsung Electro-Mechanics; explicit AI-server / power-electronics SKU lines plus broader inductor and battery business. **Note:** also tracked in [humanoid-robotics-sensors basket](humanoid-robotics-sensors_theme.md) for IMU exposure; here the MLCC + AI-server BOM thesis is the dominant driver ([Astute Group MLCC squeeze, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/)). | 2026-05-31 |
| TWSE:2327 | Yageo 國巨 | core | Taiwan MLCC + chip-R prime; David Wang guided 1Q26 revenue and op-margin up sequentially on AI orders; announced 10–20% price increases on high-voltage / high-capacitance / automotive MLCC lines effective Apr 2026 ([Digitimes, 2026-02-26](https://www.digitimes.com/news/a20260226PD231/yageo-passive-components-demand-revenue-2026.html); [Astute Group, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/)). | 2026-05-31 |
| TWSE:2492 | Walsin Technology 華新科 | core | Taiwan #2 MLCC fabricator with high-voltage and automotive franchise; participating in the same pricing cycle as Yageo and Murata; 1Y +397% on the AI-driven MLCC pricing reset ([Digitimes Taiwan MLCC AI demand, 2026-05-25](https://www.digitimes.com/news/a20260525PD222/demand-mlcc-high-power-taiwan-high-end.html)). | 2026-05-31 |
| SZSE:300408 | Sanhuan Group 三环集团 | core | China's MLCC leader with a 2025 revenue +22% YoY / NP +20%; 1Q26 earnings growth >46% YoY; achieved 0805 476 high-cap breakthrough in 4Q25 with disclosed batch shipments to Inspur and Huawei AI servers in 2026 ([Sina Finance, 2026-05-27](https://finance.sina.com.cn/wm/2026-05-27/doc-inhzivfn0778202.shtml); [aigbk Sanhuan analysis, 2026](https://www.aigbk.com/article/sanhuan_group_mlcc_business_benefits_from_ai_server_demand/)). | 2026-05-31 |
| SZSE:000636 | Fenghua Hi-Tech 风华高科 | core | China's #2 MLCC supplier; 1Q26 NP +37% YoY with high-end product mix scaling; 1206 high-capacity products in sample testing for AI-server customers; the higher-beta Chinese-substitute trade vs Sanhuan ([aigbk Fenghua analysis, 2026](https://www.aigbk.com/article/fenghua_gaoke_000636_mlcc_leader_ai_computing_demand/); [Sina Finance MLCC AI 5月推荐榜, 2026-05-26](https://finance.sina.cn/stock/jdts/2026-05-26/detail-inhzffss1517949.d.html)). | 2026-05-31 |
| TSE:2802 | Ajinomoto 味の素 | enabler | Sole supplier of ABF (Ajinomoto Build-up Film) — the dielectric resin used in every NVIDIA / AMD / Broadcom flip-chip substrate; ABF + CDMO drove FY26 record business profit ¥181.1B (+13.7% YoY); ABF tied to GB300 → Rubin BOM density step-up; Functional Materials segment guided to double-digit growth through FY26 ([BigGo Finance Ajinomoto FY26 IR, 2026-05](https://finance.biggo.com/news/jpx_tdnet_140120260501516433); [TradingKey ABF/Ajinomoto, 2026](https://www.tradingkey.com/analysis/stocks/us-stocks/261783966-abf-ajinomoto-nvidia-ai-supply-chain-tradingkey)). | 2026-05-31 |
| TSE:4062 | Ibiden イビデン | enabler | Dominant NVIDIA FC-BGA substrate supplier; new Gifu fab ramped to 25% in 4Q25 and targeting 50% utilization by Mar 2026; ¥500B three-year capex plan announced for AI-server FC-BGA capacity; CEO Kawashima publicly stated customers "purchasing all of Ibiden's products" ([Bloomberg Ibiden expansion, 2024-12](https://www.bloomberg.com/news/articles/2024-12-29/nvidia-supplier-ibiden-weighs-faster-expansion-to-meet-ai-demand); [Allelco AI substrate update, 2025](https://www.allelcoelec.com/news/nvidia-ai-chip-substrate-supplier-ibiden-accelerates-production-expansion-to-cope-with-surging-deman.html)). | 2026-05-31 |
| TWSE:3037 | Unimicron Technology 欣興電子 | enabler | Taiwan #1 ABF substrate fabricator; estimated 30–40% share of US GPU substrate market; targeting record 2026 revenue exceeding 2022 peak; substrate prices guided up 5–10% in 2H26, full capacity through 2027 ([Digitimes Unimicron revenue 2026, 2026-05-29](https://www.digitimes.com/news/a20260529PD239/unimicron-revenue-2026-demand-substrate.html); [Digitimes ABF crunch, 2026-01-30](https://www.digitimes.com/news/a20260130PD220/unimicron-abf-substrate-ai-server-market-capacity.html)). | 2026-05-31 |
| TWSE:8046 | Nan Ya PCB 南亞電路板 | enabler | Vertically integrated ABF + BT substrate supplier; dual focus strengthens negotiating position in the substrate shortage; selling out in 2026 alongside Unimicron and Kinsus ([Digitimes ABF sells out, 2026-04-20](https://www.digitimes.com/news/a20260420PD216/revenue-pcb-abf-substrate-unimicron-ai-chip.html)). | 2026-05-31 |
| TWSE:3189 | Kinsus Interconnect 景碩科技 | enabler | The third leg of the Taiwan ABF triumvirate (with Unimicron and Nan Ya PCB); operating at full capacity for AI customers as the substrate sell-out continues into 2027 ([Digitimes ABF sells out, 2026-04-20](https://www.digitimes.com/news/a20260420PD216/revenue-pcb-abf-substrate-unimicron-ai-chip.html)). | 2026-05-31 |
| SZSE:002463 | WUS Printed Circuit 沪电股份 | core | "T0" tier Chinese AI-server PCB supplier with disclosed M6+ orders from US, EU, and China customers; 1Q26 revenue +54% YoY on AI demand; NVIDIA-Wus joint M10 CCL material test with 52-layer PCB mass production targeted Q4 2026 – Q1 2027 for the Rubin platform ([WallStreetCN, 2026](https://wallstreetcn.com/articles/3770620); [IT之家 M10 CCL test, 2026](https://www.ithome.com/0/928/995.htm)). | 2026-05-31 |
| SZSE:002916 | Shennan Circuits 深南电路 | core | China T1 AI-server PCB + IC-substrate dual-platform; 2025 revenue ¥23.6B (+32% YoY) / NP ¥3.28B (+74%); Guangzhou FC-BGA line targeting 200M units annual capacity at full ramp; 16-layer-and-below FC-BGA in batch production ([Futubull 002916 deep, 2026](https://news.futunn.com/en/post/66751905/shennan-circuits-002916-ai-pcb-and-substrate-packaging-see-upward); [东方财富 002916 深度, 2026-01](https://pdf.dfcfw.com/pdf/H3_AP202601041814856702_1.pdf?1767562303000.pdf=)). | 2026-05-31 |
| SZSE:002938 | Avary Holding 鹏鼎控股 | core | World #1 PCB by revenue (¥39.2B 2025) and global #1 FPC (~30% share); AI-server + optical-module PCB business posted double-digit growth two quarters running; Huai'an ¥11B + Thailand ¥4.3B capex for advanced HDI / HLC capacity serving AI customers; 800G / 1.6T optical-module products in mass production with 3.2T in development ([东方财富 鹏鼎AI觉醒, 2026-05-24](https://caifuhao.eastmoney.com/news/20260524235130296585900); [Futunn 鹏鼎 FPC, 2026](https://news.futunn.com/en/post/50585301/avary-holding-002938-under-the-wave-of-ai-fpc-is)). | 2026-05-31 |
| SSE:600183 | Shengyi Technology 生益科技 | core | China #1 high-end CCL maker; M7/M8/M9 ultra-low-loss CCL portfolio supports AI-server PCB upstream; 1Q26 revenue ¥8.14B (+45% YoY) / NP ¥1.16B (+105.5%); the upstream pricing-power play in the Chinese AI PCB stack ([futunn 生益科技 1Q26, 2026](https://news.futunn.com/post/72564670/shengyi-technology-600183-sh-2025-annual-report-and-q1-2026); [ai-gupiao Shengyi 26Q1, 2026](https://www.ai-gupiao.com/research/summary/34343)). | 2026-05-31 |
| WBAG:ATS | AT&S Austria Technologie | enabler | European IC-substrate supplier with high-end exposure to one named AI customer; announced May 2026 Chongqing AI-substrate capacity expansion guided to a "high double-digit million" EBIT contribution in FY26/27 fully financed by long-term customer agreements; also advancing glass-core substrate program for AI / HPC ([evertiq AT&S Chongqing AI, 2026-05-26](https://evertiq.com/news/2026-05-26-ats-expands-ai-substrate-capacity-in-chongqing); [AT&S glass-core press, 2026](https://ats.net/en/press/ats-advances-glass-core-substrates-for-ai-high-performance-computing-and-photonics/)). | 2026-05-31 |
| NYSE:GLW | Corning | adjacent | Specialty-glass franchise pivoting toward semi packaging via the Glass Core program; May 2026 multi-year NVIDIA optical-connectivity partnership announcement; Advanced Packaging Carriers product line for fan-out processes already shipping; the listed proxy for the 2027–2030 organic-to-glass substrate transition ([FinancialContent Corning glass architecture, 2026-02-10](https://markets.financialcontent.com/wral/article/finterra-2026-2-10-the-glass-architecture-of-ai-a-comprehensive-research-feature-on-corning-inc-glw); [Corning Advanced Packaging Carriers, 2025](https://www.corning.com/worldwide/en/products/advanced-optics/product-materials/PrecisionGlassSolutions/advanced-packaging-carriers-release.html)). | 2026-05-31 |
| NASDAQ:PLAB | Photronics | adjacent | One of three global merchant photomask houses (with Toppan and DNP); Q2 FY26 revenue $209.9M missed on delayed design releases but commentary cited "strong demand for leading-edge memory and logic chips used in AI applications" requiring high-end masks; substantial US + Korea capex investments shifting mix to advanced-node masks ([Photronics Q2 FY26 8-K, 2026](https://www.sec.gov/Archives/edgar/data/0000810136/000114036126023057/ef20074970_ex99-1.htm); [PLAB Q2 FY26 transcript, 2026-05-29](https://www.fool.com/earnings/call-transcripts/2026/05/29/photronics-plab-q2-2026-earnings-transcript/)). | 2026-05-31 |

**Geographic / role mix (18 tickers):** Japan 3 (17%) · Taiwan 4 (22%) · CN A-share 7 (39%) · Austria 1 (6%) · US 3 (17%). Role: core 9, enabler 5, adjacent 4.

## Exclusions

| Ticker | Reason for exclusion |
|---|---|
| TSE:6967 (Shinko Electric Industries 新光電気工業) | Delisted from TSE Prime Market on Jun 6 2025 following JIC consortium take-private at ¥5,920/share (tender period Feb 18 – Mar 18 2025, cash settlement Aug 29 2025). No longer investable as a listed equity. Re-evaluate only if a re-IPO of the consortium-owned entity is announced ([JPX Decision on Delisting, 2025-05-20](https://www.jpx.co.jp/english/news/1023/20250520-11.html); [Shinko delisting notice, 2025-06-05](https://www.shinko.co.jp/english/news/docs/20250605-01_en.pdf)). |
| TSE:7912 (Dai Nippon Printing 大日本印刷) | Overlap with Toppan in the photomask + ABF substrate space; Photronics covers the merchant-photomask vector cleanly. DNP's commercial photomask agreements with Rapidus target 2027 2nm mass-production rather than 2026 AI-server BOM — re-evaluate when Rapidus moves to Risk Production ([Digitimes DNP Rapidus, 2024-03-27](https://www.digitimes.com/news/a20240327PD213/dai-nippon-printing-photomask-rapidus-2nm.html)). |
| TSE:7911 (Toppan Holdings 凸版印刷) | Photomask EUV / IBM partnership is real but the printed photomask + advanced-packaging mix is buried inside a ¥1.6T print-and-services holding; the AI-related signal is diluted vs PLAB. 1Y total return only +18.9% reflects the dilution. Re-evaluate if Toppan spins out its semiconductor electronics unit ([TOPPAN Strategic Repositioning, 2025-12](https://www.ainvest.com/news/toppan-ai-semiconductor-pivot-strategic-repositioning-growth-catalyst-2512/)). |
| TWSE:4961 (Eson Precision Industry 怡上精密) | Listed as an "advanced-substrate adjacent" candidate but no specific AI-server BOM disclosure surfaced; 1Y −14.7% confirms the de-coupling from the AI substrate / passive trade. Re-evaluate at next refresh if Eson discloses an AI customer. |
| TSE:4369 (Tri Chemical Laboratories) | High-K precursor leader, but the primary growth vector is HBM dielectric and ALD precursors — sits more cleanly in the `memory-upcycle` theme than in the packaging-passives basket. Re-evaluate if TCL discloses a packaging-specific SKU ([Omega Investment TCL price discovery, 2025-08](https://omega-inv.com/2025/08/18/4369pd/)). |
| TSE:4063 (Shin-Etsu Chemical) / TSE:3436 (SUMCO) / NASDAQ:ENTG (Entegris) | Silicon wafer + general semi materials — sit upstream of packaging passives and overlap with the broader semi-cap supply chain (separate `semi-cycle` theme). Not specific to the AI-server BOM stack tracked here. |
| NASDAQ:AMAT / NASDAQ:LRCX | Semi capex equipment — enable the foundry, not the package. Out of scope per Scope rules. |
| Private: Powerchip Technology (PSMC subsidiary 力晶), Bota / FUTEK / various unlisted | Not investable; surfaced in Watch list. |

## Keywords

MLCC / 多层陶瓷电容器 · ABF substrate / 安美特ビルドアップフィルム · 玻璃基板 / glass substrate · 高速覆铜板 / high-speed CCL · M6 / M7 / M10 ultra-low-loss · mSAP / modified semi-additive process · FC-BGA / flip-chip ball-grid-array · advanced packaging / 先进封装 · photomask / 光罩 · EUV mask blanks · AI server BOM · CoWoS-L · CoPoS / FOPLP

## Performance (as of 2026-05-31, since-inception snapshot)

Returns are simple price returns from yfinance with `auto_adjust=True`, computed against the 2026-05-29 close (most recent print before 2026-05-31 anchor). The basket is multi-market; benchmarks reported separately by geography rather than blended.

**Equal-weight basket returns:** 3-month +92.6% · YTD 2026 +174.5% · trailing 1-year +426.0%.

**Median ticker returns:** 1Y +370.6% (i.e. the basket mean is *not* dragged by a single outlier — the dispersion is uniformly extreme across the ABF and PCB sub-buckets).

**Benchmark returns over the same windows (anchored 2026-05-29 close):**

| Benchmark | 3M | YTD 2026 | 1Y |
|---|---|---|---|
| S&P 500 (SPY) | +10.6% | +11.0% | +29.7% |
| CSI 300 (510300.SS) | +4.2% | +4.3% | +30.2% |
| Nikkei 225 (^N225) | +12.7% | +28.0% | +72.6% |
| iShares Japan (EWJ) | +0.6% | +14.3% | +31.3% |

**Per-ticker performance, sorted by 1-year return:**

| Ticker | 1Y | YTD | 3M | Close (local) |
|---|---|---|---|---|
| TWSE:3037 (Unimicron) | +907.5% | +381.7% | +119.1% | 1,055.00 |
| TWSE:3189 (Kinsus) | +802.7% | +367.3% | +131.8% | 729.00 |
| TWSE:8046 (Nan Ya PCB) | +714.8% | +257.8% | +52.8% | 848.00 |
| WBAG:ATS (AT&S) | +704.8% | +329.9% | +174.9% | 141.00 |
| TSE:4062 (Ibiden) | +677.2% | +221.9% | +141.6% | 23,000 |
| TWSE:2327 (Yageo) | +528.2% | +206.2% | +147.7% | 738.00 |
| SSE:600183 (Shengyi) | +429.6% | +92.0% | +103.5% | 140.62 |
| TWSE:2492 (Walsin) | +396.5% | +216.5% | +152.6% | 394.00 |
| SZSE:002916 (Shennan) | +386.8% | +70.7% | +45.0% | 411.41 |
| TSE:6981 (Murata) | +354.4% | +191.8% | +136.5% | 9,625 |
| SZSE:002463 (WUS) | +324.8% | +74.7% | +58.7% | 132.04 |
| SZSE:300408 (Sanhuan) | +301.0% | +177.6% | +105.2% | 128.78 |
| SZSE:000636 (Fenghua) | +299.5% | +213.8% | +104.0% | 53.03 |
| SZSE:002938 (Avary) | +281.8% | +102.5% | +78.0% | 105.01 |
| NYSE:GLW (Corning) | +268.6% | +100.5% | +20.7% | 181.16 |
| TSE:6762 (TDK) | +160.8% | +84.3% | +71.1% | 4,108 |
| NASDAQ:PLAB (Photronics) | +85.6% | −3.2% | −13.6% | 32.35 |
| TSE:2802 (Ajinomoto) | +43.1% | +55.8% | +4.3% | 5,152 |

**Read of the dispersion:** The basket is *uniformly* deep in positive territory — every name except Photronics is YTD-positive. The Taiwan ABF triumvirate (Unimicron / Nan Ya PCB / Kinsus) and AT&S sit at the top as the cleanest FC-BGA shortage pure-plays. The Chinese AI-PCB names (WUS, Shennan, Avary, Shengyi) sit one rung below, reflecting US-export-control overhang. The Japanese names diverge: Ibiden screens like a Taiwan substrate (+677% 1Y, FC-BGA monopoly = CoWoS proxy); Murata + TDK are MLCC-pricing proxies (+354% / +161%); Ajinomoto's +43% 1Y is the slowest because resin pricing has not flowed through — only to substrate-customer margins. **Interpretation: this is a fully priced trade.** Mean reversion is now a more credible 6–12-month risk than further multiple expansion for the substrate triumvirate at +700–900% 1Y; the Chinese A-share names trade at notably less stretched multiples and may carry the basket if Asian substrate names cool.

## Recent events (since basket inception)

This is the inception write; "recent events" here covers the prior ~90 days of catalyst flow that informed ticker selection. Future refreshes will cover the window since the previous `Last refreshed` date.

- **Murata 2026-03-17 price-hike announcement:** 15–35% price increase on AI-server high-capacitance MLCCs effective April 1 2026 — the single most consequential pricing signal in the basket since Apple-cycle MLCC prints; triggered the Yageo / Walsin / Sanhuan / Fenghua follow-ons ([Astute Group, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/)).
- **NVIDIA-WUS M10 CCL joint test (Q1 2026):** Ming-Chi Kuo confirmed NVIDIA-WUS joint M10-grade CCL development with 52-layer PCB targeted for Q4 2026 – Q1 2027 mass production on Rubin ([IT之家, 2026](https://www.ithome.com/0/928/995.htm)).
- **AT&S 2026-05-20 Chongqing expansion:** AI IC-substrate capacity fully financed by long-term customer agreements, guided high double-digit million EBIT FY26/27 ([AT&S IR news, 2026](https://ats.net/en/ir-news/ats-expands-capacity-for-ai-substrates/)).
- **Ajinomoto FY26 results (2026-05):** record business profit ¥181.1B (+13.7% YoY); Functional Materials guided to double-digit FY26 growth ([BigGo Finance / TDnet IR, 2026-05](https://finance.biggo.com/news/jpx_tdnet_140120260501516433)).
- **NVIDIA-Corning multi-year partnership (May 2026):** optical-connectivity partnership for next-gen AI infrastructure — the most visible commercial signal in Corning's pivot toward AI revenue ([FinancialContent Corning AI architect, 2026-03-25](https://www.financialcontent.com/article/finterra-2026-3-25-corning-inc-nyse-glw-the-material-architect-of-the-ai-and-broadband-era)).
- **Sanhuan / Fenghua A-share MLCC rally (week of 2026-05-26):** Fenghua +>50% in one week, Sanhuan +>30% on confirmed 0805 476 high-cap MLCC batch shipments to Inspur / Huawei AI servers ([Sina Finance MLCC 5月推荐榜, 2026-05-26](https://finance.sina.cn/stock/jdts/2026-05-26/detail-inhzffss1517949.d.html)).
- **Photronics Q2 FY26 miss (2026-05-29):** revenue $209.9M vs $221M consensus — the basket's first material disappointment, attributed to delayed photomask design releases ([Photronics Q2 FY26 8-K, 2026](https://www.sec.gov/Archives/edgar/data/0000810136/000114036126023057/ef20074970_ex99-1.htm)).
- **Shengyi Q1 2026 print:** revenue ¥8.14B (+45% YoY) / NP ¥1.16B (+105.5%) confirming AI-driven CCL pricing power flowed through ([Futunn, 2026](https://news.futunn.com/post/72564670/shengyi-technology-600183-sh-2025-annual-report-and-q1-2026)).
- **Shinko Electric delisting completion (effective 2025-06-06):** JIC tender at ¥5,920 → cash settlement Aug 29 2025; substrate franchise persists as a JIC consortium asset, no longer a listed equity ([Shinko delisting notice, 2025-06-05](https://www.shinko.co.jp/english/news/docs/20250605-01_en.pdf)).

## Drift signals

This is the inception write — drift detection becomes the value-add starting from the *next* refresh. Initial flags for next month's pass:

- **Taiwan ABF triumvirate is the basket's largest concentration risk.** Unimicron + Nan Ya PCB + Kinsus together averaging +808% 1Y is a uniquely lopsided print; even one missed quarter from any of the three would compress the basket median materially. Watch 2H26 ABF substrate ASP guidance and any signal of new Korean / Chinese substrate capacity that could relieve the squeeze faster than the Digitimes mid-to-late 2026 expectation ([Digitimes ABF crunch, 2026-01-30](https://www.digitimes.com/news/a20260130PD220/unimicron-abf-substrate-ai-server-market-capacity.html)).
- **Glass substrate timing risk.** Corning's +269% and AT&S's +705% price in glass-substrate commercialization that Intel and TSMC target for 2027–2030. If Intel slips 18A-glass or TSMC defers CoPoS, these multiples are the most exposed in the basket.
- **Chinese A-share underperformance gap vs Taiwan.** WUS (+325%), Shennan (+387%), Avary (+282%), Shengyi (+430%), Sanhuan (+301%), Fenghua (+300%) — every Chinese name sits below the Taiwan median of +708%, despite arguably stronger 1Q26 prints. The gap reflects US-export-control overhang + A-share liquidity discount. The WUS-NVIDIA M10 mass-production milestone in Q4 2026 – Q1 2027 is the binary near-term catalyst.
- **Photronics is the basket's outlier downside.** PLAB Q2 FY26 missed on delayed design releases — if the delay extends a second quarter, the photomask thesis loses both time-to-revenue and multiple. Re-evaluate after Q3 FY26.
- **Single-modality risk in MLCC pricing.** The Murata-led 15–35% April 2026 price hike is the single biggest pillar under MLCC names' multiples. Inventory normalization signs in the Apple / Samsung handset cycle would unwind a portion of Yageo / Walsin / Sanhuan / Fenghua's gains.
- **Ajinomoto's +43% 1Y is the basket's slowest performer.** As the *resin* monopolist (not substrate fabricator), substrate margins expand before Ajinomoto's resin pricing flows through. If Ajinomoto starts pushing resin price hikes through in FY27 ([Digital Citizen, 2025-12](https://www.digitalcitizen.life/ajinomoto-may-raise-abf-film-prices-as-ai-server-demand-tightens-supply/)), the relative multiple should re-rate.
- **Watch list (public — not added at inception):** TWSE:6669 Wiwynn (AI-server ODM — separate `ai-server-ODM` theme); TSE:6976 Taiyo Yuden (Japanese MLCC #4, already covered by Murata + TDK); SZSE:300588 景旺電子 (Chinese mid-cap PCB / FPC with mSAP capacity); TWSE:8112 Supreme Electronics (CCL alternative). Re-evaluate next refresh if any disclose a specific AI-server SKU.
- **Watch list (private — surface for IPO):** Powerchip Technology (PSMC subsidiary 力晶), unlisted Korean / Chinese substrate fabricators rumored to be considering 2026–2027 listings. Any IPO is an immediate mutation candidate.

## Catalysts (next 3–6 months)

- **Ibiden + Unimicron + Kinsus quarterly substrate guidance (Jul–Aug 2026):** cleanest read on whether ABF ASP guidance is raised again into 2H26.
- **NVIDIA-WUS M10 CCL mass-production milestone (Q4 2026 – Q1 2027):** binary on whether the 52-layer Rubin PCB ramps on schedule — the most consequential event for the Chinese AI-PCB sub-bucket.
- **Murata FY26 Q1 + Ajinomoto Q1 FY27 (early-Aug 2026):** first quarter under the new MLCC pricing schedule; first read on whether ABF resin pricing is passing through to substrate customers in FY27.
- **Yageo + Walsin Q2 2026 results (Aug–Sep 2026):** Taiwan MLCC pricing-mix readouts and any sign of automotive demand aligning with AI-server build.
- **Photronics Q3 FY26 (Aug 2026):** binary on whether design-release delays were one-quarter noise or a multi-quarter pattern.
- **Intel 18A-glass commercial bring-up signal (any time 2H26):** binary catalyst for Corning's multiple; an Intel Foundry technology-day disclosure could confirm or defer.
- **NVIDIA GTC 2026 (Oct 2026 expected):** Rubin-class accelerator details + supplier callouts; an explicit supplier name for the M10 CCL or FC-BGA substrate is basket-moving.

## Data Used / 数据来源清单

**Market data**
- yfinance `auto_adjust=True` for prices, returns, market cap, sector — pulled 2026-05-31 (most recent close 2026-05-29 across all markets).
- Benchmarks: SPY (S&P 500), 510300.SS (CSI 300 ETF), ^N225 (Nikkei 225), EWJ (iShares MSCI Japan).
- 1306.T (Topix ETF) returned distorted yfinance data (suspected ex-distribution adjustment artifact) and was excluded as benchmark in favor of ^N225 + EWJ.

**Per-ticker primary / industry sources** — every ticker's source URLs are cited inline in the Tracked tickers Justification cell and in Recent events; consolidated in the References block at end of file. No duplication here.

**Industry research (theme-level)**
- [zsxq 415284451152288] **PCB行业深度跟踪报告：AI高速升级需求催生mSAP新趋势 (p41)** — flagship Chinese broker on mSAP technology and AI-PCB supplier maps; used for SZSE PCB ticker selection and the M-series CCL roadmap framing.
- [zsxq 415284451221118] **玻璃基板行业专题研究：后摩尔时代封装革命，玻璃基板迎产业化元年 (p25)** — used for Corning + AT&S glass-substrate framing and the 2027–2030 commercialization timeline.
- [zsxq 415284542842188] **GS Murata 6981.T CEO meeting AI MLCC Buy CL (p7)** — used for Murata thesis anchoring.
- [zsxq 585412242541114] **JPM 电子元器件行业：MLCC 动态 — 2026年4月进出口数据 (p16)** — used for Japanese MLCC export-channel data points referenced in MLCC price-hike commentary.
- [zsxq 585412242541244] **Citi 日本电子元器件 — 2026年4月MLCC数据 (p10)** — used for cross-broker MLCC-pricing confirmation.
- [zsxq 812485541485212] **JPM 味之素 2802.T — ABF载板 + CDMO 驱动增长 (p14)** — used for Ajinomoto FY26 ABF + CDMO breakdown.
- [zsxq 184152212415522] **GS 凸版印刷 / 大日本印刷 业绩更新 (p18)** — used for Toppan / DNP photomask landscape framing supporting the Photronics inclusion and Toppan / DNP exclusion decisions.
- [zsxq 812485814114222] **Jefferies 中国科技 — 苹果供应链潜在采用 COB 技术** — used for Apple-supply-chain context on Avary / WUS.
- [zsxq 212485814114481] **MS 日本电子元器件 — HDD/SSD 数据印证 DC 需求** — used for AI-DC demand corroboration.
- [zsxq 184152248118842] **金刚石——声光电热终极材料 (p34)** — read but de-scoped; diamond materials are a separate `advanced-materials-thermal` theme rather than packaging passives.
- [zsxq 184152581881582] **GS Tri Chemical Laboratories 4369.T 1QFY27 (p7)** — used for the TCL exclusion decision (HBM precursor angle rather than packaging passive).
- [zsxq 415284424528848] **GS 日本工业电子 — 4月光纤/光缆贸易数据，古河电气三重县新厂** — read for optical-connectivity context (relevant to Corning-NVIDIA partnership framing).

**Macro backdrop (as of 2026-05-25 latest, from `db/indicators.db` snapshot id 5)**
- VIX: 16.68 (low-vol regime — high-multiple Asian substrate / MLCC names trade well here).
- 10Y Treasury (TNX): 4.56% (2026-05-25) — still elevated; would compress multiples in a re-tightening scenario.
- HYG (high-yield credit ETF): 79.91 (2026-05-25) — risk-on credit backdrop supporting growth-multiple names.
- DXY: 98.99 (2026-05-25, USD soft) — supports non-US basket components (Taiwan / Japan / Austria) on FX translation, partially offsetting price beta.
- 3M T-bill: 3.59% — short rates eased modestly into the print, modestly supportive of duration assets.

**Stale notices / coverage gaps**
- TSE:6967 Shinko Electric pricing referenced via the JPX delisting notice as of Jun 2025; no further price data possible (delisted).
- No in-house company-research file for any basket name except those flagged in cross-coverage; deep-dive prioritization for next refresh: Ibiden 4062.T (largest single-substrate beta), Yageo 2327.TW (Taiwan MLCC prime), Shengyi 600183.SS (China high-end CCL prime).
- Murata and TDK MLCC AI-server revenue is not separately disclosed; their inclusion rests on platform-level ASP guidance and broker-tracked MLCC pricing, not a booked AI-server revenue segment.
- Glass substrate revenue at Corning is bundled into the Display + Specialty Materials segment; no AI-glass-substrate revenue line was disclosed in the most recent 10-Q. Re-evaluate after the next Corning analyst day for any glass-core revenue split disclosure.
- AT&S FY26/27 EBIT impact from the Chongqing expansion is guided as "high double-digit million EUR" with no specific decimal; refresh when AT&S reports H1 26/27 results (Nov 2026).

**Cross-coverage (existing in-house company research read as structured input, not cited inline)**
- [reports/themes/humanoid-robotics-sensors_theme.md](humanoid-robotics-sensors_theme.md) — Murata + TDK overlap; the IMU / sensor thesis vs the MLCC / AI-server thesis are tracked as independent and additive.

## References

(Key inline citations consolidated for quick scanning. All URLs above are reachable in the inline link text.)

- [Astute Group MLCC shortages AI demand, 2026](https://www.astutegroup.com/news/general/mlcc-shortages-return-as-ai-server-demand-strains-capacity/) — Murata 15–35% price hike Apr 2026
- [TrendForce Murata AI power module, 2025-12](https://www.trendforce.com/news/2025/12/17/news-murata-reportedly-to-mass-produce-ai-server-power-modules-in-2026-targets-%C2%A550b-by-fy27) — ¥50B FY27 target
- [TradingKey ABF Ajinomoto Nvidia, 2026](https://www.tradingkey.com/analysis/stocks/us-stocks/261783966-abf-ajinomoto-nvidia-ai-supply-chain-tradingkey) — ABF shortfall 2H26-2028
- [Digitimes ABF sells out (Unimicron/Kinsus/NanYa), 2026-04-20](https://www.digitimes.com/news/a20260420PD216/revenue-pcb-abf-substrate-unimicron-ai-chip.html)
- [Digitimes Unimicron 2026 revenue record, 2026-05-29](https://www.digitimes.com/news/a20260529PD239/unimicron-revenue-2026-demand-substrate.html)
- [Bloomberg Ibiden expansion, 2024-12](https://www.bloomberg.com/news/articles/2024-12-29/nvidia-supplier-ibiden-weighs-faster-expansion-to-meet-ai-demand)
- [IT之家 NVIDIA-WUS M10 CCL test, 2026](https://www.ithome.com/0/928/995.htm) — Rubin 52-layer
- [WallStreetCN WUS 沪电 1Q26 +54%, 2026](https://wallstreetcn.com/articles/3770620)
- [futunn 生益 600183 1Q26, 2026](https://news.futunn.com/post/72564670/shengyi-technology-600183-sh-2025-annual-report-and-q1-2026)
- [东方财富 鹏鼎AI觉醒, 2026-05-24](https://caifuhao.eastmoney.com/news/20260524235130296585900)
- [BigGo Finance Ajinomoto FY26 IR, 2026-05](https://finance.biggo.com/news/jpx_tdnet_140120260501516433) — ¥181.1B BP
- [evertiq AT&S Chongqing AI expansion, 2026-05-26](https://evertiq.com/news/2026-05-26-ats-expands-ai-substrate-capacity-in-chongqing)
- [Wccftech glass substrate three-year timeline, 2026](https://wccftech.com/intel-backed-glass-substrates-tech-will-be-commercilization-ready-within-three-years/)
- [Photronics Q2 FY26 8-K, 2026](https://www.sec.gov/Archives/edgar/data/0000810136/000114036126023057/ef20074970_ex99-1.htm)
- [JPX Decision on Delisting Shinko Electric, 2025-05-20](https://www.jpx.co.jp/english/news/1023/20250520-11.html)
- [Sina Finance MLCC 5月推荐榜, 2026-05-26](https://finance.sina.cn/stock/jdts/2026-05-26/detail-inhzffss1517949.d.html)
- [Corning Advanced Packaging Carriers, 2025](https://www.corning.com/worldwide/en/products/advanced-optics/product-materials/PrecisionGlassSolutions/advanced-packaging-carriers-release.html)
- [FinancialContent Corning AI material architect, 2026-03-25](https://www.financialcontent.com/article/finterra-2026-3-25-corning-inc-nyse-glw-the-material-architect-of-the-ai-and-broadband-era)
- [Digital Citizen Ajinomoto ABF film price rise, 2025-12](https://www.digitalcitizen.life/ajinomoto-may-raise-abf-film-prices-as-ai-server-demand-tightens-supply/)
- [Digitimes Yageo 1Q26 AI orders, 2026-02-26](https://www.digitimes.com/news/a20260226PD231/yageo-passive-components-demand-revenue-2026.html)

## History

- 2026-05-31 — theme created with 18-ticker basket (9 core, 5 enabler, 4 adjacent) following user request "Build a tracked-theme basket for AI Infrastructure Passives & Advanced Packaging"; initial Performance / Recent events / Drift signals populated. Murata (6981.T) and TDK (6762.T) cross-listed with the [humanoid-robotics-sensors basket](humanoid-robotics-sensors_theme.md) under independent (MLCC) vs (IMU) theses. Shinko Electric (6967.T) excluded post-Jun 2025 delisting. DNP (7912.T) and Toppan (7911.T) excluded after weighing Photronics' cleaner photomask exposure. TWSE:4961, TSE:4369, TSE:4063, TSE:3436, NASDAQ:ENTG, NASDAQ:AMAT, NASDAQ:LRCX excluded per scope rules.
