"""
streamlit_app.py — Pistelle AI
Content Intelligence Suite
"""
import base64
import time
import re
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

st.set_page_config(
    page_title="Pistelle AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_logo_b64() -> str:
    p = Path(__file__).parent / "pistelle_logo.jpg"
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return ""


LOGO_B64 = get_logo_b64()
LOGO_IMG = (
    f'<img src="data:image/jpeg;base64,{LOGO_B64}" '
    f'style="height:22px;width:auto;display:block;" alt="Pistelle AI">'
    if LOGO_B64 else ""
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Tokens ── */
:root {
  --bg:       #0e0e0e;
  --surface:  #161616;
  --raised:   #1c1c1c;
  --border:   #2a2a2a;
  --border2:  #353535;
  --t1:       #ebebeb;
  --t2:       #888;
  --t3:       #444;
  --green:    #3fb950;
  --radius:   7px;
  --f:        'Inter', system-ui, -apple-system, sans-serif;
}

/* ── Base ── */
html, body, [class*="css"] {
  font-family: var(--f) !important;
  font-size: 14px;
}
.stApp { background: var(--bg); color: var(--t1); }

/* ── Kill Streamlit chrome ── */
#MainMenu, footer, header { display: none !important; visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.st-emotion-cache-18ni7ap { display: none !important; }  /* top bar */
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar shell ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 240px !important;
  max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
  display: flex;
  flex-direction: column;
}

/* ── Sidebar brand ── */
.sb-top {
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--border);
}
.sb-logo-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 3px;
}
.sb-wordmark {
  font-size: 13px;
  font-weight: 600;
  color: var(--t1);
  letter-spacing: -0.01em;
}
.sb-tagline {
  font-size: 11px;
  color: var(--t3);
  padding-left: 30px;
}

/* ── Engine status ── */
.sb-status {
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
}
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  color: var(--t2);
  font-weight: 500;
}
.dot-green {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--green);
  flex-shrink: 0;
}

/* ── Sidebar nav section label ── */
.sb-nav-label {
  padding: 14px 16px 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--t3);
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

/* ── Override the Streamlit radio widget in sidebar ── */
/* Hide the stray label Streamlit renders for the radio group */
[data-testid="stSidebar"] [data-testid="stRadio"] > div:first-child > label {
  display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] {
  padding: 0 8px 8px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: 2px !important;
}
/* Nav item rows */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 7px 10px !important;
  border-radius: 6px !important;
  cursor: pointer !important;
  transition: background 0.12s !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: var(--raised) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
  font-size: 13.5px !important;
  color: var(--t2) !important;
  font-weight: 400 !important;
  margin: 0 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

/* ── Sidebar trust section ── */
.sb-trust {
  padding: 14px 16px;
  border-top: 1px solid var(--border);
  margin-top: auto;
}
.sb-trust-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11.5px;
  color: var(--t3);
  padding: 3px 0;
}
.sb-trust-item .ok { color: var(--green); font-size: 10px; }

/* ── Main container ── */
.block-container {
  max-width: 820px !important;
  padding: 36px 40px 60px !important;
}

/* ── Page heading ── */
.pg-h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--t1);
  letter-spacing: -0.02em;
  margin: 0 0 5px;
  line-height: 1.3;
}
.pg-lead {
  font-size: 13.5px;
  color: var(--t2);
  margin: 0 0 28px;
  line-height: 1.55;
}
.page-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 0 0 28px;
}

/* ── Breadcrumb ── */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--t3);
  margin-bottom: 24px;
  font-weight: 500;
}
.breadcrumb .active { color: var(--t2); }
.breadcrumb .sep { color: var(--border2); }

/* ── Field labels — main content only, not sidebar ── */
.block-container .stTextInput label,
.block-container .stTextArea label,
.block-container .stSelectbox label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: var(--t3) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
  margin-bottom: 6px !important;
}
/* Main content radio label (e.g. duration picker) */
.block-container .stRadio > label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: var(--t3) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}

/* ── Inputs ── */
.stTextInput input,
.stTextArea textarea {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  color: var(--t1) !important;
  font-size: 14px !important;
  font-family: var(--f) !important;
  padding: 9px 12px !important;
  transition: border-color 0.15s !important;
  box-shadow: none !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color: #555 !important;
  box-shadow: none !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: var(--t3) !important; }

