# Financial Agent — Architecture Overview

## Entry Point

**`main.py`** — Unified Flask app on port 5001 (default). Registers 4 blueprints:
- `/zep/*` — Knowledge graph UI
- `/zsxq/*` — ZSXQ PDF viewer
- `/sec/*` — US SEC filings
- `/cn/*` — A-share & HK reports

---

## Flask Sub-Apps

### `zep_app.py` — Knowledge Graph UI
Local graphiti-core + KuzuDB graph — no cloud dependencies.
- **DB**: `db/graphiti_db` (KuzuDB) + `db/graph_mirror.db` (SQLite read mirror)
- **Deps**: graphiti-core, KuzuDB C extension, bge-m3 embeddings, MiniMax LLM

#### Graph & Entity Routes
| Method | Path | Description |
|--------|------|-------------|
| GET | `/zep/` | Serve `zep.html` SPA |
| GET | `/zep/search` | Full-text + vector search → `{nodes, edges, episodes}` |
| GET | `/zep/entities` | Paginated entity list |
| GET | `/zep/entities/unassigned` | Entities not in any community (non-isolated) |
| GET | `/zep/entity-community-map` | `{uuid: community_id}` for all assigned entities |
| GET | `/zep/edges` | Paginated edge list |
| GET | `/zep/stats` | `{node_count, edge_count, episode_count, community_count}` |
| POST | `/zep/entities/<uuid>/rate` | Set star rating |
| POST | `/zep/entities/<uuid>/edit` | Edit name / summary |
| POST | `/zep/entities/<uuid>/isolate` | Hide entity from graph |
| GET | `/zep/entities/<uuid>/edges` | Edges for one entity |
| POST | `/zep/edges/<uuid>/deprecate` | Deprecate an edge |
| POST | `/zep/edges/<uuid>/edit` | Edit edge fact / name |

#### Community Routes
| Method | Path | Description |
|--------|------|-------------|
| GET | `/zep/communities` | Paginated community list (with `member_count`) |
| GET | `/zep/communities/<id>` | Community detail + member list |
| POST | `/zep/communities` | Create community from seed entity (BFS assigns all reachable) |
| DELETE | `/zep/communities/<id>` | Delete community; CASCADE removes members |
| DELETE | `/zep/communities/<id>/members/<uuid>` | BFS-remove entity + all connected members |
| POST | `/zep/build-communities` | SSE stream: label-propagation + LLM summaries for all entities |
| DELETE | `/zep/communities/singletons` | Delete all 1-member communities |

#### Ingest Routes
| Method | Path | Description |
|--------|------|-------------|
| GET | `/zep/ingest` | SSE stream: index new PDFs from watched folder |
| POST | `/zep/upload-pdf` | SSE stream: upload + index a PDF |
| POST | `/zep/refresh-mirror` | Force re-backfill SQLite from KuzuDB |
| POST | `/zep/isolate-persons` | Auto-isolate all PERSON-type entities |
| POST | `/zep/clear-graph` | Wipe all graph data |

### `fetch_financial_report.py` — US SEC Reports
Download SEC 10-K / 10-Q / 8-K / 20-F filings from EDGAR.
- Key routes: `GET /sec/` (UI), `POST /sec/download` (SSE stream), `GET /sec/reports` (JSON), `GET /sec/file/<id>`, `POST /sec/index-report/<id>` (→ graphiti)
- **DB**: `db/financial_reports.db`
- **Storage**: `financial_reports/<TICKER>/`
- Rate-limited: ≤10 req/sec to SEC EDGAR

### `fetch_cninfo_report.py` — A-share & HK Reports
Download A-share (SSE/SZSE) and HK (HKEX) reports via CNINFO.
- Key routes: `GET /cn/` (UI), `POST /cn/download` (SSE), `GET /cn/reports` (JSON), `GET /cn/file/<id>`
- **DB**: `db/cninfo_reports.db`
- **Storage**: `cninfo_reports/<EXCHANGE>/<CODE>/`

### `zsxq_viewer.py` — ZSXQ PDF Viewer
Browser for the 知识星球 research group PDF library.
- Key routes: `GET /zsxq/` (UI), `GET /zsxq/pdfs` (JSON), `GET /zsxq/pdf/<id>`, `POST /zsqx/rate/<id>`, `POST /zsxq/comment/<id>`
- **DB**: `db/zsxq.db`

---

## Data Pipeline

### Download

| Script | Purpose |
|--------|---------|
| `download/zsxq_downloader.py` | Selenium → zsxq API → PDFs → `zsxq.db` (+ optional classify) |
| `download/bulk_download_10k_10q_8k.py` | Batch SEC 10-K/10-Q/8-K + 20-F/40-F/6-K for watchlist tickers |
| `download/bulk_download_ashare.py` | Batch CNINFO A-share + HK annual/semi-annual/quarterly reports |

