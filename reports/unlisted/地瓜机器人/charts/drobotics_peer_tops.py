"""Edge AI dev-board peer comparison: TOPS vs price.
Sources: D-Robotics, Nvidia, Rockchip official product pages (cited inline)."""

import matplotlib.pyplot as plt

products = ["RDK X3\n(D-Robotics)", "RDK X5\n(D-Robotics)", "RDK S100\n(D-Robotics)",
            "RDK S100P\n(D-Robotics)", "Jetson Orin Nano Super\n(Nvidia)",
            "Jetson AGX Orin 64GB\n(Nvidia)", "RK3588 dev board\n(Rockchip)"]
tops = [5, 10, 80, 128, 67, 275, 6]
price_usd = [65, 110, 392, 560, 249, 1999, 150]

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#4C72B0", "#4C72B0", "#4C72B0", "#4C72B0", "#76B900", "#76B900", "#888888"]
sc = ax.scatter(price_usd, tops, s=[t * 3 + 50 for t in tops], c=colors, alpha=0.7, edgecolor="black", linewidth=1.2)

for i, name in enumerate(products):
    ax.annotate(name, (price_usd[i], tops[i]), xytext=(8, 6), textcoords="offset points",
                fontsize=9)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("List Price (USD, log scale)", fontsize=11)
ax.set_ylabel("AI Compute (TOPS, log scale)", fontsize=11)
ax.set_title("Edge AI Dev-Board Compute vs. Price — D-Robotics RDK vs. Nvidia Jetson / Rockchip",
             fontsize=12, fontweight="bold")
ax.grid(which="both", linestyle="--", alpha=0.4)

from matplotlib.patches import Patch
legend_elems = [Patch(facecolor="#4C72B0", label="D-Robotics RDK"),
                Patch(facecolor="#76B900", label="Nvidia Jetson"),
                Patch(facecolor="#888888", label="Rockchip RK3588")]
ax.legend(handles=legend_elems, loc="lower right", fontsize=10)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/drobotics_peer_tops.png",
            dpi=150, bbox_inches="tight")
print("Saved drobotics_peer_tops.png")
