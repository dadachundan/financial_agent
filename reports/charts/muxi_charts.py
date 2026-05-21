"""Charts for 沐曦股份 (SSE:688802) company-research report."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Hiragino Sans GB", "Arial Unicode MS", "STHeiti", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(path)


# --- Chart 1: Revenue + GM trend (3-year) ---
years = ["2023", "2024", "2025"]
rev = [0.530, 7.431, 16.441]  # 亿元 (RMB 100M)
gm = [None, 53.49, 56.51]  # %  (2023 GM 未单列，留空)
fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
b = ax1.bar(years, rev, color="#1f77b4", alpha=0.85, label="营业收入 (亿元)")
for rect, v in zip(b, rev):
    ax1.text(rect.get_x() + rect.get_width() / 2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)
ax1.set_ylabel("营业收入 (人民币 亿元)", color="#1f77b4")
ax1.set_ylim(0, max(rev) * 1.2)
ax2 = ax1.twinx()
ax2.plot(years, gm, color="#d62728", marker="o", linewidth=2.2, label="毛利率 (%)")
for i, g in enumerate(gm):
    if g is not None:
        ax2.text(i, g + 1.5, f"{g:.1f}%", ha="center", color="#d62728", fontsize=10)
ax2.set_ylabel("毛利率 (%)", color="#d62728")
ax2.set_ylim(0, 80)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
plt.title("沐曦股份 2023–2025 营业收入与毛利率走势", pad=12)
fig.tight_layout()
_save(fig, "muxi_revenue_gm_trend.png")


# --- Chart 2: 2025 营收构成 - 按产品/销售模式/地区 ---
fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
# By product
axes[0].pie([16.31, 0.13], labels=["GPU 产品及配件\n99.2%", "IP/技术服务\n0.8%"],
            colors=["#1f77b4", "#aec7e8"], autopct="", startangle=90, textprops={"fontsize": 9})
axes[0].set_title("按产品", fontsize=11)
# By channel
axes[1].pie([7.677, 8.764], labels=["直销\n46.7%", "经销\n53.3%"],
            colors=["#2ca02c", "#98df8a"], autopct="", startangle=90, textprops={"fontsize": 9})
axes[1].set_title("按销售模式", fontsize=11)
# By geography
axes[2].pie([16.416, 0.025], labels=["中国内地\n99.85%", "中国香港\n0.15%"],
            colors=["#ff7f0e", "#ffbb78"], autopct="", startangle=90, textprops={"fontsize": 9})
axes[2].set_title("按地区", fontsize=11)
plt.suptitle("沐曦股份 2025 年营业收入构成 (合计 16.44 亿元)", y=1.02, fontsize=12)
fig.tight_layout()
_save(fig, "muxi_2025_revenue_mix.png")


# --- Chart 3: 季度营收趋势 (Q1 2025 vs Q1 2026 + FY) ---
labels = ["Q1 2025", "FY 2024", "Q1 2026", "FY 2025"]
values = [3.204, 7.431, 5.619, 16.441]
colors = ["#aec7e8", "#1f77b4", "#aec7e8", "#1f77b4"]
fig, ax = plt.subplots(figsize=(8.5, 4.5))
b = ax.bar(labels, values, color=colors)
for rect, v in zip(b, values):
    ax.text(rect.get_x() + rect.get_width() / 2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10)
ax.set_ylabel("营业收入 (人民币 亿元)")
ax.set_title("沐曦股份 营收节奏：2025 年高增长延续至 2026Q1 (+75% YoY)", pad=10)
ax.text(0.5, -0.18, "Q1 2026 收入 5.62 亿元，已达 FY2024 全年 76%；FY2025 同比 +121%",
        transform=ax.transAxes, ha="center", fontsize=9, color="#444")
fig.tight_layout()
_save(fig, "muxi_quarterly_revenue.png")


# --- Chart 4: GPU 出货量与单价 ---
fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
cat = ["训推一体\nGPU 板卡", "智算推理\nGPU 板卡"]
ship = [33649, 4946]
b = ax1.bar(cat, ship, color=["#1f77b4", "#ff7f0e"])
for rect, v in zip(b, ship):
    ax1.text(rect.get_x() + rect.get_width() / 2, v + 800, f"{v:,}", ha="center", fontsize=10)
ax1.set_ylabel("2025 年销售量 (片)")
ax1.set_ylim(0, max(ship) * 1.2)
ax1.set_title("沐曦股份 2025 年 GPU 板卡出货结构\n累计销量逾 5.5 万颗 · 训推一体卡占主导", pad=10)
ax1.text(0.5, -0.18,
         "训推一体 GPU 同比 +147% · 智算推理 GPU 同比 +866%",
         transform=ax1.transAxes, ha="center", fontsize=9, color="#444")
fig.tight_layout()
_save(fig, "muxi_gpu_shipments.png")


# --- Chart 5: 研发投入与净亏损 ---
fig, ax1 = plt.subplots(figsize=(8.5, 4.6))
yrs = ["2023", "2024", "2025"]
rnd = [6.984, 9.009, 10.274]  # 亿元 — 2023 研发占比 1317.63% 反推: 0.530*13.176 ≈ 6.98
net = [-8.711, -14.089, -7.894]  # 归母净利润 亿元
ax1.bar(yrs, rnd, color="#9467bd", alpha=0.85, label="研发投入 (亿元)")
for i, v in enumerate(rnd):
    ax1.text(i - 0.18, v + 0.25, f"{v:.2f}", color="#9467bd", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(yrs, net, color="#d62728", marker="o", linewidth=2.2, label="归母净利润 (亿元)")
for i, v in enumerate(net):
    ax2.text(i + 0.1, v - 0.6, f"{v:.2f}", color="#d62728", fontsize=9)
ax1.set_ylabel("研发投入 (人民币 亿元)", color="#9467bd")
ax2.set_ylabel("归母净利润 (人民币 亿元)", color="#d62728")
ax1.set_ylim(0, 14)
ax2.set_ylim(-16, 2)
plt.title("沐曦股份 研发投入持续高企，亏损呈收窄态势", pad=10)
fig.tight_layout()
_save(fig, "muxi_rnd_vs_loss.png")


# --- Chart 6: 中国 AI 加速芯片市场规模 ---
yrs = ["2023", "2024", "2025E", "2026E", "2027E"]
mkt = [718, 1425, 2398, 3500, 5000]  # 亿元；2025E 弗若斯特沙利文；2026E/2027E est. linear
fig, ax = plt.subplots(figsize=(8.5, 4.5))
b = ax.bar(yrs, mkt, color=["#7f7f7f", "#7f7f7f", "#bcbd22", "#bcbd22", "#bcbd22"])
for rect, v in zip(b, mkt):
    ax.text(rect.get_x() + rect.get_width() / 2, v + 80, f"{v:,}", ha="center", fontsize=10)
ax.set_ylabel("市场规模 (人民币 亿元)")
ax.set_title("中国 AI 加速芯片市场规模：2024–2025 高速扩张\n(数据来源：弗若斯特沙利文 / IDC；2026–27 为线性外推)", pad=10)
fig.tight_layout()
_save(fig, "muxi_china_ai_chip_tam.png")
