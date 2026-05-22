"""Deep Robotics (云深处科技) disclosed funding-round valuations.

Values are press-reported / IT桔子 approximations; not officially confirmed by the company.
Series C closed in late 2024 led by Tencent and Lenovo Capital; further strategic
rounds in 2025 carried higher marks per Caixin / 36Kr reporting.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

rounds = [
    ("Angel",       datetime(2017, 11, 1), 0.02),   # ~RMB 10s of M
    ("Pre-A",       datetime(2019,  6, 1), 0.05),
    ("A",           datetime(2020,  6, 1), 0.10),
    ("B",           datetime(2021,  9, 1), 0.25),
    ("B+",          datetime(2022, 12, 1), 0.40),
    ("C",           datetime(2024,  9, 1), 0.80),
    ("C+/Strategic", datetime(2025, 11, 1), 1.40),  # press-reported pre-IPO mark
]

dates = [r[1] for r in rounds]
vals = [r[2] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dates, vals, marker="o", linewidth=2.5, color="#c0392b", markersize=9)
for d, v, lab in zip(dates, vals, labels):
    ax.annotate(f"{lab}\n${v:.2f}B", (d, v),
                textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9)

ax.set_title("Deep Robotics (云深处科技) Reported Post-Money Valuation by Round",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Post-money valuation (USD billion, approx.)")
ax.set_ylim(0, 1.7)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: IT桔子, 36Kr, Caixin, Tencent / Lenovo Capital press releases (2017-2026). "
         "Press-cited and approximate; not officially confirmed by Deep Robotics.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/deeprobotics_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved")
