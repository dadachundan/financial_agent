"""Charts for Infineon Technologies (XETR:IFX) research report dated 2026-05-20.

Sources:
- FY2020-FY2024 revenue: Infineon "Financial Data 2020-2024" booklet
- FY2025 revenue / segment-result margin: Infineon FY2025 press release INFXX202511-021, 12 Nov 2025
- Segment mix FY2024 (used as latest fully-disclosed): ATV 56%, PSS 21%, GIP 13%, CSS 10%
- FY2025 segment result and AI revenue target: FY2025 press release INFXX202511-021
- Yahoo Finance / yfinance for IFX.DE and peer (STM, NXPI, ON, ADI, TXN, MCHP) TTM P/E and P/S, accessed 2026-05-20
"""

import os
import matplotlib.pyplot as plt
import numpy as np

OUT = "/Users/x/projects/financial_agent/reports/charts"
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Revenue and segment-result margin trend FY2020 - FY2026e
# ---------------------------------------------------------------------------
fy = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "FY26e"]
rev_eur_m = [8567, 11060, 14218, 16309, 14955, 14662, 17500]  # FY26e midpoint of raised €17.0-18.0 bn
sr_margin = [13.7, 21.1, 23.3, 27.0, 20.8, 17.5, 20.0]        # Segment Result Margin %; FY26e ~20% (raised)

