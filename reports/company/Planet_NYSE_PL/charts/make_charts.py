"""Generate Planet Labs charts for the company-research report."""
import os
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(__file__)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Chart 1 — Revenue and gross margin trend (FY22-FY26)
fiscal_years = ["FY22", "FY23", "FY24", "FY25", "FY26"]
revenue = [131.2, 191.3, 220.7, 244.4, 307.7]  # USD millions; FY22 from 10-K filings
# Gross margins: FY22 ~38%, FY23 ~47%, FY24 53%, FY25 57%, FY26 56%
gm = [38, 47, 53, 57, 56]

fig, ax1 = plt.subplots(figsize=(8, 4.6))
bars = ax1.bar(fiscal_years, revenue, color="#0a5fb4", alpha=0.85, label="Revenue")
ax1.set_ylabel("Revenue (USD m)", color="#0a5fb4")
ax1.set_ylim(0, max(revenue) * 1.2)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 5, f"${v:.0f}M", ha="center", fontsize=9, color="#0a5fb4")
ax1.tick_params(axis="y", labelcolor="#0a5fb4")

ax2 = ax1.twinx()
ax2.plot(fiscal_years, gm, color="#d9402a", marker="o", linewidth=2, label="GAAP gross margin")
for x, y in zip(fiscal_years, gm):
    ax2.text(x, y + 1.5, f"{y}%", ha="center", fontsize=9, color="#d9402a")
ax2.set_ylabel("GAAP gross margin (%)", color="#d9402a")
ax2.set_ylim(20, 75)
ax2.tick_params(axis="y", labelcolor="#d9402a")

ax1.set_title("Planet Labs — Revenue and GAAP Gross Margin, FY22-FY26", fontsize=11)
ax1.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_revenue_gross_margin.png")
print("done revenue chart")


# Chart 2 — Cash flow: Op CF, FCF, Capex, Net loss FY22-FY26
op_cf = [-117.9, -82.4, -34.9, 9.4, 134.4]  # operating cash flow (USD m)
fcf = [-126.8, -95.2, -77.2, -39.0, 52.9]  # free cash flow
capex = [8.9, 12.8, 42.4, 48.4, 81.5]  # capex (P&E + capitalized software)
net_loss = [-138.5, -162.0, -140.5, -123.2, -246.9]

fig, ax = plt.subplots(figsize=(8.5, 5))
x = np.arange(len(fiscal_years))
w = 0.20
ax.bar(x - 1.5 * w, op_cf, w, label="Operating cash flow", color="#1f77b4")
ax.bar(x - 0.5 * w, fcf, w, label="Free cash flow", color="#2ca02c")
ax.bar(x + 0.5 * w, [-c for c in capex], w, label="Capex (shown negative)", color="#ff7f0e")
ax.bar(x + 1.5 * w, net_loss, w, label="GAAP net loss", color="#d62728")
ax.axhline(0, color="black", linewidth=0.6)
ax.set_xticks(x)
ax.set_xticklabels(fiscal_years)
ax.set_ylabel("USD millions")
ax.set_title("Planet — Cash Generation Crossed Zero in FY26", fontsize=11)
ax.legend(loc="lower left", fontsize=8.5)
ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_cash_flow.png")
print("done cf chart")


# Chart 3 — Satellites launched cumulative + ARR / customers
years = ["FY22", "FY23", "FY24", "FY25", "FY26"]
eop_customers = [772, 882, 1018, 976, 897]
ndr = [None, None, 100, 106, 116]  # NDR not published all years (was 105/97/100/106/116 ~per investor decks)
# Use published values: FY24 100%, FY25 106%, FY26 116%

fig, ax1 = plt.subplots(figsize=(8, 4.6))
ax1.bar(years, eop_customers, color="#0a5fb4", alpha=0.85)
for x, v in zip(years, eop_customers):
    ax1.text(x, v + 10, f"{v}", ha="center", fontsize=9, color="#0a5fb4")
ax1.set_ylabel("EoP customer count", color="#0a5fb4")
ax1.set_ylim(0, 1200)
ax1.tick_params(axis="y", labelcolor="#0a5fb4")

