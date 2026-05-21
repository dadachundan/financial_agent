"""Generate charts for 精锋医疗 (HKEX:2675) company-research report.
Data sourced from prospectus (2025-12-30) and Frost & Sullivan industry report cited therein.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

# Use a CJK-capable font for tick labels
for font in ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS", "STHeiti"]:
    try:
        mpl.font_manager.findfont(font, fallback_to_default=False)
        mpl.rcParams["font.sans-serif"] = [font]
        break
    except Exception:
        continue
mpl.rcParams["axes.unicode_minus"] = False

OUT = "/Users/x/projects/financial_agent/reports/charts"
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(p)


# ---------- 1. Revenue + gross margin (2023, 2024, 1H24, 1H25) ----------
fig, ax1 = plt.subplots(figsize=(8, 4.5))
periods = ["2023", "2024", "1H2024", "1H2025"]
rev = [48.0, 160.0, 30.2, 149.4]  # RMB mn
gm = [59.3, 61.3, 63.3, 62.8]  # %
x = np.arange(len(periods))
bars = ax1.bar(x, rev, color="#1f77b4", width=0.55, label="收入 (人民币百万元)")
ax1.set_xticks(x)
ax1.set_xticklabels(periods)
ax1.set_ylabel("收入 (人民币百万元)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax1.set_ylim(0, 200)
for b, v in zip(bars, rev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 4, f"{v:.1f}", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(x, gm, color="#d62728", marker="o", linewidth=2, label="毛利率 (%)")
ax2.set_ylabel("毛利率 (%)", color="#d62728")
ax2.tick_params(axis="y", labelcolor="#d62728")
ax2.set_ylim(50, 70)
for xi, v in zip(x, gm):
    ax2.text(xi, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9, color="#d62728")
plt.title("精锋医疗 收入与毛利率 (2023 — 2025H1)")
fig.tight_layout()
save(fig, "jingfeng_revenue_gm.png")


# ---------- 2. R&D expense + net loss ----------
fig, ax = plt.subplots(figsize=(8, 4.5))
rd = [171.2, 226.2, 95.6, 96.5]
loss = [212.9, 218.5, 132.6, 89.1]
w = 0.36
ax.bar(x - w / 2, rd, w, color="#2ca02c", label="研发开支")
ax.bar(x + w / 2, loss, w, color="#7f7f7f", label="净亏损")
ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.set_ylabel("人民币百万元")
ax.set_title("研发开支 vs. 净亏损")
ax.legend()
for xi, v in zip(x - w / 2, rd):
    ax.text(xi, v + 4, f"{v:.0f}", ha="center", fontsize=8)
for xi, v in zip(x + w / 2, loss):
    ax.text(xi, v + 4, f"{v:.0f}", ha="center", fontsize=8)
fig.tight_layout()
save(fig, "jingfeng_rd_loss.png")


# ---------- 3. Revenue by geography 1H25 ----------
fig, ax = plt.subplots(figsize=(6, 4.5))
labels = ["中国 (59.4%)", "欧盟 (16.3%)", "其他国家 (24.3%)"]
vals = [88.7, 24.3, 36.4]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
ax.pie(vals, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
ax.set_title("2025上半年 — 收入地域分布 (RMB mn)")
fig.tight_layout()
save(fig, "jingfeng_revenue_geo.png")


# ---------- 4. China surgical robotics TAM (Frost & Sullivan) ----------
fig, ax = plt.subplots(figsize=(9, 4.5))
yrs = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033]
total = [2714.9, 2934.5, 4192.5, 4473.4, 5931.7, 7184.2, 10185.3, 13594.4, 19311.8, 26866.4, 36595.7, 50750.3, 63260.4, 76688.5, 102018.7]
endo = [2022.6, 2218.0, 3241.3, 3117.7, 3662.9, 4185.5, 5541.9, 6692.7, 8684.8, 11172.6, 14552.8, 19551.7, 25339.1, 32125.5, 40542.9]
ax.bar(yrs, total, color="#bbbbbb", label="中国手术机器人 全行业")
ax.bar(yrs, endo, color="#1f77b4", label="腔镜手术机器人 细分")
ax.set_ylabel("市场规模 (人民币百万元)")
ax.set_title("中国手术机器人市场 — 历史与预测 (2019-2033)")
ax.legend(loc="upper left")
ax.set_xticks(yrs[::2])
fig.tight_layout()
save(fig, "jingfeng_tam.png")


# ---------- 5. Cornerstone investors ----------
fig, ax = plt.subplots(figsize=(8, 5))
inv = ["ADIA", "Tencent\n(Huang River)", "UBS AM\nSingapore", "GBA Homeland\n(Mega Prime+Poly)", "OrbiMed\nGenesis", "华夏基金\n(香港)", "LYFE Capital", "Millennium\n(ICSA)", "其他基石"]
amt = [15.0, 10.0, 10.0, 10.0, 9.0, 8.0, 6.0, 5.0, 27.0]
colors2 = plt.cm.tab20.colors[:len(inv)]
ax.barh(inv[::-1], amt[::-1], color=list(colors2)[::-1])
for i, v in enumerate(amt[::-1]):
    ax.text(v + 0.3, i, f"US${v:.1f}M", va="center", fontsize=9)
ax.set_xlabel("认购金额 (百万美元)")
ax.set_title("精锋医疗 基石投资者认购额 (按发售价 HK$43.24)")
fig.tight_layout()
save(fig, "jingfeng_cornerstone.png")


# ---------- 6. Use of IPO proceeds ----------
fig, ax = plt.subplots(figsize=(7, 5))
buckets = [
    "核心产品 R&D",
    "核心产品商业化",
    "运营资金 / 一般用途",
    "扩大产能",
    "战略收购 / 投资",
    "其他产品在研",
]
pct = [42.0, 20.0, 11.5, 10.5, 10.0, 6.0]
colors3 = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
ax.pie(pct, labels=[f"{b}\n{p}%" for b, p in zip(buckets, pct)], colors=colors3, startangle=90)
ax.set_title("IPO 募资净额 11.166 亿港元 — 用途分配")
fig.tight_layout()
save(fig, "jingfeng_use_of_proceeds.png")


# ---------- 7. Peer valuation snapshot ----------
fig, ax = plt.subplots(figsize=(8, 4.5))
peers = ["精锋医疗\n2675.HK", "微创机器人\n2252.HK", "Intuitive\nSurgical\nISRG", "术锐\n(未上市)"]
ps = [88.0, 39.7, 22.0, None]  # est. TTM P/S; 术锐 not available
mc = [262.0, 110.0, 1900.0 * 7.78, None]  # market cap HK$ bn (Intuitive ~US$190 bn × 7.78)
# Plot only P/S where available
peers_ps = ["精锋医疗\n2675.HK", "微创机器人\n2252.HK", "Intuitive\nSurgical\nISRG"]
psv = [88.0, 39.7, 22.0]
bars = ax.bar(peers_ps, psv, color=["#d62728", "#1f77b4", "#2ca02c"])
ax.set_ylabel("TTM P/S (x)")
ax.set_title("同行 P/S 比较 — 截至 2026-01 月底")
for b, v in zip(bars, psv):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}×", ha="center", fontsize=10)
fig.tight_layout()
save(fig, "jingfeng_peers_ps.png")


# ---------- 8. Patent portfolio ----------
fig, ax = plt.subplots(figsize=(8, 4.5))
cats = ["中国\n已授权", "中国\n申请中", "海外\n已授权", "海外\n申请中"]
n = [453, 213, 13, 55]
colors4 = ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78"]
bars = ax.bar(cats, n, color=colors4)
for b, v in zip(bars, n):
    ax.text(b.get_x() + b.get_width() / 2, v + 8, str(v), ha="center", fontsize=10)
ax.set_ylabel("项数")
ax.set_title("精锋医疗 全球专利组合 — 截至 2025-12 (合计 734 项)")
fig.tight_layout()
save(fig, "jingfeng_patents.png")


print("DONE")
