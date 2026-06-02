"""sector_map.py — hardcoded EXCHANGE:CODE → sector mapping.

Sourced from two watchlist files:
  - ~/Downloads/🇨🇳chinese.txt        (China / HK / regional buckets)
  - ~/Downloads/🤪PER SECTOR.txt       (global / US buckets)

Use `sector_for(ticker)` to look up the bucket for a single ticker
(EXCHANGE:CODE form, e.g. "HKEX:2513" or "NASDAQ:NVDA"). Unknown
tickers return "" so callers can render a blank cell.

The companion `to_yfinance(ticker)` converts EXCHANGE:CODE form to
the yfinance suffix form (e.g. "688802.SS", "GMIN.TO", "BRK-B").
"""
from __future__ import annotations

# Ordered list of (sector_label, [EXCHANGE:CODE, ...]).
# Preserve the exact bucket names from the source files so the
# dropdown reads back to the user's mental categories.
SECTORS: list[tuple[str, list[str]]] = [
    # ── Global / US ──────────────────────────────────────────────────────────
    ("BIG TECH", [
        "NASDAQ:NFLX", "NASDAQ:GOOG", "NYSE:BRK.B", "NASDAQ:META",
        "NASDAQ:MSFT", "NASDAQ:AAPL", "NASDAQ:AMZN", "NASDAQ:AVGO",
        "NASDAQ:NVDA", "NYSE:ORCL", "NYSE:TSM",  "NASDAQ:TSLA",
        "NASDAQ:MU",   "NASDAQ:ASML", "NASDAQ:AMD",
    ]),
    ("SEMICONDUCTORS", [
        "NASDAQ:ADI",  "NASDAQ:LITE", "NYSE:VRT",   "NASDAQ:TXN",
        "NYSE:COHR",   "TSE:6857",    "NYSE:CAT",   "NASDAQ:MCHP",
        "NASDAQ:QCOM", "NASDAQ:AMAT", "NASDAQ:KLAC","NASDAQ:GSIT",
        "NASDAQ:NXPI", "NYSE:DELL",   "XETR:IFX",   "NASDAQ:MRVL",
        "NASDAQ:APLD", "NASDAQ:LRCX", "NYSE:STM",   "NASDAQ:TER",
        "NASDAQ:INTC", "NASDAQ:CRDO", "NASDAQ:ARM", "NASDAQ:ALAB",
        "NASDAQ:NVTS",
    ]),
    ("芯片设计公司",      ["NASDAQ:SNPS", "NASDAQ:CDNS"]),
    ("STORAGE", [
        "KRX:000660", "KRX:005930", "NASDAQ:WDC", "NASDAQ:SNDK", "NASDAQ:STX",
    ]),
    ("ENERGY", [
        "NYSE:XOM",  "NYSE:OXY",   "NYSE:SHEL", "NYSE:PWR",  "NYSE:GEV",
        "NYSE:SMR",  "AMEX:UUUU",  "NASDAQ:FSLR", "NASDAQ:TLN", "NYSE:BE",
        "NYSE:OKLO",
    ]),
    ("MINING", [
        "TSX:GMIN", "NYSE:NEM", "NYSE:B", "NASDAQ:CIFR", "NASDAQ:USAR",
    ]),
    ("AI云服务",          [
        "NASDAQ:MDB", "NASDAQ:NBIS", "NASDAQ:DDOG", "NASDAQ:GTLB", "NYSE:DOCN",
    ]),
    ("网络安全",          ["NASDAQ:PANW"]),
    ("机器人 (US)",        ["NASDAQ:SERV", "NASDAQ:SYM"]),
    ("教育",              ["NASDAQ:DUOL", "NYSE:LRN"]),
    ("AI", [
        "NYSE:SNOW", "NASDAQ:SOUN", "NASDAQ:TEM", "NYSE:ZETA",
        "NASDAQ:PLTR", "NYSE:BBAI",
    ]),
    ("AEROSPACE/SATELLITE", [
        "NYSE:AMPX", "NYSE:ACHR", "NYSE:RTX",  "NYSE:BKSY", "NYSE:HEI",
        "NYSE:PL",   "NYSE:JOBY", "NYSE:HWM",  "NASDAQ:ASTS", "NASDAQ:VSAT",
        "NASDAQ:ATRO", "NYSE:RDW",
    ]),
    ("OTHER (US)", [
        "NYSE:RDDT", "ASX:RMS", "NASDAQ:WYFI", "NYSE:VST",
        "NASDAQ:INOD", "NASDAQ:AMBA", "NASDAQ:RMBS",
    ]),

    # ── China / HK / regional ────────────────────────────────────────────────
    ("HK EXCHANGE", [
        "HKEX:9660", "HKEX:9880", "HKEX:2513", "HKEX:2590", "HKEX:2533",
        "HKEX:6600", "HKEX:981",  "HKEX:100",
    ]),
    ("GPU (CN)", [
        "HKEX:6082", "SSE:688802", "SSE:688041", "SSE:688795", "SSE:688256",
        "SZSE:002837", "SZSE:300308",
    ]),
    ("AI RELATED (CN)", [
        "SSE:603486", "SZSE:301018", "SSE:603019", "SSE:688169",
        "SZSE:300383", "SZSE:002472",
    ]),
    ("机器人相关 (CN)", [
        "SSE:601100", "SZSE:301413", "HKEX:2252", "HKEX:2675", "SSE:688322",
        "SZSE:002050", "SZSE:300124", "HKEX:2050", "SSE:688017", "SSE:601689",
    ]),
    ("TRADITIONAL",      ["OTC:ZIJMF", "SSE:600519"]),
    ("美股上市 (CN)", [
        "NASDAQ:WRD", "OTC:BYDDF", "NASDAQ:PONY", "NASDAQ:BIDU",
        "NYSE:BABA",  "NASDAQ:HSAI",
    ]),
    ("ETF",              ["SSE:562500", "SSE:515980", "SSE:516510"]),
    ("电力",              ["SZSE:002028", "SSE:600089"]),
    ("CCL/PCB", [
        "TWSE:6937", "SZSE:001389", "SZSE:002463", "SSE:600183",
    ]),
    ("OTHERS (CN)", [
        "HKEX:20", "SSE:688347", "SZSE:000338", "SZSE:300751",
        "SSE:688008", "SSE:688400",
    ]),
]

