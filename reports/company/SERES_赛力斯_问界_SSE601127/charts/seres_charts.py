"""Charts for 赛力斯集团 (SSE:601127 / HKEX:9927) — SERES / AITO 问界 research report.

Sources (PRC GAAP, consolidated):
- FY2021/2022 totals: 2022 年年度报告 (cninfo, 2023-04-28).
- FY2023/2024/2025 totals: 2025 年年度报告 (cninfo, 2026-03-30), p.7-8.
- 问界 deliveries by model FY2025: 2025 年年度报告 p.14 + 媒体披露.
- Peer P/S: stockanalysis.com / 媒体 (2026-Q1).
All RMB in 亿元 (100 mn) unless noted.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

plt.rcParams.update({
    "font.family": ["Arial Unicode MS", "PingFang SC", "Heiti SC", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})
NAVY = "#1f3a5f"; TEAL = "#2a9d8f"; CORAL = "#e76f51"; GOLD = "#f4a261"; GRAY = "#888"; PURPLE="#6a4c93"

# ============== Chart 1: 5-year revenue + net income swing-to-profit ==============
years = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
revenue = [167.2, 341.0, 358.4, 1451.8, 1650.5]      # 亿元
net_income = [-18.2, -38.3, -24.5, 59.46, 59.57]      # 亿元 归母净利润
nev_gm = [None, None, None, 26.21, 28.76]             # NEV gross margin %

fig, ax = plt.subplots(figsize=(11, 6.2))
x = np.arange(len(years)); w = 0.38
b1 = ax.bar(x - w/2, revenue, w, label="营业收入 Revenue (亿元)", color=NAVY)
b2 = ax.bar(x + w/2, net_income, w, label="归母净利润 Net income (亿元)",
            color=[CORAL if v < 0 else TEAL for v in net_income])
ax.axhline(0, color="black", lw=0.9)
for b in b1:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+15, f"{b.get_height():,.0f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=NAVY)
for b, v in zip(b2, net_income):
    va = "bottom" if v >= 0 else "top"
    off = 15 if v >= 0 else -15
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+off, f"{v:+,.1f}",
            ha="center", va=va, fontsize=10, fontweight="bold",
            color=(TEAL if v >= 0 else CORAL))
ax.set_title("赛力斯 5 年营收与归母净利润 — 2024 年扭亏为盈的拐点\n"
             "SERES Group: Revenue & Net Income, FY2021–FY2025",
             fontsize=14, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(years)
ax.set_ylabel("人民币 亿元 (RMB 100 mn)")
ax.legend(loc="upper left", frameon=False, fontsize=11)
ax.annotate("2024：问界 M9 + 新 M7 满产\n营收 +305% YoY，首次大幅盈利",
            xy=(3, 59.46), xytext=(2.0, 700),
            fontsize=10, color=TEAL, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5),
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=TEAL, alpha=0.9))
ax.set_ylim(-150, 1900)
plt.tight_layout()
plt.savefig("seres_revenue_netincome.png", dpi=140, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved seres_revenue_netincome.png")

# ============== Chart 2: 问界 deliveries by model FY2025 ==============
models = ["问界 M9\n(50万+ 旗舰)", "问界 M8\n(40万级)", "问界 M7\n(30万级)", "问界 M5/其他\n(20-25万)"]
# FY2025: M9 11万+, M8 15万+, M7 11万+, total 问界 42.6万 → M5/其他 ≈ 5.6万
deliveries = [11.0, 15.0, 11.0, 5.6]
colors2 = [PURPLE, NAVY, TEAL, GOLD]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(models, deliveries, color=colors2, width=0.62)
for b, v in zip(bars, deliveries):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.2, f"{v:.1f} 万辆",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_title("问界 (AITO) FY2025 分车型交付量 — M8 / M9 撑起 40-50 万级高端\n"
             "AITO deliveries by model, FY2025 (问界全系 ≈ 42.6 万辆)",
             fontsize=13, fontweight="bold")
ax.set_ylabel("交付量 (万辆 / 10k units)")
ax.set_ylim(0, 18)
ax.text(0.98, 0.95, "M9 蝉联 50 万元级年度销冠\nM8 上市即 40 万级销冠\n新 M7 首季获 30 万级销冠",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color=NAVY,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRAY, alpha=0.9))
plt.tight_layout()
plt.savefig("seres_deliveries_by_model.png", dpi=140, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved seres_deliveries_by_model.png")

# ============== Chart 3: peer P/S comparison ==============
peers = ["赛力斯\n601127", "比亚迪\n1211.HK", "理想\nLI", "蔚来\nNIO", "小鹏\nXPEV", "零跑\n9863.HK"]
# TTM P/S (approx, 2026 Q1 / media + stockanalysis). 赛力斯 mkt cap ~1530亿 / rev 1650亿 ≈ 0.93
ps = [0.93, 1.4, 1.0, 1.4, 1.5, 2.1]
colors3 = [CORAL, NAVY, TEAL, GOLD, PURPLE, GRAY]

fig, ax = plt.subplots(figsize=(10, 5.6))
bars = ax.bar(peers, ps, color=colors3, width=0.6)
for b, v in zip(bars, ps):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.03, f"{v:.2f}×",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_title("市销率 (P/S, TTM) 同业对比 — 赛力斯估值处于行业低位\n"
             "TTM Price-to-Sales: SERES vs China NEV peers",
             fontsize=13, fontweight="bold")
ax.set_ylabel("市销率 P/S (倍)")
ax.set_ylim(0, 2.6)
ax.text(0.98, 0.95, "赛力斯已连续两年盈利，\nP/E≈25×；多数新势力仍亏损\n以 P/S 比较更具可比性",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color=NAVY,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=GRAY, alpha=0.9))
plt.tight_layout()
plt.savefig("seres_peer_valuation.png", dpi=140, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved seres_peer_valuation.png")
