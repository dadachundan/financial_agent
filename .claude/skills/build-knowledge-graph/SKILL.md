---
name: build-knowledge-graph
description: Mine entities and relationships from research reports under reports/ and write them directly into db/graph_mirror.db via manual_graph.py. Use when the user asks to "update the knowledge graph", "mine relations from reports", "build the graph", "ingest these reports into /zep/", "rebuild the graph from reports/", or anything in that family. The agent (Claude in conversation) reads the sources and curates — there is no LLM API call, ever. Honours the project-wide "NEVER call the Claude API" rule from CLAUDE.md.
---

# Build Knowledge Graph

Mine high-quality entities and edges from research markdown under `reports/`
and write them directly into the SQLite store at `db/graph_mirror.db`. The
viewer at `http://xs-macbook-air.local:5001/zep/` reads from that file, so
additions show up on browser refresh. (Any `/zep/` URL echoed to the user
must use the `xs-macbook-air.local` host, never `localhost` — and per
`feedback_no_server_reminder`, don't end a run with "refresh /zep/ to see
the changes"; just report the deltas.)

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

Run all snippets with `/opt/anaconda3/bin/python3` (per
`feedback_anaconda_python_db_scripts` — bare `python3` has failed
read-only DB opens in some shells).

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

These five rules are non-negotiable. They are why this skill exists.

1. **Allowed relation types: `COMPETES_WITH` and `SUPPLIES` only.**
   The graph has 5 stray minority types (12 edges, as of 2026-06-02) from
   earlier ad-hoc curation. Don't add new edges with any other relation name.
   - `MAKES`, `DEVELOPED`, `IS_COMPONENT_OF` → **map to `SUPPLIES`** when
     ingesting new reports (product is supplied by its maker).
   - `OUT_LICENSED_TO`, `LICENSED` → **map to `SUPPLIES`** for new edges
     (licensor "supplies" the IP / drug asset to the licensee).
   - See [references/allowed_relations.md](references/allowed_relations.md)
     for the decision tree.

2. **Tiered edge cap: ≤ 10 active edges per entity, ≤ 25 for >$1T
   mega-caps.** Quality > coverage. The mega-cap exception (user decision
   2026-06-11): a company whose **live market cap exceeds $1T USD** gets a
   cap of 25, because trillion-dollar hubs genuinely carry more
   decision-relevant relationships. Everything else — including unlisted
   companies (Huawei, SpaceX: no market cap → standard tier) — is capped
   at 10. Determine the tier at curation time via the Tier-2 helper:
   ```python
   from market_cap_cache import get_market_caps, to_usd
   mc, cur = get_market_caps(["NASDAQ:NVDA"])["NASDAQ:NVDA"]
   cap = 25 if (to_usd(mc, cur) or 0) > 1e12 else 10
   ```
   Don't churn on borderline drift (SK Hynix was $0.98T, Micron $1.01T on
   2026-06-11): reclassify an already-curated entity only when its cap
   clearly crosses the line (>10% beyond $1T either way).

   Before writing an edge whose source or target is at its cap, drop the
   *least decision-relevant* existing edge for that entity first
   (`deprecate_edge(..., reason="EDGE_BUDGET")` — soft, reversible).
   Never leave an entity above its cap. Pre-check counts with:
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
   The legacy pre-cap hubs were brought under this tiered policy on
   2026-06-11 (NVIDIA 41→25; BYD/SK Hynix/AMAT/Xpeng/AMD pruned to 10)
   via a rank-and-prune pass with adversarial verification — pruned edges
   carry `deprecated_reason="EDGE_BUDGET"` and can be resurrected.

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

5. **One entity per company — fragment-search before every `add_entity`.**
   Duplicate rows ("SKHynix" vs "SK Hynix", "Meta" vs "Meta Platforms",
   "Moons" vs "Mingzhi (鸣志电器)") split edges across two nodes and defeat
   the edge cap — a 2026-06-11 critic pass had to merge **29** such pairs.
   `add_entity` only matches the *exact* name case-insensitively; it will
   NOT catch spelling variants. Before creating, search by English
   fragment, Chinese fragment, AND ticker:
   ```python
   c.execute("SELECT name, ticker FROM entities WHERE name LIKE ? OR ticker LIKE ?",
             (f"%{frag}%", f"%{frag}%")).fetchall()
   ```
   Reuse the EXACT existing name in edges. Dual-listed companies
   (A-share + HKEX, ADR + home listing) are ONE entity. If a duplicate
   pair is discovered after the fact, merge with
   `graph_mirror.merge_entities(conn, source_uuid, target_uuid)` (re-points
   all edges, deletes the source row), then deprecate any identical
   (src, tgt, relation) edges the merge exposes.

