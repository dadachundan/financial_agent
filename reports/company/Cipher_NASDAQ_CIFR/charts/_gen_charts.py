#!/usr/bin/env python3
"""Generate matplotlib charts for the Cipher Mining (CIFR) research report."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 150, "font.size": 10})


# ── 1) Revenue & operating loss trend (2022–2025 + Q1 2026) ──────────────
def chart_revenue_opex():
    fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
    years   = ["2023", "2024", "2025"]
    rev     = [126.8, 151.3, 223.9]            # 10-K p.46
    op_loss = [-20.1, -43.7, -421.6]           # 10-K p.46 (includes 2025 non-cash impairments)
    adj_ear = [46.2, 106.7, 22.2]              # 10-K p.51 Adjusted Earnings

    x = np.arange(len(years))
    w = 0.28
    ax1.bar(x - w, rev, w, color="#1f6feb", label="Revenue (USD M)")
    ax1.bar(x,     op_loss, w, color="#d1242f", label="Operating loss (USD M)")
    ax1.bar(x + w, adj_ear, w, color="#2da44e", label="Adjusted earnings (USD M)")

    ax1.axhline(0, color="black", linewidth=0.7)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.set_ylabel("USD millions")
    ax1.set_title("Cipher Mining — Revenue, GAAP operating loss, and non-GAAP adjusted earnings\nFY2023 – FY2025  (2025 op-loss includes USD 450M derivative re-mark & USD 96M held-for-sale write-down)")
    ax1.grid(axis="y", alpha=0.3)
    ax1.legend(loc="lower left")
    for i, v in enumerate(rev):
        ax1.text(i - w, v + 6, f"{v:.0f}", ha="center", fontsize=8)
    for i, v in enumerate(adj_ear):
        ax1.text(i + w, v + 6, f"{v:.0f}", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "cifr_revenue_opex.png", bbox_inches="tight")
    plt.close(fig)


# ── 2) Hashrate / MW trend ───────────────────────────────────────────────
def chart_hashrate_mw():
    fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
    periods = ["Q4-2023", "Q4-2024", "Q1-2025", "Q3-2025\n(Black Pearl\nramp 150 MW)", "Q1-2026\n(post-AWS sale)"]
    hashrate = [7.2, 13.5, 13.5, 23.0, 11.6]     # public commentary + 10-K & business updates
    mw_self   = [127, 207, 207, 357, 207]         # 207 Odessa + 150 BP at peak

    x = np.arange(len(periods))
    w = 0.4
    ax1.bar(x - w/2, hashrate, w, color="#fb8500", label="Self-mining hashrate (EH/s)")
    ax2 = ax1.twinx()
    ax2.bar(x + w/2, mw_self, w, color="#1f6feb", alpha=0.7, label="Self-mining MW")

    ax1.set_xticks(x); ax1.set_xticklabels(periods, fontsize=8)
    ax1.set_ylabel("EH/s", color="#fb8500")
    ax2.set_ylabel("Self-mining MW", color="#1f6feb")
    ax1.set_title("Cipher Mining — Self-mining hashrate and energized MW capacity\nBlack Pearl mined briefly in 2H-2025 before HPC conversion; JV sites sold Feb-2026")
    ax1.grid(axis="y", alpha=0.3)
    fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.94))
    for i, v in enumerate(hashrate):
        ax1.text(i - w/2, v + 0.4, f"{v:.1f}", ha="center", fontsize=8, color="#fb8500")
    for i, v in enumerate(mw_self):
        ax2.text(i + w/2, v + 6, f"{v}", ha="center", fontsize=8, color="#1f6feb")
    fig.tight_layout()
    fig.savefig(OUT / "cifr_hashrate_mw.png", bbox_inches="tight")
    plt.close(fig)


# ── 3) BTC mined and cost-to-mine context ────────────────────────────────
def chart_btc_cost():
    fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
    qtrs = ["Q1-25", "Q2-25", "Q3-25", "Q4-25", "Q1-26"]
    btc_mined = [603, 458, 562, 575, 346]   # Q1-26 disclosed; others est. from MW & network hashrate
    rev_q     = [49.0, 44.0, 71.7, 59.7, 34.8]   # Q1-26 and Q4-25 from 8-K; others approx from 10-K trend
    ax1.bar(qtrs, btc_mined, color="#7d3aed", alpha=0.8, label="BTC mined (left)")
    ax1.set_ylabel("BTC mined (units)", color="#7d3aed")
    ax2 = ax1.twinx()
    ax2.plot(qtrs, rev_q, color="#1f6feb", marker="o", linewidth=2, label="Mining revenue, USD M (right)")
    ax2.set_ylabel("Quarterly mining revenue (USD M)", color="#1f6feb")
    ax1.set_title("Bitcoin produced and mining revenue — Cipher Mining, Q1-2025 to Q1-2026\nQ1-26 fall reflects sale of WindHQ JV sites and Black Pearl miners being held-for-sale")
    ax1.grid(axis="y", alpha=0.3)
    for i, v in enumerate(btc_mined):
        ax1.text(i, v + 8, f"{v}", ha="center", fontsize=8, color="#7d3aed")
    for i, v in enumerate(rev_q):
        ax2.text(i, v + 1.5, f"${v:.0f}M", ha="center", fontsize=8, color="#1f6feb")
    fig.tight_layout()
    fig.savefig(OUT / "cifr_btc_mined_cost.png", bbox_inches="tight")
    plt.close(fig)


# ── 4) AI-hosting contracted NOI ramp 2026–2035 ──────────────────────────
def chart_hpc_noi():
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    years = ["2026", "2027", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035"]
    noi   = [86, 646, 725, 747, 770, 793, 816, 841, 866, 892]   # Q1-26 deck p.6
    ax.bar(years, noi, color="#2da44e")
    ax.set_ylabel("Contracted annualized NOI (USD M)")
    ax.set_title("Cipher Digital — contracted HPC net operating income ramp\nAverage ~USD 787M/yr over the 10-yr base term — Barber Lake + Black Pearl + 3rd lease")
    for i, v in enumerate(noi):
        ax.text(i, v + 15, f"${v}M", ha="center", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "cifr_hpc_noi.png", bbox_inches="tight")
    plt.close(fig)


# ── 5) Peer EV/Revenue and Mkt-Cap-per-MW comparison ─────────────────────
def chart_peer_ev_rev():
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    tickers = ["CIFR", "IREN", "CLSK", "RIOT", "MARA", "CORZ", "BTDR", "HUT", "HIVE"]
    ev_rev  = [57.3, 27.2, 7.4, 14.7, 8.1, 21.9, 6.6, 40.2, 3.8]    # yfinance pull 2026-05
    p_s     = [41.4, 27.1, 5.5, 14.2, 5.9, 21.9, 4.6, 40.7, 3.8]
    x = np.arange(len(tickers))
    w = 0.4
    bars1 = ax.bar(x - w/2, ev_rev, w, color="#1f6feb", label="EV / TTM revenue")
    bars2 = ax.bar(x + w/2, p_s, w, color="#fb8500", label="P / TTM sales")
    ax.set_xticks(x); ax.set_xticklabels(tickers)
    ax.set_ylabel("Multiple (×)")
    ax.set_title("Cipher vs. listed bitcoin-miner / HPC-pivot peers — EV/Rev and P/S, TTM\nCIFR multiples reflect contracted HPC future revenue, not yet earned")
    ax.grid(axis="y", alpha=0.3); ax.legend()
    for i, v in enumerate(ev_rev):
        ax.text(i - w/2, v + 1, f"{v:.1f}", ha="center", fontsize=8)
    for i, v in enumerate(p_s):
        ax.text(i + w/2, v + 1, f"{v:.1f}", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "cifr_peer_ev_rev.png", bbox_inches="tight")
    plt.close(fig)


# ── 6) Capital structure / debt stack as of 31-Mar-2026 ──────────────────
def chart_cap_structure():
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    labels = [
        "Cash & equivalents",
        "Restricted cash (HPC projects)",
        "7.125% Sr Sec Notes 2030 (Barber Lake)",
        "6.125% Sr Sec Notes 2031 (Black Pearl)",
        "1.75% Conv 2030",
        "0.00% Conv 2031",
    ]
    values = [715, 3531, 1733, 2000, 173, 1300]   # USD M, Q1-26 balance sheet & cap table
    colors = ["#2da44e", "#2da44e", "#d1242f", "#d1242f", "#fb8500", "#fb8500"]
    bars = ax.barh(labels, values, color=colors)
    ax.set_xlabel("USD millions")
    ax.set_title("Cipher Digital — capital structure snapshot as of 31-Mar-2026\nGreen = cash & restricted cash, red = senior secured project notes, orange = convertibles")
    for b, v in zip(bars, values):
        ax.text(v + 60, b.get_y() + b.get_height()/2, f"${v:,}M", va="center", fontsize=8)
    ax.grid(axis="x", alpha=0.3)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUT / "cifr_capital_structure.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    chart_revenue_opex()
    chart_hashrate_mw()
    chart_btc_cost()
    chart_hpc_noi()
    chart_peer_ev_rev()
    chart_cap_structure()
    print("done")
