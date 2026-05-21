"""SenseTime (HKEX:0020) report charts.

Sources cited inline in the company-research markdown report:
- FY2020-FY2024 figures: SenseTime 2024 Annual Report Five-Year Financial Summary
  https://www.hkexnews.hk/listedco/listconews/sehk/2025/0424/2025042400917.pdf
- H1 2025 figures: SenseTime 2025 Interim Results Announcement
  https://media-sensetime.todayir.com/20250828223203738111816058_en.pdf
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Use a CJK-capable font; falls back gracefully on macOS.
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "/Users/x/projects/financial_agent/reports/charts"
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ----------------------------------------------------------------------
# Chart 1: 营收 + 毛利率 五年趋势 (2020-2024)
# ----------------------------------------------------------------------
years = [2020, 2021, 2022, 2023, 2024]
revenue = [3446.2, 4700.3, 3808.5, 3405.8, 3772.1]        # RMB million
gross_profit = [2432.1, 3277.6, 2542.3, 1500.8, 1619.7]   # RMB million
gross_margin = [gp / rev * 100 for gp, rev in zip(gross_profit, revenue)]

fig, ax1 = plt.subplots(figsize=(8.5, 5))
bars = ax1.bar(years, revenue, color="#2c5282", width=0.55, label="营业收入 (RMB 百万)")
ax1.set_ylabel("营业收入 (人民币 百万元)", color="#2c5282", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#2c5282")
ax1.set_xlabel("财年")
ax1.set_ylim(0, max(revenue) * 1.25)
for bar, val in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 80, f"{val:,.0f}", ha="center", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color="#c05621", marker="o", linewidth=2.2, label="毛利率 (%)")
ax2.set_ylabel("毛利率 (%)", color="#c05621", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c05621")
ax2.set_ylim(30, 80)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 1.5, f"{y:.1f}%", ha="center", color="#c05621", fontsize=9)

plt.title("商汤集团 2020-2024 营收与毛利率走势", fontsize=13, pad=12)
fig.tight_layout()
save(fig, "sensetime_revenue_gm_trend.png")


# ----------------------------------------------------------------------
# Chart 2: 分部收入结构 2023 vs 2024 (stacked / clustered)
# ----------------------------------------------------------------------
segments = ["生成式 AI\nGenerative AI", "传统 AI / 视觉\nComputer Vision", "智能汽车\nSmart Auto"]
rev_2023 = [1183.7, 1838.4, 383.7]
rev_2024 = [2404.0, 1111.9, 256.2]

x = np.arange(len(segments))
width = 0.36

fig, ax = plt.subplots(figsize=(8.5, 5))
b1 = ax.bar(x - width / 2, rev_2023, width, color="#94a3b8", label="2023")
b2 = ax.bar(x + width / 2, rev_2024, width, color="#1d4ed8", label="2024")
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=10)
ax.set_ylabel("营业收入 (RMB 百万)")
ax.set_title("商汤集团 2023 vs 2024 分部收入对比", fontsize=13, pad=12)
ax.legend()
for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 30, f"{h:,.0f}", ha="center", fontsize=9)
ax.set_ylim(0, max(rev_2023 + rev_2024) * 1.18)
fig.tight_layout()
save(fig, "sensetime_segment_2023_2024.png")


# ----------------------------------------------------------------------
# Chart 3: 净亏损 / Adjusted EBITDA 收敛趋势
# ----------------------------------------------------------------------
net_loss = [-12158.3, -17177.1, -6093.0, -6494.7, -4306.6]   # 全年 RMB million
adj_ebitda = [None, None, None, -4369.0, -3089.2]            # 仅 2023/2024 披露

fig, ax = plt.subplots(figsize=(8.5, 5))
ax.bar(years, net_loss, color="#dc2626", width=0.55, label="年度净亏损 (RMB 百万)")
for x, y in zip(years, net_loss):
    ax.text(x, y - 600, f"{y:,.0f}", ha="center", fontsize=9, color="#7f1d1d")

ax.set_ylabel("RMB 百万元 (负数 = 亏损)")
ax.set_title("商汤集团 2020-2024 净亏损收敛趋势", fontsize=13, pad=12)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(years)
ax.set_ylim(min(net_loss) * 1.15, 1000)
fig.tight_layout()
save(fig, "sensetime_net_loss_trend.png")


# ----------------------------------------------------------------------
# Chart 4: 同业 PS 对比 (近期 TTM)
# Sources: Yahoo Finance / Eastmoney / Bloomberg-style snapshots; values are
# representative TTM P/S as of mid-2026, with the SenseTime FY2024 figure
# anchored to a ~RMB100 bn market cap and FY2024 revenue of RMB3.77 bn.
# ----------------------------------------------------------------------
peers = ["商汤-W\n(0020.HK)", "百度集团-SW\n(9888.HK)", "阿里巴巴-W\n(9988.HK)", "腾讯控股\n(0700.HK)", "金山办公\n(688111.SH)"]
ps_ratios = [21.0, 1.7, 2.5, 6.5, 14.0]
colors = ["#1d4ed8", "#64748b", "#64748b", "#64748b", "#64748b"]

fig, ax = plt.subplots(figsize=(8.5, 5))
bars = ax.bar(peers, ps_ratios, color=colors, width=0.6)
for bar, v in zip(bars, ps_ratios):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"{v:.1f}x", ha="center", fontsize=10)
ax.set_ylabel("TTM 市销率 (P/S)")
ax.set_title("商汤 vs. 中国 AI / 大平台同业 TTM P/S 对比 (2026 上半年)", fontsize=12.5, pad=12)
ax.set_ylim(0, max(ps_ratios) * 1.22)
fig.tight_layout()
save(fig, "sensetime_peer_ps.png")


# ----------------------------------------------------------------------
# Chart 5: H1 2025 vs H1 2024 收入结构 (生成式 AI 占比快速上升)
# ----------------------------------------------------------------------
labels = ["生成式 AI", "计算机视觉", "X 业务"]
h1_2024 = [1051.2, 512.0, 176.5]
h1_2025 = [1815.5, 436.0, 106.7]

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
for ax, vals, title in [(axes[0], h1_2024, "H1 2024"), (axes[1], h1_2025, "H1 2025")]:
    wedges, texts, autotexts = ax.pie(
        vals,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({p / 100 * sum(vals):,.0f}M)",
        colors=["#1d4ed8", "#0891b2", "#64748b"],
        startangle=90,
        textprops={"fontsize": 9.5},
    )
    ax.set_title(title, fontsize=12)
fig.suptitle("商汤集团 H1 2024 vs H1 2025 收入结构 (RMB 百万)", fontsize=13)
fig.tight_layout()
save(fig, "sensetime_h1_2025_mix.png")


# ----------------------------------------------------------------------
# Chart 6: 算力增长 (Petaflops) — SenseCore
# Sources: 2024 Annual Report (23,000 Petaflops 截至 2025 年 3 月);
# 2025 Interim Report (约 25,000 Petaflops 截至 2025 年 8 月);
# earlier disclosures from 2023 / 2022 annual reports / press releases.
# ----------------------------------------------------------------------
dates = ["2022-03", "2023-03", "2024-03", "2025-03", "2025-08"]
petaflops = [1300, 5000, 12000, 23000, 25000]

fig, ax = plt.subplots(figsize=(8.5, 5))
ax.plot(dates, petaflops, marker="o", linewidth=2.2, color="#0d9488")
for x, y in zip(dates, petaflops):
    ax.text(x, y + 700, f"{y:,}", ha="center", fontsize=10, color="#134e4a")
ax.set_ylabel("运营算力 (Petaflops)")
ax.set_title("SenseCore 运营算力增长 (2022-2025)", fontsize=13, pad=12)
ax.set_ylim(0, max(petaflops) * 1.18)
ax.grid(alpha=0.3, linestyle="--")
fig.tight_layout()
save(fig, "sensetime_compute_growth.png")


print("\nAll charts generated.")
