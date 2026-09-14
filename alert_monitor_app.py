"""TradingView-style alert monitor mounted at /alert-monitor.

Shows a pannable/zoomable price chart and a sortable alert list enriched with
current-price distance to each alert trigger.

Every alert lives in one SQLite table (see :mod:`alert_monitor_db`): the
seeded TradingView alerts in ALERTS become rows on first run, alerts added
through the UI are appended beside them, and the two behave identically.
Deleting an alert marks it obsolete instead of removing it, so the list keeps
its history.
"""
from __future__ import annotations

import json
import pathlib
import uuid
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any

from flask import Blueprint, jsonify, render_template, request
from markupsafe import Markup

import alert_monitor_db as alert_db
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


# -- Storage -------------------------------------------------------------------
# The alert list lives in db/alert_monitor.db (see alert_monitor_db). ALERTS is
# only the seed used on a fresh install; alert_monitor_alerts.json is the store
# this module used before the move to SQLite, read once so the entries and
# deletions recorded there survive the upgrade.
_LEGACY_STORE = pathlib.Path(__file__).with_name("alert_monitor_alerts.json")

_EXCHANGE_SUFFIXES = ("HK", "SS", "SH", "SZ", "BJ")


def _seed_rows() -> list[dict[str, Any]]:
    """ALERTS as alert rows. Ids key on the symbol so reordering keeps them."""
    rows: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    for seed in ALERTS:
        base = f"seed-{seed.yf_symbol}"
        seen[base] = seen.get(base, 0) + 1
        rows.append({
            "id": base if seen[base] == 1 else f"{base}#{seen[base]}",
            "ticker": seed.ticker,
            "yf_symbol": seed.yf_symbol,
            "description": seed.description,
            "alert_price": seed.alert_price,
            "company": seed.company,
            "exchange": seed.exchange,
            "exchange_full": seed.exchange_full,
        })
    return rows


def _legacy_row(item: dict[str, Any]) -> dict[str, Any] | None:
    """Validate one record from the retired JSON store, or None if malformed."""
    yf_symbol = str(item.get("yf_symbol") or "").strip()
    try:
        price = float(item.get("alert_price"))
    except (TypeError, ValueError):
        return None
    if not yf_symbol or price <= 0:
        return None
    ticker = str(item.get("ticker") or yf_symbol).strip() or yf_symbol
    return {
        "id": str(item.get("id") or f"user-{uuid.uuid4().hex[:8]}"),
        "ticker": ticker,
        "yf_symbol": yf_symbol,
        "description": str(item.get("description") or f"{ticker} Crossing {price:,.2f}"),
        "alert_price": price,
        "company": str(item.get("company") or ""),
        "exchange": str(item.get("exchange") or ""),
        "exchange_full": str(item.get("exchange_full") or ""),
        "created_at": str(item.get("created_at") or ""),
        "obsolete_at": str(item.get("obsolete_at") or "") or None,
    }


