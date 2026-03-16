#!/usr/bin/env python3
"""
eval_ingest_prompt.py — Iterative entity/relation extraction eval on 10-K filings.

Workflow per filing:
  1. Extract core text (Item 1 Business + Item 7 MD&A) from the HTML
  2. Extract entities with the current prompt
  3. Heuristic quality check (pure Python — no extra LLM call)
  4. If quality is poor → ask MiniMax to suggest prompt improvements → retry (up to 2×)
  5. Extract relations with the best entity result
  6. Save everything (all attempts) to a tmp JSON file

Usage:
    python eval_ingest_prompt.py                          # 10 random 10-K filings
    python eval_ingest_prompt.py --n 5                    # 5 filings
    python eval_ingest_prompt.py --ticker NVDA TSMC       # specific tickers
    python eval_ingest_prompt.py --no-iterate             # disable prompt auto-fix
    python eval_ingest_prompt.py --show-prompts           # print full LLM I/O
    python eval_ingest_prompt.py --out /tmp/my.json       # custom output path
"""

import argparse
import json
import random
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR      = Path(__file__).parent
MAX_SECTION     = 12_000   # chars per section (Item 1 / Item 7)
MAX_RETRIES     = 2        # max prompt-refinement retries per filing


# ── Project root ───────────────────────────────────────────────────────────────

def _find_project_root() -> Path:
    p = SCRIPT_DIR.resolve()
    while p != p.parent:
        if (p / ".git").is_dir():
            return p
        p = p.parent
    return SCRIPT_DIR

PROJECT_ROOT    = _find_project_root()
REPORTS_DB_PATH = PROJECT_ROOT / "financial_reports.db"


# ── Improved HTML → text extraction ───────────────────────────────────────────

def _all_section_offsets(text: str) -> dict[str, list[int]]:
    """Return all char offsets for each 10-K section header.

    XBRL 10-K files contain headers twice: once in the Table of Contents
    (short, followed by a page number) and once as the actual body section.
    We store all offsets so callers can pick the last one (body).
    """
    patterns = {
        "item1":  r"(?i)item\s+1[\s\.\n\u2014\-]+\s*business\b",
        "item1a": r"(?i)item\s+1a[\s\.\n\u2014\-]+\s*risk factors\b",
        "item2":  r"(?i)item\s+2[\s\.\n\u2014\-]+\s*properties\b",
        "item3":  r"(?i)item\s+3[\s\.\n\u2014\-]+\s*legal proceedings\b",
        "item7":  r"(?i)item\s+7[\s\.\n\u2014\-]+\s*management",
        "item7a": r"(?i)item\s+7a[\s\.\n\u2014\-]+\s*quantitative",
        "item8":  r"(?i)item\s+8[\s\.\n\u2014\-]+\s*financial statements",
    }
    result: dict[str, list[int]] = {}
    for key, pat in patterns.items():
        result[key] = [m.start() for m in re.finditer(pat, text)]
    return result


def _last(offsets: dict[str, list[int]], key: str,
          full_text: str = "") -> int | None:
    """Return the last offset, optionally filtered to line-start occurrences only.

    Cross-references embedded in sentences (e.g. '"Part I, Item 1. Business" of
    this Annual Report') are NOT at line start, so this filter excludes them.
    """
    lst = offsets.get(key, [])
    if not lst:
        return None
    if full_text:
        line_starts = [o for o in lst
                       if re.search(r"\n\s*$", full_text[max(0, o - 60):o])]
        if line_starts:
            return line_starts[-1]
    return lst[-1]


def _first_after(offsets: dict[str, list[int]], key: str, min_offset: int,
                 full_text: str = "") -> int | None:
    """Return the first offset > min_offset + 500.

    If full_text is supplied, also require that the match is at the start of a
    paragraph (preceded only by whitespace/newlines), so we don't pick up
    in-sentence cross-references like "See Item 1A for details."
    """
    for o in sorted(offsets.get(key, [])):
        if o <= min_offset + 500:
            continue
        if full_text:
            # Check that the character before is a newline / start-of-line
            preceding = full_text[max(0, o - 60):o]
            # Accept only if preceded by a newline (section header on own line)
            if not re.search(r"\n\s*$", preceding):
                continue
        return o
    return None


