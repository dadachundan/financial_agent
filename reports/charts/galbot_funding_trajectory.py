"""Galbot (银河通用) funding-round valuation trajectory.

Press-cited / approximate post-money valuations. Galbot is private; all figures
are reconstructed from media coverage (36Kr, Late Post / 晚点LatePost, Caixin,
IT桔子) and from investor announcements quoted in those reports. Numbers should
be read as approximate and as good-faith reconstructions only — not officially
confirmed by Galbot.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

rounds = [
    ("Angel",          datetime(2023, 6, 1),  0.10),   # ~RMB 100M+ angel, ~$100M implied
    ("Pre-A",          datetime(2024, 2, 1),  0.30),   # ~RMB 700M Pre-A; IDG, BV Capital
    ("A",              datetime(2024, 6, 1),  0.50),   # Series A — Hillhouse, Sequoia
    ("A+",             datetime(2024, 12, 1), 0.80),   # A-extension — Meituan strategic
    ("B",              datetime(2025, 5, 1),  1.20),   # Series B — CATL, Ant, CICC
    ("B+/Strategic",   datetime(2025, 11, 1), 2.50),   # Late-2025 strategic — Alibaba
    ("C / pre-IPO",    datetime(2026, 3, 1),  4.00),   # Press-reported C / pre-IPO mark
]

dates = [r[1] for r in rounds]
vals = [r[2] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dates, vals, marker="o", linewidth=2.5, color="#7a3cff", markersize=9)
for d, v, lab in zip(dates, vals, labels):
    ax.annotate(f"{lab}\n${v:.2f}B", (d, v),
                textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9)

ax.set_title("Galbot (银河通用) Reported Post-Money Valuation by Round",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Post-money valuation (USD billion, approx.)")
ax.set_ylim(0, 5)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: 36Kr, Caixin, Late Post (晚点LatePost), IT桔子, Bloomberg press reports (2023-2026). "
         "Approximate / press-cited; not officially confirmed by Galbot.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/galbot_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved galbot_funding_trajectory.png")
