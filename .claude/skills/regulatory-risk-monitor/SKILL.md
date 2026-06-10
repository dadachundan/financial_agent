---
name: regulatory-risk-monitor
description: Track a specific regulatory / legal / antitrust / FDA / policy risk affecting a single ticker — producing a 3,000–6,000 word English markdown report (Simplified Chinese companion available on explicit request) with risk summary, exposure map (revenue / costs / valuation impact), evidence timeline, market pricing reaction, and dated scenario triggers. Distinct from `company-research` Section 9 (point-in-time risk inventory): this skill is *ongoing monitoring* of a named regulatory file (a court case, FDA AdComm window, FTC/DOJ investigation, MIIT/CSRC inquiry, EU DG-COMP case, etc.). Reports saved to `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md` (Chinese companion at `..._zh.md` only when requested). Use when the user asks "track the X case on <ticker>", "FDA AdComm risk for <ticker>", "antitrust monitor on <ticker>-<topic>", or "regulatory tracking on <ticker>".
---

# Regulatory Risk Monitor

Deliverable: a 3,000–6,000 word markdown report tracking **one specific regulatory file** against **one company**. Output answers six questions:

1. **What's the regulatory file?** Regulator + jurisdiction + decision window + plain-language summary of the rule / case / investigation / docket.
2. **Where does it hit the company?** Revenue / cost / capital-structure / license-to-operate exposure with quantified linkage.
3. **What's happened so far?** Dated evidence timeline (filings, agency statements, court orders, hearings).
4. **What is the market pricing?** Stock reaction on key dates; implied probability if a tradable instrument exists.
5. **What are the scenarios?** Bear / base / bull paths with named, dated triggers.
6. **What should the user watch next?** The 1–3 dated events most likely to move the verdict.

Adapted from the [LLMQuant regulatory risk monitor](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-events/workflows/regulatory-risk-monitor.md) (MIT), re-pointed at SEC 8-K Item 8.01 + jurisdiction-specific regulator portals + court records.

## When to use

The user says any of:

- "Track the FTC antitrust case on Microsoft-Activision"
- "FDA AdComm risk for <biotech ticker> Q3"
- "DOJ Section 2 case on Google search — what's the timeline?"
- "Track the EU AI Act exposure for NVIDIA"
- "Regulatory monitor on TSMC — CHIPS Act audit"
- "SAMR antitrust on the X-Y JV"
- "CSRC inquiry on <A-share ticker>"
- "EPA Superfund risk for <industrial ticker>"

The skill is **case-specific**, not company-wide. The user must name *which* regulatory file. If they ask "what regulatory risks does <ticker> have?" — that's [[company-research]] Section 9, not this skill. Ask for the specific case.

## When NOT to use

- The user wants a Section-9-style inventory of all regulatory risks for a company — use [[company-research]] (or read its existing Section 9 if a report exists).
- The user wants M&A deal-specific regulatory tracking (antitrust on a specific deal) — use [[catalyst-calendar]] mode C (single-deal M&A monitor); that mode covers M&A-antitrust within its standard workflow.
- The user wants legal advice — decline. The skill summarizes filings and surfaces dated events; it does not opine on legal outcomes.
- The risk has no specific docket / file / case number — there's nothing concrete to track; the skill becomes speculation. Ask the user to name the file.
- The "regulatory risk" is actually a tax / accounting / FX issue without a regulator file — wrong skill; use [[company-research]] risk section or a one-off note.

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim. Regulatory-specific failure modes:

