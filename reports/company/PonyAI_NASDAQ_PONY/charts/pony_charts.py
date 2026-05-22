"""Charts for Pony.ai (NASDAQ:PONY) initiation research note.

All figures pulled from:
- Pony AI Inc. Form 20-F for FY2025 (filed 2026-04-22, SEC accession 0001104659-26-046406)
- Q4 / FY2025 unaudited earnings release (filed 2026-03-26, 6-K accession 0001104659-26-034888)
- Yahoo Finance / yfinance snapshot 2026-05-20 for peer P/S multiples.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

# -- Chart 1: Revenue + Gross margin trend (2023 / 2024 / 2025) ----------------
years = ["2023", "2024", "2025"]
rev = [71.9, 75.0, 90.0]              # USDm, 20-F
gross = [16.9, 11.4, 14.2]            # USDm, 20-F
gm_pct = [23.5, 15.2, 15.7]           # %, 20-F

fig, ax1 = plt.subplots(figsize=(8, 4.6))
bar = ax1.bar(years, rev, color="#1f3b73", alpha=0.85, label="Revenue (US$ m)")
ax1.set_ylabel("Revenue (US$ m)", color="#1f3b73", fontsize=11)
ax1.set_ylim(0, max(rev) * 1.25)
ax1.tick_params(axis="y", labelcolor="#1f3b73")
for b, v in zip(bar, rev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}", ha="center", fontsize=10, color="#1f3b73")

ax2 = ax1.twinx()
ax2.plot(years, gm_pct, color="#c0392b", marker="o", linewidth=2.2, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color="#c0392b", fontsize=11)
ax2.set_ylim(0, 35)
ax2.tick_params(axis="y", labelcolor="#c0392b")
for x, v in zip(years, gm_pct):
    ax2.text(x, v + 1.2, f"{v:.1f}%", ha="center", fontsize=10, color="#c0392b")

plt.title("Pony.ai (NASDAQ: PONY) — Revenue & Gross Margin, FY2023–FY2025", fontsize=12)
fig.tight_layout()
plt.savefig(OUT / "pony_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# -- Chart 2: Revenue mix by segment (stacked bar) -----------------------------
robotaxi = [7.7, 7.3, 16.6]
robotruck = [25.0, 40.4, 40.6]
licensing = [39.2, 27.4, 32.8]

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(years, robotaxi, label="Robotaxi services", color="#2e86de")
ax.bar(years, robotruck, bottom=robotaxi, label="Robotruck services", color="#10ac84")
bot2 = [a + b for a, b in zip(robotaxi, robotruck)]
ax.bar(years, licensing, bottom=bot2, label="Licensing & applications", color="#f39c12")

totals = [a + b + c for a, b, c in zip(robotaxi, robotruck, licensing)]
for x, t in zip(years, totals):
    ax.text(x, t + 1.2, f"${t:.1f}m", ha="center", fontsize=10)

ax.set_ylabel("Revenue (US$ m)", fontsize=11)
ax.set_ylim(0, max(totals) * 1.18)
ax.set_title("Pony.ai — Revenue Mix by Business Line, FY2023–FY2025", fontsize=12)
ax.legend(loc="upper left", fontsize=9, frameon=False)
fig.tight_layout()
plt.savefig(OUT / "pony_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# -- Chart 3: Operating loss + R&D intensity -----------------------------------
op_loss = [143.2, 285.5, 260.9]  # USDm
rd = [122.7, 240.2, 217.4]       # USDm
sga = [37.4, 56.7, 57.6]         # USDm
sbc = [3.8, 127.0, 30.8]         # USDm (R&D + SG&A SBC) — 2024 inflated by IPO

x = np.arange(len(years))
w = 0.35
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(x - w / 2, rd, w, label="R&D expense", color="#5758BB")
ax.bar(x + w / 2, sga, w, label="SG&A expense", color="#A29BFE")
ax.plot(x, op_loss, marker="s", color="#c0392b", linewidth=2, label="Operating loss")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("US$ m", fontsize=11)
ax.set_title("Pony.ai — R&D, SG&A and Operating Loss, FY2023–FY2025", fontsize=12)
ax.legend(loc="upper left", fontsize=9, frameon=False)
for xi, v in zip(x, op_loss):
    ax.text(xi, v + 6, f"{v:.0f}", ha="center", fontsize=9, color="#c0392b")
fig.tight_layout()
plt.savefig(OUT / "pony_rd_opex.png", dpi=150, bbox_inches="tight")
plt.close()

# -- Chart 4: Quarterly Robotaxi revenue progression (Q4-24 vs Q4-25 + FY) -----
labels = ["Q4 2024", "Q4 2025", "FY 2024", "FY 2025"]
robotaxi_q = [2.6, 6.7, 7.3, 16.6]
fare_pct = ["", "+500% fare YoY", "", "+400% fare YoY"]

fig, ax = plt.subplots(figsize=(8, 4.6))
colors = ["#bdc3c7", "#2980b9", "#bdc3c7", "#2980b9"]
bars = ax.bar(labels, robotaxi_q, color=colors)
ax.set_ylabel("Robotaxi services revenue (US$ m)", fontsize=11)
ax.set_title("Pony.ai Robotaxi Revenue Acceleration — Q4-24 → Q4-25", fontsize=12)
for b, v, note in zip(bars, robotaxi_q, fare_pct):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.3, f"${v:.1f}m", ha="center", fontsize=10)
    if note:
        ax.text(b.get_x() + b.get_width() / 2, v + 1.4, note, ha="center", fontsize=8.5, color="#c0392b")
ax.set_ylim(0, max(robotaxi_q) * 1.4)
fig.tight_layout()
plt.savefig(OUT / "pony_robotaxi_q.png", dpi=150, bbox_inches="tight")
plt.close()

# -- Chart 5: Peer P/S TTM comparison (Yahoo Finance, 2026-05-20) --------------
peers = ["PONY", "WRD (WeRide)", "MBLY (Mobileye)", "TSLA", "GOOGL"]
ps = [42.1, 3.5, 4.1, 16.0, 11.2]
colors = ["#c0392b", "#e67e22", "#27ae60", "#2c3e50", "#2c3e50"]
fig, ax = plt.subplots(figsize=(8, 4.4))
bars = ax.barh(peers, ps, color=colors)
for b, v in zip(bars, ps):
    ax.text(v + 0.5, b.get_y() + b.get_height() / 2, f"{v:.1f}x", va="center", fontsize=10)
ax.set_xlabel("TTM Price / Sales (x)", fontsize=11)
ax.set_title("PONY vs L4 / AV-Adjacent Peers — TTM P/S (2026-05-20)", fontsize=12)
ax.set_xlim(0, max(ps) * 1.15)
ax.invert_yaxis()
fig.tight_layout()
plt.savefig(OUT / "pony_peer_ps.png", dpi=150, bbox_inches="tight")
plt.close()

# -- Chart 6: Robotaxi global TAM (analyst syntheses) --------------------------
# Numbers below sourced from McKinsey "Autonomous driving's future: Convenient
# and connected" (Jan 2023) and Goldman Sachs Research "Robotaxi: the next
# trillion-dollar opportunity?" (May 2024) — both publicly summarized.
years_t = [2025, 2027, 2030, 2035, 2040]
tam_low = [0.5, 5, 60, 250, 600]   # USD bn
tam_high = [1.5, 15, 150, 500, 1500]

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.fill_between(years_t, tam_low, tam_high, color="#3498db", alpha=0.3, label="Analyst range")
ax.plot(years_t, tam_low, color="#2c3e50", linestyle="--", marker="o", label="Low case")
ax.plot(years_t, tam_high, color="#c0392b", linestyle="-", marker="s", label="High case")
ax.set_yscale("log")
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Global robotaxi revenue (US$ bn, log)", fontsize=11)
ax.set_title("Global Robotaxi Revenue Pool — Analyst Forecast Range, 2025-2040", fontsize=12)
ax.legend(loc="upper left", fontsize=9, frameon=False)
ax.grid(True, which="both", linestyle="--", alpha=0.4)
fig.tight_layout()
plt.savefig(OUT / "pony_tam.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written:", sorted(p.name for p in OUT.glob("pony_*.png")))
