"""Sanhua and peer TTM P/E bars."""
import matplotlib.pyplot as plt
import os

# Ordered: Sanhua, Tuopu, Dunan, Yinlun, Modine, Valeo
labels = ["Sanhua\n002050", "Tuopu\n601689", "Dunan\n002011",
          "Yinlun\n002126", "Modine\nMOD", "Valeo\nFR.PA"]
pe = [46.0, 49.0, 28.0, 24.0, 48.9, 8.5]
colors = ["#c0392b", "#e67e22", "#2980b9", "#2980b9", "#7f8c8d", "#7f8c8d"]

fig, ax = plt.subplots(figsize=(9.5, 5))
bars = ax.bar(labels, pe, color=colors, alpha=0.9)
for b, v in zip(bars, pe):
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.0f}×",
            ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("TTM P/E (×)", fontsize=11)
ax.set_ylim(0, max(pe) * 1.18)
ax.set_title("Sanhua vs. thermal-management peers — TTM P/E (May 2026)",
             fontsize=12.5, pad=12)
ax.axhline(y=30, color="grey", linestyle="--", linewidth=0.8, alpha=0.6)
ax.text(5.3, 31, "≈ sector median 30×", fontsize=9, color="grey")
plt.xticks(fontsize=10)
fig.tight_layout()
path = os.path.join(os.path.dirname(__file__), "sanhua_peer_pe.png")
plt.savefig(path, dpi=150, bbox_inches="tight")
print(path)
