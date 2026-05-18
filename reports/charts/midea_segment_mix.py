"""Midea Group FY2025 revenue mix by segment."""
import matplotlib.pyplot as plt

segments = ['Smart Home\n(consumer appliances)', 'Building Technologies\n(HVAC + elevators)',
            'Robotics & Automation\n(KUKA + Swisslog)', 'Industrial Technologies\n(compressors / motors)',
            'New Energy / Logistics / Other']
revenue = [299.93, 35.79, 31.01, 27.23, 62.49]  # RMB bn, FY2025
labels_pct = [f'{r:.1f} bn ({r/sum(revenue)*100:.1f}%)' for r in revenue]
colors = ['#1f4e79', '#2e75b6', '#c00000', '#ed7d31', '#7f7f7f']

fig, ax = plt.subplots(figsize=(9, 5.5))
wedges, _ = ax.pie(revenue, labels=None, colors=colors, startangle=90,
                   wedgeprops=dict(width=0.45, edgecolor='white'))
ax.legend(wedges, [f'{s}: {l}' for s, l in zip(segments, labels_pct)],
          loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
ax.set_title('Midea Group — FY2025 Revenue Mix by Segment\n(RMB 456.5 bn total)',
             fontsize=12, pad=14)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/midea_segment_mix.png', dpi=150, bbox_inches='tight')
print('saved')
