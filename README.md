# Multi-Agent Research Pipeline

> A production-grade, multi-agent AI system that autonomously plans, researches, critiques, and writes structured research reports on any topic — powered by **CrewAI**, **Groq LLM**, and **DuckDuckGo**.

---

## 🏗️ Architecture

```
User Input → [Planner] → [Researcher] → [Critic] → [Writer] → Markdown Report
```

| Agent | Role | LLM Mode |
|---|---|---|
| 🧠 **Research Planner** | Decomposes topic into 3 precise sub-questions | Deterministic (T=0.2) |
| 🔎 **Web Researcher** | Searches web, synthesises findings with sources | Creative (T=0.7) |
| ⚖️ **Research Critic** | Identifies gaps, biases, and contradictions | Deterministic (T=0.2) |
| ✍️ **Report Writer** | Writes a polished markdown report with citations | Creative (T=0.7) |

**Process:** `Sequential` — agents execute in order with zero manager overhead, optimised for free-tier API limits.  
**Upgrade path:** Switch to `Process.hierarchical` with a paid Groq key for dynamic planning and mid-run delegation.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Sarang2401/Multi_Agent_Research.git
cd Multi_Agent_Research
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run the Streamlit app
```bash
streamlit run streamlit_app.py
```

### 5. Or run via CLI
```bash
python main.py
```

---

## ⚙️ Configuration

All settings are managed via environment variables in `.env`:

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Groq API key — [get one free](https://console.groq.com) |
| `GOOGLE_API_KEY` | Optional | Used for Google Embeddings (memory feature) |
| `LLM_MODEL` | Optional | Override LLM (default: `groq/llama-3.3-70b-versatile`) |
| `LLM_MAX_TOKENS` | Optional | Max tokens per LLM call (default: `800`) |
| `CREW_MAX_RPM` | Optional | Requests per minute throttle (default: `2`) |
| `SEARCH_MAX_RESULTS` | Optional | DuckDuckGo results per search (default: `5`) |

---

## 🔒 Security

- **No secrets in code** — all API keys loaded from `.env` via `python-dotenv`
- **Input sanitisation** — topic validated for length and injection patterns before execution
- **`.env` in `.gitignore`** — sensitive files never committed to version control
- **Graceful error handling** — all tool calls and LLM errors caught and logged without crashing

---

## 📁 Project Structure

```
Multi_Agent_Research/
├── config.py          # Centralised config, env validation, input sanitisation
├── agents.py          # Agent definitions with role-specific LLM configurations
├── tasks.py           # Task pipeline with safe filenames and output_file saving
├── crew.py            # Crew orchestration (Sequential / Hierarchical)
├── tools.py           # Custom tools: DuckDuckGoSearchTool
├── streamlit_app.py   # Premium Streamlit frontend
├── main.py            # CLI entry point
├── reports/           # Generated markdown reports (auto-created)
├── requirements.txt
├── .env.example       # Template for required environment variables
└── .gitignore
```

---

## 🧠 Key Engineering Decisions

| Decision | Rationale |
|---|---|
| `Process.sequential` | Zero manager LLM overhead; reliable within 12K TPM free-tier limit |
| `max_tokens=800` | Prevents individual calls from exceeding per-request token cap |
| `max_rpm=2` | Rate-limit throttle to avoid 429 errors across multi-agent calls |
| `output_file` on write task | Avoids tool-call JSON truncation under `max_tokens` constraints |
| Centralised `config.py` | Single source of truth; swap models/settings without touching agent code |
| Input sanitisation | Blocks prompt injection, XSS patterns, and oversized inputs |

---

## 📈 Resume / Interview Talking Points

- **Agentic AI Design**: Implemented a 4-agent sequential pipeline with role separation (Planner → Researcher → Critic → Writer), mirroring enterprise research workflows
- **Tool-Augmented Agents**: Built a custom `DuckDuckGoSearchTool` that provides real-time web data to the Researcher agent
- **LLM Configuration Tuning**: Separate deterministic and creative LLM configs to balance accuracy vs. creativity per agent role
- **Rate Limit Engineering**: Implemented `max_rpm`, `max_tokens`, and token-conscious task design to operate within free-tier API constraints
- **Production Patterns**: Input validation, structured logging, centralised config, `.env`-based secrets management, and graceful error handling

---

## 🛠️ Tech Stack

- **[CrewAI](https://crewai.com)** — Multi-agent orchestration framework
- **[Groq](https://groq.com)** — Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)** — Privacy-first web search
- **[Streamlit](https://streamlit.io)** — Interactive web frontend
- **[LiteLLM](https://litellm.ai)** — Unified LLM provider interface
- **Python 3.10+**