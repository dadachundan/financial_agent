import matplotlib.pyplot as plt
import numpy as np

# TTM P/E peer comparison May 2026
companies = ["Lenovo\n(0992.HK)", "Xiaomi\n(1810.HK)", "Samsung\n(005930.KS)", "BYD\n(1211.HK)", "Apple\n(AAPL)", "Tesla\n(TSLA)"]
pe = [14.8, 17.0, 26.0, 29.7, 36.3, 369.4]
colors = ["#888888", "#FF6900", "#1428A0", "#D71921", "#888888", "#CC0000"]

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.bar(companies, pe, color=colors, alpha=0.9)
ax.set_yscale("log")
ax.set_ylabel("TTM P/E (log scale)", fontsize=12)
ax.set_title("TTM P/E — Xiaomi vs. peer set (May 2026)", fontsize=13)
ax.axhline(20, color="grey", linestyle="--", linewidth=1, alpha=0.6)
for bar, v in zip(bars, pe):
    ax.text(bar.get_x() + bar.get_width() / 2, v * 1.05, f"{v:.1f}×", ha="center", fontsize=10, fontweight="bold")

ax.set_ylim(8, 600)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/xiaomi_peer_pe.png", dpi=150, bbox_inches="tight")
print("saved")
