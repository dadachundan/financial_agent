"""Guomao Reducer (SSE:603915) — revenue and net income trend, FY2021–FY2025."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
# Revenue (RMB mn) and net income attributable to shareholders (RMB mn)
revenue = [2767.3, 2495.7, 2660.4, 2589.4, 2645.8]
net_income = [510.2, 395.5, 395.5, 293.5, 235.0]
gross_margin_pct = [25.5, 22.1, 23.8, 21.1, 20.0]  # blended; 2025 主营业务 from 年报

fig, ax1 = plt.subplots(figsize=(9, 5.2))

# Revenue bars
bar = ax1.bar(years, revenue, color="#1f6feb", alpha=0.85, label="Revenue (RMB mn)")
# Net income overlay (lighter)
ax1.bar(years, net_income, color="#d29922", alpha=0.95, label="Net income attrib. (RMB mn)")
ax1.set_ylabel("RMB million", fontsize=11)
ax1.set_ylim(0, 3200)
for i, v in enumerate(revenue):
    ax1.text(i, v + 60, f"{v:,.0f}", ha="center", fontsize=9, color="#1f6feb")
for i, v in enumerate(net_income):
    ax1.text(i, v + 60, f"{v:,.0f}", ha="center", fontsize=9, color="#a06400")

# Gross margin line on right axis
ax2 = ax1.twinx()
ax2.plot(years, gross_margin_pct, color="#cf222e", marker="o", linewidth=2.2, label="Gross margin %")
ax2.set_ylabel("Gross margin %", fontsize=11)
ax2.set_ylim(0, 35)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
for i, v in enumerate(gross_margin_pct):
    ax2.text(i + 0.07, v + 0.6, f"{v:.1f}%", color="#cf222e", fontsize=9)

ax1.set_title("Guomao Reducer (SSE:603915) — Revenue, Net Income, Gross Margin (FY2021–FY2025)", fontsize=12)
lines1, labs1 = ax1.get_legend_handles_labels()
lines2, labs2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labs1 + labs2, loc="upper left", fontsize=9)
ax1.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/guomao_revenue_margin.png", dpi=150, bbox_inches="tight")
print("saved")
