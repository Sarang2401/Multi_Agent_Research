"""
streamlit_app.py — Social Media Script Generator
A friendly tool that helps content creators go from blank page to ready-to-film script.
"""
import time
import threading
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# ─── Load .env before anything else ──────────────────────────────────────────
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Social Media Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── Page background ── */
  .stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 60%, #0f172a 100%);
    color: #f1f5f9;
    min-height: 100vh;
  }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
  }
  .hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed33, #3b82f633);
    border: 1px solid #7c3aed55;
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #a78bfa;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
  }
  .hero-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    background: linear-gradient(135deg, #f8fafc 0%, #a78bfa 60%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 1rem;
  }
  .hero-sub {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 600px;
    margin: 0 auto 1.5rem;
    line-height: 1.7;
  }

  /* ── Step cards ── */
  .step-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s;
  }
  .step-card:hover { border-color: #7c3aed55; }
  .step-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #7c3aed;
    margin-bottom: 0.4rem;
  }

  /* ── Idea cards ── */
  .idea-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .idea-card:hover {
    border-color: #7c3aed;
    background: rgba(124, 58, 237, 0.1);
    transform: translateX(4px);
  }
  .idea-rank {
    font-size: 0.75rem;
    font-weight: 700;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
  }
  .idea-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
  }
  .idea-hook {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.5;
  }

  /* ── Script output ── */
  .script-box {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 2.5rem;
    line-height: 1.8;
    font-size: 1rem;
    color: #e2e8f0;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  }
  .script-box h2 {
    color: #a78bfa;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* ── Setup screen ── */
  .setup-card {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 3rem;
    max-width: 560px;
    margin: 3rem auto;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  }
  .setup-icon { font-size: 3rem; margin-bottom: 1rem; }
  .setup-title { font-size: 1.7rem; font-weight: 700; margin-bottom: 0.8rem; color: #f1f5f9; }
  .setup-desc { color: #94a3b8; font-size: 1rem; line-height: 1.7; margin-bottom: 1.5rem; }
  .setup-link {
    color: #a78bfa;
    text-decoration: none;
    font-weight: 600;
  }

  /* ── Platform chips ── */
  div[data-testid="stHorizontalBlock"] label {
    cursor: pointer;
  }

  /* ── Buttons ── */
  div.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
    color: white !important;
    transition: opacity 0.2s !important;
  }
  div.stButton > button:hover { opacity: 0.88 !important; }

  /* ── Alerts ── */
  .friendly-warning {
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid #f59e0b44;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #fcd34d;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0.75rem 0;
  }
  .friendly-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #ef444444;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0.75rem 0;
  }
  .friendly-info {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid #6366f144;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #a5b4fc;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0.75rem 0;
  }

  /* ── Progress ── */
  .progress-text {
    text-align: center;
    color: #94a3b8;
    font-size: 0.95rem;
    padding: 0.5rem 0;
  }

  /* ── Divider ── */
  hr { border-color: #1e293b !important; margin: 2rem 0; }

  /* ── Streamlit overrides ── */
  .stTextInput > label, .stSelectbox > label, .stRadio > label,
  .stTextArea > label { color: #cbd5e1 !important; font-weight: 500 !important; }
  .stTextInput input, .stTextArea textarea {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px #7c3aed22 !important;
  }
  [data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def show_friendly_error(msg: str):
    st.markdown(f'<div class="friendly-error">❌ {msg}</div>', unsafe_allow_html=True)

def show_friendly_warning(msg: str):
    st.markdown(f'<div class="friendly-warning">⚠️ {msg}</div>', unsafe_allow_html=True)

def show_friendly_info(msg: str):
    st.markdown(f'<div class="friendly-info">ℹ️ {msg}</div>', unsafe_allow_html=True)


# ─── Rate-limit countdown helper ─────────────────────────────────────────────

def rate_limit_countdown(seconds: int = 60):
    """Show a live countdown when the free tier limit is hit."""
    placeholder = st.empty()
    for remaining in range(seconds, 0, -1):
        placeholder.markdown(
            f'<div class="friendly-warning">⏳ Free tier limit reached — '
            f'you can try again in <strong>{remaining}s</strong>. '
            f'Just relax for a moment!</div>',
            unsafe_allow_html=True
        )
        time.sleep(1)
    placeholder.empty()


# ─── First-run API Key Setup Screen ──────────────────────────────────────────

def show_setup_screen():
    """
    Shown when no API key is detected.
    Non-technical, step-by-step, no jargon.
    """
    # Centered layout
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="setup-card">
          <div class="setup-icon">🔑</div>
          <div class="setup-title">Welcome! One quick setup step.</div>
          <div class="setup-desc">
            This app uses Google's free AI to write your scripts.
            You just need a free <strong>Gemini API key</strong> — no credit card,
            no subscription. Takes about 30 seconds to get one.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### How to get your free key:")
        st.markdown(
            "1. Click this link → **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**"
        )
        st.markdown("2. Sign in with any Google account (Gmail works fine)")
        st.markdown('3. Click **"Create API Key"**')
        st.markdown("4. Copy the key it shows you (it starts with `AIza...`)")
        st.markdown("5. Paste it in the box below and click **Save & Start**")

        st.markdown("---")

        key_input = st.text_input(
            "Paste your API key here:",
            type="password",
            placeholder="AIzaSy...",
            help="Your key is saved on your own computer only — it never leaves your machine.",
        )

        if st.button("✅ Save & Start", use_container_width=True):
            if not key_input.strip():
                show_friendly_error("Please paste your key before clicking Save.")
            elif not key_input.strip().startswith("AIza"):
                show_friendly_error(
                    "That doesn't look like a valid key — it should start with 'AIza'. "
                    "Make sure you copied the whole thing."
                )
            else:
                from config import save_api_key
                save_api_key(key_input.strip())
                st.success("Key saved! Starting the app now...")
                time.sleep(1)
                st.rerun()

        show_friendly_info(
            "Your key is stored only on your own computer in a file called '.env'. "
            "It is never sent anywhere except directly to Google's servers when generating content."
        )


# ─── Main App ────────────────────────────────────────────────────────────────

def show_main_app():
    """The main two-step creator flow."""

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🎬 Powered by Google Gemini AI — Free to use</div>
      <div class="hero-title">Social Media Script Generator</div>
      <div class="hero-sub">
        Go from blank page to ready-to-film script in minutes.
        Pick your platform, describe your channel, and let AI do the heavy lifting.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Determine which step to show ─────────────────────────────────────────
    if "ideas_result" not in st.session_state:
        st.session_state.ideas_result = None
    if "chosen_idea" not in st.session_state:
        st.session_state.chosen_idea = None
    if "script_result" not in st.session_state:
        st.session_state.script_result = None
    if "current_platform" not in st.session_state:
        st.session_state.current_platform = None

    # ── STEP 1: Generate Ideas ────────────────────────────────────────────────
    if st.session_state.ideas_result is None:
        _show_step1()
    elif st.session_state.chosen_idea is None:
        _show_idea_picker()
    else:
        _show_step2_and_script()


def _show_step1():
    """Step 1: Platform + niche + audience → generate ideas."""
    _, col, _ = st.columns([0.5, 5, 0.5])
    with col:
        st.markdown('<div class="step-label">Step 1 of 2 — What are you making?</div>', unsafe_allow_html=True)

        # Platform selector
        platform = st.radio(
            "Which platform is this video for?",
            options=["YouTube Long-Form", "YouTube Shorts", "Instagram Reels", "TikTok"],
            horizontal=True,
            index=0,
        )

        # Niche
        niche = st.text_input(
            "What's your channel about?",
            placeholder="e.g. budget travel in Southeast Asia, home workouts for busy mums, personal finance for Gen Z",
            max_chars=300,
        )

        # Audience
        audience = st.text_area(
            "Who watches your videos? (describe them in a few words)",
            placeholder="e.g. people in their 20s–30s who want to travel more but think they can't afford it",
            max_chars=300,
            height=100,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✨ Generate 5 Video Ideas", use_container_width=True):
            if not niche.strip():
                show_friendly_error("Please tell us what your channel is about before continuing.")
                return
            if not audience.strip():
                show_friendly_error("Please describe who your audience is before continuing.")
                return

            _run_planner_with_ui(niche.strip(), platform, audience.strip())


def _run_planner_with_ui(niche: str, platform: str, audience: str):
    """Call run_planner() and handle all error cases with friendly messages."""
    from crew import run_planner, RateLimitError, NoKeyError
    import crew as crew_module

    with st.spinner("🤔 Thinking up your best content ideas..."):
        try:
            result = run_planner(niche, platform, audience)
            st.session_state.ideas_result = result
            st.session_state.current_platform = platform
            st.rerun()

        except RateLimitError as e:
            show_friendly_warning(str(e))
            rate_limit_countdown(60)
            st.rerun()

        except NoKeyError:
            show_friendly_error(
                "Your API key didn't work. Please click 'Clear Key & Re-enter' below to paste it again, "
                "or get a new one at aistudio.google.com/apikey"
            )
            if st.button("🔑 Clear Key & Re-enter"):
                from config import save_api_key
                save_api_key("")
                st.rerun()

        except crew_module.ConnectionError:
            show_friendly_error(
                "Couldn't connect to the internet. Please check your Wi-Fi or data connection and try again."
            )

        except ValueError as ve:
            show_friendly_error(str(ve))

        except Exception as exc:
            show_friendly_error(
                "Something went wrong. Please try again in a moment — if it keeps happening, "
                "restart the app by closing the browser tab and double-clicking the launcher again."
            )


def _show_idea_picker():
    """Show the 5 generated ideas and let the user pick one."""
    _, col, _ = st.columns([0.5, 5, 0.5])
    with col:
        st.markdown('<div class="step-label">Choose an idea to turn into a full script</div>', unsafe_allow_html=True)
        st.markdown("Here are your 5 content ideas, ranked from best to good. Pick the one that feels right for you:")

        st.markdown("<br>", unsafe_allow_html=True)

        # Show the raw AI output as styled markdown
        st.markdown(
            f'<div class="script-box">{st.session_state.ideas_result}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Type the title of the idea you want to use as your script:**")

        chosen = st.text_input(
            "Your chosen idea:",
            placeholder="Copy and paste the video title from above, or type what you'd like to make",
            max_chars=300,
            label_visibility="collapsed",
        )

        col_back, col_go = st.columns([1, 3])
        with col_back:
            if st.button("← Start Over", use_container_width=True):
                st.session_state.ideas_result = None
                st.session_state.chosen_idea = None
                st.rerun()
        with col_go:
            if st.button("✏️ Write My Script for This Idea →", use_container_width=True):
                if not chosen.strip():
                    show_friendly_error("Please type or paste the idea you'd like to use.")
                    return
                st.session_state.chosen_idea = chosen.strip()
                st.rerun()


def _show_step2_and_script():
    """Step 2: Length selector → generate script, or show existing script."""
    _, col, _ = st.columns([0.5, 5, 0.5])
    with col:
        if st.session_state.script_result is None:
            st.markdown('<div class="step-label">Step 2 of 2 — How long is your video?</div>', unsafe_allow_html=True)

            st.markdown(f"**Selected idea:** {st.session_state.chosen_idea}")
            st.markdown("<br>", unsafe_allow_html=True)

            video_length = st.radio(
                "Choose your video length:",
                options=[
                    "30 seconds (~75 words)",
                    "60 seconds (~150 words)",
                    "3 minutes (~450 words)",
                    "10 minutes (~1,500 words)",
                    "20 minutes (~3,000 words)",
                ],
                index=1,
            )

            col_back, col_go = st.columns([1, 3])
            with col_back:
                if st.button("← Back to Ideas", use_container_width=True):
                    st.session_state.chosen_idea = None
                    st.session_state.script_result = None
                    st.rerun()
            with col_go:
                if st.button("🎬 Generate My Script", use_container_width=True):
                    _run_scriptwriter_with_ui(
                        st.session_state.chosen_idea,
                        st.session_state.current_platform or "YouTube Long-Form",
                        video_length,
                    )
        else:
            _show_script_output()


def _run_scriptwriter_with_ui(idea: str, platform: str, video_length: str):
    """Call run_scriptwriter() and handle all error cases."""
    from crew import run_scriptwriter, RateLimitError, NoKeyError
    import crew as crew_module

    with st.spinner("✍️ Writing your script... This takes 30–60 seconds."):
        try:
            result = run_scriptwriter(idea, platform, video_length)
            st.session_state.script_result = result
            st.rerun()

        except RateLimitError as e:
            show_friendly_warning(str(e))
            rate_limit_countdown(60)
            st.rerun()

        except NoKeyError:
            show_friendly_error(
                "Your API key didn't work. Please restart the app and enter your key again."
            )

        except crew_module.ConnectionError:
            show_friendly_error(
                "Couldn't connect to the internet. Please check your connection and try again."
            )

        except ValueError as ve:
            show_friendly_error(str(ve))

        except Exception:
            show_friendly_error(
                "Something went wrong while writing the script. Please try again — "
                "if it keeps happening, restart the app."
            )


def _show_script_output():
    """Display the generated script with download button."""
    st.markdown("---")

    col_title, col_dl = st.columns([4, 1])
    with col_title:
        st.markdown("### 🎬 Your Video Script")
        st.caption(f"For: {st.session_state.chosen_idea}")
    with col_dl:
        safe_name = "".join(
            c if c.isalnum() or c in " -_" else "_"
            for c in (st.session_state.chosen_idea or "script")
        )[:40].strip()
        st.download_button(
            label="⬇️ Download Script",
            data=st.session_state.script_result,
            file_name=f"{safe_name.replace(' ', '_')}_script.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown(
        f'<div class="script-box">{st.session_state.script_result}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    col_new, col_redo = st.columns(2)
    with col_new:
        if st.button("🔄 Start a New Script", use_container_width=True):
            # Reset everything for a fresh run
            for key in ["ideas_result", "chosen_idea", "script_result", "current_platform"]:
                st.session_state.pop(key, None)
            st.rerun()
    with col_redo:
        if st.button("← Pick a Different Idea", use_container_width=True):
            st.session_state.chosen_idea = None
            st.session_state.script_result = None
            st.rerun()


# ─── App Entry Point ─────────────────────────────────────────────────────────

from config import is_api_key_set

if not is_api_key_set():
    show_setup_screen()
else:
    show_main_app()