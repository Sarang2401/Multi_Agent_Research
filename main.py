from crew import run_crew

# WHY: Simple CLI for quick testing before UI

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    result = run_crew(topic)
    print("\nFinal Output:\n")
    print(result)