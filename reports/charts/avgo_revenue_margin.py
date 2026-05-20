"""AVGO 5-year revenue and gross margin trend (FY21-FY25). Sources: 10-K filings."""
import matplotlib.pyplot as plt

years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
revenue = [27.45, 33.20, 35.82, 51.57, 63.89]  # $B; FY21 from 10-K filed Dec 2021; later years from 2025 10-K p.40 (3yr) and 2023 10-K
gm_gaap_pct = [55.9, 66.6, 68.9, 63.0, 67.8]  # GAAP GM% — FY25/24/23 from 2025 10-K; FY22/FY21 from respective 10-Ks

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#1f77b4", alpha=0.78, label="Total revenue (USD B, left)")
ax1.set_ylabel("Total net revenue (USD B)", color="#1f77b4")
ax1.set_xlabel("Fiscal year")
ax1.set_ylim(0, 75)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 1.5, f"${v:.1f}B", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm_gaap_pct, color="#d62728", marker="o", linewidth=2.2, label="GAAP gross margin % (right)")
ax2.set_ylabel("GAAP gross margin %", color="#d62728")
ax2.set_ylim(40, 80)
for x, y in zip(years, gm_gaap_pct):
    ax2.text(x, y + 1.2, f"{y:.1f}%", ha="center", color="#d62728", fontsize=9)

plt.title("Broadcom (AVGO) — Revenue & GAAP Gross Margin, FY2021–FY2025")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/avgo_revenue_margin.png", dpi=150, bbox_inches="tight")
print("saved")
