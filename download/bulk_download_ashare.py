#!/usr/bin/env python3
"""
bulk_download_ashare.py — Bulk download A-share (SSE/SZSE) and HK (HKEX) financial
reports from CNINFO for a curated list of tickers.

Categories
----------
  A-share (SSE/SZSE): 年报, 半年报, 季报
  HK (HKEX):          年报, 半年报  (HK companies don't file quarterly reports)

Excluded from this script (use bulk_download_10k_10q_8k.py instead)
----------------------------------------------------------------------
  OTC:ZIJMF   — OTC in US, not on CNINFO
  NASDAQ:PONY — US NASDAQ listing → SEC EDGAR
  NYSE:BABA   — US NYSE listing   → SEC EDGAR  (also files 20-F)
  NASDAQ:BIDU — US NASDAQ listing → SEC EDGAR  (also files 20-F)
  NASDAQ:WRD  — US NASDAQ listing → SEC EDGAR
  OTC:BYDDF   — OTC in US, not on CNINFO
  NASDAQ:HSAI — US NASDAQ listing → SEC EDGAR
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_cninfo_report as cr

# ── Ticker lists ──────────────────────────────────────────────────────────────

# A-share tickers by category (all use 年报 + 半年报 + 季报)
A_SHARE_TICKERS = [
    # ── GPU / 半导体 ──────────────────────────────────────────────────────
    "SZSE:300308",  # 中际旭创  (optical transceivers)
    "SSE:688802",   # 英特尔/士兰微 or similar (check code)
    "SSE:688795",   # 研究院 / 半导体
    "SZSE:002837",  # 英联股份 / semiconductor
    "SSE:688041",   # 海光信息 (CPU/GPU)
    "SSE:688256",   # 寒武纪 (AI chips)
    # ── AI 相关 ───────────────────────────────────────────────────────────
    "SZSE:002472",  # 双环传动 / AI related
    "SSE:603486",   # 科沃斯 / robotics & AI
    "SZSE:300383",  # 光环新网 / data center
    "SSE:688169",   # 石头科技 / AI robotics
    "SSE:603019",   # 中科曙光 (Dawning Information)
    # ── 机器人相关 ────────────────────────────────────────────────────────
    "SSE:601100",   # 恒立液压 (hydraulics for robots)
    "SSE:688017",   # 绿的谐波 (harmonic drives)
    "SSE:601689",   # 拓普集团 (auto/robot parts)
    "SZSE:300124",  # 汇川技术 (industrial automation)
    # ── 传统行业 ──────────────────────────────────────────────────────────
    "SSE:600519",   # 贵州茅台 (Kweichow Moutai)
    # ── 其他 ──────────────────────────────────────────────────────────────
    "SZSE:000338",  # 潍柴动力 (Weichai Power)
    "SZSE:300751",  # 迈为股份 (Maiwei)
    "SSE:688008",   # 澜起科技 (Montage Technology)
    "SSE:688347",   # 华虹半导体 / semiconductor
]

# HK Exchange tickers (年报 + 半年报 only)
HK_TICKERS = [
    # ── HK Exchange ───────────────────────────────────────────────────────
    "HKEX:2513",    # (check company)
    "HKEX:100",     # 越秀地产 or Swire / check
    "HKEX:2533",    # (check company)
    "HKEX:9880",    # 百度集团 (Baidu HK)
    "HKEX:2590",    # 珍酒李渡 / check
    "HKEX:6082",    # (check company)
    "HKEX:9660",    # 名创优品 / Miniso
    "HKEX:981",     # 中芯国际 (SMIC)
    "HKEX:6600",    # (check company)
]

SKIPPED = [
    "OTC:ZIJMF   — OTC pink sheets in US; not on CNINFO",
    "NASDAQ:PONY — US NASDAQ listing; use bulk_download_10k_10q_8k.py",
    "NYSE:BABA   — US NYSE listing (20-F filer); use bulk_download_10k_10q_8k.py",
    "NASDAQ:BIDU — US NASDAQ listing (20-F filer); use bulk_download_10k_10q_8k.py",
    "NASDAQ:WRD  — US NASDAQ listing; use bulk_download_10k_10q_8k.py",
    "OTC:BYDDF   — OTC pink sheets in US; not on CNINFO",
    "NASDAQ:HSAI — US NASDAQ listing; use bulk_download_10k_10q_8k.py",
]


# ── Download helper ────────────────────────────────────────────────────────────

def _download_batch(
    tickers: list[str],
    categories: dict[str, str],
    logf,
    batch_label: str,
) -> list[str]:
    """Download all tickers in a batch. Returns list of failed tickers."""
    failed  = []
    n_total = len(tickers)

    for idx, ticker in enumerate(tickers, 1):
        prefix = f"[{batch_label} {idx:>3}/{n_total}] {ticker:<18}"
        print(f"\n{prefix} ─────────────────────────────")
        logf.write(f"\n{prefix} ─────────────────────────────\n")
        logf.flush()

        ticker_error = False
        try:
            for event in cr._run_download(ticker, categories):
                if not event.startswith("data: "):
                    continue
                d    = json.loads(event[6:])
                msg  = d.get("msg", "")
                line = f"  {msg}"
                print(line)
                logf.write(line + "\n")
                logf.flush()
                if d.get("error"):
                    ticker_error = True
        except Exception as exc:
            err = f"  ❌  Unhandled exception: {exc}"
            print(err)
            logf.write(err + "\n")
            ticker_error = True

        if ticker_error:
            failed.append(ticker)

    return failed


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    cr.init_db()

    log_path = Path(__file__).parent / "bulk_download_ashare.log"
    start_ts = time.strftime("%Y-%m-%d %H:%M:%S")

    header = (
        f"\n{'='*70}\n"
        f"Bulk A-share / HK download started {start_ts}\n"
        f"A-share tickers ({len(A_SHARE_TICKERS)}): "
        f"{', '.join(A_SHARE_TICKERS)}\n"
        f"HK tickers      ({len(HK_TICKERS)}): "
        f"{', '.join(HK_TICKERS)}\n"
        f"A-share categories: {', '.join(cr.ALL_CATEGORIES)}\n"
        f"HK categories:      {', '.join(cr.HK_CATEGORIES)}\n"
        f"Skipped (non-CNINFO):\n"
        + "\n".join(f"  {s}" for s in SKIPPED)
        + f"\n{'='*70}\n"
    )
    print(header)

    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(header)
        logf.flush()

        # ── A-share batch ──────────────────────────────────────────────────
        a_failed = _download_batch(
            A_SHARE_TICKERS, cr.ALL_CATEGORIES, logf, "A"
        )

        # ── HK batch ──────────────────────────────────────────────────────
        hk_failed = _download_batch(
            HK_TICKERS, cr.HK_CATEGORIES, logf, "HK"
        )

        # ── Summary ────────────────────────────────────────────────────────
        done_ts = time.strftime("%Y-%m-%d %H:%M:%S")
        summary = (
            f"\n{'='*70}\n"
            f"Finished {done_ts}\n"
            f"A-share: {len(A_SHARE_TICKERS) - len(a_failed)}/{len(A_SHARE_TICKERS)} succeeded\n"
            f"HK:      {len(HK_TICKERS) - len(hk_failed)}/{len(HK_TICKERS)} succeeded\n"
        )
        if a_failed:
            summary += f"Failed (A-share): {', '.join(a_failed)}\n"
        if hk_failed:
            summary += f"Failed (HK):      {', '.join(hk_failed)}\n"
        summary += (
            "Skipped (US-listed — use bulk_download_10k_10q_8k.py):\n"
            + "\n".join(f"  {s}" for s in SKIPPED)
            + f"\n{'='*70}\n"
        )
        print(summary)
        logf.write(summary)


if __name__ == "__main__":
    main()
