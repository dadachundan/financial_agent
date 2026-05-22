"""Sanhua revenue and net margin trend, 2020-2025."""
import matplotlib.pyplot as plt
import os

years = [2020, 2021, 2022, 2023, 2024, 2025]
revenue_bn = [12.11, 16.02, 21.35, 24.56, 27.95, 31.01]
net_income_bn = [1.46, 1.68, 2.57, 2.92, 3.10, 4.06]
net_margin = [ni / r * 100 for ni, r in zip(net_income_bn, revenue_bn)]

fig, ax1 = plt.subplots(figsize=(9.5, 5.2))
color1 = "#1f4e79"
ax1.bar(years, revenue_bn, color=color1, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color=color1, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_xticks(years)
for x, y in zip(years, revenue_bn):
    ax1.text(x, y + 0.4, f"{y:.1f}", ha="center", fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = "#c0392b"
ax2.plot(years, net_margin, color=color2, marker="o", linewidth=2.2,
         label="Net margin (%)")
ax2.set_ylabel("Net margin (%)", color=color2, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(0, 20)
for x, y in zip(years, net_margin):
    ax2.text(x, y + 0.5, f"{y:.1f}%", ha="center", fontsize=9, color=color2)

plt.title("Sanhua (SZSE:002050) revenue and net margin, FY2020–FY2025",
          fontsize=12.5, pad=12)
fig.tight_layout()
path = os.path.join(os.path.dirname(__file__), "sanhua_revenue_margin.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
print(path)
