"""restore_valid_entities.py

Second-pass correction: review all currently-isolated entities and restore
the ones that were incorrectly isolated (real companies, regulators, products, etc.)

Usage:
    cd /Users/x/projects/financial_agent
    python .claude/worktrees/competent-yalow/restore_valid_entities.py
"""

import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph_mirror import get_conn  # noqa: E402
from minimax import call_minimax  # noqa: E402

BATCH_SIZE = 80
DRY_RUN    = False
MIRROR_DB  = PROJECT_ROOT / "db" / "graph_mirror.db"

SYSTEM_PROMPT = """\
You are a financial knowledge graph curator reviewing INCORRECTLY isolated entities.

These entities were recently flagged as "not useful for financial analysis" but many \
of them are legitimate financial entities that should be RESTORED.

An entity should be RESTORED (un-isolated) if it is:
- A real company, corporation, organisation, government body, or fund \
  (e.g. Goldman Sachs, AT&T, AWS, Azure, Alphabet, Equinix, IBM, Infineon, GE Vernova)
- A financial regulator or regulatory framework \
  (e.g. BaFin, ECB, ACPR, AMF, GDPR, CHIPS Act, Inflation Reduction Act)
- A named financial product, instrument, or agreement \
  (e.g. CDX IG, A股, BIS Settlement Agreement, 2022 Walmart MAA, Convertible Notes)
- A named technology product or platform \
  (e.g. Blackwell chips, Android, Azure, GB200, DRAM, InfiniBand, EDA tools)
- A named industry category, market, or commodity \
  (e.g. Generative AI, EV, Data Center, DRAM, ETFs, Ethereum, Aluminum)
- A geographic market relevant to finance \
  (e.g. Asia Pacific, Europe, India, Hong Kong SAR)

An entity should STAY ISOLATED if it is:
- A raw monetary value (e.g. "$12 billion", "$575 million")
- A date/time expression (e.g. "2026年", "3月", "December 2024 quarter")
- A generic SEC/regulatory filing label (e.g. "Form 10-K", "Form 8-K", "Annual Report")
- A personal name (person, individual) — NOT a company or org
- A generic city or address used as filler (e.g. "Ann Arbor, Michigan", "Brighton, Colorado")
- A generic descriptive phrase (e.g. "AI-enabled solutions", "AI-powered platform", "Business Realignment Charges")
- A generic technology buzzword that is not a named product (e.g. "AI workloads", "Bots", "Components")
- A legal statute citation (e.g. "18 U.S.C. Section 1350", "10b5-1(c)")
- A customer placeholder (e.g. "Customer D")
- An internal job title/role (e.g. "Chairman of the Company's board")

Return ONLY a JSON object with one key "restore" containing an array of UUIDs to restore. \
No explanation, no markdown, just the JSON object.
"""


def un_isolate_entity(conn, uuid: str) -> bool:
    """Remove isolation from an entity and un-deprecate its edges."""
    cur = conn.execute(
        "UPDATE entities SET isolated=0, updated_at=datetime('now') WHERE uuid=?",
        (uuid,),
    )
    if cur.rowcount == 0:
        conn.commit()
        return False
    # Un-deprecate edges that were deprecated due to isolation
    conn.execute(
        """UPDATE edges
              SET deprecated=0, deprecated_reason='', updated_at=datetime('now')
            WHERE (src_uuid=? OR tgt_uuid=?)
              AND deprecated_reason='ENTITY_ISOLATED'""",
        (uuid, uuid),
    )
    conn.commit()
    return True


def classify_batch(entities: list[dict]) -> list[str]:
    """Send a batch of isolated entities to MiniMax and return UUIDs to restore."""
    items = [
        {"uuid": e["uuid"], "name": e["name"], "summary": (e["summary"] or "")[:200]}
        for e in entities
    ]
    user_content = (
        "Below are entities that were isolated from a financial knowledge graph. "
        "Identify which ones should be RESTORED because they are valid financial entities.\n\n"
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

    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        data = json.loads(text)
        return data.get("restore", [])
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse error: {e}")
        print(f"  Raw response: {text[:500]}")
        return []


def main():
    conn = get_conn(MIRROR_DB)

    # Load all currently-isolated entities
    rows = conn.execute(
        "SELECT uuid, name, summary FROM entities WHERE isolated=1 ORDER BY name"
    ).fetchall()

    total = len(rows)
    print(f"Found {total} isolated entities to review for possible restoration.")

    entities = [dict(r) for r in rows]
    batches = [entities[i:i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]

    total_restored = 0
    for i, batch in enumerate(batches):
        print(f"\nBatch {i+1}/{len(batches)} ({len(batch)} entities) …")
        try:
            to_restore = classify_batch(batch)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        print(f"  LLM says restore {len(to_restore)} entities:")
        name_map = {e["uuid"]: e["name"] for e in batch}
        for uuid in to_restore:
            name = name_map.get(uuid, uuid)
            print(f"    + {name} ({uuid})")
            if not DRY_RUN:
                un_isolate_entity(conn, uuid)
                total_restored += 1

        if i < len(batches) - 1:
            time.sleep(1)

    print(f"\nDone. Restored {total_restored} entities (dry_run={DRY_RUN}).")


if __name__ == "__main__":
    main()
