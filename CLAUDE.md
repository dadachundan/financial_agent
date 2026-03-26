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
5. Keep the dev server running after completing tasks (do **not** call `preview_stop()`).
6. If the architecture changes, update `architecture.md`.

# UI Verification (MANDATORY)

After adding or modifying any UI feature — especially new buttons, modals, or navigation flows:

1. **Always start the real web server** (`preview_start`) and load the page.
2. **Click every new button** and verify it performs the correct action (use `preview_eval` to simulate clicks if needed).
3. **Trace JS errors**: use `preview_console_logs` and `preview_eval` to check for `undefined`, `null`, or scoping issues (e.g. variables declared inside an IIFE are not accessible outside it).
4. **Verify navigation flows end-to-end**: if a button should navigate to another view, confirm the target view actually appears.
5. Do not consider UI work done until you have a screenshot or eval result proving each new interaction works.

# Editable Table Columns

When the user asks to make a field in a table editable, always use the `md_comment_widget.py` pattern:

1. The cell contains a `<span class="*-preview" data-raw="...html-escaped markdown...">` that renders markdown on load.
2. Clicking the cell opens a **preview modal** (Bootstrap) showing the rendered markdown + an "Edit" button.
3. Clicking "Edit" closes the preview modal and opens an **EasyMDE editor modal** (with image upload toolbar + clipboard-paste-to-upload support).
4. Saving POSTs the markdown to the backend, then updates `span.dataset.raw` and re-renders the cell in place — no page reload.
5. The backend save route accepts JSON `{"description": "..."}` (or whichever field name) and returns `{"ok": true}`.

See `md_comment_widget.py` for the shared blueprint (`/upload-image`, `/uploads/<path>`) and reference the entity-description implementation in `templates/index.html` (search `viewEntityDesc`) as a concrete example.

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
