#!/usr/bin/env python3
"""
bulk_download_10k_10q_8k.py — Bulk download SEC 10-K / 10-Q / 8-K for a list of tickers.

Directly calls fetch_financial_report._run_download() for each ticker in sequence,
logging all output to bulk_download_10k_10q_8k.log in addition to stdout.

Non-US tickers (TSX:GMIN, ASX:RMS, LSE:HSBA) are skipped — not on SEC EDGAR.

Usage:
    python bulk_download_10k_10q_8k.py              # run all tickers
    python bulk_download_10k_10q_8k.py WULF COIN    # run specific tickers only
"""
import sys, pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).parent.parent))

import argparse
import json
import sys
import time
from pathlib import Path

# Import from sibling module
sys.path.insert(0, str(Path(__file__).parent))
import fetch_financial_report as fr

# ── Ticker list ───────────────────────────────────────────────────────────────
# Exchange prefixes stripped; TSX/ASX/LSE tickers skipped (not on SEC EDGAR).

TICKERS = [
    # BIG TECH
    "META", "AVGO", "ORCL", "AMD", "AAPL", "MSFT", "NVDA", "AMZN",
    "TSLA", "GOOG", "ASML", "NFLX", "TSM", "MU",
    # SEMICONDUCTORS
    "VRT", "CAT", "ALAB", "QCOM", "MRVL", "APLD", "TER", "TXN",
    "DELL", "NVTS", "AMAT", "LRCX", "COHR", "LITE", "CRDO", "GSIT",
    # 芯片设计公司
    "SNPS", "CDNS",
    # STORAGE
    "STX", "WDC", "SNDK",
    # ENERGY
    "UUUU", "GEV", "BE", "OKLO", "FSLR", "SMR", "OXY", "PWR", "TLN", "SHEL", "XOM",
    # MINING  (TSX:GMIN skipped — Toronto Stock Exchange, not on SEC EDGAR)
    "UAMY", "NEM", "USAR", "CIFR",
    # AI云服务
    "DDOG", "RBRK", "GTLB", "MDB", "DOCN",
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
    # BITCOIN / CRYPTO
    "WULF", "HUT", "COIN", "CLSK", "BITF", "MARA", "CRCL",
    # HEALTHCARE
    "HIMS", "ABBV", "CRSP", "RXRX", "VRTX", "ACN", "LLY", "UNH", "ISRG", "OSCR",
    # ECOMMERCE
    "TTD", "VITL", "DHI", "SHOP", "APP",
    # ENTERTAINMENT
    "DIS", "UBER", "ABNB", "RBLX",
    # FINANCE  (BRK-B = NYSE:BRK.B)
    "UPST", "AFRM", "OPFI", "V", "HOOD", "WMT", "BRK-B", "BKNG", "SOFI", "GS", "KKR", "TREE", "APO",
    # QUANTUM
    "QBTS", "QUBT", "RGTI", "IONQ",
    # OTHERS
    "IREN", "AMBA",
]

FORMS = ["10-K", "10-Q", "8-K"]

# Foreign Private Issuers on SEC EDGAR:
#   20-F = annual (≈10-K), 6-K = current report (≈8-K), 40-F = Canadian annual
FPI_TICKERS = [
    # European / Asian FPIs
    "TSM", "ASML", "SHEL",
    # Netherlands
    "NBIS",
    # UK
    "ARM",
    # Danish
    "NVO",
    # Singapore
    "SE",
    # China ADR
    "PDD",
    # Canadian (files 40-F)
    "B",
]
FPI_FORMS   = ["20-F", "40-F", "6-K"]

SKIPPED = [
    "TSX:GMIN — Toronto Stock Exchange, no SEC EDGAR filings",
    "ASX:RMS  — Australian Stock Exchange, no SEC EDGAR filings",
    "LSE:HSBA — London Stock Exchange, no SEC EDGAR filings",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk download SEC filings")
    parser.add_argument("tickers", nargs="*", help="Specific tickers to download (default: all)")
    args = parser.parse_args()

    fr.init_db()

    # Filter lists if specific tickers requested
    if args.tickers:
        requested   = {t.upper() for t in args.tickers}
        run_tickers = [t for t in TICKERS     if t.upper() in requested]
        run_fpi     = [t for t in FPI_TICKERS if t.upper() in requested]
        unknown     = requested - {t.upper() for t in run_tickers + run_fpi}
        if unknown:
            print(f"⚠  Unknown tickers (not in list): {', '.join(sorted(unknown))}")
    else:
        run_tickers = TICKERS
        run_fpi     = FPI_TICKERS

    log_path = Path(__file__).parent.parent / "log" / "bulk_download_10k_10q_8k.log"
    total    = len(run_tickers)
    failed   = []

    start_ts = time.strftime("%Y-%m-%d %H:%M:%S")
    header   = (
        f"\n{'='*70}\n"
        f"Bulk download started {start_ts}\n"
        f"Tickers ({total}): {', '.join(run_tickers)}\n"
        f"Forms: {', '.join(FORMS)}\n"
        f"Skipped (non-SEC): {'; '.join(SKIPPED)}\n"
        f"{'='*70}\n"
    )
    print(header)

    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(header)
        logf.flush()

        for idx, ticker in enumerate(run_tickers, 1):
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

        # ── FPI tickers (20-F / 40-F / 6-K) ──────────────────────────────
        fpi_total  = len(run_fpi)
        fpi_failed = []
        fpi_header = (
            f"\n{'─'*70}\n"
            f"Foreign Private Issuers ({fpi_total}): {', '.join(run_fpi)}\n"
            f"Forms: {', '.join(FPI_FORMS)}\n"
            f"{'─'*70}\n"
        )
        print(fpi_header)
        logf.write(fpi_header)
        logf.flush()

        for idx, ticker in enumerate(run_fpi, 1):
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
            f"Note: BRK-B in DB = NYSE:BRK.B\n"
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
