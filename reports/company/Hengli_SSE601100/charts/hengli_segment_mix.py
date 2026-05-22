"""Hengli segment revenue mix FY2025."""
import matplotlib.pyplot as plt

segments = ["Hydraulic cylinders", "Hydraulic pumps/valves/motors", "Components & castings (incl. screws & rails)", "Hydraulic systems"]
revenue = [5.254, 4.326, 0.891, 0.385]    # RMB bn FY2025

fig, ax = plt.subplots(figsize=(8, 4.6))
colors = ["#1f4e79", "#4a7bb7", "#76a4d1", "#b6cce0"]
wedges, texts, autotexts = ax.pie(revenue, labels=segments, autopct=lambda p: f"{p:.1f}%\n({p*sum(revenue)/100:.2f}bn)",
                                   colors=colors, startangle=90, textprops={"fontsize": 10})
ax.set_title("Hengli Hydraulics — FY2025 revenue mix (RMB 10.86bn main business)", fontsize=12)
plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/hengli_segment_mix.png", dpi=150, bbox_inches="tight")
print("saved")
