#!/usr/bin/env python3
"""
zsxq_index.py — Classify PDFs already stored in zsxq.db using MiniMax.

Responsibilities
----------------
  This script is purely an OFFLINE classifier: it reads rows from the local
  SQLite database (written by zsxq_downloader.py) and calls MiniMax to
  classify each PDF across four categories:
    AI | Robotics | Semiconductor | Energy

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

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from minimax import MINIMAX_API_KEY as _CONFIG_MINIMAX_KEY, call_minimax  # type: ignore

from zsxq_common import (
    DEFAULT_CHROME_PROFILE, DEFAULT_DB, DEFAULT_DOWNLOADS,
    do_download, get_session_via_selenium, init_db, load_tracker,
    sanitize_filename,
)

# ── MiniMax classification prompt ─────────────────────────────────────────────

CLASSIFY_SYSTEM = (
    "You are a financial research analyst. Given a research report summary, classify it "
    "across four categories and extract tickers.\n\n"
    "Respond in exactly this format (one item per line, nothing else):\n"
    "  AI: Yes or No\n"
    "  Robotics: Yes or No\n"
    "  Semiconductor: Yes or No\n"
    "  Energy: Yes or No\n"
    "  Tickers: TICK1, TICK2, ...  (or Tickers: None)\n"
    "  Analysis: <2-3 sentence summary of the report's focus>\n\n"
    "Mark Yes when the report covers a product market where multiple companies compete "
    "— not a macro/policy theme only, and not a product line unique to one company.\n\n"
    "Category definitions:\n"
    "- AI: AI accelerator chips (GPU / NPU / TPU), LLM and foundation model products, "
    "AI inference platforms, AI agent / copilot software.\n"
    "- Robotics: humanoid robots, industrial collaborative robots (cobots), "
    "commercially deployed autonomous-driving (robotaxi), autonomous drones.\n"
    "- Semiconductor: advanced packaging (Chiplet / CoWoS / HBM), power semiconductors "
    "(SiC / GaN), leading-edge logic foundry, EDA software, NAND / DRAM.\n"
    "- Energy: battery cells (LFP / NCM / solid-state / sodium-ion), large-scale battery "
    "energy storage (BESS), solar modules (TOPCon / HJT / perovskite), grid inverters, "
    "small modular reactors (SMR).\n"
    "Tickers: A-share 6-digit codes, HK codes, US symbols explicitly referenced only."
)

CLASSIFY_USER_TMPL = """\
Report filename: {name}

Summary (Chinese):
{summary}

Classify this report. Mark Yes only when the report covers a product market with \
multiple competing companies — not just a single company's product line or a broad \
macro/policy discussion. Extract tickers that are explicitly named.
"""


# ── Parsing helpers ───────────────────────────────────────────────────────────

def _parse_yes_no(text: str, label: str) -> bool | None:
    """Find 'Label: Yes/No' in text; return True/False/None."""
    for line in text.splitlines():
        ls = line.strip().lower()
        if ls.startswith(f"{label.lower()}:"):
            val = ls.split(":", 1)[1].strip()
            if val.startswith("yes"):
                return True
            if val.startswith("no"):
                return False
    return None


# ── Classification ────────────────────────────────────────────────────────────

def classify_with_minimax(
    name: str,
    summary: str,
    api_key: str,
    retries: int = 3,
) -> tuple[str, bool | None, bool | None, bool | None, bool | None, str, float, str, str]:
    """Call MiniMax to classify a PDF across 4 categories and extract tickers.

    Returns:
        (analysis, ai_rel, robotics_rel, semiconductor_rel, energy_rel,
         tickers, elapsed_seconds, prompt_sent, raw_json)
    """
    user_msg = CLASSIFY_USER_TMPL.format(
        name=name,
        summary=summary.strip() if summary else "(no summary available)",
    )
    text, elapsed, raw_json = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": CLASSIFY_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.1,
        max_completion_tokens=300,
        retries=retries,
        api_key=api_key,
    )

    ai_rel   = _parse_yes_no(text, "AI")
    rob_rel  = _parse_yes_no(text, "Robotics")
    semi_rel = _parse_yes_no(text, "Semiconductor")
    nrg_rel  = _parse_yes_no(text, "Energy")

    if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]) and text:
        print(f"    ⚠ Could not parse all categories. Raw reply:\n{text}")

    tickers = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("tickers:"):
            raw_t = ls[len("tickers:"):].strip()
            if raw_t.lower() not in ("none", "n/a", ""):
                tickers = raw_t
            break

    analysis = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("analysis:"):
            analysis = ls[len("analysis:"):].strip()
            break
    if not analysis:
        analysis = text  # fallback: store the full response

    return analysis, ai_rel, rob_rel, semi_rel, nrg_rel, tickers, elapsed, user_msg, raw_json


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

    conn    = init_db(db_path)
    tracker = load_tracker(downloads_dir)

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
                from zsxq_common import date_subfolder as _date_sub
                sub  = _date_sub(create_time)
                dest = downloads_dir / sub / sanitize_filename(name)
                if dest.exists():
                    local_path = str(dest)
                    print(f"           → already on disk: {sub}/{dest.name}")
                else:
                    print("           → category match: downloading…")
                    local_path, ok = do_download(
                        get_session(), file_id, name, downloads_dir, tracker,
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
