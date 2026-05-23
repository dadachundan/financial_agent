#!/usr/bin/env python3
"""Ticker-specific news, combining four sources for depth and recall.

Sources (deduped by URL/title, all run in parallel logic):
  1. yfinance.Ticker.get_news       — primary, recency-biased
  2. yfinance.Search (ticker + name) — paginates further back than get_news
  3. Google News RSS (via feedparser) — broad recall, deep history
  4. SEC EDGAR 8-K listing          — official filings for the window

Any source that errors is skipped with a warning to stderr; the
remaining sources still produce output.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta

import feedparser
import requests
import yfinance as yf

DEFAULT_LIMIT = 300
# When the deduped pool exceeds --limit we stratify so the 8-30 day
# (medium-term) bucket keeps a meaningful share — Yahoo's feed is
# heavily recency-biased and would otherwise wipe out older rows.
MEDIUM_TERM_BOUNDARY_DAYS = 8
SEC_HEADERS = {
    "User-Agent": "financial-agent news-analyst lx00617@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}
SEC_DELAY = 0.12  # polite to SEC

# 8-K item codes → human-readable labels (lifted from fetch_financial_report.py).
_8K_ITEMS = {
    "1.01": "Material Definitive Agreement", "1.02": "Termination of Agreement",
    "1.03": "Bankruptcy", "1.05": "Material Cybersecurity Incident",
    "2.01": "Asset Acquisition/Disposal", "2.02": "Earnings Results",
    "2.03": "Debt Obligation", "2.04": "Debt Trigger", "2.05": "Costs",
    "2.06": "Asset Impairment",
    "3.01": "Listing Standards", "3.02": "Unregistered Equity Sales",
    "3.03": "Shareholder Rights",
    "4.01": "Auditor Change", "4.02": "Restatement",
    "5.02": "Director/Officer Change", "5.03": "Charter Amendment",
    "5.07": "Shareholder Vote", "5.08": "Director Vacancy",
    "7.01": "Regulation FD", "8.01": "Other Events",
    "9.01": "Financial Statements/Exhibits",
}


# ── source 1 + 2: yfinance ────────────────────────────────────────────────

def _extract_yf(article: dict) -> dict | None:
    c = article.get("content", article)
    title = (c.get("title") or article.get("title") or "").strip()
    if not title:
        return None
    publisher = (
        (c.get("provider") or {}).get("displayName")
        or article.get("publisher", "Unknown")
    )
    url = (
        ((c.get("canonicalUrl") or c.get("clickThroughUrl") or {}) or {}).get("url")
        or article.get("link", "")
    )
    summary = (c.get("summary") or "").strip()
    pub_date = None
    pub_str = c.get("pubDate") or ""
    if pub_str:
        try:
            pub_date = datetime.fromisoformat(pub_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            pass
    return {
        "title": title, "publisher": publisher, "link": url,
        "summary": summary, "pub_date": pub_date,
    }


def fetch_yfinance_news(ticker: str, count: int) -> list[dict]:
    try:
        raw = yf.Ticker(ticker).get_news(count=count) or []
    except Exception as exc:
        sys.stderr.write(f"[yf.Ticker.get_news] {ticker}: {exc}\n")
        return []
    out = []
    for a in raw:
        d = _extract_yf(a)
        if d:
            d["source"] = "yfinance.get_news"
            out.append(d)
    return out


def fetch_yfinance_search(query: str, count: int) -> list[dict]:
    if not query:
        return []
    try:
        s = yf.Search(query=query, news_count=count, enable_fuzzy_query=False)
        raw = s.news or []
    except Exception as exc:
        sys.stderr.write(f"[yf.Search] {query!r}: {exc}\n")
        return []
    out = []
    for a in raw:
        d = _extract_yf(a)
        if d:
            d["source"] = "yfinance.Search"
            out.append(d)
    return out


# ── source 3: Google News RSS ─────────────────────────────────────────────

def fetch_google_news_rss(query: str, look_back_days: int) -> list[dict]:
    """Pull Google News RSS via feedparser.

    Google News supports a ``when:Nd`` clause inside the query — we use the
    longest window we need (caller's start→end span) and let the post-fetch
    date filter trim. ``after:`` / ``before:`` operators are unreliable on
    the RSS endpoint, so we don't use them.
    """
    if not query:
        return []
    when_days = max(1, min(look_back_days, 365))
    q = f"{query} when:{when_days}d"
    url = (
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode({"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    )
    try:
        feed = feedparser.parse(url)
    except Exception as exc:
        sys.stderr.write(f"[google-news-rss] {query!r}: {exc}\n")
        return []
    out = []
    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        if not title:
            continue
        # Google News titles are formatted "Title - Publisher".
        publisher = "Google News"
        if " - " in title:
            head, tail = title.rsplit(" - ", 1)
            if 2 <= len(tail) <= 60:
                title, publisher = head.strip(), tail.strip()
        link = entry.get("link", "")
        pub_date = None
        if entry.get("published_parsed"):
            try:
                pub_date = datetime(*entry.published_parsed[:6])
            except Exception:
                pass
        summary = re.sub(r"<[^>]+>", "", entry.get("summary", "")).strip()
        out.append({
            "title": title, "publisher": publisher, "link": link,
            "summary": summary, "pub_date": pub_date,
            "source": "google-news-rss",
        })
    return out


# ── source 4: SEC EDGAR 8-K ───────────────────────────────────────────────

_TICKER_MAP_CACHE: dict | None = None


def _resolve_cik(ticker: str) -> tuple[str, str] | None:
    """Return (cik_padded_10, company_name) or None if not in EDGAR map."""
    global _TICKER_MAP_CACHE
    if _TICKER_MAP_CACHE is None:
        try:
            time.sleep(SEC_DELAY)
            r = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=SEC_HEADERS, timeout=30,
            )
            r.raise_for_status()
            _TICKER_MAP_CACHE = r.json()
        except Exception as exc:
            sys.stderr.write(f"[edgar ticker-map] {exc}\n")
            return None
    tic = ticker.strip().upper()
    for item in (_TICKER_MAP_CACHE or {}).values():
        if str(item.get("ticker", "")).upper() == tic:
            return str(item["cik_str"]).zfill(10), item.get("title", ticker)
    return None


def fetch_edgar_8k(ticker: str, start_date: str, end_date: str) -> tuple[list[dict], str | None]:
    resolved = _resolve_cik(ticker)
    if not resolved:
        return [], None
    cik, name = resolved
    try:
        time.sleep(SEC_DELAY)
        r = requests.get(
            f"https://data.sec.gov/submissions/CIK{cik}.json",
            headers=SEC_HEADERS, timeout=30,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as exc:
        sys.stderr.write(f"[edgar 8-K] {ticker}: {exc}\n")
        return [], name
    rec = data.get("filings", {}).get("recent", {})
    forms = rec.get("form", [])
    dates = rec.get("filingDate", [])
    accns = rec.get("accessionNumber", [])
    items_list = rec.get("items", [])
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    out: list[dict] = []
    for i, form in enumerate(forms):
        if form != "8-K":
            continue
        try:
            d = datetime.strptime(dates[i], "%Y-%m-%d")
        except (ValueError, IndexError):
            continue
        if not (start <= d <= end):
            continue
        items_raw = (items_list[i] if i < len(items_list) else "") or ""
        codes = [x.strip() for x in items_raw.split(",") if x.strip()]
        labels = [_8K_ITEMS.get(c, c) for c in codes]
        # Skip 9.01 (just means "has exhibits") unless it's the only one.
        meaningful = [
            lbl for lbl, code in zip(labels, codes) if code != "9.01"
        ] or labels
        topic = " / ".join(dict.fromkeys(meaningful)) or "8-K filing"
        accn = accns[i]
        clean = accn.replace("-", "")
        link = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{clean}/{accn}-index.htm"
        out.append({
            "title": f"{name} 8-K — {topic}",
            "publisher": "SEC EDGAR",
            "link": link,
            "summary": f"8-K filing. Items: {items_raw or 'n/a'}.",
            "pub_date": d,
            "source": "edgar-8k",
        })
    return out, name


# ── dedupe + window filter ────────────────────────────────────────────────

def _normalize_url(url: str) -> str:
    if not url:
        return ""
    try:
        u = urllib.parse.urlsplit(url)
        # Drop query string + fragment — strips yahoo/google tracking and
        # `?yptr=yahoo` / `?ncid=...` style params that defeat dedupe.
        return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, "", ""))
    except Exception:
        return url


def _title_key(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()[:80]


def dedupe(articles: list[dict]) -> list[dict]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    out: list[dict] = []
    for a in articles:
        ukey = _normalize_url(a.get("link", ""))
        tkey = _title_key(a.get("title", ""))
        if ukey and ukey in seen_urls:
            continue
        if tkey and tkey in seen_titles:
            continue
        if ukey:
            seen_urls.add(ukey)
        if tkey:
            seen_titles.add(tkey)
        out.append(a)
    return out


def in_window(art: dict, start: datetime, end: datetime) -> bool:
    pd = art.get("pub_date")
    if not pd:
        # Keep undated rows — downstream emits "date unknown" so the
        # writer can spot them. Better than discarding useful primary
        # sources just because the feed omitted pubDate.
        return True
    return start <= pd <= end


# ── main ──────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description="Fetch ticker-specific news (multi-source).")
    p.add_argument("ticker")
    p.add_argument("start_date")
    p.add_argument("end_date")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                   help="Soft cap on total articles after dedup (default %(default)s).")
    p.add_argument("--no-google", action="store_true", help="Skip Google News RSS.")
    p.add_argument("--no-edgar", action="store_true", help="Skip SEC EDGAR 8-K.")
    p.add_argument("--no-search", action="store_true", help="Skip yfinance.Search.")
    a = p.parse_args()

    start = datetime.strptime(a.start_date, "%Y-%m-%d")
    end = datetime.strptime(a.end_date, "%Y-%m-%d") + timedelta(days=1)
    look_back = max(1, (end - start).days)

    counts: dict[str, int] = {}
    bundles: list[dict] = []

    # 1. yfinance Ticker — primary
    s1 = fetch_yfinance_news(a.ticker, max(a.limit, 100))
    counts["yfinance.get_news"] = len(s1)
    bundles.extend(s1)

    # 4. EDGAR 8-K — first because it returns the canonical company name
    edgar_articles: list[dict] = []
    company_name: str | None = None
    if not a.no_edgar:
        edgar_articles, company_name = fetch_edgar_8k(a.ticker, a.start_date, a.end_date)
        counts["edgar-8k"] = len(edgar_articles)
        bundles.extend(edgar_articles)

    # 2. yfinance Search — ticker + company name
    if not a.no_search:
        s2a = fetch_yfinance_search(a.ticker, 100)
        s2b = fetch_yfinance_search(company_name, 100) if company_name else []
        counts["yfinance.Search"] = len(s2a) + len(s2b)
        bundles.extend(s2a + s2b)

    # 3. Google News RSS — ticker OR company
    if not a.no_google:
        gq = a.ticker
        if company_name and company_name.lower() != a.ticker.lower():
            gq = f'"{a.ticker}" OR "{company_name}"'
        s3 = fetch_google_news_rss(gq, look_back)
        counts["google-news-rss"] = len(s3)
        bundles.extend(s3)

    filtered = [x for x in bundles if in_window(x, start, end)]
    deduped = dedupe(filtered)
    deduped.sort(key=lambda d: d.get("pub_date") or datetime.min, reverse=True)
    total_deduped = len(deduped)

    # Stratify if we'd otherwise clip the medium-term tail.
    if total_deduped > a.limit:
        boundary = end - timedelta(days=MEDIUM_TERM_BOUNDARY_DAYS)
        medium = [d for d in deduped if d.get("pub_date") and d["pub_date"] < boundary]
        rest = [d for d in deduped if d not in medium]
        medium_floor = min(len(medium), a.limit // 3)
        keep_medium = medium[:medium_floor]
        keep_rest = rest[: a.limit - len(keep_medium)]
        deduped = keep_rest + keep_medium
        deduped.sort(key=lambda d: d.get("pub_date") or datetime.min, reverse=True)

    medium_in_output = sum(
        1 for d in deduped
        if d.get("pub_date") and d["pub_date"] < end - timedelta(days=MEDIUM_TERM_BOUNDARY_DAYS)
    )
    sys.stderr.write(f"[get_news] sources: {counts}\n")
    sys.stderr.write(
        f"[get_news] deduped in window: {total_deduped}; kept: {len(deduped)} "
        f"(medium-term 8-{(end-start).days}d: {medium_in_output})\n"
    )

    if not deduped:
        print(f"No news found for {a.ticker} between {a.start_date} and {a.end_date}")
        return 0

    blocks = []
    for d in deduped:
        date_str = d["pub_date"].strftime("%Y-%m-%d") if d.get("pub_date") else "date unknown"
        block = f"### {d['title']} (source: {d['publisher']}, {date_str})\n"
        if d.get("summary"):
            block += f"{d['summary']}\n"
        if d.get("link"):
            block += f"Link: {d['link']}\n"
        blocks.append(block + "\n")

    print(f"## {a.ticker} News, from {a.start_date} to {a.end_date}:\n")
    print("".join(blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
