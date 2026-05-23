"""
tasks.py — Task definitions for the Multi-Agent Research Pipeline.

Each task has a concise description to keep input token counts low,
which is critical for staying within Groq free-tier TPM limits.
"""
import logging
from datetime import datetime
from pathlib import Path
from crewai import Task
from agents import planner, researcher, critic, writer

logger = logging.getLogger("research_pipeline.tasks")

# Reports are saved to a dedicated output directory
OUTPUT_DIR = Path("reports")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_tasks(topic: str) -> list[Task]:
    """
    Build and return the ordered list of tasks for a research run.

    Pipeline:
        1. plan_task    — Planner formulates 3 research questions.
        2. research_task — Researcher gathers web findings per question.
        3. critique_task — Critic identifies gaps in the research.
        4. write_task   — Writer synthesises everything into a final report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_topic = "".join(c if c.isalnum() or c in " -_" else "" for c in topic)
    safe_topic = safe_topic.strip().replace(" ", "_")[:50]
    filename = OUTPUT_DIR / f"{safe_topic}_{timestamp}.md"

    logger.info("Creating tasks for topic: '%s' | output: %s", topic, filename)

    plan_task = Task(
        description=(
            f"Topic: {topic}\n"
            "Formulate exactly 3 focused, answerable research questions. "
            "Each question should cover a distinct angle of the topic."
        ),
        expected_output="A numbered list of exactly 3 research questions.",
        agent=planner,
    )

    research_task = Task(
        description=(
            "Use the DuckDuckGo Search Tool to find relevant URLs for each research question. "
            "Then, MUST use the ScrapeWebsiteTool to read the full content of the 1-2 most promising URLs per question. "
            "For each question, provide 2-3 deep, synthesized bullet points with the exact source URLs."
        ),
        expected_output=(
            "Structured findings: for each research question, "
            "2-3 deep bullet points containing facts extracted from scraped websites, along with the source URLs."
        ),
        agent=researcher,
        context=[plan_task],
    )

    critique_task = Task(
        description=(
            "Review the research findings critically. "
            "Identify exactly 2-3 specific gaps, biases, or missing perspectives. "
            "Be precise and brief — one sentence per gap."
        ),
        expected_output="A bullet list of 2-3 critical gaps in the research.",
        agent=critic,
        context=[research_task],
    )

    write_task = Task(
        description=(
            "Write a professional markdown research report. "
            "Include: Introduction, Findings (per question), Critical Gaps, Conclusion, and a numbered Sources section. "
            "Ensure that you use inline academic citations (e.g. [1], [2]) throughout the Findings section that correspond to the numbered Sources section at the end. "
            "Keep it under 600 words. Do NOT include any JSON, code blocks, or tool calls."
        ),
        expected_output=(
            "A complete markdown report with sections: "
            "Introduction, Findings (with inline citations), Critical Gaps, Conclusion, Sources."
        ),
        agent=writer,
        context=[research_task, critique_task],
        output_file=str(filename),  # CrewAI saves automatically — no tool call needed
    )

    return [plan_task, research_task, critique_task, write_task]