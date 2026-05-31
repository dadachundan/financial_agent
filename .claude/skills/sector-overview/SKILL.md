# Sector Overview

description: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".

## Guardrails (at-a-glance — the rules with the worst failure modes)

- **Do not invent TAM numbers or growth rates.** Every market-size figure traces to a specific named source — research firm + report title + publication date — with the URL. "TAM ~$X B" with no source is a defect. See § "Important Notes".
- **Do not paraphrase a sell-side opinion as a primary-source fact.** "X is the share leader" is an analyst view unless a cited third-party leaderboard (IPnest, Gartner Magic Quadrant, IDC tracker, IBISWorld, IQVIA, TrendForce) says so at a specific URL. Label `*Analyst view:*` otherwise.
- **Do not let "TAM" hide the difference between addressable, served, and obtainable.** Distinguish TAM / SAM / SOM in the market-size section; mixing them is the single most common failure of sector overviews.
- **Do not skip the Data Used manifest** at the end of the report (see block below).
- **Do not ignore freshness.** Sector reports age fast — discard web sources older than 12 months unless they're landmark research. Include publication dates in link titles.
- **Do not run destructive SQL against `db/*.db`.** Read-only only. See [`CLAUDE.md`](../../../CLAUDE.md) § "Database Safety".

## Workflow

### Step 1: Define Scope

- **Sector / subsector**: What industry and how narrowly defined?
- **Purpose**: Client report, internal research, pitch material, idea generation
- **Depth**: High-level overview (5-10 pages) or deep dive (20-30 pages)
- **Angle**: Neutral landscape vs. thematic thesis (e.g., "AI infrastructure buildout")
- **Universe**: Public companies only, or include private?

### Step 2: Market Overview

**Market Size & Growth**
- Total addressable market (TAM) with source
- Historical growth rate (5-year CAGR)
- Forecast growth rate and key assumptions
- Market segmentation (by product, geography, end market, customer type)

**Industry Structure**
- Fragmented vs. consolidated — top 5 market share
- Value chain map — where does value accrue?
- Business model types (subscription, transaction, licensing, services)
- Barriers to entry (capital, regulatory, technical, network effects)

**Key Trends & Drivers**
- Secular tailwinds (3-5 major trends)
- Headwinds and risks
- Technology disruption vectors
- Regulatory developments
- M&A activity and consolidation trends

### Step 3: Competitive Landscape

**Company Profiles** (for top 5-10 players):

| Company | Revenue | Growth | EBITDA Margin | Market Share | Key Differentiator |
|---------|---------|--------|--------------|-------------|-------------------|
| | | | | | |

For each company, brief profile:
- Business description (2-3 sentences)
- Strategic positioning and moat
- Recent developments (earnings, M&A, product launches)
- Valuation snapshot (P/E, EV/EBITDA, EV/Revenue)

**Competitive Dynamics**
- How do companies compete? (price, product, service, distribution)
- Who is gaining/losing share and why?
- Disruption risk from new entrants or adjacent players

### Step 4: Valuation Context

- Sector trading multiples (current and historical range)
- Premium/discount drivers (growth, margins, market position)
- Recent M&A transaction multiples
- How does the sector compare to the broader market?

### Step 5: Investment Implications

- Where are the best risk/reward opportunities?
- What thematic bets can be expressed through this sector?
- Key debates in the sector (bull vs. bear arguments)
- Catalysts that could change the sector narrative

### Step 6: Output

**Save to** `reports/sector/<topic-slug>_<YYYY-MM-DD>.md` (relative to the project root — `/Users/x/projects/financial_agent/reports/sector/`). `<topic-slug>` is a short, descriptive slug for the sector or thematic angle (Chinese characters are allowed: e.g. `人形机器人传感器板块综述`, `ai-infrastructure-buildout`). Supplementary deliverables (Word, PowerPoint, Excel appendix) can sit next to the markdown using the same `<topic-slug>` prefix.

Deliverables:
- Markdown sector overview (primary, always)
- Optional: Word document or PowerPoint with:
  - Market overview and sizing
  - Competitive landscape map
  - Company comparison table
  - Valuation summary
  - Key charts: market growth, share trends, valuation history
- Optional: Excel appendix with detailed company data

### Data Used / 数据来源清单 (mandatory at the end of every report)

A structured manifest of evidence categories + dates + freshness. Goes immediately before the References block (or, if the report has no separate References block, at the end). Format:

```markdown
## Data Used / 数据来源清单

**Market sizing**
- Gartner / IDC / IBISWorld / IQVIA / Yole / TrendForce report titles + publication dates + URLs. Note the TAM / SAM / SOM scope of each.

**Growth & forecasts**
- Each forward growth rate cited to a named research firm or company-disclosed projection with publication date. Recent industry-research notes (last 12 months) preferred.

**Competitive landscape**
- Top 5–10 players covered — each anchored to their latest 10-K / 年度报告 / Yuho (filing date) and IR materials (deck dates). Recent M&A transactions cited to press releases.

**Valuation context**
- Sector trading multiples as of YYYY-MM-DD; recent comparable M&A transaction multiples; sources (Yahoo Finance / Capital IQ / Bloomberg / mergermarket).

**Stale notices / coverage gaps**
- <bulleted list — TAM source paywalled, private-company financials not disclosed, regulatory data delayed, or "none">.
```

The manifest distinguishes evidence categories from the consolidated References list. References list every URL cited inline; Data Used summarizes the source categories + freshness.

### Update-in-place rule — at most one report per topic

Reports under `reports/sector/` are tracked in git and meant to be living documents. **Before writing, check whether a report for this topic already exists** and update it in place rather than creating a parallel dated copy.

```bash
ls reports/sector/ 2>/dev/null | grep -i "<topic-slug-or-keyword>"
```

- **Exactly one match for this topic** → overwrite it at the same path. Keep the existing filename even if its embedded date is stale — git history records the actual revision date. Update the document's "as of" header to today.
- **Multiple matches for the same topic** (legacy state) → update the most recent by mtime, tell the user the older duplicates exist, do not auto-delete.
- **Zero matches** → create a new file using today's date in the filename.

If the user asks for a clearly different angle on the same sector (e.g. "China robotics — *export* angle" vs. an existing "China robotics — *domestic adoption* angle"), use a distinct `<topic-slug>` so the reports stay separate. The "one per topic" rule applies per topic-slug, not per sector.

## Important Notes

- Source all market size data — cite the research firm or methodology
- Distinguish between TAM hype and realistic addressable market
- Sector overviews age fast — note the date and flag data that may be stale
- Charts are essential — market size waterfall, competitive positioning matrix, valuation scatter plot
- If for a client, tailor the "so what" to their specific situation (M&A target identification, competitive positioning, market entry)
