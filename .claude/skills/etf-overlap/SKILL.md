---
name: etf-overlap
description: Produce 3,000–6,000 word head-to-head ETF holdings-overlap reports for 2–4 ETFs in English (Simplified Chinese also available on explicit request). Covers shared-holdings count, overlapping weight, top common positions, sector / country skew, top-10 concentration, expense-ratio + AUM comparison, and a verdict on whether the funds are duplicative / complementary / orthogonal. Reports saved to `reports/etf/<A>_vs_<B>[_vs_<C>].md` (Chinese companion at `..._zh.md` only when requested). Use when the user asks "do QQQ and SMH overlap?", "is SCHD doubling my SPY exposure?", "compare VTI vs ITOT vs SCHB", or "ETF overlap on these three."
---

# ETF Overlap Report

Head-to-head deliverable: a 3,000–6,000 word markdown report that answers **whether two-to-four ETFs are duplicative, complementary, or orthogonal** — quantified, not asserted. Input is just N ETF tickers.

Adapted from the [LLMQuant ETF overlap workflow](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-etfs/workflows/etf-overlap-report.md) (MIT), re-pointed at SEC EDGAR N-PORT + issuer-published holdings CSVs + yfinance fallback.

## When to use

The user says any of:

- "Do QQQ and SMH overlap?"
- "Compare VOO vs VTI vs SCHB" (≤4 sides)
- "Is SCHD doubling my SPY exposure?"
- "ETF overlap on QQQ, SOXX, SMH"
- "Holdings-overlap report for these three ETFs"
- "How concentrated is QQQ vs IWM at the top?"

Supports **2 to 4 ETFs (N=2, 3, or 4)**. Beyond N=4 the head-to-head sharpness collapses — use [[sector-overview]] for a wider ETF-universe sweep.

## When NOT to use

