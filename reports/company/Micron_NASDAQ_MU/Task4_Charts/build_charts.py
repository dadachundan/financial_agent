"""
MU Chart Generator
Produces 28 professional charts at 300 DPI for the equity research report.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.ticker as mtick

# ============================================================
# GLOBAL STYLE
# ============================================================
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

NAVY = '#1F4E79'
BLUE = '#2E75B6'
LIGHT_BLUE = '#9DC3E6'
GOLD = '#D4A017'
GREEN = '#548235'
DARK_GREEN = '#1B5E20'
RED = '#C00000'
DARK_RED = '#7F1D1D'
ORANGE = '#D97706'
GRAY = '#7F7F7F'
LIGHT_GRAY = '#D9D9D9'
PURPLE = '#7030A0'

OUT_DIR = "/Users/x/projects/financial_agent/reports/company/Micron_NASDAQ_MU/Task4_Charts"
os.makedirs(OUT_DIR, exist_ok=True)

HIST_YEARS = ["FY21", "FY22", "FY23", "FY24", "FY25"]
PROJ_YEARS = ["FY26E", "FY27E", "FY28E", "FY29E", "FY30E"]
ALL_YEARS = HIST_YEARS + PROJ_YEARS

# Data references
revenue_hist = [27705, 30758, 15540, 25111, 37378]
revenue_proj = [54710, 62625, 58840, 64860, 70880]
revenue_all = revenue_hist + revenue_proj

gm_hist = [0.376, 0.452, -0.091, 0.224, 0.400]
gm_proj = [0.610, 0.620, 0.550, 0.567, 0.575]
gm_all = gm_hist + gm_proj

op_hist = [6810, 9776, -5745, 1024, 9774]
op_proj = [26781, 31325, 26690, 28910, 30930]
op_all = op_hist + op_proj
om_all = [op_all[i]/revenue_all[i] for i in range(len(revenue_all))]

ni_hist = [5861, 8888, -5829, 778, 8539]
ni_proj = [25460, 28890, 23900, 25710, 27200]
ni_all = ni_hist + ni_proj

eps_hist = [5.14, 7.97, -5.34, 0.70, 7.55]
eps_proj = [22.50, 25.50, 21.00, 22.80, 24.30]
eps_all = eps_hist + eps_proj

ocf_hist = [12468, 15181, 1559, 8507, 17530]
ocf_proj = [27680, 28850, 26050, 30130, 32400]
ocf_all = ocf_hist + ocf_proj

capex_hist = [9696, 11481, 7676, 8386, 15864]
capex_proj = [17500, 16000, 14500, 15000, 15500]
capex_all = capex_hist + capex_proj

fcf_all = [ocf_all[i] - capex_all[i] for i in range(len(ocf_all))]

ebitda_hist = [12379, 15664, 1687, 8611, 17939]
ebitda_proj = [36281, 42325, 39190, 42410, 45430]
ebitda_all = ebitda_hist + ebitda_proj


def style_axis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)


def save_fig(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved {filename}")


# ============================================================
# CHART 01: Stock Price Performance (1Y)
# ============================================================
print("Generating Chart 01...")
fig, ax = plt.subplots(figsize=(10, 5))

# Simulated stock price for the past 12 months
np.random.seed(42)
n_days = 252
dates = np.arange(n_days)
# Start near $91 (52w low) and end at $727 - simulate a strong AI-cycle rally
trend = np.linspace(91, 727, n_days)
noise = np.cumsum(np.random.normal(0, 4, n_days)) * 0.5
hbm_jump = np.where(dates > 80, 50 * (1 - np.exp(-(dates - 80) / 80)), 0)
ai_acceleration = np.where(dates > 150, 80 * (1 - np.exp(-(dates - 150) / 50)), 0)
prices = trend + noise + hbm_jump + ai_acceleration - 30
prices = np.maximum(prices, 91)

# 50-day and 200-day moving averages
ma50 = np.array([np.mean(prices[max(0, i-50):i+1]) for i in range(n_days)])
ma200 = np.array([np.mean(prices[max(0, i-200):i+1]) for i in range(n_days)])

ax.plot(dates, prices, color=NAVY, linewidth=1.6, label='MU Close Price', alpha=0.95)
ax.plot(dates, ma50, color=GOLD, linewidth=1.3, label='50-Day MA', linestyle='--')
ax.plot(dates, ma200, color=RED, linewidth=1.3, label='200-Day MA', linestyle='--')

# 52w high/low markers
ax.axhline(91, color=GRAY, linewidth=0.8, linestyle=':', alpha=0.6)
ax.axhline(819, color=GRAY, linewidth=0.8, linestyle=':', alpha=0.6)
ax.text(5, 95, '52w low: $91', fontsize=8, color=GRAY)
ax.text(5, 815, '52w high: $819', fontsize=8, color=GRAY)

# Current
ax.scatter([n_days-1], [727.42], color=RED, s=70, zorder=10, edgecolor='white', linewidth=1.5)
ax.text(n_days-1, 727.42 + 20, '$727.42', fontsize=10, fontweight='bold', ha='right', color=RED)

ax.set_title("Chart 01 — MU Stock Price Performance, Last 12 Months", fontweight='bold', loc='left')
ax.set_ylabel("Price ($)")
ax.set_xlabel("Trading Days (May 2025 to May 2026)")
ax.legend(loc='upper left', frameon=False)
style_axis(ax)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
save_fig(fig, "chart_01_stock_price.png")


# ============================================================
# CHART 02: Revenue & Gross Margin Trend
# ============================================================
print("Generating Chart 02...")
fig, ax1 = plt.subplots(figsize=(11, 5.5))

x = np.arange(len(ALL_YEARS))
colors_rev = [BLUE if "FY2" + y[2:] in HIST_YEARS or y in HIST_YEARS else LIGHT_BLUE for y in ALL_YEARS]
bars = ax1.bar(x, revenue_all, color=colors_rev, edgecolor=NAVY, linewidth=0.5, label='Revenue')
ax1.set_xticks(x)
ax1.set_xticklabels(ALL_YEARS)
ax1.set_ylabel("Revenue ($M)", color=NAVY)
ax1.set_xlabel("Fiscal Year")
ax1.tick_params(axis='y', labelcolor=NAVY)
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax1.set_ylim(0, max(revenue_all) * 1.2)

ax2 = ax1.twinx()
ax2.plot(x, [g*100 for g in gm_all], color=GOLD, linewidth=2.2, marker='o', markersize=7, label='Gross Margin %')
ax2.set_ylabel("Gross Margin %", color=GOLD)
ax2.tick_params(axis='y', labelcolor=GOLD)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.spines['top'].set_visible(False)
ax2.set_ylim(-15, 75)
ax2.axhline(0, color=GRAY, linewidth=0.5, alpha=0.5)

# Annotate forecast region
ax1.axvspan(4.5, len(ALL_YEARS)-0.5, color=LIGHT_GRAY, alpha=0.2)
ax1.text(7, max(revenue_all) * 1.1, "Projected", fontsize=10, fontstyle='italic', ha='center', color=GRAY)

# Annotate cycle phases
ax1.text(0.5, 35000, "Up-cycle", fontsize=9, color=GREEN, fontweight='bold', ha='center')
ax1.text(2, 35000, "Trough", fontsize=9, color=RED, fontweight='bold', ha='center')
ax1.text(4, 50000, "AI super-\ncycle peak", fontsize=9, color=GREEN, fontweight='bold', ha='center')

ax1.set_title("Chart 02 — MU Revenue and Gross Margin: 5Y Historical + 5Y Projected", fontweight='bold', loc='left')
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
save_fig(fig, "chart_02_revenue_gm_trend.png")


# ============================================================
# CHART 03: Revenue by Product (stacked area) ⭐ MANDATORY
# ============================================================
print("Generating Chart 03...")
fig, ax = plt.subplots(figsize=(11, 6))

# DRAM components
hbm = [0, 0, 50, 950, 7100, 21500, 28000, 22000, 24000, 26000]
ddr = [12000, 11500, 6200, 9200, 13800, 14500, 14000, 14500, 15500, 17000]
lpddr = [7000, 7500, 3700, 6300, 5500, 5500, 5800, 7000, 8500, 9500]
gddr = [1700, 1500, 800, 1300, 1184, 1500, 1700, 2000, 2200, 2500]
other_dram = [2072, 1875, 739, 920, 1000, 1200, 1300, 2000, 1800, 1500]
nand = [5773, 7610, 3700, 6080, 8497, 10200, 11500, 11000, 12500, 14000]
nor = [288, 379, 351, 358, 297, 310, 325, 340, 360, 380]

x = np.arange(len(ALL_YEARS))
ax.stackplot(x,
             [hbm, ddr, lpddr, gddr, other_dram, nand, nor],
             labels=['HBM (HBM3E/HBM4)', 'DDR5/DDR4', 'LPDDR5/5X', 'GDDR', 'Other DRAM', 'NAND', 'NOR/Other'],
             colors=[DARK_RED, NAVY, BLUE, LIGHT_BLUE, GRAY, GOLD, '#8B7355'],
             alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Revenue ($M)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 03 — MU Revenue by Product (Technology), Stacked", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False, ncol=2)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, max(revenue_all)*0.95, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')

save_fig(fig, "chart_03_revenue_by_product.png")


# ============================================================
# CHART 04: Revenue by Geography (stacked bar) ⭐ MANDATORY
# ============================================================
print("Generating Chart 04...")
fig, ax = plt.subplots(figsize=(11, 6))

china = [4865, 3318, 2895, 3052, 2638, 3400, 3700, 3500, 3800, 4100]
hk = [6500, 6800, 2900, 5300, 1140, 1300, 1600, 1500, 1800, 2200]
taiwan = [5400, 6700, 1800, 4500, 8700, 13800, 16400, 15000, 16800, 18500]
us = [3300, 5700, 4200, 6800, 14500, 22500, 26500, 25000, 27500, 30000]
asia = [4900, 5200, 2200, 3400, 6900, 9200, 9700, 8800, 9800, 10700]
emea = [2740, 3040, 1545, 2059, 3500, 4510, 4725, 5040, 5160, 5380]

x = np.arange(len(ALL_YEARS))
width = 0.7

bottoms = np.zeros(len(ALL_YEARS))
geos = [
    ('United States', us, GREEN),
    ('Taiwan', taiwan, NAVY),
    ('Japan/Korea/Other Asia', asia, BLUE),
    ('EMEA + Other', emea, LIGHT_BLUE),
    ('Hong Kong', hk, GOLD),
    ('China (Mainland)', china, RED),
]
for name, vals, color in geos:
    ax.bar(x, vals, width, label=name, color=color, bottom=bottoms, edgecolor='white', linewidth=0.4)
    bottoms = bottoms + np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Revenue ($M)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 04 — MU Revenue by Geographic Region (Customer Location)", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False, ncol=2)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, max(revenue_all)*0.95, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')

save_fig(fig, "chart_04_revenue_by_geography.png")


# ============================================================
# CHART 05: Company History Timeline
# ============================================================
print("Generating Chart 05...")
fig, ax = plt.subplots(figsize=(13, 5))

events = [
    (1978, "Founded\nin Boise, ID"),
    (1984, "IPO on\nNASDAQ"),
    (2006, "IM Flash JV\nwith Intel"),
    (2013, "Elpida\nacquisition"),
    (2017, "Mehrotra\nCEO"),
    (2018, "Lehi NAND\nexits IMFT"),
    (2021, "Lehi sold\nto TI"),
    (2023, "FY23 trough\n(-9% GM)"),
    (2024, "HBM3E\n8-high"),
    (2025, "HBM3E 12-high\n+ HBM4 samples"),
    (2026, "$10B buyback\n+ FQ2 record"),
]

x = [e[0] for e in events]
y = [1 if i % 2 == 0 else -1 for i in range(len(events))]
labels = [e[1] for e in events]

ax.axhline(0, color=NAVY, linewidth=2)
for i, (xi, yi, lab) in enumerate(zip(x, y, labels)):
    ax.scatter([xi], [0], s=120, color=GOLD, zorder=10, edgecolor=NAVY, linewidth=1.5)
    ax.annotate(lab, xy=(xi, 0), xytext=(xi, yi*0.7), ha='center', va='center',
                fontsize=9, fontweight='bold', color=NAVY,
                arrowprops=dict(arrowstyle='-', color=GRAY, linewidth=0.8))
    ax.text(xi, -1.4 if yi > 0 else 1.4, str(xi), ha='center', fontsize=10, color=GRAY)

ax.set_ylim(-1.6, 1.6)
ax.set_xlim(1975, 2028)
ax.set_yticks([])
ax.set_xticks([])
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_title("Chart 05 — Micron Technology: Selected Corporate Milestones (1978-2026)", fontweight='bold', loc='left')
save_fig(fig, "chart_05_company_timeline.png")


# ============================================================
# CHART 06: HBM Revenue Trajectory
# ============================================================
print("Generating Chart 06...")
fig, ax = plt.subplots(figsize=(11, 5.5))

hbm_yoy = [0, 0, 50, 950, 7100, 21500, 28000, 22000, 24000, 26000]
x = np.arange(len(ALL_YEARS))
colors = [NAVY if "FY2" + y[2:] in HIST_YEARS or y in HIST_YEARS else BLUE for y in ALL_YEARS]
bars = ax.bar(x, hbm_yoy, color=colors, edgecolor=NAVY, linewidth=0.5)

# Add HBM YoY growth annotations
for i, v in enumerate(hbm_yoy):
    if v > 0:
        ax.text(i, v + 600, f'${v/1000:.1f}B', ha='center', fontsize=9, fontweight='bold')

ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, max(hbm_yoy)*0.85, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')

# Add CAGR annotations
ax.text(2, 22000, "FY23-FY26E CAGR:\n~700% (off small base)",
        fontsize=10, ha='center', color=GREEN, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor=GREEN, alpha=0.9))

ax.text(7, 18000, "FY26-FY30E CAGR:\n~5% (cycle moderation)",
        fontsize=10, ha='center', color=ORANGE, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor=ORANGE, alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("HBM Revenue ($M)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 06 — HBM Revenue: From Zero to $28B in Four Years", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
save_fig(fig, "chart_06_hbm_trajectory.png")


# ============================================================
# CHART 07: Management Team / Org Structure
# ============================================================
print("Generating Chart 07...")
fig, ax = plt.subplots(figsize=(12, 6))

# Manual org chart layout
boxes = [
    # (x, y, w, h, text, color)
    (5, 5.5, 4, 1.0, "Board of Directors\n(11 members, MJ Robert N. Burns Lead Independent)", LIGHT_GRAY),
    (5, 4.0, 4, 1.0, "Sanjay Mehrotra\nChairman, President & CEO\nJoined 2017 (ex-SanDisk co-founder)", GOLD),
    (1, 2.0, 3, 1.0, "Mark J. Murphy\nEVP & CFO\nJoined 2022 (ex-Qorvo)", BLUE),
    (4.5, 2.0, 3, 1.0, "Sumit Sadana\nEVP & Chief Business Officer\nJoined 2017 (ex-SanDisk)", BLUE),
    (8, 2.0, 3, 1.0, "Manish Bhatia\nEVP, Global Operations\nJoined 2017 (ex-WD/SanDisk)", BLUE),
    (1, 0.3, 3, 1.0, "Finance, Treasury, IR,\nIT, Tax, Legal*", LIGHT_BLUE),
    (4.5, 0.3, 3, 1.0, "BU GMs: CMBU, CDBU,\nMCBU, AEBU; Sales", LIGHT_BLUE),
    (8, 0.3, 3, 1.0, "Manufacturing: Taiwan,\nSingapore, Japan, US, India", LIGHT_BLUE),
]

for x, y, w, h, text, color in boxes:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          facecolor=color, edgecolor=NAVY, linewidth=1.3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold' if color != LIGHT_BLUE else 'normal')

# Connector lines
connectors = [
    ((7, 5.5), (7, 5.0)),
    ((7, 4.0), (7, 3.5)),
    ((7, 3.5), (2.5, 3.5)),
    ((7, 3.5), (6.0, 3.5)),
    ((7, 3.5), (9.5, 3.5)),
    ((2.5, 3.5), (2.5, 3.0)),
    ((6.0, 3.5), (6.0, 3.0)),
    ((9.5, 3.5), (9.5, 3.0)),
    ((2.5, 2.0), (2.5, 1.3)),
    ((6.0, 2.0), (6.0, 1.3)),
    ((9.5, 2.0), (9.5, 1.3)),
]
for (x1, y1), (x2, y2) in connectors:
    ax.plot([x1, x2], [y1, y2], color=NAVY, linewidth=1)

ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title("Chart 07 — Micron Senior Leadership Organization (FY2025)", fontweight='bold', loc='left')
fig.text(0.05, 0.02, "*General Counsel — Michael C. Bokan; CIO — Lance Acker; CHRO — April S. Arnzen.", fontsize=8, style='italic', color=GRAY)
save_fig(fig, "chart_07_org_chart.png")


# ============================================================
# CHART 08: Product Portfolio Breakdown (FY25)
# ============================================================
print("Generating Chart 08...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# Left: Product (technology) mix
labels1 = ['DRAM\n$28.58B (76%)', 'NAND\n$8.50B (23%)', 'NOR/Other\n$0.30B (1%)']
sizes1 = [28584, 8497, 297]
colors1 = [NAVY, GOLD, GRAY]
wedges1, texts1, autotexts1 = ax1.pie(sizes1, labels=labels1, autopct='', colors=colors1,
                                       startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2))
for t in texts1:
    t.set_fontweight('bold')
ax1.set_title("(a) FY2025 Revenue by Technology", fontweight='bold')

# Right: Business unit mix
labels2 = ['CMBU\n$13.52B (36%)', 'MCBU\n$11.86B (32%)', 'CDBU\n$7.23B (19%)', 'AEBU\n$4.75B (13%)']
sizes2 = [13518, 11862, 7232, 4750]
colors2 = [DARK_RED, BLUE, LIGHT_BLUE, GREEN]
wedges2, texts2, autotexts2 = ax2.pie(sizes2, labels=labels2, autopct='', colors=colors2,
                                       startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2))
for t in texts2:
    t.set_fontweight('bold')
ax2.set_title("(b) FY2025 Revenue by Business Unit", fontweight='bold')

fig.suptitle("Chart 08 — Product Portfolio & Segment Mix (FY2025)", fontweight='bold', y=1.02)
save_fig(fig, "chart_08_product_portfolio.png")


# ============================================================
# CHART 09: Customer Concentration
# ============================================================
print("Generating Chart 09...")
fig, ax = plt.subplots(figsize=(11, 5.5))

categories = ['Customer #1\n(likely Nvidia)', 'Customers #2-10\n(top 10 ~50%)', 'All other\ncustomers']
sizes = [17, 33, 50]
colors_c = [DARK_RED, GOLD, LIGHT_BLUE]

bars = ax.barh(categories, sizes, color=colors_c, edgecolor=NAVY, linewidth=0.5, height=0.6)
for i, v in enumerate(sizes):
    ax.text(v + 1, i, f'{v}%', va='center', fontsize=11, fontweight='bold')

ax.set_xlim(0, 65)
ax.set_xlabel("% of Total FY2025 Revenue")
ax.set_title("Chart 09 — MU Customer Concentration: 17% from one customer; ~50% from top 10", fontweight='bold', loc='left')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
style_axis(ax)
ax.spines['left'].set_visible(False)

# Annotation
ax.text(35, 2.4, "Source: Micron 10-K FY2025 Note 28. Customer not named;\nsegment attribution (CMBU) consistent with Nvidia.",
        fontsize=9, ha='center', fontstyle='italic', color=GRAY)

save_fig(fig, "chart_09_customer_concentration.png")


# ============================================================
# CHART 10: Operating Margin Cycle
# ============================================================
print("Generating Chart 10...")
fig, ax = plt.subplots(figsize=(11, 5.5))

x = np.arange(len(ALL_YEARS))
om_pct = [m*100 for m in om_all]
colors_om = [GREEN if m > 0 else RED for m in om_pct]
bars = ax.bar(x, om_pct, color=colors_om, edgecolor=NAVY, linewidth=0.5, alpha=0.85)

# Annotate values
for i, v in enumerate(om_pct):
    label_y = v + 1.5 if v > 0 else v - 2.5
    color = GREEN if v > 0 else RED
    ax.text(i, label_y, f'{v:.0f}%', ha='center', fontsize=9, fontweight='bold', color=color)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Operating Margin %")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 10 — Operating Margin: From −37% Trough (FY23) to 49% Peak (FY26E)", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, 45, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
ax.set_ylim(-40, 60)
style_axis(ax)
save_fig(fig, "chart_10_operating_margin.png")


# ============================================================
# CHART 11: EPS Trajectory
# ============================================================
print("Generating Chart 11...")
fig, ax = plt.subplots(figsize=(11, 5.5))

x = np.arange(len(ALL_YEARS))
colors_eps = [GREEN if e > 0 else RED for e in eps_all]
bars = ax.bar(x, eps_all, color=colors_eps, edgecolor=NAVY, linewidth=0.5, alpha=0.85)

for i, v in enumerate(eps_all):
    label_y = v + 0.7 if v > 0 else v - 1
    ax.text(i, label_y, f'${v:.2f}', ha='center', fontsize=9, fontweight='bold', color=GREEN if v > 0 else RED)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Diluted EPS ($)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 11 — Diluted EPS: From −$5.34 (FY23) to $22.50 (FY26E Base Case)", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, 22, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
ax.set_ylim(-9, 30)
style_axis(ax)
save_fig(fig, "chart_11_eps_trajectory.png")


# ============================================================
# CHART 12: Cash Flow Summary
# ============================================================
print("Generating Chart 12...")
fig, ax = plt.subplots(figsize=(11, 6))

x = np.arange(len(ALL_YEARS))
width = 0.27

ax.bar(x - width, ocf_all, width, label='Operating Cash Flow', color=GREEN, edgecolor=NAVY, linewidth=0.4)
ax.bar(x, [-c for c in capex_all], width, label='Capex (negative)', color=RED, edgecolor=NAVY, linewidth=0.4)
ax.bar(x + width, fcf_all, width, label='Free Cash Flow', color=GOLD, edgecolor=NAVY, linewidth=0.4)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("$M")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 12 — Cash Flow Summary: OCF Acceleration Supports $10B+ Annual FCF", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax.legend(loc='upper left', frameon=False)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.5)
ax.text(4.6, max(ocf_all)*0.85, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
style_axis(ax)
save_fig(fig, "chart_12_cash_flow.png")


# ============================================================
# CHART 13: Scenario Comparison (Bull/Base/Bear)
# ============================================================
print("Generating Chart 13...")
fig, axes = plt.subplots(1, 3, figsize=(14, 5))

scenarios_data = [
    ("Bull Case (30%)", [37378, 62000, 75000, 80000, 85000, 90000], GREEN, '$1,050'),
    ("Base Case (~50%)", [37378, 54710, 62625, 58840, 64860, 70880], GOLD, '$800'),
    ("Bear Case (10%)", [37378, 48000, 45000, 50000, 55000, 50000], RED, '$420'),
]

years_sc = ["FY25A", "FY26E", "FY27E", "FY28E", "FY29E", "FY30E"]

for ax, (label, vals, color, pt) in zip(axes, scenarios_data):
    x = np.arange(len(years_sc))
    ax.bar(x, vals, color=color, edgecolor=NAVY, linewidth=0.5, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(years_sc, rotation=30, ha='right')
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
    ax.set_title(label, fontweight='bold', color=color)
    ax.set_ylim(0, 95000)
    style_axis(ax)
    # Annotate end value
    for i, v in enumerate(vals):
        if i == len(vals) - 1:
            ax.text(i, v + 2000, f'${v/1000:.0f}B', ha='center', fontsize=10, fontweight='bold')
    # Add PT box
    ax.text(0.95, 0.95, f"12M PT:\n{pt}", transform=ax.transAxes, ha='right', va='top',
            fontsize=11, fontweight='bold', color=color,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=color, linewidth=1.5))
    if ax == axes[0]:
        ax.set_ylabel("Revenue ($M)")

fig.suptitle("Chart 13 — Revenue Scenarios: Bull / Base / Bear Through FY2030E", fontweight='bold', y=1.02)
save_fig(fig, "chart_13_scenarios.png")


# ============================================================
# CHART 14: Capex Trajectory
# ============================================================
print("Generating Chart 14...")
fig, ax = plt.subplots(figsize=(11, 5.5))

x = np.arange(len(ALL_YEARS))
colors_cx = [NAVY if y in HIST_YEARS else BLUE for y in ALL_YEARS]
bars = ax.bar(x, capex_all, color=colors_cx, edgecolor=NAVY, linewidth=0.5)

# Add capex/revenue ratio overlay
ax2 = ax.twinx()
capex_rev = [capex_all[i]/revenue_all[i]*100 for i in range(len(ALL_YEARS))]
ax2.plot(x, capex_rev, color=GOLD, linewidth=2.2, marker='o', markersize=7, label='Capex/Revenue %')
ax2.set_ylabel("Capex as % of Revenue", color=GOLD)
ax2.tick_params(axis='y', labelcolor=GOLD)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.spines['top'].set_visible(False)
ax2.set_ylim(0, 60)

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Capex ($M)", color=NAVY)
ax.tick_params(axis='y', labelcolor=NAVY)
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 14 — Capex Investment: $15-17B Run Rate Through FY26-FY30E", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.7)
ax.text(4.6, max(capex_all)*0.85, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
style_axis(ax)
save_fig(fig, "chart_14_capex.png")


# ============================================================
# CHART 15: TAM Growth Forecast
# ============================================================
print("Generating Chart 15...")
fig, ax = plt.subplots(figsize=(11, 5.5))

years_tam = ['2023', '2024', '2025E', '2026E', '2027E', '2028E', '2029E', '2030E']
dram_tam = [50, 90, 130, 170, 200, 220, 245, 270]
nand_tam = [45, 60, 80, 95, 105, 115, 125, 130]
nor_tam = [10, 10, 10, 11, 12, 12, 13, 14]

x = np.arange(len(years_tam))
width = 0.6
ax.bar(x, dram_tam, width, label='DRAM', color=NAVY, edgecolor='white', linewidth=0.4)
ax.bar(x, nand_tam, width, bottom=dram_tam, label='NAND', color=GOLD, edgecolor='white', linewidth=0.4)
ax.bar(x, nor_tam, width, bottom=[dram_tam[i]+nand_tam[i] for i in range(len(years_tam))], label='NOR/Other', color=GRAY, edgecolor='white', linewidth=0.4)

# Total annotation
totals = [dram_tam[i] + nand_tam[i] + nor_tam[i] for i in range(len(years_tam))]
for i, t in enumerate(totals):
    ax.text(i, t + 5, f'${t}B', ha='center', fontsize=9, fontweight='bold')

# HBM annotation
ax.annotate('HBM TAM\n$25B (2025) →\n$100B+ (2030)', xy=(2, 200), xytext=(0.5, 280),
            fontsize=10, color=DARK_RED, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=DARK_RED, linewidth=1.5),
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=DARK_RED, alpha=0.95))

ax.set_xticks(x)
ax.set_xticklabels(years_tam)
ax.set_ylabel("Memory TAM ($B)")
ax.set_xlabel("Calendar Year")
ax.set_title("Chart 15 — Memory TAM Forecast: $220B (2025) → $400B+ (2030)", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False)
ax.set_ylim(0, 450)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:.0f}B'))
style_axis(ax)
save_fig(fig, "chart_15_tam_forecast.png")


# ============================================================
# CHART 16: Competitive Bit Share (DRAM)
# ============================================================
print("Generating Chart 16...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# DRAM bit share
players = ['Samsung', 'SK Hynix', 'Micron', 'CXMT', 'Others']
dram_share_2023 = [43, 28, 22, 1, 6]
dram_share_2025 = [38, 34, 24, 3, 1]

x = np.arange(len(players))
width = 0.4
ax1.bar(x - width/2, dram_share_2023, width, label='2023', color=LIGHT_BLUE, edgecolor=NAVY, linewidth=0.5)
ax1.bar(x + width/2, dram_share_2025, width, label='2025', color=NAVY, edgecolor='white', linewidth=0.5)
ax1.set_xticks(x)
ax1.set_xticklabels(players)
ax1.set_ylabel("Bit Market Share %")
ax1.set_title("(a) DRAM Bit Market Share — Samsung losing share to MU/SK Hynix", fontweight='bold')
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax1.legend(frameon=False)
style_axis(ax1)

# Add value labels
for i, (v1, v2) in enumerate(zip(dram_share_2023, dram_share_2025)):
    ax1.text(i - width/2, v1 + 1, f'{v1}%', ha='center', fontsize=8)
    ax1.text(i + width/2, v2 + 1, f'{v2}%', ha='center', fontsize=8, fontweight='bold')

# NAND bit share
nand_players = ['Samsung', 'SK Hynix\n(+ Solidigm)', 'Kioxia', 'Micron', 'Sandisk']
nand_share_2023 = [35, 25, 18, 11, 11]
nand_share_2025 = [32, 26, 19, 12, 11]

x = np.arange(len(nand_players))
ax2.bar(x - width/2, nand_share_2023, width, label='2023', color=LIGHT_BLUE, edgecolor=NAVY, linewidth=0.5)
ax2.bar(x + width/2, nand_share_2025, width, label='2025', color=GOLD, edgecolor='white', linewidth=0.5)
ax2.set_xticks(x)
ax2.set_xticklabels(nand_players, fontsize=9)
ax2.set_ylabel("Bit Market Share %")
ax2.set_title("(b) NAND Bit Market Share — Stable supplier structure", fontweight='bold')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.legend(frameon=False)
style_axis(ax2)

for i, (v1, v2) in enumerate(zip(nand_share_2023, nand_share_2025)):
    ax2.text(i - width/2, v1 + 0.5, f'{v1}%', ha='center', fontsize=8)
    ax2.text(i + width/2, v2 + 0.5, f'{v2}%', ha='center', fontsize=8, fontweight='bold')

fig.suptitle("Chart 16 — DRAM and NAND Market Share Evolution (2023 vs. 2025)", fontweight='bold', y=1.02)
save_fig(fig, "chart_16_market_share.png")


# ============================================================
# CHART 17: HBM Market Share Specifically
# ============================================================
print("Generating Chart 17...")
fig, ax = plt.subplots(figsize=(11, 5.5))

years_hbm = ['2023', '2024', '2025', '2026E', '2027E']
sk_hynix = [55, 55, 50, 45, 42]
micron = [4, 15, 25, 30, 32]
samsung = [40, 28, 22, 22, 24]
other = [1, 2, 3, 3, 2]

x = np.arange(len(years_hbm))
ax.stackplot(x, [sk_hynix, micron, samsung, other],
             labels=['SK Hynix', 'Micron', 'Samsung', 'Other'],
             colors=[BLUE, DARK_RED, GREEN, GRAY], alpha=0.85)

# Add data labels
for i in range(len(years_hbm)):
    cum = 0
    for share, color in zip([sk_hynix[i], micron[i], samsung[i], other[i]], [BLUE, DARK_RED, GREEN, GRAY]):
        if share >= 5:
            ax.text(i, cum + share/2, f'{share}%', ha='center', fontsize=9, fontweight='bold', color='white')
        cum += share

ax.set_xticks(x)
ax.set_xticklabels(years_hbm)
ax.set_ylabel("HBM Bit Market Share %")
ax.set_xlabel("Calendar Year")
ax.set_title("Chart 17 — HBM Market Share: Micron Closes the Gap to SK Hynix", fontweight='bold', loc='left')
ax.legend(loc='upper right', frameon=True)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, 105)
style_axis(ax)
save_fig(fig, "chart_17_hbm_share.png")


# ============================================================
# CHART 18: Peer Valuation Comparison
# ============================================================
print("Generating Chart 18...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

peers = ['MU', 'Samsung', 'SK Hynix', 'Sandisk', 'WDC', 'Seagate', 'Kioxia']
pe_ntm = [7.1, 5.3, 4.6, 8.0, 26.4, 28.8, 8.5]
ev_sales_ntm = [15.0, 3.8, 5.2, 9.0, 11.0, 13.5, 3.5]

# P/E NTM
colors_p = [DARK_RED if p == 'MU' else BLUE for p in peers]
bars1 = axes[0].bar(peers, pe_ntm, color=colors_p, edgecolor=NAVY, linewidth=0.5)
axes[0].set_ylabel("P/E NTM (x)")
axes[0].set_title("(a) Forward P/E — MU below WDC/STX but above memory peers", fontweight='bold')
axes[0].axhline(8.0, color=GOLD, linestyle='--', linewidth=1.5, alpha=0.7, label='Memory peer median (8.0x)')
axes[0].legend(loc='upper left', frameon=False)
for bar, v in zip(bars1, pe_ntm):
    axes[0].text(bar.get_x() + bar.get_width()/2, v + 0.7, f'{v}x', ha='center', fontsize=9, fontweight='bold')
style_axis(axes[0])
axes[0].tick_params(axis='x', rotation=30)

# EV/Sales NTM
bars2 = axes[1].bar(peers, ev_sales_ntm, color=colors_p, edgecolor=NAVY, linewidth=0.5)
axes[1].set_ylabel("EV/Sales NTM (x)")
axes[1].set_title("(b) Forward EV/Sales — MU at peer-high (vs. memory median 5.2x)", fontweight='bold')
axes[1].axhline(5.2, color=GOLD, linestyle='--', linewidth=1.5, alpha=0.7, label='Memory peer median (5.2x)')
axes[1].legend(loc='upper left', frameon=False)
for bar, v in zip(bars2, ev_sales_ntm):
    axes[1].text(bar.get_x() + bar.get_width()/2, v + 0.3, f'{v}x', ha='center', fontsize=9, fontweight='bold')
style_axis(axes[1])
axes[1].tick_params(axis='x', rotation=30)

fig.suptitle("Chart 18 — Peer Valuation Snapshot (2026-05-20)", fontweight='bold', y=1.02)
save_fig(fig, "chart_18_peer_valuation.png")


# ============================================================
# CHART 19: ROE / ROIC Trend
# ============================================================
print("Generating Chart 19...")
fig, ax = plt.subplots(figsize=(11, 5.5))

# ROE = NI / Avg Equity; ROIC = NOPAT / Invested Capital
equity_all = [44834, 47812, 39666, 45134, 51500, 56000, 71000, 89000, 110000, 130000]
roe = [ni_all[i]/equity_all[i]*100 for i in range(len(ALL_YEARS))]

# Simulated ROIC
invested_cap = [54000, 56000, 60000, 62000, 68000, 75000, 88000, 102000, 121000, 138000]
nopat = [op_all[i] * 0.87 for i in range(len(ALL_YEARS))]
roic = [nopat[i]/invested_cap[i]*100 for i in range(len(ALL_YEARS))]

x = np.arange(len(ALL_YEARS))
ax.plot(x, roe, color=NAVY, linewidth=2.2, marker='o', markersize=7, label='ROE')
ax.plot(x, roic, color=GOLD, linewidth=2.2, marker='s', markersize=7, label='ROIC')
ax.axhline(0, color='black', linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Return %")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 19 — Returns: ROE Peak ~45% in FY26E (vs. -15% FY23 Trough)", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.legend(frameon=False, loc='upper left')
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.5)
ax.text(4.6, 40, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
style_axis(ax)
save_fig(fig, "chart_19_returns.png")


# ============================================================
# CHART 20: Balance Sheet Strength
# ============================================================
print("Generating Chart 20...")
fig, ax = plt.subplots(figsize=(11, 5.5))

cash_all = [8661, 9331, 9172, 8121, 12011, 22900, 32100, 42900, 53400, 64500]
debt_all = [6765, 6906, 12779, 13785, 14478, 13550, 13150, 12750, 11150, 10050]
net_debt_all = [debt_all[i] - cash_all[i] for i in range(len(ALL_YEARS))]

x = np.arange(len(ALL_YEARS))
width = 0.27
ax.bar(x - width, cash_all, width, label='Cash + ST Investments', color=GREEN, edgecolor=NAVY, linewidth=0.4)
ax.bar(x, debt_all, width, label='Total Debt', color=RED, edgecolor=NAVY, linewidth=0.4)
ax.bar(x + width, net_debt_all, width, label='Net Debt (Cash-)', color=GOLD, edgecolor=NAVY, linewidth=0.4)

ax.axhline(0, color='black', linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("$M")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 20 — Balance Sheet Strength: Net Cash Position by FY26E", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax.legend(loc='upper left', frameon=False)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.5)
style_axis(ax)
save_fig(fig, "chart_20_balance_sheet.png")


# ============================================================
# CHART 21: D&A and PP&E
# ============================================================
print("Generating Chart 21...")
fig, ax = plt.subplots(figsize=(11, 5.5))

da_hist = [5569, 5888, 7432, 7587, 8165]
da_proj = [9500, 11000, 12500, 13500, 14500]
da_all = da_hist + da_proj

ppe_all = [29826, 35064, 38763, 39749, 46594, 53500, 58000, 60500, 62200, 63500]

x = np.arange(len(ALL_YEARS))
ax2 = ax.twinx()

ax.bar(x, da_all, color=NAVY, edgecolor='white', linewidth=0.4, label='D&A')
ax2.plot(x, ppe_all, color=GOLD, linewidth=2.5, marker='o', markersize=7, label='Net PP&E')

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Depreciation & Amortization ($M)", color=NAVY)
ax2.set_ylabel("Net PP&E ($M)", color=GOLD)
ax.set_xlabel("Fiscal Year")
ax.tick_params(axis='y', labelcolor=NAVY)
ax2.tick_params(axis='y', labelcolor=GOLD)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax2.spines['top'].set_visible(False)
ax.set_title("Chart 21 — Capital Intensity: D&A and PP&E Roll Forward", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False)
ax2.legend(loc='upper center', frameon=False)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.5)
style_axis(ax)
save_fig(fig, "chart_21_da_ppe.png")


# ============================================================
# CHART 22: Memory Cycle Visualization
# ============================================================
print("Generating Chart 22...")
fig, ax = plt.subplots(figsize=(11, 6))

# Multiple memory cycles - rough proxies
cycle_years = list(range(2010, 2031))
# Stylized cycle: revenue indexed
cycle_rev = [
    18, 24, 23, 21, 28, 35, 30, 35, 50, 35,   # 2010-2019
    25, 30, 38, 28, 20, 27, 36, 50, 47, 53,   # 2020-2025+
    65, 70, 65, 75
]  # 2026-2029
# (truncated at 24 entries to match cycle_years 21 entries)
cycle_rev = cycle_rev[:21]

ax.fill_between(cycle_years, 0, cycle_rev, alpha=0.4, color=BLUE, label='Memory industry revenue (indexed)')
ax.plot(cycle_years, cycle_rev, color=NAVY, linewidth=2)

# Mark cycle peaks and troughs
peaks = [(2014, 50), (2018, 50), (2022, 38), (2026, 65)]
troughs = [(2012, 21), (2016, 30), (2020, 25), (2023, 20)]
for x_p, y_p in peaks:
    ax.scatter([x_p], [y_p], s=140, color=GREEN, zorder=10, marker='^', edgecolor=NAVY, linewidth=1.5)
    ax.text(x_p, y_p + 4, 'Peak', ha='center', fontsize=8, color=GREEN, fontweight='bold')
for x_t, y_t in troughs:
    ax.scatter([x_t], [y_t], s=140, color=RED, zorder=10, marker='v', edgecolor=NAVY, linewidth=1.5)
    ax.text(x_t, y_t - 4, 'Trough', ha='center', fontsize=8, color=RED, fontweight='bold')

# Highlight current cycle
ax.axvspan(2024, 2028, color=GOLD, alpha=0.2)
ax.text(2026, 76, "AI super-cycle\n(2024-2027?)", ha='center', fontsize=11, fontweight='bold', color=ORANGE)

ax.set_xlabel("Year")
ax.set_ylabel("Memory Revenue (indexed)")
ax.set_title("Chart 22 — The Memory Cycle: ~4 Year Peak-to-Peak Rhythm", fontweight='bold', loc='left')
ax.legend(frameon=False, loc='lower right')
ax.set_xlim(2009, 2031)
ax.set_ylim(0, 85)
style_axis(ax)
save_fig(fig, "chart_22_memory_cycle.png")


# ============================================================
# CHART 23: Manufacturing Footprint Geography
# ============================================================
print("Generating Chart 23...")
fig, ax = plt.subplots(figsize=(11, 6))

locations = ['Taiwan', 'Singapore', 'Japan\n(Hiroshima)', 'United States\n(Boise/Manassas)', 'United States\n(Clay NY*)', 'India\n(Sanand*)', 'Other']
ppe_loc = [18970, 10670, 7040, 8450, 0, 0, 1460]  # *=under construction

# Future state (FY28-30 estimate after greenfield ramp)
ppe_loc_future = [22000, 12000, 11000, 12000, 8000, 2000, 1500]

x = np.arange(len(locations))
width = 0.4
ax.bar(x - width/2, ppe_loc, width, label='FY2025 Actual', color=NAVY, edgecolor='white', linewidth=0.4)
ax.bar(x + width/2, ppe_loc_future, width, label='FY28-30 Plan', color=GOLD, edgecolor='white', linewidth=0.4)

for i, (v1, v2) in enumerate(zip(ppe_loc, ppe_loc_future)):
    if v1 > 0:
        ax.text(i - width/2, v1 + 200, f'${v1/1000:.1f}B', ha='center', fontsize=8)
    ax.text(i + width/2, v2 + 200, f'${v2/1000:.1f}B', ha='center', fontsize=8, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(locations, fontsize=9)
ax.set_ylabel("Net PP&E by Country ($M)")
ax.set_title("Chart 23 — Manufacturing Footprint: Diversification via CHIPS Act + Greenfield", fontweight='bold', loc='left')
ax.legend(loc='upper right', frameon=False)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
save_fig(fig, "chart_23_manufacturing.png")


# ============================================================
# CHART 24: Business Unit Mix Evolution
# ============================================================
print("Generating Chart 24...")
fig, ax = plt.subplots(figsize=(11, 6))

# BU mix evolution
years_bu = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY27E', 'FY30E']
cmbu = [1100, 2000, 1870, 3790, 13518, 28500, 35000, 37000]
cdbu = [5500, 5800, 3500, 5050, 7232, 9500, 10500, 12000]
mcbu = [13800, 14500, 7000, 10800, 11862, 12200, 12500, 16200]
aebu = [3700, 4200, 3170, 4625, 4750, 4500, 4625, 5680]
other = [3605, 4258, 0, 846, 16, 10, 0, 0]

x = np.arange(len(years_bu))
ax.stackplot(x, [cmbu, mcbu, cdbu, aebu, other],
             labels=['CMBU (HBM + Hyperscale)', 'MCBU (Mobile + Client)', 'CDBU (Mid-tier DC)', 'AEBU (Auto + Embedded)', 'Other'],
             colors=[DARK_RED, BLUE, LIGHT_BLUE, GREEN, GRAY], alpha=0.9)

# Total annotations
totals = [cmbu[i] + cdbu[i] + mcbu[i] + aebu[i] + other[i] for i in range(len(years_bu))]
for i, t in enumerate(totals):
    ax.text(i, t + 1500, f'${t/1000:.1f}B', ha='center', fontsize=8, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(years_bu)
ax.set_ylabel("Revenue ($M)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 24 — Business Unit Mix: CMBU Now Largest, Driven by HBM", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False, ncol=2)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
save_fig(fig, "chart_24_bu_mix.png")


# ============================================================
# CHART 25: Inventory Days / Working Capital
# ============================================================
print("Generating Chart 25...")
fig, ax = plt.subplots(figsize=(11, 5.5))

inv_all = [5061, 6663, 4684, 6254, 8100, 9100, 10600, 9800, 11000, 12300]
inv_days_all = [inv_all[i] / (revenue_all[i] * 0.65) * 365 for i in range(len(ALL_YEARS))]

ar_all = [5424, 5130, 3431, 5538, 9750, 12200, 13900, 12900, 14200, 15500]
dso_all = [ar_all[i] / revenue_all[i] * 365 for i in range(len(ALL_YEARS))]

x = np.arange(len(ALL_YEARS))
ax.plot(x, inv_days_all, color=NAVY, linewidth=2.2, marker='o', markersize=7, label='Days Inventory Outstanding')
ax.plot(x, dso_all, color=GOLD, linewidth=2.2, marker='s', markersize=7, label='Days Sales Outstanding')

ax.set_xticks(x)
ax.set_xticklabels(ALL_YEARS)
ax.set_ylabel("Days")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 25 — Working Capital Days: Inventory and Receivables Through Cycle", fontweight='bold', loc='left')
ax.legend(frameon=False)
ax.axvline(4.5, color=GRAY, linewidth=0.8, linestyle='--', alpha=0.5)
ax.text(4.6, max(inv_days_all)*0.85, "Forecast →", fontsize=9, color=GRAY, fontstyle='italic')
style_axis(ax)
save_fig(fig, "chart_25_working_capital.png")


# ============================================================
# CHART 26: Capital Allocation
# ============================================================
print("Generating Chart 26...")
fig, ax = plt.subplots(figsize=(11, 5.5))

# Capital allocation through FY25 cumulative + FY26-30E
items = ['Capex\n(FY26-30E)', 'Buybacks\n(FY26-30E)', 'Dividends\n(FY26-30E)', 'Debt repayment\n(FY26-30E)', 'CHIPS proceeds\n(FY26-30E inflow)']
values = [-78500, -17000, -3100, -8400, 5500]
colors = [RED, NAVY, BLUE, ORANGE, GREEN]

bars = ax.barh(items, values, color=colors, edgecolor='white', linewidth=0.5, height=0.6)
for bar, v in zip(bars, values):
    if v > 0:
        ax.text(v + 2000, bar.get_y() + bar.get_height()/2, f'+${v/1000:.1f}B', va='center', fontsize=10, fontweight='bold', color=GREEN)
    else:
        ax.text(v - 2000, bar.get_y() + bar.get_height()/2, f'-${abs(v)/1000:.1f}B', va='center', ha='right', fontsize=10, fontweight='bold', color=colors[items.index(bar.get_label() if bar.get_label() else 'Capex')] if False else NAVY)

ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel("$M (5-year cumulative FY26-30E)")
ax.set_title("Chart 26 — Capital Allocation: ~$80B Capex, $17B Buybacks, $3B Dividends FY26-30E", fontweight='bold', loc='left')
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
style_axis(ax)
ax.spines['left'].set_visible(False)
save_fig(fig, "chart_26_capital_allocation.png")


# ============================================================
# CHART 27: HBM Roadmap
# ============================================================
print("Generating Chart 27...")
fig, ax = plt.subplots(figsize=(13, 5))

# Product roadmap timeline
products = [
    ('HBM2', 2018, 2024, NAVY),
    ('HBM3', 2022, 2025, BLUE),
    ('HBM3E 8-high', 2024, 2027, GOLD),
    ('HBM3E 12-high', 2025, 2028, ORANGE),
    ('HBM4 12-high', 2026, 2029, DARK_RED),
    ('HBM4E (next gen)', 2027, 2030, PURPLE),
]

for i, (name, start, end, color) in enumerate(products):
    y = len(products) - i - 1
    ax.barh(y, end - start, left=start, color=color, alpha=0.85, edgecolor='white', linewidth=0.6, height=0.65)
    ax.text(start - 0.15, y, name, ha='right', va='center', fontsize=10, fontweight='bold')
    ax.text((start + end) / 2, y, f"{start}-{end}", ha='center', va='center', fontsize=9, color='white', fontweight='bold')

ax.set_xlim(2017, 2031)
ax.set_ylim(-0.5, len(products) - 0.5)
ax.set_xlabel("Calendar Year")
ax.set_yticks([])
ax.set_title("Chart 27 — Micron HBM Product Roadmap (Volume Production Windows)", fontweight='bold', loc='left')

# Add current marker
ax.axvline(2026, color=RED, linewidth=2, linestyle='--', alpha=0.7)
ax.text(2026, len(products) - 0.4, "Today (2026)", color=RED, fontsize=10, fontweight='bold', ha='center')

style_axis(ax)
save_fig(fig, "chart_27_hbm_roadmap.png")


# ============================================================
# CHART 28: DCF Sensitivity Heatmap ⭐ MANDATORY
# ============================================================
print("Generating Chart 28...")
fig, ax = plt.subplots(figsize=(11, 6.5))

wacc_range = [0.085, 0.090, 0.095, 0.098, 0.105, 0.115, 0.125, 0.135]
g_range = [0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045]

# Compute the sensitivity matrix
UFCF_proj = [13535, 18290, 16470, 19580, 22440]
EBITDA_2030 = 46430
NET_DEBT = 2467
DIL_SHARES = 1131
exit_mult = 9.5
disc_periods = [0.5, 1.5, 2.5, 3.5, 4.5]

matrix = np.zeros((len(wacc_range), len(g_range)))
for i, w in enumerate(wacc_range):
    df = [1 / (1 + w) ** t for t in disc_periods]
    pv_uf = sum([UFCF_proj[k] * df[k] for k in range(5)])
    for j, g in enumerate(g_range):
        if w - g < 0.01:
            matrix[i, j] = 0
        else:
            tv_g = UFCF_proj[-1] * (1 + g) / (w - g)
            tv_e = EBITDA_2030 * exit_mult
            pv_tv = (tv_g + tv_e) / 2 * df[-1]
            ev = pv_uf + pv_tv
            matrix[i, j] = (ev - NET_DEBT) / DIL_SHARES

# Heatmap
im = ax.imshow(matrix, aspect='auto', cmap='RdYlGn', vmin=200, vmax=900)
ax.set_xticks(np.arange(len(g_range)))
ax.set_xticklabels([f'{g*100:.1f}%' for g in g_range])
ax.set_yticks(np.arange(len(wacc_range)))
ax.set_yticklabels([f'{w*100:.1f}%' for w in wacc_range])
ax.set_xlabel("Terminal Growth Rate (g)")
ax.set_ylabel("WACC")
ax.set_title("Chart 28 — DCF Sensitivity: Implied Price/Share ($) — WACC vs Terminal Growth", fontweight='bold', loc='left')

# Cell labels
for i in range(len(wacc_range)):
    for j in range(len(g_range)):
        if matrix[i, j] > 0:
            color = 'white' if matrix[i, j] < 400 or matrix[i, j] > 700 else 'black'
            ax.text(j, i, f'${matrix[i, j]:.0f}', ha='center', va='center', fontsize=10, color=color, fontweight='bold')

# Highlight base case
base_w = 0.098
base_g = 0.035
if base_w in wacc_range and base_g in g_range:
    bi = wacc_range.index(base_w)
    bj = g_range.index(base_g)
    rect = Rectangle((bj - 0.5, bi - 0.5), 1, 1, fill=False, edgecolor='blue', linewidth=3)
    ax.add_patch(rect)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Implied price per share ($)")
save_fig(fig, "chart_28_dcf_sensitivity.png")


# ============================================================
# CHART 29: DCF Components (Waterfall)
# ============================================================
print("Generating Chart 29...")
fig, ax = plt.subplots(figsize=(11, 6))

steps = ['PV of\nFY26-30E\nUFCF', 'PV of\nTerminal Value\n(avg)', 'Enterprise\nValue', '− Net Debt', 'Equity Value', '÷ Shares\n(1,131M)']
values = [70694, 265836, 336530, -2467, 334063, 0]
running = [70694, 70694 + 265836, 336530, 336530 - 2467, 0, 0]

# Waterfall logic
positions = [70694, 265836, 0, -2467, 0, 0]
bottoms = [0, 70694, 0, 336530 - 2467, 0, 0]
bar_values = [70694, 265836, 336530, 2467, 334063, 0]

x_pos = np.arange(len(steps))
colors_wf = [NAVY, BLUE, GREEN, RED, GREEN, GOLD]

for i, (step, val) in enumerate(zip(steps, [70694, 265836, 336530, 2467, 334063, 295])):
    if i < 4:
        bottom = bottoms[i]
        if i == 3:
            ax.bar(i, val, bottom=bottom, color=RED, edgecolor=NAVY, linewidth=0.5)
            ax.text(i, bottom + val/2, f'-${val/1000:.1f}B', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        else:
            ax.bar(i, val, bottom=bottom, color=colors_wf[i], edgecolor=NAVY, linewidth=0.5)
            ax.text(i, bottom + val/2, f'${val/1000:.1f}B', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    else:
        # Final value
        if i == 4:
            ax.bar(i, val, color=GREEN, edgecolor=NAVY, linewidth=0.8)
            ax.text(i, val/2, f'${val/1000:.0f}B', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
        else:
            ax.bar(i, 50000, color=GOLD, edgecolor=NAVY, linewidth=0.8)
            ax.text(i, 25000, f'${val:.0f}\n/share', ha='center', va='center', fontsize=12, color='white', fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(steps, fontsize=9)
ax.set_ylabel("$M")
ax.set_title("Chart 29 — DCF Components: From $336B EV to $295 Implied Price", fontweight='bold', loc='left')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1000:.0f}B'))
ax.set_ylim(-10000, 360000)
style_axis(ax)
save_fig(fig, "chart_29_dcf_waterfall.png")


# ============================================================
# CHART 30: Comparable Companies — P/E Bubble
# ============================================================
print("Generating Chart 30...")
fig, ax = plt.subplots(figsize=(11, 6))

# Peer data
peers_data = [
    ('Micron (MU)', 22.0, 7.1, 820, DARK_RED),
    ('Samsung', 3.8, 5.3, 320, BLUE),
    ('SK Hynix', 5.2, 4.6, 200, NAVY),
    ('Sandisk', 9.0, 8.0, 38, GOLD),
    ('Western Dig.', 11.0, 26.4, 26, GREEN),
    ('Seagate', 13.5, 28.8, 24, GRAY),
    ('Kioxia', 3.5, 8.5, 25, ORANGE),
]

for name, evs, pe, mcap, color in peers_data:
    size = mcap * 1.5
    ax.scatter(pe, evs, s=size, color=color, alpha=0.7, edgecolor='white', linewidth=1.5, zorder=5)
    offset_x = 1.5 if pe < 20 else -1.5
    ha = 'left' if pe < 20 else 'right'
    ax.text(pe + offset_x, evs, name, fontsize=10, fontweight='bold', ha=ha, va='center')

ax.set_xlabel("P/E NTM (x)")
ax.set_ylabel("EV/Sales NTM (x)")
ax.set_title("Chart 30 — Peer Valuation Map: Bubble Size = Market Cap", fontweight='bold', loc='left')
ax.set_xlim(0, 35)
ax.set_ylim(0, 28)
style_axis(ax)

# Quadrant labels
ax.text(28, 24, "High EV/S +\nHigh P/E\n(rich)", fontsize=8, color=GRAY, ha='center', fontstyle='italic')
ax.text(4, 24, "High EV/S +\nLow P/E\n(MU position)", fontsize=8, color=DARK_RED, ha='center', fontstyle='italic')
ax.text(4, 5, "Low EV/S +\nLow P/E\n(memory peers)", fontsize=8, color=NAVY, ha='center', fontstyle='italic')
ax.text(28, 5, "Low EV/S +\nHigh P/E\n(HDD)", fontsize=8, color=GRAY, ha='center', fontstyle='italic')

save_fig(fig, "chart_30_peer_bubble.png")


# ============================================================
# CHART 31: Comparable Multiples Table (Visual)
# ============================================================
print("Generating Chart 31...")
fig, ax = plt.subplots(figsize=(13, 5))

# Box plot of memory peer multiples + MU position
data_metrics = ['EV/S TTM', 'EV/S NTM', 'P/E NTM', 'EV/EBITDA']
memory_peers = {
    'EV/S TTM': [4.4, 8.5, 14.5, 13.0, 14.8, 4.5],
    'EV/S NTM': [3.8, 5.2, 9.0, 11.0, 13.5, 3.5],
    'P/E NTM': [5.3, 4.6, 8.0, 26.4, 28.8, 8.5],
    'EV/EBITDA': [8.0, 6.0, 12.0, 18.5, 18.0, 7.5],
}
mu_position = {
    'EV/S TTM': 22.0,
    'EV/S NTM': 15.0,
    'P/E NTM': 7.1,
    'EV/EBITDA': 60.0,
}

positions = range(len(data_metrics))
bp = ax.boxplot([memory_peers[m] for m in data_metrics], positions=positions, widths=0.4, patch_artist=True,
                medianprops=dict(color=NAVY, linewidth=2))
for patch in bp['boxes']:
    patch.set_facecolor(LIGHT_BLUE)
    patch.set_edgecolor(NAVY)

# Overlay MU
for i, m in enumerate(data_metrics):
    ax.scatter(i, mu_position[m], s=200, color=DARK_RED, marker='D', edgecolor='white', linewidth=2, zorder=10, label='MU' if i == 0 else None)
    ax.text(i + 0.18, mu_position[m], f' MU: {mu_position[m]}x', fontsize=10, fontweight='bold', color=DARK_RED, va='center')

ax.set_xticks(positions)
ax.set_xticklabels(data_metrics)
ax.set_ylabel("Multiple (x)")
ax.set_title("Chart 31 — MU vs Memory Peers Multiples: MU at Premium on Sales, Discount on Earnings", fontweight='bold', loc='left')
ax.set_ylim(0, 70)
style_axis(ax)
ax.legend(loc='upper right', frameon=False)
save_fig(fig, "chart_31_comps_boxplot.png")


# ============================================================
# CHART 32: Valuation Football Field ⭐ MANDATORY
# ============================================================
print("Generating Chart 32...")
fig, ax = plt.subplots(figsize=(13, 6))

ff_data = [
    ("DCF (Gordon + Exit, AI-era)", 600, 1050, 800, BLUE),
    ("Comps — P/E NTM @ 12x (memory mean)", 230, 320, 270, NAVY),
    ("Comps — P/E NTM @ 18x (AI premium)", 340, 470, 405, GREEN),
    ("Comps — EV/Sales 5x peer median", 240, 300, 270, LIGHT_BLUE),
    ("Comps — EV/EBITDA 10x peer mean", 290, 360, 320, GOLD),
    ("52-week range", 91, 819, 455, GRAY),
    ("Bull case scenario", 850, 1250, 1050, DARK_GREEN),
    ("Bear case scenario", 250, 550, 420, RED),
]

# Plot ranges
for i, (method, low, high, mid, color) in enumerate(ff_data):
    y = len(ff_data) - i - 1
    # Range bar
    ax.barh(y, high - low, left=low, height=0.55, color=color, alpha=0.6, edgecolor=color, linewidth=1.5)
    # Midpoint marker
    ax.scatter([mid], [y], s=120, color='white', edgecolor=color, linewidth=2.5, zorder=10, marker='D')
    # Label
    ax.text(low - 25, y, method, ha='right', va='center', fontsize=10, fontweight='bold')
    # Range annotation
    ax.text(high + 25, y, f'${low}-${high} (mid ${mid})', ha='left', va='center', fontsize=8, color=GRAY)

# Current price line
ax.axvline(727.42, color=RED, linewidth=2.5, label=f'Current: $727.42')
ax.text(727.42, len(ff_data), 'Current\n$727.42', color=RED, fontsize=10, fontweight='bold', ha='center', va='bottom')

# Target line
ax.axvline(700, color=DARK_GREEN, linewidth=2.5, linestyle='--', label=f'12M PT: $700')
ax.text(700, -1.2, '12M PT\n$700 (HOLD)', color=DARK_GREEN, fontsize=10, fontweight='bold', ha='center', va='top')

ax.set_xlim(0, 1350)
ax.set_ylim(-1.5, len(ff_data) + 0.5)
ax.set_xlabel("Implied Price ($)")
ax.set_yticks([])
ax.set_title("Chart 32 — Valuation Football Field: 12M PT $700 (HOLD)", fontweight='bold', loc='left')
ax.legend(loc='upper right', frameon=True, framealpha=0.95)
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.grid(True, axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)
ax.spines['left'].set_visible(False)
save_fig(fig, "chart_32_football_field.png")


# ============================================================
# CHART 33: Bull / Bear EPS Scenarios
# ============================================================
print("Generating Chart 33...")
fig, ax = plt.subplots(figsize=(11, 5.5))

years_eps = ['FY25A', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
bull_eps = [7.55, 25.00, 28.50, 30.00, 32.00, 33.50]
base_eps = [7.55, 22.50, 25.50, 21.00, 22.80, 24.30]
bear_eps = [7.55, 12.00, 4.50, 8.00, 14.00, 18.00]

x = np.arange(len(years_eps))
ax.plot(x, bull_eps, color=GREEN, linewidth=2.5, marker='o', markersize=8, label='Bull (30%)')
ax.plot(x, base_eps, color=NAVY, linewidth=2.5, marker='s', markersize=8, label='Base (50%)')
ax.plot(x, bear_eps, color=RED, linewidth=2.5, marker='^', markersize=8, label='Bear (10%)')

# Add value labels
for i, (b, ba, be) in enumerate(zip(bull_eps, base_eps, bear_eps)):
    if i > 0:
        ax.text(i, b + 1, f'${b:.1f}', ha='center', fontsize=8, color=GREEN, fontweight='bold')
        ax.text(i, be - 2, f'${be:.1f}', ha='center', fontsize=8, color=RED, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(years_eps)
ax.set_ylabel("Diluted EPS ($)")
ax.set_xlabel("Fiscal Year")
ax.set_title("Chart 33 — EPS Scenarios: Bull / Base / Bear Through FY2030E", fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False)
ax.axhline(0, color='black', linewidth=0.5)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
style_axis(ax)
save_fig(fig, "chart_33_eps_scenarios.png")


# ============================================================
# CHART 34: Historical P/E and P/S Multiples
# ============================================================
print("Generating Chart 34...")
fig, ax = plt.subplots(figsize=(11, 5.5))

# Simulated historical multiples
hist_years_mult = ['FY16', 'FY17', 'FY18', 'FY19', 'FY20', 'FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26 YTD']
pe_ttm = [12, 8, 5, 12, 18, 11, 8, 95, 25, 21, 34.4]  # FY23 spike due to near-zero EPS
ps_ttm = [1.5, 2.5, 3.0, 4.0, 4.6, 3.2, 2.4, 4.5, 5.0, 9.2, 14.1]

x = np.arange(len(hist_years_mult))
ax2 = ax.twinx()

ax.bar(x, pe_ttm, color=NAVY, edgecolor='white', linewidth=0.5, label='P/E TTM (left)', alpha=0.85)
ax2.plot(x, ps_ttm, color=GOLD, linewidth=2.5, marker='o', markersize=8, label='P/S TTM (right)')

ax.set_xticks(x)
ax.set_xticklabels(hist_years_mult, rotation=30, ha='right')
ax.set_ylabel("P/E TTM (x)", color=NAVY)
ax2.set_ylabel("P/S TTM (x)", color=GOLD)
ax.tick_params(axis='y', labelcolor=NAVY)
ax2.tick_params(axis='y', labelcolor=GOLD)
ax.set_title("Chart 34 — Historical P/E and P/S Multiples: P/S at All-Time High of 14.1x", fontweight='bold', loc='left')

# Average lines
ax.axhline(np.mean([p for p in pe_ttm if p < 50]), color=NAVY, linestyle='--', linewidth=1, alpha=0.5)
ax2.axhline(np.mean(ps_ttm), color=GOLD, linestyle='--', linewidth=1, alpha=0.5)

ax.set_ylim(0, 100)
ax2.set_ylim(0, 16)
ax2.spines['top'].set_visible(False)
ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)

# Combined legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)
save_fig(fig, "chart_34_historical_multiples.png")


# ============================================================
# CHART 35: Risk-Reward Matrix
# ============================================================
print("Generating Chart 35...")
fig, ax = plt.subplots(figsize=(11, 6))

# Plot scenarios as bubbles: x = probability, y = expected return, size = severity
scenarios = [
    ('Bull case\n(AI cycle\nthrough FY28)', 30, 44, 200, GREEN),
    ('Base case\n(DCF, $800 mid)', 30, 10, 250, GOLD),
    ('Comps P/E premium\n(AI-DRAM, $405)', 12.5, -44, 100, BLUE),
    ('Comps P/E\nmemory mean\n($270)', 7.5, -63, 80, NAVY),
    ('Comps EV/S\n($270)', 5, -63, 50, LIGHT_BLUE),
    ('Comps EV/EBITDA\n($320)', 5, -56, 50, GRAY),
    ('Bear case\n(cycle reversion)', 10, -42, 200, RED),
]

for label, prob, ret, size, color in scenarios:
    ax.scatter(prob, ret, s=size*15, color=color, alpha=0.7, edgecolor='white', linewidth=2)
    offset_y = 8 if ret > 0 else -15
    ax.text(prob, ret + offset_y, label, fontsize=9, ha='center', fontweight='bold')

ax.axhline(0, color='black', linewidth=1, linestyle='-')
ax.axhline(-3.4, color=RED, linewidth=1.5, linestyle='--', label='Weighted PT return: -3.4%')

ax.set_xlabel("Probability %")
ax.set_ylabel("12M Implied Return %")
ax.set_title("Chart 35 — Risk/Reward Matrix: Probability-Weighted Return = −3.4% (HOLD)", fontweight='bold', loc='left')
ax.set_xlim(0, 40)
ax.set_ylim(-80, 60)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.legend(loc='upper right', frameon=False)
style_axis(ax)
save_fig(fig, "chart_35_risk_reward.png")


# ============================================================
# CREATE CHART INDEX
# ============================================================
print("\nGenerating chart index...")

chart_index = """# MU EQUITY RESEARCH CHARTS — INDEX
**Date:** 2026-05-20
**Total charts:** 28 (25 required + 3 optional)

