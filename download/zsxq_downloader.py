#!/usr/bin/env python3
"""
zsxq_downloader.py — Download PDFs from a 知识星球 group.

Responsibilities
----------------
  1. Authenticate via Selenium (reuses existing Chrome profile).
  2. Fetch the N most-recent file listings from the zsxq API.
  3. Download each PDF that has not been downloaded before (tracked via the
     SQLite database — local_path IS NOT NULL means already downloaded).
  4. Write download metadata into zsxq.db.

Classification (AI/Robotics/Semi/Energy tags + ticker extraction) used to run
inline via an LLM API — that pipeline has been removed. If you want a PDF
classified, hand it to Claude (the agent) in conversation and ask explicitly.

Usage
-----
    python zsxq_downloader.py                                     # last 100 files per group
    python zsxq_downloader.py --count 50 --out ~/Downloads/zsxq_reports
    python zsxq_downloader.py --group-id 51111812185184 --delay 1.5
    python zsxq_downloader.py --from-date 2025-01-01 --to-date 2025-03-31
    python zsxq_downloader.py --from-date 2025-06-01              # since a date, default --count 100
    python zsxq_downloader.py --from-date 2025-06-01 --count 0   # since a date, no limit
    python zsxq_downloader.py --query qcom                        # search all groups for "qcom" (up to 100 PDFs)
    python zsxq_downloader.py --query qcom --count 0             # search, every matching PDF
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import argparse
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from zsxq_common import (
    DEFAULT_CHROME_PROFILE, DEFAULT_DB, DEFAULT_DOWNLOADS,
    clean_zsxq_text, do_download, extract_bank, fetch_all_files,
    fetch_all_search_results, fetch_all_search_topic_files, find_english_twins,
    sanitize_filename, get_session_via_selenium, init_db, is_chinese_filename,
    query_in_filename, upsert_entry,
    ZsxqAuthError,
)

GROUP_ALIASES = {
    "1": "51111812185184",
    "2": "28888824254221",
    "3": "51288148188224",
}

# Groups that are EXEMPT from the ">3 files per topic" skip rule. Most groups
# post paid/one-for-one packs as big multi-file topics we want to skip, but
# 猫哥的研报圈 (51288148188224) legitimately bundles a whole day's broker notes
# (often 8-9 PDFs) into a single post — so for this group we download every
# attachment regardless of how many files the topic carries.
BULK_EXEMPT_GROUPS = {
    "51288148188224",  # 猫哥的研报圈
}
ALL_GROUP_IDS = list(GROUP_ALIASES.values())


def _refresh_session_after_auth_error(chrome_profile: Path, exc: ZsxqAuthError):
    print(f"\nAuthentication failed: {exc}")
    print("Cached cookies look stale; retrying once with fresh Chrome-profile cookies...")
    return get_session_via_selenium(chrome_profile, use_json_cache=False)


def _drop_english_twins(pdf_entries: list[dict], conn) -> tuple[list[dict], dict]:
    """Skip Chinese-titled copies of English broker notes (see find_english_twins).

    Candidates are this batch plus DB rows from the same window. Strong matches
    (and files an earlier run already flagged skipped=1) are dropped now; weak
    matches come back as {file_id: twin names} for _drop_weak_twins to confirm
    by page count after download.
    """
    dates = [(e["file"].get("create_time") or "")[:10] for e in pdf_entries]
    dates = [d for d in dates if d]
    if not dates:
        return pdf_entries, {}
    since = (datetime.fromisoformat(min(dates)) - timedelta(days=4)).date().isoformat()
    rows = conn.execute(
        "SELECT file_id, name, create_time, skipped FROM pdf_files WHERE create_time >= ?",
        (since,),
    ).fetchall()
    flagged = {r["file_id"] for r in rows if r["skipped"]}
    cands = {r["name"]: r["create_time"] for r in rows}
    for e in pdf_entries:
        cands.setdefault(e["file"]["name"], e["file"].get("create_time"))
    cand_list = list(cands.items())

    kept, weak, dropped = [], {}, 0
    for e in pdf_entries:
        f = e["file"]
        if f["file_id"] in flagged:
            dropped += 1
            continue
        twins, strong = find_english_twins(f["name"], f.get("create_time"), cand_list)
        if twins and strong:
            dropped += 1
            continue
        if twins:
            weak[f["file_id"]] = twins
        kept.append(e)
    if dropped:
        print(f"Skipped {dropped} Chinese-titled copy(ies) of English broker notes.")
    return kept, weak


def _drop_weak_twins(conn, results: list[dict], weak: dict) -> None:
    """Delete freshly downloaded weak twins whose page count equals a
    downloaded English twin's, and flag them skipped=1 so later runs skip them."""
    for r in results:
        twins = weak.get(r["file_id"])
        if not twins or r["status"] != "ok":
            continue
        row = conn.execute(
            "SELECT local_path, page_count FROM pdf_files WHERE file_id = ?",
            (r["file_id"],),
        ).fetchone()
        twin_pages = {
            p: n for (n, p) in conn.execute(
                f"SELECT name, page_count FROM pdf_files WHERE local_path IS NOT NULL "
                f"AND name IN ({','.join('?' * len(twins))})", twins,
            )
        }
        if row and row["page_count"] and row["page_count"] in twin_pages:
            Path(row["local_path"]).unlink(missing_ok=True)
            conn.execute(
                "UPDATE pdf_files SET local_path=NULL, downloaded_at=NULL, skipped=1 "
                "WHERE file_id = ?", (r["file_id"],),
            )
            r["status"] = "skipped"
            print(f"Removed {r['name'][:60]} — same {row['page_count']}pp as English "
                  f"original {twin_pages[row['page_count']][:50]}")
    conn.commit()


