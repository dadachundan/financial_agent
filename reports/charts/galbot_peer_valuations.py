"""Humanoid / embodied-AI startup peer post-money valuations (early 2026)."""
import matplotlib.pyplot as plt

peers = [
    ("Figure AI (US)",            39.5, "#222"),
    ("Tesla Optimus* (US)",       25.0, "#999"),  # implied carve-out, sell-side
    ("Agibot (智元, CN)",          6.0,  "#0b5fff"),
    ("Unitree (宇树, CN)",         5.0,  "#0b5fff"),
    ("Skild AI (US)",              4.5,  "#222"),
    ("Apptronik (US)",             4.0,  "#222"),
    ("Galbot (银河通用, CN)",      4.0,  "#7a3cff"),
    ("Physical Intelligence (US)", 2.4,  "#222"),
    ("1X Technologies (NO/US)",    1.0,  "#222"),
    ("Fourier (傅利叶, CN)",       0.8,  "#0b5fff"),
    ("UBTECH (HKEX:9880)",         3.5,  "#0b5fff"),  # public market cap, approx mid-2026
    ("Sanctuary AI (CA)",          0.5,  "#222"),
]

# sort descending
peers.sort(key=lambda r: r[1], reverse=True)
labels = [p[0] for p in peers]
values = [p[1] for p in peers]
colors = [p[2] for p in peers]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(labels, values, color=colors)
ax.invert_yaxis()
for bar, v in zip(bars, values):
    ax.text(v + 0.5, bar.get_y() + bar.get_height() / 2,
            f"${v:.1f}B", va="center", fontsize=9)

ax.set_xlabel("Reported post-money valuation (USD billion, approx.)")
ax.set_title("Humanoid / Embodied-AI Startup Valuations, early 2026 (press-cited)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, 45)
ax.grid(True, axis="x", alpha=0.3)

# legend by color
from matplotlib.patches import Patch
legend = [
    Patch(color="#7a3cff", label="Galbot (subject)"),
    Patch(color="#0b5fff", label="China peers"),
    Patch(color="#222", label="Non-China peers"),
    Patch(color="#999", label="Implied carve-out"),
]
ax.legend(handles=legend, loc="lower right", fontsize=9)

fig.text(0.5, -0.02,
         "Sources: Bloomberg, Reuters, TechCrunch, ITjuzi, 36Kr, Caixin (2024-2026). "
         "All figures press-cited or, for UBTECH, public market capitalisation; not all officially confirmed.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/galbot_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved galbot_peer_valuations.png")
