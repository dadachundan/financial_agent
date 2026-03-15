"""
minimax_llm_client.py — MiniMax LLM client + bge-m3 embedder for graphiti-core.

Wires the project's existing MiniMax API and the local bge-m3 SentenceTransformer
model into graphiti-core's abstract interfaces so the full knowledge-graph pipeline
runs entirely locally, with no external cloud graph service.

Usage (from other modules):
    from minimax_llm_client import MiniMaxLLMClient, BGEEmbedder, get_graphiti
    graphiti = get_graphiti()          # lazy singleton
"""

import asyncio
import json
import logging
import re
from pathlib import Path
from typing import Any

from graphiti_core.llm_client import LLMClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.client import EmbedderClient
from graphiti_core.cross_encoder.client import CrossEncoderClient

logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent
GRAPH_DIR  = SCRIPT_DIR / "graphiti_db"
GROUP_ID   = "financial-pdfs"


# ── Config helpers ─────────────────────────────────────────────────────────────

def _load_minimax_key() -> str:
    for parent in [SCRIPT_DIR] + list(SCRIPT_DIR.parents):
        cfg = parent / "config.py"
        if cfg.exists():
            ns: dict = {}
            exec(cfg.read_text(), ns)
            key = ns.get("MINIMAX_API_KEY", "")
            if key:
                return key
    return ""


# ── JSON extraction helper ─────────────────────────────────────────────────────

def _extract_json(text: str) -> str:
    """Strip markdown fences and return the outermost JSON object/array."""
    text = re.sub(r"```(?:json)?\s*\n?", "", text)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE).strip()
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = text.find(start_char)
        if start == -1:
            continue
        depth = 0
        for i, c in enumerate(text[start:], start):
            if c == start_char:
                depth += 1
            elif c == end_char:
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    return text


# ── LLM response normaliser ────────────────────────────────────────────────────

def _normalize_llm_json(parsed: Any, response_model: type) -> Any:
    """Fix common MiniMax JSON inconsistencies before Pydantic validation.

    Known issues:
    1. ExtractedEntity items use ``entity_id`` instead of ``entity_type_id``.
    2. The model sometimes echoes the JSON schema back (``$defs`` or top-level
       ``properties`` key) instead of generating data — return an empty valid
       envelope in that case.
    3. NodeResolutions items sometimes omit ``duplicate_name`` (required field).
    4. ExtractedEdges items use alternate field names
       (source/target, description/fact, relation/relation_type).
    """
    name = response_model.__name__

    # ── Schema echo: model returned its own JSON schema instead of data ──────
    _schema_echo = isinstance(parsed, dict) and (
        "$defs" in parsed
        or (
            "properties" in parsed
            and "entity_resolutions" not in parsed
            and "extracted_entities" not in parsed
            and "edges" not in parsed
        )
    )
    if _schema_echo:
        if name == "ExtractedEntities":
            return {"extracted_entities": []}
        if name == "ExtractedEdges":
            return {"edges": []}
        if name == "NodeResolutions":
            return {"entity_resolutions": []}
        return parsed  # unknown model — let Pydantic report the error

    # ── ExtractedEntities: entity_id → entity_type_id ────────────────────────
    if isinstance(parsed, dict) and "extracted_entities" in parsed:
        for item in parsed.get("extracted_entities") or []:
            if isinstance(item, dict) and "entity_id" in item and "entity_type_id" not in item:
                item["entity_type_id"] = item.pop("entity_id")

    # ── NodeResolutions: default missing duplicate_name to "" ────────────────
    if isinstance(parsed, dict) and "entity_resolutions" in parsed:
        clean = []
        for item in parsed.get("entity_resolutions") or []:
            if not isinstance(item, dict):
                continue
            # Skip schema-echo objects that slipped into the list
            if "properties" in item and "id" not in item:
                continue
            item.setdefault("duplicate_name", "")
            clean.append(item)
        parsed["entity_resolutions"] = clean

    # ── ExtractedEdges: normalise alternate field names ───────────────────────
    if isinstance(parsed, dict) and name == "ExtractedEdges":
        if parsed.get("edges") is None:
            parsed["edges"] = []
        for edge in parsed.get("edges") or []:
            if not isinstance(edge, dict):
                continue
            if "source_entity_name" not in edge:
                edge["source_entity_name"] = (
                    edge.pop("source", None)
                    or edge.pop("source_entity", None)
                    or ""
                )
            if "target_entity_name" not in edge:
                edge["target_entity_name"] = (
                    edge.pop("target", None)
                    or edge.pop("target_entity", None)
                    or ""
                )
            if "relation_type" not in edge:
                edge["relation_type"] = (
                    edge.pop("type", None)
                    or edge.pop("relation", None)
                    or edge.pop("relationship", None)
                    or ""
                )
            if "fact" not in edge:
                edge["fact"] = (
                    edge.pop("description", None)
                    or edge.pop("content", None)
                    or ""
                )

    return parsed


# ── MiniMax LLM client ─────────────────────────────────────────────────────────

