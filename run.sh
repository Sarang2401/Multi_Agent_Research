#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Social Media Script Generator — Mac / Linux Launcher
#  Double-click this file (or run: bash run.sh) to start the app.
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo " ============================================================"
echo "  Social Media Script Generator — Starting up..."
echo " ============================================================"
echo ""

# ── Change to the directory where this script lives ──────────────────────────
cd "$(dirname "$0")"

# ── Check Python is installed ─────────────────────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo " !! Python is not installed on this computer."
    echo ""
    echo " To fix this:"
    echo " 1. Open your web browser and go to:  https://www.python.org/downloads/"
    echo " 2. Download the latest version and run the installer"
    echo " 3. Once installed, close this window and double-click this file again"
    echo ""
    # On Mac, also suggest the built-in way
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo " On Mac, you can also install it by running this in Terminal:"
        echo "   brew install python3"
        echo " (requires Homebrew — see brew.sh if you don't have it)"
        echo ""
    fi
    read -p "Press Enter to close..."
    exit 1
fi

# ── Check Python version is 3.9 or newer ─────────────────────────────────────
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]; }; then
    echo " !! Your Python version ($PYTHON_VERSION) is too old."
    echo ""
    echo " Please download Python 3.11 or newer from:"
    echo " https://www.python.org/downloads/"
    echo " Then close this window and double-click this file again."
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo " Python $PYTHON_VERSION found. Good to go!"
echo ""

# ── Install / update dependencies ────────────────────────────────────────────
echo " Installing required components (this may take a minute on first run)..."
echo " Please wait — do NOT close this window."
echo ""

python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo " !! Something went wrong while setting up the app."
    echo ""
    echo " This is usually caused by no internet connection."
    echo " Please check that you are connected to Wi-Fi or the internet,"
    echo " then close this window and double-click this file again."
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

echo " All components ready!"
echo ""

# ── Launch the app ────────────────────────────────────────────────────────────
echo " Opening the app in your browser..."
echo " (If the browser doesn't open automatically, go to: http://localhost:8501)"
echo ""
echo " To stop the app, press Ctrl+C in this window, or just close it."
echo ""

python3 -m streamlit run streamlit_app.py --server.headless false --browser.gatherUsageStats false

if [ $? -ne 0 ]; then
    echo ""
    echo " !! The app closed unexpectedly."
    echo ""
    echo " Try double-clicking this file again."
    echo " If the problem keeps happening, please contact support."
    echo ""
    read -p "Press Enter to close..."
fi
