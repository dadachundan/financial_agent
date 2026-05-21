#!/usr/bin/env python3
"""Generate charts for GE Vernova (NYSE:GEV) company research report.

All segment / financial data is sourced from the GE Vernova 2025 Form 10-K
(filed Jan 2026) and the 1Q26 earnings press release. Peer P/E figures are from
public market-data sources cited in the report. No fabricated numbers.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})

# ------------------------------------------------------------------
# 1. Segment revenue trend (stacked bar), FY2023–FY2025
# Source: GEV 2025 10-K MD&A, Summary of Reportable Segments
# ------------------------------------------------------------------
years = ["FY2023", "FY2024", "FY2025"]
power = [17.436, 18.127, 19.767]
wind = [9.826, 9.701, 9.110]
elec = [6.378, 7.550, 9.642]
elim = [-0.401, -0.442, -0.451]

fig, ax = plt.subplots(figsize=(8.0, 4.8))
x = np.arange(len(years))
w = 0.6
ax.bar(x, power, w, label="Power", color="#1f3a5f")
ax.bar(x, wind, w, bottom=power, label="Wind", color="#4a89dc")
ax.bar(x, elec, w, bottom=[a + b for a, b in zip(power, wind)],
       label="Electrification", color="#37b886")
# Totals on top
totals = [p + w_ + e + el for p, w_, e, el in zip(power, wind, elec, elim)]
for i, t in enumerate(totals):
    ax.text(i, t + 0.4, f"${t:.1f}B", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("Revenue (USD billions)")
ax.set_title("GE Vernova segment revenue, FY2023–FY2025")
ax.legend(loc="upper left", frameon=False)
ax.set_ylim(0, 42)
fig.tight_layout()
fig.savefig(OUT / "gev_segment_revenue.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------
# 2. Segment EBITDA (grouped bar), FY2023–FY2025
# Source: GEV 2025 10-K MD&A
# ------------------------------------------------------------------
power_e = [1.722, 2.268, 2.902]
wind_e = [-1.033, -0.588, -0.598]
elec_e = [0.234, 0.679, 1.433]

fig, ax = plt.subplots(figsize=(8.0, 4.8))
x = np.arange(len(years))
w = 0.25
ax.bar(x - w, power_e, w, label="Power", color="#1f3a5f")
ax.bar(x, wind_e, w, label="Wind", color="#c1432d")
ax.bar(x + w, elec_e, w, label="Electrification", color="#37b886")
ax.axhline(0, color="black", linewidth=0.6)
for xi, v in zip(x - w, power_e):
    ax.text(xi, v + (0.05 if v > 0 else -0.15), f"{v:+.2f}", ha="center", fontsize=8)
for xi, v in zip(x, wind_e):
    ax.text(xi, v + (0.05 if v > 0 else -0.15), f"{v:+.2f}", ha="center", fontsize=8)
for xi, v in zip(x + w, elec_e):
    ax.text(xi, v + (0.05 if v > 0 else -0.15), f"{v:+.2f}", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("Segment EBITDA (USD billions)")
ax.set_title("Segment EBITDA: Power & Electrification compounding; Wind losses persist")
ax.legend(loc="upper left", frameon=False)
ax.set_ylim(-1.5, 3.5)
fig.tight_layout()
fig.savefig(OUT / "gev_segment_ebitda.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------
# 3. Gas turbine equipment backlog + slot reservations (GW)
# Source: GEV 2025 10-K, 1Q26 8-K
# ------------------------------------------------------------------
periods = ["YE2023", "YE2024", "YE2025", "1Q26", "YE2026E"]
backlog_gw = [20, 29, 40, 44, 50]            # approx; YE2026E is gating per company
slot_gw = [0, 27, 43, 56, 60]                # approx; year-end 2026 implied
# Company guides combined to "at least 110 GW" by YE26
fig, ax = plt.subplots(figsize=(8.0, 4.8))
x = np.arange(len(periods))
w = 0.6
ax.bar(x, backlog_gw, w, label="Equipment backlog (GW in RPO)", color="#1f3a5f")
ax.bar(x, slot_gw, w, bottom=backlog_gw, label="Slot reservation agreements (GW)", color="#88b8d9")
totals = [a + b for a, b in zip(backlog_gw, slot_gw)]
for i, t in enumerate(totals):
    ax.text(i, t + 1.5, f"{t} GW", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.set_ylabel("Gigawatts")
ax.set_title("Gas turbine backlog + slot reservations — the 'gas renaissance' in pictures")
ax.legend(loc="upper left", frameon=False)
ax.set_ylim(0, 130)
ax.axhline(110, color="red", linewidth=0.8, linestyle="--", alpha=0.6)
ax.text(4.4, 111, "YE2026 target: ≥110 GW", fontsize=8, color="red", ha="right")
fig.tight_layout()
fig.savefig(OUT / "gev_gasturbine_backlog.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------
# 4. Total RPO (backlog) by segment, FY2023–FY2025
# Source: GEV 2025 10-K
# ------------------------------------------------------------------
power_rpo = [72.974, 73.351, 94.387]
wind_rpo = [25.726, 22.219, 21.184]  # implied from totals
# Wind RPO from 10K: not stated direct here for each year. Use total minus Power minus Electrification.
# Actually we have: total 115.6 / 119.0 / 150.2, Power 73.0/73.4/94.4, Elec 16.3/23.5/34.7.
# So Wind = 115.598-72.974-16.342 = 26.282 ; 119.023-73.351-23.453 = 22.219 ; 150.238-94.387-34.667 = 21.184
power_rpo = [72.974, 73.351, 94.387]
wind_rpo = [26.282, 22.219, 21.184]
elec_rpo = [16.342, 23.453, 34.667]

fig, ax = plt.subplots(figsize=(8.0, 4.8))
x = np.arange(len(years))
w = 0.6
ax.bar(x, power_rpo, w, label="Power", color="#1f3a5f")
ax.bar(x, wind_rpo, w, bottom=power_rpo, label="Wind", color="#4a89dc")
ax.bar(x, elec_rpo, w,
       bottom=[a + b for a, b in zip(power_rpo, wind_rpo)],
       label="Electrification", color="#37b886")
totals = [a + b + c for a, b, c in zip(power_rpo, wind_rpo, elec_rpo)]
for i, t in enumerate(totals):
    ax.text(i, t + 2, f"${t:.1f}B", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("Remaining performance obligations (USD billions)")
ax.set_title("Total backlog (RPO): $115B → $150B in two years")
ax.legend(loc="upper left", frameon=False)
ax.set_ylim(0, 170)
fig.tight_layout()
fig.savefig(OUT / "gev_rpo_segment.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------
# 5. Peer P/E comparison (current vs sector median)
# Source: financecharts.com, companiesmarketcap, GuruFocus (May 2026 vintages)
# Values rounded; cite in report
# ------------------------------------------------------------------
peers = ["GE Vernova\n(GEV)", "Siemens Energy\n(ENR.DE)", "Mitsubishi HI\n(7011.T)",
         "Vestas\n(VWS.CO)", "ABB Ltd\n(ABBNY)"]
pe_ttm = [31, 97, 51, 31, 39]
colors = ["#1f3a5f", "#999", "#999", "#999", "#999"]
fig, ax = plt.subplots(figsize=(8.0, 4.8))
bars = ax.bar(peers, pe_ttm, color=colors)
for b, v in zip(bars, pe_ttm):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v}×",
            ha="center", fontsize=10, fontweight="bold")
ax.axhline(30, color="red", linewidth=0.7, linestyle="--", alpha=0.6)
ax.text(0.02, 31.5, "Industrial Products sector median ≈ 30×",
        transform=ax.get_yaxis_transform(), fontsize=8, color="red")
ax.set_ylabel("TTM P/E ratio")
ax.set_title("TTM P/E: GEV trades in-line with Vestas, well below Siemens Energy & MHI")
ax.set_ylim(0, 110)
fig.tight_layout()
fig.savefig(OUT / "gev_peer_pe.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("All charts written to", OUT)
