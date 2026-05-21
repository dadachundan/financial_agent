#!/usr/bin/env python3
"""
seed_company_graph.py — Rebuild the knowledge graph as a clean company-only
network with market-cap-sized nodes and two relation kinds: COMPETES_WITH and
SUPPLIES.

Steps
-----
1. Walk reports/company/ → one canonical company per primary ticker
2. Fetch market caps (USD-equivalent via yfinance + FX cache)
3. Wipe entities / edges / communities / episodes in graph_mirror.db
4. Add market_cap_usd column to entities if missing
5. Insert one Entity node per company (labels=["Company"], market_cap_usd=…)
6. Load reports/graph_seed/*.json — keep only COMPETES_WITH / SUPPLIES /
   CUSTOMER edges whose both endpoints map onto a company in our list.
   CUSTOMER edges are reversed into SUPPLIES (A--CUSTOMER-->B  ≡  B--SUPPLIES-->A).
7. Add a hand-curated set of additional well-known competitor / supplier edges
   so each sector has at least a few links.

Run:
    cd /Users/x/projects/financial_agent
    python3 oneoff/seed_company_graph.py
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import uuid
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from market_cap_cache import get_market_caps, get_fx_rates, to_usd  # noqa: E402

MIRROR_DB    = PROJECT_ROOT / "db" / "graph_mirror.db"
REPORTS_DIR  = PROJECT_ROOT / "reports" / "company"
SEED_DIR     = PROJECT_ROOT / "reports" / "graph_seed"
GROUP_ID     = "financial-pdfs"

# ──────────────────────────────────────────────────────────────────────────────
# Directory → company parsing
# ──────────────────────────────────────────────────────────────────────────────

_EXCH = "(NASDAQ|NYSE|AMEX|OTC|SZSE|SSE|HKEX|KRX|TSE|TWSE|TSX|ASX|XETR)"
TICKER_RE = re.compile(_EXCH + r"_?([0-9]+|[A-Z][A-Z0-9.\-]*)")

# Chinese-name → English alias (for cross-language directory dedup AND for
# matching companies referenced in reports/graph_seed/*.json by either name).
EN_BY_CN = {
    "三花智控": "Sanhua",
    "恒立液压": "Hengli Hydraulic",
    "拓普集团": "Tuopu",
    "汇川技术": "Inovance",
    "绿的谐波": "Leaderdrive",
    "双环传动": "Shuanghuan Drive",
    "奥比中光": "Orbbec",
    "广汽集团": "GAC",
    "比亚迪": "BYD",
    "智谱": "Zhipu",
    "地平线机器人": "Horizon Robotics",
    "优必选": "UBTECH",
    "极智嘉": "Geek+",
    "中际旭创": "InnoLight",
    "壁仞科技": "Biren",
    "沐曦股份": "Muxi",
    "摩尔线程": "Moore Threads",
    "海光信息": "Hygon",
    "寒武纪": "Cambricon",
    "华虹公司": "Hua Hong",
    "中芯国际": "SMIC",
    "中科曙光": "Sugon",
    "汉威科技": "Hanwei",
    "天虹科技": "Tianhong",
    "石头科技": "Roborock",
    "科沃斯": "Ecovacs",
    "潍柴动力": "Weichai",
    "迈为股份": "Maxwell (CN)",
    "贵州茅台": "Kweichow Moutai",
    "紫金矿业": "Zijin Mining",
    "特变电工": "TBEA",
    "国茂股份": "Guomao",
    "申菱环境": "Shenling",
    "英维克": "Envicool",
    "沪电股份": "WUS",
    "生益科技": "Shengyi",
    "广合科技": "Guanghe",
    "黑芝麻智能": "Black Sesame",
    "光环新网": "Sinnet",
    "凌云光": "Luster LightTech",
    "卧安机器人": "Wo'an Robot",
    "微创医疗机器人": "MicroPort Medbot",
    "精锋医疗": "Edge Medical",
    "安培龙": "Anpeilong",
    "澜起科技": "Montage Technology",
    "中坚科技": "Zhongjian",
    "福莱新材": "Foly",
    "布鲁可": "Bruco",
    "思源电气": "Sieyuan",
    "长盛轴承": "Changsheng",
    "双林股份": "Shuanglin Co",
    "裕元集团": "Yue Yuen",
    "商汤": "SenseTime",
    "易方达云计算ETF": "云计算ETF",
    "华富中证人工智能产业ETF": "AI产业ETF",
    "机器人ETF": "机器人ETF",
}

# Directories that share a ticker with an unrelated dir — these are name
# collisions in the source data, not real dupes. Pin them to disambiguated tickers
# (or None for "private"). Maps DIR_NAME → primary ticker override or None.
DIR_TICKER_OVERRIDES = {
    "MiniMax_HKEX100":   None,   # MiniMax is private; HKEX:100 = Yue Yuen
    "布鲁可_HKEX2590":   "HKEX:0325",  # Bruco's real ticker; HKEX:2590 = Geek+
    "SKHynix_KRX_000660":      None,   # dup of SKHynix_KRX000660
    "Samsung_KRX_005930":      None,   # dup of SamsungElectronics_KRX005930
    "Infineon":                None,   # dup of Infineon_XETR_IFX
    "三花智控_HKEX2050":  "HKEX:2050",  # secondary HK listing
}

# Companies with no ticker (private)
PRIVATE_DIRS = {"Agibot", "Anpeilong", "Fourier", "Unitree"}


def parse_dir(name: str) -> tuple[str, list[str]]:
    """Return (display_name, [tickers]) from a company directory name."""
    tickers: list[str] = []
    for m in TICKER_RE.finditer(name):
        tickers.append(f"{m.group(1)}:{m.group(2)}")
    # Display = everything up to the first ticker fragment
    cut = TICKER_RE.search(name)
    display = name[: cut.start()].rstrip("_") if cut else name
    return display, tickers


def is_chinese(s: str) -> bool:
    return bool(re.search(r"[一-鿿]", s))


def collect_companies() -> list[dict]:
    """Return one dict per canonical company: {display, cn, tickers}."""
    by_ticker: dict[str, dict] = {}
    private: list[dict] = []

    for dir_name in sorted(p.name for p in REPORTS_DIR.iterdir() if p.is_dir()):
        # Hard-coded private dirs (no ticker at all)
        if dir_name in PRIVATE_DIRS:
            private.append({"display": dir_name, "cn": "", "tickers": []})
            continue

        # Hard-coded override → drop or relocate ticker
        if dir_name in DIR_TICKER_OVERRIDES:
            override = DIR_TICKER_OVERRIDES[dir_name]
            if override is None:
                continue   # skip duplicate / collision
            display, tickers = parse_dir(dir_name)
            tickers = [override]   # force the right ticker
        else:
            display, tickers = parse_dir(dir_name)
            if not tickers:
                private.append({"display": display, "cn": "", "tickers": []})
                continue

        primary = tickers[0]
        if primary in by_ticker:
            existing = by_ticker[primary]
            # Prefer the English display name; carry the Chinese as `cn`.
            if is_chinese(existing["display"]) and not is_chinese(display):
                existing["cn"]      = existing["display"]
                existing["display"] = display
            elif is_chinese(display) and not is_chinese(existing["display"]):
                existing["cn"] = display
            # Union of tickers
            for t in tickers:
                if t not in existing["tickers"]:
                    existing["tickers"].append(t)
        else:
            cn = display if is_chinese(display) else ""
            en = display if not is_chinese(display) else EN_BY_CN.get(display, display)
            by_ticker[primary] = {"display": en, "cn": cn, "tickers": list(tickers)}

    listed = list(by_ticker.values())
    all_companies = listed + private

    # Second-pass dedup: collapse same-display entries (dual-listed BYD/Alibaba/
    # Sanhua/etc, or a private "Anpeilong" dir + the listed "安培龙" dir).
    by_display: dict[str, dict] = {}
    for c in all_companies:
        d = c["display"]
        if d in by_display:
            ex = by_display[d]
            for t in c["tickers"]:
                if t not in ex["tickers"]:
                    ex["tickers"].append(t)
            if c.get("cn") and not ex.get("cn"):
                ex["cn"] = c["cn"]
        else:
            by_display[d] = c
    return list(by_display.values())


# ──────────────────────────────────────────────────────────────────────────────
# Market cap lookup
# ──────────────────────────────────────────────────────────────────────────────

def attach_market_caps(companies: list[dict]) -> None:
    """Fill each company's market_cap_usd field (None if unknown/private)."""
    tickers = []
    for c in companies:
        if c["tickers"]:
            tickers.append(c["tickers"][0])
    print(f"[market-cap] fetching for {len(tickers)} tickers (cached if same day)…")
    caps = get_market_caps(tickers, block=True)

    # Collect all currencies seen → fetch FX in one batch
    currencies = {ccy for (_mc, ccy) in caps.values() if ccy}
    rates = get_fx_rates(sorted(currencies)) if currencies else {}

    for c in companies:
        if not c["tickers"]:
            c["market_cap_usd"] = None
            continue
        mc, ccy = caps.get(c["tickers"][0], (None, None))
        c["market_cap_usd"]   = to_usd(mc, ccy, rates)
        c["market_cap_local"] = mc
        c["currency"]          = ccy


