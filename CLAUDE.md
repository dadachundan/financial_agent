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

# Database Safety (MANDATORY — never touch real data)

**NEVER run a destructive query against any SQLite file under `db/` — these contain the user's real research notes, comments, ratings, classifications, and downloaded report metadata. Lost data cannot be recovered.**

Forbidden, no exceptions:

- `DELETE FROM <table>` without a primary-key `WHERE` clause that targets ONLY the row(s) you yourself just inserted seconds ago in this same shell.
- `DROP TABLE`, `TRUNCATE`, `UPDATE … SET … WHERE 1=1`, `DELETE FROM <table> WHERE created_at > '…'` against `db/notes.db`, `db/zsxq.db`, `db/financial_reports.db`, `db/cninfo_reports.db`, `db/report_annotations.db`, or any other file under `db/`.
- Wiping a table "to clean up test data" — even if you "just created the rows", you do not know whether the user added their own in another tab/session in between.

Approved testing patterns:

1. **Copy the DB to /tmp and point the test server at the copy.**
   ```bash
   cp db/notes.db /tmp/notes.test.db
   # Run the module against the test copy via env var or DB_PATH override.
   # After testing: rm /tmp/notes.test.db
   ```
2. **Use a throwaway `file_id` that can never collide with real data.** For zsxq experiments, pick a value like `999000000000001` (well above any real zsxq id) and scope every insert/delete to that single id:
   ```sql
   DELETE FROM pdf_inline_comments WHERE file_id = 999000000000001;
   ```
3. **Use the HTTP API instead of raw SQL** — POST a row, capture the returned `id`, DELETE that exact id by primary key. Never write a `WHERE` clause that could match a real row.
4. **Read-only inspection is always fine** (`SELECT …`, `.schema`, `sqlite3 db.db .tables`).

Before any `DELETE`/`UPDATE`/`DROP` against a `db/*.db` file:
- Confirm the file path starts with `/tmp/` or matches a known-test name (`*.test.db`, `*.sandbox.db`).
- If it starts with `db/`, stop and ask the user instead of guessing.

This rule exists because in this session I ran `DELETE FROM pdf_inline_comments` to clear what I thought was my own test data — and silently wiped the user's two real comments on the Nomura PDF. That is the failure mode this rule prevents.

# UI Verification (MANDATORY)

After adding or modifying any UI feature — especially new buttons, modals, or navigation flows:

1. **Always start the real web server on port 5002** (`preview_start` with port 5002 — do NOT use 5001, that port belongs to the user's running instance).
2. **Click every new button** and verify it performs the correct action (use `preview_eval` to simulate clicks if needed).
3. **Trace JS errors**: use `preview_console_logs` and `preview_eval` to check for `undefined`, `null`, or scoping issues (e.g. variables declared inside an IIFE are not accessible outside it).
4. **Verify navigation flows end-to-end**: if a button should navigate to another view, confirm the target view actually appears.
5. Do not consider UI work done until you have a screenshot or eval result proving each new interaction works.
6. **Always stop the server (`preview_stop` + `lsof -ti :5002 | xargs kill -9`) the moment testing is finished.** Never leave a test server running.

# One-off Explanations / Primers / Glossaries

When the user asks for a one-off explanation, primer, glossary, or technical-term reference (anything that explains *concepts* rather than analyzing a company, sector, comparison, or earnings release), save it as a markdown file under `reports/explanation/`. This makes the doc visible on the `http://localhost:5001/claude-reports/` viewer under the **EXPLANATION** type (defined in `reports_viewer.py` via `_BUCKET_LABELS`).

- Path: `reports/explanation/<descriptive_slug>.md` — kebab-case or snake_case; include the topic + source in the slug (e.g. `glossary_nomura_greater_china_semi_2026-30F.md`, `explainer_backside_power_delivery.md`).
- TYPE column shows `EXPLANATION` (teal pill). Filterable via the report-type dropdown.
- Don't create a sub-folder per explanation — keep the directory flat.
- Always commit the file in the same task it was created (Conventional Commits, e.g. `docs(explanation): …`).

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

# Report Verification Workflow (URLs + hallucinations)

When the user asks to **verify, audit, or fix URLs / hallucinations in a report** under `reports/` (any phrasing — "verify all links are accurate", "check for hallucinations", "audit citations", "the content is not made up", etc.):

1. **Run the full verification pass without asking permission to continue.** Do not stop mid-audit to ask "should I keep going" or "want me to patch the issues now" — keep going until every URL is checked, every numerical claim is grepped against its primary source, and every external claim is web-searched. Then **edit the report in place** to fix what you found.
2. **Commit and push when done.** Use a `fix(reports/<slug>):` Conventional Commit summarising the categories of fixes (broken URLs, fabricated numbers, wrong dates, mis-paired comparisons, etc.). Push to `main` per the standard workflow.
3. **Only stop early if** (a) the report doesn't exist, (b) the fixes would require new primary research the user hasn't asked for, or (c) you encounter ambiguity that genuinely can't be resolved from sources (in which case ask one focused question).
4. **Always append a Step-10 verification log** (`<details><summary>Verification log (Step 10) — YYYY-MM-DD</summary>...`) per the company-research skill spec — listing every spot-check, every correction made, and any residual unknowns.

The standard fix-list to look for, in priority order: fabricated SEC URLs (resolve real filenames via the EDGAR submissions JSON), fabricated numbers attributed to filings (grep the actual 10-K / 8-K / DEF 14A text), fabricated third-party stats (web-search the real source), wrong launch / acquisition / filing dates, mis-paired YoY comparisons, and analyst opinions misattributed to primary filings (relabel as `*Analyst view:*` per the company-research skill rule).

# LLM API Usage

- Use **MiniMax** for simple summarisation tasks and other straightforward LLM calls.
- The MiniMax API key is stored in `config.py` (gitignored, not checked in — already present locally).
- Import and call via `minimax.py`:

  ```python
  from minimax import call_minimax, MINIMAX_API_KEY
  text, elapsed, raw_json = call_minimax(
      messages=[
          {"role": "system", "name": "MiniMax AI", "content": "..."},
          {"role": "user",   "name": "User",       "content": "..."},
      ],
      temperature=0.2,
      max_completion_tokens=512,
  )
  ```

# Skills

If you change a skill (add, remove, or modify its `## Prerequisites`), update [reference/available_skill.md](reference/available_skill.md) in the same commit.
