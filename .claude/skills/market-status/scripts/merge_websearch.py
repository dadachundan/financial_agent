"""
Merge WebSearch fallback results into the build_status JSON summary.

Run after build_status.py emits its summary + websearch queue, and after
the agent has populated a `_websearch_results.json` file (same path stem)
with per-indicator values.

Usage:
  python .claude/skills/market-status/scripts/merge_websearch.py --date 2026-06-07

Reads:
  oneoff/market_status_<DATE>_summary.json
  oneoff/market_status_<DATE>_websearch_results.json

Writes (in place — overwrites the original summary):
  oneoff/market_status_<DATE>_summary.json
    - patches each headline_indicators row with WebSearch value/url/date
    - recomputes the composite over the now-active indicator set
    - adds a `panel.websearch_extras` block with the 4 supplementary lookups
    - the `tier` field gets refreshed

The merge is deterministic — no LLM calls, no external HTTP. Re-runnable.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ONEOFF_DIR   = PROJECT_ROOT / "oneoff"


def _tier_for_score(score: float) -> str:
    if score is None or np.isnan(score):
        return "n/a"
    if score >= 80: return "Frothy"
    if score >= 60: return "Stretched"
    if score >= 40: return "Elevated"
    if score >= 20: return "Neutral"
    return "Subdued"


def _decile_label(pct: float | None) -> str:
    if pct is None or (isinstance(pct, float) and np.isnan(pct)):
        return "n/a"
    if pct >= 90: return "10th (most exuberant)"
    if pct >= 80: return "9th"
    if pct >= 70: return "8th"
    if pct >= 60: return "7th"
    if pct >= 50: return "6th"
    if pct >= 40: return "5th"
    if pct >= 30: return "4th"
    if pct >= 20: return "3rd"
    if pct >= 10: return "2nd"
    return "1st (least exuberant)"


# Map between the IDs the build_status script uses for headline rows
# and the IDs the WebSearch step writes. Mostly 1:1; spec_trade_proxy
# is the proxy row but WebSearch result is keyed on spec_trade.
ID_BRIDGE = {
    "breadth_52w":      "breadth_52w",
    "spec_trade_proxy": "spec_trade",  # override the proxy when GS-cited value lands
    "put_call":         "put_call",
    "short_interest":   "short_interest",
    "yale_confidence":  "yale_confidence",
    "aaii_bullbear":    "aaii_bullbear",
    "ipo_count":        "ipo_count",
    "net_issuance":     "net_issuance",
}

# Indicators in the WebSearch results that go into the BROADER panel, not the headline 9.
PANEL_EXTRAS = [
    "gs_sentiment_indicator",
    "eps_revision_breadth",
    "fwd_eps_growth_2026",
    "fed_funds_2026_implied",
]


def merge(date_slug: str) -> dict:
    summary_path = ONEOFF_DIR / f"market_status_{date_slug}_summary.json"
    ws_path      = ONEOFF_DIR / f"market_status_{date_slug}_websearch_results.json"
    if not summary_path.exists():
        raise SystemExit(f"summary not found: {summary_path}")
    if not ws_path.exists():
        raise SystemExit(
            f"websearch results not found: {ws_path}\n"
            f"The agent must populate this file from the WebSearch queue before merging."
        )
    summary = json.loads(summary_path.read_text())
    ws      = json.loads(ws_path.read_text())
    ws_results = ws.get("results", {})

    patched_count = 0
    for row in summary["headline_indicators"]:
        ws_id = ID_BRIDGE.get(row["id"])
        if not ws_id:
            continue
        if ws_id not in ws_results:
            continue
        wr = ws_results[ws_id]
        # Override fields the WebSearch step provided
        if wr.get("value") is not None:
            row["current_value"] = wr["value"]
            row["unit"]          = wr.get("value_unit") or row.get("unit")
        if wr.get("exuberance_pct_estimate") is not None:
            row["exuberance_pct"] = float(wr["exuberance_pct_estimate"])
            row["decile"]         = _decile_label(row["exuberance_pct"])
        if wr.get("source_url"):
            row["source_url"]  = wr["source_url"]
        if wr.get("source_date"):
            row["source_date"] = wr["source_date"]
        if wr.get("source_title"):
            row["source_title"] = wr["source_title"]
        if wr.get("note"):
            row["note"] = wr["note"]
        row["fetched"] = (row["current_value"] is not None) or (row.get("exuberance_pct") is not None)
        if row["fetched"]:
            patched_count += 1

    # Recompute composite over the fetched headline indicators ONLY
    # (drop the spec_trade_proxy when spec_trade override fired; otherwise keep proxy)
    spec_override_fired = (
        ws_results.get("spec_trade", {}).get("exuberance_pct_estimate") is not None
    )
    fetched_pcts = []
    for row in summary["headline_indicators"]:
        if row["id"] == "spec_trade_proxy" and spec_override_fired:
            # Once GS-cited spec_trade is in, the proxy row carries the GS percentile too
            # so it stays in but is no longer just a proxy — relabel.
            row["label"] = "GS Speculative Trading Indicator"
            row["is_proxy"] = False
        if row.get("fetched") and row.get("exuberance_pct") is not None:
            fetched_pcts.append(row["exuberance_pct"])

    composite = float(np.mean(fetched_pcts)) if fetched_pcts else float("nan")
    summary["composite_score"] = round(composite, 1) if not np.isnan(composite) else None
    summary["tier"] = _tier_for_score(composite)
    summary["active_indicator_count"] = len(fetched_pcts)

    # Panel extras
    panel = summary.setdefault("panel", {})
    extras = {}
    for key in PANEL_EXTRAS:
        if key in ws_results:
            extras[key] = ws_results[key]
    if extras:
        panel["websearch_extras"] = extras

    summary["merged_at"] = _dt.datetime.now().isoformat(timespec="seconds")
    summary["websearch_patched_count"] = patched_count

    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print(json.dumps({
        "as_of":            date_slug,
        "composite_score":  summary["composite_score"],
        "tier":             summary["tier"],
        "active_indicator_count": summary["active_indicator_count"],
        "websearch_patched":      patched_count,
    }, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=_dt.date.today().isoformat())
    args = parser.parse_args()
    merge(args.date)


if __name__ == "__main__":
    main()
