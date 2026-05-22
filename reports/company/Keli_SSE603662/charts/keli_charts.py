"""Charts for Keli Sensing (SSE:603662) research report."""
import matplotlib.pyplot as plt
import numpy as np

OUT = "/Users/x/projects/financial_agent/reports/charts"

# ---------- Chart 1: Revenue & gross margin trend FY2020-FY2025 ----------
years = ["2020", "2021", "2022", "2023", "2024", "2025"]
revenue = [605, 836, 950, 1072, 1295, 1558]   # RMB million
gross_margin = [44.5, 42.7, 41.1, 43.5, 43.13, 44.78]  # %, approx
net_profit = [148, 196, 199, 312, 261, 341]   # RMB million

fig, ax1 = plt.subplots(figsize=(9, 5))
x = np.arange(len(years))
bars = ax1.bar(x - 0.18, revenue, width=0.36, color="#1f4e79", label="Revenue (RMB M)")
bars2 = ax1.bar(x + 0.18, net_profit, width=0.36, color="#8faadc", label="Net profit (RMB M)")
ax1.set_ylabel("RMB millions")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(loc="upper left")
ax1.grid(axis="y", linestyle="--", alpha=0.4)

ax2 = ax1.twinx()
ax2.plot(x, gross_margin, color="#c00000", marker="o", linewidth=2, label="Gross margin (%)")
ax2.set_ylabel("Gross margin (%)")
ax2.set_ylim(35, 50)
ax2.legend(loc="upper right")

plt.title("Keli Sensing (SSE:603662) — Revenue, Net Profit & Gross Margin, FY2020-FY2025")
plt.tight_layout()
plt.savefig(f"{OUT}/keli_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 2: FY2025 revenue mix by product ----------
labels = [
    "Force sensors & instruments\n619.8 M (41.7%)",
    "IIoT & system integration\n588.9 M (39.6%)",
    "Temperature\n92.6 M (6.2%)",
    "Photoelectric (safety light curtain)\n68.5 M (4.6%)",
    "Water quality\n34.5 M (2.3%)",
    "Vibration\n33.0 M (2.2%)",
    "Platform products\n27.2 M (1.8%)",
    "Current/voltage\n23.2 M (1.6%)",
]
sizes = [619.8, 588.9, 92.6, 68.5, 34.5, 33.0, 27.2, 23.2]
colors = ["#1f4e79", "#2e75b6", "#9dc3e6", "#bdd7ee", "#a9d18e", "#c5e0b4", "#e2efda", "#fff2cc"]
fig, ax = plt.subplots(figsize=(9, 6))
wedges, _ = ax.pie(sizes, colors=colors, startangle=90, wedgeprops=dict(edgecolor="white"))
ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=9)
plt.title("Keli Sensing — FY2025 Main Revenue Mix (RMB millions, total 1,487.8 M)")
plt.tight_layout()
plt.savefig(f"{OUT}/keli_product_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 3: Peer multiples ----------
peers = ["Keli\n603662", "Hanwei\n300007", "Honeywell\nHON", "TE Conn.\nTEL", "Sector\nmedian"]
pe = [58.7, 90.5, 34.0, 21.0, 35.0]
ps = [11.2, 6.6, 3.6, 3.2, 5.0]

x = np.arange(len(peers))
fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(x - 0.18, pe, width=0.36, color="#1f4e79", label="TTM P/E (x)")
ax1.bar(x + 0.18, ps, width=0.36, color="#c00000", label="TTM P/S (x)")
ax1.set_xticks(x)
ax1.set_xticklabels(peers)
ax1.set_ylabel("Multiple (x)")
ax1.legend()
ax1.grid(axis="y", linestyle="--", alpha=0.4)
for i, (p, s) in enumerate(zip(pe, ps)):
    ax1.text(i - 0.18, p + 1.5, f"{p:.0f}x", ha="center", fontsize=9)
    ax1.text(i + 0.18, s + 1.5, f"{s:.1f}x", ha="center", fontsize=9)
plt.title("Peer Valuation: Keli vs. Hanwei, Honeywell, TE Connectivity, sector median (TTM)")
plt.tight_layout()
plt.savefig(f"{OUT}/keli_peer_multiples.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 4: TAM ----------
# China smart sensor market, RMB bn
yrs = ["2022", "2023", "2024", "2025E", "2026E", "2027E", "2028E"]
mkt = [108.7, 143.0, 162.85, 185.51, 211.32, 240.0, 273.0]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(yrs, mkt, color="#1f4e79")
for i, v in enumerate(mkt):
    ax.text(i, v + 4, f"{v:.0f}", ha="center", fontsize=9)
ax.set_ylabel("RMB billion")
ax.set_title("China Smart Sensor Market — Size and Outlook (RMB bn)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(f"{OUT}/keli_tam.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 5: Robot force sensor shipments ramp ----------
periods = ["FY2024", "FY2025", "FY2026E\n(monthly run-rate × 12)"]
units = [400, 1500, 12000]
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(periods, units, color=["#9dc3e6", "#2e75b6", "#c00000"])
for b, v in zip(bars, units):
    ax.text(b.get_x() + b.get_width()/2, v + 200, f"{v:,}", ha="center", fontsize=10)
ax.set_ylabel("Units shipped (robotic force sensors)")
ax.set_title("Keli — Robotic Force/Torque Sensor Shipment Ramp")
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(f"{OUT}/keli_robot_ramp.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written to", OUT)
