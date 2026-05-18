"""Peer P/S multiples for industrial robot / motion-control names."""
import matplotlib.pyplot as plt
import numpy as np

# Latest available TTM P/S multiples (May 2026)
peers = ['Estun\n(002747)', 'Inovance\n(300124)', 'Yaskawa\n(6506.T)',
         'Fanuc\n(6954.T)', 'ABB\n(ABBN.SW)', 'Efort\n(688165)', 'Siasun\n(300024)']
ps = [4.2, 4.8, 1.8, 4.2, 3.1, 9.8, 5.7]
colors = ['#C0392B', '#2E5C9E', '#7F8C8D', '#7F8C8D', '#7F8C8D', '#2E8B57', '#2E8B57']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(peers, ps, color=colors, alpha=0.85, edgecolor='black', linewidth=0.4)
for bar, val in zip(bars, ps):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
            f'{val:.1f}x', ha='center', fontsize=10, fontweight='bold')

ax.axhline(np.median(ps), color='gray', linestyle='--', alpha=0.6,
           label=f'Peer median: {np.median(ps):.1f}x')
ax.set_ylabel('TTM P/S Multiple (x)', fontsize=11)
ax.set_ylim(0, 12)
ax.set_title('Industrial Robot Peer P/S Multiples — TTM, May 2026',
             fontsize=12.5, pad=10)
ax.legend(loc='upper right', frameon=False)
ax.grid(axis='y', alpha=0.25)
ax.set_axisbelow(True)
fig.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/estun_peer_multiples.png',
            dpi=150, bbox_inches='tight')
print('saved')
