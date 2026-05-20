"""AVGO vs. peer TTM P/E & P/S. Source: Yahoo Finance, 2026-05-20."""
import matplotlib.pyplot as plt
import numpy as np

tickers = ["AVGO", "NVDA", "MRVL", "QCOM"]
pe = [81.4, 45.7, 60.2, 21.8]
ps = [29.0, 25.1, 19.8, 4.8]

x = np.arange(len(tickers))
w = 0.36
fig, ax1 = plt.subplots(figsize=(9, 5))
b1 = ax1.bar(x - w/2, pe, w, color="#1f77b4", label="TTM P/E")
b2 = ax1.bar(x + w/2, ps, w, color="#d62728", label="TTM P/S")
ax1.set_xticks(x); ax1.set_xticklabels(tickers)
ax1.set_ylabel("Multiple (x)")
ax1.set_title("AVGO vs. peers — TTM P/E and P/S (2026-05-20 close)")
for i, (p, s) in enumerate(zip(pe, ps)):
    ax1.text(i - w/2, p + 1.2, f"{p:.1f}x", ha="center", fontsize=9)
    ax1.text(i + w/2, s + 1.2, f"{s:.1f}x", ha="center", fontsize=9)
ax1.set_ylim(0, 95)
ax1.legend()
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/avgo_peer_valuation.png", dpi=150, bbox_inches="tight")
print("saved")
