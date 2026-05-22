"""Zhaowei revenue + gross margin trend (2020–2025)."""
import matplotlib.pyplot as plt

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
revenue_mn = [1195.1, 1140.0, 1152.5, 1205.9, 1524.6, 1715.5]      # RMB mn, 营业收入
net_income_mn = [244.7, 147.5, 150.5, 179.9, 225.1, 254.3]          # RMB mn, 归母净利润
# Gross margin (consolidated, %), from 年报 主营业务分行业 row
gross_margin = [38.6, 27.4, 27.8, 29.9, 31.4, 33.7]

fig, ax1 = plt.subplots(figsize=(9, 5.2))

color1 = "#1f4e79"
color2 = "#c45a11"
color3 = "#2e7d32"

bars = ax1.bar(years, revenue_mn, color=color1, alpha=0.85, label="Revenue (RMB mn)")
ax1.set_xlabel("Fiscal year")
ax1.set_ylabel("Revenue / Net income (RMB mn)", color=color1)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, max(revenue_mn) * 1.25)

# overlay net income as line
ax1.plot(years, net_income_mn, color=color2, marker="o", linewidth=2.2,
         label="Net income (RMB mn)")
for x, y in zip(years, net_income_mn):
    ax1.annotate(f"{y:.0f}", (x, y), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=8, color=color2)

# gross margin on right axis
ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color=color3, marker="s", linewidth=2.2,
         linestyle="--", label="Gross margin (%)")
for x, y in zip(years, gross_margin):
    ax2.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                 xytext=(0, -14), ha="center", fontsize=8, color=color3)
ax2.set_ylabel("Gross margin (%)", color=color3)
ax2.tick_params(axis="y", labelcolor=color3)
ax2.set_ylim(20, 45)

plt.title("Zhaowei (SZSE:003021) — Revenue, Net income, Gross margin (2020–2025)")
fig.tight_layout()

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

plt.savefig("/Users/x/projects/financial_agent/reports/charts/zhaowei_revenue_margin.png",
            dpi=150, bbox_inches="tight")
print("saved zhaowei_revenue_margin.png")
