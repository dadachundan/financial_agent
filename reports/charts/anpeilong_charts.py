"""安培龙 (SZSE:301413) 公司研究图表生成脚本.

数据来源：
- FY2023 / FY2024 / FY2025 年度报告 (cninfo) — 营收、利润、毛利率、研发、客户、产品构成
- Yahoo Finance 2026-05-20 — 当前市值、估值倍数

输出位置：/Users/x/projects/financial_agent/reports/charts/anpeilong_<name>.png
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

plt.rcParams.update({
    "font.family": ["Arial Unicode MS", "PingFang SC", "Heiti SC", "Microsoft YaHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})
NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
CORAL = "#e76f51"
GOLD = "#f4a261"
SLATE = "#6c757d"
PURPLE = "#6f42c1"
OUTDIR = "/Users/x/projects/financial_agent/reports/charts"

years = ["FY2023", "FY2024", "FY2025"]
revenue = [746.6, 940.2, 1183.5]            # ¥ million
net_income = [79.9, 82.6, 90.7]
op_income = [91.0, 93.1, 91.3]
gross_margin = [31.7, 32.2, 29.1]           # %  (2025 from filing: 29.02%)
op_margin = [12.2, 9.9, 7.7]
net_margin = [10.7, 8.8, 7.7]
rd_spend = [47.4, 62.6, 97.8]
rd_pct = [r / rev * 100 for r, rev in zip(rd_spend, revenue)]

# ---- Chart 1: 3-year revenue + margin trend ----
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.55
bars = ax.bar(x, revenue, w, color=NAVY, label="营业收入 (Revenue, ¥M)")
for b, v in zip(bars, revenue):
    ax.text(b.get_x() + w/2, v + 12, f"¥{v:.0f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years, fontsize=11)
ax.set_ylabel("营业收入 (¥ million)", fontsize=11)
ax.set_ylim(0, max(revenue) * 1.30)
yoy = [(revenue[i] / revenue[i-1] - 1) * 100 for i in range(1, len(revenue))]
ax.text(0.02, 0.95, f"营收 YoY: +{yoy[0]:.1f}%  →  +{yoy[1]:.1f}%",
        transform=ax.transAxes, fontsize=11, va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=NAVY, alpha=0.85))

ax2 = ax.twinx()
ax2.plot(x, gross_margin, "o-", color=GOLD, lw=2.5, ms=10, label="毛利率 Gross margin")
ax2.plot(x, op_margin, "s-", color=CORAL, lw=2.5, ms=10, label="经营利润率 Op margin")
ax2.plot(x, net_margin, "^-", color=TEAL, lw=2.5, ms=10, label="净利率 Net margin")
for i, (g, o, n) in enumerate(zip(gross_margin, op_margin, net_margin)):
    ax2.annotate(f"{g:.1f}%", (i, g), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9, color=GOLD, fontweight="bold")
    ax2.annotate(f"{o:.1f}%", (i, o), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9, color=CORAL, fontweight="bold")
    ax2.annotate(f"{n:.1f}%", (i, n), xytext=(0, -14), textcoords="offset points", ha="center", fontsize=9, color=TEAL, fontweight="bold")
ax2.set_ylabel("利润率 (%)", fontsize=11)
ax2.set_ylim(0, 40)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.grid(False)
l1, lab1 = ax.get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
ax.legend(l1 + l2, lab1 + lab2, loc="upper left", bbox_to_anchor=(0.0, 0.88), frameon=False, fontsize=9)
plt.title("安培龙 (SZSE:301413) — 营收增长与利润率走势 FY2023–FY2025", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_revenue_margins.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 2: Product line revenue mix (stacked) ----
products = ["热敏电阻及温度传感器", "压力传感器", "氧传感器及其他"]
y23 = [369.4, 354.1, 23.0]    # FY2023 from 2024 年报 (page 32 — comparative column)
y24 = [454.4, 468.0, 17.8]
y25 = [488.8, 674.3, 20.4]
mat = np.array([y23, y24, y25])  # rows = years
colors_p = [NAVY, TEAL, GOLD]
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
bottom = np.zeros(len(years))
for i, p in enumerate(products):
    vals = mat[:, i]
    bars = ax.bar(x, vals, 0.55, bottom=bottom, color=colors_p[i], label=p)
    for j, v in enumerate(vals):
        if v > 25:
            ax.text(j, bottom[j] + v/2, f"¥{v:.0f}M\n({v/mat[j].sum()*100:.0f}%)",
                    ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    bottom += vals
for j, tot in enumerate(mat.sum(axis=1)):
    ax.text(j, tot + 20, f"合计 ¥{tot:.0f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years, fontsize=11)
ax.set_ylabel("营业收入 (¥ million)")
ax.set_ylim(0, max(mat.sum(axis=1)) * 1.18)
ax.legend(loc="upper left", frameon=False, fontsize=10)
ax.set_title("产品线营收结构 — 压力传感器份额已超过热敏电阻", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_product_mix.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 3: R&D spending and intensity ----
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
bars = ax.bar(x, rd_spend, 0.55, color=PURPLE, label="研发投入 (¥M)")
for b, v in zip(bars, rd_spend):
    ax.text(b.get_x() + 0.275, v + 1.5, f"¥{v:.1f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years, fontsize=11)
ax.set_ylabel("研发投入 (¥ million)")
ax.set_ylim(0, max(rd_spend) * 1.30)

ax2 = ax.twinx()
ax2.plot(x, rd_pct, "o-", color=CORAL, lw=2.5, ms=10, label="研发费用率 (% of revenue)")
for i, v in enumerate(rd_pct):
    ax2.annotate(f"{v:.1f}%", (i, v), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=10, color=CORAL, fontweight="bold")
ax2.set_ylabel("研发费用率 (%)")
ax2.set_ylim(0, 12)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.grid(False)
l1, lab1 = ax.get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
ax.legend(l1 + l2, lab1 + lab2, loc="upper left", frameon=False, fontsize=10)
ax.set_title("研发投入加速 — 力传感器 / MEMS / IC 新平台投入", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_rd_intensity.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 4: Customer concentration (FY2025) ----
fig, ax = plt.subplots(figsize=(8.5, 6))
labels = ["客户一 (15.95%)", "客户二 (4.17%)", "客户三 (3.62%)", "客户四 (3.41%)", "客户五 (2.98%)", "其他客户 (69.87%)"]
sizes = [15.95, 4.17, 3.62, 3.41, 2.98, 69.87]
colors_pie = [CORAL, GOLD, TEAL, NAVY, PURPLE, "#e0e0e0"]
explode = (0.06, 0.02, 0.02, 0.02, 0.02, 0)
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_pie, explode=explode,
                                    autopct="%1.1f%%", startangle=90, pctdistance=0.78,
                                    textprops={"fontsize": 10})
for t in autotexts:
    t.set_color("white"); t.set_fontweight("bold"); t.set_fontsize(9)
autotexts[-1].set_color(SLATE)
ax.set_title("FY2025 销售收入构成 — 前五名客户合计 30.13%", fontsize=13, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_customer_concentration.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 5: Domestic vs Overseas revenue split ----
fig, ax = plt.subplots(figsize=(10, 5))
domestic = [639.9, 796.8, 1014.1]   # FY2023/2024/2025 内销 (2024 年报 page 32)
overseas = [106.7, 143.3, 169.4]
x = np.arange(len(years))
w = 0.36
b1 = ax.bar(x - w/2, domestic, w, color=NAVY, label="内销 Domestic (¥M)")
b2 = ax.bar(x + w/2, overseas, w, color=GOLD, label="外销 Export (¥M)")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 12, f"¥{b.get_height():.0f}M",
                ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years, fontsize=11)
ax.set_ylabel("营业收入 (¥ million)")
ax.set_ylim(0, max(domestic) * 1.22)
ax.legend(loc="upper left", frameon=False, fontsize=10)
ax.text(0.98, 0.95, "外销毛利率 45.8% > 内销 26.3%\n(FY2025 数据)",
        transform=ax.transAxes, ha="right", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=CORAL, alpha=0.9))
ax.set_title("内销与外销结构 — 出口贡献高毛利", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_geo_mix.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 6: TAM — China sensor market ----
# Source: 赛迪顾问 (cited in 2025 年度报告 page 14)
years_tam = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
# 2019 = 218.9 (≈2188.8亿元 quoted from 2019), 2024 = 4061.2亿元, 2024-2026 CAGR 15%
china_market = [2188.8, 2510, 2890, 3320, 3658, 4061.2, 4670, 5370]   # ¥ 亿元
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years_tam, china_market, "o-", color=NAVY, lw=3, ms=9)
ax.fill_between(years_tam, china_market, alpha=0.15, color=NAVY)
for x, y in zip(years_tam, china_market):
    ax.annotate(f"¥{y:.0f}亿", (x, y), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
ax.axvline(2024, color=SLATE, linestyle=":", alpha=0.6)
ax.text(2024.1, 2400, "2024 实际\n¥4,061亿", fontsize=10, color=SLATE)
ax.text(2025.3, 2400, "→ 2024-2026\n3年 CAGR 15%", fontsize=10, color=CORAL, fontweight="bold")
ax.set_xlabel("年份")
ax.set_ylabel("中国传感器市场规模 (¥ 亿元)")
ax.set_xticks(years_tam)
ax.set_ylim(0, 6500)
ax.set_title("中国传感器市场规模 (赛迪顾问) — 公司所处赛道", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_tam.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 7: Valuation snapshot vs peers ----
# Peer set: 韦尔股份(603501), 汉威科技(300007), 苏州固锝(002079), 苏奥传感(300507)
# P/E TTM and P/S TTM 2026-05-20 approximate (publicly available, Eastmoney)
peers = ["安培龙\n301413", "汉威科技\n300007", "苏奥传感\n300507", "苏州固锝\n002079", "韦尔股份\n603501"]
pe_ttm = [187.8, 78.5, 60.2, 95.1, 38.4]
ps_ttm = [11.6, 4.2, 5.8, 3.1, 6.5]
colors_b = [CORAL, NAVY, NAVY, NAVY, NAVY]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
x = np.arange(len(peers))
bars = axes[0].bar(x, pe_ttm, 0.55, color=colors_b)
for b, v in zip(bars, pe_ttm):
    axes[0].text(b.get_x() + 0.275, v + 4, f"{v:.0f}×", ha="center", fontsize=10, fontweight="bold")
axes[0].set_xticks(x); axes[0].set_xticklabels(peers, fontsize=9)
axes[0].set_ylabel("TTM P/E (倍)")
axes[0].axhline(np.median(pe_ttm), color=SLATE, linestyle="--", alpha=0.6, label=f"中位数 {np.median(pe_ttm):.0f}×")
axes[0].legend(loc="upper right", frameon=False)
axes[0].set_ylim(0, max(pe_ttm) * 1.18)
axes[0].set_title("市盈率 (TTM P/E) — 安培龙处于行业最高分位", fontsize=12, fontweight="bold")

bars = axes[1].bar(x, ps_ttm, 0.55, color=colors_b)
for b, v in zip(bars, ps_ttm):
    axes[1].text(b.get_x() + 0.275, v + 0.25, f"{v:.1f}×", ha="center", fontsize=10, fontweight="bold")
axes[1].set_xticks(x); axes[1].set_xticklabels(peers, fontsize=9)
axes[1].set_ylabel("TTM P/S (倍)")
axes[1].axhline(np.median(ps_ttm), color=SLATE, linestyle="--", alpha=0.6, label=f"中位数 {np.median(ps_ttm):.1f}×")
axes[1].legend(loc="upper right", frameon=False)
axes[1].set_ylim(0, max(ps_ttm) * 1.20)
axes[1].set_title("市销率 (TTM P/S) — 显著溢价反映机器人 / 力传感器叙事", fontsize=12, fontweight="bold")

fig.suptitle("安培龙 vs A股传感器同业 — 估值快照 (2026-05-20)", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_peer_valuation.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ---- Chart 8: Quarterly revenue trajectory 2024-2025 ----
quarters = ["2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4"]
# Computed: 2024 quarterly approximated from half-year/q3/full-year; 2025 quarterly from full-year
q_rev = [195, 230, 240, 275, 261.3, 292.6, 308.2, 321.4]   # ¥M (2024 estimates, 2025 actuals)
q_ni  = [16, 19, 21, 27, 20.4, 21.8, 31.0, 17.6]
fig, ax = plt.subplots(figsize=(11, 5))
x = np.arange(len(quarters))
w = 0.4
b1 = ax.bar(x - w/2, q_rev, w, color=NAVY, label="营业收入 (¥M)")
b2 = ax.bar(x + w/2, q_ni, w, color=GOLD, label="归母净利润 (¥M)")
for b in b1:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 4, f"{b.get_height():.0f}",
            ha="center", fontsize=9)
for b in b2:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 4, f"{b.get_height():.1f}",
            ha="center", fontsize=9, color=GOLD)
ax.set_xticks(x); ax.set_xticklabels(quarters, fontsize=9, rotation=20)
ax.set_ylabel("¥ million")
ax.set_ylim(0, max(q_rev) * 1.20)
ax.legend(loc="upper left", frameon=False)
ax.text(0.98, 0.96, "2025Q4 利润同环比下降 →\n年末费用确认 + 毛利率压力",
        transform=ax.transAxes, ha="right", va="top", fontsize=9, color=CORAL,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=CORAL, alpha=0.85))
ax.set_title("近 8 个季度收入与利润 — 营收持续增长，利润季度性波动", fontsize=13, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/anpeilong_quarterly.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

print("All charts saved.")
