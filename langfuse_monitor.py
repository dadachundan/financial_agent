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
  Session: "ingest-<label>-<timestamp>"  (groups all document traces)
    └── Trace: "<document-label>"  (one per document; root span)
          ├── Generation: "ExtractedEntities"  (entity extraction LLM call)
          ├── Generation: "ExtractedEdges"     (edge extraction LLM call)
          └── Generation: "NodeResolutions"    (dedup LLM call)
"""

from __future__ import annotations

import contextvars
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── Context vars (survive async/thread hops within a single ingest run) ────────
_current_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "langfuse_trace_id", default=None
)
_current_span_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "langfuse_span_id", default=None
)
_current_span: contextvars.ContextVar[Any | None] = contextvars.ContextVar(
    "langfuse_span", default=None
)

# ── Module-level state ─────────────────────────────────────────────────────────
_lf: "Langfuse | None" = None  # singleton Langfuse client
_session_id: str = ""          # current document's session id
_base_label: str = ""          # "ingest YYYY-MM-DD HH:MM" set at init
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
    global _lf, _session_id, _base_label, _enabled

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
        # base label is reused as the prefix for every per-document session id
        _base_label = session_label or "ingest"
        _session_id = _base_label  # overwritten per document in set_document()
        _enabled = True
        logger.info(
            "Langfuse monitoring enabled → %s  base=%s", cfg["host"], _base_label
        )
        print(
            f"  📊 Langfuse monitoring enabled → {cfg['host']}  base={_base_label}",
            flush=True,
        )
        return True
    except Exception as e:
        logger.warning("Langfuse init failed: %s", e)
        return False


def is_enabled() -> bool:
    return _enabled


# ── Document context ───────────────────────────────────────────────────────────

def set_document(label: str):
    """Create a Langfuse trace+root-span for one document.

    Call before add_episode(); pass the returned token to clear_document() afterwards.
    When Langfuse is disabled, returns None (clear_document handles None gracefully).
    Each document gets its own Langfuse session named:
        "ingest YYYY-MM-DD HH:MM <document label>"
    """
    global _session_id

    if not _enabled or _lf is None:
        return None

    try:
        # Build a per-document session id so Langfuse shows a readable session name.
        _session_id = f"{_base_label} {label}"

        # start_observation without trace_context creates a new root span → new Langfuse trace
        span = _lf.start_observation(name=label, as_type="span")

        # Tag the span with our session_id so it appears under the named session.
        # "session.id" is the OTel attribute Langfuse uses to attach spans to sessions.
        try:
            span._otel_span.set_attribute("session.id", _session_id)
        except Exception:
            pass  # defensive: don't fail if internal API changes

        t1 = _current_trace_id.set(span.trace_id)
        t2 = _current_span_id.set(span.id)
        t3 = _current_span.set(span)
        return (t1, t2, t3)
    except Exception as e:
        logger.debug("Langfuse set_document failed: %s", e)
        return None


def clear_document(token) -> None:
    """End the document span and reset context vars.  Safe to call with token=None."""
    if not _enabled or _lf is None or token is None:
        return

    try:
        t1, t2, t3 = token
        span = _current_span.get()
        if span is not None:
            span.end()
        _current_trace_id.reset(t1)
        _current_span_id.reset(t2)
        _current_span.reset(t3)
    except Exception as e:
        logger.debug("Langfuse clear_document failed: %s", e)


# ── Generation logging ─────────────────────────────────────────────────────────

def log_generation(
    call_type: str,
    model: str,
    messages: list[dict],
    response_text: str,
    elapsed_s: float,
    usage: dict | None = None,
) -> None:
    """Log a single LLM generation to Langfuse as a child of the current document span.

    Called from minimax_llm_client._generate_response() after each LLM call.
    Automatically nests under the active document trace set by set_document().
    """
    if not _enabled or _lf is None:
        return

    try:
        trace_id = _current_trace_id.get()
        span_id = _current_span_id.get()

        # Build TraceContext to nest generation under the document span
        trace_ctx = None
        if trace_id:
            from langfuse.types import TraceContext
            trace_ctx = TraceContext(trace_id=trace_id, parent_span_id=span_id)

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

        gen = _lf.start_observation(
            trace_context=trace_ctx,
            name=call_type,
            as_type="generation",
            input=lf_input,
            output=response_text[:8000] if response_text else "",
            model=model,
            model_parameters={"elapsed_s": round(elapsed_s, 2)},
            usage_details=usage_details or None,
            metadata={"session": _session_id},
        )
        gen.end()

    except Exception as e:
        logger.debug("Langfuse log_generation failed: %s", e)


def flush() -> None:
    """Flush buffered traces — call after each document or at end of session."""
    if _enabled and _lf is not None:
        try:
            _lf.flush()
        except Exception as e:
            logger.debug("Langfuse flush failed: %s", e)
