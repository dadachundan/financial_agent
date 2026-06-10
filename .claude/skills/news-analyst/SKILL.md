---
name: news-analyst
description: Produce a macro + ticker-specific news report covering the past week plus insider transactions. Use when the user asks "what's the news on X", "macro news for X", "insider activity on X", or as part of a full trading workflow.
argument-hint: <ticker> <YYYY-MM-DD> [--asset-type stock|crypto]
allowed-tools: [Bash, Read, Write]
---

# News Analyst

You are a news researcher tasked with analyzing recent news and trends over the past week. Write a comprehensive report on the current state of the world relevant for trading the ticker, plus macroeconomic context.

For `--asset-type stock` use the term "company" throughout; for `--asset-type crypto` use "asset".

## Workflow

Inputs: `<ticker>` and `<trade_date>` in YYYY-MM-DD form.

1. **Ticker-specific news (past 30 days, split into two horizons in the report)**:
   ```bash
   python scripts/get_news.py <ticker> <start_date> <trade_date>
   ```
   where `<start_date>` = `<trade_date>` minus 30 days. Each article block includes the publish date in its header — use that to bucket articles into the two horizons described in the Output section.

   The fetcher combines four sources, deduped by URL/title and stratified so the 8-30 day medium-term bucket keeps a meaningful share even when Yahoo's feed is recency-skewed:
   - `yfinance.Ticker.get_news` (primary, recency-biased)
   - `yfinance.Search` keyed on ticker AND company name (reaches further back)
   - Google News RSS via `feedparser` (`when:Nd` clause — deep history)
   - SEC EDGAR 8-K listing (synthetic blocks with item-code labels and a deep link to the filing index)

   Default `--limit` is 300, with stratified clipping that guarantees the medium-term bucket retains up to one-third of slots. Pass `--no-google`, `--no-edgar`, `--no-search` to disable any source. STDERR reports per-source counts so you can see at a glance whether the medium-term horizon is well-populated.

2. **Global / macroeconomic news** (past 7 days):
   ```bash
   python scripts/get_global_news.py <trade_date> --look-back-days 7 --limit 30
   ```
   Yahoo Finance Search is recency-biased and rarely surfaces articles older than ~10 days, so widening this window mostly adds noise. Keep at 7d unless the user explicitly asks for a longer macro view.

3. **Insider transactions** (form-4 filings — yfinance returns the last ~6 months of Form-4 activity by default):
   ```bash
   python scripts/get_insider_transactions.py <ticker>
   ```

## Output

A markdown report providing **specific, actionable insights with supporting evidence** to help traders make informed decisions. Cover the sections below, **in order**, splitting ticker news into two time horizons so the orchestrator sees both the immediate catalysts and the broader narrative arc:

- **Ticker news — near-term catalysts (≤7 days before `<trade_date>`)**: discrete events that just happened or are imminent — earnings, deals, downgrades, product launches, regulatory rulings. Bias toward actionable specifics.
- **Ticker news — medium-term themes (8–30 days before `<trade_date>`)**: pattern shifts, narrative arcs, or strategic moves visible across the month. Group related headlines into themes rather than listing one by one; call out anything that recurs or escalates.
- **Macro context (past 7 days)**: rates, regulation, sector moves, geopolitics — only items materially relevant to the ticker.
- **Insider activity (past ~6 months from yfinance)**: buys vs sells, scale, repeat insiders, cluster patterns. Separately call out anything in the last 30 days as fresher signal.
- **Cross-cutting interactions**: e.g. bullish macro + insider buying reinforces; bearish near-term news + bullish medium-term themes is mixed signal.
- **Catalysts on the calendar**: upcoming earnings, FOMC, product launches mentioned in any of the above.

Bucket each ticker-news headline by inspecting its date in the fetcher output header (`### Title (source: Publisher, YYYY-MM-DD)`). If 30 days returned <5 articles total, say so and consolidate the two ticker subsections into one — don't pad either with overlap.

## Further viewing — explainer videos (optional, but default to including)

