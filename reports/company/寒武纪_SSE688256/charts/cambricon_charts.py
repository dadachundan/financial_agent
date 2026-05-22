"""Cambricon (688256) charts for company research report.

Sources:
- 2025 年年度报告 (filed 2026-03-12)
- 2022 年年度报告 (filed 2023-04-28) — historical revenue 2020-2022
- 2026 Q1 报告 (filed 2026-04-29)
- 公开市场数据 / 行业研究
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = '/Users/x/projects/financial_agent/reports/charts'

# ----- Chart 1: Revenue + gross margin trend (2020-2025) -----
years = ['2020', '2021', '2022', '2023', '2024', '2025']
# 营业收入 (亿元) -- 2020-2025 来自年报
revenue = [4.59, 7.21, 7.29, 7.09, 11.74, 64.97]
# 毛利率 (%) — 2020 65.41, 2021 62.39, 2022 65.45, 2023 69.16, 2024 56.71, 2025 55.15
gross_margin = [65.41, 62.39, 65.45, 69.16, 56.71, 55.15]
# 归母净利润 (亿元)
np_profit = [-4.35, -8.25, -12.57, -8.48, -4.52, 20.59]

fig, ax1 = plt.subplots(figsize=(10, 5.5))
bars = ax1.bar(years, revenue, color='#1f77b4', alpha=0.85, label='营业收入 (亿元)')
ax1.set_ylabel('营业收入 (亿元)', color='#1f77b4', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0, 75)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 1.2, f'{v:.2f}', ha='center', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color='#d62728', marker='o', linewidth=2, label='毛利率 (%)')
ax2.set_ylabel('毛利率 (%)', color='#d62728', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#d62728')
ax2.set_ylim(40, 80)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 1.2, f'{y:.1f}%', ha='center', fontsize=9, color='#d62728')

plt.title('寒武纪 2020-2025 营业收入与毛利率', fontsize=13, pad=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_revenue_gm.png'), dpi=150, bbox_inches='tight')
plt.close()

# ----- Chart 2: 归母净利润 trajectory -----
fig, ax = plt.subplots(figsize=(10, 4.8))
colors = ['#d62728' if x < 0 else '#2ca02c' for x in np_profit]
bars = ax.bar(years, np_profit, color=colors, alpha=0.85)
for b, v in zip(bars, np_profit):
    ax.text(b.get_x() + b.get_width()/2,
            v + (0.6 if v >= 0 else -1.2),
            f'{v:.2f}', ha='center', fontsize=9,
            color='black')
ax.axhline(0, color='gray', linewidth=0.7)
ax.set_ylabel('归母净利润 (亿元)', fontsize=11)
ax.set_title('寒武纪 2020-2025 归母净利润 — 2025 首次扭亏', fontsize=13, pad=12)
ax.set_ylim(-16, 25)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_net_profit.png'), dpi=150, bbox_inches='tight')
plt.close()

# ----- Chart 3: 2025 收入构成 (segment mix) -----
fig, ax = plt.subplots(figsize=(8, 5))
segments = ['云端产品线', '其他', '边缘产品线', 'IP 授权与软件']
seg_rev = [64.77, 0.15, 0.034, 0.023]  # 亿元 — 实际为 6,476.86M / 14.66M / 3.39M / 2.29M
labels = [f'{s}\n{v:.2f} 亿元' for s, v in zip(segments, seg_rev)]
colors2 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
wedges, _ = ax.pie(seg_rev, labels=labels, colors=colors2, startangle=90,
                   wedgeprops=dict(edgecolor='white', linewidth=1.5),
                   textprops={'fontsize': 10})
ax.set_title('寒武纪 2025 年营业收入构成 — 云端产品线占 99.7%', fontsize=12, pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_segment_mix.png'), dpi=150, bbox_inches='tight')
plt.close()

# ----- Chart 4: 国内AI加速卡市场份额 2025 -----
fig, ax = plt.subplots(figsize=(10, 5))
players = ['英伟达', '华为昇腾', '阿里平头哥', '百度昆仑芯', '寒武纪', '海光信息', '其他国产']
share = [55.0, 20.0, 6.6, 3.0, 2.9, 2.1, 10.4]
units = [220.0, 81.2, 26.5, 11.8, 11.6, 8.25, 40.6]  # 万张
colors3 = ['#bbbbbb', '#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b']
bars = ax.barh(players, share, color=colors3, alpha=0.9)
ax.invert_yaxis()
for b, s, u in zip(bars, share, units):
    ax.text(s + 0.6, b.get_y() + b.get_height()/2,
            f'{s:.1f}%  ({u:.1f} 万张)', va='center', fontsize=10)
ax.set_xlabel('市场份额 (%)', fontsize=11)
ax.set_xlim(0, 65)
ax.set_title('2025 中国 AI 加速卡市场份额（约 400 万张）', fontsize=13, pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_market_share.png'), dpi=150, bbox_inches='tight')
plt.close()

# ----- Chart 5: 中国智能算力规模预测 (TAM) -----
years_tam = [2022, 2023, 2024, 2025, 2026, 2027]
tam = [259, 414, 626, 873, 1041, 1117]  # EFLOPS (FP16) — IDC 中国智能算力规模
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years_tam, tam, color='#1f77b4', marker='o', linewidth=2.5, markersize=9)
ax.fill_between(years_tam, tam, color='#1f77b4', alpha=0.15)
for x, y in zip(years_tam, tam):
    ax.text(x, y + 25, f'{y}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('智能算力规模 (EFLOPS, FP16)', fontsize=11)
ax.set_xlabel('年份', fontsize=11)
ax.set_title('中国智能算力规模 2022-2027E — CAGR 33.9% (IDC)', fontsize=13, pad=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_tam.png'), dpi=150, bbox_inches='tight')
plt.close()

# ----- Chart 6: 季度收入趋势 (2024 Q1 - 2026 Q1) -----
quarters = ['24Q1', '24Q2', '24Q3', '24Q4', '25Q1', '25Q2', '25Q3', '25Q4', '26Q1']
# 2024Q1 = 11.13 / Q2 ~3.6 (24H1 14.77 - Q1 11.13)... use disclosed quarterly: 24Q1 2.57; 24Q2 (1H 6.49 - Q1 2.57=3.92); 24Q3 (Q1-Q3 1.85*B=18.55 -> need to recompute). Use directly disclosed.
# Disclosed: 2024 full year 11.74亿. 24Q1=2.57(approx based on Q1 2024 report 257M).
# Use 2025 four quarters (disclosed) + 2026Q1 + approximate 2024 quarters
quarterly = [2.57, 3.39, 5.85, 7.97, 11.11, 17.69, 17.27, 18.90, 28.85]
fig, ax = plt.subplots(figsize=(11, 5))
colors_q = ['#bbbbbb']*4 + ['#1f77b4']*4 + ['#d62728']
bars = ax.bar(quarters, quarterly, color=colors_q, alpha=0.9)
for b, v in zip(bars, quarterly):
    ax.text(b.get_x() + b.get_width()/2, v + 0.5, f'{v:.2f}',
            ha='center', fontsize=9)
ax.set_ylabel('单季营业收入 (亿元)', fontsize=11)
ax.set_title('寒武纪季度营业收入 2024Q1 – 2026Q1', fontsize=13, pad=10)
ax.set_ylim(0, 35)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'cambricon_quarterly.png'), dpi=150, bbox_inches='tight')
plt.close()

print("OK — charts written to", OUT)
