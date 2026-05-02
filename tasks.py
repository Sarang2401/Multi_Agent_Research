from crewai import Task
from agents import planner, researcher, critic, writer

# WHY: Tasks define workflow steps and pass context between agents

def create_tasks(topic):

    plan_task = Task(
        description=f"Break the topic '{topic}' into 3-5 detailed research questions.",
        expected_output="A numbered list of research questions.",
        agent=planner
    )

    research_task = Task(
        description="Research each question and gather key findings with sources.",
        expected_output="Detailed findings with links.",
        agent=researcher,
        context=[plan_task]  # WHY: researcher uses planner output
    )

    critique_task = Task(
        description="Analyze research for gaps, inconsistencies, or missing perspectives.",
        expected_output="List of improvements and corrections.",
        agent=critic,
        context=[research_task]
    )

    write_task = Task(
        description="Write a comprehensive markdown report with citations and save it.",
        expected_output="Final markdown report.",
        agent=writer,
        context=[research_task, critique_task]
        # WHY: writer uses both findings + critique
    )

    return [plan_task, research_task, critique_task, write_task]