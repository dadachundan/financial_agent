"""Charts for 光环新网 (SZSE:300383) company research report.

All inputs taken from cninfo 年度报告 (2022, 2023, 2024, 2025 年报) and
2026 年第一季度报告 — never fabricated. Page references in the markdown.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# zh font (macOS)
mpl.rcParams["font.family"] = ["Heiti TC", "Kaiti SC", "Hannotate SC", "Arial Unicode MS", "sans-serif"]
mpl.rcParams["axes.unicode_minus"] = False

OUT = Path(__file__).parent
COMPANY = "sinnet"


def save(fig, name):
    path = OUT / f"{COMPANY}_{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"saved: {path}")
    plt.close(fig)


# ---------------------------------------------------------------------
# Chart 1 — 4yr revenue + net-margin trend (2022-2025), dual axis
# Source: 2024 年报 五、主要会计数据 (p.12) + 2025 年报 五、主要会计数据 (p.13)
# Revenue (万元):  2022 = 719,103;  2023 = 785,546;  2024 = 728,121;  2025 = 717,765
# Net income (万元): 2022 = -87,992;  2023 = 38,796;   2024 = 38,144;   2025 = -75,921
# ---------------------------------------------------------------------
years = ["2022", "2023", "2024", "2025"]
revenue_yi = [71.91, 78.55, 72.81, 71.78]  # 亿元
ni_yi = [-8.80, 3.88, 3.81, -7.59]  # 亿元 (归母净利润)

fig, ax1 = plt.subplots(figsize=(9, 4.8))
bars = ax1.bar(years, revenue_yi, color="#3F7CB6", alpha=0.85, label="营业收入 (亿元)")
ax1.set_ylabel("营业收入 (亿元)", color="#3F7CB6", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#3F7CB6")
ax1.set_ylim(0, max(revenue_yi) * 1.25)
for b, v in zip(bars, revenue_yi):
    ax1.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.2f}", ha="center", fontsize=10, color="#3F7CB6")

ax2 = ax1.twinx()
ax2.plot(years, ni_yi, color="#D94F4F", marker="o", linewidth=2.2, label="归母净利润 (亿元)")
ax2.set_ylabel("归母净利润 (亿元)", color="#D94F4F", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#D94F4F")
ax2.axhline(0, color="#666", lw=0.7, ls="--")
for x, y in zip(years, ni_yi):
    ax2.annotate(f"{y:+.2f}", xy=(x, y), xytext=(0, 10 if y >= 0 else -16),
                 textcoords="offset points", ha="center", fontsize=9, color="#D94F4F")

plt.title("光环新网 (300383) 2022-2025 营业收入与归母净利润趋势", fontsize=12)
fig.tight_layout()
save(fig, "rev_ni_trend")

# ---------------------------------------------------------------------
# Chart 2 — 2025 revenue mix by product (IDC vs Cloud vs Other)
# Source: 2025 年报 四、主营业务分析 (p.29)
# IDC = 22.31 亿; Cloud = 48.36 亿; 互联网宽带接入 = 0.45 亿; Other = 0.65 亿
# ---------------------------------------------------------------------
mix_labels = ["IDC 及增值服务\n31.1%", "云计算 (含 AWS)\n67.4%", "其他\n1.5%"]
mix_values = [22.31, 48.36, 0.45 + 0.65]
colors = ["#3F7CB6", "#7BAE6E", "#C8B568"]
fig, ax = plt.subplots(figsize=(7, 5.2))
wedges, _ = ax.pie(mix_values, labels=mix_labels, colors=colors, startangle=90,
                   wedgeprops={"edgecolor": "white", "linewidth": 2},
                   textprops={"fontsize": 11})
ax.set_title("2025 年营业收入按产品拆分 (合计 71.78 亿元)", fontsize=12)
save(fig, "revenue_mix_2025")

# ---------------------------------------------------------------------
# Chart 3 — IDC 业务毛利率 vs 云计算业务毛利率, 2024 vs 2025
# Source: 2025 年报 "一、报告期内公司从事的主要业务" (p.16)
#   IDC 毛利率 2025 = 29.15% (vs 2024: 34.40%)
#   云计算毛利率 2025 = 6.76% (vs 2024: 9.02%)
# ---------------------------------------------------------------------
segments = ["IDC 及增值服务", "云计算"]
gm_2024 = [34.40, 9.02]
gm_2025 = [29.15, 6.76]
x = np.arange(len(segments))
w = 0.35
fig, ax = plt.subplots(figsize=(7.5, 4.6))
b1 = ax.bar(x - w/2, gm_2024, w, label="2024 年", color="#9AB7D4")
b2 = ax.bar(x + w/2, gm_2025, w, label="2025 年", color="#D94F4F")
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4,
                f"{b.get_height():.2f}%", ha="center", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=11)
ax.set_ylabel("毛利率 (%)", fontsize=11)
ax.set_title("分业务毛利率：2025 vs 2024", fontsize=12)
ax.legend(loc="upper right")
ax.set_ylim(0, max(gm_2024) * 1.25)
save(fig, "segment_gm")

# ---------------------------------------------------------------------
# Chart 4 — 机柜投产规模 (cumulative)
# Source: 2025 年报 p.16 ("已投产机柜超过8.6 万个，其中2025 年新增投产2.6 万个")
# 2026 Q1 报告 p.5 ("2026 年截至目前新增 4,000 个，已投放机柜总量超过8.6 万个")
# Approximate prior-year cumulative end-points derived from 历年年报 disclosures.
# Using disclosed milestones only; intermediate years use the announced YoY add.
# 2025 end: 86,000; 2025 add: 26,000; → 2024 end ≈ 60,000.
# 2024 end derived (60,000); 2023 end disclosed in 2023 年报 ≈ 50,000 (per public IR);
# 2022 end ≈ 41,000 (per public IR). These pre-2024 numbers come from public IR
# call-outs (东方财富 2024 年 IR 调研纪要) — flagged as "公司公开披露" rather than 年报 page-ref.
# To stay strictly within filings, we limit to disclosed 2024 + 2025 numbers
# and the 23 万 全国规划机柜规模 anchor.
# ---------------------------------------------------------------------
labels = ["2024 年末\n(已投产)", "2025 年新增", "2025 年末\n(已投产)", "全国规划\n机柜规模"]
values = [60.0, 26.0, 86.0, 230.0]  # 千个
colors_b = ["#9AB7D4", "#D94F4F", "#3F7CB6", "#7BAE6E"]
fig, ax = plt.subplots(figsize=(8.5, 4.6))
bars = ax.bar(labels, values, color=colors_b, alpha=0.9)
for b, v in zip(bars, values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f"{v:.0f}", ha="center", fontsize=10)
ax.set_ylabel("机柜数 (千个，按 4.4KW 等效)", fontsize=11)
ax.set_title("光环新网机柜资源：投产规模 vs 全国规划储备", fontsize=12)
ax.set_ylim(0, 270)
save(fig, "rack_capacity")

# ---------------------------------------------------------------------
# Chart 5 — 2025 收入分地区 (top regions)
# Source: 2025 年报 p.29 "营业收入整体情况 → 分地区"
# 北京 56.44; 河北 7.20; 上海 3.66; 香港 2.70; 天津 1.30; 新疆 0.39; 其他 0.08
# ---------------------------------------------------------------------
regions = ["北京", "河北 (燕郊)", "上海 (嘉定)", "香港", "天津 (宝坻)", "新疆", "其他"]
rev = [56.44, 7.20, 3.66, 2.70, 1.30, 0.39, 0.08]
share = [v / sum(rev) * 100 for v in rev]
fig, ax = plt.subplots(figsize=(8.5, 4.8))
bars = ax.barh(regions[::-1], rev[::-1], color="#3F7CB6")
for i, (b, v, s) in enumerate(zip(bars, rev[::-1], share[::-1])):
    ax.text(v + 1, b.get_y() + b.get_height() / 2, f"{v:.2f} 亿 ({s:.1f}%)",
            va="center", fontsize=10)
ax.set_xlabel("营业收入 (亿元)", fontsize=11)
ax.set_title("光环新网 2025 年分地区营业收入", fontsize=12)
ax.set_xlim(0, max(rev) * 1.25)
save(fig, "revenue_by_region")

# ---------------------------------------------------------------------
# Chart 6 — 资本结构演变 (固定资产 + 在建工程 + 商誉 + 借款) 2024 vs 2025
# Source: 2025 年报 p.47-48 资产构成
# 固定资产: 87.16 亿 → 108.89 亿; 在建工程: 25.92 → 14.29; 商誉: 10.83 → 2.20;
# 长期借款: 21.19 → 35.83; 短期借款: 14.71 → 16.67
# ---------------------------------------------------------------------
items = ["固定资产", "在建工程", "商誉", "短期借款", "长期借款"]
y_2024 = [87.16, 25.92, 10.83, 14.71, 21.19]
y_2025 = [108.89, 14.29, 2.20, 16.67, 35.83]
x = np.arange(len(items))
w = 0.35
fig, ax = plt.subplots(figsize=(9.5, 4.8))
b1 = ax.bar(x - w/2, y_2024, w, label="2024 年末", color="#9AB7D4")
b2 = ax.bar(x + w/2, y_2025, w, label="2025 年末", color="#3F7CB6")
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5,
                f"{b.get_height():.1f}", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(items, fontsize=10)
ax.set_ylabel("金额 (亿元)", fontsize=11)
ax.set_title("资产负债关键科目：2025 vs 2024 (亿元)", fontsize=12)
ax.legend(loc="upper right")
ax.set_ylim(0, 130)
save(fig, "balance_sheet")

print("All charts generated.")
