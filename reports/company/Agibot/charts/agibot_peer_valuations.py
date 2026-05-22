"""Agibot vs. global humanoid-robot startup peer valuations (latest disclosed)."""
import matplotlib.pyplot as plt
import numpy as np

peers = [
    ("Figure AI",        39.5, "USA",  "Series C, 2025-02"),
    ("Tesla Optimus*",   25.0, "USA",  "implied carve-out"),
    ("Skild AI",         4.5,  "USA",  "Series A, 2024-07"),
    ("Apptronik",        4.0,  "USA",  "Series B-2, 2025-09"),
    ("Agibot",           6.0,  "CN",   "strategic, 2026-02 (press)"),
    ("Unitree",          5.0,  "CN",   "pre-IPO, 2025-Q4 (press)"),
    ("Physical Intel.",  2.4,  "USA",  "Series A, 2024-10"),
    ("1X Technologies",  1.0,  "NOR",  "Series B, 2024-01"),
    ("Sanctuary AI",     0.5,  "CAN",  "approx. last round"),
    ("Fourier",          0.8,  "CN",   "Series E (press, 2024-10)"),
]
peers.sort(key=lambda x: x[1], reverse=True)

names = [p[0] for p in peers]
vals = [p[1] for p in peers]
colors = ["#d63031" if p[2] == "USA" else "#0984e3" if p[2] == "CN"
          else "#6c5ce7" for p in peers]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(names[::-1], vals[::-1], color=colors[::-1])
ax.set_xlabel("Most recent post-money valuation (USD billion)")
ax.set_title("Global Humanoid-Robot Startup Valuations (2024-2026)",
             fontsize=13, fontweight="bold")
ax.grid(True, alpha=0.3, axis="x")

for bar, v in zip(bars, vals[::-1]):
    ax.text(v + 0.3, bar.get_y() + bar.get_height()/2,
            f"${v:.1f}B", va="center", fontsize=9)

# Highlight Agibot
for i, name in enumerate(names[::-1]):
    if "Agibot" in name:
        bars[i].set_edgecolor("black")
        bars[i].set_linewidth(2.5)

ax.set_xlim(0, 45)

fig.text(0.5, -0.04,
         "Red = US-based, Blue = China-based, Purple = Europe/Canada. "
         "*Tesla Optimus is not separately financed; figure is a sell-side estimated carve-out value.\n"
         "Sources: Bloomberg, Reuters, TechCrunch, ITjuzi, 36Kr press reports (2024-2026).",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/agibot_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved")
