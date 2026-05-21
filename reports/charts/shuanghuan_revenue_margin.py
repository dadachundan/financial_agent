"""Shuanghuan revenue + net margin trend (FY2022-FY2025) + 2026Q1."""
import matplotlib.pyplot as plt
import matplotlib

# Configure for Chinese fonts
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STHeiti', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

years = ["2022", "2023", "2024", "2025"]
revenue_bn = [68.38 / 10, 80.74 / 10, 87.81 / 10, 91.12 / 10]  # RMB bn (报告中是亿元 -> bn)
# Net profit (attributable, RMB bn)
np_bn = [5.821 / 10, 8.164 / 10, 10.239 / 10, 12.615 / 10]  # 亿元 -> bn
net_margin = [np_bn[i] / revenue_bn[i] * 100 for i in range(len(years))]

fig, ax1 = plt.subplots(figsize=(9, 5.2))
color1 = "#1f4e79"
color2 = "#c0504d"

bars = ax1.bar(years, revenue_bn, color=color1, alpha=0.82, label="营业收入 (RMB bn)", width=0.55)
ax1.set_xlabel("Fiscal Year")
ax1.set_ylabel("营业收入 (RMB bn)", color=color1)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, max(revenue_bn) * 1.25)

for bar, v in zip(bars, revenue_bn):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 0.18, f"{v:.2f}",
             ha="center", va="bottom", fontsize=9, color=color1)

ax2 = ax1.twinx()
ax2.plot(years, net_margin, color=color2, marker="o", linewidth=2.4, label="归母净利率 (%)")
ax2.set_ylabel("归母净利率 (%)", color=color2)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(min(net_margin) - 2, max(net_margin) + 3)
for x, y in zip(years, net_margin):
    ax2.text(x, y + 0.35, f"{y:.1f}%", color=color2, ha="center", fontsize=9)

plt.title("双环传动 (002472) 营收与归母净利率 — FY2022-FY2025", fontsize=13, pad=12)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/shuanghuan_revenue_margin.png",
            dpi=150, bbox_inches="tight")
print("Saved revenue/margin chart")
