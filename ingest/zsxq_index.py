#!/usr/bin/env python3
"""
zsxq_index.py — Batch-classify PDFs already stored in zsxq.db using MiniMax.

Responsibilities
----------------
  Purely an OFFLINE classifier: reads rows from the local SQLite database
  (written by zsxq_downloader.py) and calls MiniMax to classify each PDF
  across four categories:  AI | Robotics | Semiconductor | Energy

  Because classification is decoupled from downloading, you can:
    • Change the prompt and re-run without re-downloading everything.
    • Run in batch after a bulk download.
    • Trigger auto-downloads only for PDFs that match at least one category.

Usage
-----
    # Classify all unclassified rows (default)
    python zsxq_index.py

    # Re-classify every row (useful after a prompt change)
    python zsxq_index.py --reclassify

    # Classify only the N most-recently indexed files
    python zsxq_index.py --count 20

Requirements
------------
  • zsxq.db must already exist (run zsxq_downloader.py first).
  • MINIMAX_API_KEY must be set in config.py.
  • Chrome profile is only needed for auto-downloading matched PDFs that are
    not yet on disk.  If you pass --no-autodownload the Chrome profile is
    never touched.
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from minimax import MINIMAX_API_KEY as _CONFIG_MINIMAX_KEY  # type: ignore

from zsxq_classify import classify_with_minimax
from zsxq_common import (
    DEFAULT_CHROME_PROFILE, DEFAULT_DB, DEFAULT_DOWNLOADS,
    date_subfolder, do_download, get_session_via_selenium, init_db,
    sanitize_filename,
)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify PDFs in zsxq.db using MiniMax (offline — no scraping)."
    )
    parser.add_argument("--db",              default=str(DEFAULT_DB),
                        help=f"SQLite database path (default: {DEFAULT_DB})")
    parser.add_argument("--downloads",       default=str(DEFAULT_DOWNLOADS),
                        help="Directory used by zsxq_downloader.py")
    parser.add_argument("--count",           type=int, default=0,
                        help="Classify at most N rows (0 = all unclassified)")
    parser.add_argument("--reclassify",      action="store_true",
                        help="Re-classify ALL rows (even those already classified)")
    parser.add_argument("--no-autodownload", action="store_true",
                        help="Do not auto-download matched PDFs not yet on disk")
    parser.add_argument("--chrome-profile",  default=str(DEFAULT_CHROME_PROFILE),
                        help="Chrome profile for auto-downloading (only used when "
                             "--no-autodownload is NOT set and matched files are missing)")
    parser.add_argument("--classify-delay",  type=float, default=1.0,
                        help="Seconds between MiniMax API calls (default: 1.0)")
    args = parser.parse_args()

    if not _CONFIG_MINIMAX_KEY:
        print("ERROR: MINIMAX_API_KEY not found in config.py")
        sys.exit(1)

    db_path       = Path(args.db).expanduser()
    downloads_dir = Path(args.downloads).expanduser()

    if not db_path.exists():
        print(f"ERROR: DB not found at {db_path}")
        print("Run zsxq_downloader.py first to populate the database.")
        sys.exit(1)

    conn = init_db(db_path)

    # ── Lazy Chrome session (only if auto-download is needed) ──────────────
    _session = None

    def get_session():
        nonlocal _session
        if _session is None:
            chrome_profile = Path(args.chrome_profile).expanduser()
            if not chrome_profile.exists():
                print(f"ERROR: Chrome profile not found at {chrome_profile}")
                print("Use --no-autodownload to skip auto-download.")
                sys.exit(1)
            _session = get_session_via_selenium(chrome_profile)
        return _session

    # ── Banner ────────────────────────────────────────────────────────────
    print("=" * 65)
    print("  zsxq_index.py  [offline classification mode]")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  DB       : {db_path}")
    print(f"  Downloads: {downloads_dir}")
    mode_str = "reclassify ALL" if args.reclassify else "unclassified only"
    print(f"  Mode     : {mode_str}")
    if args.count:
        print(f"  Limit    : {args.count} rows")
    print("=" * 65)
    print()

    # ── Select rows to classify ───────────────────────────────────────────
    limit_sql = f" LIMIT {args.count}" if args.count > 0 else ""
    if args.reclassify:
        to_classify = conn.execute(
            f"SELECT file_id, name, summary, local_path, create_time "
            f"FROM pdf_files ORDER BY create_time DESC{limit_sql}"
        ).fetchall()
    else:
        to_classify = conn.execute(
            f"SELECT file_id, name, summary, local_path, create_time "
            f"FROM pdf_files WHERE ai_related IS NULL "
            f"ORDER BY create_time DESC{limit_sql}"
        ).fetchall()

    total = len(to_classify)
    if total == 0:
        print("All rows already classified. Use --reclassify to redo them.")
        conn.close()
        sys.exit(0)

    print(f"Classifying {total} row(s) via MiniMax…\n")
    counts = {"ai": 0, "robotics": 0, "semiconductor": 0, "energy": 0,
              "dl_ok": 0, "dl_fail": 0, "err": 0}
    elapsed_times: list[float] = []
    t_start = time.monotonic()

    for i, row in enumerate(to_classify, 1):
        file_id     = row["file_id"]
        name        = row["name"]
        summary     = row["summary"] or ""
        local_path  = row["local_path"]
        create_time = row["create_time"]

        eta_str = ""
        if elapsed_times:
            avg_s = sum(elapsed_times) / len(elapsed_times)
            eta_str = f"  ETA ~{(total - i + 1) * avg_s:.0f}s"

        print(f"  [{i}/{total}] ({i/total*100:.0f}%){eta_str}")
        print(f"    File: {name}")

        (analysis, ai_rel, rob_rel, semi_rel, nrg_rel,
         tickers, api_elapsed, prompt, raw_json) = classify_with_minimax(
            name, summary, _CONFIG_MINIMAX_KEY
        )
        elapsed_times.append(api_elapsed + args.classify_delay)

        if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]):
            counts["err"] += 1

        flags = []
        if ai_rel:    flags.append("AI");            counts["ai"] += 1
        if rob_rel:   flags.append("Robotics");      counts["robotics"] += 1
        if semi_rel:  flags.append("Semiconductor"); counts["semiconductor"] += 1
        if nrg_rel:   flags.append("Energy");        counts["energy"] += 1

        label = ("✓ " + ", ".join(flags)) if flags else "✗ None"
        print(f"    Categories : {label}  [{api_elapsed:.1f}s]")
        if tickers:
            print(f"    Tickers    : {tickers}")
        if analysis:
            print(f"    Analysis   : {analysis}")

        # ── Auto-download if matched and not yet on disk ──────────────────
        if any([ai_rel, rob_rel, semi_rel, nrg_rel]) and not local_path:
            if args.no_autodownload:
                print("           → category match (auto-download disabled)")
            else:
                sub  = date_subfolder(create_time)
                dest = downloads_dir / sub / sanitize_filename(name)
                if dest.exists():
                    local_path = str(dest)
                    print(f"           → already on disk: {sub}/{dest.name}")
                else:
                    print("           → category match: downloading…")
                    local_path, ok = do_download(
                        get_session(), file_id, name, downloads_dir,
                        create_time=create_time,
                    )
                    if ok:
                        counts["dl_ok"] += 1
                    else:
                        counts["dl_fail"] += 1

        # ── Persist classification ────────────────────────────────────────
        conn.execute(
            """UPDATE pdf_files
               SET ai_related            = ?,
                   robotics_related      = ?,
                   semiconductor_related = ?,
                   energy_related        = ?,
                   tickers               = COALESCE(?, tickers),
                   categories_analysis   = ?,
                   categories_prompt     = ?,
                   categories_raw        = ?,
                   local_path            = COALESCE(?, local_path),
                   indexed_at            = ?
             WHERE file_id = ?""",
            (
                1 if ai_rel   is True else (0 if ai_rel   is False else None),
                1 if rob_rel  is True else (0 if rob_rel  is False else None),
                1 if semi_rel is True else (0 if semi_rel is False else None),
                1 if nrg_rel  is True else (0 if nrg_rel  is False else None),
                tickers or None,
                analysis, prompt, raw_json,
                local_path,
                datetime.now().isoformat(),
                file_id,
            ),
        )
        conn.commit()

        if i < total:
            time.sleep(args.classify_delay)

    t_total = time.monotonic() - t_start
    dl_msg = (
        f"\n  Auto-downloaded : {counts['dl_ok']} OK, {counts['dl_fail']} failed"
        if (counts["dl_ok"] or counts["dl_fail"]) else ""
    )
    print(f"\n{'='*65}")
    print(f"  Classification done in {t_total:.1f}s  ({total} rows)")
    print(f"    AI           : {counts['ai']}")
    print(f"    Robotics     : {counts['robotics']}")
    print(f"    Semiconductor: {counts['semiconductor']}")
    print(f"    Energy       : {counts['energy']}")
    print(f"    Parse errors : {counts['err']}{dl_msg}")
    print(f"{'='*65}")

    conn.close()


if __name__ == "__main__":
    main()
