#!/usr/bin/env python3
"""
fetch_financial_report.py — Download and browse US company SEC 10-K / 10-Q / 8-K filings.

Features
--------
  • Enter any US ticker → streams download of all 10-K / 10-Q / 8-K filings from SEC EDGAR
  • 8-K: scans each filing index for EX-99.x PDF exhibits (investor presentations, etc.)
  • Files stored under  financial_reports/<TICKER>/
  • SQLite DB (financial_reports.db) tracks metadata
  • Web UI: download with live progress, filter, open filings in new tab, delete

Usage
-----
    python fetch_financial_report.py [--port 8081]
    Then open  http://localhost:8081
"""

import argparse
import datetime
import email.utils
import json
import re
import sqlite3
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint, Response, abort, jsonify, render_template_string, request, send_file
import md_comment_widget as mcw
import nav_widget2 as nw2

# ── Paths & config ────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "financial_reports"
UPLOADS_DIR = SCRIPT_DIR / "uploads"
DB_FILE     = SCRIPT_DIR / "db" / "financial_reports.db"

REPORTS_DIR.mkdir(exist_ok=True)

# SEC EDGAR rate-limit: ≤ 10 req/sec; be polite
_SEC_DELAY   = 0.12
MIN_FILED_YEAR = 2020  # skip filings filed before this year
_SEC_HEADERS = {
    "User-Agent": "FinancialReportDownloader contact@localhost.local",
    "Accept-Encoding": "gzip, deflate",
}

sec_bp = Blueprint("sec", __name__)

app      = Flask(__name__)
app.register_blueprint(mcw.create_blueprint(UPLOADS_DIR))
_DB_PATH = DB_FILE


# ── Database ──────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker           TEXT    NOT NULL,
                company_name     TEXT,
                period           TEXT    NOT NULL,
                form_type        TEXT,
                filed_date       TEXT,
                period_of_report TEXT,
                local_path       TEXT,
                accession_no     TEXT    UNIQUE,
                file_size        INTEGER,
                comment          TEXT,
                created_at       TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reports_ticker ON reports(ticker)"
        )
        # Migration: add comment column to existing DBs
        try:
            conn.execute("ALTER TABLE reports ADD COLUMN comment TEXT")
        except Exception:
            pass  # column already exists


# ── SEC EDGAR helpers ─────────────────────────────────────────────────────────

_ticker_map_cache: dict | None = None


def _sec_get(url: str, **kw) -> requests.Response:
    """Rate-limited GET with SEC EDGAR headers."""
    time.sleep(_SEC_DELAY)
    r = requests.get(url, headers=_SEC_HEADERS, timeout=30, **kw)
    r.raise_for_status()
    return r


def resolve_cik(ticker: str) -> tuple[str, str]:
    """Return (cik_padded_10, company_name) for a ticker symbol."""
    global _ticker_map_cache
    if _ticker_map_cache is None:
        _ticker_map_cache = _sec_get(
            "https://www.sec.gov/files/company_tickers.json"
        ).json()
    tic = ticker.strip().upper()
    for item in _ticker_map_cache.values():
        if item["ticker"].upper() == tic:
            return str(item["cik_str"]).zfill(10), item["title"]
    raise ValueError(f"Ticker '{ticker}' not found in SEC EDGAR")


def fetch_all_filings(cik: str) -> dict:
    """Return the combined recent-filings dict (parallel lists) for a CIK.

    The primary submissions JSON covers the most recent ~1 000 filings.
    Older filings are in additional pages referenced in filings.files[].
    """
    data   = _sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
    recent = data["filings"]["recent"]

    for fpage in data["filings"].get("files", []):
        page = _sec_get(f"https://data.sec.gov/submissions/{fpage['name']}").json()
        for key in recent:
            recent[key].extend(page.get(key, []))

    return recent


def _period_label(form_type: str, report_date: str) -> str:
    """Build a sortable label: '2024Q1', '2024_10K', '2024-02-21_8K', etc."""
    try:
        d     = datetime.date.fromisoformat(report_date[:10])
        year  = d.year
        month = d.month
    except Exception:
        return report_date[:10] if report_date else "unknown"

    amendment = form_type.endswith("/A")
    base      = form_type.rstrip("A").rstrip("/")
    suffix    = "_A" if amendment else ""

    if base == "10-K":
        return f"{year}_10K{suffix}"
    if base == "10-Q":
        q = (month - 1) // 3 + 1
        return f"{year}Q{q}{suffix}"
    if base == "8-K":
        return f"{report_date[:10]}_8K{suffix}"
    if base == "20-F":
        return f"{year}_20F{suffix}"
    if base == "6-K":
        return f"{report_date[:10]}_6K{suffix}"
    return f"{year}_{form_type.replace('/', '-')}"


def _download_primary(cik: str, accession_no: str, primary_doc: str, dest: Path) -> int:
    """Download the primary filing document; return bytes written."""
    clean = accession_no.replace("-", "")
    url   = (
        f"https://www.sec.gov/Archives/edgar/data"
        f"/{int(cik)}/{clean}/{primary_doc}"
    )
    r    = _sec_get(url, stream=True)
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with open(dest, "wb") as fh:
        for chunk in r.iter_content(65536):
            fh.write(chunk)
            size += len(chunk)
    return size


_EXHIBIT_EXTS   = {".pdf", ".htm", ".html"}
_EXHIBIT_HTML   = {".htm", ".html"}

# 8-K item codes → short human-readable labels
_8K_ITEMS = {
    "1.01": "Agreement", "1.02": "Termination", "1.03": "Bankruptcy",
    "1.04": "Mine Safety", "1.05": "Material Cybersecurity",
    "2.01": "Asset Acquisition/Disposal", "2.02": "Earnings Results",
    "2.03": "Debt Obligation", "2.04": "Debt Trigger", "2.05": "Costs",
    "2.06": "Asset Impairment",
    "3.01": "Exchange Delisting", "3.02": "Unregistered Sales",
    "3.03": "Shareholder Rights",
    "4.01": "Auditor Change", "4.02": "Restatement",
    "5.01": "Shell Company Change", "5.02": "Director/Officer Change",
    "5.03": "Charter Amendment", "5.04": "Bylaw Amendment",
    "5.05": "Option Plan Amendment", "5.06": "Smaller Reporting",
    "5.07": "Shareholder Vote", "5.08": "Director Vacancy",
    "6.01": "Trust Funds", "6.02": "Asset Coverage",
    "6.03": "Material Obligation", "6.04": "Exit Provision",
    "6.05": "Loss of NAV", "6.10": "Alternative Fund",
    "7.01": "Regulation FD",
    "8.01": "Other Events",
    "9.01": "Financial Statements",
}


