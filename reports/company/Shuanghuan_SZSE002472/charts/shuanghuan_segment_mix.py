"""FY2024 vs FY2025 revenue mix by product (stacked bar)."""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STHeiti', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# FY2024 -> FY2025 segment revenue (RMB bn, from annual report 收入构成)
segs = ["乘用车齿轮", "智能执行机构", "减速器及其他", "商用车齿轮", "工程机械齿轮", "电动工具齿轮", "摩托车齿轮", "钢材销售/其他"]
fy24 = [5.325, 0.642, 0.656, 0.722, 0.580, 0.130, 0.095, 0.633]   # in RMB bn
fy25 = [6.005, 0.798, 0.795, 0.672, 0.633, 0.134, 0.076, 0.002]

colors = ["#1f4e79", "#2e75b6", "#5b9bd5", "#c0504d", "#ed7d31",
          "#9e480e", "#7030a0", "#a6a6a6"]

import numpy as np
labels = ["FY2024", "FY2025"]
data = np.array([fy24, fy25])  # shape (2, n_segs)

fig, ax = plt.subplots(figsize=(9, 5.4))
bottom = np.zeros(2)
for i, seg in enumerate(segs):
    vals = data[:, i]
    ax.bar(labels, vals, bottom=bottom, label=seg, color=colors[i], width=0.45)
    for j, v in enumerate(vals):
        if v > 0.25:
            ax.text(j, bottom[j] + v / 2, f"{seg}\n{v:.2f}",
                    ha="center", va="center", fontsize=8, color="white")
    bottom += vals

ax.set_ylabel("营业收入 (RMB bn)")
ax.set_title("双环传动 分产品收入结构 — FY2024 vs FY2025", fontsize=13, pad=12)
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=9)

for j, total in enumerate(data.sum(axis=1)):
    ax.text(j, total + 0.15, f"合计 {total:.2f}", ha="center", fontsize=10, fontweight="bold")

ax.set_ylim(0, max(data.sum(axis=1)) * 1.10)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/shuanghuan_segment_mix.png",
            dpi=150, bbox_inches="tight")
print("Saved segment mix chart")
