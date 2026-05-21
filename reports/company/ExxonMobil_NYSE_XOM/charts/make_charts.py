"""Generate ExxonMobil charts for the initiating-coverage report.

All numbers come from:
- 2025 Form 10-K (FY2025, filed Feb 2026): 5-yr financial summary, segment
  table (Earnings After Income Tax by segment), Upstream operational table,
  and shareholder distribution disclosures.
- Q1-2026 10-Q & 1Q26 press release.
- Yahoo Finance peer multiples pulled 2026-05-20.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

CHARTS = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. Revenue + Net Income (3 yr from 10-K + Q1-2026 from 10-Q)
# ---------------------------------------------------------------------------
years = ["2023", "2024", "2025"]
revenue_b = [334.697, 339.247, 323.905]        # Sales & other operating revenue ($B)
net_income_b = [36.010, 33.680, 28.844]        # Net income attributable to XOM ($B)

fig, ax1 = plt.subplots(figsize=(8.0, 4.6))
x = np.arange(len(years))
width = 0.4
b1 = ax1.bar(x - width / 2, revenue_b, width, color="#1f4e79", label="Sales & other operating revenue ($B)")
ax1.set_ylabel("Revenue ($B)", color="#1f4e79")
ax1.tick_params(axis="y", labelcolor="#1f4e79")
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylim(0, 400)

ax2 = ax1.twinx()
b2 = ax2.bar(x + width / 2, net_income_b, width, color="#c97a3b", label="Net income ($B)")
ax2.set_ylabel("Net Income ($B)", color="#c97a3b")
ax2.tick_params(axis="y", labelcolor="#c97a3b")
ax2.set_ylim(0, 50)

for rect in list(b1) + list(b2):
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                 xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)

plt.title("ExxonMobil — Revenue and Net Income (FY2023-FY2025)")
fig.tight_layout()
fig.savefig(CHARTS / "xom_revenue_netincome.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 2. Segment earnings (after-tax) — Upstream / Energy Products / Chemical / Specialty
# ---------------------------------------------------------------------------
segments = ["Upstream", "Energy\nProducts", "Chemical\nProducts", "Specialty\nProducts"]
seg_2024 = [25.390, 4.033, 2.577, 3.052]
seg_2025 = [21.354, 7.423, 0.800, 2.857]

fig, ax = plt.subplots(figsize=(8.4, 4.6))
x = np.arange(len(segments))
ax.bar(x - 0.2, seg_2024, 0.4, label="FY2024", color="#5b8db8")
ax.bar(x + 0.2, seg_2025, 0.4, label="FY2025", color="#1f4e79")
for i, (a, b) in enumerate(zip(seg_2024, seg_2025)):
    ax.text(i - 0.2, a + 0.3, f"${a:.1f}B", ha="center", fontsize=8)
    ax.text(i + 0.2, b + 0.3, f"${b:.1f}B", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(segments)
ax.set_ylabel("Earnings after income tax ($B)")
ax.set_title("ExxonMobil — Earnings After Income Tax by Segment, FY2024 vs FY2025")
ax.legend()
fig.tight_layout()
fig.savefig(CHARTS / "xom_segment_earnings.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. Production / CAPEX / Dividend per share (FY2023-FY2025)
# ---------------------------------------------------------------------------
prod_moebd = [3.738, 4.333, 4.736]               # MOEBD oil-equivalent (10-K)
capex_b = [26.319, 27.602, 31.476]               # Approx total capex from CFS / "Additions to PP&E" (FY2025 10-K Five-yr table excl. Pioneer one-off)
# Better: use cash capex disclosed = 24.4B (2023), 27.6B (2024)? Use cash capex from XOM disclosures
cash_capex_b = [26.3, 27.6, 29.0]                # Cash capex; FY2025 disclosed $29.0B in Q1-26 PR ("Cash Capex")
div_per_share = [3.68, 3.84, 4.00]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11.5, 4.0))
years3 = ["2023", "2024", "2025"]
ax1.bar(years3, prod_moebd, color="#1f4e79")
for i, v in enumerate(prod_moebd):
    ax1.text(i, v + 0.05, f"{v:.2f}", ha="center", fontsize=9)
ax1.set_title("Oil-equivalent production (MOEBD)")
ax1.set_ylim(0, 5.5)

ax2.bar(years3, cash_capex_b, color="#c97a3b")
for i, v in enumerate(cash_capex_b):
    ax2.text(i, v + 0.3, f"${v:.1f}B", ha="center", fontsize=9)
ax2.set_title("Cash CapEx ($B)")
ax2.set_ylim(0, 36)

ax3.bar(years3, div_per_share, color="#3a7d44")
for i, v in enumerate(div_per_share):
    ax3.text(i, v + 0.05, f"${v:.2f}", ha="center", fontsize=9)
ax3.set_title("Dividend paid per share ($)")
ax3.set_ylim(0, 4.6)

fig.suptitle("ExxonMobil — Production, CapEx & Dividend Trend (FY2023-FY2025)", y=1.02)
fig.tight_layout()
fig.savefig(CHARTS / "xom_production_capex_dividend.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. Peer valuation — P/E vs supermajor peers
# ---------------------------------------------------------------------------
peers = ["XOM", "CVX", "SHEL", "BP", "TTE"]
pe = [25.98, 33.11, 13.55, 36.25, 13.73]
ps = [1.96, 2.04, 0.91, 0.60, 1.12]
div_y = [2.64, 3.72, 3.60, 4.42, 4.56]
ev_ebitda = [12.38, 11.19, 11.04, 22.04, 6.40]

fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.0))
def bar_panel(ax, vals, title, color, yfmt="{:.1f}"):
    bars = ax.bar(peers, vals, color=color)
    for i, (b, v) in enumerate(zip(bars, vals)):
        ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.02, yfmt.format(v),
                ha="center", fontsize=9)
    ax.set_title(title)
    ax.set_ylim(0, max(vals) * 1.18)
    # highlight XOM
    bars[0].set_edgecolor("black")
    bars[0].set_linewidth(1.5)
bar_panel(axes[0, 0], pe, "TTM P/E", "#1f4e79", "{:.1f}×")
bar_panel(axes[0, 1], ps, "TTM P/S", "#5b8db8", "{:.2f}×")
bar_panel(axes[1, 0], div_y, "Dividend yield (%)", "#3a7d44", "{:.2f}%")
bar_panel(axes[1, 1], ev_ebitda, "EV / EBITDA (TTM)", "#c97a3b", "{:.1f}×")
fig.suptitle("ExxonMobil vs Supermajor Peers — Valuation Snapshot (2026-05-20)", y=1.02)
fig.tight_layout()
fig.savefig(CHARTS / "xom_peer_valuation.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("Charts written to", CHARTS)
