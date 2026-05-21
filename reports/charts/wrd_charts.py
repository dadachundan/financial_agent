"""Charts for WeRide (NASDAQ:WRD) company-research report."""
from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Chart 1: Revenue mix + gross margin trend (2023–2025)
# Source: WRD 2025 20-F (filed 2026), Item 5.A — Key Components of Results.
# Product revenue 54,190 / 87,710 / 359,843; Service 347,654 / 273,424 / 324,744.
# GM = 45.7% / 30.7% / 30.2%
years = [2023, 2024, 2025]
product = [54.190, 87.710, 359.843]      # RMB millions
service = [347.654, 273.424, 324.744]    # RMB millions
gm_pct  = [45.7, 30.7, 30.2]

fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
x = np.arange(len(years))
w = 0.55
ax1.bar(x, product, w, label="Product (vehicle sales)", color="#1f4e79")
ax1.bar(x, service, w, bottom=product, label="Service (ops, ADAS R&D, data)", color="#9dc3e6")
ax1.set_xticks(x)
ax1.set_xticklabels([str(y) for y in years])
ax1.set_ylabel("Revenue (RMB millions)")
ax1.set_ylim(0, 750)
ax1.set_title("WeRide — Revenue mix and gross margin, FY2023–FY2025")
for xi, p, s in zip(x, product, service):
    ax1.text(xi, p + s + 15, f"{p+s:,.0f}", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(x, gm_pct, color="#c00000", marker="o", lw=2.0, label="Gross margin (%)")
for xi, g in zip(x, gm_pct):
    ax2.text(xi, g + 1.5, f"{g:.1f}%", ha="center", fontsize=9, color="#c00000")
ax2.set_ylim(0, 60)
ax2.set_ylabel("Gross margin (%)", color="#c00000")
ax2.tick_params(axis="y", labelcolor="#c00000")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "wrd_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Chart 2: Fleet growth + cumulative cities (qualitative milestones)
# Source: WRD 2025 20-F Item 4.B: 1,089 vehicles at YE2024, 2,113 as of 2026-03-23;
# 1,125 robotaxi units; target 2,600 robotaxis by YE2026; >40 cities, 12 countries.
fig, ax = plt.subplots(figsize=(8.5, 4.4))
labels = ["YE2024\n(actual)", "Mar 2026\n(actual)", "YE2026\n(target)"]
total_fleet = [1089, 2113, None]
robotaxi    = [None, 1125, 2600]
xv = np.arange(len(labels))
ax.bar(xv - 0.18, [v if v else 0 for v in total_fleet], 0.36, label="Total AV fleet (all products)", color="#1f4e79")
ax.bar(xv + 0.18, [v if v else 0 for v in robotaxi], 0.36, label="Robotaxi sub-fleet", color="#ed7d31")
for xi, v in zip(xv - 0.18, total_fleet):
    if v: ax.text(xi, v + 60, f"{v:,}", ha="center", fontsize=9)
for xi, v in zip(xv + 0.18, robotaxi):
    if v: ax.text(xi, v + 60, f"{v:,}", ha="center", fontsize=9, color="#7a3a06")
ax.set_xticks(xv)
ax.set_xticklabels(labels)
ax.set_ylabel("Vehicles in service")
ax.set_ylim(0, 3000)
ax.set_title("WeRide — Global AV fleet and robotaxi sub-fleet build-out")
ax.legend(loc="upper left", fontsize=9, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "wrd_fleet_growth.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Chart 3: Operating loss vs. R&D spend (2023–2025)
# Source: WRD 2025 20-F Item 5.A.
op_loss = [1566.2, 2185.2, 1846.8]  # RMB m, absolute value
rd      = [1058.4, 1091.4, 1372.2]
adj_net = [501.7, 801.9, 1246.7]    # non-IFRS adjusted net loss

fig, ax = plt.subplots(figsize=(8.5, 4.4))
x = np.arange(len(years))
w = 0.27
ax.bar(x - w, rd, w, label="R&D expense", color="#1f4e79")
ax.bar(x, op_loss, w, label="Operating loss (abs.)", color="#c00000")
ax.bar(x + w, adj_net, w, label="Non-IFRS adj. net loss (abs.)", color="#a6a6a6")
ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years])
ax.set_ylabel("RMB millions")
ax.set_title("WeRide — R&D spend vs. operating and adjusted losses, 2023–2025")
for xi, v in zip(x - w, rd): ax.text(xi, v + 25, f"{v:,.0f}", ha="center", fontsize=8)
for xi, v in zip(x, op_loss): ax.text(xi, v + 25, f"{v:,.0f}", ha="center", fontsize=8, color="#7a0000")
for xi, v in zip(x + w, adj_net): ax.text(xi, v + 25, f"{v:,.0f}", ha="center", fontsize=8)
ax.legend(loc="upper left", fontsize=9, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "wrd_pl_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Chart 4: Peer valuation — P/S multiple (TTM)
# Source: Yahoo Finance, accessed 2026-05-20.
peers = ["WRD", "PONY", "TSLA", "GOOGL", "BIDU"]
ps    = [3.47, 42.10, 16.01, 11.15, 0.36]
colors = ["#1f4e79", "#1f4e79", "#a6a6a6", "#a6a6a6", "#a6a6a6"]
fig, ax = plt.subplots(figsize=(8.5, 4.2))
bars = ax.bar(peers, ps, color=colors)
for b, v in zip(bars, ps):
    ax.text(b.get_x() + b.get_width()/2, v + 0.8, f"{v:.1f}x", ha="center", fontsize=9)
ax.set_ylabel("TTM Price / Sales (x)")
ax.set_title("WeRide vs. peers — TTM P/S multiple (as of 2026-05-20)")
ax.set_ylim(0, 50)
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "wrd_peer_ps.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Chart 5: Global robotaxi TAM (illustrative scaling path)
# Sources: McKinsey "The future of autonomous vehicles" (2023, latest update); WeRide F-1 prospectus,
# Frost & Sullivan section; Goldman Sachs 2024 robotaxi note (cited via Reuters 2024-09-13).
# These are public-domain industry forecasts; we plot 2025 vs. 2030 vs. 2035 mid-case.
yrs = [2025, 2030, 2035]
tam = [3, 65, 280]  # USD billion, global robotaxi revenue (illustrative blended mid-case)
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(yrs, tam, marker="o", lw=2.2, color="#1f4e79")
for x_, y_ in zip(yrs, tam):
    ax.text(x_, y_ + 12, f"${y_}B", ha="center", fontsize=10)
ax.set_xticks(yrs)
ax.set_ylabel("Global robotaxi revenue (USD billions)")
ax.set_title("Global robotaxi TAM — illustrative scaling (industry mid-case)")
ax.grid(alpha=0.25)
ax.set_ylim(0, 350)
plt.tight_layout()
plt.savefig(OUT / "wrd_tam.png", dpi=150, bbox_inches="tight")
plt.close()

print("Wrote 5 charts to", OUT)