def _run_group(group_id: str, args, session, conn, out_dir: Path,
               from_date, to_date) -> list[dict]:
    """Fetch and download PDFs for a single group. Returns results list."""
    from collections import Counter

    fetch_max = args.count
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

    print(f"\n{'='*60}")
    print(f"Fetching {limit_desc} from group {group_id}…")
    entries = fetch_all_files(
        session, group_id,
        max_files=fetch_max,
        from_date=from_date,
    )

    pdf_entries = [e for e in entries if e["file"]["name"].lower().endswith(".pdf")]

    # Skip PPTX / XLSX files
    skipped_non_pdf = sum(1 for e in entries
                          if e["file"]["name"].lower().endswith((".pptx", ".xlsx")))
    if skipped_non_pdf:
        print(f"Skipped {skipped_non_pdf} PPTX/XLSX file(s).")

    # Skip Chinese-content files (predicted from the filename — see
    # is_chinese_filename), plus 三个皮匠报告 / 景略咨询 files
    before_cn = len(pdf_entries)
    pdf_entries = [
        e for e in pdf_entries
        if not is_chinese_filename(e["file"]["name"])
        and "三个皮匠报告" not in e["file"]["name"]
        and "景略咨询" not in e["file"]["name"]
    ]
    skipped_cn = before_cn - len(pdf_entries)
    if skipped_cn:
        print(f"Skipped {skipped_cn} Chinese-content (by filename)/三个皮匠报告/景略咨询 file(s).")

    # Skip topics with more than 3 files (one-for-one / paid packs),
    # except topics tagged #外资研报 which routinely bundle a day's notes.
    topic_file_counts = Counter(
        (e.get("topic") or {}).get("topic_id") for e in entries
    )
    exempt_topic_ids = {
        tid
        for e in entries
        if (tid := (e.get("topic") or {}).get("topic_id")) is not None
        and "#外资研报" in clean_zsxq_text(
            ((e.get("topic") or {}).get("talk") or {}).get("text") or ""
        )
    }
    if group_id in BULK_EXEMPT_GROUPS:
        print("Group is exempt from the >3-attachments skip rule; keeping all files.")
    else:
        before_bulk = len(pdf_entries)
        pdf_entries = [
            e for e in pdf_entries
            if (tid := (e.get("topic") or {}).get("topic_id")) is None
            or topic_file_counts[tid] <= 3
            or tid in exempt_topic_ids
        ]
        skipped_bulk = before_bulk - len(pdf_entries)
        if skipped_bulk:
            print(f"Skipped {skipped_bulk} file(s) from topics with >3 attachments "
                  f"(#外资研报 exempt).")

    pdf_entries, weak_twins = _drop_english_twins(pdf_entries, conn)

    # Apply to_date upper bound
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
        summary = clean_zsxq_text(talk.get("text") or "")

        date_str = (f.get("create_time") or "")[:10]
        print(f"[{i}/{len(pdf_entries)}] {name[:70]}")
        print(f"         date={date_str}  size={size_mb:.1f}MB  id={file_id}")

        # ── Skip if same filename already exists in DB (any group) ──────
        name_existing = conn.execute(
            "SELECT file_id FROM pdf_files WHERE name = ? AND file_id != ?",
            (name, file_id),
        ).fetchone()
        if name_existing:
            print(f"         → duplicate filename (id={name_existing['file_id']}), skipping.")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
            continue

        existing = conn.execute(
            "SELECT local_path, downloaded_at FROM pdf_files WHERE file_id = ?",
            (file_id,),
        ).fetchone()
        local_path    = existing["local_path"]    if existing else None
        downloaded_at = existing["downloaded_at"] if existing else None

        db_row = {
            "file_id":      file_id,
            "name":         name,
            "topic_id":     topic.get("topic_id"),
            "topic_title":  summary.split("\n")[0].strip() or clean_zsxq_text(topic.get("title") or ""),
            "summary":      summary,
            "topic_json":   None,
            "local_path":   local_path,
            "file_size":    f.get("size"),
            "create_time":  f.get("create_time"),
            "downloaded_at": downloaded_at,
            "indexed_at":   now,
            "group_id":     group_id,
        }
        upsert_entry(conn, db_row)

        bank = extract_bank(name)
        conn.execute("UPDATE pdf_files SET bank=?, skipped=0 WHERE file_id=?", (bank, file_id))
        conn.commit()

        already_downloaded = local_path is not None
        if already_downloaded:
            print("         → already downloaded, skipping download.")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
        else:
            dl_ts = datetime.now().isoformat()
            local_path, ok, pages = do_download(
                session, file_id, name, out_dir,
                create_time=f.get("create_time"),
            )
            if ok:
                conn.execute(
                    "UPDATE pdf_files SET local_path=?, downloaded_at=?, page_count=? WHERE file_id=?",
                    (local_path, dl_ts, pages, file_id),
                )
                conn.commit()
                results.append({"file_id": file_id, "name": name, "status": "ok"})
            else:
                results.append({"file_id": file_id, "name": name, "status": "error"})
                print()
                if i < len(pdf_entries):
                    time.sleep(args.delay)
                continue

        print()
        if i < len(pdf_entries) and not already_downloaded:
            time.sleep(args.delay)

    _drop_weak_twins(conn, results, weak_twins)
    return results


