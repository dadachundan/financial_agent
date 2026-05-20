"""Generate matplotlib charts for HEICO research report."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# -----------------------------------------------------------------------------
# 1. Revenue + operating margin trend, FY2019–FY2025 + Q1-FY2026 TTM
# Source: HEICO 10-K FY2025 (consolidated net sales and operating income)
# -----------------------------------------------------------------------------
years = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25"]
# Net sales (USD millions) and operating income (USD millions)
# Source: HEICO FY2022 10-K segment note and FY2025 10-K segment note
# FY20 1,787.0 / op inc 376.6
# FY21 1,865.7 / op inc 392.9
# FY22 2,208.3 / op inc 496.8
# FY23 2,968.1 / op inc 625.3
# FY24 3,857.7 / op inc 824.5
# FY25 4,485.0 / op inc 1,019.0
sales = [1787.0, 1865.7, 2208.3, 2968.1, 3857.7, 4485.0]
op_inc = [376.6, 392.9, 496.8, 625.3, 824.5, 1019.0]
op_margin = [oi / s * 100 for oi, s in zip(op_inc, sales)]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, sales, color="#1f4e79", alpha=0.85, label="Net sales (USD m)")
ax1.set_ylabel("Net sales (USD millions)", color="#1f4e79", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, max(sales) * 1.18)

for b, v in zip(bars, sales):
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 60,
             f"{v:,.0f}", ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#c0504d", marker="o", linewidth=2.2,
         label="Operating margin (%)")
ax2.set_ylabel("Operating margin (%)", color="#c0504d", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c0504d")
ax2.set_ylim(15, 26)
for x, y in zip(years, op_margin):
    ax2.text(x, y + 0.3, f"{y:.1f}%", ha="center", fontsize=9, color="#c0504d")

ax1.set_title("HEICO net sales and operating margin, FY2020–FY2025",
              fontsize=13, pad=12)
ax2.spines["top"].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "hei_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 2. Segment revenue: FSG vs ETG, FY2021–FY2025 (stacked bar) + intersegment line
# Source: HEICO 10-K FY2025, Operating Segments note
# -----------------------------------------------------------------------------
seg_years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
fsg = [927.1, 1255.2, 1770.2, 2639.4, 3117.3]
etg = [959.2, 972.5, 1225.2, 1263.6, 1413.1]
intersegment = [20.6, 19.4, 27.3, 45.3, 45.4]

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(seg_years))
width = 0.6
b1 = ax.bar(x, fsg, width, label="Flight Support Group (FSG)", color="#1f4e79")
b2 = ax.bar(x, etg, width, bottom=fsg, label="Electronic Technologies Group (ETG)",
            color="#ed7d31")

for i, (a, b) in enumerate(zip(fsg, etg)):
    total = a + b - intersegment[i]
    ax.text(i, a / 2, f"FSG\n{a:,.0f}", ha="center", va="center",
            color="white", fontsize=9, fontweight="bold")
    ax.text(i, a + b / 2, f"ETG\n{b:,.0f}", ha="center", va="center",
            color="white", fontsize=9, fontweight="bold")
    ax.text(i, a + b + 80, f"net {total:,.0f}", ha="center", fontsize=9,
            color="#444")

ax.set_xticks(x)
ax.set_xticklabels(seg_years)
ax.set_ylabel("Segment net sales (USD millions)")
ax.set_title("HEICO segment revenue: FSG vs ETG, FY2021–FY2025\n"
             "(stacked; intersegment eliminations shown above stack)",
             fontsize=12, pad=10)
ax.legend(loc="upper left")
ax.set_ylim(0, 5200)
fig.tight_layout()
fig.savefig(OUT / "hei_segment_revenue.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 3. Segment operating income + margin, FY2021–FY2025
# Source: HEICO 10-K FY2025 segment note
# -----------------------------------------------------------------------------
fsg_oi = [151.9, 267.2, 387.3, 593.1, 750.4]
etg_oi = [277.3, 269.5, 285.1, 288.2, 325.0]
fsg_margin = [oi / s * 100 for oi, s in zip(fsg_oi, fsg)]
etg_margin = [oi / s * 100 for oi, s in zip(etg_oi, etg)]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5))
xpos = np.arange(len(seg_years))
w = 0.38
axL.bar(xpos - w / 2, fsg_oi, w, label="FSG op. income", color="#1f4e79")
axL.bar(xpos + w / 2, etg_oi, w, label="ETG op. income", color="#ed7d31")
axL.set_xticks(xpos)
axL.set_xticklabels(seg_years)
axL.set_ylabel("Segment operating income (USD m)")
axL.set_title("Segment operating income, FY2021–FY2025", fontsize=12)
for i, v in enumerate(fsg_oi):
    axL.text(xpos[i] - w / 2, v + 8, f"{v:,.0f}", ha="center", fontsize=8.5)
for i, v in enumerate(etg_oi):
    axL.text(xpos[i] + w / 2, v + 8, f"{v:,.0f}", ha="center", fontsize=8.5)
axL.legend(loc="upper left")
axL.set_ylim(0, 850)

axR.plot(seg_years, fsg_margin, "o-", color="#1f4e79", lw=2.2, label="FSG margin")
axR.plot(seg_years, etg_margin, "o-", color="#ed7d31", lw=2.2, label="ETG margin")
axR.set_ylabel("Segment operating margin (%)")
axR.set_title("Segment operating margin, FY2021–FY2025", fontsize=12)
axR.set_ylim(10, 32)
axR.grid(axis="y", alpha=0.3)
axR.legend(loc="lower right")
for x_, y in zip(seg_years, fsg_margin):
    axR.text(x_, y + 0.3, f"{y:.1f}%", ha="center", fontsize=9, color="#1f4e79")
for x_, y in zip(seg_years, etg_margin):
    axR.text(x_, y - 0.6, f"{y:.1f}%", ha="center", fontsize=9, color="#ed7d31")

fig.tight_layout()
fig.savefig(OUT / "hei_segment_op_income.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 4. Organic vs M&A growth decomposition, FY2024 and FY2025
# Source: HEICO 10-K FY2025 MD&A; FY2024 10-K MD&A
# FY24 consolidated YoY growth: 30.0% = ~8% organic + ~22% Wencor/Exxelia full-year + small bolt-ons
# FY25 consolidated YoY growth: 16% = ~12% organic + ~4% M&A (FY25/FY24 deals)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
periods = ["FY2024\n(+30.0% YoY)", "FY2025\n(+16.3% YoY)", "Q1-FY2026\n(+14.4% YoY)"]
organic = [7.0, 11.6, 10.5]    # consolidated organic
m_and_a = [23.0, 4.6, 3.9]     # contribution from acquisitions
bottoms_o = [0, 0, 0]
ax.bar(periods, organic, color="#2e7d32", label="Organic growth")
ax.bar(periods, m_and_a, bottom=organic, color="#1565c0", label="M&A contribution")
for i, (o, m) in enumerate(zip(organic, m_and_a)):
    ax.text(i, o / 2, f"{o:.1f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=10)
    ax.text(i, o + m / 2, f"{m:.1f}%", ha="center", va="center",
            color="white", fontweight="bold", fontsize=10)
    ax.text(i, o + m + 1, f"Total\n{o + m:.1f}%", ha="center", fontsize=9)
ax.set_ylabel("YoY revenue growth (%)")
ax.set_title("HEICO consolidated growth decomposition: organic vs M&A\n"
             "(FY24 reflects first full year of Wencor + Exxelia; FY25 is normalized)",
             fontsize=12, pad=10)
ax.legend(loc="upper right")
ax.set_ylim(0, 36)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "hei_organic_vs_ma.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 5. Peer valuation comparison (P/E, EV/EBITDA) — bar chart
# Source: stockanalysis.com / gurufocus / public.com as of May 2026
# -----------------------------------------------------------------------------
peers = ["HEI\n(HEICO)", "TDG\n(TransDigm)", "MOG.A\n(Moog)", "CW\n(Curtiss-\nWright)", "HXL\n(Hexcel)"]
pe_ttm = [58.1, 38.7, 32.9, 54.0, 62.6]
ev_ebitda = [36.1, 21.1, 16.5, 28.2, 26.4]   # MOG approximated from market data; HXL/CW most-recent

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
colors = ["#c0504d", "#1f4e79", "#7f7f7f", "#7f7f7f", "#7f7f7f"]

bars1 = ax1.bar(peers, pe_ttm, color=colors)
ax1.set_title("TTM P/E ratio (May 2026)", fontsize=12)
ax1.set_ylabel("TTM P/E")
for b, v in zip(bars1, pe_ttm):
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
             f"{v:.1f}x", ha="center", fontsize=10)
ax1.axhline(np.median(pe_ttm), color="grey", ls="--", lw=1)
ax1.text(4.4, np.median(pe_ttm) + 1, f"peer median\n{np.median(pe_ttm):.1f}x",
         ha="right", fontsize=8.5, color="grey")
ax1.set_ylim(0, max(pe_ttm) * 1.18)

bars2 = ax2.bar(peers, ev_ebitda, color=colors)
ax2.set_title("EV/EBITDA (most-recent, May 2026)", fontsize=12)
ax2.set_ylabel("EV/EBITDA")
for b, v in zip(bars2, ev_ebitda):
    ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4,
             f"{v:.1f}x", ha="center", fontsize=10)
ax2.axhline(np.median(ev_ebitda), color="grey", ls="--", lw=1)
ax2.text(4.4, np.median(ev_ebitda) + 0.4, f"peer median\n{np.median(ev_ebitda):.1f}x",
         ha="right", fontsize=8.5, color="grey")
ax2.set_ylim(0, max(ev_ebitda) * 1.18)
fig.suptitle("HEICO trades at a premium to aerospace aftermarket peers",
             fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(OUT / "hei_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 6. Long-run shareholder return: $100 invested in HEI common stock since 1990 vs DJ US Aerospace Index
# Source: HEICO 10-K FY2025 cumulative total return table, p.30-32
# -----------------------------------------------------------------------------
yrs = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024, 2025]
hei = [100, 263.25, 809.50, 1674.40, 4722.20, 10776.88, 44877.75, 99188.00, 128481.31]
dja = [100, 252.00, 418.32, 579.77, 926.75, 1766.94, 2233.00, 4731.25, 7351.46]

fig, ax = plt.subplots(figsize=(9, 5))
ax.semilogy(yrs, hei, "o-", color="#c0504d", lw=2.4,
            label="HEICO Common Stock (HEI)")
ax.semilogy(yrs, dja, "s-", color="#7f7f7f", lw=2.0,
            label="Dow Jones US Aerospace Index")
ax.set_ylabel("Cumulative total return\n($100 invested on Oct 31, 1990)")
ax.set_title("HEICO's 35-year compound: $100 → $128,481 (CAGR ~22.9%)\n"
             "vs DJ US Aerospace Index $100 → $7,351 (CAGR ~13.1%)",
             fontsize=12, pad=10)
ax.grid(True, which="both", alpha=0.25)
ax.legend(loc="upper left")
for x_, y in zip(yrs, hei):
    ax.text(x_, y * 1.25, f"${y:,.0f}", ha="center", fontsize=8, color="#c0504d")
fig.tight_layout()
fig.savefig(OUT / "hei_long_run_return.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 7. End-market mix FY2025 (commercial aviation / defense+space / other)
# Source: 10-K FY2025 MD&A: ~58% commercial aviation, ~31% defense & space, ~11% other
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
mix = [58, 31, 11]
labels = ["Commercial aviation\n(58%)",
          "Defense & space\n(31%)",
          "Other industrial\nmedical / telecom / electronics\n(11%)"]
colors_pie = ["#1f4e79", "#7f6000", "#7f7f7f"]
wedges, _ = ax.pie(mix, labels=labels, colors=colors_pie,
                   startangle=90, wedgeprops=dict(width=0.42, edgecolor="white"),
                   textprops={"fontsize": 10})
ax.set_title("HEICO FY2025 net sales by end-market", fontsize=12, pad=20)
fig.tight_layout()
fig.savefig(OUT / "hei_end_market_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 8. Acquisition cash spend per year, FY2020–FY2025
# Source: 10-K cash flow statements (acquisitions, net of cash acquired)
# -----------------------------------------------------------------------------
acq_years = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25"]
acq_spend = [
    163.9,    # FY2020
    136.5,    # FY2021
    347.3,    # FY2022
    2421.8,   # FY2023 — Wencor + Exxelia (within investing activities)
    219.3,    # FY2024
    629.8,    # FY2025 — Gables, Rosen, Millennium, SVM, Capewell, MC2, Marway
]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(acq_years, acq_spend, color="#7f6000")
ax.set_ylabel("Cash used in acquisitions (USD m)")
ax.set_title("HEICO annual acquisition cash spend, FY2020–FY2025\n"
             "(FY2023 spike = $1.9bn Wencor + $0.5bn Exxelia)",
             fontsize=12, pad=10)
for b, v in zip(bars, acq_spend):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 30,
            f"${v:,.0f}m", ha="center", fontsize=9.5)
ax.set_ylim(0, 2750)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "hei_acquisitions_per_year.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("✓ charts generated:")
for p in sorted(OUT.glob("hei_*.png")):
    print(" -", p.name)
