"""Midea Group revenue + net margin trend FY2019-FY2025."""
import matplotlib.pyplot as plt

years = ['FY2019', 'FY2020', 'FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025']
revenue = [278.22, 284.22, 341.23, 343.92, 372.04, 407.15, 456.45]  # RMB bn
net_profit = [24.21, 27.22, 28.57, 29.55, 33.72, 38.54, 43.95]      # RMB bn
net_margin = [n/r*100 for n, r in zip(net_profit, revenue)]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
color1 = '#1f4e79'
bars = ax1.bar(years, revenue, color=color1, alpha=0.85, label='Revenue (RMB bn)')
ax1.set_ylabel('Revenue (RMB bn)', color=color1, fontsize=11)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 520)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x()+b.get_width()/2, v+5, f'{v:.1f}', ha='center', fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = '#c00000'
ax2.plot(years, net_margin, color=color2, marker='o', linewidth=2.2, label='Net margin (%)')
ax2.set_ylabel('Net margin (%)', color=color2, fontsize=11)
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(7, 12)
for x, v in zip(years, net_margin):
    ax2.text(x, v+0.12, f'{v:.1f}%', ha='center', fontsize=9, color=color2)

plt.title('Midea Group — Revenue and Net Margin, FY2019–FY2025', fontsize=12, pad=14)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/midea_revenue_margin.png', dpi=150, bbox_inches='tight')
print('saved')
