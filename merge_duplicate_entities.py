"""merge_duplicate_entities.py

Scans non-isolated entities for duplicates / synonyms and merges them.

Strategy
--------
Pass 1 — Exact-name duplicates (no LLM):
    GROUP BY name HAVING count > 1.  Keep the entry with the longest summary;
    merge all others into it.

Pass 2 — Semantic duplicates (LLM, candidate-pair confirmation):
    1. Build candidate pairs using name-similarity heuristics:
       - SequenceMatcher ratio >= 0.75 on normalised names (sliding window)
       - Containment: normalised(A) is a substring of normalised(B) or vice versa
       - Shared first-word groups (first word >= 4 chars)
    2. Send small batches of candidate pairs to MiniMax for confirmation.
       The LLM only sees genuine lookalike pairs — no hallucination over
       unrelated alphabetical neighbours.
    3. Merge confirmed pairs.

For every merge the source entity's edges are re-pointed to the target in the
SQLite mirror; self-loops are removed.  Kuzu stale nodes are cleaned up via
a best-effort DELETE (skipped if Kuzu is locked by the running Flask server).

Usage:
    cd /Users/x/projects/financial_agent
    python .claude/worktrees/competent-yalow/merge_duplicate_entities.py

    # Dry-run (no writes):
    DRY_RUN=1 python .claude/worktrees/competent-yalow/merge_duplicate_entities.py

    # Skip LLM pass (exact duplicates only):
    EXACT_ONLY=1 python .claude/worktrees/competent-yalow/merge_duplicate_entities.py
"""

import difflib
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph_mirror import get_conn, merge_entities  # noqa: E402
from minimax import call_minimax                    # noqa: E402

# ── config ────────────────────────────────────────────────────────────────────
MIRROR_DB        = PROJECT_ROOT / "db" / "graph_mirror.db"
GRAPH_DIR        = PROJECT_ROOT / "db" / "graphiti_db"
SIMILARITY_RATIO = 0.85   # SequenceMatcher threshold for candidate pairing
CONFIRM_BATCH    = 40     # pairs per LLM confirmation call
DRY_RUN          = os.getenv("DRY_RUN", "0") == "1"
EXACT_ONLY       = os.getenv("EXACT_ONLY", "0") == "1"