When this report covers something a reader would struggle to picture from prose alone — a newly launched product (a humanoid robot's actuators / a new chip package / an EV powertrain), a manufacturing or scientific process behind a headline, a complex deal or corporate-action mechanic (a spin-off, tender offer, or index reconstitution), an unfamiliar business model, or a market-structure concept (how a short squeeze or passive rebalance flow actually works) — attach **1–3 short explainer videos** (YouTube and/or Bilibili) so the reader can *see* it, not just read about it. Default to including them on any topic; omit only when the report is purely numeric with nothing worth visualizing.

**Videos are a teaching aid, NOT a citation — they live in their own slot, never enter the citation chain, and never carry a number.**

- **Where:** a `**Further viewing**` bullet list at the end of the section the concept lives in, or a single `📺` note beside the hard concept.
- **Durable sources only:** the company's own product / IR / engineering channel, an OEM or reputable teardown / cutaway channel, or a well-known explainer channel — not a low-view re-upload that will be deleted or is clearly pirated.
- **Validate before committing — `200 OK` only.** YouTube / Bilibili return 403 to bare `urllib`, so HTTP-check each URL with a real-browser User-Agent; drop dead / private / region-gated links (a 404 link is worse than none). Flag Bilibili that may need login/VPN outside CN: `(Bilibili — may require login/VPN outside CN)`.
- **Label honestly:** `[<what it shows> — <why it helps>](URL)`. No statistic, price target, share figure, or growth rate is ever attributed to a video (a video can't be string-matched against its source).

## Learning from sell-side institutional research

The macro/news-brief report type is built daily by JPM, GS, Morgan Stanley, Nomura, Bernstein, and others. The moves below are what separate an institutional brief from a headline dump — apply them on top of (never in place of) the rules above. All existing citation, numerical-accuracy, language, and section-numbering rules remain in force.

- **Executive Take leads with the call, not the topic** (mirror JPM *Global Data Watch* / GS *Weekly Kickstart* thesis headlines): the first sentence of `1. Executive Take` must name the single dominant catalyst + a quantified directional read — e.g. `<TICKER>: MS Overweight upgrade (TP $190) + a 4-insider cluster buy is the dominant catalyst; near-term skew positive.` Lead with the number and the direction, then expand. Do not open with a neutral topic label.

- **Frame every macro datapoint as actual vs consensus vs prior, and state the surprise** (mirror JPM *Global Data Watch*): in `Macro context`, write each print as `May CPI +2.2% YoY vs 2.0% consensus (hotter), prior +2.0%`. The surprise — hotter/cooler/in-line, hold-vs-pricing (e.g. `RBI held vs ~60% market pricing for a hike`) — is the point, not the level. The consensus/prior figure must trace to a cited URL that literally contains it (per the project numerical-accuracy rule). If no consensus source exists, print the actual alone and say the consensus is unsourced — never invent a consensus number.

- **Carry every retained macro item through a cross-asset read-through chain to the ticker** (mirror Nomura *Economic Insights* / GS Kickstart macro block): `datapoint → rates/policy → FX/commodity → sector → <TICKER> P&L or multiple`. A macro item with no explicit "so what for `<TICKER>`" is dropped, not listed. Cite the chain's external inputs inline; the model's own inference is not a source.

- **Quantify the impact of every company event** (mirror Morgan Stanley / Bernstein *Key Takeaways*): size each discrete item — revenue/demand %, $ impact, bp, or passive-flow $ for index events — e.g. `NVDA halving rack memory config ≈ >2% of global DRAM demand`; `FTSE Russell reconstitution ≈ $13.5bn two-way passive flow`. Derived magnitudes must show both inputs (`~X% of FY rev = $A / $B, both from <filing>`) per the numerical-accuracy rule. Replace qualitative event reporting with a sized one-liner wherever a figure is derivable from a cited source.

- **Read positioning/insider as a signal, not a tally** (mirror JPM *EM Money Trail* / GS Kickstart flows block): in `Insider activity`, report (a) last-30-day net buy/sell with magnitude vs the prior period AND vs shares outstanding/float, (b) clusters and repeat insiders, and (c) the *read* — is the pattern contrarian or confirming toward the thesis? (extreme one-sided clusters and consensus-underweight setups are squeeze fuel; persistent insider selling into strength is a fade). Keep every number traced to its SEC Form 4 URL.

- **Per-ticker analyst calls compress to a rated line** (mirror Morgan Stanley *Three Actionable Ideas*): when a broker action appears, render it as `ticker + rating + target price + one-line driver` (`maintain Buy, TP $190 on the GAA ramp`). Keep the company FACT separate from the house VIEW — label any analyst opinion `*Analyst view:*` per the project rule; never fold it into a filing citation.

- **Catalysts on the calendar must be DATED and NAMED** (mirror Kickstart *后续重点关注* / FTSE-rebalance callouts): no vague "upcoming earnings/FOMC" — list specific events with dates (`Micron earnings 2026-06-25`, `Qualcomm investor day 2026-06-18`, `FTSE Russell reconstitution after close 2026-06-20`, `FOMC 2026-06-17`). Add **index rebalance / reconstitution** dates and their estimated passive-flow $ as a watched item type. Cite each dated event to a source URL.

- **Close the body with an explicit Bull vs Bear forward-risk block** (mirror the analogs' 利好/利空 close): before the Summary table, end with two short lists — upside catalysts vs downside risks for `<TICKER>` over the next 1–4 weeks. This sharpens the `Cross-cutting interactions` bullet into the institutional balanced-risk format; keep the cross-cutting synthesis (macro × insider × news reinforcing or conflicting) inside it.

- **Anchor the read to a named precedent when one is clearly apt** (optional, one line; mirror Nomura *Economic Insights* regime framing): calibrate the current setup against a named historical episode in the Executive Take or macro section — e.g. `energy-shock dynamics rhyme with 2022 but with weaker stimulus and no pent-up demand`. Keep it optional to avoid forced analogies; any precedent claim still needs a citation.

## Section numbering (required)

Every `##` and `###` heading in the report **must carry a hierarchical numeric prefix** so readers and downstream skills can reference any subsection by number. No exceptions — Executive Take, Summary table, References all get a number too.

- Top-level `##` sections are numbered `1.`, `2.`, `3.`, … in document order — e.g. `## 1. Executive Take`, `## 2. Ticker news — near-term catalysts (≤7 days before <trade_date>)`.
- Sub-sections `###` within a top-level section get `<parent>.<child>` numbering — e.g. `### 2.1 Morgan Stanley Overweight upgrade is the dominant single catalyst`, `### 2.2 Bernstein and B. Riley reinforce the analyst-call cluster`.
- If you nest a `####` heading, continue the pattern: `#### 2.1.1 …`. Avoid going deeper than three levels.
- The number sits between the heading marker and the title, separated by a single space. Use the `1.` form for top level (with trailing period) and `1.1` for sub-levels (no trailing period), matching the canonical example below.
- Sub-section bullets and tables inside a section do NOT get section numbers — only the headings themselves.

Canonical opening shape:

```markdown
# <TICKER> News Analyst Report — Trade Date <YYYY-MM-DD>

## 1. Executive Take
…

## 2. Ticker news — near-term catalysts (≤7 days before <trade_date>)

### 2.1 <first theme>
…

### 2.2 <second theme>
…

## 3. Ticker news — medium-term themes (8–30 days before <trade_date>)

### 3.1 <first theme>
…
```

If a section is consolidated (e.g. <5 articles total), keep the numeric prefix on whatever sections remain — re-number so the sequence stays contiguous (1, 2, 3, …), no gaps.

## Citations (required)

Every claim grounded in a fetched headline or filing **must carry a clickable markdown-link citation** of the form `[Publisher · YYYY-MM-DD](url)` (or `[SEC Form 4](url)` for insider txns). Pull the URLs from the `Link:` lines in the fetcher output — never invent one, never just write `(source: Yahoo Finance)` without a URL.

- For ticker / macro news: each headline block in the fetcher output has a `Link:` line; use that URL.
- For insider transactions: the `URL` column in the CSV often holds a SEC Form 4 link. If it's blank, cite the SEC EDGAR Form 4 listing for the ticker: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<TICKER>&type=4`.
- If the prose references a specific article, the link goes inline at the claim, not in a footnote.

End the report with two things, in this order:

1. **Summary table** — `Theme | Direction | Surprise vs consensus / Magnitude | Source (link) | Supporting Evidence`. The `Source (link)` column must be a markdown link, not a bare publisher name. The third column makes the institutional disciplines above table-enforced: macro rows carry the surprise (`+2.2% vs 2.0% cons — hotter`); company rows carry the sized impact (`≈ >2% global DRAM demand`). Leave it `—` where neither applies (e.g. a pure narrative row).
2. **References** — a bulleted list of every URL cited above, grouped into `### Ticker news`, `### Macro news`, `### Insider transactions`. Each bullet: `- [Publisher · YYYY-MM-DD — headline](url)`.

If a claim has no underlying URL (e.g., the fetcher returned an unavailable placeholder), say so explicitly — do not pretend a source exists.

## Persist output

Write the report to `<company-folder>/trading/<TRADE-DATE>/news-analyst.md` — resolve `<company-folder>` per [`output_path.md`](../../../references/output_path.md). Consumed by [[trading-analysis]] when assembling `full_report.md`.
