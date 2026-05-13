---
name: recommend-zsxq-pdf
description: Recommend zsxq reports to read by scanning the most-recent rows of db/zsxq.db (titles + summaries — no PDF parsing). Default: latest 50 reports, focus on AI / robotics. User may override with a count ("latest 100") and/or a subject ("focus on semiconductors", "anything on EVs"). When the user has no clue, group the recent feed into themes and surface a handful of standout reads.
---

# Recommend zsxq PDF

The user wants a curated pointer into the recent zsxq report feed —
**not** a deep read of any single PDF. Work only from
`db/zsxq.db.pdf_files`'s metadata columns (title, summary, tags, etc.).
Do not extract or open PDFs. (If they want a deep dive on a specific
report, the `analyze-zsxq` skill handles that.)

## Workflow

### 1. Parse the request

Pull out three optional knobs from the user's prompt:

- **Count** — "latest 50" (default), "latest 100", "last week", etc.
  Map to `--limit N` or `--since YYYY-MM-DD`.
- **Subject** — explicit topic ("semiconductors", "EVs", "中东"), or
  none. If none, **default focus = AI + robotics**.
- **Vibe** — does the user know what they want, or are they fishing?
  Wording like "summarize for me", "anything interesting", "what
  should I read" → fishing mode (theme-cluster + 3-5 picks).

### 2. Pull recent rows

```bash
# Latest 50 (default)
python3 .claude/skills/recommend-zsxq-pdf/scripts/list_recent.py

# Latest 100
python3 .claude/skills/recommend-zsxq-pdf/scripts/list_recent.py --limit 100

# Coarse subject filter before Claude ranks (only when the user named one)
python3 .claude/skills/recommend-zsxq-pdf/scripts/list_recent.py \
    --limit 100 --subject "semiconductor"

# Recency window
python3 .claude/skills/recommend-zsxq-pdf/scripts/list_recent.py \
    --since 2026-05-01
```

Flags:

- `--limit N` (default 50)
- `--subject TEXT` — case-insensitive LIKE on
  name/topic_title/summary/tags/comment. **Only pass this when the
  user gave an explicit subject.** Default AI/robotics focus is done
  by Claude in step 3, not by SQL — the boolean `ai_robotics_related`
  / `ai_related` / `robotics_related` columns are sparsely populated,
  so don't rely on them as a hard filter.
- `--since YYYY-MM-DD` — only rows newer than this.
- `--summary-chars N` — truncate each summary (default 1500). Bump to
  0 if the user wants very detailed picks, drop to ~500 for 100+ rows.

Output: JSON `{count, generated_at, filters, rows:[…]}`. Each row has
`file_id, name, topic_title, summary, create_time, page_count, tickers,
tags, comment, bank, ai_robotics_related, ai_related, robotics_related,
semiconductor_related, energy_related, claude_rating, user_rating`.

### 3. Rank and recommend (Claude does this in-context)

Read every row's `topic_title` + `summary`. Then:

**If the user named a subject** — pick the 5-10 most relevant reports
and explain *why* each one fits. Ignore the rest. If only 1-2 truly
match, say so honestly rather than padding.

**If no subject (default = AI/robotics)** — score each row on
AI / robotics / adjacent (semis, infra, data, autonomy). Surface 5-10
top picks across these subthemes. Down-weight pure macro / general
strategy unless tightly AI-linked.

**If the user is fishing** ("summarize for me", "what's interesting") —
first cluster the recent feed into 3-6 themes ("AI capex /
inference economics", "robotics + autonomy", "energy & power",
"China consumer slowdown", "geopolitics", …) with a one-line gist
each. Then pick 2-3 standout reads under each theme.

### 4. Output format

For each recommendation give:

- `file_id` (so the user can hand it to `/analyze-zsxq`)
- Bank / publisher if known (`bank` column, or extract from name)
- A ≤2-sentence "why read this" — anchored in the actual summary, not
  generic.
- Page count + create_time when useful for triage.

Markdown table when listing >3 picks. Keep the whole reply tight — the
user is choosing what to read next, not consuming the reports here.

## Notes

- DB is read-only here. Never write to `db/zsxq.db` from this skill.
- Do **not** open the PDF files. Title + summary is the contract.
- If `count == 0` (empty filter result), tell the user the filter and
  suggest relaxing it (drop the subject, widen `--since`).
- The `tickers` / `claude_rating` / `user_rating` columns are sparse
  but valuable when present — mention them in the "why" line if a
  recommended row has them populated.
- This skill pairs with `analyze-zsxq`: recommend here → user picks a
  `file_id` → `/analyze-zsxq <question> file_id <N>` for the deep
  read.
