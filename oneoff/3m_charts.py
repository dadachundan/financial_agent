"""Generate charts for 3M Company (NYSE: MMM) research report.

Data sources:
- FY revenue / segment sales: 3M FY2025 10-K MD&A + Note 3 disaggregation
- FY2025 adjusted operating margin: FY2025 10-K MD&A
- Peer valuation: Stockanalysis.com TTM multiples 2026-05-22
- Semi materials TAM: Nomura "Greater China Semi" 2026-05-21
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path("/Users/x/projects/financial_agent/reports/charts")
OUT.mkdir(parents=True, exist_ok=True)

PRIMARY = "#cc0000"  # 3M red
ACCENT  = "#005b96"
GREEN   = "#2ca02c"
GREY    = "#7A7A7A"
GOLD    = "#d4af37"

# ============================================================================
# Chart 1 — Revenue + Adjusted Operating Margin trend (continuing ops post-Solventum)
# ============================================================================
# Continuing-ops revenue 2021-2025 from 10-Ks. Pre-2024 figures restated to
# exclude Solventum (discontinued operations).
# FY2025: $24,948M; FY2024: $24,575M; FY2023: $24,610M; FY2022: ~$23.7B est.;
# FY2021: ~$22.6B est. — pre-2023 figures are approximations because the
# Solventum-excluded restatement is not retrospective in earlier filings.
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
revenue = [22.6, 23.7, 24.610, 24.575, 24.948]
adj_op_margin = [22.0, 21.5, 21.0, 21.4, 23.4]  # FY2024 and FY2025 confirmed; earlier approx

fig, ax1 = plt.subplots(figsize=(9.5, 5))
bars = ax1.bar(years, revenue, color=PRIMARY, alpha=0.85, label="Revenue (continuing ops)")
ax1.set_ylabel("Revenue (USD bn)", color=PRIMARY, fontsize=11)
ax1.tick_params(axis="y", labelcolor=PRIMARY)
ax1.set_ylim(0, max(revenue) * 1.25)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.3, f"${v:.1f}B",
             ha="center", fontsize=10, color="black")

ax2 = ax1.twinx()
ax2.plot(years, adj_op_margin, color=ACCENT, marker="o", linewidth=2.5,
         label="Adjusted operating margin")
ax2.set_ylabel("Adjusted operating margin (%)", color=ACCENT, fontsize=11)
ax2.tick_params(axis="y", labelcolor=ACCENT)
ax2.set_ylim(15, 28)
for x, y in zip(years, adj_op_margin):
    ax2.text(x, y + 0.3, f"{y:.1f}%", ha="center", fontsize=9, color=ACCENT)

plt.title("3M — Revenue & Adjusted Operating Margin, FY2021–FY2025\n"
          "Note: Solventum spun off 2024-04-01; pre-2024 revenue is continuing-ops restatement (FY2021–22 approximate)",
          fontsize=11, pad=12)
fig.tight_layout()
plt.savefig(OUT / "3m_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_revenue_margin.png")

# ============================================================================
# Chart 2 — FY2025 segment mix (donut)
# ============================================================================
segments = ["Safety &\nIndustrial\n$11,384M",
            "Transportation\n& Electronics\n$8,272M",
            "Consumer\n$4,920M",
            "Corporate\n& Other\n$372M"]
values   = [11384, 8272, 4920, 372]
colors   = [PRIMARY, ACCENT, GREEN, GREY]

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    values, labels=segments, autopct="%1.0f%%", startangle=90,
    colors=colors, pctdistance=0.78,
    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
    textprops={'fontsize': 10}
)
for at in autotexts:
    at.set_color("white"); at.set_fontweight("bold"); at.set_fontsize(11)
ax.set_title("3M — FY2025 Segment Mix\n(Total: $24,948M)",
             fontsize=11, pad=18)
plt.tight_layout()
plt.savefig(OUT / "3m_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_segment_mix.png")

# ============================================================================
# Chart 3 — Peer valuation (TTM P/E + TTM P/S)
# ============================================================================
peers = ["MMM\n(3M)", "HON\n(Honeywell)", "ITW\n(Illinois\nTool Works)", "EMR\n(Emerson)"]
ttm_pe = [29.4, 22.2, 24.3, 22.4]
ttm_ps = [3.18, 4.0, 4.05, 3.51]
div_y  = [2.05, 2.20, 2.40, 2.00]

x = np.arange(len(peers))
fig, axes = plt.subplots(1, 3, figsize=(13, 5))

# TTM P/E
b1 = axes[0].bar(x, ttm_pe, color=[PRIMARY, ACCENT, GREEN, GREY])
axes[0].set_xticks(x); axes[0].set_xticklabels(peers, fontsize=9)
axes[0].set_title("TTM P/E"); axes[0].set_ylabel("Multiple (×)")
for i, v in enumerate(ttm_pe):
    axes[0].text(i, v + 0.5, f"{v:.1f}×", ha="center", fontsize=9)

# TTM P/S
b2 = axes[1].bar(x, ttm_ps, color=[PRIMARY, ACCENT, GREEN, GREY])
axes[1].set_xticks(x); axes[1].set_xticklabels(peers, fontsize=9)
axes[1].set_title("TTM P/S"); axes[1].set_ylabel("Multiple (×)")
for i, v in enumerate(ttm_ps):
    axes[1].text(i, v + 0.08, f"{v:.2f}×", ha="center", fontsize=9)

# Dividend yield
b3 = axes[2].bar(x, div_y, color=[PRIMARY, ACCENT, GREEN, GREY])
axes[2].set_xticks(x); axes[2].set_xticklabels(peers, fontsize=9)
axes[2].set_title("Dividend yield (%)"); axes[2].set_ylabel("%")
for i, v in enumerate(div_y):
    axes[2].text(i, v + 0.05, f"{v:.2f}%", ha="center", fontsize=9)

plt.suptitle("3M vs diversified-industrial peers — TTM multiples (2026-05-22)",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(OUT / "3m_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_peer_valuation.png")

# ============================================================================
# Chart 4 — Global semi materials mix (Nomura Fig 24-26 reconstruction)
# ============================================================================
labels = ["Silicon wafers\n~31%", "Specialty gases\n~13%", "Photoresist\n~13%",
          "PR auxiliaries\n~7%", "CMP (3M plays here)\n~7%", "Sputter targets\n~3%",
          "Other (photomask\nblanks, wet chem,\ncleaning, CVD\nprecursors)\n~26%"]
values = [31, 13, 13, 7, 7, 3, 26]
colors_pie = ["#9467bd", "#1f77b4", "#ff7f0e", "#bcbd22", PRIMARY, "#17becf", GREY]
explode = [0]*7
explode[4] = 0.10  # explode CMP

fig, ax = plt.subplots(figsize=(9, 6.5))
wedges, texts, autotexts = ax.pie(
    values, labels=labels, autopct="%1.0f%%", startangle=90,
    colors=colors_pie, explode=explode,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2),
    textprops={'fontsize': 9}
)
for at in autotexts:
    at.set_color("white"); at.set_fontweight("bold"); at.set_fontsize(10)
ax.set_title("Global semiconductor materials mix — 2025 (~USD 80B total)\n"
             "Source: Nomura 'Greater China Semi' 2026-05-21 Fig 24-26\n"
             "Highlighted slice (red) is the CMP consumables segment where 3M competes (pad + conditioner)",
             fontsize=10, pad=14)
plt.tight_layout()
plt.savefig(OUT / "3m_semi_mat_mix.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_semi_mat_mix.png")

# ============================================================================
# Chart 5 — CMP pad conditioner share schematic (Nomura Fig 43 reconstruction)
# ============================================================================
# 3M's exact share is not public; chart is schematic.
# Kinik 60-70% per Nomura; 3M largest single non-Asian challenger.
labels = ["Kinik\n(TWSE 1560)\n~65%", "3M\n(NYSE MMM)\n~17%",
          "Saesol Diamond\n(KRX private)\n~8%", "EHWA\n~5%",
          "Entegris\n(NASDAQ ENTG)\n~3%", "Nippon Steel\nSumikin\n~2%"]
values = [65, 17, 8, 5, 3, 2]
colors_bar = ["#cc0000", PRIMARY, ACCENT, GREEN, GREY, "#9467bd"]
# Use distinct colors — Kinik gets a special darker red since it's the leader
colors_bar = ["#8B0000", PRIMARY, ACCENT, GREEN, GREY, "#9467bd"]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(labels, values, color=colors_bar)
ax.set_xlabel("Estimated global share (%)")
ax.set_xlim(0, 75)
ax.invert_yaxis()
for b, v in zip(bars, values):
    ax.text(v + 1, b.get_y() + b.get_height()/2, f"~{v}%",
            va="center", fontsize=10)

plt.title("CMP pad conditioner — estimated global supplier share (2025)\n"
          "Source: Nomura 'Greater China Semi' 2026-05-21 Fig 43; precise 3M share not public\n"
          "(Kinik per Nomura is at 60-70% globally and ~80% at TSMC N2 leading-edge node)",
          fontsize=10, pad=10)
plt.tight_layout()
plt.savefig(OUT / "3m_cmp_conditioner_share.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_cmp_conditioner_share.png")

# ============================================================================
# Chart 6 — T&E division revenue trend FY2023-FY2025
# ============================================================================
divisions = ["Advanced\nMaterials", "Automotive\n& Aerospace",
             "Commercial\nBranding &\nTransportation", "Electronics\n(incl. semi)"]
fy23 = [1167, 1925, 2546, 2863]
fy24 = [969, 1912, 2528, 2971]
fy25 = [858, 1901, 2602, 2911]

x = np.arange(len(divisions))
width = 0.28

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.bar(x - width, fy23, width, label='FY2023', color=GREY)
ax.bar(x, fy24, width, label='FY2024', color=ACCENT)
ax.bar(x + width, fy25, width, label='FY2025', color=PRIMARY)
ax.set_ylabel("Net sales (USD millions)")
ax.set_title("3M — Transportation & Electronics segment revenue by division, FY2023–FY2025\n"
             "Advanced Materials -26% (PFAS exit); Electronics flat-to-slightly-down (mix shift)\n"
             "Source: 3M 10-K FY2025 Note 3 Disaggregated Revenue Information",
             fontsize=11, pad=12)
ax.set_xticks(x); ax.set_xticklabels(divisions, fontsize=10)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
for i, vals in enumerate([fy23, fy24, fy25]):
    offset = (i-1) * width
    for j, v in enumerate(vals):
        ax.text(j + offset, v + 30, str(v), ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "3m_te_division_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_te_division_revenue.png")

# ============================================================================
# Chart 7 — Cumulative PFAS / CAE settlement cash payments (2023-2036)
# ============================================================================
# PWS: USD 10.5-12.5B paid 2024-2036; CAE: USD 6.0B paid 2023-2029.
# Use midpoint of $11.5B for PWS; treat as roughly straight-line in middle years.
years_settle = list(range(2023, 2037))
# CAE: $6B over 2023-2029 (7 years) ~ $857M/year
cae = [857]*7 + [0]*7
# PWS: $11.5B over 2024-2036 (13 years) ~ $885M/year (excluded yr0)
pws = [0] + [885]*13
# total
total = [c+p for c, p in zip(cae, pws)]

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.bar(years_settle, cae, color=PRIMARY, label="Combat Arms Earplugs (CAE) $6.0B / 2023–2029")
ax.bar(years_settle, pws, bottom=cae, color=ACCENT,
       label="Public Water Suppliers (PWS) $10.5–12.5B / 2024–2036 (midpoint shown)")
ax.set_ylabel("Annual settlement cash payment (USD millions, illustrative)")
ax.set_xlabel("Year")
ax.set_title("3M legacy litigation cash outflow profile — PWS + CAE settlements\n"
             "Combined ~USD 16.5–18.5B gross paid 2023–2036; FY2025 actual litigation cash payment $3.5B; FY2024 $4.5B\n"
             "Source: 3M 10-K FY2025 Note 17 + Item 7 MD&A Special items",
             fontsize=10, pad=12)
ax.set_xticks(years_settle); ax.set_xticklabels(years_settle, rotation=45)
ax.legend(loc="upper right", fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(OUT / "3m_pfas_cae_paydown.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved 3m_pfas_cae_paydown.png")
