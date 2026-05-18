"""Midea Group peer valuation comparison — TTM P/E."""
import matplotlib.pyplot as plt

# Source: Eastmoney / gurufocus / Yahoo Finance, May 2026 readings (TTM)
peers = ['Gree\n000651.SZ', 'Haier\n600690.SS', 'Midea\n000333.SZ', 'Whirlpool\nWHR', 'Electrolux\nELUX-B.ST', 'LG Electronics\n066570.KS']
pe_ttm = [6.5, 10.6, 13.8, 13.6, 22.0, 9.0]
colors = ['#777', '#777', '#c00000', '#777', '#777', '#777']

fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.bar(peers, pe_ttm, color=colors, alpha=0.9)
for b, v in zip(bars, pe_ttm):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f'{v:.1f}x', ha='center', fontsize=10)

ax.axhline(y=sum(pe_ttm)/len(pe_ttm), color='gray', linestyle='--', alpha=0.6,
           label=f'Peer average ({sum(pe_ttm)/len(pe_ttm):.1f}x)')
ax.set_ylabel('TTM P/E (x)', fontsize=11)
ax.set_title('Global Appliance Peer Valuation — TTM P/E (May 2026)', fontsize=12, pad=12)
ax.legend(loc='upper left')
ax.set_ylim(0, 27)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/midea_peer_valuation.png', dpi=150, bbox_inches='tight')
print('saved')
