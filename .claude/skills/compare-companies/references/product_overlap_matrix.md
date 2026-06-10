# Product Overlap Matrix — How to Build It

The product overlap matrix is the single most-cited table in the final report. Readers paste it into competitive-positioning decks. Build it carefully and exhaustively. The matrix's job is to answer the reader's first question — **do their products actually compete, or are they more complementary?** — at a glance.

## The bucket classification (N=2)

For binary comparisons, every paired product row resolves to exactly one of four buckets:

| Bucket | Definition | When to use |
|---|---|---|
| **DIRECTLY COMPETE** | Both products solve the same customer problem at the same point in the customer's workflow; customers treat them as substitutes; a customer typically buys one or the other (not both for the same project). | The two products show up in the same RFP. Both are "tool of record" candidates for the same job. |
| **DIRECTLY COMPETE (X dominant)** | Same as above, but one side has clear share leadership per a third-party source, *and* the other side ships a competitive product that occasionally displaces. | The category has a clear #1 but the #2 is still meaningfully in market. Examples: Virtuoso (CDNS) vs Custom Compiler (SNPS) in custom analog. |
| **COMPLEMENTARY** | Both sides ship something in the category, but one side has only a token / under-invested offering; the other is the obvious choice; customers rarely RFP both. | The product exists in both portfolios but the comparison is degenerate. The minority side may continue to ship for portfolio-completeness reasons. |
| **NON-OVERLAPPING** | One side does not meaningfully ship in this category. | TCAD (SNPS Sentaurus) has no CDNS counterpart. PCB (CDNS Allegro X) has no SNPS counterpart of any substance. |

Avoid an "unclear" or "mixed" bucket — every row picks one. If you can't classify it, you haven't done the research.

## The status grammar (N=3 or N=4)

For three- or four-way comparisons, the binary buckets aren't expressive enough — direct-compete-ness varies by pair. Use this grammar in the Status column:

| Status phrasing | Meaning | When to use |
|---|---|---|
| **ALL THREE COMPETE** / **ALL FOUR COMPETE** | Every side in the focal set ships in this category and customers treat them as substitutes. | Cloud data warehouse: Databricks SQL vs Snowflake vs Oracle ADW — all three present, all three pitched at the same buyer. |
| **ALL N COMPETE (X dominant)** | Every side ships; one is clearly #1 per a third-party source. | "ALL THREE COMPETE (SNOW dominant — Gartner CDW MQ leader)" — every side ships data-warehouse SQL, SNOW is the clear leader. |
| **A vs B compete; C absent** / **A and C compete; B absent** | Some sides ship, others don't — spell out which by letter. | Lakehouse / open-format engine: Databricks vs Snowflake compete (both ship Iceberg); Oracle has no meaningful equivalent. |
| **COMPLEMENTARY (X leads)** | Multiple sides ship but only one is the real choice. | "COMPLEMENTARY (ORCL leads)" — for enterprise apps, ORCL Fusion vs Databricks/Snowflake (both have light app offerings but the choice is ORCL). |
| **NON-OVERLAPPING (X only)** | Exactly one side ships; structural asymmetry. | Traditional RDBMS / OLTP: only Oracle ships (DBX and SNOW don't compete here). |

**Critical N-way discipline:**

- **Spell out which sides are absent** by letter (A, B, C, D) so the row is self-explanatory; never just "some compete, others don't".
- **The status cell should fit on one line in a wide table.** If it runs to two lines, you've added editorial that belongs in the prose paragraphs after the matrix.
- **At least one row per status type.** A 3-way matrix where every row says `ALL THREE COMPETE` is under-explored — every multi-segment industry has at least one row that is `A vs B compete; C absent` (the strategic asymmetry).

## Sourcing rules

Every row needs:

1. **Vendor product page for each side** (deep URL, not the homepage). If the company has a product matrix page in their 10-K Item 1 Business, that's the gold standard — cite it; for company website pages, cite the specific product page.
2. **Third-party share / leadership source** if classifying as "X dominant" — IPnest, Gartner, IDC, IBISWorld, SemiAnalysis, TrendForce, EvaluatePharma, IQVIA, etc. **Never cite the company's own 10-K for a share-leadership claim** (the 10-K never says "we lead"). If you can't find a third-party source, classify as DIRECTLY COMPETE without the "(X dominant)" qualifier.
3. **A specific customer-side example** if classifying as COMPLEMENTARY — name a customer or trade-press source that says they buy one and not the other.

## How to discover product pairs

For each side, walk the corporate website's `Products / Solutions / Platforms` navigation tree exhaustively. Aim for **20–40 product line items per side** for a mid-size industrial / software company. Smaller for single-product startups.

For each product, capture:
- Official product name (with trademark symbols, capitalization conventions: `ALTUS®`, not `Altus`)
- One-sentence vendor-supplied description
- The "verb + noun" of what it physically does for the customer

Then pair across sides. The pairing is the analyst's judgement; bias toward over-pairing (it's easier to demote a row to COMPLEMENTARY than to realize you missed an entire category).

