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

SCRIPT_DIR      = Path(__file__).parent
GROUP_ID        = "financial-pdfs"

# LLM call log — every request/response is appended here as a JSON line.
# Readable via the /zep/llm-log page in the Flask app.
LLM_LOG_FILE: Path | None = None   # set by graphiti_ingest.py or zep_app.py

def _log_llm_call(model_name: str, messages: list, response_text: str, elapsed_s: float) -> None:
    """Append one JSONL record to LLM_LOG_FILE (no-op if not configured)."""
    if LLM_LOG_FILE is None:
        return
    import time as _time
    record = {
        "ts":       _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model":    model_name,
        "elapsed":  round(elapsed_s, 2),
        "messages": [
            {"role": m.get("role", "?"), "content": m.get("content", "")}
            for m in messages
        ],
        "response": response_text,
    }
    try:
        with open(LLM_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _find_project_root() -> Path:
    """Return the main git repo root, even when running from a worktree.

    Worktrees have a .git FILE; the main repo has a .git DIRECTORY.
    Walking up until we find a .git directory gives us the canonical root.
    """
    p = SCRIPT_DIR.resolve()
    while p != p.parent:
        git = p / ".git"
        if git.exists() and git.is_dir():
            return p
        p = p.parent
    return SCRIPT_DIR  # fallback (should not happen in normal use)


_PROJECT_ROOT    = _find_project_root()
GRAPH_DIR        = _PROJECT_ROOT / "db" / "graphiti_db"
_LOCAL_MODEL_DIR = _PROJECT_ROOT / "models" / "bge-m3"

# Set to True to print every LLM request and response to stdout (debug aid).
PRINT_ALL_LLM_CALLS: bool = False


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
                extra = (
                    "\n\nYou MUST reply with ONLY valid JSON (no markdown, no prose) "
                    "that matches this exact JSON schema:\n" + schema
                )
                # For deduplication: force exact name match from EXISTING ENTITIES
                if response_model.__name__ == "NodeResolutions":
                    extra += (
                        "\n\nCRITICAL for duplicate_name: copy the name CHARACTER-FOR-CHARACTER "
                        "from the EXISTING ENTITIES list. Do NOT abbreviate, translate, paraphrase, "
                        "or invent any name. If no entity in EXISTING ENTITIES is a true duplicate, "
                        "use an empty string \"\"."
                    )
                # For edge extraction: force exact entity name usage + guarantee minimum edges
                if response_model.__name__ == "ExtractedEdges":
                    extra += (
                        "\n\nRELATIONSHIP EXTRACTION RULES:"
                        "\n\n1. CRITICAL — exact names: copy source_entity_name and target_entity_name "
                        "CHARACTER-FOR-CHARACTER from the ENTITIES list. Do NOT rephrase, abbreviate, "
                        "expand, or change capitalisation. If you cannot find a matching entity name, skip."
                        "\n\n2. EXTRACT AGGRESSIVELY — you MUST extract AT LEAST 2 relationships. "
                        "Never return an empty list. Start with the most obvious: what does the company "
                        "make/sell? who are its competitors? who supplies it?"
                        "\n\n3. PRIORITISED relationship types to extract:"
                        "\n   - Product/platform MADE_BY or SOLD_BY company    (e.g. H100 → NVIDIA)"
                        "\n   - Business segment OPERATED_BY company            (e.g. Data Center → NVIDIA)"
                        "\n   - Company COMPETES_WITH company                   (e.g. NVIDIA → AMD)"
                        "\n   - Company SUPPLIES or MANUFACTURES_FOR company    (e.g. TSMC → NVIDIA)"
                        "\n   - Company HAS_REVENUE_FROM segment/market"
                        "\n   - Ticker REPRESENTS company                       (e.g. NVDA → NVIDIA)"
                        "\n   - Company ACQUIRED or INVESTED_IN company"
                        "\n   - Company PARTNERS_WITH or JOINT_VENTURE_WITH company"
                        "\n   - Company IS_SUBSIDIARY_OF or SPUN_OFF_FROM company"
                        "\n\n4. relation_type should be a short ALL_CAPS verb phrase (e.g. MADE_BY, COMPETES_WITH)."
                    )
                # For entity extraction: companies, products, and named markets only
                if response_model.__name__ == "ExtractedEntities":
                    # Inject user-isolated entities so LLM skips re-discovering them
                    try:
                        import graph_mirror as _gm
                        _iso_conn = _gm.get_conn()
                        _isolated = _gm.get_isolated_entity_names(_iso_conn)
                        _iso_conn.close()
                        if _isolated:
                            _iso_list = ", ".join(f'"{n}"' for n in _isolated[:60])
                            extra += (
                                "\n\nUSER-ISOLATED ENTITIES — DO NOT EXTRACT (ever):"
                                f"\n{_iso_list}"
                                "\nThese entities have been flagged by the user as unwanted."
                                " Never extract them, even if they appear prominently in the text."
                            )
                    except Exception:
                        pass
                    extra += (
                        "\n\nSTRICT ENTITY EXTRACTION RULES:"
                        "\n\nEntities must be a real company, a specific BRANDED product/technology,"
                        " or a clearly named business segment. Nothing else."
                        "\n\nALLOWED (extract ONLY these):"
                        "\n- Companies and organisations (e.g. NVIDIA, TSMC, AMD, Microsoft, SoftBank, Arm)"
                        "\n- Stock tickers (e.g. NVDA, TSM, AAPL, AMD)"
                        "\n- Named products, chips, platforms, or proprietary technologies"
                        "\n  (e.g. H100, Blackwell, Hopper, CUDA, NVLink, CoWoS, Grace CPU, GeForce, Quadro)"
                        "\n  Must be a specific BRANDED or MODEL name — NOT a generic category."
                        "\n  BAD: 'GPU', 'AI', 'VR', 'HPC', 'Digital Signal Processors' — too generic."
                        "\n- Named business segments the company itself uses for its divisions"
                        "\n  (e.g. Data Center, Gaming, Automotive, Professional Visualization)"
                        "\n\nFORBIDDEN (NEVER extract — skip entirely):"
                        "\n- ANY monetary value or financial figure: $79 million, $5.2 billion, $1.0 billion."
                        "\n  Any string starting with '$' or containing a number + million/billion/trillion."
                        "\n  If the name contains a dollar sign OR a numeric amount, DO NOT extract it."
                        "\n- Generic technology acronyms: AI, VR, AR, GPU, HPC, IoT, ML, API, SDK"
                        "\n- Generic technology categories: 'Digital Signal Processors',"
                        "  'Analog Integrated Circuits', 'Semiconductor Market', 'Cloud Computing'"
                        "\n- Countries, regions, or geographies (China, United States, Europe, Taiwan)"
                        "\n- Financial indices, benchmarks, or ratings (S&P 500, NASDAQ, Moody's)"
                        "\n- Generic financial instruments (convertible notes, bonds, equity)"
                        "\n- Human personal names (executives, analysts, lawyers, investors)"
                        "\n  Examples: Jensen Huang, Tim Cook, Timothy S. Teter"
                        "\n- Legal cases: 'v.', 'In re', 'Derivative Litigation', 'Class Action'"
                        "\n- SEC rules and rule numbers (Rule 10b-5, Regulation S-K, etc.)"
                        "\n- SEC filing form types (Form 10-K, Form 10-Q, Annual Report, etc.)"
                        "\n- Regulatory/accounting boilerplate: IRS, FASB, GAAP, IFRS, PCAOB"
                        "\n- Laws and acts (Securities Exchange Act, Sarbanes-Oxley, Dodd-Frank)"
                        "\n- Generic legal/accounting concepts (fiscal year, audit, depreciation)"
                        "\n- Generic time periods (Q1, Q2, fiscal 2024)"
                        "\n- Vague concepts (supply chain, demand, growth, risk, strategy, innovation)"
                        "\n\nIf in doubt, skip the entity. Quality over quantity."
                    )
                content = content + extra
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

        model_name = response_model.__name__ if response_model else "plain-text"
        if PRINT_ALL_LLM_CALLS:
            print(f"\n{'='*70}")
            print(f"[LLM CALL] model={model_name}")
            for i, msg in enumerate(mm_messages):
                role = msg.get("role", "?")
                body = msg.get("content", "")
                print(f"  [{i}] {role.upper()}: {body[:2500]}{'…' if len(body) > 2500 else ''}")
            print(f"{'─'*70}")
        else:
            import time as _time
            _t0 = _time.monotonic()
            print(f"    · LLM → {model_name} …", end=" ", flush=True)

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

        if not PRINT_ALL_LLM_CALLS:
            import time as _time
            _elapsed_s = _time.monotonic() - _t0
            print(f"done ({_elapsed_s:.1f}s)", flush=True)
        else:
            _elapsed_s = 0.0  # already printed in debug mode

        # Extract token usage from raw API response
        _usage: dict | None = None
        try:
            _usage = json.loads(_raw).get("usage")
        except Exception:
            pass

        _log_llm_call(model_name, mm_messages, text, _elapsed_s)

        # Langfuse tracing (no-op if not configured)
        try:
            import langfuse_monitor
            langfuse_monitor.log_generation(
                call_type=model_name,
                model=self.config.model or "MiniMax-Text-01",
                messages=mm_messages,
                response_text=text,
                elapsed_s=_elapsed_s,
                usage=_usage,
            )
        except Exception:
            pass

        if PRINT_ALL_LLM_CALLS:
            print(f"  [RESPONSE] {text[:800]}{'…' if len(text) > 800 else ''}")
            print(f"{'='*70}\n")

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
            if _LOCAL_MODEL_DIR.exists():
                logger.info("Loading bge-m3 from local cache: %s", _LOCAL_MODEL_DIR)
                cls._model = SentenceTransformer(str(_LOCAL_MODEL_DIR))
            else:
                logger.info("Downloading bge-m3 (one-time) …")
                cls._model = SentenceTransformer("BAAI/bge-m3")
                logger.info("Saving bge-m3 to %s …", _LOCAL_MODEL_DIR)
                _LOCAL_MODEL_DIR.mkdir(parents=True, exist_ok=True)
                cls._model.save(str(_LOCAL_MODEL_DIR))
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
