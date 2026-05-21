# DATABASE.md — SQLite databases in this repo

Every database lives under `db/` (with two exceptions: the YouTube subproject keeps its own, and a few 0-byte legacy files at repo root are unused placeholders). Each file is a single SQLite database owned by one Python module — the *owner* column tells you which file creates and writes the schema.

## Quick index

| File | Owner | Purpose | Size |
|---|---|---|---|
| [db/zsxq.db](db/zsxq.db) | `zsxq_common.py` | zsxq PDF library — downloads, classifications, user ratings/comments | ~22 MB |
| [db/financial_reports.db](db/financial_reports.db) | `fetch_financial_report.py` | US SEC EDGAR filings (10-K / 10-Q / 8-K) catalog | ~9 MB |
| [db/cninfo_reports.db](db/cninfo_reports.db) | `fetch_cninfo_report.py` | Chinese A-share + HK filings catalog (from CNINFO) | ~1 MB |
| [db/notes.db](db/notes.db) | `notes_app.py` | Notes app — drag-and-drop earnings PDFs + per-note markdown comments | ~78 KB |
| [db/report_annotations.db](db/report_annotations.db) | `report_annotations.py` | User ratings/comments on the `/reports/` markdown index (this is the NEW one) | ~12 KB |
| [db/market_cap_cache.db](db/market_cap_cache.db) | `market_cap_cache.py` | Daily market cap + FX rate cache for the `/reports/` market-cap column | ~28 KB |
| [db/indicators.db](db/indicators.db) | `indicators/app.py` | Cross-asset market indicators (liquidity, credit, vol) — snapshots + time-series history | ~180 KB |
| [db/graph_mirror.db](db/graph_mirror.db) | `graph_mirror.py` | SQLite mirror of the KuzuDB knowledge graph (entities, edges, episodes, communities) + FTS5 | ~400 KB |
| [db/markdown_reports.db](db/markdown_reports.db) | `ingest/graphiti_ingest.py` | Tracks which `reports/*.md` files have been indexed into Graphiti | ~12 KB |
| [db/knowledge_graph.db](db/knowledge_graph.db) | — | **Empty placeholder.** Legacy path from before the Kuzu migration. Safe to delete. | 0 B |
| [youtube/video_summaries.db](youtube/video_summaries.db) | `youtube/analysis_video.py` | YouTube transcript chunks + per-chunk summaries (separate subproject) | varies |
| `zsxq.db`, `graph_mirror.db`, `knowledge_graph.db` (repo root) | — | **Empty placeholders** from old paths. Real files live under `db/`. Safe to delete. | 0 B |

---

## Detail per database

### `db/zsxq.db` — zsxq report library

The backbone of the `/zsxq/` viewer. One row per downloaded PDF, with classification + user annotations layered on top.

Schema is in [zsxq_common.py](zsxq_common.py) (search `CREATE TABLE pdf_files`).

**Table `pdf_files`** (primary key: `file_id`):

| Column | Type | What it is |
|---|---|---|
| `file_id` | INTEGER PK | zsxq's own file ID |
| `name` | TEXT | Original PDF filename |
| `topic_id`, `topic_title`, `topic_json` | INTEGER, TEXT, TEXT | Source post on zsxq |
| `summary` | TEXT | Short summary scraped from the zsxq post |
| `local_path` | TEXT | Path under `pdf_files/` |
| `file_size`, `page_count` | INTEGER | Basic file stats |
| `create_time`, `downloaded_at`, `indexed_at` | TEXT (ISO) | Lifecycle timestamps |
| `tickers`, `tags` | TEXT (comma-sep) | User-editable classification |
| `ai_related`, `robotics_related`, `semiconductor_related`, `energy_related` | INTEGER (0/1) | Topic flags from the classifier |
| `categories_analysis`, `categories_prompt`, `categories_raw` | TEXT | LLM categorisation trace |
| `ai_robotics_analysis`, `ai_robotics_related`, `ai_prompt`, `ai_raw_response` | TEXT, INTEGER, TEXT, TEXT | Legacy AI-relatedness columns (kept for backwards compat) |
| **`user_rating`** | INTEGER (1-5) | Human star rating |
| **`claude_rating`** | INTEGER (1-5) | LLM star rating |
| **`comment`**, `comment_updated_at` | TEXT, TEXT | Markdown comment per PDF |
| `bank` | TEXT | Brokerage / source bank |
| `group_id` | TEXT | zsxq group |
| `query_term` | TEXT | Search term that surfaced the file |
| `obsidian_path` | TEXT | Mirror path inside the Obsidian vault |
| `graphiti_indexed_at` | TEXT | When this PDF was ingested into the knowledge graph |
| `skipped` | INTEGER (0/1) | Marked as "don't process" |
| `ocr_text`, `ocr_at` | TEXT, TEXT | Cached OCR output for image-only PDFs (from `.claude/skills/zsxq-analyze/scripts/ocr_pdf.py`) |

