#!/usr/bin/env python3
"""Generate Intel research charts from 10-K data (2023-2025) and Q1 2026."""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ---------- Chart 1: Revenue + Gross margin trend ----------
# Source: Intel 2025 10-K, MD&A Consolidated Results
years = [2021, 2022, 2023, 2024, 2025]
# 2021: $79.0B, 2022: $63.1B, 2023: $54.2B, 2024: $53.1B, 2025: $52.9B
# Source 2021/2022 from prior 10-K filings (well-known public data); confirm via
# 2025 10-K presents 2023/2024/2025 directly. 2022/2021 from prior 10-K filings.
revenue = [79.0, 63.1, 54.228, 53.101, 52.853]
# GAAP gross margin %
# 2021: 55.4, 2022: 42.6, 2023: 40.0, 2024: 32.7, 2025: 34.8
gm = [55.4, 42.6, 40.0, 32.7, 34.8]

fig, ax1 = plt.subplots(figsize=(9, 5))
bar = ax1.bar(years, revenue, color="#1f77b4", alpha=0.85, label="Revenue ($B)")
ax1.set_ylabel("Revenue ($B)", color="#1f77b4")
ax1.set_xlabel("Fiscal year")
ax1.set_xticks(years)
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 90)
for b, v in zip(bar, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 1.5, f"${v:.1f}B", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#d62728", marker="o", linewidth=2.2, label="GAAP gross margin %")
ax2.set_ylabel("GAAP gross margin (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(20, 65)
for x, y in zip(years, gm):
    ax2.text(x, y + 1.2, f"{y:.1f}%", ha="center", color="#d62728", fontsize=9)

plt.title("Intel — Revenue & GAAP Gross Margin (FY2021–FY2025)")
plt.tight_layout()
plt.savefig(OUT / "intc_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 2: Segment revenue mix 2023-2025 ----------
# Intel Products (CCG / DCAI) and Intel Foundry external + All Other
# Source: 2025 10-K MD&A segment summary
segments = ["CCG", "DCAI", "Intel Foundry (incl. intersegment)", "All Other (Mobileye/Altera)"]
y2023 = [32.305, 15.980, 18.504, 5.463]
y2024 = [33.346, 16.125, 17.317, 3.601]
y2025 = [32.228, 16.919, 17.826, 3.563]

x = np.arange(3)
width = 0.18

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(x - 1.5*width, [y2023[0], y2024[0], y2025[0]], width, label="CCG", color="#1f77b4")
ax.bar(x - 0.5*width, [y2023[1], y2024[1], y2025[1]], width, label="DCAI", color="#2ca02c")
ax.bar(x + 0.5*width, [y2023[2], y2024[2], y2025[2]], width, label="Intel Foundry", color="#ff7f0e")
ax.bar(x + 1.5*width, [y2023[3], y2024[3], y2025[3]], width, label="All Other", color="#9467bd")

ax.set_ylabel("Segment revenue ($B, incl. intersegment)")
ax.set_xticks(x)
ax.set_xticklabels(["FY2023", "FY2024", "FY2025"])
ax.legend(loc="upper right")
ax.set_title("Intel — Segment Revenue (incl. intersegment), FY2023–FY2025")
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
plt.tight_layout()
plt.savefig(OUT / "intc_segment_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 3: Intel Foundry operating loss ----------
years_f = [2023, 2024, 2025]
foundry_rev = [18.504, 17.317, 17.826]
foundry_loss = [-7.083, -13.291, -10.318]

fig, ax1 = plt.subplots(figsize=(9, 5))
b1 = ax1.bar([y - 0.2 for y in years_f], foundry_rev, width=0.4, color="#1f77b4", label="Foundry revenue")
b2 = ax1.bar([y + 0.2 for y in years_f], foundry_loss, width=0.4, color="#d62728", label="Foundry operating loss")
for b, v in zip(b1, foundry_rev):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.3, f"${v:.1f}B", ha="center", fontsize=9)
for b, v in zip(b2, foundry_loss):
    ax1.text(b.get_x() + b.get_width()/2, v - 0.8, f"${v:.1f}B", ha="center", fontsize=9, color="#a50026")
ax1.axhline(0, color="black", linewidth=0.6)
ax1.set_ylabel("USD billions")
ax1.set_xticks(years_f)
ax1.set_title("Intel Foundry — Revenue vs. Operating Loss (FY2023–FY2025)")
ax1.legend(loc="lower left")
ax1.set_ylim(-16, 22)
plt.tight_layout()
plt.savefig(OUT / "intc_foundry_loss.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 4: Capex and FCF ----------
# Source: 2025 10-K cash flow statement
years_c = [2023, 2024, 2025]
# Additions to PP&E gross: 25.75, 23.94, 14.65
gross_capex = [25.750, 23.944, 14.646]
# Net capex (after govt incentives + SCIP): 23.228, 10.515, 11.204
net_capex = [23.228, 10.515, 11.204]
# Adjusted FCF: -11.853, -2.228, -1.612
adj_fcf = [-11.853, -2.228, -1.612]

fig, ax = plt.subplots(figsize=(9, 5))
x_c = np.arange(len(years_c))
w = 0.25
ax.bar(x_c - w, gross_capex, w, label="Gross capex (additions to PP&E)", color="#1f77b4")
ax.bar(x_c, net_capex, w, label="Net capex (after incentives & SCIP)", color="#2ca02c")
ax.bar(x_c + w, adj_fcf, w, label="Adjusted free cash flow", color="#d62728")
ax.axhline(0, color="black", linewidth=0.6)
ax.set_xticks(x_c)
ax.set_xticklabels([f"FY{y}" for y in years_c])
ax.set_ylabel("USD billions")
ax.set_title("Intel — Capex & Adjusted Free Cash Flow (FY2023–FY2025)")
ax.legend()
for i, v in enumerate(gross_capex):
    ax.text(i - w, v + 0.3, f"${v:.1f}B", ha="center", fontsize=8)
for i, v in enumerate(net_capex):
    ax.text(i, v + 0.3, f"${v:.1f}B", ha="center", fontsize=8)
for i, v in enumerate(adj_fcf):
    ax.text(i + w, v - 1.1, f"${v:.1f}B", ha="center", fontsize=8, color="#a50026")
plt.tight_layout()
plt.savefig(OUT / "intc_capex_fcf.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 5: Peer P/S valuation ----------
# Source: Yahoo Finance, accessed 2026-05-20
peers = ["INTC", "AMD", "AVGO", "NVDA"]
ps = [11.0, 19.3, 29.0, 25.0]
pe = [None, 149.1, 81.3, 45.5]  # INTC negative TTM
fwd_pe = [76.6, 34.3, 22.9, 19.2]

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(peers))
bars = ax.bar(x, ps, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
ax.set_xticks(x)
ax.set_xticklabels(peers)
ax.set_ylabel("TTM P/S ratio")
ax.set_title("Peer Valuation — TTM P/S (as of 2026-05-20)")
for b, v in zip(bars, ps):
    ax.text(b.get_x() + b.get_width()/2, v + 0.4, f"{v:.1f}x", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(OUT / "intc_peer_ps.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 6: GAAP gross margin compression — Intel vs. AMD vs. NVDA ----------
years_gm = [2021, 2022, 2023, 2024, 2025]
intc_gm = [55.4, 42.6, 40.0, 32.7, 34.8]      # Intel 10-Ks
amd_gm = [48.2, 44.9, 46.1, 49.3, 53.0]        # AMD 10-K (approx; FY25e from earnings)
nvda_gm = [64.9, 56.9, 72.7, 75.0, 75.0]       # NVIDIA fiscal years; approx

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(years_gm, intc_gm, marker="o", linewidth=2.5, label="Intel (GAAP)", color="#1f77b4")
ax.plot(years_gm, amd_gm, marker="s", linewidth=2.5, label="AMD (GAAP)", color="#ff7f0e")
ax.plot(years_gm, nvda_gm, marker="^", linewidth=2.5, label="NVIDIA (GAAP)", color="#2ca02c")
ax.set_xticks(years_gm)
ax.set_ylabel("GAAP gross margin (%)")
ax.set_xlabel("Fiscal year")
ax.set_title("Intel GAAP Gross Margin vs. AMD and NVIDIA (FY2021–FY2025)")
ax.legend()
ax.set_ylim(25, 85)
plt.tight_layout()
plt.savefig(OUT / "intc_gm_compression.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 7: Quarterly revenue trajectory ----------
# Source: Intel earnings releases (8-Ks), Q1 2024 to Q1 2026
quarters = ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25", "Q4-25", "Q1-26"]
q_rev = [12.72, 12.83, 13.28, 14.27, 12.67, 12.86, 13.65, 13.68, 13.58]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(quarters, q_rev, color="#1f77b4", alpha=0.85)
ax.set_ylabel("Quarterly revenue ($B)")
ax.set_title("Intel — Quarterly Revenue, Q1-24 to Q1-26")
ax.set_ylim(10, 15.5)
for b, v in zip(bars, q_rev):
    ax.text(b.get_x() + b.get_width()/2, v + 0.1, f"${v:.2f}B", ha="center", fontsize=8)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "intc_quarterly_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 8: Cash, debt, and equity dilution ----------
# Source: 2025 10-K balance sheet & equity issuance footnotes
years_b = [2023, 2024, 2025]
cash = [25.0, 22.062, 37.416]
debt = [49.266, 50.011, 46.585]
shares = [4222, 4330, 4994]  # outstanding shares (millions)

fig, ax1 = plt.subplots(figsize=(9, 5))
w = 0.35
x = np.arange(len(years_b))
ax1.bar(x - w/2, cash, w, color="#2ca02c", label="Cash + ST investments")
ax1.bar(x + w/2, debt, w, color="#d62728", label="Total debt")
ax1.set_xticks(x)
ax1.set_xticklabels([f"FY{y}" for y in years_b])
ax1.set_ylabel("USD billions")
ax1.legend(loc="upper left")
for i, v in enumerate(cash):
    ax1.text(i - w/2, v + 0.5, f"${v:.1f}B", ha="center", fontsize=9)
for i, v in enumerate(debt):
    ax1.text(i + w/2, v + 0.5, f"${v:.1f}B", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(x, shares, color="black", marker="D", linewidth=2, label="Shares outstanding (M)")
ax2.set_ylabel("Diluted shares outstanding (millions)")
ax2.set_ylim(3800, 5300)
for xi, v in zip(x, shares):
    ax2.text(xi, v + 50, f"{v:,}", ha="center", fontsize=8)
ax2.legend(loc="upper right")
plt.title("Intel — Cash, Debt and Share Count (FY2023–FY2025)")
plt.tight_layout()
plt.savefig(OUT / "intc_balance_sheet.png", dpi=150, bbox_inches="tight")
plt.close()

print("Saved all charts to", OUT)
