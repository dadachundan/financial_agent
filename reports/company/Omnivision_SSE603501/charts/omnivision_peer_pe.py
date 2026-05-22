"""OmniVision vs CIS peers — TTM P/E and P/S."""
import matplotlib.pyplot as plt
import numpy as np

names = ["OmniVision\n603501", "SmartSens\n688213", "GalaxyCore\n688728",
         "ON Semi\nON", "Sony\n6758", "Hesai\nHSAI"]
pe   = [30.9, 38.8, 57.9, 290.7, 18.5, 45.0]    # TTM P/E
ps   = [4.3, 7.6, 6.6, 5.5, 1.5, 4.2]           # TTM P/S
sector_median_pe = 38.0
sector_median_ps = 4.8

x = np.arange(len(names))
width = 0.4

fig, ax1 = plt.subplots(figsize=(11, 5.5))
b1 = ax1.bar(x - width/2, pe, width, label="TTM P/E (x)", color="#4C72B0")
ax1.set_ylabel("TTM P/E (x)", color="#4C72B0", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#4C72B0")
ax1.axhline(sector_median_pe, color="#4C72B0", linestyle="--", alpha=0.5,
            label=f"P/E median {sector_median_pe:.0f}x")
ax1.set_ylim(0, 320)
for bar, v in zip(b1, pe):
    ax1.text(bar.get_x() + bar.get_width()/2, v + 4, f"{v:.1f}",
             ha="center", va="bottom", fontsize=8, color="#4C72B0")

ax2 = ax1.twinx()
b2 = ax2.bar(x + width/2, ps, width, label="TTM P/S (x)", color="#DD8452")
ax2.set_ylabel("TTM P/S (x)", color="#DD8452", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#DD8452")
ax2.axhline(sector_median_ps, color="#DD8452", linestyle="--", alpha=0.5,
            label=f"P/S median {sector_median_ps:.1f}x")
ax2.set_ylim(0, 9)
for bar, v in zip(b2, ps):
    ax2.text(bar.get_x() + bar.get_width()/2, v + 0.1, f"{v:.1f}",
             ha="center", va="bottom", fontsize=8, color="#DD8452")

ax1.set_xticks(x)
ax1.set_xticklabels(names, fontsize=9)
ax1.set_title("CIS / image-sensor peers — TTM P/E and P/S (May 2026)",
              fontsize=12)
ax1.grid(axis="y", linestyle=":", alpha=0.3)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/omnivision_peer_pe.png",
            dpi=150, bbox_inches="tight")
print("saved")
