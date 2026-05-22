"""Charts for Apple Inc. (NASDAQ:AAPL) company-research report."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def chart_revenue_margin_trend():
    # FY2021–FY2025 from 10-Ks. FY2026 = ttm derived as FY2025 + (H1-26 - H1-25).
    fy = ["FY21", "FY22", "FY23", "FY24", "FY25", "TTM FY26"]
    revenue = [365.817, 394.328, 383.285, 391.035, 416.161, 416.161 + 254.940 - 219.659]
    gm_pct = [41.78, 43.31, 44.13, 46.21, 46.91,
              (180.683 - 103.142 + 124.012) / (391.035 - 219.659 + 254.940) * 100]

    fig, ax1 = plt.subplots(figsize=(9, 4.8))
    bars = ax1.bar(fy, revenue, color="#0072CE", alpha=0.85, label="Revenue (USD B)")
    ax1.set_ylabel("Revenue (USD Billion)", color="#0072CE")
    ax1.tick_params(axis="y", labelcolor="#0072CE")
    ax1.set_ylim(0, max(revenue) * 1.20)
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width() / 2, v + 4, f"{v:.1f}", ha="center", fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(fy, gm_pct, color="#FF6B00", marker="o", linewidth=2.4, label="Gross margin %")
    ax2.set_ylabel("Gross margin %", color="#FF6B00")
    ax2.tick_params(axis="y", labelcolor="#FF6B00")
    ax2.set_ylim(35, 55)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    for x, y in zip(fy, gm_pct):
        ax2.text(x, y + 0.5, f"{y:.1f}%", ha="center", color="#FF6B00", fontsize=9)

    plt.title("Apple — Revenue and gross-margin trend, FY2021–TTM FY2026")
    fig.tight_layout()
    fig.savefig(OUT / "aapl_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_segment_mix():
    # FY2023, FY2024, FY2025 product/services mix (USD bn)
    cats = ["iPhone", "Mac", "iPad", "Wearables/Home/Acc", "Services"]
    fy23 = [200.583, 29.357, 28.300, 39.845, 85.200]
    fy24 = [201.183, 29.984, 26.694, 37.005, 96.169]
    fy25 = [209.586, 33.708, 28.023, 35.686, 109.158]
    x = np.arange(len(cats))
    width = 0.27

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.bar(x - width, fy23, width, label="FY2023", color="#9CA3AF")
    ax.bar(x, fy24, width, label="FY2024", color="#3B82F6")
    ax.bar(x + width, fy25, width, label="FY2025", color="#1E3A8A")
    for i, vals in enumerate(zip(fy23, fy24, fy25)):
        for j, v in enumerate(vals):
            ax.text(i + (j - 1) * width, v + 2, f"{v:.0f}",
                    ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=10)
    ax.set_ylabel("Net sales (USD Billion)")
    ax.set_title("Apple — Net sales by product category, FY2023 → FY2025")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "aapl_segment_mix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_services_growth():
    # Services revenue and segment gross margin %, FY21–FY25
    fy = ["FY21", "FY22", "FY23", "FY24", "FY25"]
    services_rev = [68.425, 78.129, 85.200, 96.169, 109.158]
    services_gm = [69.7, 71.7, 70.8, 73.9, 75.4]
    fig, ax1 = plt.subplots(figsize=(9, 4.6))
    bars = ax1.bar(fy, services_rev, color="#10B981", alpha=0.85)
    ax1.set_ylabel("Services revenue (USD B)", color="#10B981")
    ax1.tick_params(axis="y", labelcolor="#10B981")
    for b, v in zip(bars, services_rev):
        ax1.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}", ha="center", fontsize=9)
    ax2 = ax1.twinx()
    ax2.plot(fy, services_gm, color="#7C3AED", marker="o", linewidth=2.4)
    ax2.set_ylabel("Services gross margin %", color="#7C3AED")
    ax2.tick_params(axis="y", labelcolor="#7C3AED")
    ax2.set_ylim(60, 85)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    for x, y in zip(fy, services_gm):
        ax2.text(x, y + 0.4, f"{y:.1f}%", ha="center", color="#7C3AED", fontsize=9)
    plt.title("Apple Services — revenue and segment gross margin, FY2021–FY2025")
    fig.tight_layout()
    fig.savefig(OUT / "aapl_services_growth.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_geo_mix():
    regions = ["Americas", "Europe", "Greater China", "Japan", "Rest of AP"]
    fy24 = [167.045, 101.328, 66.952, 25.052, 30.658]
    fy25 = [186.699, 102.686, 64.377, 28.703, 33.696]
    x = np.arange(len(regions))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(x - width / 2, fy24, width, label="FY2024", color="#94A3B8")
    ax.bar(x + width / 2, fy25, width, label="FY2025", color="#0F172A")
    for i, (a, b) in enumerate(zip(fy24, fy25)):
        ax.text(i - width / 2, a + 1.5, f"{a:.1f}", ha="center", fontsize=8)
        ax.text(i + width / 2, b + 1.5, f"{b:.1f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(regions)
    ax.set_ylabel("Net sales (USD B)")
    ax.set_title("Apple — Net sales by reportable segment, FY2024 vs FY2025")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "aapl_geo_mix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_capital_return():
    # Buybacks + dividends FY21–FY25 (in USD bn), from 10-K cash-flow disclosures
    fy = ["FY21", "FY22", "FY23", "FY24", "FY25"]
    buybacks = [85.5, 89.4, 77.6, 94.9, 89.3]
    dividends = [14.5, 14.8, 15.0, 15.2, 15.4]
    x = np.arange(len(fy))
    width = 0.6
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(x, buybacks, width, label="Share buybacks", color="#1D4ED8")
    ax.bar(x, dividends, width, bottom=buybacks, label="Dividends", color="#F59E0B")
    for i, (b, d) in enumerate(zip(buybacks, dividends)):
        ax.text(i, b / 2, f"{b:.1f}", ha="center", color="white", fontsize=9)
        ax.text(i, b + d / 2, f"{d:.1f}", ha="center", color="white", fontsize=9)
        ax.text(i, b + d + 2, f"Total {b+d:.1f}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(fy)
    ax.set_ylabel("Capital returned (USD B)")
    ax.set_title("Apple — Capital return program (buybacks + dividends), FY2021–FY2025")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "aapl_capital_return.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def chart_peer_valuation():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    pe = [35.9, 25.0, 30.0, 31.2]
    ps = [8.1, 11.8, 7.8, 3.4]
    x = np.arange(len(tickers))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.bar(x - width / 2, pe, width, label="TTM P/E", color="#0EA5E9")
    ax.bar(x + width / 2, ps, width, label="TTM P/S", color="#F97316")
    for i, (p, s) in enumerate(zip(pe, ps)):
        ax.text(i - width / 2, p + 0.6, f"{p:.1f}", ha="center", fontsize=9)
        ax.text(i + width / 2, s + 0.6, f"{s:.1f}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.set_ylabel("Multiple (×)")
    ax.set_title("Mega-cap valuation snapshot — TTM P/E and P/S, May 2026")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "aapl_peer_valuation.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    chart_revenue_margin_trend()
    chart_segment_mix()
    chart_services_growth()
    chart_geo_mix()
    chart_capital_return()
    chart_peer_valuation()
    print("done")