## Format

A single markdown table per major product axis. For multi-axis companies (e.g. EDA + IP + SD&A; or Lakehouse + AI/ML + Apps), one table per axis. **N=2 uses 4 columns (Category / A's product / B's product / Status); N=3 uses 5; N=4 uses 6.**

**N=3 worked example — Databricks vs Snowflake vs Oracle (data + AI platforms):**

```markdown
### Product overlap — analytics & AI platforms

| Function | Databricks | Snowflake | Oracle | Status |
|---|---|---|---|---|
| Cloud data warehouse (SQL-first) | Databricks SQL | Snowflake Data Cloud | Autonomous Data Warehouse + HeatWave | ALL THREE COMPETE (SNOW dominant per Gartner CDW MQ 2025) |
| Lakehouse on open formats | Lakehouse Platform + Delta + Iceberg | Snowflake Iceberg Tables (GA) | — | DBX vs SNOW compete; ORCL absent |
| Streaming ingestion | Delta Live Tables / DLT | Snowpipe / Dynamic Tables | OCI GoldenGate + Streaming | ALL THREE COMPETE |
| AI/ML lifecycle | Mosaic AI (training, fine-tune, serve) | Cortex (LLM + ML) | OCI AI Services / OCI Gen AI | ALL THREE COMPETE (DBX dominant for fine-tuning per Forrester AI Wave) |
| Traditional RDBMS / OLTP | — | — | Oracle Database 23ai | NON-OVERLAPPING (ORCL only) |
| Enterprise apps (ERP/HCM/CX) | — | — | Oracle Fusion Applications | NON-OVERLAPPING (ORCL only) |
| Native marketplace | Databricks Marketplace | Snowflake Marketplace | OCI Marketplace | ALL THREE COMPETE (SNOW dominant — first mover, deepest catalog) |
| Notebook IDE | Databricks Notebooks | Snowflake Notebooks (GA 2024) | OCI Data Science Notebooks | ALL THREE COMPETE (DBX dominant — Jupyter-native incumbent) |
| Catalog / governance | Unity Catalog | Horizon | OCI Data Catalog | ALL THREE COMPETE |
| BYOC / on-prem | — | — | Cloud@Customer + Exadata | NON-OVERLAPPING (ORCL only — uniquely on-prem-friendly) |
```

The above is a 5-column matrix for N=3. The pattern shows DBX and SNOW converging while ORCL covers an adjacent surface area (OLTP, apps, on-prem) that the other two don't touch.

**N=2 worked example — Synopsys vs Cadence (EDA core tools):**

