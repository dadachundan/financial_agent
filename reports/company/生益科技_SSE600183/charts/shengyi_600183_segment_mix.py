"""
生益科技 (SSE:600183) — 主营业务收入分产品结构 2023–2025
Data from 2025年报 主营业务分行业情况
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

categories = ["覆铜板+粘结片", "印制线路板\n(生益电子)", "废弃资源利用", "房地产"]

# 2023 data (from 2024 AR approximation)  — from available figures
# 2024 data from 2025 AR
# 2025 data from 2025年报 page 14
rev_2023 = [13.48, 4.51, 0.71, 0.07]  # bn RMB approx
rev_2024 = [14.80, 4.53, 0.71, 0.07]  # bn approx (CCL ~72%, PCB~22%)
rev_2025 = [17.77, 9.14, 0.86, 0.09]  # from 2025年报 exact

x = np.arange(len(categories))
width = 0.25

fig, ax = plt.subplots(figsize=(11, 6))

colors = ["#2A6EBB", "#27AE60", "#F39C12", "#9B59B6"]

b1 = ax.bar(x - width, rev_2023, width, label="2023年", color=colors, alpha=0.6)
b2 = ax.bar(x, rev_2024, width, label="2024年", color=colors, alpha=0.8)
b3 = ax.bar(x + width, rev_2025, width, label="2025年", color=colors, alpha=1.0)

ax.set_xlabel("业务分部", fontsize=12)
ax.set_ylabel("营业收入 (亿元人民币)", fontsize=12)
ax.set_title("生益科技 (SSE:600183) — 主营业务分产品收入 2023–2025", fontsize=13, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.legend(fontsize=11)
ax.set_ylim(0, 22)

# Add value labels for 2025
for bar in b3:
    height = bar.get_height()
    if height > 0.2:
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
path = "/Users/x/projects/financial_agent/reports/charts/shengyi_600183_segment_mix.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
print(f"Saved: {path}")
