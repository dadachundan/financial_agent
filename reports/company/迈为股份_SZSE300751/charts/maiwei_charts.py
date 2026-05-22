"""迈为股份 (SZSE:300751) 公司研究图表生成脚本.

数据来源：
- 苏州迈为科技股份有限公司 2025 年年度报告（2026-04-27 披露）— 营收、净利、毛利率、客户、产品/地区构成、研发
- 苏州迈为科技股份有限公司 2024 / 2023 / 2022 / 2021 年年度报告 — 历史财务
- 2026 年一季度报告（2026-04-27 披露）— 最新季度

输出位置：/Users/x/projects/financial_agent/reports/charts/maiwei_<name>.png
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

# ============================================================
# Chart 1 — 5-year revenue + net margin trend (dual axis)
# ============================================================
# 单位：人民币百万元
# 营收/归母净利：来自 2021/2022/2023/2024/2025 年度报告 "主要会计数据"
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
revenue = [3095.6, 4148.2, 8088.5, 9830.4, 8152.0]      # ¥ million; FY2022 取自 2024 年报追溯口径
net_income = [646.9, 861.9, 913.9, 925.9, 721.6]
# 毛利率取自历年年报 "分销售模式 直销" 行: 2021=38.30%, 2022=38.31%, 2023=30.51%, 2024=28.11%, 2025=38.61%
gross_margin = [38.30, 38.31, 30.51, 28.11, 38.61]
net_margin = [n / r * 100 for n, r in zip(net_income, revenue)]

fig, ax1 = plt.subplots(figsize=(10.5, 5.5))
x = np.arange(len(years))
w = 0.55
bars = ax1.bar(x, revenue, w, color=NAVY, label="营业收入 (¥M)")
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + w/2, v + 150, f"¥{v:.0f}M", ha="center", fontsize=10, fontweight="bold")
ax1.set_xticks(x); ax1.set_xticklabels(years, fontsize=11)
ax1.set_ylabel("营业收入 (¥ million)", fontsize=11, color=NAVY)
ax1.set_ylim(0, max(revenue) * 1.25)
yoy = [None] + [(revenue[i]/revenue[i-1]-1)*100 for i in range(1, len(revenue))]
for i, y in enumerate(yoy):
    if y is None: continue
    color = "#2a9d8f" if y >= 0 else "#c0392b"
    ax1.text(i, -800, f"{y:+.1f}% YoY", ha="center", fontsize=9, color=color)

ax2 = ax1.twinx()
ax2.plot(x, gross_margin, color=CORAL, marker="o", linewidth=2.4, markersize=8, label="毛利率 (GM %)")
for i, v in enumerate(gross_margin):
    ax2.text(i + 0.18, v + 0.6, f"{v:.1f}%", color=CORAL, fontsize=9, fontweight="bold")
ax2.plot(x, net_margin, color=GOLD, marker="s", linewidth=2.0, markersize=7, linestyle="--", label="净利率 (NM %)")
for i, v in enumerate(net_margin):
    ax2.text(i + 0.18, v - 1.6, f"{v:.1f}%", color=GOLD, fontsize=9)
ax2.set_ylabel("毛利率 / 净利率 (%)", fontsize=11, color=CORAL)
ax2.set_ylim(0, 50)
ax2.grid(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10, frameon=False)
plt.title("迈为股份 FY2021–FY2025 营收与利润率走势", fontsize=13, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_revenue_margin_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Chart 2 — FY2025 营收构成 by product & by geography (stacked horizontal bars)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

# By product
ax = axes[0]
products = ["太阳能电池\n成套生产设备", "单机", "配件及其他"]
prod_amt = [6025.1, 1717.8, 409.1]                # ¥M, 来自 2025 年报
prod_pct = [73.91, 21.07, 5.02]
colors_p = [NAVY, TEAL, GOLD]
y_pos = np.arange(len(products))
bars = ax.barh(y_pos, prod_amt, color=colors_p)
for b, v, p in zip(bars, prod_amt, prod_pct):
    ax.text(b.get_width() + 60, b.get_y() + b.get_height()/2,
            f"¥{v:,.0f}M ({p:.1f}%)", va="center", fontsize=10, fontweight="bold")
ax.set_yticks(y_pos); ax.set_yticklabels(products, fontsize=10)
ax.set_xlim(0, max(prod_amt) * 1.35)
ax.set_xlabel("营业收入 (¥ million)", fontsize=10)
ax.set_title("FY2025 按产品", fontsize=11, fontweight="bold")
ax.invert_yaxis()

# By geography
ax = axes[1]
geos = ["境内 (中国大陆)", "境外 (海外)"]
geo_amt = [5272.9, 2879.1]                        # ¥M
geo_pct = [64.64, 35.36]
geo_yoy = [-42.34, 320.19]                        # YoY %
colors_g = [SLATE, CORAL]
y_pos = np.arange(len(geos))
bars = ax.barh(y_pos, geo_amt, color=colors_g)
for b, v, p, y in zip(bars, geo_amt, geo_pct, geo_yoy):
    yoy_color = "#2a9d8f" if y >= 0 else "#c0392b"
    ax.text(b.get_width() + 60, b.get_y() + b.get_height()/2 - 0.05,
            f"¥{v:,.0f}M ({p:.1f}%)", va="center", fontsize=10, fontweight="bold")
    ax.text(b.get_width() + 60, b.get_y() + b.get_height()/2 + 0.25,
            f"YoY {y:+.1f}%", va="center", fontsize=9, color=yoy_color)
ax.set_yticks(y_pos); ax.set_yticklabels(geos, fontsize=10)
ax.set_xlim(0, max(geo_amt) * 1.45)
ax.set_xlabel("营业收入 (¥ million)", fontsize=10)
ax.set_title("FY2025 按地区", fontsize=11, fontweight="bold")
ax.invert_yaxis()

plt.suptitle("迈为股份 FY2025 营收构成 — 海外占比首次突破 35%", fontsize=13, fontweight="bold", y=1.04)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_revenue_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Chart 3 — R&D investment & R&D intensity (5-year)
# ============================================================
rd_spend = [331.4, 488.5, 763.3, 951.1, 1158.8]   # ¥M, 来自 2021–2025 年报
rd_pct = [10.71, 11.78, 9.44, 9.68, 14.22]
rd_team = [None, None, None, 1218, 1288]           # 研发人员数 (2024/2025 披露)

fig, ax1 = plt.subplots(figsize=(10.5, 5.2))
x = np.arange(len(years))
bars = ax1.bar(x, rd_spend, 0.55, color=PURPLE, label="研发投入 (¥M)")
for b, v in zip(bars, rd_spend):
    ax1.text(b.get_x() + 0.55/2, v + 30, f"¥{v:.0f}M", ha="center", fontsize=10, fontweight="bold")
ax1.set_xticks(x); ax1.set_xticklabels(years, fontsize=11)
ax1.set_ylabel("研发投入 (¥ million)", fontsize=11, color=PURPLE)
ax1.set_ylim(0, max(rd_spend) * 1.30)

ax2 = ax1.twinx()
ax2.plot(x, rd_pct, color=CORAL, marker="o", linewidth=2.4, markersize=8, label="研发费用率 (%)")
for i, v in enumerate(rd_pct):
    ax2.text(i + 0.18, v + 0.4, f"{v:.2f}%", color=CORAL, fontsize=10, fontweight="bold")
ax2.set_ylabel("研发费用率 (% of revenue)", fontsize=11, color=CORAL)
ax2.set_ylim(0, 18)
ax2.grid(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10, frameon=False)
plt.title("迈为股份 研发投入 — 2025 年 R&D 强度跃升至 14.22%", fontsize=13, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_rd_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Chart 4 — Customer concentration FY2024 vs FY2025
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

labels_24 = ["客户1\n31.42%", "客户2\n9.92%", "客户3\n6.03%", "客户4\n5.17%", "客户5\n4.50%", "其他\n42.96%"]
pct_24 = [31.42, 9.92, 6.03, 5.17, 4.50, 42.96]
colors_pie = ["#1f3a5f", "#2a9d8f", "#e76f51", "#f4a261", "#6f42c1", "#cfd8dc"]
axes[0].pie(pct_24, labels=labels_24, colors=colors_pie, startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}, textprops={"fontsize": 9.5})
axes[0].set_title("FY2024 — 前五客户 57.04%\n(top-1 = 31.42%)", fontsize=11, fontweight="bold")

labels_25 = ["客户1\n29.05%", "客户2\n14.70%", "客户3\n4.59%", "客户4\n4.13%", "客户5\n3.98%", "其他\n43.55%"]
pct_25 = [29.05, 14.70, 4.59, 4.13, 3.98, 43.55]
axes[1].pie(pct_25, labels=labels_25, colors=colors_pie, startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}, textprops={"fontsize": 9.5})
axes[1].set_title("FY2025 — 前五客户 56.46%\n(top-1 = 29.05%)", fontsize=11, fontweight="bold")

plt.suptitle("迈为股份 客户集中度 — top-1 客户依赖度近三成", fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_customer_concentration.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Chart 5 — Quarterly revenue & net profit (8 quarters)
# ============================================================
# 来自 2024 / 2025 年度报告分季度数据 + 2026Q1
q_labels = ["24Q1", "24Q2", "24Q3", "24Q4", "25Q1", "25Q2", "25Q3", "25Q4", "26Q1"]
q_rev = [2218.2, 2650.9, 2897.9, 2063.3, 2228.7, 1984.1, 1990.8, 1948.4, 1336.8]    # ¥M
# 24Q 归母净利由 2024 年报披露; 25Q 来自 2025 年报; 26Q1 自一季报
# 来自 2024 年报: 24Q1=260.1; 24Q2=201.0; 24Q3=297.4; 24Q4=167.4 (合 925.9)
q_np = [260.1, 201.0, 297.4, 167.4, 162.1, 231.8, 269.4, 58.4, 118.0]               # ¥M
fig, ax1 = plt.subplots(figsize=(11, 5.2))
x = np.arange(len(q_labels))
bars = ax1.bar(x, q_rev, 0.55, color=NAVY, label="营业收入 (¥M)", alpha=0.85)
for b, v in zip(bars, q_rev):
    ax1.text(b.get_x() + 0.55/2, v + 40, f"{v:.0f}", ha="center", fontsize=8.5)
ax1.set_xticks(x); ax1.set_xticklabels(q_labels, fontsize=10)
ax1.set_ylabel("单季营业收入 (¥ million)", fontsize=11, color=NAVY)
ax1.set_ylim(0, max(q_rev) * 1.20)

ax2 = ax1.twinx()
ax2.plot(x, q_np, color=CORAL, marker="o", linewidth=2.4, markersize=8, label="归母净利润 (¥M)")
for i, v in enumerate(q_np):
    ax2.text(i + 0.15, v + 12, f"{v:.0f}", color=CORAL, fontsize=8.5, fontweight="bold")
ax2.set_ylabel("归母净利润 (¥ million)", fontsize=11, color=CORAL)
ax2.set_ylim(0, max(q_np) * 1.55)
ax2.grid(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=10, frameon=False)
plt.title("迈为股份 单季营收与归母净利 — 24Q4 起持续承压, 26Q1 营收同比-40%", fontsize=12.5, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_quarterly_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Chart 6 — Segment revenue mix shift (光伏 vs 半导体&显示) FY2024 vs FY2025
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
segments = ["太阳能光伏", "半导体及显示", "其他"]
fy24 = [9732.2, 67.1, 31.1]              # ¥M
fy25 = [7449.6, 662.0, 40.3]
x = np.arange(len(segments))
w = 0.36
b1 = ax.bar(x - w/2, fy24, w, color=SLATE, label="FY2024")
b2 = ax.bar(x + w/2, fy25, w, color=TEAL, label="FY2025")
for bars, vals in [(b1, fy24), (b2, fy25)]:
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + w/2, v + 120, f"¥{v:,.0f}M", ha="center", fontsize=9.5, fontweight="bold")
# YoY annotations
yoy = [-23.45, 887.01, 29.62]
for i, y in enumerate(yoy):
    color = "#2a9d8f" if y >= 0 else "#c0392b"
    ax.text(i, max(fy24[i], fy25[i]) + 700, f"YoY {y:+.1f}%", ha="center", fontsize=10,
            color=color, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(segments, fontsize=11)
ax.set_ylabel("营业收入 (¥ million)", fontsize=11)
ax.set_ylim(0, max(fy24) * 1.18)
ax.legend(fontsize=11, frameon=False, loc="upper right")
plt.title("迈为股份 业务结构 — 半导体及显示 FY2025 同比 +887%", fontsize=12.5, fontweight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{OUTDIR}/maiwei_segment_shift.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts generated:")
import os
for f in sorted(os.listdir(OUTDIR)):
    if f.startswith("maiwei_"):
        print(f"  - {OUTDIR}/{f}")