SYSTEM_PROMPT = """\
You are a financial knowledge graph curator reviewing CANDIDATE DUPLICATE pairs.
Your default answer is DO NOT MERGE — only confirm a merge when you are certain.

KEY RULE — The ONLY safe reason to merge is one of:
  (a) One name is the other + a purely legal suffix: "Inc.", "Corp.", "Ltd.", "LLC",
      "Corporation", "Incorporated", "PLC", "S.A.", "GmbH", "Co.", "Group" alone, etc.
      e.g. "Intel" / "Intel Corporation" → MERGE
           "NuScale" / "NuScale Corp" → MERGE
           "Sandisk Corporation" / "SanDisk LLC" → MERGE (same company, equivalent suffixes)
  (b) One name is a well-known abbreviation or ticker of the other (abbrev must be
      all-caps initialism or widely-known short form):
      e.g. "AWS" / "Amazon Web Services" → MERGE
           "TSMC" / "Taiwan Semiconductor Manufacturing Company Limited" → MERGE
           "FCA" / "Financial Conduct Authority" → MERGE
  (c) One name is the other + a branch/country-suffix that does NOT indicate a separate
      legal entity for the parent (same bank or regulator, just different office):
      e.g. "UBS AG, Singapore Branch" / "UBS AG" → MERGE
           "Merrill Lynch (Singapore) Pte Ltd" / "Merrill Lynch International" → MERGE
  (d) Trivial spelling/punctuation variants (comma, period, abbreviation of the same word):
      e.g. "JCET Group Co. Ltd." / "JCET Group Co., Ltd." → MERGE
           "SYNOPSYS, INC." / "Synopsys, Inc." → MERGE

DO NOT MERGE if any of these apply — even if names look similar:
  • Longer name adds a meaningful word beyond a legal suffix:
    "Hitachi" ≠ "Hitachi Energy"          (Energy = different subsidiary)
    "Hitachi" ≠ "Hitachi Vantara"         (Vantara = different division)
    "Qualcomm" ≠ "Qualcomm CDMA Technologies (QCT)"  (QCT = subsidiary)
    "Caterpillar Inc" ≠ "Cat Financial"   (Cat Financial = finance arm)
    "Samsung" ≠ "Samsung Electronics"     (Electronics = specific subsidiary)
    "Cloud" ≠ "Cloud Light"              (Cloud Light = specific company)
    "Cortex" ≠ "Cortex XDR"             (XDR = specific product)
    "Cortex Cloud" ≠ "Cortex XDR"       (different products)
  • Country / geographic region ≠ company, regulator, or concept in that region:
    "China" ≠ "China Communications Construction Group"
    "Hong Kong" ≠ "Hong Kong Securities and Futures Commission"
    "United States" ≠ "United States Antimony Corporation"
    "United States" ≠ "United Airlines Inc."
  • Different regulatory bodies or different laws:
    "SEC" ≠ "Securities Act of 1933"
    "European Union" ≠ "European Central Bank"
  • Company ≠ its product or product line (even if product name starts with company name):
    "Apple" ≠ "Apple App Store"
    "Google" ≠ "Google Search"   (keep Google and its products separate)
    "Oracle" ≠ "Oracle Cloud Services"  (keep parent and cloud arm separate)
  • Customer placeholder ≠ any real entity:
    "Customer A", "Customer B" should never be merged with anything
  • Different companies that happen to share a first word

Strict rules:
- When in doubt, do NOT merge.
- Only merge on criteria (a)–(d) above.
- For "keep": choose the shorter/simpler name (brand over legal), or the one with longer summary.

Input: a JSON array of candidate pairs, each with fields a and b (uuid, name, summary).
Output: ONLY a JSON object {"groups": [{"keep": <uuid>, "merge": [<uuid>]}, ...]}.
Return {"groups": []} if nothing should be merged.
No markdown, no explanation, just the JSON object.
"""


# ── Kuzu cleanup (best-effort) ────────────────────────────────────────────────

def _kuzu_delete(uuid: str) -> None:
    """Try to remove a node from Kuzu; silently skip if DB is locked."""
    try:
        import kuzu  # type: ignore
        kdb  = kuzu.Database(str(GRAPH_DIR), read_only=False)
        conn = kuzu.Connection(kdb)
        conn.execute(
            "MATCH (n:Entity {uuid: $uuid}) "
            "OPTIONAL MATCH (:Entity)-[:RELATES_TO]->(r:RelatesToNode_)-[:RELATES_TO]->(n) "
            "OPTIONAL MATCH (n)-[:RELATES_TO]->(r2:RelatesToNode_)-[:RELATES_TO]->(:Entity) "
            "DETACH DELETE r, r2, n",
            {"uuid": uuid},
        )
    except Exception as e:
        print(f"    [kuzu] cleanup skipped for {uuid}: {e}")


# ── Pass 1: exact-name duplicates ─────────────────────────────────────────────

def pass1_exact(conn) -> int:
    """Merge entities with identical names. Returns number of merges performed."""
    rows = conn.execute(
        """SELECT name, GROUP_CONCAT(uuid, '|') as uuids
             FROM entities
            WHERE (isolated=0 OR isolated IS NULL)
            GROUP BY name
           HAVING COUNT(*) > 1
            ORDER BY name"""
    ).fetchall()

    if not rows:
        print("Pass 1: no exact-name duplicates found.")
        return 0

    total = 0
    for row in rows:
        name  = row[0]
        uuids = row[1].split("|")
        # Pick canonical: longest summary; on tie, first in list
        details = conn.execute(
            f"SELECT uuid, LENGTH(COALESCE(summary,'')) as slen FROM entities "
            f"WHERE uuid IN ({','.join('?'*len(uuids))})",
            uuids,
        ).fetchall()
        details.sort(key=lambda r: -r[1])  # longest summary first
        keep_uuid   = details[0][0]
        merge_uuids = [r[0] for r in details[1:]]

        print(f"  [{name}] keep={keep_uuid[:8]}… merge {len(merge_uuids)} duplicate(s)")
        for src in merge_uuids:
            if src == keep_uuid:
                continue  # safety: never self-merge
            if not DRY_RUN:
                merge_entities(conn, source_uuid=src, target_uuid=keep_uuid)
                _kuzu_delete(src)
            total += 1

    return total


