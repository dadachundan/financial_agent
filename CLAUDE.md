# Available Skills

The authoritative graph view of every skill registered for this project lives in [available_skill.md](available_skill.md). Read it when you need to know which skill to invoke, how skills depend on each other, or what the trading pipeline cascade looks like.

**Keep it in sync.** Whenever you add, remove, or change a skill's `## Prerequisites` block under `.claude/skills/`, update `available_skill.md` in the same commit (and bump the "Last updated" date at the top of the file). Specifically:

1. Adding a new skill under `.claude/skills/<name>/SKILL.md` → add a row in the relevant section.
2. Removing a skill → delete its row and any references / arrows in the diagrams.
3. Changing the `[[wikilink]]` upstream deps of a trading-pipeline skill → update the arrow in section 1.
4. Changing the parallel fan-out of [trading-analysis](.claude/skills/trading-analysis/SKILL.md) (e.g. a new analyst joins) → update the diagram.

# Workflow Instructions

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

# UI Verification (MANDATORY)

After adding or modifying any UI feature — especially new buttons, modals, or navigation flows:

1. **Always start the real web server on port 5002** (`preview_start` with port 5002 — do NOT use 5001, that port belongs to the user's running instance).
2. **Click every new button** and verify it performs the correct action (use `preview_eval` to simulate clicks if needed).
3. **Trace JS errors**: use `preview_console_logs` and `preview_eval` to check for `undefined`, `null`, or scoping issues (e.g. variables declared inside an IIFE are not accessible outside it).
4. **Verify navigation flows end-to-end**: if a button should navigate to another view, confirm the target view actually appears.
5. Do not consider UI work done until you have a screenshot or eval result proving each new interaction works.
6. **Always stop the server (`preview_stop` + `lsof -ti :5002 | xargs kill -9`) the moment testing is finished.** Never leave a test server running.

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
