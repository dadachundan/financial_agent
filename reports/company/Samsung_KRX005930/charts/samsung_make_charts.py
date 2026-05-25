"""Charts for Samsung Electronics company-research report (2026-05-20).

All figures sourced from Samsung IR press releases (cited inline in the
markdown report). Outputs land in /Users/x/projects/financial_agent/reports/charts/.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# ----------------------------------------------------------------------------
# Chart 1 — Group revenue + operating margin trend (FY2021–Q1 2026 annualized)
# ----------------------------------------------------------------------------
# Sources (cited in report): Samsung FY press releases. Q1 2026 annualised = Q1 x 4
# (illustrative, labeled "Q1'26 ann." not full-year forecast).
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "Q1'26 ann."]
revenue = [279.6, 302.2, 258.9, 300.9, 333.6, 535.6]   # KRW trillion
op_profit = [51.6, 43.4, 6.6, 32.7, 43.6, 228.0]       # KRW trillion (Q1 op profit 57 x 4)
op_margin = [p / r * 100 for p, r in zip(op_profit, revenue)]

fig, ax1 = plt.subplots(figsize=(9, 4.8))
bars = ax1.bar(years, revenue, color="#1f4e79", alpha=0.85, label="Revenue (KRW trn)")
ax1.set_ylabel("Revenue (KRW trillion)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 600)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 8, f"{v:.0f}", ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#c00000", marker="o", linewidth=2.2, label="Op. margin (%)")
ax2.set_ylabel("Operating margin (%)", color="#c00000")
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(0, 50)
for x, m in zip(years, op_margin):
    ax2.text(x, m + 1.5, f"{m:.1f}%", ha="center", fontsize=9, color="#c00000")

ax1.set_title("Samsung Electronics — Revenue & Operating Margin, FY2021–Q1'26 ann.", fontsize=12)
ax2.spines["top"].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "samsung_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ----------------------------------------------------------------------------
# Chart 2 — FY2025 revenue by division (stacked structure)
# ----------------------------------------------------------------------------
# Samsung FY2025 press release: DS ~ KRW 116-120T including memory recovery in 2H,
# DX (MX + VD/DA + Networks) ~ KRW 175T, SDC ~ KRW 35T, Harman ~ KRW 15.78T.
# These are inter-segment-gross; consolidated total is KRW 333.6T (eliminations).
divisions = ["DS (Memory/Foundry/LSI)", "DX (MX+VD/DA+Net)", "Samsung Display", "Harman", "Eliminations / Other"]
revenue_share = [120.0, 175.0, 35.0, 15.8, -12.2]  # KRW trillion gross-of-elim
colors = ["#1f4e79", "#2e75b6", "#9dc3e6", "#ffc000", "#a6a6a6"]

fig, ax = plt.subplots(figsize=(9, 4.6))
ypos = np.arange(len(divisions))
bars = ax.barh(ypos, revenue_share, color=colors)
ax.set_yticks(ypos)
ax.set_yticklabels(divisions)
ax.invert_yaxis()
ax.set_xlabel("FY2025 revenue (KRW trillion, segment gross)")
ax.set_title("Samsung Electronics — FY2025 Revenue by Division", fontsize=12)
for b, v in zip(bars, revenue_share):
    ax.text(v + (3 if v > 0 else -3), b.get_y() + b.get_height() / 2,
            f"{v:.1f}", va="center",
            ha="left" if v > 0 else "right", fontsize=10)
ax.axvline(0, color="black", linewidth=0.6)
fig.tight_layout()
fig.savefig(OUT / "samsung_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ----------------------------------------------------------------------------
# Chart 3 — HBM market share (2024–2026E)
# ----------------------------------------------------------------------------
# Sources cited in report: TrendForce, Counterpoint Research, Astute Group.
labels = ["2024", "Q2'25", "Q3'25", "2026E"]
sk_hynix = [52, 62, 57, 50]
samsung  = [42, 17, 22, 32]
micron   = [6,  21, 21, 18]

x = np.arange(len(labels))
width = 0.27
fig, ax = plt.subplots(figsize=(9, 4.6))
b1 = ax.bar(x - width, sk_hynix, width, label="SK Hynix", color="#c00000")
b2 = ax.bar(x,         samsung,  width, label="Samsung",  color="#1f4e79")
b3 = ax.bar(x + width, micron,   width, label="Micron",   color="#70ad47")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("HBM market share (%)")
ax.set_title("HBM Market Share — Samsung vs. SK Hynix vs. Micron", fontsize=12)
ax.set_ylim(0, 70)
ax.legend(loc="upper right")
for bars in (b1, b2, b3):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
                f"{int(b.get_height())}%", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "samsung_hbm_share.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ----------------------------------------------------------------------------
# Chart 4 — Foundry market share, TSMC vs. Samsung (Q1'24 – Q3'25)
# ----------------------------------------------------------------------------
# Source: TrendForce, BigGo Finance (cited in report).
quarters = ["Q1'24", "Q3'24", "Q1'25", "Q3'25"]
tsmc = [62.8, 64.9, 67.6, 70.4]
samsung_f = [10.5, 9.3, 7.7, 7.1]

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(quarters, tsmc, marker="o", linewidth=2.4, color="#c00000", label="TSMC")
ax.plot(quarters, samsung_f, marker="s", linewidth=2.4, color="#1f4e79", label="Samsung Foundry")
ax.fill_between(quarters, tsmc, samsung_f, color="#c00000", alpha=0.07)
for x, y in zip(quarters, tsmc):
    ax.text(x, y + 1.3, f"{y:.1f}%", ha="center", fontsize=9, color="#c00000")
for x, y in zip(quarters, samsung_f):
    ax.text(x, y - 2.5, f"{y:.1f}%", ha="center", fontsize=9, color="#1f4e79")
ax.set_ylabel("Foundry market share (%)")
ax.set_title("Foundry Market Share — TSMC vs. Samsung (Q1'24–Q3'25)", fontsize=12)
ax.set_ylim(0, 80)
ax.legend(loc="center left")
fig.tight_layout()
fig.savefig(OUT / "samsung_foundry_share.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ----------------------------------------------------------------------------
# Chart 5 — Peer P/E comparison
# ----------------------------------------------------------------------------
# Sources cited in report: Seoul Economic Daily, Nomura, finbox.
peers = ["Samsung 005930", "SK Hynix 000660", "Micron MU", "TSMC TSM", "Intel INTC"]
pe = [6.77, 6.79, 8.0, 20.0, 35.0]
colors_pe = ["#1f4e79", "#c00000", "#70ad47", "#ffc000", "#7030a0"]

fig, ax = plt.subplots(figsize=(9, 4.6))
bars = ax.bar(peers, pe, color=colors_pe)
for b, v in zip(bars, pe):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}x", ha="center", fontsize=10)
ax.set_ylabel("Forward P/E (x)")
ax.set_title("Forward P/E (2026E) — Memory & Foundry Peers", fontsize=12)
ax.set_ylim(0, 42)
fig.tight_layout()
fig.savefig(OUT / "samsung_peer_pe.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ----------------------------------------------------------------------------
# Chart 6 — Samsung capex history
# ----------------------------------------------------------------------------
# Source: Samsung Q4 press releases (cited in report).
capex_years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "FY2026E"]
capex_total = [48.2, 53.1, 53.1, 53.6, 52.7, 110.0]   # KRW trillion
capex_ds    = [43.6, 47.9, 48.4, 46.3, 47.5, 100.0]   # of which DS

fig, ax = plt.subplots(figsize=(9, 4.6))
x = np.arange(len(capex_years))
width = 0.4
b1 = ax.bar(x - width / 2, capex_total, width, color="#9dc3e6", label="Total capex")
b2 = ax.bar(x + width / 2, capex_ds, width, color="#1f4e79", label="DS (semiconductor) capex")
ax.set_xticks(x)
ax.set_xticklabels(capex_years)
ax.set_ylabel("Capex (KRW trillion)")
ax.set_title("Samsung Electronics — Annual Capex, with DS Share", fontsize=12)
ax.legend(loc="upper left")
for b, v in zip(b1, capex_total):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.0f}", ha="center", fontsize=9, color="#1f4e79")
for b, v in zip(b2, capex_ds):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.0f}", ha="center", fontsize=9, color="#1f4e79")
ax.set_ylim(0, 130)
fig.tight_layout()
fig.savefig(OUT / "samsung_capex.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("Saved 6 charts to", OUT)
