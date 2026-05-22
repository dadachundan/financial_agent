"""Charts for Micron company-research report (NASDAQ:MU).
All figures sourced from Micron 10-K FY2025 (filed 2025-09-30) and Q1 FY2026 press release (2025-12-17).
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

# ----------------------------------------------------------------------------
# Chart 1: Revenue + GAAP Gross Margin (FY2021-FY2025, fiscal year ending Aug/Sep)
# Source: 10-K FY2025 Consolidated Results table; prior years from earlier 10-Ks.
# FY2021 = 27,705 (51%), FY2022 = 30,758 (45%), FY2023 = 15,540 (-9%),
# FY2024 = 25,111 (22%), FY2025 = 37,378 (40%).
# ----------------------------------------------------------------------------
years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
rev = [27.705, 30.758, 15.540, 25.111, 37.378]   # $ bn (FY21/22 from 2022 10-K; FY23-25 from 2025 10-K)
gm_pct = [38.0, 45.0, -9.0, 22.0, 40.0]           # GAAP % (FY21=38% from 2022 10-K; FY22=45%; FY23-25 from 2025 10-K)

fig, ax1 = plt.subplots(figsize=(8, 5))
bars = ax1.bar(years, rev, color="#005EB8", alpha=0.85, label="Revenue ($B)")
ax1.set_ylabel("Revenue ($B)", color="#005EB8")
ax1.tick_params(axis='y', labelcolor="#005EB8")
ax1.set_ylim(0, 45)
for b, v in zip(bars, rev):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.6, f"{v:.1f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm_pct, color="#E03C31", marker="o", linewidth=2.4, label="GAAP gross margin %")
ax2.set_ylabel("GAAP gross margin (%)", color="#E03C31")
ax2.tick_params(axis='y', labelcolor="#E03C31")
ax2.set_ylim(-20, 60)
ax2.axhline(0, color="grey", linewidth=0.5, linestyle="--")
for x, y in zip(years, gm_pct):
    ax2.text(x, y + 2.5, f"{y:.0f}%", color="#E03C31", ha="center", fontsize=9)

plt.title("Micron — revenue and GAAP gross margin (FY2021-FY2025)")
fig.tight_layout()
plt.savefig(OUT / "micron_revenue_gm.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 2: FY2025 revenue by business unit (after Q3-FY25 segment reorganization)
# Source: 10-K FY2025 Note 27 — Revenue by Business Unit.
# CMBU 13,524 (36%); CDBU 7,229 (19%); MCBU 11,859 (32%); AEBU 4,753 (13%);
# All other 13 (~0%).  Total $37,378M.
# ----------------------------------------------------------------------------
labels = ["CMBU\n(Cloud Memory)", "CDBU\n(Core DC)", "MCBU\n(Mobile/Client)", "AEBU\n(Auto/Embedded)"]
values = [13.524, 7.229, 11.859, 4.753]
colors = ["#005EB8", "#1F8FFF", "#F6A623", "#27AE60"]

fig, ax = plt.subplots(figsize=(7.5, 5))
wedges, texts, autotexts = ax.pie(
    values, labels=labels, colors=colors, autopct=lambda p: f"${p*sum(values)/100:.1f}B\n({p:.0f}%)",
    startangle=90, textprops={"fontsize": 9},
)
ax.set_title("Micron — FY2025 revenue by business unit ($37.4B total)")
plt.tight_layout()
plt.savefig(OUT / "micron_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 3: CMBU (Cloud Memory) revenue ramp — proxy for HBM + AI DRAM
# Source: 10-K FY2025 (CMBU $13.52B 2025, $3.79B 2024, $1.87B 2023). CMBU sales
# are HBM + DDR5/DDR4 + LPDDR5/GDDR6 to hyperscalers; HBM is the largest driver.
# ----------------------------------------------------------------------------
yrs = ["FY23", "FY24", "FY25"]
cmbu = [1.872, 3.792, 13.524]

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(yrs, cmbu, color="#0072CE")
for b, v in zip(bars, cmbu):
    ax.text(b.get_x() + b.get_width()/2, v + 0.3, f"${v:.2f}B", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("CMBU revenue ($B)")
ax.set_title("Micron CMBU revenue ramp — HBM + AI DRAM proxy")
ax.set_ylim(0, 16)
ax.annotate("+103% YoY", xy=(1, 3.79), xytext=(1, 6), ha="center",
            arrowprops=dict(arrowstyle="->", color="grey"), fontsize=9)
ax.annotate("+257% YoY", xy=(2, 13.52), xytext=(2, 15.5), ha="center",
            arrowprops=dict(arrowstyle="->", color="grey"), fontsize=9, color="#0072CE", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT / "micron_cmbu_ramp.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 4: DRAM vs NAND revenue (FY2023-FY2025) — Source: 10-K Note 21
# DRAM 10,978 / 17,603 / 28,578 ; NAND 4,206 / 7,227 / 8,503 ; Other 356/281/297
# ----------------------------------------------------------------------------
yrs = ["FY23", "FY24", "FY25"]
dram = [10.978, 17.603, 28.578]
nand = [4.206, 7.227, 8.503]
other = [0.356, 0.281, 0.297]

x = np.arange(len(yrs))
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.bar(x, dram, label="DRAM", color="#005EB8")
ax.bar(x, nand, bottom=dram, label="NAND", color="#F6A623")
ax.bar(x, other, bottom=[d+n for d, n in zip(dram, nand)], label="NOR/Other", color="#888888")
for i, (d, n) in enumerate(zip(dram, nand)):
    ax.text(i, d/2, f"${d:.1f}B", ha="center", color="white", fontweight="bold", fontsize=9)
    ax.text(i, d + n/2, f"${n:.1f}B", ha="center", color="black", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(yrs)
ax.set_ylabel("Revenue ($B)")
ax.set_title("Micron revenue mix — DRAM vs NAND vs NOR (FY2023-FY2025)")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(OUT / "micron_dram_nand_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 5: Capex (gross) and operating cash flow — capital intensity
# Source: 10-K FY2025 cash flow statement.
# Expenditures for PP&E: FY23 $7.676B, FY24 $8.386B, FY25 $15.857B.
# Operating cash flow: FY23 $1.559B, FY24 $8.507B, FY25 $17.525B.
# ----------------------------------------------------------------------------
yrs = ["FY23", "FY24", "FY25"]
capex = [7.676, 8.386, 15.857]
ocf = [1.559, 8.507, 17.525]

x = np.arange(len(yrs))
w = 0.38
fig, ax = plt.subplots(figsize=(7.5, 5))
b1 = ax.bar(x - w/2, capex, w, label="Capex (gross PP&E)", color="#E03C31")
b2 = ax.bar(x + w/2, ocf, w, label="Operating cash flow", color="#27AE60")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3, f"${b.get_height():.1f}B",
                ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(yrs)
ax.set_ylabel("$ billion")
ax.set_title("Micron — capex vs. operating cash flow (FY2023-FY2025)")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "micron_capex_ocf.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 6: Geographic revenue mix FY2025 (10-K Note 29)
# U.S. 24,113; Taiwan 5,672; Mainland China 2,639; Other APAC 1,913; Hong Kong 1,138;
# Japan 895; Europe 625; Other 383.
# ----------------------------------------------------------------------------
labels = ["U.S.", "Taiwan", "Mainland China", "Other APAC", "Hong Kong", "Japan", "Europe", "Other"]
vals = [24.113, 5.672, 2.639, 1.913, 1.138, 0.895, 0.625, 0.383]
cols = ["#005EB8", "#0072CE", "#E03C31", "#F6A623", "#FFD24A", "#27AE60", "#888888", "#BBBBBB"]

fig, ax = plt.subplots(figsize=(8, 4.5))
y = np.arange(len(labels))
bars = ax.barh(y, vals, color=cols)
ax.set_yticks(y); ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("FY2025 revenue ($B)")
ax.set_title("Micron — FY2025 revenue by ship-to country ($37.4B total)")
for b, v in zip(bars, vals):
    ax.text(v + 0.25, b.get_y() + b.get_height()/2, f"${v:.2f}B ({v/37.378*100:.0f}%)",
            va="center", fontsize=9)
ax.set_xlim(0, 30)
plt.tight_layout()
plt.savefig(OUT / "micron_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------------
# Chart 7: Peer valuation snapshot — P/E TTM, forward P/E, P/S TTM
# Source: Yahoo Finance pull, 2026-05-20 (cited inline in report).
# Note: SK Hynix / Samsung TTM P/E unavailable on Yahoo (Korean comps); forward
# P/E shown instead for those names.
# ----------------------------------------------------------------------------
names = ["Micron\n(MU)", "SK hynix\n(000660.KS)", "Samsung\n(005930.KS)", "Sandisk\n(SNDK)", "WDC", "Seagate\n(STX)"]
fwd_pe = [7.08, 4.56, 5.30, 7.98, 26.42, 28.79]
ps = [14.12, 9.38, 4.67, 15.72, 13.47, 15.35]

x = np.arange(len(names))
w = 0.38
fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - w/2, fwd_pe, w, label="Forward P/E", color="#005EB8")
b2 = ax.bar(x + w/2, ps, w, label="P/S (TTM)", color="#F6A623")
for bars, vals in ((b1, fwd_pe), (b2, ps)):
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.4, f"{v:.1f}", ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8)
ax.set_ylabel("Multiple (x)")
ax.set_title("Memory + storage peer valuations — Forward P/E and TTM P/S (2026-05-20)")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "micron_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written to", OUT)
