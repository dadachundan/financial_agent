"""Huawei vs. listed peers — revenue comparison (FY2024 / latest disclosed).

All in USD bn (converted at year-average rates). Huawei is private; comparison
is on scale and segment overlap, not valuation. Listed peers shown with
TTM market cap for context.

Sources (cited inline in the report):
- Huawei 2024 Annual Report: RMB 862.1 bn = ~USD 120 bn (6.85 avg rate).
- Apple FY2024 (Sept fiscal year): USD 391 bn (10-K).
- Samsung Electronics FY2024: KRW 300.9 trn = ~USD 220 bn (DART business report).
- Cisco FY2025 (July fiscal): USD 56.7 bn (10-K).
- Nokia FY2024: EUR 19.4 bn = ~USD 21 bn.
- Ericsson FY2024: SEK 247.9 bn = ~USD 23.5 bn.
- Lenovo FY2024/25 (Mar fiscal): USD 69.1 bn (annual report).
"""
import matplotlib.pyplot as plt
import numpy as np

companies = ["Apple\nAAPL", "Samsung\n005930.KS", "Huawei\n(private)",
             "Lenovo\n0992.HK", "Cisco\nCSCO", "Ericsson\nERIC", "Nokia\nNOK"]
revenue_usd = [391.0, 220.0, 120.0, 69.1, 56.7, 23.5, 21.0]
# Huawei sets the highlight color
colors = ["#7f8c8d", "#7f8c8d", "#b22222", "#7f8c8d", "#7f8c8d", "#7f8c8d", "#7f8c8d"]

fig, ax = plt.subplots(figsize=(11, 5.5))
bars = ax.barh(companies, revenue_usd, color=colors, alpha=0.85)
ax.set_xlabel("Revenue (USD bn, latest reported full-year)", fontsize=11)
ax.set_title("Huawei vs. Listed Comparables — Revenue Scale (USD bn)",
             fontsize=12, pad=12)
ax.invert_yaxis()
for b, v in zip(bars, revenue_usd):
    ax.text(b.get_width() + 4, b.get_y() + b.get_height()/2, f"${v:,.0f} bn",
            va="center", fontsize=10,
            color="#b22222" if v == 120.0 else "#333333",
            fontweight="bold" if v == 120.0 else "normal")
ax.set_xlim(0, 440)
ax.grid(axis="x", linestyle=":", alpha=0.4)
ax.text(440, len(companies)-0.5,
        "Huawei is private and not for sale.\nComparison is scale-only.",
        ha="right", va="center", fontsize=9, color="#555555", style="italic")

fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/huawei_peer_revenue.png",
            dpi=150, bbox_inches="tight")
print("saved huawei_peer_revenue")
