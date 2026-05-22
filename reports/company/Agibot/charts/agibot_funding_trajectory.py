"""Agibot (智元机器人) funding-round valuation trajectory."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

rounds = [
    ("Seed",        datetime(2023, 5, 1),  0.15),  # ~RMB 1bn implied @ ~$150M
    ("Angel/A1",    datetime(2023, 8, 1),  0.30),
    ("A+",          datetime(2024, 3, 1),  0.70),
    ("B",           datetime(2024, 9, 1),  1.20),
    ("B+",          datetime(2025, 1, 1),  1.50),
    ("C",           datetime(2025, 7, 1),  2.50),
    ("Strategic",   datetime(2026, 2, 1),  6.00),  # press-reported pre-IPO mark
]

dates = [r[1] for r in rounds]
vals = [r[2] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dates, vals, marker="o", linewidth=2.5, color="#0b5fff", markersize=9)
for d, v, lab in zip(dates, vals, labels):
    ax.annotate(f"{lab}\n${v:.1f}B", (d, v),
                textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9)

ax.set_title("Agibot (Zhiyuan Robotics) Reported Post-Money Valuation by Round",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Post-money valuation (USD billion, approx.)")
ax.set_ylim(0, 7)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: ITjuzi, 36Kr, Caixin, Bloomberg press reports (2023-2026). "
         "Approximate / press-cited; not officially confirmed by Agibot.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/agibot_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved")
