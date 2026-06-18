"""Bespoke charts for Baidu (NASDAQ:BIDU) research report.

These three bespoke matplotlib PNGs cover ground the standard stdlib-SVG suite
(income/balance/cashflow Sankeys, donuts, revbars, DuPont, GF radar, moneyflow)
does NOT cover: a peer forward-valuation snapshot, the Q1'26 Baidu Core
AI-powered Business revenue mix, and the multi-year R&D-investment trend.

Charts that the SVG suite SUPERSEDES were dropped on the 2026-06-18 refresh:
  - revenue_margin  -> covered by income Sankey + revbars
  - segment_mix     -> covered by segment donut + revbars

Data sourced from Baidu's FY2025 Form 20-F (filed 2026-03-17, d38065d20f.htm) and
the Q1 2026 earnings press release (filed 2026-05-18, d156481dex991.htm), both on
SEC EDGAR; peer multiples from yfinance (forward P/E + TTM P/S) as of 2026-06-18.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = os.path.dirname(__file__)
SRC_FOOT = ("Source: Baidu FY2025 20-F (d38065d20f.htm) + Q1'26 results 6-K "
            "(d156481dex991.htm); peers via yfinance, 2026-06-18")

# Fiscal-year revenue (RMB bn) — FY2025 20-F Statements of Comprehensive Income
years = [2021, 2022, 2023, 2024, 2025]
revenue = [124.493, 123.675, 134.598, 133.125, 129.079]

# ---------------------------------------------------------------
# Chart A: Q1-2026 Baidu Core AI-powered Business breakdown
# Source: Q1 2026 press release (EX-99.1, 2026-05-18).
#   AI-powered Business total RMB 13.6 bn (+49% YoY); >50% of Baidu General Business.
#   AI Cloud Infra RMB 8.8 bn (+79% YoY). Remaining ~RMB 4.8 bn = AI Applications +
#   AI-native Marketing Services (press release narrates these as the other two pillars).
# ---------------------------------------------------------------
labels = ["AI Cloud Infra\nRMB 8.8 bn (+79% YoY)\nincl. GPU Cloud +184% YoY",
          "AI Applications +\nAI-native Marketing\nRMB ~4.8 bn"]
sizes = [8.8, 4.8]
colors = ["#3b78c2", "#5cb85c"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(sizes, labels=labels, colors=colors, autopct=lambda p: f"{p:.0f}%",
       startangle=90, textprops={"fontsize": 10})
ax.set_title("Baidu Core AI-powered Business — Q1 2026 revenue mix\n"
             "(total RMB 13.6 bn, +49% YoY; first quarter > 50% of Baidu General Business)")
fig.text(0.5, 0.01, SRC_FOOT, ha="center", fontsize=7, color="grey")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(os.path.join(OUT, "bidu_q1_2026_ai_mix.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart B: Peer FORWARD valuation snapshot — forward P/E + TTM P/S, 2026-06-18
# Sources: yfinance, 2026-06-18. BIDU trailing P/E is n/m (GAAP NI distorted by the
# RMB16.2 bn FY2025 impairment), so the meaningful comparison is FORWARD P/E.
# ---------------------------------------------------------------
peers = ["BIDU", "BABA", "PDD", "TCEHY", "0700.HK", "GOOGL", "MSFT"]
fwd_pe = [12.2, 11.5, 6.4, 11.0, 11.5, 25.3, 19.5]
ps = [0.29, 0.25, 0.25, 0.66, 5.17, 10.60, 8.82]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors_pe = ["#d9534f" if p == "BIDU" else "#3b78c2" for p in peers]
b = axes[0].bar(peers, fwd_pe, color=colors_pe)
axes[0].set_title("Forward P/E (2026-06-18)")
axes[0].set_ylabel("Forward P/E")
for bar, v in zip(b, fwd_pe):
    axes[0].text(bar.get_x() + bar.get_width() / 2, v + 0.4, f"{v:.1f}x",
                 ha="center", fontsize=9)

b2 = axes[1].bar(peers, ps, color=colors_pe)
axes[1].set_title("TTM P/S (2026-06-18)")
axes[1].set_ylabel("TTM P/S (log scale)")
axes[1].set_yscale("log")
for bar, v in zip(b2, ps):
    axes[1].text(bar.get_x() + bar.get_width() / 2, v * 1.12, f"{v:.2f}x",
                 ha="center", fontsize=9)

fig.suptitle("BIDU vs China-internet + global-AI peers — forward valuation snapshot",
             fontsize=12)
fig.text(0.5, 0.005, SRC_FOOT + "  ·  BIDU trailing P/E n/m (GAAP NI distorted by FY25 impairment)",
         ha="center", fontsize=7, color="grey")
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(os.path.join(OUT, "bidu_peer_valuation.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------
# Chart C: R&D as % of revenue, FY2021-FY2025
# Source: FY2025 20-F (R&D line) + prior 20-F filings for FY2021-22.
# ---------------------------------------------------------------
rd = [24.938, 23.315, 24.192, 22.133, 20.433]
rd_pct = [r / rv * 100 for r, rv in zip(rd, revenue)]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years, rd, color="#5bc0de")
for x, y, p in zip(years, rd, rd_pct):
    ax.text(x, y + 0.4, f"{y:.1f}\n({p:.1f}%)", ha="center", fontsize=9)
ax.set_ylabel("R&D expense (RMB bn)")
ax.set_xlabel("Fiscal year")
ax.set_title("Baidu — R&D investment, FY2021–FY2025\n"
             "(RMB bn; % of revenue in parentheses)")
ax.set_ylim(0, 30)
fig.text(0.5, 0.01, SRC_FOOT, ha="center", fontsize=7, color="grey")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(os.path.join(OUT, "bidu_rd_trend.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

print("Three bespoke charts written to:", OUT)
for f in ["bidu_q1_2026_ai_mix.png", "bidu_peer_valuation.png", "bidu_rd_trend.png"]:
    p = os.path.join(OUT, f)
    print(" ", f, "OK" if os.path.exists(p) else "MISSING")
