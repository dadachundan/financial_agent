"""Peer P/E comparison for Hengli vs hydraulics + humanoid-actuator peers."""
import matplotlib.pyplot as plt

peers = [
    "Hengli\n601100",
    "Yantai Eddie\n603638",
    "Parker\nHannifin PH",
    "Eaton\nETN",
    "Tuopu\n601689",
    "Shuanglin\n300100",
    "Schaeffler\nETR:SHA",
    "Sector\nMedian"
]
pe_ttm = [55, 50, 32.6, 39.3, 78, 95, 12, 35]
colors = ["#1f4e79"] + ["#7f8fa6"] * 6 + ["#c0504d"]

fig, ax = plt.subplots(figsize=(9, 4.6))
bars = ax.bar(peers, pe_ttm, color=colors, alpha=0.9)
ax.set_ylabel("TTM P/E (×)")
ax.set_title("Peer TTM P/E — Hengli vs. global hydraulics + humanoid-actuator comps (May 2026)", fontsize=11)
for bar, v in zip(bars, pe_ttm):
    ax.text(bar.get_x() + bar.get_width()/2, v + 1.5, f"{v}×", ha="center", fontsize=9)
ax.set_ylim(0, 110)
ax.axhline(35, color="#c0504d", linestyle="--", linewidth=1, alpha=0.7)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/hengli_peer_multiples.png", dpi=150, bbox_inches="tight")
print("saved")
