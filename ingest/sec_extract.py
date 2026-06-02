"""
ingest/sec_extract.py — Deterministic SEC HTML / PDF text-extraction helpers.

Pure regex + pdfplumber/pymupdf primitives. No LLM. No graph DB. No network.

Public surface (kept compatible with the previous module's importers):

  - extract_text(pdf_path, max_chars=80_000)
  - extract_html_text(html_path, form_type="10-K", max_chars=80_000)
  - _clean_html_to_text(html_path)              # internal but reused by skills
  - _sec_offsets, _last_offset, _first_after_offset   # internal helpers
  - _10K_PATTERNS, _10Q_PATTERNS, _8K_PATTERNS        # regex tables

These functions were originally part of `ingest/graphiti_ingest.py`. They were
extracted into this standalone module when the LLM-driven ingest pipeline was
deleted (2026-06-02) so the deterministic helpers could keep working for the
SEC-report-summary skill and any other consumer.
"""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

try:
    import fitz as _fitz_available  # pymupdf — optional but preferred
except ImportError:
    _fitz_available = None  # type: ignore[assignment]

MAX_CHARS = 80_000


# ── PDF extraction ────────────────────────────────────────────────────────────

def _extract_text_pdfplumber(pdf_path: Path, max_chars: int) -> str:
    """Fallback PDF extraction using pdfplumber (no heading detection)."""
    try:
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text.strip())
        full = "\n\n".join(pages)
        return full[:max_chars] if len(full) >= 200 else ""
    except Exception:
        return ""


def extract_text(pdf_path: Path, max_chars: int = MAX_CHARS) -> str:
    """Extract text from a PDF with heading detection via pymupdf (fitz).

    Detects headings from font size relative to body text, marks them with
    ``#`` / ``##`` markers, skips table-of-contents pages, and falls back to
    pdfplumber when fitz is unavailable or extracts too little.
    """
    if _fitz_available is None:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    import fitz
    from collections import Counter

    try:
        doc = fitz.open(str(pdf_path))
    except Exception:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    if not doc.page_count:
        doc.close()
        return _extract_text_pdfplumber(pdf_path, max_chars)

    BOLD_FLAG = 1 << 4

    all_sizes: list[float] = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    if len(span["text"].strip()) > 10:
                        all_sizes.append(round(span["size"], 1))

    if not all_sizes:
        doc.close()
        return _extract_text_pdfplumber(pdf_path, max_chars)

    body_size: float = Counter(all_sizes).most_common(1)[0][0]
    h1_min = body_size * 1.4
    h2_min = body_size * 1.2

    toc_line_re = re.compile(r"[.…]{2,}\s*\d+\s*$|\s{4,}\d{1,3}\s*$")

    lines_out: list[str] = []
    for page in doc:
        page_lines: list[tuple[str, float, bool]] = []
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                if not line["spans"]:
                    continue
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text:
                    continue
                max_size = max(s["size"] for s in line["spans"])
                is_bold  = any(s["flags"] & BOLD_FLAG for s in line["spans"])
                page_lines.append((text, max_size, is_bold))

        if not page_lines:
            continue

        toc_count = sum(1 for t, _, _ in page_lines if toc_line_re.search(t))
        if len(page_lines) > 5 and toc_count / len(page_lines) > 0.35:
            continue

        for text, size, bold in page_lines:
            if len(text) <= 4 and text.strip().isdigit():
                continue
            if size >= h1_min:
                lines_out.append(f"\n# {text}")
            elif size >= h2_min:
                lines_out.append(f"\n## {text}")
            else:
                lines_out.append(text)

    doc.close()

    full = "\n".join(lines_out)
    full = _clean_pdf_text(full)

    if len(full) < 200:
        return _extract_text_pdfplumber(pdf_path, max_chars)

    return full[:max_chars]


