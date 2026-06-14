#!/usr/bin/env bash
#
# backup_dbs_to_gcs.sh — back up the project's large SQLite DBs to Google Cloud Storage.
#
# WHY: db/zsxq.db (~124 MB) exceeds GitHub's 100 MB file limit, so it can no longer
# live in git. Google Cloud Storage (object storage) is the right home for a large
# binary data file. This script also backs up db/notes.db (small, but it holds the
# user's Tier-1 inline comments — worth a second, off-machine copy).
#
# SAFETY:
#   * Uses SQLite's Online-Backup API (`.backup`), which produces a CONSISTENT,
#     non-corrupt snapshot of a LIVE database — safe to run while the :5001 Flask
#     server is reading/writing. It only READS the source; it never modifies it.
#   * Runs `PRAGMA quick_check` on each snapshot before uploading; aborts on failure.
#   * Snapshots are gzip-compressed (SQLite files compress ~3-5x) to cut storage+egress.
#   * Source DBs are opened only via the backup API — no DELETE/UPDATE/VACUUM, in line
#     with the project's DB-safety tiers in CLAUDE.md.
#
# ───────────────────────── ONE-TIME SETUP ─────────────────────────
#   1. Install the Google Cloud SDK:
#        brew install --cask google-cloud-sdk
#   2. Authenticate (opens a browser):
#        gcloud init           # pick/create a project + set defaults
#        gcloud auth login
#   3. Create a bucket (globally-unique name; pick a region near you):
#        gcloud storage buckets create gs://finagent-db-backups \
#            --location=us-west1 --uniform-bucket-level-access
#   4. Turn on object versioning so each upload keeps prior copies (cheap insurance):
#        gcloud storage buckets update gs://finagent-db-backups --versioning
#   5. (optional) auto-delete versions older than 90 days to cap cost — see the
#        lifecycle rule example at the bottom of this file.
#
# ───────────────────────── USAGE ─────────────────────────
#   FINAGENT_GCS_BUCKET=gs://finagent-db-backups ./scripts/backup_dbs_to_gcs.sh
#   # or pass the bucket as the first argument:
#   ./scripts/backup_dbs_to_gcs.sh gs://finagent-db-backups
#
# Lands two objects per DB:  <db>/<db>-YYYYMMDD-HHMMSS.db.gz  (timestamped history)
#                            <db>/<db>-latest.db.gz           (always the newest)
#
# Cost for ~124 MB (Standard class, us-west1): ≈ $0.003/month storage. Negligible.
#
# ───────────────────────── RESTORE ─────────────────────────
#   # Pull the latest snapshot back to a SAFE path (never overwrite a live DB in place):
#   gcloud storage cp gs://finagent-db-backups/zsxq/zsxq-latest.db.gz - | gunzip > /tmp/zsxq_restored.db
#   /opt/anaconda3/bin/sqlite3 "file:/tmp/zsxq_restored.db?mode=ro" 'PRAGMA quick_check;'   # expect: ok
#   # then, with the :5001 server stopped, move it into place:
#   # mv /tmp/zsxq_restored.db db/zsxq.db
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SQLITE="${SQLITE_BIN:-/opt/anaconda3/bin/sqlite3}"     # project interpreter's sqlite3
BUCKET="${FINAGENT_GCS_BUCKET:-${1:-}}"                # env var, else first arg
DBS=("db/zsxq.db" "db/notes.db")                       # add more DBs here if needed

STAMP="$(date +%Y%m%d-%H%M%S)"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# ── preflight ──
if [[ -z "$BUCKET" ]]; then
  echo "ERROR: no target bucket. Set FINAGENT_GCS_BUCKET=gs://your-bucket or pass it as arg 1." >&2
  echo "       (See the ONE-TIME SETUP block at the top of this script.)" >&2
  exit 2
fi
if ! command -v gcloud >/dev/null 2>&1; then
  echo "ERROR: gcloud SDK not found. Install it:  brew install --cask google-cloud-sdk" >&2
  echo "       Then: gcloud init && gcloud auth login   (see setup block at top)." >&2
  exit 3
fi
[[ -x "$SQLITE" ]] || SQLITE="sqlite3"   # fall back to PATH sqlite3 if the anaconda one moved

cd "$PROJECT_DIR"

for DB in "${DBS[@]}"; do
  if [[ ! -f "$DB" ]]; then echo "skip: $DB not found"; continue; fi
  base="$(basename "$DB" .db)"
  snap="$TMPDIR/${base}.db"

  echo "→ ${DB}: snapshotting (read-only Online-Backup API) ..."
  # `.backup` is the SQLite online-backup API: a consistent copy of a live DB, read-only on source.
  "$SQLITE" "$DB" ".backup '$snap'"

  echo "  integrity check ..."
  res="$("$SQLITE" "file:$snap?mode=ro" 'PRAGMA quick_check;' 2>&1 || true)"
  if [[ "$res" != "ok" ]]; then
    echo "  INTEGRITY FAIL on ${DB} snapshot: $res" >&2
    exit 4
  fi

  raw="$(du -h "$snap" | cut -f1)"
  gzip -c "$snap" > "$snap.gz"
  gz="$(du -h "$snap.gz" | cut -f1)"
  echo "  ok (${raw} → ${gz} gzip). uploading ..."

  gcloud storage cp "$snap.gz" "$BUCKET/${base}/${base}-${STAMP}.db.gz"
  gcloud storage cp "$snap.gz" "$BUCKET/${base}/${base}-latest.db.gz"
  echo "  ✓ $BUCKET/${base}/${base}-${STAMP}.db.gz  (and ${base}-latest.db.gz)"
done

echo "done — $(date '+%Y-%m-%d %H:%M:%S')"

# ── optional: cap retention to 90 days (run once; needs a lifecycle.json) ──
#   printf '{"rule":[{"action":{"type":"Delete"},"condition":{"age":90,"isLive":false}}]}' > /tmp/lifecycle.json
#   gcloud storage buckets update gs://finagent-db-backups --lifecycle-file=/tmp/lifecycle.json
