"""Arm Holdings — chart pack for company research report (2026-05-20).

Data sources:
- FY23/FY24/FY25 revenue & royalty/license mix: Arm Holdings Form 20-F for FY25
  (year ended March 31, 2025), filed 2025-05-28, accession 0001973239-25-000016.
- FY26 totals (year ended March 31, 2026): Q4 FY26 earnings press release / Form
  6-K, filed 2026-05-06, accession 0001973239-26-000062, exhibit 99.2.
- TTM market multiples: Yahoo Finance (yfinance), pulled 2026-05-20.
- Q4 FYE26 royalty drivers (Armv9 share, CSS, smartphone, IoT, cloud): Q4 FY26
  shareholder letter (same filing as above).
- Total Access / Flexible Access licensee counts: Q4 FY26 earnings release.
"""

import os
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# 1. Revenue + non-GAAP operating margin trend (4 fiscal years, FY23–FY26)
# ---------------------------------------------------------------------------
years = ["FY23", "FY24", "FY25", "FY26"]
revenue = [2679, 3233, 4007, 4920]  # $M
# FY23 non-GAAP op margin disclosed in F-1 ~ 30%; FY24 46.7%, FY25 ~46% (per
# Q4 FY25 release), FY26 43.0% (per Q4 FY26 release).  We chart FY24–FY26
# where management has consistently disclosed non-GAAP operating margin.
nongaap_op_margin = [None, 46.7, 46.0, 43.0]

fig, ax1 = plt.subplots(figsize=(8.6, 4.6))
bars = ax1.bar(years, revenue, color="#0072CE", alpha=0.85, width=0.55,
               label="Revenue ($M)")
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 80, f"${v:,}", ha="center",
             fontsize=9, color="#0a2540")
ax1.set_ylabel("Revenue ($M)", color="#0072CE")
ax1.tick_params(axis="y", colors="#0072CE")
ax1.set_ylim(0, max(revenue) * 1.25)

ax2 = ax1.twinx()
mx = [i for i, v in enumerate(nongaap_op_margin) if v is not None]
my = [nongaap_op_margin[i] for i in mx]
ax2.plot([years[i] for i in mx], my, marker="o", linewidth=2.2,
         color="#E03127", label="Non-GAAP op. margin (%)")
for x_lbl, y in zip([years[i] for i in mx], my):
    ax2.annotate(f"{y:.1f}%", (x_lbl, y), textcoords="offset points",
                 xytext=(0, 10), ha="center", color="#E03127", fontsize=9)
ax2.set_ylabel("Non-GAAP operating margin (%)", color="#E03127")
ax2.tick_params(axis="y", colors="#E03127")
ax2.set_ylim(30, 55)

ax1.set_title("Arm Holdings — Revenue and non-GAAP operating margin, FY23–FY26",
              fontsize=11.5)
ax1.grid(axis="y", alpha=0.25)
fig.tight_layout()
save(fig, "arm_revenue_margin.png")


# ---------------------------------------------------------------------------
# 2. License vs. royalty revenue mix (stacked bar, FY23–FY26)
# ---------------------------------------------------------------------------
license_rev = [1004, 1431, 1839, 2307]
royalty_rev = [1675, 1802, 2168, 2613]

fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.bar(years, license_rev, label="License & other revenue", color="#0072CE",
       width=0.55)
ax.bar(years, royalty_rev, bottom=license_rev, label="Royalty revenue",
       color="#7AB800", width=0.55)
for i, (l, r) in enumerate(zip(license_rev, royalty_rev)):
    ax.text(i, l / 2, f"${l:,}", ha="center", va="center", color="white",
            fontsize=9, fontweight="bold")
    ax.text(i, l + r / 2, f"${r:,}", ha="center", va="center", color="white",
            fontsize=9, fontweight="bold")
    ax.text(i, l + r + 90, f"${l + r:,}", ha="center", color="#0a2540",
            fontsize=9)
ax.set_ylabel("Revenue ($M)")
ax.set_title("Arm Holdings — License vs. royalty revenue mix, FY23–FY26",
             fontsize=11.5)
ax.set_ylim(0, max(l + r for l, r in zip(license_rev, royalty_rev)) * 1.18)
ax.legend(loc="upper left", frameon=False)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
save(fig, "arm_revenue_mix.png")


# ---------------------------------------------------------------------------
# 3. Total Access (ATA) and Flexible Access licensee count over time
# ---------------------------------------------------------------------------
# ATA & AFA quarter-end counts disclosed in Arm's Q4 FY26 earnings
# release (year-over-year comparison Q4 FY25 → Q4 FY26).
quarters = ["Q4 FY25", "Q4 FY26"]
ata = [44, 56]  # ATA licensees, Q4 FY25 vs. Q4 FY26
afa = [314, 329]  # AFA licensees, Q4 FY25 vs. Q4 FY26

x = np.arange(len(quarters))
width = 0.36
fig, ax = plt.subplots(figsize=(8.6, 4.4))
b1 = ax.bar(x - width / 2, ata, width, color="#0072CE", label="Arm Total Access")
b2 = ax.bar(x + width / 2, afa, width, color="#7AB800",
            label="Arm Flexible Access")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 4,
                f"{int(b.get_height())}", ha="center", fontsize=9,
                color="#0a2540")
ax.set_xticks(x, quarters)
ax.set_ylabel("Licensees (count)")
ax.set_title("Arm Total Access vs. Arm Flexible Access licensees",
             fontsize=11.5)
ax.set_ylim(0, max(afa) * 1.18)
ax.legend(loc="upper left", frameon=False)
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
save(fig, "arm_subscription_licenses.png")


