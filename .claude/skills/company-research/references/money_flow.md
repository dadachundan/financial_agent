# Money-flow (supply-chain) diagram — `scripts/financial_charts.py moneyflow`

A 3-stage **"follow the dollars"** map in the dark gold-ribbon style: **who pays →
what they buy → where the money pools.** It answers, at a glance, the question a
financial-statement Sankey can't: *when this company spends (or earns), whose pockets
does the cash ultimately land in, and which one or two chokepoints catch most of it?*
The reader traces a gold ribbon from the payer, watches it fan out across the things
the company buys, then sees it **pool back onto a handful of upstream names** (a fab, a
memory maker, an equipment vendor, a raw-material chokepoint).

This is the diagram the user singled out as "very intuitive." **Generate one for every
company-research report** (Chinese always; English when bilingual) unless the company's
value chain genuinely can't be sourced (say so in the Step-10 log).

It is rendered as **stdlib-only inline SVG** by the same helper as the other charts
(`scripts/financial_charts.py`, imports just `math` / `json` / `argparse`, ~0 MB
resident — safe on the memory budget, never matplotlib). The SVG is **self-contained
and dark-themed** (it carries its own background), so it embeds cleanly inside the
otherwise-light markdown report and travels with it (screenshot / iframe / GitHub).

## Why a separate diagram (not just the cash-flow Sankey)

The `cashflow` Sankey decomposes the company's *own* statement (CFO → capex / FCF /
dividends). The money-flow map is **outward-looking**: it follows the company's COGS /
capex *out of the building* and onto its suppliers and their suppliers — the value
chain, not the income statement. It is **NOT flow-conserving**: ribbon thickness is
*rough relative scale* (the baked-in legend says so), because the underlying figures
aren't directly comparable (annual capex vs. multi-year contracts vs. a supplier's
reported revenue). Don't try to make the widths add up.

## Orientation — pick the one that illuminates the company

Two framings; choose per company (state which you chose in the prose intro):

- **Upstream / spend view (default for buyers & integrators — Tesla, Apple, an
  automaker, a hyperscaler):** Stage 1 = the company (and any sibling/peer that shares
  the spend) · Stage 2 = the key things it buys, grouped by category · Stage 3 = where
  that money ultimately pools (the deeper-tier suppliers / chokepoints). This is the
  Tesla reference.
- **Demand / revenue view (better for suppliers & component makers — a foundry, a
  sensor maker, a CDMO):** Stage 1 = the end customers / demand drivers paying in ·
  Stage 2 = the company & its product lines · Stage 3 = the company's own key suppliers
  (what *it* must buy to deliver). Shows the full pass-through chain.

Use **solid** ribbons for money paid **directly** and **dashed** ribbons for money that
reaches a name **indirectly, embedded in the price of a finished part** bought from
someone else (e.g. the HBM and TSMC wafers inside an Nvidia GPU). The legend explains
both automatically.

## CLI

```bash
python scripts/financial_charts.py moneyflow --spec spec.json   > /tmp/mf.svg
# or pipe the JSON in:
python scripts/financial_charts.py moneyflow --spec -           < spec.json
```

