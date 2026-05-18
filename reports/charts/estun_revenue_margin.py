"""Estun revenue + gross margin trend, 2020–2025."""
import matplotlib.pyplot as plt
import numpy as np

years = ['2020', '2021', '2022', '2023', '2024', '2025']
# Revenue (RMB bn) — source: Estun 2020-2025 年度报告 (cninfo)
revenue = [2.51, 3.02, 3.88, 4.65, 4.01, 4.89]
# Gross margin (%) consolidated
gross_margin = [33.6, 33.6, 32.4, 31.9, 29.6, 29.5]
# Net income attributable to shareholders (RMB m)
ni = [128, 121, 159, 135, -810, 45]

fig, ax1 = plt.subplots(figsize=(10, 5.5))

bars = ax1.bar(years, revenue, color='#2E5C9E', alpha=0.85, label='Revenue (RMB bn)')
ax1.set_ylabel('Revenue (RMB bn)', fontsize=11, color='#2E5C9E')
ax1.tick_params(axis='y', labelcolor='#2E5C9E')
ax1.set_ylim(0, 6.0)
for bar, val in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.07,
             f'{val:.2f}', ha='center', va='bottom', fontsize=9, color='#2E5C9E')

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, marker='o', color='#C0392B', linewidth=2.2, label='Gross Margin (%)')
ax2.set_ylabel('Gross Margin (%)', fontsize=11, color='#C0392B')
ax2.tick_params(axis='y', labelcolor='#C0392B')
ax2.set_ylim(25, 38)
for x, val in zip(years, gross_margin):
    ax2.text(x, val + 0.4, f'{val:.1f}%', ha='center', fontsize=9, color='#C0392B')

plt.title('Estun (SZSE:002747) Revenue and Gross Margin, FY2020–FY2025',
          fontsize=12.5, pad=12)
ax1.grid(axis='y', alpha=0.25)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/estun_revenue_margin.png',
            dpi=150, bbox_inches='tight')
print('saved')
