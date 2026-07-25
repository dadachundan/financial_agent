"""GAC Group (SSE:601238 / HKEX:2238) — research charts.

Sources:
- 广汽集团 2025 年年度报告 (cninfo, 2026-03-27)
- 广汽集团 2024 / 2023 / 2022 / 2021 年年度报告 (cninfo)
- 中国汽车工业协会 2025 销量数据 (cited in 2025 年报第19页)
- 同行 2025 业绩公告（汇总报道）

Run:  python3 oneoff/gac_charts.py
Outputs to: reports/charts/gac_*.png
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

# Chinese font (macOS)
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti TC", "Songti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(__file__), "..", "reports", "charts")
os.makedirs(OUT, exist_ok=True)


# ===== Chart 1: Revenue + net profit + gross margin (5-yr) =====
years = ["2021", "2022", "2023", "2024", "2025"]
# Annual reports, consolidated, RMB bn (亿元)
revenue   = [75.68, 110.06, 128.76, 106.80, 95.66]
net_inc   = [ 7.33, 8.07,  4.43,  0.82, -8.78]
# Group consolidated gross margin (整车 + 零部件 + 商贸 + 金融 weighted)
gm_pct    = [ 5.5,  4.5,   4.0,   3.85, -2.80]   # 2025 -2.80% per filing

fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
w = 0.35
b1 = ax1.bar(x - w/2, revenue, w, color="#1f4e79", label="营业收入 (亿元)")
b2 = ax1.bar(x + w/2, net_inc, w, color=["#5b9bd5"]*4 + ["#c00000"], label="归母净利润 (亿元)")
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel("亿元 RMB", fontsize=11)
ax1.axhline(0, color="black", linewidth=0.6)
for bars in (b1, b2):
    for b in bars:
        h = b.get_height()
        ax1.text(b.get_x()+b.get_width()/2, h + (3 if h>=0 else -6),
                 f"{h:.1f}", ha="center", va="bottom" if h>=0 else "top", fontsize=9)

ax2 = ax1.twinx()
ax2.plot(x, gm_pct, color="#ed7d31", marker="o", linewidth=2.2, label="集团毛利率 (%)")
for xi, yi in zip(x, gm_pct):
    ax2.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                 xytext=(0, 10), ha="center", fontsize=9, color="#ed7d31")
ax2.set_ylabel("毛利率 %", color="#ed7d31", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#ed7d31")
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax2.set_ylim(-6, 10)

ax1.set_title("广汽集团 2021–2025 营业收入、归母净利润与毛利率\n(GAC Group — 5-yr Revenue / Net Income / Gross Margin)",
              fontsize=12.5, pad=12)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc="lower left", framealpha=0.95)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "gac_5yr_financials.png"), dpi=150, bbox_inches="tight")
plt.close()


# ===== Chart 2: Vehicle sales by brand 2021–2025 (stacked bar) =====
brands = ["广汽传祺", "广汽埃安", "广汽本田", "广汽丰田", "其他"]
# Unit: 万辆 (10k vehicles), per annual reports' 产销快报
data = {
    "广汽传祺": [32.40, 36.34, 40.86, 41.46, 31.92],
    "广汽埃安": [12.02, 27.12, 48.00, 37.49, 29.01],
    "广汽本田": [78.01, 72.06, 64.05, 47.06, 35.20],
    "广汽丰田": [83.50, 100.05, 95.10, 73.80, 75.56],
    "其他":     [ 1.30,  7.04,  3.30, 0.60,  0.46],  # 三菱+商用车
}
fig, ax = plt.subplots(figsize=(10, 5.5))
bottoms = np.zeros(len(years))
colors = ["#2e75b6", "#5b9bd5", "#a9d18e", "#70ad47", "#bfbfbf"]
for brand, color in zip(brands, colors):
    vals = data[brand]
    ax.bar(years, vals, bottom=bottoms, label=brand, color=color)
    bottoms += np.array(vals)

# Annotate totals
totals = bottoms
for i, (yr, t) in enumerate(zip(years, totals)):
    ax.text(i, t + 3, f"{t:.1f}", ha="center", fontsize=10, fontweight="bold")

ax.set_ylabel("销量 (万辆)", fontsize=11)
ax.set_title("广汽集团 2021–2025 分品牌汽车销量\n(Vehicle Sales by Brand — 10k units)",
             fontsize=12.5, pad=12)
ax.legend(loc="upper right", framealpha=0.95)
ax.set_ylim(0, max(totals) * 1.12)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "gac_sales_by_brand.png"), dpi=150, bbox_inches="tight")
plt.close()


# ===== Chart 3: 2025 China automakers — revenue / net profit / sales comparison =====
companies = ["BYD\n比亚迪", "SAIC\n上汽", "Geely\n吉利", "Changan\n长安", "Chery\n奇瑞", "GWM\n长城", "GAC\n广汽"]
revenue_bn = [804, 627, 286, 159, 248, 202, 95.66]      # 亿元RMB 2025 (媒体汇总 + 各家年报)
net_bn     = [326, 101, 169, 8.4, 190, 99, -87.8]       # 亿元RMB 2025 归母净利润 (单位：亿)
sales_m    = [4.60, 4.51, 3.02, 2.92, 2.83, 1.30, 1.72] # 百万辆

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: revenue + net profit
xa = np.arange(len(companies))
w = 0.4
axes[0].bar(xa - w/2, revenue_bn, w, color="#1f4e79", label="营收 (亿元)")
axes[0].bar(xa + w/2, net_bn, w, color=["#5b9bd5"]*6 + ["#c00000"], label="归母净利 (亿元)")
axes[0].axhline(0, color="black", linewidth=0.6)
axes[0].set_xticks(xa); axes[0].set_xticklabels(companies, fontsize=9)
axes[0].set_ylabel("亿元 RMB")
axes[0].set_title("2025 同业营收 vs 归母净利润", fontsize=11.5)
axes[0].legend(loc="upper right", fontsize=9)
for i, v in enumerate(net_bn):
    axes[0].annotate(f"{v:.0f}", (xa[i]+w/2, v + (15 if v>=0 else -25)),
                     ha="center", fontsize=8.5, color="black")

# Right: sales volume
axes[1].bar(companies, sales_m, color=["#70ad47"]*6 + ["#c00000"])
axes[1].set_ylabel("销量 (百万辆)")
axes[1].set_title("2025 销量 (百万辆)", fontsize=11.5)
for i, v in enumerate(sales_m):
    axes[1].text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
for ax in axes:
    ax.tick_params(axis="x", labelsize=9)
plt.suptitle("中国头部车企 2025 业绩与销量对照 (GAC vs. peers)",
             fontsize=12.5, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "gac_peer_comparison.png"), dpi=150, bbox_inches="tight")
plt.close()


# ===== Chart 4: China NEV penetration vs GAC NEV mix =====
years2 = ["2020", "2021", "2022", "2023", "2024", "2025"]
china_nev_pen = [5.4, 13.4, 25.6, 31.6, 40.9, 47.9]   # CAAM, % of all new auto sales
gac_nev_share = [4.4, 9.4, 19.4, 27.3, 22.6, 25.2]    # 估算 from filings

fig, ax = plt.subplots(figsize=(9.5, 5.2))
ax.plot(years2, china_nev_pen, marker="o", linewidth=2.4, color="#2e75b6", label="全国 NEV 渗透率")
ax.plot(years2, gac_nev_share, marker="s", linewidth=2.4, color="#c00000", label="广汽集团 NEV 销量占比")
for x_, yv in zip(years2, china_nev_pen):
    ax.annotate(f"{yv:.1f}%", (x_, yv), textcoords="offset points", xytext=(0,8), ha="center", color="#2e75b6", fontsize=9)
for x_, yv in zip(years2, gac_nev_share):
    ax.annotate(f"{yv:.1f}%", (x_, yv), textcoords="offset points", xytext=(0,-14), ha="center", color="#c00000", fontsize=9)
ax.set_ylabel("占比 %")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, 55)
ax.set_title("全国 NEV 渗透率 vs 广汽 NEV 销量占比\n(China NEV penetration vs. GAC's NEV sales mix)",
             fontsize=12, pad=12)
ax.grid(alpha=0.3)
ax.legend(loc="upper left", framealpha=0.95)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "gac_nev_gap.png"), dpi=150, bbox_inches="tight")
plt.close()


# ===== Chart 5: Overseas exports surge =====
years3 = ["2021", "2022", "2023", "2024", "2025", "2026E"]
overseas_units = [1.0, 1.9, 4.97, 8.45, 12.5, 25.0]   # 万辆 — per 2025 年报第8页 + 集团目标
yoy = [None, 90, 162, 70, 48, 100]

fig, ax = plt.subplots(figsize=(9.5, 5))
bars = ax.bar(years3, overseas_units,
              color=["#5b9bd5"]*5 + ["#bfbfbf"])
ax.set_ylabel("海外销量 (万辆)")
ax.set_title("广汽自主品牌海外终端销量 — 第二增长曲线\n(GAC own-brand overseas retail sales, 10k units)",
             fontsize=12, pad=12)
for i, (v, g) in enumerate(zip(overseas_units, yoy)):
    label = f"{v:.1f}"
    if g is not None:
        label += f"\n+{g}%"
    ax.text(i, v + 0.5, label, ha="center", fontsize=9.5)
ax.set_ylim(0, max(overseas_units)*1.2)
ax.text(5, overseas_units[5]*0.55, "2026 目标\n(集团指引)",
        ha="center", color="#7f7f7f", fontsize=9, style="italic")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "gac_overseas.png"), dpi=150, bbox_inches="tight")
plt.close()

print("Saved 5 charts to", OUT)
for f in sorted(os.listdir(OUT)):
    if f.startswith("gac_"):
        print(" ", f)
