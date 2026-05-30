"""Generate ClickHouse TAM chart.

Market sizing sources (verified):
- Real-time OLAP database market: $4.2B in 2024 → $24.7B by 2033 (20.1% CAGR)
  per Growth Market Reports
- Columnar OLAP database market: $5.9B in 2024 → $18.4B by 2033 (13.7% CAGR)
  per Growth Market Reports
- DBMS market overall: $98.6B in 2025 → $275B by 2035 (10.8% CAGR)
  per Expert Market Research / Zion
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

fig, ax = plt.subplots(figsize=(10.5, 5.5))

years = np.arange(2024, 2034)

# Real-time OLAP: $4.2B (2024) → $24.7B (2033) at 20.1% CAGR
rt_olap_2024 = 4.2
rt_olap = [rt_olap_2024 * (1.201 ** (y - 2024)) for y in years]

# Columnar OLAP: $5.9B → $18.4B at 13.7% CAGR
col_olap_2024 = 5.9
col_olap = [col_olap_2024 * (1.137 ** (y - 2024)) for y in years]

# Overall DBMS market (large): $98.6B (2025) → $275B (2035)
# CAGR 10.8%, interpolate from 2024
dbms_2025 = 98.6
dbms = [dbms_2025 * (1.108 ** (y - 2025)) for y in years]

ax.fill_between(years, 0, rt_olap, color="#D9534F", alpha=0.7, label="Real-time OLAP databases (SAM) — 20% CAGR")
ax.fill_between(years, rt_olap, col_olap, color="#F0AD4E", alpha=0.6, label="Columnar OLAP databases (broader SAM) — 14% CAGR")
ax.plot(years, dbms, color="#4A90E2", linewidth=2.6, linestyle="--", label="Overall DBMS market (TAM ceiling) — 11% CAGR")

# Annotate key points
ax.annotate(f"${rt_olap[0]:.1f}B\n(2024)", xy=(2024, rt_olap[0]), xytext=(2024.3, 7), fontsize=9, color="#8B2E2A", fontweight="bold")
ax.annotate(f"${rt_olap[-1]:.1f}B\n(2033)", xy=(2033, rt_olap[-1]), xytext=(2031.5, 21), fontsize=9, color="#8B2E2A", fontweight="bold")
ax.annotate(f"${dbms[-1]:.0f}B\n(2033)", xy=(2033, dbms[-1]), xytext=(2031.5, 215), fontsize=9, color="#1F4E8C", fontweight="bold")

# ClickHouse ARR overlay
ch_years = [2024, 2025, 2026]
ch_arr = [0.06, 0.10, 0.25]  # rough ARR in $B, well below TAM scale
ax.scatter(ch_years, ch_arr, color="#5CB85C", s=80, zorder=5, label="ClickHouse ARR run-rate (current scale)")
for xi, val in zip(ch_years, ch_arr):
    ax.text(xi, val + 4, f"${val * 1000:.0f}M", ha="center", fontsize=8, color="#1F4E1F", fontweight="bold")

ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Market size (USD billions)", fontsize=11)
ax.set_title("ClickHouse addressable market — real-time OLAP fastest-growing slice of $100B+ DBMS market", fontsize=11, fontweight="bold")
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.set_yscale("log")
ax.set_ylim(1, 350)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=30)

plt.tight_layout()
out = Path(__file__).parent / "clickhouse_tam.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved: {out}")
