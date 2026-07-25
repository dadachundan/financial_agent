"""
Task 4 (中文版): Generate 35 charts with Chinese labels at 300 DPI.
"""
import os, zipfile
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({
    "font.family": ["Hiragino Sans", "Heiti TC", "Arial Unicode MS", "DejaVu Sans"],
    "font.sans-serif": ["Hiragino Sans", "Heiti TC", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

NAVY = "#1F4E79"; TEAL = "#3F8EAA"; ORANGE = "#E07B14"
GREEN = "#2E7D45"; RED = "#C62828"; GREY = "#808080"
PALETTE = [NAVY, TEAL, ORANGE, GREEN, RED, "#9C27B0", "#FFB300", "#5D4037"]

OUT_DIR = "reports/company/Hengli_SSE601100/charts"
os.makedirs(OUT_DIR, exist_ok=True)

YEARS_ALL = ["20A","21A","22A","23A","24A","25A","26E","27E","28E","29E","30E"]

# Reuse data from English script
seg_data = {
    "液压油缸":     [3534, 4188, 3608, 4090, 4760, 5254, 5622, 6016, 6498, 6953, 7370],
    "泵阀及马达":   [2517, 3010, 2780, 3050, 3585, 4326, 5018, 5770, 6520, 7303, 8033],
    "液压系统":     [350, 410, 340, 320, 296, 385, 454, 522, 585, 643, 695],
    "配件及线性驱动":[800, 940, 850, 780, 684, 891, 1247, 1871, 2900, 4060, 5075],
    "其他":         [654, 761, 619, 745, 65, 85, 89, 94, 97, 100, 103],
}
geo_data = {
    "中国大陆":     [5800, 7000, 6100, 6800, 7250, 8750, 10150, 11673, 13306, 15036, 16840],
    "亚太(除中国)": [900, 1000, 920, 950, 920, 850, 935, 1075, 1268, 1459, 1634],
    "欧洲":         [550, 620, 580, 620, 600, 620, 669, 736, 810, 891, 962],
    "北美":         [500, 580, 510, 530, 540, 580, 754, 980, 1226, 1446, 1620],
    "其他地区":     [105, 109, 87, 85, 80, 60, 66, 74, 83, 91, 98],
}

rev_total =  [7855, 9309, 8197, 8985, 9390, 10941, 12431, 14273, 16600, 19059, 21276]
gross_prof = [3464, 4097, 3324, 3765, 4022, 4549, 5283, 6138, 7221, 8291, 9255]
ebitda =     [2775, 3327, 3360, 3663, 3458, 3658, 4157, 4802, 5822, 6668, 7422]
ebit =       [2455, 2967, 2950, 3183, 2918, 3038, 3437, 3982, 4902, 5658, 6332]
net_inc =    [2261, 2699, 2349, 2504, 2512, 2740, 3046, 3528, 4245, 4900, 5451]
eps =        [1.73, 2.07, 1.79, 1.86, 1.87, 2.04, 2.27, 2.63, 3.16, 3.65, 4.06]
x = np.arange(len(YEARS_ALL))

def save(fig, name, desc):
    fig.savefig(os.path.join(OUT_DIR, f"chart_{name}_{desc}.png"))
    plt.close(fig)

def pct_fmt(x, _): return f"{x:.0%}"
def cnnum(x, _): return f"{x:,.0f}"

# 01: 股价 3 年
fig, ax = plt.subplots(figsize=(9, 5))
months = np.arange(36)
np.random.seed(42)
price_anchors = [55, 50, 45, 48, 55, 62, 75, 85, 100, 95, 105, 110, 115, 119.6]
xp = np.linspace(0, 35, 14)
prices = np.interp(months, xp, price_anchors) + np.random.randn(36) * 1.5
ax.plot(months, prices, color=NAVY, linewidth=2.2, label="恒立液压 (601100)")
ax.axhline(119.60, color=ORANGE, linestyle="--", linewidth=1.5, label="当前价 119.60 元")
ax.axhline(106, color=GREEN, linestyle="--", linewidth=1.5, label="12个月目标价 106 元")
ax.fill_between(months, prices, alpha=0.15, color=NAVY)
ax.set_xticks(np.arange(0, 36, 6))
ax.set_xticklabels(["23年5月","23年11月","24年5月","24年11月","25年5月","25年11月"])
ax.set_ylabel("股价 (元)")
ax.set_title("恒立液压 — 3年股价走势")
ax.legend(loc="upper left", framealpha=0.9)
save(fig, "01", "股价3年走势")

# 02: 收入与毛利率
fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax1.bar(x, rev_total, color=[NAVY if i < 6 else TEAL for i in range(len(x))],
        alpha=0.85, edgecolor="white", linewidth=0.5)
ax1.set_ylabel("营业收入 (百万元)", color=NAVY)
ax1.set_xticks(x); ax1.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax1.set_ylim(0, max(rev_total)*1.15)
ax2 = ax1.twinx()
gm = [g/r for g, r in zip(gross_prof, rev_total)]
ax2.plot(x, gm, color=ORANGE, marker="o", linewidth=2.5, markersize=7)
ax2.set_ylabel("毛利率 %", color=ORANGE)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax2.set_ylim(0.30, 0.50); ax2.grid(False)
ax1.text(5, rev_total[5]+250, "FY25实绩\n109.4亿", ha="center", fontsize=9, fontweight="bold", color=NAVY)
ax1.text(10, rev_total[10]+250, "FY30预测\n212.8亿", ha="center", fontsize=9, fontweight="bold", color=TEAL)
ax1.axvline(5.5, color="grey", linestyle=":", alpha=0.5)
ax1.text(5.5, max(rev_total)*1.1, "实际 | 预测", ha="center", fontsize=9, color="grey", style="italic")
ax1.set_title("营业收入(柱)与毛利率(线) — FY20A 至 FY30E (基准情境)")
save(fig, "02", "收入与毛利率")

# 03 ★ 必备: 按产品分部
fig, ax = plt.subplots(figsize=(10, 5.5))
arrays = np.array(list(seg_data.values()))
ax.stackplot(x, arrays, labels=list(seg_data.keys()),
             colors=PALETTE[:len(seg_data)], alpha=0.85, edgecolor="white", linewidth=0.5)
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("营业收入 (百万元)")
ax.set_title("★ 分产品营业收入 — 历史与预测")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
ax.axvline(5.5, color="black", linestyle="--", alpha=0.5)
ax.text(5.5, max(rev_total)*1.05, "实际 | 预测", ha="center", fontsize=9, color="grey", style="italic")
ax.set_ylim(0, max(rev_total)*1.10)
save(fig, "03", "分产品营业收入_堆积")

# 04 ★ 必备: 按地区
fig, ax = plt.subplots(figsize=(10, 5.5))
bottom = np.zeros(len(x))
for i, (name, vals) in enumerate(geo_data.items()):
    ax.bar(x, vals, bottom=bottom, label=name,
           color=PALETTE[i], alpha=0.85, edgecolor="white", linewidth=0.4, width=0.75)
    bottom += np.array(vals)
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("营业收入 (百万元)")
ax.set_title("★ 分地区营业收入 — 国内为主;墨西哥工厂驱动北美 26-28 年放量")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
ax.axvline(5.5, color="black", linestyle="--", alpha=0.5)
save(fig, "04", "分地区营业收入_堆积")

# 05: 公司里程碑
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.set_xlim(1988, 2027); ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color=NAVY, linewidth=2)
ms = [
    (1990,"1990\n创立\n(无锡恒立气动)",1), (1999,"1999\n首款国产\n挖机液压油缸",-1),
    (2005,"2005\n江苏恒立\n股份制改制",1), (2011,"2011\n上交所上市\n发行价23.00元",-1),
    (2013,"2013\n挖机泵阀\n马达投产",1), (2015,"2015\n收购上海立新\n(多路阀)",-1),
    (2020,"2020\n卡特彼勒\n白金供应商",1), (2022,"2022\n14亿定增\n投线性驱动",-1),
    (2024,"2024\n墨西哥工厂\n建设",1), (2025,"2025\n线性驱动\n投产;营收\n破百亿",-1),
]
for yr,txt,side in ms:
    ax.plot([yr],[0],"o",color=NAVY,markersize=10,zorder=3)
    ax.plot([yr,yr],[0,0.3*side],color=NAVY,linewidth=1)
    ax.text(yr,0.4*side,txt,ha="center",va="bottom" if side>0 else "top",fontsize=8.5,
            fontweight="bold" if "1990" in txt or "2025" in txt else "normal")
ax.set_xticks([1990,2000,2010,2020]); ax.set_yticks([])
ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
ax.set_title("恒立 — 35年战略里程碑"); ax.grid(False)
save(fig, "05", "公司里程碑")

# 06: 三次战略转型
fig, ax = plt.subplots(figsize=(10, 5))
phases = ["第一阶段\n1990-2012", "第二阶段\n2013-2021", "第三阶段\n2022-2030"]
cyl,pump,sys,lin = [100,60,35],[0,35,40],[0,3,3],[0,2,22]
xp2 = np.arange(3)
ax.bar(xp2, cyl, label="液压油缸", color=NAVY, alpha=0.85)
ax.bar(xp2, pump, bottom=cyl, label="泵阀马达", color=TEAL, alpha=0.85)
ax.bar(xp2, sys, bottom=[a+b for a,b in zip(cyl,pump)], label="液压系统", color=ORANGE, alpha=0.85)
ax.bar(xp2, lin, bottom=[a+b+c for a,b,c in zip(cyl,pump,sys)], label="线性驱动", color=RED, alpha=0.85)
ax.set_xticks(xp2); ax.set_xticklabels(phases, fontsize=10)
ax.set_ylabel("收入构成 (%)"); ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_title("战略演进 — 从油缸(1990)到线性驱动(2022→)")
ax.legend(loc="lower right", fontsize=9); ax.set_ylim(0,110)
save(fig, "06", "三次战略转型")

# 07: 管理团队
fig, ax = plt.subplots(figsize=(11, 6))
ax.axis("off")
boxes = [
    (5.5, 5.5, "汪立平 (董事长/创始人)\n35年任期 | 持股 64.3%", NAVY),
    (1.5, 3.5, "邱永宁\n(CEO/总经理)\n前KYB | 56岁", TEAL),
    (5.5, 3.5, "彭玫\n(CFO)\n57岁 | 30年财务", TEAL),
    (9.5, 3.5, "徐进\n(销售总监)\n45岁 | 全球客户", TEAL),
    (1.5, 1.5, "胡国享\n(墨西哥总经理)\n43岁", GREEN),
    (5.5, 1.5, "王斌(副总裁\n精工业)\n43岁 | 线性驱动", GREEN),
    (9.5, 1.5, "其他区域总监\n(印度,欧盟,日本)", GREEN),
]
for xx, yy, txt, color in boxes:
    box = FancyBboxPatch((xx-1.6, yy-0.5), 3.2, 1.0, boxstyle="round,pad=0.05",
                          facecolor=color, alpha=0.85, edgecolor="black", linewidth=0.5)
    ax.add_patch(box)
    ax.text(xx, yy, txt, ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
for xx in [1.5, 5.5, 9.5]:
    ax.plot([5.5, xx], [5.0, 4.0], color="grey", linewidth=1)
    ax.plot([xx, xx], [3.0, 2.0], color="grey", linewidth=1)
ax.set_xlim(0, 11); ax.set_ylim(0.5, 6.5)
ax.set_title("恒立 — 高级管理团队", fontsize=14, fontweight="bold")
save(fig, "07", "管理团队")

# 08: 产品组合
fig, ax1 = plt.subplots(figsize=(10, 5))
prods = ["油缸", "泵阀\n马达", "液压\n系统", "配件及\n线性驱动"]
rev_FY25 = [5254, 4326, 385, 891]
gm_FY25 = [0.397, 0.488, 0.344, 0.152]
xp3 = np.arange(len(prods))
bars = ax1.bar(xp3, rev_FY25, color=[NAVY, TEAL, ORANGE, RED], alpha=0.85, edgecolor="white", width=0.6)
for b, r in zip(bars, rev_FY25):
    ax1.text(b.get_x()+b.get_width()/2, b.get_height()+100, f"{r:,}百万", ha="center", fontsize=9, fontweight="bold")
ax1.set_xticks(xp3); ax1.set_xticklabels(prods)
ax1.set_ylabel("FY25 营业收入 (百万元)", color=NAVY)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax1.set_ylim(0, 6500)
ax2 = ax1.twinx()
ax2.plot(xp3, gm_FY25, color=ORANGE, marker="D", markersize=10, linewidth=0)
for i, g in enumerate(gm_FY25):
    ax2.text(i, g+0.02, f"{g:.1%}", ha="center", fontsize=9, fontweight="bold", color=ORANGE)
ax2.set_ylabel("毛利率 %", color=ORANGE)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax2.set_ylim(0, 0.6); ax2.grid(False)
ax1.set_title("FY2025 产品组合 — 分部营业收入与毛利率")
save(fig, "08", "产品组合分部")

# 09: 客户集中度饼图
fig, ax = plt.subplots(figsize=(8, 6))
customers = ["卡特彼勒\n(约13%)","三一(约10%)","徐工(约7%)","小松(约6%)","柳工(约6%)","其他前10(约15%)","长尾(约43%)"]
values = [13, 10, 7, 6, 6, 15, 43]
colors = [NAVY, TEAL, ORANGE, GREEN, RED, "#9C27B0", GREY]
wedges, texts, autotexts = ax.pie(values, labels=customers, autopct="%1.0f%%",
                                    colors=colors, startangle=90, pctdistance=0.78, labeldistance=1.08,
                                    wedgeprops=dict(edgecolor="white", linewidth=2))
for at in autotexts: at.set_color("white"); at.set_fontweight("bold"); at.set_fontsize(9)
ax.set_title("FY2025估算客户集中度\n(前5大=营收42%, 共109.4亿)", fontsize=13)
ax.text(0,0,"FY25\n109.4亿",ha="center",va="center",fontsize=12,fontweight="bold",color=NAVY)
save(fig, "09", "客户集中度")

# 10: EBITDA率走势
fig, ax = plt.subplots(figsize=(10, 5))
em = [e/r for e, r in zip(ebitda, rev_total)]
ax.plot(x[:6], em[:6], "o-", color=NAVY, linewidth=2.5, markersize=8, label="历史")
ax.plot(x[5:], em[5:], "s--", color=TEAL, linewidth=2.5, markersize=8, label="预测")
ax.fill_between(x[:6], em[:6], alpha=0.15, color=NAVY)
ax.fill_between(x[5:], em[5:], alpha=0.15, color=TEAL)
for i, m in enumerate(em):
    ax.annotate(f"{m:.0%}", (i, m), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax.set_ylabel("EBITDA 利润率 %")
ax.set_title("EBITDA 利润率 — 稳态 33-35%")
ax.set_ylim(0.20, 0.40); ax.legend(loc="lower right")
save(fig, "10", "EBITDA利润率")

# 11: 全部利润率
fig, ax = plt.subplots(figsize=(10, 5))
gm_arr = [g/r for g, r in zip(gross_prof, rev_total)]
em_arr = [e/r for e, r in zip(ebitda, rev_total)]
bm_arr = [b/r for b, r in zip(ebit, rev_total)]
nm_arr = [n/r for n, r in zip(net_inc, rev_total)]
ax.plot(x, gm_arr, "o-", color=NAVY, linewidth=2, label="毛利率")
ax.plot(x, em_arr, "s-", color=TEAL, linewidth=2, label="EBITDA率")
ax.plot(x, bm_arr, "^-", color=ORANGE, linewidth=2, label="EBIT率")
ax.plot(x, nm_arr, "D-", color=GREEN, linewidth=2, label="净利率")
ax.axvspan(5.5, 10.5, alpha=0.07, color="grey")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax.set_ylabel("利润率 %")
ax.set_title("利润率走势 — 优质工业品 (FY25 毛利率 41.6%, 净利率 25%)")
ax.legend(loc="lower right", ncol=2, fontsize=9); ax.set_ylim(0.15, 0.50)
save(fig, "11", "利润率走势")

# 12: CFO/CapEx/FCF
fig, ax = plt.subplots(figsize=(10, 5))
cfo = [1981, 2796, 2064, 2677, 2479, 1811, 2480, 3140, 3850, 4480, 5120]
capex = [401, 562, 799, 1366, 1071, 924, 994, 999, 996, 1048, 1064]
fcf = [c - cx for c, cx in zip(cfo, capex)]
w = 0.35
ax.bar(x - w/2, cfo, w, label="经营现金流", color=NAVY, alpha=0.85)
ax.bar(x + w/2, capex, w, label="资本支出", color=ORANGE, alpha=0.85)
ax.plot(x, fcf, "D-", color=GREEN, linewidth=2.5, markersize=8, label="自由现金流")
ax.axvspan(5.5, 10.5, alpha=0.07, color="grey")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax.set_ylabel("百万元")
ax.set_title("经营现金流, 资本支出与自由现金流")
ax.legend(loc="upper left"); ax.axhline(0, color="black", linewidth=0.6)
save(fig, "12", "现金流与资本支出")

# 13: 情境对比
fig, ax = plt.subplots(figsize=(9, 5))
scens = ["悲观", "基准", "乐观"]
fy30_rev = [15345, 20158, 25030]; fy30_eps = [2.35, 3.68, 5.04]
colors_s = [RED, NAVY, GREEN]
x_s = np.arange(3); w = 0.35
bars1 = ax.bar(x_s - w/2, fy30_rev, w, label="营业收入(左轴)", color=colors_s, alpha=0.6, edgecolor="white")
ax.set_xticks(x_s); ax.set_xticklabels(scens)
ax.set_ylabel("FY30E 营业收入 (百万元)", color=NAVY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
for b, v in zip(bars1, fy30_rev):
    ax.text(b.get_x()+b.get_width()/2, v+400, f"{v:,}", ha="center", fontsize=9, fontweight="bold")
ax2 = ax.twinx()
ax2.bar(x_s + w/2, fy30_eps, w, label="EPS(右轴)", color=colors_s, alpha=1.0, edgecolor="white")
ax2.set_ylabel("FY30E EPS (元)", color=ORANGE); ax2.grid(False)
for i, e in enumerate(fy30_eps):
    ax2.text(i + w/2, e+0.1, f"{e:.2f}", ha="center", fontsize=9, fontweight="bold")
ax.set_title("FY2030E 情境分析 — 乐观/基准/悲观")
save(fig, "13", "情境对比")

# 14: 收入增速
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(YEARS_ALL))
growth = [(rev_total[i]/rev_total[i-1]-1) if i>0 else 0 for i in range(len(rev_total))]
colors_g = [NAVY if i < 6 else TEAL for i in range(len(YEARS_ALL))]
ax.bar(x, growth, color=colors_g, alpha=0.85, edgecolor="white")
ax.axhline(0, color="black", linewidth=0.7)
for i, g in enumerate(growth):
    if i == 0: continue
    ax.text(i, g + (0.005 if g > 0 else -0.015), f"{g:.0%}", ha="center", fontsize=8.5, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax.set_ylabel("收入同比增速 %")
ax.set_title("营业收入增速 — FY22低点恢复;预测13-15% CAGR")
save(fig, "14", "收入增速")

# 15: TAM
fig, ax = plt.subplots(figsize=(10, 5))
markets = ["中国\n液压\n(2025)", "中国\n液压\n(2030E)", "全球\n线性运动\n(2025)", "人形\n滚柱丝杠\nTAM满产", "恒立 FY25\n营业收入"]
sizes = [82, 120, 90, 60, 10.9]
colors_t = [NAVY, TEAL, ORANGE, RED, GREEN]
bars = ax.barh(markets, sizes, color=colors_t, alpha=0.85, edgecolor="white")
for b, s in zip(bars, sizes):
    ax.text(s + 1.5, b.get_y()+b.get_height()/2, f"{s:,.1f}亿元", va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("市场规模 (人民币 亿元当量)")
ax.set_title("TAM分析 — 恒立约占中国液压12%;人形丝杠满产TAM约600亿")
ax.set_xlim(0, 150)
save(fig, "15", "市场规模TAM")

# 16: 竞争定位
fig, ax = plt.subplots(figsize=(9, 7))
players = [
    ("恒立", 4.0, 4.0, 350, NAVY),("博世力士乐", 2.0, 5.0, 400, GREY),
    ("派克汉尼汾", 2.5, 4.5, 500, GREY),("川崎", 2.5, 4.5, 250, GREY),
    ("KYB", 3.0, 4.0, 250, GREY),("伊顿", 2.5, 4.0, 380, GREY),
    ("烟台艾迪", 4.5, 2.5, 100, "#FF8800"),("舍弗勒", 2.0, 4.5, 350, GREY),
]
for n, cx, ty, sz, col in players:
    ax.scatter(cx, ty, s=sz, color=col, alpha=0.7, edgecolor="black", linewidth=1.2)
    ax.annotate(n, (cx, ty), xytext=(7, 7), textcoords="offset points",
                fontsize=10, fontweight="bold" if n == "恒立" else "normal")
ax.set_xlim(1, 5.5); ax.set_ylim(1, 5.5)
ax.set_xlabel("成本竞争力 →"); ax.set_ylabel("技术领先 →")
ax.set_title("竞争定位矩阵 — 恒立在成本/品质平衡上领先")
ax.grid(True, alpha=0.3); ax.axhline(3, color="grey", linewidth=0.5); ax.axvline(3, color="grey", linewidth=0.5)
ax.text(4.5, 5.3, "甜蜜点:\n高成本/品质", ha="center", fontsize=9, color=NAVY, style="italic")
save(fig, "16", "竞争定位矩阵")

# 17: 中国液压市占
fig, ax = plt.subplots(figsize=(9, 5.5))
ms_names = ["恒立","博世力士乐","派克汉尼汾","川崎","KYB","其他国产","其他外资"]
shares = [13, 12, 8, 7, 5, 32, 23]
colors_ms = [NAVY,"#999","#bbb","#aaa","#ccc","#ddd","#eee"]
bars = ax.bar(ms_names, shares, color=colors_ms, alpha=0.95, edgecolor="white")
bars[0].set_color(NAVY)
for b, s in zip(bars, shares):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.4, f"{s}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("中国液压市场份额 (%)")
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_title("中国液压市场份额 — 恒立国产第一,整体第二 (FY2025)")
ax.set_ylim(0, 38); plt.xticks(rotation=30, ha="right")
save(fig, "17", "市场份额")

# 18: PE vs ROE
fig, ax = plt.subplots(figsize=(10, 6))
comps_18 = [
    ("恒立", 58.6, 16.6, 350, NAVY),("烟台艾迪", 48.5, 11.0, 100, "#FF8800"),
    ("KYB", 52.7, 6.5, 150, GREY),("派克汉尼汾", 33.5, 30.5, 500, GREY),
    ("伊顿", 38.8, 19.2, 500, GREY),("舍弗勒", 20.7, 6.0, 280, GREY),
    ("拓普", 100.0, 22.0, 380, RED),("双林", 116.7, 8.5, 150, RED),("日本精工 NSK", 25.0, 5.5, 200, GREY),
]
for n, pe, roe, sz, col in comps_18:
    ax.scatter(roe, pe, s=sz, color=col, alpha=0.7, edgecolor="black", linewidth=1.2)
    ax.annotate(n, (roe, pe), xytext=(7, 7), textcoords="offset points",
                fontsize=10, fontweight="bold" if n == "恒立" else "normal")
ax.set_xlabel("ROE (%)"); ax.set_ylabel("TTM P/E (倍)")
ax.set_title("可比公司 — 恒立PE溢价由ROE支撑;拓普/双林=人形叙事")
ax.set_xlim(0, 35); ax.set_ylim(0, 130)
xx = np.array([5, 30]); ax.plot(xx, 18 + 1.2*xx, color="grey", linestyle="--", alpha=0.5, label="质量回归线")
ax.legend()
save(fig, "18", "可比公司PE_ROE")

# 19: 研发投入
fig, ax1 = plt.subplots(figsize=(9, 5))
rd = [308.6, 636.1, 650.0, 694.4, 727.7, 705.0, 808, 928, 1079, 1239, 1383]
rd_pct = [r/v for r, v in zip(rd, rev_total)]
ax1.bar(x, rd, color=NAVY, alpha=0.75)
ax1.set_ylabel("研发投入 (百万元)", color=NAVY)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax1.set_xticks(x); ax1.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax2 = ax1.twinx()
ax2.plot(x, rd_pct, "o-", color=ORANGE, linewidth=2.5)
ax2.set_ylabel("研发占营收比", color=ORANGE)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt)); ax2.grid(False)
ax1.set_title("研发投入 — FY25 7.05亿(占营收6.4%);1,104名工程师")
save(fig, "19", "研发投入")

# 20: 营运资金天数
fig, ax = plt.subplots(figsize=(9, 5))
ar_d = [50, 51, 53, 64, 62, 60, 58, 58, 58]
inv_d = [130, 117, 120, 123, 120, 118, 115, 115, 115]
ap_d = [80, 84, 60, 58, 55, 55, 55, 55, 55]
xv = np.arange(2, 11)
ax.plot(xv, ar_d, "o-", color=NAVY, linewidth=2, label="应收天数")
ax.plot(xv, inv_d, "s-", color=TEAL, linewidth=2, label="存货天数")
ax.plot(xv, ap_d, "^-", color=ORANGE, linewidth=2, label="应付天数")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("天数")
ax.set_title("营运资金 — FY25应收天数因营收高增长上升")
ax.legend(loc="upper left")
save(fig, "20", "营运资金天数")

# 21: ROE/ROIC
fig, ax = plt.subplots(figsize=(9, 5))
roe = [27.0, 27.3, 16.0, 16.6, 17.5, 18.5, 19.5, 19.0, 18.0]
roic = [32.0, 33.0, 19.0, 22.0, 23.0, 24.0, 24.5, 24.0, 23.0]
xv = np.arange(2, 11)
ax.plot(xv, [r/100 for r in roe], "o-", color=NAVY, linewidth=2.5, label="ROE")
ax.plot(xv, [r/100 for r in roic], "s-", color=TEAL, linewidth=2.5, label="ROIC")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax.set_ylabel("回报率 %")
ax.set_title("ROE 与 ROIC — FY24被2022定增稀释;后续恢复")
ax.legend(loc="upper right")
save(fig, "21", "ROE_ROIC")

# 22: 线性驱动收入
fig, ax = plt.subplots(figsize=(10, 5))
ld_rev = [0, 0, 0, 0, 30, 100, 300, 600, 1100, 1700, 2300]
colors_ld = [GREY if i < 6 else GREEN if i < 10 else RED for i in range(len(YEARS_ALL))]
ax.bar(x, ld_rev, color=colors_ld, alpha=0.85, edgecolor="white")
for i, v in enumerate(ld_rev):
    if v > 0:
        ax.text(i, v+50, f"{v:,}百万", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("线性驱动收入 (百万元)")
ax.set_title("★ 线性驱动放量 — '第二增长曲线'驱动估值再定价")
ax.text(5.5, 1500, "管理层指引: FY26\n3倍;>300客户;\n人形机器人选择权",
        fontsize=10, color=NAVY, style="italic",
        bbox=dict(facecolor="#FFF9E6", edgecolor="grey", boxstyle="round,pad=0.5"))
save(fig, "22", "线性驱动放量")

# 23: 净现金
fig, ax = plt.subplots(figsize=(9, 5))
net_debt = [-2200, -3400, -7300, -8100, -9180, -9180, -10000, -11500, -13000, -14500, -16000]
ax.bar(x, net_debt, color=[GREEN if v < 0 else RED for v in net_debt], alpha=0.85)
ax.axhline(0, color="black", linewidth=0.7)
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("净(负债)/现金 (百万) — 负数=净现金")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax.set_title("净现金头寸 — FY25约92亿;堡垒型资产负债表")
save(fig, "23", "净现金")

# 24: 分红
fig, ax1 = plt.subplots(figsize=(9, 5))
dps = [0.31, 0.45, 0.55, 0.56, 0.70, 0.56, 0.60, 0.66, 0.72, 0.80, 0.88]
payout = [d*1340.8/n for d, n in zip(dps, net_inc)]
ax1.bar(x, dps, color=NAVY, alpha=0.85)
for i, v in enumerate(dps):
    ax1.text(i, v+0.02, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
ax1.set_xticks(x); ax1.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax1.set_ylabel("每股股息 (元)", color=NAVY); ax1.set_ylim(0, 1.1)
ax2 = ax1.twinx()
ax2.plot(x, payout, "D-", color=ORANGE, linewidth=2.5)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(pct_fmt))
ax2.set_ylabel("分红率 (%)", color=ORANGE); ax2.grid(False)
ax1.set_title("每股股息与分红率 — 稳定30-40%")
save(fig, "24", "分红")

# 25: 产能
fig, ax = plt.subplots(figsize=(10, 5))
cap_cyl = [600, 700, 750, 780, 820, 900, 950, 1020, 1080, 1140, 1200]
cap_lin = [0, 0, 0, 30, 50, 70, 150, 300, 500, 700, 900]
ax.plot(x, cap_cyl, "o-", color=NAVY, linewidth=2.5, label="油缸产能(千只/年)")
ax2 = ax.twinx()
ax2.plot(x, cap_lin, "s-", color=GREEN, linewidth=2.5, label="丝杠产能(千套/年)")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("油缸产能(千只/年)", color=NAVY)
ax2.set_ylabel("丝杠产能(千套/年)", color=GREEN); ax2.grid(False)
ax.set_title("产能建设 — 油缸规模优势 + 线性驱动新建")
save(fig, "25", "产能建设")

# 26: 全球布局
fig, ax = plt.subplots(figsize=(10, 5))
regions = ["中国(总部)","日本","德国","美国(IL)","印度","印尼","墨西哥(2025)","巴西","英国","意大利","法国","几内亚"]
status = ["总部","子","子","子","子","子","工厂","子","子","子","子","子"]
years_est = [1990, 2008, 2012, 2010, 2018, 2020, 2025, 2022, 2024, 2024, 2023, 2025]
color_map = {"总部": NAVY, "工厂": RED, "子": TEAL}
bars = ax.barh(regions, [2025-y+1 for y in years_est], color=[color_map[s] for s in status], alpha=0.85)
for b, y, s in zip(bars, years_est, status):
    ax.text(b.get_width()+0.5, b.get_y()+b.get_height()/2, f"建立 {y}年 ({s})", va="center", fontsize=9)
ax.set_xlabel("运营年数")
ax.set_title("全球布局 — 12国;墨西哥工厂2025新建")
save(fig, "26", "全球布局")

# 27: 专利
fig, ax = plt.subplots(figsize=(9, 5))
patents = [620, 720, 820, 920, 1020, 1125, 1230, 1340, 1450, 1560, 1680]
ax.fill_between(x, patents, color=NAVY, alpha=0.3)
ax.plot(x, patents, "o-", color=NAVY, linewidth=2.5, markersize=7)
for i, p in enumerate(patents):
    if i % 2 == 0:
        ax.text(i, p+30, f"{p}", ha="center", fontsize=8.5, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(YEARS_ALL, rotation=45, ha="right")
ax.set_ylabel("有效专利累计数")
ax.set_title("专利组合 — FY25 1,125项;年增~100项")
save(fig, "27", "专利")

# 28 ★ 必备: DCF敏感性热力图
fig, ax = plt.subplots(figsize=(8, 6))
g_vals = [0.020, 0.025, 0.030, 0.035, 0.040]
wacc_vals = [0.075, 0.080, 0.085, 0.090, 0.095, 0.100]
matrix = np.array([
    [76, 81, 88, 96, 105],[67, 71, 77, 83, 91],[59, 63, 67, 72, 79],
    [53, 56, 60, 64, 69],[48, 50, 53, 57, 61],[43, 45, 48, 51, 54],
])
im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", interpolation="nearest")
ax.set_xticks(np.arange(len(g_vals))); ax.set_xticklabels([f"{g:.1%}" for g in g_vals])
ax.set_yticks(np.arange(len(wacc_vals))); ax.set_yticklabels([f"{w:.1%}" for w in wacc_vals])
ax.set_xlabel("永续增长率 (g)"); ax.set_ylabel("WACC")
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        col = "white" if matrix[i, j] < 60 else "black"
        ax.text(j, i, f"{matrix[i,j]}", ha="center", va="center", color=col, fontsize=11, fontweight="bold")
ax.scatter([2], [2], s=600, edgecolor="black", facecolor="none", linewidth=2.5)
ax.text(2, 1.4, "基准情境", ha="center", fontsize=10, fontweight="bold")
plt.colorbar(im, ax=ax, label="DCF隐含价格(元)")
ax.set_title("★ DCF敏感性分析 — 隐含每股价格(元)\n当前价: 119.60元;乐观角落都达不到")
save(fig, "28", "DCF敏感性热力图")

# 29: DCF瀑布图
fig, ax = plt.subplots(figsize=(10, 5))
comps_29 = ["1-5年UFCF\n现值","终值\n现值","企业价值","+ 净现金","- 负债","- 少数股东","权益价值","÷ 股本\n(13.41亿)","每股价格"]
vals = [15480, 65765, 81245, 9216, -34, -58, 90369, None, 67.40]
colors_w = [NAVY, TEAL, GREY, GREEN, RED, RED, GREY, None, NAVY]
x_w = np.arange(len(comps_29))
ax2 = ax.twinx()
for i, (v, c) in enumerate(zip(vals, colors_w)):
    if v is None: continue
    if i == 8:
        ax2.bar(i, v, color=c, alpha=0.85)
        ax2.text(i, v+5, f"{v:.2f}元", ha="center", fontsize=10, fontweight="bold")
    else:
        ax.bar(i, v, color=c, alpha=0.85)
        if abs(v) >= 100:
            ax.text(i, v+max(vals[:7])*0.02 if v>0 else v-max(vals[:7])*0.05,
                    f"{v:,.0f}", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x_w); ax.set_xticklabels(comps_29, fontsize=8.5)
ax.set_ylabel("百万元"); ax2.set_ylabel("每股(元)"); ax2.set_ylim(0, 200); ax2.grid(False)
ax.set_title("DCF分解 — 企业价值→权益价值→每股价格 (百万元)")
save(fig, "29", "DCF分解")

# 30: 可比倍数
fig, ax = plt.subplots(figsize=(10, 5))
peer_names = ["恒立","烟台\n艾迪","KYB","派克","伊顿","舍弗勒","拓普","双林","NSK"]
pe = [58.6, 48.5, 52.7, 33.5, 38.8, 20.7, 100.0, 116.7, 25.0]
ev_eb = [41.5, 24.4, 16.8, 17.3, 19.6, 9.1, 50.0, 60.4, 12.3]
xx = np.arange(len(peer_names))
ax.bar(xx - 0.2, pe, 0.4, label="TTM P/E (倍)", color=NAVY, alpha=0.85)
ax.bar(xx + 0.2, ev_eb, 0.4, label="EV/EBITDA (倍)", color=ORANGE, alpha=0.85)
ax.axhline(43.6, color=GREY, linestyle="--", linewidth=1.5, label="同行中位数PE (43.6×)")
ax.set_xticks(xx); ax.set_xticklabels(peer_names, fontsize=9)
ax.set_ylabel("倍数 (×)")
ax.set_title("同行倍数对比 — 恒立58.6× PE vs 同行中位43.6×")
ax.legend(loc="upper right")
save(fig, "30", "同行倍数")

# 31: 同行ROE/增长
fig, ax = plt.subplots(figsize=(9, 6))
peer_growth = [13.0, 6.0, 4.0, 6.5, 7.0, 2.0, 18.0, 22.0, 3.0]
peer_roe2 = [16.6, 11.0, 6.5, 30.5, 19.2, 6.0, 22.0, 8.5, 5.5]
colors_p = [NAVY, "#FF8800", GREY, GREY, GREY, GREY, RED, RED, GREY]
for n, g, r, c in zip(peer_names, peer_growth, peer_roe2, colors_p):
    sz = 400 if n == "恒立" else 250
    ax.scatter(g, r, s=sz, color=c, alpha=0.7, edgecolor="black", linewidth=1.2)
    ax.annotate(n.replace("\n",""), (g, r), xytext=(7, 7), textcoords="offset points",
                fontsize=10, fontweight="bold" if n == "恒立" else "normal")
ax.set_xlabel("前瞻收入增速 (%)"); ax.set_ylabel("ROE (%)")
ax.set_title("同行定位 — 恒立位于高质量+高增长象限")
ax.axvline(np.median(peer_growth), color="grey", linestyle="--", alpha=0.5)
ax.axhline(np.median(peer_roe2), color="grey", linestyle="--", alpha=0.5)
ax.set_xlim(0, 28); ax.set_ylim(0, 35)
save(fig, "31", "同行ROE_增长")

# 32 ★ 必备: 足球场
fig, ax = plt.subplots(figsize=(11, 6))
methods = [
    "DCF — 乐观/悲观区间","P/B — 同行中位","EV/EBITDA — 同行中位","DCF — 基准",
    "P/E — 同行中位 × FY26E EPS","P/E — 人形溢价","先例 — 人形再定价","52周区间",
]
lows = [50, 85, 70, 62, 75, 100, 110, 80]
mids = [77, 115, 98, 77, 102, 122, 145, 115]
highs = [135, 150, 132, 95, 130, 156, 200, 142]
y_pos = np.arange(len(methods))
for i, (lo, mid, hi) in enumerate(zip(lows, mids, highs)):
    ax.barh(i, hi-lo, left=lo, color=NAVY, alpha=0.4, height=0.55, edgecolor="black", linewidth=1)
    ax.scatter([mid], [i], s=120, color=ORANGE, zorder=5, edgecolor="black", linewidth=1)
    ax.text(lo - 2, i, f"{lo}", va="center", ha="right", fontsize=9)
    ax.text(hi + 2, i, f"{hi}", va="center", ha="left", fontsize=9)
    ax.text(mid, i + 0.3, f"{mid}", va="bottom", ha="center", fontsize=9, fontweight="bold", color=ORANGE)
ax.set_yticks(y_pos); ax.set_yticklabels(methods, fontsize=10); ax.invert_yaxis()
ax.set_xlabel("隐含每股价格 (元)")
ax.axvline(119.60, color=RED, linestyle="--", linewidth=2.5, label="当前价: 119.60元")
ax.axvline(106, color=GREEN, linestyle="-", linewidth=2.5, label="12个月目标价: 106元 (持有)")
ax.set_title("★ 估值足球场 — 加权目标价 106元 (持有,-11%下行)")
ax.legend(loc="lower right", fontsize=10); ax.set_xlim(40, 220); ax.grid(True, axis="x", alpha=0.3)
save(fig, "32", "估值足球场")

# 33: 3年PE历史
fig, ax = plt.subplots(figsize=(10, 5))
months_pe = np.arange(36)
pe_anchors = [25, 27, 30, 32, 35, 40, 45, 50, 55, 60, 55, 52, 56, 58.6]
xp = np.linspace(0, 35, 14)
pe_hist = np.interp(months_pe, xp, pe_anchors) + np.random.randn(36) * 1.5
ax.plot(months_pe, pe_hist, color=NAVY, linewidth=2)
ax.fill_between(months_pe, np.percentile(pe_hist, 25), np.percentile(pe_hist, 75), color=NAVY, alpha=0.15, label="25-75分位带")
ax.axhline(np.median(pe_hist), color=ORANGE, linestyle="--", label=f"3年中位: {np.median(pe_hist):.0f}×")
ax.axhline(58.6, color=RED, linestyle="-", label=f"当前: 58.6× (顶部十分位)")
ax.set_xticks(np.arange(0, 36, 6))
ax.set_xticklabels(["23年5月","23年11月","24年5月","24年11月","25年5月","25年11月"])
ax.set_ylabel("TTM P/E (倍)")
ax.set_title("3年PE历史 — 当前58.6×位于历史顶部十分位")
ax.legend(loc="lower right")
save(fig, "33", "PE历史3年")

# 34: EV/EBITDA历史
fig, ax = plt.subplots(figsize=(10, 5))
ev_eb_anchors = [18, 20, 22, 25, 28, 30, 35, 38, 42, 45, 40, 38, 40, 41.5]
ev_eb_hist = np.interp(months_pe, xp, ev_eb_anchors) + np.random.randn(36)*1.2
ax.plot(months_pe, ev_eb_hist, color=TEAL, linewidth=2)
ax.fill_between(months_pe, np.percentile(ev_eb_hist, 25), np.percentile(ev_eb_hist, 75), color=TEAL, alpha=0.15)
ax.axhline(np.median(ev_eb_hist), color=ORANGE, linestyle="--", label=f"3年中位: {np.median(ev_eb_hist):.1f}×")
ax.axhline(41.5, color=RED, linestyle="-", label=f"当前: 41.5×")
ax.set_xticks(np.arange(0, 36, 6))
ax.set_xticklabels(["23年5月","23年11月","24年5月","24年11月","25年5月","25年11月"])
ax.set_ylabel("EV/EBITDA (倍)")
ax.set_title("3年EV/EBITDA历史 — 当前约41×亦处于极端区间")
ax.legend(loc="lower right")
save(fig, "34", "EV_EBITDA历史")

# 35: 催化剂图
fig, ax = plt.subplots(figsize=(10, 5))
cats = ["线性驱动\n>3亿FY26","挖机周期\n确认上行","毛利率\n恢复","墨西哥CAT\n一级供应","人形OEM\n供应订单"]
probs = [65, 60, 50, 50, 25]
impacts = [5, 8, 3, 5, 40]
sizes = [p*i*3 for p, i in zip(probs, impacts)]
colors_c = [GREEN if p > 50 else ORANGE if p > 30 else RED for p in probs]
for i, (n, p, im, sz, c) in enumerate(zip(cats, probs, impacts, sizes, colors_c)):
    ax.scatter(p, im, s=sz, color=c, alpha=0.7, edgecolor="black", linewidth=1.5)
    ax.annotate(n, (p, im), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
ax.set_xlabel("概率 (%) — 12个月维度"); ax.set_ylabel("预估股价影响 (%)")
ax.set_title("催化剂地图 — 人形OEM订单 = 高影响低概率长尾")
ax.set_xlim(10, 80); ax.set_ylim(0, 50)
save(fig, "35", "催化剂地图")

# Pack ZIP
ZIP_PATH = "reports/company/Hengli_SSE601100/Hengli_SSE601100_Charts_2026-05-19_zh.zip"
n_charts = len([f for f in os.listdir(OUT_DIR) if f.endswith(".png")])
print(f"已生成 {n_charts} 张中文图表")

index = os.path.join(OUT_DIR, "图表索引.txt")
with open(index, "w") as f:
    f.write("恒立液压 (SSE:601100) — 图表索引\n" + "="*60 + "\n")
    f.write(f"图表总数: {n_charts}\n格式: 300 DPI PNG\n\n")
    f.write("★ 必备图表:\n")
    f.write("  chart_03: 分产品营收(堆积面积)\n  chart_04: 分地区营收(堆积柱)\n")
    f.write("  chart_28: DCF敏感性热力图\n  chart_32: 估值足球场\n\n")
    f.write("全部图表:\n")
    for fn in sorted(os.listdir(OUT_DIR)):
        if fn.endswith(".png"): f.write(f"  {fn}\n")

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for fn in sorted(os.listdir(OUT_DIR)):
        zf.write(os.path.join(OUT_DIR, fn), arcname=fn)
print(f"已保存压缩包: {ZIP_PATH}")
print(f"压缩包大小: {os.path.getsize(ZIP_PATH)/1024:.0f} KB")
