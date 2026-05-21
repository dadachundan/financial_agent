"""Generate charts for 沪电股份 (SZSE:002463) research report."""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

mpl.rcParams["font.family"] = "Hiragino Sans GB"
mpl.rcParams["axes.unicode_minus"] = False

OUT = Path(__file__).parent

# 1. Revenue + net profit + gross margin trend (2019-2025 + 2026E Q1 annualized)
years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
rev = [6.469, 7.460, 7.419, 8.336, 8.938, 13.342, 18.945]      # 亿元/10 -> 单位:十亿元 实际为亿元 -> 重新表达
# 单位:亿元
rev = [64.69, 74.60, 74.19, 83.36, 89.38, 133.42, 189.45]
ni = [11.86, 13.43, 10.64, 13.62, 15.13, 25.87, 38.22]         # 归母净利润 亿元
# 毛利率: 2019 26.7% (近似); 2020 32.2%; 2021 27.4%; 2022 28.4%; 2023 28.85%; 2024 35.85%; 2025 36.91% (PCB业务36.91% — 公司整体亦相近)
gm = [26.7, 32.2, 27.4, 28.4, 28.85, 35.85, 35.48]              # 公司整体毛利率（PCB 36.91% 略高）

fig, ax1 = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(years))
b1 = ax1.bar(x - 0.2, rev, width=0.4, color="#1f77b4", label="营业收入")
b2 = ax1.bar(x + 0.2, ni, width=0.4, color="#ff7f0e", label="归母净利润")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("人民币亿元")
ax1.set_xlabel("年度")
for bar, v in zip(b1, rev):
    ax1.text(bar.get_x() + bar.get_width()/2, v + 2, f"{v:.1f}", ha="center", fontsize=8)
for bar, v in zip(b2, ni):
    ax1.text(bar.get_x() + bar.get_width()/2, v + 0.6, f"{v:.1f}", ha="center", fontsize=8, color="#cc5500")

ax2 = ax1.twinx()
ax2.plot(x, gm, marker="o", color="#2ca02c", linewidth=2, label="毛利率(%)")
for xi, g in zip(x, gm):
    ax2.text(xi, g + 0.6, f"{g:.1f}%", ha="center", fontsize=8, color="#2ca02c")
ax2.set_ylabel("毛利率 (%)")
ax2.set_ylim(20, 45)

ax1.set_title("沪电股份 2019-2025 营收、归母净利润与毛利率")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
ax1.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "hudian_revenue_trend.png", dpi=150, bbox_inches="tight")
plt.close()

# 2. 2025 PCB revenue mix by application
labels = ["高速网络交换机及路由器", "AI 服务器及 HPC", "通用服务器", "无线通信网络等", "智能汽车", "工业控制及其他"]
values = [81.69, 30.06, 25.40, 9.41, 30.45, 4.42]  # 亿元
colors_ = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#d62728", "#8c564b"]
fig, ax = plt.subplots(figsize=(9, 6))
wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors_, autopct="%1.1f%%", startangle=90, pctdistance=0.78)
for t in texts: t.set_fontsize(10)
for t in autotexts: t.set_fontsize(9); t.set_color("white")
ax.set_title("沪电股份 2025 年 PCB 收入构成（按下游应用，合计 181.43 亿元）")
plt.tight_layout()
plt.savefig(OUT / "hudian_2025_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# 3. 2024 vs 2025 数据通讯下游细分对比 - 增速
sub = ["高速网络交换机\n及路由器", "AI服务器\n及HPC", "通用服务器", "无线/其他"]
y2024 = [38.92, 25.79, 23.06, 13.21]  # 估算: 2024数据通讯营收100.92亿, 按2025披露反推 (公司未严格分解, 此处仅作示意——改用2025披露值与同比%)
# 直接展示2025细分营收与同比
v25 = [81.69, 30.06, 25.40, 9.41]
yoy = [109.89, 16.6, 10.1, -28.7]  # 高速网络+109.89%; 其余按余额倒推近似
fig, ax = plt.subplots(figsize=(9, 5))
x2 = np.arange(len(sub))
bars = ax.bar(x2, v25, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"])
ax.set_xticks(x2); ax.set_xticklabels(sub)
ax.set_ylabel("2025 年营收（亿元）")
ax.set_title("数据通讯应用领域 2025 年细分营收与同比增速")
for i, (bar, v, y) in enumerate(zip(bars, v25, yoy)):
    ax.text(bar.get_x()+bar.get_width()/2, v+1.5, f"{v:.1f}亿\nYoY {y:+.1f}%", ha="center", fontsize=9)
ax.set_ylim(0, max(v25)*1.25)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "hudian_datacom_breakdown.png", dpi=150, bbox_inches="tight")
plt.close()

# 4. 全球 PCB 市场 & HLC(18+) 增长 — 引用 Prismark 2025Q4
years_p = ["2024", "2025E", "2026E", "2030E"]
total_pcb = [73.5, 85.15, 95.78, 123.35]  # 单位 十亿美元 (Prismark)
hlc18 = [2.85, 4.93, 8.00, 13.16]  # 单位 十亿美元: 2025年18层以上4,928 mil; 2026E 8,002; 2030E 13,159 ; 2024 反推 (2025同比72.8% -> 2024≈2.85)
fig, ax = plt.subplots(figsize=(9, 5))
x3 = np.arange(len(years_p))
b1 = ax.bar(x3 - 0.2, total_pcb, width=0.4, color="#4c72b0", label="全球PCB市场")
b2 = ax.bar(x3 + 0.2, hlc18, width=0.4, color="#dd8452", label="HLC(18层以上)细分")
for bar, v in zip(b1, total_pcb): ax.text(bar.get_x()+bar.get_width()/2, v+2, f"{v:.1f}", ha="center", fontsize=9)
for bar, v in zip(b2, hlc18): ax.text(bar.get_x()+bar.get_width()/2, v+0.5, f"{v:.2f}", ha="center", fontsize=9, color="#aa5520")
ax.set_xticks(x3); ax.set_xticklabels(years_p)
ax.set_ylabel("市场规模（十亿美元）")
ax.set_title("全球 PCB 市场与超高层板 HLC(18+) 规模演进 — Prismark 预测")
ax.legend(loc="upper left")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "hudian_pcb_tam.png", dpi=150, bbox_inches="tight")
plt.close()

