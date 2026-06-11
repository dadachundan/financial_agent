---
name: bull-bear-debate
description: Run a multi-round bull-vs-bear debate over a ticker using the three analyst reports (sentiment, news, company-research) as evidence. Use when the user wants "the bull case vs bear case", "debate this trade", or as part of a full trading workflow after analyst reports are ready.
argument-hint: <ticker> [--rounds N] [--asset-type stock|crypto]
allowed-tools: [Read, Write]
---

# Bull / Bear Researcher Debate

Stage a conversational debate between a **Bull Analyst** and a **Bear Analyst** over `<ticker>`. The debate proceeds for `--rounds N` rounds (default 2 if the orchestrator does not specify). Each round = one Bull turn then one Bear turn.

For `--asset-type stock` use "stock" as the target label; for `--asset-type crypto` use "asset" (and note that the company-research report may be abbreviated since the deep-dive structure assumes a corporate issuer).

## Prerequisites

This skill needs three analyst reports in the conversation context as markdown blobs:

- `sentiment_report` — from [[sentiment-analyst]]
- `news_report` — from [[news-analyst]]
- `company_research_report` — from [[company-research]] (deep institutional-grade coverage of business, management, products, customers, competition, TAM, risks)

**If any report is missing**, run the corresponding analyst skill(s) first — invoke the missing ones sequentially, per the CLAUDE.md 16 GB memory-watch rules: [[company-research]] ALONE first if needed (it is the heavy 6–10k-word agent); [[sentiment-analyst]] + [[news-analyst]] may pair 2-wide only with `/tmp/mem-watch-16gb.sh` running and free RAM >60%. The analyst skills have no further prerequisites.

**Before re-running [[company-research]]** (a 10–30 min, 6,000–10,000-word deep dive), check for a cached report first:

Glob `reports/company/*_<TICKER>/` and pick the most-recently-modified match (see [`output_path.md`](../../../references/output_path.md)). Folders follow `<Company>_<EXCHANGE><TICKER>` (e.g. `AMD_NASDAQ_AMD`, `Tesla_NASDAQ_TSLA`, `安培龙_SZSE002050`). Read the `*_Research_Document.md` / `*_公司研究.md` / `*_研究报告.md` file at the folder root. If its mtime is < 30 days old, use it as `company_research_report`.

Only invoke [[company-research]] fresh if no cache hits. `sentiment_report` and `news_report` are short-lived by design — always run those analyst skills fresh.

For a clean full-pipeline run from scratch, prefer [[trading-analysis]] over invoking this skill standalone.

## Inputs

- The three analyst reports listed above.
- `debate_history` — running transcript, empty on round 1.
- `--rounds N` — debate length (default 2).
- `--asset-type` — `stock` or `crypto`.

The company-research report searches `db/zsxq.db` for the sell-side view (price targets, FY+1/+2/+3 estimates, valuation multiples, bear case) and labels it `*Analyst view:*`. **This block is the primary source for the scenario forward estimates and multiples both sides will use below** — pull bull/base/bear EPS and the per-case multiple from it, and keep any company-guided or consensus number visually distinct from the analyst's own estimate (never blend them into one figure).

**Fresh sell-side check (run before round 1):** the cached company-research `*Analyst view:*` block can be up to 30 days stale, and the local broker library often holds a fresher, richer primary note (PT derivation, segment estimates vs consensus, bear case). Search it read-only:

```bash
/opt/anaconda3/bin/python3 zsxq_fts.py --query "<ticker / company name>" --limit 10
```

Pull the 1–2 freshest notes' PT, multiple, forward EPS, and bear case into the swing-variable values and Scenario scorecard — labeled `*Analyst view:*` and cited with the direct-download URL the script prints (`http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<urlencoded-name>`; never the `/zsxq/pdf-viewer/` route). Fall back to the cached company-research block only when the library has nothing fresher than it.