- **Never invent a docket entry, agency statement, hearing date, or decision date.** Every dated item in the timeline must trace to a verifiable primary source — agency press release, court filing (PACER / CourtListener), filing on EDGAR (8-K Item 8.01), or the regulator's case database. "Hearing scheduled for May 14" with no link is a defect.
- **Never give legal advice.** The skill summarizes regulatory filings, surfaces market reactions, and lists triggers. It does not state "this will go in the company's favor" / "the FDA will approve" / "the court will rule for the defendant". Probability ranges with named triggers replace legal verdicts.
- **Never infer outcomes from political preference.** "A Republican FCC will rule X" / "a Democratic FTC will block Y" is not analysis — it's editorializing. Regulator track record on analogous cases is fair game; partisan reasoning is not.
- **Never source agency outcomes to news articles** when the regulator's own decision is public. Cite the docket / press release / court order at a specific URL.
- **Never quantify exposure from sell-side memory.** "FDA non-approval would cost $X B" must come from the company's own risk-factor disclosure, an industry-research note, or be explicitly labeled an analyst-built scenario.
- **Never confuse different regulators in adjacent jurisdictions.** A U.S. DOJ case is not an EU DG-COMP case is not a UK CMA case is not a China SAMR case. Each has its own docket, its own timeline, its own remedies.
- **Classify the rule's true reach before quantifying it.** The single most over-priced error in a regulatory note is reading the headline as broader than the instrument. Before any number, sort the file into one of three buckets: **(i) cleanup of grey / illegal channels** (steers existing flow into a compliant pipe — bounded impact), **(ii) a genuine new restriction** (shrinks the addressable market on new business), or **(iii) an outright ban** (removes the business). J.P. Morgan's China cross-border-WM note bounds HSBC/STAN impact precisely because the State Council ODI rule targets *illegal* cross-border marketing and reroutes flow into Stock Connect / QDII — it is bucket (i), not a blanket ban — so the rev/EPS hit is small even though the headline reads severe. Bound the worst case with the regulator's **own documented remedy history** (e.g. mandatory price cut after the 3rd generic; divestiture in prior concentration cases) — never a guessed number.

## Learning from sell-side institutional research

Sell-side regulatory / policy notes (J.P. Morgan "Global Banks" single-file impact notes, Morgan Stanley pharma patent-cliff / FDA notes, Bernstein thematic policy notes, GS/MS "Three Actionable Ideas" / Weekly Kickstart) share a tighter structure than the generic monitor. The single best analog is **JPM's "China investment regulations triggering WM revenue uncertainty for HSBC/STAN/UBS/BAER"**, which tracks one named regulatory file (June-1 State Council ODI rule, effective July-1) and maps it to per-name rev% / EPS%. Fold these moves in; they sharpen, never replace, the rules above.

