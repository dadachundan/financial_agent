"""
沪电股份 (SZSE:002463) — Quarterly Revenue Trend 2024Q1–2026Q1
Data source: 沪士电子股份有限公司 2025年度报告 (quarterly breakdown), 2026年一季度报告
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

quarters = ['2024\nQ1', '2024\nQ2', '2024\nQ3', '2024\nQ4',
            '2025\nQ1', '2025\nQ2', '2025\nQ3', '2025\nQ4',
            '2026\nQ1']

# Revenue in 亿元
# 2024 quarterly from 2024 annrep page 6: 25.84, 28.40, 35.87, 43.31
# 2025 quarterly from 2025 annrep page 7: 40.38, 44.56, 50.19, 54.33
# 2026 Q1 from 2026 Q1 report: 62.14
revenue = [25.84, 28.40, 35.87, 43.31, 40.38, 44.56, 50.19, 54.33, 62.14]

# Net profit in 亿元
# 2024: 5.15, 6.26, 7.08, 7.39
# 2025: 7.62, 9.20, 10.35, 11.05
# 2026 Q1: 12.42
net_profit = [5.15, 6.26, 7.08, 7.39, 7.62, 9.20, 10.35, 11.05, 12.42]

x = np.arange(len(quarters))

fig, ax1 = plt.subplots(figsize=(13, 6))

color_rev = '#1E5FA8'
color_np = '#E84040'

bars = ax1.bar(x, revenue, color=[color_rev if i < 4 else ('#4A90D9' if i < 8 else '#003080') for i in x],
               alpha=0.75, width=0.6, label='营业收入 (亿元)')
ax1.set_xlabel('季度', fontsize=12)
ax1.set_ylabel('营业收入（亿元）', color=color_rev, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_rev)
ax1.set_ylim(0, 80)
ax1.set_xticks(x)
ax1.set_xticklabels(quarters, fontsize=10)

for bar, val in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f'{val:.1f}', ha='center', va='bottom', fontsize=8.5)

ax2 = ax1.twinx()
ax2.plot(x, net_profit, color=color_np, marker='o', linewidth=2.5, markersize=7, label='归母净利润 (亿元)')
ax2.set_ylabel('归母净利润（亿元）', color=color_np, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color_np)
ax2.set_ylim(0, 18)

for xi, yi in zip(x, net_profit):
    ax2.annotate(f'{yi:.2f}', (xi, yi), textcoords='offset points', xytext=(0, 8),
                 ha='center', fontsize=8.5, color=color_np)

# Add vertical separator line
ax1.axvline(x=3.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax1.axvline(x=7.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(1.5, 72, '2024', ha='center', fontsize=10, color='gray')
ax1.text(5.5, 72, '2025', ha='center', fontsize=10, color='gray')
ax1.text(8, 72, '2026', ha='center', fontsize=10, color='gray')

ax1.set_title('沪电股份 (SZSE:002463) 季度营收与归母净利润 2024Q1–2026Q1',
              fontsize=13, fontweight='bold', pad=15)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/wus_002463_quarterly.png',
            dpi=150, bbox_inches='tight')
print("Saved wus_002463_quarterly.png")
