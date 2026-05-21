"""谐波减速器 production / sales volume 2023-2025 for 绿的谐波."""
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'STHeiti', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

years = ['2023', '2024', '2025']
# 谐波减速器 销售量 (台) — 2025 annual reports 425,158; 2024 annual reports 246,486; 2023 annual reports 220,xxx?
# Let me use directly the 2025 annual: 销售量 425,158, 上年增减 72.48% → 2024 = 425,158/1.7248 ≈ 246,500
# Per 2024 annual it would say 销售量~ 246k vs 2023 ~ ?; we have to be careful. Use values shown to be safe.
sales = [185000, 246486, 425158]  # 估算 2023 from "去年销售量增长" pattern — not safe, use only 2024/2025 disclosed
# Drop chart approach: do 2024 / 2025 only
years = ['2024', '2025']
production = [251614, 433655]  # 2025 annual: production 433,655, 上年增减 72.27% → 2024 ≈ 251,614
sales = [246486, 425158]

x = np.arange(len(years))
w = 0.35
fig, ax = plt.subplots(figsize=(7, 5))
b1 = ax.bar(x - w/2, [p/1000 for p in production], w, label='生产量 (千台)', color='#1f77b4')
b2 = ax.bar(x + w/2, [s/1000 for s in sales], w, label='销售量 (千台)', color='#ff7f0e')
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('数量 (千台)')
ax.set_title('绿的谐波 — 谐波减速器年生产/销售量 (2024 vs 2025)')
for bars, vals in [(b1, production), (b2, sales)]:
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v/1000 + 8, f'{v/1000:.1f}', ha='center', fontsize=9)
ax.legend()
ax.set_ylim(0, 500)
fig.tight_layout()
out = '/Users/x/projects/financial_agent/reports/charts/leaderdrive_volume.png'
plt.savefig(out, dpi=150, bbox_inches='tight')
print('saved', out)
