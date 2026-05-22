"""Charts for Horizon Robotics (HKEX:9660) company research report."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from pathlib import Path

# CJK font setup for matplotlib on macOS
plt.rcParams['font.family'] = ['PingFang HK', 'PingFang SC', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUT = Path(__file__).parent

# ---------- Chart 1: Revenue + Gross Margin Trend ----------
years = ['2021', '2022', '2023', '2024', '2025E*']
revenue = [466.7, 906.0, 1551.6, 2383.6, 3390.0]  # RMB mn
gm = [70.9, 69.3, 70.5, 77.3, 65.4]  # %  (2025E uses H1 actual)

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color='#1f77b4', alpha=0.85, label='营业收入 (RMB mn)')
ax1.set_ylabel('营业收入 (RMB 百万元)', fontsize=11)
ax1.set_xlabel('财年', fontsize=11)
ax1.set_ylim(0, max(revenue) * 1.2)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 60, f'{v:,.0f}',
             ha='center', va='bottom', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm, color='#d62728', marker='o', linewidth=2.2, label='毛利率 (%)')
ax2.set_ylabel('毛利率 (%)', fontsize=11)
ax2.set_ylim(50, 90)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
for i, v in enumerate(gm):
    ax2.text(i, v + 1.2, f'{v:.1f}%', ha='center', fontsize=9, color='#d62728')

ax1.set_title('地平线机器人：营业收入与毛利率走势 (FY2021–2025E)', fontsize=13, pad=12)
ax1.grid(axis='y', alpha=0.3)
fig.text(0.5, -0.02, '* 2025E = 公司一致预期中值 (33.9 亿元)；毛利率为 2025H1 实际值 65.4%', ha='center', fontsize=8, style='italic')
fig.tight_layout()
fig.savefig(OUT / 'horizon_revenue_gm_trend.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- Chart 2: Revenue Mix (Stacked) ----------
years2 = ['2023', '2024', '2025H1']
product = [506.4, 664.2, 777.8]
license = [964.0, 1647.5, 738.5]
nonauto = [81.2, 71.9, 50.4]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years2, product, label='产品解决方案 (车规处理硬件)', color='#1f77b4')
ax.bar(years2, license, bottom=product, label='授权及服务业务 (算法/IP/服务)', color='#ff7f0e')
ax.bar(years2, nonauto, bottom=[p+l for p, l in zip(product, license)], label='非车业务', color='#2ca02c')

for i, (p, l, n) in enumerate(zip(product, license, nonauto)):
    total = p + l + n
    ax.text(i, total + 50, f'{total:,.0f}', ha='center', fontsize=10, fontweight='bold')
    if p > 100:
        ax.text(i, p/2, f'{p:.0f}\n({p/total*100:.0f}%)', ha='center', va='center', color='white', fontsize=9)
    if l > 100:
        ax.text(i, p + l/2, f'{l:.0f}\n({l/total*100:.0f}%)', ha='center', va='center', color='white', fontsize=9)

ax.set_ylabel('收入 (RMB 百万元)', fontsize=11)
ax.set_title('地平线机器人：分业务收入结构', fontsize=13, pad=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 3000)
fig.tight_layout()
fig.savefig(OUT / 'horizon_revenue_mix.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- Chart 3: Journey-series Shipments ----------
years3 = ['2020', '2021', '2022', '2023', '2024', '2025E']
ship = [0.05, 0.4, 1.0, 2.3, 5.0, 10.0]  # million units (cumulative)
annual = [0.05, 0.35, 0.6, 1.3, 2.7, 5.0]  # est. annual

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years3, annual, color='#1f77b4', alpha=0.85, label='当年出货 (估计)')
ax.plot(years3, ship, color='#d62728', marker='s', linewidth=2.5, label='累计出货')
for i, v in enumerate(ship):
    ax.text(i, v + 0.3, f'{v}M', ha='center', fontsize=9, color='#d62728', fontweight='bold')
ax.set_ylabel('征程系列处理硬件出货量 (百万套)', fontsize=11)
ax.set_xlabel('年份', fontsize=11)
ax.set_title('地平线机器人：征程系列车规芯片累计出货突破 1,000 万套 (2020–2025E)', fontsize=12, pad=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)
fig.text(0.5, -0.02, '* 2025E 累计出货量于 2025 年 8 月正式突破 1,000 万套；当年出货数据为估计值', ha='center', fontsize=8, style='italic')
fig.tight_layout()
fig.savefig(OUT / 'horizon_shipments.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- Chart 4: China ADAS / NOA Chip Market Share 2025 ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# Left: ADAS (front-camera/light-domain) market — Chinese autos
adas_labels = ['地平线', 'Mobileye', '其他', '德州仪器', 'Black\nSesame', '其他厂商']
adas_share = [47.7, 27.5, 8.0, 5.5, 5.0, 6.3]
colors1 = ['#d62728', '#1f77b4', '#7f7f7f', '#2ca02c', '#9467bd', '#bcbd22']
axes[0].pie(adas_share, labels=[f'{l}\n{v:.1f}%' for l, v in zip(adas_labels, adas_share)],
            colors=colors1, startangle=90, textprops={'fontsize': 9})
axes[0].set_title('2025 中国自主品牌\nADAS 芯片市场份额', fontsize=11, fontweight='bold')

# Right: Urban NOA market
noa_labels = ['英伟达', '华为', '地平线', '其他']
noa_share = [53.0, 27.0, 10.0, 10.0]
colors2 = ['#76b900', '#c00000', '#d62728', '#7f7f7f']
axes[1].pie(noa_share, labels=[f'{l}\n{v:.1f}%' for l, v in zip(noa_labels, noa_share)],
            colors=colors2, startangle=90, textprops={'fontsize': 9})
axes[1].set_title('2025 中国城区 NOA\n计算芯片市场份额', fontsize=11, fontweight='bold')

fig.suptitle('中国智驾芯片市场格局 — ADAS "一超" vs. NOA "三强"', fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(OUT / 'horizon_market_share.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- Chart 5: Peer Valuation Comparison (PS-TTM) ----------
peers = ['地平线\n(9660.HK)', 'Mobileye\n(MBLY)', 'Ambarella\n(AMBA)', 'Black\nSesame\n(2533.HK)', 'NVIDIA\n(NVDA)']
ps_ttm = [23.0, 7.5, 9.5, 18.0, 30.0]  # approximate TTM P/S
revenue_growth = [53.6, -10.0, 25.0, 50.0, 95.0]  # YoY growth

x = np.arange(len(peers))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 5))
bars1 = ax1.bar(x - width/2, ps_ttm, width, label='TTM P/S (x)', color='#1f77b4')
ax1.set_ylabel('TTM P/S 市销率 (x)', color='#1f77b4', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
for b, v in zip(bars1, ps_ttm):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.4, f'{v:.1f}x',
             ha='center', fontsize=9, color='#1f77b4')

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, revenue_growth, width, label='收入同比增速 (%)', color='#ff7f0e', alpha=0.8)
ax2.set_ylabel('收入同比增速 (%)', color='#ff7f0e', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#ff7f0e')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
for b, v in zip(bars2, revenue_growth):
    ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 2, f'{v:.0f}%',
             ha='center', fontsize=9, color='#ff7f0e')

ax1.set_xticks(x)
ax1.set_xticklabels(peers, fontsize=10)
ax1.set_title('地平线 vs. 全球智驾/自动驾驶芯片同行：估值与增速对比', fontsize=12, pad=12)
ax1.grid(axis='y', alpha=0.3)
fig.text(0.5, -0.02, '估值数据为 2026 年 5 月 stockanalysis.com / Yahoo Finance TTM；增速为最近披露年度同比', ha='center', fontsize=8, style='italic')
fig.tight_layout()
fig.savefig(OUT / 'horizon_peer_valuation.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- Chart 6: China ADAS/NOA Market Size Forecast ----------
years6 = ['2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E', '2030E']
adas_pen = [25, 38, 51, 59, 67, 73, 78, 85]  # ADAS penetration in new car sales (%)
noa_pen = [3, 8, 20, 32, 45, 55, 62, 72]  # mid-high NOA penetration (%)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(years6, adas_pen, marker='o', linewidth=2.5, color='#1f77b4', label='辅助驾驶 (ADAS) 渗透率')
ax.plot(years6, noa_pen, marker='s', linewidth=2.5, color='#d62728', label='中高阶辅助驾驶 (高速+城区 NOA) 渗透率')
ax.fill_between(years6, adas_pen, alpha=0.1, color='#1f77b4')
ax.fill_between(years6, noa_pen, alpha=0.1, color='#d62728')

for i, (a, n) in enumerate(zip(adas_pen, noa_pen)):
    ax.text(i, a + 2, f'{a}%', ha='center', fontsize=9, color='#1f77b4')
    ax.text(i, n + 2, f'{n}%', ha='center', fontsize=9, color='#d62728')

ax.set_ylabel('渗透率 (% 中国新乘用车销量)', fontsize=11)
ax.set_xlabel('年份', fontsize=11)
ax.set_title('中国乘用车智能驾驶功能渗透率快速提升', fontsize=12, pad=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
fig.text(0.5, -0.02, '数据来源：地平线 2024 年报、2025 中报披露的行业数据；2026E 之后为研究机构汇总估计', ha='center', fontsize=8, style='italic')
fig.tight_layout()
fig.savefig(OUT / 'horizon_market_tam.png', dpi=150, bbox_inches='tight')
plt.close(fig)

print('Charts written to:', OUT)
for p in sorted(OUT.glob('horizon_*.png')):
    print(' -', p.name)