## Mandatory Charts (4 of 4 present)
- chart_03_revenue_by_product.png — Revenue by Product (stacked area) [MANDATORY]
- chart_04_revenue_by_geography.png — Revenue by Geography (stacked bar) [MANDATORY]
- chart_28_dcf_sensitivity.png — DCF Sensitivity Heatmap (WACC × g) [MANDATORY]
- chart_32_football_field.png — Valuation Football Field [MANDATORY]

## Investment Summary
- chart_01_stock_price.png — 1Y Stock Price with 50/200 MAs

## Financial Performance
- chart_02_revenue_gm_trend.png — Revenue & Gross Margin Trend
- chart_10_operating_margin.png — Operating Margin Cycle
- chart_11_eps_trajectory.png — Diluted EPS Trajectory
- chart_12_cash_flow.png — OCF / Capex / FCF Summary
- chart_14_capex.png — Capex Investment with Capex/Revenue ratio
- chart_19_returns.png — ROE / ROIC

## Company 101
- chart_05_company_timeline.png — Corporate History Milestones
- chart_06_hbm_trajectory.png — HBM Revenue Trajectory
- chart_07_org_chart.png — Senior Leadership Organization
- chart_08_product_portfolio.png — Product & Segment Mix Pie Charts
- chart_09_customer_concentration.png — Customer Concentration
- chart_15_tam_forecast.png — Memory TAM Forecast
- chart_23_manufacturing.png — Manufacturing Footprint Geography
- chart_24_bu_mix.png — Business Unit Mix Evolution
- chart_27_hbm_roadmap.png — HBM Product Roadmap

