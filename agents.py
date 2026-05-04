"""
agents.py — Specialist AI agents for the Multi-Agent Research Pipeline.

Pipeline flow:
  Planner → Researcher → Critic → Writer

Architecture:
  - Process.sequential: zero manager overhead, reliable on free-tier APIs.
  - Process.hierarchical: manager LLM dynamically delegates; enable with paid key.
  - Two LLM configs: deterministic (planning/analysis) vs. creative (research/writing).
"""
import logging
from crewai import Agent
from crewai.llm import LLM
from tools import DuckDuckGoSearchTool
from config import LLM_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE, LLM_TEMPERATURE_DETERMINISTIC

logger = logging.getLogger("research_pipeline.agents")

# ─── LLM Configurations ─────────────────────────────────────────────────────
# Creative LLM: used by Researcher and Writer for generative tasks
llm = LLM(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
)

# Deterministic LLM: used by Planner and Critic for structured, factual tasks
deterministic_llm = LLM(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE_DETERMINISTIC,
    max_tokens=LLM_MAX_TOKENS,
)

logger.info("LLM initialised — model: %s, max_tokens: %d", LLM_MODEL, LLM_MAX_TOKENS)

# ─── Shared Tools ────────────────────────────────────────────────────────────
search_tool = DuckDuckGoSearchTool()

# ─── Agent Definitions ───────────────────────────────────────────────────────

planner = Agent(
    role="Research Planner",
    goal="Decompose a research topic into 3 precise, answerable sub-questions.",
    backstory=(
        "You are a senior research strategist with expertise in structuring "
        "complex topics into clear, measurable research questions. You think "
        "in first principles and avoid vague or overlapping questions."
    ),
    llm=deterministic_llm,
    allow_delegation=False,
    verbose=True,
)

researcher = Agent(
    role="Web Researcher",
    goal=(
        "Find accurate, recent information from the internet and "
        "synthesise it into concise, source-backed findings."
    ),
    backstory=(
        "You are a meticulous internet researcher who verifies claims against "
        "multiple sources. You always cite URLs and never fabricate data."
    ),
    tools=[search_tool],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

critic = Agent(
    role="Research Critic",
    goal="Identify the most critical gaps, biases, and contradictions in the research.",
    backstory=(
        "You are a rigorous peer reviewer who challenges assumptions and "
        "ensures research is complete, balanced, and objective. You focus "
        "on what is missing rather than what is present."
    ),
    llm=deterministic_llm,
    allow_delegation=False,
    verbose=True,
)

writer = Agent(
    role="Report Writer",
    goal=(
        "Synthesise the research and critique into a well-structured, "
        "professional markdown report with proper citations."
    ),
    backstory=(
        "You are a professional technical writer who transforms raw research "
        "into polished, readable reports. You use clear headings, bullet points, "
        "and always include a Sources section."
    ),
    # No tools: file saving is handled by output_file on the Task to avoid
    # tool-call JSON truncation under max_tokens constraints.
    llm=llm,
    allow_delegation=False,
    verbose=True,
)