# Flatten into a lookup. Later entries win on duplicates, but the
# source files are disjoint so there are none.
SECTOR_MAP: dict[str, str] = {
    t: label for label, tickers in SECTORS for t in tickers
}

# Ordered list of bucket labels for dropdown rendering.
ALL_SECTORS: list[str] = [label for label, _ in SECTORS]


def sector_for(ticker: str) -> str:
    """Return the sector label for an EXCHANGE:CODE ticker, or '' if unknown."""
    if not ticker:
        return ""
    return SECTOR_MAP.get(ticker.upper(), "")


# ── EXCHANGE:CODE → yfinance ticker conversion ───────────────────────────────

_SUFFIX_BY_EXCHANGE = {
    "HKEX":   ".HK",
    "SSE":    ".SS",
    "SZSE":   ".SZ",
    "BSE":    ".BO",   # Bombay
    "TSE":    ".T",    # Tokyo
    "KRX":    ".KS",
    "TWSE":   ".TW",
    "TSX":    ".TO",
    "ASX":    ".AX",
    "XETR":   ".DE",
    "HOSE":   ".VN",
    # US venues — no suffix, yfinance uses bare symbol.
    "NASDAQ": "",
    "NYSE":   "",
    "AMEX":   "",
    "OTC":    "",
}


# Reverse of _SUFFIX_BY_EXCHANGE: dotted yfinance suffix → exchange code.
# Only the non-US suffixes need a back-mapping; bare US tickers can be either
# NYSE or NASDAQ so the lookup tries both.
_EXCHANGE_BY_SUFFIX: dict[str, str] = {
    ".HK":  "HKEX",
    ".SS":  "SSE",
    ".SZ":  "SZSE",
    ".BO":  "BSE",
    ".T":   "TSE",
    ".JP":  "TSE",   # internal display alias for Japan listings
    ".KS":  "KRX",
    ".TW":  "TWSE",
    ".TWO": "TWSE",   # GreTai over-the-counter folds into TWSE in our map
    ".TO":  "TSX",
    ".AX":  "ASX",
    ".DE":  "XETR",
    ".VN":  "HOSE",
}


def from_yfinance(yf_ticker: str) -> str | None:
    """Convert a yfinance-style ticker to EXCHANGE:CODE form.

    Examples:
        "1109.HK"     -> "HKEX:1109"
        "300750.SZ"   -> "SZSE:300750"
        "6361.T"      -> "TSE:6361"
        "LLY"         -> None  (US listings — ambiguous NYSE/NASDAQ, caller
                                must try both)
        "^GSPC"       -> None  (indices)

    Returns None for tickers without a recognised suffix; callers handling US
    listings should retry with "NYSE:<sym>" / "NASDAQ:<sym>" themselves.
    """
    if not yf_ticker:
        return None
    if "." not in yf_ticker:
        return None  # bare ticker = US, caller resolves
    code, _, suffix = yf_ticker.rpartition(".")
    suffix = "." + suffix
    exch = _EXCHANGE_BY_SUFFIX.get(suffix)
    if not exch:
        return None
    return f"{exch}:{code}"


def sector_for_yfinance(yf_ticker: str) -> str:
    """Look up a sector for a yfinance-style ticker.

    Tries the suffix-based mapping first, then for US listings retries
    NASDAQ: and NYSE: prefixes. Returns "" when nothing matches.
    """
    if not yf_ticker:
        return ""
    ec = from_yfinance(yf_ticker)
    if ec:
        return sector_for(ec)
    # Bare ticker → try both US venues
    bare = yf_ticker.upper().replace("-", ".")  # BRK-B → BRK.B
    for venue in ("NASDAQ", "NYSE", "AMEX"):
        s = sector_for(f"{venue}:{bare}")
        if s:
            return s
    return ""


def to_yfinance(ticker: str) -> str | None:
    """Convert EXCHANGE:CODE → yfinance ticker (e.g. NASDAQ:NVDA → 'NVDA',
    HKEX:2513 → '2513.HK'). Returns None if the exchange isn't recognised."""
    if not ticker or ":" not in ticker:
        return None
    exch, code = ticker.split(":", 1)
    suffix = _SUFFIX_BY_EXCHANGE.get(exch.upper())
    if suffix is None:
        return None
    # yfinance uses '-' for share classes (BRK.B → BRK-B); only do this for US.
    if not suffix:
        return code.replace(".", "-")
    return f"{code}{suffix}"
