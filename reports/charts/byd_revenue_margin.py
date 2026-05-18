"""BYD revenue + gross margin dual-axis chart (FY2020-FY2025)."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
# Revenue in RMB bn (consolidated)
revenue = [156.6, 216.1, 424.1, 602.3, 777.1, 803.96]
# Approximate consolidated gross margin (%) — derived from segment cost lines
# 2020-2024 from prior annual reports (auto ~20% gross, electronics ~7%)
gross_margin = [19.4, 13.0, 17.0, 20.2, 19.4, 17.7]
# Net profit attributable RMB bn
net_profit = [4.23, 3.05, 16.62, 30.04, 40.25, 32.62]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
color1 = "#1f4e79"
bars = ax1.bar(years, revenue, color=color1, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color=color1, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, max(revenue) * 1.2)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 12, f"{v:,.0f}",
             ha="center", fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = "#c0392b"
ax2.plot(years, gross_margin, marker="o", color=color2, linewidth=2.4, label="Gross margin (%)")
ax2.set_ylabel("Consolidated gross margin (%)", color=color2, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(0, 30)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 1.0, f"{y:.1f}%", ha="center", fontsize=9, color=color2)

color3 = "#27ae60"
ax2_twin = ax1.twinx()
ax2_twin.spines["right"].set_position(("outward", 60))
ax2_twin.plot(years, net_profit, marker="s", linestyle="--", color=color3, linewidth=1.8,
              label="Net profit (RMB bn)")
ax2_twin.set_ylabel("Net profit attributable (RMB bn)", color=color3, fontsize=11)
ax2_twin.tick_params(axis="y", labelcolor=color3)
ax2_twin.set_ylim(0, 60)
for x, y in zip(years, net_profit):
    ax2_twin.text(x, y + 1.5, f"{y:.1f}", ha="center", fontsize=8, color=color3)

plt.title("BYD — Revenue, Gross Margin & Net Profit (FY2020-FY2025)", fontsize=12, pad=12)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/byd_revenue_margin.png",
            dpi=150, bbox_inches="tight")
print("saved revenue_margin")
