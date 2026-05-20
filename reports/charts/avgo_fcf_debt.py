"""AVGO free cash flow vs. total debt, FY21-FY25. Sources: 10-K filings."""
import matplotlib.pyplot as plt
import numpy as np

years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
fcf = [13.32, 16.31, 17.63, 19.41, 26.92]  # FCF $B (OCF less capex)
total_debt = [39.4, 39.4, 37.6, 67.6, 65.1]  # Total debt $B incl. short-term; FY24/FY25 from balance sheets; FY23/22 from 10-Ks

x = np.arange(len(years))
w = 0.36
fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(x - w/2, fcf, w, label="Free cash flow", color="#2ca02c")
ax1.bar(x + w/2, total_debt, w, label="Total debt (S/T + L/T)", color="#7f7f7f")
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel("USD billions")
ax1.set_title("Broadcom — Free cash flow vs. total debt, FY2021–FY2025")
for i, (f, d) in enumerate(zip(fcf, total_debt)):
    ax1.text(i - w/2, f + 0.6, f"${f:.1f}B", ha="center", fontsize=8.5)
    ax1.text(i + w/2, d + 0.6, f"${d:.1f}B", ha="center", fontsize=8.5)
ax1.legend(loc="upper left")
ax1.set_ylim(0, 80)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/avgo_fcf_debt.png", dpi=150, bbox_inches="tight")
print("saved")
