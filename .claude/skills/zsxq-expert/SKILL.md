---
name: zsxq-expert
description: Answer an in-depth question by grounding it in the local broker-PDF library (db/zsxq.db, ~7,000 institute reports) — the "PDF expert system". Resolves the focal company + its peers from the knowledge graph, retrieves the most relevant PDFs by ranked full-text search (zsxq_fts.py), deep-reads the top ones — pulling the actual comparison **tables** (extract_tables.py) and **figures/charts** (render_pdf_pages.py + vision) — and synthesizes a cited answer where every number traces to a specific PDF page. Each deep read is written back as a structured card (zsxq_cards.py) and as graph edges (manual_graph.py), so the library gets smarter with use. NO LLM API — Claude (the agent, in conversation) is the reader and synthesizer. Use when the user wants a deep, broker-grounded answer or comparison FROM THEIR OWN REPORTS rather than a web search — e.g. "how does ISRG compare with peers (using my reports)", "what do my broker reports say about HBM pricing", "compare Stryker vs Intuitive from zsxq", "deep dive X vs Y from my PDFs", "answer from my research library", "/zsxq-expert <question>". Distinct from /zsxq-ideas (idea shortlists) and /zsxq-analyze (one named PDF).
---

# Answer In-Depth Questions from the zsxq PDF Library (the PDF expert system)

The user has ~7,000 sell-side / institute PDFs in `db/zsxq.db`. Web answers are
shallow and messy; the depth lives in these reports — their comparison tables,
TAM exhibits, channel checks, and price-target logic. This skill turns that pile
into an **expert you can ask**: it finds the right PDFs, reads the real tables
and charts inside them, and answers with page-anchored citations — then
remembers what it read so the next question is faster.

```
question ──▶ (1) resolve focal + peers      [graph_mirror: COMPETES_WITH / SUPPLIES]
          ──▶ (2) retrieve PDFs, ranked      [zsxq_fts.py  — BM25 over the corpus]
          ──▶ (3) cards vs fresh             [zsxq_cards.py — reuse what's digested]
          ──▶ (4) deep reads (sequential)    [extract_tables.py + render_pdf_pages.py + OCR]
          ──▶ (5) synthesize cited answer    [tables + figures, every number → a page]
          ──▶ (6) write back                 [cards + graph edges — the library learns]
```

**You — Claude — are the whole intelligence layer.** There is no embedding API,
no vector DB, no LLM call (project rule). Retrieval is keyword + entity + graph;
generation is your own reading and reasoning over the actual pages.

**Interpreter:** run all project scripts with `/opt/anaconda3/bin/python3`
(per `feedback_anaconda_python_db_scripts` — bare `python3` has failed
`mode=ro` DB opens, the exact pattern `zsxq_fts.py` uses, and lacks deps
in some shells).

## When to use vs the siblings

- **`/zsxq-expert`** (this) — a *question* to answer in depth from the library:
  "how does ISRG compare", "what's the bull case on HBM", "who leads China
  surgical robots". Output is an *answer* (chat by default).
- **`/zsxq-ideas`** — "what should I buy" / "scan my feed" → an idea *shortlist*.
- **`/zsxq-analyze`** — one named PDF (by file_id / filename) → a single deep read.

If the user names exactly one PDF, defer to `/zsxq-analyze`. If they want a
buy-list, defer to `/zsxq-ideas`. Otherwise, this skill.

## Step 1 — Parse the question

Extract, in-context:

- **Focal entity(ies)** — the company / theme the question is about (e.g. ISRG
  / Intuitive Surgical). Normalize to a canonical name + ticker.
- **Comparison set** — explicit peers the user named ("vs Stryker and
  Medtronic"), OR *implicit* ("compare with other companies") — in which case
  Step 2 derives the peers.
- **Dimensions asked** — what the answer must cover (margins, procedure volume,
  TAM, moat, valuation, install base…). If unspecified, default to: business
  model, competitive position, growth, margins/economics, valuation, risks.
- **Theme keywords** — for retrieval (e.g. "surgical robotics", "手术机器人",
  "da Vinci", "Mako").

State the parse back in one line before working, so the user can correct scope.

## Step 2 — Resolve focal + peers from the knowledge graph

The graph (`db/graph_mirror.db`) already encodes COMPETES_WITH / SUPPLIES edges
for ~340 companies. Use it to (a) expand an implicit "other companies" into a
concrete peer set and (b) see what the graph already asserts.

```bash
# focal entity + its competitive/supply neighborhood
python3 - <<'PY'
import graph_mirror as gm
c = gm.get_conn()
r = gm.search(c, "Intuitive Surgical", limit=10)
print("FOCAL/NODES:", [(n["name"], n.get("labels")) for n in r["nodes"]][:5])
print("EDGES:")
for e in r["edges"][:20]:
    print(f"  {e['source_node_name']} -[{e['name']}]-> {e['target_node_name']}  :: {e['fact']}")
PY
```

From the returned edges, build the **peer set** = entities linked to the focal
by `COMPETES_WITH` (direct competitors) plus notable `SUPPLIES` counterparties
when the question is supply-chain-flavoured. If the graph is sparse on the focal
(few/no edges — likely, since the graph was built from `reports/`, not the
PDFs), don't stall: derive peers from the retrieval step (Step 3 surfaces the
peers the broker reports themselves name in their comparison tables) and you'll
*write those edges back* in Step 6.

