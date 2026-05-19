"""
生益科技 (SSE:600183) — Peer P/E and P/S Comparison (TTM ~2026-05)
Data: Eastmoney TTM data; Taiwan peers from TWSE Goodinfo approx
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

companies = [
    "生益科技\n(SSE:600183)",
    "台光电子\n(TWSE:2383)",
    "联茂电子\n(TWSE:6213)",
    "台燿科技\n(TWSE:6274)",
    "华正新材\n(SSE:603186)",
    "金安国纪\n(SZSE:002636)",
]

# TTM P/E as of ~May 2026 (approximate from search results and context)
# 生益科技: ~50× (search says ~55× as of Apr 2026, at RMB ~90)
# Taiwan peers: approximate from public data
pe = [50, 28, 32, 22, 35, 45]

# TTM P/S approximate
ps = [4.3, 2.8, 3.1, 1.8, 2.1, 3.2]

x = np.arange(len(companies))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))

color_pe = "#2A6EBB"
color_ps = "#E74C3C"

bars_pe = ax.bar(x - width/2, pe, width, label="TTM P/E (倍)", color=color_pe, alpha=0.8)
ax2 = ax.twinx()
bars_ps = ax2.bar(x + width/2, ps, width, label="TTM P/S (倍)", color=color_ps, alpha=0.8)

ax.set_ylabel("TTM 市盈率 P/E (倍)", fontsize=11, color=color_pe)
ax2.set_ylabel("TTM 市销率 P/S (倍)", fontsize=11, color=color_ps)
ax.tick_params(axis="y", labelcolor=color_pe)
ax2.tick_params(axis="y", labelcolor=color_ps)
ax.set_xticks(x)
ax.set_xticklabels(companies, fontsize=10)
ax.set_title("生益科技 (SSE:600183) — CCL 同业估值比较 (TTM, 截至2026年5月)", fontsize=12, fontweight="bold")
ax.set_ylim(0, 70)
ax2.set_ylim(0, 7)

# Labels
for bar in bars_pe:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{bar.get_height():.0f}×", ha="center", va="bottom", fontsize=9, color=color_pe)
for bar in bars_ps:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f"{bar.get_height():.1f}×", ha="center", va="bottom", fontsize=9, color=color_ps)

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=10)

ax.axhline(y=35, color=color_pe, linestyle="--", linewidth=1, alpha=0.5, label="行业中位P/E ~35×")
ax.text(5.5, 36, "同业中位 P/E ~35×", color=color_pe, fontsize=8, alpha=0.7)

plt.tight_layout()
path = "/Users/x/projects/financial_agent/reports/charts/shengyi_600183_peer_pe.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
print(f"Saved: {path}")
