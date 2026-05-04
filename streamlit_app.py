"""
streamlit_app.py — Premium Streamlit frontend for the Multi-Agent Research Pipeline.
"""
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config import sanitize_topic, MAX_TOPIC_LENGTH, MIN_TOPIC_LENGTH
from crew import run_crew

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic Research Pipeline",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Dark gradient background */
  .stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e2e8f0;
  }

  /* Hero title */
  .hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #7c3aed, #2563eb, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 0.4rem;
  }
  .hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-bottom: 2rem;
  }

  /* Agent card */
  .agent-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
  }
  .agent-card:hover { border-color: rgba(124,58,237,0.5); }
  .agent-card .icon { font-size: 1.4rem; margin-right: 8px; }
  .agent-card .label { font-weight: 600; font-size: 0.9rem; color: #e2e8f0; }
  .agent-card .desc  { font-size: 0.8rem; color: #94a3b8; margin-top: 2px; }

  /* Step badges in status panel */
  .step-badge {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #a78bfa;
    margin: 3px 0;
  }

  /* Report container */
  .report-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1.5rem;
  }

  /* Metric cards */
  .metric-row { display: flex; gap: 12px; margin: 1.2rem 0; }
  .metric-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
  }
  .metric-card .val { font-size: 1.5rem; font-weight: 700; color: #a78bfa; }
  .metric-card .key { font-size: 0.78rem; color: #64748b; margin-top: 2px; }

  /* Primary button override */
  div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    color: white !important;
    transition: opacity 0.2s !important;
  }
  div.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: rgba(15,15,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
  }
  section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

  /* Input */
  .stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.15) !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Research Pipeline")
    st.markdown("<span style='color:#64748b;font-size:0.82rem'>Powered by CrewAI + Groq</span>", unsafe_allow_html=True)
    st.divider()

    st.markdown("#### Agent Team")
    agents = [
        ("🧠", "Research Planner",  "Decomposes topic into 3 sub-questions"),
        ("🔎", "Web Researcher",    "Searches & synthesises web findings"),
        ("⚖️", "Research Critic",   "Identifies gaps and biases"),
        ("✍️", "Report Writer",     "Writes the final markdown report"),
    ]
    for icon, name, desc in agents:
        st.markdown(f"""
        <div class="agent-card">
          <span class="icon">{icon}</span><span class="label">{name}</span>
          <div class="desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Architecture")
    st.markdown("""
    <span style='color:#94a3b8;font-size:0.83rem'>
    Sequential process — each agent hands off to the next,
    producing a structured research report end-to-end.
    </span>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Tech Stack")
    cols = st.columns(2)
    with cols[0]:
        st.markdown("<span style='font-size:0.82rem;color:#a78bfa'>⚡ CrewAI</span>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:0.82rem;color:#a78bfa'>🦙 Groq LLM</span>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<span style='font-size:0.82rem;color:#a78bfa'>🦆 DuckDuckGo</span>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:0.82rem;color:#a78bfa'>🐍 Python</span>", unsafe_allow_html=True)

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Multi-Agent Research Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Enter any research topic and watch four specialised AI agents collaborate to produce a structured, cited report — in minutes.</div>', unsafe_allow_html=True)

# ─── Input Form ──────────────────────────────────────────────────────────────
with st.form("research_form", clear_on_submit=False):
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  The impact of large language models on software engineering",
        max_chars=MAX_TOPIC_LENGTH,
        help=f"Between {MIN_TOPIC_LENGTH} and {MAX_TOPIC_LENGTH} characters.",
    )
    submitted = st.form_submit_button("🚀  Run Research Pipeline", type="primary", use_container_width=True)

# ─── Execution ───────────────────────────────────────────────────────────────
if submitted:
    # Validate input
    try:
        clean_topic = sanitize_topic(topic)
    except ValueError as ve:
        st.error(f"⚠️ {ve}")
        st.stop()

    # Pipeline steps displayed in real time
    steps = [
        ("🧠", "Planner",     "Formulating 3 research questions…"),
        ("🔎", "Researcher",  "Searching the web for findings…"),
        ("⚖️", "Critic",      "Identifying gaps and weaknesses…"),
        ("✍️", "Writer",      "Synthesising the final report…"),
    ]

    start_time = time.time()

    with st.status("🚀  Agentic pipeline running…", expanded=True) as status:
        for icon, role, msg in steps:
            st.markdown(f'<span class="step-badge">{icon} {role} — {msg}</span>', unsafe_allow_html=True)

        try:
            result = run_crew(clean_topic)
            elapsed = round(time.time() - start_time, 1)
            status.update(label=f"✅  Research complete in {elapsed}s", state="complete", expanded=False)
        except EnvironmentError as env_err:
            status.update(label="❌  Configuration error", state="error")
            st.error(f"**Missing API key:** {env_err}")
            st.info("Add your keys to `.env` and restart the app.")
            st.stop()
        except ValueError as val_err:
            status.update(label="❌  Invalid input", state="error")
            st.error(str(val_err))
            st.stop()
        except Exception as exc:
            status.update(label="❌  Pipeline failed", state="error")
            st.error(f"**Unexpected error:** {exc}")
            st.stop()

    # ─── Metrics Row ─────────────────────────────────────────────────────────
    word_count  = len(str(result).split())
    agent_count = 4
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="val">{agent_count}</div><div class="key">Agents Collaborated</div></div>
      <div class="metric-card"><div class="val">{elapsed}s</div><div class="key">Total Run Time</div></div>
      <div class="metric-card"><div class="val">{word_count}</div><div class="key">Words Generated</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ─── Report Display ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📄 Research Report")
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(str(result))
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Download ─────────────────────────────────────────────────────────────
    st.download_button(
        label="💾  Download Report as Markdown",
        data=str(result),
        file_name=f"{clean_topic.replace(' ', '_').lower()}_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.caption("Report also saved locally to the `reports/` directory.")