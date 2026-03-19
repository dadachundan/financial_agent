"""isolate_nonsense_entities.py

One-off script to scan all non-isolated entities and mark ones that don't
make sense for financial analysis as isolated.

Entities that are NOT useful for financial analysis:
- Raw monetary/numeric values (e.g. "$12 billion", "$425 million", "3月")
- Generic legal/regulatory codes (e.g. "18 U.S.C. Section 1350", "10b5-1(c)")
- Date/time expressions (e.g. "2026年", "3月", "Q1 2025")
- Generic SEC filing type labels (e.g. "8-K", "10-K", "10-Q" as standalone labels)
- Open-source license names (e.g. "AGPL", "GPL", "MIT License")
- Generic plan labels that are just year+word combos with no specific entity identity
  (e.g. "2023 Plan", "2025 Plan" unless they refer to a named initiative)
- Generic technology versions or standards that are not specific products
  (e.g. bare "4G" without a company context)
- Other non-entity noise (generic phrases, boilerplate legal language)

Entities that SHOULD be kept:
- Companies, corporations, organizations, government agencies
- Named financial products, instruments, agreements (e.g. "2025 Walmart MAA", "2029 Convertible Notes")
- Named technology products or platforms (e.g. "5th Gen AMD EPYC", "3DIC Compiler")
- Business segments, divisions, programs
- Named regulatory/military programs (e.g. "AFWERX Agility Prime")
- Technologies that are named products (e.g. "5G" as a Marvell/Lam product context is borderline)
- Geographic markets, stock tickers

Usage:
    cd /Users/x/projects/financial_agent
    python .claude/worktrees/competent-yalow/isolate_nonsense_entities.py
"""

import json
import sys
import time
from pathlib import Path

# ── path setup ────────────────────────────────────────────────────────────────
WORKTREE = Path(__file__).parent
PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph_mirror import get_conn, isolate_entity  # noqa: E402
from minimax import call_minimax  # noqa: E402

# ── config ────────────────────────────────────────────────────────────────────
BATCH_SIZE = 80          # entities per LLM call
DRY_RUN    = False       # set True to print without writing
MIRROR_DB  = PROJECT_ROOT / "db" / "graph_mirror.db"

SYSTEM_PROMPT = """\
You are a financial knowledge graph curator. Your job is to identify entities \
that are NOT meaningful nodes in a financial knowledge graph.

An entity is WORTH KEEPING if it is any of:
- A company, corporation, organisation, government body, or fund
- A named financial product, instrument, or agreement (e.g. "2029 Convertible Notes", "2025 Walmart MAA")
- A named technology product, platform, or standard with business relevance
- A business segment, division, or program name
- A named regulatory, military, or research program
- A stock ticker or named index
- A technology/concept that is a major industry category (e.g. "5G", "AI", "Cloud")

An entity should be ISOLATED (removed) if it is any of:
- A raw monetary or numeric value (e.g. "$12 billion", "$425 million")
- A generic date/time expression (e.g. "2026年", "3月", "Q1 2025", "2026")
- A generic SEC filing type label used as an entity (e.g. "8-K", "10-K", "10-Q")
- A legal statute or regulatory rule citation (e.g. "18 U.S.C. Section 1350", "10b5-1(c)")
- An open-source license name (e.g. "AGPL", "GPL", "MIT License")
- A generic year-based restructuring plan with no specific identity beyond the year \
  (e.g. "2023 Plan", "2025 Plan" — UNLESS the summary shows it is a specific named initiative)
- A boilerplate legal phrase or generic clause
- A generic version label with no product context (e.g. "4G" alone with no company tie-in)
- Any other noise that is not a meaningful financial analysis entity

Return ONLY a JSON object with one key "isolate" containing an array of UUIDs to isolate. \
No explanation, no markdown, just the JSON object.
"""


def classify_batch(entities: list[dict]) -> list[str]:
    """Send a batch of entities to MiniMax and return UUIDs to isolate."""
    items = [
        {"uuid": e["uuid"], "name": e["name"], "summary": (e["summary"] or "")[:200]}
        for e in entities
    ]
    user_content = (
        "Below are entities in a financial knowledge graph. "
        "Identify which ones should be ISOLATED (not useful for financial analysis).\n\n"
        + json.dumps(items, ensure_ascii=False, indent=2)
    )
    text, elapsed, _ = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": SYSTEM_PROMPT},
            {"role": "user",   "name": "User",       "content": user_content},
        ],
        temperature=0.1,
        max_completion_tokens=2048,
    )
    print(f"  LLM responded in {elapsed:.1f}s")

    # Parse JSON from response
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        data = json.loads(text)
        return data.get("isolate", [])
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse error: {e}")
        print(f"  Raw response: {text[:500]}")
        return []


def main():
    conn = get_conn(MIRROR_DB)

    # Load all non-isolated entities
    rows = conn.execute(
        "SELECT uuid, name, summary FROM entities "
        "WHERE (isolated=0 OR isolated IS NULL) ORDER BY name"
    ).fetchall()

    total = len(rows)
    print(f"Found {total} non-isolated entities to classify.")

    entities = [dict(r) for r in rows]
    batches = [entities[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]

    total_isolated = 0
    for i, batch in enumerate(batches):
        print(f"\nBatch {i+1}/{len(batches)} ({len(batch)} entities) …")
        try:
            to_isolate = classify_batch(batch)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        print(f"  LLM says isolate {len(to_isolate)} entities:")
        # Build name lookup for this batch
        name_map = {e["uuid"]: e["name"] for e in batch}
        for uuid in to_isolate:
            name = name_map.get(uuid, uuid)
            print(f"    - {name} ({uuid})")
            if not DRY_RUN:
                isolate_entity(conn, uuid)
                total_isolated += 1

        # Small pause to be polite to the API
        if i < len(batches) - 1:
            time.sleep(1)

    print(f"\nDone. Isolated {total_isolated} entities (dry_run={DRY_RUN}).")


if __name__ == "__main__":
    main()
