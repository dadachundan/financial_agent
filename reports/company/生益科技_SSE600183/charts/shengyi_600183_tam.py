"""
生益科技 (SSE:600183) — Global CCL Market Size & Forecast
Data: Business Research Insights / Fortune Business Insights 2025 reports;
Prismark PCB data cited in 2025 annual report.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Global CCL market size USD bn — from multiple industry sources
years = [2022, 2023, 2024, 2025, 2026, 2027, 2028]
ccl_total = [16.5, 15.8, 17.2, 20.5, 21.6, 23.1, 25.0]   # USD bn (mixed sources)
ccl_hspeed = [3.2, 3.8, 5.2, 7.5, 10.0, 13.5, 18.0]       # High-speed sub-segment USD bn (approx)

# Distinction: solid = actual, dashed = forecast
fig, ax = plt.subplots(figsize=(10, 5.5))

color_total = "#2A6EBB"
color_hs = "#E74C3C"

# Actual vs forecast split
split = 5  # 2025 is the boundary between reported and forecast

ax.fill_between(years[:split], ccl_total[:split], alpha=0.15, color=color_total)
ax.plot(years[:split], ccl_total[:split], "o-", color=color_total, linewidth=2.2, markersize=7, label="全球CCL市场规模(已实现)")
ax.plot(years[split-1:], ccl_total[split-1:], "o--", color=color_total, linewidth=2.2, markersize=7, label="全球CCL市场规模(预测)")

ax.fill_between(years[:split], ccl_hspeed[:split], alpha=0.15, color=color_hs)
ax.plot(years[:split], ccl_hspeed[:split], "s-", color=color_hs, linewidth=2.2, markersize=7, label="高速/高频CCL子市场(已实现)")
ax.plot(years[split-1:], ccl_hspeed[split-1:], "s--", color=color_hs, linewidth=2.2, markersize=7, label="高速/高频CCL子市场(预测)")

ax.set_xlabel("年份", fontsize=12)
ax.set_ylabel("市场规模 (十亿美元)", fontsize=12)
ax.set_title("全球覆铜板 (CCL) 市场规模及高速高频子市场趋势 2022–2028E", fontsize=12, fontweight="bold")
ax.legend(fontsize=9.5, loc="upper left")
ax.set_xticks(years)
ax.set_ylim(0, 30)
ax.grid(axis="y", alpha=0.3)

# Annotation
ax.axvline(x=2025.5, color="gray", linestyle=":", alpha=0.5)
ax.text(2025.6, 27, "← 实际  预测 →", fontsize=9, color="gray")

plt.tight_layout()
path = "/Users/x/projects/financial_agent/reports/charts/shengyi_600183_tam.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
print(f"Saved: {path}")
