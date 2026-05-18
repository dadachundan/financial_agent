"""TAM growth: hydraulics industry + humanoid roller-screw TAM."""
import matplotlib.pyplot as plt
import numpy as np

years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
hydraulics_cn = [76, 82, 90, 99, 108, 117, 126]   # RMB bn — China hydraulics industry output, CHPSC + extrapolation
roller_screw_global = [0.2, 0.5, 1.5, 4, 9, 18, 35]   # USD bn — humanoid roller screw TAM, Morgan Stanley etc.

fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
ax1.bar([y - 0.18 for y in years], hydraulics_cn, width=0.36, color="#1f4e79", label="China hydraulics output (RMB bn)")
ax1.set_xlabel("Year")
ax1.set_ylabel("China hydraulics output (RMB bn)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_xticks(years)

ax2 = ax1.twinx()
ax2.plot(years, roller_screw_global, color="#c0504d", marker="o", linewidth=2.4, label="Humanoid roller-screw TAM (USD bn)")
ax2.set_ylabel("Humanoid roller-screw TAM (USD bn)", color="#c0504d")
ax2.tick_params(axis="y", labelcolor="#c0504d")

ax1.set_title("Dual-axis TAM: China hydraulics + global humanoid roller-screw forecast (2024–2030E)", fontsize=11)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/hengli_tam.png", dpi=150, bbox_inches="tight")
print("saved")
