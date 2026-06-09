#!/usr/bin/env python3
"""Chart renderer for the medical / surgical-robotics theme.
Renders the required minimum set (anchor, razor-and-blade, performance,
valuation) to reports/charts/theme_medical-surgical-robotics_*.png.
Headless (Agg). Global chart rules: in-image source footer, x-axis clipped
to data, latest point covers now, derived series show components.

Data are dated, third-party-sourced numbers gathered 2026-06-09 (yfinance
live for prices/returns; broker TAM/installed-base from the cited zsxq notes;
third-party TAM from Grand View / MarketsandMarkets / Precedence / GS).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SLUG = "medical-surgical-robotics"
OUT = "reports/charts/theme_%s_%s.png"
FOOT = dict(fontsize=7, color="#666", style="italic")
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": .25,
                     "font.family": ["Arial Unicode MS", "Hiragino Sans GB", "STHeiti", "DejaVu Sans"],
                     "axes.unicode_minus": False})


def esc(s):
    return s.replace("$", r"\$")


def footer(fig, txt):
    fig.text(0.005, 0.005, esc(txt), **FOOT)


# ---------------------------------------------------------------- 1. anchor
def chart_anchor():
    # Global surgical-robot SYSTEMS+I&A market TAM ($bn), by named forecaster.
    series = {
        "Grand View Research":        {2024: 11.48, 2030: 23.13},
        "MarketsandMarkets":          {2024: 11.98, 2025: 13.69, 2030: 27.14},
        "Precedence Research":        {2025: 12.49, 2035: 50.29},
        "Fortune Business Insights":  {2025: 15.85, 2034: 59.36},
        "Goldman Sachs (zsxq)":       {2035: 42.0},   # GS: $42bn global by 2035 ($19bn OUS)
    }
    colors = {"Grand View Research": "#1f77b4", "MarketsandMarkets": "#2ca02c",
              "Precedence Research": "#ff7f0e", "Fortune Business Insights": "#9467bd",
              "Goldman Sachs (zsxq)": "#d62728"}
    # da Vinci procedures (ISRG primary) — the procedure-pool component.
    proc = {2024: 2.683, 2025: 3.153}  # millions, worldwide da Vinci procedures

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 6))

    for name, pts in series.items():
        xs = sorted(pts)
        ys = [pts[x] for x in xs]
        if len(xs) > 1:
            axL.plot(xs, ys, "-o", color=colors[name], lw=2, ms=5, label=name)
        else:
            axL.plot(xs, ys, "*", color=colors[name], ms=16, label=name)
            axL.annotate(f"  \${ys[0]:.0f}bn", (xs[0], ys[0]), color=colors[name], fontsize=9, va="center")
    axL.set_title("Global surgical-robot market TAM — systems + instruments & service ($bn)", fontsize=10)
    axL.set_xlabel("Year"); axL.set_ylabel("Market size (US$bn)")
    axL.set_xlim(2023.5, 2035.5)
    axL.legend(fontsize=7, loc="upper left")
    axL.annotate("Consensus today ~\$11–16bn →\n~\$23–27bn by 2030; \$42–50bn by 2035",
                 (2024.0, 45), fontsize=8, color="#444")

    # Procedure pool (the installed-base / utilization anchor)
    yrs = sorted(proc)
    axR.bar([str(y) for y in yrs], [proc[y] for y in yrs], color="#1f77b4", width=0.5,
            label="da Vinci procedures (ISRG, actual)")
    axR.axhline(9.0, color="#2ca02c", ls="--", lw=1.5, label="~9M robotic procedures today (UBS)")
    axR.axhline(12.0, color="#ff7f0e", ls="--", lw=1.5, label="12M robotic surgeries by 2035E (GS)")
    axR.axhline(23.0, color="#d62728", ls=":", lw=1.5, label="~23M ultimate addressable (UBS TAM)")
    axR.set_title("Robotic-surgery procedure pool (M procedures/yr) — the recurring-revenue anchor", fontsize=10)
    axR.set_ylabel("Procedures (millions / yr)")
    axR.set_ylim(0, 25)
    for i, y in enumerate(yrs):
        axR.annotate(f"{proc[y]:.2f}M", (i, proc[y] + 0.3), ha="center", fontsize=8)
    axR.legend(fontsize=7, loc="upper left")

    fig.suptitle("Surgical-robotics theme — TAM anchor: market dollars + procedure pool", fontsize=12, y=0.98)
    footer(fig, "Source: Grand View Research, MarketsandMarkets, Precedence Research, Fortune Business Insights (surgical-robot market reports, 2024–25); "
                "Goldman Sachs 'China Medtech Going Global' (zsxq #585582881584284, $42bn global / $19bn OUS by 2035); "
                "procedures from Intuitive Surgical FY24/FY25 releases (isrg.intuitive.com); UBS ISRG note (zsxq #585581521118154, ~9M today→~23M TAM). Compiled 2026-06-09.")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(OUT % (SLUG, "anchor"), dpi=130); plt.close(fig)


# ---------------------------------------------------- 2. razor-and-blade
def chart_razor_blade():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.5))

    # ISRG Q1 2026 revenue mix ($bn): total 2.77; I&A 1.69; recurring 86% => service ~0.69; systems ~0.39
    labels = ["Instruments &\naccessories\n(the 'blade')", "Service", "Systems\n(the 'razor')"]
    vals = [1.69, 0.69, 0.39]
    cols = ["#1f77b4", "#6baed6", "#c6dbef"]
    axL.bar(labels, vals, color=cols)
    for i, v in enumerate(vals):
        axL.annotate(f"\${v:.2f}bn", (i, v + 0.03), ha="center", fontsize=9)
    axL.set_title("ISRG Q1'26 revenue mix — recurring = 86% of \$2.77bn", fontsize=10)
    axL.set_ylabel("Revenue (US$bn)")
    axL.annotate("Recurring (I&A + service) = 86%\nInstalled base 11,395 systems × ~300 proc/yr",
                 (0.02, 0.82), xycoords="axes fraction", fontsize=8, color="#444")

    # MedBot consumables revenue contribution ramp (early flywheel)
    yrs = ["2025", "2026E", "2027E", "2028E"]
    mix = [5, 13, 17, 21]
    axR.bar(yrs, mix, color="#2ca02c", width=0.55)
    for i, v in enumerate(mix):
        axR.annotate(f"{v}%", (i, v + 0.4), ha="center", fontsize=9)
    axR.set_title("MicroPort MedBot (2252.HK) consumables % of revenue — flywheel starting", fontsize=10)
    axR.set_ylabel("Consumables % of revenue")
    axR.set_ylim(0, 25)
    axR.annotate("China names are early in the razor-blade transition\n(FY24 ~98% systems); ISRG is the mature model",
                 (0.04, 0.78), xycoords="axes fraction", fontsize=8, color="#444")

    fig.suptitle("Razor-and-blade economics — installed base × utilization × recurring attach", fontsize=12, y=0.99)
    footer(fig, "Source: Intuitive Surgical Q1 2026 release — I&A $1.69bn, recurring 86% of $2.77bn total, installed base 11,395 systems (stocktitan.net / isrg.intuitive.com); "
                "MedBot consumables mix from Goldman Sachs China surgical-robot initiation (zsxq #212215118214521, p.3). Compiled 2026-06-09.")
    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    fig.savefig(OUT % (SLUG, "razor_blade"), dpi=130); plt.close(fig)


# ------------------------------------------------------------ 3. performance
def chart_performance():
    # 1Y total return (%), yfinance auto_adjust, as of 2026-06-09.
    rows = [
        ("JNJ +53% (mostly non-robot)", 53.3, "#c6dbef"),
        ("MedBot 2252.HK", 49.9, "#1f77b4"),
        ("TINAVI 688277", 27.3, "#1f77b4"),
        ("MDT (Hugo)", -4.8, "#9ecae1"),
        ("SYK (Mako)", -20.4, "#9ecae1"),
        ("ISRG (da Vinci)", -20.4, "#1f77b4"),
        ("EdgeMed 2675.HK*", -27.1, "#1f77b4"),
    ]
    rows.sort(key=lambda r: r[1])
    names = [r[0] for r in rows]; vals = [r[1] for r in rows]; cols = [r[2] for r in rows]
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(range(len(vals)), vals, color=cols)
    ax.set_yticks(range(len(vals))); ax.set_yticklabels(names)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:+.0f}%", (v + (1 if v >= 0 else -1), i), va="center",
                    ha="left" if v >= 0 else "right", fontsize=8)
    # benchmarks
    bm = [("IHI US Med-Devices ETF -18.8%", -18.8, "#d62728"),
          ("S&P 500 +24.8%", 24.8, "#7f7f7f"),
          ("CSI 300 +26.9%", 26.9, "#ff7f0e"),
          ("Hang Seng +6.3%", 6.3, "#9467bd")]
    for lbl, v, c in bm:
        ax.axvline(v, color=c, ls="--", lw=1.3, label=lbl)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("1-year total return (%)")
    ax.set_title("Surgical-robotics basket — 1Y total return vs benchmarks (as of 2026-06-09)", fontsize=11)
    ax.legend(fontsize=7, loc="lower right")
    footer(fig, "Source: yfinance auto_adjust=True, 1Y total return to 2026-06-09. *EdgeMed (2675.HK) shown since its 2026-01-08 IPO (~5mo, not a full year). "
                "Benchmarks: IHI (iShares US Medical Devices), ^GSPC, CSI 300 (510300.SS), ^HSI. US names (ISRG/SYK/MDT) are IHI constituents — the sector, not the broad market, is the fair benchmark.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT % (SLUG, "performance"), dpi=130); plt.close(fig)


# ------------------------------------------------------------- 4. valuation
def chart_valuation():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.5))
    # US names — NTM fwd P/E; ISRG own 5yr-avg fwd P/E overlay
    us = [("ISRG", 35.5), ("SYK", 18.0), ("MDT", 12.6), ("JNJ", 18.3)]
    n = [u[0] for u in us]; pe = [u[1] for u in us]
    axL.bar(n, pe, color=["#1f77b4", "#9ecae1", "#9ecae1", "#c6dbef"])
    for i, v in enumerate(pe):
        axL.annotate(f"{v:.0f}x", (i, v + 0.4), ha="center", fontsize=9)
    axL.scatter([0], [56], color="#d62728", zorder=5, s=80, marker="_", linewidths=3)
    axL.annotate("ISRG 5yr-avg fwd P/E ~56x\n(now 35.5x → BELOW own history\nafter the -26% YTD de-rate)",
                 (0.05, 8), fontsize=8, color="#d62728")
    axL.set_title("US incumbents — NTM forward P/E", fontsize=10)
    axL.set_ylabel("NTM P/E (x)"); axL.set_ylim(0, 62)

    # China pre-profit names — P/S; GS 2026E-implied P/S overlay
    cn = [("MedBot\n2252.HK", 46.5, 39), ("EdgeMed\n2675.HK", 35.5, 34), ("TINAVI\n688277", 28.4, 28)]
    cn_n = [c[0] for c in cn]; ps = [c[1] for c in cn]; gsimp = [c[2] for c in cn]
    x = np.arange(len(cn_n))
    axR.bar(x, ps, width=0.5, color="#2ca02c", label="Current TTM P/S")
    axR.scatter(x, gsimp, color="#d62728", zorder=5, s=70, marker="D", label="GS 2026E-implied P/S (at TP)")
    for i, v in enumerate(ps):
        axR.annotate(f"{v:.0f}x", (i, v + 0.8), ha="center", fontsize=9)
    axR.axhline(15, color="#7f7f7f", ls="--", lw=1.3, label="ISRG 5yr-avg fwd P/S ~15x")
    axR.set_xticks(x); axR.set_xticklabels(cn_n)
    axR.set_title("China pure-plays — TTM P/S (pre-profit) — priced-for-perfection flag", fontsize=10)
    axR.set_ylabel("P/S (x)"); axR.set_ylim(0, 52)
    axR.legend(fontsize=7, loc="upper right")

    fig.suptitle("Valuation — US incumbents vs own history; China pure-plays rich vs the global benchmark", fontsize=12, y=0.99)
    footer(fig, "Source: yfinance (current px/mcap → P/E, P/S) 2026-06-09; ISRG 5yr-avg fwd P/E ~56x & fwd P/S ~15x and GS 2026E-implied P/S from Goldman Sachs notes "
                "(zsxq #212215118214521 / #585582881584284). China names are loss-making → P/S, not P/E. The ~29–47x P/S vs ISRG's ~15x 5yr-avg is the air-pocket risk if order/utilization ramp disappoints.")
    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    fig.savefig(OUT % (SLUG, "valuation"), dpi=130); plt.close(fig)


if __name__ == "__main__":
    chart_anchor()
    chart_razor_blade()
    chart_performance()
    chart_valuation()
    print("rendered 4 charts to reports/charts/theme_%s_*.png" % SLUG)
