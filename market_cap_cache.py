"""market_cap_cache.py — daily-cached market caps via yfinance.

Stores one row per (yfinance_ticker, fetch_date) in
`db/market_cap_cache.db`. Once a ticker has been fetched today the
result (including None / failures) is served from the cache, so a
page reload never re-hits the network.

Public API:
    get_market_caps(tickers: list[str]) -> dict[str, int | None]
        Keys are EXCHANGE:CODE form. Values are USD-equivalent market
        caps as reported by yfinance (`info["marketCap"]`) — local
        currency for non-US listings, no FX adjustment. None when the
        upstream call fails or the field is missing.
"""
from __future__ import annotations

import logging
import sqlite3
import threading
import time
from datetime import date
from pathlib import Path

from sector_map import to_yfinance
from db_paths import db_path

log = logging.getLogger(__name__)

_DB_PATH = db_path("market_cap_cache.db")
_DB_LOCK = threading.Lock()


def _conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(_DB_PATH, timeout=30)
    c.execute(
        """CREATE TABLE IF NOT EXISTS market_cap_cache (
              ticker        TEXT NOT NULL,
              fetch_date    TEXT NOT NULL,
              market_cap    INTEGER,
              currency      TEXT,
              fetched_at    REAL NOT NULL,
              PRIMARY KEY (ticker, fetch_date)
           )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS fx_rates (
              currency      TEXT NOT NULL,   -- ISO code (e.g. 'KRW')
              fetch_date    TEXT NOT NULL,
              units_per_usd REAL,            -- 1 USD = N units of `currency`
              fetched_at    REAL NOT NULL,
              PRIMARY KEY (currency, fetch_date)
           )"""
    )
    return c


def _read_cached(yf_tickers: list[str], today: str) -> dict[str, int | None]:
    if not yf_tickers:
        return {}
    placeholders = ",".join("?" for _ in yf_tickers)
    with _DB_LOCK, _conn() as c:
        cur = c.execute(
            f"SELECT ticker, market_cap FROM market_cap_cache "
            f"WHERE fetch_date = ? AND ticker IN ({placeholders})",
            (today, *yf_tickers),
        )
        return {row[0]: row[1] for row in cur.fetchall()}


