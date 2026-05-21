"""Generate charts for Weichai Power (SZSE:000338) research report."""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

# Use a font that supports Chinese
for f in ["PingFang SC", "Heiti SC", "Songti SC", "STHeiti", "Arial Unicode MS"]:
    try:
        mpl.font_manager.findfont(f, fallback_to_default=False)
        mpl.rcParams["font.family"] = f
        break
    except Exception:
        continue
mpl.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def chart_revenue_margin():
    years = ["2021", "2022", "2023", "2024", "2025"]
    revenue = [2202.15, 1751.58, 2139.58, 2156.91, 2318.09]  # 亿元
    np_attr = [94.93, 49.05, 90.14, 114.03, 109.31]  # 亿元 归母净利润
    net_margin = [n / r * 100 for n, r in zip(np_attr, revenue)]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    color1 = "#1f4e79"
    color2 = "#c0504d"
    bars = ax1.bar(years, revenue, color=color1, alpha=0.85, label="营业收入")
    ax1.set_ylabel("营业收入（亿元）", color=color1, fontsize=11)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_ylim(0, max(revenue) * 1.2)
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width() / 2, v + 30, f"{v:,.0f}", ha="center", fontsize=9, color=color1)

    ax2 = ax1.twinx()
    ax2.plot(years, net_margin, color=color2, marker="o", linewidth=2.2, label="归母净利率")
    ax2.set_ylabel("归母净利率（%）", color=color2, fontsize=11)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.set_ylim(0, max(net_margin) * 1.6)
    for x, y in zip(years, net_margin):
        ax2.text(x, y + 0.25, f"{y:.2f}%", ha="center", fontsize=9, color=color2)

    plt.title("潍柴动力 2021-2025 营业收入与归母净利率", fontsize=13, pad=12)
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_revenue_margin.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_segment_mix():
    segments = ["动力总成、整车整机及关键零部件", "智慧物流（KION）", "农业装备", "其他零部件", "其他"]
    rev2024 = [897.79, 887.26, 183.45, 100.89, 87.51]
    rev2025 = [1004.11, 910.77, 187.89, 118.76, 96.57]

    x = np.arange(len(segments))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10, 5.2))
    b1 = ax.bar(x - width / 2, rev2024, width, label="2024", color="#8aa6c4")
    b2 = ax.bar(x + width / 2, rev2025, width, label="2025", color="#1f4e79")
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, v + 8, f"{v:,.0f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(segments, rotation=0, fontsize=9)
    ax.set_ylabel("收入（亿元）")
    ax.set_title("潍柴动力分产品收入：2024 vs 2025", fontsize=13, pad=10)
    ax.legend()
    ax.set_ylim(0, max(rev2025) * 1.2)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_segment_mix.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_engine_volumes():
    years = ["2022", "2023", "2024", "2025"]
    engines = [57.3, 70.7, 73.4, 74.3]   # 万台
    gearbox = [59.0, 77.0, 85.3, 91.1]
    axles = [53.0, 75.0, 80.0, 100.0]
    trucks = [9.1, 9.4, 11.8, 15.3]
    x = np.arange(len(years))
    w = 0.2
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - 1.5 * w, engines, w, label="发动机（万台）", color="#1f4e79")
    ax.bar(x - 0.5 * w, gearbox, w, label="变速箱（万台）", color="#4f81bd")
    ax.bar(x + 0.5 * w, axles, w, label="车桥（万根）", color="#9bbb59")
    ax.bar(x + 1.5 * w, trucks, w, label="陕重汽商用车（万辆）", color="#c0504d")
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("销量")
    ax.set_title("潍柴动力 2022-2025 关键零部件与整车销量", fontsize=13, pad=10)
    ax.legend(loc="upper left", fontsize=9)
    for i, vals in enumerate([engines, gearbox, axles, trucks]):
        offsets = [-1.5, -0.5, 0.5, 1.5]
        for xi, v in zip(x, vals):
            ax.text(xi + offsets[i] * w, v + 1.5, f"{v:.1f}", ha="center", fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_volumes.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_geo_mix():
    labels = ["国内", "国外"]
    rev2024 = [959.17, 1197.74]
    rev2025 = [1089.26, 1228.83]
    x = np.arange(len(labels))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7.5, 5))
    b1 = ax.bar(x - w / 2, rev2024, w, label="2024", color="#8aa6c4")
    b2 = ax.bar(x + w / 2, rev2025, w, label="2025", color="#1f4e79")
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, v + 10, f"{v:,.0f}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("收入（亿元）")
    ax.set_title("潍柴动力分地区收入：2024 vs 2025", fontsize=13, pad=10)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_geo_mix.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_peer_valuation():
    peers = ["潍柴动力\n(000338)", "中国重汽\n(000951)", "中国重汽\n(03808.HK)", "玉柴国际\n(CYD)", "康明斯\n(CMI)", "凯傲集团\n(KGX.DE)"]
    pe_ttm = [24.9, 16.5, 9.0, 8.5, 18.0, 12.0]  # 大致水平，仅作图示
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(peers, pe_ttm, color=["#c0504d", "#4f81bd", "#4f81bd", "#9bbb59", "#9bbb59", "#9bbb59"])
    for b, v in zip(bars, pe_ttm):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:.1f}x", ha="center", fontsize=10)
    ax.axhline(np.mean(pe_ttm[1:]), color="gray", linestyle="--", linewidth=1, label=f"同业平均 ≈ {np.mean(pe_ttm[1:]):.1f}x")
    ax.set_ylabel("TTM P/E（倍）")
    ax.set_title("潍柴动力与同业 TTM 市盈率对比（截至 2026-05-21）", fontsize=12, pad=10)
    ax.legend()
    ax.set_ylim(0, max(pe_ttm) * 1.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_peer_pe.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_china_heavy_truck():
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    sales = [161.9, 139.5, 67.2, 91.1, 90.1, 100.0]  # 万辆 — 中汽协口径，2025 为估计
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(years, sales, color="#4f81bd")
    for b, v in zip(bars, sales):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}", ha="center", fontsize=10)
    ax.set_ylabel("销量（万辆）")
    ax.set_title("中国重卡行业销量周期 2020-2025", fontsize=13, pad=10)
    ax.set_ylim(0, max(sales) * 1.2)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "weichai_china_heavy_truck.png"), dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    chart_revenue_margin()
    chart_segment_mix()
    chart_engine_volumes()
    chart_geo_mix()
    chart_peer_valuation()
    chart_china_heavy_truck()
    print("done")
