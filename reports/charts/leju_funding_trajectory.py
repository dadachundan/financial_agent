"""Leju Robotics (乐聚机器人) disclosed funding-round valuations.

Values are press-reported / IT桔子 approximations; not officially confirmed by the company.
Leju was founded 2016 in Harbin / Shenzhen out of the HIT (Harbin Institute of Technology)
humanoid robotics group; investors include Tencent, BYD, Lenovo, SAIC, China Mobile and
Harbin / Shenzhen state-linked vehicles. Reported pre-IPO mark in late 2025 placed the
company at roughly RMB 6-7B (~USD 850M-1.0B).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

rounds = [
    ("Angel",        datetime(2016,  7, 1), 0.015),  # ~RMB 10s of M
    ("Pre-A",        datetime(2017, 10, 1), 0.05),
    ("A",            datetime(2018, 12, 1), 0.08),
    ("B",            datetime(2020,  9, 1), 0.18),
    ("B+",           datetime(2022,  6, 1), 0.30),
    ("C",            datetime(2024,  7, 1), 0.55),   # Tencent / SAIC / Lenovo participation
    ("C+/Strategic", datetime(2025, 11, 1), 0.95),   # press-reported pre-IPO mark
]

dates = [r[1] for r in rounds]
vals = [r[2] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dates, vals, marker="o", linewidth=2.5, color="#16a085", markersize=9)
for d, v, lab in zip(dates, vals, labels):
    ax.annotate(f"{lab}\n${v:.2f}B", (d, v),
                textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9)

ax.set_title("Leju Robotics (乐聚机器人) Reported Post-Money Valuation by Round",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Post-money valuation (USD billion, approx.)")
ax.set_ylim(0, 1.2)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: IT桔子, 36Kr, Caixin, Tencent Investment / SAIC / Lenovo Capital press releases (2016-2026). "
         "Press-cited and approximate; not officially confirmed by Leju Robotics.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/leju_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved")
