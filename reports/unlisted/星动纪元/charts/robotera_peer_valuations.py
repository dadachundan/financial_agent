"""Robotera vs. global humanoid-startup peer post-money valuations."""
import matplotlib.pyplot as plt

# (Company, latest post-money USD bn, geography, round / date label)
peers = [
    ("Figure AI",            39.5, "US",    "Series C, 2025-02"),
    ("Agibot (智元)",         6.0, "CN",    "Strategic, 2026-02"),
    ("Unitree (宇树)",        5.0, "CN",    "Pre-IPO, 2025-Q4"),
    ("Apptronik",             4.0, "US",    "Series B-2, 2025-09"),
    ("Robotera (星动)",       3.5, "CN",    "Series B, 2026-05"),
    ("UBTECH (9880.HK)",      3.2, "HK",    "Market cap, 2026-05"),
    ("1X Technologies",       1.0, "NO/US", "Series B, 2024-01"),
    ("Fourier (傅利叶)",      0.8, "CN",    "Series E, 2024-10"),
]

names = [p[0] for p in peers]
vals  = [p[1] for p in peers]
colors = ["#888" if "Robotera" not in n else "#d6336c" for n in names]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(names, vals, color=colors)
ax.invert_yaxis()
for bar, v, lbl in zip(bars, vals, [p[3] for p in peers]):
    ax.text(v + 0.5, bar.get_y() + bar.get_height() / 2,
            f"${v:.1f}B  ({lbl})", va="center", fontsize=9)
ax.set_xlim(0, 47)
ax.set_xlabel("Latest disclosed / press-cited post-money (USD billion)")
ax.set_title("Humanoid Robot Startup Peer Valuations — Latest Marks (2024–2026)",
             fontsize=13, fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Bloomberg, Reuters, TechCrunch, Caixin Global, ITjuzi, Humanoids Daily, HKEX last-trade for UBTECH. "
         "Private-company marks are press-cited and approximate.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/robotera_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved")
