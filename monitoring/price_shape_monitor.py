"""
price_shape_monitor.py — detect the "skeleton" of a stock chart while ignoring small fluctuations.

Uses a ZigZag indicator: only records a pivot when price reverses by >= `threshold`%.
From the resulting pivot sequence it derives the dominant shape (uptrend, downtrend,
consolidation, V-bottom, inverted-V top, range, etc.).

Supported tickers
  A-share / HK : SZSE:002371  SSE:600519  HKEX:2513
  US stocks    : AAPL  NVDA  TSLA

Usage
  python price_shape_monitor.py SZSE:002371
  python price_shape_monitor.py AAPL --days 180 --threshold 8
"""

import sys
import argparse
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ──────────────────────────────────────────────
# Data fetching
# ──────────────────────────────────────────────

def fetch_ashare(code: str, exchange: str, days: int):
    """Fetch daily OHLCV for A-share / HK via akshare."""
    import akshare as ak
    end   = datetime.today()
    start = end - timedelta(days=days)
    fmt   = "%Y%m%d"

    if exchange.upper() in ("SZSE", "SSE"):
        # akshare expects pure 6-digit code
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start.strftime(fmt),
            end_date=end.strftime(fmt),
            adjust="qfq",          # forward-adjusted (复权)
        )
        df = df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close",
                                 "最高": "high", "最低": "low", "成交量": "volume"})
    elif exchange.upper() == "HKEX":
        df = ak.stock_hk_daily(symbol=code, adjust="qfq")
        df = df.rename(columns={"date": "date", "open": "open", "close": "close",
                                 "high": "high", "low": "low", "volume": "volume"})
        df = df[df["date"] >= start.strftime("%Y-%m-%d")]
    else:
        raise ValueError(f"Unknown exchange: {exchange}")

    df["date"] = np.array(df["date"], dtype="datetime64[D]")
    return df[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)


def fetch_us(ticker: str, days: int):
    """Fetch daily OHLCV for US stocks via yfinance."""
    import yfinance as yf
    end   = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False)
    df = df.reset_index()
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
    df = df.rename(columns={"adj close": "close"})
    df["date"] = np.array(df["date"], dtype="datetime64[D]")
    return df[["date", "open", "high", "low", "close", "volume"]].reset_index(drop=True)


def fetch_ohlcv(ticker: str, days: int = 365):
    if ":" in ticker:
        exchange, code = ticker.split(":", 1)
        return fetch_ashare(code, exchange, days), ticker
    else:
        return fetch_us(ticker, days), ticker


# ──────────────────────────────────────────────
# ZigZag indicator
# ──────────────────────────────────────────────

def zigzag(prices: np.ndarray, threshold: float = 5.0):
    """
    Return pivot indices and directions.

    threshold : minimum % reversal to count as a new pivot

    Returns
    -------
    pivot_idx : list[int]   — indices into `prices` of each pivot
    directions: list[int]   — +1 = peak, -1 = trough
    """
    if len(prices) < 3:
        return [], []

    pivot_idx  = [0]
    directions = [0]          # first pivot direction TBD

    last_pivot = prices[0]
    trend      = None          # None / 'up' / 'down'

    for i in range(1, len(prices)):
        p = prices[i]
        pct_change = (p - last_pivot) / last_pivot * 100

        if trend is None:
            if abs(pct_change) >= threshold:
                trend = 'up' if pct_change > 0 else 'down'
                pivot_idx.append(i)
                directions.append(+1 if trend == 'up' else -1)
                last_pivot = p
        elif trend == 'up':
            if p > last_pivot:               # extend the up-leg
                pivot_idx[-1]  = i
                last_pivot     = p
            elif (last_pivot - p) / last_pivot * 100 >= threshold:   # reversal
                trend = 'down'
                pivot_idx.append(i)
                directions.append(-1)
                last_pivot = p
        else:  # trend == 'down'
            if p < last_pivot:               # extend the down-leg
                pivot_idx[-1]  = i
                last_pivot     = p
            elif (p - last_pivot) / last_pivot * 100 >= threshold:   # reversal
                trend = 'up'
                pivot_idx.append(i)
                directions.append(+1)
                last_pivot = p

    # fix direction of the first pivot
    if len(pivot_idx) >= 2:
        directions[0] = -directions[1]      # opposite of the second pivot

    return pivot_idx, directions


# ──────────────────────────────────────────────
# Shape classification
# ──────────────────────────────────────────────

