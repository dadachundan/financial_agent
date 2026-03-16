"""
langfuse_monitor.py — Langfuse LLM call monitoring integration.

Provides a lightweight wrapper around the Langfuse Python SDK so that every
MiniMax LLM call is traced and visible in the Langfuse UI.

Setup (one-time):
  Option A — Langfuse Cloud (free):
    1. Sign up at https://cloud.langfuse.com
    2. Settings → API Keys → create a key pair
    3. Add to config.py:
         LANGFUSE_PUBLIC_KEY = "pk-lf-..."
         LANGFUSE_SECRET_KEY = "sk-lf-..."

  Option B — Self-hosted (Docker):
    docker run --rm -p 3000:3000 -e TELEMETRY_ENABLED=false langfuse/langfuse
    Then add to config.py:
         LANGFUSE_PUBLIC_KEY = "..."
         LANGFUSE_SECRET_KEY = "..."
         LANGFUSE_HOST = "http://localhost:3000"

After setup, run graphiti_ingest.py normally; traces appear in the UI automatically.

Trace hierarchy produced per ingest run:
  Trace: "<session-label>"  (one per ingest run)
    └── Span: "<document-label>"  (one per document)
          ├── Generation: "ExtractedEntities"  (entity extraction LLM call)
          ├── Generation: "ExtractedEdges"     (edge extraction LLM call)
          └── Generation: "NodeResolutions"    (dedup LLM call)
"""

from __future__ import annotations

import contextvars
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── Context vars (survive async/thread hops within a single ingest run) ────────
# Set by graphiti_ingest.py before each add_episode() call.
_current_doc_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "langfuse_current_doc", default=None
)

# ── Module-level state ─────────────────────────────────────────────────────────
_lf: "Langfuse | None" = None  # singleton Langfuse client
_session_label: str = ""
_enabled: bool = False


def _load_config() -> dict:
    """Load LANGFUSE_* keys from config.py (walk up from this file)."""
    for parent in [Path(__file__).parent, *Path(__file__).parent.parents]:
        cfg = parent / "config.py"
        if cfg.exists():
            ns: dict = {}
            try:
                exec(cfg.read_text(), ns)
            except Exception:
                pass
            if ns.get("LANGFUSE_PUBLIC_KEY") or ns.get("LANGFUSE_SECRET_KEY"):
                return {
                    "public_key": ns.get("LANGFUSE_PUBLIC_KEY", ""),
                    "secret_key": ns.get("LANGFUSE_SECRET_KEY", ""),
                    "host": ns.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
                }
    return {}


def init(session_label: str = "") -> bool:
    """Initialise Langfuse from config.py.  Returns True if enabled."""
    global _lf, _session_label, _enabled

    cfg = _load_config()
    if not cfg.get("public_key") or not cfg.get("secret_key"):
        return False

    try:
        from langfuse import Langfuse

        _lf = Langfuse(
            public_key=cfg["public_key"],
            secret_key=cfg["secret_key"],
            host=cfg["host"],
        )
        _session_label = session_label or "ingest"
        _enabled = True
        logger.info("Langfuse monitoring enabled → %s", cfg["host"])
        print(f"  📊 Langfuse monitoring enabled → {cfg['host']}", flush=True)
        return True
    except Exception as e:
        logger.warning("Langfuse init failed: %s", e)
        return False


def is_enabled() -> bool:
    return _enabled


# ── Context helpers ────────────────────────────────────────────────────────────

def set_document(label: str) -> contextvars.Token:
    """Call before add_episode(); returns a token to reset with clear_document()."""
    return _current_doc_ctx.set(label)


def clear_document(token: contextvars.Token) -> None:
    _current_doc_ctx.reset(token)


# ── Generation logging ─────────────────────────────────────────────────────────

def log_generation(
    call_type: str,
    model: str,
    messages: list[dict],
    response_text: str,
    elapsed_s: float,
    usage: dict | None = None,
) -> None:
    """Log a single LLM generation to Langfuse.

    Called from minimax_llm_client._generate_response() after each LLM call.
    Groups calls under the current document span automatically.
    """
    if not _enabled or _lf is None:
        return

    try:
        doc_label = _current_doc_ctx.get()

        # Build input list in Langfuse's chat format
        lf_input = [
            {"role": m.get("role", "user"), "content": str(m.get("content", ""))[:8000]}
            for m in messages
        ]

        usage_details: dict[str, int] = {}
        if usage:
            usage_details = {
                "input": usage.get("prompt_tokens", 0),
                "output": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            }

        observation = _lf.start_observation(
            name=call_type,
            as_type="generation",
            input=lf_input,
            output=response_text[:8000] if response_text else "",
            model=model,
            model_parameters={"elapsed_s": round(elapsed_s, 2)},
            usage_details=usage_details or None,
            metadata={"document": doc_label, "session": _session_label},
        )
        observation.end()

    except Exception as e:
        logger.debug("Langfuse log_generation failed: %s", e)


def flush() -> None:
    """Flush buffered traces — call after each document or at end of session."""
    if _enabled and _lf is not None:
        try:
            _lf.flush()
        except Exception as e:
            logger.debug("Langfuse flush failed: %s", e)
