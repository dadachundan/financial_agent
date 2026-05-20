# Memory Log Format

The decision log lives at `memory/trading_memory.md` (repo-relative). It is append-only markdown with HTML-comment delimiters between entries.

## Entry structure

Each entry has a single-line **tag** followed by a DECISION body and optionally a REFLECTION body, terminated by the separator `<!-- ENTRY_END -->`.

### Pending entry (just after decision is made)

```
[2026-01-15 | NVDA | Buy | pending]

DECISION:
**Rating**: Buy

**Executive Summary**: ...

**Investment Thesis**: ...

**Price Target**: 950

**Time Horizon**: 3-6 months

<!-- ENTRY_END -->
```

### Resolved entry (after reflection job runs)

```
[2026-01-15 | NVDA | Buy | +12.4% | +8.1% | 30d]

DECISION:
**Rating**: Buy
... (unchanged from pending) ...

REFLECTION:
The bull thesis around datacenter demand played out faster than expected ...

<!-- ENTRY_END -->
```

Tag fields, left to right:
1. `trade_date` (YYYY-MM-DD)
2. `ticker`
3. `rating` (Buy/Overweight/Hold/Underweight/Sell)
4. `raw_return` (signed percent, e.g. `+12.4%`) or `pending`
5. `alpha_return` (signed percent vs benchmark) — only on resolved entries
6. `holding_period` (e.g. `30d`) — only on resolved entries

## Read API (via `scripts/memory_log.py`)

```
python scripts/memory_log.py read --ticker NVDA          # past context for the orchestrator
python scripts/memory_log.py list                        # all entries
python scripts/memory_log.py list --pending              # just pending entries
```

`read` returns up to N_SAME (default 5) entries for the same ticker, plus N_CROSS (default 3) cross-ticker reflections, formatted as the "Lessons from prior decisions" block consumed by [[portfolio-decision]].

## Write API

```
python scripts/memory_log.py append \
    --ticker NVDA \
    --trade-date 2026-01-15 \
    --decision-file /tmp/decision.md
```

Idempotent: a second append with the same `(trade_date, ticker)` while still pending is a no-op.

## Update API (reflection job)

```
python scripts/memory_log.py resolve \
    --ticker NVDA \
    --trade-date 2026-01-15 \
    --raw-return 0.124 \
    --alpha-return 0.081 \
    --holding-days 30 \
    --reflection-file /tmp/reflection.md
```

Uses atomic temp-file + `os.replace` so a crash mid-write never corrupts the log.

## Rotation

Optional cap on resolved entries via the `memory_log_max_entries` config field. Pending entries are never rotated out (they represent unprocessed work).
