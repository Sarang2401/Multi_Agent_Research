"""
config.py — Centralised configuration for the Multi-Agent Research Pipeline.
All environment variables and tunable constants live here.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# ─── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("research_pipeline")

# ─── API Keys (validated at startup) ────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

def validate_env() -> None:
    """Raise a clear error if required environment variables are missing."""
    missing = [k for k, v in {
        "GROQ_API_KEY": GROQ_API_KEY,
    }.items() if not v]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Please add them to your .env file."
        )

# ─── LLM Settings ───────────────────────────────────────────────────────────
LLM_MODEL: str = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "800"))
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_TEMPERATURE_DETERMINISTIC: float = 0.2

# ─── Crew Settings ──────────────────────────────────────────────────────────
CREW_MAX_RPM: int = int(os.getenv("CREW_MAX_RPM", "2"))

# ─── Search Settings ────────────────────────────────────────────────────────
SEARCH_MAX_RESULTS: int = int(os.getenv("SEARCH_MAX_RESULTS", "5"))

# ─── Input Validation ───────────────────────────────────────────────────────
MAX_TOPIC_LENGTH: int = 200
MIN_TOPIC_LENGTH: int = 3
BLOCKED_PATTERNS: list[str] = [
    "<script", "javascript:", "DROP TABLE", "--", "/*", "*/",
]

def sanitize_topic(topic: str) -> str:
    """
    Sanitise and validate user-supplied research topic.
    Returns the cleaned topic or raises ValueError.
    """
    topic = topic.strip()
    if len(topic) < MIN_TOPIC_LENGTH:
        raise ValueError(f"Topic must be at least {MIN_TOPIC_LENGTH} characters.")
    if len(topic) > MAX_TOPIC_LENGTH:
        raise ValueError(f"Topic must be under {MAX_TOPIC_LENGTH} characters.")
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in topic.lower():
            raise ValueError("Topic contains disallowed content.")
    return topic
