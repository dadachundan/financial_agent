"""Skill-local SEC filing extractor.

We import only the *primitives* from ``ingest.graphiti_ingest``:

  * ``_clean_html_to_text`` — generic HTML → clean text utility
  * ``_sec_offsets`` — regex offset finder
  * the ``_10K_PATTERNS`` / ``_10Q_PATTERNS`` / ``_8K_PATTERNS`` dicts

and do our own **assembly**. The reasons for not calling
``extract_html_text`` directly:

1. It caps every section at 12,000 chars (``_MAX_SECTION``). That's the
   right tradeoff for graphiti's token budget but too small for a
   multi-year summary where the *changes* in Item 1A / MD&A across
   filings are the whole story.
2. Its 10-K assembly extracts only Item 1 (Business) + Item 1A (Risk
   Factors) — it skips **Item 7 (MD&A)**, which is exactly where
   management explains revenue mix, segment shifts, and capital
   allocation. For "summarize what changed", Item 7 is the most
   information-dense section in a 10-K.

Public API:

    text = extract(path, form_type, max_section=30_000, deep=False)

* ``max_section`` — per-section cap. Default 30,000 chars (~7.5k tokens
  per section, comfortable for in-context reading).
* ``deep=True`` — disable the cap entirely. Use for deep multi-year
  risk-factor evolution analysis where every change in language matters.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/x/projects/financial_agent")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingest.graphiti_ingest import (  # type: ignore  # noqa: E402
    _clean_html_to_text,
    _sec_offsets,
    _last_offset,
    _first_after_offset,
    _10K_PATTERNS,
    _10Q_PATTERNS,
    _8K_PATTERNS,
)


DEFAULT_MAX_SECTION = 30_000


def _slice(full: str, start: int, end: int | None, cap: int) -> str:
    chunk = full[start: end if end is not None else len(full)].strip()
    if cap and len(chunk) > cap:
        chunk = chunk[:cap] + "\n\n[…section truncated…]"
    return chunk


# Use graphiti's offset helpers — both accept ``full_text`` and filter out
# matches that aren't at the start of a line, so cross-references like
# "see Part I, Item 2, MD&A" buried inside paragraphs don't get picked up
# as section anchors.
def _last(offs: dict, name: str, full: str) -> int | None:
    return _last_offset(offs, name, full_text=full)


def _first_after(offs: dict, name: str, after: int, full: str) -> int | None:
    return _first_after_offset(offs, name, after, full_text=full)


def _extract_10k(full: str, cap: int) -> list[str]:
    """10-K: Item 1 (Business) + Item 1A (Risk Factors) + Item 7 (MD&A).

    The MD&A — which graphiti's extractor skips — is where revenue mix,
    segment shifts, and capital-allocation discussion live.
    """
    offs = _sec_offsets(full, _10K_PATTERNS)
    out: list[str] = []

    s1 = _last(offs, "item1", full)
    if s1 is not None:
        e1 = (_first_after(offs, "item1a", s1, full)
              or _first_after(offs, "item2", s1, full))
        chunk = _slice(full, s1, e1, cap)
        if len(chunk) > 300:
            out.append(f"=== ITEM 1: BUSINESS ===\n{chunk}")

    s1a = _first_after(offs, "item1a", s1 or 0, full)
    if s1a is not None:
        e1a = (_first_after(offs, "item2",  s1a, full)
               or _first_after(offs, "item3",  s1a, full)
               or _first_after(offs, "item7",  s1a, full))
        chunk = _slice(full, s1a, e1a, cap)
        if len(chunk) > 300:
            out.append(f"=== ITEM 1A: RISK FACTORS ===\n{chunk}")

    s7 = _last(offs, "item7", full)
    if s7 is not None:
        e7 = (_first_after(offs, "item7a", s7, full)
              or _first_after(offs, "item8", s7, full))
        chunk = _slice(full, s7, e7, cap)
        if len(chunk) > 300:
            out.append(f"=== ITEM 7: MD&A ===\n{chunk}")

    return out


def _extract_10q(full: str, cap: int) -> list[str]:
    """10-Q: Item 2 (MD&A) + Item 1A Part II (Risk Factors update)."""
    offs = _sec_offsets(full, _10Q_PATTERNS)
    out: list[str] = []

    s_mda = _last(offs, "item2_mda", full)
    if s_mda is not None:
        e_mda = (_first_after(offs, "item3_mkt", s_mda, full)
                 or _first_after(offs, "item4", s_mda, full))
        chunk = _slice(full, s_mda, e_mda, cap)
        # Strip forward-looking "CAUTIONARY STATEMENT" boilerplate
        chunk = re.sub(
            r"CAUTIONARY STATEMENT[^\n]*\n[\s\S]*?"
            r"(?=\n[A-Z][A-Z][A-Z\s\-]+(?:\n|$))",
            "",
            chunk,
            flags=re.IGNORECASE,
        ).strip()
        if len(chunk) > 300:
            out.append(f"=== ITEM 2: MD&A ===\n{chunk}")

    s_rf = _first_after(offs, "item1a", s_mda or 0, full)
    if s_rf is not None:
        chunk = _slice(full, s_rf, None, cap)
        if len(chunk) > 300:
            out.append(f"=== ITEM 1A: RISK FACTORS (UPDATE) ===\n{chunk}")

    return out


_8K_LABELS = {
    "item1_01": "ITEM 1.01: MATERIAL AGREEMENT",
    "item2_01": "ITEM 2.01: COMPLETION OF ACQUISITION",
    "item2_02": "ITEM 2.02: RESULTS OF OPERATIONS",
    "item8_01": "ITEM 8.01: OTHER EVENTS",
}


def _extract_8k(full: str, cap: int) -> list[str]:
    """8-K: substantive items (skip 5.02 officer changes, 7.01 Reg FD)."""
    offs = _sec_offsets(full, _8K_PATTERNS)
    starts: list[tuple[int, str]] = []
    for key in _8K_PATTERNS:
        for off in offs.get(key) or []:
            starts.append((off, key))
    starts.sort()
    out: list[str] = []
    for i, (off, key) in enumerate(starts):
        if key not in _8K_LABELS:
            continue
        end = starts[i + 1][0] if i + 1 < len(starts) else None
        chunk = _slice(full, off, end, cap)
        if len(chunk) > 200:
            out.append(f"=== {_8K_LABELS[key]} ===\n{chunk}")
    return out


def extract(
    path: Path,
    form_type: str = "10-K",
    *,
    max_section: int = DEFAULT_MAX_SECTION,
    deep: bool = False,
) -> str:
    """Extract clean narrative text from a SEC filing.

    Args:
        path: filing on disk (.htm/.html/.txt).
        form_type: "10-K", "10-Q", "8-K" (case-insensitive; /A variants OK).
        max_section: cap per extracted section (default 30k). Ignored when
            ``deep=True``.
        deep: when True, do not truncate any section — return the full
            Item 1 / 1A / 7 / MD&A text. Use for cross-year risk-factor
            evolution analysis.

    Returns:
        The assembled text. Sections are separated by blank lines and
        labelled with ``=== ITEM X: NAME ===`` headers.
    """
    full = _clean_html_to_text(path)
    if len(full) < 200:
        return ""

    cap = 0 if deep else max(max_section, 0)
    ft  = (form_type or "").upper()

    if ft.startswith("10-K"):
        sections = _extract_10k(full, cap)
    elif ft.startswith("10-Q"):
        sections = _extract_10q(full, cap)
    elif ft.startswith("8-K"):
        sections = _extract_8k(full, cap)
    else:
        sections = _extract_10k(full, cap) or _extract_10q(full, cap)

    if sections:
        return "\n\n".join(sections)
    # Fallback: raw dump capped at 2× max_section (or unlimited in deep mode)
    return full if deep else full[: max_section * 2]
