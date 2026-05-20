"""D-Robotics funding trajectory chart.
Sources: caproasia.com / Caixin / TechNode (cited inline in the report)."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

rounds = ["Spin-off\n(May 2024)", "Series A\n(May 2025)", "Series B1\n(Mar 2026)", "Series B2\n(Apr 2026)"]
amounts_usd_m = [0, 100, 120, 150]
cumulative = [0, 100, 220, 370]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(rounds, amounts_usd_m, color=["#999999", "#4C72B0", "#55A868", "#C44E52"], edgecolor="black")
ax2 = ax.twinx()
ax2.plot(rounds, cumulative, color="#E67E22", marker="o", linewidth=2.5, label="Cumulative (USD m)")

for bar, val in zip(bars, amounts_usd_m):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, val + 3, f"${val}M",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

for x, y in zip(range(len(rounds)), cumulative):
    if y > 0:
        ax2.text(x, y + 8, f"${y}M cum.", ha="center", va="bottom",
                 fontsize=9, color="#E67E22", fontweight="bold")

ax.set_ylabel("Round Size (USD millions)", fontsize=11)
ax2.set_ylabel("Cumulative External Funding (USD millions)", fontsize=11, color="#E67E22")
ax.set_title("D-Robotics (地瓜机器人) — External Funding Trajectory, 2024–2026",
             fontsize=13, fontweight="bold")
ax.set_ylim(0, 180)
ax2.set_ylim(0, 420)
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax2.tick_params(axis="y", colors="#E67E22")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/drobotics_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("Saved drobotics_funding_trajectory.png")
