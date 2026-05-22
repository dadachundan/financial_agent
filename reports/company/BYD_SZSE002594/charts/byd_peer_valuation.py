"""BYD peer valuation P/E + P/S comparison."""
import matplotlib.pyplot as plt
import numpy as np

# Approximate TTM (May 2026); see report text for citations
peers = ["BYD\n(002594)", "Tesla\n(TSLA)", "Li Auto\n(LI)", "Xpeng\n(XPEV)", "NIO\n(NIO)",
         "Geely\n(0175.HK)", "Great Wall\n(601633)", "SAIC\n(600104)"]
pe = [29.4, 317.2, 13.5, 80.0, -3.5, 15.5, 17.0, 28.0]
ps = [1.3, 9.5, 1.1, 1.6, 1.2, 0.9, 0.95, 0.5]
# negative P/E plotted as 0 with annotation
pe_plot = [max(p, 0) for p in pe]

x = np.arange(len(peers))
w = 0.38

fig, ax = plt.subplots(figsize=(11, 5.5))
b1 = ax.bar(x - w/2, pe_plot, w, label="TTM P/E (×)", color="#1f4e79")
b2 = ax.bar(x + w/2, ps, w, label="TTM P/S (×)", color="#c0392b")

ax.set_xticks(x)
ax.set_xticklabels(peers, fontsize=9)
ax.set_ylabel("Multiple (×)", fontsize=11)
ax.set_title("Peer valuation snapshot — TTM P/E and P/S (May 2026)", fontsize=12, pad=10)
ax.legend(loc="upper right")
ax.set_ylim(0, 360)
ax.grid(axis="y", linestyle=":", alpha=0.5)

for i, (pep, pev, psv) in enumerate(zip(pe_plot, pe, ps)):
    if pev < 0:
        ax.text(i - w/2, 5, "neg.", ha="center", fontsize=8, color="white")
    else:
        ax.text(i - w/2, pep + 5, f"{pev:.1f}", ha="center", fontsize=8)
    ax.text(i + w/2, psv + 5, f"{psv:.1f}", ha="center", fontsize=8)

fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/byd_peer_valuation.png",
            dpi=150, bbox_inches="tight")
print("saved peer_valuation")
