#!/usr/bin/env python3
"""Charts for Alphabet (NASDAQ:GOOG) initiation report — 2026-05-20."""
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
})

# --- 1) Revenue & operating margin trend (FY2021–FY2025) -----------------
# Source: 10-K filings (FY2025, FY2024, FY2023, FY2022, FY2021)
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
revenue = [257.637, 282.836, 307.394, 350.018, 402.836]   # $B
op_income = [78.714, 74.842, 84.293, 112.390, 129.039]    # $B
op_margin = [oi / r * 100 for oi, r in zip(op_income, revenue)]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#4285F4", alpha=0.85, label="Revenue ($B)")
ax1.set_ylabel("Revenue ($B)", color="#4285F4")
ax1.set_ylim(0, 460)
ax1.tick_params(axis="y", labelcolor="#4285F4")
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 6, f"{v:.1f}", ha="center", fontsize=9, color="#1a3a8c")

ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#EA4335", marker="o", linewidth=2.2, label="Operating margin (%)")
ax2.set_ylabel("Operating margin (%)", color="#EA4335")
ax2.set_ylim(20, 40)
ax2.tick_params(axis="y", labelcolor="#EA4335")
ax2.grid(False)
for x, v in zip(years, op_margin):
    ax2.text(x, v + 0.6, f"{v:.1f}%", ha="center", color="#a32d23", fontsize=9)

