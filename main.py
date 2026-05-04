"""
main.py — CLI entry point for the Multi-Agent Research Pipeline.
Usage: python main.py
"""
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

from crew import run_crew
from config import logger, sanitize_topic


def main() -> None:
    print("\n🤖 Multi-Agent Research Pipeline")
    print("=" * 40)

    try:
        raw_topic = input("Enter research topic: ").strip()
        topic = sanitize_topic(raw_topic)
    except (ValueError, KeyboardInterrupt) as exc:
        print(f"\n❌ Input error: {exc}")
        sys.exit(1)

    print(f"\n🚀 Starting research on: '{topic}'\n")
    logger.info("CLI run started — topic: '%s'", topic)

    try:
        result = run_crew(topic)
        print("\n" + "=" * 40)
        print("✅ Research Complete\n")
        print(result)
    except EnvironmentError as exc:
        print(f"\n❌ Configuration error: {exc}")
        sys.exit(1)
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc)
        print(f"\n❌ An error occurred: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()