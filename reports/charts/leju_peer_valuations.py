"""Peer valuation comparison — humanoid + legged-robot makers, latest disclosed marks (2024-2026).

All figures are press-cited or last-known transaction marks. UBTECH (9880.HK) is shown at
market-cap (public). Boston Dynamics is embedded inside Hyundai Motor Group and shown at a
press-cited implied EV.
"""
import matplotlib.pyplot as plt

peers = [
    ("Figure AI\n(US, humanoid)",            39.5, "#0b5fff"),
    ("Boston Dynamics\n(KR-owned, all)",      5.0, "#666"),
    ("UBTECH 9880.HK\n(CN, humanoid)",        4.5, "#c0392b"),
    ("Unitree\n(CN, quad+humanoid)",          2.0, "#c0392b"),
    ("Agibot 智元\n(CN, humanoid)",            2.0, "#c0392b"),
    ("Apptronik\n(US, humanoid)",             1.5, "#0b5fff"),
    ("Deep Robotics\n(CN, quad+humanoid)",    1.4, "#c0392b"),
    ("Robotera 星动纪元\n(CN, humanoid)",       1.2, "#c0392b"),
    ("Agility Robotics\n(US, humanoid)",      1.0, "#0b5fff"),
    ("1X Technologies\n(NO, humanoid)",       1.0, "#0b5fff"),
    ("Leju Robotics\n(CN, humanoid)",         0.95, "#16a085"),
    ("Fourier 傅利叶\n(CN, humanoid)",          0.9, "#c0392b"),
    ("LimX Dynamics 逐际\n(CN, biped/quad)",   0.7, "#c0392b"),
    ("Magiclab 魔法原子\n(CN, humanoid)",       0.5, "#c0392b"),
    ("Kepler 开普勒\n(CN, humanoid)",           0.4, "#c0392b"),
]

# Sort ascending
peers_sorted = sorted(peers, key=lambda x: x[1])
names = [p[0] for p in peers_sorted]
vals = [p[1] for p in peers_sorted]
colors = [p[2] for p in peers_sorted]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(names, vals, color=colors, edgecolor="black", linewidth=0.6)
for bar, v in zip(bars, vals):
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
            f"${v:.1f}B", va="center", fontsize=9)

ax.set_xlabel("Latest disclosed / press-cited post-money valuation (USD billion)")
ax.set_title("Humanoid + Legged-Robot Peer Valuation Set (latest known, 2024-2026)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, 45)
ax.grid(True, axis="x", alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Bloomberg, Reuters, TechCrunch, Caixin, 36Kr, IT桔子, HKEX (2024-2026). "
         "UBTECH at HKEX market cap; Boston Dynamics at press-cited implied EV inside Hyundai. "
         "Leju highlighted in green.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/leju_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved")
