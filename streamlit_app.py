"""
streamlit_app.py — Social Media Script Generator
A professional, high-trust creator studio for content strategy and script writing.
"""
import time
import re
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# ─── Load .env before anything else ──────────────────────────────────────────
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Script Studio — Social Media Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS (High-Trust Professional Dark Theme) ─────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  /* Core Font & Background */
  html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }
  
  .stApp {
    background-color: #09090b;
    color: #f4f4f5;
  }

  /* Sidebar Styling */
  [data-testid="stSidebar"] {
    background-color: #121215 !important;
    border-right: 1px solid #27272a !important;
  }
  
  [data-testid="stSidebar"] .stMarkdown h1, 
  [data-testid="stSidebar"] .stMarkdown h2, 
  [data-testid="stSidebar"] .stMarkdown h3 {
    color: #f4f4f5 !important;
  }

  /* Header Bar */
  .studio-header {
    border-bottom: 1px solid #27272a;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
  }
  .studio-badge-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.75rem;
  }
  .badge-pill {
    background-color: #18181b;
    border: 1px solid #27272a;
    color: #a1a1aa;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 9999px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
  }
  .badge-pill-active {
    background-color: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #818cf8;
  }
  .studio-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f4f4f5;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0 0 0.4rem 0;
  }
  .studio-sub {
    font-size: 1rem;
    color: #a1a1aa;
    margin: 0;
  }

  /* Card Containers */
  .pro-card {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }
  .pro-card:hover {
    border-color: #3f3f46;
  }
  
  .card-header-title {
    font-size: 1rem;
    font-weight: 600;
    color: #f4f4f5;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
  }

  /* Trust Sidebar Card */
  .trust-card {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1.5rem;
  }
  .trust-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    color: #a1a1aa;
    margin-bottom: 0.5rem;
  }
  .trust-item:last-child {
    margin-bottom: 0;
  }
  .trust-icon {
    color: #34d399;
    font-size: 0.9rem;
  }

  /* Idea Items */
  .idea-box {
    background-color: #09090b;
    border: 1px solid #27272a;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
  }
  .idea-box:hover {
    border-color: #6366f1;
    background-color: rgba(99, 102, 241, 0.04);
  }
  .idea-badge {
    display: inline-block;
    background-color: rgba(99, 102, 241, 0.2);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.4);
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
  }
  .idea-headline {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f4f4f5;
    margin-bottom: 0.4rem;
  }
  .idea-rationale {
    font-size: 0.88rem;
    color: #a1a1aa;
    line-height: 1.5;
  }

  /* Teleprompter Script Preview */
  .teleprompter-container {
    background-color: #121215;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 2rem;
    font-family: 'Inter', sans-serif;
    color: #e4e4e7;
    line-height: 1.8;
    font-size: 1.02rem;
    white-space: pre-wrap;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
  }

  /* Metadata Stats Bar */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 12px;
    margin-bottom: 1.25rem;
  }
  .stat-box {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    text-align: center;
  }
  .stat-label {
    font-size: 0.72rem;
    color: #71717a;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
  .stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: #f4f4f5;
  }

  /* Form Elements Custom Styling */
  .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background-color: #09090b !important;
    border: 1px solid #27272a !important;
    border-radius: 8px !important;
    color: #f4f4f5 !important;
    font-size: 0.95rem !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 1px #6366f1 !important;
  }
  
  /* Primary Button Styling */
  div.stButton > button {
    background-color: #4f46e5 !important;
    border: 1px solid #6366f1 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.25rem !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
  }
  div.stButton > button:hover {
    background-color: #4338ca !important;
    border-color: #818cf8 !important;
    transform: translateY(-1px);
  }
  div.stButton > button:active {
    transform: translateY(0);
  }

  /* Secondary Button Styling Override */
  div[data-testid="stFormSubmitButton"] > button {
    background-color: #4f46e5 !important;
  }

  /* System Status Indicators */
  .status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #10b981;
    margin-right: 6px;
  }
  
  /* Hide standard Streamlit header & footer chrome */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ────────────────────────────────────────────────────────

def show_friendly_error(msg: str):
    st.error(f"**Error**: {msg}")

def show_friendly_warning(msg: str):
    st.warning(f"**Notice**: {msg}")

