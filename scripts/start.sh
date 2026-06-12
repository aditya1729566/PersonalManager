#!/usr/bin/env bash
set -e

# Start the FastAPI app with uvicorn using python -m to avoid PATH issues
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
