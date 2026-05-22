"""Charts for Yue Yuen Industrial Holdings (HKEX:00551) company research."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os

plt.rcParams.update({
    "font.family": ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS", "DejaVu Sans"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- Chart 1: 5-yr Revenue + Gross Margin trend ----------
years = ["2020", "2021", "2022", "2023", "2024"]
revenue = [8445, 8533, 8970, 7890, 8182]  # USD millions
# Gross margin: from annual reports / press releases
gm = [23.4, 24.5, 23.6, 24.2, 24.4]  # %

fig, ax1 = plt.subplots(figsize=(8, 4.5))
bars = ax1.bar(years, revenue, color="#1f77b4", alpha=0.78, label="营业收入 (US$ M)")
ax1.set_ylabel("营业收入 (US$ M)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, max(revenue) * 1.18)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 80, f"{v:,}",
             ha="center", va="bottom", fontsize=9, color="#1f77b4")

ax2 = ax1.twinx()
ax2.spines["top"].set_visible(False)
ax2.plot(years, gm, color="#d62728", marker="o", linewidth=2, label="毛利率 (%)")
ax2.set_ylabel("毛利率 (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(20, 28)
for x, y in zip(years, gm):
    ax2.text(x, y + 0.25, f"{y:.1f}%", ha="center", fontsize=9, color="#d62728")

plt.title("裕元集团 营业收入与毛利率 (2020-2024)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_revenue_gm.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- Chart 2: 2024 Revenue mix by category ----------
labels = ["运动/户外鞋\n53.8%", "宝胜零售\n31.3%", "休闲鞋及\n运动凉鞋\n9.4%", "鞋底配件\n及其他 5.5%"]
sizes = [53.8, 31.3, 9.4, 5.5]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]

fig, ax = plt.subplots(figsize=(7.5, 5.5))
wedges, texts = ax.pie(
    sizes, labels=labels, colors=colors, startangle=90,
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=11),
)
ax.set_title("裕元集团 2024 财年营业收入结构 (总计 US$8,182M)", pad=20)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_revenue_mix.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- Chart 3: Manufacturing geographic production split ----------
prod_labels = ["印尼 54%", "越南 31%", "中国大陆 11%", "其他 (柬埔寨/缅甸/孟加拉) 4%"]
prod_sizes = [54, 31, 11, 4]
prod_colors = ["#e377c2", "#1f77b4", "#d62728", "#bcbd22"]

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.pie(prod_sizes, labels=prod_labels, colors=prod_colors,
       autopct="%1.0f%%", startangle=140,
       wedgeprops=dict(edgecolor="white", linewidth=2),
       textprops=dict(fontsize=11))
ax.set_title("裕元集团 2024 鞋类出货量地理分布 (总 255.3M 双)", pad=20)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_production_geo.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- Chart 4: Customer destination revenue 2023 vs 2024 ----------
dest = ["中国", "美国", "欧洲", "亚洲其他", "其他"]
fy24 = [3580.3, 1542.0, 1429.6, 1174.5, 455.7]
fy23 = [3703.8, 1408.2, 1287.0, 1058.1, 433.0]

x = np.arange(len(dest))
width = 0.38
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(x - width / 2, fy23, width, label="2023", color="#aec7e8")
ax.bar(x + width / 2, fy24, width, label="2024", color="#1f77b4")
ax.set_xticks(x)
ax.set_xticklabels(dest)
ax.set_ylabel("营业收入 (US$ M)")
ax.set_title("裕元集团 按客户交付目的地划分的营业收入 (2023 vs 2024)")
ax.legend()
for i, (a, b) in enumerate(zip(fy23, fy24)):
    ax.text(i - width / 2, a + 50, f"{a:,.0f}", ha="center", fontsize=8, color="#444")
    ax.text(i + width / 2, b + 50, f"{b:,.0f}", ha="center", fontsize=8, color="#1f77b4")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_geo_revenue.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- Chart 5: Manufacturing volume + ASP ----------
years5 = ["2020", "2021", "2022", "2023", "2024"]
volume = [243.5, 261.0, 245.0, 218.3, 255.3]  # million pairs
asp = [20.20, 19.49, 21.34, 21.34, 20.25]  # USD per pair (2020-2024 reported)

fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
ax1.bar(years5, volume, color="#2ca02c", alpha=0.8, label="鞋类出货量 (百万双)")
ax1.set_ylabel("鞋类出货量 (百万双)", color="#2ca02c")
ax1.tick_params(axis="y", labelcolor="#2ca02c")
for i, v in enumerate(volume):
    ax1.text(i, v + 3, f"{v:.1f}", ha="center", fontsize=9, color="#2ca02c")

ax2 = ax1.twinx()
ax2.spines["top"].set_visible(False)
ax2.plot(years5, asp, color="#ff7f0e", marker="s", linewidth=2, label="平均售价 (US$/双)")
ax2.set_ylabel("平均售价 (US$/双)", color="#ff7f0e")
ax2.tick_params(axis="y", labelcolor="#ff7f0e")
ax2.set_ylim(18, 23)
for i, v in enumerate(asp):
    ax2.text(i, v + 0.15, f"${v:.2f}", ha="center", fontsize=9, color="#ff7f0e")

plt.title("裕元集团 制造业务出货量与平均售价 (2020-2024)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_volume_asp.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------- Chart 6: Peer valuation comparison ----------
peers = ["裕元\n0551.HK", "丰泰\nTWSE:9910", "Stella Int'l\n1836.HK", "宝胜\n3813.HK", "宝成 (母)\nTWSE:9904"]
pe = [8.3, 19.5, 8.4, 14.5, 8.7]      # rough TTM
ps = [0.39, 1.8, 0.85, 0.45, 0.35]    # rough TTM

x = np.arange(len(peers))
fig, ax1 = plt.subplots(figsize=(9, 4.8))
bars1 = ax1.bar(x - 0.2, pe, 0.4, color="#1f77b4", label="TTM P/E")
ax1.set_ylabel("TTM P/E (倍)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_xticks(x)
ax1.set_xticklabels(peers, fontsize=10)
for b, v in zip(bars1, pe):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v:.1f}x", ha="center", fontsize=9, color="#1f77b4")

ax2 = ax1.twinx()
ax2.spines["top"].set_visible(False)
bars2 = ax2.bar(x + 0.2, ps, 0.4, color="#d62728", label="TTM P/S")
ax2.set_ylabel("TTM P/S (倍)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
for b, v in zip(bars2, ps):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.2f}x", ha="center", fontsize=9, color="#d62728")

plt.title("裕元 vs 同业估值倍数 (TTM)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "yueyuen_peer_valuation.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

print("All charts saved.")
