"""Charts for 中际旭创 (SZSE:300308) company research report."""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS"]
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = Path(__file__).parent

# ---------- Chart 1: Revenue + Net Profit trend (2023-2025) ----------
# 来自 2025 年度报告 第7页 主要会计数据 (披露的 3 年区间)
years = ["2023", "2024", "2025"]
revenue_bn = [10.72, 23.86, 38.24]      # RMB bn
np_bn = [2.17, 5.17, 10.80]              # 归母净利润 RMB bn

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue_bn, color="#2E5F8A", alpha=0.85, label="营业收入 (RMB bn)")
for b, v in zip(bars, revenue_bn):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}", ha="center", fontsize=10)
ax1.set_ylabel("营业收入 (RMB bn)", color="#2E5F8A", fontsize=11)
ax1.set_ylim(0, 45)
ax1.tick_params(axis="y", colors="#2E5F8A")

ax2 = ax1.twinx()
ax2.plot(years, np_bn, color="#4FA64F", marker="o", linewidth=2.4, label="归母净利润")
for x, y in zip(years, np_bn):
    ax2.text(x, y + 0.3, f"{y:.2f}", ha="center", color="#4FA64F", fontsize=10)
ax2.set_ylabel("归母净利润 (RMB bn)", color="#4FA64F", fontsize=11)
ax2.set_ylim(0, 13)
ax2.tick_params(axis="y", colors="#4FA64F")

plt.title("中际旭创 — 营业收入 & 归母净利润 (2023-2025)", fontsize=13, pad=14)
fig.tight_layout()
plt.savefig(OUT / "innolight_revenue_gm.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 2: Quarterly revenue trend FY2024-Q1 FY2026 ----------
quarters = ["24Q1", "24Q2", "24Q3", "24Q4", "25Q1", "25Q2", "25Q3", "25Q4", "26Q1"]
qrev = [4.86, 6.45, 6.514, 6.039, 6.674, 8.115, 10.216, 13.235, 19.496]  # RMB bn
qnp = [1.038, 1.40, 1.394, 1.339, 1.583, 2.412, 3.137, 3.665, 5.735]      # RMB bn

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(quarters))
w = 0.38
b1 = ax.bar(x - w / 2, qrev, w, color="#2E5F8A", label="营业收入")
b2 = ax.bar(x + w / 2, qnp, w, color="#4FA64F", label="归母净利润")
for bar in b1:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f"{bar.get_height():.1f}",
            ha="center", fontsize=8)
for bar in b2:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f"{bar.get_height():.1f}",
            ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_ylabel("RMB bn")
ax.set_title("中际旭创 — 季度营业收入 & 归母净利润 (2024Q1–2026Q1)", fontsize=13, pad=12)
ax.legend(loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
plt.savefig(OUT / "innolight_quarterly.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 3: Geographic revenue mix (2025) ----------
labels = ["境外 (Overseas)", "境内 (Domestic China)"]
sizes = [90.58, 9.42]
colors = ["#2E5F8A", "#D9531E"]
fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                   autopct="%1.1f%%", startangle=110,
                                   textprops={"fontsize": 11})
for t in autotexts:
    t.set_color("white")
    t.set_fontsize(12)
    t.set_weight("bold")
ax.set_title("中际旭创 — FY2025 营业收入地区构成", fontsize=13, pad=14)
fig.tight_layout()
plt.savefig(OUT / "innolight_geo_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 4: TAM — Lightcounting global datacom optical module forecast ----------
# Source: 公司 2025 年年报 引用 Lightcounting 数据
years_tam = ["2025E", "2026E", "2027E", "2028E", "2029E", "2030E"]
# 全球数通光模块整体 ~ 22.8 (26E) → 41.4 (30E); 2025E推算 ~ 16.6
total = [16.6, 22.8, 28.0, 33.5, 37.8, 41.4]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(years_tam, total, color="#2E5F8A", alpha=0.85)
for b, v in zip(bars, total):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"${v:.1f}B", ha="center", fontsize=10)
ax.set_ylabel("市场规模 (USD bn)", fontsize=11)
ax.set_ylim(0, 50)
ax.set_title("全球数通光模块市场规模预测 (Lightcounting)", fontsize=13, pad=12)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
plt.savefig(OUT / "innolight_tam.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------- Chart 5: R&D investment & headcount ----------
years_rd = ["2023", "2024", "2025"]
rd_amt = [0.809, 1.333, 1.676]   # RMB bn
rd_pct = [7.55, 5.58, 4.38]
headcount = [None, 1453, 2169]    # 2023 not explicitly disclosed in 2025 annual

fig, ax1 = plt.subplots(figsize=(9, 5))
b = ax1.bar(years_rd, rd_amt, color="#2E5F8A", alpha=0.85, label="研发投入 (RMB bn)")
for bar, v in zip(b, rd_amt):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 0.03, f"{v:.2f}", ha="center", fontsize=10)
ax1.set_ylabel("研发投入 (RMB bn)", color="#2E5F8A", fontsize=11)
ax1.set_ylim(0, 2.2)
ax1.tick_params(axis="y", colors="#2E5F8A")

ax2 = ax1.twinx()
ax2.plot(years_rd, rd_pct, color="#D9531E", marker="o", linewidth=2.4, label="占营收比 (%)")
for x, y in zip(years_rd, rd_pct):
    ax2.text(x, y + 0.2, f"{y:.2f}%", ha="center", color="#D9531E", fontsize=10)
ax2.set_ylabel("研发投入占营业收入比例 (%)", color="#D9531E", fontsize=11)
ax2.set_ylim(0, 10)
ax2.tick_params(axis="y", colors="#D9531E")
plt.title("中际旭创 — 研发投入金额与营收占比 (2023–2025)", fontsize=13, pad=12)
fig.tight_layout()
plt.savefig(OUT / "innolight_rd.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts written.")