# ──────────────────────────────────────────────────────────────────────────────
# Edge construction
# ──────────────────────────────────────────────────────────────────────────────

# When seed JSONs reference a company by a slightly different name than the one
# we'll use as our canonical node, map them here.
SEED_NAME_ALIASES = {
    # JSON name              → canonical company display name
    "Hengli Hydraulic":      "Hengli Hydraulic",
    "Joyson Electronics":    "Joyson",
    "Moons' Industries":     "Moons",
    "Keli Sensing":          "Keli",
    "Keli Sensing (corp)":   "Keli",
    "RoboSense":             "Robosense",
    "Robosense":             "Robosense",
    "Omnivision":            "Omnivision",
    "Fortior Technology":    "FortiorTech",
    "BYD Electronic":        None,                # subsidiary — drop
    "BYD Cloud Rail":        None,
    "GAC Group":             "GAC",
    "BYD":                   "BYD",
    "Tesla":                 "Tesla",
    "Apple":                 "Apple",
    "NVIDIA":                "NVIDIA",
    "AMD":                   "AMD",
    "Intel":                 "Intel",
    "Qualcomm":              "Qualcomm",
    "Samsung":               "SamsungElectronics",
    "Samsung (image sensors)": "SamsungElectronics",
    "Samsung Electronics":   "SamsungElectronics",
    "SK Hynix":              "SKHynix",
    "Sony":                  None,                # not in our list
    "TSMC":                  "TSMC",
    "ARM":                   "ARM",
    "Microsoft":             "Microsoft",
    "Amazon":                "Amazon",
    "AWS":                   "Amazon",
    "Google":                "Alphabet",
    "Alphabet":              "Alphabet",
    "GOOG":                  "Alphabet",
    "Meta":                  "Meta",
    "Cadence":               "Cadence",
    "Synopsys":              "Synopsys",
    "Synopsys (SNPS)":       "Synopsys",
    "Hesai":                 "Hesai",
    "Hesai Group":           "Hesai",
    "Xpeng":                 "Xpeng",
    "Baidu":                 "Baidu",
    "WeRide":                "WeRide",
    "Pony.ai":               "PonyAI",
    "PonyAI":                "PonyAI",
    "Xiaomi":                "Xiaomi",
    "Tencent":               "Tencent",
    "Alibaba":               "Alibaba",
    "Alibaba (BABA)":        "Alibaba",
    "CATL":                  "CATL",
    "Estun":                 "Estun",
    "Inovance":              "Inovance",
    "Leadshine":             "Leadshine",
    "Leaderdrive":           "Leaderdrive",
    "Shuanghuan Drive":      "Shuanghuan",
    "Shuanghuan":            "Shuanghuan",
    "Sanhua":                "Sanhua",
    "Tuopu":                 "Tuopu",
    "Joyson":                "Joyson",
    "Wolong Electric":       "Wolong",
    "Wolong":                "Wolong",
    "Dobot":                 "Dobot",
    "Fanuc":                 None,
    "Yaskawa":               None,
    "ABB Robotics":          None,
    "Nabtesco":              None,
    "Harmonic Drive Systems": None,
    "Volkswagen":            None,
    "Foxconn":               "Foxconn",
    "Hon Hai":               "Foxconn",
    "Glorymica":             "Glorymica",
    "Luster LightTech":      None,                # not in dir list as company entry
    "Shuanglin Co":          None,
    "Hanwei Technology":     "Hanwei",
    "Hanwei Technology (corp)": "Hanwei",
    "Zhaowei":               "Zhaowei",
    "UBTECH":                "UBTECH",
    "UBTECH (corp)":         "UBTECH",
    "Unitree":               "Unitree",
    "Agibot":                "Agibot",
    "Fourier Intelligence":  "Fourier",
    "Fourier Intelligence (corp)": "Fourier",
    "Anpeilong":             "Anpeilong",
    "Cipher Mining":         "Cipher",
    "Cipher":                "Cipher",
    "Vistra":                "Vistra",
    "Talen Energy":          "Talen",
    "Talen":                 "Talen",
    "Oklo":                  "Oklo",
    "NuScale":               "NuScale",
    "GE Vernova":            "GEVernova",
    "Vertiv":                "Vertiv",
    "Lumentum":              "Lumentum",
    "Coherent":              "Coherent",
    "Marvell":               "Marvell",
    "Credo":                 "Credo",
    "Astera Labs":           "AsteraLabs",
    "Broadcom":              "Broadcom",
    "Texas Instruments":     "TexasInstruments",
    "Analog Devices":        "AnalogDevices",
    "Microchip":             "Microchip",
    "NXP":                   "NXP",
    "STMicroelectronics":    "STMicroelectronics",
    "Infineon":              "Infineon",
    "Ambarella":             "Ambarella",
    "Rambus":                "Rambus",
    "GSI Technology":        "GSITechnology",
    "Applied Materials":     "AppliedMaterials",
    "Lam Research":          "LamResearch",
    "KLA":                   "KLA",
    "ASML":                  "ASML",
    "Teradyne":              "Teradyne",
    "Advantest":             "Advantest",
    "Navitas":               "Navitas",
    "Cadence Design":        "Cadence",
    "AppliedDigital":        "AppliedDigital",
    "Western Digital":       "WesternDigital",
    "SanDisk":               "SanDisk",
    "Seagate":               "Seagate",
    "Micron":                "Micron",
    "Cambricon":             "Cambricon",
    "Hygon":                 "Hygon",
    "Moore Threads":         "Moore Threads",
    "Biren":                 "Biren",
    "Muxi":                  "Muxi",
    "Horizon Robotics":      "Horizon Robotics",
    "Black Sesame":          "Black Sesame",
    "SMIC":                  "SMIC",
    "Hua Hong":              "Hua Hong",
    "Sugon":                 "Sugon",
    "InnoLight":             "InnoLight",
    "iFlytek":               "iFlytek",
    "Roborock":              "Roborock",
    "Ecovacs":               "Ecovacs",
    "Geek+":                 "Geek+",
    "Bruco":                 "Bruco",
    "Tianhong":              "Tianhong",
    "Hikvision":             None,
    "Dahua":                 None,
    "Huawei":                None,
    "DJI":                   None,
    "Boston Dynamics":       None,
    "Figure AI":              None,
    "Agility Robotics":      None,
    "Universal Robots":      None,
    "KUKA":                  None,
    "X-Humanoid":            None,
    "Pollen Robotics":       None,
    "Robbyant":              None,
    "Bota Systems":          None,
    "Schunk":                None,
    "GeekTouch (Yuancheng)": None,
    "LingXin Dexterous Hand": None,
    "Suzhou Fulaiying":      None,
    "Suzhou NSDA":           None,
    "Bluepoint Touch":       None,
    "ATI Industrial Automation": None,
    "XinJingCheng":          None,
    "HONOR":                 None,
    "Honor":                 None,
    "Mercedes-Benz":         None,
    "BMW":                   None,
    "Ford":                  None,
    "BorgWarner":            None,
    "Toyota":                None,
    "Hyundai-Kia":           None,
    "NIO":                   None,
    "Li Auto":               None,
    "Great Wall Motor":      None,
    "SAIC Motor":            None,
    "Geely":                 None,
    "FAW Group":             None,
    "Stellantis":            None,
    "ATL":                   None,
    "TDK":                   None,
    "Keurig Dr Pepper":      None,
    "Midea":                 "Midea",
    "BSC":                   None,
    "Mining":                None,
}


