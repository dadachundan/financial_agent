# Financial Agent — Architecture Overview

> **Looking for database schemas?** See [DATABASE.md](DATABASE.md) — single source of truth for every SQLite file under `db/`, its owner module, tables, and key columns.

## Entry Point

**`main.py`** — Unified Flask app on port 5001 (default). Registers these blueprints:
- `/zep/*` — Knowledge graph UI
- `/zsxq/*` — ZSXQ PDF viewer
- `/sec/*` — US SEC filings
- `/cn/*` — A-share & HK reports
- `/reports/*` — Research-report markdown viewer
- `/indicators/*` — Market indicators dashboard
- `/pt/*` — Sell-side price-target viewer
- `/vol/*` — Options volatility dashboard (IV / skew / VIX regime)

---

## Flask Sub-Apps

### `zep_app.py` — Knowledge Graph UI
Hand-curated knowledge graph. The only graph DB is `db/graph_mirror.db`
(SQLite); the previous KuzuDB / graphiti-core stack and its LLM-driven
ingest pipeline were removed on 2026-06-02. See
[CLAUDE.md](CLAUDE.md) — "NEVER call the Claude API".
- **DB**: `db/graph_mirror.db` (SQLite + FTS5)
- **Writes**: [manual_graph.py](manual_graph.py) — `add_entity`, `add_edge`,
  `add_episode`. Claude (the agent) reads source documents in conversation
  and curates entities + edges directly.
- **Reads**: Flask blueprint at `/zep/` (browse, search, edit, isolate, rate)

#### Graph & Entity Routes
| Method | Path | Description |
|--------|------|-------------|
| GET | `/zep/` | Serve `zep.html` SPA |
| GET | `/zep/search` | FTS5 search → `{nodes, edges, episodes}` |
| GET | `/zep/entities` | Paginated entity list |
| GET | `/zep/entities/unassigned` | Entities not in any community (non-isolated) |
| GET | `/zep/entity-community-map` | `{uuid: community_id}` for all assigned entities |
| GET | `/zep/edges` | Paginated edge list |
| GET | `/zep/stats` | `{node_count, edge_count, episode_count, community_count}` |
| POST | `/zep/entities/<uuid>/rate` | Set star rating |
| POST | `/zep/entities/<uuid>` (PATCH) | Edit name / summary |
| POST | `/zep/entities/<uuid>/isolate` | Hide entity from graph |
| GET | `/zep/entities/<uuid>/edges` | Edges for one entity |
| POST | `/zep/edges/<uuid>/deprecate` | Deprecate an edge |
| POST | `/zep/edges/<uuid>` (PATCH) | Edit edge fact / name |

#### Community Routes
| Method | Path | Description |
|--------|------|-------------|
| GET | `/zep/communities` | Paginated community list (with `member_count`) |
| GET | `/zep/communities/<id>` | Community detail + member list |
| POST | `/zep/communities` | Create community from seed entity (BFS assigns all reachable) |
| DELETE | `/zep/communities/<id>` | Delete community; CASCADE removes members |
| DELETE | `/zep/communities/<id>/members/<uuid>` | BFS-remove entity + all connected members |
| POST | `/zep/build-communities` | SSE stream: deterministic label-propagation (no LLM) |
| DELETE | `/zep/communities/singletons` | Delete all 1-member communities |

#### Removed routes (return 410 Gone)
`/zep/ingest`, `POST /zep/upload-pdf`, `POST /zep/refresh-mirror`,
`POST /zep/entities/isolate-persons`, `POST /zep/clear` — all called the
LLM API and were removed when the auto-ingest pipeline was deleted.

### `fetch_financial_report.py` — US SEC Reports
Download SEC 10-K / 10-Q / 8-K / 20-F filings from EDGAR.
- Key routes: `GET /sec/` (UI), `POST /sec/download` (SSE stream), `GET /sec/reports` (JSON), `GET /sec/file/<id>`
- **DB**: `db/financial_reports.db`
- **Storage**: `financial_reports/<TICKER>/`
- Rate-limited: ≤10 req/sec to SEC EDGAR

### `fetch_cninfo_report.py` — A-share & HK Reports
Download A-share (SSE/SZSE) and HK (HKEX) reports via CNINFO.
- Key routes: `GET /cn/` (UI), `POST /cn/download` (SSE), `GET /cn/reports` (JSON), `GET /cn/file/<id>`
- **DB**: `db/cninfo_reports.db`
- **Storage**: `cninfo_reports/<EXCHANGE>/<CODE>/`