- The user asks about a single ETF's holdings (not a comparison) — use [[company-research]] or a one-off `yfinance` query; this skill is fundamentally comparative.
- One of the ETFs is < 6 months old (no N-PORT filed yet) — flag the issue and fall back to issuer-published top-10 only, noting the limitation.
- One of the tickers is not a US 40-Act fund (e.g. it's a closed-end fund, ADR, or non-US-domiciled UCITS) — these don't file SEC N-PORT. Flag explicitly and either skip that ETF or note the holdings data is issuer-disclosed only.

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim — read its **Core principle** section before drafting. ETF-specific failure modes on top of the base rule:

- **Never invent a holding.** Every "X.Y% of the ETF is in NVDA" must trace to a specific SEC N-PORT filing OR an issuer-published holdings CSV with a stated as-of date. yfinance's `get_funds_data()` top-10 is fine for headline figures but the full overlap analysis requires the underlying holdings file.
- **Never imply N-PORT holdings are live daily holdings.** SEC N-PORT is filed quarterly with a 60-day lag; reported holdings are 60–150 days old by the time you read them. State the as-of date inline and warn the reader when the report is stale enough to matter (e.g. tracking a fast-rebalancing thematic ETF).
- **Never merge two different securities just because tickers look similar.** Match by CUSIP / ISIN when ticker is ambiguous (`GOOGL` vs `GOOG` are different securities; class-A vs class-B preferred shares are different securities; `0700.HK` vs `00700.HK` is the same security with different padding — normalize before comparing).
- **Never sum percentages across ETFs as if they're the same denominator.** If QQQ is 8% NVDA and SMH is 22% NVDA, the reader's combined NVDA exposure depends on the weight they assign to each ETF in their portfolio — say so; don't write "the total NVDA exposure is 30%."
- **Never compute overlap on incomplete holdings.** If the issuer only publishes top-10 and the N-PORT is older than 4 months, the rest of the portfolio is opaque. Report the overlap only on the retrieved rows and label it as such ("Overlap on top-10 holdings only; bottom-90% comparison unavailable").

## Report language

**Default behavior: English only.** This is a monitoring / operational skill rather than a deep-research deliverable — most users want the English read and don't need the Chinese companion every time. (The substantive research skills `company-research` / `compare-companies` / `earnings-analysis` / `sector-overview` still default bilingual; this skill does not.)

**Chinese opt-in (any of these triggers a Chinese companion file alongside the English):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

Examples:
- `compare QQQ and SMH overlap` → English only: `QQQ_vs_SMH.md`
- `compare QQQ and SMH overlap, also in Chinese` → both: `QQQ_vs_SMH.md` + `QQQ_vs_SMH_zh.md`
- `比较沪深300ETF和上证50ETF的重叠 用中文即可` → Chinese only: `..._zh.md`

When a Chinese companion is produced, use bilingual technical terms: `ETF / 交易所交易基金`, `expense ratio / 费率`, `AUM / 管理规模`, `N-PORT / N-PORT 持仓披露`, `CUSIP / CUSIP 证券代码`, `top-10 concentration / 前十大集中度`, `sector skew / 行业偏离`. Keep ticker codes in original form.

## Data sources

### Primary (in order of preference)

1. **SEC EDGAR N-PORT** — the only legally-binding full-holdings source for US 40-Act funds. Filed quarterly; full holdings disclosed for the as-of quarter-end. URL pattern:
   ```
   https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<CIK>&type=NPORT-P
   ```
   The primary doc is XML: `https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/primary_doc.xml`. Each `invstOrSec` element has issuer name, CUSIP, ISIN, % of net assets, fair value, shares. Use the EDGAR submissions JSON to resolve the latest N-PORT-P filing's accession + primary doc:
   ```bash
   curl -sS -A "Research Analyst <email>" \
     "https://data.sec.gov/submissions/CIK<10-digit-padded>.json" \
     | python3 -c "import json,sys; d=json.load(sys.stdin); r=d['filings']['recent']; [print(f, r['accessionNumber'][i], r['filingDate'][i], r['primaryDocument'][i]) for i,f in enumerate(r['form']) if 'NPORT' in f]"
   ```
   Write the parser as a one-off Python script under `oneoff/fetch_etf_nport_<TICKER>.py` — pattern-match `fetch_financial_report.py`.

2. **Issuer-published holdings CSV** — for the most-current daily holdings (no 60-day lag). Each major issuer publishes a predictable URL:
   - **iShares (BlackRock)**: `https://www.ishares.com/us/products/<product-id>/<slug>/1467271812596.ajax?fileType=csv&fileName=<TICKER>_holdings&dataType=fund` — find the product-id via the fund's main page.
   - **Vanguard**: holdings file at `https://investor.vanguard.com/investment-products/etfs/profile/<TICKER>` → "Portfolio" tab → "Holdings" CSV download.
   - **SPDR / State Street**: `https://www.ssga.com/us/en/individual/etfs/funds/<slug>-<TICKER>` → holdings CSV.
   - **Schwab**: `https://www.schwabassetmanagement.com/products/<TICKER>` → "Portfolio Holdings" link.
   - **Invesco (QQQ, etc.)**: `https://www.invesco.com/qqq-etf/en/about.html#composition` for QQQ specifically; other Invesco ETFs follow `/etfs/portfolio-management/etf-holdings`.
   The issuer's daily holdings file is the most current source — use it as the primary cite when available, and N-PORT as backup for the historical comparison.

3. **yfinance `get_funds_data()`** — fallback when both N-PORT and issuer CSV fail to parse. Returns top-10 holdings + sector breakdown + asset mix. Sufficient for a top-level overlap verdict but not for the full overlap analysis. **Label any output sourced from yfinance as "top-10 only" — never imply a full overlap was computed from yfinance data.**

### Crowding / positioning context (new — see Step 4.5)

- **Index-provider reconstitution announcements (FTSE Russell / S&P DJI)** — adds/deletes, effective dates, weight-change magnitude. Used to flag whether a shared top name sits in an index facing an *imminent* rebalance (a near-term concentration catalyst that passive ETFs mechanically trade). Cite the index-provider announcement with a deep URL; **never fabricate a passive-flow size** — if not published, state "reconstitution pending YYYY-MM-DD, flow size not estimated." Mirrors GS Index-Strategy "Rebalancing Review" framing.
- **Index-weight rank / methodology fact sheets** — to establish that a shared name is top-ranked across the tracked indices (the crowded-shared-book signal). Deep URLs to the provider's fund/index page.
- **Local zsxq broker library (`db/zsxq.db`, READ-ONLY)** — sell-side positioning language (`机构持仓拥挤`, record OW/UW, "consensus long") as a citable crowding-context source. Citation form: `[<broker> <title>, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)` — the direct-download `/zsxq/pdf/...` route only (paste `find_pdf.py`'s `pdf_url`); **never** the `/zsxq/pdf-viewer/<id>` HTML viewer (won't download on iPad) and **never** the dead `/zsxq-pdf/<id>` form. Read-only Tier-1 safety rule — never write.

### Profile / context data

- **AUM, expense ratio, inception, category** — yfinance `Ticker(etf).info` or the issuer's product page.
- **Sector breakdown** — from N-PORT (compute from holdings) or yfinance.
- **Country breakdown** — from N-PORT `invstOrSec.invCountry` field, or issuer-published.
- **Performance** — yfinance price history. Compute 1Y / 3Y / 5Y returns vs the benchmark stated in each fund's prospectus.

## Workflow

### Step 0 — Parse inputs and resolve CIKs

User input forms accepted:

- `etf-overlap QQQ SMH`
- `compare QQQ and SMH overlap`
- `QQQ vs SMH vs SOXX overlap` (N=3)
- `VOO vs VTI vs ITOT vs SCHB` (N=4)
- `holdings overlap on these four: VOO VTI ITOT SCHB`

Resolve each ETF ticker to its SEC CIK (use the EDGAR ticker→CIK map at `https://www.sec.gov/files/company_tickers.json`). Validate that each is a 40-Act fund (form types include `NPORT-P` in the recent filings).

For N ETFs in the user's left-right order, preserve the order in file naming and column ordering throughout the report. Reject N=1 (use a one-off yfinance query) and N≥5 (use [[sector-overview]]).

### Step 1 — Fetch holdings for each ETF

For each of the N ETFs, fetch in this order until you get a usable holdings table:

1. **Issuer-published daily CSV** — most current. If found, save under `oneoff/etf_holdings_<TICKER>_issuer_<YYYY-MM-DD>.csv`.
2. **SEC N-PORT primary_doc.xml** — fall back if issuer CSV unavailable or stale. Parse the XML `invstOrSec` rows; save under `oneoff/etf_holdings_<TICKER>_nport_<YYYY-MM-DD>.csv`.
3. **yfinance `get_funds_data()`** — last resort. Label all output as "top-10 only" and warn explicitly that bottom-90% overlap was not computed.

Sanity-check each holdings file: total weight should sum to ~100% ±2% (rounding); negative weights or cash-equivalents are normal for some funds (synthetic exposure, leverage); duplicate CUSIPs are errors (de-dup before merge).

### Step 2 — Normalize identifiers and align

For each holding row, normalize:
- **Ticker** as primary key when reliable (matches across ETF holdings); fall back to **CUSIP** then **ISIN** when ticker is missing, ambiguous, or non-US-listed.
- **Issuer name** (strip Inc / Corp / SE suffixes for fuzzy matching; never as primary key — too unreliable).
- **Share class** stays distinct (`GOOGL` ≠ `GOOG`).

Build a unified holdings table joining all N ETFs on the normalized identifier. Each row: holding identifier + N weight columns (one per ETF; blank when not held).

### Step 3 — Compute overlap metrics

For each pair (N=2: one pair; N=3: three pairs; N=4: six pairs):

| Metric | Definition |
|---|---|
| Shared holdings count | Count of issuers held by both ETFs |
| Overlapping weight (A→B) | Σ over shared holdings of min(weight_A, weight_B) — symmetric; the conservative overlap |
| Overlap-by-A | Σ over shared holdings of weight_A — share of ETF A that is also in ETF B (asymmetric) |
| Overlap-by-B | Σ over shared holdings of weight_B — share of ETF B that is also in ETF A |
| Largest common positions | Top 10 issuers ranked by min(weight_A, weight_B), with both weights shown |
| Disjoint top-10 of A | Top-10 of A that are not in B at all |
| Disjoint top-10 of B | Top-10 of B that are not in A at all |

For N≥3, also compute the **triple-overlap weight** — issuers held by all three (or all four) — using `min` across all participating ETFs.

### Step 4 — Compute concentration and exposure

For each ETF independently:

- **Top-10 concentration** = sum of top-10 weights.
- **Top-1 concentration** = largest single weight.
- **Herfindahl** = Σ wᵢ² (a 0–10000 scalar; SPY is ~50, QQQ ~700, SMH ~1500, single-stock fund 10000).
- **Benchmarked concentration** — don't ship Herfindahl / top-10 weight as a bare scalar. Report each **as a percentile vs a peer set** (e.g. SPY / QQQ / a sector-ETF reference) or vs the fund's own trailing history, so "concentrated" carries a number (mirrors the GS/MS "vs history / vs positioning" convention). Every percentile must trace to the computed source data in the oneoff script.
- **Sector breakdown** (GICS or N-PORT-provided) side-by-side across all N.
- **Country breakdown** for international funds; for US-equity funds compare cash + foreign sleeve.

### Step 4.5 — Crowding & positioning context

Sits between Step 4 (Concentration) and Step 6 (Verdict). For each shared top-10 name, annotate whether it is a **consensus crowded trade**, using:

- **(a) Index-weight rank** — the name's weight rank across the major indices the N ETFs track (e.g. a name that is top-3 in both the Nasdaq-100 and the PHLX Semiconductor Index is a crowded shared book). Source: index-provider fact sheets / methodology pages with deep URLs.
- **(b) Sell-side positioning language** — read the local zsxq library (`db/zsxq.db`, **read-only**) for crowding verdicts (`机构持仓拥挤`, record OW/UW, "consensus long"), cited as `[<broker> <title>, zsxq #<file_id> p.<N>](http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>#page=<N>)` — the direct-download `/zsxq/pdf/...` route only (paste `find_pdf.py`'s `pdf_url`), **not** the `/zsxq/pdf-viewer/<id>` HTML viewer and **not** the dead `/zsxq-pdf/<id>` form. The zsxq library is itself a citable positioning-context source.
  **Sell-side view evolution (卖方观点演变)** — when **≥2 zsxq notes** cover the same shared holding or question: date every cited institute view (the filename's `-YYMMDD` suffix is the authoritative report date; sanity-check against `create_time`) and order each institute's takes chronologically — a broker revising its own crowding read or rating/PT (e.g. OW → EW, `PT raised X → Y`) is reported as a dated revision with its stated trigger, never silently replaced by the latest take. When institutes disagree (opposite crowding verdicts, PTs >20% apart), present both views dated side-by-side — never blend them into a fake consensus. A 2026-03 take and a 2026-06 take from the same institute are two different views, not duplicates; each carries (institute, report date, the `/zsxq/pdf/<file_id>/<urlencoded-name>` link).
- **(c) Index-reconstitution / passive-flow check** *(near-term catalyst)* — for each ETF, identify the tracked index and flag whether shared top names sit in an index facing an **imminent FTSE Russell / S&P DJI reconstitution**. Mirror GS Index-Strategy framing: name the **effective date** and that passive ETFs mechanically trade it. Source from index-provider announcements with deep URLs. **Do not fabricate flow-size numbers** — if the passive flow isn't published, write "reconstitution pending YYYY-MM-DD, flow size not estimated."

Report this as a short table annotating the shared top-10 (name | shared min-weight | index-weight rank | crowding verdict + source | reconstitution flag). The output is **not a new verdict bucket** — it is a one-line crowding flag feeding the Step 6 verdict (see below).

### Step 5 — Compute performance / valuation backdrop

Pull 1Y / 3Y / 5Y total return for each ETF (yfinance, `auto_adjust=True`). Pull the stated benchmark from each prospectus and report tracking error vs benchmark. Pull expense ratio (yfinance `.info['annualReportExpenseRatio']` or issuer page). Compute net excess return after fees.

Optional: average P/E and P/B of the underlying basket (weighted by holdings × per-name multiple from yfinance) — useful for valuation skew between funds.

Optional — **historical co-movement** (operationalizes GS's "historical regularity / 历史走势规律" framing for an overlap context): report the trailing correlation and the **max common drawdown** of the N ETFs (yfinance `auto_adjust=True` adjusted prices) so the overlap % gets a *consequence* — "these two fell together X% in the last drawdown" rather than a bare overlap fact. This gives the reader the correlated-risk read the overlap number implies but never states.

### Step 6 — Verdict

Classify the comparison into one of four buckets:

| Verdict | Rule |
|---|---|
| **Duplicative** | Pairwise overlapping weight ≥ 60% AND sector breakdown within 5 pts on the top 3 sectors |
| **Complementary** | Overlapping weight 25–60% AND sector breakdowns differ meaningfully (top sector differs OR top-3 sectors > 15 pts apart) |
| **Orthogonal** | Overlapping weight < 25% AND no shared top-3 sector |
| **Mixed** | Overlap moderate but unevenly distributed (one ETF mostly inside the other, but the other has significant disjoint exposure — common in "core + satellite" pairings) |

For N≥3, report the verdict pairwise (a 3-by-3 verdict matrix) and surface the "most duplicative pair" and "most orthogonal pair" as top-level findings.

**Crowding flag (consume the Step 4.5 signal — not a new bucket).** Append a one-line crowding qualifier to the verdict so the reader distinguishes correlated-drawdown risk: **"Duplicative AND the shared book is the crowded consensus trade"** (highest co-drawdown risk — the shared min-weight is dominated by names that are top-ranked across the tracked indices and flagged crowded in the sources) vs **"Duplicative but the shared book is diversified / contrarian"** (lower co-drawdown risk). The flag is a sourced sentence, not a new verdict tier.

### Step 7 — Generate charts (4–6 visuals)

Save under `reports/charts/etf_overlap_<A>_vs_<B>_*.png` (DPI 150, `bbox_inches="tight"`):

1. **Overlap Venn / heatmap PNG** — for N=2 or N=3, a `matplotlib-venn` figure (`pip install matplotlib-venn`; circle sizes from total weights, intersection sized by overlapping weight); for N=4, or if `matplotlib-venn` is unavailable, a pairwise overlapping-weight heatmap matrix instead. **Never a Mermaid block — Mermaid has no Venn diagram type**, so a "mermaid venn" cannot render.
2. **Top-10 shared positions bar chart** — for each shared issuer, side-by-side bars showing weight in each ETF.
3. **Sector breakdown stacked bars** — N stacked bars, GICS sector ordering.
4. **Performance comparison** — 1Y / 3Y / 5Y total return + benchmark return + expense ratio in a single table.
5. *(Optional)* **Herfindahl + top-10 concentration scatter** — concentration risk visualized.
6. *(Optional)* **Country breakdown** for international comparisons.
7. *(Optional)* **Historical co-movement** — rolling correlation line and/or rebased price series of the N ETFs over the trailing window, annotating the max common drawdown (the Step 5 historical-co-movement metric). Carries the in-chart source annotation like every other chart.

Every PNG renders the source + as-of dates **inside the image** as a footer annotation (`fig.text(0.12, 0.02, ...)`): `Source: SEC N-PORT (<as-of>); issuer holdings CSV (<as-of>); yfinance (<as-of>). Computed in oneoff/etf_overlap_<A>_vs_<B>.py.` The markdown caption repeats it as a backup — the in-image footer is the primary mechanism (charts get viewed in isolation). For the chart-7 co-movement panel, clip the x-axis to the **intersection** of all N ETFs' valid price history (`first = max(s.index.min() for s in series)`) so a younger ETF doesn't leave an empty left region. Before saving any chart, confirm the rightmost data point is within a few days of today.

### Step 8 — Write the report

Save to `reports/etf/<A>_vs_<B>.md` (and `..._zh.md`) at the project root. Create the `reports/etf/` directory if missing.

Suggested 8-section structure:

1. **Bottom Line** — verdict + 2–3 sentence rationale + key number (pairwise overlapping weight).
2. **ETF Profiles** — N-row table: name, issuer, inception, AUM, expense ratio, stated benchmark.
3. **Overlap Summary** — shared count, overlapping weight per pair, triple-overlap for N≥3.
4. **Top Shared Positions** — table of top 10 common holdings with weights per ETF.
5. **Disjoint Top-10** — for each ETF, what's in its top-10 that's not in the others.
6. **Sector & Country Exposure** — N-column tables.
7. **Concentration & Performance** — Herfindahl, top-10 weight (each benchmarked to a percentile vs peer/own history), 1Y/3Y/5Y return, expense ratio, optional historical co-movement (trailing correlation + max common drawdown).
7-bis. **Crowding & Positioning Context** — the Step 4.5 table: for each shared top-10 name, its index-weight rank, crowding verdict (sourced from index methodology + zsxq positioning language), and any pending FTSE/S&P reconstitution flag with effective date. Closes with the one-line crowding flag that feeds the verdict.
8. **Coverage caveats** — as-of dates per data source, any stale-snapshot warnings, missing-data flags, and any pending index reconstitution ("shared name X faces FTSE reconstitution effective YYYY-MM-DD; passive flow size not estimated").
9. **Data Used** manifest (see block below).
10. **References** — deep URLs to N-PORT filings, issuer holdings pages, yfinance snapshots.

### Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — how holdings overlap and overlapping weight work, how index weighting / methodology schemes (market-cap-weight vs equal-weight vs modified-cap) shape a fund's exposure, how N-PORT vs daily issuer holdings differ, or any fund-mechanics concept for a reader new to ETF structure — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the issuer's own product / education channel, an index provider's explainer, or a well-known finance-education channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, weight, expense ratio, or return figure is ever attributed to a video (a video can't be string-matched against its source).

### Step 9 — Verify and clean up

- Re-run the script to confirm it's idempotent.
- Spot-check ≥3 weights in the report against the source holdings CSVs (`grep -F "<%>" oneoff/etf_holdings_<TICKER>_*.csv`).
- Spot-check the verdict logic — does the pairwise overlap actually compute to the reported number?
- HTTP-check every URL in the report (real-browser User-Agent, `200 OK` only; retry slow .gov sites with a 30s timeout before declaring them dead). Fix or drop any URL that fails — never ship a 404.
- **If ≥2 zsxq notes were cited on the same shared holding or question**: confirm every institute view is dated, same-institute revisions are shown as old → new with trigger, and conflicting views appear side-by-side (per Step 4.5(b) *Sell-side view evolution*) — not blended.
- Append a folded `<details><summary>Verification log — YYYY-MM-DD</summary>` block to the report listing the weight spot-checks, the verdict re-computation, and the URL-check results.
- Stop any test servers used during chart rendering.
- Commit and push per the project's standard workflow (Conventional Commit, e.g. `feat(reports/etf): …`).

## Output Format (mandatory blocks)

Every report must contain:

1. **Bottom-line verdict** at the top (bold, one line) — carrying the single load-bearing number (pairwise overlapping weight) and the **crowding flag** when the shared book is the consensus crowded trade (mirrors GS/JPM flow-note headlines that put the verdict + load-bearing number in the title itself).
2. **Profile table** with N rows (issuer, AUM, expense ratio).
3. **Overlap table** with pairwise weight, shared count, top common positions.
4. **4–6 embedded charts** with inline captions and source attribution.
5. **`## Data Used / 数据来源清单`** manifest (see block below).
6. **`## Guardrails for this verdict`** — what would invalidate the analysis.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Holdings — primary source per ETF**
- <ETF A>: Issuer-published holdings CSV from <issuer URL>, as-of YYYY-MM-DD. N=<X> rows.
- <ETF B>: SEC N-PORT-P (accession <number>, filed YYYY-MM-DD, as-of YYYY-MM-DD). N=<Y> rows. Source: https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/primary_doc.xml.
- <ETF C>: yfinance get_funds_data() top-10 only (no full N-PORT available). As-of YYYY-MM-DD.

**Profile metadata**
- AUM, expense ratio, inception, benchmark — yfinance Ticker.info / issuer product page as of YYYY-MM-DD.

**Performance**
- 1Y / 3Y / 5Y total return — yfinance auto_adjust=True, computed inline.

**Stale notices / coverage gaps**
- <bulleted list — N-PORT > 4 months old, issuer CSV behind paywall, holdings only top-10, or "none">.
- E.g.: "QQQ N-PORT filed 2026-03-15 with as-of 2026-01-31 (4 months old); for daily-current overlap use the Invesco issuer page."
```

## Primary-source-first & development-over-time rule (MANDATORY)

The user's standing preference for every report-producing skill: **reference the 10-K / 10-Q / original investor-relations materials as much as possible, cite them at page level, and present the material so the reader can see the company's development over time — what's new this period.**

1. **Source-preference order for any company fact.** (1) The company's own filings — 10-K / 10-Q / 8-K / DEF 14A / 20-F / 6-K / S-1 on EDGAR, or the non-US equivalent (年度报告 via cninfo, HKEX annual report, 有価証券報告書, 사업보고서); (2) original IR materials — earnings press release, earnings / investor-day deck, call transcript, shareholder letter; (3) third-party industry research; (4) news. Never cite a news rewrite for a fact that lives in a filing or an IR original — chase the original. Sell-side / zsxq broker notes are NOT displaced by this rule: they remain the separate `*Analyst view:*` layer (with their own page-level cites) and are never blended into the company-fact layer.

2. **10-K / 10-Q / annual-report citations must carry page numbers.** Format: `[NVDA FY2025 10-K, p. 42 — Segment results](https://www.sec.gov/...)`. When the EDGAR HTML doc makes the print page hard to pin down, give the Item + note/section heading instead (`Item 2 MD&A — Data Center revenue`, `Note 17 — Segment Information`) so the reader lands within one page-flip of the number. A bare `[10-K](url)` with no page/section locator fails the citation bar. The same locator discipline applies to prospectuses (page), IR decks (slide number), and non-US annual reports (第 N 页 / p. N).

3. **Present development over time — "what's new".** Do not render the company as a static snapshot. Wherever the output's structure allows, frame disclosures diachronically: trace the same line item across consecutive 10-Ks / 10-Qs (segment revenue & mix, risk factors added / dropped, customer-concentration %, capacity / capex, backlog, headcount, guidance language) and state explicitly what is NEW in the latest filing versus the prior one. Preferred presentations: an evolution table (`FY23 → FY24 → FY25`, each column cited to its own filing + page) and/or a short "What changed this period / 本期新变化" callout where the section covers a recurring disclosure.

4. **English originals stay English — even in Chinese-language reports.** When the original source is English (SEC filing, English IR deck / transcript / press release), cite and quote the English original directly; do not substitute a Chinese-media rewrite for language consistency. Symmetric with the existing original-language rule: the original's language always wins, whichever it is.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the subject of the output — the ticker, theme, sector, ETF holdings, deal, or any name that materially drives the analysis — sits in **AI** (foundation models, AI software/agents, AI infrastructure: datacenter compute, networking, power), **robotics** (humanoids, industrial automation, AMRs, actuators / reducers / sensors / end-effectors), or **semiconductors** (fabless, foundry, IDM, memory/HBM, equipment/WFE, materials, EDA/IP, advanced packaging), give those names a **detailed narrative treatment**, not summary bullets:

- **Write full narrative prose** for the sector-relevant sections — mechanism and causality ("X drives Y because Z"), not headline restating. Bullets may organize the prose but never replace it.
- **Cover the sector-specific dimensions that apply:**
  - *Technology position & roadmap* — process node / architecture / model-capability cadence vs named competitors (e.g., N2 vs 18A, HBM3E→HBM4, GB200→Rubin, Optimus gen-3 vs Figure 03).
  - *Supply-chain position* — key suppliers and customers up/down the chain, single-source chokepoints (TSMC/CoWoS, EUV, HBM), where pricing power sits, content-per-unit ($ per GPU / per robot / per vehicle).
  - *AI demand linkage* — the explicit path from AI capex to this name's P&L (orders → backlog → revenue recognition) with the actual disclosed numbers, never a generic "AI beneficiary" label.
  - *Robotics linkage* — design-win status, which platforms (Tesla Optimus, Figure, Unitree, domestic Chinese OEMs), volume and timeline realism vs the hype cycle.
  - *Cycle context* — where the semi / memory-pricing / AI-capex cycle stands right now and what that implies for forward estimates.
  - *Geopolitics & export controls* — US BIS rules, China localization, tariff exposure, entity-list status where relevant.
- **Quantify the narrative.** Each dimension covered should carry at least one sourced number (TAM, ASP, capacity, units, share). All figures obey the project's numerical-accuracy rule — every number traces to a URL or PDF page cited in the same paragraph.
- **Engage the sell-side view.** Where the zsxq library or other broker sources are in scope for this skill, the AI/robotics/semi narrative must engage the institute view (PTs, estimate revisions, cross-broker disagreement) rather than ignoring it.

This rule **deepens** the skill's existing output format — it never replaces or shortens the required structure. For subjects outside these sectors, the skill's baseline depth applies unchanged.

## Guardrails

- **Do not invent holdings.** Every weight traces to a specific N-PORT filing, issuer CSV, or yfinance snapshot with as-of date.
- **Do not imply N-PORT holdings are live.** They are quarterly snapshots with a 60-day filing lag — 60–150 days old by the time you read them. State the as-of date inline.
- **Do not match securities by issuer name alone.** Use ticker → CUSIP → ISIN as the match key hierarchy. "Alphabet" appears in multiple share classes.
- **Do not sum percentages across ETFs as combined exposure.** That depends on the reader's portfolio weights, which you don't know.
- **Do not ship a crowding figure without a denominator, or a crowding adjective without a number.** Any crowding / positioning figure must be denominated in money AND as % of a stated base (AUM, free-float, index weight) — modeled on GS's `占自由流通市值1.3%` convention. Any crowding adjective ("crowded", "concentrated", "consensus long") must carry a sourced number. This extends the "never sum percentages across different denominators" rule to the positioning layer.
- **Do not compute overlap on partial holdings without saying so.** If you only have top-10, label every overlap number as "top-10 only".
- **Do not treat tracking error as a verdict.** A 50-bp tracking error vs benchmark may be acceptable for one fund and a defect for another — flag it, don't grade it.
- **Do not silently drop unsupported asset types** (synthetic positions, repos, swaps, futures with cash settlement). Surface them in a "non-equity-sleeve" footer; the reader needs to know that "5% cash + futures" is part of the exposure, not just ignored.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Output location

Save to `reports/etf/<A>_vs_<B>[_vs_<C>][_vs_<D>].md` (and `..._zh.md`) under the project root. Create the `reports/etf/` directory if missing.

**Filename convention — no date suffix; `_zh` suffix marks the Chinese edition:**

| N | Language | Filename pattern |
|---|---|---|
| 2 | English | `<A>_vs_<B>.md` |
| 2 | Chinese | `<A>_vs_<B>_zh.md` |
| 3 | English | `<A>_vs_<B>_vs_<C>.md` |
| 3 | Chinese | `<A>_vs_<B>_vs_<C>_zh.md` |
| 4 | English | `<A>_vs_<B>_vs_<C>_vs_<D>.md` |
| 4 | Chinese | `<A>_vs_<B>_vs_<C>_vs_<D>_zh.md` |

Preserve the user's left-right ETF ordering — do not alphabetize.

Supplementary deliverables sit in standard locations:
- Charts: `reports/charts/etf_overlap_<A>_vs_<B>_*.png`.
- Holdings CSVs + parse script: `oneoff/etf_holdings_<TICKER>_*.csv`, `oneoff/etf_overlap_<A>_vs_<B>.py`.

### Update-in-place rule

One English file and one Chinese file per ordered tuple. If `<A>_vs_<B>.md` already exists, update it in place (refresh as-of dates, re-pull holdings, regenerate charts). Do **not** create dated parallel copies — git history is the audit trail.

## Learning from sell-side institutional research

The bank analog here is **flow / positioning notes, not holdings-overlap notes** — banks rarely publish a 2-vs-4-fund holdings join, so the report skeleton above stays (it is already strong and N-PORT-native). What transfers is the **crowding and passive-flow framing** that converts a mechanical holdings join into a *correlated-drawdown* verdict. The single most transferable idea: **two ETFs sharing the single most crowded consensus name co-drawdown harder than their headline overlap % implies.**

**Add a crowding & positioning layer (mirror MS "Collision of Themes" / "AI Still Taking Center Stage").** Morgan Stanley flags concentration as *"this exposure is the consensus crowded trade"* (e.g. `算力板块估值偏高、机构持仓拥挤`; AI names >80% of the Taiwan index weight) — the qualitative crowding verdict the overlap skill lacks. See **Step 4.5** in the Workflow section above. For each shared top-10 name, annotate whether it is the consensus crowded trade and cite the evidence; a crowding adjective ("crowded", "concentrated") must always carry a sourced number, never ship bare.

**Decompose, don't assert (mirror GS Index-Strategy rebalancing notes).** GS rebalancing notes cascade market-level flow → sector-level flow → named-stock winners/losers (`科技硬件与半导体板块遭遇全市场最大被动资金流出24亿美元`). The overlap report should never state a shared-weight number without immediately naming the **2–3 positions that dominate it** — pair every aggregate with its named drivers, the way GS pairs `韩国流出121亿美元` with the stocks that drove it.

**Benchmark concentration, don't just scalar it (mirror GS/MS "vs history / vs positioning percentile").** A Herfindahl of 1500 means nothing to the reader in isolation. Report top-10 weight and Herfindahl **as a percentile vs a peer set (SPY/QQQ/sector-ETF references) or vs the fund's own history** so "concentrated" carries a number — folded into Step 4 below.

**Denominate every crowding figure in money AND as % of a stated base (mirror GS `占自由流通市值1.3%`).** Never a bare percentage with no denominator. Any positioning / crowding figure carries both absolute money and % of a stated base (AUM, free-float, index weight) — this is the same discipline as the existing "never sum percentages across different denominators" guardrail, applied to the new positioning numbers.

All new numbers obey the project citation + numerical-accuracy standard: every figure traces to a source that **literally contains it** (deep URL, the computed oneoff script, or a `db/zsxq.db` PDF read), and the `db/zsxq.db` library is **read-only** (Tier-1 safety rule).

*The concrete workflow implementation of this layer is **Step 4.5 — Crowding & positioning context**, defined in the Workflow section above (between Step 4 and Step 5).*

## What this skill does NOT do

- It does not generate active-fund vs index-fund tracking-error analysis as a standalone deliverable — touched as a metric only.
- It does not predict future overlap (e.g. ARK-style funds with high turnover) — the analysis is anchored to the most recent snapshot; rapid rebalancers get a "stale-by" caveat.
- It does not score one ETF as "better" than another — it surfaces the duplicative / complementary / orthogonal verdict, not a recommendation. Recommendation is the reader's job given their portfolio context.
- It does not handle non-40-Act funds (UCITS, ICAVs, Bermuda-domiciled feeders) — those don't file N-PORT. If the user passes a non-US fund, flag it and either skip or rely on issuer-published holdings only.
- It does not cover leveraged or inverse ETFs as a meaningful "overlap" subject — the daily-rebalance mechanics make holdings comparison structurally misleading (see also `take-profit-lab` § leveraged ETFs guardrail).
