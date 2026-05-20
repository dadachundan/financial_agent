#!/usr/bin/env python3
"""Charts for Coherent Corp (NYSE:COHR) initiation report."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ---------------- Chart 1: revenue + GAAP gross margin trend ----------------
# Sources:
#  FY23/FY24/FY25 revenue & GAAP gross margin from 10-K filed 2025-08-15
#  9M FY26 (Jul 2025 – Mar 2026) revenue $5,072.6M, GAAP GM 37.1% from Q3 FY26 release (2026-05-06)
#  FY26E built from 9M + midpoint of Q4 guidance ($1.91-2.05B → $1.98B)
years = ["FY23", "FY24", "FY25", "FY26E"]
revenue = [5160, 4708, 5810, 5073 + 1980]   # FY26E = 9M actual + Q4 midpoint
gm = [31.4, 30.9, 35.2, 37.5]               # GAAP gross margin %, FY26E from 9M GAAP 37.1% + Q4 guide non-GAAP 40%

fig, ax1 = plt.subplots(figsize=(9.5, 4.8))
bars = ax1.bar(years, revenue, color="#1f4e79", alpha=0.85, width=0.55, label="Revenue ($M)")
ax1.set_ylabel("Revenue (USD $M)", color="#1f4e79", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, max(revenue) * 1.18)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 100, f"${v:,.0f}M", ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#c0392b", marker="o", linewidth=2.4, label="GAAP gross margin %")
ax2.set_ylabel("GAAP gross margin (%)", color="#c0392b", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c0392b")
ax2.set_ylim(25, 42)
for i, v in enumerate(gm):
    ax2.text(i, v + 0.4, f"{v:.1f}%", ha="center", fontsize=9, color="#c0392b")

plt.title("Coherent Corp — revenue and GAAP gross margin (FY23-FY26E, fiscal year ends June 30)", fontsize=11.5)
fig.tight_layout()
plt.savefig(OUT / "cohr_revenue_gm.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------- Chart 2: segment revenue mix (FY23-FY25 + 9M FY26) ---------
# Old segments (FY23-FY25) reported in 2025 10-K; new segments (Datacenter & Communications / Industrial)
# disclosed in Q3 FY26 10-Q. To keep one axis comparable we show FY23, FY24, FY25 in old buckets and
# annotate the 9M FY26 with the new segment structure.
fig, ax = plt.subplots(figsize=(9.5, 5))
labels_old = ["FY23", "FY24", "FY25"]
networking = [2341, 2296, 3421]
materials = [1350, 1017, 954]
lasers = [1469, 1395, 1435]
b1 = ax.bar(labels_old, networking, label="Networking", color="#1f4e79")
b2 = ax.bar(labels_old, materials, bottom=networking, label="Materials", color="#e67e22")
b3 = ax.bar(labels_old, lasers, bottom=[n + m for n, m in zip(networking, materials)], label="Lasers", color="#27ae60")
# 9M FY26 (Datacenter & Communications + Industrial)
labels_new = ["9M FY26"]
dc = [3660]
ind = [1413]
ax.bar(labels_new, dc, color="#2c3e50", label="Datacenter & Communications (new)")
ax.bar(labels_new, ind, bottom=dc, color="#8e6f3e", label="Industrial (new)")

for i, total in enumerate([n + m + l for n, m, l in zip(networking, materials, lasers)]):
    ax.text(i, total + 90, f"${total:,.0f}M", ha="center", fontsize=9)
ax.text(3, sum([dc[0], ind[0]]) + 90, f"${dc[0] + ind[0]:,.0f}M", ha="center", fontsize=9)

ax.set_ylabel("Segment revenue (USD $M)")
ax.set_title("Coherent — segment revenue mix (FY23-FY25 old segments; 9M FY26 new two-segment structure)")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
plt.savefig(OUT / "cohr_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------- Chart 3: Datacenter & Communications quarterly ramp ---------
# Source: Q3 FY26 press release (Table 5) and prior 8-K segment tables.
# Datacom & Comms quarterly (USD $M): Q3 FY25 968.7, recent quarters per Q3 FY26 release.
# To assemble pre-Q3 FY25 quarterly history under the new market view, we use the disclosure in
# the Q3 FY26 release which gives Q3 FY26, Q2 FY26 (Dec-25), Q3 FY25 (Mar-25). We supplement
# with Q1 FY26 derived as 9M FY26 ($3,659.6M) minus Q2 FY26 ($1,208.0M) minus Q3 FY26 ($1,361.6M)
# = $1,090.0M.
q_labels = ["Q3\nFY25", "Q1\nFY26", "Q2\nFY26", "Q3\nFY26"]
q_dc = [968.7, 1090.0, 1208.0, 1361.6]
q_ind = [529.2, 491.0, 477.6, 444.0]   # 9M FY26 industrial $1,413M minus Q2 477.6 and Q3 444 -> Q1 491.4
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(q_labels, q_dc, color="#1f4e79", label="Datacenter & Communications")
ax.bar(q_labels, q_ind, bottom=q_dc, color="#8e6f3e", label="Industrial")
for i, (d, ii) in enumerate(zip(q_dc, q_ind)):
    ax.text(i, d / 2, f"${d:,.0f}", ha="center", color="white", fontsize=9)
    ax.text(i, d + ii / 2, f"${ii:,.0f}", ha="center", color="white", fontsize=9)
    ax.text(i, d + ii + 25, f"${d + ii:,.0f}", ha="center", fontsize=9)
ax.set_ylabel("Revenue (USD $M)")
ax.set_title("Coherent — quarterly revenue by new segment (note Q1 FY26 industrial derived from disclosed 9M total)")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
plt.savefig(OUT / "cohr_quarterly_segment.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------- Chart 4: peer valuation comparison ----------------
# TTM multiples from Yahoo Finance, pulled 2026-05-20.
peers = ["COHR", "LITE", "FN", "MKSI", "IPGP"]
ttm_pe = [168.8, 151.8, 57.0, 64.4, 177.4]
ttm_ps = [10.5, 27.0, 5.6, 5.1, 4.9]
fwd_pe = [43.6, 47.8, 38.5, 20.9, 52.2]

x = np.arange(len(peers))
width = 0.27
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.bar(x - width, ttm_pe, width, label="TTM P/E", color="#1f4e79")
ax.bar(x, fwd_pe, width, label="Forward P/E", color="#5dade2")
ax.bar(x + width, ttm_ps, width, label="TTM P/S", color="#e67e22")
for i, (a, b, c) in enumerate(zip(ttm_pe, fwd_pe, ttm_ps)):
    ax.text(i - width, a + 4, f"{a:.0f}x", ha="center", fontsize=8.5)
    ax.text(i, b + 4, f"{b:.0f}x", ha="center", fontsize=8.5)
    ax.text(i + width, c + 4, f"{c:.1f}x", ha="center", fontsize=8.5)
ax.set_xticks(x)
ax.set_xticklabels(peers)
ax.set_ylabel("Multiple (x)")
ax.set_title("Photonics / optical peers — valuation snapshot (Yahoo Finance, 2026-05-20)")
ax.legend()
fig.tight_layout()
plt.savefig(OUT / "cohr_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------- Chart 5: debt / leverage trajectory ----------------
# Total debt at quarter-ends (USD $M) and net leverage via balance sheets in 10-K + 10-Qs.
# FY22-end (post-merger) ~5,330; FY23-end 4,432; FY24-end 4,100; FY25-end 3,687; Q3 FY26 3,194.
# Sources: 10-K FY25 Note 7; Q3 FY26 10-Q Note 8.
labels = ["FY22\n(post-merger)", "FY23", "FY24", "FY25", "Q3 FY26\n(Mar-26)"]
debt = [5330, 4432, 4100, 3687, 3194]
cash = [847, 928, 927, 909, 1593]      # cash & equivalents
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.bar(labels, debt, color="#c0392b", label="Total debt")
ax.bar(labels, cash, color="#27ae60", label="Cash & equivalents")
for i, (d, c) in enumerate(zip(debt, cash)):
    ax.text(i, d + 90, f"${d:,.0f}", ha="center", fontsize=9, color="#c0392b")
    ax.text(i, c + 90, f"${c:,.0f}", ha="center", fontsize=9, color="#27ae60")
ax.set_ylabel("USD $M")
ax.set_title("Coherent — total debt and cash trajectory (post-II-VI / Coherent merger)")
ax.legend(loc="upper right")
fig.tight_layout()
plt.savefig(OUT / "cohr_debt_trajectory.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------- Chart 6: capex intensity ----------------
# capex from 10-K consolidated cash flow + 9M FY26 Q3 release ($547.2M YTD)
labels = ["FY23", "FY24", "FY25", "9M FY26"]
capex = [436, 347, 441, 547]
revenue_p = [5160, 4708, 5810, 5073]
intensity = [c / r * 100 for c, r in zip(capex, revenue_p)]
fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.bar(labels, capex, color="#1f4e79", label="Capex (PP&E additions)")
ax1.set_ylabel("Capex (USD $M)", color="#1f4e79")
ax2 = ax1.twinx()
ax2.plot(labels, intensity, color="#c0392b", marker="o", linewidth=2.4)
ax2.set_ylabel("Capex / revenue (%)", color="#c0392b")
ax2.set_ylim(0, 14)
for i, (c, r) in enumerate(zip(capex, intensity)):
    ax1.text(i, c + 12, f"${c:,.0f}M", ha="center", fontsize=9, color="#1f4e79")
    ax2.text(i, r + 0.3, f"{r:.1f}%", ha="center", fontsize=9, color="#c0392b")
ax1.set_title("Coherent — capex and capex intensity (9M FY26 reflects accelerated InP / VCSEL / SiC capacity build)")
fig.tight_layout()
plt.savefig(OUT / "cohr_capex.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written to", OUT)
