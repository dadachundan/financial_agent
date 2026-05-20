"""SanDisk (SNDK) charts for initiation report.

Sources cited inline in the markdown report. All numbers are from SEC filings:
  - FY2025 10-K (filed 2025-08-21, for fiscal year ended 2025-06-27)
  - Q1 FY26 / Q2 FY26 / Q3 FY26 8-K earnings releases
  - Q2 FY26 10-Q (filed 2026-05-01)
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ---------------------------------------------------------------------------
# 1. FY23–FY25 revenue + gross margin (carve-out predecessor financials)
# ---------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(7.5, 4.2))
years = ["FY2023", "FY2024", "FY2025"]
revenue = [6086, 6663, 7355]            # $M, 10-K MD&A
gm_pct = [7.1, 16.1, 30.1]              # %, 10-K MD&A
bars = ax1.bar(years, revenue, color="#1f4e79", width=0.55, label="Revenue ($M)")
ax1.set_ylabel("Revenue (US$ millions)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 9000)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 100, f"${v:,}M", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(years, gm_pct, color="#c00000", marker="o", linewidth=2.2, label="GAAP Gross margin %")
for i, g in enumerate(gm_pct):
    ax2.text(i, g + 2.5, f"{g:.1f}%", ha="center", color="#c00000", fontsize=9)
ax2.set_ylabel("GAAP gross margin (%)", color="#c00000")
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(0, 60)
ax2.spines["top"].set_visible(False)
ax1.set_title("SanDisk carve-out financials: revenue and gross margin, FY2023–FY2025")
fig.tight_layout()
fig.savefig(OUT / "sndk_revenue_gm_carveout.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 2. FY26 quarterly inflection — revenue + non-GAAP GM by quarter
# ---------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(7.5, 4.2))
qs = ["Q1 FY26\n(Sep '25)", "Q2 FY26\n(Dec '25)", "Q3 FY26\n(Apr '26)", "Q4 FY26E\n(guide mid)"]
rev_q = [2308, 3025, 5950, 8000]        # Q4 = midpoint of $7.75-$8.25B guide
gm_q = [29.9, 51.1, 78.4, 66.0]          # Non-GAAP, Q4 = midpoint of 65.0-67.0%
colors = ["#1f4e79", "#1f4e79", "#1f4e79", "#7f7f7f"]
bars = ax1.bar(qs, rev_q, color=colors, width=0.55)
ax1.set_ylabel("Revenue (US$ millions)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 10000)
for b, v in zip(bars, rev_q):
    ax1.text(b.get_x() + b.get_width() / 2, v + 200, f"${v:,}M", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(qs, gm_q, color="#c00000", marker="o", linewidth=2.2)
for i, g in enumerate(gm_q):
    ax2.text(i, g + 3, f"{g:.1f}%", ha="center", color="#c00000", fontsize=9)
ax2.set_ylabel("Non-GAAP gross margin (%)", color="#c00000")
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(0, 100)
ax2.spines["top"].set_visible(False)
ax1.set_title("Post-spin inflection: SanDisk quarterly revenue and gross margin, FY2026")
fig.tight_layout()
fig.savefig(OUT / "sndk_fy26_inflection.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. FY26 end-market mix evolution (Datacenter / Edge / Consumer)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.2))
qs = ["Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
# Q3 FY25 (mar 2025): Datacenter 197, Edge 927, Consumer 571 (from Q3FY26 release Y/Y compare)
# Q4 FY25 (Jun 2025): Datacenter 213, Edge 1,103, Consumer 585 (from Q1FY26 release Q/Q)
# Q1 FY26 (Sep 2025): Datacenter 269, Edge 1,387, Consumer 652
# Q2 FY26 (Dec 2025): Datacenter 440, Edge 1,678, Consumer 907
# Q3 FY26 (Apr 2026): Datacenter 1,467, Edge 3,663, Consumer 820
dc = [197, 213, 269, 440, 1467]
edge = [927, 1103, 1387, 1678, 3663]
cons = [571, 585, 652, 907, 820]
x = np.arange(len(qs))
ax.bar(x, dc, label="Datacenter (Cloud / eSSD)", color="#1f4e79")
ax.bar(x, edge, bottom=dc, label="Edge (Client)", color="#2e7d32")
ax.bar(x, cons, bottom=[a + b for a, b in zip(dc, edge)], label="Consumer", color="#ed7d31")
ax.set_xticks(x)
ax.set_xticklabels(qs)
ax.set_ylabel("Revenue (US$ millions)")
ax.set_title("End-market revenue mix, Q3 FY25 – Q3 FY26")
ax.legend(loc="upper left", fontsize=9, frameon=False)
totals = [a + b + c for a, b, c in zip(dc, edge, cons)]
for i, t in enumerate(totals):
    ax.text(i, t + 100, f"${t:,}M", ha="center", fontsize=9)
ax.set_ylim(0, 7000)
fig.tight_layout()
fig.savefig(OUT / "sndk_end_market_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. Balance sheet transformation — cash, debt, equity (Jun 27, 2025 vs Apr 3, 2026)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.0))
items = ["Cash & equiv.", "Total debt", "Total stockholders'\nequity"]
fy25 = [1481, 1900, 12985 - 3769]   # equity = total assets - total liabilities
q2fy26 = [3735, 0, 17075 - 3298]
x = np.arange(len(items))
w = 0.35
b1 = ax.bar(x - w / 2, fy25, width=w, color="#7f7f7f", label="June 27, 2025 (FY25 year-end)")
b2 = ax.bar(x + w / 2, q2fy26, width=w, color="#1f4e79", label="April 3, 2026 (Q2 FY26)")
for b, v in zip(b1, fy25):
    ax.text(b.get_x() + b.get_width() / 2, v + 200, f"${v:,}M", ha="center", fontsize=9)
for b, v in zip(b2, q2fy26):
    ax.text(b.get_x() + b.get_width() / 2, v + 200, f"${v:,}M", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(items)
ax.set_ylabel("US$ millions")
ax.set_title("Balance sheet deleveraging: from $1.9 B debt to zero in three quarters")
ax.legend(loc="upper left", fontsize=9, frameon=False)
ax.set_ylim(0, 17000)
fig.tight_layout()
fig.savefig(OUT / "sndk_balance_sheet.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. Geographic mix FY2025 (from 10-K)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.2))
labels = ["Asia", "Americas", "EMEA"]
vals = [4457, 1618, 1280]
colors = ["#1f4e79", "#2e7d32", "#ed7d31"]
wedges, _, _ = ax.pie(
    vals,
    labels=[f"{l}\n${v:,}M ({v/sum(vals)*100:.0f}%)" for l, v in zip(labels, vals)],
    colors=colors,
    autopct="",
    startangle=90,
    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
)
ax.set_title("FY2025 revenue by geography (ship-to)")
fig.tight_layout()
fig.savefig(OUT / "sndk_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 6. Datacenter end-market growth — quarterly $ and YoY %
# ---------------------------------------------------------------------------
# Source: Q3 FY26 earnings release table (Q3 FY26 vs Q3 FY25 Y/Y compares)
# and Q1/Q2 FY26 releases.
fig, ax1 = plt.subplots(figsize=(7.5, 4.0))
qs = ["Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
dc_rev = [197, 213, 269, 440, 1467]
yoy = [None, None, -10.3, 76.0, 644.7]   # Q1 FY26 YoY $269 vs $300 = -10%; Q2 $440 vs $250 = +76%; Q3 $1,467 vs $197 = +644.7%
bars = ax1.bar(qs, dc_rev, color="#1f4e79")
for b, v in zip(bars, dc_rev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 30, f"${v:,}M", ha="center", fontsize=9)
ax1.set_ylabel("Datacenter revenue (US$ M)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 1700)
ax2 = ax1.twinx()
xs = list(range(len(qs)))
yoy_plot = [None, None] + yoy[2:]
ax2.plot(xs, yoy_plot, color="#c00000", marker="o", linewidth=2.2)
for i, y in enumerate(yoy_plot):
    if y is not None:
        ax2.text(i, y + 25, f"{y:+.0f}% YoY", ha="center", color="#c00000", fontsize=9)
ax2.set_ylabel("Datacenter revenue, YoY % change", color="#c00000")
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(-100, 800)
ax2.spines["top"].set_visible(False)
ax1.set_title("Datacenter (eSSD) ramp: from <$200 M / quarter to nearly $1.5 B in five quarters")
fig.tight_layout()
fig.savefig(OUT / "sndk_datacenter_ramp.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("All charts written to", OUT)