### Ingest / Index

| Script | Purpose |
|--------|---------|
| `ingest/graphiti_ingest.py` | PDF/HTML → KuzuDB graph (entity/edge extraction via MiniMax + bge-m3) |
| `ingest/zsxq_index.py` | Classify PDFs already in `zsxq.db` (AI / Robotics / Semiconductor / Energy) |

---

## LLM & Embedding

| File | Purpose |
|------|---------|
| `minimax.py` | HTTP client for MiniMax API (`MiniMax-Text-01`); returns `(text, elapsed, raw_json)` |
| `minimax_llm_client.py` | Wires MiniMax + bge-m3 into graphiti-core abstract interfaces; singleton `get_graphiti()` |
| `zsxq_classify.py` | Classification prompts + helpers for 4 research categories |

---

## Utility Modules

| File | Purpose |
|------|---------|
| `graph_mirror.py` | SQLite shadow copy of KuzuDB; WAL mode for concurrent reads; owns all community logic (`build_communities`, `create_community_from_seed`, `remove_community_bfs`); entity lifecycle: `isolate_entity`, `merge_entities` |
| `isolate_nonsense_entities.py` | One-off script: batches all visible entities, sends to MiniMax, isolates ones that don't make sense for financial analysis (dollar amounts, dates, generic labels, etc.) |
| `restore_valid_entities.py` | One-off correction pass: reviews isolated entities and restores legitimate ones (companies, regulators, named products) wrongly isolated in first pass |
| `merge_duplicate_entities.py` | Dedup script: Pass 1 exact-name merges (no LLM); Pass 2 candidate-pair LLM confirmation (SequenceMatcher + first-word heuristics, hallucination guard validates UUIDs against input pairs). Edges re-pointed to canonical entity before source is deleted. Run with `DRY_RUN=1` to preview. |
| `md_comment_widget.py` | Reusable EasyMDE markdown editor modal + image-paste-to-upload blueprint |
| `nav_widget2.py` | Shared navbar HTML injected into every sub-app template |
| `ticker_names.py` | Background-thread loader of A-share/HK `{code: company_name}` map (AKShare); weekly cache |
| `langfuse_monitor.py` | OTel-native Langfuse tracing for LLM calls |
| `pdf_eval.py` | Offline evaluation of ingest quality on random sample |
| `tradingview.py` | Selenium-based TradingView watchlist scraper (experimental) |
| `config.py` | API keys (gitignored — already present locally) |

---

## Databases

| File | Contents |
|------|---------|
| `db/graphiti_db` | KuzuDB graph: Entity, Edge, Episode, Community nodes |
| `db/graph_mirror.db` | SQLite mirror: entities, edges, episodes, communities, community_members, zsxq_imported, entities_fts, edges_fts, pending_deletions |
| `db/financial_reports.db` | SEC report metadata: ticker, form_type, period, filed_date, local_path, accession_no, comment, graphiti_indexed_at |
| `db/cninfo_reports.db` | A-share/HK report metadata: ticker, market, stock_code, period, form_type, local_path, comment |
| `db/zsxq.db` | ZSXQ PDFs: file_id, name, topic, local_path, classification tags, tickers, rating, comment, graphiti_indexed_at |

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
2. For each cluster: call MiniMax to generate `NAME` + `SUMMARY` (markdown headers stripped before storing)
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

1. **SQLite Mirror**: KuzuDB holds the write lock during ingest; SQLite mirror (WAL mode) serves all web reads concurrently.
2. **Entity Isolation**: `graph_mirror.isolate_entity(conn, uuid)` sets `isolated=1` on the entity and auto-deprecates all its edges (`deprecated_reason='ENTITY_ISOLATED'`). Isolated entities are excluded from graph view, search, stats, and LLM extraction prompts (injected as "do not extract" list in `minimax_llm_client.py`). Reversed by setting `isolated=0` and un-deprecating edges.
3. **Entity Merge**: `graph_mirror.merge_entities(conn, source_uuid, target_uuid)` re-points all edges from source to target, removes resulting self-loops, then deletes the source entity. Kuzu stale nodes cleaned up best-effort. Edges are preserved — no relationship information is lost.
2. **SSE Streaming**: Long-running operations (download, ingest, community build) stream progress via Server-Sent Events.
3. **EasyMDE Widget**: Editable table cells follow `md_comment_widget.py` pattern — click → preview modal → edit modal → POST → re-render in place.
4. **Graph Filter via `hidden`**: Community and unassigned views reuse the same `_communityFilterUuids` + `filterGraphToCommunity()` pattern; no data reload needed.
5. **Incremental Downloads**: Date-cutoff logic in `_run_download()` skips already-downloaded filings; safe to re-run.
6. **Decoupled Classify**: zsxq download and classification are separate steps — allows prompt iteration without re-downloading.
