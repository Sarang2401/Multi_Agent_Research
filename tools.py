"""
tools.py — Custom CrewAI tools for the Multi-Agent Research Pipeline.
"""
import logging
from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from config import SEARCH_MAX_RESULTS

logger = logging.getLogger("research_pipeline.tools")


class DuckDuckGoSearchTool(BaseTool):
    """
    Web search tool powered by DuckDuckGo.
    Returns a formatted list of titles and URLs for a given query.
    Fails gracefully — never crashes the agent pipeline.
    """
    name: str = "DuckDuckGo Search Tool"
    description: str = (
        "Search the internet for relevant, up-to-date information. "
        "Input should be a concise search query string."
    )

    def _run(self, query: str) -> str:
        logger.info("DuckDuckGo search — query: %s", query)
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query.strip(), max_results=SEARCH_MAX_RESULTS):
                    title = r.get("title", "No title")
                    href = r.get("href", "")
                    body = r.get("body", "")[:150]  # First 150 chars of snippet
                    results.append(f"**{title}**\n{body}\n{href}")

            if not results:
                logger.warning("No results for query: %s", query)
                return f"No results found for: {query}"

            logger.info("Found %d results", len(results))
            return "\n\n".join(results)

        except Exception as exc:
            logger.error("Search failed: %s", exc)
            return f"Search error: {exc}"