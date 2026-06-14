#!/usr/bin/env bash
#
# weekly_db_commit.sh — auto-commit the project's tracked SQLite DBs once a week.
#
# Driven by the launchd agent com.finagent.weekly-db-commit (see
# ~/Library/LaunchAgents/com.finagent.weekly-db-commit.plist). Commits ONLY
# db/zsxq.db (Git LFS) and db/notes.db — it never sweeps up other working-tree
# changes (uses `git commit -- <paths>`, the pathspec form). Push failures are
# non-fatal: the commit is saved locally and the next run (or a manual push)
# catches up.
#
# Manual run / test:  bash scripts/weekly_db_commit.sh
# Logs to:            log/weekly_db_commit.log
#
set -uo pipefail

# launchd runs with a minimal environment — set PATH so Apple git (/usr/bin) AND
# git-lfs (/opt/homebrew/bin, needed by the LFS filter on push) are both found.
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO="/Users/x/projects/financial_agent"
SQLITE="/opt/anaconda3/bin/sqlite3"
DBS=("db/zsxq.db" "db/notes.db")
TS() { date '+%Y-%m-%d %H:%M:%S'; }

cd "$REPO" || { echo "$(TS)  ERROR: cannot cd $REPO"; exit 1; }

# Safety: only auto-commit on main, so a feature-branch checkout is never disturbed.
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
if [[ "$branch" != "main" ]]; then
  echo "$(TS)  skip: on branch '$branch', not main"; exit 0
fi

# Anything changed among the DB files? (covers staged + unstaged)
if [[ -z "$(git status --porcelain -- "${DBS[@]}")" ]]; then
  echo "$(TS)  no DB changes — nothing to commit"; exit 0
fi

# Integrity-guard: never commit a corrupt DB. quick_check via a read-only handle.
for DB in "${DBS[@]}"; do
  [[ -f "$DB" ]] || continue
  res="$("$SQLITE" "file:$DB?mode=ro" 'PRAGMA quick_check;' 2>&1 | head -1 || true)"
  if [[ "$res" != "ok" ]]; then
    echo "$(TS)  ABORT: integrity check failed on $DB: $res"; exit 2
  fi
done

# Commit ONLY the DB paths (pathspec form — ignores any other staged/unstaged work).
if git commit -q -m "chore(db): weekly auto-commit of tracked SQLite DBs ($(date '+%Y-%m-%d'))" -- "${DBS[@]}"; then
  echo "$(TS)  committed $(git rev-parse --short HEAD)"
else
  echo "$(TS)  nothing committed (no net change after staging)"; exit 0
fi

# Push (LFS uploads zsxq.db automatically). Non-fatal — commit is already saved locally.
if git push -q origin HEAD:main; then
  echo "$(TS)  pushed to origin/main"
else
  rc=$?
  echo "$(TS)  WARN: push failed (rc=$rc) — commit saved locally, will retry next run."
  echo "$(TS)        If this is an LFS over-quota error, see ARCHITECTURE.md (LFS free tier = 1 GB)."
fi
