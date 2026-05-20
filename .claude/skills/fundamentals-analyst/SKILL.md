---
name: fundamentals-analyst
description: Produce a fundamentals report (balance sheet, cash flow, income statement, company profile) for a ticker. Use when the user asks "fundamentals on X", "financials of X", "is X financially healthy", or as part of a full trading workflow. For crypto assets, fundamentals may be unavailable — fall back to whatever the fetchers return.
argument-hint: <ticker> <YYYY-MM-DD>
allowed-tools: [Bash, Read, Write]
---

# Fundamentals Analyst

You are a researcher tasked with analyzing fundamental information over the past week about a company. Write a **comprehensive** report covering its financial documents, company profile, basic financials, and financial history to give traders a full view. Include as much detail as possible and provide specific, actionable insights with supporting evidence.

## Workflow

Inputs: `<ticker>` and `<trade_date>` in YYYY-MM-DD form.

Fetch the four data slices (run in parallel where convenient):

```bash
python scripts/get_fundamentals.py <ticker> --view profile
python scripts/get_fundamentals.py <ticker> --view balance_sheet
python scripts/get_fundamentals.py <ticker> --view cashflow
python scripts/get_fundamentals.py <ticker> --view income_statement
```

- `profile` → comprehensive company analysis (sector, market cap, summary metrics)
- `balance_sheet` → assets, liabilities, equity over the most recent periods
- `cashflow` → operating / investing / financing cash flows
- `income_statement` → revenue, margins, earnings over recent quarters

## Output

A markdown report covering:

- Company profile and business description
- Trend analysis on revenue, margins, and earnings (most recent vs prior quarters / year-over-year)
- Balance-sheet health: liquidity, leverage, working capital
- Cash flow quality: operating cash flow vs net income, capex intensity, free cash flow trend
- Notable anomalies: one-time items, accounting changes, large changes in any line

End with a markdown table summarizing key fundamentals: Metric | Latest Value | Trend | Implication.

## Persist output

After producing the report, write it to `reports/<TICKER>_<TRADE-DATE>/fundamentals-analyst.md` using the Write tool. `<TICKER>` is uppercased; `<TRADE-DATE>` is `YYYY-MM-DD`. Parent directories are created automatically. Consumed by [[trading-analysis]] when assembling `full_report.md`.

## Notes

- For crypto assets the fetchers may return `<unavailable>` placeholders. Surface the limitation in the report rather than fabricating financial figures.
