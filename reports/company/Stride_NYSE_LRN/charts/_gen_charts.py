#!/usr/bin/env python3
"""Generate charts for Stride (LRN) company research report."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# ─────────────────────────────────────────────────────────────────────────────
# Chart 1 — Revenue + Enrollment trend (FY20–FY25)
# Source: 10-K FY22 (FY20-22), 10-K FY24 (FY23-24), 10-K FY25 (FY25)
fy = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25"]
rev = [1040.8, 1536.8, 1686.7, 1837.4, 2040.1, 2405.3]  # $ millions
enr_total = [120.9, 186.3, 185.1, 178.2, 194.3, 234.0]  # thousands

fig, ax1 = plt.subplots(figsize=(10, 5.5))
color1 = "#1f4e79"
ax1.bar(fy, rev, color=color1, alpha=0.85, label="Total revenue ($M)")
ax1.set_ylabel("Revenue ($ millions)", color=color1, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color1)
ax1.set_ylim(0, 2800)
for i, v in enumerate(rev):
    ax1.text(i, v + 40, f"${v:,.0f}M", ha="center", fontsize=9, color=color1)

ax2 = ax1.twinx()
color2 = "#c0392b"
ax2.plot(fy, enr_total, color=color2, marker="o", linewidth=2.5, markersize=8,
         label="Total enrollment (thousands)")
ax2.set_ylabel("Total enrollment (thousands)", color=color2, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color2)
ax2.set_ylim(0, 280)
for i, v in enumerate(enr_total):
    ax2.text(i, v + 8, f"{v:.1f}K", ha="center", fontsize=9, color=color2)

plt.title("Stride (LRN): Revenue and Enrollment, FY2020–FY2025", fontsize=13, pad=15)
ax1.grid(axis="y", alpha=0.3)
fig.tight_layout()
plt.savefig(OUT / "lrn_revenue_enrollment.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Chart 2 — Adjusted EBITDA margin trend
# FY23-FY25 Adj EBITDA from 8-K earnings press releases.
# Prior to FY23, Stride disclosed plain EBITDA only — chart restricted to
# disclosed Adjusted EBITDA series.
fy2 = ["FY23", "FY24", "FY25"]
adj_ebitda = [296.2, 390.7, 571.0]  # $M (FY23 from Aug-2024 PR; FY24-25 from Aug-2025 PR)
rev_fy2 = [1837.4, 2040.1, 2405.3]
adj_ebitda_margin = [a / r * 100 for a, r in zip(adj_ebitda, rev_fy2)]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(fy2, adj_ebitda_margin, color="#16a085", alpha=0.85)
ax.set_ylabel("Adjusted EBITDA margin (%)", fontsize=11)
ax.set_title("Stride (LRN): Adjusted EBITDA Margin, FY2023–FY2025", fontsize=13, pad=15)
ax.set_ylim(0, 30)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
for bar, val, abs_val in zip(bars, adj_ebitda_margin, adj_ebitda):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.6,
            f"{val:.1f}%\n(${abs_val:.0f}M)",
            ha="center", fontsize=9)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lrn_ebitda_margin.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Chart 3 — Career Learning revenue mix (stacked bar, FY23-FY25)
fy3 = ["FY23", "FY24", "FY25"]
gen_ed = [1131.4, 1289.2, 1448.7]
cl_mhs = [586.8, 651.2, 876.3]  # Career Learning - Middle/High School
adult = [119.2, 99.7, 80.4]  # Adult Learning

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(fy3))
width = 0.55
b1 = ax.bar(x, gen_ed, width, color="#1f4e79", label="General Education")
b2 = ax.bar(x, cl_mhs, width, bottom=gen_ed, color="#27ae60",
            label="Career Learning — Middle/High School")
b3 = ax.bar(x, adult, width, bottom=[a + b for a, b in zip(gen_ed, cl_mhs)],
            color="#e67e22", label="Career Learning — Adult")
ax.set_xticks(x)
ax.set_xticklabels(fy3)
ax.set_ylabel("Revenue ($ millions)", fontsize=11)
ax.set_title("Stride (LRN): Revenue Mix by Line, FY2023–FY2025", fontsize=13, pad=15)
ax.legend(loc="upper left", fontsize=9)

for i in range(len(fy3)):
    tot = gen_ed[i] + cl_mhs[i] + adult[i]
    cl = cl_mhs[i] + adult[i]
    ax.text(i, tot + 35, f"Total ${tot:,.0f}M\nCareer Learning: {cl/tot*100:.1f}%",
            ha="center", fontsize=9)
ax.set_ylim(0, 2800)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lrn_segment_mix.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Chart 4 — Peer valuation comparison (P/E + EV/EBITDA)
# Pulled via yfinance 2026-05-20
peers = ["LRN\n(Stride)", "GHC\n(Graham)", "LAUR\n(Laureate)", "STRA\n(Strategic)",
         "LOPE\n(Grand Canyon)", "PRDO\n(Perdoceo)"]
pe = [13.7, 16.0, 17.6, 14.1, 19.6, 12.8]
ev_ebitda = [6.7, 9.9, 10.6, 7.2, 11.4, 6.3]

fig, ax = plt.subplots(figsize=(11, 5.5))
x = np.arange(len(peers))
width = 0.38
b1 = ax.bar(x - width/2, pe, width, color="#1f4e79", label="TTM P/E")
b2 = ax.bar(x + width/2, ev_ebitda, width, color="#c0392b", label="EV / EBITDA")
ax.set_xticks(x)
ax.set_xticklabels(peers, fontsize=10)
ax.set_ylabel("Multiple (x)", fontsize=11)
ax.set_title("Stride vs. For-Profit Education Peers — TTM P/E and EV/EBITDA "
             "(as of 2026-05-20)", fontsize=12, pad=15)
ax.legend(loc="upper right", fontsize=10)
for bar, v in zip(b1, pe):
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.3, f"{v:.1f}x",
            ha="center", fontsize=9, color="#1f4e79")
for bar, v in zip(b2, ev_ebitda):
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.3, f"{v:.1f}x",
            ha="center", fontsize=9, color="#c0392b")
# peer median lines
ax.axhline(np.median(pe), color="#1f4e79", linestyle=":", alpha=0.5,
           label=f"P/E median ({np.median(pe):.1f}x)")
ax.axhline(np.median(ev_ebitda), color="#c0392b", linestyle=":", alpha=0.5,
           label=f"EV/EBITDA median ({np.median(ev_ebitda):.1f}x)")
ax.set_ylim(0, 22)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lrn_peer_multiples.png", dpi=150, bbox_inches="tight")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# Chart 5 — Stock price chart 5-year with key events annotated
import yfinance as yf
import datetime as dt
t = yf.Ticker("LRN")
hist = t.history(period="5y")
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(hist.index, hist["Close"], color="#2c3e50", linewidth=1.4)
ax.set_title("Stride (LRN) — 5-Year Price Chart (May 2021 – May 2026)",
             fontsize=12, pad=15)
ax.set_ylabel("Close price ($)", fontsize=11)
events = [
    ("2021-01-15", 28, "K12 → Stride\nrebrand (Jan 2021)"),
    ("2025-09-10", 158, "All-time high\n~$163"),
    ("2025-11-03", 70, "Stock plunge + \n$500M buyback"),
    ("2026-04-28", 90, "Q3-FY26\nresults"),
]
for d, y, label in events:
    dd = dt.datetime.strptime(d, "%Y-%m-%d")
    ax.annotate(label, xy=(dd, y), xytext=(dd, y + 30),
                fontsize=8.5, ha="center",
                arrowprops=dict(arrowstyle="->", color="gray", alpha=0.6))
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "lrn_price_5y.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts written to", OUT)
for p in sorted(OUT.glob("*.png")):
    print(" -", p.name, p.stat().st_size, "bytes")
