# Workflow Instructions

When the user asks for a fix — "fix it", "patch it", "why does X render like that", or any phrasing that points at a concrete bug they want closed — **just fix it**. Do not ask "want me to apply the fix?" / "should I patch this?" / "do you want me to go ahead?" The request to fix is already on the table; asking again is friction. Diagnose, edit, verify, commit, push. If the fix branches (two plausible approaches with real trade-offs), pick the better one and say so in the commit message — don't stall on confirmation.

Before writing any code:
1. Ensure the current branch is synced to `main` HEAD:
```
git fetch origin && git merge --ff-only origin/main
```
   If the fast-forward fails (diverged branch), discard stale local changes and rebase.
2. Search existing code before writing anything new. Check if a helper, route, or utility already exists that can serve the purpose (grep for keywords, read related files). Do not duplicate functionality that already exists.

After completing a task and verifying that it works (by running tests or the app):

1. Create a concise Git commit using Conventional Commits (e.g., `fix:`, `feat:`).
2. If working on a worktree branch, immediately merge it into `main` (`git checkout main && git merge <branch> --no-ff && git push origin main`).
3. Ensure the local `main` is synced with the remote `HEAD`.
4. Do not include the "Co-authored-by: Claude" footer in commits.
5. **Always stop all test servers after verifying a task works — no exceptions.** Kill the test ports:
   ```
   lsof -ti :5002 | xargs kill -9 2>/dev/null; lsof -ti :8080 | xargs kill -9 2>/dev/null
   ```
   Port 5001 is reserved for the user's own running server — never start a test server on 5001 and never kill 5001.
6. If the architecture changes, update `architecture.md`.

# Database Safety (MANDATORY — non-negotiable, zero exceptions)

**Every `*.db` file inside this project is the user's real, irreplaceable data. Treat all of them as read-only from Claude's hands.**

This has gone wrong more than once. Past failures include (at least): wiping `pdf_inline_comments` to clear "test data" and taking real comments along with it; clearing `notes.db` rows during another session. The rule below exists to make the failure mode mechanically impossible, not to remind future-Claude to be careful.

## What's covered

**ALL `*.db` files in the project**, no matter where they live. This includes — but is not limited to — files under `db/` (`db/notes.db`, `db/zsxq.db`, `db/financial_reports.db`, `db/cninfo_reports.db`, `db/report_annotations.db`, `db/market_cap_cache.db`, `db/indicators.db`, `db/markdown_reports.db`, `db/knowledge_graph.db`, `db/graph_mirror.db`), files at the project root (`zsxq.db`, `knowledge_graph.db`, `graph_mirror.db`), files in subdirectories (`youtube/video_summaries.db`, anywhere else), and any new database file that appears in the future without an explicit `.test.db` / `.sandbox.db` suffix.

If a path matches `*.db` and is not under `/tmp/` and doesn't end in `.test.db` / `.sandbox.db`, **it is real user data.**

## The rule

Against any of those files:

- `DELETE`, `DROP`, `TRUNCATE`, `UPDATE`, `INSERT`, `ALTER`, `REPLACE`, `VACUUM` — **forbidden**, full stop. No "but I just inserted that row" carve-out. No "but it's clearly test data" carve-out. No `WHERE id = N` carve-out. No.
- `cp <db> …` overwriting another real db, `mv <db> …`, `rm <db>`, `> <db>` redirecting any process output onto a real db — **forbidden**.
- Schema migrations (`ALTER TABLE`, `CREATE TABLE`) are forbidden too. If a new column is needed, write a one-shot migration script, have the user run it themselves, and `git status` afterwards to confirm exactly one file changed.

The only thing Claude is allowed to do against a real `*.db` is read: `SELECT`, `.schema`, `.tables`, `PRAGMA table_info(...)`, `sqlite3 path.db ".dump table | head"`, copying TO `/tmp/` (`cp db/notes.db /tmp/notes.test.db` is fine — the source is read-only-ish, the destination is a sandbox path).

## How to actually test code that writes to a DB

There is exactly one approved pattern. Every Python module in the project that opens a SQLite DB resolves its path through `db_paths.db_path(name)` / `db_paths.db_dir()` (see [db_paths.py](db_paths.py)). Setting the single environment variable **`FINAGENT_DB_DIR`** redirects ALL of them at once. That's the only mechanism Claude should ever use to point the app at test data.

