import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

years = ['2022', '2023', '2024', '2025E']
# Revenue in RMB mn
revenue = [667.5, 800.3, 1134.8, 1380.0]  # 2025E from Q1-Q3 actual + Q4 implied
# Net income RMB mn
net_income = [133.8, 171.8, 230.2, 280.0]
# Gross margin %
gm = [38.5, 37.0, 34.5, 35.7]  # 2022 ~38.5 derived from filings discussion; 2024 actual 34.48; 2025 H1 implied

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(years, revenue, color='#3b82f6', alpha=0.85, label='Revenue (RMB mn)')
ax1.set_xlabel('Fiscal Year')
ax1.set_ylabel('Revenue (RMB mn)', color='#3b82f6')
ax1.tick_params(axis='y', labelcolor='#3b82f6')
for i, v in enumerate(revenue):
    ax1.text(i, v + 30, f'{v:.0f}', ha='center', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm, color='#ef4444', marker='o', linewidth=2, label='Gross margin %')
ax2.set_ylabel('Gross margin (%)', color='#ef4444')
ax2.tick_params(axis='y', labelcolor='#ef4444')
ax2.set_ylim(20, 45)
for i, v in enumerate(gm):
    ax2.text(i, v + 0.8, f'{v:.1f}%', ha='center', fontsize=9, color='#ef4444')

plt.title('Glorymica (SSE:603119) — Revenue and Gross Margin, FY2022–FY2025E')
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/glorymica_revenue_margin.png', dpi=150, bbox_inches='tight')
print('saved')
