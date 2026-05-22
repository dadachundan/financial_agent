#!/usr/bin/env python3
"""Tesla annual energy storage deployments (GWh), 2021–2025.
Source: Tesla Q4 and FY 2025 Update (8-K, 2026-01-28)."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2021", "2022", "2023", "2024", "2025"]
gwh = [4.0, 6.5, 14.7, 31.4, 46.7]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(years, gwh, color="#2e8b57")
for i, v in enumerate(gwh):
    ax.text(i, v + 0.8, f"{v} GWh", ha="center", fontweight="bold", fontsize=10)

ax.set_ylabel("Energy storage deployed (GWh)")
ax.set_title("Tesla Energy Storage Deployments, 2021–2025 (annual)",
             fontweight="bold")
ax.set_ylim(0, 55)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(4, 50, "12× growth over five years",
        ha="right", fontsize=9, style="italic", color="#444")
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_energy_storage.png",
            dpi=150, bbox_inches="tight")
print("saved")
