#!/usr/bin/env python3
"""Generate charts for TSMC research report (NYSE:TSM, 2026-05-20)."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150, "font.size": 10})


# ---------------------------------------------------------------------------
# Chart 1 — Revenue and Gross Margin trend FY2021–FY2025 + Q1-2026 annualized
# Source: 20-F FY2025, FY2024, FY2023; Q1 2026 6-K earnings release
# ---------------------------------------------------------------------------
def chart_rev_gm():
    years = ["2021", "2022", "2023", "2024", "2025"]
    # Net revenue, USD billions (from 20-F: NT$ converted at year avg)
    # 2021: NT$1,587.4 bn; 2022: NT$2,263.9 bn; 2023: NT$2,161.7 bn;
    # 2024: NT$2,894.3 bn; 2025: NT$3,809.1 bn = US$121.4 bn
    # FX (avg): 2021 27.93, 2022 29.81, 2023 31.16, 2024 32.13, 2025 31.11
    rev_usd = [56.82, 75.94, 69.38, 90.08, 121.42]
    gm = [51.6, 59.6, 54.4, 56.1, 59.9]  # gross margin %

    fig, ax1 = plt.subplots(figsize=(8.6, 4.6))
    bars = ax1.bar(years, rev_usd, color="#1f4e79", width=0.55, alpha=0.85,
                   label="Net revenue (US$ bn)")
    ax1.set_ylabel("Net revenue (US$ bn)", color="#1f4e79", fontsize=11)
    ax1.tick_params(axis="y", labelcolor="#1f4e79")
    ax1.set_ylim(0, 145)
    for b, v in zip(bars, rev_usd):
        ax1.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.1f}",
                 ha="center", va="bottom", fontsize=9, color="#1f4e79")

    ax2 = ax1.twinx()
    ax2.plot(years, gm, color="#c0504d", marker="o", linewidth=2.2,
             label="Gross margin (%)")
    ax2.set_ylabel("Gross margin (%)", color="#c0504d", fontsize=11)
    ax2.tick_params(axis="y", labelcolor="#c0504d")
    ax2.set_ylim(45, 70)
    for x, y in zip(years, gm):
        ax2.text(x, y + 0.7, f"{y:.1f}%", ha="center", color="#c0504d",
                 fontsize=9)

    plt.title("TSMC — Net Revenue and Gross Margin, FY2021–FY2025",
              fontsize=12, pad=12)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_revenue_gm.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 2 — Wafer revenue by process node (2023 / 2024 / 2025)
# Source: 20-F FY2025, "Technology Development" table
# ---------------------------------------------------------------------------
def chart_node_mix():
    nodes = ["3nm", "5nm", "7nm", "16nm", "28nm", "Other"]
    y23 = [6, 33, 19, 10, 10, 22]
    y24 = [18, 34, 17, 8, 7, 16]
    y25 = [24, 36, 14, 7, 7, 12]

    x = np.arange(len(nodes))
    w = 0.27
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.bar(x - w, y23, w, label="2023", color="#5b9bd5")
    ax.bar(x,     y24, w, label="2024", color="#1f4e79")
    ax.bar(x + w, y25, w, label="2025", color="#c0504d")
    for xi, v23, v24, v25 in zip(x, y23, y24, y25):
        ax.text(xi - w, v23 + 0.4, f"{v23}", ha="center", fontsize=8)
        ax.text(xi,     v24 + 0.4, f"{v24}", ha="center", fontsize=8)
        ax.text(xi + w, v25 + 0.4, f"{v25}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(nodes)
    ax.set_ylabel("% of total wafer revenue")
    ax.set_title("TSMC — Wafer Revenue Mix by Process Node, 2023–2025",
                 fontsize=12, pad=10)
    ax.legend(loc="upper right")
    ax.set_ylim(0, 40)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_node_mix.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 3 — Revenue by platform (HPC / Smartphone / IoT / Auto / DCE / Other)
# Source: 20-F FY2025
# ---------------------------------------------------------------------------
def chart_platform():
    plats = ["HPC", "Smartphone", "IoT", "Automotive", "DCE", "Other"]
    y23 = [43, 38, 8, 6, 2, 3]
    y24 = [51, 35, 6, 5, 1, 2]
    y25 = [58, 29, 5, 5, 1, 2]

    x = np.arange(len(plats))
    w = 0.27
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.bar(x - w, y23, w, label="2023", color="#92d050")
    ax.bar(x,     y24, w, label="2024", color="#1f4e79")
    ax.bar(x + w, y25, w, label="2025", color="#c0504d")
    for xi, v23, v24, v25 in zip(x, y23, y24, y25):
        ax.text(xi - w, v23 + 0.6, f"{v23}", ha="center", fontsize=8)
        ax.text(xi,     v24 + 0.6, f"{v24}", ha="center", fontsize=8)
        ax.text(xi + w, v25 + 0.6, f"{v25}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(plats)
    ax.set_ylabel("% of net revenue")
    ax.set_title("TSMC — Net Revenue by Platform, 2023–2025",
                 fontsize=12, pad=10)
    ax.legend(loc="upper right")
    ax.set_ylim(0, 65)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_platform_mix.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 4 — Capex history and FY2026 guide
# Source: 20-F FY2025 (NT$ capex). Convert to US$ using NT$/US$ avg.
# 2021 NT$839.2 bn @ 27.93 = US$30.0 bn
# 2022 NT$1,082.7 bn @ 29.81 = US$36.3 bn
# 2023 NT$949.8 bn @ 31.16 = US$30.5 bn
# 2024 NT$956.0 bn @ 32.13 = US$29.8 bn
# 2025 NT$1,272.4 bn @ 31.11 = US$40.9 bn
# 2026E US$52–56 bn (midpoint 54)
# ---------------------------------------------------------------------------
def chart_capex():
    years = ["2021", "2022", "2023", "2024", "2025", "2026E"]
    capex = [30.0, 36.3, 30.5, 29.8, 40.9, 54.0]
    colors = ["#1f4e79"]*5 + ["#c0504d"]
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    bars = ax.bar(years, capex, color=colors, width=0.6)
    for b, v in zip(bars, capex):
        label = f"${v:.1f}B"
        ax.text(b.get_x() + b.get_width() / 2, v + 0.8, label,
                ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Capital expenditure (US$ bn)")
    ax.set_title("TSMC — Capital Expenditure, FY2021–FY2025 and 2026 Guide (midpoint)",
                 fontsize=12, pad=10)
    ax.set_ylim(0, 65)
    ax.text(5, 58, "2026E range:\nUS$52–56 bn", ha="center", fontsize=9,
            color="#c0504d")
    fig.tight_layout()
    plt.savefig(OUT / "tsm_capex.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 5 — Operating cash flow vs capex (FCF proxy)
# Source: 20-F FY2025 cash-flow table
# ---------------------------------------------------------------------------
def chart_ocf_capex():
    years = ["2023", "2024", "2025"]
    ocf = [39.86, 56.84, 72.52]    # US$ bn (NT$ at avg FX)
    capex = [30.48, 29.76, 40.90]
    fcf = [a - b for a, b in zip(ocf, capex)]

    x = np.arange(len(years))
    w = 0.28
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.bar(x - w, ocf, w, label="Operating cash flow", color="#1f4e79")
    ax.bar(x,     capex, w, label="Capex", color="#c0504d")
    ax.bar(x + w, fcf, w, label="Free cash flow (proxy)", color="#92d050")
    for xi, a, b, c in zip(x, ocf, capex, fcf):
        ax.text(xi - w, a + 1, f"{a:.1f}", ha="center", fontsize=8)
        ax.text(xi,     b + 1, f"{b:.1f}", ha="center", fontsize=8)
        ax.text(xi + w, c + 1, f"{c:.1f}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel("US$ billions")
    ax.set_title("TSMC — Operating Cash Flow, Capex and Implied FCF, 2023–2025",
                 fontsize=12, pad=10)
    ax.legend(loc="upper left")
    ax.set_ylim(0, 85)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_ocf_capex.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 6 — Geographic revenue mix
# Source: 20-F FY2025, "Markets and Customers"
# ---------------------------------------------------------------------------
def chart_geo():
    years = ["2023", "2024", "2025"]
    na = [68, 70, 75]
    ap = [8, 10, 9]
    ch = [12, 11, 9]
    jp = [6, 5, 4]
    em = [6, 4, 3]
    x = np.arange(len(years))
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.bar(x, na, label="North America", color="#1f4e79")
    ax.bar(x, ap, bottom=na, label="Asia Pacific ex-CN/JP", color="#5b9bd5")
    bot2 = [a + b for a, b in zip(na, ap)]
    ax.bar(x, ch, bottom=bot2, label="China", color="#c0504d")
    bot3 = [a + b for a, b in zip(bot2, ch)]
    ax.bar(x, jp, bottom=bot3, label="Japan", color="#f4b183")
    bot4 = [a + b for a, b in zip(bot3, jp)]
    ax.bar(x, em, bottom=bot4, label="EMEA", color="#a5a5a5")
    ax.set_xticks(x); ax.set_xticklabels(years)
    ax.set_ylabel("% of net revenue")
    ax.set_title("TSMC — Revenue by Customer Geography, 2023–2025",
                 fontsize=12, pad=10)
    ax.legend(loc="lower left", fontsize=9)
    ax.set_ylim(0, 105)
    for xi, n in zip(x, na):
        ax.text(xi, 2, f"NA {n}%", ha="center", color="white", fontsize=9,
                weight="bold")
    fig.tight_layout()
    plt.savefig(OUT / "tsm_geo_mix.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 7 — Peer comparison: TTM P/E and TTM P/S (May 2026 snapshot)
# Sources cited in report
# ---------------------------------------------------------------------------
def chart_peers():
    peers = ["TSM", "UMC", "GFS", "ASML", "INTC"]
    pe = [30.5, 21.6, 34.5, 35.0, np.nan]   # INTC ~negative TTM
    ps = [15.5, 2.7, 5.4, 11.0, 1.7]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
    ax1, ax2 = axes
    bars1 = ax1.bar(peers, pe, color=["#1f4e79", "#5b9bd5", "#c0504d",
                                       "#92d050", "#a5a5a5"])
    for b, v in zip(bars1, pe):
        if not np.isnan(v):
            ax1.text(b.get_x() + b.get_width() / 2, v + 0.5,
                     f"{v:.1f}x", ha="center", fontsize=9)
    ax1.set_title("TTM P/E (May 2026)", fontsize=11)
    ax1.set_ylim(0, 45)
    ax1.text(4, 5, "INTC:\nneg. TTM", ha="center", fontsize=8,
             color="#555")

    bars2 = ax2.bar(peers, ps, color=["#1f4e79", "#5b9bd5", "#c0504d",
                                       "#92d050", "#a5a5a5"])
    for b, v in zip(bars2, ps):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.2,
                 f"{v:.1f}x", ha="center", fontsize=9)
    ax2.set_title("TTM P/S (May 2026)", fontsize=11)
    ax2.set_ylim(0, 20)
    fig.suptitle("Foundry / Capital-Equipment Peer Comparison — Trading Multiples",
                 fontsize=12)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_peer_multiples.png", bbox_inches="tight")
    plt.close()


# ---------------------------------------------------------------------------
# Chart 8 — Foundry market share 2025 (estimated)
# Source: TrendForce / Counterpoint via PatentPC summary
# ---------------------------------------------------------------------------
def chart_share():
    labels = ["TSMC", "Samsung Foundry", "SMIC", "UMC", "GlobalFoundries",
              "Others"]
    shares = [72, 7, 6, 5, 4, 6]
    colors = ["#1f4e79", "#c0504d", "#f4b183", "#5b9bd5", "#92d050",
              "#a5a5a5"]
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    wedges, texts, autotexts = ax.pie(
        shares, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.78,
        wedgeprops={"linewidth": 1, "edgecolor": "white"})
    for t in autotexts:
        t.set_color("white"); t.set_fontsize(10); t.set_weight("bold")
    ax.set_title("Global Pure-Play Foundry Revenue Share, Q4 2025 (est.)",
                 fontsize=12, pad=10)
    fig.tight_layout()
    plt.savefig(OUT / "tsm_foundry_share.png", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    chart_rev_gm()
    chart_node_mix()
    chart_platform()
    chart_capex()
    chart_ocf_capex()
    chart_geo()
    chart_peers()
    chart_share()
    print("Charts written to", OUT)
