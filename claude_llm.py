"""
claude_llm.py — Shared Anthropic Claude API client.

Configuration (priority order):
  1. Explicit ``api_key`` / ``base_url`` arguments
  2. ``ANTHROPIC_AUTH_TOKEN`` + ``ANTHROPIC_BASE_URL`` env vars (user's zshrc proxy)
  3. ``ANTHROPIC_API_KEY`` env var (native Anthropic)
  4. ``ANTHROPIC_API_KEY`` defined in ``config.py``

Usage:
    from claude_llm import call_claude, CLAUDE_MODEL

    text, elapsed, raw_json = call_claude(
        messages=[
            {"role": "system", "content": "You are ..."},
            {"role": "user",   "content": "..."},
        ],
        temperature=0.3,
        max_completion_tokens=1000,
    )

Notes:
- ``role: "system"`` messages are collapsed into the Anthropic SDK's top-level
  ``system`` parameter. ``user`` / ``assistant`` messages pass through.
- The default model is :data:`CLAUDE_MODEL` (Sonnet 4.6) — fast, cheap, and
  strong enough for entity / relationship extraction and one-shot
  summarisation. Override per-call with ``model=`` if needed.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

import anthropic

# Latest Claude model family (claude-opus-4-8 / claude-sonnet-4-6 / claude-haiku-4-5-20251001).
# Sonnet is the default — best quality/cost balance for batch extraction.
CLAUDE_MODEL: str = "claude-sonnet-4-6"


# ── Load ANTHROPIC_API_KEY from config.py (walk up until found) ───────────────
def _find_project_root() -> Path | None:
    script_dir = Path(__file__).parent
    for parent in [script_dir, *script_dir.parents]:
        if (parent / "config.py").exists():
            return parent
    return None


ANTHROPIC_API_KEY: str = ""
project_root = _find_project_root()
if project_root and str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
try:
    from config import ANTHROPIC_API_KEY  # type: ignore
except ImportError:
    pass


def _resolve_key(explicit: str | None) -> str:
    if explicit:
        return explicit
    return (
        os.environ.get("ANTHROPIC_AUTH_TOKEN")
        or os.environ.get("ANTHROPIC_API_KEY")
        or ANTHROPIC_API_KEY
        or ""
    )


def _split_messages(messages: list[dict]) -> tuple[str, list[dict]]:
    """Pull all ``system`` messages out of ``messages`` and join them.

    Anthropic's API takes ``system`` as a separate top-level parameter, not as
    a message with ``role=system``. We also drop any legacy ``name`` field.
    """
    system_parts: list[str] = []
    chat_messages: list[dict] = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if not isinstance(content, str):
            content = str(content)
        if role == "system":
            if content:
                system_parts.append(content)
            continue
        # Anthropic only accepts user / assistant.
        if role not in ("user", "assistant"):
            role = "user"
        chat_messages.append({"role": role, "content": content})

    if not chat_messages:
        # Anthropic requires at least one user message.
        chat_messages = [{"role": "user", "content": ""}]

    return ("\n\n".join(system_parts), chat_messages)


def call_claude(
    messages: list[dict],
    temperature: float = 0.3,
    max_completion_tokens: int = 1000,
    retries: int = 3,
    api_key: str = "",
    model: str = "",
    base_url: str = "",
) -> tuple[str, float, str]:
    """Call the Anthropic Claude messages API.

    Returns ``(text, elapsed_seconds, raw_json)``.

    Args:
        messages: Chat messages. ``role: "system"`` entries are folded into the
            Anthropic top-level ``system`` parameter.
        temperature: Sampling temperature.
        max_completion_tokens: Maximum tokens in the response.
        retries: Retry attempts on transient API failures.
        api_key: Override the key from env / config.py.
        model: Override :data:`CLAUDE_MODEL`.
        base_url: Override the Anthropic base URL (defaults to env / SDK default).
    """
    key = _resolve_key(api_key)
    if not key:
        raise ValueError(
            "ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY not set. "
            "Export it in your shell or add ANTHROPIC_API_KEY to config.py."
        )

    client_kwargs: dict[str, Any] = {"api_key": key}
    bu = base_url or os.environ.get("ANTHROPIC_BASE_URL")
    if bu:
        client_kwargs["base_url"] = bu
    client = anthropic.Anthropic(**client_kwargs)

    system_text, chat_messages = _split_messages(messages)
    used_model = model or CLAUDE_MODEL

    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            t0 = time.monotonic()
            create_kwargs: dict[str, Any] = {
                "model":       used_model,
                "messages":    chat_messages,
                "max_tokens":  max(1, min(max_completion_tokens, 8192)),
                "temperature": max(0.0, min(temperature, 1.0)),
            }
            if system_text:
                create_kwargs["system"] = system_text
            resp = client.messages.create(**create_kwargs)
            elapsed = time.monotonic() - t0
            # Concatenate text blocks (Claude responses can be a list of blocks).
            text_parts: list[str] = []
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    text_parts.append(block.text)
            text = "".join(text_parts)
            try:
                raw_json = resp.model_dump_json()
            except Exception:
                raw_json = ""
            return text, elapsed, raw_json
        except Exception as e:
            last_exc = e
            wait = 3 * (attempt + 1)
            print(
                f"  Claude error (attempt {attempt+1}/{retries}): {e}, "
                f"retrying in {wait}s...",
                flush=True,
            )
            time.sleep(wait)

    raise RuntimeError(
        f"Claude API failed after {retries} retries: {last_exc}"
    ) from last_exc
