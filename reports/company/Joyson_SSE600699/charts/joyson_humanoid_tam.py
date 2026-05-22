"""Humanoid robot global market size projections."""
import matplotlib.pyplot as plt

years = ['2025', '2026', '2027', '2028', '2029', '2030', '2035']
gs_low = [2.9, 4.1, 5.8, 8.1, 11.5, 15.3, 38.0]   # USD bn — Goldman/M&M blend
ms_high = [3.0, 5.0, 8.0, 13.0, 22.0, 37.0, 150.0]  # Morgan Stanley higher bound

fig, ax = plt.subplots(figsize=(9.5, 5.0))
ax.plot(years, gs_low, marker='o', linewidth=2.2, color='#1f4e79',
        label='Goldman Sachs / MarketsandMarkets base case (USD bn)')
ax.plot(years, ms_high, marker='s', linewidth=2.2, color='#c0392b',
        linestyle='--',
        label='Morgan Stanley / Macquarie upside case (USD bn)')

for x, y in zip(years, gs_low):
    ax.text(x, y + 2, f'${y:.0f}B', ha='center', fontsize=8.5, color='#1f4e79')
for x, y in zip(years, ms_high):
    ax.text(x, y + 4, f'${y:.0f}B', ha='center', fontsize=8.5, color='#c0392b')

ax.set_ylabel('Global humanoid robot TAM (USD bn)', fontsize=10)
ax.set_title('Humanoid Robot TAM — Wide Range of Sell-Side Forecasts, 2025–2035',
             fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)
ax.legend(loc='upper left', fontsize=9)
ax.set_ylim(0, 170)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/joyson_humanoid_tam.png',
            dpi=150, bbox_inches='tight')
print('saved')
