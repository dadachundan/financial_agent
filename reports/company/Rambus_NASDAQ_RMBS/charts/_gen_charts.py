"""Generate charts for Rambus RMBS company research report."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# --- 1. Revenue mix (Product vs Royalties vs Contract) 2021-2025 ----------
# Sources: 2022 10-K p.33-34 (2020-2022 figures) and 2025 10-K p.42-43 (2023-2025 figures)
# Note: Rambus divested SerDes/Memory Interface PHY IP business in Sept 2023;
# product/contract mix is not strictly comparable pre/post-divestiture.
years   = ["2021", "2022", "2023", "2024", "2025"]
product = [143.9, 227.1, 224.6, 246.8, 347.8]   # USD m, from 10-Ks
royalty = [136.7, 139.8, 150.1, 226.2, 279.4]
contract= [ 47.7,  87.9,  86.4,  83.6,  80.5]
fig, ax = plt.subplots(figsize=(8.5, 5))
b1 = ax.bar(years, product, label="Product (Memory Interface Chips)", color="#1f77b4")
b2 = ax.bar(years, royalty, bottom=product, label="Royalties (Patent Licensing)", color="#ff7f0e")
b3 = ax.bar(years, contract, bottom=np.array(product)+np.array(royalty), label="Contract & Other (Silicon IP)", color="#2ca02c")
ax.set_title("Rambus Revenue Mix, FY2021–FY2025 (USD millions)")
ax.set_ylabel("Revenue (USD m)")
ax.legend(loc="upper left", fontsize=9)
for i, y in enumerate(years):
    total = product[i]+royalty[i]+contract[i]
    ax.text(i, total+10, f"${total:.0f}m", ha="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT/"rmbs_revenue_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 2. Product revenue trend (DDR5 ramp proxy) ----------------------------
years2 = ["2020", "2021", "2022", "2023", "2024", "2025"]
product2 = [114.0, 143.9, 227.1, 224.6, 246.8, 347.8]   # 2020-2022 incl. divested PHY IP / security IP
fig, ax = plt.subplots(figsize=(8.5, 4.8))
ax.plot(years2, product2, marker="o", linewidth=2.5, color="#1f77b4")
ax.fill_between(years2, product2, alpha=0.15, color="#1f77b4")
for x, y in zip(years2, product2):
    ax.annotate(f"${y:.0f}m", (x, y), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9)
ax.set_title("Rambus Product Revenue (Memory Interface Chips), FY2020–FY2025")
ax.set_ylabel("USD millions")
ax.annotate("DDR5 RDIMM\nramp inflection",
            xy=("2023", 224.6), xytext=("2021", 280),
            arrowprops=dict(arrowstyle="->", color="#666"), fontsize=10, color="#444")
ax.grid(axis="y", linestyle=":", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT/"rmbs_product_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 3. Gross margin & operating margin trend ------------------------------
# Sources: 2022 10-K (FY2020-2022) and 2025 10-K (FY2023-2025)
years3 = ["2021", "2022", "2023", "2024", "2025"]
gm   = [78.6, 76.3, 77.6, 80.3, 79.6]   # gross profit / revenue
opm  = [ 7.4, 16.9, 33.3, 32.9, 36.8]
fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
ax1.bar(years3, gm, alpha=0.85, color="#2ca02c", label="Gross margin %")
ax1.set_ylabel("Gross margin %", color="#2ca02c")
ax1.set_ylim(0, 100)
ax1.tick_params(axis="y", labelcolor="#2ca02c")
for x, y in zip(years3, gm):
    ax1.text(x, y+1.5, f"{y:.1f}%", ha="center", fontsize=9, color="#2ca02c", fontweight="bold")
ax2 = ax1.twinx()
ax2.plot(years3, opm, marker="o", color="#d62728", linewidth=2.5, label="Operating margin %")
ax2.set_ylabel("Operating margin %", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(0, 50)
for x, y in zip(years3, opm):
    ax2.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, -15), ha="center",
                 fontsize=9, color="#d62728")
ax2.spines["top"].set_visible(False)
ax1.set_title("Rambus Gross Margin and Operating Margin, FY2021–FY2025 (GAAP)")
plt.tight_layout()
plt.savefig(OUT/"rmbs_margin_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 4. P/E and P/S vs peers ----------------------------------------------
peers = ["Rambus\n(RMBS)", "Cadence\n(CDNS)", "Synopsys\n(SNPS)", "Montage\n(688008.SS)", "CEVA", "Silicon Labs\n(SLAB)", "Renesas\n(6723.T)"]
pe    = [67.1, 84.0, 76.9, 117.0, np.nan, np.nan, np.nan]   # NaN = unprofitable / no TTM PE
ps    = [21.1, 17.9, 12.0, 56.3, 9.5, 8.7, 4.9]
x = np.arange(len(peers))
fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
bars1 = axs[0].bar(peers, pe, color=["#1f77b4", "#888", "#888", "#d62728", "#bbb", "#bbb", "#bbb"])
axs[0].set_title("TTM P/E — Rambus vs Semiconductor IP & Memory-IF Peers")
axs[0].set_ylabel("P/E (×)")
for i, v in enumerate(pe):
    if not np.isnan(v):
        axs[0].text(i, v+2, f"{v:.0f}×", ha="center", fontsize=9, fontweight="bold")
    else:
        axs[0].text(i, 5, "n/m\n(unprof.)", ha="center", fontsize=9, color="#666")
axs[0].tick_params(axis="x", labelsize=9)
axs[0].grid(axis="y", linestyle=":", alpha=0.4)
bars2 = axs[1].bar(peers, ps, color=["#1f77b4", "#888", "#888", "#d62728", "#bbb", "#bbb", "#bbb"])
axs[1].set_title("TTM P/S — Rambus vs Semiconductor IP & Memory-IF Peers")
axs[1].set_ylabel("P/S (×)")
for i, v in enumerate(ps):
    axs[1].text(i, v+0.7, f"{v:.1f}×", ha="center", fontsize=9, fontweight="bold")
axs[1].tick_params(axis="x", labelsize=9)
axs[1].grid(axis="y", linestyle=":", alpha=0.4)
plt.tight_layout()
plt.savefig(OUT/"rmbs_valuation_peers.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 5. Geographic revenue mix --------------------------------------------
labels = ["South Korea", "Singapore", "United States", "Other"]
y2025  = [329.3, 163.8, 124.1, 90.5]
y2024  = [197.5,  67.3, 201.5, 90.3]
y2023  = [152.3,  53.3, 176.8, 78.6]
x = np.arange(len(labels))
w = 0.27
fig, ax = plt.subplots(figsize=(8.5, 4.8))
ax.bar(x - w, y2023, w, label="FY2023", color="#aec7e8")
ax.bar(x,     y2024, w, label="FY2024", color="#6baed6")
ax.bar(x + w, y2025, w, label="FY2025", color="#1f77b4")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("USD millions")
ax.set_title("Rambus Revenue by Contracting-Party Geography, FY2023–FY2025")
ax.legend()
for i, v in enumerate(y2025):
    ax.text(i + w, v+5, f"${v:.0f}m", ha="center", fontsize=8, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT/"rmbs_geographic_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# --- 6. RMBS share price 3y ----------------------------------------------
# Use the yfinance series I just pulled
prices = {
    "2023-06": 64.2, "2023-09": 55.8, "2023-12": 68.3, "2024-03": 61.8,
    "2024-06": 58.8, "2024-09": 42.2, "2024-12": 52.9, "2025-03": 51.8,
    "2025-06": 64.0, "2025-09": 104.2, "2025-12": 91.9, "2026-03": 86.0,
    "2026-05": 141.0,
}
dates = list(prices.keys())
vals  = list(prices.values())
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(dates, vals, marker="o", linewidth=2.2, color="#1f77b4")
ax.fill_between(dates, vals, alpha=0.15, color="#1f77b4")
ax.set_title("Rambus (RMBS) Monthly Close Price, June 2023 – May 2026 (USD)")
ax.set_ylabel("Share price (USD)")
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.grid(axis="y", linestyle=":", alpha=0.5)
ax.annotate("DDR5 ramp /\nAI-memory re-rate",
            xy=("2025-09", 104), xytext=("2024-06", 130),
            arrowprops=dict(arrowstyle="->", color="#666"), fontsize=10, color="#444")
plt.tight_layout()
plt.savefig(OUT/"rmbs_price_3y.png", dpi=150, bbox_inches="tight")
plt.close()

print("Saved charts:")
for p in sorted(OUT.glob("*.png")):
    print(" ", p.name, p.stat().st_size, "bytes")
