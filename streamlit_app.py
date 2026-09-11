"""
streamlit_app.py — Pistelle AI
Research & Script Intelligence Studio
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
# Design direction: Linear.app / Vercel / Raycast
# Rules: no glow, no gradients on text, no floating blobs, no neon
# Typefaces feel deliberate, spacing is tight, hierarchy is clear
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
  min-width: 220px !important;
  max-width: 220px !important;
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
  max-width: 780px !important;
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

        # Brand
        if LOGO_B64:
            st.markdown(
                f'<div class="setup-brand">{LOGO_IMG}</div>',
                unsafe_allow_html=True,
            )

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
        # Brand block
        st.markdown(f"""
        <div class="sb-top">
          <div class="sb-logo-row">
            {LOGO_IMG}
            <span class="sb-wordmark">Pistelle AI</span>
          </div>
          <div class="sb-tagline">Research &amp; Script Studio</div>
        </div>
        """, unsafe_allow_html=True)

        # Engine status
        st.markdown("""
        <div class="sb-status">
          <span class="status-badge">
            <span class="dot-green"></span>Gemini Flash · Active
          </span>
        </div>
        """, unsafe_allow_html=True)

        # Nav label
        st.markdown('<div class="sb-nav-label">Workspace</div>', unsafe_allow_html=True)

        # Nav
        view = st.radio(
            "",
            ["Script Generator", "Session History", "Settings"],
            label_visibility="hidden",
        )

        # Trust strip — placed AFTER radio, not absolutely positioned
        st.markdown("<br>" * 6, unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-trust">
          <div class="sb-trust-item"><span class="ok">✓</span>&nbsp;Local execution only</div>
          <div class="sb-trust-item"><span class="ok">✓</span>&nbsp;Zero data collection</div>
          <div class="sb-trust-item"><span class="ok">✓</span>&nbsp;Direct API communication</div>
        </div>
        """, unsafe_allow_html=True)

        return view


# ─── Main app ─────────────────────────────────────────────────────────────────

def main():
    view = sidebar()

    for k, v in {
        "ideas": None, "idea": None, "script": None,
        "platform": "YouTube", "history": [],
    }.items():
        st.session_state.setdefault(k, v)

    if   view == "Session History": show_history()
    elif view == "Settings":        show_settings()
    else:                           show_workspace()


# ─── Workspace ────────────────────────────────────────────────────────────────

