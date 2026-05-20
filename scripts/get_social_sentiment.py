#!/usr/bin/env python3
"""Social sentiment from StockTwits and Reddit (no API keys required)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)
_UA = "financial_agent/0.1 (+local research)"

STOCKTWITS_API = "https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"
REDDIT_API = "https://www.reddit.com/r/{sub}/search.json?{qs}"
DEFAULT_SUBREDDITS = ("wallstreetbets", "stocks", "investing")


def fetch_stocktwits(ticker: str, limit: int = 30, timeout: float = 10.0) -> str:
    url = STOCKTWITS_API.format(ticker=ticker.upper())
    req = Request(url, headers={"User-Agent": _UA, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except (HTTPError, URLError, json.JSONDecodeError, TimeoutError) as exc:
        logger.warning("StockTwits fetch failed for %s: %s", ticker, exc)
        return f"<stocktwits unavailable: {type(exc).__name__}>"

    messages = data.get("messages", []) if isinstance(data, dict) else []
    if not messages:
        return f"<no StockTwits messages found for ${ticker.upper()}>"

    bullish = bearish = unlabeled = 0
    lines = []
    for m in messages[:limit]:
        created = m.get("created_at", "")
        user = (m.get("user") or {}).get("username", "?")
        sentiment_obj = (m.get("entities") or {}).get("sentiment") or {}
        sentiment = sentiment_obj.get("basic") if isinstance(sentiment_obj, dict) else None
        body = (m.get("body") or "").replace("\n", " ").strip()
        if len(body) > 280:
            body = body[:280] + "…"
        if sentiment == "Bullish":
            bullish += 1; tag = "Bullish"
        elif sentiment == "Bearish":
            bearish += 1; tag = "Bearish"
        else:
            unlabeled += 1; tag = "no-label"
        lines.append(f"[{created} · @{user} · {tag}] {body}")

    total = bullish + bearish + unlabeled
    bp = round(100 * bullish / total) if total else 0
    rp = round(100 * bearish / total) if total else 0
    summary = (
        f"Bullish: {bullish} ({bp}%) · Bearish: {bearish} ({rp}%) · "
        f"Unlabeled: {unlabeled} · Total: {total} most-recent messages"
    )
    return summary + "\n\n" + "\n".join(lines)


def _fetch_subreddit(ticker: str, sub: str, limit: int, timeout: float) -> list[dict]:
    qs = urlencode({
        "q": ticker, "restrict_sr": "on", "sort": "new", "t": "week", "limit": limit,
    })
    url = REDDIT_API.format(sub=sub, qs=qs)
    req = Request(url, headers={"User-Agent": _UA, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read())
    except (HTTPError, URLError, json.JSONDecodeError, TimeoutError) as exc:
        logger.warning("Reddit fetch failed for r/%s · %s: %s", sub, ticker, exc)
        return []
    children = (payload.get("data") or {}).get("children") or []
    return [c.get("data", {}) for c in children if isinstance(c, dict)]


def fetch_reddit(ticker: str, subreddits: Iterable[str] = DEFAULT_SUBREDDITS,
                 limit_per_sub: int = 5, timeout: float = 10.0,
                 inter_delay: float = 0.4) -> str:
    blocks, total = [], 0
    for i, sub in enumerate(subreddits):
        if i > 0:
            time.sleep(inter_delay)
        posts = _fetch_subreddit(ticker, sub, limit_per_sub, timeout)
        total += len(posts)
        if not posts:
            blocks.append(f"r/{sub}: <no posts found mentioning {ticker.upper()} in the past 7 days>")
            continue
        lines = [f"r/{sub} — {len(posts)} recent posts mentioning {ticker.upper()}:"]
        for p in posts:
            title = (p.get("title") or "").replace("\n", " ").strip()
            score = p.get("score", 0)
            comments = p.get("num_comments", 0)
            created = p.get("created_utc")
            created_str = time.strftime("%Y-%m-%d", time.gmtime(created)) if created else "?"
            selftext = (p.get("selftext") or "").replace("\n", " ").strip()
            if len(selftext) > 240:
                selftext = selftext[:240] + "…"
            lines.append(
                f"  [{created_str} · {score:>4}↑ · {comments:>3}c] {title}"
                + (f"\n    body excerpt: {selftext}" if selftext else "")
            )
        blocks.append("\n".join(lines))
    if total == 0:
        return (
            f"<no Reddit posts found mentioning {ticker.upper()} across "
            f"{', '.join(f'r/{s}' for s in subreddits)} in the past 7 days>"
        )
    return "\n\n".join(blocks)


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch social sentiment from StockTwits or Reddit.")
    p.add_argument("source", choices=["stocktwits", "reddit"])
    p.add_argument("ticker")
    p.add_argument("--limit", type=int, default=30, help="Max items (StockTwits only).")
    a = p.parse_args()

    if a.source == "stocktwits":
        print(fetch_stocktwits(a.ticker, limit=a.limit))
    else:
        print(fetch_reddit(a.ticker))
    return 0


if __name__ == "__main__":
    sys.exit(main())