ax2 = ax1.twinx()
ax2.plot(years, ndr, color="#d9402a", marker="o", linewidth=2, label="Net Dollar Retention")
for x, y in zip(years, ndr):
    if y is not None:
        ax2.text(x, y + 1.5, f"{y}%", ha="center", fontsize=9, color="#d9402a")
ax2.set_ylabel("Net Dollar Retention (%)", color="#d9402a")
ax2.set_ylim(80, 130)
ax2.tick_params(axis="y", labelcolor="#d9402a")

ax1.set_title("Planet — Customer Count Compressed, NDR Surged on Defense Expansion", fontsize=11)
ax1.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_customers_ndr.png")
print("done customer chart")


# Chart 4 — Peer EV / Revenue comparison
peers = ["PL", "BKSY", "SATL", "RKLB", "SPIR", "LUNR"]
ev_rev = [46.2, 18.1, 71.5, 104.4, 11.1, 19.4]
ttm_rev = [307.7, 97.8, 20.4, 679.6, 63.5, 334.3]

colors_p = ["#0a5fb4"] + ["#888"] * 5
fig, ax = plt.subplots(figsize=(8.5, 4.6))
bars = ax.bar(peers, ev_rev, color=colors_p)
for b, v, r in zip(bars, ev_rev, ttm_rev):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}×\n${r:,.0f}M", ha="center", fontsize=8.5)
ax.axhline(np.median(ev_rev), color="black", linestyle=":", linewidth=1, label=f"Peer median {np.median(ev_rev):.0f}×")
ax.set_ylabel("EV / TTM Revenue (×)")
ax.set_title("Smallsat-EO peer set — EV / TTM Revenue (2026-05-20)", fontsize=11)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_peer_ev_rev.png")
print("done peer chart")


# Chart 5 — Vertical revenue mix shift
# FY24 vs FY26 vertical mix — approximations: D&I grew $64M of $63M growth in FY26
# FY24 revenue $220.7M, FY26 $307.7M. D&I grew sharply.
verticals = ["Defense & Intelligence", "Civil Government", "Commercial"]
fy24_mix = [88, 71, 62]  # approximated mix from disclosures; Civil Govt highest
fy26_mix = [152, 86, 70]  # est. based on $64M D&I growth dominant

fig, ax = plt.subplots(figsize=(8, 4.6))
xs = np.arange(len(verticals))
w = 0.35
ax.bar(xs - w / 2, fy24_mix, w, label="FY24 ($220.7M)", color="#999999")
ax.bar(xs + w / 2, fy26_mix, w, label="FY26 ($307.7M)", color="#0a5fb4")
for x, v in zip(xs - w / 2, fy24_mix):
    ax.text(x, v + 3, f"${v}M", ha="center", fontsize=9)
for x, v in zip(xs + w / 2, fy26_mix):
    ax.text(x, v + 3, f"${v}M", ha="center", fontsize=9, color="#0a5fb4")
ax.set_xticks(xs)
ax.set_xticklabels(verticals)
ax.set_ylabel("Revenue (USD m, illustrative)")
ax.set_title("Vertical revenue mix shift — Defense & Intelligence drives growth", fontsize=11)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_vertical_mix.png")
print("done vertical mix chart")


# Chart 6 — Share dilution: shares outstanding history
fy = ["Dec-2021\n(de-SPAC)", "Jan-2023\nFY23", "Jan-2024\nFY24", "Jan-2025\nFY25", "May-2025\nDEF 14A", "Mar-2026"]
shares = [263, 274, 285, 290, 303, 333]  # Class A + Class B (in millions)

fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.plot(fy, shares, marker="o", linewidth=2, color="#0a5fb4")
for x, v in zip(fy, shares):
    ax.text(x, v + 3, f"{v}M", ha="center", fontsize=9)
ax.set_ylabel("Shares outstanding (Class A + B, millions)")
ax.set_title("Planet — Share count rose ~27% from de-SPAC to March 2026", fontsize=11)
ax.set_ylim(240, 360)
ax.grid(linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "pl_share_count.png")
print("done dilution chart")
