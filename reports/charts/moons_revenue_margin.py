"""Moons' Electric 6-yr revenue, net margin, gross margin chart."""
import matplotlib.pyplot as plt
import os

years = [2020, 2021, 2022, 2023, 2024, 2025]
revenue_m = [2212.8, 2714.2, 2960.0, 2542.8, 2415.9, 2762.0]  # RMB millions
net_income_m = [200.8, 279.6, 247.2, 140.4, 77.9, 61.1]
gross_margin = [38.6, 39.3, 38.2, 37.2, 37.7, 36.4]  # %, derived from filings

fig, ax1 = plt.subplots(figsize=(10, 5.5))

color_rev = "#1f77b4"
color_ni = "#d62728"
color_gm = "#2ca02c"

bars = ax1.bar([y - 0.18 for y in years], revenue_m, width=0.36, color=color_rev,
               label="Revenue (RMB m)", alpha=0.85)
bars2 = ax1.bar([y + 0.18 for y in years], net_income_m, width=0.36, color=color_ni,
                label="Net income attributable to parent (RMB m)", alpha=0.85)

ax1.set_xlabel("Fiscal Year")
ax1.set_ylabel("RMB millions", color="#333333")
ax1.set_xticks(years)
ax1.set_ylim(0, 3300)
ax1.legend(loc="upper left", framealpha=0.95)

for x, v in zip(years, revenue_m):
    ax1.text(x - 0.18, v + 30, f"{v:,.0f}", ha="center", fontsize=8)
for x, v in zip(years, net_income_m):
    ax1.text(x + 0.18, v + 30, f"{v:,.0f}", ha="center", fontsize=8, color=color_ni)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color=color_gm, marker="o", linewidth=2.0,
         label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color=color_gm)
ax2.set_ylim(30, 45)
ax2.legend(loc="upper right", framealpha=0.95)

for x, v in zip(years, gross_margin):
    ax2.annotate(f"{v:.1f}%", (x, v), textcoords="offset points", xytext=(0, 8),
                 ha="center", fontsize=8, color=color_gm)

plt.title("Moons' Electric (SSE:603728) — 2020-2025 Revenue, Net Income, Gross Margin")
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), "moons_revenue_margin.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out)
