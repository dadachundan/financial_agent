"""AVGO segment revenue mix FY23-FY25 + Q1 FY26. Source: 2025 10-K, Q1 FY26 8-K."""
import matplotlib.pyplot as plt
import numpy as np

periods = ["FY23", "FY24", "FY25", "Q1 FY26"]
semi = [28.182, 30.096, 36.858, 12.515]  # $B
sw = [7.637, 21.478, 27.029, 6.796]  # $B

x = np.arange(len(periods))
w = 0.6
fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x, semi, w, label="Semiconductor Solutions", color="#1f77b4")
b2 = ax.bar(x, sw, w, bottom=semi, label="Infrastructure Software", color="#ff7f0e")
ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.set_ylabel("Net revenue (USD B)")
ax.set_title("Broadcom — Net revenue by segment")
for i, (s, sf) in enumerate(zip(semi, sw)):
    ax.text(i, s / 2, f"${s:.1f}B", ha="center", color="white", fontsize=9)
    ax.text(i, s + sf / 2, f"${sf:.1f}B", ha="center", color="white", fontsize=9)
    ax.text(i, s + sf + 1, f"Total ${s+sf:.1f}B", ha="center", fontsize=9)
ax.legend(loc="upper left")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/avgo_segment_mix.png", dpi=150, bbox_inches="tight")
print("saved")
