#!/usr/bin/env python3
"""Technical indicators via yfinance + stockstats.

Supports a comma-separated list of indicators (one call per name; outputs joined with blank lines).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
from stockstats import wrap

INDICATOR_DESC = {
    "close_50_sma": "50 SMA: medium-term trend; dynamic support/resistance. Lags price; combine with faster indicators.",
    "close_200_sma": "200 SMA: long-term trend; confirms golden/death cross setups. Slow-reacting.",
    "close_10_ema": "10 EMA: responsive short-term average for quick momentum shifts. Noisy in choppy markets.",
    "macd": "MACD: momentum via EMA differences. Look for crossovers and divergence.",
    "macds": "MACD Signal: EMA smoothing of MACD. Crossovers with MACD line trigger trades.",
    "macdh": "MACD Histogram: MACD minus signal. Shows momentum strength; spot divergence early.",
    "rsi": "RSI: overbought/oversold via 70/30 thresholds. In strong trends RSI may stay extreme.",
    "boll": "Bollinger middle (20 SMA): dynamic benchmark; combine with bands.",
    "boll_ub": "Bollinger upper (+2 sigma): overbought / breakout zone signal.",
    "boll_lb": "Bollinger lower (-2 sigma): oversold signal.",
    "atr": "ATR: Average True Range; for stop-loss levels and position sizing.",
    "vwma": "VWMA: volume-weighted moving average. Confirms trends with volume.",
    "mfi": "MFI: Money Flow Index, momentum using price + volume. >80 overbought, <20 oversold.",
}


def _load_ohlcv(symbol: str, curr_date: str) -> pd.DataFrame:
    today = pd.Timestamp.today()
    start = today - pd.DateOffset(years=5)
    df = yf.download(
        symbol,
        start=start.strftime("%Y-%m-%d"),
        end=today.strftime("%Y-%m-%d"),
        multi_level_index=False,
        progress=False,
        auto_adjust=True,
    ).reset_index()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    for col in ("Open", "High", "Low", "Close", "Volume"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Close"])
    return df[df["Date"] <= pd.Timestamp(curr_date)]


def _compute(symbol: str, indicator: str, curr_date: str, look_back_days: int) -> str:
    if indicator not in INDICATOR_DESC:
        raise ValueError(
            f"Indicator '{indicator}' not supported. Choose from: {sorted(INDICATOR_DESC)}"
        )
    df = _load_ohlcv(symbol, curr_date)
    if df.empty:
        return f"## {indicator}: no OHLCV data available for {symbol}"
    sdf = wrap(df.copy())
    sdf["Date"] = pd.to_datetime(sdf["Date"]).dt.strftime("%Y-%m-%d")
    sdf[indicator]  # trigger stockstats to compute
    values = dict(zip(sdf["Date"], sdf[indicator]))

    end_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    before = end_dt - relativedelta(days=look_back_days)

    rows = []
    cursor = end_dt
    while cursor >= before:
        key = cursor.strftime("%Y-%m-%d")
        v = values.get(key)
        if v is None:
            v = "N/A: not a trading day"
        elif pd.isna(v):
            v = "N/A"
        rows.append(f"{key}: {v}")
        cursor -= relativedelta(days=1)

    return (
        f"## {indicator} values from {before:%Y-%m-%d} to {curr_date}:\n\n"
        + "\n".join(rows)
        + f"\n\n{INDICATOR_DESC[indicator]}"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch technical indicators for a ticker.")
    p.add_argument("ticker")
    p.add_argument("trade_date")
    p.add_argument("--indicators", required=True, help="Comma-separated names, e.g. close_50_sma,macd,rsi")
    p.add_argument("--look-back-days", type=int, default=30)
    a = p.parse_args()

    blocks = []
    for name in [n.strip().lower() for n in a.indicators.split(",") if n.strip()]:
        try:
            blocks.append(_compute(a.ticker.upper(), name, a.trade_date, a.look_back_days))
        except ValueError as exc:
            blocks.append(str(exc))
    print("\n\n".join(blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
