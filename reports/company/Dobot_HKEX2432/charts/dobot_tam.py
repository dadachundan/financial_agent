"""Global cobot TAM, 2024-2030 (USD bn)."""
import matplotlib.pyplot as plt

years = list(range(2024, 2031))
# Blended MarketsandMarkets / Fortune Business Insights mid-case (USD bn)
tam = [1.20, 1.42, 1.72, 2.05, 2.45, 2.88, 3.38]

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(years, tam, color="#2b6cb0", marker="o", linewidth=2.4)
ax.fill_between(years, [v * 0.85 for v in tam], [v * 1.25 for v in tam],
                color="#2b6cb0", alpha=0.12, label="Forecast range")
for x, y in zip(years, tam):
    ax.text(x, y + 0.08, f"${y:.1f}B", ha="center", fontsize=9)
ax.set_ylabel("Global cobot TAM (USD bn)")
ax.set_xlabel("Year")
ax.set_title("Global Collaborative Robot TAM, 2024–2030\n(MarketsandMarkets mid-case, CAGR ~19%)")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.25)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/dobot_tam.png",
            dpi=150, bbox_inches="tight")
