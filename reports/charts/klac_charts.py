"""KLAC research charts.

Data sources (verified):
- FY2021–FY2025 totals: KLA Corp 10-K filings (FY2021, FY2022, FY2023, FY2024, FY2025), SEC EDGAR.
- Segment revenues FY2023–FY2025: KLA FY2025 10-K, MD&A "Segment Reporting" table.
- Q1 FY2026 results: KLA 8-K, Oct 29 2025 earnings release.
- Q3 FY2026 results: KLA 8-K, Apr 29 2026 earnings release.
- Peer multiples: yfinance (Yahoo Finance) pull on 2026-05-20.

All numbers are in USD millions unless noted.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))


# ── 1) Revenue + gross margin (FY21–FY25) ────────────────────────────────────
def fig_revenue_gm():
    years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
    revenue = [6_918.7, 9_211.9, 10_496.1, 9_812.2, 12_156.2]   # USD M, from 10-Ks
    gm = [60.0, 61.0, 59.8, 60.0, 60.9]                          # GAAP gross margin %, 10-K MD&A
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    bars = ax1.bar(years, revenue, color="#1f4e79", alpha=0.85, label="Total revenue ($M)")
    ax1.set_ylabel("Revenue (USD millions)", color="#1f4e79")
    ax1.set_ylim(0, max(revenue) * 1.18)
    for b, v in zip(bars, revenue):
        ax1.text(b.get_x() + b.get_width() / 2, v + 200, f"${v:,.0f}", ha="center",
                 fontsize=9, color="#1f4e79", fontweight="bold")
    ax2 = ax1.twinx()
    ax2.plot(years, gm, color="#c0504d", marker="o", linewidth=2.2,
             label="GAAP gross margin (%)")
    for x, y in zip(years, gm):
        ax2.text(x, y + 0.3, f"{y:.1f}%", ha="center", fontsize=9, color="#c0504d")
    ax2.set_ylabel("GAAP gross margin (%)", color="#c0504d")
    ax2.set_ylim(56, 64)
    ax1.set_title("KLA Corporation — Revenue & Gross Margin, FY2021–FY2025", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_revenue_gm.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── 2) Segment revenue (FY23–FY25) ───────────────────────────────────────────
def fig_segment_revenue():
    years = ["FY23", "FY24", "FY25"]
    spc = [9_324.2, 8_733.6, 10_947.4]   # Semiconductor Process Control
    ssp = [543.4, 528.7, 587.1]          # Specialty Semi Process
    pcb = [631.6, 552.5, 621.7]          # PCB & Component Inspection
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(years))
    ax.bar(x, spc, label="Semiconductor Process Control", color="#1f4e79")
    ax.bar(x, ssp, bottom=spc, label="Specialty Semi Process", color="#4f81bd")
    ax.bar(x, pcb, bottom=np.array(spc) + np.array(ssp),
           label="PCB & Component Inspection", color="#9bbb59")
    totals = [a + b + c for a, b, c in zip(spc, ssp, pcb)]
    for i, t in enumerate(totals):
        ax.text(i, t + 200, f"${t:,.0f}M", ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("Revenue (USD millions)")
    ax.set_title("KLA — Revenue by Reportable Segment, FY2023–FY2025", fontsize=13, fontweight="bold")
    ax.set_ylim(0, max(totals) * 1.15)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_segments.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── 3) Services share of revenue ─────────────────────────────────────────────
def fig_services_share():
    years = ["FY21", "FY22", "FY23", "FY24", "FY25"]
    product = [5_240.3, 7_301.4, 8_379.0, 7_482.7, 9_472.9]
    service = [1_678.4, 1_910.5, 2_117.0, 2_329.6, 2_683.3]
    total = [p + s for p, s in zip(product, service)]
    service_pct = [s / t * 100 for s, t in zip(service, total)]
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    width = 0.55
    x = np.arange(len(years))
    ax1.bar(x, product, width, label="Product revenue", color="#1f4e79")
    ax1.bar(x, service, width, bottom=product, label="Service revenue", color="#f79646")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.set_ylabel("Revenue (USD millions)")
    ax1.legend(loc="upper left")
    ax2 = ax1.twinx()
    ax2.plot(x, service_pct, color="#c0504d", marker="o", linewidth=2.2,
             label="Service % of total")
    for i, v in enumerate(service_pct):
        ax2.text(i, v + 0.4, f"{v:.1f}%", ha="center", color="#c0504d", fontsize=9)
    ax2.set_ylim(15, 28)
    ax2.set_ylabel("Service share (%)", color="#c0504d")
    ax1.set_title("KLA — Product vs. Service Revenue & Services Share, FY2021–FY2025",
                  fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_services.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── 4) FCF and capital return (FY22–FY25 + LTM Q3FY26) ──────────────────────
def fig_fcf_capital_return():
    # FY22–FY25 from cash-flow tables; LTM Q3 FY26 from Apr 29 2026 8-K.
    years = ["FY22", "FY23", "FY24", "FY25", "LTM Q3FY26"]
    ocf = [3_312.7, 3_669.8, 3_308.6, 4_081.9, 4_400.0]    # last point: 8-K says "LTM operating cash flow $4.40B"
    fcf = [3_005.4, 3_328.2, 3_031.2, 3_741.7, 4_010.0]    # last point: 8-K says FCF $4.01B
    buyback = [3_967.8, 1_311.9, 1_735.7, 2_149.9, np.nan]  # FY-end repurchases
    dividends = [638.5, 732.6, 773.0, 904.6, np.nan]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(years))
    width = 0.22
    ax.bar(x - 1.5 * width, ocf, width, label="Operating cash flow", color="#1f4e79")
    ax.bar(x - 0.5 * width, fcf, width, label="Free cash flow", color="#4f81bd")
    ax.bar(x + 0.5 * width, buyback, width, label="Share repurchases", color="#c0504d")
    ax.bar(x + 1.5 * width, dividends, width, label="Dividends paid", color="#9bbb59")
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("USD millions")
    ax.set_title("KLA — Cash Generation & Capital Return", fontsize=13, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_capital_return.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── 5) Peer multiples comparison (TTM P/E, TTM P/S) ─────────────────────────
def fig_peer_multiples():
    # Source: yfinance pull 2026-05-20.
    peers = ["KLAC", "AMAT", "LRCX", "ASML", "ONTO", "CAMT"]
    pe = [51.4, 40.0, 54.8, 51.6, 120.9, 161.6]
    ps = [18.1, 11.6, 16.7, 17.7, 12.6, 14.6]
    x = np.arange(len(peers))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars1 = ax.bar(x - width / 2, pe, width, label="TTM P/E", color="#1f4e79")
    bars2 = ax.bar(x + width / 2, ps, width, label="TTM P/S", color="#f79646")
    for b, v in zip(bars1, pe):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}x", ha="center",
                fontsize=9, color="#1f4e79")
    for b, v in zip(bars2, ps):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}x", ha="center",
                fontsize=9, color="#a05a00")
    ax.set_xticks(x)
    ax.set_xticklabels(peers)
    ax.set_ylabel("Multiple (x)")
    ax.set_title("Process-Control / WFE Peers — TTM P/E and P/S (2026-05-20)",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_peer_multiples.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── 6) Geographic revenue mix (FY23–FY25) ───────────────────────────────────
def fig_geographic_mix():
    # FY25 10-K MD&A "Revenues by region, based on ship-to location"
    regions = ["China", "Taiwan", "Korea", "Japan", "North America", "Europe & Other"]
    fy23 = [27, 24, 18, 11, 12, 8]      # %
    fy24 = [43, 18, 9, 11, 12, 7]
    fy25 = [33, 27, 12, 11, 11, 6]
    x = np.arange(len(regions))
    width = 0.27
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(x - width, fy23, width, label="FY2023", color="#9bbb59")
    ax.bar(x, fy24, width, label="FY2024", color="#4f81bd")
    ax.bar(x + width, fy25, width, label="FY2025", color="#1f4e79")
    ax.set_xticks(x)
    ax.set_xticklabels(regions, rotation=20)
    ax.set_ylabel("% of total revenue")
    ax.set_title("KLA — Revenue by Region (ship-to), FY2023–FY2025",
                 fontsize=13, fontweight="bold")
    ax.legend()
    for i in range(len(regions)):
        for j, vals in enumerate([fy23, fy24, fy25]):
            v = vals[i]
            ax.text(i + (j - 1) * width, v + 0.7, f"{v}%", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "klac_geo_mix.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_revenue_gm()
    fig_segment_revenue()
    fig_services_share()
    fig_fcf_capital_return()
    fig_peer_multiples()
    fig_geographic_mix()
    print("Saved charts:")
    for name in ("revenue_gm", "segments", "services", "capital_return",
                 "peer_multiples", "geo_mix"):
        print(f"  {OUT}/klac_{name}.png")
