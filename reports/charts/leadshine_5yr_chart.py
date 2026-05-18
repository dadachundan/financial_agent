"""5-year financial trend chart for Leadshine 雷赛智能 (SZSE:002979).

Source: cninfo 年度报告 FY2020 / FY2021 / FY2022 / FY2023 / FY2024 / FY2025
(consolidated, PRC GAAP). Values in RMB.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

years = ["FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]

# Income statement (¥, raw)
revenue = [946_426_258.88, 1_203_158_184.15, 1_337_862_149.54,
           1_415_367_674.51, 1_584_283_297.46, 1_873_838_550.29]
net_income = [175_993_196.22, 218_315_646.85, 220_305_684.99,
              138_568_942.32, 200_464_567.18, 225_372_275.43]
# Approx gross margin (FY24 ~38.4%, FY25 39.0%; earlier from annual disclosures)
gm_pct = [38.5, 39.5, 36.0, 35.5, 38.4, 39.0]
# R&D / revenue %
rd_pct = [11.0, 11.5, 12.0, 12.7, 12.3, 12.63]

# Segment revenue FY24 / FY25 (¥ million)
seg_fy24 = {"Stepper": 605.85, "Servo": 708.74, "Control": 251.79, "Other": 17.91}
seg_fy25 = {"Stepper": 652.58, "Servo": 921.59, "Control": 286.94, "Other": 12.73}

# Styling
plt.rcParams.update({
    "font.family": ["Arial Unicode MS", "DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})
NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
CORAL = "#e76f51"
GOLD = "#f4a261"
GRAY = "#888"

fig, axes = plt.subplots(2, 2, figsize=(15, 9))
fig.suptitle(
    "Leadshine 雷赛智能 (SZSE:002979) — 6-Year Financial Trend (FY2020–FY2025)",
    fontsize=15, fontweight="bold", y=0.995,
)

# --- 1. Revenue & Net Income ---
ax = axes[0, 0]
x = np.arange(len(years))
w = 0.35
rev_m = [v / 1e6 for v in revenue]
ni_m = [v / 1e6 for v in net_income]
b1 = ax.bar(x - w/2, rev_m, w, label="Revenue", color=NAVY)
b2 = ax.bar(x + w/2, ni_m, w, label="Net Income", color=TEAL)
for b in b1:
    ax.text(b.get_x() + b.get_width()/2, b.get_height(),
            f"{b.get_height():.0f}", ha="center", va="bottom", fontsize=8)
for b in b2:
    ax.text(b.get_x() + b.get_width()/2, b.get_height(),
            f"{b.get_height():.0f}", ha="center", va="bottom", fontsize=8)
ax.set_title("Revenue & Net Income (¥ million)", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel("¥ million")
ax.legend(loc="upper left", frameon=False)
yoy = [(revenue[i] / revenue[i-1] - 1) * 100 for i in range(1, len(revenue))]
ax.text(0.98, 0.95,
        f"Rev CAGR FY20–25: {((revenue[-1]/revenue[0])**(1/5)-1)*100:.1f}%\n"
        f"FY25 YoY rev: +{yoy[-1]:.1f}%",
        transform=ax.transAxes, ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=GRAY, alpha=0.85))

# --- 2. Gross margin & R&D intensity ---
ax = axes[0, 1]
ax.plot(years, gm_pct, "o-", color=NAVY, lw=2.5, markersize=8, label="Gross margin")
ax.plot(years, rd_pct, "s--", color=CORAL, lw=2, markersize=8, label="R&D / Revenue")
for i, v in enumerate(gm_pct):
    ax.annotate(f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
for i, v in enumerate(rd_pct):
    ax.annotate(f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9, color=CORAL)
ax.set_title("Gross Margin & R&D Intensity", fontweight="bold")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, 50)
ax.legend(loc="lower left", frameon=False)

# --- 3. Segment revenue mix FY24 vs FY25 ---
ax = axes[1, 0]
labels = list(seg_fy24.keys())
fy24_vals = list(seg_fy24.values())
fy25_vals = list(seg_fy25.values())
x = np.arange(len(labels))
w = 0.38
b1 = ax.bar(x - w/2, fy24_vals, w, label="FY2024", color=GOLD)
b2 = ax.bar(x + w/2, fy25_vals, w, label="FY2025", color=NAVY)
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height(),
                f"{b.get_height():.0f}", ha="center", va="bottom", fontsize=9)
ax.set_title("Segment Revenue Mix (¥ million)", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("¥ million")
ax.legend(loc="upper right", frameon=False)
deltas = [(fy25_vals[i] / fy24_vals[i] - 1) * 100 for i in range(len(labels))]
delta_str = "  |  ".join(f"{labels[i]}: {deltas[i]:+.1f}%" for i in range(len(labels)))
ax.text(0.5, -0.18, "FY25 YoY: " + delta_str, transform=ax.transAxes, ha="center",
        va="top", fontsize=9, color=GRAY)

# --- 4. Peer P/E TTM bars ---
ax = axes[1, 1]
peers = ["Leadshine\n002979", "Inovance\n300124", "Estun\n002747", "Moons'\n603728", "Yaskawa\n6506"]
pe_ttm = [54.4, 36.5, None, 80.0, 22.2]  # Estun negative
labels_disp = ["54.4x", "36.5x", "neg.", "~80x", "22.2x"]
colors = [NAVY, TEAL, GRAY, CORAL, GOLD]
plot_vals = [v if v is not None else 0 for v in pe_ttm]
bars = ax.bar(peers, plot_vals, color=colors)
for b, lbl in zip(bars, labels_disp):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1,
            lbl, ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_title("TTM P/E — Leadshine vs Peers (May 2026)", fontweight="bold")
ax.set_ylabel("TTM P/E (×)")
ax.set_ylim(0, 95)
ax.text(0.98, 0.95,
        "Leadshine = 54x sits above\nInovance/Yaskawa, well below Moons'",
        transform=ax.transAxes, ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=GRAY, alpha=0.85))

plt.tight_layout(rect=[0, 0, 1, 0.96])
out = "/Users/x/projects/financial_agent/reports/charts/leadshine_5yr_chart.png"
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
