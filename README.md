# Pistelle AI — Content Intelligence Suite

> Turn ideas into ready-to-film scripts, SEO-optimised blogs, and viral hooks in minutes. Powered by Google Gemini, running 100% locally on your own computer.

---

## What's Inside

Six AI-powered tools in a single clean interface:

| Tool | What it does |
|---|---|
| **Video Script Generator** | Research a niche → pick a top idea → get a production-ready script |
| **SEO Blog Writer** | Full blog posts optimised for search, written in your chosen tone |
| **Website Copywriter** | Conversion-focused copy for landing pages and product pages |
| **Product Description** | Compelling product listings for any platform |
| **Viral Hook Generator** | Stop-the-scroll opening lines for any platform |
| **Tone Rewriter** | Paste any text, pick a tone, get an instant rewrite |

---

## Setup (5 minutes, one time only)

### Step 1 — Install Python

Python powers the backend of this app.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Download the latest version and run the installer
3. ⚠️ **Windows only:** tick **"Add Python to PATH"** before clicking Install

### Step 2 — Launch the App

**Windows:** Double-click **`run.bat`**

**Mac / Linux:** Open Terminal, drag `run.sh` into the window and press Enter

The launcher will automatically install all dependencies on first run (takes 1–2 minutes). Once ready, the app opens in your browser automatically.

### Step 3 — Get Your Free API Key

When the app opens for the first time, it will ask for a Gemini API key.

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with any Google account
3. Click **"Create API Key"**
4. Copy the key (it starts with `AIza...`)
5. Paste it into the Setup screen and click **Save & Start**

Your key is saved on your own computer only — it never leaves your machine.

### Step 4 — Start Creating

Every future session: just double-click `run.bat` (Windows) or run `run.sh` (Mac).

---

## How to Use Each Tool

### Video Script Generator
1. Select your **Platform** (YouTube, TikTok, Instagram, etc.)
2. Enter your **Niche / Topic** and **Target Audience**
3. Click **Generate Ideas** — the AI suggests 5 ranked video concepts
4. Pick the idea you like, then click **Write Script**

### SEO Blog Writer
Enter your topic, target audience, preferred tone, word-count range, and optional keywords. Click **Write Blog Post** for a fully structured, SEO-ready article.

### Website Copywriter
Describe your product, your audience, your tone, and your unique selling point. Returns a full landing-page copy block ready to publish.

### Product Description
Enter the product name, category, key features, target buyer, and the platform you're selling on (Amazon, Shopify, Etsy, etc.).

### Viral Hook Generator
Pick your platform, enter your topic and audience, choose a hook style, and get scroll-stopping opening lines.

### Tone Rewriter
Paste any existing text, pick a target tone (Professional, Casual, Persuasive, etc.), and get an instant rewrite that keeps your meaning.

---

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| "Python is not installed" | Python missing | Install from python.org, tick "Add to PATH" |
| "Your Python version is too old" | Python < 3.9 | Download Python 3.11+ |
| "Something went wrong during setup" | Network error | Check internet, relaunch run.bat |
| Setup screen asking for API key | First launch | Follow Step 3 above |
| "API key invalid" | Wrong or expired key | Create a fresh key at aistudio.google.com/apikey |
| "Free tier limit hit" | Too many requests | Wait 60 seconds, try again |
| Browser shows blank page | Server not ready | Wait 3 seconds and refresh |
| Nothing happens on double-click | Python not in PATH | Reinstall Python with "Add to PATH" ticked |

---

## File Structure

```
run.bat              <- Launch on Windows (double-click this)
run.sh               <- Launch on Mac / Linux
api.py               <- FastAPI backend (serves the app + API)
crew.py              <- AI agent orchestration
agents.py            <- Agent definitions
tasks.py             <- Task definitions for each agent
tools.py             <- Shared utilities
config.py            <- API key management
requirements.txt     <- Python dependencies
frontend/            <- React web interface source
  dist/              <- Pre-built app (served automatically by api.py)
guide/               <- Bonus content
  creator_guide.md   <- Full content strategy playbook
```

---

## FAQ

**Is this really free?**
Yes. Google Gemini Flash is free with no credit card required. You just need a Google account.

**Does it use my internet?**
Yes — it connects to Google's AI servers to generate content. No data is stored beyond what Google's API logs.

**Can I use this offline?**
No — an internet connection is required to reach the Gemini API.

**Can I share this with others?**
Each person needs to run it on their own computer with their own free API key.

**Can I customise the AI's style?**
Yes. The agent prompts are in `agents.py` and `tasks.py` — edit them to adjust tone, length, or format.

---

## Privacy & Data

- Your API key is stored locally in a `.env` file on your computer only
- No usage data, scripts, or content is collected by Pistelle AI
- All processing happens via direct calls between your computer and Google's Gemini API
- See Google's privacy policy for how Gemini handles API requests: https://policies.google.com/privacy