```bash
# 1. Copy the DBs you'll be writing to into a sandbox dir
mkdir -p /tmp/finagent-test
cp db/notes.db db/zsxq.db /tmp/finagent-test/   # whatever you need

# 2. Run the app or a script with the env var set
FINAGENT_DB_DIR=/tmp/finagent-test python main.py --port 5002
#  → pdf_inline_comments.DB_PATH         = /tmp/finagent-test/notes.db
#  → pdf_page_ocr.DB_PATH                = /tmp/finagent-test/notes.db
#  → report_inline_comments.DB_PATH      = /tmp/finagent-test/notes.db
#  → report_annotations.DB_PATH          = /tmp/finagent-test/report_annotations.db
#  → zsxq_common.DEFAULT_DB              = /tmp/finagent-test/zsxq.db
#  → fetch_financial_report.DB_FILE      = /tmp/finagent-test/financial_reports.db
#  → fetch_cninfo_report.DB_FILE         = /tmp/finagent-test/cninfo_reports.db
#  → market_cap_cache._DB_PATH           = /tmp/finagent-test/market_cap_cache.db
#  → graph_mirror._DEFAULT_MIRROR        = /tmp/finagent-test/graph_mirror.db
#  → indicators/db._DB_PATH              = /tmp/finagent-test/indicators.db
#  → zep_app.ZSXQ_DB                    = /tmp/finagent-test/zsxq.db

# 3. Test freely — DELETE / DROP / TRUNCATE are all fine against
#    /tmp/finagent-test/*.db because the path passes the sandbox check
#    (starts with /tmp/).

# 4. When done:
rm -rf /tmp/finagent-test
```

If you add a NEW Python module that opens a `.db` file, **you MUST resolve its path through `db_paths.db_path()` in the same commit as the module**. Hardcoding `Path(__file__).parent / "db" / "foo.db"` is a regression — the FINAGENT_DB_DIR override won't reach it, and future-Claude is one mis-typed `DELETE FROM` away from data loss. The test class `TestFinagentDbDirOverride` in [tests/test_db_paths.py](tests/test_db_paths.py) is the gate: add a parametrize entry for the new module's `DB_PATH` constant so CI catches the regression.

## Sanity check before any DB-touching command

Before running any `sqlite3` / `psql` / Python script that opens a DB, the literal path string in the command must satisfy:

```
path.startswith("/tmp/")  or  path.endswith(".test.db")  or  path.endswith(".sandbox.db")
```

If it doesn't, the command is permitted ONLY if its read-only nature is obvious at a glance — `SELECT …`, `.schema`, `PRAGMA …`, `.tables`, or piping `.dump` to `head`. Anything else — even something that "should be" a SELECT — stop and ask. The path check is the gate; it's stricter than "is this destructive?" because intent doesn't survive a typo.

# UI Verification (MANDATORY)

After adding or modifying any UI feature — especially new buttons, modals, or navigation flows:

1. **Always start the real web server on port 5002** (`preview_start` with port 5002 — do NOT use 5001, that port belongs to the user's running instance).
2. **Click every new button** and verify it performs the correct action (use `preview_eval` to simulate clicks if needed).
3. **Trace JS errors**: use `preview_console_logs` and `preview_eval` to check for `undefined`, `null`, or scoping issues (e.g. variables declared inside an IIFE are not accessible outside it).
4. **Verify navigation flows end-to-end**: if a button should navigate to another view, confirm the target view actually appears.
5. Do not consider UI work done until you have a screenshot or eval result proving each new interaction works.
6. **Always stop the server (`preview_stop` + `lsof -ti :5002 | xargs kill -9`) the moment testing is finished.** Never leave a test server running.

# One-off Explanations / Primers / Glossaries

**Default behavior: just answer in chat. Do NOT save to a file unless the user explicitly asks.**

When the user asks "what is X" / "explain Y" / "tell me about Z" / "什么是…" / etc., reply directly in the conversation. No file. No `reports/explanation/` write. No commit. Even if the topic is technical or the answer is long.

Save to disk **only** when the user explicitly says "save this", "write this to a file", "add to explanation folder", "保存", or similar. In that case:

- Path: `reports/explanation/<descriptive_slug>.md` — kebab-case or snake_case; include the topic + source in the slug (e.g. `glossary_nomura_greater_china_semi_2026-30F.md`, `explainer_backside_power_delivery.md`).
- The viewer at `http://localhost:5001/claude-reports/` surfaces the file under the **EXPLANATION** type (teal pill, defined in `reports_viewer.py` via `_BUCKET_LABELS`).
- Don't create a sub-folder per explanation — keep the directory flat.
- Commit in the same task using Conventional Commits, e.g. `docs(explanation): …`.

# Editable Table Columns

When the user asks to make a field in a table editable, always use the `md_comment_widget.py` pattern:

1. The cell contains a `<span class="*-preview" data-raw="...html-escaped markdown...">` that renders markdown on load.
2. Clicking the cell opens a **preview modal** (Bootstrap) showing the rendered markdown + an "Edit" button.
3. Clicking "Edit" closes the preview modal and opens an **EasyMDE editor modal** (with image upload toolbar + clipboard-paste-to-upload support).
4. Saving POSTs the markdown to the backend, then updates `span.dataset.raw` and re-renders the cell in place — no page reload.
5. The backend save route accepts JSON `{"description": "..."}` (or whichever field name) and returns `{"ok": true}`.

See `md_comment_widget.py` for the shared blueprint (`/upload-image`, `/uploads/<path>`) and reference the entity-description implementation in `templates/index.html` (search `viewEntityDesc`) as a concrete example.

# Downloading Files

When running any download script (reports, PDFs, data files), always `cd` to the main project directory first:
```
cd /Users/x/projects/financial_agent
```
This ensures all downloaded files land in the main project's directories (e.g. `cninfo_reports/`, `financial_reports/`) and not in the worktree.

# Fetching Financial Reports

- **Chinese A-share / HK reports** → use `fetch_cninfo_report.py`
  - Ticker format: `SZSE:002050`, `SSE:688802`, `HKEX:2513`
  - **Always run from the main project dir** (`cd /Users/x/projects/financial_agent`), otherwise files land in the worktree
  - Call directly: `python3 -c "import fetch_cninfo_report as cr; cr.init_db(); [print(m) for m in cr._run_download('SZSE:002050', cr.ALL_CATEGORIES)]"`
  - Files saved to `cninfo_reports/<EXCHANGE>/<CODE>_<NAME>/`
  - DB: `db/cninfo_reports.db`

- **US stock reports (10-K / 10-Q / 8-K)** → use `fetch_financial_report.py`
  - Ticker format: `AAPL`, `NVDA`, etc. (no exchange prefix)
  - Files saved to `financial_reports/<TICKER>/`
  - DB: `db/financial_reports.db`

# PDF Text Extraction (image-only / scanned reports)

When a PDF page returns empty text from `fitz.get_text()` (rasterized
cover pages, exhibit-only slides, the occasional fully-scanned report),
use the three-tier flow — never try Tesseract:

1. **Default: `ocrmac`** (Apple Vision framework on the Neural Engine).
   ~1 s/page on M-series, ~98%+ on clean English/Chinese, zero RAM
   overhead. Already wrapped in
   `.claude/skills/zsxq-analyze/scripts/ocr_pdf.py`, which writes the
   result back to `pdf_files.ocr_text` so re-runs are free.
2. **Layout-tier upgrade: Marker** (built on Surya, PyTorch+MPS). Use
   only when ocrmac scrambles the reading order or when you need
   tables-as-markdown — e.g. multi-column research notes or dense
   financial tables. Not wired in yet; add when the need first comes
   up.
3. **Vision LM (Claude multimodal) for charts.** When the meaning
   lives in a chart, axis labels alone aren't enough — render the
   page via `render_pdf_pages.py` and Read the PNG directly. Use
   sparingly because vision tokens are ~$0.03/page.

The corresponding DB columns on `pdf_files` are `ocr_text` (cached
page-marked text) and `ocr_at` (timestamp). Both are added by
`ocr_pdf.py` on first use — no manual migration.

# Research Report Filenames (MANDATORY — must include English / pinyin name)

**Every research-report file and folder under `reports/company/` MUST start with the company's English or pinyin name as the first slug component**, even when the report itself is written in Chinese. The English name is what makes the file findable via `grep`, Spotlight, the viewer's search box, or just visual scanning of `ls`. A filename containing only Chinese characters (e.g. `中砂_TWSE1560_公司研究.md`) **fails this rule** — a reader searching for "Kinik" will not find it.

**Correct format**: `[EnglishName]_[中文名 optional]_[EXCHANGE][CODE]_<suffix>.md`

Examples:
- ✅ `reports/company/Kinik_中砂_TWSE1560/Kinik_中砂_TWSE1560_公司研究.md`
- ✅ `reports/company/BYD_比亚迪_HKEX1211/BYD_比亚迪_HKEX1211_Research_Document.md`
- ✅ `reports/company/Anpeilong_安培龙_SZSE002050/Anpeilong_安培龙_SZSE002050_公司研究.md`
- ✅ `reports/company/Tesla_NASDAQ_TSLA/Tesla_NASDAQ_TSLA_Research_Document.md` (no Chinese name needed for US issuers)
- ❌ `reports/company/中砂_TWSE1560/中砂_TWSE1560_公司研究.md` — unsearchable by English name
- ❌ `reports/company/比亚迪_HKEX1211/比亚迪_HKEX1211_公司研究.md` — same

For Japanese / Korean issuers, use Romaji / Romanization (e.g. `Toyota_TSE7203`, `Samsung_KRX005930`) — never kana, kanji-only, or hangul.

This rule also applies to **all other report categories** (`reports/sector/`, `reports/compare/`, `reports/earnings/`, `reports/explanation/`): the filename must contain enough English text to be searchable. Pure-Chinese filenames are not acceptable for cross-language discoverability.

# Citation Standard for Research Reports

All markdown reports under `reports/` (company / sector / compare / earnings / unlisted / etc.) must meet the project's paragraph-level citation standard. The authoritative spec is `.claude/skills/company-research/references/citations.md`. Summary:

1. **Every substantive paragraph carries ≥1 inline markdown-link citation.** Headings, tables, chart captions, short bridge sentences, and TOC entries are exempt; everything else is not. A paragraph with zero inline `[Title](URL)` links reads as unsourced opinion.
2. **Deep URLs only — never homepages.** Link to the specific SEC EDGAR document, the specific cninfo PDF, the specific Yole/Gartner/IDC report page. A link to `yolegroup.com` or `gartner.com` is a non-citation.
3. **Source-chain labels when a third-party number appears in a primary filing.** Cite the primary filing with a chain label (e.g. `[Hesai FY25 6-K 引用 Yole](https://www.sec.gov/...)`), not Yole's homepage.
4. **The analyst's own model is NOT a source.** Never write `(Source: our model)` / `(模型估算)` / `(本模型)` / `(estimate, our analysis)`. Cite the external inputs the model is built on (10-K segment data + an industry forecast).
5. **Preserve original language in link titles.** Chinese filings stay `年度报告` / `季度报告`; Japanese stay `有価証券報告書`; US filings stay `10-K` / `10-Q` / `8-K`. Do not translate.
6. **Freshness: discard web sources older than ~12 months** (news, blog posts, industry notes) except for founding facts, landmark research, or filings themselves. Include the publication date in the link title: `[Reuters, 2025-08-12](https://...)`.

When backfilling citations on existing reports, reuse the established pattern:

- **Inventory script** — count URLs / paragraph coverage / violations across all reports. The pattern lives in `reports/_backfill_manifest.json` (priority-sorted snapshot) and is regenerated by walking `reports/**/*.md` with regex.
- **Agent prompt template** — `reports/_backfill_agent_template.md`. Each backfill agent reads it + `.claude/skills/company-research/references/citations.md`, audits paragraphs, web-searches for verifiable URLs, edits in place, and reports back URL counts before/after.
- **Quality bar** — target ≥90% substantive-paragraph coverage. Sub-90% reports go back into the queue for a closing-gap pass.

When generating NEW research / valuation / sector / earnings notes from scratch, the citation rules apply from the first draft — don't defer sourcing to a later backfill.

# Numerical Accuracy (MANDATORY — every number traces to a URL that literally contains it)

Past failure mode: a paragraph reads "+185% QoQ, FY25 KRW 43.6 trn, DRAM contract prices +90–95% QoQ" and ends with **one** "Source: A; B" footer — and one of those numbers (e.g. the 90–95%) doesn't appear in *either* A or B. The number was real (it came from a TrendForce article cited 200 lines later), but the paragraph as written is unsourced for that figure. This is hallucination as far as the reader is concerned — they click the cited URL, the number isn't there, and the report's credibility collapses.

The rule, no exceptions:

1. **Every numerical claim in a paragraph must trace to a URL cited in that same paragraph where the number literally appears as a string.** Not "elsewhere in the report" — *in the same paragraph*. If a paragraph blends numbers from three sources (e.g. company release + third-party data + industry forecaster), the paragraph must cite all three inline, and each number must string-match the URL it's attached to.
2. **Derived numbers must be labelled or have both inputs sourced in the paragraph.** "48-fold YoY" is a calc on `53.7 / 1.1`. Either write it as `~48× (= 53.7 / 1.1 trn, both from [press release](...))` so a reader can re-derive, or cite a source that states the multiple verbatim. Never quote a derived number as if it came from a source that only contains the raw inputs.
3. **Year-over-year / quarter-over-quarter prints need a source that contains the YoY or QoQ figure itself, not just the latest period.** Citing the Q1 2026 press release for a "+69% YoY revenue" claim only works if the press release contains "+69% YoY"; otherwise cite the third party that did the math, or write it as an inline calc against the Q1 2025 source.
4. **Spot-check before commit.** Before saving any new/edited report, pick 3–5 numbers at random and string-match them against the cited URLs (`curl -s URL | grep -F "133.9"`). If a number doesn't string-match in *any* URL cited in that paragraph, fix the paragraph — don't ship.
5. **No "Source:" bundles that bury the mapping.** "Source: A; B; C" at the end of a paragraph means "everything here came from A, B, or C." If a number didn't come from any of them, that footer is a lie. Either inline-cite each claim or restructure the paragraph so each cited URL contains the numbers attributed to it.
6. **When verifying an existing report, audit the number→URL mapping, not just URL-reachability.** A 200-OK URL that doesn't contain the claimed number is *worse* than a 404 — the reader trusts it. Step-10 verification logs must list spot-checks of the form `"X = N from <URL>": ✓ string-matches | ✗ NOT in source — fix`.

If a number can't be sourced inline, two options: (a) remove it, or (b) replace it with a phrasing the sources actually support ("up sharply QoQ" instead of "+90–95% QoQ" if you can't find the precise figure). Never leave an unsourced number in a report.

