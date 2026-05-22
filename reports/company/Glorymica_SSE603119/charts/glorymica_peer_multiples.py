import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

peers = ['Glorymica\n(603119)', 'Hengli Hydraulic\n(601100)', 'Shuanglin\n(300100)', 'Mingzhi Electric\n(603728)', 'Leader Harmonious\n(688017)']
pe_ttm = [128.8, 56.2, 44.3, 401.8, 409.6]
ps_ttm = [26.8, 12.3, 3.5, 12.1, 35.0]

x = range(len(peers))
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

colors = ['#dc2626', '#475569', '#475569', '#475569', '#475569']
axes[0].bar(x, pe_ttm, color=colors)
axes[0].set_xticks(x)
axes[0].set_xticklabels(peers, fontsize=8)
axes[0].set_ylabel('TTM P/E (x)')
axes[0].set_title('TTM P/E — Glorymica vs. Humanoid / Motion-Control Peers')
for i, v in enumerate(pe_ttm):
    axes[0].text(i, v + 8, f'{v:.0f}x', ha='center', fontsize=9)

axes[1].bar(x, ps_ttm, color=colors)
axes[1].set_xticks(x)
axes[1].set_xticklabels(peers, fontsize=8)
axes[1].set_ylabel('TTM P/S (x)')
axes[1].set_title('TTM P/S — Glorymica vs. Peers')
for i, v in enumerate(ps_ttm):
    axes[1].text(i, v + 1, f'{v:.1f}x', ha='center', fontsize=9)

plt.suptitle('Glorymica valuation vs. A-share humanoid / hydraulic / motion peers (2026-05-15 close)', y=1.02)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/glorymica_peer_multiples.png', dpi=150, bbox_inches='tight')
print('saved')