# Hand-curated edges to fill in well-known relationships not covered by the
# graph_seed JSONs (or to override their direction).
# Each tuple: (src, kind, tgt) — names must match canonical company `display`.
MANUAL_EDGES: list[tuple[str, str, str]] = [
    # ── Semiconductors / compute ─────────────────────────────────────────────
    ("NVIDIA",  "COMPETES_WITH", "AMD"),
    ("NVIDIA",  "COMPETES_WITH", "Intel"),
    ("AMD",     "COMPETES_WITH", "Intel"),
    ("NVIDIA",  "COMPETES_WITH", "Broadcom"),
    ("NVIDIA",  "COMPETES_WITH", "Cambricon"),
    ("NVIDIA",  "COMPETES_WITH", "Hygon"),
    ("NVIDIA",  "COMPETES_WITH", "Biren"),
    ("NVIDIA",  "COMPETES_WITH", "Moore Threads"),
    ("NVIDIA",  "COMPETES_WITH", "Muxi"),
    ("AMD",     "COMPETES_WITH", "Qualcomm"),
    ("Qualcomm","COMPETES_WITH", "ARM"),
    ("Qualcomm","COMPETES_WITH", "Apple"),
    ("Qualcomm","COMPETES_WITH", "Broadcom"),
    ("Marvell", "COMPETES_WITH", "Broadcom"),
    ("Marvell", "COMPETES_WITH", "AsteraLabs"),
    ("Credo",   "COMPETES_WITH", "Marvell"),
    ("Credo",   "COMPETES_WITH", "AsteraLabs"),
    ("Lumentum","COMPETES_WITH", "Coherent"),
    ("Lumentum","COMPETES_WITH", "InnoLight"),
    ("Coherent","COMPETES_WITH", "InnoLight"),
    ("Synopsys","COMPETES_WITH", "Cadence"),
    ("AnalogDevices","COMPETES_WITH","TexasInstruments"),
    ("AnalogDevices","COMPETES_WITH","Microchip"),
    ("AnalogDevices","COMPETES_WITH","Infineon"),
    ("AnalogDevices","COMPETES_WITH","NXP"),
    ("AnalogDevices","COMPETES_WITH","STMicroelectronics"),
    ("TexasInstruments","COMPETES_WITH","Microchip"),
    ("TexasInstruments","COMPETES_WITH","Infineon"),
    ("Infineon","COMPETES_WITH","STMicroelectronics"),
    ("NXP","COMPETES_WITH","STMicroelectronics"),
    ("NXP","COMPETES_WITH","Infineon"),
    ("Navitas","COMPETES_WITH","Infineon"),
    ("Navitas","COMPETES_WITH","STMicroelectronics"),
    ("Rambus","COMPETES_WITH","Montage Technology"),
    ("Ambarella","COMPETES_WITH","Qualcomm"),
    ("Ambarella","COMPETES_WITH","NVIDIA"),

    # Foundry / memory / equipment
    ("TSMC",    "COMPETES_WITH", "SMIC"),
    ("TSMC",    "COMPETES_WITH", "Hua Hong"),
    ("TSMC",    "COMPETES_WITH", "Intel"),
    ("TSMC",    "COMPETES_WITH", "SamsungElectronics"),
    ("SamsungElectronics","COMPETES_WITH","SKHynix"),
    ("SamsungElectronics","COMPETES_WITH","Micron"),
    ("SKHynix","COMPETES_WITH","Micron"),
    ("WesternDigital","COMPETES_WITH","SanDisk"),
    ("WesternDigital","COMPETES_WITH","Seagate"),
    ("SanDisk","COMPETES_WITH","Seagate"),
    ("ASML","COMPETES_WITH","AppliedMaterials"),
    ("AppliedMaterials","COMPETES_WITH","LamResearch"),
    ("AppliedMaterials","COMPETES_WITH","KLA"),
    ("LamResearch","COMPETES_WITH","KLA"),
    ("Teradyne","COMPETES_WITH","Advantest"),

    # Supply chains — foundry / EDA / equipment ⇒ chip designers
    ("TSMC",    "SUPPLIES", "NVIDIA"),
    ("TSMC",    "SUPPLIES", "AMD"),
    ("TSMC",    "SUPPLIES", "Apple"),
    ("TSMC",    "SUPPLIES", "Broadcom"),
    ("TSMC",    "SUPPLIES", "Qualcomm"),
    ("TSMC",    "SUPPLIES", "Marvell"),
    ("TSMC",    "SUPPLIES", "AsteraLabs"),
    ("TSMC",    "SUPPLIES", "Credo"),
    ("TSMC",    "SUPPLIES", "Tesla"),
    ("SMIC",    "SUPPLIES", "Hygon"),
    ("SMIC",    "SUPPLIES", "Cambricon"),
    ("Hua Hong","SUPPLIES", "Hygon"),
    ("ASML",    "SUPPLIES", "TSMC"),
    ("ASML",    "SUPPLIES", "SamsungElectronics"),
    ("ASML",    "SUPPLIES", "Intel"),
    ("ASML",    "SUPPLIES", "SMIC"),
    ("AppliedMaterials","SUPPLIES","TSMC"),
    ("AppliedMaterials","SUPPLIES","SamsungElectronics"),
    ("AppliedMaterials","SUPPLIES","SMIC"),
    ("LamResearch","SUPPLIES","TSMC"),
    ("LamResearch","SUPPLIES","SamsungElectronics"),
    ("LamResearch","SUPPLIES","SMIC"),
    ("KLA",     "SUPPLIES", "TSMC"),
    ("KLA",     "SUPPLIES", "SamsungElectronics"),
    ("Cadence", "SUPPLIES", "NVIDIA"),
    ("Cadence", "SUPPLIES", "AMD"),
    ("Cadence", "SUPPLIES", "Qualcomm"),
    ("Synopsys","SUPPLIES", "NVIDIA"),
    ("Synopsys","SUPPLIES", "AMD"),
    ("Synopsys","SUPPLIES", "Qualcomm"),
    ("ARM",     "SUPPLIES", "Apple"),
    ("ARM",     "SUPPLIES", "Qualcomm"),
    ("ARM",     "SUPPLIES", "NVIDIA"),
    ("Teradyne","SUPPLIES", "TSMC"),
    ("Advantest","SUPPLIES","TSMC"),
    ("Advantest","SUPPLIES","SamsungElectronics"),

    # Memory → big tech
    ("SKHynix", "SUPPLIES", "NVIDIA"),
    ("SamsungElectronics","SUPPLIES","NVIDIA"),
    ("Micron",  "SUPPLIES", "NVIDIA"),
    ("SKHynix", "SUPPLIES", "Apple"),
    ("SamsungElectronics","SUPPLIES","Apple"),
    ("Micron",  "SUPPLIES", "Apple"),

    # Optical
    ("InnoLight","SUPPLIES","NVIDIA"),
    ("InnoLight","SUPPLIES","Microsoft"),
    ("InnoLight","SUPPLIES","Meta"),
    ("InnoLight","SUPPLIES","Alphabet"),
    ("Lumentum","SUPPLIES","NVIDIA"),
    ("Coherent","SUPPLIES","NVIDIA"),

    # PCB / CCL
    ("WUS","SUPPLIES","NVIDIA"),
    ("Shengyi","SUPPLIES","NVIDIA"),
    ("Tianhong","SUPPLIES","NVIDIA"),
    ("Guanghe","SUPPLIES","NVIDIA"),

    # Foxconn
    ("Foxconn", "SUPPLIES", "Apple"),
    ("Foxconn", "SUPPLIES", "NVIDIA"),
    ("Foxconn", "SUPPLIES", "Microsoft"),
    ("Foxconn", "SUPPLIES", "Amazon"),
    ("Foxconn", "SUPPLIES", "Tesla"),

    # ── Hyperscalers / cloud / AI ────────────────────────────────────────────
    ("Microsoft","COMPETES_WITH","Alphabet"),
    ("Microsoft","COMPETES_WITH","Amazon"),
    ("Microsoft","COMPETES_WITH","Oracle"),
    ("Amazon",   "COMPETES_WITH","Alphabet"),
    ("Amazon",   "COMPETES_WITH","Oracle"),
    ("Snowflake","COMPETES_WITH","Datadog"),
    ("MongoDB",  "COMPETES_WITH","Snowflake"),
    ("Datadog",  "COMPETES_WITH","GitLab"),
    ("Palantir", "COMPETES_WITH","Snowflake"),
    ("Palantir", "COMPETES_WITH","Datadog"),
    ("Sinnet",   "COMPETES_WITH","Alibaba"),
    ("Sinnet",   "COMPETES_WITH","Tencent"),
    ("Alibaba",  "COMPETES_WITH","Tencent"),
    ("Alibaba",  "COMPETES_WITH","Baidu"),
    ("Baidu",    "COMPETES_WITH","Tencent"),
    ("iFlytek",  "COMPETES_WITH","Baidu"),
    ("iFlytek",  "COMPETES_WITH","SenseTime"),
    ("SenseTime","COMPETES_WITH","Baidu"),
    ("Zhipu",    "COMPETES_WITH","SenseTime"),
    ("Zhipu",    "COMPETES_WITH","Baidu"),
    ("Zhipu",    "COMPETES_WITH","iFlytek"),
    ("DigitalOcean","COMPETES_WITH","Amazon"),
    ("DigitalOcean","COMPETES_WITH","Alphabet"),

    # Cooling / power infra
    ("Vertiv",   "COMPETES_WITH","Envicool"),
    ("Vertiv",   "COMPETES_WITH","Shenling"),
    ("Vertiv",   "SUPPLIES",     "NVIDIA"),
    ("Envicool", "SUPPLIES",     "NVIDIA"),
    ("Shenling", "SUPPLIES",     "NVIDIA"),
    ("GEVernova","SUPPLIES",     "Microsoft"),
    ("GEVernova","SUPPLIES",     "Amazon"),
    ("GEVernova","SUPPLIES",     "Alphabet"),
    ("Talen",    "SUPPLIES",     "Amazon"),
    ("Vistra",   "SUPPLIES",     "Microsoft"),
    ("Cipher",   "COMPETES_WITH","Talen"),
    ("AppliedDigital","COMPETES_WITH","Cipher"),

    # Nuclear / power
    ("Oklo",     "COMPETES_WITH","NuScale"),
    ("Oklo",     "COMPETES_WITH","Vistra"),
    ("NuScale",  "COMPETES_WITH","Vistra"),

    # ── EV / NEV ──────────────────────────────────────────────────────────────
    ("Tesla",    "COMPETES_WITH","BYD"),
    ("Tesla",    "COMPETES_WITH","Xpeng"),
    ("Tesla",    "COMPETES_WITH","Xiaomi"),
    ("BYD",      "COMPETES_WITH","Xpeng"),
    ("BYD",      "COMPETES_WITH","GAC"),
    ("BYD",      "COMPETES_WITH","Xiaomi"),
    ("Xpeng",    "COMPETES_WITH","Xiaomi"),
    ("Xpeng",    "COMPETES_WITH","WeRide"),
    ("PonyAI",   "COMPETES_WITH","WeRide"),
    ("PonyAI",   "COMPETES_WITH","Baidu"),
    ("WeRide",   "COMPETES_WITH","Baidu"),

    # EV battery
    ("CATL",     "COMPETES_WITH","BYD"),
    ("CATL",     "SUPPLIES","Tesla"),
    ("CATL",     "SUPPLIES","BYD"),
    ("CATL",     "SUPPLIES","Xpeng"),
    ("BYD",      "SUPPLIES","Tesla"),

    # EV component / supplier  → auto OEM
    ("Sanhua",   "SUPPLIES","Tesla"),
    ("Sanhua",   "SUPPLIES","BYD"),
    ("Sanhua",   "SUPPLIES","Xiaomi"),
    ("Sanhua",   "SUPPLIES","Xpeng"),
    ("Tuopu",    "SUPPLIES","Tesla"),
    ("Tuopu",    "SUPPLIES","Xiaomi"),
    ("Tuopu",    "SUPPLIES","BYD"),
    ("Joyson",   "SUPPLIES","Tesla"),
    ("Joyson",   "SUPPLIES","BYD"),
    ("Inovance", "SUPPLIES","Tesla"),
    ("Inovance", "SUPPLIES","BYD"),
    ("Inovance", "SUPPLIES","Xpeng"),
    ("Shuanglin Co", "SUPPLIES","BYD"),
    ("Shuanghuan", "SUPPLIES","Tesla"),
    ("Shuanghuan", "SUPPLIES","BYD"),
    ("Weichai",  "COMPETES_WITH","Caterpillar"),

    # Lidar / ADAS chips / sensors
    ("Hesai",    "COMPETES_WITH","Robosense"),
    ("Hesai",    "SUPPLIES","Xpeng"),
    ("Hesai",    "SUPPLIES","BYD"),
    ("Hesai",    "SUPPLIES","GAC"),
    ("Robosense","SUPPLIES","BYD"),
    ("Robosense","SUPPLIES","GAC"),
    ("Robosense","SUPPLIES","Xpeng"),
    ("Horizon Robotics","SUPPLIES","BYD"),
    ("Horizon Robotics","SUPPLIES","Xpeng"),
    ("Horizon Robotics","SUPPLIES","GAC"),
    ("Black Sesame","SUPPLIES","Xpeng"),
    ("Black Sesame","COMPETES_WITH","Horizon Robotics"),
    ("Black Sesame","COMPETES_WITH","Ambarella"),
    ("Horizon Robotics","COMPETES_WITH","Ambarella"),
    ("Omnivision","COMPETES_WITH","Ambarella"),

    # Humanoid robotics
    ("UBTECH",   "COMPETES_WITH","Unitree"),
    ("UBTECH",   "COMPETES_WITH","Agibot"),
    ("UBTECH",   "COMPETES_WITH","Fourier"),
    ("Unitree",  "COMPETES_WITH","Agibot"),
    ("Unitree",  "COMPETES_WITH","Fourier"),
    ("Agibot",   "COMPETES_WITH","Fourier"),
    ("Dobot",    "COMPETES_WITH","Estun"),
    ("Estun",    "COMPETES_WITH","Inovance"),

    # Humanoid suppliers
    ("Leaderdrive","SUPPLIES","Unitree"),
    ("Leaderdrive","SUPPLIES","UBTECH"),
    ("Leaderdrive","SUPPLIES","Agibot"),
    ("Leaderdrive","SUPPLIES","Fourier"),
    ("Shuanghuan","SUPPLIES","Unitree"),
    ("Shuanghuan","SUPPLIES","UBTECH"),
    ("Shuanghuan","SUPPLIES","Tesla"),
    ("Moons",   "SUPPLIES","Unitree"),
    ("Moons",   "SUPPLIES","UBTECH"),
    ("FortiorTech","SUPPLIES","Moons"),
    ("FortiorTech","SUPPLIES","Inovance"),
    ("FortiorTech","SUPPLIES","Unitree"),
    ("FortiorTech","SUPPLIES","UBTECH"),
    ("Anpeilong","SUPPLIES","Tesla"),
    ("Anpeilong","SUPPLIES","BYD"),
    ("Anpeilong","SUPPLIES","Xpeng"),
    ("Anpeilong","SUPPLIES","Midea"),
    ("Keli",    "SUPPLIES","Tesla"),
    ("Keli",    "SUPPLIES","Unitree"),
    ("Keli",    "SUPPLIES","Agibot"),
    ("Orbbec",  "SUPPLIES","Unitree"),
    ("Orbbec",  "SUPPLIES","Agibot"),
    ("Glorymica","SUPPLIES","Tesla"),
    ("Hanwei",  "SUPPLIES","Tesla"),
    ("Zhaowei", "SUPPLIES","Tesla"),
    ("Zhaowei", "SUPPLIES","Xpeng"),
    ("Wolong",  "SUPPLIES","Tesla"),
    ("Wolong",  "SUPPLIES","BYD"),
    ("Wolong",  "COMPETES_WITH","Inovance"),

    # Streaming / search / consumer
    ("Netflix","COMPETES_WITH","Amazon"),
    ("Netflix","COMPETES_WITH","Apple"),
    ("Netflix","COMPETES_WITH","Alphabet"),
    ("Meta",   "COMPETES_WITH","Alphabet"),
    ("Meta",   "COMPETES_WITH","Tencent"),
    ("Reddit", "COMPETES_WITH","Meta"),

    # Aerospace / defense
    ("RTX",    "COMPETES_WITH","HEICO"),
    ("RTX",    "COMPETES_WITH","Howmet"),
    ("Howmet", "COMPETES_WITH","HEICO"),
    ("Astronics","SUPPLIES","RTX"),
    ("BlackSky", "COMPETES_WITH","Planet"),
    ("BlackSky", "COMPETES_WITH","ASTSpaceMobile"),
    ("Archer",   "COMPETES_WITH","Joby"),

    # Energy / mining
    ("ExxonMobil","COMPETES_WITH","Occidental"),
    ("ExxonMobil","COMPETES_WITH","Shell"),
    ("Occidental","COMPETES_WITH","Shell"),
    ("EnergyFuels","COMPETES_WITH","GMining"),
    ("Ramelius","COMPETES_WITH","GMining"),
    ("Zijin Mining","COMPETES_WITH","GMining"),

    # CCL/PCB
    ("Tianhong","COMPETES_WITH","WUS"),
    ("Tianhong","COMPETES_WITH","Shengyi"),
    ("Tianhong","COMPETES_WITH","Guanghe"),
    ("Shengyi","COMPETES_WITH","WUS"),
    ("Shengyi","COMPETES_WITH","Guanghe"),
    ("WUS","COMPETES_WITH","Guanghe"),

    # Consumer / appliance
    ("Midea",  "COMPETES_WITH","Roborock"),
    ("Midea",  "COMPETES_WITH","Ecovacs"),
    ("Ecovacs","COMPETES_WITH","Roborock"),

    # Lego / toys
    # (no peers in our set)

    # Education
    ("Duolingo","COMPETES_WITH","Stride"),

    # Security
    # PaloAlto has no peer in our set.

    # Logistics / industrial robot
    ("Geek+","COMPETES_WITH","Dobot"),

    # Bottle / drink — none in our set

    # Brk.B / Caterpillar — generic conglom + heavy machinery
    # (skip — too vague)
]