The classification / OCR / ratings layers all attach to the same row, so you can query "all 5-star AI-related PDFs with comments" in one go.

---

### `db/financial_reports.db` — US SEC filings

Owned by [fetch_financial_report.py](fetch_financial_report.py), served at `/sec/` via the SEC blueprint.

**Table `reports`** (primary key: `id`):

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `ticker` | TEXT | e.g. `AAPL`, `NVDA` (no exchange prefix) |
| `company_name` | TEXT | Company name from EDGAR |
| `period`, `period_of_report` | TEXT | Fiscal period this filing covers |
| `form_type` | TEXT | `10-K`, `10-Q`, `8-K`, `DEF 14A`, etc. |
| `filed_date` | TEXT (YYYY-MM-DD) | EDGAR filing date |
| `accession_no` | TEXT | EDGAR accession (uniquely identifies a filing) |
| `local_path` | TEXT | Saved-to path under `financial_reports/<TICKER>/` |
| `file_size` | INTEGER | Bytes |
| `created_at` | TEXT | When this row was inserted |
| `comment`, `comment_updated_at` | TEXT | Per-filing user comment (markdown) |
| `graphiti_indexed_at` | TEXT | When this filing was ingested into the knowledge graph |

---

### `db/cninfo_reports.db` — Chinese A-share / HK filings

Owned by [fetch_cninfo_report.py](fetch_cninfo_report.py), served at `/cn/`. Same idea as the SEC db, but for CNINFO.

**Table `cninfo_reports`** (primary key: `id`):

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `ticker` | TEXT | `SZSE:002050`, `SSE:688802`, `HKEX:2513` |
| `market` | TEXT | `SSE` / `SZSE` / `HKEX` etc. |
| `stock_code` | TEXT | Numeric code without exchange prefix |
| `company_name` | TEXT | Chinese company name |
| `period` | TEXT | Reporting period |
| `form_type` | TEXT | Annual / Quarterly / Other categories |
| `filed_date` | TEXT | Disclosure date |
| `local_path` | TEXT | Path under `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/` |
| `announcement_id` | TEXT | CNINFO's own announcement ID (dedup key) |
| `file_size` | INTEGER | Bytes |
| `comment` | TEXT | User comment |
| `created_at` | TEXT | Row insert timestamp |

---

### `db/notes.db` — Notes app

The Notes blueprint (`/notes/`) shows one row per uploaded earnings PDF with rich filename parsing. Owned by [notes_app.py](notes_app.py).

**Table `notes`** (primary key: `id`):

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PK | |
| `name` | TEXT | Original filename (dedup key) |
| `local_path` | TEXT | Stored under `MANUAL_REPORT_DIR/<ticker>/` |
| `ticker` | TEXT | Parsed from filename |
| `type` | TEXT | `10K` / `10Q` / `8K` / `slide` / `investor` |
| `quarter` | TEXT | e.g. `Q1` |
| `report_date` | TEXT | Reporting date |
| `sector`, `competitors` | TEXT | Free-form metadata |
| `pinned` | INTEGER (0/1) | Pinned in the UI |
| `comment`, `comment_updated_at` | TEXT | Per-note markdown comment |
| `created_at` | TEXT | Row insert |

---

### `db/report_annotations.db` — `/reports/` user annotations *(new)*

The one we just added. Owned by [report_annotations.py](report_annotations.py). Separate from `db/zsxq.db` and `db/notes.db` so each viewer keeps its own annotation namespace.

**Table `annotations`** (primary key: `pair_key`):

| Column | Type | Meaning |
|---|---|---|
| `pair_key` | TEXT PK | `<bucket>/<normalized-stem>` — the same key reports_viewer uses to collapse EN/ZH/DOCX siblings into a single row. One annotation per logical report regardless of which language file you opened. |
| `rating` | INTEGER (1-5, NULL=unrated) | Star rating |
| `comment` | TEXT | Markdown comment |
| `rated_at` | TEXT (ISO UTC) | Last rating change |
| `comment_updated_at` | TEXT (ISO UTC) | Last comment edit |

Written via `POST /reports/rate/<pair_key>` and `POST /reports/comment/<pair_key>` (handlers in [reports_viewer.py](reports_viewer.py)).

---

### `db/market_cap_cache.db` — market cap + FX cache

Backs the Market Cap column on `/reports/`. Owned by [market_cap_cache.py](market_cap_cache.py).

**Table `market_cap_cache`** (composite key: `ticker, fetch_date`):

| Column | Type | Meaning |
|---|---|---|
| `ticker` | TEXT | `EXCHANGE:CODE` |
| `fetch_date` | TEXT (YYYY-MM-DD) | Day of fetch — one entry per ticker per day |
| `market_cap` | INTEGER | Native-currency value |
| `currency` | TEXT | `USD` / `CNY` / `HKD` / etc. |
| `fetched_at` | REAL (epoch) | Exact fetch timestamp |

