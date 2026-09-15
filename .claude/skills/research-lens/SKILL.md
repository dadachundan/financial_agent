---
name: research-lens
description: Given ONE ticker, build its full research lens end-to-end — scan every zsxq PDF about the name, triage the ones carrying a real call, persist their price targets into db/stock_price_target.db, read each of those PDFs in full and write a per-report digest (why Overweight/Underweight, insight density, data support, event context), score each report 0-10 for how much it is worth reading, write the digests into reference/report_digests.json so they light up on the /research-lens page, and hand back a ranked reading-list markdown in reports/recommend/. Trigger on "research lens on TICKER", "what do my reports say about TICKER", "build me a reading list for TICKER", "score the TICKER reports", or a bare ticker after this skill is named. Pairs with /zsxq-recommend (triage the feed by theme) and /zsxq-analyze (deep read of one file_id).
short_description: Rank every broker report on one ticker and score each 0-10 for how much it is worth reading.
short_description_zh: 汇总单个股票的全部券商报告，按值得阅读程度打 0-10 分。
version: 2026.09.15.1
---

# Research Lens — one ticker, every report, ranked

Given a ticker, this skill answers: **what does the whole zsxq library
say about this name, which of those reports is actually worth my
time, and why?**

It is the deep, single-name counterpart to `/zsxq-recommend`: instead
of triaging the recent feed by theme from titles + summaries, it takes
one ticker, finds *every* report that touches it across the whole
13.5k-PDF library, **opens the PDFs**, and produces (a) persisted price
targets, (b) per-report digests that render on the `/research-lens`
page, and (c) a scored reading list.

## When to use vs the siblings

- **`/research-lens`** (this) — one ticker, whole library, PDFs read,
  scored reading list + price targets + page digests.
- **`/zsxq-recommend`** — "what's worth reading this week"; the feed by
  theme, titles + summaries only, no PDF opened.
- **`/zsxq-analyze`** — deep read of **one** named `file_id`.
- **`/zsxq-company`** — the company's own filings/notes, not the
  third-party broker corpus.
- **`/zsxq-ideas`** — "pitch me something"; idea shortlist, not a
  single-name lens.

**Interpreter:** run every project script with `/opt/anaconda3/bin/python3`
(bare `python3` on this box is 3.9, fails on `int | None` annotations and
lacks `yfinance` — the `feedback_anaconda_python_db_scripts` rule).

## The two write paths (never raw SQL)

| What | Path |
|---|---|
| Price targets → `db/stock_price_target.db` | pipe a JSON array to `scripts/persist_pts.py` |
| Digests → `reference/report_digests.json` | edit the JSON file directly |

Rules for PTs live in **`reference/pt_extraction.md`** — read it before
emitting. It holds the rating vocabulary, what does / does not count as
a call, the currency rules, the record schema and the Surfacing rule.

## Workflow

### 1. Parse the ticker

Normalise to **yfinance form** — that is what `price_targets.company_ticker`
and every yfinance lookup use: `GEV`, `603308.SS`, `1211.HK`, `BZ`.
A-share codes get the exchange suffix (`603308.SS`, `002594.SZ`);
HK codes are zero-padded to 4 (`0700.HK`). If the user gives a company
name, resolve it to the ticker first. Confirm the company name too —
you will need it for the deliverable title and to sharpen the search.

### 2. Scan — gather everything about the name

```bash
/opt/anaconda3/bin/python3 .claude/skills/research-lens/scripts/lens_scan.py GEV
# richer summaries, wider net:
/opt/anaconda3/bin/python3 .claude/skills/research-lens/scripts/lens_scan.py GEV \
    --name "GE Vernova" --limit 120 --summary-chars 1500
```

Returns one JSON blob with four blocks:

- **`candidates`** — BM25-ranked FTS5 (trigram) hits over `pdf_files`,
  each with `file_id, name, topic_title, summary, bank, create_time,
  page_count, tickers, local_path, has_pdf, has_pt_row, has_digest,
  digest_score`. The set always **includes every PDF that already has a
  PT row** for the ticker, even if its text ranks below the cutoff.
