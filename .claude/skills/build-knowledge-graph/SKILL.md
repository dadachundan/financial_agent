---
name: build-knowledge-graph
description: Mine entities and relationships from research reports under reports/ and write them directly into db/graph_mirror.db via manual_graph.py. Use when the user asks to "update the knowledge graph", "mine relations from reports", "build the graph", "ingest these reports into /zep/", "rebuild the graph from reports/", or anything in that family. The agent (Claude in conversation) reads the sources and curates — there is no LLM API call, ever. Honours the project-wide "NEVER call the Claude API" rule from CLAUDE.md.
---

# Build Knowledge Graph

Mine high-quality entities and edges from research markdown under `reports/`
and write them directly into the SQLite store at `db/graph_mirror.db`. The
viewer at `localhost:5001/zep/` reads from that file, so additions show up
on browser refresh.

## Where things live (paths the agent will need)

All paths are **relative to the project root**
(`/Users/x/projects/financial_agent/`). When you run a Python snippet
from `Bash`, run it from the project root so `import manual_graph`
and `import graph_mirror` resolve.

| Need to … | Path |
|---|---|
| Read this skill | [`.claude/skills/build-knowledge-graph/SKILL.md`](SKILL.md) |
| Read the relation taxonomy | [`.claude/skills/build-knowledge-graph/references/allowed_relations.md`](references/allowed_relations.md) |
| Read the entity-quality rules | [`.claude/skills/build-knowledge-graph/references/entity_quality.md`](references/entity_quality.md) |
| List unprocessed reports | [`.claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py`](scripts/unprocessed_reports.py) |
| **Write entities/edges (the only sanctioned write path)** | [`manual_graph.py`](../../../manual_graph.py) — at the project root |
| Read-only graph helpers (counts, search, deprecate, isolate) | [`graph_mirror.py`](../../../graph_mirror.py) — at the project root |
| The live graph | [`db/graph_mirror.db`](../../../db/graph_mirror.db) |
| Project-wide hard rule against LLM APIs | [`CLAUDE.md`](../../../CLAUDE.md) §"NEVER call the Claude API" |
| Source markdown to curate from | [`reports/company/`](../../../reports/company/), [`reports/sector/`](../../../reports/sector/), [`reports/compare/`](../../../reports/compare/), [`reports/earnings/`](../../../reports/earnings/) |

Imports to copy-paste:

```python
import sys; sys.path.insert(0, '.')        # if not already on sys.path
from manual_graph import (
    add_entity, add_edge, add_episode,     # single-row writes
    add_entities, add_edges,               # bulk writes
    find_entity, stats,                    # read helpers
)
import graph_mirror as gm                  # for deprecate_edge / isolate_entity / update_edge
```

## Core principle: no LLM API, ever

**This skill exists specifically because the user removed every automated
LLM extraction path.** See the "NEVER call the Claude API" section at the
top of [CLAUDE.md](../../../CLAUDE.md). The agent (you, Claude, in this
conversation) reads each report yourself, decides which entities and
relationships are real, and writes them via `manual_graph.py`. No
`from anthropic import …`, no `client.messages.create`, no `call_claude`,
no `call_minimax`. Not even "just this once."

If you find yourself wanting to write a script that calls an LLM, stop and
re-read this paragraph.

## Hard constraints

These four rules are non-negotiable. They are why this skill exists.

1. **Allowed relation types: `COMPETES_WITH` and `SUPPLIES` only.**
   The graph currently has 5 stray minority types (12 edges) from earlier
   ad-hoc curation. Don't add new edges with any other relation name.
   - `MAKES`, `DEVELOPED`, `IS_COMPONENT_OF` → **map to `SUPPLIES`** when
     ingesting new reports (product is supplied by its maker).
   - `OUT_LICENSED_TO`, `LICENSED` → **map to `SUPPLIES`** for new edges
     (licensor "supplies" the IP / drug asset to the licensee).
   - See [references/allowed_relations.md](references/allowed_relations.md)
     for the decision tree.

2. **≤ 10 active edges per entity.** Quality > coverage. Before writing
   an edge whose source or target already has 10 edges (active, not
   isolated/deprecated), drop the *least decision-relevant* existing edge
   for that entity first. Pre-check counts with:
   ```python
   import graph_mirror as gm
   c = gm.get_conn()
   n = c.execute(
       "SELECT COUNT(*) FROM edges e "
       "WHERE (e.deprecated=0 OR e.deprecated IS NULL) "
       "AND (e.src_uuid=? OR e.tgt_uuid=?)",
       (uuid, uuid),
   ).fetchone()[0]
   ```

3. **Companies only.** Every entity must carry `labels=["Company"]`. No
   `Product`, no `Index`, no `Segment`, no `Person`, no anything else.
   When a report describes a brand / chip / drug, encode the *relationship*
   between the maker and the customer / partner / competitor — never add the
   product itself as a node. (Old approach allowed products; the user
   tightened the rule on 2026-06-02. The 6 products + 1 index already in
   the graph are isolated.)

4. **No humans, no $ amounts, no generic terms.** See
   [references/entity_quality.md](references/entity_quality.md) for the
   FORBIDDEN list. If in doubt, skip.

## Workflow

### Step 1 — Pick the scope

Ask the user (or infer from their phrasing) what they want covered:

- "update the knowledge graph" → take the *newest unprocessed* reports
  (use `scripts/unprocessed_reports.py` to list them)
- "mine relations from reports/company/X" → that specific folder
- "rebuild the graph" → don't. The user has 177 entities + 311 edges that
  cost real time to curate; never wipe without explicit per-table
  instructions
- "from these tickers: A, B, C" → use those reports only