# Report Verification Workflow (URLs + hallucinations)

When the user asks to **verify, audit, or fix URLs / hallucinations in a report** under `reports/` (any phrasing — "verify all links are accurate", "check for hallucinations", "audit citations", "the content is not made up", etc.):

1. **Run the full verification pass without asking permission to continue.** Do not stop mid-audit to ask "should I keep going" or "want me to patch the issues now" — keep going until every URL is checked, every numerical claim is grepped against its primary source, and every external claim is web-searched. Then **edit the report in place** to fix what you found.
2. **Commit and push when done.** Use a `fix(reports/<slug>):` Conventional Commit summarising the categories of fixes (broken URLs, fabricated numbers, wrong dates, mis-paired comparisons, etc.). Push to `main` per the standard workflow.
3. **Only stop early if** (a) the report doesn't exist, (b) the fixes would require new primary research the user hasn't asked for, or (c) you encounter ambiguity that genuinely can't be resolved from sources (in which case ask one focused question).
4. **Always append a Step-10 verification log** (`<details><summary>Verification log (Step 10) — YYYY-MM-DD</summary>...`) per the company-research skill spec — listing every spot-check, every correction made, and any residual unknowns.

The standard fix-list to look for, in priority order: fabricated SEC URLs (resolve real filenames via the EDGAR submissions JSON), fabricated numbers attributed to filings (grep the actual 10-K / 8-K / DEF 14A text), fabricated third-party stats (web-search the real source), wrong launch / acquisition / filing dates, mis-paired YoY comparisons, and analyst opinions misattributed to primary filings (relabel as `*Analyst view:*` per the company-research skill rule).

