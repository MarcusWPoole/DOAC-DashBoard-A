#!/usr/bin/env bash
# backend/run.sh

# Activate your virtualenv if you use one:
# source .venv/bin/activate

uvicorn main:app --reload --host 127.0.0.1 --port 8000