/* ── Select ── */
.stSelectbox > div > div {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  color: var(--t1) !important;
  font-size: 14px !important;
}

/* ── Radio (main content area) ── */
.stRadio > div { gap: 4px !important; }
.stRadio label {
  display: flex !important;
  align-items: center !important;
  padding: 5px 0 !important;
  font-size: 13.5px !important;
  color: var(--t1) !important;
}

/* ── Buttons — use attribute selectors for higher specificity ── */
/* Targets the BaseWeb button element Streamlit renders */
.stButton button,
.stButton button[data-baseweb],
button[kind="primary"],
button[kind="secondary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
  background: #e8e8e8 !important;
  color: #111111 !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  font-family: var(--f) !important;
  padding: 9px 20px !important;
  letter-spacing: -0.01em !important;
  box-shadow: none !important;
  cursor: pointer !important;
  transition: background 0.15s !important;
}
.stButton button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
  background: #d2d2d2 !important;
  color: #111111 !important;
  transform: none !important;
  box-shadow: none !important;
  border: none !important;
}
/* Back / secondary buttons that should be ghost ── */
div.stButton > button[data-testid*="back"],
.back-btn div.stButton > button {
  background: transparent !important;
  color: var(--t2) !important;
  border: 1px solid var(--border2) !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] button {
  background: transparent !important;
  color: var(--t2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  box-shadow: none !important;
}
div[data-testid="stDownloadButton"] button:hover {
  border-color: #555 !important;
  color: var(--t1) !important;
  opacity: 1 !important;
  transform: none !important;
  box-shadow: none !important;
}

/* ── Horizontal field group card ── */
.field-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 20px;
}
.field-card-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--t3);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin-bottom: 16px;
}

/* ── Stat strip ── */
.stat-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 24px;
  background: var(--border);
  gap: 1px;
}
.stat-cell {
  background: var(--surface);
  padding: 14px 16px;
}
.stat-k {
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--t3);
  margin-bottom: 4px;
}
.stat-v {
  font-size: 14px;
  font-weight: 600;
  color: var(--t1);
}
.stat-v-ok { color: var(--green); }

/* ── Output block ── */
.output-block {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 28px 32px;
  font-size: 14.5px;
  line-height: 1.9;
  color: #c8c8c8;
  white-space: pre-wrap;
  font-family: var(--f);
}

/* ── Setup card ── */
.setup-wrap {
  max-width: 420px;
  margin: 0 auto;
  padding-top: 48px;
}
.setup-brand {
  margin-bottom: 28px;
}
.setup-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 28px 24px;
  margin-bottom: 16px;
}
.setup-card h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--t1);
  letter-spacing: -0.02em;
  margin: 0 0 8px;
}
.setup-card p {
  font-size: 13.5px;
  color: var(--t2);
  line-height: 1.6;
  margin: 0;
}
.setup-trust {
  border-top: 1px solid var(--border);
  padding-top: 16px;
  margin-top: 16px;
}
.setup-trust-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: var(--t2);
  padding: 5px 0;
}
.setup-trust-item .ok { color: var(--green); font-size: 11px; }

/* ── Alerts ── */
.stAlert { border-radius: var(--radius) !important; font-size: 13px !important; }

/* ── Expander ── */
summary { font-size: 13.5px !important; color: var(--t2) !important; }
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--t2) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def err(m):  st.error(m)
def warn(m): st.warning(m)

def countdown(secs=60):
    ph = st.empty()
    for r in range(secs, 0, -1):
        ph.warning(f"Rate limit — retrying in {r}s")
        time.sleep(1)
    ph.empty()

def wc(text): return len(re.findall(r'\w+', text))
def rt(n):
    s = int((n / 140) * 60)
    return f"~{s}s" if s < 60 else f"~{round(s/60,1)} min"


# ─── Setup screen ─────────────────────────────────────────────────────────────

