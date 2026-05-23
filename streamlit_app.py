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
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Dark background for the entire page */
  .stApp, .stApp > header {
    background-color: #0f172a !important;
    color: #f8fafc !important;
  }

  /* Hero title */
  .hero-container {
    text-align: center;
    padding: 3rem 0 2.5rem 0;
  }
  .hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #818cf8;
    line-height: 1.2;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
  }
  .hero-sub {
    color: #94a3b8;
    font-size: 1.2rem;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* Agent card */
  .agent-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .agent-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
  }
  .agent-card .label { font-weight: 700; font-size: 1.3rem; color: #f8fafc; margin-bottom: 4px; }
  .agent-card .desc  { font-size: 1rem; color: #cbd5e1; line-height: 1.6; }

  /* Architecture Block Diagram */
  .arch-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 2rem 0;
    flex-wrap: wrap;
  }
  .arch-block {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 16px 24px;
    border-radius: 8px;
    font-weight: 600;
    color: #f8fafc;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 1.1rem;
  }
  .arch-arrow {
    color: #475569;
    font-size: 1.5rem;
    font-weight: bold;
  }

  /* Step badges in status panel */
  .step-badge {
    display: inline-block;
    background: #312e81;
    border: 1px solid #3730a3;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 0.95rem;
    font-weight: 600;
    color: #c7d2fe;
    margin: 6px 0;
  }

  /* Report container */
  .report-box {
    background: #0f172a;
    color: #f1f5f9;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 3.5rem;
    margin-top: 1rem;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
    line-height: 1.7;
    font-size: 1.05rem;
  }
  .report-box h1, .report-box h2, .report-box h3 { 
    border-bottom: 2px solid #1e293b; 
    padding-bottom: 10px; 
    margin-top: 30px; 
    font-weight: 700;
  }
  
  /* Buttons */
  div.stButton > button[kind="primary"] {
    background-color: #4f46e5 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 1.15rem !important;
    padding: 12px 28px !important;
    color: white !important;
  }
  div.stButton > button[kind="primary"]:hover { 
    background-color: #4338ca !important; 
  }
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
        ("Planner", "Strategic Architect", "Decomposes the core topic into 3 distinct, highly focused research questions. Uses a deterministic LLM for logic.", "#ec4899"),
        ("Researcher", "Deep Web Scraper", "Searches DuckDuckGo and actively scrapes full websites (via ScrapeWebsiteTool) to extract deep, factual insights.", "#06b6d4"),
        ("Critic", "Quality Assurance", "Reviews the researcher's findings to identify critical gaps, missing perspectives, and potential biases.", "#f59e0b"),
        ("Writer", "Synthesis Expert", "Compiles all findings and critiques into a polished markdown report, ensuring perfect inline academic citations.", "#10b981"),
    ]
    
    for i, (name, role, desc, color) in enumerate(agents):
        with cols[i]:
            st.markdown(f"""
            <div class="agent-card" style="border-top: 5px solid {color};">
              <div class="label">{name}</div>
              <div style="font-size:0.85rem; color:{color}; margin-bottom:12px; text-transform:uppercase; font-weight:800;">{role}</div>
              <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)

with tab_arch:
    st.markdown("### Pipeline Architecture")
    st.markdown("This pipeline utilizes a **Sequential Process** via CrewAI, designed for maximum efficiency and zero manager-overhead. Data flows strictly from left to right.")
    
    st.markdown("""
    <div class="arch-container">
      <div class="arch-block" style="border-left: 5px solid #64748b;">User Input</div>
      <div class="arch-arrow">&rarr;</div>
      <div class="arch-block" style="border-left: 5px solid #ec4899;">Planner</div>
      <div class="arch-arrow">&rarr;</div>
      <div class="arch-block" style="border-left: 5px solid #06b6d4;">Researcher</div>
      <div class="arch-arrow">&rarr;</div>
      <div class="arch-block" style="border-left: 5px solid #f59e0b;">Critic</div>
      <div class="arch-arrow">&rarr;</div>
      <div class="arch-block" style="border-left: 5px solid #10b981;">Writer</div>
      <div class="arch-arrow">&rarr;</div>
      <div class="arch-block" style="border-left: 5px solid #4f46e5;">Final Report</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
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