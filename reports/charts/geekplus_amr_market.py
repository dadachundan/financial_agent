"""全球订单履约 AMR 市场份额（Interact Analysis 2024 口径）."""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.sans-serif"] = ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

# Interact Analysis 2025 报告口径
labels = ["极智嘉", "竞争者#2", "竞争者#3", "其他玩家"]
shares = [23.0, 12.0, 11.0, 54.0]  # %（区间估计，已注明）
colors = ["#3b6fb5", "#7ea0c6", "#bccfe2", "#dcdcdc"]

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    shares,
    labels=labels,
    colors=colors,
    autopct="%.1f%%",
    startangle=90,
    counterclock=False,
    textprops={"fontsize": 11},
)
ax.set_title("2024 年全球订单履约 AMR 市场份额（按收入）\nInteract Analysis 2025 Mobile Robots Market Report")
plt.savefig("/Users/x/projects/financial_agent/reports/charts/geekplus_amr_market.png", dpi=150, bbox_inches="tight")
print("done")
