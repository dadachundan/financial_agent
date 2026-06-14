# Step 10 — Verification recipes & log template

The bash recipes and the verification-log template for SKILL.md § "Step 10 —
Verification pass". Step 10 itself (the intent, when it runs, and the 10.5
self-audit checklist) stays in SKILL.md; this file holds the mechanical how-to so
the workflow reads lean. **Run verification on every report file produced** (default:
the Chinese report; bilingual mode: both). Skip only if the user explicitly waived it.

## 10.1 — Verify every URL resolves

```bash
REPORT=reports/company/<Slug>/<filename>.md
for url in $(grep -oE 'https?://[^)]+' "$REPORT" | sort -u); do
  code=$(curl -sSL -A "Research Analyst <your-email>" --max-time 12 -o /dev/null -w "%{http_code}" "$url")
  echo "$code  $url"
done | grep -v '^200 ' | grep -v '^301 ' | grep -v '^302 '
```

Any 404 must be either fixed (find the real URL) or removed. 403 and 406 are usually anti-bot blocks (semi.org, Yahoo Finance, congress.gov, LinkedIn) — confirm those URLs work in a real browser before keeping them.

**Local zsxq viewer URLs** (`http://xs-macbook-air.local:5001/zsxq/pdf/<file_id>/<filename>`) only resolve on the user's machine, so the loop above may report a connection failure if the server isn't reachable from where you run it. Verify them against the live route instead — `/opt/anaconda3/bin/python3 .claude/skills/zsxq-analyze/scripts/find_pdf.py --file-id <file_id>` must return the row with `local_exists: true`, and its `pdf_url` is the citation URL to paste. The path must be `/zsxq/pdf/<file_id>/<filename>` (direct download); the `/zsxq/pdf-viewer/<id>` viewer page does not download on iPad and the old `/zsxq-pdf/<id>` form is a dead 404 — if any citation uses either, fix it.

## 10.2 — Verify SEC filenames came from the EDGAR submissions JSON

For US issuers, every SEC URL has the form:
`https://www.sec.gov/Archives/edgar/data/<CIK>/<accession-no-dashes>/<filename>`

The `<filename>` is opaque — `lrcx-20250629.htm`, `tsla-20241231.htm`, `f43373e10vk.htm`, `ny20050572x2_def14a.htm`. **Never construct it by pattern.** Look it up via the EDGAR submissions API:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://data.sec.gov/submissions/CIK<10-digit-zero-padded-CIK>.json" \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d['filings']['recent']
for i, f in enumerate(r['form']):
    if f in ('10-K', '10-Q', '8-K', 'DEF 14A', '20-F', '6-K'):
        print(f, r['accessionNumber'][i], r['filingDate'][i], r['primaryDocument'][i])
"
```

For 8-K *exhibits* (the cover doc is rarely the exhibit you want), fetch the filing's directory listing:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://www.sec.gov/Archives/edgar/data/<CIK>/<accession-no-dashes>/index.json"
```

If you cannot resolve a real filename, cite the filing index page (`.../index.html`) instead of inventing one.

## 10.3 — Verify 10-K-cited claims actually appear in the 10-K

Spot-check every paragraph that cites the 10-K. Cache the 10-K once:

```bash
curl -sS -A "Research Analyst <email>" \
  "https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<primaryDoc>" > /tmp/10k.htm
```

For each cited number / fact, grep:

```bash
grep -ioE '.{40}<search-string>.{200}' /tmp/10k.htm | sed -E 's/<[^>]+>/ /g; s/&nbsp;/ /g; s/[[:space:]]+/ /g'
```

If the number / claim isn't in the 10-K, the citation is wrong. Either find the real source or drop the claim.

**Specific patterns to grep for and check:**
- `"primary competitor"` / `"主要竞争对手"` — verify the report's competitor list matches the 10-K Competition section verbatim
- `"approximately X%"` for any percentage cited — make sure the actual percentage appears
- Revenue line items (`Systems Revenue`, `Customer Support`) for segment % claims
- Restructuring / headcount claims (`Note 20`, `restructuring`)
- Customer concentration (`major customer`, `customer concentration`)

## 10.4 — Verify executive names against 8-Ks / DEF 14A

