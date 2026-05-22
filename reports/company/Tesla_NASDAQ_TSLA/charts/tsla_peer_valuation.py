#!/usr/bin/env python3
"""Peer TTM P/E and P/S comparison: TSLA vs. BYD / GM / Ford / NIO / XPEV / LI.
Sources: GuruFocus / financecharts.com / companiesmarketcap.com for each
ticker as of ~May 2026; see report References block for the per-ticker links."""
import matplotlib.pyplot as plt
import numpy as np

tickers = ["TSLA", "Li Auto", "BYD", "GM", "XPEV", "NIO", "Ford"]
# P/E TTM; NIO and XPEV are loss-making so we show N/M (set as 0 / shaded)
pe = [393.4, 112.1, 30.4, 27.6, np.nan, np.nan, 11.1]
ps = [16.0,  3.2,   1.2,  0.78, 1.5,    1.2,  0.30]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# P/E
ax = axes[0]
vals = [v if not np.isnan(v) else 0 for v in pe]
bars = ax.bar(tickers, vals, color=["#cc0000"] + ["#888"] * 6)
for i, (t, v) in enumerate(zip(tickers, pe)):
    if np.isnan(v):
        ax.text(i, 5, "N/M\n(losses)", ha="center", fontsize=9, color="#a00")
    else:
        ax.text(i, v + 8, f"{v:.0f}×", ha="center", fontsize=9)
ax.set_title("TTM P/E (May 2026, GuruFocus / financecharts.com)", fontweight="bold")
ax.set_ylabel("P/E (×)")
ax.set_ylim(0, 450)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# P/S
ax = axes[1]
bars = ax.bar(tickers, ps, color=["#cc0000"] + ["#888"] * 6)
for i, v in enumerate(ps):
    ax.text(i, v + 0.3, f"{v:.2f}×", ha="center", fontsize=9)
ax.set_title("TTM P/S (May 2026)", fontweight="bold")
ax.set_ylabel("P/S (×)")
ax.set_ylim(0, 19)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.suptitle("Tesla vs. Auto Peers — Valuation, May 2026", fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/tsla_peer_valuation.png",
            dpi=150, bbox_inches="tight")
print("saved")
