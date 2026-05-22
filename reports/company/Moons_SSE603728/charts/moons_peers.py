"""Moons' Electric vs peer TTM P/E and P/S bar chart."""
import matplotlib.pyplot as plt
import numpy as np
import os

# Peers: Moons (603728), Leadshine 雷赛智能 (002979), Inovance 汇川技术 (300124),
# Lvde Harmonic 绿的谐波 (688017), Allied Motion / Allient (AMOT US)
# Values are author estimates from public market data sources (Eastmoney/Sina,
# Stockanalysis.com) as of mid-May 2026. AMOT is private-equity-acquired in 2024
# but legacy 2023 TTM multiples shown for reference.
peers = [
    "Moons'\n603728",
    "Leadshine\n002979",
    "Inovance\n300124",
    "Lvde Harmonic\n688017",
    "Allient (AMOT)\nUS pre-buyout",
]
pe_ttm = [445, 95, 38, 250, 22]
ps_ttm = [9.9, 11.5, 6.3, 38, 1.3]

x = np.arange(len(peers))
width = 0.38

fig, ax1 = plt.subplots(figsize=(11, 5.5))
b1 = ax1.bar(x - width / 2, pe_ttm, width, color="#1f77b4", label="TTM P/E (×)")
ax1.set_ylabel("TTM P/E (×)", color="#1f77b4")
ax1.set_yscale("log")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
ax1.set_ylim(5, 600)

for xi, v in zip(x, pe_ttm):
    ax1.text(xi - width / 2, v * 1.06, f"{v}", ha="center", fontsize=9, color="#1f77b4")

ax2 = ax1.twinx()
b2 = ax2.bar(x + width / 2, ps_ttm, width, color="#d62728", label="TTM P/S (×)")
ax2.set_ylabel("TTM P/S (×)", color="#d62728")
ax2.set_ylim(0, 45)
for xi, v in zip(x, ps_ttm):
    ax2.text(xi + width / 2, v + 0.6, f"{v:.1f}", ha="center", fontsize=9, color="#d62728")

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.title("Motion-control peer group — TTM P/E and P/S (mid-May 2026, log scale on P/E)")
plt.tight_layout()
out = os.path.join(os.path.dirname(__file__), "moons_peers.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out)
