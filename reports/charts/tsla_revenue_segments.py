#!/usr/bin/env python3
"""TSLA segment revenue 2021-2025 (stacked bar) + total revenue line.
Source: Tesla Q4 and FY 2025 Update (8-K exhibit 99.1, filed 2026-01-28)."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2021", "2022", "2023", "2024", "2025"]
auto = np.array([47232, 71462, 82419, 77070, 69526]) / 1000.0       # $B
energy = np.array([2789, 3909, 6035, 10086, 12771]) / 1000.0
services = np.array([3802, 6091, 8319, 10534, 12530]) / 1000.0
total = auto + energy + services

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(years, auto, label="Automotive", color="#cc0000")
ax.bar(years, energy, bottom=auto, label="Energy Generation & Storage", color="#2e8b57")
ax.bar(years, services, bottom=auto + energy, label="Services & Other", color="#444")

for i, t in enumerate(total):
    ax.text(i, t + 1.5, f"${t:.1f}B", ha="center", fontsize=9, fontweight="bold")

ax.set_ylabel("Revenue (USD $B)")
ax.set_title("Tesla Revenue by Segment, 2021–2025", fontweight="bold")
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim(0, 115)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_revenue_segments.png",
            dpi=150, bbox_inches="tight")
print("saved")