- **Lead with the quantified per-name number, not prose.** Mirror JPM's headline — *"HSBC rev -1.9% / EPS -3.9%, STAN -1.6% / -4.9%"* is the first line, context second. The Risk Summary's opening sentence must state the single most important quantified exposure as a **base + extreme range** (`Base case: revenue -X%, EPS -Y%; extreme case -Z%`), each figure traceable to a source cited in that same sentence per the project's numerical-accuracy rule. Plain-language status follows the number.
- **Surface a standalone "Scope & Status of the Rule" block.** Every strong analog states, as a scannable unit distinct from the timeline: **(a) effective date**, **(b) in-scope vs out-of-scope** ("new business only / existing accounts unaffected"), **(c) finalized vs pending implementing rules**, **(d) issuing body + instrument + deep URL**. JPM's most consistent structural element is this triplet stated inline on first mention — *"issued June-1, effective July-1, new business only."* Do not bury it in the evidence timeline.
- **Show the EPS derivation through the disclosed-share chain.** JPM derives EPS impact = *(affected revenue share) × (segment margin / drop-through)*, each input from the bank's own disclosure (HK WM = 8% of HSBC group revenue; visitor-driven = 25% of HK WM). The exposure-map cell must show the arithmetic so a reader re-derives the EPS number — this is the literal application of the project's "derived numbers must have both inputs sourced in the paragraph" rule. A bare "-3.9% EPS" with no chain is a defect.
- **Bound each exposure with a base AND an extreme column.** Two points per name, never a single estimate: JPM gives base-case and worst-case EPS for each bank. The extreme case is the regulator's documented-remedy ceiling (see "classify the rule's true reach" above), not a guess.
- **Rank peers under the SAME file — even for a single-ticker monitor.** JPM ranks HSBC vs STAN vs UBS vs BAER by exposure (China <60% of net-new-money insulates the Swiss banks). A single-ticker report still benefits from "peers more / less exposed to the identical rule" to calibrate whether the market reaction is name-specific or sector-wide.
- **Read cross-sectional stock moves as differentiated pricing.** UBS +2% / BAER +3% rose while HSBC -3% / STAN -6% fell on the *same* rule — JPM reads this as the market correctly pricing lower China dependence. Market Pricing must compare the affected name to same-file peers, not only vs SPY / sector. Print direction + magnitude together (`HSBC -3%, STAN -6%, UBS +2%`) so the cross-sectional spread is visible at a glance.
- **Make the "rules-pending" state a first-class scenario.** JPM repeatedly flags that individual implementing rules are pending (multi-ministry) and says equity-risk-premium stays elevated until they land — clarification *timing*, not the ultimate outcome, is the dominant near-term driver. The scenario tree needs a `rules-pending` state where the verdict hinges on when detailed rules drop, not on bull/base/bear of the final outcome.
- **Run the historical analog as a ranked precedent test.** JPM tests the HK-property thesis against the 2004-06 and 2016-18 hiking cycles (property still rose); MS uses Canada / India / Brazil generic-approval outcomes as live read-throughs for the US/China Ozempic outcome. When a documented precedent exists, the analog is a *core argument* (prior rule/case → outcome → market reaction), not optional garnish — keep the "use only when it clearly fits and is well-documented" guardrail.
- **Name the resolving data series in the Watch List, not just the next date.** Analogs always identify *what evidence resolves the uncertainty* — "multi-ministry implementing ODI rules (no date set)", a specific economic print, inventory de-stocking data, a docket entry number. A Watch List entry that names a date but not the resolving document / series is half-done.
- **Keep the sell-side rating + PT as a labeled overlay, never as fact.** Where a rating / price target (incl. the local zsxq library, `db/zsxq.db`, read-only) frames the valuation exposure, surface it as `*Analyst view:*` per the project's company-research labeling rule with a deep URL — never fold a PT into a filing citation. JPM's 2028E P/E-per-name cushion is an overlay on the disclosure, not a substitute for it. **Pair every borrowed PT with the stock's price on the note's date + the implied upside** (`PT $120 vs $98 @ 2026-04-30 → +22%`) — that report-date price is what makes the analyst's cushion legible; pull it from `stock_price_target_db` (`report_date_price` / `upside_pct`, shown at `/pt`) or a yfinance close on the note's date, never today's spot, and write `report-date price n/a` if it isn't available.

## Report language

**Default behavior: English only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need the Chinese companion every time. (The substantive research skills `company-research` / `compare-companies` / `earnings-analysis` / `sector-overview` still default bilingual; this skill does not.)

**Chinese opt-in (any of these triggers a Chinese companion file alongside the English):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

When a Chinese companion is produced, use bilingual technical terms: `regulator / 监管机构`, `docket / 案件档案`, `consent decree / 同意令`, `injunction / 禁令`, `cease and desist / 停止令`, `Advisory Committee / 顾问委员会 (AdComm)`, `New Drug Application / 新药申请 (NDA)`, `Investigational New Drug / 临床试验申请 (IND)`, `Premarket Notification / 上市前通知 (510(k))`, `Section 2 / 反垄断法第二条 (谢尔曼法案)`, `Section 7 / 克莱顿法案第七条`. Keep regulator acronyms (FDA, FTC, DOJ, EU, SAMR, MOFCOM, CSRC, MIIT, CMA, BaFin, JFTC, etc.) and case numbers in original form.

**Filenames (English / pinyin first per the project rule):**
- English: `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md`
- Chinese: `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>_zh.md`
- Topic slug is short kebab-case English (e.g. `ftc-antitrust-search`, `fda-adcomm-bla-q3`, `samr-jv-concentration`, `eu-ai-act-tier1`, `chips-act-audit`).

**Update-in-place rule:** one report per (ticker, topic-slug) tuple. Each tracking pass bumps the date suffix. Older snapshots may persist if the case spans many months — they form the history.

## Data sources

### Primary: agency-specific docket / case database

