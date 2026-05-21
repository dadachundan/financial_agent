"""Charts for 中科曙光 SSE:603019 company research report."""
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# Configure Chinese font (PingFang on macOS)
mpl.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def chart_revenue_gm():
    """5-year revenue and gross margin trend, dual axis."""
    years = ['2021', '2022', '2023', '2024', '2025']
    revenue_bn = [112.69, 130.08, 143.53, 131.48, 149.64]  # 亿元
    # gross margin computed from营业成本 / 营业收入 of 主营业务: 2021 ~22.9%, 2022 23.7%, 2023 26.3%, 2024 29.2%, 2025 30.6%
    # FY2024 rev 131.48, cost 93.14 => GM 29.16%; FY2025 rev 149.64, cost 103.87 => GM 30.59%
    gm = [22.9, 23.5, 26.26, 29.16, 30.59]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    bars = ax1.bar(years, revenue_bn, color='#3B7DD8', alpha=0.85, label='营业收入 (亿元)')
    ax1.set_ylabel('营业收入 (人民币亿元)', color='#3B7DD8', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#3B7DD8')
    ax1.set_ylim(0, 180)
    for b, v in zip(bars, revenue_bn):
        ax1.text(b.get_x() + b.get_width() / 2, v + 2, f'{v:.1f}', ha='center', fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(years, gm, color='#E07B00', marker='o', linewidth=2.4, label='综合毛利率 (%)')
    ax2.set_ylabel('综合毛利率 (%)', color='#E07B00', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#E07B00')
    ax2.set_ylim(15, 38)
    for x, y in zip(years, gm):
        ax2.text(x, y + 0.8, f'{y:.1f}%', ha='center', color='#E07B00', fontsize=9)

    plt.title('中科曙光 2021–2025 营业收入与毛利率', fontsize=13)
    fig.tight_layout()
    out = os.path.join(OUT, 'sugon_revenue_gm.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', out)


def chart_segment_mix():
    """FY2025 segment revenue mix — by product (IT设备 vs 软件/集成/服务) and by sector (公共事业 vs 企业)."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # By product
    labels1 = ['IT 设备', '软件开发/系统集成/技术服务']
    vals1 = [125.03, 24.46]  # 亿元
    colors1 = ['#3B7DD8', '#E07B00']
    axes[0].pie(vals1, labels=labels1, autopct='%1.1f%%', startangle=90,
                colors=colors1, textprops={'fontsize': 10})
    axes[0].set_title('2025 主营收入分产品 (合计 149.49 亿元)', fontsize=12)

    # By sector
    labels2 = ['公共事业', '企业']
    vals2 = [77.13, 72.37]
    colors2 = ['#4DAF7C', '#9F7AEA']
    axes[1].pie(vals2, labels=labels2, autopct='%1.1f%%', startangle=90,
                colors=colors2, textprops={'fontsize': 10})
    axes[1].set_title('2025 主营收入分行业', fontsize=12)

    fig.tight_layout()
    out = os.path.join(OUT, 'sugon_segment_mix.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', out)


def chart_rd_intensity():
    """R&D spend and R&D-to-revenue ratio."""
    years = ['2021', '2022', '2023', '2024', '2025']
    rd_bn = [9.31, 11.05, 13.16, 12.92, 16.71]  # 亿元 (研发投入)
    rd_pct = [8.26, 8.49, 9.17, 9.83, 10.95]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    bars = ax1.bar(years, rd_bn, color='#9F7AEA', alpha=0.85)
    ax1.set_ylabel('研发投入 (人民币亿元)', color='#9F7AEA', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#9F7AEA')
    ax1.set_ylim(0, 22)
    for b, v in zip(bars, rd_bn):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.3, f'{v:.2f}', ha='center', fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(years, rd_pct, color='#E54B4B', marker='s', linewidth=2.4)
    ax2.set_ylabel('研发投入占营收比例 (%)', color='#E54B4B', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#E54B4B')
    ax2.set_ylim(5, 14)
    for x, y in zip(years, rd_pct):
        ax2.text(x, y + 0.2, f'{y:.2f}%', ha='center', color='#E54B4B', fontsize=9)

    plt.title('中科曙光研发投入与强度 (2021–2025)', fontsize=13)
    fig.tight_layout()
    out = os.path.join(OUT, 'sugon_rd_intensity.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', out)


def chart_associate_contribution():
    """Investment income from associates vs. core profit — Hygon impact illustration."""
    years = ['2021', '2022', '2023', '2024', '2025']
    invest_income_bn = [4.43, 5.31, 7.55, 5.63, 6.83]  # 投资收益, 亿元 (annual reports)
    net_income_bn = [11.76, 15.44, 18.36, 19.11, 21.76]
    core_ex_invest = [a - b for a, b in zip(net_income_bn, invest_income_bn)]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(years, core_ex_invest, label='归母净利润 - 投资收益', color='#3B7DD8', alpha=0.85)
    ax.bar(years, invest_income_bn, bottom=core_ex_invest, label='投资收益 (含海光信息等)', color='#E07B00', alpha=0.85)
    ax.set_ylabel('人民币亿元', fontsize=11)
    ax.set_title('归母净利润中投资收益 (主要来自海光信息) 占比，2021–2025', fontsize=13)
    ax.legend(loc='upper left', fontsize=10)
    for i, (c, inv, ni) in enumerate(zip(core_ex_invest, invest_income_bn, net_income_bn)):
        ax.text(i, ni + 0.3, f'{inv / ni * 100:.0f}%\n投资收益', ha='center', fontsize=8, color='#E07B00')
    fig.tight_layout()
    out = os.path.join(OUT, 'sugon_associate_contribution.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', out)


def chart_valuation():
    """Sugon TTM P/E vs Chinese AI/HPC peers — approximate market data."""
    names = ['中科曙光\n603019', '海光信息\n688041', '浪潮信息\n000977', '中科创达\n300496', '紫光股份\n000938']
    pe = [62.7, 145.0, 25.0, 95.0, 27.0]  # approximate TTM P/E levels — clearly labelled as approx
    colors = ['#3B7DD8', '#E07B00', '#4DAF7C', '#9F7AEA', '#888888']

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(names, pe, color=colors, alpha=0.85)
    ax.set_ylabel('TTM 市盈率 (倍)', fontsize=11)
    ax.set_title('中科曙光及国产算力同业 TTM P/E (2026-05 时点近似)', fontsize=13)
    for b, v in zip(bars, pe):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f'{v:.0f}×', ha='center', fontsize=10)
    ax.axhline(y=sum(pe) / len(pe), color='red', linestyle='--', alpha=0.5, label=f'同业中位 {sum(pe) / len(pe):.0f}×')
    ax.legend()
    fig.tight_layout()
    out = os.path.join(OUT, 'sugon_valuation.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print('saved', out)


if __name__ == '__main__':
    chart_revenue_gm()
    chart_segment_mix()
    chart_rd_intensity()
    chart_associate_contribution()
    chart_valuation()
