#!/usr/bin/env python3
"""
eval_entity_extraction.py — Eval loop for entity extraction prompt quality.

Tests the current ExtractedEntities prompt against real SEC HTML filings,
measures person-name leakage (and other noise), then iterates the prompt
until the failure rate hits zero.

Usage:
    python ingest/eval_entity_extraction.py                   # run eval, show failures
    python ingest/eval_entity_extraction.py --fix             # also apply the hardened prompt
    python ingest/eval_entity_extraction.py --rounds 3        # iterate up to 3 prompt refinements
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

# ── path bootstrap ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

from bs4 import BeautifulSoup
from minimax import call_minimax

# ── Eval corpus: real HTML filings ────────────────────────────────────────────
REPORT_DIR = Path(__file__).parent.parent / "financial_reports"

EVAL_FILES = [
    # (path, company ticker)
    (REPORT_DIR / "AAPL/2024-02-01_Earnings_Results_8-K_0000320193_24_000005_a8-kex991q1202412302023.htm", "AAPL"),
    (REPORT_DIR / "AMD/2024-01-30_Earnings_Results_-_Regulation_FD_8-K_0000002488_24_000009_q42023991final.htm", "AMD"),
    (REPORT_DIR / "NVDA/2024-02-21_Q4FY24_PRESS_RELEASE_8-K_0001045810_24_000028_q4fy24pr.htm", "NVDA"),
    (REPORT_DIR / "NVDA/2024-05-22_Q1FY25_PRESS_RELEASE_8-K_0001045810_24_000113_q1fy25pr.htm", "NVDA"),
    (REPORT_DIR / "AMD/2024-04-30_Earnings_Results_-_Regulation_FD_8-K_0000002488_24_000054_q12024991.htm", "AMD"),
]
# Trim to files that actually exist
EVAL_FILES = [(p, t) for p, t in EVAL_FILES if p.exists()]

# ── Known forbidden entity types ──────────────────────────────────────────────
PERSON_PATTERN = re.compile(
    r"^(Mr\.|Ms\.|Dr\.|Mrs\.|Sir\s)?[A-Z][a-z]+([\s\-][A-Z]\.?)*[\s\-][A-Z][a-z]+([\s\-][A-Z][a-z]+)?\.?$"
)

# Common person first names and family names that signal a person entity
_PERSON_FIRST_NAMES = {
    "james","john","robert","michael","william","david","richard","joseph","thomas","charles",
    "timothy","tim","christopher","daniel","paul","mark","donald","george","kenneth","steven",
    "edward","brian","ronald","anthony","kevin","jason","matthew","gary","jeffrey","ryan",
    "jacob","gary","eric","jonathan","stephen","larry","justin","scott","brandon","raymond",
    "frank","gregory","benjamin","samuel","patrick","alexander","jack","dennis","jerry",
    "lisa","mary","patricia","jennifer","linda","barbara","susan","jessica","sarah","karen",
    "nancy","betty","margaret","sandra","ashley","dorothy","kimberly","emily","donna","carol",
    "amanda","melissa","deborah","stephanie","sharon","rachel","carolyn","janet","catherine",
    "heather","diane","amy","julie","anna","samantha","jacqueline","christine","helen","debra",
    "jensen","lachlan","fintan","colette","severin","satya","sundar","elon","mukesh","masayoshi",
    "lisa","cristiano","bjorn","ole","lars","hans","sven","erik","stefan","henrik",
    # Asian first names common in finance
    "wei","lei","ming","hong","fang","jun","hao","yan","ling","qi","yu","bin",
}

_PERSON_FAMILY_NAMES = {
    "smith","johnson","williams","brown","jones","garcia","miller","davis","wilson","moore",
    "taylor","anderson","thomas","jackson","white","harris","martin","thompson","garcia",
    "martinez","robinson","clark","rodriguez","lewis","lee","walker","hall","allen","young",
    "hernandez","king","wright","lopez","hill","scott","green","adams","baker","gonzalez",
    "nelson","carter","mitchell","perez","roberts","turner","phillips","campbell","parker",
    "huang","cook","jobs","gates","zuckerberg","bezos","musk","nadella","pichai","ma",
    "kress","fleming","liebert","hacker","shaw","collins","chen","li","wang","zhang","liu",
    "yang","wu","xu","sun","zhao","zhou","huang","zhu","lin","he","guo","luo","song",
    "tang","han","cao","deng","xiao","peng","pan","yuan","dong","wei","fu","shen","ye",
    "lu","liang","jiang","yu","xie","shi","qian","hong","gu","yin","fan","mao",
}


# Known brand / company first-words that rule out person names
_KNOWN_BRANDS = {
    "apple","google","microsoft","amazon","meta","intel","nvidia","amd","tsmc","arm",
    "qualcomm","broadcom","samsung","sony","dell","hp","ibm","oracle","salesforce",
    "adobe","netflix","spotify","uber","lyft","airbnb","twitter","linkedin","zoom",
    "slack","palantir","snowflake","databricks","mongodb","redis","elastic","hashicorp",
    "softbank","alibaba","baidu","tencent","xiaomi","huawei","lenovo","foxconn",
    "caterpillar","boeing","lockheed","raytheon","northrop","eaton","emerson","honeywell",
    "fluid","grace","neural","data","professional","cloud","artificial","enterprise",
    "advanced","digital","general","national","american","global","international","first",
    "new","united","federal","standard","western","eastern","northern","southern","central",
    "microsoft","dell","sony","fluid","angular","vivid",
}

# Corporate / product suffix words — if present, it's not a person
_CORP_SUFFIXES = {
    "inc","corp","ltd","co","group","capital","holdings","technology","technologies",
    "systems","solutions","services","global","international","financial","resources",
    "energy","medical","sciences","platform","markets","analytics","ventures","partners",
    "industries","enterprises","associates","investments","management","consulting",
    "semiconductor","instruments","electronics","networks","communications","software",
    "hardware","cloud","computing","intelligence","labs","laboratory","research","studio",
    "studios","games","media","entertainment","press","publishing","books","films",
    "motors","automotive","aerospace","defense","pharma","bio","biotech","healthcare",
    "bank","insurance","securities","fund","trust","wealth","asset","investment",
    "superchips","frames","hopper","visualization","center","store","pay","music","watch",
    "ignite","vision","pro","max","ultra","plus","air","mini","se",
}


def _is_person_name(name: str) -> bool:
    """
    Classify a string as a human person name.
    Uses dictionary matching only — no broad regex — to avoid false positives
    on product names like 'Apple Watch' or 'Grace Hopper Superchips'.
    """
    name = name.strip()

    # Honorific prefix is a strong signal
    if re.match(r"^(Mr\.|Ms\.|Dr\.|Mrs\.|Prof\.|Sir\s)", name):
        return True

    words = name.split()
    if not (2 <= len(words) <= 3):
        return False

    # All words must start with uppercase
    if not all(re.match(r"^[A-Z]", w) for w in words):
        return False

    lower_words = [re.sub(r"[.,;]$", "", w.lower()) for w in words]

    # Rule out if any word is a known brand or corporate suffix
    if any(w in _KNOWN_BRANDS for w in lower_words):
        return False
    if any(w in _CORP_SUFFIXES for w in lower_words):
        return False
    # Rule out if any word has digits (product model numbers)
    if any(re.search(r"\d", w) for w in words):
        return False
    # Rule out ALL-CAPS words (ticker symbols / acronyms)
    if any(w.isupper() and len(w) > 1 for w in words):
        return False

    # Require at least one word to be a known personal first or last name
    if any(w in _PERSON_FIRST_NAMES or w in _PERSON_FAMILY_NAMES for w in lower_words):
        return True

    return False

NOISE_PATTERNS: list[tuple[str, re.Pattern]] = [
    # person_name is checked separately by _is_person_name() — not here
    ("dollar_amount",    re.compile(r"^\$[\d,.]+")),
    ("generic_acronym",  re.compile(r"^(AI|GPU|VR|AR|HPC|IoT|ML|API|SDK|CFO|CEO|COO|CTO|EPS|R&D|CapEx|OpEx)$")),
    ("geography",        re.compile(r"^(China|United States|USA|US|Europe|Asia|Taiwan|Japan|Korea|India|Global|North America|South America|Middle East|Africa|Pacific|APAC|EMEA)$", re.I)),
    ("sec_boilerplate",  re.compile(r"^(Form 10-K|Form 10-Q|Annual Report|Quarterly Report|Exhibit|8-K|GAAP|Non-GAAP|IFRS|FASB|PCAOB|Q[1-4] 20\d\d|FY\d\d|fiscal 20\d\d)$", re.I)),
    ("financial_figure", re.compile(r".*\b(million|billion|trillion)\b", re.I)),
]


def _html_to_text(path: Path, max_chars: int = 12_000) -> str:
    """Strip HTML, return clean plain text (first max_chars chars)."""
    html = path.read_text(errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # collapse blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text[:max_chars].strip()


def _classify_is_person(name: str) -> bool:
    """True if entity name matches person-name heuristic."""
    return _is_person_name(name)


def _classify_noise_type(name: str) -> str | None:
    for label, pat in NOISE_PATTERNS:
        if pat.search(name.strip()):
            return label
    return None


# ── Core: run extraction with a given system prompt ───────────────────────────

def extract_entities(text: str, system_prompt: str) -> list[str]:
    """Call MiniMax with the given system prompt, return list of extracted entity names."""
    user_msg = (
        "Extract all named entities from the following financial document text.\n\n"
        f"TEXT:\n{text}"
    )
    try:
        response, _, _ = call_minimax(
            messages=[
                {"role": "system", "name": "MiniMax AI", "content": system_prompt},
                {"role": "user",   "name": "User",       "content": user_msg},
            ],
            temperature=0.1,
            max_completion_tokens=1024,
        )
        # Parse: expect JSON array of strings or one name per line
        text_r = response.strip()
        if text_r.startswith("["):
            try:
                names = json.loads(text_r)
                if isinstance(names, list):
                    return [str(n).strip() for n in names if n]
            except json.JSONDecodeError:
                pass
        # fallback: one name per line
        return [ln.strip().lstrip("-• ").strip() for ln in text_r.splitlines()
                if ln.strip() and not ln.strip().startswith("#")]
    except Exception as e:
        print(f"  [extract_entities error] {e}")
        return []


# ── Eval runner ───────────────────────────────────────────────────────────────

def run_eval(system_prompt: str, label: str = "current") -> dict:
    """Run extraction on all eval files, return metrics."""
    results = []
    total_entities = 0
    total_persons = 0
    total_noise = 0
    all_failures: list[dict] = []

    print(f"\n{'='*65}")
    print(f"EVAL: {label}")
    print(f"{'='*65}")

    for path, ticker in EVAL_FILES:
        print(f"\n  [{ticker}] {path.name[:60]}")
        text = _html_to_text(path)
        entities = extract_entities(text, system_prompt)
        print(f"    → {len(entities)} entities extracted")

        persons   = [e for e in entities if _classify_is_person(e)]
        noise_ent = [e for e in entities
                     if not _classify_is_person(e) and _classify_noise_type(e)]

        if persons:
            print(f"    ❌ PERSON NAMES ({len(persons)}): {', '.join(persons[:8])}")
        if noise_ent:
            print(f"    ⚠  OTHER NOISE ({len(noise_ent)}): {', '.join(noise_ent[:5])}")
        if not persons and not noise_ent:
            print(f"    ✅ Clean — no forbidden entities detected")

        for p in persons:
            all_failures.append({"file": ticker, "entity": p, "type": "person_name"})
        for n in noise_ent:
            all_failures.append({"file": ticker, "entity": n,
                                  "type": _classify_noise_type(n)})

        total_entities += len(entities)
        total_persons  += len(persons)
        total_noise    += len(noise_ent)
        results.append({"ticker": ticker, "entities": entities,
                         "persons": persons, "noise": noise_ent})

    person_rate = total_persons / max(total_entities, 1)
    noise_rate  = total_noise   / max(total_entities, 1)

    print(f"\n{'─'*65}")
    print(f"SUMMARY ({label})")
    print(f"  Total extracted : {total_entities}")
    print(f"  Person names    : {total_persons}  ({person_rate:.1%} leak rate)")
    print(f"  Other noise     : {total_noise}    ({noise_rate:.1%})")
    print(f"  Score           : {max(0, 100 - total_persons*10 - total_noise*3)}/100")

    return {
        "label": label,
        "total": total_entities,
        "persons": total_persons,
        "noise": total_noise,
        "person_rate": person_rate,
        "failures": all_failures,
        "results": results,
    }


# ── Prompt refinement via MiniMax ─────────────────────────────────────────────

def refine_prompt(current_prompt: str, failures: list[dict]) -> str:
    """Ask MiniMax to strengthen the prompt based on observed failures."""
    if not failures:
        return current_prompt

    failure_summary = "\n".join(
        f"  - {f['entity']} (type={f['type']}, file={f['file']})"
        for f in failures[:20]
    )

    meta_prompt = textwrap.dedent(f"""
        You are a prompt engineer improving an LLM system prompt for financial entity extraction.

        CURRENT SYSTEM PROMPT:
        ---
        {current_prompt}
        ---

        OBSERVED FAILURES — these entities should NOT have been extracted:
        {failure_summary}

        Task: Rewrite the system prompt to prevent these failures while keeping
        all the ALLOWED entity types (companies, branded products, named business
        segments, stock tickers).

        Key requirements for the improved prompt:
        1. Make "NO PERSON NAMES" the absolute first rule — use ALL CAPS, bold emphasis.
        2. Add a self-check instruction: before returning any entity, the LLM must
           ask itself "Is this a human person's name?" and if yes, DISCARD it.
        3. Keep the ALLOWED section unchanged.
        4. Keep all other FORBIDDEN categories.
        5. Add concrete examples of the failed entities as FORBIDDEN examples.
        6. Output ONLY the improved system prompt text — no preamble, no explanation.
    """).strip()

    try:
        refined, _, _ = call_minimax(
            messages=[
                {"role": "system", "name": "MiniMax AI",
                 "content": "You are an expert prompt engineer. Output only the improved prompt."},
                {"role": "user", "name": "User", "content": meta_prompt},
            ],
            temperature=0.2,
            max_completion_tokens=2048,
        )
        return refined.strip()
    except Exception as e:
        print(f"[refine_prompt error] {e}")
        return current_prompt


# ── Prompt file I/O ───────────────────────────────────────────────────────────

PROMPT_FILE = Path(__file__).parent / "_entity_prompt.txt"

def load_current_prompt() -> str:
    """Load the prompt from the saved file, or extract from minimax_llm_client.py."""
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text()

    # Extract from source code as baseline
    client_path = Path(__file__).parent.parent / "minimax_llm_client.py"
    src = client_path.read_text()

    # Pull out the system message content + extra rules
    # (reconstruct as a flat string for eval purposes)
    baseline = (
        "You are a financial research analyst AI that extracts named entities "
        "from sell-side research reports, SEC filings, earnings releases, and "
        "financial news documents. "
        "The text comes from PDFs or HTML pages — NOT from a conversation. "
        "There is no 'speaker', no 'current message', and no dialogue. "
        "Your only task is to identify companies, branded products, technologies, "
        "and named business segments that are subjects of financial analysis.\n\n"
        "STRICT ENTITY EXTRACTION RULES:\n\n"
        "Entities must be a real company, a specific BRANDED product/technology, "
        "or a clearly named business segment. Nothing else.\n\n"
        "ALLOWED (extract ONLY these):\n"
        "- Companies and organisations (e.g. NVIDIA, TSMC, AMD, Microsoft, SoftBank, Arm)\n"
        "- Stock tickers (e.g. NVDA, TSM, AAPL, AMD)\n"
        "- Named products, chips, platforms, or proprietary technologies\n"
        "  (e.g. H100, Blackwell, Hopper, CUDA, NVLink, CoWoS, Grace CPU, GeForce, Quadro)\n"
        "  Must be a specific BRANDED or MODEL name — NOT a generic category.\n"
        "  BAD: 'GPU', 'AI', 'VR', 'HPC', 'Digital Signal Processors' — too generic.\n"
        "- Named business segments the company itself uses for its divisions\n"
        "  (e.g. Data Center, Gaming, Automotive, Professional Visualization)\n\n"
        "FORBIDDEN (NEVER extract — skip entirely):\n"
        "- ANY monetary value or financial figure: $79 million, $5.2 billion, $1.0 billion.\n"
        "  Any string starting with '$' or containing a number + million/billion/trillion.\n"
        "  If the name contains a dollar sign OR a numeric amount, DO NOT extract it.\n"
        "- Generic technology acronyms: AI, VR, AR, GPU, HPC, IoT, ML, API, SDK\n"
        "- Generic technology categories: 'Digital Signal Processors',\n"
        "  'Analog Integrated Circuits', 'Semiconductor Market', 'Cloud Computing'\n"
        "- Countries, regions, or geographies (China, United States, Europe, Taiwan)\n"
        "- Financial indices, benchmarks, or ratings (S&P 500, NASDAQ, Moody's)\n"
        "- Generic financial instruments (convertible notes, bonds, equity)\n"
        "- Human personal names: executives, analysts, authors, lawyers, investors\n"
        "  Examples: Jensen Huang, Tim Cook, Lachlan Shaw, Fintan Collins\n"
        "  Even if a person is important — extract the COMPANY they lead, not their name.\n"
        "- Broker or bank subsidiary entities from disclaimer sections:\n"
        "  e.g. 'UBS Securities Australia Ltd', 'J.P. Morgan Securities Asia Limited',\n"
        "  'Macquarie Capital (USA) Inc.', 'Goldman Sachs India Securities Private Ltd'.\n"
        "  Pattern: '[Bank] [Country/City] [Securities/Brokerage/Capital/Banking]'.\n"
        "  These appear in the legal disclosure pages — NEVER extract them.\n"
        "- Legal cases: 'v.', 'In re', 'Derivative Litigation', 'Class Action'\n"
        "- SEC rules and rule numbers (Rule 10b-5, Regulation S-K, etc.)\n"
        "- SEC filing form types (Form 10-K, Form 10-Q, Annual Report, etc.)\n"
        "- Regulatory/accounting boilerplate: IRS, FASB, GAAP, IFRS, PCAOB\n"
        "- Laws and acts (Securities Exchange Act, Sarbanes-Oxley, Dodd-Frank)\n"
        "- Generic legal/accounting concepts (fiscal year, audit, depreciation)\n"
        "- Generic time periods (Q1, Q2, fiscal 2024)\n"
        "- Vague concepts (supply chain, demand, growth, risk, strategy, innovation)\n\n"
        "If in doubt, skip the entity. Quality over quantity.\n\n"
        "Return your answer as a JSON array of entity name strings:\n"
        '[\"Entity A\", \"Entity B\", ...]'
    )
    PROMPT_FILE.write_text(baseline)
    return baseline


def save_prompt(prompt: str, label: str = ""):
    PROMPT_FILE.write_text(prompt)
    if label:
        backup = PROMPT_FILE.with_suffix(f".{label}.txt")
        backup.write_text(prompt)
        print(f"  Saved prompt → {backup.name}")


def apply_prompt_to_source(new_prompt: str):
    """
    Print the new FORBIDDEN/person-name rule block so the developer can
    paste it into minimax_llm_client.py.  (Full auto-patch is too fragile.)
    """
    print("\n" + "="*65)
    print("APPLY: paste the following into minimax_llm_client.py")
    print("       replacing the current 'STRICT ENTITY EXTRACTION RULES' block")
    print("="*65)
    # Extract just the rules section
    marker = "STRICT ENTITY EXTRACTION RULES"
    if marker in new_prompt:
        idx = new_prompt.index(marker)
        print(new_prompt[idx:])
    else:
        print(new_prompt)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Eval + iterate entity extraction prompt")
    ap.add_argument("--rounds", type=int, default=1,
                    help="Number of prompt refinement rounds (default 1)")
    ap.add_argument("--fix", action="store_true",
                    help="After eval, print the improved prompt for pasting into source")
    args = ap.parse_args()

    if not EVAL_FILES:
        print("No eval HTML files found — check financial_reports/ directory.")
        sys.exit(1)

    print(f"Eval corpus: {len(EVAL_FILES)} HTML filings")
    for p, t in EVAL_FILES:
        print(f"  {t}: {p.name}")

    prompt = load_current_prompt()

    for round_i in range(args.rounds):
        label = f"round_{round_i}" if args.rounds > 1 else "current"
        metrics = run_eval(prompt, label=label)

        if metrics["persons"] == 0 and metrics["noise"] == 0:
            print("\n✅ PERFECT — no forbidden entities detected. Prompt is good.")
            break

        if round_i < args.rounds - 1 or args.fix:
            print(f"\n⚙  Refining prompt (round {round_i + 1}/{args.rounds})…")
            new_prompt = refine_prompt(prompt, metrics["failures"])
            save_prompt(new_prompt, label=f"v{round_i + 1}")
            prompt = new_prompt

            if args.rounds > 1 and round_i < args.rounds - 1:
                # Re-eval with new prompt
                continue

        if args.fix and metrics["failures"]:
            apply_prompt_to_source(prompt)
    else:
        if args.rounds > 1:
            # Final eval after last refinement
            run_eval(prompt, label=f"final_v{args.rounds}")

    print("\nDone.")


if __name__ == "__main__":
    main()
