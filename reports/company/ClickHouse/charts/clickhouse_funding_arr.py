"""Generate ClickHouse funding rounds + ARR growth chart.

ClickHouse funding history (verified from press releases & filings):
- Sep 2021: Series A $50M (Index Ventures + Benchmark)
- Oct 2021: Series B $250M @ $2B post-money (Coatue + Altimeter led)
- May 2025: Series C $350M @ $6.35B post-money (Khosla led)
- Oct 2025: Series C extension (undisclosed amount) — Citi, Insight, Peak XV
- Jan 2026: Series D $400M @ $15B post-money (Dragoneer led)
- $100M credit facility (Stifel, Goldman Sachs) alongside Series C

ARR trajectory (verified from press / interviews):
- May 2025: Approaching $100M ARR run-rate (Series C announcement)
- Oct 2025: ARR more than quadrupled YoY (Series C extension)
- May 2026: $250M ARR (3x YoY), 4,000+ customers (Open House 2026)
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

# --- Left: Cumulative equity raised + post-money valuation ---
rounds = [
    ("Series A\nSep '21", 50, 0.30),
    ("Series B\nOct '21", 300, 2.0),
    ("Series C\nMay '25", 650, 6.35),
    ("Series D\nJan '26", 1050, 15.0),
]
labels = [r[0] for r in rounds]
cum_raised = [r[1] for r in rounds]
valuations = [r[2] for r in rounds]

x = list(range(len(rounds)))
ax1.bar(x, cum_raised, color="#4A90E2", alpha=0.85, width=0.55, label="Cumulative equity raised ($M)")
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=9)
ax1.set_ylabel("Cumulative equity raised (USD M)", color="#4A90E2", fontsize=10)
ax1.tick_params(axis="y", labelcolor="#4A90E2")
ax1.set_ylim(0, 1300)
for xi, val in zip(x, cum_raised):
    ax1.text(xi, val + 25, f"${val:,}M", ha="center", fontsize=9, color="#1F4E8C", fontweight="bold")

ax1b = ax1.twinx()
ax1b.plot(x, valuations, color="#D9534F", marker="o", linewidth=2.4, markersize=9, label="Post-money valuation ($B)")
ax1b.set_ylabel("Post-money valuation (USD B)", color="#D9534F", fontsize=10)
ax1b.tick_params(axis="y", labelcolor="#D9534F")
ax1b.set_ylim(0, 18)
for xi, val in zip(x, valuations):
    ax1b.text(xi, val + 0.6, f"${val:g}B", ha="center", fontsize=9, color="#8B2E2A", fontweight="bold")

ax1.set_title("ClickHouse Inc. — funding history (2021-2026)", fontsize=11, fontweight="bold")
ax1.grid(axis="y", alpha=0.25)

# --- Right: ARR + customer growth ---
arr_dates = ["May '25\nSeries C", "Oct '25\nSer.C ext.", "May '26\nOpen House"]
arr_values = [100, 175, 250]  # in $M; Oct '25 is the analyst interpolation (ARR > 4x YoY)
customers = [2000, 2500, 4000]

x2 = list(range(len(arr_dates)))
ax2.bar(x2, arr_values, color="#5CB85C", alpha=0.85, width=0.55, label="ARR ($M, run-rate)")
ax2.set_xticks(x2)
ax2.set_xticklabels(arr_dates, fontsize=9)
ax2.set_ylabel("ARR ($M, run-rate)", color="#3B8C3B", fontsize=10)
ax2.tick_params(axis="y", labelcolor="#3B8C3B")
ax2.set_ylim(0, 320)
for xi, val in zip(x2, arr_values):
    ax2.text(xi, val + 6, f"${val}M", ha="center", fontsize=9, color="#1F4E1F", fontweight="bold")

ax2b = ax2.twinx()
ax2b.plot(x2, customers, color="#9B59B6", marker="s", linewidth=2.4, markersize=9, label="Cloud customers")
ax2b.set_ylabel("Cloud customers (#)", color="#5E2D7C", fontsize=10)
ax2b.tick_params(axis="y", labelcolor="#5E2D7C")
ax2b.set_ylim(0, 5000)
ax2b.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
for xi, val in zip(x2, customers):
    ax2b.text(xi, val + 100, f"{val:,}", ha="center", fontsize=9, color="#3B1F50", fontweight="bold")

ax2.set_title("ClickHouse — ARR & customer growth (2025-2026)", fontsize=11, fontweight="bold")
ax2.grid(axis="y", alpha=0.25)

plt.suptitle("ClickHouse: from $50M Series A (Sep '21) to $15B valuation (Jan '26)", fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()

out = Path(__file__).parent / "clickhouse_funding_arr.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved: {out}")
