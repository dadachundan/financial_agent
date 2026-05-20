#!/usr/bin/env python3
"""Insider transactions via yfinance."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import yfinance as yf


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch insider transactions for a ticker.")
    p.add_argument("ticker")
    a = p.parse_args()

    try:
        df = yf.Ticker(a.ticker.upper()).insider_transactions
    except Exception as exc:
        print(f"Error retrieving insider transactions for {a.ticker}: {exc}")
        return 0

    if df is None or df.empty:
        print(f"No insider transactions data found for '{a.ticker}'")
        return 0

    print(f"# Insider Transactions data for {a.ticker.upper()}")
    print(f"# Data retrieved on: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print()
    print(df.to_csv())
    return 0


if __name__ == "__main__":
    sys.exit(main())
