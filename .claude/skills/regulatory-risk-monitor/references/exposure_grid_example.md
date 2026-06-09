# Exposure-grid worked example — disclosed-share → EPS chain

This file operationalizes the project's **numerical-accuracy** and **derivation-shown** rules for the exposure map (SKILL.md Step 3). It is illustrative: the numbers below are modeled on the structure of J.P. Morgan's "Global Banks" China cross-border-WM note (HSBC / STAN / UBS / BAER), not a live call. Every cell in a real report must footnote a primary-disclosure URL that literally contains the input figure.

## The move: never quote a derived EPS number without its inputs

A bare line — *"HSBC EPS -3.9%"* — is a defect. The reader cannot re-derive it, and per the project rule a derived number must have **both inputs sourced in the same paragraph**. Instead, show the chain:

```
EPS impact = (affected revenue share) × (segment drop-through to EPS)
```

Each factor traces to the company's own disclosure.

## Step 1 — Classify the rule's true reach (bounds the worst case)

Bucket the file before any number (SKILL.md Core principle):

- **(i) cleanup of grey / illegal channels** — reroutes existing flow into a compliant pipe (Stock Connect / QDII). Bounded impact; existing accounts unaffected.
- **(ii) genuine new restriction** — shrinks the addressable market on *new* business.
- **(iii) outright ban** — removes the business.

The illustrative China ODI rule is bucket (i): it targets *illegal* cross-border marketing and steers flow into compliant channels — "new business only, existing accounts unaffected." That is why the hit is small despite a severe-sounding headline.

## Step 2 — The disclosed-share chain (base case)

| Factor | Value | Primary-disclosure source (must string-match) |
|---|---|---|
| HK Wealth Management = share of group revenue | 8% | `[FY 10-K / annual report segment note](URL)` |
| Visitor / cross-border-driven share of HK WM | ~25% | `[risk-factor / IR disclosure](URL)` |
| → Affected revenue share = 8% × 25% | ~2.0% of group revenue | derived (both inputs above) |
| Pre-tax drop-through of that revenue to EPS | ~1.9× (operating leverage) | `[segment margin disclosure](URL)` |
| **Base EPS impact** | **≈ -3.9%** | derived: 2.0% × 1.9 — re-derivable from cells above |

Written out in the report cell:

> *HK WM = 8% of group revenue [seg note]; ~25% visitor-driven [risk factor] → ~2.0% of revenue affected; ~1.9× drop-through [margin disclosure] → **base EPS -3.9%**.*

## Step 3 — Bound the extreme case with the regulator's documented remedy, not a guess

The worst case is **not** "what if it's really bad" — it is the regulator's own documented-remedy ceiling for analogous files:

- If the precedent remedy is a full marketing ban on the cross-border cohort (not just a channel cleanup), the affected share rises from ~25% to the full visitor cohort → recompute the chain with the larger share.
- **Extreme EPS impact ≈ -X%** where X is recomputed from the same chain with the precedent-bounded share — cited to the regulator's prior action on a comparable case, never invented.

## Step 4 — Peer ranking under the same file

| Name | Disclosed metric driving exposure | Base rev% | Base EPS% | Read |
|---|---|---|---|---|
| HSBC | HK WM 8% of group, 25% visitor | -1.9% | -3.9% | most exposed |
| STAN | HK WM 7% of group | -1.6% | -4.9% | most exposed |
| UBS | China <60% of net-new-money | minimal | minimal | insulated |
| BAER | low China dependence | minimal | minimal | insulated |

The cross-sectional spread is the calibration: when exposed names fall and insulated peers rise on the *identical* rule, the market is pricing differentiated China dependence — the move is name-specific, not sector-wide.

## Checklist before committing the grid

- [ ] Each input figure string-matches a cited primary-disclosure URL (`curl -s URL | grep -F "8%"`).
- [ ] The derived EPS number is re-derivable from the inline inputs (no orphan number).
- [ ] Base AND extreme are both stated; extreme is bounded by a documented remedy, not a guess.
- [ ] Any sell-side PT / rating used for the valuation cushion is labeled `*Analyst view:*` with a deep URL, never folded into a filing citation.