## Workflow

### Step 1 — Pick the scope

Ask the user (or infer from their phrasing) what they want covered:

- "update the knowledge graph" → take the *newest unprocessed* reports
  (use `scripts/unprocessed_reports.py` to list them)
- "mine relations from reports/company/X" → that specific folder
- "rebuild the graph" → don't. Run `manual_graph.stats()` first and quote
  the live counts back to the user — hundreds of hand-curated entities /
  edges are at stake (448 entities / 761 active edges / 259 episodes as of
  2026-06-11, and growing); never wipe without explicit per-table
  instructions
- "from these tickers: A, B, C" → use those reports only

Default scope when ambiguous: **all unprocessed reports under
`reports/company/`** (typically the largest backlog).

### Step 2 — List what's not yet in the graph

```bash
python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py
python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py --subdir company --limit 20
python3 .claude/skills/build-knowledge-graph/scripts/unprocessed_reports.py --json    # machine-readable
```

The script compares `reports/**/*.md` against the **company folder**
(or single-file stem) of each `episodes.source_desc` row in the mirror,
and prints what's not yet covered, sorted by mtime (newest first).
Curating one canonical .md per company covers the EN + ZH companion
files automatically — they share the same folder. For single-file
reports (themes / compare / sector / earnings) the script normalizes
companion suffixes (`_zh`, `_CN`, `_theme`, `_主题研究`) on both sides,
so mining `memory-upcycle_theme.md` also marks
`memory-upcycle_主题研究.md` as covered. The script never modifies
any DB.

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

4. **Cap at ~10 per entity (25 for >$1T mega-caps — see hard
   constraint #2).** If the focal company is a hub (Apple, NVIDIA, TSMC),
   you'll have more candidates than the budget allows. Pick the **most
   decision-relevant within the cap** — the relationships an investor
   would actually act on. Rules of thumb:
   - Direct cost of goods / revenue counterparty > brand association
   - Named in the report's competitive map > merely mentioned in passing
   - Distinct competitive dynamic > redundant (don't add 6 different EUV
     foundry competitors when 3 cover the strategic picture)

5. **Write via `manual_graph.py`.** See "Reference write pattern" below.

6. **Update todo list / move on.** Don't try to curate 50 reports in one
   sitting — quality drops. 5–15 reports per session is realistic **in the
   main thread**. For a larger batch (validated 2026-06-11: 49 reports),
   fan out `Agent`-tool subagents, each owning a *cluster of 5–10 related
   reports* (same sector — they share counterparties, so dedup decisions
   stay coherent), and run the clusters **strictly sequentially, one
   subagent at a time**: concurrent writers race the ≤10-edge-cap check
   and contend on the SQLite file, and the 16 GB box can't fit two heavy
   agents anyway. Each subagent prompt must restate the five hard
   constraints plus the cap/dedup pre-check SQL, and must return a
   structured summary (episodes / entities added / edges added / skipped
   + reasons / anomalies) for the critic pass.

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

### Step 5 — Critic review (mandatory after any multi-report batch)

Spawn an **independent critic agent** (`Agent` tool, general-purpose) that
did not write the edges. Give it the batch's episode slugs (edges carry
them in `edges.episodes_json` — a JSON array; non-ASCII slugs are stored
unicode-escaped, so `json.loads` each row rather than `LIKE`-matching).
First thing it does: `cp db/graph_mirror.db /tmp/graph_mirror_backup_pre_critic.db`.
It may only modify the DB via the sanctioned helpers
(`graph_mirror.deprecate_edge` / `update_edge` / `merge_entities` /
`isolate_entity`); SELECTs are unrestricted. Its checklist:

1. **Relation whitelist** — every new edge is exactly `COMPETES_WITH` or
   `SUPPLIES`; anything else → `deprecate_edge(..., reason="RELATION_NOT_ALLOWED")`.
2. **SUPPLIES direction** — supplier/licensor/manufacturer → customer/
   licensee. Verify suspicious ones against the source report before
   deprecating.
3. **Entity quality** — endpoints are companies only; a non-company that
   slipped in → `isolate_entity` + deprecate its edges (`"ENTITY_QUALITY"`).
4. **Duplicates** — identical (src, tgt, relation) rows, or both directions
   of a symmetric `COMPETES_WITH` pair → keep the richer fact, deprecate
   the other (`"DUPLICATE"`).