fig, ax1 = plt.subplots(figsize=(10, 5.5))
bars = ax1.bar(fy, rev_eur_m, color="#3b6bbc", alpha=0.85, label="Revenue (€m)")
ax1.set_ylabel("Revenue (€m)", color="#3b6bbc", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#3b6bbc")
ax1.set_ylim(0, 19000)
for b, v in zip(bars, rev_eur_m):
    ax1.text(b.get_x() + b.get_width() / 2, v + 250, f"{v:,}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(fy, sr_margin, color="#d24c2e", marker="o", linewidth=2.2, label="Segment Result Margin (%)")
ax2.set_ylabel("Segment Result Margin (%)", color="#d24c2e", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#d24c2e")
ax2.set_ylim(0, 30)
for i, v in enumerate(sr_margin):
    ax2.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontsize=9, color="#d24c2e")

plt.title("Infineon Technologies — Revenue and Segment Result Margin (FY2020-FY2026e)", fontsize=12, pad=14)
ax1.set_xlabel("Fiscal Year (ended 30 Sep)")
fig.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 2. FY2025 revenue segment mix
# ---------------------------------------------------------------------------
labels = ["Automotive (ATV)", "Power & Sensor Systems (PSS)", "Green Industrial Power (GIP)", "Connected Secure Systems (CSS)"]
sizes = [56, 21, 13, 10]  # % of FY2024 revenue (last fully disclosed segment mix)
colors = ["#1f4e8c", "#3b8fd1", "#6cbf6c", "#d8a838"]

fig, ax = plt.subplots(figsize=(8.5, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors, autopct="%1.0f%%",
    startangle=110, pctdistance=0.78, textprops={"fontsize": 10}
)
for t in autotexts:
    t.set_color("white")
    t.set_fontweight("bold")
ax.set_title("Infineon FY2024 revenue by segment (Total €14,955m)", fontsize=12, pad=14)
plt.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 3. R&D spend FY2022-FY2025 (€m) and as % of revenue
# ---------------------------------------------------------------------------
rd_fy = ["FY22", "FY23", "FY24", "FY25"]
rd_eur_m = [1798, 1985, 2161, 2227]
rd_rev   = [14218, 16309, 14955, 14662]
rd_pct   = [r / s * 100 for r, s in zip(rd_eur_m, rd_rev)]

fig, ax1 = plt.subplots(figsize=(9.5, 5.5))
b = ax1.bar(rd_fy, rd_eur_m, color="#1f4e8c", label="R&D (€m)")
ax1.set_ylabel("R&D spend (€m)", color="#1f4e8c")
ax1.tick_params(axis="y", labelcolor="#1f4e8c")
for bar, v in zip(b, rd_eur_m):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 30, f"€{v:,}m", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(rd_fy, rd_pct, color="#d24c2e", marker="o", linewidth=2.2, label="R&D % of revenue")
ax2.set_ylabel("R&D as % of revenue", color="#d24c2e")
ax2.tick_params(axis="y", labelcolor="#d24c2e")
ax2.set_ylim(10, 17)
for i, v in enumerate(rd_pct):
    ax2.text(i, v + 0.2, f"{v:.1f}%", ha="center", fontsize=9, color="#d24c2e")

plt.title("Infineon R&D investment — defensive spend through the cycle (FY2022-FY2025)", fontsize=12, pad=14)
fig.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_rd_intensity.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 4. SiC market trajectory (industry) and AI data-center power target
# ---------------------------------------------------------------------------
years = [2025, 2026, 2027, 2028, 2029, 2030]
sic_market = [3.83, 4.81, 6.05, 7.61, 9.56, 12.03]  # USD bn, MarketsandMarkets SiC 25-30
infineon_ai = [0.6, 1.5, 2.5, 3.5, 4.5, 6.0]         # €bn, mgmt €1.5bn 2026 target; out-years analyst extrapolation per Infineon AI guidance trajectory

fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax1.plot(years, sic_market, color="#1f4e8c", marker="s", linewidth=2.4, label="Global SiC power semi market (USD bn)")
ax1.set_ylabel("Global SiC power semi market (USD bn)", color="#1f4e8c")
ax1.tick_params(axis="y", labelcolor="#1f4e8c")
ax1.set_xlabel("Calendar year")
for i, v in enumerate(sic_market):
    ax1.text(years[i], v + 0.2, f"${v}", ha="center", fontsize=9, color="#1f4e8c")

ax2 = ax1.twinx()
ax2.plot(years, infineon_ai, color="#d24c2e", marker="o", linewidth=2.4, label="Infineon AI data-center power rev (€bn)")
ax2.set_ylabel("Infineon AI data-center power revenue (€bn)", color="#d24c2e")
ax2.tick_params(axis="y", labelcolor="#d24c2e")
for i, v in enumerate(infineon_ai):
    ax2.text(years[i], v + 0.1, f"€{v}", ha="center", fontsize=9, color="#d24c2e")

plt.title("Two growth levers: global SiC market (25.7% CAGR) and Infineon AI data-center power", fontsize=12, pad=14)
fig.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_sic_ai_growth.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 5. Peer comparison TTM P/E and P/S (XETR:IFX vs peers, May 2026)
# ---------------------------------------------------------------------------
peers = ["IFX", "STM", "NXPI", "ON", "ADI", "TXN", "MCHP"]
# All values per Yahoo Finance / yfinance, accessed 2026-05-20
pe_ttm  = [82.9, 405.4, 29.5, 80.5, 71.8, 51.5, 425.5]
ps_ttm  = [5.84, 4.66, 6.16, 7.02, 16.30, 14.89, 10.75]

fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))

colors = ["#d24c2e" if p == "IFX" else "#3b6bbc" for p in peers]

axes[0].bar(peers, pe_ttm, color=colors)
axes[0].set_title("TTM P/E (May 2026)")
axes[0].set_ylabel("TTM P/E (×)")
for i, v in enumerate(pe_ttm):
    axes[0].text(i, v + 1.5, f"{v:.1f}", ha="center", fontsize=9)
axes[0].axhline(np.median(pe_ttm), color="gray", linestyle="--", linewidth=1, label=f"Peer median {np.median(pe_ttm):.1f}×")
axes[0].legend()

axes[1].bar(peers, ps_ttm, color=colors)
axes[1].set_title("TTM P/S (May 2026)")
axes[1].set_ylabel("TTM P/S (×)")
for i, v in enumerate(ps_ttm):
    axes[1].text(i, v + 0.15, f"{v:.1f}", ha="center", fontsize=9)
axes[1].axhline(np.median(ps_ttm), color="gray", linestyle="--", linewidth=1, label=f"Peer median {np.median(ps_ttm):.1f}×")
axes[1].legend()

fig.suptitle("Infineon vs. analog / power-semi peers — TTM valuation (May 2026)", fontsize=12, y=1.02)
fig.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 6. Capex intensity FY2020 - FY2026e
# ---------------------------------------------------------------------------
capex = [1108, 1545, 2410, 3072, 2820, 2300, 2200]   # €m investments (PP&E + intangibles + cap dev); FY26e per FY25 press release
capex_intensity = [c / r * 100 for c, r in zip(capex, rev_eur_m)]

fig, ax = plt.subplots(figsize=(10, 5.5))
b = ax.bar(fy, capex, color="#6c9c6c")
ax.set_ylabel("Investments (€m)")
ax.set_xlabel("Fiscal Year")
for bar, v, ci in zip(b, capex, capex_intensity):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 80, f"€{v:,}m\n({ci:.0f}% of rev)", ha="center", fontsize=8.5)

ax.set_title("Infineon capex — heavy investment cycle for Kulim 3 (SiC) and Dresden (300mm)", fontsize=12, pad=14)
plt.tight_layout()
plt.savefig(f"{OUT}/infineon_xetr_capex.png", dpi=150, bbox_inches="tight")
plt.close()

print("All Infineon XETR:IFX charts generated successfully.")
print("Outputs:")
for f in [
    "infineon_xetr_revenue_margin.png",
    "infineon_xetr_segment_mix.png",
    "infineon_xetr_rd_intensity.png",
    "infineon_xetr_sic_ai_growth.png",
    "infineon_xetr_peer_valuation.png",
    "infineon_xetr_capex.png",
]:
    print(" -", f)
