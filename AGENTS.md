# AGENTS.md — Codebase Guide for AI Agents

## Repository Overview

Tech-industry knowledge graph web app + zsxq PDF pipeline.

---

## Knowledge Graph (`knowledge_graph.py` + supporting modules)

### Architecture (layered)

| File | Layer | Responsibility |
|------|-------|----------------|
| `knowledge_graph.py` | Application | Flask app, routes, entry point |
| `kg_db.py` | Data | `get_db()`, `init_db()`, `seed_db()`, schema, migrations |
| `kg_models.py` | Model | `build_graph_json()` — converts DB rows to vis-network JSON |
| `kg_services.py` | Service | File upload, URL fetch, LLM summarisation, PDF extraction, entity upsert |
| `templates/index.html` | View | Jinja2 HTML template (no inline Python) |
| `static/app.js` | Frontend | All JavaScript; reads `window.graphData` injected by the template |

### Data Model

- **companies** — tech companies (NVIDIA, AMD, TSMC …)
- **businesses** — industry domains (GPU, CPU, Memory, Manufacturing …)
- **business_company** — a company participates in a business domain
- **business_business** — two business domains are related
- All relationship tables carry: `comment`, `explanation`, `image_path`, `source_url`, `rating (0-5)`

### Key Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Main page (graph + tables) |
| POST | `/bc/add` | Add Business↔Company link |
| POST | `/bc/rate/<id>` | AJAX — update rating (returns 204) |
| POST | `/bc/delete/<id>` | Delete BC link |
| POST | `/bb/add` | Add Business↔Business link |
| POST | `/bb/rate/<id>` | AJAX — update rating (returns 204) |
| POST | `/bb/delete/<id>` | Delete BB link |
| POST | `/company/add` | Add company |
| POST | `/business/add` | Add business domain |
| POST | `/api/summarize` | LLM: summarise URL for a relationship |
| POST | `/api/pdf-import` | LLM: extract entities from a PDF |
| GET | `/uploads/<fname>` | Serve uploaded images / PDFs |

### Input Validation Conventions

- `kg_services._require_str(value, field)` — raises `ValueError` on empty
- `kg_services._parse_rating(value)` — coerces to `int` in `[0, 5]`

### LLM Usage

- Import: `from minimax import call_minimax, MINIMAX_API_KEY`
- System+User prompts live in `kg_services.py` constants (`_SUMMARIZE_SYSTEM`, `_PDF_SYSTEM`)
- Summarise URL: `kg_services.llm_summarize_url(url, entity_a, entity_b)`
- Extract PDF entities: `kg_services.llm_extract_entities(raw_text)`

### Running the App

```bash
python knowledge_graph.py                    # default port 5001
python knowledge_graph.py --port 8080 --db custom.db
```

---

## zsxq PDF Pipeline

### Two-script design

| Script | Role |
|--------|------|
| `zsxq_downloader.py` | **Download only** — authenticates, fetches file listings, downloads PDFs, writes to `zsxq.db` + tracker |
| `zsxq_index.py` | **Classify only** — reads `zsxq.db`, calls MiniMax for AI/Robotics/Semiconductor/Energy classification, no web scraping |

This separation means you can:
- Re-run classification with a new prompt without re-downloading.
- Download in bulk first, then classify at any time.

### Shared module

`zsxq_common.py` contains everything both scripts need:
- Constants: `API_BASE`, `HEADERS`, `DEFAULT_CHROME_PROFILE`, `DEFAULT_DB`, `DEFAULT_DOWNLOADS`
- `get_session_via_selenium(chrome_profile)` — Selenium cookie extraction
- `sanitize_filename(name)` — strip path-unsafe chars
- `fetch_files_page(...)` / `fetch_all_files(...)` — paginated API listing
- `get_download_url(session, file_id)` / `download_file(session, url, dest)` — CDN download
- `load_tracker(dir)` / `save_tracker(dir, tracker)` — JSON tracker
- `do_download(session, file_id, name, dir, tracker)` — full download + tracker update
- `init_db(db_path)` — open/migrate `zsxq.db`
- `upsert_entry(conn, row)` — insert/update a `pdf_files` row

### Database: `zsxq.db`

Table: **pdf_files**

| Column | Type | Notes |
|--------|------|-------|
| `file_id` | INTEGER PK | zsxq file ID |
| `name` | TEXT | filename |
| `topic_title` | TEXT | full title from talk.text |
| `summary` | TEXT | Chinese summary from topic |
| `local_path` | TEXT | abs path on disk, NULL if not downloaded |
| `ai_related` | INTEGER | 1/0/NULL (v2 classification) |
| `robotics_related` | INTEGER | 1/0/NULL |
| `semiconductor_related` | INTEGER | 1/0/NULL |
| `energy_related` | INTEGER | 1/0/NULL |
| `tickers` | TEXT | comma-separated ticker symbols |
| `categories_analysis` | TEXT | MiniMax 2-3 sentence summary |

### Typical workflow

```bash
# Step 1 — download latest 50 PDFs
python zsxq_downloader.py --count 50

# Step 2 — classify all unclassified rows
python zsxq_index.py

# Step 3 — re-classify everything with updated prompt
python zsxq_index.py --reclassify
```

---

## Configuration

- `config.py` (gitignored) — must contain `MINIMAX_API_KEY = "..."`
- `chrome_profile/` — Chrome user-data-dir with zsxq.com cookies
- `kg_uploads/` — uploaded images and PDFs for the knowledge graph

## Dependencies

```
flask pdfplumber requests selenium webdriver-manager
```

Install: `pip install flask pdfplumber requests selenium webdriver-manager`
