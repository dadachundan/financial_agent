# Entity quality rules

The single most important rule: **if in doubt, skip it.** A clean graph
with 200 entities beats a noisy graph with 2,000. The viewer is for the
user's thinking; every junk node makes it less useful.

## ALLOWED (extract these)

- **Public or private companies.** Use the canonical English / pinyin
  name. Add the ticker to the `ticker` field when known
  (`HKEX:1093`, `NASDAQ:NVDA`, `SSE:600519`).
  - Subsidiaries with their own brand / business: yes (e.g. `Cipla USA`).
  - Subsidiaries that are just a shell (e.g. `J.P. Morgan Securities
    Asia Limited`): no.

- **Stock tickers** that aren't otherwise the entity name. For US issuers
  the name and the ticker are usually different (`NVIDIA` vs `NVDA`), so
  it's enough to set `ticker="NVDA"` on the company entity — don't add
  `NVDA` as a separate entity. Same for HK / A-share: keep the company
  name as the canonical entity and stash the ticker on the row.

- **Branded products / platforms / chips / drug assets** when:
  1. They're material to the focal company's revenue or strategy.
  2. They're likely to recur in *other* reports — making the cross-link
     valuable.
  3. They have a real brand name (`H100`, `NBP`, `Synodex`,
     `YS2302018`, `Blackwell`). Not generic categories
     (`GPU`, `oncology drug`, `AI accelerator`).

- **Major business segments** that the company itself uses as a
  segment label (`Data Center`, `Gaming`, `Foundry`). Only add when
  the focal company reports it as a segment in 10-K / annual results.

- **Named indices** (`Hang Seng Index`, `S&P 500`) when the report
  discusses index inclusion / weighting changes. Otherwise skip.

## FORBIDDEN — never extract these

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
  a branded entity. Exception: index inclusion (`AI产业ETF`) where the
  whole name is the index identifier.

- **Generic financial concepts.** `oncology drug`, `bill of materials`,
  `OpEx`, `gross margin`, `convertible note`, `dividend`.

- **Countries / regions.** `China`, `United States`, `EU`, `Taiwan`,
  `Greater China`. They're scopes, not entities.

- **Government bodies and trade orgs.** `IRS`, `SEC`, `FDA`, `MIIT`,
  `WTO`, `IMF`, `OPEC`. These appear *in* reports but aren't subjects
  of investment analysis. The exception: when the report is
  specifically about a regulatory action (`FDA AdComm risk on X`), the
  regulator is a relevant node — but use the
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
  Chinese / Japanese / Korean entities:
  `CSPC Pharmaceutical Group` (English-first), `NBP (恩必普)`
  (Chinese product, parens hint), `BYD (比亚迪)` (parens hint).
  - Match the existing pattern in the graph. Look first — case-
    insensitive `find_entity()` will catch most overlap, but you want
    the spelling consistent.
  - Don't include the legal suffix (`Ltd`, `Inc.`, `Corp.`) unless that
    suffix is needed to disambiguate from a sibling entity (e.g. two
    Sany subsidiaries).

- **Branded products keep the brand prefix:** `Duomeisu (多美素)` not
  just `Duomeisu`. The parenthetical helps the viewer's FTS catch both
  language searches.

- **Pinyin first when the report is bilingual** so the entity is
  searchable from the English-side user (`Anpeilong (安培龙)`, not
  `安培龙`).

## Examples of the judgment call

| Mention in the report | Add as entity? | Why |
|---|---|---|
| "TSMC, the foundry that produces these chips, …" | Yes — TSMC | Core supplier |
| "Anpeilong's sales head, James Wu, told us …" | No — James Wu (person) | Anpeilong already; James is a human |
| "FY25 revenue of RMB 1.5bn" | No — RMB 1.5bn | Currency amount |
| "Our H100 line drives the data-center segment" | Yes — H100; Yes — Data Center | Brand product + named segment |
| "Hopper architecture" | Maybe | Brand if it shows up across multiple NVIDIA reports; skip if one-off |
| "TSMC's leading customer Apple" | Yes — Apple | Customer concentration matters |
| "the Securities and Exchange Commission" | No | Regulator scope |
| "auditor PwC" | No | Service provider boilerplate |
| "Microsoft's investment in OpenAI" | Yes — both | Material strategic relationship |
