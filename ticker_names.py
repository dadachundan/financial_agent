"""
ticker_names.py — Ticker code → Chinese company name lookup via AKShare.

The A-share + HK name list is fetched once from EastMoney (via AKShare) and
cached in ticker_name_cache.json beside this file. The cache is refreshed
automatically after CACHE_MAX_AGE_DAYS days.

Because the initial fetch takes ~2 minutes, call init() at app startup to kick
off a background thread. Subsequent startups load instantly from the JSON cache.

Public API
----------
  init(force_refresh=False)        — call at startup; loads cache or spawns build thread
  is_ready() → bool                — True once the map is loaded into memory
  is_building() → bool             — True while the background fetch is running
  get_map() → dict | None          — return the in-memory {code: name} dict
  enrich_ticker_string(s, map)     — enrich a comma-separated ticker string
"""

import json
import pathlib
import datetime
import re
import threading
from typing import Optional

SCRIPT_DIR         = pathlib.Path(__file__).parent
CACHE_FILE         = SCRIPT_DIR / "ticker_name_cache.json"
CACHE_MAX_AGE_DAYS = 7  # refresh weekly

# ── module-level state ────────────────────────────────────────────────────────
_cache: Optional[dict] = None
_cache_lock            = threading.Lock()
_cache_building        = False


# ── internal: fetch from AKShare ──────────────────────────────────────────────

def _build_cache() -> None:
    """Background thread: fetch A-share + HK names and write cache file."""
    global _cache, _cache_building
    try:
        import akshare as ak
        result: dict[str, str] = {}

        # ── A-shares (EastMoney source, ~5 800 stocks, ~60 s) ────────────────
        print("[ticker_names] fetching A-share names…")
        df_a = ak.stock_zh_a_spot_em()
        for _, row in df_a[["代码", "名称"]].iterrows():
            result[str(row["代码"])] = str(row["名称"])
        print(f"[ticker_names] A-shares: {len(result)} entries")

        # ── HK stocks (EastMoney source, ~2 600 stocks, ~35 s) ───────────────
        print("[ticker_names] fetching HK stock names…")
        df_hk = ak.stock_hk_spot_em()
        hk_count = 0
        for _, row in df_hk[["代码", "名称"]].iterrows():
            code = str(row["代码"])   # e.g. "00700"
            name = str(row["名称"])
            result[code] = name
            stripped = code.lstrip("0") or "0"
            if stripped != code:
                result[stripped] = name   # "700" → same name
            hk_count += 1
        print(f"[ticker_names] HK stocks: {hk_count} entries")

        # ── persist ───────────────────────────────────────────────────────────
        CACHE_FILE.write_text(
            json.dumps(result, ensure_ascii=False), encoding="utf-8"
        )
        with _cache_lock:
            _cache = result
        print(f"[ticker_names] cache ready: {len(result)} total entries")

    except Exception as exc:
        print(f"[ticker_names] cache build failed (network issue, will retry next start): {exc}")
    finally:
        _cache_building = False


# ── Public: init ──────────────────────────────────────────────────────────────

def init(force_refresh: bool = False) -> None:
    """
    Call once at app startup.
    - If a fresh cache file exists, load it synchronously (instant).
    - Otherwise start a background thread to build the cache.
    """
    global _cache, _cache_building

    if not force_refresh and CACHE_FILE.exists():
        age = (
            datetime.datetime.now()
            - datetime.datetime.fromtimestamp(CACHE_FILE.stat().st_mtime)
        )
        if age.days < CACHE_MAX_AGE_DAYS:
            with _cache_lock:
                _cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            print(f"[ticker_names] loaded {len(_cache)} entries from cache file")
            return

    # Cache missing or stale — build in background
    print("[ticker_names] cache missing/stale; starting background build (~2 min)…")
    _cache_building = True
    threading.Thread(target=_build_cache, daemon=True).start()


def is_ready() -> bool:
    """True once the ticker map is loaded into memory."""
    return _cache is not None


def is_building() -> bool:
    """True while the background fetch thread is running."""
    return _cache_building


def get_map() -> Optional[dict]:
    """Return the in-memory {code: name} dict, or None if not ready yet."""
    return _cache


# ── Public: enrichment helpers ────────────────────────────────────────────────

_HAS_CHINESE = re.compile(r"[\u4e00-\u9fff]")
_SUFFIX_RE   = re.compile(r"\.(SZ|SS|SH|HK|KS|KP|TW|US)$", re.IGNORECASE)


def _normalize(code: str) -> str:
    """Strip exchange suffix: '688981.SH' → '688981', '00700.HK' → '00700'."""
    return _SUFFIX_RE.sub("", code.strip())


def get_name(code: str, ticker_map: Optional[dict] = None) -> Optional[str]:
    """Return Chinese name for a single code, or None if not found."""
    if ticker_map is None:
        ticker_map = get_map()
    if not ticker_map:
        return None
    c = _normalize(code)
    return ticker_map.get(c) or ticker_map.get(c.lstrip("0") or c)


def enrich_ticker_string(tickers_str: str, ticker_map: dict) -> tuple[str, int]:
    """
    Given a comma-separated ticker string like 'NVDA, 688981, 中芯国际 688981.SH',
    look up bare numeric codes and prepend the Chinese name.

    Returns:
        (enriched_str, n_enriched)  — n_enriched = how many tokens were updated
    """
    parts  = [p.strip() for p in tickers_str.split(",") if p.strip()]
    result = []
    n_enriched = 0

    for part in parts:
        # Already has a Chinese name — leave untouched
        if _HAS_CHINESE.search(part):
            result.append(part)
            continue

        # The raw code is the last whitespace-delimited token
        tokens   = part.split()
        raw_code = tokens[-1] if tokens else part
        clean    = _normalize(raw_code)

        name = ticker_map.get(clean) or ticker_map.get(clean.lstrip("0") or clean)
        if name:
            result.append(f"{name} {raw_code}")
            n_enriched += 1
        else:
            result.append(part)

    return ",".join(result), n_enriched
