"""Generate Zeta Global research-report charts."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# Style
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})

# ── Chart 1: Revenue + Adjusted EBITDA (FY2020–FY2025) ─────────────────
years = [2020, 2021, 2022, 2023, 2024, 2025]
revenue = [368.1, 458.3, 591.0, 728.7, 1005.8, 1304.7]
adj_ebitda = [39.6, 63.3, 92.2, 129.4, 193.0, 278.7]
adj_ebitda_margin = [a / r * 100 for a, r in zip(adj_ebitda, revenue)]

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
bars = ax1.bar([y - 0.2 for y in years], revenue, width=0.4, color="#1f4e79",
               label="Revenue ($M)")
bars2 = ax1.bar([y + 0.2 for y in years], adj_ebitda, width=0.4, color="#5b9bd5",
                label="Adj EBITDA ($M)")
line = ax2.plot(years, adj_ebitda_margin, "o-", color="#c00000",
                linewidth=2.5, markersize=7, label="Adj EBITDA margin (%)")
ax1.set_xlabel("Fiscal year")
ax1.set_ylabel("USD millions")
ax2.set_ylabel("Adj EBITDA margin (%)", color="#c00000")
ax2.tick_params(axis="y", colors="#c00000")
ax2.grid(False)
ax1.set_title("Zeta Global — revenue and adjusted EBITDA, FY2020–FY2025")
for y, r in zip(years, revenue):
    ax1.text(y - 0.2, r + 25, f"{r:,.0f}", ha="center", fontsize=8)
for y, e, m in zip(years, adj_ebitda, adj_ebitda_margin):
    ax1.text(y + 0.2, e + 25, f"{e:,.0f}", ha="center", fontsize=8)
    ax2.text(y, m + 0.6, f"{m:.1f}%", ha="center", fontsize=8, color="#c00000")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.tight_layout()
plt.savefig(OUT / "zeta_revenue_ebitda.png", dpi=150, bbox_inches="tight")
plt.close()

# ── Chart 2: ARPU + scaled / super-scaled customer counts (FY2024–FY2025) ─
# Using disclosed: FY2024 527 scaled, 148 super-scaled; FY2025 602 scaled, 184 super-scaled
periods = ["FY2024", "FY2025"]
scaled = [527, 602]
super_scaled = [148, 184]
arpu_scaled = [1868, 2109]      # USD '000s
arpu_super = [5713, 6156]       # USD '000s

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
x = np.arange(len(periods))
w = 0.35
axes[0].bar(x - w / 2, scaled, w, color="#1f4e79", label="Scaled customers (≥$100k)")
axes[0].bar(x + w / 2, super_scaled, w, color="#5b9bd5", label="Super-scaled (≥$1M)")
for i, (s, ss) in enumerate(zip(scaled, super_scaled)):
    axes[0].text(i - w / 2, s + 8, str(s), ha="center", fontsize=9)
    axes[0].text(i + w / 2, ss + 8, str(ss), ha="center", fontsize=9)
axes[0].set_xticks(x)
axes[0].set_xticklabels(periods)
axes[0].set_ylabel("Customer count (period-end)")
axes[0].set_title("Scaled & super-scaled customer counts")
axes[0].legend()

axes[1].bar(x - w / 2, [a / 1000 for a in arpu_scaled], w, color="#1f4e79",
            label="Scaled ARPU ($M)")
axes[1].bar(x + w / 2, [a / 1000 for a in arpu_super], w, color="#5b9bd5",
            label="Super-scaled ARPU ($M)")
for i, (s, ss) in enumerate(zip(arpu_scaled, arpu_super)):
    axes[1].text(i - w / 2, s / 1000 + 0.1, f"${s/1000:.2f}M", ha="center", fontsize=9)
    axes[1].text(i + w / 2, ss / 1000 + 0.1, f"${ss/1000:.2f}M", ha="center", fontsize=9)
axes[1].set_xticks(x)
axes[1].set_xticklabels(periods)
axes[1].set_ylabel("ARPU (USD millions)")
axes[1].set_title("Average revenue per user (annual)")
axes[1].legend()

fig.suptitle("Zeta Global — customer counts and ARPU (annual)", y=1.02)
plt.tight_layout()
plt.savefig(OUT / "zeta_customers_arpu.png", dpi=150, bbox_inches="tight")
plt.close()

# ── Chart 3: P/S vs martech peers ───────────────────────────────────────
peers = ["ZETA", "HUBS", "KVYO", "BRZE", "CRM"]
# Pulled from yfinance 2026-05-21
ps_ttm = [3.16, 3.10, 3.43, 3.46, 3.48]
ev_rev = [3.13, 2.72, 2.79, 3.06, np.nan]
rev_growth_ttm = [29.7, 17.0, 28.0, 26.0, 8.0]  # approximate latest TTM growth %, peer values rough
fig, ax = plt.subplots(figsize=(9, 5))
xpos = np.arange(len(peers))
w = 0.4
b1 = ax.bar(xpos - w / 2, ps_ttm, w, color="#1f4e79", label="P/S TTM")
b2 = ax.bar(xpos + w / 2, [v if not np.isnan(v) else 0 for v in ev_rev], w,
            color="#5b9bd5", label="EV/Revenue TTM")
for i, v in enumerate(ps_ttm):
    ax.text(i - w / 2, v + 0.05, f"{v:.2f}x", ha="center", fontsize=9)
for i, v in enumerate(ev_rev):
    if not np.isnan(v):
        ax.text(i + w / 2, v + 0.05, f"{v:.2f}x", ha="center", fontsize=9)
    else:
        ax.text(i + w / 2, 0.2, "n/a", ha="center", fontsize=9)
ax.set_xticks(xpos)
ax.set_xticklabels(peers)
ax.set_ylabel("Multiple")
ax.set_title("Zeta Global vs. martech peers — P/S TTM & EV/Revenue (2026-05-21)")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "zeta_ps_peers.png", dpi=150, bbox_inches="tight")
plt.close()

# ── Chart 4: Price chart since IPO ─────────────────────────────────────
# Plot ZETA share price since June 10, 2021 IPO; annotate Culper short report
import yfinance as yf
t = yf.Ticker("ZETA")
hist = t.history(period="max")[["Close"]]
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(hist.index, hist["Close"], color="#1f4e79", linewidth=1.4)
ax.set_title("Zeta Global (NYSE: ZETA) — share price since IPO (2021-06-10)")
ax.set_ylabel("USD")
import pandas as pd
# annotate Culper short report Nov 13 2024
culper_date = pd.Timestamp("2024-11-13", tz="America/New_York")
ipo_date = pd.Timestamp("2021-06-10", tz="America/New_York")
marigold_date = pd.Timestamp("2025-11-24", tz="America/New_York")
athena_date = pd.Timestamp("2026-03-24", tz="America/New_York")
def annot(d, label, color="#c00000", offset_y=2):
    if d in hist.index:
        y = hist.loc[d, "Close"]
    else:
        y = hist[hist.index <= d]["Close"].iloc[-1]
    ax.axvline(d, color=color, linestyle="--", alpha=0.6, linewidth=1)
    ax.annotate(label, xy=(d, y), xytext=(0, offset_y), textcoords="offset points",
                fontsize=8, color=color, rotation=0)
annot(ipo_date, "IPO\n$10.00 listing", color="#404040", offset_y=10)
annot(culper_date, "Culper short report\n(2024-11-13, −37%)", offset_y=15)
annot(marigold_date, "Marigold close\n(2025-11-24)", color="#0070c0", offset_y=12)
annot(athena_date, "Athena GA\n(2026-03-24)", color="#0070c0", offset_y=10)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(OUT / "zeta_price_history.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written:")
for p in sorted(OUT.glob("*.png")):
    print(" ", p)
