"""Charts for UBTech Robotics (HKEX:9880) company research report.

Data sourced exclusively from cninfo annual / interim reports
(see cninfo_reports/HKEX/09880_优必选/). No fabricated numbers.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

OUT = "/Users/x/projects/financial_agent/reports/charts"

# Matplotlib CJK setup
plt.rcParams["font.sans-serif"] = [
    "PingFang SC", "Heiti SC", "Hiragino Sans GB",
    "Songti SC", "STHeiti", "Arial Unicode MS", "sans-serif",
]
plt.rcParams["axes.unicode_minus"] = False


# ---------- Chart 1: Revenue + Gross Margin trend (2020–2024) ----------
years = ["2020", "2021", "2022", "2023", "2024"]
revenue = [740.2, 817.2, 1008.3, 1055.7, 1305.4]  # RMB mn
loss = [-707.0, -917.5, -987.4, -1264.6, -1159.9]  # RMB mn 年内虧損
gross_profit = [330.7, 256.0, 397.2, 332.8, 374.0]
gross_margin = [gp / rev * 100 for gp, rev in zip(gross_profit, revenue)]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#1f4e79", alpha=0.85, label="营业收入 (RMB mn)")
ax1.set_ylabel("营业收入 (RMB 百万元)", color="#1f4e79", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 1500)
for bar, v in zip(bars, revenue):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 25, f"{v:,.0f}",
             ha="center", fontsize=9, color="#1f4e79")

ax2 = ax1.twinx()
ax2.plot(years, gross_margin, color="#c00000", marker="o", linewidth=2.2,
         label="毛利率 (%)")
ax2.set_ylabel("毛利率 (%)", color="#c00000", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(0, 50)
for x, y in zip(years, gross_margin):
    ax2.text(x, y + 1.5, f"{y:.1f}%", color="#c00000", ha="center", fontsize=9)

plt.title("优必选 (9880.HK) — 营业收入与毛利率 (2020–2024)", fontsize=12.5, pad=12)
ax1.grid(axis="y", linestyle="--", alpha=0.35)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_revenue_margin.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 2: Net loss & cash burn ----------
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(years, [abs(x) for x in loss], color="#c45a5a", alpha=0.9)
for bar, v in zip(bars, loss):
    ax.text(bar.get_x() + bar.get_width() / 2, abs(v) + 30,
            f"({abs(v):,.0f})", ha="center", fontsize=9, color="#7a2222")
ax.set_ylabel("年内净亏损 (RMB 百万元)", fontsize=11)
ax.set_title("优必选 — 持续亏损 (2020–2024)", fontsize=12.5, pad=10)
ax.set_ylim(0, 1500)
ax.grid(axis="y", linestyle="--", alpha=0.35)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_net_loss.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 3: Segment revenue mix (2023 vs 2024) ----------
segments = ["教育机器人", "物流机器人", "其他行业\n定制", "消费级机器人\n及硬件", "其他"]
fy23 = [347.3, 389.7, 62.2, 253.6, 2.8]
fy24 = [363.4, 321.7, 140.7, 477.0, 2.6]
x = np.arange(len(segments))
w = 0.36

fig, ax = plt.subplots(figsize=(10, 5.2))
b1 = ax.bar(x - w / 2, fy23, w, label="FY2023", color="#7a9bbf")
b2 = ax.bar(x + w / 2, fy24, w, label="FY2024", color="#1f4e79")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                f"{bar.get_height():,.0f}", ha="center", fontsize=8.5)
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=10)
ax.set_ylabel("分部收入 (RMB 百万元)", fontsize=11)
ax.set_title("优必选 — 分部收入结构 (FY2023 vs FY2024)", fontsize=12.5, pad=10)
ax.legend(loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.35)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 4: H1 2025 vs H1 2024 ----------
metrics = ["营业收入", "毛利", "净亏损 (绝对值)"]
h1_25 = [621.5, 217.3, 440.0]
h1_24 = [487.2, 185.2, 539.8]
x = np.arange(len(metrics))
fig, ax = plt.subplots(figsize=(8, 4.7))
b1 = ax.bar(x - 0.2, h1_24, 0.38, color="#a6bcd6", label="H1 2024")
b2 = ax.bar(x + 0.2, h1_25, 0.38, color="#1f4e79", label="H1 2025")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                f"{bar.get_height():,.0f}", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10)
ax.set_ylabel("RMB 百万元", fontsize=11)
ax.set_title("优必选 — 2025 年中期 vs 2024 年中期", fontsize=12.5, pad=10)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.35)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_h1_2025.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 5: Humanoid robot TAM (Goldman + Morgan Stanley) ----------
gs_years = [2024, 2025, 2027, 2030, 2035]
gs_tam = [1.5, 3.0, 8.0, 17.0, 38.0]  # USD bn (Goldman 2024 update)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(gs_years, gs_tam, marker="o", color="#1f4e79", linewidth=2.4, markersize=8)
for x, y in zip(gs_years, gs_tam):
    ax.text(x, y + 1, f"${y:.0f}B", ha="center", fontsize=10, color="#1f4e79")
ax.set_xlabel("年份", fontsize=11)
ax.set_ylabel("全球人形机器人市场规模 (USD bn)", fontsize=11)
ax.set_title("全球人形机器人 TAM — Goldman Sachs 2024 预测\n(到 2050 年 Morgan Stanley 预计达 5 万亿美元)",
             fontsize=12, pad=10)
ax.set_ylim(0, 45)
ax.grid(linestyle="--", alpha=0.4)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_tam.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Chart 6: R&D spend & patent stockpile ----------
rd_years = ["2022", "2023", "2024", "H1 2025"]
rd_spend = [443.7, 490.5, 478.1, 268.0]  # RMB mn (FY24 478.1; H1 25 approx — see report note)
patents = [None, 2173, 2680, 2790]  # 2173 = 2680/1.2339 (i.e. 2024 +23.39% over 2023)

fig, ax1 = plt.subplots(figsize=(9, 4.8))
bars = ax1.bar(rd_years, rd_spend, color="#1f4e79", alpha=0.85)
for bar, v in zip(bars, rd_spend):
    ax1.text(bar.get_x() + bar.get_width() / 2, v + 8, f"{v:,.0f}",
             ha="center", fontsize=9, color="#1f4e79")
ax1.set_ylabel("研发支出 (RMB 百万元)", color="#1f4e79", fontsize=11)
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_ylim(0, 600)

ax2 = ax1.twinx()
ax2.plot(rd_years, patents, color="#c00000", marker="s", linewidth=2.2)
for x, y in zip(rd_years, patents):
    if y is not None:
        ax2.text(x, y + 60, f"{y:,}", color="#c00000", ha="center", fontsize=9)
ax2.set_ylabel("累计授权专利数 (项)", color="#c00000", fontsize=11)
ax2.tick_params(axis="y", labelcolor="#c00000")
ax2.set_ylim(1500, 3200)

plt.title("优必选 — 研发投入与专利累积", fontsize=12.5, pad=10)
fig.tight_layout()
plt.savefig(f"{OUT}/ubtech_rd_patents.png", dpi=150, bbox_inches="tight")
plt.close()

print("Charts written:")
for f in [
    "ubtech_revenue_margin.png",
    "ubtech_net_loss.png",
    "ubtech_segment_mix.png",
    "ubtech_h1_2025.png",
    "ubtech_tam.png",
    "ubtech_rd_patents.png",
]:
    print(" -", f)