| Regulator | Where to look | What's available |
|---|---|---|
| **U.S. SEC** | Latest 8-K Item 8.01 ("Other Events") on EDGAR for the affected ticker | Company self-disclosure of material regulatory events |
| **U.S. DOJ Antitrust Division** | `justice.gov/atr/cases` + DOJ press release archive | Civil / criminal antitrust case docket, consent decrees, indictments |
| **U.S. FTC** | `ftc.gov/legal-library` + press release archive | Section 5 investigations, merger reviews, consent orders, AdminTrials |
| **U.S. FDA** | `fda.gov/drugs` (Drugs@FDA database), `fda.gov/devices` (510(k)/PMA databases), AdComm calendar at `fda.gov/advisory-committees/advisory-committee-calendar` | NDA/BLA application status, AdComm meeting dates and outcomes, complete response letters |
| **U.S. FCC** | `fcc.gov` ECFS docket search | Spectrum auctions, license transfers, Section 214 transactions |
| **U.S. EPA** | `epa.gov/superfund` for Superfund; `epa.gov/enforcement` for enforcement actions | Site listings, consent decrees, civil penalties |
| **U.S. courts** | CourtListener (free) or PACER (paid) | Civil litigation dockets — used for shareholder suits, fiduciary-duty claims, IP litigation |
| **EU Commission DG-COMP** | `ec.europa.eu/competition/elojade/isef/index.cfm` (case M.xxxxx for mergers, AT.xxxxx for antitrust) | Merger decisions, antitrust prohibitions, state-aid rulings |
| **UK CMA** | `gov.uk/cma-cases` | Merger investigations, market investigations, consumer enforcement |
| **China SAMR** (State Administration for Market Regulation) | Press release archive on samr.gov.cn | Concentration cases (`经营者集中`), monopoly investigations, administrative penalties |
| **China CSRC** | CSRC public-comment letters + administrative-penalty decisions | Listed-company inquiries, IPO comment letters, enforcement actions |
| **China MIIT** | MIIT formal notices | Industry-policy actions affecting designated sectors (auto, semis, telecom) |
| **Japan JFTC** | `jftc.go.jp/en/pressreleases` | Antitrust enforcement, M&A clearance |
| **Korea KFTC** | `ftc.go.kr/eng/index.do` | Antitrust enforcement, M&A clearance |
| **Germany BaFin** | `bafin.de` | Financial supervisory actions, market-manipulation cases |

### Primary: company self-disclosure on EDGAR

