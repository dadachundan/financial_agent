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
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from flask import Flask, Blueprint, Response, abort, jsonify, render_template_string, request, send_file
import md_comment_widget as mcw
import nav_widget2 as nw2

# ── Paths & config ────────────────────────────────────────────────────────────

from db_paths import db_path

SCRIPT_DIR  = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "financial_reports"
UPLOADS_DIR = SCRIPT_DIR / "uploads"
DB_FILE     = db_path("financial_reports.db")

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


# Mount the in-browser PDF viewer (selection-anchored markdown comments).
# Routes land at /sec/pdf-viewer/<report_id>, /sec/pdf-inline-comments/*, etc.
import pdf_viewer as _pdf_viewer


def _sec_pdf_meta(report_id: int) -> dict | None:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT local_path, ticker, period, form_type "
            "FROM reports WHERE id = ?",
            (report_id,),
        ).fetchone()
    finally:
        conn.close()
    if not row or not row["local_path"]:
        return None
    label = f"{row['ticker']} {row['form_type'] or ''} {row['period'] or ''}".strip()
    return {
        "local_path": row["local_path"],
        "name": Path(row["local_path"]).name,
        "title": label or f"SEC {report_id}",
    }


_pdf_viewer.register(sec_bp, source="sec", path_provider=_sec_pdf_meta)


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
        try:
            conn.execute("ALTER TABLE reports ADD COLUMN comment_updated_at TEXT")
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

        # FPI hint: if nothing matched but EDGAR has 20-F/6-K, suggest those checkboxes
        if not summary_parts:
            fpi_forms_present = {f["form"] for f in all_filings if f["form"] in ("20-F", "20-F/A", "6-K", "6-K/A")}
            if fpi_forms_present and not ({"20-F", "6-K"} & set(forms)):
                yield _sse(
                    f"ℹ️  {company_name} is a Foreign Private Issuer — "
                    f"it files {', '.join(sorted(fpi_forms_present))} instead of 10-K/10-Q. "
                    f"Check the 20-F / 6-K boxes and try again.",
                    error=True,
                )

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

                # For 6-K: also download exhibit files so relative links in the HTM work
                if form.startswith("6-K"):
                    clean_acc = acc.replace("-", "")
                    exhibits = _get_8k_exhibits(cik, acc)
                    for ex in exhibits:
                        ex_fname = ex["filename"]
                        ex_dest  = ticker_dir / ex_fname
                        if ex_dest.exists():
                            continue
                        ex_url = (
                            f"https://www.sec.gov/Archives/edgar/data"
                            f"/{int(cik)}/{clean_acc}/{ex_fname}"
                        )
                        try:
                            r2 = _sec_get(ex_url, stream=True)
                            with open(ex_dest, "wb") as fh:
                                for chunk in r2.iter_content(65536):
                                    fh.write(chunk)
                            yield _sse(
                                f"       📎  {ex_fname}  ({ex['type']})",
                                count=counter, total=grand_total,
                            )
                        except Exception:
                            pass  # best-effort; don't fail the parent filing

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
  <title>US SEC Reports</title>
  <link rel="stylesheet" href="/static/vendor/bootstrap.min.css">
  __MCW_HEAD__
  <style>
    body          { background:#f8f9fa; font-size:.9rem; }
    h1            { font-size:1.5rem; }
    #logBox       { font-family:monospace; font-size:.78rem; height:180px;
                    overflow-y:auto; background:#1e1e1e; color:#d4d4d4;
                    border-radius:6px; padding:8px 12px; }
    .progress     { height:6px; }
    .bp           { font-size:.72rem; font-weight:600; }
    .b-10k        { background:#dbeafe !important; color:#1e40af !important; }
    .b-10q        { background:#dcfce7 !important; color:#166534 !important; }
    .b-8k         { background:#ede9fe !important; color:#5b21b6 !important; }
    .b-20f        { background:#cffafe !important; color:#155e75 !important; }
    .b-6k         { background:#ffedd5 !important; color:#9a3412 !important; }
    .b-gnw        { background:#fef9c3 !important; color:#854d0e !important; }
    .b-amend      { background:#fef3c7 !important; color:#92400e !important; }
    .table th     { font-size:.78rem; color:#555; white-space:nowrap; }
    .del-btn      { font-size:.72rem; padding:.15rem .45rem; }
    #search       { max-width:280px; }
    code          { font-size:.78rem; }
    .ticker-chip-bar { max-height:80px; overflow-y:auto; }
    __MCW_CSS__
  </style>
</head>
<body>
__NAV__
__URLPATCH__
<div class="container-fluid py-3 px-4">
  <h1 class="mb-0">📊 US SEC Reports</h1>
  <p class="text-muted mb-3" style="font-size:.8rem">
    SEC EDGAR &mdash; 10-K / 10-Q / 8-K / 20-F / 6-K / GNW &mdash;
    files saved in <code>financial_reports/&lt;TICKER&gt;/</code>
  </p>

  <!-- ── Download card ── -->
  <div class="card mb-4" style="max-width:780px">
    <div class="card-body pb-2">
      <div class="d-flex flex-wrap gap-2 align-items-center mb-2">
        <input id="tickerInput" class="form-control form-control-sm"
               style="max-width:120px;font-size:1rem;font-weight:700;text-transform:uppercase"
               placeholder="AAPL" maxlength="12"
               onkeydown="if(event.key==='Enter') startDownload()"
               oninput="this.value=this.value.toUpperCase()">
        <div class="d-flex gap-2 ms-1 flex-wrap">
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chk10K" checked>
            <label class="form-check-label fw-bold" for="chk10K" style="color:#1e40af">10-K</label></div>
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chk10Q" checked>
            <label class="form-check-label fw-bold" for="chk10Q" style="color:#166534">10-Q</label></div>
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chk8K" checked>
            <label class="form-check-label fw-bold" for="chk8K" style="color:#5b21b6">8-K</label></div>
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chk20F" checked>
            <label class="form-check-label fw-bold" for="chk20F" style="color:#155e75">20-F</label></div>
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chk6K" checked>
            <label class="form-check-label fw-bold" for="chk6K" style="color:#9a3412">6-K</label></div>
          <div class="form-check mb-0"><input class="form-check-input" type="checkbox" id="chkGNW" checked>
            <label class="form-check-label fw-bold" for="chkGNW" style="color:#854d0e">GNW</label></div>
        </div>
        <button class="btn btn-primary btn-sm ms-1" id="dlBtn"
                onclick="startDownload()">⬇ Download</button>
        <span class="vr ms-1" style="opacity:.25"></span>
        <span class="text-muted ms-1" style="font-size:.76rem;white-space:nowrap">Refresh — last</span>
        <input id="batchLastN" type="number" min="1" max="99" value="4"
               class="form-control form-control-sm" style="width:54px;font-size:.78rem">
        <button class="btn btn-outline-secondary btn-sm" id="batchBtn"
                onclick="startBatchDownload()" style="font-size:.76rem">🔄 Refresh All</button>
      </div>
      <p class="text-muted mb-2" style="font-size:.75rem">
        Examples:&nbsp;<code>AAPL</code>, <code>NVDA</code>, <code>TSLA</code>
      </p>
      <div id="progressSection" style="display:none">
        <div class="progress mb-2">
          <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
               id="progressBar" style="width:0%"></div>
        </div>
        <div id="logBox"></div>
      </div>
    </div>
  </div>

  <!-- ── Filter row ── -->
  <div class="d-flex gap-2 mb-2 align-items-center flex-wrap">
    <input type="search" id="search" class="form-control form-control-sm"
           placeholder="🔍  Filter by ticker / company / period…"
           oninput="applyFilters()">
    <div id="formBtns" class="d-flex gap-1 flex-wrap"></div>
    <span id="rowCount" class="text-muted ms-auto" style="font-size:.78rem"></span>
  </div>
  <!-- ── Company chips ── -->
  <div id="companyChips" class="d-flex gap-1 flex-wrap mb-2 ticker-chip-bar"></div>

  <!-- ── Reports table ── -->
  <div class="table-responsive">
    <table class="table table-sm table-hover table-bordered align-middle" id="repTable">
      <thead class="table-light">
        <tr>
          <th>#</th>
          <th>Ticker</th>
          <th>Company</th>
          <th>Period / Title</th>
          <th>Type</th>
          <th>Date</th>
          <th>Size</th>
          <th>Comment</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="repBody"></tbody>
    </table>
  </div>
  <div id="rep-pager" class="d-none d-flex align-items-center gap-2 mt-2"></div>
</div>

__MCW_MODALS__
<script src="/static/vendor/bootstrap.bundle.min.js"></script>
__MCW_FOOTER__
<script>
window._commentSavePrefix = window._BASE || '';

let _rows = [];
let _filteredRows = [];
let _page = 1;
const PAGE_SIZE = 50;
let _actForm = null;
let _actTicker = null;

function htmlEsc(s) {
  return (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function fmtSize(b) {
  if (!b) return '—';
  return b < 1048576 ? Math.round(b/1024) + ' KB' : (b/1048576).toFixed(1) + ' MB';
}
function badgeClass(ft) {
  if (!ft) return 'badge bp bg-secondary';
  if (ft.endsWith('/A')) return 'badge bp b-amend';
  if (ft.includes('10-K')) return 'badge bp b-10k';
  if (ft.includes('10-Q')) return 'badge bp b-10q';
  if (ft.includes('8-K'))  return 'badge bp b-8k';
  if (ft.includes('20-F')) return 'badge bp b-20f';
  if (ft.includes('6-K'))  return 'badge bp b-6k';
  if (ft === 'GNW')        return 'badge bp b-gnw';
  return 'badge bp bg-secondary';
}

// ── Load reports ──────────────────────────────────────────────────────────────
function loadReports() {
  // fetch() is auto-prefixed with the blueprint base by URL_PATCH_JS.
  fetch('/reports?per_page=50000&page=1').then(r => r.json()).then(data => {
    _rows = data.rows || [];
    rebuildFormBtns();
    rebuildCompanyChips();
    applyFilters();
  });
}

function rebuildFormBtns() {
  const specs = [
    { key:'10-K', cls:'b-10k',  outline:'outline-primary'   },
    { key:'10-Q', cls:'b-10q',  outline:'outline-success'   },
    { key:'8-K',  cls:'b-8k',   outline:'outline-secondary' },
    { key:'20-F', cls:'b-20f',  outline:'outline-info'      },
    { key:'6-K',  cls:'b-6k',   outline:'outline-warning'   },
    { key:'GNW',  cls:'b-gnw',  outline:'outline-warning'   },
  ];
  const div = document.getElementById('formBtns');
  div.innerHTML = '';
  specs.forEach(({key, cls, outline}) => {
    const count = _rows.filter(r => (r.form_type || '').includes(key)).length;
    if (!count) return;
    const active = _actForm === key;
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm ' + (active ? `badge bp ${cls}` : `btn-${outline}`);
    btn.style.cssText = 'font-size:.72rem;padding:.15rem .55rem;font-weight:600';
    btn.innerHTML = `${key} <span class="badge bg-light text-dark">${count}</span>`;
    btn.onclick = () => { _actForm = _actForm === key ? null : key; rebuildFormBtns(); applyFilters(); };
    div.appendChild(btn);
  });
}

function rebuildCompanyChips() {
  const counts = {};
  const names  = {};
  _rows.forEach(r => {
    counts[r.ticker] = (counts[r.ticker] || 0) + 1;
    if (r.company_name) names[r.ticker] = r.company_name;
  });
  const tickers = Object.keys(counts).sort();
  const div = document.getElementById('companyChips');
  div.innerHTML = '';
  tickers.forEach(t => {
    const btn = document.createElement('button');
    const active = t === _actTicker;
    btn.className = 'btn btn-sm ' + (active ? 'btn-dark' : 'btn-outline-secondary');
    btn.style.cssText = 'font-size:.72rem;padding:.1rem .5rem';
    const label = names[t] ? `${htmlEsc(names[t])} <span style="opacity:.6;font-size:.68rem">${t}</span>` : t;
    btn.innerHTML = `${label} <span class="badge bg-light text-dark">${counts[t]}</span>`;
    btn.onclick = () => { _actTicker = _actTicker === t ? null : t; rebuildCompanyChips(); applyFilters(); };
    div.appendChild(btn);
  });
}

function applyFilters() {
  const q = document.getElementById('search').value.toLowerCase();
  _filteredRows = _rows.filter(r => {
    if (_actForm && !(r.form_type || '').includes(_actForm)) return false;
    if (_actTicker && r.ticker !== _actTicker) return false;
    if (q) {
      const hay = [r.ticker, r.company_name, r.period, r.form_type, r.filed_date]
                   .join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
  _page = 1;
  _renderPage();
  _renderPager();
  document.getElementById('rowCount').textContent =
    `${_filteredRows.length} / ${_rows.length} records`;
}

function _renderPage() {
  const start = (_page - 1) * PAGE_SIZE;
  const slice = _filteredRows.slice(start, start + PAGE_SIZE);
  const base = window._BASE || '';
  const tbody = document.getElementById('repBody');
  tbody.innerHTML = slice.map((r, i) => {
    const num = start + i + 1;
    const sz  = fmtSize(r.file_size);
    const periodHtml = r.local_path
      ? `<a href="${base}/file/${r.id}" target="_blank">${htmlEsc(r.period)}</a>`
      : htmlEsc(r.period);
    const commentHtml = `<td id="comment-cell-${r.id}"><span class="comment-preview"
        data-comment="${htmlEsc(r.comment || '')}" title="Click to preview / edit"></span></td>`;
    const openBtn  = r.local_path
      ? `<a href="${base}/file/${r.id}" target="_blank"
           class="btn btn-outline-danger btn-sm del-btn" title="Open in browser">📄</a>`
      : '';
    const annotateBtn = r.local_path
      ? `<a href="${base}/pdf-viewer/${r.id}" target="_blank"
           class="btn btn-outline-primary btn-sm del-btn ms-1"
           title="In-browser viewer with selection-anchored markdown comments">🖍</a>`
      : '';
    const localBtn = r.local_path
      ? `<button onclick="openLocal(${r.id},this)"
           class="btn btn-outline-secondary btn-sm del-btn ms-1" title="Open in local app">🗂</button>`
      : '';
    const pinBtn   = r.local_path
      ? `<button onclick="syncAnnotations(${r.id},this)"
           class="btn btn-outline-success btn-sm del-btn ms-1"
           title="Extract annotations from PDF → save to comment">📌</button>`
      : '';
    return `<tr>
      <td class="text-muted">${num}</td>
      <td><code style="font-size:.78rem">${htmlEsc(r.ticker)}</code></td>
      <td style="max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${htmlEsc(r.company_name||'')}">${htmlEsc(r.company_name||'')}</td>
      <td style="max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
          title="${htmlEsc(r.period||'')}">${periodHtml}</td>
      <td><span class="${badgeClass(r.form_type)}">${htmlEsc(r.form_type||'—')}</span></td>
      <td>${r.filed_date || ''}</td>
      <td class="text-muted">${sz}</td>
      ${commentHtml}
      <td style="white-space:nowrap">
        ${openBtn}
        ${annotateBtn}
        ${localBtn}
        ${pinBtn}
      </td>
    </tr>`;
  }).join('');
  if (typeof renderAllCommentCells === 'function') renderAllCommentCells();
}

function _pageRange(cur, tot) {
  if (tot <= 7) return Array.from({length: tot}, (_, i) => i + 1);
  const pages = [1];
  if (cur > 3) pages.push('…');
  for (let p = Math.max(2, cur - 1); p <= Math.min(tot - 1, cur + 1); p++) pages.push(p);
  if (cur < tot - 2) pages.push('…');
  pages.push(tot);
  return pages;
}

function _renderPager() {
  const tot   = Math.ceil(_filteredRows.length / PAGE_SIZE);
  const pager = document.getElementById('rep-pager');
  if (tot <= 1) { pager.classList.add('d-none'); return; }
  pager.classList.remove('d-none');
  const from  = (_page - 1) * PAGE_SIZE + 1;
  const to    = Math.min(_page * PAGE_SIZE, _filteredRows.length);
  pager.innerHTML = `
    <small class="text-muted me-1">${from}–${to} of ${_filteredRows.length}</small>
    <nav><ul class="pagination pagination-sm mb-0">
      ${_pageRange(_page, tot).map(p =>
        p === '…'
          ? `<li class="page-item disabled"><span class="page-link">…</span></li>`
          : `<li class="page-item ${p === _page ? 'active' : ''}">
               <button class="page-link" onclick="_goPage(${p})">${p}</button>
             </li>`
      ).join('')}
    </ul></nav>`;
}

function _goPage(p) { _page = p; _renderPage(); _renderPager(); }

// ── Open local file ─────────────────────────────────────────────────────────
function openLocal(id, btn) {
  const orig = btn.textContent;
  btn.disabled = true; btn.textContent = '⏳';
  fetch('/open-local/' + id)
    .then(r => r.json())
    .then(d => {
      btn.disabled = false; btn.textContent = orig;
      if (!d.ok) alert(d.error || 'Cannot open file');
    })
    .catch(e => { btn.disabled = false; btn.textContent = orig; alert('Error: ' + e.message); });
}

// ── Extract annotations ─────────────────────────────────────────────────────
function syncAnnotations(id, btn) {
  const orig = btn.textContent;
  btn.disabled = true; btn.textContent = '⏳';
  fetch('/sync-annotations/' + id, {method: 'POST'})
    .then(r => r.json())
    .then(data => {
      btn.disabled = false;
      if (data.ok) {
        const cell = document.getElementById('comment-cell-' + id);
        if (cell && typeof renderCommentCell === 'function') {
          renderCommentCell(cell, id, data.comment);
        }
        // Also update local cached row so future re-renders keep it
        const r = _rows.find(x => x.id === id); if (r) r.comment = data.comment;
        btn.textContent = '✅';
        btn.title = data.count + ' annotation(s) saved';
        setTimeout(() => { btn.textContent = orig; btn.title = 'Extract annotations from PDF → save to comment'; }, 2500);
      } else {
        btn.textContent = '❌';
        btn.title = data.error || 'No annotations found';
        setTimeout(() => { btn.textContent = orig; btn.title = 'Extract annotations from PDF → save to comment'; }, 2500);
      }
    })
    .catch(() => {
      btn.disabled = false; btn.textContent = '❌';
      setTimeout(() => { btn.textContent = orig; }, 2000);
    });
}

// ── Delete ──────────────────────────────────────────────────────────────────
// ── Download ────────────────────────────────────────────────────────────────
function _selectedForms() {
  const forms = [];
  if (document.getElementById('chk10K').checked) forms.push('10-K');
  if (document.getElementById('chk10Q').checked) forms.push('10-Q');
  if (document.getElementById('chk8K').checked)  forms.push('8-K');
  if (document.getElementById('chk20F').checked) forms.push('20-F');
  if (document.getElementById('chk6K').checked)  forms.push('6-K');
  if (document.getElementById('chkGNW').checked) forms.push('GNW');
  return forms;
}

function startDownload() {
  const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!ticker) { alert('Enter a ticker (e.g. AAPL)'); return; }
  const forms = _selectedForms();
  if (!forms.length) { alert('Select at least one form type.'); return; }
  _startStream('/stream-download', new URLSearchParams({ticker, forms: forms.join(',')}));
}

function startBatchDownload() {
  const last  = parseInt(document.getElementById('batchLastN').value) || 4;
  const forms = _selectedForms();
  if (!forms.length) { alert('Select at least one form type.'); return; }
  _startStream('/stream-batch-download', new URLSearchParams({forms: forms.join(','), last}));
}

function _startStream(path, params) {
  document.getElementById('progressSection').style.display = '';
  document.getElementById('dlBtn').disabled    = true;
  document.getElementById('batchBtn').disabled = true;
  const bar = document.getElementById('progressBar');
  bar.style.width = '0%'; bar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  const log = document.getElementById('logBox'); log.innerHTML = '';
  const es  = new EventSource(path + '?' + params);
  es.onmessage = e => {
    const d = JSON.parse(e.data);
    const line = document.createElement('div'); line.textContent = d.msg;
    if (d.error) line.style.color = '#f48771';
    log.appendChild(line); log.scrollTop = log.scrollHeight;
    if (d.total > 0) bar.style.width = Math.round(d.count/d.total*100) + '%';
    if (d.done) {
      es.close();
      document.getElementById('dlBtn').disabled    = false;
      document.getElementById('batchBtn').disabled = false;
      bar.style.width = '100%'; bar.classList.remove('progress-bar-animated');
      if (!d.error) { bar.classList.remove('bg-primary'); bar.classList.add('bg-success'); }
      loadReports();
    }
  };
  es.onerror = () => {
    const line = document.createElement('div'); line.textContent = '⚠ Connection lost'; line.style.color = '#f48771';
    log.appendChild(line); es.close();
    document.getElementById('dlBtn').disabled    = false;
    document.getElementById('batchBtn').disabled = false;
  };
}

__MCW_JS__
loadReports();
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
    per_page = min(50000, max(1, int(request.args.get("per_page", 50))))

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


@sec_bp.route("/open-local/<int:report_id>")
def open_local(report_id: int):
    """Open the report's local file in the system default viewer."""
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path FROM reports WHERE id=?", (report_id,)
    ).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        return jsonify(ok=False, error="No local file recorded"), 404
    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error=f"File not found: {path}"), 404
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        elif sys.platform.startswith("win"):
            subprocess.Popen(["start", "", str(path)], shell=True)
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 500
    return jsonify(ok=True)


@sec_bp.route("/sync-annotations/<int:report_id>", methods=["POST"])
def sync_annotations(report_id: int):
    """Read PDF annotations from disk and save them to the comment field.

    Reuses the extraction & formatting helpers from zsxq_viewer so the
    output format matches the ZSXQ feed exactly.
    """
    import time as _time
    import concurrent.futures as _cf
    import datetime as _dt
    from zsxq_viewer import _extract_annotations_from_pdf, _format_annotations, _prune_orphan_images

    conn = get_conn()
    row = conn.execute(
        "SELECT local_path, ticker, period, comment FROM reports WHERE id = ?", (report_id,)
    ).fetchone()
    conn.close()

    if not row or not row["local_path"]:
        return jsonify(ok=False, error="No local file"), 404

    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error="File not found on disk"), 404

    if path.suffix.lower() != ".pdf":
        return jsonify(ok=False, error="Not a PDF (only PDFs have annotations)"), 200

    print(f"[sec sync-annotations] 📌 {row['ticker']} {row['period']}")
    print(f"                       path: {path}  ({path.stat().st_size/1024:.0f} KB)")
    t0 = _time.time()

    _TIMEOUT = 120.0
    with _cf.ThreadPoolExecutor(max_workers=1) as _pool:
        _fut = _pool.submit(_extract_annotations_from_pdf, path)
        try:
            anns = _fut.result(timeout=_TIMEOUT)
        except _cf.TimeoutError:
            return jsonify(ok=False, error=f"Timed out after {_TIMEOUT:.0f}s"), 200
        except Exception as exc:
            import traceback; traceback.print_exc()
            return jsonify(ok=False, error=str(exc)), 200

    elapsed = _time.time() - t0
    if not anns:
        print(f"                       ⚠ no annotations found  ({elapsed:.1f}s)")
        return jsonify(ok=False, error="No annotations found in PDF"), 200

    print(f"                       ✓ {len(anns)} annotation(s) in {elapsed:.1f}s")
    comment = _format_annotations(anns)
    _prune_orphan_images(row["comment"] or "", comment)
    now = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = get_conn()
    conn.execute(
        "UPDATE reports SET comment = ?, comment_updated_at = ? WHERE id = ?",
        (comment, now, report_id),
    )
    conn.commit()
    conn.close()
    return jsonify(ok=True, count=len(anns), comment=comment)


@sec_bp.route("/reveal/<int:report_id>", methods=["POST"])
def reveal_file(report_id: int):
    """Reveal the report's local file in Finder (macOS) / file manager (Linux/Windows)."""
    conn = get_conn()
    row  = conn.execute(
        "SELECT local_path FROM reports WHERE id=?", (report_id,)
    ).fetchone()
    conn.close()
    if not row or not row["local_path"]:
        return jsonify(ok=False, error="No local file recorded"), 404
    path = Path(row["local_path"])
    if not path.exists():
        return jsonify(ok=False, error=f"File not found: {path}"), 404
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", "-R", str(path)])
        elif sys.platform.startswith("win"):
            subprocess.Popen(["explorer", "/select,", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path.parent)])
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 500
    return jsonify(ok=True, path=str(path))


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