### `reports_viewer.py` — Research Reports Index
Markdown viewer for research reports written by the `company-research`, `sec-report-summary`, and `equity-research:*` skills.
- Key routes: `GET /reports/` (index, recursive scan + EN/ZH collapse + sector / report-type / DOCX filters + market-cap column), `GET /reports/view/<rel>` (render with marked.js + mermaid + Obsidian-highlight extension), `GET /reports/view/charts/<name>` (PNG assets)
- **Sector mapping**: `sector_map.py` — hardcoded `EXCHANGE:CODE → sector` table sourced from the two watchlist text files (`🇨🇳chinese.txt`, `🤪PER SECTOR.txt`); also exports `to_yfinance()` for converting EXCHANGE:CODE → yfinance ticker suffix
- **Market cap**: `market_cap_cache.py` — per-day sqlite cache at `db/market_cap_cache.db`. First call of the day fetches missing tickers in a parallel background thread (8 workers); the page renders immediately with `—` placeholders and reload picks up the populated cache. Stores `(market_cap, currency)`; display tags non-USD values.
- **User annotations** (Rating + Comment): `report_annotations.py` — sqlite at `db/report_annotations.db`, table `annotations(pair_key PK, rating, comment, rated_at, comment_updated_at)`. One row per pair_key so EN/ZH/DOCX siblings share a single annotation. Star widget (1-5, click same star to clear) posts to `/reports/rate/<pair_key>`; comment cell uses `md_comment_widget.py` (EasyMDE editor) posting to `/reports/comment/<pair_key>`. Pair keys are URL-encoded for path use; Flask `<path:>` converter decodes them back.
- **Storage**: `reports/` (tracked in git)
  - `reports/company/<Slug>/<file>.md` — listed (public) company research (EN + ZH coexist; ZH suffix `_zh` or `_CN`). `Slug` is `<ChineseName>_<EXCHANGE><CODE>`, e.g. `双林股份_SZSE300100`.
  - `reports/unlisted/<ChineseName>/<file>.md` — private / unlisted-company research (e.g. `unlisted/智平方科技/`). Shown as Type **unlisted** with its own pill colour.
  - `reports/sector/<file>.md` — sector / thematic overviews
  - `reports/compare/<file>.md` — head-to-head comparisons
  - `reports/earnings/<TICKER>_<YYYYMMDD>.md` — quarterly earnings notes
  - `reports/charts/<file>.png` — shared chart PNGs; relative `charts/foo.png` refs in any nested doc are rewritten client-side to `/reports/view/charts/foo.png`

### `indicators/` — Market Indicators Dashboard
Real-time cross-asset market indicators: liquidity, credit, volatility, and cross-asset signals.
- **Entry**: `indicators/app.py` exports `indicators_bp` (Blueprint) + `init_db()`
- **Data**: `indicators/data_fetcher.py` — yfinance (all direct tickers + computed spreads/ratios); optional FRED API for HY/IG OAS (requires `FRED_API_KEY` in `config.py`)
- **DB**: `indicators/db.py` → `db/indicators.db` (snapshots + history tables)
- **Cache**: 15-minute TTL; refresh triggered in background on stale load, or on-demand via `POST /indicators/api/refresh`
- **Indicators**: 3M T-bill, 10Y–3M spread, HY/IG OAS, HYG/LQD ETF, VIX, VVIX, VIX term slope (VIX9D/VIX3M), SPY, 10Y yield, DXY, Gold, WTI Crude

| Method | Path | Description |
|--------|------|-------------|
| GET | `/indicators/` | Dashboard SPA |
| GET | `/indicators/api/config` | Indicator catalogue (metadata) |
| GET | `/indicators/api/snapshot` | Latest cached snapshot; triggers background refresh if stale |
| POST | `/indicators/api/refresh` | Synchronous refresh, returns new data |
| GET | `/indicators/api/history/<id>` | Full DB history for one indicator |

---

### `zsxq_viewer.py` — ZSXQ PDF Viewer
Browser for the 知识星球 research group PDF library.
- Key routes: `GET /zsxq/` (UI), `GET /zsxq/pdfs` (JSON), `GET /zsxq/pdf/<id>`, `POST /zsqx/rate/<id>`, `POST /zsxq/comment/<id>`
- **DB**: `db/zsxq.db`
- Mounts `pdf_viewer.register(zsxq_bp, source="zsxq", path_provider=…)` for the in-browser PDF viewer. Sibling registrations exist in `fetch_financial_report.py` (sec), `fetch_cninfo_report.py` (cn), and `notes_app.py` (manual) so all four PDF libraries share the same viewer + comment store.

