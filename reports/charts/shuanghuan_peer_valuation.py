"""Peer valuation comparison (TTM P/E)."""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STHeiti', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# Peers — TTM P/E (approximate, May 2026 reference)
peers = ["双环传动\n(002472)", "精锻科技\n(300258)", "蓝黛科技\n(002765)", "中马传动\n(002698)", "万里扬\n(002434)", "绿的谐波\n(688017)"]
pe = [28.6, 33.0, 42.0, 55.0, 19.0, 110.0]
colors = ["#1f4e79", "#5b9bd5", "#5b9bd5", "#5b9bd5", "#5b9bd5", "#c0504d"]

fig, ax = plt.subplots(figsize=(9.2, 5.2))
bars = ax.bar(peers, pe, color=colors, alpha=0.85)
for bar, v in zip(bars, pe):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v:.0f}×",
            ha="center", va="bottom", fontsize=10)

ax.axhline(y=37.6, color="#7030a0", linestyle="--", linewidth=1.4, label="同行中位数 ≈ 37.6×")
ax.set_ylabel("TTM P/E (×)")
ax.set_title("双环传动 vs 同业 估值比较 — TTM P/E (参考时点 2026-05)", fontsize=13, pad=10)
ax.set_ylim(0, max(pe) * 1.15)
ax.legend(loc="upper left", fontsize=10)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/shuanghuan_peer_valuation.png",
            dpi=150, bbox_inches="tight")
print("Saved peer PE chart")
