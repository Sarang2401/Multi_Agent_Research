"""
build_guide.py — Converts creator_guide.md into a polished PDF using fpdf2.

Usage: python build_guide.py
Output: output/Creator_Guide.pdf
"""
import os
from pathlib import Path
import markdown
from fpdf import FPDF

# Setup paths
GUIDE_DIR = Path(__file__).parent
OUTPUT_DIR = GUIDE_DIR / "output"
MD_PATH = GUIDE_DIR / "creator_guide.md"
PDF_PATH = OUTPUT_DIR / "Creator_Guide.pdf"

# Create output dir
OUTPUT_DIR.mkdir(exist_ok=True)

if not MD_PATH.exists():
    print(f"Error: {MD_PATH} not found.")
    exit(1)

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

# Convert Markdown to HTML
html_body = markdown.markdown(md_text, extensions=['extra'])

# Create PDF
class GuidePDF(FPDF):
    def header(self):
        # We only want headers on the content pages, not the cover
        if self.page_no() > 1:
            self.set_font("helvetica", "I", 10)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "Creator Strategy Guide: Hitting the Feb 2027 Threshold", border=False, align="R")
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("helvetica", "I", 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = GuidePDF(format="A4")

# --- Cover Page ---
pdf.add_page()
pdf.set_y(80)
pdf.set_font("helvetica", "B", 32)
pdf.set_text_color(30, 30, 30)
pdf.multi_cell(0, 15, "Creator Strategy Guide", align="C")

pdf.set_y(100)
pdf.set_font("helvetica", "", 18)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 10, "Hitting the Feb 2027 Threshold", align="C")

pdf.set_y(150)
pdf.set_font("helvetica", "I", 14)
pdf.set_text_color(150, 150, 150)
pdf.multi_cell(0, 10, "Complete Workflow & System Manual", align="C")

# --- Content Pages ---
pdf.add_page()

# Setup styles for HTML
pdf.set_font("helvetica", size=11)
pdf.set_text_color(40, 40, 40)
# Use a bit of padding between lines
pdf.set_auto_page_break(auto=True, margin=20)

# fpdf2 write_html supports a simple CSS-like dictionary or direct tag parameters, 
# but mostly we rely on the default mapping.
try:
    pdf.write_html(html_body)
except Exception as e:
    print(f"Error rendering HTML: {e}")
    # Fallback to direct text if HTML fails
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 6, md_text)

print(f"Building PDF from {MD_PATH.name}...")
pdf.output(str(PDF_PATH))
print(f"Done! PDF saved to {PDF_PATH}")
