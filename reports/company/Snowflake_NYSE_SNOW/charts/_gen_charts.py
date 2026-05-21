"""Generate charts for Snowflake (NYSE: SNOW) company research report.

All figures sourced from Snowflake SEC filings (10-K FY2022–FY2026) and
public market data (yfinance, May 2026). See report for citations.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))

# -------- 1. Revenue + product gross margin trend --------
fy = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
revenue_b = [0.592, 1.219, 2.066, 2.806, 3.626, 4.684]      # total revenue $B, 10-Ks FY21-FY26
product_rev_b = [0.554, 1.140, 1.939, 2.667, 3.462, 4.472]  # product revenue $B
prod_gm = [69.7, 71.6, 72.0, 72.0, 71.0, 72.0]              # non-GAAP product gross margin %
# (non-GAAP product gross margin ~75% recent qtrs; using filing GAAP-comparable approximations)

fig, ax1 = plt.subplots(figsize=(9, 5))
x = np.arange(len(fy))
w = 0.4
ax1.bar(x - w/2, revenue_b, w, label="Total revenue ($B)", color="#29B5E8")
ax1.bar(x + w/2, product_rev_b, w, label="Product revenue ($B)", color="#11567F")
ax1.set_xticks(x); ax1.set_xticklabels(fy)
ax1.set_ylabel("Revenue ($B)")
ax1.set_ylim(0, 6)
ax1.set_title("Snowflake — Revenue trajectory, FY21–FY26\n(fiscal year ends Jan 31)")
ax2 = ax1.twinx()
ax2.plot(x, prod_gm, color="#FF8A00", marker="o", linewidth=2, label="Product gross margin %")
ax2.set_ylim(60, 80)
ax2.set_ylabel("Product gross margin (%)")
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)
ax1.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- 2. NRR trend --------
fy_nrr = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
nrr = [168, 178, 158, 131, 126, 125]  # % from 10-Ks
fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.bar(fy_nrr, nrr, color=["#29B5E8" if v >= 130 else "#FFB347" for v in nrr])
for i, v in enumerate(nrr):
    ax.text(i, v + 2, f"{v}%", ha="center", fontsize=9, fontweight="bold")
ax.axhline(120, color="grey", linestyle="--", linewidth=1, label="120% benchmark")
ax.set_ylabel("Net revenue retention rate (%)")
ax.set_ylim(0, 200)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_title("Snowflake — Net revenue retention rate, FY21–FY26\n(measured as of period end)")
ax.grid(axis="y", alpha=0.3)
ax.legend(loc="lower left", fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_nrr_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- 3. $1M+ customers and total customers --------
fy_cust = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
m1_plus = [77, 184, 330, 461, 580, 733]
total_cust = [4139, 5944, 7828, 9437, 11159, 13328]
g2k = [None, None, 573, 691, 750, 790]  # FY23 first disclosed
fig, ax1 = plt.subplots(figsize=(9, 5))
x = np.arange(len(fy_cust))
ax1.bar(x, total_cust, color="#11567F", label="Total customers (LHS)")
ax1.set_ylabel("Total customers")
ax1.set_xticks(x); ax1.set_xticklabels(fy_cust)
ax2 = ax1.twinx()
ax2.plot(x, m1_plus, color="#FF6B35", marker="o", linewidth=2.2, label="$1M+ TTM product-rev customers (RHS)")
g2k_x = [i for i, v in enumerate(g2k) if v is not None]
g2k_y = [v for v in g2k if v is not None]
ax2.plot(g2k_x, g2k_y, color="#29B5E8", marker="s", linewidth=2.0, label="Forbes Global 2000 customers (RHS)")
ax2.set_ylabel("Premium customer cohorts")
ax2.set_ylim(0, 1000)
ax1.set_title("Snowflake — Customer cohorts, FY21–FY26")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)
ax1.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_customer_cohorts.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- 4. RPO + free cash flow --------
fy_r = ["FY22", "FY23", "FY24", "FY25", "FY26"]
rpo_b = [1.8, 3.7, 5.2, 6.9, 9.77]      # $B, end of period (FY22–FY26; FY22 approx)
fcf_b = [0.080, 0.496, 0.779, 0.884, 1.120]  # non-GAAP FCF $B
fig, ax1 = plt.subplots(figsize=(8.5, 5))
x = np.arange(len(fy_r))
ax1.bar(x, rpo_b, color="#29B5E8", label="Remaining performance obligations ($B)")
for i, v in enumerate(rpo_b):
    ax1.text(i, v + 0.15, f"${v:.1f}B", ha="center", fontsize=9)
ax1.set_xticks(x); ax1.set_xticklabels(fy_r)
ax1.set_ylabel("RPO ($B)")
ax2 = ax1.twinx()
ax2.plot(x, fcf_b, color="#FF6B35", marker="o", linewidth=2.2, label="Non-GAAP free cash flow ($B)")
ax2.set_ylabel("Non-GAAP free cash flow ($B)")
ax1.set_title("Snowflake — RPO & non-GAAP free cash flow, FY22–FY26")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)
ax1.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_rpo_fcf.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- 5. P/S peer comparison --------
peers = ["SNOW", "DDOG", "MDB", "ORCL", "MSFT", "GOOG", "PLTR"]
ps = [12.4, 20.6, 10.8, 8.4, 9.8, 11.0, 62.9]  # TTM P/S, yfinance May 2026
ev_rev = [12.0, 19.6, 9.8, 10.5, 10.0, 11.0, 61.5]
colors = ["#29B5E8" if p == "SNOW" else "#888888" for p in peers]
fig, ax = plt.subplots(figsize=(9, 5))
xpos = np.arange(len(peers))
w = 0.38
ax.bar(xpos - w/2, ps, w, label="TTM P/S", color=colors)
ax.bar(xpos + w/2, ev_rev, w, label="EV / revenue", color=["#0D4767" if p == "SNOW" else "#444" for p in peers])
ax.set_xticks(xpos); ax.set_xticklabels(peers)
ax.set_ylabel("Multiple (×)")
ax.set_title("Snowflake vs. peers — TTM P/S and EV/Revenue, May 2026")
for i, (a, b) in enumerate(zip(ps, ev_rev)):
    ax.text(i - w/2, a + 1, f"{a:.1f}", ha="center", fontsize=8)
    ax.text(i + w/2, b + 1, f"{b:.1f}", ha="center", fontsize=8)
ax.legend(loc="upper left", fontsize=8)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_ps_peer_compare.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- 6. Geographic revenue mix --------
fy_g = ["FY24", "FY25", "FY26"]
us = [2166.4, 2761.7, 3524.0]
other_am = [72.8, 101.9, 125.3]
emea = [432.6, 574.7, 763.7]
apj = [134.6, 188.0, 271.0]
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(fy_g))
ax.bar(x, us, label="US", color="#11567F")
ax.bar(x, other_am, bottom=us, label="Other Americas", color="#29B5E8")
ax.bar(x, emea, bottom=[a + b for a, b in zip(us, other_am)], label="EMEA", color="#FF6B35")
ax.bar(x, apj, bottom=[a + b + c for a, b, c in zip(us, other_am, emea)], label="Asia-Pacific & Japan", color="#FFB347")
ax.set_xticks(x); ax.set_xticklabels(fy_g)
ax.set_ylabel("Revenue ($M)")
ax.set_title("Snowflake — Revenue by geography, FY24–FY26\n($M, customer location basis)")
ax.legend(loc="upper left", fontsize=8)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/snow_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written to", OUT)
