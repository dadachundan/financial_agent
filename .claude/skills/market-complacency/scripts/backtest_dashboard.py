"""
Backtest the market-complacency composite against actual SPY/QQQ drawdowns.

Questions answered:
  1. Conditional probability: for each composite tier, what fraction of
     trading days were followed by a >10% / >15% / >20% drawdown within
     60 / 90 / 180 trading days?
  2. Event study: at each of the top-10 worst historical drawdowns (peak →
     trough), what was the composite reading 30 / 60 / 90 days before the
     peak? Did the dashboard "see" the drop coming?
  3. Precision / recall: treating "composite > T" as a sell signal, what's
     the hit rate (how many sell signals were followed by a real drawdown
     within 90 days) and the recall (how many real drawdowns were preceded
     by a sell signal)?

Usage:
  python .claude/skills/market-complacency/scripts/backtest_dashboard.py \
    --composite-history oneoff/market_complacency_<DATE>_composite_history.csv \
    --benchmark SPY \
    --as-of 2026-06-07

Outputs:
  oneoff/backtest_<BENCHMARK>_<DATE>_conditional.csv     — P(dd > X% | tier)
  oneoff/backtest_<BENCHMARK>_<DATE>_event_study.csv     — composite at peak − 30/60/90d
  oneoff/backtest_<BENCHMARK>_<DATE>_threshold_sweep.csv — precision/recall over thresholds
  reports/charts/backtest_<BENCHMARK>_<DATE>_*.png       — visualizations

No DB writes, no LLM calls.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[4]
ONEOFF = PROJECT_ROOT / "oneoff"
CHARTS = PROJECT_ROOT / "reports" / "charts"


def fetch_benchmark(ticker: str, start: str, end: str) -> pd.Series:
    df = yf.download(ticker, start=start, end=end, progress=False,
                     auto_adjust=True, threads=False)
    if df.empty:
        raise RuntimeError(f"No data for {ticker}")
    if isinstance(df.columns, pd.MultiIndex):
        s = df["Close"].iloc[:, 0]
    else:
        s = df["Close"]
    if s.index.tz is not None:
        s.index = s.index.tz_localize(None)
    s.name = ticker
    return s.dropna()


def forward_max_drawdown(prices: pd.Series, horizon_days: int) -> pd.Series:
    """For each date t, the minimum (most negative) future return relative to
    today's price over the next `horizon_days` trading days.

    forward_min_return_t = min over k in [1, H] of (P_{t+k} / P_t - 1)

    Negative = a future drawdown is coming. Lower = bigger drawdown.
    """
    n = len(prices)
    arr = prices.values
    out = np.full(n, np.nan)
    for i in range(n):
        end = min(i + 1 + horizon_days, n)
        if end <= i + 1:
            continue
        window = arr[i + 1:end]
        if len(window) == 0:
            continue
        out[i] = (window.min() / arr[i]) - 1.0
    return pd.Series(out, index=prices.index, name=f"fwd_min_{horizon_days}d")


def tier(score: float) -> str:
    if pd.isna(score): return "n/a"
    if score < 20: return "0-20 Panicked"
    if score < 40: return "20-40 Cautious"
    if score < 60: return "40-60 Neutral"
    if score < 80: return "60-80 Elevated"
    return "80-100 Stretched"


def conditional_drawdown_table(composite: pd.Series, prices: pd.Series,
                               horizons: list[int]) -> pd.DataFrame:
    """For each (tier × horizon × threshold) combination, P(forward dd > thr | tier)."""
    fwd = {h: forward_max_drawdown(prices, h) for h in horizons}
    df = pd.DataFrame({"composite": composite})
    for h, s in fwd.items():
        df[f"fwd_min_{h}d"] = s.reindex(df.index)
    df = df.dropna(subset=["composite"]).copy()
    df["tier"] = df["composite"].apply(tier)

    rows = []
    thresholds = [-0.05, -0.10, -0.15, -0.20]
    for t_name in ["0-20 Panicked", "20-40 Cautious", "40-60 Neutral",
                   "60-80 Elevated", "80-100 Stretched"]:
        sub = df[df["tier"] == t_name]
        n_total = len(sub)
        if n_total == 0:
            continue
        for h in horizons:
            col = f"fwd_min_{h}d"
            valid = sub[col].dropna()
            if len(valid) == 0:
                continue
            row = {
                "tier": t_name,
                "horizon_days": h,
                "n_obs": len(valid),
                "mean_fwd_min_pct": round(valid.mean() * 100, 2),
                "median_fwd_min_pct": round(valid.median() * 100, 2),
                "p10_fwd_min_pct": round(valid.quantile(0.10) * 100, 2),
            }
            for thr in thresholds:
                hits = (valid < thr).sum()
                row[f"prob_dd_lt_{int(thr*100)}pct"] = round(hits / len(valid) * 100, 1)
            rows.append(row)

    return pd.DataFrame(rows)


def find_drawdown_events(prices: pd.Series, min_dd_pct: float = -0.10,
                         min_separation_days: int = 90) -> pd.DataFrame:
    """Identify peak-to-trough drawdown episodes.

    Returns one row per episode with:
      peak_date / peak_px / trough_date / trough_px / drawdown_pct /
      days_peak_to_trough
    Episodes with magnitude smaller than min_dd_pct (e.g., -0.10 = -10%) are
    excluded. Adjacent episodes within min_separation_days are merged into
    the deeper one.
    """
    p = prices.copy()
    running_max = p.cummax()
    dd = p / running_max - 1.0

    # Find local-minimum drawdown points
    events = []
    i = 0
    n = len(p)
    while i < n:
        if dd.iloc[i] >= min_dd_pct:
            i += 1
            continue
        # We're in drawdown territory — find the trough of this episode
        # (the deepest dd until prices recover to peak)
        # Trough = argmin of dd over the contiguous below-zero run that
        # contains today, until we make a new high.
        peak_px = running_max.iloc[i]
        peak_idx = p[p == peak_px].index
        # Find the actual peak (most recent date when running_max set this level)
        peak_date = peak_idx[peak_idx <= p.index[i]].max()

        # Trough = the deepest point until prices recover
        j = i
        trough_idx = i
        trough_val = dd.iloc[i]
        while j < n and p.iloc[j] < peak_px:
            if dd.iloc[j] < trough_val:
                trough_val = dd.iloc[j]
                trough_idx = j
            j += 1

        events.append({
            "peak_date": peak_date.strftime("%Y-%m-%d"),
            "peak_px": float(peak_px),
            "trough_date": p.index[trough_idx].strftime("%Y-%m-%d"),
            "trough_px": float(p.iloc[trough_idx]),
            "drawdown_pct": round(float(trough_val) * 100, 2),
            "days_peak_to_trough": int((p.index[trough_idx] - peak_date).days),
        })
        i = j + 1

    df = pd.DataFrame(events)
    if df.empty:
        return df

    # Merge clustered events (the second wave of a same regime turn shouldn't
    # be a separate observation).
    df["peak_dt"] = pd.to_datetime(df["peak_date"])
    df["trough_dt"] = pd.to_datetime(df["trough_date"])
    df = df.sort_values("peak_dt").reset_index(drop=True)
    keep = []
    last_trough = None
    for _, r in df.iterrows():
        if last_trough is not None and (r["peak_dt"] - last_trough).days < min_separation_days:
            # Merge: extend the previous event's trough if this one is deeper
            prev = keep[-1]
            if r["drawdown_pct"] < prev["drawdown_pct"]:
                prev["trough_date"] = r["trough_date"]
                prev["trough_px"] = r["trough_px"]
                prev["drawdown_pct"] = r["drawdown_pct"]
                prev["days_peak_to_trough"] = (r["trough_dt"] - pd.to_datetime(prev["peak_date"])).days
            last_trough = max(last_trough, r["trough_dt"])
            continue
        keep.append(r.to_dict())
        last_trough = r["trough_dt"]
    return pd.DataFrame(keep).drop(columns=["peak_dt", "trough_dt"], errors="ignore")


def event_study(composite: pd.Series, events: pd.DataFrame,
                lookback_days: list[int]) -> pd.DataFrame:
    """For each drawdown event, look up the composite N days before the peak."""
    rows = []
    for _, ev in events.iterrows():
        peak_dt = pd.Timestamp(ev["peak_date"])
        row = {
            "peak_date": ev["peak_date"],
            "trough_date": ev["trough_date"],
            "drawdown_pct": ev["drawdown_pct"],
            "days_peak_to_trough": ev["days_peak_to_trough"],
        }
        for lb in lookback_days:
            lookup_date = peak_dt - pd.Timedelta(days=lb)
            avail = composite[composite.index <= lookup_date]
            if len(avail) == 0:
                row[f"composite_T-{lb}d"] = None
                row[f"tier_T-{lb}d"] = "n/a"
            else:
                val = float(avail.iloc[-1])
                row[f"composite_T-{lb}d"] = round(val, 1)
                row[f"tier_T-{lb}d"] = tier(val)
        # Composite at the peak itself
        avail = composite[composite.index <= peak_dt]
        if len(avail) > 0:
            row["composite_at_peak"] = round(float(avail.iloc[-1]), 1)
            row["tier_at_peak"] = tier(float(avail.iloc[-1]))
        else:
            row["composite_at_peak"] = None
            row["tier_at_peak"] = "n/a"
        rows.append(row)
    return pd.DataFrame(rows)


def threshold_sweep(composite: pd.Series, prices: pd.Series,
                    horizon: int, dd_thr_pct: float) -> pd.DataFrame:
    """For each candidate threshold T in [40, 90], compute:
       - True positives: days with composite >= T followed by dd < dd_thr_pct within horizon
       - False positives: days with composite >= T not followed by such a drawdown
       - False negatives: days with composite < T but followed by such a drawdown
    """
    fwd = forward_max_drawdown(prices, horizon).rename("fwd_min")
    df = pd.concat([composite.rename("composite"), fwd], axis=1).dropna()

    rows = []
    for T in range(40, 95, 5):
        signal = df["composite"] >= T
        bad = df["fwd_min"] < dd_thr_pct
        tp = int((signal & bad).sum())
        fp = int((signal & ~bad).sum())
        fn = int((~signal & bad).sum())
        tn = int((~signal & ~bad).sum())
        prec = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
        rec = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
        # Base rate: probability of drawdown unconditionally
        base = bad.sum() / len(df)
        # Lift: precision / base rate
        lift = prec / base if base > 0 else float("nan")
        rows.append({
            "threshold": T,
            "n_signal_days": int(signal.sum()),
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision_pct": round(prec * 100, 1) if not pd.isna(prec) else None,
            "recall_pct": round(rec * 100, 1) if not pd.isna(rec) else None,
            "base_rate_pct": round(base * 100, 1),
            "lift": round(lift, 2) if not pd.isna(lift) else None,
        })
    return pd.DataFrame(rows)


def make_charts(as_of: str, benchmark: str, composite: pd.Series, prices: pd.Series,
                cond_df: pd.DataFrame, events_df: pd.DataFrame, event_df: pd.DataFrame,
                sweep_df: pd.DataFrame):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # Chart 1: composite overlaid on benchmark drawdown
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                    gridspec_kw={"height_ratios": [2, 1]})
    running_max = prices.cummax()
    dd = (prices / running_max - 1.0) * 100
    ax1.fill_between(dd.index, 0, dd.values, color="#d62828", alpha=0.4)
    ax1.set_ylabel(f"{benchmark} Drawdown (%)")
    ax1.set_title(f"Composite vs {benchmark} drawdown — does high complacency precede drops?")
    ax1.grid(alpha=0.3)

    # Mark the major drawdown events
    for _, ev in events_df.iterrows():
        if ev["drawdown_pct"] < -10:
            ax1.axvline(pd.Timestamp(ev["peak_date"]), color="black", alpha=0.3, ls=":")
            ax1.annotate(f"{ev['drawdown_pct']:.0f}%",
                         xy=(pd.Timestamp(ev["trough_date"]), ev["drawdown_pct"]),
                         xytext=(0, -5), textcoords="offset points",
                         ha="center", fontsize=7, color="darkred")

    ax2.plot(composite.index, composite.values, lw=0.8, color="#1f4e79")
    ax2.axhline(80, color="red", ls="--", alpha=0.5, label="Stretched (80)")
    ax2.axhline(60, color="orange", ls="--", alpha=0.5, label="Elevated (60)")
    ax2.set_ylabel("Composite")
    ax2.set_ylim(0, 100)
    ax2.grid(alpha=0.3)
    ax2.legend(loc="lower right", fontsize=8)
    ax2.xaxis.set_major_locator(mdates.YearLocator(2))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.tight_layout()
    plt.savefig(CHARTS / f"backtest_{benchmark}_{as_of}_overlay.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Chart 2: conditional probability heatmap-ish
    if not cond_df.empty:
        horizons = sorted(cond_df["horizon_days"].unique())
        tiers = ["0-20 Panicked", "20-40 Cautious", "40-60 Neutral",
                 "60-80 Elevated", "80-100 Stretched"]
        thresholds = [-5, -10, -15, -20]
        n_thr = len(thresholds)
        fig, axes = plt.subplots(1, n_thr, figsize=(4 * n_thr, 5), sharey=True)
        for ax, thr in zip(axes, thresholds):
            mat = np.full((len(tiers), len(horizons)), np.nan)
            for i, tn in enumerate(tiers):
                for j, h in enumerate(horizons):
                    row = cond_df[(cond_df["tier"] == tn) & (cond_df["horizon_days"] == h)]
                    if not row.empty:
                        mat[i, j] = row.iloc[0][f"prob_dd_lt_{thr}pct"]
            im = ax.imshow(mat, aspect="auto", cmap="Reds", vmin=0, vmax=max(40, np.nanmax(mat)))
            ax.set_xticks(range(len(horizons)))
            ax.set_xticklabels([f"{h}d" for h in horizons])
            ax.set_yticks(range(len(tiers)))
            ax.set_yticklabels([t.replace(" ", "\n", 1) for t in tiers], fontsize=8)
            ax.set_title(f"P(dd ≥ {-thr}%)\nwithin H days")
            for i in range(len(tiers)):
                for j in range(len(horizons)):
                    if not np.isnan(mat[i, j]):
                        ax.text(j, i, f"{mat[i,j]:.0f}", ha="center", va="center",
                                color="white" if mat[i, j] > 20 else "black", fontsize=8)
        fig.suptitle(f"Conditional Drawdown Probability ({benchmark}) — by composite tier")
        plt.tight_layout()
        plt.savefig(CHARTS / f"backtest_{benchmark}_{as_of}_conditional.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 3: event study scatter
    if not event_df.empty and "composite_T-30d" in event_df.columns:
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.scatter(event_df["composite_T-30d"], event_df["drawdown_pct"],
                   s=60, alpha=0.7, color="#1d3557")
        for _, r in event_df.iterrows():
            if pd.notna(r["composite_T-30d"]):
                ax.annotate(r["peak_date"][:7],
                            xy=(r["composite_T-30d"], r["drawdown_pct"]),
                            xytext=(5, 5), textcoords="offset points", fontsize=8)
        ax.axvline(60, color="orange", ls="--", alpha=0.5)
        ax.axvline(80, color="red", ls="--", alpha=0.5)
        ax.set_xlabel("Composite 30 days before peak")
        ax.set_ylabel("Subsequent drawdown (%)")
        ax.set_title(f"Event Study: composite 30d pre-peak vs subsequent drawdown ({benchmark})")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHARTS / f"backtest_{benchmark}_{as_of}_event_study.png", dpi=150, bbox_inches="tight")
        plt.close()

    # Chart 4: precision/recall vs threshold
    if not sweep_df.empty:
        fig, ax1 = plt.subplots(figsize=(11, 5))
        ax2 = ax1.twinx()
        ax1.plot(sweep_df["threshold"], sweep_df["precision_pct"],
                 "o-", color="#264653", label="Precision")
        ax1.plot(sweep_df["threshold"], sweep_df["recall_pct"],
                 "s-", color="#e76f51", label="Recall")
        ax2.plot(sweep_df["threshold"], sweep_df["lift"],
                 "^--", color="#1f4e79", label="Lift (vs base rate)", alpha=0.6)
        ax1.axhline(sweep_df["base_rate_pct"].iloc[0], color="gray", ls=":", alpha=0.5,
                    label=f"Base rate {sweep_df['base_rate_pct'].iloc[0]:.0f}%")
        ax1.set_xlabel("Composite threshold T (sell signal: composite ≥ T)")
        ax1.set_ylabel("Precision / Recall (%)")
        ax2.set_ylabel("Lift (precision ÷ base rate)", color="#1f4e79")
        ax1.set_title(f"Sell-signal performance vs threshold ({benchmark})")
        ax1.legend(loc="upper left"); ax2.legend(loc="upper right")
        ax1.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(CHARTS / f"backtest_{benchmark}_{as_of}_threshold_sweep.png", dpi=150, bbox_inches="tight")
        plt.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--composite-history", required=True,
                        help="Path to a composite_history.csv from build_dashboard.py")
    parser.add_argument("--benchmark", default="SPY", help="Ticker to backtest against")
    parser.add_argument("--as-of", default=_dt.date.today().isoformat())
    parser.add_argument("--dd-threshold", type=float, default=-0.10,
                        help="Drawdown threshold for precision/recall (default -0.10 = -10%)")
    parser.add_argument("--horizon", type=int, default=90,
                        help="Days-forward horizon for precision/recall (default 90)")
    args = parser.parse_args()

    composite = pd.read_csv(args.composite_history, index_col=0, parse_dates=True)["composite"]
    composite = composite.sort_index()

    start = (composite.index[0] - pd.Timedelta(days=30)).strftime("%Y-%m-%d")
    end = (pd.Timestamp(args.as_of) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Fetching {args.benchmark} {start} → {end}...")
    prices = fetch_benchmark(args.benchmark, start, end)
    print(f"  {len(prices)} obs from {prices.index[0].date()} to {prices.index[-1].date()}")

    # 1) Conditional drawdown table
    print("\nComputing conditional drawdown probabilities...")
    cond_df = conditional_drawdown_table(composite, prices, horizons=[30, 60, 90, 180])
    cond_path = ONEOFF / f"backtest_{args.benchmark}_{args.as_of}_conditional.csv"
    cond_df.to_csv(cond_path, index=False)
    print(cond_df.to_string(index=False))

    # 2) Event study at major drawdowns
    print("\nFinding drawdown events (≥10% peak-to-trough)...")
    events_df = find_drawdown_events(prices, min_dd_pct=-0.10, min_separation_days=120)
    events_df = events_df.sort_values("drawdown_pct").head(15).reset_index(drop=True)
    print(f"  Top 15 drawdowns:")
    print(events_df[["peak_date","trough_date","drawdown_pct","days_peak_to_trough"]].to_string(index=False))

    print("\nEvent study at top drawdowns...")
    event_df = event_study(composite, events_df, lookback_days=[0, 30, 60, 90])
    event_path = ONEOFF / f"backtest_{args.benchmark}_{args.as_of}_event_study.csv"
    event_df.to_csv(event_path, index=False)
    print(event_df.to_string(index=False))

    # 3) Threshold sweep for precision/recall
    print(f"\nThreshold sweep (sell signal = composite ≥ T, dd_thr={args.dd_threshold*100:.0f}%, horizon={args.horizon}d)...")
    sweep_df = threshold_sweep(composite, prices, horizon=args.horizon, dd_thr_pct=args.dd_threshold)
    sweep_path = ONEOFF / f"backtest_{args.benchmark}_{args.as_of}_threshold_sweep.csv"
    sweep_df.to_csv(sweep_path, index=False)
    print(sweep_df.to_string(index=False))

    # 4) Charts
    print("\nGenerating charts...")
    make_charts(args.as_of, args.benchmark, composite, prices,
                cond_df, events_df, event_df, sweep_df)

    summary = {
        "benchmark": args.benchmark,
        "as_of": args.as_of,
        "composite_n_obs": int(composite.notna().sum()),
        "price_n_obs": int(len(prices)),
        "n_drawdown_events_ge_10pct": int(len(events_df)),
        "outputs": {
            "conditional_csv": str(cond_path),
            "event_study_csv": str(event_path),
            "threshold_sweep_csv": str(sweep_path),
        },
    }
    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
