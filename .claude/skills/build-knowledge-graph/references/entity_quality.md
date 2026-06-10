# Entity quality rules

The single most important rule: **if in doubt, skip it.** A clean graph
with 200 entities beats a noisy graph with 2,000. The viewer is for the
user's thinking; every junk node makes it less useful.

## ONE allowed entity type: `Company`

Every entity in the graph carries `labels=["Company"]`. Public or private,
listed or unlisted, parent or subsidiary — but it must be a *company*.
No other label is accepted (`Product`, `Index`, `Segment`, `Person`,
`Country` are all forbidden — see below).

The user tightened this rule on **2026-06-02** after the initial pass had
added 6 products + 1 index alongside companies. Those 7 entities are
isolated; the graph is now 100% companies.

### What counts as a Company

- **Public companies.** Use the canonical English / pinyin name and set
  the `ticker` field (`HKEX:1093`, `NASDAQ:NVDA`, `SSE:600519`). For US
  issuers don't add the ticker as a separate entity — keep it on the
  company row.

- **Private companies.** Same idea, no ticker. Examples:
  `Databricks`, `OpenAI`, `Anthropic`, `MiniMax AI`, `Bytedance`,
  `SHEIN`, `Aramco` (pre-IPO).

- **Sovereign-wealth / fund-style entities** when they're an active
  transactional party in the report (e.g. `Berkshire Hathaway`,
  `Mubadala`, `SoftBank Vision Fund`). They behave like companies in the
  graph — they buy, sell, supply capital, compete for deals.

- **Subsidiaries with their own brand / business**: yes
  (`Cipla USA`, `Foxconn Industrial Internet`). Subsidiaries that are
  just a legal shell (`J.P. Morgan Securities Asia Limited`): no.

## FORBIDDEN — never extract these

- **Branded products / platforms / chips / drug assets.** Even
  high-profile ones (`H100`, `Blackwell`, `NBP`, `YS2302018`). When the
  report describes a product, encode the relationship between the maker
  and the customer / partner instead: `TSMC SUPPLIES NVIDIA` with the
  product mentioned in the `fact` string.

- **Stock tickers as standalone entities.** Set `ticker="NVDA"` on the
  NVIDIA row, don't add `NVDA` as its own node.

- **Indices.** `Hang Seng Index`, `S&P 500`, `MSCI EM` — not companies.
  Index membership goes in the company's `summary`, not as an edge.

- **Business segments** of a company. `Data Center`, `Gaming`,
  `Foundry`. The segment exists *inside* the company; it doesn't
  warrant its own node.

- **Human person names.** Ever. No CEO names, no CFO names, no analyst
  names, no author names, no board members, no founders, no
  politicians, no judges, no expert witnesses. Even if the person is
  central to the report ("Jensen Huang's keynote"), extract NVIDIA, not
  Jensen Huang.

- **Dollar / currency amounts.** `$5.2bn`, `RMB 26.0bn`,
  `US$100m upfront`, `$15 / share`. Strings that start with `$` or
  contain a number plus a unit. Never an entity.

- **Generic technology categories.** `AI`, `GPU`, `LLM`, `cloud`,
  `quantum`, `EUV`, `5G`, `HBM`. These describe a *class* of thing, not
  a branded entity.

- **Generic financial concepts.** `oncology drug`, `bill of materials`,
  `OpEx`, `gross margin`, `convertible note`, `dividend`.

- **Countries / regions.** `China`, `United States`, `EU`, `Taiwan`,
  `Greater China`. They're scopes, not entities.

- **Government bodies and trade orgs.** `IRS`, `SEC`, `FDA`, `MIIT`,
  `WTO`, `IMF`, `OPEC`. These appear *in* reports but aren't subjects
  of investment analysis. The exception: when the report is
  specifically about a regulatory action (`FDA AdComm risk on X`), the
  regulator is a relevant scope — but use the
  `regulatory-risk-monitor` skill for that, not this one.

- **Legal / accounting framework names.** `GAAP`, `IFRS`, `Sarbanes-
  Oxley`, `Reg FD`, `Rule 10b-5`, `Form 10-K`.

- **Generic time periods.** `Q1 2025`, `FY24`, `2026 outlook`.

- **Deal / transaction labels.** `Merger Agreement`,
  `OxyChem Transaction`, `Series C round`. These name an event, not a
  company.

- **Disclaimer-page broker subsidiaries.** Pattern:
  `<Bank> <Country/City> <Securities|Capital|Brokerage> Ltd`. They
  appear *only* in the legal disclosure footer and are noise. Examples:
  `UBS Securities Australia Ltd`, `Macquarie Capital (USA) Inc.`.

- **Vague or single-use product mentions.** A widget that's mentioned
  once in passing with no buyer / supplier / competitor context. If the
  product doesn't connect to at least one other entity in the report,
  it doesn't earn a node.

## Naming conventions

- **Use the form the report uses, plus a parenthetical translation** for
  Chinese / Japanese / Korean companies:
  `CSPC Pharmaceutical Group` (English-first), `BYD (比亚迪)` (parens
  hint for the Chinese name).
  - Match the existing pattern in the graph. Look first — case-
    insensitive `find_entity()` will catch most overlap, but you want
    the spelling consistent.
  - Don't include the legal suffix (`Ltd`, `Inc.`, `Corp.`) unless that
    suffix is needed to disambiguate from a sibling entity (e.g. two
    Sany subsidiaries).

- **Pinyin first when the report is bilingual** so the entity is
  searchable from the English-side user (`Anpeilong (安培龙)`, not
  `安培龙`).

## Examples of the judgment call

| Mention in the report | Add as entity? | Why |
|---|---|---|
| "TSMC, the foundry that produces these chips, …" | Yes — TSMC | Core supplier (Company) |
| "Anpeilong's sales head, James Wu, told us …" | No — James Wu (person) | Anpeilong already; James is a human |
| "FY25 revenue of RMB 1.5bn" | No — RMB 1.5bn | Currency amount |
| "Our H100 line drives the data-center segment" | No — H100 / Data Center | Products + segments banned; capture as `NVIDIA SUPPLIES <buyer>` |
| "Hopper architecture" | No | Product family — not a Company |
| "TSMC's leading customer Apple" | Yes — Apple | Customer concentration (Company) |
| "the Securities and Exchange Commission" | No | Regulator scope |
| "auditor PwC" | Maybe | PwC is a real company; add only if the report's thesis touches on auditing risk (otherwise skip — service-provider noise) |
| "Microsoft's investment in OpenAI" | Yes — both | Both are companies; material strategic relationship |
| "Hang Seng Index inclusion in 2018" | No — write it into CSPC's summary instead | Index ≠ Company |
