# Rating Taxonomy

The TradingAgents pipeline uses two rating scales depending on the agent.

## 5-tier rating (Research Manager, Portfolio Manager)

| Rating | Meaning | When to use |
|---|---|---|
| **Buy** | Strong conviction in the bull thesis | Take or grow the position; high conviction. |
| **Overweight** | Constructive view | Gradually increase exposure; favorable outlook, not max conviction. |
| **Hold** | Balanced view | Maintain the current position; reserve for situations where the evidence on both sides is **genuinely balanced**. |
| **Underweight** | Cautious view | Trim exposure; take partial profits. |
| **Sell** | Strong conviction in the bear thesis | Exit the position or avoid entry. |

**Important**: do not default to Hold out of caution. Commit to a directional stance whenever the strongest evidence warrants it. Hold is for genuine ambiguity, not for hedging your own judgment.

## 3-tier rating (Trader)

| Action | Meaning |
|---|---|
| **Buy** | Open a long position (or add to existing). |
| **Hold** | No transaction this round. |
| **Sell** | Close or reduce a position (or open a short, where applicable). |

The Trader collapses the Research Manager's 5-tier rating to its 3-tier action as follows:

- `Buy` or `Overweight` → **Buy**
- `Hold` → **Hold**
- `Underweight` or `Sell` → **Sell**

Position sizing and the nuanced Overweight/Underweight calls are resolved later at the Portfolio Manager step.

## Legacy compatibility

The Trader's output ends with the literal line:

```
FINAL TRANSACTION PROPOSAL: **BUY**
```

(or `HOLD` / `SELL`). This is required for backward compatibility with consumers that grep for this exact string.
