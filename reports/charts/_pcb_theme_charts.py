#!/usr/bin/env python3
"""Chart renderer for the PCB / HDI / ABF substrate theme.
Renders the required minimum set (anchor, performance, valuation) to
reports/charts/theme_pcb-hdi-abf-substrate_*.png. Headless (Agg).
Global chart rules: in-image source footer, x-axis clipped to data,
latest point covers now, derived series show components.
"""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SLUG = "pcb-hdi-abf-substrate"
OUT = "reports/charts/theme_%s_%s.png"
FOOT = dict(fontsize=7, color="#666", style="italic")
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": .25,
                     "font.family": ["Arial Unicode MS", "Hiragino Sans GB", "STHeiti", "DejaVu Sans"],
                     "axes.unicode_minus": False})


def esc(s):  # matplotlib treats $ as a math delimiter — escape literal dollars
    return s.replace("$", r"\$")


def footer(fig, txt):
    fig.text(0.005, 0.005, esc(txt), **FOOT)


# ---------------------------------------------------------------- performance
def chart_performance(perf_path, members, bench_keys):
    d = json.load(open(perf_path))
    rows = [(d["members"][t]["name"], d["members"][t]["ret_1y"]) for t in members
            if t in d["members"] and "ret_1y" in d["members"][t]]
    rows.sort(key=lambda r: r[1])
    names = [r[0].split(" (")[0] for r in rows]
    vals = [r[1] for r in rows]
    med = float(np.median(vals)); mean = float(np.mean(vals))
    fig, ax = plt.subplots(figsize=(10, 9))
    colors = ["#1f77b4" if v >= med else "#9ecae1" for v in vals]
    ax.barh(range(len(vals)), vals, color=colors)
    ax.set_yticks(range(len(vals))); ax.set_yticklabels(names, fontsize=8)
    for i, v in enumerate(vals):
        ax.text(v + 8, i, f"{v:.0f}%", va="center", fontsize=7, color="#333")
    bcol = {"SOXX": "#d62728", "^TWII": "#2ca02c", "^GSPC": "#7f7f7f", "SMH": "#ff7f0e", "000300.SS": "#9467bd"}
    for bk in bench_keys:
        bv = d["bench"][bk]["ret_1y"]; bn = d["bench"][bk]["name"]
        ax.axvline(bv, color=bcol.get(bk, "#444"), ls="--", lw=1.2, alpha=.8)
        ax.text(bv, len(vals) - 0.3, f" {bn} +{bv:.0f}%", rotation=90,
                va="top", ha="left", fontsize=7, color=bcol.get(bk, "#444"))
    ax.axvline(med, color="black", ls="-", lw=1.5, alpha=.6)
    ax.text(med, -0.9, f"basket median +{med:.0f}%", fontsize=8, fontweight="bold", ha="center")
    ax.set_xlabel("Trailing 1-year total return (%, yfinance auto_adjust, to 2026-06-08/09)")
    ax.set_title("PCB / HDI / ABF substrate basket — 1Y return vs benchmarks\n"
                 f"equal-weight +{mean:.0f}% · median +{med:.0f}% · a real melt-up (spot-checks corroborated) — read median-vs-benchmark, not any single print",
                 fontsize=10)
    ax.margins(y=0.01)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    footer(fig, "Source: yfinance auto_adjust=True 1Y closes (pulled 2026-06-09). Benchmarks: iShares SOXX, VanEck SMH, TAIEX, S&P 500, CSI 300. "
                "Magnitudes are extreme but spot-checked against independent quotes (Ibiden +533%, Unimicron 52-wk NT$98->1,130, EMC NT$680->5,215, SEMCO ~10x) — corroborated, not an auto_adjust artifact. Median-vs-benchmark is the signal.")
    fig.savefig(OUT % (SLUG, "performance"), dpi=130)
    print("wrote", OUT % (SLUG, "performance"), "median", round(med, 1), "mean", round(mean, 1))


