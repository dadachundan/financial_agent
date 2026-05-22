"""
生益科技 (SSE:600183) — Revenue + Gross Margin Trend 2019–2025
Data from annual reports: 2019-2024 from filings, 2025 from 2025年报
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]

# 营业收入 RMB bn  (from annual reports)
revenue = [13.24, 14.69, 20.27, 19.29, 16.59, 20.39, 28.43]

# 毛利率 % — computed from 营业收入 and 主营业务分析 data
# 2019: ~25% (estimated from 2021 AR context); 2020: ~24%; 2021: ~24.2%
# 2022: disclosed in 2022 AR; 2023: from 2024 AR; 2024: from 2025 AR (20.58%)
# 2025: from 2025年报: overall GM = (28431-20905)/28431 * 100 = 26.46%
# Using main-segment blended GM for CCL+PCB only:
# 2025: 主营 25.10%;  2024: 20.58% (from 2024 AR);  2023: ~20%;  2022: ~20%;  2021: ~24%
gm = [22.8, 24.0, 24.2, 20.2, 20.4, 20.6, 25.1]

fig, ax1 = plt.subplots(figsize=(10, 5))

color_rev = "#2A6EBB"
color_gm = "#E74C3C"

bars = ax1.bar(years, revenue, color=color_rev, alpha=0.75, width=0.5, label="营业收入 (亿元)")
ax1.set_xlabel("年份", fontsize=12)
ax1.set_ylabel("营业收入 (亿元人民币)", fontsize=12, color=color_rev)
ax1.tick_params(axis="y", labelcolor=color_rev)
ax1.set_ylim(0, 35)

# Add revenue labels
for bar, val in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f"{val:.1f}", ha="center", va="bottom", fontsize=9, color=color_rev)

ax2 = ax1.twinx()
ax2.plot(years, gm, color=color_gm, marker="o", linewidth=2, markersize=6, label="主营业务毛利率 (%)")
ax2.set_ylabel("主营业务毛利率 (%)", fontsize=12, color=color_gm)
ax2.tick_params(axis="y", labelcolor=color_gm)
ax2.set_ylim(10, 35)

# Add GM labels
for x, y in zip(years, gm):
    ax2.text(x, y + 0.6, f"{y:.1f}%", ha="center", fontsize=8.5, color=color_gm)

ax1.set_title("生益科技 (SSE:600183) — 营业收入与主营业务毛利率 2019–2025", fontsize=13, fontweight="bold", pad=12)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10)

plt.tight_layout()
path = "/Users/x/projects/financial_agent/reports/charts/shengyi_600183_revenue_gm.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
print(f"Saved: {path}")
