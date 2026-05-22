"""Global NEV TAM growth + BYD share."""
import matplotlib.pyplot as plt
import numpy as np

years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026E", "2030E"]
# Global NEV sales (M units) — approximate, blending IEA/CnEVPost data
global_nev = [3.1, 6.6, 10.5, 14.0, 17.1, 22.4, 26.5, 45.0]
byd_units = [0.18, 0.59, 1.86, 3.02, 4.27, 4.60, 4.80, 8.50]
byd_share = [s/g*100 for s, g in zip(byd_units, global_nev)]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax1.bar(years, global_nev, color="#7f8c8d", alpha=0.55, label="Global NEV sales (M units)")
ax1.bar(years, byd_units, color="#27ae60", label="BYD NEV sales (M units)")
ax1.set_ylabel("NEV unit sales (millions)", fontsize=11)
ax1.set_ylim(0, 50)
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(years, byd_share, marker="o", color="#c0392b", linewidth=2.4, label="BYD global share (%)")
ax2.set_ylabel("BYD share of global NEV (%)", color="#c0392b", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c0392b")
ax2.set_ylim(0, 30)
for x, y in zip(years, byd_share):
    ax2.text(x, y + 0.7, f"{y:.1f}%", ha="center", fontsize=8, color="#c0392b")

plt.title("Global NEV TAM vs. BYD unit sales and share (2020-2030E)", fontsize=12, pad=12)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/byd_tam_growth.png",
            dpi=150, bbox_inches="tight")
print("saved tam")
