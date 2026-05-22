"""
贵州茅台 (SSE:600519) 公司研究 — 图表生成脚本
数据来源：贵州茅台 2021–2025 年年度报告，2026 年第一季度报告（巨潮资讯网）
所有数字单位：人民币（亿元），除非另有说明
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Use system font with CJK support on macOS
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "Heiti SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "/Users/x/projects/financial_agent/reports/charts"

# ---------- Chart 1: 5-year revenue & net margin (dual-axis) ----------
years = ["2021", "2022", "2023", "2024", "2025"]
revenue = [1094.64, 1275.54, 1476.94, 1708.99, 1688.38]
net_income = [524.60, 627.16, 747.34, 862.28, 823.20]
gross_margin = [91.54, 91.87, 91.96, 91.93, 91.23]

fig, ax1 = plt.subplots(figsize=(10, 5.6))
x = np.arange(len(years))
w = 0.35
ax1.bar(x - w/2, revenue, w, label="营业总收入", color="#8B0000", alpha=0.85)
ax1.bar(x + w/2, net_income, w, label="归母净利润", color="#D4A017", alpha=0.9)
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel("人民币（亿元）", fontsize=11)
ax1.set_title("贵州茅台 2021–2025 营收、归母净利润与酒类毛利率", fontsize=13, pad=12)
ax1.grid(axis="y", alpha=0.3)
for i, v in enumerate(revenue):
    ax1.text(i - w/2, v + 25, f"{v:,.0f}", ha="center", fontsize=9)
for i, v in enumerate(net_income):
    ax1.text(i + w/2, v + 25, f"{v:,.0f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(x, gross_margin, color="#1F4E79", marker="o", linewidth=2, label="酒类毛利率（%）")
ax2.set_ylabel("酒类毛利率（%）", fontsize=11, color="#1F4E79")
ax2.set_ylim(88, 94)
for i, v in enumerate(gross_margin):
    ax2.text(i, v - 0.55, f"{v:.2f}%", ha="center", color="#1F4E79", fontsize=9)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_revenue_trend.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 2: 2025 revenue mix — product & channel ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
prod_labels = ["茅台酒", "其他系列酒"]
prod_vals = [1464.99, 222.75]
prod_colors = ["#8B0000", "#D4A017"]
axes[0].pie(prod_vals, labels=prod_labels, autopct="%1.1f%%",
            colors=prod_colors, startangle=90, textprops={"fontsize": 11})
axes[0].set_title("按产品（2025 年，亿元）\n茅台酒 1,464.99 / 系列酒 222.75",
                  fontsize=11, pad=10)

ch_labels = ["直销", "批发代理"]
ch_vals = [845.43, 842.32]
ch_colors = ["#1F4E79", "#6FA8DC"]
axes[1].pie(ch_vals, labels=ch_labels, autopct="%1.1f%%",
            colors=ch_colors, startangle=90, textprops={"fontsize": 11})
axes[1].set_title("按渠道（2025 年，亿元）\n直销 845.43 / 批发代理 842.32",
                  fontsize=11, pad=10)

fig.suptitle("贵州茅台 2025 年收入结构", fontsize=13)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_revenue_mix.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 3: Direct sales channel shift 2021–2025 ----------
direct = [240.29, 493.79, 672.33, 748.43, 845.43]
wholesale = [854.35, 781.75, 799.95, 957.69, 842.32]
years5 = ["2021", "2022", "2023", "2024", "2025"]

fig, ax = plt.subplots(figsize=(10, 5.4))
x = np.arange(len(years5))
w = 0.38
ax.bar(x - w/2, direct, w, color="#1F4E79", label="直销渠道")
ax.bar(x + w/2, wholesale, w, color="#6FA8DC", label="批发代理")
ax.set_xticks(x); ax.set_xticklabels(years5)
ax.set_ylabel("人民币（亿元）", fontsize=11)
ax.set_title("贵州茅台直销 vs. 批发代理渠道收入 2021–2025", fontsize=13, pad=10)
ax.grid(axis="y", alpha=0.3)
for i, v in enumerate(direct):
    ax.text(i - w/2, v + 15, f"{v:,.0f}", ha="center", fontsize=9)
for i, v in enumerate(wholesale):
    ax.text(i + w/2, v + 15, f"{v:,.0f}", ha="center", fontsize=9)

share = [d/(d+w_) * 100 for d, w_ in zip(direct, wholesale)]
ax2 = ax.twinx()
ax2.plot(x, share, color="#8B0000", marker="o", linewidth=2)
ax2.set_ylabel("直销占比（%）", fontsize=11, color="#8B0000")
ax2.set_ylim(15, 60)
for i, v in enumerate(share):
    ax2.text(i, v + 1.0, f"{v:.1f}%", ha="center", color="#8B0000", fontsize=9)

ax.legend(loc="upper left", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_channel_shift.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 4: Cash dividend trajectory ----------
div = [216.75, 547.09, 442.95, 646.72, 650.33]
years5 = ["2021", "2022", "2023", "2024", "2025"]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(years5, div, color="#8B0000", alpha=0.85)
ax.set_ylabel("现金分红总额（含税，亿元）", fontsize=11)
ax.set_title("贵州茅台 2021–2025 年度现金分红总额（含特别分红与中期分红）", fontsize=12, pad=10)
ax.grid(axis="y", alpha=0.3)
for b, v in zip(bars, div):
    ax.text(b.get_x() + b.get_width()/2, v + 10, f"{v:,.1f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_dividends.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 5: Production capacity 2021-2025 (吨) ----------
moutai_actual = [56551, 56473, 57218, 56272, 58473]
xilei_actual = [28249, 34800, 42305, 48114, 57651]
years5 = ["2021", "2022", "2023", "2024", "2025"]
fig, ax = plt.subplots(figsize=(10, 5.4))
x = np.arange(len(years5))
w = 0.38
ax.bar(x - w/2, moutai_actual, w, color="#8B0000", label="茅台酒基酒")
ax.bar(x + w/2, xilei_actual, w, color="#D4A017", label="酱香系列酒基酒")
ax.set_xticks(x); ax.set_xticklabels(years5)
ax.set_ylabel("实际产能（吨）", fontsize=11)
ax.set_title("贵州茅台基酒实际产能 2021–2025", fontsize=13, pad=10)
ax.grid(axis="y", alpha=0.3)
for i, v in enumerate(moutai_actual):
    ax.text(i - w/2, v + 800, f"{v:,}", ha="center", fontsize=9)
for i, v in enumerate(xilei_actual):
    ax.text(i + w/2, v + 800, f"{v:,}", ha="center", fontsize=9)
ax.legend(loc="upper left", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_capacity.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 6: 全国白酒产量趋势 ----------
prod_kl = [715.6, 671.2, 629.5, 414.5, 354.9]
years5 = ["2021", "2022", "2023", "2024", "2025"]
fig, ax = plt.subplots(figsize=(10, 5.4))
bars = ax.bar(years5, prod_kl, color="#6FA8DC", alpha=0.85)
ax.set_ylabel("产量（万千升）", fontsize=11)
ax.set_title("全国规模以上白酒企业累计产量 2021–2025（持续收缩，存量调整）",
             fontsize=12, pad=10)
ax.grid(axis="y", alpha=0.3)
for b, v in zip(bars, prod_kl):
    ax.text(b.get_x() + b.get_width()/2, v + 15, f"{v:.1f}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT}/moutai_industry.png", dpi=150, bbox_inches="tight")
plt.close()


print("All charts generated.")
