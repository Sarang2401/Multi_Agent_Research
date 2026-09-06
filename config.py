"""
config.py — Centralised configuration for the Social Media Script Generator.
All environment variables and tunable constants live here.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

# Load .env from the same folder as this file
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("script_generator")

# ── API Key helpers ───────────────────────────────────────────────────────────

def get_api_key() -> str:
    """Return the current GOOGLE_API_KEY from the environment."""
    return os.getenv("GOOGLE_API_KEY", "").strip()


def save_api_key(key: str) -> None:
    """
    Persist the user's API key to the .env file so it survives restarts.
    Creates the file if it does not exist.
    """
    key = key.strip()
    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), "GOOGLE_API_KEY", key)
    os.environ["GOOGLE_API_KEY"] = key
    logger.info("API key saved to .env")


def is_api_key_set() -> bool:
    """Return True if a non-empty API key is currently configured."""
    return bool(get_api_key())


# ── LLM Settings ─────────────────────────────────────────────────────────────
# gemini-3.6-flash: current free-tier model, fast, no credit card required.
GEMINI_MODEL: str       = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
LLM_MAX_TOKENS: int     = int(os.getenv("LLM_MAX_TOKENS", "8192"))
LLM_TEMPERATURE: float  = float(os.getenv("LLM_TEMPERATURE", "0.8"))

# ── Retry settings for free-tier 429 errors ───────────────────────────────────
RETRY_MAX_ATTEMPTS: int     = 3
RETRY_BASE_WAIT_SECONDS: int = 60  # waits 60s, then 120s between retries

# ── Input validation ──────────────────────────────────────────────────────────
MAX_FIELD_LENGTH: int = 300
MIN_FIELD_LENGTH: int = 3
MAX_TOPIC_LENGTH: int = MAX_FIELD_LENGTH  # alias for any legacy imports

BLOCKED_PATTERNS: list[str] = [
    "<script", "javascript:", "DROP TABLE", "--", "/*", "*/",
]


def sanitize_input(text: str, field_name: str = "Input") -> str:
    """
    Validate a user-supplied text field.
    Returns the cleaned text or raises ValueError with a plain-English message.
    """
    text = text.strip()
    if len(text) < MIN_FIELD_LENGTH:
        raise ValueError(f"{field_name} is too short - please add a bit more detail.")
    if len(text) > MAX_FIELD_LENGTH:
        raise ValueError(
            f"{field_name} is a little too long - please keep it under {MAX_FIELD_LENGTH} characters."
        )
    for pattern in BLOCKED_PATTERNS:
        if pattern.lower() in text.lower():
            raise ValueError(f"{field_name} contains content that cannot be processed.")
    return text


def sanitize_topic(topic: str) -> str:
    """Alias kept for any legacy imports."""
    return sanitize_input(topic, "Topic")
