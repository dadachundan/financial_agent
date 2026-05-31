---
name: ma-event-tracker
description: Track an active or proposed M&A deal — target / acquirer / consideration / spread / milestones / break-risk / probability — producing a 3,000–6,000 word English markdown report (Simplified Chinese companion available on explicit request). Pulls from SEC EDGAR (S-4, DEFM14A, 425, 8-K Item 1.01 / 2.01), recent news, and antitrust / regulatory filings. Reports saved to `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md` (Chinese companion at `..._zh.md` only when requested). Use when the user asks "track the X-Y merger", "what's the spread on the Z deal?", "M&A status on <ticker>", "is the SNPS-ANSS deal closing?", or anything in the merger-arb / deal-status family.
---

# M&A Event Tracker

Deliverable: a 3,000–6,000 word markdown report on a single active (or recently-closed) M&A transaction. Output answers five specific questions:

1. **What's the deal?** Target, acquirer, consideration, implied value per target share, announcement date, expected close.
2. **What's the spread?** Current target price vs deal value; annualized return assuming the expected close date.
3. **Where are we on the milestone path?** Shareholder vote, antitrust approvals, financing condition, other closing conditions.
4. **What's the break risk?** Financing / antitrust / shareholder / litigation / acquirer-stock / macro.
5. **What's the probability range and what would change it?** Bear / base / bull paths with named triggers.

