#!/usr/bin/env bash
# Stop the development server started by start.sh
set -e

pkill -f "uvicorn backend.main:app" || true
