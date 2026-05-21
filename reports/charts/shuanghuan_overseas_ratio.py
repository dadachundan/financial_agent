"""Domestic vs overseas revenue split."""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STHeiti', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

years = ["2023", "2024", "2025"]
# 国内 vs 国外 (RMB bn) - from 2024 & 2025 annual reports
domestic = [6.97, 7.475, 7.037]
overseas = [1.10, 1.306, 2.075]

import numpy as np
fig, ax = plt.subplots(figsize=(9, 5.0))
x = np.arange(len(years))
w = 0.36
bars1 = ax.bar(x - w/2, domestic, w, label="国内销售", color="#1f4e79")
bars2 = ax.bar(x + w/2, overseas, w, label="国外销售", color="#ed7d31")

for bars in (bars1, bars2):
    for bar in bars:
        v = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.1, f"{v:.2f}",
                ha="center", va="bottom", fontsize=9)

ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel("营业收入 (RMB bn)")
ax.set_title("双环传动 内销 vs 外销 收入趋势 (FY2023-FY2025)", fontsize=13, pad=10)
ax.legend(loc="upper left")
ax.set_ylim(0, max(domestic) * 1.20)

# overseas ratio annotation
for i, (d, o) in enumerate(zip(domestic, overseas)):
    pct = o / (d + o) * 100
    ax.text(i, max(domestic) * 1.10, f"外销占比 {pct:.1f}%",
            ha="center", fontsize=9, color="#c0504d", fontweight="bold")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/shuanghuan_overseas_ratio.png",
            dpi=150, bbox_inches="tight")
print("Saved overseas ratio chart")