def _write_cached(rows: list[tuple[str, str, int | None, str | None, float]]) -> None:
    if not rows:
        return
    with _DB_LOCK, _conn() as c:
        c.executemany(
            "INSERT OR REPLACE INTO market_cap_cache "
            "(ticker, fetch_date, market_cap, currency, fetched_at) "
            "VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        c.commit()


def _fetch_one(yf_ticker: str) -> tuple[int | None, str | None]:
    """Return (market_cap, currency) from yfinance, or (None, None) on error."""
    try:
        import yfinance as yf  # local import — heavy
        info = yf.Ticker(yf_ticker).info or {}
        mc = info.get("marketCap")
        cur = info.get("currency") or info.get("financialCurrency")
        if mc is None:
            return (None, cur)
        return (int(mc), cur)
    except Exception as e:
        log.warning("market cap fetch failed for %s: %s", yf_ticker, e)
        return (None, None)


_BG_LOCK = threading.Lock()
_BG_INFLIGHT: set[str] = set()  # yfinance tickers currently being fetched


def _background_fetch(yf_tickers: list[str], today: str) -> None:
    """Fetch a batch of tickers in parallel and persist results."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    try:
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(_fetch_one, yt): yt for yt in yf_tickers}
            for fut in as_completed(futures):
                yt = futures[fut]
                try:
                    mc, cur = fut.result()
                except Exception as e:
                    log.warning("background fetch failed for %s: %s", yt, e)
                    mc, cur = None, None
                _write_cached([(yt, today, mc, cur, time.time())])
                with _BG_LOCK:
                    _BG_INFLIGHT.discard(yt)
    finally:
        with _BG_LOCK:
            for yt in yf_tickers:
                _BG_INFLIGHT.discard(yt)


def _read_cached_full(yf_tickers: list[str], today: str) -> dict[str, tuple[int | None, str | None]]:
    if not yf_tickers:
        return {}
    placeholders = ",".join("?" for _ in yf_tickers)
    with _DB_LOCK, _conn() as c:
        cur = c.execute(
            f"SELECT ticker, market_cap, currency FROM market_cap_cache "
            f"WHERE fetch_date = ? AND ticker IN ({placeholders})",
            (today, *yf_tickers),
        )
        return {row[0]: (row[1], row[2]) for row in cur.fetchall()}


def _read_prior_day_fallback(
    yf_tickers: list[str], today: str,
) -> dict[str, tuple[int | None, str | None]]:
    """For each ticker missing today, return the most-recent prior-day row.

    Lets the UI keep showing yesterday's number while today's background
    refresh is still in flight, instead of rendering a blank cell.
    """
    if not yf_tickers:
        return {}
    placeholders = ",".join("?" for _ in yf_tickers)
    with _DB_LOCK, _conn() as c:
        cur = c.execute(
            f"""
            SELECT ticker, market_cap, currency
            FROM market_cap_cache
            WHERE fetch_date < ? AND ticker IN ({placeholders})
              AND fetch_date = (
                SELECT MAX(fetch_date) FROM market_cap_cache c2
                WHERE c2.ticker = market_cap_cache.ticker AND c2.fetch_date < ?
              )
            """,
            (today, *yf_tickers, today),
        )
        return {row[0]: (row[1], row[2]) for row in cur.fetchall()}


def get_market_caps(
    tickers: list[str], *, block: bool = True,
) -> dict[str, tuple[int | None, str | None]]:
    """Look up market caps for EXCHANGE:CODE tickers, with per-day cache.

    Returns {EXCHANGE:CODE: (market_cap_or_None, currency_or_None)}.

    When `block=True` (default) any missing tickers are fetched
    synchronously. When `block=False` missing ones return (None, None)
    and a background thread populates the cache for the next call.
    """
    today = date.today().isoformat()

    yf_by_orig: dict[str, str] = {}
    for t in tickers:
        yt = to_yfinance(t)
        if yt:
            yf_by_orig[t] = yt

    yf_tickers = sorted(set(yf_by_orig.values()))
    cached = _read_cached_full(yf_tickers, today)
    missing = [yt for yt in yf_tickers if yt not in cached]

    fetched: dict[str, tuple[int | None, str | None]] = {}
    if missing:
        if block:
            new_rows: list[tuple[str, str, int | None, str | None, float]] = []
            now = time.time()
            for yt in missing:
                mc, cur = _fetch_one(yt)
                fetched[yt] = (mc, cur)
                new_rows.append((yt, today, mc, cur, now))
            _write_cached(new_rows)
        else:
            with _BG_LOCK:
                to_kick = [yt for yt in missing if yt not in _BG_INFLIGHT]
                _BG_INFLIGHT.update(to_kick)
            if to_kick:
                t = threading.Thread(
                    target=_background_fetch, args=(to_kick, today), daemon=True,
                )
                t.start()

    # For tickers still missing today's number after the dispatch above
    # (block=False path while background fetch is in flight), fall back to
    # the most recent prior-day cached value so the UI shows yesterday's
    # data instead of a blank cell.
    still_missing = [
        yt for yt in yf_tickers if yt not in cached and yt not in fetched
    ]
    prior = _read_prior_day_fallback(still_missing, today) if still_missing else {}

    out: dict[str, tuple[int | None, str | None]] = {}
    for orig, yt in yf_by_orig.items():
        if yt in cached:
            out[orig] = cached[yt]
        elif yt in fetched:
            out[orig] = fetched[yt]
        elif yt in prior:
            out[orig] = prior[yt]
        else:
            out[orig] = (None, None)
    for t in tickers:
        out.setdefault(t, (None, None))
    return out


def pending_count() -> int:
    """Number of tickers currently being fetched in the background."""
    with _BG_LOCK:
        return len(_BG_INFLIGHT)


# ── FX rates ─────────────────────────────────────────────────────────────────

# yfinance forex pairs return `1 USD = N <ccy>`, except for a handful of
# inverted majors (EUR, GBP, AUD, NZD) where `<CCY>=X` is actually
# `<ccy> per USD` too in yfinance's parlance. yfinance accepts both
# `<CCY>=X` (e.g. KRW=X) and the explicit `USD<CCY>=X` (e.g. USDKRW=X);
# we use the explicit form to avoid ambiguity on the majors.
_USD = "USD"


def _read_cached_fx(currencies: list[str], today: str) -> dict[str, float | None]:
    if not currencies:
        return {}
    placeholders = ",".join("?" for _ in currencies)
    with _DB_LOCK, _conn() as c:
        cur = c.execute(
            f"SELECT currency, units_per_usd FROM fx_rates "
            f"WHERE fetch_date = ? AND currency IN ({placeholders})",
            (today, *currencies),
        )
        return {row[0]: row[1] for row in cur.fetchall()}


def _write_cached_fx(rows: list[tuple[str, str, float | None, float]]) -> None:
    if not rows:
        return
    with _DB_LOCK, _conn() as c:
        c.executemany(
            "INSERT OR REPLACE INTO fx_rates "
            "(currency, fetch_date, units_per_usd, fetched_at) "
            "VALUES (?, ?, ?, ?)",
            rows,
        )
        c.commit()


def _fetch_fx(currency: str) -> float | None:
    """Return units of `currency` per 1 USD (e.g. KRW → ~1380), or None."""
    if not currency or currency.upper() == _USD:
        return 1.0
    try:
        import yfinance as yf
        pair = f"USD{currency.upper()}=X"
        hist = yf.Ticker(pair).history(period="5d", interval="1d")
        if hist is None or hist.empty:
            return None
        return float(hist["Close"].dropna().iloc[-1])
    except Exception as e:
        log.warning("FX fetch failed for %s: %s", currency, e)
        return None


def get_fx_rates(currencies: list[str]) -> dict[str, float | None]:
    """Return {currency: units_per_usd} for each ISO code, with per-day cache.

    USD maps to 1.0. Unknown / failed currencies map to None.
    """
    today = date.today().isoformat()
    wanted = sorted({c.upper() for c in currencies if c})
    if not wanted:
        return {}
    cached = _read_cached_fx(wanted, today)
    out: dict[str, float | None] = {}
    new_rows: list[tuple[str, str, float | None, float]] = []
    now = time.time()
    for ccy in wanted:
        if ccy == _USD:
            out[ccy] = 1.0
            continue
        if ccy in cached:
            out[ccy] = cached[ccy]
            continue
        rate = _fetch_fx(ccy)
        out[ccy] = rate
        new_rows.append((ccy, today, rate, now))
    _write_cached_fx(new_rows)
    return out


def to_usd(value: int | None, currency: str | None,
           rates: dict[str, float | None] | None = None) -> float | None:
    """Convert a native-currency market cap to USD using cached FX rates.

    Returns None if the value or rate is unknown / unusable.
    """
    if value is None or value <= 0:
        return None
    ccy = (currency or _USD).upper()
    if ccy == _USD:
        return float(value)
    rate = (rates or {}).get(ccy)
    if rate is None:
        rate = get_fx_rates([ccy]).get(ccy)
    if not rate or rate <= 0:
        return None
    return float(value) / rate


def format_market_cap(value: int | None, currency: str | None = None) -> str:
    """Render a market cap as a short human string ("12.3B", "456M USD", "—")."""
    if value is None or value <= 0:
        return "—"
    v = float(value)
    if v >= 1e12:
        s = f"{v/1e12:.2f}T"
    elif v >= 1e9:
        s = f"{v/1e9:.2f}B"
    elif v >= 1e6:
        s = f"{v/1e6:.1f}M"
    else:
        s = f"{v:.0f}"
    # Surface non-USD currencies so KRW/JPY/HKD/CNY don't get misread.
    cur = (currency or "").upper()
    if cur and cur != "USD":
        s = f"{s} {cur}"
    return s
