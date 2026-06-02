"""Populate ``stock_price_target.db`` from the 100-zsxq-report sweep on 2026-06-02.

Pulls report_date from zsxq.db (create_time, which is when the PDF was
downloaded and indexed) and historical close + share count from yfinance
for the same date so each row carries point-in-time price + market cap.

Idempotent — re-running is a no-op on already-inserted (ticker, broker,
file_id) triples thanks to the UNIQUE index.
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yfinance as yf

from db_paths import db_path
from stock_price_target_db import upsert_target, count


# ---------------------------------------------------------------------------
# Records — extracted by hand from the 100-report zsxq sweep on 2026-06-02.
# Each tuple: (yf_ticker_for_price_lookup, payload_dict)
# yf_ticker is what we feed yfinance; ticker in payload is the human-facing
# form (e.g. "1109.HK", "300750.SZ", "LLY").
# ---------------------------------------------------------------------------
RECORDS = [
    # ============= US =============
    ("LRCX", dict(
        company_ticker="LRCX", exchange="NASDAQ",
        company_name="Lam Research", chinese_name="泛林集团",
        research_institute="Bernstein", rating="Outperform",
        price_target=340.0, target_currency="USD",
        catalyst="2026 WFE $140bn guide intact + GAA/HBM/NAND upgrades drive equipment intensity",
        report_file_id=415284282581258,
    )),
    ("AMAT", dict(
        company_ticker="AMAT", exchange="NASDAQ",
        company_name="Applied Materials", chinese_name="应用材料",
        research_institute="Bernstein", rating="Outperform",
        price_target=525.0, target_currency="USD",
        catalyst="Advanced logic / DRAM / advanced packaging = ~80% of 2026 equipment increment",
        report_file_id=415284282581258,
    )),
    ("QCOM", dict(
        company_ticker="QCOM", exchange="NASDAQ",
        company_name="Qualcomm", chinese_name="高通",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=140.0, target_currency="USD",
        catalyst="Memory supply constraint hits handset Q3; data center to add billions FY27",
        report_file_id=415284282581258,
    )),
    ("TXN", dict(
        company_ticker="TXN", exchange="NASDAQ",
        company_name="Texas Instruments", chinese_name="德州仪器",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=250.0, target_currency="USD",
        catalyst="Data center +90% YoY in Q1; 5-year capex cycle nearing end",
        report_file_id=415284282581258,
    )),
    ("MSFT", dict(
        company_ticker="MSFT", exchange="NASDAQ",
        company_name="Microsoft", chinese_name="微软",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=650.0, target_currency="USD",
        catalyst="Surface Laptop Ultra with NVIDIA RTX Spark; 1200B-param local inference",
        report_file_id=212485484285211,
    )),
    ("ARM", dict(
        company_ticker="ARM", exchange="NASDAQ",
        company_name="Arm Holdings", chinese_name="安谋控股",
        research_institute="Morgan Stanley", rating="Equal-Weight",
        price_target=202.0, target_currency="USD",
        catalyst="NVIDIA enters Arm Windows PC; agentic edge compute royalty tailwind",
        report_file_id=212485484285841,
    )),
    ("DELL", dict(
        company_ticker="DELL", exchange="NYSE",
        company_name="Dell Technologies", chinese_name="戴尔",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=500.0, target_currency="USD",
        catalyst="F1Q27: rev $43.8B vs $36.2B est; AI server backlog $51.3B; FY27 AI server $60B",
        report_file_id=585412414512154,
    )),
    ("DELL", dict(
        company_ticker="DELL", exchange="NYSE",
        company_name="Dell Technologies", chinese_name="戴尔",
        research_institute="Morgan Stanley", rating="Equal-Weight",
        price_target=448.0, target_currency="USD",
        catalyst="Upgrade from UW; supply-chain execution + AI server market share gains",
        report_file_id=415284512252488,
    )),
    ("HPE", dict(
        company_ticker="HPE", exchange="NYSE",
        company_name="Hewlett Packard Enterprise",
        research_institute="Morgan Stanley", rating="Equal-Weight",
        price_target=33.0, target_currency="USD",
        catalyst="Taiwan supply-chain channel checks; AI server competitive position vs DELL",
        report_file_id=415284512252288,
    )),
    ("HPQ", dict(
        company_ticker="HPQ", exchange="NYSE",
        company_name="HP Inc.",
        research_institute="Morgan Stanley", rating="Underweight",
        price_target=19.0, target_currency="USD",
        catalyst="Share loss + memory cost margin squeeze; FY27 EPS 7x",
        report_file_id=415284512252288,
    )),
    ("AAPL", dict(
        company_ticker="AAPL", exchange="NASDAQ",
        company_name="Apple", chinese_name="苹果",
        research_institute="Morgan Stanley", rating="Equal-Weight",
        price_target=330.0, target_currency="USD",
        catalyst="WWDC 2026 — scenario 1 (30% prob): incremental updates without substantive agentic progress",
        report_file_id=585412584454214,
    )),
    ("AVGO", dict(
        company_ticker="AVGO", exchange="NASDAQ",
        company_name="Broadcom", chinese_name="博通",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=485.0, target_currency="USD",
        catalyst="AI networking + custom ASIC long-term growth; raised from $470, Q3 earnings 6/5",
        report_file_id=585412584454154,
    )),
    ("AMD", dict(
        company_ticker="AMD", exchange="NASDAQ",
        company_name="Advanced Micro Devices",
        research_institute="Morgan Stanley", rating=None,
        price_target=360.0, target_currency="USD",
        catalyst="DC GPU share gains; ~37x FY27 EPS $11.10",
        report_file_id=212485214424151,
    )),
    ("FUTU", dict(
        company_ticker="FUTU", exchange="NASDAQ",
        company_name="Futu Holdings", chinese_name="富途控股",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=177.0, target_currency="USD",
        catalyst="Down from $225 — China onshore exits 2H26 but HK + overseas growth intact",
        report_file_id=812485484288452,
    )),
    ("COST", dict(
        company_ticker="COST", exchange="NASDAQ",
        company_name="Costco", chinese_name="好市多",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=1159.0, target_currency="USD",
        catalyst="CFO meeting — proactive price cuts, ~4000 SKUs, AI personalization 3x conv",
        report_file_id=212485484288281,
    )),
    ("CHA", dict(
        company_ticker="CHA", exchange="NASDAQ",
        company_name="Chagee", chinese_name="霸王茶姬",
        research_institute="Deutsche Bank", rating="Buy",
        price_target=19.70, target_currency="USD",
        catalyst="Q1 beat + $150M buyback; 2026 NDR +4% on margin upside",
        report_file_id=812485484285842,
    )),
    ("V", dict(
        company_ticker="V", exchange="NYSE",
        company_name="Visa",
        research_institute="Bernstein", rating="Outperform",
        price_target=450.0, target_currency="USD",
        catalyst="Agentic commerce + stablecoin Visa cards (+200% YoY); VAS 30% of revenue +27% YoY",
        report_file_id=415284282584848,
    )),
    ("CVS", dict(
        company_ticker="CVS", exchange="NYSE",
        company_name="CVS Health",
        research_institute="J.P. Morgan", rating="Overweight",
        price_target=None, target_currency="USD",
        catalyst="CostVantage reimbursement model rolled out; PCW segment margin stabilizing",
        report_file_id=812485484285522,
    )),
    ("LLY", dict(
        company_ticker="LLY", exchange="NYSE",
        company_name="Eli Lilly",
        research_institute="Bernstein", rating="Outperform",
        price_target=1300.0, target_currency="USD",
        catalyst="LIBRETTO-432 Selpercatinib RET+ adjuvant NSCLC HR=0.17; oral GLP-1 (Orforglipron)",
        report_file_id=184152151455852,
    )),
    ("GILD", dict(
        company_ticker="GILD", exchange="NASDAQ",
        company_name="Gilead Sciences",
        research_institute="Bernstein", rating="Outperform",
        price_target=160.0, target_currency="USD",
        catalyst="ASCO 2026 KOL coverage — HIV PrEP + Trodelvy TROP2-ADC",
        report_file_id=184152151455852,
    )),
    ("NUVL", dict(
        company_ticker="NUVL", exchange="NASDAQ",
        company_name="Nuvalent",
        research_institute="Bernstein", rating="Outperform",
        price_target=189.0, target_currency="USD",
        catalyst="4th-gen ALK inhibitor for lorlatinib-resistant patients; ORR ~26%",
        report_file_id=184152151455852,
    )),
    ("ABBV", dict(
        company_ticker="ABBV", exchange="NYSE",
        company_name="AbbVie",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=225.0, target_currency="USD",
        catalyst="ASCO 2026 KOL coverage; Humira biosimilar landscape, Rinvoq/Skyrizi growth",
        report_file_id=184152151455852,
    )),
    ("AMGN", dict(
        company_ticker="AMGN", exchange="NASDAQ",
        company_name="Amgen",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=335.0, target_currency="USD",
        catalyst="ASCO 2026 KOL coverage; MariTide GLP-1/GIPR antagonist",
        report_file_id=184152151455852,
    )),
    ("BMY", dict(
        company_ticker="BMY", exchange="NYSE",
        company_name="Bristol-Myers Squibb",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=58.0, target_currency="USD",
        catalyst="ASCO 2026 KOL coverage",
        report_file_id=184152151455852,
    )),
    ("MRK", dict(
        company_ticker="MRK", exchange="NYSE",
        company_name="Merck",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=100.0, target_currency="USD",
        catalyst="ASCO 2026 — Keytruda dominance + Sac-TMT combo",
        report_file_id=184152151455852,
    )),
    ("PFE", dict(
        company_ticker="PFE", exchange="NYSE",
        company_name="Pfizer",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=30.0, target_currency="USD",
        catalyst="ASCO 2026 — Lorlatinib CROWN 7-yr; ALK franchise",
        report_file_id=184152151455852,
    )),
    ("MRNA", dict(
        company_ticker="MRNA", exchange="NASDAQ",
        company_name="Moderna",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=45.0, target_currency="USD",
        catalyst="ASCO 2026 — mRNA-4157 individualized neoantigen + Keytruda",
        report_file_id=184152151455852,
    )),
    ("BNTX", dict(
        company_ticker="BNTX", exchange="NASDAQ",
        company_name="BioNTech",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=96.0, target_currency="USD",
        catalyst="ASCO 2026 — oncology transition, HER2-ADC, mRNA cancer vaccines",
        report_file_id=184152151455852,
    )),
    ("TSLA", dict(
        company_ticker="TSLA", exchange="NASDAQ",
        company_name="Tesla",
        research_institute="Goldman Sachs", rating="Neutral",
        price_target=None, target_currency="USD",
        catalyst="Robotaxi tracker — Austin ~100-120k miles/incident; FSD v15 expected YE",
        report_file_id=415284282585428,
    )),
    ("RIVN", dict(
        company_ticker="RIVN", exchange="NASDAQ",
        company_name="Rivian",
        research_institute="Goldman Sachs", rating="Neutral",
        price_target=None, target_currency="USD",
        catalyst="Uber R2 robotaxi deal — 50k units, $1.25B; L4 by 2028",
        report_file_id=415284282585428,
    )),
    ("MBLY", dict(
        company_ticker="MBLY", exchange="NASDAQ",
        company_name="Mobileye",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=None, target_currency="USD",
        catalyst="VW MOIA × Uber LA driverless target YE; ADAS attach growing",
        report_file_id=415284282585428,
    )),
    ("PONY", dict(
        company_ticker="PONY", exchange="NASDAQ",
        company_name="Pony AI", chinese_name="小马智行",
        research_institute="UBS", rating="Buy",
        price_target=20.0, target_currency="USD",
        catalyst="Joint deployment model + 27万元 hardware cost target — UE breakeven Tier-1",
        report_file_id=585412414512514,
    )),
    ("NIO", dict(
        company_ticker="NIO", exchange="NYSE",
        company_name="NIO", chinese_name="蔚来",
        research_institute="Nomura", rating="Buy",
        price_target=8.60, target_currency="USD",
        catalyst="May 37.7k deliveries +62% YoY; ES9 orders strong; 2Q26 guide 11-11.5k achievable",
        report_file_id=415284241285558,
    )),
    ("XPEV", dict(
        company_ticker="XPEV", exchange="NYSE",
        company_name="Xpeng", chinese_name="小鹏",
        research_institute="Nomura", rating="Buy",
        price_target=23.0, target_currency="USD",
        catalyst="MONA/G series demand strong; 2Q26 guide 10-10.6k achievable",
        report_file_id=415284241285558,
    )),
    ("XPEV", dict(
        company_ticker="XPEV", exchange="NYSE",
        company_name="Xpeng", chinese_name="小鹏",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=23.0, target_currency="USD",
        catalyst="New model cycle starting — growth acceleration imminent",
        report_file_id=184152481141242,
    )),
    ("LI", dict(
        company_ticker="LI", exchange="NASDAQ",
        company_name="Li Auto", chinese_name="理想",
        research_institute="Nomura", rating="Neutral",
        price_target=20.0, target_currency="USD",
        catalyst="May 33.4k deliveries -18% YoY; new L8 catalyst pending",
        report_file_id=415284241285558,
    )),
    ("SLB", dict(
        company_ticker="SLB", exchange="NYSE",
        company_name="Schlumberger",
        research_institute="Morgan Stanley", rating="Top Pick",
        price_target=None, target_currency="USD",
        catalyst="Offshore drilling upcycle — 2030 deep-water demand +17%, day rates +15-20%",
        report_file_id=585412414515514,
    )),
    ("HAL", dict(
        company_ticker="HAL", exchange="NYSE",
        company_name="Halliburton",
        research_institute="Morgan Stanley", rating="Top Pick",
        price_target=None, target_currency="USD",
        catalyst="Offshore drilling upcycle co-pick with SLB",
        report_file_id=585412414515514,
    )),
    ("RIG", dict(
        company_ticker="RIG", exchange="NYSE",
        company_name="Transocean",
        research_institute="Morgan Stanley", rating="Buy",
        price_target=None, target_currency="USD",
        catalyst="Pure-play offshore driller; PT upside 13%, long-short ratio 1.7x",
        report_file_id=585412414515514,
    )),

    # ============= HK / China =============
    ("1211.HK", dict(
        company_ticker="1211.HK", exchange="HKEX",
        company_name="BYD", chinese_name="比亚迪",
        research_institute="Nomura", rating="Buy",
        price_target=127.0, target_currency="HKD",
        catalyst="May 377k +80% YoY overseas; 4nm self-developed ADAS chip launched",
        report_file_id=415284241285558,
    )),
    ("3690.HK", dict(
        company_ticker="3690.HK", exchange="HKEX",
        company_name="Meituan", chinese_name="美团",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=116.0, target_currency="HKD",
        catalyst="1Q26 FD UE beat; long-term per-order profit assumption raised from 0.7 to 1.0 RMB",
        report_file_id=812485451482542,
    )),
    ("3690.HK", dict(
        company_ticker="3690.HK", exchange="HKEX",
        company_name="Meituan", chinese_name="美团",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=85.0, target_currency="HKD",
        catalyst="1Q26 — food delivery returns to breakeven; Ali competition modulating",
        report_file_id=212485451482841,
    )),
    ("3690.HK", dict(
        company_ticker="3690.HK", exchange="HKEX",
        company_name="Meituan", chinese_name="美团",
        research_institute="Nomura", rating="Neutral",
        price_target=92.0, target_currency="HKD",
        catalyst="FD UE improves to -0.94 RMB/order; March slightly profitable",
        report_file_id=585412428415114,
    )),
    ("2269.HK", dict(
        company_ticker="2269.HK", exchange="HKEX",
        company_name="WuXi Biologics", chinese_name="药明生物",
        research_institute="Goldman Sachs", rating="Neutral",
        price_target=41.0, target_currency="HKD",
        catalyst="3-year revenue CAGR ~20% reiterated; +30 new China D&M capex RMB",
        report_file_id=415284241285888,
    )),
    ("2269.HK", dict(
        company_ticker="2269.HK", exchange="HKEX",
        company_name="WuXi Biologics", chinese_name="药明生物",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=50.0, target_currency="HKD",
        catalyst="2026 YTD business drivers update — strong project momentum",
        report_file_id=585412584454244,
    )),
    ("9926.HK", dict(
        company_ticker="9926.HK", exchange="HKEX",
        company_name="Akeso", chinese_name="康方生物",
        research_institute="J.P. Morgan", rating="Overweight",
        price_target=162.0, target_currency="HKD",
        catalyst="HARMONi-6 OS HR=0.66 — first PD-1×VEGF OS win in squamous NSCLC",
        report_file_id=212485214424541,
    )),
    ("2616.HK", dict(
        company_ticker="2616.HK", exchange="HKEX",
        company_name="CStone Pharmaceuticals", chinese_name="基石药业",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=9.44, target_currency="HKD",
        catalyst="CS2009 PD-1/VEGF/CTLA-4 tri-specific; 81% ORR in 1L PD-L1+ NSCLC; Ph3 by YE26",
        report_file_id=812485454485222,
    )),
    ("1801.HK", dict(
        company_ticker="1801.HK", exchange="HKEX",
        company_name="Innovent Biologics", chinese_name="信达生物",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=107.04, target_currency="HKD",
        catalyst="IBI3032 oral GLP-1 SAD/MAD Ph1 data at ADA 2026",
        report_file_id=415284241282558,
    )),
    ("600276.SS", dict(
        company_ticker="600276.SS", exchange="SSE",
        company_name="Hengrui Pharmaceuticals", chinese_name="恒瑞医药",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=79.20, target_currency="CNY",
        catalyst="GLP-1 full-matrix data at ADA (HRS-9531, HRS-7535, HR17031, HRS-4729)",
        report_file_id=415284241282558,
    )),
    ("9660.HK", dict(
        company_ticker="9660.HK", exchange="HKEX",
        company_name="Horizon Robotics", chinese_name="地平线机器人",
        research_institute="Bernstein", rating="Outperform",
        price_target=10.0, target_currency="HKD",
        catalyst="OEM in-house chip threat overstated; ARM-like BPU IP licensing model",
        report_file_id=812485454488252,
    )),
    ("002847.SZ", dict(
        company_ticker="002847.SZ", exchange="SZSE",
        company_name="Yanker Shop Food", chinese_name="盐津铺子",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=87.0, target_currency="CNY",
        catalyst="Konjac snacks +30% Q2; raw material cost down 25%; mass-channel store gains",
        report_file_id=585412428414554,
    )),
    ("9985.HK", dict(
        company_ticker="9985.HK", exchange="HKEX",
        company_name="Weilong Delicious", chinese_name="卫龙美味",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=14.0, target_currency="HKD",
        catalyst="Konjac snacks resilient; mass channel >35% revenue; 60% dividend payout",
        report_file_id=585412428414554,
    )),
    ("1318.HK", dict(
        company_ticker="1318.HK", exchange="HKEX",
        company_name="Mao Geping Cosmetics", chinese_name="毛戈平",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=106.0, target_currency="HKD",
        catalyst="High-end domestic color cosmetics; Tier-1 wealth-effect beneficiary",
        report_file_id=184152128158222,
    )),
    ("1109.HK", dict(
        company_ticker="1109.HK", exchange="HKEX",
        company_name="China Resources Land", chinese_name="华润置地",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=36.6, target_currency="HKD",
        catalyst="High-end mall operator; Tier-1 housing stabilization beneficiary",
        report_file_id=184152128158222,
    )),
    ("2020.HK", dict(
        company_ticker="2020.HK", exchange="HKEX",
        company_name="Anta Sports", chinese_name="安踏体育",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=108.0, target_currency="HKD",
        catalyst="Arc'teryx/Descente/Kolon premium portfolio; Tier-1 wealth effect",
        report_file_id=184152128158222,
    )),
    ("0027.HK", dict(
        company_ticker="0027.HK", exchange="HKEX",
        company_name="Galaxy Entertainment", chinese_name="银河娱乐",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=53.2, target_currency="HKD",
        catalyst="Macau GGR + Tier-1 housing price stabilization correlation",
        report_file_id=184152128158222,
    )),
    ("1972.HK", dict(
        company_ticker="1972.HK", exchange="HKEX",
        company_name="Swire Properties", chinese_name="太古地产",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=30.7, target_currency="HKD",
        catalyst="High-end commercial property — Taikoo Hui/Li portfolio benefits from Tier-1 recovery",
        report_file_id=184152128158222,
    )),
    ("1928.HK", dict(
        company_ticker="1928.HK", exchange="HKEX",
        company_name="Sands China", chinese_name="金沙中国",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=23.2, target_currency="HKD",
        catalyst="Macau Cotai integrated resorts; premium mass recovery",
        report_file_id=184152128158222,
    )),
    ("1209.HK", dict(
        company_ticker="1209.HK", exchange="HKEX",
        company_name="China Resources Mixc Lifestyle", chinese_name="华润万象生活",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=52.0, target_currency="HKD",
        catalyst="MixC mall management; Tier-1 tenant sales improving sequentially",
        report_file_id=184152128158222,
    )),
    ("6181.HK", dict(
        company_ticker="6181.HK", exchange="HKEX",
        company_name="Lao Pu Gold", chinese_name="老铺黄金",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=1108.0, target_currency="HKD",
        catalyst="Gold + ancient craftsmanship; high-ASP differentiation; Tier-1 wealth effect",
        report_file_id=184152128158222,
    )),
    ("2282.HK", dict(
        company_ticker="2282.HK", exchange="HKEX",
        company_name="MGM China", chinese_name="美高梅中国",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=19.5, target_currency="HKD",
        catalyst="Macau gaming + Tier-1 wealth effect",
        report_file_id=184152128158222,
    )),
    ("0101.HK", dict(
        company_ticker="0101.HK", exchange="HKEX",
        company_name="Hang Lung Properties", chinese_name="恒隆地产",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=11.5, target_currency="HKD",
        catalyst="Plaza 66 Shanghai + mainland high-end mall portfolio; Tier-1 recovery",
        report_file_id=184152128158222,
    )),

    # CATL — Bernstein sodium-ion report
    ("300750.SZ", dict(
        company_ticker="300750.SZ", exchange="SZSE",
        company_name="CATL (Contemporary Amperex)", chinese_name="宁德时代",
        research_institute="Bernstein", rating="Outperform",
        price_target=620.0, target_currency="CNY",
        catalyst="Naxtra Gen-2 sodium-ion 175Wh/kg; 10k cycles; Hubo 60GWh order",
        report_file_id=184152128158542,
    )),
    ("3750.HK", dict(
        company_ticker="3750.HK", exchange="HKEX",
        company_name="CATL (Contemporary Amperex) H", chinese_name="宁德时代",
        research_institute="Bernstein", rating="Outperform",
        price_target=600.0, target_currency="HKD",
        catalyst="Naxtra Gen-2 sodium-ion 175Wh/kg; 10k cycles; Hubo 60GWh order",
        report_file_id=184152128158542,
    )),

    # Bernstein Asia Robotics
    ("002472.SZ", dict(
        company_ticker="002472.SZ", exchange="SZSE",
        company_name="Shuanghuan Driveline", chinese_name="双环传动",
        research_institute="Bernstein", rating="Outperform",
        price_target=60.0, target_currency="CNY",
        catalyst="Industrial robot output +15% YoY; NEV wholesale +10%",
        report_file_id=812485451484122,
    )),
    ("601689.SS", dict(
        company_ticker="601689.SS", exchange="SSE",
        company_name="Tuopu Group", chinese_name="拓普集团",
        research_institute="Bernstein", rating="Outperform",
        price_target=75.0, target_currency="CNY",
        catalyst="Air suspension shipments +114% YoY; Tesla humanoid robotics supplier",
        report_file_id=812485451484122,
    )),
    ("002050.SZ", dict(
        company_ticker="002050.SZ", exchange="SZSE",
        company_name="Sanhua Intelligent Controls A", chinese_name="三花智控",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=39.0, target_currency="CNY",
        catalyst="Tesla humanoid robotics + thermal mgmt; AC export -9%",
        report_file_id=812485451484122,
    )),
    ("2050.HK", dict(
        company_ticker="2050.HK", exchange="HKEX",
        company_name="Sanhua Intelligent Controls H", chinese_name="三花智控",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=27.0, target_currency="HKD",
        catalyst="Tesla humanoid robotics + thermal mgmt; AC export -9%",
        report_file_id=812485451484122,
    )),
    ("HSAI", dict(
        company_ticker="HSAI", exchange="NASDAQ",
        company_name="Hesai Group", chinese_name="禾赛科技",
        research_institute="Bernstein", rating="Outperform",
        price_target=30.0, target_currency="USD",
        catalyst="Long-range ADAS lidar shipments +177% YoY; ~50% market share",
        report_file_id=812485451484122,
    )),
    ("2525.HK", dict(
        company_ticker="2525.HK", exchange="HKEX",
        company_name="Hesai Group H", chinese_name="禾赛科技",
        research_institute="Bernstein", rating="Outperform",
        price_target=238.0, target_currency="HKD",
        catalyst="Long-range ADAS lidar shipments +177% YoY; ~50% market share",
        report_file_id=812485451484122,
    )),
    ("688017.SS", dict(
        company_ticker="688017.SS", exchange="SSE",
        company_name="Leader Drive (Harmonic)", chinese_name="绿的谐波",
        research_institute="Bernstein", rating="Underperform",
        price_target=115.0, target_currency="CNY",
        catalyst="Robot reducer output +38% YoY but valuation rich",
        report_file_id=812485451484122,
    )),

    # ============= Taiwan =============
    ("4958.TW", dict(
        company_ticker="4958.TW", exchange="TWSE",
        company_name="Zhen Ding Technology", chinese_name="臻鼎-KY",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=388.0, target_currency="TWD",
        catalyst="IC substrate +80% YoY 2026; 1.6T optical mSAP ramp Q3",
        report_file_id=415284241285428,
    )),
    ("6515.TW", dict(
        company_ticker="6515.TW", exchange="TWSE",
        company_name="WIN-Vinci Tech", chinese_name="颖崴科技",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=15000.0, target_currency="TWD",
        catalyst="2026 probe pin capacity doubles to 9M/month; CPO socket ramp 2H",
        report_file_id=585412424412254,
    )),
    ("3105.TWO", dict(
        company_ticker="3105.TWO", exchange="TWO",
        company_name="Win Semiconductors", chinese_name="稳懋半导体",
        research_institute="Morgan Stanley", rating="Underweight",
        price_target=300.0, target_currency="TWD",
        catalyst="Industry view 'Attractive' but valuation rich; 43% downside",
        report_file_id=812485211854252,
    )),
    ("4966.TWO", dict(
        company_ticker="4966.TWO", exchange="TWO",
        company_name="Parade Technologies", chinese_name="谱瑞科技",
        research_institute="Morgan Stanley", rating="Overweight",
        price_target=1000.0, target_currency="TWD",
        catalyst="DP/USB-C bridge + AI accelerator interconnects",
        report_file_id=415284511845528,
    )),
    ("6285.TW", dict(
        company_ticker="6285.TW", exchange="TWSE",
        company_name="Sercomm", chinese_name="启碁科技",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=364.0, target_currency="TWD",
        catalyst="800G switch, optical switch, AI-RAN; raised from $318",
        report_file_id=812485454485882,
    )),

    # ============= Japan =============
    ("7269.T", dict(
        company_ticker="7269.JP", exchange="TSE",
        company_name="Suzuki Motor", chinese_name="铃木",
        research_institute="Bernstein", rating="Outperform",
        price_target=2550.0, target_currency="JPY",
        catalyst="Super Carry + Kei-car e-SMART series mild-hybrid; India tailwind",
        report_file_id=812485451482812,
    )),
    ("7203.T", dict(
        company_ticker="7203.JP", exchange="TSE",
        company_name="Toyota Motor", chinese_name="丰田",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=4200.0, target_currency="JPY",
        catalyst="RAV4 6th-gen HEV/PHEV-only; Woven Arene SDV platform",
        report_file_id=812485451482812,
    )),
    ("7267.T", dict(
        company_ticker="7267.JP", exchange="TSE",
        company_name="Honda Motor", chinese_name="本田",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=1400.0, target_currency="JPY",
        catalyst="Reduced/delayed EV investment; refocus on HEV",
        report_file_id=812485451482812,
    )),
    ("6902.T", dict(
        company_ticker="6902.JP", exchange="TSE",
        company_name="Denso", chinese_name="电装",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=2050.0, target_currency="JPY",
        catalyst="3D SiC power semi -70% loss; 2027 8-inch SiC mass production",
        report_file_id=812485451482812,
    )),
    ("6361.T", dict(
        company_ticker="6361.T", exchange="TSE",
        company_name="Ebara Corporation", chinese_name="荏原制作所",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=7100.0, target_currency="JPY",
        catalyst="Precision machinery guidance likely raised in Q2; CMP wafer capex strong",
        report_file_id=212485454485221,
    )),

    # ============= Korea =============
    ("373220.KS", dict(
        company_ticker="373220.KS", exchange="KRX",
        company_name="LG Energy Solution", chinese_name="LG新能源",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=520000.0, target_currency="KRW",
        catalyst="Upgrade from Neutral; ESS TAM expanded to 170GWh; 4680 backlog 440+GWh",
        report_file_id=212485454482511,
    )),
    ("373220.KS", dict(
        company_ticker="373220.KS", exchange="KRX",
        company_name="LG Energy Solution", chinese_name="LG新能源",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=347000.0, target_currency="KRW",
        catalyst="Sodium-ion report; LFP transition pressure",
        report_file_id=184152128158542,
    )),
    ("006400.KS", dict(
        company_ticker="006400.KS", exchange="KRX",
        company_name="Samsung SDI", chinese_name="三星SDI",
        research_institute="Goldman Sachs", rating="Neutral",
        price_target=695000.0, target_currency="KRW",
        catalyst="Downgrade from Buy; YTD +121% vs peers — risk-reward less attractive",
        report_file_id=212485454482511,
    )),
    ("006400.KS", dict(
        company_ticker="006400.KS", exchange="KRX",
        company_name="Samsung SDI", chinese_name="三星SDI",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=520000.0, target_currency="KRW",
        catalyst="Sodium-ion report",
        report_file_id=184152128158542,
    )),
    ("051910.KS", dict(
        company_ticker="051910.KS", exchange="KRX",
        company_name="LG Chem", chinese_name="LG化学",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=480000.0, target_currency="KRW",
        catalyst="SOTP: LGES value + chemicals/materials bottom-recovery; 2028 ROE 15%",
        report_file_id=212485454482511,
    )),
    ("051910.KS", dict(
        company_ticker="051910.KS", exchange="KRX",
        company_name="LG Chem", chinese_name="LG化学",
        research_institute="Bernstein", rating="Market-Perform",
        price_target=298000.0, target_currency="KRW",
        catalyst="Sodium-ion report",
        report_file_id=184152128158542,
    )),
    ("066970.KS", dict(
        company_ticker="066970.KS", exchange="KRX",
        company_name="L&F",
        research_institute="Goldman Sachs", rating="Neutral",
        price_target=139000.0, target_currency="KRW",
        catalyst="US ESS LFP cathode early position; nickel cathode utilization weak",
        report_file_id=212485454482511,
    )),
    ("003670.KS", dict(
        company_ticker="003670.KS", exchange="KRX",
        company_name="POSCO Future M",
        research_institute="Goldman Sachs", rating="Sell",
        price_target=130000.0, target_currency="KRW",
        catalyst="Vertical integration advantages clear but expensive",
        report_file_id=212485454482511,
    )),
    ("247540.KS", dict(
        company_ticker="247540.KS", exchange="KRX",
        company_name="Ecopro BM",
        research_institute="Goldman Sachs", rating="Sell",
        price_target=110000.0, target_currency="KRW",
        catalyst="Sell rating maintained",
        report_file_id=212485454482511,
    )),
    ("096770.KS", dict(
        company_ticker="096770.KS", exchange="KRX",
        company_name="SK Innovation",
        research_institute="Goldman Sachs", rating="Sell",
        price_target=80000.0, target_currency="KRW",
        catalyst="Battery profit inflection later than guidance",
        report_file_id=212485454482511,
    )),
    ("010950.KS", dict(
        company_ticker="010950.KS", exchange="KRX",
        company_name="S-Oil",
        research_institute="Goldman Sachs", rating="Buy",
        price_target=147000.0, target_currency="KRW",
        catalyst="New APAC Conviction add; FCF inflection 2027; refining supercycle",
        report_file_id=585412424411844,
    )),

    # ============= China A-share misc =============
    ("002422.SZ", dict(
        company_ticker="002422.SZ", exchange="SZSE",
        company_name="Sichuan Kelun Pharmaceutical", chinese_name="科伦药业",
        research_institute="Morgan Stanley", rating="Underweight",
        price_target=29.0, target_currency="CNY",
        catalyst="OptiTROP-Lung05 ASCO data; sac-TMT TROP2-ADC ORR strong but safety concerns",
        report_file_id=585412584454284,
    )),
    ("603308.SS", dict(
        company_ticker="603308.SS", exchange="SSE",
        company_name="Anhui Yingliu", chinese_name="应流股份",
        research_institute="J.P. Morgan", rating="Overweight",
        price_target=95.0, target_currency="CNY",
        catalyst="Initiation: rare China name in global gas turbine + aero engine bottleneck",
        report_file_id=415284512252418,
    )),

    # ============= Citi China power equipment =============
    ("2727.HK", dict(
        company_ticker="2727.HK", exchange="HKEX",
        company_name="Shanghai Electric", chinese_name="上海电气",
        research_institute="Citi", rating="Buy",
        price_target=4.5, target_currency="HKD",
        catalyst="Nuclear/fusion exposure; P/B valuation for volatile profit",
        report_file_id=212485214424241,
    )),
    ("1072.HK", dict(
        company_ticker="1072.HK", exchange="HKEX",
        company_name="Dongfang Electric", chinese_name="东方电气",
        research_institute="Citi", rating="Buy",
        price_target=54.0, target_currency="HKD",
        catalyst="Top pick — largest gas turbine overseas exposure + highest margins",
        report_file_id=212485214424241,
    )),
    ("1133.HK", dict(
        company_ticker="1133.HK", exchange="HKEX",
        company_name="Harbin Electric", chinese_name="哈尔滨电气",
        research_institute="Citi", rating="Buy",
        price_target=30.0, target_currency="HKD",
        catalyst="Cheap valuation + full hydro/nuclear order book",
        report_file_id=212485214424241,
    )),

    # ============= Misc =============
    ("2498.HK", dict(
        company_ticker="2498.HK", exchange="HKEX",
        company_name="RoboSense", chinese_name="速腾聚创",
        research_institute="J.P. Morgan", rating="Overweight",
        price_target=45.0, target_currency="HKD",
        catalyst="LIDAR cycle upgrade; BYD partnership deepening; PT rolled to Jun 2027",
        report_file_id=184152121152212,
    )),

    # ============= Indices / Macro =============
    ("^GSPC", dict(
        company_ticker="^GSPC", exchange="INDEX",
        company_name="S&P 500", chinese_name="标普500",
        research_institute="Deutsche Bank", rating="Overweight",
        price_target=8000.0, target_currency="USD",
        catalyst="World Outlook — 1999 tech boom meets 1990 stagflation; SPX 8000 target",
        report_file_id=212485484282841,
    )),
]


def _report_date_from_pdf_name(name: str) -> str | None:
    """Parse YYMMDD from PDF filename suffix like '-260602.pdf'. Returns ISO."""
    import re
    m = re.search(r"-(\d{6})\.pdf$", name)
    if not m:
        return None
    yymmdd = m.group(1)
    try:
        return datetime.strptime(yymmdd, "%y%m%d").date().isoformat()
    except ValueError:
        return None


def _get_report_meta(file_ids: list[int]) -> dict[int, dict]:
    """Bulk-load zsxq.db metadata for the given file_ids."""
    out = {}
    zsxq = db_path("zsxq.db")
    with sqlite3.connect(zsxq) as c:
        qs = ",".join("?" * len(file_ids))
        rows = c.execute(
            f"SELECT file_id, name, create_time FROM pdf_files WHERE file_id IN ({qs})",
            file_ids,
        ).fetchall()
        for fid, name, ctime in rows:
            report_date = _report_date_from_pdf_name(name) or (ctime[:10] if ctime else None)
            out[fid] = dict(pdf_filename=name, report_date=report_date)
    return out


_PRICE_CACHE: dict[tuple[str, str], tuple[float | None, float | None, str | None]] = {}


def _get_price_and_cap(yf_ticker: str, report_date: str) -> tuple[float | None, float | None, str | None]:
    """Fetch close + market cap on report_date for the yf_ticker.

    Market cap = close × shares outstanding (latest available from yfinance).
    Returns (close, market_cap, currency).
    """
    key = (yf_ticker, report_date)
    if key in _PRICE_CACHE:
        return _PRICE_CACHE[key]

    close = None
    cap = None
    ccy = None
    try:
        t = yf.Ticker(yf_ticker)
        # Close on the date (yfinance treats end as exclusive — add 1 day)
        d = datetime.fromisoformat(report_date).date()
        hist = t.history(start=(d - timedelta(days=5)).isoformat(), end=(d + timedelta(days=2)).isoformat())
        if not hist.empty:
            # Take the bar on report_date if available; else last available before
            try:
                day_close = hist.loc[hist.index.date <= d]
                if not day_close.empty:
                    close = float(day_close["Close"].iloc[-1])
            except Exception:
                close = float(hist["Close"].iloc[-1])

        shares = None
        try:
            fi = t.fast_info
            shares = fi.get("shares") or fi.get("shareCount")
            ccy = fi.get("currency")
        except Exception:
            pass
        if not shares:
            try:
                shares = t.info.get("sharesOutstanding")
                ccy = ccy or t.info.get("currency")
            except Exception:
                pass
        if close and shares:
            cap = close * shares
    except Exception as e:
        print(f"  ! yfinance lookup failed for {yf_ticker}: {e}", file=sys.stderr)

    _PRICE_CACHE[key] = (close, cap, ccy)
    return close, cap, ccy


def main():
    # 1. Bulk metadata
    file_ids = sorted({rec[1]["report_file_id"] for rec in RECORDS})
    print(f"Loading metadata for {len(file_ids)} unique reports from zsxq.db…")
    meta = _get_report_meta(file_ids)
    print(f"  resolved {len(meta)}/{len(file_ids)} reports")

    # 2. Insert each row with yfinance lookup
    inserted = skipped = failed = 0
    for yf_ticker, payload in RECORDS:
        fid = payload["report_file_id"]
        m = meta.get(fid, {})
        payload["report_pdf_filename"] = m.get("pdf_filename")
        payload["report_date"] = m.get("report_date") or "2026-06-02"  # fallback to sweep date

        # Fetch price + cap on report_date
        close, cap, ccy = _get_price_and_cap(yf_ticker, payload["report_date"])
        payload["report_date_price"] = close
        payload["report_date_market_cap"] = cap
        payload["price_currency"] = ccy

        try:
            upsert_target(payload)
            inserted += 1
            print(f"  + {payload['company_ticker']:12s} {payload['research_institute']:18s} "
                  f"PT={payload.get('price_target')} {payload.get('target_currency')}  "
                  f"close={close} {ccy}")
        except Exception as e:
            failed += 1
            print(f"  ! FAILED {payload['company_ticker']}: {e}", file=sys.stderr)

    print(f"\nDone. Inserted/upserted {inserted}, failed {failed}")
    print(f"Total rows in DB: {count()}")


if __name__ == "__main__":
    main()
