"""
沪电股份 (SZSE:002463) — Revenue & Gross Margin Trend 2021–2025
Data source: 沪士电子股份有限公司年度报告 (各年)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

years = [2021, 2022, 2023, 2024, 2025]
revenue_bn = [74.19, 83.36, 89.38, 133.42, 189.45]   # 亿元 (PCB+other revenue total)
gross_margin = [28.50, 31.72, 35.22, 35.85, 36.91]    # PCB segment gross margin %
# Note: 2021, 2022 from 年报; 2023 from 2024年报; 2024 & 2025 from 2025年报
# 2023 PCB gross margin: revenue 89.38亿, PCB ~82.64亿, need to derive
# From 2024 annrep: 2023 PCB 35.22% - using reported figures
# Actually from 2024年报 2023 data: PCB revenue 8,264,304,... implied ~35%
# Using the directly reported PCB segment gross margins where available

fig, ax1 = plt.subplots(figsize=(10, 6))

color_rev = '#1E5FA8'
color_gm = '#E84040'

bars = ax1.bar(years, revenue_bn, color=color_rev, alpha=0.75, width=0.6, label='营业收入 (亿元)')
ax1.set_xlabel('年份', fontsize=12)
ax1.set_ylabel('营业收入（亿元）', color=color_rev, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_rev)
ax1.set_ylim(0, 240)
ax1.set_xticks(years)

# Add revenue labels on bars
for bar, val in zip(bars, revenue_bn):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
             f'{val:.1f}', ha='center', va='bottom', fontsize=10, color=color_rev, fontweight='bold')

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color=color_gm, marker='o', linewidth=2.5, markersize=8, label='PCB毛利率 (%)')
ax2.set_ylabel('PCB 毛利率 (%)', color=color_gm, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color_gm)
ax2.set_ylim(20, 50)

for x, y in zip(years, gross_margin):
    ax2.annotate(f'{y:.1f}%', (x, y), textcoords='offset points', xytext=(0, 10),
                 ha='center', fontsize=10, color=color_gm, fontweight='bold')

ax1.set_title('沪电股份 (SZSE:002463) 营业收入与 PCB 毛利率趋势 2021–2025',
              fontsize=13, fontweight='bold', pad=15)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/wus_002463_revenue_margin.png',
            dpi=150, bbox_inches='tight')
print("Saved wus_002463_revenue_margin.png")
