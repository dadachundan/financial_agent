#!/usr/bin/env python3
"""Quarterly Tesla deliveries 2024–2025. Source: Tesla Q4 2024 + Q4 2025 updates."""
import matplotlib.pyplot as plt
import numpy as np

quarters = ["Q1-24", "Q2-24", "Q3-24", "Q4-24",
            "Q1-25", "Q2-25", "Q3-25", "Q4-25"]
# Q1-Q3 2024 implied from FY-2024 total 1,789,226 less Q4-24 495,570 = 1,293,656.
# Per Tesla Q1/Q2/Q3 2024 quarterly delivery releases:
#   Q1-24 386,810; Q2-24 443,956; Q3-24 462,890; Q4-24 495,570
# Sources: https://ir.tesla.com — Q1 2024 production & deliveries release;
# https://ir.tesla.com — Q2 2024; https://ir.tesla.com — Q3 2024.
deliveries = [386810, 443956, 462890, 495570,
              336681, 384122, 497099, 418227]

fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#888"] * 4 + ["#cc0000"] * 4
ax.bar(quarters, [d / 1000 for d in deliveries], color=colors)
for i, d in enumerate(deliveries):
    ax.text(i, d / 1000 + 7, f"{d/1000:.0f}k", ha="center", fontsize=9)
ax.set_ylabel("Vehicle deliveries (thousands)")
ax.set_title("Tesla Quarterly Deliveries, 2024–2025", fontweight="bold")
ax.set_ylim(0, 580)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(7, 560, "FY-2025 deliveries: 1,636,129 (−9% YoY)",
        ha="right", fontsize=9, style="italic")
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_deliveries_quarterly.png",
            dpi=150, bbox_inches="tight")
print("saved")
