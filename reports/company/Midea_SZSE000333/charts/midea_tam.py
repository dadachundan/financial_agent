"""Global home appliance TAM 2025-2030 + KUKA-relevant industrial robotics TAM."""
import matplotlib.pyplot as plt
import numpy as np

years = list(range(2025, 2031))
home_appliance = [547, 575, 605, 636, 668, 702]      # USD bn, Mordor Intelligence midpoint
smart_appliance = [42.4, 47.0, 52.2, 58.0, 64.3, 71.3]  # USD bn, MarketsAndMarkets
industrial_robot = [42, 47, 53, 60, 67, 75]            # USD bn, NextMSC trajectory

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, home_appliance, marker='o', linewidth=2.2, color='#1f4e79', label='Global home appliances')
ax.plot(years, smart_appliance, marker='s', linewidth=2.2, color='#c00000', label='Smart appliances (subset)')
ax.plot(years, industrial_robot, marker='^', linewidth=2.2, color='#ed7d31', label='Industrial robotics (KUKA-served)')

for x, y in zip(years, home_appliance):
    ax.text(x, y+12, f'{y}', ha='center', fontsize=8, color='#1f4e79')
for x, y in zip(years, industrial_robot):
    ax.text(x, y-18, f'{y}', ha='center', fontsize=8, color='#ed7d31')

ax.set_xlabel('Year')
ax.set_ylabel('Market size (USD bn)')
ax.set_title('Midea Addressable Markets — 2025–2030', fontsize=12, pad=12)
ax.legend(loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/midea_tam.png', dpi=150, bbox_inches='tight')
print('saved')
