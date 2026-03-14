#!/usr/bin/env python3
"""
bulk_download_10k_10q_8k.py — Bulk download SEC 10-K / 10-Q / 8-K for a list of tickers.

Directly calls fetch_financial_report._run_download() for each ticker in sequence,
logging all output to bulk_download_10k_10q_8k.log in addition to stdout.

Non-US tickers (TSX:GMIN, ASX:RMS) are skipped — not on SEC EDGAR.
"""

import json
import sys
import time
from pathlib import Path

# Import from sibling module
sys.path.insert(0, str(Path(__file__).parent))
import fetch_financial_report as fr

# ── Ticker list ───────────────────────────────────────────────────────────────
# Exchange prefixes stripped; TSX/ASX tickers skipped (not on SEC EDGAR).

TICKERS = [
    # BIG TECH
    "META", "AVGO", "ORCL", "AMD", "AAPL", "MSFT", "NVDA", "AMZN",
    "TSLA", "GOOG", "ASML", "NFLX", "TSM", "MU",
    # SEMICONDUCTORS
    "VRT", "CAT", "ALAB", "QCOM", "MRVL", "APLD", "TER", "TXN",
    "DELL", "ARM", "NVTS", "AMAT", "LRCX", "COHR", "LITE", "CRDO", "GSIT",
    # 芯片设计公司
    "SNPS", "CDNS",
    # STORAGE
    "STX", "WDC", "SNDK",
    # ENERGY
    "UUUU", "GEV", "BE", "OKLO", "FSLR", "SMR", "OXY", "PWR", "TLN", "SHEL", "XOM",
    # MINING  (TSX:GMIN skipped — Toronto Stock Exchange, not on SEC EDGAR)
    "UAMY", "B", "NEM", "USAR", "CIFR",
    # AI云服务
    "DDOG", "RBRK", "GTLB", "MDB", "DOCN", "NBIS",
    # 网络安全
    "PANW",
    # 机器人
    "SERV", "SYM",
    # 教育
    "LRN", "DUOL",
    # AI
    "SOUN", "BBAI", "ZETA", "PLTR", "INOD", "SNOW", "TEM", "PATH",
    # AEROSPACE / SATELLITE
    "ATRO", "BKSY", "AMPX", "HWM", "ACHR", "VSAT", "PL", "ONDS", "ASTS", "HEI", "RDW", "RTX",
    # OTHER  (ASX:RMS skipped — Australian Stock Exchange, not on SEC EDGAR)
    "WYFI", "RDDT", "VST", "RMBS",
]

FORMS = ["10-K", "10-Q", "8-K"]

# Foreign Private Issuers on SEC EDGAR — file 20-F (annual) and 6-K (press releases)
# instead of 10-K and 8-K.
FPI_TICKERS = ["TSM", "ASML", "SHEL"]
FPI_FORMS   = ["20-F", "6-K"]

SKIPPED = [
    "TSX:GMIN — Toronto Stock Exchange, no SEC EDGAR filings",
    "ASX:RMS  — Australian Stock Exchange, no SEC EDGAR filings",
]


def main() -> None:
    fr.init_db()

    log_path = Path(__file__).parent / "bulk_download_10k_10q_8k.log"
    total    = len(TICKERS)
    failed   = []
    skipped  = 0

    start_ts = time.strftime("%Y-%m-%d %H:%M:%S")
    header   = (
        f"\n{'='*70}\n"
        f"Bulk download started {start_ts}\n"
        f"Tickers ({total}): {', '.join(TICKERS)}\n"
        f"Forms: {', '.join(FORMS)}\n"
        f"Skipped (non-SEC): {'; '.join(SKIPPED)}\n"
        f"{'='*70}\n"
    )
    print(header)

    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(header)
        logf.flush()

        for idx, ticker in enumerate(TICKERS, 1):
            prefix = f"[{idx:>3}/{total}] {ticker:<8}"
            print(f"\n{prefix} ─────────────────────────────")
            logf.write(f"\n{prefix} ─────────────────────────────\n")
            logf.flush()

            ticker_error = False
            try:
                for event in fr._run_download(ticker, FORMS):
                    # SSE format:  "data: {...}\n\n"
                    if not event.startswith("data: "):
                        continue
                    d   = json.loads(event[6:])
                    msg = d.get("msg", "")
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

        # ── FPI tickers (20-F / 6-K) ───────────────────────────────────────
        fpi_total  = len(FPI_TICKERS)
        fpi_failed = []
        fpi_header = (
            f"\n{'─'*70}\n"
            f"Foreign Private Issuers ({fpi_total}): {', '.join(FPI_TICKERS)}\n"
            f"Forms: {', '.join(FPI_FORMS)}\n"
            f"{'─'*70}\n"
        )
        print(fpi_header)
        logf.write(fpi_header)
        logf.flush()

        for idx, ticker in enumerate(FPI_TICKERS, 1):
            prefix = f"[FPI {idx:>2}/{fpi_total}] {ticker:<8}"
            print(f"\n{prefix} ─────────────────────────────")
            logf.write(f"\n{prefix} ─────────────────────────────\n")
            logf.flush()

            ticker_error = False
            try:
                for event in fr._run_download(ticker, FPI_FORMS):
                    if not event.startswith("data: "):
                        continue
                    d   = json.loads(event[6:])
                    msg = d.get("msg", "")
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
                fpi_failed.append(ticker)

        # ── Summary ────────────────────────────────────────────────────────
        done_ts = time.strftime("%Y-%m-%d %H:%M:%S")
        summary = (
            f"\n{'='*70}\n"
            f"Finished {done_ts}\n"
            f"US  tickers: {total - len(failed)}/{total} succeeded\n"
            f"FPI tickers: {fpi_total - len(fpi_failed)}/{fpi_total} succeeded\n"
        )
        if failed:
            summary += f"Failed (US):  {', '.join(failed)}\n"
        if fpi_failed:
            summary += f"Failed (FPI): {', '.join(fpi_failed)}\n"
        summary += f"{'='*70}\n"
        print(summary)
        logf.write(summary)


if __name__ == "__main__":
    main()
