---
name: zsxq-recommend
description: Recommend zsxq reports to read by scanning the most-recent rows of db/zsxq.db (titles + summaries — no PDF parsing). Default: latest 50 reports, focus on AI / robotics. User may override with a count ("latest 100") and/or a subject ("focus on semiconductors", "anything on EVs"). When the user has no clue, group the recent feed into themes and surface a handful of standout reads. **Also persists any sell-side price-target (PT) calls found in the same summaries into `db/stock_price_target.db`** (idempotent via UNIQUE(ticker, broker, file_id)), surfaced in the `/pt` viewer. Pair: hand a returned `file_id` to `/zsxq-analyze` for a deep read.
---

# Recommend zsxq PDF

The user wants a curated pointer into the recent zsxq report feed —
**not** a deep read of any single PDF. Work only from
`db/zsxq.db.pdf_files`'s metadata columns (title, summary, tags, etc.).
Do not extract or open PDFs. (If they want a deep dive on a specific
report, the `zsxq-analyze` skill handles that.)

## Workflow

### 1. Parse the request

Pull out three optional knobs from the user's prompt:

- **Count** — "latest 50" (default), "latest 100", "last week", etc.
  Map to `--limit N` or `--since YYYY-MM-DD`.
- **Subject** — explicit topic ("semiconductors", "EVs", "中东"), or
  none. If none, **default focus = AI + robotics**.
- **Vibe** — does the user know what they want, or are they fishing?
  Wording like "summarize for me", "anything interesting", "what
  should I read" → fishing mode (theme-cluster + 3-5 picks).

### 2. Pull recent rows

```bash
# Latest 50 (default)
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py

# Latest 100
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py --limit 100

# Coarse subject filter before Claude ranks (only when the user named one)
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py \
    --limit 100 --subject "semiconductor"

# Recency window
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py \
    --since 2026-05-01
```

Flags:

- `--limit N` (default 50)
- `--subject TEXT` — case-insensitive LIKE on
  name/topic_title/summary/tags/comment. **Only pass this when the
  user gave an explicit subject.** Default AI/robotics focus is done
  by Claude in step 3, not by SQL — the boolean `ai_robotics_related`
  / `ai_related` / `robotics_related` columns are sparsely populated,
  so don't rely on them as a hard filter.
- `--since YYYY-MM-DD` — only rows newer than this.
- `--summary-chars N` — truncate each summary (default 1500). Bump to
  0 if the user wants very detailed picks, drop to ~500 for 100+ rows.

Output: JSON `{count, generated_at, filters, rows:[…]}`. Each row has
`file_id, name, topic_title, summary, create_time, page_count, tickers,
tags, comment, bank, ai_robotics_related, ai_related, robotics_related,
semiconductor_related, energy_related, claude_rating, user_rating`.

### 3. Rank and recommend (Claude does this in-context)

Read every row's `topic_title` + `summary`. Then:

**If the user named a subject** — pick the 5-10 most relevant reports
and explain *why* each one fits. Ignore the rest. If only 1-2 truly
match, say so honestly rather than padding.

**If no subject (default = AI/robotics)** — score each row on
AI / robotics / adjacent (semis, infra, data, autonomy). Surface 5-10
top picks across these subthemes. Down-weight pure macro / general
strategy unless tightly AI-linked.

**If the user is fishing** ("summarize for me", "what's interesting") —
first cluster the recent feed into 3-6 themes ("AI capex /
inference economics", "robotics + autonomy", "energy & power",
"China consumer slowdown", "geopolitics", …) with a one-line gist
each. Then pick 2-3 standout reads under each theme.

### 4. Persist any PT calls into `stock_price_target.db` (free side-effect)

While reading the same summaries in step 3, the agent is already
inspecting the broker-call language. Whenever a row's summary contains
an explicit price-target call — patterns like `目标价 1300美元`,
`TP $450`, `12个月目标价116港元`, `target price ¥7100`,
`reiterate Buy/Outperform/Overweight/Neutral/Underweight/Sell` —
extract one record per (ticker × broker) pair into a JSON list and
pipe it to the persistence helper:

```bash
python3 .claude/skills/zsxq-recommend/scripts/persist_pts.py <<'JSON'
[
  {"ticker":"1109.HK","company_name":"China Resources Land",
   "broker":"Goldman Sachs","rating":"Buy","pt":36.6,"ccy":"HKD",
   "catalyst":"Tier-1 housing recovery; mall ops alpha",
   "file_id":184152128158222},
  {"ticker":"LLY","company_name":"Eli Lilly",
   "broker":"Bernstein","rating":"Outperform","pt":1300,"ccy":"USD",
   "catalyst":"LIBRETTO-432 Selpercatinib RET+ HR=0.17",
   "file_id":184152151455852}
]
JSON
```

Record schema (per row in the array):

| field          | required | meaning                                            |
|----------------|----------|----------------------------------------------------|
| `ticker`       | yes      | yfinance form: `LLY`, `1109.HK`, `300750.SZ`, etc. |
| `company_name` | yes      | English / Pinyin                                   |
| `broker`       | yes      | `Goldman Sachs` / `Morgan Stanley` / `Bernstein` … |
| `rating`       | no       | `Buy` / `Outperform` / `Neutral` / `Underweight` / `Sell` / `Top Pick` |
| `pt`           | no       | numeric price target in `ccy`                      |
| `ccy`          | no       | `USD` / `HKD` / `CNY` / `TWD` / `JPY` / `KRW` (required if `pt` is given) |
| `catalyst`     | no       | one-line catalyst paraphrased from the summary     |
| `file_id`      | yes      | zsxq.db `pdf_files.file_id` (links the call back to the source PDF) |

Behaviour:

- The script idempotents on `(ticker, broker, file_id)` — re-running on
  the same window is a no-op via the table's `UNIQUE` constraint.
- It auto-fills `report_date` from the PDF filename (`-260602.pdf` →
  `2026-06-02`), then fetches close + market cap on that date via
  yfinance, and computes `upside_pct`.
- Stdout is a JSON summary: `{considered, inserted, duplicate, skipped,
  errored, total_in_db}`. Surface the `inserted` and `total_in_db`
  numbers in the final user-facing reply.
- **Only emit records where a specific broker is calling on a specific
  ticker with at least a rating OR a PT.** Skip generic macro mentions
  ("we like the AI infra theme") and non-broker reports (`#代找` rows
  where `bank` is null).
- A single report often covers many tickers (sector notes / conviction
  lists). Emit one record *per ticker*; share the same `file_id` and
  `catalyst` across them.

If the summary doesn't contain any PT calls (e.g. pure macro or strategy
piece), skip step 4 entirely — no harm, no pipe.

### 5. Output format

## Notes

- DB is read-only here. Never write to `db/zsxq.db` from this skill.
- Do **not** open the PDF files. Title + summary is the contract.
- If `count == 0` (empty filter result), tell the user the filter and
  suggest relaxing it (drop the subject, widen `--since`).
- The `tickers` / `claude_rating` / `user_rating` columns are sparse
  but valuable when present — mention them in the "why" line if a
  recommended row has them populated.
- This skill pairs with `zsxq-analyze`: recommend here → user picks a
  `file_id` → `/zsxq-analyze <question> file_id <N>` for the deep
  read.
