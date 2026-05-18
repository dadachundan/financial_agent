"""CMOS image-sensor industry TAM 2020-2030E."""
import matplotlib.pyplot as plt

years = ["2020", "2021", "2022", "2023", "2024", "2025E", "2026E", "2028E", "2030E"]
tam = [20.7, 22.9, 21.3, 21.6, 23.1, 24.6, 26.4, 30.2, 34.5]  # USD bn (Yole/MMR composite)

fig, ax = plt.subplots(figsize=(9, 5))
ax.fill_between(years, tam, alpha=0.25, color="#4C72B0")
ax.plot(years, tam, marker="o", color="#4C72B0", linewidth=2)
for x, y in zip(years, tam):
    ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=9)

ax.set_ylabel("Global CIS market (USD bn)", fontsize=11)
ax.set_title("Global CMOS image-sensor market, 2020–2030E (USD bn)", fontsize=12)
ax.set_ylim(0, 40)
ax.grid(axis="y", linestyle=":", alpha=0.4)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/omnivision_cis_tam.png",
            dpi=150, bbox_inches="tight")
print("saved")