**Sell-side view evolution (卖方观点演变) — mandatory whenever ≥2 zsxq notes cover the ticker.** Extend the fresh sell-side check with a mechanical pre-pass BEFORE re-reading any PDF — STRICTLY read-only (`/opt/anaconda3/bin/python3`, `sqlite3.connect('file:db/stock_price_target.db?mode=ro', uri=True)`; writes stay exclusively with `scripts/persist_pts.py`): `SELECT research_institute, rating, price_target, target_currency, report_date, report_file_id, upside_pct FROM price_targets WHERE company_ticker=? ORDER BY research_institute, report_date`. It surfaces same-institute revisions and PT dispersion (min/median/max, spread %) cheaply. The disagreement is debate fuel, not garnish:

- **Each side names WHICH institutes back its stance, dated** — and flags recent revisions toward or away from its case (a broker that just cut its own PT is bear ammunition even if the rating stayed Buy; state the note's trigger — earnings print, policy change, channel checks, order data). Order each institute's views by report date (the filename's `-YYMMDD` suffix is the authoritative pub date; sanity-check against `create_time`); a 2026-03 PT and a 2026-06 PT from the same institute are two different views, not duplicates.
- **Contradictory institutes get named, never averaged into a fake consensus.** When they disagree (opposite ratings, PTs >20% apart, conflicting reads of the same datapoint), render the disagreement table — `| Institute | Date | Rating / PT | Core argument | What evidence would prove them right |` — the last column hands each debater its falsification test.
- **Every cited view carries (institute, report date, `/zsxq/pdf/<file_id>/<urlencoded-name>` direct-download link)** — same citation route as above.
- **Artifact:** a 6–12-line **Sell-side view evolution (卖方观点演变)** block (per-institute dated timeline + disagreement table where views conflict) placed directly after the Scenario scorecard, so [[research-manager]] sees where the street actually splits.

## Swing variables (set before round 1)

Before round 1, name the **2–4 variables that actually move the stock** — the shared levers both sides will argue at high vs low values, instead of raising disjoint topics. Borrow the GS commodity-relativity discipline (run the *same* swing variable — gold $3,500 vs $5,500 — across the case set) and the UBS Futu scenario block (paying-client CAGR 17.2% vs 15.2% vs MCC-exit per case). Typical levers: the key product/market share, an AI-capex or end-demand trajectory, a commodity/price input, and the valuation multiple itself.

- Pick levers whose value the bull and bear genuinely disagree on, and that map cleanly onto the forward-year EPS used in the scorecard.
- Cite each swing-variable value to a source that literally contains it (consensus, a third-party forecaster — CRU / Riglogix / Yole-style — or the `*Analyst view:*` block), per the project numerical-accuracy rule.
- The bull case sets these high, the bear sets them low; the base case is the middle. Both sides must use the **same** lever set so the debate converges, not diverges.

## Per-turn instructions

### Bull turn

You are a Bull Analyst advocating for investing in the {stock|asset}. Build a strong, evidence-based case emphasizing growth potential, competitive advantages, and positive market indicators. Address concerns and counter bearish arguments effectively.

Focus on:
- **Growth potential** — market opportunities, revenue projections, scalability.
- **Competitive advantages** — unique products, branding, dominant positioning.
- **Positive indicators** — financial health, industry trends, recent positive news.
- **Scenario PT** — defend a **bull-case price target shown as (valuation multiple) × (forward-year EPS/metric)**, mirroring the MS "Risk Reward Update" bull line (e.g. AVGO bull 30× = $619) and the UBS scenario block. Pull the multiple and the FY+1/+2/+3 EPS from the company-research `*Analyst view:*` block; don't assert a round number with no math behind it. State the **2–3 falsifiable conditions that must ALL hold** for the bull case (the JPM Insta360 frame: DJI coexistence AND category break-out AND GPM recovery), not a generic "growth potential" bullet.
- **Probability, priced-in & sensitivity** — assign and defend a rough probability to the bull case; run a **priced-in test** showing how much of the *bear* case is already embedded in the price (implied-growth / positioning evidence from the analyst reports); and stress **one swing variable at a time** with reported sensitivity (the JPM "+$20/bbl per month of Hormuz delay" form).
- **Bear counterpoints** — critically analyze the most recent bear argument with specific data and sound reasoning; address concerns thoroughly and show why the bull perspective holds stronger merit.
- **Engagement** — conversational style. Engage directly with the bear's points; debate rather than just list data.

Resources to leverage explicitly: sentiment report, news report, company-research report, the prior debate history, and the most recent bear argument.

**Citations:** when you cite a specific data point, headline, post, or filing passage, reproduce the underlying URL from the analyst report's References section as a clickable markdown link inline — e.g. "the [Q1 results press release](https://...) confirms 85% YoY revenue growth" or "as one user put it on [StockTwits](https://stocktwits.com/...) — 'easy $260 from here'". Never invent URLs; if the underlying analyst report has no link for a claim, paraphrase generally instead of citing a specific source. **This extends to every number in the scenario scorecard** — each PT, multiple, forward-EPS, and swing-variable value must trace to a URL cited in the same paragraph/table cell where it appears, and derived numbers (EV-PT, upside %) must show their inputs.

**A sec.gov (or any primary-filing) URL may only carry text/numbers that literally appear in that filing.** When the claim is the company-research document's own analysis or paraphrase, cite the document itself — a repo-root-relative link labeled `*Internal research:* [<Company> deep dive §N](reports/company/<folder>/<…>_Research_Document.md)` — never decorate it with a filing URL borrowed from the same paragraph (a past run quoted the deep-dive's own "20–30% multiple-compression event" sentence and cited it to the 10-K, which contains no such words). Before finishing, re-check every quoted sentence attributed to a filing for literal presence in that filing.

**Unsourced quantitative assumptions must be tagged.** Any quantitative assumption a debater introduces (per-GW dollars, attach rates, share splits, conversion ratios, rules of thumb) must either string-match a cited source or be explicitly tagged `*unsourced debate assumption*` in-line — and tagged assumptions may NOT feed the Scenario scorecard or the probability-weighted PT.

Prefix the turn with `Bull Analyst:` and append it to `debate_history`.

### Bear turn

You are a Bear Analyst making the case against investing in the {stock|asset}. Present a well-reasoned argument emphasizing risks, challenges, and negative indicators.

Focus on:
- **Risks and challenges** — market saturation, financial instability, macro threats.
- **Competitive weaknesses** — weaker positioning, declining innovation, competitor threats.
- **Negative indicators** — adverse financial data, market trends, recent negative news.
- **Scenario PT** — defend a **bear-case price target as (lower multiple) × (lower forward-year EPS)**, a real valuation — not a worry list (SanDisk bear 25× × $44; ASML bear ~20× × ~€20). Pull both inputs from the company-research `*Analyst view:*` block and set the shared swing variables to their low values.
- **Probability, priced-in & sensitivity** — assign and defend a rough probability to the bear case; run the **priced-in test** — the strongest bear case shows the *bull* case is already the price (the YOFC "current price implies a 4–5× jump in quarterly profit — too hard" form); and stress one swing variable at a time with reported sensitivity.
- **Bull counterpoints** — critically analyze the most recent bull argument; expose weaknesses or over-optimistic assumptions.
- **Engagement** — conversational style. Engage with the bull's points directly.

**Citations:** same rule as the Bull turn — reproduce URLs from the analyst reports as inline markdown links whenever you cite specific evidence; never invent URLs. Every scorecard number (bear PT, multiple, forward-EPS, swing-variable value) must string-match a cited source.

Prefix the turn with `Bear Analyst:` and append it to `debate_history`.

## Scenario scorecard (required)

After the debate rounds, both sides converge to a single **Risk-Reward-style scorecard** — the deliverable institutional desks lead with (MS "Risk Reward Update", UBS scenario-analysis block, Jefferies three-target initiation). Lead with the **verdict line**: rating + 12-month base-case PT + implied upside/downside % vs last close + valuation method. Then the table:

| Case | Price target | Valuation multiple | Forward-year EPS / metric | Rough prob. | Swing-variable value | 1-line driver |
|---|---|---|---|---|---|---|
| Bull | … | e.g. 30× | FY+2 EPS … | …% | levers set high | … |
| Base | **headline PT** | … | … | …% | levers mid | … |
| Bear | … | e.g. 20× | lower FY EPS … | …% | levers set low | … |

- **The base case IS the headline PT.** Every PT must decompose as `multiple × forward-EPS` so it is auditable; never ship a bare number.
- Below the table, compute a **probability-weighted expected-value PT** (`Σ prob × PT`, show the inputs) and an explicit **upside : downside ratio** vs last close (the Bernstein Novo "+34% / −38%" asymmetry form). Probabilities should sum to 100%.
- **The debate's own scenario PTs are stated vs *last close* (today's spot), which is correct for a freshly-built case. But whenever either side quotes a *borrowed* analyst PT** — the MS/UBS/JPM target carried over from the company-research `*Analyst view:*` block — **pair it with the stock's price on that note's date + the upside it fixed** (`MS base PT $288 vs $232 @ 2026-06-03 → +24%`), not today's close. The report-date price is what tells the reader how much of the analyst's call has already played out; pull it from `stock_price_target_db` (`report_date_price` / `upside_pct`, shown at `/pt`) or a yfinance close on the note's date. Keep the two prices visibly distinct.
- See [scenario PT framework](references/scenario_pt_framework.md) for the per-case valuation-method menu (P/E, DCF WACC/TGV, RIM, SOTP, FCF-yield), the upside-vs-downside two-list convention, and the named bank exemplars.
- If you render a PT fan-chart or upside/downside bar (optional), annotate the source + "last close as of DATE" **inside the image** and clip the price axis to the actual data range (global chart rule).