def _run_query(query: str, args, session, conn, out_dir: Path) -> list[dict]:
    """Search all groups for *query* and download matching PDFs.

    Files are saved into out_dir/<query>/ (flat, no date subfolder).
    """
    from collections import Counter

    query_dir = out_dir / sanitize_filename(query)
    query_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Searching all groups for: {query!r}  (全部星球)…")
    print(f"Output folder: {query_dir}")

    # 1) Files search
    print(f"\n[1/2] Files search…")
    # Fetch every search hit; --count (default 100) is applied only after the
    # PDF / Chinese-filename / bulk-topic filters below, so it counts PDFs
    # that will actually be downloaded rather than raw hits.
    file_entries = fetch_all_search_results(session, query, max_files=0)

    # 2) Topics search — pulls all attachments from matching posts
    print(f"\n[2/2] Topics search…")
    topic_entries = fetch_all_search_topic_files(
        session, query,
        max_topics=0,
    )

    # Merge: files-search results take priority (more metadata); add topic-only extras
    seen: dict[int, dict] = {e["file"]["file_id"]: e for e in file_entries}
    added_from_topics = 0
    for e in topic_entries:
        fid = e["file"]["file_id"]
        if fid not in seen:
            seen[fid] = e
            added_from_topics += 1
    entries = list(seen.values())
    print(f"\nCombined: {len(file_entries)} (files) + {added_from_topics} new from topics "
          f"= {len(entries)} unique files.")

    pdf_entries = [e for e in entries if e["file"]["name"].lower().endswith(".pdf")]
    skipped_non_pdf = len(entries) - len(pdf_entries)
    if skipped_non_pdf:
        print(f"Skipped {skipped_non_pdf} non-PDF file(s).")

    before_rel = len(pdf_entries)
    pdf_entries = [e for e in pdf_entries if query_in_filename(query, e["file"]["name"])]
    skipped_rel = before_rel - len(pdf_entries)
    if skipped_rel:
        print(f"Skipped {skipped_rel} file(s) without {query!r} as a whole word in the "
              f"filename (e.g. Metals, MetaX).")

    before_cn = len(pdf_entries)
    pdf_entries = [
        e for e in pdf_entries
        if not is_chinese_filename(e["file"]["name"])
        and "三个皮匠报告" not in e["file"]["name"]
        and "景略咨询" not in e["file"]["name"]
    ]
    skipped_cn = before_cn - len(pdf_entries)
    if skipped_cn:
        print(f"Skipped {skipped_cn} Chinese-content (by filename)/三个皮匠报告/景略咨询 file(s).")

    topic_file_counts = Counter(
        (e.get("topic") or {}).get("topic_id") for e in entries
    )
    exempt_topic_ids = {
        tid
        for e in entries
        if (tid := (e.get("topic") or {}).get("topic_id")) is not None
        and "#外资研报" in clean_zsxq_text(
            ((e.get("topic") or {}).get("talk") or {}).get("text") or ""
        )
    }
    before_bulk = len(pdf_entries)
    pdf_entries = [
        e for e in pdf_entries
        if (tid := (e.get("topic") or {}).get("topic_id")) is None
        or topic_file_counts[tid] <= 3
        or tid in exempt_topic_ids
    ]
    skipped_bulk = before_bulk - len(pdf_entries)
    if skipped_bulk:
        print(f"Skipped {skipped_bulk} file(s) from topics with >3 attachments "
              f"(#外资研报 exempt).")

    pdf_entries, weak_twins = _drop_english_twins(pdf_entries, conn)

    # The search API returns hits in relevance order; sort newest-first so the
    # --count cap keeps the most recent PDFs.
    pdf_entries.sort(key=lambda e: e["file"].get("create_time") or "", reverse=True)

    cap = args.count
    if cap and len(pdf_entries) > cap:
        print(f"Capped {len(pdf_entries)} PDF(s) at {cap} (--count limit).")
        pdf_entries = pdf_entries[:cap]

    print(f"Found {len(pdf_entries)} PDF(s) matching {query!r}.\n")

    results: list[dict] = []
    now = datetime.now().isoformat()

    for i, entry in enumerate(pdf_entries, 1):
        f       = entry["file"]
        topic   = entry.get("topic") or {}
        talk    = (topic.get("talk") or {})
        file_id = f["file_id"]
        name    = f["name"]
        size_mb = (f.get("size") or 0) / 1024 / 1024
        summary = clean_zsxq_text(talk.get("text") or "")
        group_id = str((entry.get("group") or {}).get("group_id") or "")

        date_str = (f.get("create_time") or "")[:10]
        print(f"[{i}/{len(pdf_entries)}] {name[:70]}")
        print(f"         date={date_str}  size={size_mb:.1f}MB  id={file_id}")

        # Skip if same filename already exists (different file_id)
        name_existing = conn.execute(
            "SELECT file_id FROM pdf_files WHERE name = ? AND file_id != ?",
            (name, file_id),
        ).fetchone()
        if name_existing:
            print(f"         → duplicate filename (id={name_existing['file_id']}), skipping.")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
            continue

        existing = conn.execute(
            "SELECT local_path, downloaded_at FROM pdf_files WHERE file_id = ?",
            (file_id,),
        ).fetchone()
        local_path    = existing["local_path"]    if existing else None
        downloaded_at = existing["downloaded_at"] if existing else None

        db_row = {
            "file_id":      file_id,
            "name":         name,
            "topic_id":     topic.get("topic_id"),
            "topic_title":  summary.split("\n")[0].strip() or clean_zsxq_text(topic.get("title") or ""),
            "summary":      summary,
            "topic_json":   None,
            "local_path":   local_path,
            "file_size":    f.get("size"),
            "create_time":  f.get("create_time"),
            "downloaded_at": downloaded_at,
            "indexed_at":   now,
            "group_id":     group_id,
            "query_term":   query,
        }
        upsert_entry(conn, db_row)

        bank = extract_bank(name)
        conn.execute("UPDATE pdf_files SET bank=?, skipped=0 WHERE file_id=?", (bank, file_id))
        conn.commit()

        already_downloaded = local_path is not None
        if already_downloaded:
            print("         → already downloaded, skipping download.")
            results.append({"file_id": file_id, "name": name, "status": "skipped"})
        else:
            dl_ts = datetime.now().isoformat()
            local_path, ok, pages = do_download(
                session, file_id, name, query_dir,
                use_date_subfolder=False,
            )
            if ok:
                conn.execute(
                    "UPDATE pdf_files SET local_path=?, downloaded_at=?, page_count=? WHERE file_id=?",
                    (local_path, dl_ts, pages, file_id),
                )
                conn.commit()
                results.append({"file_id": file_id, "name": name, "status": "ok"})
            else:
                results.append({"file_id": file_id, "name": name, "status": "error"})
                print()
                if i < len(pdf_entries):
                    time.sleep(args.delay)
                continue

        print()
        if i < len(pdf_entries) and not already_downloaded:
            time.sleep(args.delay)

    _drop_weak_twins(conn, results, weak_twins)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download PDFs from a zsxq group and record them in zsxq.db."
    )
    parser.add_argument("--query",          default=None, metavar="KEYWORD",
                        help="Search all groups (全部星球) for files matching this term "
                             "and download them. Records query_term in the DB.")
    parser.add_argument("--group-id",       default=None,
                        help="Full group ID. If omitted, both groups are downloaded.")
    parser.add_argument("--group",          default=None, metavar="N",
                        help="Group shorthand: 1=51111812185184, 2=28888824254221, "
                             "3=51288148188224")
    parser.add_argument("--count",          type=int,   default=100,
                        help="Max files per group, or max PDFs to download after "
                             "filtering with --query. 0 = unlimited.")
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
    args = parser.parse_args()

    # Resolve which group(s) to run
    if args.group is not None:
        if args.group not in GROUP_ALIASES:
            print(f"ERROR: --group must be one of: {', '.join(GROUP_ALIASES)} "
                  f"(got {args.group!r})")
            sys.exit(1)
        group_ids = [GROUP_ALIASES[args.group]]
    elif args.group_id is not None:
        group_ids = [args.group_id]
    else:
        group_ids = ALL_GROUP_IDS  # default: both groups

    chrome_profile = Path(args.chrome_profile).expanduser()
    if not chrome_profile.exists():
        print(f"ERROR: Chrome profile not found at {chrome_profile}")
        print("Make sure chrome_profile/ exists and you've logged into wx.zsxq.com.")
        sys.exit(1)

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(args.db).expanduser()

    # Validate date formats early
    from_date = args.from_date
    to_date   = args.to_date
    for label, val in [("--from-date", from_date), ("--to-date", to_date)]:
        if val:
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                print(f"ERROR: {label} must be in YYYY-MM-DD format, got: {val!r}")
                sys.exit(1)

    session = get_session_via_selenium(chrome_profile)
    conn    = init_db(db_path)

    all_results: list[dict] = []

    if args.query:
        try:
            results = _run_query(args.query, args, session, conn, out_dir)
        except ZsxqAuthError as exc:
            session = _refresh_session_after_auth_error(chrome_profile, exc)
            results = _run_query(args.query, args, session, conn, out_dir)
        all_results.extend(results)
    else:
        for group_id in group_ids:
            try:
                results = _run_group(group_id, args, session, conn, out_dir,
                                     from_date, to_date)
            except ZsxqAuthError as exc:
                session = _refresh_session_after_auth_error(chrome_profile, exc)
                results = _run_group(group_id, args, session, conn, out_dir,
                                     from_date, to_date)
            all_results.extend(results)

    conn.close()

    ok_count      = sum(1 for r in all_results if r["status"] == "ok")
    skipped_count = sum(1 for r in all_results if r["status"] == "skipped")
    failed_count  = sum(1 for r in all_results if r["status"] not in ("ok", "skipped"))
    print(f"\nTotal: {ok_count} downloaded, {skipped_count} skipped, {failed_count} failed.")
    print(f"Output : {out_dir}")
    print(f"DB     : {db_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
