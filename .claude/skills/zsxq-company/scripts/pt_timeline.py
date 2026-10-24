#!/usr/bin/env python3
"""Render a per-broker price-target timeline vs the share price.

Read-only: takes a JSON spec of PT observations the agent extracted from the
zsxq PDFs, optionally pulls the share price from yfinance, and writes a PNG.
No DB access.

Spec (JSON file or `-` for stdin):
{
  "title": "WeRide (WRD) — sell-side price targets vs share price",
  "unit": "US$ per ADS",
  "price_ticker": "WRD",              # optional; yfinance symbol, same unit as PTs
  "source": "Source: broker PDFs in zsxq library (...) · price: Yahoo Finance",
  "brokers": [
    {"name": "Morgan Stanley", "rating": "OW",
     "points": [{"date": "2026-01-29", "pt": 14.70},
                {"date": "2026-07-01", "pt": 13.10}]}
  ],
  "annotations": [{"date": "2026-07-01", "pt": 13.10,
                   "text": "MS cut 14.7→13.1\\nslower fleet ramp", "dx": -95, "dy": -60}]
}

PTs in a different currency / share class must be converted by the agent
before they go into the spec (say how in `source`).

Usage:
  python pt_timeline.py --spec spec.json --out /path/to/chart.png
"""
from __future__ import annotations

import argparse
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

PALETTE = ["#2563eb", "#d97706", "#059669", "#dc2626", "#7c3aed", "#0891b2",
           "#db2777", "#65a30d", "#9333ea", "#ea580c"]


def load_price(symbol: str, start: pd.Timestamp) -> pd.Series:
    import yfinance as yf

    df = yf.download(symbol, start=start.strftime("%Y-%m-%d"), progress=False,
                     auto_adjust=False)
    if df.empty:
        return pd.Series(dtype=float)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.dropna()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--spec", required=True, help="JSON spec path, or - for stdin")
    ap.add_argument("--out", required=True, help="output PNG path")
    args = ap.parse_args()

    spec = json.load(sys.stdin if args.spec == "-" else open(args.spec))
    if not spec.get("source"):
        sys.exit("spec.source is required (chart must carry its data source)")

    brokers = spec["brokers"]
    all_dates = [pd.Timestamp(p["date"]) for b in brokers for p in b["points"]]
    first = min(all_dates) - pd.Timedelta(days=14)

    px = load_price(spec["price_ticker"], first) if spec.get("price_ticker") else pd.Series(dtype=float)
    end = max([*all_dates, *(px.index[-1:] if len(px) else [])])
    if len(px) == 0:
        end = pd.Timestamp.today().normalize()

    fig, ax = plt.subplots(figsize=(12, 6.8))
    top = 0.0
    for i, b in enumerate(brokers):
        c = PALETTE[i % len(PALETTE)]
        pts = sorted(b["points"], key=lambda p: p["date"])
        d = [pd.Timestamp(p["date"]) for p in pts]
        v = [float(p["pt"]) for p in pts]
        top = max(top, *v)
        label = f'{b["name"]} ({b["rating"]})' if b.get("rating") else b["name"]
        ax.step(d + [d[-1]], v + [v[-1]], where="post", color=c, lw=2.2, label=label)
        ax.plot([d[-1], end], [v[-1], v[-1]], color=c, lw=1.2, ls=":")
        ax.scatter(d, v, color=c, s=36, zorder=3)

    if len(px):
        top = max(top, float(px.max()))
        ax.plot(px.index, px.values, color="#111827", lw=1.6,
                label=f'{spec["price_ticker"]} close')
        ax.annotate(f"Now {px.iloc[-1]:.2f}\n({px.index[-1]:%b %d})",
                    (px.index[-1], px.iloc[-1]), xytext=(-60, -30),
                    textcoords="offset points", fontsize=8.5, fontweight="bold")

    for a in spec.get("annotations", []):
        ax.annotate(a["text"], (pd.Timestamp(a["date"]), float(a["pt"])),
                    xytext=(a.get("dx", 10), a.get("dy", 10)), textcoords="offset points",
                    fontsize=8.2, color="#374151",
                    arrowprops=dict(arrowstyle="-", color="#6b7280", lw=0.8))

    ax.set_xlim(first, end + pd.Timedelta(days=4))
    ax.set_ylim(0, top * 1.15)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%y"))
    ax.set_ylabel(spec.get("unit", "Price"))
    ax.grid(alpha=0.25)
    ax.set_title(spec.get("title", "Sell-side price targets"), fontsize=13, loc="left")
    ax.legend(loc=spec.get("legend_loc", "lower left"), fontsize=8.5, ncol=3, frameon=False)
    footer = spec["source"] + "\nDotted = last published PT carried forward to the latest price date."
    fig.text(0.01, 0.012, footer, fontsize=7.3, color="#6b7280")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(args.out, dpi=160)
    print(json.dumps({"out": args.out, "x_start": str(first.date()), "x_end": str(end.date()),
                      "last_price": float(px.iloc[-1]) if len(px) else None}))


if __name__ == "__main__":
    main()
