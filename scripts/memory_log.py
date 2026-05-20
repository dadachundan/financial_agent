#!/usr/bin/env python3
"""Append-only markdown decision log for the trading-analysis pipeline.

The log lives at memory/trading_memory.md (repo-relative) by default;
override with --log-path. See references/memory_format.md for the schema.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

DEFAULT_LOG = "memory/trading_memory.md"

# 5-tier rating vocabulary used across the trading pipeline.
RATINGS_5_TIER = ("Buy", "Overweight", "Hold", "Underweight", "Sell")
_RATING_SET = {r.lower() for r in RATINGS_5_TIER}
_RATING_LABEL_RE = re.compile(r"rating.*?[:\-][\s*]*(\w+)", re.IGNORECASE)


def parse_rating(text: str, default: str = "Hold") -> str:
    """Heuristically extract a 5-tier rating from prose."""
    for line in text.splitlines():
        m = _RATING_LABEL_RE.search(line)
        if m and m.group(1).lower() in _RATING_SET:
            return m.group(1).capitalize()
    for line in text.splitlines():
        for word in line.lower().split():
            clean = word.strip("*:.,")
            if clean in _RATING_SET:
                return clean.capitalize()
    return default


class TradingMemoryLog:
    """Append-only markdown log of trading decisions and reflections."""

    _SEPARATOR = "\n\n<!-- ENTRY_END -->\n\n"
    _DECISION_RE = re.compile(r"DECISION:\n(.*?)(?=\nREFLECTION:|\Z)", re.DOTALL)
    _REFLECTION_RE = re.compile(r"REFLECTION:\n(.*?)$", re.DOTALL)

    def __init__(self, log_path: str, max_entries: Optional[int] = None):
        self._log_path = Path(log_path).expanduser()
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._max_entries = max_entries

    def store_decision(self, ticker: str, trade_date: str, decision: str) -> None:
        """Append a new pending entry. Idempotent on (trade_date, ticker)."""
        if self._log_path.exists():
            raw = self._log_path.read_text(encoding="utf-8")
            for line in raw.splitlines():
                if line.startswith(f"[{trade_date} | {ticker} |") and line.endswith("| pending]"):
                    return
        rating = parse_rating(decision)
        tag = f"[{trade_date} | {ticker} | {rating} | pending]"
        entry = f"{tag}\n\nDECISION:\n{decision}{self._SEPARATOR}"
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def load_entries(self) -> List[dict]:
        if not self._log_path.exists():
            return []
        text = self._log_path.read_text(encoding="utf-8")
        out = []
        for raw in (e.strip() for e in text.split(self._SEPARATOR) if e.strip()):
            parsed = self._parse_entry(raw)
            if parsed:
                out.append(parsed)
        return out

    def get_pending_entries(self) -> List[dict]:
        return [e for e in self.load_entries() if e.get("pending")]

    def get_past_context(self, ticker: str, n_same: int = 5, n_cross: int = 3) -> str:
        entries = [e for e in self.load_entries() if not e.get("pending")]
        if not entries:
            return ""
        same, cross = [], []
        for e in reversed(entries):
            if len(same) >= n_same and len(cross) >= n_cross:
                break
            if e["ticker"] == ticker and len(same) < n_same:
                same.append(e)
            elif e["ticker"] != ticker and len(cross) < n_cross:
                cross.append(e)
        if not same and not cross:
            return ""
        parts = []
        if same:
            parts.append(f"Past analyses of {ticker} (most recent first):")
            parts.extend(self._format_full(e) for e in same)
        if cross:
            parts.append("Recent cross-ticker lessons:")
            parts.extend(self._format_reflection_only(e) for e in cross)
        return "\n\n".join(parts)

    def update_with_outcome(self, ticker: str, trade_date: str, raw_return: float,
                            alpha_return: float, holding_days: int, reflection: str) -> None:
        if not self._log_path.exists():
            return
        text = self._log_path.read_text(encoding="utf-8")
        blocks = text.split(self._SEPARATOR)
        prefix = f"[{trade_date} | {ticker} |"
        raw_pct = f"{raw_return:+.1%}"
        alpha_pct = f"{alpha_return:+.1%}"
        updated = False
        new_blocks = []
        for block in blocks:
            stripped = block.strip()
            if not stripped:
                new_blocks.append(block); continue
            lines = stripped.splitlines()
            tag_line = lines[0].strip()
            if (not updated and tag_line.startswith(prefix) and tag_line.endswith("| pending]")):
                fields = [f.strip() for f in tag_line[1:-1].split("|")]
                rating = fields[2]
                new_tag = (
                    f"[{trade_date} | {ticker} | {rating}"
                    f" | {raw_pct} | {alpha_pct} | {holding_days}d]"
                )
                rest = "\n".join(lines[1:])
                new_blocks.append(
                    f"{new_tag}\n\n{rest.lstrip()}\n\nREFLECTION:\n{reflection}"
                )
                updated = True
            else:
                new_blocks.append(block)
        if not updated:
            return
        new_blocks = self._apply_rotation(new_blocks)
        new_text = self._SEPARATOR.join(new_blocks)
        tmp_path = self._log_path.with_suffix(".tmp")
        tmp_path.write_text(new_text, encoding="utf-8")
        tmp_path.replace(self._log_path)

    def _apply_rotation(self, blocks: List[str]) -> List[str]:
        if not self._max_entries or self._max_entries <= 0:
            return blocks
        decisions = []
        for block in blocks:
            stripped = block.strip()
            if not stripped:
                decisions.append((block, False)); continue
            tag = stripped.splitlines()[0].strip()
            is_resolved = (
                tag.startswith("[") and tag.endswith("]")
                and not tag.endswith("| pending]")
            )
            decisions.append((block, is_resolved))
        resolved = sum(1 for _, r in decisions if r)
        if resolved <= self._max_entries:
            return blocks
        to_drop = resolved - self._max_entries
        kept = []
        for block, is_resolved in decisions:
            if is_resolved and to_drop > 0:
                to_drop -= 1; continue
            kept.append(block)
        return kept

    def _parse_entry(self, raw: str) -> Optional[dict]:
        lines = raw.strip().splitlines()
        if not lines:
            return None
        tag = lines[0].strip()
        if not (tag.startswith("[") and tag.endswith("]")):
            return None
        fields = [f.strip() for f in tag[1:-1].split("|")]
        if len(fields) < 4:
            return None
        e = {
            "date": fields[0], "ticker": fields[1], "rating": fields[2],
            "pending": fields[3] == "pending",
            "raw": fields[3] if fields[3] != "pending" else None,
            "alpha": fields[4] if len(fields) > 4 else None,
            "holding": fields[5] if len(fields) > 5 else None,
        }
        body = "\n".join(lines[1:]).strip()
        dm = self._DECISION_RE.search(body)
        rm = self._REFLECTION_RE.search(body)
        e["decision"] = dm.group(1).strip() if dm else ""
        e["reflection"] = rm.group(1).strip() if rm else ""
        return e

    def _format_full(self, e: dict) -> str:
        raw = e["raw"] or "n/a"; alpha = e["alpha"] or "n/a"; holding = e["holding"] or "n/a"
        tag = f"[{e['date']} | {e['ticker']} | {e['rating']} | {raw} | {alpha} | {holding}]"
        parts = [tag, f"DECISION:\n{e['decision']}"]
        if e["reflection"]:
            parts.append(f"REFLECTION:\n{e['reflection']}")
        return "\n\n".join(parts)

    def _format_reflection_only(self, e: dict) -> str:
        tag = f"[{e['date']} | {e['ticker']} | {e['rating']} | {e['raw'] or 'n/a'}]"
        if e["reflection"]:
            return f"{tag}\n{e['reflection']}"
        text = e["decision"][:300]
        suffix = "..." if len(e["decision"]) > 300 else ""
        return f"{tag}\n{text}{suffix}"


def cmd_read(args, log: TradingMemoryLog) -> int:
    print(log.get_past_context(args.ticker, n_same=args.n_same, n_cross=args.n_cross))
    return 0


def cmd_list(args, log: TradingMemoryLog) -> int:
    entries = log.get_pending_entries() if args.pending else log.load_entries()
    for e in entries:
        suffix = " pending" if e.get("pending") else ""
        print(f"[{e['date']} | {e['ticker']} | {e['rating']}]{suffix}")
    return 0


def cmd_append(args, log: TradingMemoryLog) -> int:
    decision = Path(args.decision_file).read_text(encoding="utf-8")
    log.store_decision(args.ticker, args.trade_date, decision)
    return 0


def cmd_resolve(args, log: TradingMemoryLog) -> int:
    reflection = Path(args.reflection_file).read_text(encoding="utf-8")
    log.update_with_outcome(
        ticker=args.ticker, trade_date=args.trade_date,
        raw_return=args.raw_return, alpha_return=args.alpha_return,
        holding_days=args.holding_days, reflection=reflection,
    )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="TradingAgents memory log CLI.")
    p.add_argument("--log-path", default=DEFAULT_LOG)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("read")
    r.add_argument("--ticker", required=True)
    r.add_argument("--n-same", type=int, default=5)
    r.add_argument("--n-cross", type=int, default=3)
    r.set_defaults(func=cmd_read)

    ls = sub.add_parser("list")
    ls.add_argument("--pending", action="store_true")
    ls.set_defaults(func=cmd_list)

    ap = sub.add_parser("append")
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--trade-date", required=True)
    ap.add_argument("--decision-file", required=True)
    ap.set_defaults(func=cmd_append)

    rs = sub.add_parser("resolve")
    rs.add_argument("--ticker", required=True)
    rs.add_argument("--trade-date", required=True)
    rs.add_argument("--raw-return", type=float, required=True)
    rs.add_argument("--alpha-return", type=float, required=True)
    rs.add_argument("--holding-days", type=int, required=True)
    rs.add_argument("--reflection-file", required=True)
    rs.set_defaults(func=cmd_resolve)

    args = p.parse_args()
    log = TradingMemoryLog(args.log_path)
    return args.func(args, log)


if __name__ == "__main__":
    sys.exit(main())
