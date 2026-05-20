"""Humanoid robot global market-size forecast, 2024-2035.

Forecasts vary widely by source; the chart shows the rough consensus of
Goldman Sachs (2024 update), Morgan Stanley Blue Paper, and CITIC Securities
Chinese-market sizing. Numbers are illustrative — see report Section 8 for
the full citation set and caveats.
"""
import matplotlib.pyplot as plt
import numpy as np

years = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030, 2032, 2035])
# Goldman base case (annual shipments value, USD bn)
gs_base = np.array([0.3, 0.7, 1.4, 2.8, 5.0, 8.0, 12.0, 25.0, 38.0])
# Goldman bull case
gs_bull = np.array([0.4, 1.2, 2.5, 5.0, 9.0, 16.0, 25.0, 60.0, 154.0])
# Morgan Stanley (cumulative installed base × ASP proxy, smoothed)
ms = np.array([0.4, 1.0, 2.0, 4.0, 7.5, 13.0, 20.0, 45.0, 110.0])

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, gs_base, marker="o", label="Goldman Sachs base case (2024)", color="#0b5fff", linewidth=2)
ax.plot(years, gs_bull, marker="s", label="Goldman Sachs bull case (2024)", color="#c0392b", linewidth=2, linestyle="--")
ax.plot(years, ms,      marker="^", label="Morgan Stanley Blue Paper (2024)", color="#16a085", linewidth=2)

ax.set_yscale("log")
ax.set_xlabel("Year")
ax.set_ylabel("Annual humanoid robot market (USD billion, log scale)")
ax.set_title("Global Humanoid Robot Market Forecasts, 2024-2035",
             fontsize=13, fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, which="both", alpha=0.3)

fig.text(0.5, -0.03,
         "Sources: Goldman Sachs Research 'Humanoid Robots' updated forecast (2024), "
         "Morgan Stanley 'Humanoid 100' Blue Paper (2024-02), CITIC Securities China humanoid "
         "outlook (2025). Forecasts are illustrative and have wide uncertainty bands.",
         ha="center", fontsize=8, style="italic")

plt.tight_layout()
plt.savefig("/Users/x/projects/financial_agent/reports/charts/leju_tam_growth.png",
            dpi=150, bbox_inches="tight")
print("saved")
