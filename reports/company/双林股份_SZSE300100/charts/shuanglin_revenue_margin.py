#!/usr/bin/env python3
"""Shuanglin Co. (300100) revenue & GM trend 2020-2025."""
import matplotlib.pyplot as plt
import os

# Revenue (RMB bn) and GM% from 双林股份 2020-2025 年度报告
years = [2020, 2021, 2022, 2023, 2024, 2025]
revenue = [3.13, 3.85, 3.79, 4.14, 4.91, 5.48]
gm = [22.4, 17.0, 13.6, 13.0, 18.5, 20.9]
ni = [0.12, 0.16, -0.18, 0.08, 0.50, 0.50]  # net profit RMB bn

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.set_xlabel("Fiscal Year")
ax1.set_ylabel("Revenue / Net Profit (RMB bn)", color="#0b5394")
b1 = ax1.bar([y - 0.18 for y in years], revenue, width=0.36, color="#3d85c6", label="Revenue")
b2 = ax1.bar([y + 0.18 for y in years], ni, width=0.36, color="#cfe2f3", label="Net profit (attributable)")
ax1.tick_params(axis="y", labelcolor="#0b5394")
ax1.set_ylim(-0.5, 6.5)

ax2 = ax1.twinx()
ax2.set_ylabel("Gross margin (%)", color="#990000")
ax2.plot(years, gm, color="#cc0000", marker="o", linewidth=2.2, label="Gross margin")
ax2.tick_params(axis="y", labelcolor="#990000")
ax2.set_ylim(0, 30)

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Shuanglin Co. (SZSE:300100) — Revenue, Net Profit, Gross Margin 2020–2025")
out = os.path.join(os.path.dirname(__file__), "shuanglin_revenue_margin.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print(out)
