"""极智嘉 2021–2025H1 收入与毛利率走势."""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

# 数据来源：极智嘉招股书与 2025 中期报告
years = ["2021", "2022", "2023", "2024", "2025H1"]
revenue = [7.90, 14.52, 21.43, 24.09, 10.25]  # 单位：亿元人民币
gross_margin = [25.7, 31.7, 32.0, 32.7, 35.1]  # %（年报披露口径）

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#3b6fb5", alpha=0.85, label="收入（亿元人民币）")
ax1.set_ylabel("收入（亿元人民币）", color="#3b6fb5")
ax1.tick_params(axis="y", labelcolor="#3b6fb5")
ax1.set_ylim(0, 30)

for bar, v in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 0.4, f"{v:.1f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color="#d9531e", marker="o", linewidth=2, label="毛利率（%）")
ax2.set_ylabel("毛利率（%）", color="#d9531e")
ax2.tick_params(axis="y", labelcolor="#d9531e")
ax2.set_ylim(20, 40)

for x, m in zip(years, gross_margin):
    ax2.text(x, m + 0.6, f"{m:.1f}%", ha="center", fontsize=9, color="#d9531e")

plt.title("极智嘉收入与毛利率走势（2021–2025H1）")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/geekplus_revenue_margin.png", dpi=150, bbox_inches="tight")
print("done")
