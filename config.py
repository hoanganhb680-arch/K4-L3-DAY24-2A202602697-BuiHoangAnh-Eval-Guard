"""Shared configuration for K4 / Track 3A: Eval + Guardrail Stack."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "") if os.getenv("OPENAI_API_KEY", "").startswith("sk-") else ""
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini" if GEMINI_API_KEY else "openai")
ROUTER_BASE_URL = os.getenv("ROUTER_BASE_URL", "")
ROUTER_API_KEY = os.getenv("ROUTER_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Optional: for HuggingFace models

# --- Qdrant (same as Day 18) ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "lab24_production"
NAIVE_COLLECTION = "lab24_naive"

# --- Embedding (same as Day 18) ---
EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIM = 1024

# --- Chunking (same as Day 18) ---
HIERARCHICAL_PARENT_SIZE = 2048
HIERARCHICAL_CHILD_SIZE = 256
SEMANTIC_THRESHOLD = 0.85

# --- Search (same as Day 18) ---
BM25_TOP_K = 20
DENSE_TOP_K = 20
HYBRID_TOP_K = 20
RERANK_TOP_K = 3

# --- Paths ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
FIXTURES_DIR = os.path.join(ROOT_DIR, "fixtures")
ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")
TEST_SET_PATH = os.path.join(FIXTURES_DIR, "test_set_50q.json")
ANSWERS_PATH = os.path.join(ARTIFACTS_DIR, "answers_50q.json")
HUMAN_LABELS_PATH = os.path.join(FIXTURES_DIR, "human_labels_10q.json")
ADVERSARIAL_SET_PATH = os.path.join(FIXTURES_DIR, "adversarial_set_20.json")
CLEAN_SET_PATH = os.path.join(FIXTURES_DIR, "clean_set_8.json")
OUTPUT_SET_PATH = os.path.join(FIXTURES_DIR, "output_set_4.json")
GUARDRAILS_CONFIG_DIR = os.path.join(ROOT_DIR, "guardrails")
PAIR_QUESTION_IDS = (1, 5, 12, 21, 41)

# --- LLM Judge ---
_DEFAULT_MODEL = "gemini-3.1-flash-lite" if LLM_PROVIDER == "gemini" else "gpt-4o-mini"
GENERATION_MODEL = os.getenv("GENERATION_MODEL", _DEFAULT_MODEL)
JUDGE_MODEL = os.getenv("JUDGE_MODEL", GENERATION_MODEL)
_GEMINI_OPENAI_MODEL = os.getenv("RAGAS_MODEL", "gemini-3.1-flash-lite")

# --- Compat aliases used by the copied Day18 modules (m4/m5) ---
RAGAS_MODEL = _GEMINI_OPENAI_MODEL
LLM_MODEL = GENERATION_MODEL


def get_llm_client():
    """Return an LLM client, or None when no key is configured."""
    from openai import OpenAI
    if LLM_PROVIDER == "9router" and ROUTER_BASE_URL:
        return OpenAI(api_key=ROUTER_API_KEY, base_url=ROUTER_BASE_URL)
    if LLM_PROVIDER == "gemini" and GEMINI_API_KEY:
        return OpenAI(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
    if OPENAI_API_KEY:
        return OpenAI()
    return None


def gemini_http_clients():
    """HTTP clients for the Gemini OpenAI-compatible endpoint."""
    import httpx
    transport = httpx.HTTPTransport()
    http_client = httpx.Client(transport=transport)
    async_transport = httpx.AsyncHTTPTransport()
    http_async_client = httpx.AsyncClient(transport=async_transport)
    return http_client, http_async_client


def get_openai_chat_model():
    """Return a LangChain ChatOpenAI instance configured for the active provider."""
    if not (GEMINI_API_KEY or OPENAI_API_KEY or ROUTER_BASE_URL):
        return None
    from langchain_openai import ChatOpenAI
    options = {"model": RAGAS_MODEL, "timeout": 45, "max_retries": 1}
    if LLM_PROVIDER == "9router" and ROUTER_BASE_URL:
        options.update(api_key=ROUTER_API_KEY, base_url=ROUTER_BASE_URL)
    elif LLM_PROVIDER == "gemini":
        options.update(
            api_key=GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        options["http_client"], options["http_async_client"] = gemini_http_clients()
    return ChatOpenAI(**options)

# --- Guardrail latency budget ---
LATENCY_BUDGET_P95_MS = 500  # Full guard target; Task 12 currently measures input guards only.
PRESIDIO_LANGUAGE = "en"    # Presidio base language; custom VN recognizers added via PatternRecognizer
