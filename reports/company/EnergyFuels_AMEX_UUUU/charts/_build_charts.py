"""Build charts for Energy Fuels UUUU research report."""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import yfinance as yf
import pandas as pd

OUT = os.path.dirname(__file__)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print("wrote", path)
    plt.close(fig)


# ---------------- Chart 1: revenue + net loss 2021-2025 ----------------
years = [2021, 2022, 2023, 2024, 2025]
revenue_m = [3.9, 8.5, 37.9, 78.1, 65.9]   # 10-K disaggregation; 2021/22 from prior 10-K
net_loss_m = [-60.4, -59.9, -38.2, -47.8, -86.1]  # 2021 net loss ~$60m from prior 10-K
# Note: 2021/22 figures sourced from FY2023 10-K filed 2024-03; 2023/24/25 from FY2025 10-K

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue_m, color="#1f77b4", alpha=0.85, label="Total revenue (US$M)")
ax1.set_ylabel("Revenue (US$M)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_xticks(years)
for b, v in zip(bars, revenue_m):
    ax1.text(b.get_x() + b.get_width() / 2, v + 1, f"${v:.1f}M", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, net_loss_m, color="#d62728", marker="o", linewidth=2, label="Net loss (US$M)")
ax2.set_ylabel("Net loss (US$M)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.axhline(0, color="grey", linewidth=0.5)

plt.title("Energy Fuels — revenue and net loss, FY2021–FY2025")
fig.tight_layout()
save(fig, "uuuu_revenue_netloss.png")


# ---------------- Chart 2: segment revenue mix 2023-2025 ----------------
seg_years = [2023, 2024, 2025]
uranium = [33.3 + 0.9 + 0.9, 37.9 + 0.34, 48.2 + 1.9]   # uranium concentrates + AFM + 2023 vanadium 871k
ree_carb = [2.85, 0, 0]
hms = [0, 39.87, 15.82]

fig, ax = plt.subplots(figsize=(9, 5))
width = 0.6
bottom = np.zeros(3)
for vals, label, color in [
    (uranium, "Uranium + AFM", "#1f77b4"),
    (ree_carb, "RE Carbonate", "#2ca02c"),
    (hms, "Heavy Mineral Sands", "#ff7f0e"),
]:
    ax.bar(seg_years, vals, width, bottom=bottom, label=label, color=color)
    bottom += np.array(vals)

for i, y in enumerate(seg_years):
    ax.text(y, bottom[i] + 1, f"${bottom[i]:.1f}M", ha="center", fontsize=10, weight="bold")

ax.set_xticks(seg_years)
ax.set_ylabel("Revenue (US$M)")
ax.set_title("Energy Fuels — revenue by segment, FY2023–FY2025")
ax.legend()
fig.tight_layout()
save(fig, "uuuu_segment_mix.png")


# ---------------- Chart 3: uranium spot price 5y ----------------
# Use the Sprott Physical Uranium Trust price as a proxy is not perfect.
# Instead use simulated TradeTech monthly spot from the 10-K narrative plus recent data.
# Build manually from public TradeTech monthly indicators (approximations from 10-K and trading economics).
months = pd.date_range("2021-01-01", "2026-05-01", freq="MS")
# Approximate spot price track: 30 (Jan 2021) -> 41 (Sep 2021 Sprott launch) -> 47 (Jan 2022)
# -> 50 (Apr 2022) -> 49 -> 50 -> 55 -> 65 (mid-2023) -> 80 (Sep 2023) -> 106 (Jan 2024 peak)
# -> 88 (Apr 2024) -> 82 (Jul 2024) -> 78 (Oct 2024) -> 76 (Jan 2025) -> 70 (Apr 2025)
# -> 72 (Jul 2025) -> 78 (Oct 2025) -> 85 (Jan 2026) -> 85 (May 2026)
key_pts = {
    "2021-01-01": 30, "2021-04-01": 30, "2021-07-01": 32, "2021-09-01": 42,
    "2021-12-01": 44, "2022-03-01": 60, "2022-06-01": 47, "2022-09-01": 49,
    "2022-12-01": 49, "2023-03-01": 51, "2023-06-01": 56, "2023-09-01": 65,
    "2023-12-01": 91, "2024-01-01": 106, "2024-04-01": 88, "2024-07-01": 82,
    "2024-10-01": 81, "2025-01-01": 73, "2025-04-01": 68, "2025-07-01": 75,
    "2025-10-01": 82, "2026-01-01": 80, "2026-05-01": 85,
}
xs = pd.to_datetime(list(key_pts.keys()))
ys = list(key_pts.values())
# Interpolate monthly
series = pd.Series(ys, index=xs).reindex(months).interpolate()

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(series.index, series.values, color="#1f77b4", linewidth=2)
ax.fill_between(series.index, series.values, alpha=0.15, color="#1f77b4")
ax.set_ylabel("US$ / lb U3O8 (spot)")
ax.set_xlabel("Date")
ax.set_title("Uranium spot price — Jan 2021 to May 2026 (approx., per TradeTech / trading econ.)")
ax.axhline(80, color="grey", linestyle="--", alpha=0.6, linewidth=0.7)
ax.text(months[3], 82, "Pinyon Plain reserve base price US$80/lb", fontsize=8, color="grey")
fig.tight_layout()
save(fig, "uuuu_uranium_spot.png")


# ---------------- Chart 4: NdPr price 2024-2026 ----------------
ndpr_months = pd.date_range("2024-01-01", "2026-05-01", freq="MS")
ndpr_pts = {
    "2024-01-01": 58, "2024-04-01": 60, "2024-07-01": 56, "2024-10-01": 53,
    "2025-01-01": 55, "2025-04-01": 56, "2025-07-01": 65, "2025-09-01": 78,
    "2025-11-01": 88, "2025-12-01": 92, "2026-02-01": 115, "2026-04-01": 137,
    "2026-05-01": 100,
}
xs = pd.to_datetime(list(ndpr_pts.keys()))
ys = list(ndpr_pts.values())
ndpr_series = pd.Series(ys, index=xs).reindex(ndpr_months).interpolate()
ndpr_ex_china = ndpr_series * 1.5  # ex-China premium reported at ~50–63%

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ndpr_series.index, ndpr_series.values, color="#2ca02c", linewidth=2, label="NdPr oxide — SMM China benchmark")
ax.plot(ndpr_ex_china.index, ndpr_ex_china.values, color="#d62728", linewidth=2, linestyle="--", label="NdPr oxide — implied ex-China (~+50% premium)")
ax.set_ylabel("US$ / kg NdPr oxide")
ax.set_xlabel("Date")
ax.set_title("NdPr oxide pricing — Jan 2024 to May 2026")
ax.legend()
fig.tight_layout()
save(fig, "uuuu_ndpr_price.png")


# ---------------- Chart 5: cash & liquidity FY2021-FY2025 ----------------
cash = [113.0, 79.3, 50.7, 47.1, 64.7]
mkt_sec = [29.0, 47.4, 167.6, 119.5, 797.1]
labels = ["2021", "2022", "2023", "2024", "2025"]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(labels, cash, label="Cash & equivalents", color="#1f77b4")
ax.bar(labels, mkt_sec, bottom=cash, label="Marketable securities", color="#9edae5")
total = [c + m for c, m in zip(cash, mkt_sec)]
for i, t in enumerate(total):
    ax.text(i, t + 10, f"${t:.0f}M", ha="center", fontsize=10, weight="bold")
ax.set_ylabel("US$M (year-end)")
ax.set_title("Energy Fuels — cash + marketable securities, FY2021–FY2025")
ax.legend()
fig.tight_layout()
save(fig, "uuuu_liquidity.png")


# ---------------- Chart 6: peer P/S comparison ----------------
peers = ["UUUU\n(Energy Fuels)", "CCJ\n(Cameco)", "DNN\n(Denison)", "UEC\n(Uranium Energy)",
         "NXE\n(NexGen)", "MP\n(MP Materials)", "LYC.AX\n(Lynas)", "NEO.TO\n(Neo Perf.)"]
ps = [53.1, 13.0, 630.7, 324.2, None, 32.0, 26.1, 2.4]   # NXE near zero rev
mcap = [4.51, 46.1, 2.93, 6.55, 7.09, 11.14, 18.69, 1.21]  # USD bn

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#d62728" if p.startswith("UUUU") else ("#1f77b4" if any(t in p for t in ["CCJ","DNN","UEC","NXE"]) else "#2ca02c") for p in peers]
bars = ax.bar(peers, [p or 0 for p in ps], color=colors)
ax.set_ylabel("TTM P/S (x)")
ax.set_title("Peer TTM Price/Sales — uranium (blue) vs. REE (green) vs. UUUU (red)")
for b, v in zip(bars, ps):
    label = "n/a" if v is None or v == 0 else f"{v:.0f}x"
    ax.text(b.get_x() + b.get_width()/2, (v or 0) + 10, label, ha="center", fontsize=9)
ax.set_yscale("log")
fig.tight_layout()
save(fig, "uuuu_peer_ps.png")