def _clean_pdf_text(text: str) -> str:
    """Strip common research-PDF artefacts that waste downstream tokens."""
    import re as _re

    text = _re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = _re.sub(r"([a-z]{1,4})\n([a-z]{1,4}(?=\s|$))", r"\1\2", text)

    _month = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2}"
    _noise_pat = (
        r"^\s*(?:"
        r"\(?\d[\d\s\-\+\(\)]{6,}\d"
        r"|[\w.\-]+@[\w.\-]+\.[a-z]{2,}"
        r"|[\d\s\.\,\|\-\+\=\*\/\\]{4,}"
        r"|J\.P\.\s*Morgan\s+\w.*"
        r"|(?:-?\d{1,3}%\s+){3,}.*"
        r"|Source\s*:.{0,120}"
        r"|Rebased\s+to\s+\d+.*"
        r"|See\s+page\s+\d+\s+for\s+analyst.*"
        r"|factor\s+in\s+making\s+their\s+investment\s+decision.*"
        r")\s*$"
    )
    _noise = _re.compile(_noise_pat, _re.IGNORECASE)
    _date_axis = _re.compile(r"^\s*(?:" + _month + r"\s+){3,}", _re.IGNORECASE)
    lines = [
        ln for ln in text.splitlines()
        if not _noise.match(ln.lstrip("#").lstrip()) and not _date_axis.match(ln)
    ]
    text = "\n".join(lines)

    text = _re.sub(r"\n{3,}", "\n\n", text)

    _disclaimer = _re.compile(
        r"(?:^|\n)#{0,3}\s*(?:"
        r"Analyst Certif"
        r"|Important Disclos"
        r"|Required Disclos"
        r"|Legal (?:and |& )?Regulatory"
        r"|IMPORTANT REGULATORY"
        r"|Global Disclaimer"
        r"|(?:Disclosures|Disclaimer)\s*(?:\n|$)"
        r")",
        _re.IGNORECASE,
    )
    m = _disclaimer.search(text)
    if m and m.start() > len(text) * 0.25:
        text = text[: m.start()].rstrip()

    return text.strip()


# ── SEC section patterns ──────────────────────────────────────────────────────

# Separator between "Item N" and the section title.
_SEP = r"[\s\.\|\n—\-]+"

_10K_PATTERNS = {
    "item1":  rf"(?i)item\s+1{_SEP}\s*business\b",
    "item1a": rf"(?i)item\s+1a{_SEP}\s*risk factors\b",
    "item2":  rf"(?i)item\s+2{_SEP}\s*properties\b",
    "item3":  rf"(?i)item\s+3{_SEP}\s*legal proceedings\b",
    "item7":  rf"(?i)item\s+7{_SEP}\s*management",
    "item7a": rf"(?i)item\s+7a{_SEP}\s*quantitative",
    "item8":  rf"(?i)item\s+8{_SEP}\s*financial statements",
}

_10Q_PATTERNS = {
    "item1_fs":  rf"(?i)item\s+1{_SEP}\s*financial statements\b",
    "item2_mda": rf"(?i)item\s+2{_SEP}\s*management.{{0,30}}discussion\b",
    "item3_mkt": rf"(?i)item\s+3{_SEP}\s*quantitative",
    "item4":     rf"(?i)item\s+4{_SEP}\s*controls",
    "item1a":    rf"(?i)item\s+1a{_SEP}\s*risk factors\b",
}

# Excluded: 5.02 (officer changes — HR noise), 7.01 (Reg FD — boundary only).
_8K_PATTERNS = {
    "item1_01": r"(?i)item\s+1\.01\b",
    "item2_01": r"(?i)item\s+2\.01\b",
    "item2_02": r"(?i)item\s+2\.02\b",
    "item5_02": r"(?i)item\s+5\.02\b",
    "item7_01": r"(?i)item\s+7\.01\b",
    "item8_01": r"(?i)item\s+8\.01\b",
    "item9_01": r"(?i)item\s+9\.01\b",
}

_MAX_SECTION = 12_000


def _sec_offsets(text: str, patterns: dict) -> dict[str, list[int]]:
    return {k: [m.start() for m in re.finditer(p, text)]
            for k, p in patterns.items()}


def _last_offset(offsets: dict, key: str, full_text: str = "") -> int | None:
    lst = offsets.get(key, [])
    if not lst:
        return None
    if full_text:
        line_starts = [o for o in lst
                       if re.search(r"\n\s*$", full_text[max(0, o - 60):o])]
        if line_starts:
            return line_starts[-1]
    return lst[-1]


def _first_after_offset(offsets: dict, key: str, min_pos: int,
                        full_text: str = "") -> int | None:
    for o in sorted(offsets.get(key, [])):
        if o <= min_pos + 500:
            continue
        if full_text:
            preceding = full_text[max(0, o - 60):o]
            if not re.search(r"\n\s*$", preceding):
                continue
        return o
    return None


# ── HTML extraction ───────────────────────────────────────────────────────────

def _clean_html_to_text(html_path: Path) -> str:
    """Parse HTML, strip boilerplate tags, flatten tables, return clean plain text."""
    from bs4 import BeautifulSoup
    html = html_path.read_text(errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "head", "footer", "nav",
                     "ix:header", "ix:hidden", "ix:references", "ix:resources"]):
        tag.decompose()
    for tag in soup.find_all(["ix:nonfraction", "ix:nonnumeric"]):
        tag.unwrap()

    for table in soup.find_all("table"):
        rows_text = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                rows_text.append(" | ".join(cells))
        if rows_text:
            table.replace_with("\n" + "\n".join(rows_text) + "\n")

    full = soup.get_text(separator="\n")
    full = re.sub(r"[ \t]{2,}", " ", full)
    full = re.sub(r"\n{3,}", "\n\n", full).strip()
    return full