def show_setup():
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown('<div class="setup-wrap">', unsafe_allow_html=True)

        if LOGO_B64:
            st.markdown(f'<div class="setup-brand">{LOGO_IMG}</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="setup-card">
          <h2>Connect your AI engine</h2>
          <p>Pistelle AI runs on your machine using the free Gemini API. 
             No subscription, no data leaves your device.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("How to get a free API key"):
            st.markdown("""
1. Open **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with any Google account
3. Click **Create API Key**
4. Copy the key — it starts with `AIzaSy…`
""")

        key = st.text_input(
            "API key",
            type="password",
            placeholder="AIzaSy…",
            label_visibility="collapsed",
        )
        if st.button("Connect", use_container_width=True):
            if not key.strip():
                err("Paste your API key above.")
            elif not key.strip().startswith("AIza"):
                err("A Gemini key starts with 'AIza'.")
            else:
                from config import save_api_key
                save_api_key(key.strip())
                st.success("Connected — loading workspace…")
                time.sleep(0.8)
                st.rerun()

        st.markdown("""
        <div class="setup-trust">
          <div class="setup-trust-item"><span class="ok">✓</span> Key stored in <code>.env</code> on this machine only</div>
          <div class="setup-trust-item"><span class="ok">✓</span> No platform fees — free Gemini tier</div>
          <div class="setup-trust-item"><span class="ok">✓</span> Your PC calls the Google AI API directly</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-top">
          <div class="sb-logo-row">
            {LOGO_IMG}
            <span class="sb-wordmark">Pistelle AI</span>
          </div>
          <div class="sb-tagline">Content Intelligence Suite</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sb-status">
          <span class="status-badge">
            <span class="dot-green"></span>Gemini Flash · Active
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-nav-label">Tools</div>', unsafe_allow_html=True)

        view = st.radio(
            "",
            [
                "Video Script Generator",
                "SEO Blog Writer",
                "Website Copywriter",
                "Product Description",
                "Viral Hook Generator",
                "Tone Rewriter",
                "Session History",
                "Settings",
            ],
            label_visibility="hidden",
        )

        st.markdown("<br>" * 2, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-trust">
          <div class="sb-trust-item"><span class="ok">✓</span>&nbsp;Local execution only</div>
          <div class="sb-trust-item"><span class="ok">✓</span>&nbsp;Zero data collection</div>
        </div>
        """, unsafe_allow_html=True)

        return view


# ─── Main app ─────────────────────────────────────────────────────────────────

def main():
    view = sidebar()

    # Shared state
    for k in ["ideas", "idea", "script", "platform", "history", "blog_post", "web_copy", "prod_desc", "hooks", "rewritten_text"]:
        st.session_state.setdefault(k, None)
    if st.session_state.history is None:
        st.session_state.history = []

    if view == "Video Script Generator": show_video_script_generator()
    elif view == "SEO Blog Writer":      show_blog_writer()
    elif view == "Website Copywriter":   show_website_copy()
    elif view == "Product Description":  show_product_description()
    elif view == "Viral Hook Generator": show_hook_generator()
    elif view == "Tone Rewriter":        show_tone_rewriter()
    elif view == "Session History":      show_history()
    elif view == "Settings":             show_settings()


# ─── Tools: Video Script Generator ──────────────────────────────────────────

def show_video_script_generator():
    st.markdown('<p class="pg-h1">Video Script Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Research a niche, pick a high-potential concept, get a production-ready script.</p>', unsafe_allow_html=True)
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.ideas is None:
        _vsg_step_topic()
    elif st.session_state.idea is None:
        _vsg_step_pick()
    else:
        _vsg_step_script()

def _vsg_step_topic():
    st.markdown("""
    <div class="breadcrumb">
      <span class="active">1 · Topic</span>
      <span class="sep">/</span><span>2 · Pick idea</span>
      <span class="sep">/</span><span>3 · Script</span>
    </div>
    """, unsafe_allow_html=True)

    c_plat, _, _ = st.columns([1.2, 0.1, 1.7])
    with c_plat:
        platform = st.selectbox("Platform", ["YouTube", "YouTube Shorts", "Instagram Reels", "TikTok"])

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        niche = st.text_input("Topic / niche", placeholder="e.g. Personal finance for first-time investors")
    with c2:
        audience = st.text_area("Target audience", placeholder="e.g. Working professionals, 25–35, building passive income", height=108)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("Generate ideas →"):
        if not niche.strip() or not audience.strip():
            err("Please fill in both topic and audience.")
            return
        from crew import run_planner, RateLimitError, NoKeyError
        import crew as m
        with st.spinner("Researching…"):
            try:
                result = run_planner(niche.strip(), platform, audience.strip())
                st.session_state.ideas = result
                st.session_state.platform = platform
                st.rerun()
            except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
            except Exception as exc: err(f"Failed: {exc}")

def _vsg_step_pick():
    st.markdown("""
    <div class="breadcrumb">
      <span>1 · Topic</span><span class="sep">/</span><span class="active">2 · Pick idea</span><span class="sep">/</span><span>3 · Script</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="output-block">{st.session_state.ideas}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    chosen = st.text_input("Which concept do you want to script?", placeholder="Paste or type the concept title…")

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back"):
            st.session_state.ideas = None
            st.rerun()
    with c2:
        if st.button("Continue →", use_container_width=True):
            if chosen.strip():
                st.session_state.idea = chosen.strip()
                st.rerun()
            else: err("Enter a concept title.")

def _vsg_step_script():
    if st.session_state.script is None:
        st.markdown("""
        <div class="breadcrumb">
          <span>1 · Topic</span><span class="sep">/</span><span>2 · Pick idea</span><span class="sep">/</span><span class="active">3 · Script</span>
        </div>
        """, unsafe_allow_html=True)
        length = st.radio("Target length", ["30 s (~75 words)", "60 s (~150 words)", "3 min (~450 words)", "10 min (~1,500 words)", "20 min (~3,000 words)"], index=1)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("← Back"):
                st.session_state.idea = None
                st.rerun()
        with c2:
            if st.button("Write script →", use_container_width=True):
                from crew import run_scriptwriter, RateLimitError
                with st.spinner("Writing…"):
                    try:
                        res = run_scriptwriter(st.session_state.idea, st.session_state.platform, length)
                        st.session_state.script = res
                        _save_history("Script", st.session_state.idea, res)
                        st.rerun()
                    except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                    except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Video Script", st.session_state.script, st.session_state.idea, lambda: st.session_state.update(ideas=None, idea=None, script=None))


# ─── Tools: SEO Blog Writer ─────────────────────────────────────────────

def show_blog_writer():
    st.markdown('<p class="pg-h1">SEO Blog Writer</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Generate long-form, structured blog posts tailored for search engines and real readers.</p><hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.blog_post is None:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            topic = st.text_input("Blog topic", placeholder="e.g. 10 ways to improve website conversion rates")
            audience = st.text_input("Target reader", placeholder="e.g. Small business owners")
        with c2:
            tone = st.selectbox("Tone of voice", ["Authoritative & Professional", "Conversational & Friendly", "Educational & Simple", "Bold & Opinionated"])
            length = st.selectbox("Target length", ["Short (600 words)", "Standard (1,200 words)", "Long-form (2,500 words)"], index=1)
        
        keywords = st.text_input("Target keywords (comma separated, optional)", placeholder="e.g. conversion rate optimization, CRO tools")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Write blog post →"):
            if not topic.strip() or not audience.strip():
                err("Please fill in topic and audience.")
                return
            from crew import run_blog_writer, RateLimitError
            with st.spinner("Writing blog post…"):
                try:
                    res = run_blog_writer(topic.strip(), audience.strip(), tone, length, keywords.strip())
                    st.session_state.blog_post = res
                    _save_history("Blog Post", topic.strip(), res)
                    st.rerun()
                except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Blog Post", st.session_state.blog_post, "Blog Post", lambda: st.session_state.update(blog_post=None))


# ─── Tools: Website Copywriter ──────────────────────────────────────────

def show_website_copy():
    st.markdown('<p class="pg-h1">Website Copywriter</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Write high-converting landing page copy with a structured layout.</p><hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.web_copy is None:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            product = st.text_input("Product / Service Name", placeholder="e.g. Pistelle Analytics")
            audience = st.text_input("Target customer", placeholder="e.g. SaaS founders")
        with c2:
            tone = st.selectbox("Brand Tone", ["Modern & Confident", "Friendly & Approachable", "Luxury & Exclusive", "Direct & Punchy"])
            usp = st.text_input("Unique Selling Point", placeholder="e.g. The only tool that tracks X natively")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Write website copy →"):
            if not product.strip() or not usp.strip():
                err("Please fill in product and USP.")
                return
            from crew import run_website_copy, RateLimitError
            with st.spinner("Writing copy…"):
                try:
                    res = run_website_copy(product.strip(), audience.strip(), tone, usp.strip())
                    st.session_state.web_copy = res
                    _save_history("Website Copy", product.strip(), res)
                    st.rerun()
                except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Website Copy", st.session_state.web_copy, "Landing Page Copy", lambda: st.session_state.update(web_copy=None))


# ─── Tools: Product Description ──────────────────────────────────────────

def show_product_description():
    st.markdown('<p class="pg-h1">Product Description Writer</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Generate e-commerce descriptions that focus on benefits and drive sales.</p><hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.prod_desc is None:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            name = st.text_input("Product Name", placeholder="e.g. Lumina Desk Lamp")
            category = st.text_input("Category", placeholder="e.g. Home Office Lighting")
            platform = st.selectbox("Platform format", ["Shopify / Custom Store", "Amazon", "Etsy"])
        with c2:
            audience = st.text_input("Target Buyer", placeholder="e.g. Remote workers, designers")
            features = st.text_area("Key Features (bullet points)", placeholder="e.g. Adjustable warmth, clamp mount, 10,000 hour LED", height=108)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Write description →"):
            if not name.strip() or not features.strip():
                err("Please fill in product name and features.")
                return
            from crew import run_product_desc, RateLimitError
            with st.spinner("Writing description…"):
                try:
                    res = run_product_desc(name.strip(), category.strip(), features.strip(), audience.strip(), platform)
                    st.session_state.prod_desc = res
                    _save_history("Product Desc", name.strip(), res)
                    st.rerun()
                except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Product Description", st.session_state.prod_desc, "Description", lambda: st.session_state.update(prod_desc=None))


# ─── Tools: Viral Hook Generator ────────────────────────────────────────

def show_hook_generator():
    st.markdown('<p class="pg-h1">Viral Hook Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Generate 10 proven, scroll-stopping hooks and headlines for your content.</p><hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.hooks is None:
        topic = st.text_input("Topic", placeholder="e.g. Why most people fail at starting a newsletter")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            audience = st.text_input("Target Audience", placeholder="e.g. Aspiring creators")
        with c2:
            medium = st.selectbox("Medium", ["Twitter / X Thread", "Short-form Video (TikTok/Reels)", "LinkedIn Post", "Email Subject Line", "YouTube Title"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate hooks →"):
            if not topic.strip():
                err("Please enter a topic.")
                return
            from crew import run_hook_generator, RateLimitError
            with st.spinner("Generating hooks…"):
                try:
                    res = run_hook_generator(topic.strip(), audience.strip(), medium)
                    st.session_state.hooks = res
                    _save_history("Hooks", topic.strip()[:30]+"...", res)
                    st.rerun()
                except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Viral Hooks", st.session_state.hooks, "Hooks", lambda: st.session_state.update(hooks=None))


# ─── Tools: Tone Rewriter ──────────────────────────────────────────────

def show_tone_rewriter():
    st.markdown('<p class="pg-h1">Tone Rewriter</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Paste any text and rewrite it to perfectly match your desired tone of voice.</p><hr class="page-divider">', unsafe_allow_html=True)

    if st.session_state.rewritten_text is None:
        text = st.text_area("Original Text", placeholder="Paste the text you want to rewrite here...", height=200)
        c1, c2 = st.columns(2, gap="large")
        with c1:
            tone = st.selectbox("Target Tone", ["Professional & Formal", "Casual & Friendly", "Witty & Clever", "Persuasive & Confident", "Simple & Clear (Explain like I'm 12)"])
        with c2:
            context = st.text_input("Context (Optional)", placeholder="e.g. This is an email to my boss")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Rewrite text →"):
            if not text.strip():
                err("Please paste some text to rewrite.")
                return
            from crew import run_tone_rewriter, RateLimitError
            with st.spinner("Rewriting…"):
                try:
                    res = run_tone_rewriter(text.strip(), tone, context.strip())
                    st.session_state.rewritten_text = res
                    _save_history("Rewrite", tone, res)
                    st.rerun()
                except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
                except Exception as exc: err(f"Failed: {exc}")
    else:
        _render_output("Rewritten Text", st.session_state.rewritten_text, "Rewrite Output", lambda: st.session_state.update(rewritten_text=None))


# ─── Common Output Renderer ─────────────────────────────────────────────

def _save_history(tool: str, title: str, content: str):
    st.session_state.history.append({
        "ts": time.strftime("%d %b, %H:%M"),
        "tool": tool, "title": title,
        "content": content, "words": wc(content),
    })

def _render_output(type_str: str, text: str, safe_name: str, reset_func):
    words = wc(text)
    st.markdown(f"""
    <div class="stat-strip">
      <div class="stat-cell"><div class="stat-k">Type</div><div class="stat-v">{type_str}</div></div>
      <div class="stat-cell"><div class="stat-k">Words</div><div class="stat-v">{words:,}</div></div>
      <div class="stat-cell"><div class="stat-k">Reading Time</div><div class="stat-v">{rt(words)}</div></div>
      <div class="stat-cell"><div class="stat-k">Status</div><div class="stat-v stat-v-ok">Ready</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1: pass
    with c2:
        safe = "".join(c if c.isalnum() else "_" for c in safe_name)[:30]
        st.download_button("Download .txt", data=text, file_name=f"{safe}.txt", mime="text/plain", use_container_width=True)
    with c3:
        if st.button("Start over", use_container_width=True):
            reset_func()
            st.rerun()

    st.markdown(f'<div class="output-block">{text}</div>', unsafe_allow_html=True)


# ─── History ──────────────────────────────────────────────────────────────────

def show_history():
    st.markdown('<p class="pg-h1">Session history</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Everything generated in this session.</p><hr class="page-divider">', unsafe_allow_html=True)
    h = st.session_state.get("history", [])
    if not h:
        st.markdown("<p style='font-size:13.5px;color:var(--t3);'>Nothing yet — run a tool first.</p>", unsafe_allow_html=True)
        return
    for i, item in enumerate(reversed(h)):
        with st.expander(f"{item['tool']}  ·  {item['title']}  ·  {item['words']:,} words  ·  {item['ts']}"):
            st.download_button("Download", data=item["content"], file_name=f"output_{i+1}.txt", key=f"dh_{i}")
            st.markdown(f'<div class="output-block">{item["content"]}</div>', unsafe_allow_html=True)


# ─── Settings ─────────────────────────────────────────────────────────────────

def show_settings():
    st.markdown('<p class="pg-h1">Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="pg-lead">Manage your API credentials.</p><hr class="page-divider">', unsafe_allow_html=True)

    from config import get_api_key, save_api_key, GEMINI_MODEL
    k = get_api_key()
    masked = f"{k[:6]}···{k[-4:]}" if len(k) > 10 else "Not set"

    st.markdown(f"""
    <div class="stat-strip" style="grid-template-columns:1fr 1fr;">
      <div class="stat-cell"><div class="stat-k">Model</div><div class="stat-v" style="font-size:13px;font-family:monospace;">{GEMINI_MODEL}</div></div>
      <div class="stat-cell"><div class="stat-k">API key</div><div class="stat-v" style="font-size:13px;font-family:monospace;">{masked}</div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("sf"):
        new_key = st.text_input("New API key", type="password", placeholder="AIzaSy…")
        if st.form_submit_button("Save"):
            if not new_key.strip(): err("Enter a key.")
            elif not new_key.strip().startswith("AIza"): err("Keys start with 'AIza'.")
            else:
                save_api_key(new_key.strip())
                st.success("Saved.")
                time.sleep(0.8)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset workspace"):
        from config import save_api_key as _s
        _s("")
        st.session_state.clear()
        st.rerun()


# ─── Entry ────────────────────────────────────────────────────────────────────
from config import is_api_key_set
if not is_api_key_set(): show_setup()
else: main()