def load_seed_edges(canonical_names: set[str]) -> list[tuple[str, str, str]]:
    """Pull COMPETES_WITH / SUPPLIES / CUSTOMER edges from every seed JSON
    where both endpoints map to a node in `canonical_names`.

    CUSTOMER A → B is rewritten as SUPPLIES B → A (A buys from B).
    """
    out: list[tuple[str, str, str]] = []
    for js in sorted(SEED_DIR.glob("*.json")):
        try:
            payload = json.loads(js.read_text())
        except Exception as e:
            print(f"[seed] {js.name}: parse error {e}", file=sys.stderr)
            continue
        for e in payload.get("edges", []):
            kind = e.get("name", "")
            src  = SEED_NAME_ALIASES.get(e["src"], e["src"])
            tgt  = SEED_NAME_ALIASES.get(e["tgt"], e["tgt"])
            if not src or not tgt:
                continue
            if src not in canonical_names or tgt not in canonical_names:
                continue
            if src == tgt:
                continue
            if kind in ("COMPETES_WITH", "SUPPLIES"):
                out.append((src, kind, tgt))
            elif kind == "CUSTOMER":
                # A--CUSTOMER-->B  ≡  B--SUPPLIES-->A
                out.append((tgt, "SUPPLIES", src))
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Mirror DB I/O
# ──────────────────────────────────────────────────────────────────────────────

