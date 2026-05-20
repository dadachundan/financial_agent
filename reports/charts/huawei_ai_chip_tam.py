"""China data-center AI accelerator market 2023-2030 (approximate, USD bn).

Sources cited inline in the report:
- IDC "Worldwide AI Accelerator" forecasts (Aug 2025) for China share.
- TrendForce / Omdia China AI chip outlook (Q4 2025 update).
- Reuters reporting on the Chinese accelerator market doubling 2025-2027.

This chart shows orders of magnitude only; precise vendor splits are not
broken out by source. Figures shown are mid-points of cited ranges and
should be read as directional, not point-estimates.
"""
import matplotlib.pyplot as plt
import numpy as np

years = ["2023", "2024", "2025e", "2026e", "2027e", "2028e", "2030e"]
total_china = [11, 23, 38, 55, 72, 92, 130]
huawei_share_pct = [10, 23, 35, 42, 47, 50, 55]
huawei_value = [t * s / 100 for t, s in zip(total_china, huawei_share_pct)]
nvidia_value = [t - h for t, h in zip(total_china, huawei_value)]

x = np.arange(len(years))
width = 0.65

fig, ax = plt.subplots(figsize=(11, 5.5))
b1 = ax.bar(x, huawei_value, width, color="#b22222", label="Huawei Ascend (est.)")
b2 = ax.bar(x, nvidia_value, width, bottom=huawei_value,
            color="#76b900", label="Nvidia + other foreign (China-spec)")

ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=10)
ax.set_ylabel("China AI accelerator revenue (USD bn)", fontsize=11)
ax.set_title("China AI Accelerator Market — Estimated Huawei vs. Foreign Share\n"
             "(2023-2030, USD bn; directional only)", fontsize=12, pad=12)

for i, (h, n) in enumerate(zip(huawei_value, nvidia_value)):
    if h > 2:
        ax.text(x[i], h/2, f"{h:.0f}", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")
    if n > 2:
        ax.text(x[i], h + n/2, f"{n:.0f}", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")
    total = h + n
    ax.text(x[i], total + 2, f"${total:.0f}B",
            ha="center", fontsize=9, color="#333333")

ax.legend(loc="upper left", fontsize=10)
ax.set_ylim(0, 150)
ax.grid(axis="y", linestyle=":", alpha=0.4)

fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/huawei_ai_chip_tam.png",
            dpi=150, bbox_inches="tight")
print("saved huawei_ai_chip_tam")
