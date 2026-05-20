"""GAC Group sales by major brand (万辆) FY2024 vs FY2025."""
import matplotlib.pyplot as plt
import numpy as np

brands = ["GAC Toyota", "GAC Honda", "AION + Hyper", "Trumpchi", "Wuyang Honda\n(motos)"]
fy2024 = [73.8, 47.0, 37.49, 41.46, 60.0]
fy2025 = [75.6, 35.0, 29.01, 31.92, 64.0]

x = np.arange(len(brands))
w = 0.38
fig, ax = plt.subplots(figsize=(10, 5.5))
b1 = ax.bar(x - w/2, fy2024, w, label="FY2024", color="#8c8c8c")
b2 = ax.bar(x + w/2, fy2025, w, label="FY2025", color="#1f77b4")

ax.set_xticks(x)
ax.set_xticklabels(brands)
ax.set_ylabel("Units sold (10k units)")
ax.set_title("GAC Group — Sales Volume by Brand, FY2024 vs FY2025")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)

for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h:.1f}", ha="center", fontsize=9)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/gac_brand_sales.png", dpi=150, bbox_inches="tight")
print("saved")
