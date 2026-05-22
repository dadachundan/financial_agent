#!/usr/bin/env python3
"""Peer TTM P/E bar chart for Shuanglin Co. (300100)."""
import matplotlib.pyplot as plt
import os

names = [
    "NSK\n(TYO:6471)",
    "Tuopu\n(SSE:601689)",
    "Shuanghuan\n(SZSE:002472)",
    "Hengli\n(SSE:601100)",
    "Shuanglin\n(SZSE:300100)",
    "XCC\n(SSE:603667)",
    "ZDLD\n(SZSE:002896)",
]
# TTM P/E (rough, May 2026 snapshot from Eastmoney / Yahoo / Lixinger)
pe = [16.7, 24.0, 28.5, 45.0, 47.4, 90.0, 189.0]
colors = ["#999", "#999", "#999", "#999", "#cc0000", "#999", "#999"]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(names, pe, color=colors)
for b, v in zip(bars, pe):
    ax.text(b.get_x() + b.get_width() / 2, v + 3, f"{v:.0f}x", ha="center", fontsize=10)
ax.set_ylabel("TTM P/E (×)")
ax.set_title("Humanoid-Robot Supply Chain Peer P/E — Shuanglin in Context (May 2026)")
ax.axhline(28.5, color="#999", linestyle="--", linewidth=0.8, alpha=0.5)
ax.text(6.4, 30, "Auto-parts median ~28x", color="#666", fontsize=8, ha="right")
ax.set_ylim(0, 220)

out = os.path.join(os.path.dirname(__file__), "shuanglin_peer_pe.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print(out)
