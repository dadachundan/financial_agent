"""Hengli Hydraulics — 5-yr revenue + gross margin trend."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
revenue_bn = [7.86, 9.31, 8.16, 8.98, 9.39, 10.94]   # RMB bn
gross_margin = [43.5, 39.8, 37.4, 41.6, 42.8, 41.2]   # %, approx, derived from machine-equipment segment GM

fig, ax1 = plt.subplots(figsize=(8.5, 4.6))

color1 = "#1f4e79"
ax1.bar(years, revenue_bn, color=color1, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_xlabel("Fiscal Year")
ax1.set_ylabel("Revenue (RMB bn)", color=color1)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, 13)
for i, v in enumerate(revenue_bn):
    ax1.text(i, v + 0.2, f"{v:.2f}", ha="center", fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = "#c0504d"
ax2.plot(years, gross_margin, color=color2, marker="o", linewidth=2.2, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color=color2)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.set_ylim(30, 50)
for i, v in enumerate(gross_margin):
    ax2.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9, color=color2)

plt.title("Hengli Hydraulics — Revenue & Gross Margin (FY2020–FY2025)", fontsize=12)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/hengli_revenue_margin.png", dpi=150, bbox_inches="tight")
print("saved")
