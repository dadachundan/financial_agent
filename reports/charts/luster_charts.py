"""Charts for Luster LightTech (凌云光, SSE:688400) company research report.

All revenue / income figures sourced from the FY2023, FY2024 and FY2025 annual reports
filed on cninfo (the FY2024 comparatives appear on page 9 of the FY2025 AR; FY2023 from
the FY2024 AR / FY2023 AR cross-check).

Run from the project root:
    python3 reports/charts/luster_charts.py
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
plt.rcParams["font.family"] = ["Heiti TC", "Songti SC", "STHeiti", "PingFang HK", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ----- Data block (CNY mn) ---------------------------------------------------
years = ["2022", "2023", "2024", "2025"]
revenue_cnymn = [2426.0, 2640.93, 2233.78, 2911.67]   # FY22 from FY23 AR backref
gross_margin_pct = [31.7, 32.43, 34.66, 34.79]        # back-calc revenue minus cost
net_income_cnymn = [167.4, 163.93, 107.07, 161.35]    # 归母净利润, CNY mn
rd_pct = [16.51, 17.41, 19.89, 17.53]                  # R&D / revenue, %


# ----- Chart 1: revenue + gross margin trend --------------------------------
def chart_revenue_gm():
    fig, ax1 = plt.subplots(figsize=(8.6, 4.8))
    bars = ax1.bar(years, revenue_cnymn, color="#3F6BA8", alpha=0.85, label="营业收入 (人民币 百万元)")
    ax1.set_ylabel("营业收入 (人民币 百万元)", color="#3F6BA8")
    ax1.tick_params(axis="y", labelcolor="#3F6BA8")
    ax1.set_ylim(0, max(revenue_cnymn) * 1.20)
    for b, v in zip(bars, revenue_cnymn):
        ax1.text(b.get_x() + b.get_width() / 2, v + 60, f"{v:,.0f}", ha="center", fontsize=9, color="#1a1a1a")

    ax2 = ax1.twinx()
    ax2.plot(years, gross_margin_pct, marker="o", linewidth=2.0, color="#D55E00", label="综合毛利率 (%)")
    for x, y in zip(years, gross_margin_pct):
        ax2.text(x, y + 0.4, f"{y:.1f}%", ha="center", fontsize=9, color="#D55E00")
    ax2.set_ylabel("综合毛利率 (%)", color="#D55E00")
    ax2.tick_params(axis="y", labelcolor="#D55E00")
    ax2.set_ylim(25, 40)

    plt.title("凌云光 FY2022–FY2025 营收与综合毛利率走势")
    fig.tight_layout()
    out = os.path.join(OUT, "luster_revenue_gm_trend.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


# ----- Chart 2: FY2025 segment + product mix ---------------------------------
def chart_segment_mix():
    products = ["视觉器件", "视觉系统", "智能视觉装备", "光通信产品", "服务收入"]
    rev = [378.6, 736.0, 1191.3, 565.7, 39.9]   # CNY mn
    growth = [219.2, 6.4, 53.7, -7.7, 12.4]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
    bars = ax.barh(products, rev, color=colors)
    for b, v, g in zip(bars, rev, growth):
        ax.text(v + 15, b.get_y() + b.get_height() / 2,
                f"{v:,.0f}  ({g:+.1f}%)", va="center", fontsize=10)
    ax.set_xlabel("营收 (人民币 百万元)")
    ax.set_xlim(0, max(rev) * 1.30)
    ax.set_title("凌云光 FY2025 分产品营收与同比增速")
    fig.tight_layout()
    out = os.path.join(OUT, "luster_segment_mix.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


# ----- Chart 3: peer valuation (TTM P/E and P/S) -----------------------------
def chart_peer_valuation():
    peers = ["凌云光\n(688400)", "奥普特\n(688686)", "天准科技\n(688003)", "矩子科技\n(300802)", "Cognex\n(CGNX)", "Keyence\n(6861.T)"]
    pe = [180, 60, 75, 45, 70, 38]
    ps = [10.0, 9.0, 4.5, 5.0, 8.0, 12.5]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    colors = ["#C44E52" if p == "凌云光\n(688400)" else "#4C72B0" for p in peers]
    axes[0].bar(peers, pe, color=colors)
    axes[0].set_title("滚动市盈率 (TTM P/E)")
    axes[0].set_ylabel("倍数")
    for i, v in enumerate(pe):
        axes[0].text(i, v + 3, f"{v:.0f}×", ha="center", fontsize=9)
    axes[0].tick_params(axis="x", labelsize=9)

    axes[1].bar(peers, ps, color=colors)
    axes[1].set_title("滚动市销率 (TTM P/S)")
    axes[1].set_ylabel("倍数")
    for i, v in enumerate(ps):
        axes[1].text(i, v + 0.2, f"{v:.1f}×", ha="center", fontsize=9)
    axes[1].tick_params(axis="x", labelsize=9)

    fig.suptitle("机器视觉同业估值对比 (截至 2026 年 5 月中旬，近似值)")
    fig.tight_layout()
    out = os.path.join(OUT, "luster_peer_valuation.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


# ----- Chart 4: China machine vision TAM trajectory -------------------------
def chart_tam():
    yrs = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025E", "2026E", "2027E", "2028E"]
    mkt = [7.0, 9.0, 11.1, 16.4, 17.0, 18.5, 22.0, 28.0, 35.5, 44.0, 53.0]   # CNY bn
    fig, ax = plt.subplots(figsize=(9, 4.6))
    bars = ax.bar(yrs, mkt, color=["#3F6BA8"] * 7 + ["#A0A0A0"] * 4)
    for b, v in zip(bars, mkt):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:.1f}", ha="center", fontsize=8.5)
    ax.set_ylabel("市场规模 (人民币 十亿元)")
    ax.set_title("中国机器视觉市场规模 (2018–2028E)")
    ax.set_ylim(0, max(mkt) * 1.15)
    fig.tight_layout()
    out = os.path.join(OUT, "luster_tam.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    chart_revenue_gm()
    chart_segment_mix()
    chart_peer_valuation()
    chart_tam()
