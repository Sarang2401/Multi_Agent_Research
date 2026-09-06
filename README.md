# Social Media Script Generator

Go from blank page to ready-to-film script in minutes. This app uses AI to generate video ideas and write complete scripts for YouTube, TikTok, and Instagram — and it runs entirely on your own computer for free.

---

## Setup (takes about 5 minutes, one time only)

### Step 1 — Install Python

Python is the software that powers this app. If you already have it, skip to Step 2.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Click the big yellow **"Download Python"** button
3. Open the downloaded file to install it
4. ⚠️ **Important (Windows):** During installation, make sure to tick the box that says **"Add Python to PATH"** before clicking Install

### Step 2 — Start the App

**On Windows:**
Double-click **`run.bat`** in this folder.

**On Mac:**
Right-click **`run.sh`** → click **"Open"** → click **"Open"** again if a warning appears.

The app will automatically set itself up (downloading what it needs), then open in your web browser. This first-time setup may take 1–2 minutes — just leave the black window open until the browser appears.

### Step 3 — Get Your Free API Key

When the app opens for the first time, it will ask you for an API key. This is what lets the app talk to Google's AI — it's completely free.

1. Click the link in the app (or go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**)
2. Sign in with any Google / Gmail account
3. Click **"Create API Key"**
4. Copy the key that appears (it starts with `AIza...`)
5. Paste it into the box in the app and click **Save & Start**

Your key is saved on your own computer — it never leaves your machine and is never shared with anyone.

### Step 4 — Start Creating!

That's it. Every time you want to use the app in the future, just double-click `run.bat` (Windows) or `run.sh` (Mac).

---

## How to Use the App

1. **Choose your platform** — YouTube Long-Form, YouTube Shorts, Instagram Reels, or TikTok
2. **Describe your channel** — e.g. *"budget travel tips for backpackers"*
3. **Describe your audience** — e.g. *"people in their 20s who want to see the world on a budget"*
4. Click **Generate 5 Video Ideas** — the AI will suggest 5 ranked ideas with hook rationale
5. **Pick the idea you like** — type or paste it into the box
6. **Choose your video length** — 30 seconds up to 20 minutes
7. Click **Write My Script** — the AI writes your full script with hook, body, CTA, and on-screen text cues
8. **Download your script** as a text file, or copy it directly

---

## If Something Goes Wrong

| What you see | What it means | What to do |
|---|---|---|
| *"Python is not installed"* | Python hasn't been installed yet | Follow Step 1 above, restart the launcher after installing |
| *"Your Python version is too old"* | You have an older Python that won't work | Download Python 3.11+ from python.org, restart launcher |
| *"Something went wrong while setting up"* | A file couldn't download | Check your internet connection, then try the launcher again |
| *"Paste your free Gemini API key here"* | The app needs your key before it can work | Follow Step 3 above |
| *"Your API key didn't work"* | The key was typed wrong, expired, or not activated yet | Go back to aistudio.google.com/apikey and create a new key |
| *"Free tier limit hit — wait a minute"* | You've used the AI a lot in a short time | Wait 60 seconds and try again — the free limit resets quickly |
| *"Couldn't connect to the internet"* | No internet connection detected | Check your Wi-Fi or cable, then try again |
| App opens but browser shows an error | Streamlit port conflict | Close the black terminal window and double-click the launcher again |
| Nothing happens when I double-click | File permissions or Python not in PATH | On Mac: right-click → Open. On Windows: reinstall Python with "Add to PATH" ticked |

---

## What's Included in This Package

```
run.bat              ← Double-click this on Windows
run.sh               ← Double-click this on Mac / Linux
streamlit_app.py     ← The visual app
requirements.txt     ← List of components (installed automatically)
config.py            ← App settings
agents.py            ← The two AI agents
tasks.py             ← What each agent does
crew.py              ← How the agents work together
tools.py             ← Supporting tools
main.py              ← Optional command-line version
```

---

## Frequently Asked Questions

**Is this really free?**
Yes. Google Gemini Flash has a free tier with no credit card required. The app itself is free. You just need a Google account to get an API key.

**Does it use my internet?**
Yes — the app connects to Google's AI servers to generate content. Your own writing/ideas are sent to Google as part of each request. No data is stored or shared beyond that.

**Can I use this offline?**
No — an internet connection is required to generate ideas and scripts.

**Can I share this with friends?**
That depends on your licence. Each person needs to run it on their own computer and get their own free API key.

**I want to change the AI's writing style. Can I?**
The agents and their instructions are in `agents.py` and `tasks.py`. If you're comfortable with text files, you can edit the prompts to adjust tone, style, or output format.