def show_workspace():
    st.markdown('<p class="pg-h1">Script Generator</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="pg-lead">Research a niche, pick a high-potential concept, get a production-ready script.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    if   st.session_state.ideas  is None: step_topic()
    elif st.session_state.idea   is None: step_pick()
    else:                                  step_script()


# ── Step 1 ────────────────────────────────────────────────────────────────────

def step_topic():
    st.markdown("""
    <div class="breadcrumb">
      <span class="active">1 · Topic</span>
      <span class="sep">/</span><span>2 · Pick idea</span>
      <span class="sep">/</span><span>3 · Script</span>
    </div>
    """, unsafe_allow_html=True)

    # Narrow platform row + two-col inputs in one grid
    c_plat, _, c_blank = st.columns([1.2, 0.1, 1.7])
    with c_plat:
        platform = st.selectbox(
            "Platform",
            ["YouTube", "YouTube Shorts", "Instagram Reels", "TikTok"],
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        niche = st.text_input(
            "Topic / niche",
            placeholder="e.g. Personal finance for first-time investors",
        )
    with c2:
        audience = st.text_area(
            "Target audience",
            placeholder="e.g. Working professionals, 25–35, building passive income",
            height=108,
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if st.button("Generate ideas →"):
        if not niche.strip():
            err("Enter a topic or niche.")
            return
        if not audience.strip():
            err("Describe your target audience.")
            return
        run_planner(niche.strip(), platform, audience.strip())


def run_planner(niche, platform, audience):
    from crew import run_planner as _rp, RateLimitError, NoKeyError
    import crew as m
    with st.spinner("Researching…"):
        try:
            result = _rp(niche, platform, audience)
            st.session_state.ideas    = result
            st.session_state.platform = platform
            st.rerun()
        except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
        except NoKeyError: err("Invalid API key — update it in Settings.")
        except m.ConnectionError: err("Network error. Check your connection.")
        except Exception as exc: err(f"Failed: {exc}")


# ── Step 2 ────────────────────────────────────────────────────────────────────

def step_pick():
    st.markdown("""
    <div class="breadcrumb">
      <span>1 · Topic</span>
      <span class="sep">/</span><span class="active">2 · Pick idea</span>
      <span class="sep">/</span><span>3 · Script</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="output-block">{st.session_state.ideas}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    chosen = st.text_input(
        "Which concept do you want to script?",
        placeholder="Paste or type the concept title…",
    )

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back"):
            st.session_state.ideas = None
            st.rerun()
    with c2:
        if st.button("Continue →", use_container_width=True):
            if not chosen.strip():
                err("Enter or paste the concept title.")
                return
            st.session_state.idea = chosen.strip()
            st.rerun()


# ── Step 3 ────────────────────────────────────────────────────────────────────

def step_script():
    if st.session_state.script is None:
        step_configure()
    else:
        step_output()


def step_configure():
    st.markdown("""
    <div class="breadcrumb">
      <span>1 · Topic</span>
      <span class="sep">/</span><span>2 · Pick idea</span>
      <span class="sep">/</span><span class="active">3 · Script</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<p style="font-size:13px;color:var(--t2);margin-bottom:20px;">'
        f'Writing for: <strong style="color:var(--t1);">{st.session_state.idea}</strong>'
        f'&nbsp;·&nbsp;{st.session_state.platform}</p>',
        unsafe_allow_html=True,
    )

    length = st.radio(
        "Target length",
        ["30 s (~75 words)", "60 s (~150 words)",
         "3 min (~450 words)", "10 min (~1,500 words)", "20 min (~3,000 words)"],
        index=1,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back"):
            st.session_state.idea = None
            st.rerun()
    with c2:
        if st.button("Write script →", use_container_width=True):
            run_writer(st.session_state.idea, st.session_state.platform, length)


def run_writer(idea, platform, length):
    from crew import run_scriptwriter as _rw, RateLimitError, NoKeyError
    import crew as m
    with st.spinner("Writing…"):
        try:
            result = _rw(idea, platform, length)
            st.session_state.script = result
            st.session_state.history.append({
                "ts": time.strftime("%d %b, %H:%M"),
                "idea": idea, "platform": platform,
                "script": result, "words": wc(result),
            })
            st.rerun()
        except RateLimitError as e: warn(str(e)); countdown(); st.rerun()
        except NoKeyError: err("Invalid API key.")
        except m.ConnectionError: err("Connection timed out.")
        except Exception as exc: err(f"Failed: {exc}")


def step_output():
    txt   = st.session_state.script
    words = wc(txt)

    # Stats
    st.markdown(f"""
    <div class="stat-strip">
      <div class="stat-cell">
        <div class="stat-k">Platform</div>
        <div class="stat-v">{st.session_state.platform}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-k">Words</div>
        <div class="stat-v">{words:,}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-k">Duration</div>
        <div class="stat-v">{rt(words)}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-k">Status</div>
        <div class="stat-v stat-v-ok">Ready</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Toolbar row
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            f'<p style="font-size:14px;font-weight:600;color:var(--t1);'
            f'margin:6px 0;letter-spacing:-0.01em;">{st.session_state.idea}</p>',
            unsafe_allow_html=True,
        )
    with c2:
        safe = "".join(c if c.isalnum() or c in " -_" else "_"
                       for c in st.session_state.idea)[:35].strip()
        st.download_button(
            "Download .txt",
            data=txt,
            file_name=f"{safe.replace(' ','_')}_script.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c3:
        if st.button("Start over", use_container_width=True):
            st.session_state.update(ideas=None, idea=None, script=None)
            st.rerun()

    st.markdown(f'<div class="output-block">{txt}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Different idea"):
        st.session_state.script = None
        st.rerun()


# ─── History ──────────────────────────────────────────────────────────────────

def show_history():
    st.markdown('<p class="pg-h1">Session history</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="pg-lead">Scripts generated in this session.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    h = st.session_state.get("history", [])
    if not h:
        st.markdown(
            "<p style='font-size:13.5px;color:var(--t3);'>Nothing yet — generate your first script.</p>",
            unsafe_allow_html=True,
        )
        return

    for i, item in enumerate(reversed(h)):
        with st.expander(
            f"{item['idea']}  ·  {item['platform']}  ·  {item['words']:,} words  ·  {item['ts']}"
        ):
            st.download_button(
                "Download",
                data=item["script"],
                file_name=f"script_{i+1}.txt",
                key=f"dh_{i}",
            )
            st.markdown(
                f'<div class="output-block">{item["script"]}</div>',
                unsafe_allow_html=True,
            )


# ─── Settings ─────────────────────────────────────────────────────────────────

def show_settings():
    st.markdown('<p class="pg-h1">Settings</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="pg-lead">Manage your API credentials and engine configuration.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="page-divider">', unsafe_allow_html=True)

    from config import get_api_key, save_api_key, GEMINI_MODEL
    k = get_api_key()
    masked = f"{k[:6]}···{k[-4:]}" if len(k) > 10 else "Not set"

    st.markdown(f"""
    <div class="stat-strip" style="grid-template-columns:1fr 1fr;">
      <div class="stat-cell">
        <div class="stat-k">Model</div>
        <div class="stat-v" style="font-size:13px;font-family:monospace;">{GEMINI_MODEL}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-k">API key</div>
        <div class="stat-v" style="font-size:13px;font-family:monospace;">{masked}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("sf"):
        new_key = st.text_input("New API key", type="password", placeholder="AIzaSy…")
        if st.form_submit_button("Save"):
            if not new_key.strip():
                err("Enter a key.")
            elif not new_key.strip().startswith("AIza"):
                err("Keys start with 'AIza'.")
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
if not is_api_key_set():
    show_setup()
else:
    main()