Adapted from the [LLMQuant M&A event tracker](https://github.com/LLMQuant/skills/tree/master/skills/llmquant-events/workflows/mna-event-tracker.md) (MIT), re-pointed at SEC EDGAR + web search for U.S. deals and cninfo / HKEX / TDnet for cross-border deals.

## When to use

The user says any of:

- "Track the SNPS-ANSS merger"
- "What's the deal spread on TTWO-Codemasters?"
- "M&A status on AVGO-VMW closing"
- "Is the CDNS-Hexagon D&E deal closing?"
- "Risk of break on the X-Y deal?"
- "Track the antitrust on TSMC-Intel JV"
- "Merger arb on Activision-Microsoft" (post-mortem also fine)

Supports:
- **Pending deals** (announced but not closed) — primary use case; produces spread + probability.
- **Pre-announcement speculation** (rumored deals with credible sourcing) — produces a deal-likelihood map; explicitly labels as speculation; no spread math.
- **Recently closed deals** (last 6 months) — produces post-mortem analysis of how the deal went vs the consensus pre-close view.

## When NOT to use

- Routine quarterly earnings — use [[earnings-analysis]].
- Pure regulatory / antitrust monitoring with no specific deal attached — use [[regulatory-risk-monitor]].
- Private-to-private transactions with no public disclosure — there's nothing to anchor the analysis on; decline.
- Spinoffs / reverse-Morris-trust splits — these are M&A-adjacent but follow a different filing pattern (Form 10, when-issued trading); skill applies imperfectly. Flag the limitation.

## Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim. M&A-specific failure modes:

- **Never invent a deal term.** Consideration mix (cash %, stock %, ratio), implied price, walk-away conditions, termination fee, expected close date — every one of these must come from a specific SEC filing (S-4, DEFM14A, 8-K Item 1.01, 425) or a verifiable press release URL.
- **Never compute a spread without current target price.** "Spread is 4.5%" requires: deal-implied value per share, current target price (with date), and the assumed days to close. Show all three.
- **Never quote a closing date the company hasn't stated.** "Expected to close in 2Q26" must trace to the deal proxy or a company press release. "Sometime in 2026" is fine if that's what the company said; "by April 2026" is not unless that's literally in a filing.
- **Never call a deal "likely to close" or "unlikely to close" without addressing the four standard break risks** (financing, antitrust, shareholder vote, litigation). A probability statement that ignores even one of these is incomplete.
- **Never source antitrust language to a press release** when the actual filing is public. DOJ / FTC consent decrees, EU Commission decisions, and CMA / SAMR filings all have permanent URLs — cite the docket, not a Bloomberg article.
- **Never confuse "merger consideration" with "fair value."** The deal price is what the buyer is paying; fair value is the target's standalone value. They are different and must not be conflated.

## Report language

**Default behavior: English only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need the Chinese companion every time. (The substantive research skills `company-research` / `compare-companies` / `earnings-analysis` / `sector-overview` still default bilingual; this skill does not.)

**Chinese opt-in (any of these triggers a Chinese companion file alongside the English):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

When a Chinese companion is produced, use bilingual technical terms: `M&A / 并购`, `target / 标的`, `acquirer / 收购方`, `consideration / 对价`, `implied value / 隐含估值`, `spread / 套利价差`, `expected close / 预计交割`, `termination fee / 终止费`, `antitrust / 反垄断`, `shareholder vote / 股东投票`, `definitive proxy / 最终代理征集书`. Keep ticker codes, regulator names (FTC, DOJ, SAMR, MOFCOM, CMA, EU), and case numbers in original form.

**Filenames (no date in filename body, but `<YYYY-MM-DD>` of the tracking pass at the end):**
- English: `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md` (e.g. `ANSS_SNPS_2026-05-31.md`)
- Chinese: `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>_zh.md`
- Use English/pinyin name (per the project filename rule), not Chinese-only. Mixed-domicile deals: `<English-Target>_<English-Acquirer>_<YYYY-MM-DD>.md` (e.g. `Hexagon-DE_Cadence_2026-05-31.md`).

**Update-in-place rule:** one report per ordered (target, acquirer) tuple. If a report from a prior tracking pass exists, update it in place (refresh the date suffix; git history records the trail). Do not pile up dated copies.

## Data sources

### Primary (SEC EDGAR — US deals)

For every U.S.-domiciled deal, pull the following from EDGAR. Resolve via the submissions JSON (`https://data.sec.gov/submissions/CIK<padded>.json`):

| Filing | Where to find it | What it contains |
|---|---|---|
| **8-K Item 1.01** | Both target's and acquirer's 8-Ks | "Entry into a Material Definitive Agreement" — the original merger-agreement disclosure |
| **8-K Item 2.01** | Both target's and acquirer's 8-Ks | "Completion of Acquisition or Disposition" — the closing disclosure |
| **8-K Item 8.01** | Both | "Other Events" — antitrust filings, financing updates, vote outcomes |
| **S-4** | Acquirer (if stock consideration) | Registration of acquirer shares for issuance to target shareholders — the master M&A prospectus |
| **DEFM14A** | Target | Definitive merger proxy — the shareholder vote disclosure; usually 200–400 pages with full deal terms, board justification, financial advisors' fairness opinions, projections |
| **PREM14A** | Target | Preliminary merger proxy — filed before DEFM14A; useful when DEFM14A not yet filed |
| **425** | Both | M&A communications (Reg M-A) — press releases, slide decks, employee FAQs filed for disclosure compliance |
| **SC 13D / SC 13D/A** | Acquirer (if pre-deal toehold) | Schedule 13D activist / 5%+ ownership disclosures — useful when the acquirer built a toehold before announcement |
| **10-K Risk Factors update** | Acquirer's next 10-K after announcement | Material acquisition-related risks the acquirer is disclosing to its own shareholders |

For the user's project: helper at `fetch_financial_report.py` (DB `db/financial_reports.db`) covers 10-K/10-Q/8-K. M&A-specific extensions for S-4 / DEFM14A / 425 may need a one-off pull — use the same EDGAR submissions JSON pattern. Save extracted M&A docs under `oneoff/ma_<TARGET>_<ACQUIRER>/`.

### Primary (non-US deals)

- **Chinese A-share / HK targets** → cninfo (巨潮资讯) + HKEX news room. Look for: `要约收购` (tender offer), `资产重组报告书` (M&A restructuring report), `重大资产重组` (material asset reorganization), `股东大会通知` (shareholder meeting notice). Helper: `fetch_cninfo_report.py`.
- **Japanese targets** → EDINET (Yuho updates), TDnet (decision-day press release in 「公開買付届出書」 / tender offer registration statement), MOJ for antitrust filings.
- **Korean targets** → DART (`주요사항보고서` material disclosures, `타법인주식 및 출자증권 양수결정` acquisition decisions).
- **UK targets** → London Stock Exchange RNS + Takeover Panel announcements; UK Code on Takeovers and Mergers governs disclosure cadence.
- **EU cross-border** → European Commission Merger Regulation (M.xxxx case numbers), national antitrust authority filings (Bundeskartellamt for Germany, AGCM for Italy, etc.).

### Antitrust / regulatory tracking

- **U.S. DOJ Antitrust Division** → press releases at `justice.gov/atr` and CMS for case filings.
- **U.S. FTC** → press releases at `ftc.gov/news-events/press-releases` and Hart-Scott-Rodino filings (premerger notification — the company files but the receipt is not public; FTC announces second requests if issued).
- **European Commission DG-COMP** → case search at `ec.europa.eu/competition/elojade/isef/index.cfm` with the M.xxxx case number.
- **UK CMA** → `gov.uk/cma-cases` with case ID.
- **China SAMR** (State Administration for Market Regulation) → press release archive; concentration cases categorized as `经营者集中`.
- **China MOFCOM** → for legacy / foreign-investment-overlap cases.

### Pricing and spread

- Target current price + history — yfinance `auto_adjust=True`.
- Acquirer current price + history — same.
- Deal-implied value per target share — computed from announcement terms (cash + stock ratio × acquirer current price).
- Spread = (deal-implied value − target current price) / target current price.
- Annualized return = spread × (365 / days to expected close).

## Workflow

### Step 0 — Parse inputs

User input forms accepted:

- `track the ANSS-SNPS merger` (target first, then acquirer)
- `M&A status on AVGO-VMW`
- `track <ticker>` (skill identifies the active M&A involving that ticker via recent 8-K Item 1.01 / 2.01)
- `merger arb on Activision-Microsoft` (case-insensitive name matching)

Resolve target + acquirer to:
- Ticker + exchange (or `Private` if unlisted).
- CIK (via EDGAR ticker→CIK map at `https://www.sec.gov/files/company_tickers.json`).
- Domicile (drives which portal to use as primary source).

If the deal hasn't been announced yet ("rumored Microsoft-Sony deal"), explicitly label the report as "**Speculative — no definitive agreement disclosed**" and skip the spread math.

### Step 1 — Pull deal-defining filings

For each side (target + acquirer):
1. Pull recent 8-Ks from EDGAR submissions JSON. Filter for Item 1.01 and Item 2.01 in the last 180 days.
2. Pull the S-4 (acquirer) if any stock consideration.
3. Pull the DEFM14A or PREM14A (target).
4. Pull any 425 communications from the last 60 days.
5. Save under `oneoff/ma_<TARGET>_<ACQUIRER>/`.

Read the DEFM14A (or PREM14A if final not yet filed) for the canonical disclosure of: consideration mix, implied value, exchange ratio (if stock), termination fee, expected close window, board's justification, financial advisors' fairness opinions, target-board projections, target-management projections.

### Step 2 — Compute the deal economics

Build a structured deal-snapshot block:

```yaml
target: <Ticker> (<Name>, <Exchange>)
acquirer: <Ticker> (<Name>, <Exchange>)
announcement_date: YYYY-MM-DD
consideration_mix:
  cash_per_share: $X
  stock_ratio: Y acquirer shares per target share
  cap_collar: <if any>
implied_value_per_share: $Z (= X + Y × acquirer current price)
deal_value_total: $W billion (= implied_value × target shares outstanding)
expected_close: YYYY-MM-DD (range or quarter)
termination_fee: $T million
walk_away_conditions:
  - <bulleted list>
```

Then the spread block:

```yaml
target_current_price: $A (as of YYYY-MM-DD)
deal_implied_value: $Z
spread: B% (= (Z - A) / A)
days_to_expected_close: C
annualized_return: D% (= spread × 365 / C)
```

### Step 3 — Build the milestone tracker

Standard milestone path for a US public-to-public deal:

| Milestone | Expected | Status | Source |
|---|---|---|---|
| Definitive agreement signed | YYYY-MM-DD | ✓ Complete | 8-K Item 1.01 |
| Hart-Scott-Rodino filing | YYYY-MM-DD | ✓ / Pending / Pulled | FTC / DOJ announcement |
| Second Request issued | — | None / Issued (date) | FTC press release |
| EU Commission filing | YYYY-MM-DD | ✓ / Pending | M.xxxx case |
| Phase II decision (EU) | YYYY-MM-DD | — | M.xxxx |
| China SAMR review | YYYY-MM-DD | ✓ / Pending | SAMR concentration filing |
| Other jurisdictions | <list> | <per jurisdiction> | <links> |
| Target preliminary proxy filed | YYYY-MM-DD | ✓ | PREM14A |
| Target definitive proxy filed | YYYY-MM-DD | ✓ | DEFM14A |
| Target shareholder vote | YYYY-MM-DD | ✓ / Pending | Proxy + 8-K Item 5.07 |
| Acquirer shareholder vote (if needed) | YYYY-MM-DD | ✓ / Pending | Acquirer proxy |
| Financing condition met | — | ✓ / Pending | 8-K Item 8.01 |
| Closing | YYYY-MM-DD | Target | 8-K Item 2.01 |

For non-US deals, substitute jurisdiction-specific milestones (UK CMA Phase 1 / 2, UK Takeover Panel Day 60 deadline, etc.).

### Step 4 — Build the break-risk map

Score each of five break-risk categories on a 0–10 scale (0 = no risk visible; 10 = active blocker):

| Risk | Score | Evidence |
|---|---|---|
| Financing | 0–10 | Acquirer's balance sheet capacity, bridge-loan commitment status, debt-market conditions, contingent committed-financing language in agreement |
| Antitrust | 0–10 | Industry concentration, prior similar-deal antitrust outcomes, jurisdictional overlap, second-request status, divestiture commitments offered |
| Shareholder vote | 0–10 | Premium offered (low premium → vote risk), recent activist-investor disclosures, ISS / Glass Lewis recommendations, shareholder-vote-required threshold |
| Litigation | 0–10 | Plaintiff bar's record on similar deals, fiduciary-duty claims, fairness-opinion challenges, dissenters' rights |
| Acquirer-stock / macro | 0–10 | If consideration is stock-heavy, acquirer's own price stability; macro-deal-cycle headwinds |

Total break-risk score (0–50) → narrative paragraph naming the dominant risk and what would change the picture.

### Step 5 — Probability range and triggers

State the probability of close as a **range, not a point estimate**, with explicit triggers for the bear / base / bull paths:

| Scenario | Probability | Triggers |
|---|---|---|
| **Bull (close on or ahead of schedule)** | X% | <list of observable conditions> |
| **Base (close roughly on the stated window)** | Y% | <list of observable conditions> |
| **Bear (delay, restructure, or break)** | Z% | <list of observable conditions> |

The probability range should sum to 100% and have a reasonable spread — single-point "92% likely" is overconfident; "70/20/10" is healthy for a mid-pipeline deal.

### Step 6 — Recent news scan (last 30 days)

Web-search the last 30 days for:
- Antitrust / regulatory news (use `regulator + target + acquirer` query)
- Activist-investor 13D filings (rare but material)
- ISS / Glass Lewis vote recommendations
- Macro headlines that could move the spread (rate moves, credit-market stress, sector regulatory action)

Cite each material news item inline with a date in the link title. Skip items without verifiable URLs.

### Step 7 — Write the report

Save to `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md`. Suggested section structure:

1. **Deal Snapshot** — target / acquirer / consideration / implied value / expected close (the YAML block from Step 2, rendered as a clean table).
2. **Spread & Annualized Return** — current spread math, including the as-of date for the target price.
3. **Milestone Tracker** — table from Step 3.
4. **Break-Risk Map** — five-category score from Step 4 + narrative.
5. **Probability & Triggers** — Step 5's range with named triggers.
6. **Antitrust Detail** — jurisdiction-by-jurisdiction status (US HSR / EU DG-COMP / SAMR / CMA / others).
7. **Background & Strategic Rationale** — 1-2 paragraphs on why the buyer wants the target.
8. **Recent News** — last-30-days items with inline citations.
9. **What to Watch Next** — the next 1–3 dated events that should move the probability range.
10. **Data Used** manifest (mandatory).
11. **References** — every URL cited.

## Output Format (mandatory blocks)

Every report must contain:

1. **Deal Snapshot** at the top — target, acquirer, consideration, implied value, announcement date, expected close.
2. **Spread & Annualized Return** with explicit as-of date.
3. **Milestone Tracker** as a status table.
4. **Break-Risk Map** with five scored dimensions.
5. **Probability range** (not a point estimate) with named triggers.
6. **`## Data Used / 数据来源清单`** manifest.
7. **`## Guardrails for this tracking pass`** block.

### Data Used / 数据来源清单 (mandatory)

```markdown
## Data Used / 数据来源清单

**Deal-defining filings**
- DEFM14A or PREM14A (filed YYYY-MM-DD); S-4 (filed YYYY-MM-DD); 8-K Item 1.01 (target, filed YYYY-MM-DD); 8-K Item 1.01 (acquirer, filed YYYY-MM-DD); 425 communications (last filed YYYY-MM-DD). Source: SEC EDGAR.

**Antitrust / regulatory**
- US HSR (filed YYYY-MM-DD, second-request status: <yes/no>). EU Commission case M.xxxxx (filed YYYY-MM-DD, phase: <I/II>). UK CMA case ID xxxx (status). SAMR concentration filing YYYY-MM-DD (status). Other: <list>. Source: regulator press releases + case dockets.

**Pricing**
- Target price as of YYYY-MM-DD HH:MM (source: yfinance). Acquirer price as of same. Implied deal value computed inline.

**Recent news (last 30 days)**
- <N> news items: Bloomberg / Reuters / FT / WSJ / industry-trade press — each with inline citation + date. Source: WebSearch.

**Stale notices / coverage gaps**
- <bulleted list — financing condition not yet met / disclosed; jurisdiction's regulatory status not yet announced; or "none">.
- E.g.: "China SAMR concentration filing date not publicly disclosed; assumed accepted Q2 2026 based on standard timeline."
```

## Guardrails

- **Do not state a deal closing date the company hasn't stated.** "Expected by end of 2Q26" must trace to a specific filing or press release. Otherwise write "Expected close: per company disclosure, 'sometime in 2026'" and quote the exact language.
- **Do not compute a spread without all three inputs disclosed.** Deal-implied value + target current price (with timestamp) + days to assumed close — show all three.
- **Do not skip a break-risk category just because it's not currently visible.** "Antitrust: clear so far" is a valid score (1–2/10), but "not addressed" is not.
- **Do not source antitrust outcomes to news articles** when the actual regulator decision is public — cite the regulator's docket / press release at a specific URL.
- **Do not promise a deal close.** Probability is a range with named triggers; "this deal will close" is overconfidence regardless of how clean the picture looks.
- **Do not confuse deal consideration with fair value.** Deal consideration is what the buyer is paying; fair value is the target's standalone DCF. They are different.
- **Do not silently drop a pending shareholder vote.** Even on routine deals, the vote is a binary checkpoint — surface it in the milestone tracker.
- **Do not write speculation about acquirer's next move post-close** unless it's in a filing. "We expect SNPS to flip ANSS' physics-simulation IP into its EDA stack" is interpretation, not disclosure — label as `*Analyst view:*`.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Output location

Save to `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md` (and `..._zh.md`) under the project root. Create `reports/ma/` if missing.

Supplementary deliverables:
- M&A filings cache: `oneoff/ma_<TARGET>_<ACQUIRER>/` (S-4, DEFM14A, 425 PDFs/HTML).
- Charts (optional): `reports/charts/ma_<TARGET>_<ACQUIRER>_*.png` (e.g. target-price chart vs deal-implied value; spread over time).

### Update-in-place rule

One English file and one Chinese file per ordered (target, acquirer) tuple. Each tracking pass updates the date suffix in the filename to the new pass date. Older dated copies may exist if this is a multi-month tracking effort; treat them as a snapshot history.

## What this skill does NOT do

- It does not produce a Buy/Sell rating on the target — that's [[trader-plan]] / [[portfolio-decision]]. The skill outputs a deal-close probability range and spread; the trader-plan converts that into a position decision.
- It does not produce a Buy/Sell rating on the acquirer — same answer.
- It does not produce a competing-bid analysis ("is a topping bid likely from a third party?") as a standalone deliverable; the break-risk map's "Other Acquirer Interest" can address it but is not a separate workflow.
- It does not handle private-to-private deals where neither side files publicly — there's nothing to anchor on; decline gracefully.
- It does not predict regulatory outcomes from political preference. Antitrust scoring is anchored to the regulator's track record on analogous deals, not partisan reasoning.
- It does not maintain a deal database — one report per (target, acquirer) tuple lives at the path above; the user can grep across `reports/ma/` to assemble a portfolio view.
