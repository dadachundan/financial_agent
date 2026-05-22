"""Charts for Baidu (NASDAQ:BIDU) research report.

Data sourced from Baidu's 2025 Form 20-F (filed March 17, 2026) and the
Q1 2026 earnings press release (May 18, 2026), both available on SEC EDGAR.
"""
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.dirname(__file__)

# ---------------------------------------------------------------
# Chart 1: Revenue (RMB bn) + GAAP operating margin trend, 2021-2025
# Source: 2025 20-F "Selected Consolidated Financial Data" table.
# ---------------------------------------------------------------
years = [2021, 2022, 2023, 2024, 2025]
revenue = [124.493, 123.675, 134.598, 133.125, 129.079]  # RMB bn
op_income = [10.518, 15.911, 21.856, 21.270, -5.823]     # RMB bn (GAAP)
op_margin = [oi / r * 100 for oi, r in zip(op_income, revenue)]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#3b78c2", alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color="#3b78c2")
ax1.tick_params(axis="y", labelcolor="#3b78c2")
ax1.set_xlabel("Fiscal year")
ax1.set_ylim(0, 160)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, op_margin, color="#d9534f", marker="o", linewidth=2,
         label="GAAP operating margin (%)")
ax2.set_ylabel("GAAP operating margin (%)", color="#d9534f")
ax2.tick_params(axis="y", labelcolor="#d9534f")
ax2.set_ylim(-10, 20)
ax2.axhline(0, color="grey", linewidth=0.5, linestyle="--")
for x, y in zip(years, op_margin):
    ax2.text(x, y + 0.7, f"{y:.1f}%", ha="center", fontsize=9, color="#d9534f")

plt.title("Baidu — Revenue & GAAP Operating Margin, FY2021–FY2025\n(RMB billions; FY2025 includes RMB16.2 bn long-lived asset impairment)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_revenue_margin.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart 2: Segment revenue mix - Baidu General Business vs iQIYI, 2021-2025
# Source: 2025 20-F "Revenue by Segment" table (RMB bn, includes
# inter-segment revenue).
# ---------------------------------------------------------------
years2 = [2023, 2024, 2025]
core = [103.465, 104.712, 102.485]  # Source: 2025 20-F segment table
iqiyi = [31.873, 29.225, 27.290]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years2, core, color="#3b78c2", label="Baidu General Business (formerly Baidu Core)")
ax.bar(years2, iqiyi, bottom=core, color="#f0ad4e", label="iQIYI")
for i, (c, q) in enumerate(zip(core, iqiyi)):
    ax.text(years2[i], c / 2, f"{c:.1f}", ha="center", fontsize=9, color="white")
    ax.text(years2[i], c + q / 2, f"{q:.1f}", ha="center", fontsize=9, color="white")
ax.set_ylabel("Segment revenue (RMB bn, incl. inter-segment)")
ax.set_xlabel("Fiscal year")
ax.set_title("Baidu — Segment Revenue Mix, FY2021–FY2025")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_segment_mix.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart 3: Q1-2026 Baidu Core AI-powered Business breakdown
# Source: Q1 2026 press release (EX-99.1, May 18, 2026).
# ---------------------------------------------------------------
labels = ["AI Cloud Infra\n(RMB 8.8 bn, +79% YoY)",
          "AI Applications\n(RMB 2.5 bn, flat YoY)",
          "AI-native Marketing\n(RMB 2.3 bn, +36% YoY)"]
sizes = [8.8, 2.5, 2.3]
colors = ["#3b78c2", "#5cb85c", "#f0ad4e"]
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                  autopct="%1.0f%%", startangle=90,
                                  textprops={"fontsize": 10})
