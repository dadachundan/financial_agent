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

## When to use vs the siblings

- **`/zsxq-recommend`** (this) — reading-list triage from titles +
  summaries; no PDF is opened.
- **`/zsxq-ideas`** — "what should I buy" / "pitch me something" /
  "scan my feed for ideas" → an idea *shortlist*.
- **`/zsxq-expert`** — an in-depth question or comparison grounded in
  the PDFs ("what do my reports say about X").
- **`/zsxq-analyze`** — deep read of one named PDF (file_id / filename).

**Interpreter:** run all project scripts with `/opt/anaconda3/bin/python3`
(per `feedback_anaconda_python_db_scripts` — bare `python3` has failed
read-only DB opens and lacks deps like `yfinance` in some shells).

## Workflow

### 1. Parse the request

Pull out four optional knobs from the user's prompt:

- **Count** — "latest 50" (default), "latest 100", "last week", etc.
  Map to `--limit N` or `--since YYYY-MM-DD`.
- **Subject** — explicit topic ("semiconductors", "EVs", "中东"), or
  none. If none, **default focus = AI + robotics**.
- **Universe / listing constraint** — phrases like "US-traded only",
  "Chinese companies", "A/H shares", "exclude Japan", "only ADRs".
  Apply this after pulling rows by mapping broker-summary tickers to
  yfinance-style symbols (`META`, `BZ`, `600276.SS`, `002371.SZ`,
  `2269.HK`, etc.). Do not include Japan/Taiwan/Korea/Europe names when
  the user constrained the universe to US-traded or Chinese companies,
  even if those names dominate the recent feed.
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

**If the user asks for "undervalued", "high upside", "cheap", "mispriced",
"what do reports think is undervalued", or similar valuation-screen
language** — switch from reading-list mode to **valuation screen mode**:

- Scan **all** rows requested by the count/window, not just the first
  handful of visually obvious reports.
- Extract every explicit single-stock broker call that has rating and/or
  PT language, persist it through `scripts/persist_pts.py`, and use the
  returned `report_date_price` + `upside_pct` for the ranking.
- Respect any universe constraint strictly. For "US-traded or Chinese
  companies", include only bare US tickers/ADRs and China/HK/A-share
  tickers (`*.HK`, `*.SS`, `*.SZ`); exclude Tokyo/Japan names unless the
  user explicitly re-includes them.
- Do **not** arbitrarily stop at 5. Surface all clear high-upside names
  above the natural cutoff (usually `upside_pct >= 25%` for positive
  ratings), capped around 20-25 rows only to keep the answer readable.
  If there are more, say how many additional lower-conviction names were
  omitted and what cutoff was used.
- Always include `file_id`, company/ticker, broker, rating, PT, report-date
  price, implied upside, and a tight gist from the row's summary. When
  multiple brokers cover the same company in the scanned window, either
  show the strongest call and mention the confirming/conflicting file IDs,
  or show separate lines if the disagreement matters.

**Ranking rubric (after relevance filtering, all three modes).** Order
picks by: (1) bank-quality tier — GS / MS / JPM / UBS / Bernstein /
Nomura > other global > regional > unknown / `#代找`; (2) substance —
`page_count` 12–80 is the sweet spot; down-rank 1–3-page flash notes
unless the user asked for quick takes; (3) recency (`create_time`);
(4) `claude_rating` / `user_rating` when populated. A 4-page
regional-broker flyer must not outrank an 80-page GS deep-dive on
topical match alone. Name the tier in each "why read this" line.

### 3b. Persist your read/skip verdict as `claude_rating` (MANDATORY)

Every time this skill recommends (or triages away) a PDF, record your
verdict as a 1-5 star `claude_rating` on that `pdf_files` row so the
judgement is durable — it feeds the ranking rubric (step 3.4), shows in
the `/zsxq` viewer, and lets future runs skip re-triaging the same feed.
**Rate every row you actually evaluated in step 3, not just the picks.**

Convention (project-wide, set by the user):

| Stars | Meaning |
|---|---|
| **5** | must-read — top of the reading list |
| **4** | strong — worth reading |
| **3** | solid — worth reading if the topic is relevant |
| **2** | skippable — not worth reading |
| **1** | noise / off-topic / stale flash note — not worth reading |

So `3/4/5 = worth reading`, `1/2 = not worth reading`. Rate on
substance × relevance × bank tier (same signals as the step-3 rubric),
NOT on recency alone.

Write the ratings through the shared helper (this is the ONLY sanctioned
write path for `claude_rating` besides `zsxq_common.set_claude_rating` —
never raw SQL, per CLAUDE.md DB safety). Emit a JSON array of
`{file_id, rating}` on stdin:

```bash
python3 scripts/set_zsxq_ratings.py <<'JSON'
[
  {"file_id": 184418524511182, "rating": 5, "note": "GS 800G deep-dive, PT raise"},
  {"file_id": 184152128158222, "rating": 4, "note": "CR Land Buy, solid"},
  {"file_id": 212215818525881, "rating": 2, "note": "1-page macro flyer"}
]
JSON
```

