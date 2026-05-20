"""Credo Technology (CRDO) report charts.

Sources for the underlying numbers:
- FY2023, FY2024, FY2025 from CRDO 10-K (fiscal year ended May 3, 2025).
  https://www.sec.gov/Archives/edgar/data/1807794/000162828025033813/0001628280-25-033813-index.htm
- Q1 FY26 (Aug 2, 2025) — 8-K press release 2025-09-03.
- Q2 FY26 (Nov 1, 2025) — 8-K press release 2025-12-01.
- Q3 FY26 (Jan 31, 2026) — 8-K press release 2026-03-02 and Q3 10-Q.
- Peer multiples (CRDO / MRVL / ALAB / AVGO) via Yahoo Finance, 2026-05-20.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path("/Users/x/projects/financial_agent/reports/charts")

# 1. Revenue and gross margin trajectory
years = ["FY2023", "FY2024", "FY2025", "FY2026E"]
# FY26E = sum of Q1-Q3 actuals + Q4 guide midpoint (430)
fy26e = 223.1 + 268.0 + 407.0 + 430.0
revenue_m = [184.19, 192.97, 436.78, fy26e]  # FY23/24/25 from FY25 10-K p.78 income statement
gm_pct = [57.7, 61.9, 64.8, 67.4]            # FY23 = 106.194/184.194; FY24/25 per 10-K; FY26E blends 9M 68.0% with Q4 guide ~64-66

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(years, revenue_m, color="#1f77b4", alpha=0.85, label="Revenue (USD M)")
ax1.set_ylabel("Revenue (USD millions)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, max(revenue_m) * 1.15)
for i, v in enumerate(revenue_m):
    ax1.text(i, v + 25, f"${v:,.0f}M", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm_pct, color="#d62728", marker="o", linewidth=2.5, label="GAAP Gross margin")
ax2.set_ylabel("GAAP Gross margin (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(50, 75)
for i, v in enumerate(gm_pct):
    ax2.text(i, v + 0.8, f"{v:.1f}%", ha="center", fontsize=9, color="#d62728")

plt.title("Credo Technology — Revenue and Gross Margin (FY23–FY26E)")
fig.tight_layout()
plt.savefig(OUT / "crdo_revenue_gm.png", dpi=150, bbox_inches="tight")
plt.close()

# 2. Quarterly revenue ramp
qtrs = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26G"]
qrev = [59.7, 72.0, 135.0, 170.0, 223.1, 268.0, 407.0, 430.0]
fig, ax = plt.subplots(figsize=(9, 4.5))
colors = ["#7f8aaf"] * 4 + ["#1f77b4"] * 3 + ["#a8c4e8"]
ax.bar(qtrs, qrev, color=colors)
for i, v in enumerate(qrev):
    label = f"${v:.0f}M" + ("\n(guide mid)" if i == 7 else "")
    ax.text(i, v + 10, label, ha="center", fontsize=9)
ax.set_ylabel("Revenue (USD millions)")
ax.set_title("Credo Technology — Quarterly Revenue Ramp")
ax.set_ylim(0, 500)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(OUT / "crdo_quarterly_rev.png", dpi=150, bbox_inches="tight")
plt.close()

# 3. Customer concentration — Q3 FY26 (Three Months ended Jan 31, 2026), end-customer view (10-Q Note 3 and §revenue by end customer)
labels = ["Customer B (39%)", "Customer D (32%)", "Customer E (17%)", "All other (12%)"]
sizes = [39, 32, 17, 12]
colors_pie = ["#1f77b4", "#ff7f0e", "#2ca02c", "#cccccc"]
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(sizes, labels=labels, colors=colors_pie, autopct="%1.0f%%", startangle=90, wedgeprops={"edgecolor": "white"})
ax.set_title("Credo Technology — End-Customer Revenue Mix\nQ3 FY26 (Three Months ended Jan 31, 2026)")
plt.tight_layout()
plt.savefig(OUT / "crdo_customer_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# 4. R&D as % of revenue (operating leverage)
years_op = ["FY2023", "FY2024", "FY2025", "9M FY26"]
rnd_pct = [41.7, 49.5, 33.4, 21.0]   # FY23 = 76.774/184.194; FY24/25 per 10-K MD&A; 9M FY26 per 10-Q
sga_pct = [26.2, 31.2, 22.6, 14.7]   # FY23 = 48.248/184.194
op_margin = [-11.5, -19.2, 8.5, 32.2] # FY23 op loss 21.235/184.194; 9M FY26 = (610.282-188.847-132.275)/898.113

x = np.arange(len(years_op))
w = 0.35
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(x - w/2, rnd_pct, w, label="R&D % of revenue", color="#1f77b4")
ax.bar(x + w/2, sga_pct, w, label="SG&A % of revenue", color="#ff7f0e")
ax.plot(x, op_margin, color="#2ca02c", marker="o", linewidth=2.5, label="GAAP Operating margin")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels(years_op)
ax.set_ylabel("% of revenue")
ax.set_title("Credo — Operating Leverage: Opex ratio decline driving margin expansion")
ax.legend(loc="upper right")
for i, v in enumerate(op_margin):
    ax.text(i, v + (2 if v >= 0 else -4), f"{v:+.1f}%", ha="center", fontsize=9, color="#2ca02c")
plt.tight_layout()
plt.savefig(OUT / "crdo_opex_leverage.png", dpi=150, bbox_inches="tight")
plt.close()

# 5. Peer comparison — P/S TTM
peers = ["CRDO", "ALAB", "AVGO", "MRVL"]
ps_ttm = [31.3, 48.8, 29.0, 19.9]
pe_ttm = [99.1, 191.3, 81.4, 60.6]
fwd_pe = [32.9, 67.8, 22.9, 34.3]

x = np.arange(len(peers))
w = 0.25
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(x - w, ps_ttm, w, label="P/S (TTM)", color="#1f77b4")
ax.bar(x,       pe_ttm, w, label="P/E (TTM)", color="#d62728")
ax.bar(x + w,   fwd_pe, w, label="Forward P/E", color="#ff7f0e")
ax.set_xticks(x); ax.set_xticklabels(peers)
ax.set_ylabel("Multiple (x)")
ax.set_title("Credo vs. AI-Interconnect Peers — Valuation Multiples (2026-05-20)")
ax.legend()
for i in range(len(peers)):
    ax.text(i - w, ps_ttm[i] + 3, f"{ps_ttm[i]:.0f}", ha="center", fontsize=8)
    ax.text(i,     pe_ttm[i] + 3, f"{pe_ttm[i]:.0f}", ha="center", fontsize=8)
    ax.text(i + w, fwd_pe[i] + 3, f"{fwd_pe[i]:.0f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "crdo_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# 6. AEC mix and product-line evolution (illustrative attribution from filings text)
# FY25 disclosure: "AEC products contributed over 95% of the increase in product sales revenue"
# Product sales FY25 = $412.2M, FY24 = $145.0M. Implied AEC product-sales growth ~ $267M*95% = $254M.
# Product sales = 97% of total FY25 revenue. AEC is described as the dominant single product line.
# We mark this chart "Illustrative" because Credo does not break out AEC vs IC vs other in the 10-K.
years_mix = ["FY2023", "FY2024", "FY2025", "9M FY26"]
prod_sales = [141.5, 145.0, 412.2, 871.0]   # FY23/24/25 per 10-K; 9M FY26 = total - IP - services (illustrative)
ip_lic     = [31.9, 28.0, 12.5, 12.0]       # FY23/24/25 per 10-K; 9M FY26 illustrative
serv       = [10.8, 19.9, 12.1, 15.1]       # FY23/24/25 per 10-K; 9M FY26 illustrative
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(years_mix, prod_sales, label="Product sales (AEC + IC)", color="#1f77b4")
ax.bar(years_mix, ip_lic, bottom=prod_sales, label="IP license", color="#ff7f0e")
ax.bar(years_mix, serv, bottom=[p+l for p,l in zip(prod_sales, ip_lic)], label="Engineering services", color="#2ca02c")
ax.set_ylabel("Revenue (USD millions)")
ax.set_title("Credo — Revenue Mix Shift: Product sales (AEC-led) now 97% of revenue")
ax.legend()
plt.tight_layout()
plt.savefig(OUT / "crdo_revenue_mix.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts written to", OUT)
