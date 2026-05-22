import matplotlib.pyplot as plt
import numpy as np

# Segment revenue RMB bn FY2023, FY2024, FY2025
segments = ["Smartphones", "IoT & lifestyle", "Internet services", "Smart EV & new initiatives"]
fy2023 = [157.5, 80.1, 30.1, 0.0]
fy2024 = [191.8, 104.1, 34.1, 32.8]   # smart EV first full year (partial)
fy2025 = [186.5, 123.2, 41.5, 106.1]  # approximations from H1 + FY total

years = ["FY2023", "FY2024", "FY2025"]
data = np.array([fy2023, fy2024, fy2025])

fig, ax = plt.subplots(figsize=(10, 5.5))

colors = ["#FF6900", "#FFB36B", "#7AA9FF", "#4F4F4F"]
bottom = np.zeros(3)
for i, seg in enumerate(segments):
    ax.bar(years, data[:, i], bottom=bottom, color=colors[i], label=seg, width=0.55)
    for j, v in enumerate(data[:, i]):
        if v > 10:
            ax.text(j, bottom[j] + v / 2, f"{v:.0f}", ha="center", va="center", fontsize=9,
                    color="white" if i in (0, 3) else "black", fontweight="bold")
    bottom = bottom + data[:, i]

totals = data.sum(axis=1)
for j, t in enumerate(totals):
    ax.text(j, t + 8, f"Total\n{t:.0f}", ha="center", fontsize=10, fontweight="bold")

ax.set_ylabel("Revenue (RMB bn)", fontsize=12)
ax.set_ylim(0, 520)
ax.set_title("Xiaomi — Segment Revenue Mix, FY2023–FY2025", fontsize=13)
ax.legend(loc="upper left", fontsize=10)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/xiaomi_segment_mix.png", dpi=150, bbox_inches="tight")
print("saved")
