"""Wolong Electric Drive: 3-year revenue + gross margin trend."""
import matplotlib.pyplot as plt

years = ["2021", "2022", "2023", "2024", "2025"]
# Revenue in RMB bn (from cninfo annual reports)
revenue = [14.00, 14.99, 15.57, 16.25, 15.45]
# Gross margin % (consolidated, approx; from annual reports)
gross_margin = [22.4, 21.1, 22.4, 24.05, 25.37]
# Net income (attributable) RMB bn
net_inc = [0.83, 0.31, 0.53, 0.79, 1.13]

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(years, revenue, color="#1f77b4", alpha=0.75, label="Revenue (RMB bn)")
ax1.set_ylabel("Revenue (RMB bn)", color="#1f77b4")
ax1.set_ylim(0, 20)
ax1.tick_params(axis="y", labelcolor="#1f77b4")
for i, v in enumerate(revenue):
    ax1.text(i, v + 0.3, f"{v:.2f}", ha="center", fontsize=9, color="#1f77b4")

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color="#d62728", marker="o", linewidth=2, label="Gross margin (%)")
ax2.plot(years, [n / r * 100 for n, r in zip(net_inc, revenue)],
         color="#2ca02c", marker="s", linewidth=2, label="Net margin (%)")
ax2.set_ylabel("Margin (%)", color="black")
ax2.set_ylim(0, 30)
for i, v in enumerate(gross_margin):
    ax2.text(i, v + 0.3, f"{v:.1f}%", ha="center", fontsize=8, color="#d62728")

plt.title("Wolong Electric Drive (SSE:600580) — Revenue & Margins, FY2021–FY2025")
fig.legend(loc="upper left", bbox_to_anchor=(0.13, 0.93))
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/wolong_revenue_margin.png", dpi=150, bbox_inches="tight")
print("saved")