### `zsxq_fts.py` / `zsxq_cards.py` — zsxq retrieval/memory layer (the "PDF expert system")
The query-time layer beneath the [`zsxq-expert`](../.claude/skills/zsxq-expert/SKILL.md) skill.
- `zsxq_fts.py` — ranked **full-text retrieval** over `db/zsxq.db` via the `pdf_files_fts` FTS5 index (trigram tokenizer → bilingual EN+中文 substring search; BM25 ranked; LIKE fallback for <3-char queries). `search(query, ...)` + CLI; structured filters (bank / ticker / since); surfaces `has_card` per hit. Read-only; the index is created/backfilled by `zsxq_common.init_db` (run `python3 zsxq_fts.py --rebuild` to force).
- `zsxq_cards.py` — the agent-curated **card** store (`pdf_cards` table): each deep read writes back covered tickers / theme / thesis / which comparison tables live on which pages, so re-reads are skipped and the library compounds. `upsert_card` / `get_card` / `cards_for_ticker` + batch-JSON CLI. The `embedding`/`embed_model` columns are reserved for an optional future *local* (no-API) semantic layer.
- Table extraction: `.claude/skills/zsxq-analyze/scripts/extract_tables.py` recovers structured comparison tables as markdown via PyMuPDF `find_tables` (no new dep); image-only pages fall back to `render_pdf_pages.py` + vision.
- Both modules resolve `DB_PATH` via `db_paths.db_path` (FINAGENT_DB_DIR-redirectable; covered by `TestFinagentDbDirOverride`). No LLM API — Claude-the-agent is the reader/synthesizer.

### `pdf_viewer.py` — In-browser PDF viewer with selection-anchored markdown comments
PDF.js-based reader for any PDF library on disk. Mirrors the UX of the `/claude-reports` markdown viewer (right-rail comment cards anchored to selected text via a TextQuoteSelector). Source-agnostic — each parent app registers it via `register(bp, *, source, path_provider)` where `path_provider(file_id) -> {local_path, name, title}` resolves the PDF for that source.
- Key routes (mounted on the parent blueprint; e.g. `/zsxq`, `/sec`, `/cn`, `/manual-report`):
  - `GET /<bp>/pdf-viewer/<file_id>` — viewer HTML
  - `GET /<bp>/pdf-viewer-pdf/<file_id>` — raw PDF bytes for PDF.js
  - `GET/POST/PATCH/DELETE /<bp>/pdf-inline-comments[/<id>]` — CRUD (results filtered by source)
  - `POST /<bp>/pdf-page-ocr`, `POST /<bp>/pdf-ocr-region` — OCR endpoints
- **DB**: `db/notes.db` tables `pdf_inline_comments` and `pdf_page_ocr`, both namespaced by `(source, file_id)`.
- Vector pages → native text selection captures quote+prefix+suffix and re-anchors via whitespace-normalized index lookup on reload.
- Scanned pages (empty text layer) auto-enable a region-drag overlay; the dragged rect is OCR'd server-side so even scanned-only reports get the same quote-based UX.

### `pdf_inline_comments.py` — SQLite layer for PDF inline comments
Stores selection-anchored markdown comments in `db/notes.db` keyed by `(source, file_id, page)` where `source ∈ {zsxq, sec, cn, manual}` and `file_id` is the parent-table primary key (`pdf_files.file_id` / `reports.id` / `cninfo_reports.id` / `notes.id`). An `origin` column (`'inline'` / `'synced'`) distinguishes user-typed in-browser comments from PDF-extracted annotations mirrored in by `replace_synced(source, file_id, annotations)` — every `*/sync-annotations` route now calls this helper so the 📌-extracted annotations flow into the *same* table as in-browser comments. A row with an empty `body` is a *pure highlight* (no comment text); the viewer renders just the `<mark>` on the page and shows no rail card. Clicking such a mark pops a tiny [💬 Add comment / 🗑 Delete] toolbar so the user can upgrade or remove it. `init_db()` self-heals existing tables by adding the `source` (default `'zsxq'`) and `origin` (default `'inline'`) columns if missing; a standalone migration script `migrate_add_source_to_pdf_tables.py` is also provided for explicit pre-deploy migration.

The `/zsxq/feed` route ("Research Notes") reads from `pdf_inline_comments` across all four sources to render one card per PDF, falling back to each parent table's legacy `comment` column only when no inline rows exist. Cards carry a colored source pill (ZSXQ blue / SEC green / CN red / MANUAL gray) plus a per-card badge (broker name for zsxq, ticker for the others) and link out to the source's own `/pdf-viewer/<id>` endpoint.

