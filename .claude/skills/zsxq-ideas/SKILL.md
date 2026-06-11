---
name: zsxq-ideas
description: Generate investment ideas from the zsxq report library (db/zsxq.db) by combining zsxq-recommend (theme/PDF surfacing) + zsxq-analyze (parallel per-PDF deep reads) + idea-generation (Step-4 presentation). Supports three modes — **themed** ("ideas on AI infra from zsxq", "long humanoid plays from my reports"), **fishing** ("what should I buy", "scan my zsxq feed", "any ideas", "pitch me something from zsxq"), and **theme-build** ("build themes from my zsxq feed", "turn my feed into tracked baskets", "build a theme on X from zsxq") which clusters the feed and seeds/refreshes durable `theme-research` baskets from the actual broker content. Use whenever the user wants stock ideas or tracked thematic baskets sourced from their zsxq library rather than generic quantitative screens. Triggers: "ideas from zsxq", "zsxq ideas", "what stocks does my zsxq feed suggest", "scan zsxq for ideas", "build themes from zsxq", "turn my zsxq feed into baskets", "/zsxq-ideas".
---

# Generate Investment Ideas from the zsxq Library

This skill is the orchestrator that turns the zsxq feed into actionable
shortlists. Pipeline:

```
db/zsxq.db (metadata)  ──▶  cluster / theme-rank  ──▶  parallel /zsxq-analyze
                                                              │
                                                              ▼
                                       per-PDF JSON (tickers + thesis + risks)
                                                              │
                                                              ▼
                              aggregate by ticker  ──▶  idea-generation Step 4
                                                              │
                                                              ▼
                                      reports/ideas/zsxq_<slug>_<date>.md
```

You — Claude — do the orchestration and the in-context analysis. The two
helper skills (`zsxq-recommend`, `zsxq-analyze`) do the metadata pull and
the per-PDF extraction; their existing scripts are the only data layer.

## Mode detection (always the first step)

Parse the user's prompt:

- **Themed** — the user named a theme / sector / style / direction.
  Examples: "AI infra ideas from zsxq", "humanoid longs", "China semis",
  "GLP-1 supply chain", "short ideas on consumer", "find me quality at
  value price". → jump to [Themed workflow](#themed-workflow).
