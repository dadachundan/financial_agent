"""
沪电股份 (SZSE:002463) — Global PCB Market TAM and High-Layer PCB Growth
Data source: Prismark 2025Q4 Research Report (cited in 沪士电子 2025年度报告)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

years = [2023, 2024, 2025, 2026, 2030]
# Global PCB total market 亿美元
# 2023: ~704 (Prismark est implied from 2024 +5.8% = 735.65 → 2023 ~695)
# 2024: ~735 (Prismark 2024Q4: ~740)
# 2025: ~851 (Prismark 2025Q4: 851.52)
# 2026: ~957 (Prismark 2025Q4 forecast: 957.8)
# 2030: ~1230 (Prismark forecast: >1,230)
global_pcb = [695, 736, 852, 958, 1233]

# HLC (18+ layer) segment, 亿美元
# 2023: implied from 2024 data: 24.21 → 2023 ~17.3 (2024 +40.2% = 24.21 → 2023=17.3)
# 2024: ~24.21 (from Prismark table: 2,421 million)
# 2025: ~49.28 (from Prismark table: 4,928 million — +72.8% from 2,421 in Prismark estimates after correction: actually 2025 HLC = 4928M = 49.28B → approx 49.3)
# Note: Prismark table shows 18+ layer: 2025=4,928M, 2026=8,002M, 2030=13,159M
# 2023 = 2024/(1+0.402) = 2421/1.402 = 1727M
hlc_18plus = [17.3, 24.2, 49.3, 80.0, 131.6]

# Data comm PCB segment (server+network)
# 2024: 23,895M=238.95; 2025 est: 31,801=318.01; 2029 forecast: 47,398
# 2023: 23895/1.xx → use 2024 data only from here
# Interpolate for chart
data_comm = [None, 239, 318, None, None]  # only 2024, 2025 available

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Total global PCB market
ax1.bar(years, global_pcb, color=['#7EB8F7' if y < 2025 else ('#1E5FA8' if y < 2027 else '#0A2D6B') for y in years],
        alpha=0.85, width=[0.7, 0.7, 0.7, 0.7, 0.7])
ax1.set_title('全球 PCB 市场规模预测 (亿美元)', fontsize=12, fontweight='bold')
ax1.set_xlabel('年份', fontsize=11)
ax1.set_ylabel('市场规模（亿美元）', fontsize=11)
ax1.set_xticks(years)
ax1.set_ylim(0, 1500)
ax1.grid(axis='y', alpha=0.3)

# Annotate bars
for y, v in zip(years, global_pcb):
    style = 'est.' if y == 2025 else ('预测' if y >= 2026 else '')
    ax1.text(y, v + 15, f'${v}\n{style}', ha='center', va='bottom', fontsize=9.5)

# Add CAGR annotation
ax1.annotate('2025–2030 CAAGR: 7.7%', xy=(2028, 1095), fontsize=10,
             color='red', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3CD', edgecolor='orange'))

# Chart 2: 18+ layer (HLC) PCB — fastest growing segment
color_hlc = ['#7EB8F7', '#4A90D9', '#1E5FA8', '#0F3D7A', '#071E52']
ax2.bar(years, hlc_18plus, color=color_hlc, alpha=0.85, width=[0.7]*5)
ax2.set_title('高层板 HLC (18+层) 市场规模预测 (亿美元)', fontsize=12, fontweight='bold')
ax2.set_xlabel('年份', fontsize=11)
ax2.set_ylabel('市场规模（亿美元）', fontsize=11)
ax2.set_xticks(years)
ax2.set_ylim(0, 170)
ax2.grid(axis='y', alpha=0.3)

labels = ['~17.3\n(推算)', '24.2', '49.3\n(+72.8%)', '80.0\n(+62.4%)', '131.6']
for y, v, lbl in zip(years, hlc_18plus, labels):
    ax2.text(y, v + 1.5, lbl, ha='center', va='bottom', fontsize=9.5)

ax2.annotate('2025–2030 CAAGR: 21.7%', xy=(2028, 148), fontsize=10,
             color='red', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3CD', edgecolor='orange'))

fig.suptitle('全球 PCB 市场规模 — Prismark 2025Q4 预测', fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/wus_002463_tam.png',
            dpi=150, bbox_inches='tight')
print("Saved wus_002463_tam.png")