def _import_legacy_store() -> None:
    """One-time import of alert_monitor_alerts.json, the pre-SQLite store."""
    if not _LEGACY_STORE.exists():
        return
    try:
        raw = json.loads(_LEGACY_STORE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[alert_monitor] could not read {_LEGACY_STORE.name}: {exc}")
        return
    if isinstance(raw, list):  # oldest format: a bare list of alerts
        raw = {"alerts": raw, "hidden_seeds": []}
    if not isinstance(raw, dict):
        return
    added = 0
    for item in raw.get("alerts") or []:
        row = _legacy_row(item) if isinstance(item, dict) else None
        if not row:
            continue
        try:
            alert_db.insert_alert(row)
            added += 1
        except alert_db.DuplicateAlert:
            pass  # an alert for that symbol and price is already live
    hidden = raw.get("hidden_seeds") or []
    retired = sum(1 for seed_id in hidden
                  if isinstance(seed_id, str) and alert_db.set_obsolete(seed_id))
    if added or retired:
        print(f"[alert_monitor] imported {added} alert(s) and {retired} deletion(s) "
              f"from {_LEGACY_STORE.name}")


def init_db() -> None:
    """Create and, on a fresh install, seed the alert store. Idempotent."""
    if alert_db.init_db(_seed_rows()):
        _import_legacy_store()


def _row_payload(row: dict[str, Any]) -> dict[str, Any]:
    """One alert row as the API payload, enriched with its market snapshot."""
    alert = AlertSeed(row["ticker"], row["yf_symbol"], row["description"],
                      row["alert_price"], row["company"], row["exchange"],
                      row["exchange_full"])
    payload = _alert_payload(alert, row["id"])
    payload["created_at"] = row.get("created_at") or ""
    payload["obsolete_at"] = row.get("obsolete_at") or ""
    return payload


# The store is ready as soon as the blueprint is imported, so the app works
# whether or not the caller initialises it explicitly.
init_db()


def _symbol_candidates(raw: str) -> list[tuple[str, str]]:
    """Turn user input into (yfinance symbol, display ticker) guesses, best first."""
    text = raw.strip().upper().replace(" ", "")
    if not text:
        return []
    if "." in text:
        base, _, suffix = text.partition(".")
        if suffix in _EXCHANGE_SUFFIXES:
            return [(text, base)]
        return [(text, text)]
    if text.isdigit():
        if len(text) >= 6:  # A-share board code
            first = "SS" if text.startswith("6") else ("BJ" if text[0] in "48" else "SZ")
            order = [first] + [s for s in ("SS", "SZ", "BJ") if s != first]
            return [(f"{text}.{s}", text) for s in order]
        # Hong Kong codes are quoted with four digits on Yahoo
        return [(f"{text.zfill(4)}.HK", text)]
    return [(text, text)]


def resolve_symbol(raw: str) -> tuple[str, str] | None:
    """Resolve user input to a live (yfinance symbol, display ticker)."""
    for yf_symbol, ticker in _symbol_candidates(raw):
        if _market_snapshot(yf_symbol).get("price"):
            return yf_symbol, ticker
    return None


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


def _alert_payload(alert: AlertSeed, alert_id: str = "") -> dict[str, Any]:
    d = asdict(alert)
    d["id"] = alert_id
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
    live = alert_db.list_alerts()
    return render_template(
        "alert_monitor.html",
        NAV_HTML=Markup(nw2.NAV_HTML),
        initial_symbol=live[0]["yf_symbol"] if live else ALERTS[0].yf_symbol,
    )


@alert_monitor_bp.route("/api/alerts")
def api_alerts():
    refresh = request.args.get("refresh") == "1"
    if refresh:
        _market_snapshot.cache_clear()
    rows = alert_db.list_alerts(
        include_obsolete=request.args.get("include_obsolete") == "1")
    return jsonify({"alerts": [_row_payload(row) for row in rows]})


@alert_monitor_bp.route("/api/alerts", methods=["POST"])
def api_add_alert():
    """Add an alert from a symbol and a target price."""
    payload = request.get_json(silent=True) or {}
    raw_symbol = str(payload.get("symbol") or "").strip()
    if not raw_symbol:
        return jsonify({"ok": False, "error": "Enter a symbol."}), 400
    try:
        price = float(payload.get("alert_price"))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Enter a target price."}), 400
    if not price > 0:
        return jsonify({"ok": False, "error": "Target price must be greater than zero."}), 400

    resolved = resolve_symbol(raw_symbol)
    if not resolved:
        return jsonify({"ok": False,
                        "error": f"No market data found for \u201c{raw_symbol}\u201d."}), 400
    yf_symbol, ticker = resolved
    seed = AlertSeed(ticker, yf_symbol, f"{ticker} Crossing {price:,.2f}", price)
    exchange, exchange_full = _resolve_exchange(seed)
    row = {
        "id": f"user-{uuid.uuid4().hex[:8]}",
        "ticker": ticker,
        "yf_symbol": yf_symbol,
        "description": seed.description,
        "alert_price": price,
        "company": _resolve_company(seed),
        "exchange": exchange,
        "exchange_full": exchange_full,
        "created_at": alert_db.now_iso(),
    }
    try:
        alert_db.insert_alert(row)
    except alert_db.DuplicateAlert:
        return jsonify({"ok": False,
                        "error": f"{yf_symbol} already has an alert at {price:,.2f}."}), 409
    return jsonify({"ok": True, "alert": _row_payload(row)})


@alert_monitor_bp.route("/api/alerts/<path:alert_id>", methods=["DELETE"])
def api_delete_alert(alert_id: str):
    """Delete an alert by marking it obsolete -- the row is kept for the record."""
    if alert_db.get_alert(alert_id) is None:
        return jsonify({"ok": False, "error": "Alert not found."}), 404
    stamp = alert_db.set_obsolete(alert_id)
    if stamp is None:
        return jsonify({"ok": False, "error": "Alert is already obsolete."}), 409
    return jsonify({"ok": True, "id": alert_id, "obsolete_at": stamp})


@alert_monitor_bp.route("/api/alerts/<path:alert_id>/restore", methods=["POST"])
def api_restore_alert(alert_id: str):
    """Bring an obsolete alert back into the active list."""
    row = alert_db.get_alert(alert_id)
    if row is None:
        return jsonify({"ok": False, "error": "Alert not found."}), 404
    if not row["obsolete_at"]:
        return jsonify({"ok": False, "error": "Alert is not obsolete."}), 409
    try:
        alert_db.clear_obsolete(alert_id)
    except alert_db.DuplicateAlert:
        return jsonify({"ok": False,
                        "error": f"{row['yf_symbol']} already has an active alert "
                                 f"at {row['alert_price']:,.2f}."}), 409
    return jsonify({"ok": True, "id": alert_id, "obsolete_at": ""})


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
