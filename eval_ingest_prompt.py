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
MAX_SECTION     = 18_000   # chars per section (~4-5k tokens each)
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
        "item7":  r"(?i)item\s+7[\s\.\n\u2014\-]+\s*management",
        "item7a": r"(?i)item\s+7a[\s\.\n\u2014\-]+\s*quantitative",
        "item8":  r"(?i)item\s+8[\s\.\n\u2014\-]+\s*financial statements",
    }
    result: dict[str, list[int]] = {}
    for key, pat in patterns.items():
        result[key] = [m.start() for m in re.finditer(pat, text)]
    return result


def _last(offsets: dict[str, list[int]], key: str) -> int | None:
    lst = offsets.get(key, [])
    return lst[-1] if lst else None


def _first_after(offsets: dict[str, list[int]], key: str, min_offset: int) -> int | None:
    for o in sorted(offsets.get(key, [])):
        if o > min_offset + 500:
            return o
    return None


def extract_10k_core(html_path: Path) -> tuple[str, str]:
    """Extract Item 1 (Business) + Item 7 (MD&A) from a 10-K HTML filing.

    Returns (text, method) where method is 'sections' or 'full_fallback'.
    """
    from bs4 import BeautifulSoup

    raw  = html_path.read_text(errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    # Strip XBRL metadata + noise
    for tag in soup(["script", "style", "head", "footer", "nav",
                     "ix:header", "ix:hidden", "ix:references", "ix:resources"]):
        tag.decompose()

    # Flatten tables → pipe-delimited rows (preserves financial figures)
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                rows.append(" | ".join(cells))
        if rows:
            table.replace_with("\n" + "\n".join(rows) + "\n")

    full = soup.get_text(separator="\n")
    full = re.sub(r"[ \t]{2,}", " ", full)
    full = re.sub(r"\n{3,}", "\n\n", full).strip()

    if len(full) < 200:
        return "", "empty"

    offs     = _all_section_offsets(full)
    sections: list[str] = []

    # Item 1: Business
    s1 = _last(offs, "item1")
    if s1 is not None:
        e1 = (_first_after(offs, "item1a", s1)
              or _first_after(offs, "item2", s1)
              or s1 + MAX_SECTION * 2)
        chunk = full[s1:e1].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 1: BUSINESS ===\n{chunk[:MAX_SECTION]}")

    # Item 7: MD&A
    s7 = _last(offs, "item7")
    if s7 is not None:
        e7 = (_first_after(offs, "item7a", s7)
              or _first_after(offs, "item8", s7)
              or s7 + MAX_SECTION * 2)
        chunk = full[s7:e7].strip()
        if len(chunk) > 300:
            sections.append(f"=== ITEM 7: MD&A ===\n{chunk[:MAX_SECTION]}")

    if sections:
        return "\n\n".join(sections), "sections"

    return full[:MAX_SECTION * 2], "full_fallback"


# ── Heuristic quality checker (pure Python, no LLM) ───────────────────────────

# Patterns for obviously forbidden entities
_RE_PERSON   = re.compile(
    r"^(Mr\.|Ms\.|Dr\.|Prof\.)?\s*[A-Z][a-z]+(\s+[A-Z]\.?)?\s+[A-Z][a-z]+"
    r"(\s+(Jr\.|Sr\.|II|III|IV))?$"
)
_RE_LEGAL    = re.compile(r"\bv\.\s+\w|\bIn re\b|\bLitigation\b|\bClass Action\b",
                          re.IGNORECASE)
_RE_SEC_RULE = re.compile(r"\bRule\s+\d|\bRegulation\s+[A-Z]-?\d*\b|\bSection\s+\d+",
                           re.IGNORECASE)
_RE_FORM     = re.compile(r"\bForm\s+\d|\bAnnual Report\b|\bQuarterly Report\b|\b10-[KQ]\b",
                           re.IGNORECASE)
_BOILERPLATE = frozenset(["IRS", "FASB", "GAAP", "IFRS", "PCAOB", "AICPA",
                           "SEC", "EDGAR", "NYSE", "Nasdaq"])  # generic refs
_GENERIC_CONCEPTS = re.compile(
    r"\b(fiscal year|depreciation|amortization|amortisation|revenue recognition|"
    r"audit committee|proxy statement|annual meeting|common stock|preferred stock|"
    r"earnings per share|net income|gross margin)\b",
    re.IGNORECASE
)

GOOD_TYPES = frozenset(["company", "organisation", "organization", "ticker",
                         "product", "technology", "market", "sector",
                         "industry", "country", "region", "index", "instrument"])


def _classify_entity(e: dict) -> str:
    """Return 'good', 'person', 'legal', 'rule', 'form', 'boilerplate', or 'concept'."""
    name = e.get("name", "")
    etype = (e.get("entity_type") or "").lower()

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
    # Entity type hints
    if any(t in etype for t in ("person", "human", "individual", "executive")):
        return "person"
    return "good"


def heuristic_check(entities: list[dict]) -> dict:
    """Classify each entity and return a quality summary dict."""
    classified: dict[str, list[str]] = {
        "good": [], "person": [], "legal": [], "rule": [],
        "form": [], "boilerplate": [], "concept": [],
    }
    for e in entities:
        cat = _classify_entity(e)
        classified[cat].append(e["name"])

    n_total    = len(entities)
    n_bad      = sum(len(classified[k]) for k in ("person", "legal", "rule",
                                                    "form", "boilerplate", "concept"))
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
    if classified["boilerplate"]:
        issues.append(f"boilerplate entities: {', '.join(classified['boilerplate'][:5])}")
    if classified["concept"]:
        issues.append(f"generic concepts: {', '.join(classified['concept'][:5])}")
    if too_few:
        issues.append(f"too few meaningful entities ({len(classified['good'])} good)")

    quality_ok = bad_ratio < 0.20 and not too_few

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
  (e.g. H100, Blackwell, Hopper, CUDA, NVLink, CoWoS, Grace CPU)
  Must be a specific branded/model name — NOT a generic technology category.
- Named business segments or specific markets the company operates in
  (e.g. Data Center, Gaming, Automotive, Professional Visualization, Networking)

FORBIDDEN (NEVER extract — skip entirely):
- Countries, regions, or geographies (China, United States, Europe, Taiwan)
- Financial indices, benchmarks, or ratings (S&P 500, NASDAQ, Moody's)
- Generic financial instruments (convertible notes, bonds, equity)
- Human personal names of any kind (executives, analysts, lawyers, investors)
- Legal cases: anything with "v.", "In re", "Derivative Litigation", "Class Action"
- SEC rules and rule numbers (Rule 10b-5, Regulation S-K, etc.)
- SEC filing form types (Form 10-K, Form 10-Q, Annual Report, etc.)
- Generic regulatory/accounting bodies (IRS, FASB, GAAP, IFRS, SEC as boilerplate)
- Laws and acts (Securities Exchange Act, Sarbanes-Oxley, Dodd-Frank, etc.)
- Generic legal/accounting concepts (fiscal year, audit, depreciation)
- Generic time periods (Q1, Q2, fiscal 2024)
- Vague concepts (supply chain, demand, growth, risk, strategy)

If in doubt, skip the entity. Quality over quantity."""

_EDGE_RULES = """\
RELATIONSHIP EXTRACTION RULES:
1. CRITICAL — use entity names EXACTLY as they appear in the entity list.
2. EXTRACT AGGRESSIVELY — extract as many meaningful relationships as possible.
3. PRIORITISED types:
   - Product/chip MADE_BY or DEVELOPED_BY company   (e.g. H100 → NVIDIA)
   - Technology USED_BY or ENABLES company/market
   - Company COMPETES_WITH company                   (e.g. NVIDIA → AMD)
   - Company SUPPLIES or MANUFACTURES_FOR company    (e.g. TSMC → NVIDIA)
   - Company OPERATES_IN market/sector/country
   - Company HAS_REVENUE_FROM or SELLS_INTO market
   - Ticker REPRESENTS company                       (e.g. NVDA → NVIDIA)
   - Company ACQUIRED or INVESTED_IN company
   - Company PARTNERS_WITH company
4. relation_type: short ALL_CAPS verb phrase (MADE_BY, COMPETES_WITH, etc.)."""

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
    good, bad = [], []
    for ed in (edges if isinstance(edges, list) else []):
        if not isinstance(ed, dict):
            continue
        if ed.get("source_entity_name") in valid_names \
                and ed.get("target_entity_name") in valid_names:
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
