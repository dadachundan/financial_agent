"""Sanhua addressable-TAM growth chart: refrigeration valves + EV thermal + humanoid actuators."""
import matplotlib.pyplot as plt
import numpy as np
import os

years = np.array([2024, 2026, 2028, 2030, 2032])
ref = np.array([18, 21, 25, 29, 33])              # USD bn — HVAC/refrig components TAM
ev_tm = np.array([16, 24, 33, 42, 50])            # USD bn — EV thermal mgmt TAM
robot = np.array([0.3, 1.5, 6, 18, 38])           # USD bn — humanoid actuator TAM

fig, ax = plt.subplots(figsize=(9.5, 5.3))
ax.stackplot(years, ref, ev_tm, robot,
             labels=["HVAC / refrigeration components",
                     "EV thermal management",
                     "Humanoid robot mechatronic actuators"],
             colors=["#2980b9", "#27ae60", "#c0392b"], alpha=0.85)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Global TAM (USD bn)", fontsize=11)
ax.set_title("Sanhua addressable TAM by segment, 2024–2032E",
             fontsize=12.5, pad=12)
ax.set_xticks(years)
ax.legend(loc="upper left", fontsize=10)
total = ref + ev_tm + robot
for x, y in zip(years, total):
    ax.text(x, y + 2, f"${y:.0f}B", ha="center", fontsize=9, fontweight="bold")
ax.set_ylim(0, max(total) * 1.18)
fig.tight_layout()
path = os.path.join(os.path.dirname(__file__), "sanhua_tam.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
print(path)