# ---------------------------------------------------------------------------
# 4. Peer valuation (TTM P/E and P/S, pulled 2026-05-20 via yfinance)
# ---------------------------------------------------------------------------
peers = ["ARM", "NVDA", "AVGO", "CDNS", "SNPS", "QCOM", "RMBS"]
pe = [298.0, 45.5, 81.5, 81.1, 75.4, 21.8, 63.1]
ps = [54.8, 25.0, 29.0, 17.4, 11.8, 4.8, 19.9]

x = np.arange(len(peers))
width = 0.4
fig, ax1 = plt.subplots(figsize=(9.0, 4.8))
b1 = ax1.bar(x - width / 2, pe, width, color="#0072CE", label="TTM P/E")
ax1.set_ylabel("TTM P/E (x)", color="#0072CE")
ax1.tick_params(axis="y", colors="#0072CE")
for b, v in zip(b1, pe):
    ax1.text(b.get_x() + b.get_width() / 2, v + 5, f"{v:.0f}x", ha="center",
             fontsize=9, color="#0a2540")

ax2 = ax1.twinx()
b2 = ax2.bar(x + width / 2, ps, width, color="#E03127", label="TTM P/S")
ax2.set_ylabel("TTM P/S (x)", color="#E03127")
ax2.tick_params(axis="y", colors="#E03127")
for b, v in zip(b2, ps):
    ax2.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}x", ha="center",
             fontsize=9, color="#0a2540")

ax1.set_xticks(x, peers)
ax1.set_title("Peer valuation comparison — TTM P/E vs. P/S "
              "(market data via yfinance, 2026-05-20)", fontsize=11)
ax1.grid(axis="y", alpha=0.2)
ax1.set_ylim(0, max(pe) * 1.18)
ax2.set_ylim(0, max(ps) * 1.25)
fig.tight_layout()
save(fig, "arm_peer_valuation.png")


# ---------------------------------------------------------------------------
# 5. Customer concentration pie (FY25, from 20-F risk factor disclosure)
# ---------------------------------------------------------------------------
# FY25 20-F:  top 5 customers = 56% of revenue; Arm China alone = 17%;
# Qualcomm individually = 10% (FY25).
# Remaining named-large customers are not separately disclosed.  We split the
# residual 56% among an "Other top-5 customers" wedge and "All other customers
# (~44%)".
labels = ["Arm China (17%)", "Qualcomm (10%)",
          "Other top-5 customers (~29%)", "All other customers (~44%)"]
sizes = [17, 10, 29, 44]
colors = ["#0072CE", "#E03127", "#FDB515", "#7AB800"]
fig, ax = plt.subplots(figsize=(7.6, 4.8))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct="%1.0f%%", startangle=90, colors=colors,
    wedgeprops=dict(width=0.45, edgecolor="white"))
for at in autotexts:
    at.set_color("white")
    at.set_fontweight("bold")
ax.set_title("Arm FY25 revenue by customer (top-5 = 56% of total)",
             fontsize=11.5)
fig.tight_layout()
save(fig, "arm_customer_mix.png")


# ---------------------------------------------------------------------------
# 6. Royalty revenue by end market — share of total royalty (FY25)
# ---------------------------------------------------------------------------
# Disclosed in the FY25 20-F:  mobile applications processors = ~46% of
# royalty.  Remaining 54% is split across other mobile chips, consumer
# electronics, industrial / IoT / embedded, networking, cloud compute,
# other infrastructure, and automotive.  The 20-F does not give exact splits
# for the remaining 54%; we therefore chart only the disclosed 46% slice and
# the residual lump-sum, with text annotations.
labels = ["Mobile app. processors\n(46% of royalty)",
          "Other end markets\n(~54%, not disaggregated)"]
sizes = [46, 54]
colors = ["#0072CE", "#9CA3AF"]
fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90, colors=colors,
       wedgeprops=dict(width=0.45, edgecolor="white"))
ax.set_title("Arm FY25 royalty revenue mix "
             "(source: 20-F, year ended March 31, 2025)", fontsize=11)
fig.tight_layout()
save(fig, "arm_royalty_mix.png")


# ---------------------------------------------------------------------------
# 7. ARM share price since IPO (Sep 2023) — monthly close
# ---------------------------------------------------------------------------
try:
    import yfinance as yf
    hist = yf.Ticker("ARM").history(period="3y", interval="1mo")
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    ax.plot(hist.index, hist["Close"], color="#0072CE", linewidth=2.0)
    ax.fill_between(hist.index, hist["Close"], color="#0072CE", alpha=0.12)
    ax.set_title("Arm Holdings (NASDAQ: ARM) — monthly close since IPO",
                 fontsize=11.5)
    ax.set_ylabel("Price ($)")
    ax.grid(alpha=0.3)
    # Annotate key events
    events = [
        ("2023-09-14", 51, "IPO @ $51"),
        ("2024-02-08", 113, "Q3 FY24 beat"),
        ("2026-04-21", 195, "Arm AGI CPU\nlaunch"),
    ]
    import pandas as pd
    for d, y, lbl in events:
        ax.annotate(lbl, xy=(pd.Timestamp(d, tz=hist.index.tz), y),
                    xytext=(10, 25), textcoords="offset points",
                    fontsize=9, color="#0a2540",
                    arrowprops=dict(arrowstyle="->", color="#9CA3AF"))
    fig.tight_layout()
    save(fig, "arm_price_history.png")
except Exception as e:
    print("price chart failed:", e)
