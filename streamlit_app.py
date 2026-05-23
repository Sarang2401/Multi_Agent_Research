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
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Hero title */
  .hero-container {
    text-align: center;
    padding: 2rem 0 2rem 0;
  }
  .hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.2;
    margin-bottom: 0.5rem;
  }
  .hero-sub {
    color: #475569;
    font-size: 1.15rem;
    max-width: 700px;
    margin: 0 auto 2.5rem auto;
  }

  @media (prefers-color-scheme: dark) {
    .hero-title { color: #f8fafc; }
    .hero-sub { color: #94a3b8; }
  }

  /* Agent card */
  .agent-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }
  .agent-card .label { font-weight: 600; font-size: 1.2rem; color: #0f172a; margin-bottom: 6px; }
  .agent-card .desc  { font-size: 0.95rem; color: #475569; line-height: 1.5; }

  @media (prefers-color-scheme: dark) {
    .agent-card {
      background: #1e293b;
      border: 1px solid #334155;
      box-shadow: none;
    }
    .agent-card .label { color: #f8fafc; }
    .agent-card .desc  { color: #cbd5e1; }
  }

  /* Architecture Box */
  .arch-box {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    color: #334155;
    font-family: monospace;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  @media (prefers-color-scheme: dark) {
    .arch-box {
      background: #0f172a;
      border-color: #334155;
      color: #94a3b8;
    }
  }

  /* Step badges in status panel */
  .step-badge {
    display: inline-block;
    background: #e0f2fe;
    border: 1px solid #bae6fd;
    border-radius: 4px;
    padding: 4px 12px;
    font-size: 0.9rem;
    font-weight: 500;
    color: #0369a1;
    margin: 4px 0;
  }

  @media (prefers-color-scheme: dark) {
    .step-badge {
      background: #0c4a6e;
      border-color: #075985;
      color: #bae6fd;
    }
  }

  /* Report container */
  .report-box {
    background: #ffffff;
    color: #1e293b;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 3rem;
    margin-top: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  }

  @media (prefers-color-scheme: dark) {
    .report-box {
      background: #1e293b;
      color: #f8fafc;
      border-color: #334155;
    }
    .report-box h1, .report-box h2, .report-box h3 { border-bottom-color: #334155; }
  }
  .report-box h1, .report-box h2, .report-box h3 { border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-top: 24px; }
  
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
  <div class="hero-title">Deep Research Intelligence</div>
  <div class="hero-sub">Enter a topic and watch four specialised AI agents autonomously plan, scrape the web, critically analyze, and write a comprehensive, cited report.</div>
</div>
""", unsafe_allow_html=True)

# ─── Main Tabs ───────────────────────────────────────────────────────────────
tab_run, tab_team, tab_arch = st.tabs(["Run Pipeline", "Meet the Agent Team", "Architecture"])

with tab_team:
    st.markdown("### The Autonomous Research Team")
    st.markdown("Four distinct agents work together in sequence. Each has a specific role, goal, and set of tools.")
    
    cols = st.columns(4)
    agents = [
        ("Planner", "Strategic Architect", "Decomposes the core topic into 3 distinct, highly focused research questions. Uses a deterministic LLM for logic."),
        ("Researcher", "Deep Web Scraper", "Searches DuckDuckGo and actively scrapes full websites (via ScrapeWebsiteTool) to extract deep, factual insights."),
        ("Critic", "Quality Assurance", "Reviews the researcher's findings to identify critical gaps, missing perspectives, and potential biases."),
        ("Writer", "Synthesis Expert", "Compiles all findings and critiques into a polished markdown report, ensuring perfect inline academic citations."),
    ]
    
    for i, (name, role, desc) in enumerate(agents):
        with cols[i]:
            st.markdown(f"""
            <div class="agent-card">
              <div class="label">{name}</div>
              <div style="font-size:0.8rem; color:#0284c7; margin-bottom:8px; text-transform:uppercase; font-weight:700;">{role}</div>
              <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)

with tab_arch:
    st.markdown("### Pipeline Architecture")
    st.markdown("This pipeline utilizes a **Sequential Process** via CrewAI, designed for maximum efficiency and zero manager-overhead. Data flows strictly from left to right.")
    
    st.markdown("""
    <div class="arch-box">
      User Input &rarr; [ Planner ] &rarr; [ Researcher ] &rarr; [ Critic ] &rarr; [ Writer ] &rarr; Final Report
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown("**LLM Engine:** Groq (Llama 3 70B)")
        st.markdown("**Agent Framework:** CrewAI")
    with cols[1]:
        st.markdown("**Tools Used:** DuckDuckGoSearchTool, ScrapeWebsiteTool")
        st.markdown("**Frontend:** Streamlit Community Cloud")

with tab_run:
    # ─── Input Form ──────────────────────────────────────────────────────────────
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            with st.form("research_form", clear_on_submit=False):
                topic = st.text_input(
                    "What would you like to research?",
                    placeholder="e.g. The impact of quantum computing on modern cryptography",
                    max_chars=MAX_TOPIC_LENGTH,
                    label_visibility="collapsed"
                )
                submitted = st.form_submit_button("Start Deep Research", type="primary", use_container_width=True)

    # ─── Execution ───────────────────────────────────────────────────────────────
    if submitted:
        # Validate input
        try:
            clean_topic = sanitize_topic(topic)
        except ValueError as ve:
            st.error(f"Error: {ve}")
            st.stop()

        # Pipeline steps displayed in real time
        steps = [
            ("Planner", "Formulating 3 strategic research questions..."),
            ("Researcher", "Searching the web and scraping full articles..."),
            ("Critic", "Reviewing findings for gaps and biases..."),
            ("Writer", "Synthesising final report with inline citations..."),
        ]

        start_time = time.time()

        st.markdown("<br><center><h3>Agentic processing started...</h3></center>", unsafe_allow_html=True)
        with st.status("Processing the pipeline in real-time...", expanded=True) as status:
            for role, msg in steps:
                st.markdown(f'<span class="step-badge">{role} &mdash; {msg}</span>', unsafe_allow_html=True)

            try:
                result = run_crew(clean_topic)
                elapsed = round(time.time() - start_time, 1)
                status.update(label=f"Research complete in {elapsed}s", state="complete", expanded=False)
            except EnvironmentError as env_err:
                status.update(label="Configuration error", state="error")
                st.error(f"**Missing API key:** {env_err}")
                st.info("Please add your GROQ_API_KEY to your Streamlit secrets.")
                st.stop()
            except ValueError as val_err:
                status.update(label="Invalid input", state="error")
                st.error(str(val_err))
                st.stop()
            except Exception as exc:
                status.update(label="Pipeline failed", state="error")
                st.error(f"**Unexpected error:** {exc}")
                st.stop()

        # ─── Report Display ───────────────────────────────────────────────────────
        st.markdown("---")
        
        # Action row
        colA, colB = st.columns([3, 1])
        with colA:
            st.markdown("### Final Research Report")
        with colB:
            st.download_button(
                label="Download as Markdown",
                data=str(result),
                file_name=f"{clean_topic.replace(' ', '_').lower()}_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
            
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(str(result))
        st.markdown('</div>', unsafe_allow_html=True)