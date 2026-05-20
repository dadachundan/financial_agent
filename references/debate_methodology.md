# Debate Methodology

Two debates run in the TradingAgents pipeline. Both follow the same principles.

## Tone and engagement

- **Conversational, not bulleted.** Each turn reads like a person speaking. Avoid long lists of bullet points; argue in prose.
- **Engage with the most recent opposing argument.** The point isn't to deliver a one-shot pitch — it's to address the specific concerns or claims the other side raised.
- **Cite specific evidence.** "The 50-SMA flipped above the 200-SMA on $DATE" beats "the chart looks bullish."

## Bull/Bear debate (Stage 2)

- Two analysts: Bull and Bear.
- N rounds; each round = one Bull turn then one Bear turn.
- Inputs: the four analyst reports (market, sentiment, news, fundamentals) + the running debate transcript.
- Goal: surface the strongest version of each side so the Research Manager has a clear basis for a 5-tier rating.

## Risk debate (Stage 5)

- Three analysts: Aggressive, Conservative, Neutral.
- N rounds; each round = one of each, in order Aggressive → Conservative → Neutral.
- Inputs: the Trader's proposal + the four analyst reports + the running risk-debate transcript.
- Goal: stress-test the Trader's transaction proposal from three risk perspectives before the Portfolio Manager commits.

## Round counts by depth

The orchestrator's `--depth` flag maps to round counts:

| Depth | Bull/Bear rounds | Risk rounds |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 1 |
| 3 | 3 | 2 |

Default is `--depth 2`.

## What debates are *not*

- Not a courtroom. There is no judge interrupting; the synthesis happens after the debate ends (Research Manager for bull/bear, Portfolio Manager for risk).
- Not a tie-breaker. If after N rounds one side is clearly stronger, the synthesizing manager should commit. Hold/Neutral is reserved for genuinely balanced cases.
