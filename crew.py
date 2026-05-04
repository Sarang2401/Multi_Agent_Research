"""
crew.py — Crew orchestration for the Multi-Agent Research Pipeline.
"""
import logging
from crewai import Crew, Process
from agents import planner, researcher, critic, writer
from tasks import create_tasks
from config import CREW_MAX_RPM, validate_env, sanitize_topic

logger = logging.getLogger("research_pipeline.crew")


def run_crew(topic: str) -> str:
    """
    Validate input, assemble the crew, and execute the research pipeline.

    Args:
        topic: The raw research topic string from the user.

    Returns:
        The final research report as a string.

    Raises:
        ValueError: If the topic fails validation.
        EnvironmentError: If required API keys are missing.
    """
    # 1. Validate environment variables
    validate_env()

    # 2. Sanitise user input (prevents injection and garbage inputs)
    clean_topic = sanitize_topic(topic)
    logger.info("Starting research pipeline — topic: '%s'", clean_topic)

    # 3. Build tasks with the sanitised topic
    tasks = create_tasks(clean_topic)

    # 4. Assemble and run the crew
    # ── Architecture note ──────────────────────────────────────────────────
    # Process.sequential: agents execute in strict order with zero manager
    #   overhead. Reliable on free-tier APIs (Groq 12K TPM).
    # Process.hierarchical: a manager LLM plans and dynamically delegates.
    #   Enables re-planning mid-run. Recommended with a paid API key.
    # ───────────────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[planner, researcher, critic, writer],
        tasks=tasks,
        process=Process.sequential,
        memory=False,        # Requires OpenAI key for internal analysis LLM
        cache=True,          # Cache tool results to reduce duplicate API calls
        max_rpm=CREW_MAX_RPM,
        verbose=True,
    )

    result = crew.kickoff()
    logger.info("Research pipeline completed successfully.")
    return str(result)