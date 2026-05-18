"""Dobot peer P/S multiples (TTM, approximate)."""
import matplotlib.pyplot as plt

peers = [
    "Dobot\nHKEX:2432",
    "UBTECH\nHKEX:9880",
    "Estun\nSZSE:002747",
    "Doosan Rob.\nKRX:454910",
    "Teradyne\nNasdaq:TER",
]
ps = [33.0, 80.0, 38.0, 110.0, 4.0]  # rough TTM P/S
colors = ["#2b6cb0", "#9f7aea", "#38a169", "#dd6b20", "#718096"]

fig, ax = plt.subplots(figsize=(8, 4.6))
bars = ax.bar(peers, ps, color=colors, alpha=0.9)
ax.set_ylabel("TTM P/S (×)")
ax.set_title("Cobot / Humanoid Peers — TTM Price/Sales (approx., May 2026)")
for b, v in zip(bars, ps):
    ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}×", ha="center", fontsize=10)
ax.set_ylim(0, max(ps) * 1.18)
ax.axhline(40, color="#a0aec0", linestyle="--", linewidth=1)
ax.text(4.4, 41.5, "Peer median ≈ 40×", color="#4a5568", fontsize=8.5, ha="right")
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/dobot_peer_multiples.png",
            dpi=150, bbox_inches="tight")