# NEVER call the Claude API (or any LLM API) from this project

This is a hard, project-wide rule the user has restated multiple times:

> **never use CLAUDE API, use the model itself!**
> **never use call claude with API!!**
> **delete claude_llm_client, never call claude with AP[I]!**
> **delete all minimax code, don't trust the quality**

"Use the model itself" means: when the project needs a model — to read a
report, extract entities, judge quality, summarise a document, classify a
PDF — **Claude (the agent, in this conversation) does it directly**, using
`Read` / `Edit` / `Bash` / `manual_graph` and the agent's own reasoning.
There is no `anthropic.Anthropic()`, no `client.messages.create`, no
`call_claude`, no `call_minimax`, no MiniMax-Anthropic proxy, no
graphiti-core LLM client, no Langchain, no OpenAI fallback. None of it.

Already deleted on 2026-06-02 to honour this rule:

- `minimax.py`, `minimax_llm_client.py`
- `claude_llm.py`, `claude_llm_client.py`
- `ingest/graphiti_ingest.py`, `ingest/zsxq_index.py`,
  `ingest/eval_entity_extraction.py`, `ingest/eval_ingest_prompt.py`
- `isolate_nonsense_entities.py`, `merge_duplicate_entities.py`,
  `restore_valid_entities.py`
- `zsxq_classify.py`
- `fetch_news.py`
- `youtube/analysis_video.py`

