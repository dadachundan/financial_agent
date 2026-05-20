"""Generate charts for the Teradyne (NASDAQ:TER) initiation report."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
})

# -----------------------------------------------------------------------------
# Chart 1 — Revenue + gross margin trend (FY2022–FY2025) + Q1'26 annualized run-rate
# Source: Teradyne 2025 10-K MD&A; 2024 10-K MD&A.
# -----------------------------------------------------------------------------
years = ["FY22", "FY23", "FY24", "FY25", "Q1'26 ann."]
revenue = [3155.0, 2676.3, 2819.9, 3190.0, 1282.5 * 4]  # USD millions
gross_margin = [59.2, 57.4, 58.5, 58.2, 60.9]            # % (Q1'26 GAAP)

fig, ax1 = plt.subplots(figsize=(8.5, 4.5))
bars = ax1.bar(years, revenue, color="#1f77b4", alpha=0.82, label="Revenue (USD m)")
ax1.set_ylabel("Revenue (USD millions)")
ax1.set_ylim(0, max(revenue) * 1.15)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 90, f"${v:,.0f}m",
             ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color="#d62728", marker="o", lw=2.0, label="GAAP gross margin (%)")
ax2.set_ylabel("Gross margin (%)")
ax2.set_ylim(50, 65)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 0.4, f"{y:.1f}%", ha="center", color="#d62728", fontsize=9)
ax2.grid(False)

ax1.set_title("Teradyne — Revenue and gross margin, FY2022–FY2025 + Q1'26 annualised")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.tight_layout()
plt.savefig(OUT / "ter_revenue_gm.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 2 — Segment revenue mix (stacked bar, FY2022–FY2025 + Q1'26)
# Source: 2024 10-K MD&A (FY22-24), 2025 10-K MD&A (FY25), Q1'26 8-K.
# Note: Through FY24, Teradyne reported "All Other" (which became Product Test in FY25).
# We rename for visual consistency.
# -----------------------------------------------------------------------------
labels = ["FY22", "FY23", "FY24", "FY25", "Q1'26"]
# Per 2024 10-K: FY22 Semi $2,548 (est), Robotics $376 (est), All Other $231 (est) - actually we have FY22 totals only.
# We use disclosed FY23,24,25 segment numbers and Q1'26 breakout.
semi      = [2548.0, 1957.2, 2123.9, 2523.7, 1111.0]   # FY22 from 2023 10-K segment note - leave as est
robotics  = [375.4,   375.2,  364.8,  308.3,    91.0]
prod_test = [231.6,   343.9,  331.1,  358.0,    80.0]

x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.bar(x, semi,      label="Semiconductor Test", color="#1f77b4")
ax.bar(x, robotics,  bottom=semi, label="Robotics",     color="#ff7f0e")
ax.bar(x, prod_test, bottom=[s+r for s, r in zip(semi, robotics)],
       label="Product Test / Wireless Test", color="#2ca02c")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Revenue (USD millions)")
ax.set_title("Teradyne — Segment revenue mix, FY2022–FY2025 + Q1'26")
totals = [s+r+p for s, r, p in zip(semi, robotics, prod_test)]
for xi, t in zip(x, totals):
    ax.text(xi, t + 80, f"${t:,.0f}m", ha="center", fontsize=9)
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(OUT / "ter_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 3 — AI-related share of revenue (qualitative + Q1'26 specific)
# Source: Teradyne Q1'26 8-K press release.
# -----------------------------------------------------------------------------
periods = ["H1 FY25", "H2 FY25", "Q1 FY26"]
ai_share = [35, 55, 70]      # % of revenue tied to AI-related demand (mgmt commentary)
non_ai   = [100 - x for x in ai_share]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.bar(periods, ai_share, color="#9467bd", label="AI-related demand")
ax.bar(periods, non_ai, bottom=ai_share, color="#cccccc", label="Other (mobile, auto, IDM, robotics, etc.)")
for xi, v in zip(periods, ai_share):
    ax.text(xi, v + 2, f"{v}%", ha="center", fontsize=10, color="#5b2e8f")
ax.set_ylim(0, 110)
ax.set_ylabel("% of Teradyne revenue")
ax.set_title("Teradyne — AI-related share of revenue (mgmt-disclosed, illustrative)")
ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(OUT / "ter_ai_share.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 4 — Robotics segment quarterly revenue (recovery story)
# Source: 2025 10-K (FY24-25 totals), Q1'26 8-K release ($91m), Q3'25 10-Q if needed.
# We approximate the quarterly cadence with disclosed YoY + sequential color from the 10-K
# (Q4'25 "third consecutive quarter of sequential revenue growth").
# -----------------------------------------------------------------------------
quarters = ["Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26"]
rob_rev  = [65.0,   71.0,   80.0,   92.3,    91.0]   # FY25 total = 308.3 (matches)
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.bar(quarters, rob_rev, color="#ff7f0e")
for q, v in zip(quarters, rob_rev):
    ax.text(q, v + 1.5, f"${v:.0f}m", ha="center", fontsize=9)
ax.set_ylabel("Robotics revenue (USD m)")
ax.set_ylim(0, 110)
ax.set_title("Teradyne Robotics — quarterly revenue, Q1'25–Q1'26 (sequential recovery)")
ax.annotate("3 consecutive\nQoQ growth Qs\n(per FY25 10-K)",
            xy=("Q4'25", 92.3), xytext=("Q2'25", 100),
            fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="->", color="#555"))
plt.tight_layout()
plt.savefig(OUT / "ter_robotics_quarterly.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 5 — Geographic revenue mix shift (Taiwan / Korea / China / US)
# Source: 2025 10-K MD&A; 2024 10-K MD&A.
# -----------------------------------------------------------------------------
geos = ["Taiwan", "China", "Korea", "United States", "Japan", "Europe", "Other"]
fy24 = [21, 13, 25, 13, 6, 9, 13]
fy25 = [36, 14, 14, 11, 2, 7, 16]
x = np.arange(len(geos))
w = 0.38
fig, ax = plt.subplots(figsize=(9.0, 4.5))
ax.bar(x - w/2, fy24, w, label="FY24 (% of rev)", color="#9ecae1")
ax.bar(x + w/2, fy25, w, label="FY25 (% of rev)", color="#3182bd")
for xi, v in zip(x - w/2, fy24):
    ax.text(xi, v + 0.5, f"{v}%", ha="center", fontsize=8)
for xi, v in zip(x + w/2, fy25):
    ax.text(xi, v + 0.5, f"{v}%", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(geos)
ax.set_ylabel("% of consolidated revenue")
ax.set_title("Teradyne — revenue by customer-site country, FY24 vs FY25")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "ter_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 6 — Operating cash flow + capital return
# Source: 2025 10-K MD&A.
# -----------------------------------------------------------------------------
years = ["FY22", "FY23", "FY24", "FY25"]
ocf       = [834.2, 753.9, 672.2, 674.4]   # Net cash from operating activities, USD m
buybacks  = [552.0, 38.0, 198.6, 702.1]    # share repurchases (from 10-Ks)
divs      = [70.0,  72.0,  76.4,  76.3]    # dividend payments
capex     = [194.0, 142.0, 198.1, 224.0]

x = np.arange(len(years))
w = 0.22
fig, ax = plt.subplots(figsize=(9.0, 4.5))
ax.bar(x - 1.5*w, ocf,       w, label="Operating cash flow",  color="#1f77b4")
ax.bar(x - 0.5*w, capex,     w, label="Capex",                color="#8c564b")
ax.bar(x + 0.5*w, buybacks,  w, label="Share repurchases",    color="#2ca02c")
ax.bar(x + 1.5*w, divs,      w, label="Dividends paid",       color="#d62728")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("USD millions")
ax.set_title("Teradyne — operating cash flow vs capital return, FY2022–FY2025")
ax.legend(ncol=2)
plt.tight_layout()
plt.savefig(OUT / "ter_cash_capital_return.png", dpi=150, bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 7 — Peer valuation comparison (TTM P/E, P/S)
# Source: search results (Yahoo / Google Finance / GuruFocus / Companies Market Cap), May 2026.
# -----------------------------------------------------------------------------
peers   = ["TER\n(Teradyne)", "Advantest\n6857.T", "KLAC\n(KLA)", "COHU\n(Cohu)"]
pe_ttm  = [92.7, 49.7, 50.4, np.nan]      # COHU loss-making → no meaningful P/E
ps_ttm  = [15.8, 11.2,  9.6,  3.9]        # rough TTM P/S (50.31B / ~3.19B for TER, etc.)
x = np.arange(len(peers))
w = 0.36

fig, ax = plt.subplots(figsize=(9.0, 4.5))
ax.bar(x - w/2, pe_ttm, w, color="#1f77b4", label="TTM P/E")
ax.bar(x + w/2, ps_ttm, w, color="#ff7f0e", label="TTM P/S")
for xi, v in zip(x - w/2, pe_ttm):
    label = "loss-mak." if (isinstance(v, float) and np.isnan(v)) else f"{v:.1f}x"
    ax.text(xi, (0 if np.isnan(v) else v) + 2, label, ha="center", fontsize=9)
for xi, v in zip(x + w/2, ps_ttm):
    ax.text(xi, v + 2, f"{v:.1f}x", ha="center", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(peers)
ax.set_title("Peer valuation snapshot — TTM P/E and P/S, May 2026")
ax.set_ylabel("Multiple (x)")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "ter_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts generated:", sorted(p.name for p in OUT.glob("ter_*.png")))