For US issuers, **the 8-K Item 8.01 ("Other Events") filing is the canonical disclosure** of material regulatory developments outside the routine quarterly cadence. Pull the last 12 months of 8-Ks for the ticker and filter for Item 8.01:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://data.sec.gov/submissions/CIK<padded>.json" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); r=d['filings']['recent']; [print(r['filingDate'][i], r['accessionNumber'][i], r['primaryDocument'][i]) for i,f in enumerate(r['form']) if f == '8-K']"
```

Then fetch each filing's primary doc and grep for "Item 8.01" or the topic keywords (`FDA`, `antitrust`, `DOJ`, `FTC`, `consent decree`, etc.).

Also check:
- **10-K Risk Factors** — the most recent 10-K's risk-factor language on this specific regulatory category.
- **10-Q Risk Factors update** — any quarterly amendments to the risk-factor disclosure.
- **10-K / 10-Q Legal Proceedings note** — case-by-case docket history.

### Primary: court records

For US civil cases:
- **CourtListener** (free, ad-supported) — `courtlistener.com/?type=r` for the RECAP archive of PACER documents.
- **PACER** (paid, $0.10 per page) — `pacer.uscourts.gov` for cases not yet in RECAP.

Resolve the case by:
- Case caption (e.g. `United States v. Google LLC, 1:20-cv-03010, D.D.C.`)
- Court + docket number — primary lookup key.
- Plaintiff / defendant name searches as fallback.

### Secondary: news + analyst commentary

- WebSearch for the last 90 days on `<ticker> + <regulator> + <topic>` and `<docket-number>` and `<case-caption>`.
- Sell-side commentary (Bloomberg, Reuters, WSJ, FT) for market-reaction interpretation — cite the article with a date in the link title.
- Industry-specific trade press (RAPS for pharma, Mlex for antitrust, Politico for policy) for non-mainstream-press updates.
- **Local zsxq broker-report library (`db/zsxq.db`, read-only)** — a permitted secondary source for the *sell-side framing* of a regulatory file (the exposed-vs-insulated peer split, the valuation-cushion read, broker price targets on the affected name). Surface any rating / PT pulled from it as `*Analyst view:*` with a deep URL per the company-research labeling rule — **never blended into a filing citation**. Read via the read-only zsxq helper scripts; never write to or run destructive SQL against the DB.

### Quantitative: market reaction

- yfinance for the ticker's price action around each key regulatory date. Compute 1-day, 5-day, and 30-day returns vs sector ETF on key dates.
- If a prediction market (Kalshi / Polymarket) has a contract on the outcome, the contract price is a market-implied probability — note it explicitly and cite the contract URL.

## Workflow

### Step 0 — Parse inputs

User input must name:
- The **ticker** (or company name).
- The **specific regulatory file** — case number, docket, AdComm window, agency investigation, rule docket. If the user supplied only a topic ("antitrust"), ask for the specific case before proceeding.

Resolve:
- Ticker + CIK (or domicile portal CIK-equivalent).
- Regulator (one of the named portals above).
- Case identifier (docket number, M.xxxxx, AdComm meeting ID, etc.).
- Topic slug (kebab-case English; used in filename).

### Step 1 — Pull canonical regulatory documents

For the named case:
1. Fetch the regulator's docket / case page; save the case caption, filing dates, current status.
2. Pull all material filings since case open (complaints, motions, orders, schedules, hearings).
3. Fetch the latest 12 months of company 8-Ks (Item 8.01) for the affected ticker; filter for related items.
4. Pull the latest 10-K Risk Factors + Legal Proceedings sections (often most comprehensive).
5. Save under `oneoff/regulatory_<TICKER>_<topic-slug>/`.

### Step 1.5 — Pin the scope & status of the rule

Before building the timeline, classify the file and fix its scope on one scannable block (mirrors JPM's most consistent structural element). Capture:

- **Issuing body + instrument** (regulation / docket / order) with a deep URL.
- **Effective date** (and any phased dates).
- **In-scope vs out-of-scope** — e.g. "new business only / existing accounts unaffected", which products / regions / customer cohorts the rule reaches and which it explicitly does not.
- **Finalized vs pending** — which provisions are final and which await implementing rules (and from which body). Pending implementing rules are a *named source of policy uncertainty*, not a gap to paper over.
- **True reach bucket** — (i) cleanup of grey/illegal channels, (ii) genuine new restriction, or (iii) outright ban (per the Core-principle step). This bucket bounds Step 3's worst case before any number is written.

This block becomes the "Scope & Status of the Rule" report block. State the regulator-date-scope triplet inline on first mention wherever the rule is referenced (`issued June-1, effective July-1, new business only`).

### Step 2 — Build the evidence timeline

Chronological table — every entry is a date + event + source:

| Date | Event | Source |
|---|---|---|
| YYYY-MM-DD | Case filed / agency investigation opened | [docket / press release URL] |
| YYYY-MM-DD | Company first disclosed exposure in 10-K Risk Factors | [10-K URL] |
| YYYY-MM-DD | First court order / agency notice | [court / agency URL] |
| YYYY-MM-DD | Subpoena / second request / CID issued | [filing URL] |
| YYYY-MM-DD | Hearing / meeting / AdComm date | [calendar URL] |
| YYYY-MM-DD | Company comment / response | [8-K URL] |
| YYYY-MM-DD | Decision / order / consent decree | [order URL] |

Every row carries an inline citation. The table is read by skim; the URLs are the proof.

### Step 3 — Build the exposure map

For each exposure category, quantify the linkage where the disclosure allows — and give **two points per row (base + extreme), not one**. The extreme case is the regulator's documented-remedy ceiling, never a guess.

| Category | What to capture | Base impact | Extreme / worst-case impact | Where to find it |
|---|---|---|---|---|
| **Revenue exposure** | % of revenue from products / regions / customers affected by the rule | base rev% hit | extreme rev% hit | 10-K Segment / Geographic notes; risk-factor disclosures |
| **Cost exposure** | Cost-of-compliance estimates; R&D pivot costs; recall costs (for FDA) | base $ / % | extreme $ / % | Risk-factor disclosure, 10-K Legal Proceedings, sell-side notes |
| **Valuation exposure** | Multiple-compression scenarios from analyst notes; comparable historical re-rating | base re-rating | extreme re-rating | Sell-side notes; precedent re-ratings |
| **Capital structure exposure** | Fines, settlements, escrow / contingent liability accruals | base accrual | extreme accrual | 10-K Footnote (Contingent Liabilities); 10-Q updates |
| **License-to-operate exposure** | Worst case (license revocation, divestiture, breakup, criminal referral) | likely remedy | documented-precedent ceiling | Regulator's prior actions on analogous cases |

**Show the EPS / valuation derivation in the cell.** Translate the rule into EPS through the disclosed-share chain, JPM-style: `EPS impact = (affected revenue share) × (segment margin / drop-through)`, with **both inputs cited inline** so a reader re-derives the number (this is the project's "derived numbers must have both inputs sourced" rule). Example: *"HK WM = 8% of group revenue [10-K seg note]; ~25% visitor-driven, ~70% drop-through [risk factor] → ~-3.9% EPS base."* A bare "-3.9% EPS" with no chain is a defect. A worked end-to-end example lives in [`references/exposure_grid_example.md`](references/exposure_grid_example.md).

Each cell is sourced inline. Where the company hasn't disclosed (e.g. revenue %), say `not disclosed` rather than estimating.

**Peer ranking under the same file.** Even for a single-ticker monitor, add a short row/grid ranking peers exposed to the *identical* rule (most → least exposed, with the one disclosed metric that drives the ranking). This calibrates whether the market reaction is name-specific or sector-wide (JPM: HSBC/STAN exposed, UBS/BAER insulated because China <60% of net-new-money).

### Step 4 — Market pricing reaction

For each entry in the evidence timeline that the market could trade on:

- 1-day return on the affected ticker (vs. SPY for US, vs. relevant sector ETF, vs. domestic index for non-US).
- 5-day cumulative return.
- 30-day cumulative return.
- Implied-volatility snapshot if options trade (note: implied-vol context only; this skill is not an options skill).

If a prediction market exists (Kalshi / Polymarket), cite the contract URL and the current price as a market-implied probability.

**Cross-sectional peer reaction (required when peers share the file).** Beyond the primary ticker's grid vs SPY / sector, add a small peer-reaction table — the affected name *vs the same-file peers* on the key regulatory date, direction + magnitude together (`HSBC -3%, STAN -6%, UBS +2%, BAER +3%`). The cross-sectional spread is the market's differentiated pricing of exposure; a name falling while an insulated peer rises on the *identical* rule is the strongest single read of whether the move is name-specific or sector-wide. Keep the full 1d/5d/30d-vs-benchmark grid for the primary ticker.

### Step 5 — Scenarios and triggers

Named paths with explicit triggers. Include the standard bull / base / bear **plus a `rules-pending` state** whenever implementing rules are still outstanding:

| Scenario | Outcome | Triggers | Estimated probability |
|---|---|---|---|
| **Bull** (for the company) | <e.g. case dismissed / FDA approval / consent decree light> | <observable conditions> | X% |
| **Base** (consensus path) | <e.g. settlement with divestiture / FDA approval with REMS> | <observable conditions> | Y% |
| **Bear** (for the company) | <e.g. injunction / FDA non-approval / criminal referral / forced breakup> | <observable conditions> | Z% |
| **Rules-pending** (clarity overhang) | Outcome indeterminate; ERP / multiple stays elevated until detailed implementing rules land | <which body issues the rules; expected window if any> | W% |

The `rules-pending` state captures JPM's central point on the China ODI file — when implementing rules are outstanding, the dominant near-term driver is *clarification timing*, not the ultimate bull/bear outcome; the multiple stays de-rated until clarity lands. Probabilities should sum to 100% and represent a reasonable spread. Single-point estimates ("70% likely the case clears") are overconfident; ranges with named triggers ("30% bull / 50% base / 20% bear, triggers below") replace verdicts.

### Step 6 — Watch list (what to monitor next)

1–3 specific dated events most likely to move the verdict. Each carries:
- Date (or window) — or **"no date set"** when the resolver is undated.
- What's happening.
- **The resolving data series / document by name** — not just "the next hearing", but the specific evidence that settles the uncertainty: "multi-ministry implementing ODI rules (no date set)", a named economic print, an inventory de-stocking series, a docket entry number, a complete-response-letter. The analogs always name *what resolves it*, not only *when*.
- Which scenario the outcome supports.
- Source / calendar URL for the date or document.

Example: "FDA AdComm meeting July 15-16 → bear if voting committee splits >5 votes against; base if 7-5 in favor; bull if 9+ in favor [FDA AdComm calendar URL]."

Example (undated resolver): "Multi-ministry implementing rules for the ODI regulation — no date set; until they land, the `rules-pending` state dominates and the multiple stays de-rated [State Council notice URL]."

### Step 7 — Write the report

Save to `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md`. Suggested structure:

1. **Risk Summary** (200–400 words) — **lead with the single most important quantified per-name exposure number as a base + extreme range** (`Base case: revenue -X%, EPS -Y%; extreme case -Z%`), each figure traceable to a source cited in that same sentence (JPM "Global Banks" headlines with HSBC -1.9% rev / -3.9% EPS). Then the case in plain language; what's at stake; current status.
2. **Scope & Status of the Rule** — Step 1.5's scannable block: effective date, in-scope vs out-of-scope, finalized vs pending implementing rules, issuing body + instrument + deep URL, true-reach bucket.
3. **Exposure Map** — five-category base+extreme table from Step 3, with EPS derivations shown and the peer-ranking row.
4. **Evidence Timeline** — table from Step 2.
5. **Market Pricing** — primary-ticker reactions on key dates + the cross-sectional peer-reaction table + prediction-market price if any.
6. **Scenarios & Triggers** — table from Step 5, including the `rules-pending` state where applicable.
7. **What to Watch Next** — Step 6's 1–3 events, each naming the resolving data series / document.
8. **Historical Analogs** (recommended when a documented precedent exists; optional otherwise) — run as a ranked precedent test: prior analogous rule/case → outcome → market reaction (JPM tests HK property vs the 2004-06 / 2016-18 hiking cycles; MS uses Canada/India/Brazil generics as live read-throughs). Keep the "use only when an analog clearly fits and is well-documented" guardrail.
9. **Data Used** manifest (mandatory).
10. **References** — every URL.

## Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — the regulated technology, drug, or process at the center of the case (e.g. an FDA-reviewed drug's mechanism of action / dosing pathway, a medical device's implant procedure, the chip-fab step a CHIPS-Act audit turns on, the cross-border money-flow channel an ODI rule reroutes, the market-structure or search-ad mechanic an antitrust complaint targets), a manufacturing or scientific process, a complex product architecture, an unfamiliar business model, or a market-structure concept — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* what is actually being regulated, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

### Step 8 — Verify

- Confirm every dated event has a working URL (HTTP 200).
- Confirm every quantitative exposure figure traces to a primary source (10-K, regulator filing, etc.).
- Spot-check ≥3 stock-reaction numbers vs yfinance.
- Stop any test servers used during chart rendering.

## Output Format (mandatory blocks)

Every report must contain:

1. **Risk Summary** at the top — the bolded lead sentence **must open with the single most important quantified per-name exposure as a base + extreme range** (`revenue -X% / EPS -Y% base, -Z% extreme`), each figure sourced inline — then ~200-400 word context.
2. **Scope & Status of the Rule** block — effective date, in-scope vs out-of-scope, finalized vs pending implementing rules, issuing body + instrument + deep URL, true-reach bucket.
3. **Exposure Map** as a five-category table with **base + extreme columns** and the EPS derivation shown in-cell.
4. **Evidence Timeline** as a chronological table.
5. **Market Pricing** — primary-ticker grid **plus a cross-sectional peer-reaction table** when peers share the file.
6. **Scenarios** as a table with triggers, including a **`rules-pending` state** when implementing rules are outstanding.
7. **Watch List** with dated events, each naming the **resolving data series / document**.
8. **`## Data Used / 数据来源清单`** manifest.
9. **`## Guardrails for this monitor`** block.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Regulatory case primary sources**
- <Regulator> docket / case ID: <number>, status as of YYYY-MM-DD. Source: <case URL>.
- Material filings: <bulleted list of motions / orders / hearings with dates + URLs>.

