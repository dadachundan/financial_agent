#!/usr/bin/env python3
"""Generate charts for Caterpillar (NYSE:CAT) initiation report."""
import os
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))


# ---- Chart 1: Revenue + Operating Margin trend (FY2021-FY2025) ----
years = ["2021", "2022", "2023", "2024", "2025"]
# Source: 10-K FY2025 (and historical 10-Ks); 2021 = 50.971B reported
revenue = [50.971, 59.427, 67.060, 64.809, 67.589]  # USD billion
op_income = [4.434, 8.829, 12.966, 13.072, 11.151]  # USD billion
op_margin = [oi / rv * 100 for oi, rv in zip(op_income, revenue)]

fig, ax1 = plt.subplots(figsize=(8.8, 4.8))
bars = ax1.bar(years, revenue, color="#FECC00", edgecolor="#222", label="Sales & revenues (USD B)")
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.8, f"${v:.1f}B", ha="center", fontsize=9, fontweight="bold")
ax1.set_ylabel("Sales & revenues (USD bn)")
ax1.set_ylim(0, 80)
ax1.set_title("Caterpillar — Revenue and operating margin, FY2021–FY2025", fontsize=12, fontweight="bold")
ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#222", marker="o", linewidth=2, label="Operating margin (%)")
for x, y in zip(years, op_margin):
    ax2.text(x, y + 0.6, f"{y:.1f}%", ha="center", fontsize=9, color="#222")
