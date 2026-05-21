"""Charts for 奥比中光 (SSE:688322) company research report.

All figures sourced from cninfo annual report PDFs (2022–2025 年度报告).
"""
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

# Use a Chinese-capable font; fall back to PingFang on macOS
mpl.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "STHeiti", "Arial Unicode MS"]
mpl.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def chart_revenue_margin():
    # 营业收入来自 2023 年报和 2025 年报披露
    # 主营毛利率：2025 = 43.54%（年报披露主营毛利率），2024 = 41.74%（同），
    # 2023 = 36.74%，2022 = 32.83%（按 2023 年报中分行业表反推）
    years = [2022, 2023, 2024, 2025]
    revenue = [350.0, 360.0, 564.5, 940.7]
    # 综合毛利率：2023 年报披露 2023 年 42.65%，较 2022 年下降 0.98 pp → 2022 ≈ 43.63%
    # 2025 年报披露主营毛利率 43.54%（同比 +1.80pp）→ 2024 ≈ 41.74%
    gm = [43.63, 42.65, 41.74, 43.54]

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    bars = ax1.bar(years, revenue, color="#3a6ea5", alpha=0.85, label="营业收入 (百万元)")
    ax1.set_xlabel("年度")
    ax1.set_ylabel("营业收入 (百万元)", color="#3a6ea5")
    ax1.tick_params(axis="y", labelcolor="#3a6ea5")
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width() / 2, v + 15, f"{v:.0f}",
                 ha="center", fontsize=9, color="#1f3a5f")

    ax2 = ax1.twinx()
    ax2.plot(years, gm, color="#c0392b", marker="o", linewidth=2.2, label="综合毛利率 (%)")
    ax2.set_ylabel("综合毛利率 (%)", color="#c0392b")
    ax2.tick_params(axis="y", labelcolor="#c0392b")
    ax2.set_ylim(30, 55)
    for x, y in zip(years, gm):
        ax2.text(x, y + 1.2, f"{y:.1f}%", ha="center", fontsize=9, color="#7f1c10")

    plt.title("奥比中光 营业收入与综合毛利率 (2022-2025)")
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "orbbec_revenue_gm.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_segment_mix():
    """2025 主营业务分行业收入结构 (百万元)."""
    segments = ["AIoT (机器人/三维扫描等)", "生物识别 (刷脸支付/医保)", "工业三维扫描", "其他"]
    values = [512.1, 390.4, 25.8, 6.7]
    colors = ["#2980b9", "#27ae60", "#e67e22", "#95a5a6"]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.barh(segments, values, color=colors)
    ax.set_xlabel("2025 年营业收入 (百万元)")
    total = sum(values)
    for b, v in zip(bars, values):
        ax.text(v + 8, b.get_y() + b.get_height() / 2,
                f"{v:.1f} ({v / total * 100:.1f}%)", va="center", fontsize=9)
    ax.set_title("2025 年主营业务分行业收入结构")
    ax.invert_yaxis()
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "orbbec_segment_mix.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_rd_ratio():
    # 2022 年报：研发投入 380.59M，占营收 108.73%
    # 2023 年报：研发投入 300.81M，占营收 83.56%
    # 2025 年报：2024 研发 204.33M（36.20%），2025 研发 202.53M（21.53%）
    years = [2022, 2023, 2024, 2025]
    rd = [380.6, 300.8, 204.3, 202.5]  # 百万元
    rd_ratio = [108.7, 83.6, 36.2, 21.5]  # %

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    bars = ax1.bar(years, rd, color="#8e44ad", alpha=0.85)
    ax1.set_ylabel("研发投入 (百万元)", color="#8e44ad")
    ax1.tick_params(axis="y", labelcolor="#8e44ad")
    for b, v in zip(bars, rd):
        ax1.text(b.get_x() + b.get_width() / 2, v + 8, f"{v:.1f}",
                 ha="center", fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(years, rd_ratio, color="#d35400", marker="s", linewidth=2.2)
    ax2.set_ylabel("研发投入占营业收入比例 (%)", color="#d35400")
    ax2.tick_params(axis="y", labelcolor="#d35400")
    ax2.set_ylim(0, 100)
    for x, y in zip(years, rd_ratio):
        ax2.text(x, y + 3, f"{y:.1f}%", ha="center", fontsize=9, color="#7d2f00")

    plt.title("奥比中光 研发投入与研发强度 (2022-2025)")
    plt.xlabel("年度")
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "orbbec_rd_ratio.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_quarterly():
    """2025 quarterly revenue + net profit."""
    quarters = ["1Q25", "2Q25", "3Q25", "4Q25"]
    rev = [191.1, 244.4, 278.5, 226.7]
    np = [24.3, 35.9, 47.8, 19.9]

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    bars = ax1.bar(quarters, rev, color="#16a085", alpha=0.85, label="营业收入 (百万元)")
    ax1.set_ylabel("营业收入 (百万元)", color="#16a085")
    ax1.tick_params(axis="y", labelcolor="#16a085")
    for b, v in zip(bars, rev):
        ax1.text(b.get_x() + b.get_width() / 2, v + 5, f"{v:.1f}",
                 ha="center", fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(quarters, np, color="#c0392b", marker="o", linewidth=2.2, label="归母净利润 (百万元)")
    ax2.set_ylabel("归母净利润 (百万元)", color="#c0392b")
    ax2.tick_params(axis="y", labelcolor="#c0392b")
    for x, y in zip(quarters, np):
        ax2.text(x, y + 1.5, f"{y:.1f}", ha="center", fontsize=9, color="#7f1c10")

    plt.title("奥比中光 2025 年单季度营业收入与归母净利润")
    fig.tight_layout()
    plt.savefig(os.path.join(OUT, "orbbec_quarterly.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    chart_revenue_margin()
    chart_segment_mix()
    chart_rd_ratio()
    chart_quarterly()
    print("Charts written to", OUT)
