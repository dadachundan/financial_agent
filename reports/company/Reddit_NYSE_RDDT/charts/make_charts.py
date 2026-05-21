"""Charts for the Reddit (NYSE:RDDT) company-research report.

Sources for all numbers are documented in the report markdown.  Each chart
is saved as a PNG into the same folder so the markdown can embed them via
a relative path.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

REDDIT_ORANGE = "#FF4500"
REDDIT_BLUE = "#0079D3"
GREY = "#5A5A5A"
LIGHT = "#CCCCCC"


# 1. DAUq trend by quarter (Q4-23 through Q1-26) ---------------------------
def chart_dauq():
    quarters = ["Q4-23", "Q1-24", "Q2-24", "Q3-24", "Q4-24",
                "Q1-25", "Q2-25", "Q3-25", "Q4-25", "Q1-26"]
    dauq = [73.1, 82.7, 91.2, 97.2, 101.7,
            108.1, 110.4, 116.0, 121.4, 126.8]
    yoy = [None, 37, 51, 47, 39, 31, 21, 19, 19, 17]

    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    bars = ax1.bar(quarters, dauq, color=REDDIT_ORANGE, alpha=0.85,
                   label="DAUq (millions)")
    ax1.set_ylabel("Average DAUq (millions)", color=REDDIT_ORANGE)
    ax1.tick_params(axis="y", labelcolor=REDDIT_ORANGE)
    ax1.set_ylim(0, 145)
    for b, v in zip(bars, dauq):
        ax1.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}",
                 ha="center", fontsize=8, color="black")

    ax2 = ax1.twinx()
    ax2.spines["top"].set_visible(False)
    ax2.plot(quarters, yoy, color=REDDIT_BLUE, marker="o", linewidth=2,
             label="YoY growth %")
    ax2.set_ylabel("YoY growth (%)", color=REDDIT_BLUE)
    ax2.tick_params(axis="y", labelcolor=REDDIT_BLUE)
    ax2.set_ylim(0, 60)

    plt.title("Reddit DAUq — Q4 2023 through Q1 2026", fontsize=13, pad=12)
    ax1.set_xlabel("")
    fig.tight_layout()
    fig.savefig(OUT / "rddt_dauq_trend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 2. Revenue & segment mix (advertising vs other) ------------------------
def chart_revenue_mix():
    years = ["FY2023", "FY2024", "FY2025"]
    advertising = [788.8, 1185.5, 2062.5]
    other = [15.2, 114.7, 140.0]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(years, advertising, color=REDDIT_ORANGE, label="Advertising")
    ax.bar(years, other, bottom=advertising, color=REDDIT_BLUE,
           label="Other (content/data licensing)")
    totals = [a + o for a, o in zip(advertising, other)]
    for i, (a, o, t) in enumerate(zip(advertising, other, totals)):
        ax.text(i, t + 35, f"${t/1000:.2f}B", ha="center",
                fontsize=10, weight="bold")
        ax.text(i, a / 2, f"${a:,.0f}M", ha="center", fontsize=9, color="white")
        if o > 30:
            ax.text(i, a + o / 2, f"${o:,.0f}M", ha="center",
                    fontsize=9, color="white")
        elif o > 0:
            ax.text(i, a + o + 60, f"Other ${o:,.1f}M", ha="center",
                    fontsize=8, color=REDDIT_BLUE)

    ax.set_ylabel("Revenue (US$ millions)")
    ax.set_ylim(0, 2400)
    ax.set_title("Reddit revenue mix — advertising vs. data/content licensing",
                 fontsize=13, pad=12)
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "rddt_revenue_mix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 3. ARPU by region (US vs Rest of World) -----------------------------
def chart_arpu():
    quarters = ["Q4-23", "Q4-24", "Q4-25", "Q1-26"]
    arpu_us = [5.51, 7.04, 10.79, 9.63]
    arpu_row = [1.34, 1.67, 2.31, 2.02]
    arpu_global = [3.42, 4.21, 5.98, 5.23]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    x = np.arange(len(quarters))
    w = 0.27
    ax.bar(x - w, arpu_us, w, label="United States", color=REDDIT_ORANGE)
    ax.bar(x, arpu_global, w, label="Global", color=GREY)
    ax.bar(x + w, arpu_row, w, label="Rest of world", color=REDDIT_BLUE)
    for i, v in enumerate(arpu_us):
        ax.text(i - w, v + 0.15, f"${v}", ha="center", fontsize=8)
    for i, v in enumerate(arpu_global):
        ax.text(i, v + 0.15, f"${v}", ha="center", fontsize=8)
    for i, v in enumerate(arpu_row):
        ax.text(i + w, v + 0.15, f"${v}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters)
    ax.set_ylabel("ARPU (US$)")
    ax.set_ylim(0, 13)
    ax.set_title("Reddit ARPU by region — quarterly", fontsize=13, pad=12)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "rddt_arpu_region.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 4. P/S vs social-media peers -----------------------------------
def chart_ps_peers():
    peers = ["GOOGL", "RDDT", "META", "PINS", "ROKU", "SNAP"]
    ps_ttm = [11.2, 11.9, 7.2, 2.4, 3.8, 1.6]
    rev_growth = [21.8, 69.1, 33.1, 17.8, 22.4, 12.1]  # %

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    colors = [REDDIT_ORANGE if p == "RDDT" else GREY for p in peers]
    bars = ax.bar(peers, ps_ttm, color=colors)
    for b, p, g in zip(bars, ps_ttm, rev_growth):
        ax.text(b.get_x() + b.get_width() / 2, p + 0.2,
                f"P/S {p:.1f}x\nGrowth {g:.0f}%",
                ha="center", fontsize=8)
    ax.set_ylabel("TTM P/S multiple (x)")
    ax.set_ylim(0, 15)
    ax.set_title("RDDT trades inside the social-media multiple range — but at top-quartile growth",
                 fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(OUT / "rddt_ps_peers.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 5. Stock price since IPO ----------------------------------------
def chart_price():
    months = ["Mar-24", "Jun-24", "Sep-24", "Dec-24", "Mar-25", "Jun-25",
              "Sep-25", "Dec-25", "Mar-26", "May-26"]
    close = [49.32, 63.89, 65.92, 163.44, 104.90, 150.57,
             229.99, 229.87, 134.65, 152.85]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(months, close, color=REDDIT_ORANGE, marker="o", linewidth=2.2)
    for m, c in zip(months, close):
        ax.text(m, c + 6, f"${c:.0f}", ha="center", fontsize=8)
    ax.axhline(34, color=GREY, linestyle="--", alpha=0.5)
    ax.text(0.0, 36, "IPO price $34 (Mar 2024)", color=GREY, fontsize=8)
    ax.set_ylabel("Share price (US$)")
    ax.set_ylim(0, 280)
    ax.set_title("RDDT share price since the March 2024 IPO", fontsize=13, pad=12)
    fig.autofmt_xdate(rotation=30)
    fig.tight_layout()
    fig.savefig(OUT / "rddt_price_history.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 6. Quarterly revenue trend with ad/other split ---------------------
def chart_quarterly_rev():
    q = ["Q1-24", "Q2-24", "Q3-24", "Q4-24",
         "Q1-25", "Q2-25", "Q3-25", "Q4-25", "Q1-26"]
    total = [243.0, 281.2, 348.4, 427.7, 392.4, 500.0, 585.0, 726.0, 663.4]
    other = [20.1, 32.1, 33.2, 29.3, 33.7, 35.0, 31.5, 39.8, 38.7]
    # Note: other revenue Q1-24..Q4-24 derived from disclosures; Q1-25..Q4-25
    # likewise. Estimates for ad = total - other.
    ad = [t - o for t, o in zip(total, other)]

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.bar(q, ad, color=REDDIT_ORANGE, label="Advertising")
    ax.bar(q, other, bottom=ad, color=REDDIT_BLUE, label="Other / licensing")
    for i, t in enumerate(total):
        ax.text(i, t + 12, f"${t:.0f}M", ha="center", fontsize=8, weight="bold")
    ax.set_ylabel("Revenue (US$ millions)")
    ax.set_title("Reddit quarterly revenue — advertising vs. other",
                 fontsize=13, pad=12)
    ax.set_ylim(0, 800)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "rddt_quarterly_revenue.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 7. Gross / operating / net margin trajectory ---------------------
def chart_margins():
    years = ["FY2023", "FY2024", "FY2025"]
    gm = [86.4, 90.5, 91.2]  # gross margin
    om = [-69.7, -29.9, 27.6]  # operating margin (FY24 op loss / FY25 op income)
    nm = [-11.2, -37.2, 24.1]  # net margin

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    x = np.arange(len(years))
    w = 0.25
    ax.bar(x - w, gm, w, color=REDDIT_ORANGE, label="Gross margin")
    ax.bar(x, om, w, color=REDDIT_BLUE, label="Operating margin")
    ax.bar(x + w, nm, w, color=GREY, label="Net margin")
    ax.axhline(0, color="black", linewidth=0.8)
    for i, v in enumerate(gm):
        ax.text(i - w, v + 2, f"{v}%", ha="center", fontsize=8)
    for i, v in enumerate(om):
        ax.text(i, v + (3 if v >= 0 else -6), f"{v}%", ha="center", fontsize=8)
    for i, v in enumerate(nm):
        ax.text(i + w, v + (3 if v >= 0 else -6), f"{v}%", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("Margin (%)")
    ax.set_ylim(-80, 110)
    ax.set_title("Reddit margin trajectory — gross / operating / net",
                 fontsize=13, pad=12)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "rddt_margins.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# 8. P/E ratio — RDDT and peers --------------------------------
def chart_pe_peers():
    peers = ["SNAP", "PINS", "META", "GOOGL", "RDDT", "ROKU"]
    pe_ttm = [None, 39.8, 22.1, 29.8, 43.5, 94.3]
    forward_pe = [None, None, None, None, 17.3, None]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    plot_peers = [p for p, x in zip(peers, pe_ttm) if x is not None]
    plot_vals = [x for x in pe_ttm if x is not None]
    colors = [REDDIT_ORANGE if p == "RDDT" else GREY for p in plot_peers]
    bars = ax.bar(plot_peers, plot_vals, color=colors)
    for b, v in zip(bars, plot_vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}x",
                ha="center", fontsize=9)
    ax.set_ylabel("TTM P/E (x)")
    ax.set_title("TTM P/E vs. peers — RDDT premium narrows when looking forward",
                 fontsize=12, pad=12)
    ax.set_ylim(0, 110)
    ax.annotate(f"RDDT fwd P/E ≈ 17.3x",
                xy=(plot_peers.index("RDDT"), 43.5),
                xytext=(plot_peers.index("RDDT") - 1.2, 75),
                fontsize=9, color=REDDIT_ORANGE,
                arrowprops=dict(arrowstyle="->", color=REDDIT_ORANGE))
    ax.text(0.02, 0.94, "SNAP P/E undefined (negative TTM EPS)",
            transform=ax.transAxes, fontsize=8, color=GREY)
    fig.tight_layout()
    fig.savefig(OUT / "rddt_pe_peers.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    chart_dauq()
    chart_revenue_mix()
    chart_arpu()
    chart_ps_peers()
    chart_price()
    chart_quarterly_rev()
    chart_margins()
    chart_pe_peers()
    print("Wrote charts to", OUT)
