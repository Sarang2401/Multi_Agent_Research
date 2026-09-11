"""
crew.py — Direct Gemini API calls. No CrewAI.

Public functions:
    run_planner(niche, platform, audience)         -> str
    run_scriptwriter(idea, platform, length)       -> str
    run_blog_writer(topic, audience, tone, ...)    -> str
    run_website_copy(product, audience, tone, ...) -> str
    run_product_desc(name, category, ...)          -> str
    run_hook_generator(topic, audience, medium)    -> str
    run_tone_rewriter(text, tone, context)         -> str

Uses google-genai (the current official SDK).
Model: gemini-2.5-flash (free tier, no credit card).
Retry-with-backoff on 429 rate-limit errors.
All errors surface as plain-English custom exceptions.
"""

import os
import time
import logging
from google import genai
from google.genai import types

from agents import (
    PLANNER_SYSTEM_PROMPT,
    SCRIPTWRITER_SYSTEM_PROMPT,
    BLOG_WRITER_SYSTEM_PROMPT,
    WEBSITE_COPY_SYSTEM_PROMPT,
    PRODUCT_DESCRIPTION_SYSTEM_PROMPT,
    HOOK_GENERATOR_SYSTEM_PROMPT,
    TONE_REWRITER_SYSTEM_PROMPT,
)
from tasks import (
    build_planning_prompt,
    build_script_prompt,
    build_blog_prompt,
    build_website_copy_prompt,
    build_product_desc_prompt,
    build_hooks_prompt,
    build_rewrite_prompt,
)
from config import (
    GEMINI_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    RETRY_MAX_ATTEMPTS,
    RETRY_BASE_WAIT_SECONDS,
    get_api_key,
    sanitize_input,
)

logger = logging.getLogger("script_generator.crew")


# ── Custom plain-English exceptions ──────────────────────────────────────────

class RateLimitError(Exception):
    """Free tier request limit hit."""
    pass

class NoKeyError(Exception):
    """API key missing or rejected."""
    pass

class ConnectionError(Exception):
    """Cannot reach Google's servers."""
    pass


# ── Error classifier ──────────────────────────────────────────────────────────

def _classify(exc: Exception):
    msg = str(exc).lower()
    if "429" in msg or "resource_exhausted" in msg or "quota" in msg or "rate" in msg:
        return "rate_limit"
    if "401" in msg or "403" in msg or "api_key" in msg or "unauthenticated" in msg or "invalid" in msg:
        return "auth"
    if "connection" in msg or "timeout" in msg or "network" in msg or "unreachable" in msg or "name resolution" in msg:
        return "connection"
    return "unknown"


# ── Core call with retry ──────────────────────────────────────────────────────

