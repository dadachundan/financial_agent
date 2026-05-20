"""Generate charts for the Texas Instruments (TXN) initiation report.

All data is sourced from TXN 10-K filings (2021, 2023, 2024, 2025), Q4 2025 / Q1 2026
press releases, and Yahoo Finance for peer valuation multiples. See the report
for inline citations to each data point.
"""

import matplotlib.pyplot as plt
import numpy as np

OUT = "/Users/x/projects/financial_agent/reports/charts"
plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10})


# ---------------------------------------------------------------------------
# Chart 1: Revenue + Gross Margin trend, FY2019–FY2025 (dual axis)
# ---------------------------------------------------------------------------
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
revenue = [14.383, 14.461, 18.344, 20.028, 17.519, 15.641, 17.682]  # $B
# Gross margin from each 10-K: 2019 ~62.8, 2020 ~64.1, 2021 67.5, 2022 68.8, 2023 62.9, 2024 58.1, 2025 57.0
gm = [62.8, 64.1, 67.5, 68.8, 62.9, 58.1, 57.0]

fig, ax1 = plt.subplots(figsize=(8, 4.5))
bars = ax1.bar(years, revenue, color="#1f4e79", alpha=0.85, label="Revenue ($B)")
ax1.set_ylabel("Revenue ($B)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 24)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#c0392b", marker="o", linewidth=2, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color="#c0392b")
ax2.tick_params(axis="y", labelcolor="#c0392b")
ax2.set_ylim(50, 75)
for x, y in zip(years, gm):
    ax2.text(x, y + 0.6, f"{y:.1f}%", ha="center", color="#c0392b", fontsize=9)