### `pdf_page_ocr.py` — Per-page OCR cache for synthetic text layers
For scanned PDFs (no embedded text) the viewer requests `/<bp>/pdf-page-ocr` per page; this module renders the page via fitz, runs ocrmac (Apple Vision) to get word boxes, and caches them in `db/notes.db` table `pdf_page_ocr (source, file_id, page, words_json, ocr_at)`. The viewer injects those words as positioned transparent `<span>`s into PDF.js's text layer so native browser text selection works the same way it does on vector PDFs — and the same way Apple Preview's "select text on a scanned PDF" feature works (Preview is also calling Apple Vision under the hood). Like `pdf_inline_comments`, the cache namespaces by `(source, file_id, page)` and self-heals legacy schemas.

---

## Data Pipeline

### Download

| Script | Purpose |
|--------|---------|
| `download/zsxq_downloader.py` | Selenium → zsxq API → PDFs → `zsxq.db` |
| `download/bulk_download_10k_10q_8k.py` | Batch SEC 10-K/10-Q/8-K + 20-F/40-F/6-K for watchlist tickers |
| `download/bulk_download_ashare.py` | Batch CNINFO A-share + HK annual/semi-annual/quarterly reports |

### Knowledge graph (hand curation, no auto-ingest)

| Script | Purpose |
|--------|---------|
| `manual_graph.py` | The only write path to `db/graph_mirror.db`: `add_entity`, `add_edge`, `add_episode`, bulk helpers. Idempotent by name. Used by Claude (the agent) when curating from `reports/*.md`. |

---

## LLM

The project no longer calls any LLM API. All summarisation, classification,
and entity/edge extraction is done by Claude (the agent) in conversation
using `Read` / `Edit` / `Bash` + `manual_graph.py`. See
[CLAUDE.md](CLAUDE.md) for the full rule. `langfuse_monitor.py` is kept
for ad-hoc tracing of one-off manual calls.

---

## Utility Modules

| File | Purpose |
|------|---------|
| `graph_mirror.py` | SQLite knowledge-graph schema + read/write helpers; owns all community logic (`build_communities`, `create_community_from_seed`, `remove_community_bfs`); entity lifecycle: `isolate_entity`, `merge_entities` |
| `md_comment_widget.py` | Reusable EasyMDE markdown editor modal + image-paste-to-upload blueprint |
| `nav_widget2.py` | Shared navbar HTML injected into every sub-app template |
| `ticker_names.py` | Background-thread loader of A-share/HK `{code: company_name}` map (AKShare); weekly cache |
| `langfuse_monitor.py` | OTel-native Langfuse tracing (legacy / ad-hoc — no project code calls it automatically) |
| `tradingview.py` | Selenium-based TradingView watchlist scraper (experimental) |
| `config.py` | API keys (gitignored — already present locally) |

---

## Databases

| File | Contents |
|------|---------|
| `db/graph_mirror.db` | Knowledge graph: entities, edges, episodes, communities, community_members, FTS5 indices |
| `db/indicators.db` | Indicator snapshots (last 20) + daily history per indicator |
| `db/financial_reports.db` | SEC report metadata: ticker, form_type, period, filed_date, local_path, accession_no, comment |
| `db/cninfo_reports.db` | A-share/HK report metadata: ticker, market, stock_code, period, form_type, local_path, comment |
| `db/zsxq.db` | ZSXQ PDFs: file_id, name, topic, local_path, classification tags, tickers, rating, comment, `ocr_text`. Plus the **retrieval/memory layer**: `pdf_files_fts` (trigram FTS5, BM25-ranked bilingual full-text — queried by `zsxq_fts.py`) and `pdf_cards` (agent-curated cards: covered tickers / theme / thesis / comparison-table page map — written by `zsxq_cards.py`). Both schema-owned by `zsxq_common.init_db`. |

> **Backup / tracking note:** most `db/*.db` are git-ignored; `db/notes.db` is force-tracked (`!db/notes.db`). **`db/zsxq.db` is NO LONGER git-tracked** — at ~124 MB it exceeds GitHub's 100 MB hard file limit. It is backed up to **Google Cloud Storage** via [`scripts/backup_dbs_to_gcs.sh`](scripts/backup_dbs_to_gcs.sh) (SQLite Online-Backup API → integrity-check → gzip ~67 MB → timestamped + `latest` objects; read-only on the live DB, safe to run while `:5001` is up). Set `FINAGENT_GCS_BUCKET=gs://<bucket>` and run the script; restore instructions are in its header.

---

## File Storage