def classify_shape(pivot_idx, directions, prices):
    """
    Derive a human-readable shape label from the pivot sequence.
    """
    if len(pivot_idx) < 2:
        return "insufficient data"

    pivots = [(pivot_idx[i], directions[i], prices[pivot_idx[i]])
              for i in range(len(pivot_idx))]

    peaks   = [v for _, d, v in pivots if d == +1]
    troughs = [v for _, d, v in pivots if d == -1]
    n_legs  = len(pivots) - 1

    if n_legs == 0:
        return "flat"

    # -- simple 2-pivot shape (one swing)
    if n_legs == 1:
        chg = (pivots[-1][2] - pivots[0][2]) / pivots[0][2] * 100
        if chg > 0:
            return f"single upswing (+{chg:.1f}%)"
        else:
            return f"single downswing ({chg:.1f}%)"

    # -- trending: check if consecutive peaks/troughs are rising or falling
    def slope_sign(seq):
        if len(seq) < 2:
            return 0
        diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
        up   = sum(1 for d in diffs if d > 0)
        down = sum(1 for d in diffs if d < 0)
        if up > down * 1.5:
            return +1
        if down > up * 1.5:
            return -1
        return 0

    peak_slope   = slope_sign(peaks)
    trough_slope = slope_sign(troughs)

    overall_chg = (prices[pivot_idx[-1]] - prices[pivot_idx[0]]) / prices[pivot_idx[0]] * 100

    if peak_slope == +1 and trough_slope == +1:
        return f"uptrend  (HH+HL, {overall_chg:+.1f}% net)"
    if peak_slope == -1 and trough_slope == -1:
        return f"downtrend  (LH+LL, {overall_chg:+.1f}% net)"
    if peak_slope == -1 and trough_slope == +1:
        return f"converging / symmetrical triangle  ({overall_chg:+.1f}% net)"
    if peak_slope == +1 and trough_slope == -1:
        return f"expanding / megaphone pattern  ({overall_chg:+.1f}% net)"

    # -- special patterns (need ≥ 5 pivots)
    if n_legs >= 4:
        vals = [v for _, _, v in pivots]
        mid  = len(vals) // 2
        left_min  = min(vals[:mid])
        right_min = min(vals[mid:])
        left_max  = max(vals[:mid])
        right_max = max(vals[mid:])

        # Cup: low in the middle
        if vals[0] > vals[mid] and vals[-1] > vals[mid]:
            return f"cup / V-recovery  ({overall_chg:+.1f}% net)"

        # Inverted cup: high in the middle
        if vals[0] < vals[mid] and vals[-1] < vals[mid]:
            return f"rounded top / hill  ({overall_chg:+.1f}% net)"

    # consolidation / sideways
    price_range_pct = (max(prices[pivot_idx[-1]], prices[pivot_idx[0]]) /
                       min(prices[pivot_idx[-1]], prices[pivot_idx[0]]) - 1) * 100
    if abs(overall_chg) < 10 and price_range_pct < 20:
        return f"consolidation / sideways  ({overall_chg:+.1f}% net)"

    return f"mixed  ({overall_chg:+.1f}% net)"


# ──────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────

def plot(df, pivot_idx, directions, ticker, shape_label, threshold):
    dates  = df["date"].values.astype("datetime64[D]").astype(object)
    closes = df["close"].values.astype(float)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                   gridspec_kw={"height_ratios": [3, 1]},
                                   sharex=True)
    fig.suptitle(f"{ticker}   —   Shape: {shape_label}\n"
                 f"ZigZag threshold {threshold}%   |   {len(df)} trading days",
                 fontsize=12)

    # — price line (thin, semi-transparent)
    ax1.plot(dates, closes, color="#aaaaaa", linewidth=0.8, alpha=0.7, label="Close")

    # — ZigZag skeleton
    if pivot_idx:
        zz_dates  = [dates[i]  for i in pivot_idx]
        zz_prices = [closes[i] for i in pivot_idx]
        ax1.plot(zz_dates, zz_prices, color="#e65c00", linewidth=2.0,
                 label=f"ZigZag (≥{threshold}%)")

        # scatter peaks / troughs
        peak_dates   = [dates[pivot_idx[i]]  for i, d in enumerate(directions) if d == +1]
        peak_prices  = [closes[pivot_idx[i]] for i, d in enumerate(directions) if d == +1]
        trough_dates = [dates[pivot_idx[i]]  for i, d in enumerate(directions) if d == -1]
        trough_prices= [closes[pivot_idx[i]] for i, d in enumerate(directions) if d == -1]

        ax1.scatter(peak_dates,   peak_prices,   color="#d62728", s=60, zorder=5, label="Peak")
        ax1.scatter(trough_dates, trough_prices, color="#1f77b4", s=60, zorder=5, label="Trough")

    ax1.set_ylabel("Price")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(True, alpha=0.3)

    # — volume bars
    volume = df["volume"].values.astype(float)
    colors = ["#d62728" if closes[i] >= df["open"].values[i] else "#1f77b4"
              for i in range(len(df))]
    ax2.bar(dates, volume, color=colors, width=0.8, alpha=0.7)
    ax2.set_ylabel("Volume")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    out = f"price_shape_{ticker.replace(':', '_')}.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"  Chart saved → {out}")
    plt.show()


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Stock price shape monitor (ZigZag)")
    parser.add_argument("ticker",              help="e.g. SZSE:002371 or AAPL")
    parser.add_argument("--days",      type=int,   default=365,
                        help="Look-back window in calendar days (default 365)")
    parser.add_argument("--threshold", type=float, default=5.0,
                        help="Minimum %% reversal to count as a pivot (default 5)")
    parser.add_argument("--no-plot",   action="store_true",
                        help="Skip chart rendering")
    args = parser.parse_args()

    print(f"\nFetching {args.ticker}  ({args.days} days) …")
    df, label = fetch_ohlcv(args.ticker, days=args.days)
    print(f"  {len(df)} rows  |  {df['date'].iloc[0]} → {df['date'].iloc[-1]}")

    closes = df["close"].values.astype(float)
    pivot_idx, directions = zigzag(closes, threshold=args.threshold)

    shape = classify_shape(pivot_idx, directions, closes)
    print(f"\n  Pivots detected : {len(pivot_idx)}")
    print(f"  Shape           : {shape}\n")

    # Print pivot table
    if pivot_idx:
        print(f"  {'#':>3}  {'Date':12}  {'Price':>10}  {'Type':8}")
        print(f"  {'─'*3}  {'─'*12}  {'─'*10}  {'─'*8}")
        for rank, (idx, direction) in enumerate(zip(pivot_idx, directions), 1):
            kind = "PEAK  ▲" if direction == +1 else "TROUGH▼"
            print(f"  {rank:>3}  {str(df['date'].iloc[idx]):12}  {closes[idx]:>10.2f}  {kind}")

    if not args.no_plot:
        plot(df, pivot_idx, directions, label, shape, args.threshold)


if __name__ == "__main__":
    main()
