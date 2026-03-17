"""
langfuse_monitor.py — Langfuse LLM call monitoring integration (v4 / OTel-native).

Provides a lightweight wrapper around the Langfuse Python SDK (v4+) so that every
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
  Session: "ingest YYYY-MM-DD HH:MM <doc label>"  (one session per document)
    └── Trace: "<document-label>"  (root span for the document)
          ├── Generation: "ExtractedEntities"   (entity extraction LLM call)
          ├── Generation: "ExtractedEdges"      (edge extraction LLM call)
          ├── Generation: "NodeResolutions"     (dedup LLM call, if needed)
          ├── Generation: "EdgeDuplicate"       (per-edge dedup, N calls)
          └── Generation: "SummarizedEntities"  (node summary, batched)

How context propagation works (Langfuse v4 / OTel):
  set_document() creates a root span and calls opentelemetry.context.attach() to
  make it the *current* OTel span.  All subsequent start_observation() calls
  (including those from parallel asyncio.gather tasks or run_in_executor threads)
  automatically inherit this parent span because OTel propagates via Python
  contextvars, which asyncio copies to every new task.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

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
    """Create a Langfuse root span for one document and attach it to the OTel context.

    Call before add_episode(); pass the returned token to clear_document() afterwards.
    Returns None when Langfuse is disabled (clear_document handles None gracefully).

    In Langfuse v4 (OTel-native), child generations are linked to this span
    automatically via opentelemetry.context.attach() — no manual TraceContext needed.
    Each document gets its own Langfuse session named:
        "ingest YYYY-MM-DD HH:MM <document label>"
    """
    global _session_id

    if not _enabled or _lf is None:
        return None

    try:
        _session_id = f"{_base_label} {label}"

        # Create root span for this document (no trace_context → new root trace)
        span = _lf.start_observation(name=label, as_type="span")

        # ── Langfuse v4: attach span into the OTel current context ──────────
        # This is the critical step.  Without it, child observations created
        # in coroutines / thread-pool tasks have no parent and appear as
        # orphaned top-level traces in the UI.
        try:
            from opentelemetry import context as _otel_ctx, trace as _otel_trace
            from opentelemetry.context import attach as _otel_attach
            _otel_token = _otel_attach(
                _otel_trace.set_span_in_context(span._otel_span)
            )
        except Exception as e:
            logger.debug("OTel attach failed (non-fatal): %s", e)
            _otel_token = None

        # Tag with session id so Langfuse groups this trace under the named session
        try:
            span._otel_span.set_attribute("session.id", _session_id)
        except Exception:
            pass

        print(f"  📊 Langfuse trace started → session: {_session_id!r}", flush=True)
        return (span, _otel_token)

    except Exception as e:
        logger.warning("Langfuse set_document failed: %s", e)
        return None


def clear_document(token) -> None:
    """End the document span and detach OTel context.  Safe to call with token=None."""
    if not _enabled or _lf is None or token is None:
        return

    try:
        span, otel_token = token
        if span is not None:
            span.end()
        if otel_token is not None:
            try:
                from opentelemetry.context import detach as _otel_detach
                _otel_detach(otel_token)
            except Exception as e:
                logger.debug("OTel detach failed (non-fatal): %s", e)
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
    In Langfuse v4, OTel context propagation automatically nests this generation
    under whichever span was attach()ed by set_document() — no TraceContext needed.
    """
    if not _enabled or _lf is None:
        return

    try:
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

        # No trace_context argument — OTel context propagation links this generation
        # to the parent span set by set_document() → attach() automatically.
        gen = _lf.start_observation(
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
        logger.warning("Langfuse log_generation failed: %s", e)


def flush() -> None:
    """Flush buffered traces — call after each document or at end of session."""
    if _enabled and _lf is not None:
        try:
            _lf.flush()
        except Exception as e:
            logger.debug("Langfuse flush failed: %s", e)
