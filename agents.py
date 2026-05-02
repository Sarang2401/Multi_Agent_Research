from crewai import Agent
from crewai.llm import LLM
from tools import DuckDuckGoSearchTool, FileWriteTool

# WHY: Using Groq LLM (free + fast inference)
llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

search_tool = DuckDuckGoSearchTool()
file_tool = FileWriteTool()

# WHY: Each agent has a distinct role to mimic real-world research workflow

planner = Agent(
    role="Research Planner",
    goal="Break down a topic into structured research questions",
    backstory="You are an expert research strategist who structures complex topics into clear sub-questions.",
    llm=llm,
    verbose=True
)

researcher = Agent(
    role="Web Researcher",
    goal="Find accurate and relevant information from the internet",
    backstory="You are a skilled internet researcher who gathers high-quality sources.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

critic = Agent(
    role="Research Critic",
    goal="Identify gaps, contradictions, and weaknesses in research",
    backstory="You are a skeptical analyst who ensures research is complete and consistent.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Report Writer",
    goal="Generate a polished markdown report with citations",
    backstory="You are a professional writer who synthesizes research into clear reports.",
    tools=[file_tool],
    llm=llm,
    verbose=True
)