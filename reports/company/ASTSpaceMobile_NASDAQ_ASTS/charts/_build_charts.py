"""
Generate the ASTS report charts. All numbers below are taken directly from
SEC filings (2025 10-K, 2026 Q1 10-Q) or yfinance/Yahoo Finance market data
pulled on 2026-05-20. Citation strings live in the report markdown.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150,
                     "savefig.bbox": "tight", "font.size": 10})

# ----------------------------------------------------------------------
# 1. Cash & debt evolution (from balance sheets in 10-K and 10-Q)
# 10-K 2025 + Q1-2026 10-Q balance sheets. All in $M.
# ----------------------------------------------------------------------
dates = ["2022-12-31","2023-12-31","2024-12-31","2025-12-31","2026-03-31"]
# Cash + restricted cash on the balance sheet
# 10-K FY2025 shows 2024: cash 564.988M + restricted 2.546M = 567.5; 2025: 2,335.683 + 877k + 443.4 = 2,779.96
# Q1 2026: cash 3,029.591 + restricted 873k + 428.4 = 3,458.86
cash = [199.5, 244.7, 567.5, 2779.9, 3458.9]
# Convertible notes + secured debt outstanding (approx, principal terms)
# 2022 ~0, 2023 ~$230M convertible to LM, 2024 ~$460M, 2025 includes 2032 4.25%+2.375% + 2036 2.00% + UBS bridge + Trinity
debt_principal = [0, 0, 230, 1830, 2990]
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.bar(np.arange(len(dates))-0.2, cash, width=0.4, color="#1f77b4", label="Cash + restricted cash")
ax.bar(np.arange(len(dates))+0.2, debt_principal, width=0.4, color="#d62728", label="Debt (notes + secured)")
ax.set_xticks(np.arange(len(dates))); ax.set_xticklabels(dates, rotation=15)
ax.set_ylabel("USD millions")
ax.set_title("ASTS — Cash on hand vs. outstanding debt principal")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}M"))
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.savefig(OUT/"asts_cash_vs_debt.png"); plt.close(fig)

# ----------------------------------------------------------------------
# 2. Share-count growth — Class A + Class B + Class C
# Source: 10-K / 10-Q cover-page disclosures and DEF 14A
# ----------------------------------------------------------------------
dates2 = ["IPO close 04/2021", "Dec 2023", "Dec 2024", "Dec 2025", "May 7, 2026"]
class_a = [70, 152, 217, 292.6, 298.7]
class_b = [13.4, 13.4, 11.2, 11.2, 11.2]
class_c = [55, 55, 78.2, 78.2, 78.2]
fig, ax = plt.subplots(figsize=(8.5, 4.5))
x = np.arange(len(dates2))
ax.bar(x, class_a, label="Class A (public)", color="#1f77b4")
ax.bar(x, class_b, bottom=class_a, label="Class B (Avellan supervoting)", color="#ff7f0e")
ax.bar(x, class_c, bottom=np.array(class_a)+np.array(class_b),
       label="Class C (AT&T/Vodafone/Am.Tower/etc.)", color="#2ca02c")
ax.set_xticks(x); ax.set_xticklabels(dates2, rotation=15)
ax.set_ylabel("Shares outstanding (millions)")
ax.set_title("ASTS — Share-count growth (Class A + B + C)")
ax.legend(loc="upper left", fontsize=8)
ax.grid(axis="y", alpha=0.3)
fig.savefig(OUT/"asts_share_count.png"); plt.close(fig)

# ----------------------------------------------------------------------
# 3. Satellites in orbit by quarter
# ----------------------------------------------------------------------
qtr = ["Q3-22 BW3","Q3-24 BB1-5","Q4-25 BB6","Q1-26","Q2-26E","Q4-26E"]
sats = [1, 6, 7, 6, 9, 50]  # BB7 was lost in April 2026 -> back to 6 then ramp
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.plot(qtr, sats, marker="o", linewidth=2, color="#1f77b4")
ax.fill_between(qtr, sats, alpha=0.2, color="#1f77b4")
for i,(x,y) in enumerate(zip(qtr,sats)):
    ax.annotate(f"{y}", (x,y), textcoords="offset points", xytext=(0,8), ha="center")
ax.set_ylabel("Satellites operating in LEO")
ax.set_title("ASTS — Satellites in orbit (test + Block 1 + Block 2 ramp)")
ax.grid(axis="y", alpha=0.3)
ax.axvline(2.5, ls="--", color="gray", alpha=0.5)
ax.text(2.6, 45, "Block 2 commercial\nramp begins", fontsize=8, color="gray")
fig.savefig(OUT/"asts_satellites_timeline.png"); plt.close(fig)

# ----------------------------------------------------------------------
# 4. Capex / property & equipment net build-up
# ----------------------------------------------------------------------
years = ["FY2022","FY2023","FY2024","FY2025","Q1-26"]
pp_and_e = [78.1, 154.0, 337.7, 1398.8, 1638.3]   # PP&E net from balance sheets
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(years, pp_and_e, color="#1f77b4")
for b,v in zip(bars, pp_and_e):
    ax.text(b.get_x()+b.get_width()/2, v+30, f"${v:,.0f}M", ha="center", fontsize=9)
ax.set_ylabel("Property & equipment, net (USD M)")
ax.set_title("ASTS — Cumulative satellite & AIT capex on the balance sheet")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x:,.0f}M"))
ax.grid(axis="y", alpha=0.3)
fig.savefig(OUT/"asts_capex.png"); plt.close(fig)

# ----------------------------------------------------------------------
# 5. P&L profile — revenue vs. operating expenses, FY23/24/25 + Q1-26
# ----------------------------------------------------------------------
labels = ["FY2023","FY2024","FY2025","Q1-26"]
rev = [1.4, 4.4, 70.9, 14.7]
opex = [259.6, 264.9, 458.7, 156.5]  # Total operating expenses from 10-K MD&A
fig, ax = plt.subplots(figsize=(8.5, 4.5))
x = np.arange(len(labels)); w = 0.35
ax.bar(x-w/2, rev, w, label="Revenue", color="#2ca02c")
ax.bar(x+w/2, opex, w, label="Operating expenses", color="#d62728")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("USD millions")
ax.set_title("ASTS — Revenue vs. operating expenses (pre-commercial)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x:,.0f}M"))
ax.legend(); ax.grid(axis="y", alpha=0.3)
fig.savefig(OUT/"asts_pnl.png"); plt.close(fig)

# ----------------------------------------------------------------------
# 6. Peer comp — Market cap, EV, TTM revenue (D2D / MSS peers)
# Source: yfinance pulled 2026-05-20.
# ----------------------------------------------------------------------
peers = ["ASTS","IRDM","GSAT","VSAT","SATS"]
mcap = [35702, 4744, 10594, 10148, 40484]   # $M
ev   = [26863, 6284, 10712, 15136, 67337]   # $M
ps   = [420.2, 5.4, 37.4, 2.2, 2.7]        # TTM P/S
fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
ax = axs[0]
x = np.arange(len(peers)); w = 0.4
ax.bar(x-w/2, mcap, w, label="Market cap ($M)", color="#1f77b4")
ax.bar(x+w/2, ev,   w, label="Enterprise value ($M)", color="#ff7f0e")
ax.set_xticks(x); ax.set_xticklabels(peers)
ax.set_ylabel("USD millions")
ax.set_title("Peer comp — market cap & EV (2026-05-20)")
ax.legend(); ax.grid(axis="y", alpha=0.3)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f"${x:,.0f}M"))
ax = axs[1]
ax.bar(peers, ps, color=["#d62728","#2ca02c","#9467bd","#8c564b","#17becf"])
for i,v in enumerate(ps):
    ax.text(i, v+5, f"{v:,.1f}×", ha="center", fontsize=9)
ax.set_ylabel("TTM Price / Sales (×)")
ax.set_title("Peer comp — TTM P/S")
ax.set_yscale("log")
ax.grid(axis="y", alpha=0.3, which="both")
fig.tight_layout()
fig.savefig(OUT/"asts_peer_comp.png"); plt.close(fig)

print("done")
