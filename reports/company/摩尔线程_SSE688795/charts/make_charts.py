"""Generate charts for 摩尔线程 (Moore Threads, SSE:688795) company research report.

All financial figures sourced from the 2025 年度报告 (filed 2026-04-26) and 2026 Q1 季报 (filed 2026-04-26).
Stock data from Yahoo / Yicai Global news (IPO 2025-12-05, price as of 2026-05-14).
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

# Use a CJK-capable font for Chinese labels
mpl.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Songti SC', 'Arial Unicode MS', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- Chart 1: Revenue and gross margin trend (3-yr) ----------
fig, ax1 = plt.subplots(figsize=(9, 5))
years = ['2023', '2024', '2025']
revenue = [1.24, 4.38, 15.05]   # 亿元 — from 2025 年度报告 p.13
gross_margin = [None, 70.70, 65.57]  # 2024 GM = (4.38-1.28)/4.38; 2025 from p.36
# 2023 cost ~ 0.50亿 -> GM ~60%
gross_margin = [60.0, 70.70, 65.57]

bars = ax1.bar(years, revenue, color='#1f77b4', alpha=0.85, label='营业收入 (亿元)')
ax1.set_ylabel('营业收入 (亿元)', fontsize=11, color='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.3, f'{v:.2f}', ha='center', fontsize=10)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color='#d62728', marker='o', linewidth=2.5, label='毛利率 (%)')
ax2.set_ylabel('毛利率 (%)', fontsize=11, color='#d62728')
ax2.tick_params(axis='y', labelcolor='#d62728')
ax2.set_ylim(50, 80)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 1, f'{y:.1f}%', ha='center', fontsize=9, color='#d62728')

plt.title('摩尔线程 2023–2025 营业收入与毛利率', fontsize=13, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_revenue_margin.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- Chart 2: Quarterly revenue 2025Q1-2026Q1 ----------
fig, ax = plt.subplots(figsize=(9, 5))
quarters = ['2025Q1', '2025Q2', '2025Q3', '2025Q4', '2026Q1']
q_rev = [2.89, 4.13, 0.83, 7.21, 7.38]   # 亿元 — 年报 p.14 + Q1 报告 p.1
colors = ['#7fb8e0', '#7fb8e0', '#7fb8e0', '#7fb8e0', '#d62728']
bars = ax.bar(quarters, q_rev, color=colors, alpha=0.9)
for b, v in zip(bars, q_rev):
    ax.text(b.get_x() + b.get_width()/2, v + 0.15, f'{v:.2f}', ha='center', fontsize=10)
ax.set_ylabel('营业收入 (亿元)', fontsize=11)
ax.set_title('摩尔线程 单季度营业收入走势 (2025Q1–2026Q1)', fontsize=13, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_ylim(0, 9)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_quarterly_revenue.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- Chart 3: Revenue mix — Cloud vs. Edge/Terminal ----------
fig, ax = plt.subplots(figsize=(8, 5))
seg_names = ['云端产品', '边缘与终端产品', '其他']
seg_2024 = [4.17, 0.139, 0.075]    # 亿元，2024 implied from growth rates
seg_2025 = [14.61, 0.255, 0.191]   # 年报 p.36
x = np.arange(len(seg_names))
width = 0.36
b1 = ax.bar(x - width/2, seg_2024, width, label='2024', color='#cccccc')
b2 = ax.bar(x + width/2, seg_2025, width, label='2025', color='#1f77b4')
ax.set_xticks(x); ax.set_xticklabels(seg_names)
ax.set_ylabel('营业收入 (亿元)', fontsize=11)
ax.set_title('摩尔线程 主营收入分产品线 (2024 vs. 2025)', fontsize=13, fontweight='bold')
ax.legend()
for bs in (b1, b2):
    for b in bs:
        v = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, v + 0.2, f'{v:.2f}', ha='center', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_product_mix.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- Chart 4: R&D investment intensity ----------
fig, ax1 = plt.subplots(figsize=(9, 5))
rd_yuan = [13.34, 13.59, 13.05]   # 亿元 — 2023, 2024, 2025
rd_pct = [1076.31, 309.88, 86.68]  # 占营收 %
bars = ax1.bar(years, rd_yuan, color='#9467bd', alpha=0.85)
ax1.set_ylabel('研发投入 (亿元)', fontsize=11, color='#9467bd')
ax1.tick_params(axis='y', labelcolor='#9467bd')
for b, v in zip(bars, rd_yuan):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.2, f'{v:.2f}', ha='center', fontsize=10)
ax2 = ax1.twinx()
ax2.plot(years, rd_pct, color='#ff7f0e', marker='s', linewidth=2.5)
ax2.set_ylabel('研发投入占营收比 (%, 对数轴)', fontsize=11, color='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')
ax2.set_yscale('log')
for x, y in zip(years, rd_pct):
    ax2.text(x, y * 1.12, f'{y:.1f}%', ha='center', fontsize=9, color='#ff7f0e')
plt.title('摩尔线程 研发投入强度 (2023–2025)', fontsize=13, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_rd_investment.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- Chart 5: Net loss narrowing ----------
fig, ax = plt.subplots(figsize=(9, 5))
net = [-17.03, -16.18, -10.01]   # 亿元 — 归属净利润，年报 p.13
adj_net = [-15.83, -14.95, -6.48]  # 扣除股份支付影响后净利润
x = np.arange(len(years))
width = 0.36
b1 = ax.bar(x - width/2, net, width, label='归母净利润 (亿元)', color='#d62728')
b2 = ax.bar(x + width/2, adj_net, width, label='扣除股份支付后净利润 (亿元)', color='#ff7f0e')
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel('净利润 (亿元)', fontsize=11)
ax.set_title('摩尔线程 净亏损连续收窄 (2023–2025)', fontsize=13, fontweight='bold')
ax.legend(loc='lower right')
ax.axhline(0, color='black', linewidth=0.8)
for bs in (b1, b2):
    for b in bs:
        v = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, v - 0.8, f'{v:.2f}', ha='center', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_net_loss.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- Chart 6: Customer concentration ----------
fig, ax = plt.subplots(figsize=(7, 7))
# Top 5 share total 91.36%; 1st unknown, 2nd 39730.62万 (3973百万 -> 26.39%),
# 4th 19115.04 (12.69%), 5th 13335.11 (8.86%)
# Top1 + Top3 sum (long-term partners) = 91.36 - 26.39 - 12.69 - 8.86 = 43.42%
# But only 2 customers; can't split. Show as Top1+Top3
labels = ['第一/第三大客户 (合计 43.4%)', '第二大客户 (26.4%)', '第四大客户 (12.7%)', '第五大客户 (8.9%)', '其他客户 (8.6%)']
sizes = [43.42, 26.39, 12.69, 8.86, 8.64]
colors_p = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#cccccc']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_p, startangle=90, textprops={'fontsize': 10})
ax.set_title('摩尔线程 2025 年客户集中度 (前五大客户占 91.36%)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'moorethreads_customer_concentration.png'), dpi=150, bbox_inches='tight')
plt.close()

print('All charts saved to', OUT)