`zep_app.py` routes that depended on the API (`/ingest`, `/upload-pdf`,
`/entities/isolate-persons`, `/clear`) return **410 Gone**.

`download/zsxq_downloader.py` lost its `--classify` flag — it now only
downloads PDFs.

`langfuse_monitor.py` is kept for ad-hoc tracing of any manual call the
user makes themselves, but no project code calls it automatically anymore.

## Rules for future work

1. **Never** add `from anthropic import …`, `from claude_llm import …`,
   `import openai`, or any LLM-API client to any file in this repo.
2. **Never** re-create the deleted modules under a different name. If the
   user asks for "auto-classification" or "auto-extraction", push back and
   remind them of this rule — they probably forgot.
3. When the user asks to "update the knowledge graph", "classify these
   PDFs", "summarise this video", "tell me which entities are persons",
   etc., **you (the agent) do the work yourself in conversation**:
   - For graph work: `Read` the source report → use `manual_graph.py`
     to write entities and edges into `db/graph_mirror.db`. The viewer
     at `localhost:5001/zep/` picks them up immediately.
   - For classification / summary / judgement: read the source, write
     the answer in the conversation (or as a file, if asked). Don't
     spawn a script that calls an external model.
4. For large batches (e.g. dozens of reports), it's fine to fan out via
   `Agent` subagents — but each subagent does the reading and writing
   itself with `Read` + `manual_graph`. No subagent calls an LLM API.

## Knowledge graph workflow (the only sanctioned write path)

```python
from manual_graph import (
    add_entity, add_edge, add_episode, add_entities, add_edges, stats,
)

add_episode("NVDA_FY25_10K",
            name="NVIDIA FY25 10-K",
            source_desc="financial_reports/NVDA/...")

add_entity("NVIDIA", labels=["Company"], ticker="NVDA",
           summary="Fabless GPU vendor; dominant in AI training.")
add_entity("TSMC",   labels=["Company"], ticker="TSM",
           summary="World's largest dedicated foundry.")

add_edge("TSMC", "NVIDIA",
         relation="MANUFACTURES_FOR",
         fact="TSMC fabricates NVIDIA's H100 and Blackwell GPUs at N4/N3.",
         source="NVDA_FY25_10K")
```

`add_entity` is idempotent by name (case-insensitive); `add_edge` raises
`ValueError` if either endpoint is missing — add the entities first.
Every edge **must** carry a `source=` slug pointing at the document you
actually read; the viewer surfaces it in the edge tooltip and that
provenance is the entire point of curating by hand.

# Skills

If you change a skill (add, remove, or modify its `## Prerequisites`), update [reference/available_skill.md](reference/available_skill.md) in the same commit.
