#!/usr/bin/env python3
"""Company fundamentals via yfinance.

--view selects: profile | balance_sheet | cashflow | income_statement
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import pandas as pd
import yfinance as yf

PROFILE_FIELDS = [
    ("Name", "longName"), ("Sector", "sector"), ("Industry", "industry"),
    ("Market Cap", "marketCap"), ("PE Ratio (TTM)", "trailingPE"),
    ("Forward PE", "forwardPE"), ("PEG Ratio", "pegRatio"),
    ("Price to Book", "priceToBook"), ("EPS (TTM)", "trailingEps"),
    ("Forward EPS", "forwardEps"), ("Dividend Yield", "dividendYield"),
    ("Beta", "beta"), ("52 Week High", "fiftyTwoWeekHigh"),
    ("52 Week Low", "fiftyTwoWeekLow"), ("50 Day Average", "fiftyDayAverage"),
    ("200 Day Average", "twoHundredDayAverage"), ("Revenue (TTM)", "totalRevenue"),
    ("Gross Profit", "grossProfits"), ("EBITDA", "ebitda"),
    ("Net Income", "netIncomeToCommon"), ("Profit Margin", "profitMargins"),
    ("Operating Margin", "operatingMargins"), ("Return on Equity", "returnOnEquity"),
    ("Return on Assets", "returnOnAssets"), ("Debt to Equity", "debtToEquity"),
    ("Current Ratio", "currentRatio"), ("Book Value", "bookValue"),
    ("Free Cash Flow", "freeCashflow"),
]

STATEMENT_ATTRS = {
    "balance_sheet": ("quarterly_balance_sheet", "balance_sheet"),
    "cashflow": ("quarterly_cashflow", "cashflow"),
    "income_statement": ("quarterly_income_stmt", "income_stmt"),
}


def _filter_by_date(df: pd.DataFrame, curr_date: str) -> pd.DataFrame:
    """Drop fiscal-period columns after curr_date to prevent look-ahead bias."""
    if not curr_date or df is None or df.empty:
        return df
    cutoff = pd.Timestamp(curr_date)
    mask = pd.to_datetime(df.columns, errors="coerce") <= cutoff
    return df.loc[:, mask]


def _profile(ticker_obj, ticker: str) -> str:
    try:
        info = ticker_obj.info or {}
    except Exception as exc:
        return f"Error retrieving fundamentals for {ticker}: {exc}"
    if not info:
        return f"No fundamentals data found for symbol '{ticker}'"
    lines = [
        f"# Company Fundamentals for {ticker}",
        f"# Data retrieved on: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
    ]
    for label, key in PROFILE_FIELDS:
        v = info.get(key)
        if v is not None:
            lines.append(f"{label}: {v}")
    return "\n".join(lines)


def _statement(ticker_obj, ticker: str, view: str, freq: str, curr_date: str) -> str:
    qa, an = STATEMENT_ATTRS[view]
    try:
        df = getattr(ticker_obj, qa if freq == "quarterly" else an)
    except Exception as exc:
        return f"Error retrieving {view} for {ticker}: {exc}"
    df = _filter_by_date(df, curr_date)
    if df is None or df.empty:
        return f"No {view.replace('_', ' ')} data found for '{ticker}'"
    title = view.replace("_", " ").title()
    return (
        f"# {title} data for {ticker} ({freq})\n"
        f"# Data retrieved on: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
        + df.to_csv()
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch company fundamentals.")
    p.add_argument("ticker")
    p.add_argument("--view", required=True, choices=["profile", *STATEMENT_ATTRS.keys()])
    p.add_argument("--trade-date", default=datetime.today().strftime("%Y-%m-%d"))
    p.add_argument("--freq", default="quarterly", choices=["quarterly", "annual"])
    a = p.parse_args()

    t = yf.Ticker(a.ticker.upper())
    if a.view == "profile":
        print(_profile(t, a.ticker.upper()))
    else:
        print(_statement(t, a.ticker.upper(), a.view, a.freq, a.trade_date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
