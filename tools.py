from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from datetime import datetime

# WHY: We create custom tools so agents can use them as capabilities
# instead of embedding logic directly inside prompts (clean architecture)

class DuckDuckGoSearchTool(BaseTool):
    name = "DuckDuckGo Search Tool"
    description = "Search the internet for relevant information using DuckDuckGo."

    def _run(self, query: str) -> str:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"{r['title']} - {r['href']}")
        return "\n".join(results)


class FileWriteTool(BaseTool):
    name = "File Write Tool"
    description = "Writes the final report to a markdown file."

    def _run(self, content: str) -> str:
        filename = f"report_{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report saved as {filename}"