## Step 3 — Retrieve the right PDFs (ranked FTS)

Use the trigram-FTS retrieval layer — BM25-ranked, bilingual (English + 中文),
far better than the viewer's unranked LIKE scan. Run from the project root:

```bash
# focal + theme, ranked; --json for machine parsing, or omit for a readable list
python3 zsxq_fts.py -q "Intuitive Surgical da Vinci surgical robotics" -n 25 --json

# one query per named/derived peer, so each side of the comparison is covered
python3 zsxq_fts.py -q "Stryker Mako orthopedic robotics" -n 10 --json
python3 zsxq_fts.py -q "Medtronic Hugo surgical robot" -n 10 --json

# cross-cutting comparison reports (often the richest — a single PDF that
# tables several names) — search the theme itself:
python3 zsxq_fts.py -q "surgical robots TAM competitive landscape 手术机器人" -n 15 --json

# structured filters compose with the text match:
python3 zsxq_fts.py -q "surgical robotics" --bank "Goldman Sachs" --since 2025-09-01 --json
```

Each result row carries: `file_id`, `name`, `bank`, `create_time`, `page_count`,
`tickers`, a `summary` snippet, the BM25 `score`, a ready-to-cite `pdf_url`, and
crucially **`has_card`** + `card_theme` + `card_primary_ticker` (whether this PDF
was already digested — see Step 4).

**Selection.** Union the result sets; dedupe by `file_id`. Prefer:
1. **Cross-company comparison reports** (one PDF covering several peers — the
   `summary`/title names ≥2 of your entities). These are gold for "compare".
2. High BM25 score on the focal and on each peer (cover every side).
3. Bank quality (GS/MS/JPM/UBS/Bernstein/Nomura > regional > unknown), recency,
   sensible `page_count` (12–80 is the sweet spot).

Keep a shortlist of **6–12 file_ids** that together cover the focal *and* every
peer dimension. Note honestly if a peer has no coverage in the library.

## Step 4 — Cards first, then fresh reads

For each shortlisted file_id, check `has_card`:

- **`has_card == true`** → pull the existing card instead of re-reading:
  ```bash
  python3 zsxq_cards.py --get <file_id>
  ```
  The card already holds covered tickers, theme, thesis, and *which comparison
  tables live on which pages* (`key_tables`). If the card answers the dimension,
  cite from it (and the page it points to) without a fresh extraction.
- **`has_card` false / missing** → this PDF needs a deep read (Step 5).

This is the compounding mechanism: the more you use the library, the fewer
fresh reads each question needs.

### Step 4b — PT pre-pass (read-only, before any fresh read)

When ≥2 shortlisted PDFs cover the same company / theme / question, pull what
the PT store already knows **before** re-reading any PDF — it mechanically
exposes same-institute revisions and PT dispersion, and tells the deep-read
agents which revisions to find the trigger for:

```bash
python3 - <<'PY'
import sqlite3
c = sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)  # STRICTLY read-only
for r in c.execute("""SELECT research_institute, rating, price_target, target_currency,
                             report_date, report_file_id, upside_pct
                      FROM price_targets WHERE company_ticker IN ('ISRG','SYK')
                      ORDER BY company_ticker, research_institute, report_date"""):
    print(r)
PY
```

The same institute appearing twice with a different PT / rating = a
**self-revision** (two distinct views, not duplicates). Compute PT dispersion
across institutes (min / median / max, spread %). Writes to this DB remain
exclusively via `scripts/persist_pts.py` (Tier-2 helper) — never raw SQL.

## Step 5 — Deep reads (the tables + figures)