def _8k_label(filing_date: str, items_str: str, ex_description: str) -> str:
    """Return a meaningful period label for an 8-K exhibit row.

    Priority: exhibit description → item codes → date fallback.
    """
    date = filing_date[:10] if filing_date else "?"

    # Use the exhibit description if it's informative
    desc = (ex_description or "").strip()
    if desc and desc.upper() not in ("EX-99.1", "EX-99.2", "EX-99.3",
                                      "EXHIBIT 99.1", "EXHIBIT 99.2"):
        # Truncate to keep the badge readable
        desc = desc[:40].rstrip()
        return f"{date} {desc}"

    # Derive from item codes (e.g. "2.02,9.01" → "Earnings Results")
    items = [i.strip() for i in (items_str or "").split(",") if i.strip()]
    # Skip 9.01 (just means "has exhibits") unless it's the only one
    meaningful = [_8K_ITEMS.get(i, i) for i in items if i != "9.01"]
    if not meaningful:
        meaningful = [_8K_ITEMS.get(i, i) for i in items]
    if meaningful:
        label = " / ".join(dict.fromkeys(meaningful))[:40]  # dedup, truncate
        return f"{date} {label}"

    return f"{date} 8-K"


def _inject_base_tag(path: Path, base_url: str) -> None:
    """Rewrite an HTML file on disk with a <base> tag so relative URLs resolve correctly."""
    try:
        html  = path.read_bytes().decode("utf-8", errors="replace")
        lower = html.lower()
        tag   = f'<base href="{base_url}">'
        if tag in html:
            return  # already injected
        if "<head>" in lower:
            pos = lower.index("<head>") + len("<head>")
        elif "<head" in lower:
            pos = lower.index("<head")
            pos = lower.index(">", pos) + 1
        else:
            pos = 0
        html = html[:pos] + tag + html[pos:]
        path.write_bytes(html.encode("utf-8"))
    except Exception:
        pass


