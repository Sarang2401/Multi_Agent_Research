"""
generate_pdf.py
Creates the "Setup Guide.pdf" that ships inside the product ZIP.
Run this before packaging: python generate_pdf.py
Requires: pip install fpdf2
"""

from fpdf import FPDF, XPos, YPos
from pathlib import Path

OUTPUT = Path(__file__).parent / "Setup Guide.pdf"

# ── Colour palette ──────────────────────────────────────────────────────────
PURPLE      = (124, 58, 237)
DARK_BG     = (15,  23,  42)
CARD_BG     = (30,  41,  59)
TEXT_MAIN   = (241, 245, 249)
TEXT_MUTED  = (148, 163, 184)
WHITE       = (255, 255, 255)
GREEN       = (34, 197, 94)
AMBER       = (245, 158, 11)


class PDF(FPDF):
    """Custom FPDF subclass with shared helpers."""

    def header(self):
        pass   # handled manually per section

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*TEXT_MUTED)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def fill_bg(self, r, g, b):
        self.set_fill_color(r, g, b)
        self.rect(0, 0, self.w, self.h, "F")

    def accent_line(self, x, y, w=180, h=0.8):
        self.set_fill_color(*PURPLE)
        self.rect(x, y, w, h, "F")

    def section_title(self, text, top_space=8):
        self.ln(top_space)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*PURPLE)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.accent_line(self.l_margin, self.get_y(), w=self.epw, h=0.5)
        self.ln(4)

    def body(self, text, size=10, bold=False, color=None):
        self.set_font("Helvetica", "B" if bold else "", size)
        self.set_text_color(*(color or TEXT_MAIN))
        self.multi_cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def step_row(self, number, title, detail):
        """Numbered step with title + detail line."""
        x = self.l_margin
        y = self.get_y()

        # Number badge
        self.set_fill_color(*PURPLE)
        self.set_draw_color(*PURPLE)
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*WHITE)
        self.cell(8, 8, str(number), border=0, fill=True, align="C",
                  new_x=XPos.RIGHT, new_y=YPos.TOP)

        # Title
        self.set_xy(x + 11, y)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT_MAIN)
        self.cell(0, 4, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Detail
        self.set_xy(x + 11, self.get_y())
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT_MUTED)
        self.multi_cell(self.epw - 11, 5, detail,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def info_box(self, text, bg=CARD_BG, text_color=TEXT_MUTED, icon=""):
        self.set_fill_color(*bg)
        self.set_draw_color(*bg)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*text_color)
        x = self.l_margin
        y = self.get_y()
        self.set_xy(x, y)
        prefix = f"{icon}  " if icon else ""
        self.multi_cell(self.epw, 6, f"{prefix}{text}",
                        border=0, fill=True, align="L",
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def table_row(self, col1, col2, col3, header=False):
        fill  = PURPLE if header else CARD_BG
        color = WHITE  if header else TEXT_MAIN
        w1, w2, w3 = 52, 58, self.epw - 110
        self.set_fill_color(*fill)
        self.set_draw_color(40, 55, 75)
        self.set_font("Helvetica", "B" if header else "", 8)
        self.set_text_color(*color)
        h = 6 if header else 8
        x = self.l_margin
        y = self.get_y()
        self.set_xy(x, y)
        self.cell(w1, h, col1, border=1, fill=True)
        self.cell(w2, h, col2, border=1, fill=True)
        self.cell(w3, h, col3, border=1, fill=True)
        self.ln()


# ── Build the PDF ────────────────────────────────────────────────────────────

def build():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(15, 15, 15)

    # ── PAGE 1: Cover ────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.fill_bg(*DARK_BG)

    # Top accent bar
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, 0, pdf.w, 6, "F")

    pdf.ln(28)

    # Badge
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*PURPLE)
    pdf.cell(0, 8, "SETUP GUIDE", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(4)

    # Main title
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*TEXT_MAIN)
    pdf.cell(0, 14, "Social Media", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*PURPLE)
    pdf.cell(0, 14, "Script Generator", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)

    # Subtitle
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.cell(0, 7, "From blank page to ready-to-film script in minutes.", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(14)
    pdf.accent_line(pdf.l_margin, pdf.get_y(), w=pdf.epw)
    pdf.ln(14)

    # What is included
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEXT_MAIN)
    pdf.cell(0, 7, "What you get", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    items = [
        ("YouTube, TikTok, Reels, Shorts", "Covers all four major platforms"),
        ("5 ranked video ideas per run",    "With hook rationale for each"),
        ("Full scripts sized to length",    "30 seconds up to 20 minutes"),
        ("On-screen text cues included",    "Ready for editing software"),
        ("Runs on your own computer",       "No monthly fee, no subscription"),
        ("Free Google AI inside",           "No credit card required"),
    ]

    for left, right in items:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*GREEN)
        pdf.cell(6, 6, "+",
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*TEXT_MAIN)
        pdf.cell(80, 6, f"  {left}",
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*TEXT_MUTED)
        pdf.cell(0, 6, right,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(16)

    # Bottom note
    pdf.set_fill_color(*CARD_BG)
    pdf.set_draw_color(*CARD_BG)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.multi_cell(pdf.epw, 6,
        "This guide walks you through the full setup in four steps. "
        "Total time: about 5 minutes, done once.",
        border=0, fill=True, align="C",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Bottom accent bar
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, pdf.h - 6, pdf.w, 6, "F")


    # ── PAGE 2: Setup Steps ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.fill_bg(*DARK_BG)
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, 0, pdf.w, 4, "F")

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*TEXT_MAIN)
    pdf.cell(0, 9, "Setup Steps", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.cell(0, 6, "Complete these four steps once. After that, just double-click to start.",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.accent_line(pdf.l_margin, pdf.get_y(), w=pdf.epw)
    pdf.ln(6)

    pdf.step_row(
        1,
        "Install Python",
        "Python is the software that runs this app. If you already have it, skip to step 2.\n"
        "1. Open your browser and go to: python.org/downloads\n"
        "2. Click the Download Python button and run the installer.\n"
        "3. Windows: tick the box that says Add Python to PATH before clicking Install.\n"
        "4. Mac: the installer walks you through everything automatically."
    )

    pdf.step_row(
        2,
        "Start the app",
        "Windows: double-click run.bat in the folder.\n"
        "Mac / Linux: right-click run.sh, click Open, then click Open again if a warning appears.\n\n"
        "The first time you run it, the app downloads its components automatically.\n"
        "This takes about one to two minutes. Leave the black window open until your browser opens."
    )

    pdf.step_row(
        3,
        "Get your free API key",
        "The app will ask for an API key. This is what connects the app to Google AI. It is free.\n"
        "1. Go to: aistudio.google.com/apikey (or click the link shown in the app).\n"
        "2. Sign in with any Google or Gmail account.\n"
        "3. Click Create API Key.\n"
        "4. Copy the key that appears. It starts with AIza...\n"
        "5. Paste it into the box in the app and click Save and Start."
    )

    pdf.info_box(
        "Your key is saved only on your computer. It is never shared or uploaded anywhere.",
        bg=CARD_BG, text_color=TEXT_MUTED, icon="i"
    )

    pdf.step_row(
        4,
        "Start creating",
        "After saving your key, the main app opens automatically.\n"
        "From this point on, just double-click run.bat (Windows) or run.sh (Mac) each time you want to use it.\n"
        "No repeating the setup."
    )

    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, pdf.h - 6, pdf.w, 6, "F")


    # ── PAGE 3: How to Use ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.fill_bg(*DARK_BG)
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, 0, pdf.w, 4, "F")

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*TEXT_MAIN)
    pdf.cell(0, 9, "How to Use the App", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.accent_line(pdf.l_margin, pdf.get_y(), w=pdf.epw)
    pdf.ln(6)

    use_steps = [
        ("Choose your platform",
         "Select YouTube Long-Form, YouTube Shorts, Instagram Reels, or TikTok."),
        ("Describe your channel",
         "Type a short description of what your channel covers.\n"
         "Example: personal finance tips for people in their 20s"),
        ("Describe your audience",
         "Type who watches your videos.\n"
         "Example: recent graduates who want to start saving but do not know where to begin"),
        ("Click Generate 5 Video Ideas",
         "The AI returns five ranked ideas with a one-line explanation of why each would perform well."),
        ("Pick an idea",
         "Type or paste the title of the idea you want to turn into a full script."),
        ("Choose your video length",
         "Options: 30 seconds, 60 seconds, 3 minutes, 10 minutes, or 20 minutes.\n"
         "The script is sized to match."),
        ("Click Write My Script",
         "The AI writes a complete script: a hook, structured body with on-screen text cues, "
         "a call to action, and a short checklist of personal touches to add in your own voice."),
        ("Download your script",
         "Click the Download Script button to save it as a text file."),
    ]

    for i, (title, detail) in enumerate(use_steps, 1):
        pdf.step_row(i, title, detail)

    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, pdf.h - 6, pdf.w, 6, "F")


    # ── PAGE 4: Troubleshooting ──────────────────────────────────────────────
    pdf.add_page()
    pdf.fill_bg(*DARK_BG)
    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, 0, pdf.w, 4, "F")

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*TEXT_MAIN)
    pdf.cell(0, 9, "Troubleshooting", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.cell(0, 6,
             "Find your message in the left column and follow the steps in the right column.",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.accent_line(pdf.l_margin, pdf.get_y(), w=pdf.epw)
    pdf.ln(5)

    pdf.table_row("Message you see", "What it means", "What to do", header=True)

    rows = [
        ("Python is not installed",
         "Python is missing",
         "Go to python.org/downloads, install it, restart the launcher"),
        ("Python version is too old",
         "Version below 3.9",
         "Download Python 3.11 or newer from python.org"),
        ("Something went wrong while setting up",
         "No internet during install",
         "Check your connection, run the launcher again"),
        ("Paste your free Gemini API key",
         "First run, no key saved",
         "Follow Step 3 in this guide"),
        ("Your API key did not work",
         "Key is wrong or expired",
         "Go to aistudio.google.com/apikey, create a new key"),
        ("Free tier limit hit",
         "Used the AI a lot quickly",
         "Wait 60 seconds, then try again"),
        ("Could not connect to the internet",
         "No network connection",
         "Check Wi-Fi or cable, then try again"),
        ("App closes right away",
         "Port conflict or install error",
         "Close the black window, double-click launcher again"),
    ]

    for c1, c2, c3 in rows:
        pdf.table_row(c1, c2, c3)

    pdf.ln(8)

    pdf.section_title("Tips for Best Results")

    tips = [
        "Be specific when describing your niche and audience. Vague inputs produce generic ideas.",
        "For short-form platforms (Shorts, Reels, TikTok), keep the niche very focused.",
        "If you do not like an idea, click Start Over and run the planner again with a slightly different audience description.",
        "The 'Add Your Own Voice' checklist at the end of each script is important. Use it. Scripts work best when they sound like you.",
        "For YouTube long-form, the 10-minute or 20-minute script options include enough structure for a full tutorial.",
    ]

    for tip in tips:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*PURPLE)
        pdf.cell(5, 6, ".",
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*TEXT_MAIN)
        pdf.multi_cell(0, 5.5, f"  {tip}",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    pdf.ln(6)
    pdf.accent_line(pdf.l_margin, pdf.get_y(), w=pdf.epw)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.cell(0, 6, "Google Gemini Free Tier Limits",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*TEXT_MUTED)
    pdf.multi_cell(0, 5.5,
        "The free API tier allows around 15 requests per minute and 1,500 requests per day. "
        "For a single creator this is more than enough for daily use. "
        "If you hit the limit, the app tells you and shows a countdown timer.",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_fill_color(*PURPLE)
    pdf.rect(0, pdf.h - 6, pdf.w, 6, "F")

    # ── Save ─────────────────────────────────────────────────────────────────
    pdf.output(str(OUTPUT))
    print(f"PDF created: {OUTPUT}")


if __name__ == "__main__":
    build()
