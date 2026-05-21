"""Charts for Ecovacs (SSE:603486) company research report."""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

import matplotlib.font_manager as fm
for path in ["/System/Library/Fonts/STHeiti Medium.ttc",
             "/System/Library/Fonts/Hiragino Sans GB.ttc"]:
    if os.path.exists(path):
        fm.fontManager.addfont(path)
plt.rcParams["font.family"] = ["Hiragino Sans", "Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def chart_revenue_gm_trend():
    """Revenue + gross margin trend, 2021-2025. Source: cninfo 年报."""
    years = ["2021", "2022", "2023", "2024", "2025"]
    revenue = [130.86, 153.25, 155.02, 165.42, 190.40]   # 亿元
    gm = [51.41, 52.13, 44.58, 46.52, 48.82]             # %  (2023 adjusted per ASC 18 reclassification)
    net_income = [20.10, 16.98, 6.12, 8.06, 17.58]       # 归母净利润 亿元

    fig, ax1 = plt.subplots(figsize=(9, 5))
    bar_color = "#2E86AB"
    line_color = "#E63946"
    line2_color = "#06A77D"

    bars = ax1.bar(years, revenue, color=bar_color, alpha=0.85, label="营业收入 (亿元)")
    ax1.set_ylabel("营业收入 (亿元)", color=bar_color, fontsize=11)
    ax1.tick_params(axis="y", labelcolor=bar_color)
    ax1.set_ylim(0, 220)
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width()/2, v + 3, f"{v:.1f}", ha="center", fontsize=9, color=bar_color)

    ax2 = ax1.twinx()
    ax2.plot(years, gm, color=line_color, marker="o", linewidth=2.2, label="综合毛利率 (%)")
    ax2.plot(years, net_income, color=line2_color, marker="s", linewidth=2.0, linestyle="--", label="归母净利润 (亿元)")
    ax2.set_ylabel("毛利率 (%) / 归母净利润 (亿元)", fontsize=11)
    ax2.set_ylim(0, 60)
    for x, v in zip(years, gm):
        ax2.text(x, v + 1.2, f"{v:.1f}%", ha="center", fontsize=9, color=line_color)
    for x, v in zip(years, net_income):
        ax2.text(x, v - 2.5, f"{v:.1f}", ha="center", fontsize=9, color=line2_color)

    ax1.set_title("科沃斯 (603486) 营收、毛利率与归母净利润趋势 (2021–2025)", fontsize=13, pad=12)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_revenue_gm_trend.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_segment_mix():
    """Segment revenue mix, 2023 vs 2024 vs 2025 — stacked bar."""
    years = ["2023", "2024", "2025"]
    # 单位: 亿元
    service_robot = [77.42, 80.82, 106.80]   # 服务机器人 (DEEBOT / WINBOT / GOAT / 商用)
    living_appliance = [76.63, 83.19, 82.19]  # 智能生活电器 (Tineco 添可)
    other = [0.97, 1.41, 1.41]                # 其他

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(years))
    width = 0.55

    p1 = ax.bar(x, service_robot, width, color="#2E86AB", label="服务机器人 (科沃斯)")
    p2 = ax.bar(x, living_appliance, width, bottom=service_robot, color="#06A77D", label="智能生活电器 (添可)")
    bottom2 = [a + b for a, b in zip(service_robot, living_appliance)]
    p3 = ax.bar(x, other, width, bottom=bottom2, color="#F4A261", label="其他")

    for i, y in enumerate(years):
        total = service_robot[i] + living_appliance[i] + other[i]
        ax.text(i, total + 3, f"合计 {total:.1f}亿", ha="center", fontsize=10, fontweight="bold")
        ax.text(i, service_robot[i]/2, f"{service_robot[i]:.1f}\n({service_robot[i]/total*100:.0f}%)",
                ha="center", va="center", fontsize=9, color="white")
        ax.text(i, service_robot[i] + living_appliance[i]/2, f"{living_appliance[i]:.1f}\n({living_appliance[i]/total*100:.0f}%)",
                ha="center", va="center", fontsize=9, color="white")

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("收入 (亿元)", fontsize=11)
    ax.set_ylim(0, 220)
    ax.set_title("科沃斯分品牌收入结构 (2023–2025)", fontsize=13, pad=10)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_segment_mix.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_geo_mix():
    """Domestic vs overseas revenue 2023-2025."""
    years = ["2023", "2024", "2025"]
    domestic = [89.81, 94.30, 101.92]   # 境内 亿元
    overseas = [65.21, 71.12, 88.47]    # 境外 亿元

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(years))
    width = 0.35
    bars1 = ax.bar(x - width/2, domestic, width, color="#264653", label="境内")
    bars2 = ax.bar(x + width/2, overseas, width, color="#E76F51", label="境外")
    for b, v in zip(bars1, domestic):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=9)
    for b, v in zip(bars2, overseas):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=9)
    # 海外占比注释
    for i, y in enumerate(years):
        pct = overseas[i] / (domestic[i] + overseas[i]) * 100
        ax.text(i, max(domestic[i], overseas[i]) + 10, f"海外占比 {pct:.1f}%", ha="center", fontsize=10,
                color="#E76F51", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("收入 (亿元)", fontsize=11)
    ax.set_ylim(0, 125)
    ax.set_title("科沃斯境内外收入结构 (2023–2025)", fontsize=13, pad=10)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_geo_mix.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_peer_valuation():
    """TTM P/E peer comparison."""
    peers = ["科沃斯\n603486", "石头科技\n688169", "极米科技\n688696", "美的集团\n000333", "莱克电气*\n603355"]
    pe = [24.58, 26.09, 29.02, 12.26, 249.49]
    mkt_cap = [398, 337, 58, 6216, 173]  # 亿元

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#E63946", "#2E86AB", "#06A77D", "#264653", "#F4A261"]
    # clip P/E to 60× for visualization
    pe_display = [min(v, 60) for v in pe]
    bars = ax.bar(peers, pe_display, color=colors, alpha=0.85)
    for b, v, raw in zip(bars, pe_display, pe):
        label = f"{raw:.1f}×" if raw < 100 else f"{raw:.0f}× (盈利低基数)"
        ax.text(b.get_x() + b.get_width()/2, v + 1, label, ha="center", fontsize=10, fontweight="bold")

    ax.set_ylabel("TTM P/E (×)", fontsize=11)
    ax.set_ylim(0, 70)
    ax.axhline(y=24.58, color="#E63946", linestyle="--", alpha=0.5, label="科沃斯当前 P/E")
    ax.set_title("科沃斯 vs. 可比公司 — TTM 市盈率比较 (2026-05-21 收盘)", fontsize=13, pad=10)
    ax.text(0.99, 0.97, "* 莱克电气 P/E 受 2024 一次性减值拖累，参考意义有限",
            transform=ax.transAxes, ha="right", va="top", fontsize=8, style="italic", alpha=0.7)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_peer_valuation.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_global_robovac_market():
    """Global robot vacuum shipment forecast."""
    years = ["2022", "2023", "2024", "2025", "2026E", "2027E"]
    shipments = [1850, 1920, 2060, 2412, 2750, 3100]  # 万台

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#2E86AB"] * 4 + ["#A8DADC"] * 2
    bars = ax.bar(years, shipments, color=colors, alpha=0.9)
    for b, v in zip(bars, shipments):
        ax.text(b.get_x() + b.get_width()/2, v + 50, f"{v:,}", ha="center", fontsize=10)
    # YoY growth
    for i in range(1, len(shipments)):
        yoy = (shipments[i] / shipments[i-1] - 1) * 100
        ax.text(i, shipments[i]/2, f"+{yoy:.1f}%", ha="center", va="center",
                fontsize=10, color="white", fontweight="bold")

    ax.set_ylabel("全球扫地机器人出货量 (万台)", fontsize=11)
    ax.set_ylim(0, 3500)
    ax.set_title("全球扫地机器人市场出货量 (IDC 历史 + 行业一致预期)", fontsize=13, pad=10)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_robovac_tam.png"), dpi=150, bbox_inches="tight")
    plt.close()


def chart_unit_shipments():
    """Ecovacs vs Tineco unit shipments 2023-2025."""
    years = ["2023", "2024", "2025"]
    ecovacs = [284, 295, 440]   # 万台 — 科沃斯品牌服务机器人
    tineco = [559, 414, 451]    # 万台 — 添可洗地机 (估算自 2024 销售量与同比)

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(years))
    width = 0.35
    bars1 = ax.bar(x - width/2, ecovacs, width, color="#2E86AB", label="科沃斯品牌服务机器人")
    bars2 = ax.bar(x + width/2, tineco, width, color="#06A77D", label="添可品牌洗地机")
    for b, v in zip(bars1, ecovacs):
        ax.text(b.get_x()+b.get_width()/2, v+8, f"{v}", ha="center", fontsize=10)
    for b, v in zip(bars2, tineco):
        ax.text(b.get_x()+b.get_width()/2, v+8, f"{v}", ha="center", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("全球出货量 (万台)", fontsize=11)
    ax.set_title("科沃斯双品牌全球出货量趋势 (2023–2025)", fontsize=13, pad=10)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 700)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "ecovacs_unit_shipments.png"), dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    chart_revenue_gm_trend()
    chart_segment_mix()
    chart_geo_mix()
    chart_peer_valuation()
    chart_global_robovac_market()
    chart_unit_shipments()
    print("ok")
