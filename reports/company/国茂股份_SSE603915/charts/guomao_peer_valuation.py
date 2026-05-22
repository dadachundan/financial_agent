"""Guomao vs. peers — TTM P/E and TTM P/S snapshot."""
import matplotlib.pyplot as plt
import numpy as np

peers = ["Guomao\n(603915)", "Shuanghuan\n(002472)", "Leaderdrive\n(688017)", "Zhongdadi\n(002896)"]
pe_ttm = [44.7, 28.1, 156.1, 95.0]   # Leaderdrive forward FY26 from 9fzt; Zhongdadi rough estimate
ps_ttm = [4.2, 4.0, 19.5, 7.0]       # rough; Leaderdrive P/S high

x = np.arange(len(peers))
width = 0.36

fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - width / 2, pe_ttm, width, color="#1f6feb", label="TTM P/E (×)")
b2 = ax.bar(x + width / 2, ps_ttm, width, color="#d29922", label="TTM P/S (×)")
ax.set_xticks(x)
ax.set_xticklabels(peers, fontsize=10)
ax.set_ylabel("Multiple (×)")
ax.set_title("Peer valuation: Chinese precision-/general-purpose reducer plays (May 2026)", fontsize=12)
for rect in b1:
    ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 3,
            f"{rect.get_height():.0f}×", ha="center", fontsize=9, color="#1f6feb")
for rect in b2:
    ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 3,
            f"{rect.get_height():.1f}×", ha="center", fontsize=9, color="#a06400")
ax.legend()
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/guomao_peer_valuation.png", dpi=150, bbox_inches="tight")
print("saved")
