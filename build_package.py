"""
build_package.py
Creates the distributable ZIP that you upload to Superprofile.

Usage:
    python build_package.py

Output:
    Social_Media_Script_Generator.zip  (in the same folder as this script)

What goes in the ZIP:
    run.bat, run.sh, all .py source files, requirements.txt,
    .env.example, .streamlit/config.toml, Setup Guide.pdf

What is excluded:
    .env (contains your private API key), .git, __pycache__,
    *.pyc, report_*.md, build_package.py, generate_pdf.py,
    README.md (replaced by the PDF)
"""

import sys
import subprocess
import zipfile
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "Social_Media_Script_Generator.zip"

# Files and directories to include
INCLUDE_FILES = [
    "START HERE.vbs",
    "run.bat",
    "run.sh",
    "streamlit_app.py",
    "config.py",
    "agents.py",
    "tasks.py",
    "crew.py",
    "tools.py",
    "main.py",
    "requirements.txt",
    ".env.example",
]

INCLUDE_DIRS = {
    ".streamlit": ["config.toml"],
}

PDF_NAME = "Setup Guide.pdf"


def check_file(name: str) -> Path:
    p = ROOT / name
    if not p.exists():
        print(f"  MISSING: {name}")
        return None
    return p


def step(msg: str):
    print(f"\n{'='*55}")
    print(f"  {msg}")
    print(f"{'='*55}")


def main():
    print("\n  Social Media Script Generator -- Build Packager")
    print("  " + "-"*50)

    # 1. Generate the PDF first
    step("Step 1/3 -- Generating Setup Guide PDF")
    try:
        result = subprocess.run(
            [sys.executable, "generate_pdf.py"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if result.returncode != 0:
            print(f"  ERROR generating PDF:\n{result.stderr}")
            sys.exit(1)
        print(f"  OK: {result.stdout.strip()}")
    except Exception as e:
        print(f"  ERROR: Could not run generate_pdf.py -- {e}")
        sys.exit(1)

    # 2. Verify all source files exist
    step("Step 2/3 -- Checking source files")
    missing = False
    for name in INCLUDE_FILES:
        p = check_file(name)
        if p:
            print(f"  OK  {name}")
        else:
            missing = True
    if check_file(PDF_NAME):
        print(f"  OK  {PDF_NAME}")
    else:
        missing = True
    for folder, files in INCLUDE_DIRS.items():
        for f in files:
            p = ROOT / folder / f
            if p.exists():
                print(f"  OK  {folder}/{f}")
            else:
                print(f"  MISSING: {folder}/{f}")
                missing = True
    if missing:
        print("\n  Some files are missing. Fix them and run this script again.")
        sys.exit(1)

    # 3. Build the ZIP
    step("Step 3/3 -- Building ZIP")
    if OUT.exists():
        OUT.unlink()
        print(f"  Removed old: {OUT.name}")

    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Source files (at root of ZIP)
        for name in INCLUDE_FILES:
            p = ROOT / name
            zf.write(p, arcname=name)
            print(f"  + {name}")

        # PDF
        pdf_path = ROOT / PDF_NAME
        zf.write(pdf_path, arcname=PDF_NAME)
        print(f"  + {PDF_NAME}")

        # Subdirectories
        for folder, files in INCLUDE_DIRS.items():
            for f in files:
                p = ROOT / folder / f
                zf.write(p, arcname=f"{folder}/{f}")
                print(f"  + {folder}/{f}")

    size_kb = round(OUT.stat().st_size / 1024, 1)
    print(f"\n  Done! Package ready:")
    print(f"  {OUT}")
    print(f"  Size: {size_kb} KB")
    print()
    print("  Next steps:")
    print("  1. Test locally: double-click 'START HERE.vbs' to confirm the app opens.")
    print("  2. Then upload Social_Media_Script_Generator.zip to Superprofile.")
    print()


if __name__ == "__main__":
    main()
