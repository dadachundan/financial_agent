#!/usr/bin/env python3
"""Generate VST research report charts."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent
plt.rcParams.update({'figure.dpi': 150, 'savefig.bbox': 'tight', 'font.size': 11})

# ─────────────────────────────────────────────────────────────────────────────
# 1) Capacity by fuel (MW) — bar chart  (10-K FY2025, p.1)
# ─────────────────────────────────────────────────────────────────────────────
fuels = ['Natural Gas', 'Coal', 'Nuclear', 'Solar / Battery', 'Fuel Oil']
mw    = [26989, 8743, 6448, 1274, 187]
pct   = [62, 20, 15, 3, 0.4]
colors = ['#3a86ff', '#6c757d', '#fb8500', '#2a9d8f', '#adb5bd']

fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.bar(fuels, mw, color=colors, edgecolor='black', linewidth=0.6)
for b, p in zip(bars, pct):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 400,
            f'{b.get_height():,}\n({p}%)', ha='center', fontsize=10)
ax.set_ylabel('Net capacity (MW)')
ax.set_title('Vistra Generation Capacity by Fuel — 43,641 MW total (FY2025)')
ax.set_ylim(0, 32000)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.savefig(OUT / 'vst_capacity_by_fuel.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 2) Capacity by ISO / segment  — pie
# ─────────────────────────────────────────────────────────────────────────────
seg   = ['Texas (ERCOT)\n19,858 MW', 'East (PJM/ISO-NE/MISO/NYISO)\n22,254 MW', 'West (CAISO)\n1,529 MW']
sizes = [19858, 22254, 1529]
fig, ax = plt.subplots(figsize=(8, 5.2))
ax.pie(sizes, labels=seg, autopct='%1.0f%%', startangle=90,
       colors=['#fb8500', '#3a86ff', '#2a9d8f'],
       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax.set_title('Vistra Generation by Market / ISO (FY2025, MW)')
plt.savefig(OUT / 'vst_capacity_by_market.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 3) Revenue & Adjusted EBITDA trend (2021-2025) + 2026 mid guidance
# ─────────────────────────────────────────────────────────────────────────────
yrs   = ['2022', '2023', '2024', '2025', '2026E (guide)']
rev   = [13728, 14779, 17224, 17738, None]                     # USD mm; per 10-K consolidated statements
ebitda = [1812, 3437, 5539, 4775, 7200]                        # Adj EBITDA: 2024-25 from 10-K; 2026 mid = $6.8-$7.6B from Q1-26 earnings release
fig, ax1 = plt.subplots(figsize=(9.5, 5))
x = np.arange(len(yrs))
bars = ax1.bar(x[:-1], rev[:-1], width=0.55, color='#3a86ff',
               edgecolor='black', linewidth=0.6, label='Revenue (USD mm)')
ax1.set_ylabel('Revenue (USD mm)', color='#3a86ff')
ax1.set_xticks(x); ax1.set_xticklabels(yrs); ax1.tick_params(axis='y', colors='#3a86ff')
for b, v in zip(bars, rev[:-1]):
    ax1.text(b.get_x()+b.get_width()/2, b.get_height()+300, f'${v/1000:.1f}B', ha='center', fontsize=9)

ax2 = ax1.twinx()
line, = ax2.plot(x, ebitda, color='#e63946', marker='o', linewidth=2.2,
                 markersize=8, label='Adjusted EBITDA (USD mm)')
ax2.set_ylabel('Adjusted EBITDA (USD mm)', color='#e63946')
ax2.tick_params(axis='y', colors='#e63946')
for xi, v in zip(x, ebitda):
    label_str = f'${v/1000:.1f}B' + (' (mid)' if xi==len(yrs)-1 else '')
    ax2.text(xi, v+250, label_str, ha='center', color='#e63946', fontsize=9)

ax1.set_title('Vistra Revenue and Adjusted EBITDA (2021–2025, 2026 guidance mid)')
ax1.spines['top'].set_visible(False); ax2.spines['top'].set_visible(False)
plt.savefig(OUT / 'vst_rev_ebitda_trend.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 4) Peer comparison — TTM P/E, Forward P/E, EV/EBITDA  (yfinance pulled 2026-05-21)
# ─────────────────────────────────────────────────────────────────────────────
peers     = ['VST', 'TLN',   'CEG',  'NRG',  'DUK',  'AEP']
ttm_pe    = [24.8, np.nan,  25.0,   149.9,  19.1,   19.1]   # TLN: profitable but small base; NRG distorted by one-offs
fwd_pe    = [13.4, 10.5,    21.2,   12.0,   17.3,   18.9]
evebitda  = [10.4, 32.8,    15.5,   23.1,   11.4,   13.4]

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.5))
colors_p = ['#fb8500'] + ['#6c757d']*5

axes[0].bar(peers, [v if not np.isnan(v) else 0 for v in ttm_pe], color=colors_p, edgecolor='black', linewidth=0.6)
axes[0].set_title('TTM P/E')
for i, v in enumerate(ttm_pe):
    label = 'n/m' if np.isnan(v) else f'{v:.1f}x'
    axes[0].text(i, (v if not np.isnan(v) else 5) + 3, label, ha='center', fontsize=9)
axes[0].set_ylim(0, 170)

axes[1].bar(peers, fwd_pe, color=colors_p, edgecolor='black', linewidth=0.6)
axes[1].set_title('Forward P/E')
for i, v in enumerate(fwd_pe):
    axes[1].text(i, v+0.4, f'{v:.1f}x', ha='center', fontsize=9)
axes[1].set_ylim(0, 25)

axes[2].bar(peers, evebitda, color=colors_p, edgecolor='black', linewidth=0.6)
axes[2].set_title('EV / EBITDA')
for i, v in enumerate(evebitda):
    axes[2].text(i, v+0.6, f'{v:.1f}x', ha='center', fontsize=9)
axes[2].set_ylim(0, 38)

for ax in axes:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.suptitle('Vistra vs IPP / Utility Peers (multiples as of 2026-05-21)', y=1.04)
plt.tight_layout()
plt.savefig(OUT / 'vst_peer_multiples.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retail customers — Vistra now serves ~5 million (Texas 2.6M of that)
# ─────────────────────────────────────────────────────────────────────────────
labels = ['Texas (TXU Energy, Ambit)\n~2.6M', 'Northeast / Midwest /\nMid-Atlantic (Dynegy ES, Homefield,\nEnergy Harbor, USG&E, Public Power)\n~2.4M']
sizes  = [2.6, 2.4]
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90,
       colors=['#fb8500', '#3a86ff'],
       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax.set_title('Vistra Retail Customers by Region (~5M total, FY2025)')
plt.savefig(OUT / 'vst_retail_customers.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 6) Hyperscaler PPA disclosed exposure — bar chart
# ─────────────────────────────────────────────────────────────────────────────
deals  = ['AWS\n@ Comanche Peak\n(announced Sep-2025)',
          'Meta - operating\n@ Perry / Davis-Besse\n(announced Jan-2026)',
          'Meta - uprates\n@ Perry / Davis-Besse /\nBeaver Valley\n(announced Jan-2026)']
mw_ppa = [1200, 2176, 433]
years  = ['delivery 4Q-2027,\nfull by 2032', 'delivery starts late-2026,\nfull by YE-2027', 'uprate delivery\n2031 → YE-2034']
fig, ax = plt.subplots(figsize=(10, 4.5))
bars = ax.bar(deals, mw_ppa, color=['#fb8500', '#2a9d8f', '#06a77d'], edgecolor='black', linewidth=0.6)
for b, v, y in zip(bars, mw_ppa, years):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+50, f'{v:,} MW', ha='center', fontsize=11, fontweight='bold')
    ax.text(b.get_x()+b.get_width()/2, b.get_height()/2, y, ha='center', va='center', fontsize=9, color='white')
ax.set_ylabel('Contracted MW')
ax.set_title('Vistra disclosed long-term hyperscaler PPAs — 3,809 MW total\n(20-year nuclear PPAs; not all online today)')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_ylim(0, 2700)
plt.savefig(OUT / 'vst_hyperscaler_ppa.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 7) Segment Adjusted EBITDA mix (FY2025 vs FY2024)
# ─────────────────────────────────────────────────────────────────────────────
# 2025 Adj EBITDA (from 10-K segment table): Retail 1,486; Texas 1,757; East 2,489; West 248; Corp -141; Asset Closure -279
# 2024 Adj EBITDA: Retail 1,463; Texas 2,032; East 2,017; West 225; Corp -94; Asset Closure -104
segs   = ['Retail', 'Texas', 'East', 'West', 'Asset Closure', 'Corp/Other']
y2024  = [1463, 2032, 2017, 225, -104, -94]
y2025  = [1486, 1757, 2489, 248, -279, -141]
x = np.arange(len(segs))
w = 0.38
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - w/2, y2024, w, color='#6c757d', label='FY2024 Adjusted EBITDA', edgecolor='black', linewidth=0.5)
ax.bar(x + w/2, y2025, w, color='#fb8500', label='FY2025 Adjusted EBITDA', edgecolor='black', linewidth=0.5)
for i, (a, b) in enumerate(zip(y2024, y2025)):
    ax.text(i-w/2, a + (60 if a>=0 else -120), f'{a:,}', ha='center', fontsize=8)
    ax.text(i+w/2, b + (60 if b>=0 else -120), f'{b:,}', ha='center', fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(segs)
ax.set_ylabel('Adjusted EBITDA (USD mm)')
ax.set_title('Adjusted EBITDA by Segment, FY2024 vs FY2025')
ax.axhline(0, color='black', lw=0.6)
ax.legend(loc='upper right')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.savefig(OUT / 'vst_segment_ebitda.png'); plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# 8) M&A / capacity timeline — bar showing capacity added per deal
# ─────────────────────────────────────────────────────────────────────────────
deals2 = ['Dynegy merger\n(2018)', 'Energy Harbor\n(Mar-2024)', 'Lotus\n(Oct-2025)', 'Cogentrix\n(pending,\nmid/late-2026)']
mw_add = [13700, 4000, 2600, 5500]
colors2 = ['#adb5bd', '#fb8500', '#3a86ff', '#2a9d8f']
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(deals2, mw_add, color=colors2, edgecolor='black', linewidth=0.6)
for b, v in zip(bars, mw_add):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+200, f'~{v:,} MW', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('Approx. capacity added (MW)')
ax.set_title('Vistra Major Capacity-Adding M&A — 2018 to pending 2026')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_ylim(0, 16000)
plt.savefig(OUT / 'vst_ma_timeline.png'); plt.close()

print('Charts generated:')
for p in sorted(OUT.glob('*.png')):
    print('  ', p.name, p.stat().st_size, 'bytes')