def extract_10k_core(html_path: Path) -> tuple[str, str]:
    """Extract Item 1 (Business) + Item 1A (Risk Factors) from a 10-K/10-Q HTML filing.

    Sections extracted in priority order:
      1. Item 1 – Business         (primary, most entity-rich)
      2. Item 1A – Risk Factors    (competitors, dependencies, regulatory bodies)

    For Item 1A we use _first_after(item1) rather than _last() to avoid
    picking up back-references to Item 1A that appear inside Item 7 text.

    Returns (text, method) where method is 'sections' or 'full_fallback'.
    """
    from bs4 import BeautifulSoup

    raw  = html_path.read_text(errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    # Strip XBRL metadata + noise
    for tag in soup(["script", "style", "head", "footer", "nav",
                     "ix:header", "ix:hidden", "ix:references", "ix:resources"]):
        tag.decompose()

    # Skip large inline-XBRL data tables (ix:nonfraction / ix:nonnumeric wrap
    # thousands of tagged financial numbers that turn into pure numeric noise).
    for tag in soup.find_all(["ix:nonfraction", "ix:nonnumeric"]):
        tag.unwrap()   # keep the text content, just remove the XBRL wrapper

    # Collapse layout tables (single-cell rows) but drop header/footer tables
    # that are essentially page-number blocks.
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

    if len(full) < 200:
        return "", "empty"

    offs     = _all_section_offsets(full)
    sections: list[str] = []

    # ── Item 1: Business ──────────────────────────────────────────────────────
    # Use the last LINE-START occurrence — filters out in-text cross-references.
    s1 = _last(offs, "item1", full)
    if s1 is not None:
        e1 = (_first_after(offs, "item1a", s1, full)
              or _first_after(offs, "item2", s1, full)
              or s1 + MAX_SECTION * 2)
        chunk = full[s1:e1].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1: BUSINESS ===\n{chunk[:MAX_SECTION]}")

    # ── Item 1A: Risk Factors ─────────────────────────────────────────────────
    # Use FIRST occurrence AFTER Item 1 body (at start-of-line only) to avoid
    # in-text cross-references like "See Item 1A. Risk Factors for details."
    s1a = _first_after(offs, "item1a", s1 or 0, full)
    if s1a is not None:
        e1a = (_first_after(offs, "item2", s1a, full)
               or _first_after(offs, "item3", s1a, full)
               or s1a + MAX_SECTION * 2)
        chunk = full[s1a:e1a].strip()
        # Risk factors sections can be very long — truncate to same limit
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1A: RISK FACTORS ===\n{chunk[:MAX_SECTION]}")

    if sections:
        return "\n\n".join(sections), "sections"

    # Fallback: take the first chunk of stripped text (better than full dump)
    return full[:MAX_SECTION * 2], "full_fallback"


# ── Heuristic quality checker (pure Python, no LLM) ───────────────────────────

# Patterns for obviously forbidden entities

# Person names: only 2-word patterns where BOTH words are short (≤12 chars),
# not ending in corporate suffixes, and not prefixed by a known title.
# This avoids false positives on company names like "Hamilton Sundstrand".
_COMPANY_SUFFIX = re.compile(
    r"\b(Inc\.|Corp\.|Co\.|Ltd\.|LLC|LLP|GmbH|S\.A\.|N\.V\.|PLC|AG|AB|AS|SA|"
    r"Corporation|Company|Group|Holdings|Enterprises|Industries|International|"
    r"Technologies|Systems|Solutions|Services|Limited|Partners)\b",
    re.IGNORECASE,
)
_RE_PERSON = re.compile(
    r"^(Mr\.|Ms\.|Mrs\.|Dr\.|Prof\.)?\s*"
    r"[A-Z][a-z]{1,11}"           # first name: 2–12 chars
    r"(\s+[A-Z]\.)?"              # optional middle initial
    r"\s+[A-Z][a-z]{1,11}"       # last name: 2–12 chars
    r"(\s+(Jr\.|Sr\.|II|III|IV))?$"
)
_RE_LEGAL    = re.compile(r"\bv\.\s+\w|\bIn re\b|\bLitigation\b|\bClass Action\b",
                          re.IGNORECASE)
_RE_SEC_RULE = re.compile(r"\bRule\s+\d|\bRegulation\s+[A-Z]-?\d*\b|\bSection\s+\d+",
                           re.IGNORECASE)
_RE_FORM     = re.compile(r"\bForm\s+\d|\bAnnual Report\b|\bQuarterly Report\b|\b10-[KQ]\b",
                           re.IGNORECASE)
_RE_MONEY    = re.compile(
    r"^\$[\d,.]+|^\d[\d,.]*\s*(million|billion|thousand|%|percent)\b"
    r"|\d+\s+(thousand|million|billion)\s+(active|common|outstanding)",
    re.IGNORECASE,
)
_RE_GENERIC_ACRONYM = re.compile(r"^(AI|VR|AR|XR|ML|IoT|HPC|API|SDK|GPU|CPU|SoC|ASIC|FPGA|ERP|CRM)$")
_BOILERPLATE = frozenset(["IRS", "FASB", "GAAP", "IFRS", "PCAOB", "AICPA",
                           "SEC", "EDGAR"])
_GENERIC_CONCEPTS = re.compile(
    r"\b(fiscal year|depreciation|amortization|amortisation|revenue recognition|"
    r"audit committee|proxy statement|annual meeting|common stock|preferred stock|"
    r"earnings per share|net income|gross margin|"
    r"digital signal processors?|analog integrated circuits?|"
    r"supply chain|semiconductor market|capital market)\b",
    re.IGNORECASE
)

GOOD_TYPES = frozenset(["company", "organisation", "organization", "ticker",
                         "product", "technology", "market", "sector",
                         "industry", "country", "region", "index", "instrument"])

# Entity-type keywords that indicate a non-person (product, company, platform, etc.)
_GOOD_TYPE_KEYWORDS = frozenset([
    "company", "organisation", "organization", "corp", "corporation",
    "product", "technology", "platform", "chip", "device", "hardware",
    "software", "service", "system", "tool", "application", "app",
    "robot", "instrument", "machine", "engine",
    "market", "segment", "sector", "industry", "division",
    "ticker", "index", "fund", "brand", "initiative",
])


def _classify_entity(e: dict) -> str:
    """Return 'good', 'person', 'legal', 'rule', 'form', 'money', 'acronym',
    'boilerplate', or 'concept'."""
    name = e.get("name", "")
    etype = (e.get("entity_type") or "").lower()

    # Monetary values / financial figures (check first — highest confidence)
    if _RE_MONEY.search(name):
        return "money"
    # Generic one-word acronyms (AI, VR, GPU …)
    if _RE_GENERIC_ACRONYM.match(name.strip()):
        return "acronym"
    # Company suffix → definitely good
    if _COMPANY_SUFFIX.search(name):
        return "good"
    # If LLM tagged it as a non-person type → trust it before checking person regex.
    # This avoids false positives on product names like "Apple Watch", "Da Vinci".
    if any(kw in etype for kw in _GOOD_TYPE_KEYWORDS):
        return "good"
    if _RE_PERSON.match(name):
        return "person"
    if _RE_LEGAL.search(name):
        return "legal"
    if _RE_SEC_RULE.search(name):
        return "rule"
    if _RE_FORM.search(name):
        return "form"
    if name.strip() in _BOILERPLATE:
        return "boilerplate"
    if _GENERIC_CONCEPTS.search(name):
        return "concept"
    # Entity type hints for person (low-priority fallback)
    if any(t in etype for t in ("person", "human", "individual", "executive")):
        return "person"
    return "good"


def heuristic_check(entities: list[dict]) -> dict:
    """Classify each entity and return a quality summary dict."""
    classified: dict[str, list[str]] = {
        "good": [], "person": [], "legal": [], "rule": [],
        "form": [], "money": [], "acronym": [], "boilerplate": [], "concept": [],
    }
    for e in entities:
        cat = _classify_entity(e)
        classified[cat].append(e["name"])

    n_total    = len(entities)
    n_bad      = sum(len(classified[k]) for k in ("person", "legal", "rule",
                                                    "form", "money", "acronym",
                                                    "boilerplate", "concept"))
    bad_ratio  = n_bad / n_total if n_total > 0 else 0.0
    too_few    = len(classified["good"]) < 3

    issues: list[str] = []
    if classified["person"]:
        issues.append(f"person names extracted: {', '.join(classified['person'][:5])}")
    if classified["legal"]:
        issues.append(f"legal cases extracted: {', '.join(classified['legal'][:5])}")
    if classified["rule"]:
        issues.append(f"SEC rules extracted: {', '.join(classified['rule'][:5])}")
    if classified["form"]:
        issues.append(f"form types extracted: {', '.join(classified['form'][:5])}")
    if classified["money"]:
        issues.append(f"monetary values as entities: {', '.join(classified['money'][:5])}")
    if classified["acronym"]:
        issues.append(f"generic acronyms as entities: {', '.join(classified['acronym'][:5])}")
    if classified["boilerplate"]:
        issues.append(f"boilerplate entities: {', '.join(classified['boilerplate'][:5])}")
    if classified["concept"]:
        issues.append(f"generic concepts: {', '.join(classified['concept'][:5])}")
    if too_few:
        issues.append(f"too few meaningful entities ({len(classified['good'])} good)")

    quality_ok = bad_ratio < 0.20 and not too_few
    # Note: edge count is checked separately in the main loop

    return {
        "quality_ok":   quality_ok,
        "n_total":      n_total,
        "n_good":       len(classified["good"]),
        "n_bad":        n_bad,
        "bad_ratio":    round(bad_ratio, 2),
        "classified":   classified,
        "issues":       issues,
    }


# ── LLM helpers ───────────────────────────────────────────────────────────────

def _minimax(messages: list[dict], label: str, show_prompts: bool,
             max_tokens: int = 4096) -> str:
    from minimax import call_minimax, MINIMAX_API_KEY  # noqa

    if show_prompts:
        print(f"\n{'='*60}\n[PROMPT] {label}")
        for m in messages:
            body = m["content"]
            print(f"  [{m['role'].upper()}] {body[:2500]}{'…' if len(body) > 2500 else ''}")
        print(f"{'─'*60}")

    t0 = time.monotonic()
    text, _, _ = call_minimax(
        messages=messages, temperature=0.1,
        max_completion_tokens=max_tokens, api_key=MINIMAX_API_KEY,
    )
    elapsed = time.monotonic() - t0
    print(f"    · {label}: done ({elapsed:.1f}s)", flush=True)

    if show_prompts:
        print(f"  [RESPONSE] {text[:1200]}{'…' if len(text) > 1200 else ''}")
        print(f"{'='*60}\n")
    return text


def _parse_json(text: str) -> dict | list | None:
    text = re.sub(r"```(?:json)?\s*\n?", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE).strip()
    for sc, ec in [('{', '}'), ('[', ']')]:
        start = text.find(sc)
        if start == -1:
            continue
        depth = 0
        for i, c in enumerate(text[start:], start):
            if c == sc:
                depth += 1
            elif c == ec:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        return None
    return None


# ── Prompt building ────────────────────────────────────────────────────────────

_BASE_ENTITY_RULES = """\
STRICT ENTITY EXTRACTION RULES:

Entities must represent a real company, a specific branded product/technology,
or a clearly named business market. Nothing else.

ALLOWED (extract ONLY these):
- Companies and organisations (e.g. NVIDIA, TSMC, AMD, Microsoft, SoftBank, Arm)
- Stock tickers (e.g. NVDA, TSM, AAPL, AMD)
- Named products, chips, platforms, or proprietary technologies
  (e.g. H100, Blackwell, Hopper, CUDA, NVLink, CoWoS, Grace CPU, GeForce, Quadro)
  Must be a specific BRANDED or MODEL name — NOT a generic technology category.
  BAD examples (too generic): "Digital Signal Processors", "Analog ICs", "GPU", "AI", "VR", "HPC"
- Named business segments the company itself uses to describe its divisions
  (e.g. Data Center, Gaming, Automotive, Professional Visualization, Networking)

FORBIDDEN (NEVER extract — skip entirely):
- ANY monetary value or financial figure: $79 million, $5.2 billion, $1.0 billion, 13 thousand,
  any string that starts with "$", any string that contains a number + million/billion/trillion.
  If the entity name contains a dollar sign OR a numeric amount, DO NOT extract it.
- Generic technology acronyms not tied to a specific product: AI, VR, AR, GPU, HPC, IoT, ML
- Generic technology categories: "Digital Signal Processors", "Analog Integrated Circuits",
  "Semiconductor Market", "Cloud Computing" — too broad, not a company or product
- Countries, regions, or geographies (China, United States, Europe, Taiwan)
- Financial indices, benchmarks, or ratings (S&P 500, NASDAQ, Moody's)
- Generic financial instruments (convertible notes, bonds, equity, common stock)
- Human personal names (executives, analysts, lawyers, investors)
- Legal cases: anything with "v.", "In re", "Derivative Litigation", "Class Action"
- SEC rules and rule numbers (Rule 10b-5, Regulation S-K, etc.)
- SEC filing form types (Form 10-K, Form 10-Q, Annual Report, etc.)
- Regulatory/accounting boilerplate: IRS, FASB, GAAP, IFRS, PCAOB, SEC as generic ref
- Laws and acts (Securities Exchange Act, Sarbanes-Oxley, Dodd-Frank)
- Generic legal/accounting concepts (fiscal year, audit, depreciation, amortization)
- Generic time periods (Q1, Q2, fiscal 2024)
- Vague concepts (supply chain, demand, growth, risk, strategy, innovation)

If in doubt, skip the entity. Quality over quantity."""

_EDGE_RULES = """\
RELATIONSHIP EXTRACTION RULES:
1. CRITICAL — use entity names EXACTLY as they appear in the entity list.
2. EXTRACT AGGRESSIVELY — you MUST extract AT LEAST 2 relationships. Never return empty.
3. Start with the most obvious relationships first:
   - What does the company MAKE or SELL? (product/segment → company)
   - Who are the company's competitors? (company COMPETES_WITH company)
   - Who supplies or partners with the company?
4. PRIORITISED types:
   - Product/chip/platform MADE_BY or SOLD_BY company  (e.g. H100 → NVIDIA)
   - Business segment OPERATED_BY company               (e.g. Data Center → NVIDIA)
   - Company COMPETES_WITH company                      (e.g. NVIDIA → AMD)
   - Company SUPPLIES or MANUFACTURES_FOR company       (e.g. TSMC → NVIDIA)
   - Company HAS_REVENUE_FROM segment/market
   - Ticker REPRESENTS company                          (e.g. NVDA → NVIDIA)
   - Company ACQUIRED or INVESTED_IN company
   - Company PARTNERS_WITH or JOINT_VENTURE_WITH company
   - Company IS_SUBSIDIARY_OF or SPUN_OFF_FROM company
5. relation_type: short ALL_CAPS verb phrase (MADE_BY, COMPETES_WITH, IS_SUBSIDIARY_OF …)."""

_ENTITY_SCHEMA = json.dumps({
    "extracted_entities": [
        {"name": "string", "entity_type": "string", "summary": "string (one sentence)"}
    ]
})
_EDGE_SCHEMA = json.dumps({
    "edges": [
        {"source_entity_name": "string", "target_entity_name": "string",
         "relation_type": "string", "fact": "string (one sentence)"}
    ]
})


def _entity_system(ticker: str, company: str, extra_rules: str = "") -> str:
    rules = _BASE_ENTITY_RULES
    if extra_rules:
        rules += f"\n\nADDITIONAL RULES (added after reviewing previous extraction):\n{extra_rules}"
    return (
        f"You extract named entities from a {company} ({ticker}) 10-K SEC filing.\n\n"
        f"IMPORTANT: Always include '{company}' and the ticker '{ticker}' as entities — "
        f"they are the primary subjects of this filing.\n\n"
        f"{rules}\n\n"
        f"Reply with ONLY valid JSON matching this schema:\n{_ENTITY_SCHEMA}"
    )


# ── Extraction functions ───────────────────────────────────────────────────────

def extract_entities(text: str, ticker: str, company: str,
                     extra_rules: str, show_prompts: bool) -> list[dict]:
    raw = _minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI",
             "content": _entity_system(ticker, company, extra_rules)},
            {"role": "user", "name": "User",
             "content": f"Extract all entities from this 10-K excerpt:\n\n{text}"},
        ],
        label="ExtractEntities",
        show_prompts=show_prompts,
    )
    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        entities = parsed.get("extracted_entities") or []
    elif isinstance(parsed, list):
        entities = parsed
    else:
        print(f"    ⚠  Could not parse entity JSON: {raw[:200]}")
        entities = []
    return [e for e in entities if isinstance(e, dict) and e.get("name")]