Every named executive must appear by exactly that name in the cited filing. Grep the cached 8-K / DEF 14A:

```bash
curl -sS -A "..." "<8-K URL>" | sed -E 's/<[^>]+>/ /g' | grep -i "<executive name>"
```

If the name isn't in the filing, the citation is fabricated. Remove the claim or find the right filing.

## 10.6 — Verification-log template

After the References section in **every report produced** (the Chinese report by default; both Chinese and English in bilingual mode), append a `<details>` block listing what was checked. This makes verification visible to the reader and forces honesty about residual unknowns. **The `<summary>` line MUST be the exact English string `Verification log (Step 10) — YYYY-MM-DD` even in Chinese reports** — project tooling greps for it; a translated summary (`验证日志…`) breaks the contract. Chinese annotation may follow inside the block body. The logs may differ slightly between languages (e.g., different filings checked) but follow the same structure:

```markdown
<details>
<summary>Verification log (Step 10) — YYYY-MM-DD</summary>

**URL check** — all <N> URLs HTTP-checked YYYY-MM-DD; all return 200 / known-good 301.

**Step 0.5 sec-report-summary** — ran (in-session scratch `/tmp/finagent-sec-summary/<TICKER>.md`, not persisted under `reports/`) / skipped (<reason>) / n/a (non-US issuer).

**Further-viewing URLs** — <N> links validated (200 with a browser UA) / omitted because <reason — e.g. "purely numeric report, nothing worth visualizing">.

**SEC filenames** — resolved from EDGAR submissions JSON for CIK <padded>; primary docs: 10-K = `<filename>`, latest 10-Q = `<filename>`, DEF 14A = `<filename>`.

**10-K spot-checks** (claim → location in 10-K):
- Revenue $XB ✓ (MD&A Results of Operations)
- Gross margin XX% ✓ (MD&A)
- Top customer concentration NN%/MM% ✓ (Note 19 / Segment Reporting)
- Geographic mix ✓ (Results of Operations geographic table)
- Restructuring headcount ✓ (Note 20)

**Financial-statement charts (`financial_charts.py`)** — figures in each Sankey / donut / DuPont string-matched to the cited statement (e.g. "Revenue $10.1B, COGS $3.4B, Net Income $2.9B" ✓ matches FY2025 Statements of Operations); `--source` footer present; surrounding paragraph carries the page-level citation.

**Money-flow diagram (`financial_charts.py moneyflow`)** — every node is a real, sourced counterpart (no invented suppliers); each number in a ribbon label OR a "Follow the money" card body string-matched to a source cited in the surrounding paragraph (e.g. "AI6 fab · $16.5B" ✓ matches the cited deal announcement; card "capex topped $11B" ✓ matches the cited 10-K); `--source` footer present; the "follow the money" caption names the chokepoint(s) and cites each link. If dropped, the reason (chain not sourceable) is logged here.

**Chart render-check (10.7)** — `lint_report_charts.py` exit 0 (<N> svg within viewBox / <M> mermaid blocks); local viewer launched on :5002, report screenshot eyeballed — all Sankey nodes connected, donut/radar sane, no clipped/overlapping labels, every Mermaid block rendered (no syntax-error box). Server stopped after.

**Analyst-view sentences** (intentionally not cited to a primary source):
- Section 1: "<paragraph fragment>" — uncited; supported by industry observation.
- Section 4.1 / 4.2 / 4.3: share-leadership claims labeled `*Analyst view:*` / `*分析师观点：*` per skill rule.

**Institute research (`db/zsxq.db`)** — searched N aliases (ticker / English / 中文); found M relevant notes, fetched K via downloader. Cited file_ids: `<id>`, `<id>`, … — each labeled *Analyst view:*, routed via `/zsxq/pdf/<file_id>/<filename>`, numbers string-matched to summary/OCR (e.g. "MS NVDA PT $288 / 2027E EPS $13.08 × 22×" ✓ matches `file_id 812488522252442` summary).

**Residual unknowns / not yet verified:**
- <bulleted list, or "none">

</details>
```

If the log shows residual unknowns the user cares about, fix them before declaring done. Every report produced (Chinese always; English when bilingual) must be verified and signed off before final submission.
