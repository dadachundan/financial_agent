"""LimX Dynamics (逐际动力) funding-round trajectory."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Cumulative raise (USD m). Post-money not officially disclosed for most rounds;
# implied marks are press-cited and flagged as such.
rounds = [
    ("Seed",          datetime(2022,  6, 1),  10,   30),
    ("Angel + Pre-A", datetime(2023, 10, 1),  37,  150),   # ~RMB 200m total
    ("Series A",      datetime(2024,  7, 1), 100,  400),   # ~RMB 500m cum.
    ("Series A+",     datetime(2025,  3, 1), 170,  650),   # RMB 500m cum. A series
    ("Strategic",     datetime(2025,  7, 1), 200,  900),   # JD.com + Alibaba
    ("Series B",      datetime(2026,  2, 1), 400, 1500),   # +$200m → ~$1.5B implied
]

dates = [r[1] for r in rounds]
cum_raise = [r[2] for r in rounds]
implied_val = [r[3] for r in rounds]
labels = [r[0] for r in rounds]

fig, ax1 = plt.subplots(figsize=(10, 5.5))

color1 = "#d6336c"
ax1.set_xlabel("Round date")
ax1.set_ylabel("Cumulative capital raised (USD million)", color=color1)
ax1.plot(dates, cum_raise, marker="o", linewidth=2.5, color=color1, markersize=9, label="Cumulative raise")
ax1.tick_params(axis="y", labelcolor=color1)
for d, v, lab in zip(dates, cum_raise, labels):
    ax1.annotate(f"{lab}\n${v}M", (d, v),
                 textcoords="offset points", xytext=(0, 12),
                 ha="center", fontsize=8, color=color1)

ax2 = ax1.twinx()
color2 = "#2b8a3e"
ax2.set_ylabel("Implied post-money valuation (USD million)", color=color2)
ax2.plot(dates, implied_val, marker="s", linewidth=2, color=color2, linestyle="--", label="Implied post-money")
ax2.tick_params(axis="y", labelcolor=color2)

ax1.set_title("LimX Dynamics (逐际动力) — Cumulative Raise & Implied Valuation (2022–2026)",
              fontsize=13, fontweight="bold")
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
fig.autofmt_xdate()

fig.text(0.5, -0.02,
         "Sources: Yicai Global, Gasgoo, TechNode, Caixin Global, The Robot Report, NIO Capital, LimX Dynamics press (2023–2026). "
         "Implied valuations are press-cited / approximate — LimX has not officially disclosed post-money figures.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/limx_funding_trajectory.png",
            dpi=150, bbox_inches="tight")
print("saved")