def _get_8k_exhibits(cik: str, accession_no: str) -> list[dict]:
    """Return EX-99.x exhibits from an 8-K filing index page.

    Supports PDF, HTM, and HTML exhibits (companies differ).
    Each returned dict has keys: type, description, href, filename.
    """
    clean = accession_no.replace("-", "")
    # EDGAR index uses original accession number (with dashes) + .html extension
    url = (
        f"https://www.sec.gov/Archives/edgar/data"
        f"/{int(cik)}/{clean}/{accession_no}-index.html"
    )
    try:
        r = _sec_get(url)
    except Exception:
        return []

    soup    = BeautifulSoup(r.content, "html.parser")
    results = []

    for row in soup.select("table tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        doc_type    = cells[3].get_text(strip=True)
        description = cells[1].get_text(strip=True)
        link        = cells[2].find("a")
        if not link or not doc_type.upper().startswith("EX-99"):
            continue
        href = link.get("href", "")
        ext  = Path(href).suffix.lower()
        if ext in _EXHIBIT_EXTS:
            fname = href.rsplit("/", 1)[-1]
            results.append({
                "type":        doc_type,
                "description": description,
                "href":        href,
                "filename":    fname,
            })

    return results


# ── Globe Newswire RSS download ───────────────────────────────────────────────

_GNW_RSS_URLS = [
    "https://www.globenewswire.com/Search?q={ticker}&inFormat=RSS",
    "https://www.globenewswire.com/Search?q={ticker}&inCategory=Company+News&inFormat=RSS",
]

_GNW_HEADERS = {
    "User-Agent": "FinancialReportDownloader contact@localhost.local",
    "Accept": "text/html,application/xhtml+xml,application/xml",
}


def _run_gnw_download(ticker: str, company_name: str, ticker_dir: Path, conn):
    """Generator: download Globe Newswire press releases for ticker via RSS."""
    items = []
    last_exc = None
    for url_tmpl in _GNW_RSS_URLS:
        rss_url = url_tmpl.format(ticker=ticker)
        try:
            r = requests.get(rss_url, headers=_GNW_HEADERS, timeout=30)
            r.raise_for_status()
            root = ET.fromstring(r.content)
            items = root.findall(".//item")
            if items:
                break  # found results
        except Exception as exc:
            last_exc = exc

    if not items:
        msg = f"  ·  Globe Newswire: no releases found for {ticker}"
        if last_exc:
            msg += f" ({last_exc})"
        yield _sse(msg)
        return

    yield _sse(f"  📰  {len(items)} Globe Newswire releases found")
    new_dl = 0

    for item in items:
        title_text = (item.findtext("title") or "Release").strip()
        link_url   = (item.findtext("link") or "").strip()
        pub_text   = (item.findtext("pubDate") or "").strip()

        if not link_url:
            continue

        # Parse RFC-2822 publish date → YYYY-MM-DD
        try:
            dt       = email.utils.parsedate_to_datetime(pub_text)
            date_str = dt.date().isoformat()
        except Exception:
            date_str = pub_text[:10] if len(pub_text) >= 10 else "unknown"

        unique_key = f"GNW/{link_url}"
        if conn.execute(
            "SELECT 1 FROM reports WHERE accession_no=?", (unique_key,)
        ).fetchone():
            yield _sse(f"       ⏭  {title_text[:60]} — already downloaded")
            continue

        safe_title = re.sub(r"[^\w\s-]", "_", title_text)[:60].strip()
        filename   = f"{date_str}_GNW_{safe_title}.html"
        dest       = ticker_dir / filename
        period     = f"{date_str} {title_text[:60]}"

        try:
            time.sleep(_SEC_DELAY)
            r2 = requests.get(link_url, headers=_GNW_HEADERS, timeout=30)
            r2.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r2.content)
            size = len(r2.content)

            conn.execute(
                """INSERT OR IGNORE INTO reports
                   (ticker, company_name, period, form_type, filed_date,
                    period_of_report, local_path, accession_no, file_size)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (ticker, company_name, period, "GNW", date_str, date_str,
                 str(dest), unique_key, size),
            )
            conn.commit()
            new_dl += 1
            yield _sse(f"       ✅  {title_text[:60]}  ({size // 1024:,} KB)")
        except Exception as exc:
            yield _sse(f"       ❌  {title_text[:50]} — {exc}")

    yield _sse(f"  📰  Globe Newswire done — {new_dl} new release(s) for {ticker}")


# ── SSE download stream ───────────────────────────────────────────────────────

def _sse(msg: str, *, done: bool = False, error: bool = False,
         count: int = 0, total: int = 0) -> str:
    payload = json.dumps(
        {"msg": msg, "done": done, "error": error, "count": count, "total": total}
    )
    return f"data: {payload}\n\n"


def _run_download(ticker: str, forms: list[str], last: int = 0, _suppress_done: bool = False):
    """Generator: stream SSE events while downloading filings.

    last: if > 0, only download the most-recent *last* filings per form type.
    _suppress_done: if True, skip the final done=True SSE (used by batch mode).
    """
    conn = get_conn()
    try:
        tic = ticker.strip().upper()

        yield _sse(f"🔍  Resolving CIK for {tic}…")
        cik, company_name = resolve_cik(tic)
        yield _sse(f"✅  {company_name}  (CIK {cik})")

        yield _sse("📋  Fetching filing history from SEC EDGAR…")
        recent = fetch_all_filings(cik)

        # Build list of dicts from the parallel arrays
        cols        = ["accessionNumber", "form", "reportDate", "filingDate",
                       "primaryDocument", "items", "primaryDocDescription"]
        all_filings = [dict(zip(cols, v)) for v in zip(*[recent[k] for k in cols])]

        # Separate 8-K and GNW from regular forms (10-K, 10-Q, 20-F, 6-K use base path)
        base_forms   = [f for f in forms if f not in ("8-K", "GNW")]
        include_8k   = "8-K" in forms
        include_gnw  = "GNW" in forms

        # ── Regular forms (10-K / 10-Q) ──────────────────────────────────────
        expanded = set(base_forms) | {f + "/A" for f in base_forms}
        target   = [
            f for f in all_filings
            if f["form"] in expanded and f["primaryDocument"]
        ]
        target.sort(key=lambda f: f["filingDate"], reverse=True)

        # 8-K filings (include 8-K/A amendments)
        target_8k = []
        if include_8k:
            target_8k = [
                f for f in all_filings
                if f["form"] in ("8-K", "8-K/A")
            ]
            target_8k.sort(key=lambda f: f["filingDate"], reverse=True)

        # ── Date-based pre-filter ─────────────────────────────────────────────
        # Query the newest filed_date we already have for each form type.
        # Filings at or before that date are already in the library — skip them
        # immediately instead of doing a per-accession DB lookup for each one.
        _max_rows = conn.execute(
            "SELECT form_type, MAX(filed_date) FROM reports WHERE ticker=? GROUP BY form_type",
            (tic,),
        ).fetchall()
        _max_by_form: dict[str, str] = {r[0]: r[1] for r in _max_rows}

        def _date_cutoff(form_type: str) -> str | None:
            """Return the latest filed_date we already have for this form type."""
            return _max_by_form.get(form_type) or _max_by_form.get(form_type.replace("/A", ""))

        # ── Year floor filter ─────────────────────────────────────────────
        before_year = len(target) + len(target_8k)
        target    = [f for f in target    if f["filingDate"] >= f"{MIN_FILED_YEAR}-01-01"]
        target_8k = [f for f in target_8k if f["filingDate"] >= f"{MIN_FILED_YEAR}-01-01"]
        skipped_by_year = before_year - len(target) - len(target_8k)
        if skipped_by_year:
            yield _sse(f"📅  Skipping {skipped_by_year} filing(s) filed before {MIN_FILED_YEAR}")

        before_reg = len(target)
        before_8k  = len(target_8k)
        target    = [f for f in target    if not _date_cutoff(f["form"]) or f["filingDate"] > _date_cutoff(f["form"])]
        target_8k = [f for f in target_8k if not _date_cutoff(f["form"]) or f["filingDate"] > _date_cutoff(f["form"])]
        skipped_by_date = (before_reg - len(target)) + (before_8k - len(target_8k))
        if skipped_by_date:
            yield _sse(
                f"📅  Skipping {skipped_by_date} filing(s) already in library "
                f"(filed_date ≤ latest date in DB)"
            )
        # ─────────────────────────────────────────────────────────────────────

        # ── Limit to last N filings ───────────────────────────────────────────
        if last > 0:
            target    = target[:last]
            target_8k = target_8k[:last]

        total_regular = len(target)
        total_8k      = len(target_8k)
        grand_total   = total_regular + total_8k   # approximate (8-K may have 0-N exhibits)

        summary_parts = []
        if target:
            summary_parts.append(f"{total_regular} {', '.join(base_forms)} filing(s)")
        if include_8k:
            summary_parts.append(f"{total_8k} 8-K filing(s) to scan for EX-99 exhibits")
        yield _sse(
            "📂  " + ("  •  ".join(summary_parts) if summary_parts else "No filings found"),
            total=grand_total,
        )

        ticker_dir = REPORTS_DIR / tic
        ticker_dir.mkdir(exist_ok=True)

        new_dl  = 0
        counter = 0   # overall progress counter

        # ── Download regular filings ──────────────────────────────────────────
        for filing in target:
            counter += 1
            acc     = filing["accessionNumber"]
            form    = filing["form"]
            period  = _period_label(form, filing["reportDate"])
            primary = filing["primaryDocument"]
            ext     = Path(primary).suffix or ".htm"

            # Already downloaded?
            if conn.execute(
                "SELECT 1 FROM reports WHERE accession_no=?", (acc,)
            ).fetchone():
                yield _sse(
                    f"  ⏭  {period} ({form}) — already in library",
                    count=counter, total=grand_total,
                )
                continue

            safe_acc = acc.replace("-", "_")
            filename = f"{period}_{form.replace('/', '-')}_{safe_acc}{ext}"
            dest     = ticker_dir / filename

            yield _sse(
                f"  ⬇  {period} ({form})  filed {filing['filingDate']}…",
                count=counter, total=grand_total,
            )

            try:
                size = _download_primary(cik, acc, primary, dest)
                conn.execute(
                    """INSERT OR IGNORE INTO reports
                       (ticker, company_name, period, form_type, filed_date,
                        period_of_report, local_path, accession_no, file_size)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (tic, company_name, period, form, filing["filingDate"],
                     filing["reportDate"], str(dest), acc, size),
                )
                conn.commit()
                new_dl += 1
                yield _sse(
                    f"       ✅  {filename}  ({size // 1024:,} KB)",
                    count=counter, total=grand_total,
                )
            except Exception as exc:
                yield _sse(
                    f"       ❌  {period} — {exc}",
                    count=counter, total=grand_total,
                )

        # ── Download 8-K PDF exhibits ─────────────────────────────────────────
        if include_8k and target_8k:
            yield _sse(f"📑  Scanning {total_8k} 8-K filings for EX-99 exhibits…")

            for filing in target_8k:
                counter += 1
                acc    = filing["accessionNumber"]
                form   = filing["form"]

                # Scan the filing index for EX-99.x exhibits
                exhibits = _get_8k_exhibits(cik, acc)
                if not exhibits:
                    yield _sse(
                        f"  ·  {filing['filingDate']} ({form}) — no EX-99 exhibits",
                        count=counter, total=grand_total,
                    )
                    continue

                yield _sse(
                    f"  📎  {filing['filingDate']} ({form})"
                    f" — {len(exhibits)} exhibit(s)",
                    count=counter, total=grand_total,
                )

                for ex in exhibits:
                    # Per-exhibit meaningful label using item codes + description
                    period = _8k_label(
                        filing["filingDate"],
                        filing.get("items", ""),
                        ex["description"],
                    )

                    # Unique key: accession/exhibit_filename
                    unique_key = f"{acc}/{ex['filename']}"

                    if conn.execute(
                        "SELECT 1 FROM reports WHERE accession_no=?", (unique_key,)
                    ).fetchone():
                        yield _sse(f"       ⏭  {ex['filename']} — already downloaded")
                        continue

                    # Build full URL for the exhibit file
                    href  = ex["href"]
                    clean = acc.replace("-", "")   # always needed for base_url below
                    if href.startswith("/"):
                        pdf_url = f"https://www.sec.gov{href}"
                    else:
                        pdf_url = (
                            f"https://www.sec.gov/Archives/edgar/data"
                            f"/{int(cik)}/{clean}/{ex['filename']}"
                        )

                    safe_acc  = acc.replace("-", "_")
                    orig_ext  = Path(ex["filename"]).suffix.lower() or ".htm"
                    stem      = Path(ex["filename"]).stem
                    filename  = f"{period.replace(' ', '_').replace('/', '-')}_{form.replace('/', '-')}_{safe_acc}_{stem}{orig_ext}"
                    dest      = ticker_dir / filename

                    try:
                        time.sleep(_SEC_DELAY)
                        r    = requests.get(pdf_url, headers=_SEC_HEADERS,
                                            stream=True, timeout=60)
                        r.raise_for_status()
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        size = 0
                        with open(dest, "wb") as fh:
                            for chunk in r.iter_content(65536):
                                fh.write(chunk)
                                size += len(chunk)

                        # Bake <base> tag into HTML so file:// also renders images
                        if orig_ext in _EXHIBIT_HTML:
                            base_url = (
                                f"https://www.sec.gov/Archives/edgar/data"
                                f"/{int(cik)}/{clean}/"
                            )
                            _inject_base_tag(dest, base_url)

                        conn.execute(
                            """INSERT OR IGNORE INTO reports
                               (ticker, company_name, period, form_type, filed_date,
                                period_of_report, local_path, accession_no, file_size)
                               VALUES (?,?,?,?,?,?,?,?,?)""",
                            (tic, company_name, period, form, filing["filingDate"],
                             filing["filingDate"], str(dest), unique_key, size),
                        )
                        conn.commit()
                        new_dl += 1
                        label = ex["description"] or ex["type"]
                        yield _sse(
                            f"       ✅  {label} — {filename}  ({size // 1024:,} KB)"
                        )
                    except Exception as exc:
                        yield _sse(f"       ❌  {ex['filename']} — {exc}")

        # ── Download Globe Newswire releases ──────────────────────────────────
        if include_gnw:
            yield _sse(f"📰  Fetching Globe Newswire releases for {tic}…")
            yield from _run_gnw_download(tic, company_name, ticker_dir, conn)

        if not _suppress_done:
            yield _sse(
                f"🎉  Done!  {new_dl} new file(s) downloaded for {tic}.",
                done=True, count=grand_total, total=max(grand_total, 1),
            )
        else:
            yield _sse(f"✅  {tic}: {new_dl} new file(s) downloaded.")

    except Exception as exc:
        if not _suppress_done:
            yield _sse(f"❌  {exc}", done=True, error=True)
        else:
            yield _sse(f"❌  {tic}: {exc}")
    finally:
        conn.close()


