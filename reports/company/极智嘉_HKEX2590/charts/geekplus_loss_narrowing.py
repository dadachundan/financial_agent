"""极智嘉净亏损与经调整净亏损率收窄."""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

years = ["2022", "2023", "2024", "2025H1"]
net_loss = [-15.67, -11.27, -8.32, -0.48]  # 亿元，来源招股书 + 中期报告
adj_loss_pct = [-37.0, -16.0, -3.8, -1.2]  # 经调整净亏损率%，来源招股书/财报口径

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, net_loss, color="#d9531e", alpha=0.85, label="净亏损（亿元）")
ax1.set_ylabel("净亏损（亿元人民币）", color="#d9531e")
ax1.tick_params(axis="y", labelcolor="#d9531e")
ax1.set_ylim(-18, 1)
ax1.axhline(0, color="black", linewidth=0.5)

for bar, v in zip(bars, net_loss):
    ax1.text(bar.get_x() + bar.get_width() / 2, v - 0.7, f"{v:.2f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, adj_loss_pct, color="#3b6fb5", marker="o", linewidth=2, label="经调整净亏损率（%）")
ax2.set_ylabel("经调整净亏损率（%）", color="#3b6fb5")
ax2.tick_params(axis="y", labelcolor="#3b6fb5")
ax2.set_ylim(-40, 5)
ax2.axhline(0, color="#3b6fb5", linewidth=0.4, linestyle=":")
for x, m in zip(years, adj_loss_pct):
    ax2.text(x, m + 1, f"{m:.1f}%", ha="center", fontsize=9, color="#3b6fb5")

plt.title("极智嘉净亏损与经调整净亏损率收窄轨迹")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/geekplus_loss_narrowing.png", dpi=150, bbox_inches="tight")
print("done")