def show_friendly_info(msg: str):
    st.info(f"**Information**: {msg}")

def rate_limit_countdown(seconds: int = 60):
    """Show a live countdown when the free tier limit is hit."""
    placeholder = st.empty()
    for remaining in range(seconds, 0, -1):
        placeholder.warning(f"⏳ **Rate limit reached** — retrying in **{remaining}s**. Please wait a moment.")
        time.sleep(1)
    placeholder.empty()

def calculate_word_count(text: str) -> int:
    """Calculate word count for a script string."""
    return len(re.findall(r'\w+', text))

def estimate_read_time(word_count: int) -> str:
    """Estimate read time based on standard 130-150 wpm video pacing."""
    seconds = int((word_count / 140) * 60)
    if seconds < 60:
        return f"~{seconds} sec"
    minutes = round(seconds / 60, 1)
    return f"~{minutes} min"


# ─── First-run API Key Setup Screen ──────────────────────────────────────────

def show_setup_screen():
    """
    High-trust onboarding screen when no API key is detected.
    """
    _, col, _ = st.columns([1, 2.2, 1])
    with col:
        st.markdown("""
        <div class="pro-card" style="text-align: center; padding: 2.5rem 2rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔒</div>
            <h2 style="margin-bottom: 0.5rem; color: #f4f4f5;">Welcome to Script Studio</h2>
            <p style="color: #a1a1aa; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">
                This application runs 100% locally on your computer with zero recurring subscription fees.
                Connect your free <strong>Google Gemini API key</strong> to activate the generation engine.
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📖 Step-by-Step Instructions (Takes 30 seconds)", expanded=True):
            st.markdown("""
            1. Open Google AI Studio: **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
            2. Sign in with any Google / Gmail account.
            3. Click **"Create API Key"**.
            4. Copy the generated key string (starts with `AIzaSy...`).
            5. Paste your key below and click **Connect Engine**.
            """)

        key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Stored exclusively in your local .env file. Never transmitted to third-party servers.",
        )

        if st.button("Connect Engine & Get Started", use_container_width=True):
            if not key_input.strip():
                show_friendly_error("Please enter a valid API key.")
            elif not key_input.strip().startswith("AIza"):
                show_friendly_error("Invalid key format. Gemini API keys start with 'AIza'.")
            else:
                from config import save_api_key
                save_api_key(key_input.strip())
                st.success("API Key saved successfully! Initializing workspace...")
                time.sleep(1)
                st.rerun()

        st.markdown("""
        <div class="trust-card">
            <div class="trust-item"><span class="trust-icon">✓</span> <span><strong>Privacy Guaranteed:</strong> Key stored locally in <code>.env</code> file</span></div>
            <div class="trust-item"><span class="trust-icon">✓</span> <span><strong>Zero Platform Fees:</strong> Free Gemini API tier included</span></div>
            <div class="trust-item"><span class="trust-icon">✓</span> <span><strong>Direct Connection:</strong> PC directly calls Google AI API</span></div>
        </div>
        """, unsafe_allow_html=True)


# ─── Sidebar Component ───────────────────────────────────────────────────────

def render_sidebar():
    """Render high-trust navigation & system info sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="padding-bottom: 1rem; border-bottom: 1px solid #27272a; margin-bottom: 1.25rem;">
            <div style="font-size: 1.15rem; font-weight: 800; color: #f4f4f5; display: flex; align-items: center; gap: 8px;">
                <span>🎬 Script Studio</span>
            </div>
            <div style="font-size: 0.78rem; color: #71717a; margin-top: 2px;">
                v2.4 Pro Edition • Local Creator Suite
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Engine Status Indicator
        st.markdown("""
        <div style="background-color: #18181b; border: 1px solid #27272a; border-radius: 8px; padding: 0.75rem; margin-bottom: 1.25rem;">
            <div style="font-size: 0.72rem; color: #71717a; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px;">Engine Status</div>
            <div style="font-size: 0.88rem; font-weight: 600; color: #34d399; display: flex; align-items: center;">
                <span class="status-dot"></span> Gemini 3.6 Flash Active
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sidebar navigation menu
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #71717a; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>Navigation</div>", unsafe_allow_html=True)
        
        view_mode = st.radio(
            "Select View",
            options=["⚡ Script Generator", "📜 Session History", "⚙️ Engine Settings"],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Security & Privacy Box
        st.markdown("""
        <div class="trust-card">
            <div style="font-size: 0.78rem; font-weight: 700; color: #f4f4f5; margin-bottom: 0.5rem;">🔒 Security & Privacy</div>
            <div class="trust-item"><span class="trust-icon">✓</span> Local execution only</div>
            <div class="trust-item"><span class="trust-icon">✓</span> Zero data collection</div>
            <div class="trust-item"><span class="trust-icon">✓</span> Direct API communication</div>
        </div>
        """, unsafe_allow_html=True)

        return view_mode


# ─── Main Application Workflow ───────────────────────────────────────────────

def show_main_app():
    """Main application flow."""

    # Render Sidebar and get view selection
    view_mode = render_sidebar()

    # Session State Initialization
    if "ideas_result" not in st.session_state:
        st.session_state.ideas_result = None
    if "chosen_idea" not in st.session_state:
        st.session_state.chosen_idea = None
    if "script_result" not in st.session_state:
        st.session_state.script_result = None
    if "current_platform" not in st.session_state:
        st.session_state.current_platform = "YouTube Long-Form"
    if "history" not in st.session_state:
        st.session_state.history = []

    # Route based on Sidebar Navigation
    if view_mode == "📜 Session History":
        show_history_view()
    elif view_mode == "⚙️ Engine Settings":
        show_settings_view()
    else:
        show_workspace_view()


def show_workspace_view():
    """Main Script Studio Workspace."""
    
    # Workspace Header
    st.markdown("""
    <div class="studio-header">
        <div class="studio-badge-bar">
            <span class="badge-pill badge-pill-active">AI Script Studio</span>
            <span class="badge-pill">Local Execution</span>
            <span class="badge-pill">Zero Cloud Cost</span>
        </div>
        <h1 class="studio-title">Social Media Content & Script Studio</h1>
        <p class="studio-sub">Generate high-performing video ideas and production-ready scripts tailored for your audience.</p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow Router
    if st.session_state.ideas_result is None:
        _show_step1_inputs()
    elif st.session_state.chosen_idea is None:
        _show_idea_selection()
    else:
        _show_step2_scriptwriter()


# ─── Step 1: Input Form ──────────────────────────────────────────────────────

def _show_step1_inputs():
    """Step 1: Input parameters for content idea generation."""
    
    st.markdown("""
    <div class="pro-card">
        <div class="card-header-title">
            <span>Step 1 of 2</span> • <span>Define Content Strategy</span>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        platform = st.selectbox(
            "Target Video Platform",
            options=["YouTube Long-Form", "YouTube Shorts", "Instagram Reels", "TikTok"],
            index=0,
            help="Optimizes script structure and pacing for specific platform algorithm patterns.",
        )

        niche = st.text_input(
            "Channel Niche / Topic Area",
            placeholder="e.g. Personal Finance for Beginners, Tech Product Reviews, Minimalist Home Decor",
            max_chars=200,
            help="Describe the primary topic focus of your channel or content brand.",
        )

    with col2:
        audience = st.text_area(
            "Target Audience Profile",
            placeholder="e.g. Young professionals aged 22-30 looking to build passive income and invest smartly",
            max_chars=300,
            height=125,
            help="Specify demographics, pain points, or interests of your viewers.",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, _ = st.columns([1.5, 2.5])
    with col_btn:
        if st.button("Generate 5 Ranked Content Ideas →", use_container_width=True):
            if not niche.strip():
                show_friendly_error("Please specify your channel niche before proceeding.")
                return
            if not audience.strip():
                show_friendly_error("Please describe your target audience before proceeding.")
                return

            _execute_planner(niche.strip(), platform, audience.strip())


def _execute_planner(niche: str, platform: str, audience: str):
    """Execute Planner Agent with clean loading state."""
    from crew import run_planner, RateLimitError, NoKeyError
    import crew as crew_module

    with st.spinner("Analyzing channel niche & structuring 5 ranked content ideas..."):
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
            show_friendly_error("Invalid or missing API Key. Please update your key in Engine Settings.")

        except crew_module.ConnectionError:
            show_friendly_error("Network connection error. Please verify your internet access.")

        except Exception as exc:
            show_friendly_error(f"Generation failed: {str(exc)}")


# ─── Step 1 Output: Idea Selector ───────────────────────────────────────────

def _show_idea_selection():
    """Step 1 Results: Display ranked content ideas with direct selection options."""
    
    st.markdown("""
    <div class="pro-card">
        <div class="card-header-title">
            <span>Step 1 Results</span> • <span>Select a Content Concept to Script</span>
        </div>
        <p style="color: #a1a1aa; font-size: 0.9rem; margin-bottom: 1rem;">
            Below are 5 high-converting video concepts ranked by hook potential. Choose an idea to generate its complete script.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Render formatted raw output inside clean container
    st.markdown(f'<div class="teleprompter-container" style="margin-bottom: 1.5rem;">{st.session_state.ideas_result}</div>', unsafe_allow_html=True)

    # Input for chosen idea selection
    st.markdown("""
    <div class="pro-card">
        <div class="card-header-title">Confirm Chosen Concept</div>
    """, unsafe_allow_html=True)

    chosen = st.text_input(
        "Idea Title / Subject",
        placeholder="Paste or type the video concept title you wish to script",
        max_chars=250,
        help="You can use one of the generated ideas above or enter a modified version.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← Back to Strategy Inputs", use_container_width=True):
            st.session_state.ideas_result = None
            st.session_state.chosen_idea = None
            st.rerun()

    with col_next:
        if st.button("Proceed to Script Generation →", use_container_width=True):
            if not chosen.strip():
                show_friendly_error("Please enter or paste the idea title you want to script.")
                return
            st.session_state.chosen_idea = chosen.strip()
            st.rerun()


# ─── Step 2: Scriptwriter Studio ─────────────────────────────────────────────

def _show_step2_scriptwriter():
    """Step 2: Script length configuration and output viewer."""
    
    if st.session_state.script_result is None:
        _show_length_config_form()
    else:
        _show_completed_script_studio()


def _show_length_config_form():
    """Form to choose script duration before writing."""
    st.markdown("""
    <div class="pro-card">
        <div class="card-header-title">
            <span>Step 2 of 2</span> • <span>Script Pacing & Target Duration</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Target Concept:** `{st.session_state.chosen_idea}`")
    st.markdown(f"**Target Platform:** `{st.session_state.current_platform}`")
    st.markdown("<br>", unsafe_allow_html=True)

    video_length = st.radio(
        "Select Target Video Duration",
        options=[
            "30 seconds (~75 words)",
            "60 seconds (~150 words)",
            "3 minutes (~450 words)",
            "10 minutes (~1,500 words)",
            "20 minutes (~3,000 words)",
        ],
        index=1,
        help="Script word count will be calibrated to standard spoken dialogue speeds.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    col_b, col_g = st.columns([1, 2])
    with col_b:
        if st.button("← Select Different Idea", use_container_width=True):
            st.session_state.chosen_idea = None
            st.rerun()
    with col_g:
        if st.button("Generate Complete Script 🎬", use_container_width=True):
            _execute_scriptwriter(
                st.session_state.chosen_idea,
                st.session_state.current_platform,
                video_length,
            )


def _execute_scriptwriter(idea: str, platform: str, video_length: str):
    """Execute Scriptwriter Agent."""
    from crew import run_scriptwriter, RateLimitError, NoKeyError
    import crew as crew_module

    with st.spinner("Drafting full production script with hooks, body scenes, and calls-to-action..."):
        try:
            result = run_scriptwriter(idea, platform, video_length)
            st.session_state.script_result = result
            
            # Save to Session History
            words = calculate_word_count(result)
            st.session_state.history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                "idea": idea,
                "platform": platform,
                "script": result,
                "words": words,
            })

            st.rerun()

        except RateLimitError as e:
            show_friendly_warning(str(e))
            rate_limit_countdown(60)
            st.rerun()

        except NoKeyError:
            show_friendly_error("Invalid or missing API key.")

        except crew_module.ConnectionError:
            show_friendly_error("Connection timed out. Please check your network connection.")

        except Exception as exc:
            show_friendly_error(f"Script generation failed: {str(exc)}")


def _show_completed_script_studio():
    """Teleprompter & Script Export Workspace."""
    
    script_text = st.session_state.script_result
    word_count = calculate_word_count(script_text)
    read_time = estimate_read_time(word_count)

    # Metadata Stats Grid
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-label">Platform</div>
            <div class="stat-value">{st.session_state.current_platform}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Word Count</div>
            <div class="stat-value">{word_count} words</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Est. Duration</div>
            <div class="stat-value">{read_time}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Status</div>
            <div class="stat-value" style="color: #34d399;">Ready to Film</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar
    col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
    with col_t1:
        st.markdown(f"### 🎬 {st.session_state.chosen_idea}")
    with col_t2:
        safe_filename = "".join(c if c.isalnum() or c in " -_" else "_" for c in st.session_state.chosen_idea)[:35].strip()
        st.download_button(
            label="⬇️ Download Script (.txt)",
            data=script_text,
            file_name=f"{safe_filename.replace(' ', '_')}_script.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_t3:
        if st.button("🔄 New Script", use_container_width=True):
            st.session_state.ideas_result = None
            st.session_state.chosen_idea = None
            st.session_state.script_result = None
            st.rerun()

    # Teleprompter Output Block
    st.markdown(f'<div class="teleprompter-container">{script_text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_prev, _ = st.columns([1, 2])
    with col_prev:
        if st.button("← Back to Idea Concepts", use_container_width=True):
            st.session_state.script_result = None
            st.rerun()


# ─── Auxiliary Views ─────────────────────────────────────────────────────────

def show_history_view():
    """Display saved scripts from the current session."""
    st.markdown("""
    <div class="studio-header">
        <h1 class="studio-title">Session Script History</h1>
        <p class="studio-sub">Access scripts created during your current active session.</p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("history", [])

    if not history:
        st.info("No scripts generated in this session yet. Use the Script Generator to create your first script.")
        return

    for idx, item in enumerate(reversed(history)):
        with st.expander(f"🎬 {item['idea']} ({item['platform']} • {item['words']} words • {item['timestamp']})"):
            st.download_button(
                label="⬇️ Download This Script",
                data=item["script"],
                file_name=f"script_history_{idx+1}.txt",
                key=f"dl_hist_{idx}",
            )
            st.markdown(f'<div class="teleprompter-container">{item["script"]}</div>', unsafe_allow_html=True)


def show_settings_view():
    """Engine & API Key Settings Page."""
    st.markdown("""
    <div class="studio-header">
        <h1 class="studio-title">Engine & Security Settings</h1>
        <p class="studio-sub">Manage your local API credentials and engine parameters.</p>
    </div>
    """, unsafe_allow_html=True)

    from config import get_api_key, save_api_key, GEMINI_MODEL

    current_key = get_api_key()
    masked_key = f"{current_key[:6]}...{current_key[-4:]}" if len(current_key) > 10 else "Not Set"

    st.markdown("""
    <div class="pro-card">
        <div class="card-header-title">Active AI Model & Connection</div>
        <p style="color: #a1a1aa; font-size: 0.9rem;">
            <strong>Active Model:</strong> <code>{}</code> (Free Tier Engine)<br>
            <strong>Masked API Key:</strong> <code>{}</code>
        </p>
    </div>
    """.format(GEMINI_MODEL, masked_key), unsafe_allow_html=True)

    with st.form("settings_form"):
        st.markdown("#### Update Gemini API Key")
        new_key = st.text_input("New API Key", type="password", placeholder="AIzaSy...")
        submitted = st.form_submit_button("Save New Key")

        if submitted:
            if not new_key.strip():
                show_friendly_error("Please enter a non-empty key.")
            elif not new_key.strip().startswith("AIza"):
                show_friendly_error("Keys must start with 'AIza'.")
            else:
                save_api_key(new_key.strip())
                st.success("API key updated successfully!")
                time.sleep(1)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔴 Clear Saved Key & Reset Workspace"):
        save_api_key("")
        st.session_state.clear()
        st.rerun()


# ─── App Entry Point ─────────────────────────────────────────────────────────

from config import is_api_key_set

if not is_api_key_set():
    show_setup_screen()
else:
    show_main_app()