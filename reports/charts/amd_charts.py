"""Charts for AMD initiation report — 2026-05-20.
Sources: AMD 10-K FY2023, FY2024, FY2025 (SEC EDGAR); AMD Q1-2026 10-Q;
AMD Q1-2026 earnings press release; Yahoo Finance (peer multiples).
"""
import matplotlib.pyplot as plt
import numpy as np

OUT = "/Users/x/projects/financial_agent/reports/charts"

# ----- 1. Revenue + gross margin trend (FY2023–FY2025 + Q1-26 LTM proxy) -----
# Source: 10-Ks; GM from MD&A
years = ["FY2023", "FY2024", "FY2025"]
revenue_bn = [22.680, 25.785, 34.639]
# Gross margin GAAP from MD&A: FY23 46%, FY24 49%, FY25 50%
gm_pct = [46.0, 49.0, 50.0]
fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
bars = ax1.bar(years, revenue_bn, color="#ED1C24", alpha=0.85, label="Revenue (USD bn)")
ax1.set_ylabel("Revenue (USD bn)", color="#ED1C24", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#ED1C24")
ax1.set_ylim(0, 45)
for b, v in zip(bars, revenue_bn):
    ax1.text(b.get_x()+b.get_width()/2, v+0.6, f"${v:.1f}B", ha="center", fontsize=10, fontweight="bold")
ax2 = ax1.twinx()
ax2.plot(years, gm_pct, color="#0066B2", marker="o", linewidth=2.2, label="GAAP gross margin (%)")
ax2.set_ylabel("GAAP gross margin (%)", color="#0066B2", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#0066B2")
ax2.set_ylim(40, 56)
for x, y in zip(years, gm_pct):
    ax2.annotate(f"{y:.0f}%", (x, y), textcoords="offset points", xytext=(0, 9), ha="center",
                 color="#0066B2", fontsize=10, fontweight="bold")
plt.title("AMD: revenue and gross margin trend (FY2023–FY2025)", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/amd_revenue_gm_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ----- 2. Segment revenue mix stacked bar FY2023–FY2025 -----
# Source: AMD 2024 10-K (3-yr table) + 2025 10-K
# Note: in FY25 Client+Gaming combined; for chart show Client and Gaming separately consistent through 3 years
dc =      [6.496, 12.579, 16.635]
client =  [4.651, 7.054, 10.640]
gaming =  [6.212, 2.595, 3.910]
embedded= [5.321, 3.557, 3.454]
fig, ax = plt.subplots(figsize=(8.5, 5))
x = np.arange(len(years))
ax.bar(x, dc, color="#ED1C24", label="Data Center")
ax.bar(x, client, bottom=dc, color="#000000", label="Client")
ax.bar(x, gaming, bottom=[a+b for a,b in zip(dc,client)], color="#666666", label="Gaming")
ax.bar(x, embedded, bottom=[a+b+c for a,b,c in zip(dc,client,gaming)], color="#FF8800", label="Embedded")
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel("Net revenue (USD bn)", fontsize=11)
ax.set_title("AMD segment revenue mix, FY2023–FY2025", fontsize=12, fontweight="bold")
ax.legend(loc="upper left")
# Annotate DC % of total
totals = [a+b+c+d for a,b,c,d in zip(dc,client,gaming,embedded)]
for i, t in enumerate(totals):
    dc_share = dc[i]/t*100
    ax.text(i, t+0.7, f"DC {dc_share:.0f}%\nTotal ${t:.1f}B", ha="center", fontsize=9)
ax.set_ylim(0, 42)
plt.tight_layout()
plt.savefig(f"{OUT}/amd_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ----- 3. Data Center segment quarterly ramp (Instinct era) -----
# Sources: AMD quarterly earnings releases
labels = ["Q1-24", "Q2-24", "Q3-24", "Q4-24", "Q1-25", "Q2-25", "Q3-25", "Q4-25", "Q1-26"]
dc_q   = [2.337, 2.834, 3.549, 3.859, 3.674, 3.235, 4.337, 5.388, 5.775]  # $bn
fig, ax = plt.subplots(figsize=(9, 4.6))
bars = ax.bar(labels, dc_q, color="#ED1C24")
ax.set_ylabel("Data Center segment revenue (USD bn)", fontsize=11)
ax.set_title("AMD Data Center segment: quarterly revenue ramp, Q1-24 → Q1-26", fontsize=12, fontweight="bold")
for b, v in zip(bars, dc_q):
    ax.text(b.get_x()+b.get_width()/2, v+0.08, f"${v:.2f}", ha="center", fontsize=8.5)
ax.set_ylim(0, 6.8)
# Annotate MI308 export-control hit in Q2-25
ax.annotate("MI308 export\ncontrol charge\n(~$800M)", xy=(5, 3.235), xytext=(4.4, 5.3),
            arrowprops=dict(arrowstyle="->", color="black"), fontsize=8, ha="center")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUT}/amd_dc_quarterly_ramp.png", dpi=150, bbox_inches="tight")
plt.close()

# ----- 4. R&D spend in dollars and as % of revenue -----
# Source: AMD 10-Ks (R&D line)
years_full = ["FY2022", "FY2023", "FY2024", "FY2025"]
rev =  [23.601, 22.680, 25.785, 34.639]
rd =   [5.005, 5.872, 6.456, 8.091]
rd_pct = [r/v*100 for r, v in zip(rd, rev)]
fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
bars = ax1.bar(years_full, rd, color="#0066B2", alpha=0.85)
ax1.set_ylabel("R&D expense (USD bn)", color="#0066B2", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#0066B2")
for b, v in zip(bars, rd):
    ax1.text(b.get_x()+b.get_width()/2, v+0.1, f"${v:.2f}B", ha="center", fontsize=10, fontweight="bold")
ax1.set_ylim(0, 10)
ax2 = ax1.twinx()
ax2.plot(years_full, rd_pct, color="#ED1C24", marker="o", linewidth=2.2)
ax2.set_ylabel("R&D as % of revenue", color="#ED1C24", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#ED1C24")
ax2.set_ylim(15, 30)
for x, y in zip(years_full, rd_pct):
    ax2.annotate(f"{y:.0f}%", (x, y), textcoords="offset points", xytext=(0, 9), ha="center",
                 color="#ED1C24", fontsize=10, fontweight="bold")
plt.title("AMD R&D spend and intensity, FY2022–FY2025", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUT}/amd_rd_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# ----- 5. Peer valuation snapshot (TTM P/E and TTM P/S) -----
# Source: Yahoo Finance, retrieved 2026-05-20
tickers = ["AMD", "NVDA", "AVGO", "INTC"]
ttm_pe = [149.1, 45.4, 81.3, float("nan")]  # INTC negative TTM EPS
ttm_ps = [19.3, 25.0, 29.0, 11.0]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
axes[0].bar(tickers, [v if not np.isnan(v) else 0 for v in ttm_pe], color=["#ED1C24","#76B900","#CC092F","#0071C5"])
axes[0].set_title("TTM P/E (×)", fontweight="bold")
for i, v in enumerate(ttm_pe):
    label = "n/m\n(neg EPS)" if np.isnan(v) else f"{v:.0f}×"
    axes[0].text(i, (v if not np.isnan(v) else 0)+3, label, ha="center", fontsize=10, fontweight="bold")
axes[0].set_ylim(0, 175)
axes[1].bar(tickers, ttm_ps, color=["#ED1C24","#76B900","#CC092F","#0071C5"])
axes[1].set_title("TTM P/S (×)", fontweight="bold")
for i, v in enumerate(ttm_ps):
    axes[1].text(i, v+0.5, f"{v:.1f}×", ha="center", fontsize=10, fontweight="bold")
axes[1].set_ylim(0, 35)
plt.suptitle("Peer valuation snapshot — AMD vs. NVDA / AVGO / INTC (TTM, as of 2026-05-20)",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUT}/amd_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close()

# ----- 6. Server CPU revenue share narrative: AMD vs Intel DCG/DCAI (datacenter segment) -----
# AMD Data Center segment (includes GPU, networking, DC CPU) vs Intel Data Center & AI (DCAI)
# Sources: AMD 10-Ks; Intel 10-Ks for DCAI revenue.
# Sources:
#  AMD 10-K FY23/24/25 (Data Center segment).
#  Intel DCAI segment revenue from Intel 10-K FY2023 ($15.521B) and FY2024 ($12.829B). FY25 omitted — not yet verified against Intel filings.
# Note: AMD Data Center segment now includes Instinct GPUs and Pensando; Intel DCAI is Xeon + Gaudi. Apples-to-apples imperfect — see chart caption.
years_dc = ["FY2023", "FY2024"]
amd_dc =   [6.496, 12.579]
intel_dcai=[15.521, 12.829]
x = np.arange(len(years_dc))
w = 0.36
fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.bar(x-w/2, amd_dc, w, label="AMD Data Center segment", color="#ED1C24")
ax.bar(x+w/2, intel_dcai, w, label="Intel DCAI segment", color="#0071C5")
ax.set_xticks(x); ax.set_xticklabels(years_dc)
ax.set_ylabel("Segment revenue (USD bn)", fontsize=11)
ax.set_title("AMD Data Center vs. Intel DCAI segment revenue, FY2023–FY2024", fontsize=12, fontweight="bold")
for i, (a, b) in enumerate(zip(amd_dc, intel_dcai)):
    ax.text(i-w/2, a+0.3, f"${a:.1f}", ha="center", fontsize=9)
    ax.text(i+w/2, b+0.3, f"${b:.1f}", ha="center", fontsize=9)
ax.legend(loc="upper left")
ax.set_ylim(0, 20)
plt.tight_layout()
plt.savefig(f"{OUT}/amd_vs_intel_dc.png", dpi=150, bbox_inches="tight")
plt.close()

print("done")
