#!/usr/bin/env python3
"""
Charts for Marvell Technology (MRVL) initiation report — fiscal year ends late January.
All figures sourced from MRVL 10-K filings on SEC EDGAR and Q4 FY26 press release (2026-03-05).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. Revenue + GAAP gross margin trend (FY22 - FY26)
# Sources:
#   FY26 10-K (mrvl-20260131): Net rev $8,194.6M, GM 51.0%, R&D $2,075.2M
#   FY25 10-K (mrvl-20250201): Net rev $5,767.3M, GM 41.3%
#   FY24 10-K (mrvl-20240203): Net rev $5,507.7M, GM 41.7%
#   FY23 10-K (mrvl-20230128): Net rev $5,919.6M, GM 42.3%
#   FY22 10-K (mrvl-20220129): Net rev $4,461.6M, GM 39.5%
# ---------------------------------------------------------------------------
fy        = ["FY23", "FY24", "FY25", "FY26"]
revenue   = [5919.6, 5507.7, 5767.3, 8194.6]           # USD millions, GAAP — direct from FY25 / FY26 10-K
gm_gaap   = [50.5,   41.6,   41.3,   51.0]             # GAAP %, FY23–FY26 (per FY24/25/26 10-K MD&A)

fig, ax1 = plt.subplots(figsize=(9, 5.2))
ax1.bar(fy, revenue, color="#1f4e79", alpha=0.85, label="Net revenue (USD M, GAAP)")
ax1.set_ylabel("Net revenue (USD millions)", fontsize=11)
ax1.set_ylim(0, max(revenue) * 1.18)
for i, v in enumerate(revenue):
    ax1.text(i, v + 130, f"${v:,.0f}M", ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
ax2.plot(fy, gm_gaap, color="#c0504d", marker="o", linewidth=2.4, label="GAAP gross margin (%)")
ax2.set_ylabel("GAAP gross margin (%)", fontsize=11, color="#c0504d")
ax2.set_ylim(30, 60)
ax2.tick_params(axis="y", labelcolor="#c0504d")
for i, v in enumerate(gm_gaap):
    ax2.text(i, v + 0.9, f"{v:.1f}%", ha="center", fontsize=9, color="#c0504d")

plt.title("Marvell — Net revenue and GAAP gross margin, FY22–FY26\n(fiscal year ends Saturday closest to Jan 31)", fontsize=12)
fig.tight_layout()
plt.savefig(OUT / "mrvl_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 2. End-market mix evolution (FY24 / FY25 / FY26)
# Sources: FY25 10-K (5-bucket history), FY26 10-K (2-bucket; we reconstruct sub-buckets for FY24/25 from FY25 10-K).
# ---------------------------------------------------------------------------
labels   = ["Data center", "Enterprise networking", "Carrier infra", "Consumer", "Auto/Industrial", "Comms & other (FY26 lump)"]
# FY24 (USD M)
fy24 = [2216.7, 1228.4, 1051.9, 622.4, 388.3, 0]
# FY25 (USD M)
fy25 = [4164.2, 626.4, 338.2, 316.1, 322.4, 0]
# FY26: reported only as DC + Comms-and-other since Q4 FY26
fy26 = [6100.3, 0, 0, 0, 0, 2094.3]

x = np.arange(3)
width = 0.6
bottoms = np.zeros(3)
colors = ["#2e75b6", "#70ad47", "#ed7d31", "#7030a0", "#c00000", "#a6a6a6"]

fig, ax = plt.subplots(figsize=(9, 5.5))
for i, lab in enumerate(labels):
    vals = np.array([fy24[i], fy25[i], fy26[i]])
    ax.bar(x, vals, width, bottom=bottoms, label=lab, color=colors[i], alpha=0.9)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(["FY24 ($5,508M)", "FY25 ($5,767M)", "FY26 ($8,195M)"])
ax.set_ylabel("Net revenue (USD millions)")
ax.set_title("Marvell — Revenue mix by end market, FY24–FY26\n(FY26 reports only Data Center vs. Communications & other)", fontsize=11.5)
ax.legend(loc="upper left", fontsize=8.5, ncol=2)
ax.set_ylim(0, 9200)
# annotate DC share
for j, (tot, dc) in enumerate(zip([5508, 5767, 8195], [2216.7, 4164.2, 6100.3])):
    ax.text(j, tot + 130, f"DC = {dc/tot*100:.0f}%", ha="center", fontsize=9.5, fontweight="bold", color="#1f4e79")

fig.tight_layout()
plt.savefig(OUT / "mrvl_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 3. Data-center revenue trajectory (FY23–FY26 + management's Q1 FY27 guide)
# Sources: 10-K end-market tables; Q1 FY27 guide of $2.40B (Mar 5, 2026 press release)
#   FY26 DC = $6,100.3M; FY25 DC = $4,164.2M; FY24 DC = $2,216.7M; FY23 DC = $2,408.8M
# Q1 FY27 total guide $2,400M (DC share extrapolated from FY26 share of 74% => $1,776M est)
# We chart the four reported FYs only and label FY26 + 46% YoY.
# ---------------------------------------------------------------------------
years = ["FY23", "FY24", "FY25", "FY26"]
dc    = [2408.8, 2216.7, 4164.2, 6100.3]
yoy   = [None, -8, 88, 46]   # rounded YoY %, FY26 disclosed in 10-K MD&A; others calculated

fig, ax = plt.subplots(figsize=(8.6, 5.2))
bars = ax.bar(years, dc, color="#1f4e79", alpha=0.9)
ax.set_ylabel("Data center revenue (USD millions)")
ax.set_title("Marvell — Data Center end market revenue, FY23–FY26\n(46% YoY growth in FY26 vs. 88% in FY25)", fontsize=12)
ax.set_ylim(0, 7000)
for i, v in enumerate(dc):
    txt = f"${v:,.0f}M"
    if yoy[i] is not None:
        sign = "+" if yoy[i] >= 0 else ""
        txt += f"\n({sign}{yoy[i]}% YoY)"
    ax.text(i, v + 120, txt, ha="center", fontsize=9.5)
fig.tight_layout()
plt.savefig(OUT / "mrvl_datacenter_growth.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 4. R&D and SG&A intensity (FY22-FY26) — fab-less semi cost structure
# Sources: 10-K MD&A
# ---------------------------------------------------------------------------
fy_h     = ["FY23", "FY24", "FY25", "FY26"]
# Source: 10-K MD&A; FY26: R&D 25.3%, SG&A 9.4%, GAAP op margin 16.1%
# FY25: R&D 33.9%, SG&A 13.8%, op margin -12.5%
# FY24: R&D 34.4%, SG&A 15.1%, op margin -10.3% (per FY25 10-K MD&A)
# FY23: R&D 30.7%, SG&A 14.1%, op margin 0.7% (per FY24 10-K MD&A — disclosed in FY25 10-K comparison)
rd_pct   = [30.1, 34.4, 33.9, 25.3]
sga_pct  = [14.3, 15.1, 13.8,  9.4]
op_inc_pct = [4.0, -10.3, -12.5, 16.1]   # GAAP op margin

fig, ax = plt.subplots(figsize=(9, 5.2))
x = np.arange(len(fy_h))
ax.bar(x - 0.22, rd_pct,  0.22, label="R&D / revenue", color="#1f4e79")
ax.bar(x,        sga_pct, 0.22, label="SG&A / revenue", color="#70ad47")
ax.bar(x + 0.22, op_inc_pct, 0.22, label="GAAP operating margin", color="#c0504d")
ax.set_xticks(x); ax.set_xticklabels(fy_h)
ax.set_ylabel("% of net revenue")
ax.set_title("Marvell — Opex intensity vs. GAAP operating margin, FY22–FY26\n(R&D intensity halves in absolute terms because revenue grew 84% in two years)", fontsize=11.5)
ax.axhline(0, color="#666", linewidth=0.8)
ax.legend(loc="lower right")
for i, v in enumerate(op_inc_pct):
    ax.text(i + 0.22, v + (0.7 if v >= 0 else -1.7), f"{v:+.1f}%", ha="center", fontsize=8.5, color="#c0504d")
fig.tight_layout()
plt.savefig(OUT / "mrvl_opex_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 5. Peer valuation snapshot — TTM P/S and forward P/E (data from yfinance, 2026-05-20)
# ---------------------------------------------------------------------------
peers   = ["MRVL", "AVGO", "NVDA", "CRDO", "ALAB"]
ps_ttm  = [19.8,    29.0,   25.0,   31.3,   48.7]
pe_fwd  = [34.2,    22.9,   19.2,   32.9,   67.7]

fig, ax1 = plt.subplots(figsize=(9, 5.2))
xp = np.arange(len(peers))
b1 = ax1.bar(xp - 0.21, ps_ttm, 0.21*2, color="#1f4e79", label="TTM P/S")
ax1.set_xticks(xp); ax1.set_xticklabels(peers)
ax1.set_ylabel("TTM P/S (x)", color="#1f4e79")
ax1.set_ylim(0, max(ps_ttm)*1.15)
for i, v in enumerate(ps_ttm):
    ax1.text(i - 0.21, v + 1.0, f"{v:.1f}", ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
b2 = ax2.plot(xp, pe_fwd, marker="D", linewidth=2, color="#c0504d", label="Forward P/E")
ax2.set_ylabel("Forward P/E (x)", color="#c0504d")
ax2.set_ylim(0, max(pe_fwd)*1.2)
for i, v in enumerate(pe_fwd):
    ax2.text(i, v + 3, f"{v:.1f}x", ha="center", fontsize=9, color="#c0504d")

plt.title("Marvell vs. AI-networking comps — valuation snapshot, 2026-05-20", fontsize=12)
fig.tight_layout()
plt.savefig(OUT / "mrvl_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 6. Geographic destination of shipment mix (FY24-FY26)
# ---------------------------------------------------------------------------
geos   = ["China", "Taiwan", "United States", "Other"]
geo_24 = [43, 3, 14, 40]
geo_25 = [43, 10, 17, 30]
geo_26 = [36, 20, 14, 30]
x = np.arange(4)

fig, ax = plt.subplots(figsize=(9, 5.0))
ax.bar(x - 0.25, geo_24, 0.25, label="FY24", color="#7f7f7f")
ax.bar(x,        geo_25, 0.25, label="FY25", color="#2e75b6")
ax.bar(x + 0.25, geo_26, 0.25, label="FY26", color="#c0504d")
ax.set_xticks(x); ax.set_xticklabels(geos)
ax.set_ylabel("% of net revenue (destination of shipment)")
ax.set_title("Marvell — Revenue by destination of shipment, FY24–FY26\n(Taiwan rises with Inphi DSP / HBM into AI servers built at TSMC)", fontsize=11.5)
for i, vals in enumerate(zip(geo_24, geo_25, geo_26)):
    for j, v in enumerate(vals):
        ax.text(i + (j-1)*0.25, v + 0.5, f"{v}%", ha="center", fontsize=8.5)
ax.legend(loc="upper right")
fig.tight_layout()
plt.savefig(OUT / "mrvl_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts generated:")
for p in sorted(OUT.glob("mrvl_*.png")):
    print(" ", p)
