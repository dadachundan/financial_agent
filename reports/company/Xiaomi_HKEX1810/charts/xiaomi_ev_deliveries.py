import matplotlib.pyplot as plt
import numpy as np

# Xiaomi EV deliveries by quarter (units, thousands)
quarters = ["Q2 24", "Q3 24", "Q4 24", "Q1 25", "Q2 25", "Q3 25", "Q4 25", "Q1 26"]
deliveries = [27.3, 39.8, 69.7, 75.9, 81.3, 108.8, 145.0, 90.0]  # approximations; Q1 26 reflects Lunar New Year slowdown

fig, ax = plt.subplots(figsize=(10, 5.2))
bars = ax.bar(quarters, deliveries, color="#FF6900", alpha=0.85)
ax.set_ylabel("Deliveries (000 units)", fontsize=12)
ax.set_title("Xiaomi EV — Quarterly Deliveries, Q2 2024–Q1 2026", fontsize=13)
for bar, v in zip(bars, deliveries):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 2, f"{v:.0f}k", ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0, 170)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/xiaomi_ev_deliveries.png", dpi=150, bbox_inches="tight")
print("saved")
