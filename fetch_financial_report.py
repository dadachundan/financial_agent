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
  <title>US Financial Reports</title>
  <link rel="stylesheet" href="/static/vendor/bootstrap.min.css">
  __MCW_HEAD__
  <style>
    body { background:#f4f6f9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; font-size:.9rem; }

    /* ── layout ── */
    .page-layout { display:flex; align-items:flex-start; width:100%; min-height:calc(100vh - 56px); }

    /* ── sidebar ── */
    .sec-sidebar {
      width:248px; flex-shrink:0; position:sticky; top:56px;
      height:calc(100vh - 56px); display:flex; flex-direction:column;
      background:#fff; border-right:1px solid #e8ecf0; overflow:hidden;
    }
    .sidebar-top { padding:.9rem 1rem .7rem; border-bottom:1px solid #eef0f3; }
    .sidebar-label { font-size:.65rem; font-weight:700; color:#aaa; letter-spacing:.07em;
                     text-transform:uppercase; margin-bottom:.45rem; }
    .sidebar-search input { font-size:.8rem; padding:.28rem .55rem; border-radius:6px; }

    /* form-type filter pills in sidebar */
    .form-pills { display:flex; flex-wrap:wrap; gap:.3rem; margin-bottom:.5rem; }
    .form-pill {
      font-size:.67rem; font-weight:700; padding:.18rem .55rem; border-radius:20px;
      cursor:pointer; border:1.5px solid transparent; transition:all .15s; line-height:1.4;
    }
    .form-pill.fp10k  { background:#dbeafe; color:#1e40af; border-color:#93c5fd; }
    .form-pill.fp10k.active  { background:#1e40af; color:#fff; border-color:#1e40af; }
    .form-pill.fp10q  { background:#dcfce7; color:#166534; border-color:#86efac; }
    .form-pill.fp10q.active  { background:#166534; color:#fff; border-color:#166534; }
    .form-pill.fp8k   { background:#ede9fe; color:#5b21b6; border-color:#c4b5fd; }
    .form-pill.fp8k.active   { background:#5b21b6; color:#fff; border-color:#5b21b6; }
    .form-pill.fp20f  { background:#cffafe; color:#155e75; border-color:#67e8f9; }
    .form-pill.fp20f.active  { background:#155e75; color:#fff; border-color:#155e75; }
    .form-pill.fp6k   { background:#ffedd5; color:#9a3412; border-color:#fdba74; }
    .form-pill.fp6k.active   { background:#9a3412; color:#fff; border-color:#9a3412; }
    .form-pill.fpgnw  { background:#fef9c3; color:#854d0e; border-color:#fde047; }
    .form-pill.fpgnw.active  { background:#854d0e; color:#fff; border-color:#854d0e; }

    /* sort bar */
    .sort-bar { padding:.45rem 1rem; border-bottom:1px solid #eef0f3; display:flex; gap:.35rem; }
    .sort-btn { font-size:.67rem; padding:.2rem .55rem; border-radius:20px;
                border:1.5px solid #d1d5db; background:#fff; color:#6b7280; cursor:pointer; line-height:1.4; }
    .sort-btn.active { background:#1e40af; color:#fff; border-color:#1e40af; }

    /* ticker list */
    .ticker-list { overflow-y:auto; flex:1; padding:.3rem 0; }
    .ticker-item {
      display:flex; align-items:center; justify-content:space-between;
      padding:.28rem 1rem; cursor:pointer; font-size:.8rem; color:#444;
      border-left:3px solid transparent; transition:background .12s;
    }
    .ticker-item:hover { background:#f0f4ff; color:#1e40af; }
    .ticker-item.active { background:#eff6ff; color:#1e40af; font-weight:700;
                          border-left-color:#3b82f6; }
    .ticker-count { font-size:.67rem; background:#e5e7eb; color:#6b7280;
                    padding:.05rem .38rem; border-radius:10px; }
    .ticker-item.active .ticker-count { background:#bfdbfe; color:#1e40af; }

    /* ── main feed ── */
    .feed-col { flex:1; min-width:0; padding:1.1rem 1.4rem 3rem; }

    .feed-header { display:flex; align-items:center; gap:.75rem; margin-bottom:1rem; flex-wrap:wrap; }
    .feed-header h1 { font-size:1.15rem; font-weight:700; margin:0; }
    #rowCount { font-size:.75rem; color:#9ca3af; }
    #search { font-size:.82rem; border-radius:20px; padding:.28rem .9rem;
              border:1.5px solid #d1d5db; outline:none; }
    #search:focus { border-color:#3b82f6; }
    .dl-toggle-btn { font-size:.75rem; padding:.25rem .7rem; border-radius:20px;
                     border:1.5px solid #d1d5db; background:#fff; color:#374151;
                     cursor:pointer; margin-left:auto; white-space:nowrap; }
    .dl-toggle-btn:hover { background:#f9fafb; }

    /* report card */
    .report-card {
      background:#fff; border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,.07);
      margin-bottom:.65rem; padding:.9rem 1.1rem;
      border-left:4px solid #e5e7eb; transition:box-shadow .15s;
    }
    .report-card:hover { box-shadow:0 3px 10px rgba(0,0,0,.1); }
    .report-card.c10k  { border-left-color:#3b82f6; }
    .report-card.c10q  { border-left-color:#22c55e; }
    .report-card.c8k   { border-left-color:#8b5cf6; }
    .report-card.c20f  { border-left-color:#06b6d4; }
    .report-card.c6k   { border-left-color:#f97316; }
    .report-card.cgnw  { border-left-color:#eab308; }
    .report-card.camend{ border-left-color:#f59e0b; }

    .card-top { display:flex; align-items:flex-start; gap:.7rem; }
    .card-badge-col { display:flex; flex-direction:column; gap:.3rem; align-items:center; min-width:50px; }
    .ticker-badge { font-size:.7rem; font-weight:800; color:#1e40af; background:#dbeafe;
                    padding:.18rem .45rem; border-radius:5px; text-align:center; }
    .form-badge { font-size:.6rem; font-weight:700; padding:.13rem .38rem; border-radius:4px; }
    .fb10k  { background:#dbeafe; color:#1e40af; }
    .fb10q  { background:#dcfce7; color:#166534; }
    .fb8k   { background:#ede9fe; color:#5b21b6; }
    .fb20f  { background:#cffafe; color:#155e75; }
    .fb6k   { background:#ffedd5; color:#9a3412; }
    .fbgnw  { background:#fef9c3; color:#854d0e; }
    .fbamend{ background:#fef3c7; color:#92400e; }

    .card-body-col { flex:1; min-width:0; }
    .card-company { font-size:.88rem; font-weight:600; color:#1f2937; margin-bottom:.15rem;
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .card-period { font-size:.83rem; font-weight:600; color:#374151; cursor:pointer; text-decoration:none; }
    .card-period:hover { color:#1e40af; text-decoration:underline; }
    .card-meta { font-size:.72rem; color:#9ca3af; margin-top:.2rem; display:flex; flex-wrap:wrap; gap:.45rem; }

    .card-actions { display:flex; align-items:center; gap:.35rem; flex-shrink:0; }
    .act-btn { font-size:.68rem; padding:.18rem .45rem; border-radius:5px; }

    .card-comment { margin-top:.55rem; padding-top:.55rem; border-top:1px solid #f3f4f6; }

    #emptyMsg { text-align:center; color:#9ca3af; padding:3rem 0; }

    /* download drawer */
    .dl-drawer { background:#fff; border-bottom:1px solid #e5e7eb; padding:.7rem 1.4rem; display:none; }
    .dl-drawer.open { display:block; }
    #logBox { font-family:monospace; font-size:.73rem; height:150px; overflow-y:auto;
              background:#1e1e1e; color:#d4d4d4; border-radius:6px; padding:7px 11px; }
    .progress { height:4px; border-radius:2px; }

    #reports-pager { display:flex; align-items:center; gap:.5rem; margin-top:.75rem; }

    __MCW_CSS__
  </style>
</head>
<body>
__NAV__
__URLPATCH__

<!-- download drawer -->
<div id="dlDrawer" class="dl-drawer">
  <div class="d-flex flex-wrap gap-3 align-items-start">
    <div>
      <div class="d-flex gap-2 align-items-center mb-2">
        <input id="tickerInput" class="form-control form-control-sm"
               style="max-width:86px;font-size:.88rem;font-weight:700;text-transform:uppercase"
               placeholder="AAPL" maxlength="12"
               onkeydown="if(event.key==='Enter') startDownload()"
               oninput="this.value=this.value.toUpperCase()">
        <button class="btn btn-primary btn-sm" id="dlBtn" onclick="startDownload()" style="font-size:.78rem">
          ⬇ Download
        </button>
      </div>
      <div class="d-flex flex-wrap gap-2">
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chk10K" checked>
          <label class="form-check-label" for="chk10K" style="color:#1e40af;font-weight:600;font-size:.76rem">10-K</label>
        </div>
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chk10Q" checked>
          <label class="form-check-label" for="chk10Q" style="color:#166534;font-weight:600;font-size:.76rem">10-Q</label>
        </div>
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chk8K" checked>
          <label class="form-check-label" for="chk8K" style="color:#5b21b6;font-weight:600;font-size:.76rem">8-K</label>
        </div>
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chk20F" checked>
          <label class="form-check-label" for="chk20F" style="color:#155e75;font-weight:600;font-size:.76rem">20-F</label>
        </div>
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chk6K" checked>
          <label class="form-check-label" for="chk6K" style="color:#9a3412;font-weight:600;font-size:.76rem">6-K</label>
        </div>
        <div class="form-check form-check-inline mb-0">
          <input class="form-check-input" type="checkbox" id="chkGNW" checked>
          <label class="form-check-label" for="chkGNW" style="color:#854d0e;font-weight:600;font-size:.76rem">GNW</label>
        </div>
      </div>
    </div>
    <div class="vr" style="opacity:.2"></div>
    <div>
      <div class="d-flex align-items-center gap-2">
        <span class="text-muted" style="font-size:.76rem;white-space:nowrap">Refresh all — last</span>
        <input id="batchLastN" type="number" min="1" max="99" value="4"
               class="form-control form-control-sm" style="width:54px;font-size:.78rem">
        <span class="text-muted" style="font-size:.76rem">filings</span>
        <button class="btn btn-outline-secondary btn-sm" id="batchBtn"
                onclick="startBatchDownload()" style="font-size:.76rem">🔄 Refresh All</button>
      </div>
    </div>
  </div>
  <div id="progressSection" style="display:none;margin-top:.65rem">
    <div class="progress mb-2">
      <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
           id="progressBar" style="width:0%"></div>
    </div>
    <div id="logBox"></div>
  </div>
</div>

<div class="page-layout">

  <!-- sidebar -->
  <aside class="sec-sidebar">
    <div class="sidebar-top">
      <div class="sidebar-label">Form Type</div>
      <div id="formPills" class="form-pills"></div>
      <div class="sidebar-label">Tickers</div>
      <div class="sidebar-search">
        <input id="tickerSearch" type="search" class="form-control form-control-sm"
               placeholder="Filter tickers…" oninput="filterTickers(this.value)">
      </div>
    </div>
    <div class="sort-bar">
      <button id="sortFiledBtn" class="sort-btn active" onclick="setSort('filed')">📅 Recent</button>
      <button id="sortTickerBtn" class="sort-btn" onclick="setSort('ticker')">🔤 Ticker</button>
    </div>
    <div class="ticker-list" id="tickerList"></div>
  </aside>

  <!-- main feed -->
  <main class="feed-col">
    <div class="feed-header">
      <h1>📊 US Reports</h1>
      <input id="search" type="search" placeholder="Search company / period…" oninput="applyFilters()">
      <span id="rowCount"></span>
      <button class="dl-toggle-btn" onclick="toggleDrawer()">⬇ Download</button>
    </div>

    <div id="feedContainer"></div>
    <p id="emptyMsg" style="display:none">No reports yet — enter a ticker and click Download.</p>
    <div id="reports-pager" class="d-none"></div>
  </main>

</div>

__MCW_MODALS__

<script src="/static/vendor/bootstrap.bundle.min.js"></script>
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
let _allTickers = {};

function htmlEsc(s) {
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function fmtSize(b) {
  if (!b) return '';
  return b < 1048576 ? Math.round(b/1024)+' KB' : (b/1048576).toFixed(1)+' MB';
}
function cardClass(f) {
  if (!f) return '';
  if (f.endsWith('/A')) return 'camend';
  if (f.includes('10-K')) return 'c10k';
  if (f.includes('10-Q')) return 'c10q';
  if (f.includes('8-K'))  return 'c8k';
  if (f.includes('20-F')) return 'c20f';
  if (f.includes('6-K'))  return 'c6k';
  if (f === 'GNW')        return 'cgnw';
  return '';
}
function formBadgeCls(f) {
  if (!f) return '';
  if (f.endsWith('/A')) return 'fbamend';
  if (f.includes('10-K')) return 'fb10k';
  if (f.includes('10-Q')) return 'fb10q';
  if (f.includes('8-K'))  return 'fb8k';
  if (f.includes('20-F')) return 'fb20f';
  if (f.includes('6-K'))  return 'fb6k';
  if (f === 'GNW')        return 'fbgnw';
  return '';
}

function toggleDrawer() {
  document.getElementById('dlDrawer').classList.toggle('open');
}

function loadStats() {
  const base = window._BASE||'';
  fetch('/stats').then(r=>r.json()).then(stats => {
    _allTickers = stats.tickers || {};
    rebuildFormPills(stats.forms || {});
    rebuildTickerList('');
  });
}

function rebuildFormPills(formCounts) {
  const specs = [
    { key:'10-K', label:'10-K', cls:'fp10k' },
    { key:'10-Q', label:'10-Q', cls:'fp10q' },
    { key:'8-K',  label:'8-K',  cls:'fp8k'  },
    { key:'20-F', label:'20-F', cls:'fp20f' },
    { key:'6-K',  label:'6-K',  cls:'fp6k'  },
    { key:'GNW',  label:'GNW',  cls:'fpgnw' },
  ];
  const div = document.getElementById('formPills');
  div.innerHTML = '';
  specs.forEach(({key, label, cls}) => {
    const count = Object.entries(formCounts)
      .filter(([ft]) => ft && ft.includes(key))
      .reduce((s,[,c])=>s+c, 0);
    if (!count) return;
    const pill = document.createElement('button');
    pill.className = 'form-pill ' + cls + (_actForm===key?' active':'');
    pill.innerHTML = label + ' <span style="opacity:.7;font-weight:400">'+count+'</span>';
    pill.onclick = () => { _actForm = _actForm===key?null:key; loadStats(); fetchReports(1); };
    div.appendChild(pill);
  });
}

function rebuildTickerList(filter) {
  const tickers = Object.keys(_allTickers).sort();
  const f = filter.toUpperCase();
  const div = document.getElementById('tickerList');
  div.innerHTML = '';
  tickers.filter(t => !f || t.includes(f)).forEach(t => {
    const item = document.createElement('div');
    item.className = 'ticker-item' + (t===_actTick?' active':'');
    item.innerHTML = `<span>${t}</span><span class="ticker-count">${_allTickers[t]}</span>`;
    item.onclick = () => { _actTick = _actTick===t?null:t; loadStats(); fetchReports(1); };
    div.appendChild(item);
  });
}

function filterTickers(val) { rebuildTickerList(val); }

function fetchReports(page) {
  _page = page || 1;
  const q    = document.getElementById('search').value.trim();
  const base = window._BASE||'';
  const params = new URLSearchParams({ page:_page, per_page:_pageSize, sort:_sortMode });
  if (q)        params.set('q',      q);
  if (_actTick) params.set('ticker', _actTick);
  if (_actForm) params.set('form',   _actForm);
  fetch('/reports?'+params).then(r=>r.json()).then(data => {
    _total = data.total; _pages = data.pages;
    renderCards(data.rows); _renderPager();
  });
}

function setSort(mode) {
  _sortMode = mode;
  document.getElementById('sortFiledBtn').className  = 'sort-btn'+(mode==='filed' ?' active':'');
  document.getElementById('sortTickerBtn').className = 'sort-btn'+(mode==='ticker'?' active':'');
  fetchReports(1);
}

function applyFilters() {
  clearTimeout(_searchTimer);
  _searchTimer = setTimeout(()=>fetchReports(1), 250);
}

function _renderPager() {
  const pager = document.getElementById('reports-pager');
  if (!pager) return;
  pager.classList.toggle('d-none', _total <= _pageSize);
  if (_total === 0) { pager.innerHTML = ''; return; }
  const start = (_page-1)*_pageSize+1;
  const end   = Math.min(_page*_pageSize, _total);
  let html = `<small class="text-muted me-2">${start}–${end} of ${_total}</small>`;
  html += `<ul class="pagination pagination-sm mb-0">`;
  html += `<li class="page-item${_page===1?' disabled':''}"><a class="page-link" href="#" onclick="fetchReports(${_page-1});return false">‹</a></li>`;
  for (const p of _pageRange(_page, _pages)) {
    if (p==='…') { html += `<li class="page-item disabled"><span class="page-link">…</span></li>`; }
    else { html += `<li class="page-item${p===_page?' active':''}"><a class="page-link" href="#" onclick="fetchReports(${p});return false">${p}</a></li>`; }
  }
  html += `<li class="page-item${_page===_pages?' disabled':''}"><a class="page-link" href="#" onclick="fetchReports(${_page+1});return false">›</a></li>`;
  html += `</ul>`;
  pager.innerHTML = html;
}

function _pageRange(current, total) {
  if (total<=7) return Array.from({length:total},(_,i)=>i+1);
  const set    = new Set([1,Math.max(1,current-1),current,Math.min(total,current+1),total]);
  const sorted = [...set].sort((a,b)=>a-b);
  const result = []; let prev=0;
  for (const p of sorted) { if(p-prev>1) result.push('…'); result.push(p); prev=p; }
  return result;
}

function renderCards(rows) {
  const feed  = document.getElementById('feedContainer');
  const empty = document.getElementById('emptyMsg');
  document.getElementById('rowCount').textContent = _total+' report'+(_total!==1?'s':'');
  if (!_total) { feed.innerHTML=''; empty.style.display=''; return; }
  empty.style.display = 'none';
  const base = window._BASE||'';
  feed.innerHTML = rows.map(r => {
    const periodHtml = r.local_path
      ? `<a class="card-period" href="${base}/file/${r.id}" target="_blank">${htmlEsc(r.period)}</a>`
      : `<span class="card-period" style="cursor:default">${htmlEsc(r.period)}</span>`;
    const kgBadge = r.local_path
      ? (r.graphiti_indexed_at
          ? `<span class="badge bg-success act-btn" title="Indexed ${r.graphiti_indexed_at.slice(0,10)}">✓ KG</span>`
          : `<button class="btn btn-outline-primary act-btn idx-btn" title="Index into knowledge graph" onclick="indexReport(${r.id},this)">⬆ KG</button>`)
      : '';
    return `
    <div class="report-card ${cardClass(r.form_type)}" data-id="${r.id}">
      <div class="card-top">
        <div class="card-badge-col">
          <span class="ticker-badge">${htmlEsc(r.ticker)}</span>
          <span class="form-badge ${formBadgeCls(r.form_type)}">${htmlEsc(r.form_type||'—')}</span>
        </div>
        <div class="card-body-col">
          <div class="card-company" title="${htmlEsc(r.company_name||'')}">${htmlEsc(r.company_name||'—')}</div>
          ${periodHtml}
          <div class="card-meta">
            ${r.filed_date?`<span>📅 ${r.filed_date}</span>`:''}
            ${r.file_size?`<span>📄 ${fmtSize(r.file_size)}</span>`:''}
          </div>
        </div>
        <div class="card-actions">
          ${kgBadge}
          <button class="btn btn-outline-danger act-btn" onclick="deleteReport(${r.id},this)">🗑</button>
        </div>
      </div>
      <div id="comment-cell-${r.id}" class="card-comment" style="${r.comment?'':'display:none'}">
        <span class="comment-preview" data-comment="${htmlEsc(r.comment)}" title="Click to preview / edit"></span>
      </div>
    </div>`;
  }).join('');
  if (typeof renderAllCommentCells === 'function') renderAllCommentCells();
}

// ── download ──────────────────────────────────────────────────────────────────
function startDownload() {
  const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!ticker) { alert('Enter a ticker symbol (e.g. AAPL, NVDA, TSLA)'); return; }
  const forms = [];
  if (document.getElementById('chk10K').checked) forms.push('10-K');
  if (document.getElementById('chk10Q').checked) forms.push('10-Q');
  if (document.getElementById('chk8K').checked)  forms.push('8-K');
  if (document.getElementById('chk20F').checked) forms.push('20-F');
  if (document.getElementById('chk6K').checked)  forms.push('6-K');
  if (document.getElementById('chkGNW').checked) forms.push('GNW');
  if (!forms.length) { alert('Select at least one form type.'); return; }
  _startStream('/stream-download', new URLSearchParams({ticker, forms:forms.join(',')}));
}

function startBatchDownload() {
  const last = parseInt(document.getElementById('batchLastN').value)||4;
  const forms = [];
  if (document.getElementById('chk10K').checked) forms.push('10-K');
  if (document.getElementById('chk10Q').checked) forms.push('10-Q');
  if (document.getElementById('chk8K').checked)  forms.push('8-K');
  if (document.getElementById('chk20F').checked) forms.push('20-F');
  if (document.getElementById('chk6K').checked)  forms.push('6-K');
  if (document.getElementById('chkGNW').checked) forms.push('GNW');
  if (!forms.length) { alert('Select at least one form type.'); return; }
  _startStream('/stream-batch-download', new URLSearchParams({forms:forms.join(','), last}));
}

function _startStream(path, params) {
  document.getElementById('progressSection').style.display = '';
  document.getElementById('dlBtn').disabled    = true;
  document.getElementById('batchBtn').disabled = true;
  const bar = document.getElementById('progressBar');
  bar.style.width = '0%';
  bar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  const log = document.getElementById('logBox');
  log.innerHTML = '';
  const base = window._BASE||'';
  const es = new EventSource(path+'?'+params);
  es.onmessage = e => {
    const d = JSON.parse(e.data);
    const line = document.createElement('div');
    line.textContent = d.msg;
    if (d.error) line.style.color='#f48771';
    log.appendChild(line); log.scrollTop=log.scrollHeight;
    if (d.total>0) bar.style.width=Math.round(d.count/d.total*100)+'%';
    if (d.done) {
      es.close();
      document.getElementById('dlBtn').disabled    = false;
      document.getElementById('batchBtn').disabled = false;
      bar.style.width = '100%';
      bar.classList.remove('progress-bar-animated');
      if (!d.error) { bar.classList.remove('bg-primary'); bar.classList.add('bg-success'); }
      loadStats(); fetchReports(1);
    }
  };
  es.onerror = () => {
    const line = document.createElement('div');
    line.textContent = '⚠ Connection lost'; line.style.color='#f48771';
    log.appendChild(line); es.close();
    document.getElementById('dlBtn').disabled    = false;
    document.getElementById('batchBtn').disabled = false;
  };
}

// ── delete ────────────────────────────────────────────────────────────────────
function deleteReport(id) {
  if (!confirm('Remove this report from the library? (The local file will also be deleted.)')) return;
  const base = window._BASE||'';
  fetch('/report/'+id, {method:'DELETE'}).then(r=>{
    if (r.ok) { loadStats(); fetchReports(_page); }
  });
}

function indexReport(id, btn) {
  btn.disabled = true; btn.textContent = '⏳';
  const modal = document.createElement('div');
  modal.style.cssText = 'position:fixed;bottom:1rem;right:1rem;width:420px;max-height:260px;overflow-y:auto;' +
    'background:#1e1e1e;color:#d4d4d4;font:12px/1.5 monospace;padding:.75rem 1rem;border-radius:8px;' +
    'box-shadow:0 4px 20px rgba(0,0,0,.5);z-index:9999';
  document.body.appendChild(modal);
  const base = window._BASE||'';
  modal.textContent = 'Starting…\\n';
  fetch('/index-report/'+id, {method:'POST'})
    .then(async res => {
      const reader = res.body.getReader(); const dec = new TextDecoder(); let buf='';
      while (true) {
        const {value,done} = await reader.read(); if (done) break;
        buf += dec.decode(value, {stream:true});
        const lines = buf.split('\\n'); buf = lines.pop();
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const msg = line.slice(6);
          if (msg.startsWith('__done__:')) {
            const code = parseInt(msg.split(':')[1]);
            if (code===0) {
              btn.textContent='✓ KG'; btn.className='badge bg-success me-1'; btn.onclick=null;
              modal.textContent += 'Syncing graph mirror…\\n'; modal.scrollTop=modal.scrollHeight;
              fetch((window._BASE||'')+'/zep/refresh-mirror',{method:'POST'})
                .then(r=>r.json()).then(d=>{
                  modal.textContent += d.ok?`✓ Mirror synced (${d.entities} entities, ${d.edges} edges)\\n`:`⚠ Mirror sync: ${d.error}\\n`;
                }).catch(e=>{ modal.textContent+=`⚠ Mirror sync failed: ${e.message}\\n`; })
                .finally(()=>{ modal.scrollTop=modal.scrollHeight; setTimeout(()=>modal.remove(),3000); });
            } else { btn.disabled=false; btn.textContent='⬆ KG'; setTimeout(()=>modal.remove(),4000); }
          } else { modal.textContent+=msg+'\\n'; modal.scrollTop=modal.scrollHeight; }
        }
      }
    })
    .catch(e=>{ modal.textContent+='Error: '+e.message; btn.disabled=false; btn.textContent='⬆ KG'; setTimeout(()=>modal.remove(),5000); });
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