ax2.set_ylabel("Operating margin (%)")
ax2.set_ylim(0, 25)
fig.tight_layout()
plt.savefig(os.path.join(OUT, "cat_revenue_margin.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 2: Segment revenue mix FY2024 vs FY2025 (stacked bar) ----
# Source: 10-K FY2025 MD&A
segs = ["Construction Industries", "Resource Industries", "Power & Energy", "Financial Products + Other"]
fy24 = [25.455, 12.471, 28.854, 64.809 - 25.455 - 12.471 - 28.854]
fy25 = [25.060, 12.474, 32.201, 67.589 - 25.060 - 12.474 - 32.201]

fig, ax = plt.subplots(figsize=(8.8, 4.5))
colors = ["#FECC00", "#222222", "#E03A3E", "#666666"]
bottom24 = 0
bottom25 = 0
labels_used = set()
for s, v24, v25, c in zip(segs, fy24, fy25, colors):
    ax.bar(["FY2024", "FY2025"], [v24, v25], bottom=[bottom24, bottom25], color=c, label=s, edgecolor="white")
    ax.text(0, bottom24 + v24 / 2, f"${v24:.1f}B", ha="center", va="center", color="black" if c == "#FECC00" else "white", fontsize=9, fontweight="bold")
    ax.text(1, bottom25 + v25 / 2, f"${v25:.1f}B", ha="center", va="center", color="black" if c == "#FECC00" else "white", fontsize=9, fontweight="bold")
    bottom24 += v24
    bottom25 += v25
ax.set_ylabel("USD bn")
ax.set_title("Segment revenue mix — FY2024 vs FY2025", fontsize=12, fontweight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cat_segment_mix.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 3: Segment operating profit FY2024 vs FY2025 ----
segs = ["Construction\nIndustries", "Resource\nIndustries", "Power &\nEnergy", "Financial\nProducts"]
profit_24 = [6.165, 2.538, 5.736, 0.605]
profit_25 = [4.675, 1.988, 6.418, 0.864]

x = np.arange(len(segs))
w = 0.38
fig, ax = plt.subplots(figsize=(8.8, 4.5))
b1 = ax.bar(x - w / 2, profit_24, w, label="FY2024", color="#666666")
b2 = ax.bar(x + w / 2, profit_25, w, label="FY2025", color="#FECC00", edgecolor="#222")
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.08, f"${b.get_height():.2f}B", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(segs)
ax.set_ylabel("Segment operating profit (USD bn)")
ax.set_title("Segment profit — Power & Energy is the swing factor", fontsize=12, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cat_segment_profit.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 4: FCF and capital return ----
years = ["2022", "2023", "2024", "2025"]
ocf = [7.766, 12.885, 12.035, 11.739]  # operating cash flow
capex = [2.599, 3.092, 3.215, 4.286]  # capex (yfinance reports)
fcf = [o - c for o, c in zip(ocf, capex)]
divs = [2.4, 2.494, 2.629, 2.749]  # dividends paid (FY2025 = 2.749B per 10-K)
buybacks = [4.231, 6.690, 8.046, 5.190]  # share repurchases (FY2025 = 5.190B per 10-K)

x = np.arange(len(years))
w = 0.27
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.bar(x - w, ocf, w, label="Operating cash flow", color="#FECC00", edgecolor="#222")
ax.bar(x, fcf, w, label="Free cash flow", color="#E03A3E")
ax.bar(x + w, [d + b for d, b in zip(divs, buybacks)], w, label="Dividends + buybacks", color="#222")
for i, (o, f, t) in enumerate(zip(ocf, fcf, [d + b for d, b in zip(divs, buybacks)])):
    ax.text(i - w, o + 0.15, f"${o:.1f}B", ha="center", fontsize=8)
    ax.text(i, f + 0.15, f"${f:.1f}B", ha="center", fontsize=8)
    ax.text(i + w, t + 0.15, f"${t:.1f}B", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("USD bn")
ax.set_title("Cash generation & capital return — FY2022–FY2025", fontsize=12, fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cat_fcf_capital_return.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 5: Backlog ----
yrs = ["FY2023", "FY2024", "FY2025"]
backlog = [27.5, 30.0, 51.2]  # USD bn — FY2023 from 2023 10-K; FY2024 & 2025 from current 10-K
fig, ax = plt.subplots(figsize=(7.8, 4.2))
bars = ax.bar(yrs, backlog, color=["#666666", "#666666", "#FECC00"], edgecolor="#222")
for b, v in zip(bars, backlog):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"${v:.1f}B", ha="center", fontweight="bold")
ax.set_ylim(0, 60)
ax.set_ylabel("Year-end firm backlog (USD bn)")
ax.set_title("Firm backlog — Power & Energy step-change to $51B", fontsize=12, fontweight="bold")
ax.text(2, 45, "+70% YoY\n(Power & Energy\n=largest driver)", ha="center", fontsize=9, color="#E03A3E", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cat_backlog.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 6: Peer valuation comparison (TTM P/E, P/S, EV/EBITDA) ----
peers = ["CAT", "DE", "CMI", "PCAR", "OSK"]
pe = [43.7, 31.8, 34.7, 23.8, 14.0]
ps = [5.70, 3.27, 2.72, 2.12, 0.75]
ev_ebitda = [29.9, 22.2, 19.4, 19.9, 7.6]

x = np.arange(len(peers))
fig, ax1 = plt.subplots(figsize=(9.5, 4.6))
w = 0.27
ax1.bar(x - w, pe, w, label="P/E (TTM)", color="#FECC00", edgecolor="#222")
ax1.bar(x, ev_ebitda, w, label="EV/EBITDA", color="#E03A3E")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
ax1.set_ylabel("Multiple (x)")
ax1.set_title("Peer valuation — CAT trades at a premium across multiples", fontsize=12, fontweight="bold")
ax2 = ax1.twinx()
ax2.plot(x, ps, color="#222", marker="o", linewidth=2, label="P/S (TTM)")
ax2.set_ylabel("P/S (x)")
for i, (p, e, s) in enumerate(zip(pe, ev_ebitda, ps)):
    ax1.text(i - w, p + 0.5, f"{p:.1f}", ha="center", fontsize=8)
    ax1.text(i, e + 0.5, f"{e:.1f}", ha="center", fontsize=8)
    ax2.text(i, s + 0.15, f"{s:.1f}", ha="center", fontsize=8, color="#222")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "cat_peer_valuation.png"), dpi=150, bbox_inches="tight")
plt.close()

print("Charts saved:", os.listdir(OUT))