**Table `fx_rates`** (composite key: `currency, fetch_date`):

| Column | Type | Meaning |
|---|---|---|
| `currency` | TEXT | e.g. `HKD`, `CNY` |
| `fetch_date` | TEXT (YYYY-MM-DD) | |
| `units_per_usd` | REAL | Conversion rate (HKD per USD, etc.) |
| `fetched_at` | REAL (epoch) | |

The reports page renders immediately with `—` placeholders and a background thread fills in missing tickers on first call of the day; reload picks them up.

---

### `db/indicators.db` — market indicators time series

Owned by [indicators/app.py](indicators/app.py), served at `/indicators/`.

**Table `snapshots`** (primary key: `id`):

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PK | |
| `fetched_at` | INTEGER (epoch) | When snapshot was captured |
| `data_json` | TEXT | Full JSON blob — all indicator values at that moment |

**Table `history`** (composite key: `symbol, date`):

| Column | Type | Meaning |
|---|---|---|
| `symbol` | TEXT | Indicator symbol (e.g. `^VIX`, `MOVE`) |
| `date` | TEXT (YYYY-MM-DD) | |
| `value` | REAL | Closing value |

---

### `db/graph_mirror.db` — knowledge-graph SQLite mirror

Read-only mirror of the live KuzuDB knowledge graph for fast SQL queries + FTS search. Owned by [graph_mirror.py](graph_mirror.py). Used by [isolate_nonsense_entities.py](isolate_nonsense_entities.py), [merge_duplicate_entities.py](merge_duplicate_entities.py), [restore_valid_entities.py](restore_valid_entities.py), and the Zep app at `/zep/`.

| Table | Purpose |
|---|---|
| `entities` | One row per graph node — `uuid`, `name`, `labels_json`, `summary`, `isolated` (soft-delete flag), `rating`, `updated_at` |
| `edges` | One row per relationship — `src_uuid` → `tgt_uuid`, `fact` (LLM-generated sentence), `episodes_json` (source episodes), `deprecated` flag |
| `episodes` | Source episodes (chunks of text that produced graph data) — `uuid`, `name`, `source_desc`, `created_at` |
| `communities` | LLM-clustered groups of entities — `id`, `name`, `summary`, `member_count` |
| `community_members` | M:N link between `community_members.entity_uuid` and `communities.id` |
| `pending_deletions` | Soft-delete queue — `uuid`, `type`, `reason`, `queued_at` |
| `*_fts*` | FTS5 virtual tables + their sidecars for full-text search over entities/edges/communities |

---

### `db/markdown_reports.db` — Graphiti ingest tracker

Bookkeeping for which markdown reports under `reports/` have been ingested into the knowledge graph. Owned by [ingest/graphiti_ingest.py](ingest/graphiti_ingest.py).

**Table `markdown_reports`**:

| Column | Type | Meaning |
|---|---|---|
| `path` | TEXT | Relative path under `reports/` |
| `indexed_at` | TEXT | When the file was last sent to Graphiti |

Currently empty in this checkout — populated on first ingest run.

---

### `youtube/video_summaries.db` — YouTube transcript chunks

Lives outside `db/` because the `youtube/` subproject is largely self-contained. Owned by [youtube/analysis_video.py](youtube/analysis_video.py), viewed via [youtube/viewer.py](youtube/viewer.py).

**Table `video_chunks`**:

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PK | |
| `video_id` | TEXT | YouTube video ID |
| `chunk_index` | INTEGER | Sequential chunk number within a video |
| `start_seconds`, `end_seconds` | INTEGER | Time range covered |
| `start_label`, `end_label` | TEXT | Human-readable timestamps (`mm:ss`) |
| `transcript` | TEXT | Raw transcript text for this chunk |
| `summary` | TEXT | LLM summary of the chunk |
| `analyzed_at` | TEXT | When the summary was generated |

---

## Conventions

A few patterns repeat across these databases — worth knowing when you add a new one:

- **Path convention**: every database lives at `db/<name>.db` (loaded via `Path(__file__).parent / "db" / "<name>.db"`).
- **Comments are markdown**: any `comment` column stores raw markdown. The `comment_updated_at` sibling column is ISO UTC. Renderable in the UI via [md_comment_widget.py](md_comment_widget.py).
- **Ratings are 1–5 stars**: `user_rating`, `claude_rating`, and `annotations.rating` all use 1–5 with `NULL` (or 0) meaning unrated.
- **Time format**: prefer ISO 8601 strings (`2026-05-21T22:03:00Z`) over epoch ints for human-readable timestamps. Epoch reals (`REAL`) are used only when sub-second precision matters (`fetched_at` columns).
- **Owner module = schema source of truth**: search the owner file for `CREATE TABLE` to see the canonical schema; don't rely on this doc alone.
