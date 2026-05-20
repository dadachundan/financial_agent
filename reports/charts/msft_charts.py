"""Microsoft (MSFT) initiation-coverage charts.

Data sources: see citations in the report. Each chart is saved to
reports/charts/msft_<name>.png.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ----------------------------------------------------------------------
# Chart 1 — Revenue + Operating Margin trend (FY2021–FY2025)
# Source: MSFT 10-K filings (financials per 2025 10-K page F-? & yfinance)
# FY2021 rev: $168,088M (from FY21 10-K), op inc: $69,916M
# FY2022 rev: $198,270M, op inc: $83,383M
# FY2023 rev: $211,915M, op inc: $88,523M
# FY2024 rev: $245,122M, op inc: $109,433M
# FY2025 rev: $281,724M, op inc: $128,528M
# ----------------------------------------------------------------------
years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
revenue = [168.088, 198.270, 211.915, 245.122, 281.724]  # $B
op_income = [69.916, 83.383, 88.523, 109.433, 128.528]  # $B
op_margin = [oi / r * 100 for oi, r in zip(op_income, revenue)]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
bars = ax1.bar(years, revenue, color="#0078D4", alpha=0.85, label="Revenue ($B)")
ax1.set_xlabel("Fiscal year (ended June 30)")
ax1.set_ylabel("Revenue ($B)", color="#0078D4")
ax1.tick_params(axis="y", labelcolor="#0078D4")
ax1.set_ylim(0, 320)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 5, f"${v:.1f}B",
             ha="center", fontsize=9, color="#0078D4", fontweight="bold")

ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#107C10", marker="o", lw=2.5,
         label="Operating margin (%)")
ax2.set_ylabel("Operating margin (%)", color="#107C10")
ax2.tick_params(axis="y", labelcolor="#107C10")
ax2.set_ylim(35, 50)
for x, y in zip(years, op_margin):
    ax2.text(x, y + 0.4, f"{y:.1f}%", ha="center", fontsize=9,
             color="#107C10", fontweight="bold")

plt.title("Microsoft — Revenue and Operating Margin Trend, FY2021–FY2025",
          fontsize=13, fontweight="bold")
fig.tight_layout()
plt.savefig(OUT / "msft_revenue_margin_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# Chart 2 — Segment revenue mix FY2023 → FY2025 (stacked bar)
# Restated segments: P&BP, IC, MPC (Aug-2024 restatement)
# FY23: P&BP $69.3B (legacy) — use restated where available
# FY23 / FY24 / FY25 restated: from MSFT FY25 10-K segment table
# FY24 restated: P&BP $106.8B, IC $87.5B, MPC $50.8B = $245.1B
# FY25:         P&BP $120.8B, IC $106.3B, MPC $54.6B = $281.7B
# FY23 restated: from FY24 10-K (filed July 2024 reflects new structure) —
# values approximated from product-detail table; we show FY24 & FY25 only
# to avoid mixing old/new segment boundaries.
# ----------------------------------------------------------------------
segs = ["Productivity\n& Business Processes", "Intelligent Cloud",
        "More Personal\nComputing"]
fy24 = [106.820, 87.464, 50.838]
fy25 = [120.810, 106.265, 54.649]

x = np.arange(len(segs))
w = 0.36
fig, ax = plt.subplots(figsize=(10, 5.5))
b1 = ax.bar(x - w / 2, fy24, w, label="FY2024", color="#605E5C")
b2 = ax.bar(x + w / 2, fy25, w, label="FY2025", color="#0078D4")
for bars, vals in [(b1, fy24), (b2, fy25)]:
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"${v:.1f}B",
                ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(segs)
ax.set_ylabel("Revenue ($B)")
ax.set_ylim(0, 145)
ax.legend(loc="upper right")
ax.set_title("Microsoft — Segment Revenue, FY2024 vs FY2025",
             fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
plt.savefig(OUT / "msft_segment_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# Chart 3 — Azure & other cloud services growth rate (constant currency)
# Quarterly disclosures from MSFT earnings press releases
# ----------------------------------------------------------------------
quarters = [
    "Q1 FY24", "Q2 FY24", "Q3 FY24", "Q4 FY24",
    "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25",
    "Q1 FY26", "Q2 FY26", "Q3 FY26",
]
# Azure cc growth %
azure_cc = [28, 30, 31, 30, 34, 31, 33, 39, 39, 38, 39]
# Azure reported growth %
azure_rep = [29, 30, 31, 29, 33, 31, 33, 39, 40, 39, 40]

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(quarters, azure_rep, marker="o", lw=2.5, color="#0078D4",
        label="Azure & other cloud services — reported YoY %")
ax.plot(quarters, azure_cc, marker="s", lw=2.5, color="#FFB900",
        label="Azure & other cloud services — constant currency YoY %")
for x, y in zip(quarters, azure_rep):
    ax.text(x, y + 0.6, f"{y}%", ha="center", fontsize=8, color="#0078D4")
ax.set_ylabel("Year-over-year growth (%)")
ax.set_ylim(20, 45)
ax.grid(axis="y", alpha=0.3)
ax.set_title("Microsoft — Azure Growth (reported and constant currency), FY24 Q1–FY26 Q3",
             fontsize=13, fontweight="bold")
ax.legend(loc="lower right")
plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
fig.tight_layout()
plt.savefig(OUT / "msft_azure_growth.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# Chart 4 — Capital expenditures by fiscal year (additions to P&E)
# ----------------------------------------------------------------------
fy_labels = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26E"]
# FY21: 20,622 ; FY22: 23,886 ; FY23: 28,107 ; FY24: 44,477 ; FY25: 64,551
# FY26E: see Q3 FY26 disclosures — capex ~$31.9B in Q3 alone; we mark guidance
capex = [20.622, 23.886, 28.107, 44.477, 64.551, 120.0]  # FY26E ~$120B implied
bars_colors = ["#605E5C"] * 5 + ["#D13438"]
fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(fy_labels, capex, color=bars_colors)
for b, v in zip(bars, capex):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, f"${v:.1f}B",
            ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Additions to property and equipment ($B)")
ax.set_ylim(0, 150)
ax.set_title("Microsoft — Capital Expenditures by Fiscal Year (FY26 implied from Q1–Q3 actuals + Q4 run-rate)",
             fontsize=12, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
plt.savefig(OUT / "msft_capex.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# Chart 5 — Peer TTM P/E and P/S comparison (MSFT vs GOOG, ORCL, AMZN, AAPL)
# Source: yfinance pull on 2026-05-20
# ----------------------------------------------------------------------
peers = ["MSFT", "GOOG", "ORCL", "AMZN", "AAPL"]
pe = [25.0, 29.2, 33.2, 32.2, 36.6]
ps = [9.8, 11.0, 8.3, 3.8, 9.8]

x = np.arange(len(peers))
w = 0.36
fig, ax1 = plt.subplots(figsize=(10, 5.5))
b1 = ax1.bar(x - w / 2, pe, w, label="TTM P/E", color="#0078D4")
b2 = ax1.bar(x + w / 2, ps, w, label="TTM P/S", color="#FFB900")
for bars, vals in [(b1, pe), (b2, ps)]:
    for b, v in zip(bars, vals):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.1f}×",
                 ha="center", fontsize=9, fontweight="bold")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
ax1.set_ylabel("Multiple (×)")
ax1.set_ylim(0, 42)
ax1.legend(loc="upper right")
ax1.set_title("Microsoft vs Peers — TTM P/E and P/S (data: 2026-05-20)",
              fontsize=13, fontweight="bold")
ax1.grid(axis="y", alpha=0.3)
fig.tight_layout()
plt.savefig(OUT / "msft_peer_multiples.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# Chart 6 — Microsoft Cloud revenue trend (annual, $B)
# FY23 $111.6B, FY24 $137.7B, FY25 $168.9B (from 10-K)
# Quarterly: Q1 FY26 $49.1B, Q2 FY26 $51.5B, Q3 FY26 $54.5B
# ----------------------------------------------------------------------
yrs = ["FY23", "FY24", "FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
mc = [111.6, 137.7, 168.9, 49.1, 51.5, 54.5]
colors = ["#0078D4"] * 3 + ["#605E5C"] * 3
fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(yrs, mc, color=colors)
for b, v in zip(bars, mc):
    ax.text(b.get_x() + b.get_width() / 2, v + 2.5, f"${v:.1f}B",
            ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Microsoft Cloud revenue ($B)")
ax.set_ylim(0, 200)
ax.set_title("Microsoft Cloud — Annual (FY23-25) and Recent Quarterly Revenue",
             fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
plt.savefig(OUT / "msft_cloud_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

print("All 6 charts written to", OUT)
