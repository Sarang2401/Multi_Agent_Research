"""
tasks.py — Prompt builders for the two tasks.
No CrewAI. Just functions that assemble the user-side prompt for each task.
"""

# Platform-specific context added to each prompt
PLATFORM_NOTES = {
    "YouTube Long-Form": (
        "This is a YouTube long-form video (8-20 minutes). "
        "Ideas need enough depth for a tutorial, story, or deep-dive. "
        "Titles should be searchable."
    ),
    "YouTube Shorts": (
        "This is a YouTube Short (under 60 seconds). "
        "Ideas must deliver one punchy insight or quick tip. "
        "High energy. Vertical video."
    ),
    "Instagram Reels": (
        "This is an Instagram Reel (15-90 seconds). "
        "Visually driven, trend-aware, aesthetic hooks. "
        "On-screen text overlays matter a lot here."
    ),
    "TikTok": (
        "This is a TikTok video (15-60 seconds). "
        "Fast-paced, raw, authentic. "
        "The hook must land in the first 1-2 seconds. Use trend-native language."
    ),
}

# Target word counts per length option
LENGTH_WORD_COUNTS = {
    "30 seconds (~75 words)":       75,
    "60 seconds (~150 words)":      150,
    "3 minutes (~450 words)":       450,
    "10 minutes (~1,500 words)":  1500,
    "20 minutes (~3,000 words)":  3000,
}


def build_planning_prompt(niche: str, platform: str, audience: str) -> str:
    """Build the user-side prompt for the Content Planner."""
    platform_context = PLATFORM_NOTES.get(platform, platform)
    return (
        f"Platform context: {platform_context}\n\n"
        f"Channel niche: {niche}\n"
        f"Target audience: {audience}\n\n"
        "Generate my 5 ranked video ideas now."
    )


def build_script_prompt(idea: str, platform: str, video_length: str) -> str:
    """Build the user-side prompt for the Scriptwriter."""
    word_count = LENGTH_WORD_COUNTS.get(video_length, 150)
    platform_context = PLATFORM_NOTES.get(platform, platform)
    return (
        f"Platform: {platform_context}\n"
        f"Video title / idea: {idea}\n"
        f"Target length: {video_length} — write approximately {word_count} spoken words.\n\n"
        "Write my complete video script now."
    )