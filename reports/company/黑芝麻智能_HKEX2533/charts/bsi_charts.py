"""Charts for 黑芝麻智能 HKEX:2533 company research report."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'STHeiti', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.dirname(__file__)


def chart_revenue_gm():
    """Revenue + gross margin trend, FY2021-FY2025 (FY2025 = full year per 业绩预告)."""
    years = ['2021', '2022', '2023', '2024', '2025E']
    revenue = [60.5, 165.4, 312.4, 474.3, 822.0]  # RMB mn (FY2025 from 业绩预告 ~8.22亿)
    gm = [36.2, 29.4, 24.7, 41.1, 41.0]  # %; FY2025 = 3.37/8.22 ≈ 41%

    fig, ax1 = plt.subplots(figsize=(9, 5))
    bars = ax1.bar(years, revenue, color='#2E5C8A', alpha=0.85, label='收入 (RMB mn)')
    ax1.set_ylabel('收入 (人民币百万元)', fontsize=11, color='#2E5C8A')
    ax1.tick_params(axis='y', labelcolor='#2E5C8A')
    ax1.set_ylim(0, max(revenue) * 1.18)
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width() / 2, v + 18, f'{v:.0f}', ha='center', fontsize=9, color='#2E5C8A')

    ax2 = ax1.twinx()
    ax2.plot(years, gm, color='#D94F2A', marker='o', linewidth=2.2, label='毛利率 %')
    ax2.set_ylabel('毛利率 (%)', fontsize=11, color='#D94F2A')
    ax2.tick_params(axis='y', labelcolor='#D94F2A')
    ax2.set_ylim(0, 60)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    for i, v in enumerate(gm):
        ax2.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=9, color='#D94F2A')

    plt.title('黑芝麻智能 (HKEX:2533) 收入与毛利率走势  FY2021–FY2025E', fontsize=12, pad=12)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_revenue_gm.png'), dpi=150, bbox_inches='tight')
    plt.close()


def chart_segment_mix():
    """Revenue mix: 辅助驾驶 vs 智能影像."""
    years = ['2023', '2024', '1H25']
    ad = [276.3, 438.0, 236.8]
    img = [36.1, 36.3, 16.1]

    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.55
    ax.bar(years, ad, width, label='辅助驾驶产品及解决方案', color='#2E5C8A')
    ax.bar(years, img, width, bottom=ad, label='智能影像解决方案', color='#7FB069')

    for i, (a, im) in enumerate(zip(ad, img)):
        ax.text(i, a / 2, f'{a:.0f}\n({a/(a+im)*100:.0f}%)', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
        ax.text(i, a + im / 2, f'{im:.0f}', ha='center', va='center', color='white', fontsize=9)

    ax.set_ylabel('收入 (人民币百万元)', fontsize=11)
    ax.set_title('黑芝麻智能 分部收入构成  FY2023–1H2025', fontsize=12, pad=10)
    ax.legend(loc='upper left', fontsize=10)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_segment_mix.png'), dpi=150, bbox_inches='tight')
    plt.close()


def chart_opex_burn():
    """R&D + opex vs revenue showing the gap."""
    years = ['2021', '2022', '2023', '2024', '1H25']
    revenue = [60.5, 165.4, 312.4, 474.3, 252.9]
    rd = [595.4, 765.6, 1362.5, 1435.2, 618.1]
    op_loss = [722.7, 1052.8, 1696.9, 1754.0, 771.3]

    x = np.arange(len(years))
    width = 0.27
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width, revenue, width, label='收入', color='#2E5C8A')
    ax.bar(x, rd, width, label='研发开支', color='#D94F2A')
    ax.bar(x + width, op_loss, width, label='经营亏损', color='#888888')

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel('人民币百万元', fontsize=11)
    ax.set_title('黑芝麻智能 研发投入与经营亏损 vs 收入', fontsize=12, pad=10)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_burn.png'), dpi=150, bbox_inches='tight')
    plt.close()


def chart_peer_revenue():
    """Peer revenue comparison FY2024 (RMB mn)."""
    peers = ['英伟达\nDRIVE\n(中国估)', '地平线\n(09660)', '华为\nMDC', '黑芝麻智能\n(02533)', '寒武纪\n(688256)', '蔚来NIO\n神玑*']
    # FY2024 revenue, RMB mn — auto/SoC related only
    rev = [None, 2384, None, 474, 1174, None]  # None where not disclosed
    colors = ['#888', '#D94F2A', '#888', '#2E5C8A', '#7FB069', '#888']
    fig, ax = plt.subplots(figsize=(9, 5))
    valid_idx = [i for i, r in enumerate(rev) if r is not None]
    ax.bar([peers[i] for i in valid_idx], [rev[i] for i in valid_idx], color=[colors[i] for i in valid_idx])
    for i, idx in enumerate(valid_idx):
        ax.text(i, rev[idx] + 50, f'{rev[idx]:,.0f}', ha='center', fontsize=10)
    ax.set_ylabel('FY2024 智驾相关收入 (人民币百万元)', fontsize=11)
    ax.set_title('国内智驾芯片公司收入对比  FY2024 (按披露口径)', fontsize=12, pad=10)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_peer_revenue.png'), dpi=150, bbox_inches='tight')
    plt.close()


def chart_tam():
    """ADAS / 智能驾驶 China market size 2020-2030."""
    years = list(range(2020, 2031))
    # Source: 共研网 / 华经 / 沙利文 综合，单位 RMB bn
    sizes = [21.6, 38.0, 62.0, 75.0, 91.2, 122.7, 165.0, 220.0, 285.0, 350.0, 420.0]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(years, sizes, alpha=0.3, color='#2E5C8A')
    ax.plot(years, sizes, color='#2E5C8A', marker='o', linewidth=2.2)
    for i, v in enumerate(sizes):
        if i % 2 == 0:
            ax.text(years[i], v + 12, f'{v:.0f}', ha='center', fontsize=9)
    ax.set_ylabel('市场规模 (人民币 十亿元)', fontsize=11)
    ax.set_xlabel('年份', fontsize=11)
    ax.set_title('中国智能驾驶解决方案市场规模  2020–2030E\n(CAGR≈35%,含 ADAS、域控制器、L2+/L3 系统)', fontsize=12, pad=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_tam.png'), dpi=150, bbox_inches='tight')
    plt.close()


def chart_market_share():
    """2024 China 智驾芯片 market share (装机量口径)."""
    labels = ['英伟达 Orin', '特斯拉 FSD', '华为 昇腾', 'Mobileye', '地平线', '黑芝麻 / 其他']
    shares = [32.6, 26.8, 9.6, 8.7, 8.0, 14.3]
    colors = ['#76B900', '#000000', '#C7000A', '#0096D6', '#D94F2A', '#888888']
    fig, ax = plt.subplots(figsize=(8, 5.5))
    explode = [0, 0, 0, 0, 0, 0.08]
    wedges, texts, autotexts = ax.pie(shares, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, explode=explode, textprops={'fontsize': 10})
    for t in autotexts:
        t.set_color('white')
        t.set_fontweight('bold')
    ax.set_title('2024 年中国乘用车智驾 SoC 装机量份额\n(来源：盖世汽车 / 高工智能汽车，黑芝麻仍处早期放量阶段)', fontsize=11, pad=15)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, 'bsi_market_share.png'), dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    chart_revenue_gm()
    chart_segment_mix()
    chart_opex_burn()
    chart_peer_revenue()
    chart_tam()
    chart_market_share()
    print("Charts generated in", OUT)
