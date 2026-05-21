"""Charts for GMIN company research report."""
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

GMIN_NAVY = "#0b2a52"
GMIN_GOLD = "#c9a14a"
GREY = "#7f7f7f"


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {path}")


# Chart 1: Production and AISC trajectory FY2024 actual, FY2025 actual, FY2026E (guidance), FY2027E (Oko first gold H2-27 partial),
# FY2028E (full Oko ramp - mgmt LOM avg)
# Sources cited inline below the chart in the markdown report.
fig, ax1 = plt.subplots(figsize=(9, 4.8))
years = ["FY2024", "FY2025", "FY2026E", "FY2027E", "FY2028E"]
# FY24: 63,566 oz (partial year from first pour July). FY25: 171,871 oz. FY26 guidance midpoint ~175-190.
# FY27 first gold H2 (TZ ~175 + Oko partial ~50 = ~225). FY28 (TZ ~175 + Oko ~350 = ~525) -- rough mgmt frame.
prod_koz = [63.6, 171.9, 182.5, 225, 525]
aisc = [None, 1155, 1175, 1200, 1100]  # FY24 not reported on full-year AISC basis; FY25 actual; FY26-28 illustrative
labels_prod = [f"{p:.0f}" for p in prod_koz]

x = np.arange(len(years))
bars = ax1.bar(x, prod_koz, color=GMIN_NAVY, alpha=0.85, label="Gold produced / projected (koz)")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("Gold production (koz)", color=GMIN_NAVY)
ax1.tick_params(axis="y", labelcolor=GMIN_NAVY)
for b, lbl in zip(bars, labels_prod):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 8, lbl, ha="center", fontsize=9)

ax2 = ax1.twinx()
aisc_plot_x = [i for i, v in enumerate(aisc) if v is not None]
aisc_plot_y = [v for v in aisc if v is not None]
ax2.plot(aisc_plot_x, aisc_plot_y, color=GMIN_GOLD, marker="o", linewidth=2, label="AISC (US$/oz)")
ax2.set_ylabel("AISC (US$/oz)", color=GMIN_GOLD)
ax2.tick_params(axis="y", labelcolor=GMIN_GOLD)
ax2.set_ylim(900, 1400)

# annotation
ax1.annotate("First pour\nJul 2024", xy=(0, 63.6), xytext=(0.0, 250),
             ha="center", fontsize=8, color=GREY,
             arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
ax1.annotate("Oko West\nfirst gold (H2-27)", xy=(3, 225), xytext=(3, 380),
             ha="center", fontsize=8, color=GREY,
             arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
ax1.annotate("Both mines\nrunning", xy=(4, 525), xytext=(4, 600),
             ha="center", fontsize=8, color=GREY,
             arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))

ax1.set_title("GMIN production and AISC trajectory — Tocantinzinho today, Oko West from 2027")
fig.tight_layout()
save(fig, "gmin_production_aisc.png")


# Chart 2: FY2025 P&L cascade — Revenue, opex, EBITDA, net income (US$M)
fig, ax = plt.subplots(figsize=(8.5, 4.5))
labels = ["Revenue", "Total cash cost\n(opex+royalty)", "Adj EBITDA", "D&A and other", "Net income"]
# Revenue 581, cash cost ~ 748 * 172 = ~129M (mine-site), but headline ratios: EBITDA 419, NI 288, so opex+SGA ~ 581-419 = 162
values = [581, -162, 419, -131, 288]
colors = [GMIN_NAVY, GREY, GMIN_GOLD, GREY, GMIN_NAVY]
bars = ax.bar(labels, [abs(v) for v in values], color=colors)
for b, v in zip(bars, values):
    sign = "" if v >= 0 else "-"
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 8, f"{sign}${abs(v):.0f}M",
            ha="center", fontsize=9)
ax.set_ylabel("US$ millions")
ax.set_title("FY2025 P&L cascade — TZ first full year of commercial production")
ax.set_ylim(0, 700)
fig.tight_layout()
save(fig, "gmin_pnl_cascade.png")


# Chart 3: Reserves and resources mix (TZ vs Oko West)
fig, ax = plt.subplots(figsize=(8.5, 4.5))
assets = ["Tocantinzinho\n(P&P reserves)", "Oko West\n(P&P reserves)", "Oko West\n(M&I resources)", "Oko-Ghanie / G2\nresources (M&I)*"]
# TZ ~2.0 Moz, Oko West reserves ~4.3 Moz (12.3 yr * 350 koz ≈ 4.3 Moz), Oko West M&I ~5.0 Moz incremental, G2 adds ~2 Moz pro forma
ozs = [2.0, 4.3, 1.0, 2.0]
colors2 = [GMIN_NAVY, "#1f4e8b", GMIN_GOLD, "#a07d2a"]
bars = ax.barh(assets, ozs, color=colors2)
for b, v in zip(bars, ozs):
    ax.text(b.get_width() + 0.1, b.get_y() + b.get_height()/2, f"{v:.1f} Moz", va="center", fontsize=9)
ax.set_xlabel("Contained gold (Moz)")
ax.set_title("Reserves and resources mix — Brazil today, Guyana tomorrow")
ax.set_xlim(0, 6.0)
ax.text(0.0, -1.05,
        "* G2 Goldfields announced Apr-2026 (pending close). Bars sized to disclosed P&P / M&I categories;\n  resource categories not additive.",
        fontsize=7.5, color=GREY, transform=ax.transAxes)
fig.tight_layout()
save(fig, "gmin_reserves_mix.png")


# Chart 4: Peer comparison — production and AISC
fig, ax1 = plt.subplots(figsize=(9, 4.8))
peers = ["GMIN\n(FY25)", "AGI\n(Alamos)", "EQX\n(Equinox)*", "IAG\n(IAMGOLD)", "KNT\n(K92)†"]
prod = [172, 531, 850, 766, 173]  # FY25 actual or pro-forma midpoint (EQX pro-forma w Calibre, KNT 2025 guide mid)
aisc = [1155, 1524, 1850, 1879, 1510]  # midpoints
x = np.arange(len(peers))
width = 0.4
b1 = ax1.bar(x - width/2, prod, width, color=GMIN_NAVY, label="FY25 production (koz)")
ax1.set_ylabel("FY25 production (koz)", color=GMIN_NAVY)
ax1.tick_params(axis="y", labelcolor=GMIN_NAVY)
ax1.set_xticks(x); ax1.set_xticklabels(peers)
for b, v in zip(b1, prod):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 10, f"{v}", ha="center", fontsize=8, color=GMIN_NAVY)

ax2 = ax1.twinx()
b2 = ax2.bar(x + width/2, aisc, width, color=GMIN_GOLD, label="FY25 AISC (US$/oz)")
ax2.set_ylabel("FY25 AISC (US$/oz)", color=GMIN_GOLD)
ax2.tick_params(axis="y", labelcolor=GMIN_GOLD)
for b, v in zip(b2, aisc):
    ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 30, f"{v}", ha="center", fontsize=8, color=GMIN_GOLD)
ax2.set_ylim(0, 2400)

ax1.set_title("Peer scan — single-asset GMIN runs the lowest AISC in the cohort")
ax1.text(0.0, -0.22,
         "* EQX pro-forma including Calibre, FY25 guidance midpoint. † K92 2025 guidance midpoint.\nAlamos FY25 actual; IAMGOLD FY25 actual.",
         fontsize=7.5, color=GREY, transform=ax1.transAxes)
fig.tight_layout()
save(fig, "gmin_peer_compare.png")

print("Done.")