- **`price_targets`** — existing rows for the ticker: broker, rating,
  PT, currency, `report_date`, `report_date_price`, `upside_pct`. This
  is the read-only pre-pass: it tells you which reports are known calls
  and lets you spot same-institute revisions and cross-broker
  dispersion before reading anything.
- **`digests`** — the registry entries already covering these
  candidates, keyed by stringified `file_id`.
- **`counts`** — `candidates / with_pt_row / already_digested /
  missing_digest / pt_rows`.

Pass `--name` for the English/Chinese company name when the ticker is
short or ambiguous (`BZ` → Kanzhun); it is auto-filled from the PT rows
when they exist. **Re-running is cheap and safe** — `already_digested`
tells you exactly which PDFs you can skip.

### 3. Triage to real calls

Not every FTS hit is research on the name. Keep a candidate only if it
carries **a rating or a price target on this ticker** (per
`reference/pt_extraction.md`). Drop:

- comp-table rows and "top picks" list members with no per-ticker call,
- read-across notes about a *different* company that happens to cite
  this one (`Read~through from GEV` notes are about Yingliu, not GEV),
- bare narrative mentions ("as DELL showed last week").

`has_pt_row` is a strong prior, but triage from the summary yourself —
a real call with no DB row yet is exactly what this run should add.
State plainly how many candidates you dropped and why; the split
between *argues a case* and *is a table row* is itself a finding
(GEV: 15 calls, but only 6 actually argued a case).

### 4. Persist the price targets

Read `reference/pt_extraction.md`, then emit **one record per ticker ×
broker**, including rows for reports you are only now discovering:

```bash
/opt/anaconda3/bin/python3 scripts/persist_pts.py <<'JSON'
[
  {"ticker": "GEV", "company_name": "GE Vernova", "broker": "J.P. Morgan",
   "rating": "Overweight", "pt": 1330, "ccy": "USD",
   "catalyst": "Gas backlog + SRA bridge into FY28", "file_id": 584285418514214}
]
JSON
```

The script fills `report_date`, `report_date_price`, market cap,
`price_currency` and `upside_pct` from `pdf_files` + yfinance and echoes
them back per row in its stdout `rows` array. Use `--replace` here — a
full-PDF read outranks any earlier summary-only extraction. Idempotency
keys are `(ticker, broker, file_id)` and `(ticker, broker, report_date)`,
so re-running is a no-op; note that the second key means only one report
per broker per day survives (GEV lost its better 61-pp JPM note to a
same-day sibling this way — mention such losses in the deliverable).

**Surfacing rule (mandatory):** never print a bare PT. Always
`TP $1,330 vs $900.28 @ 2026-07-29 → +47.7%`, using the script's own
`report_date_price` / `upside_pct`. If the price is null, say
`report-date price n/a` rather than showing a blank or today's spot.

### 5. Read every real-call PDF in full

Extract text with `fitz` (PyMuPDF, available under the Anaconda
interpreter; there is no `pdftotext`). Files live at `local_path`
(under `/Users/x/Downloads/zsxq_reports/<YYYY_MM_DD>/`).

For more than ~4 PDFs, **fan out to parallel background subagents** —
this is the fastest path and they share the workspace. Give each one:

- the exact `local_path` list (3–4 PDFs each, keep batches small),
- the fixed digest template below,
- **a hard ≤180–250-word budget per report** — long replies get
  truncated in transit and you will have to re-request them.

```
Caller agent: <your agent id>
Read these PDFs in full: <paths>
For EACH, return exactly this, 180-250 words total:
Report / ticker call — broker, date, pages, rating + PT (and prior PT).
Why bullish-bearish — the mechanism, with the report's own numbers.
Insight quality — proprietary data or restated consensus?
Data support — exhibits, models, SOTP builds, management quotes.
Event context — was it written around a print / deal / regulatory trigger?
Read score N/10 + one line on why.
```

