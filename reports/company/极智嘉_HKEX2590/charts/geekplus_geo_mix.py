"""极智嘉境外/境内收入占比."""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

# 来源：极智嘉 2025 中期报告 + 招股书
years = ["2022", "2023", "2024", "2025H1"]
overseas_pct = [73.4, 75.8, 78.0, 79.5]  # %
domestic_pct = [100 - x for x in overseas_pct]

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(years, overseas_pct, color="#3b6fb5", label="境外收入占比")
ax.bar(years, domestic_pct, bottom=overseas_pct, color="#bcbcbc", label="中国大陆收入占比")

for i, y in enumerate(years):
    ax.text(i, overseas_pct[i] / 2, f"{overseas_pct[i]:.1f}%", ha="center", color="white", fontsize=11, fontweight="bold")
    ax.text(i, overseas_pct[i] + domestic_pct[i] / 2, f"{domestic_pct[i]:.1f}%", ha="center", color="black", fontsize=10)

ax.set_ylim(0, 100)
ax.set_ylabel("收入占比（%）")
ax.set_title("极智嘉境外 vs 中国大陆收入占比（2022–2025H1）")
ax.legend(loc="lower right")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/geekplus_geo_mix.png", dpi=150, bbox_inches="tight")
print("done")