# ---------------------------------------------------------------- anchor
def chart_anchor(anchor_json):
    """anchor_json: {'title','unit','source','years':[...],'buckets':{name:[vals...]}}"""
    a = json.load(open(anchor_json)) if isinstance(anchor_json, str) else anchor_json
    years = a["years"]; buckets = a["buckets"]
    fig, ax = plt.subplots(figsize=(10, 6))
    bottoms = np.zeros(len(years))
    palette = ["#08519c", "#3182bd", "#6baed6", "#bdd7e7", "#c6dbef"]
    for i, (bn, vals) in enumerate(buckets.items()):
        ax.bar(years, vals, bottom=bottoms, label=bn, color=palette[i % len(palette)])
        bottoms += np.array(vals, float)
    for x, tot in zip(years, bottoms):
        ax.text(x, tot, f"{tot:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_ylabel(a["unit"]); ax.set_title(esc(a["title"]), fontsize=11)
    ax.legend(fontsize=8, loc="upper left")
    if a.get("sd"):  # supply/demand ratio overlay on secondary axis
        ax2 = ax.twinx()
        sx = a["sd"]["years"]; sy = a["sd"]["vals"]
        ax2.plot(sx, sy, "o-", color="#d62728", lw=2, label="ABF supply/demand ratio (RHS)")
        ax2.axhline(100, color="#d62728", ls=":", lw=1, alpha=.6)
        ax2.text(sx[0], 100.4, "100% = balanced", fontsize=7, color="#d62728")
        for xx, yy in zip(sx, sy):
            ax2.text(xx, yy + 1.0, f"{yy:.0f}%", ha="center", fontsize=7, color="#d62728")
        ax2.set_ylabel("ABF supply/demand ratio (%)", color="#d62728")
        ax2.tick_params(axis="y", colors="#d62728")
        ax2.set_ylim(85, 130); ax2.grid(False)
        ax2.legend(fontsize=8, loc="upper center")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    footer(fig, a["source"])
    fig.savefig(OUT % (SLUG, "anchor"), dpi=130)
    print("wrote", OUT % (SLUG, "anchor"))


# ---------------------------------------------------------------- valuation
def chart_valuation(val_json):
    """val_json: {'source','rows':[{'name','fwd','avg'}...]}"""
    v = json.load(open(val_json)) if isinstance(val_json, str) else val_json
    rows = v["rows"]
    names = [r["name"] for r in rows]
    fwd = [r["fwd"] for r in rows]; avg = [r["avg"] for r in rows]
    x = np.arange(len(names)); w = 0.38
    fig, ax = plt.subplots(figsize=(11, 6))
    has_avg = [a_ > 0 for a_ in avg]
    ax.bar([xi - w / 2 if h else xi for xi, h in zip(x, has_avg)],
           fwd, w, label="current fwd P/E", color="#d62728")
    ax.bar([xi + w / 2 for xi, h in zip(x, has_avg) if h],
           [a_ for a_, h in zip(avg, has_avg) if h], w,
           label="own ~upcycle-avg fwd P/E (ABF primes, GS)", color="#aaaaaa")
    for i, (f, a_, h) in enumerate(zip(fwd, avg, has_avg)):
        ax.text(i - w / 2 if h else i, f, f"{f:.0f}", ha="center", va="bottom", fontsize=7)
        if h:
            ax.text(i + w / 2, a_, f"{a_:.0f}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Forward P/E (x)")
    ax.set_title("Core names: current forward P/E vs own long-run average — priced-for-perfection check", fontsize=11)
    ax.legend(fontsize=8)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    footer(fig, v["source"])
    fig.savefig(OUT % (SLUG, "valuation"), dpi=130)
    print("wrote", OUT % (SLUG, "valuation"))


# ---------------------------------------------------------------- demand build (bottom-up)
def chart_demand_build(cfg):
    """Stacked AI-ASIC unit drivers (M units) that build the ABF/substrate demand anchor."""
    c = json.load(open(cfg)) if isinstance(cfg, str) else cfg
    years = c["years"]; series = c["series"]
    fig, ax = plt.subplots(figsize=(10, 6))
    bottoms = np.zeros(len(years))
    palette = ["#2c7fb8", "#41b6c4", "#fe9929"]
    for i, (nm, vals) in enumerate(series.items()):
        ax.bar(years, vals, bottom=bottoms, label=nm, color=palette[i % len(palette)])
        bottoms += np.array(vals, float)
    for x, tot in zip(years, bottoms):
        ax.text(x, tot, f"{tot:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_ylabel(c["unit"]); ax.set_title(esc(c["title"]), fontsize=11)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout(rect=[0, 0.03, 1, 1]); footer(fig, c["source"])
    fig.savefig(OUT % (SLUG, "demand_build"), dpi=130); print("wrote", OUT % (SLUG, "demand_build"))


# ---------------------------------------------------------------- supply/demand balance
def chart_sd_balance(cfg):
    """Two-panel upstream S/D balance: demand vs supply/capacity in physical units."""
    c = json.load(open(cfg)) if isinstance(cfg, str) else cfg
    panels = c["panels"]
    fig, axes = plt.subplots(1, len(panels), figsize=(12, 5.5))
    if len(panels) == 1:
        axes = [axes]
    for ax, p in zip(axes, panels):
        x = np.arange(len(p["years"])); w = 0.38
        ax.bar(x - w / 2, p["demand"], w, label="Demand", color="#08519c")
        ax.bar(x + w / 2, p["supply"], w, label="Supply / capacity", color="#9ecae1")
        for i, (d, s) in enumerate(zip(p["demand"], p["supply"])):
            ax.text(i - w / 2, d, f"{d:g}", ha="center", va="bottom", fontsize=7)
            ax.text(i + w / 2, s, f"{s:g}", ha="center", va="bottom", fontsize=7)
        ax.set_xticks(x); ax.set_xticklabels(p["years"]); ax.set_ylabel(p["unit"])
        ax.set_title(esc(p["title"]), fontsize=9.5); ax.legend(fontsize=8)
        if p.get("gap_note"):
            ax.text(0.5, 0.93, p["gap_note"], transform=ax.transAxes, ha="center",
                    fontsize=8, color="#d62728", fontweight="bold")
    fig.suptitle(esc(c["title"]), fontsize=11)
    fig.tight_layout(rect=[0, 0.04, 1, 0.96]); footer(fig, c["source"])
    fig.savefig(OUT % (SLUG, "sd_balance"), dpi=130); print("wrote", OUT % (SLUG, "sd_balance"))


if __name__ == "__main__":
    import sys
    if sys.argv[1] == "demand":
        chart_demand_build(sys.argv[2])
    elif sys.argv[1] == "sd":
        chart_sd_balance(sys.argv[2])
    elif sys.argv[1] == "perf":
        members = json.load(open(sys.argv[2]))
        chart_performance("/tmp/pcb_perf.json", members, ["SOXX", "^TWII", "^GSPC"])
    elif sys.argv[1] == "anchor":
        chart_anchor(sys.argv[2])
    elif sys.argv[1] == "val":
        chart_valuation(sys.argv[2])
