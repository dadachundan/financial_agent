"""Peer P/S and 2025 unit-sales comparison for GAC and Chinese auto OEMs."""
import matplotlib.pyplot as plt
import numpy as np

peers = ["GAC\n(601238)", "SAIC\n(600104)", "BYD\n(002594)", "Geely\n(0175.HK)",
         "Dongfeng\n(0489.HK)", "Great Wall\n(601633)"]
# Unit sales 2025 (mn), approximate
units_2025 = [1.72, 4.51, 4.60, 3.03, 1.86, 1.17]  # SAIC/BYD/Geely/Dongfeng/GW
# Net income 2025 RMB bn (Dongfeng H1 = -RMB101m, full-yr est. ~loss; GW est ~12bn)
net_income = [-8.78, 10.0, 40.0, 16.6, -1.0, 12.4]

x = np.arange(len(peers))
width = 0.35
fig, ax1 = plt.subplots(figsize=(10, 5.5))

bars1 = ax1.bar(x - width / 2, units_2025, width, color="#1f77b4",
                label="2025 vehicle sales (mn units)")
ax1.set_ylabel("Vehicle sales 2025 (mn units)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 6)
for b, v in zip(bars1, units_2025):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.2f}",
             ha="center", fontsize=8, color="#1f77b4")

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width / 2, net_income, width, color="#d62728",
                label="2025 net income (RMB bn, est. where mid)")
ax2.set_ylabel("Net income 2025 (RMB bn)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.axhline(0, color="grey", linestyle="--", linewidth=0.8)
ax2.set_ylim(-15, 50)
for b, v in zip(bars2, net_income):
    ax2.text(b.get_x() + b.get_width() / 2, v + (1.2 if v >= 0 else -2.5),
             f"{v:+.1f}", ha="center", fontsize=8, color="#d62728")

ax1.set_xticks(x)
ax1.set_xticklabels(peers)
plt.title("Chinese OEM peer comparison: 2025 vehicle sales and net income")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/gac_peer_valuation.png",
            dpi=150, bbox_inches="tight")
print("Saved gac_peer_valuation.png")
