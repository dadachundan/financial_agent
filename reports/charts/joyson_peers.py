"""Joyson Electronics peer multiple comparison."""
import matplotlib.pyplot as plt
import numpy as np

peers = ['Joyson\n(600699)', 'Huayu Auto\n(600741)', 'Autoliv\n(ALV)',
         'Magna\n(MGA)', 'Aptiv\n(APTV)']
pe_ttm = [33.9, 8.7, 12.4, 13.4, 14.5]
ps_ttm = [0.71, 0.34, 0.81, 0.32, 0.55]

x = np.arange(len(peers))
width = 0.36
fig, ax1 = plt.subplots(figsize=(10, 5.5))

c1, c2 = '#1f4e79', '#c0392b'
b1 = ax1.bar(x - width/2, pe_ttm, width, label='P/E TTM (x)', color=c1, alpha=0.85)
ax2 = ax1.twinx()
b2 = ax2.bar(x + width/2, ps_ttm, width, label='P/S TTM (x)', color=c2, alpha=0.85)

ax1.set_xticks(x)
ax1.set_xticklabels(peers, fontsize=9)
ax1.set_ylabel('P/E TTM (x)', color=c1)
ax2.set_ylabel('P/S TTM (x)', color=c2)
ax1.tick_params(axis='y', labelcolor=c1)
ax2.tick_params(axis='y', labelcolor=c2)
ax1.set_ylim(0, 45)
ax2.set_ylim(0, 1.2)

for b, v in zip(b1, pe_ttm):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.8, f'{v:.1f}x',
             ha='center', fontsize=9, color=c1)
for b, v in zip(b2, ps_ttm):
    ax2.text(b.get_x() + b.get_width()/2, v + 0.025, f'{v:.2f}x',
             ha='center', fontsize=9, color=c2)

plt.title('Tier-1 Auto Supplier Peer Multiples — May 2026 (TTM)',
          fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.2)
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.92), fontsize=9)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/joyson_peers.png',
            dpi=150, bbox_inches='tight')
print('saved')