def refine_prompt(issues: list[str], bad_entities: dict[str, list[str]],
                  show_prompts: bool) -> str:
    """Ask MiniMax to generate extra FORBIDDEN rules based on the detected issues."""
    bad_summary = "\n".join(
        f"- {cat}: {', '.join(names[:8])}"
        for cat, names in bad_entities.items()
        if names and cat != "good"
    )
    raw = _minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": (
                "You are a prompt engineer improving an entity extraction system for financial analysis.\n"
                "You will be given a list of incorrectly extracted entities and their categories.\n"
                "Write 3–6 concise additional FORBIDDEN rules to add to the extraction prompt "
                "that would prevent these specific bad extractions.\n"
                "Return ONLY the additional rules as plain text bullet points (no JSON, no explanation)."
            )},
            {"role": "user", "name": "User", "content": (
                f"Issues detected:\n{chr(10).join(issues)}\n\n"
                f"Bad entities extracted:\n{bad_summary}\n\n"
                "Write additional FORBIDDEN rules to prevent these."
            )},
        ],
        label="RefinePrompt",
        show_prompts=show_prompts,
        max_tokens=512,
    )
    return raw.strip()


def extract_edges(text: str, entities: list[dict], show_prompts: bool) -> list[dict]:
    if not entities:
        return []
    entity_list = "\n".join(
        f"- {e['name']} ({e.get('entity_type', '')})" for e in entities
    )
    raw = _minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": (
                f"You extract relationships from a 10-K SEC filing.\n\n"
                f"{_EDGE_RULES}\n\n"
                f"ENTITIES (use names EXACTLY as written):\n{entity_list}\n\n"
                f"Reply with ONLY valid JSON:\n{_EDGE_SCHEMA}"
            )},
            {"role": "user", "name": "User",
             "content": f"Extract all relationships from this 10-K excerpt:\n\n{text}"},
        ],
        label="ExtractEdges",
        show_prompts=show_prompts,
    )
    parsed = _parse_json(raw)
    if isinstance(parsed, dict):
        edges = parsed.get("edges") or []
    elif isinstance(parsed, list):
        edges = parsed
    else:
        print(f"    ⚠  Could not parse edge JSON: {raw[:200]}")
        edges = []

    valid_names = {e["name"] for e in entities}
    # Case-insensitive fallback: maps lower(name) → canonical name
    _lower_map = {n.lower(): n for n in valid_names}

    def _resolve(raw: str) -> str | None:
        """Return canonical entity name or None if not found."""
        if raw in valid_names:
            return raw
        return _lower_map.get(raw.lower())

    good, bad = [], []
    for ed in (edges if isinstance(edges, list) else []):
        if not isinstance(ed, dict):
            continue
        src = _resolve(ed.get("source_entity_name", ""))
        tgt = _resolve(ed.get("target_entity_name", ""))
        if src and tgt:
            ed["source_entity_name"] = src
            ed["target_entity_name"] = tgt
            good.append(ed)
        else:
            bad.append(ed)
    if bad:
        print(f"    ⚠  {len(bad)} edge(s) dropped (name mismatch): "
              + ", ".join(
                  f"{e.get('source_entity_name')}→{e.get('target_entity_name')}"
                  for e in bad[:4]))
    return good


