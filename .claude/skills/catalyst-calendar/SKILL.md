---
name: catalyst-calendar
description: One unified catalyst & event lens with three modes. (A) **Day-of brief** — "what's big today/tomorrow" tight 500–1,500 word note covering macro releases (NFP, CPI, PCE, FOMC, ISM, jobless claims, retail sales), earnings (pre/post-market), Fed speakers, M&A milestones (votes, expected closes), index rebalances, options expiry / OPEX, government data releases. Opinionated, actionable, no fluff — written for a 7am desk read. (B) **Week-ahead / horizon calendar** — multi-day catalyst calendar over a coverage universe + weekly preview note (earnings dates, conferences, product launches, regulatory decisions, macro events). (C) **Single-deal M&A monitor** — 3,000–6,000 word English markdown report on one active or proposed M&A transaction (target / acquirer / consideration / spread / milestones / break-risk / probability range), pulling SEC EDGAR (S-4, DEFM14A, 425, 8-K Item 1.01 / 2.01) + jurisdiction antitrust portals; **always confirms target / acquirer direction before writing**. Day-of triggers — "what's big today/tomorrow", "what's hitting the tape", "morning note", "events tomorrow", "macro calendar today", "什么大事今天/明天", "key events today". Week-ahead triggers — "catalyst calendar", "upcoming events", "what's coming this week / next week", "earnings calendar", "event calendar", "catalyst tracker". Single-deal triggers — "track the X-Y merger", "what's the spread on Z deal", "M&A status on <ticker>", "merger arb on Activision-Microsoft", "is the SNPS-ANSS deal closing?".
---

# Catalyst Calendar

A single skill covering three distinct "what's coming up" lenses. Pick the mode from the user's phrasing — the modes share the same data sources but produce very different deliverables.

## Mode dispatch

| User phrasing | Mode | Deliverable | Length |
|---|---|---|---|
| "what's big today / tomorrow", "what's hitting the tape", "morning note", "key events tomorrow", "macro calendar today", "什么大事今天/明天" | **A. Day-of brief** | In-chat brief (saved to `reports/morning/<YYYY-MM-DD>_<topic-slug>.md` only when user says "save it" or "write it up") | 500–1,500 words |
| "catalyst calendar", "upcoming events", "what's coming this week / next week / this month", "earnings calendar", "event calendar", "catalyst tracker" | **B. Week-ahead horizon** | Markdown calendar + weekly preview at `reports/calendar/<week-of-YYYY-MM-DD>.md` (or in chat if 1–2 day horizon) | 1,000–3,000 words |
| "track the X-Y merger", "what's the deal spread on Z", "M&A status on <ticker>", "merger arb on X", "is the X-Y deal closing?", "break risk on the X deal" | **C. Single-deal M&A monitor** | Deep deal report at `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md` | 3,000–6,000 words |

If a request straddles modes (e.g. "what's big this week including any M&A votes?"), default to **B (week-ahead)** and surface the M&A votes inline in the milestone column — do not switch to mode C unless the user specifically asks for the single-deal deep dive.

---

## Mode A — Day-of brief

For "what's big today" / "what's hitting tomorrow" / "morning note" — a tight, opinionated brief readable in 2 minutes.

### What to cover

**Macro / data releases (priority 1 — these move the index)**
- US: NFP / employment situation, CPI, Core PCE, FOMC decision, FOMC minutes, GDP advance/second/third, ISM Manufacturing / Services, Retail Sales, jobless claims (Thursday weekly), Consumer Confidence, U-Mich sentiment, JOLTS, PPI, Housing Starts, Existing/New Home Sales, Durable Goods, Industrial Production.
- China: CPI/PPI, official + Caixin manufacturing/services PMI, trade balance, industrial production, retail sales, fixed-asset investment, GDP, total social financing, M2.
- Eurozone: ECB rate decision, HICP flash, GDP, IFO, ZEW, eurozone PMI.
- Japan: BOJ rate decision, Tankan, CPI, GDP.
- Global: OPEC meetings, IEA monthly oil report, EIA crude/products inventory (Wednesday).

For each release: time (ET), consensus (Bloomberg/Reuters), prior, our view (if held), what would surprise the market.

**Earnings (priority 2 — single-name moves)**
- Pre-market: list ticker + consensus rev/EPS + 1-line "what matters" (key metric or guidance line PMs care about).
- After-close: same.
- For mega-cap reporters (AAPL, MSFT, NVDA, GOOG, META, AMZN, TSLA), give a sentence on read-across to the index / sector.

**Fed / central bank speakers (priority 2)**
- Time, speaker, topic if known, whether voter on current FOMC. Skip non-voting regional Fed presidents giving routine remarks unless they're on a tape that traders watch.

**M&A milestones (priority 3 — situational)**
- Any deal-specific milestone hitting that day: shareholder vote, HSR expiry, EU phase-I deadline, expected close, regulator decision date.
- For each: deal name, milestone, expected market reaction (target spread tightens/widens; arbs unwind).

**Other**
- Index rebalances (S&P, Nasdaq-100, MSCI), options expiry (monthly OPEX = 3rd Friday; quadruple witching), Treasury auctions if mega-size, government shutdown / debt-ceiling deadlines, geopolitical (election results, summits with potential market impact).

