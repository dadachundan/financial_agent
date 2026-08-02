---
name: heavy-workflow-memory
description: Memory-safety procedure for launching multi-agent report fan-outs on this 16 GB M4 MacBook Air — the mem-watch-16gb.sh watcher, free-%-based thresholds, concurrency sizing, and recovery from OOM/empty-folder debris. Load before launching ANY ≥2-wide fan-out (parallel Agent calls or Workflow parallel()) or chaining >3 report agents (/company-research, /sector-overview, /compare-companies, /etf-overlap, /theme-research, /initiating-coverage). The root CLAUDE.md keeps only the hard-rule summary; the full watcher script and calibration tables live here.
---

# Workflow Memory Monitoring (heavy multi-agent fan-outs)

> **⚠️ HARDWARE (verified 2026-06-09 via `system_profiler SPHardwareDataType`): this machine is a 16 GB Apple M4 MacBook Air (`xs-macbook-air.local`) — NOT the 96 GB Mac the original version of this section assumed.** Total RAM is 16 GB; at idle (Claude app + the user's Flask `:5001` + OS) only ~8 GB is free and swap already sits at ~3–6 GB. The GB-denominated thresholds and the "concurrency-3 is safe" guidance written for 96 GB are **superseded** — they would never fire before this box OOMs. The operative rule here: **run `/company-research` (and any 6–10k-word report skill) fleets STRICTLY sequential, concurrency 1**, and prefer **Agent-tool subagents (separate OS processes, fully reclaimed on exit)** over in-process Workflow `agent()` calls. The 96 GB calibration is kept below only as documented history; the 16 GB numbers are what to follow.

**Before launching any multi-agent fan-out — especially `/company-research` fleets, batched `/sector-overview` runs, large `compare-companies` panels — start the memory watcher.** Past failure (on the **prior 96 GB machine**): a 6-wide `/company-research` workflow OOM-killed the entire Claude Code session at ~93 GB total RSS (the macOS jetsam ceiling on that 96 GB Mac); 4 EN reports were partially saved as orphan debris and the remaining ~46 companies never started. On the **current 16 GB machine** the failure surface is far closer: even 2 concurrent heavy agents thrash. **Validated 2026-06-09:** 9 sequential `/company-research` reports (RKLB/LUNR/RDW/FLY/VOYG/KRMN/KTOS/LMT/NOC) at concurrency 1 ran cleanly — worst memory pressure over the ~2h45m run was **34% free RAM**, never near the danger line. Sequential-1 is the proven-safe envelope here; the 300+ existing `reports/company/` folders likewise prove the skill runs fine one-at-a-time. The danger is fan-out, not the skill.

## When the rule applies

Any of:
- Launching **≥2 concurrent** report agents of any kind (Workflow `parallel()` OR multiple `Agent` tool calls in one message) — on 16 GB the bar is 2, not 3
- Chaining multiple report agents sequentially at fleet scale (`/company-research`, `/sector-overview`, `/compare-companies`, `/etf-overlap`, `/theme-research`, `/initiating-coverage`, or any report-generating skill, >3 tickers in one orchestration)

If a single agent is being spawned (e.g. one `/company-research X` call), the watcher is optional but cheap — on this 16 GB machine a single heavy agent peaks around 2–5 GB (the harness caps the V8 heap far below the 8–15 GB it reserves on a 96 GB box), leaving comfortable headroom. Start the watcher anyway for a multi-report chain.

## What "memory-heavy" means in practice

**Critical finding (verified empirically 2026-06-03, on the 96 GB machine):** Workflow `agent()` calls do NOT spawn separate OS processes — all N concurrent in-process agents share the parent main-loop claude process's V8 heap. Verified by `pgrep -P <main-claude-pid>` returning no children during a 4-wide workflow, while the JSONL files showed all 4 agents actively writing. **`Agent`-tool subagents, by contrast, run as separate `claude` child processes** — their heap is isolated and the OS reclaims it fully on exit. **On constrained 16 GB RAM this distinction is decisive: prefer `Agent`-tool subagents over in-process Workflow `agent()` calls**, because peak memory is then bounded to `main loop + 1 subagent` and a runaway agent can't take the interactive session's heap down with it.

Implications:
- **In-process (Workflow) memory grows monotonically with `N × per-agent context size`** as PDFs, transcripts, and tool results accumulate; you cannot kill one in-process agent (the only mid-flight intervention is `TaskStop <workflow-id>`). **Separate-process (Agent-tool) memory is per-child and reclaimed on exit** — the safer model here.
- **The 2026-06-03 OOM at 93 GB was a single in-process workflow hitting macOS jetsam**, not a sum across N processes.

What a report agent accumulates (in its heap — shared, for Workflow; isolated, for Agent-tool):
- V8 base heap + context reservation; every PDF read (10-K is 1–10 MB extracted text, retained in the message array); every WebFetch / transcript / IR deck / web page; tool-result buffers.

**Per-agent footprint differs wildly by host RAM** because V8 sizes its heap to available memory: on the 96 GB box a `/company-research` writeup held **8–15 GB**; on this **16 GB box the same agent peaks ~2–5 GB** (observed 2026-06-09 — worst whole-run pressure was 34% free ≈ 5.4 GB free, with one subagent live). So the OOM math is host-specific: at concurrency 1 on 16 GB there is comfortable headroom; at concurrency 2 the user's Flask `:5001` + Claude app + 2 subagents start contending for the ~8 GB of free RAM and the machine swaps hard; concurrency 3+ OOMs. V8 does not return heap to the OS until an agent finishes and its conversation is GC'd (by design, not a leak) — which is exactly why the separate-process Agent-tool model (full reclaim on exit) is preferred on low RAM.

## The watcher (alarm-only — workflow agents are in-process)

The 16 GB-calibrated watcher script lives at `/tmp/mem-watch-16gb.sh` (free-%-based; the old GB-threshold `/tmp/mem-watch.sh` is for the 96 GB machine — don't use it here). It polls every 30s normally / 15s in `warn` / 10s in `danger`, logs to `/tmp/mem-watch.log`, and **fires macOS osascript notifications at each threshold**. It is **alarm-only**: at concurrency 1 with Agent-tool subagents there is nothing to auto-kill from the chain (each subagent is its own process and you simply don't launch the next until the prior returns); for an in-process Workflow the only mid-flight intervention remains `TaskStop <workflow-id>`. The watcher's job is to **alert early enough to stop launching / `TaskStop` before the box swaps to death.**

**Thresholds** (free-% based, for 16 GB total RAM — `memory_pressure` "free percentage"):

| System free RAM | Notification | Poll cadence |
|---|---|---|
| ≥ 25% (≈4 GB+) | log `ok` | 30s |
| < 25% | log `warn` (climbing) | 15s |
| < 12% (≈2 GB) | osascript: "DANGER — halt the agent chain" | 8s |
| < 6% (≈1 GB) | osascript: "EMERGENCY — stop the running agent NOW" | 5s |

There is no fixed GB ceiling to leave headroom against; the signal is free-% collapsing and swap climbing fast. Validated 2026-06-09: a 9-report sequential run bottomed at **34% free** — i.e. it never even reached `warn`.

**Sizing by memory budget on 16 GB** — total RAM 16 GB, ~8 GB free at idle (Claude app + Flask `:5001` + OS), per-agent peak ~2–5 GB:

| Concurrency | Approx. free-RAM draw | Safe on 16 GB? |
|---|---|---|
| 1 | one ~2–5 GB subagent | ✓ proven safe — **the rule for `/company-research` fleets here** |
| 2 | two subagents contend for ~8 GB free with Flask live | ⚠️ marginal — swaps hard; avoid unless free RAM is >60% and no Flask running |
| 3+ | exceeds free RAM | 🚨 OOM / thrash — never |

## How to launch the watcher

The 16 GB watcher reads `memory_pressure` free-% (no kill logic, no session whitelist — it's alarm-only). It already exists at `/tmp/mem-watch-16gb.sh`; if missing, recreate it:

```bash
cat > /tmp/mem-watch-16gb.sh <<'WATCH'
#!/bin/bash
LOG=/tmp/mem-watch.log; : > "$LOG"
while true; do
  FREE=$(memory_pressure 2>/dev/null | grep -i 'free percentage' | grep -oE '[0-9]+' | head -1); [ -z "$FREE" ] && FREE=100
  RSS=$(ps -axo rss,comm | grep -iE 'claude|node' | grep -v grep | awk '{s+=$1} END{printf "%.1f", s/1024/1024}')
  SWAP=$(sysctl -n vm.swapusage 2>/dev/null | sed -E 's/.*used = ([0-9.]+[MG]).*/\1/')
  if   [ "$FREE" -lt 6 ];  then S=EMERGENCY; C=5;  osascript -e 'display notification "Free RAM <6% — stop the agent NOW" with title "MEM EMERGENCY"' 2>/dev/null
  elif [ "$FREE" -lt 12 ]; then S=DANGER;    C=8;  osascript -e 'display notification "Free RAM <12% — halt the chain" with title "MEM DANGER"' 2>/dev/null
  elif [ "$FREE" -lt 25 ]; then S=warn;      C=15
  else                          S=ok;        C=30; fi
  echo "$(date '+%H:%M:%S')  $S  free=${FREE}%  claude+node_RSS=${RSS}GB  swap_used=${SWAP}" >> "$LOG"; sleep "$C"
done
WATCH
chmod +x /tmp/mem-watch-16gb.sh
nohup bash /tmp/mem-watch-16gb.sh >/dev/null 2>&1 & disown
```

**Verify before launching the chain:**

```bash
pgrep -lf 'mem-watch-16gb.sh'      # confirm watcher PID running
tail -3 /tmp/mem-watch.log         # confirm free-% readings
```

## What to tell the user when launching a heavy workflow

Before kicking off the chain, send one short message that confirms (a) watcher is running, (b) the concurrency-1 plan, (c) live-tail command. Example:

> Watcher live (PID 4081), alarm-only on a 16 GB box. Running `/company-research` STRICTLY sequential (concurrency 1) — one Agent-tool subagent at a time, next launches only after the prior returns. Thresholds: warn <25% free, danger <12%, emergency <6%. Live tail: `tail -f /tmp/mem-watch.log`.

## Recovery when a subagent dies or is stopped

With concurrency-1 Agent-tool subagents there is no auto-kill — if free RAM collapses you simply stop launching the next subagent (and `TaskStop` the current one if it's an in-process Workflow). A subagent that dies/returns empty → empty `reports/company/<slug>/` folder = the "empty-folder debris" pattern.

After the chain completes:
1. Find empty `reports/company/<slug>/` folders that were in the target list (`find reports/company/<slug> -name "*.md" 2>/dev/null` returns nothing).
2. Re-launch a tiny catch-up for just those tickers, still at concurrency 1.
3. Commit + push the catch-up's results separately.

## Hard rules

1. **On this 16 GB machine, run `/company-research` (and every 6–10k-word report skill) fleets at concurrency 1 — strictly sequential.** One report agent at a time; launch the next only after the prior returns. Concurrency 2 is marginal (only if free RAM >60% and Flask not running); 3+ OOMs. (The old "concurrency ≤3 is safe" rule was for the 96 GB machine and does NOT apply here.)
2. **Prefer `Agent`-tool subagents (separate processes) over in-process Workflow `agent()` for report fleets on this hardware** — isolated heap, full reclaim on exit, peak bounded to `main + 1 subagent`.
3. **Never launch a ≥2-wide fan-out without the watcher running.** If `pgrep -lf 'mem-watch-16gb.sh'` returns nothing, start it first.
4. **Watcher is alarm-only.** With concurrency-1 Agent-tool subagents the recovery is "don't launch the next one"; for an in-process Workflow it's `TaskStop <workflow-id>`.
5. **When the watcher hits DANGER (<12% free), stop launching immediately** (and `TaskStop` any in-flight Workflow) — do not wait for "one more tick". Swap does not free up until agents finish.
6. **The thresholds are free-% based, not GB.** Do not reintroduce GB ceilings — they are 96 GB-machine artifacts. If the hardware changes again, re-derive from `hw.memsize`.
7. **Never report a chain as "running fine" without checking `/tmp/mem-watch.log` AND `pgrep -lf 'mem-watch-16gb.sh'`** — the watcher's status column is the source of truth.
8. **Stop the watcher when the chain finishes** (`pkill -f mem-watch-16gb.sh`) — otherwise it lingers across sessions and pollutes the next launch.
