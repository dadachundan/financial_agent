#!/usr/bin/env python3
"""
zsxq_downloader.py — Download PDFs from a 知识星球 group into a local directory
                      and record each file in zsxq.db.

Responsibilities
----------------
  1. Authenticate via Selenium (reuses existing Chrome profile).
  2. Fetch the N most-recent file listings from the zsxq API.
  3. Download each PDF that has not been downloaded before (tracked in
     downloaded.json and the SQLite database).
  4. Write download metadata into zsxq.db (file_id, name, local_path, etc.)
     so that zsxq_index.py can classify them offline without re-downloading.

Classification is NOT done here — run zsxq_index.py after downloading.

Usage
-----
    python zsxq_downloader.py --count 10
    python zsxq_downloader.py --count 50 --out ~/Downloads/zsxq_reports
    python zsxq_downloader.py --group-id 51111812185184 --delay 1.5
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from zsxq_common import (
    DEFAULT_CHROME_PROFILE, DEFAULT_DB, DEFAULT_DOWNLOADS,
    do_download, fetch_all_files, get_session_via_selenium,
    init_db, load_tracker, upsert_entry,
)

DEFAULT_GROUP_ID = "51111812185184"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download PDFs from a zsxq group and record them in zsxq.db."
    )
    parser.add_argument("--group-id",       default=DEFAULT_GROUP_ID)
    parser.add_argument("--count",          type=int,   default=10,
                        help="Number of most-recent files to process (0 = all)")
    parser.add_argument("--out",            default=str(DEFAULT_DOWNLOADS),
                        help="Download directory")
    parser.add_argument("--db",             default=str(DEFAULT_DB),
                        help="SQLite database path")
    parser.add_argument("--chrome-profile", default=str(DEFAULT_CHROME_PROFILE))
    parser.add_argument("--delay",          type=float, default=1.0,
                        help="Seconds between downloads")
    parser.add_argument("--skip-existing",  action="store_true", default=True,
                        help="Skip files already in downloaded.json (default: on)")
    args = parser.parse_args()

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
    tracker = load_tracker(out_dir)

    limit_desc = f"last {args.count}" if args.count else "all"
    print(f"Fetching {limit_desc} files from group {args.group_id}…")
    entries     = fetch_all_files(session, args.group_id, max_files=args.count)
    pdf_entries = [e for e in entries if e["file"]["name"].lower().endswith(".pdf")]
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

        print(f"[{i}/{len(pdf_entries)}] {name[:70]}")
        print(f"         size={size_mb:.1f}MB  id={file_id}")

        # ── Upsert metadata (always, even if we skip the actual download) ──
        tracker_info  = tracker.get(str(file_id)) or {}
        local_path    = tracker_info.get("path")
        downloaded_at = tracker_info.get("downloaded_at")

        db_row = {
            "file_id":      file_id,
            "name":         name,
            "topic_id":     topic.get("topic_id"),
            "topic_title":  (talk.get("text") or "").split("\n")[0].strip() or topic.get("title"),
            "summary":      talk.get("text") or "",
            "topic_json":   None,
            "local_path":   local_path,
            "file_size":    f.get("size"),
            "create_time":  f.get("create_time"),
            "downloaded_at":downloaded_at,
            "indexed_at":   now,
        }
        upsert_entry(conn, db_row)
        conn.commit()

        # ── Skip if already downloaded ──
        if args.skip_existing and str(file_id) in tracker:
            print("         → already downloaded, skipping.\n")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
            continue

        # ── Download ──
        local_path, ok = do_download(session, file_id, name, out_dir, tracker,
                                     create_time=f.get("create_time"))
        if ok:
            conn.execute(
                "UPDATE pdf_files SET local_path=?, downloaded_at=? WHERE file_id=?",
                (local_path, tracker[str(file_id)]["downloaded_at"], file_id),
            )
            conn.commit()
            results.append({"file_id": file_id, "name": name, "status": "ok"})
        else:
            results.append({"file_id": file_id, "name": name, "status": "error"})
        print()

        if i < len(pdf_entries):
            time.sleep(args.delay)

    conn.close()

    ok_count      = sum(1 for r in results if r["status"] == "ok")
    skipped_count = sum(1 for r in results if r["status"] == "skipped")
    failed_count  = sum(1 for r in results if r["status"] not in ("ok", "skipped"))
    print(f"Done: {ok_count} downloaded, {skipped_count} skipped, {failed_count} failed.")
    print(f"Output : {out_dir}")
    print(f"DB     : {db_path}")
    print("\nRun zsxq_index.py to classify the downloaded PDFs.")


if __name__ == "__main__":
    main()