def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    Send one request to Gemini with retry-on-429.
    Raises plain-English exceptions for all failure modes.
    """
    api_key = get_api_key()
    if not api_key:
        raise NoKeyError(
            "No API key found. Please paste your free Gemini key in the setup screen."
        )

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=LLM_TEMPERATURE,
        max_output_tokens=LLM_MAX_TOKENS,
    )

    last_exc = None
    for attempt in range(1, RETRY_MAX_ATTEMPTS + 1):
        try:
            logger.info("Gemini call attempt %d/%d", attempt, RETRY_MAX_ATTEMPTS)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=user_prompt,
                config=config,
            )
            return response.text

        except Exception as exc:
            last_exc = exc
            kind = _classify(exc)

            if kind == "rate_limit":
                wait = RETRY_BASE_WAIT_SECONDS * attempt
                logger.warning("Rate limit hit (attempt %d) — waiting %ds", attempt, wait)
                if attempt < RETRY_MAX_ATTEMPTS:
                    time.sleep(wait)
                    continue
                raise RateLimitError(
                    f"Free tier limit hit — please wait about {wait} seconds and try again."
                ) from exc

            elif kind == "auth":
                raise NoKeyError(
                    "Your API key did not work. Please paste it again — "
                    "or get a new one at https://aistudio.google.com/apikey"
                ) from exc

            elif kind == "connection":
                raise ConnectionError(
                    "Could not connect to the internet. "
                    "Please check your Wi-Fi or cable connection and try again."
                ) from exc

            else:
                logger.error("Unexpected Gemini error: %s", exc)
                raise RuntimeError(
                    "Something went wrong. Please try again in a moment."
                ) from exc

    raise RuntimeError("Something unexpected happened. Please try again.") from last_exc


# ── Public API ────────────────────────────────────────────────────────────────

def run_planner(niche: str, platform: str, audience: str) -> str:
    """
    Generate 5 ranked video ideas for the given niche and platform.

    Args:
        niche:    Creator's channel topic
        platform: One of the platform keys in tasks.PLATFORM_NOTES
        audience: Description of who watches the channel

    Returns:
        Formatted string with 5 ranked ideas + hook rationales.
    """
    clean_niche    = sanitize_input(niche,    "Channel niche")
    clean_audience = sanitize_input(audience, "Audience description")
    user_prompt    = build_planning_prompt(clean_niche, platform, clean_audience)

    logger.info("Running planner — platform: %s, niche: %s", platform, clean_niche)
    return _call_gemini(PLANNER_SYSTEM_PROMPT, user_prompt)


def run_scriptwriter(idea: str, platform: str, video_length: str) -> str:
    """
    Write a full video script for the chosen idea and length.

    Args:
        idea:         The chosen video idea / title
        platform:     Target platform
        video_length: One of the keys in tasks.LENGTH_WORD_COUNTS

    Returns:
        Full script as a formatted string.
    """
    clean_idea  = sanitize_input(idea, "Video idea")
    user_prompt = build_script_prompt(clean_idea, platform, video_length)

    logger.info("Running scriptwriter — idea: %s, length: %s", clean_idea, video_length)
    return _call_gemini(SCRIPTWRITER_SYSTEM_PROMPT, user_prompt)


def run_blog_writer(topic: str, audience: str, tone: str, length: str, keywords: str = "") -> str:
    """Write a full SEO blog post."""
    clean_topic    = sanitize_input(topic,    "Blog topic")
    clean_audience = sanitize_input(audience, "Target reader")
    user_prompt    = build_blog_prompt(clean_topic, clean_audience, tone, length, keywords)
    logger.info("Running blog writer — topic: %s", clean_topic)
    return _call_gemini(BLOG_WRITER_SYSTEM_PROMPT, user_prompt)


def run_website_copy(product: str, audience: str, tone: str, usp: str) -> str:
    """Generate conversion-focused website copy."""
    clean_product  = sanitize_input(product,  "Product/service name")
    clean_audience = sanitize_input(audience, "Target customer")
    clean_usp      = sanitize_input(usp,      "Unique selling point")
    user_prompt    = build_website_copy_prompt(clean_product, clean_audience, tone, clean_usp)
    logger.info("Running website copy — product: %s", clean_product)
    return _call_gemini(WEBSITE_COPY_SYSTEM_PROMPT, user_prompt)


def run_product_desc(name: str, category: str, features: str, audience: str, platform: str) -> str:
    """Write an e-commerce product description."""
    clean_name     = sanitize_input(name,     "Product name")
    clean_features = sanitize_input(features, "Product features")
    clean_audience = sanitize_input(audience, "Target buyer")
    user_prompt    = build_product_desc_prompt(clean_name, category, clean_features, clean_audience, platform)
    logger.info("Running product description — product: %s", clean_name)
    return _call_gemini(PRODUCT_DESCRIPTION_SYSTEM_PROMPT, user_prompt)


def run_hook_generator(topic: str, audience: str, medium: str) -> str:
    """Generate 10 scroll-stopping hooks for a topic."""
    clean_topic    = sanitize_input(topic,    "Topic")
    clean_audience = sanitize_input(audience, "Target audience")
    user_prompt    = build_hooks_prompt(clean_topic, clean_audience, medium)
    logger.info("Running hook generator — topic: %s", clean_topic)
    return _call_gemini(HOOK_GENERATOR_SYSTEM_PROMPT, user_prompt)


def run_tone_rewriter(text: str, tone: str, context: str = "") -> str:
    """Rewrite any text in the specified tone."""
    if len(text.strip()) < 10:
        raise ValueError("Text is too short to rewrite.")
    if len(text) > 4000:
        raise ValueError("Text is too long — please keep it under 4,000 characters.")
    user_prompt = build_rewrite_prompt(text, tone, context)
    logger.info("Running tone rewriter — tone: %s", tone)
    return _call_gemini(TONE_REWRITER_SYSTEM_PROMPT, user_prompt)