Launch **one Agent-tool subagent per fresh file_id**. This is where the depth
comes from — pull the *actual* tables and charts, not just prose.

> **Memory note (16 GB machine).** Default = **strictly sequential** — one
> Agent-tool subagent at a time; launch the next only after the prior returns.
> Go 2-wide ONLY when `pgrep -lf mem-watch-16gb.sh` shows the watcher running
> AND free RAM is >60% AND the user's Flask `:5001` is the only other load.
> **Never ≥3 concurrent** — the CLAUDE.md sizing table marks 3+ as OOM/thrash
> on this box. Process the 6–12 shortlist sequentially and lean on cards
> (Step 4) to keep fresh reads few. Watcher + thresholds:
> [CLAUDE.md § Workflow Memory Monitoring]. Prefer Agent-tool subagents
> (separate processes, fully reclaimed on exit) over in-process Workflow agents.

Each agent runs the [extraction-agent prompt](#extraction-agent-prompt). Its job
per PDF:

1. `find_pdf.py --file-id <id>` → confirm local path + the citable `pdf_url`.
2. `extract_pdf.py --file-id <id> --header` → narrative text + page markers.
   If `--header` reports image-only pages → `ocr_pdf.py --file-id <id>` first
   (caches OCR back to the DB; the sanctioned write), then re-extract.
3. **Tables:** `extract_tables.py --file-id <id> --json` → comparison tables as
   markdown, page-labelled. This is the key step for "compare" questions — the
   segment×player / metric×company grids come out structured.
4. **Figures/charts:** for a chart whose meaning isn't in the text or a table
   (install-base curve, margin bridge, share trend), `render_pdf_pages.py
   --file-id <id> --pages <n>` → PNG, then **Read the PNG** (you are multimodal)
   and transcribe the axis values / trend into the answer.
5. Return structured JSON (the extraction-agent shape) with every number tagged
   to a `page` and a verbatim original-language `quote`.

## Step 6 — Synthesize the cited answer (and write back)

**Synthesis.** Compose the answer around the *dimensions* (Step 1), not around
the PDFs. For a comparison, lead with a **head-to-head table** (companies as
columns, dimensions as rows) assembled from the extracted broker tables, then
prose per dimension. Rules:

- **Every number cites the PDF page it came from**, in the
  [zsxq citation convention](../zsxq-ideas/SKILL.md#zsxq-citation-convention):
  `[Bank — topic, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)`,
  with a short verbatim original-language quote alongside the figure.
- **Reproduce the actual comparison tables** you pulled (cite the source PDF +
  page under each). Don't paraphrase a table into vague prose — show the grid.
- **A broker's view is a broker's view**, not fact: attribute ("Goldman pegs the
  ortho-robotics TAM at US$2–3bn…"). Never present a sell-side target as truth.
- **Sell-side view evolution (卖方观点演变) — mandatory whenever ≥2 zsxq reports
  inform the answer.** Render a subsection with that exact title next to the
  broker-view content, built from the Step-4b pre-pass + the deep reads:
  1. *Per-institute timeline* — each institute's reports ordered by report date
     (the filename's `-YYMMDD` suffix is the authoritative publication date;
     sanity-check against `create_time`): institute, date, rating, PT, key
     estimates, one-line thesis. Explicitly call out **self-revisions** —
     upgrade/downgrade, PT raised/cut from X to Y, thesis pivot — and the stated
     trigger (earnings print, policy change, channel checks, order data).
  2. *Cross-institute disagreement* — never blend contradictory views into a
     fake consensus. Opposite ratings, PTs >20% apart, or conflicting reads of
     the same datapoint get a disagreement table:
     `Institute | Date | Rating / PT | Core argument | What evidence would prove them right`.
  3. *Every view dated and cited* — each view carries (institute, report date,
     `/zsxq/pdf/<file_id>/<urlencoded-name>` direct-download link). A 2026-03 PT
     and a 2026-06 PT from the same institute are two different views, not
     duplicates.
  Each PT in the timeline also carries the report-date price + implied upside
  per the PT surfacing rule (Notes below) — the Step-4b rows already hold
  `upside_pct`.
- **Be honest about gaps.** If the library covers ISRG well but barely mentions
  a named peer, say so — don't fill the hole from general knowledge and pass it
  off as sourced. General-knowledge bridging is allowed but must be *labelled*
  ("not in the cited reports; general context:").
- **No LLM-API, no fabrication.** Numerical Accuracy rule: every figure must
  string-match a cited PDF's extracted text.

**Write-back (do this every run — it's what makes it an expert system).**

1. **Cards** — for each PDF you deep-read, upsert a card so the next question
   reuses it:
   ```bash
   python3 zsxq_cards.py <<'JSON'
   [{"file_id": <id>, "primary_ticker": "ISRG",
     "covered_tickers": ["ISRG","SYK","MDT"], "theme": "surgical-robotics",
     "thesis": "<1-paragraph what-this-report-argues>",
     "has_comparison_table": true,
     "key_tables": "p.5 segment×player TAM grid; p.11 procedure-volume by company",
     "key_figures": "p.4 da Vinci install-base CAGR",
     "rating": "<broker call if any>"}]
   JSON
   ```
2. **Graph edges** — for each competitive/supply fact the PDFs establish, write
   it to the graph with the PDF as provenance (so `/zep/` shows the source and
   the next graph query is richer). Companies only; relations `COMPETES_WITH` /
   `SUPPLIES`; ≤10 edges/entity (per [[build-knowledge-graph]]):
   ```python
   from manual_graph import add_entity, add_edge, add_episode
   add_episode("pdf_585582881584284", name="GS China Medtech Going Global",
               source_desc="zsxq #585582881584284")
   add_entity("Intuitive Surgical", labels=["Company"], ticker="ISRG")
   add_entity("Stryker", labels=["Company"], ticker="SYK")
   add_edge("Stryker", "Intuitive Surgical", relation="COMPETES_WITH",
            fact="Both lead surgical robotics — Mako (ortho) vs da Vinci (soft-tissue); GS segments them as adjacent TAMs.",
            source="pdf_585582881584284")
   ```
   The `pdf_<file_id>` episode slug renders as a clickable PDF link in `/zep/`
   (graph_mirror `_episode_url` already handles the `pdf_` prefix). This is the
   first time PDFs feed the graph — every run grows it.

## 延伸观看 / Further viewing — explainer videos (optional, but default to including)

When this answer covers something a reader would struggle to picture from prose alone — the compared products' or peers' mechanics (a robot's actuators / harmonic reducers / ball-screws / force sensors), a manufacturing or scientific process, a complex product architecture, or any hard-to-visualize device or process the broker-grounded answer hinges on — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the answer is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**延伸观看 / Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept. English-only reports use `**Further viewing**`.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(B站，部分地区或需登录)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Step 7 — Verify before delivering

Spot-check 3–5 numbers from the answer against their cited PDFs' extracted text
(`extract_pdf.py --file-id <id> --pages <n>` then grep the figure). Any number
that doesn't string-match its cited page gets fixed or dropped (Numerical
Accuracy rule). Confirm every `pdf_url` is well-formed. If ≥2 zsxq reports
informed the answer, confirm the **Sell-side view evolution (卖方观点演变)**
subsection is present — per-institute timeline with dated/cited views, plus the
disagreement table wherever institutes conflict.

## Output mode

- **Default: answer in chat.** A comparison/explanation answer is a one-off —
  per [CLAUDE.md § One-off Explanations], do NOT save a file unless the user
  asks ("save this", "write a report", "保存").
- **If the user asks to save:** a 2–4 company comparison → `/compare-companies`
  format under `reports/compare/`; a single-topic explainer →
  `reports/explanation/<slug>.md`. Filename must start with English/pinyin per
  the [filename rule](../../../CLAUDE.md#research-report-filenames-mandatory--must-include-english--pinyin-name).
  Then commit per the standard workflow. The *cards and graph edges from
  write-back are persisted regardless* of whether the prose answer is saved.

## Extraction-agent prompt

Use verbatim for each parallel deep-read agent (subagent_type `general-purpose`),
plugging in the file_id and the question's dimensions:

```
Use the zsxq-analyze skill's scripts to deep-read file_id <N> from db/zsxq.db,
to help answer this question: "<the user's question>".
Focus on these dimensions: <dimensions from Step 1>.

Steps:
1. python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --file-id <N>
   (note the pdf_url and local path)
2. python3 .claude/skills/zsxq-analyze/scripts/extract_pdf.py --file-id <N> --header
   If it reports image-only pages, first run
   python3 .claude/skills/zsxq-analyze/scripts/ocr_pdf.py --file-id <N>
   then re-run extract_pdf.
3. python3 .claude/skills/zsxq-analyze/scripts/extract_tables.py --file-id <N> --json
   (pull every comparison / metric table as markdown — this is the priority)
4. For any chart that carries the answer and isn't in the text/tables:
   python3 .claude/skills/zsxq-analyze/scripts/render_pdf_pages.py --file-id <N> --pages <p>
   then Read the PNG and transcribe the axis values / trend.

Return ONLY raw JSON (no prose, no fences):
{
  "file_id": <N>,
  "name": "<PDF name>",
  "bank": "<publisher/bank or null>",
  "pdf_url": "<from find_pdf>",
  "covered_entities": ["<company/ticker>", ...],
  "theme": "<short theme slug, e.g. surgical-robotics>",
  "thesis": "<1-paragraph: what THIS report argues>",
  "comparison_tables": [
    {"page": 5, "title": "segment x player TAM", "markdown": "<the table as markdown>"}
  ],
  "key_numbers": [
    {"entity": "ISRG", "metric": "da Vinci systems placed", "value": "232",
     "page": 7, "quote": "<verbatim original-language sentence with the number>"}
  ],
  "figures": [
    {"page": 4, "describes": "da Vinci install-base CAGR", "readout": "<what the chart shows, transcribed>"}
  ],
  "broker_call": {"rating": "<or null>", "price_target": "<or null>", "page": <n>},
  "gaps": "<dimensions the user asked about that this PDF does NOT cover>"
}

Every key_numbers/comparison_tables/figures entry must carry the page where it
appears, and quotes must be the ORIGINAL printed text (EN/中文/日本語), never the
翻译精华 summary paraphrase. String-match each number to the extracted text.
```

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

- **No LLM API, ever.** You read and synthesize; subagents read and extract.
  No embeddings, no vector store, no `call_claude`. (Project hard rule.)
- **DB writes go through the helpers only.** Reads of `pdf_files` are free;
  the only writes are: `ocr_pdf.py` (OCR cache), `zsxq_cards.py` (cards),
  `manual_graph.py` (graph), `scripts/persist_pts.py` (price targets if the
  PDFs carry broker calls). Never raw SQL against any DB. (Tier-2/Tier-3 rules.)
- **Cover every side of a comparison.** Run a retrieval query per entity; a
  one-sided answer (rich on the focal, thin on peers) is a failure mode — flag
  thin coverage rather than papering over it.
- **Tables are the point.** For "compare" questions, the head-to-head grid from
  `extract_tables.py` (or a vision-read of the page) is the deliverable; prose
  supports it. `find_tables` occasionally misreads a chart as a sparse table —
  sanity-check before reproducing.
- **Persist the learning.** Always write cards + graph edges in Step 6, even
  when the prose answer stays in chat. That's the difference between a search
  box and an expert system.
- **Opportunistically persist PTs.** If a deep-read PDF states a price target,
  pipe it to `scripts/persist_pts.py --replace` (surfaces in `/pt`).
- **PT surfacing rule applies here too.** Any broker rating / PT quoted in the
  answer must carry the report-date price and implied upside from
  `persist_pts.py`'s stdout `rows` (`report_date_price`, `upside_pct`), e.g.
  `GS Buy, TP $1,159 vs $1,030 @ 2026-05-28 → +12.5%`. Write `report-date
  price n/a` if it's null; never substitute today's spot. See
  [`reference/pt_extraction.md`](../../../reference/pt_extraction.md)
  § "Surfacing rule".

## Prerequisites

Project-root modules (this skill's retrieval + memory layer):

- `zsxq_fts.py` — ranked trigram-FTS retrieval over `db/zsxq.db`
  (`pdf_files_fts`, built/backfilled by `zsxq_common.init_db`). Run
  `python3 zsxq_fts.py --rebuild` once if the index is missing.
- `zsxq_cards.py` — agent-curated card layer (`pdf_cards`); the
  read-reuse + write-back memory.

Sibling-skill scripts (the extraction layer; already installed):

- [[zsxq-analyze]] — `scripts/find_pdf.py`, `scripts/extract_pdf.py`,
  `scripts/ocr_pdf.py`, `scripts/render_pdf_pages.py`, and the new
  `scripts/extract_tables.py` (structured tables via PyMuPDF `find_tables`).

Cross-document layer:

- [[build-knowledge-graph]] — `manual_graph.py` write API + the COMPETES_WITH /
  SUPPLIES / companies-only / ≤10-edges discipline used in Step 6.
- `graph_mirror.py` — `search()` for the focal-entity neighborhood (Step 2).

Conventions reused:

- [[zsxq-ideas]] — the [zsxq citation convention](../zsxq-ideas/SKILL.md#zsxq-citation-convention)
  (page-anchored link + verbatim source quote) and the per-PDF extraction-agent
  pattern (sequenced per the Step 5 memory note).