**Company self-disclosure**
- 8-K Item 8.01 filings related to this matter (last 12 months): <list filings YYYY-MM-DD>. Source: SEC EDGAR.
- 10-K Risk Factors (FY filed YYYY-MM-DD) and Legal Proceedings note. Source: SEC EDGAR.
- 10-Q amendments to risk-factor disclosure (last 4 quarters).

**Market data**
- Ticker daily close on key event dates: <list dates>. Source: yfinance.
- Sector / index benchmark for the same dates.

**Prediction-market price (if exists)**
- Kalshi / Polymarket contract URL + price + as-of date.

**News and commentary (last 90 days)**
- <N> articles from Reuters / Bloomberg / WSJ / FT / trade-press, each with date and URL.

**Stale notices / coverage gaps**
- <bulleted list — court docket on PACER not retrieved, agency comment letter not yet public, redacted filing section, or "none">.
- E.g.: "Court docket entries beyond #34 not yet on CourtListener — relied on press summary of #35 (Reuters, 2026-05-12)."
```

## Guardrails

- **Do not give legal advice.** The skill summarizes filings and surfaces dated events. Statements like "the court will rule for the defendant" / "the FDA will approve" / "this case clears antitrust" are out of scope.
- **Do not invent a docket entry, hearing date, or agency statement.** Every dated item traces to a primary source.
- **Do not infer regulatory outcomes from political preference.** Regulator track record on analogous cases is fair game; partisan reasoning is not.
- **Do not source agency outcomes to news articles when the actual filing is public.** Cite the docket / press release / court order URL.
- **Do not confuse different regulators in adjacent jurisdictions.** Each has its own docket, timeline, and remedies.
- **Do not quantify exposure from sell-side memory.** Revenue / cost / valuation exposure must come from company disclosure, third-party research with a real URL, or be labelled an analyst-built scenario.
- **Do not blend a sell-side rating / price target into a filing citation.** Surface ratings / PTs (incl. anything from the read-only `db/zsxq.db` library) as `*Analyst view:*` with a deep URL — an overlay on the disclosure, never a substitute for it.
- **Do not quote a derived EPS / valuation number without showing its inputs.** The exposure cell must carry the `(affected revenue share) × (margin / drop-through)` chain with both inputs cited, so a reader re-derives the figure.
- **Do not call a probability with single-point confidence.** Three-path scenarios with named triggers replace "this is 80% likely to settle".
- **Do not skip the prior-disclosure check.** The 10-K Risk Factors language on this category is the company's own framing; quoting it verbatim grounds the analysis.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Output location

Save to `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md` (and `..._zh.md`). Create `reports/regulatory/` if missing.

Supplementary deliverables:
- Filings cache: `oneoff/regulatory_<TICKER>_<topic-slug>/`.
- Charts (optional): `reports/charts/regulatory_<TICKER>_<topic-slug>_*.png` — typically a price reaction chart on key event dates.

### Update-in-place rule

One report per (ticker, topic-slug) tuple per tracking pass. Each pass updates the date suffix. Snapshot history is allowed and may persist as multiple dated files if the case spans a long window — these form the audit trail; do not auto-consolidate without user confirmation.

## What this skill does NOT do

- It does not produce a company-wide risk inventory — that's [[company-research]] Section 9 / `references/risk_taxonomy.md`. This skill is one named case, deeply tracked.
- It does not produce M&A deal-specific regulatory tracking — that's [[catalyst-calendar]] mode C (single-deal M&A monitor), which has its own antitrust section.
- It does not give legal advice.
- It does not predict regulator outcomes from partisan reasoning.
- It does not maintain alerts on the case — periodic monitoring is the user's responsibility (or use [[loop]] for scheduled re-runs).
- It does not score the company's overall ESG / governance — single-case scope only.
- It does not handle cases without a public docket / file / case number — there's nothing to anchor on; decline.
