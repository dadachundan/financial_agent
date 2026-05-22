"""Joyson Electronics 5-year revenue + gross margin chart."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

years = ['2020', '2021', '2022', '2023', '2024', '2025']
revenue_bn = [47.89, 45.67, 49.79, 55.73, 55.86, 61.18]
# Approx consolidated GM from annual reports
gross_margin = [12.4, 9.8, 11.7, 14.8, 16.3, 18.3]
net_profit_bn = [0.62, -3.75, 0.39, 1.08, 0.96, 1.34]

fig, ax1 = plt.subplots(figsize=(10, 5.5))

color_rev = '#1f4e79'
color_gm = '#c0392b'

bars = ax1.bar(years, revenue_bn, color=color_rev, alpha=0.85, label='Revenue (RMB bn)')
ax1.set_ylabel('Revenue (RMB bn)', color=color_rev, fontsize=11)
ax1.tick_params(axis='y', labelcolor=color_rev)
ax1.set_ylim(0, 75)
for b, v in zip(bars, revenue_bn):
    ax1.text(b.get_x() + b.get_width()/2, v + 1.0, f'{v:.1f}',
             ha='center', va='bottom', fontsize=9, color=color_rev)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color=color_gm, marker='o', linewidth=2.2,
         label='Gross margin (%)')
ax2.set_ylabel('Gross margin (%)', color=color_gm, fontsize=11)
ax2.tick_params(axis='y', labelcolor=color_gm)
ax2.set_ylim(0, 25)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 0.6, f'{y:.1f}%', ha='center', fontsize=9, color=color_gm)

plt.title('Joyson Electronics (SSE:600699) — Revenue & Gross Margin, FY2020–FY2025',
          fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.25)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/joyson_revenue_margin.png',
            dpi=150, bbox_inches='tight')
print('saved')
