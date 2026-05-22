"""Will Semiconductor / OmniVision Group revenue + net margin chart."""
import matplotlib.pyplot as plt

years = ["2021", "2022", "2023", "2024", "2025"]
revenue_bn = [24.10, 20.08, 21.02, 25.73, 28.85]  # RMB bn
net_income_bn = [4.48, 0.99, 0.56, 3.32, 4.05]    # RMB bn

fig, ax1 = plt.subplots(figsize=(9, 5))
color_rev = "#1f77b4"
color_ni = "#d62728"

bars = ax1.bar(years, revenue_bn, color=color_rev, alpha=0.85, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color=color_rev, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color_rev)
ax1.set_ylim(0, 35)
for bar, v in zip(bars, revenue_bn):
    ax1.text(bar.get_x() + bar.get_width()/2, v + 0.4, f"{v:.1f}",
             ha="center", va="bottom", fontsize=9, color=color_rev)

ax2 = ax1.twinx()
ax2.plot(years, net_income_bn, marker="o", color=color_ni,
         linewidth=2.5, label="Net income (RMB bn)")
ax2.set_ylabel("Net income to parent (RMB bn)", color=color_ni, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color_ni)
ax2.set_ylim(0, 6)
for x, y in zip(years, net_income_bn):
    ax2.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=9, color=color_ni)

plt.title("OmniVision Group (SSE:603501) — Revenue & Net Income, 2021–2025",
          fontsize=12, pad=12)
ax1.grid(axis="y", linestyle=":", alpha=0.4)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/omnivision_rev_margin.png",
            dpi=150, bbox_inches="tight")
print("saved")
