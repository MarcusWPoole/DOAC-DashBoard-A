#!/usr/bin/env bash

# Activate the virtual environment
source "$(dirname "$0")/.venv/bin/activate"

# Launch the FastAPI app
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8001