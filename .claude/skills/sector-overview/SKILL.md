# Sector Overview

description: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".

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