# ── DB helpers ─────────────────────────────────────────────────────────────────

def sample_reports(n: int, tickers: list[str]) -> list[dict]:
    if not REPORTS_DB_PATH.exists():
        print(f"ERROR: {REPORTS_DB_PATH} not found", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(REPORTS_DB_PATH)
    conn.row_factory = sqlite3.Row
    where  = "form_type = '10-K' AND local_path IS NOT NULL"
    params: list = []
    if tickers:
        where += f" AND ticker IN ({','.join('?' * len(tickers))})"
        params.extend(tickers)
    rows = conn.execute(
        f"SELECT id, ticker, company_name, period, local_path, filed_date "
        f"FROM reports WHERE {where}",
        params,
    ).fetchall()
    conn.close()
    rows = [dict(r) for r in rows]
    random.shuffle(rows)
    return rows[:n]


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Eval + iterative prompt improvement for 10-K entity extraction."
    )
    parser.add_argument("--n",           type=int, default=10,
                        help="Number of random 10-K filings to sample (default: 10)")
    parser.add_argument("--ticker",      nargs="+", default=[],
                        metavar="TICKER", help="Restrict to these ticker(s)")
    parser.add_argument("--no-iterate",  action="store_true",
                        help="Disable automatic prompt refinement on bad results")
    parser.add_argument("--show-prompts", action="store_true",
                        help="Print full LLM input/output to stdout")
    parser.add_argument("--out",         default="",
                        help="Output JSON path (default: /tmp/eval_ingest_<ts>.json)")
    args = parser.parse_args()

    out_path = Path(args.out) if args.out else Path(
        f"/tmp/eval_ingest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    print(f"Sampling {args.n} 10-K filing(s)"
          + (f" for {', '.join(args.ticker)}" if args.ticker else "")
          + " …")
    rows = sample_reports(args.n, args.ticker)
    if not rows:
        print("No matching reports found.")
        sys.exit(0)
    print(f"Found {len(rows)} filing(s). Processing…\n")

    results      = []
    all_bad_cats: dict[str, list[str]] = {}  # accumulate bad entities across filings

    for i, row in enumerate(rows, 1):
        ticker  = row["ticker"]
        company = row["company_name"] or ticker
        period  = row["period"]
        path    = Path(row["local_path"])

        print(f"[{i}/{len(rows)}] {ticker} 10-K {period}")
        print(f"  file: {path}")

        # 1. Extract text
        if not path.exists():
            print("  ⚠  File not found, skipping.\n")
            continue
        try:
            text, method = extract_10k_core(path)
        except Exception as e:
            print(f"  ⚠  Extraction error: {e}\n")
            continue
        if not text:
            print("  ⚠  No text extracted, skipping.\n")
            continue
        print(f"  {len(text):,} chars via '{method}'")

        attempts: list[dict] = []
        extra_rules = ""
        final_entities: list[dict] = []
        final_quality:  dict       = {}

        # 2. Entity extraction with optional iterative refinement
        for attempt in range(1, MAX_RETRIES + 2):  # up to 3 attempts
            print(f"  [attempt {attempt}] extracting entities…", flush=True)
            try:
                entities = extract_entities(text, ticker, company,
                                            extra_rules, args.show_prompts)
            except Exception as e:
                print(f"  ⚠  Entity extraction error: {e}")
                entities = []

            quality = heuristic_check(entities)
            good_names = quality["classified"]["good"]

            status = "✓ OK" if quality["quality_ok"] else "✗ issues"
            print(f"  {status}  {quality['n_good']} good / {quality['n_bad']} bad "
                  f"(ratio {quality['bad_ratio']:.0%})")
            if quality["issues"]:
                for iss in quality["issues"]:
                    print(f"    • {iss}")

            attempts.append({
                "attempt":     attempt,
                "extra_rules": extra_rules,
                "entities":    entities,
                "quality":     quality,
            })

            final_entities = entities
            final_quality  = quality

            # Stop if good or no more retries or --no-iterate
            if quality["quality_ok"] or args.no_iterate or attempt > MAX_RETRIES:
                break

            # 3. Prompt refinement: ask MiniMax to improve the rules
            bad_cats = {k: v for k, v in quality["classified"].items()
                        if k != "good" and v}
            # Accumulate for final summary
            for k, v in bad_cats.items():
                all_bad_cats.setdefault(k, []).extend(v)

            print(f"  → Refining prompt (attempt {attempt} had issues)…")
            try:
                extra_rules = refine_prompt(quality["issues"], bad_cats,
                                            args.show_prompts)
                print(f"  Refined rules:\n    "
                      + extra_rules.replace("\n", "\n    ")[:400])
            except Exception as e:
                print(f"  ⚠  Prompt refinement failed: {e}")
                break

        # 4. Print final entity list
        good_names = final_quality.get("classified", {}).get("good", [])
        print(f"  → Final entities ({len(final_entities)}): "
              + ", ".join(good_names[:12])
              + ("…" if len(good_names) > 12 else ""))

        # 5. Extract edges from the best entity set
        print(f"  extracting edges…", flush=True)
        try:
            edges = extract_edges(text, final_entities, args.show_prompts)
        except Exception as e:
            print(f"  ⚠  Edge extraction error: {e}")
            edges = []
        print(f"  → {len(edges)} relationships: "
              + ", ".join(
                  f"{e['source_entity_name']}→{e['target_entity_name']}"
                  for e in edges[:6])
              + ("…" if len(edges) > 6 else ""))
        print()

        results.append({
            "ticker":        ticker,
            "company":       company,
            "period":        period,
            "filed_date":    row.get("filed_date", ""),
            "file_path":     str(path),
            "text_method":   method,
            "text_length":   len(text),
            "text_preview":  text[:600],
            "attempts":      attempts,
            "final_entities": final_entities,
            "final_quality":  final_quality,
            "edges":         edges,
        })

    # ── Summary ───────────────────────────────────────────────────────────────
    if results:
        total_e  = sum(len(r["final_entities"]) for r in results)
        total_ed = sum(len(r["edges"]) for r in results)
        n_good   = sum(r["final_quality"].get("n_good", 0) for r in results)
        n_bad    = sum(r["final_quality"].get("n_bad",  0) for r in results)

        print("=" * 60)
        print(f"Summary over {len(results)} filings:")
        print(f"  Total entities     : {total_e}  ({total_e/len(results):.1f} avg)")
        print(f"  Good entities      : {n_good}  ({n_good/len(results):.1f} avg)")
        print(f"  Bad/noise entities : {n_bad}  ({n_bad/len(results):.1f} avg)")
        print(f"  Edges              : {total_ed}  ({total_ed/len(results):.1f} avg)")

        n_multi = sum(1 for r in results if len(r["attempts"]) > 1)
        if n_multi:
            print(f"  Prompt refinements : {n_multi} filing(s) needed extra iterations")

        if all_bad_cats:
            print("\nMost common noise categories (across all filings):")
            for cat, names in all_bad_cats.items():
                uniq = list(dict.fromkeys(names))[:8]
                print(f"  {cat}: {', '.join(uniq)}")

    # ── Write output ──────────────────────────────────────────────────────────
    out_path.write_text(
        json.dumps({
            "generated_at": datetime.now().isoformat(),
            "n_sampled":    len(rows),
            "n_processed":  len(results),
            "results":      results,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
