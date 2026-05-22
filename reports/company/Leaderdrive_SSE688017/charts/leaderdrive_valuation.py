"""Valuation snapshot: 绿的谐波 P/E vs peers (机器人核心部件)."""
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'STHeiti', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# TTM P/E based on 2025 net income, market cap from Eastmoney 2026-05-20
peers = ['绿的谐波\n(SSE:688017)', '汇川技术\n(SZSE:300124)', '埃斯顿\n(SZSE:002747)', '双环传动\n(SZSE:002472)', '中大力德\n(SZSE:002896)', '国茂股份\n(SH:603915)']
pe_ttm = [493.8, 30.2, 0, 35.6, 95.0, 18.4]
# Note: 埃斯顿 reported net loss in 2024 → negative P/E shown as 0 with note
colors = ['#d62728', '#1f77b4', '#7f7f7f', '#1f77b4', '#ff7f0e', '#1f77b4']

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(peers, pe_ttm, color=colors)
ax.set_ylabel('TTM P/E (倍)')
ax.set_title('绿的谐波 vs. 同业 — TTM P/E 估值对比 (2026-05-20)')
for b, v, name in zip(bars, pe_ttm, peers):
    label = f'{v:.0f}×' if v > 0 else 'N/A (亏损)'
    ax.text(b.get_x() + b.get_width()/2, v + 10, label, ha='center', fontsize=10, fontweight='bold')
ax.set_ylim(0, max(pe_ttm) * 1.15)
ax.axhline(y=35, color='gray', linestyle='--', alpha=0.5, label='科创板 / 工业自动化板块中位 ≈ 35×')
ax.legend(loc='upper right')
fig.tight_layout()
out = '/Users/x/projects/financial_agent/reports/charts/leaderdrive_valuation.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print('saved', out)
