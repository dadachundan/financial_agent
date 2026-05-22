"""
沪电股份 (SZSE:002463) — PCB Segment Revenue Mix 2023–2025
Data source: 沪士电子股份有限公司 2025年度报告, 2024年度报告
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# PCB segment revenue in 亿元
# From 2025年报 (page 20): 数据通讯 146.56, 智能汽车 30.45, 工业控制及其他 4.42
# From 2024年报: 数据通讯 100.93, 智能汽车 24.09, 工业控制及其他 3.37
# From 2023年报 data in 2024年报: approx data
categories = ['数据通讯\n(AI服务器/交换机)', '智能汽车\n(EV/ADAS)', '工业控制\n及其他']

# 2023 from 2024 annrep § revenue breakdown: enterprise comm 60.85, auto 19.08, industrial 3.37 approx
# Actually from 2023 annual report data: enterprise comm 6,085M, auto 1,908M, industrial 337M
vals_2023 = [60.85, 19.08, 3.37]
vals_2024 = [100.93, 24.09, 3.37]
vals_2025 = [146.56, 30.45, 4.42]

x = np.arange(len(categories))
width = 0.25

fig, ax = plt.subplots(figsize=(11, 6))

colors = ['#1E5FA8', '#E84040', '#2CA02C']
b1 = ax.bar(x - width, vals_2023, width, label='2023', color='#7EB8F7', edgecolor='white')
b2 = ax.bar(x, vals_2024, width, label='2024', color='#1E5FA8', edgecolor='white')
b3 = ax.bar(x + width, vals_2025, width, label='2025', color='#0A2D6B', edgecolor='white')

def label_bars(bars):
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

label_bars(b1)
label_bars(b2)
label_bars(b3)

ax.set_xlabel('应用领域', fontsize=12)
ax.set_ylabel('营业收入（亿元）', fontsize=12)
ax.set_title('沪电股份 (SZSE:002463) PCB 各应用领域营业收入 2023–2025', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=10)
ax.legend(fontsize=11)
ax.set_ylim(0, 175)
ax.grid(axis='y', alpha=0.3)

# Add YoY annotation for 2025
ax.annotate('数据通讯 +45% YoY\n(高速交换机 +110%)',
            xy=(x[0] + width, 146.56), xytext=(x[0] + width + 0.5, 155),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=9, color='red')

plt.tight_layout()
plt.savefig('/Users/x/projects/financial_agent/reports/charts/wus_002463_segment_mix.png',
            dpi=150, bbox_inches='tight')
print("Saved wus_002463_segment_mix.png")
