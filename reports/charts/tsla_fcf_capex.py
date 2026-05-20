#!/usr/bin/env python3
"""Tesla operating cash flow, capex, and free cash flow, 2021–2025.
Source: Tesla Q4 and FY 2025 Update (8-K, 2026-01-28)."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2021", "2022", "2023", "2024", "2025"]
ocf = np.array([11497, 14724, 13256, 14923, 14747]) / 1000.0
capex = np.array([6514, 7163, 8899, 11342, 8527]) / 1000.0
fcf = ocf - capex   # by definition; matches reported $4.98 / 7.56 / 4.36 / 3.58 / 6.22B

x = np.arange(len(years))
w = 0.28
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w, ocf, w, label="Operating cash flow", color="#1f77b4")
ax.bar(x, capex, w, label="Capex", color="#ff7f0e")
ax.bar(x + w, fcf, w, label="Free cash flow", color="#2ca02c")
for i, v in enumerate(fcf):
    ax.text(i + w, v + 0.3, f"${v:.1f}B", ha="center", fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("USD $B")
ax.set_title("Tesla Cash Generation: OCF, Capex, Free Cash Flow (2021–2025)",
             fontweight="bold")
ax.legend()
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_fcf_capex.png",
            dpi=150, bbox_inches="tight")
print("saved")
