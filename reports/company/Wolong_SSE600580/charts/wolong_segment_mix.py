"""Wolong segment revenue mix FY2024 vs FY2025."""
import matplotlib.pyplot as plt
import numpy as np

segments = ["Explosion-\nproof", "Industrial", "HVAC/\nappliance", "EV / new-\nenergy transport", "Robotics\ncomponents", "Other"]
# RMB bn, from 2025 年报 pages 24
fy24 = [4.696, 4.064, 4.593, 0.390, 0.451, 1.661]
fy25 = [4.633, 4.095, 4.958, 0.433, 0.516, 0.488]

x = np.arange(len(segments))
w = 0.38

fig, ax = plt.subplots(figsize=(10, 5.5))
b1 = ax.bar(x - w/2, fy24, w, label="FY2024", color="#7f7f7f")
b2 = ax.bar(x + w/2, fy25, w, label="FY2025", color="#1f77b4")

ax.set_ylabel("Revenue (RMB bn)")
ax.set_title("Wolong Electric Drive — segment revenue mix, FY2024 vs FY2025")
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=9)
ax.legend()

for bars in [b1, b2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f"{h:.2f}", ha="center", fontsize=8)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/wolong_segment_mix.png", dpi=150, bbox_inches="tight")
print("saved")
