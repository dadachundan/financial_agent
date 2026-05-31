---
name: zsxq-ideas
description: Generate investment ideas from the zsxq report library (db/zsxq.db) by combining zsxq-recommend (theme/PDF surfacing) + zsxq-analyze (parallel per-PDF deep reads) + idea-generation (Step-4 presentation). Supports two modes — **themed** ("ideas on AI infra from zsxq", "long humanoid plays from my reports") and **fishing** ("what should I buy", "scan my zsxq feed", "any ideas", "pitch me something from zsxq"). Use whenever the user wants stock ideas sourced from their zsxq library rather than generic quantitative screens. Triggers: "ideas from zsxq", "zsxq ideas", "what stocks does my zsxq feed suggest", "scan zsxq for ideas", "/zsxq-ideas".
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

If genuinely ambiguous (e.g. "ideas from zsxq" — they may mean "any
ideas" or "I'll tell you the theme next message"), ask one short
question: *"Theme in mind, or fishing mode (I'll cluster your feed
and surface candidate themes first)?"*

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
recency. Total fan-out: up to 6 parallel `/zsxq-analyze` agents.

If the user gave a direction hint ("long only", "no macro"), filter
themes accordingly before picking.

### F5. Parallel per-PDF extraction (lite)

Spawn one Agent per file_id in a **single message**, all in parallel,
each with the [extraction-agent prompt](#extraction-agent-prompt)
below.

### F6. Compact cross-theme shortlist

Aggregate the returned JSON (see [aggregation](#aggregation)). Present
a **condensed** shortlist — 2-3 ideas per covered theme, 5-8 total —
with:

- Ticker + theme tag + one-line thesis
- 2 bullets of evidence (cited to file_ids)
- 1 risk bullet

Skip the full idea-generation Step 4 table — fishing mode is for
triage, not for committing to a shortlist.

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

**SINGLE message, multiple Agent tool calls in parallel.** One agent
per file_id. Use the [extraction-agent prompt](#extraction-agent-prompt)
below. Cap at 12 concurrent (the project's parallel agent limit is
already enforced by the orchestrator; just don't fan out more than 12
in one message).

### T4. Aggregate by ticker

Run the in-context [aggregation](#aggregation) procedure.

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
- Then a final "Sources" section listing all cited file_ids with
  `name`, `bank`, `create_time`.

The viewer at `http://localhost:5001/claude-reports/` will surface
this under its idea-generation bucket automatically (if `reports/ideas/`
isn't yet a known bucket, the file still renders — flag it for a
viewer update separately).

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
  "key_numbers": ["3-5 hard numbers from the PDF, each with units + the metric"],
  "catalysts": ["2-3 catalysts the PDF flags"],
  "risks": ["2-3 risks the PDF flags"],
  "page_citations": {"TICKER1": "p.12", ...},
  "theme_fit": "1 sentence on how this PDF fits the requested theme"
}

Tickers must use the same convention as the row's `tickers` column
when present (e.g. AAPL, NVDA, SZSE:002050, HKEX:1211). If the PDF
names a company without a ticker, include it as the company name
(e.g. "Anpeilong"). If the PDF is macro/thematic with no named
single-stock ideas, return an empty tickers array and put the macro
view in theme_fit.
```

Subagent_type: `general-purpose`. Each agent runs ~30-60s; 8-12 in
parallel = 1-2 min wall-clock.

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

This is small JSON (8-12 PDFs × a few KB each = ~50 KB) — do it
in-context, no script needed.

## Notes & guardrails

- **Parallelism is mandatory.** Per-PDF extraction must fan out in a
  SINGLE message with multiple Agent tool calls. Serializing 10 PDFs
  is a 10-minute job vs 1-minute parallel. The project's [parallel-
  multi-report feedback](../../../.claude/projects/-Users-x-projects-financial-agent/memory/feedback_parallel_multi_report.md)
  applies here directly.
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
- Not a thematic basket tracker — for that, use `theme-research`
  (which maintains tracked baskets over time at
  `reports/themes/<slug>_theme.md`). `zsxq-ideas` is a one-shot
  source-from-feed, `theme-research` is the durable basket.
- Not a deep read of a single PDF — that's `/zsxq-analyze` directly.

## Prerequisites

This skill internally uses (no machine-enforced deps — these are
already-installed sibling skills, not upstream artifacts):

- [[zsxq-recommend]] — metadata pull
- [[zsxq-analyze]] — per-PDF extraction (parallel fan-out)
- [[idea-generation]] — Step-4 presentation format