5. **Fact spot-check (hallucination audit)** — sample ≥20 new edges across
   all clusters, open each source report, confirm the counterparty really
   appears there; fabrications → deprecate (`"FACT_NOT_IN_SOURCE"`).
6. **Duplicate entities** — same ticker under two spellings →
   `merge_entities` keeping the better-connected / canonical name, then
   re-dedupe, and trim any entity the merge pushed over its tiered cap
   (10, or 25 for >$1T mega-caps — see hard constraint #2;
   `"EDGE_BUDGET"` — weakest facts lose).

Calibration from the 2026-06-11 run (49 reports, 246 new edges): 0 relation
violations, 0 direction errors, 0 fabrications in 34 samples — but 29
duplicate entity pairs and ~40 duplicate/stub edges. The critic pass earns
its cost mostly on **entity hygiene**, so don't skip item 6.

## Reference write pattern

### Citation-slug convention

Reports in `reports/company/<Folder>/...` always have one folder per
company. Both the EN file (`<Folder>_Research_Document.md`) and the ZH
file (`<Folder>_公司研究.md` or `<Folder>_Research_Document_zh.md`) live
inside it; the underlying research is identical.

**The slug IS the company folder name.** No dates, no abbreviations.

| Report path | Slug |
|---|---|
| `reports/company/NVIDIA_NASDAQ_NVDA/NVIDIA_NASDAQ_NVDA_公司研究.md` | `NVIDIA_NASDAQ_NVDA` |
| `reports/company/CSPC_石药集团_HKEX1093/...` | `CSPC_石药集团_HKEX1093` |
| `reports/company/BYD_比亚迪_HKEX1211/...` | `BYD_比亚迪_HKEX1211` |
| `reports/sector/半导体材料.md` | `sector_半导体材料` |
| `reports/compare/SNPS_vs_CDNS.md` | `compare_SNPS_vs_CDNS` |
| `reports/earnings/QCOM.md` | `earnings_QCOM` |
| a zsxq PDF (`db/zsxq.db`, file_id `N`) | `pdf_<file_id>` |

For single-file reports (sector/compare/earnings/themes) prefix with the
subdirectory so slugs don't collide with company names.

For zsxq-PDF-derived edges use
`add_episode("pdf_<file_id>", name="<PDF title>", source_desc="zsxq #<file_id>")`
— the convention [[zsxq-expert]] Step 6 writes. `graph_mirror._episode_url`
special-cases the `pdf_` prefix so the episode renders as a clickable PDF
link in `/zep/`. Keep this format exactly; don't invent ad-hoc slugs for
PDF sources.

Derive the slug deterministically from the path:

```python
from pathlib import Path

def slug_for(rel_path: str) -> str:
    parts = Path(rel_path).parts
    if len(parts) >= 3 and parts[0] == "reports" and parts[1] == "company":
        return parts[2]                       # company folder name
    if len(parts) >= 2 and parts[0] == "reports":
        return f"{parts[1]}_{Path(rel_path).stem}"
    return Path(rel_path).stem
```

### Example: NVIDIA

```python
from manual_graph import (
    add_entity, add_edge, add_episode, add_entities, add_edges, stats,
)

# 1. Register the report. SLUG = the company folder name. SOURCE_DESC = the
#    project-relative path to the canonical .md (the one you actually read).
SRC = "NVIDIA_NASDAQ_NVDA"
add_episode(
    SRC,
    name="NVIDIA (NASDAQ:NVDA) — Research Document",
    source_desc="reports/company/NVIDIA_NASDAQ_NVDA/NVIDIA_NASDAQ_NVDA_公司研究.md",
)

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
clobbers a pre-existing summary. `add_episode` does `INSERT OR REPLACE`
on its slug (so re-running with the same `SRC` is safe). `add_edge`
always creates a new row, so **don't re-run the same edge batch** — the
`unprocessed_reports.py` script exists to prevent that. If you discover
a duplicate edge after the fact, soft-delete it with
`graph_mirror.deprecate_edge(conn, edge_uuid, reason="DUPLICATE")`.

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
  + read helpers + `deprecate_edge` / `isolate_entity` / `update_edge` /
  `merge_entities` for surgical fixes.

## What this skill is NOT for

- **Generating reports.** Use `company-research`, `compare-companies`,
  `sector-overview`, etc. — those produce the markdown that this skill
  later mines.
- **Wholesale wipe-and-rebuild.** If the user genuinely wants that, ask
  twice before touching the SQL.
- **Anything that needs the Claude API.** This skill never imports
  `claude_llm` or `anthropic`. It uses your own reasoning over `Read` +
  `manual_graph`.