Default scope when ambiguous: **all unprocessed reports under
`reports/company/`** (typically the largest backlog).

### Step 2 — List what's not yet in the graph

```bash
python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py
```

The script compares `reports/**/*.md` against the citation slugs already
present in `episodes.uuid`, and prints the unprocessed paths sorted by
mtime (newest first). It does not modify any DB.

### Step 3 — For each report

For each markdown file:

1. **Read it.** Use the `Read` tool. Long reports — read in chunks; you
   don't need to memorise every paragraph, only company / supplier /
   competitor / product mentions.

2. **Identify the focal company.** Almost always the subject of the
   report; the path gives it away (`reports/company/<Slug>/...`). Add it
   as an entity if not already present.

3. **Pull supporting companies** mentioned in:
   - "Competitive landscape" / "Competitors" section → `COMPETES_WITH`
     candidates
   - "Suppliers" / "Customers" / "Supply chain" / "Bill of materials" →
     `SUPPLIES` candidates (direction matters — see the decision tree)
   - Co-development partners, licensing partners → `SUPPLIES`
   - When the report frames a relationship through a branded product
     (e.g. "TSMC fabricates NVIDIA's H100"), do **not** add the product
     as a node — write the edge `TSMC SUPPLIES NVIDIA` and mention the
     product in the `fact` string instead.

4. **Cap at ~10 per entity.** If the focal company is a hub
   (Apple, NVIDIA, TSMC), you'll have more candidates than the budget
   allows. Pick the **10 most decision-relevant** — the relationships an
   investor would actually act on. Rules of thumb:
   - Direct cost of goods / revenue counterparty > brand association
   - Named in the report's competitive map > merely mentioned in passing
   - Distinct competitive dynamic > redundant (don't add 6 different EUV
     foundry competitors when 3 cover the strategic picture)

5. **Write via `manual_graph.py`.** See "Reference write pattern" below.

6. **Update todo list / move on.** Don't try to curate 50 reports in one
   sitting — quality drops. 5–15 reports per session is realistic.

### Step 4 — Verify

After each batch:

```python
import manual_graph
print(manual_graph.stats())
# {'entities': N, 'isolated': 0, 'edges': M, 'episodes': K}
```

Spot-check one new edge in the viewer (`/zep/` → search for the focal
company → confirm the new edges appear with the citation slug visible in
the tooltip).

## Reference write pattern

```python
from manual_graph import (
    add_entity, add_edge, add_episode, add_entities, add_edges, stats,
)

# 1. Register the report as the citation slug.
SRC = "NVDA_research_2026-06-02"
add_episode(SRC,
            name="NVIDIA (NASDAQ:NVDA) 公司研究 — 2026-06-02",
            source_desc="reports/company/Nvidia_NASDAQ_NVDA/Nvidia_NASDAQ_NVDA_公司研究.md")

# 2. Idempotently add entities. Existing ones aren't clobbered.
#    Every entity must carry labels=["Company"] — no other label is allowed.
add_entities([
    {"name": "NVIDIA",  "labels": ["Company"], "ticker": "NVDA",
     "summary": "Fabless GPU vendor; dominant in AI training silicon."},
    {"name": "TSMC",    "labels": ["Company"], "ticker": "TSM",
     "summary": "World's largest dedicated foundry; ~60%+ share by revenue."},
    {"name": "AMD",     "labels": ["Company"], "ticker": "AMD",
     "summary": "Fabless x86 / GPU vendor; primary NVIDIA competitor in AI accel."},
])

# 3. Edges. Each carries `source=` so the viewer can show provenance.
add_edges([
    {"src_name": "TSMC", "tgt_name": "NVIDIA",
     "relation": "SUPPLIES",
     "fact": "TSMC fabricates NVIDIA's H100 / Blackwell GPUs at N4 / N3.",
     "source": SRC},
    {"src_name": "AMD",  "tgt_name": "NVIDIA",
     "relation": "COMPETES_WITH",
     "fact": "AMD's MI300X / MI325X line is the only credible non-NVIDIA "
             "AI training accelerator from a US fab-light vendor.",
     "source": SRC},
])
```

**Idempotency.** `add_entity` is case-insensitive by name and never
clobbers a pre-existing summary. `add_episode` does
`INSERT OR REPLACE` on its slug. `add_edge` always creates a new row, so
**don't re-run the same batch** — the unprocessed-reports script exists
to prevent that.

## Reference materials

- [references/allowed_relations.md](references/allowed_relations.md) —
  the decision tree for picking `COMPETES_WITH` vs `SUPPLIES`, plus the
  mapping table for the deprecated minority types.
- [references/entity_quality.md](references/entity_quality.md) —
  what's an entity, what's not, with examples.
- [scripts/unprocessed_reports.py](scripts/unprocessed_reports.py) —
  finds reports not yet in `episodes`.
- [manual_graph.py](../../../manual_graph.py) (project root) — the actual
  write API. Open this file if you need to confirm a function signature
  or see how idempotency / casing is handled.
- [graph_mirror.py](../../../graph_mirror.py) (project root) — schema
  + read helpers + `deprecate_edge` / `isolate_entity` / `update_edge`
  for surgical fixes.

## What this skill is NOT for

- **Generating reports.** Use `company-research`, `compare-companies`,
  `sector-overview`, etc. — those produce the markdown that this skill
  later mines.
- **Wholesale wipe-and-rebuild.** If the user genuinely wants that, ask
  twice before touching the SQL.
- **Anything that needs the Claude API.** This skill never imports
  `claude_llm` or `anthropic`. It uses your own reasoning over `Read` +
  `manual_graph`.
