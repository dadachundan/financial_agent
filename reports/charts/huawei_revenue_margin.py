"""Huawei revenue + net margin chart (FY2018-FY2024).

Sources:
- FY2018-FY2023 from Huawei Annual Reports (huawei.com/en/annual-report).
- FY2024: RMB 862.07 bn, net profit RMB 62.6 bn (Huawei 2024 Annual Report, 2025-03-31).
"""
import matplotlib.pyplot as plt

years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
# Revenue in RMB bn (consolidated, per Huawei Annual Reports)
revenue = [721.2, 858.8, 891.4, 636.8, 642.3, 704.2, 862.1]
# Net profit (RMB bn) — note FY2021 spiked from Honor divestiture gain
net_profit = [59.3, 62.7, 64.6, 113.7, 35.6, 87.0, 62.6]
# Approx R&D as % of revenue
rd_pct = [14.1, 15.3, 15.9, 22.4, 25.1, 23.4, 20.8]

fig, ax1 = plt.subplots(figsize=(10.5, 5.5))
color1 = "#b22222"  # Huawei red
bars = ax1.bar(years, revenue, color=color1, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color=color1, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, 1000)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 12, f"{v:,.0f}",
             ha="center", fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = "#1f4e79"
ax2.plot(years, net_profit, marker="o", color=color2, linewidth=2.4,
         label="Net profit (RMB bn)")
ax2.set_ylabel("Net profit (RMB bn)", color=color2, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(0, 140)
for x, y in zip(years, net_profit):
    ax2.text(x, y + 3, f"{y:.1f}", ha="center", fontsize=9, color=color2)

color3 = "#27ae60"
ax2_twin = ax1.twinx()
ax2_twin.spines["right"].set_position(("outward", 60))
ax2_twin.plot(years, rd_pct, marker="s", linestyle="--", color=color3, linewidth=1.8,
              label="R&D % of revenue")
ax2_twin.set_ylabel("R&D as % of revenue", color=color3, fontsize=11)
ax2_twin.tick_params(axis="y", labelcolor=color3)
ax2_twin.set_ylim(0, 30)
for x, y in zip(years, rd_pct):
    ax2_twin.text(x, y + 0.7, f"{y:.1f}%", ha="center", fontsize=8, color=color3)

plt.title("Huawei — Revenue, Net Profit and R&D Intensity (FY2018-FY2024)",
          fontsize=12, pad=12)
ax1.axvspan(1.5, 2.5, alpha=0.10, color="#999999")
ax1.text(2.0, 950, "Entity List\n(May 2019)\nfull-year impact", ha="center",
         fontsize=8, color="#555555")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/huawei_revenue_margin.png",
            dpi=150, bbox_inches="tight")
print("saved huawei_revenue_margin")
