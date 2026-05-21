#!/usr/bin/env python3
"""Charts for Shell plc (NYSE:SHEL) company-research report.

All figures sourced from Shell Form 20-F 2025 (FY2025, filed March 2026)
and from peer 10-K / 20-F / Annual Report 2024 filings as cited in the
markdown report.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight", "font.size": 10})

YEARS = ["2023", "2024", "2025"]

# Shell brand-ish palette (yellow/red restrained — using deep navy + warm accents)
NAVY    = "#1F3A5F"
BLUE    = "#2E75B6"
LBLUE   = "#9DC3E6"
RED     = "#C0392B"
ORANGE  = "#E58E26"
YELLOW  = "#F1C40F"
GREEN   = "#27AE60"
GREY    = "#7F8C8D"

# ─────────────────────────────────────────────────────────────────────
# 1) Total revenue + Adjusted Earnings — 2023-2025 (dual-axis)
# Source: 20-F 2025 selected financial data
# Total revenue: 316,620 / 284,312 / 266,886
# Adjusted Earnings: 28,250 / 23,716 / 18,528
rev      = [316.620, 284.312, 266.886]   # USD bn
adj_earn = [28.250,   23.716,  18.528]   # USD bn

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(YEARS, rev, color=NAVY, label="Total revenue (USD bn)")
ax1.set_ylabel("Total revenue (USD bn)", color=NAVY)
ax1.tick_params(axis="y", labelcolor=NAVY)
ax2 = ax1.twinx()
ax2.plot(YEARS, adj_earn, color=ORANGE, marker="o", linewidth=2.2,
         label="Adjusted Earnings (USD bn)")
ax2.set_ylabel("Adjusted Earnings (USD bn)", color=ORANGE)
ax2.tick_params(axis="y", labelcolor=ORANGE)
for i, v in enumerate(rev):
    ax1.text(i, v + 4, f"${v:.0f}B", ha="center", fontsize=9, color=NAVY)
for i, v in enumerate(adj_earn):
    ax2.text(i, v + 0.8, f"${v:.1f}B", ha="center", fontsize=9, color=ORANGE)
ax1.set_title("Shell plc — Total Revenue & Adjusted Earnings (2023–2025)")
ax1.set_ylim(0, 360)
ax2.set_ylim(0, 35)
plt.tight_layout()
plt.savefig(OUT / "shel_revenue_adjearnings.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────
# 2) Segment Adjusted Earnings — 2024 vs 2025 (stacked, by segment)
# Source: 20-F 2025 segment table (Adjusted Earnings plus non-controlling interest)
segs = ["Integrated\nGas", "Upstream", "Marketing",
        "Chemicals &\nProducts", "Renewables\n& Energy Sol.", "Corporate"]
y2024 = [11.390,  8.395, 3.885, 2.934, -0.497, -1.968]
y2025 = [ 8.024,  7.442, 3.994, 1.051,  0.172, -1.870]

x = np.arange(len(segs))
w = 0.38
fig, ax = plt.subplots(figsize=(9, 4.8))
b1 = ax.bar(x - w/2, y2024, w, label="2024", color=LBLUE)
b2 = ax.bar(x + w/2, y2025, w, label="2025", color=NAVY)
ax.axhline(0, color="#444", linewidth=0.6)
ax.set_xticks(x); ax.set_xticklabels(segs, fontsize=9)
ax.set_ylabel("Adjusted Earnings + NCI (USD bn)")
ax.set_title("Shell Segment Adjusted Earnings — 2024 vs 2025\n"
             "Integrated Gas remains the largest profit pool")
for bars in (b1, b2):
    for r in bars:
        h = r.get_height()
        off = 0.15 if h >= 0 else -0.35
        ax.text(r.get_x() + r.get_width()/2, h + off,
                f"{h:+.1f}", ha="center", fontsize=8)
ax.legend(loc="upper right")
plt.tight_layout()
plt.savefig(OUT / "shel_segment_adjearn.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────
# 3) LNG volumes — liquefaction & sales (Mtpa) 2023-2025
# Source: 20-F 2025 IG segment KPIs (LNG liquefaction volumes, LNG sales volumes)
# Liquefaction 2024:29 Mtpa, 2025: 28 (decreased — Trinidad restructuring & maintenance)
# Sales 2024:66, 2025:73 (record cargoes, +11% YoY)
lng_years = ["2023", "2024", "2025"]
lng_liq   = [29.0, 29.0, 28.0]     # Mtpa (2023 from 2024 20-F prior; 2024-2025 explicit)
lng_sales = [67.0, 66.0, 73.0]     # Mtpa (2024-2025 from FY25 20-F; 2023 from FY24 20-F)

x = np.arange(len(lng_years))
w = 0.38
fig, ax = plt.subplots(figsize=(8, 4.5))
b1 = ax.bar(x - w/2, lng_liq,   w, label="LNG liquefaction (Mtpa)",
            color=NAVY)
b2 = ax.bar(x + w/2, lng_sales, w, label="LNG sales (Mtpa)",
            color=ORANGE)
for bars in (b1, b2):
    for r in bars:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 0.8, f"{h:.0f}",
                ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(lng_years)
ax.set_ylabel("Million tonnes per annum (Mtpa)")
ax.set_title("Shell LNG Volumes — Liquefaction & Sales (2023–2025)\n"
             "World's largest LNG portfolio operator; 4–5%/yr sales growth target to 2030")
ax.legend(loc="upper left")
ax.set_ylim(0, 90)
plt.tight_layout()
plt.savefig(OUT / "shel_lng_volumes.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────
# 4) Cash returns to shareholders — dividends + buybacks (USD bn) 2023-2025
# Source: 20-F 2025 KPI page ("at a glance"): 2024 buybacks 13.9 / dividends 8.7
# 2025: buybacks 13.9 / dividends 8.5
# 2023: per 20-F 2023 selected data — buybacks 12.6 / dividends 7.7
divs  = [7.7, 8.7, 8.5]
bbks  = [12.6, 13.9, 13.9]
fig, ax = plt.subplots(figsize=(8, 4.5))
b1 = ax.bar(YEARS, divs, color=BLUE,  label="Dividends paid")
b2 = ax.bar(YEARS, bbks, bottom=divs, color=NAVY, label="Share buybacks executed")
totals = [d + b for d, b in zip(divs, bbks)]
for i, t in enumerate(totals):
    ax.text(i, t + 0.5, f"${t:.1f}B", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("USD bn")
ax.set_title("Shell Capital Returns to Shareholders (2023–2025)\n"
             "Target: 40–50% of CFFO returned; 2025 actual = 52%")
ax.set_ylim(0, 27)
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(OUT / "shel_capital_returns.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────
# 5) Supermajor valuation snapshot — TTM P/E and dividend yield
# Approximate values as of May 2026 — see report citations (Yahoo Finance)
# Note: figures vary day-to-day; report cites each individually.
peers = ["SHEL", "XOM", "CVX", "BP", "TTE"]
pe    = [13.5, 14.8, 15.0, 11.0, 9.7]
divy  = [3.9, 3.6, 4.5, 6.0, 5.4]   # %

x = np.arange(len(peers))
w = 0.38
fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
b1 = ax1.bar(x - w/2, pe, w, color=NAVY, label="TTM P/E (x)")
ax1.set_ylabel("TTM P/E (x)", color=NAVY)
ax1.tick_params(axis="y", labelcolor=NAVY)
ax1.set_xticks(x); ax1.set_xticklabels(peers)
for r in b1:
    ax1.text(r.get_x() + r.get_width()/2, r.get_height() + 0.2,
             f"{r.get_height():.1f}x", ha="center", fontsize=9, color=NAVY)
ax2 = ax1.twinx()
b2 = ax2.bar(x + w/2, divy, w, color=ORANGE, label="Dividend yield (%)")
ax2.set_ylabel("Dividend yield (%)", color=ORANGE)
ax2.tick_params(axis="y", labelcolor=ORANGE)
for r in b2:
    ax2.text(r.get_x() + r.get_width()/2, r.get_height() + 0.1,
             f"{r.get_height():.1f}%", ha="center", fontsize=9, color=ORANGE)
ax1.set_title("Supermajor Valuation Snapshot — May 2026\n"
              "P/E and dividend yield (approximate; see report citations)")
ax1.set_ylim(0, 20)
ax2.set_ylim(0, 8)
plt.tight_layout()
plt.savefig(OUT / "shel_peer_valuation.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────
# 6) Oil & gas production by region (Earnings before tax, Subsidiaries)
# Source: 20-F 2025 Supplementary information — oil-and-gas. Earnings before tax for 2025 by region.
# Using "Earnings before taxation" by region as a profitability snapshot
regions = ["North\nAmerica", "South\nAmerica", "Europe", "Asia",
           "Oceania", "Africa", "USA"]
ebt     = [6.331, 8.012, 2.469, 1.187, 1.884, 0.068, 1.259]  # USD bn (2025)
colors  = [NAVY, BLUE, LBLUE, ORANGE, GREEN, RED, "#444444"]
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(regions, ebt, color=colors)
for r in bars:
    ax.text(r.get_x() + r.get_width()/2, r.get_height() + 0.15,
            f"${r.get_height():.1f}B", ha="center", fontsize=9)
ax.set_ylabel("Earnings before taxation (USD bn)")
ax.set_title("Shell Upstream Earnings Before Tax by Region — 2025\n"
             "(Shell subsidiaries; from Supplementary Info, Form 20-F 2025)")
plt.tight_layout()
plt.savefig(OUT / "shel_geographic_ebt.png")
plt.close()

print("OK — wrote 6 PNG charts to", OUT)
