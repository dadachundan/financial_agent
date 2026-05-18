import matplotlib.pyplot as plt
import numpy as np

# Revenue (RMB bn) and gross margin trend 2021-2025
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
revenue = [328.3, 280.0, 271.0, 365.9, 457.3]  # RMB bn
gross_margin = [17.7, 17.0, 21.2, 20.9, 22.5]  # %, approximate consolidated GM

fig, ax1 = plt.subplots(figsize=(10, 5.5))

color1 = "#FF6900"  # Xiaomi orange
ax1.bar(years, revenue, color=color1, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color=color1, fontsize=12)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, 550)

for i, v in enumerate(revenue):
    ax1.text(i, v + 8, f"{v:.0f}", ha="center", fontsize=10, color=color1, fontweight="bold")

ax2 = ax1.twinx()
color2 = "#222222"
ax2.plot(years, gross_margin, color=color2, marker="o", linewidth=2.4, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color=color2, fontsize=12)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(10, 30)

for i, v in enumerate(gross_margin):
    ax2.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontsize=10, color=color2, fontweight="bold")

plt.title("Xiaomi (HKEX:1810) — Revenue and Gross Margin, FY2021–FY2025", fontsize=13)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/xiaomi_revenue_margin.png", dpi=150, bbox_inches="tight")
print("saved")
