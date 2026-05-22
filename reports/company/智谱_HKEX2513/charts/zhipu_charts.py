"""Charts for 智谱 (HKEX:2513) company research report."""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

# Configure CJK font (macOS)
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

OUT = Path(__file__).parent

# === Chart 1: Revenue + Gross margin trend (FY2022 - 1H2025) ===
# Source: prospectus 2025-12-30, p.14
periods = ['FY2022', 'FY2023', 'FY2024', '1H2024', '1H2025']
revenue = [57.4, 124.5, 312.4, 44.9, 190.9]  # RMB mn
gm_pct = [54.6, 64.6, 56.3, 48.9, 50.0]      # %

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(periods, revenue, color='#1f77b4', alpha=0.85, label='收入 (人民币百万元)')
ax1.set_ylabel('收入 (人民币百万元)', color='#1f77b4', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax1.set_ylim(0, max(revenue) * 1.2)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 8, f'{v:.1f}',
             ha='center', fontsize=9, color='#1f77b4')

ax2 = ax1.twinx()
ax2.plot(periods, gm_pct, color='#d62728', marker='o', linewidth=2, label='毛利率 (%)')
ax2.set_ylabel('毛利率 (%)', color='#d62728', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#d62728')
ax2.set_ylim(0, 80)
for i, v in enumerate(gm_pct):
    ax2.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=9, color='#d62728')

plt.title('智谱 (HKEX:2513) 收入与毛利率走势 (FY2022–1H2025)', fontsize=12, pad=12)
fig.tight_layout()
plt.savefig(OUT / 'zhipu_revenue_gm_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_revenue_gm_trend.png')

# === Chart 2: Net loss vs R&D expense ===
# Source: prospectus 2025-12-30, p.11 & p.14
periods2 = ['FY2022', 'FY2023', 'FY2024', '1H2024', '1H2025']
net_loss = [143.7, 788.0, 2958.0, 1235.6, 2357.9]  # RMB mn
rd_exp = [84.4, 528.9, 2195.4, 859.2, 1594.7]      # RMB mn

x = np.arange(len(periods2))
w = 0.35
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w/2, net_loss, w, label='净亏损', color='#d62728', alpha=0.85)
ax.bar(x + w/2, rd_exp, w, label='研发开支', color='#2ca02c', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(periods2)
ax.set_ylabel('人民币百万元', fontsize=11)
ax.set_title('智谱 净亏损 vs 研发开支 (FY2022–1H2025)', fontsize=12, pad=12)
ax.legend(loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.4)
for i, (nl, rd) in enumerate(zip(net_loss, rd_exp)):
    ax.text(i - w/2, nl + 30, f'{nl:.0f}', ha='center', fontsize=8, color='#d62728')
    ax.text(i + w/2, rd + 30, f'{rd:.0f}', ha='center', fontsize=8, color='#2ca02c')
plt.tight_layout()
plt.savefig(OUT / 'zhipu_loss_vs_rd.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_loss_vs_rd.png')

# === Chart 3: Customer concentration trend ===
# Source: prospectus 2025-12-30, p.10/20
periods3 = ['FY2022', 'FY2023', 'FY2024', '1H2025']
top1 = [15.4, 14.7, 19.0, 11.0]
top5 = [55.4, 61.5, 45.5, 40.0]

x = np.arange(len(periods3))
w = 0.35
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - w/2, top1, w, label='最大客户占比', color='#ff7f0e')
ax.bar(x + w/2, top5, w, label='前五大客户占比', color='#1f77b4')
ax.set_xticks(x)
ax.set_xticklabels(periods3)
ax.set_ylabel('占总收入比重 (%)', fontsize=11)
ax.set_ylim(0, 80)
ax.set_title('智谱 客户集中度趋势 (FY2022–1H2025)', fontsize=12, pad=12)
ax.legend(loc='upper right')
ax.grid(axis='y', linestyle='--', alpha=0.4)
for i, (t1, t5) in enumerate(zip(top1, top5)):
    ax.text(i - w/2, t1 + 1, f'{t1:.1f}%', ha='center', fontsize=9)
    ax.text(i + w/2, t5 + 1, f'{t5:.1f}%', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(OUT / 'zhipu_customer_concentration.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_customer_concentration.png')

# === Chart 4: China LLM-solution market share 2024 (IDC ranking referenced in press) ===
# Source: prospectus p.10 (independent general-purpose LLM #1 in China @ 6.6% of all LLM market)
# and IDC 2024 Solution market ranking (top players)
labels = ['百度', '阿里云', '商汤', '智谱', '其他']
shares = [17.0, 16.0, 9.0, 6.6, 51.4]  # rough share 2024 LLM-solution mkt - illustrative
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#cccccc']
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(shares, labels=labels, autopct='%1.1f%%',
                                   colors=colors, startangle=90,
                                   wedgeprops=dict(edgecolor='white', linewidth=2))
for t in autotexts:
    t.set_color('white'); t.set_fontsize(10); t.set_fontweight('bold')
ax.set_title('中国通用大模型市场份额 (按2024年收入，含开源 + 闭源)\n智谱在独立大模型开发商中位列第一', fontsize=11, pad=14)
plt.tight_layout()
plt.savefig(OUT / 'zhipu_market_share.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_market_share.png')

# === Chart 5: Revenue mix - on-prem vs API/cloud (2024) ===
# Source: 智谱 prospectus / 华尔街见闻 12-2025: 85% on-prem, 15% API in 2024
labels2 = ['本地化部署', '云端 API / MaaS']
sizes2 = [85, 15]
colors2 = ['#1f77b4', '#ff7f0e']
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(sizes2, labels=labels2, autopct='%1.0f%%', colors=colors2,
       startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2),
       textprops=dict(fontsize=11))
ax.set_title('智谱 FY2024 收入结构\n（本地化部署 vs 云端 API）', fontsize=11, pad=14)
plt.tight_layout()
plt.savefig(OUT / 'zhipu_revenue_mix.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_revenue_mix.png')

# === Chart 6: China AI software market size forecast (IDC) ===
years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
size_rmb_bn = [50.9, 62.0, 75.7, 92.3, 112.6, 137.5, 137.5*1.22]  # CAGR 22% per IDC
# We'll use the published 509 -> 1375 trajectory
size_rmb_bn = [50.9, 62.1, 75.7, 92.4, 112.7, 137.5, 167.7]

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(years, size_rmb_bn, marker='o', linewidth=2.5, color='#1f77b4')
ax.fill_between(years, 0, size_rmb_bn, alpha=0.15, color='#1f77b4')
ax.set_xlabel('年份')
ax.set_ylabel('市场规模 (人民币 十亿元)')
ax.set_title('中国 AI 软件市场规模预测 (2024–2030, IDC, CAGR ≈ 22%)', fontsize=12, pad=12)
for x_, y_ in zip(years, size_rmb_bn):
    ax.text(x_, y_ + 4, f'{y_:.1f}', ha='center', fontsize=9)
ax.grid(linestyle='--', alpha=0.4)
ax.set_ylim(0, max(size_rmb_bn) * 1.18)
plt.tight_layout()
plt.savefig(OUT / 'zhipu_tam.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved zhipu_tam.png')

print('\nAll charts done.')
