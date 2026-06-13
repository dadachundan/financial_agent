# Investor-relations materials — the full collection bar

After 10-Ks / 年度报告 / Yuho, **investor-relations materials are the next-most-load-bearing source category** in a research report — often *more* informative than the formal filings for the specific things research readers care most about: segment-mix economics, TAM / SAM views the company itself endorses, customer-cohort disclosures the legal filings round off, capital-allocation roadmaps, capacity build-out plans, and management's own framing of the competitive moat. **Whenever IR materials exist, treat collecting them as a non-optional Step 1 task and cite them aggressively throughout the report.**

**What "IR materials" means — collect ALL of these when they exist:**

- **Quarterly earnings deck** (slides accompanying each earnings call, every quarter — usually filed as 8-K Exhibit 99.2 for US issuers, or posted on the IR site for non-US issuers). These contain the freshest segment-mix charts, geographic mix, customer cohort updates, and KPI bridges.
- **Quarterly earnings call transcript** (or audio webcast if no transcript). The Q&A section in particular surfaces detail that doesn't appear anywhere else — competitor positioning, customer ramp dynamics, gross-margin drivers, capacity expansion timing.
- **Annual investor day / capital markets day deck** (typically held every 1–3 years; 100+ slides; multi-year guidance and TAM build-up). Each annual / triennial Investor Day is its own goldmine — pull every one available going back ~3–5 years.
- **Industry conference presentations** (JPMorgan Healthcare, SEMICON, OFC, CES, Bank of America Industrials, Goldman Sachs Communacopia, Morgan Stanley TMT, Citi Global Tech, etc.). Each major conference appearance typically has a deck on the IR site — these contain crisper strategy framings than the formal earnings deck.
- **Industry / product event keynotes** (NVIDIA GTC, Apple WWDC, Tesla AI Day / Battery Day, Salesforce Dreamforce, Microsoft Ignite, AWS re:Invent product keynotes when the speaker is the CEO or CFO). For product-led companies these contain the most detailed product roadmaps.
- **Annual integrated report / ESG report / corporate sustainability report** (especially for Japanese, European, and Asian issuers — these often contain TAM views, segment narratives, and customer-base detail that don't appear in the Yuho / annual report). Japanese issuers' "Integrated Report" / 統合報告書 is often the richest single document.
- **Annual shareholder letter** (Buffett-style; for issuers that publish one — Amazon, Berkshire, JPMorgan, Klarna, etc.). Often contains the CEO's own framing of strategy and competitive moat in their own words.
- **IPO prospectus / S-1 / 招股说明书 / F-1** (for any company that IPO'd in the last 5–10 years — the prospectus is often the most detailed business description ever published about the company, with TAM/SAM/SOM, customer concentration, technology architecture, and competitive landscape laid out in much more depth than subsequent annuals).
- **Secondary offering / convertible offering decks** (when present — often contain refreshed business descriptions and forward-looking commentary).

**Where to find them:**

- **US issuers:** company IR website (`investors.<company>.com` or `ir.<company>.com`) → "Events & Presentations" / "Quarterly Results" / "Investor Day" pages. SEC EDGAR 8-K filings often attach the deck as Exhibit 99.2 (search the filing's `index.json` directory listing). S-1 / prospectus on EDGAR.
- **China A-share / HK issuers:** company IR site (公司IR / 投资者关系页面), cninfo (巨潮资讯) attaches 业绩说明会 / 投资者交流活动记录, HKEX news room for HK issuers, and most large-cap A-share names publish 业绩说明会 PPTs at the same time as the 年度报告. Search cninfo for `投资者关系活动记录表` (formal Q&A logs are filed quarterly).
- **Taiwan issuers:** MOPS (公開資訊觀測站) → 法人說明會 (analyst meeting decks) and 重大訊息 sections.
- **Japan issuers:** company IR site → 「決算説明会資料」 (earnings call deck) + 「統合報告書」 (Integrated Report) + 「中期経営計画」 (Mid-term Plan / MTP — published every 3–5 years, contains multi-year revenue / margin / capex / ROIC targets and is by far the densest forward-looking source). TDnet (https://www.release.tdnet.info/) for the earnings-day press release; the deck is on the company site.
- **Korea issuers:** company IR site → "Earnings Release" PDFs + investor relations presentation archives. DART for the formal filings.
- **Private companies:** founder / CEO conference keynotes on YouTube, podcast transcripts (a16z, 20VC, Acquired, Stratechery, BG2, etc.), pitch decks if leaked to TechCrunch / The Information.

**Where IR slides are particularly load-bearing — and what they unlock by section:**

| Section | What IR slides typically contribute that's not in the 10-K |
|---|---|
| **1. Overview** | Latest-quarter revenue / margin chart with management's stated 1–2-yr guide; LTM KPI bridge (price × volume × mix); capital-allocation framework slide |
| **4. Products** | Roadmap slides showing what's launching in 6 / 12 / 24 months; product-family TAM breakdown; "design wins" customer logos |
| **5. Customers** | Customer-cohort retention / NRR cohort charts; named customer logos (10-Ks rarely name customers beyond the >10% threshold); geographic-mix Sankey |
| **6. Industry** | Management's own TAM / SAM build-up (with assumptions); industry-growth waterfall (units × ASP × penetration) — often more granular than third-party research |
| **7. Competitive** | Competitive-moat narrative slides ("Why we win"); side-by-side feature matrices; share-trajectory charts (handle with care — these are self-serving, but the data points are usually citable) |
| **8. TAM** | The IR deck's TAM slide is **the single most-cited TAM source** in most reports — management has done the build-up work and the slide cites the underlying research firm. Cite the deck as primary; chain-cite the underlying research as secondary |
| **9. Risks** | Management's own risk framing (which risks they're actively mitigating, capex plans for second-source supply, geographic-diversification roadmap) |

**Citation discipline for IR materials:**

- **Cite the deck at the slide level, not the deck level.** A 60-slide investor-day PDF is not a citation; "Slide 23" or "Slide 23 (TAM build)" is. Format: `[Lam Research Investor Day 2024 deck, Slide 23 — TAM build](https://ir.lamresearch.com/...)`.
- **Pull the host page URL, not a redirect link.** IR sites use redirect tags (`/news/...`, `/events/...`); follow them to the PDF or hosted page and use the canonical URL. If the deck is hosted as a PDF on the IR site, link the PDF directly.
- **Source-chain TAM citations.** When the IR deck cites Yole / Gartner / IDC for the TAM number, the citation is `[Company Investor Day 2024 deck, Slide 23 — TAM (citing Yole 2024)](https://ir.company.com/.../investor-day-2024-deck.pdf)`. The reader clicks through to the company's own deck and sees Yole credited there.
- **Earnings call transcripts vs. earnings decks are separate sources.** Cite the transcript when quoting CEO / CFO language; cite the deck for any chart or numeric callout. They are often complementary on the same earnings event — cite both when both are used.
- **Investor Day decks rarely get updated** — once you've cited one, lock the date and slide number in the title (the URL might rotate; SEC EDGAR is the most durable host for US issuers since the deck is filed as an 8-K exhibit). Re-verify the URL during Step 10.

**The "density bar" for IR citations in a finished report:**

- **At minimum 8–12 distinct IR-material citations** across the body (separate from filings, news, third-party research) when the company has a public IR program.
- **At least 1 IR citation in each of Sections 1, 4, 6, 8** when slides exist that cover that ground.
- **The latest 2 quarterly earnings decks AND the latest investor-day deck** should each be cited at least once. If only 1 of the 3 is cited, you have under-used IR materials — go back and find the right slide.
- **For Japanese / Korean / European issuers with an Integrated Report or Mid-term Plan**, that single document should generate 5–10 citations on its own (TAM, segment KPIs, capex plan, ESG / climate plan, geographic strategy).

If the company has effectively no IR program (small-cap, pre-IPO private, or genuinely doesn't host any deck publicly), note that fact explicitly in the verification log and lean harder on filings + third-party research instead. **Do not skip IR collection just because it's annoying — the absence is itself a data point worth flagging.**
