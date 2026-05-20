"""Charts for Astera Labs (NASDAQ: ALAB) initiation report.

All data sourced from ALAB 10-K (FY2025), 10-Q (Q1 FY2026), Q1 FY2026
earnings release (8-K filed 2026-05-05), and yfinance market snapshots
pulled on 2026-05-20.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})

# --------------------------------------------------------------------------- #
# 1. Quarterly revenue + sequential growth (since IPO)                         #
# --------------------------------------------------------------------------- #
# 10-Q Q1 FY2026 + 10-K FY2025 + 10-Q FY2024 disclosures.
qtrs = [
    "Q1'24", "Q2'24", "Q3'24", "Q4'24",
    "Q1'25", "Q2'25", "Q3'25", "Q4'25",
    "Q1'26",
]
# Q1'24 = 65.3, Q2'24 = 76.9, Q3'24 = 113.1, Q4'24 = 141.1, Q1'25 = 159.4,
# Q2'25 = 191.9, Q3'25 = 230.6, Q4'25 = 270.6, Q1'26 = 308.4 ($ millions).
rev = [65.3, 76.9, 113.1, 141.1, 159.4, 191.9, 230.6, 270.6, 308.4]
qoq = [None] + [(rev[i] - rev[i - 1]) / rev[i - 1] * 100 for i in range(1, len(rev))]

fig, ax1 = plt.subplots(figsize=(10, 5))
bars = ax1.bar(qtrs, rev, color="#1f77b4", alpha=0.85, label="Revenue ($M)")
ax1.set_ylabel("Revenue (US$ millions)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 350)
for b, v in zip(bars, rev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 5, f"{v:.0f}",
             ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(qtrs, qoq, color="#d62728", marker="o", linewidth=2,
         label="QoQ growth (%)")
ax2.set_ylabel("Sequential growth (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(-10, 70)
ax2.grid(False)

plt.title("Astera Labs — Quarterly revenue since IPO (Mar 2024)", fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "alab_quarterly_revenue.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------- #
# 2. Annual revenue, gross margin and operating margin                         #
# --------------------------------------------------------------------------- #
years = ["FY2022", "FY2023", "FY2024", "FY2025"]
# FY2022 revenue $79.9M (S-1), FY2023 $115.8M, FY2024 $396.3M, FY2025 $852.5M.
annual_rev = [79.9, 115.8, 396.3, 852.5]
# Gross margin (GAAP).  FY2023 67.8% (S-1: cost $37.3M / rev $115.8M),
# FY2024 76.4%, FY2025 75.7%.  FY2022 estimated near 58% per S-1 disclosures.
gm = [58.0, 68.9, 76.4, 75.7]
# Operating margin GAAP.  FY2023 -25.5% (-29.5/115.8), FY2024 -29.3%
# (-116.1/396.3), FY2025 +20.3% (173.4/852.5).  FY2022 estimated.
op_margin = [-70.0, -25.5, -29.3, 20.3]

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(years, annual_rev, color="#1f77b4", alpha=0.85, label="Revenue ($M)")
for i, v in enumerate(annual_rev):
    ax1.text(i, v + 20, f"${v:.0f}M", ha="center", fontsize=10)
ax1.set_ylabel("Revenue (US$ millions)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 1000)

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#2ca02c", marker="s", linewidth=2,
         label="GAAP gross margin (%)")
ax2.plot(years, op_margin, color="#d62728", marker="o", linewidth=2,
         label="GAAP operating margin (%)")
for i, (g, o) in enumerate(zip(gm, op_margin)):
    ax2.text(i, g + 2, f"{g:.1f}%", ha="center", color="#2ca02c", fontsize=9)
    ax2.text(i, o - 8, f"{o:.1f}%", ha="center", color="#d62728", fontsize=9)
ax2.set_ylabel("Margin (%)")
ax2.set_ylim(-90, 90)
ax2.axhline(0, color="black", linewidth=0.5)
ax2.legend(loc="lower right")
ax2.grid(False)

plt.title("Astera Labs — Annual revenue and margin trajectory", fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "alab_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------- #
# 3. Geographic revenue mix (FY2025 vs FY2024, by ship-to billing address)     #
# --------------------------------------------------------------------------- #
labels = ["Singapore", "China", "Taiwan", "United States", "Other"]
fy25 = [276.989, 256.276, 247.448, 27.428, 44.384]
fy24 = [29.056, 72.672, 269.935, 11.296, 13.331]
x = np.arange(len(labels))
width = 0.38
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width / 2, fy24, width, label="FY2024", color="#9ecae1")
ax.bar(x + width / 2, fy25, width, label="FY2025", color="#1f77b4")
for i, (a, b) in enumerate(zip(fy24, fy25)):
    ax.text(i - width / 2, a + 5, f"${a:.0f}M", ha="center", fontsize=8)
    ax.text(i + width / 2, b + 5, f"${b:.0f}M", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Revenue (US$ millions)")
ax.set_title("Astera Labs — Revenue by billing geography (FY2024 vs FY2025)")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "alab_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------- #
# 4. Customer concentration (10% customers)                                    #
# --------------------------------------------------------------------------- #
# FY2025 10-K disclosed concentrations: A=20, B=20, C=17, D=16, E=11; all
# others = 16% residual (sums to 100).  FY2024 D=24, F=36, B=11; others sum
# to 29.  We plot FY2025 only as a single stacked snapshot since labels are
# pseudonymous between years.
cust = ["Customer A", "Customer B", "Customer C", "Customer D", "Customer E",
        "All other"]
share = [20, 20, 17, 16, 11, 16]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#7f7f7f"]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(cust[::-1], share[::-1], color=colors[::-1])
for b, v in zip(bars, share[::-1]):
    ax.text(v + 0.4, b.get_y() + b.get_height() / 2, f"{v}%",
            va="center", fontsize=10)
ax.set_xlim(0, 28)
ax.set_xlabel("% of FY2025 revenue")
ax.set_title("Astera Labs — Customer concentration, FY2025\n"
             "(top 3 = 57% of revenue; top 5 = 84%; one end customer >70%)")
fig.tight_layout()
fig.savefig(OUT / "alab_customer_concentration.png", dpi=150,
            bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------- #
# 5. Peer valuation comparison (P/S and P/E, TTM)                              #
# --------------------------------------------------------------------------- #
peers = ["ALAB", "CRDO", "MRVL", "AVGO", "NVDA"]
ps = [48.8, 31.3, 19.9, 29.0, 25.0]
pe = [191.3, 99.2, 60.6, 81.4, 45.5]
rev_growth = [93, 201, 22, 30, 73]  # most-recent reported YoY %

x = np.arange(len(peers))
width = 0.38
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax = axes[0]
ax.bar(x, ps, color="#1f77b4")
for i, v in enumerate(ps):
    ax.text(i, v + 1.2, f"{v:.1f}", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(peers)
ax.set_title("TTM Price / Sales")
ax.set_ylim(0, 60)

ax = axes[1]
ax.bar(x, pe, color="#d62728")
for i, v in enumerate(pe):
    ax.text(i, v + 4, f"{v:.0f}", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(peers)
ax.set_title("TTM Price / Earnings")
ax.set_ylim(0, 230)

plt.suptitle("ALAB vs. connectivity / AI-silicon peers (Yahoo Finance, 2026-05-20)",
             fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "alab_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------------------- #
# 6. Opex composition (FY2025) - R&D heavy                                     #
# --------------------------------------------------------------------------- #
labels = ["R&D", "S&M", "G&A"]
fy25_opex = [304.0, 79.8, 88.1]
fy24_opex = [200.8, 123.7, 94.3]
x = np.arange(len(labels))
width = 0.38
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width / 2, fy24_opex, width, label="FY2024", color="#9ecae1")
ax.bar(x + width / 2, fy25_opex, width, label="FY2025", color="#1f77b4")
for i, (a, b) in enumerate(zip(fy24_opex, fy25_opex)):
    ax.text(i - width / 2, a + 5, f"${a:.0f}M", ha="center", fontsize=9)
    ax.text(i + width / 2, b + 5, f"${b:.0f}M", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Operating expense (US$ millions)")
ax.set_title("Astera Labs — Operating expenses (R&D-heavy mix)")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "alab_opex_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("ALAB charts written to", OUT)
