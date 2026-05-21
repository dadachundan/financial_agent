"""Charts for 特变电工 (SSE:600089) company research report."""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# Chinese font setup
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def fig_save(name):
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print("saved", path)


# Chart 1: Revenue + Net profit + GM trend (2020-2025)
# Source: 2025/2024/2022 annual reports (adjusted)
years = ["2020", "2021", "2022", "2023", "2024", "2025"]
revenue_bn = [49.90, 68.97, 95.89, 98.12, 97.82, 97.23]  # 亿元
net_profit_bn = [2.45, 7.25, 15.88, 10.71, 4.14, 5.95]  # 归母净利润 亿元
# Approx consolidated gross margin from 营业收入/营业成本
# 2020: gm n/a precise — derived from segment data later; we use approximate based on disclosed segments
gm_pct = [12.5, 17.5, 28.7, 23.1, 18.1, 18.8]  # 综合毛利率 估算/披露

fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.35
b1 = ax1.bar(x - w/2, revenue_bn, w, label="营业收入 (亿元)", color="#1f77b4")
b2 = ax1.bar(x + w/2, net_profit_bn, w, label="归母净利润 (亿元)", color="#ff7f0e")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("金额 (亿元 RMB)")
ax1.set_title("特变电工 2020–2025 营业收入、归母净利润与综合毛利率")
for bars in (b1, b2):
    for b in bars:
        h = b.get_height()
        ax1.annotate(f"{h:.1f}", xy=(b.get_x() + b.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha="center", fontsize=8)
ax2 = ax1.twinx()
ax2.plot(x, gm_pct, marker="o", color="#2ca02c", linewidth=2, label="综合毛利率 (%)")
for i, v in enumerate(gm_pct):
    ax2.annotate(f"{v:.1f}%", xy=(x[i], v), xytext=(0, 8), textcoords="offset points",
                 ha="center", color="#2ca02c", fontsize=8)
ax2.set_ylabel("综合毛利率 (%)", color="#2ca02c")
ax2.tick_params(axis="y", labelcolor="#2ca02c")
ax2.set_ylim(0, max(gm_pct) * 1.4)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
fig.tight_layout()
fig_save("tbea_revenue_profit_trend.png")


# Chart 2: 2025 Segment revenue stacked / pie
segments = ["电气设备", "电线电缆", "输变电成套", "新能源产品及工程",
            "煤炭", "发电", "铝电子新材料/合金", "黄金", "物流贸易", "其他"]
seg_rev = [267.60, 155.69, 49.25, 135.55, 169.66, 71.83, 63.03, 24.69, 5.53, 13.77]  # 亿元
seg_gm = [19.81, 8.34, 15.90, 0.59, 22.39, 54.75, 9.66, 57.23, 10.51, 30.97]

fig, ax = plt.subplots(figsize=(11, 5.5))
order = np.argsort(seg_rev)[::-1]
seg_sorted = [segments[i] for i in order]
rev_sorted = [seg_rev[i] for i in order]
gm_sorted = [seg_gm[i] for i in order]
bars = ax.bar(seg_sorted, rev_sorted, color="#3b78b3")
ax.set_ylabel("2025 年营业收入 (亿元)")
ax.set_title("特变电工 2025 年分产品收入结构与毛利率")
for i, b in enumerate(bars):
    ax.annotate(f"{rev_sorted[i]:.1f}\n({gm_sorted[i]:.1f}%)",
                xy=(b.get_x() + b.get_width()/2, b.get_height()),
                xytext=(0, 3), textcoords="offset points",
                ha="center", fontsize=8)
ax.tick_params(axis="x", labelrotation=25)
fig.tight_layout()
fig_save("tbea_segment_mix_2025.png")


# Chart 3: Peer P/E comparison (TTM)
peers = ["特变电工\n600089", "国电南瑞\n600406", "正泰电器\n601877", "东方电气\n600875",
         "思源电气\n002028", "科华数据\n002335", "通威股份\n600438"]
pe_ttm = [21.22, 24.77, 14.39, 29.30, 47.81, 75.09, -7.46]
colors = ["#d62728" if p == 21.22 else ("#7f7f7f" if p < 0 else "#1f77b4") for p in pe_ttm]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(peers, pe_ttm, color=colors)
ax.axhline(y=np.median([p for p in pe_ttm if p > 0]), color="green", linestyle="--",
           label=f"行业正PE中位数={np.median([p for p in pe_ttm if p>0]):.1f}x")
ax.set_ylabel("TTM 市盈率 (x)")
ax.set_title("特变电工 vs 同业可比公司 — TTM 市盈率 (2026-05-21)")
for i, b in enumerate(bars):
    h = b.get_height()
    label = f"{pe_ttm[i]:.1f}x" if pe_ttm[i] > 0 else f"亏损 ({pe_ttm[i]:.1f}x)"
    ax.annotate(label, xy=(b.get_x() + b.get_width()/2, h),
                xytext=(0, 3 if h > 0 else -15), textcoords="offset points",
                ha="center", fontsize=9)
ax.legend()
fig.tight_layout()
fig_save("tbea_peer_pe.png")


# Chart 4: Domestic vs overseas revenue (2024-2025)
labels = ["境内", "境外"]
rev_2024 = [840.65, 119.74]  # 亿元 (2024 调整后 - back-derived)
rev_2025 = [829.96, 126.62]
x = np.arange(len(labels))
w = 0.35
fig, ax = plt.subplots(figsize=(7, 4.5))
b1 = ax.bar(x - w/2, rev_2024, w, label="2024 (调整后)", color="#9aa0a6")
b2 = ax.bar(x + w/2, rev_2025, w, label="2025", color="#1f77b4")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("营业收入 (亿元)")
ax.set_title("特变电工 主营业务分地区收入 (2024 vs 2025)")
for bars in (b1, b2):
    for b in bars:
        h = b.get_height()
        ax.annotate(f"{h:.1f}", xy=(b.get_x() + b.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
ax.legend()
fig.tight_layout()
fig_save("tbea_geo_mix.png")


# Chart 5: R&D investment
years_rd = ["2021", "2022", "2023", "2024", "2025"]
rd_bn = [25.79, 32.36, 41.21, 46.13, 47.85]  # 亿元 研发投入合计
rd_ratio = [3.74, 3.38, 4.20, 4.72, 4.92]  # 占营收比
fig, ax1 = plt.subplots(figsize=(9, 4.8))
x = np.arange(len(years_rd))
bars = ax1.bar(x, rd_bn, color="#5b8def", label="研发投入 (亿元)")
ax1.set_xticks(x); ax1.set_xticklabels(years_rd)
ax1.set_ylabel("研发投入 (亿元)")
for i, b in enumerate(bars):
    ax1.annotate(f"{rd_bn[i]:.1f}", xy=(b.get_x()+b.get_width()/2, b.get_height()),
                 xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(x, rd_ratio, marker="o", color="#e45757", linewidth=2, label="占营收比 (%)")
for i, v in enumerate(rd_ratio):
    ax2.annotate(f"{v:.2f}%", xy=(x[i], v), xytext=(0, 8), textcoords="offset points",
                 ha="center", color="#e45757", fontsize=9)
ax2.set_ylabel("占营收比 (%)", color="#e45757")
ax2.tick_params(axis="y", labelcolor="#e45757")
ax1.set_title("特变电工 研发投入 (2021–2025)")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
fig.tight_layout()
fig_save("tbea_rd.png")
