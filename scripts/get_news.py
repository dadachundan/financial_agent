#!/usr/bin/env python3
"""Ticker-specific news via yfinance."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from dateutil.relativedelta import relativedelta
import yfinance as yf

DEFAULT_LIMIT = 50


def _extract(article: dict) -> dict:
    c = article.get("content", article)
    title = c.get("title", "No title")
    summary = c.get("summary", "")
    publisher = (c.get("provider") or {}).get("displayName") or article.get("publisher", "Unknown")
    url = ((c.get("canonicalUrl") or c.get("clickThroughUrl") or {}) or {}).get("url") or article.get("link", "")
    pub_date = None
    pub_str = c.get("pubDate") or ""
    if pub_str:
        try:
            pub_date = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except ValueError:
            pass
    return {"title": title, "summary": summary, "publisher": publisher, "link": url, "pub_date": pub_date}


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch ticker-specific news for a date window.")
    p.add_argument("ticker")
    p.add_argument("start_date")
    p.add_argument("end_date")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    a = p.parse_args()

    try:
        news = yf.Ticker(a.ticker).get_news(count=a.limit) or []
    except Exception as exc:
        print(f"Error fetching news for {a.ticker}: {exc}")
        return 0

    start = datetime.strptime(a.start_date, "%Y-%m-%d")
    end = datetime.strptime(a.end_date, "%Y-%m-%d") + relativedelta(days=1)

    out = []
    for art in news:
        d = _extract(art)
        if d["pub_date"]:
            naive = d["pub_date"].replace(tzinfo=None)
            if not (start <= naive <= end):
                continue
        date_str = d["pub_date"].strftime("%Y-%m-%d") if d["pub_date"] else "date unknown"
        block = f"### {d['title']} (source: {d['publisher']}, {date_str})\n"
        if d["summary"]:
            block += f"{d['summary']}\n"
        if d["link"]:
            block += f"Link: {d['link']}\n"
        out.append(block + "\n")

    if not out:
        print(f"No news found for {a.ticker} between {a.start_date} and {a.end_date}")
        return 0
    print(f"## {a.ticker} News, from {a.start_date} to {a.end_date}:\n")
    print("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