def connect_mirror() -> sqlite3.Connection:
    conn = sqlite3.connect(str(MIRROR_DB), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def add_market_cap_column(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(entities)").fetchall()}
    if "market_cap_usd" not in cols:
        conn.execute("ALTER TABLE entities ADD COLUMN market_cap_usd REAL")
    if "ticker" not in cols:
        conn.execute("ALTER TABLE entities ADD COLUMN ticker TEXT DEFAULT ''")
    conn.commit()


def wipe_graph(conn: sqlite3.Connection) -> None:
    print("[wipe] clearing entities / edges / communities / episodes …")
    for tbl in ("community_members", "communities",
                "edges_fts", "edges",
                "entities_fts", "entities",
                "episodes",
                "pending_deletions"):
        try:
            conn.execute(f"DELETE FROM {tbl}")
        except sqlite3.OperationalError:
            pass
    conn.commit()


def insert_nodes(conn: sqlite3.Connection, companies: list[dict]) -> dict[str, str]:
    """Insert one entity per company. Returns {display_name → uuid}."""
    name_to_uuid: dict[str, str] = {}
    rows = []
    for c in companies:
        u  = str(uuid.uuid4())
        nm = c["display"]
        if c.get("cn") and c["cn"] != nm:
            nm = f"{c['display']} ({c['cn']})"
        labels = ["Company"]
        ticker = c["tickers"][0] if c["tickers"] else ""
        mcusd  = c.get("market_cap_usd")
        local  = c.get("market_cap_local")
        ccy    = c.get("currency") or ""
        if mcusd:
            mc_str = f"${mcusd/1e9:.1f}B" if mcusd >= 1e9 else f"${mcusd/1e6:.0f}M"
        else:
            mc_str = "—"
        summary = (
            f"Ticker: {ticker or 'private'} · Market cap: {mc_str}"
            + (f" ({local:,} {ccy})" if local and ccy and ccy != 'USD' else "")
        )
        rows.append((u, nm, json.dumps(labels), summary, ticker, mcusd))
        name_to_uuid[c["display"]] = u
    conn.executemany(
        "INSERT INTO entities (uuid, name, labels_json, summary, ticker, market_cap_usd) "
        "VALUES (?,?,?,?,?,?)",
        rows,
    )
    conn.commit()
    return name_to_uuid


def insert_edges(conn: sqlite3.Connection,
                 edges: list[tuple[str, str, str]],
                 name_to_uuid: dict[str, str],
                 company_name_by_display: dict[str, str]) -> int:
    """Insert dedup'd edges into the mirror. Returns count written."""
    seen: set[tuple[str, str, str]] = set()
    rows = []
    for src, kind, tgt in edges:
        if src == tgt:
            continue
        if src not in name_to_uuid or tgt not in name_to_uuid:
            continue
        key = (src, kind, tgt)
        if key in seen:
            continue
        seen.add(key)
        eu = str(uuid.uuid4())
        sn = company_name_by_display[src]
        tn = company_name_by_display[tgt]
        fact = f"{sn} {'competes with' if kind == 'COMPETES_WITH' else 'supplies'} {tn}"
        rows.append((eu, kind, fact,
                     name_to_uuid[src], sn,
                     name_to_uuid[tgt], tn))
    if rows:
        conn.executemany(
            "INSERT INTO edges (uuid, name, fact, src_uuid, src_name, "
            "tgt_uuid, tgt_name) VALUES (?,?,?,?,?,?,?)",
            rows,
        )
        conn.commit()
    return len(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    companies = collect_companies()
    print(f"[parse] {len(companies)} canonical companies")

    attach_market_caps(companies)
    n_priced = sum(1 for c in companies if c.get("market_cap_usd"))
    print(f"[parse] {n_priced}/{len(companies)} have a market cap")

    canonical_names = {c["display"] for c in companies}

    conn = connect_mirror()
    add_market_cap_column(conn)
    wipe_graph(conn)

    name_to_uuid = insert_nodes(conn, companies)
    print(f"[insert] {len(name_to_uuid)} nodes")

    # Build label map for edge inserts (display → full label as stored)
    full_label_by_display = {
        c["display"]: c["display"] + (f" ({c['cn']})" if c.get("cn") and c["cn"] != c["display"] else "")
        for c in companies
    }

    seed_edges   = load_seed_edges(canonical_names)
    manual_edges = [(s, k, t) for s, k, t in MANUAL_EDGES
                     if s in canonical_names and t in canonical_names]
    all_edges    = seed_edges + manual_edges
    print(f"[edges] seed={len(seed_edges)} manual={len(manual_edges)} "
          f"total before dedup={len(all_edges)}")

    n = insert_edges(conn, all_edges, name_to_uuid, full_label_by_display)
    print(f"[insert] {n} edges (after dedup)")

    # Sentinel episode — the mirror's first-request backfill check treats an
    # empty episodes table (or edges with no episodes attached) as
    # "uninitialised" and tries to re-pull from KuzuDB. An explicit row, plus
    # tagging every edge with that episode, keeps the check happy across
    # server restarts even when KuzuDB is empty.
    sentinel_uuid = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO episodes (uuid, name, source_desc) VALUES (?,?,?)",
        (sentinel_uuid, "company_seed",
         "Synthetic episode from oneoff/seed_company_graph.py"),
    )
    conn.execute(
        "UPDATE edges SET episodes_json = ?",
        (json.dumps([sentinel_uuid]),),
    )
    conn.commit()

    # Final stats
    e_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    g_count = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    print(f"[done] mirror: {e_count} entities, {g_count} edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
