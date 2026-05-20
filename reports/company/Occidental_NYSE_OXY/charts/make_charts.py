#!/usr/bin/env python3
"""Charts for OXY company-research report."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight", "font.size": 10})

# 1) Segment net sales (continuing operations basis) — Oil&Gas vs Midstream — 2023-2025
years = ["2023", "2024", "2025"]
oilgas = [21284, 21705, 20902]  # USD millions, 10-K 2025
midstream = [2433, 886, 1279]
elim = [-561, -572, -588]
total = [a + b + c for a, b, c in zip(oilgas, midstream, elim)]
x = np.arange(len(years))
w = 0.35
fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(x - w/2, oilgas, w, label="Oil & Gas", color="#1f4e79")
ax1.bar(x + w/2, midstream, w, label="Midstream & Marketing", color="#9DC3E6")
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel("Segment net sales (USD millions)")
ax1.set_title("OXY Segment Net Sales — Continuing Operations\n(OxyChem reclassified as discontinued)")
ax1.legend(loc="upper right")
for i, v in enumerate(total):
    ax1.text(i, max(oilgas) * 1.02, f"Total ${v/1000:.1f}B", ha="center", fontsize=8, color="#444")
plt.tight_layout()
plt.savefig(OUT / "oxy_segment_sales.png")
plt.close()

# 2) Production by region — Mboe/d — 2023-2025
prod_perm = [584, 664, 786]
prod_rockies = [271, 310, 284]
prod_gom = [145, 125, 132]
prod_intl = [223, 228, 232]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(years, prod_perm, label="Permian", color="#1f4e79")
ax.bar(years, prod_rockies, bottom=prod_perm, label="Rockies & Other Domestic", color="#2E75B6")
bottom2 = [p + r for p, r in zip(prod_perm, prod_rockies)]
ax.bar(years, prod_gom, bottom=bottom2, label="Gulf of America", color="#9DC3E6")
bottom3 = [b + g for b, g in zip(bottom2, prod_gom)]
ax.bar(years, prod_intl, bottom=bottom3, label="International (Oman, Algeria, UAE, Qatar)", color="#BDD7EE")
totals = [sum(t) for t in zip(prod_perm, prod_rockies, prod_gom, prod_intl)]
for i, v in enumerate(totals):
    ax.text(i, v + 20, f"{v} Mboe/d", ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("Production (Mboe/d)")
ax.set_title("OXY Average Daily Production by Region\n(CrownRock closed Aug-2024 — full-year benefit in 2025)")
ax.legend(loc="upper left", fontsize=8)
ax.set_ylim(0, 1700)
plt.tight_layout()
plt.savefig(OUT / "oxy_production_region.png")
plt.close()

# 3) Principal debt trend — quarterly post-CrownRock close
labels = ["Pre-Crown\nQ2'24", "Crown close\nQ3'24", "YE-2024", "YE-2025", "Post-OxyChem\nQ1'26", "May-5 2026\n(disclosed)"]
debt = [18.5, 27.2, 25.3, 20.4, 13.8, 13.3]  # USD billions
target = 14.3
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(labels, debt, marker="o", linewidth=2.2, color="#1f4e79")
for i, v in enumerate(debt):
    ax.text(i, v + 0.6, f"${v:.1f}B", ha="center", fontsize=9, fontweight="bold")
ax.axhline(target, color="#C00000", linestyle="--", label=f"Mgmt target ${target}B principal")
ax.axhline(10.0, color="#7030A0", linestyle=":", label="$10B milestone (next phase)")
ax.set_ylabel("Principal debt (USD billions)")
ax.set_title("OXY Principal Debt — Pre-CrownRock through Post-OxyChem Sale")
ax.set_ylim(0, 32)
ax.legend(loc="upper right", fontsize=8)
plt.xticks(rotation=10)
plt.tight_layout()
plt.savefig(OUT / "oxy_debt_trend.png")
plt.close()

# 4) Peer P/E and EV/EBITDA bars
peers = ["OXY", "XOM", "CVX", "EOG", "FANG"]
pe_ttm = [13.3, 22.0, 28.4, 13.5, 11.9]   # ranges aggregated from public quote sources
ev_ebitda = [7.0, 7.5, 7.8, 6.3, 6.1]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
colors = ["#C00000", "#1f4e79", "#1f4e79", "#1f4e79", "#1f4e79"]
axes[0].bar(peers, pe_ttm, color=colors)
for i, v in enumerate(pe_ttm):
    axes[0].text(i, v + 0.5, f"{v}×", ha="center", fontsize=9)
axes[0].set_title("TTM P/E (May 2026)")
axes[0].set_ylabel("Times")
axes[1].bar(peers, ev_ebitda, color=colors)
for i, v in enumerate(ev_ebitda):
    axes[1].text(i, v + 0.1, f"{v}×", ha="center", fontsize=9)
axes[1].set_title("EV / EBITDA (TTM)")
axes[1].set_ylabel("Times")
fig.suptitle("OXY vs. Integrated & Independent E&P Peers — Valuation", fontsize=11)
plt.tight_layout()
plt.savefig(OUT / "oxy_peer_valuation.png")
plt.close()

# 5) Operating income by segment (pre-tax)
seg_oilgas = [6240, 5214, 4586]
seg_mid = [-35, 563, 252]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(x - w/2, seg_oilgas, w, label="Oil & Gas segment earnings", color="#1f4e79")
ax.bar(x + w/2, seg_mid, w, label="Midstream & Marketing segment earnings", color="#9DC3E6")
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel("Pre-tax segment earnings (USD millions)")
ax.set_title("OXY Pre-tax Segment Earnings — Continuing Operations")
ax.axhline(0, color="black", linewidth=0.6)
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "oxy_segment_earnings.png")
plt.close()

print("Charts written to", OUT)
for p in OUT.glob("*.png"):
    print(" -", p.name)
