# PT Extraction — Shared Reference

`/zsxq-recommend` (light: summary-only), `/zsxq-analyze` (deep:
full PDF text + optional OCR + page rendering), and `/zsxq-ideas`
(orchestrated extraction agents, aggregated once per run) extract
sell-side price-target calls and persist them into
`db/stock_price_target.db` (surfaced via the `/pt` web viewer). This
document is the **one shared rule book** every persisting skill follows
so the rows have identical shape and quality regardless of which path
produced them. The same table is also the **read-only pre-pass** behind
the project-wide "Sell-side view evolution (卖方观点演变)" convention:
any zsxq-using skill SELECTs prior rows per ticker (columns
`research_institute`, `rating`, `price_target`, `report_date`,
`report_file_id`) to detect same-institute revisions and cross-institute
PT dispersion before re-reading PDFs — writes remain exclusively via
`scripts/persist_pts.py`.

The downstream pipe is the same: a JSON array piped to
[`scripts/persist_pts.py`](../scripts/persist_pts.py), which fills in
market data via yfinance and upserts via
[`stock_price_target_db.upsert_target()`](../stock_price_target_db.py).

## What counts as a PT call (do emit)

A row is emitted when **all three** of the following hold:

1. **A specific broker** publishes the report — i.e. the zsxq row's
   `bank` column is populated, OR the broker name is unambiguous from
   the report's own title (`Bernstein——…`, `大摩——…`). Rows tagged
   `#代找` where `bank` is null are **not** broker calls.
2. **A specific ticker** is being rated — there is an explicit
   company name + (ideally) a parenthesised ticker:
   `礼来（LLY）`, `(3690.HK)`, `(300750.SZ / 3750.HK)`, `Tesla (TSLA)`.
3. **At least a rating OR a numeric PT** is attached to that ticker.

## What does NOT count (skip)

- Generic theme commentary: "we like the AI capex theme" — no ticker.
- Industry takeaways with no broker call: "China consumer is fragile".
- Bare ticker mentions inside narrative: "as DELL showed last week" —
  no rating, no PT.
- "Top picks include …" lists where the list is presented as a
  *cluster* without a per-ticker rating or PT (these are too imprecise
  to attribute to a clean call).
- Index-level targets ("S&P 500 8,000") — these are macro views, not
  single-stock PT calls. (If you want them, emit with `^GSPC` etc. —
  the schema accepts it, but skip by default.)

## Vocabulary the model should recognise

### Rating words

| Bucket | Chinese | English |
|---|---|---|
| Positive | `买入`, `跑赢大盘`, `增持`, `超配`, `首选 / 首推`, `推荐` | `Buy`, `Outperform`, `Overweight`, `Top Pick` |
| Neutral | `中性`, `持平`, `同步大盘`, `符合大盘`, `市场表现` | `Neutral`, `Market-Perform`, `Equal-Weight`, `Hold` |
| Negative | `减持`, `跑输大盘`, `卖出` | `Underweight`, `Underperform`, `Sell`, `Reduce` |

Preserve the exact phrasing the report used (`Outperform` not
`Buy` if Bernstein says `Outperform`). The DB column is free text;
the `/pt` page colour-pills by lowercased substring match.

### PT markers

`目标价`, `12个月目标价`, `TP`, `target price`, `target`, `price
target`, sometimes just an inline number right after the ticker like
`LLY $1,300`. When a report gives a `从 X 上调至 Y` / `raised from X
to Y` form, take **Y** (the new PT).

### Currency

Always tag the PT with its currency. Detect from:

1. Explicit unit attached to the number: `美元`, `$`, `USD`,
   `港元`, `HK$`, `HKD`, `元人民币`, `元 (人民币)`, `CNY`, `新台币`,
   `TWD`, `日元`, `JPY`, `韩元`, `KRW`.
2. If no unit is shown next to the number, infer from the ticker's
   listing exchange:
   - `*.HK` / `HKEX:` → `HKD`
   - `*.SS` / `*.SZ` / `SSE:` / `SZSE:` → `CNY`
   - `*.TW` / `*.TWO` → `TWD`
   - `*.T` / `*.JP` → `JPY`
   - `*.KS` → `KRW`
   - bare US ticker → `USD`
