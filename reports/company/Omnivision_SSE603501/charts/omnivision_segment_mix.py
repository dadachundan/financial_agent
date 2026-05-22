"""OmniVision 2025 CIS revenue by end-market."""
import matplotlib.pyplot as plt

# 2025 CIS end-market split (RMB bn) — from 2025 年度报告 Section 3
markets = ["Smartphone", "Automotive", "Emerging\n(robotics,\nXR, action cam)",
           "Security", "Medical"]
revenue = [82.72, 74.71, 23.69, 17.76, 9.74]  # RMB 100M
yoy = [-15.6, 26.5, 211.9, 10.8, 45.7]        # YoY % growth

fig, ax = plt.subplots(figsize=(10, 5.5))
colors = ["#4C72B0", "#DD8452", "#C44E52", "#8172B3", "#937860"]
bars = ax.bar(markets, revenue, color=colors)

for bar, rev, g in zip(bars, revenue, yoy):
    label = f"RMB {rev:.1f}\n{g:+.1f}% YoY"
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            label, ha="center", va="bottom", fontsize=9)

ax.set_ylabel("Revenue (RMB 100M)", fontsize=11)
ax.set_title("OmniVision Group — 2025 CIS revenue by end-market", fontsize=12)
ax.set_ylim(0, max(revenue) * 1.25)
ax.grid(axis="y", linestyle=":", alpha=0.4)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/omnivision_segment_mix.png",
            dpi=150, bbox_inches="tight")
print("saved")
