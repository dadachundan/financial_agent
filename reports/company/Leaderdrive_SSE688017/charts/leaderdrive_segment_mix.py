"""2025 segment / product mix stacked bar for 绿的谐波."""
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'STHeiti', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 2025 segment revenue (元), from 2025 annual page 37
# By 行业 (industry)
labels = ['工业及具身智能机器人零部件', '机械装备及其零部件', '数控机床零部件', '医疗器械零部件', '其他']
vals = [422.53, 103.46, 33.12, 5.98, 0.59]  # 百万元
colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']

fig, ax = plt.subplots(figsize=(9, 5.5))
total = sum(vals)
left = 0
for label, v, c in zip(labels, vals, colors):
    pct = v / total * 100
    ax.barh(['2025 主营业务结构'], v, left=left, color=c, label=f'{label} ({pct:.1f}%)', edgecolor='white')
    if pct > 3:
        ax.text(left + v/2, 0, f'{pct:.1f}%', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
    left += v
ax.set_xlim(0, total * 1.02)
ax.set_xlabel('营业收入 (百万元)')
ax.set_title('绿的谐波 (SSE:688017) — 2025年主营业务收入结构 (按下游行业)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=9)
fig.tight_layout()
out = '/Users/x/projects/financial_agent/reports/charts/leaderdrive_segment_mix.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print('saved', out)
