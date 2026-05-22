"""LimX Dynamics vs. global humanoid-startup peer post-money valuations."""
import matplotlib.pyplot as plt

# (Company, latest post-money USD bn, geography, round / date label)
# All values press-cited / implied — no public filings for the private names.
peers = [
    ("Figure AI",            39.5, "US",    "Series C, 2025-09"),
    ("Unitree (宇树)",        7.0, "CN",    "Pre-IPO target, 2026-03"),
    ("Agibot (智元)",         6.4, "CN",    "Strategic, 2026"),
    ("Apptronik",             5.0, "US",    "Series A ext., 2025"),
    ("UBTECH (9880.HK)",      6.0, "HK",    "Market cap, 2026-02"),
    ("LimX Dynamics (逐际)", 1.5, "CN",    "Series B est., 2026-02"),
    ("Sanctuary AI",          1.0, "CA",    "Series A, 2023"),
    ("1X Technologies",       1.0, "NO/US", "Series B, 2024-01"),
    ("Fourier (傅利叶)",      0.8, "CN",    "Series E, 2024-10"),
]

names = [p[0] for p in peers]
vals  = [p[1] for p in peers]
colors = ["#d6336c" if "LimX" in n else "#888" for n in names]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(names, vals, color=colors)
ax.invert_yaxis()
for bar, v, lbl in zip(bars, vals, [p[3] for p in peers]):
    ax.text(v + 0.5, bar.get_y() + bar.get_height() / 2,
            f"${v:.1f}B  ({lbl})", va="center", fontsize=9)
ax.set_xlim(0, 47)
ax.set_xlabel("Latest disclosed / press-cited post-money (USD billion)")
ax.set_title("Humanoid Robot Startup Peer Valuations — LimX Dynamics in Context (2024–2026)",
             fontsize=13, fontweight="bold")
ax.grid(True, axis="x", alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Caixin Global, TechNode, The Robot Report, KraneShares, Humanoids Daily, HKEX last-trade for UBTECH (2025–2026). "
         "LimX post-money est. is press-implied (not officially disclosed); private peer marks approximate.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/limx_peer_valuations.png",
            dpi=150, bbox_inches="tight")
print("saved")
