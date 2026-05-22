"""Charts for 生益科技 SSE:600183 company research report."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'STHeiti', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.dirname(os.path.abspath(__file__))

# -------- Chart 1: Revenue + GM trend (2020-2025) --------
years = ['2020', '2021', '2022', '2023', '2024', '2025']
rev = [146.87, 202.74, 180.14, 165.86, 203.88, 284.31]   # 亿元
np_attr = [16.81, 28.30, 15.31, 11.64, 17.39, 33.34]      # 亿元
# Approximate consolidated GM, derived from product GM mix
gm = [25.7, 26.5, 17.5, 18.4, 20.6, 25.1]                  # %

fig, ax1 = plt.subplots(figsize=(10, 5.2))
x = np.arange(len(years))
b1 = ax1.bar(x - 0.2, rev, width=0.4, label='营业收入 (亿元)', color='#1f77b4')
b2 = ax1.bar(x + 0.2, np_attr, width=0.4, label='归母净利润 (亿元)', color='#2ca02c')
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel('金额 (亿元 RMB)')
ax1.set_ylim(0, 320)
for r, v in zip(b1, rev):
    ax1.text(r.get_x()+r.get_width()/2, v+4, f'{v:.0f}', ha='center', fontsize=8)
for r, v in zip(b2, np_attr):
    ax1.text(r.get_x()+r.get_width()/2, v+4, f'{v:.1f}', ha='center', fontsize=8)

ax2 = ax1.twinx()
ax2.plot(x, gm, color='#d62728', marker='o', linewidth=2, label='毛利率 (%)')
ax2.set_ylabel('毛利率 (%)')
ax2.set_ylim(10, 32)
for xi, v in zip(x, gm):
    ax2.text(xi, v+0.6, f'{v:.1f}%', ha='center', fontsize=8, color='#d62728')

ax1.set_title('生益科技 2020–2025 营收 / 归母净利润 / 毛利率')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_revenue_gm.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 2: 2025 Segment revenue mix --------
seg_labels = ['覆铜板+粘结片\n(CCL & Prepreg)', '印制电路板\n(PCB, 生益电子)', '废弃资源利用\n(湖南绿晟)', '房地产 (尾盘)']
seg_vals = [177.74, 91.44, 8.55, 0.94]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
fig, ax = plt.subplots(figsize=(8.5, 5.5))
wedges, texts, autotexts = ax.pie(seg_vals, labels=seg_labels, autopct='%1.1f%%',
                                   colors=colors, startangle=90, textprops={'fontsize': 10})
ax.set_title('生益科技 2025 主营收入结构 (合计 RMB 278.67 亿)')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_segment_mix.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 3: Quarterly revenue / NP trend 2024-2026Q1 --------
quarters = ['1Q24','2Q24','3Q24','4Q24','1Q25','2Q25','3Q25','4Q25','1Q26']
rev_q = [44.23, 52.06, 51.15, 56.44, 56.11, 70.69, 79.34, 78.18, 81.41]    # 亿元
np_q  = [3.92, 5.40, 4.40, 3.66, 5.64, 8.63, 10.17, 8.91, 11.58]            # 亿元
fig, ax1 = plt.subplots(figsize=(11, 5.2))
x = np.arange(len(quarters))
ax1.bar(x-0.2, rev_q, width=0.4, color='#1f77b4', label='营业收入 (亿元)')
ax1.bar(x+0.2, np_q,  width=0.4, color='#2ca02c', label='归母净利润 (亿元)')
ax1.set_xticks(x); ax1.set_xticklabels(quarters, rotation=0)
ax1.set_ylabel('金额 (亿元 RMB)')
ax1.set_title('生益科技 单季营收 / 归母净利润 (2024Q1–2026Q1)')
for xi, (r, n) in enumerate(zip(rev_q, np_q)):
    ax1.text(xi-0.2, r+1.0, f'{r:.1f}', ha='center', fontsize=8)
    ax1.text(xi+0.2, n+1.0, f'{n:.1f}', ha='center', fontsize=8)
ax1.legend(loc='upper left', frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_quarterly.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 4: Production capacity by plant (2025 CCL sqm production) --------
plants = ['苏州生益', '陕西生益', '松山湖+东莞\n(本部, 余额)', '江西生益', '其他/生益泰国']
prod_sqm = [3491.13, 3255.92, 7367.22, 1698.92, 0]
# Actually total 15813.19; sum so far: 3491.13+3255.92+1698.92=8446. Remainder 7367.22 = 松山湖+东莞 (本部) — single largest
labels_pct = [f'{v:.0f} 万㎡\n({v/15813.19*100:.1f}%)' for v in prod_sqm[:4]]
fig, ax = plt.subplots(figsize=(9, 5))
plants4 = plants[:4]; prod4 = prod_sqm[:4]
order = sorted(range(4), key=lambda i: -prod4[i])
plants_s = [plants4[i] for i in order]
prod_s = [prod4[i] for i in order]
bars = ax.barh(plants_s, prod_s, color=['#1f77b4','#ff7f0e','#2ca02c','#d62728'])
for b, v in zip(bars, prod_s):
    ax.text(v+80, b.get_y()+b.get_height()/2, f'{v:,.0f} 万㎡', va='center', fontsize=10)
ax.set_xlabel('2025 年覆铜板产量 (万平方米)')
ax.set_title('生益科技 2025 年各基地刚性覆铜板产量 (合计 15,813 万㎡)')
ax.set_xlim(0, 8500)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_capacity.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 5: Global CCL market share (2024, Prismark) --------
labels = ['建滔积层板 Kingboard', '生益科技 Shengyi', '南亚塑胶 Nan Ya', '台光电子 EMC', '松下 Panasonic', 'ITEQ 联茂', 'Doosan', 'Isola', '其他']
shares = [19.5, 13.7, 8.0, 6.5, 5.5, 5.0, 4.0, 2.5, 35.3]
explode = [0.02, 0.08, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0]
fig, ax = plt.subplots(figsize=(9, 6.5))
colors_p = plt.cm.tab20.colors[:len(labels)]
wedges, texts, autotexts = ax.pie(shares, labels=labels, autopct='%1.1f%%', startangle=90,
                                   explode=explode, colors=colors_p, textprops={'fontsize': 9})
ax.set_title('全球刚性覆铜板市场份额 (2024, 按销售额, Prismark)\n注：除生益销售额13.7%为公司披露外，其余份额为业内估算')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_market_share.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 6: PCB / CCL market growth (Prismark) --------
years_m = ['2020','2021','2022','2023','2024','2025E']
pcb_global = [69.5, 80.4, 81.7, 73.5, 73.5, 85.2]   # USD bn (Prismark, rounded)
ccl_global = [13.8, 16.4, 16.9, 13.8, 14.5, 17.5]   # USD bn (industry estimates / Prismark)

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(years_m))
ax.plot(x, pcb_global, marker='o', linewidth=2, label='全球 PCB 产值 (USD bn)', color='#1f77b4')
ax.plot(x, ccl_global, marker='s', linewidth=2, label='全球 CCL 产值 (USD bn)', color='#d62728')
ax.set_xticks(x); ax.set_xticklabels(years_m)
ax.set_ylabel('产值 (USD bn)')
ax.set_title('全球 PCB / CCL 产业产值 2020–2025E (Prismark / 业内估算)')
ax.legend(loc='upper left', frameon=False)
ax.grid(True, alpha=0.3)
for xi, v in zip(x, pcb_global):
    ax.text(xi, v+1.5, f'{v:.1f}', ha='center', fontsize=8, color='#1f77b4')
for xi, v in zip(x, ccl_global):
    ax.text(xi, v-2.5, f'{v:.1f}', ha='center', fontsize=8, color='#d62728')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_industry_size.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 7: R&D spend trend --------
rd_years = ['2021','2022','2023','2024','2025']
rd = [9.20, 8.46, 8.66, 10.92, 14.50]  # 亿元
rd_pct = [4.54, 4.70, 5.22, 5.36, 5.10]
fig, ax1 = plt.subplots(figsize=(9, 4.8))
x = np.arange(len(rd_years))
ax1.bar(x, rd, color='#1f77b4', label='研发投入 (亿元)')
for xi, v in zip(x, rd):
    ax1.text(xi, v+0.2, f'{v:.2f}', ha='center', fontsize=9)
ax1.set_xticks(x); ax1.set_xticklabels(rd_years)
ax1.set_ylabel('研发投入 (亿元 RMB)')
ax1.set_ylim(0, 17)
ax2 = ax1.twinx()
ax2.plot(x, rd_pct, marker='o', color='#d62728', linewidth=2, label='研发投入占营收 (%)')
for xi, v in zip(x, rd_pct):
    ax2.text(xi, v+0.05, f'{v:.2f}%', ha='center', fontsize=9, color='#d62728')
ax2.set_ylabel('研发投入占营收比例 (%)')
ax2.set_ylim(3, 7)
ax1.set_title('生益科技 研发投入 2021–2025')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_rd.png'), dpi=150, bbox_inches='tight')
plt.close()

# -------- Chart 8: Peer P/E comparison --------
# Approximate TTM P/E pulled around 2026-05 from Eastmoney where available; mark as approximations
peers = ['生益科技\n600183', '生益电子\n688183', '南亚新材\n688519', '华正新材\n603186', '建滔积层板\n0148.HK', '南亚塑胶\n1303.TW', 'ITEQ\n6213.TW']
pe = [70.6, 68.0, 42.0, 38.0, 12.0, 22.0, 28.0]
colors_pe = ['#d62728' if p == pe[0] else '#1f77b4' for p in pe]
fig, ax = plt.subplots(figsize=(10, 4.8))
bars = ax.bar(peers, pe, color=colors_pe)
for b, v in zip(bars, pe):
    ax.text(b.get_x()+b.get_width()/2, v+1.5, f'{v:.1f}x', ha='center', fontsize=10)
ax.set_ylabel('TTM P/E (×)')
ax.set_title('CCL / 高速线路板同业 TTM P/E 对比 (≈2026-05, 各市场行情)')
ax.set_ylim(0, 90)
ax.axhline(y=np.median(pe), color='gray', linestyle='--', alpha=0.6, label=f'中位数 {np.median(pe):.1f}x')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'shengyi_pe_peers.png'), dpi=150, bbox_inches='tight')
plt.close()

print("All charts saved.")
for f in os.listdir(OUT):
    if f.startswith('shengyi_') and f.endswith('.png'):
        print(f, os.path.getsize(os.path.join(OUT, f)))