# ── Pass 2: candidate-pair similarity + LLM confirmation ─────────────────────

def _normalise(name: str) -> str:
    """Lowercase, collapse punctuation to space, strip whitespace."""
    n = re.sub(r"[^\w\s]", " ", name.lower())
    return re.sub(r"\s+", " ", n).strip()


# Generic first words that appear in many unrelated entities — exclude from
# first-word grouping to avoid pairing unrelated companies.
_STOP_FIRST_WORDS = {
    "the", "a", "an", "new", "old",
    "national", "international", "global", "local",
    "advanced", "general", "digital", "cloud", "data", "smart", "power",
    "design", "product", "service", "system", "technology", "tech",
    "financial", "capital", "investment", "enterprise", "business",
    "china", "india", "asia", "europe", "north", "south", "east", "west",
    "central", "federal", "state", "american", "european", "american",
    "chief", "corporate", "commercial", "industrial", "energy",
    "communication", "communications", "information",
}


def _build_candidate_pairs(entities: list[dict]) -> list[tuple[dict, dict]]:
    """Return (entity_a, entity_b) pairs that are name-similar."""
    norms = [(e, _normalise(e["name"])) for e in entities]
    norms.sort(key=lambda x: x[1])  # sort by normalised name

    seen: set[frozenset] = set()
    candidates: list[tuple[dict, dict]] = []

    def _add(ea: dict, eb: dict) -> None:
        key = frozenset([ea["uuid"], eb["uuid"]])
        if key not in seen and ea["uuid"] != eb["uuid"]:
            seen.add(key)
            candidates.append((ea, eb))

    # Sliding-window SequenceMatcher (catches legal-name / abbrev variants).
    # High threshold (0.85+) keeps only names that are very close in spelling.
    WINDOW = 20
    for i, (ea, na) in enumerate(norms):
        for j in range(i + 1, min(i + WINDOW, len(norms))):
            eb, nb = norms[j]
            if difflib.SequenceMatcher(None, na, nb).ratio() >= SIMILARITY_RATIO:
                _add(ea, eb)

    # First-word groups: same first word (>= 7 chars, not a generic stop word).
    # Min length 7 filters out short generics ("cloud", "china", "atlas", "apple"
    # all have <= 6 chars in their first word as normalised).
    # Cap group size to avoid O(n²) explosion on common prefixes.
    fw_groups: dict[str, list[dict]] = defaultdict(list)
    for e, n in norms:
        words = n.split()
        fw = words[0] if words else ""
        if len(fw) >= 7 and fw not in _STOP_FIRST_WORDS:
            fw_groups[fw].append(e)
    for grp in fw_groups.values():
        if len(grp) < 2 or len(grp) > 15:  # ignore singleton or huge groups
            continue
        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                _add(grp[i], grp[j])

    return candidates


