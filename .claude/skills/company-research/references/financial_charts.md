# Financial-statement visuals — `scripts/financial_charts.py`

Stockanalysis.com-style financial-statement charts as **inline SVG**, for embedding
directly in a research report. Six chart types, one helper, stdlib-only.

| Subcommand | Chart | Typical report home |
|---|---|---|
| `income`   | Income-statement **Sankey** (revenue → COGS / gross profit → opex / operating income → tax / net income, with revenue sources on the left) | Section 1 (Overview) or Section 2 (Valuation), as the "how it makes money" anchor |
| `balance`  | Balance-sheet **Sankey** (asset components → current / non-current → total assets → liabilities + equity → line items) | Section 1 / Section 9 (capital structure, leverage) |
| `cashflow` | Cash-flow **Sankey** (operating / investing / financing in- & out-flows → CFO / CFI / CFF → free cash flow / ending cash) | Section 1 / Section 2 (cash generation, FCF) |
| `donut`    | Revenue **donut** by business segment OR by geography | Section 1 (segment mix), Section 5 (geographic mix) |
| `revbars`  | **Historical stacked bars** — revenue by segment / geography over years | Section 1 / Section 6 (development-over-time) |
| `dupont`   | **5-step DuPont** ROE tree (ROE = net-margin × asset-turnover × equity-multiplier) | Section 1B / Section 2 (return decomposition) |

> The same helper has a **seventh** subcommand, `moneyflow` — the 3-stage supply-chain
> "money-flow" diagram (who pays → what they buy → where the money pools). It is an
> outward-looking value-chain map, not a financial-statement chart, so it lives in its
> own spec: **[`money_flow.md`](money_flow.md). It is REQUIRED — one per report.**

## Why inline SVG (NOT matplotlib, NOT Mermaid for these)

Same reasoning as `scripts/gf_score.py`:

- **Memory.** matplotlib PNG generation was disabled project-wide on 2026-06-03 to cut
  the per-agent memory footprint. This helper imports only the stdlib (`math` /
  `argparse`), adds ~0 MB resident, and is safe inside a report agent.
