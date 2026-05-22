#!/usr/bin/env python3
"""Tesla total GAAP gross margin trend, 2021–2025.
Source: Tesla Q4 and FY 2025 Update (8-K, 2026-01-28)."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2021", "2022", "2023", "2024", "2025"]
total_gm = [25.3, 25.6, 18.2, 17.9, 18.0]
op_margin = [12.1, 16.8, 9.2, 7.2, 4.6]

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(years, total_gm, marker="o", lw=2.5, color="#cc0000", label="Total GAAP gross margin (%)")
ax.plot(years, op_margin, marker="s", lw=2.5, color="#2e8b57", label="GAAP operating margin (%)")

for x, y in zip(years, total_gm):
    ax.text(x, y + 0.7, f"{y:.1f}%", ha="center", fontsize=9, color="#cc0000")
for x, y in zip(years, op_margin):
    ax.text(x, y - 1.4, f"{y:.1f}%", ha="center", fontsize=9, color="#2e8b57")

ax.set_ylabel("Margin (%)")
ax.set_title("Tesla GAAP Gross Margin and Operating Margin, 2021–2025",
             fontweight="bold")
ax.legend(loc="upper right")
ax.set_ylim(0, 30)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_gross_margin.png",
            dpi=150, bbox_inches="tight")
print("saved")