def _extract_10k_sections(full: str) -> list[str]:
    offs = _sec_offsets(full, _10K_PATTERNS)
    sections: list[str] = []

    s1 = _last_offset(offs, "item1", full)
    if s1 is not None:
        e1 = (_first_after_offset(offs, "item1a", s1, full)
              or _first_after_offset(offs, "item2", s1, full)
              or s1 + _MAX_SECTION * 2)
        chunk = full[s1:e1].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1: BUSINESS ===\n{chunk[:_MAX_SECTION]}")

    s1a = _first_after_offset(offs, "item1a", s1 or 0, full)
    if s1a is not None:
        e1a = (_first_after_offset(offs, "item2",  s1a, full)
               or _first_after_offset(offs, "item3",  s1a, full)
               or _first_after_offset(offs, "item7",  s1a, full)
               or _first_after_offset(offs, "item7a", s1a, full)
               or _first_after_offset(offs, "item8",  s1a, full)
               or s1a + _MAX_SECTION * 2)
        chunk = full[s1a:e1a].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1A: RISK FACTORS ===\n{chunk[:_MAX_SECTION]}")

    return sections


def _extract_10q_sections(full: str) -> list[str]:
    offs = _sec_offsets(full, _10Q_PATTERNS)
    sections: list[str] = []

    s_mda = _last_offset(offs, "item2_mda", full)
    if s_mda is not None:
        e_mda = (_first_after_offset(offs, "item3_mkt", s_mda, full)
                 or _first_after_offset(offs, "item4", s_mda, full)
                 or s_mda + _MAX_SECTION * 2)
        chunk = full[s_mda:e_mda].strip()
        chunk = re.sub(
            r"CAUTIONARY STATEMENT[^\n]*\n[\s\S]*?"
            r"(?=\n[A-Z][A-Z][A-Z\s\-]+(?:\n|$))",
            "",
            chunk,
            flags=re.IGNORECASE,
        ).strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 2: MD&A ===\n{chunk[:_MAX_SECTION]}")

    s_rf = _first_after_offset(offs, "item1a", s_mda or 0, full)
    if s_rf is not None:
        chunk = full[s_rf:s_rf + _MAX_SECTION].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1A: RISK FACTORS (UPDATE) ===\n{chunk[:_MAX_SECTION]}")

    return sections


def _extract_8k_sections(full: str) -> list[str]:
    offs = _sec_offsets(full, _8K_PATTERNS)

    item_labels = {
        "item1_01": "ITEM 1.01: MATERIAL AGREEMENT",
        "item2_01": "ITEM 2.01: COMPLETION OF ACQUISITION",
        "item2_02": "ITEM 2.02: RESULTS OF OPERATIONS",
        "item5_02": None,
        "item7_01": None,
        "item8_01": "ITEM 8.01: OTHER EVENTS",
    }

    found: list[tuple[int, str, str | None]] = []
    for key, label in item_labels.items():
        pos = _last_offset(offs, key, full)
        if pos is not None:
            found.append((pos, key, label))
    found.sort(key=lambda x: x[0])

    exhibits_end = _last_offset(offs, "item9_01", full) or len(full)

    sections: list[str] = []
    for i, (start, key, label) in enumerate(found):
        if label is None:
            continue
        end = found[i + 1][0] if i + 1 < len(found) else exhibits_end
        chunk = full[start:end].strip()
        if len(chunk) > 100:
            sections.append(f"=== {label} ===\n{chunk[:_MAX_SECTION]}")

    return sections


def extract_html_text(html_path: Path, form_type: str = "10-K",
                      max_chars: int = MAX_CHARS) -> str:
    """Extract the most informative narrative sections from an SEC HTML filing.

    Dispatches to form-type-specific extractors:
      10-K  → Item 1 (Business) + Item 1A (Risk Factors)
      10-Q  → Item 2 (MD&A) + Item 1A Part II (Risk Factors update)
      8-K   → all substantive items (1.01, 2.02, 8.01, …)
    Falls back to a raw text dump if no sections are detected.
    """
    full = _clean_html_to_text(html_path)
    if len(full) < 200:
        return ""

    ft = (form_type or "").upper()
    if ft in ("10-K", "10-K/A"):
        sections = _extract_10k_sections(full)
    elif ft in ("10-Q", "10-Q/A"):
        sections = _extract_10q_sections(full)
    elif ft in ("8-K", "8-K/A"):
        sections = _extract_8k_sections(full)
    else:
        sections = _extract_10k_sections(full) or _extract_10q_sections(full)

    if sections:
        return "\n\n".join(sections)

    return full[:max_chars]