- **Rendering.** The report viewer (`reports_viewer.py` → `marked.js`, **no
  sanitization** — confirmed at `reports_viewer.py` `root.innerHTML = marked.parse(...)`)
  injects raw markdown into `innerHTML`, so a literal `<svg>` block renders verbatim —
  the same untouched-raw-HTML path `gf_score.py` and the Step-10 `<details>` logs ride
  on. **Paste the emitted `<svg>` into the report UN-FENCED (no ```` ``` ````), with a
  blank line before and after, so it renders.**
- **Fidelity.** Mermaid's `sankey-beta` exists on the unpinned `mermaid@11` CDN import
  but has minimal styling and no node $/% labels; inline SVG reproduces the
  stockanalysis.com look (colored ribbons, $ + % per node, leader-line donut labels)
  far more faithfully and without depending on an unpinned CDN feature. Keep Mermaid
  for the diagram types it's good at (timeline, product tree, quadrant) — see SKILL.md
  Step 8.

## Sourcing discipline (load-bearing — this is the whole point of "correct sources")

1. **Every number you pass MUST come from the company's OWN statements that you
   actually read** — the 10-K / 10-Q / 20-F / 年度报告 / 有価証券報告書 income statement,
   balance sheet, cash-flow statement, and the **segment note** (ASC 280 / IFRS 8) for
   revenue-by-segment and revenue-by-geography. IR earnings decks are an acceptable
   primary source for the same figures (they reconcile to the filing). **Do not pull
   these from a third-party data vendor's reshaped numbers** — vendors re-bucket line
   items (e.g. fold stock-comp into "other"), and the chart then won't reconcile to the
   filing the reader clicks through to.
2. **`--source` is REQUIRED and is baked into a footer inside the SVG**, per the
   project-wide chart rule (the source must travel inside the image — charts get
   screenshotted / iframe-embedded without their caption). Cite the **exact statement**:
   `"ISRG FY2025 10-K, Consolidated Statements of Operations + Note 4 Segments"`, not
   `"ISRG 10-K"`.
3. **The surrounding prose paragraph must still carry the inline page-level citation**
   for the figures the chart visualizes (the baked-in footer is a within-image backup,
   not a substitute for the report's paragraph-level citation standard). A number in the
   chart that isn't traceable to a cited filing is the same hallucination failure the
   skill forbids everywhere else.
4. **If a line item is not disclosed, omit it — never invent it.** A company that
   doesn't break out R&D vs SG&A → pass a single `--other-opex`. A balance sheet that
   doesn't split deferred liabilities → don't fabricate the split. Omission is always
   preferable to a plausible-looking invented number.
5. **The helper does not fetch anything.** There is no API call, no XBRL auto-pull, no
   LLM call — consistent with the project-wide "never call an LLM API" rule and the
   "every number traces to a source you read" rule. You read the statement; you pass and
   cite the numbers.

## Values & units

- Pass values in whatever unit you choose with `--unit {raw,k,m,b}` (default `m` =
  **millions** of the reporting currency). The helper auto-formats labels to
  `$X.XB` / `$XXXM` / `$X.XK` so one chart can mix scales like the screenshots.
- `--currency` sets the symbol (default `$`; use `¥`, `₩`, `€`, `NT$`, `HK$`, `RMB` as
  the filing reports). Negatives render with a leading minus (cash-flow uses/outflows).
- Keep node **labels short** (they sit beside the bars). "Working Capital" not
  "Changes in Operating Assets and Liabilities (Working Capital)".

## CLI by subcommand (worked ISRG examples)

All share `--source` (required), `--title`, `--unit`, `--currency`, `--note` (optional
italic caption), `--width`, `--height`. Output goes to **stdout** — pipe to a file or
paste directly.

### `income` — income-statement Sankey
Flags: `--revenue` (required); `--cogs` / `--gross-profit` (give either — the other is
derived); `--sga`, `--rd`, `--other-opex` (operating-expense children); `--operating-income`
(derived from gross-profit − opex if omitted); `--net-interest` (positive net interest /
other income feeding pretax); `--pretax`, `--tax`, `--minority`, `--net-income` (derived
where omitted); `--segment "Label:revenue"` (repeatable revenue sources on the left).

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py income \
  --segment "Instruments & Accessories:6000" --segment "Systems:2487" --segment "Service:1576" \
  --revenue 10063 --cogs 3423 --gross-profit 6640 --sga 2387 --rd 1308 --operating-income 2945 \
  --net-interest 366 --pretax 3311 --tax 435 --minority 21 --net-income 2856 \
  --title "How Intuitive Surgical (ISRG) Makes Its Money — FY2025" \
  --source "ISRG FY2025 10-K, Consolidated Statements of Operations + Note 4 Segments"
```

### `balance` — balance-sheet Sankey
Flags (all repeatable): `--asset "Label:value:current|lt"`,
`--liability "Label:value:current|lt"`, `--equity "Label:value"` (shareholders'-equity
components), `--minority <value>` (equity-side noncontrolling interest). Totals
(current/non-current assets, total assets, current/non-current liabilities, total
liabilities, equity) are derived; percentages are of total assets.

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py balance \
  --asset "Cash & Equivalents:5900:current" --asset "Receivables:1600:current" \
  --asset "Inventories:1800:current" --asset "Other Current:376:current" \
  --asset "LT Investments:3100:lt" --asset "Net PP&E:5300:lt" \
  --asset "Intangibles:381:lt" --asset "Other LT:1900:lt" \
  --liability "Accounts Payable & Accrued:851:current" --liability "Deferred Rev & Tax:507:current" \
  --liability "Other Current:648:current" --liability "Deferred Liab:91:lt" --liability "Other LT Liab:226:lt" \
  --equity "Retained Earnings:7000" --equity "Additional Paid-In Capital:10800" --equity "Common Stock + AOCI:44" \
  --minority 118 \
  --title "Intuitive Surgical (ISRG) Balance Sheet — FY2025" \
  --source "ISRG FY2025 10-K, Consolidated Balance Sheets"
```

### `cashflow` — cash-flow Sankey
Flags (all repeatable, **signed** values — positive = inflow, negative = use):
`--operating "Label:value"`, `--investing "Label:value"`, `--financing "Label:value"`;
plus `--capex <positive>` (footer Free-Cash-Flow note only — also pass capex inside
`--investing` as a negative item so it's a real use node), `--begin-cash`, `--fx`.

The chart is a **sign-aware "sources → total → uses" Sankey** that works for cash
**generators** (CFO > 0) *and* cash **burners** (CFO < 0): each of CFO / CFI / CFF is a
**source** (blue) when its net is positive and a **use** (red) when negative; Beginning
Cash is always a source, Ending Cash always the green retained node. Percentages are of
the **mobilized total** (Beginning + Σ positive nets = Ending + Σ |negative nets|), so
every node is a sensible ≤100% share and both sides sum to 100% — never the old
CFO-anchored model that blew past 100% and inverted a negative CFO into a fake inflow.
A category whose components are all the same sign as its net (e.g. a burner's
investing → ST-investment purchases + acquisitions + capex, all uses) is decomposed on
its own side; a mixed-sign category (operating: net loss − vs add-backs +) shows as a
single net node — put the reconciliation in prose, not a tangled fan. **For a
pre-revenue / cash-burning company this is the most important financial chart** (the
income Sankey / donut / DuPont are usually N/A — no revenue).

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py cashflow \
  --operating "Net Income:2856" --operating "D&A:677" --operating "Stock-Based Comp:788" \
  --operating "Deferred Tax:19" --operating "Working Capital:-1268" --operating "Other Operating:-58" \
  --investing "Net Investments:1219" --investing "Net PP&E:-540" --investing "Net Business:-14" \
  --financing "Net Stock Issuance:-2288" --financing "Other Financing:-69" \
  --capex 540 --begin-cash 2056 --fx 13 \
  --title "Intuitive Surgical (ISRG) Cash Flow — FY2025" \
  --source "ISRG FY2025 10-K, Consolidated Statements of Cash Flows"
```
*Note:* the ending-cash reconciliation is drawn as `Free Cash Flow + Beginning Cash →
Ending Cash` (a clean "where cash came from / went" visual). Node heights are |value|;
inflow/outflow magnitudes need not net to the category total (matches the
stockanalysis.com convention).

### `donut` — revenue donut (segment or geography)
Flags: `--slice "Label:value"` (repeatable, required), `--center "ISRG"` (center text).
Run it twice for the two donuts in screenshot 4 (by segment, by geography).

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py donut \
  --title "FY2025 Operating Revenue by Business Segment" --center ISRG \
  --slice "Instruments & Accessories:6000" --slice "Systems:2487" --slice "Service:1576" \
  --source "ISRG FY2025 10-K, Note 4 — Revenue disaggregation"
```

### `revbars` — historical stacked revenue bars
Flags: `--years "2021,2022,2023,2024,2025"`, `--series "Label:v1,v2,..."` (repeatable;
values align to `--years`), `--mode value|pct` (absolute $ stack vs 100%-stacked share).
This is the time-series companion to the donut — the bottom half of screenshot 4. Obeys
the project chart rules: the x-axis must cover the full disclosed history and the
rightmost year must be the latest reported period.

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py revbars --unit b \
  --years "2019,2020,2021,2022,2023,2024,2025" \
  --series "Instruments & Accessories:2.5,2.5,3.4,3.9,4.3,5.0,6.0" \
  --series "Systems:1.5,1.1,1.6,1.6,1.6,1.9,2.5" \
  --series "Service:0.9,0.9,1.1,1.2,1.4,1.5,1.6" \
  --title "Historical Operating Revenue by Business Segment" \
  --source "ISRG FY2019–FY2025 10-Ks, Note 4 — Revenue disaggregation"
```

### `dupont` — 5-step DuPont ROE tree
Flags (all required, raw $ in `--unit`): `--net-income`, `--pretax`,
`--operating-income`, `--revenue`, `--begin-assets`, `--end-assets`, `--begin-equity`,
`--end-equity`. The helper computes the factors (net margin, asset turnover, equity
multiplier, operating margin, tax burden, interest burden) and the composite ROE; you do
not pass ratios. Averages use `(begin+end)/2`. To match a vendor's *annualized*
quarterly ROE, pass annualized P&L figures (quarterly × 4) and use `--note "annualized
from <period>"`.

```bash
/opt/anaconda3/bin/python3 scripts/financial_charts.py dupont \
  --net-income 3300 --pretax 3777 --operating-income 3436 --revenue 11136 \
  --begin-assets 20500 --end-assets 20100 --begin-equity 17800 --end-equity 17500 \
  --note "annualized from 2026-Q1 (quarterly × 4)" \
  --source "ISRG 2026-Q1 10-Q, Statements of Operations + Balance Sheets"
```

## Embedding in a report

The helper prints raw SVG to stdout. Capture it and paste it into the markdown
**un-fenced**, with a one-line markdown citation underneath (same as any chart) even
though the source is also baked in:

```markdown
### 收入结构 / How ISRG makes its money

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" ...> … </svg>

来源 / Source: [ISRG FY2025 10-K, Statements of Operations + Note 4 Segments](https://www.sec.gov/Archives/edgar/data/1035267/.../isrg-20251231.htm)
```

- One blank line before and after the `<svg>` block; do **not** wrap it in a ```` ``` ````
  fence (that would show the SVG source as code instead of rendering it).
- The markdown citation below the chart is a **clickable deep link** to the exact
  filing/page — the baked-in footer carries the source for screenshot/iframe contexts;
  the markdown link carries it for the reader who wants to click through.

## Placement bar for a full report

A 6,000–10,000-word initiation **carries the full suite by default — all seven visuals:**
the **income-statement Sankey** (the "how it makes money" anchor), the **balance-sheet
Sankey**, the **cash-flow Sankey**, a revenue **donut by segment** AND a second **donut
by geography**, the **revbars** (development-over-time view), and the **dupont** tree
(return-quality framing, complements the Section 1B GF Score). This is **not** a "minimum
+ add-by-fit" menu — ship all seven for any issuer that files full statements.

**The only sanctioned reasons to drop a chart** are that the underlying data genuinely
isn't disclosed: a private company with no published balance sheet/cash-flow statement
(skip those Sankeys + DuPont); a single-segment, single-geography issuer (skip the
segment or geography donut that would have one slice); fewer than 2–3 comparable years
(skip revbars). When you drop one, **name it and say why in the Step 10 verification
log** — a financials section missing balance/cashflow/dupont on a normal public issuer is
a defect, not a style choice. These are additive to — not a replacement for — the Mermaid
diagrams (timeline, product tree, competitive quadrant) specified in SKILL.md Step 8.

## Guardrails

- The DuPont factors and any ratio the helper computes are arithmetic on the figures you
  supply — they are derived, not a source. The underlying $ figures each need their own
  inline citation in the prose. (The DuPont composite is not a sell-side "rating" — it's
  a decomposition of reported results; no `*Analyst view:*` label needed, unlike the GF
  Score and the price target.)
- The income/balance Sankeys conserve value at each split when you supply consistent
  figures; if your gross-profit ≠ revenue − COGS (rounding, or a non-standard P&L), the
  chart will still draw but won't reconcile — fix the inputs, don't ship a chart that
  contradicts the statement.
- For loss-making periods (negative operating income / net income) the profit-waterfall
  Sankey is awkward; the helper degrades gracefully (no negative geometry) but consider a
  donut + revbars + a prose walk instead, and say so.
- Non-USD filers: pass `--currency` and the filing's own unit; keep the segment/geography
  labels in the filing's framing (don't re-translate `数据中心` ↔ `Data Center`
  inconsistently across the donut and the prose).
