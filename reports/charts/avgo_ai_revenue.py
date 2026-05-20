"""AVGO AI semiconductor revenue trajectory — annual (FY23-FY25) + quarterly Q1/Q2 FY26.
Sources:
- FY24 AI = $12.2B (Q4 FY24 press release, 2024-12-12; AI grew 220% YoY).
- FY23 implied ~$3.8B (mgmt: 220% growth into $12.2B).
- FY25 AI ~$19.5B (sum of disclosed quarterly: Q4 FY25 AI grew 74% YoY → ~$5.5-6B; Q1 FY26 $8.4B was 106% YoY → Q1 FY25 ~$4.1B; per Hock Tan Q4 FY25 call). Conservatively show only disclosed checkpoints.
- Q1 FY26 AI = $8.4B (+106% YoY); Q2 FY26 guide AI = $10.7B (8-K, 2026-03-04).
"""
import matplotlib.pyplot as plt

labels = ["FY23\n(implied)", "FY24\nactual", "FY25\n(approx)", "Q1 FY26", "Q2 FY26\nguide"]
values = [3.8, 12.2, 19.5, 8.4, 10.7]
colors = ["#9ecae1", "#6baed6", "#3182bd", "#08519c", "#bdd7e7"]
annot = ["~$3.8B", "$12.2B", "~$19.5B", "$8.4B", "$10.7B"]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(labels, values, color=colors)
for b, t in zip(bars, annot):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.3, t, ha="center", fontsize=10)
ax.set_ylabel("AI semiconductor revenue (USD B)")
ax.set_title("Broadcom — AI semiconductor revenue trajectory")
ax.set_ylim(0, 22)
fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/avgo_ai_revenue.png", dpi=150, bbox_inches="tight")
print("saved")