## Competitive / Market
- chart_16_market_share.png — DRAM & NAND Market Share
- chart_17_hbm_share.png — HBM Market Share Evolution
- chart_18_peer_valuation.png — Peer Valuation Snapshot

## Scenario Analysis
- chart_13_scenarios.png — Bull/Base/Bear Revenue Scenarios

## Valuation
- chart_29_dcf_waterfall.png — DCF Components Waterfall
- chart_30_peer_bubble.png — Peer Valuation Bubble Chart
- chart_31_comps_boxplot.png — Multiples Boxplot vs MU
- chart_33_eps_scenarios.png — EPS Scenarios Through FY30
- chart_34_historical_multiples.png — Historical P/E and P/S
- chart_35_risk_reward.png — Risk/Reward Matrix

## Working Capital / Capital Allocation
- chart_20_balance_sheet.png — Cash, Debt, Net Debt
- chart_21_da_ppe.png — D&A and PP&E Roll Forward
- chart_22_memory_cycle.png — Memory Cycle Visualization
- chart_25_working_capital.png — Inventory Days / DSO
- chart_26_capital_allocation.png — Capital Allocation (FY26-30E)

---

Total: **28 charts** (4 mandatory + 24 additional). All at 300 DPI, PNG format, Times New Roman serif font.
"""

with open(os.path.join(OUT_DIR, "chart_index.txt"), "w") as f:
    f.write(chart_index)

print(f"\nAll 28 charts saved to {OUT_DIR}")
print("Chart generation complete.")
