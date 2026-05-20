#!/usr/bin/env python3
"""Generate charts for Oklo (OKLO) research report."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- Chart 1: Cash + securities position over time ($USDm) ----
# Sources: OKLO 10-K FY2024 (filed 2025-03-24), 10-K FY2025 (filed 2026-03-17),
# 10-Q Q1 2026 (filed 2026-05-12)
# Cash & equiv | ST mkt sec | LT mkt sec | Total liquid
periods = ["12/31/2023*", "12/31/2024", "12/31/2025", "3/31/2026"]
cash    = [    None,           97.1,         788.4,       1594.1]
st_sec  = [    None,          130.7,         439.5,        614.5]
lt_sec  = [    None,           47.5,         184.6,        328.3]
# Pre-SPAC: Legacy Oklo cash was ~$15M per S-4; we use FY2024 first.
# Re-anchor: include legacy estimate visually only as label, not bar.

fig, ax = plt.subplots(figsize=(10, 5.6))
x = np.arange(len(periods) - 1)  # skip pre-SPAC
labels = periods[1:]
c1 = [v for v in cash[1:]]
c2 = [v for v in st_sec[1:]]
c3 = [v for v in lt_sec[1:]]

ax.bar(x, c1, color="#1f6dbf", label="Cash & equivalents")
ax.bar(x, c2, bottom=c1, color="#3aa6e0", label="ST marketable securities")
ax.bar(x, c3, bottom=[a+b for a,b in zip(c1,c2)], color="#9ad0ee", label="LT marketable securities")

totals = [a+b+c for a,b,c in zip(c1,c2,c3)]
for i, t in enumerate(totals):
    ax.text(i, t + 35, f"${t:,.0f}M", ha="center", fontsize=10, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("USD millions")
ax.set_title("Oklo — Cash & marketable securities position\nFY2024 close → Q1 2026 close")
ax.legend(loc="upper left")
ax.set_ylim(0, max(totals) * 1.15)
ax.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_cash_position.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 2: Operating expenses + net loss (annual burn) ----
# FY2023, FY2024, FY2025 + Q1 2026 annualized
# FY2023 numbers from 2024 10-K comparison year; we'll cite the FY2024 10-K.
# Source values (10-K FY2025):  R&D 58,852 G&A 80,442 opex 139,294 net loss (105,663) for FY2025;
#                                R&D 26,711 G&A 26,090 opex 52,801 net loss (73,616) for FY2024.
# FY2023 from FY2024 10-K: opex ~ 35,030; R&D 19,348; G&A 15,682; net loss (20,752). Source: 2024 10-K.
years_a   = ["FY2023", "FY2024", "FY2025"]
rd_a      = [    9.8,    26.7,    58.9]   # FY23 from FY24 10-K p.134; FY24-25 from FY25 10-K p.136
ga_a      = [    8.9,    26.1,    80.4]
opex_a    = [r+g for r,g in zip(rd_a, ga_a)]
netloss_a = [  -32.2,   -73.6,  -105.7]

fig, ax = plt.subplots(figsize=(10, 5.6))
x = np.arange(len(years_a))
w = 0.35
b1 = ax.bar(x - w/2, rd_a, w, label="R&D expense", color="#3b6fa6")
b2 = ax.bar(x - w/2, ga_a, w, bottom=rd_a, label="G&A expense", color="#9bc6e0")
b3 = ax.bar(x + w/2, [-v for v in netloss_a], w, label="Net loss (abs.)", color="#b94b4b")

for i, v in enumerate(opex_a):
    ax.text(i - w/2, v + 2, f"${v:.1f}M", ha="center", fontsize=9)
for i, v in enumerate(netloss_a):
    ax.text(i + w/2, -v + 2, f"${-v:.1f}M", ha="center", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(years_a)
ax.set_ylabel("USD millions")
ax.set_title("Oklo — Operating expenses and net loss (FY2022–FY2025)")
ax.legend()
ax.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_burn_trend.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 3: Share count dilution since de-SPAC ----
# Source: 10-K FY2025 stockholders' equity statement, plus Q1 2026 10-Q
# Class A shares outstanding at period end
dates = ["1/1/2024\n(Legacy)", "5/9/2024\n(Recapitalization)", "12/31/2024", "12/31/2025", "3/31/2026"]
# Pre-SPAC = 69.24M Legacy Oklo; post-recap immediate ~135M (incl. 43.1M AltC + 8.4M SAFE + 14.7M earnout)
shares_m = [69.2, 135.5, 137.7, 160.5, 173.9]

fig, ax = plt.subplots(figsize=(10, 5.6))
x = np.arange(len(dates))
bars = ax.bar(x, shares_m, color=["#7f8c8d", "#34495e", "#2980b9", "#27ae60", "#16a085"])
for i, v in enumerate(shares_m):
    ax.text(i, v + 3, f"{v:.1f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=9)
ax.set_ylabel("Class A common shares outstanding (millions)")
ax.set_title("Oklo — Share-count dilution since de-SPAC\nLegacy Oklo → Q1 2026 close")
ax.set_ylim(0, max(shares_m)*1.15)
ax.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_share_dilution.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 4: EV vs peers (advanced/SMR-adjacent stack) ----
# Values per yfinance pull 2026-05-20 (intra-session)
peers = ["Oklo\n(OKLO)", "NuScale\n(SMR)", "Nano Nuclear\n(NNE)", "Centrus\n(LEU)",
         "BWXT", "Cameco\n(CCJ)", "Constellation\n(CEG)"]
ev_bn = [7.52, 2.54, 0.59, 2.64, 19.58, 44.99, 116.09]
ttm_rev_status = ["pre-rev", "pre-rev*", "pre-rev", "rev'g", "rev'g", "rev'g", "rev'g"]
colors = ["#c0392b" if x=="pre-rev" else "#e67e22" if x=="pre-rev*" else "#27ae60"
          for x in ttm_rev_status]

fig, ax = plt.subplots(figsize=(11, 5.6))
x = np.arange(len(peers))
bars = ax.bar(x, ev_bn, color=colors)
for i, v in enumerate(ev_bn):
    ax.text(i, v + 1, f"${v:.1f}B", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(peers, fontsize=9)
ax.set_ylabel("Enterprise value (USD billions)")
ax.set_title("Oklo vs nuclear peers — enterprise value comparison\nSource: Yahoo Finance, 2026-05-20 intraday")
ax.grid(axis="y", linestyle=":", alpha=0.5)

red_p   = mpatches.Patch(color="#c0392b", label="Pre-revenue developer")
orange_p= mpatches.Patch(color="#e67e22", label="Pre-revenue/lic. (NuScale)*")
green_p = mpatches.Patch(color="#27ae60", label="Revenue-generating")
ax.legend(handles=[red_p, orange_p, green_p], loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_peer_ev.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 5: Capital raised since de-SPAC ----
# Capital sources, FY2024 + FY2025 + Q1 2026
events = ["AltC SPAC trust\n(5/2024, net of redemptions)", "Follow-on PO\n(Aug 2024)",
          "Sep-2025 ATM\n(through Sep 2025)", "Dec-2025 ATM\n(Dec 2025)",
          "Dec-2025 ATM\n(Jan 2026, residual)"]
amounts = [259.0, 440.1, 820.4 - 300.0, 300.0, 1199.9]
# 820.4M was sum of all 2025 ATM-program gross; Sep-2025 program closed; Dec ATM separate.
# To simplify, recategorize: 2025 ATM aggregate = 820.4M, then Jan-2026 residual 1199.9M = $1.2B.
events = ["AltC trust\n(May 2024, net)", "Follow-on PO\n(Aug 2024)",
          "2025 ATM program\n(through 12/4/2025)", "Dec-2025 ATM\n(12/4–12/31/2025)",
          "Dec-2025 ATM\n(Jan 2026 final)"]
amounts = [259.0, 440.1, 820.4, 300.0, 1199.9]

fig, ax = plt.subplots(figsize=(11, 5.6))
x = np.arange(len(events))
bars = ax.bar(x, amounts, color="#2c3e50")
for i, v in enumerate(amounts):
    ax.text(i, v + 30, f"${v:,.0f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(events, fontsize=9)
ax.set_ylabel("USD millions — gross proceeds (net for de-SPAC)")
ax.set_title("Oklo — Equity capital raised since de-SPAC (May 2024 → Jan 2026)\n≈ $3.0B raised in ~20 months")
ax.set_ylim(0, max(amounts) * 1.2)
ax.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_capital_raised.png"), dpi=150, bbox_inches="tight")
plt.close()

# ---- Chart 6: Implied runway at current burn ----
# Liquid cash at 3/31/2026 = $2,537M
# FY2026 management opex guide: $80–100M cash opex, plus $350–450M capex (investing)
# So 2026 total cash use = $430–550M midpoint = ~$490M
# Q1 2026 actual cash burn: ops -17.9 + invest -359 = -377M but most of invest was buying mkt securities;
# excluding net change in mkt securities: ops -17.9, capex -32.8, oth -5 ≈ -55.7M Q1 actual operating+capex.
# Annualized = ~$220M; but mgmt explicitly guides $80–100M opex + $350–450M capex = $430–550M total.
fig, ax = plt.subplots(figsize=(10, 5.6))
scenarios = ["Low end of\n2026 guide\n($430M)", "Midpoint\n2026 guide\n($490M)",
             "High end of\n2026 guide\n($550M)", "Aggressive\nbuild-up\n($800M)"]
total_liq = 2537  # cash + ST + LT marketable
runway_yrs = [total_liq / b for b in [430, 490, 550, 800]]
bars = ax.bar(scenarios, runway_yrs,
              color=["#27ae60", "#27ae60", "#e67e22", "#c0392b"])
for i, v in enumerate(runway_yrs):
    ax.text(i, v + 0.15, f"{v:.1f} yrs", ha="center", fontsize=11, fontweight="bold")
ax.set_ylabel("Implied runway (years)")
ax.set_title(f"Oklo — Implied cash runway at $2.54B liquidity (3/31/2026)\nManagement 2026 cash-use guide: $80–100M opex + $350–450M capex")
ax.grid(axis="y", linestyle=":", alpha=0.5)
ax.set_ylim(0, max(runway_yrs)*1.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "oklo_runway.png"), dpi=150, bbox_inches="tight")
plt.close()

print("All charts written to:", OUT)
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print(" ", f)
