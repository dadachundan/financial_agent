# Trading-pipeline output path resolution

All time-variant trading-pipeline skills (sentiment-analyst, news-analyst, bull-bear-debate, research-manager, trader-plan, risk-debate, portfolio-decision, trading-analysis) write their output under the **existing company-research folder** for the ticker, namespaced by trade date:

```
reports/company/<COMPANY_FOLDER>/trading/<TRADE-DATE>/<skill-name>.md
```

This keeps every artifact for a ticker — the time-invariant deep-dive *and* every trade-date run — co-located under one folder.

## Resolving `<COMPANY_FOLDER>`

Company-research folders follow the convention `<Name>_<EXCHANGE><TICKER>` (e.g. `AMD_NASDAQ_AMD`, `Tesla_NASDAQ_TSLA`, `Anpeilong_SZSE002050`, `安培龙_SZSE002050`). To resolve:

1. **Glob `reports/company/` for any sub-folder whose name ends in `_<TICKER-NO-PUNCT>`** — i.e. strip the exchange-prefix colon, then match the trailing token:
   - Ticker `AMD` → match `*_AMD` → `AMD_NASDAQ_AMD/`
   - Ticker `NVDA` → match `*_NVDA` → `Nvidia_NASDAQ_NVDA/`
   - Ticker `SZSE:002050` → strip colon → `SZSE002050` → match `*_SZSE002050` → `Anpeilong_SZSE002050/` *or* `安培龙_SZSE002050/`
2. **If multiple matches**, pick the most-recently-modified folder.
3. **Fallback (no match exists)**: write to `reports/company/<TICKER-NO-PUNCT>/trading/<TRADE-DATE>/<skill-name>.md` — parent directories auto-create. The next [[company-research]] run for this ticker can either adopt the same folder or co-exist alongside.

Concretely, in a Bash one-liner the discovery is:

```bash
COMPANY_FOLDER=$(ls -dt reports/company/*_${TICKER//:/}/ 2>/dev/null | head -1)
COMPANY_FOLDER=${COMPANY_FOLDER:-reports/company/${TICKER//:/}/}
OUTPUT_DIR="${COMPANY_FOLDER%/}/trading/${TRADE_DATE}"
mkdir -p "$OUTPUT_DIR"
```

The `Write` tool creates parent directories automatically, so an explicit `mkdir -p` is unnecessary when calling Write — but you must know the full target path.

## Why this layout

- **Co-location**: a researcher opening `reports/company/AMD_NASDAQ_AMD/` sees the deep-dive, the valuation model, the charts, *and* every dated trading run in one place.
- **Trade-date as a dimension, not a sibling**: re-running the pipeline on a new date produces a new `trading/<DATE>/` sibling without polluting the company-research namespace.
- **Backwards-compatible discovery**: works for tickers with an existing company-research folder *and* for tickers whose first artifact is a sentiment/news run (the fallback path creates a stub that a later company-research call can adopt).

## Anti-patterns

- **Do not** write to `reports/<TICKER>_<TRADE-DATE>/` — that was the legacy convention and it fragments ticker artifacts across the `reports/` root.
- **Do not** put the trade date in the company folder name (e.g. `reports/company/AMD_NASDAQ_AMD_2026-05-23/`) — the trade date is a dimension, not part of the company identity.
- **Do not** invent a parallel folder when an existing `<Name>_<EXCHANGE><TICKER>` folder already exists for the ticker — always discover and reuse.
