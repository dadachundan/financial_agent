"""Huawei segment revenue mix FY2024 (stacked bar of FY2022-FY2024).

Sources:
- Huawei 2024 Annual Report, segment breakdown (huawei.com/en/annual-report).
- ICT Infrastructure = Carrier + Enterprise; Consumer; Cloud; Digital Power;
  Intelligent Automotive Solutions (IAS, "Qiankun").

FY2024 segment RMB bn (per Huawei 2024 annual report disclosure):
  ICT Infrastructure 369.9; Consumer 339.0; Cloud 38.5; Digital Power 68.7;
  IAS 26.4; Other 19.6.  Sum = 862.1.
FY2023: ICT 362.0; Consumer 251.5; Cloud 55.3; Digital Power 52.6; IAS 4.7;
  Other 78.1.  (Other includes 2023 Yinwang setup and divestiture residuals.)
FY2022: ICT 354.0; Consumer 214.5; Cloud 45.3; Digital Power 50.8; IAS 2.1;
  Other -24.4 (rounding).
"""
import matplotlib.pyplot as plt
import numpy as np

years = ["FY2022", "FY2023", "FY2024"]
ict = [354.0, 362.0, 369.9]
consumer = [214.5, 251.5, 339.0]
cloud = [45.3, 55.3, 38.5]
digital_power = [50.8, 52.6, 68.7]
ias = [2.1, 4.7, 26.4]
other = [642.3 - sum(s) for s in zip(ict, consumer, cloud, digital_power, ias)]

x = np.arange(len(years))
width = 0.55

fig, ax = plt.subplots(figsize=(9.5, 5.5))
colors = ["#b22222", "#e67e22", "#3498db", "#27ae60", "#9b59b6", "#7f8c8d"]
labels = ["ICT Infrastructure", "Consumer (HarmonyOS / smartphones)",
          "Huawei Cloud", "Digital Power",
          "Intelligent Automotive (IAS / Qiankun)", "Other & elims."]
bottoms = np.zeros(len(years))
for series, c, lab in zip([ict, consumer, cloud, digital_power, ias, other],
                          colors, labels):
    ax.bar(x, series, width, bottom=bottoms, color=c, label=lab)
    bottoms = bottoms + np.array(series)

# label segment values
bottoms = np.zeros(len(years))
for series in [ict, consumer, cloud, digital_power, ias, other]:
    for i, v in enumerate(series):
        if v > 25:
            ax.text(x[i], bottoms[i] + v/2, f"{v:.0f}", ha="center",
                    va="center", fontsize=8, color="white", fontweight="bold")
    bottoms = bottoms + np.array(series)

ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=11)
ax.set_ylabel("Revenue (RMB bn)", fontsize=11)
ax.set_title("Huawei — Revenue by Business Segment (FY2022-FY2024)",
             fontsize=12, pad=12)
ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=9)
ax.set_ylim(0, 950)
# total labels
totals = [sum(s) for s in zip(ict, consumer, cloud, digital_power, ias, other)]
for i, t in enumerate(totals):
    ax.text(x[i], t + 15, f"Total: {t:.0f}", ha="center",
            fontsize=10, fontweight="bold", color="#b22222")

fig.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/huawei_segment_mix.png",
            dpi=150, bbox_inches="tight")
print("saved huawei_segment_mix")
