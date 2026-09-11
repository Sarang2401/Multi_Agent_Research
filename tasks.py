"""
tasks.py — Prompt builders for all Pistelle AI tools.
No CrewAI. Just functions that assemble the user-side prompt for each task.
"""

# Platform-specific context added to each prompt
PLATFORM_NOTES = {
    "YouTube":         "YouTube long-form video (8-20 minutes). Ideas need enough depth for a tutorial, story, or deep-dive. Titles should be searchable.",
    "YouTube Shorts":  "YouTube Short (under 60 seconds). Ideas must deliver one punchy insight or quick tip. High energy. Vertical video.",
    "Instagram Reels": "Instagram Reel (15-90 seconds). Visually driven, trend-aware, aesthetic hooks. On-screen text overlays matter a lot here.",
    "TikTok":          "TikTok video (15-60 seconds). Fast-paced, raw, authentic. The hook must land in the first 1-2 seconds. Use trend-native language.",
    # Legacy keys kept for backward-compat
    "YouTube Long-Form": "YouTube long-form video (8-20 minutes). Ideas need enough depth for a tutorial, story, or deep-dive. Titles should be searchable.",
}

LENGTH_WORD_COUNTS = {
    "30 s (~75 words)":         75,
    "60 s (~150 words)":       150,
    "3 min (~450 words)":      450,
    "10 min (~1,500 words)": 1500,
    "20 min (~3,000 words)": 3000,
    # Legacy keys
    "30 seconds (~75 words)":       75,
    "60 seconds (~150 words)":     150,
    "3 minutes (~450 words)":      450,
    "10 minutes (~1,500 words)": 1500,
    "20 minutes (~3,000 words)": 3000,
}

BLOG_LENGTH_WORDS = {
    "Short (600 words)":   600,
    "Standard (1,200 words)": 1200,
    "Long-form (2,500 words)": 2500,
}


# ── Video script ──────────────────────────────────────────────────────────────

def build_planning_prompt(niche: str, platform: str, audience: str) -> str:
    ctx = PLATFORM_NOTES.get(platform, platform)
    return (
        f"Platform context: {ctx}\n\n"
        f"Channel niche: {niche}\n"
        f"Target audience: {audience}\n\n"
        "Generate my 5 ranked video ideas now."
    )


def build_script_prompt(idea: str, platform: str, video_length: str) -> str:
    wc = LENGTH_WORD_COUNTS.get(video_length, 150)
    ctx = PLATFORM_NOTES.get(platform, platform)
    return (
        f"Platform: {ctx}\n"
        f"Video title / idea: {idea}\n"
        f"Target length: {video_length} — write approximately {wc} spoken words.\n\n"
        "Write my complete video script now."
    )


# ── Blog writer ───────────────────────────────────────────────────────────────

def build_blog_prompt(topic: str, audience: str, tone: str, length: str, keywords: str) -> str:
    wc = BLOG_LENGTH_WORDS.get(length, 1200)
    kw_line = f"Target keywords to include naturally: {keywords}" if keywords.strip() else ""
    return (
        f"Blog post topic: {topic}\n"
        f"Target reader: {audience}\n"
        f"Writing tone: {tone}\n"
        f"Target length: approximately {wc} words\n"
        f"{kw_line}\n\n"
        "Write the complete blog post now."
    ).strip()


# ── Website copy ──────────────────────────────────────────────────────────────

def build_website_copy_prompt(product: str, audience: str, tone: str, usp: str) -> str:
    return (
        f"Product or service: {product}\n"
        f"Target customer: {audience}\n"
        f"Brand tone: {tone}\n"
        f"Unique selling point: {usp}\n\n"
        "Write the complete website copy now."
    )


# ── Product description ───────────────────────────────────────────────────────

def build_product_desc_prompt(name: str, category: str, features: str, audience: str, platform: str) -> str:
    return (
        f"Product name: {name}\n"
        f"Product category: {category}\n"
        f"Key features / specs: {features}\n"
        f"Target buyer: {audience}\n"
        f"Selling platform: {platform}\n\n"
        "Write the complete product description now."
    )


# ── Hook generator ────────────────────────────────────────────────────────────

def build_hooks_prompt(topic: str, audience: str, medium: str) -> str:
    return (
        f"Topic: {topic}\n"
        f"Target audience: {audience}\n"
        f"Medium (where these hooks will be used): {medium}\n\n"
        "Generate my 10 hooks now."
    )


# ── Tone rewriter ─────────────────────────────────────────────────────────────

def build_rewrite_prompt(text: str, tone: str, context: str) -> str:
    ctx_line = f"Context about what this text is for: {context}" if context.strip() else ""
    return (
        f"Rewrite the following text in a {tone} tone.\n"
        f"{ctx_line}\n\n"
        f"--- ORIGINAL TEXT ---\n{text}\n--- END ORIGINAL TEXT ---\n\n"
        "Rewritten version:"
    ).strip()