3. If neither is determinable, leave `ccy` null and ship the row
   without `pt` (don't guess).

## Record schema

```json
{
  "ticker":       "1109.HK",        // yfinance form; REQUIRED
  "company_name": "China Resources Land",   // English / Pinyin; REQUIRED
  "broker":       "Goldman Sachs",  // REQUIRED — full broker name, not abbreviated
  "rating":       "Buy",            // optional
  "pt":           36.6,             // optional (number, not string)
  "ccy":          "HKD",            // required if `pt` is set
  "catalyst":     "Tier-1 housing recovery; mall ops alpha",  // 1-line; optional
  "file_id":      184152128158222   // zsxq.db pdf_files.file_id; REQUIRED
}
```

A single report often covers many tickers (sector notes, conviction
lists). Emit **one record per ticker × broker pair**; share the same
`file_id` and `catalyst` across them.

## Idempotency / dedup

`upsert_target()` enforces two uniqueness keys:

- `UNIQUE(company_ticker, research_institute, report_file_id)` —
  re-running on the same window is a no-op.
- `UNIQUE(company_ticker, research_institute, report_date)` — if the
  same broker covers the same ticker in two PDFs on the same day
  (e.g. an ASCO mega-note + a single-name follow-up), only the first
  record survives.

By default the script uses `INSERT OR IGNORE` so the first row wins.
The `/zsxq-analyze` skill should pass `--replace` to `persist_pts.py`
so its higher-fidelity full-PDF extraction overwrites a prior
summary-only row.

## Auto-filled fields (don't put in the JSON)

`persist_pts.py` fills these from `zsxq.db` + yfinance, then writes
them to the DB:

- `report_date` — parsed from PDF filename suffix `-260602.pdf` →
  `2026-06-02`. Falls back to `create_time` on the row.
- `report_pdf_filename` — the PDF's original name from `pdf_files`.
- `report_url` — `http://xs-macbook-air.local:5001/zsxq/pdf-viewer/<file_id>`.
- `report_date_price` — adjusted close on report_date.
- `report_date_market_cap` — close × shares outstanding.
- `price_currency` — listing currency from yfinance.
- `upside_pct` — `(pt − close) / close × 100`.
- `created_at` — ISO timestamp.

## Surfacing rule (mandatory) — a PT is useless without the price on the report's date

Whenever either skill **mentions** a PT back to the user — the final-reply
one-liners, a recommendation's "why read this", a deep-read answer, any
table — it MUST carry the **stock's price as of the report's publication
date** and the **implied upside that price fixes**. Never print the bare
target. `GS Costco Buy, TP $1,159` is not actionable; the reader needs
`GS Costco Buy, TP $1,159 vs $1,030 @ 2026-05-28 → +12.5%`.

You do not have to recompute any of this — `persist_pts.py` already looks
up the report-date close via yfinance, stores it, and **echoes it back per
row** in its stdout `rows` array (`report_date_price`, `price_currency`,
`upside_pct`) — the same numbers shown in `/pt` as **"Px @ Report"** /
**"Upside %"**. Read them straight out of the script's output and surface
them next to every PT you mention.

- **The report-date price is the load-bearing number**, not today's spot.
  It is what the analyst was looking at and what makes the call's upside
  reconstructable. Do NOT silently substitute the current price for it.
- **If you also show today's spot** (handy to convey how much of the move
  already happened), label both: `TP $1,159 vs $1,030 @ 2026-05-28
  (+12.5%); now $1,090`.
- **If `report_date_price` is null** (yfinance had no close — delisted,
  pre-IPO, wrong ticker), say `report-date price n/a` — never present a
  PT with a blank or stale price as if it were the report-date price.

## Invocation cheatsheet

```bash
# From /zsxq-recommend (summary-only extraction, first-wins)
python3 scripts/persist_pts.py <<'JSON'
[ ... ]
JSON

# From /zsxq-analyze (full-PDF extraction, overwrites prior rows)
python3 scripts/persist_pts.py --replace <<'JSON'
[ ... ]
JSON

# Check what's still missing a research folder, top 25 by mkt cap
python3 scripts/missing_coverage.py --markdown --limit 25
```

Stdout from `persist_pts.py` is a JSON summary:

```json
{
  "considered":  12,
  "inserted":    8,
  "duplicate":   4,
  "skipped":     0,
  "errored":     0,
  "total_in_db": 145,
  "rows": [
    {"ticker": "COST", "broker": "Goldman Sachs", "rating": "Buy",
     "pt": 1159, "ccy": "USD", "report_date": "2026-05-28",
     "report_date_price": 1030.4, "price_currency": "USD",
     "upside_pct": 12.5}
  ]
}
```

Surface `inserted` and `total_in_db` in the final user-facing reply
so the side-effect is visible:

```
📈 PT inserts: 8 new, 145 total in /pt
```

And use the `rows` array to obey the **Surfacing rule** above — every PT
you echo back carries its report-date price + upside straight from there:

```
📈 GS Costco Buy, TP $1,159 vs $1,030 @ 2026-05-28 → +12.5%
```
