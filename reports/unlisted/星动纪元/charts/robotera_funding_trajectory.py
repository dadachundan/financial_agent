"""Robotera (星动纪元) funding-round valuation trajectory."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Implied post-money valuations (USD bn). Most rounds before A+ have no
# officially disclosed post-money; figures are press estimates / implied
# from round size + sector dilution norms — flagged in source caption.
rounds = [
    ("Seed",        datetime(2023, 10, 1), 0.05),   # press: ~RMB 0.3bn implied
    ("Angel",       datetime(2024,  1, 1), 0.12),   # >RMB 100m, Lenovo-led
    ("Pre-A",       datetime(2024, 10, 1), 0.35),   # ~RMB 300m, Alibaba co-led
    ("A",           datetime(2025,  7, 1), 0.70),   # ~RMB 500m, CDH VGC + Haier
    ("A+",          datetime(2025, 11, 1), 1.45),   # ~RMB 1.0bn, Geely-led; $1.45bn post per Caproasia
    ("Strategic",   datetime(2026,  3, 1), 2.50),   # ~RMB 1.0bn add-on; press marks
    ("B (May 2026)", datetime(2026, 5, 1), 3.50),   # >$200m, SF Group/HSG/IDG-led
]

dates = [r[1] for r in rounds]
vals = [r[2] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dates, vals, marker="o", linewidth=2.5, color="#d6336c", markersize=9)
for d, v, lab in zip(dates, vals, labels):
    ax.annotate(f"{lab}\n${v:.2f}B", (d, v),
                textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9)

ax.set_title("Robotera (Xingdong Jiyuan) Reported / Implied Post-Money Valuation by Round",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Post-money valuation (USD billion, approx.)")
ax.set_ylim(0, 4.2)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: Caproasia, Caixin Global, Yicai Global, Humanoids Daily, finsmes, 36Kr, IT桔子 (2023-2026). "
         "All values press-cited / implied; Robotera has not officially disclosed post-money figures.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/robotera_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved")