class MiniMaxLLMClient(LLMClient):
    """
    Graphiti LLMClient backed by MiniMax.

    Structured extraction works by injecting the Pydantic model's JSON schema
    into the system prompt and parsing the model's JSON response.
    """

    MAX_RETRIES: int = 2

    def __init__(self, config: LLMConfig | None = None, cache: bool = False):
        if config is None:
            config = LLMConfig(
                api_key=_load_minimax_key(),
                model="MiniMax-Text-01",
                small_model="MiniMax-Text-01",
                max_tokens=8192,
            )
        super().__init__(config, cache)
        self._api_key = config.api_key or _load_minimax_key()

    async def _generate_response(
        self,
        messages: list,
        response_model: type | None = None,
        max_tokens: int = 8192,
        model_size=None,
    ) -> dict[str, Any]:
        from minimax import call_minimax

        mm_messages = []
        for m in messages:
            # Accept both Message objects and plain dicts
            if hasattr(m, "role"):
                role    = m.role
                content = m.content or ""
            else:
                role    = m.get("role", "user")
                content = m.get("content", "")

            # Inject JSON schema requirement into the system prompt
            if role == "system" and response_model is not None:
                schema = json.dumps(
                    response_model.model_json_schema(), ensure_ascii=False, indent=None
                )
                content = (
                    content
                    + "\n\nYou MUST reply with ONLY valid JSON (no markdown, no prose) "
                    "that matches this exact JSON schema:\n" + schema
                )
                mm_messages.append({
                    "role": "system", "name": "MiniMax AI", "content": content
                })
            elif role == "system":
                mm_messages.append({
                    "role": "system", "name": "MiniMax AI", "content": content
                })
            else:
                mm_messages.append({
                    "role": "user", "name": "User", "content": content
                })

        # Run the synchronous call_minimax in a thread so the event loop stays alive
        loop = asyncio.get_event_loop()
        text, _elapsed, _raw = await loop.run_in_executor(
            None,
            lambda: call_minimax(
                messages=mm_messages,
                temperature=max(self.temperature, 0.0),
                max_completion_tokens=min(max_tokens, 8192),
                api_key=self._api_key,
            ),
        )

        # Structured output path
        if response_model is not None:
            json_str = _extract_json(text)
            try:
                parsed    = json.loads(json_str)
                parsed    = _normalize_llm_json(parsed, response_model)
                validated = response_model.model_validate(parsed)
                return validated.model_dump()
            except Exception as exc:
                raise ValueError(
                    f"Structured response parse failed: {exc}\n"
                    f"Raw LLM output (first 500 chars): {text[:500]}"
                ) from exc

        # Plain-text path
        return {"content": text}

    # graphiti calls `generate_response` (the public wrapper) which handles retries
    # and multi-lingual instructions; it delegates to _generate_response above.


# ── bge-m3 Embedder ────────────────────────────────────────────────────────────

class BGEEmbedder(EmbedderClient):
    """
    Graphiti EmbedderClient using the local BAAI/bge-m3 SentenceTransformer model.

    The model is loaded once (class-level singleton) and encoding is run in a
    thread executor to avoid blocking the async event loop.
    """

    _model = None  # shared lazy instance

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading bge-m3 embedding model …")
            cls._model = SentenceTransformer("BAAI/bge-m3")
            logger.info("bge-m3 ready.")
        return cls._model

    async def create(self, input_data) -> list[float]:
        if isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, list):
            text = " ".join(str(x) for x in input_data)
        else:
            text = str(input_data)

        loop = asyncio.get_event_loop()
        vector: list[float] = await loop.run_in_executor(
            None,
            lambda: self._get_model()
                        .encode(text, normalize_embeddings=True)
                        .tolist(),
        )
        return vector

    async def create_batch(self, input_data_list: list[str]) -> list[list[float]]:
        loop = asyncio.get_event_loop()
        vectors: list[list[float]] = await loop.run_in_executor(
            None,
            lambda: self._get_model()
                        .encode(input_data_list, normalize_embeddings=True,
                                show_progress_bar=False)
                        .tolist(),
        )
        return vectors


# ── Passthrough cross-encoder (no OpenAI required) ─────────────────────────────

class PassthroughReranker(CrossEncoderClient):
    """
    No-op reranker: preserves the original passage order produced by the
    embedding-based retrieval step.  Avoids requiring an OpenAI API key.
    """

    async def rank(self, query: str, passages: list[str]) -> list[tuple[str, float]]:
        # Return passages with descending dummy scores so graphiti's sort is stable
        return [(p, float(len(passages) - i)) for i, p in enumerate(passages)]


# ── Singleton factory ──────────────────────────────────────────────────────────

_graphiti_instance = None


async def _build_graphiti():
    from graphiti_core import Graphiti
    from graphiti_core.driver.kuzu_driver import KuzuDriver

    # Pass the path string — KuzuDriver creates its own kuzu.Database internally
    driver = KuzuDriver(str(GRAPH_DIR))
    driver._database = GROUP_ID  # required by graphiti_core 0.28.2 (not set by KuzuDriver)

    # KuzuDriver.build_indices_and_constraints() is a no-op; create FTS indices manually.
    # Use a raw kuzu.Connection (same as setup_schema) to avoid graphiti's error logging.
    import kuzu as _kuzu
    from graphiti_core.graph_queries import get_fulltext_indices
    from graphiti_core.driver.driver import GraphProvider
    _conn = _kuzu.Connection(driver.db)
    for q in get_fulltext_indices(GraphProvider.KUZU):
        try:
            _conn.execute(q)
        except Exception as e:
            if 'already exists' not in str(e):
                raise
    _conn.close()

    g = Graphiti(
        llm_client=MiniMaxLLMClient(),
        embedder=BGEEmbedder(),
        cross_encoder=PassthroughReranker(),
        graph_driver=driver,
    )
    return g


def get_graphiti():
    """Return (or lazily create) the shared Graphiti instance."""
    global _graphiti_instance
    if _graphiti_instance is None:
        _graphiti_instance = asyncio.run(_build_graphiti())
    return _graphiti_instance
