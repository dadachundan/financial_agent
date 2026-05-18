"""Humanoid dexterous-hand TAM build (2024–2030)."""
import matplotlib.pyplot as plt
import numpy as np

years = list(range(2024, 2031))
# Humanoid robot annual shipments (units, k) — base case based on Morgan Stanley / Citi / GGII
shipments_k = [0.2, 5, 25, 100, 350, 900, 1800]
# Dexterous-hand pair revenue per unit (USD, blended)
asp_usd = 4000
# Dexterous-hand TAM (USD bn) = shipments * 2 hands/unit * ASP / 1e9
tam_usd_bn = [s * 1000 * 2 * asp_usd / 1e9 for s in shipments_k]

fig, ax = plt.subplots(figsize=(8.5, 5))
bars = ax.bar([str(y) for y in years], tam_usd_bn, color="#1f4e79", alpha=0.85)
for b, v in zip(bars, tam_usd_bn):
    ax.annotate(f"${v:.1f}B", (b.get_x() + b.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=9)
ax.set_ylabel("Dexterous-hand TAM (USD bn)")
ax.set_title("Global humanoid dexterous-hand TAM (USD bn, 2024-2030E)\n"
             "Assumptions: 2 hands/unit, blended ASP USD 4,000")
ax.set_ylim(0, max(tam_usd_bn) * 1.25)

# secondary axis: humanoid shipments
ax2 = ax.twinx()
ax2.plot(years, shipments_k, color="#c45a11", marker="o", linewidth=2,
         label="Humanoid units shipped (k)")
ax2.set_ylabel("Humanoid units shipped (thousand)", color="#c45a11")
ax2.tick_params(axis="y", labelcolor="#c45a11")
for x, y in zip(years, shipments_k):
    ax2.annotate(f"{y}k", (x - 2024, y), textcoords="offset points",
                 xytext=(6, -2), ha="left", fontsize=8, color="#c45a11")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/zhaowei_tam.png",
            dpi=150, bbox_inches="tight")
print("saved zhaowei_tam.png")