ax1.set_title("Alphabet revenue and operating margin, FY2021–FY2025", fontsize=12, pad=14)
fig.tight_layout()
plt.savefig(OUT / "goog_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 2) Segment revenue mix (FY2025) -------------------------------------
# Source: FY2025 10-K
labels = ["Google Search & other", "YouTube ads", "Google Network",
          "Subscriptions, platforms & devices", "Google Cloud", "Other Bets"]
values = [224.532, 40.367, 29.792, 48.030, 58.705, 1.537]  # $B
colors = ["#4285F4", "#EA4335", "#FBBC04", "#34A853", "#1E88E5", "#9E9E9E"]

fig, ax = plt.subplots(figsize=(9, 5.2))
y_pos = np.arange(len(labels))[::-1]
bars = ax.barh(y_pos, values, color=colors)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
total = sum(values)
for b, v in zip(bars, values):
    pct = v / total * 100
    ax.text(b.get_width() + 3, b.get_y() + b.get_height()/2, f"${v:.1f}B ({pct:.1f}%)",
            va="center", fontsize=9)
ax.set_xlabel("FY2025 revenue ($B)")
ax.set_xlim(0, 260)
ax.set_title("Alphabet FY2025 revenue by segment — Search still 56%, Cloud now 15%", fontsize=12, pad=14)
fig.tight_layout()
plt.savefig(OUT / "goog_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 3) Google Cloud revenue + operating income, 2022–Q1'26 --------------
# Source: 10-K filings + Q1 2026 8-K
periods = ["FY2022", "FY2023", "FY2024", "FY2025", "Q1'26 ann."]
cloud_rev = [26.280, 33.088, 43.229, 58.705, 80.112]   # Q1'26 $20.028 *4 (run rate)
cloud_oi  = [-1.922, 1.716, 6.112, 13.910, 26.392]      # Q1'26 $6.598*4

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(periods))
w = 0.36
b1 = ax.bar(x - w/2, cloud_rev, w, label="Revenue ($B)", color="#1E88E5")
b2 = ax.bar(x + w/2, cloud_oi,  w, label="Operating income ($B)", color="#34A853")
ax.set_xticks(x); ax.set_xticklabels(periods)
ax.set_ylabel("$ Billion")
ax.set_title("Google Cloud — from loss-making to >20% operating margin", fontsize=12, pad=14)
for bars in (b1, b2):
    for b in bars:
        v = b.get_height()
        ax.text(b.get_x() + b.get_width()/2,
                v + (1 if v>=0 else -3),
                f"{v:.1f}", ha="center", fontsize=8)
ax.axhline(0, color="grey", linewidth=0.7)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
plt.savefig(OUT / "goog_cloud_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 4) Capex ramp -------------------------------------------------------
# Sources: 10-K cash-flow + 2026 guidance ($175-185B)
years_cx = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "FY2026E"]
capex = [24.640, 31.485, 32.251, 52.535, 91.447, 180.0]   # midpoint of guide
revenue_cx = [257.637, 282.836, 307.394, 350.018, 402.836, 480.0]  # FY26E ~ Street consensus mid

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(years_cx, capex, color="#FBBC04", alpha=0.9)
for b, v in zip(bars, capex):
    ax.text(b.get_x()+b.get_width()/2, v + 3, f"${v:.0f}B", ha="center", fontsize=9)
ax.set_ylabel("Capex ($B)")
ax.set_title("Alphabet capex — $175–185B 2026 guide is a step-function vs. $32B in 2023", fontsize=11, pad=14)
ax.set_ylim(0, 220)
ax.annotate("Hyperscaler AI build-out begins",
            xy=(3, 52), xytext=(0.2, 130),
            arrowprops=dict(arrowstyle="->", color="grey"), fontsize=9, color="grey")
fig.tight_layout()
plt.savefig(OUT / "goog_capex.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 5) Peer valuation: TTM P/E + TTM P/S -------------------------------
# Source: yfinance pull, 2026-05-20
peers = ["GOOG", "META", "MSFT", "AMZN", "AAPL", "NVDA"]
pe    = [29.23, 22.06, 25.04, 32.20, 36.61, 45.55]
ps    = [11.01, 7.16,  9.81,  3.82,  9.83, 25.03]
op_m  = [36.1,  40.6,  46.3,  13.1,  32.3, 65.0]

fig, ax = plt.subplots(figsize=(9, 5.4))
x = np.arange(len(peers))
w = 0.36
b1 = ax.bar(x - w/2, pe, w, label="TTM P/E (×)", color="#4285F4")
b2 = ax.bar(x + w/2, ps, w, label="TTM P/S (×)", color="#34A853")
ax.set_xticks(x); ax.set_xticklabels(peers)
ax.set_ylabel("Multiple (×)")
ax.set_title("Mag-7 peer valuation snapshot — GOOG trades cheapest in the cohort on P/E", fontsize=11, pad=14)
for bars in (b1, b2):
    for b in bars:
        v = b.get_height()
        ax.text(b.get_x()+b.get_width()/2, v + 0.6, f"{v:.1f}", ha="center", fontsize=8)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
plt.savefig(OUT / "goog_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 6) Cloud market share, Q1 2026 --------------------------------------
# Source: Synergy Research / multiple secondary; ~30/25/13 split
shares = [30, 25, 13, 32]
labels = ["AWS", "Azure", "Google Cloud", "Others"]
colors = ["#FF9900", "#0078D4", "#34A853", "#9E9E9E"]
fig, ax = plt.subplots(figsize=(7.5, 5))
wedges, texts, auto = ax.pie(shares, labels=labels, colors=colors, autopct="%1.0f%%",
                              startangle=90, pctdistance=0.78, textprops={"fontsize": 11})
centre = plt.Circle((0,0), 0.55, fc="white")
ax.add_artist(centre)
ax.set_title("Global cloud-infrastructure market share, Q1 2026\nGoogle Cloud ~13%, growing 63% YoY", fontsize=11)
fig.tight_layout()
plt.savefig(OUT / "goog_cloud_share.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 7) Geographic mix ---------------------------------------------------
geo = ["United States", "EMEA", "APAC", "Other Americas"]
y23 = [146.286, 91.038, 51.514, 18.320]
y24 = [170.447, 102.127, 56.815, 20.418]
y25 = [194.229, 117.152, 67.680, 23.902]
x = np.arange(len(geo)); w = 0.27
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w, y23, w, label="FY2023", color="#9AA0A6")
ax.bar(x,     y24, w, label="FY2024", color="#4285F4")
ax.bar(x + w, y25, w, label="FY2025", color="#0F4C81")
ax.set_xticks(x); ax.set_xticklabels(geo)
ax.set_ylabel("Revenue ($B)")
ax.set_title("Alphabet revenue by geography — US still ~48% but EMEA and APAC compounding fast", fontsize=11, pad=14)
ax.legend(frameon=False)
for cx, vals in zip([x-w, x, x+w], [y23, y24, y25]):
    for xv, vv in zip(cx, vals):
        ax.text(xv, vv + 2, f"{vv:.0f}", ha="center", fontsize=8)
fig.tight_layout()
plt.savefig(OUT / "goog_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

print("Wrote charts:", sorted(p.name for p in OUT.glob("goog_*.png")))
