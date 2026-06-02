"""Visa (NYSE:V) — 3-year net revenue, GAAP operating margin, and segment-revenue mix charts.

Inputs are taken from Visa's FY2025 10-K (filed Nov 2025) and FY2025 Q4 earnings release.
Run from project root:
    cd /Users/x/projects/financial_agent && python3 reports/charts/visa_revenue_trend.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# FY2023 / FY2024 / FY2025 figures from the 10-K Item 7 MD&A revenue table.
YEARS = ["FY2023", "FY2024", "FY2025"]
NET_REVENUE = [32.653, 35.926, 40.000]            # USD bn
OPERATING_INCOME = [21.000, 23.595, 23.994]       # net rev - GAAP opex
OPERATING_MARGIN = [64.3, 65.7, 60.0]             # GAAP, percent

SERVICE_REV = [16.007, 17.714, 19.778]            # USD bn  (10-K)
DATA_PROC_REV = [16.221, 18.124, 21.754]
INTL_TRANS_REV = [11.638, 12.665, 14.166]
OTHER_REV = [2.479, 3.197, 4.053]
CLIENT_INCENTIVES = [-12.297, -13.764, -15.751]

# ---------- Chart 1: Net revenue & operating margin --------------------------
fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
x = np.arange(len(YEARS))
bars = ax1.bar(x, NET_REVENUE, width=0.55, color="#1A1F71", label="Net revenue (USD bn)")
ax1.set_ylabel("Net revenue (USD bn)", color="#1A1F71")
ax1.set_xticks(x)
ax1.set_xticklabels(YEARS)
for i, v in enumerate(NET_REVENUE):
    ax1.text(i, v + 0.7, f"${v:.1f}B", ha="center", fontsize=10, color="#1A1F71", fontweight="bold")
ax1.set_ylim(0, 50)
ax1.tick_params(axis="y", labelcolor="#1A1F71")

ax2 = ax1.twinx()
ax2.plot(x, OPERATING_MARGIN, marker="o", color="#F7B600", linewidth=2.4, label="GAAP operating margin (%)")
ax2.set_ylabel("GAAP operating margin (%)", color="#F7B600")
ax2.set_ylim(50, 75)
for i, v in enumerate(OPERATING_MARGIN):
    ax2.text(i, v + 0.6, f"{v:.1f}%", ha="center", fontsize=9, color="#F7B600", fontweight="bold")
ax2.tick_params(axis="y", labelcolor="#F7B600")

plt.title("Visa Inc. (NYSE:V) — Net Revenue & GAAP Operating Margin, FY2023–FY2025", fontsize=11)
plt.tight_layout()
plt.savefig(OUT / "visa_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 2: Stacked revenue mix (gross, before client incentives) ---
fig, ax = plt.subplots(figsize=(8.5, 4.8))
bottom_acc = np.zeros(len(YEARS))
for label, vals, color in [
    ("Service revenue", SERVICE_REV, "#1A1F71"),
    ("Data processing", DATA_PROC_REV, "#0070BA"),
    ("Intl. transaction", INTL_TRANS_REV, "#F7B600"),
    ("Other revenue", OTHER_REV, "#F26522"),
]:
    ax.bar(x, vals, bottom=bottom_acc, width=0.55, label=label, color=color)
    bottom_acc += np.array(vals)

# Negative bar: client incentives
ax.bar(x, CLIENT_INCENTIVES, width=0.55, label="Client incentives (offset)", color="#888")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels(YEARS)
ax.set_ylabel("USD bn (gross & offsets)")
ax.set_title("Visa Inc. — Gross Revenue Mix and Client Incentives, FY2023–FY2025", fontsize=11)
ax.legend(loc="upper left", fontsize=9, ncol=2)

# Net revenue line for context
for i, nr in enumerate(NET_REVENUE):
    ax.text(i, nr + 1, f"Net ${nr:.1f}B", ha="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT / "visa_revenue_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 3: VAS revenue trajectory ---------------------------------
vas_years = ["FY2023", "FY2024", "FY2025"]
vas_rev = [7.2, 8.8, 10.9]
fig, ax = plt.subplots(figsize=(8.5, 4.4))
bars = ax.bar(vas_years, vas_rev, color="#0070BA", width=0.5)
for i, v in enumerate(vas_rev):
    ax.text(i, v + 0.2, f"${v:.1f}B", ha="center", fontsize=11, color="#0070BA", fontweight="bold")
ax.set_ylabel("VAS revenue (USD bn)")
ax.set_ylim(0, 14)
# Annotation for opportunity
ax.axhline(10.9, color="grey", linestyle="--", linewidth=0.6)
ax.set_title("Visa Value-Added Services (VAS) Revenue — Inside a $520B Stated TAM", fontsize=11)
ax.text(2.4, 12.5, "$520B TAM (Investor Day 2025)", fontsize=9, color="#444", ha="right")
plt.tight_layout()
plt.savefig(OUT / "visa_vas_growth.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 4: Network competitor scale, CY2024 -----------------------
networks = ["Visa", "Mastercard", "American Express", "Diners/Discover", "JCB"]
payments_volume_bn = [13433, 8014, 1750, 253, 319]  # $B
cards_m = [4805, 3146, 147, 72, 167]
fig, ax = plt.subplots(figsize=(9, 4.6))
x = np.arange(len(networks))
ax.bar(x - 0.2, payments_volume_bn, width=0.4, label="Payments volume (USD bn, CY2024)", color="#1A1F71")
ax2 = ax.twinx()
ax2.bar(x + 0.2, cards_m, width=0.4, label="Cards (M)", color="#F7B600")
ax.set_xticks(x)
ax.set_xticklabels(networks, rotation=10)
ax.set_ylabel("Payments volume (USD bn)", color="#1A1F71")
ax2.set_ylabel("Cards in circulation (M)", color="#F7B600")
ax.set_title("Network Scale — Visa vs. Major Global Networks, CY2024 (Nilson 1288 / Visa 10-K)", fontsize=10.5)
ax.legend(loc="upper right", fontsize=9)
ax2.legend(loc="upper center", fontsize=9)
for i, v in enumerate(payments_volume_bn):
    ax.text(i - 0.2, v + 200, f"${v/1000:.1f}T" if v >= 1000 else f"${v}B", ha="center", fontsize=8.5, color="#1A1F71")
plt.tight_layout()
plt.savefig(OUT / "visa_network_scale.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts saved:")
for f in ["visa_revenue_margin.png", "visa_revenue_mix.png", "visa_vas_growth.png", "visa_network_scale.png"]:
    p = OUT / f
    print(f"  {p} ({p.stat().st_size//1024} KB)")
