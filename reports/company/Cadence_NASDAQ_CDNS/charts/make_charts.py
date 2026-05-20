"""Generate charts for the Cadence (CDNS) research report.

Sources:
  - Revenue + margins: Cadence 10-K FY2025 (SEC EDGAR accession 0000813672-26-000016)
    https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm
  - Geographic mix: same 10-K, Revenue by Geography table
  - Segment mix: same 10-K, Revenue by Product Category table
  - Quarterly: Cadence Q1-26 press release (8-K filed 2026-04-27)
    https://www.sec.gov/Archives/edgar/data/813672/000081367226000044/cdns04272026ex9901.htm
  - Valuation multiples: yfinance pull, 2026-05-20.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

# ----------------------------------------------------------------------
# Chart 1: Revenue + GAAP operating margin trend FY2021–FY2025
# ----------------------------------------------------------------------
years = ["2021", "2022", "2023", "2024", "2025"]
# Revenue $M from 10-K FY2025 (3-yr table) and 10-K FY2023 prior comparisons
rev = [2988.0, 3561.7, 4090.0, 4641.3, 5296.8]
# GAAP operating margin (%) — computed from "Income from operations" / Total revenue
# in each year's 10-K (FY2021 21.6%, FY2022 30.1%, FY2023 30.6%, FY2024 29.1%, FY2025 28.2%).
op_margin = [21.6, 30.1, 30.6, 29.1, 28.2]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, rev, color="#1f4e79", alpha=0.85, label="Revenue ($M)")
ax1.set_ylabel("Revenue (US$M)", color="#1f4e79", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 6000)
for b, v in zip(bars, rev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 80, f"${v:,.0f}M",
             ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, op_margin, marker="o", color="#c0504d", linewidth=2.2,
         label="GAAP operating margin (%)")
ax2.set_ylabel("GAAP Operating Margin (%)", color="#c0504d", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c0504d")
ax2.set_ylim(20, 40)
for x, y in zip(years, op_margin):
    ax2.text(x, y + 0.6, f"{y:.1f}%", ha="center", color="#c0504d", fontsize=9)

plt.title("Cadence Design Systems — Revenue & GAAP Operating Margin, FY2021–FY2025",
          fontsize=12, pad=12)
fig.tight_layout()
plt.savefig(OUT / "cdns_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_revenue_margin.png")

# ----------------------------------------------------------------------
# Chart 2: Revenue by Product Category, FY2023 vs FY2024 vs FY2025
# ----------------------------------------------------------------------
cats = ["Core EDA", "Semiconductor IP", "System Design & Analysis"]
# FY2024 / FY2025 product-category mix (% of total revenue) from 10-K FY2025.
# Cadence restructured the product-category disclosure in FY2024 (consolidated
# Custom IC + Digital + Functional Verification into "Core EDA"), so a like-for-like
# FY2023 bar is not available in the new framework.
share_2024 = [71, 13, 16]
share_2025 = [70, 14, 16]

x = np.arange(len(cats))
w = 0.35
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w / 2, share_2024, w, label="FY2024", color="#1f4e79")
ax.bar(x + w / 2, share_2025, w, label="FY2025", color="#0b2e4f")
for i, (a, b) in enumerate(zip(share_2024, share_2025)):
    ax.text(i - w / 2, a + 1, f"{a}%", ha="center", fontsize=9)
    ax.text(i + w / 2, b + 1, f"{b}%", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(cats)
ax.set_ylabel("% of total revenue")
ax.set_title("Cadence Revenue Mix by Product Category, FY2024 vs FY2025", pad=10)
ax.set_ylim(0, 90)
ax.legend()
fig.tight_layout()
plt.savefig(OUT / "cdns_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_segment_mix.png")

# ----------------------------------------------------------------------
# Chart 3: Revenue by Geography FY2025 (pie)
# ----------------------------------------------------------------------
geo_labels = ["United States 44%", "Other Asia 19%", "EMEA 15%",
              "China 13%", "Japan 6%", "Other Americas 3%"]
geo_pct = [44, 19, 15, 13, 6, 3]
colors = ["#1f4e79", "#2e75b6", "#5b9bd5", "#c0504d", "#ed7d31", "#a5a5a5"]

fig, ax = plt.subplots(figsize=(7.5, 6))
ax.pie(geo_pct, labels=geo_labels, autopct="", startangle=90,
       colors=colors, wedgeprops=dict(edgecolor="white", linewidth=1.5))
ax.set_title("Cadence FY2025 Revenue by Geography\n(Total: US$5,296.8M)",
             fontsize=12, pad=12)
fig.tight_layout()
plt.savefig(OUT / "cdns_geography_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_geography_pie.png")

# ----------------------------------------------------------------------
# Chart 4: Peer valuation — TTM P/E and P/S vs CDNS
# ----------------------------------------------------------------------
peers = ["CDNS", "SNPS", "KEYS", "ADSK"]
pe = [81.0, 75.1, 54.3, 46.2]
ps = [17.3, 11.7, 10.2, 7.1]

x = np.arange(len(peers))
w = 0.35
fig, ax1 = plt.subplots(figsize=(9, 5))
b1 = ax1.bar(x - w / 2, pe, w, label="TTM P/E", color="#1f4e79")
b2 = ax1.bar(x + w / 2, ps, w, label="TTM P/S", color="#c0504d")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
ax1.set_ylabel("Multiple (x)")
ax1.set_title("EDA & Design-Software Peer Valuation (TTM, 2026-05-20)", pad=10)
ax1.set_ylim(0, 100)
for bar, v in zip(b1, pe):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v:.1f}x",
             ha="center", fontsize=9)
for bar, v in zip(b2, ps):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v:.1f}x",
             ha="center", fontsize=9)
ax1.legend()
fig.tight_layout()
plt.savefig(OUT / "cdns_peer_multiples.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_peer_multiples.png")

# ----------------------------------------------------------------------
# Chart 5: EDA TAM growth (Cadence-stated TAM from Investor Day / 10-K)
# Cadence cited a "Computational Software TAM ~$50B in 2024 growing to
# ~$170B by 2032" at its 2024 Investor Day. We use that range here.
# ----------------------------------------------------------------------
yrs = ["2024", "2026E", "2028E", "2030E", "2032E"]
tam = [50, 70, 95, 130, 170]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(yrs, tam, marker="o", linewidth=2.5, color="#1f4e79")
for x, y in zip(yrs, tam):
    ax.text(x, y + 4, f"${y}B", ha="center", fontsize=10)
ax.set_ylabel("TAM (US$B)")
ax.set_title("Cadence Stated Computational Software TAM\n(per 2024 Investor Day)",
             pad=10)
ax.set_ylim(0, 200)
ax.grid(alpha=0.25)
fig.tight_layout()
plt.savefig(OUT / "cdns_tam.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_tam.png")

# ----------------------------------------------------------------------
# Chart 6: Quarterly revenue trend 2024Q1 – 2026Q1
# (From CDNS quarterly press releases / 8-Ks)
# ----------------------------------------------------------------------
qs = ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25",
      "Q4-25", "Q1-26"]
qrev = [1009, 1061, 1215, 1356, 1242, 1275, 1339, 1440, 1474]

fig, ax = plt.subplots(figsize=(9.5, 5))
bars = ax.bar(qs, qrev, color="#1f4e79")
for b, v in zip(bars, qrev):
    ax.text(b.get_x() + b.get_width() / 2, v + 18, f"${v:,}",
            ha="center", fontsize=8.5)
ax.set_ylabel("Revenue (US$M)")
ax.set_title("Cadence Quarterly Revenue, Q1-2024 to Q1-2026", pad=10)
ax.set_ylim(0, 1700)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
plt.savefig(OUT / "cdns_quarterly.png", dpi=150, bbox_inches="tight")
plt.close()
print("saved cdns_quarterly.png")

print("All charts written to", OUT)