def _confirm_batch(pairs: list[tuple[dict, dict]]) -> list[dict]:
    """Send a batch of candidate pairs to MiniMax and return confirmed merge groups.

    Each returned group is validated against the input pairs so the LLM cannot
    cross-contaminate UUIDs across unrelated pairs.
    """
    # Build a set of valid {uuid_a, uuid_b} frozensets for post-validation
    valid_sets: set[frozenset] = {frozenset([a["uuid"], b["uuid"]]) for a, b in pairs}

    items = [
        {
            "a": {"uuid": a["uuid"], "name": a["name"], "summary": (a["summary"] or "")[:200]},
            "b": {"uuid": b["uuid"], "name": b["name"], "summary": (b["summary"] or "")[:200]},
        }
        for a, b in pairs
    ]
    user_content = (
        f"Review these {len(items)} candidate entity pairs. "
        "Identify which pairs should be MERGED into one canonical node.\n\n"
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
    print(f"    LLM responded in {elapsed:.1f}s")

    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        data = json.loads(text)
        raw_groups = data.get("groups", [])
    except json.JSONDecodeError as e:
        print(f"    WARNING: JSON parse error: {e}")
        print(f"    Raw: {text[:500]}")
        return []

    # Validate: only accept (keep, src) pairs that were actually in the input batch.
    # This prevents the LLM from cross-contaminating UUIDs across unrelated pairs.
    validated = []
    for g in raw_groups:
        keep   = g.get("keep", "")
        merges = g.get("merge", [])
        if not keep or not merges:
            continue
        safe_merges = [
            src for src in merges
            if src != keep and frozenset([keep, src]) in valid_sets
        ]
        if safe_merges:
            validated.append({"keep": keep, "merge": safe_merges})

    return validated


def pass2_semantic(conn) -> int:
    """Candidate-pair + LLM confirmation dedup pass. Returns merges performed."""
    rows = conn.execute(
        "SELECT uuid, name, summary FROM entities "
        "WHERE (isolated=0 OR isolated IS NULL)"
    ).fetchall()
    entities = [dict(r) for r in rows]

    print(f"  Building candidate pairs from {len(entities)} entities …")
    pairs = _build_candidate_pairs(entities)
    print(f"  Found {len(pairs)} candidate pairs to review.\n")

    if not pairs:
        return 0

    merged_away: set[str] = set()
    confirmed_pairs: set[frozenset] = set()
    total = 0

    batches = [pairs[i:i + CONFIRM_BATCH] for i in range(0, len(pairs), CONFIRM_BATCH)]
    for bi, batch in enumerate(batches):
        print(f"  Batch {bi+1}/{len(batches)} ({len(batch)} pairs) …")
        groups = _confirm_batch(batch)

        for g in groups:
            keep   = g.get("keep", "")
            merges = g.get("merge", [])
            if not keep or not merges:
                continue

            for src in merges:
                if src == keep:
                    continue  # never self-merge
                key = frozenset([keep, src])
                if key in confirmed_pairs:
                    continue
                confirmed_pairs.add(key)

                if src in merged_away or keep in merged_away:
                    continue

                # Verify both entities still exist
                keep_row = conn.execute(
                    "SELECT name FROM entities WHERE uuid=? AND (isolated=0 OR isolated IS NULL)",
                    (keep,)
                ).fetchone()
                src_row = conn.execute(
                    "SELECT name FROM entities WHERE uuid=? AND (isolated=0 OR isolated IS NULL)",
                    (src,)
                ).fetchone()
                if not keep_row or not src_row:
                    continue

                print(f"    MERGE '{src_row[0]}' → '{keep_row[0]}'")
                if not DRY_RUN:
                    merge_entities(conn, source_uuid=src, target_uuid=keep)
                    _kuzu_delete(src)
                    merged_away.add(src)
                total += 1

        if bi < len(batches) - 1:
            time.sleep(1)

    return total


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    conn = get_conn(MIRROR_DB)

    before = conn.execute(
        "SELECT COUNT(*) FROM entities WHERE isolated=0 OR isolated IS NULL"
    ).fetchone()[0]
    print(f"Starting with {before} visible entities  (dry_run={DRY_RUN})\n")

    print("=== Pass 1: exact-name duplicates ===")
    n1 = pass1_exact(conn)
    print(f"Pass 1 done: {n1} merges.\n")

    if not EXACT_ONLY:
        print("=== Pass 2: semantic duplicates (candidate-pair LLM) ===")
        n2 = pass2_semantic(conn)
        print(f"\nPass 2 done: {n2} merges.")
    else:
        n2 = 0

    after = conn.execute(
        "SELECT COUNT(*) FROM entities WHERE isolated=0 OR isolated IS NULL"
    ).fetchone()[0]
    print(f"\nTotal merges: {n1 + n2}  ({before} → {after} visible entities)")


if __name__ == "__main__":
    main()
