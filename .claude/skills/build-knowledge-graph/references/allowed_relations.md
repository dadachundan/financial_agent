# Allowed relation types

Only two. Don't invent new ones.

## `COMPETES_WITH`

Two companies sell substitutable products into overlapping customer
segments. The edge is **directional but mostly symmetric** — write one
edge in each direction only when the competitive dynamic is genuinely
asymmetric (e.g. a small challenger targeting a dominant incumbent's
weak segment), otherwise one edge is enough.

**Examples:**

- AMD `COMPETES_WITH` NVIDIA (AI accelerators)
- TSMC `COMPETES_WITH` Samsung Foundry (leading-edge foundry)
- LiAuto `COMPETES_WITH` XPeng (China NEV mid-market)
- ASML `COMPETES_WITH` Nikon (EUV lithography — even though Nikon doesn't
  have EUV, the lithography market is the competitive scope)

**Not `COMPETES_WITH`:**

- Apple `COMPETES_WITH` TSMC — they're customer / supplier, not competitors
- NVIDIA `COMPETES_WITH` PyTorch — different layers (silicon vs framework)
- Microsoft `COMPETES_WITH` OpenAI — equity stake plus partnership

## `SUPPLIES`

Source supplies target with goods, services, components, IP, or capacity.
**Direction: src → tgt = "src supplies tgt".** Always write the edge so
the supplier is `src_name` and the buyer / licensee / downstream
incorporator is `tgt_name`.

**Examples:**

- TSMC `SUPPLIES` NVIDIA (wafers)
- ASML `SUPPLIES` TSMC (EUV scanners)
- SK Hynix `SUPPLIES` NVIDIA (HBM3E for H100)
- CSPC `SUPPLIES` AstraZeneca (out-licensed Lp(a) drug asset to AZ;
  fact text mentions YS2302018 — the asset itself is *not* a node)
- Foxconn `SUPPLIES` Apple (iPhone assembly)
- NVIDIA `SUPPLIES` Microsoft (H100 → Azure capacity)

**Products are not nodes.** Per the entity-quality rule the graph holds
only companies. When the report frames a supply relationship through a
branded product, write the edge company-to-company and mention the
product in the `fact` string. Example:

```python
add_edge("TSMC", "NVIDIA",
         relation="SUPPLIES",
         fact="TSMC fabricates NVIDIA's H100 and Blackwell GPUs at N4 / N3.",
         source="NVDA_research_2026-06-02")
```

Never add `H100` or `Blackwell` themselves as entities.

## Mapping the deprecated minority types

When you encounter a fact that *would* have used one of the old types in
the existing graph, map it as follows:

| Old type | Replace with | Notes |
|---|---|---|
| `MAKES` | `SUPPLIES` | Maker supplies the product. |
| `DEVELOPED` | `SUPPLIES` | Company "supplies" the IP / asset / product. |
| `IS_COMPONENT_OF` | `SUPPLIES` | Reverse the direction: component supplier → assembly maker. |
| `OUT_LICENSED_TO` | `SUPPLIES` | Licensor → licensee. The licensor "supplies" the asset / drug / patent. |
| `LICENSED` | `SUPPLIES` | Same direction as above. |

Don't go back and rewrite the 12 existing edges with minority types —
they're locked in and visible in the viewer with their original labels.
Just don't create new edges with those names.

## Edge cases

- **Joint venture.** Both parties supply something to the JV; the JV
  itself is usually not an entity worth adding. Capture as
  `partnerA SUPPLIES partnerB` if and only if the report describes a
  material asset flow (e.g. one side contributes the tech, the other the
  distribution).

- **Acquisition.** "X acquired Y" doesn't fit `COMPETES_WITH` or
  `SUPPLIES`. Either skip the edge (the entity merge will dominate
  anyway) or, if the acquired entity stays operational as a subsidiary,
  add the supply relationship if applicable
  (`parent SUPPLIES sub`-managed product to external customers).
  Don't invent an `ACQUIRED` edge.

- **Indirect competition through ecosystems.** "Android competes with
  iOS" — yes if the report frames them head-to-head; no if it's a passing
  mention.

- **Customer concentration disclosed in a 10-K.** "Apple was 21% of
  revenue" → `focal SUPPLIES Apple`. The directionality follows the
  cash flow: supplier (focal) → buyer (Apple).
