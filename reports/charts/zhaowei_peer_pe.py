"""Peer P/E TTM comparison."""
import matplotlib.pyplot as plt

names = [
    "Zhaowei\n003021",
    "Zhongdadi\n002896",
    "Topband\n002139",
    "Shuanglin\n300100",
    "Sector\nmedian (~30x)",
]
pe = [111.5, 281.0, 62.8, 44.3, 30.0]
colors = ["#c0392b", "#7f8c8d", "#7f8c8d", "#7f8c8d", "#2c3e50"]

fig, ax = plt.subplots(figsize=(8.5, 4.8))
bars = ax.bar(names, pe, color=colors, alpha=0.9)
for b, v in zip(bars, pe):
    ax.annotate(f"{v:.0f}x", (b.get_x() + b.get_width() / 2, v),
                textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("TTM P/E ratio (x)")
ax.set_title("Zhaowei vs. domestic micro-transmission peers — TTM P/E (2026-05-15)")
ax.axhline(30, color="#2c3e50", linewidth=0.7, linestyle=":", alpha=0.6)
ax.set_ylim(0, 320)

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/zhaowei_peer_pe.png",
            dpi=150, bbox_inches="tight")
print("saved zhaowei_peer_pe.png")
