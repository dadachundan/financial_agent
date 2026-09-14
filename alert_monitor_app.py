"""TradingView-style alert monitor mounted at /alert-monitor.

Shows a pannable/zoomable price chart and a sortable alert list enriched with
current-price distance to each alert trigger.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from flask import Blueprint, jsonify, render_template, request
from markupsafe import Markup

import nav_widget2 as nw2


alert_monitor_bp = Blueprint("alert_monitor", __name__, template_folder="templates")


@dataclass(frozen=True)
class AlertSeed:
    ticker: str
    yf_symbol: str
    description: str
    alert_price: float
    company: str = ""
    exchange: str = ""
    exchange_full: str = ""


# Seeded from the user's pasted TradingView alerts. The yfinance symbol can be
# changed here later if a TradingView ticker needs a different venue suffix.
# `exchange` is the short venue label shown as a badge and used by the
# exchange filter in the UI; leave it empty to let the resolver derive it.
ALERTS: tuple[AlertSeed, ...] = (
    AlertSeed("6869", "6869.HK", "6869 Crossing 100.5", 100.50,
              "Yangtze Optical Fibre and Cable", "HKEX", "Hong Kong Stock Exchange"),
    AlertSeed("IREN", "IREN", "IREN Crossing 29.84", 29.84,
              "IREN Limited", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("100", "0100.HK", "100 Crossing 208.4", 208.40,
              "MiniMax Group", "HKEX", "Hong Kong Stock Exchange"),
    AlertSeed("688256", "688256.SS", "688256 Crossing 688.98", 688.98,
              "Cambricon Technologies", "A-Share", "Shanghai Stock Exchange"),
    AlertSeed("SPCX", "SPCX", "SPCX Crossing 108.27", 108.27,
              "Space Exploration Technologies", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("SNDK", "SNDK", "SNDK Crossing 1,070.35", 1070.35,
              "Sandisk Corporation", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("STX", "STX", "STX Crossing 713.80", 713.80,
              "Seagate Technology Holdings", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("LITE", "LITE", "LITE Crossing 616.07", 616.07,
              "Lumentum Holdings", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("TER", "TER", "TER Crossing 316.78", 316.78,
              "Teradyne", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("GDX", "GDX", "GDX Crossing 74.98", 74.98,
              "VanEck Gold Miners ETF", "NYSE Arca", "NYSE Arca"),
    AlertSeed("XME", "XME", "XME Crossing 101.40", 101.40,
              "SPDR S&P Metals & Mining ETF", "NYSE Arca", "NYSE Arca"),
    AlertSeed("CRDO", "CRDO", "CRDO Crossing 182.05", 182.05,
              "Credo Technology Group", "NASDAQ", "Nasdaq Global Select Market"),
    AlertSeed("601899", "601899.SS", "601899 Crossing 24.89", 24.89,
              "Zijin Mining Group", "A-Share", "Shanghai Stock Exchange"),
)

# Venue label for each yfinance venue suffix.
_SUFFIX_EXCHANGE: dict[str, tuple[str, str]] = {
    ".HK": ("HKEX", "Hong Kong Stock Exchange"),
    ".SS": ("A-Share", "Shanghai Stock Exchange"),
    ".SH": ("A-Share", "Shanghai Stock Exchange"),
    ".SZ": ("A-Share", "Shenzhen Stock Exchange"),
    ".BJ": ("A-Share", "Beijing Stock Exchange"),
}

# yfinance exchange codes -> (short label, full name) for US listings.
_US_EXCHANGE: dict[str, tuple[str, str]] = {
    "NMS": ("NASDAQ", "Nasdaq Global Select Market"),
    "NGM": ("NASDAQ", "Nasdaq Global Market"),
    "NCM": ("NASDAQ", "Nasdaq Capital Market"),
    "NAS": ("NASDAQ", "Nasdaq"),
    "NYQ": ("NYSE", "New York Stock Exchange"),
    "NYS": ("NYSE", "New York Stock Exchange"),
    "PCX": ("NYSE Arca", "NYSE Arca"),
    "ASE": ("NYSE American", "NYSE American"),
    "BTS": ("BATS", "Cboe BZX"),
}


def _suffix_of(yf_symbol: str) -> tuple[str, str] | None:
    upper = yf_symbol.upper()
    for suffix, pair in _SUFFIX_EXCHANGE.items():
        if upper.endswith(suffix):
            return pair
    return None


@lru_cache(maxsize=256)
def _yf_profile(yf_symbol: str) -> dict[str, str]:
    """Company name / venue from yfinance. Only used when a seed omits them."""
    try:
        import yfinance as yf

        info = yf.Ticker(yf_symbol).get_info() or {}
    except Exception:
        return {"company": "", "exchange": "", "exchange_full": ""}
    hit = _US_EXCHANGE.get(str(info.get("exchange") or "").upper())
    return {
        "company": str(info.get("longName") or info.get("shortName") or ""),
        "exchange": hit[0] if hit else str(info.get("fullExchangeName") or ""),
        "exchange_full": hit[1] if hit else str(info.get("fullExchangeName") or ""),
    }


def _resolve_company(alert: AlertSeed) -> str:
    if alert.company:
        return alert.company
    if _suffix_of(alert.yf_symbol):
        import ticker_names

        name = ticker_names.get_name(alert.ticker) or ticker_names.get_name(alert.yf_symbol)
        if name:
            return name
    return _yf_profile(alert.yf_symbol)["company"]


def _resolve_exchange(alert: AlertSeed) -> tuple[str, str]:
    if alert.exchange:
        return alert.exchange, alert.exchange_full or alert.exchange
    pair = _suffix_of(alert.yf_symbol)
    if pair:
        return pair
    profile = _yf_profile(alert.yf_symbol)
    return profile["exchange"] or "US", profile["exchange_full"] or profile["exchange"] or "US"


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        f = float(value)
    except Exception:
        return None
    return f if f == f else None


@lru_cache(maxsize=256)
def _market_snapshot(yf_symbol: str) -> dict[str, Any]:
    try:
        import yfinance as yf

        tk = yf.Ticker(yf_symbol)
        price = None
        currency = ""
        try:
            fast = tk.fast_info
            price = _safe_float(getattr(fast, "last_price", None) or fast.get("last_price"))
            currency = getattr(fast, "currency", "") or fast.get("currency", "") or ""
        except Exception:
            pass
        hist = tk.history(period="1y", interval="1d", auto_adjust=False)
        if price is None and not hist.empty and "Close" in hist:
            price = _safe_float(hist["Close"].dropna().iloc[-1])
        high_1y = _safe_float(hist["High"].max()) if not hist.empty and "High" in hist else None
        low_1y = _safe_float(hist["Low"].min()) if not hist.empty and "Low" in hist else None
        return {
            "price": price,
            "currency": currency,
            "high_1y": high_1y,
            "low_1y": low_1y,
            "error": "" if price is not None else "no price",
        }
    except Exception as exc:
        return {"price": None, "currency": "", "high_1y": None, "low_1y": None, "error": str(exc)}


def _alert_payload(alert: AlertSeed) -> dict[str, Any]:
    d = asdict(alert)
    d["company"] = _resolve_company(alert)
    d["exchange"], d["exchange_full"] = _resolve_exchange(alert)
    px = _market_snapshot(alert.yf_symbol)
    current = px["price"]
    d["current_price"] = current
    d["currency"] = px.get("currency") or ""
    d["high_1y"] = px.get("high_1y")
    d["low_1y"] = px.get("low_1y")
    d["price_error"] = px.get("error") or ""
    if current is not None and current:
        d["diff_pct"] = ((alert.alert_price - current) / current) * 100.0
        d["diff_abs"] = alert.alert_price - current
    else:
        d["diff_pct"] = None
        d["diff_abs"] = None
    return d


@alert_monitor_bp.route("/")
def index():
    return render_template(
        "alert_monitor.html",
        NAV_HTML=Markup(nw2.NAV_HTML),
        initial_symbol=ALERTS[0].yf_symbol,
    )


@alert_monitor_bp.route("/api/alerts")
def api_alerts():
    refresh = request.args.get("refresh") == "1"
    if refresh:
        _market_snapshot.cache_clear()
    return jsonify({"alerts": [_alert_payload(a) for a in ALERTS]})


@alert_monitor_bp.route("/api/history/<path:yf_symbol>")
def api_history(yf_symbol: str):
    period = request.args.get("period", "1y")
    if period not in {"1mo", "3mo", "6mo", "1y", "2y", "5y"}:
        period = "1y"
    try:
        import yfinance as yf

        hist = yf.Ticker(yf_symbol).history(period=period, interval="1d", auto_adjust=False)
        bars = []
        if not hist.empty:
            for idx, row in hist.iterrows():
                close = _safe_float(row.get("Close"))
                if close is None:
                    continue
                bars.append({
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": _safe_float(row.get("Open")),
                    "high": _safe_float(row.get("High")),
                    "low": _safe_float(row.get("Low")),
                    "close": close,
                    "volume": _safe_float(row.get("Volume")),
                })
        return jsonify({"ok": bool(bars), "symbol": yf_symbol, "period": period, "bars": bars})
    except Exception as exc:
        return jsonify({"ok": False, "symbol": yf_symbol, "period": period, "bars": [], "error": str(exc)}), 200
