---
name: earnings-upload-to-db
description: Batch-ingest earnings PDFs into db/notes.db, mirroring the Notes drag-and-drop UI. Default source = ~/Downloads. Each PDF is deduped by filename, moved into MANUAL_REPORT_DIR/<ticker>/ (fallback "unknown"), filename parsed for ticker / type (10K/10Q/8K/slide/investor) / quarter / report_date, and inserted into the notes table. Use when the user asks to upload, ingest, or import earnings PDFs into the Notes DB, or anything like "add the PDFs in my Downloads to the notes app".
---

# Upload earnings PDFs into db/notes.db

The user wants to bulk-ingest PDFs from a folder (default `~/Downloads`)
into the Notes app's database — same end-state as dragging them onto
the `/notes/` upload zone in the web UI. Files land in
`MANUAL_REPORT_DIR/<ticker>/` (e.g. `Alibaba/`, `Tencent/`); files
without a parseable ticker go to `unknown/`.

## Workflow

### 1. Parse the request

- **Source** — default `~/Downloads` (top-level scan, not recursive).
  Override only if user names a different directory.
- **Move vs copy** — default **move** (matches drag-drop semantics —
  the file leaves `~/Downloads`). Use `--copy` if the user wants the
  source files untouched.
- **Specific files** — if the user lists individual PDF paths, pass
  them as positional args; the `--source` scan is bypassed.

### 2. Run the uploader

```bash
# Default: move every top-level .pdf in ~/Downloads
python3 .claude/skills/earnings-upload-to-db/scripts/upload_pdfs.py

# Different source
python3 .claude/skills/earnings-upload-to-db/scripts/upload_pdfs.py \
    --source ~/Desktop/earnings

# Don't delete originals
python3 .claude/skills/earnings-upload-to-db/scripts/upload_pdfs.py --copy

# Preview (no disk / DB writes)
python3 .claude/skills/earnings-upload-to-db/scripts/upload_pdfs.py --dry-run

# Specific files
python3 .claude/skills/earnings-upload-to-db/scripts/upload_pdfs.py \
    ~/Downloads/Foo.pdf ~/Downloads/Bar.pdf
```

Run it with `/opt/anaconda3/bin/python3` (per
`feedback_anaconda_python_db_scripts` — bare `python3` lacks deps /
has failed DB opens in some shells).

The script prints a single JSON document with `added`, `skipped`,
`errors` arrays plus the totals `added_count` / `skipped_count` /
`error_count` (and `db`, `dest_root`, `mode`, `scanned`). Each `added`
entry includes the parsed `meta` (ticker / type / quarter /
report_date) so you can spot misparsed filenames immediately.

### 3. Report back

Summarise: added N, skipped M (with reasons), errors K. If anything
looks wrong (missing ticker, wrong quarter, report_date not parsed),
flag the filename to the user — they can edit metadata in the UI at
`/notes/`, but if a pattern is broken in the parser fix
`_parse_filename_meta` in `notes_app.py` rather than papering over it
here.

## What the script does under the hood

It collects candidate PDFs and hands each one to
`notes_app.ingest_pdf(filename, saver)` — the **same helper the Flask
`/notes/upload` route uses** — so parsing, dedup, bucketing, and the DB
schema can never diverge from the UI path. (It imports `ingest_pdf`,
`_parse_filename_meta`, `ticker_to_bucket`, `init_db`, `get_conn`,
`MANUAL_REPORT_DIR`, and `DB_PATH` from `notes_app.py`.) Per file:

1. Skip non-PDFs and anything already living under
   `MANUAL_REPORT_DIR` (avoids self-cannibalising re-ingests).
2. `ingest_pdf` skips if `notes.name` already has this filename.
3. Move/copy to `MANUAL_REPORT_DIR/<ticker_bucket>/` — bucket from
   `ticker_to_bucket(meta ticker)`, fallback `unknown/` — auto-renaming
   with `_1.pdf`, `_2.pdf`, … on collision.
4. `INSERT INTO notes (name, local_path, created_at, type, quarter,
   report_date, ticker)` — done inside `ingest_pdf`.

DB and dest dir come from `notes_app.py` — do not hardcode paths in
the skill.

## Notes

- This skill does **not** start the Flask app. The user can browse
  the new rows at `http://xs-macbook-air.local:5001/notes/` after
  running their dev server separately. (Any URL echoed in the final
  reply must use the `xs-macbook-air.local` host, never `localhost` —
  the user browses from iPad.)
- For deeper PDF analysis (annotations, OCR, AI summarisation), the
  Notes UI's "Scan manual_report" button extracts annotations from
  the same files — this skill purposely keeps the DB write minimal
  to avoid divergence.