```
financial_reports/<TICKER>/          SEC filings (PDFs + HTMLs)
cninfo_reports/<EXCHANGE>/<CODE>/    A-share / HK reports
uploads/                             User-uploaded images (markdown editor)
db/                                  All database files
templates/                           HTML templates
static/                              JS/CSS (Bootstrap, vis-network)
log/                                 Download + server logs
```

---

## Community System

Each entity belongs to **at most one** community.

### Batch build (`POST /zep/build-communities`)
`graph_mirror.build_communities(conn)`:
1. Label-propagation on non-deprecated edges
2. For each cluster: deterministic name + summary from member rows (no LLM)
3. Upsert into `communities` + `community_members`

### Manual create from seed (`POST /zep/communities`)
`graph_mirror.create_community_from_seed(conn, entity_uuid, name)`:
- BFS through non-deprecated edges from seed entity
- Assigns all reachable, unassigned entities to the new community

### BFS member removal (`DELETE /zep/communities/<id>/members/<uuid>`)
`graph_mirror.remove_community_bfs(conn, community_id, seed_uuid)`:
- BFS restricted to current community members only
- Removes all reachable members, updates `member_count`

### Delete community (`DELETE /zep/communities/<id>`)
- SQLite `CASCADE` on `community_members.community_id` FK handles member cleanup automatically

---

## Frontend (`templates/zep.html`)

Single-page app — **vis-network** graph + **Bootstrap 5** right panel.

### Graph Filtering
- `_visNodes` / `_visEdges` — vis-network `DataSet`; `hidden: true/false` drives filtering (no data reload)
- `_communityFilterUuids` (`Set<uuid>`) — active filter; shared by community view and unassigned view
- `filterGraphToCommunity()` — hides nodes/edges not in `_communityFilterUuids`
- `clearGraphFilter()` — restores all nodes/edges visible

### Right Panel Views
| Element ID | View |
|---|---|
| `resultsList` | Search results |
| `communityCard` | Paginated community browser |
| `communityDetailCard` | Community detail: member list, filter/delete/back buttons |
| `unassignedCard` | Entities not in any community |

### Key JS State Variables
```js
let _communityFilterUuids = new Set(); // drives filterGraphToCommunity()
let _currentCommunityId   = null;
let _assignSeedUuid       = null;
let _assignSuccess        = false;     // prevents hidden.bs.modal from re-navigating on programmatic close
```

### Key JS Functions
| Function | Description |
|---|---|
| `showCommunityBrowser()` | Show community list; `clearGraphFilter()` |
| `showCommunity(id, name)` | Load community detail; filter graph to members |
| `showUnassignedEntities()` | Load unassigned list; filter graph to unassigned nodes |
| `filterGraphToCommunity()` | Apply `_communityFilterUuids` to graph |
| `clearGraphFilter()` | Un-hide all graph nodes/edges |
| `deleteCommunity()` | DELETE community, clear filter, reload list |
| `removeCommunityMember(cid, uuid)` | DELETE member (BFS on backend), reload detail |
| `submitAssignCommunity()` | POST community, 800 ms success flash → hide modal → `showUnassignedEntities()` |
| `clickEntity(uuid)` | Show entity edges; clicked entity appears first in list |

---

## Key Patterns

1. **SQLite + WAL**: the knowledge graph DB is opened in WAL mode so a long-running Flask process can read while `manual_graph.py` writes from another session.
2. **Entity Isolation**: `graph_mirror.isolate_entity(conn, uuid)` sets `isolated=1` on the entity and auto-deprecates all its edges (`deprecated_reason='ENTITY_ISOLATED'`). Isolated entities are excluded from graph view, search, and stats. Reversed by setting `isolated=0` and un-deprecating edges.
3. **Entity Merge**: `graph_mirror.merge_entities(conn, source_uuid, target_uuid)` re-points all edges from source to target, removes resulting self-loops, then deletes the source entity. Edges are preserved — no relationship information is lost.
4. **SSE Streaming**: Long-running operations (downloads, community build) stream progress via Server-Sent Events.
3. **EasyMDE Widget**: Editable table cells follow `md_comment_widget.py` pattern — click → preview modal → edit modal → POST → re-render in place.
4. **Graph Filter via `hidden`**: Community and unassigned views reuse the same `_communityFilterUuids` + `filterGraphToCommunity()` pattern; no data reload needed.
5. **Incremental Downloads**: Date-cutoff logic in `_run_download()` skips already-downloaded filings; safe to re-run.
6. **Decoupled Classify**: zsxq download and classification are separate steps — allows prompt iteration without re-downloading.
