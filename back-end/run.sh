#!/bin/bash

# Exit immediately if any command fails
set -e

# !!Ensure virtural environment is running - uncomment first line
python3 -m venv .venv
source .venv/bin/activate

# !!Upgrade pip - add back if first run
pip install --upgrade pip

# !!Ensure required packages are installed - add back if first run

pip install -r requirements.txt

# Launch the FastAPI app
uvicorn main:app --reload --host 127.0.0.1 --port 8001