- **Fishing** — the user has no theme. Examples: "what should I buy",
  "any ideas", "scan my feed", "surprise me", "pitch me something",
  `/zsxq-ideas` with no args. → jump to [Fishing workflow](#fishing-workflow).
- **Theme-build** — the user wants *tracked baskets* out of the feed, not
  a one-shot idea note. Examples: "build themes from my zsxq feed", "turn
  my feed into tracked baskets", "build a theme on X from zsxq", "make
  baskets from the latest 200 reports". → jump to [Theme-build
  workflow](#theme-build-workflow). This mode bridges into `theme-research`:
  it clusters the feed, then seeds/refreshes durable
  `reports/themes/<slug>_theme.md` baskets from the actual broker content.

If genuinely ambiguous (e.g. "ideas from zsxq" — they may mean "any
ideas" or "I'll tell you the theme next message"), ask one short
question: *"Theme in mind, fishing mode (I'll cluster your feed and
surface candidate themes first), or theme-build (turn the feed into
tracked baskets)?"* The tell for theme-build is the words *theme*,
*basket*, or *track* — fishing/themed produce a `reports/ideas/` note;
theme-build produces durable `reports/themes/` baskets.

Also pick up optional knobs if present:

- **Direction** — long / short / both (default both, lean long)
- **Window** — "last week" / "last month" / `--since YYYY-MM-DD`
  (default: most recent 200 reports, ~3-6 weeks of feed at current rate)
- **Cap / sector / style filters** — pass through to idea-generation
  Step 4 presentation if specified

## Fishing workflow

Goal: surface 3-6 candidate themes from the recent feed, plus a
**lite shortlist** of 2-3 ideas per top theme — enough that the user
gets something actionable from one invocation, without a 50-agent
fan-out.

### F1. Pull a wide window

```bash
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py \
    --limit 200 --summary-chars 800
```

(Bump `--limit` to 300+ for "last quarter", or use `--since
2026-05-01` for an explicit window. With 800-char summaries × 200 rows
the JSON is ~250 KB — fine in-context.)

### F2. Cluster in-context

Read every row's `topic_title` + `summary` + `tags`. Group into 3-6
themes that cover most of the feed. **Adapt names to what's actually
in the feed**, but typical clusters in this library:

- AI capex / inference economics / hyperscaler spend
- Robotics & autonomy (humanoids, AVs, embodied AI)
- Semis (DRAM / HBM / foundry / equipment / advanced packaging)
- Energy & power (datacenter power, grid, fuels, nuclear)
- China consumer / property / policy
- Geopolitics / supply-chain reshoring / export controls
- Biotech / healthcare / GLP-1
- Macro / rates / FX / commodities

Assign each row to its best-fit cluster (multi-assignment is fine for
crossover reports). Drop singletons / weak fits.

### F3. Theme cards (cheap — metadata only)

For each cluster, present:

- **Theme name + 1-2 sentence thesis** drawn from the cluster's summaries
- **Density** — # PDFs in the cluster from the 200-row window
- **Anchor PDFs** — top 2-3 `file_id`s (bank + 1-line "why this is the
  best read")
- **Named tickers (metadata only)** — union of the `tickers` column
  across rows in the cluster, with the most-cited 3-5 bolded

This phase requires **zero PDF reads**. Cost = 0 agents.

### F4. Pick top themes for the lite deep-dive

Auto-select the **top 2 themes by density** (most PDFs in the window).
For each, pick the **top 3 PDFs** by `claude_rating` × bank quality ×
recency. Total fan-out: up to 6 `/zsxq-analyze` extraction agents,
batched per the F5 memory gate.

If the user gave a direction hint ("long only", "no macro"), filter
themes accordingly before picking.

### F5. Parallel per-PDF extraction (lite)

Spawn one Agent per file_id with the [extraction-agent prompt](#extraction-agent-prompt)
below, subject to the same memory gate as
[T3](#t3-parallel-per-pdf-extraction-full): watcher running before any
≥2-wide fan-out, **≤4 concurrent** (6 file_ids = a batch of 4 then a
batch of 2), one-at-a-time fallback when `/tmp/mem-watch.log` shows
free RAM <25%.

### F6. Compact cross-theme shortlist

Aggregate the returned JSON (see [aggregation](#aggregation)). Present
a **condensed** shortlist — 2-3 ideas per covered theme, 5-8 total —
with:

- Ticker + theme tag + one-line thesis
- 2 bullets of evidence (cited to file_ids)
- 1 risk bullet

If two cited PDFs disagree on the same name (opposite ratings, PTs >20%
apart), say so in the evidence bullets — never blend into a fake
consensus. The full [T4b](#t4b-sell-side-view-evolution-卖方观点演变--mandatory-when-2-pdfs-cover-a-name)
treatment applies when the user picks the themed deep dive.

Skip the full idea-generation Step 4 table — fishing mode is for
triage, not for committing to a shortlist. (Fishing also omits
**Further viewing** by design.) Lite verify before presenting:
string-match 2-3 of the quoted numbers against
`extract_pdf.py --file-id <fid>` output and confirm links use the
`/zsxq/pdf/<file_id>/<name>#page=N` route — no appended log needed for
an in-chat shortlist.

### F7. Offer the deep dive

End with: *"Want the full themed workflow on any of these (5-10 ideas,
Step-4 presentation, saved to disk)? Reply with a theme name or
ticker."*

When the user picks → re-invoke as Themed workflow on the chosen theme.

## Themed workflow

Goal: a real shortlist of 5-10 ideas with full Step-4 presentation,
saved to `reports/ideas/`, with citations back to zsxq file_ids.

### T1. Pull theme-filtered rows

```bash
# Narrow themes — let SQL do a coarse cut
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py \
    --limit 300 --subject "<theme keyword>" --summary-chars 600

# Broad themes (e.g. just "AI") — skip --subject, filter in-context
python3 .claude/skills/zsxq-recommend/scripts/list_recent.py \
    --limit 300 --summary-chars 600
```

`--subject` is a single LIKE pattern across name/title/summary/tags/
comment. For multi-keyword themes ("humanoid OR robotics OR
embodied"), don't pass --subject — pull unfiltered and filter
in-context.

If `count == 0` after a --subject filter, drop the filter, widen
`--limit`, and tell the user the SQL filter was too narrow.

### T2. Rank in-context

Score each row 0-3 on relevance to the theme. Keep **top 8-12 file_ids**.
Tie-breakers (in order):

1. `claude_rating` (when populated — 0/1/2/3 scale)
2. Bank quality (GS / MS / JPM / UBS / Nomura > regional > unknown)
3. `page_count` (12-60 is the sweet spot; <5 is often a snippet, >100
   is often a year-end compendium that's mostly noise for this purpose)
4. `create_time` (recency)
5. `tickers` populated (the PDF has already been triaged)

If <3 PDFs pass the relevance bar, tell the user honestly — don't pad
with weak picks just to fill a quota.

### T3. Parallel per-PDF extraction (full)

One agent per file_id, using the [extraction-agent prompt](#extraction-agent-prompt)
below — fanned out in **memory-watcher-gated batches** (this is a 16 GB
machine; [CLAUDE.md § Workflow Memory Monitoring](../../../CLAUDE.md#workflow-memory-monitoring-mandatory-for-heavy-multi-agent-fan-outs)):

- **Before any ≥2-wide fan-out:** `pgrep -lf 'mem-watch-16gb.sh'` — if
  the watcher isn't running, start it first (recreate from CLAUDE.md if
  the script is missing).
- **Cap at 4 concurrent extraction agents** per message. They're
  lightweight single-PDF reads, not full report builds, but they still
  share RAM — 8-12 file_ids = 2-3 batches of ≤4, launching the next
  batch only after the prior returns.
- **Fall back to one-at-a-time sequential** if `tail -3
  /tmp/mem-watch.log` shows free RAM <25% (`warn` or worse).

### T4. Aggregate by ticker

Run the in-context [aggregation](#aggregation) procedure.

### T4b. Sell-side view evolution (卖方观点演变) — mandatory when ≥2 PDFs cover a name

Whenever **≥2 zsxq PDFs cover the same ticker / question**, run a
mechanical PT pre-pass *before* building the T5/T6 tables — it surfaces
same-institute revisions and PT dispersion without re-reading any PDF.
STRICTLY read-only (writes stay with `scripts/persist_pts.py`,
[Aggregation](#aggregation) step 6):

```bash
/opt/anaconda3/bin/python3 -c "
import sqlite3
con = sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)
for r in con.execute('''SELECT research_institute, rating, price_target,
    target_currency, report_date, report_file_id, upside_pct
    FROM price_targets WHERE company_ticker=?
    ORDER BY research_institute, report_date''', ('<TICKER>',)): print(r)"
```

Fold the result into the note:

- **Revision arrows in the PT cells** (T5 metric table + T6 comp table):
  when the same institute has ≥2 dated calls, render the evolution, not
  just the latest — e.g. `UBS: Buy $120 (26-03) → $150 (26-06, post-Q1
  beat)` — each leg keeping its own `zsxq #fid` cite and the stated
  trigger (earnings print, policy change, channel checks). The filename
  `-YYMMDD` suffix is the authoritative report date (see the
  [citation convention](#zsxq-citation-convention)); a 2026-03 PT and a
  2026-06 PT from the same institute are two different views, never
  dedup'd into one.
- **Disagreement row, never a fake consensus.** When institutes disagree
  (opposite ratings, PTs >20% apart, conflicting reads of the same
  datapoint), do NOT blend them — add a compact disagreement table under
  the affected idea block —
  `| Institute | Date | Rating / PT | Core argument | What evidence would prove them right |`
  — and say in the thesis bullets that the idea's conviction rests on a
  contested call (which side the bull/bear case takes, and why).
- When ≥3 institutes have live PTs on a name, quote the dispersion
  (min / median / max, spread %) next to its T6 comp row.

### T5. idea-generation Step 4 presentation

For each shortlisted ticker (top 5-10 by aggregated score), produce
the full Step-4 block from the `idea-generation` skill:

```
### [Ticker] — [Long/Short] — [One-line thesis]

| Metric | Value | vs. Peers |
|--------|-------|-----------|
| Market cap | ... | ... |
| EV/EBITDA (NTM) | ... | ... |
| P/E (NTM) | ... | ... |
| Revenue growth (NTM) | ... | ... |
| EBITDA margin | ... | ... |
| FCF yield | ... | ... |

**Thesis (3-5 bullets, each cited to zsxq file_ids):**
- ...

**Key risks (cited to zsxq):**
- ...

**zsxq evidence (the PDFs that surfaced this name):**
- file_id `184...` — Goldman, p.12 — "..."
- file_id `184...` — Morgan Stanley, p.5 — "..."

**Suggested next steps:**
- Full deep dive: `/company-research <ticker>`
- Initiate coverage: `/initiating-coverage <ticker>`
- Peer comparison: `/compare-companies <ticker> vs <peer>`
- Trade entry/exit: `/trading-analysis <ticker>` / `/take-profit-lab <ticker>`
```

For multiples (Market cap / EV/EBITDA / P/E / etc.) — look them up
quickly via yfinance if not in any of the cited PDFs. Otherwise mark
"n/a — not in cited PDFs" rather than fabricating.

Provenance is mandatory even inside tables — an uncited, undated
market-data number violates the project Numerical Accuracy rule:

- Put a one-line footer immediately under the shortlist heading:
  `*Market data: yfinance, as of YYYY-MM-DD · PTs/estimates: cited zsxq
  PDFs (file_id-linked) · n/a = in neither source*`
- PT / estimate rows inside the metric table carry the same
  `zsxq #<fid>` mini-cite used in thesis bullets.
- When a cited PDF publishes scenario PTs (bull / base / bear), include
  the triplet in the per-idea table — don't relegate the downside case
  to a risk bullet.

### T5b. Overview chart (optional, recommended)

Render ONE chart for the whole shortlist — normalized 6-month relative
performance of the top 5-8 tickers vs a relevant benchmark (yfinance) —
saved to `reports/charts/zsxq_<slug>_<date>_perf.png` and embedded near
the top of the note. Subject to the global chart rules in
[CLAUDE.md](../../../CLAUDE.md#chart-generation-rules-mandatory-every-chart-producing-skill):
in-image source footer with as-of date, x-axis clipped to the
intersection of valid data, rightmost point fresh. Skip when more than
half the shortlist lacks clean yfinance tickers.

### Further viewing — explainer videos (optional, but default to including)

When an idea's thesis rests on something a reader would struggle to picture from prose alone — the technology underlying an idea: the thing that makes the thesis work but is hard to picture (a humanoid robot's actuators / harmonic reducers / ball-screws / force sensors, an advanced-packaging or lithography step, an HBM stacking process, a complex product architecture, an unfamiliar business model, or a market-structure concept) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the idea is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the idea block the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### T6. Save the report

Path: `reports/ideas/zsxq_<theme-slug>_<YYYY-MM-DD>.md`

- Theme slug: kebab-case English (per [CLAUDE.md filename rule](../../../CLAUDE.md#research-report-filenames)).
  Examples: `zsxq_ai-infra_2026-05-31.md`, `zsxq_humanoid_2026-05-31.md`,
  `zsxq_china-semis_2026-05-31.md`. **Never** use a pure-Chinese slug.
- Include at the top:
  - Theme + date range scanned + # PDFs in the window + # PDFs analyzed
  - List of file_ids that fed the shortlist (so the user can re-run
    `/zsxq-analyze` on any of them)
- Then the shortlist (Step-4 blocks).
- Then a **PT & valuation comp** table for the whole shortlist — the
  cross-ticker view the per-idea tables can't give (modeled on
  theme-research's Valuation snapshot; this is the most-used exhibit in
  any sell-side sector piece). Columns:

  `| Ticker | Rating(s) | Broker PT(s) (each with zsxq #fid) | Px @ note
  date (from the PDF) | Current px (yfinance, dated) | Upside % vs note
  px | Fwd P/E | FY1/FY2 EPS (where the PDF states them) |`

  Mark `n/a` where a cell is in neither a cited PDF nor yfinance.
- Then a final "Sources" section listing all cited file_ids with
  `name`, `bank`, `create_time`.

The viewer at `http://xs-macbook-air.local:5001/claude-reports/` will surface
this under its idea-generation bucket automatically (if `reports/ideas/`
isn't yet a known bucket, the file still renders — flag it for a
viewer update separately).

### T7. Verify & log

Before the note ships:

1. Randomly pick 3–5 cited numbers and string-match each against the
   extracted original text:
   `python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id
   <fid> | grep -F "<number>"`.
2. Confirm every PT in the comp / metric tables literally appears in
   its cited PDF.
3. Confirm all zsxq links use the
   `/zsxq/pdf/<file_id>/<name>#page=N` route.
4. **View-evolution check (conditional — only when ≥2 PDFs covered the
   same name):** confirm the [T4b](#t4b-sell-side-view-evolution-卖方观点演变--mandatory-when-2-pdfs-cover-a-name)
   treatment landed — same-institute revisions arrow'd with dates,
   contested calls in a disagreement table, no blended PT anywhere.
5. Append `<details><summary>Verification log — YYYY-MM-DD</summary>`
   to the report, listing each check as ✓ / ✗-fixed.

Cheap to run — the extraction agents already returned page+quote pairs.

## Theme-build workflow

Goal: turn the zsxq feed into **durable tracked baskets** at
`reports/themes/<slug>_theme.md`, not a one-shot idea note. This mode is
the bridge from the feed into [[theme-research]]: it clusters the feed,
then for each chosen theme hands `theme-research` an *evidence bundle of
the cluster's actual broker content* so the basket is built (or refreshed)
from specific, cited broker numbers — not generic web knowledge.

> **Why this mode exists.** The failure it prevents: building a theme
> basket that cites the zsxq report *titles* as evidence but never uses
> the broker calls *inside* them (target prices, deal structures,
> forecasts). That content is the new, non-public part of the feed and is
> the entire reason to source from zsxq rather than a web search. If the
> basket reads like it could have been written without the PDFs, this mode
> was done wrong.

### TB1. Cluster the feed (create) — or strict-keyword re-mine (expansion refresh)

**Create-mode:** reuse Fishing steps **F1–F3** verbatim: pull the 200-row window
(`list_recent.py --limit 200 --summary-chars 800`), cluster into 3–7
themes, present theme cards (name + thesis + density + anchor file_ids +
metadata tickers). **Surface the cluster list and get the user to confirm
which themes to build** (1–7) and the ticker scope — per `theme-research`'s
create-mode rule, baskets are most useful when the user has agreed to the
scope. Also confirm language (English default; Chinese opt-in).

**Expansion-refresh mode** (rebuilding/widening an existing theme — see
[[theme-research]] Step 4b): the loose-keyword clustering used in create-mode
is the *wrong* tool — it over-matches generic AI / data-center / 算力 reports
that aren't actually on-theme. Use a **strict-keyword** query against a wider
DB window instead:

- query the recent **~600–800** rows (not just 200) since the original cluster
  may have used a narrower window;
- filter strictly on **tracked-ticker names/codes** (e.g. `海力士`, `Hua Hong`,
  `1347.HK`, `MU\b`) **OR theme-specific technical terms** (e.g. `HBM[34]`,
  `NOR Flash`, `SST`, `cobot`, `GLP-1`) — never `AI`/`data center`/`算力`/
  `存储` alone.
- exclude file_ids already in the existing theme's evidence_file_ids set.

Surface the candidate adds to the user before editing the Tracked tickers
table: each candidate ticker needs a **conviction-grade broker call** in
the original PDF text (a Buy / OW rating with target price, a deal mechanic,
a guidance raise — not just a mention). Loose mentions go in the watch list,
not the basket. User confirms which adds make it in.

### TB2. Extract the ORIGINAL PDF content (per chosen theme)

**The primary source is the original PDF text, not the summary column.**
The `summary` (zsxq's 翻译精华) is a curated, often re-translated highlight
blurb — a secondary source that paraphrases and can drop or distort numbers.
Use it only as a last resort (a pure-chart page where even OCR fails), and
label it as such. Every broker number you cite must string-match the
*extracted original text*.

First build the extraction manifest — it reports, per report, whether the
original text is text-ready / OCR-cached / needs-OCR, and emits the extract
command:

```bash
python3 .claude/skills/zsxq-ideas/scripts/evidence_bundle.py \
    --file-ids <comma-sep cluster file_ids> \
    --slug <theme-slug> --out /tmp/zsxq_evidence/<theme-slug>.md
```

Most bank PDFs in this library are **image-only** (fitz returns nothing) —
the manifest flags these. OCR them first (one sequential pass to avoid
SQLite write-contention; the `ocr_text` cache write is the sanctioned path
per [CLAUDE.md § PDF extraction](../../../CLAUDE.md)):

```bash
for f in <image-only file_ids from the manifest>; do
    python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py --file-id $f
done
```

Then extract the original text per report (now OCR-backed for image-only):

```bash
python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py \
    --file-id <id> --header --max-chars 40000
# still empty (pure charts)? render_pdf_pages.py + Read the PNG visually.
# only if THAT fails too: fall back to the 翻译精华 summary, labelled as such.
```

### TB3. Build / refresh the basket via theme-research

**Multi-theme** (`build all 7`, `refresh 5 themes`): each theme agent runs
a full [[theme-research]] build — a *heavy report skill* — so on this 16 GB
machine run them **strictly sequential, concurrency 1**: one Agent-tool
subagent at a time, launching the next only after the prior returns, with
the memory watcher running (`pgrep -lf 'mem-watch-16gb.sh'`), per
[CLAUDE.md § Workflow Memory Monitoring](../../../CLAUDE.md#workflow-memory-monitoring-mandatory-for-heavy-multi-agent-fan-outs).
**Never spawn multiple theme agents in one message.**
Each agent runs the [[theme-research]] create-or-refresh workflow on its
slug and is handed: (a) the theme slug + confirmed ticker scope, (b) the
extraction-manifest path from TB2, (c) the instruction to `extract_pdf`
**every** report it cites (not just flagships) and read the original text —
OCR'd first where the manifest says so, summary fallback-only, (d) the
[zsxq citation convention](#zsxq-citation-convention) below, (e) the
**Further viewing** explainer-video convention (same rules as the
Themed-workflow section above: durable channels only, browser-UA
200-check, teaching aid never a citation — `theme-research` requires the
block or an explicit omission notice and its Step 7 checks for it), and
(f) the instruction to persist its PT calls via
`scripts/persist_pts.py --replace` (see [Aggregation](#aggregation) step 6)
and report the upserts in the basket's **What's New** block (e.g. "11 PTs
upserted to `/pt`").

**Single-theme (the user is doing them "1 by 1")**: do the edits **directly**
in the main loop instead of delegating to an agent. The agent round-trip
overhead, plus the post-agent reconciliation pass (verifying every quote,
rebuilding the snapshot, sometimes patching partial state where the agent's
edits landed incompletely) costs more wall-clock than just opening the file
and editing. Pre-compute the things an agent would need anyway (basket
returns, OCR cache for image-only PDFs, page+quote extraction for the
flagship reports) — then write the file as one or two `Edit`/`Write` calls.
Reserved-for-parallelism is genuinely-N-independent work, not careful
single-theme refreshes.

`theme-research` owns the file format and the verified Performance/return
data; this mode's whole value-add is feeding it the **real zsxq broker
content** read from the original PDFs, woven into the Thesis, per-ticker
Justification cells, Recent events, and Data Used manifest.

If the basket already exists, this is a *refresh + enrichment* pass — edit
in place, append a `## History` line noting the zsxq enrichment, and do
**not** recompute the Performance table unless the user asked for a data
refresh. For expansion-refresh (Step 4b in `theme-research`), recompute is
required.

### TB4. Verify (the enrichment-specific checks)

Beyond `theme-research`'s own Step-7 verify:

- **Every zsxq-sourced number cites a file_id**, not just the report
  title. Grep the file for the viewer-link pattern and confirm the count
  is non-trivial (a 15-ticker basket sourced from ~10 reports should carry
  10+ `zsxq #` citations).
- **No fabricated broker numbers.** Spot-check 3–5 zsxq-attributed figures
  against the evidence bundle / extracted text — the number must literally
  appear in the cited report. This is the project's Numerical Accuracy
  rule applied to broker content.
- Structure intact (12 mandatory sections), ticker table parses, sample
  URLs resolve.

### TB5. Hand-off

The durable artifact is the `theme-research` basket, refreshed over time by
`theme-research` itself (`refresh my <slug> theme`). `zsxq-ideas` does not
maintain the basket after this — it *seeds and re-enriches* it from the
feed. Point the user at `refresh my <slug> theme` for the next cycle.

## zsxq citation convention

Whenever zsxq content lands in **any** downstream report — a `reports/ideas/`
idea note or a `reports/themes/` basket — cite the broker's *specific
content* to the source `file_id`, never the report title alone:

- **Inline format — file_id AND page:**
  `[Bank — short topic, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)`.
  The page number is mandatory: `extract_pdf.py` marks pages as
  `===== Page N =====`, so every number you cite has a known page. Put `p.N`
  in the link text and `#page=N` in the URL (the viewer honors the PDF
  `#page=` fragment; if it ever doesn't, `p.N` in the text still tells the
  reader where to look). If a figure recurs on several pages, cite the page
  with the fullest context (usually the exhibit/section page, not the p.1
  teaser).
- **Quote the source text.** Alongside the number, give a short quote of the
  *original* sentence/phrase it came from, in the PDF's original language —
  e.g. ...claim
  `([MS — Energy Meets Compute, zsxq #184152244582842 p.6](http://xs-macbook-air.local:5001/zsxq/pdf/184152244582842/Morgan%20Stanley-Energy%20Security%20%26%20AI%EF%BC%9A%20Energy%20Meets%20Compute%EF%BC%9A%20Supercycle%20Recharges-260528.pdf#page=6) — “US$5trn+ in investments across the region… unlocking US$9trn in value”)`.
  The quote is the original English/Chinese/Japanese text from the PDF, NOT
  the 翻译精华 summary's paraphrase. Keep quotes short (the clause carrying
  the number); use `…` for elisions. Match the quote verbatim to the
  extracted text.
- **Cite the number, not the headline.** "MS sees Asia energy capex doubling
  by 2030" with no link is a non-citation; the figure needs the page-anchored
  link + the source quote above.
- **Only state numbers that literally appear** in the *extracted/OCR'd
  original PDF text* — not the 翻译精华 summary (a curated secondary source
  that paraphrases and re-translates; e.g. its "超5万亿美元" rounds the
  original's precise "US$5,454bn" on p.8). String-match every number against
  the extracted text before citing it. No extrapolation. Numerical Accuracy rule.
- **Preserve original-language report titles** in the link text (年度报告,
  有価証券報告書, 创新黎明 2.0) per the project citation standard.
- **Bank publication date — the filename's `-YYMMDD` suffix is
  authoritative.** Derive the pub date from the suffix; sanity-check that
  the db `create_time` falls within suffix +0–3 days (the normal scan
  lag). If the two disagree by >7 days, or the derived pub date postdates
  the report's own date, do NOT silently print either — annotate the
  source row inline (e.g. `(date fields conflict: filename 2026-06-05 vs
  feed 2026-05-06)`) and prefer the filename suffix. A pub date after the
  scan date is impossible; an unflagged anachronism shipped once
  (Bernstein `-260605` printed as 2026-05-06 in a report dated
  2026-05-31).

## Extraction-agent prompt

Use this verbatim for every parallel `/zsxq-analyze` fan-out, plugging
in the file_id:

```
Use the zsxq-analyze skill on file_id <N>.

Extract and return ONLY raw JSON (no prose, no markdown fences, no
explanation) matching this shape:

{
  "file_id": <N>,
  "name": "<PDF name from the row>",
  "bank": "<publisher / bank if known, else null>",
  "tickers": ["TICKER1", "TICKER2", ...],
  "thesis_per_ticker": {
    "TICKER1": "1-2 sentence bull or bear case as stated in THIS PDF",
    ...
  },
  "direction_per_ticker": {
    "TICKER1": "long" | "short" | "neutral",
    ...
  },
  "key_numbers": [
    {"metric": "what it measures", "value": "the number with units",
     "page": 12, "quote": "verbatim original-language source text containing the number"}
  ],
  "pt_calls": [
    {"ticker": "MU", "company_name": "Micron", "broker": "UBS",
     "rating": "Buy", "pt": 1625, "ccy": "USD",
     "catalyst": "optional 1-line driver", "file_id": <N>,
     "page": 1, "quote": "verbatim rating/PT text from the PDF"}
  ],
  "catalysts": ["2-3 catalysts the PDF flags"],
  "risks": ["2-3 risks the PDF flags"],
  "theme_fit": "1 sentence on how this PDF fits the requested theme"
}

For every entry in `key_numbers` the `page` is the `===== Page N =====`
marker from extract_pdf where the number appears, and `quote` is the
ORIGINAL text (English / Chinese / Japanese as printed in the PDF) — never
the 翻译精华 summary's paraphrase. String-match the quote to the extracted
text. Downstream this becomes the page-anchored citation + source quote per
the [zsxq citation convention](#zsxq-citation-convention).

`pt_calls` is one record per (ticker × broker) EXPLICIT rating/PT call —
page-1 rating boxes, ratings tables, "目标价Z元" phrasings with a number.
Field names match scripts/persist_pts.py's record shape (ticker in
yfinance form, `pt` numeric, `ccy` required when `pt` is set); `page` and
`quote` ride along for citations and are ignored by the helper. Do NOT
run persist_pts.py yourself — the orchestrator persists the union once
after aggregation (SQLite write contention). Empty array if the PDF has
no explicit broker calls.

Tickers must use the same convention as the row's `tickers` column
when present (e.g. AAPL, NVDA, SZSE:002050, HKEX:1211). If the PDF
names a company without a ticker, include it as the company name
(e.g. "Anpeilong"). If the PDF is macro/thematic with no named
single-stock ideas, return an empty tickers array and put the macro
view in theme_fit.
```

Subagent_type: `general-purpose`. Each agent runs ~30-60s; 8-12
file_ids in watcher-gated batches of ≤4 = 2-4 min wall-clock.

## Aggregation

In-context, after all extraction agents return:

1. **Union all tickers.** For each ticker, collect:
   - `frequency` = # PDFs that named it
   - `bull_count` / `bear_count` from direction_per_ticker
   - `thesis_bullets` = list of `(file_id, bank, page, thesis)`
   - `key_numbers` cited near this ticker
   - `catalysts` mentioned
   - `risks` mentioned
2. **Score** = `frequency × bank_quality_factor × recency_factor`
   - bank_quality_factor: GS/MS/JPM/UBS/Nomura/Citi = 1.2; regional = 1.0; unknown = 0.8
   - recency_factor: 1.0 for PDFs <2 weeks old, 0.9 for 2-6 weeks, 0.8 for >6 weeks
3. **Lean** = "long" if `bull_count > bear_count`, "short" if reverse,
   "split" if tied (flag explicitly in the thesis).
4. **Sort by score, keep top 5-10.**
5. **Drop tickers that only appear once AND have no `claude_rating`
   on the source PDF** — that's signal-too-weak.
6. **Persist PT calls (all modes — mandatory).** Concatenate every
   agent's `pt_calls` into ONE JSON array and pipe it once, from the
   orchestrator — never from the parallel extraction agents (SQLite
   write contention) and never raw SQL (Tier-2 helper only, per
   [CLAUDE.md DB safety](../../../CLAUDE.md#database-safety-mandatory--non-negotiable-zero-exceptions)):

   ```bash
   /opt/anaconda3/bin/python3 scripts/persist_pts.py --replace <<'JSON'
   [ ...union of all pt_calls... ]
   JSON
   ```

   `--replace` because these are deep-read extractions — the same
   precedence `/zsxq-analyze` uses (they overwrite any summary-only row
   from `/zsxq-recommend`). Schema / vocabulary / skip rules:
   [`reference/pt_extraction.md`](../../../reference/pt_extraction.md).
   Surface the script's stdout counts in the note/shortlist, e.g.
   `📈 PT inserts: 9 new (2 replaced), 160 total in /pt`.

Steps 1–5 are small JSON (8-12 PDFs × a few KB each = ~50 KB) — do them
in-context, no script needed.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the subject of the output — the ticker, theme, sector, ETF holdings, deal, or any name that materially drives the analysis — sits in **AI** (foundation models, AI software/agents, AI infrastructure: datacenter compute, networking, power), **robotics** (humanoids, industrial automation, AMRs, actuators / reducers / sensors / end-effectors), or **semiconductors** (fabless, foundry, IDM, memory/HBM, equipment/WFE, materials, EDA/IP, advanced packaging), give those names a **detailed narrative treatment**, not summary bullets:

- **Write full narrative prose** for the sector-relevant sections — mechanism and causality ("X drives Y because Z"), not headline restating. Bullets may organize the prose but never replace it.
- **Cover the sector-specific dimensions that apply:**
  - *Technology position & roadmap* — process node / architecture / model-capability cadence vs named competitors (e.g., N2 vs 18A, HBM3E→HBM4, GB200→Rubin, Optimus gen-3 vs Figure 03).
  - *Supply-chain position* — key suppliers and customers up/down the chain, single-source chokepoints (TSMC/CoWoS, EUV, HBM), where pricing power sits, content-per-unit ($ per GPU / per robot / per vehicle).
  - *AI demand linkage* — the explicit path from AI capex to this name's P&L (orders → backlog → revenue recognition) with the actual disclosed numbers, never a generic "AI beneficiary" label.
  - *Robotics linkage* — design-win status, which platforms (Tesla Optimus, Figure, Unitree, domestic Chinese OEMs), volume and timeline realism vs the hype cycle.
  - *Cycle context* — where the semi / memory-pricing / AI-capex cycle stands right now and what that implies for forward estimates.
  - *Geopolitics & export controls* — US BIS rules, China localization, tariff exposure, entity-list status where relevant.
- **Quantify the narrative.** Each dimension covered should carry at least one sourced number (TAM, ASP, capacity, units, share). All figures obey the project's numerical-accuracy rule — every number traces to a URL or PDF page cited in the same paragraph.
- **Engage the sell-side view.** Where the zsxq library or other broker sources are in scope for this skill, the AI/robotics/semi narrative must engage the institute view (PTs, estimate revisions, cross-broker disagreement) rather than ignoring it.

This rule **deepens** the skill's existing output format — it never replaces or shortens the required structure. For subjects outside these sectors, the skill's baseline depth applies unchanged.

## Notes & guardrails

- **Parallelism is memory-gated, not mandatory.** Per-PDF extraction
  fans out in batches of ≤4 Agent calls with the memory watcher running
  (T3/F5); theme-build's theme-research agents run strictly sequential
  at concurrency 1 (TB3).
  [CLAUDE.md § Workflow Memory Monitoring](../../../CLAUDE.md#workflow-memory-monitoring-mandatory-for-heavy-multi-agent-fan-outs)
  (16 GB machine) overrides the older parallel-multi-report feedback:
  **never launch a ≥2-wide fan-out without `mem-watch-16gb.sh` running.**
- **The shortlist is idea sourcing, not a buy recommendation.** Every
  top name should suggest `/company-research <ticker>` as the next
  step. Do not call this output a "BUY rating" or "thesis confirmed".
- **db/zsxq.db is read-only from this skill.** Per [CLAUDE.md DB
  safety](../../../CLAUDE.md#database-safety-mandatory--non-negotiable-zero-exceptions),
  no writes whatsoever. Both helper skills already honor this.
- **Filenames must contain English.** Per the [filename rule](../../../CLAUDE.md#research-report-filenames-mandatory--must-include-english--pinyin-name),
  `zsxq_AI基建_2026-05-31.md` is wrong; `zsxq_ai-infra_2026-05-31.md`
  is right.
- **Be honest about coverage gaps.** If a theme has <3 strong PDFs in
  the window, say so — don't pad. If a top ticker is only named once,
  flag it as `(single-PDF call)` next to the score.
- **Don't double-quote OCR garble.** If a per-PDF agent reports
  scrambled OCR (multi-column research notes), down-weight that PDF's
  thesis bullets in the aggregation and note "OCR layout issue —
  thesis text may be partial".
- **Do not invoke any other heavy skill from inside this one.**
  Specifically: don't auto-trigger `/company-research` on every
  shortlisted ticker — that's the user's next step, not yours.
- This skill **does not write to db/zsxq.db**. It only reads via the
  two helper skills.

## What this skill is NOT

- Not a generic stock screener — for that, use `idea-generation`
  directly (it has quant screens for value / growth / quality / etc.)
  or `canslim-screener`.
- Not a fundamental validator — the shortlist is a starting funnel.
  Validation = `/company-research`, `/trading-analysis`.
- Not the *owner* of thematic baskets — `theme-research` owns the durable
  basket (`reports/themes/<slug>_theme.md`) and its refresh / mutate /
  drift lifecycle. `zsxq-ideas` **Theme-build mode** *seeds and
  re-enriches* those baskets from the feed (clustering → evidence bundles
  → the citation discipline), then hands off. The themed/fishing modes
  remain one-shot idea notes at `reports/ideas/`. If the user wants to
  refresh an existing basket's *data* (returns / drift) rather than its
  *zsxq sourcing*, send them straight to `theme-research` (`refresh my
  <slug> theme`).
- Not a deep read of a single PDF — that's `/zsxq-analyze` directly.

## Prerequisites

This skill internally uses (no machine-enforced deps — these are
already-installed sibling skills, not upstream artifacts):

- [[zsxq-recommend]] — metadata pull + feed clustering
- [[zsxq-analyze]] — per-PDF extraction (parallel fan-out); its
  `scripts/extract_pdf.py` / `ocr_pdf.py` go deeper than the summary bundle
- [[idea-generation]] — Step-4 presentation format (themed / fishing modes)
- [[theme-research]] — durable basket format + create/refresh/drift
  lifecycle (theme-build mode hands off to it)

Own scripts:

- `scripts/evidence_bundle.py` — builds the theme-build *extraction
  manifest*: per file_id, the metadata + whether the original text is
  text-ready / OCR-cached / needs-OCR + the extract command. Original PDF
  text is the source; the 翻译精华 summary is included only as labelled
  fallback. Read-only on `db/zsxq.db`.