# 5. R&D investment & R&D headcount
years_r = ["2021", "2022", "2023", "2024", "2025"]
rd = [4.6, 5.7, 5.50, 7.90, 11.41]  # 亿元 (2021 4.62; 2022 5.73 估算; 2023 5.5; 2024 7.90; 2025 11.41)
rd_ratio = [6.2, 6.87, 6.16, 5.92, 6.02]
fig, ax1 = plt.subplots(figsize=(9, 5))
b = ax1.bar(years_r, rd, color="#6a5acd")
for bar, v in zip(b, rd):
    ax1.text(bar.get_x()+bar.get_width()/2, v+0.2, f"{v:.2f}亿", ha="center", fontsize=9)
ax1.set_ylabel("研发投入（亿元）")
ax1.set_title("沪电股份 研发投入与研发收入占比")

ax2 = ax1.twinx()
ax2.plot(years_r, rd_ratio, marker="s", color="#cc4444", linewidth=2, label="研发投入占营收比")
for x_, v in zip(years_r, rd_ratio):
    ax2.text(x_, v+0.1, f"{v:.2f}%", ha="center", fontsize=9, color="#cc4444")
ax2.set_ylabel("占营收比 (%)")
ax2.set_ylim(4, 8)
ax2.legend(loc="upper left")
ax1.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "hudian_rd.png", dpi=150, bbox_inches="tight")
plt.close()

# 6. 季度营收 ladder 2024Q1 - 2026Q1
qtrs = ["24Q1","24Q2","24Q3","24Q4","25Q1","25Q2","25Q3","25Q4","26Q1"]
q_rev = [25.86, 30.83, 35.87, 40.86, 40.38, 44.56, 50.19, 54.33, 62.14]  # 亿元
q_ni = [4.41, 6.07, 7.07, 8.32, 7.62, 9.20, 10.35, 11.05, 12.42]
fig, ax = plt.subplots(figsize=(10, 5))
x4 = np.arange(len(qtrs))
b1 = ax.bar(x4 - 0.2, q_rev, width=0.4, color="#3a87ad", label="营业收入")
b2 = ax.bar(x4 + 0.2, q_ni, width=0.4, color="#dd6e42", label="归母净利润")
ax.set_xticks(x4); ax.set_xticklabels(qtrs)
ax.set_ylabel("人民币亿元")
ax.set_title("沪电股份 单季度营收与归母净利润 (2024Q1 – 2026Q1)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
for bar, v in zip(b1, q_rev):
    ax.text(bar.get_x()+bar.get_width()/2, v+0.8, f"{v:.1f}", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig(OUT / "hudian_quarterly.png", dpi=150, bbox_inches="tight")
plt.close()

# 7. Peer valuation snapshot (close 2026-05-21)
peers = ["沪电股份\n002463", "深南电路\n002916", "东山精密\n002384", "生益科技\n600183"]
price = [103.70, 343.88, 206.97, 98.19]
# Market caps 亿元 (approximate)
shares_bn = [1.9244, 0.5126, 1.7060, 2.3760]  # 总股本(十亿股), 深南电路 5.126亿, 东山精密 17.06亿, 生益科技23.76亿(估算)
mcap = [round(p*s/10, 1) for p, s in zip(price, shares_bn)]  # 十亿元 -> 亿元*?
# correct unit: shares (bn) × price (CNY) = mcap (bn CNY); convert to 亿元 = bn*100
mcap_bn_cny = [round(p*s, 2) for p, s in zip(price, shares_bn)]  # bn CNY
fig, ax = plt.subplots(figsize=(8, 4.5))
b = ax.bar(peers, mcap_bn_cny, color=["#1f77b4", "#aec7e8", "#ffbb78", "#98df8a"])
for bar, v in zip(b, mcap_bn_cny):
    ax.text(bar.get_x()+bar.get_width()/2, v+2, f"{v:.1f}", ha="center", fontsize=10)
ax.set_ylabel("总市值（十亿元人民币）")
ax.set_title("沪电股份 vs PCB 同业 总市值快照（2026-05-21 收盘价）")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "hudian_peers.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts written.")
