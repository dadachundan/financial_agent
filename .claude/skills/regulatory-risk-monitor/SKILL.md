---
name: regulatory-risk-monitor
description: Track a specific regulatory / legal / antitrust / FDA / policy risk affecting a single ticker — producing a 3,000–6,000 word bilingual markdown report with risk summary, exposure map (revenue / costs / valuation impact), evidence timeline, market pricing reaction, and dated scenario triggers. Distinct from `company-research` Section 9 (point-in-time risk inventory): this skill is *ongoing monitoring* of a named regulatory file (a court case, FDA AdComm window, FTC/DOJ investigation, MIIT/CSRC inquiry, EU DG-COMP case, etc.). Reports saved to `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md` (and `..._zh.md`). Use when the user asks "track the X case on <ticker>", "FDA AdComm risk for <ticker>", "antitrust monitor on <ticker>-<topic>", or "regulatory tracking on <ticker>".
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
- The user wants M&A deal-specific regulatory tracking (antitrust on a specific deal) — use [[ma-event-tracker]]; that skill covers M&A-antitrust within its standard workflow.
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

## Report language

**Default: produce both English AND Simplified Chinese.** Same rule as [[company-research]]. Single-language overrides via `--en-only` / `--zh-only` / `English only` / `用中文即可`.

Bilingual technical terms in Chinese reports: `regulator / 监管机构`, `docket / 案件档案`, `consent decree / 同意令`, `injunction / 禁令`, `cease and desist / 停止令`, `Advisory Committee / 顾问委员会 (AdComm)`, `New Drug Application / 新药申请 (NDA)`, `Investigational New Drug / 临床试验申请 (IND)`, `Premarket Notification / 上市前通知 (510(k))`, `Section 2 / 反垄断法第二条 (谢尔曼法案)`, `Section 7 / 克莱顿法案第七条`. Keep regulator acronyms (FDA, FTC, DOJ, EU, SAMR, MOFCOM, CSRC, MIIT, CMA, BaFin, JFTC, etc.) and case numbers in original form.

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

For each exposure category, quantify the linkage where the disclosure allows:

| Category | What to capture | Where to find it |
|---|---|---|
| **Revenue exposure** | % of revenue from products / regions / customers affected by the rule | 10-K Segment / Geographic notes; risk-factor disclosures |
| **Cost exposure** | Cost-of-compliance estimates; R&D pivot costs; recall costs (for FDA) | Risk-factor disclosure, 10-K Legal Proceedings, sell-side notes |
| **Valuation exposure** | Multiple-compression scenarios from analyst notes; comparable historical re-rating | Sell-side notes; precedent re-ratings |
| **Capital structure exposure** | Fines, settlements, escrow / contingent liability accruals | 10-K Footnote (Contingent Liabilities); 10-Q updates |
| **License-to-operate exposure** | Worst case (license revocation, divestiture, breakup, criminal referral) | Regulator's prior actions on analogous cases |

Each cell is sourced inline. Where the company hasn't disclosed (e.g. revenue %), say `not disclosed` rather than estimating.

### Step 4 — Market pricing reaction

For each entry in the evidence timeline that the market could trade on:

- 1-day return on the affected ticker (vs. SPY for US, vs. relevant sector ETF, vs. domestic index for non-US).
- 5-day cumulative return.
- 30-day cumulative return.
- Implied-volatility snapshot if options trade (note: implied-vol context only; this skill is not an options skill).

If a prediction market exists (Kalshi / Polymarket), cite the contract URL and the current price as a market-implied probability.

### Step 5 — Scenarios and triggers

Three named paths with explicit triggers:

| Scenario | Outcome | Triggers | Estimated probability |
|---|---|---|---|
| **Bull** (for the company) | <e.g. case dismissed / FDA approval / consent decree light> | <observable conditions> | X% |
| **Base** (consensus path) | <e.g. settlement with divestiture / FDA approval with REMS> | <observable conditions> | Y% |
| **Bear** (for the company) | <e.g. injunction / FDA non-approval / criminal referral / forced breakup> | <observable conditions> | Z% |

Probabilities should sum to 100% and represent a reasonable spread. Single-point estimates ("70% likely the case clears") are overconfident; ranges with named triggers ("30% bull / 50% base / 20% bear, triggers below") replace verdicts.

### Step 6 — Watch list (what to monitor next)

1–3 specific dated events most likely to move the verdict. Each carries:
- Date (or window).
- What's happening.
- Which scenario the outcome supports.
- Source / calendar URL for the date.

Example: "FDA AdComm meeting July 15-16 → bear if voting committee splits >5 votes against; base if 7-5 in favor; bull if 9+ in favor [FDA AdComm calendar URL]."

### Step 7 — Write the report

Save to `reports/regulatory/<TICKER>_<topic-slug>_<YYYY-MM-DD>.md`. Suggested structure:

1. **Risk Summary** (200–400 words) — the case in plain language; what's at stake; current status.
2. **Exposure Map** — five-category table from Step 3.
3. **Evidence Timeline** — table from Step 2.
4. **Market Pricing** — reactions on key dates + prediction-market price if any.
5. **Scenarios & Triggers** — three-path table from Step 5.
6. **What to Watch Next** — Step 6's 1–3 events.
7. **Historical Analogs** (optional) — similar cases against other companies + their resolution + market reaction. Use only when an analog clearly fits and is well-documented.
8. **Data Used** manifest (mandatory).
9. **References** — every URL.

### Step 8 — Verify

- Confirm every dated event has a working URL (HTTP 200).
- Confirm every quantitative exposure figure traces to a primary source (10-K, regulator filing, etc.).
- Spot-check ≥3 stock-reaction numbers vs yfinance.
- Stop any test servers used during chart rendering.

## Output Format (mandatory blocks)

Every report must contain:

1. **Risk Summary** at the top (one bolded sentence + ~200-400 word context).
2. **Exposure Map** as a five-category table.
3. **Evidence Timeline** as a chronological table.
4. **Scenarios** as a three-path table with triggers.
5. **Watch List** with dated events.
6. **`## Data Used / 数据来源清单`** manifest.
7. **`## Guardrails for this monitor`** block.

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
- It does not produce M&A deal-specific regulatory tracking — that's [[ma-event-tracker]], which has its own antitrust section.
- It does not give legal advice.
- It does not predict regulator outcomes from partisan reasoning.
- It does not maintain alerts on the case — periodic monitoring is the user's responsibility (or use [[loop]] for scheduled re-runs).
- It does not score the company's overall ESG / governance — single-case scope only.
- It does not handle cases without a public docket / file / case number — there's nothing to anchor on; decline.
