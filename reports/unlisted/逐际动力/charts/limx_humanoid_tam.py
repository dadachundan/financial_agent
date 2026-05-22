"""Global humanoid robot market — annual shipments forecast."""
import matplotlib.pyplot as plt

# Year, base/low-case shipments (units), bull-case shipments (units)
# Sources: Goldman Sachs (2024 upgrade), Morgan Stanley humanoid 2050 outlook,
# Xinhua / China gov (2025 actual range 13-16k), industry press triangulation.
years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
base  = [4,    14,   60,   180,  450,   900,  1500]   # k units
bull  = [4,    16,   90,   300,  800,  1800,  3500]

fig, ax = plt.subplots(figsize=(10, 5.5))
w = 0.35
xs = list(range(len(years)))
b1 = ax.bar([x - w/2 for x in xs], base, w, color="#888", label="Base case (k units)")
b2 = ax.bar([x + w/2 for x in xs], bull, w, color="#d6336c", label="Bull case (k units)")

for bar in list(b1) + list(b2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f"{int(bar.get_height())}", ha="center", fontsize=8)

ax.set_xticks(xs)
ax.set_xticklabels(years)
ax.set_ylabel("Annual humanoid robot shipments (thousands)")
ax.set_title("Global Humanoid Robot Shipment Forecast 2024–2030 (Base vs. Bull)",
             fontsize=13, fontweight="bold")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)

fig.text(0.5, -0.02,
         "Sources: Goldman Sachs 2024 humanoid market update; Morgan Stanley 2025 humanoid outlook; "
         "Xinhua 2025 China humanoid YE recap (~13–16k units shipped globally, ~90% from China).",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/limx_humanoid_tam.png",
            dpi=150, bbox_inches="tight")
print("saved")
