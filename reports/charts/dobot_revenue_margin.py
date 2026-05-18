"""Dobot revenue + gross margin 2021-2025 (RMB mn / %)."""
import matplotlib.pyplot as plt

years = ["2021", "2022", "2023", "2024", "2025"]
revenue = [174, 242, 287, 374, 492]  # RMB mn
gm = [41.0, 43.5, 43.7, 46.6, 47.5]  # %

fig, ax1 = plt.subplots(figsize=(8, 4.8))
bars = ax1.bar(years, revenue, color="#2b6cb0", alpha=0.85, label="Revenue (RMB mn)")
ax1.set_ylabel("Revenue (RMB mn)", color="#2b6cb0")
ax1.tick_params(axis="y", labelcolor="#2b6cb0")
ax1.set_ylim(0, max(revenue) * 1.25)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 8, f"{v}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gm, color="#c05621", marker="o", linewidth=2.2, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)", color="#c05621")
ax2.tick_params(axis="y", labelcolor="#c05621")
ax2.set_ylim(35, 55)
for x, y in zip(years, gm):
    ax2.text(x, y + 0.6, f"{y:.1f}%", ha="center", fontsize=9, color="#c05621")

plt.title("Dobot (HKEX:2432) Revenue & Gross Margin, FY2021–FY2025")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/dobot_revenue_margin.png",
            dpi=150, bbox_inches="tight")
