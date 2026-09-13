#!/usr/bin/env bash
# ============================================================
#  Pistelle AI  |  Content Intelligence Suite
#  Mac / Linux Launcher
# ============================================================

cd "$(dirname "$0")"

echo ""
echo " ============================================================"
echo "  Pistelle AI  |  Content Intelligence Suite"
echo " ============================================================"
echo ""

if ! command -v python3 &>/dev/null; then
  echo " Python 3 is not installed."
  echo " Install it from: https://www.python.org/downloads/"
  exit 1
fi

PY_OK=$(python3 -c "import sys; print(sys.version_info >= (3,9))")
if [ "$PY_OK" != "True" ]; then
  echo " Your Python version is too old. Please install Python 3.9 or newer."
  exit 1
fi

echo " Python found. Installing / updating dependencies..."
echo ""

python3 -m pip install --upgrade pip --quiet --disable-pip-version-check 2>/dev/null
python3 -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>/dev/null

echo " Dependencies ready."
echo ""
echo " Opening Pistelle AI in your browser..."
echo ""
echo " App address:  http://localhost:8000"
echo ""
echo " ============================================================"
echo "  To stop the app, press Ctrl+C in this window."
echo " ============================================================"
echo ""

(sleep 2 && open "http://localhost:8000" 2>/dev/null || xdg-open "http://localhost:8000" 2>/dev/null) &

python3 -m uvicorn api:app --host 127.0.0.1 --port 8000