For 1–4 PDFs just read them yourself in-context (fitz → text).

### 6. Score each report 0–10

| Score | Meaning |
|---|---|
| **8–10** | Primary work on the name: proprietary data or a quantified argument about the ticker itself. Read it. |
| **6–7** | Real content on the name inside a report about something else, or a short but genuinely fresh read. Worth the time. |
| **4–5** | A few sharp datapoints — a backlog number, a capacity figure — but the ticker is a comp row. Skim that section only. |
| **0–3** | The name is a table row or a line on a chart. The report may be excellent; it is not research on this ticker. |

Weight four things: **(1)** is there a thesis at all — rating + why, or
just a row in a valuation table; **(2)** insight density — proprietary /
channel data vs restated consensus; **(3)** data support — exhibits,
models, SOTP builds, verbatim management quotes; **(4)** event context —
written around a print, deal or regulatory trigger (a dated, testable
call) or in a quiet patch. Length alone does not earn a score: a 75-pp
conviction list where the name is absent scores 3; a 9-pp read-across
built on the company's fresh numbers scores 8.

### 7. Write the digests into `reference/report_digests.json`

Keyed by **stringified** `file_id`; one object per report, exactly these
keys, plus the shared `_comment`:

```json
{
  "_comment": "Per-report digests for the /research-lens page, keyed by zsxq file_id. Written by the research-lens skill.",
  "584281422521424": {
    "score": 8,
    "why": "Overweight, PT $1,302. Why the report is bullish/bearish on the ticker — the mechanism, with its own numbers.",
    "insight": "Proprietary pricing/backlog data vs restated consensus.",
    "data": "Exhibits, models, SOTP builds, management quotes.",
    "event": "Written the day after the 2Q26 print — a dated, testable call."
  }
}
```

**Merge, never clobber** — load the file, update only your file_ids,
write it back preserving every other key (`_comment` included). Read
the four fields as: *`why`* = the stance and the argument, *`insight`* =
whether the information is new, *`data`* = the evidence behind it,
*`event`* = the news/print/deal context that makes it timely.

### 8. Write the reading-list deliverable

`reports/recommend/<Company>_<TICKER>_Research_Lens_<YYYY-MM-DD>.md`,
ordered by score descending:

1. **Header** — generated date, ticker + company, the `/research-lens`
   link, the source DBs, and the **scan method**: the search terms used,
   candidates found, how many carried a real call, how many were read in
   full, and the split between reports that *argue a case* and those
   that merely *cite the name*.
2. **How to read the score** — the table from step 6.
3. **Ranked table** — `Score | Report | Pp · Date | stance & PT |
   price on date → upside | Open`. Link each row to
   `http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded name>`.
4. **Per-report detail** — for each: **Why bullish/bearish**,
   **Insight density**, **Data support**, **Event context** — the same
   four axes as the digest, expanded.
5. **Disagreement flags** — anywhere brokers split (opposite ratings, or
   PTs >20% apart), one line per side, each dated, never averaged into a
   fake consensus.
6. **How the data is stored** — which DB/table/file each number came
   from (see below).

Surface PT counts and the report-date prices in the final reply, e.g.
`📈 PT inserts: 12 new, 15 total for GEV in /pt`.

### 9. Verify before claiming anything

- **Links** — every download URL must return HTTP 200 /
  `application/pdf`: `curl -sI -o /dev/null -w '%{http_code} %{content_type}\n' <url>`.
- **DB** — re-run `lens_scan.py <ticker>` and confirm `counts.pt_rows`
  and the rows themselves match what you reported.
- **JSON** — `json.load` the digest file; confirm your file_ids are
  present and no pre-existing key was dropped.
- **Page** — to check the rendering, start a **private** instance and
  leave the user's alone:
  `/opt/anaconda3/bin/python3 main.py --port 5077`, then open
  `http://localhost:5077/zsxq/research-lens?ticker=GEV`. Kill only that
  process.