```markdown
### Product overlap — EDA core tools

| Function | Synopsys product | Cadence product | Status |
|---|---|---|---|
| Static-timing signoff | PrimeTime | Tempus | DIRECTLY COMPETE (SNPS dominant — ~90% share per SemiAnalysis) |
| Logic synthesis | Design Compiler / Fusion Compiler | Genus | DIRECTLY COMPETE (SNPS dominant — ~84–85% share per SemiAnalysis) |
| Place-and-route | Fusion Compiler | Innovus | DIRECTLY COMPETE |
| Custom-analog layout | Custom Compiler | Virtuoso | DIRECTLY COMPETE (CDNS dominant — ~80%+ share per Gartner 2003, not refreshed) |
| Functional verification | VCS | Xcelium | DIRECTLY COMPETE |
| Hardware emulation | ZeBu | Palladium | DIRECTLY COMPETE (CDNS dominant per trade press) |
| FPGA prototyping | HAPS | Protium | DIRECTLY COMPETE |
| Physical verification (DRC/LVS) | IC Validator | Pegasus | DIRECTLY COMPETE (both behind Siemens Calibre ~85% — not the leader) |
| AI-driven implementation | DSO.ai / Synopsys.ai | Cerebrus / JedAI | DIRECTLY COMPETE |
| Multi-die / 3D-IC | 3DIC Compiler | Integrity 3D-IC | DIRECTLY COMPETE |
| TCAD (process simulation) | Sentaurus | — | NON-OVERLAPPING (SNPS only) |
| Photonics design | OptoCompiler | — | NON-OVERLAPPING (SNPS only, light footprint) |
| Enterprise PCB | (none of substance) | Allegro X | NON-OVERLAPPING (CDNS only) |
| Mainstream PCB | (none) | OrCAD X | NON-OVERLAPPING (CDNS only) |

### Product overlap — IP

| IP category | Synopsys | Cadence | Status |
|---|---|---|---|
| Interface IP (PCIe, USB, DDR, HBM, SerDes, UCIe, Ethernet) | DesignWare interface IP | Cadence IP | DIRECTLY COMPETE (SNPS dominant — >55% share per IPnest 2024) |
| Processor IP — CPU | ARC (divesting to GF, close 2H 2026) | — | NON-OVERLAPPING (Arm and RISC-V ecosystem own this) |
| Processor IP — DSP | ARC DSP, NPU (divesting to GF) | Tensilica HiFi / Vision DSP | DIRECTLY COMPETE (CDNS dominant — Tensilica >1.5B HiFi/yr, 160+ licensees) |
| Foundation IP (std cells, mem compilers, GPIO) | DesignWare foundation IP | Arm Artisan (acquired Aug 2025) | DIRECTLY COMPETE — newly entered by CDNS |
| Verification IP | DesignWare VIP | Cadence VIP | DIRECTLY COMPETE |
| Security IP | DesignWare security | Secure-IC (acquired Oct 2025) | DIRECTLY COMPETE |

### Product overlap — System Design & Analysis

| Domain | Synopsys (via Ansys) | Cadence | Status |
|---|---|---|---|
| Structural FEA | Ansys Mechanical | MSC Nastran (Hexagon D&E, close Q1 2026) | DIRECTLY COMPETE |
| CFD | Ansys Fluent / CFX | Fidelity | DIRECTLY COMPETE (Ansys dominant) |
| Multibody dynamics | Ansys Motion | Adams (MSC, via Hexagon D&E) | DIRECTLY COMPETE |
| Electromagnetic | Ansys HFSS / Maxwell | Clarity 3D Solver / EMX | DIRECTLY COMPETE |
| Signal / power integrity | Ansys SIwave / RedHawk | Sigrity X / Voltus | DIRECTLY COMPETE |
| Thermal | Ansys Icepak | Celsius | DIRECTLY COMPETE |
| Pre-/post-CAE | (limited) | ANSA / META (BETA CAE, acquired 2024) | COMPLEMENTARY (CDNS leads) |
| RF system | Ansys RF | AWR | DIRECTLY COMPETE |
| Multiphysics platform | Ansys workbench | Optimality / Reality / Millennium | DIRECTLY COMPETE |
```

Each row's status cell should be no more than one short sentence; the supporting evidence belongs in the prose paragraphs after the table.

## What to write after the matrix

The matrix is the deliverable. Below it, three short paragraphs:

1. **The pattern.** Where do most rows fall? Mostly DIRECTLY COMPETE means the two companies are converging into a true head-to-head; lots of NON-OVERLAPPING means they're more like adjacencies that happen to be debated.
2. **The "X dominant" rows.** Pull out the 2–5 sub-segments where one side has a real franchise. These will be referenced throughout §5.4 (sub-segment share) and §9 (scorecard).
3. **The most informative NON-OVERLAPPING rows.** Where one side ships and the other doesn't is often the most strategically interesting fact in the report. Sentaurus, Allegro X, and (now) Arm Artisan foundation IP are three examples from the SNPS-vs-CDNS matrix.

## Common failure modes

- **Too few rows.** A matrix with 5 rows for a multi-segment company is incomplete. Mid-size industrial / software companies should have 15–40 rows.
- **All rows "DIRECTLY COMPETE".** If you didn't find a single NON-OVERLAPPING or COMPLEMENTARY row, you've under-explored. Both sides almost always have at least one niche where they're alone.
- **Pairing the wrong products.** PrimeTime is timing signoff, not synthesis — pair it with Tempus, not Genus. Read each product's actual description before pairing.
- **Citing the subject company's 10-K for the competitor's product name.** SNPS's 10-K does not say "competes with Cadence Tempus" — it just lists Cadence as a competitor company. Cite Cadence's own product page for the Tempus row.
- **Inventing a product the company doesn't actually ship.** If you list "Synopsys PCB" but Synopsys doesn't actually have a meaningful PCB product, mark the row NON-OVERLAPPING — don't fabricate a counterpart.

## Worked example reference

The SNPS-vs-CDNS report at `reports/compare/SNPS_vs_CDNS.md` is the canonical worked example. Open it when you need a sanity-check on density, classification rigor, or sourcing depth.
