"""Generate matplotlib charts for the Talen Energy (TLN) company research report."""

import os
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# 1. Capacity by fuel type (owned MW, summer rating, 2025-12-31 10-K)
# Source: 10-K FY2025 Item 2 Properties
# ---------------------------------------------------------------------------
fuels = [
    ("Nuclear (Susquehanna)", 2245, "#1f77b4"),
    ("Natural-gas baseload\n(Guernsey, Freedom,\nLower Mt. Bethel)", 1771 + 1049 + 607, "#2ca02c"),
    ("Natural-gas / oil peakers &\nintermediate (Martins Crk,\nMontour, Brunner Is.)", 1710 + 1505 + 1419, "#9467bd"),
    ("Coal RMR\n(Brandon Shores, Wagner)", 1273 + 702, "#7f7f7f"),
    ("Coal minority interests\n(Conemaugh, Keystone, Colstrip)", 392 + 213 + 222, "#8c564b"),
]
labels = [f[0] for f in fuels]
values = [f[1] for f in fuels]
colors = [f[2] for f in fuels]

fig, ax = plt.subplots(figsize=(8.5, 5.5))
wedges, texts, autotexts = ax.pie(
    values,
    labels=labels,
    colors=colors,
    autopct=lambda p: f"{p:.1f}%\n({int(round(p/100*sum(values))):,} MW)",
    startangle=90,
    pctdistance=0.72,
    textprops={"fontsize": 9},
)
ax.set_title("Talen Energy — Owned Capacity by Fuel Type (MW, 2025-12-31)\nTotal: 13,108 MW", fontsize=12, fontweight="bold")
save(fig, "tln_capacity_by_fuel.png")


# ---------------------------------------------------------------------------
# 2. Revenue & Adjusted EBITDA trend (combined predecessor + successor for 2023)
# Source: 10-K FY2025
# ---------------------------------------------------------------------------
years = ["2023 (combined)", "2024", "2025"]
# 2023 combined = predecessor Jan1-May17 + successor May18-Dec31
rev = [1210 + 1344, 2115, 2581]
ebitda = [695 + 426, 770, 1035]

x = np.arange(len(years))
w = 0.38

fig, ax1 = plt.subplots(figsize=(9, 5))
b1 = ax1.bar(x - w/2, rev, w, label="Operating revenue", color="#1f77b4")
b2 = ax1.bar(x + w/2, ebitda, w, label="Adjusted EBITDA", color="#ff7f0e")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("USD millions")
ax1.set_title("Talen Energy — Revenue & Adjusted EBITDA Trend", fontsize=12, fontweight="bold")
ax1.legend(loc="upper left")
for bars in (b1, b2):
    for r in bars:
        ax1.text(r.get_x() + r.get_width()/2, r.get_height()+30, f"${int(r.get_height()):,}", ha="center", fontsize=9)
ax1.set_ylim(0, max(rev)*1.18)
ax1.grid(axis="y", alpha=0.3)
save(fig, "tln_revenue_ebitda_trend.png")


# ---------------------------------------------------------------------------
# 3. AWS PPA — annual delivery ramp (illustrative)
# Source: 10-K FY2025: 1,920 MW max by 2032, ramps over time, through 2042
# ---------------------------------------------------------------------------
# Public disclosure: delivery ramp by 2032 to 1,920 MW; we draw an illustrative
# stepped ramp consistent with disclosed milestones (840–1,200 MW by 2029, 1,680–
# 1,920 MW by 2032). Show range as a band.
yrs = list(range(2026, 2043))
low = []
high = []
for y in yrs:
    if y <= 2026:
        low.append(300); high.append(400)
    elif y <= 2028:
        low.append(450); high.append(650)
    elif y == 2029:
        low.append(840); high.append(1200)
    elif y == 2030:
        low.append(1100); high.append(1500)
    elif y == 2031:
        low.append(1400); high.append(1750)
    elif y == 2032:
        low.append(1680); high.append(1920)
    else:
        low.append(1920); high.append(1920)

fig, ax = plt.subplots(figsize=(9, 5))
ax.fill_between(yrs, low, high, color="#1f77b4", alpha=0.25, label="Delivery range (illustrative band)")
ax.plot(yrs, high, color="#1f77b4", linewidth=2, label="Upper bound (1,920 MW by 2032)")
ax.plot(yrs, low, color="#1f77b4", linewidth=2, linestyle="--", label="Lower bound")
ax.axhline(1920, color="grey", linestyle=":", linewidth=1)
ax.text(2040, 1940, "Contract cap: 1,920 MW", color="grey", fontsize=9)
ax.set_xlabel("Year")
ax.set_ylabel("Annual nuclear delivery (MW)")
ax.set_title("Talen AWS PPA — Front-of-Meter Delivery Ramp (Susquehanna → AWS, through 2042)", fontsize=11, fontweight="bold")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
ax.set_ylim(0, 2200)
save(fig, "tln_aws_ppa_ramp.png")


# ---------------------------------------------------------------------------
# 4. Peer comparison — IPP valuations (TLN vs CEG, VST, NRG)
# Sources: market data as of mid-May 2026; forward EV/EBITDA and Forward P/E.
# ---------------------------------------------------------------------------
peers = ["TLN", "VST", "CEG", "NRG"]
mcap = [15.6, 50.1, 103.3, 35.6]   # $B
fwd_pe = [15.49, 15.53, 26.0, 18.2]  # forward P/E
fwd_ev_ebitda = [13.5, 10.56, 13.0, 9.5]  # forward EV/EBITDA

x = np.arange(len(peers))
w = 0.38
fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - w/2, fwd_pe, w, label="Forward P/E", color="#1f77b4")
b2 = ax.bar(x + w/2, fwd_ev_ebitda, w, label="Forward EV/EBITDA", color="#ff7f0e")
ax.set_xticks(x)
ax.set_xticklabels([f"{p}\n${m:.1f}B mkt cap" for p, m in zip(peers, mcap)])
ax.set_ylabel("Multiple (x)")
ax.set_title("IPP Peer Valuation — Forward Multiples (May 2026)", fontsize=12, fontweight="bold")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2, r.get_height()+0.3, f"{r.get_height():.1f}x", ha="center", fontsize=9)
ax.set_ylim(0, max(fwd_pe)*1.18)
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "tln_peer_valuation.png")
