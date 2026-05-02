from crewai import Crew, Process
from agents import planner, researcher, critic, writer
from tasks import create_tasks

# WHY: Sequential process ensures structured flow (no chaos between agents)

def run_crew(topic):
    tasks = create_tasks(topic)

    crew = Crew(
        agents=[planner, researcher, critic, writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result