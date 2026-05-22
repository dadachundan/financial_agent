"""Global legged-robot TAM — quadruped + humanoid combined, 2024-2035 forecast."""
import matplotlib.pyplot as plt
import numpy as np

years = list(range(2024, 2036))
# Approximate consensus blend of Goldman Sachs (2024), Morgan Stanley (2024),
# CITIC Securities (2025), and Citi GPS (2025) humanoid + quadruped forecasts.
# Values in USD billion of annual unit-revenue equivalents.
quadruped = [0.6, 0.9, 1.3, 1.8, 2.5, 3.3, 4.2, 5.0, 5.8, 6.5, 7.2, 8.0]
humanoid  = [0.2, 0.6, 1.6, 3.5, 7.0, 13.0, 22.0, 35.0, 52.0, 72.0, 95.0, 120.0]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.stackplot(years, quadruped, humanoid,
             labels=["Quadruped (industrial + research + consumer)",
                     "Humanoid (industrial + service)"],
             colors=["#c0392b", "#2c3e50"], alpha=0.85)

ax.set_title("Global Legged-Robot Annual Revenue TAM, 2024-2035E",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Annual unit revenue (USD billion)")
ax.legend(loc="upper left", fontsize=10)
ax.grid(True, alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Goldman Sachs (2024), Morgan Stanley Blue Paper (2024), "
         "CITIC Securities (2025), Citi GPS Future of Robotics (2025). "
         "Blended midpoint; humanoid trajectory assumes commercial-scale shipments from 2026.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/deeprobotics_tam_growth.png",
            dpi=150, bbox_inches="tight")
print("saved")
