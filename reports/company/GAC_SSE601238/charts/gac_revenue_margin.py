"""GAC Group consolidated revenue and net margin 2021–2025."""
import matplotlib.pyplot as plt

years = ["2021", "2022", "2023", "2024", "2025"]
# Revenue RMB bn (consolidated; equity-method JVs not consolidated)
revenue = [75.68, 110.06, 128.76, 106.80, 95.66]
# Net income attributable to shareholders RMB bn (incl. JV equity income)
net_income = [7.34, 8.07, 4.43, 0.82, -8.78]
# Total vehicle sales mn units (incl. JVs)
units = [2.143, 2.434, 2.503, 2.003, 1.7215]

fig, ax1 = plt.subplots(figsize=(9, 5.2))

color_rev = "#1f77b4"
ax1.set_xlabel("Year")
ax1.set_ylabel("Revenue (RMB bn)", color=color_rev)
bars = ax1.bar(years, revenue, color=color_rev, alpha=0.75, label="Revenue (RMB bn)")
ax1.tick_params(axis="y", labelcolor=color_rev)
ax1.set_ylim(0, 150)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
color_ni = "#d62728"
ax2.set_ylabel("Net income attributable (RMB bn) / Units sold (mn)", color="black")
line1, = ax2.plot(years, net_income, color=color_ni, marker="o", linewidth=2,
                   label="Net income attributable (RMB bn)")
line2, = ax2.plot(years, units, color="#2ca02c", marker="s", linewidth=2,
                   label="Vehicle sales (mn units, incl. JV)")
ax2.axhline(0, color="grey", linestyle="--", linewidth=0.8)
ax2.set_ylim(-12, 12)
for x, v in zip(years, net_income):
    ax2.annotate(f"{v:+.2f}", (x, v), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=8, color=color_ni)
for x, v in zip(years, units):
    ax2.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                 xytext=(0, -14), ha="center", fontsize=8, color="#2ca02c")

plt.title("GAC Group: Revenue, Net Income and Total Vehicle Sales (2021–2025)")
lines = [bars, line1, line2]
labels = ["Revenue (RMB bn)", "Net income attributable (RMB bn)", "Vehicle sales (mn units, incl. JV)"]
ax1.legend(lines, labels, loc="lower left", fontsize=9)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/gac_revenue_margin.png",
            dpi=150, bbox_inches="tight")
print("Saved gac_revenue_margin.png")