def _run_batch_download(forms: list[str], last: int):
    """Generator: download last N filings for every ticker already in the library."""
    conn = get_conn()
    tickers = [r[0] for r in conn.execute(
        "SELECT DISTINCT ticker FROM reports ORDER BY ticker"
    ).fetchall()]
    conn.close()

    if not tickers:
        yield _sse("⚠  No tickers in library yet. Download at least one ticker first.",
                   done=True, error=True)
        return

    n_label = f"last {last}" if last > 0 else "all"
    yield _sse(f"🔄  Batch refresh — {len(tickers)} ticker(s), {n_label} filing(s) each…",
               total=len(tickers))

    for i, tic in enumerate(tickers):
        yield _sse(f"\n━━━  {tic}  ({i + 1}/{len(tickers)})  ━━━",
                   count=i, total=len(tickers))
        yield from _run_download(tic, forms, last=last, _suppress_done=True)

    yield _sse(f"🎉  Batch refresh complete — {len(tickers)} ticker(s) processed.",
               done=True, count=len(tickers), total=len(tickers))


# ── HTML template ─────────────────────────────────────────────────────────────

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>US Financial Reports</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  __MCW_HEAD__
  <style>
    body            { background:#f8f9fa; font-size:.9rem; }
    h1              { font-size:1.5rem; }
    #logBox         { font-family:monospace; font-size:.78rem; height:200px;
                      overflow-y:auto; background:#1e1e1e; color:#d4d4d4;
                      border-radius:6px; padding:8px 12px; }
    .progress       { height:6px; }
    .bp             { font-size:.72rem; font-weight:600; }
    .b10k           { background:#cce5ff !important; color:#004085 !important; }
    .b10q           { background:#d4edda !important; color:#155724 !important; }
    .b8k            { background:#e2d9f3 !important; color:#6610f2 !important; }
    .b20f           { background:#d1ecf1 !important; color:#0c5460 !important; }
    .b6k            { background:#fde8d8 !important; color:#8a3a00 !important; }
    .bgnw           { background:#fef3cd !important; color:#856404 !important; }
    .bamend         { background:#fff3cd !important; color:#856404 !important; }
    .table th       { font-size:.78rem; color:#555; white-space:nowrap; }
    .del-btn   { font-size:.72rem; padding:.15rem .45rem; }
    .bp-link   { cursor:pointer; text-decoration:none; }
    .bp-link:hover { opacity:.75; }
    #search         { max-width:280px; }
    code            { font-size:.78rem; }
    __MCW_CSS__
  </style>
</head>
<body>
__NAV__
__URLPATCH__
<div class="container-fluid py-3 px-4">
  <h1 class="mb-0">📊 US Financial Reports</h1>
  <p class="text-muted mb-3" style="font-size:.8rem">
    SEC EDGAR 10-K / 10-Q / 8-K / 20-F / 6-K downloader &mdash; 8-K scans EX-99 exhibits &mdash;
    20-F / 6-K for Foreign Private Issuers (TSM, ASML, SHEL…) &mdash; GNW: Globe Newswire press releases &mdash;
    files stored in <code>financial_reports/&lt;TICKER&gt;/</code>
  </p>

  <!-- ── Download card ── -->
  <div class="card mb-4" style="max-width:580px">
    <div class="card-body pb-2">
      <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
        <input id="tickerInput" class="form-control form-control-sm"
               style="max-width:100px;font-size:1rem;font-weight:700;text-transform:uppercase"
               placeholder="AAPL" maxlength="12"
               onkeydown="if(event.key==='Enter') startDownload()"
               oninput="this.value=this.value.toUpperCase()">
        <div class="d-flex gap-3 ms-1">
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk10K" checked>
            <label class="form-check-label fw-bold" for="chk10K"
                   style="color:#004085">10-K (annual)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk10Q" checked>
            <label class="form-check-label fw-bold" for="chk10Q"
                   style="color:#155724">10-Q (quarterly)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk8K">
            <label class="form-check-label fw-bold" for="chk8K"
                   style="color:#6610f2">8-K (EX-99 exhibits)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk20F">
            <label class="form-check-label fw-bold" for="chk20F"
                   style="color:#0c5460">20-F (FPI annual)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chk6K">
            <label class="form-check-label fw-bold" for="chk6K"
                   style="color:#8a3a00">6-K (FPI reports)</label>
          </div>
          <div class="form-check mb-0">
            <input class="form-check-input" type="checkbox" id="chkGNW">
            <label class="form-check-label fw-bold" for="chkGNW"
                   style="color:#856404">GNW (Globe Newswire)</label>
          </div>
        </div>
        <button class="btn btn-primary btn-sm ms-1" id="dlBtn"
                onclick="startDownload()">⬇ Download All</button>
      </div>

      <!-- ── Batch refresh row ── -->
      <div class="d-flex align-items-center gap-2 mt-1 mb-1">
        <span class="text-muted" style="font-size:.8rem;white-space:nowrap">Refresh all tickers — last</span>
        <input id="batchLastN" type="number" min="1" max="99" value="4"
               class="form-control form-control-sm" style="width:64px">
        <span class="text-muted" style="font-size:.8rem">filing(s)</span>
        <button class="btn btn-outline-secondary btn-sm" id="batchBtn"
                onclick="startBatchDownload()">🔄 Refresh All Tickers</button>
      </div>

      <div id="progressSection" style="display:none">
        <div class="progress mb-2">
          <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
               id="progressBar" style="width:0%"></div>
        </div>
        <div id="logBox"></div>
      </div>
    </div>
  </div>

  <!-- ── Filter bar ── -->
  <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
    <input id="search" class="form-control form-control-sm"
           placeholder="Search ticker / company / period…"
           oninput="applyFilters()">
    <div id="formBtns" class="d-flex gap-1"></div>
    <div class="btn-group ms-1" role="group" style="font-size:.72rem">
      <button id="sortFiledBtn" type="button"
              class="btn btn-sm btn-dark"
              onclick="setSort('filed')"
              title="Sort by filed date (newest first)">📅 Filed ↓</button>
      <button id="sortTickerBtn" type="button"
              class="btn btn-sm btn-outline-secondary"
              onclick="setSort('ticker')"
              title="Sort by ticker then period">🔤 Ticker</button>
    </div>
    <span id="rowCount" class="text-muted ms-auto" style="font-size:.78rem"></span>
  </div>
  <div id="tickerChips" class="d-flex gap-1 flex-wrap mb-2"></div>

  <!-- ── Reports table ── -->
  <div class="table-responsive">
    <table class="table table-sm table-hover align-middle" id="reportsTable">
      <thead class="table-light">
        <tr>
          <th style="width:2.5rem">#</th>
          <th>Ticker</th>
          <th>Company</th>
          <th>Period</th>
          <th>Form</th>
          <th>Filed</th>
          <th>Size</th>
          <th>Comment</th>
          <th></th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
    <p id="emptyMsg" class="text-center text-muted py-4" style="display:none">
      No reports yet. Enter a ticker and click <strong>Download All</strong>.
    </p>
  </div>
  <div id="reports-pager" class="d-none d-flex align-items-center gap-2 mt-2 mb-1"></div>
</div>

__MCW_MODALS__

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
window._commentSavePrefix = window._BASE||'';
let _page     = 1;
let _total    = 0;
let _pages    = 1;
const _pageSize = 50;
let _actTick  = null;
let _actForm  = null;
let _sortMode = 'filed';
let _searchTimer = null;

// ── helpers ──────────────────────────────────────────────────────────────────
function htmlEsc(s) {
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function fmtSize(b) {
  if (!b) return '—';
  return b < 1048576 ? Math.round(b/1024)+'&nbsp;KB' : (b/1048576).toFixed(1)+'&nbsp;MB';
}
function badgeCls(f) {
  if (!f) return 'bg-secondary';
  if (f.endsWith('/A')) return 'bamend';
  if (f.includes('10-K')) return 'b10k';
  if (f.includes('10-Q')) return 'b10q';
  if (f.includes('8-K'))  return 'b8k';
  if (f.includes('20-F')) return 'b20f';
  if (f.includes('6-K'))  return 'b6k';
  if (f === 'GNW')        return 'bgnw';
  return 'bg-secondary';
}

// ── stats (chips + form buttons) ─────────────────────────────────────────────
function loadStats() {
  fetch('/stats').then(r=>r.json()).then(stats => {
    rebuildFormBtns(stats.forms || {});
    rebuildChips(stats.tickers || {});
  });
}

function rebuildFormBtns(formCounts) {
  const specs = [
    { key:'10-K', label:'10-K', cls:'b10k', outline:'outline-primary'   },
    { key:'10-Q', label:'10-Q', cls:'b10q', outline:'outline-success'   },
    { key:'8-K',  label:'8-K',  cls:'b8k',  outline:'outline-secondary' },
    { key:'20-F', label:'20-F', cls:'b20f', outline:'outline-info'      },
    { key:'6-K',  label:'6-K',  cls:'b6k',  outline:'outline-warning'   },
    { key:'GNW',  label:'GNW',  cls:'bgnw', outline:'outline-warning'   },
  ];
  const div = document.getElementById('formBtns');
  div.innerHTML = '';
  specs.forEach(({key, label, cls, outline}) => {
    const count = Object.entries(formCounts)
      .filter(([ft]) => ft && ft.includes(key))
      .reduce((s, [,c]) => s+c, 0);
    const active = _actForm === key;
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm ' + (active ? `badge bp ${cls}` : `btn-${outline}`);
    btn.style.cssText = 'font-size:.72rem;padding:.15rem .55rem;font-weight:600';
    btn.innerHTML = `${label} <span class="badge bg-light text-dark">${count}</span>`;
    btn.onclick = () => { _actForm = _actForm===key ? null : key; loadStats(); fetchReports(1); };
    div.appendChild(btn);
  });
}

function rebuildChips(tickerCounts) {
  const tickers = Object.keys(tickerCounts).sort();
  const div = document.getElementById('tickerChips');
  div.innerHTML = '';
  tickers.forEach(t => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm ' + (t===_actTick ? 'btn-dark' : 'btn-outline-secondary');
    btn.style.cssText = 'font-size:.72rem;padding:.1rem .5rem';
    btn.innerHTML = `${t} <span class="badge bg-light text-dark">${tickerCounts[t]}</span>`;
    btn.onclick = () => { _actTick = _actTick===t ? null : t; loadStats(); fetchReports(1); };
    div.appendChild(btn);
  });
}

// ── server-side fetch ─────────────────────────────────────────────────────────
function fetchReports(page) {
  _page = page || 1;
  const q = document.getElementById('search').value.trim();
  const params = new URLSearchParams({
    page: _page, per_page: _pageSize, sort: _sortMode,
  });
  if (q)       params.set('q',      q);
  if (_actTick) params.set('ticker', _actTick);
  if (_actForm) params.set('form',   _actForm);

  fetch('/reports?' + params).then(r=>r.json()).then(data => {
    _total = data.total;
    _pages = data.pages;
    renderRows(data.rows);
    _renderPager();
  });
}

function setSort(mode) {
  _sortMode = mode;
  document.getElementById('sortFiledBtn').className  =
    'btn btn-sm ' + (mode === 'filed'  ? 'btn-dark' : 'btn-outline-secondary');
  document.getElementById('sortTickerBtn').className =
    'btn btn-sm ' + (mode === 'ticker' ? 'btn-dark' : 'btn-outline-secondary');
  fetchReports(1);
}

function applyFilters() {
  clearTimeout(_searchTimer);
  _searchTimer = setTimeout(() => fetchReports(1), 250);
}

function _renderPager() {
  const pager = document.getElementById('reports-pager');
  if (!pager) return;
  pager.classList.toggle('d-none', _total <= _pageSize);
  if (_total === 0) { pager.innerHTML = ''; return; }
  const start = (_page - 1) * _pageSize + 1;
  const end   = Math.min(_page * _pageSize, _total);
  let html = `<small class="text-muted me-2">${start}\u2013${end} of ${_total}</small>`;
  html += `<ul class="pagination pagination-sm mb-0">`;
  html += `<li class="page-item${_page === 1 ? ' disabled' : ''}">`;
  html += `<a class="page-link" href="#" onclick="fetchReports(${_page-1});return false">\u2039</a></li>`;
  for (const p of _pageRange(_page, _pages)) {
    if (p === '\u2026') {
      html += `<li class="page-item disabled"><span class="page-link">\u2026</span></li>`;
    } else {
      html += `<li class="page-item${p === _page ? ' active' : ''}">`;
      html += `<a class="page-link" href="#" onclick="fetchReports(${p});return false">${p}</a></li>`;
    }
  }
  html += `<li class="page-item${_page === _pages ? ' disabled' : ''}">`;
  html += `<a class="page-link" href="#" onclick="fetchReports(${_page+1});return false">\u203a</a></li>`;
  html += `</ul>`;
  pager.innerHTML = html;
}

function _pageRange(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
  const set    = new Set([1, Math.max(1, current-1), current, Math.min(total, current+1), total]);
  const sorted = [...set].sort((a,b) => a-b);
  const result = []; let prev = 0;
  for (const p of sorted) {
    if (p - prev > 1) result.push('\u2026');
    result.push(p); prev = p;
  }
  return result;
}

function renderRows(rows) {
  const startIndex = (_page - 1) * _pageSize;
  const tbody = document.getElementById('tbody');
  const empty = document.getElementById('emptyMsg');
  document.getElementById('rowCount').textContent =
    _total + ' report' + (_total!==1?'s':'');
  if (!_total) { tbody.innerHTML=''; empty.style.display=''; return; }
  empty.style.display = 'none';
  tbody.innerHTML = rows.map((r,i) => `
    <tr>
      <td class="text-muted">${startIndex + i + 1}</td>
      <td><strong>${r.ticker}</strong></td>
      <td style="max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${(r.company_name||'').replace(/"/g,'&quot;')}">${r.company_name||'—'}</td>
      <td>
        ${r.local_path
          ? `<a href="${window._BASE||''}/file/${r.id}" target="_blank" class="badge bp bg-secondary bp-link"
               title="Click to open">${r.period}</a>`
          : `<span class="badge bp bg-secondary">${r.period}</span>`}
      </td>
      <td><span class="badge bp ${badgeCls(r.form_type)}">${r.form_type||'—'}</span></td>
      <td class="text-muted">${r.filed_date||'—'}</td>
      <td class="text-muted">${fmtSize(r.file_size)}</td>
      <td id="comment-cell-${r.id}" style="max-width:160px">
        <span class="comment-preview" data-comment="${htmlEsc(r.comment)}"
              title="Click to preview / edit"></span>
      </td>
      <td class="text-end pe-2 text-nowrap">
        ${r.local_path
          ? (r.graphiti_indexed_at
              ? `<span class="badge bg-success me-1" title="Indexed ${r.graphiti_indexed_at.slice(0,10)}">✓ KG</span>`
              : `<button class="btn btn-outline-primary btn-sm me-1 idx-btn" title="Index into knowledge graph"
                         onclick="indexReport(${r.id},this)">⬆ KG</button>`)
          : ''}
        <button class="btn btn-outline-danger del-btn"
                onclick="deleteReport(${r.id},this)">🗑</button>
      </td>
    </tr>`).join('');
  if (typeof renderAllCommentCells === 'function') renderAllCommentCells();
}

// ── download ─────────────────────────────────────────────────────────────────
function startDownload() {
  const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!ticker) { alert('Enter a ticker symbol (e.g. AAPL, NVDA, TSLA)'); return; }
  const forms = [];
  if (document.getElementById('chk10K').checked)  forms.push('10-K');
  if (document.getElementById('chk10Q').checked)  forms.push('10-Q');
  if (document.getElementById('chk8K').checked)   forms.push('8-K');
  if (document.getElementById('chk20F').checked)  forms.push('20-F');
  if (document.getElementById('chk6K').checked)   forms.push('6-K');
  if (document.getElementById('chkGNW').checked)  forms.push('GNW');
  if (!forms.length) { alert('Select at least one form type.'); return; }

  document.getElementById('progressSection').style.display = '';
  document.getElementById('dlBtn').disabled = true;
  const bar = document.getElementById('progressBar');
  bar.style.width = '0%';
  bar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  const log = document.getElementById('logBox');
  log.innerHTML = '';

  const params = new URLSearchParams({ ticker, forms: forms.join(',') });
  const es = new EventSource('/stream-download?' + params);

  es.onmessage = e => {
    const d = JSON.parse(e.data);
    const line = document.createElement('div');
    line.textContent = d.msg;
    if (d.error) line.style.color = '#f48771';
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;

    if (d.total > 0)
      bar.style.width = Math.round(d.count / d.total * 100) + '%';

    if (d.done) {
      es.close();
      document.getElementById('dlBtn').disabled = false;
      bar.style.width = '100%';
      bar.classList.remove('progress-bar-animated');
      if (!d.error) {
        bar.classList.remove('bg-primary');
        bar.classList.add('bg-success');
      }
      loadStats(); fetchReports(1);
    }
  };
  es.onerror = () => {
    const line = document.createElement('div');
    line.textContent = '⚠ Connection lost';
    line.style.color = '#f48771';
    log.appendChild(line);
    es.close();
    document.getElementById('dlBtn').disabled = false;
  };
}

function startBatchDownload() {
  const last = parseInt(document.getElementById('batchLastN').value) || 4;
  const forms = [];
  if (document.getElementById('chk10K').checked)  forms.push('10-K');
  if (document.getElementById('chk10Q').checked)  forms.push('10-Q');
  if (document.getElementById('chk8K').checked)   forms.push('8-K');
  if (document.getElementById('chk20F').checked)  forms.push('20-F');
  if (document.getElementById('chk6K').checked)   forms.push('6-K');
  if (document.getElementById('chkGNW').checked)  forms.push('GNW');
  if (!forms.length) { alert('Select at least one form type.'); return; }

  document.getElementById('progressSection').style.display = '';
  document.getElementById('dlBtn').disabled = true;
  document.getElementById('batchBtn').disabled = true;
  const bar = document.getElementById('progressBar');
  bar.style.width = '0%';
  bar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  const log = document.getElementById('logBox');
  log.innerHTML = '';

  const params = new URLSearchParams({ forms: forms.join(','), last });
  const base = window._BASE || '';
  const es = new EventSource(base + '/stream-batch-download?' + params);

  es.onmessage = e => {
    const d = JSON.parse(e.data);
    const line = document.createElement('div');
    line.textContent = d.msg;
    if (d.error) line.style.color = '#f48771';
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;

    if (d.total > 0)
      bar.style.width = Math.round(d.count / d.total * 100) + '%';

    if (d.done) {
      es.close();
      document.getElementById('dlBtn').disabled = false;
      document.getElementById('batchBtn').disabled = false;
      bar.style.width = '100%';
      bar.classList.remove('progress-bar-animated');
      if (!d.error) {
        bar.classList.remove('bg-primary');
        bar.classList.add('bg-success');
      }
      loadStats(); fetchReports(1);
    }
  };
  es.onerror = () => {
    const line = document.createElement('div');
    line.textContent = '⚠ Connection lost';
    line.style.color = '#f48771';
    log.appendChild(line);
    es.close();
    document.getElementById('dlBtn').disabled = false;
    document.getElementById('batchBtn').disabled = false;
  };
}

// ── delete ────────────────────────────────────────────────────────────────────
function deleteReport(id) {
  if (!confirm('Remove this report from the library? (The local file will also be deleted.)')) return;
  fetch('/report/' + id, { method: 'DELETE' }).then(r => {
    if (r.ok) { loadStats(); fetchReports(_page); }
  });
}

function indexReport(id, btn) {
  btn.disabled = true;
  btn.textContent = '⏳';

  // Small log modal
  const modal = document.createElement('div');
  modal.style.cssText = 'position:fixed;bottom:1rem;right:1rem;width:420px;max-height:260px;overflow-y:auto;' +
    'background:#1e1e1e;color:#d4d4d4;font:12px/1.5 monospace;padding:.75rem 1rem;border-radius:8px;' +
    'box-shadow:0 4px 20px rgba(0,0,0,.5);z-index:9999';
  document.body.appendChild(modal);

  const es = new EventSource('/index-report/' + id, {method: 'POST'});
  // EventSource is GET-only; use fetch SSE pattern instead
  es.close();
  modal.textContent = 'Starting…\\n';

  fetch('/index-report/' + id, {method: 'POST'})
    .then(async res => {
      const reader = res.body.getReader();
      const dec    = new TextDecoder();
      let buf = '';
      while (true) {
        const {value, done} = await reader.read();
        if (done) break;
        buf += dec.decode(value, {stream: true});
        const lines = buf.split('\\n');
        buf = lines.pop();
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const msg = line.slice(6);
          if (msg.startsWith('__done__:')) {
            const code = parseInt(msg.split(':')[1]);
            if (code === 0) {
              btn.textContent = '✓ KG';
              btn.className = 'badge bg-success me-1';
              btn.onclick = null;
              // Update in-memory row so the badge sticks on re-render
              const row = _rows.find(r => r.id === id);
              if (row) row.graphiti_indexed_at = new Date().toISOString();
              // Sync mirror so new entities/edges appear in the graph UI immediately
              modal.textContent += 'Syncing graph mirror…\\n';
              modal.scrollTop = modal.scrollHeight;
              fetch((window._BASE||'') + '/zep/refresh-mirror', {method:'POST'})
                .then(r => r.json())
                .then(d => { modal.textContent += d.ok ? `✓ Mirror synced (${d.entities} entities, ${d.edges} edges)\\n` : `⚠ Mirror sync: ${d.error}\\n`; })
                .catch(e => { modal.textContent += `⚠ Mirror sync failed: ${e.message}\\n`; })
                .finally(() => { modal.scrollTop = modal.scrollHeight; setTimeout(() => modal.remove(), 3000); });
            } else {
              btn.disabled = false;
              btn.textContent = '⬆ KG';
              setTimeout(() => modal.remove(), 4000);
            }
          } else {
            modal.textContent += msg + '\\n';
            modal.scrollTop = modal.scrollHeight;
          }
        }
      }
    })
    .catch(e => {
      modal.textContent += 'Error: ' + e.message;
      btn.disabled = false;
      btn.textContent = '⬆ KG';
      setTimeout(() => modal.remove(), 5000);
    });
}

// init
loadStats(); fetchReports(1);

__MCW_JS__
</script>
</body>
</html>
"""

# Apply shared markdown comment widget substitutions
for _k, _v in mcw.TEMPLATE_PARTS.items():
    TEMPLATE = TEMPLATE.replace(_k, _v)
TEMPLATE = TEMPLATE.replace("__NAV__",      nw2.NAV_HTML)
TEMPLATE = TEMPLATE.replace("__URLPATCH__", nw2.URL_PATCH_JS)


# ── Flask routes ──────────────────────────────────────────────────────────────

@sec_bp.route("/")
def index():
    from flask import url_for
    # url_for('.index') = '/sec/' when mounted, '/' standalone → strip trailing /
    base = url_for('.index').rstrip('/')
    return render_template_string(TEMPLATE, _base=base)


@sec_bp.route("/stats")
def report_stats():
    """Lightweight endpoint: counts by ticker and form_type for chips/buttons."""
    conn = get_conn()
    by_ticker = conn.execute(
        "SELECT ticker, COUNT(*) as cnt FROM reports GROUP BY ticker ORDER BY ticker"
    ).fetchall()
    by_form = conn.execute(
        "SELECT form_type, COUNT(*) as cnt FROM reports GROUP BY form_type"
    ).fetchall()
    conn.close()
    return jsonify({
        "tickers": {r["ticker"]: r["cnt"] for r in by_ticker},
        "forms":   {r["form_type"]: r["cnt"] for r in by_form},
    })


@sec_bp.route("/reports")
def list_reports():
    """Server-side search + pagination. Returns {rows, total, page, pages}."""
    q        = request.args.get("q", "").strip().lower()
    ticker   = request.args.get("ticker", "").upper().strip()
    form     = request.args.get("form", "").strip()
    sort     = request.args.get("sort", "filed")   # 'filed' | 'ticker'
    page     = max(1, int(request.args.get("page", 1)))
    per_page = min(200, max(1, int(request.args.get("per_page", 50))))

    where_clauses, params = [], []

    if ticker:
        where_clauses.append("ticker = ?")
        params.append(ticker)
    if form:
        where_clauses.append("form_type LIKE ?")
        params.append(f"%{form}%")
    if q:
        where_clauses.append(
            "(LOWER(ticker) LIKE ? OR LOWER(company_name) LIKE ? "
            "OR LOWER(period) LIKE ? OR LOWER(form_type) LIKE ? OR filed_date LIKE ?)"
        )
        like = f"%{q}%"
        params.extend([like, like, like, like, like])

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    order_sql = (
        "ORDER BY filed_date DESC, id DESC"
        if sort == "filed"
        else "ORDER BY ticker ASC, period_of_report DESC, id DESC"
    )

    conn  = get_conn()
    total = conn.execute(
        f"SELECT COUNT(*) FROM reports {where_sql}", params
    ).fetchone()[0]

    offset = (page - 1) * per_page
    rows   = conn.execute(
        f"SELECT * FROM reports {where_sql} {order_sql} LIMIT {per_page} OFFSET {offset}",
        params,
    ).fetchall()
    conn.close()

    return jsonify({
        "rows":  [dict(r) for r in rows],
        "total": total,
        "page":  page,
        "pages": max(1, (total + per_page - 1) // per_page),
    })


@sec_bp.route("/stream-download")
def stream_download_route():
    ticker = request.args.get("ticker", "").strip()
    forms  = [
        f.strip()
        for f in request.args.get("forms", "10-K,10-Q").split(",")
        if f.strip()
    ]
    if not ticker:
        return "ticker required", 400
    return Response(
        _run_download(ticker, forms),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@sec_bp.route("/stream-batch-download")
def stream_batch_download_route():
    forms = [
        f.strip()
        for f in request.args.get("forms", "10-K,10-Q").split(",")
        if f.strip()
    ]
    last = max(0, int(request.args.get("last", 4)))
    return Response(
        _run_batch_download(forms, last),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@sec_bp.route("/index-report/<int:report_id>", methods=["POST"])
def index_report(report_id: int):
    """SSE stream: index a single report into graphiti."""
    import subprocess, sys as _sys, os as _os
    from pathlib import Path as _Path
    ingestor = _Path(__file__).parent / "ingest" / "graphiti_ingest.py"

    def _gen():
        proc = subprocess.Popen(
            [_sys.executable, "-u", str(ingestor),
             "--source", "financial_reports", "--report-id", str(report_id)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
            env={**_os.environ, "PYTHONUNBUFFERED": "1"},
        )
        for line in proc.stdout:
            yield f"data: {line.rstrip()}\n\n"
        proc.wait()
        yield f"data: __done__:{proc.returncode}\n\n"

    return Response(_gen(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@sec_bp.route("/file/<int:report_id>")
def serve_file(report_id: int):
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path, form_type, ticker, period, accession_no FROM reports WHERE id=?",
        (report_id,),
    ).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        abort(404)
    path = Path(row["local_path"])
    if not path.exists():
        abort(404)

    # For HTML 8-K exhibits: inject <base> + responsive CSS so images load and fit
    acc_no = row["accession_no"] or ""
    if path.suffix.lower() in (".htm", ".html") and "/" in acc_no:
        try:
            acc      = acc_no.split("/")[0]
            cik, _   = resolve_cik(row["ticker"])
            clean    = acc.replace("-", "")
            base_url = (
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{clean}/"
            )
            html  = path.read_bytes().decode("utf-8", errors="replace")
            lower = html.lower()
            inject = (
                f'<base href="{base_url}">'
                f'<style>'
                f'img{{max-width:100%!important;height:auto!important}}'
                f'div,table{{max-width:100%!important;overflow-x:hidden!important}}'
                f'body{{overflow-x:hidden;margin:0 auto;padding:8px;box-sizing:border-box}}'
                f'</style>'
            )
            if "<head>" in lower:
                pos  = lower.index("<head>") + len("<head>")
            elif "<head" in lower:
                pos  = lower.index("<head")
                pos  = lower.index(">", pos) + 1
            else:
                pos  = 0
            html = html[:pos] + inject + html[pos:]
            from flask import make_response
            resp = make_response(html)
            resp.headers["Content-Type"] = "text/html; charset=utf-8"
            return resp
        except Exception:
            pass  # fall through to plain send_file

    return send_file(path)


@sec_bp.route("/comment/<int:report_id>", methods=["POST"])
def set_comment(report_id: int):
    comment = request.form.get("comment", "").strip()
    conn = get_conn()
    conn.execute(
        "UPDATE reports SET comment = ? WHERE id = ?",
        (comment or None, report_id),
    )
    conn.commit()
    conn.close()
    return "", 204


@sec_bp.route("/report/<int:report_id>", methods=["DELETE"])
def delete_report(report_id: int):
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path FROM reports WHERE id=?", (report_id,)
    ).fetchone()
    if row and row["local_path"]:
        p = Path(row["local_path"])
        if p.exists():
            p.unlink()
    conn.execute("DELETE FROM reports WHERE id=?", (report_id,))
    conn.commit()
    conn.close()
    return "", 204


# Register blueprint on the standalone app (after all routes are defined)
app.register_blueprint(sec_bp)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="US Financial Report downloader (SEC EDGAR 10-K / 10-Q)"
    )
    parser.add_argument("--port", type=int, default=8081,
                        help="Port to listen on (default: 8081)")
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    global _DB_PATH
    _DB_PATH = DB_FILE

    init_db()

    import socket
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        local_ip = None
    print(f"  financial-reports →  http://127.0.0.1:{args.port}")
    if local_ip:
        print(f"  financial-reports →  http://{local_ip}:{args.port}")
    print(f"  Reports folder    →  {REPORTS_DIR}")
    print(f"  DB                →  {DB_FILE}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
