#!/usr/bin/env python3
"""OHLCV stock price data via yfinance."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta

import yfinance as yf


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch OHLCV stock data for a ticker.")
    p.add_argument("ticker", help="Ticker symbol, e.g. NVDA or BTC-USD")
    p.add_argument("trade_date", help="End date YYYY-MM-DD")
    p.add_argument("--look-back-days", type=int, default=90, help="History window in days (default 90).")
    p.add_argument("--start-date", help="Explicit start_date YYYY-MM-DD (overrides --look-back-days).")
    a = p.parse_args()

    end = a.trade_date
    start = a.start_date or (
        datetime.strptime(end, "%Y-%m-%d") - timedelta(days=a.look_back_days)
    ).strftime("%Y-%m-%d")

    df = yf.Ticker(a.ticker.upper()).history(start=start, end=end)
    if df.empty:
        print(f"No data found for '{a.ticker}' between {start} and {end}")
        return 0

    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    for c in ("Open", "High", "Low", "Close", "Adj Close"):
        if c in df.columns:
            df[c] = df[c].round(2)

    print(f"# Stock data for {a.ticker.upper()} from {start} to {end}")
    print(f"# Total records: {len(df)}")
    print(f"# Data retrieved on: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print()
    print(df.to_csv())
    return 0


if __name__ == "__main__":
    sys.exit(main())
