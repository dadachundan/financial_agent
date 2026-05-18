import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# Frost & Sullivan data cited in 2024 AR: 2023-2027 CAGR
segments = ['EV mica\n(CAGR 37.6%)', 'Energy storage mica\n(CAGR 64.4%)', 'Home appliance mica\n(CAGR 14.1%)', 'Cable mica\n(CAGR 13.9%)', 'Industrial+power\n(CAGR 5-10%)']
size_2023 = [29.8, 4.7, 6.9, 16.3, 88.6]
size_2027 = [104.4, 35.3, 11.7, 27.4, 116.9]

x = np.arange(len(segments))
w = 0.38
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(x - w/2, size_2023, w, label='2023 (RMB bn)', color='#9ca3af')
ax.bar(x + w/2, size_2027, w, label='2027E (RMB bn)', color='#2563eb')
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=8.5)
ax.set_ylabel('Market size (RMB bn)')
ax.set_title('Global mica-material TAM by application — 2023 vs. 2027E (Frost & Sullivan)')
ax.legend()
for i, (a, b) in enumerate(zip(size_2023, size_2027)):
    ax.text(i - w/2, a + 2, f'{a:.1f}', ha='center', fontsize=8)
    ax.text(i + w/2, b + 2, f'{b:.1f}', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/glorymica_tam.png', dpi=150, bbox_inches='tight')
print('saved')