**Market-pricing context (lighter than Mode B — pick 1–2 signals)**
- For the day's main event: SPX 1DTE straddle implied move (as-of timestamp) + VIX entering AM + FedWatch probabilities if relevant. One line per signal.
- See the [Event positioning lens](#event-positioning-lens--option--vix--spread-context-modes-a--b) section for the full toolkit. Day-of briefs use a tight subset; the Mode B preview is where the full per-indicator playbook lives.

### Output format

Keep it scannable. A morning desk read is one screen, not three.

```markdown
# Morning brief — <YYYY-MM-DD>

**Top thing:** <one-line headline — what dominates the tape today>

## Macro calendar (ET)
- 08:30 — <release> — consensus X, prior Y. <one-line why-it-matters>
- 10:00 — <release> — same.
- 14:00 — FOMC <minutes/decision> — <what's already priced>.

## Earnings
**Pre-market:** TICKER (cons rev $X / EPS $Y) — <one-line focus>; TICKER2 (...) — <...>.
**After-close:** TICKER3 (...) — <...>.

## Fed / central bank speakers
- 09:30 — Powell, <topic>, <voter status>.
- 13:00 — Lagarde, ECB testimony.

## M&A / deal milestones
- ANSS shareholder vote (re: SNPS deal); current spread <X%>, expected to pass on offered premium.
- HSR expiry on <DEAL> at midnight — no second request expected based on no-issue letter <date>.

## Other
- Monthly OPEX (3rd Friday); $X notional in SPX, gamma <neutral/long/short>.
- Treasury 10Y auction 13:00 — recent auctions have tailed <N>bps.

## Trade angles (optional — skip if nothing actionable)
- Long/short <ticker>: thesis + catalyst + risk.

---
*Time stamp: <local time>. Pre-market may move by open.*
```

### Day-of guardrails

- **Be opinionated** — a morning note that just lists events without a view is useless. Lead with the most important thing.
- **"No news" is a valid brief** — if nothing material is on the calendar, say so ("nothing material on the macro tape; Q3 earnings season effectively wound down; quiet day, expect chop on flows") and stop. Don't pad.
- **Distinguish actionable from noise** — major data release + mega-cap earnings + FOMC decision = actionable. A regional Fed president talking on community banking ≠ actionable for most desks.
- **Time-stamp the take** — if writing at 06:30 ET, note pre-market moves may invalidate it by 09:30.
- **Don't fabricate consensus numbers.** If you can't pull the Bloomberg/Reuters consensus, say "consensus pending" and link the calendar source (e.g. Investing.com economic calendar, BLS release schedule, BEA release schedule). Don't make up a number that sounds plausible.
- **Macro release times in ET** unless the user specifies otherwise. China releases in Beijing time + ET equivalent.

### Day-of output location

Default: **in-chat only**. Save to a file only when the user says "save it" / "write this up" / "add to morning folder" / "保存".

When saving: `reports/morning/<YYYY-MM-DD>_<topic-slug>.md` (matches existing `reports/morning/` directory convention — flat, no per-day sub-folder).

---

## Mode B — Week-ahead horizon calendar

For "what's coming this week" / "catalyst calendar" / "upcoming events" — a multi-day table view over a coverage universe.

### Step 1: Scope

Resolve from the request:
- **Coverage universe** — explicit ticker list, sector (e.g. "semis"), or user's tracked portfolio.
- **Horizon** — next 5 trading days (default), next 2 weeks, this month, this quarter.
- **Include macro?** — default yes; user can scope to ticker-specific events only.

### Step 2: Gather catalysts

For each company / sector / macro lane:

**Earnings & financial events**
- Quarterly earnings date + time (pre / after market); consensus + buyside whisper if known.
- Annual shareholder meeting, investor day, capital markets day.
- Debt maturity / refinancing dates large enough to be a story.

**Corporate events**
- Product launches, FDA AdComm / PDUFA dates, regulatory decisions, contract expirations, lockup expirations, management transitions, dividend ex-dates (for income-portfolio context).

**M&A milestones** (the calendar version of mode C — surface the *date*, not the deep analysis)
- Shareholder votes, HSR expiry, EU phase-I/II deadlines, SAMR review windows, expected close dates.

**Industry events**
- Major conferences with company schedules (CES, JPM Healthcare, Money 20/20, MWC, Computex, GTC, Hot Chips, ISSCC, RSA, Dreamforce, re:Invent, etc.).
- Trade shows, industry data releases (monthly auto sales, weekly box office, etc.).

**Macro events**
- US: FOMC, NFP, CPI, PCE, ISM, retail sales, jobless claims — week-ahead view.
- Non-US: ECB, BOJ, BOE, PBOC, SAMR; CPI, PMI, GDP releases for major economies.
- Geopolitical: G7/G20, elections, summit deadlines.

**Market-pricing context (priority 2 — pair with every H-impact event)**

For each high-impact macro print or earnings name, capture the option / VIX / spread context so the bull/bear thresholds are actionable, not abstract. Use the [Event positioning lens](#event-positioning-lens--option--vix--spread-context-modes-a--b) section below as the toolkit reference. Concretely, per H-impact event:

- **Macro**: SPX 1DTE straddle implied move (as-of), VIX + VIX1D entering the week, FedWatch path probabilities, 2y yield level, MOVE percentile if rates vol is the relevant axis.
- **Earnings**: ATM straddle implied move (Friday-expiry post-print), 3-yr historical-realized vs implied (long-gamma-cheap or rich?), single-name IV vs sector mean.
- **Cross-asset cross-check**: HY OAS + 5y5y breakeven — do credit and inflation expectations agree with the equity-vol read?

If the data is not pullable at write time (e.g. cron run on a closed market), say "implied move pending market open" rather than fabricating.

### Step 3: Calendar view

Render as a sortable table:

```markdown
| Date | Day | Time (ET) | Event | Company/Sector | Type | Impact | Notes |
|------|-----|-----------|-------|----------------|------|--------|-------|
| 2026-06-09 | Mon | 10:00 | ISM Services | Macro | Macro | M | Cons 53.0; below 50 = recession concern flare |
| 2026-06-10 | Tue | AMC | Q2 earnings | ORCL | Earn | H | Cloud / OCI growth print; AI-revenue disclosure pressure |
| 2026-06-11 | Wed | 14:00 | FOMC decision | Macro | Macro | H | Market pricing 25bp cut; dots in focus |
| 2026-06-11 | Wed | 14:30 | Powell presser | Macro | Macro | H | Tone on cut path |
| 2026-06-12 | Thu | 08:30 | CPI | Macro | Macro | H | Cons 0.2% MoM / 3.2% YoY core |
| 2026-06-13 | Fri | — | Triple witching | Index | Other | M | $X notional |
```

Impact column: **H** = market or major sector move likely; **M** = single-name move likely; **L** = routine, useful to know.

### Step 4: Weekly preview note

Markdown narrative companion to the table:

```markdown
# Week of <YYYY-MM-DD>: catalyst preview

**The week in one paragraph.** Headline view of what dominates: rates? earnings? a specific binary event?

## Key events ranked

1. **<Day> — <Event>** — why it matters; what's priced; how the print would surprise.
2. **<Day> — <Event>** — same.
3. ...

## Earnings of note

- **TICKER (Day, time)** — what we're watching: <metric>. Consensus rev/EPS. Recent stock action into print.
- ...

## Macro

- <Release> on <day>: cons X vs prior Y. Why it matters this week.

## Positioning implications

For each H-impact event:
- **What's priced** — FedWatch / 2y yield / consensus path. One line.
- **Implied move** — SPX 1DTE straddle or single-name straddle (with as-of timestamp).
- **Vol-surface tell** — VIX vs historical event-day average; VIX1D backwardation vs contango; SKEW; VVIX. Flag if cheap or rich relative to setup.
- **Cross-asset check** — HY OAS + MOVE + 5y5y breakeven agree or disagree with equity vol?
- **Decision** — long gamma / short gamma / directional / flat. One sentence with the trigger that would flip the call.

Apply the [Event positioning lens](#event-positioning-lens--option--vix--spread-context-modes-a--b) per-indicator playbook table — each indicator type has a different primary tool.

## Next week heads-up

- <One-line> on the biggest event already on the radar for the week after.
```

### Week-ahead output location

`reports/calendar/<week-of-YYYY-MM-DD>.md` — Monday-of-week date. Create the directory if missing. Update in place if a previous pass for the same week exists.

Short horizons (1–2 days) can stay in-chat; only save when the horizon is ≥3 days or the user says "write this up".

---

## Mode C — Single-deal M&A monitor

For "track the X-Y merger" / "what's the spread on Z" / "M&A status on <ticker>" — a deep, single-transaction report.

Deliverable: a 3,000–6,000 word English markdown report on one active or recently-closed M&A transaction. The report answers five specific questions:

1. **What's the deal?** Target, acquirer, consideration, implied value per target share, announcement date, expected close.
2. **What's the spread?** Current target price vs deal value; annualized return assuming the expected close date.
3. **Where are we on the milestone path?** Shareholder vote, antitrust approvals, financing condition, other closing conditions.
4. **What's the break risk?** Financing / antitrust / shareholder / litigation / acquirer-stock / macro.
5. **What's the probability range and what would change it?** Bear / base / bull paths with named triggers.

Adapted from the LLMQuant M&A event tracker (MIT), re-pointed at SEC EDGAR + web search for U.S. deals and cninfo / HKEX / TDnet for cross-border deals.

### When to use mode C

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

### When NOT to use mode C

- Routine quarterly earnings — use [[earnings-analysis]].
- Pure regulatory / antitrust monitoring with no specific deal attached — use [[regulatory-risk-monitor]].
- Private-to-private transactions with no public disclosure — there's nothing to anchor the analysis on; decline.
- Spinoffs / reverse-Morris-trust splits — these are M&A-adjacent but follow a different filing pattern (Form 10, when-issued trading); skill applies imperfectly. Flag the limitation.
- "What deals are happening this week?" — that's mode B (week-ahead), not mode C; the milestone column lists deals by date.

### Core principle: accuracy over completeness — never hallucinate

The accuracy rules from [[company-research]] apply verbatim. M&A-specific failure modes:

- **Never invent a deal term.** Consideration mix (cash %, stock %, ratio), implied price, walk-away conditions, termination fee, expected close date — every one of these must come from a specific SEC filing (S-4, DEFM14A, 8-K Item 1.01, 425) or a verifiable press release URL.
- **Never compute a spread without current target price.** "Spread is 4.5%" requires: deal-implied value per share, current target price (with date), and the assumed days to close. Show all three.
- **Never quote a closing date the company hasn't stated.** "Expected to close in 2Q26" must trace to the deal proxy or a company press release. "Sometime in 2026" is fine if that's what the company said; "by April 2026" is not unless that's literally in a filing.
- **Never call a deal "likely to close" or "unlikely to close" without addressing the four standard break risks** (financing, antitrust, shareholder vote, litigation). A probability statement that ignores even one of these is incomplete.
- **Never source antitrust language to a press release** when the actual filing is public. DOJ / FTC consent decrees, EU Commission decisions, and CMA / SAMR filings all have permanent URLs — cite the docket, not a Bloomberg article.
- **Never confuse "merger consideration" with "fair value."** The deal price is what the buyer is paying; fair value is the target's standalone value. They are different and must not be conflated.

### Report language (mode C)

**Default behavior: English only.** This is a monitoring / tracking skill, not a deep-research deliverable — most users want the English read and don't need the Chinese companion every time. (The substantive research skills `company-research` / `compare-companies` / `earnings-analysis` / `sector-overview` still default bilingual; this mode does not.)

**Chinese opt-in (any of these triggers a Chinese companion file alongside the English):**
- `also in Chinese` / `add Chinese` / `bilingual` / `both languages` / `--bilingual` / `--zh`
- `用中文也输出一份` / `也输出中文版` / `中英双语`

**Chinese-only (skip English):** `用中文即可` / `--zh-only` / `Chinese only`.

When a Chinese companion is produced, use bilingual technical terms: `M&A / 并购`, `target / 标的`, `acquirer / 收购方`, `consideration / 对价`, `implied value / 隐含估值`, `spread / 套利价差`, `expected close / 预计交割`, `termination fee / 终止费`, `antitrust / 反垄断`, `shareholder vote / 股东投票`, `definitive proxy / 最终代理征集书`. Keep ticker codes, regulator names (FTC, DOJ, SAMR, MOFCOM, CMA, EU), and case numbers in original form.

**Filenames (mode C):**
- English: `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md` (e.g. `ANSS_SNPS_2026-05-31.md`)
- Chinese: `reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>_zh.md`
- Use English/pinyin name (per the project filename rule), not Chinese-only. Mixed-domicile deals: `<English-Target>_<English-Acquirer>_<YYYY-MM-DD>.md` (e.g. `Hexagon-DE_Cadence_2026-05-31.md`).

**Update-in-place rule:** one report per ordered (target, acquirer) tuple. If a report from a prior tracking pass exists, update it in place (refresh the date suffix; git history records the trail). Do not pile up dated copies.

### Data sources (mode C)

#### Primary (SEC EDGAR — US deals)

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

#### Primary (non-US deals)

- **Chinese A-share / HK targets** → cninfo (巨潮资讯) + HKEX news room. Look for: `要约收购` (tender offer), `资产重组报告书` (M&A restructuring report), `重大资产重组` (material asset reorganization), `股东大会通知` (shareholder meeting notice). Helper: `fetch_cninfo_report.py`.
- **Japanese targets** → EDINET (Yuho updates), TDnet (decision-day press release in 「公開買付届出書」 / tender offer registration statement), MOJ for antitrust filings.
- **Korean targets** → DART (`주요사항보고서` material disclosures, `타법인주식 및 출자증권 양수결정` acquisition decisions).
- **UK targets** → London Stock Exchange RNS + Takeover Panel announcements; UK Code on Takeovers and Mergers governs disclosure cadence.
- **EU cross-border** → European Commission Merger Regulation (M.xxxx case numbers), national antitrust authority filings (Bundeskartellamt for Germany, AGCM for Italy, etc.).

#### Antitrust / regulatory tracking

- **U.S. DOJ Antitrust Division** → press releases at `justice.gov/atr` and CMS for case filings.
- **U.S. FTC** → press releases at `ftc.gov/news-events/press-releases` and Hart-Scott-Rodino filings (premerger notification — the company files but the receipt is not public; FTC announces second requests if issued).
- **European Commission DG-COMP** → case search at `ec.europa.eu/competition/elojade/isef/index.cfm` with the M.xxxx case number.
- **UK CMA** → `gov.uk/cma-cases` with case ID.
- **China SAMR** (State Administration for Market Regulation) → press release archive; concentration cases categorized as `经营者集中`.
- **China MOFCOM** → for legacy / foreign-investment-overlap cases.

#### Pricing and spread

- Target current price + history — yfinance `auto_adjust=True`.
- Acquirer current price + history — same.
- Deal-implied value per target share — computed from announcement terms (cash + stock ratio × acquirer current price).
- Spread = (deal-implied value − target current price) / target current price.
- Annualized return = spread × (365 / days to expected close).

### Workflow (mode C)

#### Step 0 — Parse inputs and CONFIRM target/acquirer direction

**Critical: never silently assume which company is the target and which is the acquirer.** "SNPS-ANSS" reads either direction; getting it wrong corrupts the entire deal-snapshot block (the spread math swaps, milestones swap, break-risk attribution flips). The skill must resolve direction *explicitly* before writing anything.

**Three acceptable input forms** (in preference order):

| Form | Example | Direction signal |
|---|---|---|
| **Explicit direction (preferred)** | `"Microsoft is acquiring Activision"`, `"SNPS acquired ANSS"`, `"target=ANSS, acquirer=SNPS"`, `"track the merger where SNPS bought ANSS"` | Verb explicitly identifies who acquires whom |
| **Direction known from context** | `"track the ANSS deal"` (single ticker — skill identifies the active M&A involving that ticker via recent 8-K Item 1.01 / 2.01) | EDGAR tells us which side filed which Items |
| **Ambiguous two-ticker phrasing (REQUIRES confirmation)** | `"track the SNPS-ANSS merger"`, `"M&A status on AVGO-VMW"`, `"merger arb on Activision-Microsoft"` | **Ask the user which is target and which is acquirer before proceeding** |

**Direction-resolution workflow:**

1. **If the user's phrasing is explicit** ("X is acquiring Y" / "X acquired Y" / "target=A acquirer=B"), proceed directly.

2. **If only one ticker is given** ("track the ANSS deal", "M&A status on AVGO"), use EDGAR to auto-detect:
   - Pull the named ticker's last 12 months of 8-K Item 1.01 ("Entry into a Material Definitive Agreement") and Item 2.01 ("Completion of Acquisition or Disposition").
   - The 8-K language explicitly states "Agreement and Plan of Merger" with the counterparty named, and identifies which side is being acquired.
   - Resolve the counterparty's ticker via EDGAR's ticker→CIK map.
   - **Surface the detected direction to the user before writing** ("Resolved: ANSS = target, SNPS = acquirer, per ANSS 8-K Item 1.01 filed 2024-01-16. Confirm before I proceed?").

3. **If two tickers are given ambiguously** ("SNPS-ANSS", "AVGO-VMW"), do NOT assume order — **ask the user**:
   - `"Which side is the target (being acquired) and which is the acquirer? E.g. for SNPS-ANSS: did SNPS acquire ANSS, or did ANSS acquire SNPS?"`
   - Once the user confirms, proceed with the verified direction.

4. **Optional safety check** even after explicit confirmation: pull the target's 8-K Item 1.01 and verify the counterparty named in the filing matches the acquirer the user stated. If they disagree, surface the conflict to the user before writing — the filing is authoritative.

Resolve both sides to:
- Ticker + exchange (or `Private` if unlisted).
- CIK (via EDGAR ticker→CIK map at `https://www.sec.gov/files/company_tickers.json`).
- Domicile (drives which portal to use as primary source).

**Filename convention is target-first** (`reports/ma/<Target>_<Acquirer>_<YYYY-MM-DD>.md`) — but this is now a *consequence* of the resolved direction, not a request-format assumption. The user does not need to put target first in the request; the skill does the resolving and writes the filename correctly.

**If the deal hasn't been announced yet** ("rumored Microsoft-Sony deal"), explicitly label the report as "**Speculative — no definitive agreement disclosed**" and skip the spread math. Direction confirmation still applies — even a rumored deal has a presumed acquirer and target.

**Failure modes:**
- Silently assuming "first ticker named = target" → forbidden. Always confirm.
- Picking direction from gut feel ("SNPS is bigger so it must be the acquirer") → forbidden. Use the 8-K filing or ask the user.
- Continuing past Step 0 with the direction still ambiguous → the entire report will be wrong; stop and resolve first.

#### Step 1 — Pull deal-defining filings

For each side (target + acquirer):
1. Pull recent 8-Ks from EDGAR submissions JSON. Filter for Item 1.01 and Item 2.01 in the last 180 days.
2. Pull the S-4 (acquirer) if any stock consideration.
3. Pull the DEFM14A or PREM14A (target).
4. Pull any 425 communications from the last 60 days.
5. Save under `oneoff/ma_<TARGET>_<ACQUIRER>/`.

Read the DEFM14A (or PREM14A if final not yet filed) for the canonical disclosure of: consideration mix, implied value, exchange ratio (if stock), termination fee, expected close window, board's justification, financial advisors' fairness opinions, target-board projections, target-management projections.

#### Step 2 — Compute the deal economics

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

#### Step 3 — Build the milestone tracker

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

#### Step 4 — Build the break-risk map

Score each of five break-risk categories on a 0–10 scale (0 = no risk visible; 10 = active blocker):

| Risk | Score | Evidence |
|---|---|---|
| Financing | 0–10 | Acquirer's balance sheet capacity, bridge-loan commitment status, debt-market conditions, contingent committed-financing language in agreement |
| Antitrust | 0–10 | Industry concentration, prior similar-deal antitrust outcomes, jurisdictional overlap, second-request status, divestiture commitments offered |
| Shareholder vote | 0–10 | Premium offered (low premium → vote risk), recent activist-investor disclosures, ISS / Glass Lewis recommendations, shareholder-vote-required threshold |
| Litigation | 0–10 | Plaintiff bar's record on similar deals, fiduciary-duty claims, fairness-opinion challenges, dissenters' rights |
| Acquirer-stock / macro | 0–10 | If consideration is stock-heavy, acquirer's own price stability; macro-deal-cycle headwinds |

Total break-risk score (0–50) → narrative paragraph naming the dominant risk and what would change the picture.

#### Step 5 — Probability range and triggers

State the probability of close as a **range, not a point estimate**, with explicit triggers for the bear / base / bull paths:

| Scenario | Probability | Triggers |
|---|---|---|
| **Bull (close on or ahead of schedule)** | X% | <list of observable conditions> |
| **Base (close roughly on the stated window)** | Y% | <list of observable conditions> |
| **Bear (delay, restructure, or break)** | Z% | <list of observable conditions> |

The probability range should sum to 100% and have a reasonable spread — single-point "92% likely" is overconfident; "70/20/10" is healthy for a mid-pipeline deal.

#### Step 6 — Recent news scan (last 30 days)

Web-search the last 30 days for:
- Antitrust / regulatory news (use `regulator + target + acquirer` query)
- Activist-investor 13D filings (rare but material)
- ISS / Glass Lewis vote recommendations
- Macro headlines that could move the spread (rate moves, credit-market stress, sector regulatory action)

Cite each material news item inline with a date in the link title. Skip items without verifiable URLs.

#### Step 7 — Write the report

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

### Output format (mode C — mandatory blocks)

Every mode-C report must contain:

1. **Deal Snapshot** at the top — target, acquirer, consideration, implied value, announcement date, expected close.
2. **Spread & Annualized Return** with explicit as-of date.
3. **Milestone Tracker** as a status table.
4. **Break-Risk Map** with five scored dimensions.
5. **Probability range** (not a point estimate) with named triggers.
6. **`## Data Used / 数据来源清单`** manifest.
7. **`## Guardrails for this tracking pass`** block.

#### Data Used / 数据来源清单 (mandatory)

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

### Guardrails (mode C)

- **Never silently assume which side is target and which is acquirer.** "SNPS-ANSS" reads either direction; getting it wrong corrupts the entire deal-snapshot block. Use explicit user phrasing ("X is acquiring Y"), or EDGAR 8-K Item 1.01 auto-detection when only one ticker is given, or **ask the user** before proceeding when two tickers are given ambiguously. The filename convention `<Target>_<Acquirer>` is a *consequence* of the resolved direction, not an input-format assumption. See Step 0.
- **Do not state a deal closing date the company hasn't stated.** "Expected by end of 2Q26" must trace to a specific filing or press release. Otherwise write "Expected close: per company disclosure, 'sometime in 2026'" and quote the exact language.
- **Do not compute a spread without all three inputs disclosed.** Deal-implied value + target current price (with timestamp) + days to assumed close — show all three.
- **Do not skip a break-risk category just because it's not currently visible.** "Antitrust: clear so far" is a valid score (1–2/10), but "not addressed" is not.
- **Do not source antitrust outcomes to news articles** when the actual regulator decision is public — cite the regulator's docket / press release at a specific URL.
- **Do not promise a deal close.** Probability is a range with named triggers; "this deal will close" is overconfidence regardless of how clean the picture looks.
- **Do not confuse deal consideration with fair value.** Deal consideration is what the buyer is paying; fair value is the target's standalone DCF. They are different.
- **Do not silently drop a pending shareholder vote.** Even on routine deals, the vote is a binary checkpoint — surface it in the milestone tracker.
- **Do not write speculation about acquirer's next move post-close** unless it's in a filing. "We expect SNPS to flip ANSS' physics-simulation IP into its EDA stack" is interpretation, not disclosure — label as `*Analyst view:*`.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

### Supplementary deliverables (mode C)

- M&A filings cache: `oneoff/ma_<TARGET>_<ACQUIRER>/` (S-4, DEFM14A, 425 PDFs/HTML).
- Charts (optional): `reports/charts/ma_<TARGET>_<ACQUIRER>_*.png` (e.g. target-price chart vs deal-implied value; spread over time).

### Update-in-place rule (mode C)

One English file and one Chinese file per ordered (target, acquirer) tuple. Each tracking pass updates the date suffix in the filename to the new pass date. Older dated copies may exist if this is a multi-month tracking effort; treat them as a snapshot history.

---

## Event positioning lens — option / VIX / spread context (Modes A & B)

Bull/bear thresholds on a macro print or earnings release are only half the picture. The other half is **what's already priced** — if the market enters the print already short, a hot CPI delivers a smaller move than the same print into a long-positioned tape. This section codifies how to use option pricing, vol-surface signals, and credit spreads to translate the indicator-level bull/bear thresholds into actionable trade context.

Apply this lens to Mode A briefs (day-of) and Mode B previews (week-ahead). Skip it for Mode C (single-deal M&A) — the spread math there is direct, not vol-based.

### The 4-layer framework

For every binary event (macro print, earnings, FOMC, vote outcome), ask in order:

1. **What's priced?** — what does the consensus position imply? Tells you the size of the surprise needed to move the tape.
2. **What's the implied move?** — what does the option market literally pay for movement on the print day?
3. **What's the directional bias?** — skew + put-call ratio + 25-delta-put-vs-call IV; is downside already paid for, or is it fresh?
4. **Cross-check** — do credit spreads, MOVE, and equity vol agree on the risk premium? If one disagrees, the dissenter is usually wrong by 1–2 standard deviations.

### Toolkit

| Tool | Measures | Where to find | What it tells you |
|---|---|---|---|
| **CMEGroup FedWatch** | Implied probability of each FOMC outcome at each meeting through year-end | [cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html) | What's already priced into the rate path. If hike-odds-by-year-end are already 40%, a hot CPI only adds 5–10pp. |
| **2y Treasury yield** | The cleanest mirror of FedWatch (front-end is fully Fed-driven) | [FRED — DGS2](https://fred.stlouisfed.org/series/DGS2) | If 2y is at 4.05% before CPI, hawkish positioning is in; bearish surprise gets a small move. If 2y is at 3.85%, dovish positioning is in; hot CPI gets a 10–15bp jump. |
| **SPX 1DTE / 0DTE straddle** | The option market's literal $-value bet on the move in the next 24 hours | Bloomberg OMON, optionsalpha, spotgamma. Or compute: ATM call + ATM put expiring next session. | If SPX 5800 and the 5800 straddle expiring tomorrow is $50, implied move is ±0.86%. Compare to historical reactions at the indicator's bull/bear levels. |
| **VIX (1-mo)** | 30-day implied SPX vol — the overall risk premium | `db/indicators.db` symbol `vix` (Tier-2 helper-ingested; backup [^VIX](https://www.cboe.com/tradable_products/vix/)) | Cheap vol entering CPI (VIX <14 when 3-yr CPI-day average is ~16) = lean long gamma. Rich vol (>20) = lean short gamma. |
| **VIX1D** (true event-day vol) | 1-day SPX implied vol — spikes on CPI / NFP / FOMC days, crushes intraday post-event | `db/indicators.db` symbol `vix1d` (backup [CBOE VIX1D](https://www.cboe.com/us/indices/dashboard/VIX1D/)) | VIX1D > VIX = event fear priced today; if also VIX1D ≥ 25, downside tail is fat — sell premium with a tail hedge. |
| **VIX term structure** | VIX9D ÷ VIX3M — is risk event-driven or regime change? | `db/indicators.db` symbol `vix_slope` | <1 = contango (calm); >1 = backwardation (event-driven fear). On CPI weeks typical pre-print is ~0.85; backwardation entering means the move is already priced. |
| **VVIX** | Vol-of-vol — how much VIX itself could move | `db/indicators.db` symbol `vvix` | VVIX >100 = VIX could spike hard on surprise. VVIX <85 = vol itself is well-anchored; second-order reaction limited. |
| **SKEW (CBOE)** | Tail-risk premium — 25-delta-put IV vs 25-delta-call IV | `db/indicators.db` symbol `skew` | Steep skew (>140) = downside is priced fat, asymmetric upside on a bull print. Flat skew (<120) = balanced bets. SKEW >145 + VIX <14 = "calm with a fat tail" — buy puts cheaply. |
| **MOVE index** | Treasury vol — rates-vol equivalent of VIX | `db/indicators.db` symbol `move` | CPI weeks usually run 10–20% above 3-mo average. >120 = rates vol elevated; <80 = rates vol cheap. **Cross-check vs equity vol** — if VIX spikes but MOVE doesn't, the rates market hasn't confirmed the move (equity vol may mean-revert). |
| **HY OAS / IG OAS** | Credit risk premium — cross-asset complacency check | `db/indicators.db` symbols `hy_oas` / `ig_oas` | If HY <300bp entering a hot CPI, the credit market is under-pricing recession risk and equity vol is the cleaner expression. If HY >400bp, credit already has growth fear in. |
| **2y Treasury yield** | Front-end rates — cleanest mirror of FedWatch positioning | `db/indicators.db` symbol `dgs2` | If 2y at 4.05% before CPI, hawkish positioning is in; bearish surprise gets a small move. If 2y at 3.85%, dovish positioning in; hot CPI gets a 10–15bp jump. |
| **5y5y forward inflation breakeven** | Forward inflation expectations from TIPS | `db/indicators.db` symbol `t5yifr` | If 5y5y >2.55% entering CPI, "expectations un-anchoring" is already priced — relief print delivers outsized rally. <2.30% = expectations well-anchored (the Fed's preferred read), hot print delivers larger shock. |
| **Single-name ATM straddle** | Implied move on earnings | Bloomberg OMON; [marketchameleon.com](https://marketchameleon.com/Overview/<TICKER>/Earnings/Earnings-Dates/) — quotes consensus implied move | The ATM straddle expiring the Friday after earnings = expected gap magnitude. ORCL typical 5–7%; ADBE 6–9%; mega-cap (NVDA / META / AMZN) 6–10%. |

### Per-indicator playbook

Each macro indicator has a *primary* pricing signal and a *"too high" tell*. Use the primary tool to gauge the size of the surprise needed; the "too high" tell flags when the market has over-positioned for one outcome.

| Indicator | Primary tool | "Too high" tell (one side priced) | Decision rule |
|---|---|---|---|
| **CPI** | SPX 1DTE straddle + 2y yield + FedWatch | 1DTE straddle prices ±0.7%+ AND 2y at 4.05%+ AND hike-odds-by-year-end >35% → bear partially priced; upside outsized on a soft print | Bull print → upside ~150% of implied; bear print → downside ~110% of implied. **Buy 1DTE straddles if VIX <14 entering print AM**; sell if VIX >18. |
| **PPI** | MOVE + 5y5y breakeven | 5y5y >2.55% = inflation expectations un-anchor priced; hot PPI delivers smaller move | Lower-impact than CPI; vol crush is the main trade. Sell-the-straddle the morning before (~75% win rate when MOVE >decile-7). |
| **Jobless claims** | VIX + 2y yield | Pre-print VIX >16 AND 2y <3.85% → recession-bear partially priced | Single print rarely moves SPX >30bp unless >250k. Stay flat unless 4-week MA breaking 230k is plausible from a single print. |
| **U-Mich sentiment** | 5y5y breakeven + DXY | 5y5y >2.55% AND DXY >107 = expectations un-anchoring priced | Trade rates vol (MOVE puts) not equity vol — U-Mich moves the curve more than SPX. |
| **FOMC decision** | FedWatch + SOFR options + SPX 0DTE straddle | If FedWatch shows >85% probability for one outcome, the binary is collapsed and only the dots / Powell tone trades | Buy 0DTE straddles only when FedWatch is split 50–80% — the most asymmetric setup. SEP day amplifies move by 1.5–2x vs no-SEP meetings. |
| **NFP** | VIX1D + 2y yield + SPX gamma | Pre-print VIX1D >5 above VIX = event priced; <2 above = complacent | Asymmetric to the **upside**-on-payrolls (huge beat) and **downside**-on-claims-driven (huge miss). Sub-component beats (wage growth, U6) often dominate the headline. |
| **PCE (core)** | Already-released CPI + PPI services-ex-trade | Markets have ~70% of the PCE print priced after CPI / PPI; PCE-specific surprise is smaller | Trade PCE only on the residual surprise vs CPI/PPI predicted; standalone PCE move is rarely large. |
| **ISM Manuf / Services** | VIX1D + HY OAS | If HY tight + VIX low, recession-bear is not priced; sub-48 ISM delivers outsized risk-off | Sub-50 ISM Services is the recession trigger most-watched in 2024–26. |

### Earnings: implied-move framework

For each single-name earnings print, the deliverable should include:

1. **Implied move** (ATM straddle expiring the Friday after print) — quote from marketchameleon or Bloomberg.
2. **3-year historical-realized move on earnings** — compare to implied. If realized > implied historically by >20%, the straddle is structurally cheap; long gamma into the print wins on average.
3. **Bull / Bear gap estimate** under the bull/bear scenarios from the calendar — i.e. "If guide ≥ X, expect +8% gap; if guide ≤ Y, expect −10% gap."
4. **IV crush expectation** — single-name IV always collapses 30–40% post-print regardless of direction. Selling premium into earnings *and* holding through the print wins ~60% of the time on names without binary catalysts; loses on names with binary catalysts (ADBE-style GenAI-disruption print, NVDA-style AI-spend referendum).

### "Is the price too high?" decision rule

The synthesis: compare what the option market is paying for movement to the gap-magnitude implied by the bull/bear thresholds.

```
implied_move = ATM straddle price / spot price
expected_move_on_bull = avg(historical realized moves on similar-quality bull surprises)
expected_move_on_bear = avg(historical realized moves on similar-quality bear surprises)

if implied_move < min(|expected_move_on_bull|, |expected_move_on_bear|):
    vol is cheap → BUY gamma (long straddle)
elif implied_move > max(|expected_move_on_bull|, |expected_move_on_bear|) × 1.2:
    vol is rich → SELL gamma (short straddle / iron condor)
else:
    fairly priced → directional bet if you have a view; flat if you don't
```

Concrete example for the Wed CPI:
- If SPX 1DTE straddle is pricing ±0.85% and the bull print historically delivers +1.2%, +1.4%, +1.0% (avg 1.2%) and bear delivers −1.5%, −1.1%, −1.3% (avg −1.3%) — then implied (0.85%) < both expected moves. **Long gamma is cheap; buy the straddle.**
- If implied is ±1.4% but the bull/bear distribution is ±1.0% — implied is rich. **Sell the straddle; expected IV crush + small realized move beats the gamma.**

### Data sources in this project

The `db/indicators.db` table holds the **entire positioning toolkit** locally (Tier-2 helper-ingested per CLAUDE.md § "Database Safety"):

| Symbol | What it is | When to use |
|---|---|---|
| `vix` | 30-day SPX implied vol | Overall risk premium; "is vol cheap or rich entering the print?" |
| `vix1d` | 1-day SPX implied vol | True event-day vol — spikes above VIX on CPI/NFP/FOMC days |
| `vvix` | Vol-of-vol | >100 = VIX itself could spike further on surprise; <85 = vol anchored |
| `vix_slope` | VIX9D ÷ VIX3M | <1 = contango (calm); >1 = backwardation (event-driven fear) |
| `skew` | CBOE SKEW — 25Δ put vs call IV proxy | >145 = downside paid fat (asymmetric upside on bull); <120 = balanced |
| `move` | ICE BofA MOVE (Treasury vol) | Rates-vol cross-check; "VIX of bonds" |
| `hy_oas` / `ig_oas` | Credit spreads | Cross-asset disagreement signal — if equity vol freaks out but credit stays tight, equity vol is the dissenter |
| `hyg` / `lqd` | HY / IG ETF prices | Spread proxies (intraday-faster than OAS series) |
| `tnx` / `dgs2` | 10y / 2y Treasury yields | 2y mirrors FedWatch positioning; 10y carries growth + term premium |
| `yield_spread` | 10y − 3m spread | Curve regime (recession warning if inverted) |
| `tbill_3m` | 3-month T-bill yield | Front-end funding cost |
| `t5yifr` | 5y5y forward inflation breakeven (TIPS) | Inflation expectations anchor; >2.5% = un-anchoring; the Fed-watched signal |
| `dxy` | USD index | Risk-on/off tell; rising = dollar funding stress |
| `spy` | S&P 500 ETF | Spot reference |
| `gold` / `oil` | Safe-haven / growth proxies | Cross-asset risk-on/off |

**Query pattern (read-only):**

```bash
# Latest values for the positioning toolkit
sqlite3 db/indicators.db "SELECT symbol, date, value FROM history WHERE date = (SELECT MAX(date) FROM history) AND symbol IN ('vix','vix1d','vvix','vix_slope','skew','move','hy_oas','dgs2','tnx','t5yifr','dxy') ORDER BY symbol;"

# 4-week trend for a single indicator
sqlite3 db/indicators.db "SELECT date, value FROM history WHERE symbol = 'skew' AND date >= date('now', '-28 days') ORDER BY date;"
```

**Refreshing the data** (Tier-2 helper invocation — sanctioned write path):

```bash
python -c "from indicators import db as idb; from indicators.data_fetcher import fetch_all; idb.init_db(); idb.save_snapshot(fetch_all())"
```

The `save_snapshot()` helper uses `INSERT OR REPLACE` on `(symbol, date)` — re-running is idempotent.

**What still requires web-search at brief-write time:**
- **FedWatch probabilities** ([CMEGroup FedWatch](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html)) — implied probability of each FOMC outcome; updates intraday.
- **SPX 1DTE straddle pricing** — Bloomberg OMON, spotgamma, optionsalpha. Updates every minute.
- **Single-name ATM straddle pricing** — [marketchameleon](https://marketchameleon.com/) per ticker; same.
- **Sub-component splits** (core CPI vs headline, services-PPI-ex-trade, specific U-Mich inflation-expectation sub-readings) — fetched from BLS / U-Mich at release.

These four are not worth caching because they update faster than a daily snapshot.

### Guardrails — positioning lens

- **Never quote an implied move without an as-of timestamp.** "Implied move is ±2.1%" requires "as of Tue 15:30 ET, straddle expiring Friday." Straddles re-price every minute.
- **Never fabricate FedWatch probabilities.** Pull from CMEGroup live; if you can't, say "FedWatch pending" and don't make up a number.
- **Never treat one tool's signal as the whole picture.** VIX cheap + HY tight + MOVE rich is a *split signal* — flag it as such; don't average across them.
- **Never claim the option market is "wrong."** It's a price; it's right by definition. The trade is "is it too cheap or too rich for *my* expected move distribution?" That's a judgment call, not a fact statement.
- **Never recommend selling vol into a binary event without flagging the tail risk.** Short-straddle / iron-condor positioning into FOMC / NFP / CPI loses 5–10× the typical winner when it loses. Make the tail explicit.
- **Cross-asset disagreement is information, not a bug.** If credit is sanguine and equity vol is elevated, write that as a *finding* in the brief — don't smooth it into a single number.
- **For new indicators, calibrate from historical-realized moves before committing to a bull/bear gap estimate.** "CPI bull = +1.2% SPX move" should be backed by a sample of comparable prior bull-surprise CPI days.

## Cross-cutting guardrails (all modes)

- **Citation standard** — every substantive paragraph carries ≥1 inline markdown-link citation per the project's `.claude/skills/company-research/references/citations.md` spec. Day-of briefs are exempt from this for ephemeral macro-print numbers (consensus pulled from Bloomberg/Reuters terminals), but file-saved versions get inline links to the original release schedule (BLS, BEA, FRB, EIA, etc.).
- **Numerical accuracy** — every number traces to a URL that literally contains it. Don't quote a "+185% QoQ" without sourcing it inline. See CLAUDE.md § "Numerical Accuracy".
- **No destructive SQL against `db/*.db`** — read-only. See CLAUDE.md § "Database Safety".
- **Filenames must start with English / pinyin** — even Chinese reports. `Anpeilong_安培龙_SZSE002050_*.md` good; `安培龙_SZSE002050_*.md` bad. See CLAUDE.md § "Research Report Filenames".
- **Earnings dates shift** — verify against company IR pages and Bloomberg/FactSet closer to the date, especially when answering "what's next week?" more than 3 days out.
- **Pre-announce risk** — flag companies with a history of pre-announcing (positive or negative) when they're in the calendar week.

## What this skill does NOT do

- It does not produce a Buy/Sell rating on the target — that's [[trader-plan]] / [[portfolio-decision]]. The skill outputs a deal-close probability range and spread; the trader-plan converts that into a position decision.
- It does not produce a Buy/Sell rating on the acquirer — same answer.
- It does not produce a competing-bid analysis as a standalone deliverable; the break-risk map's "Other Acquirer Interest" can address it but is not a separate workflow.
- It does not handle private-to-private deals where neither side files publicly — there's nothing to anchor on; decline gracefully.
- It does not predict regulatory outcomes from political preference. Antitrust scoring is anchored to the regulator's track record on analogous deals.
- It does not deep-dive on regulatory cases not attached to a specific deal — use [[regulatory-risk-monitor]] for that.
- It does not produce earnings deep-dives — the calendar surfaces the date; use [[earnings-analysis]] or [[earnings-preview]] for the deep read.
- It does not maintain a deal database — one report per (target, acquirer) tuple lives at `reports/ma/`; the user can grep across to assemble a portfolio view.
