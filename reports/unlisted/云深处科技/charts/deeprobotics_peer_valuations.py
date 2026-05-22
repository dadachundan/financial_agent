"""Peer valuation comparison — legged-robot makers, latest disclosed marks (2024-2026).

All figures are press-cited or last-known transaction marks; Boston Dynamics is
embedded inside Hyundai Motor Group and is shown at a press-cited implied EV.
"""
import matplotlib.pyplot as plt

peers = [
    ("Figure AI\n(US, humanoid)",         39.5, "#0b5fff"),
    ("Boston Dynamics\n(KR-owned, all)",   5.0, "#666"),
    ("Unitree\n(CN, quad+humanoid)",       2.0, "#c0392b"),
    ("Apptronik\n(US, humanoid)",          1.5, "#0b5fff"),
    ("Agility Robotics\n(US, humanoid)",   1.0, "#0b5fff"),
    ("1X Technologies\n(NO, humanoid)",    1.0, "#0b5fff"),
    ("ANYbotics\n(CH, quad)",              0.9, "#7f8c8d"),
    ("Deep Robotics\n(CN, quad+humanoid)", 1.4, "#c0392b"),
    ("Ghost Robotics\n(US, quad)",         0.4, "#0b5fff"),
]

# Sort ascending
peers_sorted = sorted(peers, key=lambda x: x[1])
names = [p[0] for p in peers_sorted]
vals = [p[1] for p in peers_sorted]
colors = [p[2] for p in peers_sorted]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(names, vals, color=colors, edgecolor="black", linewidth=0.6)
for bar, v in zip(bars, vals):
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
            f"${v:.1f}B", va="center", fontsize=9)

ax.set_xlabel("Latest disclosed / press-cited post-money valuation (USD billion)")
ax.set_title("Legged-Robot Peer Valuation Set (latest known, 2024-2026)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, 45)
ax.grid(True, axis="x", alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Bloomberg, Reuters, TechCrunch, Caixin, IT桔子 (2024-2026). "
         "Boston Dynamics shown at press-cited implied EV inside Hyundai Motor Group; "
         "Ghost Robotics valuation derived from the 2025 LIG Nex1 majority-acquisition.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/deeprobotics_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved")