## Triggers to watch

Close with a short list of **dated, falsifiable catalysts** that would flip the call, each mapped to the case it confirms — the JPM DiDi "turns positive if 2Q intl loss-rate keeps narrowing" trigger list, plus the HSBC/Citi high-priority (real worry) vs low-priority (not yet) split. Examples: next earnings date, investor day, lockup expiry, a named data read-out, a macro print. This gives [[research-manager]] a monitoring handle. Tie each trigger to an **upgrade** or **downgrade** condition.

## AI / Robotics / Semiconductor — detailed-narrative rule (MANDATORY)

When the ticker is an AI, robotics, or semiconductor name, both analysts must argue **sector-specific mechanisms**, not generic growth-vs-valuation lines: bull/bear on AI-demand durability and the capex cycle, supply-chain pricing power and chokepoints (TSMC/CoWoS, HBM, EUV), technology-roadmap risk vs named competitors, robotics design-win/timeline realism, and export-control exposure — each grounded in numbers from the three analyst reports. The scenario scorecard's swing variables should be sector-native (e.g., hyperscaler capex growth, HBM ASP, units shipped), not generic placeholders.

## Output

Return the complete `debate_history` markdown — alternating `Bull Analyst:` and `Bear Analyst:` paragraphs, in order, for `2 × rounds` turns total — **followed by the Scenario scorecard, the Sell-side view evolution (卖方观点演变) block (required when ≥2 zsxq notes were used), and Triggers-to-watch blocks**.

The orchestrator passes this transcript to the [[research-manager]] skill next.

See [debate methodology](../../../references/debate_methodology.md) for additional guidance on tone and engagement.

## Further viewing — explainer videos (optional, but default to including)

When the debate hinges on something a reader would struggle to picture from prose alone — and an upstream analyst report did not already visualize it — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* the thing both sides are arguing over: a mechanical assembly (a humanoid robot's actuators / harmonic reducers / ball-screws / force sensors), the manufacturing or scientific process that drives the swing variable, a complex product architecture, an unfamiliar business model, or a market-structure concept. Default to including them whenever a hard concept is introduced in the debate or scorecard; omit only when the transcript is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the debate / scorecard, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Persist output

Write the transcript to `<company-folder>/trading/<TRADE-DATE>/bull-bear-debate.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
