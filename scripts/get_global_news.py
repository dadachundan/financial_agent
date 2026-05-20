#!/usr/bin/env python3
"""Global/macro news via yfinance Search."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from dateutil.relativedelta import relativedelta
import yfinance as yf

QUERIES = [
    "Federal Reserve interest rates inflation",
    "S&P 500 earnings GDP economic outlook",
    "geopolitical risk trade war sanctions",
    "ECB Bank of England BOJ central bank policy",
    "oil commodities supply chain energy",
]


def _extract(article: dict) -> dict:
    c = article.get("content", article)
    title = c.get("title") or article.get("title", "No title")
    publisher = (c.get("provider") or {}).get("displayName") or article.get("publisher", "Unknown")
    url = ((c.get("canonicalUrl") or c.get("clickThroughUrl") or {}) or {}).get("url") or article.get("link", "")
    summary = c.get("summary", "")
    pub_date = None
    pub_str = c.get("pubDate") or ""
    if pub_str:
        try:
            pub_date = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        except ValueError:
            pass
    return {"title": title, "publisher": publisher, "link": url, "summary": summary, "pub_date": pub_date}


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch global / macro news.")
    p.add_argument("trade_date")
    p.add_argument("--look-back-days", type=int, default=7)
    p.add_argument("--limit", type=int, default=30)
    a = p.parse_args()

    curr = datetime.strptime(a.trade_date, "%Y-%m-%d")
    start = (curr - relativedelta(days=a.look_back_days)).strftime("%Y-%m-%d")
    cutoff = curr + relativedelta(days=1)

    seen, all_news = set(), []
    for q in QUERIES:
        try:
            s = yf.Search(query=q, news_count=a.limit, enable_fuzzy_query=True)
            for art in (s.news or []):
                d = _extract(art)
                if d["title"] and d["title"] not in seen:
                    seen.add(d["title"])
                    all_news.append(d)
        except Exception as exc:
            sys.stderr.write(f"Warning: search '{q}' failed: {exc}\n")
        if len(all_news) >= a.limit:
            break

    if not all_news:
        print(f"No global news found for {a.trade_date}")
        return 0

    lines = []
    for d in all_news[:a.limit]:
        if d["pub_date"] and d["pub_date"].replace(tzinfo=None) > cutoff:
            continue
        block = f"### {d['title']} (source: {d['publisher']})\n"
        if d["summary"]:
            block += f"{d['summary']}\n"
        if d["link"]:
            block += f"Link: {d['link']}\n"
        lines.append(block + "\n")

    print(f"## Global Market News, from {start} to {a.trade_date}:\n")
    print("".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