Flags: `--spec FILE` (or `-` for stdin, **required**), `--source` (overrides
`spec.source`; one of the two is **required**), `--title` (overrides `spec.title`),
`--note` (optional italic caption above the source footer), `--width` (default 1180).
Output goes to **stdout** — paste it into the report **un-fenced** (no ```` ``` ````),
blank line before and after, so the viewer renders it.

## JSON spec

```json
{
  "eyebrow": "Semiconductor money flow · 2026",
  "title": "How <Company> pays for its <inputs>",
  "thesis": "One or two sentences: the spend fans out, then pools onto a few names.",
  "stages": ["who pays", "what they buy", "where the money pools"],
  "nodes": [
    {"id": "co",   "stage": 0, "label": "COMPANY", "kind": "buyer",  "sub": ["one-line descriptor"], "h": 130},
    {"id": "gpu",  "stage": 1, "label": "NVIDIA",  "kind": "compute","sub": ["what / why it's bought"]},
    {"id": "fab",  "stage": 2, "label": "TSMC",    "kind": "foundry","sub": ["#1 foundry", "the chokepoint"]}
  ],
  "flows": [
    {"from": "co",  "to": "gpu", "weight": 26, "style": "direct",   "label": "$ billions / yr"},
    {"from": "gpu", "to": "fab", "weight": 14, "style": "embedded"}
  ],
  "source": "Exact, citable sources for the chain — same discipline as every chart footer."
}
```

**Node fields:** `id` (unique), `stage` (0-based column index), `label` (short, UPPERCASE
reads best), `sub` (list of short descriptor lines), `kind` (drives the accent colour &
legend chip), optional `h` (force a node height in px — otherwise text-driven), optional
`color` / `fill` (override the kind's accent / panel).

**Flow fields:** `from` / `to` (node ids; connect a stage to the next one), `weight`
(relative thickness — the largest in the chart maps to ~24px, others scale down), `style`
(`direct` = solid, `embedded` = dashed), optional `label` (drawn on the ribbon, e.g. a
deal size — must be citable).

**`kind` palette** (accent / legend label): `buyer` (red), `buyer2` (blue),
`compute` (cyan), `silicon`/`inhouse` (red — in-house silicon), `power` (amber —
power/analog), `rf` (blue — RF/wireless), `custom` (blue), `foundry` (green),
`memory` (purple), `neutral` (gold — generic supplier). Re-skin freely via `color`; the
names are a convenience, not a constraint — for a non-semi company use `neutral` plus a
custom `color` and a custom `legend`.

**`legend`** is auto-built (direct line, embedded dots, "thickness ≈ rough scale", and a
chip per `kind` present) — override with a `legend` array of
`{"type":"direct|embedded|scale|chip","label":"…","kind":"…"}` when the auto labels
don't fit the domain.

A full worked spec — the Tesla/SpaceX reference reproduced — is committed at
[`money_flow_example.json`](money_flow_example.json) next to this doc. Copy it, swap in
your company's nodes/flows, and render:

```bash
python scripts/financial_charts.py moneyflow \
  --spec .claude/skills/company-research/references/money_flow_example.json > /tmp/mf.svg
```

## Sourcing discipline (load-bearing — the same rules as every other chart)

1. **Every node must be a REAL counterpart you sourced** — the company's named
   suppliers/customers from its 10-K / 20-F / 年度报告 (supplier & customer notes,
   risk-factor concentration language), IR decks, teardown / channel reports, or the
   local zsxq broker library. **Do not invent a plausible-looking supplier.** If you
   can't source a tier-3 chokepoint, leave that ribbon/node out.
2. **Any `$` figure in a ribbon `label` must string-match a source cited in the
   surrounding paragraph** (e.g. "AI6 fab · $16.5B" → the paragraph cites the deal
   announcement that contains "$16.5B"). Ribbon labels are claims, held to the same
   number→URL standard as prose.
3. **Thickness is explicitly rough relative scale, not dollars** — the legend says so,
   so widths need no per-ribbon citation, but the *relative ordering* must be
   defensible from what you read (don't draw Micron thicker than TSMC if the sources
   say the opposite).
4. **`--source` / `spec.source` is REQUIRED and baked into the SVG footer**, per the
   project chart rule (the source travels inside the image). Cite the actual chain
   sources, not a homepage.
5. **The surrounding report paragraph still carries inline page-level citations** for
   the supply-chain narrative the diagram visualizes — the baked-in footer is a backup,
   not a substitute. Write a short "follow the money" paragraph beneath the diagram that
   names the chokepoint(s) and cites each link.

## Placement

**Section 4 (Products & Services)** — as the supply-chain / bill-of-materials anchor
("what it takes to build the product, and whose pocket the cash lands in"), or **Section
6 (Industry Overview)** as the value-chain-position visual when the chain is more an
industry story than a product story. One diagram per report; put it wherever the supply
chain is actually discussed. Caption it with a markdown-link citation like every other
chart.

## Embedding form

Paste the emitted `<svg>` **un-fenced**, blank line before and after, then a one-line
caption + the short sourced "follow the money" paragraph:

```
<svg ...> … </svg>

*图 X：<Company> 的"资金流向"价值链图 — 实线为直接付款，虚线为隐含在成品芯片中的间接支出。* Source: [<deal/filing>](URL)
```