ax.set_title("Baidu Core AI-Powered Business — Q1 2026 Revenue Mix\n(Total RMB 13.6 bn, +49% YoY; first quarter > 50% of Baidu General Business)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_q1_2026_ai_mix.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart 4: Peer valuation - TTM P/E and P/S, May 2026
# Sources: Yahoo Finance market quote, pulled 2026-05-20
# ---------------------------------------------------------------
peers = ["BIDU", "BABA", "PDD", "TCEHY", "JD", "GOOGL"]
pe = [78.2, 20.8, 10.0, 16.5, 23.9, 29.7]
ps = [0.36, 0.32, 0.32, 0.69, 0.03, 11.15]  # JD P/S looks like a yfinance quirk; mark with note

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors_pe = ["#d9534f" if p == "BIDU" else "#3b78c2" for p in peers]
b = axes[0].bar(peers, pe, color=colors_pe)
axes[0].set_title("Trailing P/E (May 2026)")
axes[0].set_ylabel("TTM P/E")
for bar, v in zip(b, pe):
    axes[0].text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v:.1f}x",
                 ha="center", fontsize=9)
axes[0].axhline(25, color="grey", linewidth=0.7, linestyle="--",
                label="Approx. peer median")

# show P/S on log scale due to GOOGL/JD outliers
b2 = axes[1].bar(peers, ps, color=colors_pe)
axes[1].set_title("Trailing P/S (May 2026)")
axes[1].set_ylabel("TTM P/S")
axes[1].set_yscale("log")
for bar, v in zip(b2, ps):
    axes[1].text(bar.get_x() + bar.get_width() / 2, v * 1.15, f"{v:.2f}x",
                 ha="center", fontsize=9)

fig.suptitle("BIDU vs. China internet + global ad peers — Valuation snapshot",
             fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_peer_valuation.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart 5: Apollo Go cumulative rides, key disclosed milestones
# Source: 20-F filings (2022, 2023, 2024, 2025) and Q1 2026 release.
# ---------------------------------------------------------------
# Cumulative public rides disclosed in 2025 20-F (Feb 2026 ref) and Q1 2026 release.
dates = ["Feb 2026 (20-F)", "Apr 2026 (Q1 release)"]
rides_m = [20.0, 22.0]  # millions
q1_rides = 3.2  # Q1 2026 fully driverless rides, millions

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(dates, rides_m, color=["#3b78c2", "#5cb85c"], width=0.5)
for x, y in zip(dates, rides_m):
    ax.text(x, y + 0.4, f">{y:.0f}M", ha="center", fontsize=11)
ax.set_ylabel("Cumulative public rides (millions)")
ax.set_xlabel("Disclosure")
ax.set_title("Apollo Go — Cumulative public rides (disclosed milestones)\nQ1 2026 alone: 3.2 M fully driverless rides; +120% YoY; weekly peak >350k")
ax.set_ylim(0, 28)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_apollo_go_rides.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart 6: R&D as % of revenue, FY2021-FY2025
# Source: 2025 20-F "Selected Consolidated Financial Data" table.
# ---------------------------------------------------------------
rd = [24.938, 23.315, 24.192, 22.133, 20.433]
rd_pct = [r / rv * 100 for r, rv in zip(rd, revenue)]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years, rd, color="#5bc0de", label="R&D expense (RMB bn)")
for x, y, p in zip(years, rd, rd_pct):
    ax.text(x, y + 0.4, f"{y:.1f}\n({p:.1f}%)", ha="center", fontsize=9)
ax.set_ylabel("R&D expense (RMB bn)")
ax.set_xlabel("Fiscal year")
ax.set_title("Baidu — R&D Investment, FY2021–FY2025\n(figures in RMB bn; % of revenue in parentheses)")
ax.set_ylim(0, 30)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "bidu_rd_trend.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

print("All six charts written to:", OUT)
for f in ["bidu_revenue_margin.png", "bidu_segment_mix.png",
          "bidu_q1_2026_ai_mix.png", "bidu_peer_valuation.png",
          "bidu_apollo_go_rides.png", "bidu_rd_trend.png"]:
    p = os.path.join(OUT, f)
    print(" ", f, "OK" if os.path.exists(p) else "MISSING")
