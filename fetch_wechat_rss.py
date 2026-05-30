#!/usr/bin/env python3
"""
Fetch articles from Wechat2RSS feeds (https://wechat2rss.xlab.app/).

Usage:
    # One-off, one feed:
    python3 fetch_wechat_rss.py https://wechat2rss.xlab.app/feed/<hash>.xml

    # Multiple feeds:
    python3 fetch_wechat_rss.py URL1 URL2 URL3

    # From a file (one URL per line, # for comments):
    python3 fetch_wechat_rss.py --feeds-file wechat_feeds.txt

    # Show only new articles since last run (default: show last 10 per feed):
    python3 fetch_wechat_rss.py --only-new URL...

    # Output as JSON for piping into another script:
    python3 fetch_wechat_rss.py --json URL...

    # Include full HTML body of each article:
    python3 fetch_wechat_rss.py --full URL...

State file (which entry IDs have been seen per feed) lives at
~/.wechat_rss_seen.json so --only-new works across runs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Iterable

import feedparser
import requests

STATE_FILE = Path.home() / ".wechat_rss_seen.json"
DEFAULT_LIMIT = 10
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 fetch_wechat_rss/1.0"


def load_state() -> dict[str, list[str]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state: dict[str, list[str]]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def fetch_feed(url: str) -> feedparser.FeedParserDict:
    # Wechat2RSS sometimes rejects feedparser's default UA — fetch ourselves.
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    resp.raise_for_status()
    return feedparser.parse(resp.content)


def entry_id(entry) -> str:
    return entry.get("id") or entry.get("link") or entry.get("title", "")


def entry_to_dict(entry, *, include_body: bool) -> dict:
    out = {
        "id": entry_id(entry),
        "title": unescape(entry.get("title", "").strip()),
        "link": entry.get("link", ""),
        "author": entry.get("author", ""),
        "published": entry.get("published", entry.get("updated", "")),
        "summary": unescape(entry.get("summary", "").strip()),
    }
    if include_body:
        body = ""
        content = entry.get("content")
        if content and isinstance(content, list):
            body = content[0].get("value", "")
        out["content_html"] = body
    return out


def print_human(feed_url: str, feed_title: str, entries: Iterable[dict]) -> None:
    print(f"\n=== {feed_title}  ({feed_url}) ===")
    for e in entries:
        print(f"\n  • {e['title']}")
        if e["author"]:
            print(f"    by {e['author']}")
        if e["published"]:
            print(f"    {e['published']}")
        print(f"    {e['link']}")
        if e["summary"]:
            summary = e["summary"].replace("\n", " ").strip()
            if len(summary) > 240:
                summary = summary[:240] + "…"
            print(f"    {summary}")


def read_feed_file(path: Path) -> list[str]:
    urls = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*", help="Wechat2RSS feed URL(s)")
    ap.add_argument("--feeds-file", type=Path, help="File with one feed URL per line")
    ap.add_argument("--only-new", action="store_true", help="Only show entries not seen on previous runs")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max entries per feed (default {DEFAULT_LIMIT}, 0 = unlimited)")
    ap.add_argument("--full", action="store_true", help="Include full article HTML body (only meaningful with --json)")
    ap.add_argument("--json", dest="as_json", action="store_true", help="Emit JSON instead of human-readable output")
    args = ap.parse_args()

    feeds: list[str] = list(args.urls)
    if args.feeds_file:
        feeds.extend(read_feed_file(args.feeds_file))
    if not feeds:
        ap.error("provide at least one feed URL or --feeds-file")

    state = load_state() if args.only_new else {}
    all_output: list[dict] = []

    for url in feeds:
        try:
            parsed = fetch_feed(url)
        except (requests.RequestException, ValueError) as exc:
            print(f"[warn] {url}: {exc}", file=sys.stderr)
            continue

        feed_title = parsed.feed.get("title", url)
        seen = set(state.get(url, []))
        fresh = []
        for entry in parsed.entries:
            eid = entry_id(entry)
            if args.only_new and eid in seen:
                continue
            if not args.limit or len(fresh) < args.limit:
                fresh.append(entry_to_dict(entry, include_body=args.full))
            seen.add(eid)  # mark seen even if limit hit, so next run doesn't re-surface it

        if args.only_new:
            # Keep the most recent ~500 ids per feed to bound the state file.
            state[url] = list(seen)[-500:]

        if args.as_json:
            all_output.append({"feed": url, "title": feed_title, "entries": fresh, "fetched_at": datetime.now().isoformat(timespec="seconds")})
        else:
            print_human(url, feed_title, fresh)

    if args.only_new:
        save_state(state)

    if args.as_json:
        print(json.dumps(all_output, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