- **Commit** the skill + script + digests + deliverable
  (Conventional Commit, no `Co-authored-by`), then `git status`.

## Installation — two copies, and why

This skill exists twice:

| Copy | Role |
|---|---|
| `.claude/skills/research-lens/` (**canonical**, in the repo) | versioned here; holds the runnable `scripts/lens_scan.py` |
| `<app_data_dir>/agents/<agent_id>/agent_state/skills/research-lens/` | what PenguinHarness lists — the `/` skill picker and the injected `{{SKILL_METADATA}}` |

**The second must be a real directory, not a symlink.** PenguinHarness's
`listInstalledSkills` scans with `fs.readdir(..., {withFileTypes:true})`
and keeps only entries where `entry.isDirectory()` is true — and a
symlink to a directory reports `false` (it is a link, not a dir). A
symlinked skill is therefore listed nowhere and silently invisible to
the picker. After editing the repo copy, re-sync:

```bash
DST=<app_data_dir>/agents/<agent_id>/agent_state/skills/research-lens
cp .claude/skills/research-lens/SKILL.md \
   .claude/skills/research-lens/icon.svg "$DST/"
cp .claude/skills/research-lens/scripts/lens_scan.py "$DST/scripts/"
```

`lens_scan.py` resolves the project root from its own location *and* from
the working directory, so both copies run as long as you are inside the
repo. **The skill list is injected when a conversation starts** — a newly
added or renamed skill appears in the picker at once, but the running
conversation's prompt keeps its old list until you start a new one.

## Operational notes

- **The user's server runs on port 5001** (`python main.py`) — never
  kill it, never take that port. It runs with `debug=False`, so
  **templates and Python are cached: the user must restart 5001** to see
  digest or page changes. Always say so; you cannot do it for them.
- The `/research-lens` page shows at most the **18 most recent** reports
  with a PT row. A ticker with more than 18 calls will hold digests that
  never render — say which ones are off-page rather than silently
  writing them.
- `db/zsxq.db` read-only opens work via `?immutable=1` (plain
  `sqlite3.connect()` also works); `?mode=ro` has failed on it under WAL.
- Playwright is not importable as a module; if you need a browser check
  use `NODE_PATH=/Users/x/.npm/_npx/e41f203b7505f1fb/node_modules node
  script.cjs`.
- Never write `price_targets` (or any `pdf_files` column) with raw SQL —
  PTs go through `scripts/persist_pts.py`, the star rating through
  `scripts/set_zsxq_ratings.py`.

## How the data is stored

| Artifact | Location |
|---|---|
| The PDFs + their metadata | `db/zsxq.db` → `pdf_files` (13.5k rows; `file_id` PK, `name`, `topic_title`, `summary`, `local_path`, `bank`, `page_count`, `tickers`, `claude_rating`, `ocr_text`), plus the FTS5 trigram index `pdf_files_fts` |
| Price targets | `db/stock_price_target.db` → `price_targets` (one row per ticker × broker × report; `company_ticker`, `research_institute`, `rating`, `price_target`, `target_currency`, `report_file_id`, `report_date`, **`report_date_price`** — the frozen point-in-time close — `upside_pct`) |
| Per-report digests | `reference/report_digests.json`, keyed by stringified `file_id`; loaded by `zsxq_viewer._report_digests()` (mtime-cached) and attached to each report in `_research_lens_reports()` |
| The lens page | route `/zsxq/research-lens` in `zsxq_viewer.py`, template `templates/research_lens.html`; daily OHLC is **not** stored, it is pulled live from yfinance per page load |

`db/zsxq.db`, `db/notes.db` and `db/alert_monitor.db` are tracked by
git; `db/stock_price_target.db` matches `.gitignore`'s `*.db` and is
**not** committed — so PT writes never appear in a diff. Mention that
when reporting, or the user will think the step was skipped.
