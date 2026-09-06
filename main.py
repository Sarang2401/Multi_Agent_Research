"""
main.py — Optional command-line entry point for the Social Media Script Generator.
Most users will use the visual app instead (launch via run.bat or run.sh).

Usage: python main.py
"""
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

from config import logger, sanitize_input, is_api_key_set
from crew import run_planner, run_scriptwriter, RateLimitError, NoKeyError
import crew as crew_module


def main() -> None:
    print("\n🎬 Social Media Script Generator")
    print("=" * 40)
    print("Tip: For a better experience, double-click run.bat (Windows) or run.sh (Mac/Linux)")
    print("=" * 40 + "\n")

    if not is_api_key_set():
        print("❌ No API key found.")
        print("   Get a free key at: https://aistudio.google.com/apikey")
        print("   Then add it to the .env file in this folder as:")
        print("   GOOGLE_API_KEY=your_key_here\n")
        sys.exit(1)

    try:
        platform = input(
            "Platform (1=YouTube Long-Form, 2=YouTube Shorts, 3=Instagram Reels, 4=TikTok): "
        ).strip()
        platforms = {
            "1": "YouTube Long-Form",
            "2": "YouTube Shorts",
            "3": "Instagram Reels",
            "4": "TikTok",
        }
        platform_name = platforms.get(platform, "YouTube Long-Form")

        niche = sanitize_input(input("What's your channel about? ").strip(), "Channel niche")
        audience = sanitize_input(input("Who watches your videos? ").strip(), "Audience")

    except (ValueError, KeyboardInterrupt) as exc:
        print(f"\n❌ {exc}")
        sys.exit(1)

    print(f"\n🤔 Generating ideas for '{niche}' on {platform_name}...\n")
    logger.info("CLI run started")

    try:
        ideas = run_planner(niche, platform_name, audience)
        print("\n" + "=" * 40)
        print("✅ Here are your 5 content ideas:\n")
        print(ideas)

        chosen = input("\nType the title of the idea you want to turn into a script: ").strip()
        if not chosen:
            print("No idea selected. Exiting.")
            sys.exit(0)

        length = input(
            "Video length? (1=30s, 2=60s, 3=3min, 4=10min, 5=20min) [default=2]: "
        ).strip() or "2"
        lengths = {
            "1": "30 seconds (~75 words)",
            "2": "60 seconds (~150 words)",
            "3": "3 minutes (~450 words)",
            "4": "10 minutes (~1,500 words)",
            "5": "20 minutes (~3,000 words)",
        }
        length_name = lengths.get(length, "60 seconds (~150 words)")

        print(f"\n✍️  Writing your script for '{chosen}'...\n")
        script = run_scriptwriter(chosen, platform_name, length_name)

        print("\n" + "=" * 40)
        print("✅ Your Script:\n")
        print(script)

    except RateLimitError as e:
        print(f"\n⚠️  {e}")
        sys.exit(1)
    except NoKeyError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except crew_module.ConnectionError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        print(f"\n❌ Something went wrong. Please try again in a moment.")
        sys.exit(1)


if __name__ == "__main__":
    main()