The script prints `{considered, updated, missing, errored, rows}`.
Surface `updated` in the final reply's one-liners (step 6). A `missing`
row means the file_id wasn't in `pdf_files` — re-check the id.

### 4. Persist any PT calls into `stock_price_target.db` (free side-effect)

While reading the same summaries in step 3, the agent is already
inspecting the broker-call language. Whenever a row's summary contains
an explicit price-target call — patterns like `目标价 1300美元`,
`TP $450`, `12个月目标价116港元`, `target price ¥7100`,
`reiterate Buy/Outperform/Overweight/Neutral/Underweight/Sell` —
extract one record per (ticker × broker) pair into a JSON list and
pipe it to the **shared persistence helper** (this script is also
used by `/zsxq-analyze`):

```bash
python3 scripts/persist_pts.py <<'JSON'
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

**Full schema, rating/currency vocabulary, what to emit vs skip, and
idempotency rules are documented in
[`reference/pt_extraction.md`](../../../reference/pt_extraction.md) —
read it once if you're unsure what counts as a PT call.**

Recommend-specific notes (the bits that don't live in the shared doc):

- **No `--replace` flag here** — this skill works from the summary
  text, which is less reliable than the full-PDF deep read. If
  `/zsxq-analyze` later writes a higher-fidelity row for the same
  (ticker, broker, file_id), it should win. Default `INSERT OR IGNORE`
  means "first wins"; `/zsxq-analyze` passes `--replace` later to
  overwrite the summary-derived row.
- The script's stdout is a JSON summary `{considered, inserted,
  duplicate, skipped, errored, total_in_db, rows}` — surface `inserted`
  and `total_in_db` in the final reply, and use `rows` to honour the
  surfacing rule below.
- **Show the report-date price next to every PT you mention (mandatory).**
  A bare "GS Costco Buy, TP $1,159" is not actionable — the user needs
  the price the stock traded at *on the report's date* and the implied
  upside that price fixes. `persist_pts.py` returns these per row in its
  `rows` array (`report_date_price`, `price_currency`, `upside_pct`), so
  quote them: `GS Costco Buy, TP $1,159 vs $1,030 @ 2026-05-28 → +12.5%`.
  Never substitute today's spot for the report-date price; if
  `report_date_price` is null, write `report-date price n/a`. See
  [`reference/pt_extraction.md`](../../../reference/pt_extraction.md)
  § "Surfacing rule".
- **Revision arrows & disagreement flags — the summary-level case of the
  project's "Sell-side view evolution (卖方观点演变)" convention.** Before
  composing the reply, SELECT prior rows for each PT'd ticker — STRICTLY
  read-only: `sqlite3.connect('file:db/stock_price_target.db?mode=ro',
  uri=True)`, table `price_targets`. If the same institute already has a
  different PT on record for the name, annotate that PT line in step 6
  with a revision arrow — `PT ↑ from 120 (2026-04)`. If the scanned feed
  (or the live rows) carries contradictory calls on the same name —
  opposite ratings, PTs >20% apart — flag the disagreement explicitly in
  the read list (one line per side, each dated with its institute); never
  average them into a fake consensus.
- If the summary contains zero PT calls (pure macro, strategy notes,
  data dashboards), skip step 4 entirely — no harm, no pipe.

### 5. Show research-coverage gap

After step 4 finishes (even if it inserted nothing), run the
missing-coverage helper and append its markdown table to the reply.
This surfaces every PT-mentioned ticker that does **not** yet have a
`reports/company/<…>/` folder — sorted by market cap descending — so
the user can decide where to spend their next `/company-research` slot:

```bash
python3 scripts/missing_coverage.py --markdown --limit 25
```

Flags:

- `--limit N` — cap to top N by market cap (default 0 = no cap; the
  skill calls it with `--limit 25` to keep the chat tail readable).
- `--markdown` — emit a github-markdown table (drop the flag for the
  shell-friendly text table).
- `--regions US,HK,CN` — comma list of regions to include. Default is
  `US,HK,CN` which matches the user's typical
  next-research priority; widen to `US,HK,CN,TW,JP,KR,IN,EU` when the
  user explicitly says "all regions" / "include Japan" / etc.

The script's matching rule (so the model doesn't second-guess its
output): a ticker is considered **covered** if (a) any folder under
`reports/company/` ends with `<EXCH><CODE>` or `<EXCH>_<CODE>` for
the ticker's code (e.g. `Meituan_美团_HKEX3690` covers `3690.HK`),
OR (b) any folder starts with the ticker's `company_name` first
significant word (≥3 chars), followed by `_`/`-` — this catches
cross-listings (folder `BYD_SZSE002594` for the A-share counts as
coverage for a PT call on H-share `1211.HK`).

If the helper prints "✓ Every PT-mentioned ticker … already has a
report", just echo that line — no table to show.

### 6. Output format

For each recommendation give:

- `file_id` (so the user can hand it to `/zsxq-analyze`)
- Bank / publisher if known (`bank` column, or extract from name)
- **The report's own 概要 gist — NOT your one-line spin.** This is the
  load-bearing column and the one most often botched. The user is
  triaging blind: the *only* thing they see is your row, so it must
  state (a) **which company / subject** the report is about — named
  explicitly, in the gist itself, never left implied by the theme
  header — and (b) **the report's actual content**, lifted or tightly
  paraphrased from the `summary` (概要) text: the broker's thesis + the
  concrete numbers the summary contains (rating, PT, growth %, TAM,
  units, pricing). Reproduce the summary's substance; do not replace it
  with a generic gloss like "the flagship read" or "best framing of the
  cycle" — a label the user can't act on. If the summary names the
  company and gives numbers, your gist must too.
- Page count + create_time when useful for triage.

**Anti-pattern → fix (this is the exact failure this section exists to
prevent):**

- ❌ `Innolight (300308) — the single biggest markup in the feed.`
  (Reader has no idea what the report *says* — what business, what
  thesis, what numbers.)
- ✅ `中际旭创 Innolight (300308.SZ) — GS 维持"买入", 12M PT 上调至 ¥2,581
  (原 ¥1,187). 硅光在 800G/1.6T/3.2T 光模块渗透率 2026 达 60/80/100%;
  2026-28 净利润预测上调 65/108/119%, 营收 CAGR 64%. 从 scale-out 数据中心
  互联延伸到 scale-up 芯片级互联.` (Company, rating, PT + prior PT, the
  mechanism, the numbers — all from the 概要.)

Preserve the summary's original language in the gist (Chinese 概要 stay
Chinese; English broker prose stays English) — don't translate the
report's own numbers/terms into your own words if the 概要 already
states them cleanly.

Markdown table when listing >3 picks (columns: `file_id` · Bank · pg ·
Date · **概要 gist**). The gist column carries the weight — let it be
2–4 sentences even in a table; a one-clause gloss there is the bug.
Keep the surrounding prose tight — the user is choosing what to read
next, not consuming the reports here — but never compress the gist
itself down to a label.

For **valuation screen mode**, use a ticker-first table instead:
`file_id` · `Company / ticker` · `Broker call` · `PT vs report-date px`
· `Upside` · `概要 gist`. Sort by implied upside after applying the
user's universe constraint. If a report-date price lookup fails but the
summary itself states a current/reference price, label it explicitly as
`summary px`; otherwise write `report-date price n/a` and do not invent
the upside. If the user asks "which file id", every row must carry the
exact `file_id`; do not group file IDs only in prose.

End the reply with these compact one-liners (only when non-empty):

0. `⭐ claude_rating: <updated> rows rated (3-5 read / 1-2 skip)` —
   from step 3b's stdout `updated` count.
1. `📈 PT inserts: <inserted> new, <total_in_db> total in /pt` —
   from step 4's stdout summary. **When you list the actual PT calls
   (not just the count), one line per row using the step-4 `rows`
   data: `<broker> <ticker> <rating>, TP <ccy><pt> vs <ccy><report_date_price>
   @ <report_date> → <±upside_pct>%`** — the report-date price is
   mandatory (surfacing rule); `report-date price n/a` if it's null.
   Append the revision arrow when the step-4 read-only check found a
   prior same-institute PT (`PT ↑ from 120 (2026-04)`).
2. `🟡 <N> PT-mentioned tickers without a reports/company/ entry` —
   followed by the markdown table from step 5.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

AI / robotics is already this skill's default focus — so the bar is higher than a title gloss. Every surfaced AI / robotics / semiconductor pick gets **3–5 sentences of real narrative** drawn from the summary text: the broker's actual thesis (mechanism, not topic), the key numbers present in the summary (PT, TAM, pricing, units), where the name sits in the supply chain, and why the report matters *now* (cycle position, catalyst, estimate revision). Theme groupings of AI/robotics/semi reports get a short narrative paragraph per theme — what the cluster of brokers collectively believes and where they disagree — not just a list of titles.

## Notes

- `db/zsxq.db` is read-only here **except** for the agent-curated
  `claude_rating` column, which step 3b writes via
  `scripts/set_zsxq_ratings.py` → `zsxq_common.set_claude_rating()`.
  Never write any other column, and never write `claude_rating` with
  raw SQL — only through that helper.
- `scripts/list_recent.py` resolves the DB via `db_paths.db_path()`
  (honours `FINAGENT_DB_DIR`); any new script added under `scripts/`
  must copy that pattern in the same commit (CLAUDE.md DB-safety rule).
- Do **not** open the PDF files. Title + summary is the contract.
- If `count == 0` (empty filter result), tell the user the filter and
  suggest relaxing it (drop the subject, widen `--since`).
- The `tickers` / `claude_rating` / `user_rating` columns are sparse
  but valuable when present — mention them in the "why" line if a
  recommended row has them populated.
- This skill pairs with `zsxq-analyze`: recommend here → user picks a
  `file_id` → `/zsxq-analyze <question> file_id <N>` for the deep
  read.
