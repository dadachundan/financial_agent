"""
minimax.py — Shared MiniMax API client.

Usage:
    from minimax import call_minimax, MINIMAX_API_KEY

    text, elapsed, raw_json = call_minimax(
        messages=[
            {"role": "system", "name": "MiniMax AI", "content": "You are ..."},
            {"role": "user",   "name": "User",       "content": "..."},
        ],
        temperature=0.3,
        max_completion_tokens=1000,
    )
"""

import sys
import time
from pathlib import Path

import requests

MINIMAX_API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"
MINIMAX_MODEL   = "MiniMax-Text-01"

# ── Load MINIMAX_API_KEY from config.py (walk up until found) ─────────────────
def _find_project_root() -> Path | None:
    script_dir = Path(__file__).parent
    for parent in [script_dir, *script_dir.parents]:
        if (parent / "config.py").exists():
            return parent
    return None

MINIMAX_API_KEY: str = ""
project_root = _find_project_root()
if project_root and str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
try:
    from config import MINIMAX_API_KEY  # type: ignore
except ImportError:
    pass


def call_minimax(
    messages: list[dict],
    temperature: float = 0.3,
    max_completion_tokens: int = 1000,
    retries: int = 3,
    api_key: str = "",
) -> tuple[str, float, str]:
    """Call the MiniMax chat API and return (text, elapsed_seconds, raw_json).

    Args:
        messages: List of message dicts with 'role', 'name', and 'content'.
        temperature: Sampling temperature.
        max_completion_tokens: Maximum tokens in the response.
        retries: Number of retry attempts on failure.
        api_key: Override the key loaded from config.py.

    Returns:
        (text, elapsed, raw_json) — empty strings on total failure.
    """
    key = api_key or MINIMAX_API_KEY
    if not key:
        raise ValueError(
            f"MINIMAX_API_KEY not set. Add it to config.py "
            f"(looked in: {project_root or 'not found'})"
        )

    payload = {
        "model": MINIMAX_MODEL,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }

    for attempt in range(retries):
        try:
            t0 = time.monotonic()
            resp = requests.post(MINIMAX_API_URL, json=payload, headers=headers, timeout=60)
            elapsed = time.monotonic() - t0
            resp.raise_for_status()
            raw_json = resp.text
            data = resp.json()
            text = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
            )
            return text, elapsed, raw_json
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f"  MiniMax error (attempt {attempt+1}/{retries}): {e}, "
                  f"retrying in {wait}s...")
            time.sleep(wait)

    return "", 0.0, ""
