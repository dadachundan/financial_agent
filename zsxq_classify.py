"""
zsxq_classify.py — Shared classification helpers for the zsxq PDF pipeline.

Public API
----------
  classify_with_minimax(name, summary, api_key, retries=3)
      Raw LLM call → parses 4 category flags + tickers + analysis.

  classify_one(conn, file_id, name, summary, api_key,
               local_path=None, retries=3)
      classify_with_minimax + persist UPDATE to pdf_files in one shot.
      Returns a result dict (see docstring).

Used by:
  zsxq_downloader.py  — classify each PDF immediately after download
  zsxq_index.py       — batch classify / re-classify from the DB
"""

import sqlite3
from datetime import datetime

from minimax import call_minimax  # type: ignore

# ── Prompt constants ───────────────────────────────────────────────────────────

CLASSIFY_SYSTEM = (
    "You are a financial research analyst. Given a research report summary, classify it "
    "across four categories and extract tickers.\n\n"
    "Respond in exactly this format (one item per line, nothing else):\n"
    "  AI: Yes or No\n"
    "  Robotics: Yes or No\n"
    "  Semiconductor: Yes or No\n"
    "  Energy: Yes or No\n"
    "  Tickers: TICK1, TICK2, ...  (or Tickers: None)\n"
    "  Analysis: <2-3 sentence summary of the report's focus>\n\n"
    "Definitions:\n"
    "- AI: artificial intelligence, machine learning, large language models, "
    "generative AI, AI chips, AI software/services.\n"
    "- Robotics: humanoid robots, industrial robots, autonomous vehicles, drones.\n"
    "- Semiconductor: chips, fabs, EDA tools, memory, wafers, packaging.\n"
    "- Energy: oil & gas, renewables, power grids, batteries, nuclear, energy storage.\n"
    "Tickers: A-share 6-digit codes, HK codes, US symbols explicitly referenced only."
)

CLASSIFY_USER_TMPL = """\
Report filename: {name}

Summary (Chinese):
{summary}

Classify this report across all four categories and extract tickers.
"""


# ── Parsing helpers ────────────────────────────────────────────────────────────

def _parse_yes_no(text: str, label: str) -> bool | None:
    """Find 'Label: Yes/No' in text; return True/False/None."""
    for line in text.splitlines():
        ls = line.strip().lower()
        if ls.startswith(f"{label.lower()}:"):
            val = ls.split(":", 1)[1].strip()
            if val.startswith("yes"):
                return True
            if val.startswith("no"):
                return False
    return None


# ── Core classification call ───────────────────────────────────────────────────

def classify_with_minimax(
    name: str,
    summary: str,
    api_key: str,
    retries: int = 3,
) -> tuple[str, bool | None, bool | None, bool | None, bool | None, str, float, str, str]:
    """Call MiniMax to classify a PDF across 4 categories and extract tickers.

    Returns:
        (analysis, ai_rel, robotics_rel, semiconductor_rel, energy_rel,
         tickers, elapsed_seconds, prompt_sent, raw_json)
    """
    user_msg = CLASSIFY_USER_TMPL.format(
        name=name,
        summary=summary.strip() if summary else "(no summary available)",
    )
    text, elapsed, raw_json = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": CLASSIFY_SYSTEM},
            {"role": "user",   "name": "User",       "content": user_msg},
        ],
        temperature=0.1,
        max_completion_tokens=300,
        retries=retries,
        api_key=api_key,
    )

    ai_rel   = _parse_yes_no(text, "AI")
    rob_rel  = _parse_yes_no(text, "Robotics")
    semi_rel = _parse_yes_no(text, "Semiconductor")
    nrg_rel  = _parse_yes_no(text, "Energy")

    if any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel]) and text:
        print(f"    ⚠ Could not parse all categories. Raw reply:\n{text}")

    tickers = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("tickers:"):
            raw_t = ls[len("tickers:"):].strip()
            if raw_t.lower() not in ("none", "n/a", ""):
                tickers = raw_t
            break

    analysis = ""
    for line in text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("analysis:"):
            analysis = ls[len("analysis:"):].strip()
            break
    if not analysis:
        analysis = text  # fallback: store the full response

    return analysis, ai_rel, rob_rel, semi_rel, nrg_rel, tickers, elapsed, user_msg, raw_json


# ── classify_one: classify + persist in one call ──────────────────────────────

def classify_one(
    conn: sqlite3.Connection,
    file_id: int,
    name: str,
    summary: str,
    api_key: str,
    local_path: str | None = None,
    retries: int = 3,
) -> dict:
    """Classify a single PDF and persist results to pdf_files.

    Args:
        conn:       Open SQLite connection (zsxq.db).
        file_id:    Primary key in pdf_files.
        name:       PDF filename (used in the prompt).
        summary:    Chinese summary text from the zsxq topic.
        api_key:    MiniMax API key.
        local_path: If provided, stored in pdf_files.local_path (COALESCE).
        retries:    API retries on transient failures.

    Returns a dict with:
        ai, robotics, semiconductor, energy  — bool
        tickers                              — str (may be empty)
        analysis                             — str
        elapsed                              — float (seconds)
        parse_error                          — bool (True if any field unparseable)
    """
    (analysis, ai_rel, rob_rel, semi_rel, nrg_rel,
     tickers, elapsed, prompt, raw_json) = classify_with_minimax(
        name, summary, api_key, retries=retries,
    )

    parse_error = any(v is None for v in [ai_rel, rob_rel, semi_rel, nrg_rel])

    conn.execute(
        """UPDATE pdf_files
               SET ai_related            = ?,
                   robotics_related      = ?,
                   semiconductor_related = ?,
                   energy_related        = ?,
                   tickers               = COALESCE(?, tickers),
                   categories_analysis   = ?,
                   categories_prompt     = ?,
                   categories_raw        = ?,
                   local_path            = COALESCE(?, local_path),
                   indexed_at            = ?
             WHERE file_id = ?""",
        (
            1 if ai_rel   is True else (0 if ai_rel   is False else None),
            1 if rob_rel  is True else (0 if rob_rel  is False else None),
            1 if semi_rel is True else (0 if semi_rel is False else None),
            1 if nrg_rel  is True else (0 if nrg_rel  is False else None),
            tickers or None,
            analysis, prompt, raw_json,
            local_path,
            datetime.now().isoformat(),
            file_id,
        ),
    )
    conn.commit()

    return {
        "ai":            bool(ai_rel),
        "robotics":      bool(rob_rel),
        "semiconductor": bool(semi_rel),
        "energy":        bool(nrg_rel),
        "tickers":       tickers,
        "analysis":      analysis,
        "elapsed":       elapsed,
        "parse_error":   parse_error,
    }