ax1.set_title("Texas Instruments — Revenue and Gross Margin, FY2019–FY2025")
ax1.set_xticks(years)
fig.tight_layout()
fig.savefig(f"{OUT}/txn_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 2: Free cash flow per share, FY2019–FY2025
# ---------------------------------------------------------------------------
# FCF in $B from 10-K disclosures: 2019 5.50, 2020 5.59, 2021 6.29, 2022 5.91 (per TI 2022 10-K), 2023 1.35, 2024 1.498, 2025 2.938
fcf_b = [5.50, 5.58, 6.29, 5.91, 1.35, 1.498, 2.938]
# Diluted share counts (avg, in millions) from 10-Ks
diluted_shares = [931, 925, 935, 921, 916, 919, 913]
fcf_per_share = [round(1000 * fcf / s, 2) for fcf, s in zip(fcf_b, diluted_shares)]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(years, fcf_per_share, color="#16a085")
ax.set_ylabel("FCF per share ($)")
ax.set_title("Texas Instruments — Free Cash Flow per Share (signature long-term metric)")
ax.set_xticks(years)
for b, v in zip(bars, fcf_per_share):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f"${v:.2f}", ha="center", fontsize=9)
ax.set_ylim(0, max(fcf_per_share) * 1.2)
fig.tight_layout()
fig.savefig(f"{OUT}/txn_fcf_per_share.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 3: Capex cycle vs. FCF, FY2019–FY2025
# ---------------------------------------------------------------------------
# Capex from 10-K cash-flow statements ($B)
capex = [0.847, 0.649, 2.461, 4.083, 5.071, 4.820, 4.550]
cfo = [6.65, 6.45, 8.76, 8.72, 6.42, 6.32, 7.15]

x = np.arange(len(years))
width = 0.35
fig, ax = plt.subplots(figsize=(8.5, 4.7))
ax.bar(x - width / 2, cfo, width, color="#2c3e50", label="Cash flow from ops")
ax.bar(x + width / 2, capex, width, color="#e67e22", label="Capital expenditures")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("$ Billions")
ax.set_title("Texas Instruments — Operating Cash Flow vs. Capex (six-year elevated-capex cycle, 2021–2026E)")
for i, (c, k) in enumerate(zip(cfo, capex)):
    ax.text(i - width / 2, c + 0.1, f"{c:.1f}", ha="center", fontsize=8)
    ax.text(i + width / 2, k + 0.1, f"{k:.1f}", ha="center", fontsize=8)
ax.axhspan(0, 0, color="white")
ax.legend()
fig.tight_layout()
fig.savefig(f"{OUT}/txn_capex_cycle.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 4: Segment revenue mix (stacked bar), FY2021–FY2025
# ---------------------------------------------------------------------------
sm_years = [2021, 2022, 2023, 2024, 2025]
analog = [14.050, 15.359, 13.040, 12.161, 14.006]
embedded = [3.049, 3.261, 3.368, 2.533, 2.697]
other = [1.245, 1.408, 1.111, 0.947, 0.979]

fig, ax = plt.subplots(figsize=(8.5, 4.7))
b1 = ax.bar(sm_years, analog, color="#1f4e79", label="Analog")
b2 = ax.bar(sm_years, embedded, bottom=analog, color="#5d8aa8", label="Embedded Processing")
b3 = ax.bar(
    sm_years,
    other,
    bottom=[a + e for a, e in zip(analog, embedded)],
    color="#aab7b8",
    label="Other",
)
ax.set_ylabel("Revenue ($B)")
ax.set_xticks(sm_years)
ax.set_title("Texas Instruments — Revenue by Segment, FY2021–FY2025")
ax.legend(loc="upper right")
for i, y in enumerate(sm_years):
    tot = analog[i] + embedded[i] + other[i]
    ax.text(y, tot + 0.2, f"${tot:.2f}B", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(f"{OUT}/txn_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 5: 2025 end-market revenue mix
# ---------------------------------------------------------------------------
markets = ["Industrial", "Automotive", "Personal Electronics", "Data Center", "Communications", "Other (calculators, etc.)"]
shares = [33, 33, 21, 9, 3, 1]
colors = ["#1f4e79", "#c0392b", "#16a085", "#f39c12", "#8e44ad", "#7f8c8d"]
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.pie(shares, labels=[f"{m}\n{s}%" for m, s in zip(markets, shares)], colors=colors, startangle=90, wedgeprops={"edgecolor": "white"})
ax.set_title("Texas Instruments — FY2025 Revenue by End Market\n(realigned market taxonomy disclosed in 2025 10-K)")
fig.tight_layout()
fig.savefig(f"{OUT}/txn_end_markets.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 6: Capital return — dividends + buybacks, FY2019–FY2025
# ---------------------------------------------------------------------------
# Dividends paid ($B) from cash flow statements
divs = [2.63, 3.39, 3.86, 4.39, 4.557, 4.795, 4.999]
# Buybacks (gross repurchases) from cash flow statements: 2019 2.55, 2020 2.55, 2021 0.527, 2022 3.346, 2023 0.293, 2024 0.929, 2025 1.477
buybacks = [2.55, 2.55, 0.527, 3.346, 0.293, 0.929, 1.477]
total = [d + b for d, b in zip(divs, buybacks)]

x = np.arange(len(years))
width = 0.55
fig, ax = plt.subplots(figsize=(8.5, 4.7))
b1 = ax.bar(x, divs, width, color="#1f4e79", label="Dividends paid")
b2 = ax.bar(x, buybacks, width, bottom=divs, color="#c0392b", label="Share repurchases")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("$ Billions")
ax.set_title("Texas Instruments — Cash Returned to Shareholders, FY2019–FY2025")
for i, (d, bb, t) in enumerate(zip(divs, buybacks, total)):
    ax.text(i, t + 0.1, f"${t:.2f}B", ha="center", fontsize=9)
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(f"{OUT}/txn_capital_return.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 7: Peer valuation comparison (TTM P/E and P/S)
# ---------------------------------------------------------------------------
# Yahoo Finance snapshot, May 2026 (see report for source links).
peers = ["TXN", "ADI", "MCHP", "STM", "NXPI", "IFNNY\n(Infineon)"]
pe = [51.5, 71.8, 425.8, 405.4, 29.5, 83.7]
ps = [14.9, 16.3, 10.8, 4.7, 6.2, 6.8]

x = np.arange(len(peers))
width = 0.4
fig, ax1 = plt.subplots(figsize=(9, 5))
b1 = ax1.bar(x - width / 2, pe, width, color="#1f4e79", label="TTM P/E")
ax1.set_ylabel("TTM P/E (×)", color="#1f4e79")
ax1.set_yscale("log")
ax1.set_ylim(10, 600)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
for i, v in enumerate(pe):
    ax1.text(i - width / 2, v * 1.05, f"{v:.0f}×", ha="center", fontsize=8, color="#1f4e79")

ax2 = ax1.twinx()
b2 = ax2.bar(x + width / 2, ps, width, color="#c0392b", label="TTM P/S")
ax2.set_ylabel("TTM P/S (×)", color="#c0392b")
ax2.set_ylim(0, 20)
ax2.tick_params(axis="y", labelcolor="#c0392b")
for i, v in enumerate(ps):
    ax2.text(i + width / 2, v + 0.3, f"{v:.1f}×", ha="center", fontsize=8, color="#c0392b")

ax1.set_title("Analog & Embedded Peer Valuation — TTM P/E (log) and TTM P/S, May 2026")
fig.tight_layout()
fig.savefig(f"{OUT}/txn_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 8: Geographic revenue mix (end-customer headquarters basis)
# ---------------------------------------------------------------------------
geo_years = [2023, 2024, 2025]
us = [33, 38, 38]
china = [19, 19, 21]
rest_asia = [10, 11, 11]
emea = [26, 25, 22]
japan = [10, 10, 7]
row = [2, 1, 1]

x = np.arange(len(geo_years))
fig, ax = plt.subplots(figsize=(8.5, 4.7))
labels = ["United States", "China", "Rest of Asia", "EMEA", "Japan", "Rest of world"]
data = [us, china, rest_asia, emea, japan, row]
colors_geo = ["#1f4e79", "#c0392b", "#16a085", "#f39c12", "#8e44ad", "#7f8c8d"]
bottom = np.zeros(len(geo_years))
for d, lab, c in zip(data, labels, colors_geo):
    ax.bar(x, d, bottom=bottom, label=lab, color=c)
    for i, v in enumerate(d):
        if v >= 5:
            ax.text(i, bottom[i] + v / 2, f"{v}%", ha="center", va="center", fontsize=8, color="white")
    bottom += np.array(d)
ax.set_xticks(x)
ax.set_xticklabels(geo_years)
ax.set_ylabel("Share of revenue (%)")
ax.set_title("Texas Instruments — Revenue by End-Customer HQ Location, FY2023–FY2025")
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=9)
ax.set_ylim(0, 100)
fig.tight_layout()
fig.savefig(f"{OUT}/txn_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close(fig)


print("Saved charts to", OUT)
