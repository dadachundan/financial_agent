#!/usr/bin/env python3
"""
zsxq_downloader.py — Download PDFs from a 知识星球 group and classify them.

Responsibilities
----------------
  1. Authenticate via Selenium (reuses existing Chrome profile).
  2. Fetch the N most-recent file listings from the zsxq API.
  3. Download each PDF that has not been downloaded before (tracked via the
     SQLite database — local_path IS NOT NULL means already downloaded).
  4. Write download metadata into zsxq.db.
  5. Classify each PDF via MiniMax immediately after download (unless
     --no-classify is passed).  Already-classified rows are skipped.

Run zsxq_index.py for bulk re-classification with a different prompt.

Usage
-----
    python zsxq_downloader.py --count 10
    python zsxq_downloader.py --count 50 --out ~/Downloads/zsxq_reports
    python zsxq_downloader.py --group-id 51111812185184 --delay 1.5
    python zsxq_downloader.py --no-classify          # download only, skip LLM step
    python zsxq_downloader.py --from-date 2025-01-01 --to-date 2025-03-31
    python zsxq_downloader.py --from-date 2025-06-01              # since a date, default --count 10
    python zsxq_downloader.py --from-date 2025-06-01 --count 0   # since a date, no limit
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from zsxq_classify import classify_one
from zsxq_common import (
    DEFAULT_CHROME_PROFILE, DEFAULT_DB, DEFAULT_DOWNLOADS,
    do_download, fetch_all_files, get_session_via_selenium,
    init_db, upsert_entry,
)

DEFAULT_GROUP_ID = "51111812185184"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download PDFs from a zsxq group, record them in zsxq.db, "
                    "and classify each one via MiniMax."
    )
    parser.add_argument("--group-id",       default=DEFAULT_GROUP_ID)
    parser.add_argument("--count",          type=int,   default=10,
                        help="Max files to fetch (0 = unlimited); also applies with --from-date / --to-date")
    parser.add_argument("--from-date",      default=None, metavar="YYYY-MM-DD",
                        help="Only process files published on or after this date")
    parser.add_argument("--to-date",        default=None, metavar="YYYY-MM-DD",
                        help="Only process files published on or before this date")
    parser.add_argument("--out",            default=str(DEFAULT_DOWNLOADS),
                        help="Download directory")
    parser.add_argument("--db",             default=str(DEFAULT_DB),
                        help="SQLite database path")
    parser.add_argument("--chrome-profile", default=str(DEFAULT_CHROME_PROFILE))
    parser.add_argument("--delay",          type=float, default=1.0,
                        help="Seconds between downloads")
    parser.add_argument("--classify-delay", type=float, default=1.0,
                        help="Seconds between MiniMax API calls (default: 1.0)")
    parser.add_argument("--no-classify",    action="store_true",
                        help="Skip MiniMax classification after download")
    args = parser.parse_args()

    # ── Check API key early if we'll need it ──────────────────────────────
    api_key = None
    if not args.no_classify:
        try:
            from minimax import MINIMAX_API_KEY  # type: ignore
            api_key = MINIMAX_API_KEY
        except ImportError:
            pass
        if not api_key:
            print("WARNING: MINIMAX_API_KEY not found in config.py — "
                  "classification will be skipped (pass --no-classify to suppress this warning).")
            args.no_classify = True

    chrome_profile = Path(args.chrome_profile).expanduser()
    if not chrome_profile.exists():
        print(f"ERROR: Chrome profile not found at {chrome_profile}")
        print("Make sure chrome_profile/ exists and you've logged into wx.zsxq.com.")
        sys.exit(1)

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(args.db).expanduser()

    session = get_session_via_selenium(chrome_profile)
    conn    = init_db(db_path)

    from_date = args.from_date
    to_date   = args.to_date

    # Validate date formats early
    for label, val in [("--from-date", from_date), ("--to-date", to_date)]:
        if val:
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                print(f"ERROR: {label} must be in YYYY-MM-DD format, got: {val!r}")
                sys.exit(1)

    fetch_max = args.count  # 0 = unlimited; respected even with date filters

    if from_date or to_date:
        date_desc = (
            f"between {from_date} and {to_date}" if (from_date and to_date)
            else f"from {from_date} onwards"     if from_date
            else f"up to {to_date}"
        )
        count_desc = f"up to {fetch_max} " if fetch_max else ""
        limit_desc = f"{count_desc}files {date_desc}"
    else:
        limit_desc = f"last {fetch_max}" if fetch_max else "all"

    print(f"Fetching {limit_desc} from group {args.group_id}…")
    entries = fetch_all_files(
        session, args.group_id,
        max_files=fetch_max,
        from_date=from_date,
    )

    pdf_entries = [e for e in entries if e["file"]["name"].lower().endswith(".pdf")]

    # Apply to_date upper bound (fetch_all_files doesn't filter this end)
    if to_date:
        pdf_entries = [
            e for e in pdf_entries
            if (e["file"].get("create_time") or "")[:10] <= to_date
        ]

    print(f"Found {len(pdf_entries)} PDF(s) (of {len(entries)} total files).\n")

    results: list[dict] = []
    now = datetime.now().isoformat()

    for i, entry in enumerate(pdf_entries, 1):
        f       = entry["file"]
        topic   = entry.get("topic") or {}
        talk    = (topic.get("talk") or {})
        file_id = f["file_id"]
        name    = f["name"]
        size_mb = (f.get("size") or 0) / 1024 / 1024
        summary = talk.get("text") or ""

        date_str = (f.get("create_time") or "")[:10]
        print(f"[{i}/{len(pdf_entries)}] {name[:70]}")
        print(f"         date={date_str}  size={size_mb:.1f}MB  id={file_id}")

        # ── Look up existing DB record for this file ──────────────────────
        existing = conn.execute(
            "SELECT local_path, downloaded_at FROM pdf_files WHERE file_id = ?",
            (file_id,),
        ).fetchone()
        local_path    = existing["local_path"]    if existing else None
        downloaded_at = existing["downloaded_at"] if existing else None

        # ── Upsert metadata (always, even if we skip the actual download) ──
        db_row = {
            "file_id":      file_id,
            "name":         name,
            "topic_id":     topic.get("topic_id"),
            "topic_title":  (summary).split("\n")[0].strip() or topic.get("title"),
            "summary":      summary,
            "topic_json":   None,
            "local_path":   local_path,
            "file_size":    f.get("size"),
            "create_time":  f.get("create_time"),
            "downloaded_at": downloaded_at,
            "indexed_at":   now,
        }
        upsert_entry(conn, db_row)
        conn.commit()

        # ── Skip download if already done (local_path exists in DB) ──────
        already_downloaded = local_path is not None
        if already_downloaded:
            print("         → already downloaded, skipping download.")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
        else:
            # ── Download ──
            dl_ts = datetime.now().isoformat()
            local_path, ok = do_download(
                session, file_id, name, out_dir,
                create_time=f.get("create_time"),
            )
            if ok:
                conn.execute(
                    "UPDATE pdf_files SET local_path=?, downloaded_at=? WHERE file_id=?",
                    (local_path, dl_ts, file_id),
                )
                conn.commit()
                results.append({"file_id": file_id, "name": name, "status": "ok"})
            else:
                results.append({"file_id": file_id, "name": name, "status": "error"})
                print()
                if i < len(pdf_entries):
                    time.sleep(args.delay)
                continue

        # ── Classify (unless disabled or already classified) ──────────────
        if not args.no_classify:
            row = conn.execute(
                "SELECT ai_related FROM pdf_files WHERE file_id = ?", (file_id,)
            ).fetchone()
            already_classified = row and row["ai_related"] is not None
            if already_classified:
                print("         → already classified, skipping LLM.")
            else:
                print("         → classifying via MiniMax…")
                try:
                    result = classify_one(
                        conn, file_id, name, summary, api_key,
                        local_path=local_path,
                    )
                    flags = [label for label, hit in [
                        ("AI", result["ai"]), ("Robotics", result["robotics"]),
                        ("Semi", result["semiconductor"]), ("Energy", result["energy"]),
                    ] if hit]
                    cat_str = ("✓ " + ", ".join(flags)) if flags else "✗ None"
                    print(f"         → {cat_str}  [{result['elapsed']:.1f}s]")
                    if result["tickers"]:
                        print(f"         → Tickers: {result['tickers']}")
                    if i < len(pdf_entries):
                        time.sleep(args.classify_delay)
                except Exception as exc:
                    print(f"         ⚠ Classification failed: {exc}")

        print()
        if i < len(pdf_entries) and not already_downloaded:
            time.sleep(args.delay)

    conn.close()

    ok_count      = sum(1 for r in results if r["status"] == "ok")
    skipped_count = sum(1 for r in results if r["status"] == "skipped")
    failed_count  = sum(1 for r in results if r["status"] not in ("ok", "skipped"))
    print(f"Done: {ok_count} downloaded, {skipped_count} skipped, {failed_count} failed.")
    print(f"Output : {out_dir}")
    print(f"DB     : {db_path}")
    if args.no_classify:
        print("\nRun zsxq_index.py to classify the downloaded PDFs.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
