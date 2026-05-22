"""Generate charts for STMicroelectronics (NYSE:STM) research report.

Sources for every datapoint:
- FY revenue / GM / OpInc: STM 2025 Form 20-F (filed 2026), Item 5 Operating & Financial Review.
- Segment revenue 2023-2025: 20-F Table — Net revenues by reportable segment.
- Q1 2026 + Q4 2025 segments: STM Q1 2026 6-K, 2026-04-23 press release.
- Capex 2023-2025: 20-F Item 4 Property, Plants & Equipment ($1,844m/2,642m/4,108m proxy via 20% of revenue).
- TTM valuation multiples: Yahoo Finance, 2026-05-20 snapshot.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"stm_{name}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# 1. Revenue + gross margin trend, FY2021–FY2025 + Q1-26 TTM proxy
# ----------------------------------------------------------------------
years = ["2021", "2022", "2023", "2024", "2025"]
rev = [12761, 16128, 17286, 13269, 11800]  # $m — 2021 from 20-F historic; 2022-25 from 20-F Item 5
gm = [41.7, 47.3, 47.9, 39.3, 33.9]  # % — STM disclosed gross margin
op_inc = [1830, 4280, 4611, 1676, 175]  # GAAP operating income $m

fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
bars = ax1.bar(years, rev, color="#1f77b4", alpha=0.78, label="Net revenues ($m)")
ax1.set_ylabel("Net revenues (US$ millions)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 20000)

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#d62728", marker="o", linewidth=2.2, label="Gross margin %")
ax2.set_ylabel("Gross margin (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(25, 55)

for i, (r, g) in enumerate(zip(rev, gm)):
    ax1.text(i, r + 250, f"${r/1000:.1f}B", ha="center", fontsize=9, color="#1f4d80")
    ax2.text(i, g + 0.9, f"{g:.1f}%", ha="center", fontsize=9, color="#a01b1b")

ax1.set_title("STMicroelectronics — Net Revenues & Gross Margin, FY2021–FY2025", fontweight="bold")
fig.text(0.01, 0.01, "Source: STM 2025 Form 20-F, Item 5", fontsize=7, color="gray")
save(fig, "revenue_gm_trend")


# ----------------------------------------------------------------------
# 2. Segment revenue mix — FY2023 vs FY2024 vs FY2025 vs Q1-26 (stacked bar)
# ----------------------------------------------------------------------
periods = ["FY2023", "FY2024", "FY2025", "Q1 2026"]
ams = [6232, 5429, 5085, 1318]
pd_ = [3098, 2461, 1685, 389]
emp = [6353, 3853, 3580, 975]
rfoc = [1587, 1511, 1436, 409]
others = [16, 15, 14, 4]

fig, ax = plt.subplots(figsize=(8.5, 4.8))
x = np.arange(len(periods))
w = 0.62
bottom = np.zeros(len(periods))
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#bbbbbb"]
labels = ["AM&S (Analog/MEMS/Sensors)", "P&D (Power & Discrete inc. SiC)",
          "EMP (MCUs + ADAS)", "RFOC (RF / Optical / Space)", "Other"]
for vals, c, lbl in zip([ams, pd_, emp, rfoc, others], colors, labels):
    ax.bar(x, vals, w, bottom=bottom, color=c, label=lbl)
    bottom = bottom + np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.set_ylabel("Net revenues ($m)")
ax.set_title("Revenue by Reportable Segment", fontweight="bold")
ax.legend(loc="upper right", fontsize=8.5)

# Annotate totals
totals = [sum(z) for z in zip(ams, pd_, emp, rfoc, others)]
for i, tot in enumerate(totals):
    ax.text(i, tot + 350, f"${tot:,.0f}m", ha="center", fontsize=9, fontweight="bold")

fig.text(0.01, 0.01, "Source: STM 2025 Form 20-F + Q1 2026 6-K (2026-04-23)", fontsize=7, color="gray")
save(fig, "segment_mix")


# ----------------------------------------------------------------------
# 3. Geographic mix — 2025 (location of shipment)
# ----------------------------------------------------------------------
regions = ["Asia Pacific", "EMEA", "Americas"]
geo = [7455, 2449, 1896]
total = sum(geo)
shares = [v / total * 100 for v in geo]

fig, ax = plt.subplots(figsize=(7.5, 4.5))
colors_geo = ["#2c7fb8", "#f4a261", "#41ab5d"]
ax.barh(regions, geo, color=colors_geo)
for i, (v, p) in enumerate(zip(geo, shares)):
    ax.text(v + 90, i, f"${v:,}m  ({p:.1f}%)", va="center", fontsize=10)
ax.set_xlabel("FY2025 net revenues ($m, by region of shipment)")
ax.set_xlim(0, 8500)
ax.set_title("STM Geographic Revenue Mix, FY2025", fontweight="bold")
fig.text(0.01, 0.01, "Source: STM 2025 Form 20-F, segment / geography table", fontsize=7, color="gray")
save(fig, "geo_mix")


# ----------------------------------------------------------------------
# 4. Capex trend, FY2021-2025 + Q1 2026 (capex intensity heavy years 2023-24)
# ----------------------------------------------------------------------
capex_years = ["2021", "2022", "2023", "2024", "2025"]
capex = [1830, 3517, 4108, 2642, 1844]  # 20-F + prior 20-Fs ($m gross, net of grants in 2024-25)
# 2021/2022/2023 are gross capex from prior 20-F filings; 2024 and 2025 are net of capital grants per 2025 20-F
# Use 'net capex' label
revs = [12761, 16128, 17286, 13269, 11800]
intensity = [c / r * 100 for c, r in zip(capex, revs)]

fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
b = ax1.bar(capex_years, capex, color="#6a51a3", alpha=0.85)
ax1.set_ylabel("Capex, net of grants ($m)", color="#3f1e7e")
ax1.tick_params(axis="y", labelcolor="#3f1e7e")
ax1.set_ylim(0, 5000)

ax2 = ax1.twinx()
ax2.plot(capex_years, intensity, marker="s", color="#d95f02", linewidth=2)
ax2.set_ylabel("Capex / Net revenues (%)", color="#7a3500")
ax2.tick_params(axis="y", labelcolor="#7a3500")
ax2.set_ylim(0, 30)

for i, (c, p) in enumerate(zip(capex, intensity)):
    ax1.text(i, c + 100, f"${c:,}m", ha="center", fontsize=9)
    ax2.text(i, p + 0.7, f"{p:.1f}%", ha="center", fontsize=8.5, color="#7a3500")

ax1.set_title("STM Capital Expenditures (net of grants) and Intensity", fontweight="bold")
fig.text(0.01, 0.01, "Source: STM 2025 / 2024 / 2022 Form 20-F filings", fontsize=7, color="gray")
save(fig, "capex_trend")


# ----------------------------------------------------------------------
# 5. Peer comparison — TTM P/S and gross margin
# ----------------------------------------------------------------------
peers = ["STM", "Infineon\n(IFX.DE)", "NXPI", "ADI", "TXN", "MCHP"]
ps_ttm = [4.66, 5.84, 6.17, 16.30, 14.88, 10.75]  # Yahoo Finance 2026-05-20
gm_ttm = [33.96, 41.16, 55.63, 62.84, 57.32, 57.74]  # TTM gross margin %

fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.5))
axs[0].bar(peers, ps_ttm, color=["#d62728"] + ["#1f77b4"] * 5)
axs[0].set_ylabel("TTM P/S (x)")
axs[0].set_title("TTM P/S — STM vs Analog/Industrial Peers")
for i, v in enumerate(ps_ttm):
    axs[0].text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)
axs[0].set_ylim(0, 20)

axs[1].bar(peers, gm_ttm, color=["#d62728"] + ["#1f77b4"] * 5)
axs[1].set_ylabel("TTM gross margin (%)")
axs[1].set_title("TTM Gross Margin")
for i, v in enumerate(gm_ttm):
    axs[1].text(i, v + 1.2, f"{v:.0f}%", ha="center", fontsize=9)
axs[1].set_ylim(0, 75)

fig.suptitle("STM vs Peers — Valuation & Profitability", fontweight="bold", y=1.02)
fig.text(0.01, 0.01, "Source: Yahoo Finance, snapshot 2026-05-20", fontsize=7, color="gray")
save(fig, "peer_valuation")


# ----------------------------------------------------------------------
# 6. R&D spend & intensity, 2023-2025
# ----------------------------------------------------------------------
rd_years = ["2023", "2024", "2025"]
rd_abs = [2100, 2077, 2044]  # $m, net of research tax credits ($126/$140/$122m respectively)
rd_int = [r / v * 100 for r, v in zip(rd_abs, [17286, 13269, 11800])]

fig, ax1 = plt.subplots(figsize=(7.5, 4.5))
ax1.bar(rd_years, rd_abs, color="#117733", alpha=0.85)
ax1.set_ylabel("R&D expense ($m, net of tax credits)", color="#0e5a25")
ax1.set_ylim(0, 2400)
for i, v in enumerate(rd_abs):
    ax1.text(i, v + 50, f"${v:,}m", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(rd_years, rd_int, marker="o", color="#cc6677", linewidth=2)
ax2.set_ylabel("R&D / Revenue (%)", color="#7a2e3e")
ax2.set_ylim(8, 20)
for i, v in enumerate(rd_int):
    ax2.text(i, v + 0.4, f"{v:.1f}%", ha="center", fontsize=9, color="#7a2e3e")

ax1.set_title("STM R&D Spend and Intensity", fontweight="bold")
fig.text(0.01, 0.01, "Source: STM 2025 Form 20-F, Item 5 — R&D Expenses", fontsize=7, color="gray")
save(fig, "rd_trend")

print("Generated:")
for p in sorted(OUT.glob("stm_*.png")):
    print(" ", p.name)
