"""Peer P/E comparison."""
import matplotlib.pyplot as plt

peers = ["Wolong\n(600580)", "Inovance\n(300124)", "Regal Rexnord\n(RRX)", "ABB\n(ABBN)", "Nidec\n(6594)", "Siemens\n(SIE)"]
pe = [70.9, 35.4, 49.6, 35.0, 13.7, 24.0]
colors = ["#d62728" if p > 50 else "#1f77b4" if p > 25 else "#2ca02c" for p in pe]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(peers, pe, color=colors)
ax.set_ylabel("TTM P/E (×)")
ax.set_title("Industrial-motor peer set — TTM P/E (as of 2026-05-16)")
ax.axhline(38, color="grey", linestyle="--", linewidth=1, label="Peer median ≈38×")
ax.legend()
for bar, v in zip(bars, pe):
    ax.text(bar.get_x() + bar.get_width()/2, v + 1, f"{v:.1f}×", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/wolong_peer_pe.png", dpi=150, bbox_inches="tight")
print("saved")
